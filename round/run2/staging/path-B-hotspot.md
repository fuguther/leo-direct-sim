# run2 路径B 选题卡（热点/OD分布变化）— staging

> 生成时间 2026-09-10；生成器：路径B探索子代理。
> 研究范围：低轨卫星网络负载变化下 RL 路由保持到达率与端到端时延。
> 入口：总流量相近但热点位置/源—目的分布变化。产出卡 3 张（0–4 允许，未凑数：第 4 个方向已并入卡3，见放弃线）。
> 证据分档：【原文事实】=zotero_fulltext 回全文核对（给篇名/itemKey+节/表/图号）；【笔记】=notes-neutral 线索未回原文；【推演】=本人推理链；【待证】=未检验假设。

---

## 1. 阅读与检索诊断

**浏览/精读清单**（zotero_fulltext 共 12 次调用、11 个不同 key；每次为关键词窗口提取，非逐行通读）：
| 篇名 | itemKey | 提取重点 | 截断情况 |
|---|---|---|---|
| Traffic-Aware MARL-Based Distributed Routing for LEO (Ferrer 2026, IEEE OJVT) | CMNCS52M | 队列分布三模型、训练协议、NMB/PDR 结果（2 次调用） | truncated=true（约 80k 字符，尾部泛化实验章节未逐行核验） |
| Traffic-Predictive Routing G-AODV (Liu 2024, Electronics 13(1):6) | UF8IQTA2 | 负载预测机制、实验场景（不同连接对） | 全文 78k，完整 |
| SaTE: Low-Latency TE for Satellite Networks (Wu, SIGCOMM'25) | JLF7IEBQ | 流量矩阵生成、地理稀疏剪枝、未见拓扑/流量评估 | truncated=true（尾部实验数字未核验） |
| Multi-Commodity Flow Routing via DRL (Tsai, WCNC 2022) | GPDPLJNG | MCF 形式化、请求注入方式 | 全文 32k，完整 |
| A DQN-Based Routing Algorithm for Load Balancing (Chen 2025, 书章) | XLRW7XXN | Poisson 初始负载、状态组成、离线+在线 | 全文完整 |
| On-Demand Routing with Dynamic Laser ISL (Bhattacharjee 2024) | DVS8C3CC | 需求驱动建链、ILP+启发式（非 RL） | truncated=true |
| High-Throughput Routing: Flow-Centric DRL (Liu 2024) | S85KQ4FC | 人口分布+泊松用户模型、推理时延瓶颈 Fig.2 | truncated=true（尾部实验合同未核验） |
| Queue-Aware and Resilient Routing MARL (2026 preprint) | 42E4NAQU | uniform vs population 双流量模式、集中训+在线学 | 全文 31k，完整 |
| Deciphering Region-Level Signatures (Shi 2026) | GJJQUMQ2 | 区域 RTT 签名、时间泛化下降 | 全文完整 |
| Small-scale LEO for Global-scale Demands / TinyLEO (Li, SIGCOMM'25) | MYBALQ2D | 真实需求不均衡+昼夜波动（Cloudflare 数据）、热点物理时间尺度 | truncated=true（§2.2-2.3 已核验） |
| Shaping Rewards, Shaping Routes: MADQN (Roth et al.) | L2VKYTAV | 热点=地理而非拓扑、动态链路负载实验 | 全文 19k，完整 |

**笔记线索（【笔记】档来源，均未因此直接下承重断言）**：CHEN-2025-TMIX、CHOU-2026-STL、LOZANO-2025-CONTINUAL、ZHOU-2026-DTAR、WANG-2021-GROUTING、ALMASAN-2022-DRLGNN（6 篇 notes-neutral）；round/knowledge/NEUTRAL-KNOWLEDGE-VIEW.md（Assumption Map 与 Claim Map）；round/zotero/ZOTERO-INDEX.md（111 篇总索引，近邻搜索覆盖 [新] 批次）；LITERATURE/SOURCES.csv（53 行，仅用于确认旧题录边界与 GraphPR 定位）。

**检索渠道与查询词**：
- Undermind search_papers：语义检索 2 次成功——Q1「traffic demand matrix change between training and deployment / hotspot moves / delivery ratio under unseen traffic matrices」；Q2「LEO hotspots move as satellites fly over densely populated regions / diurnal patterns across time zones / OD demand distribution changes」。另尝试 4 次均因参数校验失败（缺 workspace_id、search_type 误填 'global'、误传 sample_papers/max_results），未执行检索即返回，如实计入诊断。未用 launch_deep_search（禁用）、未用 read_pdfs（预算保留未耗）。
- 检索结论（仅标题/摘要级线索，未回原文，全部按【待证】对待）：LEO 侧近年有 PPO-SDR: Routing for Uneven Traffic Loads in LEO (Lai26)、STG-SR (Wei26)、RL robust routing against cascading failures (Zha26b)——均为负载不均/故障轴，未见「训练-测试 OD 分布互换」协议；地面网侧有 Spatial-Temporal RL for Network Routing with Non-Markovian Traffic (Wan25f)、ML for Network Optimization Across Diverse Traffic Scenarios (Nia26)、Exploring Limitations of GNNs for Network Modeling (Hap22)——是卡3的外部近邻。
- 失败渠道：无其他渠道失败；Undermind 首轮参数错误已定位为 API schema 变化（需 workspace_id + search_type='semantic'）。

**入口的总体证据判断（先说结论）**：
1. 文献把「负载变化」几乎全部实现为**强度变化或脚本化拥塞场**，没有一篇 LEO 逐跳 RL 工作在训练/测试间**互换 OD 分布或热点位置**【原文事实+检索，跨篇归纳】。CMNCS52M 的三种「流量模型」是三种**队列占用分布场**，各自单独训练（表2：输入维度/队列容量/速率逐模型不同）；SaTE 测「未见拓扑与未见流量流」但流量来自同一地理生成器【原文事实】；唯一显式测「不同通信连接对」的是非逐跳 RL 的 G-AODV【原文事实】。
2. 真实世界依据充分：Starlink 用户流量呈空间长尾+跨时区昼夜周期波动（TinyLEO 图3，Cloudflare 测量）【原文事实】；热点是「地理的而非拓扑的」（Roth §1.1）【原文事实】；卫星盖住热点约 3 分钟即离开【原文事实】。
3. 因此路径B的核心空白是真实存在的：**空间非平稳（热点迁移/OD漂移）下的逐跳 RL 表现，是文献的测量盲区**——不是「没做好」，而是「没测过」。所有卡按此定位写。

---

## 2. 候选卡

### 卡 B1：「热点可辨识性」——把可预测的拥塞场相位注入观测，检验时变空间负载下逐跳 RL 的大半差距是否为信息缺失

**1) 场景与可观察现象**
- 决策时刻：逐包/逐跳，每星仅凭本星与一跳邻居状态选下一跳。
- 信息条件：现有工作的状态=本星队列+邻居队列/链路时延+（部分工作）坐标与目的坐标【原文事实：CHOU-2026-STL 深读笔记 s_i(t)=[Q_i,{D_ij},x_i]；LOZANO-2025-CONTINUAL 深读笔记 28 字段一跳邻域编码；CMNCS52M §IV 表2 DQN-BL 22 个局部特征含邻居队列占用、残余传播时延、坐标、时间信息】。
- 负载变化形式：热点位置随卫星-地球相对运动迁移——卫星盖住热点约 3 分钟【原文事实：MYBALQ2D/TinyLEO §2.3】；人口场相位随地球自转以小时尺度扫过星座【原文事实：CMNCS52M §IV-B-2) population-based 模型 "the congestion level of a satellite depends not only on its position along the orbit but also on the time of day, as the Earth's rotation influence on the number of users served"】。
- 可观察/测量：相对最短路（全知）的归一化平均偏差 NMB、PDR、平均跳数。CMNCS52M 表3：静态 zone 模型下 RL NMB≈15%，而时变的 population/traffic 模型下 DQN-BL NMB 70%/55%、其最优改进版 40%/20%【原文事实：§IV-D/表3，p.1378】。GF/DRP 在 traffic 模型下 NMB 达 2.3/3.2。

