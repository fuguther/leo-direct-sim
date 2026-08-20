"""Tests for CODE.leo_sim.rng and CODE.leo_sim.trace."""
import csv
import hashlib
import json
from pathlib import Path

import pytest

from CODE.leo_sim import config, population, rng, trace


POPULATION_TIFF = (Path(__file__).resolve().parents[2] / "population_map"
                   / "gpw_v4_population_count_rev11_2020_15_min.tif")


def _cfg(**over):
    sites = [
        {"name": "a", "lat": 31.23, "lon": 121.47, "demand_weight": 2.0},
        {"name": "b", "lat": 40.0, "lon": 116.0},
        {"name": "c", "lat": 51.5, "lon": 0.1},
    ]
    user = {
        "endpoints": {"sites": sites},
        "scenario": {"duration_s": 5.0, "seed": 7},
        "demand": {"offered_mbps": 2.0, "packet_bits": 1_000_000},
    }
    user.update(over)
    return config.resolve_config(user)


def test_rng_streams_independent_and_deterministic():
    s1 = rng.streams(42)
    s2 = rng.streams(42)
    for name in rng.STREAM_NAMES:
        assert s1[name].random() == s2[name].random()
    # different stream names produce different sequences
    a = rng.streams(42)["demand"].random(5)
    b = rng.streams(42)["ge_isl"].random(5)
    assert not (a == b).all()


def test_compile_trace_byte_reproducible(tmp_path):
    cfg = _cfg()
    m1 = trace.compile_trace(cfg, str(tmp_path / "t1"))
    m2 = trace.compile_trace(cfg, str(tmp_path / "t2"))
    h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    assert h(tmp_path / "t1" / "trace.csv") == h(tmp_path / "t2" / "trace.csv")
    assert h(tmp_path / "t1" / "manifest.json") == h(tmp_path / "t2" / "manifest.json")
    assert m1["schema"] == trace.TRACE_MANIFEST_SCHEMA
    assert m1["trace_identity_sha256"] == config.trace_identity_sha256(cfg)
    assert m1["offered_packets"] == m1["ledger"]["packets"]
    assert m1["offered_bits"] == m1["ledger"]["bits"]
    contract = m1["provenance_contract"]
    assert contract["schema"] == "leo-sim-trace-provenance/v1"
    assert contract["source"] == {
        "type": "synthetic_generator", "path": None, "sha256": ""
    }
    assert contract["units"]["emit_time"] == "seconds_since_run_start"
    assert contract["units"]["bits"] == "bits"
    assert contract["offered_load"]["offered_bits"] == m1["offered_bits"]
    assert contract["offered_load"]["offered_packets"] == m1["offered_packets"]
    assert m1["active_endpoints"] == 3
    assert m1["time_range_s"][0] >= 0.0
    assert m1["time_range_s"][1] <= 5.0


def test_trace_columns_and_sorted(tmp_path):
    cfg = _cfg()
    trace.compile_trace(cfg, str(tmp_path / "t"))
    with open(tmp_path / "t" / "trace.csv") as fh:
        rows = list(csv.DictReader(fh))
    assert rows, "trace should not be empty"
    times = [float(r["emit_time_s"]) for r in rows]
    assert times == sorted(times)
    for r in rows:
        assert r["src_grid_id"] != r["dst_grid_id"]
        assert int(r["bits"]) > 0


def test_trace_csv_mode(tmp_path):
    src_csv = tmp_path / "in.csv"
    src_csv.write_text(
        "packet_id,emit_time_s,src_lat,src_lon,dst_lat,dst_lon,bits,deadline_at_s\n"
        "1,0.1,31.0,121.0,40.0,116.0,8000000,3.5\n"
        "2,0.2,31.0,121.0,51.5,0.1,8000000,\n"
    )
    cfg = _cfg()
    cfg["config"]["demand"]["mode"] = "csv"
    cfg["config"]["demand"]["csv_path"] = str(src_csv)
    m = trace.compile_trace(cfg, str(tmp_path / "t"))
    assert m["offered_packets"] == 2
    contract = m["provenance_contract"]
    assert contract["source"]["type"] == "csv_input"
    assert contract["source"]["sha256"] == hashlib.sha256(src_csv.read_bytes()).hexdigest()
    assert contract["od_mapping"]["input_coordinate_fields"] == [
        "src_lat", "src_lon", "dst_lat", "dst_lon"
    ]
    assert contract["offered_load"]["load_mode"] == "observed_trace"
    with open(tmp_path / "t" / "trace.csv") as fh:
        rows = list(csv.DictReader(fh))
    assert rows[0]["deadline_at_s"] == "3.5"
    assert rows[1]["deadline_at_s"] == ""


def test_trace_csv_mode_preserves_zero_deadline(tmp_path):
    """R5-G1 regression: deadline_at_s='0' is a valid instant deadline and
    must not be treated as 'no deadline' by a falsy-string check."""
    src_csv = tmp_path / "in.csv"
    src_csv.write_text(
        "packet_id,emit_time_s,src_lat,src_lon,dst_lat,dst_lon,bits,deadline_at_s\n"
        "1,0.0,31.0,121.0,40.0,116.0,8000000,0\n"
        "2,0.1,31.0,121.0,40.0,116.0,8000000,\n"
    )
    cfg = _cfg()
    cfg["config"]["demand"]["mode"] = "csv"
    cfg["config"]["demand"]["csv_path"] = str(src_csv)
    m = trace.compile_trace(cfg, str(tmp_path / "t"))
    assert m["offered_packets"] == 2
    with open(tmp_path / "t" / "trace.csv") as fh:
        rows = list(csv.DictReader(fh))
    assert rows[0]["deadline_at_s"] == "0"
    assert rows[1]["deadline_at_s"] == ""


