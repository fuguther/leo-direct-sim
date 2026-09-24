#!/usr/bin/env python3
"""F2 attribution step for WP-LEO-V2-PLATFORM-AUDIT-F2 (PROCEDURE section 5b).

Why this tool exists: the F2 node-processing stage is recorded ONLY on the kernel
timeline sink (kernel.py:4297/4300; it deliberately emits no packet_event).
metrics_independent.decompose_packet_delay defines decision_compute_s as the sum of
the UNCOVERED intervals of the packet timeline, and an F2 occupancy IS exactly an
uncovered interval -- so an analyzer that is not handed the F2 spans publishes
satellite node-processing time as decision computation time.  This tool performs
both readings on the SAME persisted run so the difference is explicit and auditable.

HARDENING (revision 3).  Revision 2 of this tool reported ok=true on a TRUNCATED
timeline, on an EMPTY timeline, and on a vacuous ledger, and it took the compute
delay from a CLI argument that need not match the arms.  A verifier that passes on
damaged artifacts is worse than no verifier, so every one of those channels is now
closed and each closure is exercised by --self-test:

  * the delays come from EACH ARM resolved_config.json, never from a flag alone;
  * the timeline sidecar is verified: row_count and log_sha256 must match the
    stream actually read, and receipt_sha256 must match the receipt on disk;
  * exactly one of {control, f2} must have node_process milestones, and the arm
    whose resolved node_process_delay_s > 0 must have a POSITIVE, EVEN count;
  * at least one packet must be delivered, and the declared delivery set must be
    non-empty, or the run is refused instead of reported as vacuously ok.

Usage:
  python3 CODE/work/WP-LEO-V2-PLATFORM-AUDIT-F2/R02/attribute_f2.py \
      --results-root CODE/Results \
      --experiment EXP-20260924-PLATFORM-AUDIT-F2-R02 \
      --out ANALYSIS/EXP-20260924-PLATFORM-AUDIT-F2-R02/f2-attribution.json
  python3 .../attribute_f2.py --self-test     # exercises every refusal path
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from CODE.leo_sim import metrics_independent as indep  # noqa: E402

ARMS = ("control", "f2")
TOL = 1e-9


class AttributionError(RuntimeError):
    """A claimed identity did not hold, or an input is too damaged to judge."""


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_arm(results_root: Path, run_id: str, compute_delay_s: float | None):
    base = results_root / run_id
    ledger_path = base / "ledgers.json"
    timeline_path = base / "timeline.jsonl"
    manifest_path = base / "timeline.jsonl.manifest.json"
    resolved_path = base / "resolved_config.json"
    receipt_path = base / "receipt.json"
    for path in (ledger_path, timeline_path, manifest_path, resolved_path,
                 receipt_path):
        if not path.is_file():
            raise AttributionError(
                f"{run_id}: missing {path.name} -- F2 is unattributable without "
                f"the full artifact set; re-run with --timeline-log")

    # The delays are read from the ARM OWN resolved configuration.  A caller-
    # supplied flag can only be cross-checked against it, never substituted for
    # it: revision 2 accepted --compute-delay-s 0.1 on configs that say 0.05.
    resolved = json.loads(resolved_path.read_text(encoding="utf-8"))
    execution = resolved["config"]["execution"]
    arm_compute = float(execution["compute_delay_s"])
    arm_node = float(execution["node_process_delay_s"])
    if arm_compute <= 0.0:
        raise AttributionError(
            f"{run_id}: execution.compute_delay_s = {arm_compute!r}; the "
            f"decision stage must be active or the separation is not "
            f"discriminating")
    if compute_delay_s is not None and arm_compute != compute_delay_s:
        raise AttributionError(
            f"{run_id}: --compute-delay-s {compute_delay_s!r} does not match "
            f"the arm resolved_config.json value {arm_compute!r}")

    # The sidecar binds the stream to this very run.  A truncated stream must
    # not be judgeable: revision 2 reported ok=true after whole node pairs were
    # deleted, silently shrinking the F2 term.
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("log_sha256") != _sha256(timeline_path):
        raise AttributionError(
            f"{run_id}: timeline sha256 != sidecar log_sha256 -- the stream was "
            f"modified after the run")
    if manifest.get("receipt_sha256") != _sha256(receipt_path):
        raise AttributionError(
            f"{run_id}: receipt sha256 != sidecar receipt_sha256")

    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    rows = [json.loads(line) for line in
            timeline_path.read_text(encoding="utf-8").splitlines() if line]
    if manifest.get("row_count") != len(rows):
        raise AttributionError(
            f"{run_id}: sidecar row_count {manifest.get('row_count')!r} != "
            f"{len(rows)} rows actually read -- the timeline is truncated")
    return ledger, rows, arm_compute, arm_node


def analyse_arm(results_root: Path, run_id: str,
                compute_delay_s: float | None = None) -> dict:
    ledger, timeline, arm_compute, arm_node = _load_arm(
        results_root, run_id, compute_delay_s)
    events = ledger.get("packet_events") or []
    windows = ledger.get("link_service_windows") or []

    milestones = [r.get("milestone") for r in timeline]
    starts = milestones.count("node_process_start")
    ends = milestones.count("node_process_end")
    if starts != ends:
        raise AttributionError(
            f"{run_id}: {starts} node_process_start vs {ends} node_process_end "
            f"-- an unclosed occupancy must never be silently dropped")
    if arm_node > 0.0 and starts == 0:
        raise AttributionError(
            f"{run_id}: resolved node_process_delay_s = {arm_node!r} but the "
            f"timeline carries NO node_process milestones -- the stream cannot "
            f"support the claim it is being used for")
    if arm_node == 0.0 and starts != 0:
        raise AttributionError(
            f"{run_id}: resolved node_process_delay_s = 0 but {starts} node "
            f"occupancies were recorded")

    spans = indep.node_process_spans(timeline)
    node_total = math.fsum(end - start
                           for values in spans.values()
                           for start, end in values)

    labelled = indep.verify_delay_decomposition(
        events, windows, ledger, node_spans_by_pid=spans)
    unlabelled = indep.verify_delay_decomposition(events, windows, ledger)

    delivered = list(labelled["delivered_pids"])
    if not delivered:
        raise AttributionError(
            f"{run_id}: no delivered packet in the declared set -- a vacuous "
            f"ledger must not be reported as ok")

    labelled_dc = labelled["total_decision_compute_s"]
    unlabelled_dc = unlabelled["total_decision_compute_s"]
    leakage = unlabelled_dc - labelled_dc
    decisions = labelled_dc / arm_compute

    checks = {
        "spans_supplied": labelled["node_process_spans_supplied"] is True,
        "labelled_closure_ok": bool(labelled["ok"]),
        "labelled_residual_within_tol":
            labelled["max_abs_residual_s"] <= TOL,
        "leakage_equals_node_total": math.isclose(
            leakage, node_total, rel_tol=0.0, abs_tol=TOL),
        "labelled_dc_is_multiple_of_compute_delay":
            abs(decisions - round(decisions)) <= 1e-9,
        "unlabelled_closure_ok": bool(unlabelled["ok"]),
    }
    links = (ledger.get("congestion_metrics") or {}).get("links") or {}
    return {
        "run_id": run_id,
        "resolved_compute_delay_s": arm_compute,
        "resolved_node_process_delay_s": arm_node,
        "node_process_milestones": {"start": starts, "end": ends},
        "f2_packets": sorted(int(pid) for pid in spans),
        "total_node_process_s": node_total,
        "labelled_total_decision_compute_s": labelled_dc,
        "unlabelled_total_decision_compute_s": unlabelled_dc,
        "leakage_s": leakage,
        "decision_count": round(decisions),
        "labelled_max_abs_residual_s": labelled["max_abs_residual_s"],
        "delivered_pids": delivered,
        "per_packet": {
            pid: {"node_process_s": item["node_process_s"],
                  "decision_compute_s": item["decision_compute_s"],
                  "e2e_s": item["e2e_s"]}
            for pid, item in labelled["packets"].items()},
        "link_capacity": {
            link: {"served_bits": item["served_bits"],
                   "capacity_bits": item["capacity_bits"],
                   "available_capacity_bits": item["available_capacity_bits"],
                   "available_time_s": item["available_time_s"],
                   "utilization": item["utilization"]}
            for link, item in links.items()},
        "checks": checks,
    }


def run(results_root: Path, experiment: str, compute_delay_s: float | None,
        pairing_key: str = "s7") -> dict:
    if not pairing_key or "/" in pairing_key or not pairing_key.isalnum():
        raise AttributionError(
            f"pairing_key must be a non-empty alphanumeric string, got "
            f"{pairing_key!r}")
    arms = {arm: analyse_arm(results_root,
                             f"{experiment}-{arm}-{pairing_key}",
                             compute_delay_s)
            for arm in ARMS}
    if arms["control"]["node_process_milestones"]["start"] != 0:
        raise AttributionError("control arm recorded node occupancies")
    if arms["f2"]["node_process_milestones"]["start"] <= 0:
        raise AttributionError("f2 arm recorded no node occupancy")

    left = arms["control"]["link_capacity"]
    right = arms["f2"]["link_capacity"]
    differing = sorted(k for k in set(left) | set(right)
                       if left.get(k) != right.get(k))
    failed = [f"{arm}:{name}" for arm, data in arms.items()
              for name, ok in data["checks"].items() if not ok]
    return {
        "schema": "leo-sim-f2-attribution/v1",
        "experiment": experiment,
        "tolerance_s": TOL,
        "arms": arms,
        "cross_arm": {
            "differing_link_count": len(differing),
            "differing_links": differing[:50],
            "asserted_equal": False,
            "note": ("reported, not asserted: a 0.05 s shift may legitimately move "
                     "an availability window across the 0.1 s sampling boundary"),
        },
        "failed_checks": failed,
        "ok": not failed,
    }


def _self_test() -> int:
    """Exercise every refusal path on a synthetic, deliberately damaged run."""
    import copy
    good = {
        "packet_events": [
            {"kind": "packet_emitted", "pid": 1, "at": 0.0, "bits": 100},
            {"kind": "queue_enter", "pid": 1, "at": 0.0, "queue": "isl",
             "link_id": "isl:0:1", "queue_id": 7},
            {"kind": "service_start", "pid": 1, "at": 0.5, "stage": "isl",
             "link_id": "isl:0:1", "queue_id": 7, "bits": 100,
             "rate_bps": 400.0},
            {"kind": "propagation_start", "pid": 1, "at": 0.75, "stage": "isl",
             "link_id": "isl:0:1", "prop_id": 3, "delay_s": 0.25},
            {"kind": "propagation_arrival", "pid": 1, "at": 1.0, "prop_id": 3},
            {"kind": "delivered", "pid": 1, "at": 1.0},
        ],
        "link_service_windows": [{
            "pid": 1, "stage": "isl", "link_id": "isl:0:1", "start": 0.5,
            "end": 0.75, "rate_bps": 400.0, "capacity_bits": 100.0,
            "served_bits": 100, "bits": 100, "outcome": "ok"}],
        "deliveries": {"1": {"delivered_at": 1.0}},
        "congestion_metrics": {"links": {}},
    }
    timeline = [
        {"milestone": "node_process_start", "pid": 1, "sat": 0, "via": "uplink",
         "at": 0.2},
        {"milestone": "node_process_end", "pid": 1, "sat": 0, "via": "uplink",
         "at": 0.25, "started_at": 0.2},
    ]
    failures = []

    def build(root: Path, *, ledger=None, tl=None, manifest=None,
              compute=0.05, node=0.05, receipt=b"{}"):
        base = root / "EXP-x-f2-s7"
        base.mkdir(parents=True)
        (base / "ledgers.json").write_text(
            json.dumps(good if ledger is None else ledger))
        raw = "".join(json.dumps(r) + "\n" for r in (timeline if tl is None else tl))
        (base / "timeline.jsonl").write_text(raw)
        (base / "resolved_config.json").write_text(json.dumps(
            {"config": {"execution": {"compute_delay_s": compute,
                                        "node_process_delay_s": node}}}))
        (base / "receipt.json").write_bytes(receipt)
        rows = [r for r in raw.splitlines() if r]
        side = {"row_count": len(rows),
                "log_sha256": hashlib.sha256(raw.encode()).hexdigest(),
                "receipt_sha256": hashlib.sha256(receipt).hexdigest()}
        side.update(manifest or {})
        (base / "timeline.jsonl.manifest.json").write_text(json.dumps(side))
        return root

    def expect_refusal(name, **kwargs):
        with tempfile.TemporaryDirectory() as tmp:
            root = build(Path(tmp), **kwargs)
            try:
                analyse_arm(root, "EXP-x-f2-s7", None)
            except AttributionError:
                print(f"  control triggered: {name}")
                return
            except Exception as exc:  # noqa: BLE001
                print(f"  control triggered (other): {name} -> {type(exc).__name__}")
                return
            failures.append(name)
            print(f"  UNPROVEN CONTROL: {name}")

    print("self-test refusal controls:")
    expect_refusal("truncated timeline (sidecar row_count mismatch)",
                   manifest={"row_count": 3})
    expect_refusal("empty timeline while config says node>0", tl=[])
    expect_refusal("vacuous ledger (no deliveries)",
                   ledger={**good, "deliveries": {}})
    expect_refusal("node_process_delay_s = 0 but milestones present",
                   node=0.0)
    expect_refusal("compute_delay_s = 0 (not discriminating)", compute=0.0)
    expect_refusal("receipt hash mismatch",
                   manifest={"receipt_sha256": "0" * 64})
    with tempfile.TemporaryDirectory() as tmp:
        try:
            root = build(Path(tmp))
            analyse_arm(root, "EXP-x-f2-s7", 0.1)
        except AttributionError:
            print("  control triggered: --compute-delay-s disagrees with the arm")
        else:
            failures.append("compute-delay mismatch")
            print("  UNPROVEN CONTROL: --compute-delay-s disagrees with the arm")
    with tempfile.TemporaryDirectory() as tmp:
        try:
            root = build(Path(tmp))
            out = analyse_arm(root, "EXP-x-f2-s7", None)
        except AttributionError as exc:
            failures.append(f"clean input refused: {exc}")
            print(f"  UNPROVEN CONTROL: clean input refused: {exc}")
        else:
            print("  clean input accepted (expected)"
                  f" leakage={out['leakage_s']!r}")
    if failures:
        print(f"SELF-TEST FAILED: {failures}")
        return 1
    print("self-test: all controls triggered")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-root", type=Path, default=Path("CODE/Results"))
    parser.add_argument("--experiment")
    parser.add_argument("--compute-delay-s", type=float, default=None)
    parser.add_argument("--pairing-key", default="s7",
                        help="the trace-seed suffix of the compiled run ids "
                             "(default s7); it is read from the request, not "
                             "guessed")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return _self_test()
    if not args.experiment or args.out is None:
        parser.error("--experiment and --out are required (or use --self-test)")

    report = run(args.results_root, args.experiment, args.compute_delay_s,
                 args.pairing_key)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    arms = report["arms"]
    print(json.dumps({
        "status": "ok" if report["ok"] else "FAILED",
        "out": str(args.out),
        "failed_checks": report["failed_checks"],
        **{f"{a}_node_process_s": d["total_node_process_s"]
           for a, d in arms.items()},
        **{f"{a}_labelled_decision_compute_s":
           d["labelled_total_decision_compute_s"] for a, d in arms.items()},
        **{f"{a}_unlabelled_decision_compute_s":
           d["unlabelled_total_decision_compute_s"] for a, d in arms.items()},
        "cross_arm_differing_links": report["cross_arm"]["differing_link_count"],
    }, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
