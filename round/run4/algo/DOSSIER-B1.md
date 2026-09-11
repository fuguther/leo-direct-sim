# DOSSIER-B1 — Batch 1：深度 DQN/MARL 族（8 个 itemKey / 7 篇）

> 材料：MinerU MD 全文（VM 路径 /data/liguang13/topic-loop-r2/md/〈key〉/〈key〉/txt/〈key〉.md）。
> 所有行号均为该 MD 文件行号；引文逐字照抄（含原文笔误，如 "dificult"、"Of"=Off）。公式一律抄 LaTeX 原文。
> **重复条目**：5PYWVRC5 与 L2VKYTAV 是同一篇的两个入库副本（md5 同为 b116d516852ae09a832f7e658d1ed602，均 123 行），本批只拆一次，见第 7 篇。

---

## CMNCS52M Traffic-Aware MARL Routing (DQN-LSNR)

IEEE Open Journal of Vehicular Technology 2026（DOI 10.1109/OJVT.2026.3688868），374 行。

### 1. MDP 定义

**状态 s_t**：16 维连续向量（zone-based 场景为 15 维，时间特征被删）。L141 逐字：

> "This information is encoded in a 16-dimensional continuous vector structured as follows:"

逐字段（L143–L155）：

- **邻居队列长度**（L143）："Queue lengths of neighbors: a vector q that stores the queue lengths of the four neighbors of satellite i. The elements are ordered clockwise and denoted by $q _ { i } ^ { N } , q _ { i } ^ { E }$ $q _ { i } ^ { S } .$ , and $q _ { i } ^ { W }$"（4 维，瞬时量；未说明归一化）
- **地理坐标**（L145）："The next four values capture the geographic positions with longitude λ and latitude φ coordinates of both the current satellite $i ( \lambda _ { i } , \phi _ { i } )$ and the destination satellite $( \lambda _ { D } , \phi _ { D } )$"（4 维）
- **包长**（L147）："Packet size (L), ranging from 50 B to 250 B."（1 维）
- **邻居距离**（L149）："the vertical (north-south) distance, denoted as $d _ { i } ^ { V }$ , and the horizontal (east-west) distance, denoted as $d _ { i } ^ { H }$"（2 维）
- **访问计数器**（L151）："a vector h<sub>i</sub> that stores how many times the current packet in satellite i has previously visited each direction or neighbor... These elements act as a form of memory, helping the agent to avoid routing loops."（4 维）
- **时刻 t**（L153）："The final element is a float variable ranging from 0 to 24, representing the time of day in hours."（1 维）

L155 合并式（逐字）：

> $\mathbf { s } _ { \mathbf { i } } =$ $[ \mathbf { q } _ { i } , \phi _ { i } , \lambda _ { i } , \phi _ { D } , \lambda _ { D } , L , d _ { i } ^ { V } , d _ { i } ^ { H } , \mathbf { h } _ { i } , t ]$

**动作 a_t**：L159 逐字：

> "we consider four discrete actions, each corresponding to forwarding a packet to one of the satellite's immediate neighbors... The set of all possible actions can be expressed as $\mathbf { A } = \{ N , E , S , W \}$ ."

动作掩码：**无显式掩码**，只有硬禁止（L159）："forwarding a packet to a neighbor moving in the opposite direction is prohibited... satellites located in the cross-seam regions have only one horizontal neighbor available. Additionally, forwarding a packet to a congested satellite is also forbidden"。禁止动作靠奖励 −R 惩罚，而非 logits mask。

**奖励 r_t**：Eq (6)，MD L166 逐字：

