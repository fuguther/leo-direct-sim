# 旧课题联想剥离附录（2026-09-10 起）

> 规则：正文只留论文事实/作者解释/外部推断；旧课题联想逐字移入本附录保全，不删历史。
> 每条注明来源笔记、批次与提案文件。应用前经提案字面校验+主控逐段复核双关。

## SONG-2014-TLR（batch b1-3）
- 提案: out/research-ops/notes-cleanup/proposals/b1-3/SONG-2014-TLR.md.json
- 移出原文: 与我们:它正是我们 F0 层"局部队列信息"的经典极端版——我们的双 seed 事实是加局部队列改了约 1/3 ISL 路径但交付率零差异,而 TLR 恰恰押注这种信息有用,可直接作对照基线,验证信息阶梯的边界。

## SONG-2014-TLR（batch b1-3）
- 提案: out/research-ops/notes-cleanup/proposals/b1-3/SONG-2014-TLR.md.json
- 移出原文: ,与我们的零差异吻合。

## TALEB-2009-ELB（batch b1-3）
- 提案: out/research-ops/notes-cleanup/proposals/b1-3/TALEB-2009-ELB.md.json
- 移出原文: 对我们：是天然的第一对比基线。

## TALEB-2009-ELB（batch b1-3）
- 提案: out/research-ops/notes-cleanup/proposals/b1-3/TALEB-2009-ELB.md.json
- 移出原文: ——这恰好构成"路由状态信息年龄"的天然实验场，只是原文从未这样表述，也从没量化陈旧度代价。

## WIGMORE-2025-MAGNN（batch b1-3）
- 提案: out/research-ops/notes-cleanup/proposals/b1-3/WIGMORE-2025-MAGNN.md.json
- 移出原文: 对我们最对味的是控制粒度：路由系数级决策天然避免逐包动作维度爆炸，与"ISL 平均利用率 <3%、瓶颈在接入排队"的现实相互印证——也许我们真的不需要逐包的 ISL 智能。

## WIGMORE-2025-MAGNN（batch b1-3）
- 提案: out/research-ops/notes-cleanup/proposals/b1-3/WIGMORE-2025-MAGNN.md.json
- 移出原文: 多类别矩阵特征与我们的单级流量抽象错位。

## WIGMORE-2025-MAGNN（batch b1-3）
- 提案: out/research-ops/notes-cleanup/proposals/b1-3/WIGMORE-2025-MAGNN.md.json
- 移出原文: OA PDF 可下，值得作为"系数输出型路由"基线家族精读。

## ZHANG-2025-GRLR（batch b1-3）
- 提案: out/research-ops/notes-cleanup/proposals/b1-3/ZHANG-2025-GRLR.md.json
- 移出原文: ——我们 F0/F1 负结果（加队列+广告不改变聚合交付率）恰好给这类设计泼冷水。

## ALMASAN-2022-DRLGNN.md（batch b1-1）
- 提案: out/research-ops/notes-cleanup/proposals/b1-1/ALMASAN-2022-DRLGNN.json
- 移出原文: 不舒服处：需求级抽象意味着队列、丢包、时延动态基本缺席，网络性能只体现为"需求能否满足"，与我们逐包仿真中"瓶颈在接入排队"的结论天然不可比。

## ALMASAN-2022-DRLGNN.md（batch b1-1）
- 提案: out/research-ops/notes-cleanup/proposals/b1-1/ALMASAN-2022-DRLGNN.json
- 移出原文: 它重金投在"图表示"而非"信息新鲜度"，与 AoI-of-state 空白无关；但它是 GNN 路由泛化被引用最多的方法底座，edge-level 消息传递+动作条件化值得移植进我们的 GAT/MPNN 臂。

## ALMASAN-2022-DRLGNN.md（batch b1-1）
- 提案: out/research-ops/notes-cleanup/proposals/b1-1/ALMASAN-2022-DRLGNN.json
- 移出原文: 全文 arXiv 开放，值得精读核对架构与泛化协议。

## ALMASAN-2022-DRLGNN.md（batch b1-1）
- 提案: out/research-ops/notes-cleanup/proposals/b1-1/ALMASAN-2022-DRLGNN.json
- 移出原文: **与我们对账**：

## ALMASAN-2022-DRLGNN.md（batch b1-1）
- 提案: out/research-ops/notes-cleanup/proposals/b1-1/ALMASAN-2022-DRLGNN.json
- 移出原文: 1. **F0/F1 零差异的方法论对照**——他们全部指标都建立在"带宽分配量"（连续、每次 demand 都变化）上，根本没有逐包交付/丢包动态；我们的"信息阶梯改变路由但交付率零差异"在他们这种 demand 级抽象里**测量不可见**。这提示：交付率 0/1 饱和量对局部改道不敏感，改道影响应转向时延/路径熵等连续量测量。

