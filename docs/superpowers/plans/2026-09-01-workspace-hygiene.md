# Workspace Hygiene Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Consolidate the existing current project facts, preserve older research material as history, and add one read-only workspace check that exposes ignored evidence and local assets before task start or handoff.

**Architecture:** Existing CURRENT documents remain the only authorities; newer verified R02 facts are added at their top while dated sections remain unchanged below. A dependency-free Python checker reads only Git porcelain output and repository-relative path names, records Git state and path family independently, and returns a phase-specific exit code without deleting, hashing, or reading any asset.

**Tech Stack:** Markdown, JSON, YAML, Python 3 standard library, Git porcelain, pytest.

---

## File map

- Modify `.gitignore`: make the local group archive private in every clone.
- Modify `README.md` and `CODE/scripts/remote/remote.env.template`: repair executable examples and canonical VM paths.
- Modify `ANALYSIS/CURRENT-EXPERIMENT-READINESS.md`, `ANALYSIS/EXPERIMENT-PROGRAM.md`, `EXPERIMENTS/experiment-program.yaml`, and `ANALYSIS/PLATFORM-CAPABILITY-LEDGER.md`: synchronize the existing human and machine current facts without replacing historical sections.
- Create `ANALYSIS/claims/RESEARCH_CLAIMS.yaml`: materialize the existing empty claim-registry contract.
- Modify `PAPER/tests/test_eligible_claims.py`: lock the documented empty-registry CLI behavior.
- Create `scripts/check_workspace_hygiene.py`: the sole workspace classifier.
- Create `ANALYSIS/tests/test_workspace_hygiene.py`: disposable-repository behavior tests.
- Modify `AGENT-START-HERE.md`, `.github/pull_request_template.md`, and `ANALYSIS/DOCUMENT-STATUS.json`: integrate and govern the one checker.
- Modify local-only `/Users/lge/Desktop/leo-direct-sim/GROUP-MEETINGS-LOCAL/README.md`: point report preparation to the 2026-08-31 direction while retaining every older asset in place. This file is not committed.

### Task 1: Consolidate current facts and executable guidance

**Files:**
- Modify: `.gitignore`
- Modify: `README.md`
- Modify: `CODE/scripts/remote/remote.env.template`
- Modify: `ANALYSIS/CURRENT-EXPERIMENT-READINESS.md`
- Modify: `ANALYSIS/EXPERIMENT-PROGRAM.md`
- Modify: `EXPERIMENTS/experiment-program.yaml`
- Modify: `ANALYSIS/PLATFORM-CAPABILITY-LEDGER.md`
- Modify: `ANALYSIS/DOCUMENT-STATUS.json`
- Modify local-only: `/Users/lge/Desktop/leo-direct-sim/GROUP-MEETINGS-LOCAL/README.md`

- [ ] **Step 1: Recompute the current evidence facts before editing**

Run:

```bash
python3 - <<'PY'
import json
from collections import Counter
from pathlib import Path

root = Path("ANALYSIS/EXP-20260829-GLOBAL-PRESSURE-BRACKET-R02")
manifest = json.loads((root / "v2-paired/analysis-manifest.json").read_text())
summary = json.loads((root / "v2-paired/summary.json").read_text())
gate = json.loads((root / "v2-paired/claim-gate.json").read_text())
scenes = [json.loads(path.read_text()) for path in sorted((root / "scene-check").glob("*.json"))]
print(manifest["status"], len(manifest["verified_run_ids"]))
print(summary["design_accounting"])
print(Counter(scene["status"] for scene in scenes))
print(gate["status"], gate["cannot_claim"])
PY
```

Expected: `VERIFIED 24`, 12 unique configurations, 12 exact reexecutions, 24 `ACCESS_LIMITED`, and `READY_FOR_INDEPENDENT_CLAIM_REVIEW` with the bounded cannot-claim list.

- [ ] **Step 2: Add a new dated current section without altering old dated evidence**

At the top of each existing current Markdown authority, add a 2026-09-01 section that states:

```text
origin/main evidence snapshot: 79796b6 (PR #192)
R02: 24 VERIFIED run receipts = 12 unique resolved configurations + 12 exact reexecutions
scene checks: 24/24 ACCESS_LIMITED
claim gate: READY_FOR_INDEPENDENT_CLAIM_REVIEW
allowed: descriptive scene/load values and repeatability evidence
not allowed: ISL-pressure threshold/curve, causal claim, algorithm superiority,
information value, RL value, new-method contribution, or paper-ready conclusion
next gate: first resolve the access-limited scene/experiment question under the
2026-08-31 advisor-facing research direction; do not select an old task by date search
```

Mark the former 2026-08-29 heading as a historical snapshot; do not rewrite its numbers or delete any dated section.

- [ ] **Step 3: Synchronize machine-readable planning facts**

Update `EXPERIMENTS/experiment-program.yaml` to `updated_at: "2026-09-01"`, replace the two-run global-scene evidence with R02 24-run design accounting, and remove any machine-readable next-gate text that still directs Agents to preregister the already-completed bracket. Preserve blocked Q0, information, RL, and paper-claim gates.

