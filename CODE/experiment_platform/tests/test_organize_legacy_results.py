from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from CODE.experiment_platform.organize_legacy_results import build_plan, execute_moves


class OrganizeLegacyResultsTest(unittest.TestCase):
    def fixtures(self):
        review = {
            "summary": {"run_count": 4},
            "records": [
                {"record_type": "RUN", "relative_path": "core", "size_bytes": 10},
                {"record_type": "RUN", "relative_path": "rescue", "size_bytes": 20},
                {"record_type": "RUN", "relative_path": "old-a", "size_bytes": 30},
                {"record_type": "RUN", "relative_path": "old-b", "size_bytes": 40},
                {"record_type": "NON_RUN_ASSET", "relative_path": "_plan_runs", "size_bytes": 5},
            ],
        }
        salvage = {
            "core_retrospective_cohorts": {"X": {"paths": ["core"]}},
            "deletion_candidate_reclassification": {
                "RESCUE_FOR_REVIEW": {
                    "records": [{"relative_path": "rescue", "size_bytes": 20}]
                }
            },
        }
        return review, salvage

    def test_plan_is_exhaustive_and_keeps_non_run_assets(self):
        review, salvage = self.fixtures()
        plan = build_plan(review, salvage)
        self.assertEqual(plan["protected_paths"], ["core", "rescue"])
        self.assertEqual(plan["archive_paths"], ["old-a", "old-b"])
        self.assertEqual(plan["non_run_asset_paths"], ["_plan_runs"])
        self.assertEqual(plan["counts"]["archive_run_total"], 2)

    def test_execute_is_reversible_move_and_idempotent(self):
        review, salvage = self.fixtures()
        plan = build_plan(review, salvage)
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            source = parent / "Results"
            archive = parent / "Results_ARCHIVE"
            source.mkdir()
            for path in plan["protected_paths"] + plan["archive_paths"] + plan["non_run_asset_paths"]:
                (source / path).mkdir()

            first = execute_moves(source, archive, plan)
            self.assertEqual(first["moved_now"], 2)
            self.assertTrue((source / "core").is_dir())
            self.assertTrue((source / "rescue").is_dir())
            self.assertTrue((source / "_plan_runs").is_dir())
            self.assertFalse((source / "old-a").exists())
            self.assertTrue((archive / "old-a").is_dir())

            second = execute_moves(source, archive, plan)
            self.assertEqual(second["moved_now"], 0)
            receipt = json.loads((archive / "_organization_receipt.json").read_text())
            self.assertEqual(receipt["verification"]["archived_count"], 2)


if __name__ == "__main__":
    unittest.main()