## ALMASAN-2022-DRLGNN.md（batch b1-1）
- 提案: out/research-ops/notes-cleanup/proposals/b1-1/ALMASAN-2022-DRLGNN.json
- 移出原文: 2. **AoI 空白正面交锋**——状态含"链路可用容量+介数"快照，从未问这些特征的新鲜度/传播年龄；动作条件化使 Q(s,a) 只能表达"此刻已知的容量"，信息过期的代价从未建模。整个图表示投资在结构，不在时间戳——与我们的 AoI-of-state 空白同向。

## ALMASAN-2022-DRLGNN.md（batch b1-1）
- 提案: out/research-ops/notes-cleanup/proposals/b1-1/ALMASAN-2022-DRLGNN.json
- 移出原文: 3. **ISL 利用率无关但启发**——OTN 场景无 ISL 概念；但其"链路可用容量"若等价于我们 ISL 残留带宽，则其介数特征隐含"路径集中于少数关键链路"的图谱，可对照我们的 ISL<3% 瓶颈（他们没报任何利用率类指标，未核实）。

## ALMASAN-2022-DRLGNN.md（batch b1-1）
- 提案: out/research-ops/notes-cleanup/proposals/b1-1/ALMASAN-2022-DRLGNN.json
- 移出原文: 可复用——edge-level 消息传递 + 动作条件化（我们的 GAT/MPNN 臂可直接对照）、链路介数特征、k 路径动作离散化。

## ARXIV-2310.03969.md（batch b1-1）
- 提案: out/research-ops/notes-cleanup/proposals/b1-1/ARXIV-2310.03969.json
- 移出原文: **与我们对账**：

## ARXIV-2310.03969.md（batch b1-1）
- 提案: out/research-ops/notes-cleanup/proposals/b1-1/ARXIV-2310.03969.json
- 移出原文: 1. 他们测的正是"access 缺口"的年龄代价——AoI 由覆盖 on-off（等卫星进穹顶）主导，与我们的 holding/access 瓶颈同构：接入缺口是年龄时钟真正走动的地方；我们的 ISL 利用率<3% 说明星间网内侧排队几乎不贡献年龄，本模型的 on-off 服务结构就是接入瓶颈的理论化，可当我们的解析锚；

## ARXIV-2310.03969.md（batch b1-1）
- 提案: out/research-ops/notes-cleanup/proposals/b1-1/ARXIV-2310.03969.json
- 移出原文: 2. 覆盖/服务主导时，网内路径选择与队列信息与 AoI 几乎无关（等价于我们 F0/F1 信息阶梯改路由而交付零差异的机理：瓶颈不在被选路径上）；新鲜度杠杆是更新率 μ 与星座密度 λ，不是路由；

## ARXIV-2310.03969.md（batch b1-1）
- 提案: out/research-ops/notes-cleanup/proposals/b1-1/ARXIV-2310.03969.json
- 移出原文: 3. AoI 对象仍是"载荷更新包"，无人把路由状态年龄当状态/分析对象——AoI-of-state 空白继续成立（三重核实未动摇）。

## ARXIV-2310.03969.md（batch b1-1）
- 提案: out/research-ops/notes-cleanup/proposals/b1-1/ARXIV-2310.03969.json
- 移出原文: on-off 服务过程的 AoI 闭式可直接套到我们的 holding/access 级联建模；穹顶面积/密度换算公式可复核我们 280×14 Walker 对地覆盖假设。

## BHAVANASI-2023-GNNMADRL.md（batch b1-1）
- 提案: out/research-ops/notes-cleanup/proposals/b1-1/BHAVANASI-2023-GNNMADRL.json
- 移出原文: 舒服处：它把"变化"本身当问题，训练时扰动、评估时未见拓扑的协议与星座旋转带来的拓扑变化同构，韧性评估模板可直接借给我们 GNN 臂。

## BHAVANASI-2023-GNNMADRL.md（batch b1-1）
- 提案: out/research-ops/notes-cleanup/proposals/b1-1/BHAVANASI-2023-GNNMADRL.json
- 移出原文: 不舒服处：它依赖完整且即时的链路/队列观测，对"观测本身会陈旧"毫无意识；"流集碰撞"目标与逐包公平性/拥塞语义绑定较深，搬到 LEO 需重想。

## BHAVANASI-2023-GNNMADRL.md（batch b1-1）
- 提案: out/research-ops/notes-cleanup/proposals/b1-1/BHAVANASI-2023-GNNMADRL.json
- 移出原文: 它不做状态年龄，但它的扰动-评估协议正好是我们量化"陈旧度代价"时的对照组设计参考。

