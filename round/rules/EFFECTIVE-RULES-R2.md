# 本线有效入口规则（EFFECTIVE-RULES R2，2026-09-10）

> **权威声明**：在 `agent/20260910-topic-loop` 工作线上，本文件是选题流程入口规则的**唯一有效来源**。
> 其他入口文档与本文件冲突时，以本文件为准；本文件未规定的事项回落到仓库 AGENTS.md / LITERATURE/README.md 防火墙。
> 依据：Codex+Luna 架构深审裁决（2026-09-10）+ 返工包第一组。复现与证据：`round/logs/`。

## 1. 被本文件取代的旧条款（消除多套权威）

| 旧条款 | 出处 | 处置 | 理由 |
|---|---|---|---|
| "候选排序用 elo.py 调度（相似优先、高分多轮、同对复赛≤2）" | research-ops RESEARCH-ENTRIES.md 产出合同 | **本线作废**。Elo 不得参与推荐或淘汰；相似度只作合并线索 | 主报告裁决 + 2026-09-10 workbuddy 独立评审：15 局 K=24 名次差 ≪ 置信区间，排序无信息量 |
| "允许入口 #4：LITERATURE/KNOWLEDGE-MAP.md" | RESEARCH-ENTRIES.md | **本线替换**为 `round/knowledge/NEUTRAL-KNOWLEDGE-VIEW.md`（程序化切片，行号溯源） | 原 KNOWLEDGE-MAP 含旧候选 A-D 关系段与旧"未找到"检索结论；三路生成器实测全部撞见（各自文件内声明） |
| "允许入口 #5：out/research-ops/candidates/ledger.csv（生成阶段可用）" | RESEARCH-ENTRIES.md | **本线收窄**：任何候选台账（旧卡与本线卡）仅用于**生成后**的复现对账，禁止作为生成输入 | 旧候选正文/排序属防火墙禁止项 |
| "验收=入池≥6 / unnoted≥40% / 误放0误杀0" | run-test-20260910 验收线 | **本线作废**为验收；阅读覆盖与来源分布仅作诊断记录 | 无笔记占比/卡数/小测试集零误判均不可决定推荐或验收（深审第一组） |
| "Undermind 只查缺口证据+最强替代" | RESEARCH-ENTRIES.md | **维持**（限额≤3 次/生成器不变） | 与返工包不冲突 |

> 同步义务：research-ops 线的 RESEARCH-ENTRIES.md 归 harness-unify 代理所有（单写入者，本线不改其文件）。
> 其 owner 后续合入时应参照本表对齐；在此之前，本线一切生成/审查活动以本文件为准。

## 2. 生成阶段知识入口（白名单 v3，2026-09-10 run2 修订）

> v2→v3 原因：Codex 内容审核发现 raw 笔记仍含 F0/F1、旧候选与『我们的机会点』内容，与『已去倾向』声明不一致（实测 41 篇中 15 篇 30 处命中）。run1 生成器实际经 raw 笔记浏览 14 篇，暴露属实，已记入 ROUND-LOG §13。v3 起 raw 笔记移出生成入口，仅保留给生成后历史审查。

1. `LITERATURE/SOURCES.csv`（论文总目录）
2. `round/knowledge/notes-neutral/*.md`（程序化剥离倾向句的事实笔记，manifest: `round/knowledge/notes-neutral-manifest.json`，含源文件 sha256 与删除统计；只当线索，承重断言回原文）
3. `round/knowledge/NEUTRAL-KNOWLEDGE-VIEW.md`（中性事实视图——Claim/Assumption/Evidence 三图 + 全文阅读证据表；不含候选关系与旧未找到判断）
4. Zotero 本机库（"毕设"集合等）
5. 本地 PDF：`LITERATURE/papers/`、`tao25.pdf`（身份=arXiv 2512.03211，内容为 2001 Olpomdp 经典）
6. Undermind search_papers（定向补查 ≤3 次；禁 launch_deep_search）、arXiv API、web 搜索

**黑名单（生成阶段禁止读取）**：`out/**`、其他代理 worktree 产物、`LITERATURE/notes/raw/*.md`（v3 起移出，倾向句未清除）、`LITERATURE/notes/COLDSTART-20260903.md`、`00-READING-QUEUE.md`、`related-work-notes/`、**任何候选台账（旧卡与本线卡）**、**原版 KNOWLEDGE-MAP.md**、`ANALYSIS/**`、`NOTES.md`、`PAPER/**`、历史 run 报告。

