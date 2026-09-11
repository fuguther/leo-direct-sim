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

## JLF7IEBQ — SaTE: Low-Latency Traffic Engineering for Satellite Networks

**1. 一句话**
把"星上流量工程（TE）算得太慢"当成核心矛盾：用一张**异构图**（卫星/流量/路径/链路四类节点 + 三类关系）让 **纯 GNN（不带 DNN）**直接输出每条流的路径分配，在 4236 星的 Starlink 上把求解时间从 Gurobi 的 46 s 压到 **17 ms**，并靠"拓扑可剪枝"把训练集压到 512 个代表拓扑。

**2. 问题设定**
LEO 星座拓扑变化极快——作者实测 Starlink **拓扑保持时间 THT 平均仅 70 ms、最大约 700 ms**（L110），而传统 TE 求解要几分钟（L100）。后果是：在 TE 算完之前，预配的路径已经失效——**150 秒内 14,941 条预配路径中超过 56% 变成过时**（L120）。同时用户面流量有亚秒级波动（L41 引用 RedTE [23]），要求 TE 实时响应。所以痛点是"**算子太慢 → 路径过期 + 分配过时**"，而不是"网络不稳"。范围明确限定在 TE 工作流中的**计算步**（L100 逐字："The paper focuses on the TE computation step within the broader TE workflow"）。

**3. 方法骨架**
非 RL，是**监督学习 + 可微惩罚**：
- **图设计（第 3.2 节）**：节点 4 类（Satellite / Traffic / Path / Link），关系剪到只剩 3 类（R1 星间连接、R2 Path–Satellite、R3 Path–Traffic），L175。剪掉 "access" 关系（被 crosses+transports 隐含覆盖），Link 并入 connect 的边权。**关键卖点：全部关系都能被 GNN 学，因此不需要 DNN 层**，从而支持可变尺寸输入 → 可剪枝 → 可泛化到未见拓扑。
- **学习（第 3.3 节）**：三个 GAT 模块按 R1/R2/R3 顺序传递消息（式 1，L194），嵌入维 768（L183）；初始化用邻居数/路径长度/流量需求/链路容量/候选路径数（L189 表）；最后 MLP 解码出 $x_{jp}$（流量 j 分到路径 p 的量）。
- **约束违反修正（L199）**：GNN 是软约束，"we trim overloaded traffic"——**硬约束靠事后裁剪**，不是模型保证。
- **训练（L201）**：监督学习，标签由 **Gurobi 求解同一输入**生成（L201 逐字）。损失 = 监督项 + 惩罚项（式 4，L565）。
- **剪枝（第 3.4 节）**：流量/路径剪枝（只留非零需求，335 GB → 15 MB，**22,381×**，L209/Table 1）；拓扑剪枝（Graph2Vec 向量化 + **DPP 采样**取 512 个代表拓扑，L629）。

**4. 它声称的效果**
- **计算时延**：Starlink（4236 星）平均 **17 ms**，标准差 87 µs（L268）；比 Gurobi 快 **2738×**、比 POP 快 1462×、比 ECMP+WF 快 1013–5230×（L261）。在线间隔上 Gurobi/PoP/ECMP+WF 分别是 47 s / 25 s / 54 s（L292）。
- **满足需求（online，计入计算时延）**：比各自最强基线平均改善 **23.5%（激光）/ 46.6%（地面中继）**，绝对多满足 **11.0% / 17.7%** 的需求（L294）。
- **对照 Teal（同为 GNN TE）**：在 396 星上平均高 **17.4% / 19.8%**（L294）；训练时间快 2.8×；Starlink 规模下 Teal 因单点 335 GB **根本放不进 GPU**（L259）。
- **剪枝收益**：512 个代表拓扑可达 8000 随机拓扑模型性能的 **>99%**（L288）。
- **离线**：比 Gurobi 上界低 **12.8%（激光）/ 12.3%（中继）**（L679）。
- **MLU 目标**：比基线 [55] 好 24.5% / 9.3%，但比专门做 MLU 的 HARP 还差 **16% / 13%**（L697）。

**5. 它的实验条件**
- 拓扑：Starlink 4236 星、**四层壳**（540/550/560/570 km，L659 表 4），壳内 4 邻居，**跨壳链路两种：激光（<2000 km）或地面中继（仰角 >25°，222 个真实站点）**（L108）；另有 Iridium 66 星、396 星、1584 星三个尺度。
- **所有链路容量统一限 200 Mbps**（L226），上下行 50 Mbps/连接（L232）。
- 流量：300 万用户 + 1000 网关按人口密度布放（L230），业务混合 voice 64 kbps / video 8 Mbps / file transfer 50 Mbps（表 2）。
- **负载设置：每 1 秒一个 Poisson 过程，强度 λ（flows/s），四档 125 / 250 / 375 / 500**（L232, L292）。
- 训练/评估：每个星座单独训一个模型；**10000 个 1 秒间隔拓扑，训练:测试 4:1**；测试集是**完全未见的拓扑与流量矩阵**（L245）；另有跨尺度泛化测试（396 训练 → 4236 测试，L313）。
- 硬件：Azure + A100 80 GB（L222）。

**6. 它自述的局限**
- **剪枝不能用于带 DNN 的混合模型**（L216 逐字："The pruning method is applicable only to fully GNN-based frameworks. It cannot be applied to hybrid models with DNNs."）
- **约束靠事后裁剪**（L199 逐字："Neural networks including GNNs are inherently soft constraint models... As a result, the computation outcome $x_{jp}$ may violate TE constraints. To address this, we trim overloaded traffic"）
- **公平性缺失**（L309 逐字："some flows experience partial satisfaction—a common limitation of centralized TE algorithms focused on global objectives"）
- **离线仍差 Gurobi 12.8%**，作者称"Bridging this gap represents a central goal for the future development of our framework"（L679）
- MLU 目标下不如专用方法（L697）；跨尺度泛化会掉 6.3–18.2%（L315）

**7. 它没做但看起来能做的地方**
1. **延迟只在"计算侧"被度量**。THT 70 ms 是它自己测的，17 ms 也是它自己测的，但**数据面的端到端时延、排队时延全文一个数字都没有**——它用的是"满足需求"这一吞吐口径代替时延。（Appendix C 提到 access 策略影响时延、Fig 12 有图，但正文自述"beyond the scope of this paper"，L595。）
2. **λ 是"每秒新流数"，不是"每流速率"**。500 flows/s 的负载扫描只改了流的数量，流的速率档位是固定的三档业务（表 2）。真正"负载变化"的另一半（单流速率变化、突发性）没扫。
3. **亚秒波动被引用了但没有建模**（L41 引 RedTE 说用户面有 subsecond dynamics，而自己的流量生成器是 1 秒粒度的 Poisson）。这是一个它自己点出来的缺口。
4. **拓扑剪枝的 512 个点是用 DPP 从已有快照里选的**，选多少完全靠经验（128 已够用、512 达 99%），没有给出"要多少点"的先验判据。
5. **跨壳链路两种方案（激光 vs 地面中继）性能差 2 倍以上**（23.5% vs 46.6% 改善幅度），但论文没有解释为什么地面中继方案下 GNN 相对基线优势更大——这背后可能是基线在中继场景更差，而非 SaTE 更好。

**8. 和同批其他篇的关系**
这是本批里唯一的 **SIGCOMM 系、非 RL、纯 GNN 监督学习**路线。它的对照对象是 WAN TE 谱系（Teal[78]、HARP[2]、POP[55]、ECMP+WF[35]、Gurobi[24]）。**引用了本领域的经典时延论文**：Handley "Delay is Not an Option" [27] 与 "Using ground relays for low-latency wide-area routing in megaconstellations" [28] —— 这两篇是"LEO 路由为时延服务"的源头，可作为跨批次溯源的锚点。也引用了 [45] Stable Hierarchical Routing（MobiCom'24）、[44] Starlink self-driving。**未见引用本批其他 10 篇**。与 J68GU76W 形成鲜明对照：J68 是"RL + 队列长"，SaTE 是"监督 GNN + 吞吐"，两者都把时延排除在指标之外。

**9. 对"负载变化下到达率/时延"的贡献**
**有直接贡献，但是"到达率 → 满足需求"而非"到达率 → 时延"**：
- 显式的**到达强度扫描**：λ ∈ {125, 250, 375, 500} flows/s（L292），并给出定性结论逐字："satisfied demand decreases as traffic loads increase due to the successive saturation of link capacity (200 Mbps)"（L294）——这是**链路容量饱和导致的拐点**，与 S85KQ4FC 的"决策资源饱和"是同一类现象的不同瓶颈。
- 给出**两个时间尺度的直接对照**：拓扑保持时间 **70 ms**（L110）vs TE 计算 **17 ms**（L268）。这是"决策周期必须快于环境变化周期"的量化论证，是可复用的**时间尺度论证范式**。
- 给出了**控制面收敛的下界**：向 4236 星分发规则最长 **174 ms**（L619, Fig 13）——即"算得快"并不等于"配置生效快"，控制面传播本身就有百毫秒量级。
- **但它不测时延**。λ 增大时它看的是"多少需求被满足"，没有排队时延、没有端到端时延。所以对"负载 → 时延"这条曲线，它贡献的是**瓶颈机理（200 Mbps 链路饱和）**与**时间尺度的量级**，不是时延数字。

**10. 一句话评价**
**把 WAN TE 的"GNN 加速"思路系统性地移植到 LEO，并用"纯 GNN 图设计"换来了剪枝能力与泛化能力**——是"用更好的图表示解决规模问题"的典范；但它把时延问题整体让渡给了"满足需求"这一吞吐代理指标，且硬约束靠事后裁剪，属于**把已有 X（GNN TE）用到 Y（卫星）上并改了图设计**，对负载–时延机制只提供了一个容量饱和拐点。


## JP79GMZS — Explicit Load Balancing Technique for NGEO Satellite IP Networks With On-Board Processing Capabilities

**1. 一句话**
**ELB**：卫星监视自己的队列占用率，把状态分成 free / fairly-busy / busy 三档，在**拥塞真正发生之前**给邻居发信令，让邻居把一部分流量改道到不含自己的备用路径上；论文的精髓不在"改道"这个动作，而在**三个参数（两个阈值 α、β 和一个降速比 χ）怎么用闭式公式动态算出来**。

**2. 问题设定**
地球人口分布不均（地理/气候约束），覆盖城市的卫星拥塞、覆盖乡村的卫星闲置（L25）。当时所有路由协议都只找"最小传播时延/最小跳数"路径（L27、L45），**完全不看星座上总的流量分布**，结果是重载链路排队时延暴涨、缓冲溢出、丢包。论文点名批评 CEMR [22]：它的代价函数虽然含排队时延，但**不反映下一跳的拥塞状态、也不估计在下一跳会排多久、更不反映在下游被丢的概率**（L49 逐字："it does not reflect the congestion state of the next hop, nor does it estimate the queuing delay a packet may experience there. It does not reflect the likelihood of packets to be dropped by the downstream hop either."）。

**3. 方法骨架**
非 RL，是**基于队列的分布式拥塞通告 + 多路径分流**：
- **状态机（L61）**：队列占用率 $Qr$ = 当前队列/总队长；$Qr<alpha$ → Free；$alphale Qr<eta$ → Fairly Busy；$Qr>eta$ → Busy。
- **两级信令（L63）**：进入 FBS 时发 warning，邻居更新路由表、开始找**不含 A 的替代路径**；进入 BS 时发 **BSA（Busy State Advertisement）**包，携带卫星 ID 与 **TRR χ**，邻居把发往 A 的速率降低 χ，剩下的 $(1-chi)$ 走之前找好的替代路。信令只在状态跳变时广播给邻居，不到全路径（L65）。
- **β 的闭式设定（L69–L93）**：设 δ_d = 距丢包还有多久 = $rac{(Q_l-q(t))cdot P_{avg}}{I-O}$（式 1）；丢包概率 $p=min(1,rac{delta+d}{delta_d})$（式 2，d 为 ISL 时延，δ 为监视间隔）；令 $eta = 1-p$（式 3）。**即：把"预测的丢包概率"直接写进阈值**。监视间隔 δ 取 **1 ms**（实时监视，L93）。$alpha=eta/2$（式 4）。
- **χ 的闭式设定（L103–L126）**：由式 5 算出 BSA 到达时刻的队列占用，再要求新速率满足式 6（保证卫星恢复后能在 Free 态停留至少 θ），反解 $I_s^{new}$，得 $chi=min(max(0,I_s^{	ext{new}}/I_s),1)$（式 7）。默认 θ = 200 ms。
- **防级联改道（L128）**：路由代价 $L_{cost}(t)=T_d+T_B(t)$（式 8），其中 $T_B(t)=rac{1}{Delta}int_{t-Delta}^{t} q(i)rac{P_{avg}}{C}di$（式 9）是**预测排队时延**；路由表每 Δ = 1 s 更新一次。
- **多业务类（L142–L164）**：A 类时延敏感（VoIP、交互视频）、B 类吞吐敏感（VoD、大文件）、C 类 best effort。改道**先 C 后 B，A 类永不改道**（Table I，L168）。类占比用 EWMA 预测（式 10），ω=0.1。
- **TCP 乱序修复（第 III.D 节）**：多路径导致乱序 → TCP 误判拥塞。用 **TTL 字段**判别：若到达包的 TTL ≥ 之前按序包的 TTL，说明只是**路径变了**，则**扣住 ACK 一段时间**；否则视为真丢包，照常发 DupACK（Algorithm 1，L172–L191，判定式 11）。只改接收端，不改协议。

