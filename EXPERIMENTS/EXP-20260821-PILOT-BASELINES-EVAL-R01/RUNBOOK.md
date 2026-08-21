# EXP-20260821-PILOT-BASELINES-EVAL-R01

Runtime: `leo_sim_v2`; compilation only, no run is launched.

Each cell is an independent controlled command after review, authorization, and clean deployment:

## EXP-20260821-PILOT-BASELINES-EVAL-R01-qlearning_a_eval-s7-l7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260821-PILOT-BASELINES-EVAL-R01/resolved/EXP-20260821-PILOT-BASELINES-EVAL-R01-qlearning_a_eval-s7-l7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260821-PILOT-BASELINES-EVAL-R01/authorization.json \
  --session exp-20260821-pilot-baselines-eval-r01-qlearning_a_eval-s7-l7
```

## EXP-20260821-PILOT-BASELINES-EVAL-R01-qlearning_b_eval-s7-l7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260821-PILOT-BASELINES-EVAL-R01/resolved/EXP-20260821-PILOT-BASELINES-EVAL-R01-qlearning_b_eval-s7-l7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260821-PILOT-BASELINES-EVAL-R01/authorization.json \
  --session exp-20260821-pilot-baselines-eval-r01-qlearning_b_eval-s7-l7
```

## EXP-20260821-PILOT-BASELINES-EVAL-R01-ddqn_c3_a_eval-s7-l7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260821-PILOT-BASELINES-EVAL-R01/resolved/EXP-20260821-PILOT-BASELINES-EVAL-R01-ddqn_c3_a_eval-s7-l7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260821-PILOT-BASELINES-EVAL-R01/authorization.json \
  --session exp-20260821-pilot-baselines-eval-r01-ddqn_c3_a_eval-s7-l7
```

## EXP-20260821-PILOT-BASELINES-EVAL-R01-ddqn_c3_b_eval-s7-l7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260821-PILOT-BASELINES-EVAL-R01/resolved/EXP-20260821-PILOT-BASELINES-EVAL-R01-ddqn_c3_b_eval-s7-l7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260821-PILOT-BASELINES-EVAL-R01/authorization.json \
  --session exp-20260821-pilot-baselines-eval-r01-ddqn_c3_b_eval-s7-l7
```

## EXP-20260821-PILOT-BASELINES-EVAL-R01-gat_a_eval-s7-l7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260821-PILOT-BASELINES-EVAL-R01/resolved/EXP-20260821-PILOT-BASELINES-EVAL-R01-gat_a_eval-s7-l7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260821-PILOT-BASELINES-EVAL-R01/authorization.json \
  --session exp-20260821-pilot-baselines-eval-r01-gat_a_eval-s7-l7
```

## EXP-20260821-PILOT-BASELINES-EVAL-R01-gat_b_eval-s7-l7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260821-PILOT-BASELINES-EVAL-R01/resolved/EXP-20260821-PILOT-BASELINES-EVAL-R01-gat_b_eval-s7-l7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260821-PILOT-BASELINES-EVAL-R01/authorization.json \
  --session exp-20260821-pilot-baselines-eval-r01-gat_b_eval-s7-l7
```

## EXP-20260821-PILOT-BASELINES-EVAL-R01-mpnn_a_eval-s7-l7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260821-PILOT-BASELINES-EVAL-R01/resolved/EXP-20260821-PILOT-BASELINES-EVAL-R01-mpnn_a_eval-s7-l7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260821-PILOT-BASELINES-EVAL-R01/authorization.json \
  --session exp-20260821-pilot-baselines-eval-r01-mpnn_a_eval-s7-l7
```

## EXP-20260821-PILOT-BASELINES-EVAL-R01-mpnn_b_eval-s7-l7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260821-PILOT-BASELINES-EVAL-R01/resolved/EXP-20260821-PILOT-BASELINES-EVAL-R01-mpnn_b_eval-s7-l7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260821-PILOT-BASELINES-EVAL-R01/authorization.json \
  --session exp-20260821-pilot-baselines-eval-r01-mpnn_b_eval-s7-l7
```

## V2 analysis after every authorized cell has a natural-end result

```bash
python3 -m CODE.experiment_platform.v2_analysis \
  --experiment EXPERIMENTS/EXP-20260821-PILOT-BASELINES-EVAL-R01 \
  --authorization EXPERIMENTS/EXP-20260821-PILOT-BASELINES-EVAL-R01/authorization.json \
  --out ANALYSIS/EXP-20260821-PILOT-BASELINES-EVAL-R01/v2-paired
```

The output is evidence-bound analysis only; claim-support and value-gate review remain required.