# 选题循环 ROUND-LOG（2026-09-10，agent/20260910-topic-loop）

> 本文件是本轮主控台账与过程记录主入口；最终交付时由 PROCESS-APPENDIX 引用。单一事实源，不另设"最终版"。

## 0. 开工声明（2026-09-10 18:4x）

体检:6/6 结构通过,附 4 项环境注意 = [主 checkout 非clean(LITERATURE/notes 未提交修改,属他者工作流,本轮不触碰); .worktrees/research-ops 为他人活跃 checkout(harness-unify),只读; 治理检查 2 项 STALE_CURRENT(FINDINGS-REGISTRY.md / experiment-program.yaml,均实验域文档,选题轮不依赖→按规范记 UNVERIFIED 不沿旧结论执行); literature_search 插件本会话未暴露(不可用,记录)]。
通过项: cwd=目标目录; DSH Web 3080 响应(401=需鉴权正常); node v25.8.2 / python3 3.14.2 / ffmpeg / pypdf 可用; workspace-write 沙箱满足; github.com 与 arxiv.org 可达; Undermind MCP 可用(账号 torak1024@gmail.com); Zotero 可用(集合"毕设"44条); 上下文水位充足。

## 1. 暴露声明（防火墙合规）

主控在生成器派发【前】未读取任何旧候选正文；派发【后】、合并前，因职责所需接触：
- .workbuddy/memory/2026-09-10.md（harness 独立评审纪要）——含 run-test-20260910 验收缺陷判据；
- out/research-ops/run-test-20260910/ARCH-BRIEF.md 头部 60 行（架构自述）；
- out/research-ops/candidates/ledger.csv 头 12 行（旧候选 12 卡中 3 卡的字段内容）；
- LITERATURE/KNOWLEDGE-MAP.md 全文（含 2026-09-03 冷启动轮 A/B/C/D 候选的碰撞结论段）。
锚定风险：主控知晓旧候选存在性与部分主题词。处置：①三路生成器提示词在接触上述材料前已锁定且未含旧候选信息；②候选合并/对账/近邻核查由主控承担并在此声明；③推荐裁决只基于本轮新证据与近邻核查结果，旧候选无优先权也不因存在而自动排除。

## 2. research_ops 组件核验记录（2026-09-10）

对象：.worktrees/research-ops/scripts/topic_harness/{retrieve,dedup,novelty,checks,pool}.py（owner=harness-unify 代理，未合入 main，本会话只读执行）。
- retrieve.py：S2 客户端可导入；live 检索返回空——取证：直接 curl S2 search API → HTTP 429（公共档限速），环境无 LEO_S2_API_KEY/S2_API_KEY。结论：S2 公共档当前不可依赖，本轮近邻核验主通道=Undermind search_papers + arXiv API + 本地库；S2 有 key 后为补充。
- dedup.py：dice_same=1.0 / 两篇不同论文笔记=0.232 / 单词替换近重复探针=0.996；sentence-transformers 不可用→按设计退化 Dice(0.6)。限制：换名不换内容的语义同族在 Dice 回退下基本测不出，该风险由主控按"困难-原因-决策变化"人工合并兜底。
- novelty.py：确定性查询抽取可用（质量一般，作召回网）；其 S2 判定链受同一 429 限制。
- checks.py：6 类机械检查器可导入（M/M/1、固定权重⇒固定动作反例、可退回基线、相关≠因果、有界否定、对照网格）。
- pool.py：未直接写入他者 worktree（单写入者规则）；本轮复用其 CandidateCard 15 字段 schema 与 merge_key=(困难,原因,决策变化)，台账落在本轮 worktree 的 round/CANDIDATE-LEDGER.csv（入库可审计）。
- 独立评审结论采用：Elo 取消排序权（workbuddy 2026-09-10 纪要 + 本工作包"不按票数/Elo/自评分推荐"），dedup 相似度仅作合并线索。

## 3. 派发台账