**4. 它声称的效果**
- Fig 2（L231）：丢包数 vs 各连接发送速率（0.8–1.5 Mbps），**ELB-over-CEMR 丢包最低**；即便 ELB-over-DSP 也比纯 DSP 和纯 CEMR 丢包少。
- Fig 3（L231）：总吞吐同样以 ELB 两种实现最高。
- Fig 4（L239）：**流量分布指数** $f=rac{(sum x_i)^2}{nsum x_i^2}$（式 12，L224）随速率变化，ELB-over-DSP 显著优于 DSP；但 **ELB-over-CEMR 相比纯 CEMR 只有"minimal"改善**（L239 逐字），因为 CEMR 本来就用多条不相交路径。
- Fig 5（L246）：**流平均时延的 CDF**——"个别流可能比传统路由更慢，但整体（CDF）ELB 最好"，因为 ELB 压低了队列占用。
- Fig 6（L246）：逐星平均排队时延——**北美、西欧、东亚最高**（覆盖人口密集区）。
- Fig 7/8（L256）：多业务类下，传统 ELB 平均时延高于 DSP；增强 ELB 下 **A 类时延小于其他类**；**重载时纯 DSP 平均时延最小，但代价是大量丢包**。
- Fig 10（L271–L275）：TTL 机制的 goodput 在**所有场景**都优于标准 TCP；与 TCP-PR 相比，在低 χ 时自己更差、高 χ 时更好；ISL 时延越大（MEO）自己越占优。
- **基线**：DSP（Dijkstra 最短路）、CEMR [22]。

**5. 它的实验条件**
- **NS-2 仿真**；星座：**Iridium-like，66 星、6 个轨道面**；**显式不考虑 seam**（L213 逐字："we do not consider the seams where two ISLs are switched off"），因此**每个卫星恒定 4 条 ISL，拓扑是静止的**。
- 容量：上行/下行/ISL **统一 25 Mbps**；**所有链路假设无差错**（L213）；ISL 时延**常数 20 ms**；平均包长 1 KB；**Drop-Tail 缓冲 200 包**。
- 流量：**600 条非持续 On-Off 流**，On/Off 时长服从 **Pareto 分布（形状参数 1.2）**，平均突发/空闲各 200 ms；源端**恒定速率 0.8–1.5 Mbps**；端到端分布按六大洲的重力式矩阵（Table II，如北美→北美 60%）。
- 参数：δ = 1 ms 实时监视，Δ = 1 s 路由更新，θ = 200 ms（刻意设为 ISL 时延的 10 倍）。
- 仿真是稳态跑 60 s，**无训练/评估之分**（非学习方法）。多业务类实验设 A:B:C = 20%:30%:50%。

**6. 它自述的局限**
- **拓扑静止**（L213 逐字）："In the considered constellation, we do not consider the seams where two ISLs are switched off due to the motion in opposite directions."
- **无差错信道**（L213 逐字）："In all conducted simulations, all links are presumed to be error-free. The rationale beneath this assumption is to avoid any possible confusion between throughput degradation due to packet drops ... While such an assumption does not hold in real networks, results of simulations conducted in environments with channel errors demonstrated that link errors do not change any of the fundamental observations...（后半句是作者自己的辩解，无数据）
- **目标应用受限**（L289 逐字）："The targeted applications of the ELB scheme are preferably those that are delay insensitive and most importantly tolerant to a certain level of packet disorder or delay jitter."
- **个别流会更慢**（L246 逐字）："while some individual flows may experience longer delays than in case of traditional routing schemes"
- 未来工作只写了 DiffServ 集成（L293），**未提"参数 α/β/χ 与负载的关系是否随场景漂移"**。

**7. 它没做但看起来能做的地方**
1. **α、β、χ 全是"负载的瞬时函数"而不是"负载轨迹的函数"**：β 由当前 I、O、q(t) 算出，χ 由当前 I_s 算出。它们对**到达率的二阶变化（突发、趋势）完全无感知**——而它自己的流量模型恰恰是 Pareto 突发的。这是一个它自己埋下却没收的口子。
2. **改道只做一跳**：邻居把流量挪到"不含 A 的路径"，但**没有任何全局视野**去判断这条替代路径下游会不会也马上拥塞。多级级联虽有代价函数缓解，但论文没有做"级联改道发生了几次"的统计。
3. **只测了恒定源速率 0.8–1.5 Mbps**。真正的"负载变化"（时变到达率、阶跃、过载）没有作为自变量——λ 是静态扫描而非动态轨迹。
4. **66 星 Iridium-like 静止拓扑**，与 LEO 的真实动态（seam、极区断链、ISL 重配）完全脱节；在真实 LEO 中"替代路径"的生存期可能短于改道所需的时间。
5. **A 类永不改道**（Table I）这一硬规则在**A 类本身造成拥塞**时会退化——论文假设 A 类占比小（引 Odlyzko 说 >80% 是时延不敏感流量，L164），但没有测 A 类占比升高时的行为。

**8. 和同批其他篇的关系**
**这是本批的"祖辈"层文献**——多篇 LEO 路由论文（含 S85KQ4FC 锚件卡里明确列出的 ELB[38]）把它当作经典对照基线。它是**非学习、纯启发式、本地信息**的代表：不训练、不预测、不集中。与 J68GU76W（GEO 集中控制 + 残差 RL）形成对照：J68 也做"机会式转发"，但那个"机会"是"谁能看见网关"，ELB 的"机会"是"谁不拥塞"。与 JLF7IEBQ（SaTE，集中式 TE + GNN）也形成对照：SaTE 追求**算得快**，ELB 根本不做全局优化、只做**邻居间告警**。它引用的 Sun & Modiano [13]、CEMR [22]、Henderson & Katz [14]、PRP [21] 都是 LEO 路由的经典谱系。

**9. 对"负载变化下到达率/时延"的贡献**
**贡献很大，而且是本批目前为止最直接的一篇**：
- **给出了"到达率 → 丢包概率"的闭式关系**：$p=min(1,rac{delta+d}{delta_d})$，$delta_d=rac{(Q_l-q(t))cdot P_{avg}}{I-O}$（式 1–2，L72/L84）。**这是"输入速率 I 与输出速率 O 之差"直接决定排队溢出速度**的显式表达——正是"负载变化下到达率"这件事的机理内核：负载超过服务能力时，剩余缓冲被填满的时间与 (I−O) 成反比。
- **给出了排队时延的估计式**：$T_B(t)=rac{1}{Delta}int_{t-Delta}^{t}q(i)rac{P_{avg}}{C}di$（式 9，L137）——把队列占用积分换算成时延，是可复用的**队列→时延换算**。
- **实测了"负载 → 时延"的转折**：L256 逐字："When the traffic load is heavy, normal DSP exhibits the minimum average delay. However, this comes at the price of significant packet drops"——**重载下"最小时延"与"不丢包"不可兼得**：短路由时延最低但丢包最多，ELB 牺牲单流时延换低丢包。这条 trade-off 的定性结论对本选题很关键。
- **给出了负载的空间不均匀性事实**：Fig 6 逐星排队时延显示北美/西欧/东亚最高——即**负载不是全局均匀标量，而是地理局部化的**，这直接支持"到达率应按足迹人口加权"的建模（与 J68GU76W 式 4 的人口积分到达模型呼应）。
- **但**：它没有把时延作为"负载的连续函数"画成曲线（只有不同速率下的 CDF 与均值柱状），也没有区分传播/排队/改道额外跳数的时延分解。

**10. 一句话评价**
**LEO 负载均衡的奠基性工程解法**：把"拥塞通告"从"事后丢弃反馈"提前到"事前状态播报"，并把阈值参数用丢包概率闭式反解出来——它的价值在**参数化思想**（α、β、χ 由队列/速率/时延推出，而非手调）；局限则在于拓扑静止、信道无差错、负载只做静态扫描，本质上仍是**用本地队列信息做启发式分流，没有把"到达率如何演化"纳入模型**。


## JS857IYN — Time-Dependent Network Topology Optimization for LEO Satellite Constellations

**1. 一句话**
不换路由算法，改**星间链路本身怎么连**：把 LEO 星群的 ISL 拓扑设计写成"最大化容量 + 最小化时延 + 抑制链路抖动"的多目标问题，用**动态时间扩展图（DTEG）+ 动态规划**把它化成每颗星的一个**打分函数**，每颗星每步按分数挑 top-U（U=4）邻居建链。

**2. 问题设定**
默认的 **+Grid** 拓扑（每星连同轨两个 + 邻轨两个）建立在"理想星座"假设上：轨道面等间距、同轨卫星等间隔、近地点相近。作者用真实 TLE 数据指出**真实星座根本不理想**（L42 逐字："Not all orbital planes are parallel; some orbits intersect with others... The inclinations and RAANs of all orbits are not equally spaced"）。后果：+Grid 选出来的邻居**不对齐最优路由**、跳数暴涨。更关键的是既有工作（[22][24][25]）只看**当前时刻**的性能，而卫星 7.66 km/s，**上一步选中的邻居下一步可能已经跑远**（L44）。

**3. 方法骨架**
非 RL，是**动态规划 + 打分函数**：
- **优化问题 P1（式 10，L131）**：$max sum_isum_j phi_{i,j,t}left(S_{i,j,t}+rac{1}{L_{i,j,t}}+phi_{i,j,t-1}ight)$，约束 C1 每星最多 U 条链路、C2 ISL 双向对称、C3 星间可见（三角形高 $Gamma_{i,j,t}>Gamma_{Atmos p}$，式 6）、C4 距离 $<D_{Max}$。注意第三项 $phi_{i,j,t-1}$——**上一时刻同一条链路存在就给加分**，这就是"抑制抖动"的实现方式（式 10 下方 L134 解释）。
- **DTEG 图（第 III.A 节）**：把 T 切成 τ 的时隙，展开成 (T̂+1) 层，节点 $v_{i,t}$，空间链路 $(v_{i,t},v_{j,t+1})$（L146）。
- **归一化 + 打分（式 11–13，L158/L170）**：$ar S,ar L,arphi$ 各自除以时变最大值归到 [0,1]（式 12 的 $g_{Max,t}=max{g_{Max,t-1},max_{i,j}g_{i,j,t}}$，**历史最大值单调不减**）。链路代价 $A_{i,j,t}=w_1ar S_{i,j,t}+w_2(1-ar L_{i,j,t})+(1-w_1-w_2)arphi_{i,j,t-1}$（式 13）。
- **分数递推（式 14/16）**：$alpha_{i,j,t}=mathbb 1_{{Gamma>Gamma_{Atm}}}mathbb 1_{{D<D_{Max}}}(A_{i,j,t}+Pi_{j,t-1})$，$Pi_{i,t}=rac{1}{U}sum_jphi^*_{i,j,t}(A_{i,j,t}+Pi_{j,t-1})$（式 16，L188）——**把邻居的历史分数带进来**，这是"时间依赖"的核心，也是它跟 greedy 的唯一区别。
- **选链（式 15）**：在双方都还没满 U 条的前提下选最优链；C2 通过 $phi^*_{j,i,t}=phi^*_{i,j,t}$ 强制双向。
- **两个引理**：Lemma III.1（式 12 的时变最大值确实是历史最大值，归纳法证明，L191–L199）；Lemma III.2（分数函数**不会发散**，$Pi_{i,T}<infty$，L201–L211）。
- **上层路由（L252）**：在 DoTD 造出的拓扑上跑 **OSPF**（交换 IP 与分数）。
- **复杂度**：$mathcal O(hat T M^2)$，把 $hat T=T/	au$ 视为常数后 ≈ $mathcal O(M^2)$（L215）。

**4. 它声称的效果**
- 摘要（L56）：相对 **Greedy** 平均容量 **+28.09%**、跳数 **−10.91%**、时延 **−39.71%**；相对 **+Grid** 容量最高 **+70.47%**、跳数最高 **−81.82%**、时延最高 **−96.61%**。
- 单场景实例（L282）：纽约→旧金山，**DoTD 只需 5 跳，Greedy 6 跳，+Grid 多达 22 跳**。
- 时延单点数字（L284）：悉尼→达尔文，**DoTD 4.2 ms，Greedy 9.9 ms，+Grid 高达 203.6 ms**。
- 链路抖动（Experiment 3，L296）：监测 **3 小时 20 分**（2024-06-10 08:23 → 11:03），统计相邻两步保持同一条 ISL 的次数，DoTD 最多。
- **基线**：Greedy、+Grid。**明确声明不评估 ×Grid 与 Motif**（L282 逐字："Therefore, we do not present performance evaluations for ×Grid and Motif in comparison to our proposed algorithm."）。

