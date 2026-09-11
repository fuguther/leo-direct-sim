# 读卡批次 R6

> 通读者逐字通读全文（VM MinerU MD），行号对应 VM MD 行号。11 篇：J68GU76W JLF7IEBQ JP79GMZS JS857IYN JSX5XG88 JZA5SEQA K7U4TYJN K93SCUF2 KPUZIMU5 L2VKYTAV L5F3DK68。

## J68GU76W — Reinforcement Learning for Opportunistic Routing in Software-Defined LEO–Terrestrial Systems

**1. 一句话**
把 LEO 星群看成"没有固定收件人"的投递网络：只要某颗星当下能看见地面网关，就往那儿送（opportunistic routing），用**残差 RL**（在 backpressure 之上叠加一个学出来的修正项）来学这个转发策略，目标是压小最大队列长度。

**2. 问题设定**
LEO 星大部分轨道时间里"无事可做"，只有限时窗口能把缓存数据卸给地面网关（L20 段逐字："during most of their orbital period, LEO satellites remain idle with respect to data collection and have only limited time windows for offloading buffered data to ground gateways"）。传统静态路由要指定源–目的对，而这里 backhaul 不需要固定端到端路径（L13）。痛点：拓扑快速变化 + 非平稳到达 + 时变信道，使 backpressure/MaxWeight 难以直接适用（L133）；且每颗星只有局部信息，跨星协同难。

**3. 方法骨架**
- **架构**：GEO 卫星当 SDN 控制器（控制面），LEO 当数据面交换机，星上回传状态给 GEO（L20）。
- **网络模型**：邻域 $mathcal{N}_k(t)$ 由式 1 选出——在距离 $le R_{max}$、面间夹角 $Phi le Theta$ 约束下取最近的 $M$ 个（式 1，L40）。
- **到达模型（关键）**：$lambda_k(t) = M_{mathrm{tod}}(h(t))int_{A_k(t)} ho_k(mathbf r),mathrm dA$（式 4，L64），其中 $M_{mathrm{tod}}(h)=alphasin(2pi(h-	au)/24)+eta$ —— **日内正弦调制 × 人口密度空间积分**；到达量服从 Poisson（式 5，L70）。
- **队列动力**：式 12，$Q_k(t+1)=(Q_k(t)+u_k+r_k-v_k-d_k)^+$（L116）。
- **目标**：$min mathbb E[max_k Q_k(t+1)]$（式 13，L128）——**最小化全网最大队列长**，不是平均时延。
- **RL 设计**：state（式 15，L156）$S(t)={Q_k, v_k, d_k, r_k: kinmathcal K}$ 全体星；action（式 16）每条 ISL 的二值激活 $a_{km}in{0,1}$；**奖励（式 18，L178）是差分式的**：$R(t)=-[alpha(ar Q_a-ar Q_{mathrm{BP}})+eta(Q_a^{max}-Q_{mathrm{BP}}^{max})]$，即**跟 backpressure 的队列做比较**，比它差就罚。基座策略是 backpressure 打分 $s^{mathrm{BP}}_{km}=(Q_k-Q_m)C^{mathrm{ISL}}_{km}$（式 14）；LG-BP 加一项 $+lambda^{mathrm{LG-BP}}C_m^{mathrm{LG}}$（式 17，L172）。算法用 **DDQN**，3 层 256 隐单元（L204）。

**4. 它声称的效果**
- 训练奖励（Fig 3）：比 vanilla DDQN 高 **643.81%**，比 residual policy baseline 高 **34.01%**（L204）。
- 队列长（Fig 4 左）：相对 vanilla DDQN 降 3.9–18.1%（$Min{1..5}$）；相对 backpressure 从 $M=1$ 的 **1.6%** 涨到 $M=5$ 的 **12.1%**（L215）。
- 三个星座（Starlink / Iridium / OneWeb，Fig 4 右）：相对 backpressure 平均降 **7.6–16.1%**。
- 变卫星数（Fig 5 左）：比次优方法降 **5.3–14.8%**。
- 网关布放（Fig 6）：hybrid（全球）最好；单区域内 Asia 较好，**Europe 与 North America 覆盖有限、出现瓶颈**（L217）。
- **基线**：Backpressure、Equalize、No-ISL、Max-Weight、Random（L194）。指标**只有队列长度**，没有时延、没有丢包。

