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


def test_snapshot_gsl_ge_covers_associated_pairs_explicitly():
    """A1 regression: GSL GE pairs must be materialized at association and
    every current endpoint-satellite pair must appear with an explicit
    materialized/bad/next_flip triple (no silent key absence)."""
    geo = StaticGeometry(1, neighbors_map={0: {}},
                         visible=lambda *_: True, gsl_changes=[])
    cfg = _cfg(**{"links": {"ge_enabled": True}})
    k = kernel.Kernel(cfg, [row(1, 0.0, A, B)], geometry=geo)
    res = k.run()
    assert res["natural_end"]
    snap = k.snapshot_global()
    # the single endpoint should be associated with sat 0 during the run
    assert "0:0" in snap["gsl_ge"] or any(
        key.startswith("0:") for key in snap["gsl_ge"])
    for key, ge in snap["gsl_ge"].items():
        assert "materialized" in ge
        assert ge["materialized"] is True
        assert "bad" in ge and "next_flip" in ge


def test_snapshot_unmaterialized_gsl_pair_is_explicit_not_missing():
    """A1 fallback: a current endpoint link whose GE was never materialized
    must show as materialized=False, never as an absent key."""
    geo = StaticGeometry(1, neighbors_map={0: {}},
                         visible=lambda *_: True, gsl_changes=[])
    k = kernel.Kernel(_cfg(), [row(1, 0.0, A, B)], geometry=geo)
    ep = k.endpoints[A]
    # inject a link without going through _associate (which materializes)
    ep.links[0] = kernel.Link(0, "active", 0.0)
    snap = k.snapshot_global()
    assert snap["gsl_ge"][f"0:{A}"] == {
        "materialized": False, "bad": None, "next_flip": None}


def test_snapshot_in_flight_exposes_full_packet_state():
    """A3 regression: _in_flight entries must expose the full current packet
    state (pid/src/dst/bits/deadline/emitted_at/path/assigned_sat), not just
    kind/sat/arrival_at."""
    geo = StaticGeometry(1, neighbors_map={0: {}},
                         visible=lambda *_: True, gsl_changes=[])
    k = kernel.Kernel(_cfg(), [row(1, 0.0, A, B)], geometry=geo)
    pkt = kernel.DataPacket(42, A, B, 1000, 5.0, 0.0)
    pkt.path.append(0)
    pkt.assigned_sat = 0
    k._in_flight[42] = {"kind": "isl", "sat": 0, "arrival_at": 3.0,
                        "pkt": pkt}
    snap = k.snapshot_global()
    entry = snap["in_flight"][42]
    assert entry["kind"] == "isl" and entry["sat"] == 0
    assert entry["arrival_at"] == pytest.approx(3.0)
    assert entry["pid"] == 42
    assert entry["src"] == A and entry["dst"] == B
    assert entry["bits"] == 1000
    assert entry["deadline"] == 5.0
    assert entry["emitted_at"] == 0.0
    assert entry["path"] == [0]
    assert entry["assigned_sat"] == 0


def test_snapshot_service_phase_distinguishes_waiting_from_transmitting():
    """A2 regression: pre-service down-wait must not be reported as consumed
    service time; remaining_service_s is the full duration while waiting and
    non-negative while transmitting."""
    geo = StaticGeometry(1, neighbors_map={0: {}},
                         visible=lambda *_: True, gsl_changes=[])
    k = kernel.Kernel(_cfg(), [row(1, 0.0, A, B)], geometry=geo)
    pkt = kernel.DataPacket(7, A, B, 1000, 5.0, 0.0)
    dl = k.downlinks[0]
    dl.current = pkt
    dl._svc = (0.0, "gsl_downlink_s")
    dl._svc_phase = "waiting_for_link"
    dl._tx_started_at = None
    snap = k.snapshot_global()
    dl_snap = snap["downlinks"][0]
    expected_full = pkt.bits / k.dl_rate_bps
    assert dl_snap["remaining_service_s"] == pytest.approx(expected_full)
    assert dl_snap["svc"]["phase"] == "waiting_for_link"
    assert dl_snap["svc"]["tx_started_at"] is None
    # after real transmission starts, elapsed time is measured from the
    # transmission start, and remaining is never negative by construction
    dl._svc_phase = "transmitting"
    dl._tx_started_at = 0.0
    snap2 = k.snapshot_global()
    dl_snap2 = snap2["downlinks"][0]
    assert dl_snap2["svc"]["phase"] == "transmitting"
    assert dl_snap2["remaining_service_s"] == pytest.approx(expected_full)
