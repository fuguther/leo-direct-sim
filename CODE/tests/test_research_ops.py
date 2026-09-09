"""Failure-oriented tests for the local evidence transaction contract."""
import copy
import importlib.util
import json
import multiprocessing
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[2] / "scripts" / "research_ops.py"
spec = importlib.util.spec_from_file_location("research_ops", MODULE)
ops = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ops)


def writer(root, revision, gate, results):
    gate.wait()
    try:
        ops.Store(root).apply({"expected_revision": revision, "actor": "worker", "reason": "concurrency",
                              "operations": [{"op": "paper", "record": {"id": "race", "title": "Race", "metadata_source": "fixture"}}]})
        results.put("ok")
    except ops.Invalid:
        results.put("conflict")


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.store = ops.Store(self.base / "store")
        # Synthetic bytes test storage only; real PDF semantics are checked in the smoke exercise.
        self.pdf = self.base / "paper.pdf"
        self.pdf.write_bytes(b"%PDF-fixture-one")
        self.sha = ops.digest(self.pdf.read_bytes())
        self.loc = {"pdf_page_index": 0, "section": "Abstract"}
        self.source = {"id": "s1", "paper_id": "p1", "path": str(self.pdf), "sha256": self.sha,
                       "media_type": "application/pdf", "pages": 2, "version": "v1", "origin": "fixture",
                       "identity_status": "checked", "identity_by": "reader", "identity_basis": "fixture only"}
        self.receipt = {"id": "r1", "source_id": "s1", "source_sha256": self.sha, "session_id": "reader-1",
                        "question": "fixture question", "mode": "original", "truncated": False, "unread": ["rest"],
                        "coverage": {k: {"status": "unread"} for k in ("identity", "method", "results", "limitations")}}
        self.receipt["coverage"]["identity"] = {"status": "checked", "locators": [self.loc]}
        self.claim = {"id": "c1", "paper_id": "p1", "source_id": "s1", "source_sha256": self.sha,
                      "statement": "fixture statement", "scope": "fixture only", "support": "supported",
                      "interpretation": "author_report", "evidence_type": "abstract", "read_id": "r1",
                      "locator": self.loc, "checked_by": "reader-1", "checked_at": "2026-09-09T00:00:00Z", "basis": "fixture basis"}
        self.apply([{"op": "paper", "record": {"id": "p1", "title": "Paper", "doi": "https://doi.org/10.1234/Test", "metadata_source": "fixture"}},
                    {"op": "source", "record": self.source}, {"op": "activate_source", "paper_id": "p1", "source_id": "s1"},
                    {"op": "read", "record": self.receipt}, {"op": "claim", "record": self.claim}])

    def apply(self, operations, revision=None):
        return self.store.apply({"expected_revision": self.store.read()["revision"] if revision is None else revision,
                                 "actor": "test", "reason": "test change", "operations": operations})

    def unchanged_failure(self, operation):
        before = (self.store.root / "state.json").read_bytes()
        with self.assertRaises((ops.Invalid, KeyError)):
            self.apply([operation])
        self.assertEqual(before, (self.store.root / "state.json").read_bytes())

    def test_normalized_identity_and_duplicate(self):
        self.assertEqual(self.store.read()["papers"]["p1"]["doi"], "10.1234/test")
        self.unchanged_failure({"op": "paper", "record": {"id": "p2", "doi": "10.1234/TEST", "title": "P", "metadata_source": "fixture"}})

    def test_wrong_asset_hash_is_atomic(self):
        self.unchanged_failure({"op": "source", "record": dict(self.source, id="wrong", sha256="0"*64)})

    def test_same_pdf_multiple_reads_one_blob(self):
        self.apply([{"op": "source", "record": dict(self.source, id="s-copy")},
                    {"op": "read", "record": dict(self.receipt, id="r2")}])
        self.assertEqual(len(list((self.store.root / "blobs").iterdir())), 1)
        self.assertEqual(len(self.store.read()["reads"]), 2)

    def test_checked_claim_location_and_receipt(self):
        for loc in ({"pdf_page_index": -1, "section": "X"}, {"pdf_page_index": 2, "section": "X"},
                    {"pdf_page_index": 1, "section": "unread"}, {}):
            self.unchanged_failure({"op": "claim", "record": dict(self.claim, id="c2", locator=loc)})
        self.unchanged_failure({"op": "claim", "record": dict(self.claim, id="c2", read_id="missing")})

    def test_unverified_hypothesis_allowed_without_fake_verification(self):
        c = dict(self.claim, id="h1", support="unverified", interpretation="hypothesis")
        for key in ("locator", "read_id", "checked_by", "checked_at", "basis"):
            c.pop(key)
        self.apply([{"op": "claim", "record": c}])

    def test_equation_requires_identifier_not_abstract_badge(self):
        self.unchanged_failure({"op": "claim", "record": dict(self.claim, id="equation", evidence_type="equation")})

    def test_derived_binding_requires_attestation_and_correct_hash(self):
        md = self.base / "derived.md"
        md.write_text("unrelated text")
        d = {"id": "d1", "source_id": "s1", "source_sha256": self.sha, "path": str(md), "sha256": ops.digest(md.read_bytes()),
             "parser": "fixture", "parser_version": "1", "parameters": {}, "defects": [], "binding_status": "unverified", "page_convention": "0 based"}
        self.unchanged_failure({"op": "derived", "record": dict(d, source_sha256="0"*64)})
        self.unchanged_failure({"op": "derived", "record": dict(d, binding_status="checked")})
        self.apply([{"op": "derived", "record": d}])
        r = dict(self.receipt, id="r2", mode="both", derived_id="d1")
        self.apply([{"op": "read", "record": r}])
        self.unchanged_failure({"op": "claim", "record": dict(self.claim, id="c2", read_id="r2")})

    def test_truncation_keeps_missing_scope(self):
        self.unchanged_failure({"op": "read", "record": dict(self.receipt, id="r2", truncated=True, unread=[])})
        self.apply([{"op": "read", "record": dict(self.receipt, id="r2", truncated=True)}])

    def test_revision_and_correction_history(self):
        before = copy.deepcopy(self.store.read())
        c = dict(self.claim, id="c2", supersedes="c1", statement="corrected")
        self.apply([{"op": "claim", "record": c}])
        self.assertEqual(self.store.read()["claims"]["c1"]["currency"], "superseded")
        self.assertEqual(json.loads((self.store.root / "history/000001.json").read_text()), before)
        with self.assertRaises(ops.Invalid):
            self.apply([{"op": "claim", "record": dict(c, id="c3")}], revision=1)

    def task(self):
        self.apply([{"op": "task", "record": {"id": "t1", "worker_session": "producer", "question": "review evidence", "claim_ids": ["c1"], "execution": "queued"}},
                    {"op": "task_transition", "task_id": "t1", "execution": "running", "resume_from": "start"}])
        report = self.base / "report.md"
        report.write_text("candidate report")
        sha = ops.digest(report.read_bytes())
        self.apply([{"op": "task_transition", "task_id": "t1", "execution": "delivered", "resume_from": "await review", "artifact_path": str(report), "artifact_sha256": sha}])
        return report, sha

    def test_source_versions_only_explicit_activation_invalidates(self):
        self.task()
        self.pdf.write_bytes(b"%PDF-fixture-new")
        source2 = dict(self.source, id="s2", version="v2", sha256=ops.digest(self.pdf.read_bytes()))
        self.apply([{"op": "source", "record": source2}])
        self.assertEqual(self.store.read()["claims"]["c1"]["currency"], "current")
        self.apply([{"op": "activate_source", "paper_id": "p1", "source_id": "s2"}])
        s = self.store.read()
        self.assertEqual(s["claims"]["c1"]["currency"], "needs_recheck")
        self.assertEqual(s["tasks"]["t1"]["currency"], "needs_recheck")
        self.assertEqual((self.store.root / "blobs" / self.sha).read_bytes(), b"%PDF-fixture-one")

    def test_review_reject_is_successful_delivery(self):
        _, sha = self.task()
        self.apply([{"op": "review", "record": {"id": "v1", "task_id": "t1", "reviewer_session": "reviewer", "verdict": "reject", "rationale": "insufficient evidence", "artifact_sha256": sha}}])
        task = self.store.read()["tasks"]["t1"]
        self.assertEqual((task["execution"], task["review"], task["content"]), ("delivered", "reject", "draft"))

    def test_self_review_and_mutated_artifact_rejected(self):
        report, sha = self.task()
        r = {"id": "v1", "task_id": "t1", "reviewer_session": "producer", "verdict": "accept", "rationale": "review", "artifact_sha256": sha}
        self.unchanged_failure({"op": "review", "record": r})
        report.write_text("changed")
        self.unchanged_failure({"op": "review", "record": dict(r, reviewer_session="reviewer")})

    def test_post_review_mutation_fails_validation(self):
        report, sha = self.task()
        self.apply([{"op": "review", "record": {"id": "v1", "task_id": "t1", "reviewer_session": "reviewer", "verdict": "accept", "rationale": "review", "artifact_sha256": sha}}])
        report.write_text("changed after review")
        with self.assertRaises(ops.Invalid):
            self.store.validate(self.store.read())

    def test_concurrent_writers_exactly_one_commits(self):
        ctx = multiprocessing.get_context("fork")
        gate, results = ctx.Event(), ctx.Queue()
        workers = [ctx.Process(target=writer, args=(str(self.store.root), 1, gate, results)) for _ in range(2)]
        for p in workers:
            p.start()
        gate.set()
        for p in workers:
            p.join(10)
            self.assertEqual(p.exitcode, 0)
        self.assertEqual(sorted([results.get(timeout=2), results.get(timeout=2)]), ["conflict", "ok"])
        self.assertEqual(self.store.read()["revision"], 2)

    def test_note_versions_preserve_original(self):
        note = self.base / "note.md"
        note.write_text("first")
        op = {"op": "note", "paper_id": "p1", "parent_note_revision": 0, "path": str(note), "sha256": ops.digest(note.read_bytes()), "claim_ids": ["c1"], "reason": "initial"}
        self.apply([op])
        old = op["sha256"]
        note.write_text("reread")
        self.apply([dict(op, parent_note_revision=1, sha256=ops.digest(note.read_bytes()), reason="reread")])
        self.assertEqual((self.store.root / "blobs" / old).read_text(), "first")
        self.unchanged_failure(dict(op, sha256=ops.digest(note.read_bytes())))

    def test_corrupt_blob_detected(self):
        (self.store.root / "blobs" / self.sha).write_bytes(b"corrupt")
        with self.assertRaises(ops.Invalid):
            self.store.verify_blobs(self.store.read())

    def hook(self, payload, bindings):
        path = self.base / "bindings.json"
        path.write_text(json.dumps(bindings))
        result = subprocess.run([sys.executable, str(MODULE.with_name("research_ops_hook.py")), "--bindings", str(path)],
                                input=json.dumps(payload), text=True, capture_output=True, check=True)
        return json.loads(result.stdout)

    def test_hook_blocks_pending_and_accepts_reject_delivery(self):
        _, sha = self.task()
        payload = {"hook_event_name": "PreToolUse", "tool_name": "update_goal", "tool_input": {"action": "complete"},
                   "session_id": "producer", "cwd": str(self.base)}
        bindings = {"sessions": {"producer": {"cwd": str(self.base), "store": str(self.store.root), "task_id": "t1"}}}
        self.assertEqual(self.hook(payload, bindings)["hookSpecificOutput"]["permissionDecision"], "deny")
        self.apply([{"op": "review", "record": {"id": "v1", "task_id": "t1", "reviewer_session": "reviewer", "verdict": "reject", "rationale": "insufficient", "artifact_sha256": sha}}])
        self.assertEqual(self.hook(payload, bindings), {})
        self.assertEqual(self.hook(dict(payload, cwd=str(self.base/'other')), bindings)["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_hook_does_not_force_stop_or_touch_unbound_sessions(self):
        payload = {"hook_event_name": "PreToolUse", "tool_name": "update_goal", "tool_input": {"action": "complete"}, "session_id": "other"}
        self.assertEqual(self.hook(payload, {"sessions": {}}), {})
        self.assertEqual(self.hook(dict(payload, hook_event_name="Stop"), {}), {})
        self.assertEqual(self.hook(dict(payload, tool_input={"action": "blocked"}), {}), {})

    def test_new_task_with_old_claim_is_not_current(self):
        self.apply([{"op": "claim", "record": dict(self.claim, id="c2", supersedes="c1")}])
        self.apply([{"op": "task", "record": {"id": "old-task", "worker_session": "worker", "question": "old evidence", "claim_ids": ["c1"], "execution": "queued"}}])
        self.assertEqual(self.store.read()["tasks"]["old-task"]["currency"], "needs_recheck")


if __name__ == "__main__":
    unittest.main()
