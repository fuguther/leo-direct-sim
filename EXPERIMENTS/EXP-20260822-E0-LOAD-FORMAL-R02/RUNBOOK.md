# EXP-20260822-E0-LOAD-FORMAL-R02

Runtime: `leo_sim_v2`; compilation only, no run is launched.

Each cell is an independent controlled command after review, authorization, and clean deployment:

## EXP-20260822-E0-LOAD-FORMAL-R02-low_control-s7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260822-E0-LOAD-FORMAL-R02/resolved/EXP-20260822-E0-LOAD-FORMAL-R02-low_control-s7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260822-E0-LOAD-FORMAL-R02/authorization.json \
  --session exp-20260822-e0-load-formal-r02-low_control-s7
```

## EXP-20260822-E0-LOAD-FORMAL-R02-low_copy-s7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260822-E0-LOAD-FORMAL-R02/resolved/EXP-20260822-E0-LOAD-FORMAL-R02-low_copy-s7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260822-E0-LOAD-FORMAL-R02/authorization.json \
  --session exp-20260822-e0-load-formal-r02-low_copy-s7
```

## EXP-20260822-E0-LOAD-FORMAL-R02-medium_control-s7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260822-E0-LOAD-FORMAL-R02/resolved/EXP-20260822-E0-LOAD-FORMAL-R02-medium_control-s7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260822-E0-LOAD-FORMAL-R02/authorization.json \
  --session exp-20260822-e0-load-formal-r02-medium_control-s7
```

## EXP-20260822-E0-LOAD-FORMAL-R02-medium_copy-s7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260822-E0-LOAD-FORMAL-R02/resolved/EXP-20260822-E0-LOAD-FORMAL-R02-medium_copy-s7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260822-E0-LOAD-FORMAL-R02/authorization.json \
  --session exp-20260822-e0-load-formal-r02-medium_copy-s7
```

## EXP-20260822-E0-LOAD-FORMAL-R02-high_control-s7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260822-E0-LOAD-FORMAL-R02/resolved/EXP-20260822-E0-LOAD-FORMAL-R02-high_control-s7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260822-E0-LOAD-FORMAL-R02/authorization.json \
  --session exp-20260822-e0-load-formal-r02-high_control-s7
```

## EXP-20260822-E0-LOAD-FORMAL-R02-high_copy-s7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260822-E0-LOAD-FORMAL-R02/resolved/EXP-20260822-E0-LOAD-FORMAL-R02-high_copy-s7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260822-E0-LOAD-FORMAL-R02/authorization.json \
  --session exp-20260822-e0-load-formal-r02-high_copy-s7
```

## V2 analysis after every authorized cell has a natural-end result

```bash
python3 -m CODE.experiment_platform.v2_analysis \
  --experiment EXPERIMENTS/EXP-20260822-E0-LOAD-FORMAL-R02 \
  --authorization EXPERIMENTS/EXP-20260822-E0-LOAD-FORMAL-R02/authorization.json \
  --out ANALYSIS/EXP-20260822-E0-LOAD-FORMAL-R02/v2-paired
```

The output is evidence-bound analysis only; claim-support and value-gate review remain required.