#!/usr/bin/env python3
"""Zotero 111 篇 vs SOURCES.csv 52 篇 交叉比对。"""
import csv, json, re
from pathlib import Path

zot = json.load(open("round/zotero/raw-items.json"))
src = list(csv.DictReader(open("LITERATURE/SOURCES.csv")))

def norm(s):
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())

src_titles = {norm(r["title"]): r["source_id"] for r in src}
src_words = [set(re.findall(r"[a-z]{4,}", (r["title"] or "").lower())) for r in src]

matched, unmatched = [], []
for z in zot:
    t = norm(z.get("title", ""))
    hit = src_titles.get(t)
    if not hit:
        zw = set(re.findall(r"[a-z]{4,}", (z.get("title") or "").lower()))
        for i, sw in enumerate(src_words):
            if sw and len(zw & sw) / max(1, len(zw | sw)) > 0.6:
                hit = src[i]["source_id"]; break
    (matched if hit else unmatched).append((z, hit))

print(f"Zotero 论文 {len(zot)} 篇：与题录匹配 {len(matched)}，未入题录 {len(unmatched)}")
print()
print("=== 未入题录的（前 40）===")
for z, _ in unmatched[:40]:
    print(f"  [{(z.get('itemType') or '')[:12]:12s}] {str(z.get('date'))[:4]:4s} {str(z.get('title'))[:78]}")
print()
print(f"... 共 {len(unmatched)} 篇未入题录")
Path("round/zotero/unmatched.json").write_text(json.dumps([z for z,_ in unmatched], ensure_ascii=False, indent=1), encoding="utf-8")
