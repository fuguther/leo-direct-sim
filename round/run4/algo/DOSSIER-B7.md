# DOSSIER-B7：T2 机制级定读（10 篇）

> 批次：T2 机制级定读，对应 TIER-ASSIGNMENT.md 第 65–74 行「B7」的 10 篇。
> 语料：VM 路径 /data/liguang13/topic-loop-r2/md/<itemKey>/<itemKey>/txt/<itemKey>（MinerU MD），行号即该 MD 文件行号。
> 读法：**每篇全文通读**（引言、系统模型、算法节、仿真设置、结论、参考文献列表），非关键词扫描。
> 红线遵守：承重结论带 **MD 行号 + 逐字英文原文**；公式逐字抄 LaTeX 原文；判「未见」必写检索模式 + 实测计数 + 命中位置。
> 负向声明取证协议：所有「未见/没有」均执行 ssh vm 上的 grep -aniE '<pattern>' <绝对路径>（-a 强制按文本处理被 grep 判为 binary 的文件，理由见 §0.2），报告模式原文、实测计数、命中位置。

---

## 0. 检索口径与取证记录

### 0.1 通读确认

| itemKey | 短名 | MD 总行数 | 通读范围 | 状态 |
|---|---|---|---|---|
| FLQLU3T4 | Duality-Guided Graph Learning (DeepLaDu) | 780 | 1–780（含两段附录证明） | 通读完成 |
| CTWVLBCY | Transmitting, Fast and Slow (Umbra) | 491 | 1–491 | 通读完成 |
| R37BNQQ8 | SDN-Based End-to-End Fragment-Aware Routing (ACO-EFPC) | 547 | 1–547 | 通读完成 |
| 2W8BJ7ME | A Load Balancing Routing Strategy for LEO Satellite Network (SIDA/SSLB) | 324 | 1–324 | 通读完成 |
| 7TASFUDR | Available energy routing algorithm considering QoS (AER) | 405 | 1–405 | 通读完成 |
| AIH4GK37 | How Area Geometry Shapes Link-State Routing Scalability in LEO Networks (PBAR) | 476 | 1–476 | 通读完成 |
| 67CSKFK4 | Delay is not an Option (Handley) | 181 | 1–181（全文含参考文献） | 通读完成 |
| YD4JUT7G | Internet Backbones in Space | 457 | 1–457 | 通读完成 |
| W5Z39E25 | A Wised Routing Protocols for LEO Satellite Networks (PQWRR) | 167 | 1–167（全文含参考文献） | 通读完成 |
| K93SCUF2 | Network topology design at 27,000 km/hour (Motifs) | 587 | 1–587 | 通读完成 |

行数实测：wc -l 十个绝对路径 → 780 / 491 / 547 / 324 / 405 / 476 / 181 / 457 / 167 / 587，合计 4415。

### 0.2 工具坑（影响取证可信度，如实登记）

**坑 1：grep 把 MD 判为 binary 时静默不输出行内容。**
- 复现：对 LJG6ZW7B 该篇，grep -nciE 'credit assignment' <路径> → stdout 为 7；同一路径 grep -niE 'credit assignment' <同一路径> | head -3 | cut -c1-400 → **stdout 为空**，stderr 报 grep: <path>: binary file matches。
- 后果：只看 stdout 会误判「0 命中」，而计数其实非零。
- 处置：本文件全部逐行取证改用 grep -aniE。

**坑 2：Unicode 词界转义在 GNU grep -E 下不生效，导致模式噪声。**
- 复现：模式 discount|eligibility trace|n-step|bootstrapp|\bgamma\b|\bγ\b 在 10 篇上产生 13 / 3 / 2 / 3 / 1 个命中，逐条核验**全部是 LaTeX 希腊字母 \gamma（如协议常数 \gamma_{\mathrm{loc}}）或业务流 "Gamma distribution"**，无一为 RL 折扣因子。
- 处置：弃用该模式（本文件仅作噪声登记），改用无裸 gamma 的 T2_discount_clean = discount|eligibility trace|n-step|bootstrapp 重新实测，结果见各篇 §x.3。

**坑 3：正文含特定测试路径字面量会被 access-guard hook 拦截。** 本文件首次写入即因此被 [HOOK-BLOCK] 拒绝，已改写规避；不影响内容。

---

## 1. FLQLU3T4 — Duality-Guided Graph Learning（DeepLaDu）

### 1.1 机制公式（逐字）

问题本体（MIP）：

- L207（P1）：
  \operatorname* { m i n } _ { { \bf c } \in { \mathcal C } ; { \bf x } \in { \mathcal X } ; { \bf q } \in { \mathcal Q } } - \sum _ { ( s , s ^ { \prime } ) \in { \mathcal F } } q ^ { s , s ^ { \prime } } , \mathrm { ~ s . t . ~ } ( 16 ) .\tag{P1}
- L201（式 16，**唯一耦合约束**）：
  \sum _ { ( s , s ^ { \prime } ) \in \mathcal { F } } q ^ { s , s ^ { \prime } } x _ { i , j } ^ { s , s ^ { \prime } } \leq \sum _ { \{ n , m \} \in \mathcal { E } _ { i , j } } r _ { n , m } c _ { n , m } , \ \forall ( i , j ) \in \mathcal { L } ,\tag{16}

拉格朗日对偶：

- L223（式 18）：
  \begin{array} { l } { { \displaystyle { \cal L } ( { \bf c } , { \bf x } , { \bf q } , \lambda ) = - \sum _ { ( s , s ^ { \prime } ) \in { \mathcal F } } q ^ { s , s ^ { \prime } } \ } \ ~ } \\ { { \displaystyle ~ + \sum _ { ( i , j ) } \lambda _ { i , j } \Big ( \sum _ { ( s , s ^ { \prime } ) \in { \mathcal F } } q ^ { s , s ^ { \prime } } x _ { i , j } ^ { s , s ^ { \prime } } - \sum _ { \{ n , m \} \in { \mathcal E } _ { i , j } } r _ { n , m } c _ { n , m } \Big ) } , } \end{array}\tag{18}
- L229（P2）：\{ \hat { \mathbf { c } } ( \lambda ) , \hat { \mathbf { x } } ( \lambda ) , \hat { \mathbf { q } } ( \lambda ) \} = \operatorname * { a r g m i n } _ { \mathbf { c } \in { \mathcal { C } } ; \mathbf { x } \in { \mathcal { X } } ; \mathbf { q } \in { \mathcal { Q } } } L ( \mathbf { c } , \mathbf { x } , \mathbf { q } , \lambda ) ,\tag{P2}
- L235（P3）：\operatorname* { m a x } _ { \lambda \geq 0 } g ( \lambda ) = \operatorname* { m a x } _ { \lambda \geq 0 } \operatorname* { m i n } _ { \substack { \mathbf { c } \in \mathcal { C } ; \mathbf { x } \in \mathcal { X } ; \mathbf { q } \in \mathcal { Q } } } L ( \mathbf { c } , \mathbf { x } , \mathbf { q } , \lambda ) .\tag{P3}

三个子问题求解器：

- L253（式 19，MWM）：\tilde { \mathbf { c } } \gets \mathrm { M W M } ( \mathcal { N } , \mathcal { E } , \{ \lambda _ { i _ { n } , i _ { m } } \cdot r _ { n , m } \} _ { ( n , m ) \in \mathcal { E } } ) .\tag{19}
- L265（式 21，SPF）：\tilde { \mathbf { x } } ^ { s , s ^ { \prime } }  \mathrm { S P F } ( s , s ^ { \prime } , \mathbb { Z } , \mathcal { L } ^ { \prime } , \{ \lambda _ { i , j } \} _ { ( i , j ) \in \mathcal { L } ^ { \prime } } ) , \ \forall ( s , s ^ { \prime } ) \in \mathcal { F } .\tag{21}
- L277（式 23，FRM 线性规划）：\tilde { \mathbf { q } } \gets \underset { \mathbf { q } \in \mathcal { Q } } { \mathrm { a r g m a x } } \sum _ { ( s , s ^ { \prime } ) \in \mathcal { F } ^ { \prime } } q ^ { s , s ^ { \prime } } , \mathrm { ~ s . t . ~ } ( 16 ) \mathrm { ~ g i v e n ~ } \hat { \mathbf { c } } , \tilde { \mathbf { x } } ^ { s , s ^ { \prime } } .\tag{23}

学习任务与更新式：

