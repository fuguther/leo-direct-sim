#!/usr/bin/env python3
"""Classify Git worktree dirt without reading or changing reported assets."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


SCHEMA = "leo-workspace-hygiene/v1"
CLASS_ORDER = (
    "DIRTY",
    "EVIDENCE_PRESENT",
    "PROTECTED_LOCAL",
    "EPHEMERAL",
    "UNEXPECTED_IGNORED",
)
STOP_START = {"DIRTY", "EVIDENCE_PRESENT", "UNEXPECTED_IGNORED"}
STOP_HANDOFF = STOP_START | {"EPHEMERAL"}


class CheckerError(RuntimeError):
    """A fail-loud error in Git collection, parsing, or report output."""


def git(cwd: Path, *args: str) -> str:
    command = ["git", *args]
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise CheckerError(f"{' '.join(command)} failed: {detail}")
    return completed.stdout


def family_for(raw_path: str) -> str | None:
    path = raw_path.rstrip("/")
    parts = Path(path).parts
    basename = parts[-1] if parts else path
    if (
        path == "GROUP-MEETINGS-LOCAL"
        or path.startswith("GROUP-MEETINGS-LOCAL/")
        or path == "CODE/scripts/remote/remote.env"
        or basename == ".env"
        or basename.endswith(".pem")
    ):
        return "PROTECTED_LOCAL"
    if (
        basename == ".DS_Store"
        or "__pycache__" in parts
        or basename.endswith(".pyc")
        or ".pytest_cache" in parts
    ):
        return "EPHEMERAL"
    for root in ("CODE/Results", "Results", "leo_sim_out", "out"):
        if path == root or path.startswith(root + "/"):
            return "EVIDENCE_PRESENT"
    return None


def parse_status(output: str) -> list[dict[str, str | None]]:
    entries: list[dict[str, str | None]] = []
    for record in output.split("\0"):
        if not record:
            continue
        if len(record) < 4 or record[2] != " ":
            raise CheckerError(f"malformed git status record: {record!r}")
        code, path = record[:2], record[3:]
        if code == "??":
            git_state = "untracked"
        elif code == "!!":
            git_state = "ignored"
        else:
            git_state = "tracked"
        entries.append({
            "family": family_for(path),
            "git_state": git_state,
            "path": path,
        })
    return entries


def classify(entries: list[dict[str, str | None]]) -> list[str]:
    classes: set[str] = set()
    for entry in entries:
        state = entry["git_state"]
        family = entry["family"]
        if state in {"tracked", "untracked"}:
            classes.add("DIRTY")
        if family:
            classes.add(family)
        elif state == "ignored":
            classes.add("UNEXPECTED_IGNORED")
    return [name for name in CLASS_ORDER if name in classes] or ["CLEAN"]


def inspect_worktree(path: Path, phase: str) -> dict[str, Any]:
    root = Path(git(path, "rev-parse", "--show-toplevel").strip()).resolve()
    status = git(
        root,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
        "--ignored=matching",
        "--no-renames",
    )
    entries = parse_status(status)
    classes = classify(entries)
    stop_classes = STOP_HANDOFF if phase == "handoff" else STOP_START
    stop = bool(set(classes) & stop_classes)
    protected = bool(set(classes) & {"DIRTY", "EVIDENCE_PRESENT"})
    return {
        "classes": classes,
        "decision": "STOP_AND_INSPECT" if stop else "CONTINUE",
        "entries": sorted(entries, key=lambda item: str(item["path"])),
        "path": str(root),
        "protection": "DIRTY-PROTECT" if protected else "NONE",
        "recoverable": classes == ["CLEAN"],
    }


def worktree_paths(cwd: Path) -> list[Path]:
    output = git(cwd, "worktree", "list", "--porcelain")
    paths: list[Path] = []
    for block in output.strip().split("\n\n"):
        lines = block.splitlines()
        if not lines or not lines[0].startswith("worktree "):
            raise CheckerError(f"malformed git worktree record: {block!r}")
        if "bare" in lines[1:]:
            continue
        paths.append(Path(lines[0].removeprefix("worktree ")).resolve())
    if not paths:
        raise CheckerError("git worktree list returned no worktrees")
    return paths


def path_is_within(candidate: Path, root: Path) -> bool:
    return candidate == root or root in candidate.parents


def validate_report_path(report: Path, roots: list[Path]) -> Path:
    resolved = report.expanduser().resolve(strict=False)
    if any(path_is_within(resolved, root) for root in roots):
        raise CheckerError("--report must be outside every inspected worktree")
    return resolved


def print_human(worktrees: list[dict[str, Any]]) -> None:
    for item in worktrees:
        print(f"{item['path']}: {', '.join(item['classes'])} [{item['decision']}]")
        for entry in item["entries"]:
            family = f" family={entry['family']}" if entry["family"] else ""
            print(f"  {entry['git_state']}: {entry['path']}{family}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--phase", choices=("start", "handoff"))
    mode.add_argument("--all-worktrees", action="store_true")
    parser.add_argument("--report", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    cwd = Path.cwd()
    try:
        if args.all_worktrees:
            phase = "audit"
            roots = worktree_paths(cwd)
            worktrees = [inspect_worktree(path, "handoff") for path in roots]
            exit_code = 0
        else:
            phase = args.phase
            worktree = inspect_worktree(cwd, phase)
            roots = [Path(worktree["path"])]
            worktrees = [worktree]
            exit_code = 1 if worktree["decision"] == "STOP_AND_INSPECT" else 0
        report = validate_report_path(args.report, roots) if args.report else None
        payload = {
            "exit_code": exit_code,
            "mode": phase,
            "schema": SCHEMA,
            "worktrees": worktrees,
        }
        print_human(worktrees)
        if report:
            report.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        return exit_code
    except (CheckerError, OSError, ValueError) as exc:
        print(f"workspace-hygiene: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
