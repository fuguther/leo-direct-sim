# Workspace hygiene and current-entry consolidation design

> **EVIDENCE-SNAPSHOT**: this dated design records the approved implementation
> boundary. It is not a second current-status or experiment authority. Current
> work still starts at `AGENT-START-HERE.md`.

## Objective

First remove misleading current guidance without deleting historical evidence.
Then add one small, read-only check that prevents an Agent from treating a
tracked-clean worktree as disposable while it contains untracked, ignored,
private, or experimental assets.

The latest local advisor-facing direction is
`GROUP-MEETINGS-LOCAL/03-CURRENT-PREP/2026-08-31/论文方向梳理与文献调研任务.md`.
It is the only group-meeting file allowed to direct the next report. Older
dated preparation files remain historical source material and are opened only
for an explicit provenance, commitment, or comparison question.

## Non-goals

- Do not delete, move, archive, overwrite, stash, or reset any existing path.
- Do not create another CURRENT project-status document.
- Do not scan historical document contents during normal Agent startup.
- Do not hash or parse raw experiment results.
- Do not add a daemon, database, background monitor, mandatory local Git hook,
  or a second governance framework.
- Do not start a formal experiment or change GitHub settings.

## Phase 1: consolidate existing entry points

Use the existing authorities instead of adding replacements:

1. Update the local group-meeting `README.md` so the 2026-08-31 direction is
   the sole current report entry. Mark 2026-08-22/24/29/30 preparations as
   historical material without moving them.
2. Add `GROUP-MEETINGS-LOCAL/` to the repository `.gitignore`. The directory
   remains private and local; a clean checkout does not require it.
3. Synchronize the existing readiness Markdown, experiment-program Markdown,
   machine YAML, capability ledger, and document review dates to the tracked
   `EXP-20260829-GLOBAL-PRESSURE-BRACKET-R02` evidence in `origin/main`.
4. Preserve the bounded conclusion: 24 verified runs represent 12 unique
   resolved configurations plus 12 exact reexecutions; all scene checks are
   `ACCESS_LIMITED`; the claim gate is
   `READY_FOR_INDEPENDENT_CLAIM_REVIEW`; no ISL-pressure, causal, algorithm
   superiority, information-value, RL-value, or new-method claim follows.
5. Repair current executable guidance: use `python3`, use the positional
   `config validate` argument, and make `remote.env.template` match the
   canonical `/data/论文/leo-direct-sim` guard.
6. Materialize the empty YAML claim registry already required by
   `PAPER/eligible_claims.py`, so the documented no-claim state is `[]` rather
   than a missing-file error. Keep `PAPER/CLAIM_MAP.csv` until a separate,
   user-approved disposition.

## Phase 2: thin workspace-hygiene check

Add one script, `scripts/check_workspace_hygiene.py`, plus focused tests. The
script reads Git metadata and path names only. It does not read file contents,
calculate result hashes, remove files, or mutate Git.

### Interface

```text
python3 scripts/check_workspace_hygiene.py --phase start [--report PATH]
python3 scripts/check_workspace_hygiene.py --phase handoff [--report PATH]
python3 scripts/check_workspace_hygiene.py --all-worktrees [--report PATH]
```

- `start` checks the current worktree before a new task begins.
- `handoff` applies the stricter completion/recovery boundary.
- `--all-worktrees` is an audit view for the project owner. It never authorizes
  cleanup.
- Human-readable output goes to stdout; an optional JSON report carries the
  same classification and exact paths/counts.

### Classifications

| Class | Meaning | Default decision |
|---|---|---|
| `CLEAN` | No tracked or ordinary untracked changes; no relevant ignored assets | Continue |
| `PROTECTED_LOCAL` | Declared private local inputs such as `GROUP-MEETINGS-LOCAL/` or `remote.env` | Report; do not commit or delete; does not block the root anchor |
| `EPHEMERAL` | Re-creatable cache such as `.DS_Store`, `__pycache__`, or `.pytest_cache` | Report exact paths; never auto-delete |
| `EVIDENCE_PRESENT` | `CODE/Results/`, `Results/`, `out/`, `leo_sim_out/`, witness, or other experiment output | `DIRTY-PROTECT`; block task replacement and worktree recovery |
| `DIRTY` | Tracked modifications or ordinary untracked files | Block a new writer unless it is the declared owner continuing the same task |
| `UNEXPECTED_IGNORED` | Ignored content outside the declared private/cache/evidence families | Block and require classification |

`PROTECTED_LOCAL` is intentionally non-fatal in the main anchor because the
private group archive and `remote.env` are expected there. It remains visible
so an Agent cannot mistake GitHub for their backup. `EVIDENCE_PRESENT` never
means garbage and never produces a deletion recommendation by itself.

### Enforcement points

1. Add the `start` command to `AGENT-START-HERE.md` before document governance.
2. Add the `handoff` command to the pull-request evidence checklist.
3. Extend the existing document-governance invariant so removal of the startup
   command fails CI.
4. Keep implementation tests in the current Python test suite. CI verifies
   classification behavior using disposable repositories; CI is not claimed
   to see local ignored assets.

No Git hook is installed. Hooks are clone-local, bypassable, and would add a
second installation lifecycle without solving ignored evidence on another
machine.

## Error and safety behavior

- Git command failure, malformed status output, inaccessible worktree, or JSON
  report failure returns a non-zero exit and prints the original error.
- Symlink targets and file contents are not followed during classification.
- The tool never calls `rm`, `git clean`, `git stash`, `git reset`,
  `git worktree remove`, or branch-deletion commands.
- A cleanup candidate is emitted only as an inventory item. Existing repository
  rules still require exact-path proof and user approval before deletion or
  movement.

## Size and performance budget

- One production script and one focused test module.
- No third-party dependency.
- Target implementation size: approximately 200 lines, excluding tests. If the
  design requires persistent state, background execution, or a second status
  registry, stop and redesign.
- Normal `start` reads only the current worktree and should complete in about
  one second for the present repository. The all-worktree audit may take longer
  but is never part of every command.

## Verification

The implementation is accepted only when all of the following are freshly
verified:

1. Tests first reproduce the existing blind spot: a Git-clean worktree with an
   ignored result file is not classified as clean.
2. Tests cover protected local material, ephemeral caches, tracked/untracked
   dirt, unexpected ignored files, evidence-bearing worktrees, Git failures,
   JSON output, and all-worktree aggregation.
3. The current root is reported as an anchor with protected local material,
   not as disposable clean space.
4. The three existing evidence worktrees are reported `EVIDENCE_PRESENT` /
   `DIRTY-PROTECT` without reading or changing their results.
5. Document governance, paper claim CLI, command examples, remote-template
   checks, targeted tests, and the full test suite pass on the resulting exact
   commit.
6. `git diff --check` passes and the implementation worktree contains no
   undeclared untracked or ignored artifacts.

## Delivery order

Use one owner branch and small commits:

1. Supporting design record.
2. Current-entry and executable-guidance consolidation.
3. Red tests for workspace classification.
4. Minimal guard implementation and integration.
5. Independent candidate review, Codex adjudication, full verification, push,
   Draft/Review evidence, and normal merge gates.

No cleanup or experiment claim is authorized merely by this design.