**5. 它的实验条件**
Space-Track 取 TLE 真实轨道 + 2020 GPW 人口数据（L198）；仿真跨 **3 天**，时隙 $Delta t = 60$ s；**Starlink 只用 K = 10 颗星**，$M=4$ 邻居；**队列设为无界，显式不建模缓冲溢出**（L198 逐字："Queues for the satellites are assumed unbounded, so buffer overflow is not explicitly modeled"）；结果取 5 次独立运行平均；PyTorch + Gymnasium，A100 训练。训练与评估同一套仿真环境，未见跨分布测试。

**6. 它自述的局限**
- L198："Queues for the satellites are assumed unbounded, so buffer overflow is not explicitly modeled, though reducing queue length inherently lowers overflow risk."（无界队列 = 不建模丢包）
- L221 结论："Future work will address scalability to mega-constellations, account for delays between the GEO controller and LEO satellites, and ensure consistent implementation of the reinforcement learning framework."（承认没做大规模、**没算 GEO 控制器到 LEO 的控制时延**、实现一致性待补）

**7. 它没做但看起来能做的地方**
1. **奖励是"相对 backpressure"的差分式**（式 18）——意味着每个训练步都要跑一份 backpressure 参考轨迹。这个设计可以改成"相对上一时刻"或"相对滑动基线"，但论文完全没讨论它的代价与偏置。
2. **K=10 的星座规模**却被用来宣称"scalable"（L221 自认没做 mega-constellation）。而 state 式 15 是**全体星的队列**，天然随 K 线性膨胀——它给了一个会撞墙的状态表示。
3. **只有队列长度一个指标**。它自己在结论里说 RL 对 low-latency 有前途，但全文**没有任何时延数字**。
4. **无界队列**把"拥塞"与"丢包/时延"解耦了，等于回避了负载真正超载时的行为。
5. 网关可见性是**外部给定的时间窗**（式 2/3），没有把"选网关"当作动作——动作只是 ISL 二值激活。

**8. 和同批其他篇的关系**
本篇是"SDN + 残差 RL + 队列稳定"路线。同批中 L2VKYTAV 同为极短稿（123 行），若也是队列/负载类可对照。它引用的经典基线 Tassiulas–Ephremides backpressure/MaxWeight [13] 是多篇 LEO 路由论文的公共祖辈；引用 Silver 的 residual policy learning [15] 是本篇的算法来源。**未见引用本批其他篇**（参考文献 17 条全为经典/他领域）。

**9. 对"负载变化下到达率/时延"的贡献**
**有一手事实，但方向偏**。它给出了一个**带日内节律的到达率模型**：$lambda_k(t)$ = 人口密度空间积分 × 正弦日内调制（式 4），到达为 Poisson（式 5），并用 Fig 1 展示全球活动率随时间的变化——这是"负载随时间变化"的显式建模，可直接复用。但它**没有做到达率扫描实验**（没有 λ 从小到大看性能拐点），指标全是队列长度而**没有时延**，且**无界队列**使"过载"不可观测。所以：它贡献了**负载模型**，没有贡献**负载→时延的响应曲线**。

**10. 一句话评价**
**把"残差策略学习"这一现成技术搬到 LEO 机会路由上，并给了一个可复用的日内+人口到达模型**；但规模小（K=10）、无界队列、指标单一，本质上是一次"方法搬家 + 队列长对比"，而非对负载–时延机制的新认识。
