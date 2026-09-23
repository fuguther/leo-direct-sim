"""Fold decision snapshots and timeline milestones into per-decision ledgers.

Output-only post-processing for T1 (stale-neighbour-state / candidate-arrival
alignment).  It reads the two optional sinks produced by kernel.Kernel
(decision_sink rows and timeline_sink milestones) and rebuilds, for every
decision, the time chain the T1 measurement contract requires.  Nothing here
influences simulation behaviour: it is a pure function over recorded rows.

See ANALYSIS/T1-MEASUREMENT-PROTOCOL.md for the gate this serves
(T1-TIME-LEDGER-PASS).

Missing values are reported as MISSING rather than 0 so that "the milestone
never happened" can never be confused with "it happened at t=0".
t_measure, t_decision_start and t_decision_commit are equal until
T1-COMPUTE-DELAY-PASS lands, but they are kept as three distinct fields so that
gate can fill them in without changing the schema.
"""
from __future__ import annotations

MISSING = "missing"

#: The eleven fields required by the T1 time-ledger gate, in lifecycle order.
TIMELINE_FIELDS = (
    "t_measure",
    "t_control_rx",
    "t_decision_start",
    "t_decision_commit",
    "t_local_queue_enter",
    "t_service_start",
    "t_service_finish",
    "t_peer_arrival",
    "t_peer_redecision",
    "t_peer_target_egress_enter",
    "t_peer_target_egress_service_start",
)


def _first_at(milestones, milestone, decision_id):
    rows = milestones.get((milestone, decision_id))
    return float(rows[0]["at"]) if rows else MISSING


def _freshest_control_rx(row):
    """Newest control-cache arrival that could have informed this decision.

    The audit blob carries one entry per contributing origin, so a single
    scalar would be lossy.  The freshest value is reported here (the best the
    decision could have known) while the full per-origin detail stays in the
    decision row's info_audit.cache_entries.  Returns MISSING when the contract
    contributed no entry at all (for example a non-learning run).
    """
    audit = row.get("info_audit") or {}
    entries = audit.get("cache_entries") or {}
    arrivals = [float(e["received_at"]) for e in entries.values()
                if e.get("received_at") is not None]
    return max(arrivals) if arrivals else MISSING


def build_ledger(decision_rows, timeline_rows):
    """Rebuild the per-decision time ledger.

    decision_rows are the rows appended to Kernel.decision_sink; timeline_rows
    are the milestones appended to Kernel.timeline_sink.  Returns
    (by_decision, diagnostics): by_decision maps decision_id to a dict holding
    every TIMELINE_FIELDS key plus pid, sat, kind and chosen.
    """
    milestones = {}
    redecision_of = {}
    for row in timeline_rows:
        decision_id = row.get("decision_id")
        if decision_id is None:
            continue
        milestones.setdefault((row["milestone"], decision_id), []).append(row)
        if row["milestone"] == "redecision":
            previous = row.get("prev_decision_id")
            if previous is not None and previous not in redecision_of:
                redecision_of[previous] = decision_id

    by_decision = {}
    duplicates = []
    for row in decision_rows:
        decision_id = row.get("decision_id")
        if decision_id is None:
            continue
        if decision_id in by_decision:
            duplicates.append(decision_id)
            continue
        committed = float(row["t"])
        # The three instants are kept as distinct fields on purpose.  With the
        # default zero compute delay they coincide.  With a non-zero delay the
        # decision body re-reads the state when the computation lands, so
        # t_measure (what the choice was actually based on) coincides with
        # t_decision_commit while t_decision_start precedes both --
        # the interval between them is the computation latency.
        started = float(row.get("t_decision_start", committed))
        by_decision[decision_id] = {
            "pid": row.get("pid"),
            "sat": row.get("sat"),
            "kind": row.get("kind"),
            "chosen": row.get("chosen"),
            "t_measure": committed,
            "t_control_rx": _freshest_control_rx(row),
            "t_decision_start": started,
            "t_decision_commit": committed,
            "t_local_queue_enter": _first_at(milestones, "queue_enter",
                                             decision_id),
            "t_service_start": _first_at(milestones, "service_start",
                                         decision_id),
            "t_service_finish": _first_at(milestones, "service_finish",
                                          decision_id),
            "t_peer_arrival": _first_at(milestones, "peer_arrival",
                                        decision_id),
            "t_peer_redecision": MISSING,
            "t_peer_target_egress_enter": MISSING,
            "t_peer_target_egress_service_start": MISSING,
            "_successor": redecision_of.get(decision_id),
        }

    # Second pass: from the predecessor's point of view, the successor's local
    # enqueue and service start ARE the peer-side target egress milestones.
    for entry in by_decision.values():
        successor = entry.pop("_successor", None)
        if successor is None or successor not in by_decision:
            continue
        nxt = by_decision[successor]
        entry["t_peer_redecision"] = float(nxt["t_measure"])
        entry["t_peer_target_egress_enter"] = nxt["t_local_queue_enter"]
        entry["t_peer_target_egress_service_start"] = nxt["t_service_start"]

    diagnostics = {
        "decisions": len(by_decision),
        "duplicate_decision_ids": sorted(duplicates),
        "orphan_redecisions": sorted(previous for previous in redecision_of
                                     if previous not in by_decision),
        "milestones": len(timeline_rows),
    }
    return by_decision, diagnostics


