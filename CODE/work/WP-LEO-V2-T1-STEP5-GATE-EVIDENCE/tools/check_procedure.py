#!/usr/bin/env python3
"""Mechanical executable-procedure gate (step-5 batch, revision R05).

WHY THIS EXISTS
===============
Four review rounds kept finding the same class of defect: a process document was
treated as if it were executable while nothing mechanically compared the prose to
the tools it invokes - a RUNBOOK mandating a tool that rejects the declared
metric; a procedure naming superseded experiment directories; a procedure that
never documented the authorization step the launcher requires.

NEGATIVE CONTROLS ARE MANDATORY
===============================
A check that cannot fail is not a check. The first version of G1a used a regex
that forbade hyphens, matched none of the real ids and passed VACUOUSLY. The
second version scanned only backtick-fenced bash blocks, so a complete run command
placed in unfenced prose was accepted (found by the R04 adversarial review,
reproduced by the producer). Both are the failure mode this gate exists to
prevent. Therefore EVERY check runs a negative control in the same invocation and
prints its result:

  * a check whose negative control does NOT trigger is reported as an UNPROVEN
    GATE, listed in unproven_gates, and does NOT count as passed;
  * all_checks_ok is true only when no executed check failed AND none is unproven.

CHECKS
======
G1a NO line of the procedure - fenced or not - may contain an experiment id from
    another revision. The whole document text is scanned; there is no fence
    exemption. Control: a foreign id injected into UNFENCED text must be found.
G1b every command-like run-remote invocation anywhere in the document must be
    inside a fenced block that parses to a compiled cell of this revision, and the
    set of documented invocations must equal the compiled cells (config path,
    authorization path, session). Control: an unfenced complete invocation must be
    reported.
G2  the declared primary_metric must actually be ACCEPTED by the analyzer dispatch.
    Control: an unsupported metric name must be REJECTED.
G3  (phase all) the documented chain reaches the launcher accept/reject decision
    point for every cell. Control: a wrong run id must be REJECTED.
G4  the gate and the procedure are inside the revision's reviewed artifact set.
    Control: a synthetic set with a zeroed gate hash must report a problem.
G5  every cell's resolved config must have F2 DISABLED and the gate must report the
    actual resolved value, so the F2 disclosure is mechanically backed.
    Control: a synthetic config with node_process_delay_s = 0.5 must be flagged.
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

SCHEMA = "leo-sim-step5-procedure-gate/v3"
FENCE = chr(96) * 3
REVISION_ID = re.compile(r"EXP-[A-Za-z0-9_-]*-R(\d\d)\b")
CONFIG_ARG = re.compile(r"--config\s+(\S+?\.leo-sim\.yaml)")
AUTH_ARG = re.compile(r"--authorization\s+(\S+?\.json)")
SESSION_ARG = re.compile(r"--session\s+(\S+)")
UNSUPPORTED_METRIC = "definitely_not_a_supported_metric_xyz"
F2_KEY = "node_process_delay_s"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fence_index(text: str):
    """Return (lines, inside) where inside[i] says whether line i is fenced."""
    lines = text.splitlines()
    inside, flags = False, []
    for line in lines:
        if line.strip().startswith(FENCE):
            flags.append(False)
            inside = not inside
            continue
        flags.append(inside)
    return lines, flags


def bash_blocks(text: str):
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


def _verdict(name, ok, control, control_triggered, detail, skipped_reason=None):
    entry = {"check": name, "ok": bool(ok), "control": control,
             "control_triggered": bool(control_triggered),
             "proven": bool(control_triggered), "detail": detail}
    if skipped_reason:
        entry["skipped_reason"] = skipped_reason
    return entry


# ------------------------------------------------------------------ G1a
def _foreign_ids(text, own):
    """Scan the WHOLE document text; no fence exemption."""
    seen = sorted({m.group(0) for m in REVISION_ID.finditer(text)})
    return seen, sorted(t for t in seen if t not in own)


def check_g1a(procedure_text, own_set, results):
    seen, foreign = _foreign_ids(procedure_text, own_set)
    # control: inject a foreign id into UNFENCED text
    injected = None
    if own_set:
        first = sorted(own_set)[0]
        injected = first[:-3] + "R99"
        mutated = procedure_text + chr(10) + "See also " + injected + " for history." + chr(10)
        _s, ctrl_foreign = _foreign_ids(mutated, own_set)
        ctrl_ok = injected in ctrl_foreign
        control = {"injected_id": injected, "injected_outside_fences": True,
                   "detected": bool(ctrl_ok),
                   "note": None if ctrl_ok else "unfenced foreign id NOT detected - G1a is defeatable"}
    else:
        ctrl_ok = False
        control = {"injected_id": None, "detected": False, "note": "no own id to mutate"}
    results.append(_verdict("G1a_no_foreign_revision_anywhere_in_document",
                            not foreign, control, ctrl_ok,
                            {"revision_ids_in_document": seen,
                             "this_revision_ids": sorted(own_set), "foreign": foreign}))


# ------------------------------------------------------------------ G1b
def _planned_cells(root, experiment_ids):
    planned = {}
    for eid in experiment_ids:
        man = json.loads((root / "EXPERIMENTS" / eid / "run-manifest.json").read_text())
        for cell in man["cells"]:
            planned[cell["run_id"]] = cell["config_path"]
    return planned


def _is_command_like(line: str) -> bool:
    return "run-remote.sh" in line and ("--config" in line or "--runtime-kind" in line)


def _parse_fenced_invocations(text):
    found, mismatches = {}, []
    for block in bash_blocks(text):
        if "run-remote.sh" not in block:
            continue
        cfg, auth, sess = CONFIG_ARG.search(block), AUTH_ARG.search(block), SESSION_ARG.search(block)
        if not (cfg and auth and sess):
            mismatches.append({"block": block.strip()[:160],
                               "reason": "incomplete run-remote invocation"})
            continue
        run_id = Path(cfg.group(1)).name.removesuffix(".leo-sim.yaml")
        found[run_id] = {"config": cfg.group(1), "authorization": auth.group(1),
                         "session": sess.group(1)}
    return found, mismatches


def _g1b_evaluate(root, text, experiment_ids):
    lines, inside = _fence_index(text)
    planned = _planned_cells(root, experiment_ids)
    found, mismatches = _parse_fenced_invocations(text)
    # every command-like run-remote line must sit inside a fence
    for i, line in enumerate(lines):
        if _is_command_like(line) and not inside[i]:
            mismatches.append({"line_number": i + 1, "reason": "command-like run-remote line OUTSIDE any fence",
                               "line": line.strip()[:160]})
    for run_id, got in found.items():
        if run_id not in planned:
            mismatches.append({"run_id": run_id, "reason": "not a compiled cell of this revision"})
            continue
        exp_id = run_id.rsplit("-", 2)[0]
        expected_cfg = "EXPERIMENTS/" + exp_id + "/" + planned[run_id]
        if got["config"] != expected_cfg:
            mismatches.append({"run_id": run_id, "reason": "config path mismatch",
                               "documented": got["config"], "expected": expected_cfg})
        expected_auth = "EXPERIMENTS/" + exp_id + "/authorization.json"
        if got["authorization"] != expected_auth:
            mismatches.append({"run_id": run_id, "reason": "authorization path mismatch",
                               "documented": got["authorization"], "expected": expected_auth})
        if got["session"] != run_id.lower():
            mismatches.append({"run_id": run_id, "reason": "session name does not match run id",
                               "documented": got["session"], "expected": run_id.lower()})
    missing = sorted(set(planned) - set(found))
    extra = sorted(set(found) - set(planned))
    return planned, found, mismatches, missing, extra


def check_g1b(root, procedure_text, experiment_ids, results):
    planned, found, mismatches, missing, extra = _g1b_evaluate(root, procedure_text, experiment_ids)
    # negative control: append a COMPLETE run-remote invocation in unfenced prose
    own = sorted(experiment_ids)[0] if experiment_ids else None
    ctrl_ok, control = False, {"injected": None, "detected": False}
    if own:
        bogus = ("Prose: CODE/scripts/remote/run-remote.sh --runtime-kind leo_sim_v2 "
                 "--config EXPERIMENTS/" + own + "/resolved/DOES-NOT-EXIST.leo-sim.yaml "
                 "--authorization EXPERIMENTS/" + own + "/authorization.json --session bogus")
        _p, _f, mm, _mi, _e = _g1b_evaluate(root, procedure_text + chr(10) + bogus + chr(10), experiment_ids)
        hit = [m for m in mm if "OUTSIDE any fence" in m.get("reason", "")]
        ctrl_ok = bool(hit)
        control = {"injected": "unfenced complete run-remote invocation",
                   "detected": bool(ctrl_ok), "hits": hit[:2]}
        if not ctrl_ok:
            control["note"] = "unfenced invocation NOT reported - G1b is defeatable"
    results.append(_verdict("G1b_run_commands_match_compiled_cells_and_are_fenced",
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
    try:
        V._metric_from_result(receipt, ledgers, UNSUPPORTED_METRIC)
        ctrl_ok = False
        control = {"probe": UNSUPPORTED_METRIC, "rejected": False,
                   "note": "unsupported metric ACCEPTED - G2 probe is vacuous"}
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
                            {"wrong_run_id_probe": ctrl}, ctrl_ok, {"cells": per_cell}))


# ------------------------------------------------------------------ G4
def _binding_problems(arts, procedure_path, root, gate_path):
    problems = []
    if not root.is_absolute() or not str(gate_path).startswith(str(root)):
        problems.append("gate path " + str(gate_path) + " is NOT inside root " + str(root))
        return problems, None, None
    rel_gate = str(gate_path.relative_to(root))
    rel_proc = str(procedure_path.relative_to(root))
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
    gate_path = Path(__file__).resolve()
    if not artifact_set.is_file():
        results.append(_verdict("G4_gate_is_inside_reviewed_set", False, {}, False,
                                {"reason": "artifact-set.json not found"}))
        return
    arts = json.loads(artifact_set.read_text())
    problems, rel_gate, rel_proc = _binding_problems(arts, procedure, root, gate_path)
    ctrl_ok, ctrl_problems = False, []
    if rel_gate is not None:
        synth = dict(arts); synth[rel_gate] = "0" * 64
        ctrl_problems, _g, _p = _binding_problems(synth, procedure, root, gate_path)
        ctrl_ok = bool(ctrl_problems)
    control = {"injected": "gate hash replaced with zeros in a synthetic set",
               "detected": bool(ctrl_problems), "control_problems": ctrl_problems}
    if not ctrl_ok:
        control["note"] = "zeroed gate hash NOT reported - G4 is vacuous"
    results.append(_verdict("G4_gate_is_inside_reviewed_set", not problems, control, ctrl_ok,
                            {"gate_path": rel_gate, "procedure_path": rel_proc,
                             "problems": problems}))


# ------------------------------------------------------------------ G5
def _f2_ok(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and float(value) == 0.0


def check_g5(root, experiment_ids, results):
    per_cell, ok = [], True
    for eid in experiment_ids:
        exp_dir = root / "EXPERIMENTS" / eid
        man = json.loads((exp_dir / "run-manifest.json").read_text())
        for cell in man["cells"]:
            cfg = json.loads((exp_dir / cell["config_path"]).read_text())
            ex = cfg["execution"]
            f2 = ex.get(F2_KEY)
            good = _f2_ok(f2)
            if not good:
                ok = False
            per_cell.append({"run_id": cell["run_id"],
                             F2_KEY: f2,
                             "compute_delay_s": ex.get("compute_delay_s"),
                             "f2_disabled": good})
    # control: a non-zero F2 value must be rejected by the same predicate
    ctrl_ok = not _f2_ok(0.5)
    control = {"probe": {F2_KEY: 0.5}, "flagged_as_not_disabled": bool(ctrl_ok)}
    if not ctrl_ok:
        control["note"] = "non-zero F2 value NOT flagged - G5 is vacuous"
    results.append(_verdict("G5_f2_disabled_and_actual_value_reported", ok, control, ctrl_ok,
                            {"cells": per_cell,
                             "statement": "deployment contains F2 code with F2 DISABLED; actual resolved values reported per cell"}))


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
    check_g1a(text, set(a.experiment_id), results)
    check_g1b(root, text, a.experiment_id, results)
    check_g2(root, a.experiment_id, results)
    check_g3(root, a.experiment_id, results, a.phase)
    check_g4(root, procedure, artifact_set, results)
    check_g5(root, a.experiment_id, results)

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
                      "skipped_checks": [s["check"] for s in skipped],
                      "checks_executed": len(executed)}, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
