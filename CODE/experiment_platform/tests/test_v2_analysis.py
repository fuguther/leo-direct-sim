"""Focused tests for the dedicated V2 result-to-analysis adapter."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from unittest import mock

import pytest

from CODE.experiment_platform import v2_analysis
from CODE.leo_sim import kernel, receipt, trace
from CODE.leo_sim.tests.helpers import StaticGeometry, cell, make_cfg, row


def _write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


def _run_fixture(root: Path, run_id: str, arm_id: str, pair: str) -> dict:
    cfg = make_cfg({"scenario": {"duration_s": 1.0, "num_satellites": 1,
                                  "num_planes": 1},
                    "endpoints": {"sites": [
                        {"name": "a", "lat": 0.0, "lon": 0.0},
                        {"name": "b", "lat": 0.0, "lon": 10.0},
                    ]}})
    a, b = cell(0.0, 0.0), cell(0.0, 10.0)
    geometry = StaticGeometry(1, visible=lambda *_: True)
    trace_dir = root / "trace" / run_id
    manifest = trace.compile_trace(cfg, str(trace_dir))
    trace_bytes = (trace_dir / "trace.csv").read_bytes()
    manifest["__trace_sha256"] = hashlib.sha256(trace_bytes).hexdigest()
    manifest["__sha256"] = hashlib.sha256(
        (trace_dir / "manifest.json").read_bytes()).hexdigest()
    rows = trace.load_trace(str(trace_dir / "trace.csv"),
                            horizon_s=cfg["config"]["scenario"]["duration_s"],
                            max_packets=cfg["config"]["execution"]["max_packets"])
    result = kernel.run_simulation(cfg, rows, geometry=geometry)
    out = root / "CODE" / "Results" / run_id
    out.mkdir(parents=True)
    receipt_payload = receipt.write_run(
        str(out), cfg, trace_bytes, manifest, result, rows)
    auth_sha = "a" * 64
    _write(out / "formal_run.json", {
        "schema": "leo-sim-formal-run/v1", "run_id": run_id,
        "launch_nonce": "b" * 32, "authorization_sha256": auth_sha,
        "config_sha256": receipt_payload["config_sha256"],
        "code_sha256": receipt_payload["code_sha256"],
        "receipt_sha256": hashlib.sha256(
            (out / "receipt.json").read_bytes()).hexdigest(),
        "natural_end": True, "conservation_ok": True,
    })
    _write(out / "governance_receipt.json", {
        "schema": "leo-sim-governance-receipt/v2", "research_eligible": True,
        "run_id": run_id, "verification_errors": [],
        "receipt_schema": receipt_payload["schema"],
        "resolved_config_sha256": v2_analysis.file_sha256(
            out / "resolved_config.json"),
        "trace_manifest_schema": manifest["schema"],
        "trace_identity_contract": receipt_payload["trace_identity_contract"],
        "trace_manifest_sha256": v2_analysis.file_sha256(out / "manifest.json"),
        "run_receipt_sha256": hashlib.sha256(
            (out / "receipt.json").read_bytes()).hexdigest(),
    })
    return {"run_id": run_id, "arm_id": arm_id, "pairing_key": pair,
            "config_sha256": receipt_payload["config_sha256"]}


def test_primary_metric_is_derived_from_v2_receipt_and_ledgers():
    receipt_payload = {"totals": {"delivered_bits": 10},
                       "fate_counts": {"DELIVERED": 1, "IN_SYSTEM_AT_STOP": 1}}
    ledgers = {"congestion_metrics": {
        "packets": {"1": {"e2e_s": 1.0, "total_queue_wait_s": 0.2,
                            "tx_s": 0.3, "prop_s": 0.4}},
        "links": {"isl:0:1": {"utilization": 0.5}},
    }}
    assert v2_analysis._metric_from_result(
        receipt_payload, ledgers, "delivery_rate") == 0.5
    assert v2_analysis._metric_from_result(
        receipt_payload, ledgers, "e2e_delay_mean_s") == 1.0
    assert v2_analysis._metric_from_result(
        receipt_payload, ledgers, "link_utilization_mean") == 0.5


def test_access_boundary_metrics_are_explicit_v2_metrics():
    receipt_payload = {"totals": {"delivered_bits": 10},
                       "fate_counts": {"DELIVERED": 1}}
    ledgers = {"congestion_metrics": {
        "schema": "leo-sim-congestion-metrics/v2",
        "offered_packets": 4,
        "admitted_at_satellite_ingress_packets": 2,
        "access_admission_rate": 0.5,
        "network_delivery_rate_by_horizon": 0.25,
        "packets": {}, "links": {}}}
    assert v2_analysis._metric_from_result(
        receipt_payload, ledgers, "access_admission_rate") == 0.5
    assert v2_analysis._metric_from_result(
        receipt_payload, ledgers,
        "network_delivery_rate_by_horizon") == 0.25


def test_planned_contrasts_scope_each_contrast_to_its_own_pairing_key():
    results = [
        {"pairing_key": "load-50", "arm_id": "low_control",
         "primary_metric": 0.40},
        {"pairing_key": "load-50", "arm_id": "low_copy",
         "primary_metric": 0.45},
        {"pairing_key": "load-100", "arm_id": "medium_control",
         "primary_metric": 0.50},
        {"pairing_key": "load-100", "arm_id": "medium_copy",
         "primary_metric": 0.55},
    ]
    contrasts = [
        {"name": "low_copy_minus_low_control", "left_arm": "low_copy",
         "right_arm": "low_control"},
        {"name": "medium_copy_minus_medium_control",
         "left_arm": "medium_copy", "right_arm": "medium_control"},
    ]
    output = v2_analysis._compute_planned_contrasts(
        results, contrasts, "delivery_rate")
    assert [item["n_pairs"] for item in output] == [1, 1]
    assert [item["mean_difference"] for item in output] == pytest.approx([0.05, 0.05])


def test_v2_analysis_binds_two_real_receipts_and_persisted_outputs(tmp_path):
    root = tmp_path
    rows = [
        _run_fixture(root, "EXP-V2-ANALYSIS-control-s1", "control", "pair-1"),
        _run_fixture(root, "EXP-V2-ANALYSIS-treatment-s1", "treatment", "pair-1"),
    ]
    experiment = root / "EXPERIMENTS" / "EXP-V2-ANALYSIS"
    experiment.mkdir(parents=True)
    cells = [{**row, "trace_seed": 1} for row in rows]
    _write(experiment / "request.json", {
        "experiment_id": "EXP-V2-ANALYSIS",
        "claim_boundary": {"can_claim": ["none"],
                            "cannot_claim": ["not independently reviewed"]},
    })
    _write(experiment / "run-manifest.json", {
        "schema": v2_analysis.MATRIX_SCHEMA,
        "experiment_id": "EXP-V2-ANALYSIS", "cells": cells,
    })
    _write(experiment / "analysis-request.json", {
        "schema": v2_analysis.ANALYSIS_SCHEMA,
        "experiment_id": "EXP-V2-ANALYSIS",
        "planned_run_ids": [row["run_id"] for row in rows],
        "analysis": {
            "analysis_id": "AN-V2-ANALYSIS", "primary_metric": "delivery_rate",
            "planned_contrasts": [{"name": "treatment_minus_control",
                                   "left_arm": "treatment", "right_arm": "control"}],
        },
    })
    auth = {
        "status": "AUTHORIZED", "experiment_id": "EXP-V2-ANALYSIS",
        "authorized_cells": rows,
    }
    auth_path = experiment / "authorization.json"
    _write(auth_path, auth)
    auth_sha = v2_analysis.file_sha256(auth_path)
    for row in rows:
        result_dir = root / "CODE" / "Results" / row["run_id"]
        formal_path = result_dir / "formal_run.json"
        formal = json.loads(formal_path.read_text(encoding="utf-8"))
        formal["authorization_sha256"] = auth_sha
        _write(formal_path, formal)
        governed_path = result_dir / "governance_receipt.json"
        governed = json.loads(governed_path.read_text(encoding="utf-8"))
        governed["authorization_sha256"] = auth_sha
        _write(governed_path, governed)
    with mock.patch.object(v2_analysis.authorize_experiment,
                           "verify_authorization", return_value=auth):
        manifest = v2_analysis.analyze(root, experiment, auth_path)
        out = root / "ANALYSIS" / "EXP-V2-ANALYSIS"
        v2_analysis.write_outputs(root, out, manifest)
        ok, errors = v2_analysis.verify_persisted_analysis(
            root, out / "analysis-manifest.json")
    assert ok, errors
    assert manifest["status"] == "VERIFIED"
    assert manifest["claim_status"] == "READY_FOR_INDEPENDENT_CLAIM_REVIEW"
    assert manifest["planned_contrasts"][0]["n_pairs"] == 1


def test_v2_analysis_rejects_governance_witness_contract_mismatch(tmp_path):
    root = tmp_path
    row = _run_fixture(root, "EXP-V2-ANALYSIS-witness-s1", "control", "pair-1")
    experiment = root / "EXPERIMENTS" / "EXP-V2-ANALYSIS-WITNESS"
    experiment.mkdir(parents=True)
    row = {**row, "trace_seed": 1}
    _write(experiment / "request.json", {
        "experiment_id": experiment.name,
        "claim_boundary": {"can_claim": [], "cannot_claim": []},
    })
    _write(experiment / "run-manifest.json", {
        "schema": v2_analysis.MATRIX_SCHEMA,
        "experiment_id": experiment.name, "cells": [row],
    })
    _write(experiment / "analysis-request.json", {
        "schema": v2_analysis.ANALYSIS_SCHEMA,
        "experiment_id": experiment.name,
        "planned_run_ids": [row["run_id"]],
        "analysis": {"analysis_id": "AN-WITNESS", "primary_metric": "delivery_rate",
                     "planned_contrasts": []},
    })
    auth = {"status": "AUTHORIZED", "experiment_id": experiment.name,
            "authorized_cells": [row]}
    auth_path = experiment / "authorization.json"
    _write(auth_path, auth)
    auth_sha = v2_analysis.file_sha256(auth_path)
    result_dir = root / "CODE" / "Results" / row["run_id"]
    formal_path = result_dir / "formal_run.json"
    formal = json.loads(formal_path.read_text(encoding="utf-8"))
    formal["authorization_sha256"] = auth_sha
    _write(formal_path, formal)
    governed_path = result_dir / "governance_receipt.json"
    governed = json.loads(governed_path.read_text(encoding="utf-8"))
    governed["authorization_sha256"] = auth_sha
    governed["trace_manifest_schema"] = "leo-sim-trace-manifest/v1"
    _write(governed_path, governed)
    with mock.patch.object(v2_analysis.authorize_experiment,
                           "verify_authorization", return_value=auth):
        with pytest.raises(v2_analysis.V2AnalysisError, match="witness"):
            v2_analysis.analyze(root, experiment, auth_path)
