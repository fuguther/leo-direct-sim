#!/usr/bin/env python3
"""由 round/zotero/index-raw.json 生成生成器可用的 Zotero 索引（Markdown）。"""
import json, re, csv
from pathlib import Path

rows = json.load(open("round/zotero/index-raw.json"))
src = list(csv.DictReader(open("LITERATURE/SOURCES.csv")))

def norm(s): return re.sub(r"[^a-z0-9]+", "", (s or "").lower())
src_keys = {norm(r["title"]) for r in src}
src_words = [set(re.findall(r"[a-z]{4,}", (r["title"] or "").lower())) for r in src]

def in_catalog(t):
    n = norm(t)
    if n in src_keys: return True
    zw = set(re.findall(r"[a-z]{4,}", (t or "").lower()))
    for sw in src_words:
        if sw and len(zw & sw) / max(1, len(zw | sw)) > 0.6: return True
    return False

rows_sorted = sorted(rows, key=lambda r: (str(r.get("year") or "0"), r.get("title") or ""), reverse=True)
new = [r for r in rows_sorted if not in_catalog(r["title"])]
L = []
L.append("# Zotero 本机库索引（111 篇，2026-09-10 程序化生成）")
L.append("")
L.append("> 用途：生成器/审查者的**库内文献总入口**（白名单条目）。每一篇都有本地 PDF 全文：")
L.append("> 用 zotero_fulltext(itemKey=KEY) 直接读全文；zotero_item(key=KEY) 看元数据与附件。")
L.append("> 标记 [新] = 此前不在 LITERATURE/SOURCES.csv（52 篇题录）中——这些是过去从未纳入选题语料的文献。")
L.append("> 纪律：承重引文必须回全文核对并给页码/节号；仅凭标题不得作为 G1 证据。")
L.append("")
L.append("统计：共 %d 篇；其中 %d 篇不在题录中；PDF 可得 %d 篇。" % (len(rows), len(new), sum(1 for r in rows if r["pdf"] > 0)))
L.append("")
L.append("| # | key | 年份 | 类型 | 标题 | 作者 | 题录 |")
L.append("|---|---|---|---|---|---|---|")
for i, r in enumerate(rows_sorted, 1):
    mark = "" if in_catalog(r["title"]) else "**[新]**"
    title = (r.get("title") or "(无标题)").replace("|", "/")
    au = (r.get("creators") or "")
    parts = [a.strip() for a in au.split(";") if a.strip()]
    aus = (parts[0] if parts else "") + (" 等" if len(parts) > 1 else "")
    L.append("| %d | %s | %s | %s | %s | %s | %s |" % (i, r["key"], r.get("year",""), (r.get("type") or "")[:14], title, aus, mark))
Path("round/zotero/ZOTERO-INDEX.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("index written: %d items, %d NOT in catalog" % (len(rows), len(new)))
print()
print("=== 未入题录（样例 25 篇）===")
for r in new[:25]:
    print("  %s | %s" % (r.get("year") or "????", str(r.get("title"))[:80]))