**5. 它的实验条件**
- **无流量模型、无到达率、无队列、无负载**——容量就是每链路的香农容量 $S_{i,j,t}=B_{12G}log_2(1+SNR)$（式 8），**与是否有业务无关**。
- 星座：**真实 TLE**，CelesTrak 2024-06-10 08:23:00 UTC 快照，**907 颗星**（Table I，L255）。
- 参数（Table I）：载频 12.2 GHz、带宽 100 MHz、$D_{Max}=7000$ km、U=4、$w_1=w_2=0.4$、GS 天线 33.2 dBi、星上天线 40 dBi、偏振损耗 4.5 dB、失配 0.5 dB。
- 场景：**5 组 GS 源–目的对**（Table II：悉尼→达尔文、迈阿密→卡尔加里、纽约→迈阿密、纽约→旧金山、金边→加德满都），全部是**两个地面站之间的单条路径**。
- 仿真平台：**xeoverse [26] 增强版 + SpaceNet**（基于 Mininet），开源 [1]。
- 时间粒度：τ 秒级（如 1 s），拓扑更新周期 T **数分钟量级（如 10 分钟）**（L252）。

**6. 它自述的局限**
- **拓扑更新不能太快**（L252 逐字）："This update interval is restricted by constraints related to configuration complexity, service continuity, and stability, which prevent updates at sub-second intervals."
- **只做 OSPF，未优化**（L302 逐字）："This study applies OSPF routing over the created network topologies. One line of future work is exploring other emerging hierarchical routing algorithms [40], or to optimize OSPF weights [39]."
- **未来工作才提"端到端路由 + 地面站位置 + CDN"**（L302），等于承认当前没考虑。
- **主动放弃两个更强基线**（L282）：×Grid 与 Motif 不参与对比——理由是同为邻居式连接会同样退化，**但这是论证不是测量**。
- **QoS/拥塞/丢包全文未提**。

**7. 它没做但看起来能做的地方**
1. **完全没有负载维度**：容量是香农上界，不是"能承载多少需求"。所以"容量 +28%"到底在什么负载下有意义，无法回答——链路更快的拓扑在轻载下与慢拓扑无差别。
2. **式 9 的时延定义量纲错了**：$L_{i,j,t}=rac{c}{D_{i,j,t}}$（L123），而传播时延应为 $D/c$。写成 $c/D$ 得到的是"每秒"，不是秒。此外式 15 用 **argmin** 选 α，但 α 是**越大越好**的打分（L155、L173 都写"highest scores"），Algorithm 1 第 19 行也写 argmin——**最大化目标却用最小化算子**，是内部不一致。这两处让人无法独立复现它报告的 4.2 ms。
3. **只测 5 条固定 GS 路径**，且都落在北美/亚太，没有全球平均，也没有对**卫星位置采样多个时刻**做统计（只在 08:23:00 一个快照上算路由）。
4. **打分权重 $w_1,w_2$ 固定 0.4/0.4**，全文无敏感性分析——而它自己说三个目标的量纲不同才要归一化，那么权重理应更敏感。
5. **Π 的递推引入了"历史声誉"**，可能造成**拓扑锁死**（高分邻居一直被选），而它恰恰以"抑制抖动"为卖点——**抑制抖动与探索新链路之间的张力**完全没有讨论，也没有指标去衡量（比如"多少比例的链路是历史惯性导致的"）。
6. **U 固定为 4**。真实星上光端机数量确实是约束，但换个 U 会怎样，未测。

**8. 和同批其他篇的关系**
与 **JS857IYN 的对立面 JLF7IEBQ（SaTE）** 构成有趣对照：SaTE 认为**拓扑给定、只优化流量分配**，DoTD 认为**流量不管、只优化拓扑连接**。两者都把对方那一半当成黑箱。与 **JP79GMZS（ELB）** 对照：ELB 完全不动拓扑（固定 +Grid / Iridium-like 4 邻居），靠改道分流；DoTD 恰恰说固定邻居网格是原罪。与 **J68GU76W** 对照：J68 也做"邻居选择"，但把选邻居当作 RL 动作，DoTD 用动态规划打分。它引用了 **Handley 谱系之外的 [17] Bhattacherjee & Singla "Network topology design at 27,000 km/hour"** 与 **[16] ×Grid**，这两篇是"拓扑设计"子方向的源头。它也引用了 **[40] Stable Hierarchical Routing**（与 JLF7IEBQ 引用同一篇，说明这是该领域的公共锚点）。**未见引用本批其他 10 篇**。

**9. 对"负载变化下到达率/时延"的贡献**
**没有直接贡献**——全文没有到达率、没有队列、没有负载扫描，容量是链路香农容量而非承载需求，时延是纯传播时延（且定义有量纲问题）。**但有两条外围事实值得记**：
- **拓扑重配的时间尺度下界**：作者明确说重配**不能做到亚秒级**，因为配置复杂度、服务连续性与稳定性（L252）。这与 JLF7IEBQ 实测的 **THT 70 ms** 形成一个尖锐矛盾：物理拓扑 70 ms 就变了，而工程上可接受的重配周期是分钟级——**"负载响应"必须在这个夹缝里找空间**。这是一条对整个选题有用的约束。
- **时延作为一个可设计目标被显式纳入**：它的确把 1/L 写进了目标函数（式 10 第二项），给出了"拓扑选择能带来 4.2 ms vs 203.6 ms 量级差异"的证据——说明**时延对拓扑极度敏感**，但这是传播时延，不是排队时延。

**10. 一句话评价**
**把"时间扩展图"这一经典工具用到 ISL 拓扑设计上，用历史分数把静态贪心变成动态规划**——方法上是干净的，但代价是**彻底剥离了流量**：没有负载、没有到达率、没有队列，所以它优化的是"这条链路物理上有多快"，而不是"在真实负载下这条链路会不会堵"。属于"把已有 X（DTEG/DP）用到 Y（星间拓扑）上、未改 X"。


## JSX5XG88 — High-Dimensional Continuous Control Using Generalized Advantage Estimation

**1. 一句话**
提出 **GAE(γ, λ)**：把优势函数估计写成 $\hat A_t=\sum_{l=0}^{\infty}(\gamma\lambda)^l\delta^V_{t+l}$——一个由 TD 残差构成的指数加权和，用一个参数 λ 在"偏差/方差"之间连续调节，从而让策略梯度在神经网络的函数逼近下也能稳定跑起来。

**2. 问题设定**
策略梯度有两难（L11 摘要逐字）：**样本量太大**，且**数据非平稳导致训练不稳**。用 value function 降方差会引入偏差，而偏差更致命（L19 逐字："bias is more pernicious—even with an unlimited number of samples, bias can cause the algorithm to fail to converge, or to converge to a poor solution that is not even a local optimum."）。这篇要的是：**在可容忍偏差下把方差大幅压下去**。这是纯 RL 方法论问题，与任何具体网络场景（更不必说卫星）无关。

**3. 方法骨架**
- **设定（第 2 节）**：**无折扣**的目标 $\max\sum_t r_t$，γ 不用来表示目标折扣，而是当作**算法层的降方差参数**（L35 逐字："we are not using a discount as part of the problem specification; it will appear below as an algorithm parameter that adjusts a bias-variance tradeoff"）。这是理解全文的关键。
- **策略梯度的统一形式**：$g=\mathbb E[\sum_t \Psi_t\nabla_\theta\log\pi_\theta(a_t|s_t)]$（式 1），$\Psi_t$ 可取 6 种形式（总回报 / 后续回报 / 带基线的 / Q / A / TD 残差，L45–L49）。
- **γ-just 的定义**（Definition 1，式 7，L85）：把估计量 $\hat A_t$ 代进式 6 后无偏，就叫 γ-just。**Proposition 1**（L99）：只要 $\hat A_t=Q_t-b_t$ 且 $Q_t$ 是 $Q^{\pi,\gamma}$ 的无偏估计、$b_t$ 只依赖 $a_t$ 之前的信息，就是 γ-just。
- **k 步估计与 telescoping**：$\hat A^{(k)}_t=\sum_{l=0}^{k-1}\gamma^l\delta^V_{t+l}$（式 14，L144），k→∞ 退化为"经验回报 − 基线"（式 15）。
- **GAE（核心，式 16，L158）**：对这族 k 步估计做指数加权平均，化简为 $\hat A_t^{\mathrm{GAE}(\gamma,\lambda)}=\sum_{l=0}^\infty(\gamma\lambda)^l\delta^V_{t+l}$。
- **两个特例（式 17/18）**：$\lambda=0$ → 单步 TD 残差（低方差、$V$ 不准时有偏）；$\lambda=1$ → 经验回报减基线（**无论 $V$ 准不准都 γ-just**，但方差大）。L173 逐字："GAE(γ,1) is γ-just regardless of the accuracy of V, but it has high variance"。
- **γ 与 λ 的分工（L175）**：γ 即使 $V$ 精确**也**引入偏差；λ 只在 $V$ 不精确时引入偏差，所以**最优 λ 通常远小于最优 γ**。
- **奖励塑形解释（第 4 节）**：令 $\Phi=V$，塑形奖励 $\tilde r$ 恰是 Bellman 残差 $\delta^V$（式 25，L222）——即 GAE = 对塑形后的奖励再打一个"更陡的折扣" $\gamma\lambda$。定义**响应函数** $\chi(l;s_t,a_t)=\mathbb E[r_{t+l}|s_t,a_t]-\mathbb E[r_{t+l}|s_t]$（式 26，L230），把优势按时间步分解；用 $\gamma<1$ 相当于丢掉 $l\gg 1/(1-\gamma)$ 的项，只要 $\chi$ 衰减够快，误差就小（L241）。
- **值函数估计（第 5 节）**：对 $V_\phi$ 也用**信赖域**（式 29/30），约束是"新旧值函数之间的平均 KL ≤ ε"，用**共轭梯度**解（L263–L269）。动机是**防止过拟合到最新一批数据**。
- **交错更新顺序很讲究（L307）**：策略更新 $\theta_i\to\theta_{i+1}$ 用的是 $V_{\phi_i}$ 而不是 $V_{\phi_{i+1}}$；否则会引入额外偏差——极端情形下若 $V$ 过拟合使 Bellman 残差处处为零，**策略梯度会整个变成 0**。
- **实验算法（第 6.1 节）**：策略更新用 **TRPO**（式 31）。

**4. 它声称的效果**
- **Cart-pole**（21 个随机种子平均，L339）：最优区间 $\gamma\in[0.96,0.99]$、$\lambda\in[0.92,0.99]$——**中间值最好**（Fig 2）。
- **3D 双足行走**（9 次试验平均，L353）：最优 $\gamma\in[0.99,0.995]$、$\lambda\in[0.96,0.99]$，1000 次迭代后得到"fast, smooth, and stable gait that is effectively completely stable"。折算真实时间 **5.8 天**（0.01 s/步 × 50000 步/批 × 1000 批）。
- **四足行走 / 双足站起**（各 5 次试验，L357）：固定 $\gamma=0.995$，$\lambda\in\{0,0.96\}$ 加上"无值函数"条件；四足最优 $\lambda=0.96$；站起任务中**值函数总是有帮助**，但 $\lambda=0.96$ 与 $\lambda=1$ 差不多。
- **"No VF" 基线**（L335）：用**只依赖时间、不依赖状态**的基线（按批内每个时间步对回报取平均）。
- **规模**：人形 33 维状态 + 10 个致动自由度；四足 29 维 + 8 个；策略与值函数网络各 **3 隐层（100/50/25 tanh）**，各超过 $10^4$ 参数（L315, L23）。

**5. 它的实验条件**
- **完全不是网络/通信场景**：任务是 **cart-pole 平衡** + 三个 **MuJoCo 仿真的 3D 机器人运动**任务（双足行走、四足行走、双足从躺姿站起）（L311）。
- 时步 0.01 s；每 episode 2000 步后截断；批大小：双足 50000 步/批，四足与站起 200000 步/批（L324）。
- 奖励函数显式给出（L327）：双足 $v_{\mathrm{fwd}}-10^{-5}\|u\|^2-10^{-5}\|f_{\mathrm{impact}}\|^2+0.2$；四足 $v_{\mathrm{fwd}}-10^{-6}\|u\|^2-10^{-3}\|f_{\mathrm{impact}}\|^2+0.05$；站起 $-(h_{\mathrm{head}}-1.5)^2-10^{-5}\|u\|^2$。常数项的作用是**鼓励更长的 episode**，否则二次惩罚会让策略倾向于尽快结束（L331）。
- 算力：双足每次试验约 2 小时（16 核）；四足/站起每次约 4 小时（32 核）。
- 训练与评估同一套仿真环境，无跨任务/跨分布测试。

**6. 它自述的局限**
- **对 γ、λ 的自适应调节是未来工作**（L368 逐字）："A possible topic for future work is how to adjust the estimator parameters γ, λ in an adaptive or automatic way."
- **值函数误差与策略梯度误差的关系未知**（L370 逐字）："One question that merits future investigation is the relationship between value function estimation error and policy gradient estimation error."
- **λ=0 偏差过大**（L398 逐字）："We have found that the bias is prohibitively large when using a one-step estimate of the returns, i.e., the λ = 0 estimator"。
- **分析是"直观但非形式化"的**（L366 逐字）："We have provided an intuitive but informal analysis of the problem of advantage function estimation"。
- 与同期确定性策略梯度方法（DDPG/SVG）的比较**留作未来工作**，且指出那些工作的问题维度远低于本文（L374）。

