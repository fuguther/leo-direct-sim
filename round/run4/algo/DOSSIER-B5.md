# DOSSIER-B5 — T2 机制级定读（11 篇）

> 批次：T2 → B5｜itemKey：JP79GMZS、TQF59BD7、SBCHGBCP、X5K285MW、AJJI57M9、9GPFG5U3、AF674CSF、IXVSNEE3、9KZDXPKC、BBNQ4EAQ、VFS59FHI
> 产出：deepener 子会话（session-eee37a6ecf5b）｜日期：2026-09-11｜分支：agent/20260911-topic-loop-r2
> 证据源：VM MinerU MD，/data/liguang13/topic-loop-r2/md/<itemKey>/<itemKey>/txt/<itemKey>.md，**11 篇逐行通读**（总 5286 行）。
> 纪律：每条 = MD 行号 + 逐字英文原文；公式逐字抄 LaTeX，不改写；"未见"声明一律附精确检索模式 + 实测计数 + 命中位置与不构成反例的理由；负载/流量设置只作条件登记。

## 0. 通读范围与总览

| # | itemKey | 短名 | 行数 | 学习成分 | 决策主体 | 动作空间 | 本批内引用 |
|---|---|---|---|---|---|---|---|
| 1 | JP79GMZS | ELB 显式负载均衡 | 412 | 无 | 每颗卫星（分布式） | 邻居级：转发比例 chi + 改路由表 | 被 SBCHGBCP[31] L392、IXVSNEE3[23] L663、BBNQ4EAQ[24] L469 引用 |
| 2 | TQF59BD7 | IDLB 分布式 SDN 负载均衡 | 605 | 无 | 簇内 SDN 控制器卫星 + 入口卫星 | per-flow 选路（best-of-k）+ NHCN 选择 | 引用 X5K285MW[9] L544 |
| 3 | SBCHGBCP | 分段路由 TE + 快速重路由 | 419 | 无 | 源节点（TE）+ 本地故障节点 | per-flow 分流比 r_k；本地备份下一跳/2 段路径 | 引用 JP79GMZS[31] L392 |
| 4 | X5K285MW | 源路由方案分析 | 166 | 无 | 入口卫星 | per-flow 从最小跳路径集随机选 1 条 | 被 TQF59BD7[9] 引用 |
| 5 | AJJI57M9 | Ekici 数据报路由 | 431 | 无 | 每颗卫星逐包 | 2 个（primary/secondary 方向） | 见 §5.6（无直接引用） |
| 6 | 9GPFG5U3 | LiR 链路标识 + 包内 BF | 712 | 无 | 源卫星 + 重编码卫星 | 每跳查 3 条出向 ISL；编码策略向量 x | 被 9KZDXPKC[10] L307 引用 |
| 7 | AF674CSF | LPIH 逻辑路径标识分层路由 | 619 | 无 | 管理卫星（单/多） | 组间 PID 选择 + 组内 NID 下一跳 | 被 9KZDXPKC[9] L305 引用 |
| 8 | IXVSNEE3 | KNBG-MHCE + 星地协同路由 | 726 | 无 | 每颗卫星逐包（源封装） | 2 个（水平/垂直候选方向）+ 队列饱和硬切换 | — |
| 9 | 9KZDXPKC | DB-R 默认+备份路由 | 336 | 无 | 每颗卫星路由表 + 触发器 | 路由表项（默认项出接口/备份项优先级） | 引用 AF674CSF[9]、9GPFG5U3 线[10] |
| 10 | BBNQ4EAQ | TNM / NSR 时序网网格 | 495 | 无 | 每颗卫星逐跳 | 邻居 netgrid 集合（每跳多选） | 引用 JP79GMZS[24] L469 |
| 11 | VFS59FHI | SR 负载均衡（回传） | 365 | 无 | 集中算路 + 每业务小区 | 选路 + **显式拒绝** | — |

### 0.1 "无学习成分"的统一检索证据（适用全 11 篇）

检索范围：上述 11 个 MD 全文（5286 行）。命令形态：grep -ciE '<模式>' <11 个文件路径>；命中行用 grep -inE 复核。

| 模式（逐字） | 11 篇计数 |
|---|---|
| Q-learning\|DQN\|deep Q\|reinforcement learning\|actor-critic\|policy gradient\|multi-agent | 全 0 |
| reinforcement | 全 0 |
| \blearn | TQF59BD7=1、X5K285MW=1，其余 0 |
| \btrain | TQF59BD7=1（唯一命中 L82 "trains"，地面交通工具名词），其余 0 |
| supervised | 全 0 |
| neural | JP79GMZS=1，其余 0 |
| reward | **全 0** |
| credit assignment | **全 0** |
| counterfactual | **全 0** |

命中位置与"是否构成学习成分"的判定（逐条）：
- TQF59BD7 **L516**："The proposed protocol is also suitable for multilayer constellations, and multilevel SDN hierarchies. It offers an extensible baseline for future research, for instance as an enabler of machine learning-enhanced traffic engineering." → **未来工作展望，协议本体无学习成分**。
- X5K285MW **L74**："Alternatively, ML-based approaches have gathered interest, as they can approximate functions of optimization problems with lower computational complexity [19]." → **旁述他人方向，本文未使用**。
- X5K285MW **L165**：参考文献 [19] 题名 "Deep Learning in Mobile and Wireless Networking: A Survey" → **参考文献题名，非本文内容**。
- JP79GMZS **L403**：作者简介 "...his research interests are ... image processing, and neural networks." → **作者简历，非论文内容**。

> **踩坑登记（供后续批次复用）**：朴素模式 train 会命中散文词 "constraints" 的子串（JP79GMZS L5/L25、TQF59BD7 L31/L82、IXVSNEE3 L21/L29/L58 等）；裸 penal 会命中 X5K285MW L106 "processing penalty"；裸 Pareto 会命中 JP79GMZS L215 的 "Pareto distribution"；裸 drop cause 会命中 9KZDXPKC L246/L248 的 "drop caused by" 子串。**必须用带边界的模式**。

### 0.2 本批内引用关系（可核验，非推测）

- SBCHGBCP **L392** 文献 [31]："T. Taleb, D. Mashimo, A. Jamalipour, N. Kato, Y. Nemoto, Explicit load balancing technique for NGEO satellite IP networks with on-board processing capabilities, IEEE/ACM Trans. Netw. 17 (1) (2009) 281-293." → 即 JP79GMZS。
- IXVSNEE3 **L663** 文献 [23]：同篇；且 **L525** 明确沿用其流量模型："we set 3000 non-persistent on-off flows similar to [23]"。
- BBNQ4EAQ **L469** 文献 [24]：同篇。
- TQF59BD7 **L544** 文献 [9]："M. M. H. Roth, Analyzing Source-Routed Approaches for Low Earth Orbit Satellite Constellation Networks, in LEO-NET'23" → 即 X5K285MW。
- 9KZDXPKC **L305** 文献 [9]："F. Yan, Z. Wang, S. Zhang, Q. Meng, and H. Luo, Logic path identified hierarchical routing for large-scale leo satellite networks, IEEE TNSE, vol. 11, no. 4, pp. 3731-3746, 2024." → 即 AF674CSF；**L307** 文献 [10]："H. Zhang, Z. Wang, S. Zhang, Q. Meng, and H. Luo, Optimizing link-identified forwarding framework in LEO satellite networks" → 即 9GPFG5U3 的会议前身（9GPFG5U3 L633 文献 [1] 同篇）。

---

## 1. JP79GMZS — Explicit Load Balancing Technique（ELB），412 行

### 1) 决策机制：谁在何时决定什么

- **谁**：每颗具备星上处理能力的卫星各自决策（分布式）。**L49**："In such distributed load balancing techniques, satellites independently decide on the best next hop to which packets should be forwarded."
- **何时**：持续监测 + 状态迁移时立即通告。**L29**："a satellite continuously monitors its queue size to determine its state which may be free, fairly-busy, or busy. A change in the state of a satellite is immediately notified to its neighboring satellites via a Self-State Advertisement packet. As a consequence, the cost of the links between the busy satellite and its neighbors is then increased."
- **三态定义 L61**："The state of a satellite is marked as Free State (FS) when the queue ratio of its current queue occupancy to the total queue size, $Q r$ , is inferior to a pre-defined threshold $\alpha .$ . The satellite is considered to be in a Fairly Busy State (FBS) when its queue ratio is between the threshold and another predetermined threshold $\beta .$ . The satellite is considered to be in a Busy State (BS) if its queue ratio exceeds the threshold $\beta .$"
- **决定什么（两级通告）L63**："when a given satellite A experiences a state transition from free to fairly busy, it sends a warning message to its neighboring satellites informing them that it is about to get congested. The neighboring satellites are then requested to update their routing tables and start searching for alternate paths that do not include satellite A. When the satellite enters the busy state, it transmits a Busy State Advertisement (BSA) signaling packet requesting the neighboring satellites to reduce their sending rates of traffic destined to satellite A by a ratio $\chi .$ The $( 1 - \chi )$ portion of traffic data will be transmitted via alternate paths retrieved earlier."
- **状态估计用"持续队列长度"而非 EWMA L57**："the proposed ELB scheme considers the use of persistent queue length to indicate congestion. In essence, the persistent queue length is defined as the sustained buffer occupancy of a satellite during a time interval. This computation solves the heuristics in the EWMA parameter setting and can be easily implemented in satellites with much less computational demand than EWMA."
- **多业务类分派顺序 L164**："a satellite starts detouring first packets of class C. If the requested detouring ratio of traffic $X ( X = 1 - \chi )$ is larger than the traffic percentage of class C, the traffic of class B is detoured as well. The delay-sensitive traffic of class A always traverses the default path that is determined by the routing protocol in use (e.g., Dijkstra) and is not detoured."

### 2) 代价/阈值/更新函数（公式逐字）

公式 (1)，L71-73：
$$
\delta _ { d } = { \frac { \left( Q _ { l } - q ( t ) \right) \cdot P _ { \mathrm { a v g } } } { I - O } }\tag{1}
$$

公式 (2)，L83-85：
$$
p = \mathrm { M i n } \left( 1 , \frac { \delta + d } { \delta _ { d } } \right) .\tag{2}
$$

公式 (3)，L89-91：
$$
\beta = 1 - p .\tag{3}
$$

公式 (4)，L97-99：
$$
\alpha = { \frac { \beta } { 2 } } .\tag{4}
$$

公式 (5)，L105-107：
$$
q ( t _ { \mathrm { B S A } } ) = \mathrm { M i n } \left( Q _ { l } \cdot \beta + \frac { d \cdot ( I _ { s } + I _ { t } - O ) } { P _ { \mathrm { a v g } } } , Q _ { l } \right) .\tag{5}
$$

公式 (6)，L116-118：
$$
( I _ { s } ^ { \mathrm { n e w } } + I _ { t } ) - O = \frac { P _ { \mathrm { a v g } } \cdot ( q ( t _ { \mathrm { B S A } } ) - Q _ { l } \cdot \alpha ) } { \theta } .\tag{6}
$$

公式 (7)，L122-124：
$$
{ { { \chi } } } = \mathrm { M i n } \left( \mathrm { M a x } \left( 0 , \frac { { { \cal I } _ { s } ^ { \mathrm { n e w } } } } { { { \cal I } _ { s } } } \right) , 1 \right) .\tag{7}
$$

公式 (8)，L130-132：
$$
L _ { \mathrm { c o s t } } ( t ) = T _ { d } + T _ { B } ( t )\tag{8}
$$

公式 (9)，L136-138：
$$
T _ { B } ( t ) = \frac { 1 } { \Delta } \times \int _ { t - \Delta } ^ { t } q ( i ) \times \frac { P _ { \mathrm { a v g } } } { C } \times d i\tag{9}
$$

公式 (10)，L158-160：
$$
\bar { N } _ { i } ( n ) = \omega N _ { i } ( n ) + ( 1 - \omega ) \bar { N } _ { i } ( n - 1 ) \quad i \in \{ A , B , C \}\tag{10}
$$

公式 (11)，L201-203：
$$
T T L \geq T T L _ { \mathrm { i n - o r d e r } }\tag{11}
$$

公式 (12)，L223-225：
$$
f = \frac { \left( \sum _ { i = 1 } ^ { n } x _ { i } \right) ^ { 2 } } { n \sum _ { i = 1 } ^ { n } x _ { i } ^ { 2 } }\tag{12}
$$

参数设定理由（逐字）：**L87** "To reflect the packet dropping probability in the setting of $\beta ,$ we set $\beta$ to $( 1 - p )$"；**L93** "As a remedy to this issue, the satellites are assumed to monitor their queues in a real time fashion. Therefore, is set to 1 ms throughout this paper."；**L95** "for the sake of the scheme simplicity, is set to half of $\beta$"。

### 3) 决策粒度与动作空间

- 粒度：邻星级（不是逐包）；路由表周期更新（**L128** "We assume that routing tables are updated periodically every interval time."，Δ=1 s 见 L221）。
- 动作空间：三态触发两类通告；对邻居的实际动作是"按比例 chi 削减发往该星的速率，并把 (1-chi) 部分改走已检索到的备用路径"（L63）。
- 多类时退化为按类优先级分配绕行比例（表 I，**L168**）：三行判据 X < c / c <= X < (b+c) / (b+c) <= X，对应 A 类恒 0，B/C 类 0 / X/c / (X-c)/b / All。
- 环路防护：**L128** "To cope with the issue of traffic redistribution cascading, we use a routing metric that instantly reflects both the one-way propagation delay and the instant queuing delay."

### 4) 是否含学习成分

**无。** §0.1 证据：reinforcement=0、\blearn=0、\btrain=0、supervised=0、reward=0、credit assignment=0；唯一 neural=1 为 L403 作者简历。全部参数由解析式 (1)-(7) 一次性设定，无用数据拟合参数的环节。

### 5) 负载与流量设置（仅作条件登记）

- **L213**："We consider an Iridium-like constellation. The constellation is formed of 66 satellites evenly and uniformly distributed over six orbits. ... Uplinks, downlinks, and ISLs are each given a capacity equal to 25 Mbps ... all links are presumed to be error-free. ... the average packet size is set to 1 KB ... Drop-Tail based buffers of lengths equal to 200 packets are used ..."（ISL 时延固定 20 ms）
- **L215**："we consider 600 non-persistent On-Off flows. The On/Off periods of the connections are derived from a Pareto distribution with a shape equal to 1.2. The average burst time and the average idle time are set to 200 ms. ... The sources send data at constant rates from within the range of 0.8 Mbps to 1.5 Mbps."
- **L219**：Table II 六大洲端点分布矩阵。
- **L221**：基线 DSP 与 CEMR；"the routing cost metrics of CEMR and ELB are updated every 1s interval of time $( \Delta = 1 \ : \mathrm { s } )$"。
- **L227**："Simulations are all run for 60s. ... satellites monitor their current queue occupancy in a real time fashion $( \delta = 1 \mathrm { m s } )$ . Finally, unless otherwise specified, the desired time for a satellite to reside in the Free state after a transition to the Busy state is set to 200 ms (e.g., deliberately set to ten times the ISL delay)."
- **L248**（多类）："The traffic percentages of traffic classes A, B, and C are set to 20%, 30%, and 50% ... The EWMA smoothing constant is set to 0.1."
- **L266**（TCP 实验）：单一 TCP 连接、最小跳数 3、美国区；ISL 时延取 "ms, 20 ms, and 25 ms"。

### 6) 可迁移点（能否搬进 RL 路由）

- **可搬**：ELB 的"状态迁移 → 邻星协同降速"是显式多智能体协同协议，可作 RL 的动作屏蔽/协调层：(a) (Qr, alpha, beta) 三态作 state 离散特征；(b) 公式 (7) 给出 chi 的可行域构造，可作连续动作的先验区间；(c) 公式 (9) 的 T_B(t) 是下一跳排队时延的短窗估计器，可直接作为 RL 的奖励时延项估计，无需学习。
- **障碍**：① 依赖邻星间状态交换（L63 的 warning/BSA），在部分可观测设定下是通信开销；② **L95 "for the sake of the scheme simplicity, is set to half of $\beta$"** 这类人工比值正是 RL 应当学掉的超参，构成"用学习替换启发式"的选题点；③ 公式 (1)(2) 需要 I、O、P_avg、d 的实时量。
- **已被本库采用？** 本批内可见的采用均为非学习论文：SBCHGBCP[31] L392、IXVSNEE3[23] L663+L525、BBNQ4EAQ[24] L469。T1 批次（B1-B4）是否采用 ELB 作基线，本会话无读权限，**未验证**（见 §13）。

---

## 2. TQF59BD7 — IDLB 分布式 SDN 负载均衡路由，605 行

### 1) 决策机制：谁在何时决定什么

- **谁**：**L123** "Typically a satellite near the center of a cluster takes on the role of cluster controller."；**L129** "Network information is aggregated at the dedicated SDN controller node of each cluster, enabling proactive and loadaware routing decisions. This autonomous, space-borne decision-making can provide improved reactivity, routing convergence and signaling overhead."
- **何时**：周期/事件更新；切换前 1 s 预置（**L137** "In our simulations, the process is triggered 1 s before a handover."）；新流到达时按 best-of-k 计算。
- **决定什么 L302**："The NHCN choice is QoS-dependent, similar to intracluster routing. Delay-critical traffic should follow the shortest path, while any low-load link is valid for best effort traffic. Notably, the choice should be randomized for low-priority flows to mitigate bottlenecks."
- **该文自己写出 Bellman 值函数（关键）L226**："To highlight why formulating a solution to this problem is intractable, we formulate a corresponding value function $\mathcal { V } _ { t } ( s _ { t } )$ for a state $s _ { t ^ { \star } }$ Besides the cost $C _ { t }$ of the current network state $s _ { t } ,$ and the flow requests $f _ { t } ,$ other aspects are relevant. ... Moreover, we assume stochastic traffic models. Therefore, future states are probabilistic in nature. An analytical formulation of suitable traffic models is exceedingly difficult. Therefore, the estimation of future states may be quite imprecise, limiting the effectiveness of approximate solutions."