**2) 困难与原因假设**
- 【原文事实】时变空间负载场景正是 RL 相对最优差距放大的场景：CMNCS52M 作者明言「the population and traffic-based models experience significant temporal variations due to Earth's rotation. Consequently, the RL agent must continuously adapt its routing policy to evolving congestion patterns」（§IV-D）。
- 【推演】机制假设一（部分可观测性）：地转+人口决定的拥塞场是 (星下点位置, UTC) 的近似确定函数。只看队列快照的策略看到的是同一观测对应不同最优动作（取决于此刻星座正对哪条人口密集经线）——MDP 性质被破坏，策略被迫做反应式追逐。该信息本身可预测、可免费获得（星历+时钟星上现成），属于**信息可辨识性缺口**而非能力缺口。
- 【推演】机制假设二（观测混淆）：「全局热点迁移」与「局部随机突发」在一跳队列快照上不可区分，但前者应提前绕行整片区域、后者就地一跳改道。快照无法支撑两种差异化策略。
- 【待证】CMNCS52M 虽已把时间特征放进状态（15/16 维区别），但没有报告切断时间特征的消融，也没有跨流量模型的训练-测试互换——「差距有多少来自相位信息缺失」未被分离过。

**3) 拟议改动**（辨因→选法：信息可辨识性，不动网络结构、不预设课程/门控）
- 状态增强：s_i(t) = [Q_i, {Q_j, D_ij}_j∈N(i), 目的方位, φ_orb(t), (λ_i, β_i), ΔQ_j(t;τ)]，其中 φ_orb=轨道相位角（或等效的「当前 UTC 下正对的人口权重经线」标量），(λ_i,β_i)=星下点经纬度，ΔQ_j=邻居队列 τ 窗斜率。DQN 结构、奖励、更新式全部不变，仅状态拼接扩维。
- 一次具体学习更新： TD 目标 y = r + γ max_a' Q(s'(t+1; 增广), a'; θ⁻) 不变；变化仅在 replay 里 (s,a,r,s') 以增广形式存取。预期作用：φ_orb 使「相同增广观测→相同最优动作」近似成立，恢复 Bellman 一致性；ΔQ_j 提供热点逼近的超前量（队列积分 ahead of 峰值）。机制上作用于第 2 节假设一与二：可预测分量从隐状态变为显式输入。
- 什么情况下不起作用：(a) 热点由与轨道相位无关的随机接入突发主导（如 SaTE 所述业务级波动）时 φ_orb 无信息量；(b) 队列反馈年龄大（邻居状态传播延迟达数跳时延）时 ΔQ_j 是噪声放大器；(c) 若训练-测试都在同一相位带内（如仿真只跑固定 UTC 段），增广无益且增方差。

