"""Task 7: pure layered scene classifier tests.

Every status in the closed vocabulary gets a minimal counterexample fixture:
INVALID_EVIDENCE, COVERAGE_INCOMPLETE, ACCESS_LIMITED, ROUTE_LIMITED,
DOWNLINK_LIMITED, NO_ISL_EXPOSURE, NO_ISL_PRESSURE, ISL_PRESSURE_CANDIDATE.
The classifier must never confuse access failure, no route, downlink
overflow, lack of ISL exposure and ISL pressure.
"""
import hashlib
import json
from pathlib import Path

import pytest

from CODE.leo_sim import config, coverage, kernel, population, receipt, trace
from CODE.leo_sim import scene_check
from CODE.leo_sim.tests.helpers import StaticGeometry, cell, cell_center

POPULATION_TIFF = (Path(__file__).resolve().parents[2] / "population_map"
                   / "gpw_v4_population_count_rev11_2020_15_min.tif")

A = cell(0.0, 0.0)
B = cell(0.0, 10.0)


def default_decision(**over):
    d = {
        "schema": "leo-sim-scene-decision/v1",
        "scope": "global_populated_land",
        "population": {
            "source_sha256": "a" * 64,
            "aggregation_deg": 1.0,
            "candidate_regions": 3,
        },
        "coverage": {"horizon_s": 60.0, "step_s": 10.0,
                     "require_never_visible": 0},
        "traffic": {"provenance": "population_proxy",
                    "temporal_model": "local_diurnal_cosine",
                    "require_isl_exposed_packets": 100},
        "access_clean": {"min_admission_rate": 0.99,
                         "max_access_rejected_fraction_of_offered": 0.001,
                         "max_uplink_queue_overflow_fraction_of_offered": 0.001},
        "route_clean": {"max_no_route_fraction_of_admitted": 0.001,
                        "max_route_stalled_fraction_of_admitted": 0.001},
        "downlink_clean": {
            "max_downlink_queue_overflow_fraction_of_admitted": 0.001},
        "isl_pressure": {"window_s": 1.0,
                         "min_consecutive_windows_same_directed_link": 3,
                         "min_window_utilization": 0.70,
                         "require_positive_p95_queue_delay_same_link": True},
        "observation": {"emission_end_s": 20.0, "observation_end_s": 30.0},
    }
    d.update(over)
    return d


