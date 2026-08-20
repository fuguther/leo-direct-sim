"""Tests for the event-backed congestion and link-utilization metrics."""

import pytest

from CODE.leo_sim import metrics
from CODE.leo_sim import kernel
from CODE.leo_sim.tests.helpers import StaticGeometry, cell, make_cfg, row


def test_summarize_recomputes_queue_tx_propagation_and_link_utilization():
    events = [
        {"kind": "packet_emitted", "pid": 1, "at": 0.0, "bits": 100},
        {"kind": "queue_enter", "pid": 1, "at": 0.0, "queue": "isl",
         "queue_id": 7},
        {"kind": "service_start", "pid": 1, "at": 0.5,
         "stage": "isl", "link_id": "isl:0:1", "queue_id": 7,
         "bits": 100, "rate_bps": 400.0},
        {"kind": "propagation_start", "pid": 1, "at": 0.75,
         "stage": "isl", "link_id": "isl:0:1", "prop_id": 3,
         "delay_s": 0.25},
        {"kind": "propagation_arrival", "pid": 1, "at": 1.0,
         "stage": "isl", "prop_id": 3},
        {"kind": "delivered", "pid": 1, "at": 1.0},
    ]
    windows = [{
        "pid": 1, "stage": "isl", "link_id": "isl:0:1",
        "start": 0.5, "end": 0.75, "rate_bps": 400.0,
        "capacity_bits": 100.0, "served_bits": 100,
        "outcome": "ok",
    }]

    got = metrics.summarize(events, windows)

    packet = got["packets"]["1"]
    assert packet["queue_wait_s"] == pytest.approx(0.5)
    assert packet["tx_s"] == pytest.approx(0.25)
    assert packet["prop_s"] == pytest.approx(0.25)
    assert packet["e2e_s"] == pytest.approx(1.0)
    link = got["links"]["isl:0:1"]
    assert link["capacity_bits"] == pytest.approx(100.0)
    assert link["served_bits"] == 100
    assert link["utilization"] == pytest.approx(1.0)
    assert got["validation"]["ok"] is True


def test_summarize_rejects_orphan_service_start():
    with pytest.raises(metrics.MetricsError, match="unknown queue_id"):
        metrics.summarize([
            {"kind": "service_start", "pid": 1, "at": 0.0,
             "stage": "isl", "link_id": "isl:0:1", "queue_id": 99,
             "bits": 100, "rate_bps": 400.0},
        ], [])


def test_kernel_persists_real_event_metrics_for_a_delivered_packet():
    a = cell(0.0, 0.0)
    b = cell(0.0, 10.0)
    geo = StaticGeometry(1, visible=lambda *_: True)
    result = kernel.run_simulation(
        make_cfg({"scenario": {"num_satellites": 1, "num_planes": 1}}),
        [row(1, 0.0, a, b)], geometry=geo)

    packet = result["congestion_metrics"]["packets"]["1"]
    assert result["congestion_metrics"]["validation"]["ok"] is True
    assert packet["queue_wait_s"] >= 0.0
    assert packet["tx_s"] > 0.0
    assert packet["prop_s"] > 0.0
    assert packet["e2e_s"] == pytest.approx(
        result["deliveries"][1]["delivered_at"])
    assert result["packet_events"]
    assert result["link_service_windows"]
