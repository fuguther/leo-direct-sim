import pytest

from CODE.leo_sim import kernel
from CODE.leo_sim.q0 import JointPlan, PlanAction, PlanError, validate_plan_version
from CODE.leo_sim.tests.helpers import StaticGeometry, cell, make_cfg, row


def test_plan_is_immutable_and_version_bound():
    action = PlanAction("forward", packet_id=1, sat=0, direction="E")
    plan = JointPlan(version=4, actions=(action,))
    assert validate_plan_version(plan, 4) == (True, ())
    assert validate_plan_version(plan, 5)[0] is False
    with pytest.raises((AttributeError, TypeError)):
        plan.version = 5


def test_plan_rejects_unknown_or_malformed_actions():
    with pytest.raises(PlanError):
        PlanAction("teleport", packet_id=1, sat=0)  # type: ignore[arg-type]
    with pytest.raises(PlanError):
        PlanAction("forward", packet_id=1, sat=0, direction="X")
    with pytest.raises(PlanError):
        PlanAction("wait", packet_id=1, sat=0, until=None)


def test_plan_rejects_duplicate_packets_and_mutable_actions():
    a = PlanAction("deliver", packet_id=1, sat=0)
    with pytest.raises(PlanError):
        JointPlan(version=0, actions=(a, a))
    with pytest.raises(PlanError):
        JointPlan(version=0, actions=[a])  # type: ignore[arg-type]


def test_kernel_plan_validation_is_versioned_and_fail_closed():
    geo = StaticGeometry(2, neighbors_map={0: {"E": 1}, 1: {"W": 0}})
    cfg = make_cfg({"scenario": {"num_satellites": 2, "num_planes": 1}})
    src, dst = cell(0.0, 0.0), cell(0.0, 10.0)
    k = kernel.Kernel(cfg, [row(1, 0.0, src, dst)], geometry=geo)
    pkt = kernel.DataPacket(1, src, dst, 8_000, None, 0.0)
    k.pending[0].append(pkt)
    valid = JointPlan(0, (PlanAction("forward", 1, 0, direction="E"),))
    assert k.validate_joint_plan(valid) == (True, ())
    stale = JointPlan(1, valid.actions)
    assert k.validate_joint_plan(stale)[0] is False
    bad_dir = JointPlan(0, (PlanAction("forward", 1, 0, direction="N"),))
    assert k.validate_joint_plan(bad_dir)[0] is False
    k._in_flight[1] = {"kind": "isl", "sat": 1, "arrival_at": 1.0, "pkt": pkt}
    assert k.validate_joint_plan(valid)[0] is False