**7. 它没做但看起来能做的地方**
1. **γ、λ 全靠人工网格搜索**（Fig 2 就是一张 γ×λ 的热力图）。作者自己把它列为未来工作（L368）——这是本文最明显的、被作者亲口承认的缺口。
2. **γ 被当成纯降方差参数，因此"折扣"不再对应任何语义上的时间偏好**（L35）。这意味着**用它做长时程信用分配时，"看得多远"是被降方差需求而非任务需求决定的**——对"负载变化"这类需要长记忆的任务，这个替代关系没有被讨论。
3. **响应函数 χ(l)** 被定义出来了（式 26）却**只用于解释，从未被测量**。它是一个可观测的诊断量（"动作的影响多久被遗忘"），但论文没有用它来指导 λ 的选择——明明可以直接估计 $1/(1-\gamma\lambda)$ 与 χ 的衰减尺度对比。
4. **所有实验都是单智能体、低维动作空间（≤10  actuators）**。多智能体/大规模动作空间（如 LEO 路由中每条 ISL 一个二值动作）会怎样，完全没测。
5. **值函数的信赖域只在防止"对最新一批过拟合"上被论证**（L255），没有做消融证明它比简单回归（式 28）好多少。

**8. 和同批其他篇的关系**
**这篇是本批的方法论底座，不是 LEO 论文**。同批中任何用策略梯度类 RL 的 LEO 路由论文（如 S85KQ4FC 锚件卡里的 DRL 系列，以及本批 J68GU76W 用的 DDQN——虽然 DDQN 是值方法不用 GAE）都可能用到它的技术。它引用的谱系是：Sutton & Barto 教材、Konda & Tsitsiklis（actor-critic）、Kakade（自然策略梯度）、Ng et al.（奖励塑形）、Schulman et al. 2015（TRPO）、Lillicrap et al. 2015（DDPG）。**未见引用任何 LEO/卫星文献，也未被本批其他篇直接引用**。

**9. 对"负载变化下到达率/时延"的贡献**
**没有直接贡献**——零。全文没有网络、没有队列、没有到达率、没有时延，一个数字都不沾。
**但有一条间接的、值得记录的事实**：它明确指出 **γ 作为降方差参数时，"折扣"不再有语义**（L35），且**λ<1 只在 $V$ 不准时引入偏差**（L175）。这对"用 RL 学路由"这件事的意义是：**当研究人员为了训练稳定而调小 γ 时，agent 实际上"看不见"比 $1/(1-\gamma)$ 更远的效果**。在负载变化的场景下，如果"负载升高 → 排队 → 丢包"这条因果链的延迟超过了 $1/(1-\gamma)$ 步，**策略在结构上就不可能学到它**。这条推论是本文给本选题的**唯一**可用线索，且需要我们自己推。

**10. 一句话评价**
**策略梯度方差缩减的经典构件**——把 TD(λ) 的思想从"估计值函数"搬到"估计优势函数"上，用 λ 一个旋钮统一了"单步 TD"与"蒙特卡洛回报"两极；在方法谱系里属于**被反复征引的基础设施**，而不属于 LEO 路由这条具体的研究线。对卫星/负载选题而言，它是一把好用的螺丝刀，不是一个关于网络的发现。


## JZA5SEQA — Fast Reroute Algorithms for Satellite Network with Segment Routing

**1. 一句话**
把**快速重路由（FRR）**搬到卫星网上，用**段路由（SR）+ 混合路由**的分工解决"星上算力不够"：把中继卫星分成**计算卫星**和**转发卫星**，计算星预先算好备份路径、转发星只管查表转发；配套两个算法——**DOD**（把普通节点分配到各域）和 **BKM**（链路失效时增量维护备份路径，不全局重算）。

**2. 问题设定**
LEO 比 GEO 单向链路时延低，但**链路可变、不稳定**，导致时延更高、失效更多（L17 摘要）。而 FRR 需要**较大的计算资源**，星上资源却很有限（L17 逐字："FRR need relatively large computing resources while satellites have limited resources"）。传统路由因为拓扑频繁变化 + 算力差，无法直接用（L27）。既有工作要么集中式（耗控制器算力、有单点故障），要么分布式（控制灵活性差）（L71）。

**3. 方法骨架**
非 RL，是**架构 + 两个启发式算法**：
- **SS-FFR 架构（第 III.A 节）**：地面控制中心仍是主控，另选一批**稳定中继卫星**当卫星控制面，再细分为**计算星**（收集邻近链路状态、算路径、定期与地面中心交换、链路变化后更新转发表的）和**转发星**（存路径、标标签、转发）。失效时转发星**直接切到备份路径**，同时计算星算新备份路径（L84）。**用 ISL 替代星地链路来传控制信息以降低时延**（L86）。
- **中继星选取（第 III.B 节）**：优先选**不过极区**、剩余正常工作时间长的星。$work\_time_i = avg\_age - age_i$（式 1，L104）；权重 $\Delta_i=\alpha\cdot work\_time_i+\beta\cdot UDL_i$（式 2，L110）；配对时最大化式 3（含两侧权重、存储、算力，**除以两星距离**——即越近越好）；把剩余节点分域时最小化加入后的平均距离（式 4），约束是 $mem_i>0$、$cpu_i>0$（式 5/6）。资源用尽时**把平均距离最长的节点换出**，塞进满足条件的新域（L135）。
- **DOD 节点分区算法（Algorithm 1，L147）**：三步——①按距中继星最近原则分配、标记"临时分配"；②处理临时分配（若只被一个域临时占用则转"确认"）；③对剩余节点计算加入各域后的 avg_dis，选最小者。复杂度 $\mathcal O(len^3+len^2)$，仍属多项式（L159）。
- **BKM 备份路径维护算法（Algorithm 2，L212）**：输入初始路径集 I、备份路径集 B、故障链路 $e_{u,v}$。**Step 1**：把受影响的初始路径换成其备份路径，并把 $B(e_{u,v})$ 从 B 中删除。**Step 2**：对所有包含 $e_{u,v}$ 的备份路径，**基于下一跳原则**在 I 里 DFS 搜索新路径，用并集拼出新备份路径；搜不到就标为不可达（L217–L240）。核心卖点是**不重算全部备份路径**。
- 备份路径计算分"下一跳式"与"全局式"，作者选择前者，因为它**算力开销小、更适合星上**（L205）。

**4. 它声称的效果**
- **DOD vs SDF（贪心）vs LFR[33]**：平均距离更低——**220 个节点时 DOD 平均距离 4，SDF 为 24，LFR 为 20**（L169）。
- **存储资源利用率**：最好情况下（120 节点）**DOD 比 SDF 好 30.9%、比 LFR 好 13.6%**（L189）。
- **计算资源利用率**：三者**没有明显差别**（L189，作者归因于节点数对算力影响小、且算力开销难以比较）。
- **高负载（500 节点）**：DOD 比 SDF 多容纳 2 个节点、比 LFR 多 1 个；资源利用率高 1%（L191）。
- **BKM vs Dijkstra vs LFA+[34]**：链路失效率 10% 时，**BKM 比 Dijkstra 好 74.3%、比 LFA+ 好 60.0%**（L253，指更新耗时）。
- **NS2 时延实验**：BKM 与 LFA+ 基于下一跳的备份路径**长度大于 Dijkstra 的最短路备份路径**，且有些路径连不通（L258）。

**5. 它的实验条件**
- **DOD 实验是抽象实验，不是卫星仿真**：节点**随机撒在一个 100 单位的平面上**，共 12 个域，每种规模跑 **10 次取平均**（L165）。也就是说：**没有轨道、没有卫星运动、没有 ISL**——这是一个纯几何分区问题。
- **BKM 实验**：**NS2** 仿真，**Teledesic 星座，12 个轨道面 × 每面 24 颗 LEO**，每面**一颗独立路由计算卫星**，面内数据全经它转发；**ISL 容量 155 Mb**；面间 ISL 按卫星运动方向开/关；**仿真时长 = 一个轨道周期 6794 秒**；**每 30 秒发一个数据包**测平均时延（L258）。
- 无流量模型、无到达率、**每 30 秒一个包**相当于极轻负载（1 包/30 s）。
- 训练/评估：无训练过程（非学习方法）。

**6. 它自述的局限**
- **BKM 实现复杂、结果依赖实现方式**（L265 逐字）："The experimental results show that the BKM algorithm can help accelerate the update of some backup paths, but its implementation is more complicated, and the availability and length of the backup paths are affected by the implementation method. Therefore, the BKM algorithm needs further optimization."
- **计算星仍需与地面高频通信**（L269 逐字）："However, computing satellites still need to maintain high-frequency periodic contact with the ground."
- **NS2 实验中部分路径连不通**（L258 逐字）："in actual situations, some paths cannot be connected, which is related to the specific implementation of the algorithm."
- **计算资源利用率无法有效比较**（L189）——等于承认这个指标没测出来。

**7. 它没做但看起来能做的地方**
1. **摘要与正文严重不一致（这是最硬的问题）**：摘要（L17）写"the proposed **LFR** algorithm is 30.9% better... and the proposed **LFA+** algorithm is 74.3% better"，但正文里 **LFR[33] 与 LFA+[34] 都是基线**，30.9% 是 DOD 相对 SDF 的存储利用率优势（L189），74.3% 是 BKM 相对 Dijkstra 的更新耗时优势（L253）。**摘要把两个基线算法说成了自己的算法**。这让论文的贡献陈述无法直接采用。
2. **参考文献 [25] 与 [34] 是同一篇**（Zhang S, Li X, Yeung K L, L321/L339）。
3. **相关工作里塞了与主题无关的引用**：L51 讨论 FRR 前景时引用了 [10] 夜间图像去雾、[11] 夜间图像去霾——与卫星路由毫无关系。
4. **DOD 的"高负载"是指"中继星承载的节点数"，不是"流量负载"**（L191），但用词容易误导。
5. **BKM 只在 LEO 单点/多点随机失效下测**，没有测**失效与拓扑变化叠加**的情形——而 LEO 里拓扑变化本身就在持续制造"失效"。
6. **备份路径长度代价没有被量化成时延**：作者知道下一跳式备份路径更长（L258），但只画了平均时延图，没有给出"多一跳 = 多多少 ms"的分解。
7. **没有和任何"不预设备份路径"的在线重算方案对比端到端时延**，只有耗时对比。

**8. 和同批其他篇的关系**
与 **S85KQ4FC（锚件卡）** 的那条主线呼应：**"星上资源有限"被当作一等约束**——S85 关心的是"推理算力"，JZA5SEQA 关心的是"路径计算算力"和"转发表存储"。两者都在说同一件事：**LEO 路由的瓶颈不只是链路，还有星上资源**。与 **JS857IYN（DoTD）** 对照：DoTD 改拓扑连接、JZA5SEQA 改控制面分工，前者假设星上不用算（集中算），后者恰恰反对把一切都压给中心。与 **JP79GMZS（ELB）** 对照：ELB 用**信令**通知邻居改道，JZA5SEQA 用**预置备份路径**，一个反应式一个预置式。它引用的 [9] OPSPF、[25]/[34] Zhang 的 SR 卫星论文是该子方向的锚点。**未见引用本批其他 10 篇**。

**9. 对"负载变化下到达率/时延"的贡献**
**没有直接贡献**——它研究的是**失效恢复**，不是负载。全文没有到达率、没有业务流量模型，NS2 实验里**每 30 秒才发一个包**，是极端轻载，排队时延根本不显现。所谓"high load"指的是分区算法的节点容量压力（L191）。
**但有一条外围事实值得记**：它明确量化了"**可靠性换时延**"的代价——基于下一跳的备份路径**比最短路更长**（L258），即**故障恢复路径的时延一定劣于正常路径**。另外，与 S85KQ4FC 一样，它把**星上计算/存储资源的稀缺性**作为设计前提（L17、L205），这对"负载升高时星上处理能力先饱和还是链路先饱和"这个问题提供了一个侧面论据：**星上算力可能比带宽更早成为瓶颈**。

**10. 一句话评价**
**把地面 FRR/SR 的成熟工具箱（备份路径 + 段路由 + 集中/分布混合）搬到卫星网，并给出两个具体的分区与维护算法**——工程动机（星上算力有限）是真实的，但实验做在"平面上随机撒点"和"每 30 秒一个包"的极简设定上，**摘要还把两个基线算法说成自己的算法**，结论的可采信度受限。


## K7U4TYJN — SKYLINK: Scalable and Resilient Link Management in LEO Satellite Networks

**1. 一句话**
把每颗星变成一个**独立的多臂老虎机（MAB）**：用 **UCB + tile coding** 只根据"到邻居的距离"这一个上下文，给自己的各条出边排一个优先级列表，再按**注水（water-filling）**把进来的流量灌进去——全程**不用任何全局信息、不用中心控制器**，目标是同时压低**平均时延**与**丢包率**的加权和。

**2. 问题设定**
三条罪状针对既有方案（L25）：① 最短路（Dijkstra/k-shortest）会让大量路径**重叠在同一条 GSL 上**，在高密度区或 GSL 容量受限处形成瓶颈；② 学习类方案（DQN）与最短路一样**依赖中心控制器**（通常在地面，因为星上算力有限），需要持续收集全局状态 → 对拓扑变化的**响应慢**、通信开销大；③ 中心依赖还**降低韧性**（失效必须被中心发现才能处理）。它点名既有工作"考虑 mega 星座但只看预定义的源–目的对，而不是全网流量模式"，且**同时做到"分布式"与"抗失效"的工作是缺失的**（L53 逐字："a critical gap in the literature is the lack of approaches that simultaneously adopt a distributed framework and focus on resilience against network failures"）。

