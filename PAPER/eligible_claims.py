#!/usr/bin/env python3
"""Print only claims whose independent support and value gates are verifiable."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ANALYSIS.paired_analysis import verify_persisted_analysis
from CODE.experiment_platform.compile_experiment import canonical_sha, schema_errors


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = Path("ANALYSIS/claims/RESEARCH_CLAIMS.yaml")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_project_path(root: Path, raw: Any) -> Path | None:
    if not isinstance(raw, str) or not raw or Path(raw).is_absolute():
        return None
    root = root.resolve()
    candidate = (root / raw).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate


def artifact_matches(root: Path, artifact: Any) -> bool:
    if not isinstance(artifact, dict):
        return False
    path = resolve_project_path(root, artifact.get("path"))
    expected = artifact.get("sha256")
    return bool(
        path
        and path.is_file()
        and isinstance(expected, str)
        and file_sha256(path) == expected
    )


def analysis_manifest_is_verified(root: Path, artifact: Any) -> bool:
    """Recompute a VERIFIED analysis receipt rather than trusting its labels."""
    if not artifact_matches(root, artifact):
        return False
    path = resolve_project_path(root, artifact.get("path"))
    if path is None or path.name != "analysis-manifest.json":
        return False
    try:
        path.resolve().relative_to((root / "ANALYSIS").resolve())
    except ValueError:
        return False
    valid, _errors = verify_persisted_analysis(root.resolve(), path.resolve())
    return valid


def analysis_manifest_is_paper_eligible(root: Path, artifact: Any) -> bool:
    """Require verified analysis plus a confirmatory PAPER_ELIGIBLE profile."""
    if not analysis_manifest_is_verified(root, artifact):
        return False
    manifest_path = resolve_project_path(root, artifact.get("path"))
    if manifest_path is None:
        return False
    try:
        analysis_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    inputs = analysis_manifest.get("inputs")
    if not isinstance(inputs, dict):
        return False
    run_manifests: list[Path] = []
    requests: list[Path] = []
    for raw, expected_digest in inputs.items():
        candidate = resolve_project_path(root, raw)
        if candidate is None or not candidate.is_file() or file_sha256(candidate) != expected_digest:
            continue
        if candidate.name == "run-manifest.json":
            run_manifests.append(candidate)
        elif candidate.name == "request.json":
            requests.append(candidate)
    if len(run_manifests) != 1 or len(requests) != 1:
        return False
    try:
        run_manifest = json.loads(run_manifests[0].read_text(encoding="utf-8"))
        request = json.loads(requests[0].read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return (
        run_manifest.get("profile_status") == "PAPER_ELIGIBLE"
        and request.get("design", {}).get("intended_role") == "confirmatory"
    )


def claim_review_payload(claim: dict[str, Any]) -> dict[str, Any]:
    """Fields reviewers must bind; gate receipts are excluded to avoid a hash cycle."""
    keys = (
        "schema", "claim_id", "author_id", "author_session_id", "candidate_artifact",
        "statement", "claim_type", "status", "scope", "evidence", "limitations",
        "alternative_explanations", "supersedes",
    )
    payload = {key: claim.get(key) for key in keys if key in claim}
    payload["support_gate"] = {"status": claim.get("support_gate", {}).get("status")}
    payload["value_gate"] = {"status": claim.get("value_gate", {}).get("status")}
    return payload


def claim_review_sha256(claim: dict[str, Any]) -> str:
    return canonical_sha(claim_review_payload(claim))


def load_bound_receipt(
    root: Path,
    reference: Any,
    *,
    expected_role: str,
    author_id: str,
    author_session_id: str,
    required_artifacts: dict[str, str],
    claim_payload_sha256: str,
) -> dict[str, Any] | None:
    if not isinstance(reference, dict):
        return None
    receipt_path = resolve_project_path(root, reference.get("path"))
    if receipt_path is None or not receipt_path.is_file():
        return None
    if file_sha256(receipt_path) != reference.get("sha256"):
        return None
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(receipt, dict):
        return None
    try:
        receipt_schema = json.loads((root / "CODE" / "work" / "review-receipt.schema.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if schema_errors(receipt, receipt_schema):
        return None

    expected_prefix = "RR-SUPPORT-" if expected_role == "claim_support" else "RR-VALUE-"
    expected_filename_prefix = "support-" if expected_role == "claim_support" else "value-"
    if not str(reference.get("receipt_id", "")).startswith(expected_prefix):
        return None
    if not receipt_path.name.startswith(expected_filename_prefix):
        return None
    if receipt.get("schema") != "agent-review-receipt/v2":
        return None
    if not str(receipt.get("work_id", "")).startswith("WP-") or not isinstance(receipt.get("revision"), int):
        return None

    exact_fields = {
        "receipt_id": reference.get("receipt_id"),
        "role": expected_role,
        "verdict": "PASS",
        "reviewer_id": reference.get("reviewer_id"),
        "reviewer_session_id": reference.get("reviewer_session_id"),
        "subject_sha256": claim_payload_sha256,
    }
    if any(receipt.get(key) != value for key, value in exact_fields.items()):
        return None
    if reference.get("role") != expected_role or reference.get("verdict") != "PASS":
        return None
    if not str(receipt.get("producer_id", "")).startswith("producer:"):
        return None
    if not str(receipt.get("producer_session_id", "")).startswith("P-"):
        return None
    if not str(receipt.get("reviewer_id", "")).startswith("reviewer:"):
        return None
    if not str(receipt.get("reviewer_session_id", "")).startswith("R-"):
        return None
    if receipt.get("producer_id") != author_id or receipt.get("producer_session_id") != author_session_id:
        return None
    if receipt.get("reviewer_id") == author_id or receipt.get("reviewer_session_id") == author_session_id:
        return None
    independence = receipt.get("independence")
    if not isinstance(independence, dict):
        return None
    if independence.get("producer_and_reviewer_are_distinct") is not True:
        return None
    if independence.get("review_started_from_declared_inputs") is not True:
        return None

    artifact_hashes = receipt.get("artifact_hashes")
    if not isinstance(artifact_hashes, dict) or not artifact_hashes:
        return None
    if any(artifact_hashes.get(path) != digest for path, digest in required_artifacts.items()):
        return None
    if receipt.get("blocking_findings") != []:
        return None
    if not isinstance(receipt.get("evidence"), list) or not receipt["evidence"]:
        return None
    return receipt


def is_eligible(root: Path, claim: Any) -> bool:
    if not isinstance(claim, dict):
        return False
    allowed_claim_keys = {
        "schema", "claim_id", "author_id", "author_session_id", "candidate_artifact",
        "statement", "claim_type", "status", "scope", "evidence", "limitations",
        "alternative_explanations", "support_gate", "value_gate", "supersedes",
    }
    required_claim_keys = allowed_claim_keys - {"supersedes"}
    if set(claim) - allowed_claim_keys or not required_claim_keys <= set(claim):
        return False
    if claim.get("schema") != "research-claim/v2":
        return False
    try:
        claim_schema = json.loads((root / "ANALYSIS" / "claims" / "claim.schema.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    if schema_errors(claim, claim_schema):
        return False
    if not str(claim.get("claim_id", "")).startswith("CL-"):
        return False
    if len(str(claim.get("statement", "")).strip()) < 10 or len(str(claim.get("scope", "")).strip()) < 10:
        return False
    if claim.get("status") not in {"SUPPORTED", "SUPPORTED_LIMITED"}:
        return False
    if claim.get("claim_type") not in {
        "HYPOTHESIS", "OBSERVATION", "EXPERIMENT_RESULT", "MECHANISM_EXPLANATION",
        "NEGATIVE_RESULT", "SCOPE_BOUNDARY",
    }:
        return False
    evidence = claim.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        return False
    if not all(
        isinstance(item, dict)
        and set(item) == {"evidence_id", "evidence_kind", "artifact", "supports"}
        and str(item.get("evidence_id", "")).startswith("EV-")
        and item.get("evidence_kind") == "VERIFIED_ANALYSIS"
        and len(str(item.get("supports", "")).strip()) >= 10
        and analysis_manifest_is_paper_eligible(root, item.get("artifact"))
        for item in evidence
    ):
        return False
    if not isinstance(claim.get("limitations"), list) or not claim["limitations"] or not all(
        isinstance(item, str) and len(item.strip()) >= 10 for item in claim["limitations"]
    ):
        return False
    if not isinstance(claim.get("alternative_explanations"), list) or not claim["alternative_explanations"] or not all(
        isinstance(item, str) and len(item.strip()) >= 10 for item in claim["alternative_explanations"]
    ):
        return False

    candidate = claim.get("candidate_artifact")
    if not artifact_matches(root, candidate):
        return False
    support_gate = claim.get("support_gate")
    value_gate = claim.get("value_gate")
    if not isinstance(support_gate, dict) or support_gate.get("status") != "PASS":
        return False
    if not isinstance(value_gate, dict) or value_gate.get("status") not in {"KEEP", "PROMOTE"}:
        return False
    support_ref = support_gate.get("receipt")
    value_ref = value_gate.get("receipt")
    if not isinstance(support_ref, dict) or not isinstance(value_ref, dict):
        return False

    # The gates are independent decisions, not two labels on one review.
    for key in ("receipt_id", "path", "sha256", "reviewer_id", "reviewer_session_id"):
        if support_ref.get(key) == value_ref.get(key):
            return False

    author_id = claim.get("author_id")
    author_session_id = claim.get("author_session_id")
    if not isinstance(author_id, str) or not author_id.startswith("producer:"):
        return False
    if not isinstance(author_session_id, str) or not author_session_id.startswith("P-"):
        return False
    required_artifacts = {candidate["path"]: candidate["sha256"]}
    required_artifacts.update(
        {item["artifact"]["path"]: item["artifact"]["sha256"] for item in evidence}
    )
    subject_sha = claim_review_sha256(claim)
    if support_ref.get("subject_sha256") != subject_sha or value_ref.get("subject_sha256") != subject_sha:
        return False
    support_receipt = load_bound_receipt(
        root,
        support_ref,
        expected_role="claim_support",
        author_id=author_id,
        author_session_id=author_session_id,
        required_artifacts=required_artifacts,
        claim_payload_sha256=subject_sha,
    )
    value_receipt = load_bound_receipt(
        root,
        value_ref,
        expected_role="claim_value",
        author_id=author_id,
        author_session_id=author_session_id,
        required_artifacts=required_artifacts,
        claim_payload_sha256=subject_sha,
    )
    return support_receipt is not None and value_receipt is not None


def eligible_claims(root: Path, registry_path: Path) -> list[dict[str, Any]]:
    registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    if not isinstance(registry, dict) or not isinstance(registry.get("claims"), list):
        raise ValueError("claim registry must contain a claims list")
    return [claim for claim in registry["claims"] if is_eligible(root, claim)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--claims", type=Path, default=DEFAULT_REGISTRY)
    args = parser.parse_args()

    root = args.root.resolve()
    registry_path = args.claims if args.claims.is_absolute() else root / args.claims
    try:
        selected = eligible_claims(root, registry_path.resolve())
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"eligible_claims: {exc}", file=sys.stderr)
        return 2
    json.dump(selected, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
