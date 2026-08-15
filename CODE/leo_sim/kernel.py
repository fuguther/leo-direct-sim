"""Bounded SimPy discrete-event kernel for leo_sim V2.

Formal data path (no Gateway anywhere):
immutable trace -> sparse TrafficEndpoint -> finite association (K access
slots, acquisition delay) -> satellite ingress -> dynamic finite ISL ->
arrived-control local cache -> legal egress discovery (destination endpoint
must be actively associated and served) -> finite downlink -> destination
TrafficEndpoint.

Fair finite access: endpoints request association from CURRENT demand
(queued uplink packets, or a satellite holding this endpoint's downlink
traffic). Free slots are granted immediately (pre-positioning when nothing
contends). Under contention each satellite keeps a deterministic FIFO wait
queue; holders rotate out when (a) their association exceeds slot_lease_s
(graceful retire: packets assigned while the link was active drain, the
retirement deadline is the hard backstop and races any in-flight service),
or (b) they have been idle for idle_release_s. Rotation period per holder is
bounded by slot_lease_s + min(assigned-backlog drain, retirement_deadline_s)
+ acquisition_delay_s, so a waiting demanding endpoint is served within
queue-position x that bound.

Transmission race semantics: every service races (a) service completion,
(b) certified deterministic geometry loss, (c) Gilbert-Elliott outage,
(d) data deadline, (e) hard link retirement. GE trajectories are
continuous-time two-state processes with exponential dwells on private
per-link RNG streams, so outcomes never depend on query patterns. A failure
mid-flight counts only the service time already occupied; no implicit
pause/resume, no ARQ. A hard-retired packet is requeued in full (the partial
transmission never reached the receiver, so this is not a duplicate send);
its occupied time stays accounted and it keeps exactly one eventual fate.
Deadlines are enforced again after each propagation segment.

Horizon: the closed interval [0, duration_s]; a dedicated closer process
guarantees the clock reaches the exact horizon, where in-service occupation,
queue areas and IN_SYSTEM_AT_STOP all settle.

GSL uplink and downlink are explicit full-duplex resources: separate
capacities, each shared across endpoints by deficit round-robin (DRR) with a
configured quantum. ISL queues are per-direction with a single capacity
shared by data and control; control has non-preemptive priority.
"""
from __future__ import annotations

import math
import hashlib
from collections import deque

import numpy as np
import simpy

from . import control, fates, grid as gridmod, learning as _learning, model
from . import outage, rng as rngmod, routing
from . import trace as tracemod

LearningUnavailable = _learning.LearningUnavailable


class KernelError(RuntimeError):
    pass


class CapExceeded(KernelError):
    """A configured bound (events/entities/packets) was exceeded. Fail closed."""


class DataPacket:
    __slots__ = ("pid", "src", "dst", "bits", "deadline", "emitted_at", "path",
                 "assigned_sat", "learning_state", "learning_action",
                 "learning_reward", "isl_enqueued_at")

    def __init__(self, pid, src, dst, bits, deadline, emitted_at):
        self.pid = pid
        self.src = src
        self.dst = dst
        self.bits = bits
        self.deadline = deadline
        self.emitted_at = emitted_at
        self.path: list[int] = []
        self.assigned_sat: int | None = None
        self.learning_state = None
        self.learning_action = None
        self.learning_reward = None
        # enqueue time on the current ISL egress queue; the realized queue
        # wait (service start minus this) feeds the M1 queue reward
        self.isl_enqueued_at = None


class QueueArea:
    """Exact queued-bits x seconds integral. Mutations call add/remove with
    the current time; close(t) settles the integral at the stop time."""

    __slots__ = ("area", "bits", "last")

    def __init__(self):
        self.area = 0.0
        self.bits = 0
        self.last = 0.0

    def _acc(self, now: float):
        self.area += self.bits * (now - self.last)
        self.last = now

    def add(self, bits: int, now: float):
        self._acc(now)
        self.bits += bits

    def remove(self, bits: int, now: float):
        self._acc(now)
        self.bits -= bits

    def close(self, t: float):
        self._acc(t)


class ControlPacket:
    """A real control-plane packet (the task contract: origin, sequence,
    generated_at, received_at, ttl, remaining_hops, payload_bits,
    validity/AoI).

    received_at is None until the packet physically arrives at a receiving
    satellite; the arrival path sets it and records it in the control ledger.
    valid_at(t) is the TTL window from generation — the same rule the
    receiving cache enforces on arrived entries; AoI at any instant is
    t - generated_at (surfaced via the cache entry on arrival).
    """

    __slots__ = ("iid", "origin", "seq", "generated_at", "_received_at",
                 "ttl_s", "remaining_hops", "payload_bits", "payload")

    def __init__(self, iid, origin, seq, generated_at, ttl_s, remaining_hops,
                 bits, payload):
        if not isinstance(generated_at, (int, float)) \
                or isinstance(generated_at, bool) \
                or not math.isfinite(generated_at) or generated_at < 0:
            raise ValueError("ControlPacket generated_at must be finite and >= 0")
        if not isinstance(ttl_s, (int, float)) or isinstance(ttl_s, bool) \
                or not math.isfinite(ttl_s) or ttl_s <= 0:
            raise ValueError("ControlPacket ttl_s must be finite and > 0")
        if not isinstance(remaining_hops, int) \
                or isinstance(remaining_hops, bool) or remaining_hops < 0:
            raise ValueError("ControlPacket remaining_hops must be a non-negative int")
        if not isinstance(bits, int) or isinstance(bits, bool) or bits <= 0:
            raise ValueError("ControlPacket payload_bits must be a positive int")
        self.iid = iid
        self.origin = origin
        self.seq = seq
        self.generated_at = float(generated_at)
        self._received_at = None
        self.ttl_s = float(ttl_s)
        self.remaining_hops = remaining_hops
        self.payload_bits = bits
        self.payload = payload

    @property
    def bits(self) -> int:
        """Compatibility alias; payload_bits is the authoritative field."""
        return self.payload_bits

    @property
    def received_at(self) -> float | None:
        return self._received_at

    def mark_received(self, t: float) -> None:
        if self._received_at is not None:
            raise ValueError("ControlPacket received_at may only be set once")
        if not isinstance(t, (int, float)) or isinstance(t, bool) \
                or not math.isfinite(t) or t < self.generated_at:
            raise ValueError(
                "ControlPacket received_at must be finite and >= generated_at")
        self._received_at = float(t)

    def valid_at(self, t: float) -> bool:
        return self.generated_at <= t <= self.generated_at + self.ttl_s

    def aoi(self, t: float) -> float:
        if not isinstance(t, (int, float)) or isinstance(t, bool) \
                or not math.isfinite(t) or t < self.generated_at:
            raise ValueError("ControlPacket AoI time must be finite and >= generated_at")
        return float(t) - self.generated_at


class Link:
    """Endpoint<->satellite association state.

    cause: what put the link into retiring ("mbb" | "lease"); interrupt fires
    at retire_at so an in-flight service races the hard retirement deadline.
    """

    __slots__ = ("sat", "state", "since", "ready_at", "retire_at", "cause",
                 "interrupt")

    def __init__(self, sat, state, since, ready_at=0.0, retire_at=None,
                 cause=None, interrupt=None):
        self.sat = sat
        self.state = state  # acquiring | active | retiring
        self.since = since
        self.ready_at = ready_at
        self.retire_at = retire_at
        self.cause = cause
        self.interrupt = interrupt


class TrafficEndpoint:
    __slots__ = ("cell", "lat", "lon", "queue", "queued_bits", "links", "area")

    def __init__(self, cell):
        self.cell = cell
        self.lat, self.lon = gridmod.grid_center(cell)
        self.queue: deque[DataPacket] = deque()
        self.queued_bits = 0
        self.links: dict[int, Link] = {}
        self.area = QueueArea()

    def primary_link(self) -> Link | None:
        """The newest non-retiring link, if any."""
        best = None
        for link in self.links.values():
            if link.state in ("active", "acquiring"):
                if best is None or link.since >= best.since:
                    best = link
        return best


class _DRRMixin:
    """Deficit round-robin selection with a configured quantum."""

    def _drr_init(self, quantum: int):
        self.quantum = float(quantum)
        self.deficit: dict[str, float] = {}
        self.rr_cursor = 0

    def _drr_select(self, items, pick):
        """items: sorted keys; pick(key) -> head packet or None.

        Deficit round-robin: visits backlogged keys in rotating order, adds
        one quantum per visit, and serves the head packet when it fits the
        deficit. Packets larger than the quantum accumulate deficit over
        several visits, so bit-level fairness holds for heterogeneous packet
        sizes and no oversize packet can deadlock the server.
        Returns (key, pkt) or None.
        """
        avail = [(k, pick(k)) for k in items]
        avail = [(k, p) for k, p in avail if p is not None]
        if not avail:
            return None
        n = len(avail)
        while True:
            start = self.rr_cursor % n
            for offset in range(n):
                i = (start + offset) % n
                k, pkt = avail[i]
                dc = self.deficit.get(k, 0.0) + self.quantum
                self.deficit[k] = dc
                if pkt.bits <= dc:
                    self.deficit[k] = dc - pkt.bits
                    self.rr_cursor = i + 1
                    return k, pkt

