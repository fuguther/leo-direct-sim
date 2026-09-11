# 读卡批次 R7

> 读法：逐字通读 VM MinerU 导出 MD 全文（从第 1 行到最后一行），行号对应 VM MD。禁止用 grep 替代阅读。
> 批次：L63JISQN LBMABZJ7 LJG6ZW7B LNA28YZY LRSXMWX9 LZKNZA8B MXQVNU3P MYBALQ2D NPF75WS5 P6XJZNQK PIXWFHAC

## L63JISQN — Making Sense of Constellations: Methodologies for Understanding Starlink's Scheduling Algorithms

**1. 一句话**
用 4 个真实 Starlink 终端的毫秒级测量，加上从 gRPC 遮挡图反推"当前服务卫星"的新方法，实证 Starlink 存在层级式流量工程：一个每 15 秒重分配一次的**全局卫星分配器** + 一个星上 MAC 调度器；再用随机森林给全局分配器做一个离线近似。全篇不是 RL，是测量+逆向工程。

**2. 问题设定**
Starlink 是目前最大的 LEO WAN，但其调度算法不透明，研究者因此无法提出也无法验证性能改进方法（L19）。具体的麻烦落在两类人身上：想优化 Starlink 性能的研究者，和想建 Starlink 仿真的研究者。L41 逐字："Internals of the algorithm that maps user terminals to satellites are currently known only to the operators of the Starlink network."

**3. 方法骨架**
非 RL。三块拼起来：

- **高频测量（第 3 节，L49）**：4 个终端（西欧 / 美东北 / 美中 / 美西北），Starlink 路由器桥接模式 + 专用树莓派；目的服务器与终端所在 PoP 同址，以剔除地面网络干扰；iRTT 以 1 包/20 ms 发包、iPerf3 用 50% 上行带宽；NTP 同步时钟。选这个频率/带宽是因为更高频更高带宽时丢包与时延"highly variable"。
- **卫星识别（第 4 节，L63–L89）**：不用 app（app 已不再显示服务卫星），改用遮挡图。gRPC 遮挡图是 123×123 二维图，作者标定出它是极坐标图：中心 62×62、极坐标半径 = 仰角（25–90）、θ = 方位角（θ=0 为北）、极坐标图半径 45 像素（L69）。对相邻两个 15 秒槽的图做 XOR 抹掉共同轨迹，隔离出槽 x 的那颗星（L71）；每 10 分钟重置终端防止轨迹重叠。候选星位置来自 CelesTrak TLE + SGP4 传播（L67）。最后把候选星的仰角/方位角轨迹转笛卡尔，用 DTW 距离匹配（L89）；作者用 500 组人工目视比对验证，DTW 与人工重合 >99%。
- **全局分配器建模（第 6 节，L130–L134）**：把可用星按 (θ, φ, 年龄 a, 光照 ε) 的 **z-score 四元组**聚类（即"离组均值几个标准差"），特征是"本地时间 + 起始于最近 15 秒区间各簇的可用卫星数"；用随机森林（作者选它是因为抗过拟合 + 可解释），网格搜索 + 5 折交叉验证。

**4. 它声称的效果**
- 时延特征每 15 秒突变，发生在每分钟第 12/27/42/57 秒，四个站点、所有时段都能观察到；相邻 15 秒窗口的时延特征经 Mann-Whitney U 检验显著不同（p<.05）（L57）。
- 仰角：被选中星的中位仰角比"可用但未选中"的星高 22.9°；45°–90° 区间只占可用星的 30%，却贡献了被选中星的 80%（L97）。
- 方向：被选星方位角偏北（Ithaca 站例外，因西北被树遮挡，该站只从该区域拿 9.7%，其他站平均 55.4%）；其他站点平均 58% 可用星在北侧，但被选中 82% 来自北侧（L99）。
- 发射批次：被选概率随发射月份单调上升（L111）。
- 光照：同时有受照星与暗星时，72.3% 选受照星；只有当暗星占可用星 ≥35% 时才选暗星，且此时选中的暗星仰角比对应的受照星高 25°（L122）。
- 模型：top-5 准确率 **65%**，基线 22%（L134）。基线 = 直接返回"可用星最多的 top-k 簇"。

