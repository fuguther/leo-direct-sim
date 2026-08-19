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

from . import control, fates, grid as gridmod, learning as _learning, model, q0
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
                 "learning_reward", "isl_enqueued_at", "holding_until")

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
        self.holding_until = None


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


class SatelliteHoldingQueue:
    """Finite FIFO for packets held by a satellite between decisions.

    Unlike the legacy ``pending`` list, admission is capacity checked and
    every mutation updates the shared queue-area integral.  The small list
    compatibility surface is intentional while callers migrate: iteration,
    indexing, ``append`` and equality remain available to old diagnostics.
    """

    __slots__ = ("capacity_bits", "area", "_items", "queued_bits", "_now")

    def __init__(self, capacity_bits: int, area: QueueArea, now_fn=None):
        if capacity_bits < 0:
            raise ValueError("holding queue capacity must be >= 0")
        self.capacity_bits = capacity_bits
        self.area = area
        self._items: list[DataPacket] = []
        self.queued_bits = 0
        self._now = now_fn or (lambda: 0.0)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def __eq__(self, other):
        if isinstance(other, SatelliteHoldingQueue):
            other = other._items
        return self._items == other

    def room(self, bits: int) -> bool:
        return self.queued_bits + bits <= self.capacity_bits

    def put(self, pkt: DataPacket, now: float) -> bool:
        if not self.room(pkt.bits):
            return False
        self._items.append(pkt)
        self.queued_bits += pkt.bits
        self.area.add(pkt.bits, now)
        return True

    def append(self, pkt: DataPacket) -> None:
        """Compatibility append at the kernel's current time.

        New kernel paths use ``put`` so an overflow can receive an explicit
        fate.  Direct legacy-style callers get a loud error instead of an
        unaccounted packet.
        """
        if not self.put(pkt, self._now()):
            raise CapExceeded("holding queue capacity exceeded")

    def remove(self, pkt: DataPacket, now: float) -> None:
        self._items.remove(pkt)
        self.queued_bits -= pkt.bits
        self.area.remove(pkt.bits, now)

    def pop(self, index: int = 0, now: float = 0.0):
        if not self._items:
            return None
        pkt = self._items.pop(index)
        self.queued_bits -= pkt.bits
        self.area.remove(pkt.bits, now)
        return pkt

    def clear(self, now: float) -> list[DataPacket]:
        items = list(self._items)
        self._items.clear()
        if self.queued_bits:
            self.area.remove(self.queued_bits, now)
        self.queued_bits = 0
        return items

    def take_ready(self, now: float) -> list[DataPacket]:
        """Remove packets whose explicit WAIT interval has elapsed."""
        ready = [p for p in self._items
                 if p.holding_until is None or now >= p.holding_until]
        if not ready:
            return []
        for pkt in ready:
            self.remove(pkt, now)
            pkt.holding_until = None
        return ready

    def sweep_expired(self, now: float) -> list[DataPacket]:
        """Remove packets whose data deadline has passed while being held."""
        expired = [p for p in self._items
                   if p.deadline is not None and now > p.deadline]
        for pkt in expired:
            self.remove(pkt, now)
        return expired


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
        self._svc_phase = None  # None | waiting_for_link | transmitting
        self._tx_started_at = None
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
            self._svc_phase = "waiting_for_link"
            self._tx_started_at = None
            outcome = yield k.env.process(
                k._transmit(dur, pkt, ("gsl", self.sat, ep, ep.links.get(self.sat)),
                            "gsl_uplink_s", owner=self))
            k.service_log["uplink_bits"].append((k.env.now, cell, pkt.bits))
            self._svc = None
            self._svc_phase = None
            self._tx_started_at = None
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
            k._in_flight[pkt.pid] = {
                "kind": "ingress", "sat": self.sat,
                "arrival_at": k.env.now + prop, "pkt": pkt}
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
        self._svc_phase = None  # None | waiting_for_link | transmitting
        self._tx_started_at = None
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
                        k._hold_packet(self.sat, pkt)
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
            self._svc_phase = "waiting_for_link"
            self._tx_started_at = None
            outcome = yield k.env.process(
                k._transmit(dur, pkt, ("gsl", self.sat, ep, ep.links.get(self.sat)),
                            "gsl_downlink_s", owner=self))
            self._svc = None
            self._svc_phase = None
            self._tx_started_at = None
            self.current = None
            if outcome == "retired":
                # partial downlink never reached the endpoint: re-decide at
                # this satellite (the destination holds a new association).
                k._hold_packet(self.sat, pkt)
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
            k._in_flight[pkt.pid] = {
                "kind": "deliver", "sat": self.sat,
                "arrival_at": k.env.now + prop, "pkt": pkt}
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
        self.current: DataPacket | ControlPacket | None = None
        self._svc = None
        self._svc_phase = None  # None | waiting_for_link | transmitting
        self._tx_started_at = None
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
            self.current = pkt
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
            self._svc_phase = "waiting_for_link"
            self._tx_started_at = None
            outcome = yield k.env.process(
                k._transmit(dur, pkt, ("isl", self.sat, self.peer, self.ge),
                            occ, owner=self))
            self._svc = None
            self._svc_phase = None
            self._tx_started_at = None
            self.current = None
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
                k._in_flight[pkt.pid] = {
                    "kind": "isl", "sat": self.peer,
                    "arrival_at": k.env.now + prop, "pkt": pkt}
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
        algorithm = cfg["learning"]["algorithm"]
        if algorithm == "ddqn":
            self.learner = _learning.TensorflowDDQN(
                self.cfg_rt["contract"], cfg["learning"],
                cfg["learning"]["seed"]
                if cfg["learning"]["seed"] is not None
                else self.cfg_sc["seed"])
        elif algorithm == "qlearning":
            self.learner = _learning.TabularQLearning(
                self.cfg_rt["contract"], cfg["learning"],
                cfg["learning"]["seed"]
                if cfg["learning"]["seed"] is not None
                else self.cfg_sc["seed"])
        else:
            self.learner = None

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
        # exact-argument memoization wrapper: transparent and bit-equivalent
        # (cached values are the first-computed results for identical pure
        # queries), bounded LRU, filled only on demand — never reads future
        # times itself.
        self.geometry = model.MemoizedGeometry(geometry)
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
            self.geometry, self.num_sats, self.cfg_links["isl_dirs"])
        # static routing structures: topo never changes, so build the reverse
        # adjacency and its sorted neighbour lists once instead of rebuilding
        # them on every decision (behaviour-identical, same iteration order)
        self._routing_reverse_adj = routing._reverse_adj(self.topo)
        self._routing_sorted_rev_adj = {
            s: sorted(self._routing_reverse_adj.get(s, ()))
            for s in self._routing_reverse_adj}
        self.control_children = [
            routing.control_broadcast_children(
                self.topo, origin, self.cfg_cp["vis_k"])
            for origin in range(self.num_sats)
        ] if self.cfg_cp["enabled"] and self.cfg_cp["vis_k"] > 0 else []

        # per-satellite state
        self.slots: list[set[str]] = [set() for _ in range(self.num_sats)]
        self.caches: list[control.LocalCache] = [control.LocalCache() for _ in range(self.num_sats)]
        self.holding_areas = [QueueArea() for _ in range(self.num_sats)]
        self.pending: list[SatelliteHoldingQueue] = [
            SatelliteHoldingQueue(
                self.cfg_access["holding_queue_bits"], self.holding_areas[s],
                now_fn=lambda self=self: self.env.now)
            for s in range(self.num_sats)]
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
        self.q0_plan_audit: list[dict] = []
        self.monitor = bool(self.cfg_ex["monitor"])
        self.data_packet_count = 0
        # Q0 readiness: monotonic state version (bumped once per event step)
        # and the set of data packets currently propagating between nodes
        # (scheduled timeout arrivals), so a global snapshot can include the
        # in-flight component of the network state.
        self._state_version = 0
        self._in_flight: dict[int, dict] = {}
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
            "learning_discarded_at_stop": 0,
            "holding_queue_overflows": 0,
        }
        # packets holding an open (not yet closed) learning transition; the
        # horizon close must account for every one of them, never silently
        self._learning_open: set[DataPacket] = set()
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
        # tabular Q-learning is pure numpy; only the DDQN arm needs TF
        if requested and cfg["learning"]["algorithm"] == "ddqn":
            _learning.require_tensorflow()

    def _poke(self, event):
        if not event.triggered:
            event.succeed()

    def _note_busy(self, cell: str):
        """Last-activity stamp for fair-access idle measurement."""
        self.access_last_busy[cell] = self.env.now

    def _hold_packet(self, sat: int, pkt: DataPacket) -> bool:
        """Admit a packet to finite satellite holding, or assign its fate."""
        if self.pending[sat].put(pkt, self.env.now):
            self._note_busy(pkt.dst)
            return True
        self.mech["holding_queue_overflows"] += 1
        self._fail(pkt, "HOLDING_QUEUE_OVERFLOW")
        return False

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

    # ------------------------------------------------------- Q0 snapshot
    def snapshot_global(self) -> dict:
        """Read-only global state snapshot for a centralized Q0 planner.

        Bound to the current simulation time and the monotonic
        ``_state_version`` (bumped once per event step), so a plan computed
        from this snapshot is provably stale after any intervening event.
        All nested containers are freshly constructed per call: the caller
        may not reach into kernel objects through this view.  The snapshot is
        CURRENT-state only: Q0-A (global current information) may use it;
        future information (Q0-B) needs a separate, explicitly labelled
        future view.  Physical constraints remain enforced by the kernel at
        execution time; this interface never writes.

        Read-only holds at the observable-state level: ge.is_down() lazily
        advances each GE's internal trajectory, but GilbertElliott
        trajectories are query-pattern independent, so the snapshot never
        mutates the world state it reports (R6-A3).
        """
        now = self.env.now

        def _drr_state(srv) -> dict:
            return {"deficit": dict(srv.deficit),
                    "rr_cursor": srv.rr_cursor}

        def _svc_state(srv) -> dict | None:
            if srv._svc is None:
                return None
            t0, occ = srv._svc
            # remaining service time is derivable from the in-service packet
            # and its link rate (uplink/downlink only; ISL rate depends on
            # data-vs-control, resolved by the caller)
            return {
                "started_at": t0,
                "occ_key": occ,
                "phase": getattr(srv, "_svc_phase", None),
                "tx_started_at": getattr(srv, "_tx_started_at", None),
            }

        def _packet_info(pkt) -> dict:
            return {
                "src": pkt.src,
                "bits": pkt.bits,
                "deadline": pkt.deadline,
                "dst": pkt.dst,
                "emitted_at": pkt.emitted_at,
                "path": list(pkt.path),
                "assigned_sat": getattr(pkt, "assigned_sat", None),
                "holding_until": getattr(pkt, "holding_until", None),
            }

        def _remaining_service(bits, rate_bps, srv) -> float | None:
            """Phase-aware residual service time.

            waiting_for_link: no bit has been transmitted yet; report the
            full duration (what the server will need once the link is up).
            transmitting: duration - elapsed since the real transmission
            started (never negative by construction).
            """
            if srv._svc is None:
                return None
            if srv._svc_phase == "waiting_for_link":
                return bits / rate_bps
            if srv._svc_phase == "transmitting" \
                    and srv._tx_started_at is not None:
                return (bits / rate_bps) - (now - srv._tx_started_at)
            return None
        isl_links = {}
        for s in range(self.num_sats):
            isl_links[s] = {}
            for d, lnk in self.isls[s].items():
                in_service = None
                if lnk.current is not None:
                    if isinstance(lnk.current, ControlPacket):
                        in_service = {"iid": lnk.current.iid}
                    else:
                        in_service = {"pid": lnk.current.pid}
                remaining = None
                if lnk._svc is not None and lnk.current is not None:
                    remaining = _remaining_service(
                        lnk.current.bits, self.isl_rate_bps, lnk)
                isl_links[s][d] = {
                    "peer": lnk.peer,
                    "data_bits": lnk.data_bits,
                    "ctrl_bits": lnk.ctrl_bits,
                    "data_q": [{"pid": p.pid, **_packet_info(p)}
                               for p in lnk.data_q],
                    "ctrl_q": [c.iid for c in lnk.ctrl_q],
                    "in_service": in_service,
                    "svc": _svc_state(lnk),
                    "remaining_service_s": remaining,
                    "ge_bad": bool(lnk.ge.is_down(now)) if self.ge_enabled
                    else False,
                    "ge_next_flip": (float(lnk.ge._next_flip)
                                     if self.ge_enabled else math.inf),
                }

        endpoints = {}
        for cell, ep in self.endpoints.items():
            endpoints[cell] = {
                "queue": [{"pid": p.pid, **_packet_info(p)}
                          for p in ep.queue],
                "queued_bits": ep.queued_bits,
                "links": {
                    sat: {"state": lk.state, "since": lk.since,
                          "ready_at": lk.ready_at,
                          "retire_at": lk.retire_at, "cause": lk.cause}
                    for sat, lk in ep.links.items()
                },
            }

        downlinks = {}
        for s in range(self.num_sats):
            dl = self.downlinks[s]
            downlinks[s] = {
                "queues": {cell: [{"pid": p.pid, **_packet_info(p)}
                                  for p in q]
                           for cell, q in dl.queues.items()},
                "queued_bits": dl.queued_bits,
                "in_service": ({"pid": dl.current.pid}
                               if dl.current is not None else None),
                "svc": _svc_state(dl),
                "remaining_service_s": (
                    _remaining_service(dl.current.bits, self.dl_rate_bps, dl)
                    if dl.current is not None else None),
                "drr": _drr_state(dl),
            }

        uplinks = {}
        for s in range(self.num_sats):
            up = self.uplinks[s]
            uplinks[s] = {
                "in_service": ({"pid": up.current[1].pid}
                               if up.current is not None else None),
                "svc": _svc_state(up),
                "remaining_service_s": (
                    _remaining_service(up.current[1].bits, self.ul_rate_bps,
                                       up)
                    if up.current is not None else None),
                "drr": _drr_state(up),
            }

        gsl_ge = {}
        # Universe = every materialized GSL GE pair plus every current
        # endpoint-satellite association.  A pair must never be implied by
        # key absence: un-materialized pairs are explicit with bad=None.
        gsl_pairs = set(self.gsl_ge)
        for cell, ep in self.endpoints.items():
            for sat in ep.links:
                gsl_pairs.add((sat, cell))
        for sat, cell in sorted(gsl_pairs, key=lambda p: (p[0], p[1])):
            ge = self.gsl_ge.get((sat, cell))
            if ge is None:
                gsl_ge[f"{sat}:{cell}"] = {
                    "materialized": False, "bad": None, "next_flip": None,
                }
            else:
                gsl_ge[f"{sat}:{cell}"] = {
                    "materialized": True,
                    "bad": bool(ge.is_down(now)),
                    "next_flip": float(ge._next_flip),
                }

        return {
            "now": now,
            "state_version": self._state_version,
            "topology": {s: dict(nb) for s, nb in self.topo.items()},
            "slots": {s: sorted(v) for s, v in enumerate(self.slots)},
            "access_wait": {
                s: {cell: req_t for cell, req_t in self.access_wait[s].items()}
                for s in range(self.num_sats)},
            "access_last_busy": dict(self.access_last_busy),
            "endpoints": endpoints,
            "pending": {s: [{"pid": p.pid, **_packet_info(p)}
                            for p in self.pending[s]]
                        for s in range(self.num_sats)},
            "holding": {s: {"queued_bits": self.pending[s].queued_bits,
                             "capacity_bits": self.pending[s].capacity_bits}
                         for s in range(self.num_sats)},
            "uplinks": uplinks,
            "downlinks": downlinks,
            "isl_links": isl_links,
            "gsl_ge": gsl_ge,
            "in_flight": {
                pid: {"pid": pid, "kind": v["kind"], "sat": v["sat"],
                      "arrival_at": v["arrival_at"],
                      **_packet_info(v["pkt"])}
                for pid, v in self._in_flight.items()},
            "caches": {
                s: {origin: {"serve_cells": sorted(entry.payload.get(
                        "serve_cells", ())),
                             "generated_at": entry.generated_at}
                    for origin, entry in self.caches[s].valid_entries(now).items()}
                for s in range(self.num_sats)
            },
        }

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

    def _data_packet_locations(self) -> dict[int, tuple[str, int | None]]:
        """Read-only index of live data packets for Q0 plan validation."""
        found: dict[int, tuple[str, int | None]] = {}
        for sat, packets in enumerate(self.pending):
            for pkt in packets:
                found[pkt.pid] = ("pending", sat)
        for ep in self.endpoints.values():
            for pkt in ep.queue:
                found[pkt.pid] = ("uplink", pkt.assigned_sat)
        for srv in self.uplinks:
            if srv.current is not None:
                found[srv.current[1].pid] = ("in_service", srv.sat)
        for sat, srv in enumerate(self.downlinks):
            for packets in srv.queues.values():
                for pkt in packets:
                    found[pkt.pid] = ("downlink", sat)
            if isinstance(srv.current, DataPacket):
                found[srv.current.pid] = ("in_service", sat)
        for sat, links in enumerate(self.isls):
            for link in links.values():
                for pkt in link.data_q:
                    found[pkt.pid] = ("isl", sat)
                if isinstance(link.current, DataPacket):
                    found[link.current.pid] = ("in_service", sat)
        for value in self._in_flight.values():
            pkt = value["pkt"]
            if isinstance(pkt, DataPacket):
                found[pkt.pid] = ("in_flight", value.get("sat"))
        return found

    def _data_packets(self) -> dict[int, DataPacket]:
        packets: dict[int, DataPacket] = {}
        for ep in self.endpoints.values():
            packets.update({p.pid: p for p in ep.queue})
        for packets_by_cell in (srv.queues for srv in self.downlinks):
            for queue in packets_by_cell.values():
                packets.update({p.pid: p for p in queue})
        for links in self.isls:
            for link in links.values():
                packets.update({p.pid: p for p in link.data_q})
        for packets_at_sat in self.pending:
            packets.update({p.pid: p for p in packets_at_sat})
        return packets

    def validate_joint_plan(self, plan: q0.JointPlan) -> tuple[bool, tuple[str, ...]]:
        """Validate a Q0 plan without mutating kernel state.

        This is intentionally narrower than execution: it proves the plan is
        current and physically admissible at this instant.  Applying actions
        remains a separate atomic operation and is not exposed yet.
        """
        errors: list[str] = []
        ok, version_errors = q0.validate_plan_version(plan, self._state_version)
        errors.extend(version_errors)
        locations = self._data_packet_locations()
        packets = self._data_packets()
        forward_bits: dict[tuple[int, str], int] = {}
        deliver_bits: dict[int, int] = {}
        for action in plan.actions:
            location = locations.get(action.packet_id)
            if location is None:
                errors.append(f"packet {action.packet_id} is not live")
                continue
            if location[0] in ("in_service", "in_flight"):
                errors.append(f"packet {action.packet_id} is not actionable")
                continue
            if action.sat >= self.num_sats:
                errors.append(f"packet {action.packet_id}: sat {action.sat} out of range")
                continue
            packet = packets.get(action.packet_id)
            if packet is None:
                errors.append(f"packet {action.packet_id}: packet lookup failed")
                continue
            if location[0] != "pending":
                errors.append(f"packet {action.packet_id}: plan requires pending packet")
                continue
            if action.kind == "forward":
                if location[1] is not None and action.sat != location[1] \
                        and location[0] == "pending":
                    errors.append(f"packet {action.packet_id}: wrong pending satellite")
                    continue
                peer = self.topo.get(action.sat, {}).get(action.direction)
                if peer is None:
                    errors.append(f"packet {action.packet_id}: non-adjacent direction")
                    continue
                link = self.isls[action.sat].get(action.direction)
                if link is None:
                    errors.append(f"packet {action.packet_id}: ISL capacity unavailable")
                    continue
                forward_bits[(action.sat, action.direction)] = (
                    forward_bits.get((action.sat, action.direction), 0) + packet.bits)
            elif action.kind == "deliver":
                if action.packet_id not in locations:
                    continue
                ep = self.endpoints.get(packet.dst)
                link = ep.links.get(action.sat) if ep is not None else None
                if link is None or link.state != "active" \
                        or not self.geometry.ground_visible(action.sat, ep.lat, ep.lon, self.env.now):
                    errors.append(f"packet {action.packet_id}: deliver target unavailable")
                    continue
                if not self.downlinks[action.sat].room(packet.bits):
                    errors.append(f"packet {action.packet_id}: downlink capacity unavailable")
                deliver_bits[action.sat] = deliver_bits.get(action.sat, 0) + packet.bits
            else:
                if location[0] != "pending":
                    errors.append(f"packet {action.packet_id}: WAIT requires pending packet")
                elif action.until is None or action.until <= self.env.now or action.until > self.horizon:
                    errors.append(f"packet {action.packet_id}: invalid WAIT deadline")
        for (sat, direction), bits in forward_bits.items():
            link = self.isls[sat][direction]
            if link._used() + bits > self.cfg_links["isl_queue_bits"]:
                errors.append(f"ISL plan capacity overcommitted at {sat}:{direction}")
        for sat, bits in deliver_bits.items():
            if self.downlinks[sat].queued_bits + bits > self.cfg_access["downlink_queue_bits"]:
                errors.append(f"downlink plan capacity overcommitted at {sat}")
        return not errors, tuple(errors)

    def apply_joint_plan(self, plan: q0.JointPlan) -> tuple[bool, tuple[str, ...]]:
        """Atomically apply a validated pending-packet plan.

        The first Q0 execution contract intentionally accepts only packets in
        finite kernel ``pending`` lists.  All actions are revalidated against
        the same live version before any mutation, so an invalid action cannot
        partially consume a plan.
        """
        ok, errors = self.validate_joint_plan(plan)
        if not ok:
            return False, errors
        packets = self._data_packets()
        pending_by_pid = {
            pkt.pid: sat for sat, queue in enumerate(self.pending)
            for pkt in queue
        }
        for action in plan.actions:
            sat = pending_by_pid[action.packet_id]
            self.pending[sat].remove(packets[action.packet_id], self.env.now)
        for action in plan.actions:
            pkt = packets[action.packet_id]
            if action.kind == "forward":
                pkt.assigned_sat = None
                self.isls[action.sat][action.direction].put_data(pkt)
            elif action.kind == "deliver":
                self.downlinks[action.sat].put(pkt)
                pkt.assigned_sat = action.sat
            else:
                pkt.holding_until = action.until
                self._hold_packet(action.sat, pkt)
        if plan.actions:
            self._state_version += 1
            self.q0_plan_audit.append({
                "version": plan.version,
                "applied_at": float(self.env.now),
                "actions": len(plan.actions),
            })
        return True, ()

    # --------------------------------------------------------- transmission
    def _fire_interrupt(self, link: Link, at: float):
        yield self.env.timeout(max(0.0, at - self.env.now))
        if not link.interrupt.triggered:
            link.interrupt.succeed()

    def _transmit(self, dur: float, pkt, link_ref, occ_key: str,
                  owner=None):
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
            interrupt = link.interrupt if link is not None else None
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
                    nxt_up = ge.next_up(t0)
                    if nxt_up <= self.horizon:
                        ups.append(nxt_up)
                    self.mech["ge_waits"] += 1
                # Wait for the earliest of: link recovery, the actual
                # deadline, or the hard retirement interrupt.  The packet is
                # NEVER failed at t0 before its deadline: retirement may free
                # it for re-association, and the expiry fate may only be
                # assigned once the deadline is actually reached (or, with no
                # deadline, settle as IN_SYSTEM_AT_STOP at the horizon).
                wake_at = None
                for u in ups:
                    wake_at = u if wake_at is None else min(wake_at, u)
                if expiry is not None and expiry <= self.horizon:
                    wake_at = (expiry if wake_at is None
                               else min(wake_at, expiry))
                if wake_at is None:
                    # never available again within the horizon and no
                    # deadline: settle the packet at the exact horizon
                    if t0 >= self.horizon:
                        return "stalled"
                    wait = self.env.timeout(max(0.0, self.horizon - t0))
                else:
                    wait = self.env.timeout(max(0.0, wake_at - t0))
                # the down-wait MUST race the link retirement interrupt: a
                # retiring link's hard deadline applies to the waiting
                # service too ("retirement deadline races any in-flight
                # service").  Without the race the link stays pinned until
                # the outage recovers, blocking the whole server and every
                # endpoint on it.
                if interrupt is not None and not interrupt.triggered:
                    yield wait | interrupt
                else:
                    yield wait
                if retire_t is not None and self.env.now >= retire_t:
                    # hard retirement is due NOW: return "retired" so the
                    # caller performs the retirement side effect (release +
                    # requeue).  The packet is re-decided afterwards and, if
                    # the deadline has also been reached, fails there with
                    # the expiry fate -- the tie is resolved in favour of
                    # running the link lifecycle, not swallowed by the fate.
                    return "retired"
                if expiry is not None and expiry <= self.horizon \
                        and self.env.now >= expiry:
                    # the deadline has actually been reached while the link
                    # is still not usable: fail at the deadline
                    self._fail(pkt, expiry_fate)
                    return "fail"
                if wake_at is None and self.env.now >= self.horizon:
                    return "stalled"
                continue
            if owner is not None and owner._svc is not None \
                    and owner._svc[0] != t0:
                # service is about to actually start: restamp the caller's
                # _svc so the stop-time settle does not book the pre-service
                # down-wait as occupied (K2)
                owner._svc = (t0, occ_key)
            end = t0 + dur
            if owner is not None and owner._svc_phase == "waiting_for_link":
                # Real transmission starts only after every availability
                # check passed (geometry up, GE up, no retirement deadline).
                # Down-wait before this point must not be reported as
                # service progress: stamp the phase and start time here.
                owner._svc_phase = "transmitting"
                owner._tx_started_at = t0
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
            if retire_t is not None and retire_t <= fail_t:
                fail_t, fail_kind = retire_t, "RETIRE"
            # race the wait against a possibly later-scheduled retirement
            # interrupt: on ANY wake the whole race is recomputed from now.
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
            for pkt in self.pending[sat].sweep_expired(self.env.now):
                self._fail(pkt, "DATA_DEADLINE_EXPIRED")
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
        # GSL GE is part of the Q0 global-state universe: materialize it at
        # association so snapshot_global() can report every current
        # endpoint-satellite pair explicitly instead of silently omitting
        # not-yet-queried pairs (keyed RNG stream keeps this deterministic).
        self._gsl_ge(sat, ep.cell)
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
        root_pos = None
        if self.cfg_rt["contract"] in _learning.GRAPH_CONTRACTS:
            # The root satellite's own position is directly measured local
            # state: query geometry, never the control cache — the control
            # plane explicitly refuses to cache a satellite's own looped
            # advertisement, so a cache lookup would read (0, 0, 0).
            root_pos = self.geometry.positions(self.env.now)[sat]
        return _learning.build_observation(
            self.cfg_rt["contract"], sat, self.caches[sat], self.env.now,
            self.topo, own, self.cfg_links["isl_queue_bits"],
            obs_hops=obs_hops, dst_feats=dst_feats, root_pos=root_pos,
        )

    def _finish_learning_transition(self, pkt: DataPacket, next_state,
                                    next_mask: dict, done: bool,
                                    terminal_reward: float | None = None) -> None:
        if self.learner is None or pkt.learning_state is None:
            return
        if terminal_reward is None and pkt.learning_reward is None:
            # every reward is settled where the rewarded event actually
            # happens: the forward queue reward at ISL service start
            # (_transmit), the arrival reward at real delivery
            # (_deliver_after_prop, passed as terminal_reward). Reaching here
            # with neither means the reward was never realized — fail loud
            # instead of storing a silent None
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
        self._learning_open.discard(pkt)

    def _close_learning_at_stop(self) -> None:
        """Explicitly discard every learning transition still open at the
        stop time (packets pending re-decision, queued on an ISL/downlink,
        in service, or in propagation).

        A horizon-truncated episode is NOT remembered: fabricating a terminal
        reward for it would corrupt training. The discards are counted in the
        mechanism counters so the receipt can check
        ``decisions == transitions + discarded_at_stop`` instead of the
        difference vanishing silently."""
        if self.learner is None:
            return
        for pkt in self._learning_open:
            pkt.learning_state = None
            pkt.learning_action = None
            pkt.learning_reward = None
            self.mech["learning_discarded_at_stop"] += 1
        self._learning_open.clear()

    def _learning_action(self, pkt: DataPacket, sat: int, mask: dict) -> str:
        state = self._learning_observation(sat, pkt.dst)
        if pkt.learning_state is not None and pkt.learning_reward is None:
            # The only action allowed to be open without a settled reward is
            # deliver: its arrival reward exists only at real delivery. A
            # deliver that never reached the user (e.g. the downlink was hard
            # retired and the packet bounced back to pending) settles at 0 on
            # re-decision — it must NOT collect arrive_reward.
            if pkt.learning_action != "deliver":
                raise KernelError(
                    "unsettled non-deliver learning transition at re-decision "
                    f"(pid={pkt.pid}, action={pkt.learning_action})")
            self._finish_learning_transition(
                pkt, state, mask, False, terminal_reward=0.0)
        else:
            self._finish_learning_transition(pkt, state, mask, False)
        action = self.learner.choose(state, mask, self.env.now)
        # No reward is known at decision time by construction: a forward
        # action's M1 queue reward is settled when its ISL service actually
        # starts (_transmit); the deliver arrival reward is settled at real
        # delivery (_deliver_after_prop).
        pkt.learning_state = state
        pkt.learning_action = action
        pkt.learning_reward = None
        self._learning_open.add(pkt)
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
            "state_version": self._state_version,
            "pid": pkt.pid,
            "src": pkt.src,
            "dst": pkt.dst,
            "sat": sat,
            "kind": kind,
            "policy": (self.cfg_rt["policy"] if self.learner is None
                       else f"{self.cfg_learning['algorithm']}:{self.cfg_rt['contract']}"),
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
            # oracle_targets is consumed only by the oracle policy; compute it
            # only there instead of scanning serving satellites every decision
            oracle_targets=([s for s in self._serving_sats(pkt.dst) if s != sat]
                            if self.cfg_rt["policy"] == "oracle" else None),
            # learning must choose among ALL local legal directions: the
            # heuristic only orders candidates, it never pre-clips the
            # learner's action set (otherwise DDQN is a tie-breaker over the
            # heuristic-best path and cannot learn to deviate from it)
            best_only=False,
            reverse_adj=self._routing_reverse_adj,
            sorted_adj=self._routing_sorted_rev_adj)
        if status == "unreachable":
            self._fail(pkt, "NO_ROUTE")
            return
        if status == "no_info":
            if not self.cfg_cp["enabled"] and self.cfg_rt["policy"] != "oracle":
                self._fail(pkt, "NO_ROUTE")
            else:
                self._hold_packet(sat, pkt)  # wait for re-decision
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
                if action not in legal:
                    # fail loud like the deliver-only branch: a learner that
                    # returns an action outside the legal mask must never
                    # silently overflow an ISL queue (put_data does not
                    # re-check room())
                    raise KernelError(
                        f"learner selected action {action!r} outside the "
                        f"legal mask {sorted(legal)}")
            else:
                action = legal[0]
            self._record_decision(pkt, sat, "forward", legal, action)
            self.isls[sat][action].put_data(pkt)
            return
        if unavailable:
            self._hold_packet(sat, pkt)  # temporarily unavailable: wait
            return
        if cands:
            self._fail(pkt, "ISL_QUEUE_OVERFLOW")
        else:
            self._fail(pkt, "NO_ROUTE")  # every candidate loops

    def _redecide_pending(self, sat: int):
        if not self.pending[sat]:
            return
        waiting = self.pending[sat].take_ready(self.env.now)
        for pkt in waiting:
            self._decide(pkt, sat)

    def _ingress_after_prop(self, pkt: DataPacket, sat: int, prop: float):
        yield self.env.timeout(prop)
        self._in_flight.pop(pkt.pid, None)
        if pkt.deadline is not None and self.env.now > pkt.deadline:
            self._fail(pkt, "DATA_DEADLINE_EXPIRED")
            return
        pkt.path.append(sat)
        self._note_busy(pkt.dst)  # new downlink demand may have appeared
        self._decide(pkt, sat)

    def _isl_arrive_after_prop(self, pkt: DataPacket, sat: int, prop: float):
        yield self.env.timeout(prop)
        self._in_flight.pop(pkt.pid, None)
        if pkt.deadline is not None and self.env.now > pkt.deadline:
            self._fail(pkt, "DATA_DEADLINE_EXPIRED")
            return
        pkt.path.append(sat)
        self._note_busy(pkt.dst)  # new downlink demand may have appeared
        self._decide(pkt, sat)

    def _deliver_after_prop(self, pkt: DataPacket, sat: int, prop: float):
        yield self.env.timeout(prop)
        self._in_flight.pop(pkt.pid, None)
        now = self.env.now
        if pkt.deadline is not None and now > pkt.deadline:
            self._fail(pkt, "DATA_DEADLINE_EXPIRED")
            return
        self._finish_learning_transition(
            pkt, np.zeros(_learning.CONTRACT_DIMS[self.cfg_rt["contract"]]),
            {a: False for a in _learning.ACTIONS}, True,
            # the arrival reward (legacy ArriveReward,
            # ANALYSIS/REWARD-DIFF-20260816.md) exists only here, at real
            # delivery — never at the deliver decision
            terminal_reward=float(self.cfg_learning["arrive_reward"]),
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
                # simpy.peek() returns inf when the queue is empty; no
                # exception is expected here, so a raise must propagate
                # (fail loud) instead of being converted into a natural end
                t_next = self.env.peek()
                if t_next > self.horizon or t_next == math.inf:
                    break
                self.env.step()
                self._state_version += 1
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
            self.holding_areas[s].close(stop_time)
            self.downlinks[s].area.close(stop_time)
            for lnk in self.isls[s].values():
                lnk.data_area.close(stop_time)
                lnk.ctrl_area.close(stop_time)
        queue_area = {
            "uplink": sum(ep.area.area for ep in self.endpoints.values()),
            "downlink": sum(self.downlinks[s].area.area for s in range(self.num_sats)),
            "holding": sum(area.area for area in self.holding_areas),
            "isl_data": sum(lnk.data_area.area for s in range(self.num_sats)
                            for lnk in self.isls[s].values()),
            "isl_ctrl": sum(lnk.ctrl_area.area for s in range(self.num_sats)
                            for lnk in self.isls[s].values()),
        }
        self.access_stats["waiting_at_stop"] = sum(
            len(q) for q in self.access_wait)
        self._close_learning_at_stop()
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
                self.cfg_learning["algorithm"]
                if self.learner is not None else "none"),
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