| # | 时间 | 执行体 | 目的 | 关键未知 | 回传证据 | 状态 |
|---|---|---|---|---|---|---|
| D1 | 09-10 | subagent A (c50de73b) | 场景与学习原理推演：把场景压力点翻译成学习机制失败模式 | 哪些场景困难未被机制级解释 | round/staging/path-A-scenario.md | 运行中 |
| D2 | 09-10 | subagent B (3e83c394) | 文献实际行为：作者解释的失败/张力→机制假设 | 文献自述的行为反常何在 | round/staging/path-B-literature.md | 运行中 |
| D3 | 09-10 | subagent C (aaf17ff2) | 方法迁移与假设检查：迁到LEO什么假设破、需何实质改动 | 哪些迁移是实质而非贴标 | round/staging/path-C-transfer.md | 运行中 |

派发合规：并行=3（上限3，目的互独立）；未同时派发重复全文精读；生成器收 到=研究目标+资源边界+证据规范+RESEARCH-ENTRIES 白名单入口，未收 到=旧候选正文/排序/淘汰结论/平台功能清单。

## 4. 主控决策记录（增量）

- 2026-09-10：S2 429 → 近邻核验通道切换（见§2）。
- 2026-09-10：chatgpt_dispatch health 探测异模型审查可用性（结果追加于下）。
- 2026-09-10：chatgpt_dispatch health 失败。事实：工具返回 invalid output: missing required property "value.note"（工具输出契约错误，非登录/配额错误）。结论：本会话异模型审查通道不可用；处置：审查采用同模型三角色分离（建设者/近邻替代审查者/证据审查者），不可用性记录于过程附件，最终独立审核留给 Codex。失败分类：工具/配置问题（插件输出 schema），未重试第二次。
## 5. 证据链真实抽查（2026-09-10，最小闭环能力#2/#3）

- 探针1（HE-2025-PRIMAL.pdf p9）：Table I 定位成功，列结构与笔记描述一致（Throughput/Drop Rate/E2E Delay/Queuing Delay/Load Balancing/CVaR）；笔记预警的 std 异常（62.0±85.0 ms）在原文确认。行级断言（学习算法交付损失接近零）未逐行核验 → 记"部分核验"，留证据审查角色补全。
- 探针2（LIAQ-2026-QARR.pdf p1 摘要）：笔记断言"Dijkstra 在部分时延与韧性指标上仍有竞争力"获原文直接支持（"Dijkstra achieves the lowest end-to-end latency under ideal conditions"）。结论：笔记→原文定位链路可用；小样本 2/2 定位成功，不外推为普遍可靠。
## 6. 合并协议（生成器回传前预写，回传后按此执行并留痕）

1. 解析三路 staging 卡 → 统一卡结构（round/CANDIDATE-LEDGER.csv 字段）。
2. 轮内合并线索：merge_sim.py 两两 Dice>0.40 列出；相似度只作合并线索，是否同一(困难,原因,决策变化)由主控人工判定，禁止按相似度自动删除。
3. 与 16 张历史候选对账（9/3 冷启动 4 卡 + run-test-20260910 12 卡）：
   - (困难,原因,决策变化) 同一且无新实质证据 → 判"复现旧卡"，merged_into 指向旧卡 ID，不入推荐池；
   - 同困难不同机制/改动 → 保留为独立候选；
   - 携带新实质证据 → 按 pool 语义 reopened，必须写明 new_evidence。
4. 质量闸门（每卡过四问）：是否钉住具体决策时刻+信息条件；是否给出可观察现象；是否区分事实/推理/假设；是否连到到达率或时延的机制。不合格记录淘汰理由后归档。
5. 幸存集逐卡近邻核查：每卡指定"最可能已解决它的 1 篇/类工作"，用 Undermind/arXiv/本地全文定向核对（主控检索预算 ≤4 次 search_papers，免费档）。
6. 深化选择：只选有正面价值依据者（"未被反驳"不构成扶正理由），目标 2 个，允许 1-3 个；不设固定配额。
## 7. 最小闭环能力#1 收口（2026-09-10 晚）