class UplinkServer(_DRRMixin):
    """Shared GSL uplink service: DRR over associated endpoints."""

    def __init__(self, kern, sat):
        self.k = kern
        self.sat = sat
        self.wake = kern.env.event()
        self.current: tuple[TrafficEndpoint, DataPacket] | None = None
        self._svc = None
        self._drr_init(kern.cfg_access["drr_quantum_bits"])
        kern.env.process(self._run())

    def _pick(self, ep: TrafficEndpoint):
        """First queued packet this link may serve (per-link FIFO preserved)."""
        link = ep.links.get(self.sat)
        if link is None or link.state not in ("active", "retiring"):
            return None
        if link.state == "retiring" and self.k.env.now >= link.retire_at:
            return None
        for p in ep.queue:
            if link.state == "retiring":
                if p.assigned_sat == self.sat:
                    return p
            elif p.assigned_sat in (None, self.sat):
                return p
        return None

    def _run(self):
        k = self.k
        while True:
            cells = sorted(ep.cell for ep in k.endpoints.values())
            sel = self._drr_select(cells, lambda c: self._pick(k.endpoints[c]))
            if sel is None:
                yield self.wake
                self.wake = k.env.event()
                continue
            cell, pkt = sel
            ep = k.endpoints[cell]
            ep.queue.remove(pkt)
            ep.queued_bits -= pkt.bits
            ep.area.remove(pkt.bits, k.env.now)
            if pkt.assigned_sat is None:
                pkt.assigned_sat = self.sat
            self.current = (ep, pkt)
            k._note_busy(cell)
            k.service_log["uplink"].append((cell, pkt.pid))
            dur = pkt.bits / k.ul_rate_bps
            self._svc = (k.env.now, "gsl_uplink_s")
            outcome = yield k.env.process(
                k._transmit(dur, pkt, ("gsl", self.sat, ep, ep.links.get(self.sat)),
                            "gsl_uplink_s"))
            k.service_log["uplink_bits"].append((k.env.now, cell, pkt.bits))
            self._svc = None
            self.current = None
            if outcome == "retired":
                # hard retirement mid-service: the partial transmission never
                # reached the satellite, so requeueing the full packet at the
                # head for the new link is NOT a duplicate send; the occupied
                # service time is already accounted.
                pkt.assigned_sat = None
                ep.queue.appendleft(pkt)
                ep.queued_bits += pkt.bits
                ep.area.add(pkt.bits, k.env.now)
                k._note_busy(cell)
                k._on_link_retired(ep, self.sat)
                for sat_id in list(ep.links):
                    k._poke(k.uplinks[sat_id].wake)
                continue
            if outcome == "stalled":
                ep.queue.appendleft(pkt)
                ep.queued_bits += pkt.bits
                ep.area.add(pkt.bits, k.env.now)
                if k.env.now >= k.horizon:
                    # No service can start past the horizon: requeue and stop
                    # retrying in the same time slice, or the process loops
                    # forever with no event to advance the clock.
                    break
                yield self.wake
                self.wake = k.env.event()
                continue
            if outcome != "ok":
                continue
            now = k.env.now
            prop = model.propagation_delay_s(
                k.geometry.slant_range_km(self.sat, ep.lat, ep.lon, now))
            k.env.process(k._ingress_after_prop(pkt, self.sat, prop))


class DownlinkServer(_DRRMixin):
    """Shared GSL downlink service: finite shared queue, DRR over endpoints."""

    def __init__(self, kern, sat):
        self.k = kern
        self.sat = sat
        self.queues: dict[str, deque[DataPacket]] = {}
        self.queued_bits = 0
        self.area = QueueArea()
        self.wake = kern.env.event()
        self.current: DataPacket | None = None
        self._svc = None
        self._drr_init(kern.cfg_access["drr_quantum_bits"])
        kern.env.process(self._run())

    def room(self, bits: int) -> bool:
        return self.queued_bits + bits <= self.k.cfg_access["downlink_queue_bits"]

    def put(self, pkt: DataPacket) -> None:
        self.queues.setdefault(pkt.dst, deque()).append(pkt)
        self.queued_bits += pkt.bits
        self.area.add(pkt.bits, self.k.env.now)
        self.k._note_busy(pkt.dst)
        self.k._poke(self.wake)

    def _servable(self, cell):
        """Head packet if this satellite may legally serve the endpoint now."""
        q = self.queues.get(cell)
        if not q:
            return None
        ep = self.k.endpoints[cell]
        link = ep.links.get(self.sat)
        if link is None or link.state not in ("active", "retiring"):
            return None
        if link.state == "retiring" and self.k.env.now >= link.retire_at:
            return None
        if not self.k.geometry.gsl_available(self.sat, ep.lat, ep.lon, self.k.env.now):
            return None
        return q[0]

    def _run(self):
        k = self.k
        while True:
            cells = sorted(c for c, q in self.queues.items() if q)
            # packets whose endpoint lost this association go back to pending
            for c in cells:
                if self.queues[c] and self._servable(c) is None:
                    ep = k.endpoints[c]
                    link = ep.links.get(self.sat)
                    if link is None or link.state not in ("active", "retiring"):
                        pkt = self.queues[c].popleft()
                        self.queued_bits -= pkt.bits
                        self.area.remove(pkt.bits, k.env.now)
                        k.pending[self.sat].append(pkt)
            sel = self._drr_select(cells, self._servable)
            if sel is None:
                yield self.wake
                self.wake = k.env.event()
                continue
            cell, pkt = sel
            self.queues[cell].popleft()
            self.queued_bits -= pkt.bits
            self.area.remove(pkt.bits, k.env.now)
            self.current = pkt
            ep = k.endpoints[cell]
            k.service_log["downlink"].append((cell, pkt.pid))
            dur = pkt.bits / k.dl_rate_bps
            self._svc = (k.env.now, "gsl_downlink_s")
            outcome = yield k.env.process(
                k._transmit(dur, pkt, ("gsl", self.sat, ep, ep.links.get(self.sat)),
                            "gsl_downlink_s"))
            self._svc = None
            self.current = None
            if outcome == "retired":
                # partial downlink never reached the endpoint: re-decide at
                # this satellite (the destination holds a new association).
                k.pending[self.sat].append(pkt)
                k._on_link_retired(ep, self.sat)
                continue
            if outcome == "stalled":
                self.queues[cell].appendleft(pkt)
                self.queued_bits += pkt.bits
                self.area.add(pkt.bits, k.env.now)
                if k.env.now >= k.horizon:
                    break
                yield self.wake
                self.wake = k.env.event()
                continue
            if outcome != "ok":
                continue
            now = k.env.now
            prop = model.propagation_delay_s(
                k.geometry.slant_range_km(self.sat, ep.lat, ep.lon, now))
            k.env.process(k._deliver_after_prop(pkt, self.sat, prop))