**留给生成后比较阶段**：旧候选关系、旧排序、旧"未找到"判断——由主控在合并对账时使用并判定旧判断是否仍然成立、是否适用。

## 3. 查新与检查器判断权限（本线强制）

- 查新一律用 `round/tools/patched_novelty.py`：四态检索状态（ok_hits/ok_empty/service_unavailable/exec_error）；失败 → incomplete，**失败不构成无先例**；成功无命中只支持"限定范围内未命中"；输出=近邻线索+证据+未决项，**不认证科研新颖性**；服务失败即停（断点+未执行查询清单）。
- 相似度（标题/文本 Dice）只产生 **lead**（线索），值域 high/mid/low_similarity_lead；**不自动判同一工作、不自动淘汰**。"覆盖"判断必须由主控/审查者比对〔条件/困难/机制/决策变化〕并保留依据。
- 机械检查一律用 `round/tools/patched_checks.py`：判定级 PASS / BLOCK / NOT_APPLICABLE / INPUT_INSUFFICIENT；占位文本（TODO/待补/空）→ INPUT_INSUFFICIENT，**不产生 PASS 也不冒充科研否定**；缺输入 → 报"未检查"。
- 审计一律用 `round/tools/patched_audit.py`：执行错误/未知检查器/参数错误独立记账并使验收失败；**"程序未能检查"≠"确实找到反例"**。

## 4. 台账与修订语义

- 唯一 CLI：`round/tools/ledger.py`（`ledger_add.py` 已废弃，缺陷复现存档）。只追加；cand_id 稳定；当前版本=最大 version；content_hash 幂等（重试/同批不重复入账）；修订=新版本行+supersedes_row；承重字段变化自动把审过旧哈希的意见置 needs_review。触发口径（R4 精化）：非承重字段修改不触发；承重字段仅纯空白差异不触发；承重字段的标点/符号/小数点变化即触发。
- 状态词表：`backlog(待建设) / awaiting_evidence(待证据) / needs_revision(需修订) / recommended_pending_review(推荐待审) / archived(归档) / merged(合并簿记)`。**"文件已交付"≠"科研通过"**。
- 旧题匹配只报告不淘汰：old_topic_match 字段 + stdout 提示，处置由主控核对旧判断后决定（保留/修订/合并/归档），并留理由。
- new_evidence 非空必须携带 new_evidence_source 与 evidence_judgment（主控判定），否则 CLI 拒绝（fail-loud）。

## 5. 审查绑定版本

- 每份审查意见登记于 `round/reviews/reviews.csv`：review_id / cand_id / 所审 ledger_content_hash 与候选文件 sha256 / 角色 / 文件路径 / 状态(active|needs_review|superseded)。
- 同模型不同角色 = **互补意见**，不声称天然独立；异模型通道当前不可用（chatgpt_dispatch 插件故障，已记录）。
- 建设者输出独立修订建议，主控整合后才写入台账（审查者禁止修改生产者原件）。
- 承重变更 → 相关旧意见自动 needs_review；非承重字段修改不触发；承重字段仅纯空白差异不触发（标点/符号/小数点变化即触发）。
- 审查登记双哈希（R4 补强）：reviews.csv 同时记 ledger_content_hash（台账字段哈希，--verify-ledger 校验存在性）与 candidate_file/candidate_file_sha256（被审候选文件+工具实算 sha256）；登记缺一即拒绝。

## 6. 依赖固定

- 全部承重组件指纹见 `round/deps/DEPENDENCIES.md`；`round/tools/deps_check.py` 漂移检查（exit 1 = 必须显式报告并决定，不静默换版）。

## 7. 验收方式（替代旧验收线）

- 本线验收 = 离线回归（`round/tools/test_rework_regressions.py`，10 项）+ 单卡完整小流程留痕 + 证据链抽查，全部以真实执行记录为准；
- 阅读覆盖、来源分布、卡数只记录、只诊断，**不构成任何通过/推荐依据**；
- 推荐与否由主控依据证据裁决（原工作包规则），任何评分/名次不得替代。
## 8. 历史碰撞审查（R3 新增：位于初筛之后、近邻核查与深化之前）

**流水线**：独立生成 → 初筛 → **历史碰撞审查** → 近邻核查与深化 → 内容审查 → 推荐。

