#!/usr/bin/env python3
"""hook #1：黑名单访问拦截（PreToolUse）。

拦截对象：任何对黑名单路径的**读取、列目录、写入**（含 run_code 里嵌的工具调用）。
依据：EFFECTIVE-RULES-R2 §8.1 隔离矩阵。

设计原则（避免误伤）：
  - 只判"路径参数位"与"命令模式"，不判 content/code 正文（正文里写路径名不违规）；
  - 对主控/审查者角色不作区分——本 hook 只拦"生成器/深化者/审查者"子会话；
    判据：环境变量 DSH_SUBAGENT_ROLE 或 session_id 是否在允许清单（见 is_privileged）。
  - 主会话（编排者本人）放行——否则主控无法管理这些文件。
"""
import os, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_hook import (BLACKLIST_CMD, block, extract_targets, is_blacklisted, read_input)


def is_privileged(payload: dict) -> bool:
    """主控会话放行：靠环境变量声明（挂载时由 profile 注入主会话标记）。"""
    if os.environ.get("DSH_HOOK_ORCHESTRATOR") == "1":
        return True
    # 只有"明确标识为子代理"才约束：payload 的 agent_id 在部分桥接中是当前会话 ID，
    # 不能作为子代理判据（自测用例 9 曾因此把主控误拦）。
    return not bool(os.environ.get("DSH_SUBAGENT_ID"))


def main() -> None:
    payload = read_input()
    if payload.get("_parse_error"):
        block("hook 输入无法解析（协议异常）", "检查 bridge 版本；本 hook 拒绝在无法判定的情况下放行")
    if is_privileged(payload):
        sys.exit(0)

    tool = payload.get("tool_name") or payload.get("tool") or ""
    ti = payload.get("tool_input") or payload.get("arguments") or {}
    cwd = payload.get("cwd") or os.getcwd()

    # write/edit 的目标也拦（防止把候选内容写进黑名单区）
    for t in extract_targets(tool, ti):
        if t.startswith("__CMD__"):
            cmd = t[len("__CMD__"):]
            m = BLACKLIST_CMD.search(cmd)
            if m:
                block(
                    "命令试图访问黑名单区域：%s" % m.group(0)[:120],
                    "黑名单路径见 EFFECTIVE-RULES-R2 §8.1；列目录（ls/find/glob）同样违规",
                )
            continue
        why = is_blacklisted(t, cwd)
        if why:
            block(
                "%s（目标：%s）" % (why, t[:160]),
                "若确需该文件，请由主控（编排者）读取后以中性事实形式转述；生成端不得直接接触历史候选与淘汰理由",
            )
    sys.exit(0)


if __name__ == "__main__":
    main()