#!/usr/bin/env python3
"""Audit document authority, coverage, replacement links, and review cadence."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


SCHEMA = "leo-document-governance-report/v1"
CURRENT_STATUSES = {"CURRENT-CONTRACT", "CURRENT-VOLATILE"}
NON_DIRECTIVE_STATUSES = {
    "SUPPORTING",
    "ROLLING-LOG",
    "EVIDENCE-SNAPSHOT",
    "HISTORICAL",
    "SUPERSEDED",
}
REQUIRED_ENTRY_KEYS = {
    "status",
    "purpose",
    "may_direct_current_work",
    "owner",
    "last_reviewed",
    "review_interval_days",
    "replacement",
    "require_banner",
    "archive_candidate",
    "suggested_archive_target",
}


def load_registry(path: Path) -> dict[str, Any]:
    """Load a document-governance registry without mutating repository state."""

    with path.open("r", encoding="utf-8") as handle:
        registry = json.load(handle)
    if not isinstance(registry, dict):
        raise ValueError("document registry must be a JSON object")
    return registry


def _error(code: str, message: str, *, path: str | None = None, kind: str = "structure") -> dict[str, str]:
    item = {"code": code, "kind": kind, "message": message}
    if path is not None:
        item["path"] = path
    return item


def _entry_label(entry: dict[str, Any]) -> str:
    return str(entry.get("path") or entry.get("glob") or "<missing path/glob>")


def _matches(entry: dict[str, Any], relative_path: str) -> bool:
    if "path" in entry:
        return entry["path"] == relative_path
    pattern = entry.get("glob")
    return isinstance(pattern, str) and PurePosixPath(relative_path).match(pattern)


def _expand_pattern(root: Path, pattern: str) -> list[str]:
    if any(character in pattern for character in "*?["):
        return sorted(
            path.relative_to(root).as_posix()
            for path in root.glob(pattern)
            if path.is_file()
        )
    path = root / pattern
    return [pattern] if path.is_file() else []


def _covered_paths(root: Path, patterns: Iterable[str]) -> set[str]:
    covered: set[str] = set()
    for pattern in patterns:
        if isinstance(pattern, str):
            covered.update(_expand_pattern(root, pattern))
    return covered


def _first_lines(path: Path, limit: int = 12) -> str:
    try:
        return "\n".join(path.read_text(encoding="utf-8").splitlines()[:limit])
    except UnicodeDecodeError:
        return ""


def _audit_current_fact_sync(
    root: Path,
    registry: dict[str, Any],
    errors: list[dict[str, str]],
) -> None:
    """Fail when a newer claim gate is not reflected in current entries."""

    sync = registry.get("current_fact_sync")
    if sync is None:
        return
    if not isinstance(sync, dict):
        errors.append(_error("INVALID_CURRENT_FACT_SYNC", "current_fact_sync must be an object"))
        return

    source_glob = sync.get("source_glob")
    current_source = sync.get("current_source")
    expected_sha256 = sync.get("current_source_sha256")
    targets = sync.get("targets")
    if not isinstance(source_glob, str) or not isinstance(current_source, str):
        errors.append(
            _error(
                "INVALID_CURRENT_FACT_SYNC",
                "current_fact_sync requires source_glob and current_source strings",
            )
        )
        return
    if not isinstance(expected_sha256, str) or len(expected_sha256) != 64:
        errors.append(
            _error(
                "INVALID_CURRENT_FACT_SYNC",
                "current_source_sha256 must contain 64 hex characters",
            )
        )
        return
    if not isinstance(targets, list):
        errors.append(_error("INVALID_CURRENT_FACT_SYNC", "targets must be a list"))
        return

    sources = _expand_pattern(root, source_glob)
    if not sources:
        errors.append(
            _error(
                "CURRENT_FACT_SOURCE_MISSING",
                "source_glob matches no claim gates",
                path=source_glob,
                kind="staleness",
            )
        )
        return
    latest_source = max(sources)
    if current_source != latest_source:
        errors.append(
            _error(
                "CURRENT_FACT_SOURCE_OUTDATED",
                f"current source is {current_source}; latest tracked source is {latest_source}",
                path=current_source,
                kind="staleness",
            )
        )

    source_path = root / current_source
    if not source_path.is_file():
        errors.append(
            _error(
                "CURRENT_FACT_SOURCE_MISSING",
                "configured current source does not exist",
                path=current_source,
                kind="staleness",
            )
        )
    else:
        actual_sha256 = hashlib.sha256(source_path.read_bytes()).hexdigest()
        if actual_sha256 != expected_sha256:
            errors.append(
                _error(
                    "CURRENT_FACT_SOURCE_CHANGED",
                    "current fact source hash changed without a synchronized status update",
                    path=current_source,
                    kind="staleness",
                )
            )

    for target in targets:
        if not isinstance(target, dict) or not isinstance(target.get("path"), str):
            errors.append(_error("INVALID_CURRENT_FACT_TARGET", "each target requires a path"))
            continue
        relative_path = target["path"]
        required_tokens = target.get("contains")
        if not isinstance(required_tokens, list) or not all(
            isinstance(token, str) for token in required_tokens
        ):
            errors.append(
                _error(
                    "INVALID_CURRENT_FACT_TARGET",
                    "target contains must be a list of strings",
                    path=relative_path,
                )
            )
            continue
        target_path = root / relative_path
        if not target_path.is_file():
            errors.append(
                _error(
                    "CURRENT_FACT_TARGET_MISSING",
                    "current fact target does not exist",
                    path=relative_path,
                    kind="staleness",
                )
            )
            continue
        content = target_path.read_text(encoding="utf-8")
        for token in required_tokens:
            if token not in content:
                errors.append(
                    _error(
                        "CURRENT_FACT_TEXT_MISSING",
                        f"current fact token missing: {token}",
                        path=relative_path,
                        kind="staleness",
                    )
                )


def audit_repository(
    root: Path,
    registry: dict[str, Any],
    today: date | None = None,
) -> dict[str, Any]:
    """Return a deterministic audit report; never edit, move, or delete files."""

    root = root.resolve()
    today = today or date.today()
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    stale: list[str] = []
    archive_candidates: list[dict[str, str]] = []

    allowed_statuses = registry.get("allowed_statuses")
    if not isinstance(allowed_statuses, list) or not all(
        isinstance(status, str) for status in allowed_statuses
    ):
        errors.append(_error("INVALID_ALLOWED_STATUSES", "allowed_statuses must be a list of strings"))
        allowed_status_set: set[str] = set()
    else:
        allowed_status_set = set(allowed_statuses)

    entries = registry.get("entries")
    if not isinstance(entries, list):
        errors.append(_error("INVALID_ENTRIES", "entries must be a list"))
        entries = []

    coverage = registry.get("coverage")
    if not isinstance(coverage, list) or not all(isinstance(pattern, str) for pattern in coverage):
        errors.append(_error("INVALID_COVERAGE", "coverage must be a list of path patterns"))
        coverage = []

    exact_paths: set[str] = set()
    matched_by_entry: list[list[str]] = []

    for index, raw_entry in enumerate(entries):
        if not isinstance(raw_entry, dict):
            errors.append(_error("INVALID_ENTRY", f"entry {index} must be an object"))
            matched_by_entry.append([])
            continue
        entry = raw_entry
        label = _entry_label(entry)
        has_path = isinstance(entry.get("path"), str)
        has_glob = isinstance(entry.get("glob"), str)
        if has_path == has_glob:
            errors.append(_error("INVALID_MATCHER", "entry must define exactly one of path or glob", path=label))
            matched_by_entry.append([])
            continue
        missing_keys = sorted(REQUIRED_ENTRY_KEYS - set(entry))
        if missing_keys:
            errors.append(
                _error(
                    "MISSING_ENTRY_FIELDS",
                    f"missing required fields: {', '.join(missing_keys)}",
                    path=label,
                )
            )

        if has_path:
            if label in exact_paths:
                errors.append(_error("DUPLICATE_EXACT_PATH", "exact path is registered more than once", path=label))
            exact_paths.add(label)

        matches = _expand_pattern(root, label)
        matched_by_entry.append(matches)
        if not matches:
            errors.append(_error("REGISTERED_PATH_MISSING", "registered path or glob matches no files", path=label))

        status = entry.get("status")
        if status not in allowed_status_set:
            errors.append(_error("INVALID_STATUS", f"unsupported status: {status!r}", path=label))

        may_direct = entry.get("may_direct_current_work")
        if not isinstance(may_direct, bool):
            errors.append(_error("INVALID_DIRECTIVE_FLAG", "may_direct_current_work must be boolean", path=label))
        elif status in NON_DIRECTIVE_STATUSES and may_direct:
            errors.append(_error("NONCURRENT_MAY_DIRECT", f"{status} may not direct current work", path=label))

        replacement = entry.get("replacement")
        if replacement is not None:
            if not isinstance(replacement, str) or not (root / replacement).is_file():
                errors.append(_error("INVALID_REPLACEMENT", "replacement must name an existing file", path=label))
        if status == "SUPERSEDED" and not replacement:
            errors.append(_error("SUPERSEDED_WITHOUT_REPLACEMENT", "superseded entry requires replacement", path=label))

        require_banner = entry.get("require_banner")
        if not isinstance(require_banner, bool):
            errors.append(_error("INVALID_BANNER_FLAG", "require_banner must be boolean", path=label))
        elif require_banner:
            for matched in matches:
                header = _first_lines(root / matched)
                if str(status) not in header:
                    errors.append(_error("MISSING_STATUS_BANNER", f"first 12 lines must contain {status}", path=matched))
                if replacement and Path(replacement).name not in header:
                    errors.append(
                        _error(
                            "MISSING_REPLACEMENT_BANNER",
                            f"first 12 lines must name {Path(replacement).name}",
                            path=matched,
                        )
                    )

        protected_sha256 = entry.get("protected_sha256")
        if protected_sha256 is not None:
            if not has_path or not isinstance(protected_sha256, str) or len(protected_sha256) != 64:
                errors.append(_error("INVALID_PROTECTED_HASH", "protected_sha256 requires an exact path and 64 hex characters", path=label))
            elif matches:
                actual = hashlib.sha256((root / label).read_bytes()).hexdigest()
                if actual != protected_sha256:
                    errors.append(_error("PROTECTED_CONTENT_CHANGED", "protected content hash differs from registry", path=label))

        reviewed = entry.get("last_reviewed")
        interval = entry.get("review_interval_days")
        if status in CURRENT_STATUSES:
            if not isinstance(reviewed, str) or not isinstance(interval, int) or interval <= 0:
                errors.append(
                    _error(
                        "CURRENT_WITHOUT_REVIEW_CADENCE",
                        "current entries require last_reviewed and a positive review_interval_days",
                        path=label,
                    )
                )
            else:
                try:
                    reviewed_date = date.fromisoformat(reviewed)
                except ValueError:
                    errors.append(_error("INVALID_REVIEW_DATE", "last_reviewed must use YYYY-MM-DD", path=label))
                else:
                    if today > reviewed_date + timedelta(days=interval):
                        stale.extend(matches or [label])
                        errors.append(
                            _error(
                                "STALE_CURRENT",
                                f"review expired on {(reviewed_date + timedelta(days=interval)).isoformat()}",
                                path=label,
                                kind="staleness",
                            )
                        )

        if entry.get("archive_candidate"):
            target = entry.get("suggested_archive_target")
            if not isinstance(target, str) or not target:
                errors.append(_error("ARCHIVE_TARGET_MISSING", "archive candidate requires suggested_archive_target", path=label))
            elif has_path:
                archive_candidates.append({"path": label, "suggested_target": target})
            else:
                warnings.append(_error("GLOB_ARCHIVE_CANDIDATE", "glob archive candidates must be reviewed path by path", path=label))

    covered = _covered_paths(root, coverage)
    for relative_path in sorted(covered):
        matching_entries = [entry for entry in entries if isinstance(entry, dict) and _matches(entry, relative_path)]
        if not matching_entries:
            errors.append(_error("UNCLASSIFIED_DOCUMENT", "governed document has no registry entry", path=relative_path))
        elif len(matching_entries) > 1:
            labels = ", ".join(_entry_label(entry) for entry in matching_entries)
            errors.append(_error("AMBIGUOUS_CLASSIFICATION", f"matches multiple entries: {labels}", path=relative_path))

    invariants = registry.get("entry_point_invariants", [])
    if not isinstance(invariants, list):
        errors.append(_error("INVALID_INVARIANTS", "entry_point_invariants must be a list"))
    else:
        for invariant in invariants:
            if not isinstance(invariant, dict) or not isinstance(invariant.get("path"), str):
                errors.append(_error("INVALID_INVARIANT", "each invariant must have a path"))
                continue
            relative_path = invariant["path"]
            target = root / relative_path
            if not target.is_file():
                errors.append(_error("INVARIANT_PATH_MISSING", "entry-point invariant path is missing", path=relative_path))
                continue
            content = target.read_text(encoding="utf-8")
            for expected in invariant.get("contains", []):
                if expected not in content:
                    errors.append(_error("ENTRY_POINT_TEXT_MISSING", f"required text missing: {expected}", path=relative_path))
            for forbidden in invariant.get("excludes", []):
                if forbidden in content:
                    errors.append(_error("FORBIDDEN_ENTRY_POINT_TEXT", f"forbidden text remains: {forbidden}", path=relative_path))

    _audit_current_fact_sync(root, registry, errors)

    return {
        "schema": SCHEMA,
        "checked_at": today.isoformat(),
        "errors": errors,
        "warnings": warnings,
        "stale": sorted(set(stale)),
        "archive_candidates": sorted(archive_candidates, key=lambda item: item["path"]),
    }


def _parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default_root = Path(__file__).resolve().parents[1]
    parser.add_argument("--root", type=Path, default=default_root)
    parser.add_argument("--registry", type=Path, default=Path("ANALYSIS/DOCUMENT-STATUS.json"))
    parser.add_argument("--today", type=_parse_date)
    parser.add_argument("--mode", choices=("structure", "staleness", "all"), default="all")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args(argv)

    root = args.root.resolve()
    registry_path = args.registry if args.registry.is_absolute() else root / args.registry
    try:
        registry = load_registry(registry_path)
        report = audit_repository(root, registry, today=args.today)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"document governance audit failed to start: {exc}", file=sys.stderr)
        return 2

    if args.report:
        report_path = args.report if args.report.is_absolute() else root / args.report
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    selected_errors = [
        error
        for error in report["errors"]
        if args.mode == "all"
        or (args.mode == "structure" and error["kind"] == "structure")
        or (args.mode == "staleness" and error["kind"] == "staleness")
    ]
    for error in selected_errors:
        location = f" [{error.get('path')}]" if error.get("path") else ""
        print(f"{error['code']}{location}: {error['message']}", file=sys.stderr)
    print(
        f"document-governance: {len(selected_errors)} selected errors, "
        f"{len(report['warnings'])} warnings, {len(report['archive_candidates'])} archive candidates"
    )
    return 1 if selected_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