## CHU-2023-RRSDRL.md（batch b1-1）
- 提案: out/research-ops/notes-cleanup/proposals/b1-1/CHU-2023-RRSDRL.json
- 移出原文: 连接：AoI 入奖励罕见先例，精读价值在于看其 AoI 定义如何避免循环依赖（AoI 依赖转发路径、路径由策略决定）；175 星 vs 我们 3920 星，量级差一截，结论外推要打折。

## GAO-2026-RAOI.md（batch b1-1）
- 提案: out/research-ops/notes-cleanup/proposals/b1-1/GAO-2026-RAOI.json
- 移出原文: 不舒服：RAoI 度量被转发数据的年龄，不是路由决策信息的年龄——它是我们已知空白的镜像而非答案；RAoI 自身的计时/携带开销摘要没说。

## GAO-2026-RAOI.md（batch b1-1）
- 提案: out/research-ops/notes-cleanup/proposals/b1-1/GAO-2026-RAOI.json
- 移出原文: 连接：与 CHU 的 RRS-DRL 构成"数据 AoI 入奖励"小谱系；同一机制把对象换成"路由状态"就是我们想做的实验【我的推测：把奖励从数据 AoI 换成状态 AoI 的工程改动不大，但问题语义与实验设计完全不同】。

## HAN-2024-DMR.md（batch b1-2）
- 提案: out/research-ops/notes-cleanup/proposals/b1-2/HAN-2024-DMR.json
- 移出原文: MHMRD 按最小跳发现路径，对时变链路速率不敏感——与我们 MCS 动态链路速率设定直接相关。

## HAN-2024-DMR.md（batch b1-2）
- 提案: out/research-ops/notes-cleanup/proposals/b1-2/HAN-2024-DMR.json
- 移出原文: 与课题：ISL 状态进 GNN 的输入时刻正是状态年龄问题的切片；无公开代码，作多径方法论参照，不作基线。

## HAN-2024-DMR.md（batch b1-2）
- 提案: out/research-ops/notes-cleanup/proposals/b1-2/HAN-2024-DMR.json
- 移出原文: ——AoI-of-state 空白未被触碰

## HAN-2024-DMR.md（batch b1-2）
- 提案: out/research-ops/notes-cleanup/proposals/b1-2/HAN-2024-DMR.json
- 移出原文: ，与 F0/F1 零差异形成直接张力：关键差异在**场景**——他们 ISL 受限、无接入瓶颈，我们压力在 holding/access，info 价值取决于瓶颈位置，这正支持瓶颈感知方向

## HAN-2024-DMR.md（batch b1-2）
- 提案: out/research-ops/notes-cleanup/proposals/b1-2/HAN-2024-DMR.json
- 移出原文: 可复用：MHMRD 的 Walker 闭式跳数公式（eq.11-21）可作我们 280×14 的解析路径枚举/校验基准；PPO+优先回放训练协议；「5 快照平均」协议（警示：样本太少）。

## IZHIKEVICH-2024.md（batch b1-2）
- 提案: out/research-ops/notes-cleanup/proposals/b1-2/IZHIKEVICH-2024.json
- 移出原文: 对我们:最大价值是警示——把 GSL/ISL 简化成"可用/不可用"会丢掉真实行为;我们仿真要引入链路/时延复杂性时,它提供现实锚点(时延分布、路径多样性),也再次提醒:测量有多少,结论才能走多远。

## IZHIKEVICH-2024.md（batch b1-2）
- 提案: out/research-ops/notes-cleanup/proposals/b1-2/IZHIKEVICH-2024.json
- 移出原文: 实测直接支持我们 ISL 利用率<3% 与 holding/access 瓶颈

## IZHIKEVICH-2024.md（batch b1-2）
- 提案: out/research-ops/notes-cleanup/proposals/b1-2/IZHIKEVICH-2024.json
- 移出原文: ，与 F0/F1「路径改道不带来聚合收益」（这里重路由甚至有害）同构

## IZHIKEVICH-2024.md（batch b1-2）
- 提案: out/research-ops/notes-cleanup/proposals/b1-2/IZHIKEVICH-2024.json
- 移出原文: ，但其重路由 15s 粒度与尖峰统计可作为我们状态陈旧度实验的现实锚点

## IZHIKEVICH-2024.md（batch b1-2）
- 提案: out/research-ops/notes-cleanup/proposals/b1-2/IZHIKEVICH-2024.json
- 移出原文: 可复用：开源测量管线+数据集（仿真时延分布/重路由模型校准素材）；TTL-ping 差分法；15s 平滑窗=星切换时间粒度实测参考。

