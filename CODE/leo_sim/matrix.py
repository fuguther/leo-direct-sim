"""Strict, reviewable matrix contracts for the retained leo_sim V2 runtime.

The matrix contract is deliberately separate from the historical single-run
``leo-sim-experiment-request/v1`` contract.  It resolves every cell through
the same V2 governance path, but never launches a run or performs analysis.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from . import config as config_mod
from . import governance

MATRIX_REQUEST_SCHEMA = "leo-sim-experiment-matrix-request/v1"
MATRIX_MANIFEST_SCHEMA = "leo-sim-experiment-matrix-manifest/v1"
MATRIX_ANALYSIS_SCHEMA = "leo-sim-matrix-analysis-request/v1"
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
EXPERIMENT_ID = re.compile(r"^EXP-[A-Za-z0-9][A-Za-z0-9_-]*$")
PHASES = {"training", "evaluation", "train", "eval", "non_learning"}
LINEAGE_MODES = {"new_training", "evaluation_only", "not_applicable"}


class MatrixError(ValueError):
    """Raised when a matrix cannot be represented without ambiguity."""


def _normalize_phase(value: str) -> str:
    return {"train": "training", "eval": "evaluation"}.get(value, value)


def canonical_sha(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _expect_keys(value: Any, expected: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise MatrixError(f"{label} must be a mapping")
    unknown = set(value) - expected
    missing = expected - set(value)
    if unknown:
        if label == "matrix request":
            raise MatrixError(f"unknown request fields {sorted(unknown)}")
        raise MatrixError(f"{label} unknown fields {sorted(unknown)}")
    if missing:
        raise MatrixError(f"{label} missing fields {sorted(missing)}")
    return value


def _safe_id(value: Any, label: str) -> str:
    if not isinstance(value, str) or SAFE_ID.fullmatch(value) is None:
        raise MatrixError(f"{label} must be a safe identifier")
    return value


def _nonnegative_int(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise MatrixError(f"{label} must be a non-negative integer")
    return value


def _mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise MatrixError(f"{label} must be a mapping")
    return value


def _validate_checkpoint_lineage(value: Any, label: str) -> dict[str, Any]:
    lineage = _expect_keys(value, {"mode", "source_run_id", "source_sha256"}, label)
    if lineage["mode"] not in LINEAGE_MODES:
        raise MatrixError(f"{label}.mode is invalid")
    source_run_id = lineage["source_run_id"]
    source_sha = lineage["source_sha256"]
    if source_run_id is not None:
        _safe_id(source_run_id, f"{label}.source_run_id")
    if source_sha is not None and (
            not isinstance(source_sha, str) or
            not re.fullmatch(r"[0-9a-f]{64}", source_sha)):
        raise MatrixError(f"{label}.source_sha256 must be lowercase SHA256 or null")
    mode = lineage["mode"]
    if mode == "evaluation_only" and (
            source_run_id is None or source_sha is None):
        raise MatrixError(f"{label}.evaluation_only requires source checkpoint identity")
    if mode != "evaluation_only" and (source_run_id is not None or source_sha is not None):
        raise MatrixError(f"{label}.{mode} cannot name a source checkpoint")
    return lineage


def _validate_acceptance(value: Any) -> dict[str, Any]:
    acceptance = _expect_keys(value, {
        "min_delivered_packets", "min_multisat_deliveries",
        "require_data_isl", "require_control_delivery",
    }, "acceptance")
    for key in ("min_delivered_packets", "min_multisat_deliveries"):
        if not isinstance(acceptance[key], int) or isinstance(acceptance[key], bool) \
                or acceptance[key] < 0:
            raise MatrixError(f"acceptance.{key} must be a non-negative integer")
    for key in ("require_data_isl", "require_control_delivery"):
        if not isinstance(acceptance[key], bool):
            raise MatrixError(f"acceptance.{key} must be bool")
    return acceptance


def _validate_analysis(value: Any) -> dict[str, Any]:
    analysis = _expect_keys(value, {
        "analysis_id", "primary_metric", "estimand", "paired_by",
        "planned_contrasts",
    }, "analysis")
    _safe_id(analysis["analysis_id"], "analysis.analysis_id")
    for key in ("primary_metric", "estimand"):
        if not isinstance(analysis[key], str) or not analysis[key]:
            raise MatrixError(f"analysis.{key} must be a non-empty string")
    if not isinstance(analysis["paired_by"], list) or not analysis["paired_by"] \
            or any(not isinstance(x, str) or not x for x in analysis["paired_by"]):
        raise MatrixError("analysis.paired_by must be a non-empty string list")
    contrasts = analysis["planned_contrasts"]
    if not isinstance(contrasts, list) or not contrasts:
        raise MatrixError("analysis.planned_contrasts must be non-empty")
    for i, contrast in enumerate(contrasts):
        item = _expect_keys(contrast, {"name", "left_arm", "right_arm", "estimand"},
                            f"analysis.planned_contrasts[{i}]")
        _safe_id(item["name"], f"analysis.planned_contrasts[{i}].name")
        _safe_id(item["left_arm"], f"analysis.planned_contrasts[{i}].left_arm")
        _safe_id(item["right_arm"], f"analysis.planned_contrasts[{i}].right_arm")
        if not isinstance(item["estimand"], str) or not item["estimand"]:
            raise MatrixError(f"analysis.planned_contrasts[{i}].estimand must be a string")
    return analysis


def _validate_claim_boundary(value: Any) -> dict[str, Any]:
    boundary = _expect_keys(value, {"can_claim", "cannot_claim"}, "claim_boundary")
    for key in ("can_claim", "cannot_claim"):
        if not isinstance(boundary[key], list) or any(
                not isinstance(x, str) or not x for x in boundary[key]):
            raise MatrixError(f"claim_boundary.{key} must be a string list")
    return boundary


def validate_request(request: Any) -> dict[str, Any]:
    request = _expect_keys(request, {
        "schema", "experiment_id", "runtime_kind", "work_finalization",
        "common_config", "arms", "cells", "acceptance", "analysis",
        "claim_boundary",
    }, "matrix request")
    if request["schema"] != MATRIX_REQUEST_SCHEMA:
        raise MatrixError(f"request.schema must be {MATRIX_REQUEST_SCHEMA!r}")
    experiment_id = request["experiment_id"]
    if not isinstance(experiment_id, str) or EXPERIMENT_ID.fullmatch(experiment_id) is None:
        raise MatrixError("experiment_id must be a safe EXP-* identifier")
    if request["runtime_kind"] != governance.RUNTIME_KIND:
        raise MatrixError("runtime_kind must be 'leo_sim_v2'")
    finalization = request["work_finalization"]
    if (not isinstance(finalization, str) or not finalization.startswith("CODE/work/")
            or not finalization.endswith("/finalization.json")
            or ".." in Path(finalization).parts):
        raise MatrixError("work_finalization must be a safe CODE/work/.../finalization.json path")
    _mapping(request["common_config"], "common_config")
    arms = request["arms"]
    if not isinstance(arms, list) or not arms:
        raise MatrixError("arms must be a non-empty list")
    arm_ids: set[str] = set()
    normalized_arms: list[dict[str, Any]] = []
    for i, raw in enumerate(arms):
        arm = _expect_keys(raw, {"arm_id", "config_overrides"}, f"arms[{i}]")
        arm_id = _safe_id(arm["arm_id"], f"arms[{i}].arm_id")
        if arm_id in arm_ids:
            raise MatrixError(f"duplicate arm_id: {arm_id}")
        arm_ids.add(arm_id)
        normalized_arms.append({"arm_id": arm_id,
                                "config_overrides": _mapping(
                                    arm["config_overrides"],
                                    f"arms[{i}].config_overrides")})
    cells = request["cells"]
    if not isinstance(cells, list) or not cells:
        raise MatrixError("cells must be a non-empty list")
    run_ids: set[str] = set()
    normalized_cells: list[dict[str, Any]] = []
    for i, raw in enumerate(cells):
        cell = _expect_keys(raw, {
            "run_id", "arm_id", "phase", "trace_seed", "learning_seed",
            "pairing_key", "config_overrides", "checkpoint_lineage",
        }, f"cells[{i}]")
        run_id = _safe_id(cell["run_id"], f"cells[{i}].run_id")
        if run_id in run_ids:
            raise MatrixError(f"duplicate run_id: {run_id}")
        run_ids.add(run_id)
        arm_id = _safe_id(cell["arm_id"], f"cells[{i}].arm_id")
        if arm_id not in arm_ids:
            raise MatrixError(f"unknown arm_id: {arm_id}")
        if cell["phase"] not in PHASES:
            raise MatrixError(f"cells[{i}].phase is invalid")
        trace_seed = _nonnegative_int(cell["trace_seed"], f"cells[{i}].trace_seed")
        learning_seed = cell["learning_seed"]
        if learning_seed is not None:
            learning_seed = _nonnegative_int(learning_seed, f"cells[{i}].learning_seed")
        if not isinstance(cell["pairing_key"], str) or not cell["pairing_key"] \
                or SAFE_ID.fullmatch(cell["pairing_key"]) is None:
            raise MatrixError(f"cells[{i}].pairing_key must be a safe identifier")
        lineage = _validate_checkpoint_lineage(
            cell["checkpoint_lineage"], f"cells[{i}].checkpoint_lineage")
        normalized_cells.append({
            "run_id": run_id, "arm_id": arm_id,
            "phase": _normalize_phase(cell["phase"]),
            "trace_seed": trace_seed, "learning_seed": learning_seed,
            "pairing_key": cell["pairing_key"],
            "config_overrides": _mapping(cell["config_overrides"],
                                           f"cells[{i}].config_overrides"),
            "checkpoint_lineage": lineage,
        })
    _validate_acceptance(request["acceptance"])
    _validate_analysis(request["analysis"])
    _validate_claim_boundary(request["claim_boundary"])
    for contrast in request["analysis"]["planned_contrasts"]:
        if contrast["left_arm"] not in arm_ids or contrast["right_arm"] not in arm_ids:
            raise MatrixError("analysis contrast references unknown arm")
        if contrast["left_arm"] == contrast["right_arm"]:
            raise MatrixError("analysis contrast must compare distinct arms")
    if not any(c["arm_id"] == request["analysis"]["planned_contrasts"][0]["left_arm"]
               for c in normalized_cells):
        raise MatrixError("analysis contrast left arm has no planned cell")
    return {
        **request,
        "arms": normalized_arms,
        "cells": normalized_cells,
    }


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def _set_if_absent_or_equal(tree: dict[str, Any], group: str, key: str,
                            expected: Any, label: str) -> None:
    values = tree.setdefault(group, {})
    if not isinstance(values, dict):
        raise MatrixError(f"{label} crosses a scalar")
    actual = values.get(key)
    if actual is not None and actual != expected:
        raise MatrixError(f"{label} conflicts with explicit seed")
    values[key] = expected


def _checkpoint_for_config(config: dict[str, Any], lineage: dict[str, Any],
                           phase: str, learning_seed: int | None,
                           label: str) -> None:
    phase = _normalize_phase(phase)
    learning = config["learning"]
    algorithm = learning["algorithm"]
    if phase == "non_learning":
        if (algorithm != "none" or lineage["mode"] != "not_applicable"
                or learning_seed is not None or learning.get("seed") is not None):
            raise MatrixError(f"{label}: non_learning phase has learning configuration")
        return
    if algorithm == "none":
        raise MatrixError(f"{label}: learning phase requires a learning algorithm")
    if learning_seed is None:
        raise MatrixError(f"{label}: learning phase requires learning_seed")
    expected_phase = "train" if phase == "training" else "eval"
    if learning["mode"] != expected_phase:
        raise MatrixError(f"{label}: phase does not match learning.mode")
    expected_lineage = "new_training" if phase == "training" else "evaluation_only"
    if lineage["mode"] != expected_lineage:
        raise MatrixError(f"{label}: phase/checkpoint lineage mismatch")


def _control_projection(resolved_config: dict[str, Any]) -> dict[str, Any]:
    projection = copy.deepcopy(resolved_config)
    projection["scenario"].pop("seed", None)
    projection["learning"].pop("seed", None)
    for key in ("checkpoint_path", "checkpoint_sha256", "checkpoint_metadata_sha256"):
        projection["learning"].pop(key, None)
    return projection


def _canonical_run_id(experiment_id: str, cell: dict[str, Any]) -> str:
    suffix = f"s{cell['trace_seed']}"
    if cell["learning_seed"] is not None:
        suffix += f"-l{cell['learning_seed']}"
    return f"{experiment_id}-{cell['arm_id']}-{suffix}"


def _resolve_cells(request: dict[str, Any], project_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    validated = validate_request(request)
    arm_by_id = {arm["arm_id"]: arm for arm in validated["arms"]}
    common_resolved = governance.build_run_intent({
        "runtime_kind": governance.RUNTIME_KIND,
        "config": validated["common_config"],
    }, project_root=project_root)
    controlled_signature = canonical_sha(_control_projection(
        common_resolved["resolved"]["config"]))
    rows: list[dict[str, Any]] = []
    for index, cell in enumerate(validated["cells"]):
        if _canonical_run_id(validated["experiment_id"], cell) != cell["run_id"]:
            raise MatrixError(f"cells[{index}] run_id identity mismatch")
        merged = _deep_merge(validated["common_config"],
                             arm_by_id[cell["arm_id"]]["config_overrides"])
        merged = _deep_merge(merged, cell["config_overrides"])
        _set_if_absent_or_equal(merged, "scenario", "seed", cell["trace_seed"],
                                f"cells[{index}].trace_seed")
        if cell["learning_seed"] is not None:
            _set_if_absent_or_equal(merged, "learning", "seed",
                                    cell["learning_seed"],
                                    f"cells[{index}].learning_seed")
        intent = governance.build_run_intent({
            "runtime_kind": governance.RUNTIME_KIND,
            "config": merged,
        }, project_root=project_root)
        _checkpoint_for_config(intent["resolved"]["config"],
                               cell["checkpoint_lineage"], cell["phase"],
                               cell["learning_seed"], f"cell {cell['run_id']}")
        rows.append({
            **cell,
            "runtime_kind": governance.RUNTIME_KIND,
            "config": intent["resolved"],
            "config_sha256": intent["config_sha256"],
            "trace_identity_sha256": intent["trace_identity_sha256"],
            "input_sha256": intent["input_sha256"],
            "code_sha256": intent["code_sha256"],
            "execution_chain_sha256": governance.execution_chain_sha256(),
            "controlled_signature": controlled_signature,
            "config_path": f"resolved/{cell['run_id']}.leo-sim.yaml",
        })
    by_pair: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_pair.setdefault(row["pairing_key"], []).append(row)
    for pairing_key, group in by_pair.items():
        if len({row["arm_id"] for row in group}) != len(group):
            raise MatrixError(f"pairing_key {pairing_key} repeats an arm")
        identity = {
            (row["phase"], row["trace_seed"], row["learning_seed"],
             json.dumps(row["checkpoint_lineage"], sort_keys=True),
             row["controlled_signature"])
            for row in group
        }
        if len(identity) != 1:
            raise MatrixError(f"pairing_key {pairing_key} has inconsistent paired control or learning identity")
    return validated, rows


def _write_json(path: Path, value: Any) -> None:
    if path.is_symlink():
        raise MatrixError(f"refusing symbolic output artifact: {path}")
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2,
                               sort_keys=True) + "\n", encoding="utf-8")


def _artifact_hashes(out_dir: Path, paths: list[str]) -> dict[str, str]:
    return {raw: hashlib.sha256((out_dir / raw).read_bytes()).hexdigest()
            for raw in sorted(paths)}


def _analysis_document(request: dict[str, Any], manifest_sha: str,
                       request_sha: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema": MATRIX_ANALYSIS_SCHEMA,
        "runtime_kind": governance.RUNTIME_KIND,
        "experiment_id": request["experiment_id"],
        "analysis": request["analysis"],
        "claim_boundary": request["claim_boundary"],
        "planned_run_ids": [row["run_id"] for row in rows],
        "planned_cells": [
            {key: row[key] for key in (
                "run_id", "arm_id", "phase", "trace_seed", "learning_seed",
                "pairing_key", "config_sha256", "trace_identity_sha256",
                "input_sha256", "controlled_signature")}
            for row in rows
        ],
        "request_sha256": request_sha,
        "matrix_manifest_sha256": manifest_sha,
        "status": "WAITING_FOR_VERIFIED_RUNS",
    }


def compile_matrix_experiment(request_path: Path, out_dir: Path,
                              project_root: Path | None = None) -> dict[str, Any]:
    request_path = Path(request_path)
    out_dir = Path(out_dir)
    project_root = Path(project_root or request_path.parent).resolve()
    if request_path.is_symlink() or not request_path.is_file():
        raise MatrixError(f"request is not a regular file: {request_path}")
    try:
        request = json.loads(request_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MatrixError(f"request unreadable: {exc}") from exc
    validated, rows = _resolve_cells(request, project_root)
    if out_dir.is_symlink():
        raise MatrixError("output directory may not be symbolic")
    if out_dir.exists():
        if not out_dir.is_dir():
            raise MatrixError("output path is not a directory")
        if any(out_dir.iterdir()):
            raise MatrixError("output directory must be empty")
    else:
        out_dir.mkdir(parents=True)
    (out_dir / "resolved").mkdir()
    _write_json(out_dir / "request.json", validated)
    request_sha = hashlib.sha256((out_dir / "request.json").read_bytes()).hexdigest()
    for row in rows:
        config_path = out_dir / row["config_path"]
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps({
            "config_version": row["config"]["version"],
            **row["config"]["config"],
        }, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest = {
        "schema": MATRIX_MANIFEST_SCHEMA,
        "runtime_kind": governance.RUNTIME_KIND,
        "experiment_id": validated["experiment_id"],
        "request_sha256": request_sha,
        "common_config_sha256": canonical_sha(validated["common_config"]),
        "arms": validated["arms"],
        "cells": [{key: row[key] for key in (
            "run_id", "runtime_kind", "arm_id", "phase", "trace_seed",
            "learning_seed", "pairing_key", "config_overrides",
            "checkpoint_lineage", "config_path", "config_sha256",
            "trace_identity_sha256", "input_sha256", "code_sha256",
            "execution_chain_sha256", "controlled_signature")}
                   for row in rows],
        "execution_authorized": False,
    }
    _write_json(out_dir / "run-manifest.json", manifest)
    manifest_sha = hashlib.sha256((out_dir / "run-manifest.json").read_bytes()).hexdigest()
    analysis = _analysis_document(validated, manifest_sha, request_sha, rows)
    _write_json(out_dir / "analysis-request.json", analysis)
    runbook_lines = [
        f"# {validated['experiment_id']}", "",
        "Runtime: `leo_sim_v2`; compilation only, no run is launched.", "",
        "Each cell is an independent controlled command after review, authorization, and clean deployment:", "",
    ]
    for row in rows:
        runbook_lines.extend([
            f"## {row['run_id']}", "", "```bash",
            "CODE/scripts/remote/run-remote.sh \\",
            "  --runtime-kind leo_sim_v2 \\",
            f"  --config EXPERIMENTS/{validated['experiment_id']}/{row['config_path']} \\",
            f"  --authorization EXPERIMENTS/{validated['experiment_id']}/authorization.json \\",
            f"  --session {row['run_id'].lower()}", "```", "",
        ])
    (out_dir / "RUNBOOK.md").write_text("\n".join(runbook_lines), encoding="utf-8")
    bound_paths = ["request.json", "run-manifest.json", "analysis-request.json",
                   "RUNBOOK.md", *(row["config_path"] for row in rows)]
    report = {
        "schema": governance.COMPILE_REPORT_SCHEMA,
        "status": "COMPILED_REVIEW_REQUIRED",
        "runtime_kind": governance.RUNTIME_KIND,
        "experiment_id": validated["experiment_id"],
        "errors": [],
        "request_sha256": request_sha,
        "execution_authorized": False,
        "launcher_generated": False,
        "artifact_hashes": _artifact_hashes(out_dir, bound_paths),
    }
    _write_json(out_dir / "compile-report.json", report)
    return report


def verify_compiled_matrix(root: Path, experiment_dir: Path) -> tuple[str, dict[str, str], list[dict[str, Any]]]:
    """Recompute all matrix identities without trusting compiled documents."""
    root = Path(root).resolve()
    experiment_dir = Path(experiment_dir).resolve()
    docs = {}
    for name in ("request.json", "compile-report.json", "run-manifest.json",
                 "analysis-request.json"):
        path = experiment_dir / name
        if path.is_symlink() or not path.is_file():
            raise MatrixError(f"missing compiled matrix artifact: {name}")
        docs[name] = json.loads(path.read_text(encoding="utf-8"))
    runbook = experiment_dir / "RUNBOOK.md"
    if runbook.is_symlink() or not runbook.is_file():
        raise MatrixError("missing compiled matrix artifact: RUNBOOK.md")
    request = validate_request(docs["request.json"])
    report = docs["compile-report.json"]
    manifest = docs["run-manifest.json"]
    analysis = docs["analysis-request.json"]
    request_sha = hashlib.sha256((experiment_dir / "request.json").read_bytes()).hexdigest()
    if set(report) != {
            "schema", "status", "runtime_kind", "experiment_id", "errors",
            "request_sha256", "execution_authorized", "launcher_generated",
            "artifact_hashes"}:
        raise MatrixError("matrix compile report has an invalid field set")
    if (report["schema"] != governance.COMPILE_REPORT_SCHEMA
            or report["status"] != "COMPILED_REVIEW_REQUIRED"
            or report["errors"] != [] or report["request_sha256"] != request_sha
            or report["execution_authorized"] is not False
            or report["launcher_generated"] is not False):
        raise MatrixError("matrix compile report is not a clean review-required build")
    if manifest.get("schema") != MATRIX_MANIFEST_SCHEMA or \
            manifest.get("runtime_kind") != governance.RUNTIME_KIND or \
            manifest.get("experiment_id") != request["experiment_id"] or \
            manifest.get("request_sha256") != request_sha or \
            manifest.get("execution_authorized") is not False or \
            manifest.get("common_config_sha256") != canonical_sha(request["common_config"]) or \
            manifest.get("arms") != request["arms"]:
        raise MatrixError("matrix manifest identity/state mismatch")
    expected_request, rows = _resolve_cells(request, root)
    expected_cells = [{key: row[key] for key in (
        "run_id", "runtime_kind", "arm_id", "phase", "trace_seed",
        "learning_seed", "pairing_key", "config_overrides", "checkpoint_lineage",
        "config_path", "config_sha256", "trace_identity_sha256", "input_sha256",
        "code_sha256", "execution_chain_sha256", "controlled_signature")}
                     for row in rows]
    if set(manifest) != {"schema", "runtime_kind", "experiment_id", "request_sha256",
                         "common_config_sha256", "arms", "cells", "execution_authorized"}:
        raise MatrixError("matrix manifest has an invalid field set")
    if manifest["cells"] != expected_cells:
        raise MatrixError("matrix manifest cells do not derive from request")
    expected_manifest_sha = hashlib.sha256((experiment_dir / "run-manifest.json").read_bytes()).hexdigest()
    expected_analysis = _analysis_document(request, expected_manifest_sha, request_sha, rows)
    if analysis != expected_analysis:
        raise MatrixError("matrix analysis request does not bind the exact cohort")
    paths = ["request.json", "run-manifest.json", "analysis-request.json", "RUNBOOK.md",
             *(row["config_path"] for row in rows)]
    expected_hashes = _artifact_hashes(experiment_dir, paths)
    if report["artifact_hashes"] != expected_hashes:
        raise MatrixError("matrix compile report artifact hash map is incomplete or stale")
    for row in rows:
        config_path = experiment_dir / row["config_path"]
        if config_path.is_symlink() or not config_path.is_file():
            raise MatrixError(f"matrix config is missing or symbolic: {row['run_id']}")
        resolved = config_mod.load_config_file(str(config_path))
        if resolved != row["config"]:
            raise MatrixError(f"matrix resolved config changed: {row['run_id']}")
    artifact_hashes = {
        str((experiment_dir / raw).resolve().relative_to(root)): digest
        for raw, digest in expected_hashes.items()
    }
    # The report cannot hash itself recursively, but authorization must still
    # bind the report file as an artifact after recomputing its embedded map.
    report_relative = str((experiment_dir / "compile-report.json").resolve().relative_to(root))
    artifact_hashes[report_relative] = hashlib.sha256(
        (experiment_dir / "compile-report.json").read_bytes()).hexdigest()
    authorized = [{key: row[key] for key in (
        "run_id", "runtime_kind", "arm_id", "phase", "trace_seed",
        "learning_seed", "pairing_key", "config_path", "config_sha256",
        "trace_identity_sha256", "input_sha256", "code_sha256",
        "execution_chain_sha256", "controlled_signature", "checkpoint_lineage")}
                  for row in rows]
    if len(authorized) != len(request["cells"]) or \
            {row["run_id"] for row in authorized} != {cell["run_id"] for cell in request["cells"]}:
        raise MatrixError("authorized matrix cohort is not exactly the planned cells")
    return request["experiment_id"], artifact_hashes, authorized
