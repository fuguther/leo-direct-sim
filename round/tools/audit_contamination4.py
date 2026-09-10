#!/usr/bin/env python3
"""污染审计 v4（决定性）：只检查 tool/call 的路径参数位，不看 content/code 正文。

做法：对每个 tool/call，序列化参数后：
  1) 去掉 content / code / old_string / new_string / text / message 的值；
  2) 剥离 bash heredoc 正文；
  3) 在剩余文本里找黑名单路径 —— 剩余部分只含 file_path/path/command 等真实访问目标。
"""
import json, re, subprocess, sys
from pathlib import Path

SESS = Path.home() / ".dsh" / "sessions" / "--Users-lge-Desktop-leo-direct-sim--"
BLACK = ["LITERATURE/notes/raw", "KNOWLEDGE-MAP.md", "notes-neutral-manifest",
         "P0-SEMANTIC-SPOTCHECK", "round/run1", "CANDIDATE-LEDGER", "round/reviews",
         "round/history", "ELIMINATED-REGISTER", "ROUND-LOG.md", "ANALYSIS/",
         "NOTES.md", "QUALITY-GATE-R2", "research-ops", "00-READING-QUEUE",
         "related-work-notes", "COLDSTART-20260903", "PIPELINE-MAP", "DRYRUN-REPORT"]
DROP_KEYS = ("content", "code", "old_string", "new_string", "text", "message", "prompt", "description")

def strip_heredoc(s):
    return re.sub(r"<<-?\s*['\"]?(\w+)['\"]?\n.*?\n\s*\1\s*$", " <<HEREDOC>>", s, flags=re.S | re.M)

def tool_invocations(code):
    """从 run_code 源码里抽出 tools.X({...}) 的调用，返回 (名字, 参数文本)。"""
    out = []
    for m in re.finditer(r"tools\.(\w+)\s*\(", code):
        name = m.group(1)
        i = m.end()
        depth = 1
        j = i
        instr = None
        while j < len(code) and depth > 0:
            ch = code[j]
            if instr:
                if ch == "\\": j += 2; continue
                if ch == instr: instr = None
            elif ch in "\"'": instr = ch
            elif ch == "(": depth += 1
            elif ch == ")": depth -= 1
            j += 1
        out.append((name, code[i:j-1]))
    return out

def sanitize_args(name, blob):
    """把参数文本里的 content/code 正文挖掉，只留下路径与命令。"""
    b = blob
    for k in DROP_KEYS:
        b = re.sub(r"\b" + k + r"\s*:\s*`[^`]*`", k + ": <STRIPPED>", b, flags=re.S)
        b = re.sub(r'\b' + k + r'\s*:\s*"(?:[^"\\]|\\.)*"', k + ': <STRIPPED>', b, flags=re.S)
    b = strip_heredoc(b)
    return b

def audit(sid):
    f = SESS / sid / "session.jsonl.zstd"
    if not f.exists(): return None
    out = subprocess.run(["zstd", "-dc", str(f)], capture_output=True, timeout=120)
    total, viol = 0, []
    for line in out.stdout.decode("utf-8", "ignore").splitlines():
        try: e = json.loads(line)
        except Exception: continue
        if e.get("type") != "tool/call": continue
        d = e.get("data", {})
        name = d.get("name") or d.get("tool") or "?"
        raw = d.get("arguments", d.get("args", {}))
        try: args = json.loads(raw) if isinstance(raw, str) else raw
        except Exception: args = {}
        total += 1
        blobs = []
        if name == "run_code":
            code = str(args.get("code", ""))
            for tname, blob in tool_invocations(code):
                blobs.append(sanitize_args(tname, blob))
        else:
            blobs.append(sanitize_args(name, json.dumps({k: v for k, v in args.items() if k not in DROP_KEYS}, ensure_ascii=False)))
        joined = " ".join(blobs)
        for b in BLACK:
            if b in joined:
                viol.append((name, b, joined[:260]))
    return {"calls": total, "violations": viol}

if __name__ == "__main__":
    for sid in sys.argv[1:]:
        r = audit(sid)
        if r is None: print(sid[:8], "NO LOG"); continue
        v = r["violations"]
        print("=== %s tool_calls=%d 真实违规=%d" % (sid[:8], r["calls"], len(v)))
        for name, b, blob in v[:8]:
            print("    !! [%s] matched=%s" % (name, b))
            print("       %s" % blob[:200])