class ISLLink:
    """One directional ISL: ONE finite queue capacity shared by data and
    control, control with non-preemptive priority (queued control overtakes
    queued data when the link next goes idle; a packet in service is never
    interrupted). Availability is re-checked at every use."""

    def __init__(self, kern, sat, direction, peer):
        self.k = kern
        self.sat = sat
        self.dir = direction
        self.peer = peer
        self.data_q: deque[DataPacket] = deque()
        self.ctrl_q: deque[ControlPacket] = deque()
        self.data_bits = 0
        self.ctrl_bits = 0
        self.data_area = QueueArea()
        self.ctrl_area = QueueArea()
        self.wake = kern.env.event()
        self._svc = None
        ge_cfg = kern.cfg_links["ge_isl"]
        self.ge = outage.GilbertElliott(
            ge_cfg["mean_good_s"], ge_cfg["mean_bad_s"],
            rngmod.link_stream(kern.cfg_sc["seed"], f"isl:{sat}:{direction}"),
            enabled=kern.ge_enabled)
        kern.env.process(self._run())

    def _used(self) -> int:
        return self.data_bits + self.ctrl_bits

    def room(self, bits: int) -> bool:
        return self._used() + bits <= self.k.cfg_links["isl_queue_bits"]

    def available_now(self) -> bool:
        k = self.k
        if k.ge_enabled and self.ge.is_down(k.env.now):
            return False
        return k.geometry.isl_available(self.sat, self.peer, k.env.now)

    def put_data(self, pkt: DataPacket) -> None:
        pkt.isl_enqueued_at = self.k.env.now
        self.data_q.append(pkt)
        self.data_bits += pkt.bits
        self.data_area.add(pkt.bits, self.k.env.now)
        self.k._poke(self.wake)

    def put_ctrl(self, pkt: ControlPacket) -> None:
        self.ctrl_q.append(pkt)
        self.ctrl_bits += pkt.bits
        self.ctrl_area.add(pkt.bits, self.k.env.now)
        self.k._poke(self.wake)

    def _run(self):
        k = self.k
        while True:
            self._expire_waiting()
            if not self.ctrl_q and not self.data_q:
                yield self.wake
                self.wake = k.env.event()
                continue
            if not self.available_now():
                # link down right now: wait for the earliest recovery
                ups = [k.geometry.next_isl_change(self.sat, self.peer,
                                                 k.env.now, k.horizon)]
                if k.ge_enabled:
                    ups.append(self.ge.next_up(k.env.now))
                ups = [u for u in ups if u is not None]
                expiries = [p.generated_at + p.ttl_s for p in self.ctrl_q]
                expiries.extend(p.deadline for p in self.data_q
                                if p.deadline is not None)
                waits = [u for u in ups + expiries
                         if k.env.now < u <= k.horizon]
                if not waits:
                    yield self.wake
                    self.wake = k.env.event()
                    continue
                timeout = k.env.timeout(max(0.0, min(waits) - k.env.now))
                yield timeout | self.wake
                if self.wake.triggered:
                    self.wake = k.env.event()
                continue
            is_ctrl = bool(self.ctrl_q)
            pkt = self.ctrl_q.popleft() if is_ctrl else self.data_q.popleft()
            if is_ctrl:
                self.ctrl_bits -= pkt.bits
                self.ctrl_area.remove(pkt.bits, k.env.now)
                k.mech["control_tx_started"] += 1
            else:
                self.data_bits -= pkt.bits
                self.data_area.remove(pkt.bits, k.env.now)
            k.service_log["isl"].append(("ctrl" if is_ctrl else "data",
                                         pkt.iid if is_ctrl else pkt.pid))
            dur = pkt.bits / k.isl_rate_bps
            occ = "ctrl_isl_s" if is_ctrl else "isl_s"
            self._svc = (k.env.now, occ)
            outcome = yield k.env.process(
                k._transmit(dur, pkt, ("isl", self.sat, self.peer, self.ge), occ))
            self._svc = None
            if outcome == "stalled":
                if is_ctrl:
                    self.ctrl_q.appendleft(pkt)
                    self.ctrl_bits += pkt.bits
                    self.ctrl_area.add(pkt.bits, k.env.now)
                else:
                    self.data_q.appendleft(pkt)
                    self.data_bits += pkt.bits
                    self.data_area.add(pkt.bits, k.env.now)
                if k.env.now >= k.horizon:
                    break
                yield self.wake
                self.wake = k.env.event()
                continue
            if outcome != "ok":
                continue
            if is_ctrl:
                k.mech["control_tx_completed"] += 1
            now = k.env.now
            prop = model.propagation_delay_s(
                k.geometry.isl_range_km(self.sat, self.peer, now))
            if is_ctrl:
                k.env.process(k._ctrl_arrive_after_prop(pkt, self.sat, self.peer, prop))
            else:
                k.env.process(k._isl_arrive_after_prop(pkt, self.peer, prop))

    def _expire_waiting(self) -> None:
        """Retire queued packets at their own deadline/TTL even while an ISL
        is down forever.  Queue residence is part of the information/link
        model and cannot silently turn an expired packet into IN_SYSTEM."""
        now = self.k.env.now
        kept_ctrl = deque()
        for pkt in self.ctrl_q:
            if now >= pkt.generated_at + pkt.ttl_s:
                self.ctrl_bits -= pkt.bits
                self.ctrl_area.remove(pkt.bits, now)
                self.k._fail(pkt, "CONTROL_EXPIRED")
            else:
                kept_ctrl.append(pkt)
        self.ctrl_q = kept_ctrl
        kept_data = deque()
        for pkt in self.data_q:
            if pkt.deadline is not None and now >= pkt.deadline:
                self.data_bits -= pkt.bits
                self.data_area.remove(pkt.bits, now)
                self.k._fail(pkt, "DATA_DEADLINE_EXPIRED")
            else:
                kept_data.append(pkt)
        self.data_q = kept_data