## LIAQ-2026-QARR.md（batch b1-2）
- 提案: out/research-ops/notes-cleanup/proposals/b1-2/LIAQ-2026-QARR.json
- 移出原文: "queue-aware"我们在 F0 已做过且是负结果——队列感知本身卷不出差异，缺的正是一个信息价值/陈旧度维度。

## LIAQ-2026-QARR.md（batch b1-2）
- 提案: out/research-ops/notes-cleanup/proposals/b1-2/LIAQ-2026-QARR.json
- 移出原文: 连接：可作弱基线；它的盲区恰是我们的机会点。

## LIAQ-2026-QARR.md（batch b1-2）
- 提案: out/research-ops/notes-cleanup/proposals/b1-2/LIAQ-2026-QARR.json
- 移出原文: ，与我们 F0/F1 零差异互为印证

## LIAQ-2026-QARR.md（batch b1-2）
- 提案: out/research-ops/notes-cleanup/proposals/b1-2/LIAQ-2026-QARR.json
- 移出原文: ，反衬 ISL 利用率<3%/holding-access 瓶颈判断

## LIAQ-2026-QARR.md（batch b1-2）
- 提案: out/research-ops/notes-cleanup/proposals/b1-2/LIAQ-2026-QARR.json
- 移出原文: ③ AoI-of-state 空白：状态全部取瞬时值，无信息年龄维度；

## LIAQ-2026-QARR.md（batch b1-2）
- 提案: out/research-ops/notes-cleanup/proposals/b1-2/LIAQ-2026-QARR.json
- 移出原文: ——我们的 AoI-of-state 恰是该梯度中间带

## LIAQ-2026-QARR.md（batch b1-2）
- 提案: out/research-ops/notes-cleanup/proposals/b1-2/LIAQ-2026-QARR.json
- 移出原文: **可复用**：集中训-分散部署+星上在线学习流程；韧性分公式可直接进我们奖励；均匀/人口双流量合同。

## MA-2022.md（batch b1-2）
- 提案: out/research-ops/notes-cleanup/proposals/b1-2/MA-2022.json
- 移出原文: 我们一直盯交付率,"时延中断"作为次级指标是不是更贴近用户体验?

## MA-2022.md（batch b1-2）
- 提案: out/research-ops/notes-cleanup/proposals/b1-2/MA-2022.json
- 移出原文: 对我们:MCS 动态链路速率正是这种时变距离/信道的显式后果,其 FSMC 做法可作"距离→速率"映射的参考模型,也提醒我们把该映射做成可复现组件。

## RAN-2025-GRAPHPR.md（batch b1-2）
- 提案: out/research-ops/notes-cleanup/proposals/b1-2/RAN-2025-GRAPHPR.json
- 移出原文: 连接：设定与我们的 POMDP+局部队列+全分布式最接近，但通篇没有"信息有多旧/值多少钱"的位置——正是我们 F0/F1 信息阶梯想问的。

## ARXIV-2007.05449.md（batch b2-1）
- 提案: out/research-ops/notes-cleanup/proposals/b2-1/ARXIV-2007.05449.json
- 移出原文:   1. AoI 对负载呈 U 型（Fig.7，低负载时 AoI 由源生成间隔主导）——我们 ISL 利用率<3% 正落在 U 型左支：队列状态几乎无信息量，这就是 F0/F1 信息阶梯改了 1/3 路由却交付零差异的机理侧证据（信息不稀缺时路由决策不敏感）；

## ARXIV-2007.05449.md（batch b2-1）
- 提案: out/research-ops/notes-cleanup/proposals/b2-1/ARXIV-2007.05449.json
- 移出原文:   2. 他们结论反指"年龄瓶颈节点"（加强关键链路速率/可靠性比改路由更影响 AoI，Abstract/VI）——与我们的 holding/access 瓶颈判定同构：瓶颈不在被选路径上的 ISL（<3%），而在接入/持有环节；

## ARXIV-2007.05449.md（batch b2-1）
- 提案: out/research-ops/notes-cleanup/proposals/b2-1/ARXIV-2007.05449.json
- 移出原文:   3. OPF/HAF 证明不改路径、只改排队纪律即可换 AoI/公平（Sec II,V）——支持把年龄感知下沉到 holding/队列管理而非多径重路由；

## ARXIV-2007.05449.md（batch b2-1）
- 提案: out/research-ops/notes-cleanup/proposals/b2-1/ARXIV-2007.05449.json
- 移出原文:   4. 本文 AoI 对象是"网络内传输的更新包"，无人把路由状态信息年龄当状态/分析对象——我们的 AoI-of-state 空白依旧成立。

