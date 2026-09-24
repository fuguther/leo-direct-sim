# Agent Reading Order After Research Context Migration

## Purpose

This file defines how automated agents should consume repository context after the research direction migration.

The repository contains historical experiments and earlier research iterations. Historical material is preserved for evidence tracking but must not silently define current objectives.

## Required reading order

1. `RESEARCH_CONTEXT.md`

Current scientific question and research boundaries.

2. `AGENTS.md`

Engineering constraints and repository safety rules.

3. `README.md`

Repository overview.

4. `ANALYSIS/README.md`

Current analysis documents and evidence routing.

5. Task-specific files only.

## Current research interpretation

The platform is not committed to a final routing algorithm.

Do not assume:

- DDQN is the final method.
- Prediction accuracy is the primary objective.
- Future queue prediction is the correct target.
- Packet-level inference is required.

The current objective is to establish whether time misalignment between observed information, computation, control execution, and packet arrival causes measurable routing decision loss.

## Historical material

Files with historical dates, old experiment names, or previous algorithm goals should be treated as evidence snapshots unless explicitly promoted by a CURRENT document.

## Implementation rule

Before changing simulation behavior, identify whether the change affects:

- physical model;
- event timing semantics;
- information availability;
- experiment reproducibility;
- historical evidence compatibility.

Changes affecting these areas require explicit justification.