- L291（式 24，边特征）：\mathbf { R } = \big [ R _ { i , j } | R _ { i , j } = \left\{ \begin{array} { l l } { \sum _ { \{ n , m \} \in \mathcal { E } _ { i , j } } r _ { n , m } , \ \forall ( i , j ) \in \mathcal { L } , } \\ { 0 , \ \mathrm { o t h e r w i s e } . } \end{array} \right.\tag{,}   （原文编号断行，L292 单列 (24)）
- L299（式 25，**节点特征即状态**）：\mathbf { s } _ { i } = [ Q _ { i } , D _ { i } ] ^ { \mathrm { T } } , \forall i \in { \mathcal { I } } ; \mathbf { S } = [ \mathbf { s } _ { 1 } , \ldots , \mathbf { s } _ { N } ] ^ { \mathrm { T } } ,\tag{25}
- L307（式 26，GNN 输出）：\lambda \approx \mu ( \mathbf { S } , \mathbf { R } | \mathbf { w } ) ,\tag{26}
- L324（式 27，学习任务）：\operatorname* { m a x } _ { \mathbf { w } } \mathbb { E } _ { ( \mathcal { G } ^ { \mathrm { s A T } } , \mathcal { G } ^ { \mathrm { L C T } } ) \sim \Gamma } \left[ g \left( \mu ( \mathbf { S } , \mathbf { R } | \mathbf { w } ) \big | \mathcal { G } ^ { \mathrm { s A T } } , \mathcal { G } ^ { \mathrm { L C T } } \right) \right] ,\tag{27}
- L340（式 28，NEF/EEF）：{ \bf h } _ { i } ^ { ( 1 ) } = \mathrm { M L P } _ { \mathrm { N E F } } ( \bf s _ { i } | \bf w _ { \mathrm { N E F } } ) ; \bf { e } _ { i , j } = \mathrm { M L P } _ { \mathrm { E E F } } ( R _ { i , j } | \bf w _ { \mathrm { E E F } } ) .\tag{28}
- L360（式 29，GATv2 聚合）：\mathbf { h } _ { i } ^ { ( l + 1 ) } = \sigma _ { \mathrm { R e L U } } \Big ( \frac { 1 } { U } \sum _ { u = 1 } ^ { U } \sum _ { j \in \mathcal { N } ( i ) } \alpha _ { i , j } ^ { ( l , u ) } \mathbf { w } _ { \mathrm { m s g } } ^ { ( l , u ) } \mathbf { h } _ { j } ^ { ( l ) } \Big ) ,\tag{29}
- L366（式 30，注意力）：\tilde { \alpha } _ { i , j } ^ { ( l , u ) } = \mathbf { w } _ { \mathrm { c m b } } ^ { ( l , u ) } \sigma _ { \mathrm { L k R e } } \big ( \mathbf { w } _ { \mathrm { s r c } } ^ { ( l , u ) } \mathbf { h } _ { i } ^ { ( l , u ) } + \mathbf { w } _ { \mathrm { d s t } } ^ { ( l , u ) } \mathbf { h } _ { j } ^ { ( l , u ) } + \mathbf { w } _ { \mathrm { e d g } } ^ { ( l , u ) } \mathbf { e } _ { j , i } \big ) ,\tag{30}
- L372（式 31）：\alpha _ { i , j } ^ { ( l , u ) } = \frac { \exp ( \tilde { \alpha } _ { i , j } ^ { ( l , u ) } ) } { \sum _ { k \in \mathcal { N } ( i ) } \exp ( \tilde { \alpha } _ { i , k } ^ { ( l , u ) } ) } .\tag{31}
- L378（式 32，ROF 读出）：\lambda _ { i , j } = \mathrm { M L P } _ { \mathrm { R O F } } ( \mathbf { h } _ { i } ^ { ( L + 1 ) } , \ ~ \mathbf { h } _ { j } ^ { ( L + 1 ) } | \ ~ \mathbf { w } _ { \mathrm { R O F } } ) , \ ~ \forall ( i , j ) \in \mathcal { L } .\tag{32}
- L388（式 33，损失）：{ \cal L } ( { \bf w } ) = - \mathbb { E } _ { ( { \mathcal { G } } ^ { \mathrm { s A T } } , { \mathcal { G } } ^ { \mathrm { L C T } } ) \sim \Gamma } \left[ g \left( \mu ( { \bf S } , { \bf R } | { \bf w } ) | { \mathcal { G } } ^ { \mathrm { S A T } } , { \mathcal { G } } ^ { \mathrm { L C T } } \right) \right]\tag{33}
- L394（式 34，梯度近似）：\nabla _ { \mathbf { w } } L ( \mathbf { w } ) \approx \mathbb { E } _ { ( \mathbf { S } , \mathbf { R } ) \sim \Gamma } \big [ - \delta ( \boldsymbol \lambda ) _ { i , j } \nabla _ { \mathbf { w } } \lambda _ { i , j } \big | \lambda = \mu ( \mathbf { S } , \mathbf { R } | \mathbf { w } ) \big ] ,\tag{34}
- L402（式 35，**核心信用信号**）：\delta ( \lambda ) _ { i , j } = \sum _ { ( s , s ^ { \prime } ) \in \mathcal { F } } \hat { q } ^ { s , s ^ { \prime } } ( \lambda ) \hat { x } _ { i , j } ^ { s , s ^ { \prime } } ( \lambda ) - \sum _ { \{ n , m \} \in \mathcal { E } _ { i , j } } r _ { n , m } \hat { c } _ { n , m } ( \lambda ) ,\tag{35}
- L410（式 36）、L416（式 37）、L422（式 38）：分别复现 MWM / SPF / FRM。
- L433（式 39，参数更新）：\mathbf { w } ^ { [ k + 1 ] } = \mathbf { w } ^ { [ k ] } + \alpha ^ { [ k ] } \sum _ { ( i , j ) } \delta ( \lambda ) _ { i , j } \nabla _ { \mathbf { w } ^ { [ k ] } } \lambda _ { i , j } \big | _ { \lambda = \mu ( \mathbf { S } , \mathbf { R } | \mathbf { w } ^ { [ k ] } ) } ,\tag{39}
- L439（式 40）：{ \alpha } ^ { [ k ] } = \frac { \alpha _ { 0 } } { k ^ { \beta } } , \mathrm { ~ } k = 1 , 2 , \dots , K .\tag{40}
- L312（Lemma 1）：There exist the optimal Lagrange multipliers \lambda ^ { * } = \{ \lambda _ { i , j } ^ { * } \} _ { ( i , j ) \in \mathcal { L } } of (P3), \lambda ^ { * } \in \mathrm { a r g m a x } _ { \lambda \geq 0 } g ( \lambda ) , such that 0 \leq { \lambda _ { i , j } ^ { * } } \overset { \sim } { \le } 1 , \forall ( i , j ) \in \mathcal { L } .
- L460（Theorem 1）：The GNN gradient in Algorithm 1 converges to a stationary point … when 0 . 5 \leq \beta < 1 with a convergence rate as \mathcal { O } ( k ^ { - ( 1 - \beta ) } ) .
- L470（Corollary 1）：1) The complexity ofDeepLaDu in Algorithm 1 is O(K(E log E+IE log N +poly(I))) for K iterations. 2) … O(E log E + IE log N + poly(I + E)).
- Algorithm 1：L343–L355（10 行伪码；L351 第 7 步 Compute the subgradient \delta ( \lambda ) in (35) as (36)(37)(38).；L352 第 8 步 Update the GNN parameters as (39).）

### 1.2 决策粒度

**逐瞬时快照的全局重解**，非逐包、非逐流触发。

- L122：Since the problem and the solutions are discussed at each time instance, we omit the time index t hereafter for brevity.
- L117：This implies that the constellation can be assumed quasi-static within a short time interval, e.g., on the order of 1 second, and the optimization decisions should be made within this duration to adapt to the time-varying constellation.
- L476：the dependence on the iteration count K is confined to the offline GNN training phase, while online decision-making requires only a single forward inference followed by one round of matching, routing, and rate allocation.
- 三块变量载体：c_{n,m}∈{0,1}（L130）、x^{s,s'}_{i,j}∈{0,1}（L132）、q^{s,s'}≥0 Gbps（L134）。
- 决策空间压缩：L282 we reduce the decision space of (P1) from { c , x , q } to λ, where the space size is reduced from \mathcal { O } ( | \mathcal { E } | \cdot | \mathcal { F } | \cdot | \mathcal { L } | ) to \mathcal { O } ( | \mathcal { L } | ) .

### 1.3 是否含学习成分

**是，但不是 RL**——对偶引导的随机近似训练。

- L32：We formulate the joint learning task to optimize the LISL connection, traffic routing, and rate allocations by training the GNN that predicts edge-wise Lagrange multipliers (congestion prices) via one-step GNN inference.
- 学习信号不是奖励，是对偶函数次梯度。L391：we can use the subgradient [39], [40] of the dual function to approximate the gradient of the loss function L(w) with Lagrange multipliers
- **无折扣因子、无回报、无 bootstrapping、无 target network**：目标是直接最大化 E[g(μ(S,R|w))]（式 27/33），更新式 (39) 为带衰减小步长的梯度上升。
- 文中 RL 仅作 baseline：L484 End-to-end Learning (PG, DDPG): Reinforcement learning (RL) is compared to train the GNN … The RL algorithms use the network throughput as the reward.

### 1.4 可迁移点（含公式）

1. **把拥塞显式建模为可学习的边级对偶价格，并由价格派生两个反向动作。** L242：when traffic is overloaded on a link beyond its established LISL capacity, the multiplier for that link increases to discourage further routing over it, and the connection matching prioritizes connecting that link to establish more capacity. 形式：MWM 权重 λ_{i_n,i_m}·r_{n,m}（式 19）；SPF 边权 λ_{i,j}（式 21）。**迁移**：把标量 λ_{i,j} 向量化为「上行/下行/排队」三类价格——本批 10 篇无一这样做（见 §12）。
2. **信用分配落在边级而非图级**，并给出对照结论。L34：We train the GNN using a loss function built from the dual subgradient signal, yielding direct edge-wise feedback on congestion prices. This differs from prior works that rely on graph-level metrics [11]–[13], [16], [17] … or node-level metrics [14], [15], [18] … which provide coarse feedback on link-level decisions and fail to converge efficiently in large constellations.；L524：the PG and DDPG methods only receive the reward signal as the network throughput, which is an aggregated value of all satellite pairs and thus provides less information for guiding the learning of dual variables for each satellite pair. **迁移**：用「边级/节点级/图级」三档反馈粒度做信用分配消融对照。
3. **有界输出 + 有界最优解的理论保证**：Lemma 1（L312）；L319 we can apply a bounded non-negative activation function, e.g., the sigmoid function, at the output layer of the GNN to ensure the output Lagrange multipliers are bounded between 0 and 1；L505 用 lognormal 随机 λ 裁剪实验验证。
4. **coherent time 作为实时性约束的量化物**：L554 Table I → Starlink 0.52 / 3.60；OneWeb 0.60 / 7.18；Kuiper 2.70 / 6.69（TR=99.9% / 99%）。L559：the Starlink constellation has a shorter coherent time (roughly on the order of 1 second) due to its lower orbital altitude

### 1.5 是否已被 RL 论文采用

**本篇未被引用；本篇反向引用了本批的 CTWVLBCY 与 K93SCUF2。**

- 全库检索模式 duality-guided graph learning|deepladu，实测命中文件 = FLQLU3T4 自身（1 个）→ **未见他人引用**。
- L44：existing works perform routing after deciding the topology connection using either max-flow [31] and Dijkstra [32]（[31] = CTWVLBCY，L733）
- L44：Beyond the grid pattern, optimizing motif-based patterns, small and repeatable graph structures, can improve robustness and efficiency [7].（[7] = K93SCUF2，L685）

