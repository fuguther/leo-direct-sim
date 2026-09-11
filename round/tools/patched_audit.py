#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""审查测试集运行器（修订版 v2）—— research-ops audit.py 的明确补丁（本线所有）。

原件: .worktrees/research-ops/scripts/topic_harness/audit.py
     sha256 前缀 926d5f2586067b07（完整指纹见 round/deps/DEPENDENCIES.md）
原件 owner: harness-unify 代理（按单写入者约束本线只读引用、未改原件）
补丁 owner: agent/20260910-topic-loop
复现依据: round/logs/repro-group2.txt §C（checker 异常/未知检查器在 expected=BLOCK 时被判"正确"，
all_ok=True——原 docstring 自称 fail-loud，实际 fail-into-pass）

补丁内容:
1. 执行结果分五类记账：correct / false_release(误放) / false_kill(误杀) / EXEC_ERROR / UNKNOWN_CHECKER / PARAM_ERROR。
2. all_ok 收紧：必须 无误放 & 无误杀 & 零执行错误 & 用例非空。ERROR 类永不计"正确"。
3. INPUT_INSUFFICIENT / NOT_APPLICABLE 在审计夹具上出现视为夹具缺陷（verdict 与 expected 不匹配 → all_ok=False），
   单独计数便于定位；不影响对真实候选卡使用检查器时的语义。
4. 区分"程序未能检查"（EXEC_ERROR/INPUT_INSUFFICIENT）与"确实找到反例"（BLOCK）。
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patched_checks as checks

DEFAULT_CASES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit_cases")


def run_audit(cases_dir: str) -> dict:
    results = []
    for path in sorted(os.listdir(cases_dir)):
        if not path.endswith(".json"):
            continue
        case = json.load(open(os.path.join(cases_dir, path), encoding="utf-8"))
        expected = case["expected_verdict"]
        category = "correct"
        try:
            out = checks.run_check(case["check"], case.get("params", {}))
            verdict, reason = out["verdict"], out["reason"]
            if verdict == checks.VERDICT_INSUF:
                category = "input_insufficient"
            elif verdict == checks.VERDICT_NA:
                category = "not_applicable"
        except KeyError as exc:
            verdict, reason, category = "ERROR", "unknown checker: %r" % (exc,), "unknown_checker"
        except (TypeError, ValueError) as exc:
            verdict, reason, category = "ERROR", "param error: %r" % (exc,), "param_error"
        except Exception as exc:  # 执行错误独立报告，绝不计作正确
            verdict, reason, category = "ERROR", "checker error: %r" % (exc,), "exec_error"
        if category == "correct":
            if expected == "PASS" and verdict == "BLOCK":
                category = "false_kill"
            elif expected == "BLOCK" and verdict == "PASS":
                category = "false_release"
        ok = (category == "correct")
        results.append({
            "case": case["id"], "check": case["check"], "expected": expected,
            "verdict": verdict, "ok": ok, "category": category, "reason": reason,
            "origin": case.get("origin", ""),
        })
    def cnt(kind):
        return sum(1 for r in results if r["category"] == kind)
    return {
        "results": results,
        "false_release": cnt("false_release"),
        "false_kill": cnt("false_kill"),
        "exec_errors": cnt("exec_error"),
        "unknown_checkers": cnt("unknown_checker"),
        "param_errors": cnt("param_error"),
        "input_insufficient": cnt("input_insufficient"),
        "not_applicable": cnt("not_applicable"),
        "all_ok": bool(results) and all(r["ok"] for r in results),
    }


def main(argv: list) -> int:
    cases_dir = argv[1] if len(argv) > 1 else DEFAULT_CASES
    rep = run_audit(cases_dir)
    for r in rep["results"]:
        mark = "OK " if r["ok"] else "XX "
        print(mark, r["case"], "| 期望", r["expected"], "-> 判", r["verdict"], "|", r["category"], "|", r["reason"][:80])
    print("误放:", rep["false_release"], "| 误杀:", rep["false_kill"],
          "| 执行错误:", rep["exec_errors"], "| 未知检查器:", rep["unknown_checkers"],
          "| 参数错误:", rep["param_errors"], "| 输入不足:", rep["input_insufficient"],
          "| 不适用:", rep["not_applicable"], "| 用例数:", len(rep["results"]))
    return 0 if rep["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