### 2) 代价/阈值/更新函数（公式逐字）

公式 (1)，L216-218：
$$
u _ { t } ( i , j ) = \frac { f _ { t } ( i , j ) } { c _ { t } ( i , j ) } = \frac { \sum _ { ( i , j ) \in E } f _ { t } ^ { \kappa } ( i , j ) } { c _ { t } ( i , j ) }\tag{1}
$$

公式 (2)，L222-224：
$$
\operatorname* { m i n } _ { t } \operatorname* { m a x } _ { ( i , j ) \in E } u _ { t } ( i , j )\tag{2}
$$

公式 (3) Bellman 值函数，L228-230：
$$
\mathcal { V } _ { t } ( s _ { t } ) = \operatorname* { m i n } _ { f _ { t } } \big [ C _ { t } ( s _ { t } , f _ { t } ) + \mathbb { E } _ { \omega _ { t } } \big [ \mathcal { V } _ { t + 1 } ( s _ { t + 1 } ) | s _ { t } , f _ { t } \big ] \big ]\tag{3}
$$

公式 (4) 状态转移，L234-236：
$$
s _ { t + 1 } = \Phi ( s _ { t } , f _ { t } , \tau _ { t } , \omega _ { t } , E _ { t } )\tag{4}
$$

公式 (5)(6)(7) 三类 QoS 效用函数，L250-260：
$$
Y _ { 1 } ( p ) = ( L ( p ) + \epsilon ) ^ { - 1 }\tag{5}
$$
$$
Y _ { 2 } ( p ) = \psi _ { 2 } \cdot ( N _ { h o p s } ( p ) + \epsilon ) ^ { - 1 } + ( 1 - \psi _ { 2 } ) \cdot ( U ( p ) + \epsilon ) ^ { - 1 }\tag{6}
$$
$$
Y _ { 3 } ( p ) = \psi _ { 3 } \cdot ( N _ { h o p s } ( p ) + \epsilon ) ^ { - 1 } + ( 1 - \psi _ { 3 } ) \cdot ( U ( p ) + \epsilon ) ^ { - 1 }\tag{7}
$$

公式 (8) 路径利用率，L264-266：
$$
U ( p ) = \sum _ { ( i , j ) \in p } u _ { t } ( i , j )\tag{8}
$$

公式 (9)(10)(11) 复杂度，L270-284：
$$
\mathcal { T } _ { \mathrm { i n t r a , p a t h } } = \mathcal { O } ( | F | \cdot \left( | E | + | V | \log | V | + k \right) )\tag{9}
$$
$$
\mathcal { T } _ { \mathrm { i n t r a , d e c i s i o n } } = \mathcal { O } ( | \boldsymbol { F } | \cdot \boldsymbol { k } )\tag{10}
$$
$$
\mathcal { S } _ { \mathrm { i n t r a } } = \mathcal { O } ( | V | \cdot k )\tag{11}
$$

公式 (12)(13) 层间复杂度，L345-353：
$$
\mathcal { T } _ { \mathrm { i n t e r } } = \mathcal { O } \big ( | F | \cdot \big ( | \mathcal { E } | + | C | \log | C | + N _ { \mathrm { N H C N } } \big ) \big )\tag{12}
$$
$$
\mathcal { S } _ { \mathrm { i n t e r } } = \mathcal { O } ( | \mathcal { C } | ) + \mathcal { O } ( | N _ { \mathrm { N H C N } } | ) + \mathcal { O } ( | N _ { \mathrm { N H C N } } | ) = \mathcal { O } ( | N _ { \mathrm { N H C N } } | )\tag{13}
$$

公式 (14) 端到端时延分解，L403-405：
$$
L _ { t } ( \boldsymbol { p } ) = \sum _ { ( i , j ) \in \boldsymbol { p } } [ \mu s ] \underbrace { l _ { s } ( i ) } _ { \Uparrow } + \mu s ] \underbrace { l _ { r } ( i ) } _ { \Uparrow } + \mu s ] \underbrace { l _ { q , t } ( i ) } _ { \Uparrow } + m s ] \underbrace { l _ { p , t } ( i , j ) } _ { \Uparrow } ]\tag{14}
$$

公式 (15) 抖动，L411-413：
$$
J _ { \mathrm { i n s t , m a x } } = \operatorname* { m a x } _ { \rho \in \{ 2 , . . . , M \} } \Bigl | L _ { \rho } - L _ { \rho - 1 } \Bigr |\tag{15}
$$

公式 (16) 网络负载定义，L434-436：
$$
\mathrm { N e t w o r k 1 o a d } ( t ) = \frac { 1 } { T _ { \mathrm { w i n d o w } } } \sum _ { i } ^ { N _ { \mathrm { u p l i n k } } ( t ) } \zeta ( \rho _ { i } )\tag{16}
$$

Algorithm 1 关键行（逐字，L308-339）：L314 "4: candidates <- list()"；L317-318 "if (nhcn ∉ next clusters)∨ isl shutdown(ngbr, nhcn) ∨ isl_load_threshold(ngbr, nhcn, qos) then"；L321 "10: dist <- distance(nhcn, dst_cell)"；L322 "11: link_load <- isl_link_load(ngbr, nhcn)"；L323 "12: value <- cost(dist, link_load, qos)"；L328 "17: if to_randomize(qos) then"；L336 "25: return sample(candidates)"。

### 3) 决策粒度与动作空间

- 粒度显式二选一并给出对照：per-flow（F-IDLB）vs per-packet（P-IDLB）。**L290-294**："Stateful information about flows is not required, which can lead to a less complex routing logic." ... "If a load-balancing update is triggered, all packets toward a certain destination adjust their path accordingly. ... Nevertheless, periodic updates may lead to path instability for load-balanced traffic. Link load hysteresis and thresholds have to be implemented to mitigate potential route flapping."
- 动作空间：(a) 层内从 k 条候选中择优（效用由 (5)(6)(7) 决定）；(b) 层间 NHCN 选择，可 per-flow 或 per-area（**L359** "For the NHCN choice, per-flow and per-area decisions are possible."）。
- 平票处理 **L246**："If paths have equal cost, we apply a tie-breaking mechanism similar to Always-Go-Left [38]. A nonuniform choice with such an asymmetry has been shown to improve load balancing [38]."

### 4) 是否含学习成分

**无。** §0.1 证据：reinforcement=0；\blearn=1 但为 L516 未来工作；\btrain=1 但为 L82 "trains"；reward=0；credit assignment=0。权重 psi2、psi3 由人工设定，**L262**："The values are chosen to comply with the QoS requirements and the system scenario."

### 5) 负载与流量设置（仅作条件登记）

- **L17**："the protocol can handle network loads of up to 15.0 Gbps before quality of service compliance falls below 95%. Compared with the 7.6 Gbps supported by source-routing, this represents an increase of 97.4%."
- **L66** Table 1：SCN-288（12 面 x 24 星，780 km，86.4 度，每星 4 ISL，最大 ISL 速率 1000 Mbps，每 ISL 输出缓冲 0.36-1.08 Mbit）；SCN-1440（30 面 x 48 星，600 km）。
- **L76**："We assume an ISL data rate of 1 Gbps. Moreover, output buffers with a size of 0.36 Mbit are considered for each ISL, utilizing a first-in-first-out (FIFO) tail drop policy. With an assumed packet size of 1500 Byte, ... this means 30 packets can be buffered."
- **L88** Table 2：2000 活跃 UT、UT 最小仰角 30 度、每 UT 聚合 100 Mbps、39 GW、GW 最小仰角 20 度、馈电上行 5000 Mbps / 下行 1000 Mbps。
- **L109-113**：业务份额假设（best effort > 50%、时延敏感约 10%、中间类 30-40%）+ 信令专用缓冲优先调度。
- **L371**：会话模型（以 CBR 为主；开始时刻均匀采样，结束时刻指数分布；优先级按业务份额分配）。
- **L385** Table 4：QoS0 信令（<150 ms，<1e-6，<30 ms）、QoS1（150 ms，1e-2，<30 ms，10%）、QoS2（200 ms，1e-4，<50 ms，34%）、QoS3（300 ms，1e-6，N/A，56%）。
- **L430**："We assume that a QoS compliance of >95% is considered acceptable."；**L438** "in the presented simulations we assumed a general packet size of 12 kbit."；**L443** "Network load of 13.2 Gbps, which corresponds to 9500 sessions of an average duration of 100 s."
- **L449**：源路由 7.6 Gbps、12 节点簇 12.5 Gbps（+64.5%）、24 节点 15.0 Gbps（+97.4%）、48 节点 16.2 Gbps（+113.2%）；**L472** P-IDLB 在 8.6 Gbps 跌破 95%，F-IDLB 提升 45.3%；**L500** SCN-1440 考察 13.9-25.0 Gbps。

### 6) 可迁移点（能否搬进 RL 路由）

- **可搬（本批最强接口之一）**：论文自己写出 Bellman 最优性方程 (3) 与状态转移 (4)，RL 的状态/动作/奖励可逐项对齐：state s_t <- 链路利用率 u_t(i,j) + 流请求 f_t + 拓扑 E_t（公式 (4) 的显式自变量表）；action f_t <- 流分配；cost C_t(s_t,f_t) <- 公式 (2) 的 min-max 链路利用率 + 公式 (14) 的四项时延分解。公式 (2) 的 min-max 目标天然可转成负奖励。
- **可搬**：公式 (5)(6)(7) 的参数化效用函数 = 把 QoS 差异编码进动作价值的方式，可作 RL 多头输出（每 QoS 类一个头）的先验。
- **障碍（作者自陈）**：**L232** 的 E_{omega_t} 项不可解析（"An analytical formulation of suitable traffic models is exceedingly difficult"），正是用采样替代期望的动机；此外 **L379**（信令开销 <5%）与 **L382**（收敛时延 <130 ms）是硬约束，RL 推理时延必须纳入同一预算。
- **已被本库采用？** 未验证（见 §13）。备注：本篇是本批中**唯一非学习论文直接写出值函数与状态转移**的条目，T1 批次若用"MDP 化"论证，这是最直接的锚点。

---

## 3. SBCHGBCP — Segment Routing for TE and Fast Reroute，419 行

### 1) 决策机制：谁在何时决定什么

- **谁/何时（TE）L155**："To minimize the MSL in each slot, source routing with traffic splitting is adopted: At each source/edge node, the packets of a flow are distributed onto a set of delay-bounded, satellite-disjoint 2-segment paths."
- **谁/何时（故障）L221**："With fast rerouting, the failure detecting node immediately reroutes the affected traffic to a local backup path (if available) to bypass the failed component."
- **决定什么 L163**："When a packet of flow $( x , y )$ arrives at node x, a random path $p _ { k }$ is selected from Φ. We assume that the end node of the first segment in $p _ { k }$ is s. Segment list { s , y } is added to the packet for segment routing."
- **LFA+ 枚举 L227**："LFA enumerates all satellites and ground relays as the middle points forming a 2-segment backup path around the failed satellite. If there exist multiple backup paths for the same destination, the path with the shortest length would be chosen. ... It should be noted that even with $\mathrm { L F A + , }$ 100% protection coverage is not guaranteed."

### 2) 代价/阈值/更新函数（公式逐字）

星座方程 (1a)(1b)(1c)，L78-88：
$$
\begin{array} { l } { { x _ { i , j } ( t ) = R \left[ \cos \left( \displaystyle \frac { 2 \pi t } { T _ { 0 } } + \frac { 2 \pi j } { J } \right) \cos \left( \displaystyle \frac { 2 \pi i } { I } \right) \right. } } \\ { { \left. \quad - \cos ( \xi ) \mathrm { s i n } \left( \displaystyle \frac { 2 \pi t } { T _ { 0 } } + \frac { 2 \pi j } { J } \right) \sin \left( \displaystyle \frac { 2 \pi i } { I } \right) \right] , t \geq 0 , 0 \leq j < J , 0 \leq i < I } } \end{array}\tag{1a}
$$
$$
\begin{array} { l } { { y _ { i , j } ( t ) = R \left[ \cos \left( \displaystyle \frac { 2 \pi t } { T _ { 0 } } + \frac { 2 \pi j } { J } \right) \sin \left( \displaystyle \frac { 2 \pi i } { I } \right) \right. } } \\ { { \left. + \cos ( \xi ) \sin \left( \displaystyle \frac { 2 \pi t } { T _ { 0 } } + \frac { 2 \pi j } { J } \right) \cos \left( \displaystyle \frac { 2 \pi i } { I } \right) \right] , ~ t \geq 0 , 0 \leq j < J , 0 \leq i < I } } \end{array}\tag{1b}
$$
$$
z _ { i , j } ( t ) = R \mathrm { s i n } ( \xi ) \mathrm { s i n } \bigg ( \frac { 2 \pi t } { T _ { 0 } } + \frac { 2 \pi j } { J } \bigg ) , ~ t \geq 0 , 0 \leq j < J\tag{1c}
$$

公式 (2)，L92-94：
$$
T _ { 0 } = 2 \pi \sqrt { \frac { R ^ { 3 } } { G M } }\tag{2}
$$

公式 (3)（MSL 目标，正文在 L144，编号在第 149 行），L144-149。正文 L144 逐字："The MSL is defined as follows while assuming the traffic matrix is given. At time slot m with LEO-SC topology $G _ { m } ,$ let the set of incoming RF links at satellite s be $L _ { s }$ and the traffic load carried by link $l \in L _ { s }$ be $\eta _ { l } .$ With SPR, eta_l can be found. Accordingly, the traffic load carried by s is $\textstyle \sum _ { l \in L _ { s } } \eta _ { l } .$ The MSL in slot m is then max $\forall s \sum \forall l \in L _ { s } \eta _ { l } .$ Our TE goal is to design an efficient routing algorithm to minimize the MSL on a slot-by-slot basis, or"。公式本体与编号（L146-149）逐字：
$$
\min \max \sum _ { \forall l \in L _ { s } } \eta _ { l }
$$
（s 为下标行）
$$
(3)
$$

公式 (4)(5)（**DBTS+ 的核心代价与分流比**），L195-213：
$$
c _ { k } = 1 / h _ { k }\tag{4}
$$
$$
r _ { k } = \frac { c _ { k } } { \sum _ { \forall p _ { i } \in \Phi } c _ { i } }\tag{5}
$$

公式 (6) 流量加权 RTT，L252-254：
$$
\Theta = \frac { \sum _ { \boldsymbol { p } _ { i } \in \boldsymbol { P } } \boldsymbol { \theta } _ { i } \cdot \boldsymbol { f } _ { i } } { \sum _ { \boldsymbol { p } _ { i } \in \boldsymbol { P } } \boldsymbol { f } _ { i } }\tag{6}
$$

公式 (7)(8)，L260-268：
$$
\Psi = \frac { \sum _ { t _ { m } \in T } \sum _ { x \in \Psi , y \in \Psi , x \neq y } \vert P _ { x y } \vert } { T \cdot ( \vert \Phi \vert ^ { 2 } - \vert \Phi \vert ) }\tag{7}
$$
$$
H = \frac { \underset { t _ { m } \in T } { \sum } \frac { \sum _ { p _ { i } \in P } h _ { i } \cdot f _ { i } } { \sum _ { p _ { i } \in P } f _ { i } } } { T }\tag{8}
$$

公式 (9)(10) 保护覆盖率，L310-318：
$$
\delta = \frac { \sum _ { n \in N } \lvert P _ { n } ^ { * } \rvert } { \sum _ { n \in N } \lvert P _ { n } \rvert }\tag{9}
$$
$$
\delta ^ { * } = \frac { \sum _ { n \in N } \lvert P _ { n } ^ { * } \rvert - \lvert \varepsilon \rvert } { \sum _ { n \in N } \lvert P _ { n } \rvert - \lvert \varepsilon \rvert }\tag{10}
$$

阈值/约束（逐字）：**L155** "To limit the path length, a delay factor denoted by z is defined. We require that the delay of any candidate path must be within z times of the corresponding shortest path (In Section 7, simulation results for z in the range of [1,2] are obtained.)."；**L161-163** "the delay bound $D = z * d _ { 0 }$ is found."；**L155** "we only require candidate paths to be satellite-disjoint."；Algorithm 1 L178 "5:if $d _ { s } \leq D$ then"；L183 "10: if $p _ { i }$ is satellite-disjoint with all paths in Φ then"。

### 3) 决策粒度与动作空间

- 粒度：per-flow（每流一个段列表）；但**包级随机抽样**选路（L163）；备份为 per-node-per-destination（L223-225）。
- 动作空间：(a) 分流比向量 r_k（连续，公式 (5)）；(b) 备份下一跳 / 2 段备份路径（离散）。
- 约束（可迁移）**L155**："Under the assumption that congestion only occurs at satellites, we relax this requirement to allow path intersection at ground relays. In other words, we only require candidate paths to be satellite-disjoint."

### 4) 是否含学习成分

**无。** §0.1 证据：reinforcement=0、\blearn=0、\btrain=0、supervised=0、reward=0。TE 用 ILP/MILP 的启发式替代（L57 引用 K-MILP），故障恢复用预计算本地备份。

### 5) 负载与流量设置（仅作条件登记）

