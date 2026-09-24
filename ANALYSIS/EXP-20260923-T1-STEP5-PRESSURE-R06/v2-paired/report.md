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

### EXP-20260923-T1-STEP5-PRESSURE-R06-control-s7

- MCS samples: `0`; MCS zero-rate holds: `0`; rate range: `0`–`0` bps
- control registered/completed: `57696`/`28800`
- directed ISL links: `48`; saturated directed ISL links: `none`
- 1 s active-window p99/max utilization: `0.8999999999999987`/`1.0000000000000568`; sustained hotspot links: `[]`
- episode-coincident pressure-candidate links: `[]`
- drain residue packets/unmatched ISL queue entries: `162`/`0`
- matched/unmatched ISL queue entries: `2222`/`0`

### EXP-20260923-T1-STEP5-PRESSURE-R06-cd05-s7

- MCS samples: `0`; MCS zero-rate holds: `0`; rate range: `0`–`0` bps
- control registered/completed: `57696`/`28800`
- directed ISL links: `48`; saturated directed ISL links: `none`
- 1 s active-window p99/max utilization: `0.8898162297627801`/`1.0000000000000568`; sustained hotspot links: `[]`
- episode-coincident pressure-candidate links: `[]`
- drain residue packets/unmatched ISL queue entries: `162`/`0`
- matched/unmatched ISL queue entries: `2222`/`0`

This output is evidence-bound analysis, not a paper claim.
Independent claim-support and value-gate review remains required.
