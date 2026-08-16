"""Tests for the V2 governance integration surface."""
import json

import hashlib
import pytest

from CODE.leo_sim import config, governance
from CODE.experiment_platform import authorize_experiment
from CODE.work.finalize_decision import file_sha256


def test_valid_intent_seals_identities():
    sites = {"endpoints": {"sites": [
        {"name": "a", "lat": 0.0, "lon": 0.0},
        {"name": "b", "lat": 0.0, "lon": 10.0},
    ]}}
    intent = governance.build_run_intent({
        "runtime_kind": "leo_sim_v2",
        "config": {"scenario": {"duration_s": 5.0}, **sites},
    })
    assert intent["schema"] == governance.INTENT_SCHEMA
    assert len(intent["config_sha256"]) == 64
    assert len(intent["trace_identity_sha256"]) == 64
    assert len(intent["code_sha256"]) == 64
    # deterministic
    again = governance.build_run_intent({
        "runtime_kind": "leo_sim_v2",
        "config": {"scenario": {"duration_s": 5.0}, **sites},
    })
    assert intent["config_sha256"] == again["config_sha256"]
    chain = governance.execution_chain_sha256()
    assert set(chain) == set(governance.EXECUTION_CHAIN_PATHS)
    assert all(len(value) == 64 for value in chain.values())


def test_non_csv_intent_requires_two_sites():
    # csv supplies rows directly; other modes compile traffic from sites, so
    # an intent sealed without two sites would be green on ungenerable demand
    with pytest.raises(governance.IntentError, match="two endpoints.sites"):
        governance.build_run_intent({
            "runtime_kind": "leo_sim_v2",
            "config": {"scenario": {"duration_s": 5.0}},
        })
    with pytest.raises(governance.IntentError, match="two endpoints.sites"):
        governance.build_run_intent({
            "runtime_kind": "leo_sim_v2",
            "config": {"endpoints": {"sites": [
                {"name": "a", "lat": 0.0, "lon": 0.0}]}},
        })


def test_wrong_runtime_kind_rejected():
    with pytest.raises(governance.IntentError, match="runtime_kind"):
        governance.build_run_intent({"runtime_kind": "legacy_gateway", "config": {}})
    with pytest.raises(governance.IntentError):
        governance.build_run_intent({"config": {}})


def test_unknown_request_fields_rejected():
    with pytest.raises(governance.IntentError, match="unknown request fields"):
        governance.build_run_intent({
            "runtime_kind": "leo_sim_v2", "config": {}, "shell": "rm -rf /"})


def test_formal_csv_intent_uses_project_relative_input_on_each_host(tmp_path):
    demand = tmp_path / "EXPERIMENTS" / "inputs" / "demand.csv"
    demand.parent.mkdir(parents=True)
    demand.write_text("packet_id,emit_time_s\n1,0\n", encoding="utf-8")
    request = {
        "runtime_kind": "leo_sim_v2",
        "config": {"demand": {
            "mode": "csv",
            "csv_path": "EXPERIMENTS/inputs/demand.csv",
        }},
    }
    intent = governance.build_run_intent(request, project_root=tmp_path)
    assert intent["input_sha256"]
    assert intent["resolved"]["config"]["demand"]["csv_path"] == (
        "EXPERIMENTS/inputs/demand.csv")
    request["config"]["demand"]["csv_path"] = "../outside.csv"
    with pytest.raises(governance.IntentError, match="inside the project"):
        governance.build_run_intent(request, project_root=tmp_path)


def test_invalid_config_rejected():
    with pytest.raises(Exception):
        governance.build_run_intent({
            "runtime_kind": "leo_sim_v2",
            "config": {"access": {"uplink_rate_mbps": -1.0}},
        })


def test_compile_experiment_emits_reviewable_v2_artifacts(tmp_path):
    request = {
        "schema": governance.REQUEST_SCHEMA,
        "experiment_id": "EXP-LEO-V2-SMOKE",
        "runtime_kind": "leo_sim_v2",
        "work_finalization": "CODE/work/WP-SMOKE/R01/finalization.json",
        "acceptance": {"min_delivered_packets": 1,
                       "min_multisat_deliveries": 1,
                       "require_data_isl": True,
                       "require_control_delivery": True},
        "config": {
            "scenario": {"duration_s": 1.0, "num_satellites": 1,
                         "num_planes": 1, "seed": 9},
            "endpoints": {"sites": [
                {"name": "a", "lat": 0.0, "lon": 0.0},
                {"name": "b", "lat": 0.0, "lon": 10.0},
            ]},
            "control_plane": {"enabled": False},
            "routing": {"policy": "oracle"},
        },
    }
    request_path = tmp_path / "request-input.json"
    request_path.write_text(json.dumps(request), encoding="utf-8")
    out = tmp_path / "EXPERIMENTS" / request["experiment_id"]
    report = governance.compile_experiment(request_path, out, project_root=tmp_path)
    assert report["status"] == "COMPILED_REVIEW_REQUIRED"
    manifest = json.loads((out / "run-manifest.json").read_text())
    assert manifest["runtime_kind"] == "leo_sim_v2"
    assert manifest["execution_authorized"] is False
    assert manifest["planned_runs"][0]["runtime_kind"] == "leo_sim_v2"
    cfg_path = out / manifest["planned_runs"][0]["config_path"]
    resolved = config.load_config_file(str(cfg_path))
    assert resolved["sha256"] == manifest["planned_runs"][0]["config_sha256"]
    assert not any("Gateway" in p.read_text(encoding="utf-8")
                   for p in (out / "RUNBOOK.md",))


