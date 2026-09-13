#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重生成 round/knowledge/NEUTRAL-KNOWLEDGE-VIEW.md（本线所有）。
从主库 KNOWLEDGE-MAP.md 节级切片：保留 Claim/Assumption/Evidence 三图与全文阅读证据表；
排除『检索记录与覆盖边界』与『外部碰撞补充』（含旧候选关系与旧"未找到"判断，留给生成后比较）。
原 KNOWLEDGE-MAP 变更后重跑本脚本并同步 gen_manifest.py。
"""
import hashlib, os, re

MAIN = "/Users/lge/Desktop/leo-direct-sim"
OUT = "/Users/lge/Desktop/leo-direct-sim/.worktrees/topic-loop-20260910/round/knowledge/NEUTRAL-KNOWLEDGE-VIEW.md"
src = MAIN + "/LITERATURE/KNOWLEDGE-MAP.md"
lines = open(src, encoding="utf-8").read().splitlines(keepends=True)
secs = [[i, ln.strip()[3:].strip()] for i, ln in enumerate(lines, 1) if ln.startswith("## ")]
secs.append([len(lines) + 1, "EOF"])
def span(prefix):
    for idx, (start, title) in enumerate(secs[:-1]):
        if title.startswith(prefix):
            return start, secs[idx + 1][0] - 1, title
    return None
KEEP = ["Claim Map", "Assumption Map", "Evidence Map", "全文阅读证据表"]
EXCLUDE = ["检索记录与覆盖边界", "外部碰撞补充"]
kept, excl = [], []
for p in KEEP:
    s = span(p)
    if s: kept.append(s)
for p in EXCLUDE:
    s = span(p)
    if s: excl.append(s)
out = ["# 中性知识视图（生成器可见版，程序化生成 " + __import__("time").strftime("%Y-%m-%d %H:%M") + "）", "",
       "> KNOWLEDGE-MAP.md 的候选无关切片。生成阶段入口用本文件，不用原 KNOWLEDGE-MAP",
       "> （其含旧候选关系标注与旧『未找到』检索结论，按 EFFECTIVE-RULES-R2 §2 留给生成后比较）。", "",
       "> 原件 sha256:" + hashlib.sha256(open(src, 'rb').read()).hexdigest(), "",
       "## 切片明细", "",
       "- 保留节: " + "; ".join(f"{t}（原件 L{s}-L{e}）" for s, e, t in kept),
       "- 排除节: " + ("; ".join(f"{t}（原件 L{s}-L{e}）" for s, e, t in excl) or "无"), ""]
for s, e, t in kept:
    out.append(f"<!-- BEGIN {t} | KNOWLEDGE-MAP.md L{s}-L{e} -->")
    out.extend(lines[s - 1:e])
    out.append(f"<!-- END {t} -->")
    out.append("")
open(OUT, "w", encoding="utf-8").write("\n".join(out))
print("regenerated:", OUT, len("\n".join(out)), "chars; kept", len(kept), "excluded", len(excl))
