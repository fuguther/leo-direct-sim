#!/usr/bin/env python3
"""P0 语义抽查：列出被剥离器删除的全部句子，标记可能含论文事实者（数字/引用/限定词）。"""
import re, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "LITERATURE" / "notes" / "raw"
NEU = ROOT / "round" / "knowledge" / "notes-neutral"

SENT = re.compile(r"(?<=[。！？；])")
FACT_MARK = re.compile(r"\d|Eq\.|Table|§|p\.|P\d|行 |原文|已核|未核实|核对|DOI|arXiv|Fig")
report = []
for f in sorted(RAW.glob("*.md")):
    raw = f.read_text(encoding="utf-8")
    neu = (NEU / f.name).read_text(encoding="utf-8")
    neu_sents = set(SENT.split(neu))
    removed = [s.strip() for s in SENT.split(raw) if s.strip() and s.strip() not in neu_sents]
    flagged = [s for s in removed if FACT_MARK.search(s)]
    report.append({"file": f.name, "removed_sentences": len(removed), "fact_flagged": flagged})

out = ROOT / "round" / "knowledge" / "notes-neutral-spotcheck.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
tot = sum(r["removed_sentences"] for r in report)
fl = sum(len(r["fact_flagged"]) for r in report)
print(f"files={len(report)} removed_sentences={tot} fact_flagged={fl}")
for r in report:
    if r["fact_flagged"]:
        print("\n### " + r["file"])
        for s in r["fact_flagged"][:6]:
            print("  - " + s[:220])
