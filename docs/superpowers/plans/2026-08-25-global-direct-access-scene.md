# Global populated-land direct-access scene implementation plan

> **For DeepSeek Harness:** Execute this plan task-by-task with the `standard` preset, keep an explicit plan, and use test-driven development for every behavior change. The producer must stop at a review-ready PR; because this plan touches `kernel.py` and receipt-adjacent evidence contracts, DeepSeek Harness may not self-approve or self-merge.

**Goal:** Build an honest, scalable 1-degree global populated-land direct-access scene, prove that every populated candidate region is included in the coverage and demand support, separate access limitation from ISL pressure, and leave a verified path for a later bounded pressure calibration. Do not run an algorithm-comparison matrix in this work package.

**Architecture:** Keep all positive-population 1-degree cells as the potential user universe, but instantiate only cells that actually emit or receive packets in a finite trace. Generate population-weighted, local-time-varying Poisson demand and exact gravity destinations. Audit the full candidate universe with a chunked geometry-only coverage engine. Generate load arms as deterministic nested subsets of one master demand trace. Finally, classify each diagnostic run through independent coverage, access, route, and ISL-pressure gates, so access failure can never be mislabeled as ISL congestion.

**Tech Stack:** Python 3, NumPy, SimPy, PyYAML, Pillow GeoTIFF reader, pytest, existing `leo_sim` config/trace/coverage/receipt/metrics contracts, existing experiment-platform compiler and canonical remote launcher.

---

## 0. DeepSeek Harness execution contract

DeepSeek Harness is the implementation runner, not the scientific authority. Codex owns final scope control, exact-SHA verification, finding adjudication, and the decision to authorize any later VM calibration. Kimi may provide a candidate cold review, but neither worker may turn its own output into accepted evidence.

The currently inspected local runner is DeepSeek Harness `0.1.0-rc.8` from source commit `141eb6fef83422698aef7a981029e843e8161534`. It is a developer-preview dependency, so the implementation receipt must record the actual runner version and source commit used. If either differs, stop and report the difference before editing; do not silently upgrade, rebuild from another revision, or claim runner equivalence.

Execution rules:

- Use the existing DeepSeek Harness `standard` preset and configured model route; never write API keys, `.credentials.yaml`, `.env`, or machine-specific provider configuration into this repository.
- Select only the isolated implementation worktree as the Harness workspace. Do not select or modify the user's dirty checkout, the DeepSeek Harness source checkout, or the old LEO repository.
- Feed Harness this entire plan, not a paraphrased one-line request. It must keep Task 0 through Task 9 as the authoritative order and may not add a formal matrix, RL work, report edits, or unrelated cleanup.
- Before each task, Harness records the exact starting SHA and the task-local allowed file list. After each task, it runs the listed tests, inspects `git diff --name-only`, and commits only that task's declared theme.
- Harness must pause with `NEEDS_CODEX_JUDGMENT` when a stop condition fires, a listed contract must change, a tracked path would be deleted/moved/overwritten, a test appears to require weakening, or evidence conflicts. It may fix ordinary implementation defects within the declared scope without asking the user.
- Harness stops at `PR_READY_FOR_INDEPENDENT_REVIEW`; it does not merge, deploy to the VM, authorize experiments, or interpret the local smoke as a research result.

The Web UI handoff text is intentionally short because this document carries the full contract:

```text
Implement docs/superpowers/plans/2026-08-25-global-direct-access-scene.md exactly, Task 0 through Task 9. Use the standard preset and TDD. Work only in the isolated worktree created from current origin/main. Obey AGENTS.md and every exclusion, stop condition, file list, test, evidence, and claim boundary in the plan. Do not edit mentor reports, run a formal matrix, deploy, self-approve, or merge. On an ordinary in-scope defect, diagnose and fix it. On a contract conflict or stop condition, stop with NEEDS_CODEX_JUDGMENT and preserve the evidence. Final state must be PR_READY_FOR_INDEPENDENT_REVIEW with exact SHA, diff, test counts, benchmark results, smoke receipt, and unresolved limitations.
```

---

## 1. Decision and claim boundary

The scene definition is:

- Spatial support: all positive-population cells from the checked-in GPW raster aggregated to 1 degree. On the current audited asset this is 16,988 cells and source SHA-256 `c5742d16fc01d454e8ac5c5345a7e7716883acd28ac4d0d34c24613bc315e59a`.
- Runtime activity: sparse and stochastic. A cell is a potential source even when it emits no packet in a finite run. The trace-derived source set, destination set, and runtime endpoint set must be reported separately.
- Time: source intensity varies by a declared local-solar-time proxy. This is a population proxy, not measured operator demand and not calibrated subscriber traffic.
- Destination: gravity demand with an exact scalable sampler. No uniform or nearest-neighbour fallback is allowed.
- Access: intermittent geometric opportunity and access queues are measured as their own layer.
- Pressure: ISL pressure is accepted only when access and route gates are clean enough that the observed queue/utilization signal cannot reasonably be attributed to failure before ISL entry.
- Geographic claim: this work package supports **global populated-land direct access**. It does not cover maritime, aviation, polar expeditions in empty cells, or every point on Earth.
- Statistical claim: one smoke or one seed is diagnostic only. It cannot support an algorithm ranking, a universal congestion threshold, or a paper claim.

External source check behind this boundary:

- The 6G-NTN space-segment study treats population mapping as an input that still needs explicit UE adoption and service assumptions; therefore population must remain a proxy, not “real user traffic”: <https://6g-ntn.eu/wp-content/uploads/2026/02/6G-NTN_D3.10_r2_v00.pdf>.
- A recent LEO-NTN handover study uses a population-plus-local-time spatiotemporal field as a simulation model; this supports the model form, not calibration to a real operator: <https://pmc.ncbi.nlm.nih.gov/articles/PMC12987173/>.
- Congestion work reports utilization together with queue behaviour rather than treating loss or delivery alone as proof of congestion: <https://doi.org/10.1109/TNET.2006.883130>.

The checked baseline, before any implementation, is:

