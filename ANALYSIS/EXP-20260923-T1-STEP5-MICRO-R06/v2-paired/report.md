# leo_sim V2 paired analysis

- status: `VERIFIED`
- primary metric: `e2e_delay_mean_s`
- verified runs: `2`

## Design accounting

- planned cells: `2`
- unique resolved configurations: `2`
- exact re-execution cells: `0`
- exact re-executions are repeatability evidence, not additional independent conditions

## Run diagnostics

### EXP-20260923-T1-STEP5-MICRO-R06-control-s7

- MCS samples: `0`; MCS zero-rate holds: `0`; rate range: `0`–`0` bps
- control registered/completed: `656`/`640`
- directed ISL links: `16`; saturated directed ISL links: `none`
- 1 s active-window p99/max utilization: `1.0000000000000002`/`1.0000000000000002`; sustained hotspot links: `['isl:0:1', 'isl:1:2']`
- episode-coincident pressure-candidate links: `['isl:0:1']`
- drain residue packets/unmatched ISL queue entries: `0`/`0`
- matched/unmatched ISL queue entries: `12`/`0`

### EXP-20260923-T1-STEP5-MICRO-R06-cd05-s7

- MCS samples: `0`; MCS zero-rate holds: `0`; rate range: `0`–`0` bps
- control registered/completed: `656`/`640`
- directed ISL links: `16`; saturated directed ISL links: `none`
- 1 s active-window p99/max utilization: `1.0000000000000002`/`1.0000000000000002`; sustained hotspot links: `['isl:0:1', 'isl:1:2']`
- episode-coincident pressure-candidate links: `['isl:0:1']`
- drain residue packets/unmatched ISL queue entries: `0`/`0`
- matched/unmatched ISL queue entries: `12`/`0`

This output is evidence-bound analysis, not a paper claim.
Independent claim-support and value-gate review remains required.
