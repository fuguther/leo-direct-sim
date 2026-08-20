# Research Documentation Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Consolidate recent LEO platform and experiment documentation into stable, evidence-bounded current truth sources aligned to experiment readiness and long-term simulation fidelity.

**Architecture:** Keep six stable human-facing entry documents plus one machine-readable experiment-program manifest. Preserve detailed and dated documents as supporting or historical evidence with visible status banners, while compacting the rolling NOTES log into a current evidence index plus a verbatim archive.

**Tech Stack:** Markdown, YAML, Git, repository-local link and status validation.

---

### Task 1: Establish canonical navigation and current readiness

**Files:**
- Modify: `ANALYSIS/README.md`
- Create: `ANALYSIS/CURRENT-EXPERIMENT-READINESS.md`

- [ ] Replace the current README command example with a document map that does not claim missing analysis code is runnable.
- [ ] Record exact live facts: main `4c8d38f`, D1 PR #55, D2 PR #56, and VM deployment `a2a588d`.
- [ ] Define separate gates and estimate ranges for experiment readiness and the research-simulation ceiling.
- [ ] Verify every estimate is labeled `ESTIMATE` and every live status has a verification date.

### Task 2: Consolidate platform capability and issue state

**Files:**
- Create: `ANALYSIS/PLATFORM-CAPABILITY-LEDGER.md`
- Modify: `ANALYSIS/FINDINGS-REGISTRY.md`

- [ ] Merge the current decisions from migration, legacy audit, feature ledger, and expert review into one capability table.
- [ ] Separate near-term experiment blockers, claim-dependent prerequisites, and long-term research arms.
- [ ] Add missing reward-loop and action-mask information-boundary findings to the issue registry without deleting closed history.
- [ ] Reconcile the registry's review-round wording with the observed D1/D2 review history.

### Task 3: Consolidate Q0 and experiment design

**Files:**
- Create: `ANALYSIS/Q0-INFORMATION-ABLATION-PROTOCOL.md`
- Create: `ANALYSIS/EXPERIMENT-PROGRAM.md`
- Create: `EXPERIMENTS/experiment-program.yaml`

- [ ] Merge Q0 purpose, Q0-F/Q0-I definitions, algorithm families, interface boundaries, tiny verification, and the combination matrix.
- [ ] Define the top-down theoretical ladder and bottom-up engineering ladder with separate claims.
- [ ] Merge E0, engineering pilot, EXP1, EXP2, EXP2b, EXP3, and Q0 diagnostic experiments into one ordered program.
- [ ] Encode stable experiment IDs, dependencies, statuses, and required evidence in YAML without claiming authorization.

### Task 4: Compact NOTES and label legacy documents

**Files:**
- Create: `ANALYSIS/HISTORY/NOTES-THROUGH-20260819.md`
- Modify: `NOTES.md`
- Modify: recent dated roadmap, audit, Q0, report, and experiment-plan documents.

- [ ] Preserve older NOTES content verbatim in the history file.
- [ ] Rewrite NOTES as a rolling current-cycle evidence index with links to the canonical documents.
- [ ] Add `HISTORICAL`, `SUPERSEDED`, or `SUPPORTING` banners to dated documents without rewriting their historical body.
- [ ] Verify no tracked file was deleted or moved.

### Task 5: Verify consistency

**Files:**
- Verify all changed Markdown and YAML files.

- [ ] Run `rg` checks for stale truth-source claims, old D1/D2 hashes, and runnable references to missing `paired_analysis.py`.
- [ ] Parse `EXPERIMENTS/experiment-program.yaml` with the available Python YAML library, or use a minimal syntax check if PyYAML is unavailable.
- [ ] Run `python3 -m pytest CODE/leo_sim/tests CODE/tests -q`; expected baseline is 411 passing tests.
- [ ] Review `git diff --check`, changed-file scope, and final `git status`.
- [ ] Commit with a documentation-only commit message and open a PR; do not merge until CI is green and the diff contains no path deletion or move.
