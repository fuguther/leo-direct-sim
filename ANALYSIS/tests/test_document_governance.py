import hashlib
import re
import sys
from datetime import date
from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts.check_document_governance import (
    CURRENT_STATUSES,
    _covered_paths,
    _matches,
    audit_repository,
    load_registry,
)


ROOT = Path(__file__).resolve().parents[2]

# Directive documents that must be registered exactly once and may direct
# current work only while their status is current.
NEWLY_GOVERNED_PATHS = (
    ".github/pull_request_template.md",
    "CODE/data/traffic/README.md",
    "PAPER/README.md",
)

CURRENT_EXECUTION_DOCS = (
    "EXPERIMENTS/README.md",
    "CODE/work/README.md",
    "CODE/experiment_platform/AGENT_EXPERIMENT_PROTOCOL.md",
)
FORBIDDEN_CURRENT_PATH_REFERENCES = (
    "PLATFORM/authorize_experiment.py",
    "CODE/run.py",
    "ARCHIVE-20260803",
)
CANONICAL_FORMAL_RUNNER = "CODE/scripts/remote/run-remote.sh"
ARTIFACT_CONTRACT_PATH = ROOT / "EXPERIMENTS" / "contracts" / "run-artifact-contract.md"

# remote_job imports its sibling deployment_guard as a top-level name (the
# canonical VM layout), so expose that directory before importing it.
sys.path.insert(0, str(ROOT / "CODE" / "scripts" / "remote"))

from CODE.scripts.remote import remote_job as remote_runner
V2_EVIDENCE_FAMILY_ARTIFACTS = (
    "receipt.json",
    "formal_run.json",
    "governance_receipt.json",
)
_REPO_PATH_LEADERS = (
    "CODE/", "EXPERIMENTS/", "ANALYSIS/", "scripts/", ".github/", "PAPER/",
    "LITERATURE/", "docs/",
)
_TEMPLATE_PLACEHOLDERS = ("...", "<", ">", "*", "?", "[", "]", "$", " ", "YYYY", "NNN")


def _fenced_blocks(text: str) -> list[str]:
    """Whitespace-split tokens from every fenced markdown code block."""
    return [
        token
        for match in re.finditer(r"```[a-z]*\n(.*?)```", text, flags=re.S)
        for token in match.group(1).split()
    ]


def _code_tokens(text: str) -> list[str]:
    """Backtick tokens plus whitespace-split tokens from fenced code blocks."""
    return [
        *re.findall(r"`([^`]+)`", text),
        *_fenced_blocks(text),
    ]


def _concrete_paths(text: str, doc_dir: Path) -> list[Path]:
    """Path-like tokens that are concrete repo paths (or doc-relative paths).

    Scans both backtick tokens and fenced code blocks, so commands inside
    fence blocks are covered as well as inline tokens.
    """
    paths: list[Path] = []
    for token in _code_tokens(text):
        if any(marker in token for marker in _TEMPLATE_PLACEHOLDERS):
            continue
        if token.startswith(("./", "../")):
            paths.append((doc_dir / token).resolve())
        elif token.startswith(_REPO_PATH_LEADERS):
            paths.append((ROOT / token).resolve())
    return paths


def _markdown_sections(text: str) -> dict[str, str]:
    """Split a markdown document into its top-level sections by title."""
    sections: dict[str, str] = {}
    current: str | None = None
    buffer: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buffer)
            current = line[3:].strip()
            buffer = []
        else:
            buffer.append(line)
    if current is not None:
        sections[current] = "\n".join(buffer)
    return sections


def _section(sections: dict[str, str], prefix: str) -> str:
    for title, body in sections.items():
        if title.startswith(prefix):
            return body
    raise AssertionError(f"document is missing a section starting with {prefix!r}")


def _entry(path: str, **overrides: object) -> dict:
    entry = {
        "path": path,
        "status": "CURRENT-CONTRACT",
        "purpose": "test fixture",
        "may_direct_current_work": True,
        "owner": "test",
        "last_reviewed": "2026-08-23",
        "review_interval_days": 30,
        "replacement": None,
        "require_banner": False,
        "archive_candidate": False,
        "suggested_archive_target": None,
    }
    entry.update(overrides)
    return entry


