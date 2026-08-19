"""Direct coverage for D2 dynamic topology rematch semantics.

Complements the indirect routing/holding-queue coverage: retired-link
control draining and Q0 state-version staleness on recompute.
"""
from __future__ import annotations

from CODE.leo_sim import kernel
from CODE.leo_sim.tests.helpers import StaticGeometry, make_cfg


class _DrainGeo(StaticGeometry):
    """Topology rematch decoupled from physical availability.

    The greedy rematch switches 0:E from peer 1 to peer 2 at t=0.5, but the
    physical 0-1 link stays up (as with the real Constellation geometry,
    where availability comes from range, not from the matcher), so the
    retired link can drain its queue naturally.
    """

    def isl_available(self, a, b, t):
        return b in self._nb.get(a, {}).values()


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