## ARXIV-2007.05449.md（batch b2-1）
- 提案: out/research-ops/notes-cleanup/proposals/b2-1/ARXIV-2007.05449.json
- 移出原文: 串联队列 AoI 界与 U 型/最优负载区公式可直接做我们 holding 瓶颈的理论对照；OPF/HAF 可搬进 holding/access 调度器做年龄感知基准实验；PAoI 尾界可作最坏情形指标。

## ARXIV-2512.00985.md（batch b2-1）
- 提案: out/research-ops/notes-cleanup/proposals/b2-1/ARXIV-2512.00985.json
- 移出原文: ① 我们最刺痛的点（信息阶梯改道~1/3 但交付率零差异）此文恰好反向佐证：路由选择的价值只在 AoI 惩罚度量、且惩罚陡峭时显现——α=1 时最优比最佳单路由惩罚低 ~60%（VII-D1 行~1340），时延/交付率度量下改道无收益 → 度量-决策解耦是共性现象，不是我们仿真独有的；

## ARXIV-2512.00985.md（batch b2-1）
- 提案: out/research-ops/notes-cleanup/proposals/b2-1/ARXIV-2512.00985.json
- 移出原文: ② 路由可用性 p_k（II-A 行~289）即我们 holding/access 瓶颈的显式随机化：p 小时 MAD-Zero Wait 反劣于简单策略、与最优差距收窄（VII-D3 行~1358）→ 支持把接入可用性作为状态分量而非仅链路几何；

## ARXIV-2512.00985.md（batch b2-1）
- 提案: out/research-ops/notes-cleanup/proposals/b2-1/ARXIV-2512.00985.json
- 移出原文: ③ AoI 仍是"数据更新年龄"（对端收到的最新样本年龄），与"路由决策状态年龄"无关 → AoI-of-state 空白依旧成立。

## ARXIV-2512.00985.md（batch b2-1）
- 提案: out/research-ops/notes-cleanup/proposals/b2-1/ARXIV-2512.00985.json
- 移出原文: p_k 可用性 on/off 建模、能量约束 Lagrange 处理、阈值策略作 RL 行为先验。

## CHEN-2025-TMIX.md（batch b2-1）
- 提案: out/research-ops/notes-cleanup/proposals/b2-1/CHEN-2025-TMIX.json
- 移出原文: 关键假设「局部观测足以支撑全局负载均衡」正是我最想拆的点：他们没度量局部状态里有多少过期信息，与「路由状态年龄」空白无涉。

## CHEN-2025-TMIX.md（batch b2-1）
- 提案: out/research-ops/notes-cleanup/proposals/b2-1/CHEN-2025-TMIX.json
- 移出原文: 与课题：观测粒度与我们的 F0 信息阶梯同族，可直接对照；但 18% 失效场景远超我们 <3% ISL 利用率压力合同，【我的推测】-13.6% 大概率是失效/拥塞场景红利，稳态未必有。

## CHEN-2025-TMIX.md（batch b2-1）
- 提案: out/research-ops/notes-cleanup/proposals/b2-1/CHEN-2025-TMIX.json
- 移出原文: 作 CTDE-MIX 结构参考，不作基线。

## DONG-2023-DQNLLRA.md（batch b2-1）
- 提案: out/research-ops/notes-cleanup/proposals/b2-1/DONG-2023-DQNLLRA.json
- 移出原文: 与课题：其 state 设计正是我们 F0 阶梯后几档的同类内容——把这套状态喂给逐跳学习器，即可复测「信息增加是否带来聚合收益」。逐跳 DQN 粒度与我们一致，最容易自实现为对照基线（无代码）。

## DONG-2023-DQNLLRA.md（batch b2-1）
- 提案: out/research-ops/notes-cleanup/proposals/b2-1/DONG-2023-DQNLLRA.json
- 移出原文: ——直接支持我们「路径改道≠聚合交付收益」的 F0/F1 警示（他们连交付都不测）

## DONG-2023-DQNLLRA.md（batch b2-1）
- 提案: out/research-ops/notes-cleanup/proposals/b2-1/DONG-2023-DQNLLRA.json
- 移出原文: ——AoI-of-state 空白未被触碰

## DONG-2023-DQNLLRA.md（batch b2-1）
- 提案: out/research-ops/notes-cleanup/proposals/b2-1/DONG-2023-DQNLLRA.json
- 移出原文: 可复用：逐跳 DQN 的 state/action/reward 模板（最易复现为 T1 对照组）；Ci−Cj 防环梯度；动态 ε 策略；反面教材：「决策节点降带宽」式公平性 hack。

