#!/usr/bin/env python3
"""核实 SOURCES.csv local_path 是否可达（悬空指针检查）。"""
import csv, os
from pathlib import Path
MAIN = Path("/Users/lge/Desktop/leo-direct-sim")
rows = list(csv.DictReader(open("LITERATURE/SOURCES.csv")))
ok, dangling = [], []
for r in rows:
    lp = (r.get("local_path") or "").strip()
    if not lp:
        continue
    for base in (MAIN / "LITERATURE", MAIN):
        p = base / lp
        if p.exists():
            ok.append((r["source_id"], str(p)[-60:])); break
    else:
        dangling.append((r["source_id"], lp[:80]))
print(f"local_path 可解析: {len(ok)}  悬空: {len(dangling)}")
for s, p in ok: print("  OK  ", s, "|", p)
print()
for s, p in dangling: print("  DANGLING", s, "|", p)
print()
print("related-work-notes/papers-txt 是否存在:", (MAIN/"LITERATURE/related-work-notes/papers-txt").exists())
