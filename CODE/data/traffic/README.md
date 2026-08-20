# Traffic inputs

`mlab_2026-05-27.csv` is a checked-in M-Lab-derived **measurement proxy**. It is
an hourly city-to-city summary, not a packet capture and not a calibrated user
demand trace. The simulator uses `mean_throughput_mbps * sample_count` only to
weight source/destination choices; it does not claim that these measurements
are the offered load of a real satellite operator.

The compiler maps each latitude/longitude to the configured V2 grid and records
the source SHA-256, row count, OD-pair count, and observed UTC hours in the
trace manifest. Invalid rows, missing fields, zero/negative measurements, and
out-of-range hours fail closed. No silent uniform fallback is allowed.

`mlab` may be combined with an explicit burst window. That means “measured OD
weights plus a reproducible stress transform”, not a measured burst. The burst
is recorded in the manifest and must be analysed separately from the
measurement-proxy baseline.

The source snapshot was prepared from the public M-Lab measurement ecosystem;
the checked-in CSV and its SHA are the reproducibility boundary for this repo.
The source fields and units are described by
`mlab_measured_od_burst.schema.json`. Raw client identifiers and packet-level
records are not present.
