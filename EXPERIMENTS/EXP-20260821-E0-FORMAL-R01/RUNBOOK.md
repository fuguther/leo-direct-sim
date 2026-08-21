# EXP-20260821-E0-FORMAL-R01

Runtime: `leo_sim_v2` (no legacy fallback).

Required order: three independent reviews -> finalization -> authorization -> clean deployment -> formal remote run.

Run id: `EXP-20260821-E0-FORMAL-R01-main-s7`

Authorize after the accepted finalization exists:

```bash
python3 CODE/experiment_platform/authorize_experiment.py \
  --experiment EXPERIMENTS/EXP-20260821-E0-FORMAL-R01 \
  --finalization CODE/work/WP-LEO-V2-E0-FORMAL/R01/finalization.json \
  --out EXPERIMENTS/EXP-20260821-E0-FORMAL-R01/authorization.json
```

Deploy a clean commit with `CODE/scripts/remote/push-remote.sh`, then launch:

```bash
CODE/scripts/remote/run-remote.sh \
  --runtime-kind leo_sim_v2 \
  --config EXPERIMENTS/EXP-20260821-E0-FORMAL-R01/resolved/EXP-20260821-E0-FORMAL-R01-main-s7.leo-sim.yaml \
  --authorization EXPERIMENTS/EXP-20260821-E0-FORMAL-R01/authorization.json \
  --session exp-20260821-e0-formal-r01
```
