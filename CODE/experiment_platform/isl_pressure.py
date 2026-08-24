"""Recompute fixed-window directed-ISL pressure evidence from raw ledgers.

The formal congestion metric is intentionally horizon-aggregate.  This module
adds a diagnostic view for short-lived pressure without changing the simulator
or inventing queue samples.  ISL queue waiting is reconstructed only for
queue entries that have an exact ``service_start`` match; unmatched entries are
reported as censored rather than assigned a fabricated exit time.
"""
from __future__ import annotations

import math
from typing import Any


class PressureAnalysisError(ValueError):
    """Raw window evidence is malformed or internally inconsistent."""


def _finite(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) \
            or not math.isfinite(float(value)):
        raise PressureAnalysisError(f"{label} must be finite numeric")
    return float(value)


def _nonempty(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise PressureAnalysisError(f"{label} must be a non-empty string")
    return value


def _pid(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise PressureAnalysisError(f"{label} must be a non-negative integer")
    return value


def _percentile(values: list[float], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    rank = max(0, math.ceil(fraction * len(ordered)) - 1)
    return ordered[rank]


def _longest_consecutive(indices: list[int]) -> int:
    longest = current = 0
    previous: int | None = None
    for index in indices:
        current = current + 1 if previous is not None and index == previous + 1 else 1
        longest = max(longest, current)
        previous = index
    return longest


def analyze_windows(
        ledgers: dict[str, Any], *, window_s: float = 1.0,
        min_available_fraction: float = 0.9,
        high_utilization: float = 0.8,
        min_consecutive_high_windows: int = 2) -> dict[str, Any]:
    """Return exact-overlap 1-D window diagnostics for directed ISLs.

    Service and available-capacity intervals are apportioned by their overlap
    with fixed bins.  A successful constant-rate service interval therefore
    contributes served bits uniformly in time.  This does not infer demand;
    it only rebins already receipt-verified physical service evidence.
    """
    if not isinstance(ledgers, dict):
        raise PressureAnalysisError("ledgers must be a mapping")
    stop = _finite(ledgers.get("stop_time_s"), "stop_time_s")
    window_s = _finite(window_s, "window_s")
    min_available_fraction = _finite(
        min_available_fraction, "min_available_fraction")
    high_utilization = _finite(high_utilization, "high_utilization")
    if stop <= 0 or window_s <= 0:
        raise PressureAnalysisError("stop_time_s and window_s must be positive")
    if not 0 < min_available_fraction <= 1:
        raise PressureAnalysisError(
            "min_available_fraction must be in (0, 1]")
    if not 0 < high_utilization <= 1:
        raise PressureAnalysisError("high_utilization must be in (0, 1]")
    if isinstance(min_consecutive_high_windows, bool) or not isinstance(
            min_consecutive_high_windows, int) \
            or min_consecutive_high_windows < 1:
        raise PressureAnalysisError(
            "min_consecutive_high_windows must be a positive integer")

    packet_events = ledgers.get("packet_events")
    service_windows = ledgers.get("link_service_windows")
    available_windows = ledgers.get("link_available_windows")
    if not isinstance(packet_events, list) or not isinstance(
            service_windows, list) or not isinstance(available_windows, list):
        raise PressureAnalysisError(
            "packet_events and link window ledgers must be lists")

    bin_count = math.ceil(stop / window_s)
    links: dict[str, dict[str, Any]] = {}

    def ensure(link_id: str) -> dict[str, Any]:
        return links.setdefault(link_id, {
            "served": [0.0] * bin_count,
            "capacity": [0.0] * bin_count,
            "available_time": [0.0] * bin_count,
            "queue_area": [0.0] * bin_count,
            "max_queue_wait_s": 0.0,
            "matched_queue_entries": 0,
        })

    def allocate(start: float, end: float, callback) -> None:
        first = max(0, int(math.floor(start / window_s)))
        last = min(bin_count - 1,
                   max(first, int(math.ceil(end / window_s) - 1)))
        for index in range(first, last + 1):
            bin_start = index * window_s
            bin_end = min(stop, bin_start + window_s)
            overlap = max(0.0, min(end, bin_end) - max(start, bin_start))
            if overlap > 0:
                callback(index, overlap)

    interval_sets: dict[tuple[str, str], list[tuple[float, float]]] = {}

    def record_interval(kind: str, link_id: str, start: float, end: float) -> None:
        interval_sets.setdefault((kind, link_id), []).append((start, end))

    for raw in available_windows:
        if not isinstance(raw, dict):
            raise PressureAnalysisError(
                "every available-capacity window must be a mapping")
        if raw.get("stage") != "isl":
            continue
        link_id = _nonempty(raw.get("link_id"), "available.link_id")
        start = _finite(raw.get("start"), f"{link_id}.available.start")
        end = _finite(raw.get("end"), f"{link_id}.available.end")
        rate = _finite(raw.get("rate_bps"), f"{link_id}.available.rate_bps")
        capacity = _finite(
            raw.get("capacity_bits"), f"{link_id}.available.capacity_bits")
        if start < 0 or end <= start or end > stop + 1e-9 or rate <= 0:
            raise PressureAnalysisError(f"invalid available window for {link_id}")
        if not math.isclose(capacity, rate * (end - start),
                            rel_tol=1e-9, abs_tol=1e-6):
            raise PressureAnalysisError(
                f"available capacity mismatch for {link_id}")
        record_interval("available", link_id, start, end)
        item = ensure(link_id)
        allocate(start, end, lambda index, overlap: (
            item["capacity"].__setitem__(
                index, item["capacity"][index] + rate * overlap),
            item["available_time"].__setitem__(
                index, item["available_time"][index] + overlap),
        ))

    for raw in service_windows:
        if not isinstance(raw, dict):
            raise PressureAnalysisError(
                "every service window must be a mapping")
        if raw.get("stage") != "isl":
            continue
        link_id = _nonempty(raw.get("link_id"), "service.link_id")
        start = _finite(raw.get("start"), f"{link_id}.service.start")
        end = _finite(raw.get("end"), f"{link_id}.service.end")
        rate = _finite(raw.get("rate_bps"), f"{link_id}.service.rate_bps")
        capacity = _finite(
            raw.get("capacity_bits"), f"{link_id}.service.capacity_bits")
        served = _finite(raw.get("served_bits"), f"{link_id}.served_bits")
        if start < 0 or end < start or end > stop + 1e-9 or rate <= 0:
            raise PressureAnalysisError(f"invalid service window for {link_id}")
        if not math.isclose(capacity, rate * (end - start),
                            rel_tol=1e-9, abs_tol=1e-6):
            raise PressureAnalysisError(
                f"service capacity mismatch for {link_id}")
        if served < 0 or served > capacity * (1 + 1e-9):
            raise PressureAnalysisError(
                f"served bits exceed service capacity for {link_id}")
        if end == start:
            if capacity != 0 or served != 0:
                raise PressureAnalysisError(
                    f"zero-duration service carries bits for {link_id}")
            ensure(link_id)
            continue
        record_interval("service", link_id, start, end)
        item = ensure(link_id)
        served_rate = served / (end - start)
        allocate(start, end, lambda index, overlap: item["served"].__setitem__(
            index, item["served"][index] + served_rate * overlap))

    for (kind, link_id), intervals in interval_sets.items():
        previous_end = -1.0
        for start, end in sorted(intervals):
            if start < previous_end - 1e-9:
                raise PressureAnalysisError(
                    f"overlapping {kind} windows for {link_id}")
            previous_end = max(previous_end, end)

    emitted_bits: dict[int, int] = {}
    queue_entries: dict[int, dict[str, Any]] = {}
    service_starts: list[dict[str, Any]] = []
    for raw in packet_events:
        if not isinstance(raw, dict):
            raise PressureAnalysisError("every packet event must be a mapping")
        kind = raw.get("kind")
        if kind == "packet_emitted":
            pid = _pid(raw.get("pid"), "packet_emitted.pid")
            bits = raw.get("bits")
            if isinstance(bits, bool) or not isinstance(bits, int) or bits <= 0:
                raise PressureAnalysisError(
                    "packet_emitted.bits must be a positive integer")
            if pid in emitted_bits:
                raise PressureAnalysisError(f"duplicate packet_emitted for {pid}")
            emitted_bits[pid] = bits
        elif kind == "queue_enter" and raw.get("queue") == "isl":
            qid = raw.get("queue_id")
            if isinstance(qid, bool) or not isinstance(qid, int) or qid < 0:
                raise PressureAnalysisError(
                    "queue_enter.queue_id must be a non-negative integer")
            if qid in queue_entries:
                raise PressureAnalysisError(f"duplicate queue_id {qid}")
            queue_entries[qid] = {
                "pid": _pid(raw.get("pid"), "queue_enter.pid"),
                "at": _finite(raw.get("at"), "queue_enter.at"),
                "link_id": _nonempty(raw.get("link_id"),
                                     "queue_enter.link_id"),
            }
        elif kind == "service_start" and raw.get("stage") == "isl" \
                and raw.get("queue_id") is not None:
            service_starts.append(raw)

    matched_qids: set[int] = set()
    max_wait_global = 0.0
    for raw in service_starts:
        qid = raw.get("queue_id")
        if qid in matched_qids:
            raise PressureAnalysisError(f"queue_id {qid} starts service twice")
        entry = queue_entries.get(qid)
        if entry is None:
            raise PressureAnalysisError(f"unknown ISL queue_id {qid}")
        pid = _pid(raw.get("pid"), "service_start.pid")
        link_id = _nonempty(raw.get("link_id"), "service_start.link_id")
        start = _finite(raw.get("at"), "service_start.at")
        if pid != entry["pid"] or link_id != entry["link_id"]:
            raise PressureAnalysisError(
                f"ISL queue/service identity mismatch for queue_id {qid}")
        if start < entry["at"]:
            raise PressureAnalysisError(
                f"ISL service precedes queue entry for queue_id {qid}")
        bits = emitted_bits.get(pid)
        if bits is None:
            bits = raw.get("bits")
        if isinstance(bits, bool) or not isinstance(bits, int) or bits <= 0:
            raise PressureAnalysisError(
                f"missing packet bits for ISL queue_id {qid}")
        wait = start - entry["at"]
        item = ensure(link_id)
        item["matched_queue_entries"] += 1
        item["max_queue_wait_s"] = max(item["max_queue_wait_s"], wait)
        max_wait_global = max(max_wait_global, wait)
        allocate(entry["at"], start,
                 lambda index, overlap: item["queue_area"].__setitem__(
                     index, item["queue_area"][index] + bits * overlap))
        matched_qids.add(qid)

    output_links: dict[str, Any] = {}
    sustained: list[str] = []
    active_utilizations: list[float] = []
    for link_id, raw in sorted(links.items()):
        windows: list[dict[str, float | bool]] = []
        eligible_indices: list[int] = []
        high_indices: list[int] = []
        for index in range(bin_count):
            start = index * window_s
            end = min(stop, start + window_s)
            capacity = raw["capacity"][index]
            served = raw["served"][index]
            available_time = raw["available_time"][index]
            queue_area = raw["queue_area"][index]
            if served > 1e-9 and capacity <= 0:
                raise PressureAnalysisError(
                    f"served bits without available capacity for {link_id} "
                    f"at {start}")
            if served > capacity * (1 + 1e-9):
                raise PressureAnalysisError(
                    f"served bits exceed available capacity for {link_id} "
                    f"at {start}")
            duration = end - start
            eligible = available_time >= min_available_fraction * duration - 1e-9
            utilization = served / capacity if capacity > 0 else 0.0
            if eligible:
                eligible_indices.append(index)
                if served > 0:
                    active_utilizations.append(utilization)
                if utilization >= high_utilization - 1e-12:
                    high_indices.append(index)
            if served > 0 or queue_area > 0:
                windows.append({
                    "start_s": start,
                    "end_s": end,
                    "served_bits": served,
                    "available_capacity_bits": capacity,
                    "available_time_s": available_time,
                    "utilization": utilization,
                    "eligible": eligible,
                    "matched_queue_wait_bits_s": queue_area,
                })
        longest = _longest_consecutive(high_indices)
        if longest >= min_consecutive_high_windows:
            sustained.append(link_id)
        total_capacity = sum(raw["capacity"])
        total_served = sum(raw["served"])
        output_links[link_id] = {
            "horizon_served_bits": total_served,
            "horizon_available_capacity_bits": total_capacity,
            "horizon_available_time_s": sum(raw["available_time"]),
            "horizon_utilization": (
                total_served / total_capacity if total_capacity > 0 else 0.0),
            "eligible_window_count": len(eligible_indices),
            "active_window_count": sum(
                1 for index in eligible_indices if raw["served"][index] > 0),
            "max_window_utilization": max(
                (raw["served"][index] / raw["capacity"][index]
                 for index in eligible_indices if raw["capacity"][index] > 0),
                default=0.0),
            "high_window_count": len(high_indices),
            "high_window_starts_s": [index * window_s for index in high_indices],
            "longest_consecutive_high_windows": longest,
            "matched_queue_entries": raw["matched_queue_entries"],
            "matched_queue_wait_bits_s": sum(raw["queue_area"]),
            "max_matched_queue_wait_s": raw["max_queue_wait_s"],
            "windows": windows,
        }

    return {
        "schema": "leo-sim-isl-window-pressure/v1",
        "window_s": window_s,
        "stop_time_s": stop,
        "min_available_fraction": min_available_fraction,
        "high_utilization_threshold": high_utilization,
        "min_consecutive_high_windows": min_consecutive_high_windows,
        "directed_isl_link_count": len(output_links),
        "active_window_utilization_p99": _percentile(
            active_utilizations, 0.99),
        "max_window_utilization": max(active_utilizations, default=0.0),
        "sustained_hotspot_link_ids": sustained,
        "matched_isl_queue_entries": len(matched_qids),
        "unmatched_isl_queue_entries": len(set(queue_entries) - matched_qids),
        "max_matched_isl_queue_wait_s": max_wait_global,
        "links": output_links,
    }