def _registry(*entries: dict, coverage: list[str] | None = None) -> dict:
    return {
        "schema": "leo-document-governance/v1",
        "updated_at": "2026-08-23",
        "allowed_statuses": [
            "CURRENT-CONTRACT",
            "CURRENT-VOLATILE",
            "SUPPORTING",
            "ROLLING-LOG",
            "EVIDENCE-SNAPSHOT",
            "HISTORICAL",
            "SUPERSEDED",
        ],
        "coverage": coverage or [entry["path"] for entry in entries],
        "entry_point_invariants": [],
        "entries": list(entries),
    }


def test_shallow_glob_does_not_match_nested_document():
    entry = {"glob": "ANALYSIS/HISTORY/*.md"}

    assert _matches(entry, "ANALYSIS/HISTORY/root.md") is True
    assert _matches(entry, "ANALYSIS/HISTORY/topic/nested.md") is False


def test_repository_document_governance_is_clean():
    registry = load_registry(ROOT / "ANALYSIS" / "DOCUMENT-STATUS.json")
    report = audit_repository(ROOT, registry, today=date(2026, 8, 23))
    assert report["errors"] == []


@pytest.mark.parametrize("relative_path", NEWLY_GOVERNED_PATHS)
def test_directive_document_governed_by_exactly_one_current_entry(relative_path):
    registry = load_registry(ROOT / "ANALYSIS" / "DOCUMENT-STATUS.json")
    covered = _covered_paths(ROOT, registry.get("coverage") or [])
    assert relative_path in covered, (
        f"{relative_path} is not covered by any registry coverage pattern"
    )
    matching = [
        entry
        for entry in registry.get("entries") or []
        if isinstance(entry, dict) and _matches(entry, relative_path)
    ]
    assert len(matching) == 1, (
        f"{relative_path} must be governed by exactly one registry entry, "
        f"matched {len(matching)}"
    )
    entry = matching[0]
    assert entry["status"] in CURRENT_STATUSES, (
        f"{relative_path} may direct work only with a current status, "
        f"got {entry['status']!r}"
    )
    assert entry["may_direct_current_work"] is True


def test_current_contract_path_references_exist_in_checkout():
    for relative_doc in CURRENT_EXECUTION_DOCS:
        text = (ROOT / relative_doc).read_text(encoding="utf-8")
        for candidate in _concrete_paths(text, (ROOT / relative_doc).parent):
            assert candidate.exists(), (
                f"{relative_doc} presents a path that does not exist in this "
                f"checkout: {candidate.relative_to(ROOT)}"
            )


def test_nonexistent_legacy_path_references_absent_from_current_docs():
    for relative_doc in CURRENT_EXECUTION_DOCS:
        text = (ROOT / relative_doc).read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_CURRENT_PATH_REFERENCES:
            assert forbidden not in text, (
                f"{relative_doc} still presents nonexistent "
                f"{forbidden!r} as current"
            )


def test_run_artifact_contract_separates_three_families():
    text = ARTIFACT_CONTRACT_PATH.read_text(encoding="utf-8")
    assert "leo_sim_v2" in text, "artifact contract must name the leo_sim_v2 family"
    for name in V2_EVIDENCE_FAMILY_ARTIFACTS:
        assert name in text, f"V2 evidence family must name {name}"
    assert "不能替代" in text, (
        "generic artifacts must be explicitly non-substitutable for V2 governance artifacts"
    )
    assert "claim" in text, (
        "contract must state that no artifact family alone establishes a claim"
    )
    sections = _markdown_sections(text)
    legacy = _section(sections, "通用/legacy")
    core = _section(sections, "leo_sim_v2 核心")
    increment = _section(sections, "leo_sim_v2 正式")
    # The legacy/generic file family keeps its own file names and runtime scope.
    assert "run_trace/run_meta.json" in legacy
    assert "legacy_gateway" in legacy
    # The leo_sim V2 core result files are what the local leo_sim CLI produces;
    # they are NOT the legacy run_trace family and NOT formal evidence alone.
    assert "run_trace/run_meta.json" not in core
    assert "receipt.json" in core
    assert "resolved_config.json" in core
    assert "不得升级为正式证据" in core
    # The formal governance increment is only produced by the formal chain and
    # must not be claimed as a local CLI output.
    for name in ("formal_run.json", "governance_receipt.json",
                 "_external_launch_witness"):
        assert name in increment, f"formal increment must name {name}"
        assert name not in core, (
            f"{name} is a formal increment and must not be presented as a "
            "local leo_sim CLI output"
        )


