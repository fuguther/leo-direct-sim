# DOSSIER B3 — 逐篇算法拆解（Batch 3：风险/奖励设计/图算子/多径族）

> 批次 itemKey：39NJWBI7、9C6HB6AF、XM64YRAW、MXQVNU3P、2FBBURX7、GPDPLJNG、GPLEP83L、6GWNYSTT
> 材料：VM `/data/liguang13/topic-loop-r2/md/<itemKey>/<itemKey>/txt/<itemKey>.md`（MinerU MD）
> 格式：强制 12 项模板（`EXTRACTION-TEMPLATE.md`），每项带 MD 行号 + 逐字英文原文；公式逐字抄 LaTeX。
> 镜头：主体是算法（状态/记忆、动作/策略、奖励、价值与信用分配、多智能体交互、训练与适应、决策结构）；负载/评测设置仅作实验条件登记（第 12 项）。
> 核验：全部逐字引文经归一化子串比对脚本（`norm = lowercase + [^a-z0-9]+ → 单空格`）对 MD 原文回核，结果汇总见文末「核验记录」。

---

## 39NJWBI7 Asynchronous Risk-Aware Multi-Agent Packet Routing for Ultra-Dense LEO Satellite Networks

**1. MDP 定义**
- 建模为 per-packet 的 POCSMDP，L162 给出元组 `<S,A,T,r,{c_k},O,H,γ_r,γ_c>_p`。
- **状态 s_t**：L164 仅有整体描述，未逐字段给维度/归一化：
> "A state $s _ { h } \in \mathcal { S }$ is a snapshot of the network’s physical status and packetspecific information at the h-th hop." (L164)
  观测 L170：
> "which includes packet state and local node/neighbor statistics" (L170)
  → 无字段级定义，**无任何时间聚合**（见第 4 项）。
- **动作 a_t**：L166
> "the set of four outgoing ISLs (NSWE)" (L166)
  |A|=4（四个方向出链路），无动作掩码（全文 `grep -n -i 'mask'` 543 行 0 命中）。
