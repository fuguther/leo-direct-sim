from CODE.leo_sim.q0 import JointPlan, PlanAction
from CODE.leo_sim.q0_tiny import TinyPacket, TinyPlan, solve_current_tiny


def test_tiny_dp_finds_two_hop_plan_and_exports_joint_plans():
    packets = (TinyPacket(1, 0, 2, deadline=4),)
    plan = solve_current_tiny(
        packets, {0: (1,), 1: (0, 2), 2: (1,)}, horizon=4)

    assert isinstance(plan, TinyPlan)
    assert plan.score == (1, -3, 0)
    assert plan.actions == (
        PlanAction("forward", 1, 0, direction="N"),
        PlanAction("forward", 1, 1, direction="N"),
        PlanAction("deliver", 1, 2),
    )

    joints = plan.to_joint_plans(version=7)
    assert [p.version for p in joints] == [7, 7, 7]
    assert all(isinstance(p, JointPlan) for p in joints)
    assert joints[0].actions == (plan.actions[0],)


def test_tiny_dp_prioritizes_deadline_delivery_over_shorter_route():
    packets = (
        TinyPacket(1, 0, 2, deadline=2),
        TinyPacket(2, 0, 1, deadline=4),
    )
    plan = solve_current_tiny(
        packets, {0: (1, 2), 1: (0,), 2: (0,)}, horizon=4)

    assert plan.score[0] == 2
    assert {a.packet_id for a in plan.actions if a.kind == "deliver"} == {1, 2}


def test_tiny_plan_rejects_non_integer_horizon_and_invalid_graph():
    packets = (TinyPacket(1, 0, 1, deadline=2),)
    try:
        solve_current_tiny(packets, {0: (1,), 1: (0,)}, horizon=1.5)
    except ValueError as exc:
        assert "horizon" in str(exc)
    else:
        raise AssertionError("non-integer horizon must fail closed")

    try:
        solve_current_tiny(packets, {0: (2,), 1: ()}, horizon=2)
    except ValueError as exc:
        assert "adjacency" in str(exc)
    else:
        raise AssertionError("invalid adjacency must fail closed")


def test_tiny_optimum_uses_earliest_legal_transitions():
    packets = (TinyPacket(1, 0, 1, deadline=3),)
    plan = solve_current_tiny(
        packets, {0: (1,), 1: (0,)}, horizon=3)

    assert plan.score == (1, -2, 0)
    assert plan.actions[0].kind == "forward"
    assert plan.action_times == (0, 1)
