"""CI bridge for canonical analysis and claim tests without double collection.

The hosted workflow explicitly targets ``CODE/tests`` and therefore would not
discover the canonical tests under ANALYSIS and PAPER.  In that explicit
scope this module runs those source modules in one isolated pytest subprocess.
For a no-target full-suite invocation, pytest discovers the source modules
itself and this bridge skips, so every test has one logical execution.
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


def _explicitly_targets_code_tests(argv: list[str]) -> bool:
    code_tests = ROOT / "CODE/tests"
    for raw in argv[1:]:
        if raw.startswith("-"):
            continue
        target = raw.split("::", 1)[0]
        try:
            candidate = Path(target).resolve()
            candidate.relative_to(code_tests)
            return True
        except ValueError:
            continue
    return False


@pytest.mark.skipif(
    not _explicitly_targets_code_tests(sys.argv),
    reason="no-target full pytest discovers ANALYSIS/PAPER source tests directly",
)
def test_canonical_analysis_and_claim_contracts_for_code_ci_scope() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", *CANONICAL_TESTS, "-q"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