def test_governance_receipt_producer_is_the_remote_runner():
    remote_source = (
        ROOT / "CODE" / "scripts" / "remote" / "remote_job.py"
    ).read_text(encoding="utf-8")
    assert "def build_v2_governance_receipt(" in remote_source, (
        "the code fact this regression protects is missing from remote_job.py"
    )
    text = ARTIFACT_CONTRACT_PATH.read_text(encoding="utf-8")
    increment = _section(_markdown_sections(text), "leo_sim_v2 正式")
    assert "remote_job.py" in increment, (
        "the contract must attribute governance_receipt.json production to remote_job.py"
    )
    assert "自然结束后" in increment, (
        "the contract must state the receipt is built after the formal run ends"
    )
    assert "authorize_experiment" not in increment, (
        "authorize_experiment.py must not be presented as the governance "
        "receipt producer (it only verifies predecessor evidence)"
    )
    assert "finalize_decision" not in increment, (
        "finalize_decision.py must not be presented as the governance receipt "
        "producer (it only materializes the finalization)"
    )
    assert "v2_analysis" in increment, (
        "the contract must name v2_analysis as the posterior verifier"
    )
    assert "后验" in increment


def _patch_remote_runner_canonical_paths(monkeypatch, tmp_path):
    """Point remote_job's canonical path constants at throwaway test paths."""
    code = tmp_path / "code"
    code.mkdir()
    experiments = tmp_path / "experiments"
    experiments.mkdir()
    logs = tmp_path / "logs"
    logs.mkdir()
    status = tmp_path / "status.json"
    for name, value in (
        ("CANONICAL_CODE", code),
        ("CANONICAL_STATUS", status),
        ("CANONICAL_LOGS", logs),
        ("CANONICAL_EXPERIMENTS", experiments),
    ):
        monkeypatch.setattr(remote_runner, name, value)
    return code, experiments, logs, status


@pytest.mark.parametrize(
    ("runtime_kind", "config_name", "valid"),
    [
        ("legacy_gateway", "control.s20260715.config.json", True),
        ("leo_sim_v2", "EXP-PILOT-main-s7.leo-sim.yaml", True),
        ("leo_sim_v2", "control.s20260715.config.json", False),
        ("legacy_gateway", "EXP-PILOT-main-s7.leo-sim.yaml", False),
    ],
)
def test_remote_job_validate_formal_paths_suffix_rules(
    monkeypatch, tmp_path, runtime_kind, config_name, valid
):
    code, experiments, logs, status = _patch_remote_runner_canonical_paths(
        monkeypatch, tmp_path
    )
    config = experiments / config_name
    config.write_text("{}\n", encoding="utf-8")
    authorization = experiments / "authorization.json"
    authorization.write_text("{}\n", encoding="utf-8")
    args = SimpleNamespace(
        workdir=str(code),
        status_file=str(status),
        log_file=str(logs / "run.log"),
        config=str(config),
        authorization=str(authorization),
        runtime_kind=runtime_kind,
    )
    if valid:
        _workdir, _status, _log, resolved_config, resolved_authorization = (
            remote_runner.validate_formal_paths(args)
        )
        assert resolved_config.name == config_name
        assert resolved_authorization == authorization
    else:
        with pytest.raises(ValueError, match="compiled"):
            remote_runner.validate_formal_paths(args)