## GILBERT-ELLIOTT.md（batch b2-1）
- 提案: out/research-ops/notes-cleanup/proposals/b2-1/GILBERT-ELLIOTT.json
- 移出原文: 凭什么信:数学简洁、半个多世纪被当作工程标准件;不舒服:两态把链路降级的连续谱压成二元开关,参数必须靠实测数据标定,直接搬进我们仿真会引入未标定参数。

## GILBERT-ELLIOTT.md（batch b2-1）
- 提案: out/research-ops/notes-cleanup/proposals/b2-1/GILBERT-ELLIOTT.json
- 移出原文: 对我们:与 GUVEN-2023 的 Markov 多态同源,是给 ISL/GSL 加突发中断的最省事抽象;而它和"MCS 连续速率"之间哪个态粒度更贴近真实链路,值得做成消融。

## HE-2025-PRIMAL.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/HE-2025-PRIMAL.json
- 移出原文: 不舒服：异步事件驱动天然产生陈旧信息，它容忍陈旧而不度量陈旧的价值——绕开了我们最关心的问题；异步本身的训练稳定性也存疑。连接：与我们极端拥塞压力合同最接近之一，CVaR 尾部约束可移植；异步=信息陈旧的自然来源，属机制近邻而非设定继承。

## HE-2025-PRIMAL.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/HE-2025-PRIMAL.json
- 移出原文: **与我们对账**：

## HE-2025-PRIMAL.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/HE-2025-PRIMAL.json
- 移出原文: 1. **F0/F1 零差异的镜像证据**：所有学习算法丢包率都 ≈0.00%（表 I）——路由决策在变（MADQN 73.4ms→PRIMAL-CVaR 61.5ms、排队时延 17.6→4.8ms，-72.7%），但**交付(丢包)零差异**，收益只落在时延/排队指标。

## HE-2025-PRIMAL.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/HE-2025-PRIMAL.json
- 移出原文: 直接反哺我们："信息阶梯零交付差异"或需在时延/队列指标下复查，或我们的网络比其 50Mbps-ISL+10k包/s 更不拥塞。

## HE-2025-PRIMAL.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/HE-2025-PRIMAL.json
- 移出原文: 2. **ISL 利用率<3% 的工程注脚**：其拥塞是**刻意工程化**的（ISL 仅 50Mbps 远低于真实 Starlink ~10Gbps），SPF 丢包 84.8% 说明环境重度拥塞才有 RL 增益；我们的 M-Lab 分散流量+动态 MCS 天然不拥塞——呼应"ISL<3% 时信息增益=0"。

## HE-2025-PRIMAL.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/HE-2025-PRIMAL.json
- 移出原文: 3. **holding/access 瓶颈反向**：其 GSL(1000Mbps)比 ISL(50Mbps)快 20 倍，瓶颈在星间链路而非我们实测的 holding/access；其卫星仅 FIFO+丢包，无 holding 概念。

## HE-2025-PRIMAL.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/HE-2025-PRIMAL.json
- 移出原文: 4. **AoI-of-state 空白确认**：异步事件驱动天然容忍陈旧，观测"本地邻居统计"无时间戳/年龄字段，全文不量化陈旧损伤——仍是空白。

## HE-2025-PRIMAL.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/HE-2025-PRIMAL.json
- 移出原文: **可复用部件**：IQN 分布批判器 + CVaR 约束（可移植到我们 DDQN/GAT 的队列代价）；包级 episode+事件驱动（与 SimPy 事件驱动同构）；3 城市 Poisson 10k 包/s 作工程拥塞压力测试；primal-dual 约束 RL 写法。

## LI-2023-LUR.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/LI-2023-LUR.json
- 移出原文: 舒服的地方：它把"年龄"当目标函数而非事后指标，时变图建模 ISL 中断的数学工具对我们有复用价值。

## LI-2023-LUR.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/LI-2023-LUR.json
- 移出原文: 不舒服处在于对象错位：LUR 度量的是被转发数据到达接收端的陈旧度，而我们要的是"路由决策所依据的状态信息"的年龄——两者不是同一个量；它隐式假设全局路由信息总是即时的，恰好是我们想攻的假设。可作为 AoI 数学工具的参考实现，但不能当作与我们空白重叠的竞争者。

## LI-2023-LUR.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/LI-2023-LUR.json
- 移出原文: **评级**：B

## LOZANO-2025-CONTINUAL.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/LOZANO-2025-CONTINUAL.json
- 移出原文: 连接：平台谱系前身（提示称）；它显式处理"策略随轨道移动而过时"，与我们的"观测状态陈旧度"是邻近但不同的两个问题，精读时值得鉴别。