```text
base commit: 98d9092751abd84a3d3ad6b39e932e5e501740c0
leo_sim + CODE/tests subset: 598 passed, 1 skipped
CI-equivalent suite: 686 passed, 1 skipped, 3 subtests passed
legacy population profile trace SHA-256: 0780da2fedea503d5f600830aecc805c95b1b8fc098395150ecaf2185846279a
legacy population profile trace identity SHA-256: 2715dfb316de48d958cd05fa09aafcf22e340766d186e7a0a9a9b6a4b0dd9ad4
legacy population profile: 1,061 candidates, 108 packets, 127 runtime endpoints
1-degree population candidates: 16,988
0.5-degree population candidates: 61,295 (future sensitivity only)
```

## 2. Explicit exclusions

DeepSeek Harness must not do any of the following in this work package:

- Do not edit either mentor report, any group-meeting report, or any `.docx` file.
- Do not edit RL, Q0-I, Q0-F, Q0-J, reward, observation, or new-algorithm code.
- Do not create or launch a formal algorithm-comparison matrix.
- Do not copy code or data from the old private platform into this repository.
- Do not call the 56-cell M-Lab scenario global. Keep it as a separate measurement-proxy diagnostic.
- Do not make all 16,988 cells permanent runtime processes merely to say they are “online”.
- Do not switch to 0.5-degree demand in the first implementation.
- Do not raise entity/event/packet limits until a measured diagnostic proves the existing limit is the blocker.
- Do not reduce satellite bandwidth, slots, coverage, or queue capacity while searching the first demand-induced ISL-pressure bracket. If no pressure appears in the registered load menu, stop with `PRESSURE_NOT_FOUND_WITHIN_REGISTERED_ENVELOPE`.
- Do not change a failed test, receipt verifier, or acceptance threshold merely to make a run pass.

## 3. Layered acceptance ladder

Each layer is independent. A later layer is not evaluated if an earlier required artifact is invalid.

| Layer | Question | Required evidence | Allowed conclusion |
|---|---|---|---|
| L0 integrity | Did the requested code/config/trace actually run and end correctly? | exact SHA, immutable trace, natural end, conservation, receipt verification | engineering run is valid |
| L1 coverage | Was every 1-degree populated cell audited for access opportunity? | population source SHA, 16,988 candidates, full endpoint ledger, sampled horizon/step, no omitted cell | coverage within the audited time window |
| L2 demand | Does finite traffic have global population support and dynamic local-time intensity? | config-bound population/local-time model, observed source/destination/runtime sets, realized load | global-support population proxy trace |
| L3 access | Did packets reach the satellite network without access dominating the outcome? | access admission, access wait/overflow/rejection, uplink fate, route-entry exposure | access-clean or access-limited |
| L4 route | Did admitted packets obtain a legal route instead of stalling before ISL exposure? | no-route fates, holding events, first-ISL exposure, stop fate | route-clean or route-limited |
| L5 egress | Is downlink queue failure small enough not to confound the run? | ingress-bound downlink overflow, downlink wait, destination coverage | downlink-clean or downlink-limited |
| L6 ISL pressure | Is there sustained directed-link pressure after L3-L5 are clean? | directed link/time-window utilization with available-capacity denominator, ISL queue delay/overflow, exposed packets | ISL-pressure candidate or no pressure |

The single-run `scene_check.py` status vocabulary is closed:

```text
INVALID_EVIDENCE
COVERAGE_INCOMPLETE
ACCESS_LIMITED
ROUTE_LIMITED
DOWNLINK_LIMITED
NO_ISL_EXPOSURE
NO_ISL_PRESSURE
ISL_PRESSURE_CANDIDATE
```

`GLOBAL_SUPPORT_DIAGNOSTIC` is an allowed trace/coverage claim label, not a run status. `PRESSURE_NOT_FOUND_WITHIN_REGISTERED_ENVELOPE` is a later menu-level outcome emitted only after every predeclared load arm is classified `NO_ISL_PRESSURE`; it is not emitted by a single-run checker. This work package ends at `PR_READY_FOR_INDEPENDENT_REVIEW`, not at calibration readiness.

---

### Task 0: Start from a clean exact base

**Files:** No repository edits.

- [ ] Run `git fetch origin`.
- [ ] Run `git status --short --branch` in the user's checkout. If it is dirty, do not stash, clean, or commit it.
- [ ] Record DeepSeek Harness version, source commit, preset, and model route name without recording any credential value.
- [ ] Create an isolated worktree from the then-current `origin/main` using branch `dsh/20260825-global-direct-access`.
- [ ] Record `git rev-parse HEAD`, `git rev-parse origin/main`, and `git status --porcelain=v1`.
- [ ] Run the CI-equivalent baseline:

```bash
python3 scripts/check_document_governance.py --mode all
python3 -m pytest CODE/leo_sim/tests CODE/experiment_platform/tests CODE/tests -q
```

Expected: document governance has 0 selected errors, pytest is green, and the worktree is clean. The recorded `686 passed, 1 skipped, 3 subtests passed` count is context only; DeepSeek Harness must record the new exact count from its actual base.

**Stop conditions:** main is red; origin cannot be fetched; the isolated worktree is not clean; the checked population raster SHA differs from the value above. Report the exact mismatch and stop before editing.

### Task 1: Freeze the minimal configuration contract

**Files:**

- Modify: `CODE/leo_sim/config.py`
- Modify: `CODE/leo_sim/receipt.py`
- Test: `CODE/leo_sim/tests/test_config.py`
- Test: `CODE/leo_sim/tests/test_trace.py`
- Test: `CODE/leo_sim/tests/test_receipt.py`

Add only these fields:

```python
# scenario
"geometry_epoch_s": (int, float),

# demand
"temporal_model": str,
"utc_start_hour": (int, float),
"population_destination_sampler": str,
"destination_rejection_max_draws": int,
"nested_master_offered_mbps": (int, float, type(None)),
```

Defaults:

```python
"scenario": {
    "geometry_epoch_s": 0.0,
},
"demand": {
    "temporal_model": "constant",
    "utc_start_hour": 0.0,
    "population_destination_sampler": "scan",
    "destination_rejection_max_draws": 10_000,
    "nested_master_offered_mbps": None,
},
```