**4) 初步近邻**（已查 Zotero 111 篇，含 [新]）
- CMNCS52M【原文事实】：时间特征已在状态中，但逐模型单独训练、无消融、无跨模型泛化测试——本卡差异=把「相位信息值多少」正面量化。
- ZHOU-2026-DTAR【笔记（深读）】：GAT 域特征显式含「surge 热点」指示，surge=5× 局部热点——已在用热点指示器，但 flow 级、3 流/步、域间链路远未饱和，无逐包排队语义。
- LOZANO-2025-CONTINUAL【笔记（深读）】：状态含坐标但无时间相位；其「模型预演+联邦聚合」是靠通信对齐模型，与本卡「靠信息对齐观测」是不同轴。
- DONG-2023-DQNLLRA【笔记（视图）】：邻居队列+链路特征逐跳 DQN，无地理/时间锚。
- 差异点总结：没有工作把「热点迁移的可预测性」当作信息设计问题检验；全部要么加结构（GAT/LSTM），要么扩训练分布。

**5) 简单替代猜想**
- 「训练覆盖」替代：直接在多个相位/多个热点位置混合训练（普通多场景训练，不增观测），可能吃掉本卡收益的 40–60%【待证】——因为混合训练本质是让策略内化相位→动作映射，但其参数容量与训练预算开销更大，且对未见相位带外推无保证。
- 「规则路由对齐」替代：把 CA-DRP/ELB 类邻居队列启发式的信息条件对齐（同样给它 φ_orb 加权），可能吃掉 30–50%【待证】。注意 CMNCS52M 表3 显示启发式在时变模型下掉队严重（CA-DRP NMB 1.2–1.4 vs RL 0.2–0.4）【原文事实】，说明启发式吃不完。
- 综合判断：若纯信息增强就能收回时变场景下 RL-最优差距（40%/20% vs 最优）的 60% 以上，则「泛化」叙事应改为「信息设计」叙事，这是本卡最大价值。