> $r _ { i } ^ { a } = \left\{ \begin{array} { l l } { R , } & { \mathrm { i f ~ } j = D , } \\ { - R , } & { \mathrm { i f ~ } j = - 1 , } \\ { - \big ( t _ { \mathrm { H O P } } ( i , j , L ) \times ( 1 + \mathbf { h } _ { i } ( a ) ) } & { \mathrm { o t h e r w i s e } . } \end{array} \right.\tag{6}$

单跳时延，Eq (7)，MD L172 逐字：

> $t _ { \mathrm { H O P } } ( i , j , L ) = t _ { \mathrm { P } } ( i , j ) + t _ { \mathrm { T X } } ( L ) + t _ { \mathrm { Q } } ( j ) .\tag{7}$

系数说明（L169）：R 的定标——"$R$ must be sufficiently large to compensate for the cumulative penalty incurred at each next-hop decision... $R$ is determined by estimating the mean hop delay for each queue-distribution model and scaling it by the average number of hops, along with an additional safety factor. Consequently, each queue model requires a distinct value of $R$."；归一化——"the absolute values of all immediate rewards $r _ { i } ^ { a }$ are normalized between 0 and 30 k"。

折扣 γ：L131 "The discount factor $\gamma \in [ 0 , 1 ]$"；表 2（L182）取 **0.99**。

**转移/终止**：L137 "we define both the transition function and the reward function as deterministic"。L189 终止条件逐字：

> "An episode terminates under one of three conditions: (1) the agent executes a forbidden action, (2) the maximum number of steps is reached, or (3) the destination is successfully reached."

无资格迹、无多步回报（见第 10 项检索）。

### 2. 学习算法与更新式

算法名（L131）："Double Deep Q-Network (DDQN)-based LSN Routing (referred here to DQN-LSNR)"。

TD 目标 Eq (5)，MD L134 逐字：

> $y _ { j } = r _ { j } + \gamma \operatorname* { m a x } _ { a } \mathcal { Q } _ { t } ( s _ { j + 1 } , a ) .\tag{5}$

**注意**：Eq (5) 是原版 DQN 的 max 目标（由 target net 取 max），**文中未给 double-DQN 的 action-selection / evaluation 分解式**；仅在 L131 声称使用两个网络。损失函数原文未给公式。

网络结构（L179 + 表 2 L182）："four hidden layers"，宽度 "64, 32, 16, 8"；输出 4；输入 15/16。无图算子。

超参（表 2，L182）：Learning rate 0.005；Discount factor 0.99；Exploration decay factor 10；Training episodes 500,000；Target network update 10,000 steps；Replay buffer 10,000；Batch size 128。

### 3. 信用分配

**逐跳即时奖励**，不做路径级终局分解。L163 逐字：

> "In our model, three types of rewards are defined: a large positive reward when the selected action delivers the packet to its final destination, a large negative reward for forbidden actions, and a moderate penalization for valid actions that forward the packet to an intermediate node."

归因到"动作方向"而非具体链路；惩罚按 visit counter 放大（Eq (6) 第三支的 $1 + \mathbf { h } _ { i } ( a )$）。**不区分损失原因**（丢包/拥塞/环路无独立奖励项）。

### 4. 状态里有没有时间信息？

**有，但只有两类，均非聚合统计量**：(a) 时刻 t（L153，0–24 h 瞬时值）；(b) visit counters $h_i$（L151，**包级累计记忆**，随包走，非时间窗聚合）。

**没有** EWMA / 滑窗 / 差分 / 趋势项。检索：全文 grep -n -i -E "EWMA|exponential(ly)? weighted|moving average|smoothing factor" → 仅 L185 命中 "moving average of the long-term reward"（训练曲线画法，非状态特征）；grep -n -i -E "frame.?stack|stacked|historical|history|previous state|past state|memory" → 命中 L151（即 visit counters 的 "a form of memory"）与 §II 相关工作，无历史窗口状态。

### 5. 动作有没有时间结构？

**无**。每包每跳独立决策；无动作驻留、无流级缓存、无摊销。L191 逐字："Each satellite observes its current local state and feeds it into the trained model to infer next-hop routing decisions." 无切换代价项。

### 6. 多智能体设定

**完全独立学习**（FDR-MARL 式）：无参数共享、无智能体间通信（唯一"通信"是观测邻居队列长度）、无 CTDE、无非平稳处理。检索：全文 grep -n -i -E "VDN|QMIX|QTRAN|MADDPG|centrali[sz]ed critic|centrali[sz]ed training|parameter sharing|shared parameters|non-?stationar" → **0 命中**。

L191 部署方式逐字："The training process is conducted on the ground using a simulated LSN environment with sufficient computational resources. Once training is completed, the learned policy can be deployed onboard resource-constrained satellites."

### 7. 训练协议

L189 逐字（训练分布随机化）：

> "During training, each episode is initialized by randomly sampling the number of orbits, the number of satellites per orbit, the source and destination satellites, the packet size, the satellite queue states, and the orbital positions, following the system model described in Section III."

表 2（L182）：Number of orbits {3,4,…,12}；Satellites per orbit {4,5,…,16}；Orbit altitude 780 km；inclination 90°。

评估：L217 "a total of 10,000 packet transmissions with varying source–destination pairs are evaluated. The constellation configuration is fixed to an Iridium-like topology, comprising 6 orbital planes with 11 satellites per orbit."；泛化评估 L272 覆盖训练用过的全部星座配置（原文 L272："all constellation configurations used during training"，共 130 种，100 test episodes）。

**训练/评估分布**：Iridium-like 6×11 落在训练区间内；三种队列分布模型各自训练独立策略（R 与 queue capacity 按模型区分），**未做跨模型迁移**。

### 8. 该文的算法贡献（与 1–7 具体改动对应）

对照同为 DQN 但状态 22 维、奖励含"到目的地残余传播时延"的 DQN-BL（L201）：(a) 状态由 22 维压到 16 维，去掉绝对目标导向量、改为本地几何量 $d_i^V, d_i^H$，并加入 **visit counters $h_i$**；(b) 奖励改为**实测单跳时延** $t_{\mathrm{HOP}}$（Eq (7)）。L232 逐字：

> "In contrast, the proposed DQN-LSNR learns from the actual hop-to-hop delay associated with each action, enabling it to select longer routes when beneficial in order to avoid congested regions."

### 9. 该文自述的局限

L285 逐字：

> "However, careful design of the state representation, reward function, and loop-avoidance mechanisms remains critical to ensure stable and reliable performance."

L287 逐字：

> "Future work will focus on further analyzing the generalization capabilities of DQN-LSNR under large-scale mega-constellations. In addition, routing complexity will be increased by incorporating satellites with different orbital altitudes and inclinations, resulting in a highly dynamic and heterogeneous environment."

### 10. 该文没有考察的算法选择

（基于 1–7 实际内容；检索式为全文 grep，范围＝该篇 MD 全文 374 行）

- **TD 目标未做 double 分解**：Eq (5) 仍是 $\max_a Q_t$；grep -n -i "double" 仅命中 L131/L283 的名称声明，无 action-selection/evaluation 分离公式 → 名义 DDQN、实现式未变。**从未比较 DQN vs DDQN**。
- **无多步回报/资格迹**：grep -n -i -E "n-step|multi-step|eligibility trace|lambda-return" → 0 命中。从未比较 1-step 与 n-step。
- **无 DQN 变体消融**：grep -n -i -E "dueling|prioriti[sz]ed replay|noisy net|distributional|rainbow" → 0 命中。从未比较不同 TD 目标/回放策略。
- **无策略梯度族对照**：grep -n -i -E "actor.?critic|PPO|A2C|A3C|SAC|DDPG|TD3|policy gradient" → 仅命中资助机构名（L11）与 "Opportunistic"（L19）等假匹配，无算法。
- **状态逐字段均为瞬时量或包级计数，无任何时间窗聚合**（见第 4 项检索）：从未比较"瞬时状态 vs 带历史状态"。
- **动作无时间结构**：从未考察动作驻留/流级路由缓存（对比本批 S85KQ4FC 的 flow-centric）。
- **无多智能体协作机制**（第 6 项检索全 0）：从未考察 CTDE、参数共享、通信。
- **训练分布**：只在同一状态/奖励设计下比较三种队列模型 + 一个 DQN-BL，从未比较不同星座族/不同负载族之间的迁移。
- **无动作掩码**：grep -n -i -E "mask|feasib|legality" → 3 命中（L46 相关工作、L125 路径可行性约束、L151 visit counters memory），**均非动作掩码**。

### 11. 可复用的具体机制

1. **visit-counter 放大的单跳代价**（Eq (6) 第三支）：$r = -\left( t _ { \mathrm { H O P } } ( i , j , L ) \times ( 1 + \mathbf { h } _ { i } ( a ) ) \right)$ —— 用乘性放大即可内生出环路规避，无需额外 loop-breaker 模块；且 h 是**包级**而非时间级记忆，与时间聚合正交，可直接叠加到我们的方案上。
2. **R 的定标规则**（L169）：R = 该负载模型下的平均单跳时延 × 平均跳数 × 安全系数，并把 $|r|$ 归一化到 $[0, 30k]$ —— 跨不同负载情景保持奖励尺度的可操作方法。
3. **单跳时延作为奖励核**（Eq (7)）：$t _ { \mathrm { H O P } } = t _ { \mathrm { P } } + t _ { \mathrm { T X } } + t _ { \mathrm { Q } }(j)$，直接把"下一跳排队"记入本跳代价。

### 12. 实验合同里与"负载"相关的设置（仅作条件登记）

- 三种队列分布模型（L77）：zone-based（8 区，均值占用 0.5，队列容量 10 MB）、population-based（GPWv4 人口，均值占用约 0.06，容量 100 MB）、traffic-based（IUD 由 GDP 线性回归，容量 150 MB，含速率自适应 25%/50%/100%）。
- 传输速率 50 Mbps（traffic 场景 {12.5, 25, 50}）；包长 50–250 B。
- 链路失效实验：0%–30% 随机断链，10,000 evaluation episodes（L238）。
- 星座：训练 {3–12 平面} × {4–16 星/面}；评估 6×11。

---

## 42E4NAQU Queue-Aware and Resilient Routing in LEO Using MARL

197 行。**全文无任何奖励公式、无 TD 目标公式** —— 这是本批最需要标注的一点。

### 1. MDP 定义

**状态**：L125 逐字（仅自然语言，无公式）：

> "The state includes the coordinates of the current satellite, the coordinates of its four neighboring satellites, the queue levels associated with each neighbor (across their respective queues), and the coordinates of the packet destination."

扩展（L131）："we extend the state space by introducing four additional features corresponding to the resilience score of the four connected links, where values range from 0 (highly vulnerable) to 1 (highly reliable)." → 韧性分 4 维，**值域 [0,1] 已归一化**；其余分量未说明归一化。

**动作**：L127 逐字：

> "each agent selects one of the neighboring satellites as the next hop, corresponding to four possible directions: upward, downward, rightward, or leftward."

L131："The action space remains unchanged, with the model selecting the next-hop link for packet forwarding." 无动作掩码（grep -n -i -E "mask|feasib|legality" → **0 命中**）。

**奖励**：**无公式**。L127 逐字（四项，散文）：

> "The reward function is formulated as a combination of four key metrics. First, it accounts for the queueing delay at the current satellite prior to forwarding. Second, it captures the reduction in distance toward the destination achieved by the selected action. Third, a penalty is imposed to discourage revisiting previously traversed nodes, thereby avoiding routing loops. Finally, the reward incorporates the resilience associated with the selected path, promoting more reliable routing decisions."

L131 再次："The reward function is extended with a fourth component, the resiliency score, which provides a reward proportional to the resilience of the selected route."

→ **四项权重、量纲、归一化、折扣 γ 全部未给**。全文唯一带公式的评分类量是韧性分 Eq (10)。逐字：

> R^{all} = \omega _ { 1 } \big ( 1 - P _ { o u t } ^ { a l l } \big ) + \omega _ { 2 } \max_{i \ne j,\ i,j \in N} \left( \max \big ( 1 - q _ { i } , 1 - q _ { j } \big ) \cdot S _ { ( i , j ) } \right)\tag{10}

单跳时延 Eq (5)，MD L72 逐字：

> D ( i , j ) = \frac { \| i j \| } { c } + \frac { B } { R ( i , j ) } + t _ { q } ( i ) .\tag{5}

（L67 给出 $t _ { q } ( i ) = q _ { i } \cdot B / R ( i , \cdot )$。）

**转移/终止**：均未给；无 episode 终止条件描述，无多步回报。

### 2. 学习算法与更新式

L129 逐字：

> "We adopt a Double Deep Q-Network (DDQN)-based DRL algorithm to solve the considered problem. The proposed framework consists of a neural network that approximates the action-value (Q) function, a target network used to stabilize training by periodically updating its weights, and a replay memory buffer for experience storage and sampling."

**无 TD 目标公式、无损失公式**。表 I（L134）登记：Loss function = Huber loss；Optimizer = Adam；Optimizer learning rate = 0.0001；Policy neural network = "DNN with three layers"；Target neural network = "DNN with three layers"；Training iterations 100000；Replay memory 2000；DRL batch size 128；Epsilon start 0.99 / end 0.1 / decay rate 1000。层宽与激活函数未给。

### 3. 信用分配

四项散文奖励（见第 1 项引文），**逐跳即时**；无路径级终局项、无按节点/链路分解、**不区分损失原因**。第 4 项（韧性分）是唯一带公式的分量，但它按**路径**定义（L89："$S _ { ( i , j ) } \in \{ 0 , 1 \}$ is the path selection variable"），把路径级量塞进逐跳奖励而**未见分配规则**。

### 4. 状态里有没有时间信息？

**没有**。状态为瞬时坐标 + 队列 + 静态韧性分。检索：grep -n -i -E "EWMA|exponential(ly)? weighted|moving average|smoothing factor" → 0 命中；grep -n -i -E "frame.?stack|stacked|historical|history|previous state|past state|memory" → 仅 2 命中（L129 replay memory、表 I 的 "Replay memory"），均非状态历史项。

### 5. 动作有没有时间结构？

**无**。逐包选下一跳；无驻留、无摊销、无切换代价。

### 6. 多智能体设定

该篇有一处值得登记的结构（本批少见），L129 逐字：

> "Initially, we train a global Q-network to learn routing policies across the entire satellite constellation. This centralized training enables the model to capture the overall traffic dynamics and network conditions. Once the global model converges, it is deployed on individual satellites, where each utilizes the trained model to make local routing decisions. Furthermore, we incorporate online learning at each satellite to continuously update the model based on local observations, thereby improving decision-making in dynamic network conditions."

即 **集中训练 + 分布执行 + 部署后在线微调**。但参数共享与否未说明，无智能体间通信，无针对非平稳的显式机制。检索 grep -n -i -E "VDN|QMIX|QTRAN|MADDPG|centrali[sz]ed critic|CTDE|non-?stationar" → 仅 L129 一处（措辞为描述，非 CTDE 机制），其余 0。

### 7. 训练协议

表 I（L134）：Starlink shell 1，O=72 平面，S=1584 星，550 km，Walker Delta，200 ground terminals，ISL 带宽 500 MHz，包长 64 kb，训练 100000 iterations。

负载两种（L123 逐字）：

> "we consider two types of traffic generation patterns: (i) uniform traffic generation, where each ground terminal produces an equal amount of data, and (ii) population-based traffic generation, where the data generation is proportional to the number of users connected to each ground terminal."

**训练/评估分布**：未区分训练分布与评估分布，未描述 episode 采样方式，**未给训练时长/收敛曲线**。

### 8. 该文的算法贡献

(1) 把**韧性分**（Eq (10)）同时作为 4 维状态与奖励第 4 分量（L131）；(2) 全局 Q 网络集中训练后在星上继续在线学习（L129）。相对其参考框架 [8] 的具体改动即此两点。

### 9. 该文自述的局限

L160 逐字：

> "In contrast, the proposed approach exhibits comparatively lower resilience. Although each agent has access to its local queue state as well as the queue conditions of its neighboring nodes and attempts to make optimal routing decisions, it lacks a global view of the network. This limited observability results in slightly reduced resilience performance for both MA-DRL and SARSA."

L164 逐字（兼作局限）：

> "Future work will investigate advanced learning techniques and hybrid learning–traditional formulations for improved efficiency and robustness."

### 10. 该文没有考察的算法选择

- **奖励从未公式化**：第 1 项显示四项仅有散文；全文无奖励等式。**从未比较不同奖励构成/权重**。
- **无 TD 目标/损失的 double 分解**：第 2 项；grep -n -i "double" → 仅 L129 名称。从未比较 DQN vs DDQN 或其他 target 机制。
- **无多步回报/资格迹**：grep -n -i -E "n-step|multi-step|eligibility trace|lambda-return" → 0。
- **无 DQN 变体/回放策略消融**：grep -n -i -E "dueling|prioriti[sz]ed replay|noisy net|distributional|rainbow" → 0。
- **无策略梯度族对照**：grep -n -i -E "actor.?critic|PPO|A2C|SAC|DDPG|TD3|policy gradient" → 仅参考文献标题（L186）。
- **状态无任何时间聚合**（第 4 项检索）：从未比较瞬时状态 vs 带历史状态。
- **动作无时间结构**：未考察流级缓存/驻留。
- **在线学习的效果未隔离**：L129 声称部署后在线更新，但**全文无消融**（无 online vs frozen 对比），故无法据以判断该机制增益。
- **无动作掩码**（检索 0 命中）。
- **终止/episode 定义缺失**：从未定义 episode 边界，无从比较不同 episode 切分。

### 11. 可复用的具体机制

1. **韧性分作为状态维 + 奖励分量**（Eq (10)）：R^{all} = \omega_1 (1 - P_{out}^{all}) + \omega_2 \max_{i \ne j} ( \max(1-q_i, 1-q_j) \cdot S_{(i,j)} ) —— 把"可用性不确定性"与"队列余量"合成一个 [0,1] 标量，可直接作为观测字段。
2. **端到端中断概率的乘法合成**（Eq (9)）：P_{out}^{all} = 1 - ( 1 - P_{out}^{u} ) ( 1 - P_{out}^{d} ) \times \prod_{\forall i,j \in N,\ i \ne j} ( 1 - P_{out}^{i,j} ) \times S_{(i,j)} —— 逐跳失效的可观测量。
3. **排队时延的速率耦合近似**（L67）：t_{q}(i) = q_i \cdot B / R(i,\cdot) —— 用"包数×包长/出口速率"近似 FIFO 等待，工程上易落地。

### 12. 实验合同里与"负载"相关的设置（仅作条件登记）

- 两种流量生成：uniform / population-based（L123）。
- Starlink shell 1（72 平面 × 1584 星，550 km），200 地面终端；每终端 10 W，星上 20 W；ISL 500 MHz；噪声 −174 dBm/Hz；α=2；Nakagami-m=2；载频 30 GHz；包长 64 kb。
- 对照组 Dijkstra / SARSA / MA-DRL（L143）。为公平比较 Dijkstra，L145 逐字："the queue capacity in the simulation is set to 1 Gb/s, effectively preventing queue overflow" —— **该设置改变了负载条件本身**，登记备查。

## LZKNZA8B Spatial-Temporal Learning-Based Distributed Routing (GAT+LSTM+DQN)

341 行。

### 1. MDP 定义

**形式**：L86 逐字："The routing problem is formulated as a POMDP [8], defined by the tuple $( \mathcal { S } , \mathcal { A } , \mathcal { P } , \mathcal { R } )$"。

**状态**：Eq (3)，MD L91 逐字：

> s _ { i } ( t ) = \big [ Q _ { i } ( t ) , \{ D _ { i j } ( t ) \} _ { j \in \mathcal { N } _ { i } ( t ) } , \pmb { x } _ { i } ( t ) \big ] \in \mathbb { R } ^ { d }\tag{3}

分量含义（L94 逐字）："where $\pmb { x } _ { i } ( t ) \in \mathbb { R } ^ { d _ { x } }$ are topology-related features, such as relative position information or connectivity indicators of neighboring satellites. Since global network information is not fully observable, the problem is partially observable."

即三分量：本星队列 $Q_i(t)$、到各邻居的时延集合 $\{D_{ij}(t)\}$、拓扑特征 $x_i(t)$。维度 d、$d_x$ **未给具体数值**；未说明归一化。

**动作**：L96 逐字："The action $a _ { i } ( t ) \in \mathcal { A }$ is defined as selecting the next-hop node $a _ { i } ( t ) \in \mathcal { N } _ { i } ( t )$ , where $\mathcal { A } = \mathcal { N } _ { i } ( t )$ is the action space." → 动作空间随邻居数动态变化，**无动作掩码**（grep -n -i -E "mask|feasib|legality" → **0 命中**）。

**奖励**：Eq (4)，MD L103 逐字：

> \boldsymbol { r } _ { i } ( t ) = - \left( \alpha D _ { i , a _ { i } ( t ) } ( t ) + \beta Q _ { i } ( t ) \right)\tag{4}

L106 逐字："where $D _ { i , a _ { i } ( t ) } ( t )$ is the transmission delay to the selected nexthop node, and $\alpha , \beta > 0$ are weighting coefficients [10]."

系数关系（L108）逐字："This design emphasizes congestion avoidance over distance minimization by assigning a higher weight to the queueing term $( \mathrm { i . e . , ~ } \beta ~ > ~ \alpha )$ ." **α、β 具体数值未给**；奖励未归一化；γ 见表（0.99）。

**转移/终止**：L98 逐字："The state transition probability $\mathcal { P } ( s ^ { \prime } | s , a )$ is governed by stochastic packet arrivals $A _ { i } ( t )$ , service rates $\mu _ { i } ( t )$ , and time-varying topology $\mathcal { E } ( t )$"。队列演化 Eq (1)，MD L71 逐字：

> Q _ { i } ( t + 1 ) = \operatorname* { m a x } \{ Q _ { i } ( t ) - \mu _ { i } ( t ) , 0 \} + A _ { i } ( t )\tag{1}

**episode 终止条件未给**；无资格迹/多步回报。

### 2. 学习算法与更新式

DQN（L164："a DQN [6] is employed to estimate the action-value function"，Q 值写作 $Q _ { \theta } ( h _ { i } ^ { ( t ) } , a )$，**以 LSTM 隐状态而非原始观测为输入**）。动作选择 Eq (9)，MD L167 逐字：

> a _ { i } ( t ) = \arg \operatorname* { m a x } _ { a \in \mathcal { N } _ { i } ( t ) } Q _ { \theta } ( \boldsymbol { h } _ { i } ^ { ( t ) } , a ) .\tag{9}

TD 目标 Eq (10)，MD L173 逐字：

> y _ { i } ( t ) = r _ { i } ( t ) + \gamma \operatorname* { m a x } _ { a ^ { \prime } } Q _ { \theta ^ { - } } ( \pmb { h } _ { i } ^ { ( t + 1 ) } , a ^ { \prime } ) ,\tag{10}

（L176："where $\theta ^ { - }$ are the parameters of the target network." → 原版 DQN 目标，非 double。）损失：Algorithm 1 第 16 步（L226）逐字给

> \Big ( y _ { i } ( t ) - Q ( \pmb { h } _ { i } ^ { ( t ) } , a _ { i } ( t ) ; \theta ) \Big ) ^ { 2 } ;

即 MSE。

**网络结构**（三分支串接）：

- GAT 注意力，Eq (6)，MD L135 逐字：

> \alpha _ { i j } ( t ) = \frac { \exp \left( \sigma \left( { \pmb w } ^ { T } [ { \pmb x } _ { i } ( t ) \| { \pmb x } _ { j } ( t ) ] \right) \right) } { \sum _ { k \in \mathcal { N } _ { i } ( t ) } \exp \left( \sigma \left( { \pmb w } ^ { T } [ { \pmb x } _ { i } ( t ) \| { \pmb x } _ { k } ( t ) ] \right) \right) } ,\tag{6}

- 聚合，Eq (7)，MD L143 逐字：

> z _ { i } ( t ) = \sum _ { j \in \mathcal { N } _ { i } ( t ) } \alpha _ { i j } ( t ) \pmb { x } _ { j } ( t ) ,\tag{7}

- LSTM，Eq (8)，MD L155 逐字：

> \pmb { h } _ { i } ^ { ( t ) } = \mathrm { L S T M } ( \pmb { z } _ { i } ( t ) , \pmb { h } _ { i } ^ { ( t - 1 ) } ) ,\tag{8}

超参（表 II，L242；MinerU 表格发生过列错位，以下为原文单元格顺序）：GAT attention heads = 4；GAT hidden dimension / LSTM hidden dimension = 64；Maximum training episodes = 128；Learning rate = $1 \times 1 0 ^ { - 4 }$；Discount factor γ = 0.99；Replay buffer size = 100,000；Batch size = 128；Target update frequency = 200 steps；Initial ε = 1.0；Minimum ε = 0.01；ε decay = 0.995。

ε 衰减式（Algorithm 1 第 5 步，L206）逐字：$\epsilon _ { t } = \operatorname* { m a x } ( \epsilon _ { \operatorname* { m i n } } , \epsilon _ { 0 } e ^ { - t / K _ { \mathrm { d e c a y } } } ) ;$

### 3. 信用分配

**逐跳即时奖励**（Eq (4)），仅两项：本跳到所选邻居的传输时延 + 本星队列长度。**无路径级终局奖励、无按链路因果分解、不区分损失原因**。

### 4. 状态里有没有时间信息？

**有，且是本篇的核心**：LSTM 隐状态递推（Eq (8)）把无限历史压进 $h_i^{(t)}$。L160 逐字：

> "This enables the agent to capture historical congestion patterns and link variations. Such temporal modeling is particularly important in LEO networks, where time-varying traffic arrivals, as modeled by the NHPP in Sec. II, introduce temporal correlations that cannot be captured by purely spatial methods."

注意：**窗口长度未给**（LSTM 为无限记忆，无截断长度、无 EWMA 系数），状态里也没有显式差分/趋势项。检索 grep -n -i -E "EWMA|exponential(ly)? weighted|moving average|smoothing factor" → **0 命中**。

### 5. 动作有没有时间结构？

**无**。每时隙独立选下一跳。L56 逐字："a routing agent determines the next-hop action $a _ { i } ( t ) \in \mathcal { N } _ { i } ( t )$"。无驻留、无流级缓存、无切换代价。

### 6. 多智能体设定

**完全分布式、独立智能体**。L180 逐字：

> "The proposed framework operates in a fully distributed manner. Each satellite independently constructs its local state, performs feature extraction, and determines routing actions without requiring global network information."

无参数共享、无通信、无 CTDE、无非平稳处理。检索 grep -n -i -E "VDN|QMIX|QTRAN|MADDPG|centrali[sz]ed critic|centrali[sz]ed training|parameter sharing|shared parameters|non-?stationar" → **0 命中**。

**训练/执行一致性**：Algorithm 1（L190–L228）中每个时隙对**每颗卫星**都做 GAT+LSTM+动作+存转移（第 6 步 "for each satellite $i \in \mathcal V$ do"），即所有智能体同时更新；但显式写明"各星独立"，属工程并行而非协作机制。

### 7. 训练协议

L188 逐字："we evaluate the proposed spatial-temporal learning-based distributed routing scheme in a dynamic LEO satellite network with periodically varying traffic loads... the considered constellation contains 45 satellites interconnected by ISLs, and the traffic load is varied from 120 Mbps to 240 Mbps"。

表 I（L239）：45 星；倾角 70°；高度 570 km；载频 23.28 GHz；信道带宽 25 MHz；ISL 容量 300 Mbps；Traffic load 120 / 180 / 240 Mbps；包长 1500 Bytes；最大队列 640；Max hop count (TTL) 30。

负载过程（L66 逐字）："The packet arrival process is modeled as a non-homogeneous Poisson process (NHPP), where the arrival rate $\lambda _ { i } ( t )$ varies over time. To capture temporal periodicity, $\lambda _ { i } ( t )$ is modeled as a periodic function, e.g., $\lambda _ { i } ( t ) ~ = ~ \lambda _ { 0 } \big ( 1 + \sin ( 2 \pi t / T ) \big )$"。

**训练/评估分布**：**未区分**；无 train/test 场景划分描述，未给训练步数/时长（只给 128 episodes）。基线：Dijkstra、GraphPR、DQN-IR、FDR-MARL（L232–L244）。

### 8. 该文的算法贡献

把 **GAT 空间聚合 + LSTM 时序隐状态**串接到 DQN 之前，且 **Q 函数直接以 $h_i^{(t)}$ 为输入**（Eq (9)/(10)），而非以瞬时观测为输入——这是本批唯一把"时序表征"作为策略网络输入的做法。

### 9. 该文自述的局限

L300 逐字：

> "Future work will extend this framework to QoS-aware routing, heterogeneous traffic scenarios, and cooperative multi-agent learning in large-scale LEO constellations."

（并未自述"时序窗口/消融"类局限。）

### 10. 该文没有考察的算法选择

- **未消融时序模块**：第 2 项显示 GAT/LSTM/DQN 三件套固定；全文无 "w/o LSTM"、"w/o GAT" 类对照 —— 检索 grep -n -i -E "ablation|w/o|without LSTM|without GAT" → 0 命中；因此**无法判断增益来自时序还是空间**。
- **未考察其他时序编码器**：从未比较 LSTM vs GRU vs Transformer vs 帧堆叠/EWMA（检索 grep -n -i -E "GRU|transformer|attention.{0,20}time|frame.?stack" → 0 命中）。
- **无多步回报/资格迹**（检索 0 命中）。
- **无 double/dueling/优先回放**：grep -n -i -E "double|dueling|prioriti[sz]ed replay|rainbow" → 0 命中。
- **无策略梯度族对照**：grep -n -i -E "actor.?critic|PPO|SAC|DDPG|TD3|policy gradient" → 0 命中。
- **无 CTDE/协作**：第 6 项检索 0 命中；作者自认属未来工作（L300）。
- **动作空间随邻居数变化但无掩码**：从未考察 action masking（检索 0 命中）。
- **训练分布**：只在单一 45 星 / 三档负载下评估，从未比较不同星座规模或不同流量周期 T 之间的迁移。
- **奖励只有两项且权重未给**：从未比较 β>α 之外的其他配比（检索无敏感性分析）。

### 11. 可复用的具体机制

1. **以时序隐状态为 Q 网络输入**（Eq (8)+(9)）：$h_i^{(t)} = \mathrm{LSTM}(z_i(t), h_i^{(t-1)})$，$a = \arg\max_a Q_\theta(h_i^{(t)}, a)$ —— 状态里不必显式堆历史帧，把记忆交给递归模块；转移元组也存 $h$（Algorithm 1 第 14 步）。
2. **GAT 按邻居注意力加权聚合拓扑特征**（Eq (6)+(7)）：可替换为"按链路质量的软加权"，且注意力权重可解释为下一跳偏好。
3. **周期正弦到达过程**（L66）：$\lambda_i(t) = \lambda_0 (1 + \sin(2\pi t/T))$ —— 廉价可复现的时变负载发生器，与我们关心的负载条件直接相关。

### 12. 实验合同里与"负载"相关的设置（仅作条件登记）

- 45 星，570 km，70°；ISL 300 Mbps；包长 1500 B；最大队列 640；TTL 30 跳。
- 负载 120 / 180 / 240 Mbps 三档，NHPP + 正弦周期（周期 T 未给数值）。
- 训练 128 episodes；target 每 200 步更新；ε 1.0→0.01，decay 0.995。
- 另有 "Green AI" 能效分析（L276–L296）：TDP 30 W、碳强度 495（单位见 L280）。

---

## S85KQ4FC Flow-Centric DRL for High-Throughput Routing

664 行。本批唯一把"路由粒度"本身作为算法设计变量的论文。

### 1. MDP 定义

**形式**：Eq (12)，MD L199 逐字：

> \mathcal { P } = ( S , A , T , R , O , \gamma ) .\tag{12}

**观测/状态**：L204 逐字：

> "The observation vector of satellite Sat comprises several components, and is denoted as $O _ { i } ~ = ~ \{ \Phi _ { i , k } , B _ { i } , \Theta _ { i } , \Omega _ { i } \}$ ."

逐字段：

- $\Phi _ { i , k } = \{ D i s _ { i , k } ^ { \mathrm { u p p e r } } , D i s _ { i , k } ^ { \mathrm { l o w e r } } , D i s _ { i , k } ^ { \mathrm { l e f t } } , D i s _ { i , k } ^ { \mathrm { r i g h t } } \}$（4 维，四个邻居到目的地的空间距离，由 Eq (8) 算）
- $B _ { i } = \{ b _ { i } ^ { \mathrm { u p p e r } } , b _ { i } ^ { \mathrm { l o w e r } } , b _ { i } ^ { \mathrm { l e f t } } , b _ { i } ^ { \mathrm { r i g h t } } \}$（4 维，四条 ISL 可用带宽）
- $\Theta _ { i }$（4 维，本星四个转发队列负载）
- $\Omega _ { i }$（4 维，四个邻居的决策队列负载）

**归一化**：Eq (13)，MD L207 逐字：

> x _ { n o r m } = \frac { x - x _ { \operatorname* { m i n } } } { x _ { \operatorname* { m a x } } - x _ { \operatorname* { m i n } } } .\tag{13}

**动作**：L210 逐字："Sat<sub>i</sub> can conduct one of the actions in $A _ { i } \ = \ \{ a _ { i } ^ { \mathrm { u p p e r } } , a _ { i } ^ { \mathrm { l o w e r } } , a _ { i } ^ { \mathrm { l e f t } } , a _ { i } ^ { \mathrm { r i g h t } } \}$"。4 离散动作，无掩码（grep -n -i -E "mask|feasib|legality" 的 4 处命中均为 "feasibility/scalability" 语境，见 L53/L81/L204/L333）。

**奖励**：Eq (14)，MD L215 逐字：

> r _ { i } ( t ) = \left\{ \begin{array} { l } { - \psi , \qquad \mathcal { P } _ { k } \mathrm { ~ } i s \mathrm { ~ d r o p p e d } } \\ { - \kappa _ { 1 } D i s _ { j , k } - \kappa _ { 2 } \mathcal { D } _ { i , j , k } ^ { f w d } - \kappa _ { 3 } \mathcal { D } _ { j , k } ^ { \mathrm { d e c } } , \mathrm { ~ o t h e r w i s e } } \end{array} \right.\tag{14}

三项含义（L218 逐字）："$D i s _ { j , k }$ indicates the normalized spatial distance between the next-hop satellite Sat<sub>j</sub> and the destination satellite... $\mathcal { D } _ { i , j , k } ^ { \hat { \mu } \hat { d } }$ denotes the normalized forwarding delay, and $\psi$ is a penalty value to the agent in case of packet loss. It is noted that the normalized decision delay $\mathcal { D } _ { j , k } ^ { \mathrm { d e c } }$ of routing packet $\mathcal { P } _ { k }$ on $S a t _ { j }$ is further taken into account, which is overlooked in the previous studies. Additionally, $\kappa _ { 1 } , \kappa _ { 2 }$ and $\kappa _ { 3 }$ are weights to balance the above factors."

折扣回报 Eq (15)，MD L221 逐字：

> R _ { i } ( t ) = \sum _ { n = 0 } ^ { \infty } \gamma ^ { n } r _ { i } ( t + n )\tag{15}

γ = 0.99（表 II，L415）。κ、ψ 数值**未给**。

**时延模型**：总时延 Eq (10)，MD L179 逐字：

> \mathcal { D } _ { i , k } = \underbrace { \mathcal { D } _ { i , k } ^ { q , \mathrm { d e c } } + \mathcal { D } _ { i , k } ^ { m , \mathrm { d e c } } } _ { \mathrm { d e c i s i o n ~ d e l a y } } + \underbrace { \mathcal { D } _ { i , j , k } ^ { q , f w d } + \mathcal { D } _ { i , j , k } ^ { \mathrm { p r o } } + \mathcal { D } _ { i , j , k } ^ { \mathrm { t r a n s } } } _ { \mathrm { f o r w a r d i n g ~ d e l a y } } .\tag{10}

**episode 终止未给**；无资格迹/多步回报。

### 2. 学习算法与更新式

DDQN + MADRL。ε-greedy Eq (16)，MD L234 逐字：

> a _ { i } ( t ) = \left\{ \begin{array} { l l } { \mathrm { r a n d o m ~ a c t i o n , ~ } } & { \mathrm { p r o b a b i l i t y } = \varepsilon } \\ { \mathrm { a r g m a x } _ { a } Q _ { i } ( o _ { i } ( t ) , a _ { i } ( t ) ; \mu _ { i } ) , \mathrm { p r o b a b i l i t y } = 1 - \varepsilon . } \end{array} \right.\tag{16}

目标 Eq (17)，MD L240 逐字：

> y _ { i } ( t ) = r _ { i } ( t ) + \gamma \mathrm { { m a x } } _ { a _ { i } ( t + 1 ) } Q _ { i } ^ { \prime } \big ( o _ { i } ( t + 1 ) , a _ { i } ( t + 1 ) ; \mu _ { i } ^ { \prime } \big )\tag{17}

损失 Eq (18)，MD L246 逐字：

> \operatorname { L o s s } _ { i } ( t ) = ( y _ { i } ( t ) - Q _ { i } ( o _ { i } ( t ) , a _ { i } ( t ) ; \mu _ { i } ) ) ^ { 2 } .\tag{18}

梯度步 Eq (19)，MD L252 逐字：

> \mu _ { i } = \mu _ { i } + \alpha \nabla _ { \mu _ { i } } \mathrm { L o s s } _ { i } ( t )\tag{19}

目标网软更新 Eq (20)，MD L258 逐字：

> \mu _ { i } ^ { \prime } = \tau \mu _ { i } + ( 1 - \tau ) \mu _ { i } ^ { \prime }\tag{20}

**登记两处原文不一致**：(a) Eq (17) 是原版 DQN 的 max 目标，**未体现 double-DQN 的分解**（标题却写 DDQN）；(b) Eq (19) 写成加号上升（沿梯度加），而 L249 文字说 "trained to minimize the loss"。

网络结构（表 II，L415）：Num. of network layers = 3；Num. of neurons per layer = 256；Num. of episodes = 10；Learning rate = 0.0005；Discount factor γ = 0.99；Batch size = 128；Replay buffer size = 500,000；Training frequency = 10；Optimizer = Adam；Action space = discrete。

### 3. 信用分配

**逐包逐跳即时奖励**（Eq (14)），三项可分：到目的地距离、转发时延、**下一跳的决策时延**（本篇新增项）。丢包给 −ψ 常量。**无路径级终局奖励、不区分损失原因**（丢包才区分，拥塞/环路不区分）。

### 4. 状态里有没有时间信息？

**没有**。第 1 项四组观测（距离/带宽/本星队列/邻居队列）**全部是瞬时量**，且经 Eq (13) 按 min-max 归一化 —— 归一化本身反而抹掉绝对水平。

时延抖动量 $\Delta \mathcal{D}$ 确实存在（Eq (21)），但它**不进状态、不进奖励**，只作为"是否重新推理"的触发信号（见第 5 项）。检索 grep -n -i -E "EWMA|exponential(ly)? weighted|moving average|smoothing factor|frame.?stack|stacked|previous state" → **0 命中**。

### 5. 动作有没有时间结构？

**有，且是本篇的算法贡献核心**——流级缓存 + 抖动触发的按需刷新。

流定义（L272 逐字）：

> "Definition 1: On each LEO satellite router, a traffic flow pertains to a consecutive sequence of traffic packets, which are received from the same networking port and destined for the same LEO satellite node."

缓存逻辑（L280 逐字）："the flow-centric DRL approach requires an LEO satellite to utilize DNN model to make routing decision for the first packet in a traffic flow. The route information is then stored as a corresponding entry in the LEO satellite's flow routing table, and can be directly used by the subsequent packets in the same flow."

刷新触发（Eq (21)，MD L338 逐字）：

> \Delta \mathcal { D } _ { i } ^ { \nu , k } = \left| \mathcal { D } _ { i } ^ { \nu , k } - \mathcal { D } _ { i } ^ { \nu , k - 1 } \right| .\tag{21}

刷新规则（Eq (22)，MD L368 逐字）：

> \mathrm { r o u t e } _ { i } ^ { \nu , k + 1 } = \left\{ \begin{array} { l l } { \mathrm { a r g m a x } _ { a } Q _ { i } ( o _ { i } ( t ) , a _ { i } ( t ) ; \mu _ { i } ) , ~ \Delta \mathcal { D } _ { i } ^ { \nu , k } > \theta _ { t h r } ( 2 2 ) } \\ { \mathrm { r o u t e } _ { i } ^ { \nu , k } , ~ \mathrm { o t h e r w i s e } } \end{array} \right.

即"同一流的后续包沿用缓存路由，仅当相邻两包转发时延抖动超过 $\theta_{thr}$ 时才重推理"。**无切换代价项**（换路本身不惩罚）。

动机量化（L77 逐字）："when the packet arrival rate reaches 21 000 pps (approximately 300 Mb/s, assuming a packet size of 1500 bytes), the packet routing decision delay and packet loss ratio increase to 17.5 milliseconds (ms) and 21%, respectively."

### 6. 多智能体设定

**完全分布、独立智能体**。L491 逐字：

> "the proposed flow-centric DRL operates within a fully distributed architecture where each satellite independently classifies local flows and decides nexthop routes for them, without relying on any central controllers."

无参数共享、无通信、无 CTDE、无非平稳处理。检索 grep -n -i -E "VDN|QMIX|QTRAN|MADDPG|centrali[sz]ed critic|centrali[sz]ed training|parameter sharing|shared parameters|non-??stationar" → 0 命中（L214 附近 "shared" 语境为 "a specific traffic flow"，非参数共享）。

### 7. 训练协议

L411 逐字（场景与训练规模）："We leverage the Gridded Population of the World data set released by NASA [61] to estimate user density within different regions. And the request frequency of each user follows a negative exponential distribution with an expectation of 10 pps. The destination nodes for these packets are chosen completely at random. The capability of each satellite to conduct DNN inference in parallel is set to be 8, and the network bandwidth of each ISL is 1.2 Gb/s. The upper bounds of decision and forwarding queue on each satellite are set at 400 and 200, respectively. The simulation duration is 60 min"。

两个场景（L405–L409）：Iridium-like（66 星，780 km，6×11 Walker，倾角 86.4°，用户 15 000–27 000）与 Large-Scale（12×30 Walker，500 km，用户 30 000–50 000）。

**训练/评估分布**：L405 "we conducted extensive experiments encompassing two representative scenarios, with different satellite constellation configurations and user counts" —— 同一流水线跑两个场景，**但未说明是否两场景分别训练**；episodes 仅 10。基线：OSPF、HeurOSPF、ELB、Packet-Centric DRL（L419–L427）。

### 8. 该文的算法贡献

把**路由粒度从"包"改为"流"**：每流只做一次 DNN 推理并缓存路由（L280），再叠加**无模型、纯测量的时延抖动触发刷新**（Eq (21)+(22)），从而消掉逐包推理的累积时延（动机见 L77 的 21 000 pps / 17.5 ms / 21% 丢包）。

### 9. 该文自述的局限

L493 逐字：

> "As a natural progression of our research, we intend to delve into the performance of the proposed approach in higher fidelity LSBNs characterized by more intricate constellation configurations."

（另 L326 实证性自述局限，逐字："its effectiveness gradually diminishes, particularly from the 9th batch onward, where the average delay exceeds 60 ms"。）

### 10. 该文没有考察的算法选择

- **状态完全无时间聚合**：第 4 项四组观测均为瞬时量 + min-max 归一化；检索 EWMA/滑窗/帧堆叠 → 0 命中。**从未比较"瞬时观测 vs 带历史观测"**，尽管它自己论证了网络高度时变。
- **抖动阈值 $\theta_{thr}$ 只做敏感性扫描，未做自适应**：$\theta_{thr}$ 为固定超参（Algorithm 2 L347 "Initialize delay jitter threshold $\theta _ { t h r }$"），从未考察学习/自适应阈值。
- **无 TD 目标变体比较**：Eq (17) 名义 DDQN 但公式是 max 目标，且从未比较 DQN vs DDQN（grep -n -i "double" 仅命中 L226/L491 的名称声明）。
- **无多步回报/资格迹**（检索 0 命中）。
- **无 dueling/优先回放/分布式 RL**（检索 0 命中）。
- **无策略梯度族对照**（检索 0 命中）。
- **无多智能体协作机制**：第 6 项检索 0 命中；自述"without relying on any central controllers"，从未考察 CTDE。
- **无动作掩码**（第 1 项检索）。
- **奖励权重 $\kappa_1,\kappa_2,\kappa_3,\psi$ 未给数值**，故也无权重敏感性分析。
- **训练分布**：从未比较不同训练时长（仅 10 episodes）、不同 $\theta_{thr}$ 训练/测试错配下的鲁棒性。

### 11. 可复用的具体机制

1. **流级路由缓存 + 抖动触发刷新**（Eq (21)+(22)）——**本批最接近可直接落地的机制**：
   - 抖动 $\Delta \mathcal { D } _ { i } ^ { \nu , k } = \left| \mathcal { D } _ { i } ^ { \nu , k } - \mathcal { D } _ { i } ^ { \nu , k - 1 } \right|$
   - 触发式：$\mathrm{route}^{k+1} = \arg\max_a Q(o,a)$ 若 $\Delta \mathcal{D} > \theta_{thr}$，否则沿用 $\mathrm{route}^{k}$
   它把"推理开销"从每包摊销到每流，且刷新条件**完全免模型**（只需测量转发时延），可直接叠加在我们的策略之上而不改训练。
2. **流的本地化定义**（Definition 1）："received from the same networking port and destined for the same LEO satellite node" —— 把全局流 ID 降为**本星入端口 + 目的星**的二元组，使流表规模不随源-目的用户对爆炸。
3. **决策时延入奖励**（Eq (14) 第三项 $\mathcal{D}_{j,k}^{\mathrm{dec}}$）与 **M/D/C/N 决策排队模型**（Eq (5)，MD L141：$\mathcal { D } _ { i , k } ^ { q , \mathrm { d e c } } = \frac { \mathcal { D } _ { i , k } ^ { m , \mathrm { d e c } } } { C _ { i } ^ { \mathrm { d e c } } - \lambda _ { i } ^ { \mathrm { d e c } } \mathcal { D } _ { i , k } ^ { m , \mathrm { d e c } } } = Q _ { i , k } ^ { \mathrm { d e c } } \frac { \mathcal { D } _ { i , k } ^ { m , \mathrm { d e c } } } { C _ { i } ^ { \mathrm { d e c } } }$）—— 若我们的方案要把推理开销算进端到端时延，这是现成模型。

### 12. 实验合同里与"负载"相关的设置（仅作条件登记）

- 用户需求到达：负指数分布，期望 10 pps；目的节点完全随机（L411）。
- 并行推理能力 F = 8；ISL 带宽 1.2 Gb/s；决策队列上界 400、转发队列上界 200；仿真时长 60 min。
- 用户数：Iridium-like 15 000–27 000；Large-Scale 30 000–50 000。
- 网络吞吐结果：两场景分别约 64 Gb/s 与 118 Gb/s（L487）。

## J68GU76W Reinforcement Learning for Opportunistic Routing in SDN LEO–Terrestrial Systems

256 行。本批唯一把 **backpressure 基线 + 残差策略** 引入 LEO 路由的论文。

### 1. MDP 定义

**状态**：Eq (15)，MD L156 逐字：

> S ( t ) = \{ Q _ { k } ( t ) , v _ { k } ( t ) , d _ { k } ( t ) , r _ { k } ( t ) : k \in \mathcal { K } \} .\tag{15}

四个分量的定义见 Eq (7)/(10)：$Q_k(t)$ 队列长度；$v_k(t)$ 下卸到最近网关的包数（Eq (7)，MD L82 逐字：$v _ { k } ( t ) = \left\{ \begin{array} { l l } { \mathrm { m i n } \left( Q _ { k } ( t ) , D ^ { \mathrm { L G } } R _ { k } ( t ) \right) , \mathrm { i f ~ a ~ g a t e w a y ~ i s ~ a v a i l a b l e , } } \\ { 0 , \mathrm { o t h e r w i s e , } } \end{array} \right.$）；$d_k(t), r_k(t)$ 为 ISL 总发出/接收包数（Eq (10)，MD L104 逐字：$d _ { k } ( t ) = \sum _ { m \in \mathcal { N } _ { k } ( t ) } w _ { k \to m } ( t ) , \quad r _ { k } ( t ) = \sum _ { i \in \mathcal { N } _ { k } ( t ) } w _ { i \to k } ( t )$）。

**这是全局状态**（遍历所有 $k \in \mathcal{K}$），非局部观测 —— 与同批其他"各星局部观测"论文的关键区别。全部为瞬时量，未说明归一化。

**动作**：Eq (16)，MD L162 逐字：

> a ( t ) = \{ a _ { k  m } : m \in \mathcal { N } _ { k } ( t ) , k \in K \} , \quad a _ { k  m } \in \{ 0 , 1 \} .\tag{16}

L166 逐字给出包调度关系："with scheduled packets given as; $w _ { k \to m } ( t )$ [=] $a _ { k \to m } ( t ) D ^ { \mathrm { I S L } } \log _ { 2 } ( 1 + \Gamma _ { k \to m } ( t ) )$"。即**二值链路激活**（不是比例/下一跳选择）。无掩码（grep -n -i -E "mask|feasib|legality" → L107 "queue feasibility constraint"，为容量约束非掩码）。

**奖励**：Eq (18)，MD L178 逐字：

> R ( t ) = - \Big [ \alpha \left( \bar { Q } _ { \mathrm { a } } ( t + 1 ) - \bar { Q } _ { \mathrm { B P } } ( t + 1 ) \right) + \beta \left( Q _ { \mathrm { a } } ^ { \operatorname* { m a x } } ( t + 1 ) - Q _ { \mathrm { B P } } ^ { \operatorname* { m a x } } ( t + 1 ) \right) \Big ] ,

即**相对 backpressure 基线的差分奖励**（L181 逐字："where $\bar { Q } _ { \mathrm { a } } ( t + 1 )$ and $Q _ { \mathrm { a } } ^ { \operatorname* { m a x } } ( t + 1 )$ are the mean and maximum queue lengths under the agent's actions, respectively, and $\bar { Q } _ { \mathrm { B P } } ( t { + } 1 )$ and $Q _ { \mathrm { B P } } ^ { \operatorname* { m a x } } ( t { + } 1 )$ are the corresponding values under backpressure, respectively. The weights $\alpha , \beta > 0$ control the trade-off between reducing overall congestion and protecting the worst-case queues."）。α、β 数值未给；奖励未归一化。

目标函数 Eq (19)，MD L187 逐字：$\pi ^ { * } = \underset { \pi } { \mathrm { a r g m a x } } ~ \mathbb { E } _ { \pi } \left[ \sum _ { t = 0 } ^ { \infty } \gamma ^ { t } R ( t ) \right] ,$（"where $\gamma \in ( 0 , 1 )$ represents the discount rate"）。

**转移/终止**：队列演化 Eq (12)，MD L116 逐字：

> Q _ { k } ( t + 1 ) = ( Q _ { k } ( t ) + u _ { k } ( t ) + r _ { k } ( t ) - v _ { k } ( t ) - d _ { k } ( t ) ) ^ { + }\tag{, ∀k}

（L119："where $( x ) ^ { + } = \operatorname* { m a x } ( 0 , x )$"。）episode 终止条件未给；无多步回报。

**残差策略基座**（Eq (14)，MD L146 逐字）：

> \pi _ { \mathrm { B P } } : s _ { k  m } ^ { \mathrm { B P } } ( t ) = \big ( Q _ { k } ( t ) - Q _ { m } ( t ) \big ) C _ { k  m } ^ { \mathrm { I S L } } ,\tag{14}

（L149："a link is activated between two satellites k and its neighbor m if $s _ { k  m } ^ { \mathrm { B P } } > 0$"。）

### 2. 学习算法与更新式

L202 逐字："To learn a residual policy over the backpressure baseline, we adopt a Double Deep Q-Network (DDQN) agent [17], which extends the classical Q-learning framework by approximating the state–action value function with a DNN, and by decoupling the action selection and action evaluation through a target network."

**无 TD 目标公式、无损失公式**（全文未给）。网络：L204 "under identical settings (3 layers, 256 hidden units each)"。

残差的具体注入方式（Eq (17)，MD L172 逐字）：

> \pi _ { \mathrm { L G - B P } } : s _ { k  m } ^ { \mathrm { L G } } ( t ) = s _ { k  m } ^ { \mathrm { B P } } ( t ) + \lambda ^ { \mathrm { L G - B P } } C _ { m } ^ { \mathrm { L G } } ,\tag{17}

（L175："where $C _ { m } ^ { \mathrm { L G } } = D ^ { \mathrm { L G } } \log _ { 2 } ( 1 + \Gamma _ { m } ^ { \mathrm { LG } } ( t ) )$ is the downlink capacity of neighbor m and $\lambda ^ { \mathrm { LG - j B P } }$ is a weight balancing ISL backlog reduction against downstream LG availability."）

**注意**：Eq (17) 是**解析的加性修正**（把 LG 容量加权加到 BP 分数上），而非学习到的残差网络输出；真正"学习"的部分（DDQN）与 Eq (17) 的解析修正**如何组合，文中未给出公式** —— 这是读该篇最关键的缺口。

### 3. 信用分配

奖励是**与基线对比的差分**（Eq (18)）：均值队列改善 + 最大队列改善两项，逐时隙即时。**无路径级终局奖励、无按节点/链路分解、不区分损失原因**（该文未建丢包模型，L198："Queues for the satellites are assumed unbounded, so buffer overflow is not explicitly modeled"）。

### 4. 状态里有没有时间信息？

**没有**。Eq (15) 四项全为瞬时量（队列、下卸量、发出量、接收量）。检索 grep -n -i -E "EWMA|exponential(ly)? weighted|moving average|smoothing factor" → 0 命中；grep -n -i -E "frame.?stack|stacked|historical|history|previous state|past state|memory" → 0 命中。

背景里确实有周期性（L137 逐字："although the network topology changes rapidly, it exhibits quasi-periodic patterns driven by orbital mechanics, allowing the reinforcement learning agent to exploit these patterns"），但**该周期性只体现在到达过程 $M_{\mathrm{tod}}(h)$（Eq (4)，MD L64 逐字：$\lambda _ { k } ( t ) = M _ { \mathrm { t o d } } ( h ( t ) ) \int _ { A _ { k } ( t ) } \rho _ { k } ( \mathbf { r } ) \mathrm { d } A$，其中 $M _ { \mathrm { t o d } } ( h ) = \alpha \sin ( 2 \pi ( h - \tau ) / 24 ) + \beta$），并不进入状态**。

### 5. 动作有没有时间结构？

**无驻留/无缓存**。每个时隙（$\Delta t$ = 60 s）重新决定全网的链路激活二值向量。无切换代价项。

### 6. 多智能体设定

**不是多智能体**：单一中心智能体、全局状态、全局动作（Eq (15)/(16) 均为全 $\mathcal{K}$ 遍历）。L139 逐字：

> "the SDN-based reinforcement learning framework can benefit from the global view of the network provided by the SDN controller on the GEO satellites, enabling centralized decision-making, while still allowing for distributed packet forwarding in the data plane."

L141 明确列出两个难点（逐字）："1) The action space is not fixed but varies with the number of neighbors $| \mathcal { N } _ { k } ( t )$ |... 2) The reward feedback is delayed and highly coupled, since the queue dynamics in (12) depend jointly on all agents' actions across the network."

检索 grep -n -i -E "VDN|QMIX|QTRAN|MADDPG|centrali[sz]ed critic|CTDE" → 0 命中（"centralized decision-making" 为架构描述）。

### 7. 训练协议

L198 逐字："We use Space-Track [16] APIs to obtain TLE data for satellite positions, and the 2020 Gridded Population of the World dataset to model ground traffic... Simulations span three consecutive days with slot length $\Delta t = 6 0 \mathrm { ~ s }$ . Unless specified otherwise, the Starlink constellation with $K = 1 0$ satellites is used for the simulation, with $M = 4$ neighbors per satellite... the reported results are averaged over five independent runs of the evaluated methods. The environment is implemented in PyTorch and Gymnasium, and the reinforcement learning model was trained using the NVIDIA A100 GPU."

训练规模：L204 "over 100 episodes under identical settings"。**注意 $K = 10$ 卫星** —— 远小于真实星座，是个"子网/概念验证"规模。

**训练/评估分布**：星座在 Starlink / Iridium / OneWeb 之间切换评估（L215），但**未说明是否同一模型跨星座泛化**（措辞为 "we compare performance of various methods across Starlink, Iridium, and OneWeb constellations"）。

### 8. 该文的算法贡献

把 **backpressure 作为先验基线、RL 只学残差**，并把"邻居是否可下卸到网关"的能力 $C_m^{\mathrm{LG}}$ 作为加性项并入链路激活分数（Eq (17)），奖励改为相对基线的差分（Eq (18)）。L204 报告增益：残差策略相对 vanilla DDQN 提升 643.81%，相对 residual policy baseline 提升 34.01%。

### 9. 该文自述的局限

L221 逐字：

> "Future work will address scalability to mega-constellations, account for delays between the GEO controller and LEO satellites, and ensure consistent implementation of the reinforcement learning framework."

### 10. 该文没有考察的算法选择

- **残差注入方式唯一且为解析式**：Eq (17) 是手写加性项，**从未考察其他残差形式**（乘性、门控、学习式残差网络），也**未说明 DDQN 输出与 Eq (17) 的合成公式**。
- **无 TD 目标/损失公式**：第 2 项；无法判断 double 分解是否实现，**从未比较 DQN vs DDQN**。
- **无多步回报/资格迹**（检索 0 命中）。
- **无 dueling/优先回放/分布式 RL**（grep -n -i -E "dueling|prioriti[sz]ed replay|noisy net|distributional|rainbow" → 0 命中）。
- **无策略梯度族对照**（grep -n -i -E "actor.?critic|PPO|A2C|SAC|DDPG|TD3|policy gradient" → 0 命中）。
- **状态完全无时间聚合**（第 4 项检索 0 命中）：从未比较瞬时状态 vs 带历史状态，尤其讽刺的是它自己承认拓扑"quasi-periodic"。
- **动作无时间结构**：从未考察链路激活的驻留/最小保持时长（这会直接影响振荡）。
- **不做多智能体**：从未考察分布式（局部观测）与集中式（全局观测）的对比 —— 而 L141 自己指出全局动作空间随星座规模爆炸。
- **无动作掩码**（第 1 项检索）。
- **训练分布**：从未做跨星座（Starlink→Iridium）的迁移实验，只做同场景对比。
- **非平稳**：L141 自认奖励"delayed and highly coupled"，但**从未考察任何非平稳处理机制**（检索 non-stationar → 0 命中）。

### 11. 可复用的具体机制

1. **backpressure 先验 + 加性修正**（Eq (14)+(17)）：$s _ { k m } ^ { \mathrm { B P } } = ( Q _ { k } - Q _ { m } ) C _ { k m } ^ { \mathrm { I S L } }$，$s _ { k m } ^ { \mathrm { L G } } = s _ { k m } ^ { \mathrm { B P } } + \lambda ^ { \mathrm { L G - B P } } C _ { m } ^ { \mathrm { L G } }$ —— 把"确定性最优但短视"的调度规则作为骨架，只让 RL 学"是否向正在经过网关的邻居偏移"。**对我们的方案**：可把"向地面站/Gateway 方向重路由"做成这一类加性先验项，避免 RL 从零学可用性。
2. **相对基线的差分奖励**（Eq (18)）：$R(t) = -[ \alpha ( \bar{Q}_a - \bar{Q}_{BP} ) + \beta ( Q_a^{max} - Q_{BP}^{max} ) ]$ —— 奖励尺度自动跟随负载（基线表现差时动作空间大），缓解"负载变化导致奖励尺度漂移"的问题，与 CMNCS52M 的 R 定标规则是同一问题的两种解法。
3. **均值 + 最坏值双目标**（Eq (18) 两项）：同时优化平均拥塞与最大队列，是"公平性/最坏情形"最小成本实现。

### 12. 实验合同里与"负载"相关的设置（仅作条件登记）

- 到达过程 Eq (4)：$\lambda _ { k } ( t ) = M _ { \mathrm { t o d } } ( h ( t ) ) \int _ { A _ { k } ( t ) } \rho _ { k } ( \mathbf { r } ) \mathrm { d } A$，昼夜因子 $M _ { \mathrm { t o d } } ( h ) = \alpha \sin ( 2 \pi ( h - \tau ) / 24 ) + \beta$（α 幅度、β 基线、τ 峰值相位，数值未给）。
- 包到达为 Poisson：Eq (5)，MD L70 逐字：$u _ { k } ( t ) \sim \operatorname { P o i s } ( \lambda _ { k } ( t ) )$。
- 3 天仿真，$\Delta t$ = 60 s，K = 10 星，M = 4 邻居，队列无界（不建丢包）。
- 5 次独立重复取平均；基线：Backpressure、Equalize、No-ISL、Max-Weight、Random（L194）。

---

## CYMQ2GLA Two-Hops State-Aware Routing (DRL-THSA, Double-DQN)

418 行。**本批唯一在"链路状态预测"里做了显式时间聚合（带自适应系数的 EWMA 式滤波）的论文。**

### 1. MDP 定义

**形式**：L190 逐字："an agent is modeled as a four-tuple consisting of {S, A, P, R}"。表 3（L196）登记：

- State S = $\mathsf { S t a t e } ( [ N _ { s } , N _ { d } , L S T ] )$ —— 源节点、目的节点、当前星链路状态表
- Action A = $\mathrm { A c t i o n } ( N _ { n e x t } )$ —— 下一跳卫星
- P = $\mathrm { P o s s i b i l i t y } \left( P _ { n e x t } \right)$，Eq (13)，MD L201 逐字：$P _ { n e x t } = \left( \sum _ { i = 1 , 2 , . . . , m } s _ { i } \right) ^ { - 1 }$（L204："where m represents the number of neighbors for current satellite node, and $s _ { i }$ represents the number of link states of neighbor satellite i."）
- R = Reward (r)

**LST 的字段**（表 2，MD L141 逐字）：Node N / Direction n / Connectedness (On/Off) / Link State (Free/Busy/Congested) / Timestamp t。→ 状态是**离散三元组 + 时间戳**，无连续负载数值。

**动作**：$N_{next}$ 四方向（L44："Each satellite has four ISLs, including two intra-plane ISLs and two inter-plane ISLs"）。**无动作掩码**（grep -n -i -E "mask|feasib|legality" → 0 命中），环路靠运行时探测规避（见第 5 项）。

**奖励**：Eq (14)+(15)，MD L209/L213 逐字：

> d i f ( N _ { s } , N _ { d } ) = \alpha \cdot \left( R A A N _ { s } - R A A N _ { d } \right) ^ { 2 } + \beta \cdot \operatorname* { m i n } \lbrack \vert \omega _ { s } - \omega _ { d } \vert ^ { 2 } , ( 2 \pi - \vert \omega _ { s } - \omega _ { d } \vert ) ^ { 2 } \rbrack\tag{14}

> r = \left\{ \begin{array} { l c r } { { r _ { d } } } & { { } } & { { N _ { n e x t } = N _ { d } } } \\ { { - r _ { c } } } & { { } } & { { N _ { n e x t } f a i l e d / c o n g e s t e d } } \\ { { - d i f ( N _ { s } , N _ { d } ) } } & { { } } & { { O t h e r } } \end{array} \right.\tag{15}

L216 逐字："where RAAN represents right ascension of ascending node. ω represents the mean anomaly. α and $\beta$ are the weights of inter-plane ISLs and intra-plane ISLs. We define $r _ { d }$ as a high reward for success and $- r _ { c }$ as a punishment for mistake."

**奖励是"轨道几何距离"而非时延/队列** —— 拥堵只通过 $N_{next}$ 失败/拥塞的 −r_c 进入，且 −r_c 为常量（数值未给）。$r_d$、$r_c$、α、β 均未给数值。折扣 γ 未在正文给（表 1 未列）。

**转移/终止**：episode 终止未定义；Algorithm 2（L247）中有 "if an episode terminates at iteration j + 1 then Set $Y _ { j } ^ { D D Q N } = r _ { d }$"，即**终局目标值直接置为 $r_d$（不做 bootstrap）**。

### 2. 学习算法与更新式

算法名（3.2.1）：Double-DQN。L224 逐字："We propose to use the DDQN which is composed of an online DNN with weight $\theta ^ { o n l i n e }$ and a target DNN with weights $\theta ^ { t a \mathrm { r g e t } }$ . The online DNN updates its weights $\theta ^ { o n l i n e }$ at each iteration. The target DNN resets its weights $\theta ^ { t a \mathrm { r g e t } }$ to $\theta ^ { o n l i n e }$ in every $N ^ { t a r g e t }$ iterations and keeps weights $\theta ^ { t a \mathrm { r g e t } }$ fixed at other iterations."

损失 Eq (16)，MD L227 逐字：

> { \cal L } ^ { D D Q N } = { [ { \cal Y } ^ { D D Q N } - { \cal Q } ( s , a , \theta ^ { o n l i n e } ) ^ { 2 } ] }\tag{16}

目标 Eq (17)，MD L233 逐字：

> Y ^ { D D Q N } = r + \gamma Q ( s ^ { \prime } , \mathrm { a r g m a x } Q _ { i } ( s ^ { \prime } , a ^ { \prime } ; { \theta } ^ { o n l i n e } ) ; { \theta } ^ { t a \mathrm { r g e t } } )\tag{17}

→ **这是本批唯一写出真正 double-DQN 分解式的论文**（action selection 用 online，evaluation 用 target）。Eq (16) 的括号位置在原文中即如此（平方在方括号内），属排版笔误。

Algorithm 2（L238–L257）逐字要点：输入 $A ; N ^ { t a r g e t } ; N _ { b } ; M$；每 episode 每 iteration 用 ε-greedy 执行；存 $< s , a , r _ { t } , s ^ { \prime } >$ 于 M；终局置 $Y _ { j } ^ { D D Q N } = r _ { d }$，否则 $a = \arg \operatorname* { m a x } Q ( s ^ { \prime } , a ^ { \prime } ; \theta ^ { o n l i n e } )$ 并置 $Y _ { j } ^ { D D Q N } = r _ { j } + \gamma Q ( s ^ { \prime } , a ; \theta ^ { t a r g e t } )$；梯度下降更新 $\theta^{online}$；每 $N^{target}$ 次重置。

网络结构：**未给层数/宽度/激活**（全文无）。每星一个模型（L259 逐字："For the whole LEO satellite networks, the number of DDQN is equal to the number of satellites."）。ε = 0.9（表 4，L302；L363："according to the training efficiency and the convergence degree of the network, the ε-greedy value of DDQN is chosen as 0.9"）。

### 3. 信用分配

三支分段（Eq (15)）：到达目的地 $+r_d$；下一跳失败/拥塞 $-r_c$；其余 $-\mathrm{dif}(N_s, N_d)$。逐跳即时。**不区分失败原因**（failed 与 congested 用同一 $-r_c$）。**无路径级终局回报**（终局是 $+r_d$ 而非路径累计）。

### 4. 状态里有没有时间信息？

**有——在链路状态预测里，且带自适应系数**。这是本篇与我方选题最相关的部分。

输入/输出速率的指数滤波，Eq (1)(2)，MD L60/L64 逐字：

> I _ { a v g } = ( 1 - \lambda _ { I } ) \cdot I _ { a v g } ( t - t _ { c } ) + \lambda _ { I } \cdot I _ { a v g } ( t )\tag{1}

> O _ { a v g } = ( 1 - \lambda _ { O } ) \cdot O _ { a v g } ( t - t _ { c } ) + \lambda _ { O } \cdot O _ { a v g } ( t )\tag{2}

L67 逐字说明其作用："The short-term light traffic load needs to be filtered. Therefore, the selection of $\lambda _ { I }$ and $\lambda _ { O }$ are essential. If these weights are too large, the average packet rate will nearly equal the instantaneous traffic load. Otherwise, if these weights are too small, it is hard for the average packet rate to represent the long-range traffic load... In this paper, the values of $\lambda _ { I }$ and $\lambda _ { O }$ are assigned dynamically according to the traffic load by Equations (3) and (4)."

自适应系数 Eq (3)(4)，MD L70/L74 逐字：

> \lambda _ { I } = \left\{ \begin{array} { l l } { \operatorname* { m a x } \biggr \{ \frac { I _ { a v g } ( t ) } { I _ { a v g } ( t - t _ { c } ) } \cdot \alpha _ { 1 } , a _ { 0 } \biggr \} , I _ { a v g } ( t ) < I _ { a v g } ( t - t _ { c } ) } \\ { \operatorname* { m i n } \biggr \{ \frac { I _ { a v g } ( t ) - I _ { a v g } ( t - t _ { c } ) } { I _ { a v g } ( t - t _ { c } ) } , \alpha _ { 2 } \biggr \} } \end{array} \right.\tag{3}

> \lambda _ { O } = \left\{ \begin{array} { l l } { \operatorname* { m a x } \Bigl \{ \frac { O _ { a v g } ( t ) } { O _ { a v g } ( t - t _ { c } ) } \cdot \alpha _ { 1 } , a _ { 0 } \Bigr \} , O _ { a v g } ( t ) < O _ { a v g } ( t - t _ { c } ) } \\ { \operatorname* { m i n } \Bigl \{ \frac { O _ { a v g } ( t ) - O _ { a v g } ( t - t _ { c } ) } { O _ { a v g } ( t - t _ { c } ) } , \alpha _ { 2 } \Bigr \} } \end{array} \right.\tag{4}

（α0=0.02, α1=0.1, α2=0.3，表 4 L302。）

**预测占用率**（把滤波结果外推一个检查周期），Eq (5)(6)，MD L82/L88 逐字：

> q = \frac { L ( t ) } { L _ { \operatorname* { m a x } } } \in [ 0 , 1 ]\tag{5}

> p = q + \frac { \left[ I _ { a v g } - O _ { a v g } \right] \cdot t _ { c } } { L _ { \operatorname* { m a x } } }\tag{6}

**由预测反解阈值**，Eq (9)(10)，MD L108/L112 逐字：

> T _ { 1 } = \operatorname* { m i n } ( \operatorname* { m a x } ( 1 - \frac { 2 \big [ I _ { a v g } - O _ { a v g } \big ] \cdot t _ { c } } { L _ { \operatorname* { m a x } } } , 0 ) , 1 )\tag{9}

> T _ { 2 } = \operatorname* { m i n } ( \operatorname* { m a x } ( 1 - \frac { \left[ I _ { a v g } - O _ { a v g } \right] \cdot t _ { c } } { L _ { \operatorname* { m a x } } } , 0 ) , 1 )\tag{10}

状态分级（L115 逐字）："The link state is marked as Free State (FS) when $q$ is below $T _ { 1 }$ and is considered to be Busy State (BS) if q is between $T _ { 1 }$ and $T _ { 2 }$ . It is defined as Congested State (CS) when q exceeds $T _ { 2 }$"；且 L93："$p \geq 1$: It means packet drop may happen in the next $t _ { c }$ seconds. Therefore, the link state is set to be congested whatever the current queue occupancy rate is."

→ 即：**状态里的 LST 是"滤波后外推的预测等级"，不是瞬时等级**。这是本批唯一一处显式的、带自适应系数的时序状态设计。

### 5. 动作有没有时间结构？

**部分有**：路由重算周期 600 ms（表 4 L302："Routing recomputation period 600 ms"），但**决策本身仍逐包**（Algorithm 3 第 5–9 步每包输入 DDQN 推理两次：当前跳与两跳）。**无动作驻留、无流级缓存、无切换代价**。

环路处理是**运行时探测**而非学习（L291 逐字）："if the $N _ { t w o }$ is equal to $N _ { c } ,$ it means endless-loop occurs. We suppose the link connectedness of the current next-hop satellite $N _ { n e x t }$ to be of during this routing process. Repeat the routing strategy until the $N _ { t w o }$ is not equal to $N _ { c }$ ."（"of" = "off" 的 OCR 笔误。）

### 6. 多智能体设定

**每星一个独立 DDQN**（L259 逐字："the number of DDQN is equal to the number of satellites"），参数**不共享**、无 CTDE、无非平稳处理。唯一的邻居间交互是 LST 广播（L145："the current satellite updates its LST and sends the link state change messages to its neighbor satellites"）。检索 grep -n -i -E "VDN|QMIX|QTRAN|MADDPG|centrali[sz]ed critic|CTDE|parameter sharing|non-?stationar" → 0 命中。

### 7. 训练协议

L220 逐字（离线训练 + 部署后冻结）：

> "Due to limited resources and processing capacity on the satellite, we simulate the flows of the satellite networks and complete the DDQN training process on the ground. The of-line training process enables the DDQN model to cope with all the link states that may be encountered. Then the trained DDQN models are stored on the satellite and no longer updated during the satellite routing process."

L299 逐字（仿真设置）："we use NS-3.29 (Network Simulator 3, Version 3.29) as the simulation tool to construct the simulations in an Iridium-like satellite network with 66 satellites distributed over six planes... The capacity of ISLs is set to 25Mbps. The average packet size is set to 1 KB and the queue length is set to 100 packets. We utilize 200 On–Of flows and the On–Of period of each flow follows a Pareto distribution with the shape of 1.5. The average burst and idle time are both set to 500ms... All the simulations are run for 60s equivalent to that in [9]. All scenarios are run 100 times, and the average values are considered as the final results."

**训练/评估分布**：**未区分**；未给训练 episode 数/迭代数（$N^{target}$、$N_b$、M 在 Algorithm 2 是输入但数值未给）。基线：ELB、TLR、ELMDR（L304）。

### 8. 该文的算法贡献

(1) **带自适应系数的速率滤波 + 外推预测**（Eq (1)–(10)），把链路状态从"瞬时占用"改为"下一检查周期内的预期等级"；(2) **两跳状态感知**（当前星 LST + 邻居 NLST，Algorithm 1 L149–L182），并据此在推理时连续调用两次 DDQN 做环路探测。

### 9. 该文自述的局限

L293 逐字：

> "However, it is not applicable to the networks where the number of disconnected links is destructive."

L363 逐字：

> "In future research, we will study the impact of deep learning network structure and parameter settings on routing strategy performance."

### 10. 该文没有考察的算法选择

- **网络结构完全未给**：第 2 项显示无层数/宽度/激活；作者自己在 L363 承认"deep learning network structure"是未来工作 → **从未比较任何网络结构**。
- **无 TD 目标变体比较**：虽然 Eq (17) 是唯一真正的 double 分解式，但**从未比较 DQN vs DDQN**（grep -n -i "double" 命中仅名称）。
- **无多步回报/资格迹**（grep -n -i -E "n-step|multi-step|eligibility trace|lambda-return" → 0 命中），终局直接置 $r_d$ 不 bootstrap。
- **无 dueling/优先回放/分布式 RL**（grep -n -i -E "dueling|prioriti[sz]ed replay|noisy net|distributional|rainbow" → 0 命中）。
- **无策略梯度族对照**（grep -n -i -E "actor.?critic|PPO|A2C|SAC|DDPG|TD3|policy gradient" → 0 命中）。
- **滤波窗口机制未消融**：自适应 λ（Eq (3)(4)）是本篇卖点，但**从未比较固定 λ vs 自适应 λ**，也从未比较不同 $t_c$（表 4 固定 30 ms）。
- **奖励与时延/队列解耦**：Eq (14) 只用轨道几何（RAAN/mean anomaly），**从未把时延或队列数值直接放进奖励**（只有离散的 failed/congested 触发 −r_c）—— 这是与同批其他论文最大的分歧点。
- **动作无时间结构**：600 ms 重算周期固定，从未考察驻留时长/重算频率的敏感性。
- **无多智能体协作**（第 6 项检索 0 命中）。
- **无动作掩码**：环路用运行时"假装断链"的 hack（L291），**从未考察可学习的环路规避或动作掩码**。
- **训练分布**：只在 66 星 Iridium-like 单场景；从未做跨星座/跨负载分布的迁移。

### 11. 可复用的具体机制

1. **自适应系数 EWMA + 外推预测 → 状态分级**（Eq (1)–(6)+(9)(10)）——**本批最完整的"把时间维度做进状态"的现成件**：
   - 滤波：$I_{avg} = (1-\lambda_I) I_{avg}(t-t_c) + \lambda_I I_{avg}(t)$
   - 外推：$p = q + \frac{[I_{avg} - O_{avg}] \cdot t_c}{L_{max}}$
   - 反解阈值：$T_2 = \min(\max(1 - \frac{[I_{avg}-O_{avg}] \cdot t_c}{L_{max}}, 0), 1)$
   与 S85KQ4FC 的"阈值触发"不同，这里阈值本身由观测量反解，**无需调参即可随负载自适应**。
2. **两跳前瞻作为推理期环路探测**（Algorithm 3 第 6–10 步）：连续两次前向推理检查 $N_{two} \neq N_c$，把"环路规避"从训练期移到推理期 —— 与 CMNCS52M 的 visit-counter 训练期方案形成互补，两者可叠加。
3. **状态变更广播 + 时间戳去重**（Algorithm 1，L164–L182）：只广播"状态变化的链路"，收方校验时间戳后更新 NLST —— 低开销的一致性维护模式。

### 12. 实验合同里与"负载"相关的设置（仅作条件登记）

- 表 4（L302）：高度 780 km；极区边界纬度 70；路由重算周期 600 ms；ISL 带宽 25 Mb/s；上下行 25 Mb/s；包长 1 kB；仿真时长 60 s；α0=0.02、α1=0.1、α2=0.3；$t_c$ 队列检查间隔 30 ms；ISL 缓冲队列 100；$t_s$ 期望驻留自由态时间 200 ms；$t_h$ HELLO 周期 30 ms；$t_d$ ACK 最大等待 30 ms；ε=0.9。
- 流量：200 个 On–Off 流，On–Off 周期 Pareto(shape=1.5)，平均 burst/idle 各 500 ms；传输速率 2.5–3.5 Mbps 与流数 200–300 两组扫描（L310）。
- 66 星 6 平面 Iridium-like；每场景跑 100 次取平均。

---

## XLRW7XXN DQN-Based Load Balancing Routing

217 行。本批篇幅最短、算法细节最少的一篇（会议短文）。

### 1. MDP 定义

**形式**：L102 逐字："Deep Q network is currently a popular deep reinforcement learning algorithm. And it is usually described as a Markov model. It can be represented as a quadruple(s, $a , s ^ { \prime } , r )$"。

**状态**：L135 逐字：

> "the state space consists of link states and node information, mainly including the satellite node where the data packet is currently located, the load situation of adjacent satellite links, and the connectivity and distance between each satellite node. It is divided into three state matrices: position relationship matrix, load matrix, and distance matrix, which are merged into one state."

→ 三个矩阵拼接成"一张多通道图"，**维度未给**，未说明归一化。

**动作**：L135 逐字："Actions represent next hop node selection... each node is connected to four adjacent nodes, representing four output directions and four actions. Meanwhile, real-time connectivity of the four links is considered for judgment, and different output values are given."（4 离散动作；连通性作为"judgment"，**无显式掩码**，grep -n -i -E "mask|feasib|legality" → 0 命中。）

**奖励**：Eq (13)，MD L138 逐字：

> r e w a r d = - \omega _ { 1 } * d _ { n } - \omega _ { 2 } * C _ { n } + \omega _ { 3 } * B _ { n }\tag{13}

L141 逐字："where reward represents the reward. And $d _ { n }$ represents the distance to the destination node. $C _ { n }$ represents congestion levels of node n, $C _ { n } = q _ { n } / Q _ { m } .$ $q _ { n }$ represents the current queue length, and $Q _ { m }$ indicates the maximum queue length. $B _ { n }$ represents the remaining available bandwidth of the link, $\omega_1, \omega_2, \omega_3$ represents the weight coefficient, $\omega _ { 1 } + \omega _ { 2 } + \omega _ { 3 } = 1$ . The weight coefficient can be adjusted according to the network situation."

→ 三项归一化后可加权（权重和为 1），但**具体权重值未给**；折扣 γ 见表 1 的 "Reward attenuation 0.9"。

**转移/终止**：未给。

### 2. 学习算法与更新式

DQN。Q 函数定义 Eq (9)–(12)，MD L107/L113/L119/L125 逐字：

> Q ( s , a ) = E _ { \pi } [ G _ { t } | S _ { t } = s , A _ { t } = a ]\tag{9}

> G _ { t } = R _ { t + 1 } + \gamma R _ { t + 2 } + \cdot \cdot \cdot = \sum _ { k = t } ^ { T } \gamma ^ { k - t } R ( s _ { k } , a _ { k } )\tag{10}

> Q _ { \pi } ( s _ { t } , a _ { t } ) = E \bigl [ R ( s _ { t } , a _ { t } ) + \gamma E _ { a _ { t + 1 } \sim \pi } Q _ { \pi } ( s _ { t + 1 } , a _ { t + 1 } ) \bigr ]\tag{11}

> a = \arg \operatorname* { m a x } _ { a \in A } Q ( s , a )\tag{12}

**无 TD 目标的显式写法、无损失函数公式**（L128 仅文字："The DQN algorithm constructs labels for algorithm training through reward values of behavior, and the experience replay and target network effectively reduce the connections between datasets"）。

网络结构（L172 逐字）："The neural network in the DQN model uses CNN to better utilize its matrix computing power for processing multidimensional resources and extracting features. The CNN model contains two convolutional layers with 16 and 32 convolutional kernels respectively."

超参（表 1，L177）：Height of LEO track 895.5 km；Number of LEO satellites 8×8；Orbit inclination angle 86.4°；Channel capacity 100 Mb/s；Maximum data rate 2Mb/s；Size of packets 512 bit；Maximum queue length 100；Patch size 200；Learning rate 0.01；Soft update network weight 0.3；Action exploration attenuation 0.998；Minimum exploration rate 0.1；Reward attenuation 0.9。

### 3. 信用分配

**逐跳即时标量**（Eq (13)），三项线性组合：到目的地距离、本节点拥塞度、剩余带宽。**无路径级终局奖励、不区分损失原因**，且拥塞项用的是**节点**而非**下一跳节点**（$C_n$ 的 n 指代在原文中未明确是当前节点还是候选下一跳 —— 登记为原文歧义）。

### 4. 状态里有没有时间信息？

**没有**。三矩阵（位置关系/负载/距离）均为当前快照。检索 grep -n -i -E "EWMA|exponential(ly)? weighted|moving average|smoothing factor" → 0 命中；grep -n -i -E "frame.?stack|stacked|historical|history|previous state|past state|memory" → 仅 L27（"field of vision" 假匹配）与 L146（"Experience replay" 语境），均非状态历史项。

仅有"时隙 T"这一**拓扑更新节拍**（L152："Set the topology update duration T, timer t"），不是状态里的时间特征。

### 5. 动作有没有时间结构？

**无**。逐包决策（Algorithm 1 的 for packet i = 1 to n 循环），仅拓扑/链路状态按 T 周期更新（L161–L163）。无驻留、无缓存、无切换代价。

### 6. 多智能体设定

**不是多智能体**：单控制器集中收集状态。L102 逐字：

> "In the routing model of the LEO satellite network in this paper, the controller collects link states and node information of the network at regular intervals as the state space for training routing strategies. The controller uses this routing strategy to output the optimal next hop node"

L146 逐字补充："network topology information is transmitted to each satellite node... Then, each node sends requests to each other and establishes connections, then shares network status and node information."

检索 grep -n -i -E "multi-?agent|independent agent" → **0 命中**（本批唯一完全不含此词的论文）。

### 7. 训练协议

L146 逐字："The offline stage of the DQN routing model mainly utilizes historical traffic data and simulated data for learning... In the online phase, the connection and distance between nodes in the satellite network are first calculated within the time slot, and network topology information is transmitted to each satellite node. The number and size of data packets are set, and the state of each node is initialized and initial loads following a Poisson distribution are allocated."

L172 逐字："Generate a single-layer LEO constellation of 64 satellites using STK, with a total of 8 orbits, each with 8 satellites. The orbit altitude is 895.5km and the inclination angle is 86.4°. Use STK's corresponding functions to calculate the connection status and distance between satellite nodes, and generate a link matrix and a distance matrix."

**训练/评估分布**：**未区分**；未给训练时长/步数/收敛曲线。基线仅两个：Dijkstra 最短路径、最大流算法（L174）。

### 8. 该文的算法贡献

把三张网络矩阵（位置关系、负载、距离）作为 CNN 多通道输入做 DQN，奖励为"距离 + 拥塞 + 剩余带宽"三目标的线性加权（Eq (13)），用于负载均衡。相对基线，其"贡献"主要是**多目标加权奖励 + 矩阵式状态表示**。

### 9. 该文自述的局限

**未见自述**。检索：grep -n -i -E "limitation|future work|drawback|shortcoming" 于该篇全文 → 0 命中；L192–L194 的 Conclusion 全为总结性正面陈述，无局限句。

### 10. 该文没有考察的算法选择

- **无 TD 目标/损失公式**：第 2 项；**从未比较 DQN vs DDQN**（grep -n -i "double" → 0 命中，连名称都未出现）。
- **无多步回报/资格迹**（grep -n -i -E "n-step|multi-step|eligibility trace|lambda-return" → 0 命中）。
- **无 DQN 变体/回放策略消融**（grep -n -i -E "dueling|prioriti[sz]ed replay|noisy net|distributional|rainbow" → 0 命中）。
- **无策略梯度族对照**（grep -n -i -E "actor.?critic|PPO|A2C|SAC|DDPG|TD3|policy gradient" → 0 命中）。
- **奖励权重从未研究**：L141 只说 "can be adjusted according to the network situation"，**全文无权重取值、无敏感性分析**。
- **状态无时间聚合**（第 4 项检索）：从未比较瞬时状态 vs 带历史状态。
- **动作无时间结构**：从未考察驻留/摊销。
- **无多智能体设定**：第 6 项检索 0 命中；从未考察分散式决策。
- **网络结构未消融**：CNN 两卷积层（16/32）是唯一配置，从未比较 MLP vs CNN（尽管其状态本身就是矩阵，这一对比本应自然）。
- **训练分布**：单一 64 星星座，单一负载条件；从未比较不同负载强度下的迁移。
- **无动作掩码**（第 1 项检索）。

### 11. 可复用的具体机制

1. **三目标线性加权奖励**（Eq (13)）：$reward = -\omega_1 d_n - \omega_2 C_n + \omega_3 B_n$，$\sum \omega_i = 1$，其中拥塞度用**归一化队列占用** $C_n = q_n / Q_m$、带宽用**剩余可用带宽** —— 三项量纲统一到 [0,1] 区间，是"量纲对齐"的廉价做法（对比 CMNCS52M 用 R 定标、J68GU76W 用差分基线）。
2. **状态即矩阵、用 CNN 提取**（L135+L172）：位置关系矩阵 / 负载矩阵 / 距离矩阵拼成多通道图输入。对小星座（8×8）成本可接受。
3. **软更新系数 0.3**（表 1 "Soft update network weight 0.3"）：与 S85KQ4FC 的硬性 Eq (20) $\mu' = \tau\mu + (1-\tau)\mu'$ 同类，可作我们实现时的默认值参照。

### 12. 实验合同里与"负载"相关的设置（仅作条件登记）

- 64 星（8 平面 × 8 星），895.5 km，倾角 86.4°；信道容量 100 Mb/s；单任务最大速率 2 Mb/s；包长 512 bit；最大队列 100。
- 初始负载服从 Poisson 分布（L172）；源/目的节点由任务指定。
- 对比基线：Dijkstra 最短路径、最大流算法（L174）。
- 评估指标：端到端时延（Fig. 4）、吞吐量（Fig. 5）、参与转发的卫星数（Fig. 6，"反映负载均衡"）。

## 5PYWVRC5 Shaping Rewards, Shaping Routes（FD-MADRL 路由的奖励塑形研究）

**重复条目说明**：5PYWVRC5 与 L2VKYTAV 为同一篇的两个入库副本，MD 正文逐字节相同（md5 均为 b116d516852ae09a832f7e658d1ed602，均 123 行，均为 20434 字节）。本篇按 itemKey **5PYWVRC5** 记录一次；L2VKYTAV 不再重复拆解。以下行号对两个副本通用。

作者：Manuel M. H. Roth, Anupama Hegde, Thomas Delamotte, Andreas Knopp（DLR / UniBw München）。这是一篇 **workshop/short paper**（含 Acknowledgment、References 共 123 行），核心内容是**奖励塑形的系统刻画**，而非新算法。

### 1. MDP 定义

**状态**：L29 逐字（一句话，无公式）：

> "For FD-MADRL, the state space consists of information about the adjacent link loads, the previous hop and the destination."

→ 三个分量：邻居链路负载、**上一跳**（previous hop）、目的地。**无维度、无归一化说明**。注意 "previous hop" 是唯一的记忆类字段，但它是**空间路标**（防环）而非时间量。

**动作**：L29 逐字："The action space emcompasses the available ISLs, so the available next hops."（原文 "emcompasses" 为笔误。）4 条 ISL（L17："we assume four ISLs on each satellite as in [6]"）。无掩码（grep -n -i -E "mask|feasib|legality" → 0 命中）。

**奖励**：本篇的重点，**给了三个公式**。

全局奖励（含 T 步滞后），Eq (2)，MD L39 逐字：

> r _ { t + T } ^ { G } = w _ { 1 } U ( t ) - w _ { 2 } L ( t ) - w _ { 3 } D ( t )\tag{2}

（L33 逐字："At time step t, the global reward of an agent can capture relevant end-to-end characteristics. Specifically, the flow-specific latency L(t), the maximum or average link utilization $U ( t ) .$ , and the resulting packet dropping rate D(t) can be considered. Each metric is weighted by a factor, denoted as $w _ { 1 } , w _ { 2 } ,$ and $\boldsymbol { w } _ { 3 }$ . However, this reward is only received after a significant time lag, denoted by $T ,$ , due to the multi-hop propagation delays."）

局部奖励，Eq (3)，MD L45 逐字：

> r _ { t + 1 } ^ { L } = w _ { 4 } \delta _ { t h } ^ { L } ( t ) - w _ { 5 } l ^ { L } ( t ) - w _ { 4 } d ^ { L } ( t )\tag{3}

（**原文笔误登记**：第三项应为 $w_6$，原文写作 $w_4$；L42 明确 "these metrics are weighted by factors, denoted as $w _ { 4 } , w _ { 5 } ,$ , and $\boldsymbol { w } _ { 6 }$"，故 Eq (3) 与文字自相矛盾。）

**最终用于 FD-MADRL 的局部奖励**，Eq (4)，MD L53 逐字（8 分支分段函数）：

> r _ { t + 1 } ^ { \prime } = \left\{ \begin{array} { l l } { + \Psi , } & { \mathrm { i f ~ g o a l ~ r e a c h e d } } \\ { + \psi , } & { \mathrm { i f ~ o v e r a l l ~ p a t h ~ r e d u c t i o n } } \\ { - \psi , } & { \mathrm { i f ~ o v e r a l l ~ p a t h ~ e x t e n s i o n } } \\ { - \Psi , } & { \mathrm { i f ~ p a t h ~ n o t ~ r e d u c e d } \ \& \log } \\ { + \xi _ { 1 } , } & { \mathrm { i f ~ l i n k ~ l o a d < 0 . 4 } } \\ { - \xi _ { 2 } , } & { \mathrm { i f ~ 0 . 4 < l i n k ~ l o a d \leq 0 . 8 } } \\ { - \xi _ { 3 } , } & { \mathrm { i f ~ l i n k ~ l o a d > 0 . 8 } } \\ { - \Xi , } & { \mathrm { i f ~ l i n k ~ s a t u r a t e d } } \end{array} \right.\tag{4}

（"& log" 为 "& loop" 的 OCR 笔误。）

系数关系（L48–L50 逐字）："Instead of using local delays, we utilize the estimated resulting decrease in distance towards the destination, as in [4]. We denote the value of this path reduction ψ. Most importantly, to form coherent paths, loops have to be punished, but only at the nodes which are actually causing them. In this case a punishment −Ψ is received, which should be at least a magnitude higher than ψ. Including a similarly large reward, so +Ψ, for a successful path improved training performance - even though it was not propagated to all nodes along the path." / "To incentivise decentralized load balancing, a threshold-based approach proved effective. The utilized values of ξ are in the domain of ψ for balanced paths. Depending on which policy is more desired, the values for ψ and ξ can be varied. −Ξ punishes the usage of saturated links, which results in packet drops. As we intend to strongly discourage this behaviour, −Ξ is in the domain of −Ψ."

→ **所有系数只给定性量级关系（Ψ ≫ ψ，Ξ ~ Ψ），无具体数值。**

折扣 γ：Eq (1)（MD L24）中出现 $\gamma$，但**未给数值**。

**转移/终止**：episode 终止＝到达目的节点（Eq (4) 的 "+Ψ, if goal reached"）。**有跨 episode 的状态耦合**（见第 5 项）——这是本篇最独特的一点。

### 2. 学习算法与更新式

DQN（L27："DQNs utilize DNNs to approximate the Q-function in complex routing environments. During training, agents interact with the environment and store their experiences in replay bufers for increased stability."）。

Q 值更新（Bellman 式），Eq (1)，MD L24 逐字：

> Q ( s _ { t } , a _ { t } ) = r _ { t } + \gamma \operatorname* { m a x } _ { a _ { t + 1 } } Q ( s _ { t + 1 } , a _ { t + 1 } )\tag{1}

**无 target network 公式、无损失公式、无 ε 策略公式**。实现（L60 逐字）："a specifically designed environment was created using the gym library [8]. The DQN functionality were implemented using Keras for Tensorflow [9, 10]."

**网络结构未给**（层数/宽度/激活全无）。**超参全无**。这与本篇"只研究奖励设计"的定位一致（L60 逐字："Due to the limited scope of this manuscript, only the described reward design is investigated."）。

### 3. 信用分配

**按"造成问题的那个节点"精准归因**——这是本篇的核心论点。L48 逐字：

> "Most importantly, to form coherent paths, loops have to be punished, but only at the nodes which are actually causing them."

并明确指出路径级奖励的传播问题（L48）："+Ψ ... even though it was not propagated to all nodes along the path."

同时也指出**全局奖励的时滞**（Eq (2)，滞后 T 步）与**分布式不可用性**（L48 逐字："For fully decentralized designs, composite rewards are typically not considered [3, 4]. The limited scope makes it difficult to evaluate the impact of individual actions of independent agents."）。

→ **本批对"信用分配"问题论述最深入的一篇**：它把"奖励该发给谁"作为独立研究对象。

### 4. 状态里有没有时间信息？

**没有**。第 1 项三个分量（邻居链路负载 / 上一跳 / 目的地）均为瞬时或静态。检索 grep -n -i -E "EWMA|exponential(ly)? weighted|moving average|smoothing factor" → 0 命中；grep -n -i -E "frame.?stack|stacked|historical|history|previous state|past state|memory" → 0 命中（"previous hop" 未被该检索覆盖，但它本身是空间量）。

**但时间性体现在奖励上**：Eq (2) 的全局奖励滞后 T 步、Eq (3) 的局部奖励滞后 1 步 —— 论文把"奖励到达时间"当作设计变量（L33："this reward is only received after a significant time lag, denoted by T"），这在本批中是唯一如此表述的。

### 5. 动作有没有时间结构？

**无动作驻留/缓存**。但**有跨 episode 的环境耦合**——本批独有，L78 逐字：

> "The idea is to test the robustness of the approach by evolving the state space according to previously made decisions. This corresponds more to an actual SCN scenario, where routing decisions impact future states and link loads change dynamically. In a sense, we investigate subsequent snapshots of the constellation. To this end, we change the network to be affected by the previous action trajectory: an additional load of 20% is added to each utilized link of the previous episode. These additional loads are only episode-specific, to avoid saturation on all links."

→ 即"上一 episode 用过的链路，本 episode 负载 +20%"。这是**直接针对"路由决策反作用于负载"**的机制。

### 6. 多智能体设定

FD-MADRL：每星独立智能体、各自模型、局部知识。L27 逐字：

> "While CDRL is based on a singular agent, in FD-MADRL, each satellite is assumed to act as an independent agent with its own model and only partial knowledge of the environment."

无参数共享、无通信、**无 CTDE**；但**明确把 CL-DC（集中学习-分散控制）作为提出的方向**。检索 grep -n -i -E "VDN|QMIX|QTRAN|MADDPG|centrali[sz]ed critic|CTDE" → 0 命中；L92 的 "Centralized Learning - Decentralized Control (CL-DC)" 与 "multi-agent actor-critic" 是**讨论中的未来架构**，非本文实现。

L92 逐字（提议架构）："To balance these concepts, future research may consider a hybrid approach based on Centralized Learning - Decentralized Control (CL-DC)... a central controller provides guidance, while decisions are made locally by the agents. Local actions and rewards are forwarded to the central entity for learning."

### 7. 训练协议

L60 逐字：

> "The resulting grid network represents a sub-network of an SCN, e.g. a cluster in a distributed architecture [6]. For the comparisons we use a cluster of 12 satellites as well as a cluster of 24 satellites with varied link loads. The larger cluster is shown in Fig. 1. While the loads are set randomly, they comply with observed link characteristics of plausible non-uniformly distributed traffic scenarios [6]. For this performance comparison, we focus on the latency on a per-hop basis, i.e. the hop count, as well as the link loads."

两个设置：(a) **静态**路径寻找（Fig. 2/3）；(b) **动态可变链路负载**（Fig. 4，即第 5 项的 +20% 耦合）。

**训练/评估分布**：12 节点与 24 节点两规模对比（L66："more than twice as many episodes are required to achieve maximum rewards consistently"）。**未给 episode 数、步数、训练时长**。

### 8. 该文的算法贡献

(1) 对 FD-MADRL 的**局部奖励塑形**做系统刻画：给出 Eq (4) 的 8 分支分段奖励（含"只在致环节点惩罚"与基于 0.4/0.8 阈值的负载分档），并与 Eq (2)(3) 的全局/局部复合奖励对照；(2) 提出**决策反作用于负载的动态场景**（L78 的 +20% 耦合）来暴露短视；(3) 提出 CL-DC 混合架构（未实现）。

### 9. 该文自述的局限

L87 逐字：

> "For FD-MADRL, we have shown that the limited scope of each agent negatively impacts the end-to-end routes, in both static and dynamic scenarios. Moreover, with increasingly complex policies, the agents have to learn the behavior of other agents, which is counterproductive for scalability."

L94 逐字：

> "In conclusion, while DQN-based architectures represent promising solutions for routing and network control in complex SCNs, they still have practical limitations. The investigated FD-MADRL approaches face scaling challenges, particularly in mastering complex scenarios where they are expected to surpass state-of-the-art methods. In-depth investigations are required to fully evaluate their actual viability."

### 10. 该文没有考察的算法选择

- **未实现所提的 CL-DC**：第 6 项；L92 明说是 "future research may consider"，**从未做集中学习 vs 分散学习的实验对照**。
- **未考察 actor-critic**：L92 提到 "future research may also focus on policy gradient techniques for multi-agent actor-critic architectures [12]"，**只有展望无实验**（检索 grep -n -i -E "actor.?critic|PPO|A2C|SAC|DDPG|TD3|policy gradient" → 命中仅 L92 与参考文献 L124）。
- **无 TD 目标/损失公式、无网络结构**：第 2 项；**从未比较任何网络或算法变体**（L60 自认 "only the described reward design is investigated"）。
- **无多步回报/资格迹**：grep -n -i -E "n-step|multi-step|eligibility trace|lambda-return" → 0 命中；但它自己识别了"奖励时滞 T"问题（Eq (2)），却**未考察任何时滞补偿手段**（reward shaping potential、delay-aware credit assignment 等）。
- **无 DQN 变体**：grep -n -i -E "dueling|prioriti[sz]ed replay|noisy net|distributional|rainbow|double" → 0 命中。
- **状态完全无时间聚合**（第 4 项检索）：从未比较瞬时状态 vs 带历史状态。
- **动作无时间结构**：从未考察驻留/摊销（尽管第 5 项已引入负载与决策的耦合，这本是研究"决策频率"的天然场景）。
- **未研究奖励系数数值**：Ψ、ψ、ξ、Ξ 只给定性量级（第 1 项引文），**从未做系数的敏感性扫描**——而这是"reward shaping"论文最该做的实验。
- **无动作掩码**（检索 0 命中）。
- **网络规模非真实星座**：12/24 节点的 grid 网络，**从未在真实 Walker 星座或真实轨道动力学下验证**。
- **无负载分布变化的迁移研究**：负载"randomly"设置且"episode-specific"，从未比较不同负载强度/分布的泛化。

### 11. 可复用的具体机制

1. **8 分支分段奖励（局部、只在致环节点惩罚）**（Eq (4)）——**本批最值得直接借用奖励设计**。它的三个设计要点可逐条搬走：
   - 目标达成给大正 $+\Psi$ 且**大正奖励不上溯到路径所有节点**（L48）；
   - 环路惩罚 $-\Psi$ **只发给真正致环的节点**，量级 $\gg \psi$；
   - 链路负载用 0.4 / 0.8 两档阈值离散化（$+\xi_1$ / $-\xi_2$ / $-\xi_3$），饱和链路 $-\Xi$（$\Xi \sim \Psi$）。
   对我们：把"是否造成环路""是否把包推向饱和链路"做成**只归因到当前节点的离散奖惩**，可与连续项（如 CMNCS52M 的 $t_{\mathrm{HOP}}$）叠加。
2. **决策反作用于负载的 episode 耦合**（L78）："an additional load of 20% is added to each utilized link of the previous episode" —— 一个极低成本的机制，用来把"路由的长期后果"引入训练，避免策略只学"当下最短"。可直接作为我们训练环境的负载演化规则。
3. **全局奖励的显式时滞项**（Eq (2)）：$r _ { t + T } ^ { G } = w _ { 1 } U ( t ) - w _ { 2 } L ( t ) - w _ { 3 } D ( t )$，把"端到端指标 T 步后才可得"写成公式 —— 若我们要做"路径级奖励 + 分布式执行"，这是需要显式面对的时滞建模起点（尽管该文未解决它）。

### 12. 实验合同里与"负载"相关的设置（仅作条件登记）

- 网络：**grid 子网**，12 星与 24 星两档；每星 4 条 ISL（L17）。
- 负载：随机设置，但"comply with observed link characteristics of plausible non-uniformly distributed traffic scenarios [6]"（L60）。
- 动态场景：上一 episode 使用过的链路 +20% 负载，且仅 episode 内有效（L78）。
- 链路负载阈值：0.4 / 0.8 / 饱和（Eq (4)）。
- 对比基线：动态多代价 Dijkstra（SPF），且"Links with high link loads (> 80% of capacity used) are actively avoided"（L74）。
- 评估指标：每跳时延（hop count）与路径上最大链路负载（Fig. 3）。

---

## 本批小结（Batch 1：深度 DQN/MARL 族，7 篇 / 8 个 itemKey）

### 一、本批共同采用的算法范式

7 篇全部落在 **value-based、离散动作、off-policy 的 DQN 家族**，无一例外：

| 篇 | 算法名（原文写法） | TD 目标公式 | 状态是否含时间聚合 | 动作是否有时间结构 | 多智能体 |
|---|---|---|---|---|---|
| CMNCS52M | DQN-LSNR（称 DDQN） | 有 Eq(5)，但是 max 目标 | 无（仅包级 visit counter） | 无 | 独立 |
| 42E4NAQU | DDQN | **无公式** | 无 | 无 | 集中训练+分布执行+在线 |
| LZKNZA8B | GAT-LSTM-DQN | 有 Eq(10)，max 目标 | **有（LSTM 隐状态）** | 无 | 独立 |
| S85KQ4FC | MADRL（称 DDQN） | 有 Eq(17)，但是 max 目标 | 无 | **有（流级缓存+抖动刷新）** | 独立 |
| J68GU76W | DDQN + 残差策略 | **无公式** | 无 | 无 | 单集中智能体 |
| CYMQ2GLA | Double-DQN（DRL-THSA） | 有 Eq(17)，**真 double 分解** | **有（自适应 EWMA 预测）** | 部分（600 ms 重算节拍） | 独立 |
| XLRW7XXN | DQN | **无公式** | 无 | 无 | 单集中控制器 |
| 5PYWVRC5 | DQN（FD-MADRL） | 仅 Eq(1) Bellman 式 | 无 | 无（但有 episode 间负载耦合） | 独立 |

共同点（每一条都有上文的行号与引文支撑）：

1. **奖励一律是标量、逐跳即时**，没有任何一篇把奖励分解到"链路 × 时间"的二维结构上。
2. **动作空间一律是"四邻居选一"**（J68GU76W 的链路激活二值、S85KQ4FC 的四方向概率是仅有的两个变体），且**全部没有动作掩码**——掩码相关检索在 7 篇里全为 0（CMNCS52M/CYMQ2GLA/XLRW7XXN/5PYWVRC5 为 0 命中；其余命中均为 "feasibility/scalability" 语境的假匹配）。
3. **训练与评估分布基本同一套**：只有 CMNCS52M 系统随机化了训练星座（3–12 平面 × 4–16 星/面）并做 130 配置外推；其余 6 篇全部单场景训练单场景评估。
4. **"DDQN" 多为名义称呼**：4 篇自称 DDQN，但只有 CYMQ2GLA 写出了真正的 double 分解式（Eq (17)：selection 用 $\theta^{online}$、evaluation 用 $\theta^{target}$）；CMNCS52M（Eq (5)）与 S85KQ4FC（Eq (17)）的公式仍是原版 max 目标。
5. **离线训练 + 星上冻结推理**是共同部署范式（CMNCS52M L191、CYMQ2GLA L220、XLRW7XXN L146），只有 42E4NAQU 声称部署后在线更新（且无消融）。

### 二、本批共同【没有】考察什么

1. **没有一篇做过"状态里有没有时间信息"的消融**。LZKNZA8B 有 LSTM、CYMQ2GLA 有 EWMA 预测，但两者都**从未比较"带时序 vs 不带时序"**（LZKNZA8B 全文无 ablation 检索结果）。这意味着"时序到底有没有用"在本批中**是空白**——恰好是我们选题可以正面回答的问题。
2. **没有一篇比较过不同训练分布**。负载分布的差异（CMNCS52M 三模型、J68GU76W 三种星座）都是"各自训练各自评估"，从未测"在 A 分布训练、在 B 分布评估"。
3. **没有一篇做过多步回报 / 资格迹 / n-step**（7 篇检索全 0 命中）。全部是 1-step TD。
4. **没有一篇做过 dueling / 优先回放 / 分布式 RL / Rainbow 类变体**（7 篇检索全 0 命中）。
5. **没有一篇用过策略梯度族**（PPO/SAC/DDPG/TD3 检索全 0 命中）；actor-critic 仅出现在 5PYWVRC5 的未来工作展望里。
6. **没有一篇实现过真正的 MARL 协作机制**（VDN/QMIX/QTRAN/MADDPG/CTDE 检索全 0 命中）。所谓"多智能体"全部是"每星一个独立 DQN + 局部观测"，**无参数共享、无通信、无集中 critic、无针对非平稳的处理**。5PYWVRC5 与 42E4NAQU 各自把"集中学习-分散控制"写进未来工作，但本批无人做。
7. **没有一篇把"推理开销/决策时延"作为一等算法变量**——只有 S85KQ4FC 正面处理（且用工程手段而非学习手段），CYMQ2GLA 的 600 ms 重算节拍是隐式处理。
8. **公平性/能耗**：检索 "fairness|jain|energy consumption|power consumption" 在 7 篇中，除 LZKNZA8B 的 "Green AI" 计算碳排分析（L276–L296）与几处参考文献标题外，**无一篇把公平性或能耗写进奖励**。

### 三、本批里最接近可复用机制的 2–3 条（含公式）

**第 1 条（首选）：S85KQ4FC 的"流级路由缓存 + 时延抖动触发刷新"**（MD L338 / L368）

- 刷新判据：$\Delta \mathcal { D } _ { i } ^ { \nu , k } = \left| \mathcal { D } _ { i } ^ { \nu , k } - \mathcal { D } _ { i } ^ { \nu , k - 1 } \right|$
- 路由更新：$\mathrm { r o u t e } _ { i } ^ { \nu , k + 1 } = \left\{ \begin{array} { l l } { \mathrm { a r g m a x } _ { a } Q _ { i } ( o _ { i } ( t ) , a _ { i } ( t ) ; \mu _ { i } ) , ~ \Delta \mathcal { D } _ { i } ^ { \nu , k } > \theta _ { t h r } } \\ { \mathrm { r o u t e } _ { i } ^ { \nu , k } , ~ \mathrm { o t h e r w i s e } } \end{array} \right.$
- 流的定义：$\text{flow} \equiv (\text{入端口}, \text{目的星})$，与源用户解耦。

**为什么最可复用**：它是本批唯一一个**把"决策时刻"本身作为算法变量**的机制，且**完全免模型**（只测量转发时延），可以叠加在任何已有策略之上而不改变训练过程——对我们的"动作时间结构"这一选题目是最直接的起点。

**第 2 条：CYMQ2GLA 的"自适应系数 EWMA + 外推预测 → 状态分级"**（MD L60/L64/L70/L74/L88/L108）

- 滤波：$I _ { a v g } = ( 1 - \lambda _ { I } ) \cdot I _ { a v g } ( t - t _ { c } ) + \lambda _ { I } \cdot I _ { a v g } ( t )$
- 自适应系数：$\lambda _ { I } = \left\{ \begin{array} { l l } { \operatorname* { m a x } \biggr \{ \frac { I _ { a v g } ( t ) } { I _ { a v g } ( t - t _ { c } ) } \cdot \alpha _ { 1 } , a _ { 0 } \biggr \} , I _ { a v g } ( t ) < I _ { a v g } ( t - t _ { c } ) } \\ { \operatorname* { m i n } \biggr \{ \frac { I _ { a v g } ( t ) - I _ { a v g } ( t - t _ { c } ) } { I _ { a v g } ( t - t _ { c } ) } , \alpha _ { 2 } \biggr \} } \end{array} \right.$
- 外推与阈值反解：$p = q + \frac { \left[ I _ { a v g } - O _ { a v g } \right] \cdot t _ { c } } { L _ { \operatorname* { m a x } } }$，$T _ { 2 } = \operatorname* { m i n } ( \operatorname* { m a x } ( 1 - \frac { \left[ I _ { a v g } - O _ { a v g } \right] \cdot t _ { c } } { L _ { \operatorname* { m a x } } } , 0 ) , 1 )$

**为什么可复用**：这是本批唯一**把时间维度真正做进状态**（而非只做进网络结构）的设计，且**阈值由观测量反解而非超参**，可随负载自适应。与 LZKNZA8B 的 LSTM 方案形成两种可对照的"时间进状态"路线（显式统计量 vs 学习表征）——这正是我们选题可以做的对照实验。

**第 3 条：CMNCS52M 的"visit-counter 放大的单跳代价" + 5PYWVRC5 的"只在致环节点惩罚"**（MD L166 / L172；MD L53）

- CMNCS52M：$r _ { i } ^ { a } = \left\{ \begin{array} { l l } { R , } & { \mathrm { i f ~ } j = D } \\ { - R , } & { \mathrm { i f ~ } j = - 1 } \\ { - \big ( t _ { \mathrm { H O P } } ( i , j , L ) \times ( 1 + \mathbf { h } _ { i } ( a ) ) } & { \mathrm { o t h e r w i s e } } \end{array} \right.$，$t _ { \mathrm { H O P } } ( i , j , L ) = t _ { \mathrm { P } } ( i , j ) + t _ { \mathrm { T X } } ( L ) + t _ { \mathrm { Q } } ( j )$
- 5PYWVRC5：Eq (4) 的 $-\Psi$ 只发给"actually causing them"的节点（见 L48 引文）

**为什么可复用**：两者解决的是同一个问题（环路与拥塞的信用分配）的**两种互补范式**——CMNCS52M 把它塞进连续奖励的乘性系数（训练期、隐式），5PYWVRC5 把它做成离散分支的精确归因（显式、只在过错节点）。二者**在原理上可以叠加**，且都无需改动网络结构。

---

## 附：本批拆解完整性与核验说明

- 覆盖：CMNCS52M、42E4NAQU、LZKNZA8B、S85KQ4FC、J68GU76W、CYMQ2GLA、XLRW7XXN、5PYWVRC5（= L2VKYTAV 重复副本，已注明）。
- 每篇均给出 12 项；奖励/更新式均抄 LaTeX 原文；原文笔误与 MinerU 表格错位均已就地标注。
- 判"未见"的检索方式：对每篇 MD 全文执行 grep -n -i -E，检索词与命中情况逐条写在该篇第 4/10 项内；检索范围＝该篇 MD 全文行数（CMNCS52M 374 / 42E4NAQU 197 / LZKNZA8B 341 / S85KQ4FC 664 / J68GU76W 256 / CYMQ2GLA 418 / XLRW7XXN 217 / 5PYWVRC5 123）。

**⚠️ 负向声明的权威证据以「附录 A」为准**（精确检索模式原文 + 实测计数 + 命中位置与判定）。正文第 4/10 项中的检索描述为早期宽模式版本；若与附录 A 冲突，以附录 A 为准。

---

# 附录 A：负向声明（"未见/没有 X"）的精确检索证据

**检索方式**：grep -n -iE，逐条给出**模式原文 / 实测计数 / 命中位置与判定**。凡有命中一律给出位置并说明**为何不构成反例**。

| itemKey | 全文行数 | | itemKey | 全文行数 |
|---|---|---|---|---|
| CMNCS52M | 374 | | J68GU76W | 256 |
| 42E4NAQU | 197 | | CYMQ2GLA | 418 |
| LZKNZA8B | 341 | | XLRW7XXN | 217 |
| S85KQ4FC | 664 | | 5PYWVRC5 | 123 |

## A.1 模式 P1 — DQN 变体（dueling / 优先回放 / 分布式 RL）

模式原文：
**double[- ]?(q|dqn)|dueling|prioriti[sz]ed (experience )?replay|noisy net|distributional|c51|rainbow**

| 篇 | 实测计数 | 命中位置与判定 |
|---|---|---|
| CMNCS52M | **2** | L81、L256 —— **均为图片文件名哈希**（"…b2c51bdb743…"、"…d833ac51c3b4de…"），命中子串 c51。**实质命中数 = 0**。另：L131 的算法名 "Double Deep Q-Network" 未被本模式命中（写作 double-deep 而非 double-dqn），属**模式覆盖不足**，人工核对确认该名称存在。 |
| 42E4NAQU | 0 | — |
| LZKNZA8B | 0 | — |
| S85KQ4FC | **3** | L192 "incorporates double DQNs (DDQNs)"（**仅名称声明**；其 TD 目标 Eq (17) 仍是 max 形式，见正文第 2 项）；L541 参考文献 [23] 标题 "Distributional reinforcement learning-based router…"（**他引标题**）；L621 参考文献 [63] Van Hasselt "Deep reinforcement learning with double Q-learning"（**他引标题**）。→ **均不构成"比较过 DQN 变体"的反例**。 |
| J68GU76W | **1** | L257 参考文献 [17] Van Hasselt double Q-learning 标题。**他引，非本文实验**。 |
| CYMQ2GLA | **6** | L222/L224/L238/L261 等，均为**本文算法名** "Double-DQN" 的正常出现（该篇确实实现了 double 分解）。**不构成反例**；本篇"未比较 DQN vs DDQN"由"全文无对照实验"支撑，非由计数支撑。 |
| XLRW7XXN | 0 | — |
| 5PYWVRC5 | **1** | L110 参考文献 [5] "Hierarchical Deep Double Q-Routing" 标题。**他引，非本文实验**。 |

## A.2 模式 P2 — 多步回报 / 资格迹

模式原文：**n-step|multi-step|eligibility trace|lambda-return**
→ **8 篇全部实测计数 0**（无任何命中，含参考文献）。"全部为 1-step TD"成立。

## A.3 模式 P3 — 策略梯度族

模式原文：**actor-?critic|\bppo\b|\ba2c\b|\ba3c\b|\bsac\b|\bddpg\b|\btd3\b|policy gradient**

| 篇 | 实测计数 | 命中位置与判定 |
|---|---|---|
| CMNCS52M / 42E4NAQU / LZKNZA8B / J68GU76W / CYMQ2GLA / XLRW7XXN | 0 | — |
| S85KQ4FC | **1** | L41 —— 命中词 **actor-critic**，位于**相关工作**："Liu et al. [16] proposed DRL-OR-S, a highly scalable online routing algorithm using a novel graph-based actor-critic network architecture." **他引，非本文方法**。 |
| 5PYWVRC5 | **3** | L90（图 5 标题 "actor-critic approach using Centralized Learning and Decentralized Control"）、L92（正文 "future research may also focus on policy gradient techniques for multi-agent actor-critic architectures"）、L124（参考文献 [12] Lowe et al. MADDPG 标题）。**L90/L92 属未来工作展望，L124 属他引**；本文实验未用任何策略梯度方法。 |

## A.4 模式 P4 — MARL 协作机制 / CTDE

模式原文：**\bvdn\b|qmix|qtran|maddpg|centrali[sz]ed critic|\bctde\b|parameter sharing|shared (network )?parameters**
→ **8 篇全部实测计数 0**。"无一篇实现协作式 MARL"成立。

> 注：42E4NAQU L129 含 "centralized training" 字样（"This centralized training enables the model to capture the overall traffic dynamics"），**未被本模式命中**（模式限定 centrali[sz]ed **critic**）。人工核对确认该处为**架构描述**而非 CTDE 机制，见正文该篇第 6 项引文。

## A.5 模式 P5 — 动作掩码

模式原文：**action mask|masking|invalid action|illegal action|infeasible action**
→ **8 篇全部实测计数 0**。

> 注：正文另查过宽模式 **mask|feasib|legality**，CMNCS52M 有 3 处命中（L46 相关工作、L125 路径可行性约束、L151 visit counters memory），**均为散文词而非动作掩码**。采用收紧模式后为 0。

## A.6 模式 P6 — 状态中的时间聚合

模式原文：**ewma|exponentially weighted|moving average|smoothing factor|frame[- ]stack|stacked (frames|observations)|sliding window**

| 篇 | 实测计数 | 命中位置与判定 |
|---|---|---|
| CMNCS52M | **1** | L185 "showing the **moving average** of the long-term reward of the last 100 episodes" —— **训练曲线的平滑画法**，非状态特征。**不构成反例**。 |
| 其余 7 篇 | 0 | — |

> **重要限制（防止误导）**：本模式**不覆盖** LZKNZA8B 的 LSTM（Eq (8)）与 CYMQ2GLA 的 EWMA 式滤波（Eq (1)(2)）——后两者是**真实的时间聚合机制**，但表述为 "LSTM" / "$\lambda_I$" 而不含上述关键词。因此正文对这两篇的判定是"**有**时间信息，并已逐字引述公式"；本模式仅用于支撑**其余篇目**的"无时间聚合"结论。

## A.7 模式 P7 — 训练分布迁移

模式原文：**curriculum|domain randomi|transfer learning|meta-learning|fine-tun**
→ **8 篇全部实测计数 0**。"无一篇做过 training→evaluation 分布迁移"成立。

## A.8 模式 P8 — 公平性 / 能耗

模式原文：**fairness|jain index|energy consumption|power consumption**

| 篇 | 实测计数 | 命中位置与判定 |
|---|---|---|
| CMNCS52M | **1** | L97 —— "This adaptive modulation strategy helps reduce **power consumption** and conserves satellite resources…"（**系统模型里的速率自适应描述**，非奖励项、非优化目标）。 |
| 42E4NAQU | **1** | L15 —— 相关工作综述句 "…with a focus on latency, **power**…"（**背景陈述**）。 |
| LZKNZA8B | **3** | L278/L280/L292 —— "Green AI" 能效/碳排**评估**（TDP 30 W、碳强度 495），是**事后指标**，未进入奖励或状态。 |
| 其余 5 篇 | 0 | — |

**结论**：无一篇把公平性或能耗写进奖励函数；LZKNZA8B 只在评估侧做了能耗核算。

---

# 附录 B：对抗性问题 G-A 的库级回答

> **问题 G-A**：全库是否有任何工作，把**同一个失败事件**（丢包 / 超时 / 溢出）按**物理原因**拆成**不同的学习通道或惩罚项**（例如区分"决策缓存溢出"与"链路队列溢出"）？

**检索范围**：全库 **111** 个 itemKey 的 MD 全文（/data/liguang13/topic-loop-r2/md/星/星/txt/星.md）。

**结论：未发现覆盖 G-A 的工作。** 全库有若干篇在"分解轴"上做了通道/项拆分，但轴分别是**目标类型、智能体、时间**，**没有一篇以"失败事件的物理原因"为分解轴**。

## B.1 检索证据（模式原文 / 全库命中文件数 / 判定）

| 模式原文 | 命中文件数 | 判定 |
|---|---|---|
| credit assignment | 5 | 命中 6C843JTS（Sutton 早期 TD 文献）、JSX5XG88（GAE）、QGAREQUM、9FLZ88LZ。**均为"时间延迟型信用分配"**，无失败原因分解。 |
| counterfactual | 5 | 9FLZ88LZ（QMIX 综述 COMA）、FGQSH4AI / I2WH9RRR / KPUZIMU5（COMA 他引标题）。轴＝**智能体**。 |
| reward decompos | **0** | 无命中。 |
| multi-objective 或 mult(objective 或 i-objective | 12 | 多为波束跳变/资源分配领域与他引标题；实质命中见 B.2。 |
| separate (reward 或 penalt) | 1 | 唯一命中非 G-A 语境。 |
| drop (reason 或 cause) 或 drop reason | 1 | 9KZDXPKC L246/L248 —— 是**实验分场景**（GSL 切换 / ISL 失效）分别测吞吐，非学习通道拆分。 |
| overflow | 10 | 42E4NAQU L145（队列容量设 1 Gb/s）、J68GU76W L198（队列无界）、TQF59BD7 L482（buffer limitations）、X2FCSU4S L15（cache overflow）等。**均为建模/实验条件**，无一处把溢出原因拆成不同惩罚项。 |
| reward vector 或 vector reward 或 multi-head 或 multiple heads 或 separate (value )?heads 或 per-objective | 16 | 实质命中仅 UKBSA7WN（见 B.2）；其余为 Transformer "Multi-Head Attention"（35T2JJRJ 等）假匹配。 |
| failure (type 或 cause 或 reason) 或 cause of (the )?(loss 或 drop 或 failure) 或 loss cause | 23 | 最近邻见 B.3（8N9QJHC2）；其余为物理层安全、能量等无关语境。 |
| distinguish(es 或 ing)? between 或 differentiat(e 或 es 或 ing) between | 21 | 8N9QJHC2 L358 为最近邻；其余无关。 |
| penalt(y 或 ies 或 ize) (term 或 for 或 on) | 6 | 39NJWBI7 L304（拉格朗日乘子阈值）、7TASFUDR L200、X5K285MW L106（每跳处理惩罚）等，**均为单一标量惩罚项**。 |

## B.2 最近邻反例 1（轴＝**目标类型**，不覆盖 G-A）：UKBSA7WN / QRLSN

该书用 **MORL + 奖励向量**，为**每个目标**维护**独立 Q 通道**。逐字引文（L141 / L147 / L149）：

> "MORL differs from typical RL, which considers several optimization objectives simultaneously in the learning process, where a reward vector is provided for the agent at each update step"

> "where \(i \in [ 1 , n ]\) and n represents the number of objectives; \(r _ { i }\) is the i th feedback signal of the agent's reward vector obtained from the interaction with the environment."

逐目标的 Bellman 更新 Eq (6)（MD L144）与合成式 Eq (7)（MD L155）——**这是"分通道 Bellman + 加权合成"的现成骨架**：

> \(Q _ { i } ( s , a ) \gets ( 1 - \alpha ) Q _ { i } ( s , a ) + \alpha \biggl [ r _ { i } + \gamma \operatorname* { m a x } _ { a ^ { \prime } \in A } Q _ { i } ( s ^ { \prime } , a ^ { \prime } ) \biggr ]\)

> \(\mathrm { T Q } ( s , a ) = \sum _ { i = 1 } ^ { n } w _ { i } Q _ { i } ( s , a )\)

两目标的奖励分量 Eq (8)(9)（MD L161/L165），**差异仅为几何量不同**（时延 vs 队列长度）：

> \(f _ { r _ { 1 } }\)：达目的地 \(r _ { \mathrm { m a x } }\)，否则 \(r _ { \mathrm { m i n } } + \left ( \frac { e } { 2 } \right ) ^ { - d _ { i j } }\)（d_ij ＝邻星间传输时间）

> \(f _ { r _ { 2 } }\)：达目的地 \(r _ { \mathrm { m a x } }\)，否则 \(r _ { \mathrm { m i n } } + \left ( \frac { e } { 2 } \right ) ^ { - n _ { q } }\)（n_q ＝本节点排队包数）

**判定**：分解轴＝**目标类型**（端到端时延 vs 网络流量开销负载）。**没有**按失败原因拆分——两个通道对**同一次失败**（未达目的地）给的都是同一个 r_min，不区分原因。→ **不覆盖 G-A**。但它是本库"一个事件 → 多学习通道"在**目标轴**上的最近邻，其 Eq (6)+(7) 结构**可直接改轴复用**（把通道索引 i 从"目标"换成"失败物理原因"）。

## B.3 最近邻反例 2（轴＝**故障物理原因**，但停在检测/恢复层，不覆盖 G-A）：8N9QJHC2

该书是**基于 Q-Learning** 的卫星网络故障恢复路由（L3 标题 "Recovery Routing Based on Q-Learning for Satellite Network Faults"；L31 "based on the Q-learning algorithm in reinforcement learning"），**明确区分两类物理故障**，逐字（L358）：

> "It solved the problem that currently it is impossible to distinguish between temporary and permanent failures. This mechanism introduces two factors of a priori probability of link failure, permanent node port failure and temporary link failure, due to transmission medium interference. Two types of failure a posteriori pr[obability]..."

L362 逐字：

> "It solved the problem that there is no corresponding route recovery design for faults with diferent durations. This technology divides the route restoration process into two phases."

**判定**：分解轴＝**故障物理原因（永久端口故障 vs 介质干扰引起的临时链路故障）**——与本问题最接近。但两处拆分分别落在**故障检测的先验/后验概率估计**与**路由恢复流程的阶段划分**上，**未见**把这二者拆成**不同的 Q 通道或不同的奖励惩罚项**。→ **不覆盖 G-A**。价值：证明"按物理原因分类"在本领域**已有先例可援引**，只是尚未进入学习通道。

## B.4 最近邻反例 3（轴＝**智能体** / **时间**，不覆盖 G-A）：9FLZ88LZ、JSX5XG88

- 9FLZ88LZ 逐字（L52 / L54）："COMA (Foerster et al., 2018) uses a centralised critic to train decentralised actors, estimating a **counterfactual advantage function for each agent** in order to address multi-agent credit assignment" / "value decomposition networks (VDN)... decomposes a central state-action value function into a **sum of individual agent terms**"。→ 轴＝**智能体**。
- JSX5XG88 逐字（L17）："A key source of difficulty is the long time delay between actions and their positive or negative effect on rewards; this issue is called the **credit assignment problem**"，并给出 GAE（广义优势估计）。→ 轴＝**时间**（偏差-方差权衡）。

**判定**：二者均为"信用分配"的经典解，但分解轴为智能体 / 时间。→ **不覆盖 G-A**。其中 GAE 尤其值得登记：本批 7 篇**全部是 1-step TD**（附录 A.2 实测 0 命中），而全库已有 GAE 这类**多步信用分配**工具，构成"库内有工具、本批未用"的明确空位。

## B.5 非反例登记（易被误认为覆盖 G-A）

- **IXVSNEE3**（L385 逐字）："Considering packets may be dropped due to **congestion or link unavailability**, path survival probability is introduced to quantify the likelihood of a packet successfully reaching its intended destination." —— 它在**同一句里区分了两种丢包原因**，但通篇是**解析式路径存活概率**（Eq (29) 等）。实测 grep -c -iE "reinforcement learning|q-learning|dqn|reward" ＝ **0**，即**该文不含任何强化学习**。→ **不覆盖 G-A**。
- **9KZDXPKC**：把 GSL 切换 / ISL 失效作为**两个实验场景**分别报告吞吐（L246/L248），是**评测分层**而非学习通道拆分。
- **X5K285MW**（L106）："we applied the processing penalty on each hop" —— 单一标量逐跳惩罚，非按原因分通道。

## B.6 G-A 的净结论

1. **全库 111 篇中，没有任何一篇把同一失败事件按物理原因拆成不同的学习通道或惩罚项。** → **G-A 作为缺口主张成立**，可直接用于选题论证（附精确检索证据，见 B.1）。
2. 最接近的反例是 **8N9QJHC2**（按永久/临时故障分类，停在检测与恢复流程层）与 **UKBSA7WN**（分通道 Bellman + 加权合成，轴为目标类型）。
3. **对选题的正面价值**：UKBSA7WN 的"逐通道 Bellman（Eq (6)）+ 加权合成（Eq (7)）"提供了**现成的分通道工程骨架**；只需把通道索引从"目标"换成"失败物理原因"，即可把 G-A 从缺口变成可实现的机制。这属于"**机制可复用、轴未被占**"，是理想的选题位。
4. **风险提示**：8N9QJHC2 说明"永久 vs 临时故障"这一分类在本领域已被用过，因此 G-A 的新颖性应建立在**"把该分类接进学习通道/奖励"**上，而**不是**"首次区分这两类故障"——后者的新颖性已被占。