Validation contract:

```python
if sc["geometry_epoch_s"] < 0:
    raise ConfigError("scenario.geometry_epoch_s must be >= 0")
if dm["temporal_model"] not in {"constant", "local_diurnal_cosine"}:
    raise ConfigError(
        "demand.temporal_model must be constant or local_diurnal_cosine")
if dm["temporal_model"] == "local_diurnal_cosine" \
        and dm["mode"] != "population_gravity":
    raise ConfigError(
        "local_diurnal_cosine is only valid with population_gravity")
if not 0 <= dm["utc_start_hour"] < 24:
    raise ConfigError("demand.utc_start_hour must be in [0, 24)")
if dm["mode"] != "population_gravity" and dm["utc_start_hour"] != 0:
    raise ConfigError(
        "demand.utc_start_hour is only configurable for population_gravity")
if dm["population_destination_sampler"] not in {"scan", "alias_rejection"}:
    raise ConfigError(
        "demand.population_destination_sampler must be scan or alias_rejection")
if dm["population_destination_sampler"] != "scan" \
        and dm["mode"] != "population_gravity":
    raise ConfigError(
        "population destination sampler is only valid with population_gravity")
if dm["destination_rejection_max_draws"] < 1:
    raise ConfigError("demand.destination_rejection_max_draws must be >= 1")
master = dm["nested_master_offered_mbps"]
if master is not None:
    if dm["mode"] != "population_gravity":
        raise ConfigError(
            "nested master load is only valid with population_gravity")
    if master < dm["offered_mbps"]:
        raise ConfigError(
            "demand.nested_master_offered_mbps must be >= demand.offered_mbps")
```

The trace identity payload is a versioned evidence contract, so do not silently extend identity/v2. Freeze the current builder as `trace_identity_payload_v2()` and introduce `leo-sim-trace-identity/v3` for new compilations. The v2 builder must remove the five newly defaulted demand fields after config resolution so an old v2 receipt can be reconstructed byte-for-byte. Receipt v5 verification chooses the v2 or v3 builder from the persisted `trace_identity_contract`, accepts no other value, and never guesses from the current code version or the manifest schema. Identity/v1 support remains unchanged.

- [ ] First write failing tests for every invalid combination and every boundary.
- [ ] Add a regression compiling the unchanged `population_gravity.yaml` and assert that `trace.csv` SHA remains `0780da2fedea503d5f600830aecc805c95b1b8fc098395150ecaf2185846279a`. New compilations declare identity/v3; do not hard-code their not-yet-produced hash.
- [ ] Add a frozen old-v2 verification fixture whose trace identity is `2715dfb316de48d958cd05fa09aafcf22e340766d186e7a0a9a9b6a4b0dd9ad4`; prove it still verifies under the new code and fails if any old v2 trace-determining field is tampered.
- [ ] Assert `geometry_epoch_s` is excluded from `trace_identity_payload()` because it changes geometry, not trace bytes.
- [ ] Assert all five new demand fields are present in identity/v3, while the frozen identity/v2 builder removes exactly those fields and nothing else.
- [ ] Run:

```bash
python3 -m pytest CODE/leo_sim/tests/test_config.py CODE/leo_sim/tests/test_trace.py -q
```

Expected: all targeted tests pass and the legacy trace-byte regression stays exact.

- [ ] Commit: `feat: freeze global scene configuration contract`.

### Task 2: Add an explicit orbital phase block without changing default geometry

**Files:**

- Modify: `CODE/leo_sim/model.py`
- Modify: `CODE/leo_sim/kernel.py`
- Modify: `CODE/leo_sim/coverage.py`
- Test: `CODE/leo_sim/tests/test_model.py`
- Test: `CODE/leo_sim/tests/test_kernel.py`

Implementation rule: store `geometry_epoch_s` in `Constellation` and apply it once in `subpoint`; all higher geometry methods already depend on `subpoint` or `ecef`.

```python
def __init__(self, num_satellites: int, num_planes: int,
             altitude_km: float, inclination_deg: float,
             min_elevation_deg: float = 25.0,
             max_isl_km: float = 6000.0,
             geometry_epoch_s: float = 0.0):
    if not math.isfinite(float(geometry_epoch_s)) or geometry_epoch_s < 0:
        raise ValueError("geometry_epoch_s must be finite and >= 0")
    self.geometry_epoch_s = float(geometry_epoch_s)

def subpoint(self, sat_id: int, t: float) -> tuple[float, float, float]:
    at = float(t) + self.geometry_epoch_s
    plane = sat_id // self.per_plane
    idx = sat_id % self.per_plane
    raan = 2 * math.pi * plane / self.num_planes
    phase = 2 * math.pi * (idx / self.per_plane + at / self.period_s)
    inc = math.radians(self.inclination_deg)
    lat = math.asin(math.sin(inc) * math.sin(phase))
    lon_inertial = (
        math.atan2(math.cos(inc) * math.sin(phase), math.cos(phase)) + raan)
    lon = lon_inertial - EARTH_ROT_RATE_RAD_S * at
    lon = math.degrees((lon + math.pi) % (2 * math.pi) - math.pi)
    return math.degrees(lat), lon, self.altitude_km
```

- [ ] RED: for several satellites/times, assert `Constellation(epoch=x).ecef(s,t)` equals `Constellation(epoch=0).ecef(s,t+x)`.
- [ ] RED: assert epoch 0 is bit-equivalent to the old default for fixed expected subpoints.
- [ ] RED: run a one-packet kernel fixture at two epochs and prove the resolved epoch is actually passed to the geometry provider.
- [ ] GREEN: wire `cfg["scenario"]["geometry_epoch_s"]` into both kernel and coverage constructors.
- [ ] Run:

```bash
python3 -m pytest CODE/leo_sim/tests/test_model.py CODE/leo_sim/tests/test_kernel.py CODE/leo_sim/tests/test_coverage.py -q
```

- [ ] Commit: `feat: expose deterministic geometry phase blocks`.

