#!/usr/bin/env python3
"""Fail-closed paired analysis for compiled leo_sim experiment artifacts.

The analyzer is deliberately small and boring.  It does not infer run
identity from directory names, fill missing metrics, or turn a successful
process exit into evidence.  Every run is admitted only after the compiled
manifest, run metadata, config bytes, artifact manifest and summary metrics
agree.  The persisted analysis manifest is then a reproducible claim-bound
artifact for :mod:`PAPER.eligible_claims`.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import sys
from pathlib import Path
from typing import Any, Iterable


ANALYSIS_SCHEMA = "analysis-request/v2"
MANIFEST_SCHEMA = "experiment-run-manifest/v2"
OUTPUT_SCHEMA = "analysis-manifest/v1"
RECEIPT_SCHEMA = "leo-effective-receipt/v1"
ARTIFACT_SCHEMA = "artifact-manifest/v1"


def canonical_sha(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _read_json(path: Path) -> Any:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"missing or symbolic JSON artifact: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"unreadable JSON artifact {path}: {exc}") from exc


def _safe_child(root: Path, raw: str, label: str) -> Path:
    if not isinstance(raw, str) or not raw or Path(raw).is_absolute():
        raise ValueError(f"{label} must be a non-empty relative path")
    root = root.resolve()
    candidate = root / raw
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError) as exc:
        raise ValueError(f"{label} escapes its root or is missing: {raw}") from exc
    # Every component is checked.  A symlink that happens to resolve inside
    # the root is still not a reproducible run artifact.
    cursor = root
    for part in Path(raw).parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise ValueError(f"{label} contains a symbolic link: {raw}")
    return resolved


def _safe_artifact(root: Path, raw: str, label: str) -> Path:
    return _safe_child(root, raw, label)


def _finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def _load_metrics(path: Path, required: Iterable[str]) -> dict[str, float]:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"summary metrics missing or symbolic: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ["metric", "value"]:
            raise ValueError("summary_metrics.csv must have exactly metric,value columns")
        metrics: dict[str, float] = {}
        for row_number, row in enumerate(reader, start=2):
            metric = row.get("metric")
            raw_value = row.get("value")
            if not isinstance(metric, str) or not metric.strip():
                raise ValueError(f"summary metrics row {row_number} has an empty metric")
            if metric in metrics:
                raise ValueError(f"summary metrics contains duplicate metric: {metric}")
            try:
                value = float(raw_value)  # type: ignore[arg-type]
            except (TypeError, ValueError) as exc:
                raise ValueError(f"summary metric {metric} is not numeric") from exc
            if not math.isfinite(value):
                raise ValueError(f"summary metric {metric} is not finite")
            metrics[metric] = value
    missing = sorted(set(required) - set(metrics))
    if missing:
        raise ValueError(f"summary metrics missing required fields: {missing}")
    return metrics


def _artifact_entries(run_dir: Path, artifact_manifest: dict[str, Any], required: list[str]) -> list[dict[str, Any]]:
    if artifact_manifest.get("schema") != ARTIFACT_SCHEMA:
        raise ValueError("artifact manifest schema mismatch")
    entries = artifact_manifest.get("artifacts")
    if not isinstance(entries, list):
        raise ValueError("artifact manifest artifacts must be a list")
    if artifact_manifest.get("required_artifacts") != required:
        raise ValueError("artifact manifest required set differs from compiled config")
    seen: set[str] = set()
    checked: list[dict[str, Any]] = []
    for item in entries:
        if not isinstance(item, dict) or set(item) not in ({"path", "size", "sha256"}, {"path", "size", "sha256", "schema"}):
            raise ValueError("artifact manifest entry must contain path,size,sha256")
        raw = item["path"]
        if not isinstance(raw, str) or raw in seen or raw == "artifact_manifest.json":
            raise ValueError("artifact manifest has duplicate, invalid or self entry")
        seen.add(raw)
        path = _safe_artifact(run_dir, raw, "run artifact")
        if not isinstance(item["size"], int) or item["size"] < 0:
            raise ValueError(f"artifact size is invalid: {raw}")
        digest = item["sha256"]
        if not isinstance(digest, str) or len(digest) != 64 or file_sha256(path) != digest:
            raise ValueError(f"artifact hash mismatch: {raw}")
        if path.stat().st_size != item["size"]:
            raise ValueError(f"artifact size mismatch: {raw}")
        checked.append({"path": raw, "size": item["size"], "sha256": digest})
    expected = set(required) - {"artifact_manifest.json"}
    if seen != expected:
        raise ValueError(f"artifact manifest does not cover exact required set: missing={sorted(expected-seen)} extra={sorted(seen-expected)}")
    return checked


def _planned_row(manifest: dict[str, Any], run_id: str) -> dict[str, Any]:
    rows = manifest.get("planned_runs")
    if not isinstance(rows, list):
        raise ValueError("run manifest planned_runs must be a list")
    matches = [row for row in rows if isinstance(row, dict) and row.get("run_id") == run_id]
    if len(matches) != 1:
        raise ValueError(f"run id is not unique in planned cohort: {run_id}")
    return matches[0]


def _verify_run(root: Path, manifest: dict[str, Any], run_id: str, raw_path: Path, required_metrics: list[str]) -> dict[str, Any]:
    run_dir = raw_path.resolve()
    if run_dir.is_symlink() or not run_dir.is_dir():
        raise ValueError(f"run directory is missing or symbolic: {raw_path}")
    row = _planned_row(manifest, run_id)
    meta_path = _safe_child(run_dir, "run_trace/run_meta.json", "run metadata")
    config_path = _safe_child(run_dir, "config_used.json", "config used")
    artifact_path = _safe_child(run_dir, "artifact_manifest.json", "artifact manifest")
    meta = _read_json(meta_path)
    config = _read_json(config_path)
    artifacts = _read_json(artifact_path)
    if not isinstance(meta, dict) or not isinstance(config, dict) or not isinstance(artifacts, dict):
        raise ValueError(f"run {run_id} identity files must be JSON objects")
    config_sha = canonical_sha(config)
    if meta.get("requested_run_id") != run_id:
        raise ValueError(f"run {run_id} requested_run_id mismatch")
    if meta.get("config_canonical_sha256") != config_sha:
        raise ValueError(f"run {run_id} config hash mismatch in run_meta")
    if row.get("config_sha256") != config_sha:
        raise ValueError(f"run {run_id} config hash differs from run manifest")
    provenance = config.get("provenance")
    if not isinstance(provenance, dict):
        raise ValueError(f"run {run_id} lacks config provenance")
    for key in ("run_id", "arm_id", "seed"):
        if provenance.get(key) != row.get(key):
            raise ValueError(f"run {run_id} provenance {key} differs from run manifest")
    if "controlled_signature" in provenance and provenance.get("controlled_signature") != row.get("controlled_signature"):
        raise ValueError(f"run {run_id} provenance controlled_signature differs from run manifest")
    if provenance.get("experiment_id") != manifest.get("experiment_id"):
        raise ValueError(f"run {run_id} experiment identity mismatch")
    scenario = manifest.get("scenario_identity")
    scenario_sha = canonical_sha(scenario)
    if provenance.get("scenario_identity") != scenario:
        raise ValueError(f"run {run_id} scenario identity mismatch")
    if meta.get("scenario_identity_sha256") not in (None, scenario_sha):
        raise ValueError(f"run {run_id} scenario identity hash mismatch")
    if meta.get("natural_end") is not True or meta.get("interrupted") is not False:
        raise ValueError(f"run {run_id} did not end naturally")
    receipt = meta.get("effective_receipt")
    if not isinstance(receipt, dict) or receipt.get("schema") != RECEIPT_SCHEMA or receipt.get("research_eligible") is not True or receipt.get("mismatches") != []:
        raise ValueError(f"run {run_id} effective receipt is not eligible")
    required = provenance.get("required_artifacts")
    if not isinstance(required, list) or any(not isinstance(item, str) for item in required):
        raise ValueError(f"run {run_id} required_artifacts is invalid")
    checked_artifacts = _artifact_entries(run_dir, artifacts, required)
    metrics_path = _safe_child(run_dir, "experiment_bundle/summary_metrics.csv", "summary metrics")
    metrics = _load_metrics(metrics_path, required_metrics)
    return {
        "run_id": run_id,
        "arm_id": row.get("arm_id"),
        "seed": row.get("seed"),
        "config_sha256": config_sha,
        "controlled_signature": row.get("controlled_signature"),
        "scenario_identity": scenario_sha,
        "metrics": metrics,
        "run_path": run_dir,
        "bound_artifacts": [
            {"path": str(path.relative_to(root.resolve())), "sha256": file_sha256(path)}
            for path in (meta_path, config_path, artifact_path, metrics_path)
        ] + [
            {"path": str((run_dir / item["path"]).relative_to(root.resolve())), "sha256": item["sha256"]}
            for item in checked_artifacts
        ],
    }


def _pair_key(row: dict[str, Any], paired_by: list[str]) -> tuple[Any, ...]:
    values = {
        "seed": row["seed"],
        "scenario_identity": row["scenario_identity"],
        "controlled_signature": row["controlled_signature"],
    }
    unknown = sorted(set(paired_by) - set(values))
    if unknown:
        raise ValueError(f"unsupported paired_by fields: {unknown}")
    return tuple(values[key] for key in paired_by)


def _bootstrap(values: list[float], seed: int, draws: int = 4000) -> tuple[float | None, float | None, str]:
    if len(values) < 2:
        return None, None, "NOT_ESTIMATED_LT2_PAIRS"
    rng = random.Random(seed)
    means: list[float] = []
    for _ in range(draws):
        means.append(sum(values[rng.randrange(len(values))] for _ in values) / len(values))
    means.sort()
    low = means[max(0, int(0.025 * draws) - 1)]
    high = means[min(draws - 1, int(0.975 * draws))]
    return low, high, "BOOTSTRAP_95"


def execute(root: Path, analysis: dict[str, Any], run_manifest: dict[str, Any], run_entries: list[tuple[str, Path]], out_dir: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    results: list[dict[str, Any]] = []
    if analysis.get("schema") != ANALYSIS_SCHEMA:
        errors.append("analysis request schema mismatch")
    if run_manifest.get("schema") != MANIFEST_SCHEMA:
        errors.append("run manifest schema mismatch")
    if analysis.get("experiment_id") != run_manifest.get("experiment_id"):
        errors.append("analysis and run manifest experiment_id mismatch")
    planned = run_manifest.get("planned_runs")
    if not isinstance(planned, list) or any(not isinstance(row, dict) for row in planned):
        errors.append("run manifest planned_runs is invalid")
        planned = []
    planned_ids = [row.get("run_id") for row in planned]
    if len(planned_ids) != len(set(planned_ids)):
        errors.append("run manifest contains duplicate run ids")
    supplied_ids = [run_id for run_id, _ in run_entries]
    if len(supplied_ids) != len(set(supplied_ids)):
        errors.append("analysis invocation contains duplicate run ids")
    if set(supplied_ids) != set(planned_ids) or supplied_ids != planned_ids:
        errors.append("analysis run cohort/order does not exactly match run manifest")
    primary = analysis.get("primary_metric")
    secondary = analysis.get("secondary_metrics", [])
    if not isinstance(primary, str) or not primary:
        errors.append("analysis primary_metric is invalid")
        primary = ""
    if not isinstance(secondary, list) or any(not isinstance(item, str) for item in secondary):
        errors.append("analysis secondary_metrics is invalid")
        secondary = []
    required_metrics = [primary, *secondary] if primary else list(secondary)
    for run_id, path in run_entries:
        if errors and set(supplied_ids) != set(planned_ids):
            break
        try:
            results.append(_verify_run(root, run_manifest, run_id, path, required_metrics))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"{run_id}: {exc}")
    pair_by = analysis.get("preregistration", {}).get("paired_by", []) if isinstance(analysis.get("preregistration"), dict) else []
    if not isinstance(pair_by, list) or not pair_by:
        errors.append("analysis preregistration paired_by is missing")
        pair_by = []
    grouped: dict[tuple[Any, ...], dict[str, dict[str, Any]]] = {}
    for row in results:
        try:
            key = _pair_key(row, pair_by)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        arm = row["arm_id"]
        if arm in grouped.setdefault(key, {}):
            errors.append(f"duplicate run for pairing key {key} and arm {arm}")
        grouped[key][arm] = row
    contrasts = analysis.get("preregistration", {}).get("planned_contrasts", []) if isinstance(analysis.get("preregistration"), dict) else []
    if not isinstance(contrasts, list) or not contrasts:
        errors.append("analysis preregistration planned_contrasts is missing")
        contrasts = []
    output_contrasts: list[dict[str, Any]] = []
    for contrast in contrasts:
        if not isinstance(contrast, dict):
            errors.append("planned contrast is not an object")
            continue
        name = contrast.get("name")
        left = contrast.get("left_arm")
        right = contrast.get("right_arm")
        diffs: list[float] = []
        for key, arms in grouped.items():
            if left not in arms or right not in arms:
                continue
            diffs.append(arms[left]["metrics"][primary] - arms[right]["metrics"][primary])
        if not diffs:
            errors.append(f"contrast {name} has no complete pairs")
        low, high, uncertainty = _bootstrap(diffs, int(canonical_sha({"experiment_id": run_manifest.get("experiment_id"), "contrast": name})[:16], 16))
        output_contrasts.append({
            "name": name,
            "left_arm": left,
            "right_arm": right,
            "metric": primary,
            "n_pairs": len(diffs),
            "differences": diffs,
            "mean_difference": (sum(diffs) / len(diffs)) if diffs else None,
            "median_difference": (sorted(diffs)[len(diffs) // 2] if diffs and len(diffs) % 2 else ((sorted(diffs)[len(diffs)//2 - 1] + sorted(diffs)[len(diffs)//2]) / 2 if diffs else None)),
            "ci95_low": low,
            "ci95_high": high,
            "uncertainty_status": uncertainty,
        })
    input_paths: dict[str, str] = {}
    if root.exists():
        # The caller adds the exact request/manifest paths in write_outputs;
        # execute itself only binds the run artifacts and current analyzer.
        code_path = (root / "ANALYSIS" / "paired_analysis.py").resolve()
        if code_path.is_file():
            input_paths[str(code_path.relative_to(root.resolve()))] = file_sha256(code_path)
    manifest = {
        "schema": OUTPUT_SCHEMA,
        "status": "VERIFIED" if not errors else "BLOCKED",
        "errors": sorted(set(errors)),
        "experiment_id": run_manifest.get("experiment_id"),
        "analysis_id": analysis.get("analysis_id"),
        "primary_metric": primary,
        "paired_by": pair_by,
        "verified_run_ids": [row["run_id"] for row in results],
        "bound_run_artifacts": [item for row in results for item in row["bound_artifacts"]],
        "planned_contrasts": output_contrasts,
        "input_hashes": input_paths,
        "claim_boundary": {"cannot_conclude": analysis.get("cannot_conclude", [])},
    }
    return manifest, results, sorted(set(errors))


def _write_summary(path: Path, manifest: dict[str, Any]) -> None:
    rows = [
        ["contrast", "metric", "n_pairs", "mean_difference", "median_difference", "ci95_low", "ci95_high", "uncertainty_status"]
    ]
    for row in manifest.get("planned_contrasts", []):
        rows.append([row.get(key) for key in ("name", "metric", "n_pairs", "mean_difference", "median_difference", "ci95_low", "ci95_high", "uncertainty_status")])
    with path.open("w", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerows(rows)


def _write_report(path: Path, manifest: dict[str, Any]) -> None:
    lines = [
        "# Paired analysis report",
        "",
        f"- status: `{manifest.get('status')}`",
        f"- experiment: `{manifest.get('experiment_id')}`",
        f"- primary metric: `{manifest.get('primary_metric')}`",
        f"- verified runs: `{len(manifest.get('verified_run_ids', []))}`",
        "",
        "This report is generated from the persisted analysis manifest. It is not a paper claim by itself.",
    ]
    if manifest.get("errors"):
        lines.extend(["", "## Errors", "", *[f"- {item}" for item in manifest["errors"]]])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs(root: Path, out_dir: Path, manifest: dict[str, Any], results: list[dict[str, Any]]) -> None:
    root = root.resolve()
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    _write_summary(out_dir / "summary.csv", manifest)
    _write_report(out_dir / "report.md", manifest)
    code_path = Path(__file__).resolve()
    (out_dir / "analysis-code.py").write_bytes(code_path.read_bytes())
    # Persist the exact input bindings needed to recompute this output.  The
    # request and run-manifest paths are supplied by execute_main through the
    # private keys below and never accepted from untrusted report text.
    persisted = dict(manifest)
    # ``inputs`` is the public, paper-facing name.  Keep input_hashes as an
    # internal-compatible alias so old callers can inspect the same binding.
    persisted["inputs"] = dict(persisted.get("input_hashes", {}))
    persisted["output_hashes"] = {
        "summary.csv": file_sha256(out_dir / "summary.csv"),
        "report.md": file_sha256(out_dir / "report.md"),
        "analysis-code.py": file_sha256(out_dir / "analysis-code.py"),
    }
    persisted["output_artifacts"] = [
        {"path": str((out_dir / name).relative_to(root.resolve())), "sha256": digest}
        for name, digest in persisted["output_hashes"].items()
    ]
    (out_dir / "analysis-manifest.json").write_bytes(_json_bytes(persisted))


def verify_persisted_analysis(root: Path, manifest_path: Path) -> tuple[bool, list[str]]:
    errors: list[str] = []
    try:
        root = root.resolve()
        manifest_path = manifest_path.resolve(strict=True)
        manifest_path.relative_to((root / "ANALYSIS").resolve())
        manifest = _read_json(manifest_path)
        if not isinstance(manifest, dict) or manifest.get("schema") != OUTPUT_SCHEMA:
            raise ValueError("analysis manifest schema mismatch")
        if manifest.get("status") != "VERIFIED" or manifest.get("errors") != []:
            raise ValueError("analysis manifest is not VERIFIED and empty-error")
        code = _safe_child(root, "ANALYSIS/paired_analysis.py", "analysis source")
        inputs = manifest.get("inputs")
        if not isinstance(inputs, dict) or inputs.get("ANALYSIS/paired_analysis.py") != file_sha256(code):
            raise ValueError("analysis source hash mismatch")
        if manifest.get("input_hashes") != inputs:
            raise ValueError("analysis input hash aliases differ")
        for raw, digest in inputs.items():
            path = _safe_child(root, raw, "analysis input")
            if not isinstance(digest, str) or file_sha256(path) != digest:
                raise ValueError(f"analysis input hash mismatch: {raw}")
        bound = manifest.get("bound_run_artifacts")
        if not isinstance(bound, list) or not bound:
            raise ValueError("analysis manifest has no bound run artifacts")
        for entry in bound:
            if not isinstance(entry, dict) or set(entry) != {"path", "sha256"}:
                raise ValueError("bound run artifact entry malformed")
            path = _safe_child(root, entry["path"], "bound run artifact")
            if file_sha256(path) != entry["sha256"]:
                raise ValueError(f"bound run artifact hash mismatch: {entry['path']}")
        for entry in manifest.get("output_artifacts", []):
            if not isinstance(entry, dict) or set(entry) != {"path", "sha256"}:
                raise ValueError("output artifact entry malformed")
            path = _safe_child(root, entry["path"], "analysis output")
            if file_sha256(path) != entry["sha256"]:
                raise ValueError(f"analysis output hash mismatch: {entry['path']}")
        output_dir = Path(manifest_path).relative_to(root).parent
        output_abs = root / output_dir
        code_output = _safe_child(root, str(output_dir / "analysis-code.py"), "analysis code snapshot")
        if code_output.read_bytes() != code.read_bytes():
            raise ValueError("analysis-code.py does not match current analyzer")
        summary = _safe_child(root, str(output_dir / "summary.csv"), "analysis summary")
        expected_summary = output_abs / ".expected-summary.csv"
        _write_summary(expected_summary, manifest)
        try:
            if summary.read_bytes() != expected_summary.read_bytes():
                raise ValueError("analysis summary does not match persisted contrasts")
        finally:
            expected_summary.unlink(missing_ok=True)
        report = _safe_child(root, str(output_dir / "report.md"), "analysis report")
        expected_report = output_abs / ".expected-report.md"
        _write_report(expected_report, manifest)
        try:
            if report.read_bytes() != expected_report.read_bytes():
                raise ValueError("analysis report does not match persisted manifest")
        finally:
            expected_report.unlink(missing_ok=True)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(str(exc))
    return not errors, errors


def _load_run_entries(raw: list[str]) -> list[tuple[str, Path]]:
    result: list[tuple[str, Path]] = []
    for item in raw:
        if "=" not in item:
            raise ValueError("--run must be RUN_ID=RESULT_DIRECTORY")
        run_id, raw_path = item.split("=", 1)
        if not run_id or not raw_path:
            raise ValueError("--run must have non-empty RUN_ID and path")
        result.append((run_id, Path(raw_path)))
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--analysis", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--run", action="append", default=[])
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        analysis = _read_json(args.analysis)
        run_manifest = _read_json(args.manifest)
        root = Path.cwd().resolve()
        manifest, results, errors = execute(root, analysis, run_manifest, _load_run_entries(args.run), args.out)
        manifest["input_hashes"].update({
            str(args.analysis.resolve().relative_to(root)): file_sha256(args.analysis.resolve()),
            str(args.manifest.resolve().relative_to(root)): file_sha256(args.manifest.resolve()),
        })
        write_outputs(root, args.out.resolve(), manifest, results)
        if errors:
            for error in errors:
                print(f"BLOCK: {error}", file=sys.stderr)
            return 1
        print(f"VERIFIED: {args.out / 'analysis-manifest.json'}")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
