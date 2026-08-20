# Population-Gravity Traffic Implementation Plan

> **HISTORICAL IMPLEMENTATION PLAN**：实现计划不代表当前待办；现行实验范围见 `EXPERIMENT-PROGRAM.md`。

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build reproducible population-distributed source traffic and probabilistic gravity destinations for the V2 satellite-direct platform.

**Architecture:** A focused population adapter reads and aggregates the repository GeoTIFF. The immutable trace compiler consumes its endpoint table and samples source Poisson processes plus conditional gravity destinations. The existing kernel remains unchanged and consumes the resulting trace.

**Tech Stack:** Python 3.11, NumPy, Pillow TIFF reader, existing leo_sim config/trace/receipt CLI.

---

### Task 1: Population raster adapter

**Files:**
- Create: `CODE/leo_sim/population.py`
- Create: `CODE/leo_sim/tests/test_population.py`

- [ ] Test that negative/no-data pixels become zero, 0.25° cells aggregate exactly into configured 5° cells, centers are canonical, and aggregate population is conserved.
- [ ] Implement GeoTIFF metadata validation, deterministic row/column-to-lat/lon mapping and aggregate population sums.
- [ ] Test the repository GPW file directly: 1440×720, positive finite total population, at least two 5° regions.

### Task 2: Population-gravity trace mode

**Files:**
- Modify: `CODE/leo_sim/config.py`
- Modify: `CODE/leo_sim/trace.py`
- Modify: `CODE/leo_sim/tests/test_trace.py`

- [ ] Add fail-closed fields `population_path`, `source_population_exponent`, `destination_population_exponent`; add mode `population_gravity`.
- [ ] Bind population file SHA through existing trace identity input hash.
- [ ] Generate source Poisson rates from `population^beta` and destinations from `population^gamma / distance^alpha`.
- [ ] Record population provenance and model parameters in manifest.
- [ ] Prove byte reproducibility and parameter/input identity sensitivity.

### Task 3: Executable profile and real outcome

**Files:**
- Create: `CODE/leo_sim/profiles/population_gravity.yaml`
- Modify: `CODE/leo_sim/platform_check.py`
- Modify: `CODE/leo_sim/tests/test_platform_check.py`
- Modify: `CODE/README.md`
- Modify: `NOTES.md`

- [ ] Add a bounded 5° population profile using the repository GPW file.
- [ ] Add a population stage to `platform check` that requires natural end, conservation, receipt verification, delivered data, multiple source regions and multiple destination regions.
- [ ] Run focused tests, all V2 tests, then the exact one-command check in the isolated VM environment.
- [ ] Record only engineering evidence; do not claim calibrated demand or algorithm superiority.
