#!/usr/bin/env python3
"""Local evidence transactions. Validates records, not scientific truth.

The caller controls this filesystem: identities/reviews are attestations, not an
authorization boundary. No network, model calls, Zotero writes or simulations.
"""
import argparse
import copy
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone


class Invalid(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def packed(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def text(value):
    return isinstance(value, str) and bool(value.strip())


def ident(value):
    require(isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,119}", value), "invalid record id")
    return value


def stamp():
    return datetime.now(timezone.utc).isoformat()


def atomic(path, data):
    path = Path(path)
    fd, name = tempfile.mkstemp(prefix=".write-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
        dirfd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(dirfd)
        finally:
            os.close(dirfd)
    finally:
        if os.path.exists(name):
            os.unlink(name)


EMPTY = {"schema": "leo-research-ops/v1", "revision": 0, "papers": {}, "sources": {},
         "derived": {}, "reads": {}, "claims": {}, "notes": {}, "tasks": {}, "reviews": {}, "history": []}


class Store:
    def __init__(self, root):
        self.root = Path(root).resolve()

    @contextmanager
    def lock(self):
        self.root.mkdir(parents=True, exist_ok=True)
        with (self.root / ".lock").open("a+b") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            yield

    def read(self):
        path = self.root / "state.json"
        return json.loads(path.read_text()) if path.exists() else copy.deepcopy(EMPTY)

    def blob(self, path, expected):
        path = Path(path)
        require(path.is_file(), "asset is not a file")
        data = path.read_bytes()
        actual = digest(data)
        require(expected == actual, "asset hash mismatch")
        dest = self.root / "blobs" / actual
        dest.parent.mkdir(exist_ok=True)
        if dest.exists():
            require(digest(dest.read_bytes()) == actual, "corrupt existing blob")
        else:
            atomic(dest, data)
        return actual

    def verify_blobs(self, state):
        hashes = set()
        for name in ("sources", "derived"):
            hashes.update(r["sha256"] for r in state[name].values())
        for versions in state["notes"].values():
            hashes.update(r["sha256"] for r in versions)
        hashes.update(r["artifact_sha256"] for r in state["tasks"].values() if r.get("artifact_sha256"))
        for sha in hashes:
            path = self.root / "blobs" / sha
            require(path.is_file() and digest(path.read_bytes()) == sha, "missing/corrupt blob: " + sha)

    def apply(self, patch):
        require(isinstance(patch, dict), "patch must be an object")
        require(type(patch.get("expected_revision")) is int, "expected_revision integer required")
        require(text(patch.get("actor")) and text(patch.get("reason")), "actor and reason required")
        require(isinstance(patch.get("operations"), list) and patch["operations"], "operations required")
        with self.lock():
            before = self.read()
            require(before["revision"] == patch["expected_revision"], "revision conflict; reread and rebase")
            self.verify_blobs(before)
            state = copy.deepcopy(before)
            for op in patch["operations"]:
                self.operation(state, op)
            self.validate(state)
            self.verify_blobs(state)
            state["revision"] += 1
            state["history"].append({"revision": state["revision"], "parent": before["revision"],
                                     "actor": patch["actor"], "reason": patch["reason"], "at": stamp(),
                                     "patch_sha256": digest(packed(patch)), "previous_sha256": digest(packed(before))})
            history = self.root / "history"
            history.mkdir(exist_ok=True)
            previous = history / f'{before["revision"]:06d}.json'
            if previous.exists():
                require(previous.read_bytes() == packed(before), "history mismatch")
            else:
                atomic(previous, packed(before))
            # This replace is the transaction commit. Earlier orphan blobs are harmless.
            atomic(self.root / "state.json", packed(state))
            return state

    def operation(self, s, op):
        require(isinstance(op, dict), "operation must be an object")
        kind = op.get("op")
        record = copy.deepcopy(op.get("record", {}))
        require(isinstance(record, dict), "record must be an object")
        if kind in {"paper", "source", "derived", "read", "claim", "task", "review"}:
            key = ident(record.get("id"))
            table = {"paper": "papers", "source": "sources", "derived": "derived", "read": "reads",
                     "claim": "claims", "task": "tasks", "review": "reviews"}[kind]
            require(key not in s[table], "record exists; append a new revision/id")
            if kind == "paper":
                doi = record.get("doi")
                if doi:
                    doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi.strip().lower())
                    require(doi.startswith("10.") and "/" in doi, "invalid DOI")
                    require(not any(p.get("doi") == doi for p in s["papers"].values()), "DOI exists; reuse paper id")
                    record["doi"] = doi
                require(text(record.get("title")) and text(record.get("metadata_source")), "paper metadata required")
            if kind in {"source", "derived"}:
                self.blob(record.pop("path"), record.get("sha256"))
            if kind == "claim":
                active = s["papers"].get(record.get("paper_id"), {}).get("active_source")
                record["currency"] = "needs_recheck" if active and active != record.get("source_id") else "current"
                old = record.get("supersedes")
                if old:
                    require(old in s["claims"], "unknown superseded claim")
                    require(s["claims"][old]["paper_id"] == record["paper_id"], "cross-paper correction")
                    require(s["claims"][old]["currency"] != "superseded", "claim already superseded")
                    s["claims"][old]["currency"] = "superseded"
                    self.invalidate(s, {old})
            if kind == "task":
                require(record.get("execution") == "queued", "new task must be queued")
                record.update(review="pending", content="draft", currency="current")
                if any(s["claims"].get(c, {}).get("currency") != "current" for c in record.get("claim_ids", [])):
                    record["currency"] = "needs_recheck"
            if kind == "review":
                task = s["tasks"].get(record.get("task_id"))
                require(task and task["execution"] == "delivered", "review requires delivered task")
                require(record.get("verdict") in {"accept", "revise", "reject", "unavailable"}, "invalid verdict")
                require(text(record.get("reviewer_session")) and text(record.get("rationale")), "review evidence required")
                require(record["reviewer_session"] != task["worker_session"], "self review is not independent")
                require(record.get("artifact_sha256") == task["artifact_sha256"], "review hash mismatch")
                require(digest(Path(task["artifact_path"]).read_bytes()) == task["artifact_sha256"], "artifact changed after delivery")
                require(task["currency"] == "current", "task evidence needs recheck")
                task["review"] = record["verdict"]
                task["content"] = "ready_for_content_review" if record["verdict"] == "accept" else "draft"
            s[table][key] = record
        elif kind == "activate_source":
            paper = s["papers"][op["paper_id"]]
            source = s["sources"][op["source_id"]]
            require(source["paper_id"] == op["paper_id"], "source/paper mismatch")
            paper["active_source"] = op["source_id"]
            stale = set()
            for key, claim in s["claims"].items():
                if (claim["paper_id"] == op["paper_id"] and claim["source_id"] != op["source_id"]
                        and claim["currency"] != "superseded"):
                    claim["currency"] = "needs_recheck"
                    stale.add(key)
            self.invalidate(s, stale)
        elif kind == "note":
            paper_id = op["paper_id"]
            require(paper_id in s["papers"], "unknown paper")
            versions = s["notes"].setdefault(paper_id, [])
            require(op["parent_note_revision"] == len(versions), "note revision conflict")
            sha = self.blob(op["path"], op["sha256"])
            require(all(c in s["claims"] and s["claims"][c]["paper_id"] == paper_id for c in op["claim_ids"]), "bad note claim")
            require(text(op.get("reason")), "note change reason required")
            versions.append({"revision": len(versions) + 1, "sha256": sha, "claim_ids": op["claim_ids"], "reason": op["reason"]})
        elif kind == "task_transition":
            task = s["tasks"][op["task_id"]]
            target = op["execution"]
            allowed = {"queued": {"running", "cancelled"}, "running": {"delivered", "failed", "cancelled"},
                       "failed": {"running"}, "cancelled": {"running"}, "delivered": {"running"}}
            require(target in allowed[task["execution"]], "invalid task transition")
            require(text(op.get("resume_from")), "resume_from / terminal explanation required")
            if target == "delivered":
                require(task["currency"] == "current", "cannot deliver with stale evidence")
                task["artifact_sha256"] = self.blob(op["artifact_path"], op["artifact_sha256"])
                task["artifact_path"] = str(Path(op["artifact_path"]).resolve())
            task.update(execution=target, review="pending", content="draft", resume_from=op["resume_from"])
        else:
            raise Invalid("unknown operation")

    @staticmethod
    def invalidate(s, claim_ids):
        for task in s["tasks"].values():
            if claim_ids.intersection(task.get("claim_ids", [])):
                task.update(currency="needs_recheck", content="draft", review="pending")

    @staticmethod
    def locator(source, loc):
        require(isinstance(loc, dict), "locator required")
        if source["media_type"] == "application/pdf":
            page = loc.get("pdf_page_index")
            require(type(page) is int and 0 <= page < source["pages"], "PDF page out of bounds")
            require(text(loc.get("section")) or text(loc.get("element")), "PDF section/element required")
        elif source["media_type"] == "text/html":
            require(text(loc.get("anchor")), "HTML anchor required")
        else:
            require(text(loc.get("file")) and type(loc.get("line")) is int and loc["line"] > 0, "code file/line required")

    def validate(self, s):
        require(s.get("schema") == EMPTY["schema"], "unsupported schema")
        for source in s["sources"].values():
            require(source.get("paper_id") in s["papers"], "unknown source paper")
            require(text(source.get("version")) and text(source.get("origin")), "version and origin required")
            require(source.get("media_type") in {"application/pdf", "text/html", "text/x-source"}, "unsupported source media")
            require(source.get("identity_status") in {"unverified", "checked"}, "identity status required")
            if source["identity_status"] == "checked":
                require(text(source.get("identity_by")) and text(source.get("identity_basis")), "identity attestation required")
            if source["media_type"] == "application/pdf":
                require(type(source.get("pages")) is int and source["pages"] > 0, "PDF pages required")
            if source["media_type"] == "text/x-source":
                require(bool(re.fullmatch(r"[a-f0-9]{40}", source.get("commit", ""))), "exact code commit required")
        for derived in s["derived"].values():
            source = s["sources"].get(derived.get("source_id"))
            require(source and derived.get("source_sha256") == source["sha256"], "derived source mismatch")
            require(text(derived.get("parser")) and text(derived.get("parser_version")), "parser version required")
            require(isinstance(derived.get("parameters"), dict) and isinstance(derived.get("defects"), list), "parse metadata required")
            require(derived.get("binding_status") in {"unverified", "checked"}, "binding status required")
            if derived["binding_status"] == "checked":
                require(text(derived.get("checked_by")) and text(derived.get("binding_basis")), "binding attestation required")
            require(text(derived.get("page_convention")), "page mapping convention required")
        for receipt in s["reads"].values():
            source = s["sources"].get(receipt.get("source_id"))
            require(source and receipt.get("source_sha256") == source["sha256"], "read source mismatch")
            require(text(receipt.get("session_id")) and text(receipt.get("question")), "reader and question required")
            require(type(receipt.get("truncated")) is bool and isinstance(receipt.get("unread"), list), "read coverage required")
            require(receipt.get("mode") in {"original", "derived", "both"}, "read mode required")
            if receipt["mode"] in {"derived", "both"}:
                derived = s["derived"].get(receipt.get("derived_id"))
                require(derived and derived["source_id"] == receipt["source_id"], "read derived mismatch")
            coverage = receipt.get("coverage", {})
            require(set(coverage) == {"identity", "method", "results", "limitations"}, "four coverage topics required")
            for topic in coverage.values():
                require(topic.get("status") in {"unread", "scanned", "checked", "not_applicable"}, "invalid coverage status")
                if topic["status"] in {"scanned", "checked"}:
                    require(bool(topic.get("locators")), "read locations required")
                    for loc in topic["locators"]:
                        self.locator(source, loc)
            if receipt["truncated"]:
                require(bool(receipt["unread"]), "truncated read must describe omitted scope")
        for claim in s["claims"].values():
            source = s["sources"].get(claim.get("source_id"))
            require(source and source["paper_id"] == claim.get("paper_id") and source["sha256"] == claim.get("source_sha256"), "claim source mismatch")
            require(text(claim.get("statement")) and text(claim.get("scope")), "claim statement/scope required")
            require(claim.get("support") in {"unverified", "supported", "partial", "contradicted"}, "invalid support")
            require(claim.get("interpretation") in {"author_report", "our_inference", "hypothesis"}, "invalid interpretation")
            require(claim.get("evidence_type") in {"abstract", "body_text", "equation", "table", "figure", "code", "experiment"}, "invalid evidence type")
            if claim["support"] != "unverified":
                require(source["identity_status"] == "checked", "source identity unchecked")
                receipt = s["reads"].get(claim.get("read_id"))
                require(receipt and receipt["source_id"] == claim["source_id"] and receipt["mode"] in {"original", "both"}, "checked claim requires original read")
                if receipt["mode"] == "both":
                    require(s["derived"][receipt["derived_id"]]["binding_status"] == "checked", "derived binding unchecked")
                self.locator(source, claim.get("locator"))
                if claim["evidence_type"] in {"equation", "table", "figure"}:
                    require(text(claim["locator"].get("element")), "equation/table/figure identifier required")
                recorded = [loc for topic in receipt["coverage"].values() if topic["status"] == "checked" for loc in topic.get("locators", [])]
                require(claim["locator"] in recorded, "claim location not covered by checked reading")
                require(text(claim.get("checked_by")) and text(claim.get("checked_at")) and text(claim.get("basis")), "claim verification attestation required")
                if claim["evidence_type"] == "figure":
                    require(claim.get("value_method") in {"no_numeric_value", "reported", "digitized_approx"}, "figure value method required")
                    if claim["value_method"] == "digitized_approx":
                        require(text(claim.get("digitization_note")), "digitization method/range required")
        for task in s["tasks"].values():
            require(text(task.get("worker_session")) and text(task.get("question")), "task session/question required")
            require(isinstance(task.get("claim_ids"), list) and all(c in s["claims"] for c in task["claim_ids"]), "task claim dependencies invalid")
            require(task.get("content") in {"draft", "ready_for_content_review"}, "worker cannot set user acceptance")
            if task.get("currency") == "current":
                require(all(s["claims"][c]["currency"] == "current" for c in task["claim_ids"]), "current task has stale claim dependencies")
            if task.get("content") == "ready_for_content_review":
                require(task["execution"] == "delivered" and task["review"] == "accept" and task["currency"] == "current", "invalid ready status")
                require(digest(Path(task["artifact_path"]).read_bytes()) == task["artifact_sha256"], "reviewed artifact changed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store", required=True, help="local evidence store outside tracked source")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    sub.add_parser("validate")
    apply = sub.add_parser("apply")
    apply.add_argument("patch")
    args = parser.parse_args()
    try:
        store = Store(args.store)
        if args.command == "apply":
            state = store.apply(json.loads(Path(args.patch).read_text()))
        else:
            with store.lock():
                state = store.read()
                if args.command == "validate":
                    store.validate(state)
                    store.verify_blobs(state)
        print(json.dumps({"ok": True, "revision": state["revision"], "counts": {k: len(state[k]) for k in ("papers", "sources", "derived", "reads", "claims", "notes", "tasks", "reviews")}}, ensure_ascii=False))
        return 0
    except (Invalid, OSError, KeyError, TypeError, AttributeError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
