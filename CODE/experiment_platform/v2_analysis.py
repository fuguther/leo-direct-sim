"""Evidence-bound analysis for the dedicated ``leo_sim_v2`` matrix runtime.

The historical paired analyzer consumes the legacy Gateway artifact layout.
V2 has a different, stricter result contract (receipt/ledgers/formal witness),
so this adapter verifies that contract directly and only then computes paired
metrics.  A VERIFIED analysis is still not a paper claim: ``claim-gate.json``
records the boundary and requires the normal independent claim-support/value
reviews before any claim can be promoted.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

from CODE.experiment_platform import authorize_experiment
from CODE.leo_sim import metrics as metrics_mod
from CODE.leo_sim import receipt as receipt_mod


SCHEMA = "leo-sim-v2-analysis/v1"
CLAIM_GATE_SCHEMA = "leo-sim-v2-claim-gate/v1"
MATRIX_SCHEMA = "leo-sim-experiment-matrix-manifest/v1"
ANALYSIS_SCHEMA = "leo-sim-matrix-analysis-request/v1"


class V2AnalysisError(ValueError):
    """A V2 result or analysis contract cannot be verified."""


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _read_json(path: Path) -> Any:
    if path.is_symlink() or not path.is_file():
        raise V2AnalysisError(f"missing or symbolic artifact: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise V2AnalysisError(f"unreadable JSON artifact {path}: {exc}") from exc


def _direct_result(results_root: Path, run_id: str) -> Path:
    if not isinstance(run_id, str) or not run_id or "/" in run_id or "\\" in run_id:
        raise V2AnalysisError(f"invalid run id: {run_id!r}")
    path = results_root / run_id
    if path.is_symlink() or not path.is_dir() or path.resolve() != path.absolute():
        raise V2AnalysisError(f"result must be a lexical direct directory: {run_id}")
    if path.parent.resolve() != results_root.resolve() or run_id.startswith("_"):
        raise V2AnalysisError(f"result is outside the canonical results root: {run_id}")
    return path


def _finite(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) \
            or not math.isfinite(float(value)):
        raise V2AnalysisError(f"{label} must be finite numeric")
    return float(value)


def _metric_from_result(receipt: dict[str, Any], ledgers: dict[str, Any],
                        primary: str) -> float:
    totals = receipt.get("totals")
    fate_counts = receipt.get("fate_counts")
    if not isinstance(totals, dict) or not isinstance(fate_counts, dict):
        raise V2AnalysisError("receipt totals/fate_counts are missing")
    if primary == "delivery_rate":
        offered = sum(int(value) for value in fate_counts.values())
        return (float(fate_counts.get("DELIVERED", 0)) / offered
                if offered else 0.0)
    if primary in {"delivered_bits", "terminal_loss_bits",
                   "in_system_bits_at_stop"}:
        return _finite(totals.get(primary), f"receipt totals.{primary}")
    congestion = ledgers.get("congestion_metrics")
    if not isinstance(congestion, dict):
        raise V2AnalysisError("ledgers.congestion_metrics is missing")
    if primary in {"access_admission_rate",
                   "network_delivery_rate_by_horizon"}:
        value = congestion.get(primary)
        return _finite(value, f"congestion metrics.{primary}")
    packets = congestion.get("packets")
    links = congestion.get("links")
    if not isinstance(packets, dict) or not isinstance(links, dict):
        raise V2AnalysisError("congestion metrics packets/links are missing")
    delivered_packets = [item for item in packets.values()
                         if isinstance(item, dict) and "e2e_s" in item]
    if primary in {"e2e_delay_mean_s", "queue_wait_mean_s",
                   "tx_time_mean_s", "propagation_time_mean_s"}:
        key = {
            "e2e_delay_mean_s": "e2e_s",
            "queue_wait_mean_s": "total_queue_wait_s",
            "tx_time_mean_s": "tx_s",
            "propagation_time_mean_s": "prop_s",
        }[primary]
        values = [_finite(item.get(key), f"packet metric {key}")
                  for item in delivered_packets]
        if not values:
            raise V2AnalysisError(f"primary metric {primary} has no delivered packets")
        return sum(values) / len(values)
    if primary in {"link_utilization_mean", "service_window_utilization_mean"}:
        values = [_finite(item.get("utilization"), "link utilization")
                  for item in links.values()]
        if not values:
            raise V2AnalysisError(f"primary metric {primary} has no service links")
        return sum(values) / len(values)
    raise V2AnalysisError(f"unsupported V2 primary metric: {primary}")


def _verify_result(root: Path, results_root: Path, row: dict[str, Any],
                   authorized: dict[str, Any], primary: str) -> dict[str, Any]:
    run_id = row.get("run_id")
    result_dir = _direct_result(results_root, run_id)
    required = (
        "formal_run.json", "governance_receipt.json", "receipt.json",
        "ledgers.json", "resolved_config.json", "manifest.json",
    )
    paths = {name: result_dir / name for name in required}
    docs = {name: _read_json(path) for name, path in paths.items()}
    receipt_errors = receipt_mod.verify_receipt_dir(str(result_dir))
    if receipt_errors:
        raise V2AnalysisError(
            f"{run_id} receipt verification failed: {'; '.join(receipt_errors)}")
    formal = docs["formal_run.json"]
    governed = docs["governance_receipt.json"]
    receipt = docs["receipt.json"]
    ledgers = docs["ledgers.json"]
    if not isinstance(formal, dict) or formal.get("schema") != "leo-sim-formal-run/v1":
        raise V2AnalysisError(f"{run_id} formal witness schema mismatch")
    if any(formal.get(key) != expected for key, expected in {
            "run_id": run_id,
            "config_sha256": authorized.get("config_sha256"),
            "authorization_sha256": authorized.get("authorization_sha256", formal.get("authorization_sha256")),
    }.items() if expected is not None):
        raise V2AnalysisError(f"{run_id} formal witness identity mismatch")
    if not isinstance(governed, dict) or governed.get("schema") != "leo-sim-governance-receipt/v1":
        raise V2AnalysisError(f"{run_id} governance receipt schema mismatch")
    if governed.get("run_id") != run_id or governed.get("research_eligible") is not True \
            or governed.get("verification_errors") != []:
        raise V2AnalysisError(f"{run_id} governance receipt is not eligible")
    if governed.get("authorization_sha256") not in (None, authorized.get("authorization_sha256")):
        raise V2AnalysisError(f"{run_id} governance authorization hash mismatch")
    receipt_sha = file_sha256(paths["receipt.json"])
    if governed.get("run_receipt_sha256") != receipt_sha \
            or formal.get("receipt_sha256") != receipt_sha:
        raise V2AnalysisError(f"{run_id} receipt hash is not bound by witnesses")
    if receipt.get("config_sha256") != authorized.get("config_sha256"):
        raise V2AnalysisError(f"{run_id} receipt config hash mismatch")
    metric = _metric_from_result(receipt, ledgers, primary)
    artifacts = [{
        "path": str(path.relative_to(root)),
        "sha256": file_sha256(path),
    } for path in paths.values()]
    return {
        "run_id": run_id,
        "arm_id": row.get("arm_id"),
        "pairing_key": row.get("pairing_key"),
        "seed": row.get("trace_seed"),
        "config_sha256": receipt.get("config_sha256"),
        "primary_metric": metric,
        "result_path": str(result_dir.relative_to(root)),
        "artifacts": artifacts,
    }


def _compute_planned_contrasts(
        results: list[dict[str, Any]], contrasts: list[dict[str, Any]],
        primary: str) -> list[dict[str, Any]]:
    """Compute each registered contrast only over its own arm pairs.

    A matrix may contain several independent pairing keys (for example one
    pair per offered-load tier).  An unrelated pair must not be treated as a
    missing arm for every contrast; only a pairing key that contains exactly
    one side of the requested contrast is malformed.
    """
    by_pair: dict[str, dict[str, dict[str, Any]]] = {}
    for result in results:
        by_pair.setdefault(result["pairing_key"], {})[result["arm_id"]] = result
    output: list[dict[str, Any]] = []
    for contrast in contrasts:
        left, right = contrast.get("left_arm"), contrast.get("right_arm")
        diffs: list[float] = []
        for pair_key in sorted(by_pair):
            pair = by_pair[pair_key]
            has_left, has_right = left in pair, right in pair
            if has_left != has_right:
                raise V2AnalysisError(
                    f"contrast {contrast.get('name')} missing arm at pair {pair_key}")
            if has_left:
                diffs.append(pair[left]["primary_metric"] -
                             pair[right]["primary_metric"])
        if not diffs:
            raise V2AnalysisError(f"contrast {contrast.get('name')} has no pairs")
        output.append({
            "name": contrast.get("name"), "left_arm": left, "right_arm": right,
            "metric": primary, "n_pairs": len(diffs),
            "differences": diffs, "mean_difference": sum(diffs) / len(diffs),
        })
    return output


def analyze(root: Path, experiment_dir: Path, authorization_path: Path,
            results_root: Path | None = None) -> dict[str, Any]:
    """Verify an authorized V2 cohort and return a persisted analysis manifest."""
    root = Path(root).resolve()
    experiment_dir = Path(experiment_dir).resolve()
    results_root = (Path(results_root) if results_root is not None
                    else root / "CODE" / "Results").resolve()
    request = _read_json(experiment_dir / "request.json")
    matrix = _read_json(experiment_dir / "run-manifest.json")
    analysis_request = _read_json(experiment_dir / "analysis-request.json")
    if matrix.get("schema") != MATRIX_SCHEMA or analysis_request.get("schema") != ANALYSIS_SCHEMA:
        raise V2AnalysisError("V2 matrix/analysis schema mismatch")
    if request.get("experiment_id") != matrix.get("experiment_id") \
            or analysis_request.get("experiment_id") != matrix.get("experiment_id"):
        raise V2AnalysisError("V2 experiment identity mismatch")
    try:
        authorization = authorize_experiment.verify_authorization(
            root, Path(authorization_path))
    except Exception as exc:
        raise V2AnalysisError(f"authorization verification failed: {exc}") from exc
    if authorization.get("status") != "AUTHORIZED" \
            or authorization.get("experiment_id") != matrix.get("experiment_id"):
        raise V2AnalysisError("authorization is not for this V2 experiment")
    cells = matrix.get("cells")
    planned_ids = analysis_request.get("planned_run_ids")
    if not isinstance(cells, list) or not isinstance(planned_ids, list) \
            or planned_ids != [cell.get("run_id") for cell in cells]:
        raise V2AnalysisError("analysis cohort does not exactly match matrix cells")
    authorized_rows = authorization.get("authorized_cells") or authorization.get("authorized_runs")
    if not isinstance(authorized_rows, list):
        raise V2AnalysisError("authorization has no authorized V2 cohort")
    authorization_sha256 = file_sha256(Path(authorization_path))
    auth_by_id = {
        row.get("run_id"): {**row, "authorization_sha256": authorization_sha256}
        for row in authorized_rows if isinstance(row, dict)
    }
    if set(auth_by_id) != set(planned_ids):
        raise V2AnalysisError("authorization cohort differs from matrix cohort")
    primary = analysis_request.get("analysis", {}).get("primary_metric")
    if not isinstance(primary, str) or not primary:
        raise V2AnalysisError("V2 primary metric is missing")
    results = [
        _verify_result(root, results_root, cell, auth_by_id[cell["run_id"]], primary)
        for cell in cells
    ]
    contrasts = analysis_request.get("analysis", {}).get("planned_contrasts", [])
    output_contrasts = _compute_planned_contrasts(results, contrasts, primary)
    input_paths = [experiment_dir / name for name in (
        "request.json", "run-manifest.json", "analysis-request.json")]
    input_paths.append(Path(authorization_path).resolve())
    for result in results:
        input_paths.extend(root / item["path"] for item in result["artifacts"])
    inputs = {str(path.relative_to(root)): file_sha256(path)
              for path in input_paths}
    return {
        "schema": SCHEMA,
        "status": "VERIFIED",
        "errors": [],
        "experiment_id": matrix["experiment_id"],
        "analysis_id": analysis_request["analysis"].get("analysis_id"),
        "primary_metric": primary,
        "verified_run_ids": planned_ids,
        "run_results": results,
        "planned_contrasts": output_contrasts,
        "claim_boundary": request.get("claim_boundary", {}),
        "inputs": inputs,
        "authorization_sha256": authorization_sha256,
        "experiment_dir": str(experiment_dir.relative_to(root)),
        "authorization_path": str(Path(authorization_path).resolve().relative_to(root)),
        "results_root": str(results_root.relative_to(root)),
        "claim_status": "READY_FOR_INDEPENDENT_CLAIM_REVIEW",
    }


def write_outputs(root: Path, out_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    root = Path(root).resolve()
    out_dir = Path(out_dir).resolve()
    if out_dir.exists() and (out_dir.is_symlink() or not out_dir.is_dir()
                             or any(out_dir.iterdir())):
        raise V2AnalysisError("analysis output directory must be new or empty")
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "schema": "leo-sim-v2-analysis-summary/v1",
        "experiment_id": manifest["experiment_id"],
        "primary_metric": manifest["primary_metric"],
        "planned_contrasts": manifest["planned_contrasts"],
        "claim_status": manifest["claim_status"],
    }
    (out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = [
        "# leo_sim V2 paired analysis", "",
        f"- status: `{manifest['status']}`",
        f"- primary metric: `{manifest['primary_metric']}`",
        f"- verified runs: `{len(manifest['verified_run_ids'])}`", "",
        "This output is evidence-bound analysis, not a paper claim.",
        "Independent claim-support and value-gate review remains required.",
    ]
    (out_dir / "report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    persisted = dict(manifest)
    persisted["output_hashes"] = {
        "summary.json": file_sha256(out_dir / "summary.json"),
        "report.md": file_sha256(out_dir / "report.md"),
    }
    persisted["output_artifacts"] = [
        {"path": str((out_dir / name).relative_to(root)), "sha256": digest}
        for name, digest in persisted["output_hashes"].items()
    ]
    (out_dir / "analysis-manifest.json").write_text(
        json.dumps(persisted, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    claim_gate = {
        "schema": CLAIM_GATE_SCHEMA,
        "status": "READY_FOR_INDEPENDENT_CLAIM_REVIEW",
        "analysis_manifest": str((out_dir / "analysis-manifest.json").relative_to(root)),
        "analysis_manifest_sha256": file_sha256(out_dir / "analysis-manifest.json"),
        "cannot_claim": manifest.get("claim_boundary", {}).get("cannot_claim", []),
    }
    (out_dir / "claim-gate.json").write_text(
        json.dumps(claim_gate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return persisted


def verify_persisted_analysis(root: Path, manifest_path: Path) -> tuple[bool, list[str]]:
    """Verify the output hashes and every bound input without trusting report text."""
    errors: list[str] = []
    root = Path(root).resolve()
    manifest_path = Path(manifest_path).resolve()
    try:
        manifest = _read_json(manifest_path)
        if manifest.get("schema") != SCHEMA or manifest.get("status") != "VERIFIED":
            raise V2AnalysisError("analysis manifest is not VERIFIED")
        for raw, digest in manifest.get("inputs", {}).items():
            path = (root / raw).resolve(strict=True)
            path.relative_to(root)
            if file_sha256(path) != digest:
                raise V2AnalysisError(f"input hash mismatch: {raw}")
        output_dir = manifest_path.parent
        for name, digest in manifest.get("output_hashes", {}).items():
            path = output_dir / name
            if file_sha256(path) != digest:
                raise V2AnalysisError(f"output hash mismatch: {name}")
        gate = _read_json(output_dir / "claim-gate.json")
        if gate.get("analysis_manifest_sha256") != file_sha256(manifest_path):
            raise V2AnalysisError("claim gate does not bind analysis manifest")
        recomputed = analyze(
            root,
            root / manifest["experiment_dir"],
            root / manifest["authorization_path"],
            root / manifest["results_root"],
        )
        for key in ("experiment_id", "primary_metric", "verified_run_ids",
                    "run_results", "planned_contrasts", "claim_boundary",
                    "inputs", "authorization_sha256"):
            if recomputed.get(key) != manifest.get(key):
                raise V2AnalysisError(f"persisted analysis differs for {key}")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(str(exc))
    return not errors, errors


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Verify/analyze leo_sim_v2 matrix results")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--experiment", type=Path, required=True)
    parser.add_argument("--authorization", type=Path, required=True)
    parser.add_argument("--results-root", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        manifest = analyze(args.root, args.experiment, args.authorization,
                           args.results_root)
        write_outputs(args.root, args.out, manifest)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"V2 ANALYSIS BLOCKED: {exc}")
        return 2
    print(json.dumps({
        "status": manifest["status"],
        "experiment_id": manifest["experiment_id"],
        "verified_runs": len(manifest["verified_run_ids"]),
        "claim_status": manifest["claim_status"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