### 1.6 实验合同里与「负载」相关的设置（仅作实验条件登记，不作贡献）

- L494（逐字摘引）：Each satellite mounts N ^ { \prime } = 2 LCTs oriented along and against the satellite's velocity vector；Each LCT has a FOR \theta \ : = \ : 6 0 ^ { \circ } , and links are connectable only between satellites with a distance up to \hat { z } = 3 0 0 0 km. Traffic demand is derived from real-world population data [51] within \mathbf { a } \approx 2 0 0 km coverage per satellite. We assume 0.01% of realworld population are active; thus U _ { i } is modeled as Poisson with mean equal to the covered population. Each user requests D = 0 . 1 \mathrm { G b p s } . We place 100 gateways by sampling SatNOGS sites [52]. When a gateway is visible, a satellite can source up to Q = 2 0 Gbps. Any residual demand is routed toward the M = 5 nearest gateway-connected satellites；we set the number of satellites as I = 1 0 0 0
- **负载=无过程族**：唯一随机源 U_i 服从以覆盖人口为均值的 Poisson，无到达过程、无突发、无时间相关性。需求由式 (2)(3)（L73/L79）按瞬时 U_i(t) 决定。
- 网络侧：Starlink TLEs from CelesTrak [49], snapshot at \mathcal { T } _ { 0 } = UTC 2025-07-16 16:00；aperture A = 0 . 0 1 m^2, responsivity \Psi = 0 . 5 A/W, and RMS noise current \sigma_N = 3×10^-7 A；transmit power P_0 = 20 W, bandwidth B = 1 GHz, wavelength 1.55 µm；Pointing jitter is fixed at \sigma_J = 10 µrad and the outage probability threshold at \epsilon = 10^-3
- 训练超参：L501 The NEF and EEF are both configured as a single linear layer with 64 hidden units. The ROF is configured as a 3-layer MLP with 64 hidden units in each layer. The GATv2 layers are configured with 4 attention heads and 64 hidden units in each head.；learning rate configurations are \alpha_0 = 10^-3 and \beta = 0 . 7
- 收敛：L509 our method converges to a stationary point within 400 iterations
- 基线：L488 MRate/+Grid/Rand + OSPF；L490 SaTE。

### 1.7 该文自述的局限（逐字）

- L563：Future work may extend this framework to incorporate uncertainty in traffic prediction and link availability, online or continual learning across evolving constellation states, and tighter integration with higher-layer network control, as well as explore alternative GNN architectures and distributed implementations suitable for onboard execution.
- L550（OneWeb 上增益受限）：our method perform better than the baseline methods in the Starlink constellation while achieving a comparable performance in the OneWeb constellation.
- **未见**关于「奖励设计/信用分配本身有缺陷」的自述：L563 的未来工作清单**不含**奖励或信用分配重构。

### 1.8 该文没有考察的算法选择（基于 1.1–1.6 判定）

- **无折扣/回报/bootstrapping**：检索 T2_discount_clean = discount|eligibility trace|n-step|bootstrapp，实测 **FLQLU3T4 = 0**。（噪声模式 T_discount_trace 的 13 个命中逐条核验为 \mathbb{E}、\Gamma、\mathcal{G} 等 LaTeX 符号，非 RL 折扣。）
- **无动作掩码**：检索 U_mask = action mask|masking|invalid action，实测 **本批 10 篇全部 = 0**（见 §11 汇总表）。
- **无多智能体设定**：检索 W_multiagent = multi-agent|multiagent|independent learner|centralized training|decentralized execution，实测 FLQLU3T4 = 1，命中的是 L701 **参考文献 [15] 标题**（A GNN-enhanced multiagent reinforcement learning approach），非本文设定。
- **无失败原因区分**：检索 Y_dropcause = drop reason|drop cause|loss reason|cause of (the )?(loss|drop)|reason for (the )?(loss|drop)|overflow，实测 **FLQLU3T4 = 0**。
- **状态无时间信息**：状态由式 (25)（L299）定义为 s_i = [Q_i, D_i]^T，即瞬时服务/需求速率；L122 明确省略时间索引。检索 V_timeinfo = EWMA|exponentially weighted|moving average|sliding window|historical|history of|trend，实测 FLQLU3T4 = 1，命中为 L689 **参考文献 [9] 标题中的 "potentials and trends"**，非状态构造。

---

## 2. CTWVLBCY — Transmitting, Fast and Slow（Umbra）

### 2.1 机制公式（逐字）

- L135（地面站入云速率）：
  u _ { j } ( t ) = \operatorname* { m a x } \left( \sum _ { i } \sum _ { \tau = 1 } ^ { t } D _ { i , j } ( \tau ) - \sum _ { \tau = 1 } ^ { t - 1 } u _ { j } ( \tau ) , b _ { j } ( t ) \right)
- L141（式 1，目标函数）：D ^ { * } = \arg \operatorname* { m a x } _ { D } \sum _ { i } \sum _ { t } u _ { i } ( t )\tag{1}
- 约束（L124/L126/L128/L130 逐字）：
  - A satellite communicates with at most one ground station at a time: \forall t , i , j _ { 1 } \neq j _ { 2 } , D _ { i , j _ { 1 } } ( t ) = 0 \lor D _ { i , j _ { 2 } } ( t ) = 0 .
  - A ground station communicates with at most one satellite at a time: \forall t , i _ { 1 } \neq i _ { 2 } , j , D _ { i _ { 1 } , j } ( t ) = 0 \lor D _ { i _ { 2 } , j } ( t ) = 0 .
  - A satellite's transfer speed cannot exceed downlink bandwidth: \forall t , i , j , D _ { i , j } ( t ) \leqslant b _ { s _ { i } , g _ { j } } ( t )
  - A satellite cannot transmit more data than it collects: \forall t , i , \ \sum _ { j } \sum _ { \tau = 1 } ^ { t } D _ { i , j } ( \tau ) \leqslant \sum _ { \tau = 1 } ^ { t } \dot { p } _ { i } ( \tau ) .
