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
- 模式 /MDP|Markov (decision|chain)/ → **1 命中**（L412：算法复杂度讨论中的非决策过程用法，未构成本文方法）。
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


