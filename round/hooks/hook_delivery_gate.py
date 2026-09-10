#!/usr/bin/env python3
"""hook #3：交付门槛（PreToolUse）。

拦截"把未过闸的卡写进交付物"：
  - 写 MAIN-REPORT / PROPOSAL / TRADEOFF-LOG / LITERATURE-GUIDE 时，
    必须存在对应的闸门判定表（round/run2/gates/<cand_id>.md）且非 BLOCK；
  - 否则 exit 2，要求先跑 gate_check.py 并补表。

这补的是"推荐必须附闸门判定表"这条软规则的硬约束。
"""
import json, os, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_hook import block, read_input

DELIVER = re.compile(r"(MAIN-REPORT|PROPOSAL|TRADEOFF-LOG|LITERATURE-GUIDE|run2/DELIVERY)\.md$")
GATE_DIR = "round/run2/gates"


def find_worktree(cwd: str) -> Path | None:
    for base in (cwd, os.getcwd()):
        p = Path(base)
        for cand in (p, *p.parents):
            if (cand / "round" / "rules").is_dir():
                return cand
    return None


def main() -> None:
    p = read_input()
    if p.get("_parse_error"):
        sys.exit(0)
    # 放行规则（修正版）：只有在"明确标识为子代理"时才约束。
    # 判据优先级：① 显式声明编排者 → 放行；② 环境变量 DSH_SUBAGENT_ID 非空 → 视为子代理；
    # ③ 否则放行（主会话）。注意：payload 里的 agent_id 在部分桥接中是"当前会话 ID"，
    # 不能作为子代理判据——自测用例 9 曾因此把主控误拦。
    if os.environ.get("DSH_HOOK_ORCHESTRATOR") == "1":
        sys.exit(0)
    if not os.environ.get("DSH_SUBAGENT_ID"):
        sys.exit(0)
    ti = p.get("tool_input") or {}
    target = ti.get("file_path") or ti.get("path") or ""
    if not isinstance(target, str) or not DELIVER.search(target):
        sys.exit(0)

    wt = find_worktree(p.get("cwd") or "")
    if wt is None:
        block("无法定位 worktree（含 round/rules 的目录）", "确认 cwd 或在该 worktree 内产出交付物")
    gates = wt / GATE_DIR
    tables = list(gates.glob("*.md")) if gates.is_dir() else []
    real = [t for t in tables if t.name != "GATE-TEMPLATE.md"]
    if not real:
        block(
            "准备写入交付物 %s，但 %s 下没有任何闸门判定表" % (Path(target).name, GATE_DIR),
            "先用 round/tools/gate_check.py 逐卡判定，并按 round/run2/gates/GATE-TEMPLATE.md 落表；无表不得交付",
        )
    bad = []
    for t in real:
        txt = t.read_text(encoding="utf-8", errors="ignore")
        if "VERDICT: BLOCK" in txt or "判定：BLOCK" in txt:
            bad.append(t.name)
    if bad:
        block(
            "存在判定为 BLOCK 的闸门表：%s —— 该卡不得进入交付" % ", ".join(bad),
            "消除致命项并重跑 gate_check.py；或将该卡移入淘汰台账",
        )
    sys.exit(0)


if __name__ == "__main__":
    main()