"""CI collection bridge for the canonical analysis and claim tests.

The existing workflow collects ``CODE/tests``.  These imports intentionally
re-export the single source tests without copying fixtures or assertions.
"""

from ANALYSIS.tests.test_paired_analysis import (
    test_artifact_identity_mismatch_is_blocked,
    test_authorization_or_binding_bypass_is_blocked,
    test_complete_hash_verified_pairs_are_analyzed,
    test_entry_symlink_is_blocked,
    test_every_preregistered_pairing_key_requires_both_contrast_arms,
    test_existing_output_is_not_overwritten,
    test_hash_drift_is_fail_closed,
    test_incomplete_cohort_and_duplicate_run_are_rejected,
    test_missing_artifact_is_blocked,
    test_non_natural_and_bad_receipt_are_blocked,
    test_persisted_semantics_and_field_set_are_fail_closed,
)
from PAPER.tests.test_eligible_claims import VerifiedAnalysisEvidenceTests


__all__ = [
    "VerifiedAnalysisEvidenceTests",
    "test_artifact_identity_mismatch_is_blocked",
    "test_authorization_or_binding_bypass_is_blocked",
    "test_complete_hash_verified_pairs_are_analyzed",
    "test_entry_symlink_is_blocked",
    "test_every_preregistered_pairing_key_requires_both_contrast_arms",
    "test_existing_output_is_not_overwritten",
    "test_hash_drift_is_fail_closed",
    "test_incomplete_cohort_and_duplicate_run_are_rejected",
    "test_missing_artifact_is_blocked",
    "test_non_natural_and_bad_receipt_are_blocked",
    "test_persisted_semantics_and_field_set_are_fail_closed",
]
