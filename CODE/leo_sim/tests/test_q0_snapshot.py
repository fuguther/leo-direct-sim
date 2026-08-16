"""Q0 readiness: read-only global state snapshot interface."""
import pytest

from CODE.leo_sim import kernel
from CODE.leo_sim.tests.helpers import StaticGeometry, cell, make_cfg, row

A, B = cell(0.0, 0.0), cell(0.0, 10.0)


def _cfg(**over):
    base = {
        "scenario": {"num_satellites": 1, "num_planes": 1, "duration_s": 2.0},
        "control_plane": {"enabled": False},
    }
    for k, v in over.items():
        base.setdefault(k, {}).update(v)
    return make_cfg(base)


def test_snapshot_has_complete_structure_and_version_after_run():
    geo = StaticGeometry(1, neighbors_map={0: {}},
                         visible=lambda *_: True, gsl_changes=[])
    k = kernel.Kernel(_cfg(), [row(1, 0.0, A, B)], geometry=geo)
    snap0 = k.snapshot_global()
    assert snap0["state_version"] == 0
    res = k.run()
    assert res["natural_end"]
    snap = k.snapshot_global()
    for key in ("now", "state_version", "topology", "slots", "access_wait",
                "access_last_busy", "endpoints", "pending", "uplinks",
                "downlinks", "isl_links", "in_flight", "caches"):
        assert key in snap, f"snapshot missing {key}"
    assert snap["state_version"] > 0
    assert snap["in_flight"] == {}  # run finished: no packets propagating
    assert snap["now"] == pytest.approx(2.0)


def test_snapshot_versions_strictly_increase_across_events():
    geo = StaticGeometry(1, neighbors_map={0: {}},
                         visible=lambda *_: True, gsl_changes=[])
    sink = []
    k = kernel.Kernel(_cfg(), [row(1, 0.0, A, B)], geometry=geo,
                      decision_sink=sink)
    res = k.run()
    assert res["natural_end"]
    assert len(sink) >= 1
    versions = [rec["state_version"] for rec in sink]
    assert all(v < w for v, w in zip(versions, versions[1:]))


def test_snapshot_in_flight_tracks_propagating_packets():
    # 1 sat, no ISL: run to a natural end and verify the tracker drains
    geo = StaticGeometry(1, neighbors_map={0: {}},
                         visible=lambda *_: True, gsl_changes=[])
    k = kernel.Kernel(_cfg(), [row(1, 0.0, A, B)], geometry=geo)
    res = k.run()
    assert res["natural_end"]
    assert k._in_flight == {}