- [ ] **Step 4: Repair executable examples and private-path handling**

Apply these exact contracts:

```text
.gitignore: GROUP-MEETINGS-LOCAL/
README: python3 -m CODE.leo_sim config validate CODE/leo_sim/profiles/smoke.yaml
README: python3 for run, receipt, platform check, and pytest
remote.env.template: /data/论文/leo-direct-sim and /data/论文/leo-direct-sim/CODE
```

- [ ] **Step 5: Update the local-only group archive entry**

Add a “当前唯一汇报入口” section to the local README pointing to:

```text
03-CURRENT-PREP/2026-08-31/论文方向梳理与文献调研任务.md
```

State that it is the current teacher-request interpretation, not a teacher-confirmed final paper plan; 2026-08-22/24/29/30 folders are historical/supporting and may be opened only for provenance or explicit comparison. Do not move, rename, or delete them.

- [ ] **Step 6: Synchronize registry review dates and verify**

Set `updated_at` and the `last_reviewed` dates only for entries actually reviewed in this task. Then run:

```bash
python3 scripts/check_document_governance.py --mode all --report /tmp/leo-document-governance.json
git diff --check
```

Expected: zero governance errors/warnings and no whitespace errors.

- [ ] **Step 7: Commit the consolidation**

```bash
git add .gitignore README.md CODE/scripts/remote/remote.env.template \
  ANALYSIS/CURRENT-EXPERIMENT-READINESS.md ANALYSIS/EXPERIMENT-PROGRAM.md \
  EXPERIMENTS/experiment-program.yaml ANALYSIS/PLATFORM-CAPABILITY-LEDGER.md \
  ANALYSIS/DOCUMENT-STATUS.json
git commit -m "docs: 收口当前实验事实与执行入口"
```

### Task 2: Close the empty claim-registry mismatch

**Files:**
- Create: `ANALYSIS/claims/RESEARCH_CLAIMS.yaml`
- Modify: `PAPER/tests/test_eligible_claims.py`

- [ ] **Step 1: Add a failing CLI test**

Add a subprocess test that creates an empty registry containing:

```yaml
schema: leo-research-claims/v1
claims: []
```

Run `PAPER/eligible_claims.py --registry <path>` and assert exit code 0 and parsed stdout `[]`.

- [ ] **Step 2: Run the targeted test**

Run:

```bash
python3 -m pytest PAPER/tests/test_eligible_claims.py -q
```

Expected before the registry exists at the documented default: the default-path behavior remains reproducibly missing or the new default-path assertion fails.

- [ ] **Step 3: Materialize the default empty registry**

Create exactly:

```yaml
schema: leo-research-claims/v1
claims: []
```

Do not populate claims and do not delete `PAPER/CLAIM_MAP.csv`.

- [ ] **Step 4: Verify CLI and tests**

Run:

```bash
python3 PAPER/eligible_claims.py
python3 -m pytest PAPER/tests/test_eligible_claims.py CODE/tests/test_claim_schema_contract.py -q
```

Expected: stdout `[]`; targeted tests pass.

- [ ] **Step 5: Commit**

```bash
git add ANALYSIS/claims/RESEARCH_CLAIMS.yaml PAPER/tests/test_eligible_claims.py
git commit -m "fix: 物化空论文主张登记表"
```

### Task 3: Specify workspace behavior with red tests

**Files:**
- Create: `ANALYSIS/tests/test_workspace_hygiene.py`

- [ ] **Step 1: Write disposable-repository helpers**

Use `tempfile.TemporaryDirectory`, `subprocess.run`, and `git init` to create isolated repositories. The helper must configure a local test identity, commit `.gitignore`, and invoke the future checker through `sys.executable`.

- [ ] **Step 2: Add classification tests**

Cover these exact cases:

```text
clean repo -> CLEAN, start 0, handoff 0
GROUP-MEETINGS-LOCAL/note.md ignored -> PROTECTED_LOCAL, start 0
out/run/receipt.json ignored -> EVIDENCE_PRESENT, start 1, handoff 1
.pytest_cache/state ignored -> EPHEMERAL, start 0, handoff 1
ordinary untracked note.md -> DIRTY, start 1
tracked modification -> DIRTY, start 1
new ignored scratch.bin outside constants -> UNEXPECTED_IGNORED, start 1
tracked modification under a family path -> both DIRTY and family, never hidden
report path inside repository -> tool error 2 and no report file
report path outside repository -> valid JSON with the same findings as stdout
```

- [ ] **Step 3: Add aggregate and failure tests**

Create two linked disposable worktrees, place evidence in one, and assert `--all-worktrees` exits 0 while retaining `DIRTY-PROTECT` for that worktree. Also assert a non-Git directory exits 2 with the Git error visible.

- [ ] **Step 4: Run tests to prove they are red**

Run:

```bash
python3 -m pytest ANALYSIS/tests/test_workspace_hygiene.py -q
```

