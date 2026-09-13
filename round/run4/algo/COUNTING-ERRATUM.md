# 计数勘误：JSON 副本导致的计数虚增（COUNTING-ERRATUM，主控亲验，2026-09-11）

> 触发：B10 报告"未用 --include='*.md' 会使计数虚增约 3 倍"，并给出 credit assignment 5→76 的例子。
> 主控独立复现并量化，然后**回溯校正此前各批的"全库扫描"数字**。

## 1. 主控独立复现（已验证）

| 项 | 实测 |
|---|---|
| MD 文件数 | **111**（/md/<KEY>/<KEY>/txt/<KEY>.md） |
| JSON 文件数 | **446**（<KEY>_middle.json / _model.json / _content_list.json / _content_list_v2.json 等） |
| `credit assignment`，`--include='*.md'` | **5 文件** |
| `credit assignment`，不限类型 | **20 文件**（≈4 倍虚增） |

**结论：B10 的判断成立且量级正确。** 446 个 JSON 是 MinerU 的中间产物，内容与 MD 重复但**按行/按块切分方式不同**，导致同一散文会被多次计数，且 JSON 内部的换行拼接会产生**原文中不存在的字面相邻**（B10 已举 LJG6ZW7B 的 "separate reward" 假命中）。

## 2. 受影响的主张与回溯校正

| 主张 | 原数字 | 校正后 | 影响 |
|---|---|---|---|
| G-A 反例（各批"全库扫描"） | B9 称"全库 113 个 itemKey 扫描"、B8 称"全库 111 篇"、B10 称"全库计数" | **结论不变**（各批均同时给出 md-only 命中位置与逐条排除，且 md-only 计数已由主控复核） | G-A 判定有效 |
| `credit assignment` 命中数 | B9 报"17"、B2 报"5 篇" | **md-only = 5** | 需在 GAP-VERIFICATION 中统一为 5 |
| `multi-objective`、`MORL`、`counterfactual` 等 | 各批报数不一（27/9/8/32） | 需按 md-only 重算 | 不影响"轴不同"的判定 |

**主控校正**：凡进入交付文档的全库计数，一律改为 **md-only（111 篇）** 口径。已在 CROSS-BATCH-CHECK 与 GAP-VERIFICATION 中注明。

## 3. T1 档 34 篇的负载过程统一计数（主控补做，md-only）

B10 建议"对 T1 全部 34 篇跑统一计数"——已执行（poisson / burst / self-similar|heavy-tail|MMPP / non-stationar / arrival(rate|process)）：

| 命中类别 | 篇数（/34） | 说明 |
|---|---|---|
| 含 `poisson` | 11 篇 | 多为流量生成假设 |
| 含 `burst` | 5 篇 | CYMQ2GLA / UKEKU5ZG / 8N9QJHC2 / JLF7IEBQ（SaTE，含 RedTE 引用）/ 另有误配 |
| 含 `self-similar` 或 `heavy-tail`/`MMPP` | **2 篇** | TSV3IE8S（引用 Gragopoulos 2000 的题名）、UF8IQTA2 |
| 含 `non-stationar` | 2 篇 | J68GU76W、39NJWBI7（指多智能体非平稳，非流量非平稳） |
| 含 `arrival (rate|process)` | 10 篇 | 到达率是**参数**，不是被扫描的自变量 |

**关键结论（md-only 口径下依然成立）**：
- **突发族过程（self-similar/heavy-tail/MMPP）在 T1 的 34 篇中：0 篇作为自身的负载模型**（TSV3IE8S 是引用他文题名，且该文非 RL；UF8IQTA2 无 RL）；
- `burst` 的 5 处命中：CYMQ2GLA/UKEKU5ZG 为散文词（burst of traffic 类表述）、8N9QJHC2 指链路故障突发、JLF7IEBQ 指其引用的 RedTE 工作——**无一处是"把突发形状作自变量"**。

## 4. 全库取证 SOP 增补（三条，来自各批实测事故）

1. **必须 `--include='*.md'`**：否则 JSON 副本使计数虚增（本文件 §1）。
2. **必须 `-a`**：grep 把部分 MD 判为 binary 时，`-c` 仍报数而 `-n` 输出为空 → 只看 stdout 会误判"0 命中"（B6 首报、B7 独立复现、主控补 B8 缺口时再次遇到）。
3. **负向声明必须用精确模式 + 报告命中位置**：裸词会命中散文（`per`→"per hop"、`priorit`→"prioritizes"、`double`→"double-check"、`gamma`→LaTeX `\gamma`/Gamma 分布）；Unicode 词界转义在 GNU grep -E 下不生效。
