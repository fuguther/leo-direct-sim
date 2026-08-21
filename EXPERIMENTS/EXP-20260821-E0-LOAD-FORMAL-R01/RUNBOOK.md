# EXP-20260821-E0-LOAD-FORMAL-R01

Runtime: `leo_sim_v2`; compilation only, no run is launched.

Each cell is an independent controlled command after review, authorization, and clean deployment:

## EXP-20260821-E0-LOAD-FORMAL-R01-low_control-s7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260821-E0-LOAD-FORMAL-R01/resolved/EXP-20260821-E0-LOAD-FORMAL-R01-low_control-s7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260821-E0-LOAD-FORMAL-R01/authorization.json \
  --session exp-20260821-e0-load-formal-r01-low_control-s7
```

## EXP-20260821-E0-LOAD-FORMAL-R01-low_copy-s7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260821-E0-LOAD-FORMAL-R01/resolved/EXP-20260821-E0-LOAD-FORMAL-R01-low_copy-s7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260821-E0-LOAD-FORMAL-R01/authorization.json \
  --session exp-20260821-e0-load-formal-r01-low_copy-s7
```

## EXP-20260821-E0-LOAD-FORMAL-R01-medium_control-s7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260821-E0-LOAD-FORMAL-R01/resolved/EXP-20260821-E0-LOAD-FORMAL-R01-medium_control-s7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260821-E0-LOAD-FORMAL-R01/authorization.json \
  --session exp-20260821-e0-load-formal-r01-medium_control-s7
```

## EXP-20260821-E0-LOAD-FORMAL-R01-medium_copy-s7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260821-E0-LOAD-FORMAL-R01/resolved/EXP-20260821-E0-LOAD-FORMAL-R01-medium_copy-s7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260821-E0-LOAD-FORMAL-R01/authorization.json \
  --session exp-20260821-e0-load-formal-r01-medium_copy-s7
```

## EXP-20260821-E0-LOAD-FORMAL-R01-high_control-s7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260821-E0-LOAD-FORMAL-R01/resolved/EXP-20260821-E0-LOAD-FORMAL-R01-high_control-s7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260821-E0-LOAD-FORMAL-R01/authorization.json \
  --session exp-20260821-e0-load-formal-r01-high_control-s7
```

## EXP-20260821-E0-LOAD-FORMAL-R01-high_copy-s7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260821-E0-LOAD-FORMAL-R01/resolved/EXP-20260821-E0-LOAD-FORMAL-R01-high_copy-s7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260821-E0-LOAD-FORMAL-R01/authorization.json \
  --session exp-20260821-e0-load-formal-r01-high_copy-s7
```

## V2 analysis after every authorized cell has a natural-end result

```bash
python3 -m CODE.experiment_platform.v2_analysis \
  --experiment EXPERIMENTS/EXP-20260821-E0-LOAD-FORMAL-R01 \
  --authorization EXPERIMENTS/EXP-20260821-E0-LOAD-FORMAL-R01/authorization.json \
  --out ANALYSIS/EXP-20260821-E0-LOAD-FORMAL-R01/v2-paired
```

The output is evidence-bound analysis only; claim-support and value-gate review remain required.