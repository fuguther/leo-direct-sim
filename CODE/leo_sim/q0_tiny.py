"""Deterministic current-information Q0 tiny reference solver.

This is a correctness anchor, not a scalable optimizer.  It models a small
discrete-time packet network with unit service per slot, fixed bidirectional
adjacency, no future arrivals, no outages, and no topology changes.  The
solver enumerates the finite state space with memoized dynamic programming and
exports only the existing immutable ``JointPlan`` contract.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from .q0 import JointPlan, PlanAction


@dataclass(frozen=True)
class TinyPacket:
    packet_id: int
    source: int
    destination: int
    deadline: int

    def __post_init__(self):
        if self.packet_id < 0 or self.source < 0 or self.destination < 0:
            raise ValueError("packet identifiers and nodes must be >= 0")
        if self.deadline < 0:
            raise ValueError("deadline must be >= 0")


@dataclass(frozen=True)
class TinyPlan:
    score: tuple[int, int, int]
    actions: tuple[PlanAction, ...]
    action_times: tuple[int, ...]

    def to_joint_plans(self, version: int) -> tuple[JointPlan, ...]:
        """Export one atomic plan per action time, preserving action order."""
        if len(self.actions) != len(self.action_times):
            raise ValueError("actions and action_times length mismatch")
        out = []
        for time in sorted(set(self.action_times)):
            actions = tuple(a for a, t in zip(self.actions, self.action_times)
                            if t == time)
            out.append(JointPlan(version=version, actions=actions))
        return tuple(out)


def _direction(src: int, dst: int) -> str:
    # Tiny graphs are numbered; the wire contract still needs a legal
    # direction.  N is the canonical synthetic direction for a forward edge.
    if src == dst:
        raise ValueError("self edge is not a forward action")
    return "N"


def solve_current_tiny(packets: tuple[TinyPacket, ...], adjacency: dict[int, tuple[int, ...]],
                       horizon: int) -> TinyPlan:
    """Solve the bounded current-information tiny model exactly.

    ``score`` is ``(on-time deliveries, -sum completion times,
    -wait-slots)``.  Since all transitions and the horizon are finite, the
    memoized recursion is an exact Bellman solution for this model.
    """
    if not isinstance(horizon, int) or isinstance(horizon, bool) or horizon < 0:
        raise ValueError("horizon must be a non-negative integer")
    if not packets:
        return TinyPlan((0, 0, 0), (), ())
    ids = [p.packet_id for p in packets]
    if len(set(ids)) != len(ids):
        raise ValueError("packet ids must be unique")
    nodes = set(adjacency)
    for src, peers in adjacency.items():
        for peer in peers:
            if peer == src or peer not in nodes or src not in adjacency.get(peer, ()):
                raise ValueError("adjacency must be finite, non-self, and bidirectional")
    index = {p.packet_id: i for i, p in enumerate(packets)}
    start = tuple(p.source for p in packets)
    done = tuple(-1 for _ in packets)

    def terminal_score(completion):
        timely = sum(t >= 0 and t <= p.deadline for p, t in zip(packets, completion))
        total_delay = sum(t for t in completion if t >= 0)
        return timely, -total_delay

    @lru_cache(maxsize=None)
    def best(time: int, positions: tuple[int, ...], completion: tuple[int, ...]):
        if time >= horizon or all(t >= 0 for t in completion):
            return terminal_score(completion) + (0,), ()
        candidates = [(time + 1, positions, completion, None)]
        for i, pkt in enumerate(packets):
            if completion[i] >= 0:
                continue
            src = positions[i]
            for peer in adjacency.get(src, ()):
                next_pos = list(positions)
                next_pos[i] = peer
                next_completion = list(completion)
                action = PlanAction("forward", pkt.packet_id, src,
                                    direction=_direction(src, peer))
                candidates.append((time + 1, tuple(next_pos), completion,
                                   (action, time)))
            if src == pkt.destination:
                next_completion = list(completion)
                next_completion[i] = time + 1
                action = PlanAction("deliver", pkt.packet_id, src)
                candidates.append((time + 1, positions, tuple(next_completion),
                                   (action, time)))

        best_value = None
        best_path = ()
        for next_time, next_pos, next_completion, action in candidates:
            value, path = best(next_time, next_pos, next_completion)
            waits = value[2] - (1 if action is None else 0)
            value = (value[0], value[1], -waits)
            if best_value is None or value > best_value:
                best_value = value
                best_path = (() if action is None else (action,)) + path
        return best_value, best_path

    score, path = best(0, start, done)
    actions = tuple(a for a, _time in path)
    action_times = tuple(time for _action, time in path)
    return TinyPlan(score, actions, action_times)
