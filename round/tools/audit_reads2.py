#!/usr/bin/env python3
"""统计生成器实际接触的笔记与外部新论文。"""
import json, re, subprocess
from pathlib import Path
SESS = Path.home()/".dsh/sessions/--Users-lge-Desktop-leo-direct-sim--"
STEMS = {p.stem for p in Path("round/knowledge/notes-neutral").glob("*.md")}
IDS = {"6dd5881f-3bd2-498d-978b-c37511d9fcd2":"A","b77deb91-6ea1-4348-b6fa-ad75e951ecb1":"B","4e787df3-9a12-45c4-ac1d-358527bdc760":"C"}
for sid, tag in IDS.items():
    out = subprocess.run(["zstd","-dc",str(SESS/sid/"session.jsonl.zstd")], capture_output=True, timeout=120)
    txt = out.stdout.decode("utf-8","ignore")
    seen = {s for s in STEMS if s in txt}
    ext = sorted(set(re.findall(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5})", txt)))
    print(f"生成器{tag}: 接触笔记 {len(seen)}/{len(STEMS)} 篇")
    print(f"   未接触: {sorted(STEMS - seen)[:20]}")
    print(f"   外部 arXiv 编号: {ext}")
    print()
