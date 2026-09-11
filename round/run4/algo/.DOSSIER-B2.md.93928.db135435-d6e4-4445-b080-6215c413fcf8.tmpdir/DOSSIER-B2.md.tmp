# DOSSIER-B2 算法拆解（Batch 2：表格 Q-learning 与收敛加速族）

> 模板：`round/run4/algo/EXTRACTION-TEMPLATE.md`（12 项强制格式）
> 材料：VM `/data/liguang13/topic-loop-r2/md/<itemKey>/<itemKey>/txt/<itemKey>.md`（MinerU MD），行号即该文件行号。
> 全部引文逐字英文原文；公式逐字抄 LaTeX 原文，未做自然语言改写。
> 全批统一检索范围（用于"未见"判定）：对 8 篇 MD 全文执行 ripgrep，检索词集合 =
> `credit assignment|counterfactual|difference reward|Shapley|decompos`、
> `centralized training|CTDE|parameter sharing|shared parameters|non-stationar`、
> `EWMA|exponential moving average|moving average|history of|trend|differential|window`、
> `mask|invalid action|infeasible action|action filtering`、
> `n-step|multi-step|eligibility|trace|lookahead`。下文凡写"未见"均指该集合在该篇 0 命中。

---

## Y2H4NPLU Q-learning 分布式 E2E 路由（Soret et al., LEO 星座）

**1. MDP 定义**
- 形式：L62 "The problem is formulated as a POMDP with a 4-tuple `$( \mathcal { S } , \mathcal { A } , P ( s , a ) , \mathcal { R } ( s , a ) )$` where the observation agents have a partial knowledge of the underlying system state, specifically obtained from their own queues and links and from the feedback of the neighbouring satellites."
- 状态 s_t（逐字段）：L79 "We denote the state space of agent i as `$S _ { i }$` `$\{ L _ { i } , N _ { i } \}$` ... Specifically, `$L _ { i }$` is the information of the packet destination extracted from the packet header and the link connectivity `$\mathcal { E } _ { i } ,$` whereas `$N _ { i }$` contains the link quality and buffer congestion to the two intra-plane and two inter-plane neighbours each of them encoded with two bits: `$s _ { t } = 2$` is reserved for the case with a long queue or unavailable link, and `$s _ { t } = 0$` and `$s _ { t } = 1$` reflect uncongested cases (empty/short queues) with high and low link capacity, respectively."
  - 字段：`L_i` = {当前包目的 d_p（来自包头的整数 ID）, 链路连通性 E_i（集合，|E_i|≤4）}；`N_i` = 4 个邻居 × 2 bit 离散档 {0,1,2}。
  - 维度：L_i 为 ID+集合；N_i 为 4 元、每元 3 值 → 状态基数上界 3^4。
  - 归一化：无（离散编码，原文未做归一化）。
  - 时间聚合：无（见第 4 项）。
  - 原文自陈动机 L79："This simple encoding minimizes the state space and alleviates the computation cost, which is an advantage for satellites with limited computation capabilities."
- 动作 a_t：L97 "The action decision `$a _ { t }$` is the next hop j selected from the set `$\mathcal { E } _ { i } \cup \mathcal { E } _ { i _ { G } } ,$` i.e., one of the neighbouring satellites or the link towards a gateway." 大小 ≤4 ISL + 可选 GSL。行动掩码：未见显式掩码；可选集由拓扑发现动态更新，L110 "Update `$\mathcal { E } _ { S }$` and `$\mathcal { E } _ { G }$` using [3]"。
- 奖励 r_t（逐字 LaTeX）：
  - L84 `$$r _ { t } = \left\{ \begin{array} { l l } { r _ { \mathrm { d e l } } } & { j d \in \mathcal { E } _ { G } } \\ { r _ { \mathrm { l o o p } } } & { j \in \mathcal { P } _ { p } } \\ { r _ { \mathrm { q u e u e } } + r _ { \mathrm { d i s t } } } & { \mathrm { o t h e r w i s e } } \end{array} \right.\tag{5}$$`
  - L88 `$$r _ { \mathrm { q u e u e } } = w _ { 1 } \cdot \bigg ( 1 - 1 0 ^ { t _ { q } ( j ) } \bigg )\tag{6}$$`
  - L92 `$$r _ { \mathrm { d i s t } } = w _ { 2 } \cdot \frac { | | i d | | - | | j d | | + | | s d | | } { | | s d | | }\tag{7}$$`
  - 系数含义 L95："where `$w _ { 1 }$`, w2 are adjustment constants, `$t _ { q } ( j )$` is the time spent in the queue of the next hop, i.e., satellite j; `$| | i d | | - | | j d | |$` is the slant range reduction of the decision ... and `$| | s d | |$` is the total slant range between i and d"。**w1/w2 数值未报告**。
  - 归一化：仅 r_dist 经 ||sd|| 归一化；r_queue 为 (1−10^{t_q})，无界（t_q 增大时趋于 −∞）。
  - 折扣 γ：L67 更新式含 γ；**γ 数值未报告**，α 亦未报告。
- 转移/终止：episode L72 "The episode is composed by T steps, indexed by `$t = 0 , 1 , . . . , T$`"；终止 = 包抵达目的 gateway（L111-113 "`$\mathbf { i f } \ | | i d | | \in \mathcal { E } _ { G }$` then / Deliver `$p _ { i }$` to destination d / `$r _ { t } = r _ { \mathrm { d e l } }$`"）。资格迹/多步回报：未见（检索 `n-step|eligibility|trace` 0 命中）。

**2. 学习算法与更新式**
- 算法名：L99 "Q-routing algorithm. The pseudo-code of the Q-routing algorithm is in Algorithm 1"。
- 教科书式更新（原文写作通用式）：L67 `$$Q ( s _ { t } , a _ { t } ) = ( 1 - \alpha ) Q ( s _ { t } , a _ { t } ) + \alpha \left( r _ { t } + \gamma \mathrm { m a x } Q ( s _ { t + 1 } , a ) \right) ,\tag{4}$$`
- **该文实际部署的更新式（关键改动）**：L130 `$$Q _ { i } ^ { * } ( s _ { t } , a _ { t } ) = ( 1 - \alpha ) Q _ { i } ( s _ { t } , a _ { t } ) + \alpha \left( r _ { t } + \gamma \mathrm { m a x } Q _ { j } ( s _ { t + 1 } , a ) \right)\tag{8}$$`
  - 即 bootstrap 项取**下一跳节点 j 的 Q 表**而非自表。理由 L103："In the conventional formulation of Qlearning, each agent updates its own q-table based on the new state and reward. However, this is not effective in our problem, because the actions taken by satellite i are observable in the state change of the neighbouring satellites, more specifically in the increased queue length of the next hop j."
- double/target net：未见（表格法，无网络）。
- 网络结构：无神经网络；每星维护独立 Q 表（L75 "Each satellite maintains its own Q-table"）。图算子：未见。

**3. 信用分配：这篇怎么把奖励归到动作上？**
- 逐跳即时奖励：L81 "For this action, the immediate reward considers the two main contributors to the end-2-end delay: (1) the propagation time, for which the topology and the slant range of each decision should be considered; (2) the queueing time, which becomes dominant when the system gets congested"。
- 路径级终局奖励：仅到达目的的 r_del（L95 "If the data block has been sent to a satellite whose linked gateway matches the destination of the data block, the agent will receive the extra reward `$r _ { \mathrm { d e l } }$`"）。
- 环路惩罚：L95 "To avoid loops, the penalty `$r _ { \mathrm { l o o p } }$` is applied if the agent sends the data block to a satellite where it has already been."
- 分解到节点/链路：部分——奖励由**决策本身**（下一跳 j）的排队时延与到目的地的距离缩减构成，属于 hop-level credit；**链路**层面无独立分解。
- 是否区分损失原因：未见。全文检索 `credit assignment|counterfactual|decompos` 0 命中；奖励仅 4 档（del/loop/queue+dist），无丢包或链路失效的独立惩罚项。

**4. 状态里有没有时间信息？**
- **没有**。L79 逐字段均为瞬时量：包头目的、当前链路连通性 E_i、邻居当前 link quality 与 buffer congestion（2 bit，三档）。
- 检索佐证：`EWMA|moving average|history of|trend|differential|window` 全文命中 2 处（L141、L143），均为**评测稳定性判据**而非状态特征——L141 "we perform a linear regression with the model `$Y _ { i } = \beta _ { 0 } + \beta _ { 1 } X _ { i } + \epsilon$` using the last 200 packets received at the destination to avoid considering the training period"。
- 唯一的时间结构在算法层面是 ε 退火（L101），与状态无关。