## LOZANO-2025-CONTINUAL.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/LOZANO-2025-CONTINUAL.json
- 移出原文: **与我们对账**：

## LOZANO-2025-CONTINUAL.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/LOZANO-2025-CONTINUAL.json
- 移出原文: 1. **F0/F1 零差异的正面裁判**——他们证明：仅加一跳邻居拥塞信息（16 值）即足以在ℓ=1 重载下绕开拥塞链路、追平全知最短路，且把"邻居拥塞信息"作为状态核心（III 节 1785-1861 行）；

## LOZANO-2025-CONTINUAL.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/LOZANO-2025-CONTINUAL.json
- 移出原文: 我们的 F0/F1 信息阶梯加了局部队列/物理信息只改道不改交付率——对照可见差异在主链路(ISL)本就空闲时无从体现，改道增益只发生在拥塞场景，而我们的实验负载可能从未把 ISL 推到利用瓶颈。

## LOZANO-2025-CONTINUAL.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/LOZANO-2025-CONTINUAL.json
- 移出原文: 2. **ISL 利用率<3% 与 holding/access 瓶颈**——他们报时延不报 ISL 利用率，但热力图(Fig.7)显示最短路把流量集中在少数链路边、MA-DRL 随负载升高才扩散到备选路径——若 ISL 利用率低，MA-DRL 与最短路几乎等价(50th 差 1.7ms)正是他们"低拥塞追平"的机理，与我们"ISL<3% 时改道无收益"定量吻合；

## LOZANO-2025-CONTINUAL.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/LOZANO-2025-CONTINUAL.json
- 移出原文: 他们暴露的瓶颈是队列时延(拥塞时)而非 holding/access，未测量接入/保持瓶颈，未核实与我们同测度可比。

## LOZANO-2025-CONTINUAL.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/LOZANO-2025-CONTINUAL.json
- 移出原文: 3. **AoI-of-state 空白**——状态里邻居拥塞 C_j,k 假设每步即时可得，Q 函数从未建模该信息的传播年龄/反馈延迟；"最短路径需实时全网信息故 genie 化、我们只要一跳信息"正是对信息新鲜度价值的显式承认但未量化——AoI-of-state 仍是空白，且本篇是"信息获取成本 vs 新鲜度"最接近的邻居文献。

## LOZANO-2025-CONTINUAL.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/LOZANO-2025-CONTINUAL.json
- 移出原文: **可复用部件 + 危险信号**：可复用——log 压缩拥塞编码 C_j,k、相对坐标粒度化(σ=20)消 180° 边界、CKA 模型发散度度量、模型预演+分层 FL 双尺度对齐、greedy matching 建 ISL。危险——

## MANFREDI-2021-RELATIONAL.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/MANFREDI-2021-RELATIONAL.json
- 移出原文: 这一手和我们实测的"瓶颈在对接入排队"直接呼应——十篇里极少有把排队等待时长当决策一等公民的。舒服处：它承认"等待时长本身是高信息量状态"，与我们把 holding/access 排队识别为瓶颈互为印证；跨拥塞泛化与我们压力合同实验同构。

## MANFREDI-2021-RELATIONAL.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/MANFREDI-2021-RELATIONAL.json
- 移出原文: 可作为"排队等待作为信息"的对照参考，提示我们在 AoI 实验里把"预计等待"也写成显式状态分量。全文公开可作基线移植候选。

## MANFREDI-2021-RELATIONAL.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/MANFREDI-2021-RELATIONAL.json
- 移出原文: **评级**：B

## RAO-2025-DGAT.md（batch b2-2）
- 提案: out/research-ops/notes-cleanup/proposals/b2-2/RAO-2025-DGAT.json
- 移出原文: 与课题：图注意力感知资源状态与我们的 GAT 臂同源，仍未涉状态年龄；【我的推测】其「增量」是给确定性拓扑变化预分配演化方向，属结构红利。

## SORET-2024-QLEARN.md（batch b2-3）
- 提案: out/research-ops/notes-cleanup/proposals/b2-3/SORET-2024-QLEARN.json
- 移出原文: 证据：仿真，genie 上界设计值得抄。

## SORET-2024-QLEARN.md（batch b2-3）
- 提案: out/research-ops/notes-cleanup/proposals/b2-3/SORET-2024-QLEARN.json
- 移出原文: 舒服处：把时延拆成传播+排队两段，与我们的瓶颈分析同语言；同组 MA-DRL 模拟器公开（SatCom-TELMA/MA-DRL_Routing_Simulator，已核存在），大概率为实验底座。

