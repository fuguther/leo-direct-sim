# Access boundary implementation plan (2026-08-22)

Scope is limited to access policy/queue semantics, ingress-stage metrics,
coverage audit, and directly affected truth documents.

1. Configuration and kernel (commit `fix`):
   - Files: `CODE/leo_sim/config.py`, `CODE/leo_sim/kernel.py`, config tests,
     access-boundary tests, and the explicit diagnostic profile.
   - RED: unknown policy; default/reject no-coverage rejection; queue retry
     after coverage returns; queue stop fate; finite uplink overflow.
   - GREEN command: `python3 -m pytest CODE/leo_sim/tests/test_config.py CODE/leo_sim/tests/test_access_boundary.py -q`.
   - Acceptance: default is reject, queue uses the existing bounded endpoint
     queue/ticker, no new bypass queue, and every packet has one fate.

2. Ingress metrics and analysis (commit `feat`):
   - Files: `CODE/leo_sim/metrics.py`, `CODE/leo_sim/kernel.py`,
     `CODE/leo_sim/receipt.py` only if compatibility requires it,
     `CODE/experiment_platform/v2_analysis.py`, metric catalog, and tests.
   - RED: exact metric values; duplicate ingress; delivery before ingress;
     zero admitted denominator; two V2 analysis metric names; historical v1
     ledger verification.
   - GREEN command: `python3 -m pytest CODE/leo_sim/tests/test_congestion_metrics.py CODE/experiment_platform/tests/test_v2_analysis.py -q`.
   - Acceptance: raw events independently recompute v2, v1 stored ledgers
     still verify, and malformed order fails loudly.

3. Coverage audit and truth sources (commit `feat`/`docs`):
   - Files: `CODE/leo_sim/coverage.py`, coverage tests, this spec/plan,
     `ANALYSIS/CURRENT-EXPERIMENT-READINESS.md`,
     `ANALYSIS/EXPERIMENT-PROGRAM.md`,
     `ANALYSIS/PLATFORM-CAPABILITY-LEDGER.md`, and
     `EXPERIMENTS/experiment-program.yaml`.
   - RED: invalid bounds, deterministic endpoint ordering, never-visible
     null/flag, and exact gap/fraction summaries using static fake geometry.
   - GREEN command: `python3 -m pytest CODE/leo_sim/tests/test_coverage.py -q`.
   - Acceptance: stable JSON and bounded explicit inputs; no RL, network, VM,
     new orbit equations, or automatic satellite-selection claim.

Final gates: targeted tests above, then `python3 -m pytest -q`,
`git diff --check`, a local same-trace reject/queue A/B, and clean status.
Historical formal results are preserved; the queue semantics require new E0
coverage/horizon audit, VM smoke, and then retraining before formal use.