def test_mlab_adapter_labels_measurement_proxy(tmp_path):
    # Sites sit on a real measured OD pair of the repository M-Lab snapshot
    # (Amagasaki <-> Tokyo). Sites without measurement coverage now fail
    # closed (round-4 contract); the previous Shanghai/Beijing/London trio has
    # no OD coverage in the snapshot and only ever worked through the removed
    # 1e-9 uniform-smoothing fallback.
    cfg = _cfg(**{"endpoints": {"sites": [
        {"name": "a", "lat": 34.717, "lon": 135.418, "demand_weight": 2.0},
        {"name": "b", "lat": 35.553, "lon": 139.781},
    ]}})
    cfg["config"]["demand"]["mode"] = "mlab"
    m = trace.compile_trace(cfg, str(tmp_path / "t"))
    assert m["provenance"] == "measurement_proxy"
    assert m["not_calibrated_user_demand"] is True
    assert "never calibrated user demand" in m["provenance_note"]
    assert m["offered_packets"] > 0


def test_demand_modes_all_generate(tmp_path):
    for mode in ("uniform", "gravity", "hotspot", "burst", "diurnal"):
        over = {"demand": {"mode": mode, "offered_mbps": 5.0, "packet_bits": 100_000}}
        if mode == "burst":
            over["demand"]["burst_start_s"] = 1.0
            over["demand"]["burst_duration_s"] = 2.0
        cfg = _cfg(**over)
        m = trace.compile_trace(cfg, str(tmp_path / mode))
        assert m["offered_packets"] > 0, mode
        assert m["provenance"] == "synthetic"
        transform = m["provenance_contract"]["traffic_transform"]
        assert transform["mode"] == mode
        if mode == "burst":
            assert transform["burst"] == {
                "start_s": 1.0, "duration_s": 2.0, "multiplier": 2.0
            }


def test_population_gravity_uses_population_for_sources_and_destinations(
        tmp_path, monkeypatch):
    regions = (
        population.PopulationRegion("G5:18:36", 2.5, 2.5, 100.0),
        population.PopulationRegion("G5:18:37", 2.5, 7.5, 10.0),
        population.PopulationRegion("G5:18:38", 2.5, 12.5, 1.0),
    )
    table = population.PopulationTable(
        regions=regions, source_path="/fake/pop.tif", source_sha256="a" * 64,
        source_shape=(720, 1440), source_resolution_deg=(0.25, 0.25),
        aggregation_deg=5.0, total_population=111.0)
    monkeypatch.setattr(population, "load_population_regions",
                        lambda path, aggregation_deg: table)
    cfg = config.resolve_config({
        "scenario": {"duration_s": 100.0, "seed": 11},
        "endpoints": {"aggregation_deg": 5.0},
        "demand": {
            "mode": "population_gravity", "population_path": "/fake/pop.tif",
            "offered_mbps": 100.0, "packet_bits": 1_000_000,
            "source_population_exponent": 1.0,
            "destination_population_exponent": 1.0,
            "gravity_alpha": 1.0, "gravity_d_floor_km": 100.0,
        },
        "execution": {"max_packets": 20_000},
    })
    manifest = trace.compile_trace(cfg, str(tmp_path / "population"))
    rows = trace.load_trace(
        str(tmp_path / "population" / "trace.csv"),
        horizon_s=100.0, max_packets=20_000)
    source_counts = {region.grid_id: 0 for region in regions}
    for row in rows:
        source_counts[row["src_grid_id"]] += 1
    assert source_counts[regions[0].grid_id] > source_counts[regions[1].grid_id]
    assert source_counts[regions[1].grid_id] > source_counts[regions[2].grid_id]
    from_first = [r["dst_grid_id"] for r in rows
                  if r["src_grid_id"] == regions[0].grid_id]
    assert set(from_first) == {regions[1].grid_id, regions[2].grid_id}
    assert from_first.count(regions[1].grid_id) > from_first.count(regions[2].grid_id)
    assert manifest["provenance"] == "population_proxy"
    assert manifest["input_sha256"] == "a" * 64
    assert manifest["not_calibrated_user_demand"] is True


def test_population_gravity_trace_is_byte_reproducible(tmp_path, monkeypatch):
    regions = (
        population.PopulationRegion("G5:18:36", 2.5, 2.5, 2.0),
        population.PopulationRegion("G5:18:37", 2.5, 7.5, 1.0),
    )
    table = population.PopulationTable(
        regions=regions, source_path="/fake/pop.tif", source_sha256="b" * 64,
        source_shape=(720, 1440), source_resolution_deg=(0.25, 0.25),
        aggregation_deg=5.0, total_population=3.0)
    monkeypatch.setattr(population, "load_population_regions",
                        lambda path, aggregation_deg: table)
    cfg = config.resolve_config({
        "scenario": {"duration_s": 5.0, "seed": 3},
        "endpoints": {"aggregation_deg": 5.0},
        "demand": {"mode": "population_gravity",
                   "population_path": "/fake/pop.tif"},
    })
    m1 = trace.compile_trace(cfg, str(tmp_path / "one"))
    m2 = trace.compile_trace(cfg, str(tmp_path / "two"))
    assert (tmp_path / "one" / "trace.csv").read_bytes() == (
        tmp_path / "two" / "trace.csv").read_bytes()
    assert m1["trace_identity_sha256"] == m2["trace_identity_sha256"]