**6) 立即淘汰条件**
- 增广后 zone 静态模型出现同等幅度增益（说明只是扩维的普适效应，与热点相位无关）；
- population/traffic 模型下增益 <5% NMB 或不显著（同 seed 方差内）；
- 发现 CMNCS52M 类环境里队列场与轨道相位的相关性弱（地转假设不成立于所用数据）。

**7) 下一项廉价核验**（半天–1 天）
- 在复现的队列分布场环境（CMNCS52M 协议简化版：zone/population 两模型即可）中，同一 DQN 加/删 φ_orb 与 ΔQ_j 特征各跑 5 seed，比较 NMB 与 PDR；同时跑「多相位混合训练」对照。产出=机制归因小图。

**8) 来源指针**：CMNCS52M（itemKey CMNCS52M，§IV-B Queue-Distribution Model p.1372、§IV-D p.1377-1378 表3、图2/图3、§III-A）；MYBALQ2D（itemKey MYBALQ2D，§2.2-2.3、图3、图4）；CHOU-2026-STL/LOZANO-2025-CONTINUAL/ZHOU-2026-DTAR/DONG-2023-DQNLLRA 笔记（notes-neutral）；Undermind Q2 检索记录。

---

### 卡 B2：热点迁移下的「决策面拥塞」——逐包 RL 推理成本是到达率损失的一条未被计入的通道

**1) 场景与可观察现象**
- 决策时刻：每包到达每星触发一次（或多次）DNN 前向推理。
- 信息条件：状态观测+模型推理时间本身构成资源竞争；S85KQ4FC 用 M/D/C/N 排队模型为决策过程建模（包到达为 Poisson、每包决策时长恒定 D_m、C 个并发推理、N 缓存）【原文事实：S85KQ4FC §决策排队时延部分，M/D/C/N 定义】。
- 负载变化形式：热点扫过某星 → 该星到达率（接入+中转）陡增。
- 可观察/测量：S85KQ4FC 图2——到达率 13k→21k pps（~300 Mb/s @1500B）时，路由决策时延升至 17.5 ms、丢包率达 21%【原文事实：S85KQ4FC 图2 与其上下文】。即：到达率上升→决策队列溢出→直接吃掉投递率，与数据面链路拥塞无关。

**2) 困难与原因假设**
- 【原文事实】文献普遍默认「路由决策在包到达时立即完成」；S85KQ4FC 明确指出此前 LSBN DRL 研究忽略推理时延会使可行性结论失真（§引言/相关工作：given constrained energy and computation resources, it is impractical to entirely dismiss DNN inference time）。
- 【推演】机制假设：热点迁移使「推理负载的空间分布」与「数据负载的空间分布」同步高度不均。热点星的决策队列时延 D_q = Q·D_trans/(C_fwd−λ·D_trans) 型关系非线性发散；一旦决策缓存溢出，丢包计入 PDR——这条损失通道在均匀负载评估中被低估，在热点迁移评估中会被放大，且它对 RL 是**结构性税**（相对规则路由每包多一次前向）。
- 【待证】没有任何 LEO RL 路由工作报告过「热点区星上推理拥塞对 PDR 的贡献占比」；42E4NAQU、CMNCS52M 等的实验合同均未见推理时延项【原文事实：其表1/参数表无该项；42E4NAQU 表格仅 DRL 超参】。

**3) 拟议改动**（辨因→选法：决策结构，不改学习算法）
- 事件触发+流级动作复用：星上仅当 (a) 本星队列梯度 (Q_i(t)−Q_i(t−T))/T > θ，或 (b) 到达率 λ_i > λ_th，或 (c) 该流首包，才执行 NN 推理；否则复用该流上一包动作。目标函数与更新式不变；变化仅在执行层的「是否调用策略」。
- 一次具体决策更新：对包 p 属流 f，act(p) = π(s(t)) if trigger(t,f) else act(prev(f))；trigger(t,f) = 1[ΔQ>θ] ∨ 1[λ>λ_th] ∨ 1[f 未决]。
- 作用于第 2 节机制：把 M/D/C/N 的有效到达率 λ_dec 从「全部包」降为「触发包」，决策队列发散点右移，推理丢包通道关闭；同时保留热点星在需要时的高频决策能力。
- 什么情况下不起作用：(a) 拓扑时变快，缓存的下一跳在复用期内失效（链路切换/ISL 断），复用导致次优或环路；(b) 队列梯度本身是高噪声信号（突发到达），触发器误报率高反而增加推理负载；(c) 推理硬件足够快（决策时延 << 传播时延），通道本来就不存在。

