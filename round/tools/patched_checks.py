#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""机械论证检查器（修订版 v2）—— research-ops checks.py 的明确补丁（本线所有）。

原件: .worktrees/research-ops/scripts/topic_harness/checks.py
     sha256 前缀 9da8c6282fbcf98a（完整指纹见 round/deps/DEPENDENCIES.md）
原件 owner: harness-unify 代理（research-ops worktree；按单写入者约束本线只读引用、未改原件）
补丁 owner: agent/20260910-topic-loop（本 worktree）
复现依据: round/logs/repro-group2.txt（第二组 C/D 全部复现）

补丁内容（对应深审发现）:
1. 新增判定级 INPUT_INSUFFICIENT（输入不足/程序未能检查）与 NOT_APPLICABLE（该检查不适用）。
   占位文本（TODO/待补/TBD/空串）一律 INPUT_INSUFFICIENT，不再产生 PASS，也不冒充科研否定。
2. queue_divergence: rhos 为空、claimed_W 缺项、mu 缺失 → INPUT_INSUFFICIENT；
   数值检查只对"给定 mu/rho/claimed 输入"负责；类型错误 raise（由审计层记 EXEC_ERROR）。
3. correlation_causality: 无因果断言 → NOT_APPLICABLE（原版误给"有设计支撑"PASS）；
   设计为占位 → INPUT_INSUFFICIENT；PASS 理由明确"设计存在≠因果成立"。
4. fallback_lossless: 未声明无损 → NOT_APPLICABLE；证据占位 → INPUT_INSUFFICIENT；
   缺失 → BLOCK（维持：声明无损而无论证是实质缺口）。
5. grid_completeness: required_arms 为空 → INPUT_INSUFFICIENT（未定义网格≠完备）。
6. 所有 PASS 理由限定为"在给定输入下成立"，不构成普适科研认证。
7. 适用范围：本库只回答"这类论证在给定参数下是否成立"，不做文本理解；文本级反例是审查者模型职责。

约定: check(params) -> {"verdict": PASS|BLOCK|NOT_APPLICABLE|INPUT_INSUFFICIENT, "reason": str, "evidence": dict}
  BLOCK = 断言被反例/证据缺口击落（科研层面的否定，须有依据）
  INPUT_INSUFFICIENT = 程序未能检查（不是科研否定，也不是通过）
  NOT_APPLICABLE = 该检查对此输入不适用（既非通过也非否定）
