#!/usr/bin/env python3
"""hook：角色化访问守卫（PreToolUse）。

强制级别（诚实分级，见 HOOK-CONTRACT.md §3）：
  【可强制】read/write/edit/glob/grep 等工具的结构化路径参数 —— 按角色授权表判定；
  【尽力检测】bash / run_code 内的任意命令与代码 —— 只做字面路径匹配，
               **不构成硬隔离**（任意 shell/Python 可绕过），仅作预警与常见路径拦截。

身份来源：载荷 session_id → 权限清单（perm.py）。不使用任何环境变量判定身份。
未登记会话：放行但记录（避免误伤无关会话），由 perm.py audit 事后核对。
"""
import json, os, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_hook import (EXTERNAL_DENY_SUBSTR, READ_TOOLS, WRITE_TOOLS, block, find_worktree,
                      glob_match, grants_for, load_perms, log_unregistered, normalize,
                      read_input, resolve_role, tool_paths)

SHELL_TOOLS = {"bash", "shell", "run_code"}
# 尽力检测：命令/代码里出现的"像路径"的字符串（含引号内、heredoc 内）
PATHLIKE = re.compile(r"[A-Za-z0-9_./\-]*\.(?:md|csv|json|pdf|txt|py)\b|(?:round|LITERATURE|ANALYSIS|tao25\.pdf)[A-Za-z0-9_./\-]*")


def check_path(kind: str, val: str, grants: dict, tool: str, session: str) -> None:
    if kind == "empty":
        return
    if kind == "external":
        for sub in EXTERNAL_DENY_SUBSTR:
            if sub in val:
                block("访问工作区外的高危目标（%s）" % sub,
                      "跨会话/跨代理读取等同绕过隔离；需要该信息请由主控转述")
        return
    if tool in READ_TOOLS or (tool in SHELL_TOOLS and False):
        if not any(glob_match(g, val) for g in grants["read"]):
            block("角色不允许读取：%s（工具 %s）" % (val, tool),
                  "当前角色的可读范围见 perm.py grants；需要更多材料请让主控用 --extra-read 追加授权")
    if tool in WRITE_TOOLS:
        if not any(glob_match(g, val) for g in grants["write"]):
            block("角色不允许写入：%s（工具 %s）" % (val, tool),
                  "只允许写自己的产出；需要更多写权限请让主控用 --extra-write 追加授权")


def best_effort_shell(tool: str, ti: dict, grants: dict, cwd: str, wt, session: str) -> None:
    """尽力检测：从命令/代码里抽出字面路径，按同一授权表判定。"""
    blob = ""
    if isinstance(ti, dict):
        blob = " ".join(str(ti.get(k, "")) for k in ("command", "code", "script"))
    if not blob:
        return
    seen = set()
    for m in PATHLIKE.finditer(blob):
        cand = m.group(0)
        if cand in seen or len(cand) < 4:
            continue
        seen.add(cand)
        kind, val = normalize(cand, cwd, wt)
        if kind != "worktree":
            if kind == "external":
                for sub in EXTERNAL_DENY_SUBSTR:
                    if sub in val:
                        block("命令涉及工作区外高危目标（%s）" % sub, "同上：由主控转述所需信息")
            continue
        if not any(glob_match(g, val) for g in grants["read"]) and \
           not any(glob_match(g, val) for g in grants["write"]):
            block("命令字面涉及未授权路径：%s" % val,
                  "注意：这是【尽力检测】，不是硬隔离——请只用授权范围内的路径；确需越界由主控追加授权")


def main() -> None:
    p = read_input()
    if p.get("_parse_error"):
        # 门禁类 hook：解析失败保守阻塞（与声明一致）
        block("hook 载荷无法解析：%s" % p["_parse_error"],
              "协议异常时拒绝放行；请检查 bridge 版本或载荷格式")
    session = p.get("session_id") or ""
    tool = p.get("tool_name") or ""
    ti = p.get("tool_input") or {}
    cwd = p.get("cwd") or os.getcwd()

    if not session:
        block("载荷缺少 session_id，无法判定角色（拒绝在无法判定时放行）")

    role, entry = resolve_role(session)
    if role == "orchestrator":
        sys.exit(0)
    if role == "unknown":
        log_unregistered(session, tool, json.dumps(ti, ensure_ascii=False)[:180])
        sys.exit(0)

    grants = grants_for(role, entry)
    wt = find_worktree(cwd)

    for raw in tool_paths(tool, ti):
        kind, val = normalize(raw, cwd, wt)
        check_path(kind, val, grants, tool, session)

    if tool in SHELL_TOOLS:
        best_effort_shell(tool, ti, grants, cwd, wt, session)
    sys.exit(0)


if __name__ == "__main__":
    main()