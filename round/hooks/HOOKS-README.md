# Research hook closure

## Status

Current implementation replaces anonymous tickets with explicit runtime session binding.
Unit/control tests and the installed Harness bridge integration are separate checks.
The integration test uses the real installed bridge and subprocess execution, with a synthetic
session/tool host; it does not claim a running web session was tested.

## Startup and identity

Only the controller operates `perm.py`. Initialize a new run using its real session id.
Create an idle Harness session, bind its returned id with one role and exact task files,
then submit work. If using the existing auto-start subagent tool, first give it a bootstrap
instruction containing no research material; unauthorized worktree access is denied until
its returned id has been bound. Resume that same child after binding. Never reserve anonymous
role slots or give every worker all output paths.

```
python3 round/hooks/perm.py init --run RUN --orchestrator MAIN_SESSION
python3 round/hooks/perm.py bind --session CHILD_SESSION --role deepener \
  --extra-read round/run2/cards/CARD.md --extra-read round/run2/feedback/CARD.md \
  --extra-write round/run2/drafts/CARD.md
```

A child cannot claim a role. Rebinding fails; revoked sessions remain tombstones.
The permission CLI serializes mutations with flock and writes via atomic replacement.
Read-only guard processes do not consume or mutate permissions.
The controller's recovery identity is stored separately; it is not cryptographic authorization.

## Stop and resume

1. `perm.py pause` prevents subsequent registered-worker tool calls once the bridge is active.
2. Use Harness's own cancel/interrupt interface on each active child. Pausing the guard does
   not cancel an in-flight model request, shell command, or already executing tool.
3. Wait for confirmed terminal states. Record run_id, active_sessions (must be []), and tasks.
   A completed task carries task_id, state=completed, artifact absolute path and sha256;
   pending/failed/cancelled tasks carry task_id and state. Never call completed merely because
   a file exists. The host task status is authoritative; the receipt is the reconciliation record.
4. `perm.py resume --run RUN --orchestrator NEW_MAIN --receipt RECORD.json` validates the
   record and completed artifact hashes, revokes old worker permissions, and changes owner.
   Dispatch only pending work; completed outputs stay untouched. A new main must also comply
   with repository single-writer handoff; session authority does not transfer branch ownership.

`init` cannot clear an active run. It is not a substitute for reconciliation.

## Recommendation

All revise/status paths check the final state. A load-bearing revision resets a recommendation
to needs_revision. A PASS for the old content cannot approve new content. Missing or changed
card files reject recommendation. A valid gate record is a controller judgment, not a machine
proof of research value; reviewers must still check facts, causal reasoning, and alternatives.

## Scope and limitations

Structured file paths are checked against role grants. Shell/code inspection remains best effort;
use structured read/write tools for isolated research workers. This is not a hostile-code sandbox.
Generic prompt substring blocking is not mounted: it wrongly blocks authorized history reviewers
and cannot infer the child role. Controller dispatch contracts enforce limited feedback and fresh
contexts. Existing prompt checker remains available as a diagnostic, not an isolation proof.

No changes to installed packages or user session databases are needed. `hooks.json` uses projectDir
substitution. `overlay-research-guard.yml` replaces the existing bridge row at service startup.
Do not restart a host with other active work without first reconciling/cancelling that work.
After startup a real allowed/denied tool probe with hook/invoked and hook/result events is required
before unattended research. If the bridge fails to load, do not dispatch research.

## Tests

- `python3 round/hooks/selftest.py`: isolated temp worktrees, no live manifest replacement.
- `python3 round/tools/test_rework_regressions.py`: existing 12 control regressions.
- `node round/hooks/test_bridge.mjs [installed bridge module]`: actual bridge integration,
  7 cases/14 hook events, no model requests, synthetic host explicitly labelled.