**5. 动作有没有时间结构？**
- 每包独立决策：L75 "(1) Upon arrival of packet `$p ( d )$` at sat i, the best action `$a _ { t }$` is selected, i.e., forward the packet to sat j."
- 动作驻留/流级缓存/摊销：未见（检索 `flow|reside|amortiz|cache` 无相关命中；决策粒度 = 单包）。
- 触发式更新：是——一旦收到邻居反馈即更新 L75 "(2) Sat j calculates the new Q-value and sends it to sat i, who (3) updates the Q-table accordingly."
- 切换代价：未见（奖励中无切换/重路由惩罚项）。

**6. 多智能体设定**
- 独立学：L60 "we aim at a fully-distributed solution where each satellite is an independent learning agent that learns its routing policy"。
- 共享参数：不适用（per-node 表格）。检索 `parameter sharing|shared parameters` 0 命中。
- 非平稳处理：未见。检索 `CTDE|centralized training|non-stationar` 0 命中。
- 通信：极简，L133 "Minimal feedback information: As illustrated in the steps of Fig. 2, the algorithm minimizes the interaction with nearby satellites. Specifically, the Q-value is the only feedback after the successful reception of a packet, over a link that has been previously established."
- 动作同步：无（异步逐包）。

**7. 训练协议**
- 训练分布 vs 评估分布：**同一套**——同一仿真的连续运行；L141 明确只把"最后 200 个包"排除训练期做统计，未划分独立评估环境。
- 采样 episode：按包到达驱动，L72 "the time scale of the learning episodes is dictated by the arrival of the packets"。
- 负载/拓扑变化：led by 活跃 gateway 数 `2 ≤ |G| ≤ 18`（L137）；拓扑由轨道运动自然演化，L72 "The satellite passes for an observer at the Earth surface or between satellites in different orbital planes are at the scale of few minutes"。
- 训练步数/时长：未给出步数；以收敛速度描述 L72 "the agents learn the new paths in less than 0.5 s"。

**8. 该文的算法贡献（与 1–7 的具体改动对应）**
把 Q-routing 的 bootstrap 从"自身下一状态"改为**下一跳节点 j 的 Q 表**（eq 8，对应第 2 项），配合 4 邻居×2 bit 的极小状态编码（eq 状态定义，对应第 1/4 项）与四档奖励（queue 指数项 + 距离归一化项 + loop 惩罚 + delivery 奖励，对应第 1/3 项），使纯分布式逐跳学习在 gateway 数扫描下比 data-rate BM 与 latency-genie BM 支撑更高负载（L143）。

**9. 该文自述的局限（逐字）**
- L164 "Future work will look at the extension of the state space to DRL and the evaluation in scenarios with heterogeneous QoS requirements and policies."
- L151 "we use a simple encoding of the status of the link to limit the size of the state space. In the future, we will explore the use of Deep RL (RL) which allows enlarging the state space, although at the expenses of a higher computation complexity."
- L79 "In the future, we will extend the space space and apply other advanced learning techniques to characterize the tradeoff between complexity of the learning algorithm and performance gain."

**10. 该文没有考察的算法选择（基于 1–7 实际内容）**
- **奖励始终是标量 r_t，从未分解**：eq (5)–(7) 单一标量，全文无奖励向量/多目标（检索 `credit assignment|counterfactual|decompos` 0 命中）。对比同批 UKBSA7WN 用 reward vector `$f _ { r } = [ f _ { r _ { 1 } } , f _ { r _ { 2 } } ]$`。
- **状态逐字段均为瞬时量，无任何时间聚合**：见第 4 项；唯一的"时间"出现在评测判据（L141）而非特征。
- **从未比较过不同训练分布**：第 7 项显示训练与评估同源，且未做跨负载泛化实验（训练于 ℓ=0.85 后只在同 ℓ 下扫描 |G|）。
- 从未使用动作掩码：动作集仅由连通性隐式裁剪，无显式 safe-action 约束（检索 `mask|invalid action|infeasible` 0 命中）。
- 从未使用多步回报/资格迹：检索 `n-step|multi-step|eligibility|trace` 0 命中。
- 从未做 α / γ 的敏感性或调参：eq (4)(8) 含 α、γ 但全文未报告取值（对比同批 ZIUBKVPZ Table I 明列 α=0.001/0.007、γ=0.99/0.9）。
- 从未按损失原因分解信用：奖励仅 del/loop/queue+dist 四档，无丢包项。

**11. 可复用的具体机制（含公式）**
1. **邻居 Q 表 bootstrap（分布式 Bellman）**：L130 `$Q _ { i } ^ { * } ( s _ { t } , a _ { t } ) = ( 1 - \alpha ) Q _ { i } ( s _ { t } , a _ { t } ) + \alpha \left( r _ { t } + \gamma \mathrm { m a x } Q _ { j } ( s _ { t + 1 } , a ) \right)$` —— 用接收方 j 的估值代替自身估值，天然把"下一跳拥塞"写进目标值。
2. **指数型队列惩罚**：L88 `$r _ { \mathrm { q u e u e } } = w _ { 1 } \cdot \bigg ( 1 - 1 0 ^ { t _ { q } ( j ) } \bigg )$` —— 原文 L95 解释 "the first exponential term makes the penalty grow faster as the queue time increases"；对排队时延呈凸惩罚。
3. **归一化距离进度项**：L92 `$r _ { \mathrm { d i s t } } = w _ { 2 } \cdot \frac { | | i d | | - | | j d | | + | | s d | | } { | | s d | | }$` —— 以源-目全程斜距为尺度做无量纲化，可直接搬到我们的逐跳 shaping。
4. **2-bit 邻居状态编码**：link quality × buffer congestion 两维各三档（0/1/2），把邻居状态空间压到 3^4。

**12. 实验合同里与"负载"相关的设置（仅作实验条件登记，不作贡献）**
- 星座：L137 "We consider a Kepler constellation with `$M \ = \ 7$` orbital planes at heights `$h _ { m } \ = \ 6 0 0$` km and `$N _ { m } \ = \ 2 0$` satellites per orbital plane."
- 地面：L137 "There are up to 18 transmitting gateways at ground positions around the globe ... with `$2 \leq | \mathbb { G } | \leq 1 8$` and traffic load `$\ell = 0 . 8 5$`."
- 负载定义：L38 "`$\ell = \sum _ { g \in \mathbb { G } } \lambda _ { \mathrm { U L } } ^ { ( g ) } / \lambda ^ { * }$`"（上行生成率 / 网络最大可支撑负载）。
- 流量生成 L38 "each active gateway transmits an equal amount of data among the rest of the gateways in `$\mathbb { G }$` through the LSatC" —— 均匀源目对，非热点偏斜。
- 物理参数 L137-139：发射功率 10 W（星）/20 W（地面站）；载频 20 GHz 下行、30 GHz 上行、26 GHz ISL；天线 33 cm（地面）/26 cm（星）；`$W = 5 0 0 \mathrm { M H z }$`；包长 `$B = 6 4 . 8 \mathrm { k b i t s }$`。
- 稳定性判据 L141（线性回归 + 单边 t 检验，H0: β1≤0，取最后 200 包，显著性 0.05）——是**评测协议**，非算法部件。

---

## UKBSA7WN QRLSN：多目标 Q-routing（mega LSN）

**1. MDP 定义**
- 形式：L53 "RL could be described as a Markov Decision Process (MDP) consisting of a tuple `$( S , A , P _ { \mathrm { t } } , R )$`"。
- 状态 s_t：**原文未显式定义状态向量的分量**。全文只有 L112 的伪码行 "12. Update state `$s _ { \scriptscriptstyle { t - 1 } }  s _ { \scriptscriptstyle { t } }$`" 与 L127 "the current node will update its Q-table according to Eq. (2) under the new state `$s _ { t + 1 }$`"。检索 `state space|state set|State:` 在该篇无状态分量定义段 → **未见状态逐字段定义**。
  - 可间接推断的隐含状态即 Q 表索引：L61 "`$Q _ { i } ( j , d )$` represents the Q-value of transmitting the data packet in the node `$N _ { i }$` to destination node d by selecting the neighbor node j as the next hop." 即状态 ≈ (当前节点 i, 目的 d)。
