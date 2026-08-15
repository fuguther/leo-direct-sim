#!/usr/bin/env python3
"""Build a bounded, read-only inventory of legacy Results directories.

The inventory grades evidence *completeness*, never performance or scientific
value.  Every discovered run remains ``UNVERIFIED_LEGACY`` and is ineligible
for direct use by ANALYSIS/claims and PAPER.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "legacy-results-inventory-v2"
MAX_HASH_BYTES = 2 * 1024 * 1024
MAX_METADATA_READ_BYTES = 2 * 1024 * 1024
MAX_LOG_TAIL_BYTES = 64 * 1024
NON_RUN_DIRECTORY_NAMES = {"analysis", "curated"}

# Only small identity/provenance files are eligible for hashing.  Large result
# arrays, tables and checkpoints are deliberately excluded even when tiny.
HASH_CANDIDATES = (
    "artifact_manifest.json",
    "config_used.json",
    "config_used.yaml",
    "hyperparams.txt",
    "logfile.log",
    "resolved-config.json",
    "run_trace/graph_snapshot.json",
    "run_trace/run_meta.json",
    "experiment_bundle/metrics_definitions.json",
)
NEVER_HASH_SUFFIXES = {
    ".ckpt",
    ".csv",
    ".gz",
    ".h5",
    ".hdf5",
    ".npy",
    ".npz",
    ".parquet",
    ".pickle",
    ".pkl",
    ".pt",
    ".pth",
    ".zip",
}
CHECKPOINT_SUFFIXES = {".ckpt", ".h5", ".hdf5", ".pickle", ".pkl", ".pt", ".pth"}
SMOKE_TOKEN_RE = re.compile(r"(?:^|[^a-z0-9])(smoke|canary|preflight)(?:$|[^a-z0-9])")
ELAPSED_TIME_RE = re.compile(r"(?m)^Elapsed time(?: for [^:\n]+)?:\s*\S.*$")


class InventoryError(ValueError):
    """Raised when the requested inventory would violate its safety boundary."""


@dataclass(frozen=True)
class ScannedFile:
    path: Path
    size_bytes: int
    mtime_ns: int


@dataclass
class ScanSnapshot:
    files: dict[str, ScannedFile]
    size_bytes: int
    subdirectory_count: int
    symlinks: list[dict[str, Any]]
    scan_errors: list[str]

    @property
    def complete(self) -> bool:
        return not self.scan_errors


def _open_regular_no_follow(path: Path) -> tuple[int, os.stat_result]:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        file_stat = os.fstat(fd)
        if not stat.S_ISREG(file_stat.st_mode):
            raise OSError("not a regular file")
    except Exception:
        os.close(fd)
        raise
    return fd, file_stat


def _sha256(scanned: ScannedFile) -> str:
    digest = hashlib.sha256()
    fd, _ = _open_regular_no_follow(scanned.path)
    with os.fdopen(fd, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _bounded_files(scan_root: Path) -> ScanSnapshot:
    """Index regular files without following symlinks or leaving ``scan_root``."""

    files: dict[str, ScannedFile] = {}
    total_size = 0
    directory_count = 0
    symlinks: list[dict[str, Any]] = []
    scan_errors: list[str] = []
    stack: list[Path] = [scan_root]

    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as scanner:
                entries = sorted(scanner, key=lambda entry: entry.name)
        except OSError as exc:
            rel = current.relative_to(scan_root).as_posix() or "."
            scan_errors.append(f"{rel}: {exc.__class__.__name__}")
            continue

        child_dirs: list[Path] = []
        for entry in entries:
            rel = Path(entry.path).relative_to(scan_root).as_posix()
            try:
                entry_stat = entry.stat(follow_symlinks=False)
            except OSError as exc:
                scan_errors.append(f"{rel}: {exc.__class__.__name__}")
                continue
            mode = entry_stat.st_mode
            if stat.S_ISLNK(mode):
                try:
                    target: str | None = os.readlink(entry.path)
                except OSError as exc:
                    target = None
                    scan_errors.append(f"{rel}: readlink {exc.__class__.__name__}")
                symlinks.append(
                    {
                        "claim_status": "UNVERIFIED_LEGACY",
                        "direct_claim_or_paper_eligible": False,
                        "relative_path": rel,
                        "target": target,
                        "target_followed": False,
                    }
                )
            elif stat.S_ISDIR(mode):
                directory_count += 1
                child_dirs.append(Path(entry.path))
            elif stat.S_ISREG(mode):
                files[rel] = ScannedFile(
                    path=Path(entry.path),
                    size_bytes=entry_stat.st_size,
                    mtime_ns=entry_stat.st_mtime_ns,
                )
                total_size += entry_stat.st_size
            else:
                scan_errors.append(f"{rel}: unsupported_file_type")
        # Reverse because the stack is LIFO; traversal is deterministic either
        # way, but this keeps lexical order for any recorded scan errors.
        stack.extend(reversed(child_dirs))

    return ScanSnapshot(
        files=files,
        size_bytes=total_size,
        subdirectory_count=directory_count,
        symlinks=symlinks,
        scan_errors=scan_errors,
    )


def _read_run_meta(
    files: dict[str, ScannedFile], scan_errors: list[str]
) -> tuple[str, dict[str, Any] | None]:
    scanned = files.get("run_trace/run_meta.json")
    if scanned is None:
        return "ABSENT", None
    if scanned.size_bytes > MAX_METADATA_READ_BYTES:
        scan_errors.append("run_trace/run_meta.json: metadata_too_large")
        return "INVALID", None
    try:
        fd, _ = _open_regular_no_follow(scanned.path)
        with os.fdopen(fd, "rb") as handle:
            raw = handle.read(MAX_METADATA_READ_BYTES + 1)
        if len(raw) > MAX_METADATA_READ_BYTES:
            raise ValueError("metadata grew beyond bounded read")
        payload = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        scan_errors.append("run_trace/run_meta.json: unreadable_or_invalid")
        return "INVALID", None
    except ValueError:
        scan_errors.append("run_trace/run_meta.json: changed_during_scan")
        return "INVALID", None
    if not isinstance(payload, dict):
        scan_errors.append("run_trace/run_meta.json: root_not_object")
        return "INVALID", None
    return "VALID", payload


def _log_has_elapsed_time(scanned: ScannedFile | None, scan_errors: list[str]) -> bool:
    if scanned is None:
        return False
    try:
        fd, file_stat = _open_regular_no_follow(scanned.path)
        with os.fdopen(fd, "rb") as handle:
            size = file_stat.st_size
            handle.seek(max(0, size - MAX_LOG_TAIL_BYTES))
            tail = handle.read(MAX_LOG_TAIL_BYTES)
    except OSError as exc:
        scan_errors.append(f"logfile.log: {exc.__class__.__name__}")
        return False
    return ELAPSED_TIME_RE.search(tail.decode("utf-8", errors="replace")) is not None


def _completion_signal(
    meta: dict[str, Any] | None,
    files: dict[str, ScannedFile],
    scan_errors: list[str],
) -> dict[str, Any]:
    natural_end = meta.get("natural_end") if meta else None
    interrupted = meta.get("interrupted") if meta else None
    natural_end = natural_end if isinstance(natural_end, bool) else None
    interrupted = interrupted if isinstance(interrupted, bool) else None
    legacy_clues: list[str] = []
    if _log_has_elapsed_time(files.get("logfile.log"), scan_errors):
        legacy_clues.append("NATURAL_END_LOG_CLUE")
    if "run_trace/interrupt_meta.json" in files:
        legacy_clues.append("INTERRUPT_META_PRESENT")

    if natural_end is True and interrupted is True:
        classification = "CONFLICTING_METADATA"
    elif interrupted is True:
        classification = "INTERRUPTED_REPORTED"
    elif natural_end is True and interrupted is False:
        classification = "NATURAL_END_REPORTED"
    elif natural_end is False:
        classification = "NOT_NATURAL_END_REPORTED"
    elif "INTERRUPT_META_PRESENT" in legacy_clues:
        # An interrupt receipt is conservatively stronger than a legacy log
        # marker.  Both remain clues and cannot establish modern completion.
        classification = "INTERRUPT_META_CLUE"
    elif "NATURAL_END_LOG_CLUE" in legacy_clues:
        classification = "NATURAL_END_LOG_CLUE"
    else:
        classification = "UNKNOWN"
    return {
        "classification": classification,
        "interrupted": interrupted,
        "legacy_clues": legacy_clues,
        "modern_natural_end_established": False,
        "natural_end_metadata_reports_noninterrupted": (
            natural_end is True and interrupted is False
        ),
        "natural_end": natural_end,
        "source": "run_trace/run_meta.json" if meta is not None else None,
        "warning": (
            "legacy_clues_do_not_establish_modern_natural_end"
            if legacy_clues
            else None
        ),
    }


def _smoke_clues(run_name: str, meta: dict[str, Any] | None) -> dict[str, Any]:
    sources: list[str] = []
    for match in SMOKE_TOKEN_RE.finditer(run_name.casefold()):
        source = f"path_token:{match.group(1)}"
        if source not in sources:
            sources.append(source)
    if meta and meta.get("smoke") is True:
        sources.append("run_meta.smoke=true")
    return {
        "detected": bool(sources),
        "sources": sources,
        "warning": "clue_only_not_a_verified_run_purpose" if sources else None,
    }


def _presence(files: dict[str, ScannedFile]) -> dict[str, bool]:
    paths = set(files)
    return {
        "artifact_manifest": "artifact_manifest.json" in paths,
        "checkpoint_any": any(Path(rel).suffix.casefold() in CHECKPOINT_SUFFIXES for rel in paths),
        "graph_snapshot": "run_trace/graph_snapshot.json" in paths,
        "hyperparams": "hyperparams.txt" in paths,
        "interrupt_meta": "run_trace/interrupt_meta.json" in paths,
        "logfile": "logfile.log" in paths,
        "metrics_definitions": "experiment_bundle/metrics_definitions.json" in paths,
        "resolved_config": any(
            rel in paths for rel in ("config_used.json", "config_used.yaml", "resolved-config.json")
        ),
        "run_meta": "run_trace/run_meta.json" in paths,
        "summary_metrics": "experiment_bundle/summary_metrics.csv" in paths,
    }


def _evidence_grade(
    run_meta_state: str,
    presence: dict[str, bool],
    completion: dict[str, Any],
) -> tuple[str, list[str]]:
    reasons: list[str] = [
        "legacy inventory does not verify provenance, manifest contents, or completion"
    ]
    if run_meta_state != "VALID":
        reasons.append("valid run_meta missing")
        return "E0_MINIMAL", reasons

    if not (presence["graph_snapshot"] and presence["summary_metrics"]):
        if not presence["graph_snapshot"]:
            reasons.append("graph_snapshot missing")
        if not presence["summary_metrics"]:
            reasons.append("summary_metrics missing")
        return "E1_METADATA", reasons

    has_configuration = presence["resolved_config"] or presence["hyperparams"]
    if not has_configuration:
        reasons.append("configuration record missing")
    if completion["classification"] != "NATURAL_END_REPORTED":
        reasons.append("natural non-interrupted completion not established")
    if not presence["artifact_manifest"]:
        reasons.append("artifact_manifest missing")

    if has_configuration and completion["classification"] == "NATURAL_END_REPORTED":
        if presence["artifact_manifest"]:
            return "E3_MANIFEST_AND_COMPLETION_REPORT_PRESENT", reasons
        return "E2_CORE_ARTIFACTS_AND_COMPLETION_REPORT_PRESENT", reasons
    return "E1_METADATA", reasons


def _hash_key_files(
    files: dict[str, ScannedFile], scan_errors: list[str]
) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    hashes: dict[str, dict[str, Any]] = {}
    skipped: dict[str, str] = {}
    for rel in HASH_CANDIDATES:
        scanned = files.get(rel)
        if scanned is None:
            continue
        suffix = scanned.path.suffix.casefold()
        size = scanned.size_bytes
        if suffix in NEVER_HASH_SUFFIXES:
            skipped[rel] = "excluded_artifact_type"
        elif size > MAX_HASH_BYTES:
            skipped[rel] = f"larger_than_{MAX_HASH_BYTES}_bytes"
        else:
            try:
                hashes[rel] = {"bytes": size, "sha256": _sha256(scanned)}
            except OSError as exc:
                skipped[rel] = f"read_error:{exc.__class__.__name__}"
                scan_errors.append(f"{rel}: hash {exc.__class__.__name__}")
    return hashes, skipped


def _checkpoint_role_heuristic(relative_path: str) -> str:
    lowered = relative_path.casefold()
    if "target" in lowered:
        return "POSSIBLE_TARGET_NETWORK_STATE"
    if "optim" in lowered:
        return "POSSIBLE_OPTIMIZER_STATE"
    if any(token in lowered for token in ("replay", "buffer", "memory")):
        return "POSSIBLE_REPLAY_STATE"
    if "actor" in lowered:
        return "POSSIBLE_ACTOR_STATE"
    if "critic" in lowered:
        return "POSSIBLE_CRITIC_STATE"
    if any(token in lowered for token in ("model", "network", "nn/", "nns/")):
        return "POSSIBLE_MODEL_STATE"
    return "UNCLASSIFIED_CHECKPOINT"


def _pending_file_record(relative_path: str, scanned: ScannedFile) -> dict[str, Any]:
    record: dict[str, Any] = {
        "claim_status": "UNVERIFIED_LEGACY",
        "direct_claim_or_paper_eligible": False,
        "hash_status": "PENDING_NOT_HASHED_BY_QUICK_INVENTORY",
        "lineage_status": "UNKNOWN",
        "mtime_ns": scanned.mtime_ns,
        "relative_path": relative_path,
        "sha256": None,
        "size_bytes": scanned.size_bytes,
    }
    if scanned.path.suffix.casefold() in CHECKPOINT_SUFFIXES:
        record.update(
            {
                "role_heuristic": _checkpoint_role_heuristic(relative_path),
                "role_heuristic_basis": "path_tokens_only_not_checkpoint_contents",
            }
        )
    return record


def _checkpoint_records(files: dict[str, ScannedFile]) -> list[dict[str, Any]]:
    return [
        _pending_file_record(rel, scanned)
        for rel, scanned in sorted(files.items())
        if scanned.path.suffix.casefold() in CHECKPOINT_SUFFIXES
    ]


def inventory_run(run_dir: Path, results_root: Path) -> dict[str, Any]:
    scan = _bounded_files(run_dir)
    run_meta_state, meta = _read_run_meta(scan.files, scan.scan_errors)
    completion = _completion_signal(meta, scan.files, scan.scan_errors)
    presence = _presence(scan.files)
    grade, limitations = _evidence_grade(run_meta_state, presence, completion)
    hashes, skipped_hashes = _hash_key_files(scan.files, scan.scan_errors)
    return {
        "claim_status": "UNVERIFIED_LEGACY",
        "checkpoints": _checkpoint_records(scan.files),
        "completion_signal": completion,
        "direct_claim_or_paper_eligible": False,
        "evidence_grade": grade,
        "evidence_limitations": limitations,
        "file_count": len(scan.files),
        "key_artifacts_present": presence,
        "key_file_hashes": hashes,
        "key_file_hashes_skipped": skipped_hashes,
        "relative_path": run_dir.relative_to(results_root).as_posix(),
        "run_meta_state": run_meta_state,
        "scan_complete": scan.complete,
        "scan_errors": scan.scan_errors,
        "size_bytes": scan.size_bytes,
        "smoke_clues": _smoke_clues(run_dir.name, meta),
        "subdirectory_count": scan.subdirectory_count,
        "symlinks": scan.symlinks,
    }


def _inventory_non_run_directory(asset_dir: Path, results_root: Path) -> dict[str, Any]:
    scan = _bounded_files(asset_dir)
    return {
        "asset_type": "CONTROL_DIRECTORY",
        "claim_status": "UNVERIFIED_LEGACY",
        "direct_claim_or_paper_eligible": False,
        "file_count": len(scan.files),
        "file_index": [
            _pending_file_record(rel, scanned) for rel, scanned in sorted(scan.files.items())
        ],
        "relative_path": asset_dir.relative_to(results_root).as_posix(),
        "scan_complete": scan.complete,
        "scan_errors": scan.scan_errors,
        "size_bytes": scan.size_bytes,
        "subdirectory_count": scan.subdirectory_count,
        "symlinks": scan.symlinks,
    }


def _inventory_top_level_file(relative_path: str, scanned: ScannedFile) -> dict[str, Any]:
    record = _pending_file_record(relative_path, scanned)
    record.update(
        {
            "asset_type": "TOP_LEVEL_FILE",
            "claim_status": "UNVERIFIED_LEGACY",
            "direct_claim_or_paper_eligible": False,
            "scan_complete": True,
            "scan_errors": [],
        }
    )
    if scanned.path.suffix.casefold() not in NEVER_HASH_SUFFIXES and scanned.size_bytes <= MAX_HASH_BYTES:
        try:
            record["sha256"] = _sha256(scanned)
            record["hash_status"] = "HASHED_BY_QUICK_INVENTORY"
        except OSError as exc:
            record["scan_complete"] = False
            record["scan_errors"].append(f"hash {exc.__class__.__name__}")
    return record


def _inventory_top_level_symlink(relative_path: str, path: Path) -> dict[str, Any]:
    scan_errors: list[str] = []
    try:
        target: str | None = os.readlink(path)
    except OSError as exc:
        target = None
        scan_errors.append(f"readlink {exc.__class__.__name__}")
    return {
        "asset_type": "TOP_LEVEL_SYMLINK",
        "claim_status": "UNVERIFIED_LEGACY",
        "direct_claim_or_paper_eligible": False,
        "relative_path": relative_path,
        "scan_complete": not scan_errors,
        "scan_errors": scan_errors,
        "target": target,
        "target_followed": False,
    }


def build_inventory(results_root: Path) -> dict[str, Any]:
    root = results_root.expanduser().resolve(strict=True)
    if not root.is_dir():
        raise InventoryError(f"Results root is not a directory: {root}")

    runs: list[dict[str, Any]] = []
    non_run_assets: list[dict[str, Any]] = []
    top_level_scan_errors: list[str] = []
    try:
        with os.scandir(root) as scanner:
            entries = sorted(scanner, key=lambda candidate: candidate.name)
    except OSError as exc:
        entries = []
        top_level_scan_errors.append(f".: {exc.__class__.__name__}")
    for entry in entries:
        try:
            entry_stat = entry.stat(follow_symlinks=False)
        except OSError as exc:
            top_level_scan_errors.append(f"{entry.name}: {exc.__class__.__name__}")
            continue
        mode = entry_stat.st_mode
        if stat.S_ISLNK(mode):
            non_run_assets.append(_inventory_top_level_symlink(entry.name, Path(entry.path)))
        elif stat.S_ISDIR(mode):
            if entry.name.startswith("_") or entry.name.casefold() in NON_RUN_DIRECTORY_NAMES:
                asset_dir = Path(entry.path)
                if not _is_within(asset_dir.resolve(strict=True), root):
                    raise InventoryError(f"Control directory escapes Results root: {entry.name}")
                non_run_assets.append(_inventory_non_run_directory(asset_dir, root))
                continue
            run_dir = Path(entry.path)
            # scandir + lstat already prevents a top-level symlink.  Keep the
            # resolved-boundary assertion as a fail-closed defense in depth.
            if not _is_within(run_dir.resolve(strict=True), root):
                raise InventoryError(f"Run directory escapes Results root: {entry.name}")
            runs.append(inventory_run(run_dir, root))
        elif stat.S_ISREG(mode):
            non_run_assets.append(
                _inventory_top_level_file(
                    entry.name,
                    ScannedFile(
                        path=Path(entry.path),
                        size_bytes=entry_stat.st_size,
                        mtime_ns=entry_stat.st_mtime_ns,
                    ),
                )
            )
        else:
            top_level_scan_errors.append(f"{entry.name}: unsupported_file_type")

    grades: dict[str, int] = {}
    completions: dict[str, int] = {}
    for run in runs:
        grades[run["evidence_grade"]] = grades.get(run["evidence_grade"], 0) + 1
        classification = run["completion_signal"]["classification"]
        completions[classification] = completions.get(classification, 0) + 1

    all_scan_errors = list(top_level_scan_errors)
    all_scan_errors.extend(
        f"run:{run['relative_path']}:{error}"
        for run in runs
        for error in run["scan_errors"]
    )
    all_scan_errors.extend(
        f"asset:{asset['relative_path']}:{error}"
        for asset in non_run_assets
        for error in asset["scan_errors"]
    )
    checkpoint_count = sum(len(run["checkpoints"]) for run in runs)
    checkpoint_count += sum(
        1
        for asset in non_run_assets
        for file_record in asset.get("file_index", [asset])
        if "role_heuristic" in file_record
    )

    return {
        "eligibility_policy": {
            "all_legacy_records_status": "UNVERIFIED_LEGACY",
            "direct_claim_or_paper_eligible": False,
            "evidence_grade_definitions": {
                "E0_MINIMAL": "valid run_meta absent",
                "E1_METADATA": "valid run_meta present but core evidence incomplete",
                "E2_CORE_ARTIFACTS_AND_COMPLETION_REPORT_PRESENT": (
                    "configuration, graph, summary and a legacy completion report are present; "
                    "manifest absent and completion not independently verified"
                ),
                "E3_MANIFEST_AND_COMPLETION_REPORT_PRESENT": (
                    "E2 file presence plus artifact_manifest presence; neither manifest contents "
                    "nor completion are trusted by this inventory"
                ),
            },
            "grade_basis": "evidence_completeness_only_not_result_direction_or_performance",
        },
        "hash_policy": {
            "algorithm": "sha256",
            "candidate_paths": list(HASH_CANDIDATES),
            "checkpoint_hash_status": "PENDING_NOT_HASHED_BY_QUICK_INVENTORY",
            "max_bytes": MAX_HASH_BYTES,
            "never_hash_suffixes": sorted(NEVER_HASH_SUFFIXES),
        },
        "inventory_semantics": {
            "deletion_authorization": False,
            "inventory_class": "QUICK_INDEX_ONLY",
            "migration_or_preservation_proof": False,
            "required_before_copy_or_delete": (
                "source_and_destination_content_hashes_plus_explicit_lineage_review"
            ),
            "warning": (
                "file_presence_metadata_and_partial_hashes_do_not_prove_complete_preservation"
            ),
        },
        "legacy_completion_clue_policy": {
            "interrupt_marker": "run_trace/interrupt_meta.json presence is a conservative interruption clue",
            "log_marker": f"Elapsed time line within final {MAX_LOG_TAIL_BYTES} logfile bytes",
            "modern_natural_end_established_by_inventory": False,
        },
        "non_run_assets": non_run_assets,
        "results_root": str(root),
        "runs": runs,
        "schema_version": SCHEMA_VERSION,
        "summary": {
            "checkpoint_count": checkpoint_count,
            "completion_counts": dict(sorted(completions.items())),
            "evidence_grade_counts": dict(sorted(grades.items())),
            "non_run_asset_count": len(non_run_assets),
            "run_count": len(runs),
            "scan_complete": not all_scan_errors,
            "scan_error_count": len(all_scan_errors),
            "scan_errors": all_scan_errors,
        },
    }


def write_inventory(payload: dict[str, Any], output_path: Path, results_root: Path) -> None:
    root = results_root.expanduser().resolve(strict=True)
    output = output_path.expanduser()
    output_parent = output.parent.resolve(strict=True)
    resolved_output = output_parent / output.name
    if _is_within(resolved_output, root):
        raise InventoryError("Output must be outside the read-only Results root")
    if output.exists() and output.is_symlink():
        raise InventoryError("Output path must not be a symlink")

    encoded = (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=output_parent, prefix=f".{output.name}.", suffix=".tmp", delete=False
        ) as handle:
            temp_name = handle.name
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, resolved_output)
        temp_name = None
    finally:
        if temp_name is not None:
            Path(temp_name).unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results_root", type=Path, help="legacy Results directory to inspect read-only")
    parser.add_argument("--out", required=True, type=Path, help="JSON output path outside Results")
    args = parser.parse_args()

    try:
        payload = build_inventory(args.results_root)
        write_inventory(payload, args.out, args.results_root)
    except (InventoryError, FileNotFoundError, NotADirectoryError, PermissionError) as exc:
        parser.error(str(exc))
    if payload["summary"].get("scan_complete") is not True:
        print(
            f"INCOMPLETE {args.out} runs={payload['summary']['run_count']} "
            f"scan_errors={payload['summary'].get('scan_error_count', 0)}",
            file=sys.stderr,
        )
        return 3
    print(f"WROTE {args.out} runs={payload['summary']['run_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
