# 审核摘要（正式选题循环 run1 收口，2026-09-11）

> 状态：**待 Codex 内容审核**（框架 PR #199 已 READY+auto-merge 挂起；run1 全部产物在 agent/20260910-topic-loop 分支）。历史返工记录：round/ROUND-LOG.md、R3-DELIVERY.md。

## 1. 实际完成了什么 / 哪些能力真实验证

按 EFFECTIVE-RULES-R2 §8 流水线完整跑通一轮：**三路独立生成**（A 场景推演/B 文献行为/C 方法迁移，各 4 卡+4 条诚实放弃线）→ **主控初筛**（12 卡入账，12 个独立身份）→ **历史碰撞审查**（两批全新上下文审查者：批1 新鲜度四卡→家族合并裁决（三机制层不可互替）；批2 八卡→7×②+1×③*，B4 并入寿命卡、信用族合成）→ **深化**（F1/B3 有限反馈接力）→ **三角色内容审查**（builder 11 条+neighbor（发现 Wang24b 部分覆盖、TEG/GANNON 近邻缺口）+evidence 23 条（M1：TAP-DAR 真实直接对手坐实））→ **主控整合**（全部实质修订落账）→ **推荐裁决**。
真实验证的能力：五类历史判别（S1-S5 样例 5/5+R1 实跑）、家族合并键裁决、意见双哈希绑定（R6-R13 登记，修订自动失效链）、生成端隔离（深化者只收有限反馈）、证据链逐字核对（LOZANO/CHOU/LIAQ/WEIL/HE 原文+代码抽核）。

## 2. 推荐候选与三个核心问题直答

**L1 星历可预报的链路剩余寿命（cc72be0cbef v6，推荐）**：①ISL 计划内遥断+非计划失效的逐包路由层，观测向量无寿命字段（四篇已核）、可预报性只用于模型层继承（eq.13 限定）、"刚选完就断"的在途损失无人防；②针对"可预报性闲置在观测/动作层"，改观测（τ_ho 通道）+动作（T* 屏蔽进选择）+更新（target 同掩码同步）；③计划内分量被 TEG 规划部分覆盖、GSL 坑被 StarTCP/GANNON 夹击、固定死线解决计划内大半——生存域=分布式逐包+非计划失效的交集外。
**B3 队列感知价值的负载带塌陷窗（cc029fa6119 v3，推荐）**：①队列感知价值只在窄负载带成立（四锚互证：LOZANO 低载无差异/HE 工程化拥塞才有收益/LIAQ 自认 Dijkstra 理想最优且隔离排队/WEIL 无带宽限制≈SP），跨体制迁移的阈值行为从未被测量；②针对"训练合同单一化"，改训练合同（负载课程，profile 层零代码改动）+评估协议（阈值显式化+稳态/瞬态两腿）；③ELB/TLR 带内解决跨体制同坏、多负载混合可能拿走大半（自承最可能归宿）、负载数率入状态为生死对照——胜负条件均已写明。

## 3. 为什么值得开展（而非仅未被淘汰）

- L1：观测向量缺字段是四篇论文的**逐字级负证据**；"唯一用点=模型层"有 eq.(13) 原文锚；生存域是被两个部分覆盖域夹击后的明确交集外，验证第一步（现象占比统计）半天可判生死——负结果同样可发表（现象不存在=对"切换坑"直觉的澄清）。
- B3：四锚各自合同已回原文核对，其中 **LIAQ 自认构成可引用的自证锚**（卖 queue-aware 的论文自认 Dijkstra 理想时延最低且隔离排队）；测量对象（跨体制阈值行为）限定范围负断言成立且被 evidence 审查确认未越界。

## 4. 哪些证据改变了原判断

1. **TAP-DAR 真实存在且摘要级高度重叠**（evidence M1）——F1 从"空白家族"降为"条件保留"（原拟推荐）。
2. **Wang24b（GLOBECOM 自适应 LSU）**（neighbor 新发现）——F1 层①信令控制层[部分覆盖]，"年龄是隐式常量"表述须纳入反例。
3. **TEG 规划+GANNON**（neighbor C2）——L1 计划内分量[部分覆盖]，生存域收窄为 ISL 逐包+非计划失效。
4. **IZHIKEVICH"尖峰与切换无关"**（evidence L1-3）——L1 主机制假设的库内反证方向，已正面纳入竞争解释。

## 5. 最大未决项及其对推荐的影响

- **TAP-DAR/Wang24b 全文核读不可得**（arXiv 环境阻断、Undermind 仅摘要）——F1 不推荐（第一淘汰条件悬空）；L1 已对其开窗限定但不阻塞（其领地=lag 补偿，与 L1 的寿命屏蔽机制不同）。
- **现象存在性未测**（L1 占比、B3 窗宽）——两卡的验证第一步都是半天-两天级廉价核验，存在性证伪不影响本轮结论（已按"不承诺阴性结果必有论文价值"设计）。
- **Nie25/Hua25b 不在库**——F1 层③（塑形理论）维持挂起。

## 6. 本轮消耗与重要执行限制

- 模型：全部子代理走配置的默认非 Pro 路由；派发总计=生成×3+历史审查×2+深化×2+内容审查×3（前台/后台混合）；Undermind 每生成器 ≤3 次、每审查者 ≤2 次（限额遵守）；S2 公共档 429 全程受限（已切换 Undermind/arXiv 通道）。
- 限制：arXiv API 在部分子代理环境被 DNS 策略阻断（库外全文不可得，均如实标 INPUT_INSUFFICIENT）；LOZANO 开源模拟器无 LICENSE（仅内部复现义务已写入两卡）。
- 产物绝对路径：主文稿 /Users/lge/Desktop/leo-direct-sim/.worktrees/topic-loop-20260910/ANALYSIS/TOPIC-LOOP-20260910/PROPOSAL.md；证据 /Users/lge/Desktop/leo-direct-sim/.worktrees/topic-loop-20260910/round/run1/（staging/op-*/feedback/draft）；台账 /Users/lge/Desktop/leo-direct-sim/.worktrees/topic-loop-20260910/round/CANDIDATE-LEDGER.csv；审查登记 /Users/lge/Desktop/leo-direct-sim/.worktrees/topic-loop-20260910/round/reviews/reviews.csv；全程台账 /Users/lge/Desktop/leo-direct-sim/.worktrees/topic-loop-20260910/round/ROUND-LOG.md。

## 7. 交付物索引

PROPOSAL.md（方案正文+机制图）｜ LITERATURE-GUIDE.md（文献导读）｜ PROCESS-APPENDIX.md（过程附件）｜ README.md（入口）。