- 动作 a_t：L121 "ε-greedy is taken as the next-hop policy to explore better choices"；L124 `$$a _ { t } = \left\{ \begin{array} { c c l } { { \mathrm { r a n d o m ~ a c t i o n ~ i n } } } & { { A _ { i } } } & { { \mathrm { w . p . } \in } } \\ { { \mathrm { a r g m a x } _ { a \in A _ { i } } \mathcal Q _ { t + 1 } } } & { { \mathrm { w . p . } 1 - \epsilon } } \end{array} \right.\tag{ð4Þ}$$`。动作集 A_i = 邻居集（mesh 下 4）。动作掩码：未见。
- 奖励 r_t：**分两阶段，且维护阶段是向量**。
  - 发现阶段（标量）L132 `$$f _ { \mathrm { r d } } = \left\{ \begin{array} { l l } { r _ { \mathrm { m a x } } } & { N _ { t + 1 } \mathrm { i s ~ d e s t i n a t i o n } } \\ { r _ { \mathrm { m i n } } } & { \mathrm { O t h e r w i s e } } \end{array} \right.\tag{ð5Þ}$$`，L135 "In this paper, `$r _ { \mathrm { m i n } }$` is set to 1 and `$r _ { \mathrm { m a x } }$` is set to 100"。
  - 维护阶段（**向量奖励，两个目标**）L161 `$$f _ { r _ { 1 } } = \left\{ \begin{array} { c c } { { r _ { \mathrm { m a x } } } } & { { N _ { t + 1 } \mathrm { i s \ d e s t i n a t i o n } } } \\ { { r _ { \mathrm { m i n } } + \left( \frac { e } { 2 } \right) ^ { - d _ { i j } } } } & { { \mathrm { O t h e r w i s e } } } \end{array} \right.\tag{ð8Þ}$$`
  - L165 `$$f _ { r _ { 2 } } = \left\{ \begin{array} { c c } { { r _ { \mathrm { m a x } } } } & { { N _ { t + 1 } \mathrm { i s \ d e s t i n a t i o n } } } \\ { { r _ { \mathrm { m i n } } + \left( \frac { e } { 2 } \right) ^ { - n _ { q } } } } & { { \mathrm { O t h e r w i s e } } } \end{array} \right.\tag{ð9Þ}$$`
  - 含义 L168 "where `$f _ { r _ { 1 } }$` and `$f _ { r _ { 2 } }$` denote the reward function to optimize the end-to-end delay and network traffic overhead load respectively; `$d _ { i j }$` is the transmission time between adjacent satellite nodes; `$n _ { q }$` is the number of data packet queued in the current node."
  - 归一化：无（底数 e/2 < 1 的负指数，随 d_ij / n_q 增大而趋 0）。
  - 折扣 γ：Table 2 (L188) "Discount factor | 0.95"；α="Learning rate | 0.8"。
- 转移/终止：终止 = 包到达目的（r_max 分支）。episode：Table 2 "Maximum training episodes | 1000"、"Maximum steps per episode | 1500"。资格迹/多步：未见（检索 `n-step|eligibility|trace` 0 命中）。

**2. 学习算法与更新式**
- 基础 Q-routing（教科书式）L56 `$$Q ( s , a ) \gets ( 1 - \alpha ) Q ( s , a ) + \alpha [ r + \gamma \operatorname* { m a x } _ { a ^ { \prime } \in A } Q ( s ^ { \prime } , a ^ { \prime } ) ]\tag{ð1Þ}$$`
- Q-routing 展开式 L66 `$$Q _ { i } ( j , d ) \gets ( 1 - \alpha ) Q _ { i } ( j , d ) + \alpha [ r + \gamma Q _ { j } ( d ) ]\tag{ð2Þ}$$`，其中 L72 `$$Q _ { j } ( d ) = \operatorname* { m a x } _ { k \in \mathrm { N g } ( j ) } Q _ { j } ( k , d )\tag{ð 3Þ}$$` —— 同样是**邻居 Q 表 bootstrap**。
- MORL 更新式（维护阶段）L144 `$$Q _ { i } ( s , a ) \gets ( 1 - \alpha ) Q _ { i } ( s , a ) + \alpha \biggl [ r _ { i } + \gamma \operatorname* { m a x } _ { a ^ { \prime } \in A } Q _ { i } ( s ^ { \prime } , a ^ { \prime } ) \biggr ]\tag{ð6Þ}$$`，L147 "where `$i \in [ 1 , n ]$` and n represents the number of objectives; `$r _ { i }$` is the i th feedback signal of the agent's reward vector"。
- 合成策略（加权和）L155 `$$\mathrm { T Q } ( s , a ) = \sum _ { i = 1 } ^ { n } w _ { i } Q _ { i } ( s , a )\tag{ð7Þ}$$`，L158 "where w is the weight vector value and the sum of w equals 1." **权重数值未报告**。
- double/target net：未见。网络结构：无神经网络，Q 表（Table 1，L91-92）。

**3. 信用分配**
- 逐跳即时奖励（发现阶段每步都给信号）：L135 "In each data packet propagation step, the current node could obtain an immediate reward signal `$r _ { \mathrm { m i n } }$`, whether packets reach the terminal or not. This minimum reward is employed to prevent the updating delay of Q-values due to the sparse reward feedback."
- 路径级终局：r_max=100（到达目的）。
- 分解到节点/链路：部分——r_{2} 用**当前节点排队数 n_q**、r_{1} 用**相邻星间传输时间 d_ij**，属 hop-level。
- 是否区分损失原因：未见。检索 `credit assignment|counterfactual|decompos` 0 命中；无丢包/失效独立项（发现阶段丢包只体现为不给 r_max）。

**4. 状态里有没有时间信息？**
- **没有**。Q 表索引 (i, j, d) 无时间维度；奖励中的 d_ij 与 n_q 均为瞬时量。检索 `EWMA|moving average|history of|trend|differential|window` 命中均为结果叙述（L215 "convergent trend"、L225 "trend of delay time"、L235 "downward trend"），非状态特征。
- 唯一时间量是**邻居发现周期**（Table 3, L207 "Neighbor discovery period(min) | 1"、"Time discretization(min) | 1"），属通信协议节拍，不进状态。

**5. 动作有没有时间结构？**
- 事件触发、逐包决策：L170 "the routing decision process is event-triggered, once a data packet arrives at a satellite node, the next hop is determined by the maximum Q-value."
- 动作驻留/流级缓存：未见。切换代价：未见。
- 有 ε（固定 0.1，Table 2 L188 ""€-greedy factor" | 0.1"），**无退火**（与同批 53HEEK33/UKEKU5ZG/PIXWFHAC 的退火形成对比）。

**6. 多智能体设定**
- 独立学：L75 "Note that in the Q-routing algorithm, Q-table in each node is autonomously updated in a distributed manner without global information."
- 共享参数：不适用（per-node Q 表）。非平稳处理：未见（`CTDE|centralized training|non-stationar` 0 命中）。
- 通信：周期 hello，L83 "The 'Hello' packets contain neighbor status, nodes Q-tables and link information. Unlike the entire flooding of 'Hello' packets in ad-hoc on-demand routing 12 'Hello' packets are merely propagated to neighbors in QRLSN without being resource-intensive."
- 动作同步：无。

**7. 训练协议**
- **训练分布与评估分布不同**（本批少数）：发现阶段用 `$x _ { k } \sim \mathrm { P o i } ( \lambda )$`（L89），Table 2 取 "User request | `$x _ { k } \sim \operatorname { P o i } ( 5 )$`"；维护阶段 Table 3 改为 "User request | xk ∼ Poi(20)"。即**训练用 λ=5，上线用 λ=20**，且评估扫描 k∈{5,20,35}（L237-239）。
- 采样 episode：L102-104 "for episode=1, 2,…, M do / Clear all delivering data packets / for step=1, 2,···, N do / Randomly generate x, data packets"。
- 拓扑变化：L176 "while LSNs topology changes dynamically do"，Table 3 时间窗 2022-01-29 04:00 至 2022-01-30 04:00（1 天）。
- 训练步数：Table 2 "Maximum training episodes | 1000"、"Maximum steps per episode | 1500"。

**8. 算法贡献（与 1–7 对应）**
把 Q-routing 从单标量奖励扩展为**两目标向量奖励 + 加权和 Q 表**（eq 8/9 + eq 7，对应第 1/3 项），并把训练拆成"发现阶段稀疏到达奖励（r_min=1/r_max=100）→ 维护阶段多目标稠密奖励"的两段协议（对应第 1/7 项），在 288/512/1152 星三档规模下相对 VT-SPR 取得优势（L253）。

**9. 自述局限（逐字）**
- L255 "In our future works, we will improve the QRLSN's robustness in the presence of node failures and inter-satellite link instability. Additionally, in-depth research on congestion awareness will be the focus for further investigation."

**10. 没有考察的算法选择**
- **状态从未被显式定义**：全文无状态分量定义段（见第 1 项），因此也无从考察"状态里放什么"这一选择——这是与本批其余 7 篇最大的结构性差异。
- **加权和权重 w 数值未报告**，且**从未比较多目标聚合方式**（只做线性加权和，eq 7；检索 `Chebyshev|Pareto|scalariz` 0 命中）。
- 从未使用动作掩码（检索 0 命中）。
- 从未使用多步回报/资格迹（检索 0 命中）。
- 状态无时间聚合（第 4 项）。
- 从未做 α/γ 敏感性分析（Table 2 固定 α=0.8、γ=0.95）。
- 唯一做了**训练/上线分布差异**的一篇（Poi(5) → Poi(20)），但**未把该差异本身作为变量研究**（无跨 λ 迁移实验设计）。