def test_compile_experiment_refuses_nonempty_or_symlink_output(tmp_path):
    request_path = tmp_path / "request.json"
    request_path.write_text(json.dumps({
        "schema": governance.REQUEST_SCHEMA,
        "experiment_id": "EXP-LEO-V2-SMOKE",
        "runtime_kind": "leo_sim_v2",
        "work_finalization": "CODE/work/WP-SMOKE/R01/finalization.json",
        "acceptance": {"min_delivered_packets": 0,
                       "min_multisat_deliveries": 0,
                       "require_data_isl": False,
                       "require_control_delivery": False},
        "config": {"scenario": {"duration_s": 1.0},
                   "endpoints": {"sites": [
                       {"name": "a", "lat": 0.0, "lon": 0.0},
                       {"name": "b", "lat": 0.0, "lon": 10.0},
                   ]}},
    }), encoding="utf-8")
    out = tmp_path / "out"
    out.mkdir()
    (out / "sentinel").write_text("keep", encoding="utf-8")
    with pytest.raises(governance.IntentError, match="empty"):
        governance.compile_experiment(request_path, out, project_root=tmp_path)


def test_authorization_rejects_rebound_request_that_no_longer_produced_config(
        tmp_path):
    request = {
        "schema": governance.REQUEST_SCHEMA,
        "experiment_id": "EXP-LEO-V2-REBIND",
        "runtime_kind": "leo_sim_v2",
        "work_finalization": "CODE/work/WP-REBIND/R01/finalization.json",
        "acceptance": {"min_delivered_packets": 0,
                       "min_multisat_deliveries": 0,
                       "require_data_isl": False,
                       "require_control_delivery": False},
        "config": {"scenario": {"duration_s": 1.0, "seed": 7},
                   "endpoints": {"sites": [
                       {"name": "a", "lat": 0.0, "lon": 0.0},
                       {"name": "b", "lat": 0.0, "lon": 10.0},
                   ]}},
    }
    request_path = tmp_path / "request-input.json"
    request_path.write_text(json.dumps(request), encoding="utf-8")
    out = tmp_path / "EXPERIMENTS" / request["experiment_id"]
    governance.compile_experiment(request_path, out, project_root=tmp_path)

    rebound = json.loads((out / "request.json").read_text())
    rebound["config"]["scenario"]["duration_s"] = 2.0
    (out / "request.json").write_text(
        json.dumps(rebound, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    request_sha = file_sha256(out / "request.json")
    manifest = json.loads((out / "run-manifest.json").read_text())
    manifest["request_sha256"] = request_sha
    (out / "run-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    analysis = json.loads((out / "analysis-request.json").read_text())
    analysis["request_sha256"] = request_sha
    analysis["run_manifest_sha256"] = file_sha256(out / "run-manifest.json")
    (out / "analysis-request.json").write_text(
        json.dumps(analysis, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = json.loads((out / "compile-report.json").read_text())
    report["request_sha256"] = request_sha
    report["artifact_hashes"] = {
        str(path.relative_to(out)): file_sha256(path)
        for path in sorted(out.rglob("*"))
        if path.is_file() and path.name != "compile-report.json"
    }
    (out / "compile-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    with pytest.raises(authorize_experiment.AuthorizationError,
                       match="does not derive from request"):
        authorize_experiment._verified_experiment(tmp_path, out)


def test_formal_population_gravity_intent_binds_input_sha(tmp_path):
    demand = tmp_path / "EXPERIMENTS" / "inputs" / "pop.tif"
    demand.parent.mkdir(parents=True)
    demand.write_bytes(b"fake-tiff-bytes-12345")
    request = {
        "runtime_kind": "leo_sim_v2",
        "config": {"endpoints": {"sites": [
            {"name": "a", "lat": 0.0, "lon": 0.0},
            {"name": "b", "lat": 0.0, "lon": 10.0},
        ]}, "demand": {
            "mode": "population_gravity",
            "population_path": "EXPERIMENTS/inputs/pop.tif",
        }},
    }
    intent = governance.build_run_intent(request, project_root=tmp_path)
    assert intent["input_sha256"] == hashlib.sha256(
        demand.read_bytes()).hexdigest()
    request["config"]["demand"]["population_path"] = "../outside.tif"
    with pytest.raises(governance.IntentError, match="inside the project"):
        governance.build_run_intent(request, project_root=tmp_path)