**3. 方法骨架**
- **系统模型（第 III 节）**：时隙制，τ 固定。星间是**全双工光 ISL**，星地是**半双工射频 GSL**，**每星最多 4 条 ISL**（同轨 2 + 邻轨 2，构成 +grid）；地面站有 $mu_i$ 副天线，接最近的 $mu_i$ 颗星（L63）。有向图 $mathcal G_t=(mathcal V,mathcal E_t)$，$mathcal V=mathcal Ncupmathcal Mcup{z}$（$z$ 是互联网节点）。
- **到达模型（式 1，L77，核心）**：$R^{mathrm g}_{n,t}=mathrm{Pop}_{n,t}cdot dcdot
ucdotmathrm t_{n,t}$ —— **该星覆盖范围内的人口数 × 人均设备数 × 每设备每秒流量 × 当地时刻缩放因子**。即**到达率 = 人口密度 × 日周期节律**。
- **缓冲与丢弃（第 III.C 节）**：每节点缓冲 $Q_v^{max}$。若出速率 < 入速率，缓冲被填满；**满则对所有入流按同一比例丢弃**使 $R^{mathrm{out}}=R^{mathrm{in}}$。**关键建模取舍（L82 逐字）**："Our model focuses on the steady state of buffers, either filled or empty, disregarding the transitional phases of filling or emptying." 丢包原因：链路容量不够、成环、无出边、时延超 $T_{max}$。
- **容量**：ISL 用光链路功率预算（式 2 接收功率含指向损耗与截获比例）→ 香农（式 4，含缩放因子 λ<1，因为只有部分容量能给用户数据）；GSL 用 EIRP/FSPL/大气衰减（式 5–8），**天空噪声温度 $T_{sky}$ 随仰角变化**（式 8）。
- **时延（式 10–12）**：传播 $D^{mathrm{Tx}}=d/c$；**排队时延（式 11，L161）**：$Delta_C:=R^{mathrm{in}}-summin(x,C)$，若 $Delta_Cle 0$ 则 $D^q=0$，否则 $D^q=rac{Q_v^{max}}{sum_{(v,w)}min(x_{(v,w)},C_{(v,w)})}$；路径时延 $D_X=min(sum D^{mathrm{Tx}}+D^q, T_{max})$。
- **目标（式 13–15）**：$c_{v,t}=rac{sum_X R_X D_X}{sum_X R_X}$（**按流量加权的平均路径时延**），全网 $c_t=rac{sum_n R^{mathrm g}_{n,t}c_{n,t}}{sum_n R^{mathrm g}_{n,t}}$。**丢包之所以能被"联合最小化"，是因为被丢弃的数据被记为时延 $T_{max}$**（L186 逐字："As dropped data contributes the highest possible delay of $T_{max}$ to $c_t$, considering $c_t$ as the optimization target leads to a joint minimization of average delay and drop rate."）——**这是一个把丢包折算成时延的加权技巧**。
- **SKYLINK（第 V 节）**：
  - **动作是连续的**（各链路的流量分配），MAB 处理不了 → 先**给链路排序**，再按序注水（L205），容量用满才灌下一条。
  - **UCB（式 16）**：$mathrm{UCB}^g_t(v,w)=ar c_{v,w}(g,d)-sqrt{rac{2log t}{n(v,w,g,d)}}$——**是减号**，因为目标是最小化 cost，**低分 = 高偏好**。
  - **上下文 = 到邻居的距离**，用 **tile coding** 量化成**重叠的若干分区**（例：500 km 一段），每个 tile 独立学习，最后对 |G| 个分区取平均（式 17）。
  - **注水（式 18/19）**：前 i 条用满 $sigma C_j$，第 i+1 条补足余额，其余为 0；链路内部再按**入流比例分摊**。$sigma<1$ 是**容量不确定性折扣**，防止高估容量导致高丢包（L227）。
  - **复杂度（第 V.E 节）**：$mathcal O(k|mathcal G|+klog k)$，**与星座规模、用户数无关**（因为 k 受可见地面站数限制，不超过 4+可见 GSL）。
- **仿真器（第 VI 节）**：用 **CosmicBeats** 预算位置，flow-level（stream-based）仿真，**不实例化单个包**。

**4. 它声称的效果**
- **摘要（L17）**：2540 万用户下，加权 cost 比 bent-pipe **降 29%**、比 Dijkstra **降 92%**；丢包率比 k-最短路**降 95%**、比 Dijkstra **降 99%**、比 bent-pipe **降 74%**；吞吐**高 46%**。
- **可扩展性（Fig 4，L327–L348）**：用户数 12.7 / 25.4 / 63.5 / 127 M。
  - 12.7 M 时：cost 比 k-最短路 −5.0%、比 NC-SKYLINK −11.3%、比 bent-pipe −29.5%、比分布式 Q-learning −29.8%、比 random −54.4%、比 Dijkstra −84.6%。
  - 25.4 M 时：比 Dijkstra −91.7%、k-最短路 −64.5%、random −52.5%、Q-learning −27.3%、bent-pipe −28.7%；上下文化本身（vs NC-SKYLINK）贡献 **+11.1%**。
  - **丢包率随负载的爆炸**（L348，本卡最有价值的数字）：**Dijkstra 从 15.6% 涨到 72.4%，k-最短路从 0.6% 涨到 38.6%**（12.7 → 127 M 用户）。
  - 25.4 M 时丢包率：比 k-最短路 −95.4%、比 Dijkstra −99.2%、比 Q-learning −56.1%、bent-pipe −75.6%、random −87.6%。**SKYLINK 与 NC-SKYLINK 的丢包率都是 0.3%**，所以 cost 的改善**全部来自平均时延更低**（L348 逐字："showing that the improvements in cost are due to the fact that SKYLINK achieves a lower average delay than NC-SKYLINK"）。
  - 吞吐：比 Dijkstra +45.8%、比 k-最短路 +6.0%。
- **一周时间序列（Fig 5–7）**：三条结论（L350 逐字）："(a) shortest-path algorithms lack scalability, (b) SKYLINK has a learning phase and converges within days, and (c) SKYLINK is resilient to fluctuations affecting other schemes"。**丢包率呈现日周期模式**（L362），最短路算法波动大、SKYLINK 几乎可忽略。
- **时延的关键反直觉发现（L364，本卡最重要的一条）**：最短路算法的**平均时延反而更低**，但那是因为**它们本来就送得少**——"favoring data that are closer to the ground"；SKYLINK 送的是那些会被最短路丢弃的数据。而 NC-SKYLINK 缺少上下文，会**渐进式"遗忘"**，时延越来越高。
- **韧性（第 VII.B 节）**：第 3 天起 3% 卫星 GSL 中断、第 5 天恢复。cost 上升：bent-pipe **+67.6%**、k-最短路 **+23.2%**、**SKYLINK <10%**。丢包率：k-最短路 5.7%→7.5%、bent-pipe 1.1%→3.7%、**SKYLINK ≤0.7%**。Dijkstra 的丢包率**始终 >12%**（大到被排除出图）。
- **跳数**：大多数数据在靠近地面站的高人口区，**平均跳数接近 1**；失效期间 SKYLINK 与 NC-SKYLINK 跳数显著上升（说明在改道）。
- **基线**：bent-pipe、Dijkstra、k-最短路（k=4）、random、分布式 Q-learning [24]，外加**消融变体 NC-SKYLINK**（去掉上下文与 tile coding）。

**5. 它的实验条件**
- **星座**：**OneWeb，636 颗**，近极轨 Walker Star；**146 个地面站**（全球最大城市）（L315）。
- **仿真参数（Table II，L317）**：时间步长 **τ=15 s**，总步数 **T=40320**（≈7 天），**TTL $T_{max}$=200 ms**，仿真起点 2023-09-28 08:26 UTC，**用户 25.4 M**（$d=0.003175$），**每设备上传流量 ν=22.98 kbps**；**缓冲：地面站 1 GB、卫星 50 MB**；地面站到互联网链路 50 Gbps、时延 1–5 ms；**ISL 带宽 5 GHz**、口径 10 cm、发散角 $1.744	imes10^{-5}$ rad、指向损耗 0.9、噪声温度 290 K、发射功率 0.1 W；**上行缩放 λ=0.08**；**GSL 带宽 250 MHz**、EIRP 34.6 dBW、$G_{rx}$=10.8 dB、载频 19 GHz。
- 每个实验**重复 R=100 次**取平均；各指标标准差 **<1%**。
- **负载扫描**：12.7 / 25.4 / 63.5 / 127 M 用户（锚定 Starlink 2026-01 预测的 12.7 M，再取 1×/2×/5×/10×）。
- **训练 = 评估**：在线学习（MAB 无离线训练），但**有数百到数千个时隙的学习期**（τ=15 s，一周 = 40320 步）。
- **参数调优（第 VII.C 节）**：距离量化精度扫 20–2000 km，分区数扫 1–6；**最优 = 500 km + 2 分区**。20–50 km 太细（每上下文样本太少），1000–2000 km 太粗（无法区分上下文）。
- **上下文消融（L397，重要负面结果）**：试过**卫星数据负载、当地时刻、UTC、卫星位置**，**全都不比"到邻居的距离"更好**，把它们加进去也不提升。作者归因于距离直接影响链路容量与时延。

**6. 它自述的局限**
- **缓冲只建模稳态**（L82 逐字，最关键）："Our model focuses on the steady state of buffers, either filled or empty, disregarding the transitional phases of filling or emptying."
- **流级模型、不实例化包**（L146 逐字）："We do not consider single packets. Drop rates are computed directly at the rate level in our stream-based model."；L296："Individual packets are not instantiated."
- **地面站选择的影响被排除**（L156 逐字）："While the choice of ground station does influence the actual delay, this effect is beyond the scope of this work."
- **未来工作才做大星座与其它 QoS**（L403 逐字）："In future work, we will scale our experiments to larger constellations (e.g., Starlink), incorporate alternative Quality-of-Service objectives, and integrate MEO and GEO satellites as well as airborne relays"；能耗对比也只是"an interesting direction"。
- **只测 GSL 失效**（L382 逐字）："We restrict our analysis to GSLs failures because they have the higher impact."——并说即使 50% 卫星失去全部 ISL，各方案 cost 上升也都 <10%，**因为瓶颈是 GSL 容量**。

**7. 它没做但看起来能做的地方**
1. **"缓冲只建稳态"这一条直接抹掉了负载瞬变**（L82）。负载变化最关键的物理过程恰恰是缓冲**填充的那段时间**——那正是排队时延从 0 涨上去的过程。作者把它显式排除了。**这是本选题最直接可切入的缺口**。
2. **排队时延是"阶跃函数"而非"负载的连续函数"**（式 11）：$Delta_Cle0$ 时为 0，一旦过载立刻跳到 $Q^{max}_v/	ext{出速率}$。也就是说论文里报告的"时延"在过载时其实是"**排空一整个满缓冲要多久**"，而不是当前队列长度对应的时延。**"负载 → 时延"曲线在这篇论文里被建模成了二值台阶**，中间那段连续过渡完全不存在。
3. **"卫星负载"作为上下文无效**（L397）——这是一个反直觉的负面结果，而它恰恰说明**在当前建模下负载信息对决策没帮助**。但这很可能是因为第 2 条（时延被建模成台阶，负载的细微差别不体现为 cost 差别）。**这两条限制是耦合的**，作者没有意识到。
4. **学习期长达数天**（L350）。τ=15 s 下一周是 40320 步。"负载变化"若发生在小时级以下，策略根本来不及。**收敛速度与负载变化速度的失配没有被讨论**。
5. **σ（容量折扣）与 tile coding 两个参数都是手工调的**，且 σ 的具体取值在正文没有给出。
6. **只用了一个星座（OneWeb 636 星）**；作者自认要扩到 Starlink。
7. **成本函数把丢包折算为 $T_{max}$ 的时延**（L186）——这是一个**人为的等价汇率**，权重由 $T_{max}$ 隐含决定。换一个 $T_{max}$ 会不会改变方案排序？没有做敏感性分析。
8. **平均跳数接近 1**（L389），意味着这个网络上绝大多数流量根本没走 ISL——**这篇论文的"路由"其实更像"选地面站"**。ISL 的价值在它的评测里被人口分布结构稀释了。

**8. 和同批其他篇的关系**
**这是本批（R6）里与选题最贴合的一篇**，且与多篇构成直接对照：
- vs **S85KQ4FC（锚件卡）**：S85 把"决策队列"当一等约束，SKYLINK 完全没有决策成本的概念（它的算法复杂度是常数级，这是它敢全分布式的底气）；S85 是集中式 GEO 控制 + DDQN，SKYLINK 是**彻底反中心**。
- vs **J68GU76W**：两者都用 RL/学习做转发，但 J68 是集中式残差 DDQN + 队列长度目标；SKYLINK 是分布式 MAB + 时延/丢包目标。
- vs **JLF7IEBQ（SaTE）**：SaTE 是中心化 TE，认为"算得快"是核心；SKYLINK 直接绕开计算问题——**它证明"不算全局最优"也能赢**。
- vs **JS857IYN（DoTD）**：DoTD 只优化链路拓扑的物理性能（无流量），SKYLINK 有完整流量模型。
- vs **JZA5SEQA**：JZA5SEQA 用预置备份路径换可靠性，SKYLINK 用在线学习换自适应。
- **它引用了本领域的关键文本**：[26] Handley "Delay is not an option"、[29] Li et al. "Stable Hierarchical Routing"（**与 JLF7IEBQ、JS857IYN 引用同一篇**，说明这是公共锚点）、[22] Deng et al. 距离 back-pressure、[19] Gounder k-最短路、[30] Lai et al. INFOCOM'23 韧性路由。**未见引用本批其他 10 篇**。

