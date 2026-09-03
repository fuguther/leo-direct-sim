# 查新轮 1 判读报告：N1 实测动态盲的 RL 路由评估

- 判读代理：fresh-context（查新判读）
- 输入：cards/card-04-n1.md + novelty/_raw-r1.json 之 "card-04-n1" 键（已亲验存在：6 组 queries + 5 条 anchors，anchors[0]=ARXIV:2310.09242 n=20）
- 日期：2026-09-03
- 判读口径：【直接答复】= 同现象（RL 路由结论的实测动态重评估）+ 同机制核心（把实测队列/重配置/PoP 动态注入 RL 路由训练或评测环境）；【相邻】= 触及一方（实测标定卫星仿真、RL 卫星路由、评估方法论）但未见"重评估"闭环；原始数据仅含 id+标题（无摘要字段），凡标题不足以判定者标【存疑-需摘要】。

## 1. 逐查询组判读（6 组）

### Q1 "reinforcement learning evaluation measurement-driven network"（24 条）
【无关为主】。结果以 RL 通用理论/综述（Robbins-Siegmund 形式化、Meta-RL 教程、DRL 综述）、机器人平台（The Open Ant）、医学影像、分子设计、结构健康监测为主，与 LEO 卫星 RL 路由评估无现象重叠。可疑者：
- 10.2139/ssrn.5798349 / 10.2139/ssrn.5274748（重复收录）"Expert-driven Jumpstart RL for Managing Network Congestion Control"【相邻-存疑-需摘要】：网络拥塞控制 + RL，若其用实测痕迹评测则触及"实测驱动 RL 网络评测"，但拥塞控制非路由、SSRN 预印本无摘要不可判。
- 10.59628/jast.v4i8.3250（UAV 网络切片 DRL）【无关】：无线资源管理，非卫星路由重评估。

### Q2 "reinforcement learning routing real-world trace evaluation"（24 条）
【无关为主】。多为机器人真实环境 RL、车辆路径问题（Learning to Route Electric Trucks——"routing"为车辆径路非网络路由）、RL 通识综述。可疑者：
- 10.1109/tvt.2018.2887282 "Hierarchical Routing for VANETs via RL"【无关】：VANET RL 路由，非实测动态重评估。
- 10.48550/arxiv.2004.07219 "D4RL"【相邻（远）】：数据驱动 RL 评测基准的方法论先例，非网络路由域——可引用非竞争。

### Q3 "simulation-to-real gap reinforcement learning network routing"（22 条）
【无关为主，1 条存疑】。
- 10.1016/j.eswa.2024.124310 "Bridging the simulation-to-real gap of depth images for deep RL"【无关】：sim2real 概念同源但域为视觉深度图。
- 10.61951/sciencepaperonline.202401.0007 "Traffic Engineering in Segment Routing Network Based on DRL"【相邻-存疑-需摘要】：地面 SR 网 DRL 流量工程，若评测用真实拓扑/痕迹则与本卡"评估环境保真度"议题相接，标题不足以下判定。
- 10.2139/ssrn.4414648 "MARL for Network Routing in IAB Networks"【无关】：接入回传网，非卫星、无测量标定迹象。
- 其余（NoC 路由 DRL、Onion 路由检测、EEERP-RL 评审记录）【无关】。

### Q4 "benchmark RL routing satellite realistic environment"（24 条）——本卡最敏感组
【相邻多条】。
- arXiv 2009.08155 / 10.1109/netsoft70012.2026.11603525 "Hybrid Table-Assisted and RL-Based Dynamic Routing for NGSO Satellite Networks"【相邻-存疑-需摘要】：NGSO 卫星 RL 路由，域完全重叠（且与池内 2509.14909 方法族"表驱动+RL"同类）。关键问题恰是其评测环境是否含实测队列/重配置动态——标题无法判定；若其已做实测标定评测则直接威胁 N1 现象段，**轮 2 必须取摘要/全文复核**。
- 10.1109/icmlcn59089.2024.10624807 "Q-learning for distributed routing in LEO satellite constellations"【相邻-存疑-需摘要】：LEO 分布式 Q-learning 路由，域重叠；评测保真度标题不可判。
- 10.3390/su16219239 "GNN for Routing Optimization: Challenges and Opportunities"【相邻（远）】：GNN 路由综述，可能综述评估环境缺陷，非重评估工作。
- 2608.20575 "URB — Urban Routing Benchmark for RL-equipped Connected Autonomous Vehicles"【相邻】：**跨域同范式平行工作**——为 RL 路由构建真实感基准并评测，但域为车联网非卫星。它证明"真实感基准重审 RL 路由"范式已存在于别的域，压缩 N1 的"首个"声明范围（须限定为"LEO 卫星域首个"），但不构成同域直接答复。
- 2002.03071（暗夜保护）、2412.08244、2505.17734、SVRPBench/VRP 基线族【无关】。

### Q5 "measurement-informed emulation satellite network RL"（24 条）
【相邻 3 条】——测量/仿真社区一侧密集命中，说明 trace 驱动卫星仿真已是活跃线，但均未见 RL 路由重评估闭环：
- 2304.00708 "Trace-driven Path Emulation of Satellite Networks using Hypatia"【相邻】：真实痕迹驱动卫星路径仿真——与 N1"实测标定环境"同侧，产出是仿真设施而非对 RL 方法的裁决。
- 2507.03248 "An eBPF-Based Trace-Driven Emulation Method for Satellite Networks"【相邻】：同上，trace 驱动仿真设施。
- 2011.05202 "OpenSN: An Open Source Library for Emulating LEO Satellite Networks"【相邻】：LEO 仿真开源库，评估基础设施。
- 2603.01172（波长路由链路分配）【无关】：光学卫星网链路分配，非 RL、非实测动态。
- 其余（天气雷达仿真评审、NetPolicy-RL 药物优先级、6G 数字孪生综述等）【无关】。