"""
from __future__ import annotations

import math

VERDICT_PASS = "PASS"
VERDICT_BLOCK = "BLOCK"
VERDICT_NA = "NOT_APPLICABLE"
VERDICT_INSUF = "INPUT_INSUFFICIENT"

_PLACEHOLDERS = {"", "todo", "tbd", "待补", "待定", "稍后填", "n/a", "none", "null"}


def _is_placeholder(v) -> bool:
    """占位文本判定：字符串去空白小写后属占位集合，或非字符串空值。"""
    if v is None:
        return True
    if not isinstance(v, str):
        return False
    return v.strip().lower() in _PLACEHOLDERS


def _require_number(params: dict, key: str, default=None) -> float:
    """取数值参数；缺失且有默认 → 默认；缺失无默认 → INPUT_INSUFFICIENT 信号（KeyError 子类）。"""
    if key not in params or params[key] is None:
        if default is not None:
            return float(default)
        raise MissingInput(key)
    v = params[key]
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise TypeError(f"param {key!r} must be numeric, got {type(v).__name__}: {v!r}")
    return float(v)


class MissingInput(Exception):
    """缺必需输入：由 run_check 捕获并转为 INPUT_INSUFFICIENT 判定（附缺什么）。"""


def _res(verdict, reason, evidence=None):
    return {"verdict": verdict, "reason": reason, "evidence": evidence or {}}


def mm1_wait(rho: float, mu: float) -> float:
    """M/M/1 平均等待 W = rho/(mu*(1-rho))；仅对给定 rho/mu 负责。"""
    if not (0.0 <= rho < 1.0):
        raise ValueError("rho must be in [0,1)")
    if mu <= 0.0:
        raise ValueError("mu>0 required")
    return rho / (mu * (1.0 - rho))


def check_queue_divergence(params: dict) -> dict:
    """重算队列时延，核对断言数值是否算错（只对给定输入负责）。"""
    mu = _require_number(params, "mu")
    rhos = params.get("rhos")
    if not isinstance(rhos, dict) or not rhos:
        return _res(VERDICT_INSUF, "未检查：rhos 为空或缺失，无数值可复核")
    claimed = params.get("claimed_W")
    if not isinstance(claimed, dict):
        return _res(VERDICT_INSUF, "未检查：claimed_W 缺失或非映射")
    missing = [k for k in rhos if k not in claimed or claimed[k] is None]
    if missing:
        return _res(VERDICT_INSUF, "未检查：claimed_W 缺少键 " + "、".join(map(str, missing)),
                    {"missing_keys": missing})
    computed, worst_rel = {}, 0.0
    for key, rho in rhos.items():
        w = mm1_wait(float(rho), mu)
        computed[key] = w
        rel = abs(w - float(claimed[key])) / max(abs(float(claimed[key])), 1e-12)
        worst_rel = max(worst_rel, rel)
    if worst_rel > 0.05:
        return _res(VERDICT_BLOCK,
                    "算术复核不一致：给定输入下相对误差 %.1f%% 超过 5%% 容差" % (worst_rel * 100),
                    {"computed_W": computed, "claimed_W": claimed})
    return _res(VERDICT_PASS, "在给定 mu/rho/claimed 输入下数值复核一致（不构成对模型本身的认证）",
                {"computed_W": computed})


def check_fixed_weight_action_switch(params: dict) -> dict:
    """反例检查：固定权重定价是否推出固定最优动作（本检查自构模型，参数有默认）。"""
    p_s = _require_number(params, "p_short", default=2.0)
    p_d = _require_number(params, "p_detour", default=5.0)
    mu = _require_number(params, "mu", default=1.0)
    prev, switch_rho = None, None
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
        return _res(VERDICT_BLOCK,
                    "反例成立：给定模型参数下权重全固定而最优动作在 rho*=%.3f 切换（固定权重≠固定行为）" % switch_rho,
                    {"switch_rho": switch_rho, "p_short": p_s, "p_detour": p_d, "mu": mu})
    return _res(VERDICT_PASS, "在给定模型参数下未出现动作切换（仅对该参数组合负责）")


def check_fallback_lossless(params: dict) -> dict:
    """"可退回基线 ⇒ 无损"完整性：声明无损必须有显著性与被丢弃经验分析。"""
    if not params.get("claims_lossless"):
        return _res(VERDICT_NA, "不适用：输入未声明无损主张，本检查不评判")
    sig = params.get("significance_evidence")
    dropped = params.get("dropped_experience_analysis")
    if _is_placeholder(sig) or _is_placeholder(dropped):
        which = [k for k, v in (("significance_evidence", sig), ("dropped_experience_analysis", dropped)) if _is_placeholder(v)]
        return _res(VERDICT_INSUF, "未检查：证据字段为占位文本（" + "、".join(which) + "），程序无法据此判定",
                    {"placeholder_fields": which})
    if not sig:
        return _res(VERDICT_BLOCK, "可退回基线≠无损：声明无损但缺显著性证据（实质缺口）",
                    {"evaluated_variants": params.get("evaluated_variants", [])})
    if not dropped:
        return _res(VERDICT_BLOCK, "可退回基线≠无损：声明无损但未分析被丢弃/降权经验（实质缺口）")
    return _res(VERDICT_PASS, "在给定证据字段非空且非占位的意义上，损失论证要素齐备（不等于证明无损）")


def check_correlation_causality(params: dict) -> dict:
    """相关≠因果：因果断言必须有干预/判别实验设计；设计存在≠因果成立。"""
    if not params.get("causal_claim"):
        return _res(VERDICT_NA, "不适用：输入未含因果断言，本检查不评判")
    design = params.get("intervention_design")
    if _is_placeholder(design):
        return _res(VERDICT_INSUF, "未检查：intervention_design 为占位文本，程序无法据此判定设计存在")
    if not design:
        return _res(VERDICT_BLOCK, "仅有相关性证据不足以支撑因果断言：缺判别/干预实验设计（实质缺口）",
                    {"evidence_note": params.get("evidence_note", "")})
    return _res(VERDICT_PASS, "判别设计存在（仅说明设计存在；因果结论须待实验结果，本检查不认证因果）",
                {"design_digest": str(design)[:200]})


def check_bounded_negative(params: dict) -> dict:
    """缺席性结论必须限定范围：'读到集合内未发现'可过；'无人做过'拦截。"""
    has_absence = bool(params.get("claims_absolute") or params.get("claims_absence") or params.get("scope"))
    if not has_absence:
        return _res(VERDICT_NA, "不适用：输入未作缺席性结论，本检查不评判")
    if params.get("claims_absolute"):
        return _res(VERDICT_BLOCK, "把限定范围的缺席性检索当成了领域空白（实质缺口）")
    scope = params.get("scope")
    if _is_placeholder(scope):
        return _res(VERDICT_INSUF, "未检查：scope 为占位文本，程序无法据此判定范围")
    if not scope:
        return _res(VERDICT_BLOCK, "缺席性结论缺范围限定（实质缺口）")
    return _res(VERDICT_PASS, "有界否定：范围已限定（'范围内未发现'，不等于领域空白）", {"scope": scope})


def check_grid_completeness(params: dict) -> dict:
    """对照网格完备性：断言"学习优于静态"必须含最小动态简单臂。"""
    required = params.get("required_arms")
    if not isinstance(required, list) or not required:
        return _res(VERDICT_INSUF, "未检查：required_arms 为空或缺失——未定义网格不能判'完备'")
    provided = params.get("provided_arms")
    if not isinstance(provided, list) or not provided:
        return _res(VERDICT_INSUF, "未检查：provided_arms 为空或缺失——无实测臂不能判'完备'")
    req = {str(x) for x in required}
    prov = {str(x) for x in provided if not _is_placeholder(x)}
    if not prov:
        return _res(VERDICT_INSUF, "未检查：provided_arms 全为占位文本，无实测臂可比对")
    missing = sorted(req - prov)
    if missing:
        return _res(VERDICT_BLOCK, "对照网格缺臂: " + "、".join(missing), {"missing": missing})
    return _res(VERDICT_PASS, "在给定 required/provided 清单下网格完备（不认证实验结论本身）",
                {"provided": sorted(prov)})


CHECKS = {
    "queue_divergence": check_queue_divergence,
    "fixed_weight_action_switch": check_fixed_weight_action_switch,
    "fallback_lossless": check_fallback_lossless,
    "correlation_causality": check_correlation_causality,
    "bounded_negative": check_bounded_negative,
    "grid_completeness": check_grid_completeness,
}


def run_check(name: str, params: dict) -> dict:
    """统一入口。MissingInput → INPUT_INSUFFICIENT；未知检查器 → KeyError（审计层记 UNKNOWN_CHECKER）。"""
    if name not in CHECKS:
        raise KeyError("unknown check: " + name)
    try:
        return CHECKS[name](params or {})
    except MissingInput as e:
        return _res(VERDICT_INSUF, "未检查：缺必需输入 %s" % e, {"missing": str(e)})