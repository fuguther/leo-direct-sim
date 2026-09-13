#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重生成 round/deps/DEPENDENCIES.md（本线所有）。
在承重文件被显式修改后运行；运行后 deps_check.py 应 exit 0。
任何未走本脚本的依赖变化都会被 deps_check.py 报为 drift。
"""
import hashlib, glob, os

MAIN = "/Users/lge/Desktop/leo-direct-sim"
W = "/Users/lge/Desktop/leo-direct-sim/.worktrees/topic-loop-20260910"
RO = "/Users/lge/Desktop/leo-direct-sim/.worktrees/research-ops"

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

m = []
m.append("# 依赖指纹清单（DEPENDENCIES，重生成于 " + __import__("time").strftime("%Y-%m-%d %H:%M") + "）")
m.append("")
m.append("> 本轮所有承重组件的内容指纹。deps_check.py 重算比对；指纹变化必须显式报告，不静默换版。")
m.append("> 重生成工具：round/tools/gen_manifest.py（承重文件被显式修改后运行）。")
m.append("")
m.append("| 组件 | 路径 | owner | sha256 | 获取方式 |")
m.append("|---|---|---|---|---|")
for f in ["retrieve.py", "dedup.py", "novelty.py", "checks.py", "audit.py", "pool.py", "elo.py"]:
    p = RO + "/scripts/topic_harness/" + f
    m.append(f"| research-ops topic_harness/{f} | {p} | harness-unify 代理（未合入 main，只读） | {sha(p)} | 只读包导入 |")
m.append(f"| research-ops RESEARCH-ENTRIES.md | {RO}/LITERATURE/RESEARCH-ENTRIES.md | harness-unify 代理 | {sha(RO + '/LITERATURE/RESEARCH-ENTRIES.md')} | 只读；冲突条款被 round/rules/EFFECTIVE-RULES-R2.md 取代（本线） |")
km = MAIN + "/LITERATURE/KNOWLEDGE-MAP.md"
m.append(f"| KNOWLEDGE-MAP.md（主库） | {km} | 主库（main） | {sha(km)} | 只读；生成入口用切片 round/knowledge/NEUTRAL-KNOWLEDGE-VIEW.md |")
m.append(f"| SOURCES.csv | {MAIN}/LITERATURE/SOURCES.csv | 主库（main） | {sha(MAIN + '/LITERATURE/SOURCES.csv')} | 只读 |")
m.append(f"| tao25.pdf | {MAIN}/tao25.pdf | 用户放置 | {sha(MAIN + '/tao25.pdf')} | 只读；身份=arXiv 2512.03211（内容为 2001 Olpomdp 经典重贴） |")
for f in ["patched_checks.py", "patched_audit.py", "patched_novelty.py", "ledger.py", "merge_sim.py", "deps_check.py", "gen_manifest.py", "gen_neutral_view.py", "test_rework_regressions.py"]:
    p = W + "/round/tools/" + f
    if os.path.exists(p):
        m.append(f"| 本线 {f} | {p} | agent/20260910-topic-loop | {sha(p)} | 本线自有 |")
kv = W + "/round/knowledge/NEUTRAL-KNOWLEDGE-VIEW.md"
if os.path.exists(kv):
    m.append(f"| 本线 NEUTRAL-KNOWLEDGE-VIEW.md | {kv} | agent/20260910-topic-loop | {sha(kv)} | 本线自有（程序化切片） |")
n = len(glob.glob(MAIN + "/LITERATURE/notes/raw/*.md"))
m.append(f"| notes/raw 规模 | {MAIN}/LITERATURE/notes/raw/ | 主库 | count={n}（目录级，文件级不固定） | 只读 |")
m.append("")
m.append("变更政策：任何依赖内容变化 → deps_check.py 报告 drift（exit 1），主控显式决定是否重指纹；禁止静默使用另一版。")
open(W + "/round/deps/DEPENDENCIES.md", "w", encoding="utf-8").write("\n".join(m) + "\n")
print("manifest regenerated:", len(m), "lines")