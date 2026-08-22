# Agent Document Governance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent current and future agents from treating stale project documents, old experiment artifacts, or historical conclusions as current instructions.

**Architecture:** A single JSON registry classifies governed documents by authority and review cadence. A standard-library checker validates coverage, replacement links, status banners, entry points, and staleness; the same checker runs at agent startup, in pull requests, and on a weekly GitHub Actions schedule. It reports archive candidates but never moves or rewrites tracked files.

**Tech Stack:** Markdown, JSON, Python 3.11 standard library, pytest, GitHub Actions.

---

## File map

- Create `AGENT-START-HERE.md`: mandatory human/agent entry point and authority order.
- Create `ANALYSIS/DOCUMENT-STATUS.json`: machine-readable classification and review cadence.
- Create `scripts/check_document_governance.py`: deterministic structural/staleness checker and JSON report writer.
- Create `ANALYSIS/tests/test_document_governance.py`: checker and anti-regression tests.
- Create `.github/workflows/document-governance.yml`: weekly scheduled audit and report artifact.
- Modify `.github/workflows/test.yml`: run the checker in the required PR test job.
- Modify `AGENTS.md`, `README.md`, `ANALYSIS/README.md`, `EXPERIMENTS/README.md`, and `CODE/work/README.md`: correct the entry points and immutable-evidence boundaries.
- Modify selected high-risk historical documents: add status banners without changing historical body text or numbers.

### Task 1: Lock the governance failures with tests

**Files:**
- Create: `ANALYSIS/tests/test_document_governance.py`

- [ ] **Step 1: Write failing tests for the checker contract**

```python
from datetime import date
from pathlib import Path

from scripts.check_document_governance import audit_repository, load_registry


ROOT = Path(__file__).resolve().parents[2]


def test_repository_document_governance_is_clean():
    registry = load_registry(ROOT / "ANALYSIS" / "DOCUMENT-STATUS.json")
    report = audit_repository(ROOT, registry, today=date(2026, 8, 23))
    assert report["errors"] == []


def test_stale_current_document_fails_loud(tmp_path):
    registry = {
        "allowed_statuses": ["CURRENT-VOLATILE"],
        "coverage": ["CURRENT.md"],
        "entries": [{
            "path": "CURRENT.md",
            "status": "CURRENT-VOLATILE",
            "purpose": "test",
            "may_direct_current_work": True,
            "owner": "status",
            "last_reviewed": "2026-01-01",
            "review_interval_days": 7,
            "replacement": None,
            "require_banner": False,
            "archive_candidate": False,
        }],
    }
    (tmp_path / "CURRENT.md").write_text("# current\n", encoding="utf-8")
    report = audit_repository(tmp_path, registry, today=date(2026, 8, 23))
    assert any(error["code"] == "STALE_CURRENT" for error in report["errors"])
```

- [ ] **Step 2: Run the tests and verify RED**

Run: `python -m pytest ANALYSIS/tests/test_document_governance.py -q`

Expected: collection fails because `scripts.check_document_governance` does not exist.

### Task 2: Implement registry loading and deterministic auditing

**Files:**
- Create: `scripts/__init__.py`
- Create: `scripts/check_document_governance.py`
- Create: `ANALYSIS/DOCUMENT-STATUS.json`

- [ ] **Step 1: Implement the checker**

The checker must expose:

```python
def load_registry(path: Path) -> dict: ...
def audit_repository(root: Path, registry: dict, today: date | None = None) -> dict: ...
def main(argv: list[str] | None = None) -> int: ...
```

`audit_repository` must return `schema`, `checked_at`, `errors`, `warnings`, `stale`, and `archive_candidates`. It must validate allowed status values, unique exact paths, glob coverage, existing replacements, required banners in the first twelve lines, protected content hashes, entry-point invariants, and `last_reviewed + review_interval_days`. The CLI must support `--root`, `--registry`, `--today`, `--mode {structure,staleness,all}`, and `--report`; it exits nonzero when the selected mode has errors.

- [ ] **Step 2: Populate the registry**

Use exactly these status values:

```json
[
  "CURRENT-CONTRACT",
  "CURRENT-VOLATILE",
  "SUPPORTING",
  "ROLLING-LOG",
  "EVIDENCE-SNAPSHOT",
  "HISTORICAL",
  "SUPERSEDED"
]
```

Classify root guidance, every Markdown file under `ANALYSIS/`, experiment/work README and runbook guidance, and `docs/superpowers/` plans/specs. Current volatile entries receive finite review intervals; immutable history receives no review interval. Superseded entries must name an existing replacement.

