# EXP-20260822-INFO-LADDER-FORMAL-R02

Runtime: `leo_sim_v2`; compilation only, no run is launched.

Each cell is an independent controlled command after review, authorization, and clean deployment:

## EXP-20260822-INFO-LADDER-FORMAL-R02-info_queue-s7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260822-INFO-LADDER-FORMAL-R02/resolved/EXP-20260822-INFO-LADDER-FORMAL-R02-info_queue-s7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260822-INFO-LADDER-FORMAL-R02/authorization.json \
  --session exp-20260822-info-ladder-formal-r02-info_queue-s7
```

## EXP-20260822-INFO-LADDER-FORMAL-R02-info_physical-s7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260822-INFO-LADDER-FORMAL-R02/resolved/EXP-20260822-INFO-LADDER-FORMAL-R02-info_physical-s7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260822-INFO-LADDER-FORMAL-R02/authorization.json \
  --session exp-20260822-info-ladder-formal-r02-info_physical-s7
```

## EXP-20260822-INFO-LADDER-FORMAL-R02-info_queue-s11

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260822-INFO-LADDER-FORMAL-R02/resolved/EXP-20260822-INFO-LADDER-FORMAL-R02-info_queue-s11.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260822-INFO-LADDER-FORMAL-R02/authorization.json \
  --session exp-20260822-info-ladder-formal-r02-info_queue-s11
```

## EXP-20260822-INFO-LADDER-FORMAL-R02-info_physical-s11

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260822-INFO-LADDER-FORMAL-R02/resolved/EXP-20260822-INFO-LADDER-FORMAL-R02-info_physical-s11.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260822-INFO-LADDER-FORMAL-R02/authorization.json \
  --session exp-20260822-info-ladder-formal-r02-info_physical-s11
```

## V2 analysis after every authorized cell has a natural-end result

```bash
python3 -m CODE.experiment_platform.v2_analysis \
  --experiment EXPERIMENTS/EXP-20260822-INFO-LADDER-FORMAL-R02 \
  --authorization EXPERIMENTS/EXP-20260822-INFO-LADDER-FORMAL-R02/authorization.json \
  --out ANALYSIS/EXP-20260822-INFO-LADDER-FORMAL-R02/v2-paired
```

The output is evidence-bound analysis only; claim-support and value-gate review remain required.