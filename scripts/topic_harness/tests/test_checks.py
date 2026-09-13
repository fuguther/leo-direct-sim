# -*- coding: utf-8 -*-
"""机械检查器测试：M/M/1 数值、反例存在性、各类证据缺口。"""
import math

import pytest

from scripts.topic_harness import checks


def test_mm1_known_values():
    # mu=1250/s 时 W(0.9)=0.72ms —— 与 run-20260910 审查复核的数字一致
    assert abs(checks.mm1_wait(0.9, 12500.0) * 1000.0 - 0.72) < 1e-9
    # rho->1 发散
    assert checks.mm1_wait(0.999, 12500.0) / checks.mm1_wait(0.9, 12500.0) > 100


def test_mm1_domain():
    with pytest.raises(ValueError):
        checks.mm1_wait(1.0, 12500.0)


def test_fixed_weight_counterexample_fires():
    # p_s=2, p_d=5, mu=1：rho*=0.75 处最优动作切换 → 固定权重推出固定动作被击落
    out = checks.run_check("fixed_weight_action_switch", {"p_short": 2.0, "p_detour": 5.0, "mu": 1.0})
    assert out["verdict"] == "BLOCK"
    assert abs(out["evidence"]["switch_rho"] - 0.75) < 0.01


def test_fallback_lossless_blocked_without_evidence():
    out = checks.run_check("fallback_lossless", {
        "claims_lossless": True, "evaluated_variants": ["u=1"], 
        "significance_evidence": 0, "dropped_experience_analysis": False})
    assert out["verdict"] == "BLOCK"
    out2 = checks.run_check("fallback_lossless", {
        "claims_lossless": True, "significance_evidence": 1, "dropped_experience_analysis": True})
    assert out2["verdict"] == "PASS"


def test_correlation_causality():
    assert checks.run_check("correlation_causality", {
        "causal_claim": True, "intervention_design": False, "evidence_note": "CKA 下降"})["verdict"] == "BLOCK"
    assert checks.run_check("correlation_causality", {
        "causal_claim": True, "intervention_design": True})["verdict"] == "PASS"


def test_bounded_negative():
    assert checks.run_check("bounded_negative", {
        "claims_absolute": False, "scope": "2026-09-03 检索式与数据库覆盖内"})["verdict"] == "PASS"
    assert checks.run_check("bounded_negative", {"claims_absolute": True})["verdict"] == "BLOCK"
    assert checks.run_check("bounded_negative", {"claims_absolute": False})["verdict"] == "BLOCK"


def test_grid_completeness():
    out = checks.run_check("grid_completeness", {
        "required_arms": ["静态最短路", "双阈值滞回最小动态臂"],
        "provided_arms": ["静态最短路"]})
    assert out["verdict"] == "BLOCK" and "双阈值滞回" in out["reason"]
    out2 = checks.run_check("grid_completeness", {
        "required_arms": ["静态最短路"], "provided_arms": ["静态最短路", "RL"]})
    assert out2["verdict"] == "PASS"