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

<!-- END -->
