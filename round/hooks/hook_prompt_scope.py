#!/usr/bin/env python3
"""hook #4：深化者提示词越界（PreToolUse）。

拦截"派发子代理时把历史全集塞进提示词"：
  - 派发者的 prompt 里出现 HISTORY-INDEX / ELIMINATED-REGISTER / 淘汰台账 / 其他卡全文 → exit 2；
  - 允许出现"本卡 must-address 反馈文件路径"。

这补的是"深化者不得拿历史全集（否则等于把污染从生成端搬到深化端）"这条规则。
"""
import os, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_hook import block, read_input

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
    # 历史审查角色豁免：其职责就是读历史库（否则任务无法派发）
    if any(mk in blob for mk in HISTORY_ROLE_MARKERS):
        sys.exit(0)
    hits = [f for f in FORBIDDEN_IN_PROMPT if f in blob]
    if hits:
        block(
            "派发子代理的提示词里出现历史全集内容：%s" % ", ".join(hits),
            "深化者只能收到本卡的有限死因反馈（round/run2/feedback/<卡ID>.md）；历史全集会诱导照旧题改",
        )
    sys.exit(0)


if __name__ == "__main__":
    main()