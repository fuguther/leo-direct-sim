import pytest

from CODE.leo_sim import config, kernel
from CODE.leo_sim.tests.helpers import StaticGeometry, cell, make_cfg, row


def test_queue_policy_retries_after_temporary_no_coverage_and_delivers():
    src, dst = cell(0.0, 0.0), cell(0.0, 10.0)
    geo = StaticGeometry(1, visible=lambda _s, _lat, _lon, t: t >= 0.5)
    cfg = make_cfg({"scenario": {"duration_s": 3.0},
                    "access": {"unavailable_policy": "queue"}})
    result = kernel.run_simulation(cfg, [row(1, 0.0, src, dst)], geometry=geo)
    assert result["fates"][1] == "DELIVERED"
    assert result["fate_counts"]["ACCESS_REJECTED"] == 0
    assert result["congestion_metrics"]["packets"]["1"]["admitted_at"] >= 0.5


def test_queue_policy_keeps_packet_in_system_when_window_never_visible():
    src, dst = cell(0.0, 0.0), cell(0.0, 10.0)
    cfg = make_cfg({"scenario": {"duration_s": 1.0},
                    "access": {"unavailable_policy": "queue"}})
    result = kernel.run_simulation(
        cfg, [row(1, 0.0, src, dst)],
        geometry=StaticGeometry(1, visible=lambda *_: False))
    assert result["fates"][1] == "IN_SYSTEM_AT_STOP"
    assert result["fate_counts"]["ACCESS_REJECTED"] == 0


def test_reject_policy_preserves_no_coverage_fate():
    src, dst = cell(0.0, 0.0), cell(0.0, 10.0)
    result = kernel.run_simulation(
        make_cfg({"scenario": {"duration_s": 1.0}},),
        [row(1, 0.0, src, dst)],
        geometry=StaticGeometry(1, visible=lambda *_: False))
    assert result["fates"][1] == "ACCESS_REJECTED"


def test_queue_policy_keeps_existing_finite_uplink_overflow():
    src, dst = cell(0.0, 0.0), cell(0.0, 10.0)
    cfg = make_cfg({"scenario": {"duration_s": 1.0},
                    "access": {"unavailable_policy": "queue",
                               "uplink_queue_bits": 100}})
    result = kernel.run_simulation(
        cfg, [row(1, 0.0, src, dst, bits=80), row(2, 0.0, src, dst, bits=80)],
        geometry=StaticGeometry(1, visible=lambda *_: False))
    assert result["fates"][1] == "IN_SYSTEM_AT_STOP"
    assert result["fates"][2] == "ACCESS_QUEUE_OVERFLOW"
