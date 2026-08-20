# Traffic and Runtime Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the approved M-Lab measurement-driven OD plus burst design into a reproducible V2 trace pipeline, calibrate topology/load/resource budgets, and prove every claimed learning arm can train and evaluate on the VM.

**Architecture:** Keep `CODE/leo_sim/trace.py` as the immutable trace compiler and extend its existing provenance contract instead of creating a second traffic runtime. Keep topology cadence in the existing `topology.recompute_interval_s` kernel ticker. Add resource and train/eval acceptance around the existing platform check and V2 analysis chain; never treat a successful import or unit test as a runtime result.

**Tech Stack:** Python 3.11, NumPy, SimPy, TensorFlow for DDQN, existing YAML config, JSON/YAML experiment contracts, VM remote runner.

---

### Task 1: Freeze and validate the measurement-driven traffic source

**Files:**
- Create: `CODE/data/traffic/mlab_measured_od_burst.schema.json`
- Create: `CODE/data/traffic/README.md`
- Modify: `CODE/leo_sim/trace.py:201-225`
- Modify: `CODE/leo_sim/tests/test_trace.py`

- [ ] **Step 1: Write the failing source-contract tests**

Add tests asserting that an M-Lab source row has finite WGS84 coordinates, positive sample count and throughput, a valid UTC hour, and that the compiler records `source_type`, source SHA, coordinate mapping, time mapping and `measurement_proxy` without silently substituting uniform demand.

```python
def test_mlab_source_contract_records_time_and_mapping(tmp_path):
    source = tmp_path / "mlab.csv"
    source.write_text(
        "client_lat,client_lon,server_lat,server_lon,hour_utc,sample_count,mean_throughput_mbps\n"
        "34.717,135.418,35.553,139.781,10,2,100\n",
        encoding="utf-8",
    )
    # compile with two matching endpoint cells and assert the manifest
    # contains source SHA, hour mapping, and measurement_proxy provenance.
```

- [ ] **Step 2: Run the focused tests to verify the new contract is absent**

Run: `python3 -m pytest -q CODE/leo_sim/tests/test_trace.py -k 'mlab or source'`

Expected: the new contract test fails before implementation; existing trace tests remain the baseline.

- [ ] **Step 3: Implement fail-closed source parsing**

Keep `_load_mlab_weights` as the single adapter. Validate every consumed numeric field, aggregate pair weights by `mean_throughput_mbps * sample_count`, retain an hourly histogram in the in-memory result, and raise `TraceError` for invalid rows or zero coverage. Put the exact schema and field meanings in the new JSON schema/README. Do not store raw IPs or raw archives in the repository.

- [ ] **Step 4: Run focused and full trace tests**

Run: `python3 -m pytest -q CODE/leo_sim/tests/test_trace.py`

Expected: all trace tests pass; the manifest’s source SHA equals the source bytes SHA and no test accepts a silent uniform fallback.

- [ ] **Step 5: Commit**

```bash
git add CODE/data/traffic CODE/leo_sim/trace.py CODE/leo_sim/tests/test_trace.py
git commit -m "feat: freeze measurement-driven traffic source contract"
```

### Task 2: Add temporal M-Lab weighting and burst transformation

**Files:**
- Modify: `CODE/leo_sim/config.py:70-95, 450-505`
- Modify: `CODE/leo_sim/trace.py:133-190, 201-225, 341-390, 430-470`
- Modify: `CODE/leo_sim/tests/test_trace.py`
- Create: `CODE/leo_sim/profiles/mlab_measured_od_burst.yaml`

- [ ] **Step 1: Write the failing behavior tests**

Add one fixture with the same OD in two different `hour_utc` buckets and assert that the compiled manifest records the bucket mapping and that a burst multiplier changes realized offered bits only inside the declared window. Add a reproducibility test compiling the same config twice and comparing both `trace.csv` and `manifest.json` SHA-256 values.

- [ ] **Step 2: Run the focused tests and capture the failure**

Run: `python3 -m pytest -q CODE/leo_sim/tests/test_trace.py -k 'hour or burst or reproducible'`

Expected: the hourly/burst-combination test fails before implementation because the current `mlab` mode only uses OD weights.

- [ ] **Step 3: Implement one explicit transform**

Add a named mode or transform flag for `mlab_measured_od_burst`. Use measured OD weights for source/destination selection, use the declared time bucket for the deterministic rate multiplier, and apply burst only through the declared window. Keep the total offered load controlled by `demand.offered_mbps`; measured throughput remains a distribution weight, never an unscaled capacity claim.

- [ ] **Step 4: Add the bounded profile and run it locally**

The profile must use a short horizon only for pipeline validation, set `topology.recompute_interval_s: 1.0`, and set `execution.max_packets` before compilation. Run:

```bash
python3 -m CODE.leo_sim trace compile --config CODE/leo_sim/profiles/mlab_measured_od_burst.yaml --out /private/tmp/mlab-trace-smoke
```

