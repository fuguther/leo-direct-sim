import json
import tempfile
import unittest
from pathlib import Path

from CODE.experiment_platform.classify_legacy_results import (
    COLD,
    DELETE,
    KEEP,
    build_review,
    classify_asset,
    classify_run,
)


def run_record(
    *,
    path: str,
    completion: str = "NATURAL_END_LOG_CLUE",
    smoke: bool = False,
    grade: str = "E1_METADATA",
    resolved_config: bool = True,
    run_meta: bool = True,
    summary_metrics: bool = True,
) -> dict:
    return {
        "relative_path": path,
        "size_bytes": 100,
        "completion_signal": {"classification": completion},
        "smoke_clues": {"detected": smoke},
        "evidence_grade": grade,
        "key_artifacts_present": {
            "resolved_config": resolved_config,
            "run_meta": run_meta,
            "summary_metrics": summary_metrics,
        },
        "checkpoints": [],
    }


class LegacyCleanupClassificationTests(unittest.TestCase):
    def test_priority_keep_requires_complete_retrospective_clues(self) -> None:
        classification, reasons = classify_run(run_record(path="strong"))
        self.assertEqual(classification, KEEP)
        self.assertIn("SUMMARY_METRICS_PRESENT", reasons)

        classification, _ = classify_run(
            run_record(path="missing-summary", summary_metrics=False)
        )
        self.assertEqual(classification, COLD)

    def test_smoke_interrupted_and_minimal_are_review_only_delete_candidates(self) -> None:
        cases = (
            run_record(path="smoke", smoke=True),
            run_record(path="interrupted", completion="INTERRUPTED_REPORTED"),
            run_record(path="minimal", grade="E0_MINIMAL"),
        )
        for record in cases:
            with self.subTest(record=record["relative_path"]):
                classification, reasons = classify_run(record)
                self.assertEqual(classification, DELETE)
                self.assertTrue(reasons)

    def test_only_ds_store_non_run_asset_is_delete_candidate(self) -> None:
        self.assertEqual(classify_asset({"relative_path": ".DS_Store"})[0], DELETE)
        self.assertEqual(classify_asset({"relative_path": "curated"})[0], COLD)

    def test_review_never_authorizes_deletion_or_paper_use(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            inventory_path = Path(tmp) / "inventory.json"
            inventory = {
                "results_root": "/legacy/Results",
                "summary": {"scan_complete": True, "scan_error_count": 0},
                "runs": [run_record(path="strong"), run_record(path="smoke", smoke=True)],
                "non_run_assets": [
                    {"relative_path": ".DS_Store", "size_bytes": 14}
                ],
            }
            inventory_path.write_text(json.dumps(inventory), encoding="utf-8")
            review = build_review(inventory_path, inventory)

        self.assertEqual(review["status"], "REVIEW_ONLY_NOT_DELETE_AUTHORIZATION")
        self.assertFalse(review["fact_boundary"]["classification_authorizes_deletion"])
        self.assertFalse(review["fact_boundary"]["direct_claim_or_paper_eligible"])
        self.assertEqual(review["summary"]["record_count"], 3)
        self.assertTrue(
            all(
                record["direct_claim_or_paper_eligible"] is False
                for record in review["records"]
            )
        )


if __name__ == "__main__":
    unittest.main()
