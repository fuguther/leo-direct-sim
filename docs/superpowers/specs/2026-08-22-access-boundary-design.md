# Access boundary design (2026-08-22)

This change isolates ground-to-satellite access coverage from congestion.
`access.unavailable_policy` is an explicit enum: `reject` (the default,
backward-compatible behavior) or `queue`. Unknown values fail closed.

In `queue` mode a packet emitted while no satellite is visible enters the
existing finite endpoint uplink queue and is retried by the existing access
ticker. It is not an infinite cache and does not bypass FIFO, queue capacity,
overflow, or conservation. If the run stops before first satellite ingress,
the packet fate is `IN_SYSTEM_AT_STOP`; it is not `DELIVERED` or
`ACCESS_REJECTED`. The explicit queue profile is an engineering diagnostic,
not a paper result. Existing historical M-Lab profiles retain their meaning;
new E0 calibration and training are required for the new semantics.

The only admission event is `satellite_ingress`, emitted at the successful
arrival of an uplink propagation event. It is exactly once per packet and is
not inferred from queue entry, service start, or propagation start.
Metrics v2 reports offered, admitted-at-ingress, and delivered packets/bits,
per-packet `admitted_at` and emitted-to-ingress `access_wait_s`, plus
`access_admission_rate` and `network_delivery_rate_by_horizon`. The existing
v1 `delivery_rate` meaning and v1 ledger fixtures remain unchanged.

Coverage scanning is deterministic evidence for a specified constellation,
simulation horizon/phase, step, and endpoint set. It reports visibility
fractions, first wait, no-coverage gaps, and visible-satellite counts with
provenance. It does not prove capacity is sufficient and does not choose
whether or how to add satellites; that remains an evidence-based design
decision after the audit.
