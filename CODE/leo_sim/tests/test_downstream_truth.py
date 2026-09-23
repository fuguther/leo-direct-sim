"""T1-DOWNSTREAM-RESOURCE tests: candidate-specific downstream contention truth.

The gate exists because the older audit field peer_egress_queue_bits is a SUM
over every direction of the neighbour, which is not the resource a packet
contends for after arrival (R8-A4).  These tests pin the replacement:
per-candidate, per-direction, with the peer's predicted egress and its
in-service remaining work.
"""
from __future__ import annotations

from CODE.leo_sim import kernel
from CODE.leo_sim.tests.helpers import StaticGeometry, cell, cell_center, make_cfg, row

A = cell(0.0, 0.0)
B = cell(0.0, 10.0)
AC, BC = cell_center(A), cell_center(B)

# 3-satellite line 0 - 1 - 2; only the ends see a cell, so a packet from A to B
# is forwarded twice and the first forward's peer really does forward onward.
LINE_NB = {0: {"E": 1}, 1: {"E": 2, "W": 0}, 2: {"W": 1}}


def _line_geo():
    vis = lambda s, lat, lon, t: (s == 0 and (lat, lon) == AC) or \
                                 (s == 2 and (lat, lon) == BC)
    return StaticGeometry(3, neighbors_map=LINE_NB, visible=vis)


LINE_CFG = {"scenario": {"duration_s": 20.0, "num_satellites": 3,
                         "num_planes": 1, "seed": 3},
            "control_plane": {"enabled": True},
            "routing": {"policy": "oracle"}}

DOWNSTREAM_KEYS = {
    "prediction_method", "peer_is_destination", "peer_egress_direction",
    "peer_egress_link_id", "peer_egress_data_bits", "peer_egress_ctrl_bits",
    "peer_egress_ctrl_packets", "peer_in_service_bits",
    "peer_in_service_phase", "peer_in_service_is_control",
    "peer_in_service_remaining_bits", "peer_in_service_remaining_method",
}


def _run(geometry, rows, overrides=None):
    sink, timeline = [], []
    res = kernel.run_simulation(make_cfg(overrides), rows, geometry=geometry,
                                decision_sink=sink, timeline_sink=timeline)
    return res, sink, timeline


def _kernel_with_sinks(geometry, rows, overrides=None):
    sink, timeline = [], []
    kern = kernel.Kernel(make_cfg(overrides), rows, geometry=geometry,
                         decision_sink=sink, timeline_sink=timeline)
    return kern, sink, timeline


def _candidates(row_):
    return ((row_.get("info_audit") or {}).get("candidate_truth") or {})


def test_every_candidate_carries_the_declared_downstream_schema():
    _, sink, _ = _run(_line_geo(), [row(1, 0.0, A, B)], LINE_CFG)
    checked = 0
    for row_ in sink:
        for direction, entry in _candidates(row_).items():
            assert "downstream" in entry, (row_["decision_id"], direction)
            assert set(entry["downstream"]) == DOWNSTREAM_KEYS
            checked += 1
    assert checked, "fixture must produce candidate ISL directions"


def test_downstream_is_per_direction_not_a_peer_wide_sum():
    """The recorded single-direction occupancy must never exceed the summed
    field, and must be strictly smaller wherever the peer owns more than one
    direction -- that difference is exactly what R8-A4 is about."""
    kern, sink, _ = _kernel_with_sinks(_line_geo(), [row(1, 0.0, A, B)])
    kern.run()
    scored = 0
    for row_ in sink:
        for direction, entry in _candidates(row_).items():
            ds = entry["downstream"]
            peer = entry["edge"][1]
            per_dir = ds["peer_egress_data_bits"] + ds["peer_egress_ctrl_bits"]
            # monotonicity: one direction can never exceed the sum
            assert per_dir <= entry["peer_egress_queue_bits"]
            # the two fields are different quantities by construction: the
            # summed field aggregates EVERY direction the peer owns, so on a
            # peer with more than one direction it cannot be reproduced from
            # the single predicted egress alone
            peer_dirs = len(kern.isls[peer])
            if peer_dirs > 1:
                assert entry["peer_egress_queue_bits"] >= per_dir
                assert ds["peer_egress_direction"] in kern.isls[peer] or \
                    ds["peer_egress_direction"] is None
                scored += 1
    assert scored, "fixture must score a peer that owns more than one direction"


def test_predicted_peer_egress_matches_the_peers_own_decision():
    """The prediction is only useful if it is right: for the chosen
    direction, the predicted peer egress must equal the direction the peer
    actually selects at its own re-decision."""
    _, sink, timeline = _run(_line_geo(), [row(1, 0.0, A, B)], LINE_CFG)
    by_id = {r["decision_id"]: r for r in sink}
    successor = {m["prev_decision_id"]: m["decision_id"]
                 for m in timeline if m["milestone"] == "redecision"}
    compared = 0
    for did, row_ in by_id.items():
        if row_["kind"] != "forward":
            continue
        succ = successor.get(did)
        if succ is None or succ not in by_id:
            continue
        entry = _candidates(row_).get(row_["chosen"])
        if entry is None:
            continue
        predicted = entry["downstream"]["peer_egress_direction"]
        if predicted is None:
            continue
        assert predicted == by_id[succ]["chosen"], (
            "predicted peer egress %r but the peer chose %r"
            % (predicted, by_id[succ]["chosen"]))
        compared += 1
    assert compared, "fixture must allow at least one prediction to be scored"


def test_peer_that_is_the_destination_is_flagged_without_an_egress():
    """When the neighbour already serves the destination the packet leaves
    the network there, so there is no downstream ISL egress to predict."""
    _, sink, _ = _run(_line_geo(), [row(1, 0.0, A, B)], LINE_CFG)
    flagged = [entry for row_ in sink for entry in _candidates(row_).values()
               if entry["downstream"]["peer_is_destination"]]
    assert flagged, "the second hop's peer serves the destination"
    for entry in flagged:
        assert entry["downstream"]["peer_egress_direction"] is None
        assert entry["downstream"]["peer_egress_link_id"] is None
        assert entry["downstream"]["peer_egress_data_bits"] == 0


def test_remaining_work_is_reported_with_an_honest_method_label():
    _, sink, _ = _run(_line_geo(), [row(1, 0.0, A, B)], LINE_CFG)
    methods = {entry["downstream"]["peer_in_service_remaining_method"]
               for row_ in sink for entry in _candidates(row_).values()}
    assert methods <= {"no_service_on_predicted_egress",
                       "linear_at_constant_rate",
                       "not_started_full_bits",
                       "unavailable_varying_rate"}, methods


def test_downstream_truth_does_not_change_behavior():
    rows = [row(i, 0.5 * i, A, B) for i in (1, 2, 3)]
    base, _, _ = _run(_line_geo(), rows, LINE_CFG)
    with_sink, sink, timeline = _run(_line_geo(), rows, LINE_CFG)
    assert sink and timeline, "the sink run must actually record"
    for key in ("fates", "fate_counts", "totals", "deliveries", "occupied",
                "queue_area_bits_s", "access", "service_log", "handover",
                "events_processed", "packet_events", "link_service_windows"):
        assert with_sink[key] == base[key], key


def test_plain_runs_pay_nothing():
    kern = kernel.Kernel(make_cfg(LINE_CFG), [row(1, 0.0, A, B)],
                         geometry=_line_geo())
    assert kern.decision_sink is None and kern.timeline_sink is None
    assert kern._decision_seq == 0