**9. 对"负载变化下到达率/时延"的贡献**
**本批目前为止贡献最大的一篇**，而且贡献的恰好是**负载 → 时延/丢包**这条曲线：
- **显式的、成规模的到达率扫描**：12.7 → 127 M 用户（**10 倍跨度**），并给出 **Dijkstra 丢包率 15.6%→72.4%、k-最短路 0.6%→38.6%** 的完整响应曲线（L348）。**这是全批最干净的"负载 → 性能崩溃"数据**。
- **日内到达率节律被建模并被验证为真实可观测**：式 1 的 $mathrm t_{n,t}$ 因子（人口 × 当地时刻），Fig 6a 显示**最短路算法的丢包率呈现明显的日周期波动，而 SKYLINK 几乎没有**（L362）。这直接支持"负载是时变的、且时变幅度足以改变方案排序"。
- **一条极重要的测量学警告（L364）**：**平均时延不能单独看**——最短路算法的平均时延更低，纯粹是因为它们**只送近距离的数据、把远距离的数据丢掉了**。任何"负载升高时看时延"的实验，如果不**同时报丢包率与吞吐**，结论会完全反过来。这条对整个选题的方法论都适用。
- **瓶颈定位**：作者明确说**GSL 容量才是全网瓶颈**，ISL 全断 cost 也只涨 <10%（L382）；且**平均跳数接近 1**（L389）。这对"负载变化下到底哪个环节先饱和"给出了一个具体答案：**在这个人口分布下，先饱和的是星地链路，不是星间链路**。
- **明示的缺口**：**缓冲被建模为"非满即空"的稳态**（L82），**排队时延被建模成台阶函数**（式 11）——**负载变化过程中的瞬态排队行为被整篇论文排除在外**。这正是"负载变化下的到达率/时延"可以合法切入的位置。

**10. 一句话评价**
**把"每颗星一个上下文老虎机"这一极简分布式方案做到全域规模并打赢集中式/最短路基线**——方法上属于"用经典的 MAB + tile coding 换掉全局优化"，胜在复杂度与星座规模解耦；对负载–时延问题，它给出了本批最有价值的**负载扫描曲线**与一条**"时延必须与丢包同看"**的测量学教训，但它自己把**缓冲瞬态与排队时延的连续过渡**显式排除在模型之外，留下了最直接的可攻缺口。


## K93SCUF2 — Network topology design at 27,000 km/hour

**1. 一句话**
提出 **motif（基元）**：一个"3 颗星、2 条 ISL"的局部连接模式，把它**复制到全网每颗星**就能完整定义整个星座的 ISL 拓扑——于是拓扑设计从"全网 NP-hard 优化"塌缩成"**在一颗赤道星的可达集合里穷举选 2 个**"；再用**按纬度分区的 multi-motif** 换一点可控的链路抖动，换来更大增益。

**2. 问题设定**
挑战既有默认假设：**ISL 必须连接近邻、必须网格化**（L31 逐字："a more widespread, usually implicit, assumption that inter-satellite links must be local, and grid-like"）。作者算了一笔账：550 km 高度下，只要 ISL 不进入中间层（**离地 80 km 以上**），**最大 ISL 长度可达 5014 km**（L114）；对 40² 星座，赤道上的一颗星**理论上能与 190 颗其他星建链**（L116）。所以"+Grid 的近邻约束是不必要的自我限制"。问题被精确定义为（L136）：给定轨迹、每星少量 ISL、目标地面流量矩阵，**如何连线使端到端时延与跳数最小**。

**3. 方法骨架**
非 RL，是**结构化的穷举搜索**：
- **Motif 定义（第 4.1 节）**：若卫星 A 从其可达集合中选两颗 B、C 相连，**把这个模式复制到全网**，则每颗星的局部视图完全相同（Fig 6，L221）。A 的另外两条 ISL 由其他星按同样方式连过来决定。**一个 motif = 3 星 2 链的模式**，重复即得全网拓扑。**+Grid 是这个家族的一个成员**。
- **穷举流程（L231–L239）**：① 取一颗**赤道上的星** $e$（那里卫星间距最大，可达集合最小，保证 motif 在其他纬度也都可行）；② $S_e$ = $e$ 可达的全部卫星；③ $M=[S_e]^2=\{\{a,b\}:a,b\in S_e,a\ne b\}$；④ 可选地剔除等价 motif（利用对称性）；⑤ 输出 $m=\arg\min_{x\in M}\Phi_\alpha(x)$。
- **目标函数（第 3.1 节）**：$M_\alpha=\alpha S+B$，$S$ 是 **stretch**（设计网络最短路距离 / 大地线距离），$B$ 是**跳数**；$\Phi_\alpha=\sum_{\text{端点对}}M_\alpha\cdot H$（按流量矩阵加权）。$\alpha=1$ 为默认（时延与容量等权）。
- **流量矩阵**：**人口乘积模型**——取 1000 个人口最多的城市（2025 估计），城市对流量正比于人口乘积，缩放到 [0,1]（L156）；另有 **GDP 乘积模型**（前 100 城市）作对照（L308）。
- **为什么传统方法不行（第 3 节，本文最有价值的论证）**：
  - **ILP**：20 城时最优（$\Phi_1$ 比 +Grid 低 54%），但 **25 城在 64 核/500 GB 上跑 2 天跑不完**，外推到 1000 城需 $10^{29}$ 天（L185）。更致命的是**时间动态**：相隔仅 1 分钟的两次 ILP 解**只有 9% 的链路重合**（L187）。
  - **随机正则图（RRG）**：median stretch 牺牲 11%，median 跳数降 53%，$M_1$ 降 43%，$\Phi$ 降 42%（L200）。但 **2 分钟内 >8%、5 分钟内 >19% 的 ISL 变得不可行**（L202）；且**无法针对流量矩阵优化**（L207）。
  - **蚁群**：小规模好，大规模不收敛，链路抖动大（L209）。
- **Multi-motif（第 5 节）**：卫星在高纬更密（Fig 12：53° 星座的 motif 选项从赤道 ~1100 涨到 53° ~3600，L321），所以**按纬度分区**用不同 motif。分区分辨率 $W$ 是"允许多少抖动"的旋钮（第 5.3 节的迭代搜索：从赤道侧开始，固定前一区的链路，穷举下一区）。**$W=18^\circ$ 时卫星约每 12 分钟换一次 ISL**（L346），而 ISL 建立开销是"几秒到几十秒"（L103）。
- **拥塞分析（第 5.6 节）**：用**边介数中心性**（5000 个随机城市对的最低时延路径计数）作为拥塞代理。

**4. 它声称的效果**
- **40² 星座（53°、550 km）有 1029 个唯一 motif**（L252）。**+Grid 的加权 stretch = 1.25、跳数 = 10.57**（L252）。
- 最优 motif 相对 +Grid：**median（95 分位）$M_1$ 改善 44.5%(54%)、$M_5$ 改善 26.2%(37%)、$M_{10}$ 改善 16.8%(22.3%)**（L262）。
- 单个 motif 的 $\Phi_1$ 比 +Grid 好 **45%**，但比 ILP（20 城）差 **18%**（L264）。
- **用 2% 的 stretch 换 32% 的跳数改善；用 10% 换 47%**（L260）。
- **Multi-motif（3 区、W=18°）**：$\Phi_1/\Phi_5/\Phi_{10}$ 分别比 +Grid 好 **48% / 30% / 20%**（L357）。3 区以上收益饱和（比单 motif 再好 7%，2 区时是 5.6%）；极轨下 3 区比单 motif 好 9.5%（L346）。
- **具体星座（Table 1，L378）**：**Starlink** 可见距离 ISL 下 median $M_1$ 改善 **52%**、$\Phi_1$ **54%**；**即使最悲观的功率受限距离下仍有 37% / 40%**。**Kuiper** 38% / 45%（可见距离），但最小距离下只有 **1% / 4%**。40² 为 45%/48%（可见）、9%/7%（最小）。
- **时间稳定性（Fig 8，L276）**：2 小时逐分钟快照，$\Phi_1$ 的时间波动**在 median 的 10% 以内**；多 motif 还能进一步降低时间方差（Fig 14）。
- **拥塞（Fig 15，L370）**：+Grid 的 75 分位与 90 分位链路使用频次分别是 $mm_1$ 的 **4 倍与 5 倍**。
- **RTT 对比（Fig 3，L124）**：40² 星座 vs 今日互联网，8 个大城市 28 对，median（95 分位）RTT 改善 **70%(65%)**。
- **基线**：+Grid（主基线）、ILP、随机正则图、蚁群。

**5. 它的实验条件**
- 主星座：**40² = 1600 颗**（53° 倾角、550 km），另测 $16^2/24^2/32^2/40^2$ 和极轨 90° 版本。
- **最大 ISL 长度 5014 km**（80 km 中间层净空），最低界为 +Grid 所需长度（40² 是 1467 km，Starlink 2006 km，Kuiper 1761 km）。
- 地面站：**1000 个人口最多的城市各一个站**，假设任意带宽、只要在可见范围内就能连（L158）。**地面站布放与星地连接联合优化被明确排除**（留给未来工作）。
- 流量：**静态、时不变**的流量矩阵（人口乘积或 GDP 乘积）；**"考虑时变流量留给未来工作"**（L310 逐字）。
- 时延只算**传播时延**：$D^{Tx}=d/c$ 类的最短路；**忽略排队与处理时延**（L130 逐字："our accounting for latency uses only propagation delay, ignoring queuing and processing at each hop"）。
- 吞吐用**跳数做代理**（L126），依据是"固定 ISL 数与容量下，减少端到端跳数就释放了带宽"。
- 代码与数据公开（[12]，L448）。无训练过程（非学习方法）。

**6. 它自述的局限**
- **只算传播时延**（L130 逐字）："our accounting for latency uses only propagation delay, ignoring queuing and processing at each hop. However, accounting for these would only improve our results, as we achieve much lower hop counts than +Grid."（后半句是**推测**，无数据支撑）
- **RTT 对比可能对卫星网络过于有利**（L124 逐字）："We acknowledge that this comparison is perhaps overly favorable to satellite networks: overheads from sub-optimal routing, congestion and queuing, and forward error correction are not accounted for here"
- **时变流量未做**（L310 逐字）："Considering time-varying traffic is left to future work, we note that one could evaluate the potential motifs against snapshots of traffic over a desired time period, picking the one that provides the highest performance over time."
- **输入参数本身不确定**（L390–L394）：ISL 距离与建链速度取决于卫星重量/发射成本等非网络因素；市场需求决定流量矩阵；Starlink 计划本身在变（用的是 2019 年 7 月前的数据）。
- **跳数只是吞吐的代理**（L126 逐字）："We use the number of on-path satellite hops as a simple proxy for network throughput"。
- **星地连接被简化**（L158）：只在可见范围内假设可连，"Considering GS placement and GS-satellite connections jointly in the optimization is left to future work"。
- 未来工作（L398）：时变流量矩阵、大星座不同阶段互联、更多 ISL、与星地连接/路由的联合设计。

**7. 它没做但看起来能做的地方**
1. **流量矩阵是静态的，且明确把时变留给未来工作**（L310）。这意味着**"负载变化"在这篇论文里根本不存在**——拓扑是对着一张固定的流量表选的。而作者自己已经指出"可以拿一段时间内的流量快照来评估 motif，选长期最优的那个"——**这个提示没有被任何人（包括他自己）执行**。
2. **时延只算传播时延**（L130）。它辩解说"排队时延只会让我们的结果更好"，但这个论证**只在拥塞确实更轻时成立**——如果 motif 把流量集中到了少数长链路上（stretch 换跳数正是这个方向），拥塞的**空间分布**会改变，跳数少不等于不排队。**这是一个被推测掩盖的空洞**。
3. **stretch 与跳数的权衡（$\alpha$）由算子手选**，论文给了 Pareto 前沿但没有给"该选哪个 α"的判据。
4. **multi-motif 的分区宽度 W 是唯一控制抖动的旋钮**，而"抖动代价"（每次重连几秒到几十秒）**从未被量化成时延或丢包**——只有"12 分钟换一次，所以几十秒可以接受"这样的定性论证（L346）。**ISL 建立期间的数据去哪了？没写。**
5. **地面站布放被排除在外**（L158）。但人口乘积流量模型 + "每城一个站"的假设，与 SKYLINK（K7U4TYJN）实测的"绝大多数流量在近地面站处直接落地、平均跳数≈1"形成尖锐张力——**motif 优化的链路，可能承载的是被这个假设人为放大出来的长距离流量**。
6. 只测了 **Starlink / Kuiper 的 phase-1**，与当时规划相比已经是"未来"，与今天的实际部署结构差异更大。

