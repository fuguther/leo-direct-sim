"""CI bridge for canonical analysis and claim tests without double collection.

The hosted workflow targets ``CODE/tests`` and therefore does not discover the
canonical tests under ANALYSIS and PAPER.  This bridge inspects the tests that
pytest actually collected: unless both canonical source modules are already
present it runs both in one isolated subprocess; when both source modules are
in the current session it skips, so a full-suite run does not duplicate them.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
CANONICAL_TESTS = (
    "ANALYSIS/tests/test_paired_analysis.py",
    "PAPER/tests/test_eligible_claims.py",
)


def test_canonical_analysis_and_claim_contracts_for_code_ci_scope(
    request: pytest.FixtureRequest,
) -> None:
    canonical_paths = {(ROOT / relative).resolve() for relative in CANONICAL_TESTS}
    collected_paths = {Path(item.path).resolve() for item in request.session.items}
    if canonical_paths <= collected_paths:
        pytest.skip("canonical ANALYSIS/PAPER source tests already collected")

    completed = subprocess.run(
        [sys.executable, "-m", "pytest", *CANONICAL_TESTS, "-q"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
