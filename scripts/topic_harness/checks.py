#!/usr/bin/env python3
"""机械论证检查器（选题 harness 第四层第一格）。

原则（AlphaEvolve §2.4 / run-20260910 裁决教训）：
- 可执行检查是地板；LLM 审查只补难量化维度，不做主指标。
- 本库只回答"这一类论证在给定参数下是否成立"，不做文本理解；
  文本级反例发现是审查者模型的职责，本库给它提供可复跑的裁决器。

每个 check(params) -> {"verdict": "PASS"|"BLOCK", "reason": str, "evidence": dict}
约定：对"断言类"检查，BLOCK = 该断言被反例/证据缺口击落。
"""
from __future__ import annotations

import math


def mm1_wait(rho: float, mu: float) -> float:
    """M/M/1 平均等待 W = rho/(mu*(1-rho))；单位与 1/mu 一致（mu 用 1/s 则 W 为 s）。"""
    if not (0.0 <= rho < 1.0):
        raise ValueError("rho must be in [0,1)")
    if mu <= 0.0:
        raise ValueError("mu>0 required")
    return rho / (mu * (1.0 - rho))


def check_queue_divergence(params: dict) -> dict:
    """重算队列时延，核对断言数值是否算错（算术程序复核的参数化版）。"""
    mu = float(params["mu"])
    claimed = params.get("claimed_W", {})
    computed = {}
    worst_rel = 0.0
    for key, rho in params.get("rhos", {}).items():
        w = mm1_wait(float(rho), mu)
        computed[key] = w
        if key in claimed:
            rel = abs(w - float(claimed[key])) / max(abs(float(claimed[key])), 1e-12)
            worst_rel = max(worst_rel, rel)
    if worst_rel > 0.05:
        return {"verdict": "BLOCK",
                "reason": "算术复核不一致：相对误差 %.1f%% 超过 5%% 容差" % (worst_rel * 100),
                "evidence": {"computed_W": computed, "claimed_W": claimed}}
    return {"verdict": "PASS", "reason": "队列时延数值复核一致", "evidence": {"computed_W": computed}}


def check_fixed_weight_action_switch(params: dict) -> dict:
    """反例检查：固定权重定价是否推出固定最优动作。

    模型：短路边传播 p_short + 短路队列 M/M/1(mu)；绕路边传播 p_detour、不排队。
    两边权重固定为 1（成本=传播+排队，权重不随负载变）。
    若存在 rho* 使 argmin 切换 → "固定权重 ⇒ 固定动作" 被击落 → BLOCK。
    """
    p_s = float(params.get("p_short", 2.0))
    p_d = float(params.get("p_detour", 5.0))
    mu = float(params.get("mu", 1.0))
    prev = None
    switch_rho = None
    for i in range(1000):
        rho = i / 1000.0
        c_s = p_s + mm1_wait(rho, mu)
        c_d = p_d
        cur = "S" if c_s <= c_d else "D"
        if prev is not None and cur != prev:
            switch_rho = rho
            break
        prev = cur
    if switch_rho is not None:
        return {"verdict": "BLOCK",
                "reason": "反例成立：权重全固定，最优动作仍在 rho*=%.3f 切换（固定权重≠固定行为）" % switch_rho,
                "evidence": {"switch_rho": switch_rho, "p_short": p_s, "p_detour": p_d, "mu": mu}}
    return {"verdict": "PASS", "reason": "给定参数下未出现动作切换", "evidence": {}}


def check_fallback_lossless(params: dict) -> dict:
    """"可退回基线 ⇒ 无损"完整性检查：必须给显著性与被丢弃经验分析。"""
    if params.get("claims_lossless"):
        if not params.get("significance_evidence"):
            return {"verdict": "BLOCK",
                    "reason": "可退回基线≠无损：缺显著性证据",
                    "evidence": {"evaluated_variants": params.get("evaluated_variants", [])}}
        if not params.get("dropped_experience_analysis"):
            return {"verdict": "BLOCK",
                    "reason": "可退回基线≠无损：未分析被丢弃/降权经验的影响",
                    "evidence": {}}
    return {"verdict": "PASS", "reason": "损失论证完备", "evidence": {}}


def check_correlation_causality(params: dict) -> dict:
    """相关≠因果：因果性断言必须有干预/判别实验设计。"""
    if params.get("causal_claim") and not params.get("intervention_design"):
        return {"verdict": "BLOCK",
                "reason": "仅有相关性证据（如表示相似度下降）不足以支撑因果断言，需要判别实验",
                "evidence": {"evidence_note": params.get("evidence_note", "")}}
    return {"verdict": "PASS", "reason": "因果断言有判别设计支撑", "evidence": {}}


def check_bounded_negative(params: dict) -> dict:
    """缺席性结论必须限定范围：'读到集合内未发现'可过；'无人做过'拦截。"""
    if params.get("claims_absolute"):
        return {"verdict": "BLOCK",
                "reason": "把限定范围的缺席性检索当成了领域空白",
                "evidence": {}}
    if not params.get("scope"):
        return {"verdict": "BLOCK",
                "reason": "缺席性结论缺范围限定",
                "evidence": {}}
    return {"verdict": "PASS", "reason": "有界否定，范围已限定", "evidence": {"scope": params["scope"]}}


def check_grid_completeness(params: dict) -> dict:
    """对照网格完备性：断言"学习优于静态"必须含最小动态简单臂。"""
    required = set(params.get("required_arms", []))
    provided = set(params.get("provided_arms", []))
    missing = sorted(required - provided)
    if missing:
        return {"verdict": "BLOCK",
                "reason": "对照网格缺臂: " + "、".join(missing),
                "evidence": {"missing": missing}}
    return {"verdict": "PASS", "reason": "对照网格完备", "evidence": {}}


CHECKS = {
    "queue_divergence": check_queue_divergence,
    "fixed_weight_action_switch": check_fixed_weight_action_switch,
    "fallback_lossless": check_fallback_lossless,
    "correlation_causality": check_correlation_causality,
    "bounded_negative": check_bounded_negative,
    "grid_completeness": check_grid_completeness,
}


def run_check(name: str, params: dict) -> dict:
    if name not in CHECKS:
        raise KeyError("unknown check: " + name)
    return CHECKS[name](params or {})
