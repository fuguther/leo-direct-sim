# -*- coding: utf-8 -*-
"""审查运行器测试：误放/误杀统计与真实测试集全绿。"""
import json
import os

from scripts.topic_harness.audit import audit_dir, DEFAULT_CASES


def test_audit_counts(tmp_path):
    cases = tmp_path / "cases"
    cases.mkdir()
    (cases / "c1.json").write_text(json.dumps({
        "id": "c1", "check": "bounded_negative",
        "params": {"claims_absolute": False, "scope": "s"},
        "expected_verdict": "PASS"}), encoding="utf-8")
    (cases / "c2.json").write_text(json.dumps({
        "id": "c2", "check": "correlation_causality",
        "params": {"causal_claim": True, "intervention_design": False},
        "expected_verdict": "BLOCK"}), encoding="utf-8")
    (cases / "c3.json").write_text(json.dumps({
        "id": "c3", "check": "bounded_negative",
        "params": {"claims_absolute": True},
        "expected_verdict": "PASS"}), encoding="utf-8")  # 故意造一个误杀
    rep = audit_dir(str(cases))
    assert rep["false_release"] == 0
    assert rep["false_kill"] == 1
    assert rep["all_ok"] is False


def test_real_testset_all_green():
    rep = audit_dir(DEFAULT_CASES)
    assert rep["results"], "真实测试集不应为空"
    assert rep["false_release"] == 0, [r for r in rep["results"] if r["kind"] == "误放"]
    assert rep["false_kill"] == 0, [r for r in rep["results"] if r["kind"] == "误杀"]
