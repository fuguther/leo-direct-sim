#!/usr/bin/env python3
"""建立 Zotero itemKey -> PDF 存储路径 的清单，供 VM 批量转文本。"""
import json, os
from pathlib import Path

ZW = Path.home() / "Zotero" / "storage"
rows = json.load(open("round/zotero/index-raw.json"))
out, miss = [], []
for r in rows:
    pk = r.get("pdfKey")
    if not pk:
        miss.append((r["key"], r.get("title"), "no pdfKey")); continue
    d = ZW / pk
    pdfs = list(d.glob("*.pdf")) if d.exists() else []
    if not pdfs:
        miss.append((r["key"], r.get("title"), "storage dir/file missing: %s" % d)); continue
    p = max(pdfs, key=lambda x: x.stat().st_size)
    out.append({"itemKey": r["key"], "pdfKey": pk, "year": r.get("year"),
                "title": r.get("title"), "src": str(p), "size": p.stat().st_size})
Path("round/zotero/pdf-manifest.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("resolved:", len(out), "missing:", len(miss))
tot = sum(o["size"] for o in out)
print("total size: %.1f MB" % (tot/1e6))
for m in miss[:10]: print("  MISS", m)