- [ ] **Step 3: Run tests and inspect remaining classification errors**

Run: `python -m pytest ANALYSIS/tests/test_document_governance.py -q`

Expected: checker imports successfully; repository test reports the still-unfixed entry-point and banner errors.

### Task 3: Establish the single entry point and evidence boundaries

**Files:**
- Create: `AGENT-START-HERE.md`
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `ANALYSIS/README.md`
- Modify: `EXPERIMENTS/README.md`
- Modify: `CODE/work/README.md`

- [ ] **Step 1: Write the mandatory start page**

It must state the read order, authority hierarchy, command below, and the rule that external state is never trusted from a repository snapshot alone:

```bash
python3 scripts/check_document_governance.py --mode all --report /tmp/leo-document-governance.json
```

- [ ] **Step 2: Correct repository entry points**

`AGENTS.md` must require the start page, point current migration choices to `PLATFORM-CAPABILITY-LEDGER.md`, and stop naming `NOTES.md` as the current truth source. Keep this edit minimal: do not add dates, current SHA, PR, VM, run, review cadence, or archive details. Register the resulting SHA-256 as protected content in the manifest so normal status updates do not keep editing the constitutional file. Other README files must distinguish current contracts from immutable historical evidence and revision-bound authorizations.

- [ ] **Step 3: Run structural audit**

Run: `python3 scripts/check_document_governance.py --mode structure --today 2026-08-23`

Expected: entry-point errors are gone; only missing historical banners, if any, remain.

### Task 4: Quarantine high-risk historical documents

**Files:**
- Modify: the exact `SUPERSEDED` and `HISTORICAL` paths listed in `ANALYSIS/DOCUMENT-STATUS.json`

- [ ] **Step 1: Add non-destructive status banners**

For every `SUPERSEDED` entry with `require_banner=true`, add this form within the first twelve lines:

```markdown
> **SUPERSEDED**：本文只保留历史证据，不得用于安排当前工作。现行入口见 `<replacement>`。
```

For high-risk historical reports, use `HISTORICAL SNAPSHOT` and state that branch/SHA/VM/run status must be reverified. Do not alter body text, tables, or numbers.

- [ ] **Step 2: Run the full deterministic audit**

Run: `python3 scripts/check_document_governance.py --mode all --today 2026-08-23 --report /tmp/leo-document-governance.json`

Expected: exit 0, zero errors, JSON report includes any archive candidates but no mutations.

### Task 5: Make governance continuous

**Files:**
- Modify: `.github/workflows/test.yml`
- Create: `.github/workflows/document-governance.yml`

- [ ] **Step 1: Add PR enforcement**

Add this step to the existing required pytest job before the test suite:

```yaml
- name: Check document governance
  run: python scripts/check_document_governance.py --mode all
```

- [ ] **Step 2: Add the weekly audit**

Create a workflow triggered by `workflow_dispatch` and `schedule: cron: "17 2 * * 1"`. It checks out main, runs the same script with `--mode all --report document-governance-report.json`, uploads the report with `if: always()`, and does not commit, open a PR, move files, or edit conclusions.

- [ ] **Step 3: Validate workflow syntax and governance tests**

Run:

```bash
python -c 'import yaml; [yaml.safe_load(open(p)) for p in [".github/workflows/test.yml", ".github/workflows/document-governance.yml"]]'
python -m pytest ANALYSIS/tests -q
```

Expected: YAML parses and all analysis tests pass.

### Task 6: Verify and deliver

**Files:**
- Verify all modified files; do not move or delete tracked paths.

- [ ] **Step 1: Run targeted and full tests**

Run:

```bash
python3 scripts/check_document_governance.py --mode all --today 2026-08-23
python -m pytest ANALYSIS/tests -q
python -m pytest CODE/leo_sim/tests CODE/tests -q
git diff --check
```

Expected: governance audit exits 0, all test suites pass with truthful passed/skipped counts, and diff check is clean.

- [ ] **Step 2: Inspect scope and archive candidates**

Run:

```bash
git diff --stat origin/main...HEAD
git diff --name-status origin/main...HEAD
python3 scripts/check_document_governance.py --mode all --today 2026-08-23 --report /tmp/leo-document-governance.json
```

Confirm there are no deleted, moved, or renamed paths. Extract archive candidates from the report for user approval; do not execute them.

- [ ] **Step 3: Commit, push, open a Draft PR, and wait for CI**

Use a scoped docs commit, push `codex/20260823-doc-governance`, create a Draft PR with the exact base/head SHA and test counts, then mark READY only after current CI is green and the diff still contains no destructive path changes.