class Kernel:
    def __init__(self, resolved: dict, rows: list[dict], geometry=None,
                 learning_out_dir=None, decision_sink=None):
        cfg = resolved["config"]
        self.resolved = resolved
        self.cfg_sc = cfg["scenario"]
        self.cfg_access = cfg["access"]
        self.cfg_links = cfg["links"]
        self.cfg_cp = cfg["control_plane"]
        self.cfg_rt = cfg["routing"]
        self.cfg_learning = cfg["learning"]
        self.cfg_ex = cfg["execution"]
        self.horizon = float(self.cfg_sc["duration_s"])
        self.time_step = float(self.cfg_sc["time_step_s"])
        self.env = simpy.Environment()
        self.learning_gate(cfg)
        self.learning_out_dir = learning_out_dir
        self.learner = (
            _learning.TensorflowDDQN(
                self.cfg_rt["contract"], cfg["learning"],
                cfg["learning"]["seed"]
                if cfg["learning"]["seed"] is not None
                else self.cfg_sc["seed"])
            if cfg["learning"]["algorithm"] == "ddqn" else None
        )

        if geometry is None:
            geometry = model.Constellation(
                self.cfg_sc["num_satellites"], self.cfg_sc["num_planes"],
                self.cfg_sc["altitude_km"], self.cfg_sc["inclination_deg"],
                self.cfg_sc["min_elevation_deg"],
                max_isl_km=self.cfg_links["max_isl_km"])
        if self.cfg_links["geometry_loss"] and not getattr(
                geometry, "certifies_change_times", False):
            # a provider that cannot authoritatively answer "next availability
            # change" would force the kernel to guess link continuity inside
            # service intervals; fail closed instead.
            raise KernelError(
                "geometry provider does not certify next-change times; "
                "failing closed (set links.geometry_loss=false only for "
                "diagnostic runs)")
        self.geometry = geometry
        self.num_sats = geometry.num_satellites
        # optional output-only per-hop decision snapshot sink (a list); when
        # None the recording code paths are never entered
        self.decision_sink = decision_sink

        self.ge_enabled = bool(self.cfg_links["ge_enabled"])

        self.ul_rate_bps = self.cfg_access["uplink_rate_mbps"] * 1e6
        self.dl_rate_bps = self.cfg_access["downlink_rate_mbps"] * 1e6
        self.isl_rate_bps = self.cfg_links["isl_rate_mbps"] * 1e6

        # sparse activation: only trace-active cells become endpoints; every
        # row passes the unified packet-row contract regardless of its origin
        rows = sorted(rows, key=lambda r: (r["emit_time_s"], r["packet_id"]))
        tracemod.validate_packet_rows(
            rows, horizon_s=self.horizon,
            max_packets=self.cfg_ex["max_packets"])
        self.endpoints: dict[str, TrafficEndpoint] = {}
        per_ep_rows: dict[str, list[dict]] = {}
        for r in rows:
            for c in (r["src_grid_id"], r["dst_grid_id"]):
                if c not in self.endpoints:
                    self.endpoints[c] = TrafficEndpoint(c)
            per_ep_rows.setdefault(r["src_grid_id"], []).append(r)

        self.topo = routing.build_topology(
            geometry, self.num_sats, self.cfg_links["isl_dirs"])
        self.control_children = [
            routing.control_broadcast_children(
                self.topo, origin, self.cfg_cp["vis_k"])
            for origin in range(self.num_sats)
        ] if self.cfg_cp["enabled"] and self.cfg_cp["vis_k"] > 0 else []

        # per-satellite state
        self.slots: list[set[str]] = [set() for _ in range(self.num_sats)]
        self.caches: list[control.LocalCache] = [control.LocalCache() for _ in range(self.num_sats)]
        self.pending: list[list[DataPacket]] = [[] for _ in range(self.num_sats)]
        self.seen_ctrl: list[set[tuple[int, int]]] = [set() for _ in range(self.num_sats)]
        self.gsl_ge: dict[tuple[int, str], outage.GilbertElliott] = {}

        # fair access state: per-satellite FIFO wait queues (cell -> request
        # time), endpoint last-activity tracking, and admission/occupancy
        # accounting
        self.access_wait: list[dict[str, float]] = [dict() for _ in range(self.num_sats)]
        self.access_last_busy: dict[str, float] = {}
        self.access_stats = {
            "requests": 0, "grants": 0, "preposition_grants": 0,
            "wait_time_s_total": 0.0, "wait_time_s_max": 0.0,
            "slot_hold_s_total": 0.0, "waiting_at_stop": 0,
            "releases": {},
        }

        n_entities = len(self.endpoints) + self.num_sats
        self.uplinks = [UplinkServer(self, s) for s in range(self.num_sats)]
        self.downlinks = [DownlinkServer(self, s) for s in range(self.num_sats)]
        self.isls: list[dict[str, ISLLink]] = [{} for _ in range(self.num_sats)]
        for s in range(self.num_sats):
            for d, n in self.topo[s].items():
                self.isls[s][d] = ISLLink(self, s, d, n)
                n_entities += 1
        if n_entities > self.cfg_ex["max_entities"]:
            raise CapExceeded(f"entities {n_entities} > max_entities")

        self.ledger = fates.DataFateLedger()
        self.ctrl_ledger = fates.ControlFateLedger()
        self.deliveries: dict[int, dict] = {}
        self.occupied = {"gsl_uplink_s": 0.0, "gsl_downlink_s": 0.0,
                         "isl_s": 0.0, "ctrl_isl_s": 0.0}
        self.service_log = {"uplink": [], "downlink": [], "isl": [],
                            "uplink_bits": []}
        self.handover_events: list[dict] = []
        self.monitor_log: list[tuple] = []
        self.monitor = bool(self.cfg_ex["monitor"])
        self.data_packet_count = 0
        self.ctrl_seq = 0
        self.ctrl_iid = 0
        self.mech = {
            "ge_gsl_queries": 0, "ge_isl_queries": 0,
            "ge_waits": 0, "ge_failures": 0,
            "control_snapshots": 0,
            "control_registered": 0,
            "control_entered_queue": 0,
            "control_tx_started": 0,
            "control_tx_completed": 0,
            "control_initialized": bool(self.cfg_cp["enabled"]),
            "ge_initialized": self.ge_enabled,
            "mbb_events": 0,
            "learning_initialized": self.learner is not None,
            "learning_decisions": 0,
            "learning_transitions": 0,
            "learning_train_steps": 0,
        }
        self.closed_at: float | None = None

        # process creation order fixes same-time ordering: handover ticks and
        # control advertisers at t=0 precede emissions at t=0. The horizon
        # closer is created last; events AT the horizon are still processed
        # (closed interval [0, horizon]) and final accounting settles at the
        # exact horizon, never at an incidental last-event time.
        for cell in sorted(self.endpoints):
            self.env.process(self._endpoint_ticker(self.endpoints[cell]))
        if self.cfg_cp["enabled"] and self.cfg_cp["vis_k"] > 0:
            for s in range(self.num_sats):
                self.env.process(self._control_advertiser(s))
        for cell in sorted(per_ep_rows):
            self.env.process(self._emitter(self.endpoints[cell], per_ep_rows[cell]))
        for s in range(self.num_sats):
            self.env.process(self._pending_ticker(s))
        self.env.process(self._horizon_closer())

    # ------------------------------------------------------------------ util
    @staticmethod
    def learning_gate(cfg):
        requested = (cfg["routing"]["learning_enabled"]
                     or cfg["learning"]["algorithm"] != "none")
        if requested:
            _learning.require_tensorflow()

    def _poke(self, event):
        if not event.triggered:
            event.succeed()

    def _note_busy(self, cell: str):
        """Last-activity stamp for fair-access idle measurement."""
        self.access_last_busy[cell] = self.env.now

    def _log(self, kind, **kv):
        if self.monitor:
            self.monitor_log.append((self.env.now, kind, tuple(sorted(kv.items()))))

    def _count_data_packet(self):
        """Enforce the trace/data-packet cap.

        Control instances are bounded by max_events and their finite queues;
        counting them here made a valid, already max_packets-validated trace
        fail merely because the control plane advertised for a long horizon.
        """
        self.data_packet_count += 1
        if self.data_packet_count > self.cfg_ex["max_packets"]:
            raise CapExceeded("max_packets exceeded")

    def _gsl_ge(self, sat: int, cell: str) -> outage.GilbertElliott:
        key = (sat, cell)
        ge = self.gsl_ge.get(key)
        if ge is None:
            cfg = self.cfg_links["ge_gsl"]
            ge = outage.GilbertElliott(
                cfg["mean_good_s"], cfg["mean_bad_s"],
                rngmod.link_stream(self.cfg_sc["seed"], f"gsl:{sat}:{cell}"),
                enabled=self.ge_enabled)
            self.gsl_ge[key] = ge
        return ge

    # --------------------------------------------------------- transmission
    def _fire_interrupt(self, link: Link, at: float):
        yield self.env.timeout(max(0.0, at - self.env.now))
        if not link.interrupt.triggered:
            link.interrupt.succeed()

    def _transmit(self, dur: float, pkt, link_ref, occ_key: str):
        """Race service completion vs geometry loss vs GE outage vs deadline
        vs (GSL only) hard link retirement.

        link_ref: ("gsl", sat, endpoint, link) or ("isl", a, b, ge). Returns
        "ok" only if the full service completed with the link continuously up;
        "retired" when the hard retirement deadline fired mid-service (no
        fate: the sender requeues the never-completed packet); "stalled" when
        the link never comes back before the horizon (no fate: the packet
        returns to its queue and settles as IN_SYSTEM_AT_STOP); otherwise the
        packet gets exactly one fate and only the service time already
        occupied is accounted. A link that is down before any service begins
        simply defers the start (this is not pause/resume: no transmission
        has started yet, so nothing is resumed).
        """
        link = None
        if link_ref[0] == "gsl":
            _, sat, ep, link = link_ref
            ge = self._gsl_ge(sat, ep.cell)

            def avail(x):
                return self.geometry.gsl_available(sat, ep.lat, ep.lon, x)

            def next_change(a, b):
                return self.geometry.next_gsl_change(sat, ep.lat, ep.lon, a, b)
        else:
            _, a, b, ge = link_ref

            def avail(x):
                return self.geometry.isl_available(a, b, x)

            def next_change(x, y):
                return self.geometry.next_isl_change(a, b, x, y)

        ge_q_key = "ge_gsl_queries" if link_ref[0] == "gsl" else "ge_isl_queries"
        if isinstance(pkt, ControlPacket):
            expiry = pkt.generated_at + pkt.ttl_s
            expiry_fate = "CONTROL_EXPIRED"
        else:
            expiry = pkt.deadline
            expiry_fate = "DATA_DEADLINE_EXPIRED"
        while True:
            t0 = self.env.now
            if self.ge_enabled:
                self.mech[ge_q_key] += 1
            geom_up = (not self.cfg_links["geometry_loss"]) or avail(t0)
            ge_up = (not self.ge_enabled) or not ge.is_down(t0)
            retire_t = None
            if (link is not None and link.state == "retiring"
                    and link.retire_at is not None):
                retire_t = link.retire_at
                if retire_t <= t0:
                    return "retired"  # no service may start past the deadline
            if not (geom_up and ge_up):
                ups = []
                if not geom_up:
                    nxt = next_change(t0, self.horizon)
                    if nxt is not None:
                        ups.append(nxt)
                if not ge_up:
                    ups.append(ge.next_up(t0))
                    self.mech["ge_waits"] += 1
                if expiry is not None and (not ups or min(ups) >= expiry):
                    self._fail(pkt, expiry_fate)
                    return "fail"
                if not ups:
                    # never available again within the horizon: settle the
                    # packet back in its queue at the exact horizon
                    if t0 >= self.horizon:
                        return "stalled"
                    yield self.env.timeout(max(0.0, self.horizon - t0))
                    if self.env.now >= self.horizon:
                        return "stalled"
                    continue
                yield self.env.timeout(max(0.0, min(ups) - t0))
                continue
            end = t0 + dur
            if (link_ref[0] == "isl" and isinstance(pkt, DataPacket)
                    and pkt.learning_state is not None
                    and pkt.isl_enqueued_at is not None):
                # M1 queue reward: settle the packet's REALIZED queue wait at
                # the instant its service actually starts (legacy analog:
                # checkPointsSend - checkPoints, SimulationRL.py:2052).
                pkt.learning_reward = _learning.queue_reward(
                    t0 - pkt.isl_enqueued_at,
                    self.cfg_learning["reward_w1"],
                    self.cfg_learning["reward_beta"])
                pkt.isl_enqueued_at = None
            fail_t, fail_kind = end, None
            if self.cfg_links["geometry_loss"]:
                nxt = next_change(t0, end)
                if nxt is not None and nxt < fail_t:
                    fail_t, fail_kind = nxt, "GEOMETRY_LOSS_IN_FLIGHT"
            if self.ge_enabled:
                gd = ge.next_down(t0)
                if gd < fail_t:
                    fail_t, fail_kind = gd, "RANDOM_OUTAGE_IN_FLIGHT"
            if expiry is not None and expiry < fail_t:
                fail_t, fail_kind = expiry, expiry_fate
            if retire_t is not None and retire_t < fail_t:
                fail_t, fail_kind = retire_t, "RETIRE"
            # race the wait against a possibly later-scheduled retirement
            # interrupt: on ANY wake the whole race is recomputed from now.
            interrupt = link.interrupt if link is not None else None
            wait = self.env.timeout(max(0.0, fail_t - t0))
            if interrupt is not None and not interrupt.triggered:
                yield wait | interrupt
            else:
                yield wait
            self.occupied[occ_key] += self.env.now - t0
            if self.env.now < fail_t - 1e-12:
                continue  # woken by the interrupt: recompute the race
            if fail_kind is None:
                return "ok"
            if fail_kind == "RETIRE":
                return "retired"
            if fail_kind == "RANDOM_OUTAGE_IN_FLIGHT":
                self.mech["ge_failures"] += 1
            self._fail(pkt, fail_kind)
            return "fail"

    # ------------------------------------------------------------- processes
    def _horizon_closer(self):
        """Guarantees the simulation clock reaches the exact horizon, so
        final accounting (in-service occupation, queue areas, IN_SYSTEM)
        settles at the configured horizon, never at a stray last event."""
        yield self.env.timeout(self.horizon)
        self.closed_at = self.env.now

    def _emitter(self, ep: TrafficEndpoint, rows):
        for r in rows:
            delay = r["emit_time_s"] - self.env.now
            if delay > 0:
                yield self.env.timeout(delay)
            self._count_data_packet()
            pkt = DataPacket(r["packet_id"], r["src_grid_id"], r["dst_grid_id"],
                             r["bits"], r["deadline_at_s"], self.env.now)
            self.ledger.register(pkt.pid, pkt.bits)
            now = self.env.now
            if pkt.deadline is not None and now > pkt.deadline:
                self._fail(pkt, "DATA_DEADLINE_EXPIRED")
                continue
            link = ep.primary_link()
            if link is None and not self._visible_sats(ep):
                # no satellite is visible at all at emission time: the
                # endpoint is not part of the network for this packet
                self._fail(pkt, "ACCESS_REJECTED")
                continue
            if ep.queued_bits + pkt.bits > self.cfg_access["uplink_queue_bits"]:
                self._fail(pkt, "ACCESS_QUEUE_OVERFLOW")
                continue
            # MBB: new arrivals go to the newest active/acquiring link; an
            # unassociated endpoint queues and requests fair access instead of
            # being rejected just because every slot is currently taken.
            pkt.assigned_sat = link.sat if (link is not None and link.state == "active") else None
            ep.queue.append(pkt)
            ep.queued_bits += pkt.bits
            ep.area.add(pkt.bits, now)
            self._note_busy(ep.cell)
            if link is None:
                self._request_or_grant(ep, now)
            for sat_id in list(ep.links):
                self._poke(self.uplinks[sat_id].wake)
            # let link servers dequeue at the same instant before the next
            # emission; this keeps same-time ordering deterministic.
            yield self.env.timeout(0.0)

    def _endpoint_ticker(self, ep: TrafficEndpoint):
        while True:
            self._sweep_endpoint_queue(ep)
            self._access_tick_endpoint(ep)
            self._evaluate_handover(ep)
            yield self.env.timeout(self.time_step)

    def _pending_ticker(self, sat: int):
        while True:
            yield self.env.timeout(self.time_step)
            self._redecide_pending(sat)
            self._sweep_downlink_queues(sat)
            self._access_tick_sat(sat)

    def _sweep_downlink_queues(self, sat: int):
        now = self.env.now
        dl = self.downlinks[sat]
        for cell, q in list(dl.queues.items()):
            kept = deque()
            for pkt in q:
                if pkt.deadline is not None and now > pkt.deadline:
                    dl.queued_bits -= pkt.bits
                    dl.area.remove(pkt.bits, now)
                    self._fail(pkt, "DATA_DEADLINE_EXPIRED")
                else:
                    kept.append(pkt)
            dl.queues[cell] = kept

    # -------------------------------------------------------- fair access
    def _endpoint_demand(self, ep: TrafficEndpoint) -> bool:
        """Current demand: queued uplink packets, or some satellite holding
        packets destined to this endpoint (pending re-decision or an actual
        downlink queue)."""
        if ep.queue:
            return True
        return bool(self._downlink_demand_sats(ep.cell))

    def _downlink_demand_sats(self, cell: str) -> list[int]:
        out = []
        for s in range(self.num_sats):
            if any(p.dst == cell for p in self.pending[s]):
                out.append(s)
                continue
            if self.downlinks[s].queues.get(cell):
                out.append(s)
        return out

    def _candidates(self, ep: TrafficEndpoint, now: float):
        """Association candidates, demand-aware: satellites already holding
        this endpoint's downlink traffic first (by elevation), then every
        other currently visible satellite by elevation. Current geometry
        only — no future ephemeris."""
        dl = [s for s in self._downlink_demand_sats(ep.cell)
              if self.geometry.ground_visible(s, ep.lat, ep.lon, now)]
        dl.sort(key=lambda s: (-self.geometry.elevation_deg(s, ep.lat, ep.lon, now), s))
        seen = set(dl)
        rest = [(elev, s) for elev, s in self._visible_sats(ep) if s not in seen]
        return [(self.geometry.elevation_deg(s, ep.lat, ep.lon, now), s) for s in dl] + rest

    def _try_grant(self, ep: TrafficEndpoint, now: float, preposition: bool = False) -> bool:
        for _elev, s in self._candidates(ep, now):
            if len(self.slots[s]) < self.cfg_access["slots_per_satellite"]:
                req_t = self.access_wait[s].pop(ep.cell, None)
                self._associate(ep, s, now)
                if preposition:
                    self.access_stats["preposition_grants"] += 1
                else:
                    self.access_stats["grants"] += 1
                    if req_t is not None:
                        wt = now - req_t
                        self.access_stats["wait_time_s_total"] += wt
                        self.access_stats["wait_time_s_max"] = max(
                            self.access_stats["wait_time_s_max"], wt)
                return True
        return False

    def _request_or_grant(self, ep: TrafficEndpoint, now: float):
        """Explicit access request from current demand. Grants immediately
        when a candidate has a free slot; otherwise the endpoint joins the
        FIFO wait queue of its best candidate (deterministic, reproducible)."""
        if self._try_grant(ep, now):
            return
        cand = self._candidates(ep, now)
        if not cand:
            return  # nothing visible: retried at the next tick
        s = cand[0][1]
        if ep.cell not in self.access_wait[s]:
            self.access_wait[s][ep.cell] = now
            self.access_stats["requests"] += 1

    def _access_tick_endpoint(self, ep: TrafficEndpoint):
        now = self.env.now
        # idle = no uplink queue, no satellite-side demand, nothing in
        # service; idleness is measured from the last ACTIVITY (emission,
        # service start, requeue, arriving downlink demand), so work done
        # between ticks never counts as idle time
        idle = (not ep.queue
                and not self._downlink_demand_sats(ep.cell)
                and not any(self._in_service(ep, s) for s in ep.links))
        last_busy = self.access_last_busy.get(ep.cell, 0.0)
        # lease rotation and idle release apply only under contention; with
        # no waiters, keep-stable wins and nothing rotates gratuitously
        for sat, link in list(ep.links.items()):
            if link.state != "active" or not self.access_wait[sat]:
                continue
            if now - link.since >= self.cfg_access["slot_lease_s"]:
                # planned rotation: graceful retire — only already-assigned
                # (in-flight) packets drain; the hard retirement deadline is
                # the backstop and races any in-flight service
                link.state = "retiring"
                link.cause = "lease"
                link.retire_at = now + self.cfg_access["retirement_deadline_s"]
                self.env.process(self._fire_interrupt(link, link.retire_at))
                self.handover_events.append(
                    {"t": now, "endpoint": ep.cell, "type": "lease_retire",
                     "sat": sat})
                continue
            if idle and now - last_busy >= self.cfg_access["idle_release_s"]:
                self._release(ep, sat, now, "idle_release")
        # demand-driven requests, or free-slot pre-positioning when nothing
        # contends for any slot
        if ep.primary_link() is not None:
            return
        if any(l.state == "retiring" for l in ep.links.values()):
            return  # wait for the retiring link to clear first
        if self._endpoint_demand(ep):
            self._request_or_grant(ep, now)
        elif not any(self.access_wait[s] for s in range(self.num_sats)):
            self._try_grant(ep, now, preposition=True)

    def _access_tick_sat(self, sat: int):
        """Grant freed slots to waiting endpoints in FIFO request order."""
        now = self.env.now
        q = self.access_wait[sat]
        for cell in list(q):
            ep = self.endpoints[cell]
            if ep.primary_link() is not None or not self._endpoint_demand(ep):
                del q[cell]  # stale request
                continue
            if len(self.slots[sat]) >= self.cfg_access["slots_per_satellite"]:
                break
            if not self.geometry.ground_visible(sat, ep.lat, ep.lon, now):
                continue  # stays queued until geometry allows
            req_t = q.pop(cell)
            self._associate(ep, sat, now)
            self.access_stats["grants"] += 1
            wt = now - req_t
            self.access_stats["wait_time_s_total"] += wt
            self.access_stats["wait_time_s_max"] = max(
                self.access_stats["wait_time_s_max"], wt)

    def _control_advertiser(self, sat: int):
        interval = self.cfg_cp["advertise_interval_s"]
        while True:
            self._advertise(sat)
            yield self.env.timeout(interval)

    # --------------------------------------------------------------- control
    def _advertise(self, sat: int):
        self.ctrl_seq += 1
        isl_bits = {d: link.data_bits + link.ctrl_bits
                    for d, link in self.isls[sat].items()}
        isl_prop = {
            d: model.propagation_delay_s(
                self.geometry.isl_range_km(sat, link.peer, self.env.now))
            for d, link in self.isls[sat].items()
        }
        serve = sorted(c for c, ep in self.endpoints.items()
                       if ep.links.get(sat) is not None
                       and ep.links[sat].state == "active")
        snap = control.build_snapshot(
            sat, self.env.now, self.geometry,
            {c: (ep.lat, ep.lon) for c, ep in self.endpoints.items()},
            isl_bits, isl_prop, len(self.slots[sat]),
            self.cfg_access["slots_per_satellite"])
        snap["serve_cells"] = serve
        self.mech["control_snapshots"] += 1
        # the origin never accepts its own advertisement back, however long
        # it loops: its own (origin, seq) keys are pre-seeded as seen
        self.seen_ctrl[sat].add((sat, self.ctrl_seq))
        for d in self.control_children[sat][sat]:
            link = self.isls[sat][d]
            self.ctrl_iid += 1
            pkt = ControlPacket(
                self.ctrl_iid, sat, self.ctrl_seq, self.env.now,
                self.cfg_cp["ttl_s"], self.cfg_cp["vis_k"],
                self.cfg_cp["packet_bits"], snap)
            self.ctrl_ledger.register(pkt.iid, pkt.bits)
            self.mech["control_registered"] += 1
            if not link.room(pkt.bits):
                self.ctrl_ledger.record(pkt.iid, "QUEUE_OVERFLOW", pkt.bits)
                continue
            self.mech["control_entered_queue"] += 1
            link.put_ctrl(pkt)

    def _ctrl_arrive_after_prop(self, pkt: ControlPacket, from_sat: int, sat: int, prop: float):
        yield self.env.timeout(prop)
        now = self.env.now
        pkt.mark_received(now)  # the physical arrival instant, whatever the fate
        if not pkt.valid_at(now):
            self.ctrl_ledger.record(pkt.iid, "CONTROL_EXPIRED", pkt.bits,
                                    received_at=now)
            return
        if pkt.origin == sat:
            # explicit guard: an origin never consumes its own looped
            # advertisement, independent of topology/vis_k
            self.ctrl_ledger.record(pkt.iid, "DUPLICATE", pkt.bits,
                                    received_at=now)
            return
        key = (pkt.origin, pkt.seq)
        if key in self.seen_ctrl[sat]:
            self.ctrl_ledger.record(pkt.iid, "DUPLICATE", pkt.bits,
                                    received_at=now)
            return
        self.seen_ctrl[sat].add(key)
        self.ctrl_ledger.record(pkt.iid, "DELIVERED", pkt.bits, received_at=now)
        hops = self.cfg_cp["vis_k"] - pkt.remaining_hops + 1
        entry = control.CacheEntry(pkt.origin, pkt.payload, pkt.generated_at,
                                   pkt.received_at, pkt.ttl_s, hops=hops)
        self.caches[sat].put(entry)
        if pkt.remaining_hops > 1:
            for d in self.control_children[pkt.origin][sat]:
                link = self.isls[sat][d]
                self.ctrl_iid += 1
                fwd = ControlPacket(
                    self.ctrl_iid, pkt.origin, pkt.seq, pkt.generated_at,
                    pkt.ttl_s, pkt.remaining_hops - 1, pkt.bits, pkt.payload)
                self.ctrl_ledger.register(fwd.iid, fwd.bits)
                self.mech["control_registered"] += 1
                if not link.room(fwd.bits):
                    self.ctrl_ledger.record(fwd.iid, "QUEUE_OVERFLOW", fwd.bits)
                    continue
                self.mech["control_entered_queue"] += 1
                link.put_ctrl(fwd)

    # -------------------------------------------------------------- handover
    def _sweep_endpoint_queue(self, ep: TrafficEndpoint):
        now = self.env.now
        kept = deque()
        for pkt in ep.queue:
            if pkt.deadline is not None and now > pkt.deadline:
                ep.queued_bits -= pkt.bits
                ep.area.remove(pkt.bits, now)
                self._fail(pkt, "DATA_DEADLINE_EXPIRED")
            else:
                kept.append(pkt)
        ep.queue = kept

    def _visible_sats(self, ep: TrafficEndpoint):
        now = self.env.now
        out = []
        for s in range(self.num_sats):
            if self.geometry.ground_visible(s, ep.lat, ep.lon, now):
                out.append((self.geometry.elevation_deg(s, ep.lat, ep.lon, now), s))
        out.sort(key=lambda x: (-x[0], x[1]))
        return out

    def _associate(self, ep: TrafficEndpoint, sat: int, now: float):
        acq = self.cfg_access["acquisition_delay_s"]
        link = Link(sat, "acquiring", now, ready_at=now + acq,
                    interrupt=self.env.event())
        ep.links[sat] = link
        self.slots[sat].add(ep.cell)
        self.handover_events.append({"t": now, "endpoint": ep.cell,
                                     "type": "associate", "sat": sat})
        if acq <= 0:
            link.state = "active"
            self._poke(self.uplinks[sat].wake)
        else:
            self.env.process(self._activate_after_delay(ep, link))

    def _activate_after_delay(self, ep: TrafficEndpoint, link: Link):
        yield self.env.timeout(max(0.0, link.ready_at - self.env.now))
        if ep.links.get(link.sat) is link and link.state == "acquiring":
            link.state = "active"
            self._poke(self.uplinks[link.sat].wake)

    def _release(self, ep: TrafficEndpoint, sat: int, now: float, reason: str):
        link = ep.links.pop(sat, None)
        if link is None:
            return
        self.slots[sat].discard(ep.cell)
        self.access_stats["slot_hold_s_total"] += now - link.since
        rel = self.access_stats["releases"]
        rel[reason] = rel.get(reason, 0) + 1
        self.handover_events.append({"t": now, "endpoint": ep.cell,
                                     "type": "release", "sat": sat,
                                     "reason": reason})

    def _on_link_retired(self, ep: TrafficEndpoint, sat: int):
        """An in-flight service hit the hard retirement deadline: the link
        dies NOW (never used past retire_at). Any still-assigned queued
        packets are unassigned so a later association can serve them."""
        link = ep.links.get(sat)
        if link is None or link.state != "retiring":
            return
        if link.retire_at is None or self.env.now < link.retire_at:
            return
        for p in ep.queue:
            if p.assigned_sat == sat:
                p.assigned_sat = None
        self._release(ep, sat, self.env.now,
                      f"{link.cause or 'mbb'}_retire_deadline")

    def _in_service(self, ep: TrafficEndpoint, sat: int) -> bool:
        up = self.uplinks[sat].current
        if up is not None and up[0] is ep:
            return True
        dl = self.downlinks[sat].current
        return dl is not None and dl.dst == ep.cell

    def _evaluate_handover(self, ep: TrafficEndpoint):
        now = self.env.now
        # state transitions due
        for sat, link in list(ep.links.items()):
            if link.state == "retiring":
                in_service = self._in_service(ep, sat)
                drained = not any(p.assigned_sat == sat for p in ep.queue) and not in_service
                if drained:
                    self._release(ep, sat, now, f"{link.cause or 'mbb'}_drained")
                elif now >= link.retire_at and not in_service:
                    for p in ep.queue:
                        if p.assigned_sat == sat:
                            p.assigned_sat = None
                    self._release(ep, sat, now,
                                  f"{link.cause or 'mbb'}_retire_deadline")
        cand = self._visible_sats(ep)
        current = ep.primary_link()
        if current is None:
            return  # (re-)association is the fair access manager's job
        cur_sat = current.sat
        cur_vis = self.geometry.ground_visible(cur_sat, ep.lat, ep.lon, now)
        cur_elev = self.geometry.elevation_deg(cur_sat, ep.lat, ep.lon, now) if cur_vis else -90.0
        best_elev, best_sat = cand[0] if cand else (-90.0, None)
        if cur_vis:
            if not cand:
                return
            if best_sat == cur_sat:
                return
            if best_elev - cur_elev < self.cfg_access["hysteresis_deg"]:
                return  # keep-stable via elevation hysteresis (degrees)
            if now - current.since < self.cfg_access["min_dwell_s"]:
                return  # minimum dwell time
        # switch (or re-establish after geometry loss)
        target = None
        for elev, s in cand:
            if s == cur_sat:
                continue
            if len(self.slots[s]) < self.cfg_access["slots_per_satellite"]:
                target = s
                break
        if target is None:
            if not cur_vis:
                self._release(ep, cur_sat, now, "geometry_lost_no_candidate")
            return
        mbb = (self.cfg_access["association"] == "mbb"
               and self.cfg_access["dual_connect"]
               and cur_vis
               and len([l for l in ep.links.values() if l.state == "retiring"])
               < self.cfg_access["retiring_link_limit"])
        if mbb:
            # old link keeps draining already-assigned packets, but the hard
            # retirement deadline races any in-flight service on it
            old = ep.links[cur_sat]
            old.state = "retiring"
            old.cause = "mbb"
            old.retire_at = now + self.cfg_access["retirement_deadline_s"]
            self.env.process(self._fire_interrupt(old, old.retire_at))
            for p in ep.queue:
                if p.assigned_sat is None:
                    p.assigned_sat = cur_sat
            self._associate(ep, target, now)
            self.mech["mbb_events"] += 1
            self.handover_events.append({"t": now, "endpoint": ep.cell,
                                         "type": "mbb", "from": cur_sat,
                                         "to": target})
        else:
            # BBM: never preempts a packet currently in service on the old link
            if self._in_service(ep, cur_sat):
                return  # defer the break until the in-flight packet completes
            self._release(ep, cur_sat, now, "bbm_switch")
            self._associate(ep, target, now)
            self.handover_events.append({"t": now, "endpoint": ep.cell,
                                         "type": "bbm", "from": cur_sat,
                                         "to": target})

    # --------------------------------------------------------------- routing
    def _serving_sats(self, cell: str) -> list[int]:
        """Satellites whose association with the endpoint is active right now
        (direct kernel truth; used ONLY by the labeled oracle)."""
        ep = self.endpoints[cell]
        return sorted(s for s, l in ep.links.items() if l.state == "active")

    def _learning_observation(self, sat: int, dst_cell: str) -> np.ndarray:
        queues = {d: lnk.data_bits + lnk.ctrl_bits
                  for d, lnk in self.isls[sat].items()}
        visible = sum(
            1 for ep in self.endpoints.values()
            if self.geometry.ground_visible(sat, ep.lat, ep.lon, self.env.now)
        )
        own = _learning.own_state(
            len(self.slots[sat]), self.cfg_access["slots_per_satellite"],
            queues, self.cfg_links["isl_queue_bits"], visible,
            len(self.endpoints),
        )
        obs_hops = self.cfg_learning.get("obs_hops")
        ep = self.endpoints.get(dst_cell)
        dst_feats = None
        if ep is not None:
            sat_lat, sat_lon, _ = self.geometry.subpoint(sat, self.env.now)
            dst_feats = _learning.destination_features(
                sat_lat, sat_lon, ep.lat, ep.lon)
        return _learning.build_observation(
            self.cfg_rt["contract"], sat, self.caches[sat], self.env.now,
            self.topo, own, self.cfg_links["isl_queue_bits"],
            obs_hops=obs_hops, dst_feats=dst_feats,
        )

    def _finish_learning_transition(self, pkt: DataPacket, next_state,
                                    next_mask: dict, done: bool,
                                    terminal_reward: float | None = None) -> None:
        if self.learner is None or pkt.learning_state is None:
            return
        if terminal_reward is None and pkt.learning_reward is None:
            # the forward reward is settled when the packet's ISL service
            # actually starts; reaching here without it means the reward was
            # never realized — fail loud instead of storing a silent None
            raise KernelError(
                "learning transition closed with unrealized reward "
                f"(pid={pkt.pid})")
        reward = (pkt.learning_reward if terminal_reward is None
                  else float(terminal_reward))
        self.learner.remember(
            pkt.learning_state, pkt.learning_action, reward,
            next_state, next_mask, done,
        )
        pkt.learning_state = None
        pkt.learning_action = None
        pkt.learning_reward = None

    def _learning_action(self, pkt: DataPacket, sat: int, mask: dict) -> str:
        state = self._learning_observation(sat, pkt.dst)
        self._finish_learning_transition(pkt, state, mask, False)
        action = self.learner.choose(state, mask, self.env.now)
        if action == "deliver":
            # terminal delivery reward: legacy ArriveReward (v1 has no
            # distance component; see ANALYSIS/REWARD-DIFF-20260816.md)
            reward = float(self.cfg_learning["arrive_reward"])
        else:
            # forward reward is the M1 queue reward over the packet's
            # REALIZED queue wait, settled when its ISL service starts
            # (_transmit); unknown at decision time by construction
            reward = None
        pkt.learning_state = state
        pkt.learning_action = action
        pkt.learning_reward = reward
        return action

    def _record_decision(self, pkt: DataPacket, sat: int, kind: str,
                         candidates: list, chosen: str) -> None:
        """Append one per-hop decision snapshot to the optional decision sink.

        Output only: never influences routing, learning, timing, or fates.
        ``candidates`` is the legal action set at decision time; for learning
        runs ``obs`` summarizes the observation actually used (dim, short
        content hash, L2 norm) so decision streams are diffable without
        storing full vectors.
        """
        if self.decision_sink is None:
            return
        obs = pkt.learning_state
        obs_summary = None
        if obs is not None:
            arr = np.ascontiguousarray(np.asarray(obs, dtype=np.float64))
            obs_summary = {
                "contract": self.cfg_rt["contract"],
                "dim": int(arr.size),
                "sha256_16": hashlib.sha256(arr.tobytes()).hexdigest()[:16],
                "l2_norm": float(np.linalg.norm(arr)),
            }
        self.decision_sink.append({
            "t": float(self.env.now),
            "pid": pkt.pid,
            "src": pkt.src,
            "dst": pkt.dst,
            "sat": sat,
            "kind": kind,
            "policy": (self.cfg_rt["policy"] if self.learner is None
                       else f"ddqn:{self.cfg_rt['contract']}"),
            "candidates": list(candidates),
            "chosen": chosen,
            "own_queue_bits": {d: int(lnk.data_bits + lnk.ctrl_bits)
                               for d, lnk in self.isls[sat].items()},
            "obs": obs_summary,
        })

    def _decide(self, pkt: DataPacket, sat: int) -> None:
        now = self.env.now
        if pkt.deadline is not None and now > pkt.deadline:
            self._fail(pkt, "DATA_DEADLINE_EXPIRED")
            return
        if len(pkt.path) > self.cfg_rt["max_hops"]:
            self._fail(pkt, "NO_ROUTE")
            return
        ep = self.endpoints[pkt.dst]
        link = ep.links.get(sat)
        if (link is not None and link.state == "active"
                and self.geometry.gsl_available(sat, ep.lat, ep.lon, now)):
            dl = self.downlinks[sat]
            if dl.room(pkt.bits):
                if self.learner is not None:
                    action = self._learning_action(
                        pkt, sat,
                        {a: a == "deliver" for a in _learning.ACTIONS},
                    )
                    if action != "deliver":
                        raise KernelError("DDQN selected a non-deliver action from deliver-only mask")
                self._record_decision(pkt, sat, "deliver", ["deliver"],
                                      "deliver")
                dl.put(pkt)
            else:
                self._fail(pkt, "ACCESS_QUEUE_OVERFLOW")
            return
        own_q = {d: lnk.data_bits + lnk.ctrl_bits for d, lnk in self.isls[sat].items()}
        cands, status = routing.choose_next_hop(
            self.cfg_rt["policy"], sat, pkt.dst, now, self.geometry, self.topo,
            self.caches[sat], own_q, self.isl_rate_bps, model.propagation_delay_s,
            oracle_targets=[s for s in self._serving_sats(pkt.dst) if s != sat],
            best_only=self.learner is not None)
        if status == "unreachable":
            self._fail(pkt, "NO_ROUTE")
            return
        if status == "no_info":
            if not self.cfg_cp["enabled"] and self.cfg_rt["policy"] != "oracle":
                self._fail(pkt, "NO_ROUTE")
            else:
                self.pending[sat].append(pkt)  # wait for re-decision
            return
        # loop avoidance: never forward back onto a satellite already visited
        cands = [d for d in cands if self.topo[sat][d] not in pkt.path]
        unavailable = False
        legal = []
        for d in cands:
            link = self.isls[sat][d]
            if self.cfg_links["geometry_loss"] and not self.geometry.isl_available(
                    sat, link.peer, now):
                unavailable = True
                continue
            if link.room(pkt.bits):
                legal.append(d)
        if legal:
            if self.learner is not None:
                mask = {a: a in legal for a in _learning.ACTIONS}
                action = self._learning_action(pkt, sat, mask)
            else:
                action = legal[0]
            self._record_decision(pkt, sat, "forward", legal, action)
            self.isls[sat][action].put_data(pkt)
            return
        if unavailable:
            self.pending[sat].append(pkt)  # temporarily unavailable: wait
            return
        if cands:
            self._fail(pkt, "ISL_QUEUE_OVERFLOW")
        else:
            self._fail(pkt, "NO_ROUTE")  # every candidate loops

    def _redecide_pending(self, sat: int):
        if not self.pending[sat]:
            return
        waiting = self.pending[sat]
        self.pending[sat] = []
        for pkt in waiting:
            self._decide(pkt, sat)

    def _ingress_after_prop(self, pkt: DataPacket, sat: int, prop: float):
        yield self.env.timeout(prop)
        if pkt.deadline is not None and self.env.now > pkt.deadline:
            self._fail(pkt, "DATA_DEADLINE_EXPIRED")
            return
        pkt.path.append(sat)
        self._note_busy(pkt.dst)  # new downlink demand may have appeared
        self._decide(pkt, sat)

    def _isl_arrive_after_prop(self, pkt: DataPacket, sat: int, prop: float):
        yield self.env.timeout(prop)
        if pkt.deadline is not None and self.env.now > pkt.deadline:
            self._fail(pkt, "DATA_DEADLINE_EXPIRED")
            return
        pkt.path.append(sat)
        self._note_busy(pkt.dst)  # new downlink demand may have appeared
        self._decide(pkt, sat)

    def _deliver_after_prop(self, pkt: DataPacket, sat: int, prop: float):
        yield self.env.timeout(prop)
        now = self.env.now
        if pkt.deadline is not None and now > pkt.deadline:
            self._fail(pkt, "DATA_DEADLINE_EXPIRED")
            return
        self._finish_learning_transition(
            pkt, np.zeros(_learning.CONTRACT_DIMS[self.cfg_rt["contract"]]),
            {a: False for a in _learning.ACTIONS}, True,
        )
        self.ledger.record(pkt.pid, "DELIVERED", pkt.bits)
        self.deliveries[pkt.pid] = {"delivered_at": now, "path": list(pkt.path)}
        self._log("delivered", pid=pkt.pid, sat=sat)

    # ----------------------------------------------------------------- fates
    def _fail(self, pkt, fate: str):
        if isinstance(pkt, ControlPacket):
            self.ctrl_ledger.record(pkt.iid, fate, pkt.bits)
        else:
            self._finish_learning_transition(
                pkt,
                np.zeros(_learning.CONTRACT_DIMS[self.cfg_rt["contract"]]),
                {a: False for a in _learning.ACTIONS}, True,
                terminal_reward=0.0,
            )
            self.ledger.record(pkt.pid, fate, pkt.bits)
            self._log("fate", pid=pkt.pid, fate=fate)

    # ------------------------------------------------------------------- run
    def run(self) -> dict:
        interrupted = False
        error = None
        events = 0
        try:
            while True:
                try:
                    t_next = self.env.peek()
                except Exception:
                    break
                if t_next > self.horizon or t_next == math.inf:
                    break
                self.env.step()
                events += 1
                if events > self.cfg_ex["max_events"]:
                    raise CapExceeded("max_events exceeded")
        except (CapExceeded, fates.FateError) as exc:
            interrupted = True
            error = f"{type(exc).__name__}: {exc}"
        # packets still in service at stop occupied their link up to the end
        for s in range(self.num_sats):
            for srv in (self.uplinks[s], self.downlinks[s]):
                if srv._svc is not None:
                    t0, key = srv._svc
                    self.occupied[key] += self.env.now - t0
            for lnk in self.isls[s].values():
                if lnk._svc is not None:
                    t0, key = lnk._svc
                    self.occupied[key] += self.env.now - t0
        stop_time = self.env.now  # == horizon on a natural end (closer)
        # settle all queue-area integrals at the exact stop time
        for ep in self.endpoints.values():
            ep.area.close(stop_time)
        for s in range(self.num_sats):
            self.downlinks[s].area.close(stop_time)
            for lnk in self.isls[s].values():
                lnk.data_area.close(stop_time)
                lnk.ctrl_area.close(stop_time)
        queue_area = {
            "uplink": sum(ep.area.area for ep in self.endpoints.values()),
            "downlink": sum(self.downlinks[s].area.area for s in range(self.num_sats)),
            "isl_data": sum(lnk.data_area.area for s in range(self.num_sats)
                            for lnk in self.isls[s].values()),
            "isl_ctrl": sum(lnk.ctrl_area.area for s in range(self.num_sats)
                            for lnk in self.isls[s].values()),
        }
        self.access_stats["waiting_at_stop"] = sum(
            len(q) for q in self.access_wait)
        self.ledger.close_at_stop()
        self.ctrl_ledger.close_at_stop()
        if interrupted:
            totals = self.ledger.totals()
            ctrl_totals = self.ctrl_ledger.totals()
        else:
            totals = self.ledger.check_conservation()
            ctrl_totals = self.ctrl_ledger.check_conservation()
        requested = {
            "policy": self.cfg_rt["policy"],
            "association": self.cfg_access["association"],
            "ge_enabled": self.ge_enabled,
            "control_enabled": bool(self.cfg_cp["enabled"]),
            "monitor": self.monitor,
            "learning_algorithm": (
                "ddqn" if self.learner is not None else "none"),
            "learning_mode": (
                self.learner.mode if self.learner is not None else "train"),
        }
        ctrl_fc = self.ctrl_ledger.fate_counts()
        control_counters = {
            "snapshots_created": self.mech["control_snapshots"],
            "registered": self.mech["control_registered"],
            "entered_queue": self.mech["control_entered_queue"],
            "transmission_started": self.mech["control_tx_started"],
            "transmission_completed": self.mech["control_tx_completed"],
            "arrived": ctrl_fc["DELIVERED"],
            "expired": ctrl_fc["CONTROL_EXPIRED"],
            "lost": ctrl_fc["RANDOM_OUTAGE_IN_FLIGHT"],
            "geometry_lost": ctrl_fc["GEOMETRY_LOSS_IN_FLIGHT"],
            "overflow": ctrl_fc["QUEUE_OVERFLOW"],
            "duplicate": ctrl_fc["DUPLICATE"],
            "in_system": ctrl_fc["IN_SYSTEM_AT_STOP"],
        }
        # a requested mechanism is EFFECTIVE only if it really entered the
        # send path: control requires a real ControlPacket admitted to a link
        # queue (a bare snapshot proves nothing); GE requires the channel to
        # have been consulted on a service path; MBB requires a real event.
        effective = {
            "control_plane": self.mech["control_entered_queue"] > 0,
            "ge": self.ge_enabled and (
                self.mech["ge_gsl_queries"] + self.mech["ge_isl_queries"] > 0),
            "mbb": self.mech["mbb_events"] > 0,
            "learning": False,
            "ge_gsl_queries": self.mech["ge_gsl_queries"],
            "ge_isl_queries": self.mech["ge_isl_queries"],
            "ge_waits": self.mech["ge_waits"],
            "ge_failures": self.mech["ge_failures"],
            "mbb_events": self.mech["mbb_events"],
        }
        learning_result = None
        if self.learner is not None:
            learning_result = self.learner.diagnostics()
            if self.learning_out_dir is not None:
                learning_result = self.learner.save_and_verify(
                    self.learning_out_dir)
            self.mech["learning_decisions"] = self.learner.decisions
            self.mech["learning_transitions"] = self.learner.transitions
            self.mech["learning_train_steps"] = self.learner.train_steps
            effective["learning"] = (
                self.learner.train_steps > 0 if self.learner.mode == "train"
                else self.learner.decisions > 0
            )
        # A local kernel cannot self-authorize a scientific result. Mechanism
        # effectiveness is reported above; research eligibility requires an
        # externally anchored review/authorization/deployment receipt and is
        # therefore always false for this ungoverned runtime entry point.
        research_eligible = False
        result = {
            "natural_end": not interrupted,
            "interrupted": interrupted,
            "error": error,
            "events_processed": events,
            "horizon_s": self.horizon,
            "stop_time_s": stop_time,
            "fates": dict(self.ledger._fates),
            "fate_counts": self.ledger.fate_counts(),
            "totals": totals,
            "deliveries": self.deliveries,
            "occupied": dict(self.occupied),
            "queue_area_bits_s": queue_area,
            "access": dict(self.access_stats),
            "service_log": self.service_log,
            "handover": {"events": self.handover_events},
            "control": {
                "counters": control_counters,
                # deprecated mirror of counters["snapshots_created"], kept so
                # frozen external probes still execute
                "generated": control_counters["snapshots_created"],
                "bits": dict(self.ctrl_ledger.bits),
                "totals": ctrl_totals,
                "fate_counts": ctrl_fc,
                "instances": self.ctrl_ledger.instances(),
                "cache_expired_open": sum(
                    c.count_expired(self.env.now) for c in self.caches),
            },
            "caches": {s: {o: {"generated_at": e.generated_at,
                               "received_at": e.received_at,
                               "visible_cells": list(e.payload.get("visible_cells", ())),
                               "serve_cells": list(e.payload.get("serve_cells", ())),
                               "aoi": e.aoi(self.env.now),
                               "valid": e.valid_at(self.env.now)}
                           for o, e in c._entries.items()}
                       for s, c in enumerate(self.caches)},
            "mechanisms": {"requested": requested, "effective": effective},
            "learning": learning_result,
            "mechanism_counters": dict(self.mech),
            "research_eligible": research_eligible,
            "monitor_log": list(self.monitor_log),
            "routing_label": routing.ORACLE_LABEL if self.cfg_rt["policy"] == "oracle" else None,
        }
        return result


def run_simulation(resolved: dict, rows: list[dict], geometry=None,
                   learning_out_dir=None, decision_sink=None) -> dict:
    kern = Kernel(resolved, rows, geometry=geometry,
                  learning_out_dir=learning_out_dir,
                  decision_sink=decision_sink)
    return kern.run()