- Undermind search_papers 端到端实测通过：workspace_id=eef99118-f623-4a47-a34a-05c6617b7ecb（"l's workspace"），样例查询返回 14+ 条高相关 LEO RL 路由文献（含 PDF 可得标记）。注：该工具必须显式传 workspace_id。
- 检索入口矩阵（当前可用）：Undermind（已验证）+ arXiv API（可达）+ 本地 SOURCES.csv 52 条 + Zotero"毕设"44 条 + 本地 PDF 15 篇（14 库内 + tao25）。S2 公共档 429 记录在案。
- 结论：能力#1（检索入口覆盖总目录而非仅笔记）通过；三路生成器均 running（list_agents 确认）。
## 8. 用户指令：冻结选题（2026-09-10 19:3x）

用户直接指令："搭好了也不要先开始选题，先跟我说，我看看架构行不行。"
处置：合并裁决/近邻核查/深化/审查/推荐全部冻结；三路已产出（A/B/C 各4卡）仅作架构试运行证据保留；
架构审查材料写入 ARCHITECTURE-REVIEW.md 并呈用户。恢复条件=用户裁决①架构可用性②入口污染处理③12卡去留。
## 9. 转审包落盘（2026-09-10）

REVIEW-REQUEST-FOR-CODEX.md 写入 worktree 根：自包含审查请求（背景/层图/试运行证据/六问题/三决策/文件索引/审阅边界/验收方式），供用户整段转发 Codex。
## 10. R2 架构返工（2026-09-10 晚，Codex+Luna 深审裁决后）

**裁决采纳**：保留骨架；修复影响判断可信度的关键问题；选题推荐与实验继续冻结。

### 10.1 复现（全部先复现后修，日志 round/logs/）
- 2A 检索失败→novel：确认（空近邻→novel；异常裸逃；测试 codify 空→novel）。
- 2B 标题相似→同一工作：判定级 same 确认（dice 0.8632≥0.85）；补充发现=多字段卡经展平稀释→不稳定；title-only 下聚合输出 collision 成立。
- 2C 检查器异常→正确否定：确认（异常与未知检查器在 expected=BLOCK 时计入正确）。
- 2D 占位文本假通过：4 例+补充 1 例全确认。
- 3A 台账 CLI：dataclass AttributeError 精确复现（Python 3.14.2；spec 加载未注册 sys.modules）；批内重复/重试幂等缺失自认成立。
- 指纹固定：research-ops 7 脚本+RESEARCH-ENTRIES+KNOWLEDGE-MAP+主库件全量 sha256 入 round/deps/DEPENDENCIES.md。

### 10.2 修复（全部落本线，未触碰 research-ops）
- round/tools/patched_checks.py（INPUT_INSUFFICIENT/NOT_APPLICABLE 语义+占位检测）
- round/tools/patched_audit.py（五类记账，all_ok 收紧）
- round/tools/patched_novelty.py（四态检索+断点+线索化判定+覆盖比对提示词+标题提取修稀释）
- round/tools/ledger.py（幂等/唯一当前版本/修订留痕/审查失效链/中断恢复/schema 校验）；ledger_add.py 废弃留档
- round/tools/{deps_check.py, gen_manifest.py, gen_neutral_view.py, merge_sim.py, test_rework_regressions.py}
- round/rules/EFFECTIVE-RULES-R2.md（唯一权威：取代 RESEARCH-ENTRIES 冲突条款；白名单 v2 用中性知识视图；取消 Elo/卡数/占比验收）
- round/knowledge/NEUTRAL-KNOWLEDGE-VIEW.md（程序化切片，节级行号溯源）
- round/dispatch/{DISPATCH-RECORD.md, D123-prompts.md}（会话补取，未取得字段如实标注）
- 三路产物横幅（试运行材料标签）；REVIEW-ROLE-PROMPTS v2（版本绑定/路径/互补声明）

### 10.3 验收
- 离线回归 10/10 PASS（round/tools/test_rework_regressions.py；期间发现并修复 status 子命令缺 --writer 的回归缺口，已纳入 T3）
- deps_check 20/20 一致（gen_manifest 流程化；视图时间戳变更→重指纹→复验，漂移检测本身被验证）
- governance/hygiene：worktree 内运行，除主库既有 2 项 STALE_CURRENT 外无新错误；DOCUMENT-STATUS.json 登记 7 条目（纯增 112 行，protected_sha256 继承污染已清理）
- 单卡小流程七步全实走：B3 卡入账→三角色前台审查（v1 指纹绑定，三份实算 sha256 一致）→主控整合 20 意见全采纳→v2 承重修订（6 字段）→R1-R3 自动 needs_review→v3 awaiting_evidence；OLD_TOPIC_MATCH 报告路径以合成同键旧卡演示（报告不淘汰）；语义同族跨 run 不键撞如实记录为主控职责

