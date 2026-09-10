#!/usr/bin/env python3
"""独立污染审计 v2：只解析真实 tool/call 事件的参数，排除提示词文本干扰。"""
import json, subprocess, sys
from pathlib import Path

SESS = Path.home() / ".dsh" / "sessions" / "--Users-lge-Desktop-leo-direct-sim--"
BLACK = ["LITERATURE/notes/raw", "KNOWLEDGE-MAP.md", "notes-neutral-manifest",
         "P0-SEMANTIC-SPOTCHECK", "round/run1", "CANDIDATE-LEDGER", "round/reviews",
         "round/history", "ELIMINATED-REGISTER", "ROUND-LOG.md", "ANALYSIS/",
         "NOTES.md", "QUALITY-GATE-R2", "research-ops", "00-READING-QUEUE"]

def events(sid):
    f = SESS / sid / "session.jsonl.zstd"
    if not f.exists(): return []
    out = subprocess.run(["zstd", "-dc", str(f)], capture_output=True, timeout=90)
    evs = []
    for line in out.stdout.decode("utf-8", "ignore").splitlines():
        try: evs.append(json.loads(line))
        except Exception: pass
    return evs

def audit(sid):
    calls, viol = [], []
    for e in events(sid):
        if e.get("type") != "tool/call": continue
        d = e.get("data", {})
        name = d.get("name") or d.get("tool") or "?"
        args = d.get("arguments") if isinstance(d.get("arguments"), (dict, str)) else d.get("args", "")
        s = json.dumps(args, ensure_ascii=False) if not isinstance(args, str) else args
        calls.append((name, s[:120]))
        for b in BLACK:
            if b in s:
                viol.append((name, b, s[:200]))
    return calls, viol

for sid in sys.argv[1:]:
    calls, viol = audit(sid)
    print(f"=== {sid[:8]} tool_calls={len(calls)} violations={len(viol)}")
    for name, s in calls: print(f"    [{name}] {s}")
    for name, b, s in viol: print(f"    !! VIOLATION [{name}] matched={b} :: {s}")