def test_protocol_presents_only_v2_as_current_formal_launch():
    protocol = (
        ROOT / "CODE" / "experiment_platform" / "AGENT_EXPERIMENT_PROTOCOL.md"
    ).read_text(encoding="utf-8")
    assert CANONICAL_FORMAL_RUNNER in protocol, (
        "formal execution must point at the canonical remote runner"
    )
    assert "--runtime-kind leo_sim_v2" in protocol
    for match in re.finditer(r"```bash\n(.*?)```", protocol, flags=re.S):
        block = match.group(1)
        if "run-remote.sh" in block:
            assert "--runtime-kind leo_sim_v2" in block, (
                "the only current runnable launch example is the leo_sim_v2 "
                "route; legacy_gateway must not appear as a runnable block"
            )
    assert "外部旧平台" in protocol, (
        "legacy_gateway must be described as an external old-platform contract"
    )
    assert "不能从本仓库独立完成" in protocol, (
        "legacy execution must be stated as impossible from this repository alone"
    )
    assert "不属于正式执行" in protocol, (
        "protocol must state that local CLI/smoke commands are not formal execution"
    )


def test_governance_receipt_existence_is_not_formal_admission():
    text = ARTIFACT_CONTRACT_PATH.read_text(encoding="utf-8")
    increment = _section(_markdown_sections(text), "leo_sim_v2 正式")
    assert "research_eligible" in increment
    assert "正式准入" in increment, (
        "the contract must separate file existence from formal admission"
    )
    assert "可能" in increment, (
        "the contract must allow the governance receipt to exist even in "
        "failed/non-natural-end cases"
    )
    assert "自身" in increment, (
        "formal_run.json must be described as written by leo_sim itself"
    )


def test_stale_current_document_fails_loud(tmp_path):
    (tmp_path / "CURRENT.md").write_text("# current\n", encoding="utf-8")
    registry = _registry(
        _entry(
            "CURRENT.md",
            status="CURRENT-VOLATILE",
            last_reviewed="2026-01-01",
            review_interval_days=7,
        )
    )

    report = audit_repository(tmp_path, registry, today=date(2026, 8, 23))

    assert any(error["code"] == "STALE_CURRENT" for error in report["errors"])
    assert report["stale"] == ["CURRENT.md"]


def test_unregistered_governed_document_fails_loud(tmp_path):
    (tmp_path / "known.md").write_text("# known\n", encoding="utf-8")
    (tmp_path / "forgotten.md").write_text("# forgotten\n", encoding="utf-8")
    registry = _registry(_entry("known.md"), coverage=["*.md"])

    report = audit_repository(tmp_path, registry, today=date(2026, 8, 23))

    assert any(
        error["code"] == "UNCLASSIFIED_DOCUMENT"
        and error["path"] == "forgotten.md"
        for error in report["errors"]
    )


def test_protected_document_hash_detects_casual_edit(tmp_path):
    protected = tmp_path / "AGENTS.md"
    protected.write_text("stable constitution\n", encoding="utf-8")
    expected = hashlib.sha256(protected.read_bytes()).hexdigest()
    registry = _registry(
        _entry("AGENTS.md", protected_sha256=expected, review_interval_days=90)
    )
    protected.write_text("casual status edit\n", encoding="utf-8")

    report = audit_repository(tmp_path, registry, today=date(2026, 8, 23))

    assert any(
        error["code"] == "PROTECTED_CONTENT_CHANGED"
        and error["path"] == "AGENTS.md"
        for error in report["errors"]
    )


def test_archive_candidates_are_reported_without_moving_files(tmp_path):
    historical = tmp_path / "old.md"
    historical.write_text("# old\n", encoding="utf-8")
    registry = _registry(
        _entry(
            "old.md",
            status="HISTORICAL",
            may_direct_current_work=False,
            last_reviewed=None,
            review_interval_days=None,
            archive_candidate=True,
            suggested_archive_target="HISTORY/old.md",
        )
    )

    report = audit_repository(tmp_path, registry, today=date(2026, 8, 23))

    assert report["archive_candidates"] == [
        {"path": "old.md", "suggested_target": "HISTORY/old.md"}
    ]
    assert historical.exists()
    assert not (tmp_path / "HISTORY" / "old.md").exists()
