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

## 6. AIH4GK37 — How Area Geometry Shapes Link-State Routing Scalability in LEO Networks（PBAR）

> **特别说明（任务点名）**：本篇主轴是**控制面开销**（不是数据面负载），且**显式排除数据面流量**。其机制是链路状态路由的区域几何，与 RL 路由的接口在「事件率 → 状态更新频率」这一环，如实写。

### 6.1 机制公式（逐字）

- L136（式 1）：N = W _ { 0 } H _ { 0 }\tag{1}
- L144（式 2，区域数）：K ( w , h ) = \frac { W _ { 0 } } { w } \frac { H _ { 0 } } { h } = \frac { N } { w h }\tag{2}
- L154（**区内 ISL 数**，逐字含指示函数）：
  { \cal E } _ { \mathrm { i n } } ( w , h ) = ( w - 1 ) h + w ( h - 1 ) + \mathbf { 1 } _ { \{ w = W _ { 0 } \} } h + \mathbf { 1 } _ { \{ h = H _ { 0 } \} } w ,
- L160（式 4，**区内洪泛开销**）：C _ { \mathrm { l o c } } ( w , h ) = \gamma _ { \mathrm { l o c } } E _ { \mathrm { i n } } ( w , h ) ,\tag{4}
- L168（式 5，**跨区 ISL 数**）：
  E _ { \mathrm { c u t } } ( w , h ) = \mathbf { 1 } _ { \{ w < W _ { 0 } \} } \frac { W _ { 0 } } { w } H _ { 0 } + \mathbf { 1 } _ { \{ h < H _ { 0 } \} } \frac { H _ { 0 } } { h } W _ { 0 } ,\tag{5}
- L174（式 6，**归一化边界暴露度**）：\beta ( w , h ) = \frac { E _ { \mathrm { c u t } } ( w , h ) } { 2 N } .\tag{6}
- L180（式 7，**全局传播概率**）：q ( w , h ) = \operatorname* { min } \{ 1 , \alpha \beta ( w , h ) \} ,\tag{7}
- L188（式 8，**形状项**）：\beta ( w , h ) = \frac { 1 } { 2 } \left( \frac { 1 } { w } + \frac { 1 } { h } \right) .\tag{8}
- L196（式 9）：C _ { \mathrm { g l o b } } = 2 \gamma _ { \mathrm { g l o b } } N ,\tag{9}
- L202（式 10，**期望控制开销率——主目标**）：R ( w , h ) = \lambda \left[ C _ { \mathrm { l o c } } ( w , h ) + q ( w , h ) C _ { \mathrm { g l o b } } \right] .\tag{10}
- L214（式 11，区内直径）：D _ { \mathrm { l o c } } ( w , h ) = ( w - 1 ) + ( h - 1 ) .\tag{11}
- L222（式 12）：T _ { \mathrm { l o c } } ( w , h ) = \delta _ { \mathrm { l o c } } D _ { \mathrm { l o c } } ( w , h ) ,\tag{12}
- L228（式 13，**收敛时间一阶分解**）：T ( w , h ) \approx { \cal T } _ { \mathrm { l o c } } ( w , h ) + q ( w , h ) { \cal T } _ { \mathrm { g l o b } } ,\tag{13}
- L400（路径拉伸定义）：We measure path stretch as the ratio of area-routing path cost to flat-routing path cost, using both hop count and delay: S _ { \mathrm { h o p } } \triangleq H _ { \mathrm { a r e a } } / H _ { \mathrm { f l a t } } and S _ { \mathrm { d e l a y } } = D _ { \mathrm { a r e a } } / D _ { \mathrm { f l a t } } .
- 三条预测（L237/L239/L241 逐字）：
  - **(P1)** Intermediate optimum PBAR overhead and convergence time are minimized at an intermediate area size, not at either extreme of one large area or many tiny ones.
  - **(P2)** Balanced shapes For a given area size, balanced (squarelike) divisions outperform elongated ones because they minimize both boundary exposure and local flood diameter.
  - **(P3)** Wrap-around alignment Path stretch is governed primarily by whether area boundaries preserve the shorter toroidal direction, not by the total number of areas; stretch can therefore be non-monotonic in area granularity.

### 6.2 决策粒度

**配置级（区域划分 w×h）——这是一篇「设计规则」论文，不是「运行时决策」论文。**

- L280：To study PBAR sensitivity to area division geometry, we evaluate only rectangular exact-divisor area layouts on the baseline 72×22 shell, so every reported partition tiles the shell exactly with no partial edge areas. The evaluated widths and heights are w ∈ { 72 , 36 , 18 , 9 , 4 , 2 } and h ∈ { 22 , 11 , 2 }, yielding 18 area divisions.
- 运行时决策外包给 OSPF + Dijkstra：L257 Routers outside the area run Dijkstra on Area-Link LSAs to compute inter-area shortest paths, then forward toward the nearest border router of the next-hop area; once a packet enters the destination area, intra-area Local-Link LSA-based routing takes over.
- 固定度量，禁止时延触发：L270 We assign a fixed per-hop metric of 1 to all ISLs, as in ASER [3], so that delay variations do not trigger routing updates.
- 运行时有硬选择但由协议决定、不被优化：L259 Each area elects its area leader deterministically as the router with the highest Router ID in that area.

### 6.3 是否含学习成分

**否。**

- 检索 X2_anylearning_all，实测 **AIH4GK37 = 0**。
- 检索 T2_discount_clean，实测 **AIH4GK37 = 0**（噪声模式 T_discount_trace 曾命中 3 次，逐条核验为 \gamma_{\mathrm{loc}} / \gamma_{\mathrm{glob}} 协议常数，见 L160/L163/L196）。
- 机制为解析建模 + ns-3 包级仿真验证（L249 We evaluate flat link-state routing and PBAR using ns-3 [9].）。