def score_downstream_predictions(decision_rows, timeline_rows):
    """Score each forward decision's downstream prediction against reality.

    Pairs the decision-time belief recorded in
    info_audit.candidate_truth[chosen].downstream (what the decision expected
    the neighbour's contended egress to be) with the egress snapshot taken
    when the packet ACTUALLY arrived at that neighbour, plus the direction the
    neighbour then really chose.  The gap between the two is the
    stale-neighbour-state misalignment T1 studies.

    Returns (scores, summary); scores maps decision_id to a dict.
    """
    arrivals = {}
    successor = {}
    for row in timeline_rows:
        if row.get("egress_snapshot") is not None:
            arrivals[row.get("decision_id")] = row
        if row["milestone"] == "redecision":
            previous = row.get("prev_decision_id")
            if previous is not None and previous not in successor:
                successor[previous] = row.get("decision_id")

    by_id = {}
    for row in decision_rows:
        if row.get("decision_id") is not None:
            by_id[row["decision_id"]] = row

    scores = {}
    for decision_id, row in sorted(by_id.items()):
        if row.get("kind") != "forward":
            continue
        truth = (row.get("info_audit") or {}).get("candidate_truth") or {}
        entry = truth.get(row.get("chosen"))
        prediction = (entry or {}).get("downstream")
        arrival = arrivals.get(decision_id)
        succ = successor.get(decision_id)
        realized_direction = None
        if succ is not None and succ in by_id:
            realized_direction = by_id[succ].get("chosen")

        predicted_direction = None
        predicted_bits = None
        predicted_remaining = None
        if prediction is not None:
            predicted_direction = prediction.get("peer_egress_direction")
            predicted_bits = (prediction.get("peer_egress_data_bits", 0)
                              + prediction.get("peer_egress_ctrl_bits", 0))
            predicted_remaining = prediction.get("peer_in_service_remaining_bits")

        realized_bits = None
        realized_remaining = None
        realized_actual_bits = None
        if arrival is not None:
            snapshot = arrival.get("egress_snapshot") or {}
            if predicted_direction is not None:
                slot = snapshot.get(predicted_direction)
                if slot is not None:
                    realized_bits = slot["data_bits"] + slot["ctrl_bits"]
                    realized_remaining = slot["in_service_remaining_bits"]
            if realized_direction is not None:
                slot = snapshot.get(realized_direction)
                if slot is not None:
                    realized_actual_bits = slot["data_bits"] + slot["ctrl_bits"]

        match = None
        if predicted_direction is not None and realized_direction is not None:
            match = predicted_direction == realized_direction

        scores[decision_id] = {
            "pid": row.get("pid"),
            "sat": row.get("sat"),
            "predicted_egress": predicted_direction,
            "realized_egress": realized_direction,
            "egress_match": match,
            "arrival_recorded": arrival is not None,
            "predicted_egress_bits": predicted_bits,
            "realized_egress_bits": realized_bits,
            "egress_bits_delta": (None if (predicted_bits is None
                                           or realized_bits is None)
                                  else realized_bits - predicted_bits),
            "realized_actual_egress_bits": realized_actual_bits,
            "predicted_remaining_bits": predicted_remaining,
            "realized_remaining_bits": realized_remaining,
            "remaining_delta": (None if (predicted_remaining is None
                                         or realized_remaining is None)
                                else realized_remaining - predicted_remaining),
        }

    compared = [s for s in scores.values() if s["egress_match"] is not None]
    deltas = [s["egress_bits_delta"] for s in scores.values()
              if s["egress_bits_delta"] is not None]
    summary = {
        "scored_decisions": len(scores),
        "with_prediction": sum(1 for s in scores.values()
                               if s["predicted_egress"] is not None),
        "with_arrival_snapshot": sum(1 for s in scores.values()
                                     if s["arrival_recorded"]),
        "egress_compared": len(compared),
        "egress_matched": sum(1 for s in compared if s["egress_match"]),
        "egress_match_rate": ((sum(1 for s in compared if s["egress_match"])
                               / len(compared)) if compared else None),
        "egress_bits_delta_samples": len(deltas),
        "egress_bits_delta_mean": (sum(deltas) / len(deltas)) if deltas else None,
        "egress_bits_delta_max": max(deltas) if deltas else None,
    }
    return scores, summary


def audit_ledger(by_decision):
    """Report which of the eleven fields are still MISSING, per decision."""
    gaps = {}
    for decision_id, entry in sorted(by_decision.items()):
        missing = [field for field in TIMELINE_FIELDS
                   if entry.get(field) == MISSING]
        if missing:
            gaps[decision_id] = missing
    return gaps
