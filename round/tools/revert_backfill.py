#!/usr/bin/env python3
"""回退误回补：删除 backfill_facts.py 追加的事实补录块。"""
from pathlib import Path
NEU = Path(__file__).resolve().parents[1] / "knowledge" / "notes-neutral"
MARK = "## 事实补录（剥离器误删回补，2026-09-10）"
n = 0
for f in NEU.glob("*.md"):
    t = f.read_text(encoding="utf-8")
    if MARK in t:
        t = t[:t.index(MARK)].rstrip() + "\n"
        f.write_text(t, encoding="utf-8"); n += 1
print("reverted_files=", n)