**5. 实验条件**
真实网络，无仿真。4 个 Starlink 终端（美/欧），目的地在对应 PoP；为标定极坐标边界让终端连续在线 2 天；每 10 分钟重置终端。视野内任一 15 秒槽平均有 **35–44 颗**星（L93）。模型评估用 80% 数据做 5 折 CV，另 20% 作 holdout 验证抗过拟合（L132）。**没有做负载扫描**——测量是在终端"well under capacity"状态下做的。

**6. 它自己承认的局限**
L136 逐字："Our model is constructed using only publicly measurable data related to Starlink's satellites. However, based on disclosures in SpaceX's FCC filings, we expect that other publicly-unavailable features such as terminal density in a region and satellite load characteristics will also impact the global scheduler. Therefore, the performance of our model is constrained by the unavailability of data."
另有 L59 对星上调度器自述："Further investigation is required to exactly identify the characteristics of this controller."

**7. 它没做但看起来能做的地方**
1. **卫星负载与终端密度**是作者自认缺失的两个特征（L136），而这两个恰恰是负载变化场景的核心；作者没试过用可观测量（如 15 秒窗口内的时延带结构）去代理它们。
2. **星上 MAC 调度器只被观察到"几条相差几毫秒的平行带"，推测是 round-robin**（L59），明确说需要进一步研究——这是全篇留下的最大口子。
3. 模型只预测"卫星属于哪个特征簇"，**不预测具体卫星 ID**，因此无法直接用于路由仿真。
4. 没有把该模型接回仿真器，验证它对路由/时延的影响（L141 只说模型会在录用后公开）。
5. 测量条件全是低负载，未做负载-时延的联合扫描。

**8. 和同批其他篇的关系**
与同批 LBMABZJ7（DisCoRoute）同属 Starlink 实体研究但角度正交：LBMABZJ7 做纯几何的最少跳路由，假设拓扑理想、无拥塞；本篇提供"卫星分配每 15 秒变一次、且与负载无关地抖动"这一实测约束，正好是几何路由忽略掉的那一层。方法上与 LZKNZA8B 完全不像（测量 vs 学习）。未见引用同批其他篇。

**9. 对"负载变化下到达率/时延"的贡献**
**基本没有直接贡献，但提供了一条关键的负事实。** 逐字 L57："these effects were noticed even when our terminals were running well under capacity" —— 即 15 秒周期性的时延台阶**不是负载驱动的**，终端远低于容量时依然存在。这反过来说明：在 LEO 场景下观察到的短周期时延抖动，可能主要来自调度周期而非排队，做"负载→时延"建模时必须把这两个来源分开。另一方面，负载确实进入分配决策（L43 引 FCC 专利：星上 MAC 调度器考虑 user priority、current load、per-terminal flow characteristics），但本篇**完全没有量化**负载的影响，也没做负载扫描。所以对到达率/时延的直接事实贡献≈0。

**10. 一句话评价**
测量与逆向工程类工作，把 Starlink 调度器从黑盒压成"可预测的特征簇代理"，并给出了一条被后续建模者必须处理的实测约束（15 秒全局重分配）；不涉及 RL，是 LEO 路由/调度仿真研究的外部对照物与约束来源。

## LZKNZA8B — Spatial-Temporal Learning-Based Distributed Routing for Dynamic LEO Satellite Networks

**1. 一句话**
把 GAT（空间特征）+ LSTM（时间依赖）+ DQN（决策）拼成一个"每颗星自己当 agent"的分布式路由框架，问题建成 POMDP，主打"主动拥塞避免"，最后用一张碳排放表把它包装成 Green AI。