### Task 3: Extend the existing coverage audit to all populated 1-degree cells

**Files:**

- Modify: `CODE/leo_sim/coverage.py`
- Test: `CODE/leo_sim/tests/test_coverage.py`
- Reuse without modification unless a defect is found: `CODE/leo_sim/population.py`

Do not create a second geometry implementation. Preserve `scan_coverage()` as the generic scalar reference. Add a `scan_constellation_coverage()` optimized path and compare it against the scalar function in tests.

The existing scalar caps remain unchanged: 10,000 endpoints and 50,000,000 scalar visibility calls. The population-vector path is a separate, explicit contract because even the required 600 s/60 s smoke is 52,323,040 comparisons and cannot legally pass through the scalar cap. It must fail before allocation unless all are true:

```text
endpoint_source == population_raster
endpoint_count <= 20,000
sample_count <= 1,000,001
endpoint_count * sample_count * satellite_count <= 50,000,000,000
0 < max_working_mib <= 4096
```

The optimized report records these four resolved limits, the calculated comparison count, chosen endpoint/time chunk sizes, projected bytes, observed peak RSS, and whether the full scan or only a bounded smoke ran. Do not raise the legacy constants or route arbitrary trace endpoints through the population exception.

The CLI must use mutually exclusive endpoint sources:

```text
--trace TRACE_DIR_OR_CSV
--population POPULATION_TIFF
```

Population mode loads `population.load_population_regions(path, aggregation_deg)` and emits one endpoint per positive-population region with a `population` weight.

Use the exact spherical footprint test for a same-altitude constellation. For Earth radius `R`, satellite radius `r`, and minimum elevation `e`, the maximum geocentric footprint angle is:

```python
elevation = math.radians(geometry.min_elevation_deg)
footprint_angle = math.acos(
    model.EARTH_RADIUS_KM / geometry.r * math.cos(elevation)) - elevation
cos_footprint = math.cos(footprint_angle)
visible = endpoint_unit_vectors @ satellite_unit_vectors.T > cos_footprint
```

Compute the cosine margin before classification. For pairs within a declared `64 * machine_epsilon` ambiguity band, fall back to the existing scalar `ground_visible()` predicate and count those fallbacks in the audit report. This keeps the fast path conservative at the floating-point boundary without pretending two algebraically equivalent formulas are bit-identical.

Chunk endpoints and times so peak working memory stays under a caller-specified `--max-working-mib` default of 256 MiB. Do not allocate an endpoint-by-satellite-by-all-times tensor. The report must include:

```json
{
  "schema": "leo-sim-coverage-audit/v2",
  "endpoint_source": {
    "type": "population_raster",
    "source_sha256": "64 lowercase hex characters",
    "aggregation_deg": 1.0,
    "candidate_regions": 16988,
    "total_population": 7969444350.355793
  },
  "scan": {
    "horizon_s": 86400.0,
    "step_s": 10.0,
    "sample_count": 8641,
    "sampling_error_bound_s": 10.0,
    "geometry_epoch_s": 0.0
  },
  "summary": {
    "endpoints_total": 16988,
    "never_visible": 0,
    "population_weighted_visible_fraction": 0.0,
    "population_weighted_never_visible_fraction": 0.0
  }
}
```

The zeros above are type examples, not expected scientific results. Tests must recompute all summary values from endpoint rows.

- [ ] RED: scalar and vector paths are identical on a small real `Constellation`; explicit `nextafter` cases just below, within, and above the strict visibility boundary exercise the scalar fallback and its counter.
- [ ] RED: population weights reject negative, non-finite, missing, duplicate, or silently omitted endpoints.
- [ ] RED: the output ledger contains each loaded population grid ID exactly once.
- [ ] RED: population-weighted summaries use the population denominator, not endpoint count.
- [ ] RED: a tampered source SHA/candidate count fails the L1 verifier.
- [ ] GREEN: implement chunked vectorized scanning and stable JSON v2 while retaining v1 trace-mode compatibility.
- [ ] Run the functional smoke:

```bash
python3 -m pytest CODE/leo_sim/tests/test_coverage.py -q
python3 -m CODE.leo_sim.coverage \
  --config CODE/leo_sim/profiles/population_gravity.yaml \
  --population CODE/population_map/gpw_v4_population_count_rev11_2020_15_min.tif \
  --horizon 600 --step 60 --max-working-mib 256 \
  --output /tmp/leo-global-coverage-smoke.json
```

Expected smoke facts: exact source SHA, 16,988 endpoints, 11 samples, no omitted IDs, stable repeat SHA.

- [ ] Benchmark the 280-satellite geometry at 600 s/10 s and project the cost of 24 h/10 s. Record wall time, max RSS, endpoint count, satellite count, sample count, and the raw visibility evaluation count. The full audit is 41,102,126,240 endpoint-satellite-sample comparisons.
- [ ] Do not run the full 24 h audit during implementation if projected wall time exceeds 60 minutes or projected RSS exceeds 4 GiB. Optimize or stop with measured evidence; do not coarsen the step and still call it the 10-second audit.
- [ ] Commit: `feat: audit global populated-land coverage in bounded memory`.

### Task 4: Add local-time-varying population demand without pretending it is measured traffic

**Files:**

- Modify: `CODE/leo_sim/trace.py`
- Modify: `CODE/leo_sim/receipt.py`
- Test: `CODE/leo_sim/tests/test_trace.py`
- Test: `CODE/leo_sim/tests/test_cli.py`

Keep legacy `mode: diurnal` bytes unchanged. For `population_gravity` only, apply the opt-in temporal model:

