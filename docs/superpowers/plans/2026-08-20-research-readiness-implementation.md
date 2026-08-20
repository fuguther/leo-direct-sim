# Research Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task with a verification checkpoint after every task.

**Goal:** Make the LEO V2 platform trustworthy for congestion-control and link-utilization experiments, then close the minimum evidence chain needed for reproducible paper data.

**Architecture:** Work in four independently testable packages. First make the learning objective non-positive for every extra forwarding step, while retaining the raw legacy queue-reward diagnostic. Next add immutable per-link capacity/served-bit intervals and per-packet queue/service/propagation events. Then connect V2 run artifacts to recomputed metrics and paired claims. Finally compile real-traffic E0 inputs and run non-learning and learning pilot smokes on one deployed SHA.

**Tech Stack:** Python 3, SimPy, NumPy, PyYAML, pytest, existing `leo_sim` receipt/governance contracts, YAML experiment manifests.

---

### Task 1: Safe learning reward objective

**Files:**
- Modify: `CODE/leo_sim/config.py`
- Modify: `CODE/leo_sim/learning.py`
- Modify: `CODE/leo_sim/kernel.py`
- Modify: `CODE/leo_sim/receipt.py`
- Test: `CODE/leo_sim/tests/test_reward_objective.py`
- Update: `ANALYSIS/FINDINGS-REGISTRY.md`, `ANALYSIS/REWARD-DIFF-20260816.md`

- [ ] Write a failing test asserting the configured forwarding reward is never positive: `forward_reward(wait_s=0, w1=20, beta=200, step_penalty=-20) == 0`, and every positive wait produces a negative value.
- [ ] Write a failing config test rejecting `forward_step_penalty > -reward_w1` and accepting the default `-reward_w1`.
- [ ] Run `python3 -m pytest CODE/leo_sim/tests/test_reward_objective.py -q` and observe the missing symbol/config failure.
- [ ] Add `learning.forward_step_penalty` with default `-reward_w1`, validate `forward_step_penalty <= -reward_w1`, and implement `learning.forward_reward()` as raw queue reward plus the step penalty.
- [ ] Make ISL service-start transitions use `forward_reward`; keep `queue_reward()` as the raw legacy diagnostic and keep terminal delivery reward unchanged.
- [ ] Add receipt requested/effective reward-objective fields and tests proving the active objective is bound to the resolved config.
- [ ] Run the reward tests and the existing reward migration tests; update only assertions whose expected transition reward intentionally changes from positive raw M1 to safe composite reward.
- [ ] Run `python3 -m pytest CODE/leo_sim/tests CODE/tests -q`, run `git diff --check`, and commit `fix: prevent positive forwarding reward cycles`.

### Task 2: Minimum congestion measurement layer

**Files:**
- Modify: `CODE/leo_sim/kernel.py`, `CODE/leo_sim/trace.py`, `CODE/leo_sim/receipt.py`
- Create: `CODE/leo_sim/metrics.py`
- Test: `CODE/leo_sim/tests/test_congestion_metrics.py`

- [ ] Write failing tests for per-link interval capacity (`rate_bps × available_time`), served bits, and per-packet queue/service/propagation components summing to end-to-end delay.
- [ ] Implement immutable event records at queue entry, service start/end, propagation start/arrival, and link identity.
- [ ] Implement a pure recomputation module that rejects missing events, negative durations, mismatched packet IDs, and denominator-free utilization.
- [ ] Persist metric hashes and schema in the receipt; run targeted, CI-range, and full tests.

### Task 3: V2 artifact-to-claim analysis gate

**Files:**
- Modify: `CODE/experiment_platform/compile_experiment.py`, `CODE/experiment_platform/authorize_experiment.py`
- Create/modify: `ANALYSIS/v2_analysis.py`, `ANALYSIS/tests/test_v2_analysis.py`, claim schema/tests

- [ ] Write failing tests that load one authorized V2 run, recompute metrics from immutable artifacts, pair planned cells exactly, and reject output-path/hash/claim-boundary tampering.
- [ ] Implement the narrow V2 analyzer and persisted analysis manifest with code/config/receipt hashes.
- [ ] Run full analysis tests and verify failure propagation for missing or malformed artifacts.

### Task 4: Real-traffic E0 and pilot execution

**Files:**
- Modify: `CODE/leo_sim/trace.py`, `EXPERIMENTS/experiment-program.yaml`, `ANALYSIS/EXPERIMENT-PROGRAM.md`
- Create: `CODE/leo_sim/traffic_provenance.py`, `CODE/leo_sim/tests/test_traffic_provenance.py`
- Create: E0 request/manifests under `EXPERIMENTS/`

- [ ] Write failing tests for source hash, source type, unit conversion, OD mapping, burst transformation, and offered-bit recomputation.
- [ ] Implement the provenance contract and compile uniform-control plus real/measurement-proxy arms.
- [ ] Compile and authorize a tiny E0 matrix, run one non-learning and one learning smoke on the same deployed SHA, verify natural end/conservation/seed identity, then begin PILOT-ALL.

### Verification checkpoint

- [ ] For every package, record exact branch/commit, targeted tests, CI result, VM result, and remaining limitations in `NOTES.md`.
- [ ] Do not mark the platform paper-ready until reward, measurement, V2 analysis, and E0/pilot gates all have direct evidence.