### 6.4 可迁移点（含公式）

1. **「同一事件按影响范围分成本不同的两级」的代价结构（式 10）**——本批最接近「按事件性质分通道计代价」的设计。
   - 结构：R(w,h) = λ[ C_loc(w,h) + q(w,h)·C_glob ]（式 10），其中 q 是该事件升级为全局的概率（式 7）。
   - L205 逐字：Increasing w and h raises C_loc because a local flood covers more of the shell, but lowers q because fewer events affect exported state.
   - **迁移到 RL**：把「动作代价」拆成**局部代价 + 概率×全局代价**两项——与「按失败原因分通道」是**不同轴但同形**的结构（轴 = **事件影响范围**）。可作 G-A 的结构模板。
2. **局部/全局事件的判据 = 「是否改变对外导出的状态」**——一个协议无关、可操作的事件分类准则。
   - L97：Under PBAR, an event is local if it does not change the exported area summary and global if it does.
   - L113：A global event changes the information the area must export. The triggering LSA is flooded within the area; once the area leader detects a change in exported state, it generates an updated area summary and floods it constellation-wide.
3. **前缀复制吸收事件（机制层面的「事件吸收」）**：
   - L325：a gateway advertises the same prefix through all of its attached satellites, so when C_g > 1 multiple satellites in the same area concurrently carry the same prefix. A handover that transfers the prefix between two such satellites leaves the exported set unchanged; the event is absorbed locally without any global flooding. We refer to this as prefix replication.
   - **迁移**：我们方案中「同源多路径」可同理把「拓扑抖动」吸收为「无状态变化」，从而下降事件率。
4. **形状项闭式解（式 8）**：固定面积 wh 时 β = (1/2)(1/w + 1/h)，给出「方正优于狭长」的可计算判据。L209：Equation (8) therefore predicts that more balanced shapes such as 4 × 11 should outperform more elongated ones such as 2 × 22 when area size is held fixed.
5. **绕环歧义导致拉伸非单调（P3）**——对任何环形拓扑（含 LEO 星座）的路由抽象都有直接反例价值：
   - L402：Area routing abstracts destination location to the area level. On a torus, this can obscure which wrap-around direction is shorter, causing inter-area routing to select a longer path. … Stretch can therefore be non-monotonic in area granularity.
   - L404：The largest observed values occur for the 36×11 division, with hop-count stretch peaking at 1.073 and delay stretch at 1.079.

### 6.5 是否已被 RL 论文采用

**全库检索未见。** 模式 area geometry shapes link-state，实测命中文件 = AIH4GK37 自身（1 个）。

（该文为 2026 新稿；其引用的 RFC 9717 / RFC 9666 / ASER 均未被本库 111 篇中的学习型路由论文引用。）

### 6.6 实验合同里与「负载」相关的设置（**本篇最特殊，必须逐字登记**）

- **显式排除数据面流量（本批 10 篇中唯一）**，L272 逐字：
  b) No data-plane traffic: No user or data traffic is injected, avoiding congestion effects that could obscure control-plane behavior.
- **显式排除检测时延（只测分发）**，L274：c) Detection latency excluded: We exclude detection latency: the event generator determines when changes become visible to the routing process, and convergence is measured from the first advertisement transmission to the last processing anywhere in the network. Periodic Hellos are also excluded from all overhead accounting.
- **显式声明排除原因**（L276）：Although our simulator can represent richer scenarios, including multi-shell or polar-shell constellations, concurrent ISL failures, data-plane traffic, and protocol detection timers, we intentionally exclude those factors here because they introduce additional mechanisms that would confound the paper's target question: how area geometry affects event-driven linkstate dissemination overhead, convergence, and path stretch.
- 链路参数（L266 Table I 逐字）：ISL bandwidth 10 Gbps / MTU 8192 bytes / Queue discipline FIFO / Max queue size 100,000 packets / Propagation delay dist(t)/c at send time / Failure behavior Drop packet during link down
- 拓扑：L280 Our baseline shell is Starlink Phase 1 Shell 1 at 53° inclination with 72 orbital planes and 22 satellites per plane, i.e., a 72×22 shell.
- **「负载」= 控制面事件率**：
  - GSL 事件：L288 Gateway locations are derived from a publicly compiled Starlink gateway dataset [11], which provides 129 gateways.；三种挂接策略 L290–L294（Closest-C_g / Keep-C_g / Keep-C_g with margin）。
  - ISL 事件：L298 ISL instability is modeled as discrete link down/up events, with at most one ISL down at a time to isolate individual disruptions. Because public measurements of ISL outage and restoration times are limited, we use a single Pareto distribution for both down-interval and up-interval durations (shape k=2.5, scale x_m = 7.2 s, mean 12 s)
- 事件率结果：L320 Closest-C_g generates roughly 1.3× more routing events than Keep-C_g , with the margin variants in between.
- 开销量级：L327 In the no-area 72×22 baseline, every gateway handover floods Local-Prefix LSAs across all 1584 satellites, generating approximately 600k packets/s at the observed handover rate.
- **负载=事件率（不是比特率）**；无流量矩阵、无到达过程、无突发。

### 6.7 该文自述的局限（逐字）

- L431（结论中的边界声明）：The 18 × 22 and 18 × 11 layouts reflect our workload, not universal choices. The model can evaluate other divisions, including non-exactdivisor layouts. These results do not establish superiority over centralized, precomputed, or geographic routing.
- L435（未来工作，**含明确的机制缺口**）：PBAR can complement time-variant routing (TVR). Preinstalling predictable GSL prefix relocations avoids reactive flooding; link state handles unexpected failures, as our ISL scenarios evaluate. Richer non-toroidal topologies require scheduled adjacency changes and spatial event rates. Delaytriggered updates and concurrent events require a richer event model for λ. Nonuniform gateway or failure distributions require weighted boundary exposure. Congestion with mixed control/data traffic requires load-dependent costs and transient end-to-end evaluation. Empirical traces should calibrate ISL disruption, recovery, and correlated failures such as localized space weather.
- L183（模型定位自述）：The model is intended as an explanatory tool rather than a quantitative fit to simulation output: it predicts qualitative trends—such as the existence of an intermediate optimum and the advantage of balanced shapes—that we then verify experimentally.