Expected: FAIL because `scripts/check_workspace_hygiene.py` does not exist.

- [ ] **Step 5: Commit the red tests**

```bash
git add ANALYSIS/tests/test_workspace_hygiene.py
git commit -m "test: 固化工作区污染盲点"
```

### Task 4: Implement the minimal read-only checker

**Files:**
- Create: `scripts/check_workspace_hygiene.py`

- [ ] **Step 1: Implement Git collection**

Run only these read-only commands through a small checked subprocess wrapper:

```text
git rev-parse --show-toplevel
git status --porcelain=v1 --untracked-files=all --ignored=matching
git worktree list --porcelain        # only for --all-worktrees
```

Parse ` M`, `M `, `A `, `??`, and `!!` records without reading any reported path.

- [ ] **Step 2: Implement independent family and Git-state findings**

Use in-script tuples for protected, ephemeral, and evidence families exactly as frozen in the design. Preserve both dimensions in JSON fields `git_state` and `families`; calculate worktree classes as a set rather than a first-match enum.

- [ ] **Step 3: Implement decisions and output**

Expose mutually exclusive argparse modes `--phase {start,handoff}` and `--all-worktrees`, plus optional `--report`. Return 0/1/2 per the design table; in aggregate mode retain a per-worktree `recoverable` boolean and `protection` value while returning 0 unless the tool fails.

- [ ] **Step 4: Guard report output**

Resolve the report parent and every inspected worktree lexically. Reject any report path inside an inspected worktree before opening it. Write JSON only after classification succeeds.

- [ ] **Step 5: Run the red tests until green**

Run:

```bash
python3 -m pytest ANALYSIS/tests/test_workspace_hygiene.py -q
```

Expected: all workspace tests pass. Do not weaken assertions or add persistent state to make them pass.

- [ ] **Step 6: Verify the production-size boundary**

Run:

```bash
wc -l scripts/check_workspace_hygiene.py
rg -n "rm|git clean|git stash|git reset|worktree remove|unlink|rmtree" scripts/check_workspace_hygiene.py
```

Expected: approximately 200 lines and no destructive command implementation.

- [ ] **Step 7: Commit**

```bash
git add scripts/check_workspace_hygiene.py
git commit -m "chore: 增加只读工作区污染检查"
```

### Task 5: Integrate, verify locally, and prepare independent review

**Files:**
- Modify: `AGENT-START-HERE.md`
- Modify: `.github/pull_request_template.md`
- Modify: `ANALYSIS/DOCUMENT-STATUS.json`

- [ ] **Step 1: Add the startup and handoff commands**

Put this before document governance in `AGENT-START-HERE.md`:

```bash
python3 scripts/check_workspace_hygiene.py --phase start
```

Add this to the PR evidence/READY checklist:

```bash
python3 scripts/check_workspace_hygiene.py --phase handoff
```

- [ ] **Step 2: Make startup command removal fail governance**

Add the exact start command to the existing `AGENT-START-HERE.md` `contains` invariant. Update `updated_at` and reviewed entry dates for the entry point, PR template, and registry.

- [ ] **Step 3: Run focused integration checks**

Run:

```bash
python3 scripts/check_document_governance.py --mode all --report /tmp/leo-document-governance.json
python3 scripts/check_workspace_hygiene.py --phase start --report /tmp/leo-workspace-current.json
python3 PAPER/eligible_claims.py
python3 -m CODE.leo_sim config validate CODE/leo_sim/profiles/smoke.yaml
python3 -m pytest ANALYSIS/tests/test_workspace_hygiene.py ANALYSIS/tests/test_document_governance.py PAPER/tests/test_eligible_claims.py CODE/tests/test_remote_gate.py -q
```

Expected: governance passes; this implementation worktree reports only its declared task dirt before commit; eligible claims is `[]`; config validates; targeted tests pass.

- [ ] **Step 4: Commit integration, then audit every worktree**

```bash
git add AGENT-START-HERE.md .github/pull_request_template.md ANALYSIS/DOCUMENT-STATUS.json
git commit -m "docs: 接入工作区开工与交接门禁"
python3 scripts/check_workspace_hygiene.py --all-worktrees --report /tmp/leo-workspaces.json
```

Expected: the root anchor exposes protected local material; all three evidence worktrees are non-recoverable `DIRTY-PROTECT`; no content is read or changed.

- [ ] **Step 5: Run full verification**

```bash
python3 -m pytest CODE/leo_sim/tests CODE/tests ANALYSIS/tests PAPER/tests -q
python3 scripts/check_document_governance.py --mode all
git diff --check
git status --short --branch
```

Record exact passed/failed/skipped counts. Test success is engineering evidence only, not a research conclusion.

- [ ] **Step 6: Push and obtain a fresh independent candidate review**

Push the exact full SHA, ask one ordinary Kimi reviewer to audit only the declared write set and safety contract, then independently adjudicate every finding before moving the Draft PR toward READY. Do not use a Pro model and do not merge, deploy, run a formal experiment, delete, move, or archive any asset as part of this plan.