**4) 初步近邻**
- S85KQ4FC【原文事实】：flow-centric 方案=在入口集中做流级决策以摊薄推理（需流表与入口控制），本卡差异=分布式逐跳场景的「退化复用+事件触发」，不需要流级入口控制权。
- L2VKYTAV (Roth MADQN)【原文事实】：动机段落明言 onboard processing typically limited（§1.1），但其评估未建决策时延模型。
- 42E4NAQU【原文事实】：队列感知+星上在线学习，未计推理成本【待证：其全文未见相关讨论】。
- DVS8C3CC【原文事实】：非 RL，需求驱动建链+ILP，代表「算力在地面控制器」的另一极，可作对照系。

**5) 简单替代猜想**
- 「均匀降频」启发式（每 N 包推理一次，无流/梯度感知）在到达率峰区可吃掉本卡收益的 50–70%【待证】；增量主要来自「按队列梯度触发」在突发初期就降载的部分，估 10–30%【待证】。
- 「规则路由兜底」替代：热点区直接切换到几何贪心/CA-DRP（零推理），RL 只在非热点区使用——可能吃掉更多（60–80%）【待证】，但牺牲热点区的拥塞规避质量，需实测权衡；这也构成对「RL 在热点区到底比规则好多少」的正面测量。

**6) 立即淘汰条件**
- 目标平台推理供给足够（21k pps 量级下决策时延可忽略）→ 机制不存在；
- 实测决策时延占总 E2E 时延 <5% 且推理丢包 <1% → 放弃；
- 触发器在合理 θ 下误报率 >30%，收益被抵消。

**7) 下一项廉价核验**（1–2 天）
- 在现有仿真（含排队）里把接入到达率拉到 13k–21k pps 量级，测逐包 DQN 的决策时延/PDR 曲线，叠加「每 N 包推理」「事件触发」两个变体；若推理时延通道贡献 <5% 即淘汰。

**8) 来源指针**：S85KQ4FC（itemKey S85KQ4FC，图2 与其上下文、M/D/C/N 决策排队模型节、§IV-B User Model）；L2VKYTAV（itemKey L2VKYTAV，§1.1、§2.2.2）；42E4NAQU（itemKey 42E4NAQU，§IV-A 流量模式、表1）；DVS8C3CC（itemKey DVS8C3CC，§II、§IV）。

---

### 卡 B3：「热点迁移评估协议」——建立守恒 OD 漂移算子，把「可辨识性缺口 / 策略记忆 / 数据面拥塞」三个失败原因正面分离

**1) 场景与可观察现象**
- 决策时刻与信息条件同卡 B1；本卡的对象是**评估合同本身**。
- 负载变化形式：总到达率守恒的 OD 漂移算子族——(a) 热点质心平移（人口场整体时移 Δt 对应的地转漂移）；(b) OD 对重采样（固定边缘总量、重连源-目的配对）；(c) 昼夜相位偏移（人口场固定、UTC 平移）；(d) 强度-only 对照（同一分布、总负载变化）。
- 可观察/测量：PDR 与 E2E 时延的退化曲线（漂移幅度×类型），叠加在线微调/信息增强/重训上界三层对照。

