"""Compatibility smoke for the canonical analysis fixture module.

The implementation tests live in ``ANALYSIS/tests/test_paired_analysis.py``;
this tracked path remains only to prove the historical CODE test import path
does not define a second fixture source.
"""

from ANALYSIS.tests.test_paired_analysis import PairedAnalysisTests


def test_paired_analysis_fixture_has_current_contract() -> None:
    assert "test_complete_hash_verified_pairs_are_analyzed" in dir(PairedAnalysisTests)
