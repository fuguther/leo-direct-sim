import copy
import json

import pytest

from CODE.experiment_platform import authorize_experiment
from CODE.leo_sim import matrix


def _request():
    return {
        "schema": matrix.MATRIX_REQUEST_SCHEMA,
        "experiment_id": "EXP-LEO-V2-MATRIX",
        "runtime_kind": "leo_sim_v2",
        "work_finalization": "CODE/work/WP-MATRIX/R01/finalization.json",
        "common_config": {
            "scenario": {"duration_s": 1.0, "num_satellites": 1,
                          "num_planes": 1},
            "endpoints": {"sites": [
                {"name": "a", "lat": 0.0, "lon": 0.0},
                {"name": "b", "lat": 0.0, "lon": 10.0},
            ]},
            "control_plane": {"enabled": False},
            "routing": {"policy": "oracle"},
        },
        "arms": [
            {"arm_id": "control", "config_overrides": {}},
            {"arm_id": "treatment", "config_overrides": {
                "demand": {"offered_mbps": 2.0},
            }},
        ],
        "cells": [
            {"run_id": "EXP-LEO-V2-MATRIX-control-s42", "arm_id": "control",
             "phase": "non_learning", "trace_seed": 42, "learning_seed": None,
             "pairing_key": "pair-42", "config_overrides": {},
             "checkpoint_lineage": {"mode": "not_applicable",
                                     "source_run_id": None, "source_sha256": None}},
            {"run_id": "EXP-LEO-V2-MATRIX-treatment-s42", "arm_id": "treatment",
             "phase": "non_learning", "trace_seed": 42, "learning_seed": None,
             "pairing_key": "pair-42", "config_overrides": {},
             "checkpoint_lineage": {"mode": "not_applicable",
                                     "source_run_id": None, "source_sha256": None}},
        ],
        "acceptance": {"min_delivered_packets": 0,
                       "min_multisat_deliveries": 0,
                       "require_data_isl": False,
                       "require_control_delivery": False},
        "analysis": {
            "analysis_id": "AN-LEO-V2-MATRIX",
            "primary_metric": "delivery_rate",
            "estimand": "paired difference",
            "paired_by": ["pairing_key"],
            "planned_contrasts": [{"name": "treatment_minus_control",
                                   "left_arm": "treatment",
                                   "right_arm": "control",
                                   "estimand": "paired difference"}],
        },
        "claim_boundary": {
            "can_claim": ["compiled matrix identity"],
            "cannot_claim": ["run completion", "algorithm effect"],
        },
    }


def test_compile_matrix_emits_one_bound_v2_config_and_runbook_command_per_cell(tmp_path):
    request = _request()
    source = tmp_path / "request.json"
    source.write_text(json.dumps(request), encoding="utf-8")
    out = tmp_path / "EXPERIMENTS" / request["experiment_id"]

    report = matrix.compile_matrix_experiment(source, out, project_root=tmp_path)

    assert report["status"] == "COMPILED_REVIEW_REQUIRED"
    manifest = json.loads((out / "run-manifest.json").read_text())
    assert manifest["schema"] == matrix.MATRIX_MANIFEST_SCHEMA
    assert [c["run_id"] for c in manifest["cells"]] == [
        "EXP-LEO-V2-MATRIX-control-s42", "EXP-LEO-V2-MATRIX-treatment-s42"]
    for cell in manifest["cells"]:
        assert cell["runtime_kind"] == "leo_sim_v2"
        assert len(cell["config_sha256"]) == 64
        assert len(cell["trace_identity_sha256"]) == 64
        assert len(cell["input_sha256"]) == 0
        assert len(cell["code_sha256"]) == 64
        assert all(len(v) == 64 for v in cell["execution_chain_sha256"].values())
        assert len(cell["controlled_signature"]) == 64
        config_path = out / cell["config_path"]
        assert config_path.name == f"{cell['run_id']}.leo-sim.yaml"
        assert config_path.is_file()
    analysis = json.loads((out / "analysis-request.json").read_text())
    assert analysis["schema"] == matrix.MATRIX_ANALYSIS_SCHEMA
    assert analysis["planned_run_ids"] == [c["run_id"] for c in manifest["cells"]]
    runbook = (out / "RUNBOOK.md").read_text(encoding="utf-8")
    assert runbook.count("CODE/scripts/remote/run-remote.sh") == len(manifest["cells"])
    assert "python3 CODE/scripts/remote/run-remote.sh" not in runbook


@pytest.mark.parametrize("mutation, message", [
    (lambda r: r.update(extra=True), "unknown request fields"),
    (lambda r: r["cells"].append(copy.deepcopy(r["cells"][0])), "duplicate run_id"),
    (lambda r: r["cells"][0].update(arm_id="missing"), "unknown arm_id"),
    (lambda r: r["cells"][0].update(run_id="wrong-id"), "run_id identity"),
])
def test_matrix_compiler_rejects_invalid_contract(mutation, message, tmp_path):
    request = _request()
    mutation(request)
    source = tmp_path / "request.json"
    source.write_text(json.dumps(request), encoding="utf-8")
    with pytest.raises(matrix.MatrixError, match=message):
        matrix.compile_matrix_experiment(source, tmp_path / "out", project_root=tmp_path)


def test_authorizer_verifies_matrix_cohort_as_one_atomic_set(tmp_path):
    request = _request()
    source = tmp_path / "request.json"
    source.write_text(json.dumps(request), encoding="utf-8")
    experiment = tmp_path / "EXPERIMENTS" / request["experiment_id"]
    matrix.compile_matrix_experiment(source, experiment, project_root=tmp_path)

    experiment_id, artifacts, authorized = authorize_experiment._verified_experiment(
        tmp_path, experiment)

    assert experiment_id == request["experiment_id"]
    assert len(authorized) == len(request["cells"])
    assert {row["run_id"] for row in authorized} == {
        cell["run_id"] for cell in request["cells"]}
    assert all(row["runtime_kind"] == "leo_sim_v2" for row in authorized)
    assert all(path.startswith(str(experiment.relative_to(tmp_path)))
               for path in artifacts)
