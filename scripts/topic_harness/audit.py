#!/usr/bin/env python3
"""审查测试集运行器：用已知对错论证校准机械检查器。

用法：PYTHONPATH=. python3 -m scripts.topic_harness.audit [cases_dir]
验收合同（批评文第 6 节）：三项已知错误必须全拦（误放=0），成立论证不得误杀（误杀=0）。
检查器异常按 fail-loud 处理：记 BLOCK 并在 reason 里暴露异常。
"""
from __future__ import annotations

import glob
import json
import os
import sys

from scripts.topic_harness import checks

DEFAULT_CASES = "scripts/topic_harness/testset"


def audit_dir(cases_dir: str) -> dict:
    results = []
    for path in sorted(glob.glob(os.path.join(cases_dir, "*.json"))):
        with open(path, encoding="utf-8") as f:
            case = json.load(f)
        try:
            out = checks.run_check(case["check"], case.get("params", {}))
            verdict = out["verdict"]
            reason = out["reason"]
        except Exception as exc:  # fail-loud：异常显式暴露，不静默放行
            verdict = "BLOCK"
            reason = "checker error: %r" % (exc,)
        expected = case["expected_verdict"]
        if expected == "PASS" and verdict == "BLOCK":
            kind = "误杀"
        elif expected == "BLOCK" and verdict == "PASS":
            kind = "误放"
        else:
            kind = "正确"
        results.append({
            "case": case["id"],
            "check": case["check"],
            "expected": expected,
            "verdict": verdict,
            "ok": verdict == expected,
            "kind": kind,
            "reason": reason,
            "origin": case.get("origin", ""),
        })
    return {
        "results": results,
        "false_release": sum(1 for r in results if r["kind"] == "误放"),
        "false_kill": sum(1 for r in results if r["kind"] == "误杀"),
        "all_ok": all(r["ok"] for r in results) and bool(results),
    }


def main(argv: list) -> int:
    cases_dir = argv[1] if len(argv) > 1 else DEFAULT_CASES
    rep = audit_dir(cases_dir)
    for r in rep["results"]:
        mark = "OK " if r["ok"] else "XX "
        print(mark, r["case"], "| 期望", r["expected"], "-> 判", r["verdict"], "|", r["reason"][:90])
    print("误放:", rep["false_release"], "| 误杀:", rep["false_kill"], "| 用例数:", len(rep["results"]))
    return 0 if rep["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