### 10.4 收口状态
- 备份：commit→push→Draft PR（本节完成于收口提交）；未合并，待 Codex 架构返工验收。
- 明确不做：embedding/S2 key/插件修复/检查器扩容/仪表盘/架构重设计。
## 11. R3 工作包（2026-09-10 深夜：历史索引+碰撞审查接入+四项修复+判别验收）

### 11.1 历史材料盘点与索引
- 全量盘点发现 4 条谱系 38 题：A=ONE-PAGE 开题一页纸线（1 题，冻结推荐后被删，38d0b5e，理由=锚定流程违规非证伪）；B=三透镜阶段线（14 候选→9 族→阶段2 演化淘汰族1/6/7+合并→3 族→2.5 压测→A5 四卡，分支 coldstart-clean/coldstart-deepdive 可 git show 检索）；C=冷启动备忘录 4 题（未裁决，自declared ANCHORED）；D=run-test 台账 12 卡（open）。
- 缺失如实登记：literature-index.csv（旧44条）、RECONCILED-LIBRARY.csv、archived-topic-stages-20260910、历史 run hypotheses/drafts、旧仓库路径（已不存在）。
- 产物：round/history/HISTORY-INDEX.md（指针式索引：每题五元组/处置/未通过原因+依据/原因货币性/重开条件；§5 货币性总表；§6 处置规则）。

### 11.2 历史碰撞审查接入
- 流水线位置写入 EFFECTIVE-RULES-R2 §8：独立生成→初筛→**历史碰撞审查**→近邻核查与深化→内容审查→推荐；五类输出；第四类主控核实后停止；第五类弃权不冒充否定；意见绑定版本；深化者只收有限反馈；下一批生成全新上下文。
- 子代理模板：round/tools/HISTORY-REVIEW-PROMPT.md。

### 11.3 四项修复（复现→修→验）
1. 审查失效判断：_norm_lb 原来剔除全部符号标点（τ<15s≡τ≤15s 不触发）→改为仅折叠空白；符号/小数点改变即触发。回归：T8 扩展（符号触发+纯空白不触发）PASS。
2. 身份与相似度分离：cand_id 原按合并键派生（同键不同内容被并成同题新版本）→改为首见内容派生+similar_to 线索字段+显式 merge 子命令（reason 留痕）；创建/显式修订/重试幂等分离。回归：T2 重写+merge 路径 PASS。
3. CSV 恢复保护：doctor 原按物理行截断（会毁多行字段合法记录）→停用破坏性修复；--backup 备份原件、--repair-out 产出重建候选文件（原件任何情况不动，采纳由人）。回归：T10 重写（多行字段+损坏尾：原件字节不变、重建件保留多行字段）PASS。
4. 解析失败误记成功无命中：safe_search 中 _normalize_paper 返回 None 未计入 skipped→全部解析失败输出 ok_empty；改为 None 也计数→全败=exec_error。回归：T12（monkeypatch 真路径）PASS。
- 全量：test_rework_regressions.py **11/11 PASS**；deps_check 21/21（gen_manifest 重指纹）。

