#!/usr/bin/env python3
"""hook：角色化访问守卫（PreToolUse）—— v4（路径判定版）。

v3 → v4 的关键修正：
  实测发现子代理 session cwd = 主仓库（不是本 worktree），按 cwd 判定"是否研究会话"会漏判；
  现改为**按访问路径判定**：受控研究区 = 本 hook 所在 worktree（HOOK_WORKTREE 固定）。

规则：
  - 主控（清单中的 orchestrator）：全权；
  - 已登记角色：按授权表校验其访问的**研究区路径**；
  - 未登记（无票据）：只要访问到研究区路径 → 暂停并报告；只访问区外 → 放行并记录；
  - 权限清单 missing/corrupt：研究会话失败关闭；主控凭 orchestrator.id 可修复。

强制级别：【可强制】结构化路径参数；【尽力检测】bash/run_code 内任意代码。
"""
import json, os, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib_hook as L
from lib_hook import (EXTERNAL_DENY_SUBSTR, HOOK_WORKTREE, READ_TOOLS, WRITE_TOOLS, block,
                      glob_match, grants_for, in_worktree, log_unregistered, normalize,
                      read_input, resolve_role, tool_paths)

SHELL_TOOLS = {"bash", "shell", "run_code"}
# 只抽取两类候选，避免把路径中间段（如裸 "round"）当成访问目标而误拦：
#   A) 具体文件：带已知扩展名
#   B) 敏感目录：历史/候选/暂存等（列目录本身即泄漏）
PATHLIKE = re.compile(r"[A-Za-z0-9_./\-]*\.(?:md|csv|json|pdf|txt|py)\b")
# 目录列举即视为访问的敏感目录（相对 HOOK_WORKTREE 的路径前缀）
SENSITIVE_DIRS = (
    "round/history", "round/run1", "round/reviews", "round/run2/staging",
    "round/run2/feedback", "round/run2/cards", "round/run2/gates",
    "round/knowledge/notes-neutral", "LITERATURE/notes/raw", "ANALYSIS",
    "round/hooks", "round/CANDIDATE-LEDGER.csv", "round/ROUND-LOG.md",
)
DIRLIKE = re.compile(r"(?:[A-Za-z0-9_./\-]*/)?(round|LITERATURE|ANALYSIS)[A-Za-z0-9_./\-]*")
HINT_UNREG = "已暂停本次操作。请主控执行 perm.py reserve --role <角色> --count N 预留票据，或 perm.py bind --session <id> --role <角色> --extra-read/--extra-write <具体文件> 后重试。"


def collect(payload_tool, ti, cwd):
    """收集本次访问涉及的路径。

    Codex 要求 #5（2026-09-11 修复）：
      - 可强制部分只取**工具的结构化路径参数**（file_path/path/target/notebook_path）；
      - 任意 shell 代码做字面量匹配，**仅作尽力检测**；
        不再使用"路径存在"启发式（既漏又误），也不把文本里的文件名当成访问。
      - bash 的 workdir 作为相对路径基准（此前用 session cwd 会漏判）。
    """
    out = []
    for raw in tool_paths(payload_tool, ti):
        kind, val = normalize(raw, cwd, HOOK_WORKTREE)
        out.append((kind, val, "param"))
    if payload_tool in SHELL_TOOLS and isinstance(ti, dict):
        base = ti.get("workdir") or cwd
        shell_cwd = base if isinstance(base, str) and base else cwd
        blob = " ".join(str(ti.get(k, "")) for k in ("command", "code", "script"))

        def dual_base(seg):
            """字面量在两个基准下解析；任一落入研究区即取之（解决 cwd=主仓库的漏判）。"""
            first = None
            for cand_base in (shell_cwd, str(HOOK_WORKTREE)):
                k2, v2 = normalize(seg, cand_base, HOOK_WORKTREE)
                if k2 == "worktree":
                    return (k2, v2)
                if first is None:
                    first = (k2, v2)
            return first or ("empty", "")

        seen = set()
        for m in PATHLIKE.finditer(blob):
            c = m.group(0)
            if c in seen or len(c) < 4:
                continue
            seen.add(c)
            kind, val = dual_base(c)
            if kind != "empty":
                out.append((kind, val, "shell-file"))
        for m in DIRLIKE.finditer(blob):
            seg = m.group(0).rstrip("/")
            if seg in seen or len(seg) < 4:
                continue
            seen.add(seg)
            kind, val = dual_base(seg)
            if kind == "worktree" and any(val == d or val.startswith(d + "/") or val.startswith(d) for d in SENSITIVE_DIRS):
                out.append(("worktree", val, "shell-dir"))
    return out


def main():
    p = read_input()
    if p.get("_parse_error"):
        block("hook 载荷无法解析：%s" % p["_parse_error"], "协议异常时拒绝放行")
    session = p.get("session_id") or ""
    tool = p.get("tool_name") or ""
    ti = p.get("tool_input") or {}
    cwd = p.get("cwd") or ""
    if not session:
        block("载荷缺少 session_id，无法判定角色（拒绝在无法判定时放行）")

    targets = collect(tool, ti, cwd)
    # 修复（实测）：normalize() 已把研究区内路径归一化为**相对路径**，
    # 再对其调用 in_worktree() 会以 hook 进程 cwd 解析而误判为区外 → 漏拦。
    # 正确判据：kind == "worktree" 本身即表示 realpath 落在 HOOK_WORKTREE 内。
    research_touch = [(k, v, s) for (k, v, s) in targets if k == "worktree"]
    external_touch = [(k, v, s) for (k, v, s) in targets if k == "external"]

    role, entry, why = resolve_role(session, HOOK_WORKTREE)

    if role == "orchestrator":
        sys.exit(0)

    if role == "unknown":
        if research_touch:
            log_unregistered(session, tool, "BLOCKED(%s): %s" % (why, research_touch[0][1]))
            block("本研究运行中的会话身份/权限异常（%s）：试图访问研究区文件 %s"
                  % (why, research_touch[0][1]), HINT_UNREG)
        log_unregistered(session, tool, "allowed-outside: " + json.dumps(ti, ensure_ascii=False)[:150])
        sys.exit(0)

    grants = grants_for(role, entry)
    # 区外高危目标
    for kind, val, _src in external_touch:
        for sub in EXTERNAL_DENY_SUBSTR:
            if sub in val:
                block("访问工作区外的高危目标（%s）" % sub, "跨会话/跨代理读取等同绕过隔离；需要该信息请由主控转述")
    for kind, val, src in research_touch:
        # 修复（实测）：collect 现在产出 shell-file / shell-dir / param 三类来源，
        # 此前只判 "shell-literal" 导致 shell 派生目标**完全不校验**（漏拦）。
        shell_derived = src.startswith("shell-")
        if tool in READ_TOOLS or shell_derived:
            if not any(glob_match(g, val) for g in grants["read"]) and not any(glob_match(g, val) for g in grants["write"]):
                block("角色 %s 不允许访问：%s（%s）" % (role, val, src),
                      "可读范围见 perm.py grants；需要更多材料请让主控用 --extra-read 授予具体文件")
        if tool in WRITE_TOOLS:
            if not any(glob_match(g, val) for g in grants["write"]):
                block("角色 %s 不允许写入：%s" % (role, val),
                      "只允许写派发端授予的具体文件；需要时用 --extra-write 追加")
    sys.exit(0)


if __name__ == "__main__":
    main()