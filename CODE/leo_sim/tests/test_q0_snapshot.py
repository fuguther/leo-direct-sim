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


def test_snapshot_handles_control_packet_in_service():
    """Regression: ISL in-service control packets must not crash the
    snapshot (ControlPacket has no pid; it is identified by iid)."""
    # 2-sat line with the control plane advertising over the ISL; a slow ISL
    # keeps a control packet in service so the snapshot must read it
    nb = {0: {"E": 1}, 1: {"W": 0}}
    vis = lambda s, lat, lon, t: (s == 0 and (lat, lon) == (0.0, 0.0)) or \
        (s == 1 and (lat, lon) == (0.0, 10.0))
    geo = StaticGeometry(2, neighbors_map=nb, visible=vis)
    cfg = make_cfg({
        "scenario": {"num_satellites": 2, "num_planes": 1, "duration_s": 1.0},
        "links": {"isl_rate_mbps": 0.008},  # 8 kbit control = 1 s service
        "control_plane": {"enabled": True, "advertise_interval_s": 1.0,
                          "packet_bits": 8_000},
        "routing": {"policy": "hop"},
    })
    k = kernel.Kernel(cfg, [], geometry=geo)
    res = k.run()
    assert res["natural_end"]
    snap = k.snapshot_global()  # must not raise on control in-service data
    assert "isl_links" in snap
