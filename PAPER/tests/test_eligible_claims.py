from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "PAPER"))
sys.path.insert(0, str(ROOT))
import eligible_claims as ec
from ANALYSIS.tests.test_paired_analysis import PairedAnalysisTests
from ANALYSIS import paired_analysis as pa


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class VerifiedAnalysisEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = PairedAnalysisTests(methodName="test_complete_hash_verified_pairs_are_analyzed")
        self.fixture.setUp()
        self.out = self.fixture.tmp / "paper-evidence"
        manifest, results, errors = pa.execute(
            ROOT, self.fixture.analysis, self.fixture.run_manifest,
            self.fixture.run_entries, self.out,
        )
        self.assertEqual(errors, [])
        pa.write_outputs(ROOT, self.out, manifest, results)
        self.manifest_path = self.out / "analysis-manifest.json"
        self.reference = {
            "path": str(self.manifest_path.relative_to(ROOT)),
            "sha256": sha(self.manifest_path),
        }

    def tearDown(self) -> None:
        self.fixture.tearDown()

    def test_recomputed_verified_manifest_is_accepted(self) -> None:
        self.assertTrue(ec.analysis_manifest_is_verified(ROOT, self.reference))

    def test_reference_or_smoke_profile_is_not_paper_evidence(self) -> None:
        self.assertFalse(ec.analysis_manifest_is_paper_eligible(ROOT, self.reference))

    def test_mutated_analysis_output_invalidates_evidence(self) -> None:
        summary = self.out / "summary.csv"
        summary.write_text("metric,value\nx,999\n", encoding="utf-8")
        self.assertFalse(ec.analysis_manifest_is_verified(ROOT, self.reference))

    def _rehash_manifest_entry(self, section: str, path: Path) -> None:
        manifest = json.loads(self.manifest_path.read_text())
        rel = str(path.relative_to(ROOT))
        if section == "inputs":
            manifest[section][rel] = sha(path)
        else:
            for item in manifest[section]:
                if item["path"] == rel:
                    item["sha256"] = sha(path)
        self.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        self.reference["sha256"] = sha(self.manifest_path)

    def test_rehashed_fabricated_report_is_rejected(self) -> None:
        report = self.out / "report.md"
        report.write_text("# Fabricated narrative\n\nThis was not rendered from the analysis.\n", encoding="utf-8")
        self._rehash_manifest_entry("output_artifacts", report)
        self.assertFalse(ec.analysis_manifest_is_verified(ROOT, self.reference))

    def test_rehashed_extra_summary_column_is_rejected(self) -> None:
        summary = self.out / "summary.csv"
        lines = summary.read_text(encoding="utf-8").splitlines()
        lines[0] += ",fabricated_claim"
        for index in range(1, len(lines)):
            lines[index] += ",invented"
        summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
        self._rehash_manifest_entry("output_artifacts", summary)
        self.assertFalse(ec.analysis_manifest_is_verified(ROOT, self.reference))

    def test_rehashed_fake_code_snapshot_is_rejected(self) -> None:
        code = self.out / "analysis-code.py"
        code.write_text("not executable analysis code\n", encoding="utf-8")
        self._rehash_manifest_entry("inputs", code)
        self.assertFalse(ec.analysis_manifest_is_verified(ROOT, self.reference))

    def test_self_declared_verified_manifest_over_arbitrary_text_is_rejected(self) -> None:
        fake = self.fixture.tmp / "fake"
        fake.mkdir()
        text = fake / "run_meta.json"
        text.write_text("{}\n", encoding="utf-8")
        fake_manifest = fake / "analysis-manifest.json"
        fake_manifest.write_text(json.dumps({
            "schema": "analysis-manifest/v1", "status": "VERIFIED", "errors": [],
            "inputs": {str(text.relative_to(ROOT)): sha(text)},
            "bound_run_artifacts": [{"path": str(text.relative_to(ROOT)), "sha256": sha(text)}],
            "output_artifacts": [], "verified_run_ids": ["invented"],
            "planned_contrasts": ["invented"],
        }), encoding="utf-8")
        reference = {"path": str(fake_manifest.relative_to(ROOT)), "sha256": sha(fake_manifest)}
        self.assertFalse(ec.analysis_manifest_is_verified(ROOT, reference))

    def test_post_review_claim_text_change_is_rejected(self) -> None:
        candidate = self.out / "report.md"
        claim = {
            "schema": "research-claim/v2", "claim_id": "CL-TEST",
            "author_id": "producer:claim-author", "author_session_id": "P-claim-r01",
            "candidate_artifact": {"path": str(candidate.relative_to(ROOT)), "sha256": sha(candidate)},
            "statement": "The paired fixture shows a bounded diagnostic difference.",
            "claim_type": "EXPERIMENT_RESULT", "status": "SUPPORTED_LIMITED",
            "scope": "Only the two planned fixture seeds and compiled scenario.",
            "evidence": [{
                "evidence_id": "EV-TEST", "evidence_kind": "VERIFIED_ANALYSIS",
                "artifact": self.reference, "supports": "Supports only the stated paired diagnostic contrast.",
            }],
            "limitations": ["The fixture is not a scientific performance experiment."],
            "alternative_explanations": ["The difference is deliberately injected by the test fixture."],
            "support_gate": {"status": "PASS"}, "value_gate": {"status": "KEEP"},
        }
        subject = ec.claim_review_sha256(claim)
        artifacts = {
            claim["candidate_artifact"]["path"]: claim["candidate_artifact"]["sha256"],
            self.reference["path"]: self.reference["sha256"],
        }
        refs = []
        for label, role, reviewer in (
            ("support", "claim_support", "support-reviewer"),
            ("value", "claim_value", "value-reviewer"),
        ):
            receipt_id = f"RR-{label.upper()}-TEST"
            receipt_path = self.fixture.tmp / f"{label}-test.json"
            receipt = {
                "schema": "agent-review-receipt/v2", "receipt_id": receipt_id,
                "work_id": "WP-CLAIM-TEST", "revision": 1, "artifact_hashes": artifacts,
                "producer_id": claim["author_id"], "producer_session_id": claim["author_session_id"],
                "reviewer_id": f"reviewer:{reviewer}", "reviewer_session_id": f"R-{reviewer}-r01",
                "independence": {"producer_and_reviewer_are_distinct": True, "review_started_from_declared_inputs": True},
                "role": role, "verdict": "PASS", "subject_sha256": subject,
                "evidence": ["Reviewed the canonical claim payload and every bound artifact."],
                "blocking_findings": [], "unknowns": [], "required_revision": [],
            }
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
            refs.append({
                "receipt_id": receipt_id, "path": str(receipt_path.relative_to(ROOT)),
                "sha256": sha(receipt_path), "reviewer_id": receipt["reviewer_id"],
                "reviewer_session_id": receipt["reviewer_session_id"], "role": role,
                "verdict": "PASS", "subject_sha256": subject,
            })
        claim["support_gate"]["receipt"] = refs[0]
        claim["value_gate"]["receipt"] = refs[1]
        with mock.patch.object(ec, "analysis_manifest_is_paper_eligible", return_value=True):
            self.assertTrue(ec.is_eligible(ROOT, claim))
            original_statement = claim["statement"]
            claim["statement"] = "A materially different claim was inserted after review."
            self.assertFalse(ec.is_eligible(ROOT, claim))
            claim["statement"] = original_statement
            claim["value_gate"]["status"] = "PROMOTE"
            self.assertFalse(ec.is_eligible(ROOT, claim))
            claim["value_gate"]["status"] = "KEEP"
            support_path = ROOT / claim["support_gate"]["receipt"]["path"]
            support_receipt = json.loads(support_path.read_text())
            support_receipt.pop("unknowns")
            support_path.write_text(json.dumps(support_receipt), encoding="utf-8")
            claim["support_gate"]["receipt"]["sha256"] = sha(support_path)
            self.assertFalse(ec.is_eligible(ROOT, claim))


if __name__ == "__main__":
    unittest.main()
