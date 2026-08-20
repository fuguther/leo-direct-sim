# LEO Research Documentation Consolidation Design

## Purpose

Replace date-stamped status fragments with a small set of stable, current documents aligned to the user's two platform goals:

1. **Experiment-ready platform**: a frozen, reviewable, deployable baseline that can produce research-eligible experiment evidence.
2. **Research-simulation ceiling**: a high-fidelity platform whose physical, information, control, learning, and evidence capabilities approach the practical ceiling for the stated LEO routing research program.

The consolidation must not erase historical evidence or present estimates as facts.

## Canonical document set

- `ANALYSIS/README.md`: navigation and document-status policy.
- `ANALYSIS/CURRENT-EXPERIMENT-READINESS.md`: live platform state, two-goal gap table, gates, estimates, and next actions.
- `ANALYSIS/PLATFORM-CAPABILITY-LEDGER.md`: current old-to-new capability comparison and blocker classification.
- `ANALYSIS/Q0-INFORMATION-ABLATION-PROTOCOL.md`: Q0 purpose, Q0-F/Q0-I separation, top-down information ablation, bottom-up practical validation, and tiny-scale exactness requirements.
- `ANALYSIS/EXPERIMENT-PROGRAM.md`: research questions, dependency graph, E0/pilot/formal experiment list, execution order, and evidence contract.
- `ANALYSIS/FINDINGS-REGISTRY.md`: the only issue ledger; open items first, closed items retained for traceability.
- `NOTES.md`: rolling operational log and evidence index, not a current-state authority.

## Compaction policy

- Preserve dated reports as immutable historical snapshots.
- Add a visible status banner to stale documents: `HISTORICAL`, `SUPERSEDED`, or `SUPPORTING`.
- Copy older `NOTES.md` entries verbatim into `ANALYSIS/HISTORY/NOTES-THROUGH-20260819.md`; keep only the current cycle and pointers in `NOTES.md`.
- Merge current conclusions, not every paragraph. Detailed derivations remain in supporting documents and are linked from canonical documents.
- Do not delete or move tracked paths in this change.

## Status and estimate rules

- Every changing statement must include `last verified`, an exact commit/PR/receipt where available, and `FACT`, `INFERENCE`, or `ESTIMATE`.
- Calendar estimates must be ranges with explicit assumptions and must not be used as readiness evidence.
- “Experiment-ready” and “research-simulation ceiling” have separate gates; optional long-term research arms must not silently block the near-term baseline.

## Experiment representation

Use two layers:

1. Human-readable `ANALYSIS/EXPERIMENT-PROGRAM.md` for research questions, rationale, dependencies, statistics, and interpretation.
2. Machine-readable `EXPERIMENTS/experiment-program.yaml` for stable experiment IDs, prerequisites, arm definitions, status, and required receipts. It is a planning manifest, not an authorization or run request.

Individual formal executions continue to use the existing experiment-platform request/manifest/authorization artifacts. Results remain outside Git.

## Information-ablation design

The primary scientific ladder is top-down:

`Q0-F future-aware optimum -> Q0-I current-global optimum -> progressively restricted current information -> local/stale information`.

The secondary engineering ladder is bottom-up:

`current local policy -> add one information family at a time`.

The top-down ladder estimates information value under fixed physical constraints and control scope. The bottom-up ladder measures realizable value under a fixed practical learner. A single removal order is insufficient, so selected one-cut and two-cut combinations are retained to detect interactions.

## Non-goals

- No code, CI, VM, PR, or experiment execution changes.
- No deletion or relocation of existing tracked documents.
- No claim that the current platform is experiment-ready.
- No claim that large-scale approximate MPC/RL results are strict numerical upper bounds.
