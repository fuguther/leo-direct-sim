"""Recomputeable congestion metrics from the kernel's raw event ledger.

The kernel records events; this module deliberately does not trust a pre-made
queue/latency/utilization number.  ``summarize`` rebuilds queue wait, actual
service time, propagation time, and service-window link utilization from those
events.  The utilization denominator is the capacity of recorded *service
windows* (rate multiplied by occupied transmission time), not all time a link
could theoretically have been available.
"""
from __future__ import annotations

import math
from collections import defaultdict


class MetricsError(ValueError):
    """Raw event ledger is malformed or internally inconsistent."""


def _finite(value, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise MetricsError(f"{name} must be numeric")
    value = float(value)
    if not math.isfinite(value):
        raise MetricsError(f"{name} must be finite")
    return value


def _pid(event: dict) -> int:
    value = event.get("pid")
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise MetricsError("event pid must be a non-negative integer")
    return value


def _nonempty(event: dict, key: str) -> str:
    value = event.get(key)
    if not isinstance(value, str) or not value:
        raise MetricsError(f"event {key} must be a non-empty string")
    return value


def summarize(packet_events: list[dict], service_windows: list[dict]) -> dict:
    """Return metrics rebuilt from raw packet and service-window events.

    A queue entry may remain unmatched when a packet is still queued or is
    terminated before service.  Every service start must, however, identify a
    known queue entry when it supplies ``queue_id``.  Propagation starts and
    arrivals are strict one-to-one pairs so a reported propagation delay cannot
    be manufactured from a delivery timestamp alone.
    """
    if not isinstance(packet_events, list) or not isinstance(service_windows, list):
        raise MetricsError("packet_events and service_windows must be lists")

    emitted: dict[int, float] = {}
    queue_entries: dict[int, tuple[int, float, str]] = {}
    queue_wait: defaultdict[int, float] = defaultdict(float)
    service_starts: dict[tuple[int, int], dict] = {}
    prop_starts: dict[tuple[int, int], dict] = {}
    prop_durations: defaultdict[int, float] = defaultdict(float)
    delivered: dict[int, float] = {}
    tx_durations: defaultdict[int, float] = defaultdict(float)
    holding_wait: defaultdict[int, float] = defaultdict(float)
    packet_bits: dict[int, int] = {}

    for event in packet_events:
        if not isinstance(event, dict):
            raise MetricsError("every packet event must be a mapping")
        kind = _nonempty(event, "kind")
        pid = _pid(event)
        at = _finite(event.get("at"), f"{kind}.at")
        if at < 0:
            raise MetricsError(f"{kind}.at must be non-negative")
        if kind == "packet_emitted":
            if pid in emitted:
                raise MetricsError(f"duplicate packet_emitted for {pid}")
            bits = event.get("bits")
            if isinstance(bits, bool) or not isinstance(bits, int) or bits <= 0:
                raise MetricsError("packet_emitted.bits must be a positive integer")
            emitted[pid] = at
            packet_bits[pid] = bits
        elif kind == "queue_enter":
            qid = event.get("queue_id")
            if isinstance(qid, bool) or not isinstance(qid, int) or qid < 0:
                raise MetricsError("queue_enter.queue_id must be a non-negative integer")
            if qid in queue_entries:
                raise MetricsError(f"duplicate queue_id {qid}")
            queue_entries[qid] = (pid, at, _nonempty(event, "queue"))
        elif kind == "service_start":
            stage = _nonempty(event, "stage")
            link_id = _nonempty(event, "link_id")
            rate = _finite(event.get("rate_bps"), "service_start.rate_bps")
            if rate <= 0:
                raise MetricsError("service_start.rate_bps must be positive")
            bits = event.get("bits")
            if isinstance(bits, bool) or not isinstance(bits, int) or bits <= 0:
                raise MetricsError("service_start.bits must be a positive integer")
            qid = event.get("queue_id")
            if qid is not None:
                if qid not in queue_entries:
                    raise MetricsError(f"unknown queue_id {qid}")
                qpid, entered_at, _ = queue_entries[qid]
                if qpid != pid:
                    raise MetricsError(f"queue_id {qid} belongs to packet {qpid}")
                if at < entered_at:
                    raise MetricsError("service_start precedes queue_enter")
                queue_wait[pid] += at - entered_at
            key = (pid, len([k for k in service_starts if k[0] == pid]))
            service_starts[key] = {
                "at": at, "stage": stage, "link_id": link_id,
                "bits": bits, "rate_bps": rate,
            }
        elif kind == "propagation_start":
            stage = _nonempty(event, "stage")
            _nonempty(event, "link_id")
            prop_id = event.get("prop_id")
            if isinstance(prop_id, bool) or not isinstance(prop_id, int) or prop_id < 0:
                raise MetricsError("propagation_start.prop_id must be a non-negative integer")
            delay = _finite(event.get("delay_s"), "propagation_start.delay_s")
            if delay < 0:
                raise MetricsError("propagation_start.delay_s must be non-negative")
            key = (pid, prop_id)
            if key in prop_starts:
                raise MetricsError(f"duplicate propagation start {key}")
            prop_starts[key] = {"at": at, "stage": stage, "delay_s": delay}
        elif kind == "propagation_arrival":
            prop_id = event.get("prop_id")
            key = (pid, prop_id)
            start = prop_starts.get(key)
            if start is None:
                raise MetricsError(f"unknown propagation id {key}")
            if at < start["at"]:
                raise MetricsError("propagation_arrival precedes start")
            realized = at - start["at"]
            if not math.isclose(realized, start["delay_s"], rel_tol=1e-9, abs_tol=1e-12):
                raise MetricsError(f"propagation delay mismatch for {key}")
            prop_durations[pid] += realized
            del prop_starts[key]
        elif kind == "delivered":
            if pid in delivered:
                raise MetricsError(f"duplicate delivered event for {pid}")
            delivered[pid] = at
        else:
            raise MetricsError(f"unknown packet event kind {kind!r}")

    if prop_starts:
        raise MetricsError(f"unmatched propagation starts: {sorted(prop_starts)}")

    # Holding is a real queue, but it has no service_start of its own.  Its
    # residence is therefore paired with the next downstream queue admission
    # for the same packet.  A packet still held at the horizon remains
    # unmatched and is intentionally not assigned a fabricated exit time.
    by_packet_queue = defaultdict(list)
    for event in packet_events:
        if event.get("kind") == "queue_enter":
            by_packet_queue[_pid(event)].append(event)
    for pid, entries in by_packet_queue.items():
        for index, entry in enumerate(entries[:-1]):
            if entry.get("queue") != "holding":
                continue
            nxt = entries[index + 1]
            leave_at = _finite(nxt.get("at"), "queue_enter.at")
            entered_at = _finite(entry.get("at"), "queue_enter.at")
            if leave_at < entered_at:
                raise MetricsError("holding queue exit precedes entry")
            holding_wait[pid] += leave_at - entered_at

    links: dict[str, dict] = {}
    for window in service_windows:
        if not isinstance(window, dict):
            raise MetricsError("every service window must be a mapping")
        pid = _pid(window)
        stage = _nonempty(window, "stage")
        link_id = _nonempty(window, "link_id")
        start = _finite(window.get("start"), "service_window.start")
        end = _finite(window.get("end"), "service_window.end")
        rate = _finite(window.get("rate_bps"), "service_window.rate_bps")
        if start < 0 or end < start or rate <= 0:
            raise MetricsError("invalid service window bounds/rate")
        duration = end - start
        capacity = rate * duration
        declared_capacity = _finite(window.get("capacity_bits"), "service_window.capacity_bits")
        if not math.isclose(capacity, declared_capacity, rel_tol=1e-9, abs_tol=1e-9):
            raise MetricsError("service_window capacity does not equal rate*time")
        served = _finite(window.get("served_bits"), "service_window.served_bits")
        bits = window.get("bits", packet_bits.get(pid, 0))
        if isinstance(bits, bool) or not isinstance(bits, int) or bits <= 0:
            raise MetricsError("service_window.bits must be a positive integer")
        if served < 0 or served > bits:
            raise MetricsError("service_window.served_bits outside packet bounds")
        if served > capacity * (1.0 + 1e-9):
            raise MetricsError("service_window served bits exceed capacity")
        if window.get("outcome") == "ok" and not math.isclose(served, bits):
            raise MetricsError("successful service window must serve whole packet")
        tx_durations[pid] += duration
        item = links.setdefault(link_id, {
            "stage": stage, "capacity_bits": 0.0, "served_bits": 0.0,
            "service_windows": 0,
        })
        if item["stage"] != stage:
            raise MetricsError(f"link {link_id} changes stage")
        item["capacity_bits"] += capacity
        item["served_bits"] += served
        item["service_windows"] += 1

    for item in links.values():
        item["utilization"] = min(
            1.0,
            item["served_bits"] / item["capacity_bits"]
            if item["capacity_bits"] else 0.0)

    packets = {}
    for pid in sorted(set(emitted) | set(delivered) | set(queue_wait)
                       | set(tx_durations) | set(prop_durations)):
        item = {
            "emitted_at": emitted.get(pid),
            "queue_wait_s": queue_wait.get(pid, 0.0),
            "holding_wait_s": holding_wait.get(pid, 0.0),
            "tx_s": tx_durations.get(pid, 0.0),
            "prop_s": prop_durations.get(pid, 0.0),
        }
        item["total_queue_wait_s"] = item["queue_wait_s"] + item["holding_wait_s"]
        if pid in delivered:
            if pid not in emitted:
                raise MetricsError(f"delivered packet {pid} was never emitted")
            item["delivered_at"] = delivered[pid]
            item["e2e_s"] = delivered[pid] - emitted[pid]
            if item["e2e_s"] < 0:
                raise MetricsError(f"negative e2e delay for packet {pid}")
        packets[str(pid)] = item

    return {
        "schema": "leo-sim-congestion-metrics/v1",
        "packets": packets,
        "links": links,
        "validation": {"ok": True, "errors": []},
    }