**2) 困难与原因假设**
- 【原文事实+检索】LEO 逐跳 RL 文献的泛化轴几乎全部开在**拓扑**上：Almasan 在未见拓扑评估（180 合成+232 Topology Zoo）【笔记（深读）】；SaTE 强调 unseen topologies and traffic flows【原文事实：JLF7IEBQ §1/§4，但其流量生成器同一】；CMNCS52M 的泛化=星座规模 3–12 面×4–16 星【原文事实：§III-A、摘要贡献3】。流量轴的「不同 traffic patterns」=三种队列分布模型各自单独训练【原文事实：表2 输入维度逐模型不同；图3 只展示 population 模型训练曲线】。
- 【笔记】中性视图 Assumption Map 第一条即「流量平稳或统计已知，突发性和多源目的业务被简化」。
- 【推演】因此「空间非平稳失败」的原因归属目前完全未测量，三种假说并存：(H1) 信息可辨识性缺口（卡 B1 的机制）；(H2) 策略记忆——策略记住了训练热点位置的绕行模式，本质是需要重训的分布偏移；(H3) 数据面拥塞——退化与策略无关，换任何路由都退化（总负载虽守恒，但局部链路/队列被重新压爆）。三者的修复手段完全不同（加观测 / 在线更新或覆盖训练 / 改容量或准入），不分离就无法选方法。
- 【待证】Roth MADQN 的动态链路负载实验（上 episode 使用的链路 +20% 负载）已观察到「rewards are lower and less stable… not able to robustly respond to the more varied state space」【原文事实：L2VKYTAV §2.2.2】——是文献中罕见的负载结构演化致不稳的直接记录，但那是路径依赖的负载演化，不是外生 OD 漂移；可视为 H2 的弱证据。

**3) 拟议改动**（方法论卡：协议+一个对照族，不预设赢的方法）
- 实现 OD 漂移算子（保持总到达率与业务构成守恒，只动空间结构），输出退化曲线族；
- 三层对照定位机制：L0 基线（不适应）；L1 信息增强（卡 B1 特征，探 H1）；L2 在线微调（几千步星上续训，探 H2；LOZANO 已证低探索续训可行【笔记（深读）】；42E4NAQU 有星上在线学习【原文事实】）；L3 重训上界。
- 判读规则：L1 收回大部分 → H1 主导（信息卡成立）；L2 收回大部分而 L1 无效 → H2 主导（学习更新卡成立）；L0-L3 全部同退化 → H3 主导（问题不属于策略，转为容量/准入问题，路线改写）。
- 什么情况下不成立：漂移幅度选太温和（<5% 退化，问题不存在）或太剧烈（>80%，落入强度变化而非结构变化），需先做幅度扫描定标。

**4) 初步近邻**
- G-AODV【原文事实：UF8IQTA2 摘要及实验节】：唯一显式测「不同通信连接对」场景的近邻，但非逐跳 RL（AODV+NN 预测+阈值控制），无守恒约束、无机制分离。
- Almasan【笔记（深读）】：拓扑泛化协议+「状态=容量+介数快照，信息过期代价未建模」——本卡把泛化轴平移到流量侧。
- Wan25f / Nia26（Undermind Q1 检索线索，未回原文）【待证】：地面网上 Non-Markovian traffic 与 diverse traffic scenarios 的经验分析——存在外部先行，LEO 逐跳语境是空白；若后续回原文发现协议重合，本卡降级为「LEO 化复现」。
- ZHOU-2026-DTAR【笔记（深读）】：其 surge/normal/fault 三场景是最接近的既有评估矩阵，但 flow 级、无守恒定义、图为主无精确数字。

**5) 简单替代猜想**
- 「合理在线微调」可能吃掉 50–80% 的漂移退化【待证】：理由是总负载守恒时只有空间重分配，邻居队列反馈时间尺度（秒-分钟）短于热点迁移时间尺度（分钟-小时），反应式适应理应有效；若实测确实如此，本卡价值转向「定位救不了的那 20–50%（快速迁移/突发重连）」。
- 「规则路由对齐」对照（CA-DRP/ELB 同协议跑漂移）可能显示启发式退化曲线与 RL 几乎平行【待证】——若成立，「RL 泛化失败」叙事整体降级为「所有分布式路由对空间结构变化都退化，RL 无特殊脆弱性」，这本身是可发表的诚实负结果。

**6) 立即淘汰条件**
- 守恒约束下漂移不产生 >5% 的 PDR/时延变化（问题不存在）；
- 退化被 H3 完全解释（所有方法同退化）且容量分析清晰归因于链路瓶颈 → 转 B2/容量方向，本卡放弃；
- 发现外部工作已发表等价协议（回原文核对后）。

**7) 下一项廉价核验**（1–2 天）
- 在任一已复现逐跳 DQN 环境（如 DONG-DQNLLRA/CHOU-STL 型）实现「热点质心平移」单一算子，跑 L0/L1/L2 三点，画出 5 seed 退化图；半天出幅度定标，1–2 天出三点判读。

