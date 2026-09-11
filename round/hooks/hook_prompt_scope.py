#!/usr/bin/env python3
"""hook：派发提示词越界——【诊断件，非门禁】（2026-09-11 Codex 收口 #3 降级）。

降级理由（已核实）：
  - PreToolUse 载荷**不含角色字段**（实测 grep=0）：只有 session_id/cwd/tool_name/tool_input；
  - 此前用"提示词里出现历史审查者字样"作为豁免依据 → **可被任意提示词绕过**，
    不能作为授权依据，故不得宣称已实现角色隔离。

现在的定位：
  - 记录"提示词携带历史全集"这一事实，供主控事后审查（stderr 提示）；
  - **不阻塞**、不冒充授权判定；
  - 真正的隔离由 hook_access_guard（按角色+具体文件授权）承担。

诚实声明：本 hook **不提供角色隔离保证**。
"""
import os, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_hook import block, note, read_input

# Codex 要求 #5（2026-09-11）：历史审查**必须能被正常派发**。
# 此前一律禁止提示词出现 HISTORY-INDEX 等字样，导致"派历史审查任务"这一合法动作被拦。
# 现改为**按角色判定**：只有非历史审查角色才禁止携带历史全集。
HISTORY_ITEMS = [
    "HISTORY-INDEX",
    "ELIMINATED-REGISTER",
    "淘汰台账",
    "CANDIDATE-LEDGER",
    "run1/card-",
    "notes/raw/",
]
# 允许携带历史全集的任务类型标记（派发端在提示词中显式声明角色）
HISTORY_ROLE_MARKERS = [
    "历史碰撞审查", "历史审查者", "history_reviewer", "history reviewer",
    "role: history_reviewer", "角色：历史审查者",
]
FORBIDDEN_IN_PROMPT = HISTORY_ITEMS
DISPATCH_TOOLS = ("subagent", "subagent_fork", "subagent_codex")


def main() -> None:
    p = read_input()
    if p.get("_parse_error"):
        # 门禁类：解析失败保守阻塞（与 HOOKS-README 声明一致；Codex 收口 #3 指出旧版此处放行）
        block("hook 载荷无法解析：%s" % p["_parse_error"],
              "协议异常时拒绝放行；请检查 bridge 版本或载荷格式")
    tool = p.get("tool_name") or ""
    ti = p.get("tool_input") or {}
    blob = ""
    if tool in DISPATCH_TOOLS:
        blob = str(ti.get("prompt", ""))
    else:
        # run_code 里嵌的 tools.subagent({prompt: `...`})
        code = ti.get("code")
        if isinstance(code, str) and "subagent" in code:
            for m in re.finditer(r"prompt\s*:\s*`([^`]{0,20000})`", code):
                blob += m.group(1) + "\n"
            for m in re.finditer(r"prompt\s*:\s*\"((?:[^\"\\]|\\.){0,20000})\"", code):
                blob += m.group(1) + "\n"
    if not blob:
        sys.exit(0)
    # Codex 收口 #3（已核实载荷无角色字段）：本 hook 降级为**诊断**，不阻塞、不冒充授权。
    # 角色是否恰当由主控在派发时用 grant --role 明确记录，并由 hook_access_guard 按文件授权执行。
    hits = [f for f in FORBIDDEN_IN_PROMPT if f in blob]
    if hits:
        note("诊断（不阻塞）：派发提示词携带历史全集字样 [%s] —— 请确认目标角色为 history_reviewer；"
             "本 hook 无角色记录，不构成授权判定。" % ", ".join(hits))
    sys.exit(0)


if __name__ == "__main__":
    main()