**11. 可复用机制（含公式）**
1. **向量奖励 + 加权和 Q 表**：L144 eq(6) 对每个目标维护独立 Q_i，L155 `$\mathrm { T Q } ( s , a ) = \sum _ { i = 1 } ^ { n } w _ { i } Q _ { i } ( s , a )$` 合成。这是本批**唯一**把奖励显式分解为多目标的实现，可直接作为我们"时延 vs 负载"双目标的基线写法。
2. **底数为 e/2 的负指数奖励**：L161 `$r _ { \mathrm { m i n } } + \left( \frac { e } { 2 } \right) ^ { - d _ { i j } }$`、L165 `$r _ { \mathrm { m i n } } + \left( \frac { e } { 2 } \right) ^ { - n _ { q } }$` —— 以 0<e/2<1 为底，d_ij / n_q 增大时奖励平缓衰减并**始终为正**，天然不需要归一化。
3. **稀疏→稠密的两段奖励**：先用 r_min=1 常值稠密信号跑通可达性（L135 明确动机 "to prevent the updating delay of Q-values due to the sparse reward feedback"），再切多目标稠密奖励。

**12. 实验条件登记（负载相关）**
- 星座 L198 "we consider mega LEO satellite constellations placed at 53 orbital inclination and 550 km altitude"；规模 L202 "constellations with 288, 512, and 1152 total number of satellites are selected for comparison"，Walker Delta `T=P=F`。
- 流量 L89 "`$x _ { k } \sim \mathrm { P o i } ( \lambda )$`"，发现 λ=5 / 维护 λ=20 / 评估扫描 k∈{5,20,35}。
- 丢包定义 L204 "data packets are considered to be lost if they are not received within 2000 ms."
- 邻居发现周期 1 min、时间离散 1 min（Table 3）。
- 仿真工具 L198 "constructed by using the System Tool Kit (STK) and the Network X tool package"。对比算法 VT-SPR，时间片 20 min（L233）。

---

## 53HEEK33 FRL–SR：快收敛 Q-routing（Iridium）

**1. MDP 定义**
- 形式：L109 "The entire packet forwarding process can be viewed as a finite-state Markov decision process (MDP) whose final state occurs when the packets have arrived at the destination node. We use (S, A, P, R) to represent a state of the MDP"。
- 状态 s_t（逐字段）：L113 "Each state `$s _ { t } \in S = \{ N _ { c } , N _ { d } , q _ { 1 } ^ { t } , q _ { 2 } ^ { t } , \dots , q _ { P } ^ { t } \}$` indicates the present situation in the satellite network environment, where `$N _ { c } , N _ { d }$` represent current node and destination node for packet, respectively. The parameter `$q _ { p } ^ { t }$` represents the current queue length of the p-th node for `$p = 1$` to `$p = P$`."
  - 字段：N_c（当前节点 ID）、N_d（目的节点 ID）、q_p^t（**全网 P 个节点的当前队列长度**）。
  - 维度：P = 节点数（实验中 49）；队列长度整数 [0,150]（Table 3 "Max queue length | 150"）。
  - 归一化：无。
  - 时间聚合：**无**（q_p^t 为 t 时刻瞬时队列，见第 4 项）。
  - 注意：状态含**全网**队列 → 与"分布式局部观测"的常见设定不同，靠 hello 包把邻居 Q 表+链路+资源传过来（L140）。
- 动作 a_t：L115 "The action `$a _ { t } \in A = \{ p _ { 1 } , p _ { 2 } , . . . , p _ { P } \}$` represents the agent choosing a node from its neighborhood nodes for each upcoming packet ... In satellite networks, each satellite has up to four neighbor nodes, so the length of A is up to four"。
- 奖励 r_t（逐字 LaTeX）L128 `$$r e w a r d _ { j } = \left\{ \begin{array} { l l } { { 2 0 N } } & { { N _ { j } { \mathrm { i s ~ t h e ~ d e s t i n a t i o n } } } } \\ { { q _ { m a x } - ( q _ { r } + q _ { t } ) - w _ { 1 } * g _ { j } - w _ { 2 } * D _ { j } } } & { { \mathrm { O t h e r w i s e } } } \end{array} \right.\tag{3}$$`
  - 三项 L119-123：Propagation delay（"we consider both reconnection time and propagation time as propagation time delay"）、Queue length（"Each satellite node maintains the receiving queue `$q _ { r }$` and the transmitting queue `$q _ { t }$`"）、Load growth（L123 "we record the receiving queue length in the previous stage as the load growth of the satellite, which is recorded as `$g _ { i }$` ... `$g _ { i }$` could be seen as the congestion level of nodes `$N _ { i }$`"）。
  - 系数 L125 "where `$q _ { m a x }$` represents the maximum queue length, and `$w _ { 1 }$` and `$w _ { 2 }$` represent the growth and delay coefficients"。**w1/w2 数值未在正文报告**；实验用 reward2 的等价式 L256 给出 `$r e w a r d 2 = ... 3 0 0 - ( q _ { r } + q _ { t } ) - 5 * g _ { j } - 0 . 1 * D _ { i j }$`，即 q_max=300、w1=5、w2=0.1。
  - 归一化：无（靠 q_max 做尺度）。
  - 折扣 γ：Table 3 (L245) "discount factor | 0.9"；学习率 "Learning rate for offline training | 0.8"、"Learning rate for online training | 0.2"。
  - **终止奖励不一致**：正文 L125 "When the next hop is the destination node, we set the reward to 20N"，伪码 L173 写 "reward = 20"（Algorithm 1 第 15 行）。两处不一致，登记备查。
- 转移/终止：终止 = 到达目的（L146 "if a packet is forwarded to its destination node, a new packet is generated"）。资格迹/多步：未见（检索 0 命中）。

**2. 学习算法与更新式**
- 算法名：L81 "Q routing is the application of the Q learning algorithm to the routing problem. In the Q routing algorithm, each communication node is treated as an agent"。
- 教科书式 L76 `$$Q ( s , a ) = ( 1 - \alpha ) Q ( s , a ) + \alpha [ r + \gamma \operatorname* { m a x } _ { d \in A } Q ( s ^ { ' } , a ^ { ' } ) ]\tag{1}$$`
- Q-routing 式（**邻居下标 j**）L84 `$$Q _ { i } ( s , a ) = ( 1 - \alpha ) Q _ { i } ( s , a ) + \alpha [ r + \gamma \operatorname* { m a x } _ { d \in A } Q _ { j } ( s ^ { ' } , a ^ { ' } ) ]\tag{2}$$`，L87 "where α is the learning rate which determines the updating rate, γ is discount factor, and i, j represent the index of different nodes. This equation is the essence of agent learning."
- Q 表结构 L89 Table 1："State | Neighbor"，行 = `$( i , D _ { 1 } )$`，列 = `$N _ { 1 } , N _ { 2 } , N _ { 3 } , \ldots$`。
- double/target net：未见。网络结构：无神经网络（L109 明确选表格法："Each satellite node only forwards packets to its neighbor nodes, which means that the action space is up to four. Therefore, we chose reinforcement learning rather than deep reinforcement learning to achieve this."）。

**3. 信用分配**
- 逐跳即时奖励：eq(3) 的 otherwise 分支。
- 路径级终局：20N（到达目的）。
- 分解到节点/链路：**分解到"下一跳节点 j"**，且在奖励中同时含**下一跳的收/发队列**与**负载增长率 g_j（上一阶段队列）**——是本批对拥塞最细的逐跳刻画之一。
- 是否区分损失原因：未见。检索 `credit assignment|counterfactual|decompos` 0 命中；丢包只在结果解释中出现（L272 "The algorithm in this paper does not have a data retransmission function"）。

**4. 状态里有没有时间信息？**
- **状态里没有，但奖励里有一步滞后**。L113 状态字段 `$q _ { p } ^ { t }$` 为 t 时刻瞬时队列；而 L123 的 `$g _ { j }$` 是"the receiving queue length in the previous stage"，进入**奖励**（eq 3 的 w1·g_j 项）而非状态。
- 检索佐证：`EWMA|moving average|history of|trend|differential|window` 在该篇 **0 命中**。
- 结论：本篇是本批唯一含"相邻时刻差分"思想的（g_j 即一阶差分代理），但只用在奖励 shaping，未进状态。

