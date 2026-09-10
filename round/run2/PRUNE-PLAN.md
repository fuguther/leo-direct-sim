# 修剪方案（PRUNE-PLAN v1.0，2026-09-11）——**需用户批准**

> 依据：AGENTS.md 第 5 条与第 9 条——**删除、移动任何已跟踪路径前必须逐条列出并等用户批准**。
> 现状：`round/tools/` 有 **45 个文件**，经交叉引用检测，**29 个零引用**；规则 **10 份**（1066 行）存在职责重叠；`ANALYSIS/.../run2/` 有 **v1/v2 两份交接包**并存。
> 目标：tools 45 → **18**；rules 10 → **8**（含把 1 份报告移出）；消除版本残留导致的误用风险。

---

## A. 删除（12 项，均为被取代或对应任务已废弃）

**A1 迭代残留的转换脚本（被 `vm_mineru_one.py` 取代）**
1. `round/tools/vm_mineru_batch.py`（首版，6 分片并行，已被取代）
2. `round/tools/vm_mineru_batch2.py`（两遍策略版，输出路径判断有 bug）
3. `round/tools/vm_mineru_batch3.py`（修路径版，仍被 `one.py` 取代）
4. `round/tools/vm_convert_pdfs.py`（pymupdf 方案，未采用）
5. `round/tools/vm_extract_evidence.py`（关键词抽取方案，未采用）
6. `round/tools/vm_mineru_quality_test.py`（vlm 对比测试，**用户已决定不跑 vlm**）

**A2 有已知缺陷的旧审计工具（v4 已修正，旧版会误报）**
7. `round/tools/audit_contamination2.py`（全文关键词计数，**假阳性**）
8. `round/tools/audit_reads.py`（正则错误，零命中）
9. `round/tools/audit_reads2.py`（同上）

**A3 被取代的抽查工具**
10. `round/tools/spotcheck_removed.py`（归一化缺失，**把重分段误判成删除**）

**A4 失效的监听脚本（对应任务已结束）**
11. `round/tools/watch_qtest.sh`（vlm 测试已放弃）
12. `round/tools/watch_vm_conversion.sh`、`watch_vm_v3.sh`（对应 batch/v3，已被 one.py 取代）

**A5 已废弃 / 重复**
13. `round/tools/ledger_add.py`（规则明写废弃，缺陷已复现存档）
14. `round/tools/merge_sim.py`（无引用）
15. `round/tools/HISTORY-REVIEW-PROMPT.md`（18 行，内容已并入 `rules/PROMPT-TEMPLATES.md` §3）
16. `round/tools/REVIEW-ROLE-PROMPTS.md`（31 行，内容已并入 §5）
17. `ANALYSIS/TOPIC-LOOP-20260910/run2/HANDOFF.md`（v1，已被 `HANDOFF-v2.md` 取代）

> 注：A1–A4 的**功能均已在现存文件中具备**，删除不影响任何执行路径。若你希望保留审计痕迹，可改为"移入 `round/tools/archive/`"（选项见 §D）。

---

## B. 归档（10 项，一次性任务已完成，保留证据价值）

移入 `round/tools/archive/`（或保持原位但标注"已完成"）：

1. `fix_chu.py`（CHU 笔记定点修复，已应用）
2. `revert_backfill.py`（回退误回补，已执行）
3. `neutral_residual_fix1.py`、`neutral_residual_fix2.py`（倾向句清除，已应用）
4. `backfill_facts_min.py`（承重事实回补，已应用）
5. `annotate_confound.py`（CMNCS52M 混淆标注，已应用）
6. `freeze_neutral_hashes.py`（指纹固化，已执行；后续若有变更需重跑）
7. `corpus_gap.py`、`check_local_paths.py`、`zotero_compare.py`（语料缺口诊断，一次性）
8. `spotcheck_removed2.py`（语义抽查，已在报告中引用结论）
9. `audit_reads2.py`（读取统计，结论已入 dispatch 记录）

---

## C. 规则文件整理（10 → 8）

| 文件 | 处置 | 理由 |
|---|---|---|
| `CHAIN-AUDIT.md` | **移出 rules** → `ANALYSIS/TOPIC-LOOP-20260910/run2/`（与 FRAMEWORK-SELFCHECK 同处） | 是一次性审计报告，不是活规则 |
| `QUALITY-GATE-R2.md` + `LOOP-CONTROLLER.md` | **合并**为 `QUALITY-GATE-R3.md` | 前者说"怎么判"，后者说"循环几次"，属同一议题；两处都写"≤3 轮"存在重复 |
| 其余 8 份 | 保留 | 各司其职 |

**合并后规则清单（8 份）**：
`TOPIC-SELECTION-METHOD.md`（总纲）、`EFFECTIVE-RULES-R2.md`（强制规则）、`QUALITY-GATE-R3.md`（闸门+循环）、`EXPLORATION-FALLBACK.md`（失败升级）、`UNDERMIND-PLAYBOOK.md`、`MINERU-CONVERSION-SOP.md`、`ROUTE-POLICY.md`、`PROMPT-TEMPLATES.md`

---

## D. 请你选择处置强度

| 选项 | 动作 | 影响 |
|---|---|---|
| **① 保守**（推荐） | 只做 §C 规则整理 + §B 归档；**不删任何文件**；在 FRAMEWORK-MAP 中标注"A1–A5 为已废弃，勿使用" | 零风险；但 tools/ 仍有 45 文件，新会话需靠文档辨别 |
| **② 标准** | §C + §B + **§A 中 A2/A3/A4/A5（11 项）删除**（有缺陷或纯重复），A1（6 个转换脚本）归档 | 删的是"有已知缺陷/纯重复"的，证据价值低 |
| **③ 彻底** | §C + §B + §A 全部 17 项删除 | tools 45→18；最干净，但丢失迭代痕迹（git 历史仍可追） |

**我的建议：②标准**。理由：A2/A3/A4/A5 属于"旧版有已知缺陷会误用"或"纯内容重复"，留着是**风险**而非资产；A1 是转换脚本的迭代史，归档即可。

---

## E. 不做的事（避免过度整理）

- **不动** `ANALYSIS/` 下的平台/实验类文档（非本任务产物，属其他工作线）；
- **不动** `round/run1/`、`round/miniflow*/`、`round/staging/`（历史轮次证据）；
- **不动** `LITERATURE/` 下任何内容（含 raw 笔记——它们是审计底本）；
- **不重构** 任何工具的代码（只在必要时改路径引用）。

---

## F. 批准后我会执行的动作（逐条可核对）

1. `git rm` 选定的文件（选项②=11 项）；
2. `git mv` A1 六项 → `round/tools/archive/`；
3. 合并 `QUALITY-GATE-R2` + `LOOP-CONTROLLER` → `QUALITY-GATE-R3.md`，并更新所有引用；
4. `git mv round/rules/CHAIN-AUDIT.md ANALYSIS/TOPIC-LOOP-20260910/run2/`；
5. 更新 `TOPIC-SELECTION-METHOD.md` 的文件索引表；
6. 重跑回归（12/12）与 `deps_check`（指纹一致性）；
7. 提交 + push，并在 `FRAMEWORK-MAP.md` 记录本次修剪结果。