Expected: a trace, manifest, source SHA, OD mapping and burst transform are produced; no result is called paper evidence.

- [ ] **Step 5: Commit**

```bash
git add CODE/leo_sim/config.py CODE/leo_sim/trace.py CODE/leo_sim/tests/test_trace.py CODE/leo_sim/profiles/mlab_measured_od_burst.yaml
git commit -m "feat: compile temporal measured OD bursts"
```

### Task 3: Calibrate topology recomputation cadence

**Files:**
- Create: `ANALYSIS/TOPOLOGY-CADENCE-20260821.md`
- Modify: `CODE/leo_sim/tests/test_dynamic_topology.py`
- Modify: `EXPERIMENTS/experiment-program.yaml`

- [ ] **Step 1: Add the cadence acceptance test**

Run the same immutable trace, topology seed and deterministic policy for `0.5`, `1.0`, `2.0` and `5.0` seconds. The result record must include recompute count, created/retired link generations, holding packets, delivery, utilization p95, wall time and peak RSS.

- [ ] **Step 2: Define the selection rule before observing results**

Use the locked rule: 0.5 s and 1 s must be compared on the same inputs; select 1 s only when delivery differs by at most 2 percentage points and utilization p95 by at most 5%, while 1 s is cheaper in wall time/RSS. Otherwise select the smallest interval that converges.

- [ ] **Step 3: Run the cadence matrix**

Run the bounded non-learning VM smoke for all four intervals. Store the raw receipts and the cadence table outside Git; commit only the contract, script and verified summary.

- [ ] **Step 4: Commit**

```bash
git add ANALYSIS/TOPOLOGY-CADENCE-20260821.md CODE/leo_sim/tests/test_dynamic_topology.py EXPERIMENTS/experiment-program.yaml
git commit -m "exp: calibrate topology recomputation cadence"
```

### Task 4: Calibrate E0 load and CPU/memory budget

**Files:**
- Create: `ANALYSIS/RESOURCE-PROFILE-20260821.md`
- Modify: `EXPERIMENTS/experiment-program.yaml`
- Modify: `CODE/leo_sim/platform_check.py`
- Create: `CODE/leo_sim/tests/test_resource_profile.py`

- [ ] **Step 1: Run non-learning E0 load scan**

Use the final measured-OD burst trace and deterministic routing. Test low, transition, high and overload candidate rates; record delivered/deadline/backlog/utilization and natural-end status. Freeze low/medium/high only after the transition regime is visible.

- [ ] **Step 2: Run the four CPU profiles**

For one fixed short training cell, vary only CPU/thread budget `1,2,4,8`. Record `steps_per_second`, wall time, peak RSS, TensorFlow execution mode and seed. Reserve at least 20% memory headroom and never run profiles concurrently.

- [ ] **Step 3: Fail before launch when memory is unsafe**

Make the profile runner reject a configuration when its measured/declared peak RSS would exceed the available budget; do not wait for an OOM kill.

- [ ] **Step 4: Commit the calibrated contract**

```bash
git add ANALYSIS/RESOURCE-PROFILE-20260821.md CODE/leo_sim/platform_check.py CODE/leo_sim/tests/test_resource_profile.py EXPERIMENTS/experiment-program.yaml
git commit -m "exp: freeze load and training resource budgets"
```

### Task 5: Prove learning train/checkpoint/eval on the VM

**Files:**
- Modify: `CODE/leo_sim/platform_check.py:138-205`
- Modify: `CODE/leo_sim/tests/test_platform_check.py`
- Modify: `EXPERIMENTS/experiment-program.yaml`
- Modify: `ANALYSIS/CURRENT-EXPERIMENT-READINESS.md`

- [ ] **Step 1: Add acceptance tests for the actual runtime contract**

Tests must require: train natural end, saved checkpoint SHA, checkpoint reload, eval natural end, identical trace SHA for train/eval, no silent algorithm fallback, and a resource profile artifact. A green unit test without these artifacts is not sufficient.

- [ ] **Step 2: Run Q-learning first**

Use the fixed measured trace and selected resource budget. Complete train → checkpoint → eval and verify the persisted analysis manifest. Q-learning is the dependency-light runtime smoke.

- [ ] **Step 3: Run DDQN second**

Require TensorFlow, the configured fast/eager path, checkpoint reload and the same immutable trace. If a formal arm claims GAT or MPNN, repeat this test for that contract; otherwise do not list it as a formal arm.

- [ ] **Step 4: Run the platform check on the exact deployed SHA**

Run the canonical VM command through the authorized remote runner. The result is accepted only if both learning arms and the non-learning arm naturally end, receipts verify, analysis recomputes, and peak RSS stays below the budget.

- [ ] **Step 5: Commit the evidence-index update**

```bash
git add CODE/leo_sim/platform_check.py CODE/leo_sim/tests/test_platform_check.py EXPERIMENTS/experiment-program.yaml ANALYSIS/CURRENT-EXPERIMENT-READINESS.md
git commit -m "test: require learning train eval runtime evidence"
```
