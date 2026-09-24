# Research Document Migration Status

## Purpose

This document records the migration from the previous research workflow to the current research question. It does not delete historical evidence and does not alter experiment results.

## Current research context

The repository is currently used to study:

- information age in distributed hop-by-hop LEO routing;
- computation and control execution delay;
- whether stale or delayed information creates measurable routing decision loss;
- whether compensation mechanisms provide end-to-end benefit under realistic cost.

No algorithm is assumed to be the final solution.

## Document classes

### CURRENT

Documents in this class define current execution rules, contracts, and verified state.

Examples:

- AGENTS.md
- RESEARCH_CONTEXT.md
- current contracts
- active experiment protocols

### SUPPORTING

Documents that provide evidence, methods, implementation notes, or analysis support. They may inform experiments but do not define the research question.

### HISTORICAL

Documents describing previous experiment stages, old interpretations, or superseded plans. They remain valuable for provenance and regression analysis.

### SUPERSEDED

Documents whose assumptions no longer match the current research direction.

They must not be used as default instructions for agents.

## Migration rules

1. Preserve historical experiment artifacts.
2. Do not rewrite old results to match the new direction.
3. Do not remove evidence because the research question changed.
4. Replace outdated instructions with explicit status classification.
5. Separate implementation capability from scientific claim.

## Pending migration areas

- ANALYSIS experiment planning documents: classify current versus historical sections.
- EXPERIMENTS configuration: remove implicit algorithm assumptions.
- prompts and agent instructions: remove outdated research objectives.
- Python code: inspect only for hard-coded research assumptions after document migration.

## Non-goals

This migration does not:

- prove a routing method is effective;
- choose packet/flow/background execution granularity;
- introduce a prediction model;
- modify simulator physics without evidence.