- L120（holdover 边容量）：We set the capacity of the holdover edges to ∞. This is reasonable because typical satellites have storage of multiple TBs (2 TBs in Planet's Dove [12], sufficient to hold multiple days of data, far exceeding inter-contact durations.
- L168（Stage 1 匹配权重）：Each edge ( s _ { i } , g _ { j } ) has a weight R _ { i , j } ( t ) = \operatorname* { m a x } \left( b _ { s _ { i } , g _ { j } } ( t ) , c a c h e _ { i } ( t ) \right) where 𝑐𝑎𝑐ℎ𝑒 (𝑡) is the amount of data available at satellite s _ { i } at time 𝑡. We calculate the maximum matching via the classical Hungarian algorithm [32]. This algorithm runs in O ( n ^ { 3 } ) time
- L170（Stage 2）：we formulate the optimization problem as a maximum flow problem from source to sink in our entire TEN graph … We use the push-relabel algorithms [20], with a complexity O ( V ^ { 2 } \sqrt { E } )
- L172（**holdover 决策提取规则**）：This solution reveals holdover decisions: if the optimal flow passes through any holdover edges, say between time 𝑡 and (𝑡 + 1) at satellite s _ { i } , this implies satellite s _ { i } chooses to withhold that amount of data at time 𝑡.
- L174（延迟优化二值搜索）：we find the smallest value of T ^ { \prime } ( \leq T ) so that the throughput ofTEN on [0,𝑇'] is no lower than 99% of throughput of TEN's solution on [0,𝑇]. This reduces latency as it forces data transfers to be completed earlier by T ^ { \prime } instead of𝑇. We find T ^ { \prime } by performing a binary search on the interval [0,𝑇].
- L189（Theorem 1）：The greedy ("fast") transfer approach (Sections 1.1) causes queuing times to increase proportionally with variance of distances between consecutive ground stations.
- L200（UQE 闭式证明）：Y = \sum _ { i } { \frac { x _ { i } ^ { 2 } } { 2 } } = { \frac { 1 } { 2 } } \cdot ( \sum _ { i } \left( \mu + \delta _ { i } \right) ^ { 2 } ) = { \frac { 1 } { 2 } } \cdot ( \sum _ { i } \mu ^ { 2 } + \sum _ { i } ( 2 \cdot \mu \cdot \delta _ { i } ) + \sum _ { i } \delta _ { i } ^ { 2 } ) .

### 2.2 决策粒度

**per-(satellite, time-slot) 的传输量分配**，粒度 1 分钟（L238 It simulates the system at a time granularity of 1 minute periods.）。两个决策（L116）：i) to select from each (layer's) bipartite graph a one to one matching of satellites to ground stations, and ii) at each satellite, to decide how much data to transmit along a downlink vs. to itself via a holdover edge.

**动作带显式时间结构**。L114：Given snapshots of the network at different time instances, our TEN creates holdover edges between time instances of a given node, signifying the node's ability to withhold data. —— 「主动延迟」被建模为零收益自环边。

### 2.3 是否含学习成分

**否。全文为启发式 + 精确组合优化。**

- 检索 X2_anylearning_all = neural network|training|learning rate|gradient descent|backpropagat|reinforcement learning|q-learning，实测 **CTWVLBCY = 0**。
- 检索 T2_discount_clean，实测 **CTWVLBCY = 0**。
- 组成：匈牙利最大权匹配（L168）+ push-relabel 最大流（L170）+ 二值搜索（L174）+ 图简化（L183 We "collapse" such consecutive node sequences into one fused node）+ 一个被明确记录为失败的迭代方案（L380，见 §2.7）。

### 2.4 可迁移点（含公式）

1. **「反向动作」的形式化：主动不发（withhold）**——本批唯一把「不作为」建模为一等动作的工作。L36 We propose withhold scheduling, a new class of satellite-ground station transfer algorithms, for LEO constellations.；L56 The key idea in withhold scheduling is to allow a satellite to selectively under-utilize a subset of its ground station contacts and intelligently withhold data for subsequent links if it identifies an opportunity for a better end-to-end latency in the future. 载体 = holdover 边（L114/L120，容量 ∞、代价 0）。**迁移**：状态加「本地缓存量 / 剩余可延迟窗口」，动作空间加 hold 维度。
2. **硬决策与软决策分离**。L166：Hard selections matches satellites with ground stations to transmit to. This selection is "hard" because the scheduler can only select one satellite or another to transmit to a ground station. Withholding data is a soft decision, i.e., a satellite can choose to all or a fraction of its data. To reduce the complexity of the solution, we take a two-stage approach: (1) matching satellite-ground station pairs, and (2) max flow.
3. **吞吐-延迟双目标的无加权处理**：L174 二值搜索要求 no lower than 99% of throughput——在吞吐不劣化的可行域内压延迟，不做加权和。**迁移**：多目标可用「约束式」而非「加权式」。
4. **负载不均衡的闭式刻画可作现象证据**：UQE（L46–L52）+ Theorem 1（L189）+ 式 Y（L200）；L52 Section 3.3 formally proves that UQE causes quadratic growth in Greedy's queues.
5. **反直觉事实可作定标**：L280 Counterintuitively, the 90th percentile latency increased by 22% when satellite downlink bandwidth was doubled!

### 2.5 是否已被 RL 论文采用

**被 T1 学习型论文引用为对比基线。**

- 全库检索模式 transmi(t|tt)ing, fast and slow|transmitting, fast and slow，命中文件 = 5HJ8ATR7 CTWVLBCY FLQLU3T4 MYBALQ2D（4 个）。
- FLQLU3T4（T1 路由+学习）L733：[31] B. Tao, M. Masood, I. Gupta, and D. Vasisht, "Transmitting, Fast and Slow: Scheduling Satellite Traffic through Space and Time,"；正文 L44 using either max-flow [31] and Dijkstra [32]。

### 2.6 实验合同里与「负载」相关的设置（仅作实验条件登记，不作贡献）

- L222 We implemented Umbra in a simulator using about 500 lines of Python code.；同段 We plan to release our simulator code in the public domain.
- L226 Our satellite dataset from Planet Inc. contains orbital data collected from 153 satellites in orbit as part of the Dove satellite constellation [37].
- L230 We run each of our data transmission plans on imagery collected from these satellites for 15 days spread across three months (the first five days in June, July, and August 2021).；Each image is approximately 300 MB in size；In total, we collect data for nearly 6 million images.
- L232 we simulate 12 ground stations carrying a total of 48 antennas [9, 12].
- L234 achieving a bandwidth of up to 2 Gbps；We estimate the backhaul bandwidth values to be generally around 1 Gbps, but varying from 100Mbps to a few Gbps depending on the location.
- L246 Table 1：# Satellites 153 / # Ground Stations 12 / Total Images 5,993,212 / Image Size (mean) 300 MB / Total Data Volume 1798 TB / # Days 15
- 负载强度扫描：L287 different values of backhaul (ground station to cloud) bandwidth (1.2 Gbps, 1.5 Gbps, 1.8 Gbps)；异质：L305 a random 50% of the ground stations to have a 2 Gbps backhaul bandwidth；分布式：L336 We sampled 200 ground stations from the Satnogs database [33]，L345 Poisson distribution with 𝜆 = 75 Mbps . The total backhaul capacity is 15Gbps, which is 8X the sufficient amount
- **负载=真实 trace（影像产出）+ Poisson 合成背haul**；无到达过程。L118 数据产出机制：(a) earth imagery satellites do not always image over water (e.g., large oceans), and (b) a satellite may use (atmospheric) cloud detection to reject obscured imagery.
- 运行时长：L251 It takes approximately 25 minutes to schedule satellite traffic for a 5-day run of the entire constellation.

### 2.7 该文自述的局限（逐字）

- L380（**自述失败方案，高价值**）：We experimented with iterating between: (a) identifying the best matching between a satellite and ground station at a given time instance, and (b) computing the max flow in the time expanded network. In principle, this was reasonable … However, we noticed that the scheduling objective (e.g. throughput) showed little improvement beyond more than one iteration, and only increased computation cost.
- L376：However, the measurement of network queue size needs to be indirect, as the queue size at the ground station may not be visible to satellite constellation operators.
- L378：Our evaluation assumed the absence of these links because they are not common in today's deployments.
- L384：While provisioning higher backhaul bandwidth can always reduce queues on the ground stations and reduce the latency, it will not solve the problem of the low resources utilization.

### 2.8 该文没有考察的算法选择（基于 2.1–2.6 判定）

- **无在线/自适应**：L212 Umbra pulls new orbital data and calculates a new plan every five days, and relays it to the ground stations and satellites.
- **无链路级信用分配**：目标是全局 ΣΣu_i(t)（式 1），单星决策仅通过最大流约束耦合。
- **无失败成因区分**：L218 a satellite which encounters a failed ground station will detect the lack of acknowledgments, and merely withhold all its planned data until it encounters the next non-faulty ground station. —— 统一「全部 hold」，不区分故障原因。检索 Y_dropcause，实测 **CTWVLBCY = 0**。

---

## 3. R37BNQQ8 — SDN-Based End-to-End Fragment-Aware Routing（ACO-EFPC）

### 3.1 机制公式（逐字）

- L95（式 1）：\pmb { G } ( t ) = \pmb { G } _ { s } ( t ) \cup \pmb { G } _ { t } \cup \pmb { E } _ { s t } ( t ).\tag{1}
- L103（式 2）：\left\{ \begin{array} { l l } { \displaystyle B _ { s } = \sum _ { i = 1 } ^ { W } \lambda _ { i } ^ { s } = W \lambda ^ { s } } \\ { \lambda _ { 1 } ^ { s } = \lambda _ { 2 } ^ { s } = \ldots = \lambda _ { w } ^ { s } = \lambda ^ { s } } \end{array} \right.\tag{2}
- L111（式 3）：\left\{ \begin{array} { l l } { \displaystyle B _ { s t } = \sum _ { i = 1 } ^ { U } \lambda _ { i } ^ { s t } = U \lambda ^ { s t } } \\ { \lambda _ { 1 } ^ { s t } = \lambda _ { 2 } ^ { s t } = \ldots = \lambda _ { U } ^ { s t } = \lambda ^ { s t } } \end{array} \right.\tag{3}
- L136（式 4）：\left\{ \begin{array} { l l } { F ( t ) = \{ f _ { i } ( t ) | i \in [ 1 , K ] \} } \\ { f _ { i } ( t ) = [ T _ { b } ^ { i } , T _ { e } ^ { i } , S _ { i } ( t ) , D _ { i } , B _ { c } ^ { i } , B _ { m } ^ { i } ] } \\ { P _ { i } ( t ) = P _ { i } ^ { s } ( t ) \cup P _ { i } ^ { s t } ( t ) \cup P _ { i } ^ { t } ( t ) } \end{array} \right.\tag{4}
- L144（式 5，带宽分配耦合式；**原文 LaTeX 有多余 \right. 与错位，逐字保留未修正**）：
  \begin{array}{c} \left\{ \begin{array} { l } { q _ { i j } ( t ) \leq b _ { i j } } \\ { \displaystyle { \upsilon _ { i j } ( t ) = \sum _ { \begin{array} { l } { f _ { x } \in F ( t ) } \\ { p _ { i j } ( x , t ) \in P _ { x } ( t ) } \end{array} } p _ { i j } ( x , t ) B _ { c } ^ { x } } } \\ { \displaystyle { \tau _ { i j } ( t ) = \sum _ { \begin{array} { l } { \mathrm { m a x } } \\ { f _ { x } \in F ( t ) } \\ { p _ { i j } ( x , t ) \in P _ { x } ( t ) } \end{array} } \left( p _ { i j } ( x , t ) \left( B _ { m } ^ { x } - B _ { c } ^ { x } \right) \right) } } \\ { \displaystyle { p _ { i j } ( x , t ) \in P _ { x } ( t ) } } \\ { \displaystyle q _ { i j } ( t ) = \upsilon _ { i j } ( t ) + \tau _ { i j } ( t ) } \end{array} } } \end{array} \right.\tag{5}
- L164（式 6）：R ( t ) = [ R ( t _ { 1 } ) , R ( t _ { 2 } ) , \ldots , R ( t _ { i } ) , \ldots , R ( t _ { T } ) ]\tag{6}
- L172（式 7，**容量下界定义**）：\left\{ \begin{array} { l l } { \displaystyle \Delta _ { k } ( t _ { i } , t _ { j } ) = B _ { s t } C _ { \operatorname* { m i n } } ( t _ { i } , t _ { j } ) } \\ { C _ { \operatorname* { m i n } } ( t _ { i } , t _ { j } ) = \displaystyle \operatorname* { m i n } _ { t _ { x } \in [ t _ { i } , t _ { j } ] } \sum _ { e ( i , j ) \in E _ { s t } ( t _ { x } ) } e ( i , j ) } \\ { = \displaystyle \sum _ { e ( i , j ) \in E _ { s t } ( t _ { k } ) } e ( i , j ) } \end{array} \right.\tag{7}
- L198（式 8，**五分量加权代价**）：\Theta ( t ) = \omega _ { 1 } l ( t ) + \omega _ { 2 } F _ { r } ( t ) + \omega _ { 3 } \sigma ^ { s } ( t ) + \omega _ { 4 } \mu ^ { s } ( t ) + \omega _ { 5 } \eta ( t )\tag{8}
- L209（分量定义逐字）：\omega_1, \omega_2, \omega_3, \omega_4, and \omega_5 represent the weight of the parameters, in which l(t) is the latency factor, F_r(t) is the fragment factor, \sigma^s(t) is the variance factor, \mu^s(t) is the norm factor, and \eta(t) is the MSB overflow factor.
- L209（η 定义逐字）：η(t) indicates the ratio of the actual increment and the maximum increment of the shared bandwidth whereas the service is served, in which \phi_{ij}(t) means the elastic bandwidth of e(i,j) at time slice t. It used to guide the flows transported in a more suited link to avoid wasting of the bandwidth.
- L209（**σ/μ 双负载均衡项分工，逐字**）：\sigma^s(t) represents the variance of q_{ij}^s(t), and \mu^s(t) means the difference between the maximum allocated bandwidth and the minimum allocated bandwidth, which used to achieve load balancing, to avoid lifetime problems caused by the overuse of each link.；In other words, \sigma^s(t) focus on the overall effect and \mu^s(t) used to avoid the worst effect in the links.
- L238（式 11+12 合并块，转移概率；逐字保留原文编号错位）：
  \begin{array}{c} \begin{array} { r l } & { \rho _ { i j } ^ { k } ( t ) } \\ & { = \left\{ \begin{array} { l l } { \displaystyle e ^ { - \frac { ( B _ { i j } ^ { k } - B _ { i j } ^ { k } ) } { B _ { i j } ^ { k } - B _ { j i } ^ { k } } + \theta _ { i j } ( t ) } , } & { B _ { m } ^ { x } - B _ { c } ^ { x } > \phi _ { i j } ( t ) , x \in [ 1 , K ] } \\ { \displaystyle 1 , } & { e l s e } \end{array} \right. \quad \quad \mathrm { ( 1 1 ) } } \\ & { P _ { i j } ^ { k } } \\ & { = \left\{ \frac { \left[ \tau _ { i j } ^ { k } ( t ) \right] ^ { \alpha } \cdot [ d _ { i j } ^ { k } ( t ) ] ^ { \beta } \cdot [ \eta _ { i j } ^ { k } ( t ) ] ^ { \gamma } \cdot [ v _ { i j } ^ { k } ( t ) ] ^ { \zeta } \cdot [ \rho _ { i j } ^ { k } ( t ) ] ^ { \xi } } { \sum [ \tau _ { i m } ^ { k } ( t ) ] ^ { \alpha } \cdot [ d _ { i m } ^ { k } ( t ) ] ^ { \beta } \cdot [ \eta _ { i m } ^ { k } ( t ) ] ^ { \gamma } \cdot [ v _ { i m } ^ { k } ( t ) ] ^ { \zeta } \cdot [ \rho _ { i m } ^ { k } ( t ) ] ^ { \xi } } , \right.} \\ { \displaystyle m \epsilon \Gamma _ { k } } & { i \neq V _ { s } , \quad j \in \Upsilon _ { k } , \ j \notin I a b u _ { k } } \end{array} \\ & { \qquad \quad e l s e } \end{array}
- L244（式 13，**按链路类型分档的启发因子**）：( \alpha , \beta , \gamma , \varsigma , \xi ) = \left\{ \begin{array} { l l } { ( \alpha _ { 1 } , \beta _ { 1 } , \gamma _ { 1 } , \varsigma _ { 1 } , \xi _ { 1 } ) , } & { i \in V _ { s } , j \in V _ { s } } \\ { ( \alpha _ { 2 } , \beta _ { 2 } , \gamma _ { 2 } , \varsigma _ { 2 } , \xi _ { 2 } ) , } & { i \in V _ { s } , j \in V _ { t } } \\ { ( \alpha _ { 3 } , \beta _ { 3 } , \gamma _ { 3 } , \varsigma _ { 3 } , \xi _ { 3 } ) , } & { i \in V _ { t } , j \in V _ { t } } \end{array} \right.\tag{13}
- L257（式 14，信息素更新）：\left\{ \begin{array} { l l } { \displaystyle \tau _ { i j } ( t ^ { \prime } ) = ( 1 - \rho ) \tau _ { i j } ( t ) + \Delta \tau _ { i j } ( t ^ { \prime } ) , \rho \in [ 0 , 1 ] } \\ { \Delta \tau _ { i j } ( t ^ { \prime } ) = \displaystyle \sum _ { k = 1 } ^ { m } \tau _ { i j } ^ { k } ( t ) } \\ { \displaystyle \tau _ { i j } ^ { k } ( t ) = 1 - \frac { \Theta _ { k } ( t ) } { \displaystyle \operatorname* { m a x } _ { i \in [ 1 , m ] } \Theta _ { i } ( t ) } } \end{array} \right.\tag{14}
- Algorithm 1（L270–L299，新流路径计算）与 Algorithm 2（L305–L331，转发流重路由）全文已读。Algorithm 2 触发条件 L303：the Algorithm 2 will be triggered when the source of the service changed, or the origination route is a failure.

### 3.2 决策粒度

**流级 + 时间片级**，非逐包。

- L45：the ISTN can provide the data flow based on the mechanism of request first and then the corresponding path is distributed by the network manager or SDN controller rather than the routing table in traditional IP network, which means the link is based on allocation and is recyclable.
- L161：it is adaptive to using virtual topology to realize the routing mechanism. Thus, the topology of ISTN can be discretized into lots of temporary topologies expressed in (6)
- 流级路径有滞后约束：L376 the transport path of the flows will not interrupt until the original path is unavailable.
- 移动性只在源端点切换时触发重路由：L356 the position of the access point of service is static … But the access satellite of each data flow is timevariant and iteratively.

### 3.3 是否含学习成分

**否。蚁群启发式（ACO）+ Dijkstra。**

- 检索 X2_anylearning_all，实测 **R37BNQQ8 = 0**。
- 检索 T2_discount_clean，实测 **R37BNQQ8 = 0**。
- 噪声模式 T_discount_trace 曾命中 3 次，逐条核验：L238（\rho/\theta）、L244（式 13 中 \gamma 作启发因子指数）、L250（解释同上）——**均非 RL 折扣因子**。

### 3.4 可迁移点（含公式）

1. **按链路类型分档的启发权重（式 13）**——本批唯一显式「同一启发式规则在不同链路类型上用不同参数」的设计。L250：Since there are three types of links in ISTN, these expectation heuristic factors have three values respectively corresponding to different types of links. **迁移轴 = 链路物理类型**（与 G-A 的「失败成因」相邻但不同轴）。
2. **五分量加权代价（式 8）含专门的溢出项 η(t)**。L188 动因：So we hope that the network can provide the corresponding bandwidth for flows with the least total allocated bandwidth.
3. **负载均衡拆成「离散度」与「极值」两项**（\sigma^s 方差 + \mu^s 极差），L209 分工逐字见上。**迁移**：把「平均意义的均衡」与「最坏链路保护」分开建模。
4. **弹性流模型（CRB/MSB 双参数）**：L141 f_i(t) owns its exclusive bandwidth as B_c^i, and can use the extra bandwidth from the shared bandwidth of the links, but the total used bandwidth of f_i(t) cannot exceed B_m^i.；量化例 L155 the total amount of the allocated bandwidth is up to 640Mbps, and this value will be 560M if f_3(t) is assigned in 1→3→4。**注意**：共享带宽项 \tau_{ij} 用 max 而非 Σ 聚合（式 5，L144）。
5. **ACO 与 Dijkstra 混合降规模**：L303 once one ant goes into the terrestrial network, the ant will stop to search and finish the remaining path determined by Dijkstra algorithm。
6. **Tabu 表的跨域重置规则**：L227 once the ant has visited the node in the terrestrial network, all the nodes in satellite network should be registered in the tabu list.

### 3.5 是否已被 RL 论文采用

**被 2 篇 T1 学习型路由论文引用。**

全库检索模式 fragment-aware routing|ACO-EFPC，命中文件 = 8N9QJHC2 CYMQ2GLA PIXWFHAC R37BNQQ8。

| 引用方 | 性质 | 行号 | 逐字 |
|---|---|---|---|
| 8N9QJHC2 | T1（Q-learning 恢复路由） | L382 | [3] Q. Guo, R. Gu, T. Dong et al., "SDN-based end-to-end fragment-aware routing for elastic data flows in LEO satelliteterrestrial network," IEEE Access, vol. 7, pp. 396–410, 2019. |
| PIXWFHAC | T1（RL 路由） | L523 | [36] Q. Guo, R. Gu, T. Dong et al., "SDN-based end-to-end fragment-aware routing for elastic data flows in LEO satellite-terrestrial network," IEEE Access, vol. 7, pp. 396– 410, 2019. |

**如实登记的不确定项**：CYMQ2GLA 亦被该模式命中，但定位到的行（L375，Qu et al. IoT 条目）**不含命中片段**，疑为超长行合并所致；**本条不作承重声明**。

### 3.6 实验合同里与「负载」相关的设置（仅作实验条件登记，不作贡献）

- 星座（L344 Table 1 逐字）：Configuration π / Inclination,(θ) 86.4° / Number of Satellites,(H) 66 / Number of Orbits, (M) 6 / Number of Satellite/Orbit, (N) 11 / Phasing Factor, (PF) 0 / Altitude, (Unit:km) 780 / ISL 2 intra/2 inter / ISL state Non-permanent / Elevation Angle 8.2°
- 链路（L354 Table 2 逐字）：λ^s = 800Mbps / W = 3 / B_s = 2400Mbps / λ^st = 960Mbps / U = 3 / B_st = 2880Mbps
- L358 we assume that the processing time of the node in G(t) is static and set it to 100 μs.
- **负载=合成流请求，均匀分布**：L370 We create 300 elastic data flow requests, each data flow owns one endpoint which is randomly selected in the worldwide and another endpoint which is in the terrestrial network. Meanwhile, we supposed both the MSB and CRB of these data flows are subject to average distribution as the average value are 150Mbps and 75Mbps, which are the common parameters.
- 负载扫描：L378 setting different numbers of services from 30 to 180 with an interval of 30；we set the upper limit to 180 because it has reached the capacity of the ISTN.
- L372 We put these flow requests into 20 consecutive time slices
- **负载=无过程族、无突发**：流在 20 个时间片内静态存在，无到达过程。
- 环境：L364 the simulation of ACO-EFPC is simulated by using MATLAB.

### 3.7 该文自述的局限（逐字）

- L439：the ACO-EFPC has got an advantage in bandwidth fragment, bandwidth utilization, and load balancing, only with little inferior in latency while network load is high. For any fixed number of data flows, the indicators are changed over time. Though we do not simulate the ACO-EFPC in every time slice, the corresponding indicators are statistically advantageous.
- L387：In general, the average latency of data flows using ACO-EFPC is 7.52% lower than that using Dijkstra algorithm.；L394 the average latency using ACO-EFPC is a little higher than that using SADR, with the gap is shrinking as the data flows increases
- L266/L268（两条简化假设逐字）：First, as the transport capacity of the terrestrial network is much larger than that of the satellite network, we assume that the data flows in ISTN have negligible influence on terrestrial network segment of routes, what means we only consider the latency in the terrestrial network.；Second, as the links between the satellite network and terrestrial network are limited, and the capacity of ISTN is limited by the capacity of the available STLs, we assume that one data flow in ISTN only transports through one STL and transport through the STL once, what is pretty obvious.
- L129 our algorithm for routing is based on the unified management of ISTN, and is independent on the way to achieve unified management.

### 3.8 该文没有考察的算法选择（基于 3.1–3.6 判定）

- **无学习成分**（§3.3 实测）；ω 权重手工设定，无双层优化、无自动调参。
- **无失败成因区分**：Algorithm 2 只在链路消失时重算（L317 if e(i,j) in G(t_a) equals to 0 then），**不区分链路故障 / 容量不足 / 排队溢出**，全走同一重路由分支。检索 Y_dropcause，实测 **R37BNQQ8 = 2**；逐条核验：L198 与 L238 命中的都是 **MSB overflow factor η(t)**（式 8）——它是加权和 Θ 中的一个**代价类型项**（轴 = 代价类型），且属**启发式而非学习梯度**，**不构成 G-A 的学习通道/惩罚项分解**。
- **无逐包决策、无动作驻留建模**：动作一经下发驻留至路径不可用（L376）。

---

## 4. 2W8BJ7ME — A Load Balancing Routing Strategy for LEO Satellite Network（SIDA / SSLB）

### 4.1 机制公式（逐字）

- L60（式 1，逻辑位置）：
  \left\{ { \begin{array} { l } { k = \left[ { \frac { i } { m } } \right] } \\ { r = i m o d m } \end{array} } \right.\tag{1}
- L63（**拥塞判据**，逐字）：If node i and node j are adjacent nodes(i ≠ j , i , j ∈ [ O , N - I ] ) and ISL exists between node i and node j , E^(i)(j) stands for the remaining bandwidth of the link between the two nodes. Assuming that the communication between node i and nodej shares one communication channel, the threshold value of ISL residual bandwidth is set as Q_threshold .. When E^(i)(j) < Q_threshold ,, the ISL is considered to occur congestion. When calculating the routing path, all ISL link weights are considered to be the same.
- L74（**SIDA 机制一：遍历序反转**，逐字）：SIDA changes the traversal mode in Dijkstra algorithm, from positive order to reverse order, the larger numbered nodes can be given more priority to increase the utilization rate. In order to ensure the utilization rate of nodes with different numbers is as equal as possible, in SIDA algorithm, when the destination node number is larger than the source node, the second traversal adopts positive order traversal. And when the destination node number is smaller than the source node, the second traversal adopts reverse order traversal.
- L76（**SIDA 机制二：重复使用节点加权惩罚**，逐字）：In order to avoid multiple routing paths to select the same node as the next hop, SIDA algorithm deals with the nodes that are repeatedly used. If a node is already used in a path, the weight of the source node to this node should be increased. In this way, the node can be avoided from being selected again in the next routing path calculation, so that other alternative shortest paths can be generated without an increase of hop.
- Algorithm 1（L100–L126）：逐包下一跳选择伪码。关键分支逐字：L107 If congestion link is the same track link:；L109 If kd == kc → n = max(EAC, EBC)；L111 Else if kd > kc: → n = (kc+1, r)；L113 Else: → n = (kc-1, r)；L117 If congestion link is adjacent track link:；L119 If rd == rc: → n = max(EAC, EBC)。
- L128（跳数不变性论证，逐字）：if the link between node (k, r+1) is congested, the neighbor node (k, r-1) can't accept the shunted traffic flow. Because it will inevitably lead to an increase in the minimum number of hops by two. Therefore, this type of neighbor node should not be used.
- L141（式 2，**小流量节点分流比**）：
  \alpha = \overline { { \frac { E ^ { X P } - Q _ { t h r e s h o l d } } { F ^ { x } } } }\tag{2}
- L147（式 3）：( 1 - \alpha ) F ^ { x }\tag{3}
- L155（式 4，**大流量节点分流比**）：
  \beta = \frac { E ^ { Y Q } - Q _ { t h r e s h o l d } } { F ^ { y } }\tag{4}
- L161（式 5）：( 1 - \beta ) F ^ { y }\tag{5}
- L168（复杂度）：Computational complexity: SSLB uses the residual bandwidth and the value of traffic flow to calculate the ratio of shunted traffic, and the time complexity is O ( I )
- L170（信令复杂度）：the node periodically detects the remaining bandwidth between the neighbor nodes. The congested node only needs one signaling interaction to determine the neighbor node that can accept the shunted traffic. The complexity of signaling interaction is lower.

### 4.2 决策粒度

**SIDA：快照级（离线）**，为每个拓扑快照计算全网路由表；**SSLB：拥塞事件触发 + 逐包级下一跳改选**。

- L26：The operation period of LEO satellite can be divided into several time slices. In each time slice, the network topology is different and is considered static, which is called topology snapshot. The central node calculates the routing paths of all topology snapshots and uploads them to the satellite node. The nodes execute synchronously and switch periodically.
- L86：SSLB is a distributed load balancing strategy that uses the route path calculated by the snapshot sequence algorithm. After the link congestion occurs, the traffic of the congestion node is shunted to the neighbor nodes.
- L134：The satellite nodes at both ends of the congestion link is recorded as X and Y. When the traffic is shunted, in order to ensure that the ISL between the congested node and the neighbor node will not congest again, the value of shunted traffic needs to be limited. Therefore, the congested node with a small traffic is preferred for diversion.
- **动作带触发条件**：仅在 E < Q_threshold 时改选下一跳；正常态沿用快照路由。

### 4.3 是否含学习成分

**否。**

- 检索 X2_anylearning_all，实测 **2W8BJ7ME = 0**。
- 检索 T2_discount_clean，实测 **2W8BJ7ME = 0**。
- 机制全部为 Dijkstra 变体 + 阈值判据 + 线性比例分流。

### 4.4 可迁移点（含公式）

1. **「用遍历序打破对称性」以均摊链路使用**——针对高对称栅格拓扑的**零成本负载均衡**技巧。
   - L67（动因，逐字）：the topology of LEO network is similar to a symmetrical grid, which induce to the load balancing inefficiency of the traditional Dijkstra algorithm, since multiple shortest paths from the same node may use the same link.
   - L80（量化，逐字）：we use a 19 × 9 grid as an example. The number on the node identifies the number of times the node has been used by the path after running the algorithm. In Dijkstra's algorithm, the upper left part of the node is used is obviously greater than the lower right part nodes. In SIDA, the whole network is relatively evenly used.
   - **迁移**：若用静态路由做 baseline，需先做等价的对称性破除，否则 baseline 会被系统性低估。
2. **「重复使用即加权」的隐式拥塞惩罚**（L76）——无需全局状态、无需通信的分布式拥塞避让近似。**迁移**：可作 RL 动作掩码/惩罚的廉价先验。
3. **分流比例闭式解（式 2/4）**——把「分多少」写成剩余带宽裕量与当前流量之比：
   - α = (E^{XP} − Q_threshold)/F^x（式 2，L141）；β = (E^{YQ} − Q_threshold)/F^y（式 4，L155）。
   - 分两步、从小到大：L134 the congested node with a small traffic is preferred for diversion. If the congestion cannot be solved, then consider the diversion of large traffic nodes.
   - **迁移**：可作「拥塞缓解动作幅度」的解析 baseline。
4. **分流后跳数不变性的证明思路**（L128）：牺牲 2 跳换负载均衡的上界保证。
5. **高低纬度可用性差异**（L94，逐字）：SSLB reduces the link congestion in the low latitude area. In order to reduce packet jitter after shunting, the strategy needs to ensure the minimum hop number of the routing path will not increase too much after shunting. In the low latitude area, and the topology is a highly symmetrical and uniform grid. There are multiple equivalent shortest paths between the source node and the destination node. After the traffic is divided into neighbor nodes, the minimum number of hops increases by two at most. However, ISL is disconnected between satellites in adjacent orbits in high latitude. If there is congestion in the high latitude area, it must be the link in the same orbit. At this time, there is almost no equivalent multipath route. Therefore, SSLB will play a better role at low latitudes.

### 4.5 是否已被 RL 论文采用

**被 2 篇 T1 学习型路由论文引用。**

全库检索模式 a load balancing routing strategy for LEO，命中文件 = 2W8BJ7ME 36RZKNW5 K7U4TYJN PIXWFHAC T9X6QCLL X5Z98UPM。

| 引用方 | 性质 | 行号 | 逐字 |
|---|---|---|---|
| PIXWFHAC | T1（RL 路由） | L503 | [26] J. Liu, R. Z. Luo, T. Huang, and C. W. Meng, "A load balancing routing strategy for LEO satellite network," IEEE Access, vol. 8, pp. 155136–155144, 2020. |
| X5Z98UPM | T1（DRL 负载均衡路由） | L394 | 26. Liu, J.; Luo, R.; Huang, T.; Meng, C. A Load Balancing Routing Strategy for LEO Satellite Network. IEEE Access 2020, 8, 155136–155144. [CrossRef] |

### 4.6 实验合同里与「负载」相关的设置（仅作实验条件登记，不作贡献）

- 星座（L176–L185 逐字）：Each satellite node has four ISLs, including two same orbit links and two adjacent orbit links.；The constellation has six orbital planes and 54 satellites. Nine satellites are evenly distributed on each orbital plane.；When the latitude position of the satellite is higher than 60°, the adjacent orbit link will be disconnected.；This constellation is polar orbit. The orbit has no angular deflection at the pole.
- 快照参数（L189–L195）：There are 54 satellites, numbered from 1 to 54. Set node 1 at the North Pole of the eastern hemisphere at 90°N；The same orbit satellite is connected end to end. The latitude difference between adjacent satellites in the same orbit is 40°；The latitude phase difference of adjacent orbital links is ±20.
- **负载模型（关键，逐字）**：L197 Some traffic flows have higher requirements for link bandwidth but are less sensitive to delay, such as large file transmission. Generally, this type of traffic flow accounts for 10% of the total flow but accounts for 80% of the bandwidth. However, some traffic flows are sensitive to the transmission delay, but occupy a smaller link bandwidth, such as voice calls and so on. In order to simulate different traffic flows in LEO network, we generation the traffic distribution in Gamma distribution.
- 流量条目定义（L204–L210）：Source node(S): source satellite node mapped by user IP; / Destination node(D): the final hop satellite node of the destination IP mapping of the traffic flow; / Value of traffic flow(F): traffic value of each traffic flow; / The traffic flow paths of different users are different.
- 负载强度扫描：L222 Under [20], [64] group traffic flow；L245 In this simulation, [20], [59] traffic flows are selected and divided into four groups on average.
- **负载=Gamma 分布静态流量组，无到达过程、无时间相关性**。
- 评价指标：L214 We take the residual bandwidth of link and the average number of congested links as the indexes；L257 If the standard deviation of the remaining bandwidth of the link under SIDA is smaller than Dijkstra algorithm, it shows better load balancing ability.

### 4.7 该文自述的局限（逐字）

- L94：SSLB will play a better role at low latitudes. Overall, it will also alleviate the congestion that appears in LEO network.（自承高纬受限）
- L245（自设成功判据，隐含边界）：SSLB should reduce the number of all link congestion in LEO network. So it should meet the requirements of F < C , G < D .
- L272（**SSLB 反而不如 SIDA 的自述负面结果**）：As shown in Figure 11 and Figure 12. Under six traffic flows, the standard deviation of LCRA residual link bandwidth is much larger than SSLB when the traffic value is small. And the standard deviation of the remaining link bandwidth of SSLB is almost always greater than SIDA. With the increase of traffic flow, the difference between the two algorithms increases.

### 4.8 该文没有考察的算法选择（基于 4.1–4.6 判定）

- **无学习成分**（§4.3 实测）。
- **无失败/丢包成因区分**：全文唯一状态量是链路剩余带宽与比较阈值 Q_threshold（L63）。检索 Y_dropcause 实测 **2W8BJ7ME = 0**。
- **无动作时间结构的显式建模**：分流是即时的，没有「延迟分流/驻留窗口」概念。

---

## 5. 7TASFUDR — Available energy routing algorithm considering QoS requirements（AER）

> **特别说明（任务点名）**：本篇是本批唯一以**能量**为主轴的工作，与「负载」的关系链是「负载 → 转发功耗 → 可用能量 → 节点休眠 → 丢包」。其信用分配轴是**能量状态**而非负载，如实登记。

### 5.1 机制公式（逐字）

- L71（式 1，**流量相关功耗，三项**）：
  P _ { f l o w } ^ { i } = \sum _ { \langle i j \rangle \in E } \alpha \cdot ( f _ { i j } + f _ { j i } ) + \mu \cdot ( f _ { i j } + f _ { j i } ) ^ { \sigma } + f _ { i j } \cdot P _ { s } + f _ { j i } \cdot P _ { r }\tag{1}
- L77（式 2，**总功耗三分量**）：P _ { d } ^ { i } = P _ { n o r m } ^ { i } + P _ { f l o w } ^ { i } + P _ { d v c } ^ { i }\tag{2}
- L83（式 3，**电池状态转移**）：C _ { i } ^ { t + 1 } = C _ { i } ^ { t } + m i n ( P _ { B } ^ { + } , ( P _ { s u n } ^ { i } - P _ { d } ^ { i } ) )\tag{3}
- L87（式 4）：0 < C _ { i } ^ { t } < C _ { i } ^ { m a x }\tag{4}
- L99（式 5，**可用能量定义——本文核心机制**）：
  E _ { a v a } ^ { i } = \left\{ \begin{array} { l l } { C _ { i } ^ { t } - P _ { d v c } \cdot { A T _ { e } ^ { i } } - P _ { n o r m } \cdot { A T _ { u } } } & { i f : A T _ { e } ^ { i } > 0 } \\ { C _ { i } ^ { t } + ( P _ { s u n } ^ { i } - P _ { d v c } - P _ { n o r m } ) \cdot { A T _ { u } } } & { o t h e r w i s e } \end{array} \right.\tag{5}
- L113（式 6，**丢包率定义——本文唯一失败度量**）：
  R _ { l o s t } = \frac { \sum _ { s , d \in V , s \neq d } \delta _ { s d } ^ { E } \cdot f _ { s } ^ { d } } { \sum _ { s , d \in V } f _ { s } ^ { d } , s \neq d } \mathrm { ~ , ~ } \langle i j \rangle \in P a t h _ { s d }\tag{6}
- L119（式 7，**丢包二元指示器——是「有无」而非「何因」**）：
  \delta _ { s d } ^ { E } = \left\{ \begin{array} { l l } { 1 } & { , i f : E _ { a v a } ^ { i } = 0 \mathrm { ~ a n d ~ } i \in p a t h _ { s d } } \\ { 0 } & { , o t h e r w i s e } \end{array} \right.\tag{7}
- L125（式 8，端到端时延）：
  T _ { s d } = \sum _ { \langle i j \rangle \in P a t h _ { s d } } ( \frac { d _ { i j } } { v } + \frac { q _ { i } \cdot P _ { a v g } } { B _ { i j } } ) \ , s d \in V , s \neq d\tag{8}
- L131（式 9，流守恒）：\sum _ { \langle i j \rangle \in E } f _ { i j } ^ { d } - \sum _ { \langle i j \rangle \in E } f _ { j i } ^ { d } = f _ { i } ^ { d } , i \neq d , d \in V\tag{9}
- L137（式 10，**三目标加权和**）：
  m i n : \theta _ { 1 } \cdot R _ { l o s t } + \theta _ { 2 } \cdot \sum _ { s , d \in V , s \neq d } T _ { s d } - \theta _ { 3 } \cdot \sum _ { i \in V } E _ { a v a } ^ { i }\tag{10}
- L145（式 12）：\theta _ { 1 } + \theta _ { 2 } + \theta _ { 3 } = 1\tag{12}
- L173（式 16，**低时延业务链路权，含能量惩罚项**）：
  W _ { i j } ^ { d } = T _ { i j } + \delta _ { i } ^ { E } \frac { 1 } { E _ { a v a } ^ { i } } + \delta _ { j } ^ { E } \frac { 1 } { E _ { a v a } ^ { j } }\tag{16}
- L179（式 17，**「即将耗尽」= 2 个时间片余量**）：
  \delta _ { i } ^ { E } = \left\{ \begin{array} { l l } { 1 } & { , i f : \frac { E _ { a v a } ^ { i } } { P _ { f l o w } ( t _ { i } ^ { m a x } ) } < 2 \cdot \Delta T _ { u } } \\ { 0 } & { , o t h e r w i s e } \end{array} \right.\tag{17}
- L189（式 18，**高带宽业务链路权 = 归一化剩余带宽倒数 + 归一化能量状态倒数**）：
  W _ { i j } ^ { b } = \frac { B _ { r e s } ^ { m a x } - B _ { r e s } ^ { m i n } } { B _ { r e s } ^ { i j } - B _ { r e s } ^ { m i n } } + \frac { \hat { E } _ { e l p s } ^ { m a x } - \hat { E } _ { e l p s } ^ { m i n } } { \hat { E } _ { e l p s } ^ { i j } - \hat { E } _ { e l p s } ^ { m i n } }\tag{18}
- L197（式 19，**未来能耗预估——把未来流量期望折进当前状态**）：
  E _ { e f } ^ { i } = P _ { n o r m } \cdot { \varDelta } T _ { e } ^ { i } + \sum _ { k \in a r e a _ { i } } P _ { f l o w } ( \mu _ { k } ) \cdot { \varDelta } T _ { i k }\tag{19}
- L203（式 20，**改进可用能量**）：
  E _ { e l p s } ^ { i } = \left\{ \begin{array} { l l } { E _ { a v a } ^ { i } - E _ { e f } ^ { i } } & { i f : \Delta T _ { e } ^ { i } > 0 } \\ { E _ { a v a } ^ { i } } & { o t h e r w i s e } \end{array} \right.\tag{20}
- L213（式 21，链路能量状态）：\hat { E } _ { e l p s } ^ { i j } = \frac { E _ { e l p s } ^ { i } - E _ { e l p s } ^ { m i n } } { E _ { e l p s } ^ { m a x } - E _ { e l p s } ^ { m i n } } + \frac { E _ { e l p s } ^ { j } - E _ { e l p s } ^ { m i n } } { E _ { e l p s } ^ { m a x } - E _ { e l p s } ^ { m i n } }\tag{21}
- L223（式 22，**通用业务链路权**）：
  W _ { i j } ^ { g } = \frac { 1 } { B _ { r e s } ^ { i j } } + \delta _ { i } ^ { E } \cdot \frac { 1 } { E _ { a v a } ^ { i } } + \delta _ { j } ^ { E } \frac { 1 } { E _ { a v a } ^ { j } }\tag{22}
- L275（式 23，**休眠判据**）：
  \delta _ { s l p } ^ { i } = \left\{ \begin{array} { l l } { 1 } & { i f : E _ { a v a } ^ { i } < P _ { f l o w } ( t _ { i } ^ { m a x } ) \cdot \varDelta T _ { u } } \\ { 0 } & { o t h e r w i s e } \end{array} \right.\tag{23}
- Algorithm 1（L230–L249）：输入 𝑡𝑜𝑝𝑜, 𝑛𝑜𝑑𝑒_𝑒𝑛𝑒𝑟𝑔𝑦, 𝑡𝑚，输出 p a t h _ { d } , p a t h _ { b } , p a t h _ { g }；三步顺序 Dijkstra（L237 𝑝𝑎𝑡ℎ ← dijkstra(𝑡𝑜𝑝𝑜, 𝑐𝑜𝑠𝑡^𝑑)；L243 𝑝𝑎𝑡ℎ ← dijkstra(𝑡𝑜𝑝𝑜, 𝑐𝑜𝑠𝑡^𝑏)；L248 𝑝𝑎𝑡ℎ ← dijkstra(𝑡𝑜𝑝𝑜, 𝑐𝑜𝑠𝑡^𝑔)）。

### 5.2 决策粒度

**per-(source, destination) per-time-slot 的单路径**，按业务类型分三条独立路径集。

- L228：The algorithm operates by selecting decision factors based on the specific requirements of multiple services. These decision factors are then converted into link weights, which are used to determine the minimum cost path set via the Dijkstra algorithm.
- L164：This paper divides network services into low-latency services, high-bandwidth services and general services.
- **三类业务共享同一拓扑但用三套权重**（式 16/18/22），且**顺序求解并传递链路利用率**：L251 the algorithm assigns weights to each link through (16) based on the network topology and available energy status, obtains the path for low-latency type services, and distributes this type of traffic through the path to obtain the link utilization rate. In lines 7 to 12, using the previously obtained link utilization rate and improved available energy, (18) is used to assign link weights
- 时间片：L64 A virtual topology strategy is employed to divide time into equal-length time slots with the assumption that topology remains constant within each time slot.
- **动作带驻留**：路径在时间片内固定（L263 In each period, the topology is regarded as constant.）。

### 5.3 是否含学习成分

**否。纯启发式最短权路径。**

- 检索 X2_anylearning_all，实测 **7TASFUDR = 4**。
- **逐条核验 4 个命中（命中的都是他文引用或未来工作，不是本文方法）**：
  - L27：DRL-ER [7] introduced a deep reinforcement learning-based routing approach that incorporates delay and discharge depth factors in the reward formulation. However, this method consumes a substantial number of computational resources.（**引用他人**）
  - L346：in our future work, we will jointly consider the data flow size and the available energy status of satellites, and employ reinforcement learning and multipath routing techniques to dynamically generate multiple paths for nodes on congested links（**未来工作**）
  - L382：参考文献 [9] Xiaojing Shi, Pinyi Ren, Qinghe Du, Reinforcement learning routing in space-airground integrated networks（**参考文献**）
  - L404：参考文献 [20] Mitigating routing update overhead for traffic engineering by combining destinationbased routing with reinforcement learning（**参考文献**）
- 检索 T2_discount_clean，实测 **7TASFUDR = 0**。
- **结论：本文不含任何学习成分；"reinforcement learning" 在本文中出现 4 次，0 次属于本文方法。**

### 5.4 可迁移点（含公式）

1. **「可用能量」= 剩余能量 − 固定开销 × 剩余不利时长**（式 5，L99）。这是把**未来必然损失**折进**当前状态量**的通用模式。**对我们方案的意义：状态里可以合法地放「未来必然代价」的预测，而不必等它发生。**
   - L102（逐字解释）：When ΔT_e > 0 , indicating that satellite 𝑖 is within the eclipse region, its solar panels are rendered almost incapable of generating energy. As a result, the satellite must rely solely on the energy stored within its batteries, undergoing a continuous discharge process. By leveraging the periodic characteristics of satellite topology, the remaining eclipse time ΔT_e can be predicted and the energy consumption of other devices in the eclipse region can be calculated as P_dvc · ΔT_e .
2. **「未来流量期望」进当前决策**（式 19，L197）——把**历史/预测流量**（μ_k = 区域流量数学期望）与**未来连接时长**（ΔT_ik）卷积成能耗惩罚。L192 逐字给出方法论：considering the regularity of traffic [19], we can statistically analyze the daily traffic trends in global areas to obtain the mathematical expectation of traffic size in each area at any time. At the same time, using the periodicity of satellite topology, we can obtain the future connection relationship and connection time between satellites and ground areas.
   - **这是本批唯一把「负载的时间规律性」显式写进状态的工作**，对「状态里有没有时间信息」这一问题有直接正面价值。
3. **「即将耗尽」用相对余量而非绝对阈值判定**（式 17，L179）：E_ava^i / P_flow(t_i^max) < 2·ΔT_u，即「按当前最大负载速率，能源撑不过 2 个时间片」。**迁移**：我们方案的「链路即将拥塞」可用同构判据「剩余队列 / 当前入队速率 < k·Δt」。
4. **按业务类型切换决策因子的三套权重**（式 16/18/22），且**能量只在必要时才进入权重**：
   - L170：When the energy of the nodes at both ends of the link are sufficient, the link weight is determined by the delay on that link. If the energy state of the nodes at both ends of the link is poor, the energy state is incorporated into the calculation of link weight
   - **迁移**：这是「条件激活的惩罚项」（gate 由 δ^E 控制），可作「只在拥塞时才激活拥塞惩罚」的设计模板。
5. **休眠作为显式动作**（式 23；L272 逐字）：When the available energy is less than the threshold, it is considered that the satellite has entered a state where its energy is about to be exhausted. At this time, it is necessary to set the satellite to sleep mode, stop the space router of the satellite, and only keep the necessary device outside of routing functions working.
6. **归一化处理负值**（L206）：Since the improved available energy may have negative values, normalization is necessary to represent the energy state of the link.

### 5.5 是否已被 RL 论文采用

**全库检索未见。** 模式 available energy routing algorithm，实测命中文件 = 7TASFUDR 自身（1 个）。

（对比：本批的 67CSKFK4 / YD4JUT7G / K93SCUF2 被大量 RL 论文引用；本篇作为较新的能量文献尚未进入引用网络。）

### 5.6 实验合同里与「负载」相关的设置（仅作实验条件登记，不作贡献）

- 星座（L263 逐字）：We build Walker Constellation consisting of 6 orbits and 5 satellites spreading evenly in each orbit in STK. Thus there are 30 satellites in total. The orbital altitude is 1325 km, the inclination is 70°, and the orbital period is 112 min. We set 12 ground stations [21] around the world to simulate data communication among big cities.
- 时间：L263 We recorded the topology every 1 min, and the simulation time was 2 h, with 120 time slots in total.
- 能量参数（L257 Table 2 逐字）：Battery Capacity 80 Wh / Receiver Power 0.02 W/Mbps / Sender Power 0.05 W/MBps / Maximum Power of Solar Panel 800 W / Maximum Charging Power 400 W / Processor Power 50 W / Power of Other Device 50 W
- **负载模型（关键，逐字）**：L265 To simplify the calculation to a certain extent, we only divide the ground region into ordinary area and ground station area. The mathematical expectation of the traffic size in the ordinary area is set to 0, and the mathematical expectation of the traffic size in the ground station area is always set to 512Mbps. In practical applications, the mathematical expectation of the traffic size can be obtained by statistically analyzing the traffic in different areas at different time periods.
- **负载合成（本批少见的显式过程建模）**：L278 Considering that time and space constraints should be considered in traffic synthesis, we use MGM [19,20] to synthesize traffic matrix for 120 min. We set the maximum threshold of uploaded traffic in each area to 1Gbps, the average traffic value to 512Mbps, traffic hourly peak-to-mean ratio to 1.5.
- 初始能量：L286 The initial satellite energy is uniformly set to 100%.；L302 we set the initial energy of the satellite to 70% at the start of the simulation, then employ the sleep strategy
- 基线：L282 We evaluate the performance of the proposed AER algorithm by comparing it with the QoS-SR [15] and Green-SR [14] algorithms.

### 5.7 该文自述的局限（逐字）

**本文局限自述质量高，逐字如下：**

- L346：The approach proposed in this paper primarily considers energy and link bandwidth factors when forwarding high-bandwidth class traffic. It generates a single path for each pair of source and destination satellites, causing a large amount of data to aggregate on a few paths, resulting in significant end-to-end delay for this type of traffic. Therefore, in our future work, we will jointly consider the data flow size and the available energy status of satellites, and employ reinforcement learning and multipath routing techniques to dynamically generate multiple paths for nodes on congested links, thereby reducing congestion levels and network packet loss in satellite networks.
- 自述负面结果（L306）：the end-to-end delay of the AER algorithm is worse than that of the QoS-SR algorithm, with an average increase of 28%. However, it is comparable to the Green-SR algorithm, with an average difference of only 1.07%. This is because when forwarding high-bandwidth services, AER algorithm consider both the energy status of adjacent nodes and remaining link bandwidth as decision factors. However, a link with better energy status may not necessarily have the minimum delay.
- 自述负面结果（L332）：The AER algorithm increases minimum energy by up to 4.81% compared to QoS-SR and reduces it by up to 30.14% compared to GreenSR.
- 自述负面结果（L340）：under multiple service traffic, both AER and QoS-SR algorithms have higher cycle life consumption than the GreenSR algorithm, increasing by 188% and 221%, respectively.

### 5.8 该文没有考察的算法选择（基于 5.1–5.6 判定）

- **无学习成分**（§5.3 已实测，4 个 reinforcement learning 命中全部为他文/未来工作）。
- **丢包不做成因区分**：式 6/7（L113/L119）把**所有**丢包压成单一标量 R_lost，且指示器 δ_sd^E 只判「路径上是否存在可用能量为 0 的节点」——即**只认「能量耗尽」这一种丢包原因**，链路故障、队列溢出、无路由均不在此模型内。检索 Y_dropcause，实测 **7TASFUDR = 0**。
- **无逐包决策**：源宿对级单路径（L346 自述 It generates a single path for each pair of source and destination satellites）。
- **无动作掩码**：仅用权重惩罚（式 16/18/22）软性避让。

---