- 历史审查子代理：**全新上下文**（不得读主控推理链、不得读生成端对话）；输入=当前候选固定版本（文件+指纹）+ [round/history/ELIMINATED-REGISTER.md]（**淘汰清单唯一权威入口**；三类分离：A 证伪 / B 流程中止 / C 合并吸收）+ [round/history/HISTORY-INDEX.md]（全量索引与失败原因货币性）+ 按需读取原件权限（索引指向的 git show 命令/文件路径）；**只审历史重合与旧理由适用性，不替候选选新题**。
- 比较基准=**条件、困难、原因、机制、决策变化**五元组；标题/主题词相似只作定位线索。
- 输出五类（定义见 HISTORY-INDEX §6）：①未发现实质重合 ②同族但机制/适用条件实质差异 ③实质重复但新证据可能改变旧判断 ④实质重复且旧失败理由仍直接适用 ⑤历史依据不足或冲突，弃权。
- 反馈格式（逐条）：匹配对象 / 具体重合点 / 旧失败理由与出处 / 对新候选是否适用 / 建议处置。
- 第四类经主控核实后停止该卡深入；第五类=弃权，不得冒充否定；第①类≠科研新颖性通过（近邻核查仍须做）。
- 新证据必须能改变旧论证；换名称、加模块、缩小场景、"这次做消融"本身不构成重新推荐理由。
- 候选核心机制修订后**重新历史审查**；意见经 review-register 绑定候选版本（content_hash）。
- **淘汰理由必须回传深化者**：审查判 ④（旧失败理由仍直接适用）或带条件判 ②③ 时，主控把「撞的是谁 / 为什么不行 / 旧依据出处 / 本卡若要存活必须处理什么」写成**有限反馈文件**交给该卡深化者，作为 **must-address 项**；未逐条处理并给出新证据的卡**不得进入推荐**。
- **反馈文件不得夹带历史全集**：深化者收到的反馈只含与本卡相关的条目，禁止把 HISTORY-INDEX / 淘汰台账整份交给深化者——否则深化者会照着旧题改，等于把污染从生成端搬到深化端。
- **失败理由只回传到该卡为止**：下一批生成仍用全新上下文，历史失败理由**不回流生成端**；新生成器只能通过白名单 v3 读论文事实。
- **台账追加义务**：每轮结束由主控把本轮淘汰（A）、中止（B）、合并（C）追加进 round/history/ELIMINATED-REGISTER.md 的 §6，写明类型/依据/是否带复活条件；台账**永不进入生成端可见范围**。
- **防「不断选出旧题」的闭环**：生成隔离（生成器不读历史）→ 初筛 → 历史审查（判撞车 + 给死因）→ 死因回传深化者作 must-address → 未处理即淘汰并登记 → 下轮生成仍隔离。任一环缺失，该轮选题视为**未完成**。
- 索引"原因货币性"被新证据推翻时主控修订索引 §5 并留痕，不改写历史原文。
### 8.1 输入隔离矩阵（防污染，逐格可查）

| 角色 | 论文事实（SOURCES/notes-neutral/PDF） | 当前候选卡 | 历史索引与淘汰台账 | 淘汰死因反馈 | 主控推理链 |
|---|---|---|---|---|---|
| 生成器（新子对话） | ✅ 唯一知识来源 | ❌ 不读（含同批其他卡卡面） | ❌ **绝对禁止** | ❌ 不读 | ❌ |
| 初筛（主控） | ✅ | ✅ 全批 | ✅ | — | — |
| 历史审查者（新子对话） | 按需（判断旧理由是否被新证据推翻） | ✅ 该卡固定版本+指纹 | ✅ **必读**（台账+索引） | — | ❌ |
| 深化者（新子对话） | ✅ | ✅ 仅本卡 | ❌ 不读全集 | ✅ **只读本卡有限的死因反馈（must-address）** | ❌ |
| 三角色审查者（新子对话） | ✅ 按需回原文 | ✅ 该卡 | 仅涉历史重合时由主控按需投喂相关条目 | ✅ 相关 | ❌ |

**判定要点**：
1. 生成器若接触任何历史候选或淘汰理由 → 该批生成**作废重跑**（不是标注一下继续用）；
2. 深化者若拿到历史全集 → 该卡深化**作废重跑**（避免照旧题改）；
3. 历史审查者**不得**替候选选新题、不得给出应该改成什么的方案——只判撞车与死因；
4. 每次派发在 DISPATCH-RECORD 登记：角色、是否新上下文、实际投喂文件清单（可审计）。