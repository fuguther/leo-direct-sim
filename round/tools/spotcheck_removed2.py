#!/usr/bin/env python3
"""P0 语义抽查（精确版）：判定被删内容是否"真的不在中性笔记里"，并筛出含论文事实者。
归一化=去空白+去标点，避免重分段误报。"""
import re, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "LITERATURE" / "notes" / "raw"
NEU = ROOT / "round" / "knowledge" / "notes-neutral"
SENT = re.compile(r"(?<=[。！？；])")
NORM = re.compile(r"[\s。，、；：？！（）()「」【】\[\]“”\"'\-—~·]")
FACT = re.compile(r"\d|Eq\.|Table|§|Fig|Abstract|arXiv|DOI|行\s*~?\d")

def norm(s):
    return NORM.sub("", s)

report = []
for f in sorted(RAW.glob("*.md")):
    raw = f.read_text(encoding="utf-8")
    neutxt = (NEU / f.name).read_text(encoding="utf-8")
    nneu = norm(neutxt)
    missing, fact_missing = 0, []
    for s in SENT.split(raw):
        s = s.strip()
        if not s:
            continue
        ns = norm(s)
        if len(ns) < 8:
            continue
        # 真实缺失判定：归一化整句或其前 24 字不在中性文本中
        probe = ns if len(ns) <= 60 else ns[:60]
        if probe and probe in nneu:
            continue
        missing += 1
        if FACT.search(s):
            fact_missing.append(s)
    report.append({"file": f.name, "truly_missing": missing, "fact_missing": fact_missing})

out = ROOT / "round" / "knowledge" / "notes-neutral-spotcheck2.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
tot = sum(r["truly_missing"] for r in report)
fl = sum(len(r["fact_missing"]) for r in report)
print(f"files={len(report)} truly_missing={tot} fact_missing={fl}")
for r in report:
    if r["fact_missing"]:
        print("\n### " + r["file"] + f" (fact_missing={len(r['fact_missing'])})")
        for s in r["fact_missing"][:8]:
            print("  - " + s[:200])
