#!/usr/bin/env python3
"""Create a review-only retention classification from a legacy inventory.

This tool never reads, moves, or deletes the legacy Results tree. It only
classifies records already present in the supplied quick inventory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


KEEP = "KEEP_FOR_VERIFICATION"
COLD = "COLD_ARCHIVE_REVIEW"
DELETE = "DELETE_CANDIDATE_REVIEW"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def classify_run(run: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    completion = run.get("completion_signal", {}).get("classification")
    artifacts = run.get("key_artifacts_present", {})

    if run.get("smoke_clues", {}).get("detected") is True:
        reasons.append("SMOKE_CLUE")
    if completion != "NATURAL_END_LOG_CLUE":
        reasons.append(f"NO_NATURAL_END_LOG_CLUE:{completion or 'MISSING'}")
    if run.get("evidence_grade") == "E0_MINIMAL":
        reasons.append("E0_MINIMAL")

    if reasons:
        return DELETE, reasons

    strong_retrospective_candidate = all(
        artifacts.get(key) is True
        for key in ("resolved_config", "run_meta", "summary_metrics")
    )
    if strong_retrospective_candidate:
        return KEEP, [
            "NATURAL_END_LOG_CLUE",
            "RESOLVED_CONFIG_PRESENT",
            "RUN_META_PRESENT",
            "SUMMARY_METRICS_PRESENT",
        ]

    return COLD, [
        "NOT_DELETE_CANDIDATE",
        "INSUFFICIENT_FOR_PRIORITY_VERIFICATION",
    ]


def classify_asset(asset: dict[str, Any]) -> tuple[str, list[str]]:
    if asset.get("relative_path") == ".DS_Store":
        return DELETE, ["MACOS_METADATA_FILE"]
    return COLD, ["NON_RUN_ASSET_REQUIRES_MANUAL_LINEAGE_REVIEW"]


def human_gib(size_bytes: int) -> float:
    return round(size_bytes / (1024**3), 3)


def build_review(inventory_path: Path, inventory: dict[str, Any]) -> dict[str, Any]:
    records: list[dict[str, Any]] = []

    for run in inventory.get("runs", []):
        classification, reasons = classify_run(run)
        records.append(
            {
                "record_type": "RUN",
                "relative_path": run["relative_path"],
                "size_bytes": run.get("size_bytes", 0),
                "classification": classification,
                "reasons": reasons,
                "legacy_completion_clue": run.get("completion_signal", {}).get(
                    "classification"
                ),
                "evidence_grade": run.get("evidence_grade"),
                "checkpoint_count": len(run.get("checkpoints", [])),
                "direct_claim_or_paper_eligible": False,
            }
        )

    for asset in inventory.get("non_run_assets", []):
        classification, reasons = classify_asset(asset)
        records.append(
            {
                "record_type": "NON_RUN_ASSET",
                "relative_path": asset["relative_path"],
                "size_bytes": asset.get("size_bytes", 0),
                "classification": classification,
                "reasons": reasons,
                "legacy_completion_clue": None,
                "evidence_grade": None,
                "checkpoint_count": 0,
                "direct_claim_or_paper_eligible": False,
            }
        )

    records.sort(key=lambda record: (record["classification"], record["relative_path"]))
    counts = Counter(record["classification"] for record in records)
    byte_totals: dict[str, int] = defaultdict(int)
    for record in records:
        byte_totals[record["classification"]] += record["size_bytes"]

    classes = {}
    for classification in (KEEP, COLD, DELETE):
        classes[classification] = {
            "record_count": counts[classification],
            "size_bytes": byte_totals[classification],
            "size_gib": human_gib(byte_totals[classification]),
        }

    total_bytes = sum(record["size_bytes"] for record in records)
    return {
        "schema_version": "legacy-cleanup-review-v1",
        "status": "REVIEW_ONLY_NOT_DELETE_AUTHORIZATION",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": {
            "inventory_path": str(inventory_path),
            "inventory_sha256": sha256_file(inventory_path),
            "legacy_results_root": inventory.get("results_root"),
            "inventory_scan_complete": inventory.get("summary", {}).get(
                "scan_complete"
            ),
            "inventory_scan_error_count": inventory.get("summary", {}).get(
                "scan_error_count"
            ),
        },
        "fact_boundary": {
            "all_records_status": "UNVERIFIED_LEGACY",
            "direct_claim_or_paper_eligible": False,
            "classification_is_scientific_validity_review": False,
            "classification_authorizes_deletion": False,
            "large_artifacts_fully_hashed": False,
        },
        "classification_policy": {
            "priority_order": [DELETE, KEEP, COLD],
            DELETE: (
                "Review as a deletion candidate when a smoke clue is present, "
                "the run lacks a natural-end log clue, or evidence is E0_MINIMAL. "
                "This label does not authorize deletion."
            ),
            KEEP: (
                "Prioritize for retrospective verification when a non-smoke run "
                "has a natural-end log clue plus resolved config, run meta, and "
                "summary metrics."
            ),
            COLD: (
                "Retain without priority analysis until lineage or research value "
                "is reviewed manually."
            ),
        },
        "required_before_any_deletion": [
            "Refresh the source inventory immediately before deletion.",
            "Complete content-hash preservation and lineage review for the selected KEEP cohort.",
            "Confirm no active process writes anywhere under the legacy Results root.",
            "Approve an exact-path deletion manifest separately.",
            "Delete only exact approved paths and run a post-delete inventory.",
        ],
        "summary": {
            "record_count": len(records),
            "run_count": len(inventory.get("runs", [])),
            "non_run_asset_count": len(inventory.get("non_run_assets", [])),
            "size_bytes": total_bytes,
            "size_gib": human_gib(total_bytes),
            "classes": classes,
        },
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inventory", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
    if inventory.get("inventory_semantics", {}).get("inventory_class") != "QUICK_INDEX_ONLY":
        raise SystemExit("refusing input that is not a QUICK_INDEX_ONLY inventory")
    if inventory.get("summary", {}).get("scan_complete") is not True:
        raise SystemExit("refusing incomplete inventory")
    if inventory.get("summary", {}).get("scan_error_count") != 0:
        raise SystemExit("refusing inventory with scan errors")

    review = build_review(args.inventory, inventory)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
