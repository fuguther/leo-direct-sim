# 选题方法论总纲（TOPIC-SELECTION-METHOD v1.0，2026-09-10）

> **本文是选题工作的单一入口**。所有规则文件、流程图、台账、模板的作用与位置在此索引；新人/新会话读这一份即可上手。
> 目标读者：主控 Agent、子代理提示词作者、Codex/人工审核者。

---

## 0. 目标与范围

**研究范围（用户锁定）**：低轨卫星网络中，**负载变化**下强化学习路由如何保持良好的**到达率**与**端到端时延**。

**本轮任务**：在这个方向内形成一条**有充分理由值得开展、能向老师讲清楚**的研究主线——不是跑实验，不是写论文。
**产出形态**：1 条主线（+ 至多 1 条独立备选），附三问答案、机制图、验证设计、最近读差异、取舍记录。
**允许的产出**：**"无合格主线"**及其卡点报告（这是设计中合法的成功，不是失败）。

---

## 1. 什么叫"合格的选题"（可判据定义）

一张卡只有在**五道闸门**下全部通过，才算合格：

| 闸门 | 判据（简版） | 详见 |
|---|---|---|
| **G1 现象成立** | ≥1 条原文事实（回全文，给节号/表号）+ ≥1 独立第二来源或明确"单一来源"；四档标注清晰；**"论文没测"≠"论文做不好"** | QUALITY-GATE-R2 §1 |
| **G2 原因有依据** | 机制链完整（条件→量变→哪一步失效→到达率/时延受损）；**排除≥1 个竞争解释**；跨论文可比性检查通过 | 同上 |
| **G3 改动对症** | 先辨因再选法；能写出**一次具体决策或学习更新**；写明失效条件；不以模块数衡量创新 | 同上 |
| **G4 简单办法为何不足** | 在信息/预算/条件**对齐后**比较：混合负载训练、在线微调、已有信息、规则路由、直接近邻；须存在"尚存困难+机制依据" | 同上 |
| **G5 最近邻差异** | 库内+外部双向查新；无未处理的直接对手；差异按四要素表述 | 同上 |

**致命项一票否决**：G1/G2/G4/G5 任一被判死且未消除 → 不得进入推荐。**迭代 ≤3 轮，超限淘汰**（不靠改名/加条件/补风险声明续命）。

**合格选题还应具备**（软标准，供人工/Codex 判断）：
- 能用一句话向老师说明"现有方法在什么条件下为什么不够"；
- 验证设计的第一步行**半天到两天可完成**，且负结果也有意义；
- 机制图能走通**一次决策 + 一次学习更新**。

---

## 2. 流水线（步骤与角色；**权威定义在 EFFECTIVE-RULES-R2 §8**，本节仅为索引）

> R5 修正：本节原写「十步」，与 §8 的段数不一致。**冲突时以 §8 为准**；下表仅列角色与输入输出，编号不代表权威顺序。

见 `ANALYSIS/TOPIC-LOOP-20260910/run2/PIPELINE-MAP.md` 的流程图。文字版：

