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
        "bits": 100, "outcome": "ok",
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


def test_summarize_uses_idle_physical_capacity_as_utilization_denominator():
    windows = [{
        "pid": 1, "stage": "isl", "link_id": "isl:0:1",
        "start": 0.5, "end": 0.75, "rate_bps": 400.0,
        "capacity_bits": 100.0, "served_bits": 100,
        "bits": 100, "outcome": "ok",
    }]
    available = [{
        "stage": "isl", "link_id": "isl:0:1",
        "start": 0.0, "end": 1.0, "rate_bps": 400.0,
        "capacity_bits": 400.0,
    }]
    got = metrics.summarize([], windows,
                            available_capacity_windows=available)
    link = got["links"]["isl:0:1"]
    assert link["capacity_bits"] == pytest.approx(100.0)
    assert link["available_capacity_bits"] == pytest.approx(400.0)
    assert link["available_time_s"] == pytest.approx(1.0)
    assert link["available_samples"] == 1
    assert link["utilization"] == pytest.approx(0.25)


def test_summarize_rejects_service_above_sampled_available_capacity():
    with pytest.raises(metrics.MetricsError, match="available capacity"):
        metrics.summarize(
            [], [{
                "pid": 1, "stage": "isl", "link_id": "isl:0:1",
                "start": 0.0, "end": 1.0, "rate_bps": 200.0,
                "capacity_bits": 200.0, "served_bits": 200,
                "bits": 200, "outcome": "ok",
            }],
            available_capacity_windows=[{
                "stage": "isl", "link_id": "isl:0:1",
                "start": 0.0, "end": 1.0, "rate_bps": 100.0,
                "capacity_bits": 100.0,
            }])


def test_summarize_rejects_orphan_service_start():
    with pytest.raises(metrics.MetricsError, match="unknown queue_id"):
        metrics.summarize([
            {"kind": "service_start", "pid": 1, "at": 0.0,
             "stage": "isl", "link_id": "isl:0:1", "queue_id": 99,
             "bits": 100, "rate_bps": 400.0},
        ], [])


def test_summarize_accepts_in_flight_packet_without_fabricating_arrival():
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
    ]
    windows = [{
        "pid": 1, "stage": "isl", "link_id": "isl:0:1",
        "start": 0.5, "end": 0.75, "rate_bps": 400.0,
        "capacity_bits": 100.0, "served_bits": 100,
        "outcome": "ok",
    }]

    with pytest.raises(metrics.MetricsError, match="unmatched propagation"):
        metrics.summarize(events, windows)

    got = metrics.summarize(events, windows, non_arrival_pids={1})
    packet = got["packets"]["1"]
    assert packet["prop_s"] == pytest.approx(0.0)
    assert "e2e_s" not in packet


def test_receipt_recomputation_uses_fate_qualified_in_flight_set(tmp_path):
    """An in-flight packet at horizon remains verifiable from raw events."""
    import hashlib
    from CODE.leo_sim import receipt, trace

    cfg = make_cfg({
        "scenario": {"duration_s": 0.1},
        "endpoints": {"sites": [
            {"name": "a", "lat": 0.0, "lon": 0.0},
            {"name": "b", "lat": 0.0, "lon": 10.0},
        ]},
        "demand": {"mode": "csv", "csv_path": str(tmp_path / "input.csv")},
    })
    (tmp_path / "input.csv").write_text(
        "packet_id,emit_time_s,src_lat,src_lon,dst_lat,dst_lon,bits,deadline_at_s\n"
        "1,0.099,0.0,0.0,0.0,10.0,8000000,\n",
        encoding="utf-8")
    trace_dir = tmp_path / "trace"
    manifest = trace.compile_trace(cfg, str(trace_dir))
    trace_bytes = (trace_dir / "trace.csv").read_bytes()
    manifest["__trace_sha256"] = hashlib.sha256(trace_bytes).hexdigest()
    manifest["__sha256"] = hashlib.sha256(
        (trace_dir / "manifest.json").read_bytes()).hexdigest()
    geo = StaticGeometry(2, visible=lambda *_: True,
                         neighbors_map={0: {"E": 1}, 1: {"W": 0}},
                         slant_km=600.0)
    result = kernel.run_simulation(
        cfg, trace.load_trace(str(trace_dir / "trace.csv"),
                              horizon_s=0.1,
                              max_packets=cfg["config"]["execution"]["max_packets"]),
        geometry=geo)
    assert result["fate_counts"]["IN_SYSTEM_AT_STOP"] == 1
    out = tmp_path / "run"
    receipt.write_run(str(out), cfg, trace_bytes, manifest, result,
                      trace.load_trace(str(trace_dir / "trace.csv"),
                                       horizon_s=0.1,
                                       max_packets=cfg["config"]["execution"]["max_packets"]))
    assert receipt.verify_receipt_dir(str(out)) == []


def test_kernel_persists_real_event_metrics_for_a_delivered_packet():
    a = cell(0.0, 0.0)
    b = cell(0.0, 10.0)
    geo = StaticGeometry(1, visible=lambda *_: True)
    result = kernel.run_simulation(
        make_cfg({"scenario": {"num_satellites": 1, "num_planes": 1},
                  "execution": {"available_capacity_interval_s": 1.0}}),
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
    assert result["link_available_windows"]
    assert any(v["available_capacity_bits"] > v["capacity_bits"]
               for v in result["congestion_metrics"]["links"].values())


def test_capacity_metric_splits_scripted_visibility_change_inside_interval():
    class Flap(StaticGeometry):
        def __init__(self):
            super().__init__(1, visible=lambda *_: True,
                             gsl_changes=[0.25, 0.75])

        def ground_visible(self, sat_id, lat, lon, t):
            return 0.25 <= t < 0.75

    result = kernel.run_simulation(
        make_cfg({"scenario": {"duration_s": 1.0},
                  "execution": {"available_capacity_interval_s": 1.0}}),
        [row(1, 0.0, cell(0.0, 0.0), cell(0.0, 10.0))],
        geometry=Flap())
    link_id = f"gsl:uplink:0:{cell(0.0, 0.0)}"
    windows = [w for w in result["link_available_windows"]
               if w["link_id"] == link_id]
    assert [(w["start"], w["end"]) for w in windows] == [(0.25, 0.75)]


def test_capacity_metric_includes_retired_isl_generation():
    from CODE.leo_sim.tests.test_dynamic_topology import _cfg, _geometry

    cfg = _cfg()
    cfg["config"]["execution"]["available_capacity_interval_s"] = 1.0
    result = kernel.run_simulation(cfg, [], geometry=_geometry())
    assert any(w["link_id"] == "isl:0:1"
               for w in result["link_available_windows"])
