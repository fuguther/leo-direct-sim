#!/usr/bin/env python3
"""hook 共享库 v2（2026-09-11 重写，对应 Codex 三项收口）。

与 v1 的关键差异：
  1. 身份只认 session_id + 权限清单（perm.py），**不用任何环境变量判定子代理身份**；
  2. 路径统一 realpath 归一化（./ 相对 绝对 符号链接 一律同判）；
  3. 显式区分"可强制"（工具级路径）与"仅尽力检测"（bash/run_code 任意代码）。
"""
import fnmatch, json, os, re, sys, time
from pathlib import Path

HOOK_DIR = Path(__file__).resolve().parent
PERM_FILE = HOOK_DIR / "permissions.json"
LOG_FILE = HOOK_DIR / "unregistered.log"

# 工作区外的高危读取目标（偷看其他会话/其他代理，等于绕过隔离）
EXTERNAL_DENY_SUBSTR = [
    "/.dsh/sessions/",
    "/.worktrees/research-ops/",
    "LEO-Research-Workspace",
]

TOOL_PATH_KEYS = ("file_path", "path", "target", "notebook_path")
READ_TOOLS = {"read", "read_document", "read_image", "glob", "grep", "ls"}
WRITE_TOOLS = {"write", "edit", "notebook_edit"}


# ── 工作区定位与路径归一化 ───────────────────────────────────────────

def find_worktree(cwd: str = "") -> Path | None:
    for base in (cwd, os.getcwd()):
        if not base:
            continue
        p = Path(base).resolve()
        for cand in (p, *p.parents):
            if (cand / "round" / "rules").is_dir():
                return cand
    return None


def normalize(raw: str, cwd: str, wt: Path | None) -> tuple[str, str]:
    """返回 (类别, 归一化值)。类别 ∈ worktree / external / empty。

    归一化使用 realpath，因此 ./x、x、/abs/.../x 与符号链接指向同一文件时结果一致。
    """
    if not raw or not isinstance(raw, str):
        return "empty", ""
    s = raw.strip().strip("'" + '"')
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


# ── glob 匹配（支持 **）────────────────────────────────────────────

def _glob_to_re(pat: str) -> re.Pattern:
    out, i, n = [], 0, len(pat)
    while i < n:
        c = pat[i]
        if c == "*":
            if pat[i:i + 2] == "**":
                out.append(".*"); i += 2
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


_GLOB_CACHE: dict = {}


def glob_match(pattern: str, path: str) -> bool:
    rx = _GLOB_CACHE.get(pattern)
    if rx is None:
        rx = _glob_to_re(pattern)
        _GLOB_CACHE[pattern] = rx
    return bool(rx.match(path))


# ── 权限清单 ─────────────────────────────────────────────────────

def load_perms() -> dict:
    if not PERM_FILE.exists():
        return {}
    try:
        return json.loads(PERM_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def resolve_role(session_id: str) -> tuple[str, dict]:
    """返回 (role, session_entry)。role ∈ orchestrator / <角色> / unknown。"""
    d = load_perms()
    if not d:
        return "unknown", {}
    if session_id and session_id == d.get("orchestrator_session"):
        return "orchestrator", {}
    entry = (d.get("sessions") or {}).get(session_id or "")
    if entry:
        return entry.get("role") or "unknown", entry
    return "unknown", {}


def grants_for(role: str, entry: dict) -> dict:
    """角色授权 + 该会话的额外授权（派发端 bind 时指定）。"""
    try:
        sys.path.insert(0, str(HOOK_DIR))
        from perm import ROLE_GRANTS
        base = ROLE_GRANTS.get(role)
    except Exception:
        base = None
    if base is None:
        return {"read": [], "write": [], "shell": "deny"}
    return {
        "read": list(base.get("read", [])) + list(entry.get("extra_read") or []),
        "write": list(base.get("write", [])) + list(entry.get("extra_write") or []),
        "shell": base.get("shell", "deny"),
    }


def log_unregistered(session_id: str, tool: str, detail: str) -> None:
    try:
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write("%s\t%s\t%s\t%s\n" % (session_id or "?", tool, detail[:200], time.strftime("%H:%M:%S")))
    except Exception:
        pass


# ── 协议 ─────────────────────────────────────────────────────────

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
    """只取**结构化路径参数位**——这是可强制的部分。"""
    out = []
    if not isinstance(ti, dict):
        return out
    for k in TOOL_PATH_KEYS:
        v = ti.get(k)
        if isinstance(v, str) and v.strip():
            out.append(v)
    return out