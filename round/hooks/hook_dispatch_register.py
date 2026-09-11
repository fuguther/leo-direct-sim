#!/usr/bin/env python3
"""hook：派发登记强制（PostToolUse，subagent 类工具）。

机制：主控每次 dispatch 子代理后，返回的 subagentId（= 子会话 session_id）必须登记进权限清单；
未登记的子代理，其工具调用会落入"未登记会话"分支（放行但记录）＝ 隔离失效。
本 hook 在派发返回后立即校验并强制要求补登记。

诚实边界：PostToolUse 无法撤销已发生的派发；它的作用是**立刻暴露漏登记**（exit 2 + 明确指令），
而不是假装自动完成登记。
"""
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_hook import block, load_perms, note, read_input

DISPATCH = ("subagent", "subagent_fork", "subagent_codex")
UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


def main() -> None:
    p = read_input()
    if p.get("_parse_error"):
        note("派发登记校验：载荷无法解析，跳过")
        sys.exit(0)
    tool = p.get("tool_name") or ""
    ti = p.get("tool_input") or {}
    is_dispatch = tool in DISPATCH
    if not is_dispatch and isinstance(ti, dict):
        code = ti.get("code")
        if isinstance(code, str) and re.search(r"tools\.(subagent|subagent_fork|subagent_codex)\s*\(", code):
            is_dispatch = True
    if not is_dispatch:
        sys.exit(0)
    resp = p.get("tool_response")
    s = json.dumps(resp, ensure_ascii=False) if isinstance(resp, (dict, list)) else str(resp or "")
    ids = UUID.findall(s)
    if not ids:
        note("派发登记校验：本次返回值未含 subagentId；若已派发子代理，请手工 perm.py bind 并自查")
        sys.exit(0)
    perms = load_perms()
    bound = set((perms.get("sessions") or {}).keys())
    orch = perms.get("orchestrator_session")
    missing = [i for i in ids if i not in bound and i != orch]
    if missing:
        block("派发后未登记权限角色：" + ", ".join(missing),
              "立即执行 python3 round/hooks/perm.py bind --session <id> --role <角色> [--extra-read P] [--extra-write P]；未登记子代理不受访问约束")
    sys.exit(0)


if __name__ == "__main__":
    main()