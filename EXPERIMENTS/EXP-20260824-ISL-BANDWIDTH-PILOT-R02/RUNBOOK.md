# EXP-20260824-ISL-BANDWIDTH-PILOT-R02

Runtime: `leo_sim_v2`; compilation only, no run is launched.

Cells are listed in mandatory order; every later command is blocked until its predecessors pass the serial evidence gate:

Execution policy: `serial_fail_closed`. The canonical runner applies a machine-enforced serial predecessor gate before every cell after the first; missing or ineligible pulled predecessor evidence blocks the next launch.

## EXP-20260824-ISL-BANDWIDTH-PILOT-R02-b500-s7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260824-ISL-BANDWIDTH-PILOT-R02/resolved/EXP-20260824-ISL-BANDWIDTH-PILOT-R02-b500-s7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260824-ISL-BANDWIDTH-PILOT-R02/authorization.json \
  --session exp-20260824-isl-bandwidth-pilot-r02-b500-s7
```

## EXP-20260824-ISL-BANDWIDTH-PILOT-R02-b50-s7

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260824-ISL-BANDWIDTH-PILOT-R02/resolved/EXP-20260824-ISL-BANDWIDTH-PILOT-R02-b50-s7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260824-ISL-BANDWIDTH-PILOT-R02/authorization.json \
  --session exp-20260824-isl-bandwidth-pilot-r02-b50-s7
```

## V2 analysis after every authorized cell has a natural-end result

```bash
python3 -m CODE.experiment_platform.v2_analysis \
  --experiment EXPERIMENTS/EXP-20260824-ISL-BANDWIDTH-PILOT-R02 \
  --authorization EXPERIMENTS/EXP-20260824-ISL-BANDWIDTH-PILOT-R02/authorization.json \
  --out ANALYSIS/EXP-20260824-ISL-BANDWIDTH-PILOT-R02/v2-paired
```

The output is evidence-bound analysis only; claim-support and value-gate review remain required.