### 11.4 判别验收与流程接力
- 判别样例 S1-S5（合成卡）：历史审查子代理（全新上下文）判 S1=④/S2=②/S3=③/S4=③(旧理由不适用+来源核验硬要求)/S5=⑤ —— 与设计预期 5/5 一致；模型正确性由主控逐项对照索引与原件核实（含亲证 taste-gate.md）。**如实登记**：样例文件含【预期】行、盲化不完美（审查者自查发现并声明，判定仅基于标题+五元组）。
- **审查者的独立发现**：索引 v1 与原件冲突——A5 四卡实有品味门裁决（taste-gate.md：F-I 收窄存活/F-II、F-III 死亡打捞/N1 通过附交割条件），v1 误记"未裁决"。主控亲证后修订索引至 v1.1（§2/§5，留痕）。
- 单卡流程接力（card-A1，path-A 卡A 切片）：初筛（主控卡片合同检查）→ 历史审查（后台子代理，全新上下文，唯一历史入口=索引，按需 git show 原件）→ 结论 ③（T-C1 最强匹配/D卡10/T-C3/F-I=②/缺失维度⑤）→ 主控处置（继续+四项前置义务，MASTER-DISPOSITION.md）→ 有限反馈 feedback-cardA1.md（仅卡相关 5 条）→ 深化者接力产出 card-A1-revised-draft.md（对账登记/基线升格 B0-B4/检索义务前置/竞争解释 6 项）。
- 隔离验证：深化者输入仅卡+有限反馈（无历史索引/台账）；其草案自证"历史前置名称唯一出处=反馈文件"并标未核实。台账：A1 入账 c30b20940a3 + R5-A1-history 意见登记绑定 content_hash。
- 未验证：S2 检索实际重跑（429 受限，义务已登记未执行——流程验证不含）；age-conditioned 先例是否存在（属下一步深化的检索义务）；台账 lexical 键不触发跨 run 匹配（语义匹配=历史审查者职责，已验证其工作）。
## 12. 正式选题循环 run1（2026-09-10 深夜→09-11）

按 EFFECTIVE-RULES-R2 §8 全流水线执行：三路生成（A/B/C 各 4 卡+4 诚实放弃线）→初筛入账 12 卡→历史碰撞审查两批（批1 家族合并裁决=A1/B1/C1/C4→F1 三机制层，T-C1 前身继承；批2 7×②+1×③*，B4 并入 L1、B2+C2 信用族）→深化（F1/B3 有限反馈接力，深化者隔离验证=其草案唯一出处=反馈文件）→三角色审查（builder 11 条/neighbor 发现 Wang24b 部分覆盖+TEG/GANNON 缺口/evidence 23 条含 M1 TAP-DAR 摘要级直接对手）→主控整合（全采纳，修订触发 R6-R13 失效链）→**推荐裁决：L1（cc72be0cbef v6）+B3（cc029fa6119 v3）推荐待审；F1（cc24a3f94e5 v3）条件保留（TAP-DAR/Wang24b 全文核读为第一淘汰条件）；A2/A3/A4/C3 backlog；信用族 awaiting_evidence（PRIMAL 0% 前提）**。
证据改变判断：M1（F1 降条件保留）、Wang24b、TEG+GANNON（L1 收窄）、IZHIKEVICH 反证方向。
交付物：ANALYSIS/TOPIC-LOOP-20260910/{PROPOSAL,AUDIT-SUMMARY,LITERATURE-GUIDE,PROCESS-APPENDIX}.md。本轮未启动训练/仿真；性能收益全部标为待验证假设。

## 13. run2 输入链修复与暴露声明（2026-09-10，Codex 内容审核驱动）

