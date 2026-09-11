# DOSSIER-B6：T2 机制级定读（11 篇）

> 批次：T2 → B6。产出 6 项：决策机制 / 代价函数公式逐字 / 粒度与动作 / 是否含学习 / 负载设置登记 / 可迁移点。
> 全文来源：VM /data/liguang13/topic-loop-r2/md/<key>/<key>/txt/<key>.md（MinerU MD）；所有行号为该 MD 的绝对行号。
> 红线遵守：承重结论带行号 + 逐字英文原文；公式逐字抄 LaTeX；"未见"声明带精确检索模式 + 实测计数 + 命中位置。
> **算法是主体，环境是实验条件**：负载/流量/评测设置仅作条件登记（第 5 项），不计入贡献。

---

## 0. 本批 11 篇一句话定位

| itemKey | 短名 | 决策对象 | 含学习 | 负载是否入模型 |
|---|---|---|---|---|
| DVS8C3CC | On-demand routing w/ dynamic LISLs (IEEE TAES 2024) | 端到端路由 + 路由保持时长 | 否 | **显式排除**（L375） |
| 36RZKNW5 | Integrated routing + data fragmentation (RSFFA) | M 条路由上的数据量分配 | 否 | 是（数据量 D 为决策输入） |
| LBMABZJ7 | DisCoRoute (Starlink case study) | 逐跳下一跳方向 | 否 | **无负载模型** |
| MYBALQ2D | TinyLEO (SIGCOMM'25) | 星座规模 + gateway 匹配 + 地理段转发 | 否 | 是（需求向量 y_t） |
| JS857IYN | DoTD (DTEG topology design) | 每卫星每时隙选 U 个 ISL 邻居 | 否（但有价值累积） | 否（只有链路容量/时延） |
| K7U4TYJN | SKYLINK | 每时隙每星出链路流量分配 | **是**（contextual MAB + UCB） | 是（全局流量 + 缓冲） |
| JZA5SEQA | Fast Reroute + Segment Routing | 域划分 + 备份路径维护 | 否 | 否（实验为随机节点图） |
| TRM2HPFN | DT-DVTR (Werner 1997) | 逐时隙路径选择 + 路径序列优化 | 否 | 否（只有呼叫模型） |
| XM6NUPM4 | MEGAREDUCE | 星座规模收缩（卫星子图） | 否 | 是（需求矩阵 + 容量约束） |
| WHS8Z44C | BDBC + TEDG (VNF 放置 + 路由) | VNF 放置 + 每时隙链路选择 | 否 | 是（服务集合 + 容量） |
| X2FCSU4S | Stackelberg 缓存负载均衡 | 每 LEO 上传到 GEO 的数据份额 | 否 | 是（到达过程 + 队列） |

---

## 1. DVS8C3CC — On-demand routing in LEO mega-constellations with dynamic laser inter-satellite links

**出处**：Bhattacharjee, Madoery, Chaudhry, Yanikomeroglu, Kurt, Hu, Ahmed, Martel；IEEE TAES 2024，DOI 10.1109/TAES.2024.3415571（L3–L15）。

### 1.1 决策机制

两个正交决策维度，作者自述逐字（L229）：

> "Each algorithm has two orthogonal perspectives: how the route is selected, and how long the selected route is active. Route selection can be based on the instantaneous or average latencies of the routes. The route, once selected, can be kept active for as long as possible (i.e., multiple time slots) or route selection can be performed in each time slot."

四种机制的定位（L231 逐字）：

> "In our benchmark algorithm, we apply Dijkstra's shortest route (DSR) algorithm [39] in each time slot. As this algorithm finds the route based on instantaneous latencies and route selection is performed in every time slot, the benchmark algorithm is termed as instantaneous latency based slotted routing (ILSR) algorithm."

> "Our first proposed algorithm termed as instantaneous latency based persistent routing (ILPR) also selects the shortest route using DSR based on instantaneous latencies, but keeps the selected route active as long as the route exists. In average latency based persistent routing (ALPR), route selection is based on the average latencies of the available routes, and the selected route is persistently used for as long as possible. Finally, in instantaneous stability and activeness based slotted routing (ISASR) algorithm, the route is selected based on the stability of the LISLs and whether the link is already active or not."

编排架构为 SDN 集中式（L116 逐字）：

> "For routing table calculation and distribution orchestration, we consider a software-defined networking (SDN) architecture where GSs and satellites as switches, and logically centralized controllers are physically distributed across the Earth. Ground controllers are responsible for calculating and distributing optimal routes, along with link information (A^[i]), so that nodes (GSs and satellites) associated with those routes, can establish the necessary links."

### 1.2 代价函数公式（逐字 LaTeX，行号即 MD 行号）

时延分量（L148，式 5）：
$$
\eta _ { d e l a y } = \sum _ { i = 1 } ^ { N } \sum _ { r \in \mathcal { R } } \delta _ { r } ^ { [ i ] } \alpha _ { r } ^ { [ i ] } .\tag{5}
$$

切换惩罚分量（L154，式 6）：
$$
\eta _ { p e n a l t y } = \eta _ { s } \sum _ { i = 1 } ^ { N - 1 } ( 1 - \sum _ { r \in \mathcal { R } } \alpha _ { r } ^ { [ i ] } \alpha _ { r } ^ { [ i + 1 ] } ) .\tag{6}
$$

总时延（L162，式 7）：
$$
\eta _ { L E } = \eta _ { d e l a y } + \eta _ { p e n a l t y } .\tag{7}
$$

平均时延（L168，式 8）：
$$
\overline { { \eta _ { L E } } } = \overline { { \eta _ { d e l a y } } } + \frac { \eta _ { s } } { N } \sum _ { i = 1 } ^ { N - 1 } ( 1 - \sum _ { r \in \mathcal { R } } \alpha _ { r } ^ { [ i ] } \alpha _ { r } ^ { [ i + 1 ] } ) .\tag{8}
$$

路由切换率（L174，式 9）：
$$
\lambda = \frac { 1 } { N } \sum _ { i = 1 } ^ { N - 1 } ( 1 - \sum _ { r \in \mathcal { R } } \alpha _ { r } ^ { [ i ] } \alpha _ { r } ^ { [ i + 1 ] } ) \times 1 0 0 \% .\tag{9}
$$

平均时延与 λ 的线性关系（L180，式 10）：
$$
\overline { { { \eta _ { L E } } } } = \overline { { { \eta _ { d e l a y } } } } + \frac { \eta _ { s } } { 1 0 0 } \lambda .\tag{10}
$$

优化问题（L186，式 11a）：
$$
\operatorname* { m i n } _ { \alpha _ { r } ^ { [ i ] } } \quad \sum _ { i = 1 } ^ { N } \sum _ { r \in \mathcal { R } } \delta _ { r } ^ { [ i ] } \alpha _ { r } ^ { [ i ] } + \eta _ { s } \sum _ { i = 1 } ^ { N - 1 } ( 1 - \sum _ { r \in \mathcal { R } } \alpha _ { r } ^ { [ i ] } \alpha _ { r } ^ { [ i + 1 ] } )\tag{11a}
$$
约束（L190 式 11b、L194 式 11c）：
$$
\mathrm { s . t . } \sum _ { r \in \mathcal { R } } \alpha _ { r } ^ { [ i ] } = 1 ; \forall i = 1 , 2 , . . . , N ,\tag{11b}
$$
$$
\alpha _ { r } ^ { [ i ] } \in ( 0 , 1 ) ; \forall r \in \mathcal { R } , i = 1 , 2 , . . . , N .\tag{11c}
$$
ILP 化后的目标（L200，式 12a）：
$$
\operatorname* { m i n } _ { \alpha _ { r } ^ { [ i ] } , \beta _ { r } ^ { [ i ] } } \quad \sum _ { i = 1 } ^ { N } \sum _ { r \in \mathcal { R } } \delta _ { r } ^ { [ i ] } \alpha _ { r } ^ { [ i ] } + \eta _ { s } \sum _ { i = 1 } ^ { N - 1 } ( 1 - \sum _ { r \in \mathcal { R } } \beta _ { r } ^ { [ i ] } )\tag{12a}
$$
ALPR 的"剩余生存期平均"度量（L277，式 13）：
$$
\overline { { { \eta } } } _ { r } ^ { [ i ] } = \frac { 1 } { l - i + 1 } ( \eta _ { s } + \sum _ { k = i } ^ { l } \delta _ { r } ^ { [ k ] } ) .\tag{13}
$$
ISASR 的边代价修改（L314，式 14）：
$$
\mathrm { c o s t } _ { m o d } = \mathrm { c o s t } _ { o l d } + \gamma \{ \mathrm { c o s t } _ { s t } + \mathrm { c o s t } _ { a c t } \} .\tag{14}
$$
ISASR 稳定性代价三段式（L320，式 15）：
$$
\begin{array} { r } { \mathrm { c o s t } _ { s t } ^ { [ i ] } = \left\{ \begin{array} { l l } { 0 } & { l = N } \\ { \frac { \eta _ { s } } { l - f + 1 } } & { i < f \mathrm { a n d } l < N } \\ { \frac { \eta _ { s } } { l - i + 1 } } & { f \leq i \leq l < N } \\ { \infty } & { l < i \leq N . } \end{array} \right. } \end{array}\tag{15}
$$
平均抖动（L450，式 16）：
$$
\mathrm { A v e r a g e ~ J i t t e r } = \frac { 1 } { N - 1 } \sum _ { i = 1 } ^ { N - 1 } \big | \delta _ { r } ^ { [ i ] } - \delta _ { r } ^ { [ i + 1 ] } \big | .\tag{16}
$$

### 1.3 粒度与动作

- **决策粒度**：以"源 GS–目的 GS 对"为单位，每时隙为该对选择**一条完整端到端路由**（不是逐跳）。动作是二值指示 alpha_r^[i]（L122 式 1：alpha_r^[i]=1 当 r=A^[i]，否则 0）。
- **动作的时间结构**：ILSR/ISASR 每时隙重选；ILPR/ALPR 选定即保持到路由失效（persistent，L231）。
- **ISASR 的复合动作**：删边（L341–343，式 15 阈值 cost_thrsh 过滤）→ 边代价更新（L344，式 14）→ 跑 DSR（L346）。
- **单路由硬约束**：式 11b 强制每时隙只有一条激活路由 —— **无双路径、无分流**，与 36RZKNW5 / WHS8Z44C 的多路径形成对照。

### 1.4 是否含学习

**结论：不含任何学习成分。** 全部算法是图搜索（DSR/Dijkstra）＋启发式代价加权，无参数学习、无梯度、无价值更新。

检索与实测（范围：该 MD 全文 568 行，命令 grep -niE，在 VM 上对全文执行）：
- 模式 /reinforcement learning|Q-learning|DQN|deep Q-network/ → **2 命中**：**L77**（转述文献 [27]："the authors propose a queuing delay and available bandwidth aware decentralized routing algorithm through reinforcement learning based training process"）、**L533**（参考文献 [27] 著录项）。**两处均为他人工作转述/著录，不是本文方法。**
- 模式 /dueling|prioriti[sz]ed (experience )?replay|double (q|dqn|deep q)|actor(-| )critic|\bppo\b|\bsac\b|policy gradient|a3c|ddpg|td3/ → **0 命中**（全库 11 篇同一计数见 §12）。
- 模式 /MDP|Markov (decision|chain)/ → **0 命中**。
- 模式 /reward/ → **0 命中**。

**作者自述的学习缺口（L465 逐字）**：

> "In particular, we envision the use of machine learning models to predict congestion situations even before they occur, and use these predictions as input to the route selection and link establishment process."

### 1.5 负载设置（实验条件登记，非贡献）

Table III（L367）逐字要点：Number of satellites 1584；orbits 24；satellites per plane 66；inclination 53°；altitude 550 km；satellite speed 7.6 km/s；LISL range 1500 km；GS range 1000 km；Node delay 1 ms；N=600；Duration of a time slot 1 second；cost_thrsh=100。

**关键条件声明（L375 逐字）**：

> "Considering very high data rate (tens of gigabits per second) LISLs, the transmission delay is assumed to be negligible. Also, as congestion is beyond the scope of this paper, queuing delay is not considered."

即：**本文显式把排队/拥塞排除在模型之外**，链路代价 = 传播 + 1 ms 节点时延。把本文当"无负载基线"引用时必须写明此边界。

### 1.6 可迁移点

1. **切换惩罚进目标函数**：式 6 / 式 10 把"路由改变次数 × 建立代价 eta_s"写成加性罚项，等价于 RL 中"动作切换成本（action-switching cost）"。式 10 给出了切换频率与切换代价之间可直接套用的线性关系。
2. **persistent vs slotted 的动作时间结构**：ILPR/ALPR 的"选定即保持"对应 RL 中的 **options / semi-MDP** 结构；本文给出了该结构的确定性对照基线，可用于判断 RL 是否真需要每时隙重决策。
3. **式 13 的"剩余生存期平均"**：不依赖学习的、带固定开销的折扣平均，可作为 RL 状态特征（当前路由剩余寿命）或 baseline 价值估计。
4. **式 15 的三段式 cost_st**：把"链路未来还剩多少时隙"映射为代价，可作为 RL 动作 mask 的构造依据（对即将失效的动作置 ∞）。
5. **gamma 与 eta_s 成比例的经验律**（L392 逐字）："> the optimal value of gamma increases with eta_s which motivates us to select gamma proportionally to eta_s" —— 一条"代价权重随环境参数缩放"的可复现超参规则。
6. **是否已被 RL 论文采用**：本批内可见 DVS8C3CC 自身引用 RL 工作 [27]（L535 参考文献）；但它**被** RL 论文引用的情况在本批 11 篇范围内无法验证，不做主张。

---

## 2. 36RZKNW5 — An integrated routing and data fragmentation strategy for optimizing end-to-end delay in LEO satellite networks

**出处**：Zhuotong Feng, Bo Li, Hongwei Ding, Fen Hou（云南大学 / 澳门大学），L1–L9。

### 2.1 决策机制

策略 = **时间切片 + 接触图模型 + BP bundle 分片多路径**。摘要逐字（L22）：

> "this paper proposes an innovative satellite network routing strategy that integrates time slicing and contact graph models. This strategy divides time into multiple segments, dynamically acquiring topological information for each segment and selecting the optimal set of routing paths based on the topology at each given moment. Furthermore, this paper introduces a strategy that combines routing selection with data fragmentation, optimizing data transmission paths through an efficient data allocation mechanism, which significantly reduces end-to-end delay and improves data transmission efficiency."

数据面机制（L70 逐字）：

> "In the proposed data fragmentation strategy, each data fragment selects the next optimal relay node based on the current network topology and communication conditions. If no next hop relay node can be found, the data can be temporarily stored, awaiting better network conditions or a new path before forwarding."

候选路径生成（L166 逐字）：

> "to reduce the computational complexity of path selection, we used the Yen algorithm to find multiple candidate paths and applied capacity filtering for each path."

### 2.2 代价函数公式（逐字 LaTeX）

传播时延（L102，式 1）：
$$
t _ { i , j } ^ { p r o p } = \frac { L _ { i , j } } { c }\tag{1}
$$
传输时延（L110，式 2）：
$$
t _ { i , j } ^ { t r a n s } = \frac { D _ { i , j } } { r _ { i , j } }\tag{2}
$$
等待时延（L116，式 3）：
$$
t _ { i , j } ^ { w a i t } = \left\{ \begin{array} { l l } { 0 , } & { \mathrm { i f ~ } t _ { i , j } ^ { s t a r t } \le t _ { n o w } , } \\ { t _ { i , j } ^ { s t a r t } - t _ { n o w } , } & { \mathrm { i f ~ } t _ { i , j } ^ { s t a r t } > t _ { n o w } . } \end{array} \right.\tag{3}
$$
链路容量（L124，式 4）：
$$
C _ { i , j } = ( I _ { i , j } - t _ { i , j } ^ { p r o p } ) \times r _ { i , j }\tag{4}
$$
单路由总时延（L130，式 5）：
$$
T _ { r } = \sum _ { c o n t a c t ( i , j ) \in r _ { k } } ( t _ { i , j } ^ { p r o p } + t _ { i , j } ^ { t r a n s } + t _ { i , j } ^ { w a i t } )\tag{5}
$$
**端到端时延 = 最慢路径**（L153，式 6）：
$$
T _ { M } = \operatorname* { m a x } _ { r \in \{ 1 , 2 , . . . , M \} } T _ { r }\tag{6}
$$
优化问题 P1（L137–L141 逐字照抄）：
> P1 : min T_M, or, min [max_{r∈{1,2,...,M}} T_r]
> s.t. C1 : Σ_{r=1}^{M} x_r = D
> C2 : x_r ≤ C_r y_r, ∀r ∈ {1,2,...,N}
> C3 : Σ_{r=1}^{N} y_r = M
> C4 : x_r ≥ 0, y_r ∈ {0,1}, ∀r ∈ {1,2,...,N}

### 2.3 粒度与动作

- **决策粒度**：不是逐跳在线决策，而是**每个时间片内一次性决定"选哪 M 条路由 + 每条分配多少数据"**。动作 = 连续向量 (x_1..x_N) + 二值选择 (y_1..y_N)，且 M 动态增长（L214 逐字）："> The value of M, which represents the number of routes selected for transmission, is dynamic and changes throughout the iterations."
- **算法结构**（Algorithm 1 RSFFA，L168–L208）：初始化 → 按 delay 排序 → 顺序灌满 → 找 max/min delay 路由 → 在两者间搬运数据量 transfer（L190–L191）→ 衰减 size×alpha（L195）→ 评估 T_M 是否改善，否则停止加路由（L203–L206）。
- **目标类型**：makespan 型（最慢路径决定），而非 sum 型。

### 2.4 是否含学习

**结论：不含学习成分。** 算法为确定性启发式（RSFFA），依赖排序 + 搬运 + 衰减因子 alpha + 收敛阈值 0.1（L197）。

检索与实测（范围：该 MD 全文 435 行，grep -niE）：
- 模式 /reinforcement learning|Q-learning|DQN|deep Q-network/ → **5 命中**：L52（相关工作泛述）、L60（相关工作泛述）、**L234（对比基线 PPO-CSO MR 的介绍）**、L386（参考文献 [13] GNN/DRL 路由）、L426（参考文献 [33] DTN 拥塞控制的 DRL）。**只有 L234 与本文实验直接相关，且明确作为被比较的第三方算法。**
  L234 逐字："> PPO-CSO Based Multipath Routing Algorithm (PPO-CSO MR) [36]: The PPO-CSO MR algorithm uses deep reinforcement learning to sense path states and identify multiple available paths for collaborative transmission. It also incorporates an adaptive traffic scheduling mechanism that dynamically adjusts traffic allocation based on changing path conditions, enabling multipath load balancing."
- 模式 /\bppo\b/ → **10 命中**（L60, 234, 286, 288, 290, 306, 314, 321, 327, 329），**逐条核验：全部是基线名 PPO-CSO MR 或其结果讨论**；本文自身方法不涉及 PPO。（该模式带词边界，不含裸 prioritized / 裸 double，按主控教训避免散文词误命中。）
- 模式 /MDP|Markov (decision|chain)/ → **1 命中**：**L60**（相关工作段转述他人 DRL 工作，逐字："Several works focusing on deep-space DTNs, characterized by high latency and constrained resources, embed a delay model into the Markov Decision Process and apply Proximal Policy Optimization (PPO) for congestion control [33]."）。**是他人工作的转述，不是本文方法。**
- 模式 /reward/ → **0 命中**。

### 2.5 负载设置（实验条件登记）

Table 3（L260）逐字：Satellite constellation = Iridium-NEXT；Orbital altitude 780 km；Orbital period 102 min；Time slice duration 6 min；Number of time slices in one period W = 17；Number of algorithm iterations 100；**Data volume D = [100, 1000] MB**；Data transfer attenuation factor alpha = 0.9；Initial transfer size 10 MB；Inter-satellite transmission rate r = 25 Mbps；Ground-satellite transmission rate r_g = 20 Mbps。

仿真器：DtnSim（L248）。负载以"总数据量 D"形式进入模型，**没有到达过程 / 突发性建模**；拥塞只通过容量约束 C_r 间接体现。

### 2.6 可迁移点

1. **makespan 型端到端目标（式 6）**：当 RL 动作为"多路径 / 多下一跳并行传输"时，奖励应以 max 而非 sum 聚合。这是本批中唯一把 max 型目标写进代价函数的论文。
2. **容量过滤作为动作 mask**（L166 "capacity filtering"）：把不满足最小分片容量需求的路径预先剔除，对应 RL 的 **action masking**，可直接复用为可行性掩码构造规则。
3. **alpha 衰减 + 收敛阈值的停止规则**（L195–L197）：size ← size × alpha，当 max(Delay) − min(Delay) ≤ 0.1 或迭代耗尽则停。可作为 RL 中"何时停止继续增加并行动作"的确定性启发式。
4. **store-and-forward 的等待时延项（式 3）**：t_wait = max(0, t_start − t_now)，把"链路未可用时的等待"显式建模为可加项，可迁移为 RL 状态特征（到下一个接触窗口的时间）。
5. **自述局限（L344 逐字）** 可用于诚实定位："> First, the computational complexity of the algorithm is relatively high, particularly in large-scale satellite networks where increasing numbers of routes and nodes lead to significant computational overhead. Second, the study primarily focuses on validating the strategy in simulation environments."

---

## 3. LBMABZJ7 — Distributed On-Demand Routing for LEO Mega-Constellations: A Starlink Case Study

**出处**：Gregory Stock, Juan A. Fraire, Holger Hermanns（Saarland University），L3。

### 3.1 决策机制

核心是**闭式最小跳数公式 + 由它诱导的球面矩形搜索空间**，再加两个不做全局搜索的分布式算法。摘要逐字（L9）：

> "First, we introduce a formal model that mathematically captures the time-evolving locations of satellites in a Walker Delta constellation and use it to establish a formula to compute the minimum number of ISL hops between two given satellites. In the second part, we present an on-demand hop-count-based routing algorithm that approximates the optimal path while achieving superior performance compared to classical shortest-path algorithms like Dĳkstra."

搜索空间压缩（L169 逐字）：

> "Knowing the minimum number of hops in both dimensions and their directions between two satellites allows the routing algorithm to restrict the exploration: The search space can be reduced significantly, forming a spherical rectangle where the source and destination satellites are at opposing corners. Note that in this rectangle, every possible route from the source to the destination has the same number of hops (similar to a Manhattan Street Network [8])."

DisCoRoute 的两条几何洞察（L215–L219 逐字）：
> "1) The length of an intra-plane hop is always constant in the constellation, independent of the satellite's positions. 2) The length of an inter-plane hop should decrease the further it is away from the Equator."
> "Therefore, the main idea is to cleverly distribute the inter-plane hops so that they happen as close as possible to the poles."

### 3.2 代价函数公式（逐字 LaTeX）

经度差（L71）：
$$
\Delta L _ { 0 } = \left( L _ { 0 , 2 } - L _ { 0 , 1 } \right) { \bmod { 2 \pi } } \in [ 0 , 2 \pi |
$$
方向性 inter-plane 跳数（L77）：
$$
H _ { h } ^ { \left. } = \left\lfloor \frac { 2 \pi - \Delta L _ { 0 } } { \Delta \Omega } \right\rceil \qquad H _ { h } ^ { \right. } = \left\lfloor \frac { \Delta L _ { 0 } } { \Delta \Omega } \right\rceil
$$
相位角关系（L86）：
$$
u _ { 2 } = u _ { 1 } + ( H _ { h } ^ {  } \cdot \Delta f ) + \underbrace { ( H _ { \nu } ^ { \nearrow } \cdot \Delta \Phi ) } _ { \Delta \vec { u } }
$$
相位差分解（L92）：
$$
\begin{array} { r } { \Delta \stackrel { \right. } { u } = ( u _ { 2 } - u _ { 1 } - H _ { h } ^ { \right. } \cdot \Delta f ) \bmod 2 \pi } \\ { \Delta \stackrel { \left. } { u } = ( u _ { 2 } - u _ { 1 } + H _ { h } ^ { \left. } \cdot \Delta f ) \bmod 2 \pi } \end{array}
$$
方向性 intra-plane 跳数（L98）：
$$
\begin{array} { l } { { \hat { H } _ { \nu } ^ { \setminus } = \displaystyle \left\| \displaystyle \frac { \displaystyle \bigtriangleup \overleftarrow { u } } { \displaystyle \Delta \Phi } \right\| } } & { { \qquad H _ { \nu } ^ { / } = \displaystyle \left\lfloor \displaystyle \frac { \Delta \overrightarrow { u } } { \displaystyle \Delta \Phi } \right\rceil } } \\ { { \displaystyle H _ { \nu } ^ { \swarrow } = \displaystyle \left\lfloor \displaystyle \frac { 2 \pi - \Delta \overleftarrow { u } } { \Delta \Phi } \right\rceil } } & { { \qquad H _ { \nu } ^ { \setminus } = \displaystyle \left\lfloor \displaystyle \frac { 2 \pi - \Delta \overrightarrow { u } } { \Delta \Phi } \right\rceil } } \end{array}
$$
最小跳数（L104）：
$$
\operatorname* { m i n } \{ H _ { h } ^ { \left. } + H _ { \nu } ^ { \setminus } , ~ H _ { h } ^ { \left. } + H _ { \nu } ^ { \angle } , ~ H _ { h } ^ { \right. } + H _ { \nu } ^ { \prime } , ~ H _ { h } ^ { \right. } + H _ { \nu } ^ { \setminus } \}
$$
DisCoRoute 的几何"奖励"（L188–L189，Algorithm 2）：
> reward_s ← |phi_{i,0} + phi_{i+1,0}|
> reward_t ← |phi_{j,H_nu} + phi_{j-1,H_nu}|
（Algorithm 3 对应 L235–L236：reward_s ← |phi_{0,i} + phi_{0,i+1}|、reward_t ← |phi_{H_h,j} + phi_{H_h,j-1}|）

**跳数优先于路径长度的量化论证（L167 逐字）**：

> "As the signals travel with the speed of light, it is clear that slightly shorter routes do not compensate for the overhead of an additional hop. For example, the transmission time of a packet of size 65 535 bytes (largest possible IPv4 payload) at an ISL rate of 1 Gbps is about 500 microseconds. Even if faster ISL data rates are leveraged, there is internal packetisation and queuing delay which can easily add up to several milliseconds of on-board processing, even when using highly eficient ATM fabrics [7]. A single hop is thus comparable with the propagation delay of 1000 km distance at the speed of light (299 792 km s) totalling 3.3 ms."

### 3.3 粒度与动作

- **决策粒度：逐跳、分布式**。每颗卫星本地决定下一跳走 intra-plane 后继还是 inter-plane 右邻居。摘要（L15 逐字）："> The algorithms have almost no overhead and work in a distributed way, as neither an exhaustive exploration nor a centralised precomputation of the path is needed."
- **动作空间被闭式公式限制在球面矩形内**，且"每条可能路由跳数相同"（L169）—— 极端压缩的动作空间。
- **两种动作策略**：CoinFlipRoute（每星抛硬币随机选方向，L177 逐字："it flips a coin at each satellite to randomly decide in which of the two directions the packet should continue"）；DisCoRoute（按纬度绝对值和选更靠近极地的方向，L188–L195 / L235–L243）。
- Algorithm 2/3 的 assert（L198、L245）保证最终落到同一轨道平面。

### 3.4 是否含学习

**结论：不含学习成分。**

检索与实测（范围：该 MD 全文 340 行，grep -niE）：
- 模式 /reinforcement learning|Q-learning|DQN|deep Q-network/ → **0 命中**。
- 模式 /dueling|prioriti[sz]ed (experience )?replay|double (q|dqn|deep q)|actor(-| )critic|\bppo\b|\bsac\b|policy gradient|a3c|ddpg|td3/ → **0 命中**（全库计数见 §12）。
- 模式 /MDP|Markov (decision|chain)/ → **0 命中**。

**必须澄清的假阳性（防止后续误判为"含学习"）**：模式 /reward/ 在该文 **6 命中**，位置 **L188、L189、L190**（Algorithm 2）与 **L235、L236、L237**（Algorithm 3），全部是 DisCoRoute 内部用于比较两跳纬度和的**几何量** reward_s / reward_t，**与强化学习奖励无关**。这是本批最容易误判为"含学习"的陷阱，特此登记。

### 3.5 负载设置（实验条件登记）

- Starlink 第一轨道壳：Walker Delta 53.0 deg : 1584/72/39 at 550 km（L284）。
- 可扩展性测试星座（L307）：60 deg : 500/25/5、60 deg : 2000/50/10、60 deg : 8000/100/20、60 deg : 32 000/200/40；每个采样 100 000 随机卫星对。
- **本文无流量/负载模型**：全文评测指标为运行时间（L288）、路径长度（L296）与可扩展性（L305），不涉及到达过程、队列、缓冲或丢包。
- **自述下一步（L313 逐字）** 直接承认："> Furthermore, we are currently embarking on extensions of this work, taking into account congestion and background trafic, as well as further evaluations (e. g. route length and latency)."

### 3.6 可迁移点

1. **闭式可达性/下界作为动作掩码**：L104 的最小跳数组合直接给出"任意合法路由的跳数下界 + 方向指示"，可作为 RL 动作空间的硬约束（把 O(M) 邻居选择压到球面矩形内的 2 个方向）。这是本批中**最强的动作空间压缩机制**。
2. **"跳数优先于长度"的度量选择论证（L167）**：给出把"每跳固定处理开销"折算为等效距离（约 1000 km ≈ 3.3 ms）的**可复算换算**，可直接用于确定 RL 奖励中 hop 项与 delay 项的权重比。
3. **随机化基线（CoinFlipRoute）是最重要的反例警示**：在压缩后的动作空间内随机选方向性能已相当好（L288 逐字："CoinFlipRoute has a slightly lower mean than DisCoRoute but is slower in the worst case"）。**若 RL 在同类压缩动作空间内不能显著超过"随机选方向"，则学习没有价值。**
4. **近似算法的最优性边界**（L298 逐字）："the hop-count-based algorithms are all approximates and do not always find the overall optimal solution"；Dijkstra 最坏可短 2%，均值仅 0.02%（L303）。可作为"近似度"的定量参照。
5. **被同批 T2 论文引用**：DVS8C3CC 的参考文献 [23]（L523）即本文。**"被 RL 论文采用"在本批范围内无证据，不做主张。**

---


## 4. MYBALQ2D — Small-scale LEO Satellite Networking for Global-scale Demands (TinyLEO)

**出处**：Yuanjie Li 等（清华大学 / 中关村实验室），ACM SIGCOMM 2025，DOI 10.1145/3718958.3750525（L3、L21）。

### 4.1 决策机制

三层解耦：离线稀疏综合（压缩感知）→ 控制面（地理意图 + 轨道 MPC）→ 数据面（地理段任播）。摘要逐字（L9）：

> "We thus propose TinyLEO, a software-defined solution to shrink LEO network size for enormous global demands via dynamic spatiotemporal supply-demand matching. TinyLEO sparsifies satellite supplies on demand by combining diverse yet sparse orbits, hides complexities of this sparse LEO network via orbital model predictive control, and shifts the responsibility for handling these complexities to its geographic segment anycast for higher network usability, lower resource wastes, faster failovers, simpler satellites, and more flexible network orchestration."

控制面机制（L263 逐字）：

> "It seeks to stabilize the LEO network topology as long as possible since frequent ISL reconfigurations are not desirable [17, 38]. To this end, TinyLEO adopts a three-stage stable matching."

三阶段：① cell u → 邻 cell v 的 many-to-one 稳定匹配（Gale-Shapley）；② u 内卫星 s 与 v 内卫星 s' 的一对一稳定匹配（用 ISL 生存期 tau_{s,s'} 作偏好）；③ cell 内把匹配上的 gateway 卫星连成环。

数据面机制（L294 逐字）：

> "Upon receiving a packet, each satellite extracts its next-hop geographic cell (segment) to forward to. If it has a direct ISL to a gateway satellite covering this next-hop cell, it immediately forwards this packet through this ISL. Otherwise, it uses the "intra-domain" ring in §4.2 to clockwise pass this packet to its next neighboring satellite inside the same cell."

### 4.2 代价函数公式（逐字 LaTeX）

地球重复轨道条件（L186，式 1）：
$$
T / T _ { E } = p / q , \ p , q \in \mathbb { N } ^ { + }\tag{1}
$$
稀疏匹配目标（L208，式 2）：
$$
\begin{array} { r l r l } { \operatorname* { m i n } } & { { } } & { \left| \left| \mathbf { x } \right| \right| _ { 1 } } \end{array}\tag{2}
$$
覆盖约束（L212，式 3）：
$$
\mathrm { s . t . } \quad \mathbf { A _ { t } x } \geq \mathbf { y _ { t } } \quad \forall t = 1 , 2 , . . . , T _ { m a x }\tag{3}
$$
整数约束（L216，式 4）：
$$
x _ { i } \in \mathbb { N } \qquad \forall i = 1 , 2 , . . . , n\tag{4}
$$
gateway 偏好权重（L266）：
$$
\tau _ { S , v } = \frac { 1 } { n _ { v } } \sum _ { s ^ { \prime } \in v } \tau _ { s , s ^ { \prime } }
$$

式 2–4 的性质（L224 逐字）："> Equation 2–4 is a standard integer linear programming problem, which is NP-hard in general [35]. Fortunately, in our context, the LEO network supply x, the network demand y_t, and satellite coverage matrix A_t are all sparse. This domain-specific property can cast our optimization as a sparse signal recovery problem, which can be more eficiently solved with compressed sensing techniques [19–22]."

### 4.3 粒度与动作

三个不同粒度的决策，是本批中**粒度层次最丰富**的一篇：
1. **星座级（离线）**：决定每条地球重复轨道放几颗卫星 —— 式 2–4 的整数向量 x（L203 逐字："> It will optimize the number of satellites x_j >= 0 (x_j in N) to place in this orbit and their distributions"）。由 matching pursuit 贪心迭代（Alg.1，L226）。
2. **cell 级（在线，每时隙）**：决定哪些卫星做通往哪个邻 cell 的 gateway —— 三阶段稳定匹配（L263）。
3. **包级（数据面）**：只决定**下一个地理 cell**，不决定具体卫星（L294）。段列表形如 u → w1 → w2 ... v（L256）。

**与 RL 路由的关键结构性差异**：动作被定义为"地理不变量"而非卫星实例（L280–L282 逐字）："> each segment in this route represents a geographic cell. It is stable and decoupled from the rapidly changing satellites. Any satellite covering this cell can receive a packet destined for this segment" —— 动作空间不随卫星运动而膨胀。

### 4.4 是否含学习

**结论：不含学习成分。** 三个机制分别是压缩感知（匹配追踪）、模型预测控制（基于轨道律的预测）、Gale-Shapley 稳定匹配，均为确定性算法。

检索与实测（范围：该 MD 全文 640 行，grep -niE）：
- 模式 /reinforcement learning|Q-learning|DQN|deep Q-network/ → **0 命中**。
- 模式 /dueling|prioriti[sz]ed (experience )?replay|double (q|dqn|deep q)|actor(-| )critic|\bppo\b|\bsac\b|policy gradient|a3c|ddpg|td3/ → **0 命中**（全库计数见 §12）。
- 模式 /MDP|Markov (decision|chain)/ → **0 命中**。
- 模式 /reward/ → **0 命中**。
- 模式 /MORL/（大小写不敏感）→ **1 命中，为假阳性**：**L621** 参考文献作者名 "Z Morley Mao"（"> ...Nitin Varyani, Z Morley Mao, Feng Qian, and Zhi-Li Zhang..."）。**不构成多目标 RL 证据。**

**必须注意的措辞陷阱**：MPC（model predictive control）在形式上与 RL 的"序贯决策"同构。L258 逐字："As a classic sequential decision-making framework, MPC lets us iteratively collect the runtime LEO network status, forecast its short-term evolutions based on these feedbacks and orbital laws, and decide near-term control actions with these predictions." —— 但**预测模型来自轨道律而非学习**，不得登记为学习成分。

### 4.5 负载设置（实验条件登记）

- 需求模型：把地表分成 m 个地理 cell，输入每 cell 每时刻的**最大可服务需求 y_i^t，单位是"卫星数"**（L201 逐字）；该需求可包含无线接入容量、ISL 容量、冗余、故障备份、昼夜动态等因素（L201）。
- 候选轨道库：Table 1（L319）—— 高度 423–1,873 km；周期 92.8–124.2 min；RAAN [−pi, pi]；倾角 [0, pi]；**总地面轨迹数 64,800**。
- 三类需求场景：Starlink、Internet backbone、Latin America（Fig.13/14，L324–L334）。
- 评测结果（摘要 L9）："> Our evaluation using this toolkit shows that TinyLEO can compress the existing LEO mega-constellation network size by 2.0–7.9x, cut control plane costs by 1–3 orders of magnitude, and maintain the same demands and comparable data plane performance."

### 4.6 可迁移点

1. **动作空间的地理不变化（本批最强可迁移点）**：把 RL 的动作从"选哪颗卫星"改为"选哪个地理 cell 段"（L280），使动作维度与卫星运动解耦、不随时间膨胀。这直接回应 LEO RL 路由中 state/action 空间随时变拓扑漂移的问题。
2. **偏好权重 = 期望 ISL 生存期 tau**（L263–L269）：把"动作持久性"作为排序偏好，可在 RL 中作为奖励的稳定项（鼓励选长寿命链路）。
3. **失败修复的增量式重匹配（L271 逐字）**："> It checks the unsatisfied residual demands of the geographic intent after failures, incrementally runs the above three-stage matching for residual demands, and finds new ISLs/satellites to replace failed ones." —— 只对"残余需求"重算而非全局重优化，可作为 RL 中断链重路由的低开销策略。
4. **局部最优陷阱的显式处理（对 RL 逐跳贪心的警示）**（L290 逐字）："> Despite appealing, geographic routing is prone to forwarding failures due to its local greedy nature. Without global routes, it can get stuck in a "local minimum" where a node is closer to the destination than all its neighbors but is obstructed from reaching it."
5. **环作为连通性保证**（L294）：cell 内 gateway 连成环保证段内可达；环断裂则缓冲至 MPC 修复。

---

## 5. JS857IYN — Time-Dependent Network Topology Optimization for LEO Satellite Constellations (DoTD)

**出处**：L1 标题；IEEE 风格期刊稿，TLE 数据来自 CelesTrak（L264）。

### 5.1 决策机制

**动态时间扩展图（DTEG）+ 动态规划打分选边**。摘要逐字（L27）：

> "In this paper, we introduce the Dynamic Time-Expanded Graph (DTEG)-based Optimal Topology Design (DoTD) algorithm to tackle these challenges effectively. We first formulate a novel space network topology optimization problem encompassing a multi-objective function – maximize network capacity, minimize latency, and mitigate link churn – under key inter-satellite link constraints. Our proposed approach addresses this optimization problem by transforming the objective functions and constraints into a time-dependent scoring function."

打分机制的核心比喻（L155 逐字）：

> "The concept of a score is widely understood as an indicator used to evaluate student outcomes. Top students are ranked based on the assessment of their time-dependent scores obtained from exams, assignments, and homework. With this key idea, the proposed DoTD algorithm enables each LEO satellite to evaluate others based on their scores and select the top U satellites with the highest scores to establish link connections."

DTEG 构造（L142–L148）：T 分为等长时隙 tau，节点集 V = {v_{i,t}}，共 |V| x (T_hat + 1) 个节点；空间链路 (v_{i,t}, v_{j,t+1})。

### 5.2 代价函数公式（逐字 LaTeX）

原始优化问题 P1（L131）：
$$
\begin{array} { r l } & { \displaystyle \mathbf { P } \mathbf { 1 } { \operatorname* { m a x } } \Big ( \displaystyle \sum _ { i = 1 } ^ { M } \sum _ { j = 1 \backslash \left\{ i \right\} } ^ { M } \phi _ { i , j , t } \big ( S _ { i , j , t } + \frac { 1 } { L _ { i , j , t } } + \phi _ { i , j , t - 1 } \big ) \Big ) } \\ & { \mathrm { ~ s . t . ~ } \displaystyle \sum _ { j = 1 } ^ { M } \phi _ { i , j , t } \leq U , \forall i \in \{ 1 , \ldots , M \} } \\ & { \qquad \displaystyle \mathbf { C 2 } \cdot \phi _ { i , j , t } = \phi _ { j , i , t } , \forall i , j \in \{ 1 , \ldots , M \} , } \\ & { \qquad \displaystyle \mathbf { C 3 } \cdot \Gamma _ { i , j , t } > \Gamma _ { A t m o s p } , \forall i , j \in \{ 1 , \ldots , M \} , } \\ & { \qquad \displaystyle \mathbf { C 4 } : D _ { i , j , t } < D _ { M a x } , \forall i , j \in \{ 1 , \ldots , M \} , } \end{array}\tag{10}
$$
归一化（L158，式 11）：
$$
\bar { S } _ { i , j , t } = \frac { S _ { i , j , t } } { S _ { \mathrm { { M a x } , \it { t } } } } ; \bar { L } _ { i , j , t } = \frac { L _ { i , j , t } } { L _ { \mathrm { { M a x } , \it { t } } } } ; \bar { \phi } _ { i , j , t } = \frac { \phi _ { i , j , t } } { U } ,\tag{11}
$$
时变最大值递推（L164，式 12）：
$$
\begin{array} { l } { g _ { \mathrm { M a x } , t } = \operatorname* { m a x } \{ g _ { \mathrm { M a x } , t - 1 } , } \\ { \displaystyle \operatorname* { m a x } _ { i \in \mathcal { M } , j \in \mathcal { M } } ( \mathbf { 1 } _ { \{ \Gamma _ { i , j , t } > \Gamma _ { A t m o s p } \} } \mathbf { 1 } _ { \{ D _ { i , j , t } < D _ { M a x } \} } g _ { i , j , t } ) \} , } \end{array}\tag{12}
$$
**链路代价（多目标加权归一）**（L170，式 13）：
$$
A _ { i , j , t } = w _ { 1 } \bar { S } _ { i , j , t } + w _ { 2 } ( 1 - \bar { L } _ { i , j , t } ) + ( 1 - w _ { 1 } - w _ { 2 } ) \bar { \phi } _ { i , j , t - 1 } ,\tag{13}
$$
**打分函数（带历史累积）**（L176，式 14）：
$$
\alpha _ { i , j , t } = \mathbf { 1 } _ { \left\{ \Gamma _ { i , j , t } > \Gamma _ { A t m o s p } \right\} } \mathbf { 1 } _ { \left\{ D _ { i , j , t } < D _ { M a x } \right\} } \big ( A _ { i , j , t } + \Pi _ { j , t - 1 } \big ) ,\tag{14}
$$
最优链路选择（L182，式 15）：
$$
\phi _ { i , j , t } ^ { * } = \underset { l \in \cal { M } } { \mathrm { a r g m i n } } ( \{ \alpha _ { i , l , t } | ( \sum _ { k = 1 } ^ { M } \phi _ { i , k , t } ^ { * } < U \cap \sum _ { k = 1 } ^ { M } \phi _ { j , k , t } ^ { * } < U ) \} ) .\tag{15}
$$
**分数更新规则（形如价值迭代）**（L188，式 16）：
$$
\Pi _ { i , t } = \frac { 1 } { U } \sum _ { j = 1 \backslash \{ i \} } ^ { M } \phi _ { i , j , t } ^ { \ast } \left( A _ { i , j , t } + \Pi _ { j , t - 1 } \right) .\tag{16}
$$
有界性（Lemma III.2，L203）：Pi_{i,t} < infinity, T -> infinity。证明尾部（L211 逐字）："> From (13), L_bar_{i,j,t} > 0 and phi_bar_{i,j,t-1} < 1 => A_{i,j,t} < 1, for all t. Then, from (17), if T -> infinity => U^T -> infinity; thus, Pi_{i,T} < infinity."

物理量公式位置（供回溯）：仰角关系 L71 式 1；星地距离 L77 式 2；信道增益 L83 式 3；容量 L89 式 4；链路选择 L95 式 5；ISL 可见性 L105 式 6；ISL 信道 L111 式 7；ISL 容量 L117 式 8；ISL 时延 L123 式 9。

### 5.3 粒度与动作

- **决策粒度：每时隙、每颗卫星，选择最多 U 个邻居建立 ISL**（拓扑设计），U = 4（L264 逐字）："> Our proposed DoTD approach in Algorithm 1 generates the network topology that allows each satellite to connect with four other satellites."
- 动作是二值矩阵 phi_{i,j,t}，强制对称（C2: phi_{i,j,t} = phi_{j,i,t}；Alg.1 line 20 显式赋值）。
- **本文不决定逐包路由**：路由由 OSPF 在 DoTD 生成的拓扑上运行（L252 逐字）："> We apply the Open Shortest Path First (OSPF)-based method to the optimal network topology obtained by our proposed DoTD algorithm."
- 拓扑更新周期（L252 逐字）："> The proposed Algorithm 1 updates the network topology at intervals of T, where T can be several minutes or more (e.g., 10 minutes). This update interval is restricted by constraints related to configuration complexity, service continuity, and stability, which prevent updates at sub-second intervals."
- 复杂度（L215 逐字）："> the time complexity of the proposed algorithm equals to O(T_hat M^2) ... Consequently, the time complexity of the proposed algorithm simplifies to O(M^2)."

### 5.4 是否含学习

**结论：不含学习成分（无梯度 / 无试错 / 无策略更新），但含"价值累积"结构** —— 式 16 的形式与时间差分 / 价值迭代高度相似，是一个必须精确措辞的边界案例。

检索与实测（范围：该 MD 全文 389 行，grep -niE）：
- 模式 /reinforcement learning|Q-learning|DQN|deep Q-network/ → **2 命中**：**L42**（相关工作泛述）、**L356**（参考文献 [25] "A topology design method for satellite networks based on deep reinforcement learning"）。**均为他人工作，非本文方法。**
- 模式 /dueling|prioriti[sz]ed (experience )?replay|double (q|dqn|deep q)|actor(-| )critic|\bppo\b|\bsac\b|policy gradient|a3c|ddpg|td3/ → **0 命中**（全库计数见 §12）。
- 模式 /MDP|Markov (decision|chain)/ → **0 命中**。
- 模式 /reward/ → **0 命中**。
- **必须登记并逐条核验的模式** /q-table|bellman|temporal difference|value function/ → **7 命中**（L148, 173, 215, 224, 252, 276, 300）。**逐条核验：全部是本文自造的 "score value function"（打分值函数），指式 14/16 的打分**。例：L300 逐字 "we formulated a score value function by normalizing multiple objective functions to a common range from 0 to 1"；L148 逐字 "The score value function is a weighted sum of normalized values for capacity, latency and link churns"。**无一处指贝尔曼方程、Q 表或时序差分学习。** 故"无学习"成立，此核验说明为负向声明的必备证据。

### 5.4b 关于缺口 G-A 的边界说明（提前标注）

式 13 是本批中**唯一**把多个目标显式分解成不同系数项的代价函数（容量、时延、链路抖动三项，各带权重 w1 / w2 / (1−w1−w2)），但：
- 分解轴是**目标类型**（capacity / latency / link churn），**不是失败原因**；
- 三项被**线性标量化为单一 A_{i,j,t}**，**没有独立的学习通道或独立惩罚项**；
- 全程无学习（见上）。
因此式 13 **不构成对缺口 G-A 的反例**，但它是最接近"多目标分解"机制的确定性对照物（详见 §13）。

### 5.5 负载设置（实验条件登记）

Table I（L254）逐字要点：光速 3 x 10^8 m/s；LEO 速度 7.66 km/s；大气层高 50 km；地球半径 6378 km；载频 12.2 GHz；总带宽 100 MHz；极化损耗 4.5 dB；失配损耗 0.5 dB；GS 天线增益 33.2 dBi；LEO 天线增益 40 dBi；最大通信距离 D_Max 7000 km；链路选择数 U = 4；**LEO 卫星数 907**；目标权重 w1 = w2 = 0.4。

- 实验场景：TABLE II（L267）5 组 GS 源–目的对（S1 悉尼→达尔文；S2 迈阿密→卡尔加里；S3 纽约→迈阿密；S4 纽约→旧金山；S5 金边→加德满都）。
- **本文无流量 / 拥塞负载模型**：代价只用链路容量 S_{i,j,t}、时延 L_{i,j,t} 与链路抖动三项，不涉及到达过程、队列或缓冲。把本文结果外推到高负载场景时必须声明此边界。
- 结果量级（L284、L296 供登记）：hop count 平均降低 10.91%（vs Greedy）、最高 81.82%（vs +Grid）；时延 4.2 ms（vs Greedy 9.9 ms、+Grid 203.6 ms）；容量平均提升 28.09%（vs Greedy）、最高 70.47%（vs +Grid）。

### 5.6 可迁移点

1. **式 13 + 式 14 + 式 16 是一整套"无学习的价值累积"机制**：多目标归一化 → 加权求和 → 加历史项 → argmin 选择 → 历史项更新。可作为 RL 奖励塑形的**确定性 ablation 对照**：若 RL 不能超过这套零参数启发式，则学习无增益。这是本批中对"RL 是否必要"最直接的可反驳对照。
2. **链路抖动项 phi_{i,j,t-1}**（式 13 第三项）：显式奖励"与上一时隙保持同一条链路"，即**切换惩罚的正面写法**（与 DVS8C3CC 式 6 的罚项写法互为镜像）。
3. **时变归一化 + 单调递增的最大值**（式 11–12 与 Lemma III.1，L191–L199）：解决"不同时隙量纲不可比"的问题，可直接复用于 RL 状态 / 奖励的在线归一化。
4. **对称性约束**（C2 + Alg.1 line 20）：多智能体场景中"动作需成对一致"的约束形式，可迁移为互斥动作掩码。
5. **O(T_hat M^2) -> O(M^2) 的复杂度论证**（L215）：给出"把时间轴折进常数"的推理，可作为 RL 中时域截断的复杂度参照。

---

## 6. K7U4TYJN — SKYLINK: Scalable and Resilient Link Management in LEO Satellite Networks

**出处**：L3 标题；IEEE 风格，OneWeb 数据 + 自研 stream-based 仿真器（L313）。

### 6.1 决策机制（本批唯一"含学习"的确定性案例）

**每颗卫星独立的 contextual multi-armed bandit + UCB 排序 + 水填充流量分配**。逐字证据：

L401（结论）：
> "SKYLINK uses a contextualized MAB solution, learning link preferences based on relative distances to satellites' neighbors. It employs tile coding and the UCB criterion for effective generalization over multiple contexts."

L200（机制）：
> "Using SKYLINK, each satellite autonomously decides which of its established links to prioritize for data transmission in order to minimize the average delay and drop rate in the network. SKYLINK is based on the MAB framework and uses the Upper Confidence Bound (UCB) criterion. The satellite uses the MAB framework to decide which links to use. It evaluates each option using the UCB criterion and selects its next action based on the updated evaluation."

L205（连续决策的处理）：
> "The decision (x_{(v,w),t} | w in O_{v,t}) of a satellite v represents the distribution of traffic across available links w in O_{v,t}. Unlike traditional MAB problems with discrete choices, this decision is continuous. SKYLINK addresses this by first creating a ranked list of preferences for the established links. Incoming traffic is then directed through the highest-ranked link on this list. Once its capacity is reached, additional traffic is routed through the next link in the ranking, and so forth."

上下文与 tile coding（L205 末、L207）：
> "We consider that each satellite uses the distances to its neighbors as context. As a result, instead of a single global context, the satellite observes a separate context (i.e., distance) for each link. ... Note however, that the considered context is continuous. Therefore, to maintain a low computational complexity and low learning time, we quantize it into discrete partitions using a tile coding mechanism [38]."
> "The satellite discretizes the distances to its neighbors into fixed-length intervals (e.g., 500 km segments; see Fig. 2), with a maximum distance defining the size of each partition. For every neighbor and for each context within these partitions, the satellite learns independently."

**上下文选择的实证依据（L288 逐字）**：
> "We based our implementation of SKYLINK on distances as contexts, because experiments showed that, among all tested features, per-link distance has the most direct and strongest influence on routing performance, outperforming any single alternative and all feature combinations. Beyond per-link distance, we evaluated local and UTC time, satellite load, neighbor distance, total path distance, and their combinations as contexts."

### 6.2 代价函数公式（逐字 LaTeX）

丢包率（L143，式 9）：
$$
\zeta _ { v , t } = 1 - \tilde { R } _ { v , t } ,\tag{9}
$$
传播时延（L151，式 10）：
$$
D _ { ( v , w ) , t } ^ { \mathrm { T x } } : = \frac { d _ { v , w , t } } { c } .\tag{10}
$$
排队时延（L161，式 11）：
$$
D _ { v , t } ^ { \ P } : = \left\{ \begin{array} { l l } { 0 } & { \mathrm { ~ i f ~ } \Delta _ { C } \leq 0 } \\ { \frac { Q _ { v } ^ { \operatorname* { m a x } } } { \sum _ { ( v , w ) \in O _ { v , t } } \operatorname* { m i n } \left( x _ { ( v , w ) , t } , C _ { ( v , w ) , t } \right) } } & { \mathrm { ~ i f ~ } \Delta _ { C } > 0 , } \end{array} \right.\tag{11}
$$
其中（L164）：Delta_C := R_{v,t}^{in} − sum_{(v,w) in O_{v,t}} min(x_{(v,w),t}, C_{(v,w),t})
路径时延（L169，式 12）：
$$
D _ { X } : = \operatorname* { m i n } \left( \sum _ { ( v , w ) \in X } D _ { ( v , w ) , t } ^ { \mathrm { T x } } + D _ { v , t } ^ { \mathrm { q } } , T _ { \operatorname* { m a x } } \right) .\tag{12}
$$
卫星级加权代价（L177，式 13）：
$$
c _ { v , t } = \frac { \sum _ { X \in \mathcal { X } _ { v , t } } R _ { X } D _ { X } } { \sum _ { X \in \mathcal { X } _ { v , t } } R _ { X } } ,\tag{13}
$$
全网平均代价（L183，式 14）：
$$
c _ { t } ( \mathbf { x } _ { t } ) = \frac { \sum _ { n \in \mathcal { N } } R _ { n , t } ^ { \mathrm { g } } c _ { n , t } } { \sum _ { n \in \mathcal { N } } R _ { n , t } ^ { \mathrm { g } } } .\tag{14}
$$
优化目标（L189，式 15）：
$$
\mathbf { x } _ { t } ^ { * } = \underset { \mathbf { x } _ { t } \in ( \mathbb { R } _ { + } ) ^ { \vert \boldsymbol { \varepsilon } _ { t } \vert } } { \arg \operatorname* { m i n } } c _ { t } ( \mathbf { x } _ { t } ) , \quad \forall t = 0 , . . . , T - 1\tag{15}
$$
**UCB 打分（成本型，注意减号偏置）**（L214，式 16）：
$$
\mathrm { U C B } _ { t } ^ { g } ( v , w ) = \bar { c } _ { v , w } ( g , d _ { ( v , w ) } ) - \sqrt { \frac { 2 \log ( t ) } { n ( v , w , g , d _ { ( v , w ) } ) } } .\tag{16}
$$
跨分区平均（L220，式 17）：
$$
\operatorname { U C B } _ { t } ( v , w ) = \frac { 1 } { | \mathcal { G } | } \sum _ { g \in \mathcal { G } } \operatorname { U C B } _ { t } ^ { g } ( v , w ) ,\tag{17}
$$
水填充分配（L244 式 18、L250 式 19）：
$$
x _ { ( v , w _ { j } ) , t } = \sigma C _ { j } , \quad j = 1 , . . . , i .\tag{18}
$$
$$
x _ { ( v , w _ { i + 1 } ) , t } = R _ { v , t } ^ { \mathrm { i n } } - \sum _ { j = 1 } ^ { i } \sigma C _ { j } .\tag{19}
$$
运行均值更新（Alg.1 line 19，L275）：
$$
\bar { c } v , w _ { 1 } ( g , d _ { ( v , w _ { 1 } ) } ) \gets \frac { { n \cdot \bar { c } _ { v , w _ { 1 } } ( g , d _ { ( v , w _ { 1 } ) } ) + c _ { v , t } } } { n + 1 }
$$

### 6.3 粒度与动作

- **决策粒度：每时隙 x 每颗卫星 x 每条出链路，分配连续流量 x_{(v,w),t} in R+**（式 15 的动作域 (R_+)^{|eps_t|}）。
- **动作被结构性拆成两半**（本批最重要的机制级观察之一）：
  - **学习部分**：链路**排序**（Alg.1 line 7：按 UCB 升序排序，成本越低越优先）；
  - **确定性部分**：给定排序后的**水填充流量分配**（Alg.1 lines 8–15，式 18/19），不学习。
  - L205 逐字佐证："> Unlike traditional MAB problems with discrete choices, this decision is continuous. SKYLINK addresses this by first creating a ranked list of preferences" —— **学习只作用于离散排序，连续分配用确定性规则**。
- 不确定性折减（L227 逐字）："> we include an uncertainty factor sigma < 1 when determining the link's capacity. By using sigma C_{(v,w),t}, SKYLINK ensures that the capacity of a link is not overestimated, which would result in higher drop rates."
- **每颗卫星同时独立执行**（L282 逐字）："Each of the satellites simultaneously executes this algorithm."
- 复杂度（L292 逐字）："> Overall, per satellite and time slot, the time complexity of SKYLINK is in O(k|G| + k log k). This makes the complexity independent of the number of satellites and users because k is bounded by visibility of ground stations rather than constellation size or demand."

### 6.4 是否含学习

**结论：含学习 —— contextual MAB + UCB，在线、每时隙更新、无中心训练。**

检索与实测（范围：该 MD 全文 506 行，grep -niE）：
- 模式 /reinforcement learning|Q-learning|DQN|deep Q-network/ → **10 命中**：L25（相关工作泛述）、**L321（对比基线：distributed Q-learning）**、L327 / L346 / L348 / L362 / L389（结果讨论，非算法核心）、**L433（参考文献 [14] "Shaping rewards, shaping routes: On multi-agent deep q-networks for routing in satellite constellation networks"）**、**L453（参考文献 [24] "Q-learning for distributed routing in LEO satellite constellations"）**、**L481（参考文献 [38] R. S. Sutton and A. G. Barto, Reinforcement Learning: An Introduction, 2nd ed. MIT Press, 2018）**。
  **重要交叉引用**：L433 的 [14] 与 L453 的 [24] 分别对应本选题 T1 批次表中的 5PYWVRC5 / L2VKYTAV（"Shaping Rewards, Shaping Routes"）与 Y2H4NPLU（"Q-learning for distributed routing in LEO satellite constellations"）。这是本批内**可验证的 T2 → T1 引用链**。
- 模式 /dueling|prioriti[sz]ed (experience )?replay|double (q|dqn|deep q)|actor(-| )critic|\bppo\b|\bsac\b|policy gradient/ → **0 命中**。
- **假阳性登记**：模式 /a3c|ddpg|td3/ 全库唯一命中落在本文 **L339**，核验为**图片文件名** "9d7c3d5e6c25e51480d85e1372bc4dda9711aeddba3cba11ebfe3956de352226.jpg"（".jpg" 前的哈希串中夹带 a3c 子串），**非文本内容**。
- 模式 /reward/ → **1 命中**（L433，即参考文献 [14] 标题中的 "Shaping rewards"）。本文自身用**成本（cost）**而非奖励，见式 16 的负号偏置。

**机制上的学习成分清单（逐条对应行号）**：
1. 上下文定义：每链路距离（L205、L288）；
2. 离散化：tile coding，固定长度区间（如 500 km）（L207）；
3. 统计量：平均成本 c_bar 与使用次数 n（L211）；
4. 选择规则：UCB（式 16/17，Alg.1 line 7）；
5. 更新规则：运行均值（Alg.1 line 19，L275）+ 计数（Alg.1 line 18/21，L274/L277）；
6. 收敛性依据（L205 末逐字）："> Under the assumption that the cost distribution is stationary in each context, our link selection algorithm inherits the convergence properties of the contextual UCB algorithm."

### 6.5 负载设置（实验条件登记）

TABLE II（L317）逐字要点：R = 100 次重复；N = 636 卫星（OneWeb）；M = 146 地面站（全球最大 146 城市）；T = 40320 时步；tau = 15 s；TTL T_max = 200 ms；起始 28.09.2023 08:26 UTC；**用户数 25.4M**；人均设备数 d = 0.003175；人均上传流量 nu = 22.98 kbps；GS 缓冲 Q_m^max = 1GB；卫星缓冲 Q_n^max = 50MB；GS→互联网容量 C_v = 50 Gbps；GS 到互联网时延 1–5 ms；ISL 带宽 B_ISL = 5 GHz；接收孔径 10 cm；ISL 发散角 1.744 x 10^-5 Rad；指向损耗 0.9；噪声温度 290 K；ISL 发射功率 0.1 W；上传比例 lambda = 0.08；GSL 带宽 250 MHz；EIRP 34.6 dbW；G_rx = 10.8 db；载频 f_c = 19 GHz；微波背景温度 275 K。

**负载纵向扫描（本批唯一做用户数扩展的）**（L327 逐字）："> we present the results of SKYLINK and the reference schemes for 12.7, 25.4, 63.5, and 127.0 million users respectively"。流量按当地时间逐小时调整（L315 逐字："The generated traffic per second varies depending on the local time. t_{n,t} is adjusted every hour, matching a characteristic daily pattern observed from [51]"）。

对比基线（L321 逐字）："> (i) a bent-pipe solution that sorts only the established GSLs randomly for its preference list (orange), (ii) a solution based on Dijkstra's algorithm that considers only the shortest path to the ground (gray), and (iii) a solution using not just the shortest, but the k-shortest paths to the ground [19], with k = 4 (green). (iv) A random solution that sorts the established links randomly to generate its preference list (blue), (v) A solution based on distributed Q-learning as proposed in [24] (beige)." 另有消融变体 NC-SKYLINK（去掉上下文与 tile coding，L323）。

### 6.6 可迁移点

1. **"学习只做排序、分配用确定性规则"的架构**（§6.3）：把连续动作空间拆成"学习的离散排序 + 确定性的解析分配"，兼顾收敛性与维度可控。**这是本批对 LEO RL 路由最直接可复用的架构建议**（式 16–17 学排序，式 18–19 只做水填充）。
2. **成本型 UCB（式 16 用减号）**：直接对"成本"做置信下界（而非对奖励做置信上界），与式 14 的代价函数天然衔接，**无需设计奖励函数**。对"必须先设计 reward"的默认假设构成直接反例。
3. **context = 单链路距离，且经实证筛选**（L288）：为"上下文该选什么"提供了可复现的消融结论（距离 > 时间 / 负载 / 路径距离及其组合）。注意这是**该文自己的实验结论**，不可不加限定地外推。
4. **sigma < 1 的容量保守估计**（L227）：把"容量不确定性"折进动作可行性以降低丢包，可迁移为 RL 中乐观初始化的反向技巧（悲观可行性）。
5. **分布式 + 局部信息下复杂度与星座规模无关**（L292）：O(k|G| + k log k)。这是 RL 路由可扩展性的强 baseline 指标。
6. **对 RL 的定量负面证据（L327 逐字）**："> For 12.7 million users, SKYLINK reduces the cost by 5.0% compared to k-shortest paths, 11.3% compared to NC-SKYLINK, 29.5% compared to the bent-pipe solution, 29.8% compared to distributed Q-learning, 54.4% compared to the random approach, and 84.6% compared to Dijkstra."
   → **contextual MAB 比 distributed Q-learning 低 29.8% 成本**。对"RL 优于轻量 bandit"的主张，这是一条必须正面回应的反例。
7. **消融的定量价值**：NC-SKYLINK（去上下文与 tile coding）差 11.3%，说明上下文机制贡献显著 —— 可作为 RL 中"状态设计是否值得"的对照量级。

---


## 7. JZA5SEQA — Fast Reroute Algorithms for Satellite Network with Segment Routing

**出处**：Xun Chen, Zhengjian Chen, Xiaolei Chang, Tian Ji, Zhenzhou Wu, Chenxi Li（深圳职业技术大学 / 深圳能源集团 / 清华大学 / 清华深研院），L3–L15。

### 7.1 决策机制

两套方案：(A) 集中式 SS-FFR —— 分段路由 + 中继卫星分为"计算卫星 / 转发卫星"两类；(B) 混合路由下的备份路径维护 BKM —— 下一跳机制 + DFS 搜索初始路径集 + 并集替换。摘要逐字（L17）：

> "we propose a hybrid FRR schemes for satellite networks that combines the centralized computing with distributed segment routing (SR). With the scheme, satellites with relatively more computing resources can pre-compute the reroute paths, and distribute the routing rules to satellites that have more forwarding resources. We formulate the problem, propose a classification algorithm that can distinguish satellites according to their computing and forwarding resources. Additionally, we also propose a real-time backup path maintenance algorithm in the hybrid rerouting scheme."

角色分工（L84 逐字）：

> "Under normal circumstances, the forwarding satellite is responsible for storing and delivering the forwarding path, and the computing satellite is responsible for collecting nearby link state information and calculating the path, exchanging data with the ground control center regularly, and updating the routing table for the forwarding satellite after any changes in the link state. When a protected link or node fails, the forwarding satellite can directly switch to the backup path and deliver the path, while the calculation satellite calculates a new backup path."

备份维护机制（L203 逐字）：

> "If the link state in the backup path changes, it is necessary to find a new backup path, which requires a lot of calculations. If the paths of all protected links need to be recalculated, it will consume a lot of satellite computing resources and take a lot of time. To address this issue, this paper proposes a BKM algorithm that makes realtime adjustments according to link state changes in backup paths without re-computation."

### 7.2 代价函数公式（逐字 LaTeX）

剩余平均正常工作时间（L104，式 1）：
$$
w o r k \_ t i m e _ { i } = a v g \_ a g e - a g e _ { i }\tag{1}
$$
中继卫星权重（L110，式 2）：
$$
\Delta _ { i } \mathrm { = } \alpha \times w o r k \_ t i m e _ { i } + \beta \times U D L _ { i }\tag{2}
$$
中继星对选择目标（L116，式 3）：
$$
m a x \frac { \Delta _ { f } + \Delta _ { r } + \mu \left( m e m _ { f } + m e m _ { r } \right) + \upsilon \left( c p u _ { f } + c p u _ { r } \right) } { \sqrt { \left( x _ { f } - x _ { r } \right) ^ { 2 } + \left( y _ { f } - y _ { r } \right) ^ { 2 } } } \ f ,\tag{3}
$$
域分配目标与约束（L122 式 4、L126 式 5、L130 式 6）：
$$
\operatorname* { m i n } { a v g \_ d i s _ { i } } \quad _ { i \in t }\tag{4}
$$
$$
\begin{array} { r l r } { s . t . } & { { } } & { m e m _ { i } > 0 } \end{array}
$$
$$
c p u _ { i } > 0\tag{5}
$$

符号表 TABLE I（L99）逐字要点：G(V,E,C) 卫星拓扑图；u 总轨道数；p 过极区轨道数；q 不过极区轨道数；k_i 轨道上卫星数；age_i 自上次故障以来的工作时间；avg_age 故障平均间隔；UDL_i 卫星 UDL 距离；Delta_i 候选卫星权重；cpu_i 可用计算资源；mem_i 可用存储资源；alpha 中继星在线时长权重；beta 中继星 UDL 距离权重；mu 转发星存储资源权重；lambda 转发星计算资源权重。

### 7.3 粒度与动作

- **本批中"决策粒度最粗"的一篇**：决策对象不是数据包、不是路由，而是 **① 节点的域划分**（Algorithm 1 DOD，把卫星分到 t 个域）与 **② 备份路径集合 B(e_{u,v}) 的维护**（Algorithm 2 BKM）。
- BKM 的动作序列（L213–L239）：给定故障链路 e_{u,v}，① 用备份路径替换初始路径（line 3–4：dp_{i,j} = bp_{i,j}；若 bp = 空则 dp = 空，表示 i 到 j 不可达）；② 从 B 中移除 B(e_{u,v})（line 7）；③ 对每个受影响备份路径，按下一跳原则重新搜索并做并集替换（line 13：bp_{i,j} = m 并 dp_{k,j}；line 16：bp_{s,d} = bp_{s,d} / path_{i,j} 并 bp_{i,j}）；若找不到则置空（line 17）。
- 复杂度（L159 逐字）："> Therefore, the time complexity of the DOD algorithm is O(len3+len2), which is still within the polynomial."（空间 O(len x t)）
- 域内用 DFS 修复（L247 逐字）："> The backup path can be repaired more efficiently by searching the initial path set I through DFS."

### 7.4 是否含学习

**结论：不含学习成分。**

检索与实测（范围：该 MD 全文 374 行，grep -niE）：
- 模式 /reinforcement learning|Q-learning|DQN|deep Q-network/ → **0 命中**。
- 模式 /dueling|prioriti[sz]ed (experience )?replay|double (q|dqn|deep q)|actor(-| )critic|\bppo\b|\bsac\b|policy gradient|a3c|ddpg|td3/ → **0 命中**（全库计数见 §12）。
- 模式 /MDP|Markov (decision|chain)/ → **0 命中**。
- 模式 /reward/ → **0 命中**。
- 模式 /neural network|deep learning|machine learning/ → **1 命中**：**L295**，为参考文献著录项（逐字片段："... Prathap, P. M. Mohan and M. Gurusamy, "Fast and Adaptive Failure Recovery using Machine Learning in Software Defined Networks," 2019 IEEE International Conference on Communicat..."）。**仅为参考文献，非本文方法。**

### 7.5 负载设置（实验条件登记）

- **第一组实验无流量模型**（L165 逐字）："> The experiment of this study is to run the DOD algorithm on several randomly generated discrete nodes and compare the results with those of the greedy algorithm (SDF) based on the average shortest distance and a local fast reroute (LFR)[33] algorithm with flow aggregation. ... nodes of different scales were randomly placed into 12 domains on a plane with a size of 100 units, each of the two algorithms was run 10 times for nodes of each scale and the mean averages of the results were taken."
  **必须区分**：此处的"高负载"（L191 逐字 "This study includes high load performance comparison experiment that uses 500 random discrete nodes to compare the performance of the three algorithms in various aspects"）指的是**节点数多**，不是流量负载。**勿当作流量负载实验引用。**
- 第二组（L258 逐字）："> we conducted experiments using the Teledisic satellite constellation on the NS2 simulator. The constellation used in the experiment has 12 planes, and each plane has 24 low-Earth orbit satellites, one of which is an independent routing calculation satellite, and all data in the plane are forwarded through this satellite. In the experiment of this study, the capacity of the ISL is 155 Mb, the ISL between planes is turned on or off according to the direction of satellite movement, and the simulation time equals the orbit cycle (6794 seconds). To test the performance of the BKM algorithm in dealing with link failures, randomly generated failed links of gradually increasing numbers were deployed to the corresponding planes, and the average delay was calculated by sending a data packet every 30s."
  → 负载 = 每 30 秒发一个数据包；故障链路数逐步增加。
- 结果量级（摘要 L17 逐字）："> the results show that under extreme conditions, the proposed LFR algorithm is 30.9% better than traditional algorithms in storage resource utilization; and the proposed LFA+ algorithm is 74.3% better than traditional algorithms in update time comparison."

### 7.6 可迁移点

1. **失败事件的"预置备份 + 实时维护"两阶段分离**：把 RL 的在线动作从"重新计算路径"降级为"在预置备份路径集合中挑选 / 替换"，可将在线决策空间压到常数级，对应 RL 中的 **action set pre-computation**。
2. **备份路径的级联失效处理**（Alg.2 line 16 的并集替换）：一个失败事件会同时使多条备份路径失效，需要级联更新。这直接对应 RL 中"一次动作改变导致其他动作价值失效"的问题（动作价值的非平稳性），可作为动作价值失效检测的工程对照。
3. **可靠性权重 work_time = avg_age − age**（式 1–2）：把节点的"剩余期望寿命"作为选择权重，可迁移为 RL 状态特征或奖励的可靠性项。
4. **资源异质性作为约束**（式 3、式 5）：把计算 / 存储资源显式分为两类并各自加权，可迁移为多智能体 RL 中不同 agent 的能力约束（异构动作空间）。
5. **自述局限（L265 逐字）—— 可作负面证据引用**："> The experimental results show that the BKM algorithm can help accelerate the update of some backup paths, but its implementation is more complicated, and the availability and length of the backup paths are affected by the implementation method." 即：下一跳式备份修复会**牺牲路径长度**（L258 亦指出 BKM 与 LFA+ 的备份路径比 Dijkstra 长）。

---

## 8. TRM2HPFN — A Dynamic Routing Concept for ATM-Based Satellite Personal Communication Networks (DT-DVTR)

**出处**：M. Werner，IEEE JSAC 1997。本 MD 的 L1 为标题；版本信息由同批 DVS8C3CC 的参考文献 [35] 佐证（L549 逐字："M. Werner, "A Dynamic Routing Concept for ATM-based Satellite Personal Communication Networks," IEEE Journal on Selected Areas in Communications, vol. 15(8), pp. 1636–1648, Oct. 1997."）。

### 8.1 决策机制

**离散时间虚拟拓扑 + 路径序列优化**。这是本批（也是该领域）的**方法论源头**之一。

L131 逐字（网络模型与快照）：
> "the proposed routing concept is based on a discrete-time topology approach as illustrated in Fig. 5. The dynamic network topology is considered as a periodically repeating series of topology snapshots separated by step width Delta t = T/K. Each of the snapshots at t = k Delta t, k = {0, ..., K-1}, is modeled as a graph G(k) = (V, E(k)), where V = {1, ..., N} is the constant set of nodes and E(k) represents the set of undirected links (i,j)_k = (j,i)_k between neighboring nodes and j, existing at t = k Delta t. Associated with each link are its costs c_ij(k) according to an appropriate cost metric."

L150 逐字（路径集构造）：
> "The assignment procedure reflects the setup of an instantaneous virtual topology VT(k) upon G(k) covered by module I-VTS( ) in Fig. 6. This task is performed by an iterative -best path search algorithm for every OD pair. The single shortest path search task can be formulated as finding the least cost path p(k), i.e., the path with minimum path cost C_{p(k)} = Sigma_{i,j} c_ij(k) delta^{p(k)}_{(i,j)_k}. We suggest an iterative approach based on successive calls of the Dijkstra shortest path algorithm (DSPA) [11] because this allows us to introduce topology modifications in between. For instance, by "eliminating" already occupied links, one can force a set of disjoint paths, thus providing a base for simple and robust fault recovery mechanisms and building a sound framework for network traffic flow shaping at operation time."

L157 逐字（真正动态的部分 —— 路径序列选择 DT-PSS）：
> "It is obvious that a connection-oriented routing strategy adapted to such topology dynamics must also solve the problem of selecting for all OD pairs (virtual) path sequences over successive time intervals from the virtual topology provided by DT-VTS; this is the point where really dynamic routing is achieved, instead of independently solving a series of quasistatic routing tasks and then "living with" the consequences coming in due to path handover (instantaneous path delay offset, handover signaling complexity, etc.). DT-PSS is essentially performed for all OD pairs as a path continuity optimization procedure, where immediately promising variants are: 1) minimizing HO delay jitter (i.e., instantaneous delay offsets during path handover), and 2) minimizing path HO rate, with some restrictions also 3) minimizing (average) delay."

### 8.2 代价函数公式（逐字）

链路代价单调变化条件（L140，MD 中为行内公式）：
> (c_ij((k+1) Delta t - 0) - c_ij(k Delta t)) / c_ij(k Delta t) << 1, for all (i,j)_k in E(k)

链路占用指示与路径代价（L148 逐字）：
> "A link occupation indicator delta^{p(k)}_{(i,j)_k} = 1 shows that (i,j)_k belongs to path p(k); otherwise, delta^{p(k)}_{(i,j)_k} = 0"
> "... finding the least cost path p(k), i.e., the path with minimum path cost C_{p(k)} = Sigma_{i,j} c_ij(k) delta^{p(k)}_{(i,j)_k}"

整周期最优路径序列（L162 逐字）：
> "The optimization is performed over the complete period T, then achieving an optimal network solution. The result is one unique first-choice path sequence S_{T,1} = {p_1(0), p_1(1), ..., p_1(K-1)} out of m^K possible ones, with p_1(k) in P_w(k), or a set of Q ordered (i.e., prioritized: first-choice, second-choice, ) sequences of such kind, S_{T,q} = {p_q(0), p_q(1), ..., p_q(K-1)}, q = {1, ..., Q}"

滑动窗口最优（L167 逐字）：
> "The optimization is performed in a time-distributed manner within a sliding window of discrete-time duration tau, i.e., extending over the interval [k Delta t, (k+tau) Delta t[ (modulo ), k = {0, ..., K-1}, tau in {2, ..., K-1}. The results are - unique first-choice path sequences S_{tau,1}(k) = {p_1(k), p_1(k+1), ..., p_1(k+tau-1)} (modulo ), for all k in {0, ..., K-1} respectively, sets of ordered sequences, S_{tau,q} = {p_q(k), p_q(k+1), ..., p_q(k+tau-1)}, q = {1, ..., Q}"

每链路 VP 占用数（L187 逐字）：
> v_ij(k) = Sigma_{w in W} delta^{p_1(k)}_{(i,j)_k}, for all (i,j) in E, for all k in {0, ..., K-1}

滑动窗口目标函数（L202 逐字）：
> "The latter is in essence a weighted sum of maximum and average delay jitter. In this way, optimal tracks through the "landscape" of alternative VPC's are selected."

### 8.3 粒度与动作

- **决策粒度：OD 对 x 时隙 → 选择整条路径**，并组织为"路径序列"。动作语义 = "这一时段用哪条 VPC，下一时段切到哪条 VPC"。
- 两级分组（L177 逐字）："> All end-to-end VCC's sharing the same first and last satellites at arbitrary time can simply be aggregated in one common VPC across the ISL subnetwork, the latter being a unique concatenation of VP's on the single ISL's of the VPC."
- 执行层（L179 逐字）："> Every transit satellite provides—on the basis of locally available switching tables—pure VP switching functionality between every pair of ISL ports, and thus the whole space segment becomes a pure fast operating cross-connect network."
- **VPI 容量硬上界**（L183 逐字）："> The ATM cell header contains 12 bits in the virtual path identifier (VPI) field, thus allowing a maximum of 2^12 = 4096 VP's on a single ISL per step."；仿真实测（L190 逐字）："> counting VP's per link in computer simulations yields a maximum of roughly 400 VP's on such links that are in equatorial regions and just in the middle between the seam "boarders""。
- **算法离线**（L155 逐字）："> Performing I-VTS( ) for all k = {0, ..., K-1} completes the discrete-time virtual topology setup DT-VTS. The dynamic virtual topology given as result of the completely off-line DT-VTS procedure may be used for on-line traffic adaptive routing strategies as indicated in the figure, i.e., traffic adaptive routing can be performed within the limits of the given virtual topology."

### 8.4 是否含学习

**结论：不含学习成分（1997 年论文，纯组合优化 + 仿真）**。

检索与实测（范围：该 MD 全文 275 行，grep -niE）：
- 模式 /reinforcement learning|Q-learning|DQN|deep Q-network/ → **0 命中**。
- 模式 /dueling|prioriti[sz]ed (experience )?replay|double (q|dqn|deep q)|actor(-| )critic|\bppo\b|\bsac\b|policy gradient|a3c|ddpg|td3/ → **0 命中**。
- 模式 /MDP|Markov (decision|chain)/ → **0 命中**。
- 模式 /reward/ → **0 命中**。
- 模式 /neural network|deep learning|machine learning/ → **0 命中**。

### 8.5 负载设置（实验条件登记）

- **本文无流量 / 拥塞负载模型**。L125 逐字给出唯二的业务假设："> The primary services to be provided are delay sensitive (e.g., telephony, video), and thus require clear priority for the QoS parameters delay and delay jitter; this is reflected in the link cost functions, and thereby drives path search."；另两条基线假设 L127："> Information flows of a single end-to-end connection always use the same path in both directions."、L129："> The system should inherently provide a straightforward and robust scheme to cope with path failures, i.e., disjoint backup paths are desired."
- 仿真呼叫模型（L219 逐字）："> It provides the distribution of VPC handover delay jitter for typical telephone service, i.e., showing a negative exponentially distributed call holding time with mean T = 3 min. The length of the sliding window for HO delay jitter minimization has been 5 min. Note that the shown distribution is conditional, normalizing with respect to the total number of encountered handover situations. With the given simulation parameters, in fact, only fewer than 20% of the calls are affected by a handover at all."
- 定长呼叫对照组（L219 逐字）："> The simulated calls are equally distributed over time and all possible first/last satellite pairs. Considering such 2 min fixedlength calls is, of course, not close to reality, but it is the only way to make a fair (and at least basic) comparison of both approaches with a discrete-time interval Delta t = 1 min."
- 星座：Iridium，N = 66（L188 逐字："equivalent to the number of terminating satellite pairs (= 2145 for Iridium, N = 66)"）。

### 8.6 可迁移点

1. **"准静态逐时隙重算"与"路径序列优化"的区分（L157）是本批最重要的方法论警示**：
   > "this is the point where really dynamic routing is achieved, instead of independently solving a series of quasistatic routing tasks and then "living with" the consequences coming in due to path handover"
   → 对 RL 的直接含义：**在每时隙独立做最优决策，并不等于做了跨时隙的动态优化**。若 RL 把时间折扣设得过短、或把每步当独立 MDP，就会退化成本文所称的 "quasistatic" 情形。这是一条可反驳"我的 RL 是动态路由"主张的判据。
2. **切换代价的双目标形式（L157）**：minimizing HO delay jitter vs minimizing path HO rate —— 把"切换的瞬时抖动"与"切换的频率"作为**两个不同目标**。这是本批中对 G-A 最接近的**目标类型分解**（但仍非失败原因分解，详见 §13）。
3. **滑动窗口 vs 整周期的权衡（L200–L202）**：整周期最小化 HO 率 → 全局最优但所有连接共用一条 VPC 轨迹；滑动窗口最小化抖动 → 更贴合短连接但 VPI 消耗随窗口线性增长（L202 逐字："the average number of VPI's required per link grows proportionally with the sliding window size"）。**这是"决策视野长度"与"资源开销"之间的显式权衡**，可迁移为 RL 中 episode 长度 / 决策频率的选择依据。
4. **离线预计算 + 在线自适应（L155）**：DT-VTS 离线算好，在线只在虚拟拓扑内做流量自适应路由。对应 RL 中的 **offline policy pretraining + online adaptation** 两段式结构。
5. **可行性硬上界（VPI <= 4096，L183）**：把执行层物理资源上限直接作为设计约束，可作为 RL 动作空间上界的构造依据。
6. **被同批 T2 论文引用**：DVS8C3CC 的参考文献 [35]（L549）即本文。**"被 RL 论文采用"在本批范围内无证据，不做主张。**

---

## 9. XM6NUPM4 — Your Mega-Constellations Can Be Slim: A Cost-Effective Approach for Constructing Survivable and Performant LEO Satellite Networks (MEGAREDUCE)

**出处**：L1 标题；作者含 Hewu Li（L362 逐字："Hewu Li is the corresponding author"）；代码公开于 github.com/SpaceNetLab/MegaReduce（L362）。

### 9.1 决策机制

**需求驱动的星座规模收缩：多项式可行性判定 + Shrink/Expand 迭代搜索**。L177 逐字：

> "MEGAREDUCE exploits a basic idea that: while it is difficult to directly solve the SPLD problem and obtain the optimal solution, it is doable to determine whether a given LSN is feasible to meet survivability and performance requirements in polynomial time. Specifically, MEGAREDUCE starts with an initial constellation state, then repeatedly tunes the constellation structure as well as the number of satellites in multiple rounds of iterations, and searches the feasible LSN design with the minimum number of satellites."

四步（L184–L190 逐字）：① Constellation initialization；② Feasibility checking；③ Constellation tuning（feasible → Shrink，否则 Expand）；④ Solution search（取卫星数最少者）。

搜索范围下界（L196 逐字）：

> "We calculate the initial N_min by exploiting a key insight that: to guarantee at least r_ij disjoint paths for communication pair between cell i and j, there should be at least r_ij visible satellites for i and j. Hence, the initial N_min is calculated as the minimum number of satellites that ensures each cell i has at least max{r_ij}, for all j in C satellites in their transmission range during the service hours."

可行性判定核心为 **CalculateMaxFlow**（Alg.2 line 11，L238），判据（L249 逐字）："> The LSN graph can meet the survivability requirement only if the maximum number of flows from src(d) to dst(d) is at least r_{src(d),dst(d)}."

### 9.2 代价函数公式（逐字 LaTeX）

SPLD 目标（L84 逐字）：Objective: min Sigma_{i in S} x(i)

$$
I _ { i j } ^ { t } \ge e _ { i j } ^ { t } , \forall i , j \in { \mathcal { S } } \cup { \mathcal { C } } , i \neq j , \forall t \in T ,\tag{1}
$$
$$
{ \boldsymbol { x } } ( i ) \cdot { \boldsymbol { x } } ( j ) \geq e _ { i j } ^ { t } , \forall i , j \in { \mathcal { S } } \cup { \mathcal { C } } , i \neq j , \forall t \in T ,\tag{2}
$$
$$
\sum _ { j \in \cal S } e _ { i j } ^ { t } \le N _ { I S L } , \forall i \in \cal S , i \neq j , \forall t \in \cal T ,\tag{3}
$$
$$
\sum _ { \forall d : \operatorname { s r c } ( d ) = j } \operatorname { s i z e } ( d ) \leq \sum _ { i \in \mathcal { S } } e _ { j i } ^ { t } \cdot C a p _ { j i } ^ { t } , \forall j \in \mathcal { C } , \forall t \in T ,\tag{4}
$$
$$
\sum _ { \forall d : \operatorname { d s t } ( d ) = j } \operatorname { s i z e } ( d ) \leq \sum _ { i \in \mathcal { S } } e _ { i j } ^ { t } \cdot C a p _ { i j } ^ { t } , \forall j \in \mathcal { C } , \forall t \in T ,\tag{5}
$$
$$
\sum _ { j \in \mathcal { C } } \boldsymbol { e } _ { j i } ^ { t } \cdot C a p _ { j i } ^ { t } \le C a p _ { u p } ^ { m a x } , \forall i \in \mathcal { S } , \forall t \in T ,\tag{6}
$$
$$
\sum _ { j \in \mathcal { C } } \boldsymbol { e } _ { i j } ^ { t } \cdot C a p _ { i j } ^ { t } \le C a p _ { d o w n } ^ { m a x } , \forall i \in \mathcal { S } , \forall t \in T ,\tag{7}
$$
$$
\sum _ { ( i , j ) \in \sigma ( \overline { { V } } ) } e _ { i j } ^ { t } \geq \mathbf { m a x } _ { \forall p \in V - \overline { { V } } , \forall q \in \overline { { V } } } \ r _ { p q } , \forall \overline { V } \subset V , \overline { V } \neq \emptyset .\tag{8}
$$
延迟约束扩展（L146 式 9、L154 式 10、L158 式 11、L162 式 12）：
$$
\begin{array} { r l } & { \qquad \displaystyle \sum _ { \forall j : ( j , i , l - 1 ) \in E _ { t } ^ { d } } \omega _ { j i } ^ { ( l - 1 ) d } - \sum _ { \forall j : ( i , j , l ) \in E _ { t } ^ { d } } \omega _ { i j } ^ { l d } } \\ & { \qquad = \left\{ \begin{array} { l l } { - r _ { d } , } & { i f \quad i = \mathrm { s r c } ( d ) } \\ { r _ { d } , } & { i f \quad i = \mathrm { d s t } ( d ) _ { l } , } \\ { 0 , } & { o t h e r w i s e } \end{array} \right. } \end{array}\tag{9}
$$
$$
\omega _ { i j } ^ { l d } + \omega _ { j i } ^ { ( l + 1 ) d } \leq 1 , \forall ( i , j ) \in E _ { t } , d \in \mathcal { D } , t \in T ,\tag{10}
$$
$$
\sum _ { l \in \{ 2 , \dots , L _ { d } \} } \omega _ { i j } ^ { l d } \leq x ( i ) , \forall ( i , j ) \in E _ { t } , d \in \mathcal { D } , i \in \mathcal { S } , t \in T ,\tag{11}
$$
时延门限设定（L128 逐字）："> Assume the path length of demand d associated with i and j is expected to be lower than L_d (or denoted by L_ij). Inspired by [41], the value of L_d can be set to ceil(lambda * L_ij^{sp}) where L_ij^{sp} is the shortest path length between i and j, and lambda >= 1 is a constraint factor."

### 9.3 粒度与动作

- **决策粒度：星座级** —— 动作是二值向量 x(i) in {0,1}，表示"第 i 颗卫星是否被纳入子图"（L82 逐字："> we define x(i) as a binary variable indicating whether a satellite i in S is included or not in the sub-graph"）。
- 外层搜索是 **Shrink/Expand 迭代**（Alg.1，L202–L216）；每次由"可行性检查（多项式）"决定方向，最终取卫星数最少者（Alg.1 line 15：G <- argmin_{for all G in G_list^result}(|G.O * G.M|)）。
- **本文不决定路由**：路由只作为可行性检查里的**流**出现（分层图最大流 r_d，式 9；容量式 12）。"路由"是约束的载体，不是决策对象。
- 复杂度动机（L171 逐字）："> Even if we set all r to 1, the SPLD problem in a single time slot can be converted to the classic Steiner Tree Problem which is known to be NP-hard. Our preliminary results show that the problem becomes intractable to solve even for moderately-sized instances with hundreds of satellites. Hence solving the SPLD problem requires the development of more efficient methods to obtain feasible solutions."

### 9.4 是否含学习

**结论：不含学习成分。**

检索与实测（范围：该 MD 全文 465 行。**注意：该文件被 grep 判定为 binary（含非 UTF-8 字节），故必须用 grep -a 才得到真实计数；不加 -a 会误报 "binary file matches" 而无数字**）：
- 模式 /reinforcement learning|Q-learning|DQN|deep Q-network/（grep -aniE）→ **1 命中**：**L430**（参考文献 [34] "Yang Cao, Shao-Yu Lien, and Ying-Chang Liang. Multi-tier collaborative deep reinforcement learning for non-terrestrial network empowered vehicular connections..."）。**仅为参考文献著录，非本文方法。**
- 模式 /dueling|prioriti[sz]ed (experience )?replay|double (q|dqn|deep q)|actor(-| )critic|\bppo\b|\bsac\b|policy gradient|a3c|ddpg|td3/ → **0 命中**。
- 模式 /MDP|Markov (decision|chain)/ → **0 命中**。
- 模式 /reward/ → **0 命中**。
- 模式 /neural network|deep learning|machine learning/ → **0 命中**。
- **假阳性登记**：模式 /train(ing|ed)?/ 在该文 **20 命中**，核验为 **"transmission" 等词的子串误命中**（"transmission range" 含 "train"）—— 本批第四类陷阱。

### 9.5 负载设置（实验条件登记）

- 仿真器（L284 逐字）："> we evaluate MEGAREDUCE by LSN simulation. To build a trace-driven simulation environment, we collect constellation information from the public regulatory documents [43], [44], and extend StarPerf [45], a state-of-the-art LSN simulator which can mimic the LEO dynamics and network behaviors of an LSN. Specifically, we extend StarPerf with the ability of flexibly tuning the constellation structure as well as the ability for survivability assessment."
- 容量参数（L284 逐字）："> we follow a recent study [47] to set the capacity of each laser ISL to 20Gbps, set the capacity of each shared GSL to 4Gbps, and set N_ISL = 4 in our experiment. For each experiment in this section, we simulate a complete regression period for the evaluated constellation."
- 求解器（L284 逐字）："> we implement our MEGAREDUCE optimizer based on two open libraries: Gurobi [48] and SkyField [49], which is an astronomy package for high precision research-grade orbit analysis and trajectory calculation."
- **流量需求生成（L286 逐字）**："> We combine Starlink's availability map [50] and a recent population-based traffic model used in [11] to generate the LSN traffic demand matrix in our experiments. Specifically, we generate the traffic demand for each terrestrial cell where satellite service is ready based on the availability map, and the traffic volume is set proportional to its population size which can be obtained from [51]."
- 测试星座（L290 逐字）："> we use the first phase of Starlink (4408 LEO satellites in 5 orbital shells with the altitudes between 540 km and 570 km) and Kuiper (3236 satellites in total) as the initial constellation configuration."
- 生存性参数扫描（L306 逐字）："> Even in the case of r_min = 6, MEGAREDUCE can reduce 20.05% and 21.88% of the total number of required satellites for Starlink and Kuiper respectively."

### 9.6 可迁移点

1. **"直接优化 NP-hard 目标"改为"多项式可行性判定 + 迭代搜索"**（L177）：本批中**最强的算法结构迁移点**。对 RL 而言，若约束可行性可高效判定，则可用可行性驱动的搜索替代直接优化，避免在巨大离散动作空间上的低效探索。
2. **约束 (8) 的 min-cut 写法**（L117 逐字）："> This constraint ensures that the value of a minimum cut separating p and q is at least r_pq, implying that there are at least r_pq edge-disjoint paths between the pair (p, q)." —— 把"冗余路径数"编码为最小割下界，可直接用作 RL 的硬约束或可行性 mask。
3. **分层图把时延约束转成跳数约束**（L128–L139）：节点复制 L_d+1 层，层间边代表一跳（L139 逐字："> By this transformation, we guarantee that any path from src to dst satisfies the L-hop constraint (L=5)"）。可迁移为 RL 状态增广（把剩余跳数预算放进状态）。
4. **需求驱动的"收缩"而非"扩张"视角**：与所有其他论文（都在给定星座上做路由）相反，本文问"最少需要多少卫星"。对选题的意义：可反驳"必须用大规模星座"的隐含前提。
5. **公开可复现代码**（L362）：github.com/SpaceNetLab/MegaReduce —— 本批中唯一明确给出公开代码仓库的论文，可作为平台对照实现的候选。

---


## 10. WHS8Z44C — Joint Network Function Placement and Routing Optimization in Dynamic Software-defined Satellite-Terrestrial Integrated Networks (BDBC + TEDG)

**出处**：Shuo Yuan, Yaohua Sun, Mugen Peng，L3。

### 10.1 决策机制

**联合 VNF 放置与路由规划，用时间演化图（TEG）建模**；最优解用 Benders 分解 + 分支切割（BDBC），实用解用时间扩展解耦贪心（TEDG）。摘要逐字（L5）：

> "we study service provisioning in SDSTNs via joint optimization of virtual network function (VNF) placement and routing planning with network dynamics characterized by a time-evolving graph. Aiming at minimizing average service latency, the corresponding problem is formulated as an integer nonlinear programming under resource, VNF deployment, and time-slotted flow constraints. Since exhaustive search is intractable, we transform the primary problem into an integer linear programming by involving auxiliary variables and then propose a Benders decomposition based branch-and-cut (BDBC) algorithm. Towards practical use, a time expansion-based decoupled greedy (TEDG) algorithm is further designed with rigorous complexity analysis."

TEDG 的解耦（L524 逐字）：

> "Note that Algorithm 2 decouples routing planning and VNF placement into two stages, where lines 13-18 generate potential service flow paths, and lines 19-24 perform VNF placement. For the path search, the TEG needs to be converted into an adjacency matrix without losing the dynamic characteristics of network topology under resource constraints."

Benders 分解的关键论证（L440 逐字）："> Since the objective of P2 is independent of the variables of the subproblem, it implies that the subproblem aims to find a feasible VNF placement on a given routing path. Therefore, we can take the average VNF placement load at network nodes as the objective to generate the feasibility cuts, which does not affect the optimality of the solution to P2."

### 10.2 代价函数公式（逐字 LaTeX）

通信时延（L123，式 8）：
$$
T _ { n m } ^ { q , l _ { i } , t } = \delta _ { q } \sum _ { q \in \mathcal { Q } } \sum _ { i \in \mathcal { I } _ { q } \setminus I _ { q } } y _ { n m } ^ { q , i , t } / R _ { n m } ^ { t } + \frac { d _ { n m } ^ { t } } { v } .\tag{8}
$$
计算时延（L131 式 9、L137 式 10）：
$$
T _ { n } ^ { q , i } = \delta _ { q } \varepsilon / c _ { q } ,\tag{9}
$$
$$
T _ { n } ^ { q } = \sum _ { i \in \mathcal { I } _ { q } } T _ { n } ^ { q , i } x _ { n } ^ { q , i } .\tag{10}
$$
时延约束（L145 式 11、L151 式 12）：
$$
T _ { n m } ^ { q , l _ { i } , t } y _ { n m } ^ { q , i , t } \leq \tau , \forall i \in \mathcal { I } _ { q } \backslash I _ { q } , q \in \mathcal { Q } , n m \in \mathcal { L } _ { c } , t \in \mathcal { T } .\tag{11}
$$
$$
T _ { n } ^ { q } \le \sum _ { i \in \mathcal { I } _ { q } \setminus I _ { q } } \sum _ { t \in \mathcal { T } } y _ { n n } ^ { q , i , t } \tau , \forall q \in \mathcal { Q } , n \in \mathcal { N } ,\tag{12}
$$
VNF 放置约束（L159 式 13、L165 式 14）：
$$
\sum _ { n \in { \cal N } } x _ { n } ^ { q , i } = 1 , \forall i \in { \cal T } _ { q } , q \in { \cal Q } .\tag{13}
$$
$$
x _ { s _ { q } } ^ { q , 1 } = 1 , x _ { e _ { q } } ^ { q , I _ { q } } = 1 , \forall q \in \mathcal { Q } .\tag{14}
$$
流守恒（L171 式 15、L177 式 16、L183 式 17、L195 式 18a、L229 式 18e）：
$$
\sum _ { n \in \mathcal { N } } y _ { s _ { q } n } ^ { q , 1 , 1 } = 1 , \forall q \in \mathcal { Q } .\tag{15}
$$
$$
x _ { n } ^ { q , i } \leq \sum _ { t \in \mathcal { T } } y _ { n n } ^ { q , i , t } , \forall q \in \mathcal { Q } , n \in \mathcal { N } , i \in \mathcal { T } _ { q } \backslash \{ 1 , I _ { q } \} .\tag{16}
$$
$$
\begin{array} { r } { \displaystyle \sum _ { n m \in \mathcal { L } _ { c } } \displaystyle \sum _ { i \in \mathcal { T } _ { q } \setminus I _ { q } } y _ { n m } ^ { q , i , t } + \displaystyle \sum _ { n n \in \mathcal { L } _ { s } } \mathbb { I } ( \displaystyle \sum _ { \substack { i \in \mathcal { T } _ { q } \setminus I _ { q } } } y _ { n n } ^ { q , i , t } \geq 1 ) \leq 1 , } \\ { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \forall q \in \mathcal { Q } , t \in \mathcal { T } , } \end{array}\tag{17}
$$
$$
\begin{array} { r } { \displaystyle { \sum _ { m \in { \cal N } } y _ { m n } ^ { q , i , t } = \sum _ { m \in { \cal N } } \big ( y _ { n m } ^ { q , i + 1 , t } + y _ { n m } ^ { q , i + 1 , t + 1 } + y _ { n m } ^ { q , i , t + 1 } \big ) } , } \\ { \forall t < t _ { q } , i < I _ { q } - 1 , q \in { \mathcal { Q } } , n \in { \cal N } . } \end{array}\tag{18a}
$$
资源与可用性约束（L235 式 19、L241 式 20）：
$$
\mathbb { I } ( \sum _ { q \in \mathcal { Q } } \sum _ { i \in \mathcal { Z } _ { q } \setminus I _ { q } } y _ { n m } ^ { q , i , t } \geq 1 ) \leq \varphi _ { n m } ^ { t } , \forall n m \in \mathcal { L } , t \in \mathcal { T } .\tag{19}
$$
$$
\sum _ { q \in \mathcal { Q } } \sum _ { i \in \mathcal { Z } _ { q } \setminus I _ { q } } x _ { n } ^ { q , i } ( \beta _ { i } ^ { q } + y _ { n n } ^ { q , i , t } c _ { q } ) \leq C _ { n } , \forall n \in \mathcal { N } , t \in \mathcal { T } ,\tag{20}
$$
**端到端时延 = 占用时隙数 x tau**（L249，式 21）：
$$
T _ { e 2 e } ^ { q } = \tau \sum _ { t \in \mathcal { T } } \mathbb { I } ( \sum _ { i \in \mathcal { Z } _ { q } \setminus I _ { q } } \sum _ { n m \in \mathcal { L } } y _ { n m } ^ { q , i , t } \geq 1 ) , \forall q \in \mathcal { Q } .\tag{21}
$$
**主问题 P1**（L255，式 22）：
$$
\quad ( { \mathrm { P 1 } } ) : \quad \operatorname* { m i n } _ { \mathbf { x } , \mathbf { y } } \quad { \frac { 1 } { Q } } \sum _ { q \in { \mathcal { Q } } } T _ { e 2 e } ^ { q }\tag{22}
$$
Benders 分解后的 MP / RSP（L443 式 42、L449 式 43）：
$$
\begin{array} { r c l } { { \displaystyle ( \mathrm { MP } ) : } } & { { \displaystyle \operatorname* { min } _ { \mathcal Z ^ { \prime } } } } & { { \displaystyle \frac { 1 } { Q } \sum _ { q \in { \mathcal Q } } T _ { e 2 e } ^ { q } } } \\ { { } } & { { \mathrm { s . t . } } } & { { \displaystyle ( 1 5 ) , ( 2 4 ) , ( 2 6 ) - ( 2 9 ) , ( 3 1 ) , } } \\ { { } } & { { } } & { { \displaystyle ( 3 3 ) , ( 3 4 ) , ( 3 8 ) , } } \end{array}\tag{42}
$$
$$
\begin{array} { r l } { ( \mathrm { R S P } ) : \underset { \mathbf { x } } { \mathrm { m i n } } } & { \displaystyle \sum _ { n \in \cal N } \frac { 1 } { C _ { n } } ( \sum _ { q \in \cal Q } \displaystyle \sum _ { i \in I _ { q } } x _ { n } ^ { q , i } \beta _ { q } ^ { i } ) } \\ { \mathrm { s . t . ~ } } & { ( 1 2 ) , ( 1 3 ) , ( 1 6 ) , ( 2 0 ) , } \\ & { 0 \leq x _ { n } ^ { q , i } \leq 1 , \forall q \in \mathcal { Q } , i \in \mathcal { I } _ { q } , n \in \mathcal { N } . } \end{array}\tag{43}
$$

### 10.3 粒度与动作

- **双粒度决策**：① VNF 放置 x_n^{q,i} in {0,1}（第 q 个服务的第 i 个 VNF 是否放在节点 n）；② 路由 y_{nm}^{q,i,t} in {0,1}（第 q 个服务的第 i 条虚拟链路是否在时隙 t 通过物理链路 nm）。
- **"stay link" 机制**（L181 逐字）：当服务路径走 stay link（nn）时，同一时隙内可部署多个连续 VNF 并在一个时隙内完成处理（L181 逐字："> On the other hand, when the service path traverses a stay link, the potential arises for deploying multiple consecutive VNFs on a single node and accomplishing their processing within a single time slot, which means Sigma_{i in I_q \ I_q} y_{nn}^{q,i,t} >= 1"）。**这等价于 RL 中的"原地动作 / 一次动作完成多步处理"**，且式 17 保证两种情形互斥（和 <= 1）。
- 服务的端到端时延被定义为"占用的时隙数 x tau"（式 21）—— **连续时延被离散化为整数时隙计数**。
- 复杂度（L652 逐字）："> Therefore, the overall complexity of the proposed TEDG algorithm is O(Q Sigma_{t=1}^{T}(tN^2 + ktN^2 + k(tN+N) log(tN+N) + k I_q (t-1))) ~= O(Q T N^2 (1+k)(1+T) / 2)"。

### 10.4 是否含学习

**结论：不含学习成分（整数规划 + Benders 分解 + 贪心启发式）**。

检索与实测（范围：该 MD 全文 805 行，grep -niE）：
- 模式 /reinforcement learning|Q-learning|DQN|deep Q-network/ → **1 命中**：**L752**，即参考文献 [14]（逐字："C. Qiu, H. Yao, F. R. Yu, F. Xu, and C. Zhao, "Deep Q-learning aided networking, caching, and computing resources allocation in software-defined satellite-terrestrial net..."）。**仅为参考文献著录。**
- 模式 /dueling|prioriti[sz]ed (experience )?replay|double (q|dqn|deep q)|actor(-| )critic|\bppo\b|\bsac\b|policy gradient|a3c|ddpg|td3/ → **0 命中**。
- 模式 /MDP|Markov (decision|chain)/ → **0 命中**。
- 模式 /reward/ → **0 命中**。
- 模式 /neural network|deep learning|machine learning/ → **0 命中**。
- **假阳性登记**：模式 /train(ing|ed)?/ 在该文 **36 命中**，核验为 **"transmission" / "constraint" 的子串误命中**（"transmission" 与 "constraint" 均含 "train"）—— 与 §9.4 同类陷阱。

### 10.5 负载设置（实验条件登记）

- 仿真环境（L656 逐字）："> The Walker constellation is used to construct an LEO satellite network in AGI Systems Tool Kit (STK) [40], based on which the parameters of the dynamic SDSTN topology are generated. All algorithms are executed on a simulation platform with an AMD Ryzen 5 5600X processor and 16GB of memory, and GUROBI is used to solve the master problem and subproblem in the BDBC algorithm."
- 场景（L660 逐字）："> The SDSTN scenario considered in our experiments includes 12 satellites which are distributed among 4 orbits with 45 deg inclination and altitude of 700 km, and the orbit period is 5927 seconds. In addition, there are 4 ground stations located at Jiuquan (39.76N, 98.56E), Taiyuan (37.87N, 112.56E), Wenchang (19.62N, 110.75E), and Xichang (27.89N, 102.27E), respectively, and 4 ground users located at (31.49N, 110.13E), (34.45N, 84.98E), (52.26N, 124.35E), and (21.98N, 100.94E), respectively."
- 时间参数（L660 逐字）："> The configuration period is set to 3600 seconds ... Moreover, the number of time slots is set as T = 36 and thus each time slot has a length of tau = 100 seconds."
- 资源与业务参数（L660 逐字）："> Communication links operate in Ka-band with a bandwidth of 20 MHz. The transmission capacity between two ground stations is set as 1 Gbps and all ground stations are able to place VNFs. We assume that each service requires two VNFs in addition to the first and last dummy VNF, and hence we have I_q = 4. The computation resource required for hosting each VNF is either 20 units or 30 units. The source node and destination node of each service are randomly selected according to the service type."
- 服务数扫描：Q = 20 / 40 / 60（L718）。
- **重要边界**：星座规模仅 **12 颗卫星**，远小于本批其他论文（907–4408）。引用其结论时必须声明该规模边界。

### 10.6 可迁移点

1. **式 21：端到端时延 = 占用时隙数 x tau**（L249）：把连续时延离散成**整数时隙计数**，可直接作为 RL 的即时奖励（每次状态转移 +1 时隙）。比直接用毫秒更利于学习（整数、尺度稳定、无归一化需求）。
2. **stay link 机制**（L181 + 式 17）：用指示函数把"同一节点同时隙连续处理多个 VNF"与"跨链路传输"区分开，且两种情形互斥。可迁移为 RL 中"原地动作（no-op / self-loop）"的显式动作项，避免策略被迫每步换节点。
3. **BDBC / TEDG 的两级方案**：精确解与实用解并存，复杂度有严格分析。可作为 RL 的**最优性上界参照**（在 12 星小规模上，RL 若不能逼近 BDBC 最优值则无意义）。
4. **服务完成时间 t_q 不确定性的处理（L188 逐字）**："> However, the number of time slots needed to deliver service data from the source node to the destination node is uncertain, which poses a challenge in formulating flow conservation constraints. To overcome this issue, we assume that service q is completed in time slot t_q, with 1 <= t_q <= T. Then, we formulate the dynamic flow conservation constraints as follows." —— 用"假定完成时隙"把不确定终点变成可枚举的分段约束（Case 1 / Case 2）。这是 RL 中"终止时刻未知"的一类处理技巧。
5. **资源按每时隙分配（L37 逐字）**："> the communication resource of each communication link and computation resource at each network node are allocated to each service on a per-time-slot basis" —— 时隙级资源重分配，对应 RL 中高频动作的可行性基础。

---

## 11. X2FCSU4S — Load Balancing Based on Cache Resource Allocation in Satellite Networks (Stackelberg 博弈)

**出处**：Erbao Wang, Hongyan Li, Shun Zhang（西安电子科技大学），IEEE Access 2019，DOI 10.1109/ACCESS.2019.2914167（L1–L9）。

### 11.1 决策机制

**Martingale 包络估计 backlog → 溢出概率界 → Stackelberg 博弈定价 → 分布式缓存价格议价**（外加流行度匹配）。摘要逐字（L15）：

> "During a high-speed movement, the satellites are connected intermittently, so the queue length becomes larger and a cache overflow appears. In this paper, the abundant storage resources of the multilayered satellite network (MLSN) are used to avoid the packet loss caused by a cache overflow of the Low Earth Orbit (LEO) satellites. However, due to the limited storage space of the Geostationary Earth Orbit (GEO) satellites, an effective load balance scheme which addresses two problems: LEO satellites competition in a non-cooperative fashion and content popularity utilization, is needed. Therefore, we propose a load balancing scheme based on the Stackelberg game, containing Members of a Game Algorithm and Distributed Cache Price Bargaining Algorithm. In addition, a storage technology based on content popularity (Popularity Matching Algorithm) is introduced."

角色划分（L260 逐字）：

> "the objective of a low layer satellite (LEO satellites) has a lower congestion probability, as low as possible. In other words, LEO satellites are expected to upload as much data as possible to the GEO satellite. However, due to the limited storage space of an GEO satellite, the LEO satellites compete for the resources in a non-cooperative fashion. At the GEO satellite side, the objective is to maximize the revenue by selling the storage space to the LEO satellites."

**必须标注：本文的"负载均衡"是缓存空间分配，不是路由。** 标题与摘要均如此。

### 11.2 代价函数公式（逐字 LaTeX）

Martingale 包络（L142，式 9）：
$$
\begin{array} { c } { { M _ { A ^ { t } } ( T ) = h _ { A ^ { h } } ( a _ { T } ) h _ { A ^ { f } } ( a _ { T } ^ { f } ) h _ { S ^ { q } } ( s _ { T } ) } } \\ { { \times e ^ { \theta ( A ^ { h } ( \kappa , T ) - ( T - \kappa ) \kappa _ { f } + A ^ { f } ( T ) - T k _ { h } + T \kappa _ { s } - S ^ { q } ( T ) ) } . } } \end{array}\tag{9}
$$
等效服务过程（L154，式 10）：
$$
M _ { S } ( T ) = h _ { S } ( s _ { T } ) e ^ { \theta ^ { * } ( \{ S ( T ) - T \kappa _ { s s } \} ) }\tag{10}
$$
Zipf 流行度（L164，式 11）：
$$
t _ { f } = { \frac { 1 / f ^ { s } } { \displaystyle \sum _ { i = 1 } ^ { F } ( 1 / i ^ { s } ) } } , \quad \forall f \in { \mathcal { F } } ,\tag{11}
$$
时延上界（L185 式 12、L193 式 13）：
$$
p ( \mathbf { W } ( T ) > \kappa ) \leq \frac { E ( M _ { A ^ { t } } ( 0 ) ) E ( M _ { S } ( 0 ) ) } { H } e ^ { - \theta _ { 1 } ^ { * } \kappa \kappa _ { S S } } ,\tag{12}
$$
$$
\theta _ { 1 } ^ { * } \in \bigg \{ \theta > 0 \bigg \vert \frac { R _ { a } \mathrm { l n } [ s p ( \mathbf { M } ^ { \theta } ) ] } { \theta } \leq \frac { \ln [ e ^ { - \theta \kappa _ { s s } } ] } { - \theta } \bigg \}\tag{13}
$$
FIFO 溢出概率界（L208 式 14、L214 式 15、L220 式 16）：
$$
\frac { E ( M _ { A ^ { t } } ( 0 ) ) E ( M _ { S } ( 0 ) ) } { H } e ^ { - \theta _ { 1 } ^ { * } \sigma _ { F I F O , L } } ,\tag{14}
$$
$$
\theta _ { 1 } ^ { \ast } \in \Bigg \{ \theta > 0 \bigg \vert R _ { a } \leq \frac { \kappa _ { s s } \mathrm { l n } [ s p ( \mathbf { M } ^ { \theta } ) ] } { \theta } \Bigg \}\tag{15}
$$
$$
\sigma _ { F I F O , L } = \frac { 1 } { \theta _ { 1 } ^ { * } } \ln \frac { E ( M _ { A ^ { t } } ( 0 ) ) E ( M _ { S } ( 0 ) ) } { H p _ { F I F O , L } } ,\tag{16}
$$
SP 调度下的溢出概率界（L228，式 17）：
$$
\frac { E ( M _ { A ^ { f } } ( 0 ) ) E ( M _ { A ^ { h } } ( 0 ) ) E ( M _ { S } ( 0 ) ) } { H } e ^ { - \theta _ { 2 } ^ { * } ( \sigma _ { S P , L } - \sigma _ { S P , L } ^ { a , h } ) } ,\tag{17}
$$
GEO 收益（L267，式 20）：
$$
R _ { \mathrm { G E O } } ( \pmb { \eta } , q ) = \sum _ { k = 1 } ^ { K } \eta _ { L _ { k } } s _ { L _ { k } } ( q _ { L _ { k } } ) ,\tag{20}
$$
Leader 问题（L273，式 21）：
$$
\begin{array} { r l } { P r o b l e m ~ { \cal I } \colon } & { \operatorname* { m a x } ~ R _ { \mathrm { G E O } } ( \eta , q ) } \\ & { \mathrm { s . t . } ~ \displaystyle \sum _ { k = 1 } ^ { K } s ( q _ { L _ { k } } ) \leq h ( \sigma _ { G } ( p _ { G } ) ) . } \end{array}\tag{21}
$$
拥塞指数（L281，式 22）：
$$
\begin{array} { r } { I ( q _ { L _ { k } } ) = \ln \left( \displaystyle 1 + \frac { q _ { L _ { k } } \sigma _ { L _ { k } } } { \displaystyle \sum _ { j \neq k } ^ { K } q _ { L _ { j } } \sigma _ { L _ { j } } } \right) , ~ \displaystyle \sum _ { j \neq k } ^ { K } q _ { L _ { j } } \sigma _ { L _ { j } } \neq 0 } \\ { \forall k , ~ j , ~ q _ { L _ { k } } > 0 , q _ { L _ { j } } > 0 k , ~ j \in \{ 1 , 2 , \ldots , K \} } \end{array}\tag{22}
$$
LEO 利润（L291，式 23）：
$$
\mathrm { R } _ { \mathrm { L E O } } = c f ( \sigma _ { L _ { k } } ) I ( q _ { L _ { k } } ) - \eta _ { L _ { k } } s ( q _ { L _ { k } } ) ,\tag{23}
$$
Follower 问题（L299，式 24）：
$$
P r o b l e m 2 \colon \operatorname* { m a x } R _ { \mathrm { L E O } } ( q _ { L _ { k } } , - q _ { L _ { k } } , \eta _ { L _ { k } } ) ,\tag{24}
$$
Stackelberg 均衡条件（L311 式 25、L315 式 26）：
$$
R _ { \mathrm { G E O } } ( \pmb { \eta } ^ { * } , \pmb { q } ^ { * } ) \geq ( \pmb { \eta } , \pmb { q } ^ { * } ) ,\tag{25}
$$
$$
R _ { \mathrm { L E O } } ( q _ { L _ { k } } ^ { * } , - q ^ { * } , \eta ^ { * } ) \geq ( q _ { L _ { k } } , - q ^ { * } , \eta ^ { * } ) .\tag{26}
$$
最优份额闭式解（L335，式 28）：
$$
q _ { L _ { k } } ^ { * } = \left( \frac { c f ( \sigma _ { L _ { k } } ) } { \sigma _ { L _ { k } } \eta _ { L _ { k } } } - y _ { L _ { k } } \right) ^ { + } , \quad \forall k ,\tag{28}
$$
非统一定价最优解（L421，式 36）与统一定价最优解（L463 式 40、L471 式 41）亦为闭式。

### 11.3 粒度与动作

- **决策粒度：每颗 LEO 卫星，决定上传到 GEO 的数据份额 q_{L_k} in R+（连续）**，以及 GEO 侧的定价向量 eta（连续）。
- 三层算法（L486 逐字）："> In the initialization phase, first an error calculation accuracy value zeta is given, and then Algorithm 1 is implemented. If |Sigma q_{L_k} - h(sigma_G)| < zeta is satisfied, then Algorithm 3 is implemented; otherwise, Algorithm 2 is implemented."
  - **Algorithm 1**（L398–L418）：确定参与者集合 U（按 sqrt(f / y) 排序，逐步剔除）。
  - **Algorithm 2**（L424–L444）：分布式缓存价格议价（GEO 按 Sigma q_{L_k} 与 h(sigma_G) 的差以 Delta eta 步长调价，直至 |Sigma q - h| < zeta）。
  - **Algorithm 3**（L492–L500）：流行度匹配（把不受欢迎的内容上传到 GEO）。
- **本文不涉及路由**：动作是"上传多少缓存内容"，不是"发往哪条链路"。
- 高 / 低优先级两类到达被显式区分（L137 逐字）："> we divide the arriving traffic into two types highpriority arrival A^h(T) and the low-priority arrives A^f(T) and A^t(T) = A^h(T) + A^f(T)."

### 11.4 是否含学习

**结论：不含学习成分（博弈论 + 凸优化 + 阈值 + Martingale 界）**。

检索与实测（范围：该 MD 全文 850 行，grep -niE）：
- 模式 /reinforcement learning|Q-learning|DQN|deep Q-network/ → **0 命中**。
- 模式 /dueling|prioriti[sz]ed (experience )?replay|double (q|dqn|deep q)|actor(-| )critic|\bppo\b|\bsac\b|policy gradient|a3c|ddpg|td3/ → **0 命中**。
- 模式 /MDP|Markov (decision|chain)/ → **2 命中**：**L80**（逐字："FIGURE 2. Gilbert−Elliott model can be abstracted as a two-state Markov chain."）与 **L82**（逐字："Explicitly, the evolution states of the terrestrial-satellite link can be depicted by a twostate Markov chain model which is shown in Fig.2, where g denotes the good state; b denotes the bad state..."）。**两处均为"信道状态"的马尔可夫链，不是决策过程（MDP）；不构成学习成分。**
- 模式 /reward/ → **0 命中**。
- 模式 /neural network|deep learning|machine learning/ → **1 命中**：**L730**（附录 Martingale 背景的通用表述，逐字："a very useful class of random processes which appear in many fields (e.g., finance, machine learning, information theory, etc.)"）。**属通用背景叙述，非本文方法。**

### 11.5 负载设置（实验条件登记）

- 星座（L490 逐字）："> In the simulations, we used the STK (Satellite Tool Kit) tool to generate an Iridium-like constellation, as shown in Fig.10. This constellation contained 66 LEO satellites evenly distributed over six orbital planes. At the same time, we added three GEO satellites to this scene."
- 队列参数（L201 逐字）："> The simulation parameters were lambda_f = 0.6, p_m = 0.1 and R_su = 1."
- Martingale 界的紧致性验证（L201 逐字）："> As Fig.5 shows that the delay bound p(W(T) > kappa) given by the Martingale bounds is quite tight. Since the method of Martingale-envelope can achieve a tight upper bound, we use this delay bound directly in the backlog estimation."
- 到达与信道：Gilbert-Elliott 两态信道（L80/L82）+ 按时间片恒定的信道状态（L135 逐字："> the state of the Gilbert-Elliott channel keeps constant during a time slot but changes from one slot to another"）。
- 流行度：Zipf 参数 s in [0,1]（L167 逐字："> s is the coefficient which controls the popularity distribution of the contents, and 0 <= s <= 1. At s = 0, the distribution is uniform"）。
- **注意**：本文的负载是**内容请求到达 + 缓存排队**，与"包级路由负载"不是同一类对象。引用时须区分。

### 11.6 可迁移点

1. **溢出概率上界作为约束而非硬门限（式 12–17）**：用 Martingale 包络把"队列溢出概率"写成可计算的闭式上界，而不是把缓冲写死。可迁移为 RL 中"软约束"的构造方式（用概率界替代硬截断）。
2. **FIFO 与 SP 两种调度下的不同溢出界（式 14 vs 式 17）**：**同一物理现象（缓存溢出）在不同调度策略下有不同的上界表达式**——这是本批中对 G-A 最有启发的一条，但分解轴是**调度策略**（FIFO/SP）与**业务优先级**（A^h/A^f），**不是失败原因**（详见 §13）。
3. **拥塞指数 I(q) 的对数干扰式定义（式 22）**：把"我对他人造成的拥塞"定义为 ln(1 + 自身占用 / 他人占用之和)，与 Shannon 公式中干扰项的类比（L284 逐字："> In the Shannon formula, the power of other users to the user interference is used as a denominator."）。可迁移为多智能体 RL 中的**拥塞型外部性**奖励项。
4. **Stackelberg 两层结构（leader = GEO，follower = LEO）**：leader 先定价、follower 再决策，对应 RL 中的 **Stackelberg / bilevel 博弈**结构（分层 RL）。式 28 给出 follower 的闭式最优响应，可作层级 RL 中下层策略的解析对照。
5. **流行度作为决策依据（式 11 + Alg.3）**：把"内容冷热"纳入决策，对应 RL 中"请求分布作为状态特征"。

---

## 12. 负向声明台账（本批全部"未见/没有"的证据）

以下所有计数均为在 VM 上对这 11 个 MD 文件执行 `grep -niE`（对 XM6NUPM4 因含非 UTF-8 字节必须加 `-a`）所得的实测值。

### 12.1 模式 A：/reinforcement learning|Q-learning|DQN|deep Q-network/

| itemKey | 计数 | 命中位置与性质 |
|---|---|---|
| DVS8C3CC | 2 | L77（转述他人工作 [27]）、L533（参考文献著录） |
| 36RZKNW5 | 5 | L52、L60（相关工作泛述）、**L234（基线 PPO-CSO MR）**、L386、L426（参考文献） |
| LBMABZJ7 | **0** | — |
| MYBALQ2D | **0** | — |
| JS857IYN | 2 | L42（相关工作泛述）、L356（参考文献 [25]） |
| K7U4TYJN | 10 | L25、L321、L327、L346、L348、L362、L389（正文/对比基线）、L433、L453、L481（参考文献） |
| JZA5SEQA | **0** | — |
| TRM2HPFN | **0** | — |
| XM6NUPM4 | 1 | L430（参考文献 [34]） |
| WHS8Z44C | 1 | L752（参考文献 [14]） |
| X2FCSU4S | **0** | — |

**判定**：本批 11 篇中，**只有 K7U4TYJN（SKYLINK）自身的核心方法是学习型的**（contextual MAB + UCB）；其余 10 篇的全部命中都是**相关工作转述、对比基线引用或参考文献著录**，不构成本文方法。

### 12.2 模式 B：具体 RL 算法名（用于排除隐含的 RL 方法）

| 子模式 | 全库计数 | 说明 |
|---|---|---|
| /dueling/ | **全 11 篇 = 0** | — |
| /prioriti[sz]ed (experience )?replay/ | **全 11 篇 = 0** | 注意本模式**不含裸 priorit\***，避免命中散文词 "prioritize"（主控 B3 批次教训） |
| /double (q\|dqn\|deep q)/ | **全 11 篇 = 0** | 注意本模式**不含裸 double**，避免命中散文词 "double-check" 等 |
| /actor(-\| )critic/ | **全 11 篇 = 0** | — |
| /\bppo\b/ | 36RZKNW5 = 10 | L60, 234, 286, 288, 290, 306, 314, 321, 327, 329——**全部为基线名 PPO-CSO MR 及其结果讨论**，逐条核验无例外 |
| /\bsac\b/ | **全 11 篇 = 0** | — |
| /policy gradient/ | **全 11 篇 = 0** | — |
| /a3c\|ddpg\|td3/ | K7U4TYJN = 1 | **假阳性**：L339 图片文件名 "9d7c3d5e6c25e51480d85e1372bc4dda9711aeddba3cba11ebfe3956de352226.jpg" 中夹带 a3c 子串 |

### 12.3 模式 C：/MDP|Markov (decision|chain)/

| itemKey | 计数 | 命中位置与核验 |
|---|---|---|
| 36RZKNW5 | 1 | **L60**——他人 DRL 工作的转述（"embed a delay model into the Markov Decision Process and apply Proximal Policy Optimization (PPO) for congestion control [33]"），非本文方法 |
| X2FCSU4S | 2 | **L80、L82**——Gilbert-Elliott **信道** 两态马尔可夫链，非决策过程 |
| 其余 9 篇 | **0** | — |

### 12.4 模式 D：/reward/

| itemKey | 计数 | 命中位置与核验 |
|---|---|---|
| LBMABZJ7 | 6 | **L188, L189, L190, L235, L236, L237**——DisCoRoute 内部比较两跳纬度和的**几何量** reward_s / reward_t，**与 RL 奖励无关** |
| K7U4TYJN | 1 | **L433**——参考文献 [14] 标题 "Shaping rewards, shaping routes" 中的词 |
| 其余 9 篇 | **0** | — |

### 12.5 模式 E：/neural network|deep learning|machine learning/

| itemKey | 计数 | 命中位置与核验 |
|---|---|---|
| DVS8C3CC | 1 | **L465**——作者未来工作愿景（"we envision the use of machine learning models to predict congestion situations"） |
| 36RZKNW5 | 3 | L28（GNN 相关工作）、L52（GRouting = GNN + DRL，相关工作）、L428（参考文献标题） |
| K7U4TYJN | 1 | **L477**——参考文献标题（卫星入侵检测的深度学习模型），与本文方法无关 |
| JZA5SEQA | 1 | **L295**——参考文献标题 "Fast and Adaptive Failure Recovery using Machine Learning in Software Defined Networks" |
| X2FCSU4S | 1 | **L730**——附录 Martingale 背景的通用叙述（"finance, machine learning, information theory, etc."） |
| 其余 6 篇 | **0** | — |

### 12.6 已登记的假阳性陷阱清单（供后续批次复用）

1. **几何量叫 "reward"**：LBMABZJ7 的 reward_s / reward_t（§12.4）——最易误判为"含学习"。
2. **图片文件名夹带算法缩写**：K7U4TYJN L339 的 .jpg 哈希串含 "a3c"（§12.2）。
3. **子串误命中 train**：XM6NUPM4 的 20 次、WHS8Z44C 的 36 次 /train(ing|ed)?/ 命中，来自 "transmission" / "constraint"（§9.4、§10.4）。
4. **作者姓名或参考文献命中缩写**：MYBALQ2D L621 的 "Z Morley Mao" 命中 /MORL/（§4.4）。
5. **散文词命中**：主控 B3 批次已知的 "prioritize"；本批已在模式设计阶段用词边界规避（§12.2）。
6. **文件被判为 binary 导致 grep 无数字**：XM6NUPM4 必须用 `grep -a`，否则只输出 "binary file matches"，容易出现"未读到就报数"的失真。

---

## 13. 对抗性问题（缺口 G-A）的答复

**问题**：全库（本批 11 篇）是否有任何工作，把**同一个失败事件**（丢包 / 超时 / 溢出）按**物理原因**拆成**不同的学习通道或惩罚项**（例如区分"决策缓存溢出"与"链路队列溢出"）？

### 13.1 结论

**没有。本批 11 篇中不存在把同一失败事件按物理原因分解为不同学习通道或不同惩罚项的工作。** 缺口 G-A 在本批范围内**成立**。

但存在 **1 条最接近的"原因枚举但单通道惩罚"证据（K7U4TYJN）** 与 **3 条在"分解轴"上相邻但不同的证据（JS857IYN、TRM2HPFN、X2FCSU4S）**，必须逐条写清它们的分解轴，避免被误读为反例。

### 13.2 检索与实测（全部为 grep -niE 实测计数）

| 模式 | 全库计数 | 命中位置与核验 |
|---|---|---|
| /credit assignment/ | **全 11 篇 = 0** | — |
| /counterfactual/ | **全 11 篇 = 0** | — |
| /reward decompos/ | **全 11 篇 = 0** | — |
| /reward vector/ | **全 11 篇 = 0** | — |
| /multi-head/ | **全 11 篇 = 0** | — |
| /per-cause/ | **全 11 篇 = 0** | — |
| /separate (reward\|penalt\|channel\|loss\|queue)/ | **全 11 篇 = 0** | — |
| /loss (reason\|cause\|type)\|(reason\|cause) (for\|of) (the )?(loss\|drop\|failure)/ | X2FCSU4S = 1 | **L15**，逐字："the abundant storage resources of the multilayered satellite network (MLSN) are used to avoid the packet loss caused by a cache overflow of the Low Earth Orbit (LEO) satellites"——**只提到"cache overflow 导致 packet loss"这一条因果，未拆分为不同通道** |
| /different (types\|kinds\|categories) of (loss\|drop\|failure\|outage)/ | **全 11 篇 = 0** | — |
| /failure (type\|cause\|reason)\|cause of (the )?failure\|failures? (are )?(classified\|categorized)/ | **全 11 篇 = 0** | — |
| /packet loss\|dropped\|drop rate\|drops/ | K7U4TYJN = 29（详见 13.3）、36RZKNW5 = 4、JS857IYN = 2、X2FCSU4S = 2、DVS8C3CC = 1 | — |
| /multi-objective/ | JS857IYN = 4 | L27 与 L48（本文目标函数自述）、L318 与 L362（**参考文献标题**）——详见 13.4 |
| /MORL/ | MYBALQ2D = 1 | **假阳性**：L621 作者名 "Z Morley Mao" |
| /overflow/ | X2FCSU4S = 1 | **L15**（cache overflow 的因果描述） |
| /penalt/ | DVS8C3CC = 16 | 均为 **eta_penalty**（LISL 建立延迟惩罚，式 6）——分解轴是"时延分量 vs 切换惩罚"，**不是失败原因** |
| /reward shap\|scalariz\|weighted sum of (the )?(objective\|reward\|cost)/ | **全 11 篇 = 0** | — |
| /queue overflow\|cache overflow\|buffer overflow/ | X2FCSU4S = 1 | **L15** |

### 13.3 最接近的证据：K7U4TYJN —— "原因枚举，但单通道惩罚"（**不覆盖 G-A**）

该文是**本批唯一同时做到"枚举失败原因"和"含学习成分"**的论文，因此是最可能构成反例的候选。逐条核验如下：

**它确实枚举了失败原因**（L146 逐字）：
> "Data streams are dropped due to low link capacity, whenever they are transmitted in a loop, if they reach a node without outgoing links, or if their delay exceeds the maximum tolerable delay T_max."

即四种原因：① 链路容量不足；② 进入环路；③ 到达无出链路的节点；④ 时延超过 T_max。

**但它把所有原因压进同一个标量惩罚**（L172 + L186 逐字）：
> "If the terminal node in path X is not the internet node z or if the path contains a loop, the traffic is dropped and D_X is set to T_max. The same applies if the paths' delay exceeds T_max."
> "As dropped data contributes the highest possible delay of T_max to c_t(x_t), considering c_t(x_t) as the optimization target leads to a joint minimization of average delay and drop rate."

**判定**：4 种不同的物理原因，**全部映射到同一个数值 T_max = 200 ms（TABLE II，L317）**，并汇入同一个标量代价 c_t（式 14）。学习通道也只有一个：单一 UCB 分数（式 16–17）按**链路**更新，**不按失败原因分流**。

→ **这是"原因枚举 + 单通道惩罚"，不构成 G-A 的反例。** 但它极有价值：它证明了"在 LEO 路由的工程语境下，作者已经意识到失败原因不止一种"，却仍然选择单一惩罚 —— 这正好支撑 G-A 的缺口主张（**原因被识别了，但从未被分开学习**）。

### 13.4 相邻但分解轴不同的三条证据（**均不覆盖 G-A**）

| itemKey | 分解对象 | 分解轴 | 是否分流到不同学习通道/惩罚项 | 是否覆盖 G-A |
|---|---|---|---|---|
| JS857IYN（式 13，L170） | 链路代价 A_{i,j,t} 的三项：容量 S_bar、时延 L_bar、链路抖动 phi_bar | **目标类型**（capacity / latency / link churn） | **否**：三项被线性标量化为单一 A_{i,j,t}，再加历史项 Pi 后 argmin；且全程无学习 | **否** |
| TRM2HPFN（L157） | 路径序列优化的目标：HO delay jitter vs path HO rate | **代价类型**（切换的瞬时抖动 vs 切换的频率） | **否**：两个目标是**并列的备选优化准则**（分别在不同研究中实现），不是同一事件的多个通道；且无学习 | **否** |
| X2FCSU4S（式 14 vs 式 17） | 缓存溢出概率界 | **调度策略**（FIFO vs SP）+ **业务优先级类别**（A^h 高优先 / A^f 低优先） | **否**：同一"溢出"现象在不同调度下换了上界表达式，但仍是**单一溢出事件**；且无学习 | **否** |

补充说明 X2FCSU4S 的特殊性：它是本批中唯一**显式区分两类到达流**（L137 逐字："we divide the arriving traffic into two types highpriority arrival A^h(T) and the low-priority arrives A^f(T)"）并给出两种调度下不同溢出界的论文。若要把 G-A 推广为"按**业务类别**分流惩罚"，本文是最接近的先例；但 G-A 问的是**物理原因**（如"决策缓存溢出"vs"链路队列溢出"），本文的两类流是**优先级**而非原因，故**不覆盖**。

### 13.5 对 G-A 的净判断

- **反例：0 条。**
- **最接近：K7U4TYJN（原因枚举但单通道 T_max 惩罚）** —— 这是本批对该缺口最强的**支持性**证据，因为它证明原因清单已被识别却未被分通道学习。
- **相邻但不覆盖：JS857IYN（按目标类型标量化）、TRM2HPFN（按代价类型并列）、X2FCSU4S（按调度策略/业务优先级）**。
- 三条边界提醒：
  1. 本批 11 篇中**仅 1 篇（K7U4TYJN）含学习**，其余 10 篇无学习成分，因此"按原因分流的学习通道"这一概念在本批中的**可观测基数极小**——本结论的强度受此限制，不能外推为"全库都没有"。
  2. "失败"在本批中的语义高度分散：丢包（K7U4TYJN）、缓存溢出（X2FCSU4S）、链路/节点故障（JZA5SEQA）、路径失效（MYBALQ2D）、超时（K7U4TYJN 的 T_max），**彼此不是同一个事件**，因此"同一失败事件按物理原因拆分"这一提法在本批中甚至缺少统一的被分解对象。
  3. 建议在更大范围（T1 的 34 篇 RL 路由论文）复核模式 /credit assignment|counterfactual|reward decompos|multi-head|separate (reward|penalt)/，因为本批学习型论文仅 1 篇，统计功效不足。

---

## 14. 本批完成度声明

- **已通读并产出 6 项的论文：11 / 11**（DVS8C3CC、36RZKNW5、LBMABZJ7、MYBALQ2D、JS857IYN、K7U4TYJN、JZA5SEQA、TRM2HPFN、XM6NUPM4、WHS8Z44C、X2FCSU4S）。
- **未完成项：无。**
- **读取方式**：对每篇 MD 全量取行（`awk` 带行号打印正文，跳过的仅为纯图片行 `![](images/...)` 与空行；参考文献区在 DVS8C3CC、LBMABZJ7、WHS8Z44C、X2FCSU4S、36RZKNW5、K7U4TYJN 中做了抽样核验而非逐条精读，用于判定"RL 提及是否属本文方法"）。公式一律逐字抄 LaTeX 原文。
- **未做的事（诚实声明）**：① 未对任何论文做复现实验；② 未核验其数值结果的正确性；③ "是否已被 RL 论文采用"一项，仅登记了本批内部可验证的引用关系（DVS8C3CC ← LBMABZJ7 / TRM2HPFN；K7U4TYJN → T1 的 [14][24]），**跨批次的外部引用情况未做检索**；④ 未读取 T1/T3–T6 批次的论文，因此 §13 的 G-A 结论**仅限本批 11 篇**。

