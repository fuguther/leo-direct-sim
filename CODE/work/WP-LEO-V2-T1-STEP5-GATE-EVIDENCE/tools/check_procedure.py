#!/usr/bin/env python3
"""Mechanical executable-procedure gate (step-5 batch, R04).

WHY THIS EXISTS
===============
Three review rounds found the same class of defect: a process document was
treated as if it were executable, and nothing mechanically compared the prose to
the tools it invokes. Round 1: the compiler-generated RUNBOOK mandates a
post-run analysis step whose metric whitelist unconditionally rejects the metric
the request declared, so the documented flow could not complete. Round 2: the
procedure named superseded experiment directories, and because run-remote.sh
derives the run id from the config filename, following it would have run the
wrong revision - and the procedure documented no finalization/authorization step
even though the launcher refuses to start without an authorization.

This gate turns those lessons into a check that FAILS LOUD. It is itself part of
the reviewed artifact set, so a revision cannot claim compliance it does not
have.

CHECKS
======
G1  no run command references any revision other than this one, and the run
    commands in the procedure are exactly the cells of this revision's compiled
    run-manifests (config path, authorization path and session all consistent).
G2  the primary_metric the request declares is actually ACCEPTED by the
    toolchain, proven by invoking the very function the RUNBOOK-mandated
    analyzer uses (CODE.experiment_platform.v2_analysis._metric_from_result) -
    not by reading code.
G3  (pre-run) the whole documented chain reaches the launcher accept/reject
    decision point: for every cell, the exact module run-remote.sh invokes
    (CODE.experiment_platform.v2_serial_gate) plus the exact authorization
    binding check the launcher performs must pass.
G4  this gate is itself inside the revision's reviewed artifact set.

Any failure exits non-zero; a failing revision must be REVISED and must not
reach a formal run.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

SCHEMA = "leo-sim-step5-procedure-gate/v1"
FENCE = chr(96) * 3
REVISION_ID = re.compile(r"EXP-[A-Za-z0-9_-]*-R(\d\d)\b")
CONFIG_ARG = re.compile(r"--config\s+(\S+?\.leo-sim\.yaml)")
AUTH_ARG = re.compile(r"--authorization\s+(\S+?\.json)")
SESSION_ARG = re.compile(r"--session\s+(\S+)")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bash_blocks(text: str):
    """Yield the body of every fenced bash block."""
    out, current, inside = [], [], False
    for line in text.splitlines():
        if line.strip().startswith(FENCE):
            if inside:
                out.append("\n".join(current))
                current, inside = [], False
            else:
                inside = True
            continue
        if inside:
            current.append(line)
    if inside:
        out.append("\n".join(current))
    return out


def command_lines(text: str):
    """Command lines only: bash-block lines that are not prose or comments."""
    lines = []
    for block in bash_blocks(text):
        for raw in block.splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            lines.append(line)
    return lines


def _scan_revision_ids(text):
    joined = "\n".join(command_lines(text))
    return sorted({m.group(0) for m in REVISION_ID.finditer(joined)})


def check_g1(root: Path, procedure: Path, experiment_ids, results):
    text = procedure.read_text(encoding="utf-8")
    cmds = command_lines(text)
    own = set(experiment_ids)
    seen = _scan_revision_ids(text)
    foreign = sorted(t for t in seen if t not in own)
    results.append({
        "check": "G1a_no_foreign_revision_in_commands",
        "ok": not foreign,
        "detail": {"revision_ids_in_commands": seen,
                   "this_revision_ids": sorted(own),
                   "foreign": foreign},
    })

    # NEGATIVE CONTROL: the scan above must be able to SEE an id at all. A regex
    # that matches nothing would make G1a pass vacuously, which is exactly the
    # failure mode this gate exists to prevent. Mutate one own id to an earlier
    # revision and require the scan to report it as foreign.
    control_detail = {"applicable": False}
    control_ok = True
    if own:
        first = sorted(own)[0]
        mutated = text.replace(first, first[:-3] + "R99")
        ctrl_seen = _scan_revision_ids(mutated)
        ctrl_foreign = sorted(t for t in ctrl_seen if t not in own)
        control_ok = bool(ctrl_foreign) and len(ctrl_seen) >= len(seen)
        control_detail = {"applicable": True, "mutated_id": first[:-3] + "R99",
                          "control_ids_seen": ctrl_seen,
                          "control_foreign": ctrl_foreign,
                          "real_ids_seen": seen,
                          "note": "scan must detect the injected foreign id, else G1a is vacuous"}
    results.append({
        "check": "G1a_negative_control_scan_is_not_vacuous",
        "ok": control_ok,
        "detail": control_detail,
    })

    planned = {}
    for eid in experiment_ids:
        man = json.loads((root / "EXPERIMENTS" / eid / "run-manifest.json").read_text())
        for cell in man["cells"]:
            planned[cell["run_id"]] = cell["config_path"]

    found = {}
    mismatches = []
    for block in bash_blocks(text):
        if "run-remote.sh" not in block:
            continue
        cfg = CONFIG_ARG.search(block)
        auth = AUTH_ARG.search(block)
        sess = SESSION_ARG.search(block)
        if not (cfg and auth and sess):
            mismatches.append({"block": block.strip()[:200],
                               "reason": "incomplete run-remote invocation"})
            continue
        run_id = Path(cfg.group(1)).name.removesuffix(".leo-sim.yaml")
        found[run_id] = {"config": cfg.group(1), "authorization": auth.group(1),
                         "session": sess.group(1)}
        if run_id not in planned:
            mismatches.append({"run_id": run_id,
                               "reason": "not a compiled cell of this revision"})
            continue
        exp_id = run_id.rsplit("-", 2)[0]
        expected_cfg = "EXPERIMENTS/" + exp_id + "/" + planned[run_id]
        if cfg.group(1) != expected_cfg:
            mismatches.append({"run_id": run_id, "reason": "config path mismatch",
                               "documented": cfg.group(1), "expected": expected_cfg})
        expected_auth = "EXPERIMENTS/" + exp_id + "/authorization.json"
        if auth.group(1) != expected_auth:
            mismatches.append({"run_id": run_id, "reason": "authorization path mismatch",
                               "documented": auth.group(1), "expected": expected_auth})
        if sess.group(1) != run_id.lower():
            mismatches.append({"run_id": run_id, "reason": "session name does not match run id",
                               "documented": sess.group(1), "expected": run_id.lower()})
    missing = sorted(set(planned) - set(found))
    extra = sorted(set(found) - set(planned))
    results.append({
        "check": "G1b_run_commands_match_compiled_cells",
        "ok": not (mismatches or missing or extra),
        "detail": {"planned_cells": len(planned), "documented_runs": len(found),
                   "missing_from_procedure": missing, "extra_in_procedure": extra,
                   "mismatches": mismatches},
    })


def _metric_fixture():
    """A synthetic receipt/ledgers pair carrying every field the analyzer's
    metric dispatch can need, so a rejection means whitelist rejection."""
    receipt = {
        "totals": {"delivered_bits": 1000.0, "terminal_loss_bits": 0.0,
                   "in_system_bits_at_stop": 0.0},
        "fate_counts": {"DELIVERED": 1},
    }
    ledgers = {"congestion_metrics": {
        "access_admission_rate": 1.0,
        "network_delivery_rate_by_horizon": 1.0,
        "packets": {"1": {"e2e_s": 1.5, "total_queue_wait_s": 0.25,
                          "tx_s": 1.0, "prop_s": 0.25}},
        "links": {"isl:0:1": {"stage": "isl", "utilization": 0.5},
                  "gsl:uplink:0:A": {"stage": "uplink", "utilization": 0.25}},
    }}
    return receipt, ledgers


def check_g2(root: Path, experiment_ids, results):
    from CODE.experiment_platform import v2_analysis as V
    receipt, ledgers = _metric_fixture()
    accepted, rejected = [], []
    for name in ("delivery_rate", "delivered_bits", "terminal_loss_bits",
                 "in_system_bits_at_stop", "access_admission_rate",
                 "network_delivery_rate_by_horizon", "e2e_delay_mean_s",
                 "queue_wait_mean_s", "tx_time_mean_s", "propagation_time_mean_s",
                 "link_utilization_mean", "service_window_utilization_mean",
                 "isl_link_utilization_mean", "isl_link_utilization_max"):
        try:
            V._metric_from_result(receipt, ledgers, name)
            accepted.append(name)
        except V.V2AnalysisError as exc:
            rejected.append({"metric": name, "error": str(exc)[:120]})
    declared = {}
    for eid in experiment_ids:
        ana = json.loads((root / "EXPERIMENTS" / eid / "analysis-request.json").read_text())
        declared[eid] = ana["analysis"]["primary_metric"]
    bad = [{"experiment": eid, "primary_metric": m,
            "status": "REJECTED by the analyzer toolchain"}
           for eid, m in declared.items() if m not in accepted]
    results.append({
        "check": "G2_declared_primary_metric_accepted_by_toolchain",
        "ok": not bad,
        "detail": {"declared": declared, "accepted_metrics": accepted,
                   "rejected_metrics": rejected, "rejected_declared": bad},
    })


def check_g3(root: Path, experiment_ids, results):
    from CODE.experiment_platform import authorize_experiment as A
    per_cell, ok = [], True
    for eid in experiment_ids:
        exp_dir = root / "EXPERIMENTS" / eid
        auth = exp_dir / "authorization.json"
        man = json.loads((exp_dir / "run-manifest.json").read_text())
        if not auth.is_file():
            per_cell.append({"experiment": eid, "status": "NO_AUTHORIZATION_YET"})
            ok = False
            continue
        for cell in man["cells"]:
            run_id = cell["run_id"]
            entry = {"experiment": eid, "run_id": run_id}
            try:
                A.verify_authorization_for_leo_sim_v2_config(
                    root, auth, (exp_dir / cell["config_path"]).resolve(), run_id)
                entry["authorization_binding"] = "ACCEPT"
            except Exception as exc:
                entry["authorization_binding"] = "REJECT: " + type(exc).__name__ + ": " + str(exc)[:120]
                ok = False
            proc = subprocess.run(
                [sys.executable, "-m", "CODE.experiment_platform.v2_serial_gate",
                 "--root", str(root), "--experiment", str(exp_dir),
                 "--authorization", str(auth), "--next-run-id", run_id],
                cwd=str(root), capture_output=True, text=True)
            entry["serial_gate"] = "ACCEPT" if proc.returncode == 0 else \
                "REJECT(exit=" + str(proc.returncode) + "): " + (proc.stderr or proc.stdout).strip()[:160]
            if proc.returncode != 0:
                ok = False
            per_cell.append(entry)
    results.append({"check": "G3_chain_reaches_launcher_decision_point",
                    "ok": ok, "detail": {"cells": per_cell}})


def check_g4(root: Path, procedure: Path, artifact_set: Path, results):
    if not artifact_set.is_file():
        results.append({"check": "G4_gate_is_inside_reviewed_set", "ok": False,
                        "detail": {"reason": "artifact-set.json not found",
                                   "path": str(artifact_set)}})
        return
    arts = json.loads(artifact_set.read_text())
    rel_gate = str(Path(__file__).resolve().relative_to(root.resolve()))
    rel_proc = str(procedure.resolve().relative_to(root.resolve()))
    problems = []
    if rel_gate not in arts:
        problems.append("gate not bound: " + rel_gate)
    elif arts[rel_gate] != sha256_file(Path(__file__).resolve()):
        problems.append("gate bound with a stale hash")
    if rel_proc not in arts:
        problems.append("procedure not bound: " + rel_proc)
    elif arts[rel_proc] != sha256_file(procedure):
        problems.append("procedure bound with a stale hash")
    results.append({"check": "G4_gate_is_inside_reviewed_set", "ok": not problems,
                    "detail": {"gate_path": rel_gate, "procedure_path": rel_proc,
                               "problems": problems}})


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".")
    ap.add_argument("--procedure", required=True)
    ap.add_argument("--artifact-set", required=True)
    ap.add_argument("--experiment-id", action="append", required=True)
    ap.add_argument("--phase", choices=["pre-review", "pre-run", "all"], default="all")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    root = Path(a.root).resolve()
    procedure = (root / a.procedure).resolve()
    artifact_set = (root / a.artifact_set).resolve()
    if not procedure.is_file():
        print("gate: procedure not found: " + str(procedure), file=sys.stderr)
        return 2
    results = []
    check_g1(root, procedure, a.experiment_id, results)
    check_g2(root, a.experiment_id, results)
    if a.phase in ("pre-run", "all"):
        check_g3(root, a.experiment_id, results)
    check_g4(root, procedure, artifact_set, results)
    ok = all(r["ok"] for r in results)
    report = {"schema": SCHEMA, "phase": a.phase, "root": str(root),
              "procedure": str(a.procedure), "experiment_ids": a.experiment_id,
              "checks": results, "all_checks_ok": ok}
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(json.dumps({"wrote": str(out), "phase": a.phase, "all_checks_ok": ok,
                      "failed": [r["check"] for r in results if not r["ok"]]},
                     sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