**8) 来源指针**：JLF7IEBQ（itemKey JLF7IEBQ，§1、§2.2、§4）；CMNCS52M（§III-A、表2、图3）；UF8IQTA2（摘要、实验节）；L2VKYTAV（§2.2.2）；ALMASAN-2022-DRLGNN 与 LOZANO-2025-CONTINUAL 深读笔记；NEUTRAL-KNOWLEDGE-VIEW.md Assumption Map L43；Undermind Q1/Q2 检索记录（Lai26/Wan25f/Nia26/Wei26 仅线索）。

---

## 3. 诚实放弃线（考虑过但放弃）

1. **GNN 拓扑泛化机制移植到流量泛化**（SaTE 异构图/Almasan MPNN 思路直接搬）：回原文后确认其泛化声明全部落在拓扑轴，流量轴无证据；直接移植属于「以模块换说辞」，且 TE demand 级与逐跳逐包决策结构错位——放弃，其教训已并入卡 B3 的协议设计。
2. **预测式路由独立成卡**（G-AODV 式 NN 负载预测 + RL）：预测可预测分量（地转/昼夜）与卡 B1 的信息注入是同一因（把可预测信息交给预测器 vs 直接交给策略），单独成卡重复；且突发事件下预测误差不可控——放弃，作为卡 B1 的对照系保留。
3. **联邦聚合/模型预演扩展**（LOZANO 路线的通信对齐扩卡）：学习更新类大改动，通信与星上算力成本高，且其低拥塞收益作者自证微弱（追平最短路）【笔记（深读）】；性价比低——放弃，仅在卡 B3 的 L2 层作为在线微调实现选项。
4. **时空非平稳分离独立卡**（时间波动 vs 空间迁移谁主导退化）：已并入卡 B3 的算子族 (c)(d) 与判读规则，不再单独成卡。
5. **域划分/分层路由扩展**（DTAR 路线）：域级 flow 级动作与本研究逐包逐跳信息条件错位，对照不公平——放弃。

## 4. 防火墙声明

- **读取的白名单文件**：round/zotero/ZOTERO-INDEX.md（全 122 行）；round/knowledge/NEUTRAL-KNOWLEDGE-VIEW.md（全 131 行）；round/knowledge/notes-neutral/ 6 篇：CHEN-2025-TMIX.md、CHOU-2026-STL.md、LOZANO-2025-CONTINUAL.md、ZHOU-2026-DTAR.md、WANG-2021-GROUTING.md、ALMASAN-2022-DRLGNN.md；LITERATURE/SOURCES.csv（53 行）。目录列示仅限 round/zotero/、round/knowledge/notes-neutral/、round/run2/（均为白名单/产出目录）。
- **zotero_fulltext 调用**：12 次，11 个不同 itemKey（CMNCS52M×2、UF8IQTA2、JLF7IEBQ、GPDPLJNG、XLRW7XXN、DVS8C3CC、S85KQ4FC、42E4NAQU、GJJQUMQ2、MYBALQ2D、L2VKYTAV）；zotero_item 未调用；Undermind read_pdfs 未调用（预算 0/2）。
- **Undermind**：search_papers 成功 2 次（语义检索 Q1「流量分布漂移下的路由泛化」、Q2「LEO 热点昼夜 OD 路由」）；另有 4 次调用尝试因参数 schema 校验失败未执行（缺 workspace_id、search_type 取值错误、多余参数），未产生检索结果。未使用 launch_deep_search。
- **其他外部渠道**：未使用 arXiv API 与 web 搜索（库内语料+Undermind 已覆盖本入口需求）。
- **黑名单接触**：未接触。未读取、未列目录：LITERATURE/notes/raw/**、LITERATURE/KNOWLEDGE-MAP.md、ANALYSIS/**、NOTES.md、round/run1/**、round/CANDIDATE-LEDGER.csv、round/reviews/**、round/history/**、round/ROUND-LOG.md、round/knowledge/notes-neutral-manifest.json、round/knowledge/P0-SEMANTIC-SPOTCHECK.md、round/rules/QUALITY-GATE-R2.md 及任何旧候选台账/评审/其他 worktree。