**8. 和同批其他篇的关系**
**它是本批的"拓扑设计"祖辈**：**JS857IYN（DoTD）明确引用它（作为 [17]）并称"motif 方法相对邻居网格把时延与容量改善了 2 倍"**——DoTD 是它的直接后继（用动态规划打分替代穷举 motif）。与 **JS857IYN** 的差异很关键：motif 追求**零链路抖动**（结构本身就不变），DoTD 追求**最大化历史链路留存**；motif 用穷举，DoTD 用 DP；两者都**没有流量负载模型**。与 **JLF7IEBQ（SaTE）** 对照：SaTE 说拓扑给定、优化流量分配；motif 说流量给定、优化拓扑。与 **K7U4TYJN（SKYLINK）** 形成本批最强对照：SKYLINK **分布式、在线学习、有流量负载与排队时延**，motif **集中式设计、静态流量、无排队时延**。它引用了 **[71] Taleb et al. 的 ELB——即本批 JP79GMZS**（L566），这是本批内一条明确的引用链。也引用 Handley "Delay is Not an Option" [28]、Klenze "Networking in Heaven as on Earth" [39]、del Portillo [21]、Wood [81]、Gavish & Kalvenes [26]、Singla Jellyfish [62]。

**9. 对"负载变化下到达率/时延"的贡献**
**没有直接贡献**，而且是有意识的排除：流量矩阵**静态且时不变**（L310 明确留作未来工作），时延**只算传播时延、忽略排队**（L130），没有任何到达率扫描或负载维度。
**但有两条外围事实可记**：
- **"跳数 ≈ 容量占用"这一代理关系被显式论证并在第 5.6 节用边介数拥塞验证**（L370：+Grid 的 75/90 分位链路使用频次是 $mm_1$ 的 4/5 倍）。这给"如何在不做逐流仿真时估计网络拥塞"提供了一个廉价代理，且给出了"代理与真实拥塞方向一致"的证据。
- **"+Grid 的拥塞分布更不均"** 这一结论可以借用：**同样的总流量下，拓扑选择会改变拥塞的空间集中度**。对"负载升高时哪条链路先饱和"这个问题，它给出了一个结构性答案（近邻网格把流量压在少数短链上）。
- 另有一条**可用的量级**：ISL 建立开销"**几秒到几十秒**"（L103），且 550 km 高度星速 **27,306 km/h**（标题所指）。

**10. 一句话评价**
**用"重复模式"这一极简结构性洞察，把 LEO 拓扑设计从 NP-hard 优化里救出来**——论证（为什么 ILP/随机图/蚁群都不行）比解法本身更有价值，且"用 2% 的 stretch 换 32% 的跳数"是一个非常干净的权衡事实；但它把**流量负载、排队时延、星地连接**三样东西全部排除在模型外，因此它回答的是"拓扑在物理上能有多好"，而不是"负载变化下会有多堵"。


## KPUZIMU5 — The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games

**1. 一句话**
**MAPPO**：把单智能体的 PPO 原样搬到协作多智能体场景（策略只看局部观测、**价值函数看全局状态**，即 CTDE），不做任何领域特化的算法或架构改动，就在 MPE / SMAC / GRF / Hanabi 四个基准上打平甚至超过 off-policy 的 SOTA——并总结出**五个决定成败的实现细节**。

**2. 问题设定**
MARL 文献近年几乎被 off-policy 方法（MADDPG、值分解类 QMix/QPlex/RODE）占据，PPO 这种 on-policy 方法"significantly less utilized"（L9）。作者认为原因有两个（L15）：① **人们相信 PPO 在样本效率上不如 off-policy**；② **单智能体 PPO 的常见实现与调参习惯直接搬到多智能体场景会失效**。注意：本文**不是要提出新算法**（L19 逐字："Our aim in this work is not to propose a novel MARL algorithm"），而是要**纠正一个经验判断**并给出实操建议。

**3. 方法骨架**
- **问题设定（第 3.1 节）**：**DEC-POMDP** $\langle\mathcal S,\mathcal A,O,R,P,n,\gamma\rangle$，**共享奖励**（L43）。每个 agent 用自己的策略 $\pi_\theta(a_i|o_i)$ 从局部观测出动作，联合优化 $J(\theta)=\mathbb E[\sum_t\gamma^t R(s^t,A^t)]$。
- **MAPPO vs IPPO（第 3.2 节）**：两者结构都跟单智能体 PPO 一样（策略 + 价值两个网络）。区别只在价值函数的输入——**MAPPO 的价值网络吃全局状态**（因此是 CTDE 结构），**IPPO 只吃局部观测**（完全独立学习）。$V_\phi(s)$ 只用于训练期降方差，执行时不需要。
- **实现细节（第 3.3 节）**：**参数共享**（同质 agent 共享策略与价值网络，被认为能提升学习效率）；采用 **GAE [29]**（即本批 JSX5XG88）+ 优势归一化 + **value clipping**。
- **五个关键因素（第 5 节，本文真正的贡献）**：
  1. **价值归一化**（第 5.1 节）：用**滑动均值/标准差**标准化价值目标，算 GAE 时再反归一化。建议 1：**务必用价值归一化**。
  2. **价值函数输入表示**（第 5.2 节）：对比 CL（拼接所有局部观测）/ EP（环境提供的全局状态）/ **AS**（EP + 本 agent 局部观测）/ **FP**（AS 去掉重叠特征）。结论：**CL 维度太高、效果差**（尤其 agent 多时）；EP 缺 agent 特有信息；**AS 与 FP 都好，FP 略优**。建议 2：**同时包含局部与全局特征，并检查不要无谓增加输入维度**。
  3. **训练数据使用**（第 5.3 节）：**与单智能体的惯例相反**——单智能体常用 32/64 个 mini-batch、训几十个 epoch，而**多智能体下复用样本过多会掉性能**。建议 3：**难任务 ≤10 epoch、易任务 15 epoch，且尽量不要切 mini-batch**（1 个 mini-batch 在 22/23 个 SMAC 地图上最好）。
  4. **PPO 裁剪**（第 5.4 节）：建议 4：**裁剪系数 ε 保持在 0.2 以下**，在此区间内权衡稳定性与收敛速度。作者的解释（L192）：小 ε 限制每次更新中策略的变化幅度，从而**缓解 MARL 的非平稳性**。
  5. **Batch size**（第 5.5 节）：存在一个**临界批量**，低于它最终性能差；但不是越大越好，过大反而损害样本效率。建议 5：**先用大批量拿最好性能，再调小以优化样本效率**。
- **一个未列入五因素但单独详述的技巧**：**death masking（第 C.3 节）**——SMAC 里 agent 死亡后，其局部观测变为全零，但全局状态仍有非零信息，造成**价值输入分布漂移**。作者把死亡 agent 的价值输入替换为"零向量 + agent ID"（$\mathbf 0_a$），四种方案里这个最好，且**必须保留 agent ID**（否则不同角色的 agent 无法区分）。

**4. 它声称的效果**
- **MPE（Fig 1，L90）**：MAPPO 与 QMix 在所有任务上近乎持平，在 Comm 任务上超过 MADDPG，**样本量相当**；IPPO 虽不用全局信息，也能打平或超过集中式 off-policy 方法，但在 Comm/Reference 上最终回报略低。
- **SMAC（Table 1，L96）**：**MAPPO(FP) 与 IPPO 在绝大多数地图上至少与 QMix 持平**，用同样步数；**MAPPO 在 14 个地图中的 10 个上与 RODE 相当或更好**；给更多样本后几乎每个地图都能追平或超过 RODE。多个地图上 MAPPO 达 **100.0% 胜率**（如 2m_vs_1z、3m、25m、corridor），而 QMix 在 25m 只有 85.9%、6h_vs_8z 只有 9.4%（MAPPO 88.3%）。
- **GRF（Table 2，L110）**：MAPPO 在**每个场景都明显超过 QMix**（如 3v.1：88.03 vs 8.12）；**在没有用内在奖励的情况下超过使用内在奖励的 CDS**；且在 5 个场景中的 4 个上**超过用了人类专家数据预训练的 TiKick**。
- **Hanabi（Table 3，L124）**：MAPPO 在几乎所有设置下与 SAD / VDN 的最好与平均回报相当或更优。**关键发现**：IPPO 在 2 agent 时与 MAPPO 相当，但**随着 agent 数增加，MAPPO 明显拉开差距**——说明**集中式 critic 输入是关键的**（L126）。
- **参数共享消融（Table 4，L331）**：MAPPO 全面优于 MAPPO-Ind（不共享），差距在难图上极大：MMM2 90.6 vs 13.0、6h_vs_8z 88.3 vs 11.4、3s5z 84.4 vs 37.8。
- **基线**：MPE 用 QMix/MADDPG；SMAC 用 QMix、QPlex、CWQMix、AIQMix、RODE；GRF 用 QMix、CDS、TiKick；Hanabi 用 SAD、VDN。所有基线都**重新实现并做了等规模网格搜索**（L73）。

**5. 它的实验条件**
- **完全不是网络场景**：四个基准是 **MPE（2D 粒子世界）**、**SMAC（星际争霸微操）**、**GRF（谷歌足球）**、**Hanabi（花火卡牌）**（L59）。
- 硬件（L82）：**256 GB RAM、单颗 64 核 CPU、一块 RTX 3090**。
- 规模：SMAC agent 数 **2 到 27**（L305）；Hanabi 2–5 人；GRF 每场景 2500 万步（CA-hard 和 Corner 为 5000 万步）；Hanabi 最多 **100 亿环境步**（L124）。
- 超参（Table 7，L558）：**GAE λ=0.95、γ=0.99**、Huber loss（δ=10.0）、梯度裁剪范数 10.0、Adam、优化器 ε=1e-5；SMAC 用 num envs=128、buffer length=25、1 层 GRU、hidden 64、fc dim 64。
- **训练与评估同分布**：所有基准都是标准评测集，**没有做跨分布/跨任务泛化测试**。
- 种子数：MPE 10 个（L88）、SMAC 6 个（L96）、GRF 6 个（L106）、Hanabi 至少 3 个（L122）。

**6. 它自述的局限**
- **只有离散动作、只有协作、几乎全是同质 agent**（L218 逐字）："our benchmark environments all use discrete action spaces, are all cooperative, and in the vast majority of cases, contain homogeneous agents."
- **未来工作才做竞争性、连续动作、异质 agent**（L218 逐字）："In future work, we aim to test PPO on a wider range of domains such as competitive games and MARL problems with continuous action spaces and heterogeneous agents."
- **纯经验、无理论**（L218 逐字）："our work is primarily empirical in nature, and does not directly analyze the theoretical underpinnings of PPO."
- 对 death masking 的理论刻画也只是"值得做"（L358 逐字）："While the arguments here are intuitive the clear experimental benefits suggest that theoretically characterizing the effect of this method would be valuable."

**7. 它没做但看起来能做的地方**
1. **它明确说"多智能体下样本复用要少"，理由是缓解非平稳性（L170），但没有验证这个假设**——把 epoch 数降下来到底是缓解非平稳、还是仅仅相当于缩小了每次更新的有效步长？没有做诊断（比如测策略 KL 随 epoch 的变化）。
2. **临界批量（critical batch size）现象被观测到但没有被解释**（L212）。"低于临界值性能差、高于临界值只损样本效率"这个形状本身值得一个理论或至少一个 scaling 分析。
3. **最优超参是按任务类别手工网格搜出来的**（Table 13：MPE 与 SMAC 用同一套搜索空间）。**"易任务 15 epoch、难任务 5–10 epoch"这条建议需要预先知道任务难度**——没有给出自动判断难度的办法。这与 JSX5XG88 把 γ/λ 的自适应列为未来工作是**同一类缺口**。
4. **所有实验都是同质 agent**，而参数共享恰恰依赖同质性。**异质多智能体（例如每颗卫星角色不同）时这套建议是否还成立完全未知**。
5. **没有报告训练时间/算力对比**（只有硬件配置），只说"样本量相当"。在 RL 用于实际系统的语境下，墙钟时间与能耗同样是约束。
6. **death masking 的"保留 agent ID"这一条**，本质上说明**价值函数需要角色信息**——这与它对价值输入表示的讨论（AS/FP）是同一个主题，却没有合并成一个统一的"价值函数该看什么"的结论。

**8. 和同批其他篇的关系**
**这是一篇 MARL 方法论论文，不是 LEO 论文**。它与本批的 **JSX5XG88（GAE）** 有**直接的引用关系**：MAPPO 用 GAE 算优势（L53、Alg.1 L245 逐字 "Compute advantage estimate $\hat A$ via GAE on $\tau$, using PopArt"），参考文献 [29] 就是 Schulman et al. 的 GAE（L486）。两者是同一方法论谱系的两代：GAE 解决"优势怎么估"，MAPPO 解决"多智能体下 PPO 怎么配"。
与 LEO 类论文的关系：本批中 **J68GU76W 用 DDQN（值方法）**、**S85KQ4FC（锚件）与 K7U4TYJN（SKYLINK）用 MAB**——**没有一篇用 PPO/MAPPO**。也就是说，这篇代表的方法线在 LEO 路由语料里**尚未被使用**。它引用的谱系全是 RL：Qmix[27]、MADDPG[22]、VDN[32]、COMA[11]、SAD[15]、RODE[37]、QPlex[36]。**未见引用任何卫星/网络文献**。

