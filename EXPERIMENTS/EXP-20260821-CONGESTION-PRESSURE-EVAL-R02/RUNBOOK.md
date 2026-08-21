# EXP-20260821-CONGESTION-PRESSURE-EVAL-R02

Runtime: `leo_sim_v2`; compilation only, no run is launched.

Each cell is an independent controlled command after review, authorization, and clean deployment:

## EXP-20260821-CONGESTION-PRESSURE-EVAL-R02-qlearning_pressure_ddqn-s7-l7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260821-CONGESTION-PRESSURE-EVAL-R02/resolved/EXP-20260821-CONGESTION-PRESSURE-EVAL-R02-qlearning_pressure_ddqn-s7-l7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260821-CONGESTION-PRESSURE-EVAL-R02/authorization.json \
  --session exp-20260821-congestion-pressure-eval-r02-qlearning_pressure_ddqn-s7-l7
```

## EXP-20260821-CONGESTION-PRESSURE-EVAL-R02-qlearning_pressure_gat-s7-l7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260821-CONGESTION-PRESSURE-EVAL-R02/resolved/EXP-20260821-CONGESTION-PRESSURE-EVAL-R02-qlearning_pressure_gat-s7-l7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260821-CONGESTION-PRESSURE-EVAL-R02/authorization.json \
  --session exp-20260821-congestion-pressure-eval-r02-qlearning_pressure_gat-s7-l7
```

## EXP-20260821-CONGESTION-PRESSURE-EVAL-R02-qlearning_pressure_mpnn-s7-l7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260821-CONGESTION-PRESSURE-EVAL-R02/resolved/EXP-20260821-CONGESTION-PRESSURE-EVAL-R02-qlearning_pressure_mpnn-s7-l7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260821-CONGESTION-PRESSURE-EVAL-R02/authorization.json \
  --session exp-20260821-congestion-pressure-eval-r02-qlearning_pressure_mpnn-s7-l7
```

## EXP-20260821-CONGESTION-PRESSURE-EVAL-R02-ddqn_c3_pressure-s7-l7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260821-CONGESTION-PRESSURE-EVAL-R02/resolved/EXP-20260821-CONGESTION-PRESSURE-EVAL-R02-ddqn_c3_pressure-s7-l7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260821-CONGESTION-PRESSURE-EVAL-R02/authorization.json \
  --session exp-20260821-congestion-pressure-eval-r02-ddqn_c3_pressure-s7-l7
```

## EXP-20260821-CONGESTION-PRESSURE-EVAL-R02-gat_pressure-s7-l7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260821-CONGESTION-PRESSURE-EVAL-R02/resolved/EXP-20260821-CONGESTION-PRESSURE-EVAL-R02-gat_pressure-s7-l7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260821-CONGESTION-PRESSURE-EVAL-R02/authorization.json \
  --session exp-20260821-congestion-pressure-eval-r02-gat_pressure-s7-l7
```

## EXP-20260821-CONGESTION-PRESSURE-EVAL-R02-mpnn_pressure-s7-l7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260821-CONGESTION-PRESSURE-EVAL-R02/resolved/EXP-20260821-CONGESTION-PRESSURE-EVAL-R02-mpnn_pressure-s7-l7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260821-CONGESTION-PRESSURE-EVAL-R02/authorization.json \
  --session exp-20260821-congestion-pressure-eval-r02-mpnn_pressure-s7-l7
```

## V2 analysis after every authorized cell has a natural-end result

```bash
python3 -m CODE.experiment_platform.v2_analysis \
  --experiment EXPERIMENTS/EXP-20260821-CONGESTION-PRESSURE-EVAL-R02 \
  --authorization EXPERIMENTS/EXP-20260821-CONGESTION-PRESSURE-EVAL-R02/authorization.json \
  --out ANALYSIS/EXP-20260821-CONGESTION-PRESSURE-EVAL-R02/v2-paired
```

The output is evidence-bound analysis only; claim-support and value-gate review remain required.