**2. 问题设定**
LEO 拓扑高速变化、ISL 时变，最短路/静态路由失效，导致时延、拥塞、丢包上升；集中式路由信令开销过大、大规模星座不可扩展（L21）。作者指出的三个具体缺口（L29）：(a) 既有方法把空间拓扑与时间动态**分开**处理；(b) 全连接网络不适合图结构；(c) 集中/半集中框架开销大。进一步的批评针对 [14]：它把"时空流量预测"与"路由决策"**解耦**，突变时预测与实时状态失配会造成次优路由与更差时延（L27）。

**3. 方法骨架**
POMDP (S, A, P, R)：
- **状态**（式 3, L91）：$s_i(t)=[Q_i(t), \{D_{ij}(t)\}_{j\in\mathcal N_i(t)}, x_i(t)]$，即本星队列 + 到各邻居的时延 + 拓扑相关特征（相对位置/连通指示）。
- **动作**（L96）：在邻居集 $\mathcal N_i(t)$ 中选下一跳。
- **奖励**（式 4, L103）：$r_i(t)=-(\alpha D_{i,a_i(t)}(t)+\beta Q_i(t))$，**刻意取 β>α**，让 agent 愿意放弃更短的路径去走不拥塞的路，作者称这是"anticipate future congestion"（L108）。
- **更新**（式 9/10）：DQN，$a=\arg\max Q_\theta(h_i^{(t)},a)$，目标 $y=r+\gamma\max_{a'}Q_{\theta^-}$，目标网 θ⁻ 每 C=200 步同步（算法 1）。
- **GAT**（式 6/7, L135–143）：注意力系数 α_ij 由 $\sigma(w^T[x_i\|x_j])$ 经 softmax 得到，聚合 $z_i=\sum_j \alpha_{ij}x_j$。
- **LSTM**（式 8, L155）：$h_i^{(t)}=\mathrm{LSTM}(z_i(t), h_i^{(t-1)})$。
- 全分布式：每颗星独立构造局部状态、独立推理，不需要全局信息（第 III.E 节，L180）。

**4. 它声称的效果**
- 240 Mbps 时吞吐约 **210 Mbps**（ISL 容量 300 Mbps）（L254）。
- 240 Mbps 时端到端时延约 **498 ms**，是所有对比方法里最低（L256）。
- 丢包率降到"**低于 46.81%**"（L272）。
- 平均队列长度最多降 **23.26%**（L274）。
- 碳排：10000 次路由决策耗 $2.25\times10^{-4}$ kWh ≈ **0.111 g CO₂**，相当于 10 W LED 亮 81 秒（L294）。
- 基线：Dijkstra [19]、GraphPR [11]（GNN+MARL）、DQN-IR [8]（单 agent DRL）、FDR-MARL [3]（MARL 分布式）。
- 训练收敛（Fig 2）：本文方法收敛更快更稳，但**没有给任何收敛数值**（L248）。

**5. 实验条件**
45 颗星、倾角 70°、高度 570 km、载频 23.28 GHz、信道带宽 25 MHz、ISL 容量 300 Mbps、包长 1500 B、最大队列 640、TTL 30（表 I）。**负载 = 120 / 180 / 240 Mbps 三档**（轻/中/重）。流量模型 NHPP，$\lambda_i(t)=\lambda_0(1+\sin(2\pi t/T))$（L66）。超参（表 II）：GAT 4 头、GAT/LSTM 隐藏 64、最多 128 episodes、lr $1\times10^{-4}$、γ=0.99、回放 10 万、batch 128、目标网 200 步、ε 1.0→0.01 衰减 0.995。训练与评估在同一仿真环境，**未见跨分布测试**。注意 L188 逐字："Following the simulation setting in the thesis implementation" —— 这是学位论文衍生稿。

**6. 它自己承认的局限**
**没有独立的 Limitations 节。** 最接近的自述在结论 L300："Future work will extend this framework to QoS-aware routing, heterogeneous traffic scenarios, and cooperative multi-agent learning in large-scale LEO constellations."（即当前不支持 QoS、异构流量、协作多智能体）。另 L292 承认自身代价："the proposed GAT-LSTM-DQN based routing framework incurs higher computational complexity and inference time due to the joint spatial and temporal modeling."

**7. 它没做但看起来能做的地方**
1. **算力代价被承认却没被检验**：表 III 显示它的推理时间 2.70 ms，是最快的 FDR-MARL（0.56 ms）的 **4.8 倍**。作者只用"碳排绝对值很小"把它洗白，没做"星上算力受限时性能如何退化"的实验——而星上算力恰恰是硬约束。
2. **负载只扫 3 个点**（120/180/240），没有连续负载曲线；也**没有做"训练负载 ≠ 测试负载"的泛化实验**，而这是负载变化场景最该问的问题。
3. **NHPP 的参数没给**：周期 T 与基准 λ_0 全文未出现具体值，负载变化的"变化率"因此不可复现（L66 只有函数形式）。
4. **β>α 是人为武断设定**，没有任何 α/β 敏感性分析——而整个"主动拥塞避免"的卖点就压在这个比值上。
5. 式 2 定义了传播/传输/排队/处理四个时延分量，但**全文没有报告任何一个分量的占比**；498 ms 这个量级对 LEO 而言极高，不拆开就无法判断排队时延是否占绝对主导。

**8. 和同批其他篇的关系**
与 LBMABZJ7 方法相反（学习式 vs 几何闭式），但都做 LEO 分布式路由、都以时延为主要指标——是天然的对照组。与 L63JISQN 无关。它的基线 [3] FDR-MARL 与 [11] GraphPR 是 LEO DRL 路由的常见参照，同批其他学习式路由论文大概率也引这两篇。未见引用同批其他篇。

**9. 对"负载变化下到达率/时延"的贡献**
**直接相关，是同批里少见的把负载当自变量的论文。** 它把到达过程显式建成 NHPP 周期函数（L66），并把负载从 120 扫到 240 Mbps，Fig 3(b) 给出负载→端到端时延曲线（240 Mbps → 498 ms），Fig 4(b) 给出负载→队列长度，Fig 4(a) 给出负载→丢包率。但有三处硬伤：(a) 只有 3 个负载点，画不出拐点；(b) 498 ms 时延、46.81% 丢包这两个绝对值说明仿真里拥塞已极端严重，作者没有解释也没拆解成因；(c) 没有"训练-测试负载不匹配"实验，因此无法回答"负载分布变了策略还灵不灵"——而这正是选题要问的。

**10. 一句话评价**
把 GAT+LSTM+DQN 三个现成组件拼进 LEO 路由的"标准组合拳"论文；真正的论断是"空间与时间必须联合建模而非解耦"，但支撑它的实验只有 3 个负载点、单一拓扑、无跨分布测试，证据强度撑不起论断。

## LBMABZJ7 — Distributed On-Demand Routing for LEO Mega-Constellations: A Starlink Case Study

**1. 一句话**
给 Walker Delta 星座（Starlink 所属类型）推导"两颗星之间最少需要几跳 ISL"的闭式公式，再用它把搜索空间压成球面矩形，得到两个几乎零开销的按需分布式路由算法；核心论点是**跳数比距离更应该被优先最小化**。

**2. 问题设定**
巨型星座下"为所有卫星对、所有时刻预计算最短路"在空间与时间上都不可行（L7）；而已有的分布式按需路由只针对特定配置（极轨 Walker Star、ATM 式小包，跳数不重要），不适配越来越流行的 Walker Delta 巨型星座（L21）。前人的跳数公式（Chen et al. [5]）有一个错误假设："若某方向路径过长（如 $H_h>P/2$），包就走反方向"，这会产生不必要的多余跳（L111）。

**3. 方法骨架**
纯几何/算法，非 RL。
- **卫星模型**（第 II.B 节，L28–L50）：Kepler 元素 → 大地坐标 $\varphi=\arcsin(\sin\alpha\cdot\sin u)$、$\lambda=N(\Omega+\zeta(u))$，其中 $\zeta(u)=\arctan(\cos\alpha\tan u)+(0\ \text{或}\ \pi)$ 按升/降段取 → ECEF 笛卡尔 $(X,Y,Z)$。轨道半径 = h + WGS84 长半轴 6378.137 km。
- **Walker Delta**（第 II.C 节，L54–L56）：$\alpha{:}PQ/P/F$，$\Delta\Omega=2\pi/P$、$\Delta\Phi=2\pi/Q$、$\Delta f=2\pi F/(PQ)$；卫星 $(o,i)$ 由 $(L_0=N(o\Delta\Omega),\ u=N(o\Delta f+i\Delta\Phi))$ 确定。每颗星 **4 条 ISL**：同轨前/后 + 邻轨左/右，跨面绕回规则见 L58。
- **最少跳数模型**（第 III.A 节，L68–L107）：$\Delta L_0=(L_{0,2}-L_{0,1})\bmod 2\pi$ → 东西向的跨轨跳数 $H_h^{\leftarrow}=\lfloor(2\pi-\Delta L_0)/\Delta\Omega\rceil$、$H_h^{\rightarrow}=\lfloor \Delta L_0/\Delta\Omega\rceil$；跨轨跳会顺带改变相位角（每跳 +Δf），扣掉后得 $\Delta\vec u$、$\Delta\overleftarrow u$，再算四个方向的同类内跳数；**最终跳数 = 四种方向组合的最小值**，公式同时给出两个方向指示。
- **路由算法**（第 IV 节）：已知 $H_h,H_\nu$ 后，路径被限制在"源与目的为对角的球面矩形"内，矩形内**所有路径跳数相同**（类比 Manhattan Street Network，L169），因此构成 DAG，可用拓扑排序在 $O(V+E)$ 求最短路（DAGshort，替代 Dijkstra）(L171)；另有 DijkstraHops（堆里存 $(hops,distance)$ 按字典序比较）(L173)。
- **CoinFlipRoute**（第 IV.C 节，L177）：每跳抛硬币随机选两个方向之一，靠 $H_h/H_\nu$ 计数强制收尾。作者指出它**不等于**在矩形内均匀随机枚举路径。
- **DisCoRoute**（第 IV.D 节，L213–L258）：两条洞察——(1) 同轨跳长度恒定；(2) 异轨跳越靠近极点越短。于是"把异轨跳尽量安排在远离赤道处"。分两种情况：A2A/D2D 把异轨跳分配到路径两端、同类跳放中间，选择准则是 $|\varphi_i+\varphi_{i+1}|$ 更大者优先（算法 2）；A2D/D2A 必须靠近极点（只有那里才有升降轨之间的链路），因此反过来把同类跳放两端、异轨跳放中间，准则改为 $|\varphi_i+\varphi_{i+1}|$ 更小者（算法 3，L256）。

**4. 它声称的效果**
- 对 Chen 公式的改进：Starlink 星座上约 **2.7%** 的星对跳数被高估（1.26% 多 1 跳、1.01% 多 3 跳、0.44% 多 5 跳）（L115）。
- 最短路反而可能比最少跳路径多 1 跳，占 1% 的星对；此时两个公式一致（L117）。
- "含最少跳数的最短路"比"整体最短路"最多长 **2%**（≈1284 km），只发生在 1% 的星对上（L165, Fig 3）。
- 运行时间（Fig 5）：DAGshort 比 Dijkstra 平均快约 **22×**；DisCoRoute 比 Dijkstra 快约 **158×**、比 DAGshort 快 7×（L288）。CoinFlipRoute 平均比 DisCoRoute 略快但最坏情况更慢。
- 精确性（Fig 6）：以 DAGshort 为基线，Dijkstra 平均只优 0.02%、最坏 2%（L303）。
- 可扩展性（Fig 7）：4 个合成星座 60°:500/25/5、2000/50/10、8000/100/20、32000/200/40，各采样 10 万随机星对（L307）。

**5. 实验条件**
主星座 = Starlink 第一壳层 **Walker Delta 53.0°: 1584/72/39 @ 550 km**，其中相位因子 **F=39 是作者自己估计的**（L284 逐字："except for the phasing factor F = 39 which is not explicitly mentioned and had to be estimated based on the available documents and by inspecting the publicly available data"）。Python 与 Rust 双实现，测速用 Rust；Intel i7-6700 @3.40 GHz、32 GB；每个星对跑 10 次取平均（L280）。**全文没有负载、没有队列、没有拥塞、没有到达率** —— 只有几何与拓扑。训练/评估概念不适用。

**6. 它自己承认的局限**
L313 逐字："we are currently embarking on extensions of this work, taking into account congestion and background trafic, as well as further evaluations (e. g. route length and latency)."
L262："it becomes trivial to prove that the approximative DisCoRoute algorithm can solve the shortest path problem exactly for Walker Delta constellations with zero phase ofset $\Delta f=0$" —— 即最优性只在 Δf=0 时成立。
L270 承认 Theorem 2 在非零相位偏移下**无法形式化证明**，只能作为 Conjecture 1/2 提出。

**7. 它没做但看起来能做的地方**
1. **全文用跳数当时延代理但从未真算时延**。L167 给了一段很有用的量级论证（65535 B 包 @1 Gbps ≈ 500 μs 传输；一跳 ≈ 1000 km/光速 = 3.3 ms；星上处理可达数 ms），但**没有把它变成端到端时延指标**——作者自己在结论里承认要补 latency。
2. **完全无排队/拥塞建模**，而 DisCoRoute 的策略是"把异轨跳全部推向极区"，在负载不均时这会造成极区链路热点。论文没有讨论这个风险——这是一个明显的、由它自己的算法设计引出的问题。
3. **没有 ISL 失效/卫星故障场景**。
4. **只支持固定的 4 度 ISL 邻接**，未考虑实际 Starlink 的 ISL 规划与切换。
5. 相位因子 F 是估计值，但**没有做 F 的敏感性分析**——若 F 估错，跳数公式的误差有多大，未知。

**8. 和同批其他篇的关系**
同批里唯一的纯几何路由论文。与 LZKNZA8B（GAT-LSTM-DQN 分布式路由）构成方法对照：两者都主张分布式、都以 LEO 路由为题，但一个靠闭式几何、一个靠学习；LZKNZA8B 追求拥塞规避，本篇根本不建模拥塞。它直接改进的对象是 Chen et al. [5] 的 ISL 跳数模型。未见引用同批其他篇。

**9. 对"负载变化下到达率/时延"的贡献**
**无直接贡献，且作者明确承认。** 全文没有到达率、没有队列、没有负载扫描，所有结果都是"拓扑几何决定的最短路/最少跳路径"。唯一可复用的时延相关素材是 L167 的那段标尺：一跳 ≈ 1000 km 光速传播 = 3.3 ms，星上处理可达数 ms——这为"何时该为了少一跳而牺牲距离"提供了量化依据（作者的结论是：一跳的处理开销大于短路径省下的传播时延）。结论 L313 自认拥塞与背景流量是未做的扩展。

**10. 一句话评价**
把 Walker Delta 星座几何榨出闭式跳数公式的算法论文，用"跳数优先于距离"替换了经典最短路的度量选择；它是路由层的确定性基线，与 RL 路线的差距恰好在于它完全不处理负载与拥塞。