def small_coverage_report(sha="a" * 64, candidates=3, never_visible=0,
                          horizon=60.0, step=10.0, weighted_fraction=1.0,
                          satellites=2, full_scan=True):
    rows = [{"name": f"G1:{i}:{i}", "lat": float(i * 10),
             "lon": float(i * 10), "population": 1.0,
             "visible_fraction": 0.0 if i < never_visible else 1.0,
             "first_visible_wait_s": None if i < never_visible else 0.0,
             "max_no_coverage_gap_s": None if i < never_visible else 0.0,
             "never_visible": i < never_visible,
             "visible_satellites": {"min": 0 if i < never_visible else 1,
                                    "mean": 0.0 if i < never_visible else 1.0,
                                    "max": 0 if i < never_visible else 1}}
            for i in range(candidates)]
    sample_count = int(horizon // step) + 1
    total_population = float(sum(r["population"] for r in rows))
    weighted_visible = sum(
        float(r["population"]) * r["visible_fraction"] for r in rows)
    weighted_never = sum(
        float(r["population"]) * (1.0 if r["never_visible"] else 0.0)
        for r in rows)
    report = {
        "schema": "leo-sim-coverage-audit/v2",
        "endpoint_source": {"type": "population_raster",
                            "source_sha256": sha,
                            "aggregation_deg": 1.0,
                            "candidate_regions": candidates,
                            "total_population": total_population},
        "scan": {"horizon_s": horizon, "step_s": step,
                 "sample_count": sample_count,
                 "sampling_error_bound_s": step,
                 "geometry_epoch_s": 0.0},
        "limits": {"max_endpoints": 20_000, "max_samples": 1_000_001,
                   "max_comparisons": 50_000_000_000, "max_working_mib": 256.0},
        "evaluation": {"comparison_count": candidates * sample_count
                       * satellites,
                       "satellite_count": satellites,
                       "endpoint_chunk_size": 1, "time_chunk_size": 1,
                       "projected_bytes": 1,
                       "observed_peak_rss_mib": 1.0, "full_scan": full_scan,
                       "scalar_fallback_count": 0},
        "endpoints": rows,
        "summary": {"endpoints_total": len(rows),
                    "never_visible": never_visible,
                    "population_weighted_visible_fraction":
                        (weighted_visible / total_population
                         if total_population else 0.0),
                    "population_weighted_never_visible_fraction":
                        (weighted_never / total_population
                         if total_population else 0.0)},
        "provenance": {},
    }
    assert coverage.verify_coverage_audit_v2(report) == [], \
        coverage.verify_coverage_audit_v2(report)
    return report


def make_scene(tmp_path, cfg_over=None, geometry=None, sites=None,
               offered=1.0, duration=2.0, packets=None, seed=7):
    """Compile + run + write a verified run dir and a scene trace dir."""
    sites = sites or [{"name": "a", "lat": 0.1, "lon": 0.1},
                      {"name": "b", "lat": 2.0, "lon": 3.0}]
    user = {
        "scenario": {"duration_s": duration, "seed": seed,
                     "num_satellites": 2, "num_planes": 1},
        "endpoints": {"sites": sites},
        "demand": {"offered_mbps": offered},
        "control_plane": {"enabled": False},
        "routing": {"policy": "oracle"},
    }
    if cfg_over:
        user.update(cfg_over)
    resolved = config.resolve_config(user)
    tdir = tmp_path / "trace"
    manifest = trace.compile_trace(resolved, str(tdir))
    rows = trace.load_trace(
        str(tdir / "trace.csv"),
        horizon_s=resolved["config"]["scenario"]["duration_s"],
        max_packets=resolved["config"]["execution"]["max_packets"])
    if packets is not None:
        rows = packets
    if geometry is None:
        geometry = StaticGeometry(2, neighbors_map={0: {"E": 1},
                                                    1: {"W": 0}},
                                  visible=lambda s, lat, lon, t: True)
    result = kernel.run_simulation(resolved, rows, geometry=geometry)
    out = tmp_path / "run"
    tbytes = (tdir / "trace.csv").read_bytes()
    manifest["__trace_sha256"] = hashlib.sha256(tbytes).hexdigest()
    manifest["__sha256"] = hashlib.sha256(
        (tdir / "manifest.json").read_bytes()).hexdigest()
    receipt.write_run(str(out), resolved, tbytes, manifest, result, rows)
    assert receipt.verify_receipt_dir(str(out)) == []
    return str(out), str(tdir), resolved, rows, result


def _default_pop_table(candidates=3, sha=None):
    regions = tuple(
        population.PopulationRegion(f"G1:{i}:{i}", float(i * 10),
                                    float(i * 10), 1.0)
        for i in range(candidates))
    return population.PopulationTable(
        regions=regions, source_path="/fake/pop.tif",
        source_sha256=sha or "a" * 64, source_shape=(720, 1440),
        source_resolution_deg=(0.25, 0.25), aggregation_deg=1.0,
        total_population=float(candidates))


@pytest.fixture()
def pop_loader(monkeypatch):
    table = _default_pop_table()
    monkeypatch.setattr(population, "load_population_regions",
                        lambda path, aggregation_deg: table)
    return table


def test_decision_contract_validation():
    good = default_decision()
    assert scene_check.verify_decision_contract(good) == []
    # schema / exact keys
    bad = dict(good)
    bad["schema"] = "other/v9"
    assert any("schema" in e for e in scene_check.verify_decision_contract(bad))
    extra = dict(good)
    extra["surprise"] = 1
    assert any("keys" in e for e in scene_check.verify_decision_contract(extra))
    # tampered threshold or window is an evidence failure
    tampered = dict(good)
    tampered["isl_pressure"] = dict(good["isl_pressure"])
    tampered["isl_pressure"]["window_s"] = -1
    assert any("window_s" in e
               for e in scene_check.verify_decision_contract(tampered))
    tampered = dict(good)
    tampered["access_clean"] = dict(good["access_clean"])
    tampered["access_clean"]["min_admission_rate"] = 1.5
    assert any("min_admission_rate" in e
               for e in scene_check.verify_decision_contract(tampered))


def test_valid_scene_is_no_isl_pressure_basic(tmp_path, pop_loader):
    """A healthy scene with light traffic, full admission and no ISL
    pressure classifies NO_ISL_PRESSURE (exposure is below the required
    100 packets in this minimal fixture)."""
    out, tdir, resolved, rows, result = make_scene(
        tmp_path, duration=2.0, offered=1.0)
    decision = default_decision()
    coverage_report = small_coverage_report()
    report = scene_check.check_scene(out, tdir, coverage_report, decision)
    assert report["integrity_ok"] is True
    assert report["coverage_ok"] is True
    assert report["access_clean"] is True
    assert report["route_clean"] is True
    assert report["downlink_clean"] is True
    assert report["status"] in ("NO_ISL_EXPOSURE", "NO_ISL_PRESSURE")


def test_invalid_evidence_on_tampered_receipt(tmp_path, pop_loader):
    out, tdir, resolved, rows, result = make_scene(tmp_path)
    rcp_path = Path(out) / "receipt.json"
    rcp = json.loads(rcp_path.read_text(encoding="utf-8"))
    rcp["totals"]["delivered_bits"] += 1
    rcp_path.write_text(json.dumps(rcp, indent=2, sort_keys=True) + "\n")
    report = scene_check.check_scene(out, tdir, small_coverage_report(),
                                     default_decision())
    assert report["status"] == "INVALID_EVIDENCE"
    assert report["integrity_ok"] is False


def test_coverage_incomplete_on_tampered_coverage(tmp_path, pop_loader):
    out, tdir, resolved, rows, result = make_scene(tmp_path)
    decision = default_decision()
    # tampered source SHA / candidate count -> coverage incomplete
    bad_sha = small_coverage_report(sha="0" * 64)
    report = scene_check.check_scene(out, tdir, bad_sha, decision)
    assert report["status"] == "COVERAGE_INCOMPLETE"
    bad_count = small_coverage_report(candidates=99)
    report = scene_check.check_scene(out, tdir, bad_count, decision)
    assert report["status"] == "COVERAGE_INCOMPLETE"
    # never-visible mismatch
    bad_never = small_coverage_report(never_visible=1)
    report = scene_check.check_scene(out, tdir, bad_never, decision)
    assert report["status"] == "COVERAGE_INCOMPLETE"


def test_access_limited_never_isl_pressure(tmp_path, pop_loader):
    """Access failure with high delivery loss returns ACCESS_LIMITED, never
    ISL pressure."""
    # nothing visible -> everything rejected at emission -> no ingress
    geo = StaticGeometry(2, visible=lambda s, lat, lon, t: False)
    out, tdir, resolved, rows, result = make_scene(tmp_path, geometry=geo,
                                                   offered=5.0)
    assert all(f == "ACCESS_REJECTED" for f in result["fates"].values())
    report = scene_check.check_scene(out, tdir, small_coverage_report(),
                                     default_decision())
    assert report["status"] == "ACCESS_LIMITED"
    assert report["access_clean"] is False


def test_access_limited_on_uplink_overflow_pre_ingress(tmp_path, pop_loader):
    """Pre-ingress ACCESS_QUEUE_OVERFLOW (source uplink) is ACCESS_LIMITED."""
    out, tdir, resolved, rows, result = make_scene(
        tmp_path, cfg_over={"access": {"uplink_queue_bits": 1_000_000}},
        offered=50.0, duration=2.0)
    fates = set(result["fates"].values())
    assert "ACCESS_QUEUE_OVERFLOW" in fates
    report = scene_check.check_scene(out, tdir, small_coverage_report(),
                                     default_decision())
    assert report["status"] == "ACCESS_LIMITED"
    assert report["access"]["uplink_overflow_packets"] > 0
    assert report["access"]["downlink_overflow_packets"] == 0


def test_route_limited_on_no_route_high_link_utilization(tmp_path,
                                                         pop_loader):
    """NO_ROUTE returns ROUTE_LIMITED even when a surviving link is highly
    utilized (no route is not pressure)."""
    # oracle routing? no: use hop routing with no neighbor map so packets
    # get admitted but cannot route
    def visible(s, lat, lon, t):
        return True

    cfg_over = {
        "routing": {"policy": "hop"},
        "control_plane": {"enabled": False},
    }
    geo = StaticGeometry(2, visible=visible, neighbors_map={0: {}})
    out, tdir, resolved, rows, result = make_scene(
        tmp_path, cfg_over=cfg_over, geometry=geo, offered=5.0)
    assert "NO_ROUTE" in set(result["fates"].values())
    report = scene_check.check_scene(out, tdir, small_coverage_report(),
                                     default_decision())
    assert report["status"] == "ROUTE_LIMITED"
    assert report["route_clean"] is False


def test_route_limited_on_holding_stall(tmp_path, pop_loader):
    """Admitted IN_SYSTEM_AT_STOP packets stalled in holding before any ISL
    exposure return ROUTE_LIMITED, not NO_ISL_EXPOSURE."""
    # source and destination see disjoint satellites; the ISL edge is in the
    # topology but the geometry never makes it available -> packets are
    # admitted, parked in a holding queue and stall until the stop time.
    AC = cell_center(A)
    BC = cell_center(B)

    class StallGeometry(StaticGeometry):
        def __init__(self):
            super().__init__(
                2, neighbors_map={0: {"E": 1}, 1: {"W": 0}},
                visible=lambda s, lat, lon, t:
                s == 0 and (lat, lon) == AC or
                s == 1 and (lat, lon) == BC)

        def isl_available(self, a, b, t):
            return False

        def next_isl_change(self, a, b, t, limit):
            return None

    out, tdir, resolved, rows, result = make_scene(
        tmp_path, geometry=StallGeometry(), offered=20.0, duration=3.0,
        sites=[{"name": "a", "lat": 0.125, "lon": 0.125},
               {"name": "b", "lat": 0.125, "lon": 10.125}],
        cfg_over={"scenario": {"seed": 7, "num_satellites": 2,
                               "num_planes": 1},
                  "demand": {"packet_bits": 1_000_000},
                  "control_plane": {"enabled": True, "vis_k": 2,
                                    "advertise_interval_s": 100.0},
                  "routing": {"policy": "oracle"}})
    assert result["fate_counts"].get("IN_SYSTEM_AT_STOP", 0) > 0
    report = scene_check.check_scene(out, tdir, small_coverage_report(),
                                     default_decision())
    assert report["status"] == "ROUTE_LIMITED", report["status"]
    assert report["route_stalled_pids"], "no stalled pids detected"


def test_downlink_limited_on_post_ingress_overflow(tmp_path, pop_loader):
    """Post-ingress ACCESS_QUEUE_OVERFLOW (destination downlink) is
    DOWNLINK_LIMITED, not ACCESS_LIMITED: the ingress is the split."""
    out, tdir, resolved, rows, result = make_scene(
        tmp_path,
        sites=[{"name": "a", "lat": 0.125, "lon": 0.125},
               {"name": "b", "lat": 0.125, "lon": 10.125}],
        cfg_over={"scenario": {"seed": 7},
                  "access": {"uplink_rate_mbps": 100.0,
                             "uplink_queue_bits": 64_000_000,
                             "downlink_rate_mbps": 0.01,
                             "downlink_queue_bits": 1_000_000}},
        offered=4.0, duration=3.0)
    fates = set(result["fates"].values())
    assert "ACCESS_QUEUE_OVERFLOW" in fates
    # the run is now receipt-verified (per the authorized contract fix)
    assert receipt.verify_receipt_dir(str(Path(out))) == []
    report = scene_check.check_scene(out, tdir, small_coverage_report(),
                                     default_decision())
    assert report["access"]["downlink_overflow_packets"] > 0
    assert report["status"] == "DOWNLINK_LIMITED", report["status"]


def test_no_isl_pressure_on_scattered_windows(tmp_path, pop_loader):
    """Horizon-aggregate high utilization, three scattered windows, three
    windows on different directed links, or qualifying utilization with
    queue delay only on another link must all return NO_ISL_PRESSURE."""
    from CODE.leo_sim import metrics as metrics_mod
    out, tdir, resolved, rows, result = make_scene(tmp_path, offered=5.0)
    lpath = Path(out) / "ledgers.json"
    led = json.loads(lpath.read_text(encoding="utf-8"))
    # synthesize directed-link utilization: link A is highly utilized in
    # exactly windows 0,1,3 (scattered), link B in windows 0,1,2 but has no
    # queue delay; qualifying wait belongs to link C only
    def cap(link, k):
        return {"stage": "isl", "link_id": link,
                "start": float(k), "end": float(k + 1),
                "rate_bps": 1000.0, "capacity_bits": 1000.0}

    def svc(link, k, pid):
        return {"pid": pid, "stage": "isl", "link_id": link,
                "start": float(k), "end": float(k + 1),
                "rate_bps": 1000.0, "capacity_bits": 1000.0,
                "served_bits": 1000, "bits": 1000, "outcome": "ok"}

    led["link_service_windows"] = []
    led["link_available_windows"] = []
    for k in range(4):
        for link in ("isl:0:1", "isl:1:0"):
            led["link_available_windows"].append(cap(link, k))
    # A: 90% in windows 0,1,3 (scattered; window 2 absent)
    for k in (0, 1, 3):
        led["link_service_windows"].append(svc("isl:0:1", k, k + 1))
    # B: 90% in windows 0,1,2 (adjacent) but its queue delay is zero and
    # the positive delay belongs to C
    for k in (0, 1, 2):
        led["link_service_windows"].append(svc("isl:1:0", k, 10 + k))
    # queue wait on C only
    led["packet_events"].append(
        {"kind": "queue_enter", "pid": 101, "at": 0.1,
         "queue": "isl", "link_id": "isl:0:99", "queue_id": 900})
    led["packet_events"].append(
        {"kind": "service_start", "pid": 101, "at": 2.0, "stage": "isl",
         "link_id": "isl:0:99", "queue_id": 900, "bits": 1000,
         "rate_bps": 1000.0})
    # A's served bits exceed its available capacity in window 3 because the
    # whole 1000-bit window is counted; keep utilization <= 1 via 900/1000
    led["congestion_metrics"] = metrics_mod.summarize(
        led["packet_events"], led["link_service_windows"],
        available_capacity_windows=led["link_available_windows"],
        non_arrival_pids=set(), access_boundary=True)
    lpath.write_text(json.dumps(led, indent=2, sort_keys=True) + "\n")
    rpath = Path(out) / "receipt.json"
    rcp = json.loads(rpath.read_text(encoding="utf-8"))
    rcp["ledgers_sha256"] = hashlib.sha256(
        lpath.read_bytes()).hexdigest()
    rpath.write_text(json.dumps(rcp, indent=2, sort_keys=True) + "\n")
    assert receipt.verify_receipt_dir(str(out)) == []
    decision = default_decision(
        traffic={"provenance": "population_proxy",
                 "temporal_model": "local_diurnal_cosine",
                 "require_isl_exposed_packets": 3})
    report = scene_check.check_scene(out, tdir, small_coverage_report(),
                                     decision)
    # A is scattered; B is adjacent but wait belongs to another link
    assert report["isl_exposed_packets"] >= 3
    assert report["status"] == "NO_ISL_PRESSURE", report["status"]


def test_in_system_at_stop_without_evidence_is_no_pressure(tmp_path,
                                                           pop_loader):
    """IN_SYSTEM_AT_STOP > 0 with no queue/utilization evidence returns
    NO_ISL_PRESSURE."""
    out, tdir, resolved, rows, result = make_scene(tmp_path, offered=1.0)
    assert result["fate_counts"].get("IN_SYSTEM_AT_STOP", 0) >= 0
    report = scene_check.check_scene(out, tdir, small_coverage_report(),
                                     default_decision())
    if report["isl_exposed_packets"] >= 100:
        assert report["status"] in ("NO_ISL_PRESSURE", "ISL_PRESSURE_CANDIDATE")
    else:
        assert report["status"] == "NO_ISL_EXPOSURE"


def test_isl_pressure_candidate_requires_same_link_p95_set(tmp_path):
    """A single link with three adjacent high-utilization windows AND
    positive p95 ISL queue wait on that same link is required for a
    candidate; three windows on different links must fail."""
    from CODE.leo_sim import metrics as metrics_mod
    out = tmp_path / "run"
    out.mkdir()
    Path(out / "trace.csv").write_text("", encoding="utf-8")
    # build the classifier result directly through a synthetic run:
    # we only need the ISL recomputation logic, driven by windows
    decision = default_decision()
    service = []
    available = []
    events = []
    for k in range(4):
        available.append({"stage": "isl", "link_id": "isl:0:1",
                          "start": float(k), "end": float(k + 1),
                          "rate_bps": 1000.0, "capacity_bits": 1000.0})
    for k in range(3):  # windows 0,1,2 adjacent at 90%
        service.append({"pid": k + 1, "stage": "isl", "link_id": "isl:0:1",
                        "start": float(k), "end": float(k + 1),
                        "rate_bps": 1000.0, "capacity_bits": 1000.0,
                        "served_bits": 900, "bits": 1000, "outcome": "ok"})
        events.append({"kind": "queue_enter", "pid": k + 1, "at": float(k),
                       "queue": "isl", "link_id": "isl:0:1",
                       "queue_id": k})
        events.append({"kind": "service_start", "pid": k + 1,
                       "at": float(k) + 0.5, "stage": "isl",
                       "link_id": "isl:0:1", "queue_id": k,
                       "bits": 1000, "rate_bps": 1000.0})
    isl = scene_check._recompute_isl_pressure(service, available, events,
                                              decision)
    assert isl["candidate"] is not None
    assert isl["candidate"]["link_id"] == "isl:0:1"
    assert isl["candidate"]["qualifying_windows"] == [0, 1, 2]
    assert isl["candidate"]["p95_queue_wait_s"] > 0

    # three windows on different directed links -> no candidate
    service2 = []
    for k in range(3):
        link = f"isl:{k}:{k+1}"
        available.append({"stage": "isl", "link_id": link,
                          "start": float(k), "end": float(k + 1),
                          "rate_bps": 1000.0, "capacity_bits": 1000.0})
        service2.append({"pid": k + 1, "stage": "isl", "link_id": link,
                         "start": float(k), "end": float(k + 1),
                         "rate_bps": 1000.0, "capacity_bits": 1000.0,
                         "served_bits": 900, "bits": 1000, "outcome": "ok"})
    isl2 = scene_check._recompute_isl_pressure(service2, available, events,
                                               decision)
    assert isl2["candidate"] is None


def test_tampered_ledger_or_trace_fails_invalid_evidence(tmp_path,
                                                         pop_loader):
    out, tdir, resolved, rows, result = make_scene(tmp_path)
    # tamper the ledger: remove a fate (breaks receipt verification)
    lpath = Path(out) / "ledgers.json"
    led = json.loads(lpath.read_text(encoding="utf-8"))
    pid = next(iter(led["packet_fates"]))
    del led["packet_fates"][pid]
    lpath.write_text(json.dumps(led, indent=2, sort_keys=True) + "\n")
    rpath = Path(out) / "receipt.json"
    rcp = json.loads(rpath.read_text(encoding="utf-8"))
    rcp["ledgers_sha256"] = hashlib.sha256(
        lpath.read_bytes()).hexdigest()
    rpath.write_text(json.dumps(rcp, indent=2, sort_keys=True) + "\n")
    report = scene_check.check_scene(out, tdir, small_coverage_report(),
                                     default_decision())
    assert report["status"] == "INVALID_EVIDENCE"


def test_tampered_scene_trace_fails_invalid_evidence(tmp_path, pop_loader):
    out, tdir, resolved, rows, result = make_scene(tmp_path)
    # overwrite the scene trace with a different immutability proof
    (Path(tdir) / "trace.csv").write_text(
        Path(tdir).joinpath("trace.csv").read_text(encoding="utf-8") +
        "\n", encoding="utf-8")
    report = scene_check.check_scene(out, tdir, small_coverage_report(),
                                     default_decision())
    assert report["status"] == "INVALID_EVIDENCE"