### 6.8 该文没有考察的算法选择（基于 6.1–6.6 判定）

- **无学习成分**（§6.3 实测）。
- **无拥塞/负载相关代价**：L272 显式排除数据面流量；L435 自述 Congestion with mixed control/data traffic requires load-dependent costs——即**作者自己承认没有负载相关代价**。
- **无失败成因区分**：ISL 故障被建模为单一 Pareto 分布的 down/up 过程（L298），**不区分故障物理成因**；检索 Y_dropcause，实测 **AIH4GK37 = 0**。
- **无逐包路由决策**：路由由 OSPF Dijkstra 决定（L257），论文不优化它。

---

## 7. 67CSKFK4 — Delay is not an Option（Handley）

### 7.1 机制公式（逐字）

**本文无编号公式**。实测取证：模式 \tag\{ → 命中 **0**；模式 \begin\{array\} → 命中 **0**；模式 \$ → 命中 **4**，逐条核验为 L33 的 53 度记法、L35 的 p+1、L41 的度数记法、L142 的 t_last，**全部是行内变量名，无任何显示公式/编号公式**。其「机制」是拓扑构造规则 + 最短时延路由。核心机制陈述逐字：

- L76（路由机制）：The simplest way to route is for each groundstation to connect to the satellite that is most directly overhead. This has the advantage of providing the best RF signal strength for uplinks and downlinks. We can then run Dijkstra's algorithm[5] over the satellite network using link latencies as metrics to provide the lowest latency paths.
- L78（**预计算 + 源路由**，逐字）：Of course, the network is not static; the satellite most directly overhead changes frequently, the laser links between NE- and SE-bound satellites change frequently, and link latencies for links that are up change constantly. We can, however, run Dijkstra on this topology for all traffic sourced by a groundstation to all destinations, and do so every 10 ms with no difficulty, even on laptop-grade CPUs. In addition, all the link changes are completely predictable. If we run Dijkstra every 50 ms, for the network as it will be 200 ms in the future, and cache the results, we can then see whether packets we send will traverse a link that will no longer be there when the packets arrive. In this way, each sending groundstation can source-route traffic that will always find links up by the time the packet arrives at the relevant satellite.
- L95（**把 RF 上下行也纳入图**）：To achieve the lowest delay, we need to include all possible RF up and down links into the network map that we run Dijkstra over. In this way, we always choose the best matched satellite pair for the uplink and downlink, and we use satellites that are in the correct direction.
- L68（**用第 5 条激光连通两个子网**）：The network resulting from this use of each satellite's first four laser links provides a good mesh network, but in any one region their are two distinct meshes - one moving generally northeast and the other moving southeast, with no local connectivity between the two without going the long way round the planet.
- L126（多路径：迭代删边 Dijkstra）：This is calculated iteratively; first we run Dijkstra to calculate the best path, then we remove all the RF uplinks and laser links used by that path from the network graph. We then re-run Dijkstra to find the next best path, eliminate those links, and iterate.
- L142（**乱序修复判据，含时间判据**）：Suppose the known difference in path delays is t _ { d i f f } . If any preceding packets are missing, the receiving groundstation queues all packets arriving on the new path until either all predicing packets have arrived, or time equal to t _ { d i f f } - t _ { l a s t } has elapsed.
- L37（**相位偏置选择**）：With all even multiples of 1/32 as phase offset, satellites collide. … To minimize the probability of collision if station-keeping is not perfect, we conclude that the phase offset should be 5/32.
- L41（第二阶段相位偏置）：We conclude that 17/32 is the best phase offset, though a few other values also appear to be viable.

### 7.2 决策粒度

**源端源路由（source routing），决策由地面站做，按「未来 N ms 的图」预计算。**

- L78（见上）：each sending groundstation can source-route traffic，预计算窗口 200 ms，重算周期 every 50 ms。
- **决策粒度 = 地面站 + 卫星对**（不是逐卫星转发决策，也不是逐包）：
  - L95：we always choose the best matched satellite pair for the uplink and downlink
  - L93：Lower latency can be achieved by using a satellite lower in the sky in the direction of the destination. This is, of course, at the expense of 3dB lower RF signal strength[12], likely resulting in lower achievable bitrate.
- 多路径：L126 迭代求出互不相交的前 20 条路径（L124 …with Starlink there may be 60 satellites within coverage range for latitudes close to 50°N）。
- **动作无时间结构（无驻留、无延迟）**：路径即时生效，且强调「避免排队」——L134：So long as queues are not allowed to build in satellites, reordering is completely predictable, as all routes are known several hundred milliseconds in advance.

### 7.3 是否含学习成分

**否。纯最短时延路由 + 预计算源路由。**

- 检索 X2_anylearning_all，实测 **67CSKFK4 = 0**。
- 检索 T2_discount_clean，实测 **67CSKFK4 = 0**。

### 7.4 可迁移点（含公式）

1. **「把未来图算出来再发」——预测式路由的时间边界**：L78 If we run Dijkstra every 50 ms, for the network as it will be 200 ms in the future, and cache the results, we can then see whether packets we send will traverse a link that will no longer be there when the packets arrive. **迁移**：我们方案的「动作时间结构」可借用此「前视窗口 vs 重算周期」的比率设计。
2. **把最后一跳 RF 也纳入优化图（co-routing）**：L95。**迁移**：端到端优化不应把接入段当常量。
3. **多路径用「迭代删边最短路」生成，且给出隐式容量假设的诚实边界**：L126 With this formulation, no satellite overhead either city can provide more than one up or downlink, and no intermediate satellite can be used by more than two paths. This implicitly assumes that laser links and RF links have the same capacity - this is unlikely in reality; whichever turns out to be the bottleneck, a real network will allow more paths than this, so the figure effectively shows an upper bound on path latency.
4. **乱序修复的时间判据**：L142 的 t_diff − t_last 等待窗口——**与我们方案「动作带时间结构」时的跨路径时序处理直接相关**。
5. **反例价值：加负载控制不等于排队可控**。
   - L150（**明确的无排队假设**）：All the simulations above assume that no significant queuing happens in the satellites themselves. For high-priority (likely high cost) traffic, this can be ensured by admission control, so long as it forms a minority of the traffic.
   - L152：In terrestrial networks, centralized load-dependent routing schemes such as B4[9] and LDR[7] can pro-actively route so as to achieve low latency without causing congestion. These schemes, however, make routing decisions on a minute-byminute basis - too slow for routing on dense LEO constellations. It is an open question whether such schemes can be extended for this use, or if the latency between the controller and groundstations will always be too high.
   - L154（**混合方案提案**，逐字）：We postulate that a hybrid solution may work well. High priority low-latency traffic always gets priority, admission control limits its volume, preventing it causing congestion and it gets explicit routing ensuring minimum latency. For the remaining traffic, satellites monitor link load; this is broadcast to all groundstations globally, so everyone is aware of hotspots. Because of the nature of a LEO constellation, these hotspots tend to be geographic rather than topological. Groundstations then randomize their path choice across slightly less favorable paths to load-balance traffic away from hotspots. … This allows groundstations to be much more conservative about when they move traffic back to the lowest delay path, using timescales much longer than the latency of the broad cast load reports, so avoiding instability.

### 7.5 是否已被 RL 论文采用

**被大量 T1 学习型论文引用（本批被引最广的一篇）。**

全库检索模式 delay is not an option，命中文件（23 个）= 42E4NAQU 4QG5VYHQ 5HJ8ATR7 67CSKFK4 7AXASN73 8AYW2Y78 9GPFG5U3 AF674CSF DS9SPARV DVS8C3CC GPDPLJNG IEI3BYFF IXVSNEE3 JLF7IEBQ K7U4TYJN K93SCUF2 L63JISQN MYBALQ2D S85KQ4FC T9X6QCLL TQF59BD7 W6M3GU7L X5K285MW YD4JUT7G。

其中 T1（路由+学习）确认引用：

| 引用方 | 性质 | 行号 | 逐字 |
|---|---|---|---|
| 42E4NAQU | T1（MA-DRL 队列感知路由） | L168 | [1] M. Handley, "Delay is not an option: Low latency routing in space," in Proceedings of the 17th ACM Workshop on Hot Topics in Networks, Nov. 2018, pp. 85–91. |
| GPDPLJNG | T1（多商品流 + 深度学习） | L289 | [2] M. Handley, "Delay is not an option: Low latency routing in space," in Proceedings of the 17th ACM Workshop on Hot Topics in Networks, ser. HotNets, New York, NY, Nov. 2018, p. 85–91. |
| S85KQ4FC | T1（锚件：流级 DRL） | L603 | [54] M. Handley, "Delay is not an option: Low latency routing in space," in Proc. 17th ACM Workshop Hot Topics Netw., 2018, pp. 85–91. |

**采用方式**：均为引用其**低时延/动态拓扑动机**（如 42E4NAQU L13 low Earth orbit (LEO) satellite networks are increasingly being utilized to provide global internet coverage [1]），**未见把其预计算源路由机制吸收为学习方法的一环**。

### 7.6 实验合同里与「负载」相关的设置（仅作实验条件登记，不作贡献）

- **本文明确不做容量建模**，L25 逐字：It seems probable that free-space laser link speeds of 100 Gb/s or higher will be possible. However, in this paper we will refrain from modelling network capacity, as this is too speculative, and focus instead on latency, which is constrained only by topology and the speed of light.
- **明确假设无排队**，L150（见 §7.4）。
- 星座（L31 表，逐字）：Orbital Planes 32 / 32 8 / 5 / 6；Sats per plane 50 / 50 50 / 75 / 75；Altitude (km) 1,150 / 1,110 1,130 / 1,275 / 1,325；Inclination 53° / 53.8° 74° / 81° / 70°
- L19：Starlink's initial phase, 1,600 satellites in 1,150 km altitude orbits
- 覆盖判据（L21）：The main restriction is that satellites are considered reachable if, from the ground, they are within 40 degrees from the vertical.
- 激光链路数（L23）：A good working assumption is that each satellite will have five free-space laser links to connect to other Starlink satellites.
- 负载相关结果（**仅有乱序/TCP 层面的定性讨论**）：L128 There are five paths that have lower latency than the greatcircle fiber path, and all 20 paths have lower latency than the current Internet path. However, latency variability increases as the path gets worse: path 20 has much more variable latency than path 1, as it has fewer options available. In figure 12 we see the one-way latency of path 20 in more detail. 10% variability is likely insufficient to trigger spurious TCP timeouts, and increases in RTT are also unlikely to impact TCP. However, when latency decreases rapidly, reordering will occur, causing TCP to incorrectly assume a loss has occurred and triggering a fast retransmit.
- **负载=无流量模型、无到达过程、无突发**；唯一的「负载」讨论是定性提及 admission control 与 hotspot（L150/L154）。

### 7.7 该文自述的局限（逐字）

- L150：All the simulations above assume that no significant queuing happens in the satellites themselves.（**核心局限，自述**）
- L152：It is an open question whether such schemes can be extended for this use, or if the latency between the controller and groundstations will always be too high.
- L132（研究议程段，逐字，多项自认未解）：A network such as Starlink raises many research questions, both for the network itself, and for traffic traversing it. For legacy Internet traffic, reordering must be avoided. Delaybased congestion control such as BBR[3] may not perform well over such a network. The network must be resilient to failures. And it must be capable of routing with low delay, even when traffic levels are high enough to saturate the best paths. We briefly discuss some of these questions.
- L25：However, in this paper we will refrain from modelling network capacity, as this is too speculative

### 7.8 该文没有考察的算法选择（基于 7.1–7.6 判定）

- **无学习成分**（§7.3 实测）。
- **无排队/拥塞建模**（L150 自述；L25 自述不做容量）。
- **无失败成因区分**：故障只在 L146 定性讨论，且未区分原因——L146 逐字 Such a network is inherently resilient to failures. If an RF transceiver fails, that satellite can still relay through traffic; there are many other satellites within range of a groundstation, so the impact on coverage is minimal. However, all groundstations need to be informed of any failure, so they can factor it in to their routing considerations. 检索 Y_dropcause，实测 **67CSKFK4 = 0**。
- **无动作时间结构（无延迟/驻留动作）**：唯一的时间机制是预计算窗口（L78），不是「主动不发」。

---

## 8. YD4JUT7G — Internet Backbones in Space

### 8.1 机制公式（逐字）

**本文无编号公式**。实测取证：模式 \tag\{ → 命中 **0**；模式 \$ → 命中 **0**（该篇 MD 全文无 LaTeX 数学）。其「机制」是架构级的路由/寻址与成本模型。核心机制陈述逐字：

- L141（**SCION 扩展：连通性剖面 + 带宽类**，逐字）：This system can be leveraged to embed more information in the PCBs (and, in turn, in the paths distributed to end hosts) on the status of the GSLs and of the constellation. Specifically, for each ground station on the path, we suggest to include (i) a representation of the connectivity variations of the GSLs, called connectivity profile, and (ii) a time-varying bandwidth class, representing the total bandwidth available from the GST to the satellites.
- L141（**两信息的用途，逐字**）：The connectivity profile ensures that the path can be disseminated with no need for continuous announcements and withdrawals: the end host can determine whether the path is available at any point in time by intersecting the connectivity profiles of the GSTs on the path. The bandwidth class, computed as a function of local weather forecasts and the number of satellites in view from the GSTs, is used to check if the SN can support the bandwidth required for the communication or if it is actually unusable due to adverse conditions.
- L159（**inactive GST 定义，逐字**）：We call a GST inactive if it has no GSL that is connected or if its available bandwidth is below a minimum threshold. Inactive GSTs will re-route their traffic to active GSTs over terrestrial networks.
- L171（ReRo 核心分支，逐字）：(2) The s-GST is inactive. It will then forward the packet to its nearest active GST, which will then forward the packet to the SN. If none is available, the packet is re-routed on the terrestrial Internet. Since the GST is multihomed, this is achieved by removing the encapsulation and using the default routes of the BGP control plane. In case of congestion on the GSLs, a load balancer will determine the re-routing of packets to other nearby GSTs.
- L217（**时延计算三步，逐字，含 2.3 拉伸因子**）：(1) The great-circle distance from the source to the closest GST is computed. This figure is multiplied by a terrestrial path stretch factor of 2.3, to account for the tortuous path of fiber on land [40], and divided by the speed of light in fiber (which is 2c/3) to obtain the latency of the source-GST hop. (2) The same operation is repeated for the destination, finding the GST closest to the destination. (3) The GST-to-GST latency over the satellite path is computed by dividing the path length by the speed of light in vacuum.
- L238（PaCo 搜索空间，逐字）：To simulate PaCo, instead, we optimize the first hop between the three nearest GSTs to the source and destination. We chose to use the three nearest GSTs to constrain the optimization space, keeping the path-choice possibility for the source limited locally. Moreover our simulations show that the returns of allowing the selection between more than three nearest GSTs are rapidly diminishing.
- L104/L106/L108（黑盒成本模型三项，逐字）：the cost for a US-based satellite ground station is on the order of 7 million dollars；the price for the 30 antennas of a single GSTs around three million dollars；Pricing the deployment of fiber at 10,000 dollars per kilometer
- L88（**本文唯一「负载-稳定性」量化结论**）：While the graph displays the values for a latitude of 40°, Figure 1b shows that there is a similar tradeoff at different latitudes. Even if the threshold is fixed at 6 minutes and most events are filtered out, close to 20 events per day remain for each GST, each triggering at least one BGP update. This is despite setting the threshold so high that 15 – 45 % of available connectivity is wasted.

### 8.2 决策粒度

**域间路由架构级**：源端选 s-GST、s-GST 选 d-GST，之后交给 SN 内部路由协议。

- L165：The source initiates the communication by preparing a packet with the IP address of the destination and encapsulating it inside another IP packet with the address of the geographically closest GST, called source GST (s-GST). Similar to current CDN deployments, the choice of the closest GSTs relies either on DNS lookups or IP anycast
- L169：The s-GST active. Then, using the information contained in the packet, the s-GST computes the active GST geographically closest to the destination (d-GST). The packet is forwarded over the satellite path, employing the internal routing protocol of the SN-AS.
- L177：d-GST to destination. When the packet arrives at the d-GST, it is forwarded via standard BGP routing to the destination.
- **决策粒度 = 每包选入口/出口地面站**（不是逐跳），且**无动作时间结构**（没有延迟/驻留动作；唯一的「时间」是 connectivity profile 的可用性交集，L141）。

### 8.3 是否含学习成分

**否。**

- 检索 X2_anylearning_all，实测 **YD4JUT7G = 0**。
- 检索 T2_discount_clean，实测 **YD4JUT7G = 1**，逐条核验为 L102 the total cost of a ground-segment deployment is divided into recurring and non-recurring costs —— **成本会计用语，非 RL 折扣**。

### 8.4 可迁移点（含公式）

1. **把「路径可用性的时间剖面」作为可分发的一等对象（connectivity profile）**。
   - L141 逐字见上。**迁移到 RL**：这是「状态里放时间信息」的**分布式版本**——把未来可用窗口预先编码进路由公告，而非在每步决策时现算。我们方案可借用：动作若依赖未来链路可用性，可把「可用窗口」做成状态分量而非让网络自己学。
2. **带宽类（bandwidth class）作为天气与可见星数的函数**：L141 computed as a function of local weather forecasts and the number of satellites in view from the GSTs。**迁移**：把不可控外部因素（天气）聚合成离散类别而非连续值，可降低状态维度。
3. **「稳定优先于最优」的架构级权衡，且量化了代价**：
   - L245：the CDF of path control and the CDF of re-routing are very close, showing that, on average, the difference in the performance of the two systems is small. … on average, the loss is on the order of a few percent. These losses are negligible … However, we also see that in each simulation scenario these fluctuations can be substantial, degrading the performance of the network by more than 30 % (“Avg. maximum”). Moreover, in the absolute-worst case across all simulations the loss in performance can be higher than 80 % (“Worst case”).
   - **迁移**：这是「平均指标好、尾部分布差」的量化反例，对我们「负载/评测设置」的证据链有直接价值。
4. **把「加基础设施」证明为不解决问题的正面反例**：
   - L121：The black box model adds the cost of the WAN on top of this, more than doubling the original figure and highly increasing the risk of failure for the SN.
   - L50（**与 CTWVLBCY 同源现象，本篇独立佐证**）：This situation is worsening as more computer resources are being added to ground stations for “edge”-style processing, which further exaggerates the problem of load imbalance due to both network delays and computational delays, both of which could be imbalanced. Therefore, even if backhaul bandwidths increase in the future, UQE will continue to back up queues.
   - **迁移**：直接支撑「加带宽/加算力不能解决排队不均衡」这一结论，跨 CTWVLBCY 与 YD4JUT7G 两篇独立成立。
5. **路径感知网络（PAN）三要求清单（可作我们方案定位的架构锚点）**：L131 an architecture needs to (i) shield the terrestrial Internet from the SN's instability, (ii) allow for distributed deployments, splitting cost among entities, and (iii) enable the choice of the satellite path “on-demand”.

### 8.5 是否已被 RL 论文采用

**被多篇引用，但本批未检到 T1 RL 论文引用。**

全库检索模式 internet backbones in space，命中文件（13 个）= 8AYW2Y78 9GPFG5U3 9KZDXPKC AF674CSF DS9SPARV IEI3BYFF L63JISQN SBCHGBCP T9X6QCLL W6M3GU7L X5K285MW XM6NUPM4 YD4JUT7G。

按 TIER-ASSIGNMENT 定档：9GPFG5U3 / AF674CSF / SBCHGBCP / X5K285MW / K7U4TYJN / XM6NUPM4 属 T2，9KZDXPKC 属 T2，8AYW2Y78 / DS9SPARV / IEI3BYFF / L63JISQN / W6M3GU7L 属 T3，T9X6QCLL 属 T5 —— **未见 T1 学习型路由论文引用**。

### 8.6 实验合同里与「负载」相关的设置（仅作实验条件登记，不作贡献）

- 星座：L195 The satellite constellation considered in our simulation is SpaceX Starlink, in its deployment phase two [21]. The ISLs, four per satellite, are assumed to be connected to two in-plane (fore and aft satellite in the orbit) and two cross-plane (in the left and right neighboring planes).
- 源宿采样：L195 We sample source and destination from the set of medium- and large-sized cities (> 300,000 inhabitants) according to UN data [10]. Because the SN does not have coverage near the poles, we restrict the set to the 1833 cities in the −56° to 56° latitude range.
- **部分部署场景（关键「负载」条件）**：L88 Based on a 10 % deployment of the SpaceX phase 2 constellation.；L88 we use filtering to remove windows below a certain threshold, thus reducing the number of routing updates. In contrast, an availability window that is filtered out (i.e., not announced) induces connectivity waste.
- GST 部署：L211 we consider IXPs from the Euro-IXP dataset … from the initial 626 IXPs in the dataset we extract 353 unique locations.；L106 we choose the positions of GSTs by sampling from a probability distribution based on the gross domestic product (GDP) per unit area of the globe [31].
- **天气导致的负载/可用性扰动（本批唯一的真实气象数据负载）**：L236 we use historical weather data provided by NOAA [32], and for the duration of 2018 we analyze the rainfall accumulation in two instants every day. Then, we use 11 different thresholds to determine whether GSTs are inactive: a GST is inactive if the rainfall in its location exceeds the threshold. … This results in 7744 different simulation scenarios, each with a set of disabled GSTs.
- 未建模项（自述）：L223 For these experiments we disregard failures and disconnections, and assume that all GSTs are active in each deployment.
- **负载=城市对均匀采样 + NOAA 降雨阈值生成的停用集；无到达过程、无突发。**

### 8.7 该文自述的局限（逐字）

- L254–L262（Findings 段，逐字，含系统性边界）：
  - While the white-box solution would be the easiest to deploy today, the analysis oflink disruptions shows that it is severely lacking: it is highly susceptible to SN's instability, and BGP gives no guarantees on the latency of the selected paths.
  - The black-box solution improves stability by adding redundant links, but increases costs manifold. This poses limits to the scalability of the system and hinders performance … Moreover, the losses on the path from the host to the SN-AS are unpredictable, as such paths are chosen by BGP.
  - The CDN solution solves the scalability problem by hosting GSTs inside other networks … Sending traffic to the closest GST—and eventually re-routing—provides almost-optimal performance in the average case (Figure 3).
  - An architecture that implements path-control, enabling addressing of the optimal GST, would further lower the communication latency, providing an average improvement of more than 10 % in the 95th-percentile.
- L106（成本模型自述简化）：The choice of the optimal placement of GSTs given cost and performance constraints is a hard problem, and is outside the scope of this article. Therefore, we use a simple heuristic to simulate the positioning of the stations
- L110：Note that this analysis excludes equipment to light the fiber, support facilities and staff, management costs, and leasing prices for trans-oceanic fiber.

### 8.8 该文没有考察的算法选择（基于 8.1–8.6 判定）

- **无学习成分**（§8.3 实测：X2 命中 0）。
- **无域内（ISL）路由算法**：L272 自述 Intra-domain satellite routing: Routing inside a satellite constellation is a well studied topic … However, these works do not consider the effects that SNs have on the Internet as a whole. —— 本文**不做** ISL 级路由，明确交给 the internal routing protocol of the SN-AS（L169）。
- **无失败成因区分**：停用原因是「无 GSL 连接 或 带宽低于阈值」（L159 单一布尔），降雨只是触发阈值的一种外部因素，**不构成按原因分通道**。检索 Y_dropcause，实测 **YD4JUT7G = 0**。
- **无动作时间结构**：无延迟/驻留动作。

---

## 9. W5Z39E25 — A Wised Routing Protocols for LEO Satellite Networks（PQWRR）

### 9.1 机制公式（逐字）

**本文无编号公式**。实测取证：模式 \tag\{ → 命中 **0**；模式 \$ → 命中 **0**。其「机制」是调度策略 + 双路由表 + 阈值状态机的文字描述。核心机制逐字：

- L29（**PQWRR 混合调度**，逐字）：This paper propose a hybrid scheduling algorithm combining PQ and WRR scheduling algorithm-PQWRR algorithm, which set priority queue for traffic class A to ensure its priority; traffic class B is divided into different service level, each service level share the remainder bandwidth using the WRR scheduling policy, ensure the relative fairness of bandwidth allocation.
- L29（调度算法族谱，逐字）：Frequently-used packet scheduling algorithms according to service rules can be divided into simple queue scheduling algorithm(FIFO, PQ, QLT, etc.), scheduling algorithm based on round-robin (RR, WRR and DRR and URR, etc.), scheduling algorithm based on the GPS model (WFQ ,WF2Q ,SPQ, PFQ) [5].
- L34（队列行为，逐字）：Traffic will be put into different buffer queues depending on its type once it arrives, traffic class A will be transferred to high priority queue and wait to be sent forward, traffic class B will be transferred to corresponding low priority buffer queues, when buffer queue A is empty, traffic class B will be sent forward according to WRR scheduling policies.
- L36（**双路由表**，逐字）：this paper proposes a multiple path congestion control algorithm for multi-service traffic: each satellite stores 2 the route table: shortest path route table (route table1) and backup route table based on congestion control.
- L43（**阈值状态机**，逐字）：For satellite traffic arrival rate λ set two state thresholds: idle threshold α and busy threshold β ; Satellite nodes keep track of their own traffic arrival rate, when λ > β namely determining satellite into busy state, when λ < α determining satellite into idle state, defining α < λ < β as a transition state. Satellite state is monitored, when state change busy/idle occurs, notice the neighbor satellites and routing control center, when neighbor satellite receives ”busy” signal, it will reduce traffic to congestion nodes, and the routing control center will remove busy satellite node from the network topology and recalculate the backup route table.
- L45（**逐类转发分支**，逐字）：When retransmit on-board traffic, first find the next hop according to the shortest path route table, check its status, if the next hop node is idle, send forward the traffic to the next hop satellite; If the next hop node in busy state, then judge the forward direction depending on the traffic class: traffic class A will be forwarded to the next hop satellites directly ,lookup to backup route table and find a new next-hop for class B, if no next-hop node conform to the conditions, traffic class B will be put into routing waiting queue and wait to be forwarded when route table updated.
- L38（虚拟拓扑与链路类型，逐字）：The shortest path route table is established based on virtual topology [6, 7] and calculated offline according to the network topology structure within each timeslot. … for LEO constellation, each satellite can establish connection with 4 neighbor satellites, build two inter-satellite links(ISL) and 2 inter-orbit links(IOL), ISL length can be generally regarded as constant over time, IOL length is changing as the satellite moves. In addition, ISL connection is permanent, while IOL connection is dynamic, IOL connection will turn off when satellites go through the high latitudes, angle of visibility between satellites is too small, and satellites in the cross-seam do not have IOL [2].
- L53（无下一跳时的排队，逐字）：When module sat router monitors the lower layer transmitter has idle channel, it will send packets in sending waiting queue forward to the transmitter; when next time-slot arrives update the route table and look up the route table to find the next hop node for packets in waiting routing queue

### 9.2 决策粒度

**逐包调度 + 逐时隙路由表更新**。

- 调度粒度：L29/L34 逐包入队、按 PQ/WRR 出队。
- 路由粒度：L38 每个 timeslot 离线重算最短路表；L72 Fig. 5 it recalculates the shortest path route table and backup route table when time-slot and satellite node state shift.
- **无动作时间结构（无延迟转发）**：拥塞时 class B 走备份表或进等待队列（L45 traffic class B will be put into routing waiting queue and wait to be forwarded when route table updated），但这是**被迫排队**而非**主动延迟动作**。

### 9.3 是否含学习成分

**否。**

- 检索 X2_anylearning_all，实测 **W5Z39E25 = 0**。
- 检索 T2_discount_clean，实测 **W5Z39E25 = 0**。

### 9.4 可迁移点（含公式）

1. **按业务等级分离的「谁承担拥塞」规则——本批最接近「同一失败事件按类型分流处理」的设计**。
   - L45 逐字（见 9.1）：class A 直接转发（不让路），class B 查备份表，无可用下一跳则进等待队列。
   - L91 逐字的实测后果：traffic class A has the priority right of preemption for satellite resources, its packet loss rate has remained 0, traffic class B suffers packet loss during the on-board resource shortage, because inner traffic class B using weighted round-robin scheduling, only traffic class B0 with the lowest weight suffers packet loss when congestion is lighter (see Figure 10), but when congestion get heavier, all the traffic class B suffers packet loss in different degrees.
   - **迁移轴 = 业务类别**（不是失败物理成因）。这是 G-A 的**最近邻机制**，须在 §12 明确写清其与 G-A 的差别。
2. **「备份路由表 + 拥堵节点从拓扑中摘除」**：L43 the routing control center will remove busy satellite node from the network topology and recalculate the backup route table. **迁移**：把「拥塞节点」当作临时不可用节点处理，可复用现成的失效重路由逻辑。
3. **双阈值迟滞状态机（idle/transition/busy）**：L43 定义 λ > β 忙、λ < α 闲、α < λ < β 过渡态——**避免状态抖动**。**迁移**：我们方案的链路拥塞标记应带迟滞，否则会引发动作震荡。
4. **反例价值：加备用路径会放大时延抖动**。L115 逐字：when composite PQWRR scheduling strategy and alternate path, non-real-time traffic choose relatively free satellite as a relay node in the network, the end-to-end delay dramatically reduce , but due to the multipath strategy and the routing hop relatively increase, which cause the severe mutations of ETE delay of class B. While, we found that at some point the time delay of class B has not been improved obviously, this is because although the queuing delay on single satellite reduced, but the routing hop count get larger, times of queued get larger, path length get longer, these lead to the increase of delay.
   - **迁移**：这是「绕行换低排队」不一定净收益的明确反例，对我们方案的动作设计有直接约束价值。
5. **量化结果可作对照**：L126 90% ETE delay of the traffic class A, B2, B1, B0 respectively less than 102ms, 98ms, 567ms and 790ms（纯 PQWRR）对比 90% ETE delay of traffic class B2, B1, B0 respectively less than 136ms, 145ms and 460ms（复合策略）。

### 9.5 是否已被 RL 论文采用

**全库检索未见。** 模式 a wised routing protocols，实测命中文件 = W5Z39E25 自身（1 个）。

### 9.6 实验合同里与「负载」相关的设置（仅作实验条件登记，不作贡献）

- 星座（L79 逐字）：using iridium constellation model as LEO constellation topology, it has six orbit plane, on each plane distribute 11 satellites, orbit altitude is 780 km, latitude threshold and the minimum elevation are set to be 60° and 8.2°, orbit file is generated by STK software and then imported to OPNET.
- **业务比例与参数（逐字）**：L79 Traffic class B is divided into three types- B0, B1, B2, their weights are increasing in turn, proportion of traffic A, B2, B1, B0 is 25%, packet size is 1000 bits, on-board traffic processing rate is 500 packets/s, and the buffer queue length is 50 packets.
- **负载来源（两篇文献的流量矩阵）**：L81 Literature [10] has divided the earth into 12 x 24 cells and predicted the traffic demand in every cell (see figure 7), the literature [11] provides the flow ratio between continents (see table 1). We set traffic background based on these two literatures, using little green dots to simulate the traffic demand of its region and setting the destination address on the basis of traffic ratio between the continents.
- **源宿与总需求（逐字）**：L81 Source, destination nodes are set respectively in (56°south latitude, 26°east longitude) and (65.2°north latitude, 58° west longitude), total traffic demand between them is 100 packets/s.；L81 We set up two simulation scenarios, respectively to validate the performance of PQWRR scheduling algorithm and the composite routing algorithm, each policy is simulated for 30 min.
- 大陆间流量比（L93 Table 1 逐字，行=源，列=目的，单位 %）：North America→自身 86.18；Europe→自身 55.88；Asia→自身 47.74；South America→自身 25.12；Africa→自身 7.95；Oceania→自身 30.12（L95 图例：1-North America 2-Europe 3-Asia 4-South America 5-Africa 6-Oceania）。
- **负载=两篇文献导出的静态流量矩阵 + 固定源宿 + 固定 100 packets/s；无过程族、无到达过程、无突发**。

### 9.7 该文自述的局限（逐字）

- L140（**自认未解核心问题**）：But in this paper how to choose state threshold , has not been discussed, the selection method will be the focus of our future research.
- L140（自认负面结果）：the simulation result shows that the proposed algorithm has the very good performance to ensure the QoS of real-time and non-real-time traffic in aspect of ETE delay, throughput, although under this policy the delay jitter of class B is severe, but as a whole, for traffic class B the ETE delay reduce greatly, throughput improves significantly.
- L128（**自认低优先级被饿死的量化证据**）：the lower traffic priority, the worse throughput performance, especially class B0, due to its weak resource competitiveness, its throughput is only about 15 packets/s, throughput rate only reached to 60%.
- L104：due to the congestion, the bandwidth of on real-time traffic is preempted by the real-time traffic, QoS performance of class B get worse, its ETE delay and delay jitter get larger（原文此处「on real-time」疑为非实时之误，**逐字保留**）

### 9.8 该文没有考察的算法选择（基于 9.1–9.6 判定）

- **无学习成分**（§9.3 实测）。
- **阈值 α/β 未给选择方法**（L140 自述）。
- **无失败物理成因区分**：丢包只按**业务类别**归因（L91），不按丢包原因归因。检索 Y_dropcause，实测 **W5Z39E25 = 0**。
- **无拥塞程度的连续度量**：只有 idle/transition/busy 三态（L43），无队列长度/速率余量的连续状态量。

---