**9. 对"负载变化下到达率/时延"的贡献**
**没有直接贡献**——零。四个基准都是游戏/控制环境，没有网络、没有到达率、没有排队、没有时延。
**但有两条间接的、对"用 MARL 做 LEO 路由"这件事有用的事实**：
- **"多智能体下样本复用要少"**（建议 3）：这条建议如果迁移到 LEO 路由（每颗星一个 agent、网络状态随负载与拓扑持续非平稳变化），意味着**必须用较少的 epoch、不做 mini-batch 切分**。这是对"在线适应负载变化"这条路线的一个**具体的工程约束**。
- **"agent 数增加时，集中式 critic 的价值会凸显"**（L126，Hanabi 从 2 人到 5 人 MAPPO 相对 IPPO 优势扩大）。这直接对应 LEO 场景里"星座规模从几十颗涨到几千颗"的情形——**如果要用 MARL 做路由，全局 critic 的收益会随星座规模增大而增大，但全局状态的维度也会随之爆炸**。这个张力本文没有触及（它最大 27 个 agent）。

**10. 一句话评价**
**一次高质量的"经验纠偏"**：它证明了在协作多智能体里 PPO 不必被 off-policy 方法取代，并把"怎么配 PPO"从口口相传变成五条可操作的建议（尤其"少 epoch、不切 mini-batch"与单智能体惯例相反）；在方法谱系里它属于**基础工具链的配置手册**，与 LEO 路由无直接关系，但对任何打算用 MARL 做星上决策的工作构成必要的前置知识。


## L2VKYTAV — Shaping Rewards, Shaping Routes: On Multi-Agent Deep Q-Networks for Routing in Satellite Constellation Networks

**1. 一句话**
对**全分布式多智能体 DQN（FD-MADRL）**做一次诚实的压力测试：重点不是提新算法，而是**逐条设计奖励函数并量化训练收敛**，结论是"**当前奖励设计能学出短路径，但会把链路用饱和，而且节点数一涨就不稳**"，于是提出一个 **CL-DC（集中式学习 + 分散式控制）** 的混合架构作为出路。

**2. 问题设定**
LEO 星座路由要在"高度动态、物理上巨大、流量非均匀分布且有 QoS 要求"的网络里找最优配置（L11）。FD-MADRL 的吸引力在于每颗星就地快速决策；**但代价是**：端到端连贯性与稳定性存疑，agent 之间必须互相学习对方的行为，可能出现复杂而意外的相互作用（L27）。SCN 的独特困难还包括：**频繁的 ISL 与星地链路切换**，以及**热点是地理性的而非拓扑性的**（L17 逐字："hot spots are geographical rather than topological"）。

**3. 方法骨架**
- **RL 设定（第 1.2 节）**：MDP，式 1 给出 Q 值的 Bellman 形式；DQN 用 DNN 逼近 Q，经验回放提稳定性。**FD-MADRL 的状态空间 = 相邻链路负载 + 上一跳 + 目的节点**；**动作空间 = 可用的 ISL，即下一跳的选择**（L29）。每颗星 4 条 ISL（L17）。
- **奖励分层（第 1.3 节，本文核心）**：
  - **全局奖励（面向 CDRL）**：$r^G_{t+T}=w_1U(t)-w_2L(t)-w_3D(t)$（式 2）——由链路利用率 U、流时延 L、丢包率 D 加权组成；**但只在多跳传播延迟 T 之后才收到**（L33 逐字："this reward is only received after a significant time lag, denoted by T, due to the multi-hop propagation delays"）。
  - **局部奖励**：$r^L_{t+1}=w_4delta^L_{th}(t)-w_5l^L(t)-w_4d^L(t)$（式 3）——**注意这里 $w_4$ 被用了两次**（链路阈值项与丢包项），而正文说三项权重大小为 $w_4,w_5,w_6$（L42），**公式与文字不一致，疑为笔误**。
  - **FD-MADRL 实际用的局部奖励（式 4，L53）**：不用局部时延，改用**到目的地的路径缩短量 ψ**（沿用 [4]）；**+Ψ 到达终点**；**−Ψ 若路径未缩短且成环**（量级至少比 ψ 大一个数量级，且**只惩罚真正造成环的那个节点**）；**+ξ₁ 若链路负载 < 0.4；−ξ₂ 若 0.4 < 负载 ≤ 0.8；−ξ₃ 若负载 > 0.8；−Ξ 若链路饱和**。−Ξ 与 −Ψ 同量级。
  - 作者自述两个经验发现（L48/L50）：**加入与 −Ψ 同量级的 +Ψ（到达终点）能改善训练**，即使它没有沿路径传播到所有节点；**阈值式的负载均衡奖励被证明有效**。
- **评估指标（第 2.1 节）**：**逐跳时延（即跳数）** 与**所选路径上的最大链路负载**（L60）。
- **对比基线**：**动态最短路优先（SPF）**，一个基于 Dijkstra 的多代价规则算法，代表典型 SOTA，**主动避开负载 >80% 的链路**（L74）。

**4. 它声称的效果**
- **静态寻路（第 2.2.1 节）**：24 节点集群需要**两倍以上的 episode** 才能稳定达到最大奖励（L66）。
- **典型的短视失败案例（L66，很具体）**：24 节点集群里，从节点 4 到节点 23，学习到的策略**先走到节点 8**（因为相邻链路负载低），但这条路由可能经过**节点 22，再从 22 走一条接近饱和的链路到 23**——**局部最优的下一跳选择导致端到端上的昂贵决策**。
- **vs 动态 SPF（Fig 3，L74）**：**FD-MADRL 在多数路由上跳数更少**（路径更短），**但它倾向于把链路用饱和**。作者强调静态场景下这问题不明显，**但在动态场景中缺乏前瞻性会导致整体系统性能下降**。
- **动态链路负载（第 2.2.2 节）**：把上一 episode 中用过的每条链路**额外加 20% 负载**（只在本 episode 内生效，避免所有链路都饱和）。结果：**奖励更低、更不稳定**；**12 节点集群还能保持高性能，24 节点集群结果不稳定**（L83）。原因：更大的网络里更容易出现"选中饱和链路"或"意外引入环路"从而产生大幅负奖励的情形；且**全分散的 agent 很难学会主动规避潜在瓶颈**。

**5. 它的实验条件**
- 自建 **gym** 环境，DQN 用 **Keras/TensorFlow** 实现（L60）。
- 拓扑：**"SCN 的子网"，即分布式架构中的一个 cluster**——具体用 **12 节点**与 **24 节点**两个集群（Fig 1 展示 24 节点那个），不是完整星座。
- **负载是随机设定的**，但声称"符合[6]中观测到的合理非均匀分布流量场景的链路特性"（L60 逐字："While the loads are set randomly, they comply with observed link characteristics of plausible non-uniformly distributed traffic scenarios [6]"）。
- **动态场景的"动态"仅指**：上一 episode 用过的链路加 20% 负载（L78）。
- **无流量到达率模型、无排队模型**；时延用**跳数**代替。
- 评估：训练过程中的 smoothed reward 曲线 + 最终路径的跳数/最大负载散点。
- 作者明确限定范围（L60 逐字）："Due to the limited scope of this manuscript, only the described reward design is investigated."

**6. 它自述的局限**
- **只考察了这一种奖励设计**（L60 逐字）："Due to the limited scope of this manuscript, only the described reward design is investigated."
- **FD-MADRL 的短视在静态与动态场景下都损害端到端路由**（L87 逐字）："For FD-MADRL, we have shown that the limited scope of each agent negatively impacts the end-to-end routes, in both static and dynamic scenarios."
- **策略越复杂，agent 之间要互相学习就越有反效果**（L87 逐字）："Moreover, with increasingly complex policies, the agents have to learn the behavior of other agents, which is counterproductive for scalability."
- **CDRL 的代价**（L87 逐字）："A CDRL-based scheme on the other hand, loses the flexibility of decentralization, introduces a single point of failure, and needs additional signalling."
- **结论保守**（L94 逐字）："while DQN-based architectures represent promising solutions for routing and network control in complex SCNs, they still have practical limitations... In-depth investigations are required to fully evaluate their actual viability."
- 未来的 CL-DC 架构**只是提案**（Fig 5），**没有实现、没有实验**。

**7. 它没做但看起来能做的地方**
1. **CL-DC 混合架构只有一张示意图（Fig 5），没有任何实验**（L92）。它给出的理由很具体：**Q 函数在训练与执行时需要同样的信息，所以未来要考虑 policy gradient 的多智能体 actor-critic 架构**——这是一个明确、可执行、且尚未被执行的下一步。
2. **"动态"负载的建模极其粗暴**：上一 episode 用过的链路 +20%。这既不是到达率变化，也不是排队动力学，**而是一个人为的、无时间结构的扰动**。真正的负载演化（到达率随时间变化 → 队列 → 拥塞）完全没建模。
3. **时延用跳数代替**（L60）。而它的奖励里明明有"局部时延 $l^L(t)$"这一项（式 3），FD-MADRL 却**放弃了它**、改用路径缩短量（L48）。**为什么放弃时延信息、以及放弃的代价，没有被讨论**。
4. **式 3 的权重 $w_4$ 重复使用**（应为 $w_6$），公式与正文不符——这处错误让"局部奖励的权重如何选"这件事无法独立复核。
5. **只测 12 与 24 节点两个规模**，且都是"集群"而非完整星座。24 节点就不稳，那条"要到多少节点才会彻底失效"的曲线完全没有——**这恰恰是它宣称的 scalability 问题所最需要的证据**。
6. **没有报告训练所需的时间/episode 数的绝对值**（只说"两倍以上"），也没有说明是否需要重训、多久重训一次。
7. **负载阈值 0.4 / 0.8 是硬编码的**（式 4），与 JP79GMZS 的 ELB 用闭式公式反解阈值形成对比——**这篇没有做阈值敏感性分析**。

**8. 和同批其他篇的关系**
**与 J68GU76W 是同一族但更诚实的一篇**：两者都用**多智能体 DQN 做 LEO 转发**，J68 用残差学习叠在 backpressure 上、目标是队列长度，本篇用纯局部奖励、目标是时延+负载均衡，且**明确报告了方法在 24 节点就不稳**。与 **JP79GMZS（ELB）** 直接对照：ELB 用**闭式公式**动态设定阈值 α/β/χ，本篇用**硬编码阈值 0.4/0.8** + 学习——ELB 无学习但参数有依据，本篇有学习但阈值靠猜。与 **K7U4TYJN（SKYLINK）** 对照：SKYLINK 也是全分布式的（MAB），但它**明确报告卫星负载作为上下文无效**，而本篇恰恰把"相邻链路负载"放进状态空间——**两篇在"负载信息对分布式 agent 有没有用"上给出了相反的实践**，值得并列记录。与 **KPUZIMU5（MAPPO）** 的关系：本篇在讨论里自己指出"未来要用 policy gradient 的多智能体 actor-critic"（L92），而 MAPPO 正是这类方法的标准实现。它引用了 **[4] Soret et al. Q-learning for distributed routing in LEO**（也就是 K7U4TYJN 的基线之一 [24]），以及 [3] You et al. 全分布多智能体 DRL 路由、[5] Hierarchical Deep Double Q-Routing、[6] Roth et al. 分布式 SDN 负载均衡路由。

**9. 对"负载变化下到达率/时延"的贡献**
**有直接贡献，而且是负面的、很有价值的贡献**：
- **"时延最优 ≠ 负载均衡"这个矛盾被实测出来**（L74）：FD-MADRL 学出来的路径**跳数更少**（时延代理更优），**但把链路用饱和**。也就是说，**当 agent 只看"能多快到达"时，它会给网络制造拥塞**——这条 trade-off 对"负载变化下的时延"是核心事实：**低时延的达成方式本身会推高未来的负载与时延**。
- **负载变化直接摧毁分布式学习的稳定性**（第 2.2.2 节）：把用过的链路加 20% 负载后，**12 节点还能撑住，24 节点就不稳了**。这是一个**关于"负载动态性 → 学习稳定性"的规模阈值现象**，虽然实验粗糙，但结论方向清晰。
- **明确点出"前瞻性"的缺失**（L74 逐字："a lack of foresight can result in decreased overall system performance"）：局部观测的 agent **无法主动规避潜在瓶颈**（L83）。这正是"负载变化"场景下最需要的那个能力。
- **一条关于奖励时序的事实**（L33）：全局奖励**要等多跳传播延迟 T 之后才到达**——即**时延/丢包这类端到端指标天生是滞后信号**，而局部奖励是即时的。**"即时信号 vs 滞后信号"的取舍**，是任何做负载自适应路由的工作都必须面对的结构性问题，这篇把它明确写了出来。
- 局限同样明确：**没有到达率模型、没有排队模型、时延用跳数**，所以它给不出"到达率 → 时延"的曲线。

**10. 一句话评价**
**一次有价值的负面结果报告**：它没有把 FD-MADRL 包装成成功案例，而是**用奖励消融和两档规模说明了全分布式 DQN 路由的短视与不稳定**，并诚实承认 CL-DC 方案还只是提案；在方法谱系里它属于"**对已有 FD-MADRL 路线做压力测试与诊断**"，对本选题的贡献是那条"**跳数更优 → 链路更饱和**"的实测矛盾与"**负载一变、24 节点就学不动**"的规模现象。

