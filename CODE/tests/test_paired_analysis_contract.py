from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from ANALYSIS import paired_analysis as pa


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


class PairedAnalysisContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "ANALYSIS").mkdir()
        shutil.copy(Path(pa.__file__), self.root / "ANALYSIS/paired_analysis.py")
        self.analysis = {
            "schema": "analysis-request/v2",
            "analysis_id": "AN-TEST",
            "experiment_id": "EXP-TEST",
            "primary_metric": "delivery_rate",
            "secondary_metrics": [],
            "cannot_conclude": ["This fixture is not a paper result."],
            "preregistration": {
                "paired_by": ["seed", "scenario_identity", "controlled_signature"],
                "planned_contrasts": [{
                    "name": "treatment_minus_control",
                    "left_arm": "treatment",
                    "right_arm": "control",
                    "estimand": "paired mean difference in delivery_rate",
                }],
            },
        }
        self.manifest = {
            "schema": "experiment-run-manifest/v2",
            "experiment_id": "EXP-TEST",
            "scenario_identity": {"fixture": "paired-analysis"},
            "planned_runs": [],
        }
        self.entries: list[tuple[str, Path]] = []
        for arm, value in (("control", 0.4), ("treatment", 0.6)):
            run_id = f"EXP-TEST-{arm}-s7"
            config = {
                "provenance": {
                    "experiment_id": "EXP-TEST", "run_id": run_id,
                    "arm_id": arm, "seed": 7,
                    "scenario_identity": self.manifest["scenario_identity"],
                    "required_artifacts": [
                        "run_trace/run_meta.json", "config_used.json",
                        "artifact_manifest.json", "experiment_bundle/summary_metrics.csv",
                    ],
                }
            }
            run = self.root / "runs" / run_id
            run.mkdir(parents=True)
            _write_json(run / "config_used.json", config)
            (run / "experiment_bundle").mkdir()
            (run / "experiment_bundle/summary_metrics.csv").write_text(
                f"metric,value\ndelivery_rate,{value}\n", encoding="utf-8")
            (run / "run_trace").mkdir()
            _write_json(run / "run_trace/run_meta.json", {
                "requested_run_id": run_id,
                "config_canonical_sha256": pa.canonical_sha(config),
                "scenario_identity_sha256": pa.canonical_sha(self.manifest["scenario_identity"]),
                "natural_end": True, "interrupted": False,
                "effective_receipt": {
                    "schema": "leo-effective-receipt/v1",
                    "research_eligible": True, "mismatches": [],
                },
            })
            required = config["provenance"]["required_artifacts"]
            artifacts = []
            for relative in required:
                if relative == "artifact_manifest.json":
                    continue
                path = run / relative
                artifacts.append({"path": relative, "size": path.stat().st_size, "sha256": _sha(path)})
            _write_json(run / "artifact_manifest.json", {
                "schema": "artifact-manifest/v1", "run_id": run_id,
                "config_sha256": pa.canonical_sha(config),
                "required_artifacts": required, "artifacts": artifacts,
            })
            self.manifest["planned_runs"].append({
                "run_id": run_id, "arm_id": arm, "seed": 7,
                "config_sha256": pa.canonical_sha(config),
                "controlled_signature": "same-control-config",
            })
            self.entries.append((run_id, run))

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_complete_hash_verified_pairs_are_analyzed(self) -> None:
        manifest, results, errors = pa.execute(self.root, self.analysis, self.manifest, self.entries, self.root / "ANALYSIS/out")
        self.assertEqual(errors, [])
        self.assertEqual(len(results), 2)
        self.assertEqual(manifest["planned_contrasts"][0]["n_pairs"], 1)
        manifest["input_hashes"].update({
            "ANALYSIS/paired_analysis.py": _sha(self.root / "ANALYSIS/paired_analysis.py"),
        })
        pa.write_outputs(self.root, self.root / "ANALYSIS/out", manifest, results)
        valid, errors = pa.verify_persisted_analysis(self.root, self.root / "ANALYSIS/out/analysis-manifest.json")
        self.assertTrue(valid, errors)

    def test_hash_drift_is_fail_closed(self) -> None:
        manifest, results, errors = pa.execute(self.root, self.analysis, self.manifest, self.entries, self.root / "ANALYSIS/out")
        self.assertEqual(errors, [])
        manifest["input_hashes"]["ANALYSIS/paired_analysis.py"] = _sha(self.root / "ANALYSIS/paired_analysis.py")
        pa.write_outputs(self.root, self.root / "ANALYSIS/out", manifest, results)
        (self.entries[0][1] / "experiment_bundle/summary_metrics.csv").write_text("metric,value\ndelivery_rate,9\n", encoding="utf-8")
        valid, errors = pa.verify_persisted_analysis(self.root, self.root / "ANALYSIS/out/analysis-manifest.json")
        self.assertFalse(valid)
        self.assertTrue(any("hash mismatch" in item for item in errors))

    def test_incomplete_cohort_and_duplicate_run_are_rejected(self) -> None:
        manifest, _results, errors = pa.execute(self.root, self.analysis, self.manifest, self.entries[:1], self.root / "ANALYSIS/out")
        self.assertTrue(any("cohort" in item or "complete pairs" in item for item in errors))
        _manifest, _results, errors = pa.execute(self.root, self.analysis, self.manifest, self.entries + [self.entries[0]], self.root / "ANALYSIS/out")
        self.assertTrue(any("duplicate" in item or "cohort" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