- **L111**："In this paper, our goal is to minimize the MSL, and we assume linking capacity is not the bottleneck."；**L113**：时隙 50 ms（同 [2]），保证每目的最多一次路由变化。
- **L73**：Starlink Phase 1：1584 星 @550 km、72 面、倾角 53 度、每面 22 星、单点波束、仰角 25 度、最大 RF 距离约 1123 km、footprint 半径 940 km。
- **L104**："Fig. 3 shows the relay placements with $\omega = 9 4 0$ km and $\rho = 4 .$ It can be shown that when $\rho \geq 1$ , Starlink can cover the whole Earth."
- **L235**："ground relays are placed with density ratio $\rho = 4 ,$ ... with a slot duration of 50 ms. Each simulation lasts 500 s, or 10000 time slots $( T = 1 0 0 0 0 )$ ."
- **L239-244**："we assume user terminals are evenly placed using the same ground relay placement model in Section 3.2, with a density ratio of $\rho = 1$ ... a total of 19 user terminals can be placed inside the USA border. So two 19 19 traffic matrices are constructed. In the uniform traffic matrix, all 361 entries/flows have the identical load of 1 unit (which can be regarded as one thousand packets per second here). In the non-uniform traffic matrix, each entry is randomly chosen between [0, 2]"
- **L246/248**：z=1.2/1.5/2/无穷 下 MSL 降约 20%（均匀）/ 15%（非均匀），D=1.5d0 最优；RTT 增加约 10%。
- **L293**：LFA/LFA+ 用 rho=1 或 4；**L320-324**：rho=1 时 LFA+ 比 LFA 高约 15%，delta 与 delta* 差约 25%；rho=4 时差降到 13%，delta* > 99%。

### 6) 可迁移点（能否搬进 RL 路由）

- **可搬（强）**：公式 (5) 的 r_k 是一个**显式的随机策略分布**（按 1/跳数归一化）。RL 可直接替换为学出来的 softmax 策略，并把 (4) 的 c_k = 1/h_k 作为初始策略先验（模仿学习热启动）。本批中**动作空间与 RL 策略输出形状完全同构**的一篇。
- **可搬**：公式 (9)(10) 的 delta/delta* 是可度量的鲁棒性指标，可作 RL 训练约束/评估指标。
- **障碍**：① **L239 作者自陈**："(Note that, the traffic matrix used here is only to evaluate our proposed algorithms. It does not mean that such a traffic matrix can be easily collected or even utilized to construct the corresponding forwarding table.)" —— 分流比依赖不可得的流量矩阵，正是用在线观测替代离线矩阵的切口；② **L113** 时隙 50 ms 准静态假设须与 RL 决策周期对齐；③ 论文假设容量非瓶颈（L111），与"拥挤/丢包"奖励设计冲突，搬运需重新引入容量约束。
- **已被本库采用？** 未验证（见 §13）。

---

## 4. X5K285MW — Analyzing Source-Routed Approaches，166 行

### 1) 决策机制：谁在何时决定什么

- **谁**：入口卫星。**L62**："source-routing enables efficient route computation and selection by the source node (in our scenarios the ingress satellite) based on the network's current state. Since the acquisition of load information results in a massive amount of signalling overhead, we assume that no link load information is present at the ingress node. However, the orbits of the satellites are highly predictable, so the ISL connectivity and propagation delays can be computed at the source node (also in advance)."
- **何时**：**L62** "These computations can be done periodically according to a timed handover strategy. In our tests, we use an Multiprotocol Label Switching (MPLS)-like approach: the calculated path is added to the header of the packet and popped at every hop."
- **决定什么（核心机制）L68**："By randomly choosing a path from the set of paths between the ingress and egress node, the load is intrinsically more balanced. This random path selection is flow-based in our analysis, to decrease jitter and the potential for packet reordering. Due to the grid structure of the mesh network, the set of minimum hop paths contains the fastest path in terms of propagation delay. As the paths of the minimum hop set have similar end-to-end propagation delay, they can be considered as viable alternatives."
- **路径集构造 L72**："utilizing a Breadth-First Search (BFS) path discovery was efficient enough to compute all paths with the minimum amount of hops on an off-the-shelf laptop in milliseconds"。
- **放宽最小跳约束（关键设计）L70**："Most importantly, it is possible to relax the minimum hop constraint (or propagation delay constraint), for instance by allowing paths with two or more additional hops. If the resulting end-to-end latency is compliant with the requirement of the QoS class, this relaxation can enable more intrinsic load-balancing."

### 2) 代价/阈值/更新函数

**本篇（166 行，全文通读）无编号公式、无 $$ 展示式**；定量关系全部以散文 + 表格给出，逐字登记：
- **L70 时延量级**："For the P-288 constellation, the intra-plane propagation delay is approximately 6 ms, and the maximum inter-plane propagation delay is approximately 8 ms. So, the maximum additional delay can be estimated easily based on the constellation design."
- **L92 负载估计（Little 定律）**："Using Little's law [12], we can estimate that there is an average network load of 9.72 Gbps for 70000 sessions and 16.67 Gbps for 120000 sessions. These values correspond to the average network load measured during the simulation."
- **L106 处理与头操作代价**："We assumed a processing time of 50 us for each packet processing operation. So, even if consider longer routes consisting of 20 hops, only an additional delay of 0.55 ms is observed. On the other hand, the amount of additional header operations increased linearly with the number of forwarded packets. At 3.5*10^6 packets, approximately 30.0*10^6 additional operations were required. So, around 8.6 header label operations per packet."
- **L106 信令开销**："in all test cases, the relative share of signalling overhead was below 1% of the overall traffic."
- **L78 无更新的论证**："However, if the ISL and ESL connectivity is predictable, no signalling is required. The ingress nodes adjust their headers in time."

### 3) 决策粒度与动作空间

- 粒度：per-flow（**L68** 明写 "This random path selection is flow-based"）。
- 动作空间：从最小跳路径集中均匀随机取 1 条（约等于均匀随机策略）；集合规模未给数，但 L94 "the route diversity is still remarkable"。

### 4) 是否含学习成分

**无。** §0.1 证据：reinforcement=0；\blearn=1（L74 旁述 "Alternatively, ML-based approaches have gathered interest, as they can approximate functions of optimization problems with lower computational complexity [19]."）；L165 为参考文献题名；\btrain=0、supervised=0、reward=0。

### 5) 负载与流量设置（仅作条件登记）

- **L54** Table 1：P-288 星座参数（表格 OCR 混排，可辨参数含 86.4、30、15、7.5、80、1000、0.36）；地面段 2000 UT / 39 GW / 10 度。
- **L81** Table 2 逐字："Simulation duration [s] Number of sessions Average session duration [s] Session data rate [Mbps] Session begin distribution | 7200 [30*10^3, 120*10^3] 100 10 uniform normal"。
- **L85**："The simulated traffic consists of individual sessions between randomly chosen terminals on ground with constant data rates. ... It is important to note, that 60% of traffic is still UT-to-GW and vice-versa. Since the GWs maintain their positions, links in their proximity remain potential hot spots."
- **L87**："The UT-to-UT traffic share assumption of 40% results in a more diverse ingress and egress node distribution."
- **L92**："the inherently more diverse routes for a uniform UT distribution enable higher loads. We can support approximately 64% more traffic (QoS compliance > 95%)."
- **L96**："By using a minimum hop metric instead of the propagation delay, and applying a random path selection per flow, we reduce the tendency for hot spots. Approximately 73% more traffic can be supported (QoS compliance > 95%)."
- **L104**："Looking at the end-to-end latency depicted in Fig. 5, we see that both approaches perform as anticipated, with the propagation delay-based SPF offering superior performance (on average 53.66 ms). Despite being marginally less efficient, the enhanced scheme still achieves comparable performance (on average 60.23 ms)."
- **L117 局限（逐字）**："In the proposed approach, load information is not used, leading to a path distribution that differs from active load-balancing. Sharing all link load details for every possible entry satellite is considered too expensive given the unpredictable traffic characteristics and the network topology. The physical size of these networks also leads to notable delays, limiting reactive load-balancing schemes."

### 6) 可迁移点（能否搬进 RL 路由）

- **可搬（定位为基线，不是贡献）**：该文是"零负载信息随机策略"的严格量化，给出两个可引用的门槛：**L96** 随机最小跳选路比时延优先 SPF 多支持约 **73%** 负载；**L92** 非均匀 UT 分布下增益从 64%（均匀）回落。任何 RL 路由方案若不能显著超过"均匀随机最小跳"这条线，贡献不成立。
- **障碍**：① 明确不使用链路负载信息（L117），RL 若需负载观测则状态空间与信令开销假设全变；② 随机化是 per-flow 一次性抽签，与 RL 逐决策周期更新不同构；③ **无任何代价函数公式**，迁移时需自行定义。
- **已被本库采用？** 本批内：TQF59BD7 引用它（L544 文献 [9]），并在 **L395** 的基线论证语境中使用："Thus, we focused on source routing, which represents a common baseline and mirrors the deterministic path computation used in many existing systems." —— 即**源路由基线在本库非学习批次中确实被采用**；RL 批次是否采用源路由基线，本会话无读权限（见 §13）。

## 5. AJJI57M9 — A Distributed Routing Algorithm for Datagram Traffic，431 行

### 1) 决策机制：谁在何时决定什么

- **谁/何时**：每颗卫星**逐包独立**决策。**L34**："The new routing algorithm is distributed, i.e., the routing decisions are made independently for each packet. The packets are routed between the logical locations, which are embodied by the closest satellites. The algorithm causes no overhead since the satellites do not exchange any topology information."
- **三阶段结构（核心机制）L192**："The next hop on the path is determined in three phases. In the direction estimation phase, possible next hops on the minimum-hop path are determined assuming that all ISLs have equal length. ... Thus, we have the direction enhancement phase, where we consider that the interplane ISLs have different lengths [(2)] and refine our decision made in the first phase about the next hop accordingly. The primary direction chosen in the direction enhancement phase ensures that the packets are routed on $P _ { S _ { 0 }  S _ { \it n } } ^ { * }$ . In the case of link congestions, the queueing delay has a larger effect on the end-to-end delay of the packets, hence, the packets sent on $P _ { S _ { 0 }  S _ { \eta } } ^ { * }$ may experience high delays. In order to reduce the negative effects of congested links, the routing decisions are revised in the congestion avoidance phase."
- **拥塞避免阈值规则 L271-281**：**L271** "Since no traffic load information is exchanged between the satellites, the congested links are detected by considering the fill levels of the output buffers. If the next hop of a packet is associated with an overloaded output buffer, i.e., if the output buffer has more than $\xi$ packets, then this situation is interpreted as a congestion occurrence. The main idea behind the congestion avoidance phase is to send the packets in their secondary directions, if the link in the primary direction is congested."；**L275** "2) If the secondary direction of a packet (either $d _ { v }$ or $d _ { h } )$ is zero, then the packet is sent in the primary direction, regardless of the number of the packets in the output buffers."；**L279** "4) If there are more than $\xi$ packets in the output buffer of the primary direction and less than packets in the output buffer of the secondary direction, then the packet is sent in the secondary direction. If output buffers of both primary and secondary directions have more than packets, then the packet is still sent in the primary direction."
- **故障绕行 L283-295**：**L283** "In order to reroute packets destined to the failed satellite, they are deflected into orthogonal directions."；**L289** "3) If the current satellite is in the polar region and the next satellite has failed, the packet is sent back to the previous hop, which is the only available direction."；**L295** "This rerouting strategy finds alternative routes for packets that would normally pass through a failed satellite. However, it does not guarantee that the packets are routed on a minimum-hop path."
- **环路避免 L281**："Also note that, to ensure the loop-free routing, the packets are never sent back to satellites where they came from, unless the current satellite is in one of the polar regions."

### 2) 代价/阈值/更新函数（公式逐字）

公式 (1)，L55-57：
$$
L _ { v } = \sqrt { 2 } R \sqrt { 1 - \cos \left( \frac { 3 6 0 ^ { \circ } } { M } \right) }\tag{1}
$$

公式 (2) 及其系数 alpha，L66-74：
$$
L _ { h } = \alpha \times \mathrm { c o s } ( \mathrm { l a t } )\tag{2}
$$
$$
\alpha = \sqrt { 2 } R \sqrt { 1 - \cos \left( \frac { 3 6 0 ^ { \circ } } { 2 \times N } \right) }
$$

公式 (3)(4)(5)，L94-112：
$$
P _ { S _ { 0 } }  S _ { n } = \{ l _ { S _ { 0 } S _ { 1 } } , l _ { S _ { 1 } S _ { 2 } } , . . . , l _ { S _ { n - 1 } S _ { n } } \}\tag{3}
$$
$$
D _ { P } = \sum _ { i = 0 } ^ { n - 1 } { \cal { D } } ( l _ { S _ { i } S _ { i + 1 } } )\tag{4}
$$
$$
P _ { S _ { 0 }  S _ { n } } ^ { * } = \arg \operatorname* { m i n } _ { P \in \{ P _ { S _ { 0 }  S _ { n } } \} } \{ D _ { P } \}\tag{5}
$$

公式 (6) **极区穿越判据 = 该文的阈值函数**，L156-158：
$$
n _ { h } > \operatorname* { m a x } _ { 0 \le a \le A } \left\{ \frac { N \cos ( \mathrm { l a t } _ { \mathrm { m i n } } ) + \frac { L _ { v } } { \alpha } ( 2 ( k - a ) + 1 ) } { \cos \left( \mathrm { l a t } + a \frac { 3 6 0 ^ { \circ } } { M } \right) + \cos ( \mathrm { l a t } _ { \mathrm { m i n } } ) } \right\}\tag{6}
$$

公式 (7)(9) 推导式，L164-166 / L180-182：
$$
\begin{array} { l } { { \displaystyle D _ { v } < D _ { h + a } } } \\ { { \displaystyle ( N - n _ { h } ) \alpha \cos ( \mathrm { l a t } ) + L _ { v } ( 2 k + 1 ) } } \\ { { \displaystyle ~ < n \alpha \cos \left( \mathrm { l a t } _ { \mathrm { m i n } } + a \frac { 3 6 0 ^ { \circ } } { M } \right) + 2 a L _ { v } . } } \end{array}\tag{7}
$$
$$
\begin{array} { c } { { D _ { h } < D _ { h + a } } } \\ { { \displaystyle n _ { h } \alpha \cos ( \mathrm { l a t } ) < n _ { h } \alpha \cos \left( \mathrm { l a t } + a \frac { 3 6 0 ^ { \circ } } { M } \right) + 2 a L _ { v } . } } \end{array}\tag{9}
$$

公式 (8) 同环判据，L174-176：
$$
n _ { h } < \operatorname* { m i n } _ { 1 \leq a \leq A } \left\{ \frac { 2 a L _ { v } } { \alpha } \frac { 1 } { \cos ( \mathrm { l a t } ) - \cos \left( \mathrm { l a t } + a \frac { 3 6 0 ^ { \circ } } { M } \right) } \right\} .\tag{8}
$$

