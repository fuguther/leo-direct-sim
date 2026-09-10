#!/usr/bin/env python3
"""hook 共享库：黑名单判定、路径提取、输入/输出协议封装。

协议要点（实测自 dsh-hook-protocol / dsh-hooks-claude-code）：
  - 输入：stdin 收 JSON（含 tool_name / tool_input / cwd / session_id / hook_event_name）
  - 阻塞：exit 2 + stderr 写原因（模型会看到）
  - 放行：exit 0；附加上下文用结构化 stdout（本套件暂不用）
  - 其他退出码 = 非阻塞失败（记录但不拦）——本库坚持用 2 表达"确实要拦"
"""
import json, os, re, sys
from pathlib import Path

# ── 黑名单（与 EFFECTIVE-RULES-R2 §8.1 隔离矩阵一致）────────────────
BLACKLIST_PREFIXES = [
    "LITERATURE/notes/raw/",
    "round/run1/",
    "round/reviews/",
    "round/history/",
    "round/run2/",                   # 整个 run2 目录对生成端不可见（含 cards/scope/errata/审阅）
    "ANALYSIS/",                     # 交付与分析文档不进生成端
    "round/tools/archive/",
    "round/hooks/",                  # hook 配置不进生成端
]
BLACKLIST_EXACT = [
    "LITERATURE/KNOWLEDGE-MAP.md",
    "round/CANDIDATE-LEDGER.csv",
    "round/ROUND-LOG.md",
    "round/knowledge/notes-neutral-manifest.json",
    "round/knowledge/P0-SEMANTIC-SPOTCHECK.md",
    "round/zotero/undermind-gap-review.txt",
]
BLACKLIST_SUBSTR = [
    "KNOWLEDGE-MAP.md",
    "ELIMINATED-REGISTER",
    "HISTORY-INDEX",
    "CANDIDATE-LEDGER",
    "notes-neutral-manifest",
    "QUALITY-GATE-R",
]
# 命令级高危模式（bash 里出现即视为试图触碰黑名单）
BLACKLIST_CMD = re.compile(
    r"(ls|find|glob|cat|head|tail|grep|rg|tree|less|more|wc)\s+[^|;]*"
    r"(notes/raw|run1/|reviews/|history/|CANDIDATE-LEDGER|KNOWLEDGE-MAP|ELIMINATED-REGISTER|HISTORY-INDEX|staging/)"
)


def norm_path(p: str, cwd: str = "") -> str:
    """把绝对路径规整为相对 worktree 的形式，便于前缀匹配。"""
    if not p:
        return ""
    p = p.strip()
    for root in (cwd, os.environ.get("DSH_WORKSPACE", ""), os.getcwd()):
        if root and p.startswith(root):
            p = p[len(root):]
            break
    p = p.lstrip("/")
    if p.startswith(".worktrees/"):
        parts = p.split("/", 2)
        p = parts[2] if len(parts) > 2 else p
    return p


def is_blacklisted(path: str, cwd: str = "") -> str | None:
    """命中返回原因字符串，否则 None。"""
    np = norm_path(path, cwd)
    if not np:
        return None
    for pre in BLACKLIST_PREFIXES:
        if np.startswith(pre):
            return "路径命中黑名单前缀：%s" % pre
    if np in BLACKLIST_EXACT:
        return "路径命中黑名单（精确）：%s" % np
    for sub in BLACKLIST_SUBSTR:
        if sub in np:
            return "路径含黑名单标记：%s" % sub
    return None


def extract_targets(tool_name: str, ti: dict) -> list[str]:
    """从工具调用参数里提取"真实访问目标"（不含正文内容）。"""
    out = []
    if not isinstance(ti, dict):
        return out
    for k in ("file_path", "path", "target", "notebook_path"):
        v = ti.get(k)
        if isinstance(v, str):
            out.append(v)
    if tool_name in ("bash", "shell"):
        cmd = ti.get("command", "")
        if isinstance(cmd, str):
            out.append("__CMD__" + cmd)
    code = ti.get("code")
    if isinstance(code, str):
        # run_code 里嵌的工具调用：抽取 path/file_path/command 参数位
        for m in re.finditer(r"(?:file_path|path|target)\s*:\s*['\"]([^'\"]+)['\"]", code):
            out.append(m.group(1))
        for m in re.finditer(r"command\s*:\s*['\"]([^'\"]+)['\"]", code):
            out.append("__CMD__" + m.group(1))
        for m in re.finditer(r"command\s*:\s*`([^`]{0,400})", code):
            out.append("__CMD__" + m.group(1))
    for k in ("pattern", "query"):
        v = ti.get(k)
        if isinstance(v, str) and ("/" in v or v.endswith(".md") or v.endswith(".csv")):
            out.append(v)
    return out


def read_input() -> dict:
    try:
        raw = sys.stdin.read()
    except Exception:
        return {}
    if not raw.strip():
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {"_parse_error": raw[:200]}


def block(reason: str, hint: str = "") -> None:
    msg = "[HOOK-BLOCK] " + reason
    if hint:
        msg += "\n  应对：" + hint
    print(msg, file=sys.stderr)
    sys.exit(2)


def allow(note: str = "") -> None:
    if note:
        print("[HOOK-OK] " + note, file=sys.stderr)
    sys.exit(0)