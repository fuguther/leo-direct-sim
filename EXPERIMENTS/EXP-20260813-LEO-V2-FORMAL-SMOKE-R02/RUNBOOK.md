# EXP-20260813-LEO-V2-FORMAL-SMOKE-R02

Runtime: `leo_sim_v2` (no legacy fallback).

Required order: three independent reviews -> finalization -> authorization -> clean deployment -> formal remote run.

Run id: `EXP-20260813-LEO-V2-FORMAL-SMOKE-R02-main-s7`

Authorize after the accepted finalization exists:

```bash
python3 CODE/experiment_platform/authorize_experiment.py \
  --experiment EXPERIMENTS/EXP-20260813-LEO-V2-FORMAL-SMOKE-R02 \
  --finalization CODE/work/WP-LEO-V2-FORMAL-SMOKE/R02/finalization.json \
  --out EXPERIMENTS/EXP-20260813-LEO-V2-FORMAL-SMOKE-R02/authorization.json
```

Deploy a clean commit with `CODE/scripts/remote/push-remote.sh`, then launch:

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260813-LEO-V2-FORMAL-SMOKE-R02/resolved/EXP-20260813-LEO-V2-FORMAL-SMOKE-R02-main-s7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260813-LEO-V2-FORMAL-SMOKE-R02/authorization.json \
  --session exp-20260813-leo-v2-formal-smoke-r02
```
