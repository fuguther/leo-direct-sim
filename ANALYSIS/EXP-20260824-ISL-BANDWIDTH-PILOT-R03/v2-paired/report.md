# leo_sim V2 paired analysis

- status: `VERIFIED`
- primary metric: `isl_link_utilization_max`
- verified runs: `2`

## Run diagnostics

### EXP-20260824-ISL-BANDWIDTH-PILOT-R03-b5-s7

- MCS samples: `2354177`; MCS zero-rate holds: `0`; rate range: `29504275`–`2950427500` bps
- control registered/completed: `2344720`/`2343600`
- directed ISL links: `1120`; saturated directed ISL links: `none`
- 1 s active-window p99/max utilization: `0.46727570561645143`/`0.9674623423216687`; sustained hotspot links: `['isl:267:7', 'isl:4:3', 'isl:5:4', 'isl:6:5', 'isl:7:6']`
- episode-coincident pressure-candidate links: `[]`
- drain residue packets/unmatched ISL queue entries: `0`/`0`
- matched/unmatched ISL queue entries: `6863`/`0`

### EXP-20260824-ISL-BANDWIDTH-PILOT-R03-b2-s7

- MCS samples: `2354177`; MCS zero-rate holds: `0`; rate range: `11801710`–`2950427500` bps
- control registered/completed: `2344720`/`2343600`
- directed ISL links: `1120`; saturated directed ISL links: `none`
- 1 s active-window p99/max utilization: `0.91862264100115`/`0.918660276684619`; sustained hotspot links: `['isl:147:167', 'isl:167:187', 'isl:187:207', 'isl:207:227', 'isl:222:242', 'isl:227:247', 'isl:22:42', 'isl:242:262', 'isl:247:267', 'isl:248:268', 'isl:262:2', 'isl:267:7', 'isl:4:3', 'isl:5:4', 'isl:6:5', 'isl:7:6']`
- episode-coincident pressure-candidate links: `['isl:147:167', 'isl:167:187', 'isl:222:242']`
- drain residue packets/unmatched ISL queue entries: `0`/`0`
- matched/unmatched ISL queue entries: `6863`/`0`

This output is evidence-bound analysis, not a paper claim.
Independent claim-support and value-gate review remains required.