## SORET-2024-QLEARN.md（batch b2-3）
- 提案: out/research-ops/notes-cleanup/proposals/b2-3/SORET-2024-QLEARN.json
- 移出原文: 不舒服处：表格 Q 状态空间极小，「邻居信息」的时间维度装不进去——Q 值在陈旧观测下如何衰减正是可补的空。

## SORET-2024-QLEARN.md（batch b2-3）
- 提案: out/research-ops/notes-cleanup/proposals/b2-3/SORET-2024-QLEARN.json
- 移出原文: 与课题：收益来自排队避免而非路径最短化，与我们「路径改变但交付率不变」同构；【我的推测】他们没测尾部分布。

## WANG-2021-GROUTING.md（batch b2-3）
- 提案: out/research-ops/notes-cleanup/proposals/b2-3/WANG-2021-GROUTING.json
- 移出原文: 谱系价值大于方法价值：二作 Yongyi Ran 即 GraphPR（TVT 2025，我们最近邻基线）核心作者，这是那条进化线的起点。

## WANG-2021-GROUTING.md（batch b2-3）
- 提案: out/research-ops/notes-cleanup/proposals/b2-3/WANG-2021-GROUTING.json
- 移出原文: 与课题：line-graph 把链路特征织进表示，与我们 F1「第一跳物理链路显式加入」角度互补——他们隐式带，我们显式加，正好对照。

## XIANG-2025-MATGCIR.md（batch b2-3）
- 提案: out/research-ops/notes-cleanup/proposals/b2-3/XIANG-2025-MATGCIR.json
- 移出原文: 不舒服处：模仿 SPF 预训练是双刃剑——策略被锁进最短路径吸引域后，「绕行/负载均衡」只是微扰；恰是我们 F0/F1 想测的（路径改了、聚合收益为零）。

## XIANG-2025-MATGCIR.md（batch b2-3）
- 提案: out/research-ops/notes-cleanup/proposals/b2-3/XIANG-2025-MATGCIR.json
- 移出原文: 与课题：时序图卷积把拓扑历史揉进表示，与「路由状态年龄」相邻——时间窗等权聚合 vs 按年龄加权，是可做的实验变体。

## ZHOU-2026-DTAR.md（batch b2-3）
- 提案: out/research-ops/notes-cleanup/proposals/b2-3/ZHOU-2026-DTAR.json
- 移出原文: 最关键的不适感：域级抽象把决策粒度抬到"域"而非"星间逐跳"，与我们 280×14 逐包逐跳的仿真直接错位。

## ZHOU-2026-DTAR.md（batch b2-3）
- 提案: out/research-ops/notes-cleanup/proposals/b2-3/ZHOU-2026-DTAR.json
- 移出原文: 它对"信息年龄"仍无意识，但"把链路负载/故障状态动态编码进 GNN"其实就是我们要量化的"路由信息新鲜度"的粗糙版。

## ZHOU-2026-DTAR.md（batch b2-3）
- 提案: out/research-ops/notes-cleanup/proposals/b2-3/ZHOU-2026-DTAR.json
- 移出原文: 可作参照系，也提示：就算状态又全又新，域级粒度也撑不起对拥塞的响应——和我们 ISL 利用率 <3% 的发现同构。

## ZHOU-2026-DTAR.md（batch b2-3）
- 提案: out/research-ops/notes-cleanup/proposals/b2-3/ZHOU-2026-DTAR.json
- 移出原文: **评级**：A

## ZHOU-2026-DTAR.md（batch b2-3）
- 提案: out/research-ops/notes-cleanup/proposals/b2-3/ZHOU-2026-DTAR.json
- 移出原文: **与我们对账**：① F0/F1——他们把"实时链路负载/故障"编进 GNN 状态（≈我们的 F1 物理信息阶梯），但 normal/surge 场景只报 CV/延迟改善、**无交付率量化提升**，fault 场景才有 pp 级收益；与 VM 实测"信息多了路径变了、交付率零差异"结构同构：低负载下拥塞感知无从发力。

## ZHOU-2026-DTAR.md（batch b2-3）
- 提案: out/research-ops/notes-cleanup/proposals/b2-3/ZHOU-2026-DTAR.json
- 移出原文: ② ISL 利用率<3%——flow 级 3 流/步 + 18 域，域间链路远未饱和，CV 优化就是低利用率下的摆布，同构。

## ZHOU-2026-DTAR.md（batch b2-3）
- 提案: out/research-ops/notes-cleanup/proposals/b2-3/ZHOU-2026-DTAR.json
- 移出原文: **可复用**：action masking（连通性+跳预算）可直接移植我们 DDQN/GAT 臂；GAT 节点/边特征模板与 δ 方向塑形奖励；离线划分+在线路由两时间尺度解耦；开源 https://github.com/ChenZ-code/DTAR_Routing。