**5. 动作有没有时间结构？**
- 逐包决策：L107 "When the data packet arrives at the satellite node, it observes the current state and forwards the packet based on the present situation."
- **有触发式周期更新**（该文核心机制）：L203 "Neighboring nodes do not only send status information after receiving a packet, but also broadcast its message by period t. The traditional learning process only updates a certain item of the two-dimensional Q-table at a time, while the empty packet convergence method updates the entire content of a node's action space at a time. The smaller the t, the more often agents perceive the network. Therefore, we designed t to be inversely proportional to the node traffic density; the higher the traffic density, the smaller the t".
- 伪码 Algorithm 2 (L214) "2 if time mod t == 0 then / 3 Neighborhood discovery; / 4 Update the Q-table according to Equation (2);"。
- 动作驻留/流级缓存：未见。切换代价：未见。

**6. 多智能体设定**
- 独立学：L113 "In multi-agent reinforcement learning, each agent observes a different state, and they make independent routing decisions based on the current state"。
- 共享参数：不适用（per-node Q 表）。非平稳处理：**未做显式机制**，但**明确把它识别为问题并作为动机**：L201 "If we suppose that the link state of a satellite changes, it is obtained first by the two satellite nodes of this link, followed by the neighboring nodes of the two satellite nodes. Therefore, the state of links is serial propagation, which causes certain difficulties for the convergence of the reinforcement learning algorithm."
- 通信：L140 "the 'hello' packet contains a Q-table, link information, and available resources that nodes can use to calculate reward values and update their own Q-table."
- 动作同步：无。

**7. 训练协议**
- **两阶段，训练分布 ≠ 上线分布**：L144 "The network `$G _ { t 0 }$` at `$t _ { 0 }$` time is input as the initial state, and the output is that each satellite node receives a Q-table."；L131 "During the offline training phase, we perform the initial training of the agents in a ground-based network environment."；L189 在线阶段 "We simplify the satellite network routing problem to finding the smallest delay path."
- 探索差异：离线用 ε-greedy 且退火（L148），在线**不用**探索 L187 "Unlike offline training, agents in online training do not make decisions according to the ε-greedy strategy, since agents avoided the local optimal solution in the previous step."
- 学习率差异：0.8（离线）→ 0.2（在线），L242 "we adjusted the learning rate of this stage to 0.2, and the corresponding learning rate of the offline training stage was 0.8."
- 采样：L146 "the initial and destination nodes of packets are randomly selected from the set of satellite nodes."
- 训练步数：L242 "In the offline training phase, the algorithm ran for 30 episodes—the step for each episode was 200"（=6000 步）。

**8. 算法贡献（与 1–7 对应）**
用"空包收敛（empty packet convergence）"把邻居信息的发送从"仅随数据包携带"改为**周期 t 广播**（对应第 5/6 项），使一次广播更新整行 Q 表（原文 "updates the entire content of a node's action space at a time"），并把 t 设计为**与节点流量密度成反比**（对应第 5 项）；网络侧配套离线预训练 + 在线只做微调（不探索）的两阶段协议（对应第 7 项）。

**9. 自述局限（逐字）**
- L296 "In future work, we will continue to work on multi-agent reinforcement learning algorithms to better solve the problem of satellite network routing."
- L272 "The algorithm in this paper does not have a data retransmission function, which means the delay of lost packets will keep increasing, resulting in a rising average delay."

**10. 没有考察的算法选择**
- **奖励是标量、从未分解**：eq(3) 单一标量（对比同批 UKBSA7WN 的向量奖励）。
- **状态逐字段均为瞬时量、无任何时间聚合**（第 4 项）：q_p^t 是 t 时刻快照；唯一的时间差分思想 g_j 只进奖励。
- **从未比较过不同训练分布**：虽然事实上做了"地面离线 → 星上在线"的两阶段，但**两阶段的分布如何构造、差异多大**未被参数化或消融（离线/在线的差别只体现为学习率 0.8→0.2 与是否探索）。
- 从未使用动作掩码（检索 0 命中）。
- 从未使用多步回报/资格迹（检索 0 命中）。
- **做了奖励函数的消融**（本批唯一）：L247 "The performance of different rewards is shown in Figure 4."，比较 reward1（仅距离，L250 `$r e w a r d 1 = ... - 0 . 1 * D _ { i j }$`）与 reward2（含队列+负载增长，L256 `$3 0 0 - ( q _ { r } + q _ { t } ) - 5 * g _ { j } - 0 . 1 * D _ { i j }$`），L259 "we chose the second reward function for subsequent simulations"。
- 状态含**全网 P 个队列**但不做特征压缩/注意力，也从未考察状态规模的取舍（P=49）。

**11. 可复用机制（含公式）**
1. **空包收敛 / 周期广播整行更新**：L203 与 Algorithm 2 L214 "2 if time mod t == 0 then"，且 **t 与节点流量密度成反比** —— 这是本批最直接可搬的"感知时效性"机制（与同批 5N5LQPPP 的 two-hop、UKEKU5ZG 的周期广播同族，但只有本篇给了"t 反比于流量密度"的自适应规律）。
2. **负载增长项 g_j（一阶拥塞差分）**：L123 "we record the receiving queue length in the previous stage as the load growth of the satellite, which is recorded as `$g _ { i }$` ... This avoids the situation that everyone sends data to 'high-quality' nodes at the same time." —— 奖励中加入队列的**时间差分**，抑制羊群效应。
3. **在线不探索的微调协议**：L187 + 学习率 0.8→0.2（L242）—— 预训练后关闭探索、只用小学习率微调，可作为我们"离线预训练 → 上线"的默认纪律。

**12. 实验条件登记（负载相关）**
- 星座 L242 "The network had a total of 7 satellite orbits, each containing 7 satellites, for a total of 49 satellites"；Table 3 L245 "Number of satellites | 49"。
- **时延模型** L242 "we set the propagation delay to vary according to a sinusoidal curve"；Table 3 "Delay type | sinusoidal"。这是本篇的负载/动态注入方式（非队列驱动的真实拥塞演化）。
- 负载：Table 3 "Offline training network load | 3000"、"Initial network load for online training | 3000"；实验中另测 5000（L264 "the initial number of packages in Figure 6 is 5000"）。
- 队列/转发上限：Table 3 "Max queue length | 150"、"Max transmit packages at one time | 10"。
- 重复次数 L238 "we repeated all the experiments three times and took the average"；Table 3 "Trials | 3"。
- 对比算法：Dijkstra（L240）。

---

## 5N5LQPPP SDDRL-SR：Dijkstra 蒸馏 + 两跳收敛（DDQN）

