"""Tests for fixed-window directed-ISL pressure diagnostics."""
from __future__ import annotations

import pytest

from CODE.experiment_platform import isl_pressure


def _base_ledgers() -> dict:
    return {
        "stop_time_s": 30.0,
        "packet_events": [],
        "link_service_windows": [],
        "link_available_windows": [],
    }


def test_two_second_burst_is_visible_when_horizon_aggregate_is_low():
    ledgers = _base_ledgers()
    ledgers["packet_events"] = [
        {"kind": "packet_emitted", "pid": 1, "at": 0.0, "bits": 200},
        {"kind": "queue_enter", "pid": 1, "at": 8.0,
         "queue": "isl", "link_id": "isl:1:2", "queue_id": 7},
        {"kind": "service_start", "pid": 1, "at": 10.0,
         "stage": "isl", "link_id": "isl:1:2", "queue_id": 7,
         "bits": 200, "rate_bps": 100.0},
    ]
    ledgers["link_service_windows"] = [{
        "pid": 1, "stage": "isl", "link_id": "isl:1:2",
        "start": 10.0, "end": 12.0, "rate_bps": 100.0,
        "capacity_bits": 200.0, "served_bits": 200.0,
        "bits": 200, "outcome": "ok",
    }]
    ledgers["link_available_windows"] = [{
        "stage": "isl", "link_id": "isl:1:2",
        "start": 0.0, "end": 30.0, "rate_bps": 100.0,
        "capacity_bits": 3000.0,
    }]

    got = isl_pressure.analyze_windows(ledgers)

    link = got["links"]["isl:1:2"]
    assert link["horizon_utilization"] == pytest.approx(2 / 30)
    assert link["max_window_utilization"] == pytest.approx(1.0)
    assert link["longest_consecutive_high_windows"] == 2
    assert link["high_window_starts_s"] == [10.0, 11.0]
    assert link["matched_queue_wait_bits_s"] == pytest.approx(400.0)
    assert link["max_matched_queue_wait_s"] == pytest.approx(2.0)
    assert got["sustained_hotspot_link_ids"] == ["isl:1:2"]
    assert got["unmatched_isl_queue_entries"] == 0


def test_partial_overlap_and_rate_are_allocated_to_exact_bins():
    ledgers = _base_ledgers()
    ledgers["stop_time_s"] = 2.0
    ledgers["link_service_windows"] = [{
        "pid": 1, "stage": "isl", "link_id": "isl:3:4",
        "start": 0.75, "end": 1.25, "rate_bps": 100.0,
        "capacity_bits": 50.0, "served_bits": 50.0,
        "bits": 50, "outcome": "ok",
    }]
    ledgers["link_available_windows"] = [{
        "stage": "isl", "link_id": "isl:3:4",
        "start": 0.5, "end": 1.5, "rate_bps": 100.0,
        "capacity_bits": 100.0,
    }]

    got = isl_pressure.analyze_windows(
        ledgers, min_available_fraction=0.5)
    windows = got["links"]["isl:3:4"]["windows"]

    assert [item["served_bits"] for item in windows] == pytest.approx([25, 25])
    assert [item["available_capacity_bits"] for item in windows] == \
        pytest.approx([50, 50])
    assert [item["available_time_s"] for item in windows] == \
        pytest.approx([0.5, 0.5])
    assert [item["utilization"] for item in windows] == pytest.approx([0.5, 0.5])


def test_service_without_available_capacity_fails_loud():
    ledgers = _base_ledgers()
    ledgers["stop_time_s"] = 1.0
    ledgers["link_service_windows"] = [{
        "pid": 1, "stage": "isl", "link_id": "isl:5:6",
        "start": 0.0, "end": 1.0, "rate_bps": 10.0,
        "capacity_bits": 10.0, "served_bits": 10.0,
        "bits": 10, "outcome": "ok",
    }]

    with pytest.raises(isl_pressure.PressureAnalysisError,
                       match="served bits without available capacity"):
        isl_pressure.analyze_windows(ledgers)


def test_overlapping_service_windows_on_one_directed_link_fail_loud():
    ledgers = _base_ledgers()
    ledgers["stop_time_s"] = 2.0
    ledgers["link_available_windows"] = [{
        "stage": "isl", "link_id": "isl:7:8",
        "start": 0.0, "end": 2.0, "rate_bps": 100.0,
        "capacity_bits": 200.0,
    }]
    ledgers["link_service_windows"] = [
        {"pid": 1, "stage": "isl", "link_id": "isl:7:8",
         "start": 0.0, "end": 1.0, "rate_bps": 50.0,
         "capacity_bits": 50.0, "served_bits": 50.0,
         "bits": 50, "outcome": "ok"},
        {"pid": 2, "stage": "isl", "link_id": "isl:7:8",
         "start": 0.5, "end": 1.5, "rate_bps": 50.0,
         "capacity_bits": 50.0, "served_bits": 50.0,
         "bits": 50, "outcome": "ok"},
    ]

    with pytest.raises(isl_pressure.PressureAnalysisError,
                       match="overlapping service windows"):
        isl_pressure.analyze_windows(ledgers)


def test_unmatched_isl_queue_entry_is_reported_not_fabricated():
    ledgers = _base_ledgers()
    ledgers["stop_time_s"] = 1.0
    ledgers["packet_events"] = [
        {"kind": "packet_emitted", "pid": 9, "at": 0.0, "bits": 100},
        {"kind": "queue_enter", "pid": 9, "at": 0.2,
         "queue": "isl", "link_id": "isl:9:10", "queue_id": 1},
    ]
    ledgers["link_available_windows"] = [{
        "stage": "isl", "link_id": "isl:9:10",
        "start": 0.0, "end": 1.0, "rate_bps": 100.0,
        "capacity_bits": 100.0,
    }]

    got = isl_pressure.analyze_windows(ledgers)

    assert got["matched_isl_queue_entries"] == 0
    assert got["unmatched_isl_queue_entries"] == 1
    assert got["links"]["isl:9:10"]["matched_queue_wait_bits_s"] == 0.0


def test_zero_duration_unsuccessful_service_window_is_ignored():
    ledgers = _base_ledgers()
    ledgers["stop_time_s"] = 1.0
    ledgers["link_available_windows"] = [{
        "stage": "isl", "link_id": "isl:11:12",
        "start": 0.0, "end": 1.0, "rate_bps": 100.0,
        "capacity_bits": 100.0,
    }]
    ledgers["link_service_windows"] = [{
        "pid": 1, "stage": "isl", "link_id": "isl:11:12",
        "start": 0.5, "end": 0.5, "rate_bps": 100.0,
        "capacity_bits": 0.0, "served_bits": 0.0,
        "bits": 100, "outcome": "interrupted",
    }]

    got = isl_pressure.analyze_windows(ledgers)

    assert got["links"]["isl:11:12"]["horizon_served_bits"] == 0.0
    assert got["links"]["isl:11:12"]["windows"] == []
