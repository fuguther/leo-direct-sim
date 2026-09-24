# EXP-20260923-T1-STEP5-MICRO-R04

Runtime: `leo_sim_v2`; compilation only, no run is launched.

Each cell is an independent controlled command after review, authorization, and clean deployment:

## Design accounting

2 planned cells; 2 unique resolved configurations; 0 exact re-execution cells.

Exact re-executions are repeatability evidence only and do not increase the independent-condition count.

## EXP-20260923-T1-STEP5-MICRO-R04-control-s7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260923-T1-STEP5-MICRO-R04/resolved/EXP-20260923-T1-STEP5-MICRO-R04-control-s7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260923-T1-STEP5-MICRO-R04/authorization.json \
  --session exp-20260923-t1-step5-micro-r04-control-s7
```

## EXP-20260923-T1-STEP5-MICRO-R04-cd05-s7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260923-T1-STEP5-MICRO-R04/resolved/EXP-20260923-T1-STEP5-MICRO-R04-cd05-s7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260923-T1-STEP5-MICRO-R04/authorization.json \
  --session exp-20260923-t1-step5-micro-r04-cd05-s7
```

## V2 analysis after every authorized cell has a natural-end result

```bash
python3 -m CODE.experiment_platform.v2_analysis \
  --experiment EXPERIMENTS/EXP-20260923-T1-STEP5-MICRO-R04 \
  --authorization EXPERIMENTS/EXP-20260923-T1-STEP5-MICRO-R04/authorization.json \
  --out ANALYSIS/EXP-20260923-T1-STEP5-MICRO-R04/v2-paired
```

The output is evidence-bound analysis only; claim-support and value-gate review remain required.