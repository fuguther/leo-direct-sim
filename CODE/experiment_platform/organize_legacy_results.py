#!/usr/bin/env python3
"""Reversibly separate legacy review candidates from archived runs.

The operation is intentionally limited to atomic, same-filesystem moves of
top-level RUN records.  Non-run assets remain in the source Results directory.
No file or directory is deleted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _canonical_hash(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build_plan(review: dict[str, Any], salvage: dict[str, Any]) -> dict[str, Any]:
    records = review.get("records", [])
    run_records = {
        record["relative_path"]: record
        for record in records
        if record.get("record_type") == "RUN"
    }
    non_run_records = [
        record for record in records if record.get("record_type") != "RUN"
    ]
    if len(run_records) != review.get("summary", {}).get("run_count"):
        raise ValueError("review run records are missing or duplicated")

    core: set[str] = set()
    for cohort in salvage.get("core_retrospective_cohorts", {}).values():
        core.update(cohort.get("paths", []))
    rescue = {
        record["relative_path"]
        for record in salvage.get("deletion_candidate_reclassification", {})
        .get("RESCUE_FOR_REVIEW", {})
        .get("records", [])
    }
    protected = core | rescue
    missing = protected - set(run_records)
    if missing:
        raise ValueError(f"protected paths absent from review: {sorted(missing)!r}")
    if core & rescue:
        raise ValueError("core and rescue path sets unexpectedly overlap")

    archive = set(run_records) - protected
    protected_records = [run_records[path] for path in sorted(protected)]
    archive_records = [run_records[path] for path in sorted(archive)]
    plan = {
        "schema_version": "legacy-results-organization-plan-v1",
        "status": "REVERSIBLE_MOVE_ONLY",
        "fact_boundary": {
            "all_runs_remain": "UNVERIFIED_LEGACY",
            "scientific_claim_eligible": False,
            "deletion_authorized": False,
            "non_run_assets_moved": False,
        },
        "counts": {
            "protected_core_runs": len(core),
            "protected_rescue_runs": len(rescue),
            "protected_run_total": len(protected_records),
            "archive_run_total": len(archive_records),
            "non_run_assets_left_in_place": len(non_run_records),
        },
        "bytes": {
            "protected_runs": sum(r.get("size_bytes", 0) for r in protected_records),
            "archive_runs": sum(r.get("size_bytes", 0) for r in archive_records),
            "non_run_assets_left_in_place": sum(
                r.get("size_bytes", 0) for r in non_run_records
            ),
        },
        "protected_paths": sorted(protected),
        "archive_paths": sorted(archive),
        "non_run_asset_paths": sorted(r["relative_path"] for r in non_run_records),
    }
    plan["plan_sha256"] = _canonical_hash(plan)
    return plan


def _validate_top_level(paths: list[str]) -> None:
    invalid = [
        path
        for path in paths
        if not path or path in {".", ".."} or "/" in path or "\\" in path
    ]
    if invalid:
        raise ValueError(f"refusing non-top-level paths: {invalid!r}")


def inspect_layout(source_root: Path, archive_root: Path, plan: dict[str, Any]) -> dict[str, Any]:
    archived = []
    pending = []
    problems = []
    for relative_path in plan["archive_paths"]:
        source = source_root / relative_path
        destination = archive_root / relative_path
        source_exists = source.exists()
        destination_exists = destination.exists()
        if source_exists and not destination_exists:
            pending.append(relative_path)
        elif destination_exists and not source_exists:
            archived.append(relative_path)
        else:
            problems.append(
                {
                    "relative_path": relative_path,
                    "source_exists": source_exists,
                    "archive_exists": destination_exists,
                }
            )

    protected_missing = [
        path for path in plan["protected_paths"] if not (source_root / path).exists()
    ]
    non_run_missing = [
        path for path in plan["non_run_asset_paths"] if not (source_root / path).exists()
    ]
    return {
        "pending_count": len(pending),
        "archived_count": len(archived),
        "problem_count": len(problems),
        "protected_missing": protected_missing,
        "non_run_missing": non_run_missing,
        "problems": problems,
    }


def execute_moves(source_root: Path, archive_root: Path, plan: dict[str, Any]) -> dict[str, Any]:
    source_root = source_root.resolve()
    archive_root = archive_root.resolve()
    if archive_root.parent != source_root.parent:
        raise ValueError("archive root must be a sibling of the source Results root")
    if archive_root == source_root:
        raise ValueError("archive root must differ from source root")
    _validate_top_level(
        plan["protected_paths"]
        + plan["archive_paths"]
        + plan["non_run_asset_paths"]
    )
    if not source_root.is_dir():
        raise ValueError(f"source Results root does not exist: {source_root}")

    archive_root.mkdir(mode=0o755, exist_ok=True)
    if os.stat(source_root).st_dev != os.stat(archive_root).st_dev:
        raise ValueError("source and archive roots are not on the same filesystem")

    before = inspect_layout(source_root, archive_root, plan)
    if before["problems"] or before["protected_missing"] or before["non_run_missing"]:
        raise ValueError(f"pre-move layout does not match plan: {before}")

    moved_now = 0
    for relative_path in plan["archive_paths"]:
        source = source_root / relative_path
        destination = archive_root / relative_path
        if destination.exists() and not source.exists():
            continue
        os.replace(source, destination)
        moved_now += 1

    after = inspect_layout(source_root, archive_root, plan)
    if (
        after["pending_count"]
        or after["problem_count"]
        or after["protected_missing"]
        or after["non_run_missing"]
    ):
        raise RuntimeError(f"post-move verification failed: {after}")

    receipt = {
        "schema_version": "legacy-results-organization-receipt-v1",
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "operation": "ATOMIC_SAME_FILESYSTEM_MOVE_NO_DELETE",
        "source_root": str(source_root),
        "archive_root": str(archive_root),
        "plan_sha256": plan["plan_sha256"],
        "moved_now": moved_now,
        "counts": plan["counts"],
        "bytes": plan["bytes"],
        "verification": after,
    }
    (archive_root / "_organization_receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", required=True, type=Path)
    parser.add_argument("--salvage", required=True, type=Path)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--archive-root", type=Path)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    plan = build_plan(_load_json(args.review), _load_json(args.salvage))
    if not args.execute:
        print(json.dumps({k: plan[k] for k in ("status", "counts", "bytes", "plan_sha256")}, ensure_ascii=False, indent=2))
        return 0
    if args.source_root is None or args.archive_root is None:
        parser.error("--execute requires --source-root and --archive-root")
    receipt = execute_moves(args.source_root, args.archive_root, plan)
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
