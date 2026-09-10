#!/usr/bin/env python3
"""审计生成器实际读取的语料层：notes-neutral / 本地PDF / 外部下载 / Undermind 调用。"""
import json, re, subprocess
from pathlib import Path
SESS = Path.home()/".dsh/sessions/--Users-lge-Desktop-leo-direct-sim--"
IDS = {"6dd5881f-3bd2-498d-978b-c37511d9fcd2": "A",
       "b77deb91-6ea1-4348-b6fa-ad75e951ecb1": "B",
       "4e787df3-9a12-45c4-ac1d-358527bdc760": "C"}
for sid, tag in IDS.items():
    f = SESS/sid/"session.jsonl.zstd"
    if not f.exists():
        print(tag, "no log"); continue
    out = subprocess.run(["zstd", "-dc", str(f)], capture_output=True, timeout=120)
    txt = out.stdout.decode("utf-8", "ignore")
    notes, pdfs, arxiv, und, soft = set(), set(), set(), 0, set()
    for line in txt.splitlines():
        try: e = json.loads(line)
        except Exception: continue
        if e.get("type") != "tool/call": continue
        d = e.get("data", {})
        s = json.dumps(d.get("arguments", d), ensure_ascii=False)
        for m in re.finditer(r"notes-neutral/([A-Za-z0-9\-_.]+)\.md", s): notes.add(m.group(1))
        for m in re.finditer(r"papers/([A-Za-z0-9\-_.]+)\.pdf", s): pdfs.add(m.group(1))
        for m in re.finditer(r"arxiv\.org/(?:abs|pdf)/([0-9.]+)", s): arxiv.add(m.group(1))
        for m in re.finditer(r"semanticscholar|openalex|doi\.org|crossref", s): soft.add(m.group(0))
        und += s.count("undermind")
    print(f"=== 生成器{tag} ({sid[:8]}) ===")
    print(f"  notes-neutral 读取: {len(notes)} 篇 -> {sorted(notes)[:10]}")
    print(f"  本地 PDF 引用: {len(pdfs)} -> {sorted(pdfs)}")
    print(f"  arXiv 获取: {len(arxiv)} -> {sorted(arxiv)[:8]}")
    print(f"  其他检索域名: {sorted(soft)}")
    print(f"  undermind 调用迹象: {und}")
    print()
