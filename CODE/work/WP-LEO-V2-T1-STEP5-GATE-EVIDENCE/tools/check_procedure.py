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

NEGATIVE CONTROLS ARE MANDATORY
===============================
A check that cannot fail is not a check. The first version of G1a used a regex
that forbade hyphens, matched none of the real ids, and passed VACUOUSLY - the
very failure mode this gate exists to prevent. Therefore EVERY check here runs a
negative control in the same invocation and prints its result:

  * a check whose negative control does NOT trigger is reported as an
    UNPROVEN GATE, is listed in unproven_gates, and does NOT count as passed;
  * all_checks_ok is true only when no executed check failed AND no executed
    check is unproven.

CHECKS
======
G1a no run command references another revision (control: inject a foreign id and
    require detection).
G1b the documented run commands are exactly this revision's compiled cells -
    config path, authorization path and session (control: corrupt one session and
    require a mismatch).
G2  the declared primary_metric is actually ACCEPTED by the analyzer dispatch
    (control: an unsupported metric name must be REJECTED).
G3  (phase all) the documented chain reaches the launcher accept/reject decision
    point for every cell (control: a wrong run id must be REJECTED).
G4  the gate and the procedure are inside the revision's reviewed artifact set
    (control: a synthetic set with a wrong gate hash must report a problem).
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

SCHEMA = "leo-sim-step5-procedure-gate/v2"
FENCE = chr(96) * 3
REVISION_ID = re.compile(r"EXP-[A-Za-z0-9_-]*-R(\d\d)\b")
CONFIG_ARG = re.compile(r"--config\s+(\S+?\.leo-sim\.yaml)")
AUTH_ARG = re.compile(r"--authorization\s+(\S+?\.json)")
SESSION_ARG = re.compile(r"--session\s+(\S+)")
UNSUPPORTED_METRIC = "definitely_not_a_supported_metric_xyz"


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


def _verdict(name, ok, control, control_triggered, detail, skipped_reason=None):
    entry = {"check": name, "ok": bool(ok), "control": control,
             "control_triggered": bool(control_triggered),
             "proven": bool(control_triggered), "detail": detail}
    if skipped_reason:
        entry["skipped_reason"] = skipped_reason
    return entry


# ------------------------------------------------------------------ G1a
def _scan_revision_ids(text):
    joined = "\n".join(command_lines(text))
    return sorted({m.group(0) for m in REVISION_ID.finditer(joined)})


def check_g1a(procedure_text, own, results):
    seen = _scan_revision_ids(procedure_text)
    foreign = sorted(t for t in seen if t not in own)
    if own:
        first = sorted(own)[0]
        injected = first[:-3] + "R99"
        ctrl_seen = _scan_revision_ids(procedure_text.replace(first, injected))
        ctrl_foreign = sorted(t for t in ctrl_seen if t not in own)
        control = {"injected_id": injected, "detected": bool(ctrl_foreign),
                   "control_ids_seen": ctrl_seen}
        ctrl_ok = bool(ctrl_foreign)
    else:
        control = {"injected_id": None, "detected": False, "note": "no own id available to mutate"}
        ctrl_ok = False
    results.append(_verdict("G1a_no_foreign_revision_in_commands", not foreign,
                            control, ctrl_ok,
                            {"revision_ids_in_commands": seen,
                             "this_revision_ids": sorted(own), "foreign": foreign}))