**1. MDP 定义**
- 形式：L129 "We store `$\left( { { s _ { t } } , { a _ { t } } , { r _ { t } } , { s _ { t + 1 } } } \right)$` in replay memory for the learning of the agent `$v _ { x }$`"（标准 (s,a,r,s') 四元组）。
- 状态 s_t（逐字段）：L98 "Each agent observes the network state independently. The state observed by satellite node `$v _ { 0 }$` is `$s _ { t } =$` `$\{ l _ { t } ^ { v _ { 0 } } , \bar { l } _ { t } ^ { v _ { d } } , S _ { t } ^ { v _ { 0 } } , N ^ { v _ { 0 } } \} . \ : l _ { t } ^ { v _ { 0 } } , l _ { t } ^ { v _ { d } }$` represent the location of current node and destination node respectively. `$S _ { t } ^ { v _ { 0 } }$` is the available storage of satellite `$v _ { 0 }$` at time t, `$N ^ { v _ { 0 } }$` represents the information of neighbours."
  - 字段：l^{v0}（当前节点位置）、l^{vd}（目的节点位置）、S^{v0}（**可用存储**，Table I "Storage space for each satellite (S_max) | 15 GB"）、N^{v0}（邻居信息）。
  - 维度：原文未给特征维度；"Number of hidden layers of DDQN | 3"（Table I）。
  - 归一化：原文未说明。
  - 时间聚合：无。
- 动作 a_t：L103 "The action space of agent `$v _ { 0 }$` is `$a _ { t } = \{ \alpha _ { t , i } ^ { v _ { 0 } , v _ { x } } , v _ { x } \ \in \ n e i g h b o r ( v _ { 0 } ) \}$` ... In LSNs, each satellite has up to four neighboring nodes, resulting in a maximum action space of 4." 掩码：未见（候选由 neighbor 集合隐式裁剪）。
- 奖励 r_t（逐字 LaTeX）L108 `$$R ( s _ { t } , a _ { t } ) = \left\{ \begin{array} { l l } { D _ { a v g } ^ { v _ { s } , v _ { d } } | \mathcal { V } | , } & { a _ { t } = v _ { d } , } \\ { - D _ { a v g } ^ { v _ { s } , v _ { d } } | \mathcal { V } | , } & { \mathrm { N o ~ f o r w a r d i n g ~ p a t h } , } \\ { - D _ { i } ^ { v _ { 0 } , a _ { t } } ( t ) , } & { \mathrm { o t h e r w i s e } , } \end{array} \right.\tag{8}$$`
  - 三档：到达目的 = +D_avg·|V|；无转发路径 = −D_avg·|V|；否则 = 该跳时延的负值。
  - 系数：D_avg 定义见 L202 eq(10) `$$D _ { a v g } = \frac { 1 } { | \mathcal { T } | } \sum _ { i = 1 } ^ { I } D _ { i } ^ { v _ { s } , v _ { d } }$$`；乘 |V| 做量纲放大。
  - 归一化：无显式归一化（用 |V| 缩放）。
  - 折扣 γ：**未报告**（Table I 列了 η=0.005、l_r=0.5，无 γ）；伪码 L157 的 y_j 中也未出现 γ。这是本批唯一给了两跳回报却未给折扣因子的一篇。
- 转移/终止：终止 = a_t = v_d（到达目的）或无转发路径（伪码 L152 "if `$a _ { j }$` isn't the destination node then"）。
- 多步回报：**有，显式两跳**（见第 2 项，本批唯一）。资格迹：未见（检索 `n-step|eligibility|trace` 0 命中）。

**2. 学习算法与更新式**
- 算法：DDQN。L131 "We utilize the Double Deep Q-Network (DDQN) technique in SDDRL-SR. This technique involves maintaining a main network that estimates the overall value of taking an action in a specific network state. ... In addition, the agent maintains a target network that is used to update the parameters of the main network. The advantage of this technique is that it mitigates estimation bias and improves training stability."
- **两跳 TD 目标（核心）**，伪码 L152-162：
  - L157 "Set `$y _ { j } = r _ { j } + r _ { j + 1 } + Q ^ { ' } ( s _ { j + 2 } , a _ { j + 2 } , \theta ^ { ' } ) ;$`"
  - L159 "Set `$y _ { j } = r _ { j } + Q ^ { ' } ( s _ { j + 1 } , a _ { j + 1 } , \theta ^ { ' } ) ;$`"
  - L162 "Set `$y _ { j } = r _ { j } ;$`"
  - 原文表述 L133 "If the packet can reach the destination node within two hops, the true value is set to the corresponding reward. Otherwise, the true value is calculated by adding the reward value of the two hops to the residual benefit estimate `$Q ^ { ' } ( s _ { j + 2 } , a _ { j + 2 } , \theta ^ { ' } )$`. We refer to it as the Two-Hop Convergence method."
- 网络更新 L166 "Update parameters of main network by mean-square error: `$\theta  \theta + \frac { 1 } { K } \sum _ { j = 1 } ^ { K } \eta \nabla _ { \theta } ( y _ { j } - Q ( s _ { j } , a _ { j } , \theta ) ^ { 2 } ) ;$`"
- 目标网软更新 L168 "`$\theta ^ { ' }  l _ { r } \theta + ( 1 - l _ { r } ) \theta ^ { ' } ;$`"，Table I "Soft update factor (l_r) | 0.5"。
- 网络结构：Table I "Number of hidden layers of DDQN | 3"；宽度与激活函数**未报告**；图算子未见。
- 探索（Dijkstra 蒸馏）：L124 `$$a _ { t } = { \left\{ \begin{array} { l l } { \operatorname { r a n d o m \ a c t i o n , } } & { { \mathrm { i f } } \ \epsilon , } \\ { \operatorname { a c t i o n \ o f \ t h e \ D i j k s t r a , } } & { { \mathrm { i f } } \ 1 - \epsilon , } \end{array} \right. }\tag{9}$$` —— 用 Dijkstra 动作**替换 ε-greedy 的利用分支**；L121 "We replace the optimal action in `$\epsilon - g r e e d y$` with the action generated by Dijkstra's algorithm"。

**3. 信用分配**
- 逐跳即时奖励：eq(8) otherwise 分支 = −D_i(t)（下一跳链路时延）。
- 路径级终局：+D_avg·|V|（仅到达目的）。
- 分解到链路：分解到**单跳链路时延** `$D _ { i } ^ { v _ { 0 } , a _ { t } } ( t )$`。
- 是否区分损失原因：**部分区分** —— eq(8) 把 "No forwarding path" 单列一档（L111 "the agent receives a sufficiently large negative reward as a penalty"），是本批唯一为"无路可走"单设奖励档的。
- 检索 `credit assignment|counterfactual|decompos` 0 命中（无形式化信用分配）。

**4. 状态里有没有时间信息？**
- **没有**。L98 四字段均为瞬时：当前/目的位置（静态拓扑量）、当前可用存储、邻居信息。
- 检索 `EWMA|moving average|history of|trend|differential|window` 仅命中 1 处，且是**反面证据** —— L119 "instead of using historical data to pretrain the agents, DIRL uses the Dijkstra function as a target strategy and the agents learn on future real data."（明确拒绝用历史数据）。
- 注意：两跳机制是**前瞻**（预测 s_{j+2}），不是向后聚合历史；两者不可混为一谈。

**5. 动作有没有时间结构？**
- 逐包决策：L96 "The state, action, and reward of the SDDRL-SR when receiving the event `$\dot { \bf 1 } = ( v _ { s } , v _ { d } )$`"。
- 动作驻留/流级缓存/摊销：未见。切换代价：未见。
- 触发式更新：有——触发源是"包到达"而非时钟；伪码 L141 "Each agent maintains a table containing information about two-hop range nodes;"。
- ε 退火：L183 "we set `$\epsilon = 0 . 8$` and gradually decrease it with the number of training rounds"。

**6. 多智能体设定**
- 独立学：L96 "each satellite is considered as an agent of DRL that makes routing decisions with the help of neighboring agents."；伪码 L136-138 "Initialize the main networks Q(s, θ) and target networks `$Q ^ { ' } ( \mathrm { s } , \theta ^ { ' } )$` with weights `$\theta$` and `$\theta ^ { ' }$` that are obtained by pre training for all agents"。
- 共享参数：**表述含糊** —— "for all agents" 可读作共享，但未明说是否共用同一组 θ。检索 `parameter sharing|shared parameters` 0 命中 → 判定**未见明确共享**。
- 非平稳处理：**识别但未机制化** —— L133 "Traditional multi-agent reinforcement learning learns forwarding strategies based on information from neighboring nodes, so the state of LSN propagates linearly among the agents. When the network state changes, it takes some time for the distant agents to perceive the change, which results in a lag in the forwarding policy."（以两跳扩大感知域缓解）。
- 通信：L96 "makes routing decisions with the help of neighboring agents"；两跳表本地维护。

**7. 训练协议**
- 训练分布 vs 评估分布：**同一套**（同一 7x7 仿真；无跨分布迁移实验）。L175 "synthetic data representative of user requests is generated for experimental purposes."
- 两阶段：预训练（Dijkstra 引导）→ 在线执行（两跳收敛）。L133 "In the online execution phase, a Two-Hop Convergence method which updates the routing policy by predicting the future two-hop state of the data is designed to sense network state faster."
- 采样：replay memory + mini-batch，L129；Table I "The size of mini-batch (K) | 16"、"Number of events in an episode (I) | 3000"、"Number of episode (M) | 1000"。
- 训练方法消融：L199 "SDDRL-SR with Dijkstra-Aided processes packets with much better average latency than SDDRL-SR without Dijkstra-Aided. Moreover, while the former converges at around 400 steps, the latter's performance keeps improving and still has not converged at 1000 steps."（**训练信号来源的消融，非算法部件消融**）。

**8. 该文的算法贡献（与 1–7 的具体改动对应）**
(1) 用 **Dijkstra 动作替换 ε-greedy 的 argmax 分支**做蒸馏式预训练（eq 9，对应第 2/7 项）；(2) **两跳 TD 目标** `$y _ { j } = r _ { j } + r _ { j + 1 } + Q ^ { ' } ( s _ { j + 2 } , a _ { j + 2 } , \theta ^ { ' } )$` 扩大感知域（对应第 2 项），并配 eq(8) 三档奖励把"无转发路径"单列（对应第 3 项）。

**9. 该文自述的局限（逐字）**
- L226 "In future work, we expect to improve the way agents collaborate with each other to achieve better satellite routing results."
- L119 对方法边界的自述："DIRL avoids the problem of supervisory data being difficult to collect and also avoids the problem of overfitting to historical data."

**10. 该文没有考察的算法选择（基于 1–7 实际内容）**
- **奖励是标量、从未分解**：eq(8) 为单一标量；所谓"三档"是按情形分支，不是多目标向量（对比同批 UKBSA7WN eq 8/9）。
- **状态逐字段均为瞬时量、无任何时间聚合**（第 4 项）：且其两跳是**前瞻**而非历史聚合。
- **从未比较过不同训练分布**：训练与评估同源同分布（第 7 项）。已做的是 Dijkstra-aided vs 无引导的消融，那是**训练信号来源**差异，不是**分布**差异。
- **从未隔离两跳的净效应**：L193 的 DQN 对比写 "The agent updates the forwarding policy based on `$r _ { t } + Q ( s _ { t } , a _ { t } )$` only without predicting the state of the user request two hops in the future"，但 DQN 与 SDDRL-SR 还同时差在网络/奖励细节，两跳的独立贡献未被消融；且 eq(11)/(12) 的下标本身错位（L211 `$y _ { t } = r _ { t } + r _ { t + 1 } + Q ^ { ' } ( s _ { i + 1 } , a _ { i + 1 } , \theta ^ { ' } )$` vs L215 `$y _ { t } = r _ { t } + Q ^ { ' } ( s _ { i + 2 } , a _ { i + 2 } , \theta ^ { ' } )$`）。
- **折扣因子 γ 未报告**（Table I 无 γ 行）——对一个显式做两跳回报的方法，γ 缺失使回报尺度不可复现。
- 从未使用动作掩码（检索 0 命中）。
- 网络宽度、激活函数未报告。

**11. 可复用的具体机制（含公式）**
1. **两跳 TD 目标**：L157 `$y _ { j } = r _ { j } + r _ { j + 1 } + Q ^ { ' } ( s _ { j + 2 } , a _ { j + 2 } , \theta ^ { ' } )$`（配 L159/L162 的终止短路）。原文缺 τ 步折扣，移植时建议补成 `$y_j=\sum_{k=0}^{1}\gamma^{k}r_{j+k}+\gamma^{2}Q'(s_{j+2},a_{j+2},\theta')$`。
2. **传统算法蒸馏替换利用分支**：L124 eq(9)；原文强调其与监督式预训练的区别（L119，第 4 项引）。
3. **"无路可走"单列奖励**：eq(8) 第二分支 `$- D _ { a v g } ^ { v _ { s } , v _ { d } } | \mathcal { V } |$`，把可达性失败与高时延分离。

**12. 该文实验合同里与"负载"相关的设置（仅作实验条件登记，不作贡献）**
- 星座 L183 "we constructed a 7x7 LEO network model, which means that there are seven satellite orbits, seven satellites per orbit, for a total of 49 satellites."
- 链路/存储 L183 "The link capacity is 1 Gbps and storage space for request is 15GB of each ISL. The size of each request is 100MB. Thus, the satellite can only process a maximum of ten user requests at a time and store a maximum of 150 requests simultaneously."
- 失效注入 Table I (L206) "Link failure probability | 0.1"；L218 测试突发 ISL 失效。
- 训练量：Table I "Number of events in an episode (I) | 3000"、"Number of episode (M) | 1000"、"Learning rate of DDQN (η) | 0.005"、"The size of mini-batch (K) | 16"、"The probability of exploration in ε − greedy(ε) | 0.8"。
- 仿真栈 L175 "We used Python, Pytorch and Gym"。

---

## UKEKU5ZG MARL-JR：集中预训练 Q 表 + 周期广播

**1. MDP 定义**
- 形式：L132 "The data forwarding process between satellites can be modeled as a finite-state Markov chain, where the terminal state corresponds to the successful delivery of the data packet to the destination node. The Markov decision process (MDP) can be defined by `$( S , A , P , R )$`"。
- 状态 s_t（逐字段）：L134 "State: The global environmental state of the satellite network at time `$t ,$` denoted as `$s e _ { t } \in S _ { \cdot }$`, is defined as `$s e _ { t } = \left\{ N _ { c } , N _ { a } , q _ { 1 } ^ { t } , q _ { 2 } ^ { t } , \dots , q _ { N u m _ { v } } ^ { t } \right\}$` , where `$N _ { c }$` and `$N _ { a }$` represent the current and destination nodes of the data packet, and `$q _ { i } ^ { t } ( 1 \leq i \leq N u m _ { v } )$` indicates the queue length of i node at time t."
  - 字段：N_c（当前节点）、N_a（目的节点）、q_i^t（**全网 Num_v 个节点的队列长度**）。
  - 维度：Num_v = 49（Table 4 L203 "Total satellites | 49"）。
  - 归一化：无（队列上限 Table 5 "Maximum queue length q_max | 200"）。
  - 时间聚合：无。
- 动作 a_t：L136 "The action `$a _ { t } \in A c t = \left\{ Q _ { 1 } , Q _ { 2 } , \dots , Q _ { p } \right\}$` corresponds to the forwarding decision for the data packet ... In LEO satellite networks, each satellite can establish connections with a maximum of four neighboring satellites [22], thus `$\operatorname* { m a x } ( p ) = 4$`"。
  - 注：记号不一致 —— 动作集写作 `$\{ Q _ { 1 } , \dots , Q _ { p } \}$` 却描述为"转发到第 i 个节点"，登记备查。
  - 掩码：未见。
- 奖励 r_t（逐字 LaTeX）L143 `$$r e w a r d _ { j } = \left\{ \begin{array} { l r } { q _ { m a x } } & { N _ { j } i s t h e d e s t i n a t i o n } \\ { q _ { m a x } - w _ { 1 } * g _ { j } - w _ { 2 } * D _ { i j } } & { \mathrm { o t h e r w i s e } } \end{array} \right.\tag{3}$$`
  - 负载项 L147 `$$g _ { j } = q _ { r e c e i v e } + q _ { s e n d } + q _ { o c c u p i e d }\tag{4}$$`
  - 含义 L138 "The reward function is influenced by two key factors—propagation delay `$D _ { i j }$` and the load condition `$g _ { j } .$`"；L140 "where `$w _ { 1 } , w _ { 2 }$` are the weighting coefficients that balance the objectives of load balancing and delay minimization. If the neighboring node is the destination node, the reward is set to `$q _ { m a x }$` to prioritize rapid data delivery to the destination."
  - 系数数值：Table 5 L210 "Load weight ω1 | 5"、"Delay weight `$\omega _ { 2 }$` | 1"、"Maximum queue length `$q _ { m a x }$` | 200"。
  - 归一化：无（以 q_max=200 为共同尺度）。
  - 折扣 γ：Table 5 "Discount factor `$\gamma$` | 0.9"；学习率 "Learning rate for Q-table Initialization | 0.7"、"Learning rate for operational phase | 0.3"。
- 转移/终止：终止 = 到达目的（r = q_max 分支）。资格迹/多步回报：未见（检索 `n-step|eligibility|trace` 0 命中）。

**2. 学习算法与更新式**
- 算法名：MARL-JR，但更新式即 Q-routing。
- 更新式 L105 `$$Q _ { i } ( s , a ) = ( 1 - \alpha ) Q _ { i } ( s , a ) + \alpha \biggl [ r + \gamma _ { a ^ { \prime } \in \mathrm { A } _ { \mathrm { c } } } ^ { m a x } Q _ { j } \bigl ( s ^ { \prime } , a ^ { \prime } \bigr ) \biggr ]\tag{1}$$` —— 与 Y2H4NPLU eq(8)、UKBSA7WN eq(2)、53HEEK33 eq(2) 同族：**邻居 Q 表 bootstrap**。
- 运行期 Q 值分解式 L182 `$$Q _ { i } ( s , a ) = ( 1 - \alpha ) R _ { i } + \alpha \gamma ( R _ { i + 1 } + R _ { i + 2 } + \cdot \cdot \cdot + R _ { n } ) |\tag{6}$$`（原文末尾带一个多余的竖线），L179 "Consequently, `$Q ( s , a )$` is determined by the reward conditions of traversed nodes rather than all nodes in the network, where n specifies the index of the final destination node"。
- 路径总 Q L186 `$$Q _ { s u m } = \sum _ { i } ^ { n } Q _ { i } ( s _ { i } , a _ { i } )\tag{7}$$`，L179 "A higher Q-value indicates a more optimal forwarding path selection, and a higher total Q-value corresponds to the globally optimal path."
  - 注：eq(6)(7) 与同批 53HEEK33 eq(5)(6) 形式几乎相同，登记备查（同课题组写作脉络）。
- double/target net：未见。网络结构：无神经网络，Q 表（Table 2，L111）。

**3. 信用分配：这篇怎么把奖励归到动作上？**
- 逐跳即时奖励：eq(3) otherwise 分支（q_max − w1·g_j − w2·D_ij）。
- 路径级终局：q_max（=200）。
- 分解到节点：分解到**下一跳 j** 的负载 g_j（含收/发/占用三项，eq 4）与链路时延 D_ij。
- 是否区分损失原因：未见。检索 `credit assignment|counterfactual|decompos` 0 命中；无丢包/失联独立项（丢包只在评测侧出现，L245）。
- 单列说明：L255 把 "incorporation of a residual load factor for congestion-aware routing" 列为相对 Q-Routing 的两项改进之一，即 eq(4) 的 g_j。

**4. 状态里有没有时间信息？**
- **没有**。L134 的 q_i^t 为 t 时刻瞬时队列长度；g_j（eq 4）为接收+发送+占用的瞬时计数之和，**非差分、非 EWMA**。
- 检索 `EWMA|moving average|history of|trend|differential|window` 命中 2 处（L234 "limitations in handling highly dynamic networks"、L255 "declining performance trends"），均为结果叙述，非状态特征。
- 唯一的时间结构在**通信协议**：L152 "At regular time intervals T, the link-state information within the network is updated, and the agents correspondingly update their Q-tables based on the received information."

**5. 动作有没有时间结构？**
- 逐包决策：L130 "When a data packet arrives at satellite node `$N _ { i } ,$` the node `$N _ { i }$` will select the most appropriate action `$a _ { t }$` ... to forward the packet to node `$N _ { j }$`"。
- 动作驻留/流级缓存：未见。切换代价：未见。
- **触发式 + 周期双轨更新**：L189 "This study proposes a periodic broadcasting mechanism. Upon receiving a data packet, a node actively broadcasts its Q-table and link-state information, enabling receiving nodes to promptly update their own Q-tables and improving learning efficiency. When a satellite's neighbor nodes change, the affected node updates both its Q-table and link-state information, subsequently propagating these updates to new neighbors to maintain network-wide information consistency."
- 队列优先级（差分服务，**本批唯一**）：L163 "The queue determines the packet forwarding priority when it is not empty, while the node prioritizes transmitting the highest-priority packet first, thereby satisfying differentiated forwarding requirements for data of varying levels of importance."
- ε 退火，**有显式衰减因子**：L165 "a ε decay factor µ is introduced. As the iterations progress, the probability of randomly selecting the next hop is reduced. As shown in Equation (5), the selection of the next hop will be impacted by `$\mu ^ { \mathrm { t } } \varepsilon .$`" → L168 `$$a _ { t } = \left\{ \begin{array} { l r } { { \mathrm { r a n d o m ~ a c t i o n ~ } } } & { { \mathrm { p r o b a b i l i t y : \mu ^ { t } \varepsilon } } } \\ { { \mathrm { m a x } ( Q _ { t + 1 } ) } } & { { \mathrm { p r o b a b i l i t y : 1 - \mu ^ { t } \varepsilon } } } \end{array} \right.\tag{5}$$`。Table 5 "`$\varepsilon$` decay factor µ | 0.998"、"Greedy factor ε | 0.8"。

**6. 多智能体设定**
- 独立学：L102 "In LEO satellite networks, each satellite acts as an agent, capable of independent learning and forwarding state information. Each agent maintains a Q-table, which records the Q-values for forwarding data packets to neighboring nodes."
- **集中预训练 + 分布式执行**（该文核心）：L156 "we employ ground-based pre-training to initialize the Q-table"；L173 "The centralized approach of periodically acquiring global satellite network information and reinitializing the Q-tables can effectively reduce the computational burden of online training on satellite nodes, while simultaneously improving routing accuracy."
- 共享参数：不适用（per-node Q 表）。
- 非平稳处理：**有** —— 周期广播 + 失效标记，L152 "if a satellite fails to receive the ISL state information within a predefined time interval, it is flagged as faulty, and all associated links are deactivated."
- 通信：L152 "we adopt a periodic broadcasting mechanism for link-state information ... 'hello' packets only transmit local neighbor and link-state information from the originating node. It significantly reduces network overhead and decreases nodal computational loads."
- 动作同步：无。

**7. 训练协议**
- **训练分布 vs 评估分布：同源但阶段分离** —— 地面预训练初始化 Q 表，星上运行期继续在线更新；训练输入为初始拓扑 `$G _ { t _ { 0 } }$`（L161 "The Q-table Initialization process is conducted based on the initial topology of the satellite network, denoted as `$G _ { t _ { 0 } } ,$`"）。
- 包生成：L161 "data packets will be generated upon the arrival of the previous packet, with randomly assigned source and destination nodes."（**上一包到达后才生成下一包**，与本批其他篇的固定速率/泊松到达不同）。
- 拓扑变化：L177 "a temporal network model is adopted during the operational phase of the satellites"。
- 训练步数：Table 5 "Number of episodes | 40"、"Number of steps peer episode | 300"。
- 失效注入（评测侧）：L230 "we primarily simulate link failures and node malfunctions through stochastic edge deletion and restoration in the graph representation. The simulation constrains the maximum number of simultaneous link failures during any single routing process to five"。

**8. 该文的算法贡献（与 1–7 的具体改动对应）**
(1) **地面集中预训练 Q 表 + 周期性重初始化**（L171 "the Q-table Initialization scheme conducted via ground stations can be periodically reapplied"），对应第 6/7 项；(2) **周期广播取代"随包携带"**（L152/L189），对应第 5/6 项；(3) **残留负载因子 g_j = q_receive + q_send + q_occupied**（eq 4）进入奖励，对应第 1/3 项 —— 原文 L255 自述为相对 Q-Routing 的第一项改进。

**9. 该文自述的局限（逐字）**
- L264 "Future research will focus on extending the reinforcement learning framework to diverse satellite network scenarios and complex link connectivity conditions to further enhance its applicability and performance."

**10. 该文没有考察的算法选择（基于 1–7 实际内容）**
- **奖励是标量、从未分解**：eq(3) 为单一标量 —— w1·g_j 与 w2·D_ij 的加权求和在**奖励内部**完成，不是向量奖励（对比同批 UKBSA7WN eq 8/9 保留向量）。且**从未考察 w1/w2 的敏感区间**，只报一组 (5, 1)（Table 5）。
- **状态逐字段均为瞬时量、无任何时间聚合**（第 4 项）：q_i^t 是快照；g_j 是三个瞬时计数之和，不是差分。
- **从未比较过不同训练分布**：预训练用 `$G_{t_0}$` 初始拓扑、运行期用真实演化拓扑（第 7 项），但**两者的分布差异未被设计为实验变量**。
- **从未做"周期广播 vs 随包携带"的消融**：这是该文自述的第二项改进（L255），但实验只与 DR-BM 和 Q-Routing **整体**对比（L224-226），未隔离广播周期 T 的效应；而原文自己承认 T 是关键旋钮 —— L189 "The smaller the broadcasting period T, the more frequently agents can perceive network state changes."
- 从未使用动作掩码（检索 `mask|invalid action|infeasible` 0 命中）。
- 从未使用多步回报/资格迹（检索 0 命中）。
- 从未考察预训练重初始化周期（"periodically reapplied"，L171）的取值。
- 状态含全网 Num_v 个队列但不做压缩或注意力。

**11. 可复用的具体机制（含公式）**
1. **残留负载因子**：L147 `$g _ { j } = q _ { r e c e i v e } + q _ { s e n d } + q _ { o c c u p i e d }$` 进入奖励 L143 `$q _ { m a x } - w _ { 1 } * g _ { j } - w _ { 2 } * D _ { i j }$`，权重是以 q_max 为共同尺度的绝对量（q_max=200, w1=5, w2=1），可直接照搬为负载项。
2. **地面预训练 + 周期性重初始化**：L171 "owing to the predictable nature of satellite networks, the Q-table Initialization scheme conducted via ground stations can be periodically reapplied. This approach mitigates potential inaccuracies in the online-trained Q-table that are caused by significant changes in the satellite network topology" —— 对 LEO 可预测轨道这一先验的**显式利用**，是"预训练 + 漂移重置"的直接模板。
3. **索引式 ε 退火**：L168 eq(5) 的 `$\mu ^ { t } \varepsilon$`，Table 5 µ=0.998、ε=0.8 —— 比连续退火更易复现（只需两个数）。

**12. 该文实验合同里与"负载"相关的设置（仅作实验条件登记，不作贡献）**
- 星座 L200 "an Iridium-like satellite constellation [24] with an orbital altitude of 780 km, an inclination of 86.4°, and seven orbits with seven satellites each."；Table 4：49 星 / 7 面 / 7 星每面 / 780 km / 86.4°。
- 负载：L245 "under a traffic load of 3000 packets in the network"；L250 "under the condition of 3000 packets circulating in the network"；L255 "maintaining a constant network load of 3000 data packets"。
- 负载均衡判据 L245 "the load balancing condition is represented by the variance of the packet counts across nodes, where a lower variance indicates a more balanced network load"。
- 失效注入 L230（随机删边/恢复，单次路由最多 5 条并发失效）。
- 对比算法 L224 "Data Rate Benchmark (DR-BM) algorithm" 与 L226 "The Q-routing algorithm"。
- 集中式开销对照 L218（地面站周期性获取全局信息）。
