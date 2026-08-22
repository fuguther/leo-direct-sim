import hashlib
from datetime import date
from pathlib import Path

from scripts.check_document_governance import audit_repository, load_registry


ROOT = Path(__file__).resolve().parents[2]


def _entry(path: str, **overrides: object) -> dict:
    entry = {
        "path": path,
        "status": "CURRENT-CONTRACT",
        "purpose": "test fixture",
        "may_direct_current_work": True,
        "owner": "test",
        "last_reviewed": "2026-08-23",
        "review_interval_days": 30,
        "replacement": None,
        "require_banner": False,
        "archive_candidate": False,
        "suggested_archive_target": None,
    }
    entry.update(overrides)
    return entry


def _registry(*entries: dict, coverage: list[str] | None = None) -> dict:
    return {
        "schema": "leo-document-governance/v1",
        "updated_at": "2026-08-23",
        "allowed_statuses": [
            "CURRENT-CONTRACT",
            "CURRENT-VOLATILE",
            "SUPPORTING",
            "ROLLING-LOG",
            "EVIDENCE-SNAPSHOT",
            "HISTORICAL",
            "SUPERSEDED",
        ],
        "coverage": coverage or [entry["path"] for entry in entries],
        "entry_point_invariants": [],
        "entries": list(entries),
    }


def test_repository_document_governance_is_clean():
    registry = load_registry(ROOT / "ANALYSIS" / "DOCUMENT-STATUS.json")
    report = audit_repository(ROOT, registry, today=date(2026, 8, 23))
    assert report["errors"] == []


def test_stale_current_document_fails_loud(tmp_path):
    (tmp_path / "CURRENT.md").write_text("# current\n", encoding="utf-8")
    registry = _registry(
        _entry(
            "CURRENT.md",
            status="CURRENT-VOLATILE",
            last_reviewed="2026-01-01",
            review_interval_days=7,
        )
    )

    report = audit_repository(tmp_path, registry, today=date(2026, 8, 23))

    assert any(error["code"] == "STALE_CURRENT" for error in report["errors"])
    assert report["stale"] == ["CURRENT.md"]


def test_unregistered_governed_document_fails_loud(tmp_path):
    (tmp_path / "known.md").write_text("# known\n", encoding="utf-8")
    (tmp_path / "forgotten.md").write_text("# forgotten\n", encoding="utf-8")
    registry = _registry(_entry("known.md"), coverage=["*.md"])

    report = audit_repository(tmp_path, registry, today=date(2026, 8, 23))

    assert any(
        error["code"] == "UNCLASSIFIED_DOCUMENT"
        and error["path"] == "forgotten.md"
        for error in report["errors"]
    )


def test_protected_document_hash_detects_casual_edit(tmp_path):
    protected = tmp_path / "AGENTS.md"
    protected.write_text("stable constitution\n", encoding="utf-8")
    expected = hashlib.sha256(protected.read_bytes()).hexdigest()
    registry = _registry(
        _entry("AGENTS.md", protected_sha256=expected, review_interval_days=90)
    )
    protected.write_text("casual status edit\n", encoding="utf-8")

    report = audit_repository(tmp_path, registry, today=date(2026, 8, 23))

    assert any(
        error["code"] == "PROTECTED_CONTENT_CHANGED"
        and error["path"] == "AGENTS.md"
        for error in report["errors"]
    )


def test_archive_candidates_are_reported_without_moving_files(tmp_path):
    historical = tmp_path / "old.md"
    historical.write_text("# old\n", encoding="utf-8")
    registry = _registry(
        _entry(
            "old.md",
            status="HISTORICAL",
            may_direct_current_work=False,
            last_reviewed=None,
            review_interval_days=None,
            archive_candidate=True,
            suggested_archive_target="HISTORY/old.md",
        )
    )

    report = audit_repository(tmp_path, registry, today=date(2026, 8, 23))

    assert report["archive_candidates"] == [
        {"path": "old.md", "suggested_target": "HISTORY/old.md"}
    ]
    assert historical.exists()
    assert not (tmp_path / "HISTORY" / "old.md").exists()
