import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from CODE.experiment_platform.inventory_legacy_results import (
    InventoryError,
    MAX_LOG_TAIL_BYTES,
    build_inventory,
    main,
    write_inventory,
)


class LegacyResultsInventoryTests(unittest.TestCase):
    def _write(self, path: Path, content: str | bytes = "x") -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")

    def test_inventory_is_stable_and_grades_only_evidence_completeness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            results = base / "Results"
            results.mkdir()
            for non_run_name in ("_overnight_logs", "_plan_runs", "analysis", "curated"):
                self._write(results / non_run_name / "control.json", "{}")
            self._write(results / "_plan_runs" / "saved/checkpoint.pt", b"control checkpoint")
            self._write(results / "README.txt", "legacy notes")

            complete = results / "z_formal_run"
            self._write(
                complete / "run_trace/run_meta.json",
                json.dumps({"natural_end": True, "interrupted": False, "score": 999999}),
            )
            self._write(complete / "run_trace/graph_snapshot.json", "{}")
            self._write(complete / "hyperparams.txt", "seed=4")
            self._write(complete / "experiment_bundle/summary_metrics.csv", "metric,value\nscore,999999\n")
            self._write(complete / "experiment_bundle/metrics_definitions.json", "{}")
            self._write(complete / "artifact_manifest.json", "{}")
            self._write(complete / "NNs/model.h5", b"checkpoint")

            interrupted = results / "a_smoke_run"
            self._write(
                interrupted / "run_trace/run_meta.json",
                json.dumps({"natural_end": False, "interrupted": True}),
            )
            self._write(interrupted / "logfile.log", "interrupted")

            legacy_end = results / "b_legacy_end"
            self._write(legacy_end / "logfile.log", "work\nElapsed time: 0:00:03.1\n---\n")

            legacy_interrupt = results / "c_legacy_interrupt"
            self._write(legacy_interrupt / "logfile.log", "Elapsed time: 0:00:04\n")
            self._write(legacy_interrupt / "run_trace/interrupt_meta.json", "{}")

            payload = build_inventory(results)
            self.assertEqual(
                [run["relative_path"] for run in payload["runs"]],
                ["a_smoke_run", "b_legacy_end", "c_legacy_interrupt", "z_formal_run"],
            )
            self.assertEqual(
                [asset["relative_path"] for asset in payload["non_run_assets"]],
                ["README.txt", "_overnight_logs", "_plan_runs", "analysis", "curated"],
            )
            self.assertEqual(payload["summary"]["non_run_asset_count"], 5)
            smoke, legacy_end_record, legacy_interrupt_record, formal = payload["runs"]
            self.assertEqual(smoke["completion_signal"]["classification"], "INTERRUPTED_REPORTED")
            self.assertTrue(smoke["smoke_clues"]["detected"])
            self.assertEqual(smoke["evidence_grade"], "E1_METADATA")
            self.assertEqual(
                legacy_end_record["completion_signal"]["classification"],
                "NATURAL_END_LOG_CLUE",
            )
            self.assertFalse(legacy_end_record["completion_signal"]["modern_natural_end_established"])
            self.assertEqual(legacy_end_record["evidence_grade"], "E0_MINIMAL")
            self.assertEqual(
                legacy_interrupt_record["completion_signal"]["classification"],
                "INTERRUPT_META_CLUE",
            )
            self.assertEqual(
                legacy_interrupt_record["completion_signal"]["legacy_clues"],
                ["NATURAL_END_LOG_CLUE", "INTERRUPT_META_PRESENT"],
            )
            self.assertEqual(legacy_interrupt_record["evidence_grade"], "E0_MINIMAL")
            self.assertEqual(
                formal["evidence_grade"], "E3_MANIFEST_AND_COMPLETION_REPORT_PRESENT"
            )
            self.assertFalse(formal["completion_signal"]["modern_natural_end_established"])
            self.assertTrue(
                formal["completion_signal"]["natural_end_metadata_reports_noninterrupted"]
            )
            self.assertIn(
                "does not verify provenance",
                " ".join(formal["evidence_limitations"]),
            )
            self.assertTrue(formal["key_artifacts_present"]["checkpoint_any"])
            for run in payload["runs"]:
                self.assertEqual(run["claim_status"], "UNVERIFIED_LEGACY")
                self.assertFalse(run["direct_claim_or_paper_eligible"])
            for asset in payload["non_run_assets"]:
                self.assertEqual(asset["claim_status"], "UNVERIFIED_LEGACY")
                self.assertFalse(asset["direct_claim_or_paper_eligible"])

            # Checkpoints are indexed one-by-one but are not silently promoted
            # to preservation proof by the quick inventory.
            self.assertNotIn("experiment_bundle/summary_metrics.csv", formal["key_file_hashes"])
            self.assertNotIn("NNs/model.h5", formal["key_file_hashes"])
            self.assertIn("run_trace/run_meta.json", formal["key_file_hashes"])
            self.assertEqual(len(formal["checkpoints"]), 1)
            checkpoint = formal["checkpoints"][0]
            self.assertEqual(checkpoint["relative_path"], "NNs/model.h5")
            self.assertEqual(checkpoint["size_bytes"], len(b"checkpoint"))
            self.assertIsInstance(checkpoint["mtime_ns"], int)
            self.assertEqual(checkpoint["role_heuristic"], "POSSIBLE_MODEL_STATE")
            self.assertEqual(
                checkpoint["hash_status"], "PENDING_NOT_HASHED_BY_QUICK_INVENTORY"
            )
            self.assertIsNone(checkpoint["sha256"])
            self.assertEqual(checkpoint["lineage_status"], "UNKNOWN")
            self.assertEqual(checkpoint["claim_status"], "UNVERIFIED_LEGACY")
            self.assertFalse(checkpoint["direct_claim_or_paper_eligible"])

            plan_asset = next(
                asset for asset in payload["non_run_assets"] if asset["relative_path"] == "_plan_runs"
            )
            self.assertEqual(plan_asset["asset_type"], "CONTROL_DIRECTORY")
            control_checkpoint = next(
                item
                for item in plan_asset["file_index"]
                if item["relative_path"] == "saved/checkpoint.pt"
            )
            self.assertEqual(control_checkpoint["lineage_status"], "UNKNOWN")
            self.assertEqual(payload["summary"]["checkpoint_count"], 2)
            top_file = payload["non_run_assets"][0]
            self.assertEqual(top_file["asset_type"], "TOP_LEVEL_FILE")
            self.assertEqual(top_file["hash_status"], "HASHED_BY_QUICK_INVENTORY")
            self.assertEqual(payload["inventory_semantics"]["inventory_class"], "QUICK_INDEX_ONLY")
            self.assertFalse(payload["inventory_semantics"]["migration_or_preservation_proof"])
            self.assertFalse(payload["inventory_semantics"]["deletion_authorization"])

            output = base / "inventory.json"
            write_inventory(payload, output, results)
            first = output.read_bytes()
            write_inventory(build_inventory(results), output, results)
            self.assertEqual(first, output.read_bytes())

    def test_invalid_metadata_is_minimal_and_large_log_is_not_hashed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            results = base / "Results"
            run = results / "broken"
            self._write(run / "run_trace/run_meta.json", "not-json")
            self._write(run / "logfile.log", b"x" * (2 * 1024 * 1024 + 1))

            record = build_inventory(results)["runs"][0]
            self.assertEqual(record["run_meta_state"], "INVALID")
            self.assertEqual(record["evidence_grade"], "E0_MINIMAL")
            self.assertIn("logfile.log", record["key_file_hashes_skipped"])
            self.assertFalse(record["scan_complete"])
            self.assertTrue(record["scan_errors"])

    def test_elapsed_time_search_is_bounded_to_log_tail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            results = Path(tmp) / "Results"
            run = results / "run"
            self._write(
                run / "logfile.log",
                b"Elapsed time: 0:00:01\n" + b"x" * (MAX_LOG_TAIL_BYTES + 1),
            )

            completion = build_inventory(results)["runs"][0]["completion_signal"]
            self.assertEqual(completion["classification"], "UNKNOWN")
            self.assertEqual(completion["legacy_clues"], [])

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks unsupported")
    def test_symlinks_are_skipped_and_cannot_escape_results_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            results = base / "Results"
            run = results / "run"
            run.mkdir(parents=True)
            secret = base / "outside.json"
            secret.write_text('{"secret": true}', encoding="utf-8")
            (run / "run_meta_link.json").symlink_to(secret)
            (run / "outside_dir").symlink_to(base, target_is_directory=True)
            (results / "linked_run").symlink_to(base, target_is_directory=True)

            payload = build_inventory(results)
            self.assertEqual(payload["summary"]["run_count"], 1)
            linked_run = next(
                asset
                for asset in payload["non_run_assets"]
                if asset["relative_path"] == "linked_run"
            )
            self.assertEqual(linked_run["asset_type"], "TOP_LEVEL_SYMLINK")
            self.assertEqual(linked_run["target"], str(base))
            self.assertFalse(linked_run["target_followed"])
            self.assertEqual(
                payload["runs"][0]["symlinks"],
                [
                    {
                        "claim_status": "UNVERIFIED_LEGACY",
                        "direct_claim_or_paper_eligible": False,
                        "relative_path": "outside_dir",
                        "target": str(base),
                        "target_followed": False,
                    },
                    {
                        "claim_status": "UNVERIFIED_LEGACY",
                        "direct_claim_or_paper_eligible": False,
                        "relative_path": "run_meta_link.json",
                        "target": str(secret),
                        "target_followed": False,
                    },
                ],
            )
            self.assertEqual(payload["runs"][0]["size_bytes"], 0)

    def test_root_scan_error_is_recorded_as_incomplete_not_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            results = Path(tmp) / "Results"
            results.mkdir()
            with mock.patch(
                "CODE.experiment_platform.inventory_legacy_results.os.scandir",
                side_effect=PermissionError("denied"),
            ):
                payload = build_inventory(results)

            self.assertFalse(payload["summary"]["scan_complete"])
            self.assertEqual(payload["summary"]["scan_error_count"], 1)
            self.assertIn("PermissionError", payload["summary"]["scan_errors"][0])
            self.assertEqual(payload["summary"]["run_count"], 0)

    def test_cli_writes_partial_inventory_but_returns_nonzero_when_scan_is_incomplete(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            results = base / "Results"
            results.mkdir()
            output = base / "partial.json"
            incomplete = build_inventory(results)
            incomplete["summary"]["scan_complete"] = False
            incomplete["summary"]["scan_error_count"] = 1
            incomplete["summary"]["scan_errors"] = [".: PermissionError"]

            with (
                mock.patch.object(sys, "argv", ["inventory_legacy_results.py", str(results), "--out", str(output)]),
                mock.patch(
                    "CODE.experiment_platform.inventory_legacy_results.build_inventory",
                    return_value=incomplete,
                ),
                mock.patch("CODE.experiment_platform.inventory_legacy_results.print") as printed,
            ):
                self.assertEqual(main(), 3)

            self.assertTrue(output.is_file())
            self.assertFalse(json.loads(output.read_text())["summary"]["scan_complete"])
            self.assertTrue(
                any(call.args and str(call.args[0]).startswith("INCOMPLETE ") for call in printed.call_args_list)
            )

    def test_top_level_checkpoint_is_pending_with_unknown_lineage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            results = Path(tmp) / "Results"
            results.mkdir()
            self._write(results / "orphan_target.ckpt", b"legacy")

            payload = build_inventory(results)
            record = payload["non_run_assets"][0]
            self.assertEqual(record["asset_type"], "TOP_LEVEL_FILE")
            self.assertEqual(record["role_heuristic"], "POSSIBLE_TARGET_NETWORK_STATE")
            self.assertEqual(record["hash_status"], "PENDING_NOT_HASHED_BY_QUICK_INVENTORY")
            self.assertEqual(record["lineage_status"], "UNKNOWN")
            self.assertIsNone(record["sha256"])

    def test_output_inside_results_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            results = Path(tmp) / "Results"
            results.mkdir()
            payload = build_inventory(results)
            with self.assertRaisesRegex(InventoryError, "outside"):
                write_inventory(payload, results / "inventory.json", results)


if __name__ == "__main__":
    unittest.main()