```python
def _rate_multiplier(mode: str, t: float, src_lon: float, dm: dict) -> float:
    if mode in ("burst", "mlab") and dm["burst_start_s"] is not None:
        start = dm["burst_start_s"]
        duration = dm["burst_duration_s"]
        return dm["burst_multiplier"] if start <= t < start + duration else 1.0
    if mode == "diurnal":
        # Preserve the historical trace contract exactly.
        local_hour = (t / 3600.0 + src_lon / 15.0) % 24.0
        amplitude = float(dm["diurnal_amplitude"])
        phase = float(dm["diurnal_phase_h"])
        return max(
            0.0,
            1.0 + amplitude
            * math.cos(2.0 * math.pi * (local_hour - phase) / 24.0),
        )
    if mode == "population_gravity" \
            and dm["temporal_model"] == "local_diurnal_cosine":
        local_hour = (
            dm["utc_start_hour"] + t / 3600.0 + src_lon / 15.0) % 24.0
        amplitude = float(dm["diurnal_amplitude"])
        phase = float(dm["diurnal_phase_h"])
        return max(
            0.0,
            1.0 + amplitude
            * math.cos(2.0 * math.pi * (local_hour - phase) / 24.0),
        )
    return 1.0
```

For `population_gravity + local_diurnal_cosine`, use `1 + abs(amplitude)` as the thinning envelope, exactly as legacy diurnal mode does. `offered_mbps` remains the baseline target before local-time modulation; `realized_offered_mbps` remains the truth for the finite trace.

Do not add unverified “online users” counts. The trace/scene audit must derive and name these sets:

```python
observed_source_regions = sorted({row["src_grid_id"] for row in rows})
observed_destination_regions = sorted({row["dst_grid_id"] for row in rows})
runtime_endpoint_regions = sorted(
    set(observed_source_regions) | set(observed_destination_regions))
```

The existing exact top-level manifest v2 key set must remain unchanged. Record the new transform inside the existing `traffic_transform.diurnal` value:

```python
{
    "amplitude": float(dm["diurnal_amplitude"]),
    "phase_h": float(dm["diurnal_phase_h"]),
    "utc_start_hour": float(dm["utc_start_hour"]),
    "clock": "source_local_solar_time_proxy"
}
```

Only the new population-local-time combination uses this four-key value. Legacy `mode: diurnal` retains its existing two-key value. Update receipt verification to reproduce this branch exactly; do not accept arbitrary extra keys.

- [ ] RED: longitude `0°` at UTC 12 and longitude `180°` at UTC 0 produce the declared local hour.
- [ ] RED: amplitude 0 is byte-equivalent to constant for the same population trace.
- [ ] RED: different UTC blocks change population trace bytes, while repeated compilation of one block is byte-identical.
- [ ] RED: the manifest remains `population_proxy`, `not_calibrated_user_demand=true`, and receipt verification rejects a tampered local-time transform.
- [ ] RED: a finite trace may have far fewer observed sources than 16,988 without changing candidate support; the audit reports both counts and never renames one as the other.
- [ ] Run:

```bash
python3 -m pytest CODE/leo_sim/tests/test_trace.py CODE/leo_sim/tests/test_cli.py -q
```

- [ ] Commit: `feat: add explicit local-time population demand proxy`.

### Task 5: Replace the O(N) population destination scan with an exact opt-in sampler

**Files:**

- Modify: `CODE/leo_sim/trace.py`
- Test: `CODE/leo_sim/tests/test_trace.py`

Default `scan` must preserve existing traces. `alias_rejection` must implement the same target distribution:

```text
P(dst=j | src=i) proportional to
population[j]^destination_population_exponent
/ max(distance(i,j), distance_floor_km)^gravity_alpha
```

Build one Vose alias table for proposal weights `population[j]^gamma`. For every source packet:

```python
def sample_population_destination(gen, alias, endpoints, src_index, dm):
    floor = float(dm["gravity_d_floor_km"])
    alpha = float(dm["gravity_alpha"])
    max_draws = int(dm["destination_rejection_max_draws"])
    src = endpoints[src_index]
    for _ in range(max_draws):
        candidate_index = alias.draw(gen)
        if candidate_index == src_index:
            continue
        dst = endpoints[candidate_index]
        distance = max(
            _haversine_km(src["lat"], src["lon"], dst["lat"], dst["lon"]),
            floor,
        )
        acceptance = (floor / distance) ** alpha
        if gen.random() < acceptance:
            return dst
    raise TraceError(
        "population alias_rejection exhausted "
        f"destination_rejection_max_draws={max_draws}")
```

There is no fallback to `scan`, uniform, nearest, or the last endpoint. The rejection cap is part of trace identity and must fail loudly.

- [ ] RED: scripted RNG draws exercise alias branch, same-source rejection, distance rejection, success, and cap exhaustion.
- [ ] RED: on a fixed three-region fixture, 200,000 deterministic samples match the normalized scan probabilities within an absolute tolerance of 0.01 for every destination.
- [ ] RED: the 1-degree population table builds one proposal table, not one O(N) table per source.
- [ ] Benchmark 10,000 destination draws at 1 degree. Acceptance: `alias_rejection` is at least 10 times faster than `scan` on the same machine and returns no invalid/self destination. If not, stop and profile rather than asserting scalability.
- [ ] For a deterministic 201-source sample that includes population and latitude extrema, compute the exact proposal acceptance probability, expected draws, observed draws, and the 10,000-draw exhaustion probability per source. Record min/median/max acceptance. If the worst calculated exhaustion probability exceeds `1e-9`, stop and revise the cap before accepting the sampler; speed alone is insufficient.
- [ ] Run:

```bash
python3 -m pytest CODE/leo_sim/tests/test_trace.py -q
```

- [ ] Commit: `feat: scale exact population gravity destination sampling`.

### Task 6: Build deterministic nested load families as a companion contract

**Files:**

- Modify: `CODE/leo_sim/trace.py`
- Modify: `CODE/leo_sim/rng.py`
- Modify: `CODE/leo_sim/receipt.py`
- Create: `CODE/leo_sim/trace_family.py`
- Create: `CODE/leo_sim/tests/test_trace_family.py`
- Modify: `CODE/leo_sim/tests/test_receipt.py`
- Modify only if required for CLI routing: `CODE/leo_sim/__main__.py`

Do not add nested metadata to the exact-key trace manifest v2. Write `nested-family.json` only when `nested_master_offered_mbps` is non-null.

Generation rule:

1. Generate candidate arrivals and destinations at `nested_master_offered_mbps` using the existing `demand` RNG stream.
2. Draw one independent `nested_filter` uniform value for every fully generated candidate.
3. Keep the candidate iff `u < offered_mbps / nested_master_offered_mbps`.
4. Sort kept rows and renumber packet IDs `1..N` in emission order.
5. Apply `execution.max_packets` to the master candidate count, not only the child count.

Append `nested_filter` to the end of the canonical `rng.STREAM_NAMES` tuple. The demand stream remains child 0 and the filter becomes child 7; it must not reuse child 1, which is already `ge_gsl` in the runtime RNG contract. NumPy's `SeedSequence(seed).spawn(1)[0] == SeedSequence(seed).spawn(8)[0]` state equality has been locally checked, but a permanent regression is still required.

```python
generators = rng.streams(sc["seed"])
demand_gen = generators["demand"]
filter_gen = generators["nested_filter"]
inclusion_probability = (
    float(dm["offered_mbps"])
    / float(dm["nested_master_offered_mbps"])
)
```

The manifest `rng_streams` contract branches exactly with the active feature: legacy and non-nested traces retain only the canonical demand mapping; nested traces select the canonical demand and nested-filter entries from the full mapping. Receipt verification reconstructs that same branch from the resolved config and rejects a missing, extra, wrongly indexed, or tampered stream. This is an exact contract change only for nested traces.

The companion schema is exact-key and versioned:

```json
{
  "schema": "leo-sim-nested-trace-family/v1",
  "family_identity_sha256": "64 lowercase hex characters",
  "master_offered_mbps": 80.0,
  "child_offered_mbps": 20.0,
  "inclusion_probability": 0.25,
  "master_candidate_packets": 1600,
  "child_packets": 400,
  "demand_rng_stream": "SeedSequence(7).spawn[0]",
  "filter_rng_stream": "SeedSequence(7).spawn[7]",
  "canonical_row_contract": "emit_time_s,src_grid_id,dst_grid_id,bits,deadline_at_s",
  "config_sha256": "64 lowercase hex characters",
  "trace_identity_sha256": "64 lowercase hex characters",
  "trace_sha256": "64 lowercase hex characters"
}
```

`family_identity_sha256` must hash the trace-determining config after removing only `demand.offered_mbps` and non-scientific output paths. It retains seed, master load, temporal model, population asset, geometry-independent trace fields, packet size, emission window, and sampler settings.

Extend the compile-time artifact guard from `trace.csv` and `manifest.json` to `nested-family.json`: reject a symlink, directory, device, or other non-regular pre-existing target before writing. A failed compile must not leave a companion that appears valid.

The verifier compares multisets of canonical rows excluding packet ID:

```python
def canonical_row(row: dict) -> tuple:
    return (
        row["emit_time_s"],
        row["src_grid_id"],
        row["dst_grid_id"],
        row["bits"],
        row["deadline_at_s"],
    )

def is_multiset_subset(child_rows: list[dict], parent_rows: list[dict]) -> bool:
    from collections import Counter
    child = Counter(canonical_row(row) for row in child_rows)
    parent = Counter(canonical_row(row) for row in parent_rows)
    return all(count <= parent[item] for item, count in child.items())
```

- [ ] RED: 10 < 20 < 40 < 80 Mbps children from an 80 Mbps master are strict multiset subsets for a non-degenerate fixture.
- [ ] RED: all children share one family identity but have distinct trace identities and trace hashes.
- [ ] RED: changing seed, UTC block, population SHA, packet size, emission window, master load, or sampler breaks family identity.
- [ ] RED: changing routing, access slots, ISL bandwidth, learning, geometry epoch, or output path does not alter trace family identity.
- [ ] RED: non-contiguous child IDs, non-sequential IDs, a row not in the parent, a duplicate beyond parent multiplicity, or a tampered companion hash fails.
- [ ] RED: master candidates over `execution.max_packets` fail before any trace artifact is accepted.
- [ ] RED: appending `nested_filter` leaves the generated values and mapping indices of all seven existing streams unchanged; the filter differs from every existing stream and is recorded as child 7.
- [ ] Run:

```bash
python3 -m pytest CODE/leo_sim/tests/test_trace_family.py CODE/leo_sim/tests/test_trace.py -q
```

- [ ] Commit: `feat: verify strict nested global load families`.

### Task 7: Add a pure layered scene classifier

**Files:**

- Create: `CODE/leo_sim/scene_check.py`
- Create: `CODE/leo_sim/tests/test_scene_check.py`
- Reuse: `CODE/leo_sim/metrics.py`, `CODE/leo_sim/receipt.py`

`scene_check.py` is read-only. It must not run a simulation, modify a receipt, or grant research eligibility. It accepts a versioned decision contract, coverage report, trace directory, and verified run directory; it recomputes its outputs from those artifacts.

Decision contract v1:

```yaml
schema: leo-sim-scene-decision/v1
scope: global_populated_land
population:
  source_sha256: c5742d16fc01d454e8ac5c5345a7e7716883acd28ac4d0d34c24613bc315e59a
  aggregation_deg: 1.0
  candidate_regions: 16988
coverage:
  horizon_s: 86400
  step_s: 10
  require_never_visible: 0
traffic:
  provenance: population_proxy
  temporal_model: local_diurnal_cosine
  require_isl_exposed_packets: 100
access_clean:
  min_admission_rate: 0.99
  max_access_rejected_fraction_of_offered: 0.001
  max_uplink_queue_overflow_fraction_of_offered: 0.001
route_clean:
  max_no_route_fraction_of_admitted: 0.001
  max_route_stalled_fraction_of_admitted: 0.001
downlink_clean:
  max_downlink_queue_overflow_fraction_of_admitted: 0.001
isl_pressure:
  window_s: 1.0
  min_consecutive_windows_same_directed_link: 3
  min_window_utilization: 0.70
  require_positive_p95_queue_delay_same_link: true
observation:
  emission_end_s: 20
  observation_end_s: 30
```

These are operational decision thresholds, not physical constants. They may be revised only in a separate reviewed contract change before compiling the calibration menu, never after viewing the candidate results.

