"""Formal governance gate tests (remote_job.v2_governance_errors)."""
import sys
import json
from pathlib import Path

import pytest

# remote_job.py imports its sibling modules as top-level names (VM layout)
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "remote"))

from CODE.scripts.remote import remote_job


def _base_receipt():
    return {
        "mechanisms": {"requested": {}, "effective": {}},
        "fate_counts": {"DELIVERED": 1},
        "control": {"counters": {"arrived": 1}},
    }


def test_require_data_isl_uses_recomputed_multisat_not_diagnostic_occupied():
    """The formal gate must not rest on the diagnostic occupied field: a
    delivery path spanning >=2 satellites proves real data ISL service."""
    # occupied claims ISL service but no multi-sat delivery exists -> gate
    # must fail even though the (diagnostic) field is positive
    receipt = _base_receipt()
    ledgers = {"deliveries": {"1": {"path": [0]}},
               "occupied": {"isl_s": 999.0}}
    errors = remote_job.v2_governance_errors(
        receipt, ledgers, {"require_data_isl": True}, [])
    assert any("data ISL" in e for e in errors)
    # real multi-sat delivery satisfies the gate even if occupied is zero
    ledgers = {"deliveries": {"1": {"path": [0, 1]}},
               "occupied": {"isl_s": 0.0}}
    errors = remote_job.v2_governance_errors(
        receipt, ledgers, {"require_data_isl": True}, [])
    assert not any("data ISL" in e for e in errors)


def test_v2_governance_receipt_binds_raw_config_and_trace_contract(tmp_path):
    receipt_path = tmp_path / "receipt.json"
    config_path = tmp_path / "resolved_config.json"
    manifest_path = tmp_path / "manifest.json"
    receipt = {"schema": "leo-sim-receipt/v5",
               "trace_identity_contract": "leo-sim-trace-identity/v2",
               "natural_end": True, "conservation_ok": True}
    ledgers = {}
    receipt_path.write_text(json.dumps(receipt) + "\n", encoding="utf-8")
    config_path.write_text('{"config": {"scenario": {}}}\n', encoding="utf-8")
    manifest_path.write_text(json.dumps({"schema": "leo-sim-trace-manifest/v2"}) + "\n",
                              encoding="utf-8")
    deployment = {"source_git_commit": "c" * 40,
                  "source_tree_sha256": "d" * 64}
    governed = remote_job.build_v2_governance_receipt(
        receipt=receipt, ledgers=ledgers, verification_errors=[], acceptance={},
        run_id="run-1", launch_nonce="a" * 32, authorization_sha256="b" * 64,
        deployment=deployment, deployment_receipt_sha256="e" * 64,
        execution_chain_sha256="f" * 64, receipt_path=receipt_path,
        resolved_config_path=config_path, manifest_path=manifest_path)
    assert governed["schema"] == "leo-sim-governance-receipt/v2"
    assert governed["receipt_schema"] == receipt["schema"]
    assert governed["trace_manifest_schema"] == "leo-sim-trace-manifest/v2"
    assert governed["trace_identity_contract"] == receipt["trace_identity_contract"]
    assert len(governed["resolved_config_sha256"]) == 64
    assert len(governed["trace_manifest_sha256"]) == 64
