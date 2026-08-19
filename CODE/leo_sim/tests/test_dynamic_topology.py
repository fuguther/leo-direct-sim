"""Direct coverage for D2 dynamic topology rematch semantics.

Complements the indirect routing/holding-queue coverage: retired-link
control draining and Q0 state-version staleness on recompute.
"""
from __future__ import annotations

import numpy as np

from CODE.leo_sim import kernel, learning, receipt
from CODE.leo_sim.tests.helpers import StaticGeometry, cell, make_cfg, row


class _DrainGeo(StaticGeometry):
    """Topology rematch decoupled from physical availability.

    The greedy rematch switches 0:E from peer 1 to peer 2 at t=0.5, but the
    physical 0-1 link stays up (as with the real Constellation geometry,
    where availability comes from range, not from the matcher), so the
    retired link can drain its queue naturally.
    """

    def isl_available(self, a, b, t):
        return b in self._nb.get(a, {}).values()


class _LearningRematchGeo(_DrainGeo):
    """Three-satellite rematch with endpoint visibility for one packet."""

    def __init__(self, src_ll, dst_ll, **kwargs):
        super().__init__(**kwargs)
        self._src_ll = src_ll
        self._dst_ll = dst_ll

    def ground_visible(self, sat_id, lat, lon, t):
        if (lat, lon) == self._src_ll:
            return sat_id == 0
        if (lat, lon) == self._dst_ll:
            return (sat_id == 1 and t < 0.5) or (sat_id == 2 and t >= 0.5)
        return False


def _geometry():
    def at(sat, dirs, t):
        if t < 0.5:
            nb = {0: {"E": 1}, 1: {"W": 0}}
        else:
            nb = {0: {"E": 2}, 2: {"W": 0}}
        return {d: n for d, n in nb.get(sat, {}).items() if d in dirs}

    return _DrainGeo(3, neighbors_map={0: {"E": 1}, 1: {"W": 0}},
                     neighbors_at_fn=at)


def _cfg():
    return make_cfg({
        "scenario": {"num_satellites": 3, "num_planes": 1,
                     "duration_s": 1.0},
        "topology": {"recompute_interval_s": 0.5},
    })


def test_retired_isl_drains_queued_control_after_rematch():
    geo = _geometry()
    k = kernel.Kernel(_cfg(), [], geometry=geo)
    old = k.isls[0]["E"]
    cp = kernel.ControlPacket(1, 0, 1, 0.0, 10.0, 1, 8_000, {})
    k.ctrl_ledger.register(cp.iid, cp.bits)
    old.put_ctrl(cp)

    k._recompute_topology(0.5)
    assert old in k._retired_isls
    assert k.isls[0]["E"].peer == 2

    res = k.run()
    assert res["natural_end"]
    # the retired link kept serving its queued control to the OLD peer
    assert not old.ctrl_q
    assert old.ctrl_bits == 0
    assert cp.received_at is not None


def test_recompute_bumps_state_version_and_stales_snapshots():
    geo = _geometry()
    k = kernel.Kernel(_cfg(), [], geometry=geo)
    snap = k.snapshot_global()
    v0 = snap["state_version"]

    k._recompute_topology(0.5)

    assert k._state_version == v0 + 1
    snap2 = k.snapshot_global()
    assert snap2["state_version"] == v0 + 1
    # the rematch is visible in the snapshot content, not just the counter
    assert snap2["topology"] != snap["topology"]


def test_learning_rematch_requeue_discards_open_forward_transition():
    src_ll, dst_ll = (0.0, 0.0), (10.0, 0.0)
    geo = _LearningRematchGeo(
        src_ll, dst_ll, num_satellites=3,
        neighbors_map={0: {"E": 1}, 1: {"W": 0}},
        neighbors_at_fn=lambda s, dirs, t: {
            d: n for d, n in (
                {0: {"E": 1}, 1: {"W": 0}} if t < 0.5
                else {0: {"E": 2}, 2: {"W": 0}}).get(s, {}).items()
            if d in dirs})
    cfg = make_cfg({
        "scenario": {"num_satellites": 3, "num_planes": 1,
                     "duration_s": 1.0},
        "topology": {"recompute_interval_s": 0.5},
        "endpoints": {"sites": [
            {"name": "src", "lat": src_ll[0], "lon": src_ll[1]},
            {"name": "dst", "lat": dst_ll[0], "lon": dst_ll[1]},
        ]},
        "control_plane": {"enabled": True},
        "routing": {"policy": "hop", "learning_enabled": True},
        "learning": {"algorithm": "qlearning"},
    })
    src, dst = cell(*src_ll), cell(*dst_ll)
    k = kernel.Kernel(cfg, [row(1, 0.0, src, dst)], geometry=geo)
    old = k.isls[0]["E"]
    pkt = kernel.DataPacket(999, src, dst, 8_000, None, 0.0)
    # simulate a packet whose forward action was decided but whose ISL
    # service has not started when the rematch retires that link
    pkt.learning_state = np.zeros(learning.CONTRACT_DIMS["C3"])
    pkt.learning_action = "E"
    pkt.learning_reward = None
    k._learning_open.add(pkt)
    old.put_data(pkt)

    k._recompute_topology(0.5)

    assert k.pending[0] == [pkt]
    assert pkt.learning_state is None
    assert pkt.learning_action is None
    assert pkt not in k._learning_open
    assert k.mech["learning_discarded_at_rematch"] == 1

    # decision/transition accounting must make room for an environment abort
    # before receipt verification can reuse the existing stop-time identity
    mc = dict(k.mech)
    mc["learning_decisions"] = 1  # the one queued decision before rematch
    assert receipt._learning_transition_accounting(mc) == []


def test_dynamic_t0_matching_counts_as_effective_without_recompute():
    def at(sat, dirs, t):
        if t < 0.3:
            nb = {0: {"E": 2}, 2: {"W": 0}}
        else:
            nb = {0: {"E": 1}, 1: {"W": 0}}
        return {d: n for d, n in nb.get(sat, {}).items() if d in dirs}

    # the static builder defaults to the 0-1 edge; the dynamic t=0 matching
    # already differs, so no interval recompute is needed for effectiveness
    geo = _DrainGeo(3, neighbors_map={0: {"E": 1}, 1: {"W": 0}},
                    neighbors_at_fn=at)
    k = kernel.Kernel(_cfg(), [], geometry=geo)
    assert k.mech["topo_dynamic_init"] is True
    assert k.mech["topo_recomputes"] == 0
    res = k.run()
    assert res["natural_end"]
    mc = res["mechanism_counters"]
    assert mc["topo_dynamic_init"] is True
    assert mc["topo_recomputes"] == 1
    assert res["mechanisms"]["effective"]["dynamic_topology"] is True
