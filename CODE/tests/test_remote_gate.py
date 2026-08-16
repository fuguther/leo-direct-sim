"""Formal governance gate tests (remote_job.v2_governance_errors)."""
import sys
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
