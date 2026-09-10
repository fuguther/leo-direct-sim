#!/usr/bin/env python3
"""hook 共享库 v3（按 Codex 5 项实查收口）。

v2 → v3 关键变化：
  #2 首次访问即受控：未登记会话在**研究区内**首次访问时原子领取票据；无票据则暂停并报告；
  #4 损坏即停：清单 missing/corrupt 时，研究会话失败关闭；主控凭 orchestrator.id 仍可操作；
  #3 最小授权：读/写一律按具体文件匹配（由 perm.py 的角色表 + 派发端 --extra-* 决定）。
"""
import json, os, re, sys, time
from pathlib import Path

# 受控研究区 = 本 hook 所在 worktree（**不依赖载荷 cwd**）。
# 实测教训：子代理的 session cwd 是主仓库（/Users/lge/Desktop/leo-direct-sim），
# 而非本 worktree；因此按 cwd 判定"是否研究会话"会漏判 —— 必须按**访问路径**判定。
HOOK_DIR = Path(__file__).resolve().parent
HOOK_WORKTREE = HOOK_DIR.parents[1]        # round/hooks -> round -> worktree 根
PERM_FILE = HOOK_DIR / "permissions.json"
ORCH_FILE = HOOK_DIR / "orchestrator.id"
LOG_FILE = HOOK_DIR / "unregistered.log"

EXTERNAL_DENY_SUBSTR = [
    "/.dsh/sessions/",
    "/.worktrees/research-ops/",
    "LEO-Research-Workspace",
]
TOOL_PATH_KEYS = ("file_path", "path", "target", "notebook_path")
READ_TOOLS = {"read", "read_document", "read_image", "glob", "grep", "ls"}
WRITE_TOOLS = {"write", "edit", "notebook_edit"}


def find_worktree(cwd: str = ""):
    """兼容保留：返回本 hook 所属的受控工作区（忽略 cwd）。

    v3 曾按 cwd 判定，实测失效（子代理 cwd = 主仓库）。现统一以 HOOK_WORKTREE 为准。
    """
    return HOOK_WORKTREE


def in_worktree(path: str) -> bool:
    """该（已归一化的）路径是否落在受控研究区内。"""
    try:
        rel = os.path.relpath(path, str(HOOK_WORKTREE))
    except Exception:
        return False
    return not rel.startswith("..")


def normalize(raw: str, cwd: str, wt):
    if not raw or not isinstance(raw, str):
        return "empty", ""
    s = raw.strip().strip(chr(39) + chr(34))
    if not s:
        return "empty", ""
    if not os.path.isabs(s):
        s = os.path.join(cwd or os.getcwd(), s)
    try:
        real = os.path.realpath(s)
    except Exception:
        real = os.path.abspath(s)
    if wt is not None:
        try:
            rel = os.path.relpath(real, str(wt))
        except Exception:
            rel = real
        if not rel.startswith(".."):
            return "worktree", rel.replace(os.sep, "/")
    return "external", real.replace(os.sep, "/")


def _glob_to_re(pat: str):
    out, i, n = [], 0, len(pat)
    while i < n:
        c = pat[i]
        if c == "*":
            if pat[i:i + 2] == "**":
                out.append(".*")
                i += 2
                if i < n and pat[i] == "/":
                    i += 1
                continue
            out.append("[^/]*")
        elif c == "?":
            out.append("[^/]")
        else:
            out.append(re.escape(c))
        i += 1
    return re.compile("^" + "".join(out) + "$")


_CACHE = {}


def glob_match(pattern: str, path: str) -> bool:
    rx = _CACHE.get(pattern)
    if rx is None:
        rx = _glob_to_re(pattern)
        _CACHE[pattern] = rx
    return bool(rx.match(path))


def load_perms():
    if not PERM_FILE.exists():
        return {}, "missing"
    try:
        d = json.loads(PERM_FILE.read_text(encoding="utf-8"))
        return (d, "ok") if isinstance(d, dict) else ({}, "corrupt")
    except Exception:
        return {}, "corrupt"


def orchestrator_id() -> str:
    try:
        return ORCH_FILE.read_text(encoding="utf-8").strip()
    except Exception:
        return ""


def resolve_role(session_id: str, wt, allow_claim: bool = True):
    """返回 (role, entry, reason)。role ∈ orchestrator / <角色> / unknown。"""
    d, st = load_perms()
    if st != "ok":
        if session_id and session_id == orchestrator_id():
            return "orchestrator", {}, "清单 %s，会话是主控（可修复）" % st
        if wt is not None:
            return "unknown", {}, "权限清单 %s —— 研究会话失败关闭" % st
        return "unknown", {}, "权限清单 %s —— 非研究区，放行但记录" % st
    if session_id and session_id == d.get("orchestrator_session"):
        return "orchestrator", {}, ""
    entry = (d.get("sessions") or {}).get(session_id or "")
    if entry:
        return entry.get("role") or "unknown", entry, ""
    if allow_claim and wt is not None and session_id:
        try:
            sys.path.insert(0, str(HOOK_DIR))
            import perm as _perm
            got, why = _perm.claim_ticket(session_id)
            if got:
                return got["role"], got, why
        except Exception:
            pass
    return "unknown", {}, "未登记且无可用票据"


def grants_for(role: str, entry: dict) -> dict:
    try:
        sys.path.insert(0, str(HOOK_DIR))
        from perm import ROLE_GRANTS
        base = ROLE_GRANTS.get(role)
    except Exception:
        base = None
    if base is None:
        return {"read": [], "write": [], "shell": "deny"}
    return {"read": list(base.get("read", [])) + list(entry.get("extra_read") or []),
            "write": list(base.get("write", [])) + list(entry.get("extra_write") or []),
            "shell": base.get("shell", "deny")}


def log_unregistered(session_id: str, tool: str, detail: str) -> None:
    try:
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write("%s\t%s\t%s\t%s\n" % (session_id or "?", tool, detail[:200], time.strftime("%H:%M:%S")))
    except Exception:
        pass


def read_input() -> dict:
    try:
        raw = sys.stdin.read()
    except Exception:
        return {"_parse_error": "stdin read failed"}
    if not raw.strip():
        return {}
    try:
        d = json.loads(raw)
        return d if isinstance(d, dict) else {"_parse_error": "not an object"}
    except Exception as e:
        return {"_parse_error": str(e)}


def block(reason: str, hint: str = "") -> None:
    msg = "[HOOK-BLOCK] " + reason
    if hint:
        msg += "\n  应对：" + hint
    print(msg, file=sys.stderr)
    sys.exit(2)


def note(msg: str) -> None:
    print("[HOOK] " + msg, file=sys.stderr)


def tool_paths(tool: str, ti: dict) -> list:
    out = []
    if not isinstance(ti, dict):
        return out
    for k in TOOL_PATH_KEYS:
        v = ti.get(k)
        if isinstance(v, str) and v.strip():
            out.append(v)
    return out