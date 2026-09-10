#!/usr/bin/env python3
"""文献笔记去倾向提案应用器。

输入：out/research-ops/notes-cleanup/proposals/<batch>/*.json（子代理产出，quote 已逐字校验）
行为：
- move-to-annex：从笔记正文中摘除 quote（必须唯一命中），原文逐字保全到 annex（不删历史）；
- split：用 replacement 替换 quote（replacement 必填，否则跳过交人工）；
- 标点修复：摘除后修复悬空标点（保守集合）；
- 幂等：state JSON 记录 (batch/proposal/index)，重跑跳过已完成项；
- 残留扫描：应用后报告各笔记残留的课题关联词命中（只报告不自动删）。

用法：
  PYTHONPATH=. python3 -m scripts.topic_harness.apply_note_patches --batch b1-1 --batch b2-1
"""
from __future__ import annotations

import argparse
import glob
import json
import os

def _root() -> str:
    """worktree 内运行用空前缀；主库内运行自动加 worktree 前缀。"""
    return "" if os.path.exists("LITERATURE/notes/raw") else ".worktrees/research-ops/"

RAW_DIR = _root() + "LITERATURE/notes/raw/"
ANNEX = _root() + "LITERATURE/notes/annex/20260910-debias-annex.md"
PROP_DIR = _root() + "out/research-ops/notes-cleanup/proposals/"
STATE = _root() + "out/research-ops/notes-cleanup/applied-state.json"
RESIDUE_PAT = r"我们|F0|F1|信息阶梯|AoI-of-state|与课题|与对账|与我们对账|可复用"

PUNCT_FIXES = [("。。", "。"), ("；。", "。"), ("——。", "。"), ("：。", "。"),
               ("、。", "。"), ("，，", "，"), ("（）", ""), ("  ", " ")]


def load_state(path: str) -> set:
    if os.path.exists(path):
        return set(json.load(open(path, encoding="utf-8")))
    return set()


def save_state(path: str, done: set) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(sorted(done), open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def apply_proposal(prop_path: str, batch: str, raw_dir: str,
                   annex_lines: list, done: set, report: list) -> None:
    prop = json.load(open(prop_path, encoding="utf-8"))
    note = prop["file"]
    if not os.path.exists(note):
        report.append("SKIP " + os.path.basename(prop_path) + " 笔记不存在: " + note)
        return
    s = open(note, encoding="utf-8").read()
    base = os.path.basename(prop_path)
    for i, seg in enumerate(prop.get("segments", [])):
        key = batch + "/" + base + "/" + str(i)
        if key in done:
            continue
        op = seg.get("op", "")
        q = seg.get("quote", "")
        if op not in ("move-to-annex", "split"):
            continue
        if not q or s.count(q) != 1:
            report.append("SKIP " + base + "#" + str(i) + " 未命中或不唯一")
            continue
        if op == "split":
            rep = seg.get("replacement") or ""
            if not rep:
                report.append("SKIP " + base + "#" + str(i) + " split 缺 replacement")
                continue
        else:
            rep = ""
        s = s.replace(q, rep)
        annex_lines += ["## " + os.path.basename(note) + "（batch " + batch + "）",
                        "- 提案: out/research-ops/notes-cleanup/proposals/" + batch + "/" + base,
                        "- 移出原文: " + q, ""]
        done.add(key)
        report.append("OK " + base + "#" + str(i) + " " + op)
    for a, b in PUNCT_FIXES:
        s = s.replace(a, b)
    open(note, "w", encoding="utf-8").write(s)


def residue_scan(raw_dir: str, notes: list) -> list:
    import re
    pat = re.compile(RESIDUE_PAT)
    out = []
    for n in sorted(notes):
        s = open(n, encoding="utf-8").read()
        hits = pat.findall(s)
        if hits:
            out.append(os.path.basename(n) + ": " + str(len(hits)) + " 处 -> " + ",".join(sorted(set(hits))))
    return out


def main(argv: list) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", action="append", required=True)
    args = ap.parse_args(argv)
    done = load_state(STATE)
    annex_lines, report, touched = [], [], []
    for batch in args.batch:
        for prop_path in sorted(glob.glob(PROP_DIR + batch + "/*.json")):
            prop = json.load(open(prop_path, encoding="utf-8"))
            touched.append(prop["file"])
            apply_proposal(prop_path, batch, RAW_DIR, annex_lines, done, report)
    if annex_lines:
        mode = "a" if os.path.exists(ANNEX) else "w"
        with open(ANNEX, mode, encoding="utf-8") as f:
            f.write(chr(10).join(annex_lines) + chr(10))
    save_state(STATE, done)
    for line in report:
        print(line)
    print("--- 残留扫描（只报告）---")
    for line in residue_scan(RAW_DIR, touched):
        print(line)
    print("应用段数:", sum(1 for r in report if r.startswith("OK ")),
          "| 跳过:", sum(1 for r in report if r.startswith("SKIP ")))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))