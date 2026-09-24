# Research Context Migration Plan

## Purpose

This document records the migration from the previous research workflow to the current research question.

This is not a deletion plan. Historical experiments remain evidence, but they must not silently act as current research constraints.

## Current research context

The platform is currently used to study:

> In distributed hop-by-hop LEO routing, whether information age, computation delay, and control execution delay create measurable routing decision degradation, and whether physically grounded compensation or learned estimation can recover this loss under realistic cost constraints.

## Current assumptions

The following are NOT fixed conclusions:

- DDQN is not assumed to be the final solution.
- Prediction accuracy is not the primary objective.
- Future queue prediction is not assumed to be the correct prediction target.
- Packet-level inference is not assumed to be the required deployment mode.
- End-to-end routing benefit is the evaluation target.

## Migration categories

### CURRENT

Documents that define current rules, interfaces, experiment contracts, and verified platform behavior.

Action:

- Keep active.
- Agent may use as current constraints.

### SUPPORTING

Documents containing methods, measurements, or evidence.

Action:

- Keep available.
- Do not allow them to define the research question.

### HISTORICAL

Documents describing previous experiments or previous interpretations.

Action:

- Preserve.
- Do not use as default task objectives.

### SUPERSEDED

Documents whose assumptions are replaced by the current research context.

Action:

- Preserve for traceability.
- Point future agents to replacement documents.

## First-pass audit targets

1. AGENT instructions
2. ANALYSIS experiment planning documents
3. Prompt and configuration files
4. Python defaults and naming that encode old research assumptions

## Required standard before changing code

A code change must state whether it changes:

- simulator behavior;
- experiment protocol;
- research interpretation;
- only documentation/context.

Documentation cleanup must not silently modify experimental claims.
