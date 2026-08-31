from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts" / "check_workspace_hygiene.py"


def run(*args: str, cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=cwd,
        text=True,
        capture_output=True,
        check=check,
    )


def make_repo(path: Path) -> Path:
    path.mkdir()
    run("git", "init", "-q", cwd=path)
    run("git", "config", "user.name", "Workspace Hygiene Test", cwd=path)
    run("git", "config", "user.email", "workspace-hygiene@example.invalid", cwd=path)
    (path / ".gitignore").write_text(
        "GROUP-MEETINGS-LOCAL/\nout/\n.pytest_cache/\nscratch.bin\n",
        encoding="utf-8",
    )
    (path / "tracked.txt").write_text("base\n", encoding="utf-8")
    run("git", "add", ".gitignore", "tracked.txt", cwd=path)
    run("git", "commit", "-q", "-m", "base", cwd=path)
    return path


def check_repo(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return run(sys.executable, str(CHECKER), *args, cwd=repo, check=False)


def report_for(tmp_path: Path, repo: Path, *args: str) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
    report = tmp_path / "workspace-report.json"
    completed = check_repo(repo, *args, "--report", str(report))
    payload = json.loads(report.read_text(encoding="utf-8")) if report.exists() else {}
    return completed, payload


def only_worktree(payload: dict[str, object]) -> dict[str, object]:
    worktrees = payload["worktrees"]
    assert isinstance(worktrees, list) and len(worktrees) == 1
    item = worktrees[0]
    assert isinstance(item, dict)
    return item


def test_clean_repo_continues_start_and_handoff(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "repo")
    for phase in ("start", "handoff"):
        completed, payload = report_for(tmp_path, repo, "--phase", phase)
        assert completed.returncode == 0, completed.stderr
        item = only_worktree(payload)
        assert item["classes"] == ["CLEAN"]
        assert item["decision"] == "CONTINUE"


def test_protected_local_archive_is_visible_but_nonfatal(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "repo")
    note = repo / "GROUP-MEETINGS-LOCAL" / "note.md"
    note.parent.mkdir()
    note.write_text("private\n", encoding="utf-8")

    completed, payload = report_for(tmp_path, repo, "--phase", "start")

    assert completed.returncode == 0, completed.stderr
    item = only_worktree(payload)
    assert item["classes"] == ["PROTECTED_LOCAL"]
    assert item["decision"] == "CONTINUE"
    assert any(entry["path"] == "GROUP-MEETINGS-LOCAL/" for entry in item["entries"])


def test_ignored_result_is_evidence_not_clean(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "repo")
    receipt = repo / "out" / "run-1" / "receipt.json"
    receipt.parent.mkdir(parents=True)
    receipt.write_text("{}\n", encoding="utf-8")

    completed, payload = report_for(tmp_path, repo, "--phase", "start")

    assert completed.returncode == 1
    item = only_worktree(payload)
    assert item["classes"] == ["EVIDENCE_PRESENT"]
    assert item["decision"] == "STOP_AND_INSPECT"
    assert item["protection"] == "DIRTY-PROTECT"


def test_ephemeral_cache_blocks_handoff_only(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "repo")
    cache = repo / ".pytest_cache" / "state"
    cache.parent.mkdir()
    cache.write_text("cache\n", encoding="utf-8")

    start, start_payload = report_for(tmp_path, repo, "--phase", "start")
    assert start.returncode == 0
    assert only_worktree(start_payload)["classes"] == ["EPHEMERAL"]

    handoff, handoff_payload = report_for(tmp_path, repo, "--phase", "handoff")
    assert handoff.returncode == 1
    assert only_worktree(handoff_payload)["decision"] == "STOP_AND_INSPECT"


def test_ordinary_untracked_and_tracked_changes_are_dirty(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "repo")
    (repo / "note.md").write_text("untracked\n", encoding="utf-8")
    (repo / "tracked.txt").write_text("changed\n", encoding="utf-8")

    completed, payload = report_for(tmp_path, repo, "--phase", "start")

    assert completed.returncode == 1
    item = only_worktree(payload)
    assert item["classes"] == ["DIRTY"]
    states = {entry["git_state"] for entry in item["entries"]}
    assert {"tracked", "untracked"} <= states


def test_unknown_ignored_path_requires_classification(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "repo")
    (repo / "scratch.bin").write_text("unknown ignored\n", encoding="utf-8")

    completed, payload = report_for(tmp_path, repo, "--phase", "start")

    assert completed.returncode == 1
    item = only_worktree(payload)
    assert item["classes"] == ["UNEXPECTED_IGNORED"]
    assert item["decision"] == "STOP_AND_INSPECT"


def test_family_label_never_hides_tracked_dirt(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "repo")
    note = repo / "GROUP-MEETINGS-LOCAL" / "tracked.md"
    note.parent.mkdir()
    note.write_text("base\n", encoding="utf-8")
    run("git", "add", "-f", str(note.relative_to(repo)), cwd=repo)
    run("git", "commit", "-q", "-m", "tracked protected fixture", cwd=repo)
    note.write_text("changed\n", encoding="utf-8")

    completed, payload = report_for(tmp_path, repo, "--phase", "start")

    assert completed.returncode == 1
    item = only_worktree(payload)
    assert item["classes"] == ["DIRTY", "PROTECTED_LOCAL"]
    entry = next(entry for entry in item["entries"] if entry["path"].endswith("tracked.md"))
    assert entry == {
        "family": "PROTECTED_LOCAL",
        "git_state": "tracked",
        "path": "GROUP-MEETINGS-LOCAL/tracked.md",
    }


def test_report_inside_worktree_is_rejected_without_writing(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "repo")
    report = repo / "self-polluting-report.json"

    completed = check_repo(repo, "--phase", "start", "--report", str(report))

    assert completed.returncode == 2
    assert "outside" in completed.stderr.lower()
    assert not report.exists()


def test_outside_report_matches_human_inventory(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "repo")
    receipt = repo / "out" / "run" / "receipt.json"
    receipt.parent.mkdir(parents=True)
    receipt.write_text("{}\n", encoding="utf-8")
    completed, payload = report_for(tmp_path, repo, "--phase", "start")

    assert completed.returncode == 1
    item = only_worktree(payload)
    assert "EVIDENCE_PRESENT" in completed.stdout
    assert item["classes"] == ["EVIDENCE_PRESENT"]
    assert payload["exit_code"] == 1


def test_all_worktrees_inventory_protects_evidence_without_failing(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "repo")
    evidence_worktree = tmp_path / "evidence-worktree"
    run("git", "worktree", "add", "-q", "-b", "evidence", str(evidence_worktree), cwd=repo)
    result_dir = evidence_worktree / "out" / "unique-run"
    result_dir.mkdir(parents=True)
    (result_dir / "receipt.json").write_text("{}\n", encoding="utf-8")
    report = tmp_path / "all-worktrees.json"

    completed = check_repo(repo, "--all-worktrees", "--report", str(report))

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(report.read_text(encoding="utf-8"))
    by_path = {item["path"]: item for item in payload["worktrees"]}
    evidence = by_path[str(evidence_worktree.resolve())]
    assert evidence["classes"] == ["EVIDENCE_PRESENT"]
    assert evidence["recoverable"] is False
    assert evidence["protection"] == "DIRTY-PROTECT"


def test_non_git_directory_fails_loud(tmp_path: Path) -> None:
    completed = check_repo(tmp_path, "--phase", "start")

    assert completed.returncode == 2
    assert "git" in completed.stderr.lower()
