# 读卡批次 R1

> 读法：逐字通读 VM MinerU MD 全文（行号即 VM MD 行号）。批次 11 篇：2FBBURX7 2QRYMWBI 2W8BJ7ME 35T2JJRJ 36RZKNW5 39NJWBI7 3MRQRWHU 42E4NAQU 47J2H748 4QG5VYHQ 524XNF29。

## 2FBBURX7 — Graph Attention Reinforcement Learning for Multicast Routing and Age-Optimal Scheduling

**1. 一句话**
把"多播给哪些目的点发更新（调度）+ 用什么树发（路由）"联立成一个 AoI 最小化问题，用拉格朗日乘子 λ 把原问题拆成"调度子问题 P1"和"Steiner 树生成子问题 P2"，两个子问题各建一个 MDP，再用分层 A2C（TGMS）端到端训；方法上的真新意是一个带**压缩映射性质**的归一化图注意力（NGAT），用来证明 RL 收敛。**跟 LEO 没关系**——全文没有卫星、没有 ISL、没有轨道动力学。

**2. 问题设定**
实时多播（视频流、VR、元宇宙、智能交通，L79/L84）中，源节点每个时隙可产生更新包，要送给一组目的节点；目的节点的信息新鲜度用 AoI 度量（L135-153）。麻烦在于三件事叠加（L39-43）：跨层（调度与路由互相影响，分开做次优）、计算复杂度（多播路由=Steiner 树，NP-hard，L21/L41）、图信息高维（非欧结构难提取）。额外有一条**长期能量预算**约束 $\lim_T \frac1T\sum C(T_t) \le \bar C$（式 8，L175-179），导致"树越大 AoI 越低但能耗越高"的取舍（L181）。注意：问题里**没有到达率、没有队列、没有拥塞**——见第 9 项。