| # | 步骤 | 角色（上下文） | 输入 | 输出 |
|---|---|---|---|---|
| ① | 生成 | 生成器 ×3（**全新子对话，互不可见**） | 白名单 v4：ZOTERO-INDEX(111) / notes-neutral / 中性视图 / PDF / Undermind | 0–4 卡 + 放弃线 + 防火墙声明 |
| ② | 初筛 | 主控 | 全部生成产物 | 去重合并 → `ledger.py add` 入账 |
| ②b | **独立污染审计** | 主控跑工具 | 子会话 `tool/call` 日志 | 违规→**该批作废重跑** |
| ③ | **历史碰撞审查** | 审查者（**全新子对话**） | 候选固定版本+指纹 + HISTORY-INDEX + **ELIMINATED-REGISTER** | 五类裁决 + 死因依据 |
| ③b | **死因回传** | 主控摘录 | 审查结论 | **有限反馈文件**（must-address）交深化者 |
| ④ | 深化 | 深化者（**全新子对话/每卡**） | 本卡 + 本卡死因反馈（**禁历史全集**） | 三问答案 + 承重引文回原文 |
| ④b | 近邻核查 | 深化者 + 主控 | patched_novelty（四态）+ Undermind `citing` | 四要素差异表述 |
| ⑤ | 三角色审查 | builder/neighbor/evidence（**各新子对话**） | 该卡 | 逐条 PASS/REVISE/KILL |
| ⑥ | **质量闸门** | 主控 + 判定表 | G1–G5 | 过 / 修订(≤3轮) / 淘汰 |
| ⑦ | 推荐裁决 | 主控 | 全部门禁记录 | recommended_pending_review / awaiting_evidence / 淘汰 |
| ⑧ | 交付 | 主控 | — | 五件套（见 §5） |
| ⑨ | 台账追加 | 主控 | 本轮淘汰/中止/合并 | ELIMINATED-REGISTER §6 |
| ⑩ | 下一轮 | 主控 | — | 生成仍**全新上下文**；失败理由**不回流生成端** |

---

## 3. 四条核心原则

### 3.1 证据防火墙（隔离）
- 生成器**只读论文事实**，绝不读历史候选、旧排序、淘汰理由、其他生成器的卡面；
- 违反 → 产物**作废重跑**（不是"标注一下继续用"）；
- 完整隔离矩阵见 EFFECTIVE-RULES-R2 **§8.1**；审计工具 `audit_contamination4.py`（只判路径参数位，已修掉三代误报）。

### 3.2 死因必须闭环（防"不断选出旧题"）
生成隔离 → 历史审查（判撞车+给死因）→ **死因作 must-address 回传深化者** → 未逐条处理+新证据 → 不得推荐 → 淘汰登记 → 下轮仍隔离。
**任一环缺失，该轮选题视为未完成。**

### 3.3 三类淘汰分开记（历史审查最常犯的错）
- **A 证伪/覆盖**：有外部证据 → 真淘汰（可能带复活条件）
- **B 流程中止**：因防火墙/审批/入口重置停止 → **不是对该问题的否定**
- **C 合并吸收**：并入更大卡，资产保留 → **不是淘汰**
详见 `ELIMINATED-REGISTER.md`（含 §5 复活条件登记表：哪些"条件"至今无人执行）。

### 3.4 判断可信度优先于产出数量
- 关键词清零 ≠ 内容中立（实测 15 处隐含旧判断残留）；
- 自证声明 ≠ 证据（污染审计独立跑日志）；
- "程序未能检查" ≠ "确实找到反例"（检查器四态：PASS/BLOCK/NOT_APPLICABLE/INPUT_INSUFFICIENT）；
- 空/畸形绑定一律拒绝（防"永不过期的陈旧意见"，回归 T13）。

---

## 4. 语料与证据通道

| 通道 | 规模 | 用途 | 文档 |
|---|---|---|---|
| **Zotero 本机库** | **111 篇，全部有 PDF** | 库内精读主力 | `round/zotero/ZOTERO-INDEX.md` |
| MinerU 转 MD（VM） | 111 篇（进行中） | 高质量全文（表格/公式/结构） | `round/zotero/VM-CONVERSION-LOG.md` |
| notes-neutral | 41 篇 | 事实笔记（倾向已剥离） | `round/knowledge/notes-neutral/` |
| SOURCES.csv | 52 篇题录 | 旧题录（`local_path` 已全部悬空，不可信） | `round/knowledge/CORPUS-COVERAGE.md` |
| **Undermind** | 外部语料 | 发现/查新/引用网络/跨论文问答 | `round/rules/UNDERMIND-PLAYBOOK.md` |
| 本地 PDF | 14 篇（主库） | 遗留通道 | — |

---

## 5. 交付形态（每轮）

