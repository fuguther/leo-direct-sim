# 研究生成入口合同（2026-09-10）

> 对生成、比较、续作三个阶段，本页是**唯一入口清单**；违反即视为锚定污染。
> 依据与全景论证：GROUP-MEETINGS-LOCAL/90-RAW-INBOX/RESEARCH-HARNESS-BORROWING-20260910.md（第 1.4、5 节）。
> 背景：run-20260910 的生成入口指向旧 44 条笔记索引，夜间书单全部落在"有笔记/有 PDF"的熟面孔上；候选无跨 run 台账，旧题改名即可重现。

## 允许入口（生成阶段可用）

1. `LITERATURE/SOURCES.csv` —— 论文总目录（身份/访问/核验状态），扩库在此发生。
2. Zotero storage —— 身份与附件（只读研究 PDF/文献附件）。
3. `LITERATURE/notes/raw/` —— 已去倾向笔记（20260910 清理后），只当线索；承重断言一律回原文。
4. `LITERATURE/KNOWLEDGE-MAP.md` —— 主张/假设/证据三图（SUPPORTING）。
5. `out/research-ops/candidates/ledger.csv` —— 候选台账，仅用于"重现必须携带新证据"的判定，不得当推荐源。

## 禁止入口（发现/比较/续作阶段一律不得读取）

- `literature-index.csv`（旧 44 条笔记索引，run-20260910 的污染入口；路径位于已结束会话工作区）。
- `RECONCILED-LIBRARY.csv`（当前不可寻；再现须先过身份核验）。
- 已归档旧选题目录（.r2~.r8stage，现位于 archived-topic-stages-20260910）。
- 任何历史 run 的 hypotheses.md / draft-*.md / REPORT.md 作为生成输入。
- `ANALYSIS/` 旧候选排序、`OVERNIGHT-REPORT-*` 等历史汇报。

## 阅读分配硬规则

- 每轮阅读清单中"**无笔记论文**"占比 ≥40%（runbook 内可机检）。
- 每轮至少一次 Undermind 定向补查，只回答两个问题：a) 当前判断所缺的证据；b) 最强替代方法。不做"这个点有没有人做"式检索。

## 产出合同

- 新候选必须入池：`out/research-ops/candidates`（`scripts/topic_harness/pool.py`：只添不改；旧键重现须带 new_evidence）。
- 候选排序用 `scripts/topic_harness/elo.py` 调度（相似优先、高分多轮、同对复赛≤2）。
- 审查前先跑 `PYTHONPATH=. python3 -m scripts.topic_harness.audit`：误放/误杀必须为 0。
- 承重断言分层标注【原文事实/作者解释/代码事实/推演/待证】（沿用 run-20260910 约定）。