- **奖励 r_t**：逐跳奖励 L400-406，逐字：
$$
r _ { h } = \frac { \tau } { D _ { n o r m } } - c _ { h } + \Delta d + B _ { p }\tag{35}
$$
> "where τ is the total action delay, and $\Delta d$ provides a dense reward for geographic progress towards the destination, which measured by the difference of Great Circle Distance (GCD). A large terminal reward $B _ { p }$ is added at the final hop to prioritize successful packet delivery" (L400)
$$
B _ { p } = \left\{ \begin{array} { l l } { 1 + L _ { p } , } & { \mathrm { i f ~ } p \mathrm { ~ i s ~ d e l i v e r e d , } } \\ { - \frac { 5 \tau _ { p } ^ { t t l } } { D _ { n o r m } } - \sum _ { j = 0 } ^ { h } \Delta d _ { G C D } , } & { \mathrm { i f ~ } p \mathrm { ~ i s ~ d r o p p e d , } } \\ { 0 , } & { \mathrm { e l s e , } } \end{array} \right.\tag{36}
$$
  cost（约束量）L397：
> "we define the cost function as the normalized queuing delay $c _ { h } = D _ { h } ^ { Q } / D _ { n o r m } ,$ where $D _ { h } ^ { Q }$ is the queuing delay experienced when packet $p$ is forwarded over a link at hop $h ,$ and $D _ { n o r m } = 1 0 0$ ms is a predefined constant for normalization." (L397)
  奖励本身**未归一化**（只有 cost 归一化）；折扣 $gamma_r=0.99$、$gamma_c=0.97$（L395），按 hop 指数 $gamma^h$（L180）。
- **转移/终止**：半马尔可夫（semi-Markov），可变时长 $	au$（L168）；episode = 单个包的整段旅程（L158）；TTL $H=64$（L393）。无资格迹、无 n-step 回报（`grep -n -iE 'eligibility|n-step|multi-step'` 0 命中）。

**2. 学习算法与更新式**
- 原名：PRIMAL-Avg / PRIMAL-CVaR，L226 定位为离散 SAC 的 primal-dual 扩展。Bellman（L250-256）：
$$
Q _ { \phi } ^ { r } ( o , a ) = r ( o , a , o ^ { \prime } ) + \gamma _ { r } \mathbb { E } _ { a ^ { \prime } \sim \pi _ { \theta } ( \cdot | o ^ { \prime } ) } \left[ Q _ { \phi } ^ { r } ( o ^ { \prime } , a ^ { \prime } ) - \alpha \log \pi ( a ^ { \prime } | o ^ { \prime } ) \right] ,\tag{20}
$$
$$
Q _ { \psi _ { k } } ^ { c } ( o , a ) = c _ { k } ( o , a , o ^ { \prime } ) + \gamma _ { c } \mathbb { E } _ { a ^ { \prime } \sim \pi _ { \theta } ( \cdot \vert o ^ { \prime } ) } \left[ Q _ { \psi _ { k } } ^ { c } ( o ^ { \prime } , a ^ { \prime } ) \right]\tag{21}
$$
TD 目标（L267-273）：
$$
y _ { \phi ^ { \prime } } ^ { r } = r + \gamma _ { r } \pi _ { \theta } ^ { \top } ( o ^ { \prime } ) \left( Q _ { \phi ^ { \prime } } ^ { r } ( o ^ { \prime } ) - \alpha \log \pi ( o ^ { \prime } ) \right) ,
$$
$$
y _ { \psi _ { k } ^ { \prime } } ^ { c } = c _ { k } + \gamma _ { c } \pi _ { \theta } ^ { \top } ( o ^ { \prime } ) Q _ { \psi _ { k } ^ { \prime } } ^ { c } ( o ^ { \prime } ) ,\tag{22}
$$
critic 损失（L279-283）：
$$
\mathcal { L } _ { \phi } = \mathbb { E } _ { ( o , a , r , o ^ { \prime } ) \sim \mathcal { D } } \left[ \frac { 1 } { 2 } \left( Q _ { \phi } ^ { r } ( o , a ) - y _ { \phi ^ { \prime } } ^ { r } \right) ^ { 2 } \right] ,\tag{24}
$$
$$
\mathcal { L } _ { \psi _ { k } } = \mathbb { E } _ { ( o , a , c _ { k } , o ^ { \prime } ) \sim \mathcal { D } } \left[ \frac { 1 } { 2 } \left( Q _ { \psi _ { k } } ^ { c } ( o , a ) - y _ { \psi _ { k } ^ { \prime } } ^ { c } \right) ^ { 2 } \right] ,\tag{25}
$$
actor 损失（L289）与乘子更新（L297）：
$$
\mathcal { L } _ { \boldsymbol { \theta } } = \underset { o \sim \mathcal { D } } { \mathbb { E } } \left[ \pi _ { \boldsymbol { \theta } } ^ { \top } ( o ) \big ( \alpha \log \pi _ { \boldsymbol { \theta } } ( o ) - Q _ { \boldsymbol { \phi } } ^ { r } ( o ) + \sum _ { \boldsymbol { k } } \lambda _ { \boldsymbol { k } } Q _ { \boldsymbol { \psi } _ { \boldsymbol { k } } } ^ { c } ( o ) \big ) \right]\tag{26}
$$
$$
\mathcal { L } _ { \lambda _ { k } } = \underset { o \sim \mathcal { D } } { \mathbb { E } } \left[ \lambda _ { k } \left( \pi _ { \theta } ^ { \top } ( o ) Q _ { \psi _ { k } } ^ { c } ( o ) - D _ { k } \right) \right] ,\tag{27}
$$
- CVaR 变体：cost critic 换成 IQN，分布 Bellman L315、分位点 Huber L357、CVaR 近似 L370：
> "CVaR is then approximated by averaging the critic’s output for these tail-end quantile fractions:" (L368)
$$
\Gamma _ { \epsilon _ { k } } ( o , a ) \approx \frac { 1 } { N ^ { k } } \sum _ { m = 1 } ^ { N ^ { k } } Q _ { \psi _ { k } } ^ { c } ( o , a , \zeta _ { m } ) .\tag{32}
$$
- 目标网络：有（`mirrored parameters` L276；Algorithm 1 步 25-26 L343-344 软更新）。
- **负向声明（精确模式 + 实测计数）**：
  - `grep -ciE "double (q|dqn)"` = **0**；`grep -ciE "dueling"` = **0**；`grep -ciE "prioritized (experience )?replay"` = **0** → 无 double Q、无 dueling、无优先回放。
  - `grep -ciE "\bper\b"` = **6**，命中 L23 / L264 / L354 / L379 / L393 / L397，**全部为散文或 LaTeX 中的 "per time slot / per-action / per-sample / per run / per-hop"**，不构成优先回放反例。
  - （先前裸模式 `double|dueling|priorit` 有 1 命中 = L403 `"to prioritize successful packet delivery"`，系 `priorit` 误命中 `prioritize`；实质结论不变，模式已收紧。）
- 网络结构 L395：
> "the actor $\left( \pi _ { \boldsymbol { \theta } } \right)$ and critics $( Q _ { \phi } ^ { r } , \ Q _ { \psi _ { k } } ^ { c } )$ use a shared backbone, a two-layer MLP with 512 hidden units, to process observations. Each component has a separate MLP output head. For the PRIMAL-CVaR variant, the cost critic $Q _ { \psi _ { k } } ^ { c }$ is an IQN suggested in [39] with two layers and quantile parameters $N = N ^ { \prime } = N ^ { k } = 6 4$ . All algorithms use a mini-batch size of 1024, a replay buffer size of 300000, and discount factors $\gamma _ { r } = 0 . 9 9$ and $\gamma _ { c } = 0 . 9 7$" (L395)
  激活函数未给出（`grep -n -i 'activation'` 0 命中）；**不使用图算子**。

**3. 信用分配**
逐跳即时 dense reward + 逐跳归一化 cost，终局 $B_p$ 区分 delivered/dropped 两种结局（L400-406）。路径级约束被"逐跳化"表达，L145：
$$
D _ { p } ^ { Q } = \sum _ { h , ( i , j ) } x _ { p , i j } ^ { h } \cdot D _ { i j } ^ { Q } ( \tau _ { p } ^ { h } ) \leq D _ { m a x } ^ { Q } , \quad \forall p \in \mathcal { P }\tag{C4}
$$
> "where $D _ { m a x } ^ { Q }$ is a predefined threshold." (L148)
奖励是**标量**，未分解到链路/邻居；"损失原因"只体现在 $B_p$ 的两个分支（delivered / dropped），dropped 分支再拆成 TTL 惩罚与 GCD 倒退惩罚（L406）。

**4. 状态里有没有时间信息**
**未见**。L164 明写 snapshot；L170 只列 packet state 与 local node/neighbor statistics。检索（精确模式 + 实测计数，范围 = 全文 543 行）：`grep -ciE "ewma|history|window|trend"` = **1**，唯一命中 **L472**，为参考文献标题 `"…: Paradigm, solutions, and trends,"` → 属 `trends` 误命中；拆开计 **ewma 0 / history 0 / window 0**。故判：状态无任何历史/差分/EWMA。→ 无历史/差分/EWMA 任何形式。唯一时间量 $	au$（动作时延）只进奖励 (35)，不进状态。

**5. 动作有没有时间结构**
每包独立决策，L176：
> "This event-driven formulation ensures that satellites react to packet arrivals in real-time based on current local information. While each packet defines a conceptual learning episode, the physical agents are the satellites." (L176)
事件驱动收集 transition（L325-329）：
> "for each event e do" (L325)
  → packet arrival 才出动作（L326）、action completion 才落 $(o',r,{c_k})$（L329）。动作驻留 = 一跳；奖励 (35) 中**无切换/重路由惩罚项**；无流级缓存/摊销机制。

**6. 多智能体设定**
独立学习 + 参数共享：单一同质策略 $pi_	heta(a|o)$，本地执行、全网共享（L176）。非平稳处理靠策略熵，L180：
> "maintaining a certain level of policy stochasticity is beneficial for ... mitigating the non-stationary environment issue" (L180)
训练侧 CTDE 共享经验池，L385：
> "Note that we use a shared centralized replay buffer here by following the Centralized Training and Decentralized Execution (CTDE) paradigm during offline training." (L385)
**无智能体间显式通信/消息传递**（`grep -n -iE 'communicat|coordinat'` 命中行均指网络层通信或对他人工作的批评，L23/25/27/40/180，无一行描述自身通信通道）；**无动作同步**（异步正是其卖点，L40）。

**7. 训练协议**
训练与评估**同一分布、同一负载**，L393：
> "a 30-second training or evaluation epoch with a packet traffic rate of 10, 000 packets/s, totaling 300, 000 packets per run according to the Poisson process." (L393)
每 1 ms 迭代一次、每 2 s 上报（L393）；mini-batch 1024、replay buffer 300000（L395）；评估用 5 个随机种子（L454）。拓扑：1584 星、600 km、53°、每 100 ms 更新位置（L391）。**未见跨分布/OOD 训练；未见训练分布对比**。

**8. 该文的算法贡献（一句话）**
把路由建模为事件驱动 POCSMDP（L158-176），在其上用离散 SAC 的 primal-dual 扩展（L226、L233-301）并把 cost critic 换成 IQN + CVaR 近似（L315-382），从而在逐跳归一化队列 cost 上同时约束均值与尾部——对应第 1 项的 state/reward/cost 定义、第 2 项的 (20)-(27) 与 IQN 分支、第 6 项的 CTDE 共享池。

**9. 该文自述的局限**
无独立 Limitations 章节；有三处自述边界（逐字）：
> "Note that primal-dual CRL has been proved to have strong duality for single-agent fully observable RL [26]. However, the constrained and partially observable MARL problem of our case is fundamentally more challenging and highly nonconvex, such that there exist none known strong duality guarantees [41]. Despite this fact, primaldual approach still serves as a feasible and principled way to solve the problem approximately." (L236)
> "Note that we use a shared centralized replay buffer here by following the Centralized Training and Decentralized Execution (CTDE) paradigm during offline training." (L385)
> "we set the minimum entropy as $\bar { \mathcal { H } } \approx 0 . 0 6 7$ , which is a heuristic value considering the best action confidence to be 0.99" (L429)

**10. 该文没有考察的算法选择（重点，均基于 1-7 实见内容）**
- (a) **状态逐字段全为瞬时量，从未引入历史/窗口/趋势**——依据 L164/L170 的两句描述 + 第 4 项 grep 全空。"记忆"这一维在本文完全缺席。
- (b) semi-MDP 的可变时长 $	au$ 只出现在 L168（转移）与 (35)（奖励）中，Bellman (20)(21) 仍用 $gamma_r/gamma_c$ 按 **hop 指数**折扣；**从未比较 hop 折扣 vs 真实耗时折扣**（`grep -n -iE 'duration|elapsed'` 仅 L162/168/403 三处）。
- (c) **从未做超参敏感性**：全文只报一个约束阈值 $D_{max}^Q=10$ ms（L431）、一个风险水平 CVaR$_{0.25}$（L443/L456）；框架写了 K 个约束（L187），实验只做 queuing delay 一项（L397/L431），$arepsilon_k$ 与 $K>1$ 多约束组合从未实验。
- (d) 动作空间固定 4 个方向，**从未做动作掩码/链路可用性屏蔽**（L166 + `grep -n -i 'mask'` 0 命中）。
- (e) **从未比较不同训练分布或负载水平**：训练与评估同为 10,000 packets/s（L393）；摘要所称 "loaded scenarios"（L11）并无第二个负载设定。
- (f) 多智能体侧**从未比较"独立学习 vs 通信/协同"**（第 6 项无通信通道）。
- (g) **RL 组件从未消融**：无 double Q、无优先回放、无 n-step、无图算子（grep 0 命中），亦未见 $gamma_r/gamma_c$、$alpha$、$eta$ 的敏感性分析。

**11. 可复用的具体机制**
- **IQN + CVaR 尾部约束闭环**：$Gamma_{arepsilon_k}(o,a) approx rac{1}{N^k}sum_{m=1}^{N^k} Q(o,a,zeta_m)$，$zeta_m sim mathcal{U}(1-arepsilon_k,1)$（L370）；把它塞进 actor loss（L376）与乘子更新（L382）即得"尾部约束"闭环，可直接搬到我们的逐跳路由。
- **约束逐跳化**：把路径级累计约束（L145）落到逐跳归一化 cost $c_h = D_h^Q/D_{norm}$、$D_{norm}=100$ ms（L397），再用 $lambda_k$ 在线加权进 actor（L289）——这是"风险不进奖励、进约束"的干净做法。
- **结局分叉终局奖励**（L406）：delivered 给 $1+L_p$，dropped 给 $-5	au_p^{ttl}/D_{norm}-sumDelta d_{GCD}$，天然编码"丢包原因"。
- **事件驱动 transition 收集范式**（L325-329）：packet arrival 出动作、action completion 落 transition —— 与我们异步时隙无关的采集接口兼容。
- **熵下界可操作换算**（L429）：由 best action confidence 0.99 反推 $ar{mathcal{H}} approx 0.067$。

**12. 实验合同里与"负载"相关的设置（仅登记，不作贡献）**
单负载 10,000 packets/s Poisson，300,000 packets/run，30 s epoch（L393）；包长 80% 64.8 Kbits + 20% 16.2 Kbits（L393）；节点与链路缓冲 16 Mbits（L393）；GSL 1000 Mbps、ISL 50 Mbps（L393）；TTL $H=64$（L393）；3 城市等概率源/宿（L391）；$D_{norm}=100$ ms（L397）、$D_{max}^Q=10$ ms（L431）；拓扑 1584 星 / 600 km / 53° / 每 100 ms 更新（L391）。

---

## 9C6HB6AF Deep Reinforcement Learning-Based Multipath Routing for LEO Megaconstellation Networks

**1. MDP 定义**
- 明确声明为 MDP，且**以"不依赖历史状态"为前提**，L266：
> "Since the traffic assignment decision in satellite networks depends on the current node and surrounding node states in the network, independent of the historical state, the multipath traffic scheduling subproblem can be described as a Markov decision process (MDP)." (L266)
- **状态 s_t** = $[C_t, TR_t, G_t, P_t]$（L282）：$C_t$ 残差带宽向量 $c_i = BW - f_i$（L276 (23)）；$TR_t$ 时段流量需求矩阵（L273）；$P_t$ 路径矩阵 $p_{i,j}={e_1..e_{H_{max}}}$（L279）；**$G_t$ 在正文无定义**（`grep -n -i 'G_t|adjacency'` 无定义行，只出现在 L282 的向量式与图 4）。
- **动作 a_t**：每路径流量比例向量（L292），维数 $M\times L$，受 $\sum_l \omega = 1$ 约束（L92 (2)）；**无动作掩码/投影机制**（`grep -n -iE 'mask|softmax|normaliz'` 全文 587 行 0 命中）。
- **奖励 r_t**：L302 与 L118：
$$
r _ { t } = \sum _ { m } \sum _ { l } U ( \bar { f } _ { m , l } , \bar { d } _ { m , l } )\tag{26}
$$
$$
U ( \bar { f } _ { t } , \bar { d } _ { t } ) = \beta _ { 1 } \log \bar { f } _ { t } - \beta _ { 2 } \log \bar { d } _ { t }\tag{6}
$$
  其中 $\beta_1+\beta_2=1$（L121）。对数效用，**标量，未见归一化**；无风险项。
- **折扣** L308-310：$R_t = \sum_{k=0}^{\infty} \rho^k r_{t+k+1}$，$\rho\in[0,1]$；实现值 $\rho=0.5$（Table 2，L427）。
- **终止** L335：
> "$\chi \in \{ 0 , 1 \}$ is used to determine whether the training of the model is complete in the current phase" (L335)
  TD 目标用 $\rho(1-\chi)$ 关断 bootstrap（L338）。

**2. 学习算法与更新式**
- **算法身份自相矛盾**：L266 写 PPO，L478/L480 写 DQN：
> "The DRL agent uses a proximal policy optimization (PPO) algorithm, which is an actor-critic algorithm." (L266)
> "Each routing node is controlled by a DQN agent" (L478)
- 但更新式 (32)-(39) 全部是 DQN + 优先回放形式（L338-L403）：
$$
y _ { i } = r _ { i } + \rho ( 1 - \chi ) [ Q ( s _ { i + 1 } , a _ { i + 1 } | \theta ^ { Q } ) ]\tag{32}
$$
$$
\delta _ { i } = | y _ { i } - Q ( s _ { i } , a _ { i } | \theta ^ { Q } ) |\tag{...}
$$
$$
P ( i ) = p _ { i } ^ { \alpha } / \sum _ { k } p _ { k } ^ { \alpha }\tag{...}
$$
$$
\mathcal{L} _ { q } = \frac{1}{N_B} \sum \omega _ { i } \delta _ { i } ^ { 2 }\tag{...}
$$
$$
\mathcal{L} _ { \mu } = - Q ( s , a | \theta ^ { Q } )\tag{...}
$$
  优先回放三件套逐字：$p_i = \delta_i + \eta$（L375）、$P(i)=p_i^\alpha/\sum_k p_k^\alpha$（L381）、IS 权重 $\omega_i=(P(i)/P_{min})^\beta$（L387）。
- **有目标网络**（Algorithm 2 输入含 target network，L343）。
- **负向声明（精确模式 + 实测计数，范围 = 全文 587 行）**：`grep -ciE "double (q|dqn)"` = **0**；`grep -ciE "dueling"` = **0** → 无 double Q、无 dueling。（优先回放则**确有**：L412 `"this paper adopts priority experience replay to speed up the convergence of the model"`，公式见 L375/L381/L387。）
- 网络结构：正文**未给**任何层数/宽度/激活/节点特征（`grep -n -iE 'gnn|graph|hidden|layer|activation|embed'` 命中均为泛泛表述）；唯一架构句 L412：
> "we adopt GNN for variable size graph structures ... they can be used to aggregate elementary features without specifying the input dimensions" (L412)

**3. 信用分配**
**积分到"整时段、全网"级别**：奖励 (26) 对全部 $M$ 条流、$L$ 条路径求和（L302），一个动作向量对应**一个标量效用**；无逐跳奖励、无逐流/逐路径分解、**无损失原因区分**（丢包只通过 (8) 的成功指示量 $\kappa_y$（L128）进入 $\bar d$）。唯一逐路径量是路径时延三分解（L86）：
$$
\eta = \sum ( q + r + \gamma / c )
$$
  但它只进约束/评估，不进信用分配。

**4. 状态里有没有时间信息**
**未见**。逐字段均为 $t$ 时刻瞬时量：$C_t$ 由 (23) 当前残差带宽（L276）、$TR_t$ 为 "within each time slot" 的需求（L273）、$P_t$ 为当前路径矩阵（L279）；L266 更把"不依赖历史"写成 MDP 成立的前提。检索（精确模式 + 实测计数，范围 = 全文 587 行）：`grep -ciE "ewma|history|window|trend"` = **2**，命中 **L64**（相关工作 `"predicting the trend of the optimization objectives"`）与 **L454**（结果曲线 `"a decreasing trend"`），均非状态特征；拆开计 **ewma 0 / history 0 / window 0**（注意：L266 的 "historical state" 未被该模式命中，因模式写的是 `history` 而非 `historical`——L266 见第 1 项引文，其语义正是"不依赖历史"）。`grep -ciE "mask"` = **0**。→ 无时间聚合/差分/EWMA/记忆。

**5. 动作有没有时间结构**
**动作按时间片驻留**，L410：
> "the network is divided into multiple time slices according to time slot intervals, and the network topology remains stable in each discrete time slice" (L410)
> "the network control center generates the split ratios for each service on different paths based on the model obtained from GMTS training and sends them to the corresponding satellites at the appropriate time before the start of each time slot." (L410)
路径集每时段由 MHMRD 重算（L410）。奖励 (26) 中**无切换代价项**；无流级缓存/摊销（每时段重新输出一组比例）。

**6. 多智能体设定**
**不是多智能体**。动作是全局 $M\times L$ 比例向量（L292）且由 NCC 集中生成（L410），单一学习体；无参数共享、无通信、无非平稳处理、无动作同步讨论。注：与 L478 "Each routing node is controlled by a DQN agent" 冲突（见第 10 项 (c)）。

**7. 训练协议**
训练数据与评估数据**并非同一套**，L429/L443：
> "the GMTS algorithm was trained using inclined orbit constellation topology and traffic matrices [37], which were deployed to the NCC after training" (L429)
> "DMR employed the same model as that used for the Iridium constellation, while the other algorithms were retrained" (L443)
即在 Iridium 上训练的同一模型直接用于 OneWeb 且不重训。采样：Algorithm 2 每轮重置 $s_0$、for $t=1:T$ 存 $(s_t,a_t,r_t,s_{t+1},\chi)$（L335/L346）。表 2（L427）：$N_g=24$、$L_q=100$、$\nabla_{pak}=1$KB、$N_B=32$、$B_{max}=100$、$\alpha=0.6$、$\beta$ 与 $\rho$ 同列 0.5。**训练步数/时长未见**（`grep -n -iE 'epoch|iteration|steps'` 仅命中 L321 的泛泛表述）。

**8. 该文的算法贡献（一句话）**
把多路径路由解耦为 MHMRD（最小跳数多候选路径，L227/算法 1 L229）+ GMTS（GNN 编码变尺寸图 → DQN/优先回放输出每路径流量比例，L266/L292/L338-403），并用对数效用 (6) 做全网单一标量奖励——对应第 1 项的状态四元组、第 2 项的 (32)-(39)、第 5 项的时间片比例下发。

**9. 该文自述的局限**
> "It should be noted that as the size of the constellation continues to expand, the computational requirements of DQN-based online routing also rise. In the future, we intend to explore the potential of adopting solutions such as multi-controller deployment to enhance the responsiveness of the network and further validate its efficacy in real-world scenarios." (L480)

**10. 该文没有考察的算法选择（重点，均基于 1-7 实见内容）**
- (a) **状态无任何时间聚合/记忆，且论文把"不依赖历史"当作 MDP 成立的前提**（L266）——"无记忆"是被默认而非被验证的选择，从未与含历史窗口/趋势的输入对比。
- (b) **GNN 这一"图算子"选择实际未被披露**：正文没有 GNN 变体（GCN/SAGE/GAT）、层数、宽度、激活、节点/边特征构造的任何信息（唯一句 L412）；**无 GNN vs MLP 消融**。
- (c) **算法身份自相矛盾**（L266 PPO vs L478/L480 DQN），而更新式 (32)-(39) 是 DQN+PER、动作却是连续比例向量 (25)——**动作空间与价值函数形式不匹配**；从未比较 PPO/DQN。
- (d) 约束 $\sum\omega=1$（L92/L136）**在动作层如何强制完全未说明**（`grep -ciE "softmax|normaliz|project"` = **2**，命中 L482/L484，二者均为 CRediT 投稿声明中的 `"Project administration"` / `"Fund Project"`，非动作层投影；**softmax 0 / normaliz 0** 命中），也未见约束违反率指标。
- (e) **奖励是唯一标量** (26)，从未分解到流/路径/链路，**完全没有风险/尾部指标**（`grep -ciE "CVaR|risk|variance|tail"` = **0**，范围 = 全文 587 行）。
- (f) 折扣 $\rho$ 与终止 $\chi$ 的语义（(32) 的 $\rho(1-\chi)$）直接沿用 DQN 惯例，未见对 $\rho$ 的敏感性或对 $\chi$ 定义的分析。
- (g) 训练分布只做了一次跨星座迁移（Iridium→OneWeb，L443），**未见不同负载/不同流量强度下的训练分布比较**，也未见重训练策略对比。

**11. 可复用的具体机制**
- **对数效用单标量奖励** $U = \beta_1 \log \bar f_t - \beta_2 \log \bar d_t$、$\beta_1+\beta_2=1$（L118/L121）——把吞吐与时延的量纲差异用 log 拉平。
- **残差带宽入状态** $c_i = BW - f_i$（L276），比原始队列长度更直接反映可分配余量。
- **路径时延三分解** $\eta = \sum(q_\varepsilon + r_\varepsilon + \gamma_\varepsilon/c)$（L86），传播项用距离/光速，队列与处理项逐链路单独保留。
- **优先回放三件套**：$p_i=\delta_i+\eta$（L375）、$P(i)=p_i^\alpha/\sum p_k^\alpha$（L381）、$\omega_i=(P(i)/P_{min})^\beta$（L387）。
- **终止掩码 bootstrap 关断**：$y_i = r_i + \rho(1-\chi)[Q(\cdot)]$（L338）。
- **时间片内冻结拓扑、片前统一下发比例**（L410）——与我们时隙化实验合同的接口。

**12. 实验合同里与"负载"相关的设置（仅登记，不作贡献）**
流量强度扫描至 8 Gbps（L443/L454）；源-宿对 50、流量数据集按地面流量密度生成（L421）；Iridium 66 星（6×11）、OneWeb 648 星（18×36），$N_G=16$，倾角 90°/53°，高度 780/550 km，最小仰角 20°（Table 1，L423-425）；每个数据点 = 5 个连续拓扑快照的平均（L443）；训练参数 $N_g=24$、$L_q=100$、$\nabla_{pak}=1$KB、$N_B=32$、$B_{max}=100$、$\alpha=0.6$、$\beta$ 与 $\rho$ 表内同列 0.5（Table 2，L426-427）；NS3 仿真（L421）。

---

## XM64YRAW Inter-Satellite Routing for LEO Satellite Networks: A GNN and DRL Integrated Approach

标题原文（L5/L15）：`# Inter-Satellite Routing for LEO Satellite Networks: A GNN and DRL Integrated Approach`。全文 306 行。

**1. MDP 定义**
- **状态**：全文唯一状态定义在 L165，逐字：
> "The state vector of the MDP is obtained by concatenating the state vectors of all ISLs. The state vector of each ISL encompasses the traffic demand received by the ISL and the residual capacity of the ISL. To accommodate the operation of GNN, the concatenated vector is further augmented with multiple zero elements at specific positions to store the aggregated information from adjacent ISLs." (L165)
  逐字段：① 每条 ISL "the traffic demand received by the ISL"；② 每条 ISL "the residual capacity of the ISL"。维度 = 全网 M 条 ISL 的 2 元状态向量拼接 + 若干零填充槽位。**GNN 的节点是 ISL 而非卫星**：
> "we set ISLs as nodes in the GNN model." (L165)
  归一化：**未见**。检索 `grep -ciE "normaliz|scale|clip|standard deviation"` = **4**，命中 L37/L39/L175/L287，分别为 "unique features"、"unseen data"、"next hop"、参考文献 [4] 标题，均与状态归一化无关。
- **动作**：候选路径集合而非下一跳，L175：
> "In contrast to traditional DQNbased routing algorithms, which typically define the selection of the next hop as the action, we consider the available paths between origin and destination nodes as part of the action space, which enhances the model's global awareness. To address the challenges of large-scale satellite networks, we employ Yen's k-shortest path algorithm [13] to generate the candidate paths ... which constitute the set of actions." (L175)
  动作规模 = $k$（算法输入）：`Input: Traffic matrix F, number of shortest paths k` (L180)。
  **负向声明**：`grep -ciE "mask|invalid"` = **0** → 无动作掩码。
- **奖励**（eq 15，L170）：
$$
\mathrm { R e w a r d } = \alpha \frac { L _ { \mathrm { s t a n d a r d } } } { L _ { \mathrm { a c t i o n } } } + \beta \frac { R _ { \mathrm { a c t i o n } } } { R _ { \mathrm { s t a n d a r d } } } ,\tag{15}
$$
> "where α and $\beta$ are the respective weights for the two components. $L _ { \mathrm { a c t i o n } }$ and $L _ { \mathrm { s t a n d a r d } }$ are the delays of the selected and reference paths, respectively. $R _ { \mathrm { a c t i o n } }$ and $R _ { \mathrm { s t a n d a r d } }$ are the residual capacities of the selected and reference paths, respectively." (L173)
  两项均为"动作路径 / 参考路径"的**无量纲比值**；$\alpha,\beta$ 取值**全文未给**；奖励式本身不含 $\gamma$（$\gamma$ 只见于 Q 定义 L137 与 TD 目标 L145）。
- **转移/终止**：转移 $(s,a,r,s')$ 存回放池（L161）。**episode 终止条件正文未定义**，仅伪码一行 `13: until (the episode is done)` (L197)。
  **负向声明**：`grep -ciE "eligibility|n-step|multi-step|GAE|trace"` = **0** → 无资格迹/多步回报。

**2. 学习算法与更新式**
- 算法名 DQN（`DRL is implemented by training DQN` L142），Q 函数由 MPNN 实现。TD 目标与 MSE 损失（eq 13/14，L145/L151）：
$$
Q _ { \mathrm { t a r g e t } } = r _ { t } + \gamma \operatorname* { m a x } _ { a _ { t + 1 } } Q ( s _ { t + 1 } , a _ { t + 1 } ; \theta ^ { - } ) .\tag{13}
$$
$$
L ( \theta ) = \mathbb { E } \left[ ( Q _ { \mathrm { t a r g e t } } - Q ( s _ { t } , a _ { t } ; \theta ) ) ^ { 2 } \right] .\tag{14}
$$
  **非 double**：直接对 target net 取 $\max$（L145）。
  **负向声明**：`grep -ciE "double (q|dqn)|dueling|prioritized (experience )?replay"` = **0** → 无 double Q、无 dueling、无优先回放。
- 有 target net + 经验回放（L142）：
> "the Q-network (referred to as the Behavior Network in this paper) and the Target Network. The Behavior Network continually learns and updates, while the Target Network periodically copies the parameters of the Behavior Network to compute the target Q-values." (L142)
- **图算子 = MPNN**（eq 9/10/11，L117/L123/L129）：
$$
m _ { v } ^ { ( t + 1 ) } = \mathbb { A } \big ( \{ \mathbb { M } ( h _ { v } ^ { ( t ) } , h _ { u } ^ { ( t ) } ) | u \in B ( v ) \} \big ) ,\tag{9}
$$
$$
h _ { v } ^ { ( t + 1 ) } = \mathbb { U } ( x _ { v } ^ { ( t ) } , m _ { v } ^ { ( t + 1 ) } ) ,\tag{10}
$$
$$
\hat { y } = \mathbb { R } ( \mathbb { A } ( \{ h _ { v } ^ { ( T ) } \mid v \in V \} ) ) ,\tag{11}
$$
> "A denotes the aggregation function (with summation used for approximation in this work)" (L120)
  实现（L161）：T 次消息传递迭代中用 RNN 更新、求和聚合、readout 出 $Q(s,a;\theta)$；行为网与目标网同构（`both constructed with the MPNN architecture` L161）。**层数/宽度/激活全文未报告**。探索 $\varepsilon$-greedy（L157），但 $\varepsilon$ 数值与衰减未给（该处概率符号在 MinerU 转换中丢失）。

**3. 信用分配**
**路径级标量、一次给足、且以参考路径为基准**（L167）：
> "The reward comprises two components: one is related to the path propagation delay and the other is determined by the residual capacity. The first component assesses the performance of path selection by comparing the length of the action path to the reference path. The second part evaluates load balancing by comparing the residual capacity of the action path to that of the reference path." (L167)
**未见**逐跳即时奖励、**未见**分解到节点/链路、**未见**区分损失原因。丢包只出现在评估公式（L238），从未进入奖励。

**4. 状态里有没有时间信息**
**未见**。两个字段均为当前时隙瞬时量（L165）；网络按时隙离散、槽内拓扑视为固定：
> "We divide time into time slots. In each time slot, the network topology is regarded as fixed [8]" (L51)
检索（精确模式 + 实测计数，范围 = 全文 306 行）：`grep -ciE "ewma|history|window|trend|differ"` = **7**，命中 L27 / L35 / L39 / L250 / L268 / L271 / L273（均为散文用词如 "pivotal trend"、"different routing strategies"、"Variance of link utilization"），**无一为状态特征**。拆开计：**ewma 0 / history 0 / window 0 / trend 2**（仅 L27、L35）。另有 L161 的 `"historical messages are updated using RNN"`（该词由 `historical` 命中，不被上述模式捕获），它聚合的是**图上的迭代步**而非时间步。→ 状态无历史/趋势/差分/EWMA，也无窗口长度。

**5. 动作有没有时间结构**
**不是每包独立决策**：动作 = 给某个 $(o,d)$ 需求选一条路径，输出为路由表（`Output: Routing table composed of optimal paths for various traffic demands` L181）；伪码每轮重算候选路径与状态（`3: Based on the matrix F, calculate k available paths for each origin-destination pair using Yen's k-shortest path algorithm` L185）。
**负向声明**：`grep -ciE "switch|handover|penalt|reconfigur|reroute"` = **1**，唯一命中 **L307 参考文献 [14] 标题** `"Optical Switching and Networking"`，不构成切换代价建模 → 无动作驻留、无流级缓存/摊销、无切换代价。

**6. 多智能体设定**
**单智能体（集中式）**。状态是全网络所有 ISL 状态向量的拼接（L165），动作是对某个 $(o,d)$ 的全局路径选择（L175），伪码只有一份网络、一次选动作（`12: Select a = argmax Q(s,a;θ)` L196）。**负向声明**：`grep -ciE "multi-agent|multi agent|non-stationar"` = **0** → 未见独立 vs 集中学习对比、未见参数共享讨论、未见非平稳处理、未见智能体间通信与动作同步。

**7. 训练协议**
训练与评估共用同一套 9×12 星座与同一流量模型；评估扫 "sum required data rate"（L212），并沿轨道周期看泛化（L273）：
> "To assess the generalization ability of our solution, we evaluate the average performance over the satellite orbit period T and show the performance at time 0, 0.2T, 0.4T, 0.6T, and 0.8T." (L273)
episode 采样方式未描述（伪码仅 repeat/until，L183/L197）；**训练步数/时长/收敛判据未给**（`grep -ciE "batch size|buffer size|learning rate|discount|training step|number of episodes"` 仅命中 L140 的 "discounted by γ"）。**无显式链路/节点失效训练课程；无训练分布 ≠ 评估分布对照**。

**8. 该文的算法贡献（一句话）**
把动作空间从"下一跳"改为"Yen k-最短路生成的候选路径"（L175/L185），用 MPNN 替代 DNN 做 Q 函数近似以承载图结构与拓扑变化（L161/L165），并给出与参考路径相比的比值型双分量奖励（L170）——分别对应第 1 项动作定义、第 2 项 eq(9)-(11)、第 1/3 项 eq(15)。

**9. 该文自述的局限**
**未见自述**。`grep -ciE "limitation|future work"` 仅命中 L35，其 "limitations" 指"现有卫星网络部署受限"，非本文算法局限；结论段 L275-L277 无任何局限或未来工作陈述。

**10. 该文没有考察的算法选择（重点，均基于 1-7 实见内容）**
- (a) **奖励始终是单个路径级标量**，从未逐跳/逐链路分解（L167、L170），也从未把丢包/排队作为奖励项——丢包只出现在评估公式（L238-L247）。
- (b) **状态逐字段均为瞬时量**（L165），无任何时间聚合（第 4 项检索证据）。
- (c) **从未比较不同信用分配**：无 advantage / eligibility / n-step（`grep -ciE "eligibility|n-step|multi-step|GAE|trace"` = 0）。
- (d) **从未处理不可行动作**：`grep -ciE "mask|invalid"` = 0，而容量约束明确存在（L89 `$\lambda _ { i , j } \leq R _ { i , j } ^ { \mathrm { t o t a l } }$`）。
- (e) **未做 DQN 变体比较**：无 double / dueling / 优先回放（模式见第 2 项，计数 0）。
- (f) **未建模切换/重路由代价**（第 5 项，唯一命中为参考文献标题）。
- (g) **单智能体集中式**，未比较多智能体独立学习或参数共享（第 6 项，计数 0）。
- (h) **未比较不同训练分布**：只有一套星座与一套负载设定（L206），评估仅扫总需求速率（L212）。

**11. 可复用的具体机制**
- **比值型相对奖励**（eq 15，L170）：以参考路径为分母，两个分量都成为"优于/劣于基准"的无量纲比值；我们可把 standard 换成"当前策略/上一策略"构成自博弈基线。**这是本批最直接可搬的奖励设计。**
- **残余容量定义（可直接算）**（eq 3，L71）：
$$
R _ { p , o , d } ^ { \mathrm { r e s } } = \operatorname* { m i n } _ { ( i , j ) \in p } \left\{ R _ { i , j } ^ { \mathrm { t o t a l } } - \lambda _ { i , j } \right\} , \quad \forall p \in \mathcal { P } _ { o , d } .
$$
- **路径级动作空间 + Yen k-最短路降维**（L175/L185）：动作数从 M 降到 k。
- **MPNN 作为 Q 函数的图算子**：eq(9)(10)(11)（L117/L123/L129）+ T 次 RNN 消息更新、求和聚合、readout 出 Q（L161），可直接替换现有 MLP-Q。

**12. 实验合同里与"负载"相关的设置（仅登记，不作贡献）**
> "We evaluate the performance of our proposed approach with a satellite network consisting of 9 inclined orbits. Each inclined orbit in the LEO constellation accommodates 12 satellites with an inclination of 50 degrees, and all satellites are positioned at an altitude of 550 km. We establish 4 inter-satellite links for each satellite, with two links within the same orbit and two links between adjacent orbits. We set the capacity of all ISLs to 10 Mbps, while the traffic demands $f _ { o , d }$ fluctuate between 1.8 and 2.7 Mbps, with a packet size η of 10 Kbs." (L206)
即 108 星、每星 4 条 ISL、ISL 容量 10 Mbps、需求 $f_{o,d}\in[1.8,2.7]$ Mbps、包长 $\eta=10$ Kbs。队列时延用 M/M/1 式（eq 18，L227）；链路利用率 $\rho_{i,j}=\lambda_{i,j}/R^{total}_{i,j}$（eq 22，L265）。**注：需求上限 2.7 Mbps 对单链路 10 Mbps 容量，负载水平整体偏低。**

---

## MXQVNU3P Low Earth Orbit Satellite Network Routing Algorithm Based on Graph Neural Networks and Deep Q-Network

标题原文（L3）：`# Low Earth Orbit Satellite Network Routing Algorithm Based on Graph Neural Networks and Deep Q-Network`。全文 352 行。

**1. MDP 定义**
- **状态**：网络侧 + 用户侧拼接（L111）：
> "The network state is defined by link characteristics such as link delay, link capacity and current link utilization. These characteristics are stored in a fixed size vector filled with zero padding. At the beginning of a DRL event, a hidden feature vector representation of all nodes is generated by a graph neural network. ... And the user state (including the source node src, the destination node dst, and the traffic demand bw) is added in the current network state." (L111)
  组合式（L211）：$h ^ { \tau } = \left[ h _ { i } ^ { \tau } , s _ { d } ^ { \tau } \right]$；Algorithm 3 第 4 步 $s _ { i } \gets [ h _ { i } \| h _ { ( s , d , b w ) } ]$（L246）。
  逐字段：① 链路特征 link delay / link capacity / current link utilization（先经图重构折叠进节点）；② 用户状态 (src, dst, bw)；③ GraphSAGE 输出的节点隐向量 $h_i^\tau$。节点特征 $x _ { i } = [ q _ { i } , v _ { i } ^ { \prime } ]$：
> "where $q _ { i }$ denotes the traffic flow. $v _ { i } ^ { \prime }$ indicates the aggregated characteristics of the edges related to this node, including information such as link capacity and delay." (L97)
  归一化：仅隐表示做 L2 归一化（Algorithm 2 第 7 步，L204）；**输入状态本身未见归一化**。
- **动作**：下一跳（邻居）选择，动作数 = 邻居数 m（L117）：
> "In time period t, we define an action $a _ { t } \in A _ { . }$ , where $A = \left\{ b _ { 1 } , b _ { 2 } , \cdot \cdot \cdot , b _ { m } \right\}$ is the set of neighboring nodes of the node $u _ { i }$ The action $a _ { t }$ represents the selected neighbor node to forward the packet for the node $u _ { i }$" (L117)
  **负向声明**：`grep -ciE "mask|invalid"` = **0**；`grep -ciE "feasible"` = **1**，唯一命中 L276 的 `"find a feasible solution"`，与掩码无关 → 无动作掩码。
- **奖励**（eq 2，L124）：
$$
R = \alpha \cdot W - \beta \cdot L .\tag{2}
$$
> "where α, $\beta \in [ 0 , 1 ]$ is the adjustable weight determined by the routing policy." (L127)
  $W$ 为 rate（吞吐）、$L$ 为 delay（L121）。**另一处实现口径不同**：`The reward is set to the minimum end-to-end delay between two steps.` (L221) —— 两处口径**从未做对照实验**。
  折扣（eq 3，L132）：$R _ { \tau } = \sum _ { k = 0 } ^ { \infty } \gamma ^ { k } R _ { \tau + k }$；> "where $\gamma \in ( 0 , 1 )$ is a discount factor that weighs the historical and current reward data for the agent." (L135)
- **终止**：一次 "event" 结束 = agent 遍历完所有流量需求（L111、L221）。
  **负向声明**：`grep -ciE "eligibility|n-step|multi-step|GAE|trace"` = **0** → 无资格迹/多步回报。

**2. 学习算法与更新式**
- 声称 DQN（`DQN is executed and distributed at each node` L209），但**未给 TD 目标或 MSE 损失**；给出的两个更新式是**优势函数与策略梯度**形式（eq 9/10，L226/L232）：
$$
A ^ { \pi } ( s _ { \tau } , a _ { \tau } ) = Q ^ { \pi } ( s _ { \tau } , a _ { \tau } ) - V ^ { \pi } ( s _ { \tau } ) = R _ { \tau } - V ^ { \pi } ( s _ { \tau } )\tag{9}
$$
$$
\nabla _ { \theta } J ( \theta ) = E _ { \pi _ { \theta } } \bigg [ \sum _ { \tau = 0 } ^ { \infty } \nabla _ { \theta } \log \pi _ { \theta } ( a _ { \tau } \vert s _ { \tau } ) A ^ { \pi _ { \theta } } ( s _ { \tau } , a _ { \tau } ) \bigg ]\tag{10}
$$
  **原文口径冲突（照实记录，不融合）**：标题与 L209 称 DQN，正文却给 actor-critic 形式的 (9)(10)。
- GraphSAGE 权重更新（eq 8，L183），此处 $\gamma$ 被复用为学习率、与折扣因子符号冲突：
$$
\boldsymbol { W } ^ { t } = \boldsymbol { W } ^ { t - 1 } - \gamma \nabla _ { W } \boldsymbol { R } ( \boldsymbol { W } )\tag{8}
$$
> "where $\gamma \in ( 0 , 1 )$ is the learning rate" (L186)
- target net 仅出现在 Algorithm 3 第 10 步（L254）：`10: Reset the target action value function $\hat { Q } = Q^- ;$`。
- **图算子 = GraphSAGE**，$L=2$ 层、均值聚合、concat（eq 6/7，L167/L173）：
$$
h _ { i } ^ { 1 } = \sigma \Bigl ( W ^ { 1 } \cdot C O N C A T \Bigl ( h _ { i } ^ { 0 } , A G G R \Bigl ( h _ { j } ^ { 0 } , \forall v _ { j } \in N _ { i } \Bigr ) \Bigr ) \Bigr ) .\tag{6}
$$
$$
h _ { i } ^ { J } = \sigma \Big ( W ^ { J } \cdot C O N C A T \Big ( h _ { i } ^ { J - 1 } , A G G E \Big ( h _ { j } ^ { J - 1 } , \forall v _ { j } \in N _ { i } \Big ) \Big ) \Big )\tag{7}
$$
- DQN 侧结构（L211）：`The hidden layer of the neural network consists of a two-layer fully connected network and an activation function.`
  **负向声明**：`grep -ciE "double (q|dqn)|dueling|prioritized (experience )?replay"` = **1**，唯一命中 **L329 参考文献 [3] 标题** `"An Intelligent Routing Algorithm Based on Prioritized Replay Double DQN for MANET"`（属他人工作，非本文设定）→ 本文**无** double/dueling/优先回放。

**3. 信用分配**
**节点级即时标量**（L121、L124），执行后由环境给一次（L213）：
> "The reward function represents the different immediate rewards from different routing selections." (L121)
> "During execution progress, the node that saves the packet fixes its state and selects an action to determine the next hop node using DQN. After performing an action, the node receives a reward from its environment." (L213)
**无逐链路分解、无按损失原因（丢包/排队/传播）分项、无终局路径级奖励项。**

**4. 状态里有没有时间信息**
**未见**。状态字段全部为瞬时量（L111）；GraphSAGE 的 $T=5$ 次消息传递（L266）是**图上空间聚合**，不是时间聚合。
检索（精确模式 + 实测计数，范围 = 全文 352 行）：`grep -ciE "ewma|history|window|trend|differenti|previous state"` = **0**。**注意**：`historical` 另有 `grep -ciE "historical"` = **3** 命中，其中 L129 的 `"maximize the reward $R_{\tau}$ accumulated in the historical experience"` 与 L135 的 `"historical and current reward data"` 指的均是**累积折扣回报**，不是状态特征 → 故状态无任何时间聚合。

**5. 动作有没有时间结构**
**每包、每节点的下一跳决策**（L117）：
> "In the process of selecting the routing path, the node $u _ { i }$ with the packet needs to select a neighboring node as the next hop to forward the packet." (L117)
每时隙 $\tau$ 重新生成状态与 Q（L211）。**负向声明**：`grep -ciE "switch|handover|penalt|reconfigur|reroute"` = **3**，全部命中 L81/L83/L85，指图的 `"reconfiguration map"`（**图数据重构**），与切换/重路由代价无关 → 无动作驻留、无流级缓存/摊销、无切换代价。

**6. 多智能体设定**
**分布式执行 + 集中训练 + 参数广播（即共享参数）**（L209、L213）：
> "DQN is executed and distributed at each node, while the centralized training of DQN is implemented to improve stability." (L209)
> "During training, the centralized trainer draws a small random sample from the experience pool and updates its parameters by minimizing the loss of the DQN. After the parameters are updated, the centralized trainer sends the updated parameters to each node. Upon receiving the updated parameters, each node updates the parameters of its DQN. Then, the old experiences are deleted, and the new policy parameters are used to collect new experiences." (L213)
**负向声明**：`grep -ciE "multi-agent|multi agent|non-stationar"` = **0** → 未讨论非平稳性、智能体间通信、动作同步；从未比较"独立学习 vs 集中学习""共享参数 vs 不共享"。**未见参数广播同步频率的讨论。**

**7. 训练协议**
**训练分布 ≠ 评估分布**（明确用替代数据集训练，L259）：
> "Since the LEO networks lack of the dataset for training, we use NSFNet dataset instead of the LEO dataset in this section for training. Both LEO networks and NSFNet are hierarchical routing networks." (L259)
拓扑失效的建模（L259）：
> "Changing the connecting state of some links in NSFNet can monitor the topological changes in LEO networks. Usually the topological changes in LEO are caused by link failure and node failure, and in this paper, they can be monitored by disabling the nodes in the NSFNet, which will cause link failure and node failure." (L259)
超参（L266）：
> "In each execution of the GNN, $\mathrm { T } = 5$ message passing steps are run, and a small batch of 50 samples are used. The optimizer used for training is the Adam optimizer, which has an initial learning rate of $2 \times 1 0 ^ { - 4 }$ and follows an exponential learning rate decay during training." (L266)
**训练步数/时长未给**；收敛判据仅 `"This progress is repeated until convergence or a predefined criterion is reached."` (L213)。

**8. 该文的算法贡献（一句话）**
用 GraphSAGE 的**归纳式节点隐表示**替代固定维度状态矩阵，作为每节点 DQN 的输入，使状态维度与网络规模解耦并获得对未见拓扑的泛化；训练集中、执行分布——对应第 1 项 $h^\tau=[h_i^\tau, s_d^\tau]$（L211）与 eq(6)(7)（L167/L173）、第 6 项集中训练 + 参数广播（L209/L213）。

**9. 该文自述的局限**
**未见专门的局限/未来工作段落**（`grep -ciE "limitation|future work|further work"` 命中 L36/L42/L46/L70/L81，均为评述他人工作或动机）。但有一句自述适用性疑虑（L292）：
> "Due to the small number of nodes in the dataset used for training, it needs to be considered whether the algorithm is applicable to large networks." (L292)

**10. 该文没有考察的算法选择（重点，均基于 1-7 实见内容）**
- (a) **状态无任何时间维度**：三个字段均为瞬时量（L111），全文无 EWMA/历史/趋势/差分/上一状态（第 4 项检索证据，计数 0）。
- (b) **奖励是单一标量** $\alpha W-\beta L$（L124），从未分解到链路/跳，也从未区分损失原因；而实现口径又变成 `"minimum end-to-end delay between two steps"`（L221），**两处口径从未做对照实验**。
- (c) **动作从未处理不可达/拥塞邻居掩码**（`grep -ciE "mask|invalid"` = 0）。
- (d) **探索策略完全未交代**：`grep -ciE "epsilon|greedy|exploration|random action"` = **1**，唯一命中 L211 的执行期 `"greedy strategy"`（按 Q 值选路径），**训练期 exploration 无任何描述**。
- (e) **未比较任何 DQN 变体**（第 2 项，唯一命中为参考文献标题）。
- (f) **未使用多步回报/资格迹**（计数 0）。
- (g) **多智能体方面只用了分布式执行 + 集中训练**，从未做"独立学习 vs 集中学习""共享 vs 不共享"的对照，也未讨论非平稳性与参数广播同步频率（第 6 项，计数 0）。
- (h) **未比较训练分布**：训练固定 NSFNet（L259），评估才换拓扑/节点数（L287/L294），**从未做"训练分布不同 → 性能如何"的对照**。

**11. 可复用的具体机制**
- **边特征折叠进节点的图重构算子**（解决 GraphSAGE 只能吃节点特征的问题，L81）：
> "GraphSAGE can only deal with the network topology and the network characteristics of nodes and cannot analyze the network characteristics of links. To solve this problem, the graph structure is reconstructed by aggregating link information into nodes." (L81)
  配套三元组（eq L88/L92/L93）：$e _ { k } ^ { \prime } \gets \mathcal { D } ^ { e } ( e _ { k } , r _ { k } , s _ { k } )$；$\overline { e } _ { i } \gets \rho ( E _ { i } )$；$v _ { i } ^ { \prime } \gets \infty ^ { v } ( \bar { e } _ { i } , v _ { i } )$，节点特征 $x _ { i } = [ q _ { i } , v _ { i } ^ { \prime } ]$（L97）——**要让 GNN 处理链路状态可直接照搬**。**这是本批图算子族里最可复用的一条。**
- **归纳式嵌入 → 状态维度与网络规模解耦**：$h_i^\tau$ 由 eq(6)(7) 产生、权重矩阵跨节点共享，故可迁移到不同规模网络。
- **等变动作定义原则**（L115）：
> "actions need to be defined in a way that is invariant to the alignment of edges and nodes to exploit the ability of GNNs to generalize over graphs (i.e., only link-level features rather than specific identifiers or labels)." (L115)
- **$q$ 邻居采样 + 放回/不放回重采样**处理度数不匹配（L158 原文被 MinerU 的 `<sup>` 标签**碎片化**，仅以下片段在原文中连续）：`"a resampling method with a put-back action is"`（L158，已验证连续），其后 `used` 与前半句被标签打断，故**不作整句引文**。

**12. 实验合同里与"负载"相关的设置（仅登记，不作贡献）**
> "In order to make the weights for all links equal, the network is set to have a bandwidth capacity of 100 Mbps for each link. Traffic demand is initially distributed on each node according to precomputed routing paths, then the simulation environment is sequentially updated when training by traffic demand." (L264)
数据集为 KDN（OMNet++ 生成）中的 **NSFNet 拓扑**（L259/L264）。评估维度：不同流量需求（L276：吞吐 +29.47%/18.42%，时延 −39.76%/−15.29%）、节点失效下的拓扑变化（L287）、不同节点数（L294）。训练超参 $T=5$、batch 50、Adam、lr $2\times10^{-4}$ 指数衰减（L266）。**注：这是 NSFNet 而非 LEO 星座的负载设置，与 XM64YRAW 的 108 星 / 10 Mbps 完全不同量级。**

---

## 2FBBURX7 Graph Attention Reinforcement Learning for Multicast Routing and Age-Optimal Scheduling

标题原文（L1-2）：`Graph Attention Reinforcement Learning for Multicast Routing and Age-Optimal Scheduling`。全文 1204 行；正文至 L709 结论，L712-1046 为附录（含证明），L1052 起为参考文献。

**1. MDP 定义**
**分层双 MDP**，非单一 MDP（L355）：
> "In our case, $\mathcal { M } _ { 1 }$ is the root MDP, and $\mathcal { M } _ { 2 }$ is a sub-MDP" (L355)
- **状态（M1）** eq (14)，L246：
$$s _ { t } = \{ \mathcal { G } _ { t } , \mathbf { x } _ { t } \} , s _ { t } \in \mathbb { R } ^ { \hat { \mathcal { V } } ^ { 2 } + 6 \hat { \mathcal { V } } }$$
  $\mathcal{G}_t$ = t 时刻邻接矩阵（$\hat{\mathcal{V}}^2$ 维），$\hat { \mathcal { V } } = \operatorname* { m a x } _ { t \in \mathbb { N } _ { 0 } } | \mathcal { V } _ { t } |$（L244）。$\mathbf{x}_t\in\mathbb{R}^{6\hat{\mathcal{V}}}$ 节点特征，**Table I（L259-260）逐字段共 6 维**：One-hot encoding of node type (3) + Weighted node importance $\omega_u$ (1) + AoI of the node $A_u(t)$ (1) + Number of transmitting packets (1)。四类分量**全部是 t 时刻瞬时量**；**未见任何归一化说明**。
- **状态（M2）** eq (19)，L308：$s _ { \tau } = \{ \mathcal { P } _ { \tau } \} , s _ { \tau } \in \mathbb { R } ^ { \hat { \mathcal { V } } ^ { 2 } + \hat { \mathcal { V } } }$，即部分解；L310：
> "The state $s _ { \tau }$ includes two indicators for $\mathcal { V } _ { \tau } ^ { \mathcal { P } }$ and $\mathcal { E } _ { \tau } ^ { \mathcal { P } }$ respectively" (L310)
  注意 $\tau$ 是**虚拟构建时刻**，不是网络时刻 t。
- **动作（M1）** eq (15)，L254：$\mathcal { A } _ { 1 } = \operatorname* { P o w } ( \mathcal { U } _ { t } )$，> "It follows that the cardinality $| \mathcal { A } _ { 1 } |$ is $2 ^ { | { \mathcal { U } } _ { t } | }$" (L266)。实现降维为逐节点 Bernoulli（见第 11 项）；**M1 无显式动作掩码**。
- **动作（M2）** eq (20)，L316：$\mathcal { A } _ { 2 } = \{ v | v \in \mathcal { V } _ { t } , v \not \in \mathcal { V } _ { \tau } ^ { \mathcal { P } } , \exists u \in \mathcal { V } _ { \tau } ^ { \mathcal { P } } , ( u , v ) \in \mathcal { E } _ { t } \}$；**M2 有动作掩码**：
> "where the policy $\pi _ { 2 } ( a _ { \tau } | s _ { \tau } )$ is masked to ensure valid actions" (L500)
- **奖励（M1）** eq (16)(17)，L269/L277：
$$r _ { 1 } ( s _ { t } , a _ { t } ) = g ( \lambda , \mathcal { U } _ { t } ^ { \prime } )\tag{16}
$$
$$g ( \lambda , \mathcal { U } _ { t } ^ { \prime } ) = \operatorname* { m a x } _ { T \in \Omega ( \mathcal { U } _ { t } ^ { \prime } ) } \sum _ { u \in \mathcal { U } _ { t } ^ { \prime } } \omega _ { u } \left( 1 - \frac { h _ { T } ( u ) } { \hat { h } _ { \mathcal { G } _ { t } } } \right) A _ { u } ( t ) - \lambda ( C ( T ) - \overline { { C } } )$$
  逐项：$\omega_u\in(0,1)$ 目的地权重（L150）；$h_T(u)$ 源到 u 在树 T 上的跳数；$\hat{h}_{\mathcal{G}_t}$ 为图直径（L282）；$A_u(t)$ 瞬时 AoI；$\lambda$ 能量约束的拉格朗日乘子；$C ( \mathcal { T } _ { t } ) \triangleq \sum _ { e \in \mathcal { E } ( \mathcal { T } _ { t } ) } c _ { e }$ (eq 7, L172)。**M1 即时奖励式中无折扣 $\gamma$**；A2C 训练统一 $\gamma=0.99$（Table IV L725 / Table V L729）。
- **奖励（M2）** 势函数差分，eq (22)(23)，L330/L336：
$$q _ { 2 } ( s _ { \tau } ) = \sum _ { u \in \mathcal { U } _ { t } ^ { \prime } \cap \mathcal { V } _ { \tau } ^ { \mathcal { P } } } \omega _ { u } \left( 1 - \frac { h _ { \mathcal { P } _ { \tau } } ( u ) } { \hat { h } _ { \mathcal { G } _ { t } } } \right) A _ { u } ( t )$$
$$r _ { 2 } ( s _ { \tau } , a _ { \tau } ) = q _ { 2 } ( s _ { \tau + 1 } ) - q _ { 2 } ( s _ { \tau } ) .\tag{23}$$
  **能量项不在 $r_2$ 中**，只出现在整树目标 (17)/(25)。
- **转移/终止**：M1 的 $\mathbb{P}_1$ 未知（L267）；M2 转移确定性，eq (21) L324：$s _ { \tau + 1 } = s _ { \tau } \cup \{ a _ { \tau } , ( v _ { \tau } ^ { * } , a _ { \tau } ) \}$；终止（L310）：
> "When $a _ { t }$ is covered by $\mathcal { P } _ { \tau } , \ s _ { \tau }$ will be a terminal state and $\mathcal { P } _ { \tau }$ is the generated multicast tree" (L310)
  **无资格迹、无 n-step 回报**；多步仅体现为 Algorithm 1 的蒙特卡洛回报 $A _ { t } \gets \sum _ { k = t } ^ { T } \gamma ^ { k } r _ { k } - V _ { \omega } ( s _ { t } )$（L441）。

**2. 学习算法与更新式**
- > "Our proposed TGMS algorithm consists of two agents: a scheduler and a tree generator. Each agent is learned from the Advantage Actor-Critic (A2C) algorithm [68]." (L418)
- 价值/优势/策略梯度 eq (29)(30)(31)，L421/L427/L433：
$$v _ { \pi _ { \theta } } ( s ) = \mathbb { E } \left[ \sum _ { t = 0 } ^ { \infty } \gamma ^ { t } r ( s _ { t } , a _ { t } ) | s _ { 0 } = s \right] ,$$
$$A _ { \pi _ { \theta } } ( s _ { t } , a _ { t } ) = r ( s _ { t } , a _ { t } ) - v _ { \pi _ { \theta } } ( s _ { t } ) .$$
$$\nabla _ { \pmb { \theta } } J ( \pmb { \theta } ) = \mathbb { E } _ { s _ { t } \sim \mu _ { \pmb { \theta } } , a _ { t } \sim \pi _ { \pmb { \theta } } } \big [ A _ { \pi _ { \pmb { \theta } } } \big ( s _ { t } , a _ { t } \big ) \nabla _ { \pmb { \theta } } \log \pi _ { \pmb { \theta } } \big ( a _ { t } | s _ { t } \big ) \big ] .$$
- Algorithm 1 实际更新行（L441-L443）：
> "3: $A _ { t } \gets \sum _ { k = t } ^ { T } \gamma ^ { k } r _ { k } - V _ { \omega } ( s _ { t } ) .$" (L441)
> "4: $d \pmb { \theta } \gets d \pmb { \theta } + \nabla _ { \pmb { \theta } } ( \log \pi _ { \pmb { \theta } } ( a _ { t } | s _ { t } ) A _ { t } + H _ { \pmb { \theta } } ) .$" (L442)
> "5: $d \omega \gets d \omega + \partial ( R - V _ { \omega } ( s _ { t } ) ) ^ { 2 } / \partial \omega .$" (L443)
  即 critic 用 MSE 直接回归**蒙特卡洛回报**，actor 含熵正则 $H_\theta$。
  **负向声明**：`grep -ciE "double|target network|DQN|PPO|TRPO|SAC|DDPG|Q-learning|TD error"` 命中 L827/L847/L935/L951 与参考文献段（L1095+），**无一处是本文算法**（来源为 Assumption 2/3 与文献标题）→ **无 target network、无 double、无 TD 自举**。
- 网络结构（eq 34a-34d，L475-487）：NGAT 图嵌入层 + 全局均值池化 + 双头：
$$\mathbf { H } _ { t } ^ { ( 0 ) } = s _ { t } , \quad \mathbf { H } _ { t } ^ { ( l + 1 ) } = f _ { \mathrm { N G A T } } ( \{ \mathbf { h } _ { t , i } ^ { ( l ) } \} _ { i \in \mathcal { V } _ { t } } , \mathbf { x } _ { t } ) ,$$
$$\tilde { \mathbf { h } } _ { t } = \frac { 1 } { | \mathcal { V } | } \sum _ { i = 1 } ^ { | \mathcal { V } | } \mathbf { h } _ { t } ^ { ( L ) } , \quad \pi _ { 1 } ( a _ { t } | s _ { t } ) = \mathrm { S i g m o i d } ( \mathbf { W } _ { 1 } \sigma ( \mathbf { W } _ { 2 } \tilde { \mathbf { h } } _ { t } ) ) , \quad V _ { 1 } ( s _ { t } ) = \mathbf { W } _ { 3 } \sigma ( \mathbf { W } _ { 4 } \tilde { \mathbf { h } } _ { t } ) ,$$
  树生成头（35a-35b，L493/L497）：$\pi _ { 2 } ( a _ { \tau } | s _ { \tau } ) = \log \mathrm { s o f t m a x } ( \mathbf { W } _ { 1 } ^ { \prime } \sigma ( \mathbf { W } _ { 2 } ^ { \prime } \mathbf { H } _ { \tau } ^ { ( L ) } ) )$，$V _ { 2 } ( s _ { \tau } ) = \mathbf { W } _ { 3 } ^ { \prime } \sigma ( \mathbf { W } _ { 4 } ^ { \prime } \tilde { \mathbf { h } } _ { \tau } )$。两 agent 结构相同但**参数不共享**（W 与 W′）。超参（Table IV L725 / Table V L729）：Hidden dim 8、Attention heads 3、Accumulation Steps 32、$\gamma=0.99$、PReLU、Dropout 0.1（调度）/0.5（树生成）、AdamW、Actor LR $10^{-3}$/$10^{-2}$。
- **图算子 = 本文自创 NGAT**（27a-27c，L377-399）：
$$\phi ( \mathbf { h } _ { i } , \mathbf { h } _ { j } ) = \mathbf { a } ^ { \mathrm { T } } \mathrm { L e a k y R e L U } ( \mathbf { W } _ { 1 } \mathbf { h } _ { i } + \mathbf { W } _ { 2 } \mathbf { h } _ { j } + \mathbf { W } _ { e } \mathbf { e } _ { i , j } ) ,\tag{27a}$$
$$f _ { \mathrm { N G A T } } ( \mathbf { h } _ { i } , \mathbf { x } ) = \frac { 1 } { \| \mathbf { W } _ { 1 } \| } \big ( \alpha _ { i i } ( \mathbf { W } _ { 1 } \mathbf { h } _ { i } + \mathbf { W } _ { 3 } \mathbf { x } _ { i } ) + \sum _ { j \in \mathcal { N } _ { i } } \alpha _ { i j } ( \mathbf { W } _ { 1 } \mathbf { h } _ { j } + \mathbf { W } _ { 3 } \mathbf { x } _ { j } ) \big ).\tag{27c}$$
  **重要提示**：注意力权重式 (27b)（L381）在 MinerU 转出的 MD 中 **OCR 残损**（原文为 `$\alpha _ { i j } = \frac { \exp  \Psi  \mathbf { u } _ { l } , \mathbf { u } _ { j }  / J } { \sum _ { k \in \mathcal { N } _ { i } \cup \{ i \} } \exp ( \phi ( \mathbf { h } _ { i } , \mathbf { h } _ { k } ) ) }$`），**故不引该式为逐字原文**；对照 (26a) L377 的 GATv2 形式应为标准 softmax 注意力。压缩映射性质 eq (28) L405：$d ( f ( \mathbf { H } , \mathbf { x } ) , f ( \mathbf { H } ^ { \prime } , \mathbf { x } ) ) \leq d ( \mathbf { H } , \mathbf { H } ^ { \prime } ) .$，定理 1 要求 $\alpha_{ij}=\alpha_{ji}$（L411）。

**3. 信用分配**
- **M1 层：整槽一个标量、不分解**——$r_1 = g(\lambda,\mathcal{U}'_t)$（L269），一次动作结算一个数，不区分哪个目的地贡献。
- **M2 层：分解到"加一个节点 + 一条边"的单步**，用势函数差分（L336）；等价性 eq (25) L362 给出 $\gamma=1$ 时 telescope 回整树目标。
- **逐跳即时奖励：无。** $h_T(u)$ 是**整棵树**的跳数，不是逐跳累积；单跳成本 $c_e$ 只在最终 $C(T)$ 里以边权和出现（L172），**从未作为单步奖励项**。
- **是否区分损失原因：未见。** 精确模式 `grep -niE "credit assignment|per-hop|link-level|node-level|decompos"`（全文 1204 行）= **9** 命中，位置 **L9 / L45 / L53 / L207 / L209 / L355 / L709 / L907 / L1183**，**全部为"问题分解（decompose the problem）"语境**；其中 `credit assignment`、`per-hop`、`link-level`、`node-level` 四个词**零命中**。丢包（L132 `"the packet will be dropped when it reaches the inactive link"`）在奖励中**无任何对应惩罚项**。

**4. 状态里有没有时间信息**
**未见**，全部瞬时快照。M1 的 $\mathbf{x}_t$ 四类特征中 one-hot 与 $\omega_u$ 是静态属性、$A_u(t)$ 与 transmitting packets 是 t 时刻瞬时值（Table I L260），$\mathcal{G}_t$ 是瞬时邻接矩阵（L246）；M2 的 $s_\tau=\{\mathcal{P}_\tau\}$ 只含部分解指示（L308），且 (22) 中 $A_u(t)$ 固定在决策时刻 t、不随构建步 $\tau$ 更新。
检索（精确模式 + 实测计数，范围 = 全文 1204 行）：`grep -ciE "ewma|history|window|trend|differential|recurrent|LSTM|GRU|RNN"` = **3**，位置 **L185 / L675 / L1065**。L1065 为参考文献 [6] 标题；L675 为基线兜底（`"we force the scheduler to select an empty set if the history energy consumption exceeds the given energy constraint"`）；**L185 是问题定义层的因果策略**：
> "We consider causal policies, in which control decisions are made based on the history and current information of the network. Specifically, $\mathcal { T } _ { t }$ is determined based on $\{ \mathcal { G } _ { k } , \mathcal { T } _ { k } , A _ { u } ( k ) | 0 \leq k \leq t - 1 , u \in \mathcal { U } _ { k } \}$" (L185)
  即**允许**用历史，但 (14)+Table I 给出的**具体状态里没有任何历史项**。唯一"聚合"是 NGAT 的 L 层**空间**层数（(34a) 的 l 迭代），无 RNN/TCN。→ **状态逐字段均为瞬时量，无任何时间聚合。**

**5. 动作有没有时间结构**
- **每时隙独立决策**（Algorithm 2 每轮 t 重算 $\pi_1$、采样 $\mathcal{U}'_t$，再跑完整 $\tau$ 循环，L504-513）。
- **有"包级驻留"但无"动作驻留"**（Remark 2，L130）：
> "when a multicast tree is generated, the included routers can add the corresponding forwarding rules to their routing tables. One routing entry will not be modified until the same destination is included in a new multicast tree. This mechanism ensures the stability of packet forwarding between the generation of two multicast trees." (L130)
  即只约束**在途包**沿旧树走完，策略仍每时隙重出。
- **负向声明**：`grep -ciE "switch|dwell|handover|oscillat|chatter"` = **0** → **无切换代价**；树重建、目的地集合变动、转发规则重写均无代价项或频率惩罚。**无流级缓存/摊销、无触发式更新。**

**6. 多智能体设定**
严格说是**两层级的两个 agent，不是分布式多智能体**（L418）。集中式单控制器（L116 `"a controller can select a subset of destination nodes"`），全局共享 critic $V_1(s_t)$（L487）；**参数不共享**（$W_{1..4}$ vs $W'_{1..4}$）；**无显式通信通道**，耦合全靠环境——M1 的动作 $a_t$ 定义一个 induced MDP：
> "Given $a _ { t } ,$ an induced MDP $\mathcal { M } _ { 2 } ( a _ { t } ) = \{ S _ { 2 } , A _ { 2 } , \mathbb { P } _ { 2 } , r _ { 2 } \}$ is defined" (L306)
  M2 的整树回报又构成 M1 的奖励 $r_1$（L269）。
**负向声明**：`grep -ciE "multi-agent|decentralized|non-stationary|parameter shar"` = **1**，唯一命中 **L723**：
> "Other interesting future directions for research include exploring the consideration of multisource multicast and the decentralized implementation of the proposed algorithm via multi-agent RL." (L723)
  → 去中心化 MARL 是**未来工作**，本文未做；**无动作同步机制**（Alg 3 先取 scheduler transition 存 $B_s$ L547、再跑完 M2 循环存 $B_t$ L556；tree generator 每 t 更新 L565、scheduler episode 末更新 L570）。

**7. 训练协议**
- **训练分布 ≠ 评估分布（刻意泛化测试）**：Algorithm 3 第 2 行 `2: Sample a graph $\mathcal { G } \sim D .$`（L544）；> "We only train the model on the I080 dataset for the algorithms that need to be trained. The remaining datasets are only used for testing." (L667)（AS-733 / ER / BA 只做测试）。
- episode 采样：一个 episode = 一张采样图 + t 从 0 跑到 T（L543-546），每个 t 内嵌一次 $\tau$ 循环。
- **无拓扑漂移或负载渐变的训练课程**；测试每图 50 时隙（L669），能量预算 $\bar{C}\in\{1,\dots,20\}$ 逐个扫（L687）。**未给训练步数/时长/episode 数**；收敛判据仅 `while not converged`（L543）。
- **$\lambda$（对偶变量）更新**：Init 0.05、Training Interval 100、LR $1e-5$（Table VI L733-735）；Alg 3 第 16 行 `Store the extra energy cost`（L560）、第 20 行 `Update the Lagrangian multiplier`（L562）；> "The Lagrangian multiplier λ is updated at each time slot to ensure that the energy cost is within the budget" (L529)。**联合训练**：
> "The training process is performed end-to-end, where the scheduler and tree generator are jointly optimized." (L529)
- 训练稳定性特设：动态 $\varepsilon$-greedy（36-39，L536/L571-583）与选择性反向传播（L588-596）。

**8. 该文的算法贡献（一句话）**
把联合"调度 + 组播树"的长期 AoI 问题先用拉格朗日对偶拆成调度子问题与树生成子问题，再把树生成写成"从源出发逐节点加边"的序列决策，并用**只对已覆盖目的地结算、可增量计算的质量函数**做**势差奖励**使终局目标变成逐构建步的稠密信号——对应第 1 项的状态/动作重定义（(14)(19)(20)）、第 3 项的势函数信用分配（(22)(23)）、第 2 项的 NGAT 算子（(27c)）。

**9. 该文自述的局限**
> "The proposed TGMS algorithm has a few limitations. First, it requires high memory for training on a large graph. This can be mitigated by using a distributed training framework. Second, the multicast tree may not be able to update in realtime due to the complexity of the graph. The real update frequency depends on the SDN devices used." (L701)
> "A limitation of our algorithm is that the scheduler needs to be retrained if the energy constraint changes. This motivates potential future research directions, such as designing a metalearning framework to optimize the scheduler. This can be achieved by training the scheduler on multiple graphs with different energy constraints." (L723)
训练稳定性自述（L531）：
> "due to the action masking of the tree generator, the tree generator may converge to a local minimum, and the gradient may explode" (L531)

**10. 该文没有考察的算法选择（重点，均基于 1-7 实见内容）**
- (a) **奖励从未分解到节点或链路，也从未区分损失原因**：M1 是整槽标量（L269），M2 是势差标量（L336），能量项只能是整树边权和（L172）；依据 = 第 3 项的精确模式实测 9 命中且全为"问题分解"语境。
- (b) **状态逐字段均为瞬时量，无任何时间聚合**，也**从未比较"有历史 vs 无历史"**（第 4 项，实测 3 命中均非状态特征）。
- (c) **从未比较不同训练分布**：训练图只有 I080（L667），无 curriculum / domain randomization / 多分布混合训练的对照。
- (d) **从未给动作加切换代价或驻留约束**（第 5 项，精确模式 0 命中）。
- (e) **未使用 target network / double / replay / TD 自举**（第 2 项），故**从未比较自举式 critic 与蒙特卡洛 critic**。
- (f) **未考察多智能体/去中心化的任何机制或实验**（第 6 项，唯一命中 L723 属未来工作）。
- (g) **未对两层 agent 的更新顺序/频率做消融**（固定为 tree generator 每 t 更新、scheduler episode 末更新，L565/L570）。
- (h) **未考察 $\lambda$ 的其他更新方式**：只有一套超参（L733-735）与 episode 级对偶更新（L560-562）；与固定 $\lambda$、多 $\lambda$ 条件化策略的比较被明确推到未来工作（L723）。

**11. 可复用的具体机制**
- **(a) 势函数差分奖励（终局目标 → 逐跳稠密信号）**（(22)(23)，L330/L336）：
$$q _ { 2 } ( s _ { \tau } ) = \sum _ { u \in \mathcal { U } _ { t } ^ { \prime } \cap \mathcal { V } _ { \tau } ^ { \mathcal { P } } } \omega _ { u } \left( 1 - \frac { h _ { \mathcal { P } _ { \tau } } ( u ) } { \hat { h } _ { \mathcal { G } _ { t } } } \right) A _ { u } ( t ) , \quad r _ { 2 } ( s _ { \tau } , a _ { \tau } ) = q _ { 2 } ( s _ { \tau + 1 } ) - q _ { 2 } ( s _ { \tau } ) .$$
  条件：势函数可**增量**计算（只依赖已加入节点）。**这是本批最贴近"逐跳信用分配"的可复用机制。**
- **(b) 跳数/直径归一化的延迟折扣因子** $(1 - h_T(u)/\hat{h}_{\mathcal{G}_t})$（L277/L330）：把路径长度惩罚与 AoI 权重耦合进同一标量且天然落在 $[0,1)$，代价是每张图要算一次全对最短路径直径（L282）。
- **(c) NGAT 的"除以权重范数"归一化**（(27c)，L399）：自环项与邻居项共用 $W_1$ 并整体除以 $\|W_1\|$，再用三角不等式换出压缩映射 $d(f(\mathbf{H},\mathbf{x}),f(\mathbf{H}',\mathbf{x}))\leq d(\mathbf{H},\mathbf{H}')$（证明 (48)，L818-822）——要论证嵌入层稳定性可直接复制。
- **(d) 动作空间降维两件套**：调度侧"大集合动作 → 逐元素独立 Bernoulli"（L467 `"we predict a Bernoulli distribution for each node"` + (34c) L483）；树生成侧"只允许部分解邻居"的 mask（L316/L500）。把 $2^n$ 幂集动作压成 n 个伯努利。
- **(e) 基于策略熵的动态 $\varepsilon$-greedy**（37-39，L571-583）。**注意方向问题**：按 (39)，熵最大时 $\varepsilon\to\varepsilon_{min}$，与 L535/L585 的文字描述相反——**搬用前必须核对**。
- **(f) 选择性反向传播**（L588-596）：$\varepsilon$-greedy 随机抽到的动作、以及概率高于阈值的动作都不触发反传，用于缓解 mask 引起的梯度爆炸；对应 transition 仍保留（L592）。

**12. 实验合同里与"负载"相关的设置（仅登记，不作贡献）**
拓扑与规模：调度实验统一 $|V|=80$（L667）；四类拓扑 I080（SteinLib）、AS-733（真实 AS 拓扑，L643）、ER 随机图（L645）、BA 图（L663）。目的地集合：> "For those datasets that do not contain the terminal nodes, we randomly select 10% of nodes as destinations. The source node is randomly selected from the remaining nodes." (L667)。链路代价 > "We randomly assign the costs of edges from $\{ 1 , 2 , \ldots , 1 0 \}$ ." (L667)。能量/负载约束扫描 $\bar{C}\in\{1,2,\ldots,20\}$（L687），"low-energy scenarios" 指 $\bar{C}<5$。每图测试 50 时隙（L669）。训练/测试分离见第 7 项。STP 侧 SteinLib I080/I160/I320/I640，> "Each dataset has 100 instances." (L605)，80 训练 / 20 测试。基线：调度侧 Random（L671）与 Greedy（L673），两者超限时强制选空集（L675）。硬件：PyGraph 2.4.0，RTX 4090 训练（L741）。
**关键登记**：**负载模型本身在正文中不存在**——generate-at-will（L106/L88），Assumption 1 一跳 = 一个时隙（L110-112），> "If multiple packets arrive at a destination node simultaneously, only the packet with the smallest AoI is considered." (L114)，链路失效则包被丢弃（L132）。故"负载"在此文仅体现为能量预算 $\bar{C}$ 与目的地抽样比例，**无到达过程、无队列、无缓存模型**。

---

## GPDPLJNG Multi-Commodity Flow Routing for Large-Scale LEO Satellite Networks Using Deep Reinforcement Learning

标题原文（L1）：`Multi-Commodity Flow Routing for Large-Scale LEO Satellite Networks Using Deep Reinforcement Learning`。全文 304 行。

**1. MDP 定义**
- **状态** $s _ { t } \in S = \{ P _ { t } , Q _ { t } \}$（L184）：
> "• States: State $s _ { t } ~ \in ~ S ~ = ~ \{ P _ { t } , Q _ { t } \}$ represents the current information in the satellite network. The set $P _ { t } = \{ ( l _ { t } ^ { i } , p _ { t } ^ { i } ) , i = 1 , 2 , \cdots , | V | \}$ indicates the condition of all the nodes in the satellite network, where $l _ { t } ^ { i }$ is satellite $i \mathrm { \ ' } _ { \mathrm { s } }$ location at timeslot t and $p _ { t } ^ { i }$ is the available storage of satellite i at timeslot t. The set $Q _ { t } \ = \ \{ ( l _ { t } ^ { k _ { i , \delta } } , w ^ { k _ { i , \delta } } ) , i \ = 1 , 2 , \cdots , N , \delta \in \{ 1 , 2 , \cdots , t \} \}$ specifies all the location and size of the requests at timeslot t..." (L184)
  逐字段：$l_t^i$（卫星位置，连续量，**原文未给维度与归一化**）；$p_t^i$（卫星可用缓存，标量，**未归一化**）；$l_t^{k_{i,\delta}}$（请求所在卫星，离散索引）；$w^{k_{i,\delta}}$（请求大小，标量；实验固定 100 MB，L277）。注意 $Q_t$ 的下标是 $\delta \in \{1,\cdots,t\}$——**状态里挂着全部历史注入且尚未完成的请求**，这是全篇唯一带"过去"的分量，由请求队列本身承载，**不是显式时间聚合**。
  存储量演化写在状态转移里（eq 15，L207）：$p _ { t + 1 } ^ { u } = p _ { t } ^ { u } + \sum _ { k _ { i , \delta } \in u _ { o u t } } w ^ { i , \delta } - \sum _ { k _ { i , \delta } \in u _ { i n } } w ^ { i , \delta } , \forall t , u$。
- **动作**：**联合动作**（L186）：
> "• Actions: Each action $a _ { t } ~ = ~ \{ a _ { t } ^ { k _ { i , \delta } } , i ~ = ~ 1 , 2 , \cdot \cdot \cdot N , \delta ~ \in \{ 1 , 2 , \cdots , t \} \}$ indicates that the agent should determine the next-hop for all users' requests, where $a _ { t } ^ { k _ { i , \delta } } \in \{ u , n b _ { u } \}$ with $u = l _ { t } ^ { k _ { i , \delta } }$ specifying that the request $k _ { i , \delta }$ stays at the same satellite u at timeslot t or be forwarded to one of the neighbor satellites in set $n b _ { u }$ at next timeslot." (L186)
  即每个请求一个 $1+|nb_u|$ 元子动作（含"留在原地"），整体是 $(N\times M)$ 个子动作的集合；输出层切成 $(N\times M)$ 组、每组 $|V|$ 个 Q 值（L214）。eq (16) L217：$a _ { t } = \{ \mathbf { a } _ { \mathbf { t } } ^ { \mathbf { k } _ { 1 , \delta } } , \mathbf { a } _ { \mathbf { t } } ^ { \mathbf { k } _ { 2 , \delta } } , \cdot \cdot \cdot , \mathbf { a } _ { \mathbf { t } } ^ { \mathbf { k } _ { \mathbf { N } , \delta } } \}$。
  **有动作掩码**（L202，三条规则见第 11 项）。
- **奖励**（eq 14，L191）：
$$R ( s _ { t } , a _ { t } ) = \sum _ { i } ^ { N } \sum _ { \delta \in \{ 1 , 2 , \cdots , t \} } D ^ { k _ { i , \delta } } ( s _ { t } , a _ { t } ^ { k _ { i , \delta } } ) ,\tag{14}$$
  $D^{k_{i,\delta}}$ 是分段式奖励（原文标 (13a)-(13h)，位于 L141-L177），关键档逐字：等待档 $1/\tau-\beta$（L155-157）；到达档 $( \frac { c } { \triangle _ { u , v } ( t ) } + \frac { r _ { u , v } } { w ^ { i , \delta } ( t ) } ) + \Gamma$（(13d)，L161）；越走越远档 $( \frac { c } { \triangle _ { u , v } ( t ) } + \frac { r _ { u , v } } { w ^ { i , \delta } ( t ) } ) - 2 \beta$（(13h)，L177）。系数含义（L188 段正文）：$1/\tau$ 基础等待奖励；$\beta$ 驻留/方向奖励；$\Gamma>2\beta$ 到达目的地的终局加成；$-2\beta$ 越走越远惩罚。**奖励非归一化**（延迟倒数与常数 $\beta$ 混量纲）。$\gamma=0.99$ 只在超参处给出（L277），奖励式本身不含 $\gamma$。
- **转移/终止**：**无丢包假设使转移确定化**（L204）：
> "the channels between the two satellites are assumed to be no-loss, which means the request will be forwarded successfully from satellite u to one of its neighbors during each timeslot. In addition, the request will not remain on the link at next timeslot." (L204)
  Episode 终止（Alg 1 第 17-18 行，L254-256）：`17: if all the requests arrive at their destination or $t = = O b r T$ then / 18: break`。
  **使用 n-step 回报、无资格迹**：$R _ { t } ^ { ( n ) } = \sum _ { k = 0 } ^ { n - 1 } \gamma _ { t } ^ { ( k ) } R _ { t + k + 1 }$（L228）；**原文未给 $n$ 的具体取值**。

**2. 学习算法与更新式**
- 自述：`"a multi-Deep Q-network (DQN) based RL method, extending the technique of multi-step learning"`（L29），方法名 DRL-SR。
- 损失（eq 17，L225）：
$$\left( R _ { t } ^ { \left( n \right) } + \gamma _ { t } ^ { \left( n \right) } \operatorname* { m a x } _ { a ^ { \prime } } { Q _ { G } \left( s _ { t + n } , a ^ { \prime } ; \theta _ { G } \right) } - Q \left( s _ { t } , a _ { t } ; \theta \right) \right) ^ { 2 } ,\tag{17}$$
- **有 target network，非 double**：target 用 $\max_{a'}$ 而非 double 分解（L225）；target 更新为**硬替换**：`25: update the target network : $\theta _ { G } \gets \theta$`（L263）。
  **负向声明**：replay 采样为 `"sample random minibatch of experience from $\Psi ^ { ( n ) }$"`（L259）→ **无优先经验回放**；损失式用 $\max_{a'}$ → **非 double**。
- 网络结构（L277 逐字）：
> "In the neural network structure, three residual blocks with the number of channels per layer are constructed as [64], [64, 64], [128, 128], respectively, and two linear fully connected layers as one hidden layer and one output layer in the end. The number of neurons in the hidden layer is 128. We apply ReLU as an activation function and -greedy policy to make the agent explore the environment and exploit the collected data." (L277)
  即 3 个残差块（通道 [64] / [64,64] / [128,128]）+ 两个全连接层（隐藏 128、输出 $|V|$），激活 ReLU。
  **负向声明**：`grep -ciE "graph neural|GNN|GCN|convolution"` = **0** → **无图算子**（单智能体、无参数共享问题）。

**3. 信用分配**
**逐请求、逐时隙的即时奖励 + 一个到达终局加成**，按"动作档位"而非按损失原因分解；奖励是所有在网请求即时项求和（eq 14，L191）。关键在 Alg 1 第 15-16 行——把每条请求拆成独立 transition：
> "15: select an action set $a _ { t }$ via -greedy method, receive each request's reward individually $r _ { t } ^ { k _ { i , \delta } , j }$ , receive reward $r \gets R ( s _ { t } , a _ { t } )$ by calculating (14), and set $s _ { t } \gets s _ { t + 1 }$" (L248-251)
> "16: store transition $\left( s _ { t } , a _ { t } ^ { k _ { i } , \delta , j } , r _ { t } ^ { k _ { i } , \delta , j } , s _ { t + 1 } \right)$ in $\Psi ^ { ( n ) }$ and Ψ for $i  1 , N$ and $j  1 , M$" (L252-253)
故**信用分配粒度 = (请求 × 时隙)**。**不区分损失原因**：L204 明确假设 no-loss，无排队溢出惩罚；(13a)-(13h) 的分档依据只有"与目的地的距离比较"与"是否到达"（L163）。**路径级终局奖励只有 $\Gamma$ 一项**（(13d) L161），其余全是逐跳即时项。

**4. 状态里有没有时间信息**
**未见显式时间信息，只有"未完成请求集合"构成的隐式队列记忆。** 检索（精确模式 + 实测计数，范围 = 全文 304 行）：`grep -ciE 'ewma|history|window|trend|differential|momentum|memory|recurrent|LSTM|GRU'` = **0**。$l_t^i$ 与 $p_t^i$ 均为时隙 t 瞬时快照（L184）；$p_{t+1}^u$ 的递推（L207）是**环境的物理演化**，不是喂给网络的差分/趋势特征——网络输入仍是 $s_t$ 而非 $s_{t+1}-s_t$。唯一跨时隙的量是 $\delta\in\{1,\cdots,t\}$ 的请求索引集合（L184）。

**5. 动作有没有时间结构**
**每时隙对全部在网请求重新决策一次**（Alg 1 第 13 行 `for $t \gets 1 , O b r T$ do`，L246）；**无动作驻留缓存、无流级摊销、无触发式更新**。"留在原地"是**显式动作**（L186 的 $a_t^{k_{i,\delta}}=u$），故驻留是学出来的而非硬编码。驻留有显式代价：$1/\tau$ 等待项与 $\pm\beta$ 方向项（L141-177）；链路断开重连也有代价，见延迟模型第三项（eq 10，L105）：
$$D _ { u , v } ^ { s _ { i , \delta } , d _ { i , \delta } } ( t ) = \left\{ \begin{array} { l l } { 0 , \quad \mathrm { i f } u = d _ { i , \delta } , } \\ { \alpha _ { t , u , v } ^ { s _ { i , \delta } , d _ { i , \delta } } \left( \frac { \Delta _ { u , v } \ ( t ) } { c } + \frac { w ^ { i , \delta } } { r _ { u , v } } \right) + \beta _ { t , u } ^ { s _ { i , \delta } , d _ { i , \delta } } \tau , \quad \mathrm { o t h e r w i s e } , } \end{array} \right.\tag{10}$$
> "as the connection between node u and the next hop satellite v fails, reconnection time is needed, which can be expressed as the third term" (L105 段)
在网请求数上限由约束 (6) 给出（L79）。

**6. 多智能体设定**
**单智能体、集中式**：
> "Assume that an agent acts as a controller in the satellite launch company to solve the multi-commodity flow routing problem" (L182)
> "The satellite operation center as an agent will determine the next-hop for all the considered $( N \times M )$ requests in the LEO satellite network, which is a contemporaneous multiaction mechanism." (L214)
**负向声明**：`grep -ciE "multi-agent"` = **1**，唯一命中 **L23**，且为**引述他人工作** [8]（`"Rolla et al. [8] utilized the multi-agent reinforcement learning approach..."`），非本文设定 → **无参数共享问题、无通信、无非平稳处理、无动作同步**；只有一个决策体，输出层一次吐 $(N\times M)$ 组动作（L214）。

**7. 训练协议**
超参（L277）：30 星 / 6 轨道面 / 每面 5 颗；每星 buffer 1 GB；星间传输率 5.625 Gbps；链路容量同样 5.625 Gbps（perfect channel）；每请求 100 MB；Adam LR $\alpha=0.001$；$\gamma=0.99$；> "The observation time for each episode is 250 seconds. The duration of each timeslot is 5 seconds." (L277)
Episode 采样：Alg 1 第 12 行 `set up an environment and reset it`（L245），每 episode 重置后跑至全部请求送达或 $t=ObrT$（L254）。**未报告总 episode 数、minibatch 大小、replay 容量、$n$ 的具体取值**（Alg 1 中仅作符号定义，L233-239）。**训练分布与评估分布未作区分**：只报 latency vs 卫星数 / vs 用户数（L275/L279），无 held-out 拓扑或负载的泛化划分。

**8. 该文的算法贡献（一句话）**
把单智能体 DQN 的输出层扩成 $(N\times M)$ 组、每组 $|V|$ 个 Q 值，从而在**同一时隙内一次性输出所有在网请求的下一跳**（L214/L217），并配一套三规则动作掩码（L202）与把 n-step 回报接进该联合动作的损失（eq 17，L225）。原文自述 `"our modified DQN method considers multiple actions in the output layer for single-agent DRL"`（L31）。

**9. 该文自述的局限**
**未见自述。** 检索：`grep -niE "limitation|future work|we do not|not consider|drawback|shortcom"`（全文 304 行）= **1**，唯一命中 **L126**，语境为约束函数枚举（`"...limitation of one action per request and requests occupation..."`），**非自述局限**；结论节（L283）只有结果复述，**无任何 future work 段落**。

**10. 该文没有考察的算法选择（重点，均基于 1-7 实见内容）**
- (a) **从未使用图算子**：`grep -ciE "graph neural|GNN|GCN|convolution"` = **0**（L277 网络是残差块+全连接），而状态本身是图结构（$G^t=(V,E^t)$，L43）。
- (b) **从未做时间聚合**：第 4 项精确模式 **0 命中**；状态逐字段（L184）全是瞬时量。
- (c) **从未分解损失原因**：奖励只有 (13a)-(13h) 八档（L141-177），分档依据是"与目的地距离比较"与"是否到达"（L163/L188）；**无丢包、排队溢出、链路中断的独立惩罚项**，且 L204 明确假设 no-loss。
- (d) **从未比较多智能体**（第 6 项，唯一命中为引述他人工作）。
- (e) **从未用 Double DQN 或优先回放**（第 2 项）：损失用 $\max_{a'}$ 而非 double 分解（L225）；replay 为 `"sample random minibatch"`（L259）。
- (f) **从未扫描 $n$（多步步数）**：$R_t^{(n)}$ 定义在 L228，全文无 $n$ 取值。
- (g) **从未做动作掩码消融**：三条规则在 L202 一次性给出，无"有掩码 vs 无掩码"对照。
- (h) **从未区分训练/评估分布**（第 7 项）。

**11. 可复用的具体机制**
- **(a) 联合多动作输出层**（L214/L217）：把网络输出 reshape 成 $(N\times M)\times|V|$，每个请求一组 logits，$|V|$ 覆盖全部卫星、掩码掉非法项——**可直接搬到我们的多流并发路由头**。
- **(b) 三规则动作掩码**（L202 逐字）：
> "Here, the masking schemes to eliminate the infeasible requests forwarding and enhance the agent's training speed are introduced. Firstly, the storage of the satellites reaching full capacity is not allowed to accommodate coming requests. Then, links with empty available bandwidth are not allowed to be used. Furthermore, the size of requests greater than the assigned satellites or links is masked." (L202)
- **(c) 驻留=显式动作 + 驻留代价**：$a _ { t } ^ { k _ { i , \delta } } \in \{ u , n b _ { u } \}$（L186），驻留奖励 $1/\tau$ 与方向奖励 $\pm\beta$（L141-177），重连再加 $\beta\tau$（eq 10，L105）——给了"等待/绕行"统一量纲的定价。
- **(d) 按请求拆 transition**（L248-253）：同一联合动作下每条请求存一条 $(s_t,a_t^k,r_t^k,s_{t+1})$，用共享网络做 per-request TD，避免某条请求的贡献被总奖励平均掉。
- **(e) n-step 损失的写法**（eq 17，L225）：target 用 $Q_G(s_{t+n},\cdot)$，可与我们现有 TD 目标直接对接。

**12. 实验合同里与"负载"相关的设置（仅登记，不作贡献）**
每星 buffer 1 GB；星间传输率与链路容量均 5.625 Gbps（perfect channel）（L277）。每请求固定 100 MB（L277）。每用户同时在网请求上限 M（约束 6，L79）；N 用户随机注入——`"each user's request is generated and infused into the network randomly"`（L43）。每 episode 观测 250 s、时隙 5 s（L277）。评估轴：latency vs 卫星数（L275）；latency vs 用户数，12 与 18 星拓扑（L279）。基线：最短路径法（L279）。

---

## GPLEP83L LLM-Driven Automated Reward Design for Reinforcement Learning-Based Routing in LEO Satellite Networks

标题原文（L1）：`LLM-Driven Automated Reward Design for Reinforcement Learning-Based Routing in LEO Satellite Networks`。全文 174 行。

**1. MDP 定义**
- **状态：原文没有定义状态向量的任何字段。** 全文只有抽象三元组（L29）：
> "Consider an agent operating in a Markov decision process (MDP) defined by $\overset { \cdot } { M } \ = \ ( \overset { \cdot } { S } , \overset { \cdot } { A } , \mathcal { P } )$ where $s$ is the state space, $\mathcal { A }$ is the action space, and $\mathcal { P }$ is the transition function." (L29)
  检索：`grep -ciE "observation space|state vector|state representation|input dimension"`（全文 174 行）= **0** → **无法逐字段列出状态**；只能推知含"部分网络信息"（L69 `"based on partial network information"`）与队列相关量。**维度、是否归一化、是否随时间聚合——原文均未给出。**
- **动作**（L69）：
> "the routing problem consists of deciding, at each satellite, the next hop to which a packet should be forwarded among the currently available neighboring nodes" (L69)
  即下一跳选择，动作集 = 当前可用邻居集合（"currently available" 暗示存在可用性过滤，但**未描述任何掩码实现**）；**动作空间大小未给**。
- **奖励**：**本文不写奖励公式，奖励由 LLM 生成的可执行代码给出**。只给奖励设计的优化目标式（eq 1，L34）：
$$r ^ { * } = \arg \operatorname* { m a x } _ { r \in \mathcal { R } } F ( \mathcal { T } _ { M } ( r ) )\tag{1}$$
> "where each $r \in \mathcal { R }$ maps states and actions to scalar values guiding the learning process. A RL algorithm operating on M is denoted by $\mathcal { T } _ { M } ( r )$ , which takes a reward function r as input and produces a policy $\pi \in \Pi$ . The fitness function $F : \Pi \xrightarrow { } \mathbb { R }$ evaluates the quality of a learned policy π." (L29)
  **奖励是标量**（L29 逐字 `"maps states and actions to scalar values"`）。**全文没有一条奖励公式、没有系数、没有归一化说明**；`grep -ciE "discount|gamma"` = **0** → **折扣因子完全未报告**。
- **转移/终止**：$\mathcal{P}$ 未展开（L29）；**episode 定义、终止条件、是否多步回报——全文未提**。

**2. 学习算法与更新式**
- 算法名 **DDQN**（L69）：
> "The agents are trained using a Double Deep Q-Network (DDQN) algorithm, which is used in all experiments. Since the focus of this work is on reward optimization, we primarily analyze the behavior of the agents during the training phase." (L69)
  **更新式、TD 目标、损失函数、target net 更新周期一律未给出**（`grep -niE "loss|TD target|bellman|update rule"` 只命中 L57 的 "training loss" 作为指标名与 L75）。
- 网络结构未给，因为超参一律继承模拟器默认（L73）：
> "The hyperparameters of the DDQN agent are kept fixed across all experiments and set to the default values provided by the simulator [18], ensuring that only the reward function varies." (L73)
  **负向声明**：`grep -ciE "convolution|GNN|graph neural|LSTM|attention"` = **1**，唯一命中 **L137 参考文献 [1] 标题** → **本文网络无图算子自述**。是否 double / 是否有 target net 可从算法名推知，但**实现细节原文零描述**。

**3. 信用分配**
**逐跳（hop-level）即时奖励，且规模被明确点数化**（L75）：
> "Each candidate reward function generated by LARGE is evaluated by training the DDQN agent for 0.2 seconds, producing approximately 70,000 hop-level reward events and 35,000 training steps." (L75)
即信用分配单位 = **一次转发跳**（不是流、不是 episode）。奖励内部按"被选中的下一跳 vs 当前可用邻居集合"做**局部排序**（L110）：
> "Rather than evaluating only the selected hop in isolation, it compares the chosen action against the set of currently available neighboring satellites and assigns reward components based on local ranking criteria." (L110)
四项具体分解（L112 逐字）：
> "First, it includes local ranking terms that favor neighbors with higher data rate and better progress-time efficiency. Second, it modifies the queue component by relating the observed queueing delay to the best available service time, making the penalty depend on the relative quality of the selected hop rather than only on the absolute queueing time. Third, it adds an explicit hop cost, discouraging unnecessarily long routes. Finally, it strengthens loop avoidance by penalizing repeated visits and ping-pong behavior, using satellite identifiers to detect revisits more robustly." (L112)
Table II（L121）给出基线 vs 生成奖励的八项结构对照。惩罚按"事件类型"给（L110 列出 `"fixed penalties or bonuses for special events such as delivery, unavailable links, and loop formation"`），因此**部分区分了损失原因**——回路、不可用链路、无效动作各有独立惩罚项。

**4. 状态里有没有时间信息**
**原文未定义状态，因而无法确认；就写出来的内容看，无任何显式时间聚合。** 检索（精确模式 + 实测计数，范围 = 全文 174 行）：`grep -ciE "ewma|history|window|trend|differential|momentum|memory|recurrent"` = **7**，位置 **L23 / L75 / L89 / L91 / L104 / L118 / L137**，命中词**全部是 `window`（"training window" / "search window" / "evaluation window"）或 `memory`（L23 综述语境）**，**无一处是状态的历史/趋势/差分/EWMA 项**。奖励用的是 `"the observed queueing delay"` 与 `"the best available service time"` 两个**当下量**（L112），其比较是**同一时刻的空间比较**（选中跳 vs 最佳可用邻居），**不是时间比较**。

**5. 动作有没有时间结构**
**每包独立决策、无动作驻留、无流级缓存**：L69 `"deciding, at each satellite, the next hop to which a packet should be forwarded"`——决策对象是单个 packet。**切换是否有代价：未见自述**（`grep -iE 'handover|switch|trigger|hysteresis'` 无本文设定命中）；不过生成奖励含 `"progress-time efficiency"` 与 `"ping-pong penalties"`（L112/L121），后者**等价于对"来回切换"施加代价**，但这是 LLM 生成的结果、**不是论文指定的机制**。**无触发式更新**：训练/推理都以固定时间窗推进（L75：0.2 s / 1 s / 12 s）。

**6. 多智能体设定**
**独立学习（independent learners）**，无集中式 critic、无参数共享、无通信、无非平稳处理（L69）：
> "The RL framework follows a multi-agent setting, where each satellite acts as an independent agent responsible for making local routing decisions based on partial network information. The learning process includes two phases: during the online phase, agents learn from interactions with the environment through exploration, while during the offline phase, pre-trained models are deployed for decision making." (L69)
**负向声明**：`grep -ciE "centraliz|decentraliz|parameter shar|communicat|message passing|non-stationar"` = **0**（无本文设定命中；命中项均为参考文献标题，如 L161/L163）→ **无动作同步机制**，在线/离线两阶段是唯一结构性描述。

**7. 训练协议**
**训练分布与评估分布是同一套固定星座**（L73）：
> "The proposed framework is evaluated on the Kepler constellation, which consists of 140 satellites distributed across seven orbital planes at an altitude of 600 km. We use a fixed constellation to isolate the effect of reward optimization from changes in orbital topology, link dynamics, and path-length distributions." (L73)
三阶段协议（L75）：search 相位每候选奖励训 0.2 s（≈70,000 hop-level 奖励事件、35,000 训练步）；training 相位从头训满 1 s，每 0.2 s 记 checkpoint；inference 相位无学习部署 12 s（卫星位置随时间更新）。停止准则（L75）：
> "The LARGE search loop terminates once a candidate reward function achieves a goodput higher than that of the baseline reward" (L75)
> "To account for the stochastic nature of the training process, all results are reported as mean ± standard deviation over 10 independent runs with different random seeds." (L75)
**负载/拓扑不变化**：星座固定（L73），负载未作为变量（L129 自述留作 future work）。**未报告训练步数总量、batch 大小、回放容量。**

**8. 该文的算法贡献（一句话）**
把**奖励函数本身当成优化变量**、用"LLM 生成奖励代码 + 模拟器反馈"的外层闭环迭代求解（eq 1，L34），内层用三个 LLM 角色（Metrics Interpreter / Reward Design / Code Generator，L41）做"变量可得性校验"，从而**在不改 DDQN 超参与状态/动作定义的前提下（L73）替换奖励结构**。

**9. 该文自述的局限**
> "Although this work focuses on a controlled Kepler constellation scenario to isolate reward optimization, future work will extend the evaluation to additional constellation architectures, traffic loads, gateway deployments, and longer inference horizons. Further directions include robust multiobjective stopping criteria, prompt sensitivity analysis, and fine-tuned LLMs to improve convergence speed and reward quality." (L129)
另有与泛化直接相关的一句（L114）：
> "the inference results also show that a more expressive reward does not necessarily lead to uniformly better generalization." (L114)

**10. 该文没有考察的算法选择（重点，均基于 1-7 实见内容）**
- (a) **状态定义从头到尾缺席**（L29 抽象三元组；精确模式 0 命中）→"状态该不该含队列历史/趋势"这个选择**从未被摆上台面**。
- (b) **折扣因子与全部 DDQN 超参被冻结、从未作为变量**：L73 逐字超参固定，且 `grep -ciE "discount|gamma"` = **0**，**连 $\gamma$ 取值都未报告**。
- (c) **奖励始终是标量、从未做多目标/向量奖励**（L29）——goodput / path stretch / delay 三者被压进一个标量再靠权重调和；L129 把 multiobjective 推到未来工作。
- (d) **从未做逐项奖励消融**：Table II（L121）只做"基线 vs 生成"的结构对照，无"去掉 hop cost / 去掉 ping-pong penalty"的分项去除实验。
- (e) **多智能体设定被固定为"每星独立智能体"**（L69），从未比较集中式 critic、参数共享或通信。
- (f) **动作空间设计从未被改动**（L69 固定为下一跳），未见模式级动作、比例路由或显式动作掩码的比较。
- (g) **从未考察训练/评估分布偏移**（同一固定 Kepler 星座，L73）。
- (h) **搜索窗口长度这一超参从未被消融**：固定 0.2 s（L75/L89），论文只说它 `"keeps the LLM-in-the-loop reward search computationally feasible"`（L75），**没有比较过更长窗口对最终奖励选择的影响**。

**11. 可复用的具体机制**
- **(a) "奖励代码变量可得性"内层校验环**（L48）：
> "If a variable is not available for implementation in Python, the Code Generator Agent returns the definition along with a report listing the missing variables and requests a revised version." (L48)
  这一环**逼着奖励设计从环境真实可观测的量出发**，而不是生成一个跑不起来的公式。
- **(b) 外层闭环的反馈内容**（L57）：
> "it converts the metrics obtained at the end of training into a structured prompt that highlights areas for improvement, reinforces the optimization objective, and indicates whether the reward function improved or degraded compared to the previous run" (L57)
- **(c) 奖励结构的四种可搬设计**（L112）：局部邻居排序项、相对服务时间队列惩罚、显式 per-hop 代价、基于卫星 ID 的重复访问+乒乓惩罚——这是"**逐跳即时奖励也能做局部比较**"的具体做法，与本批其他论文的标量奖励形成对照。
- **(d) 短窗搜索 + 长窗复核的双相位协议**（L75）：0.2 s 搜索选奖励 → 1 s 从头重训验证 → 12 s 无学习推理，**用于防止奖励过拟合到短搜索窗口**；可原样搬作我们的奖励/超参筛选协议。

**12. 实验合同里与"负载"相关的设置（仅登记，不作贡献）**
流量模型：地面网关把邻近用户流量聚成 $B=64{,}800$ bits 的同目的地块注入星座（L67）。星座：Kepler，140 星 / 7 轨道面 / 600 km，固定（L73）。指标：path stretch、goodput (Mbps)、end-to-end delay (ms)（L81-85）。推理相位实测（Table I，L102）：Baseline 1451.62±131.67 Mbps / 85.65±2.44 ms / 1.464±0.066；LARGE-GPT 1324.03±237.34 / 88.41±2.32 / 1.569±0.088；LARGE-Opus 1409.56±133.10 / 85.13±3.03 / 1.486±0.034。搜索相位步数：每候选奖励 0.2 s ≈ 70,000 hop-level 奖励事件、35,000 训练步（L75）。10 个随机种子取 mean±std（L75）。基线奖励：模拟器 [18] 自带的专家设计奖励（L73）。

---

## 6GWNYSTT LEO laser microwave hybrid inter-satellite routing strategy based on modified Q-routing algorithm

标题原文（L5）：`LEO laser microwave hybrid inter‑satellite routing strategy based on modified Q‑routing algorithm`。全文 384 行。
**短名说明**：这是本批唯一**表格式 RL（tabular Q-routing）**，不是深度 RL——全篇无神经网络、无状态向量、无奖励函数；"状态"退化成 Q 表下标，"奖励"退化成延迟代价，"折扣"退化成 $\gamma=1$。

**1. MDP 定义**
- **状态：没有状态向量，只有 Q 表索引。** 原文只定义 Q 值下标（eq 12，L195）：
$$Q _ { u _ { i } } \big ( u _ { N _ { P } } , u _ { i + 1 } \big )\tag{12}$$
> "This value represents the estimated cost for the satellite to send the packet from the neighbor satellite $u _ { i + 1 } \tan u _ { N _ { P } } .$" (L198)
  即状态 ≈ (目的卫星 $u_{N_P}$, 候选邻居 $u_{i+1}$)，**不存在特征向量、维度、归一化这些概念**。检索：`grep -niE 'state|observ|feature|input'` 命中全部为 `"Link State aware"` 类语义（L42/L343）与 `"monitor the satellite status"`（L46），**无任何状态向量定义**。
  **"下一跳队列长度"与"路径长度"都不进入状态，而是被压进即时代价**（L29）：
> "According to the next hop queue length and path length continuously iterating in real time, the reinforcement learning algorithm Q-routing can obtain the shortest delay path in dynamic networks." (L29)
  队列长度 → 经排队论变成处理延迟 $W_S$（式 4-6，L99/L105/L115），再进 (13)；路径长度 → 经逐跳传输延迟 $T_l = d_{AS}/c$（式 3，L87）每跳叠加。**无显式队列长度特征、无剩余跳数特征、无拥塞等级特征。**
- **动作：选下一个邻居，纯贪心 argmin**（L200）：
> "The satellite $u _ { i }$ sends the packet to the neighbor with the lowest Q-value" (L200)
  动作空间 = 邻居集合。**负向声明**：`grep -ciE "mask"` = **0** → 无动作掩码；可行性靠路径级硬约束 (8)-(10) 事后施加（L162-183）。
- **奖励：本文没有奖励函数。** **负向声明**：`grep -ciE "reward"` = **0**（范围 = 全文 384 行）。Q 值直接以**时延**为代价（"最短时延函数"），目标项（式 11 的目标部分，L183）：
$$\sum _ { i = 1 } ^ { N _ { \oplus } - 1 } T _ { l } ( u _ { i } , u _ { i + 1 } ) + \sum _ { i = 1 } ^ { N _ { \oplus } } W _ { S } ( u _ { i } )$$
  **重要提示**：式 (11) 在 L183 处的 MinerU Markdown 转换**排版噪声严重**（含重复嵌套的 \sum 与乱码下标），**无法逐字还原完整 LaTeX**，故此处只抄其中可确认的目标项，**其余字符以 L183 原文为准**。
  **负向声明**：`grep -ciE "discount"` = **0**、`grep -ciE "gamma"` = **0** → 式 (13) 迭代形式上等价于 $\gamma=1$；**无终端奖励、无失败惩罚**。
- **转移/终止**：拓扑被切片离散成静态图（L158）：
> "The academic method to cope with this dynamic characteristic is called "topology slicing," which slices the continuously changing topology into n discrete topologies with little change between neighboring slices... Above all, the topology used for routing calculations is static." (L158)
  故**切片内转移静态**，**不存在 episode/终止概念**；**负向声明**：`grep -ciE "n-step|multi-step|eligibility|trace"` = **0** → 无资格迹/多步回报（更新是单步 bootstrapping）。

**2. 学习算法与更新式**
- 算法名 `"a modified Q-routing algorithm [27]"`（L190，[27] 即 Boyan & Littman 的 Q-routing）；`"this algorithm uses Dijkstra algorithms to accelerate the convergence"`（L190）。
- **核心更新式逐字抄录**（(13)，L202-204）：
$$\begin{array} { r l r } {  { \mathbf { N e w } Q _ { u _ { i } } ( u _ { N _ { p } } , u _ { i + 1 } ) } } \\ & { = ( 1 - \alpha ) Q _ { u _ { i } } ( u _ { N _ { p } } , u _ { i + 1 } ) } \\ & { } & { + \alpha ( T _ { l } ( u _ { i } , u _ { i + 1 } ) + W _ { S } ( u _ { i } ) + \operatorname* { m i n } _ { u _ { i + 2 } \in \mathrm { n e i g h b o r s ~ o f ~ } u _ { i + 1 } } Q _ { u _ { i + 1 } } ( u _ { N _ { p } } , u _ { i + 2 } ) ) } \end{array}\tag{13}$$
  逐项含义（L200）：
> "the neighbor satellite $u _ { i + 1 }$ immediately reports its minimum sending cost $Q _ { u _ { i + 1 } } \left( u _ { N _ { P } } , u _ { i + 1 } \right)$ , path delay $T _ { l } \big ( u _ { N _ { P } } , u _ { i + 1 } \big )$ , receive delay $W _ { S 1 } ( u _ { i + 1 } )$ to the satellite $u _ { i } ,$ then $u _ { i }$ iterates over these value." (L200)
  **原文内部不一致（照实登记，复现时必须二选一）**：L200 说上报的是**邻居**的接收延迟 $W _ { S 1 } ( u _ { i + 1 } )$，而式 (13) 用的是**当前节点**的处理延迟 $W _ { S } ( u _ { i } )$。
  该更新 = **一步 bootstrap 的 Q-learning（TD(0)）**，$\alpha$ 直接乘在 TD 误差上，$\gamma$ 隐含为 1。
- **无神经网络**：**负向声明** `grep -ciE "neural"` = **1**，且该唯一命中处**无任何层数/宽度/激活描述** → 表格法，**无 target net、无 replay、无 double**。
- Dijkstra 的作用是**预热初值 + 给出方向**（L206、L208）：
> "Since the transmission delay is constant for each topology, Dijkstra algorithm can provide an approximate direction to the destination." (L206)
> "paths find by Dijkstra algorithm only use transmission delay, so they can be pre-calculated before the arrival of packets and do not take up the routing delay" (L208)
  复杂度（L210、Table 1）：Dijkstra 全网空间 $O(N^2)$ / 时间 $O(N^3)$；Q-routing 全网空间 $O(NAH)$ / 时间 $O(NKH)$。

**3. 信用分配**
**逐包、逐跳即时代价，并按"延迟成因"做了三段分解**——这是本文唯一的信用分配结构（eq 7，L148）：
$$W _ { S } = W _ { S 1 } + W _ { S 2 } + W _ { S 3 }\tag{7}$$
> "a satellite includes three queuing models and generates three processing delay: $W _ { S 1 }$ when reception, ${ \cal W } _ { S 2 }$ when on-board processing, and ${ \mathbb Y } _ { S 3 }$ when transmission." (L146)
> "Laser receivers follow $M / M / 1 / N / \infty ,$ and microwave receivers follow $M / M / 1 / { \infty } / { \infty }$" (L139)
  即处理延迟拆成**接收（光电转换）/ 在轨处理（CPU 资源池）/ 发送（电光转换）**三段，**"延迟来自哪个环节"可直接读到**。
**路径级终局奖励：无。** **是否区分损失原因：部分**——延迟成因可分，但丢包/不可达**无独立惩罚项**；**负向声明** `grep -ciE "packet loss"` = **1**，唯一命中 L27 为泛述（`"lead to new packet loss rate and processing delay"`），非惩罚项；且 (8)-(10) 是**硬约束而非软惩罚**。

**4. 状态里有没有时间信息**
**特征层面没有；价值层面有——本文用"运行平均"代替状态记忆。** **负向声明**：`grep -ciE "ewma|history|window|trend|differential|momentum|memory|recurrent"` = **0**（范围 = 全文 384 行）。依据：
- 特征层面：无状态向量（第 1 项），无任何历史/趋势/差分项。
- 价值层面：式 (13) 的 $(1-\alpha)Q+\alpha(\cdot)$ **就是对历史代价估计的指数滑动平均，有效窗口由 $\alpha$ 控制**（$\alpha\in\{1,0.8,0.5\}$，L269）——全篇唯一的时间聚合机制，且作用于**代价估计**而非状态输入。
- 拓扑时间：由 topology slicing 处理（L158），切片内静态，路由表只在切片边界重算（L210 `"this calculation happens only one time in each time slice"`）。

**5. 动作有没有时间结构**
**每包独立决策、无动作驻留、无流级缓存**（L160）：
> "The packet enters the starting satellite from the ground, passes through starting receiver, through the CPU resource pool, through the transmitter, and then reaches the next satellite. The packet repeats these steps until reaches destination satellite, which then transmits it to the aiming ground station." (L160)
**切换代价：无显式项**（Q 值里只有 $T_l + W_S$，式 13）。**触发式更新：部分有**——邻居收到包后 `"immediately reports"` 其最小代价（L200），更新由**包到达事件**驱动而非定时轮询。

**6. 多智能体设定**
**完全去中心化的独立学习（每星一个 Q 表），无参数共享、无集中式 critic、无通信协商协议**（L29）：
> "The algorithm also has the advantages of decentralized computation, small space cost, and short single iteration time." (L29)
每星维护自己的 Q 表（L210 `"each satellite have a Q-table of size Num(d) ∗ Num y"`），靠邻居的**局部标量上报**更新（L200）：通信**有**，但是最轻量的三点标量（$Q_{\min}$、$T_l$、$W_{S1}$），**报文本篇未量化**。
**负向声明**：`grep -niE "non-stationar|multi-agent"` 全文 384 行**无本文设定命中** → **非平稳处理未见自述**；**动作同步：无**——每包独立走自己的路。

**7. 训练协议**
**没有训练/评估划分——全部结果是同一批在线仿真的收敛曲线**（L221-269）。路由 200 万包，每批 20,000 包，随机起讫，$18\times40$ 网络（L221）；对比 Dijkstra / Q-routing / modified Q-routing 三算法（L217）；轨道 1200 km / 18 面 / 每面 40 颗 / 倾角 87.9°（Table 2，L228）。收敛判据 = 延迟收敛（约 20 ms）：
> "the delay converges to the minimum for all batches when the number of network iteration rounds near 30" (L242)
**学习率取值**：$\alpha=1,0.8,0.5$（L269）：
> "As presented in the picture, with large learning rates, the network takes 20 to 40 batches to converge; the smaller the learning rate, the slower the convergence rate." (L261)
负载与拓扑在仿真中同时变化（批次 2000–10,000+，L242；拓扑 $5\times5$ 到 $25\times25$，L248），但**无 held-out 评估分布**。

**8. 该文的算法贡献（一句话）**
把 Q-routing 的即时代价从"队列延迟"换成"**逐跳传输延迟 + 三段式排队处理延迟**"（式 13 的 $T_l + W_S$，L203；$W_S$ 由式 7 给出，L148），并用 Dijkstra 预计算路由表做初值/方向引导加速收敛（L206/L208）——对应第 1 项代价定义与第 2 项 eq(13)。

**9. 该文自述的局限**
**未见自述。** **负向声明**：`grep -niE "limitation|future work|not consider|drawback|shortcom"` = **0**（范围 = 全文 384 行）；第 6 节 Results and discussion（L271）只复述结果，无局限段。最接近的只有一句复杂度权衡：`"Therefore for diferent system configurations, diferent algorithms are available."`（L210 末）。

**10. 该文没有考察的算法选择（重点，均基于 1-7 实见内容）**
- (a) **从未使用函数逼近**：`grep -ciE "neural"` = 1 且无网络描述；Q 为表格（L195）。**从未比较线性/神经网络逼近**——而 $O(NAH)$ 空间复杂度正是表格法的直接后果（L210）。
- (b) **从未做时间聚合**：`grep -ciE "ewma|history|window|trend|differential|momentum|memory|recurrent"` = 0；唯一时间效应是式 (13) 的 $\alpha$ 平滑（L203），且作用于价值而非状态。
- (c) **从未讨论折扣因子**：`discount` = 0、`gamma` = 0；式 (13) 等价 $\gamma=1$。
- (d) **从未使用探索机制**：`grep -ciE "epsilon"` = **0**；L200 固定为纯贪心，**从未比较 ε-greedy / softmax / 乐观初始化**。
- (e) **从未设计状态特征**：全文无状态向量，"状态该含什么（下一跳队列长度？历史拥塞？链路质量？）"这一整类选择**根本不在讨论范围**。
- (f) **从未有奖励函数，因而无从讨论奖励塑形**：`reward` = 0；信用分配 = 延迟三段分解，无终端奖励、无失败惩罚、**无多目标加权**。
- (g) **从未使用动作掩码/可行性屏蔽**：`mask` = 0；可行性靠 (8)-(10) 路径级硬约束事后处理。
- (h) **多智能体只做了"独立 Q 表 + 邻居标量上报"**（L200/L210）；**从未比较参数共享、集中式学习、通信频率或非平稳处理**。
- (i) **从未做训练/评估分布划分**：全部结果是同一在线过程的收敛曲线（L221-269）。

**11. 可复用的具体机制**
- **(a) "预计算静态路由表 + 在线 Q 学习"的双层结构**（L206/L208）：Dijkstra 用只含传输延迟的静态代价预热并约束搜索方向，Q 学习只补偿动态排队/处理延迟。对我们等于"**拓扑快照给骨架、RL 只学拥塞残差**"。
- **(b) 三段式处理延迟分解**（式 7，L148）：接收 / 在轨处理 / 发送分别用 $M/M/1/N$、$M/M/c$、$M/M/1$ 建模（L139/L141/L143），使"延迟来自哪个环节"可直接读到；配套排队式（eq 4/5/6，L99/L105/L115）：
$$W _ { s } = { \frac { 1 } { \mu - \lambda } }\tag{4} \qquad W _ { s } = \frac { L _ { s } } { \mu ( 1 - P _ { 0 } ) }\tag{5} \qquad W _ { S } = \frac { L _ { S } } { \lambda }\tag{6}$$
  其中 $L _ { s } = \frac { \rho } { 1 - \rho } - \frac { ( N + 1 ) \rho ^ { N + 1 } } { 1 - \rho ^ { N + 1 } } , P _ { 0 } = \frac { 1 - \rho } { 1 - \rho ^ { N + 1 } } , \rho = \frac { \lambda } { c \mu }$（L109）。
- **(c) 邻居上报的最小信息接口**（L200）：只传三个标量（$Q_{\min}$、$T_l$、$W_{S1}$）——可作我们 DRL 方案里"状态通信"的最小带宽版本。
- **(d) 事件触发的价值更新**（L200 `"immediately reports"`）：更新由包到达驱动而非时钟驱动，天然适配稀疏流量。
- **(e) 学习率作为唯一稳定-速度旋钮**（L269）：
> "Note that in the same network, the smaller the learning rate α, the smaller the convergence delay, indicating a large learning rate in a small network makes trafic slow." (L269)

**12. 实验合同里与"负载"相关的设置（仅登记，不作贡献）**
每包到达服从泊松分布（L137），各接收机到达率 $\lambda_{1j}$ / 离去率 $\mu_{1j}$，$j\in\{1,\dots,5\}$（L139）；资源池总到达率 $\lambda_2=\sum_{i=1}^{5}\lambda_{1i}$（L141），CPU 单元平均处理速度 $\mu_2$（L141）。每星 5 个收发信机：2 路激光（同轨）+ 3 路微波（异轨与地面）（L128）；CPU 资源池 5 个计算单元，占满后新包进缓存（L132）。单星总处理延迟 $W_S=W_{S1}+W_{S2}+W_{S3}$（式 7，L148）。路径约束：$\sum T_l\le T_{l_{\max}}$（式 8，L164）、$\sum W_S\le W_{S_{max}}$（式 9，L168）、总延迟 $\le T_{max}$（式 10，L172）。负载扫描：每批 2000–20,000 包（L221 说每批 20,000 包、共 200 万包；L242 报告 `"each batch of 2000 to 10,000 packets"`）；`"As the load increases, the convergence delay also increases"`（L242）。拓扑扫描：$5\times5$ / $10\times10$ / $15\times15$ / $20\times20$ / $25\times25$（L248）与 $18\times40$（L221）。轨道参数：1200 km / 18 面 / 每面 40 颗 / 倾角 87.9°（Table 2，L228）。复杂度对照表（Table 3，L236）；收敛延迟约 20 ms（L242）。

---

# 本批小结（Batch 3：风险/奖励设计/图算子/多径族）

## 一、本批共同采用的算法范式

1. **价值型/actor-critic 的"标准件拼装"占绝对主导**，且几乎都是**把已有 RL 算法接到路由 MDP 上**，而非新算法：DQN（XM64YRAW L142、MXQVNU3P L209、GPDPLJNG L29）、Double DQN（GPLEP83L L69）、DQN+优先回放（9C6HB6AF L412/L375-L387）、SAC 的 primal-dual 扩展（39NJWBI7 L226）、A2C（2FBBURX7 L418）；**唯一的非深度 RL 是 6GWNYSTT 的表格式 Q-routing**（L190/L195）。
2. **决策粒度集中在"下一跳"或"路径/比例"两档**：下一跳（MXQVNU3P L117、GPLEP83L L69、6GWNYSTT L200、GPDPLJNG L186）；候选路径（XM64YRAW L175）；每路径流量比例（9C6HB6AF L292）；组播树逐节点加边（2FBBURX7 L316）。
3. **图算子是本批的主题轴**，但披露质量差异极大：MPNN（XM64YRAW eq 9-11）、GraphSAGE（MXQVNU3P eq 6-7）、自创 NGAT（2FBBURX7 eq 27c）；**9C6HB6AF 声称 GNN 却未披露任何结构**（唯一句 L412）。
4. **多智能体绝大多数是"参数共享的独立学习"或"单智能体集中式"**：独立+共享（39NJWBI7 L176、GPLEP83L L69）、分布式执行+集中训练+参数广播（MXQVNU3P L209/L213）、单智能体集中式（9C6HB6AF L410、XM64YRAW、GPDPLJNG L214、2FBBURX7 L418）。

## 二、本批共同没考察什么

1. **状态里没有任何时间聚合——8/8 全批为零**（精确模式 `ewma|history|window|trend|differential|momentum|memory|recurrent`，逐篇实测：39NJWBI7 0 / 9C6HB6AF 0（作状态特征）/ XM64YRAW 0 / MXQVNU3P 0 / 2FBBURX7 0（作状态特征）/ GPDPLJNG 0 / 6GWNYSTT 0；GPLEP83L 的 7 命中全为 "training/search window"）。**唯一的时间聚合出现在价值层而非状态层**：6GWNYSTT 式 (13) 的 $(1-\alpha)Q+\alpha(\cdot)$ 指数滑动平均（L203）。
2. **奖励几乎全是标量、且大多不分解到链路/节点**：39NJWBI7 (35)(36) 是逐跳标量+结局分叉；XM64YRAW (15)、MXQVNU3P (2)、9C6HB6AF (26)、GPDPLJNG (14)、GPLEP83L 均为单一标量；**只有 2FBBURX7 做了严格的逐构建步分解**（势差 (23)）。**全批没有一篇把奖励分解到链路级并做消融**。
3. **动作掩码基本缺席**：仅 GPDPLJNG（三规则掩码 L202）与 2FBBURX7 的 M2（L500）有掩码；其余 6 篇 `mask` 命中 0。
4. **几乎没有论文做过"训练分布 ≠ 评估分布"的系统对照**：只有 MXQVNU3P（NSFNet 训练、LEO 评估，L259）与 2FBBURX7（I080 训练、AS-733/ER/BA 测试，L667）存在分布差异，但**都没有把"训练分布如何影响性能"当作实验变量**；其余 6 篇训练与评估同分布。
5. **全批只有 1 篇处理风险/尾部**（39NJWBI7 的 CVaR）；**只有 1 篇做多目标**（9C6HB6AF 的对数效用 (6)，但仍压成标量）；**没有任何一篇做奖励的分项消融**。
6. **切换/重路由代价几乎全批缺席**（2FBBURX7 精确模式 `switch|dwell|handover|oscillat|chatter` = 0；其余篇亦无显式切换惩罚项），只有 2FBBURX7 用"在途包沿旧树走完"的包级复用（L130）间接收敛了稳定性。

## 三、本批最接近"可直接复用机制"的 3 条（含公式）

**① 把尾部风险做成约束而不是奖励项——39NJWBI7（本批唯一，且是最有价值的一条）**
逐跳归一化 cost 化 $c _ { h } = D _ { h } ^ { Q } / D _ { n o r m }$（L397，$D_{norm}=100$ ms），再用 IQN 分布 critic + CVaR 近似把约束落到 actor 与乘子上：
$$\Gamma _ { \epsilon _ { k } } ( o , a ) \approx \frac { 1 } { N ^ { k } } \sum _ { m = 1 } ^ { N ^ { k } } Q _ { \psi _ { k } } ^ { c } ( o , a , \zeta _ { m } ) .\tag{32}$$
$$\mathcal { L } _ { \lambda _ { k } } = \underset { o \sim \mathcal { D } } { \mathbb { E } } \left[ \lambda _ { k } \left( \pi _ { \theta } ^ { \top } ( o ) Q _ { \psi _ { k } } ^ { c } ( o ) - D _ { k } \right) \right] ,\tag{27}$$
**搬用价值**：可在**不动奖励函数**的前提下单独加一条"队列时延 CVaR"约束通道，风险水平 $\varepsilon_k$ 与阈值 $D_k$ 是两个可扫超参——这正是本批其他 7 篇都没做的维度。

**② 势函数差分奖励：把路径级目标转成逐跳稠密信号——2FBBURX7**
$$q _ { 2 } ( s _ { \tau } ) = \sum _ { u \in \mathcal { U } _ { t } ^ { \prime } \cap \mathcal { V } _ { \tau } ^ { \mathcal { P } } } \omega _ { u } \left( 1 - \frac { h _ { \mathcal { P } _ { \tau } } ( u ) } { \hat { h } _ { \mathcal { G } _ { t } } } \right) A _ { u } ( t ) , \qquad r _ { 2 } ( s _ { \tau } , a _ { \tau } ) = q _ { 2 } ( s _ { \tau + 1 } ) - q _ { 2 } ( s _ { \tau } ) .\tag{22,23}$$
原文给出等价性（eq 25，L362）：$\gamma=1$ 时 $\sum_\tau r_2$ 精确 telescope 回整树目标。**搬用价值**：本批唯一"**终局目标 ≡ 逐跳奖励之和**"的严谨构造；只要能把评估目标写成"当前已覆盖/已推进集合的势函数"且**可增量计算**，就能同时拿到稠密信用分配与无偏目标，且跳数用图直径 $\hat{h}_{\mathcal{G}_t}$ 归一化后天然落在 $[0,1)$。

**③ 比值型相对奖励：把"优于基准"直接写进奖励——XM64YRAW**
$$\mathrm { R e w a r d } = \alpha \frac { L _ { \mathrm { s t a n d a r d } } } { L _ { \mathrm { a c t i o n } } } + \beta \frac { R _ { \mathrm { a c t i o n } } } { R _ { \mathrm { s t a n d a r d } } } ,\tag{15}$$
配套残余容量（eq 3，L71）：$R _ { p , o , d } ^ { \mathrm { r e s } } = \operatorname* { m i n } _ { ( i , j ) \in p } \left\{ R _ { i , j } ^ { \mathrm { t o t a l } } - \lambda _ { i , j } \right\}$。
**搬用价值**：两个分量都是无量纲比值、以参考路径为分母，**跨拓扑/负载尺度天然可比**，避免"延迟倒数与常数混量纲"的问题；把 standard 换成"当前策略/上一策略"即可构成自博弈基线。**配套可搬**：MXQVNU3P 的"边特征折叠进节点的图重构"（L81/L88-L93/L97）与等变动作定义原则（L115）。

---

# 核验记录

**核验方法**：所有逐字引文（含公式行）用归一化子串比对脚本对 VM 上 MD 原文回核，归一化 = 转小写 + 非字母数字字符折叠为单空格 + 压缩连续空格。脚本在 VM 侧执行（base64 传入后 python3），对每篇全文建缓存后逐条匹配，并额外校验行号锚点（引文须落在所标行号 ±8 行窗口内）。本批共回核 **约 150 条**引文/公式。

**已修正的问题（原稿 → 修正后）**：
1. **39NJWBI7 L164**：初稿引文 "a snapshot of the network's physical status and packet-specific information at the h-th hop" 与原文不符（原文为 "$s_h$ is a snapshot of the network's physical status and **packetspecific** information"，MinerU 把 "packet-specific" 连写成 "packetspecific"）。→ 改为逐字原文。
2. **39NJWBI7 L145**：初稿把约束 (C4) 写成了转述式。→ 改为逐字 LaTeX 原文 $D _ { p } ^ { Q } = \sum _ { h , ( i , j ) } x _ { p , i j } ^ { h } \cdot D _ { i j } ^ { Q } ( \tau _ { p } ^ { h } ) \leq D _ { m a x } ^ { Q } , \quad \forall p \in \mathcal { P }$（L145）+ L148 原句。
3. **39NJWBI7 行锚**："每包独立决策（L158）"→ 实际该句在 **L176**，已改。
4. **39NJWBI7 CVaR 式**：初稿 tag 留空且省略了 $\psi_k^c$ 下标 → 补全为原文 tag{32} 逐字形式。
5. **负向声明的模式收紧（主控核验反馈，全批通用）**：初稿使用裸模式 `double|dueling|priorit`，在 39NJWBI7 有 1 处误命中（L403 `"to prioritize successful packet delivery"`），**模式与计数不符事实**。→ 全批负向声明一律改为**精确模式 + 实测计数 + 命中位置**：
   - `double (q|dqn)` / `dueling` / `prioritized (experience )?replay`（39NJWBI7 = 0/0/0；9C6HB6AF = 0/0/—；XM64YRAW = 0/0/0；MXQVNU3P = 1 命中 L329 **参考文献标题**；GPDPLJNG 非 double + 无优先回放；6GWNYSTT 无网络/无 replay）
   - `per` 单词边界模式（39NJWBI7 = 6，命中 L23/L264/L354/L379/L393/L397，**全为 "per-action/per-sample/per-hop/per run" 散文**，不构成优先回放反例）
   - `mask`（39NJWBI7=0、9C6HB6AF=0、XM64YRAW=0、MXQVNU3P=0、6GWNYSTT=0；仅 GPDPLJNG L202 与 2FBBURX7 L500 有掩码）
   - `softmax|normaliz|project`（9C6HB6AF = 2，命中 L482/L484 的 CRediT 投稿声明 `"Project administration"`/`"Fund Project"`；softmax 与 normaliz 各 0）
   - `CVaR|risk|variance|tail`（9C6HB6AF = 0）
6. **MXQVNU3P L158 整句引文**：子代理给出的 "If the number of neighbors of a particular node is less than q, a resampling method with a put-back action is used." 在 MD 原文中**被 MinerU 的 sup 标签碎片化打断**（该行被两遍重复文本与上标标记交错穿插），**归一化后无法整句匹配**。→ 本稿**撤回整句引文**，只保留可验证的连续片段 `"a resampling method with a put-back action is"`（已单独验证连续），并注明碎片化原因。
7. **2FBBURX7 两处措辞**：子代理的 "In our case, M1 is the root MDP, and M2 is a sub-MDP"（L355）与 "will be a terminal state and"（L310）经归一化匹配失败——原文中 $\mathcal{M}_1$ 等符号混在句中。→ 本稿按**可验证的连续子串**引用，并保留行号。
8. **2FBBURX7 decompos 命中数**：子代理报 6，**实测 9**（L9/L45/L53/L207/L209/L355/L709/L907/L1183）。→ 按实测 9 记录，结论（全为"问题分解"语境）不变。
9. **2FBBURX7 式 (27b)**：注意力权重式在 MD 中 **OCR 残损**（含 \Psi 与乱码分母）→ **不引为逐字原文**，仅保留可确认的 (27a)/(27c)，并注明残损。
10. **6GWNYSTT 式 (11)**：L183 处 Markdown 转换**排版噪声严重**（重复嵌套求和符号与乱码下标）→ **不整式引用**，只抄可确认的目标项并指向 L183 原文。
11. **6GWNYSTT 原文内部不一致**：L200 说邻居上报 $W_{S1}(u_{i+1})$，式 (13) 用当前节点 $W_S(u_i)$。→ **照实登记，不做融合**，并标注"复现时必须二选一"。
12. **9C6HB6AF 原文内部矛盾**：L266 称 PPO，L478/L480 称 DQN，更新式 (32)-(39) 却是 DQN+PER。→ 照实并列，不融合。
13. **MXQVNU3P 原文口径冲突**：L117/L209 动作 = 邻居下一跳，L211 却称输出 "multiple candidate paths"。→ 照实并列。
14. **GPDPLJNG 局限检索**：子代理称 limitation 仅命中 L126；实测该模式全文命中 **1** 处，确为 L126，但语境是约束枚举（`"...limitation of one action per request..."`）→ "未见自述局限"成立，已注明命中原文。

**访问受限说明**：本会话角色（deepener）**无权限读取**同批次的一篇姊妹锚点稿（ANCHOR-DISSECT-*），首次访问被 HOOK-BLOCK（理由：角色 deepener 不允许访问 shell-file）。按协议等待 20 秒重试后**仍被拦**，故**本稿未参考该锚点稿的体例**，格式完全依 `EXTRACTION-TEMPLATE.md`。`EXTRACTION-TEMPLATE.md` 首次访问亦被 HOOK-BLOCK，等待 20 秒重试后**成功读取**。

**覆盖度**：本批 8 篇 **全部完成 12 项拆解**（39NJWBI7、9C6HB6AF、XM64YRAW、MXQVNU3P、2FBBURX7、GPDPLJNG、GPLEP83L、6GWNYSTT）。全部论文全文分块读完（543 / 587 / 306 / 352 / 1204 / 304 / 174 / 384 行），文献读取阶段均无 HOOK-BLOCK 阻断。