1. `MAIN-REPORT.md` 一页主报告（最值得继续的问题，直答三问）
2. `PROPOSAL.md` 完整文稿（场景→不足→原因→改动→近邻差异→验证设计）
3. 机制图（Mermaid，能走通一次决策+一次学习更新）
4. `LITERATURE-GUIDE.md`（核心文献 + 承重原文位置）
5. `TRADEOFF-LOG.md`（取舍记录：比较过哪些实质不同问题、什么证据改变判断、为何推荐）
6. （若适用）**未通过项与淘汰原因单列**，与推荐项同等显著

---

## 6. 文件索引（按用途）

| 用途 | 文件 |
|---|---|
| **单一入口（本文）** | `round/rules/TOPIC-SELECTION-METHOD.md` |
| 流水线与隔离矩阵（**权威**） | `round/rules/EFFECTIVE-RULES-R2.md`（§2 白名单 v4、§8 流水线含 §8.0 批内对账/§8.0.1 锚件核验、§8.1 隔离矩阵） |
| 全框架结构图与体检 | `ANALYSIS/TOPIC-LOOP-20260910/run2/FRAMEWORK-MAP.md`（九个子系统流程图 + 矛盾清单） |
| 闸门机械判定 | `round/tools/gate_check.py`（PASS/BLOCK/INPUT_INSUFFICIENT） |
| 轮次硬计数 | `round/tools/gate_rounds.py`（≤3 轮，超限硬拒绝） |
| 路线与降级链 | `round/rules/ROUTE-POLICY.md` |
| 断点审计报告 | `round/rules/CHAIN-AUDIT.md`（一次性报告，非活规则） |
| 质量闸门 | `round/rules/QUALITY-GATE-R2.md` |
| 失败后怎么办 | `round/rules/EXPLORATION-FALLBACK.md` |
| Undermind 用法 | `round/rules/UNDERMIND-PLAYBOOK.md` |
| 流程图 | `ANALYSIS/TOPIC-LOOP-20260910/run2/PIPELINE-MAP.md` |
| 淘汰台账 | `round/history/ELIMINATED-REGISTER.md` |
| 历史全量索引 | `round/history/HISTORY-INDEX.md` |
| 语料覆盖真相 | `round/knowledge/CORPUS-COVERAGE.md` |
| 语义抽查记录 | `round/knowledge/P0-SEMANTIC-SPOTCHECK.md` |
| 台账工具 | `round/tools/ledger.py`（add/revise/status/merge/review-register/invalidate） |
| 输入链净化 | `round/tools/sanitize_notes.py`（raw→notes-neutral 剥离倾向句）+ `gen_neutral_view.py` |
| 语料构建 | `round/tools/gen_zotero_index.py`、`zotero_pdf_manifest.py`、`stage_zotero_pdfs.py`、`build_citekey_crosswalk.py` |
| VM 转换 | `round/tools/vm_mineru_one.py`（逐篇串行，唯一活跃转换脚本） |
| 依赖指纹 | `round/tools/gen_manifest.py`、`deps_check.py` |
| 查新/检查/审计工具 | `round/tools/patched_novelty.py` / `patched_checks.py` / `patched_audit.py` |
| 污染审计 | `round/tools/audit_contamination4.py` |
| 回归测试 | `round/tools/test_rework_regressions.py`（13 项） |
| 闸门/反馈模板 | `round/run2/gates/GATE-TEMPLATE.md`、`round/run2/feedback/FEEDBACK-TEMPLATE.md` |

---

## 7. 反面清单（明令禁止）

1. 把"流程跑完/文件齐全/审查有意见"当作通过证据；
2. 把"性能收益待验证"当作免责声明反复使用（G3/G4 必须有机制级理由）；
3. 用弱化基线创造空间；
4. 用改名/加条件/缩小场景/"这次做消融"维持推荐；
5. 因一张卡失败就推翻整个研究方向；
6. 把"未命中"写成"无人做过"（Undermind 原文明确：窄结果≠文献不存在）；
7. 把 B 类（流程中止）与未裁决项当作科研否定；
8. 让深化者拿到历史全集（等于把污染从生成端搬到深化端）。