# ------------------------------------------------------------------ G1b
def _compare_run_commands(root, text, experiment_ids):
    planned = {}
    for eid in experiment_ids:
        man = json.loads((root / "EXPERIMENTS" / eid / "run-manifest.json").read_text())
        for cell in man["cells"]:
            planned[cell["run_id"]] = cell["config_path"]
    found, mismatches = {}, []
    for block in bash_blocks(text):
        if "run-remote.sh" not in block:
            continue
        cfg = CONFIG_ARG.search(block)
        auth = AUTH_ARG.search(block)
        sess = SESSION_ARG.search(block)
        if not (cfg and auth and sess):
            mismatches.append({"block": block.strip()[:160],
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
    return planned, found, mismatches, missing, extra


def check_g1b(root, procedure_text, experiment_ids, results):
    planned, found, mismatches, missing, extra = _compare_run_commands(
        root, procedure_text, experiment_ids)
    # negative control: corrupt one documented session and require a mismatch
    mutated, injected = procedure_text, None
    if found:
        any_run = sorted(found)[0]
        want = "--session " + any_run.lower()
        if want in mutated:
            injected = "WRONG-session-for-" + any_run
            mutated = mutated.replace(want, "--session " + injected, 1)
            _p, _f, mm, _mi, _e = _compare_run_commands(root, mutated, experiment_ids)
            ctrl_ok = bool(mm) or bool(_e)
            control = {"injected": injected, "detected": bool(ctrl_ok),
                       "control_mismatches": mm[:3]}
            if not control["detected"]:
                control["note"] = "corrupted session was NOT reported - G1b is vacuous"
        else:
            ctrl_ok, control = False, {"injected": None, "detected": False,
                                       "note": "no session token found to corrupt"}
    else:
        ctrl_ok, control = False, {"injected": None, "detected": False,
                                   "note": "no run-remote block found to corrupt"}
    results.append(_verdict("G1b_run_commands_match_compiled_cells",
                            not (mismatches or missing or extra), control, ctrl_ok,
                            {"planned_cells": len(planned), "documented_runs": len(found),
                             "missing_from_procedure": missing, "extra_in_procedure": extra,
                             "mismatches": mismatches}))


# ------------------------------------------------------------------ G2
def _metric_fixture():
    receipt = {"totals": {"delivered_bits": 1000.0, "terminal_loss_bits": 0.0,
                          "in_system_bits_at_stop": 0.0},
               "fate_counts": {"DELIVERED": 1}}
    ledgers = {"congestion_metrics": {
        "access_admission_rate": 1.0, "network_delivery_rate_by_horizon": 1.0,
        "packets": {"1": {"e2e_s": 1.5, "total_queue_wait_s": 0.25,
                          "tx_s": 1.0, "prop_s": 0.25}},
        "links": {"isl:0:1": {"stage": "isl", "utilization": 0.5},
                  "gsl:uplink:0:A": {"stage": "uplink", "utilization": 0.25}}}}
    return receipt, ledgers


def check_g2(root, experiment_ids, results):
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
    # negative control: an unsupported name must be rejected, else the probe
    # accepts everything and proves nothing.
    try:
        V._metric_from_result(receipt, ledgers, UNSUPPORTED_METRIC)
        ctrl_ok = False
        control = {"probe": UNSUPPORTED_METRIC, "rejected": False,
                   "note": "unsupported metric was ACCEPTED - the G2 probe is vacuous"}
    except V.V2AnalysisError as exc:
        ctrl_ok = True
        control = {"probe": UNSUPPORTED_METRIC, "rejected": True, "error": str(exc)[:120]}
    results.append(_verdict("G2_declared_primary_metric_accepted_by_toolchain",
                            not bad, control, ctrl_ok,
                            {"declared": declared, "accepted_metrics": accepted,
                             "rejected_metrics": rejected, "rejected_declared": bad}))


# ------------------------------------------------------------------ G3
def check_g3(root, experiment_ids, results, phase):
    from CODE.experiment_platform import authorize_experiment as A
    if phase == "pre-review":
        results.append(_verdict(
            "G3_chain_reaches_launcher_decision_point", True, {}, False, {},
            skipped_reason="phase pre-review: no authorization exists yet; run --phase all after authorization"))
        return
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
    # negative control: a wrong run id must be REJECTED for every experiment
    ctrl, ctrl_ok = [], True
    for eid in experiment_ids:
        exp_dir = root / "EXPERIMENTS" / eid
        auth = exp_dir / "authorization.json"
        man = json.loads((exp_dir / "run-manifest.json").read_text())
        if not auth.is_file():
            ctrl_ok = False
            ctrl.append({"experiment": eid, "note": "no authorization to test the control against"})
            continue
        run_id = man["cells"][0]["run_id"] + "-NONEXISTENT"
        try:
            A.verify_authorization_for_leo_sim_v2_config(
                root, auth, (exp_dir / man["cells"][0]["config_path"]).resolve(), run_id)
            ctrl_ok = False
            ctrl.append({"experiment": eid, "wrong_run_id": run_id, "result": "ACCEPTED (control failed)"})
        except Exception as exc:
            ctrl.append({"experiment": eid, "wrong_run_id": run_id,
                         "result": "REJECTED: " + type(exc).__name__})
    results.append(_verdict("G3_chain_reaches_launcher_decision_point", ok,
                            {"wrong_run_id_probe": ctrl}, ctrl_ok,
                            {"cells": per_cell}))


# ------------------------------------------------------------------ G4
def _binding_problems(arts, procedure_path, root, gate_path):
    problems = []
    rel_gate = str(gate_path.resolve().relative_to(root.resolve()))
    rel_proc = str(procedure_path.resolve().relative_to(root.resolve()))
    if rel_gate not in arts:
        problems.append("gate not bound: " + rel_gate)
    elif arts[rel_gate] != sha256_file(gate_path):
        problems.append("gate bound with a stale hash")
    if rel_proc not in arts:
        problems.append("procedure not bound: " + rel_proc)
    elif arts[rel_proc] != sha256_file(procedure_path):
        problems.append("procedure bound with a stale hash")
    return problems, rel_gate, rel_proc


def check_g4(root, procedure, artifact_set, results):
    if not artifact_set.is_file():
        results.append(_verdict("G4_gate_is_inside_reviewed_set", False, {}, False,
                                {"reason": "artifact-set.json not found"}))
        return
    arts = json.loads(artifact_set.read_text())
    gate_path = Path(__file__).resolve()
    problems, rel_gate, rel_proc = _binding_problems(arts, procedure, root, gate_path)
    # negative control: a synthetic set with a wrong gate hash must report a problem
    synth = dict(arts)
    synth[rel_gate] = "0" * 64
    ctrl_problems, _g, _p = _binding_problems(synth, procedure, root, gate_path)
    ctrl_ok = bool(ctrl_problems)
    results.append(_verdict("G4_gate_is_inside_reviewed_set", not problems,
                            {"injected": "gate hash replaced with zeros in a synthetic set",
                             "detected": bool(ctrl_problems),
                             "control_problems": ctrl_problems},
                            ctrl_ok,
                            {"gate_path": rel_gate, "procedure_path": rel_proc,
                             "problems": problems}))


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
    text = procedure.read_text(encoding="utf-8")
    results = []
    check_g1a(text, a.experiment_id, results)
    check_g1b(root, text, a.experiment_id, results)
    check_g2(root, a.experiment_id, results)
    check_g3(root, a.experiment_id, results, a.phase)
    check_g4(root, procedure, artifact_set, results)

    executed = [c for c in results if "skipped_reason" not in c]
    failed = [c["check"] for c in executed if not c["ok"]]
    unproven = [c["check"] for c in executed if not c["proven"]]
    skipped = [{"check": c["check"], "reason": c["skipped_reason"]}
               for c in results if "skipped_reason" in c]
    ok = not failed and not unproven
    report = {"schema": SCHEMA, "phase": a.phase, "root": str(root),
              "procedure": a.procedure, "experiment_ids": a.experiment_id,
              "checks": results, "checks_executed": len(executed),
              "failed_checks": failed, "unproven_gates": unproven,
              "skipped_checks": skipped, "all_checks_ok": ok,
              "rule": ("all_checks_ok is true only when no executed check failed AND no "
                       "executed check is unproven; an unproven check means its negative "
                       "control did not trigger and it must not be counted as passed")}
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(json.dumps({"wrote": str(out), "phase": a.phase, "all_checks_ok": ok,
                      "failed_checks": failed, "unproven_gates": unproven,
                      "skipped_checks": [s["check"] for s in skipped]}, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