**3. 方法骨架**
- 分解：OP（式 9）→ 对偶 DP（式 10）→ P1（调度，式 11）+ P2（树生成，式 12），两者由 λ 耦合（L207）。Lemma 2 把 P2 等价改写成可算的形式 P2-B（式 17，L277）：$\max_T \sum_u \omega_u(1-h_T(u)/\hat h_{G_t})A_u(t) - \lambda(C(T)-\bar C)$。
- **MDP $\mathcal M_1$（调度者，L241-269）**：状态 $s_t=\{G_t, x_t\}\in\mathbb R^{\hat V^2+6\hat V}$（式 14），$x_t$ 是逐节点 6 维特征（节点类型 one-hot 3 维 + 权重 $\omega_u$ + 该节点 AoI $A_u(t)$ + 正在传输的包数，Table I，L260）；动作=目的点集合的幂集 $\mathcal A_1=\mathrm{Pow}(\mathcal U_t)$，共 $2^{|\mathcal U_t|}$（式 15，L251-262，作者自己说这导致维数灾难）；奖励 $r_1=g(\lambda,\mathcal U'_t)$（式 16）。实现上用连续化：对每个节点输出 Bernoulli 后采样（L467），从而绕开幂集。
- **MDP $\mathcal M_2(a_t)$（树生成者，L303-336）**：状态=当前部分解 $\mathcal P_\tau$；动作=$\mathcal P_\tau$ 的邻居中尚未加入的节点（式 20）；转移确定（式 21）；奖励是质量函数差 $r_2=q_2(s_{\tau+1})-q_2(s_\tau)$（式 23），而 $q_2$ 就是 P2-B 的目标（式 22）。这就是 Khalil 等 [23] 的贪心元算法套进 RL。接边时取连接两端的**最小代价边**（式 24）。Proposition 1 保证终止时 $\mathcal P$ 是合法多播树（L347-351）。
- **表示**：NGAT（式 27a-c，L391-399）在 GATv2（式 26）基础上除以 $\|W_1\|$ 并加自环/特征项，Theorem 1 证明注意系数对称时 $f_{\text{NGAT}}$ 是压缩映射（L410），Lemma 4/Remark 4 说明有唯一不动点、可当降维与"带噪的网络状态表示"（L414）。
- **学习**：调度者与树生成者各一个 A2C（式 29-33，Algorithm 1 L438-447，Theorem 2 给出收敛率 $\mathcal O(\mathcal E(k)/n)+\mathcal O(1/n^\sigma)$）；λ 每个时隙更新（Algorithm 3 第 20 行，L564），λ 初值 0.05、训练间隔 100、学习率 1e-5（Table VI，L735）；两个训练技巧：用策略熵自适应调 ε（式 37-39，L568-586）、选择性反向传播（贪心探索产生的动作与概率超阈值的动作不反向传播，L588-597）。
- **推理**：Algorithm 2（L504-525）每时隙先采目的集合再生成树。

**4. 它声称的效果**
- **STP 部分**（Fig 6/7，Table III L650）：TG-NGAT 的近似比 ρ 在 I080/I160/I320/I640 上为 1.149/1.231/1.257/1.345，对比 SOTA IRR 的 1.168/1.223/1.226/1.187——**I160/I320 上与 SOTA 相当，I640 上劣于 SOTA（Comp.(SOTA) 一栏对 I640 写的是 13.3% 而其余多为上升箭头，可读作劣化）**；单图推理时间 0.285/1.227/7.082/22.245 s，相对 IRR 加速 2.99×/3.55×/5.20×/**9.85×**（摘要 L9 与 L637 都只报 9.85× 、6.35× 这两个最好看的数）；摘要说"approximation ratios of 1.1–1.3"。
- **泛化**：只用 I160 训练（因显存限制），直接测 I320/I640（L628）。
- **调度部分**（Fig 9/10，L687）：在 $\bar C\in\{1..20\}$ 上，平均加权 AoI 降 21.6%（全体约束）/25.6%（低能量 $\bar C<5$）；加权峰值年龄降 21.0%/29.2%。基线只有 Random 和 Greedy 两个（L671-673），且基线无法保证能量约束、超了就强制选空集（L675）。摘要与结论给的数字又不一样（结论 L709 写 21.1% 与 29.7%）——**同一篇内部数字不自洽**。

**5. 它的实验条件**
- 拓扑：STP 用 SteinLib [70] 的 I080/I160/I320/I640（80/160/320/640 节点，边数区间与终端数区间见 Table II L593），每集 100 个实例，随机取 80 训 20 测（L605）。
- 调度实验统一 $|V|=80$（L667），四个拓扑：I080、真实 AS-733（L645）、ER 随机图、BA 无标度图；没给终端节点的图随机取 10% 节点当目的点，源从剩余节点随机选，边代价从 {1,…,10} 随机赋（L667）；**只用 I080 训练**，其余只测（L667/L669）。每张图测 50 个时隙（L669）——**评估时长极短**。
- 能量约束扫 $\bar C\in\{1,\dots,20\}$（L687）。训练 RTX 4090，测试 AMD EPYC 7763（L741）。
- 训练与评估是否同一套：调度器在 I080 上训练、在 AS-733/ER/BA 上测试（跨分布测试），但**没有负载维度可跨**（见下）。

**6. 它自己承认的局限**（逐字）
- L705："First, it requires high memory for training on a large graph. This can be mitigated by using a distributed training framework. Second, the multicast tree may not be able to update in realtime due to the complexity of the graph. The real update frequency depends on the SDN devices used."
- L723："A limitation of our algorithm is that the scheduler needs to be retrained if the energy constraint changes. This motivates potential future research directions, such as designing a metalearning framework to optimize the scheduler."
（以上是第 VI.C 节"Limitations"与结论段，全文只有这两处自述局限。）

**7. 它没做但看起来能做的地方**（基于内容）
1. **换一个资源约束就要重训**（L723）——作者自己点出但没有做，且 λ 本可以当在线对偶变量调；这是最直接的口子。
2. **AoI 与 hop 数绑定**（Assumption 1，L110-112："the delay between the source and the destination is linearly proportional to the hops"）：这意味着"时延"被退化成正整数跳数，树生成者只需最短跳数即可，**任何拥塞/排队/带宽效应都被排除在模型外**。把 $h_T(u)$ 换成"路径时延和"是他们自己说"conceptually straightforward"的扩展（L112），但没做。
3. **能量预算是唯一被扫的运行点**（L687），负载不是变量：源"每时隙至少给每个目的点生成一个更新包"（L88），是 generate-at-will 模型（L106），没有到达过程。
4. 调度基线只有 Random/Greedy（L671），且它们没有 λ 机制、靠"超预算就选空集"硬压（L675）——**没有与任何 DRL/对偶方法对比**，21.6%/25.6% 的增益缺少强对照。
5. 树生成器只在 |V|=80 与 SteinLib 静态图上验证；动态拓扑 $G_t$ 在第 III 节就定义了（式 1，L96-102），**但实验里所有图都是静态的**，$G_t$ 的随机演化从未被实例化。

**8. 和同批其他篇的关系**
不像 LEO 路由文献：参考文献 [1]-[74] 逐条看过（L1055-1204），**没有任何 LEO/卫星/ISL 路由或 RL 路由的引用**（[46]-[50] 是能量收割/AoI 多播，[64] MAXQ，[66] GATv2，[23] Khalil 贪心元算法）。它与同批的可能接触面是"图神经网络 + RL 做路由"这一共同技术栈，以及 AoI/排队论这一指标族；不引用同批任何 LEO 篇目（这一点可反证它不在 LEO 直连的引用圈内）。

**9. 对"负载变化下到达率/时延"这件事的贡献**
**没有直接贡献。** 它的网络模型里根本不存在到达率：源是 generate-at-will（L106）、每时隙每目的点至少一个包（L88）、链路无损（L114 "error-free transmission"）、时延=跳数（Assumption 1）。唯一带"运行点扫描"性质的实验是能量预算 $\bar C\in\{1..20\}$（L687）；由此能带走的**一个可迁移事实**是：**策略在资源约束这个运行点上不迁移，换个约束必须重训**（L723 作者自述）——这跟"负载一变、策略失效"是同一类现象，但这里变的是能量预算而不是负载，且没有任何时延/到达率曲线可引。

**10. 一句话评价**
**把已有的"贪心元算法 + 图嵌入 + 分层 RL"（Khalil [23] + GATv2）搬到多播 AoI 问题上，理论包装（NGAT 压缩映射、A2C 收敛率）是新的，问题模型是退化的（时延=跳数、无到达过程、无动态拓扑实验）**；对 LEO 直连选题只提供"资源约束换点需重训"这一条类比事实，不提供任何可用的负载-时延证据。


## 524XNF29 — Non-Terrestrial Networks in 5G & Beyond: A Survey

> 覆盖：正文逐字读完第 1–439 行（第 440–757 行为参考文献，758–771 行为作者简介，均已确认边界）。全文 771 行。

**1. 一句话**
一篇**面向 3GPP 标准的 NTN 综述**：把 NTN 的平台分类（GEO/MEO/LEO/UAS + 透明/再生载荷）、接入架构（直连 / 中继 / 多连接）、从 1G 到 4G 的星地融合史、5G 视角（SDN/NFV、切片、边缘计算、NOMA、IoST、CubeSat）、3GPP Rel-15/16/17 的 NTN 研究项与规范编号，以及移动性/传播时延/无线资源三大开放问题，从 1G 一路整理到 6G 展望。**没有算法、没有仿真、没有 RL**——它是一张地图，不是一次实验。

**2. 问题设定**
要解决的问题是"任何时间任何地点的连接"（L20/L30）：卫星要补足地面网覆盖不到或经济上不划算的区域（海事、航空、高铁、灾区，L28/L32/L39），并且要在 5G/6G 里与地面网**融合**而不是并存。作者列出的具体麻烦（第 VII 节）：① NGSO 卫星相对地面高速运动 → 小区图样随之移动 → 切换与寻呼（paging）频繁（L339-345、L360）；② 传播时延取决于平台高度、网关位置与仰角、终端位置，且 NGSO 信道快速起伏（L370-376）；③ 频谱与干扰（intra-NTN 波束间、inter-NTN、inter-RAN，L386-390）。**注意：它的"负载"只出现在"忙时把地面流量卸载到卫星"（L113）和"移动跟踪区带来高寻呼负载"（L360）两句，没有把负载当成被建模的变量。**

**3. 方法骨架**
不是方法论文，骨架是**分类 + 表格**，逐节列清：
- 平台分类 Table 3（L77）：GEO 35786 km / 波束足迹 200–3500 km；MEO 7000–25000 km；LEO 300–1500 km，二者足迹 100–1000 km；UAS 8–50 km（HAPS 20 km），足迹 5–200 km。NGSO 轨道周期 1.5–10 h（L95）。
- 载荷二型（L99/L130）：**透明（bent-pipe）**只做滤波/变频/放大；**再生**在星上实现全部或部分 gNB。gNB 再分 gNB-CU（地面）与 gNB-DU（星上），F1 接口过 SRI（L147）。
- 接入架构（L132-151）：卫星直连（Fig.2 a/b/c）与中继式（Fig.3 a/b/c，另有 IAB）。
- 多连接与服务连续性（L156-178）：地面 NG-RAN + 透明/再生 NTN 的五种组合（Fig.4 a–f），两星可经 **ISL** 互联（L178）。作者明确说"LEO 用于时延敏感业务，GEO 补充带宽"（L164）。
- 历史脉络（第 IV 节）：GMR（GEO 承载 GSM，L199）→ S-UMTS（SW-CDMA 空口、IMR 中继、RRM/DCA/切换排队，L205-215）→ 4G（MSS 受多径而非大气衰减 L223；集成式 vs 混合式 L225-229；多播 AMC 三方案 CMS/OMS/Subgrouping L235；多波束频率复用与动态带宽分配 L237-239；切换分 intra-satellite / inter-satellite / vertical，L243）。
- 5G 视角（第 V 节）：SDN/NFV、网络切片、边缘计算（L255-290）、认知无线电与物理层安全（L259-265）、NOMA（L267-269）、IoST/CubeSat（L284-286）。
- 3GPP 活动（第 VI 节，L294-315）：RAN 级 NTN NR 研究 2019-12 完成、Rel-17 规范工作 2020-08 启动（L301）；给出 TR 38.811 / TR 38.821 / TR 22.822 / TS 22.261 / TR 23.737 各自的范围（L305-315）。
- 6G 展望（第 VIII 节）：HTC、多感官网络、时间工程应用、关键基础设施；全息无线电/LIS、非射频（光）、AI（L404-427）。

**4. 它声称的效果**
**没有数值结果，一篇也没有。** 全文没有任何仿真、测量或对比曲线。可称"效果"的只有规格数字与定性论断：Table 3 的平台高度/足迹表（L77）；Table 9 的 1G→6G 演进表（L430）；以及若干引自 3GPP 的定性结论，如"NTN 主要把 eMBB 与 mMTC 当作 5G 主用例，因为 URLLC 受卫星传播时延所限难以提供"（L115 逐字："Since providing URLLC services may be a challenging task due to the satellite propagation delays and stringent URLLC requirements... NTN mainly considers the eMBB and mMTC as the main 5G service enablers"）。**任何引用它当"数据来源"的写法都是错的。**

**5. 它的实验条件**
无实验。写作条件倒是给了：这是一次系统性文献综述（虽然本篇没写方法学小节，但同类工作有），信息来源是 3GPP TR/TS 原文与 IEEE/MDPI/Elsevier/Wiley 的期刊会议论文。无拓扑、无规模、无负载、无训练/评估。

**6. 它自己承认的局限**（逐字）
**未见自述局限章节。** 第 IX 节结论（L432-438）只有总结，没有任何"本文不足"的段落；第 VII 节"开放问题"是**给领域**提的开放问题，不是给自己提的。作者唯一近似自陈边界的一句是 L19（属于另一篇调查的段落结构）——不对，那是 2QRYMWBI。本篇最接近的是 L366："None of the works in past literature considered the 5G NR. Future studies might integrate the NR technology with the NTN..."——这是说**别人**没做，不是说自己没做。（依据：通读 L1-439 全文，第 VII/VIII/IX 节逐行确认。）

**7. 它没做但看起来能做的地方**（基于内容）
1. **全文只有定性时延，没有一条时延-负载曲线**：L370-376 把传播时延的构成讲得很清楚（平台高度、网关仰角、终端位置），L348 的 Table 8 甚至把 "Delay-CSI-MCS management" 列为方向——但**从未把"负载"与"时延"放进同一个关系式**。它自己开的这个口子（Table 8 第一行）就是最自然的下一步。
2. **寻呼负载（L360）只被描述为"高、难管理"，没有量化**：移动跟踪区带来的寻呼负载与到达率直接相关，是无成本的切入点。
3. **"忙时卸载地面流量到卫星"（L113）**被列为一个 use case，但全文没有任何关于卸载多少、什么时候卸载、卸载后卫星侧时延怎么变的讨论——一个纯粹的空白。
4. **馈电链路切换的运营时延被点出是"几分钟"（L428）**，且明说"短于该时延的中断不应触发切换"（L428）——这是一个现成的、由时延决定的决策阈值，但论文只是陈述，没有建模。
5. 表格里出现的多播 AMC 三方案（CMS/OMS/Subgrouping，L235）与多播预编码（L392-394）都是**按最差用户定 MCS** 的机制——这直接决定一个多播组能承载的到达率，但论文没有把这条线接到它的 5G 用例上去。

**8. 和同批其他篇的关系**
它**不引用**同批任何 LEO-RL 路由论文（参考文献 L440-757 通读，全部是 3GPP 规范与 2003–2020 年的卫星通信/网络文献；RL/ML 路由一篇都没有）。与同批的关系是**层级关系而非竞争关系**：它给出的是"这个领域被 3GPP 正式承认的物理约束清单"（传播时延构成、NGSO 移动性、切换分类、波束足迹尺寸、ISL 存在）。任何同批的 LEO 路由工作，其场景参数的合法性最终都要能对回这张表。它和我批次里的 2FBBURX7 形成鲜明对照：**后者有 RL 但没有物理约束，前者有物理约束但没有算法。**

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**没有直接贡献——没有模型、没有曲线、没有数据。** 但贡献了三条**可引用的约束事实**（都属于"设定合法性"层面而非"结论"层面）：
1. **时延的构成是几何的，不是排队的**：L370 逐字列出传播时延取决于 "the NTN platform altitude, the NTN gateway position and elevation angle, and the NTN terminal position"——这里**没有队列项**。也就是说本文语境下的"时延"是传播时延，负载引起的排队时延不在其视野内。
2. **NGSO 下信道变化快于传播时延本身**：L376 逐字："In NGSO satellite-based communications, the UE radio channel is characterized by rapid fluctuations over time; hence, after the propagation time has elapsed, the UE may no longer be able to decode the received data or can perceive an undesired QoS." 这条对"基于反馈的到达率/时延控制"是一个**根本性约束**：等一个 RTT 回来，信道已经变了。
3. **URLLC 被判定为 NTN 的难点**（L115），而 URLLC 正是时延指标的归宿——这为"LEO 直连要做时延敏感业务"提供了一个来自标准侧的、非算法视角的旁证。

**10. 一句话评价**
**这是一份 3GPP 视角的 NTN 场景与约束底账**，在方法谱系里不在算法线上而在"问题定义线"上：它不提出任何方法，但把 LEO 直连路由选题里"哪些物理量是真实存在的、哪些是必须交代的"这张清单立了下来——用它来给同批的 RL 路由论文做设定校验，比用它来找方法有用得多。


## 39NJWBI7 — Asynchronous Risk-Aware Multi-Agent Packet Routing for Ultra-Dense LEO Satellite Networks

> 覆盖：逐字读完第 1–543 行（第 464–543 行为参考文献）。全文 543 行。

**1. 一句话**
提出 PRIMAL：**事件驱动、异步、无中心协调**的 LEO 逐包路由框架，每个卫星自己在"包到达/动作完成"事件上独立决策；风险意识不是靠调奖励系数，而是把**代价回报的整条分布**学出来（IQN），再用原始-对偶（拉格朗日乘子）**直接约束 CVaR**（最差 ε 尾部的平均排队时延）。这是本批唯一把"尾风险"写成可优化约束的 LEO 路由工作。

**2. 问题设定**
超密 LEO 星座（1584 颗）里，包到达与离开**天生是异步事件**（L23 逐字："the naturally event-driven packet routing decision process (i.e., asynchronous packet arrivals or departures)"）。作者指出既有 MARL 路由的两个毛病：
① **同步时隙假设不物理**——MAPPO 一类协同 MARL 把时间切成同步时隙、每时隙每 agent 至多一次决策，所有 agent 必须等一个"global tick"（L23），人为引入时延并造成可扩展性瓶颈；即使物理时钟同步也解决不了这个问题。
② **风险意识要么没有、要么是近视的**——启发式奖励整形（把延迟/负载/能量加权求和）没有形式保证且要人工试系数（L25/L222）；CRL 类工作（如 [17]）只约束**均值**，"risk-myopic to constraining only the average values (neglecting tail-end risks)"（L25），而且依赖中心协调器。
它要回答的是：在全局流量不均导致**不可预测拥塞**（L19）时，怎么让每个卫星只用局部信息就同时管住时延与负载均衡、并且管住最坏情况。

**3. 方法骨架**
- **模型**：时变有向图 $\mathcal G_t=(\mathcal N,\mathcal E(t))$（L46）；卫星是有限缓存的存储转发路由器，四种出边 NSWE（L38/L166）；边含 FSO 激光 ISL 与 Ka 频段 GSL，可用性取决于 LoS 与最小仰角（L50）。包 $p=\{s_p,d_p,L_p,\tau_p,\tau_p^{ttl}\}$，FIFO 处理，TTL 过期或缓冲满即丢（L50）。
- **时延模型（本文最关键的一段）**：单跳时延 $D^h_{p,ij}=D^P_{ij}+D^T_{ij}(L_p)+D^Q_{ij}$（式 1，L57），到达时刻 $\tau^h_p$ 递推（式 2，L63）。传播时延 = 欧氏距离/光速（式 3）；传输时延 = 包长/链路速率（式 8），GSL 用香农公式含 SNR（式 4-5-6），ISL 用 FSO 速率式 $\frac{\tilde B}{2}\log_2(1+\kappa_1 e^{-\kappa_2 d})$（式 7）；**排队时延 = 同一出边队列中所有前序包的传输时间之和** $D^Q_{ij}(t)=\sum_{q\in\mathcal P_{ij}(t)} L_q/R_{ij}(t)$（式 9，L109）——作者明说这是局部拥塞的直接指示量（L112）。
- **优化问题 P1**（式 11）：最小化平均 E2E 时延，约束 C1 路径连续、C2 源汇、C3 每跳至多一条边、**C4 累计排队时延 ≤ $D^Q_{max}$**（式 C4，L145）。
- **POCSMDP（第 III.A 节）**：把**单包的旅程**建模成一个有限时程 POCSMDP（L158），这是半马尔可夫过程（转移带可变时长 τ = 单跳时延，L168）。状态=网络物理状态+包信息快照；动作=四条出边；观测=包状态+本地节点/邻居统计（L170）；奖励 $r$ 与 K 个代价 $\{c_k\}$；折扣 $\gamma_r,\gamma_c$。所有卫星**共享一个同构策略 $\pi_\theta$**（参数共享），本地存储、全网共用（L176）。
- **最大熵 CRL（第 III.B 节）**：P2 = max $\mathbb E[Z^r_\pi]$，s.t. $\mathcal T_{c_k}(\pi)\le D_k$（可用期望式 13 **或 CVaR 式 16**），以及策略熵下界 $\mathcal H(\pi)\ge\bar{\mathcal H}$（式 12c）。熵下界的作用是缓解"其他 agent 同时学习造成的非平稳"（L180）。
- **PRIMAL-Avg**：拉格朗日 $\mathcal L(\pi,\lambda,\alpha)$（式 17）；把 SAC 扩到离散动作多智能体——奖励 critic $Q^r_\phi$（式 18/20/24）、代价 critic $Q^c_{\psi_k}$（式 19/21/25）、actor loss（式 26，用 $\lambda_k$ 加权代价 Q 值）、$\lambda_k$ 更新（式 27，违反约束就增大乘子）、熵乘子 $\alpha$ 更新（式 28）。
- **PRIMAL-CVaR**：代价 critic 换成 **IQN** $Q^c_{\psi_k}(o,a,\zeta)$，$\zeta\sim U(0,1)$ 是分位点输入（L312）；用分位 Huber 损失训练（式 31）；CVaR 用尾部 $U(1-\epsilon_k,1)$ 上采样的 $N^k$ 个分位平均近似（式 32）；actor loss（式 33）与 $\lambda$ 更新（式 34）都换成 CVaR 估计 $\Gamma_{\epsilon_k}$。
- **Algorithm 1**（L320-348）：主循环是 **事件循环**——包到达事件触发一次动作采样，动作完成事件触发一次 transition 入回放池；乘子、目标网软更新都在事件循环内。
- **奖励/代价**（第 IV.A 节末）：代价 = 归一化排队时延 $c_h=D^Q_h/D_{norm}$，$D_{norm}=100$ ms（L397）；奖励 $r_h=\tau/D_{norm}-c_h+\Delta d+B_p$（式 35），含向目的地的大圆距离进展项；终局奖励 $B_p$ 送达为正、丢弃为负（式 36）。

**4. 它声称的效果**
全部在 1584 星场景、10 000 pps 到达率下，**5 个随机种子取平均**（L454）：
- **Table I（L449）**：SPF（Dijkstra 最短路）丢包率 **84.8%**、E2E $62.0\pm85.0$ ms、排队 $17.5\pm80.2$ ms、CVaR$_{0.25}$ 70.1 ms、违规率 85.7%；MADQN（异步 DQN 基线 [20]）吞吐 542.7 Mbps、丢包 0.00%、E2E $73.4\pm20.4$ ms、排队 $17.6\pm10.1$ ms、**CVaR$_{0.25}$ 31.1 ms**、违规率 75.5%、违规幅度 $11.60\pm8.10$ ms；**PRIMAL-Avg** E2E $64.6\pm17.7$ ms、排队 $8.9\pm5.3$ ms、CVaR$_{0.25}$ 16.0 ms、违规率 38.6%；**PRIMAL-CVaR** 吞吐 543.0 Mbps、E2E $61.5\pm18.2$ ms、排队 $4.8\pm3.0$ ms、**CVaR$_{0.25}$ 8.9 ms（在 10 ms 阈值内）**、违规率 5.8%、违规幅度 $2.47\pm2.38$ ms。
- 训练曲线（L441-443）：三种学习算法约 150K 迭代后丢包率近零；收敛时 E2E 时延 PRIMAL-CVaR ≈62 ms < PRIMAL-Avg ≈66 ms < MADQN ≈77 ms；排队时延 MADQN 稳定在**约 18 ms（违反 10 ms 阈值）**，PRIMAL-Avg 恰好压在 10 ms，PRIMAL-CVaR 降到约 5 ms。
- **延迟成分分解（Fig. 8，L458）**：PRIMAL-CVaR 相对 PRIMAL-Avg **多花约 1 ms 传播时延**（走物理上更长的路），换来**排队时延降 46%**。
- 摘要口径（L11）："reduces queuing delay by over 70%, and achieves a nearly 12 ms end-to-end delay reduction in loaded scenarios"——与 Table I 对照，70% 是相对 MADQN 的 17.6→4.8，12 ms 是 73.4→61.5。

**5. 它的实验条件**
自建 Python/PyTorch **异步事件驱动仿真器**（L391）。拓扑：Walker-Delta，**22 星/轨道 × 72 轨道 = 1584 星**，高度 600 km，倾角 53°，最小仰角 15°（L393）。地面：**只有 3 个地面站**（卢森堡、迪拜、北京），等概率作源或宿（L393）。卫星位置 **每 100 ms 更新一次**；"**固定**链路速率 GSL 1000 Mbps / ISL 50 Mbps"（L393 逐字："We set stable link data rates at 1000 Mbps for GSLs and 50 Mbps for ISLs"）；节点与链路缓冲均 16 Mbits；包长 80% 为普通包 64.8 Kbits、20% 小包 16.2 Kbits；TTL 上限 H=64。**每次运行 30 秒训练或评估 epoch，到达率 10 000 packets/s 泊松，共 300 000 包**；每 1 ms 一次训练迭代，每 2 秒报一次指标（L393）。
网络：actor 与两个 critic 共享主干（两层 MLP，512 隐单元）+ 独立输出头；IQN 两层、$N=N'=N^k=64$；batch 1024；回放池 300 000；$\gamma_r=0.99,\gamma_c=0.97$（L395）。熵下界 $\bar{\mathcal H}\approx0.067$，由"最优动作置信度 0.99"hueristic 反推（L429）。约束阈值 $D^Q_{max}=10$ ms（L431）。
基线：SPF（基于可预测轨道运动预计算路由表）、MADQN（[20] 的异步 DQN，用式 37 的启发式奖励，等价 $\lambda_k=1$）、以及本文两个变体。作者**明确说明 [17] 因为要求同步联合动作，在他们的异步仿真器里跑不了**，因此只能用 PRIMAL-Avg 当作它的异步替代（L437）。训练与评估同一套仿真器（离线 CTDE，共享回放池，L385）。

**6. 它自己承认的局限**（逐字）
- **无强对偶保证**（L236）："Note that primal-dual CRL has been proved to have strong duality for single-agent fully observable RL [26]. However, the constrained and partially observable MARL problem of our case is fundamentally more challenging and highly nonconvex, such that there exist none known strong duality guarantees [41]. Despite this fact, primal-dual approach still serves as a feasible and principled way to solve the problem approximately."
- **训练阶段仍非完全去中心**（L385）："Note that we use a shared centralized replay buffer here by following the Centralized Training and Decentralized Execution (CTDE) paradigm during offline training. However, it can be easily extended to use private replay buffers via online federated learning, as shown in [20]."
- **对照缺失**（L437）：[17] 因同步假设无法在本仿真器运行，作者自认只能以 PRIMAL-Avg 代跑。
**全文没有独立的 Limitations 章节**，第 V 节结论（L460-462）无任何自述不足。

**7. 它没做但看起来能做的地方**（基于内容）
1. **到达率只测了一个点（10 000 pps）**——全文没有第二档流量。作者在摘要里说 "in loaded scenarios"，但**没有做负载扫描**，也就没有"到达率 → 时延/丢包"的曲线。这是最直接、最省事的下一步。
2. **式 4–7 的速率模型在实验里被架空了**：论文花大力气写香农 SNR 与 FSO 速率公式，实验却用"**stable** link data rates 1000/50 Mbps"（L393）。也就是说距离/信噪比导致的速率变化从未被激活——链路速率本应随几何关系变化，这是一个自己写了模型却没用的问题。
3. **"流量分布不均"是全文动机（L19），但实验里三个城市等概率**（L393）。动机与设置在这一点上是脱节的：真正的热点不均（比如一个源产生 90% 流量）没有构造。
4. **$D^Q_{max}$ 只在 10 ms 一个点**：CRL 最有价值的"约束松紧 vs 性能"前沿曲线完全没画。$D^Q_{max}\in\{2,5,10,20,50\}$ 是很自然的扫描。
5. **没有 risk-aware 但非分布式的对照**：只用了一个 risk-oblivious 基线（MADQN），没有"WCSAC 风格的平均-方差 critic"或"人工调好的 CVaR 惩罚系数"这类中间对照，因此"分布式的收益有多大"与"风险意识的收益有多大"两个因素被绑在一起。
6. **TTL、缓冲大小、流量成分（80/20 包长比）都是单点设定**，没有任何敏感性分析。
7. **可扩展性只在 1584 星一个规模上验证**，论文却把"可扩展"作为核心卖点（L40）。

**8. 和同批其他篇的关系**
它是 **LEO 路由 MARL 这条线里最新的一段**，引文密集地覆盖了这条线的全部近亲：**[17] Lyu et al.（JSAC 2024，constrained MARL 路由，被它批评为同步+只约束均值）**、**[19] Li, Wu & Wang（WCNC 2025，cooperative-MARL + 排队论模型）**、**[20] Lozano-Cuadra et al.（持续 DRL 去中心卫星路由 = MADQN 基线）**、[15] IRIS（软件定义卫星智能路由）、[16] 单智能体 DRL 路由、[25] 多智能体 DRL 负载均衡路由（L464-543 逐条看完）。方法源流上它接的是 **SAC（[37]）→ 离散 SAC（[40]）→ IQN（[39]）→ CVaR 约束策略优化（[31]）→ WCSAC（[27]）**，也就是说：**它的"风险感知"部分是从通用安全 RL 搬来的，LEO 只是载体**——真正的领域新意在于**事件驱动的半马尔可夫异步形式化**（第 III.A 节）与"排队时延作为本地拥塞指示量 + 约束量"这个建模选择。同批若有 2W8BJ7ME/35T2JJRJ 一类 LEO 路由篇，本篇是它们最可能引用的同期锚点。

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**这是本批最直接相关的一篇。** 它贡献了三件可用的事实：
1. **一个闭合的、可直接抄的"负载→时延"分解式**：式 1 + 式 9。排队时延被写成"同一出边队列中前序包传输时间之和"，即 $D^Q=\sum L_q/R$。这条式子可以把任意到达率映射到排队时延，**不需要仿真就能算**，是本批少见的可复用公式。
2. **一个"平均 vs 尾部"的定量分裂事实**：在 10 000 pps 下，按**均值**优化代价的路由（PRIMAL-Avg）把平均排队时延压到 8.9 ms 却留下 **CVaR$_{0.25}$=16.0 ms** 的尾巴；按 CVaR 优化才把尾巴压到 8.9 ms。**这说明"到达率固定时，时延的均值不能代表时延的分布"**——对任何以平均时延为目标函数的选题，这是一条必须先回答的反驳。
3. **一个"用传播时延换排队时延"的兑换率**：+1 ms 传播时延 ↔ −46% 排队时延（L458）。在有负载的网络里，**最短路不是最快路**这件事被量化了。
**但要小心它的边界**：这三条全部来自**单一负载点（10 000 pps）**。论文没有做到达率扫描，所以它**没有**给出"负载升高时时延如何劣化""哪个到达率下风险约束开始不可行（infeasible）"这两条对选题最关键的曲线。它证明的是"在一个负载点上风险感知值多少"，不是"负载变化时会发生什么"。

**10. 一句话评价**
**把安全 RL 的 distributional + CVaR 工具第一次系统性地接到 LEO 逐包路由上，并用事件驱动半马尔可夫把"同步时隙"这个不物理的假设摘掉了**——领域贡献在**形式化与约束建模**（排队时延当本地拥塞量、CVaR 当约束），算法部件（SAC/IQN/primal-dual）全部来自通用 RL；它最大的空白恰恰是它最该做的：**只测了一个到达率**，因此它给出的是"负载固定时的风险价值"，而不是"负载变化下的到达率-时延规律"。


## 4QG5VYHQ — Information Freshness of Updates Sent over LEO Satellite Multi-Hop Networks

> 覆盖：逐字读完第 1–507 行（第 406–507 行为参考文献，正文 1–404）。全文 507 行。

**1. 一句话**
把 LEO 多跳中继网建模成 **K 级串联 M/M/1 队列（含逐节点交叉流量、逐链路擦除信道）**，给出**平均 AoI 的紧近似与上下界、PAoI 分布尾部的上界、以及系统平均时延的精确值**，再通过蒙特卡洛验证；核心发现是 **AoI 关于负载是 U 形曲线、存在一个最优运行点 $\rho^*$**，且丢包在低负载下有害、在高负载下反而有益。**这是本批唯一把"到达率扫描"当作主要实验维度的论文。**

**2. 问题设定**
船舶/货物跟踪这类卫星 IoT 应用（VDES、AIS、ADS-B，L19/L36）的端点是"多个相距极远的地面源与地面站"，单跳连不上，必须靠 **ISL 串起若干颗卫星中继**（L21）。麻烦在于：**串联队列之间的相互作用使理论分析极难**（L28 逐字："These multi-hop networks are difficult to study theoretically due to the complex interactions between subsequent queueing systems, and the literature on the subject is limited"），再加上**每条链路有独立的错误率**、**每个节点还有自己的交叉流量**（L58）。作者自述本文是"第一篇对一般拓扑给出平均 AoI 与总时延的很好近似与上下界的工作"（L28）。指标取舍上，它明确说对这类应用**信息新鲜度（AoI）比传统时延更重要**（L19）。

**3. 方法骨架**
- **模型**（第 III 节）：K 跳串联，第 k 跳服务速率 $\mu_k$（平均服务时间 $S_k=1/\mu_k$），擦除概率 $\varepsilon_k$（以 $1-\varepsilon_k$ 正确到达，L60）。源是速率 λ 的泊松过程；节点 k 还接收速率 $\theta_k$ 的交叉流量，其中比例 $\psi_k$ 从该节点离开本连接、其余沿同一条路走（L58）。汇聚到节点 k 的交叉流量 $\bar\theta_k=\sum_{j=1}^{k}\theta_j\prod_{i=j}^{k-1}(1-\psi_i)(1-\varepsilon_i)$（式 1）。上行接入两种极端：理想多包接收（UNB/SigFox）与破坏性碰撞（经典 ALOHA）；两者都归结为"错就不重传，等下一次更新"，得到**被稀释的泊松流 $\lambda(1-p_c)$**（L73-77，Fig.3 验证了该近似的合理性）。
- **平均 AoI 的几何法**（第 III.A-III.B 节）：AoI 过程是锯齿（Fig.4），时间平均 AoI 写成面积比（式 2），每个梯形的面积 $Q_i=Y_iT_i+Y_i^2/2$（式 3），于是 $\bar\Delta=\lambda\mathbb E[Q_i]$（式 4）。**有错时**引入"连续 n 个包丢失"的额外面积 $Q_i^{(n)}$（式 5-6），再按丢包个数取期望得 $\bar\Delta=\lambda\sum_n p_s(K)(1-p_s(K))^n\mathbb E[Q_i^{(n)}]$（式 7），其中 $p_s(j)=\prod_{i=1}^j(1-\varepsilon_i)$。关键中间量是**节点响应率** $\alpha_j=\mu_j-(p_s(j)\lambda+\bar\theta_j)$（L141），总系统时间服从 **Hypoexponential 分布**（式 8-9），进而把式 7 化成闭式**式 10**。
- **界与近似**（第 IV 节）：$\mathbb E[Y_iT_i]$ 难以精算，于是给出
  - **近似** $\bar\Delta\simeq\sum_j\frac{1}{p_s(K)\alpha_j^{n_j}}+\frac{1}{\lambda p_s(K)}+\frac{(1-p_s(K))^2}{\lambda p_s(K)^2}$（式 14，假设 $Y_i$ 与 $W_i$ 独立）；
  - FCFS 的**下界**（式 21，用 $\sum(x_i)^+\ge(\sum x_i)^+$ 式 17 推得）与**上界**（式 22，用 $W_{i,k}\le T_{i-1,k}$）；
  - 合并成 $\bar\Delta$ 的上下界（式 23）。
- **队列策略**：FCFS；**OPF（Oldest Packet First，按源端时间戳而非到达时间排优先级）**；**HAF（Highest Age First，按该节点上"当前 AoI 最大"的源优先）**（L84/L257）。OPF/HAF 的下界由式 24-29 给出（用了两个简化假设：队列从不为空、且后到的包都更年轻，L259）。
- **PAoI 尾部上界**（第 IV.C 节）：$\xi_i\le T_{i-1}+S_i+Y_i$（式 30），右边是参数向量 $\omega=(\alpha,\mu,\lambda)$ 的 Hypoexponential 变量，CDF 由式 31 给出。
- **验证**：蒙特卡洛（L317），两种拓扑：**line**（K 颗卫星串联、每个节点都有地面源、$\psi_i=0$，瓶颈在最后的下行）与 **dumbbell**（K=4，三个源-宿对共享一条 ISL，$\theta_2>0,\psi_2=1$）（L326-328）。

**4. 它声称的效果**
- **AoI 关于负载是 U 形**（L344，Fig.7a）：低负载时主导项是"同源相邻包之间的间隔"，AoI 很高；高负载时排队成为主导，AoI 又升上去。**中间存在最优负载**。举例：$\rho=0.05,K=10$ 时每个源到达率仅 0.004（因 $\mu_{DL}=0.8$），平均到达间隔 250。
- **界的紧度**：低 ρ 时上下界很紧（排队近似的误差对总 AoI 影响小）；高 ρ 时仍"reasonably tight"尤其 K 小；近似式"非常接近经验曲线、仅略微高估"（L344）。
- **丢包的双面性**（L346）：低 ρ 时丢包**增加** AoI（本来就稀少的包丢一个影响很大）；高 ρ 时丢包**反而降低**平均 AoI——因为包很密、丢一个无关紧要，而**下行负载下降缓解了拥塞、减少了排队时延**。作者自己把它称作 age-dilemma 的又一个实例（L54）。
- **缓冲影响可忽略**（L346/L50）：无限缓冲的假设下，有限缓冲对平均 AoI 的影响**低于 1%**，除非缓冲只有 1-2 个包。
- **调度策略**（L361）：OPF 与 FCFS 在全网平均 AoI 上**差别可忽略**；**HAF 在高负载下能小幅降低 AoI**。公平性上（Fig.10，JFI）：OPF 显著缩小源间差距、链越长效果越明显；HAF 居中。
- **PAoI 尾部上界很松**（L374）：除 $\rho=0.8$ 外，界"几乎总是松的"；作者解释是因为界推导把 $Y_i$ 与 $W_i$ 解耦，而两者的**负相关在尾部极其重要**（长的到达间隔与长的等待同时出现现实中极罕见，但在上界分布里不罕见）。
- **ALOHA vs 泊松**（L379，Fig.12）：在第一跳速率相同的前提下，ALOHA 上行的 AoI 略低于理想泊松，除极高负载外。
- **Dumbbell**（L383-392）：$\rho=N\lambda$。**源数越多，达到最小 AoI 的最优负载越高**（$\rho=0.7$ 时 N=2 对应 λ=0.28，N=6 对应 λ=0.093）；高 ρ 段 AoI 上升但在 N 大时更平缓。HAF 在高负载下能明显降低平均 AoI（Fig.14），且负载体现在"源间协调"上。
- **一条可以直接拿走的网络设计结论**（L390 逐字）："the bottleneck should be placed as early as possible in the path, as links before might suffer from queueing, but packets coming out from the bottleneck are spaced far apart in time and are almost never queued at later links. **The line network example we presented above, with gradually increasing load until the bottleneck in the downlink, is the worst possible scenario for AoI.**"

**5. 它的实验条件**
**仿真参数表（Table II，L349）**：line 网 $K\in\{2,6,10\}$；$\mu_{ISL}=1$；$\mu_{DL}=0.8$；$\psi=0$；所有链路 $\varepsilon=0.01$；每个源 100 000 个包；dumbbell $K=4$、交叉源数 $N\in\{2,6,10\}$。
**负载定义（式 32）**：$\rho=(\lambda+\sum_j\theta_j)/\mu_{DL}$；取 $\theta_1=0$、$\lambda=\theta_j=\rho\mu_{DL}/K$（L342）。**即：负载 ρ 是被主动扫描的自变量**，从低到高扫过整条曲线，且明确不计入链路错误率以便与无错情形可比。
验证方式是**蒙特卡洛**而非包级网络仿真；仿真中丢弃初始瞬态与尾部包以保证稳态（L334）。**没有真实的 Walker 星座几何、没有轨道动力学、没有 ISL 切换**——"LEO"体现在参数含义（ISL/DL 速率不同、仰角、覆盖）而非拓扑构造。

**6. 它自己承认的局限**（逐字）
- **跳间服务时间独立**（L60）："in this work, we model the service time for each link for the same packet as independent for tractability. This assumption is equivalent to considering uncorrelated distances between pairs of satellites; **considering a correlated system is left for future work**."
- **无限缓冲**（L50）："The analysis is done for **infinite buffers** at each node, but it has been observed that having a limited storage capacity has little impact in the age performance of the multi-hop network."（后文 L346 给出量化：除 1-2 包缓冲外影响 <1%。）
- **关键项无法精算，只能给界**（L161）："The $\mathbb E[Y_iT_i]$ term is complex... its analytical derivation is **too cumbersome to calculate for the general case**, but we can find lower and upper bounds on the average AoI for each source."
- **OPF/HAF 的下界用了两个简化假设**（L259）："The lower bound is based on two simplifying assumptions, both of which reduce the age by removing possible cases from the calculation..."（队列从不为空；只考虑后到的包都更年轻）
- **PAoI 尾部上界很松**（L374）："In this case, the bound is **almost always loose**, except for $\rho=0.8$... The looseness of the bounds can be explained by the fact that they are derived by decoupling $Y_i$ and $W_i$."
- **未来工作自陈**（L404）：拥塞控制（限制源生成速率以维持最低 AoI）、抢占式队列管理（短状态更新与长传输混合）、**更真实的 ISL 模型（把每个中继变成 G/G/1）**、以及**含错误情形的更紧尾部界**。

**7. 它没做但看起来能做的地方**（基于内容）
1. **路径是给定的，路由从不被决策**（全篇）：它分析 AoI，但不优化路径；连"换一条路"这种动作都不存在。作者自己在 L404 提的"拥塞控制"也只限速不换路——**把限速与选路联合起来是开着的口子**。
2. **$\rho^*$（最优负载）只被画出来，没有被求解**：Fig.15 给了 $\rho^*$ 随源数 N 的曲线，但没有解析的 $\rho^*$ 表达式或闭式条件。既然式 10/14 已经是闭式，$\partial\bar\Delta/\partial\rho=0$ 应该是可推的。
3. **交叉流量参数 $\theta_k,\psi_k$ 是外生静态的**：真实的 LEO 交叉流量会随轨道位置与时刻变化，论文完全没碰时变性。
4. **跳间距离相关性被显式排除**（L60），但 LEO 同轨 ISL 链的距离几乎完全相关——这是它自己指出却未做的最贴近物理的一条。
5. **只到 M/M/1**，G/G/1 被留给未来（L404），而 LEO 的 ISL 服务时间显然不是指数分布（定长包 + 基本恒定速率）。
6. **PAoI 尾部界太松**（L374 自述），且**不覆盖有错情形**（第 IV.C 节标题就是 "in the error-free case"）——最需要尾部保证的场景恰好没有界。
7. **HAF 只在高负载下有收益、OPF 只改善公平**，两者都没有被组合，也没有与"限速"这一最古老的 AoI 手段联合评估。

**8. 和同批其他篇的关系**
它与同批的 LEO-RL 路由论文（如 39NJWBI7）是**同一物理系统、两种方法论**的镜像关系：39NJWBI7 把排队时延作为约束用 CVaR 去优化、但只在**一个到达率**上验证；本篇不做任何学习、**却把整条到达率→AoI 曲线解析地算了出来**。参考文献（L406-507，逐条看完）显示它的血统完全在**排队论/AoI 理论**一侧：Kaul/Yates [5]、Bedewy-Sun-Shroff 的多跳 LCFS 最优性 [33][34]、Champati 的 PAoI 统计保证 [31]、Yates 的抢占服务器网络 [40]、以及作者自己的前作 [17]（2 星串联的理想链路版本）与 [32]（串联队列的 PAoI 分布）。**它不引用任何 RL/DRL 路由工作。** 与 524XNF29（3GPP NTN 综述）互补：后者给约束清单，本篇给约束下的解析性能。

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**本批到目前为止最直接、最可复用的一篇。** 它贡献了五条硬事实：
1. **AoI 对负载是 U 形，存在内部最优 $\rho^*$**（L344/L390）。这条直接否定了"负载越低越好"和"负载越高越好"两个直觉，且给出了两种机制的交接：低负载段由**到达间隔**主导，高负载段由**排队**主导。
2. **$\rho^*$ 随源数 N 单调升高**（L390）：同一个总负载 ρ 由更多源分摊时，每源 λ 更小、包流更平滑，最优运行点就上移。（L390 给出具体数：$\rho=0.7$ 时 N=2 → λ=0.28，N=6 → λ=0.093。）
3. **丢包在过载侧是"减压阀"**（L346）：同一积压水平下，链路错误通过降低下游负载**降低**平均 AoI。**任何把"丢包率"当作纯负指标的时延研究都需要处理这个反号。**
4. **瓶颈位置决定 AoI，早瓶颈优于晚瓶颈**（L390）：负载沿路径递增、直到下行才拥塞的 line 网络是 AoI 最差的情形。这是一条纯粹的拓扑-负载交互事实。
5. **一组可直接代入的闭式表达式**（式 10/14/23/29）：给定 $\lambda,\theta_k,\psi_k,\mu_k,\varepsilon_k,K$，可以直接算出平均 AoI 与均值的上下界，不需要仿真。**这为"负载扫描"提供了一个零成本的高保真对照组**——任何声称在负载变化下改进了时延/AoI 的学习方法，都可以先与这条解析曲线对账。
**边界**：它的"时延"是 AoI 与系统时延，**不是到达率意义上的吞吐**；且所有结论建立在 M/M/1 + 独立跳间服务时间上，**跳数 K ≤ 10、交叉流量静态**，与真实 Walker 星座的动态性有距离。

**10. 一句话评价**
**把 LEO 多跳中继的 AoI 从"单跳/两跳特例"推进到一般 K 节点串联队列，并给出了整条负载-新鲜度曲线与最优运行点**——方法谱系上它站在**排队论/AoI 理论**那条线的最前沿，**完全不做学习、也不做路由**；对本次选题而言它是**最理想的"解析对照物"**：凡是声称"负载变化下改进了到达率/时延"的学习类工作，都应该能对回它的 U 形曲线与 $\rho^*$ 位移规律。


## 3MRQRWHU — Multi-QoS routing algorithm based on reinforcement learning for LEO satellite networks

> 覆盖：逐字读完第 1–468 行（正文 1–361，参考文献 363–443，作者简介 445–468）。全文 468 行。

**1. 一句话**
用**表格型 Q-learning** 给 LEO 星座做逐业务选路，用 DiffServ 的优先级给业务分级，再加两条工程手段：①**等待时间晋级**（低优先级业务等久了自动提权，防止饿死）；②**辅助收敛**（走过的节点临时删掉，压缩动作空间、避免绕圈）。出发点不是时延最优而是**"高优先级业务优先 + 低优先级业务用来填负载均衡"**这个双目标折中。

**2. 问题设定**
LEO 卫星"资源受限 + 拓扑时变"，且用户请求呈**区域集中**（L17 逐字："concentrated services requests in small areas and time-varying network topology in the case of limited regional resources"）。作者指出的既有毛病是：多 QoS 路由优化会让流量**挤在时延最短的那条链路上**，破坏负载均衡，而且**低优先级业务被长期忽略**（L17）。它要在满足业务多 QoS（时延/丢包/带宽三类）的同时，把全网的**链路利用率方差**压下来，并且让低优先级业务也能被处理（L27-33）。

**3. 方法骨架**
- **拓扑**（第 2.1 节）：$N=i\times j$ 星座，每星 4 条 ISL（2 条同轨 + 2 条异轨）；**极区（纬度 >70°）异轨链路关闭**，且第 1 条与第 6 条轨道运行方向相反形成的**缝隙两侧不建链**（L41）——所以拓扑是不规则的。时间切成 $\tau_n=(t_{n-1},t_n]$，**每个时间片内拓扑视为静态**（L46）。
- **业务模型（DiffServ，第 2.2 节）**：每个业务 $u$ 有三个需求等级：$\phi_{delay}(u),\phi_{loss}(u),\phi_{band}(u)$，总等级 $\phi(u)=\phi_{loss}+\phi_{band}+\phi_{delay}$（式 1）。权重 $\alpha=\phi_{delay}/\phi^{max}$、$\beta=\phi_{loss}/\phi^{max}$、$\lambda=\phi_{band}/\phi^{max}$、$\gamma=(\phi^{max}-\phi(u))/(k\phi^{max})$，满足 $\alpha+\beta+\lambda+k\gamma=1$（式 2）；**$\gamma$ 是负载均衡的权重**，业务需求越低、$\gamma$ 越大——即"低需求业务承担负载均衡任务"。
- **等待时间晋级机制**：定义 $\phi_{time}(u)$，业务每跨过一个未被处理的时间片就 +1，上限 $\phi_{time}^{max}$；最终优先级 $\phi_{time}(u)+\phi(u)$（式 3）。上限的作用是"**避免低优先级业务反过来长期抢占高优先级资源**"（L80）。
- **问题**（式 10）：max $R(\mathbf{path})=\max(\alpha r^{delay},\beta r^{loss},\lambda r^{band},\gamma r^{var})$，约束为：链路总带宽 ≤ 链路容量（式 4）、业务带宽 ≤ 路径上最小可用带宽（式 5）、路径时延 ≤ 等级要求（式 7）、路径丢包率 ≤ 等级要求（式 8）、路径带宽 ≥ 等级要求（式 9）。
- **Q-learning（第 3.1 节）**：MDP $M=(S,P,R,A)$；**状态 $S_{\tau_p}=\{\mathrm{delay}(e_{i,j}),\mathrm{loss}(e_{i,j}),\mathrm{band}(e_{i,j})\}$（式 11）**；动作 = 从当前星跳到下一跳星；$\varepsilon$-greedy（式 12）；Q 表更新用式 13 的 Bellman；$a^*=\arg\max Q^*$（式 14）。
- **奖励（第 3.2 节）**：用 min-max 归一化定义 $r^{delay},r^{loss},r^{band}$（式 15）；负载均衡用**全网链路利用率的方差** $\mathrm{Var}(E)=\frac{\sum(l(e_{i,j})-\overline{l})^2}{\mathrm{num}(e_{i,j})}$（式 16），$\mathrm{Var}^{max}=(\mathrm{Band}(e_{i,j})/2)^2$（式 17），$r^{var}=\frac{\mathrm{Var}^{max}-\mathrm{Var}(E)}{\mathrm{Var}^{max}}$（式 18）；总奖励 $r(a)=\alpha r^{delay}+\beta r^{loss}+\lambda r^{band}+k\gamma r^{var}$（式 19）。
- **辅助收敛算法（第 3.3 节）**：标记走过的节点，把该节点及其邻接节点临时设为"不可通行"，直到到达目的节点；好处是**在节点 H 处可选动作从 3 降到 2**（L266）。Algorithm 1（L273-310）：按 $\phi$ 排序业务 → 逐业务初始化 Q 表 → 迭代 maxepoch 次 → 每次删节点/断邻边 → 更新 Q → 记录总回报 $R(j)$ → 取最优路径 → 更新拓扑 → 移除该业务。

**4. 它声称的效果**
- **负载均衡效用**（Fig.6，L346）：AQLRA 相对 Dijkstra **提升 200%**、相对蚁群 **提升 50%**。理由是 Dijkstra 只看跳数导致业务集中在少数链路、蚁群受权重设置影响更偏时延。
- **综合效用**（Fig.7，L353）：AQLRA 相对 Dijkstra **提升约 88%**、相对蚁群 **提升约 43%**。
- **低优先级业务的时延稳定性**（Fig.5，L340）：设置"每个时间片都有大量高优先级业务，而 Default 业务数随时片递增"。**从第 3 个时间片起 Default 业务无法在片内处理完、平均处理时延开始上升**；AQLRA 因考虑因素多、总时延更大；但**第 5 个时间片后等待时间晋级机制生效**，Default 业务的平均总时延**被稳定在 80 ms 附近**；而两个对比算法（优先级固定）的总时延**波动很大**，说明"相当一部分低优先级流量长期没被处理"。
- **高负载下高优先级的质量**（L328）：高负载时 AQLRA 让低优先级业务**主动选差链路**，把好链路留给"可能到达的高优先级业务"，即**用牺牲低优先级换取高优先级的 QoS 保证**。

（所有数字都没有给置信区间、重复次数或方差。）

**5. 它的实验条件**
**星座（L318）**：**66 颗卫星、6 条极轨**，轨道高度 720 km，倾角 86.4°，轨道面间距 31.6°，相位因子 0.5；**纬度 >70° 时不建异轨链路**；运行周期 100.45 min，**时间片 = 1 min**。
**业务**：源/宿节点在 66 星中随机选取；业务最小带宽需求**按需求等级在 10–100 Mb/s 之间**；**每条卫星链路最大可用带宽 4000 Mb/s**；业务起止时间用**正态分布**描述并随机生成持续时间。
**负载维度**：没有显式到达率参数。Fig.4 固定一组同源同宿请求；Fig.5 通过**"Default 业务数量随时片增加"**制造负载上升（L340）；Fig.6/Fig.7 用"用户数量增加"作横轴。**训练与评估同一套仿真器**，无跨场景测试。
**基线**：只有 Dijkstra 与蚁群算法（L320-322），**没有任何其他 RL/DRL 路由基线**。

**6. 它自己承认的局限**（逐字）
只有结论段一处（L361）："In future research, we will consider **making the algorithm update the networks model in time when the networks topology changes**. At the same time, we also **incorporate cross-layer information transmission between different satellite orbital planes** into future research topics."
即作者自认：**当前算法在网络拓扑时变时并不及时更新网络模型**，且**尚未利用跨层信息**。**全文没有独立的 Limitations 章节。**

**7. 它没做但看起来能做的地方**（基于内容）
1. **全文没有给出 delay(e_ij) 的显式公式**——我逐行读完全文（1–361）并核对了符号表（Table 1 只写 "delay(·) Time delay calculation function"），**时延自始至终是一个未定义的黑盒链路属性**：没有传播时延（距离/光速）、没有传输时延（包长/速率）、**完全没有排队时延**。这意味着它的"时延"无法随负载变化——**这是本篇最大的结构性空洞**。
2. **状态是连续量，却宣称用 Q 表**：式 11 的状态含 delay/loss/band 三个连续值，论文从未说明如何离散化（L202-210 只说"初始化 Q 表…直到 Q 表收敛"）。**状态空间定义与表格型 Q-learning 不兼容**。
3. **式 3 自我指涉**：写成 φ(u)=φ_time(u)+φ(u)，右边又出现 φ(u)，字面上是循环定义；**式 9 的符号方向也疑似笔误**（把带宽与时延两个量直接比较）。
4. **负载维度极粗**：只有"业务数增多"这一种负载变化，没有到达率参数、没有泊松/突发流量模型、没有 ρ 的扫描。Fig.5 的横轴是"时间片"而非负载——**时延-负载曲线实际上没被真正测量过**（因为时延本身无定义，见第 1 条）。
5. **规模只有 66 星**，与 LEO 巨型星座差两个数量级；且没有可扩展性讨论。
6. **没有与任何 RL 路由方法对比**，只有两个经典启发式；"提升 200%"缺少强对照。
7. **没有给重复实验次数/方差**，所有增幅都是单点数字。
8. **等待时间上限 φ_time^max 与 k 等超参没有做敏感性分析**。

**8. 和同批其他篇的关系**
属于 **LEO 路由的"经典 Q-learning + 工程技巧"支线**，与 39NJWBI7（PRIMAL，事件驱动 MARL + 分布 RL + CVaR）形成鲜明的方法代差：**本篇是表格型 Q-learning + 手工加权奖励，正是 PRIMAL 所批评的 "heuristic reward shaping" 典型**（39NJWBI7 的 L25 逐字批评："Existing attempts at risk-awareness often rely on heuristic reward shaping... they require extensive human-effort on trial-and-error based adjusting"）。引文（L363-443）覆盖 LEO 路由传统文献：GRouting（图 DRL 路由 [11]）、DRL 负载均衡路由 [12]、时变拓扑最短路 [33]、蚁群 RWA [35-37]、Littman 的 Markov games [31]。**不引用本批任何其他篇目**。与三篇 AoI 类（4QG5VYHQ / 39NJWBI7 / 2FBBURX7）不同，它完全不关心信息新鲜度。

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**贡献非常有限，但有一条值得记的机制性事实。**
- **可贡献的**：它展示了**优先级老化（aging）在过载时对低优先级时延的稳定作用**——Fig.5 里固定优先级的两个算法时延剧烈波动、"相当部分低优先级流量长期未被处理"，而加了 φ_time 晋级后低优先级平均时延**稳定在 80 ms 附近**（L340）。也就是说：**在负载上升到某一点后，"谁先被服务"对时延的影响可能大于"走哪条路"**。这条观察独立于它的路由算法。另外，它给出的**负载均衡度量（全网链路利用率方差，式 16-18）**是一个便宜且可复用的拥塞代理指标。
- **不能贡献的**：它**没有到达率**（业务靠"正态分布的起止时间"生成，没有 λ），**没有排队模型**，**连时延本身的公式都没有**（见第 7 项第 1 条）。因此它**无法回答"到达率升高时时延如何变化"**——它所谓的"负载"只是"业务条数变多"，而时延是被当作链路静态属性喂给 Q 表的。**若要用它支撑任何负载-时延论断，只能引它的优先级老化定性结论，不能引任何数字。**

**10. 一句话评价**
**一个用 DiffServ 优先级 + 等待时间老化 + 表格 Q-learning 拼起来的 LEO 多 QoS 路由工程方案**，方法谱系上处在"经典 Q-learning 手工奖励"这一代（正被 39NJWBI7 一类分布 RL/受约束 RL 取代），且**时延在整篇论文里从未被定义**——因此它对"负载变化下的到达率/时延"只提供了一个定性机制（优先级老化可稳定过载时的低优先级时延）和一个可复用的负载均衡指标，**不提供任何可引用的时延-负载数据**。






## 36RZKNW5 — An integrated routing and data fragmentation strategy for optimizing end-to-end delay in LEO satellite networks

> 覆盖：逐字读完第 1–435 行（正文 1–346，CRediT 348–350，参考文献 360–435）。全文 435 行。

**1. 一句话**
在 **DTN/接触图（CGR）** 框架下，先用 **Yen 算法**找出 K 条候选多路径，再按 **Bundle Protocol 把数据切成碎片分派到多条路径**，用一个贪心迁移过程（把数据从"时延最长的那条路"搬到"时延最短的那条路"）来最小化 T_M = max_r T_r；方法名叫 RSFFA。**没有强化学习**——这是本批少见的纯启发式 + 组合优化路线。

**2. 问题设定**
LEO 网络拓扑时变、链路频繁中断，传统路由算法应付不了（L26）。既有工作的问题被逐条列出：基于 CGR 的路由（[6][7]）虽然能找最优路径，但"**在应对星间链路拥塞方面鲁棒性不足**"（L32 逐字："the robustness of these methods in handling inter-satellite link congestion remains insufficient"）；单路径路由对拥塞和突发事件的适应性差（L56）；多路径算法要么对拓扑变化敏感、要么管理开销大（L56）。作者要的是：**多条可用路径同时用、并按各条路的容量把数据分下去**，让最慢的那条路不再成为端到端时延的瓶颈（L216）。

**3. 方法骨架**
- **系统模型（第 3 节）**：图 G=(V,E)，类 Iridium 的同轨/异轨 ISL；只考虑"用户经卫星链路到地面站"这一过程（L85）。用 DTN 的**存储-转发 + Bundle Protocol**，把数据包 D 切成若干 bundle，各 bundle 独立选路并行传输，中间节点找不到下一跳就暂存等机会（L70/L87）。
- **时延模型（第 3.2 节，本文最该被仔细看的一段）**：把总时延拆成三部分（L91）：
  - 传播时延 t_prop = L_ij / c（式 1）；
  - 传输时延 t_trans = D_ij / r_ij（式 2）；
  - **等待时延** t_wait = 0（若 t_start ≤ t_now），否则 = t_start − t_now（式 3）——**注意：这里的"等待"是"等接触窗口开始"的链路可用性等待，不是排队拥塞等待。**
  - 接触容量 C_ij = (I_ij − t_prop_ij) × r_ij（式 4）；路径容量取沿途接触的最小值；路径时延 T_r = Σ(t_prop + t_trans + t_wait)（式 5）。
- **问题 P1（第 3.3 节）**：从 N 条可用路径中选 M 条，把数据 D 分下去，最小化最晚到达时间 T_M = max_r T_r（式 6/7）；约束 C1 数据全部分完、C2 不得超过各路径容量、C3 恰好选 M 条、C4 非负/0-1（L138-141）。这是一个 **MILP**，M 在优化过程中动态确定。
- **RSFFA（Algorithm 1，L168-208）**：① 记录最小容量 C_min，按初始分配算出各路时延并**按时延升序排序**；② 顺序分配数据（每路取 min(C_r, D_rem)）；③ **碎片优化循环**：找出时延最长/最短的两条路，把 transfer = min(min_vol, size) 的数据从最长搬到最短，若最大最小延迟差 < size 则 size 按衰减因子 α 缩小，直到"最大最小延迟差 ≤ 0.1"或迭代次数耗尽；④ **增路判据**：若新的 T_M' 比旧的差、或已用满 N 条路就停，否则加一条路重跑（L203-207）。
- **复杂度**：O(N log N + T·N)，空间 O(N)（L218）。
- **部署设想**（L222）：作为**星上增强模块**嵌入现有路由协议，输入是 TLE 推出的接触计划与当前网络资源状态。
- **理论性质**：因为 T_M = max_r T_r，最终时延由最慢路径决定；理想情况（各路时延相等）下最终时延等于各路时延的平均值，算法通过碎片调度让最大值逼近这个理想值（L216）。

**4. 它声称的效果**
- **迭代曲线**（Fig.2，L266-268）：前若干次迭代把大量数据从最长时延路搬走、总时延快速下降，之后趋于稳定，末段只做小规模搬移。
- **路径数的影响**（Fig.3，L272）：500 MB 数据，路径数 2→11：**2 条 200.01 s；3 条 133.41 s（降约 33%）；4 条 127.06 s；5–8 条降幅放缓；9 条骤降到 53.80 s；10 条 46.27 s；11 条 44.23 s**。边际收益递减。
- **端到端时延 vs 数据量**（Fig.4，L286-290）：**100 MB 时 RSFFA 23.68 s，MPJOL 235.48 s，PPO-CSO MR 236.81 s，RMA 77.66 s**；**1000 MB 时 RSFFA 145.26 s，MPJOL 260.22 s，PPO-CSO MR 306.41 s，RMA 349.35 s**；500 MB 时 RSFFA 79.95 s vs MPJOL 245.92 s。RMA 在 500→1000 MB 之间从 292.90 s 涨到 349.35 s。
- **路径利用率**（Fig.5，L304-306）：RSFFA 从 100 MB 的 **0.094406** 升到 1000 MB 的 **0.56288**；PPO-CSO MR 在 1000 MB 为 0.369849；RMA 从 0.0316729 升到 0.2807291。
- **负载均衡度（Jain 公平指数）**（Fig.6，L312-319）：RSFFA 0.36（100 MB）→ **0.66**（1000 MB）；MPJOL 0.57→0.64；PPO-CSO MR 0.34→0.62；RMA 0.084→0.23。
- **时延方差**（Fig.7，L325-331）：RSFFA 从 **1.62** 缓升到 **18.62**；MPJOL 75.23→68.01（一直很高）；PPO-CSO MR 300 MB 时 76.44 → 1000 MB 时 84.40；**RMA 从 100 MB 的 2.35 暴涨到 1000 MB 的 101.97**。
- 作者对最后一条的解释（L333）：数据量增大后低时延路径容量逼近上限，必须引入更高时延的路径来分担，因此方差会略升——**这是全文少数几处诚实的机制解释**。

**5. 它的实验条件**
**仿真器**：DtnSim（DTN 专用网络仿真器，L248）。
**拓扑**：**Iridium-NEXT，66 颗活跃卫星**，高度约 780 km，周期 102 min，6 个近极轨道面、每面 11 颗、相邻面间隔 60°（L250）。
**参数（Table 3，L260）**：**时间片 6 min，一个轨道周期分 W=17 片**；算法迭代 100 次；**数据量 D ∈ [100,1000] MB**；衰减因子 α=0.9；初始搬移量 10 MB；**星间速率 r=25 Mbps，星地速率 r_g=20 Mbps**。
**每个时间片内接触计划视为静态**，接触计划由预测卫星位置/距离/可见性预生成后喂给仿真器（L252）。
**负载维度**：**变化的量是"数据总量 D"（100→1000 MB）**，不是到达率；Fig.3 另扫路径数 2→11。
**基线**：RMA（随机多路径）、MPJOL [27]（KSP + 按路径权重比例分配）、PPO-CSO MR [36]（DRL 多路径协同路由）。**明确排除了单路径 CGR 作为对照**，理由是"单路径 CGR 与多路径负载均衡策略设计目标不同，直接比较不能反映本方法的价值"（L254），作者改为在 DtnSim 里把 CGR 与 Yen 算法结合生成多路径作为共同底座。
**训练与评估**：无训练（无学习成分），全部为同一套仿真。

**6. 它自己承认的局限**（逐字）
- L344："First, **the computational complexity of the algorithm is relatively high**, particularly in large-scale satellite networks where increasing numbers of routes and nodes lead to significant computational overhead. Second, the study **primarily focuses on validating the strategy in simulation environments**. Future research should incorporate more realistic network scenarios... Moreover, **enhancing the algorithm's robustness and adaptability in dynamically changing network environments remains an open challenge.**"
- L346（未来工作中最重要的一条自陈）："**Integrating buffer-aware mechanisms is a critical next step for practical deployment.** In real LEO networks with multiple data flows, **incorporating buffer status at intermediate satellites into routing decisions will be essential to effectively manage congestion** and optimize resource utilization. Exploring lightweight buffer state information and dynamic congestion control strategies is therefore paramount."
即作者自认：**当前模型不含中间节点缓冲状态，也就没有真正的拥塞/排队建模**；此外还要处理计算复杂度、更具动态性的网络环境与真实流量模型。

**7. 它没做但看起来能做的地方**（基于内容）
1. **"拥塞"是被反复声称要解决的问题，但模型里根本没有排队**：式 3 的 t_wait 是"等接触窗口开始"的链路可用性等待，**与队列长度无关**。论文却在 L216、L290、L321 多处把结果归因于"避免拥塞""缓解链路拥塞"。作者自己在 L346 承认 buffer-aware 是未来工作——**这意味着全文关于"拥塞"的论断都缺少对应的建模基础**。
2. **负载轴是"数据总量"而不是到达率**：D 从 100 到 1000 MB 是一次性数据量的扫描，没有 λ、没有多流并发、没有流到达过程。**"负载变化"在本篇里等价于"这次要传多少数据"**。
3. **100 MB 时与基线的差距达 10 倍（23.68 s vs 235 s）没有被解释**：如此量级的差距通常提示基线实现或参数配置有问题。论文只做定性归因（"MPJOL 无法绕过中断路径"），没有任何诊断。
4. **Fig.3 与 Fig.4 的数字互相矛盾**：Fig.3 说 500 MB 且 2 条路时 200.01 s，Fig.4 说 500 MB 时 RSFFA 为 79.95 s——除非路径数不同，但论文没有交代，也没给出 Fig.4 的路径数。
5. **容量式 4 假设链路在接触窗口内对该流独占**，多流并发下不成立；论文没有讨论共享。
6. **没有重复实验/置信区间**：100 次是算法内部迭代次数，不是 100 次独立仿真。
7. **只考虑单一"用户→地面站"的传输**（L85），没有多源多宿的竞争。
8. **没有做参数敏感性**（α、初始搬移量、时间片长度都是单点设定）。

**8. 和同批其他篇的关系**
它代表本批里 **DTN/接触图这条独立支线**——与"RL 路由"支线（39NJWBI7、3MRQRWHU）在方法论上几乎不相交：**不用学习、不用 Q 值、不做在线决策**，而是"预生成接触计划 + 组合优化 + 贪心碎片迁移"。它的对照基线里有一个 DRL 方法（PPO-CSO MR [36]），也就是说它**把 RL 方法当作被击败的对象**——这与 39NJWBI7 把启发式当作被击败对象的方向正好相反。参考文献（L360-435）覆盖 CGR/DTN 传统（[6][7][10][11][29][31]）、LEO 负载均衡路由（[17]-[20][28]）、多路径（[22]-[27]）与 DRL 拥塞控制（[33][34][36]），**不引用本批任何其他篇目**。

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**有负载轴、有时延曲线，但"负载"的定义不是到达率，且时延里没有排队项。**
- **可以带走的定性事实**：**多路径碎片化能压住"时延离散度随负载增长"的速度**。Fig.7 给出具体对照：RSFFA 的时延方差从 1.62 涨到 18.62（10 倍数据量），而随机分配（RMA）从 2.35 暴涨到 **101.97**。也就是说，**在负载上升时，不做分配策略时受害最大的不是平均时延而是时延的离散度**——这条与 39NJWBI7 的"平均 vs 尾部"分裂现象是同一类观察，只是指标不同。
- **另一个可用的断言**：路径数增加对时延的边际收益递减（Fig.3），并且出现**非线性骤降**（2→3 降 33%；8→9 从百余秒级骤降到 53.80 s）——说明"多路径"的收益不是平滑的，存在需要跨过的门限。
- **不能带来的**：它**没有到达率 λ**（负载 = 一次性数据量 D）；它的"等待时延"是**接触窗口等待而非排队等待**（式 3），所以**它测到的时延增长不包含拥塞排队成分**——尽管论文反复用"拥塞"来解释结果。作者自己在 L346 承认模型缺 buffer 状态。

**10. 一句话评价**
**把 DTN 接触图路由与 Bundle 碎片化拼成一个"多路径 + 按容量分数据"的启发式调度器（RSFFA）**，在方法谱系上属于 **CGR/DTN 组合优化支线**而非学习路线，并且明确把 DRL 路由当作对照击败；它最大的问题不在于方法而在于**模型**：**"等待时延"被定义成等链路可用而非排队**，因此它一边声称解决拥塞、一边没有任何拥塞模型——它对"负载变化下到达率/时延"能提供的是"多路径可抑制负载上升时时延离散度的膨胀"这一条定性事实，**给不出任何到达率意义下的排队时延证据**。

## 2W8BJ7ME — A Load Balancing Routing Strategy for LEO Satellite Network

> 覆盖：逐字读完第 1–324 行（正文 1–278，参考文献 280–306，作者简介 308–324）。全文 324 行。

**1. 一句话**
两个互补的**纯启发式**组件：**SIDA**（改 Dijkstra 的遍历顺序 + 给用过的节点加权重，让高度对称的网格拓扑不再反复压同一条链路）用来算快照路由；**SSLB**（分布式、无中心）在拥塞发生时把拥塞节点的流量按剩余带宽算出的比例**分流给邻居**。**不涉及任何学习，也完全没有时延模型**——全文指标只有"拥塞链路条数"和"剩余带宽标准差"。

**2. 问题设定**
LEO 网络有两个结构性麻烦（L22-24）：① **高纬度区天线角度偏移导致异轨链路断开**，拓扑周期性频繁变化；② **陆地/海洋面积比例不均、用户分布与需求不均，导致流量分布不均**。作者指出快照序列算法（把轨道周期切成时片、每片拓扑视为静态、由中心节点离线算好全网路由再上传）能解决①，**但解决不了②**——流量不均会造成链路拥塞，而且会出现"有些链路很忙、另一些链路空闲"的局面（L26）。它要在**尽量少信令、尽量低算力**（星上算力有限、通信代价高，L46）的前提下做负载均衡。

**3. 方法骨架**
- **网络模型（第 III 节）**：N = n×m 颗星（n 条轨道、每轨 m 颗），逻辑位置记作 (n,m)；地面按位置与星座划成矩形**流量小区**，每小区任一时刻绑定一颗星；每星 4 条 ISL（2 同轨 + 2 异轨）。高纬区异轨链路断开；第 1 条升轨与最后一条降轨卫星之间**无 ISL（反向缝隙）**（L52）。节点编号 i 与轨道/轨内序号 (k,r) 的换算见式 1（k=⌊i/m⌋，r=i mod m）。
- **拥塞定义**：链路 (i,j) 的剩余带宽 E，阈值 Q_threshold；**E < Q_threshold 即判定为拥塞**（L63）。**注意：这是一个二值阈值判据，背后没有队列、没有到达率、没有服务率。**
- **SIDA（第 IV.A 节）**：标准 Dijkstra 的第二次遍历按节点编号**从小到大**进行，在高对称规则网格里会导致"新路径叠加在原最短路径上、部分链路被反复使用"（L72）。SIDA 的改法是：**当目的节点编号大于源节点时用正序遍历，小于时用逆序遍历**（L74），使全网约一半节点正序、一半逆序；另外**若某节点已被某条路径用过，就把源到该节点的权重加大**，使后续算路避开它、且**不增加跳数**（L76）。作者用 9×9 网格示例：Dijkstra 下左上区域被用得明显多于右下，SIDA 下全网较均匀（L80）。
- **SSLB（第 IV.B 节）**：分布式策略，基于 SIDA 算出的路径。
  - **适用场景**（L94）：低纬区拓扑是高度对称均匀网格，源宿之间存在多条**等价最短路**，分流到邻居后**最小跳数最多增加 2**；高纬区异轨链路断开、"几乎没有等价多路径"，**SSLB 在那里基本用不了**（逐字："If there is congestion in the high latitude area, it must be the link in the same orbit. At this time, there is almost no equivalent multipath route. Therefore, SSLB will play a better role at low latitudes."）。
  - **下一跳选择（Algorithm 1，L100-126）**：按拥塞链路是同轨还是异轨、以及目的节点相对拥塞节点的方位，从 1–2 个可接受分流的邻居中选；两个邻居跳数相同时**只选一个**以免分流量过大；两个都可用时**选剩余带宽更大的**。明确排除会使跳数增加 2 的那类邻居（L128）。
  - **分流量计算（式 2-5）**：设拥塞链路两端流量 F_x < F_y。优先分流小流量节点 X：α = (E_XP − Q_threshold)/F_x（式 2），X 继续按原路发的流量为 (1−α)F_x（式 3）；若 E_XY 仍低于阈值，再让 Y 参与：β = (E_YQ − Q_threshold)/F_y（式 4），Y 走原路的流量为 (1−β)F_y（式 5）。
  - **复杂度**（L168-170）：计算复杂度 O(I)；信令上**拥塞节点只需一次信令交互**就能确定可接受分流的邻居。

**4. 它声称的效果**
- **SIDA vs Dijkstra，拥塞链路条数**（Fig.4，L222-227）：在 **[20]–[30] 组流量**时两者都出现振荡、幅度相近、**没有显著差别**；在 **[31]–[64] 组流量**时，Dijkstra 的拥塞链路条数**振荡上升**，而 SIDA **平稳单调上升**，且 Dijkstra 逐渐多于 SIDA，差距随流量增加而拉大。
- **SIDA vs Dijkstra，剩余带宽标准差**（Fig.10，L259）：Dijkstra 的标准差**始终高于** SIDA，且随流量增加 SIDA 上升更慢 → 链路利用率更高。
- **SSLB vs LCRA，拥塞链路条数**（Fig.5，L235）：SSLB 的平均链路拥塞**远小于** LCRA。
- **分流的效果**（Fig.6-9，L245-247）：在 [20]–[59] 组流量、均分四组下，用 C（总拥塞链路）、D（低纬拥塞链路）、E（分流后被解决的拥塞链路）、F（分流后新增拥塞）、G（分流后低纬拥塞）五个量衡量。结果满足 F < C、G < D：**不仅低纬拥塞被解决，部分高纬拥塞也随之解决**，全网拥塞链路数整体下降。
- **一条诚实的负面结果**（Fig.11-12，L272）：六个流量下，**SSLB 的剩余带宽标准差几乎总是大于 SIDA**，且两者差距随流量增加而扩大；只有在流量值较小时 LCRA 的标准差才远大于 SSLB。**也就是说，分流确实降低了拥塞链路条数，但代价是链路负载分布变得更不均匀。**

**5. 它的实验条件**
**星座（第 V.A 节）**：**LEO54**——6 条轨道面、**54 颗卫星**、每轨 9 颗；每星 4 条 ISL；**纬度高于 60° 时异轨链路断开**；极轨、极点无角度偏转。快照设定：节点 1 位于东半球 90°N；同轨相邻卫星纬度差 **40°**；相邻轨链路的纬度相位差 **±20°**（L189-195）。
**关键限制**：**只用了一个时间片的拓扑快照**来验证（L187 逐字："this section can use the topological snapshot of one time slice to verify the feasibility of the algorithm"）——**没有跨时片评估**，尽管全篇建立在快照序列框架上。
**流量模型（L197-202）**：按"10% 的大文件类流量占 80% 带宽、其余对时延敏感但占带宽小"的假设，**用 Gamma 分布生成流量分布**；每次实验假设 N 个用户同时发送流量；源/宿节点随机生成；不同用户路径不同。**负载轴 = 流量流数（[20]–[64] 组）**。
**指标**：拥塞链路平均条数、链路剩余带宽的标准差。**没有时延、没有吞吐、没有丢包率、没有任何端到端指标。**
**基线**：Dijkstra（对照 SIDA）、LCRA（[10]，对照 SSLB）。**没有任何 RL/DRL 基线**。

**6. 它自己承认的局限**（逐字）
**未见自述局限章节。** 第 VI 节结论（L274-278）只有正面总结，**没有 limitations，也没有 future work**。全文唯一接近能力边界的一句在 L94，但那是**对适用范围的描述而非自认不足**："**SSLB will play a better role at low latitudes.**"
（依据：逐行读完 L1-278 全文，第四节、第五节、第六节均无 limitations 小节。）

**7. 它没做但看起来能做的地方**（基于内容）
1. **完全没有时延模型**：全文的"拥塞"是"剩余带宽 < 阈值"这样一个二值标志（L63），**没有排队、没有到达率、没有服务率，因而也没有任何把负载换算成时延的通道**。作者反复说分流能"及时消除拥塞"，但**从未验证拥塞减少是否带来时延下降**——这是最大的缺口，也是最容易补的一步。
2. **只验证了一个时间片**（L187），却通篇宣称服务于快照序列框架；跨时片（尤其是拓扑切换时路由表切换）的性能从未测过。
3. **SSLB 的代价被自己测出来却没被处理**：L272 明确显示 SSLB 的剩余带宽标准差大于 SIDA 且差距随负载扩大——**"分流把拥塞变成了更不均匀的负载"**，作者只陈述不分析，也没有给出"在什么负载下分流得不偿失"的判据。
4. **式 2/4 没有做非负截断**：当 E_XP ≤ Q_threshold 时 α ≤ 0，字面意思变成"往拥堵链路里倒流量"，论文未讨论这种情况。
5. **SIDA 的"给用过的节点加权重"没有给出具体增量**（L76 只说 "the weight ... should be increased"），属于不可复现的实现细节。
6. **Q_threshold 是单点设定**，无敏感性分析；而阈值直接决定"什么算拥塞"，是全篇结论的第一驱动量。
7. **高纬区被显式放弃**（L94），但高纬正是 LEO 拓扑退化最严重的地方——这个空白没有被任何后续方案填补。
8. **没有与 RL/学习类路由对比**，也没有与 ELB [6]（它自己在相关工作里重点介绍的经典方法）做数值对比。

**8. 和同批其他篇的关系**
属于 **LEO 负载均衡路由的"经典启发式"支线**，血统清楚：相关工作（L38-46）把 **ELB [6]**（拥塞节点通知邻居另找路）、**LCRA [10]**（低复杂度网格选下一跳，本文的参照系）、**agent-based 负载均衡 [7][8]**、**按需路由 [9]** 依次评述，并明确说"这些方法要么需要频繁信令、要么需要密集计算，星上难以实现"（L44），本文要的是**轻量**。这与 39NJWBI7（PRIMAL，1584 星、事件驱动 MARL + CVaR）和 3MRQRWHU（Q-learning 多 QoS）处在同一问题域但方法代差明显；对照关系是：**它把"拥塞"当二值现象处理，而 39NJWBI7 把排队时延当连续量并约束其 CVaR**。参考文献（L280-306）**不引用本批任何其他篇目**，且引文最新到 2018 年。

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**有负载轴，但没有时延——贡献的是"负载 → 拥塞"而非"负载 → 时延"。**
- **可带走的第一条事实**：在负载上升时，**拓扑盲的最短路路由的拥塞链路条数是振荡且加速上升的，而"使用感知"的变体是平稳上升的**（Fig.4，L222/L227）。这在低负载段（[20]–[30] 组）**两种算法没有显著差异**——说明使用感知带来的收益只在负载越过某个门限后才显现。这是一条有门限结构的负载-拥塞事实。
- **可带走的第二条事实（且是负面结论）**：**"把拥塞节点的流量分给邻居"并不免费**——它降低拥塞链路条数（F < C, G < D），但**使剩余带宽的标准差变大**（SSLB > SIDA，且差距随负载扩大，L272）。**任何以"拥塞缓解"为卖点的分流/绕行机制，都必须回答"缓解的是拥塞数还是负载均衡度"这个问题。**
- **不能带来的**：它**没有到达率**（负载是"同时发送的流量流组数"）、**没有队列**、**没有任何时延数字**。因此它**无法支持"到达率升高 → 时延升高"的任何论断**。若引用，只能引"负载门限 + 分流代价"这两条结构性事实。

**10. 一句话评价**
**一篇典型的"经典启发式 + 阈值拥塞判据"的 LEO 负载均衡工作**（SIDA 改遍历顺序、SSLB 按剩余带宽比例分流），在方法谱系上属于 ELB/LCRA 这一代的后续改良，**完全不涉及学习**；它的价值在于给出两条可复用的结构性观察——**使用感知路由的收益存在负载门限**、**分流会以负载均衡度为代价换取拥塞条数下降**——但由于**全篇没有任何时延模型、且只验证了一个时间片**，它对"负载变化下的到达率/时延"**只能提供拥塞侧的旁证，提供不了任何时延证据**。

## 35T2JJRJ — Attention Is All You Need

> 覆盖：逐字读完第 1–324 行（正文 1–233，参考文献 235–315，注意力可视化附录 317–324）。全文 324 行。
> **重要：本篇不是 LEO 论文**，也不是卫星/网络领域论文，而是序列建模的方法论奠基作（Transformer）。批次里出现它说明语料含方法学地基条目；以下按规范照读照写，不做领域关联的硬扯。

**1. 一句话**
提出 **Transformer**——第一个**完全靠注意力机制**、彻底去掉循环与卷积的序列转换模型：编码器/解码器各 6 层，每层是"多头自注意力 + 逐位置前馈"，配上正弦位置编码；它把"序列建模必须递归"这个假设拆掉，换来训练可并行，代价是注意力对序列长度呈二次复杂度。

**2. 问题设定**
要解决的是**循环模型的内在串行性**（第 1 节）。RNN/LSTM/GRU 沿符号位置逐步计算：h_t 是 h_{t−1} 与位置 t 输入的函数，这种串行本质**使得训练样本内部的并行化不可能**，而序列一长就致命——显存限制了跨样本批处理（L29 逐字："This inherently sequential nature precludes parallelization within training examples, which becomes critical at longer sequence lengths, as memory constraints limit batching across examples"）。既有的因式分解技巧 [21] 与条件计算 [32] 只是缓解，"**串行计算这一根本约束依然存在**"（L29）。同时，注意力机制虽然已成标配，但"除了少数例外 [27]，都是与循环网络结合使用"（L31）。

**3. 方法骨架**
- **整体**（第 3 节）：标准 encoder-decoder，编码器把 (x_1,…,x_n) 映射为 z=(z_1,…,z_n)，解码器自回归地逐个生成 (y_1,…,y_m)。
- **Encoder/Decoder 栈（第 3.1 节）**：各 **N=6 层**。编码器每层两个子层（多头自注意力 + 逐位置全连接）；解码器每层三个子层（多插一个对编码器输出的多头注意力）。每个子层外包 **残差连接 + LayerNorm**，即 LayerNorm(x + Sublayer(x))；所有子层与嵌入层输出维度 d_model=512。**解码器自注意力做掩码**（把非法连接置 −∞），保证位置 i 只能依赖 <i 的输出。
- **缩放点积注意力（第 3.2.1 节）**：Attention(Q,K,V) = softmax(QKᵀ/√d_k)·V（**式 1**）。缩放的理由：d_k 大时点积幅度大，会把 softmax 推入梯度极小的区域（L81）。
- **多头注意力（第 3.2.2 节）**：把 Q/K/V 用 h 组不同线性投影投到 d_k, d_k, d_v，并行做注意力后拼接再投影一次：MultiHead = Concat(head_1,…,head_h)W^O，head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)。本文取 **h=8，d_k=d_v=d_model/h=64**；因为每头维度降低，总计算量与全维度单头相当。动机是"单头注意力做平均会抑制多子空间的信息"（L87）。
- **三种注意力用法（第 3.2.3 节）**：编码器-解码器注意力（Q 来自解码器、K/V 来自编码器）；编码器自注意力；解码器自注意力（带掩码）。
- **逐位置前馈（第 3.3 节）**：FFN(x) = max(0, xW_1+b_1)W_2+b_2（**式 2**），d_ff=2048；等价于两个 kernel size 为 1 的卷积。
- **嵌入与 softmax（第 3.4 节）**：输入/输出嵌入与 pre-softmax 线性层**共享同一个权重矩阵**，嵌入权重乘以 √d_model。
- **位置编码（第 3.5 节）**：因为没有循环也没有卷积，必须显式注入位置信息。用不同频率的正余弦：PE(pos,2i)=sin(pos/10000^(2i/d_model))、PE(pos,2i+1)=cos(·)。选它的理由是"对任意固定偏移 k，PE(pos+k) 可以表示为 PE(pos) 的线性函数"，便于学相对位置，且**可能外推到比训练时更长的序列**（L136）。
- **为什么用自注意力（第 4 节，Table 1）**：三条判据——每层计算复杂度、最少串行操作数、任意两位置间的最大路径长度。Table 1：自注意力 O(n²·d) / 串行 O(1) / 路径 O(1)；循环 O(n·d²) / 串行 O(n) / 路径 O(n)；卷积 O(k·n·d²) / 串行 O(1) / 路径 O(log_k n)；受限自注意力 O(r·n·d) / 串行 O(1) / 路径 O(n/r)。（**Table 1 是本文除翻译成绩外信息量最大的一张表**。）

**4. 它声称的效果**
- **WMT 2014 EN-DE**（Table 2，L179）：Transformer(base) **27.3** BLEU，Transformer(big) **28.4**；此前最强是 ConvS2S Ensemble 26.36 与 GNMT+RL Ensemble 26.30。作者称 big 模型"**比此前报告的最好模型（含集成）高出 2.0 BLEU 以上**"（L189）。
- **WMT 2014 EN-FR**：Table 2 记 Transformer(big) = **41.8**；但正文 L191 写的是"**achieves a BLEU score of 41.0**，outperforming all of the previously published single models，训练成本不到此前 SOTA 的 1/4"。——**同一篇里表格（41.8）与正文（41.0）数字不一致**，需注意引用口径。
- **训练成本**（Table 2）：Transformer base **3.3×10¹⁸** FLOPs（远低于 ConvS2S 的 9.6×10¹⁸、GNMT+RL 的 2.3×10¹⁹）；big 2.3×10¹⁹。
- **训练时长**（第 5.2 节）：8 张 P100；base 每步 0.4 s、共 100 000 步 = **12 小时**；big 每步 1.0 s、共 300 000 步 = **3.5 天**。
- **消融（Table 3，dev=newstest2013）**：base 配置 6 层/512/2048/h=8，PPL 4.92，BLEU 25.8，**65M 参数**，100K 步。
  - (A) 头数：1 → 24.9（比最佳差 0.9 BLEU）；4 → 25.5；16 → 25.8；32 → 25.4（**头太多也掉**）。
  - (B) 减小 d_k 到 16/32 → 25.1/25.4，**掉点**，作者据此猜测"兼容性函数比点积更复杂可能有益"（L206）。
  - (C) 层数 2/4/8 → 23.7/25.3/25.5；d_model 256/1024 → 24.5/26.0（**模型越大越好**）。
  - (D) dropout 0.0 → 26.2；0.2 → 24.6；label smoothing 0.0/0.2 → 25.5/25.3。作者结论是"**dropout 对避免过拟合非常有帮助**"（L206）。
  - (E) **用可学习位置嵌入替代正弦编码 → 25.7，与 base 的 25.8 几乎相同**。
  - big：d_model=1024, d_ff=4096, h=16, P_drop=0.3，300K 步，PPL 4.33，BLEU 26.4，**213M 参数**。
- **成分句法分析（Table 4，WSJ 第 23 节）**：4 层 Transformer，仅 WSJ 训练 F1 **91.3**，半监督 **92.1**；对比 Berkeley-Parser 92.1、Recurrent Neural Network Grammar 93.3（**未能超过 RNN Grammar**，L219 自述"with the exception of the Recurrent Neural Network Grammar"）。**注：MinerU 对该表的行列对齐有错乱（parser 名与 F1 值发生错位），引用具体配对时需回原文核对。**

**5. 它的实验条件**
**数据（第 5.1 节）**：WMT 2014 EN-DE，约 450 万句对，BPE 共享词表约 37 000；WMT 2014 EN-FR，**3600 万句对**，32 000 word-piece 词表。按近似句长组批，每批约 25 000 源 token + 25 000 目标 token。
**优化（第 5.3 节）**：Adam，β_1=0.9, β_2=0.98, ε=10⁻⁹；学习率 lrate = d_model^−0.5 · min(step^−0.5, step·warmup^−1.5)（式 3），**warmup=4000**（线性升后按步数平方根倒数降）。
**正则（第 5.4 节）**：残差 dropout 0.1；标签平滑 ε_ls=0.1（作者自述"**hurts perplexity，但提升准确率与 BLEU**"）。
**推理（第 6.1 节）**：base 取最后 5 个 checkpoint 平均（每 10 分钟存一次），big 取最后 20 个；beam size **4**，长度惩罚 α=0.6；最大输出长度 = 输入长度 + 50。
**句法分析（第 6.3 节）**：4 层、d_model=1024；WSJ 部分约 40K 训练句；半监督用约 17M 句；词表 16K/32K；beam size **21**，α=0.3。
**训练与评估**：同一套模型规格；消融只在 dev 集（newstest2013）上做，测试集成绩只用最终配置。**硬件是 8×P100。**

**6. 它自己承认的局限**（逐字）
**未见独立的 Limitations 章节。** 全文零散的自我限定有三处：
- **注意力平均导致分辨率下降**（L37）："...albeit at **the cost of reduced effective resolution due to averaging attention-weighted positions**, an effect we counteract with Multi-Head Attention as described in section 3.2."
- **长序列需要受限注意力，本文未做**（L146）："To improve computational performance for tasks involving very long sequences, self-attention could be restricted to considering only a neighborhood of size r... This would increase the maximum path length to O(n/r). **We plan to investigate this approach further in future work.**"
- **生成仍是串行的、且只验证了文本模态**（L229）："We plan to extend the Transformer to problems involving input and output modalities other than text and to investigate local, restricted attention mechanisms to efficiently handle large inputs and outputs such as images, audio and video. **Making generation less sequential is another research goals of ours.**"
- **句法任务未超过 RNN Grammar**（L219）："yielding better results than all previously reported models **with the exception of the Recurrent Neural Network Grammar [8]**."

**7. 它没做但看起来能做的地方**（基于内容）
1. **O(n²) 的注意力墙没有被处理**：Table 1 明确写出自注意力每层 O(n²·d)，受限版本能降到 O(r·n·d)，但作者把它推到 future work（L146/L229）。**这是本文留给后续工作最大、最明确的一个口子**（后来的 Longformer/Sparse Transformer 一类工作正是在填这个坑）。
2. **解码仍是自回归、逐步生成**（L229 自述"making generation less sequential"仍是目标）——**训练可并行了，推理没有**。
3. **位置编码的选择没有被充分论证**：正弦编码 vs 可学习嵌入在 dev 上几乎无差别（25.7 vs 25.8），作者仍选正弦，理由是"**可能**外推到更长序列"（L136），**但这个外推能力从未被实验验证**。
4. **多头数存在最优点（16）而非单调**（Table 3 (A)：1→24.9，16→25.8，32→25.4），但**为什么 16 最优没有任何解释**。
5. **注意力可解释性只有附录里的两张图**（L319/L322），属于**轶事级证据**，没有定量分析。
6. **只在两个翻译任务 + 一个句法任务上验证**，跨任务的广度有限。
7. **dropout 0.0 在 dev 上 BLEU 反而最高（26.2）**（Table 3 (D)）这条反直觉结果没有被讨论。

**8. 和同批其他篇的关系**
**它不是同批任何 LEO 论文的同类项，而是它们所依赖的方法族的上游**。具体而言：本批 2FBBURX7 用的 **GATv2**（其参考文献 [66]）正是把"注意力"从序列搬到图上的产物，其思想源头可追到本篇（虽然 2FBBURX7 直接引的是 GAT [24]/[65] 而非本篇）；39NJWBI7 的 actor/critic 用两层 MLP（未用注意力），**不依赖本篇**；4QG5VYHQ 是排队论解析，与深度模型无关。参考文献（L237-315）**全部是 NLP/深度学习文献**（Bahdanau 注意力、LSTM、ByteNet、ConvS2S、LayerNorm、Adam、dropout、label smoothing），**没有任何网络/通信/卫星文献**。因此：**本篇在本次选题的语境里是"工具谱系的祖先"，不是"问题域的同侪"**。

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**没有直接贡献**——它既没有到达率、没有队列、没有网络时延，实验对象是自然语言句子。**不硬扯。**
唯一可迁移的是一条**"决策机制自身开销随规模增长"的标度律**：**Table 1（L122）** 指出——如果需要"关注"的实体数量为 n，则自注意力每层代价是 O(n²·d)、受限自注意力是 O(r·n·d)、循环是 O(n·d²)。**也就是说：一个基于注意力的策略网络，其推理开销对"被关注的实体数"是二次的。** 如果把 n 理解为"卫星数 / 候选路径数 / 并发流数"（在负载升高时这些量会一起变大），那么**"负载升高 → 策略网络推理开销二次上升"** 是一件可以直接从本篇表格里读出的事实——这与 S85KQ4FC 关心的"决策资源饱和"是同一类担忧，但**本篇只给了复杂度表达式，没有任何网络场景下的实测**。任何把 Transformer 用进 LEO 路由的工作，都应先回答"n² 这一项在星上算力下是否可接受"，而本篇不提供这个答案。

**10. 一句话评价**
**这是本批语料里唯一的一篇方法论地基论文**：它把循环从序列建模里去掉、把并行度和长程依赖路径同时改善，代价是 O(n²) 的注意力与仍然串行的生成——在方法谱系上它处在**所有注意力系模型的共同祖先位置**，与 LEO 路由选题的关系是"工具的上游"而非"问题的同侪"；对"负载变化下到达率/时延"**无任何直接贡献**，唯一可迁移的是"注意力机制开销随被关注实体数二次增长"这条**标度律**。

## 42E4NAQU — Queue-Aware and Resilient Routing in LEO Satellite Networks Using Multi-Agent Reinforcement Learning

> 覆盖：逐字读完第 1–197 行（正文 1–164，参考文献 166–197）。全文 197 行（短文/工作坊级篇幅）。

**1. 一句话**
把**队列长度**塞进 DDQN 的状态与奖励，让每颗卫星作为独立 agent 用局部（自己 + 四个邻居的）队列信息选下一跳；另外造了一个"韧性分数"（outage probability 与队列状态的加权组合）来提前避开不可靠链路。**最诚实的结论是：它的平均时延（49.31 ms）打不过队列盲的 Dijkstra（38.54 ms）**——它卖的是决策开销低（O(1) 推理）而不是时延更低。

**2. 问题设定**
LEO 做全球互联网接入，但拓扑剧变、流量时变、链路易失效（L13）。作者点名既有工作的缺口（L17/L27）：**大多数 DRL 路由只盯着时延最小化，不显式考虑网络队列状态**（逐字 L17："most focus primarily on latency minimization without explicitly considering network queue conditions, which play a critical role in such environments, **especially under varying traffic loads**"）；传统路由假设链路度量静态、不考虑队列积压（L7）；韧性方面多数方法是"故障后恢复"而非"提前规避"；MA-DRL 类工作缺少与经典/优化基线的充分对照（L27）。

**3. 方法骨架**
- **星座与链路（第 III 节）**：O 个轨道面、每面 N_o = N/O 颗，圆轨、偏心率可忽略（e ≈ 0.00001）；**每星 5 副天线**——4 副 ISL（2 条同轨 + 2 条异轨）+ 1 副星地；地面网关 G 个，每个网关只保留一条到**可见范围内最近卫星**的星地链路（L31）。
- **速率模型**：ISL 速率 R(i,j) = log₂(1 + P·d^−α·|h|²·G_i·G_j / (qσ²))（式 1），q = 4π/λ；星地上下行 SNR 用 Nakagami-m 信道（式 2/3/4）。
- **每跳时延（式 5，本文最核心的一段）**：
  D(i,j) = ‖ij‖/c + B/R(i,j) + t_q(i) —— 传播 + 传输 + 排队三项。
  其中**排队时延 t_q(i) = q_i · B / R(i,·)**——q_i 是节点 i 的队列长度，B 是包大小，R(i,·) 是一个**未指明的代表性速率**。作者自述理由："**队列中在前的包可能去往不同链路、速率各不相同**"（L67 逐字："Since packets ahead in the queue may be destined for different links with varying transmission rates R(i,·), the queueing delay can be approximated as t_q(i) = q_i · B / R(i,·)"）。**这是一个明确的粗近似：排队时延只用队列长度乘一个代表性包传输时间，不区分各包的实际出边。**
- **中断概率与韧性分数（第 III.C 节）**：单跳 outage（式 8）、全网路径 outage（式 7）与总计 P_out^all（式 9）；韧性分数 R^all = ω₁(1 − P_out^all) + ω₂ · max_{i≠j∈N} ( max(1−q_i, 1−q_j) · S_(i,j) )（**式 10**）。注意第二项**直接把队列长度 q_i 当作 [0,1] 内的量去算 1−q_i**——论文没交代 q 如何归一化。**式 11 在 MD 里是空行（L107），内容缺失。**
- **目标函数（第 III.D 节）**：**式 12 在 MD 中几乎全是空行与乱码（L114），读不出完整式子。没读懂：式 12。** 正文只有一句话说明目标：最小化时延、最小化网络不确定性，"optimize compute and offloading energy while also considering communication overhead"（L111）。
- **MDP（第 IV 节）**：**状态**＝当前卫星坐标 + 4 个邻居卫星坐标 + 每个邻居的队列水平 + 包目的地坐标（L125）；再额外加 4 维"四条链路各自的韧性分数（0–1）"（L131）。**动作**＝选四条方向之一（上/下/左/右）作为下一跳（L127）。**奖励**＝四项组合：①当前卫星转发前的排队时延；②该动作带来的到目的地距离缩减；③访问已走过节点的惩罚（防环）；④所选路径的韧性分数（L127/L131）。
- **算法**：**DDQN**（Q 网络 + 周期性同步的目标网 + 经验回放）；训练策略是**先在中心训练一个全局 Q 网络**（捕捉全星座流量动态），**收敛后下发到每颗星**做本地决策，**再加入在线学习**用本地观测持续更新（L129）。
- **流量模型（L123）**：两种生成模式——**均匀**（每个地面终端产生等量数据）与**人口分布**（按各终端连接的用户数成比例）；同一终端内部的通信不经过星座。**这两种模式制造"背景负载"**。

**4. 它声称的效果**
- **时延（Fig.1，L145）**：**MA-DRL 平均 49.31 ms；Dijkstra 38.54 ms；SARSA 59.28 ms**。关键实验设定：**为"公平比较并隔离时延性能"，把队列容量设成 1 Gb/s，"有效防止了队列溢出，让 Dijkstra 在近乎理想条件下运行"**（L145 逐字："To ensure a fair comparison and isolate latency performance, the queue capacity in the simulation is set to 1 Gb/s, effectively preventing queue overflow and allowing Dijkstra's algorithm to operate under near-ideal conditions"）。**即：这篇论文的核心指标对比是在"队列不溢出"的环境下做的，而它的卖点恰恰是队列感知。**
- **决策开销（Fig.2，L147）**：Dijkstra 必须反复重算全局路由并下发路由表，开销随重算频率上升；SARSA 与 MA-DRL 是每星前向推理。摘要说"**约 50% of Dijkstra at a 5 s recalculation interval**"（L7）。作者补充：**当 Dijkstra 的重算间隔拉长到 10 s 以上时，它的决策成本反而低于 MA-DRL 与 SARSA，"但这会带来其他不希望的副作用"**（L147，副作用未具体展开）。
- **路径变化（Fig.3，L155）**：重算频率越低，Dijkstra 的路径变化百分比越大——省了计算却牺牲最优性（原最优路径因拓扑变化失效），**时延反而上升**。
- **韧性（Fig.4，L160）**：在变化的背景流量下，**Dijkstra 的韧性分数最高**——作者归因于它有全局视图；**MA-DRL 与 SARSA 的韧性都更低**，两者互相比接近（同为分布式架构）。
- 与 [8]（Lozano-Cuadra et al.）对比：作者称本方在"数据块丢失"上与 [8] 相当，**两者在各自定义下丢包都可忽略**（L138）。
- **注意：全文没有任何时延-负载曲线**。Fig.4 的横轴是背景流量，但纵轴是韧性分数；时延只有一个数。

**5. 它的实验条件**
**星座（Table I，L134）**：**Starlink shell 1，Walker Delta，72 个轨道面、1584 颗卫星、高度 550 km**；地面终端 **200 个**；地面链路功率预算 10 W、卫星 20 W；**链路带宽 500 MHz**；噪声 −174 dBm/Hz；天线增益 **60 dB**；路径损耗指数 α=2；Nakagami-m 参数 2；频率 30 GHz；**包大小 64 kb**。
**DRL 超参**：**DDQN**；ε-greedy，ε 从 0.99 衰减到 0.1、衰减率 1000；训练 **100 000 次迭代**；**回放池只有 2000**；batch 128；Huber 损失；Adam，**学习率 10⁻⁴**；策略网与目标网都是 **3 层 DNN**（隐层宽度未给出）。
**负载维度**：**背景流量**分两档（均匀 / 人口分布，L123），Fig.4 的横轴是"每个基站平均产生的数据量"；**没有到达率参数、没有泊松过程、没有 λ 扫描**。
**基线**：Dijkstra（以链路时延为边权、**不含队列状态**）与 **SARSA**（用完整星座信息中心化训练后复制到每个节点，作为学习类对照）。**训练与评估同一套仿真**，环境配置"基于 [8] 和 [16]"（L131）。
**范围限制**：只在 Starlink Shell 1 一个壳层上实验。

**6. 它自己承认的局限**（逐字）
**未见独立的 Limitations 章节**，但有四处自陈：
- **时延打不过 Dijkstra**（L145）："While Dijkstra's algorithm shows lower latency under these controlled conditions, it does not explicitly account for queue dynamics."
- **韧性更差**（L160）："In contrast, **the proposed approach exhibits comparatively lower resilience**. Although each agent has access to its local queue state as well as the queue conditions of its neighboring nodes... **it lacks a global view of the network. This limited observability results in slightly reduced resilience performance** for both MA-DRL and SARSA."
- **开销优势有前提，且代价未说明**（L147）："...after increasing the update frequency for Dijkstra to more than 10 s, the cost of decision making becomes less th[a]n of MA-DRL and SARSA, **but this causes other unintended side effects.**"
- **未来工作**（L164）："Future work will investigate advanced learning techniques and **hybrid learning–traditional formulations** for improved efficiency and robustness."

**7. 它没做但看起来能做的地方**（基于内容）
1. **时延对比是在"队列不溢出"（容量 1 Gb/s）的条件下做的**（L145），而队列感知的全部价值本应在**过载/排队显著**时才体现。**把队列容量调回现实值、给出"时延 vs 背景流量"曲线**，是这篇论文自己铺好却没用的一步——最直接、最有价值的缺口。
2. **只有一个时延数**（49.31/38.54/59.28 ms），**没有随负载变化的时延曲线**：Fig.4 明明已经扫了背景流量，却只画了韧性。
3. **排队时延是粗近似**（t_q = q_i·B/R(i,·)，L67）：把整条队列当作都走"某个代表性速率"，掩盖了"队列里各包出边不同、速率各异"这一事实。**按出边分别记账的队列**会显著改变结果——作者自己点出了这个问题却没处理。
4. **式 10 里 1−q_i 的归一化没有定义**；**式 11 与式 12 在原文中缺失/乱码**——目标函数与约束集完全无法核对。
5. **韧性分数是"加权和"而非约束**（ω₁, ω₂ 未给取值），这意味着它又回到"手工调权重"的老路；把它写成受约束优化是现成的下一步——**39NJWBI7 正是这么做的（CVaR 约束）**。
6. **回放池只有 2000**（Table I），对 1584 星场景异常小，论文没有讨论这是否限制了学习。
7. **没有与其他 MA-DRL 路由对照**，基线只有 Dijkstra 与 SARSA。
8. **在线学习的稳定性/收敛性完全没测**（L129 只声明"加入在线学习"，Fig.1-4 无对应曲线）。

**8. 和同批其他篇的关系**
**它与 39NJWBI7（PRIMAL）共享同一个直接祖先**：本文自述方法 "inspired by the framework presented in [8]"（L129），而 **[8] = Lozano-Cuadra, Soret, Leyva-Mayorga et al., Continual deep reinforcement learning for decentralized satellite routing, IEEE TCOM 2025**——这正是 39NJWBI7 用来当基线（MADQN）的同一篇工作（39NJWBI7 的参考文献 [20]）。**两篇是同一棵树上长出的两个分支**：39NJWBI7 走"异步事件驱动 + 分布 RL + CVaR 约束"，本篇走"队列感知 + 韧性分数 + DDQN + 中心训练下发"。它的时延模型（式 5：传播 + 传输 + 排队）与 39NJWBI7 的式 1 逐项同构。参考文献（L168-197）**不引用本批其他篇目**，但 [7][8] 都指向 Soret/Lozano-Cuadra 这一系。

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**有队列、有负载维度，但缺少把两者连起来的那张图。**
- **可带走的第一条（也是最重要的一条）事实**：**在队列被过度配置（1 Gb/s，不溢出）的条件下，队列感知的 MA-DRL 平均时延 49.31 ms 反而高于队列盲的 Dijkstra 38.54 ms**（L145）。这是一条**负面但极有价值**的证据：**"把队列信息放进状态"本身并不自动带来更低的时延**——在负载不足以形成排队的环境里，局部决策的信息劣势（看不到全局）会抵消队列感知的收益。任何声称"队列感知改善时延"的工作都必须交代它的负载区间。
- **第二条**：**决策开销的对照是有条件的**——MA-DRL 的 O(1) 推理相对 Dijkstra 的反复全局重算，优势在重算间隔 ≤5 s 时约为 Dijkstra 的一半；**一旦 Dijkstra 把重算间隔拉到 10 s 以上，它的开销就低于 MA-DRL**（L147），代价是路径失配与时延上升（Fig.3）。**"决策开销"与"负载"之间是通过"拓扑变化速度"而非"到达率"耦合的。**
- **第三条**：**分布式相比集中式会损失韧性**——Dijkstra 全局视图下韧性分数最高，MA-DRL 与 SARSA 都更低（L160）。
- **不能带来的**：它**没有到达率 λ**（背景流量只是"每个基站平均产生多少数据"两档），**没有时延-负载曲线**，且**唯一的时延数字来自队列不溢出的设定**。因此**它不能支持"负载升高 → 排队时延升高 → 队列感知更优"这个链条的任何一环**——那条链在这里断在最后一步。

**10. 一句话评价**
**一篇把"队列长度 + 韧性分数"接入 DDQN 的 LEO 分布式路由短文**，方法上属于 **Lozano-Cuadra 系（[8]）的直接衍生**，与 39NJWBI7 同源而分叉；它最大的价值不在于结论而在于**它诚实地报告了一个负面结果**——在队列不溢出的近理想条件下，队列感知的多智能体路由时延劣于队列盲的 Dijkstra（49.31 vs 38.54 ms），赢的只是决策开销；**它把"时延 vs 负载"这张最该画的图留成了空白**，而这恰好是"负载变化下到达率/时延"这个选题最需要的那块拼图。

## 47J2H748 — Packet Routing in Dynamically Changing Networks: A Reinforcement Learning Approach

> 覆盖：逐字读完第 1–119 行（正文 1–98，参考文献 100–119）。全文 119 行。**这是 Q-routing 的原始论文（Boyan & Littman, 1993）**，是本批所有 RL 路由工作的共同祖先，也是本批（乃至全部语料）对"负载变化下的到达率/时延"给出**最直接、最干净结论**的一篇。

**1. 一句话**
在每个交换节点里嵌一个 Q-learning 模块：节点 $x$ 维护一张 $Q_x(d,y)$ 表，记录"经邻居 $y$ 送包到目的地 $d$ 预计要多久（**含在 $x$ 自己队列里排队的时间**）"，每发一个包就用邻居回报的估计值做一次在线更新。不需要预先知道拓扑和流量模式，也不需要任何中心路由控制。作者把它刻画为**Bellman-Ford 最短路算法的一个变体**：路径松弛步骤是异步在线的，而且**路径长度不用跳数、用总投递时间**来衡量（L37）。

**2. 问题设定**
路由策略要回答的是"当前节点该把包交给哪个邻居，才能尽快送到最终目的地"，但策略的好坏只能用包的**总投递时间**来衡量，而**在包最终到达目的地之前根本没有训练信号**（L23 逐字："there is no 'training signal' for directly evaluating or improving the policy until a packet finally reaches its destination"）。强化学习的价值就在于：**只用局部信息就能更快地更新策略**（L23）。作者要证明的是"**穿过通信网络路由数据包**"是一个天然适合 RL 的实际任务（L15）——当时的 RL 除双陆棋外几乎没什么大规模实际应用。

**3. 方法骨架**
- **Q 值定义（L25）**：$Q_x(d,y)$ ＝ 节点 $x$ 估计的"把去往 $d$ 的包经邻居 $y$ 送出所需的全部时间"，**其中包含包在 $x$ 队列里等待的时间**（"including any time that P would have to spend in node x's queue"）。
- **更新式（L28-37）**：$x$ 把包发给 $y$ 后**立刻**收到 $y$ 的剩余时间估计
  $t=\min_{z\in\mathrm{neighbors\ of\ }y} Q_y(d,z)$
  若包在 $x$ 的队列里呆了 $q$ 个时间单位、在 $x\to y$ 的传输上花了 $s$ 个时间单位，则
  $\Delta Q_x(d,y)=\eta\big(\underbrace{q+s+t}_{\text{新估计}}-\underbrace{Q_x(d,y)}_{\text{旧估计}}\big)$
  学习率 $\eta$ **实验里通常取 0.5**（L37）。
- **与经典算法的关系（L37）**：它是 Bellman-Ford [1,3] 的一个变体，两点不同——(1) 路径松弛**异步且在线**进行；(2) 路径长度**不是跳数而是总投递时间**。
- **表示**：$Q_x(d,y)$ 用**一张大表**存储。作者也试过用**神经网络近似** $Q_x$，好处是能把"本地队列长度、一天中的时段"等多样化系统参数纳入距离估计；但**"these experiments were inconclusive"（结果不确定）**（L39）。
- **拓扑实验范围（L46）**：7-超立方、116 节点 LATA 电话网、**不规则 6×6 网格**；详细结果只报 6×6 网格。
- **探索的两种做法（第 3.2 节）**：
  - **随机探索**：作者指出它在分布式路由里有两个严重问题（L79）——① 网络持续在变，**初始探索期永远不会结束**；② **随机流量对拥塞有极负面的影响**：发往次优方向的包会增加排队时延，从而拖慢所有经过该队列的包，进一步增加时延……而且**因为节点只依据局部信息决策，这种加剧的拥塞实际上改变了学习器试图解决的那个问题本身**。
  - **"full echo" Q-routing（L81）**：不发真包，而是每次决策时向**直接邻居发信息请求**，邻居用**独立信道**回一个数（该邻居对到目的地总时间的当前估计），从而不增加网络拥塞；用这些估计去调整 $Q_x(d,y)$。捷径出现或策略低效时，信息在网络里传播得很快。

**4. 它声称的效果**
- **总量性结论（L46 逐字）**："The result was that **in all cases, Q-routing is able to sustain a higher level of network load than could shortest paths.**"
- **低负载（L48）**：经过一段学习拓扑的初始低效期后，Q-routing **表现与最短路路由器相当**——而后者在低负载下是最优的。
- **高负载（L50）**：最短路路由**不再最优**，因为"**它无视上升的拥塞水平，很快用包淹没整个网络**"；而 Q-routing 学到有效策略。
- **机制证据（Fig.3 策略摘要图，L50）**：最短路策略下，网络**中心的两个节点（标号 570 与 573）出现在大量最短路上**，高负载时成为拥塞点；Q-routing 在高负载下学到的策略**让一部分流量走比必要更长的路（沿网络顶部绕行）以避开中心拥塞**。
- **投递时间 vs 负载（Fig.4，L60）**：每个数据点是**学习稳定后平均包投递时间在 19 次试验上的中位数**。**极低负载时 Q-routing 与最短路几乎一样高效；随着负载上升，最短路策略导致"爆炸式的网络拥塞"，而学习算法持续高效；只有在负载再显著提高之后，Q-routing 才也屈服于拥塞。** —— **这是一条完整的"负载→时延"曲线，且给出了两种策略各自的稳定边界。**
- **动态变化（第 3.1 节，L67-73）**：
  - **拓扑**：手工断开链路，Q-routing 反应迅速、继续高效路由。
  - **流量模式**：让请求模式在"上下半区"与"左右半区"之间周期性振荡，每次切换后只需短暂低效期即可适应。
  - **负载水平（关键）**：**负载升高时 Q-routing 很快调整策略绕开新的瓶颈；但负载再降回去时，适应要慢得多，而且"从未收敛到最优最短路"**（L73 逐字："However, when network traffic levels were then lowered again, adaptation was much slower, and **never converged on the optimal shortest paths**."）
- **"full echo" 的对照（Fig.5，L83）**：**低负载下 full echo 与最短路无法区分**（所有低效都被清除）；**高负载下 full echo 优于最短路，但基本版 Q-routing 更好**。原因是 full echo 在高负载下**策略不断变化，在上方瓶颈与中心瓶颈之间来回振荡**，行为不稳定。
- **全文最锋利的一句（L88 逐字）**："**Ironically, the 'drawback' of the basic Q-routing algorithm—that it does no exploration and no fine-tuning after initially learning a viable policy—actually leads to improved performance under high load conditions. We still know of no single algorithm which performs best under all load conditions.**"

**5. 它的实验条件**
**仿真器**：离散事件仿真器模拟局域网中的包传输，细节见技术报告 [5]（L19）。
**拓扑**：7-超立方、116 节点 LATA 电话网、**不规则 6×6 网格（36 节点）**；详细结果只给 6×6 网格（Fig.1）。
**负载**：**负载水平是被主动扫描的自变量**——Fig.4/Fig.5 的横轴就是"various levels of network load"，并明确给出"最短路爆炸的负载点""Q-routing 也屈服的更高负载点"两个边界（L60）。
**统计口径**：**每个点 = 学习稳定后的平均包投递时间，在 19 次试验上取中位数**（L60）。**这是本批为数不多明确给出重复次数与统计量的论文。**
**学习率**：$\eta$ 通常 0.5（L37）。**训练与评估的关系**：学习是**在线持续**的（"The learning is continual and online"，L17），即"训练"与"运行"是同一过程；评估是在学习稳定后测的。
**流量模式**：含周期性振荡的请求模式（上下半区 ↔ 左右半区，L71）。

**6. 它自己承认的局限**（逐字）
- **仿真不够真实**（L92）："Although **the simulations described here are not fully realistic from the standpoint of actual telecommunication networks**, we believe this paper has shown that adaptive routing is a natural domain for reinforcement learning."
- **神经网络近似未能成功**（L39）："We also tried approximating $Q_x$ with a neural network... However, **the results of these experiments were inconclusive.**"
- **基础 Q-routing 无法发现捷径、无法精调**（L77）："Q-routing **cannot fine-tune a policy to discover shortcuts**, since only the best neighbor's estimate is ever updated."
- **负载下调时不收敛**（L73）："when network traffic levels were then lowered again, adaptation was much slower, and **never converged on the optimal shortest paths**."
- **没有单一算法在所有负载下都最优**（L88）："We still know of no single algorithm which performs best under all load conditions."
- **未来工作**（L94）：用函数近似替代表格表示，以便纳入更多系统变量、跨目的地泛化、减少每节点存储、扩展适用规模。

**7. 它没做但看起来能做的地方**（基于内容）
1. **只用了表格表示，函数近似试了但失败**（L39）：作者在结论里把"换成函数近似"列为最重要的未来方向（L94）——**这正是后来 DRL 路由的全部起点**，而本文只走到"inconclusive"。
2. **探索与拥塞的耦合被指出但未解决**（L79）：作者深刻地指出"随机探索的流量会加剧拥塞，从而**改变学习问题本身**"，但给出的 full echo 方案在高负载下反而不如不探索（L83）。**"如何在有负载的网络里安全探索"这个问题在本文里被明确提出却没有答案。**
3. **负载不对称**（L73）只被陈述、没被解释：为什么降负载时收敛慢而升负载时快？作者只说"This effect is discussed in the next section"（L73），但第 3.2 节讨论的是探索，**并没有真正解释这个不对称**。
4. **没有区分"平均时延"与"时延尾部"**：所有指标都是平均包投递时间（L46/L60），没有方差、没有尾部分位数。而拥塞恰恰是尾部现象。
5. **没有到达率模型**：负载是仿真里的一个总水平参数，未说明是泊松到达还是固定并发数；也没有给出"到达率"与"队列占用"的显式关系。
6. **只有 36 节点（6×6）的详细结果**：7-超立方与 116 节点 LATA 网只给了一句总结（L46），**大网络的结果没有展示**。
7. **没有与当时的非学习型自适应路由（如 delta routing [6]）做数值对比**，而 [6] 正是它引用的对照类工作。

**8. 和同批其他篇的关系**
**它是本批全部 RL 路由论文的共同祖先**，血统关系可以逐条对上：
- **42E4NAQU**（Queue-Aware MA-DRL）的每跳时延 $D(i,j)=\|ij\|/c+B/R(i,j)+t_q(i)$ 与状态里放"邻居队列水平"，正是本文"$Q_x(d,y)$ 含 $x$ 的排队时间"这一设计的多智能体深度学习版；
- **39NJWBI7**（PRIMAL）的式 1 $D^h_{p,ij}=D^P+D^T+D^Q$ 与"reward 里含排队时延"同样直接继承本文的时延分解；本文"$Q$ 值就是到目的地的预计时间"也对应 PRIMAL 的"cost-return"；
- **3MRQRWHU**（多 QoS Q-learning）的状态 $\{\mathrm{delay},\mathrm{loss},\mathrm{band}\}$ 与 Q 表更新（Bellman）几乎是本文 Q-learning 的直接沿用，只是加了优先级权重；
- **2FBBURX7**（多播 AoI 的 A2C）不做逐包路由，关系较远，但同属"RL 解网络优化"这一族。
本文引用的 [1] Bellman、[3] Ford（最短路）、[6] Rudin（delta routing）、[8] Tesauro（TD 学习）说明它的根在 **Bellman-Ford 与 TD 学习**两处；**它不引用任何 LEO/卫星文献（1993 年尚无此领域），也不引用本批其他篇目**。

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**这是本批最直接、最干净、也最可引用的一篇——而且它发表于 1993 年。** 它贡献了五条硬事实：
1. **完整的"负载 → 投递时延"曲线与两条稳定边界**（Fig.4，L60）：最短路策略在某个负载点**爆炸**，Q-routing 把可承受负载推高很多，**但 Q-routing 自己也有一个更高的屈服点**。也就是说：**学习型路由不改变"存在拥塞崩溃点"这件事，只是把它往后推。**
2. **"绕远路避拥塞"在节点级被证据化**（L50，Fig.3）：Q-routing 学到让部分流量走**比必要更长**的路径以避开中心节点 570/573。**这是"最短跳数 ≠ 最低时延"在负载下的最早、最清楚的实验证据。**
3. **负载变化的不可逆/不对称性**（L73）：**升负载适应快，降负载适应慢且永不收敛回最短路。** 这条对任何"负载是时变的需求"的选题都构成一个必须回应的警告——**策略在负载回落后不会自动回到最优**。
4. **探索本身会污染被学习的问题**（L79）：随机探索的包**增加排队时延 → 拖慢所有经过的包 → 进一步增加时延**，而且由于决策是局部的，**这种加剧的拥塞改变了学习器要解决的那个问题**。这是"在线学习 × 负载"耦合的最本质陈述。
5. **不存在全负载域最优的算法**（L88）：探索多的（full echo）低负载好、高负载振荡；探索少的（基础 Q-routing）低负载差一点、高负载最好。**"哪个算法好"这一问在负载变化下没有单一答案。**
**边界**：它的"负载"是一个仿真总水平，**没有显式的到达率 λ、没有泊松过程、没有队列占用率的闭式关系**；所有指标都是**平均投递时间**（无尾部）；详细结果只在 **36 节点**上。但作为**定性规律的来源**，它的权重高于本批任何一篇 LEO 论文。

**10. 一句话评价**
**RL 路由的开山之作**（把 Bellman-Ford 的距离从"跳数"换成"总投递时间"，并在每个节点嵌一个 Q-learning），方法谱系上处在**本批全部学习型路由工作的共同祖先**位置；它对本选题的价值甚至高于任何一篇 LEO 论文——因为它用最少的假设、最清楚的对照（最短路 vs Q-routing vs full-echo，负载扫描 + 19 次试验取中位数）给出了**"负载-时延曲线存在崩溃点""绕远避堵""负载回落不收敛""探索会改变学习问题""无全负载域最优算法"**这五条至今仍然成立的结论。

<!-- END -->
