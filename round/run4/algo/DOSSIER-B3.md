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
**未见**。L164 明写 snapshot；L170 只列 packet state 与 local node/neighbor statistics。检索：`grep -n -iE 'ewma|history|window|trend'` 覆盖全文 543 行 → ewma 0 命中、history 0 命中、window 0 命中、trend 仅命中 L472（参考文献标题）。→ 无历史/差分/EWMA 任何形式。唯一时间量 $	au$（动作时延）只进奖励 (35)，不进状态。

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
- **有目标网络**（Algorithm 2 输入含 target network，L343）；**无 double**（未提）。
- 网络结构：正文**未给**任何层数/宽度/激活/节点特征（`grep -n -iE 'gnn|graph|hidden|layer|activation|embed'` 命中均为泛泛表述）；唯一架构句 L412：
> "we adopt GNN for variable size graph structures ... they can be used to aggregate elementary features without specifying the input dimensions" (L412)

**3. 信用分配**
**积分到"整时段、全网"级别**：奖励 (26) 对全部 $M$ 条流、$L$ 条路径求和（L302），一个动作向量对应**一个标量效用**；无逐跳奖励、无逐流/逐路径分解、**无损失原因区分**（丢包只通过 (8) 的成功指示量 $\kappa_y$（L128）进入 $\bar d$）。唯一逐路径量是路径时延三分解（L86）：
$$
\eta = \sum ( q + r + \gamma / c )
$$
  但它只进约束/评估，不进信用分配。

**4. 状态里有没有时间信息**
**未见**。逐字段均为 $t$ 时刻瞬时量：$C_t$ 由 (23) 当前残差带宽（L276）、$TR_t$ 为 "within each time slot" 的需求（L273）、$P_t$ 为当前路径矩阵（L279）；L266 更把"不依赖历史"写成 MDP 成立的前提。检索：`grep -n -iE 'ewma|history|window|trend|mask'` 全文 587 行 → ewma 0、window 0、mask 0；history 仅命中 L266（即"不用历史"这一句）；trend 命中 L64（相关工作"predicting the trend"）与 L454（曲线下降趋势）。→ 无时间聚合/差分/EWMA/记忆。

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
- (d) 约束 $\sum\omega=1$（L92/L136）**在动作层如何强制完全未说明**（`grep -n -iE 'softmax|normaliz|project'` 0 命中），也未见约束违反率指标。
- (e) **奖励是唯一标量** (26)，从未分解到流/路径/链路，**完全没有风险/尾部指标**（`grep -n -iE 'CVaR|risk|variance|tail'` 全文 0 命中，risk 仅命中参考文献）。
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