公式 (10)(11) **动作空间的数学定义**，L199-207：
$$
d _ { v } = { \left\{ \begin{array} { l l } { + 1 , } & { { \mathrm { u p w a r d } } } \\ { 0 , } & { { \mathrm { n o ~ v e r t i c a l ~ m o v e m e n t } } } \\ { - 1 , } & { { \mathrm { d o w n w a r d } . } } \end{array} \right. }\tag{10}
$$
$$
d _ { h } = { \left\{ \begin{array} { l l } { + 1 , } & { { \mathrm { r i g h t } } } \\ { 0 , } & { { \mathrm { n o ~ h o ~ h o r i z o n t a l ~ m o v e m e n t } } } \\ { - 1 , } & { { \mathrm { l e f t . } } } \end{array} \right. }\tag{11}
$$

Table I / Table II 方向判定表（逐字结构，L213-217 / L241-243）：按"同一半球 / 不同半球"与 $p_{S_c}$ vs $p_{S_n}$、$s_{S_c}$ vs $s_{S_n}$ 的组合给出 $d_h, d_v$；半球判据 **L219-222**："If $s _ { S _ { c } } < M / 2$ and $s _ { S _ { \imath } } < M / 2$ with as the number of the satellites in a plane, then $S _ { c }$ and $S _ { n }$ are in the Eastern Hemisphere, on the same side of the seam."；"If $s _ { S _ { c } } \geq M / 2$ and $s _ { S _ { \imath } } \geq M / 2$ , then they both are in the Western Hemisphere, on the other side of the seam."；"Otherwise, $S _ { c }$ and $S _ { n }$ are on different sides of the seam."；hop 数计算 **L225-235**（a/b 两分支，逐字见原文）。

### 3) 决策粒度与动作空间

- 粒度：per-packet（L34）。
- 动作空间：本质上只有 2 个动作 —— primary 方向 / secondary 方向（各自是 (d_h,d_v) 组合之一）。**L275** 明确指出 secondary 可为 0（即不存在第二动作）。故障时扩展为"正交方向"（L293）。
- 方向由 Table I/II **确定性查表**决定，不含随机化 —— 这是与 §4（随机源路由）和 §3（分流比）的关键区别。

### 4) 是否含学习成分

**无。** §0.1 证据：本批 11 篇中该篇 reinforcement=0、\blearn=0、\btrain=0、supervised=0、neural=0、reward=0、penal*=0、counterfactual=0。全部判据为闭式不等式 (6)(8)。本批唯一完全不依赖任何"测量/反馈"的纯几何路由。

### 5) 负载与流量设置（仅作条件登记）

> **重要：本篇没有流量/负载设置。** 实验是**全源目的对**的拓扑与时延实验，不生成业务流、不设到达率、不设缓冲丢弃事件。

- **L324**："In all experiments, we generate a satellite constellation with $M \ : = \ : 1 2$ planes and $N = 2 4$ satellites in each plane. The planes as well as the satellites within a plane are separated from each other by $1 5 . 0 ^ { \circ }$ . The polar regions are defined as regions between the latitudes $7 5 . 0 ^ { \circ }$ and $9 0 . 0 ^ { \circ }$ ... In the first three experiments, we computed the average values for all possible source-destination pairs. We assume that each source-destination pair occurs with the same probability."
- **L305（关键硬约束）**："Simulation results have shown that deciding on the next hop of a packet takes $5 \mu \mathrm { s }$ with an Intel Pentium III 450 MHz processor. Hence, it is possible to use our algorithm for satellite networks with arbitrarily large number of satellites."
- **L307（存储）**："the decision map for that network can be generated and embedded into the routing code before deploying the satellites. Hence, no additional space for routing tables is needed."
- **L339**："In the worst case ( ) in Fig. 9, the average difference between our algorithm and Bellman's algorithm is less than 0.3%."；**L353** "The worst average deviation for our new algorithm is less than 0.3%. On the other hand, if we only use the direction estimation phase, the average percentage deviation is always greater than 8.1%."
- **L362**："When the failed satellite moves from the equator $( \mathrm { l a t } = 0 ^ { \circ } )$ toward the poles $( \mathrm { l a t } = 9 0 ^ { \circ } )$ , the average percentage deviation decreases from 6.25% to 4.4%. When the failed satellite is in the ring closest to the polar regions ..., the average deviation increases to 15%. Similarly, the average deviation is 16% when failure is inside the polar region."
- **L368/L379**：北美到中欧，Bellman 43.5-47.1 ms vs 本文 43.5-48 ms；偏差最大 0.9 ms 约 2%。

### 6) 可迁移点（能否搬进 RL 路由）

- **可搬（结构层面，本批最干净的动作空间定义）**：公式 (10)(11) 把动作定义为 d_v 属于 {-1,0,+1} 与 d_h 属于 {-1,0,+1}，再经 direction enhancement 收敛到 primary/secondary 二值 —— 把"几何可达方向"约化为离散动作集的完整范例。RL 可直接继承该动作定义（保证动作合法、环路可证），只把"选 primary 还是 secondary"换成学出来的策略。
- **可搬（观测设计）**：xi（输出缓冲包数阈值）是唯一的状态反馈，且**无需星间交换**（L269 "the satellites do not exchange traffic load information"）。这给出一个**完全局部可观**的 RL 状态设计，规避全局状态同步的开销论证难题。
- **障碍**：① "决策地图"是**离线预计算并烧入星载代码**（L307），与 RL 在线更新权重的范式冲突——搬运需先论证"何时更新决策地图"；② L281 的"不回头"环路保证在长出 RL 策略后可能失效，需重新证明；③ **本文无任何丢包/溢出/排队实验**，因此**不能**为 G-A 提供失败事件分解证据（对 §12 关键）。
- **已被本库采用？** 本批内未见直接引用；AF674CSF **L54** 引用的是 Ekici 的 VN 线（ref [11] 为 VN 机制，非本文的 datagram 路由）。T1 批次是否采用，本会话无读权限（见 §13）。

---

## 6. 9GPFG5U3 — Link-Identified Routing（LiR），712 行

### 1) 决策机制：谁在何时决定什么

- **谁/何时（源）L111**："The source satellite $S _ { 1 , 1 }$ calculates the path towards the destination satellite $S _ { 2 , 4 }$ via Dijkstra algorithm, and and obtains the path represented by four ISL identifiers {0x01, 0x05, 0x10, 0x13}. Afterwards, the source satellite $S _ { 1 , 1 }$ encodes the four ISL identifiers into the BF of the packets (to be delivered)."
- **中间节点 L113**："Upon receiving the packets, intermediate satellites determine the forwarding direction by checking whether the other three outgoing ISLs (except for the incoming ISL) are recorded in the in-packet BF."
- **重编码决策（核心机制）L384**："If a satellite finds itself not the destination and none of its outgoing ISLs are recorded in the BF, then this satellite is a re-encoding satellite. In this case, this satellite will lookup its routing table to find the path to the destination. Once the path is identified, the satellite calculates the segment of ISL identifiers it needs to encode based on the Algorithm 1. ... Finally, the satellite empties the in-packet BF and encodes these identifiers into the in-packet BF to guide packet forwarding towards the next re-encoding satellite."
- **按需故障机制 L394-396**：ODR "each satellite monitors the status of its ISLs in real time. When an intermediate satellite receives a packet that is about to be sent to a failed ISL according to the in-packet BF. ODR recalculates the route to the destination without this failed ISL and updates the in-packet BF."；ODD "Different from ODR scheme, ODD activates a predetermined equivalent path to bypass this failed ISL."
- **对照 LSA L407**："Under the LSA scheme, each satellite will generate hello packets according to a fixed time interval (e.g., 5 seconds for OSPF), which will be delivered to its neighbors."

### 2) 代价/阈值/更新函数（公式逐字）

公式 (1) BF 假阳性率，L96-98：
$$
p ( M , N , K ) = \left[ 1 - \left( 1 - \frac { 1 } { M } \right) ^ { K N } \right] ^ { K } .\tag{1}
$$

公式 (2) 错误转发开销闭式，L132-134：
$$
f _ { I F O } ( N , M , K ) = \frac { ( 2 N + 1 ) ( M + C ) p ( N , M , K ) } { 1 - 3 p ( N , M , K ) } ,\tag{2}
$$

公式 (3)(4)(5) 期望跳数递推，L140-160：
$$
f _ { I F O } ( N , M , K ) = ( 2 N + 1 ) ( M + C ) E ( p ) .\tag{3}
$$
$$
E ( p ) = ( 1 - p ) \cdot 0 + p \cdot [ 1 + 3 E ( p ) ] .\tag{4}
$$
$$
E ( p ) = { \frac { p } { 1 - 3 p } } .\tag{5}
$$

公式 (6) 正确转发开销，L173-175：
$$
f _ { C F O } ( N , M ) = M N .\tag{6}
$$

公式 (7) **总开销 = 两类开销相加**，L179-181：
$$
f _ { F O } ( N , M , K ) = f _ { I F O } ( N , M , K ) + f _ { C F O } ( N , M ) .\tag{7}
$$

公式 (8) 最优 BF 长度下的开销，L185-187：
$$
f ( N ) \triangleq \operatorname* { m i n } _ { M \geq 0 } \quad f _ { F O } ( N , M , K ) .\tag{8}
$$

公式 (9)(10) 编码策略空间，L267-275：
$$
\begin{array} { r } { \pmb { x } = \left( x _ { n } \in \{ 0 , 1 \} : x _ { 1 } = x _ { N + 1 } = 1 : \forall n \in \pmb { \mathscr { N } } \right) . } \end{array}\tag{9}
$$
$$
\begin{array} { r } { \mathcal { X } \triangleq \left( \pmb { x } \in \{ 0 , 1 \} ^ { N + 1 } : x _ { 1 } = x _ { N + 1 } = 1 \right) . } \end{array}\tag{10}
$$

公式 (11) 下一编码节点函数，L287-289：
$$
r _ { n } ( { \pmb x } ) \triangleq \arg \operatorname* { m i n } _ { i > n } \quad i \qquad\tag{11}
$$

公式 (12)(13) **单跳与总时间开销**，L295-303：
$$
\left[ { \frac { f ( r _ { n } ( { \pmb x } ) - n ) } { B } } + \tau \right] x _ { n } ,\tag{12}
$$
$$
\sum _ { n = 1 } ^ { N } \left[ \frac { f ( r _ { n } ( { \pmb x } ) - n ) } { B } + \tau \right] x _ { n } .\tag{13}
$$

公式 (14) 最优编码策略（Problem 1），L309-311：
$$
\pmb { x } ^ { \star } = \arg \operatorname* { m i n } \quad \sum _ { n = 1 } ^ { N } \left[ \frac { f ( r _ { n } ( \pmb { x } ) - n ) } { B } + \tau \right] x _ { n }\tag{14}
$$

公式 (15a)(15b)(15c) 子问题，L323-333：
$$
H ( i ) = \operatorname* { m i n } \quad \sum _ { n = 1 } ^ { i } \left[ { \frac { f ( r _ { n } ( x ) ) - n } { B } } + \tau \right] x _ { n }\tag{15a}
$$
$$
s . t . . \ x _ { i + 1 } = 1\tag{15b}
$$
$$
v a r . \quad \{ x _ { 1 } , x _ { 2 } , . . . , x _ { i } \} \in \{ 0 , 1 \} ^ { i } .\tag{15c}
$$

公式 (16)，L358-360：
$$
H ( N ) = \sum _ { n = 1 } ^ { N } \left[ \frac { f ( r _ { n } ( { \pmb x } ^ { \star } ) - n ) } { B } + \tau \right] .\tag{16}
$$

公式 (17) 递推关系（Lemma 1），L368-370：
$$
H ( i ) = \operatorname* { m i n } _ { 0 \leq q < i } \left\{ H ( q ) + \left[ { \frac { f ( i - q ) } { B } } + \tau \right] \right\} .\tag{17}
$$

Algorithm 1（逐字，L341-356）关键行：L345 "1 Initial $H ( 0 ) = 0 , P ( 0 ) = 0 , \bar { { \bf x } } ^ { \star } = ( \bar { { \bf 0 } } _ { N } , 1 )$"；L348 "4 Compute $\Psi ( j ) = H ( j ) + \left[ \frac { f ( i - j ) } { B } + \tau \right]$"；L349 "5 Find $j ^ { \star } = \arg$ min $\Psi ( j )$"；L351 "6 Set $H ( i ) = \Psi ( j )$ and $P ( i ) = j ^ { \star }$"。

**两类开销的定义（对 §12 关键）L121-123 逐字**：
- L121："Hence false positives will lead to incorrect forwardings towards unspecified ISLs. We let $f _ { I F O } ( \cdot )$ denote the incorrect forwarding overhead, which measures the data volume (in KB) delivered on the incorrect ISLs."
- L123："The BF-based forwarding utilizes the M-bit vector to record the ISL identifiers, which also increases the forward overhead along the correct path. We let $f _ { C F O } ( \cdot )$ denote the correct forwarding overhead, which measures the data volume (in KB) caused by the M-bit BF along the planned route."

### 3) 决策粒度与动作空间

- 粒度：逐跳转发决策（查 3 条出向 ISL）+ 逐包 BF；编码策略是 per-node 二值向量 x（N+1 维，公式 (9)(10)）。
- 动作空间：分层 —— (a) 源/重编码卫星的"编码什么"（x 向量，组合优化）；(b) 中间卫星的"往哪条出向 ISL 发"（查 BF，最多 3 选 1）。
- 代价函数 f(N) 是**对 BF 长度 M 的一维优化**（公式 (8) 的说明 L189："It is not difficult to derive (8), as it is a one-dimensional optimization."）。

### 4) 是否含学习成分

**无。** §0.1 证据：reinforcement=0、\blearn=0、\btrain=0、supervised=0、reward=0、credit assignment=0。全部为闭式分析与动态规划（Lemma 1 + Algorithm 1）。

### 5) 负载与流量设置（仅作条件登记）

- **L481**："Our packet-level experiments are based on the Iridium constellation, which is a typical polar constellation consisting of 66 LEO satellites at an altitude of 780km. The bandwidth of each ISL is set to 10Mbps, and the time consumption of BF replacement is set to $\tau = 1 0$ microseconds. Additionally, the effective data volume of each packet is $C = 1 ~ \mathrm { K B }$ ."
- **L509**：BF 长度 20-50 bits 扫描；**L513**：BF 长度集合 {20,21,22,23,25,27,30,35,40,45,50}（bit）。
- **L530**："we consider four pairs of two-way source-destination with overlapping ISLs. The sending rate of each source satellite is 1250 packets per second."；BF 长度 M 属于 {30,40,...,70}。
- **L550**：payload 1KB；源卫星发送速率 1000 packets per second。
- **L554**：ISL 失败率 {0%, 5%, 10%, 15%, 20%}；源卫星发送速率 100 packets per second；LSA hello 间隔 1 s。
- **L592**：one-to-N 模式，N 属于 {2,3,..6}；源卫星发送速率 1.6 Mbps。
- **L487**：ISL 失败/恢复事件按 Poisson 过程随机生成。

### 6) 可迁移点（能否搬进 RL 路由）

- **可搬**：公式 (14) 把"编码位置"作为决策变量、把公式 (13) 的 temporal overhead 作为目标 —— 与 RL 的"动作 -> 代价"结构一一对应；公式 (17) 的递推即动态规划最优子结构，可作为 RL 的 baseline 或奖励塑形参考。
- **可搬（对 G-A 最关键）**：公式 (2)(6)(7) 把**总转发开销按物理来源拆成两项**：f_IFO（BF 假阳性导致的错误转发）与 f_CFO（BF 位宽导致的正确路径开销），公式 (7) 再把两者**加和为单一标量**。**分解存在，但未分成独立学习通道/独立惩罚项**——见 §12 的判定。
- **障碍**：① f(N) 的期望值可解析但逐样本噪声大（BF 假阳性是随机事件）；② tau 与 B 需标定（L481 给出 tau=10us）；③ 该文的"动作"是静态编码策略而非逐包动作，与逐包 RL 的时间尺度不同构。

---

## 7. AF674CSF — Logic Path Identified Hierarchical Routing（LPIH），619 行

### 1) 决策机制：谁在何时决定什么

- **谁/何时（组内）L87**："Each satellite detects the connectivity of the ISL and ground-satellite link (GSL) status via the Hello mechanism, enabling dynamic detection of the physical link connection. To this end, each satellite constructs an inner-group routing table that records how to reach the satellites within the group."
- **谁/何时（组间）L89**："The management satellite constructs the adjacency relation between two adjacent satellite groups (denoted by PID) as well as a GS and its connected satellite group by collecting the link connectivity information (generated by border satellites). Accordingly, the management satellites in each group maintain a group-level topology for inter-group routing."
- **决定什么（PID 追加）L101**："when $S _ { 1 , 3 }$ receives the GET packet, it will forward the GET packet to the management satellite of Group A (i.e., $S _ { 3 , 2 }$) based on its inner-group routing table. Then, $S _ { 3 , 2 }$ appends PID1 to the end of GET packet and forwards it to one of egress border satellites (i.e., $S _ { 4 , 2 }$) associated with PID1 according to the inter-group content routing table"。
- **容错语义（PID 对多物理链路）L103**："if one of the ISLs fails (i.e., the red cross in Fig. 2), the intermediate satellite $S _ { 1 0 , 3 }$ could forward the DATA packet via alternative ISL to the nearest border satellite $S _ { 9 , 4 }$ , since PID2 represents the logic path and corresponds to multiple border satellites."
- **状态更新触发 L179**："a new inter-group LSA will be generated when the logic adjacency among the adjacent groups is changed (e.g., all of the inter-group ISLs are invalid at the same time)."
- **Algorithm 1（逐字，L199-228）**：L202 "1 if ISL state change detected then"；L206 "5 Flood the LSA within the satellite group"；L213 "10 if the satellite is a management satellite then"；L216 "12 if changed then"；L220 "16 Send inter-group LSA to all management satellites of adjacent groups"；L227 "21 Forward the inter-group LSA to all management satellites of adjacent groups"。

### 2) 代价/阈值/更新函数

**本篇（619 行，全文通读）无编号公式、无 $$ 展示式**；只有 Algorithm 1 伪码与两张路由表（L145 Fig.4、L175 Fig.5）。逐字登记其"代价"定义：
- **L173**："each entry of the inner-group routing table contains the following information: - NID of the destination satellite in this group, - NID of the next-hop satellite in this group, - content name (provided by the destination satellite), - and the cost metric (i.e., the hop to a destination satellite)."
- **L189**："- the content name, - the next-hop group, - the corresponding path identifier, - and the metric for the route to the destination group."
- 复杂度相关（间接）：L460 "LPIH announces the ISL state change within the satellite group instead of the entire constellation."；L462（路由表规模）"LPIH decouples inner-group routing from inter-group routing based on the path identifier (PID). Hence the reachability of inner-group nodes will be known only within the group instead of the entire network in IP-based ASER. Second, LPIH nodes maintain an inner-group routing table based on the NID instead of IP prefixes assigned to each ISL."

### 3) 决策粒度与动作空间

- 粒度：逐包（GET/DATA 两类包），但决策在**组级**（PID 序列）。
- 决策主体两类（**L121**）："Management Satellite: The management satellites record the content reachability information globally (i.e., where to find the content). Hence the management satellites can specify the next-hop group (indicated by the appended PID) during the GET packet forwarding."；**L123** "Forwarding Satellite: The other satellites are forwarding satellites that forward the packets according to the PID appended by the management satellites."
- 动作空间：组间 = 选下一跳组（PID）；组内 = 选下一跳卫星（NID）。**L346-348** 给出两种管理卫星配置：LPIH-1（单管理星）与 LPIH-A（全管理星）。
- 边距星选择：**L249** "the GET packet will be forwarded to the nearest border satellite (i.e., Step ❽)"；**L257** "if the satellite is one of the border satellites, then the DATA packet will be forwarded to the adjacent group."

### 4) 是否含学习成分

**无。** §0.1 证据：本篇 reinforcement=0、\blearn=0、\btrain=0、supervised=0、reward=0、credit assignment=0、penal*=0、counterfactual=0。本批 11 篇中该篇**全部学习类模式均为 0 命中（零散文干扰）**。

### 5) 负载与流量设置（仅作条件登记）

- **L305**："this module will randomly and independently generate the ISL failure (and recovery) events to simulate the topology dynamics. Specifically, we adopt the Poisson process as the ISL failure model with a specific rate lambda since it aligns with the assumption that link failures in satellite networks occur randomly and independently."
- **L312** Table I 星座参数：Telesat 351 星/27 面/13 星每面/98.98 度/1015 km；OneWeb 720/18/40/87.9/1200；Starlink-S1 720/36/20/70/570；Starlink-S2 1584/72/22/53/550；GW 2000/40/50/50/600。
- **L330**："we let p s denote a general group, where there are p orbital planes per group and s satellites on the orbital plane per group. Accordingly, the constellation is divided into several groups (i.e., {1, 4, 8, 12}) under corresponding grouping schemes (i.e., {18 40, 18 10, 9 10, 6 10})."
- **L334**："Let U x Py denote the traffic pattern, which represents that x users request the contents from y provider(s)."
- **L336**："Traffic load is characterized by the content request rate of each user, which is measured by the number of requests per second in our experiments."
- **L340**："Moreover, the payload of each DATA packet is 1 KB. The capacity of all links (i.e., ISLs and GSLs) is 10 Mbps, and each ISL's buffer size equals 500 packets."
- **L367**："the 6 10 grouping scheme of ASER and LPIH is adopted, i.e., 12 groups with 60 satellites per group. We focus on the average packet delivery ratio (PDR) and packet delay under different traffic patterns (i.e., U8P1, U8P2, U8P4, and U8P8). To simulate the topology dynamics, we randomly generate the ISL failure events according to the Poisson process with different rates (i.e., {0%, 1%,..., 20%})."
- **L435**："Now we evaluate how the traffic load affects the content delivery performance of LPIH routing. We set the ISL failure rate as 20%."
- 结果登记：L363（协议开销比 ASER 低最多 75.2%）、L408（U8P8 下 PDR 比 NLSR 高最多 105.3%）、L410（U8P1 下比 ASER/NLSR 高 155.6%/70.9%）、L439（重载下比 ASER/NLSR 高 266.9%/67.8%）。

### 6) 可迁移点（能否搬进 RL 路由）

- **可搬**：PID 的"**多条物理链路映射为单一逻辑标识**"是动作空间的**降维/抽象**手段，可直接用于 RL 的层次化动作（高层选 group/PID，低层选具体链路）；且在故障时天然提供"跨层替代动作"（L103），等价于 RL 中的 fallback 动作集。
- **可搬**：组内/组间路由解耦 + ISL 状态只在组内通告（L88-89）= **局部可观测 + 分层策略**的现成架构模板，可直接映射为 HRL（hierarchical RL）的两层策略。
- **障碍**：① **L496** 作者自陈未来工作："There are some open issues that need to be investigated in the future. First, we would study how to improve the network throughput via multipath content delivery. Second, it is also interesting to extend LPIH to the multi-shell constellation." —— 多径与多层均未做；② PID 语义是**内容路由**（GET/DATA），与目的地址路由不同构，迁移到 RL 路由需重定义动作语义；③ **本篇无任何代价函数公式**，奖励设计需完全自行定义。
- **已被本库采用？** 本批内：9KZDXPKC **L305** 引用它作为相关工作（ref [9]）；**L382** 还引用其姊妹篇："Q. Shan, Z. Wang, S. Zhang, Q. Meng, and H. Luo, 'Routing in leo satellite networks: How many link-state updates do we need?'"（该篇不在我这批）。

---

## 8. IXVSNEE3 — KNBG-MHCE + 星地协同路由，726 行

### 1) 决策机制：谁在何时决定什么

- **谁/何时**：每颗卫星逐包，源星预封装约束。**L29**："We propose a distributed satellite-terrestrial cooperative routing strategy based on the local load information and minimum end-to-end hop-count constraints given by KNBG-MHCE. To reduce the routing overhead, source routing paradigm is employed where the source node encapsulates the minimum end-to-end hop-count constraints derived from KNBG-MHCE into packets. Subsequently, each node can make distributed routing decisions with fast routing convergence by extracting the encapsulated information and jointly considering the load status of current satellite queues as well as next-hop node."
- **决定什么（三模式）L56**："Under the satellite-terrestrial cooperative routing framework, packets can be forwarded in three potential modes, which include inter-satellite forwarding, satellite-terrestrial forwarding, and terrestrial-satellite forwarding."；**L56** 还定义了两候选方向："In Walker Delta constellation, all potential routing directions can be categorized into four types, which involve top-right, bottom-right, top-left, and bottom-left [33]."
- **决策规则（阈值 + 硬切换）L301**："In our proposal, once queue saturation occurs in one candidate direction, next-hop satellite corresponding to the other candidate direction will be selected as the next-hop node. For example, if $Q _ { i } ^ { h } \ \geq \ B _ { s }$ or $Q _ { i + 1 } ^ { h } ~ \geq ~ B _ { s } ,$ and both $Q _ { i } ^ { v }$ and $Q _ { i + 1 } ^ { 2 }$ are less than $B _ { s }$ , we call the sending buffer queue is saturated in horizontal candidate forwarding direction. Then the satellite corresponding to vertical direction will be selected as the next-hop satellite. Otherwise, routing decisions are made by comparing $T _ { i } ^ { h }$ and $T _ { i } ^ { v }$ with threshold Γ"。
- **星地/地星两模式的门限触发 L307**："when a packet has been forwarded to satellite gateway $S G _ { k , i } ,$ if the load status of $S G _ { k , i }$'s downlink SGL does not exceed threshold $\Psi _ { d o w n }$ ground relay $G R _ { k }$ will be selected as the next-hop node, which is determined by KNBG-MHCE method. Alternatively, the packet will be first forwarded to another satellite gateway $S G _ { k , j }$ , and then forwarded from $S G _ { k , j }$ to $G R _ { k } .$"
- **Algorithm 3（逐字，L329-373）** 关键行：L332 "2: if $H _ { v } ^ { r } = 0 , H _ { h } ^ { r } \neq 0 \mathbf { o r } H _ { v } ^ { r } \neq 0 , H _ { h } ^ { r } = \mathbf { \bar { 0 } }$ then"；L335-336 "4: else if horizontal queue saturated or vertical queue saturated and the other queue is unsaturated then"；L340-341 "7: if $H _ { h } ^ { r } \leq H _ { v } ^ { r } , T _ { i } ^ { h } - T _ { i } ^ { v } \leq \Gamma \ \mathbf { o r } \ H _ { v } ^ { r } \leq H _ { h } ^ { r } , T _ { i } ^ { v } - T _ { i } ^ { h } > \Gamma$ then"；L353-355 "15: if the queuing delay of $S G _ { k , i }$'s downlink SGL does not exceed $\Psi _ { d o w n }$ then 16: $G R _ { k }$ is selected as the next-hop node."。

### 2) 代价/阈值/更新函数（公式逐字）

公式 (1)(2)，L69-75：
$$
\left\{ \begin{array} { l l } { \lambda _ { l e f t } = P \cdot \Delta \Omega , } \\ { \lambda _ { r i g h t } = ( P + 1 ) \cdot \Delta \Omega . } \end{array} \right.\tag{1}
$$
$$
\left\{ \begin{array} { l } { \varphi _ { l o w e r } = \arcsin \bigl ( \sin \alpha \sin \bigl ( \frac { \pi } { 2 } - \frac { 2 \pi } { M } ( M - R ) \bigr ) \bigr ) , } \\ { \varphi _ { u p p e r } = \arcsin \bigl ( \sin \alpha \sin \bigl ( \frac { \pi } { 2 } - \frac { 2 \pi } { M } ( M - R - 1 ) \bigr ) \bigr ) . } \end{array} \right.\tag{2}
$$

公式 (3)(4)(5)，L83-93：
$$
\begin{array} { r } { u _ { m , t } = \left\{ \begin{array} { l l } { \mathrm { a r c s i n } \frac { \sin \varphi _ { m , t } } { \sin \alpha } , } & { \mathrm { a s c e n d i n g ~ s a t e l l i t e } , } \\ { \frac { \varphi _ { m , t } } { | \varphi _ { m , t } | } \pi - \mathrm { a r c s i n } \frac { \sin \varphi _ { m , t } } { \sin \alpha } , } & { \mathrm { d e s c e n d i n g ~ s a t e l l i t e } . } \end{array} \right. } \end{array}\tag{3}
$$
$$
L _ { n , t } = \mathbb { N } \big ( \lambda _ { m , t } - \xi ( u _ { m , t } ) \big ) .\tag{4}
$$
$$
\xi ( u _ { m , t } ) = \left\{ \begin{array} { l l } { \mathrm { a r c t a n } ( \mathrm { c o s } \alpha \mathrm { t a n } u _ { m , t } ) , } & { \mathrm { a s c e n d i n g ~ s a t e l l i t e } , } \\ { \mathrm { a r c t a n } ( \mathrm { c o s } \alpha \mathrm { t a n } u _ { m , t } ) + \pi , } & { \mathrm { d e s c e n d i n g ~ s a t e l l i t e } . } \end{array} \right.\tag{5}
$$

公式 (6)(7)(8)(9)，L97-115：
$$
P _ { n , t } = \lfloor \frac { L _ { n , t } } { \Delta \Omega } \rfloor , \quad n = 1 , 2 , \cdots , N .\tag{6}
$$
$$
R _ { m , t } = \big \lfloor \frac { { u _ { m , t } - \pi / 2 } } { \Delta \Phi } \big \rfloor , \quad m = 1 , 2 , \cdots , M ,\tag{7}
$$
$$
\mathrm { w h e r e ~ } u _ { m , t } = \left\{ \begin{array} { l l } { u _ { m , t } , } & { \mathrm { i f ~ } u _ { m , t } \geq \pi / 2 , } \\ { u _ { m , t } + 2 \pi , } & { \mathrm { i f ~ } u _ { m , t } < \pi / 2 . } \end{array} \right.\tag{8}
$$
$$
\left\{ \begin{array} { l l } { \mathcal { U } _ { u } ( { \pmb u } _ { m , t } ) = ( R _ { m , t } + 1 ) \Delta \Phi , } \\ { \mathcal { U } _ { l } ( { \pmb u } _ { m , t } ) = R _ { m , t } \Delta \Phi . } \end{array} \right.\tag{9}
$$

公式 (10)(11a)(11b)(12)(13)(14a)(14b) 最小跳数估计，L132-160：
$$
\begin{array} { r } { H _ { \mathrm { m i n } } = \operatorname* { m i n } \{ H _ { h } ^ { \right. } + H _ { v } ^ { \right. \uparrow } , H _ { h } ^ { \right. } + H _ { v } ^ { \right. \downarrow } , } \\ { H _ { h } ^ { \left. } + H _ { v } ^ { \left. \uparrow } , H _ { h } ^ { \left. } + H _ { v } ^ { \left. \downarrow } \} . } \end{array}\tag{10}
$$
$$
\left\{ \begin{array} { c } { H _ { h } ^ { \right. } = \mathrm { m o d } \big ( N - ( P _ { n 1 } - P _ { n 2 } ) , N \big ) , } \\ { H _ { h } ^ { \left. \right.} = \mathrm { m o d } \big ( N + ( P _ { n 1 } - P _ { n 2 } ) , N \big ) . } \end{array}\tag{11a}
$$
（11b 为编号行，正文见 L136）
$$
\mathbb { R } ( H _ { h } , R _ { m 1 } ) = \left\{ \begin{array} { l l } { R _ { m 1 } , } & { H _ { h } ^ {  } \Delta f \leq \mathcal { U } _ { u p p e r } ( u _ { m , t } ) , } \\ { \mathrm { m o d } \bigg ( R _ { m 1 } + \lceil \frac { H _ { h } ^ {  } \Delta f - | \mathcal { U } _ { u p p e r } ( u _ { m , t } ) - u _ { m , t } | } { \Delta \Phi } \rceil , } & { H _ { h } ^ {  } \Delta f > \mathcal { U } _ { u p p e r } ( u _ { m , t } ) . } \end{array}  , \right.\tag{13}
$$
$$
H _ { v } ^ { \uparrow } = \mathrm { m o d } \bigl ( M + \bigl ( R _ { m 2 } - \mathbb { R } ( H _ { h } , R _ { m 1 } ) \bigr ) , M \bigr ) ,\tag{14a}
$$
$$
H _ { v } ^ { \downarrow } = \mathrm { m o d } \big ( M - \big ( R _ { m 2 } - \mathbb { R } ( H _ { h } , R _ { m 1 } ) \big ) , M \big ) .\tag{14b}
$$

公式 (15)(16)(17)(18)(19)(20)(21) 关键节点提取，L180-222：
$$
\beta = \frac { \pi } { 2 } - \theta - \gamma , \quad \gamma = \arcsin \frac { r _ { e } \cdot \sin ( \theta + \frac { \pi } { 2 } ) } { h + r _ { e } } .\tag{15}
$$
$$
\Delta P = 2 \cdot \big \lceil \frac { 1 8 0 \cdot r _ { s } } { \pi \cdot r _ { e } \cos ( \varphi _ { G R _ { k } } ) \Delta \Omega } \big \rceil .\tag{16}
$$
$$
\Delta R = 2 \cdot \big \lceil \frac { 1 8 0 \cdot r _ { s } } { \pi \cdot r _ { e } \cdot \Delta h _ { m i n } } \big \rceil .\tag{17}
$$
$$
\Delta h = | f _ { R _ { m }  \varphi } ( R _ { m } + 1 ) - f _ { R _ { m }  \varphi } ( R _ { m } ) | .\tag{18}
$$
$$
f _ { R _ { m }  \varphi } ( r ) = \arcsin \bigl ( \sin ( \alpha ) \mathrm { s i n } \bigl ( \frac { \pi } { 2 } - \frac { 2 \pi } { M } \cdot ( M - r ) \bigr ) \bigr ) ,\tag{19}
$$
$$
\nabla f _ { R _ { m }  \varphi } ( r ) = \frac { \frac { 2 \pi } { M } \sin ( \alpha ) \mathrm { c o s } ( \frac \pi 2 - \frac { 2 \pi } { M } \cdot ( M - r ) ) } { \sqrt { 1 - \sin ^ { 2 } ( \alpha ) \mathrm { c o s } ^ { 2 } ( \frac { 2 \pi } { M } \cdot ( M - r ) ) } } .\tag{20}
$$
$$
h _ { m i n } = \alpha - \arcsin \bigl ( \sin ( \alpha ) \sin \bigl ( \frac { \pi } { 2 } - \frac { 2 \pi } { M } \cdot ( M - 1 ) \bigr ) \bigr ) .\tag{21}
$$

公式 (22)(23) 搜索范围，L274-276（逐字见原文）。

**公式 (24)(25)(26)(27) —— 本篇的代价函数与阈值（最关键）**，L297-319：
$$
\left\{ \begin{array} { l l } { T _ { i } ^ { h } = \left( Q _ { i , h } + Q _ { i + 1 } ^ { h } \right) / R _ { I S L } , } \\ { T _ { i } ^ { v } = \left( Q _ { i , v } + Q _ { i + 1 } ^ { v } \right) / R _ { I S L } . } \end{array} \right.\tag{24}
$$
$$
\Gamma = \eta _ { 1 } \times \big ( \frac { 2 B _ { s } } { R _ { I S L } } - \mathrm { m a x } \big ( T _ { i } ^ { h } , T _ { i } ^ { v } \big ) \big ) .\tag{25}
$$
$$
\Psi _ { d o w n } = \eta _ { 2 } \times \tau R _ { I S L } + \eta _ { 3 } \times \tau R _ { S G L } ^ { d o w n } .\tag{26}
$$
$$
\Psi _ { u p } = \eta _ { 4 } \times \tau R _ { I S L } + \eta _ { 5 } \times \tau R _ { S G L } ^ { u p } .\tag{27}
$$

公式 (28)-(45)（复杂度、生存概率、充要条件、指标定义），L377-605：
$$
\rho = \frac { f _ { 2 } ( K \mathcal { X } ) } { f _ { 1 } ( K \mathcal { X } ) } = \frac { K S + K \frac { \mathcal { X } ! } { 2 ( \mathcal { X } - 2 ) ! } + S ^ { 2 } } { ( K + 0 . 5 ) K \mathcal { X } ^ { 2 } + 5 . 5 K \mathcal { X } } .\tag{28}
$$
$$
P _ { 2 } = \left\{ \begin{array} { l l } { p ^ { H _ { h } - H _ { v } } \big ( p q ( 2 - p q ) \big ) ^ { H _ { v } } , } & { \mathrm { i f ~ } H _ { h } \geq H _ { v } , } \\ { q ^ { H _ { v } - H _ { h } } \big ( p q ( 2 - p q ) \big ) ^ { H _ { h } } , } & { \mathrm { i f ~ } H _ { h } < H _ { v } . } \end{array} \right.\tag{29}
$$
$$
N _ { p } = \frac { H _ { \operatorname* { m i n } } ! } { H _ { v } ! \cdot ( H _ { \operatorname* { m i n } } - H _ { v } ) ! } .\tag{30}
$$
$$
P _ { I n t e r S a t } = \sum _ { m = 1 } ^ { N _ { P } } ( - 1 ) ^ { m - 1 } \sum _ { 1 \le a _ { i } < a _ { i + 1 } \le N _ { p } } \bigg | P \Big ( \bigcap _ { a _ { 1 } } ^ { a _ { m } } A _ { a _ { i } } \Big ) \bigg | .\tag{31}
$$
$$
P _ { 1 } = p ^ { 3 } q ^ { 2 } , \ P _ { 2 } = p ^ { 3 } q ^ { 2 } ( 2 - p q ) ^ { 2 } , \ P _ { 3 } = p q ( 2 - p q ) r ^ { 2 } .\tag{32}
$$
$$
\mathbb H _ { h } L _ { h \operatorname* { m i n } } > \mathbb H _ { v } L _ { v } .\tag{33}
$$
$$
s . t . \quad \left\{ \begin{array} { l } { \mathbb H _ { h } > \mathbb H _ { v } , } \\ { \mathbb H _ { h } \in \left[ 0 , \lfloor \frac { N } { 2 } \rfloor \right] , } \\ { \mathbb H _ { v } \in \left[ 0 , \mathcal Z \right] . } \end{array} \right.\tag{34}
$$
$$
\mathcal { Z } = \left\{ \begin{array} { l l } { \mathrm { m o d } ( F , M ) , } & { \mathrm { i f ~ } \mathrm { m o d } \bigl ( F , M \bigr ) \leq \bigl \lfloor \frac { M } { 2 } \bigr \rfloor , } \\ { M - \mathrm { m o d } ( F , M ) , } & { \mathrm { i f ~ } \mathrm { m o d } \bigl ( F , M \bigr ) > \bigl \lfloor \frac { M } { 2 } \bigr \rfloor . } \end{array} \right.\tag{35}
$$
$$
L _ { h \operatorname* { m i n } } > \frac { \mathbb { H } _ { v } ^ { \operatorname* { m a x } } } { \mathbb { H } _ { v } ^ { \operatorname* { m a x } } + 1 } L _ { v } .\tag{36}
$$
$$
\mathbb { H } _ { v } ^ { \operatorname* { m a x } } = \operatorname* { m i n } \Bigl \{ \mathcal { Z } , \bigl \lfloor \frac { N } { 2 } \bigr \rfloor - 1 \Bigr \} .\tag{37}
$$
$$
\mathbb { H } _ { v } L _ { v } > \mathbb { H } _ { h } L _ { h \operatorname* { m i n } } .\tag{38}
$$
$$
s . t . \quad \left\{ \begin{array} { l } { \mathbb { H } _ { v } > \mathbb { H } _ { h } , } \\ { \mathbb { H } _ { h } \in \left[ 0 , \lfloor \frac { N } { 2 } \rfloor \right] , } \\ { \mathbb { H } _ { v } \in \left[ 0 , \mathcal Z \right] . } \end{array} \right.\tag{39}
$$
$$
L _ { v } > \frac { \mathbb { H } _ { h } ^ { \operatorname* { m a x } } } { \mathbb { H } _ { h } ^ { \operatorname* { m a x } } + 1 } L _ { h \operatorname* { m i n } } .\tag{40}
$$
$$
\mathbb { H } _ { h } ^ { \operatorname* { m a x } } = \operatorname* { m i n } \Bigl \{ \mathcal { Z } - 1 , \bigl \lfloor \frac { N } { 2 } \bigr \rfloor \Bigr \} .\tag{41}
$$
$$
L _ { h \mathrm { m i n } } = 2 \cdot ( r _ { e } + h ) \cdot \sin ( \frac { \Gamma _ { \mathrm { m i n } } } { 2 } ) , ~ L _ { v } = 2 \cdot \sin ( \frac { \pi } { M } ) \cdot ( r _ { e } + h ) .\tag{42}
$$
$$
\left\{ \begin{array} { l l } { \Gamma _ { \mathrm { m i n } } = \operatorname { a r c c o s } \left( \frac { 1 - \cos \gamma } { 2 } - \frac { 1 + \cos \gamma } { 2 } \cos \left( 2 \kappa - \Delta f \right) \right) , } \\ { \gamma = \operatorname { a r c c o s } \left( 1 - \frac { \left( \sin \alpha \sin \frac { 2 \pi } { N } \right) ^ { 2 } } { 1 + \cos \frac { 2 \pi } { N } } \right) , } \\ { \kappa = \arcsin \left( \sqrt { \frac { \left( 1 + \cos \frac { 2 \pi } { N } \right) ^ { 2 } } { 2 + 2 \cos \frac { 2 \pi } { N } - \left( \sin \alpha \sin \frac { 2 \pi } { N } \right) ^ { 2 } } } \right) . } \end{array} \right.\tag{43}
$$
$$
\mathrm { T h r o u g h p u t } = \operatorname* { l i m } _ { T \to \infty } { \frac { \sum _ { t = 0 } ^ { T } { \mathrm { P a c k e t s ~ r e a c h i n g ~ d e s t i n a t i o n s } } } { T } } .\tag{44}
$$
$$
{ \mathrm { P a c k e t ~ D r o p ~ R a t e } } = { \frac { \mathrm { N u m b e r ~ o f ~ d r o p p e d ~ p a c k e t s } } { \mathrm { N u m b e r ~ o f ~ g e n e r a t e d ~ p a c k e t s } } } .\tag{45}
$$

### 3) 决策粒度与动作空间

- 粒度：**逐包、分布式**（源星封装约束，L29/L484）。**L484**："To reduce routing overhead, we employ source routing paradigm, executing KNBG-MHCE only at source satellite and encapsulating its results into packets as shown in Fig. 8. Subsequent nodes can make distributed routing decisions by extracting the encapsulated information"。
- 动作空间：**2 个**（水平候选方向 / 垂直候选方向），且当某方向剩余跳数为 0 时退化为单动作（L332）；星地/地星模式下额外有"直接落地/改走另一网关星"两个选择（L307/L315）。
- 硬化规则：队列饱和（Q >= B_s）时**强制**切换到另一方向（L301），这是硬约束而非软代价。

### 4) 是否含学习成分

**无。** §0.1 证据：reinforcement=0、\blearn=0、\btrain=0、supervised=0、reward=0、credit assignment=0。阈值 Γ、Ψ_down、Ψ_up 全由解析式 (25)(26)(27) 给出，平滑因子 eta1-eta5 由人工设定（**L301** "and $\eta _ { 1 }$ is a smoothing factor"；**L309** "where $\eta _ { 2 }$ and $\eta _ { 3 }$ are smoothing factors and τ is time interval"；**L315** "$\eta _ { 4 }$ and $\eta _ { 5 }$ are both smoothing factors"）。

### 5) 负载与流量设置（仅作条件登记）

- **L500**："extensive experiments are conducted under Starlink phase I constellation, and $N _ { 0 }$ in Section V-A is set to 4. Key node based graphs are regenerated every 600ms, and all simulations last 20.51s with the time interval τ of 1 ms [25]. ... we deploy a total of 25 ground relays in two phases ... 12 ground relays are deployed in the first phase, while other 13 ground relays are further added in the second phase"。
- **L509** Table II 逐字："Configuration of constellations The size of sending buffer queue $B _ { s }$ The size of public waiting buffer queue $B _ { w }$ The rate of ISL $R _ { I S L }$ The rate of SGL $R _ { S G L }$ in Ka band | 1584/72/39/550/53° 5Mbit, Ka / 10Mbit, laser 40Mbit, Ka / 1Gbit, laser 25Mbps, Ka / 2.5Gbps, laser 1.5Gbps downlink / 2Gbps uplink 5Gbps downlink / 5Gbps uplink"
- **L525**："In both systems, we set 3000 non-persistent on-off flows similar to [23], and employ Ka band SGLs along with our proposal as uniform routing strategy."
- **L539**："$R _ { p a c } ^ { t h }$ is about 150Mbps in the system with Ka band ISLs, and with the increase of link rate, $R _ { p a c } ^ { t h }$ grows to 350Mbps in system with laser band ISLs"；"$B _ { s } ^ { t h }$ becomes 2.5 Mbit in laser system"。
- **L545**："end-to-end delay refers to the sum of propagation delay and queuing delay. Packet forwarding rate refers to the number of packets forwarded by a satellite per unit of time"。
- **L549**："our proposal can reduce the average end-to-end delay by more than 200ms in all cases."；**L607** "our proposal can improve system throughput by more than 116.99% in system with Ka band ISLs and over 104.73% in system with laser band ISLs. Furthermore, in contrast to Type II strategies, our proposal can improve system throughput with the increase of 13.29% and 32.5%, respectively."
- **L609**：包转发速率加倍时丢包率显著下降、吞吐上界提升近 200%。

### 6) 可迁移点（能否搬进 RL 路由）

- **可搬（本批最强可操作件）**：公式 (24)(25) 的 Γ 阈值 —— 它是一个"**用剩余队列空间把两条候选动作的代价差归一化**"的门限：Gamma = eta1 * (2B_s/R_ISL - max(T^h, T^v))。可直接搬成 RL 动作选择的**安全门/动作屏蔽（action masking）**：当 T^h - T^v <= Γ 时强制走某方向。两个观测量（各向队列占用、ISL 速率）都是仿真平台现成可得的。
- **可搬**：公式 (30)(31) 的路径数组合与 inclusion-exclusion 生存概率，可作为 RL 探索多样性的**理论下界**或评估指标（衡量策略是否真的利用了多径）。
- **障碍**：① Γ 需要人工调 eta1（L301），这与"让学习替代调参"的动机一致，但 RL 需要把 eta1 纳入动作或超参搜索；② 动作空间只有 2 个方向，若扩展到 4 邻居需重新推导 Hop-count 约束（公式 (10)-(14)）；③ **L340** 其"仅静态拓扑"的近亲问题在本篇以"每 600ms 重建 KNBG"回避，RL 的决策频率需与之一致。
- **已被本库采用？** 本批内：该篇引用 JP79GMZS[23]（L663）与 TLR[25]（L667）；未验证 T1 批次是否采用其 Γ 阈值。


## 9. 9KZDXPKC — How to Route CUBIC and BBR Packets in Space（DB-R），336 行

### 1) 决策机制：谁在何时决定什么

- **谁/何时（默认路由）L190**："By definition, default routing is a node's default choice when it is going to forward packets but finds no routing entry matched. We leverage default routing to address the temporarily missing routing entry caused by GSL handover. Specifically, when a satellite is going to disconnect the old GSL, it will add a default routing entry to its routing table. After the old GSL disconnects, this default routing entry is used to guide the packets to the new GSL."
- **何时（切换检测）L196**："To achieve seamless GSL handover, the GS usually establishes a new GSL with a latter satellite before disconnecting the old GSL with the former satellite [23]. The establishment of a new GSL is actually a signal of the upcoming GSL handover. It could be viewed as the trigger event of configuring default routing for the former satellite."
- **检测判据 L202**："Given the above preparations, if a new routing entry appears in a satellite's routing table, then the satellite will check whether the destination address of the new routing entry has the same prefix as any IP address in its GSL Array."；**L204** "If yes, then this means that the satellite has detected the trigger event of configuring default routing. It would immediately add a default routing entry in its routing table"。
- **出接口选择 L216**："Upon detecting the trigger event of configuring default routing, the satellite needs to determine the outgoing interface of the default routing entry. Specifically, the satellite associated with the old GSL will calculate the shortest path towards the satellite associated with the new GSL. ... Then a new routing entry with the outgoing interface of eth will be loaded into the routing table of satellite $S _ { a } .$ When satellite $S _ { a }$ detects the newly added routing entry meets the condition specified in Section IV-A3, it would configure a default routing entry with the same outgoing interface as the new routing entry, i.e., eth2."
- **备份路由 L230**："Backup routing can significantly improve the availability of LEO satellite networks. Specifically, each satellite has four interfaces (i.e., four ISLs) that reach the destination with different costs. The interface of the smallest cost has the highest preference, and is also the main route. All the others are backup routes for this satellite. Moreover, the four entries are sorted according to their costs so that the routing entry with the minimal cost has the highest priority."
- **故障时实际动作 L232**："When the ISL between satellite $S _ { a }$ and satellite $S _ { d }$ becomes faulty (i.e., the interface eth2 of satellite $S _ { a }$ becomes unavailable), all the routing entries associated with the interface eth2 immediately disappear from the routing table of satellite $S _ { a } .$ Before routing convergence, satellite $S _ { a }$ will forward the packets with destination 173.18.0.26 via the interface eth1."

### 2) 代价/阈值/更新函数（公式逐字）

注：本篇的公式全部属于**被保护的 TCP 拥塞控制**（CUBIC/BBR），DB-R 本身不含代价函数公式 —— 这一点对判断其"是否学习"很关键。

公式 (1)(2) CUBIC，L96-104：
$$
\mathrm { c w n d } _ { n e w } = \mathrm { c w n d } _ { o l d } \cdot \beta ,\tag{1}
$$
$$
W ( t ) = C \cdot ( t - K ) ^ { 3 } + W _ { \mathrm { m a x } } ,\tag{2}
$$

公式 (3)(4) BBR，L138-148：
$$
\mathbf { B W } = \frac { D e l i \nu e r e d - p a c k e t . d e l i \nu e r e d } { N o w - p a c k e t . d e l i \nu e r e d \_ t i m e } .\tag{3}
$$
$$
P a c i n g \_ r a t e = B W \_ m a x \cdot p a c i n g \_ g a i n ,\tag{4}
$$
（**L150**："where pacing gain is periodically changing and takes values in {1.25, 0.75, 1, 1, 1, 1, 1, 1, ...}."）

**DB-R 的一切实质性判据都是定性的**，逐字：
- **L188（时间尺度阈值）**："Despite the packet loss, the time period when the routing entry is missing will not be long. According to our experiments on virtual network emulation environment, such a period lasts for about tens of milliseconds."
- **L198（前缀判据）**："The IP addresses of all GSLs associated to the same GS have the same IP address prefix."
- **L200（GSL 数组）**："Each satellite maintains a GSL Array that records the IP addresses of all the GSLs in use for this satellite."
- **L208（实例）**："the IP addresses of GSLs connected with GS have the same prefix of 172.18.10.64/26 and the IP address of the GSL_new is 172.18.10.80."

### 3) 决策粒度与动作空间

- 粒度：**每路由表项（前缀级）与每接口**；触发是事件驱动（新路由项出现 / 接口失效）。
- 动作空间：(a) 是否插入 default routing entry（二值）；(b) default entry 的出接口（从最短路径算出，非枚举）；(c) 四个备份项的优先级顺序（由 cost 排序，L230）。**动作空间极小且无需搜索**。
- 实现载体：Linux kernel 5.19.0 + FRR（**L57** "We implement DB-R mechanism in Linux kernel 5.19.0. Specifically, we add the default routing entry to the routing table when an upcoming GSL handover is detected. We also improve the process for calculating the shortest path in OSPF, which generates backup routing entries in the routing table."）。

### 4) 是否含学习成分

**无。** §0.1 证据：本篇 reinforcement=0、\blearn=0、\btrain=0、supervised=0、reward=0、credit assignment=0。CUBIC 是丢包驱动、BBR 是带宽估计驱动，**两者都不是学习算法**；DB-R 是纯路由机制，无任何参数拟合。

> **但本篇是 §12 对抗性问题的头号候选**：它把"同一失败事件（丢包）"按**物理原因**拆成两条互不相同的处理通路（GSL handover -> default routing；ISL failure -> backup routing）。详见 §12。

### 5) 负载与流量设置（仅作条件登记）

- **L238**："Our experiments are based on Iridium constellation. It is a walker-star constellation that consists of 66 satellites on 6 orbital planes. The orbital altitude is 780 km. We set the bandwidth of GSL to 200 Mbps, the bandwidth of ISL to 1000 Mbps. We consider two GSes located in Shanghai and Los Angeles, respectively."
- **L88**：Starlink 典型参数用于 pass duration 说明（h=550 km，beta=25 度）；Sydney 到 London 的会话时长分布（Fig. 3）。
- **L130**："ISL failure also causes packet loss. CUBIC takes packet loss as the congestion signal, thus reducing CWND as shown by the red curve in Fig. 6(b)."；RTT 从 130 ms 增至 170 ms。
- **L170**：BBR 的 BW 由 80 Mbps 跌至再升至 180 Mbps（GSL 切换）；由 50 Mbps 再升至 150 Mbps（ISL 故障）。
- **L246**："When GSL handover occurs at the 95-th second, the blue curve suddenly drops to 120 Mbps, and then gradually increases to 160 Mbps. However, the red curve directly drops to 160 Mbps due to the increment in end-to-end propagation delay."
- **L248**："When ISL failure occurs at the 50-th second, the blue curve suddenly drops to 46 Mbps, then gradually increases to 150 Mbps. However, the red curve directly drops to 150 Mbps because of the increment in end-to-end propagation delay."（ISL 故障持续 5 秒）
- **L252**："We randomly generate flows of different sizes according to Poisson process. We focus on the average throughput, average FCT, and average slowdown during 1 second after GSL handover or ISL failure."
- **L53（影响量级）**："Experiments show that GSL handover and ISL failure can reduce the average throughput of CUBIC (and BBR, respectively) up to 67% (and 41%, respectively)."；**L59**（DB-R 增益）"DB-R reduces the average flow completion time of CUBIC (and BBR, respectively) by up to 52% (and 42%, respectively) compared to OSPF."；**L262**（吞吐增益）"up to 37% (and 18%, respectively)"。
- **L132**："Note that GSL handover enlarges the FCT and slowdown up to 5x."；**L172** "Fig. 7 indicates that GSL handover increases the FCT and slowdown up to 4.9x. Fig. 8 shows that ISL failure enlarges the FCT and slowdown up to 5x."

### 6) 可迁移点（能否搬进 RL 路由）

- **可搬（对 G-A 最关键，见 §12）**：DB-R 提供了一台**"失败原因标注器"**：GSL 切换可由"新路由项的前缀命中 GSL Array"检测（L198-204），ISL 失效可由"接口不可用"检测（L220/L230）。RL 若要把失败按原因分通道，可以直接复用这套标签来源，而不必自己发明检测逻辑。
- **可搬**：default routing 的"无匹配表项时的兜底动作"= RL 的 **fallback / 安全动作**，可避免策略在未知状态下的空动作；备份项按 cost 排序 = 天然的**动作优先级先验**。
- **障碍**：① 依赖 Linux kernel 与 FRR 的具体实现（L57），迁移到仿真平台需重写；② DB-R 的目标是"不丢包"，而 RL 路由的目标通常是吞吐/时延，奖励构造不同；③ 论文只测两个 GS（上海/洛杉矶）与 66 星 Iridium（L238），规模与 RL 常用 mega-constellation 场景不匹配。
- **已被本库采用？** 本批内：9KZDXPKC 引用 AF674CSF[9]（L305）与 LiR 线[10]（L307），并引用 OpenSN[20]（L329）作为仿真平台。未验证 T1 批次是否采用 DB-R。

---

## 10. BBNQ4EAQ — Temporal Netgrid Model / NSR，495 行

### 1) 决策机制：谁在何时决定什么

- **谁/何时（状态收集）L207**："The beacon protocol is proposed by taking into account two factors. One is to adapt the dynamic environments in satellite networks, such as unpredictable link interruption and node failure. The other is to diminish the influence of the accuracy sacrifice in TNM. In short, the basic idea of the beacon protocol is to collect status (e.g., queuing delay, transmission rate and so on) of neighbor satellites periodically for routing decision."
- **存活判定 L209**："In order to detect link interruption and node failure, alive neighbor v will be deleted after three broadcast periods (i.e, 3T^b) unless a new beacon packet broadcasted by v is received."
- **谁/何时（路由计算）L221**："Let time $t _ { s }$ denote route start time, which is decided by the packet arrival time. NSR focuses on non-empty netgrids where satellite nodes locate and NSR only considers the network topology at time $t _ { s }$ when the algorithm executes. Since the beacon protocol can only collect neighbor nodes information, the transmission rate $R$ in line 8 of Algorithm 3 is estimated. That is to say, the optimal routing path output by NSR only outputs the estimated shortest path, thus each intermediate node could adjust routing path according to the real-time status of neighbor satellites."
- **决定什么 L223**："Here, we use greedy approach to find the shortest path from source netgrid $\mathcal { C } _ { s }$ ... to destination netgrid $\mathcal { C } _ { d }$ ... Note that the shortest path found by NSR is composed by netgrids."
- **未走通时的重算 L365**："NSR will be firstly executed at the source node to find the optimal routing path. If multi-choice satellites in the path are unreachable, NSR will be executed at intermediate node to find another routing path."
- **Algorithm 1（逐字，L235-265）** 关键行：L256-258 "12 Neighbor($\mathcal { C } ^ { \prime }$) <- Find all non-empty neighbor netgrids of $\mathcal { C } ^ { \prime }$ within effective netgrids at $t _ { s } ;$ 13 Update $Q$ and $\mu$ by executing Algorithm 3"；L260-263 "15 Extract netgrid $\mathcal { C } _ { m i n }$ which has minimum time($\mathcal { C } _ { m i n }$) from $Q$; 16 Add $\mathcal { C } _ { m i n }$ into $S ^ { * } ;$ 17 Add {time($\mathcal { C } _ { m i n }$), $p(\mathcal { C } _ { m i n }$)} into $\mathcal { R }$"。

### 2) 代价/阈值/更新函数（公式逐字）

公式 (1)(2) 网格表定义，L77-85：
$$
\mathcal { P } _ { v , i } = \{ v , \mathcal { T } _ { v } , ( t _ { v , i } ^ { e } , t _ { v , i } ^ { l } ) \} , v \in V , t _ { v , i } ^ { e } , t _ { v , i } ^ { l } \in [ 0 , \mathcal { T } _ { v } ] .\tag{1}
$$
$$
\begin{array} { r } { \mathcal { C } _ { i } = \{ \mathcal { P } _ { v , i } | v \in V _ { i } \} , i \in [ 1 , K ] , } \end{array}\tag{2}
$$

公式 (3) 分层网格边长，L118-120：
$$
L _ { l } = 2 L _ { l + 1 } = \frac { \sqrt { 3 } } { 3 \cdot 2 ^ { l } } R _ { a } , l \in \mathbb { Z } ,\tag{3}
$$

Definition 2（描述精度），L134：
$$
\eta _ { l } = \frac { V _ { l } ^ { c u b e s } } { \frac { 4 } { 3 } \pi R _ { a } ^ { 3 } }
$$

公式 (4)(5)（最大层与最大格数），L180-186：
$$
m _ { n } ^ { * } = a r g m i n [ f _ { l } ( n , m _ { n } ) ] , f _ { l } ( n , m _ { n } ) > 0 ,\tag{4}
$$
$$
n ^ { * } = a r g m i n [ f _ { l } ( n , 0 ) ] , f _ { l } ( n , m _ { n } ) > 0 ,\tag{5}
$$
（辅助式 **L175**："$f _ { l } ( n , m _ { n } ) = \sqrt { R _ { a } ^ { 2 } - \sqrt { ( m _ { n } + 1 ) \cdot L _ { l } ^ { 2 } } } - \left( 2 ^ { l } + n - \frac 1 2 \right) \cdot L _ { l }$"）

**代价函数（逐字，Algorithm 3 第 8 行）L326**：
$$
\mathrm{time}( e ( \mathcal { C } ^ { \prime } , \mathcal { C } _ { n } ) ) = \frac { | D | } { R ( \mathcal { C } ^ { \prime } , \mathcal { C } _ { n } ) } + T _ { p } ( e ( \mathcal { C } ^ { \prime } , \mathcal { C } _ { n } ) ) ;
$$
**沿用状态（L327）**："9 $t i m e ( \mathcal { C } _ { n } ) = t i m e ( \mathcal { C } ^ { \prime } ) + t i m e ( e ( \mathcal { C } ^ { \prime } , \mathcal { C } _ { n } ) ) ;$"
**含等待的扩展式（讨论节）L342**："the transmission time calculation in line 8 of Algorithm 3 will be changed to time$( e ( \mathcal { C } ^ { \prime } , \mathcal { C } _ { n } ) ) = T _ { w } ( C _ { n } ) + \frac { | D | } { R ( \mathcal { C } ^ { \prime } , \mathcal { C } _ { n } ) } + T _ { p } ( e ( \mathcal { C } ^ { \prime } , \mathcal { C } _ { n } ) )$"。
**直连情形（Algorithm 2 第 4 行）L287**："Put $time ( \mathcal { C } _ { i } ) = \frac { | D | } { R ^ { b } ( \mathcal { C } _ { s } , \mathcal { C } ^ { \prime } ) }$ and $p ( \mathcal { C } ^ { \prime } ) = e ( \mathcal { C } _ { s } , \mathcal { C } ^ { \prime } )$ into $\mathcal { R }$"。
**复杂度（对比）L309/L311**："the computation complexity of NSR is $\mathcal { O } ( \overline { { { N } } } _ { n } ^ { \ 2 } + \overline { { E } } _ { n } )$"；"There are two main operations in the algorithm, 'Extract-min' and 'Relaxation', and the typical computation complexity is $\mathcal { O } ( N ^ { 2 } + E )$ [29]."；**L309 降维关键式**："We assume that $\overline { { N } } _ { n } = \frac { N } { W _ { l } } , \overline { { E } } _ { n } = \frac { E } { W _ { l } ^ { \prime } }$"。

### 3) 决策粒度与动作空间

- 粒度：**逐跳**（每个中间节点可重算，L221），但每个 hop 的候选是"**邻居网格集合**"而非单个卫星。
- **L273（动作空间的多选性质，逐字）**："It should be emphasized that the shortest path $p *$ found by NSR from $\mathcal { C } _ { s }$ to ${ \mathcal { C } } _ { d } ,$ is composed by netgrids. Therefore, if ${ \mathcal { C } } _ { m }$ is an intermediate netgrid of $p *$ , then all satellite nodes contained in $\mathcal { C } _ { m }$ can be selected as an intermediate node during the transmission, which makes each hop in the routing path contain multi-choice."
- 动作集合大小：由网格内卫星数决定（**L103**："If we assume $F$ as the average number of effective netgrids, then the complexity of neighbor nodes searching operation will be $\mathcal { O } ( F l o g ( \overline { { N } } ) _ { . } )$"）。

### 4) 是否含学习成分

**无。** §0.1 证据：reinforcement=0、\blearn=0、\btrain=0、supervised=0、reward=0、credit assignment=0、penal*=0、counterfactual=0。本批 11 篇中该篇同样**零散文干扰**。全部为图搜索 + 精度分析。

### 5) 负载与流量设置（仅作条件登记）

- **L353** Table II 逐字："Type of Satellites LEO / Altitude 780km / Number of Planes 6 / Eccentricity 0 / Inclination 86.4 degrees / TTL of Packet 10min / Transmission Rate 100kbps / Total Generated Packets 1000 / Communication Range 5000km / Simulator Update Interval 0.1s"
- **L363**："Iridium-like constellation is adopted to construct satellite networks and the software and hardware configurations of simulation platform are: Core i3-4150 CPU, 3.50 GHz, 12G RAM, O.S. Windows 10 Professional 64 bits. The orbit calculation model is two-body model. Since we consider random traffic transmission situation, users' requests in the simulation are generated randomly. We also assume that all satellites have one omni-directional antenna, and each satellite can only connect to one satellite at the same time."
- **L375**："we repeat the same simulation 10 times with different 1000 generated packets for each point in routing performance comparisons, and we plot the average value with 95% confidence interval in Fig. 6 and Fig. 7."
- **L379**："When the packet size is exceeded 300 KB, the performance of NSR in partition layer 2 degrades compared with NSR in partition layer 3, this is due to the fact that TNM sacrifices more topology information with the lower number of partition layers."
- **L390**："We depict the performance of all routing schemes under random ISL interruption situation as shown in Fig. 7."；**L397**："Fig. 7. Performance comparison versus different interruption probability among five routing schemes (Packet Size = 150 KB)."
- 基线登记（L365-373）：NSR / TSR / CGR / TBR / EASR 五种。

### 6) 可迁移点（能否搬进 RL 路由）

- **可搬（状态表示降维）**：网格抽象把状态空间从 N 个卫星压缩到 N/W_l 个格子（L309），复杂度由 O(N^2+E) 降到 O((N/W_l)^2 + E/W_l')。这对 RL 的**状态表示/图神经网络节点数**直接有用，且论文给出了精度-代价权衡的解析式（公式 (3) + Definition 2 + Proposition 1，L140）。
- **可搬（POMDP 证据）**：L221 明说"**only estimated shortest path can be obtained since each satellite only collects status of neighbor satellites**"——这是**局部可观测**的直接文本证据，可作为"LEO 路由是 POMDP"的引文。
- **障碍**：① **L340 自陈局限**："In the proposed NSR algorithm, the optimal path is only considered in static topology. ... However, when route time becomes long enough, the shortest path obtained from NSR might be non-optimal."；② beacon 只能收集邻居状态，RL 的观测构造必须与此一致，否则状态假设失真；③ 每跳多选（L273）意味着动作空间是**集合**，RL 需要一个额外的"选哪颗卫星"子策略。
- **已被本库采用？** 本批内：BBNQ4EAQ 引用 JP79GMZS[24]（L469）与 TLR[14]（L449）；**IXVSNEE3 L655 引用本篇**（ref [19]："J. Li, H. Lu, K. Xue et al., 'Temporal netgrid model-based dynamic routing in large-scale small satellite networks,' IEEE Trans. Veh. Technol., vol. 68, no. 6, pp. 6009-6021, Apr. 2019."）→ 即本批内部的**双向引用**（IXVSNEE3 引用 BBNQ4EAQ，且 IXVSNEE3 的 RTPG 思路明显承袭 TNM）。

---

## 11. VFS59FHI — Load-Balancing Routing Based on Segment Routing（回传），365 行

### 1) 决策机制：谁在何时决定什么

- **谁/何时**：集中算路 + 分区规则。**L23**："Light and heavy load zones are dynamically divided according to the relative position relationship between gateways and the reverse slot, and different routing rules are adopted in different zones to improve network throughput and avoid congestion. The pre-balancing shortest path algorithm is used in the light load zone, and the minimum weight routing is based on congestion index when the traffic is converged to the heavy load zone."
- **决定什么（轻载区）L136**："In the light load zone, routing paths of satellite nodes will pass through the heavy load zone, and must include one of outermost circle satellite nodes inside the heavy load zone, recorded as outermost nodes. Then, outermost nodes are responsible for subsequent routing. The shortest path algorithm is used to generate minimum spanning tree (MST) because the traffic of light load zone is at a low level, which can improve the delay performance and reduce SR overhead. A pre-equalization is adopted in the light load zone to avoid excessive traffic selecting the same outermost node that causes unexpected congestion."
- **权重预均衡（更新函数）L136**："The number of outermost node i occupied is assumed to $x _ { i } ,$ and the weight of links is adjusted to $( 0 . 5 + 0 . 1 \times x _ { i } )$ where 0.5 is the initial link weight in the network, and 0.1 is used to reduce the order of magnitude for $x _ { i }$ avoiding over-adjustment."
- **决定什么（重载区）L138**："In order to save resources and maximize throughput, the priority of each satellite node in the heavy load is sorted from high to low with traffic from large to small considering the difference in traffic carried by each satellite. Satellite nodes route in order of priority from high to low, so that the larger the traffic, the shorter the path, which can reduce the resource occupation."
- **拒绝（动作空间的一部分）L165**："If the satellite node has no path to the central station, the traffic carried by the node is rejected and lost."
- **分区边界 L134**："The size $( y _ { \mathrm { n } } , \ y _ { \mathrm { m } } )$ of heavy load zone is defined as $y _ { \mathrm { n } }$ orbits and $y _ { \mathrm { m } }$ satellite nodes on each orbit within heavy load zone, while the light load zone has $( N \ - \ y _ { \mathrm { n } } \times y _ { \mathrm { m } } )$ satellite nodes."

### 2) 代价/阈值/更新函数（公式逐字）

公式 (1)，L66-68：
$$
\lambda ( e , P ) = { \left\{ \begin{array} { l l } { 1 , } & { e \in P } \\ { 0 , } & { e \not \in P } \end{array} \right. }\tag{1}
$$

公式 (2)(3) 链路承载流量，L81-89：
$$
F [ e _ { i j } ^ { ( \mathrm { I S L } ) } ] = u \times [ \sum _ { k = 0 } ^ { N - 1 } f ^ { ( k ) } \times \lambda ( e _ { i j } ^ { ( \mathrm { I S L } ) } , { \pmb { P } } _ { \mathrm { I S L } } ^ { ( k ) } ) ]\tag{2}
$$
$$
F [ e _ { i j } ^ { ( \mathrm { { F } } ) } ] = u \times [ \sum _ { k = 0 } ^ { N - 1 } f ^ { ( k ) } \times \lambda ( e _ { i j } ^ { ( \mathrm { { F } } ) } , { \pmb { P } } _ { \mathrm { { F } } } ^ { ( k ) } ) ]\tag{3}
$$

问题定义的约束，L111-117：
$$
F [ e _ { i j } ^ { \mathrm { ( I S L ) } } ] \le B _ { \mathrm { I S L } } , i \neq j , i , j \in [ 0 , N - 1 ]
$$
$$
F [ e _ { i j } ^ { \mathrm { ( F ) } } ] \leq B _ { \mathrm { F } } , , i \in [ 0 , N - 1 ] , j \in [ 0 , X - 1 ]
$$

**公式 (4)(5)(6)(7) —— 本篇的核心代价函数**，L142-163：
$$
c ( e ) = { \cal F } ^ { ( e ) } \big / _ { r ( e ) } , r ( e ) = b ( e ) - { \cal F } ( e )\tag{4}
$$
$$
w ( e ) = 0 . 0 1 + c ( e ) = 0 . 0 1 + { } ^ { F ( e ) } \big / { r ( e ) }\tag{5}
$$
$$
w ( P ) = \sum _ { e \in P } w ( e )\tag{6}
$$
$$
r ( P ) = { \underset { e \in P } { m i n } } r ( e )\tag{7}
$$

**拥堵指数的语义（逐字）L140**："The larger c(e) is, the more congested the link is. c(e) = 无穷 when r(e) = 0 and $b ( e ) ~ = ~ { \cal F } ( e )$ which presents that link e has no available bandwidth and is open. On the other hand, c(e) = 0 when r(e) = b(e) and $F ( e ) = 0$ , which presents that the full bandwidth of link e is available. Compared with link utilization F(e)/b(e), c(e) is more monotonously incremental to F(e) and more sensitive to load change. c(e) would increases sharply if the traffic is too larger which is good to balance the network load."

指标定义 (8)-(12)，L203-277：
$$
R = { \frac { \displaystyle \sum _ { a \in R _ { S } } f ^ { ( a ) } \times u } { \displaystyle \sum _ { k = 0 } f ^ { ( k ) } \times u } } = { \frac { \displaystyle \sum _ { a \in R _ { S } } f ^ { ( a ) } } { \displaystyle \sum _ { k = 0 } f ^ { ( k ) } } } \times 1 0 0 \%\tag{8}
$$
$$
T = \sum _ { b \in S _ { \mathrm { S } } } f ^ { ( b ) } \times u\tag{9}
$$
$$
U _ { \mathrm { e } } = ( { m a x \frac { F ( e ) } { e \in E } } ) \times 1 0 0 \%\tag{10}
$$
$$
D _ { T } = \frac { \displaystyle { \sum _ { b \in S _ { S } } d ^ { ( b ) } } } { | S _ { S } | }\tag{11}
$$
$$
J _ { T } = \frac { { \displaystyle \sum _ { b \in { \cal S } _ { S } } j _ { T } ^ { ( b ) } } } { | { \cal S } _ { S } | }\tag{12}
$$

复杂度（无编号，L169 逐字）："The complexity of routing in the light load zone is $O ( ( N + X + 1 ) ^ { 2 } ) = O ( N ^ { 2 } )$ , while the complexity of routing in the heavy load zone is $O ( ( y _ { \mathrm { n } } \times y _ { \mathrm { m } } ) \times ( y _ { \mathrm { n } } \times y _ { \mathrm { m } } + X + 1 ) ^ { 2 } ) = O ( ( y _ { \mathrm { n } } \times y _ { \mathrm { m } } ) ^ { 3 } ) . \mathrm { S o }$ , the time complexity of the proposed algorithm is $O ( N ^ { 2 } + ( y _ { \mathrm { n } } \times y _ { \mathrm { m } } ) ^ { 3 } )$"

### 3) 决策粒度与动作空间

- 粒度：**每地面业务小区（traffic cell）+ 每流**；按优先级逐节点串行算路（L138）。
- 动作空间：**三条分支** —— (a) 轻载区：走 MST 到某个 outermost node（预均衡后的权重决定选哪个）；(b) 重载区：Dijkstra 求最小权重路径到中心站；(c) **显式拒绝**（无可达路径时丢弃，L165）。**注意"拒绝"是显式动作，不是失败**。
- 转发一致性由 SR 保证（L125："paths in the light or the heavy load zone would generate a series of segments to ensure forwarding coherence based on SR."）。

### 4) 是否含学习成分

**无。** §0.1 证据：本篇 reinforcement=0、\blearn=0、\btrain=0、supervised=0、reward=0、credit assignment=0、penal*=0、counterfactual=0。全部为 MST + Dijkstra + 人工权重 (0.5+0.1x_i)。

### 5) 负载与流量设置（仅作条件登记）

- **L174** Table 1 逐字："The number of orbits 6 / The number of satellites per orbit 12 / The inclination of orbits 90 度 (polar orbit) / The angle between adjacent orbits 30 度 / The number of gateways 4 / The bandwidth of satellite links 25 / The bandwidth of feedback links 100"
- **L191**："Traffic cells are divided in Fig. 6 which gives gateways location. The value in each cell is the traffic density obtained by prediction. Two traffic density distributions are considered in simulation, uniform distribution where all traffic density is 1 and prediction distribution as Fig. 6. The unit service value u is assumed to be 1, 2, and 3 for uniform distribution. The unit service value u is considered to be 4 and 5 for prediction distribution"。
- **L62**（流量模型）"The ground surface is divided into rectangular traffic cells according to location and constellation. Each traffic cell should be bind to one satellite anytime which is responsible for communication and traffic in that cell. ... At the same time, the traffic density of each traffic cell is predicted and marked referring to the geographical location, population, et al."
- **L181** Table 2 重载区尺寸枚举：(3,2)(3,3)(3,4)(4,4)(3,5)(4,5)(5,5)(3,6)(4,6)；(4,2)(4,3)；(5,2)(5,3)(5,4)；(6,2)(6,3)(6,4)(6,5)(6,6)；(6,12) 即全网。
- **L195**："Programming language C++ is used for simulation to simulate network scenario and implement algorithms. ... The results of size (6,12) are used as thresholds for five indicators."
- **L283**："The uniform traffic distribution is adopted and the unit service value is assumed to be 2. The size of the proposed algorithm selects (6,5) in this scenario because of benefit, cost and time complexity."；对比算法为 Dijkstra、HRA、JDDA（L294）。
- **L298**："The average rejection ratio decreases, the average relative throughput increases, and the maximum link utilization decreases as the size extends ... For another, the average delay also increases with the extension of size that contributes to the increase of cost and resources occupied."

### 6) 可迁移点（能否搬进 RL 路由）

- **可搬（状态特征）**：公式 (4)(5) 的拥塞指数 c(e) = F(e)/r(e) 是一个对负载**单调且高敏感**的连续特征，作者明确论证其优于 F(e)/b(e)（L140）。可直接作为 RL 的 state feature 或奖励中的拥塞惩罚项，无需学习。
- **可搬（动作空间设计）**：把"无可行路径"**显式建模为拒绝动作**（L165），而不是当作失败——这对 RL 的动作空间设计直接有用（避免 reward 把"主动拒绝"与"被动丢包"混为一谈）。**这一点与 §12 的 G-A 同源**：它区分的是"决策导致的拒绝"与"资源导致的丢失"。
- **可搬**：区域划分（轻/重载）是**状态空间分区 + 分策略**的现成模板，可映射为 RL 的 context/meta-policy 切换。
- **障碍**：① 论文假设流量密度**可离线"预测并标记"**（L62），RL 需要在线观测替代先验；② 参数 0.5/0.1（L136）与区域尺寸 (6,5)（L283）均为人工选择，正是 RL 应当搜索的对象；③ 论文场景是"网关集中在一个有限区域"的**回传**流量，与一般任意源-目的流量不同构，迁移需重新论证。
- **已被本库采用？** 本批内未见引用关系。T1 批次是否采用，本会话无读权限（见 §13）。


## 12. 对抗性问题（针对缺口主张 G-A）的答复

**问题（主控原文）**：全库是否有任何工作，把**同一个失败事件**（丢包/超时/溢出）按**物理原因**拆成**不同的学习通道或惩罚项**（例如区分"决策缓存溢出"与"链路队列溢出"）？

### 12.1 检索记录（模式 + 计数 + 命中处置）

检索范围：本批 11 篇全文（5286 行）；命令形态 grep -ciE '<模式>' <11 个文件路径>，命中行再用 grep -inE 逐条复核。

| 模式（逐字） | 命中计数 | 命中处置 |
|---|---|---|
| credit assignment | 11 篇全 0 | — |
| counterfactual | 11 篇全 0 | — |
| reward | **11 篇全 0** | — |
| multi-objective\|multiobjective\|MORL\|reward vector\|multiple objectives\|Pareto | JP79GMZS=1，其余 0 | **假阳性**：JP79GMZS **L215** "The On/Off periods of the connections are derived from a Pareto distribution with a shape equal to 1.2." —— 指流量分布，非多目标。**不构成反例** |
| separate (reward\|penalty)\|distinct (reward\|penalty)\|different (reward\|penalty)\|per-cause\|penalty term\|penal | X5K285MW=1，其余 0 | **假阳性**：X5K285MW **L106** "While we applied the processing penalty on each hop, its effect on the average end-to-end latency was not significant." —— 指逐跳处理开销，非惩罚项。**不构成反例** |
| drop (reason\|cause)\|reason for (the )?(drop\|loss)\|cause of (the )?(drop\|loss)\|root cause\|discard reason | 9KZDXPKC=2，其余 0 | **假阳性**：9KZDXPKC **L246** "...the throughput drop caused by GSL handover..." 与 **L248** "...the throughput drop caused by ISL failure..." —— 命中原因是子串 "drop cause**d** by"。语义上确实在区分两类失败，但**不是** per-cause 学习通道。**不构成反例（但见 §12.2 先例 1）** |
| overflow\|saturat\|full buffer | JP79GMZS=2、TQF59BD7=4、IXVSNEE3=6，其余 0 | 逐条见 §12.2 末段；**均无学习通道含义** |

### 12.2 结论：本批 11 篇中**未发现**满足 G-A 的工作

**判定为"未发现"的依据**：本批 11 篇**全部无学习成分**（§0.1：reinforcement=0、\blearn=0、\btrain=0、supervised=0、reward=0、credit assignment=0、counterfactual=0）。既然不存在学习通道，**原则上不可能存在"把失败按原因拆成不同学习通道或惩罚项"的工作**。这是**结构性排除**，而非抽样遗漏。

但检索发现 **3 个必须登记的机制层部分先例**（分解轴各不同）：

#### 先例 1（最强，分解轴 = 失败原因）：9KZDXPKC / DB-R

- **分解轴**：**失败原因**（GSL 切换 vs ISL 失效）。同一个失败事件 = **丢包**。
- **逐字证据**：**L55** "DB-R mechanism leverages default routing to address the packet loss caused by GSL handover. Moreover, DB-R mechanism configures backup routing to address the packet loss caused by ISL failure."；**L180** "When a GSL is disconnected, the satellite's routing entries that correspond to the interface of the disconnected GSL will immediately disappear."；**L220** "When an ISL becomes disconnected due to antenna misalignment, the corresponding interface of the faulty ISL become unavailable."；**L188**（时间尺度差异）"such a period lasts for about tens of milliseconds."
- **是否覆盖 G-A**：**否**。它拆的是**路由处理通路**（default route vs backup route），不是**学习通道/惩罚项**；两条通路的目标都是"消灭丢包"，没有把两条通路变成两个独立的学习信号。
- **但它对 G-A 的价值**：它是本批中**唯一提供"失败原因可在线标注"机制的论文**（L198-204 的前缀命中判据 + L230 的接口失效判据）。RL 若要实现 G-A，这台标注器是现成可复用的起点。**建议主控把它登记为 G-A 的"机制模板"而非"反例"。**

#### 先例 2（分解轴 = 代价来源）：9GPFG5U3 / LiR

- **分解轴**：**代价来源**（BF 假阳性导致的错误转发 vs BF 位宽导致的正确路径开销）。
- **逐字证据**：**L121** "Hence false positives will lead to incorrect forwardings towards unspecified ISLs. We let $f _ { I F O } ( \cdot )$ denote the incorrect forwarding overhead, which measures the data volume (in KB) delivered on the incorrect ISLs."；**L123** "The BF-based forwarding utilizes the M-bit vector to record the ISL identifiers, which also increases the forward overhead along the correct path. We let $f _ { C F O } ( \cdot )$ denote the correct forwarding overhead..."；**公式 (7)**（L179-181）"f_FO(N,M,K) = f_IFO(N,M,K) + f_CFO(N,M)"。
- **是否覆盖 G-A**：**部分**。分解**存在**（两项物理来源不同），但公式 (7) 立刻把两者**加和为单一标量**，没有形成两个独立学习通道/两个惩罚项。**是最接近 G-A 的"分解但未分通道"形态。**
- **G-A 的切口**：把公式 (7) 的加法拆成两路（例如两条 reward 通道或双头 critic），在 LiR 架构上即为可实施的最小反例构造。**建议主控把它登记为 G-A 的"最近邻工作"**——若审查者质问"分解代价不是新鲜事"，必须先承认 LiR 已做分解、再指出其未分通道。

#### 先例 3（分解轴 = 逻辑域/层次/动作维度，均非失败原因）

- **AF674CSF**：分解轴 = **组内 / 组间**（L87-89、L153-157）。
- **TQF59BD7**：分解轴 = **簇内 / 簇间 + QoS 类**（L302、L385 的四类 QoS）。
- **JP79GMZS**：分解轴 = **业务类 A/B/C**（L148-154、L164 的绕行优先级）。
- **IXVSNEE3**：分解轴 = **动作方向**（水平/垂直两套队列 Q^h/Q^v，L293、公式 (24) L297-299）——按**动作维度**分离，而非按失败原因。
- **是否覆盖 G-A**：**均否**。分解轴都不是"同一失败事件的物理原因"。

#### 假阳性与"看似相关但不同"的条目（必须登记）

- **JP79GMZS L213**："The rationale beneath this assumption is to avoid any possible confusion between throughput degradation due to packet drops (due in turn to buffer overflows at satellites) and that due to satellite channel errors." → 这是**实验设计**上刻意区分"缓冲溢出丢包"与"信道错误丢包"，语义上与 G-A 最接近，但**它是为了排除混淆变量，不是为了分通道学习**。**不构成反例**，但**是 G-A 的动机类证据**（连非学习论文都认为这两类丢包必须分开对待）。
- **TQF59BD7 L482**："Using the same small buffer size of 360 kbit caused issues for signaling in larger clusters. ... Signaling traffic is prioritized by the scheduler, so packets of other QoS classes may be dropped. Figure 11 illustrates this systematic error consisting of periodic drops due to peaks in high-priority signaling traffic." → 归因了"**信令突发导致其他类丢包**"的因果链，但用于**缓冲尺寸调参**，非学习通道。**不构成反例**。
- **IXVSNEE3 L301 / L539-541**：队列饱和与系统饱和是**控制判据**（切换方向 / 定义 B_s^th、R_pac^th），不是失败原因分解。**不构成反例**。
- **VFS59FHI L165**：把"无可行路径"显式建模为**拒绝**而非丢包 → 是"区分决策导致的拒绝与资源导致的丢失"的先例，但**无学习成分**。**不构成反例**。

### 12.3 一句话结论

> **本批 11 篇中没有任何工作把同一失败事件按物理原因拆成不同的学习通道或惩罚项——因为本批 11 篇全部不含学习成分（结构性排除，非抽样遗漏）。最接近的是 9KZDXPKC（按失败原因拆成两条路由通路）与 9GPFG5U3（把总转发开销按物理来源拆成两项后再加和为单一标量）；两者都不覆盖 G-A，但分别提供了"失败原因在线标注器"与"最近邻分解先例"两件可直接使用的素材。**

---

## 13. 本批完成度与受限声明

### 13.1 完成度

- **11/11 篇全文逐行通读完毕**，无遗留：JP79GMZS(412)、TQF59BD7(605)、SBCHGBCP(419)、X5K285MW(166)、AJJI57M9(431)、9GPFG5U3(712)、AF674CSF(619)、IXVSNEE3(726)、9KZDXPKC(336)、BBNQ4EAQ(495)、VFS59FHI(365)，合计 5286 行。
- 每篇均产出规定的 6 项；公式逐字抄录（编号式计数：AJJI57M9 11 个、9GPFG5U3 17 个、IXVSNEE3 45 个、SBCHGBCP 10 个、JP79GMZS 12 个、TQF59BD7 16 个、VFS59FHI 12 个、BBNQ4EAQ 5 个、9KZDXPKC 4 个）。
- **如实说明（非未读完）**：**X5K285MW（166 行）与 AF674CSF（619 行）通读全文后确认"无编号公式、无展示式"** —— 这两篇本身以散文 + 表格 + 伪码承载机制。已在各自 §2 明确写出，并逐字登记其唯一的定量陈述与代价定义（X5K285MW：L70/L92/L106；AF674CSF：L173/L189）。
- **AJJI57M9 的 §5 特别标注"本篇没有流量/负载设置"**：其实验是全源目的对的拓扑/时延实验，无业务流与到达率。这是如实登记，不是漏读。

### 13.2 受限声明（必须由主控处置）

1. **"是否已被本库 RL 论文采用"无法完整回答**。本会话读权限只覆盖：本人分配的 11 个 VM MD、TIER-ASSIGNMENT.md，以及要写出的 DOSSIER-B5.md。
   - 尝试读取 ANCHOR-DISSECT-S85KQ4FC.md 与 EXTRACTION-TEMPLATE.md：**两次均被 [HOOK-BLOCK]**（"角色 deepener 不允许访问：ANCHOR-DISSECT-S85KQ4FC.md（shell-file）"）。已按协议等待 20 秒重试一次，仍被拦，随即停止。
   - 尝试 glob 检索 round/run4/ 下其它产出文件：**被 [HOOK-BLOCK]**（"角色 deepener 不允许访问：.（param）"）。
   - 因此 T1 批次（B1-B4）与 T2 其它批次（B6/B7）是否采用本批机制作为基线，**我无法核验**。本文件中所有"已被本库采用"的表述**一律限定为我能在本批内直接读到引用关系的条目**（§0.2 已逐条给出参考文献行号），其余一律标注"未验证（见 §13）"。**请主控在 B1-B4 产出后做一次交叉核验**。
2. **X5K285MW Table 1 的 OCR 损坏**：L54 表格行列错位（数值被合并为 "28841224760"，地面段字段名与数值分行），我**未能可靠还原该表**。已在该篇 §5 标注"表格 OCR 混排"。若该表数值承重，请主控从原始 PDF 复核。
3. **SBCHGBCP 表格 OCR 损坏**：L270 的 19x19 非均匀流量矩阵在 MD 中被压缩为单行 HTML 表，数值可读但行列对应关系不可靠；L297-299 Table 2 亦存在列错位。已如实标注，未据此下结论。
4. **公式编号 OCR 断行**：SBCHGBCP 公式 (3) 的编号独占 L149（正文在 L144）；9KZDXPKC 全文无编号公式。已在引用时同时给出行号区间便于复核。
5. **未做**：本批未对任何一篇做外部检索（未用 web_search / Undermind），未核验引用数或后续影响；所有结论**仅基于 VM MD 全文**。

---

## 14. 交给主控的三条行动项

1. **G-A 的"最近邻工作"必须先承认**：9GPFG5U3 公式 (7) 已把转发开销按物理来源拆成 f_IFO 与 f_CFO（L121/L123/L179-181）。若 G-A 主张"首次按失败原因分解"，措辞必须避开"首次分解代价"，改为"分解后**未分通道学习**"。建议把 9GPFG5U3 与 9KZDXPKC 一并列入 G-A 的对抗性审查清单。
2. **可直接复用的两件素材**：
   - **失败原因在线标注器** <- 9KZDXPKC L198-204（前缀命中 GSL Array 判定 GSL 切换）+ L230（接口失效判定 ISL 故障）。
   - **动作安全门 / 动作屏蔽** <- IXVSNEE3 公式 (25) L303-305 的 Gamma 阈值（用剩余队列空间归一化两条候选动作的代价差）。
3. **RL 路由必须超越的对照基线（本批给出三个可引用数字）**：
   - 零状态随机最小跳选路：比时延优先 SPF 多支持约 **73%** 负载（X5K285MW L96）；
   - 逐包 vs 逐流：per-flow 比 per-packet 多支持 **45.3%** 负载（TQF59BD7 L472）；
   - 源路由 vs 负载感知：7.6 Gbps vs 15.0 Gbps（TQF59BD7 L17/L449）。
   任何 RL 路由选题若不在这三条基线上给出增量，贡献不成立。