### Q6 "ecological validity reinforcement learning evaluation networking"（24 条）
【无关为主】。
- 10.1201/9781498710411-41 与 10.4135/9781506326139.n219（Ecological Validity 两条款）【相邻（远）】：生态效度方法论源头（社科/人因），可作 N1 论证引用，非竞争工作。
- 10.2139/ssrn.7145518 "FVF: Evaluating MDP Formulations for Healthcare RL"【相邻（远）】：医疗域 RL 评测效度框架——方法论平行，非网络域。
- 其余（生态景观评价 DRL、生态物种扩散 MADRL 等为 "ecological" 误命中）【无关】。

## 2. 逐锚点前向引用判读（5 条）

| 锚点 | n | 判读 |
|---|---|---|
| ARXIV:2310.09242（15s 重配置） | 20 | 【相邻 1 + 无关 19】。"A Cross-US View of Starlink's PoP and Satellite Assignment Strategy to Mobile Users"【相邻-存疑-需摘要】：PoP 分配策略实测，供给侧参数更新，未见 RL 评测；"The More We Measure, The Less We See"（移动测量可复现性）、HERMES（speedtest 监测）、Planet-Scale IoT via LEO、AI Infrastructure in Space 等均为测量/基础设施向。**20 条中无一为"把 15s 重配置注入 RL 评测"**——正面证据。 |
| ARXIV:2605.27717（drop-front 队列） | 1 | 唯一命中为其自身（"Dissecting the StarLink: Characterizing Queuing..."）。**无前向吸收者**——发表即无 RL 路由工作跟进，直接支持 Puzzle 段"两社区脱节"。 |
| DOI:10.1109/iwqos65803.2025.11143359（PoP 切换） | 3 | 【相邻 + 无关】。"Inferring Starlink Latency Structure from Public RIPE Atlas Measurements"【相邻】：同社区测量延续，供参数更新而非 RL 评测；"Characterizing the Configuration of Starlink Queuing"疑为 2605.27717 同族/自引；"Edge-Side Fingerprints of Service Tiering..."【无关】（限速指纹）。无 RL 评测吸收者。 |
| ARXIV:2601.13662（residual RL 回传路由） | 1 | "Toward Scalable SDN for LEO Mega-Constellations: A Graph Learning Approach"【相邻-存疑-需摘要】：LEO 学习类路由（GNN/SDN），域重叠；其评测环境保真度标题不可判——若其引入实测队列/重配置则威胁 N1。注意其方向是做新方法而非重评估旧方法，初步判【相邻】。 |
| ARXIV:2604.12382（DTAR，开源） | 0 | **零前向引用**。开源 RL 代表尚无任何后续（含重评估）——支持"空白"，但该文献过新、覆盖窗口有限（n=0 可能是时间窗效应）。 |

## 3. 【查新结论】

- **直接答复数：0**。6 组查询 + 5 条锚点前向链中，未发现任何"把实测卫星动态（队列语义/重配置节律/PoP 切换）注入 RL 路由训练或评测环境并重测既有方法结论"的工作。锚点侧尤其干净：2605.27717 零吸收、2604.12382 零前向、2310.09242 的 20 条前向无一触及 RL 评测。
- **相邻清单**（按威胁度降序）：
  1. 2608.20575 URB——跨域（车联网）同范式"真实感基准重审 RL 路由"，压缩"首个"声明，须限定卫星域；
  2. 2009.08155 / NetSoft'26 NGSO 混合表+RL 路由【存疑-需摘要】；
  3. 10.1109/icmlcn59089.2024.10624807 LEO 分布式 Q-learning【存疑-需摘要】；
  4. 2601.13662 前向：Toward Scalable SDN for LEO（GNN）【存疑-需摘要】；
  5. 2304.00708 Hypatia trace-driven 仿真、2507.03248 eBPF trace-driven 仿真、2011.05202 OpenSN——测量/仿真设施侧同侧相邻，供给"环境已开源"叙事、暂无重评估闭环；
  6. 10.61951/sciencepaperonline.202401.0007 SR 段 DRL 流量工程【存疑-需摘要】；
  7. 10.2139/ssrn.5798349 拥塞控制 jumpstart RL【存疑-需摘要】；
  8. 2310.09242 前向：Cross-US PoP 分配策略【存疑-需摘要】；
  9. 方法论远邻（可引用非竞争）：D4RL、FVF（医疗 MDP 效度）、生态效度两条款。
- **存疑数：6**（SSRN 拥塞控制、SR 流量工程、NGSO 混合、LEO Q-learning、LEO SDN GNN、Cross-US PoP——均因原始数据仅含标题无摘要而挂起；轮 2 应定向取前 4 条摘要/全文）。
- **证据等级**：标题/元数据级（raw 数据无摘要字段），对"无直接答复"的判定为中等强度——未发现反例是正面证据，但覆盖空洞在案：①池内 tail-* 5 篇仅摘要级未入本次检索；②2604.12382 过新（n=0 或为时间窗效应）；③6 组查询为英文关键词检索，未覆盖 IEEE/ACM 全库与中文文献；④结果含明显关键词误命中（"The Open Ant"反复出现、"ecological"误命中），召回偏松、精度偏低——但松召回正符合"漏报比杀死更糟"纪律。综合：**N1 现象段在轮 1 检索下未被证伪**，可进入轮 2 定向复核（优先 4 条同域存疑项取摘要）。