- **Codex 发现**：白名单 v2 声明 \`LITERATURE/notes/raw/*.md\` 为「已去倾向笔记」，但 raw 仍含 F0/F1、旧候选推荐及「我们的机会点」内容。实测：41 篇 raw 中 15 篇 30 处命中黑名单词（grep F0/F1/机会点/我们的/对账/信息阶梯）。发现属实。
- **run1 实际暴露（诚实声明）**：run1 三路生成器声明「浏览 14 篇全部经 notes/raw 笔记」，即生成阶段实际读入了含倾向句的 raw 笔记——v2 的「已去倾向」声明不成立，run1 卡的生成隔离存在缺陷。run1 推荐结论（L1/B3/F1）的证据链在 AUDIT-SUMMARY 中均已标注回原文核验状态，结论处置以 Codex 审核为准；run2 不继承 run1 卡作为生成输入。
- **修复**：\`round/tools/sanitize_notes.py\` 程序化剥离（块级删『与我们对账/连接：』+句级删黑名单句），产出 \`round/knowledge/notes-neutral/*.md\`（41/41 残留零容忍通过），manifest 含源 sha256 与删除统计；白名单升 v3，raw 移入黑名单、仅留给生成后历史审查。
- **run2 范围（用户锁定）**：低轨卫星网络中，负载变化下 RL 路由如何保持良好的到达率与端到端时延。旧 B3 的窄负载带/阈值失标定/课程学习恢复为待检查假设，不作生成前提；链路寿命方向退出主线。
## 14. run2 正式生成轮（2026-09-10）

**语料升级**：用户指正后接入 Zotero 111 篇（94 篇为旧题录遗漏），并新增 VM MinerU 全文转 MD 管线。
**生成**：三路独立生成器（A 强度 / B 热点OD / C 突发速度），路线 z-ai/glm-5.3-flash，白名单 v4（ZOTERO-INDEX + notes-neutral + 视图 + PDF）。
- 独立污染审计（audit_contamination4.py，只判路径参数位，剥离 content/code 正文）：A 14 调用 / B 13 / C 18，**真实违规 0**。
- 产出：9 张卡（各 3 张）→ 入账 `round/run2/cards.json`，cand_id：A1=c77e62eb00f、A2=c806e1db789、A3=c37b7753f31、B1=c9bbc1f6604、B2=cc0e429067b、B3=c3d376febf7、C1=cdc387b303e、C2=c24abb72218、C3=c6f6c2b12ad。
- **三路共同横向发现**：库内**无一篇** LEO 逐跳 RL 工作报告"训练强度/OD 分布/突发结构"三轴中任一轴的训练-评估分离实验——负载变化的三轴在文献里都是测量盲区（A: 训练负载合同普遍不披露；B: 空间非平稳从未互换；C: 同均值突发从未扫描）。
- 每条路径均含：八节卡 + 诚实放弃线（A 6 条 / B 5 条 / C 6 条）+ 防火墙声明 + 【原文事实/笔记/推演/待证】四档标注。
**下一步**：历史碰撞审查（独立子代理 0c226ffe）→ 深化（三问）→ 三角色审查 → G1–G5 闸门 → 推荐。
**VM 转换**：111 篇 MinerU（pipeline 后端，A100），修正输出路径探测后 v3 重启（已完成者跳过），监听作业 bash-3。

## 15. run3 续作收口（2026-09-11，新主控 session-100ff665）

- **交接**：旧主控冻结于 334fe9c（HANDOFF-FREEZE）；续作分支 agent/20260911-topic-loop-r2（PR #200，supersedes #199）；perm 主控切换完成（run topic-loop-r3-20260911）。
- **B3 补稿**：重派深化者 35 分钟产出 B3-v2.md（196 行）；HE/LIAQ/CMNCS52M 回 VM 逐字核验（新增 HE 训练=评估同 10,000 pps 第二实例）；纠正旧稿两处口径（-72.7% 改推演、WEIL 数字弃用）；miniflow-r3 A1 授权错位已披露，真 A1（c77e62eb00f）由主控回 path-A-intensity.md L68–101 核验，转引相符、回炉条件不触发。
- **A3 对抗检查**（ADVERSARIAL-A3）：四点补丁拆解——双通道记账够格、前兆信号半够格（挂提前量实测）、滞回/准入/地板降为实现细节；E4/E5 逐字核验通过。
- **C2 强化**：审计 14→19 篇（AUDIT-EXT-C2，TQF59BD7"有 ON-OFF 却聚焦 CBR"逐字）；Wan25f 摘要级划界（NEIGHBOR-WAN25F：不覆盖，状态件新颖性降为迁移）。
- **裁决**（VERDICT-3CARDS + gate_verdict 绑定）：**主线 C2**（recommended_pending_review v2）、**独立备选 A3**、**B3 退出**（awaiting_evidence v4，资产并入 C2 强度轴，T-C2 回写通道保留）。
- **交付五件套**：MAP-UPDATE / VERDICT-3CARDS / MAIN-RECOMMENDATION（含机制图与备选节）/ READING-GUIDE / 备选判定（A3），均在 round/run3/。
- 技术遗留：orchestrator.id 被误跟踪（deb5305）致 DIRTY，选择式暂存规避；根治（git rm --cached + gitignore）待用户批准。