Fractions are compared at full precision with no rounding or continuity correction. With a denominator below 1,000, a `0.001` maximum therefore means zero tolerated packets; that is intentional fail-closed behaviour, but the roughly hundred-packet local smoke is too small to validate or tune these thresholds.

Every fraction has one closed denominator. `offered` is the immutable trace row count; `admitted` is the independently recomputed count of unique `satellite_ingress` packets. `ACCESS_REJECTED` is always pre-ingress. The current kernel unfortunately uses `ACCESS_QUEUE_OVERFLOW` for both source uplink and destination downlink queues, so the checker must split that fate by the independently verified ingress event: no ingress means uplink/access overflow and ingress means downlink overflow. Any contradictory event/fate pair is `INVALID_EVIDENCE`.

The route numerator contains authoritative `NO_ROUTE` fates plus a separately reported `route_stalled_at_stop` count: admitted packets ending `IN_SYSTEM_AT_STOP` that entered a holding queue but never entered ISL or downlink service. Both use admitted packets as denominator. A zero admitted denominator stops at `ACCESS_LIMITED` and never evaluates routing. The checker emits every numerator, denominator, packet-ID set, and fraction; it does not rename an association grant as physical satellite ingress.

Classification order:

```python
if not integrity_ok:
    status = "INVALID_EVIDENCE"
elif not coverage_ok:
    status = "COVERAGE_INCOMPLETE"
elif not access_clean:
    status = "ACCESS_LIMITED"
elif not route_clean:
    status = "ROUTE_LIMITED"
elif not downlink_clean:
    status = "DOWNLINK_LIMITED"
elif isl_exposed_packets < require_isl_exposed_packets:
    status = "NO_ISL_EXPOSURE"
elif not isl_pressure:
    status = "NO_ISL_PRESSURE"
else:
    status = "ISL_PRESSURE_CANDIDATE"
```

ISL utilization must be recomputed per directed link and fixed time window:

```text
served ISL bits in window
---------------------------------
sampled available ISL capacity bits in the same window
```

The numerator is successfully served **data-packet** ISL bits from `link_service_windows`; the current ledger does not expose per-link/time control-packet service windows. Control packets share physical capacity, so the checker also reports run-level control occupancy/failures, but it must call the utilization result `data_plane_utilization` and treat it as a conservative lower bound on total physical utilization. It may not claim total-link utilization or compare runs with different control-plane settings under this contract.

An ISL-pressure candidate requires one specific directed `isl:<src>:<dst>` link to meet the utilization threshold in at least three adjacent, non-overlapping windows whose boundaries differ by exactly `window_s`, plus positive p95 ISL queue wait for packets queued on that same link during the same consecutive run. Three windows scattered across different links or separated in time do not pass. Report the qualifying link ID, exact windows, served bits, available-capacity bits, utilization, packet count, and queue-wait sample count.

Requirements:

- Available-capacity denominator is mandatory; missing exposure returns null plus a reason.
- Report `[0, T_emit]`, `[0, T_obs]`, and drain separately.
- `IN_SYSTEM_AT_STOP` is a fate, not congestion evidence.
- Access, holding, uplink, ISL, and downlink waits/overflows are separate fields.
- Pooled average utilization alone never passes L6.
- `scene_check.py` is the preformal single-run scene gate. It does not replace `CODE/experiment_platform/isl_pressure_decision.py`, which remains the later verified paired-arm decision step after canonical VM analysis.

- [ ] RED: every one of the eight single-run statuses above has a minimal counterexample fixture.
- [ ] RED: access failure plus high delivery loss returns `ACCESS_LIMITED`, never ISL pressure.
- [ ] RED: no-route failure returns `ROUTE_LIMITED` even if a surviving link is highly utilized.
- [ ] RED: admitted `IN_SYSTEM_AT_STOP` packets stalled in holding before any ISL exposure return `ROUTE_LIMITED`, not `NO_ISL_EXPOSURE`.
- [ ] RED: the same historical `ACCESS_QUEUE_OVERFLOW` fate is split by verified ingress: pre-ingress returns `ACCESS_LIMITED`, post-ingress returns `DOWNLINK_LIMITED`, and a contradictory ledger returns `INVALID_EVIDENCE`.
- [ ] RED: horizon-aggregate high utilization, three scattered windows, three windows on different directed links, or qualifying utilization with queue delay only on another link returns `NO_ISL_PRESSURE`.
- [ ] RED: `IN_SYSTEM_AT_STOP > 0` with no queue/utilization evidence returns `NO_ISL_PRESSURE`.
- [ ] RED: tampered trace, manifest, receipt, ledger, coverage source SHA, candidate count, window, or threshold contract returns `INVALID_EVIDENCE` or `COVERAGE_INCOMPLETE` as appropriate.
- [ ] Run:

```bash
python3 -m pytest CODE/leo_sim/tests/test_scene_check.py CODE/leo_sim/tests/test_congestion_metrics.py -q
```

- [ ] Commit: `feat: separate coverage access and ISL pressure gates`.

### Task 8: Add one diagnostic profile and prove the cheap path only

**Files:**

- Create: `CODE/leo_sim/profiles/population_global_1deg_diagnostic.yaml`
- Test: `CODE/leo_sim/tests/test_platform_check.py`
- Modify only if the existing population check cannot accept an explicit profile: `CODE/leo_sim/platform_check.py`

Profile contract:

