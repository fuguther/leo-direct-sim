#!/usr/bin/env python3
"""合并辅助：卡文本两两 Dice 相似度矩阵（dedup.py 只读复用）。
用法: python3 merge_sim.py cards.json [--old LEDGER.csv] [--out report.md]
cards.json: [{"id": "...", "text": "..."}]
"""
import json, sys, csv, importlib.util
RO = "/Users/lge/Desktop/leo-direct-sim/.worktrees/research-ops"
spec = importlib.util.spec_from_file_location("dedup", RO + "/scripts/topic_harness/dedup.py")
dedup = importlib.util.module_from_spec(spec); spec.loader.exec_module(dedup)

def card_text_row(row):
    return " ".join(str(row.get(k) or "") for k in ("title","conditions","difficulty","cause_hypothesis","possible_change","strongest_alternative"))

def main():
    args = sys.argv[1:]
    cards = json.load(open(args[0], encoding="utf-8"))
    olds = []
    if "--old" in args:
        p = args[args.index("--old")+1]
        with open(p, newline="", encoding="utf-8") as f:
            olds = [(r["card_id"], card_text_row(r)) for r in csv.DictReader(f)]
    items = [(c["id"], c["text"]) for c in cards] + olds
    lines = ["# 相似度报告（Dice>0.40）", ""]
    for i in range(len(items)):
        for j in range(i+1, len(items)):
            s = dedup.dice_similarity(items[i][1], items[j][1])
            if s > 0.40:
                lines.append(f"- {items[i][0]} <-> {items[j][0]}: {s:.3f}")
    out = "\n".join(lines)
    if "--out" in args:
        open(args[args.index("--out")+1], "w", encoding="utf-8").write(out + "\n")
    print(out)
if __name__ == "__main__":
    main()