```yaml
config_version: leo-sim-config/v1
scenario:
  name: population-global-1deg-diagnostic
  duration_s: 30
  time_step_s: 0.1
  num_satellites: 280
  num_planes: 14
  altitude_km: 600
  inclination_deg: 98.6
  min_elevation_deg: 25
  geometry_epoch_s: 0
  seed: 7
endpoints:
  grid_deg: 0.25
  aggregation_deg: 1
demand:
  mode: population_gravity
  population_path: CODE/population_map/gpw_v4_population_count_rev11_2020_15_min.tif
  offered_mbps: 5
  nested_master_offered_mbps: 80
  emission_end_s: 20
  packet_bits: 1000000
  source_population_exponent: 1
  destination_population_exponent: 1
  gravity_alpha: 1.25
  gravity_d_floor_km: 100
  temporal_model: local_diurnal_cosine
  utc_start_hour: 0
  diurnal_amplitude: 0.5
  diurnal_phase_h: 12
  population_destination_sampler: alias_rejection
  destination_rejection_max_draws: 10000
access:
  unavailable_policy: queue
  slots_per_satellite: 4
  uplink_rate_mbps: 100
  downlink_rate_mbps: 100
  uplink_queue_bits: 64000000
  downlink_queue_bits: 64000000
  association: bbm
  hysteresis_deg: 0
  min_dwell_s: 0
  acquisition_delay_s: 0.1
links:
  rate_model: mcs
  ge_enabled: false
topology:
  recompute_interval_s: 1
  matching: markovian
control_plane:
  enabled: true
  advertise_interval_s: 1
  ttl_s: 10
  vis_k: 17
  packet_bits: 8000
routing:
  policy: hop
  max_hops: 64
learning:
  algorithm: none
execution:
  max_events: 20000000
  max_entities: 2000
  max_packets: 5000
  available_capacity_interval_s: 1
outputs:
  out_dir: leo_sim_out/population-global-1deg-diagnostic
  plotting: false
```

The 80 Mbps master is a deterministic trace-generation ceiling for the nested family. It is not a claim that 80 Mbps is realistic or congested.

- [ ] Compile the exact profile twice into two `/tmp` directories and assert byte-identical trace, manifest, and family companion files.
- [ ] Assert the manifest says 16,988 candidate regions and `population_proxy`; report the observed source, destination, and runtime endpoint counts separately.
- [ ] Run a trace-only microbenchmark for child loads 5/10/20/40/80 Mbps from the same master and verify strict nesting. Do not run five network simulations locally.
- [ ] Run exactly one local 5 Mbps engineering smoke to check entity/event cost. Required outcome: natural end, conservation, receipt verification, no silent sampler fallback, and resource measurements. A low delivery rate is not a pass criterion and must be classified by layer.
- [ ] Treat `ACCESS_LIMITED` as a plausible and non-bug result for this 30-second cost smoke: most candidate regions are inactive and sparse active endpoints may wait beyond the short horizon. The smoke cannot validate the 0.99 access threshold or the pressure scene; it validates only compilation, resource bounds, natural end, conservation, and evidence plumbing.
- [ ] If `max_entities=2000`, `max_events=20000000`, or 30-second wall time blocks this smoke, record the actual peak and failure. Change only the proven blocker in a separate commit with a regression; do not raise all limits together.
- [ ] Do not run 10/20/40/80 network arms, VM calibration, RL, or Q0 in this task.
- [ ] Run:

```bash
python3 -m pytest CODE/leo_sim/tests/test_platform_check.py CODE/leo_sim/tests/test_trace_family.py -q
```

- [ ] Commit: `exp: add bounded global population diagnostic profile`.

### Task 9: Full verification and independent review handoff

**Files:**

- Modify: `NOTES.md`
- Do not modify truth reports or mentor reports.

- [ ] Run the full CI command:

```bash
python3 scripts/check_document_governance.py --mode all
python3 -m pytest CODE/leo_sim/tests CODE/experiment_platform/tests CODE/tests -q
git diff --check
git status --short
```

- [ ] Run the legacy population trace SHA regression again.
- [ ] Re-run the 1-degree 600 s/60 s coverage smoke twice and compare output SHA.
- [ ] Re-run the 5/10/20/40/80 trace family compile and independent verifier.
- [ ] Record exact base SHA, final SHA, commit list, tests, benchmarks, smoke receipt path/hash, source raster SHA, candidate count, and every unresolved limitation in `NOTES.md`.
- [ ] Assert from `git diff --name-only` that no report, `.docx`, RL/Q0/learning file, experiment request, authorization, or result directory changed.
- [ ] Push the branch and open one PR with the exact evidence above.
- [ ] Request a cold review bound to the exact PR head SHA. The reviewer must specifically audit:

```text
1. scalar/vector coverage equivalence and memory bound;
2. legacy trace-byte compatibility;
3. alias-rejection distribution and fail-loud cap;
4. strict nested family semantics and exact-key artifacts;
5. geometry epoch call path through kernel;
6. access/route/ISL classification counterexamples;
7. claim boundary: population proxy, global populated land, diagnostic only.
```

**Stop condition:** DeepSeek Harness stops at `PR_READY_FOR_INDEPENDENT_REVIEW`. It does not merge. Codex remains responsible for reviewing the exact SHA and deciding whether a later precompiled VM pressure-calibration menu may be authorized.

## 4. Definition of done

This work package is done only when all are true:

- The full positive-population 1-degree universe is loaded as 16,988 candidate regions from the exact source asset.
- The coverage audit processes every one of those IDs exactly once and is scalar-equivalent on test fixtures.
- The demand trace has population support, opt-in local-time variation, scalable exact destinations, and explicit proxy labeling.
- Legacy profiles retain their old trace bytes when the new features are not selected.
- Load arms are strict deterministic subsets of a common master and an independent verifier rejects tampering.
- A pure scene checker cannot confuse access failure, no route, lack of ISL exposure, and ISL pressure.
- One bounded 5 Mbps engineering smoke closes the cheap path with receipt and resource evidence.
- All tests and document governance are green on an exact clean commit.
- An independent reviewer receives the exact PR head SHA.
- The two mentor reports remain untouched.

Not done by this package:

```text
full 24-hour coverage result (unless the measured resource gate permits it)
VM pressure-calibration menu
formal load bracket
multi-seed statistics
information ablation
RL comparison
new algorithm comparison
paper claim
mentor report update
```

The next authorized work package, after exact-SHA review, is to precompile a bounded nested load menu, run it through the canonical VM chain, and stop at the first honest classification among `ACCESS_LIMITED`, `ROUTE_LIMITED`, `NO_ISL_PRESSURE`, or `ISL_PRESSURE_CANDIDATE`. Only after that result is stable across predeclared phase/seed blocks should algorithm comparisons begin.
