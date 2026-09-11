# 读卡批次 R4

> 读法：逐字通读 VM MinerU MD 全文（含表格、算法、参考文献、作者简介）。行号 = VM MD 行号。
> 我读的顺序即批次顺序；每篇读完立刻写卡。

## BBNQ4EAQ — Temporal Netgrid Model-Based Dynamic Routing in Large-Scale Small Satellite Networks

**1. 一句话**
把"卫星坐标"换成"空间立方格（netgrid）编号"来做拓扑描述，使路由搜索的复杂度只与立方格数有关、与卫星数无关；再配一个周期性 beacon 收集邻居状态，于是按需路由（on-demand）在随机到达流量下也能跑。

**2. 问题设定**
大规模小卫星网络（SSN）里，流量是"随机传输需求 + 随机包生成/到达"（L5、L24）。两类既有方案都不合用（L22）：(a) 计划式路由（temporal graph / contact plan）是**时间离散**的——若请求发生在 $t \notin \{t_1..t_M\}$，只能用最近时刻的静态图近似（L66）；缩短时隙能提高精度但存储爆炸，对资源受限小卫星是"bad bargain"（L22）；(b) 机会式路由要在轨收集全网状态，开销随网络规模（成百上千颗）急剧增大（L22、L49）。作者还点名 CGR 的 contact plan "can hardly be optimized without perceiving transmission requirements in advance"（L42）。

**3. 方法骨架**
非 RL，是**确定性图模型 + 贪心最短路 + 周期 beacon**。
- **TNM 模型**（第 III 节）：把轨道空间切成静态立方格 $\mathcal{C}_i$；每格存一个三元组 $\mathcal{P}_{v,i}=\{v,\mathcal{T}_v,(t^e_{v,i},t^l_{v,i})\}$（式 1，L78），即"哪颗星、轨道周期、进入/离开时刻"；格=集合 $\mathcal{C}_i=\{\mathcal{P}_{v,i}|v\in V_i\}$（式 2）。因为轨迹周期，时间 $t$ 用 $t \bmod \mathcal{T}_v$ 折回（L87）——这是"时间连续"的来源：任意 $t$ 都能定位，不需要离散快照。
- **数据结构**（第 III.C）：hashmap 索引到格，冲突用链表；格内 Data 用二叉树存（搜索 $O(\log \bar N)$），Pointer 指向"有效格"（Definition 1，L99：卫星通信范围内被完全包含的邻居格）。
- **多层划分**（第 IV 节）：$L_l = 2L_{l+1} = \frac{\sqrt 3}{3\cdot 2^l}R_a$（式 3，L119），层 1 取 $\frac{\sqrt3}{6}R_a$ 的理由是"卫星在格内位置未知，取格顶点画覆盖圆求交集，保证邻居格全落在交叠区"（L126）。精度 $\eta_l = V_l^{cubes}/(\frac43\pi R_a^3)$（Definition 2，L134），Proposition 1 证明 $l\to\infty$ 时 $\eta_l\to1$（L140–194）。
- **NSR 路由**（第 V 节）：beacon 协议周期广播，收到即标记 alive neighbor，**三个广播周期未收到就删除**（L209）；NSR 用优先队列 Q 在**格图**上做贪心最短路（Algorithm 1，L235–265），代价函数是 $time(e)=|D|/R + T_p$（Algorithm 3 第 8 行，L326）。关键设计：**只考虑 $t_s$ 时刻的静态拓扑**（L221、L340），路径由格组成，因此每一跳"含多选"（L273）。
- 复杂度：NSR 为 $O(\bar N_n^2 + \bar E_n)$，Dijkstra-SPF 为 $O(N^2+E)$（L309–311）。

**4. 它声称的效果**
- 端到端时延与丢包率上，NSR（层 2/层 3）**逼近 TBR 暴力最优**（L379、Fig 6）。
- 层 2 与层 3 多数情况接近，**包大小 > 300 KB 时层 2 开始劣化**（L379）。
- 抗链路中断：中断概率上升时 TBR/NSR/CGR 丢包平稳、时延上升；NSR 仍接近 TBR（L390、Fig 7）。
- NSR 优于自己的前作 EASR，且中断概率越高差距越大（L399、Fig 8）。
- 计算开销：TGM 拓扑开销随规模 $O(N^2)$ 增长，TNM 各层**线性**增长；路由开销 NSR 增长最慢（L408、Fig 9）。10 次重复取均值 + 95% CI（L375）。

**5. 实验条件**
Iridium-like 星座，6 个轨道面，高度 780 km，倾角 86.4°，偏心率 0，通信距离 5000 km，**传输速率 100 kbps**，TTL 10 min，**总共只生成 1000 个包**，仿真步长 0.1 s（Table II，L351–353）。硬件 Core i3-4150 / 12 GB / Win10，二体轨道模型（L363）。用户请求随机生成（L363）。
基线：TSR（TGM 源路由，只在源节点算一次）、CGR（每跳跑 Dijkstra-SPF）、TBR（暴力，视为最优上界）、EASR（作者前作，基于 TNM 的层 3）（L365–373）。
**训练/评估**：无学习环节，同一仿真器既做对比也做复杂度测量；性能点 10 次重复，复杂度点 10000 次重复（L408）。

**6. 自述局限（逐字）**
第 V.D 节（L340）："In the proposed NSR algorithm, the optimal path is only considered in static topology. There is no doubt that this approach can achieve significant complexity reduction. However, when route time becomes long enough, the shortest path obtained from NSR might be non-optimal."
同段给出两条不做时变拓扑的理由（计算代价过高；只能拿到邻居状态，收益有限），并给了一个"简单想法"（把等待时间 $T_w(\mathcal{C}_n)$ 加进代价，L342）**但没实现**。
L221 也承认："the optimal routing path output by NSR only outputs the estimated shortest path"。

**7. 它没做但看起来能做的地方（基于内容）**
1. **V.D 那个"简单想法"没做**（L342 给了 $T_w$ 公式却没进实验）——时变拓扑下的 NSR 版本是作者自己点名、自己没跑的空位。
2. **beacon 状态只用了传输速率 $R^b$**（Algorithm 2 第 12 行、Algorithm 3 第 8 行）：作者在 L207 明说 beacon 收集"queuing delay, transmission rate and so on"，但代价函数里**只有 $|D|/R$ 和传播时延 $T_p$**，排队时延$T_w$ 在实现里是 0——收集了却不使用。
3. **卫星只能同时连一颗星**（L363："each satellite can only connect to one satellite at the same time"），这一约束把 ISL 变成单服务器资源，但论文没做与之对应的排队建模。
4. 层数选择（层 2 还是层 3）靠实验经验（L379），精度 $\eta_l$ 的解析式已给，却**没把 $\eta_l$ 与端到端时延定量挂钩**——可做一个"精度→时延"的换算。
5. 到达过程只说"随机生成"（L363），**没有给出到达分布**（论文摘要 L5 写 "stochastic packet generations/arrivals"），也没扫描达率。

**8. 和同批其他篇的关系**
与 CYMQ2GLA（两跳状态感知 DRL 路由）、EG9X569M（鲁棒 DRL 路由）、CMNCS52M（流量感知 MARL）同属"LEO 路由"大类，但**路线相反**：这三篇是学习式/状态感知启发式，本篇是**确定性图模型 + 贪心最短路**，且明确把"在轨状态收集开销"当成要压的目标（L49）。它引用的经典对照是 TLR[14]（机会式代表）、MLSR[15]/SGRP[16]（多层结构）、CGR[20-22]、FSA[17]、Werner 动态虚拟拓扑[12]（L445–465）。它也是"时间离散快照 vs 时间连续模型"这条线的代表，DS9SPARV（OpenSN 仿真库）在仿真工具层面与它相邻（本篇还自建了 LSNS 仿真器，L361，并且开源 L481）。**同批中未见其他篇引用它**（它的年代早，2019 前后）。

**9. 对"负载变化下到达率/时延"的贡献**
**有间接贡献，但没有到达率扫描。** 贡献点：它把"随机到达"作为核心动机（L5、L22、L24），并论证时间离散模型与随机到达之间存在 "mismatching"（L22）——这是一条**模型层面的**事实：快照式拓扑描述会系统性错配按需到达。但它的实验轴是**包大小**（Fig 6）和**中断概率**（Fig 7），**不是到达率/负载**；全网只有 1000 个包、100 kbps，谈不上负载压力。可用的旁证：L381 指出"平均端到端时延随包大小增加 → 传输期间拓扑变化的概率更高 → TSR 性能变差"，这是"在网时间越长、过时拓扑越吃亏"的定性论证，可迁移到高负载场景，但论文自己没做负载实验。

**10. 一句话评价**
把"时间连续的空间离散化（netgrid）"这一建模技巧引入 LEO 路由，用**降低搜索空间规模**（$N \to$ 非空格数）换取可接受的精度损失；属于"拓扑描述模型创新 + 经典最短路"的路线，与全库的 DRL 主流正交，且它自己承认的静态拓扑假设正是高负载/长在网时间下最脆弱的地方。

## BLFJ6CLV — Analysis of Age of Information in Non-terrestrial Networks

**1. 一句话**
把"地面上一个源节点 ↔ LEO 星座"之间的连接过程抽象成一个 on-off 服务过程，用随机几何推出**时间平均 AoI 的闭式解**，然后看"状态更新速率 μ"和"星座密度 λ"各把 AoI 压到多少。

**2. 问题设定**
源节点与目的节点都在**地面网覆盖之外**，必须靠 NTN 中继状态更新（L40）。卫星高速运动 → 连接/断开频繁切换 → AoI 被这些切换推高（L21）。既有工作用随机几何算过覆盖概率（BPP on sphere，L23），但**"NTN 里的 AoI"没人算过**（L25）。关键麻烦：更新在**off 期间到达就直接丢掉**（L25 逐字："updates arriving during the off-service period are dropped"）。最近的工作 [23] 分析过 on-off 下的 AoI，但**只限 on/off 都服从指数分布**，而卫星的服务过程不是（L25）——这是本文要补的具体缺口。

**3. 方法骨架**
**不是 RL，是纯解析（随机几何 + 更新报酬定理）**。
- 网络模型（第 II 节）：卫星位置在半径 $R_\oplus+h$ 的球面上服从**齐次 PPP**，强度 λ（L40）；地面源节点用 generate-at-will，两个更新之间的间隔 i.i.d. 指数分布、速率 μ（L42）；连接判据是 SNR > 阈值 θ，由此得到最大可解码距离 $r_{max}=(P_{tx}/\sigma^2\theta)^{1/\alpha}$（L82），并在球面上切出一个"穹顶"区域；源节点只连接收功率最大的那一颗（L44）。
- **关键近似（L96 逐字）**：把穹顶内的所有卫星视为**空间静止**（"similar to stars in the sky that appear static for a short period of time"），而让**源节点以速度 v 做圆周运动**；每转完一圈，卫星位置按同一 PPP **重新生成**（独立再生）。这是全文的核心简化。
- **Theorem 1**（L100–110）：off 期间服从指数分布，速率 $\lambda_{os}=2\omega\lambda\sin(\varphi_e)(R_\oplus+h)^2$（式 6）；on 期间 W 的 PDF 由式 7 给出，**支撑集是 $[0, 2\varphi_e/\omega]$——有界区间**（这正是相对 [23] 的推广）。
- **Lemma 1/2**（L138–196）：算两个条件概率 $P_{f|f}=\frac{1-a}{1-ab}$（式 11，$a=\lambda_{os}/(\mu+\lambda_{os})$，$b=\int e^{-\mu s}f_W(s)ds$）与 $P_{o|o}$（式 12），再算 $E[Y_k]$、$E[Y_k^2]$（式 18、19，$\gamma=1/(1-P_{f|f})$）。
- **Theorem 2**（式 27，L245）：$\bar\Delta = \frac{\gamma^2(1-P_{o|o})}{\mu+\mu\gamma(1-P_{o|o})} + \frac1\mu + D$。用的框架是式 10 的 $\bar\Delta=\frac{E[Y_k^2]}{2E[Y_k]}+D$（L133），即经典 AoI 更新报酬形式。

**4. 它声称的效果**
- Fig 4（L251、L259）：时间平均 AoI 随**状态更新速率 μ** 上升而下降，且**下降速度逐渐变慢**；星座密度越大，AoI 越接近下界 $1/\mu$。原因是密度↑ → off 期间变短、on 占比变大（L259）。
- Fig 5（L264）：节点天顶角 $\varphi_s$ 变大 → on 期间变长 → AoI 下降。
- **精度验证**：解析曲线与仿真"close match"（L259）。
- 基线：**没有算法基线**，唯一的对照是自身的解析式 vs 数值仿真。

**5. 实验条件**
$h=800$ km，$\omega=\pi/3600$ rad/s，$\varphi_s=1°$，$D=1$ s（L255）。卫星密度扫描 $\lambda = 2\times10^{-5}$ 到 $5\times10^{-4}$ km⁻²（对应 12 924 与 323 100 颗星，L251），Fig 4 另有"通过穹顶的卫星数 225 到 5 638"这一口径（L259）、Fig 5 用 $5\times10^{-6}$ 到 $1\times10^{-4}$ km⁻²（3 231 与 64 620 颗，L264）。仿真：源节点绕行，每圈重生卫星位置，**每次仿真跑 $10^6$ 个到达**取 AoI 统计均值（L257）。
**训练/评估**：无训练；解析与仿真在同一套参数下对照，**没有跨场景泛化检验**。

**6. 自述局限（逐字）**
本文**没有独立"Limitations"章节**。可引的自述近似/假设：
- L96："We assume that the velocity difference between the satellites and the source node remains constant." 以及把穹顶内卫星"treat all satellites within the dome region as stationary"。
- L96："we assume that after completing a full cycle, the positions of the satellites are regenerated independently, following a homogeneous PPP with a density of λ."
- L40：卫星位置用**齐次 PPP** 近似真实星座（Walker 星座并非 PPP）。
另外它在 L25 明确把 [23] 的局限当成自己的出发点（"was limited to the case of on and off periods being exponentially distributed"）。
**未见**作者对自己"PPP 近似真实 Walker 星座""单源单目的""恒定传播时延 D"这些假设做过误差量化。

**7. 它没做但看起来能做的地方（基于内容）**
1. **只算了单调链路、单源单目的**（L40）：**没有路由、没有多跳、没有排队**——AoI 里唯一的时延是常数 $D$（式 27 最后一项）。把 $D$ 换成"随负载变化的排队时延"是这个式子最自然的下一步。
2. **没有把 AoI 做成优化问题**：μ 和 λ 都是外部给定，论文只是"算出来"，从未问"给定功率/密度预算，μ 取多少使 AoI 最小"。
3. **off 期间更新直接丢弃**（L25）——没有缓存、没有重传、没有"等下一个窗口"的策略；而 Fig 4 已经显示 off 是 AoI 的主要贡献项（$\gamma$ 项），所以"如何利用 off 期间"是作者自己数据指出的空位。
4. **式 25 有一个明显的印刷错误**：$E[Y_k^{2,f}] = \frac{2}{\lambda^2}\frac{P_{f|f}^2-3P_{f|f}+3}{(1-P_{f|f})^2}$（L231），分母是 $\lambda^2$ 而 $\lambda$ 在全文是**卫星密度**，此处按上下文应为 $\mu^2$（对照式 19 与式 23）。这个符号冲突读者需自行纠正。
5. 只给时间平均 AoI，**没有峰值 AoI（PAoI）**，也没有 AoI 的分布——L55 的 Fig 2 明明画了轨迹。

**8. 和同批其他篇的关系**
与本批其余 10 篇**基本不在一个世界里**：那 10 篇几乎都是"路由/调度算法 + 仿真"，本篇是**纯解析的性能界**，无算法、无基线、无 RL。它与 BBNQ4EAQ 共享"LEO 拓扑时变"这一动机，但处理方式相反（BBNQ4EAQ 用几何离散化建模拓扑，本文用 PPP + 几何概率建模连接性）。它的参考文献里没有本批任何一篇；本批也没有一篇引用它（它引的是 AoI 经典 [14][15][17]、卫星随机几何 [19][21][22]、以及 on-off AoI [23]，L302–326）。

**9. 对"负载变化下到达率/时延"的贡献**
**这是本批里与"到达率"关系最直接的一篇，但方向不同。** 它把**到达率 μ 当作自变量**、把 AoI 当作因变量，给出闭式曲线（Fig 4，L259）：μ↑ → AoI↓，且**收益递减**（"the rate of the time-average AoI descent gradually decreases"），下界是 $1/\mu$。同时它把到达率与**连接可用性**耦合：更新能不能被接收，取决于到达时刻落在 on 还是 off，于是有了式 11/12 那两个条件概率——**这是"到达时刻 × 间歇可用性"的一个可复用形式化**。
但它**没有时延这一维**：$D$ 是常数（L255 取 1 s），**没有排队、没有拥塞、没有负载对时延的反作用**。它给出的是"负载（更新速率）→ 信息新鲜度"的解析关系，而不是"负载 → 排队时延"的关系。若要把本批多数论文的"负载变化"问题接上 AoI，本式是现成的输入，但需要把常数 $D$ 换成排队模型。

**10. 一句话评价**
把 AoI 这一度量**首次**搬进 NTN，并把 on-off 服务过程的解析从"双指数"推广到"一指数 + 一有界支撑"（式 7），方法上干净、结论是"到达率越高越新鲜但边际递减、密度只能把 AoI 压向下界 $1/\mu$"；代价是**极度简化**——PPP 代星座、静止卫星代运动、常数时延代排队，因此它更像一个**参照下界**，而不是可部署的路由/调度结论。

## BV4XI6CU — Load Balancing for 5G Integrated Satellite-Terrestrial Networks

**1. 一句话**
定义了一个跨 RAT 通用的负载指标 RRUR（占用带宽/总带宽），用它做"先地面小区间迁移、还超载就把**容忍时延的业务流**甩给卫星"的两级负载均衡，并在迁移前先估算"搬到目标小区后目标会不会也被压垮"以防乒乓。

**2. 问题设定**
5G 多 RAT 网络里地面小区 + 卫星小区共存（L44）。UE 移动导致小区间负载不均，超载小区的 UE QoS 下降（L23、L124）。作者指出的两个具体障碍：(a) 既有负载均衡算法**只考虑单一 RAT**（地面↔地面），没考虑 NTN 共存（L27）；(b) 多 RAT 下**各 RAT 的资源分配单位不同**——地面用 PRB，而 **5G 的 PRB 总数 $N_{PRB}$ 随子载波间隔动态变化**，因此 LTE 时代的 RBUR **不能直接用于 5G**（L100），卫星侧根本不按 PRB 分配（L102）。所以需要一个共同负载口径。

**3. 方法骨架**
**不是 RL，是规则式/阈值式算法 + 5G 标准流程（事件 A3/A4、QoS flow、SMF/UPF）**。
- **负载度量 RRUR**（第 II.D，式 3、4，L107/L115）：地面小区 $\beta_n = \frac{1}{T\omega_n}\sum_{\tau}\gamma_\tau\varsigma_\tau$（分配的 PRB 数 × 每 RB 带宽 / 小区总带宽）；卫星小区 $\beta_S = \frac{1}{T\omega_{sat}}\sum_\tau \Omega_\tau$，其中 $\Omega_\tau$ 按 **Shannon 公式**由 UE 需求速率换算成带宽（L118）。作者的论点是 RRUR 是"带宽占比"，因此**与物理层信道特性无关**（L120 逐字："the physical layer channel of each RAT does not affect the problem formulation"）。
- **问题形式**（式 5，L129）：$\min\sum_{n\in\mathcal T}|\bar\beta-\beta_n|^2$，约束卫星不过载 $\beta_S\le Thr_{adp}$、每 UE 分到不少于所需 $\rho_i$。目标值 $\bar\beta$ 用**均方估计**推出等于 $E[\beta_n]$（式 6、7，L155–161）——这一段的数学其实只是"最小化平方距离的解是均值"，属常识推导。
- **自适应阈值**（式 8，L189）：$Thr_{adp}=\max(\bar\beta, thr_{init})$，跟着网络负载浮动；超载判据 $\beta_n > Thr_{adp}$（式 9）。
- **两级流程**（Algorithm 1，L166–175）：
  1. **info_gather**（Algorithm 2）：测各地面 RRUR → 算均值 → 定阈值 → 得超载集合 $\mathcal O$。
  2. **intRAlb**（Algorithm 3，L228–250）：用 **A4 事件**筛出边缘 UE 集合 $E_o$，按 RSRP 升序、**先时延敏感后时延容忍**排列；对每个 UE 逐个尝试候选邻区（A3 事件给出 $\Gamma_{e_i}$），**先估算** $\hat\beta_{\Gamma_k}^{e_1}=\rho_{e_1}\varsigma/\omega_{\Gamma_k}$（式 10），要求**目标迁入后仍不过载**（式 11）**且迁出比迁入更划算**（式 12：$\beta_o-\hat\beta_o^{e_1} > \beta_{\Gamma_k}+\hat\beta_{\Gamma_k}^{e_1}$），满足才迁，迁完就地更新两侧 RRUR（L255）。
  3. **intERlb**（Algorithm 4，L274–294）：若地面仍超载且 $\beta_S<Thr_{adp}$（式 13），把**时延容忍流**逐个甩给卫星，前提是 $\beta_S+\hat\beta_S^{\varepsilon_1}<Thr_{adp}$（式 14），由 **UPF 直接改用户面**（L302）。
- **时延敏感的判定标准（关键）**：流的 PDB **大于**卫星传播时延 → 容忍；**小于** → 敏感（L52）。即用"传播时延本身"当分界线。
- 复杂度：$O(I|\mathcal T|)$（L314）。

**4. 它声称的效果**
- **负载均衡**（Fig 6，L332–344）：无 MLB 时同一时刻最大/最小 RRUR 差 **0.28**（cell 4 的 0.99 vs cell 1 的 0.71）；只用 intra-RAT MLB 降到 **0.10**；用提出的 multi-RAT MLB 进一步降到 **0.019**，且所有地面小区 RRUR 都降到阈值以下。
- **标准差**（Fig 8，L352）：multi-RAT 的 RRUR 标准差**接近 0**，小于 intra-RAT。
- **吞吐与 QoS**（Fig 9，L356）：multi-RAT 的吞吐与"满足 QoS 的 UE 数"都高于 intra-RAT，且**100% 的 UE 拿到所需速率**（结论 L408）。
- **UE 数变化**（Fig 10，L376）：UE 越多吞吐越高；标准差随 UE 数增加而升，但 multi-RAT 升得**很少**。Fig 11：卫星资源利用率**不到一半**。
- **带宽变化**（Fig 12、13，L380）：地面带宽 > 30 MHz 后 intra-RAT 的标准差逐渐追上 multi-RAT。
- **时延容忍流比例扫描**（Fig 14，L400–404）：容忍流占比 0→30%，multi-RAT 性能随之上升；**容忍流占比为 0 时 multi-RAT 退化为 intra-RAT**；超过某个最小占比后性能**饱和为常数**；**高负载时需要更高的容忍流占比**。
- 基线：adaptive intra-RAT MLB（即文献 [15] 的自适应移动性负载均衡）与 no MLB（L328）。

**5. 实验条件**
**注意：这里的"卫星"是 GEO 不是 LEO**——卫星高度 **35 780 km**，C 波段 3.7–4.2 GHz 下行，500 MHz 带宽、12 个转发器、每转发器 36 MHz + 4 MHz 保护带（L320、Table 3 L326）。作者的理由是 GEO 相对静止、无需星间切换、无多普勒（L44）。
地面：**7 个 5G 小站，六边形部署**，发射功率 46 dBm，带宽 20 MHz，路损 $PL=147.4+43.3\log_{10}(d)$（Table 3）。**110 个 UE**，需求速率 5–15 Mbps，随机分布，**一半静止一半随机移动**（L318）。**70% UE 是时延容忍流**，其余时延敏感；容忍流用 15 kHz 子载波间隔，敏感流用 15 或 30 kHz（L320）。初始阈值 75%（Table 3）。
**训练/评估**：**无任何学习**，规则算法在同一仿真里评估；论文**没有给出仿真器的名称/来源**（L316–320 只描述场景），也没有说重复次数与置信区间。

**6. 自述局限（逐字）**
本篇**没有 Limitations 章节**。最接近的自述在结论（L408）：
"**The proposed algorithm depends on the availability of delay-tolerant flows to achieve better performance.**"
以及 L404 的展开："**the adaptive multi-RAT MLB depends on the availability of delay-tolerant flows for inter-RAT offloading to achieve better performance**"，并明确指出"当网络负载高时，需要**更高**的容忍流占比才能平衡地面小区"。
另一条自述性说明在 L310：迁到卫星的 UE "will experience a long delay"，作者的处理方式是"反正它们的流是时延容忍的"。
**未见**作者讨论：GEO 时延具体多大、卫星链路容量与地面用户数的匹配、UE 移动模型、以及"RRUR 与物理层无关"这一强假设的边界。

**7. 它没做但看起来能做的地方（基于内容）**
1. **全是 GEO + 静止卫星**（L44），而 LEO 的核心难点恰恰是"卫星会走、覆盖会变、RRUR 会随卫星移动剧烈波动"——这篇的所有结论都建立在"卫星永远在那儿、覆盖全网"上（L302 逐字："all UEs are within the coverage area of the satellite"）。换成 LEO 后，"何时该卸载到卫星"立刻变成一个**时变**问题，本文没有工具。
2. **时延只在"分类"里出现一次**（PDB vs 传播时延，L52），此后**再也不进入优化目标**。式 5 的目标只有 RRUR 方差。可以自然地把"卸载带来的时延增量"写进代价。
3. **没有排队模型**：式 3/4 的 RRUR 是**时间窗口平均的带宽占用率**，完全是"资源占用"口径，不含等待时延、不含缓冲区。所以"负载均衡做好了，时延就一定好吗"在这篇里没有被验证。
4. **阈值 $thr_{init}=75\%$ 是固定常数**（Table 3），$Thr_{adp}=\max(\bar\beta, thr_{init})$ 只做了"取较大值"这一层自适应；$\bar\beta$ 的推导（式 6/7）说明它只是样本均值，**没有用任何反馈/控制理论**（例如 PID、拥塞控制的 AIMD）来自适应，而负载均衡本身就是一个典型的闭环控制问题。
5. **乒乓规避靠式 11/12 两个静态不等式**（L221/L225），一旦 UE 移动或需求速率变化，这两个不等式的前提就变了；论文**没有报告乒乓率**。
6. Fig 14 显示"高负载需要更多容忍流"——这是**负载与可行域**的关系曲线，但论文只是描述现象，没有回答"容忍流不够时怎么办"（例如降级、部分卸载、缓存）。

**8. 和同批其他篇的关系**
与 BBNQ4EAQ、CYMQ2GLA、EG9X569M、CMNCS52M 同属"（星地）网络资源/路由管理"，但**层次不同**：那几篇是**星间路由/拓扑**，本篇是**接入侧小区间负载迁移**，完全不涉及 ISL、不涉及星间多跳。与 CTWVLBCY（调度）相邻但正交：那篇在**时间维**上调度（何时发），本篇在**空间/RAT 维**上迁移（发给谁）。与 BLFJ6CLV 有一处概念交集——两篇都用"时延容忍 vs 敏感"这一分类，但 BLFJ6CLV 用的是 AoI 度量，本篇用的是 3GPP PDB。
它引用的基础是 LTE/5G 负载均衡文献 [13][14][15][16]（L436–442），其中 [15] 既是它的主要基线也是它的方法来源（L440）。**本批其余 9 篇没有一篇引用它**，它也没引本批任何一篇。

**9. 对"负载变化下到达率/时延"的贡献**
**有直接贡献，但口径是"资源占用"而不是"到达率"。** 它做的是**负载变化下的资源再分配**，而且**负载是被显式扫描的自变量**：
- Fig 10（L376）扫 UE 数量；
- Fig 14（L400）**把"网络负载"直接定义成每 UE 的需求速率（低载 5–10 Mbps / 高载 10–15 Mbps）**，再扫容忍流占比，得到"负载越高，越需要容忍流才能平衡"——这是一条**负载 → 可调度性**的关系曲线，是本文对"负载"最实质的贡献。
- 式 11/12（L221/L225）提供了一条可复用的**准入判据**：迁移前先估"迁入后目标是否超载"，等价于"目标剩余容量 ≥ 新需求"。这套判据可以直接搬到"负载变化下是否接纳新流"的决策上。
但它**对时延的贡献很弱**：全文唯一涉及时延的地方是"PDB 与卫星传播时延比大小"的分类规则（L52），以及 L310 一句"迁到卫星会经历长时延，但那些业务容忍"。**没有时延的数值结果、没有排队、没有负载→时延的曲线**。所以：它贡献了"负载→资源占用/均衡度/QoS 满足数"的事实链，**没有**贡献"负载→时延"的事实链。

**10. 一句话评价**
把 LTE 时代的移动性负载均衡（MLB）**扩展到多 RAT（地面 + 卫星）**，核心创新是一个可跨 RAT 比较的负载口径 RRUR（式 3/4）加一条"先租邻居、再租卫星"的两级规则；方法上属于**工程化的启发式 + 标准流程复用**，无学习、无排队、无 LEO，因此它是一个**接入侧负载管理的参照系**，而不是路由或时延研究。


## CMNCS52M — Traffic-Aware Multi-Agent Reinforcement Learning-Based Distributed Routing for Low Earth Orbit Satellite Network

**1. 一句话**
每颗星一个 DDQN agent、只看自己周围 15/16 维局部观测选下一跳，**奖励直接用"实际一跳时延"（传播+发送+下一跳排队）**，并刻意在三个"队列分布模型"（人造分区 / 人口分布 / 真实流量生成）上训练同一个策略，以此换取跨星座规模、跨流量模式、跨链路故障的泛化。

**2. 问题设定**
LEO 极化星座的分布式路由（L13、L23）。作者点出的既有工作的三个具体病灶（L21 逐字概括）："these methods are often highly tailored to specific network sizes, congestion levels, and packet lengths, which limits their effectiveness when applied to different configurations"；"the reward function is not always well aligned with the ultimate objective"；以及"DRL-based routing strategies have not been leveraged to learn from specific traffic patterns to avoid congestion, and their performance evaluations are typically restricted to idealized scenarios that do not consider link failures"。
更具体的技术批评：文献 [14][15] 的奖励**只有排队时延和传播时延、漏了发送时延**（L56 逐字："the reward function considers only queuing and propagation delays, neglecting the transmission time of packets"），因此对不同包长是次优的；[16][17] 强加**最大跳数**，与卫星数强耦合（L58）；[17] 的奖励是**基于拥塞的不连续函数**（L58）；[18] 的队列状态是**离散的**（free/busy，L60）。

**3. 方法骨架**
- **问题形式**（第 IV 节，式 1，L106–125）：$\min_{\mathbf p_k}\sum_i (t_P + t_{TX} + t_Q)$，即路径上**传播 + 发送 + 排队**三项之和。论文明确说明"最优路径会随包长变化"（L125）。
- **观测**（第 V.A，L141–155）：16 维连续向量 $\mathbf s_i=[\mathbf q_i,\phi_i,\lambda_i,\phi_D,\lambda_D,L,d_i^V,d_i^H,\mathbf h_i,t]$——四邻居队列长度、自身与目的经纬度、包长（50–250 B）、**南北/东西两个星间距离**、**四个方向的访问计数器 $\mathbf h_i$**（防环用）、一天中的小时 $t$（0–24）。注意：$d^V$/$d^H$ 保留的理由是"真实场景中星座参数未必在星上已知"（L149）。
- **动作**（第 V.B，L159）：$\mathbf A=\{{N,E,S,W}\}$ 四邻居，**禁止朝反向运动的邻居转发**（否则天线指向要突变），因此 cross-seam 上的星只有 3 个邻居；**也禁止转发给拥塞卫星**（L159）。
- **奖励**（式 6，L166）：到目的 $R$；动作非法 $-R$；否则 $-(t_{HOP}(i,j,L)\times(1+\mathbf h_i(a)))$。其中 $t_{HOP}=t_P(i,j)+t_{TX}(L)+t_Q(j)$（式 7，L172）——**这一项就是本文相对 [14][15] 的核心修正：补上 $t_{TX}$**。惩罚还要乘"该方向已访问次数"，这是在奖励里内嵌防环。$R$ 需按每个队列模型单独标定（L169），所有瞬时奖励绝对值归一化到 0–30k（L169）。
- **算法**（第 V 节，L131–137）：DDQN，在线网 + 目标网，目标值式 5 写的是 $y_j=r_j+\gamma\max_a Q_t(s_{j+1},a)$——注意这**是普通 DQN 的 max 目标，不是 double**（同 S85KQ4FC 的同类问题）。目标网每 10000 步硬拷贝。论文明确声明转移与奖励都是**确定性**的（L137 逐字："we define both the transition function and the reward function as deterministic"）。
- 网络：4 隐层 64/32/16/8，输出 4（Table 2，L182）。训练 500 000 episodes、lr 0.005、γ 0.99、replay 10 000、batch 128。

**4. 它声称的效果**（数字以 Table 3（L228）与结论（L283）为准，注意 Table 3 的 OCR 表格列错位，数字需谨慎对应）
- 摘要（L13）：**在特定条件下 E2E 时延相对三个传统分布式协议降低 72%、66%、48%**；相对 SOTA 的 RL 分布式路由**最高降低 27%**。
- NMB（式 8，L222）：zone 下 DQN-BL 与 DQN-LSNR 都约 **15%**；population 下从 DQN-BL 的 70% 降到 LSNR 的 **40%**；traffic 下从 55% 降到 **20%**（L230）。结论里改口径说 traffic-based 下 NMB 只有 **17%**（L283）——与正文 20% 口径不一致。
- 结论（L283）：population 下 E2E 约为 DRP 的**一半**，traffic 下**最高三倍低**；相对 SOTA DQN 降低 **18%**（population）与 **27%**（traffic）。
- **路径最优性**（Fig 7，L272）：跨越训练用到的 **130 种星座配置**，traffic 与 zone 下最优性**> 80%**，population 下**> 50%**，且**星座越密最优性越高**。
- **PDR**：DQN-BL 在 population/traffic 下 PDR 只有 **95%/97%**（陷入环路，L232）；DQN-LSNR 100%。链路故障 0→30% 时，GF 与 DQN-BL 的 PDR 掉到 **约 40%**（L238）。
- 复杂度（第 VI.G，L276）：Dijkstra 用二叉堆 $O((V+E)\log V)$；DQN-LSNR **单次推理约 110 μs**（PyTorch CPU，i7-11800H，batch=1）；超过 **10 000 颗星**时分布式方案在计算时间上占优。
- 基线：GF、DRP、CA-DRP、DQN-BL（=复现文献[17]的 FDR-MARL）、SP（Dijkstra 集中式上界）、H-DRP（作者新造的防环版 DRP，L238）。

**5. 实验条件**
- 星座：**极轨均匀星座，高度 780 km、倾角 90°**；轨道面数 **{3,…,12}**、每面卫星数 **{4,…,16}**，即 **12 到 192 颗**（L73）。cross-seam 在 0°。包长 **50–250 B 随机**（L73）。
- **三个队列分布模型**（第 III.B，L77–97）：(a) zone：8 个经纬分区、占用率 0–1，均值 0.5，队列容量 **10 MB**；(b) population：用 **GPWv4**（2020 年 1° 网格）+ 世界银行互联网使用率换算活跃用户，最高区归一为 1，平均占用率**仅约 0.06**，容量 **100 MB**；(c) traffic：由 **GDP/人 线性回归**得人均需求 IUD，卫星流量随经过区域累积，容量 **150 MB**，并**按队列长度自适应调发送速率**（<25 MB 用 25%、25–50 MB 用 50%、否则 100%）。最大排队出现在北美，**150 MB @ 50 Mbps 对应最大排队时延 24 s**（L97）。
- **关键简化**（L73 逐字）：星速约 0.07°/s，因此"**we assume that the network topology remains static during the transmission of a packet**"，并把可允许 E2E 时延约束在**几秒**内。
- 训练/评估：训练 500 000 episodes，每 episode 随机抽轨道面数、每面星数、源/目的、包长、队列状态、轨道位置（L189）；评估 Iridium-like（**6 面 × 11 颗**）下 **10 000 次**传输（L217），路径最优性用 **100 个测试 episode**（L272）。**训练与评估共用同一套仿真器**，但训练覆盖多配置、评估抽其中配置。

**6. 自述局限（逐字）**
- L73（核心假设）："we assume that the network topology remains static during the transmission of a packet. **This assumption simplifies the routing problem, but it constrains the maximum allowable E2E delay to a few seconds.**"
- L238（链路故障下的取舍）："Although it solves fewer scenarios than DRP and H-DRP, it consistently maintains lower E2E delays than H-DRP." 并给出一条务实建议：**"the most effective strategy in practical environments with potential link failures would be to primarily rely on DQN-LSNR, switching to H-DRP only when the E2E delay or hop count exceeds a predefined upper threshold."**——即它自己承认单独用 DQN-LSNR 不能保证送达。
- L287（未来工作）："Future work will focus on further analyzing the generalization capabilities of DQN-LSNR under large-scale mega-constellations. In addition, routing complexity will be increased by incorporating satellites with different orbital altitudes and inclinations."
- L276：承认推理开销仍需优化（"optimizing inference efficiency... is crucial for scalability"）。
- 另注 L291：作者声明使用了 AI 语言工具润色。

**7. 它没做但看起来能做的地方（基于内容）**
1. **"拓扑在一次传输内静止"（L73）与"E2E 时延不能超过几秒"是同一个硬币的两面**——这直接把情景锁死在低时延小包（50–250 B）上。若包变大或拥塞变重，这个假设先崩，"队列 150 MB、排队时延 24 s"的模型（L97）与该假设**互相矛盾**：24 s 的排队早就超过"几秒"。作者没有处理这个内部张力。
2. **队列模型与训练/评估的关系没有消融**：论文说"the learning process enables agents to infer the underlying traffic patterns"（L127），但**没有报告"只在一个队列模型上训练、到另一个上测"的迁移实验**——而这恰恰是"traffic-aware"这个标题的主张。已有的 cross-model 结果全是"一个策略在三个模型上分别测"（若真如此训练，则是 joint training），论文未明确说明三模型是联合训练还是分别训练。
3. **奖励里的 $R$ 需要按队列模型逐个标定**（L169）——作者自己也说"each queue model requires a distinct value of R"。这是一个**逐场景手调的超参**，与它"泛化"的主张有张力，但论文没有把 $R$ 也做成自适应。
4. **访问计数器 $\mathbf h_i$ 的四个额外维度有效但未消融**（L151、L232）：作者说它把观测从 22 降到 16（去掉历史是 12），但**没有给出"有/无 $\mathbf h$"的对照**——防环到底是 $\mathbf h$ 的功劳还是奖励里 $(1+\mathbf h_i(a))$ 的功劳，不可分辨。
5. **DDQN 名不副实**：式 5（L134）是 $\max_a Q_t$ 的普通 DQN 目标，论文自称 DDQN（L131），但没有 double 的第二张网取动作。与同批 S85KQ4FC 犯同一个错。
6. **Table 3（L228）的 OCR 严重错位**，列名与数值错配（如 "DRP" 落在 NMB 行），**无法可靠复原每个协议每格的数值**；正文里 NMB 的 15%/40%/20% 与结论的 17% 也不一致（L230 vs L283）。这是一处需要回原文图确认的地方。
7. **没有到达率这个自变量**：所有负载差异都通过"换一个队列分布模型"体现，**没有扫描流量强度**（如 IUD 从 1 到 100）。"负载变化"在这篇里是**空间模式**的变化，不是**强度**的变化。

**8. 和同批其他篇的关系**
- **直接引用并复现 CYMQ2GLA**：文献 [18] = C. Wang et al., "A two-hops state-aware routing strategy based on deep reinforcement learning for LEO satellite networks", Electronics 2019（L329）——这正是同批的 CYMQ2GLA。CMNCS52M 在 L60 明确批评它："**its advantages over a simpler one-hop strategy remain unclear given the additional overhead it introduces**"。
- **同批 S85KQ4FC 的批评对象也在本文里**：文献 [17] = Xu et al. FDR-MARL（L327），正是 S85KQ4FC 点名的"逐包 DRL 代表"之一；本文把 [17] 复现为 DQN-BL 当基线并**赢它 18%/27%**。文献 [20] = DRL-ER（L333）也被 S85KQ4FC 列为逐包对照。
- 与 BBNQ4EAQ 同属"LEO 路由"，但路线相反：BBNQ4EAQ 用几何离散化 + 确定性最短路，本文用局部观测 DRL；BBNQ4EAQ 引 TLR[14]（其 L449）作为机会式代表，本文 L46 也把 **ELB 与 TLR** 作为距离矢量协议代表——两篇共享同一套经典对照。
- 它明确站在"分布式 > 集中式"的立场上（L46、L54），与 BBNQ4EAQ 的"减少在轨状态收集开销"是同一动机的不同解法。

**9. 对"负载变化下到达率/时延"的贡献**
**有实质贡献，而且是最贴近本主题的一篇。**
- **奖励函数里显式含排队项**：$t_{HOP}=t_P+t_{TX}+t_Q(j)$（式 7，L172），且 $t_Q$ 由**下一跳的队列长度**决定。这意味着 agent 学到的策略本身就是"**负载 → 时延 → 下一跳**"的映射。
- **给了具体的负载–时延换算**：150 MB 队列 @ 50 Mbps = **24 s 排队时延**；10 MB @ 50 Mbps 把平均排队压到约 **1 s**；population 模型平均占用率 0.06，容量 100 MB（L89、L93、L97）。这些是可以直接复用的量级锚点。
- **给了"负载的性质比负载的大小更重要"这一事实**：traffic-based 模型队列容量最大（150 MB）却**总体几乎不拥塞**，因为大部分区域队列为空、时延只剩传播+发送（L97 逐字："white regions indicate that satellite queues are consistently empty, meaning that the E2E delay is solely influenced by propagation and transmission times"）；反而是人造 zone 模型平均占用率最高（0.5）。GF/DRP 在 traffic 场景下最差（L225），说明**稀疏但极端的负载**对距离型协议杀伤更大。
- **给了"排队时延让最优路径变长"的直接证据**：Table 3 讨论（L232）指出 SP 在 zone/population 下**平均跳数更大**（6.87、8.34 跳）却时延更优，即"绕远但避堵"确实成立；而 traffic 场景下最优路径接近最小跳。
- **但缺"到达率"这一维**：完全没有以包到达率/流强度为自变量的扫描。负载只通过"取哪个队列分布图"来变，**负载强度不可调**。所以它贡献的是"**负载的空间分布 → 时延**"，不是"**负载的时间强度（到达率）→ 时延**"。

**10. 一句话评价**
把 MARL 路由的**奖励函数对齐到真实 E2E 时延**（补上被前人漏掉的发送时延，式 7）并把**队列分布模型**从"人造拥塞"推进到"人口+GDP 驱动的真实流量"，是本批里工程完备度最高的一篇；但它用"包内拓扑静止 + 时延不超几秒"这一条假设把问题锁在小包低时延区间，且把泛化主张建立在一个需逐场景手调的 $R$ 上——**方法谱系位置：把已有的多智能体 DQN 路由 × 更好的状态/奖励设计 × 更真实的流量模型**，属改良而非新范式。


## CTWVLBCY — Transmitting, Fast and Slow: Scheduling Satellite Traffic through Space and Time (Umbra, MobiCom'23)

**1. 一句话**
发现"每个接触窗口都拼命传满"这种贪心做法反而会把某些地面站撑爆、别的站点闲置（作者命名为 UQE），于是定义一个叫 **withhold scheduling** 的新调度范式——**主动少用一部分星地链路、把数据扣下来留给后面更划算的接触**——并把整个"卫星→地面站→云"两跳传输建成**时间扩展网络（TEN）**，用匈牙利匹配 + 最大流 + 二分搜索求出同时优化吞吐和时延的计划。

**2. 问题设定**
对地观测 LEO 星座（Planet Dove，153 星）每天产生 TB 级影像，要经地面站中转上云（L28–L30）。约束是：单星-单站接触一天只有 4–6 个十分钟窗口（L30），**地面站数量（10 量级）远少于卫星（100 量级）**（L101），且地面站分布不均匀（L46），**地面站到云的 backhaul 带宽在 100s Mbps 到几 Gbps 之间浮动**（L50、L234）。
具体病灶（UQE，L46–L52）：卫星连续经过地面站 A、B、C，若 A-B 距离 > B-C，则卫星在 A-B 段采集的数据远多于 B-C 段；贪心全速传输会让 B 收到 9 GB 而 C 只收到 1 GB → **B 侧排队爆、C 侧闲置**。作者进一步指出"即使未来 backhaul 带宽提升，UQE 仍会继续堆积队列"（L50 逐字："even if backhaul bandwidths increase in the future, UQE will continue to back up queues"），因为带宽提升也让卫星侧传得更快。

**3. 方法骨架**
**不是 RL，是组合优化（网络流）**。
- **TEN 建模**（第 3.1 节，L114–L130）：把"空间"和"时间"放进同一张图。每层（时刻）是一个卫星-地面站二部图；层间用 **holdover edge**（节点指向自己未来时刻）表示"**有带宽也不用、把数据扣住**"的能力，容量设 ∞（依据：Dove 卫星有 2 TB 存储，L120）。变量 $D_{i,j}(t)$ = 卫星 $s_i$ 在时刻 $t$ 下传给地面站 $g_j$ 的数据量，四条约束：单星同时只连一站、单站同时只连一星（可扩展到多天线）、不超过下行带宽 $b_{s_i,g_j}(t)$、累计传出不超过累计采集 $p_i(t)$。地面站上传量 $u_j(t)=\max(\sum_i\sum_\tau D_{i,j}(\tau)-\sum_\tau^{t-1}u_j(\tau),\ b_j(t))$。目标 $D^*=\arg\max\sum_i\sum_t u_i(t)$（式 1）。
- **三步算法**（第 3.2 节）：
  1. **Stage 1 匹配**（3.2.1）：逐时刻解二部图最大权匹配，边权 $R_{i,j}(t)=\max(b_{s_i,g_j}(t), cache_i(t))$，用**匈牙利算法** $O(n^3)$。
  2. **Stage 2 最大流**（3.2.2）：在整张 TEN 上做**推流-重标号（push-relabel）**最大流，复杂度 $O(V^2\sqrt E)$。**流经过 holdover edge 就意味着那颗星在这一时刻选择 withhold**（L172）。
  3. **Stage 3 时延优化**（3.2.3）：在 $[0,T]$ 上**二分搜索**最小的 $T'$，使 $[0,T']$ 上的吞吐 ≥ 原方案 99%，然后滚动到 $[T', T'+T]$ 执行——**在不牺牲吞吐的前提下压时延**。
  4. **图简化**（3.2.4）：一天 1 分钟粒度的 TEN 有 **200 万节点**；利用接触稀疏性把"只有一条入边一条出边"的连续节点序列**折叠成一个融合节点**，不改变最大流结果。
- **UQE 定量分析**（第 3.3 节，Theorem 1，L189–203）：设相邻地面站间距 $x_i=\mu+\delta_i$，则数据被采集的概率正比于 $x_i$，平均额外等待正比于 $x_i/2$，于是平均排队时间 $Y\propto\sum x_i^2/2 = \frac12(\sum\mu^2+\sum\delta_i^2)$——**与间距的方差成正比**（正文 L187 说"二次增长"，推导实际给的是"正比于方差"）。
- 系统实现（第 4 节）：调度器**跑在云上**，计划经地面站中继给卫星；用 TLE + PyOrbital 算轨道，用 **ITU P.838/839/840 模型**算雨衰、DarkSky API 取天气；每 **5 天**重算一次计划；故障时卫星靠"收不到 ACK"自行判定并扣住数据等下个可用站（L218）。

**4. 它声称的效果**
- **总收益**（摘要 L7、L75）：吞吐 **+13–31%**，P90 时延 **降低 3–6×**。
- **吞吐**（Table 2，L307）：1.2 Gbps backhaul 下 Umbra 比 Greedy 高 **13%**、比 Naive withhold 高 **31%**、比 Smart withhold 高 **13%**。backhaul 越高（1.8 Gbps）优势越小（L289）。
- **时延**（L293）：1.2 Gbps 时 **中位时延 Greedy 8.8 h vs Umbra 6.2 h（Greedy 高 42%）**；Naive 13.7 h；Smart 8.9 h。**P90：Umbra 11.0 h vs Greedy 38.7 h（3.5×）、Naive 66.5 h（6×）、Smart 37.98 h（3.5×）**。1.5 Gbps 下 P90：Greedy 19.3 h、Naive 60.9 h、Smart 20 h、Umbra 8.3 h。
- **反直觉结果**（L280，Fig 10）：**把卫星下行带宽翻倍，P90 时延反而上升 22%**——因为 UQE 下更快的下行只会把更多数据灌进拥堵的地面站。
- **异构 backhaul**（Table 4，L305）：随机 50% 地面站给 2 Gbps，Umbra **571.8 TB（标准差 0.10）** vs Greedy 435.99 TB（标准差 8.36），**提升 31%** 且波动极小。
- **分布式大量小站**（Table 5，L354）：200 个 SatNOGS 业余站、总 backhaul 8× 冗余时，吞吐提升**不显著**（445.01 vs 425.54），但 **P90 时延仍好 2.5×**——作者据此论证"UQE 不是靠堆基础设施能解决的"。
- **鲁棒性**（L358–L362）：带宽估计噪声 0.05→0.2 使中位时延退化 15%、P90 退化 8.4%；33% 地面站在 t=60h 挂掉时，Umbra(Update) 与 Oracle 持平，Umbra(No Update) 只能撑约 40 小时（**计划不到 2 天就过时**）。
- **内部观察**（L299–L301）：Umbra 的 withhold 决策**大多是二值的**（要么全扣要么全传）；Greedy 下不同地面站队列"wildly vary"，Umbra 把队列拉平。
- 基线：**Greedy**（现状）、**Withhold-Naive**（只看当前与下一个地面站队列大小，若下一个更空就全扣）、**Withhold-Smart**（按 $V_0=V\frac{q_2}{q_1+q_2}$ 按比例扣）。
- 开销：单核调度整个星座 5 天的流量约 **25 分钟**（L251）。

**5. 实验条件**
**真实 trace 驱动**：Planet Dove 星座 **153 颗星**、**12 个地面站（共 48 副天线）**、**5 993 212 张影像**、平均 **300 MB/张**、总计 **1798 TB**、跨 **15 天**（2021 年 6/7/8 月各前 5 天）（Table 1，L246）。星地链路 **X 波段、最高 2 Gbps**；backhaul 估计多数约 1 Gbps（100 Mbps–几 Gbps），实验中扫描 **1.2 / 1.5 / 1.8 Gbps**。仿真时间粒度 **1 分钟**，离散事件仿真。硬件 SuperMicro SYS-4028GR-TR。
**关键假设**（L93 逐字三条）：(a) **卫星之间不能直接传数据**（no ISL，"true for all major LEO earth observation satellite constellations today"）；(b) 地面站之间也不能互传（会占用本该给云的带宽）；(c) 地面站不跨应用共享。另假设云始终可用（L214）。
**训练/评估**：无学习；同一 trace 上对比四种算法，另在 3 个不同月份/年度的 trace 上重复（L287，只取 Day 2 以后衡量稳态）。

**6. 自述局限（逐字）**
- L378：**没有 ISL** 是评估假设——"Our evaluation assumed the absence of these links because they are not common in today's deployments. However, both these kinds of links can be added to our graph and our TEN-based solution (Section 3) would still generate a solution."
- **第 8 节"What did not work?"**（L380）：作者主动报告失败尝试——"We experimented with iterating between: (a) identifying the best matching... and (b) computing the max flow... However, we noticed that the scheduling objective (e.g. throughput) showed little improvement beyond more than one iteration, and only increased computation cost."
- L354：分布式地面站场景下"**The improvement on average throughput by Umbra is not significant**"。
- L251：调度器 25 分钟的运行时间"could be optimized further by leveraging parallelization... However we do not explore this"。
- L376：GSaaS 场景下"the measurement of network queue size needs to be indirect, as the queue size at the ground station may not be visible to satellite constellation operators"——即**它依赖的队列信息在真实多租户场景下拿不到**。
- L382 提出三个未来会加剧 backhaul 需求的因素（含地面站侧预处理带来的计算排队）。

**7. 它没做但看起来能做的地方（基于内容）**
1. **没有 ISL 是最大口子**，而作者自己在 L378 给了补法（"a satellite could route data through another satellite using an inter-satellite link, especially when the latter satellite is connected to a low-queue station"）——**并明确指出这正好能治 UQE**，但没做。这是现成的下一步，而且和本批其他篇（都在做 ISL 路由）天然衔接。
2. **队列信息在 GSaaS 场景不可见**（L376），作者只说"需要间接测量"，没给方案——"从卫星侧反推地面站队列"是一个自然课题。
3. **$T'$ 的 99% 阈值是拍出来的常数**（L174），没有敏感性分析；等价于"吞吐换时延"曲线上的一个固定工作点，**没有刻画吞吐–时延权衡的整条前沿**。
4. **计划每 5 天重算，但实测不到 2 天就过时**（L362）——重算周期与失效速度不匹配，论文没解释为什么不缩短周期（只说 25 分钟算得动）。
5. **负载（影像到达）完全是真实 trace，不可调**：没有任何"把数据量放大/缩小 k 倍"的扫描，因此**"负载强度 → 时延"的曲线不存在**。所有负载变化都来自轨道几何与 backhaul 带宽两个维度。
6. **三项假设（无 ISL / 无站间链路 / 站不共享）**若放松，问题结构会变（作者说算法仍适用），但没有验证。

**8. 和同批其他篇的关系**
- **与全批 DRL 路由论文（CMNCS52M、CYMQ2GLA、EG9X569X 等）是"同一问题的另一半"**：那些论文优化"卫星到卫星的多跳路径"，**明确假设数据要落到地面**；Umbra 优化"从卫星落到地面站再到云"的**最后一跳 + 回传**，而且**明确假设没有 ISL**（L93）。两者在真实系统里是串联的两段。
- 与 **BV4XI6CU（5G 星地负载均衡）问题结构高度相似**：两者都在治"某些地面节点过载、另一些闲置"，但 BV4XI6CU 用**在线启发式规则**（RRUR 阈值 + 迁移），Umbra 用**离线全局最优网络流**；BV4XI6CU 的"卫星"是 GEO 静止的，Umbra 的全部难点恰恰来自 LEO 的**时变可见性**。两篇可以互为对照：一个治静态异构、一个治时变几何。
- 与 **BBNQ4EAQ**共享"用可预测轨道做**离线计划**"这一思路（BBNQ4EAQ 的 netgrid 表、Umbra 的 TLE 预计算），但目标相反：BBNQ4EAQ 求最短**路径**，Umbra 求**时间维上的流量分配**；BBNQ4EAQ 的 contact plan 思路与 Umbra 批评的"计划式路由"同源。
- 与 **BLFJ6CLV（AoI）**有共同度量直觉：两者都在意"数据等多久"，但 BLFJ6CLV 用 AoI 解析、Umbra 用小时级端到端时延，**时间尺度差 4 个数量级**。
- 它引用的 DTN 文献 [30][34][35][46]、时变流 [16][17][40]、卫星时段图 [39][45][47] 都是经典对照；**本批没有一篇引用它**（2023 年，晚于多数）。

**9. 对"负载变化下到达率/时延"的贡献**
**这是本批对"排队时延"贡献最直接、最量化的一篇**，但有重要口径差异：
- **它给了完整的"负载 → 排队 → 时延"因果链和解析式**：Theorem 1（L189–203）把贪心下的平均排队时间写成**与相邻地面站间距的方差成正比**；U_n 的 $\max(\cdot, b_j(t))$ 形式（L135）明确了"到达量 vs 服务速率"的关系。这是可直接复用的结论：**排队的根源是负载的空间不均匀（方差），而不只是负载的大小（均值）**。
- **它给了量化的负载–时延标定**：接触时长 1–7 分钟（众数 6）、单次接触可下载 **10.37–103.48 GB（中位 74.98 GB）**（L278）；150 MB 级队列→小时级时延（中位 6.2–8.8 h、P90 最高 66.5 h）。
- **它给了"容量提升反而更差"的反例**（L280，带宽翻倍 P90 +22%）——这是对"负载变化下时延"最反直觉、最有价值的单条事实，直接反驳"扩容即可"的直觉。
- **但它没有"到达率"这个自变量**：数据生成率由真实影像 trace 决定，**不是可调的到达过程**，也没有 Poisson/自相似等到达模型。它的"负载"是**确定性的、由轨道几何决定的时空分布**。
- 另外它的时延口径是**小时级端到端（采集→到云）**，且**包含"等下一个可见窗口"这种几何等待**，不是链路排队时延本身——与本批其他论文（毫秒/秒级）不可直接比较。

**10. 一句话评价**
把互联网与 sneakernet 领域的**时间扩展网络**首次搬到卫星数据下传场景，并用它**证明了一个反直觉命题：主动闲置链路比用满链路更好**；方法谱系上属于"**把经典网络流用到新场景 + 发现新现象（UQE）**"，理论上干净（有定理、有多项式算法）、实验上扎实（真实 153 星 trace、6 M 影像），但由于**假设无 ISL**、且负载不可调，它与本批的路由类论文是**互补而非竞争**关系。


## CYMQ2GLA — A Two-Hops State-Aware Routing Strategy Based on Deep Reinforcement Learning for LEO Satellite Networks (DRL-THSA)

**1. 一句话**
让每颗星维护**两跳范围内**的链路状态表（用 HELLO 包互通），把每条 ISL 按"预测的队列占用率"分成 Free/Busy/Congested 三档并据此反向要求上游降速，再用**每个目的节点一个 DDQN** 直接由两跳状态输出下一跳；离线训练、星上只推理。

**2. 问题设定**
LEO 星座几十到几百颗星，**"arbitrary flow arrival and uneven traffic load among areas bring about unbalanced traffic distribution"**（摘要 L13；引言 L19 写作"dynamic link states and unbalanced traffic load caused by arbitrary flow arrival and communication hot spots"）。作者点出的两个既有缺陷（L21 逐字）："the packet drop rate at network layer becomes abnormally high, and the cumulative queuing delay during transmission gets non-negligibly large"。
对既有方案的两条具体批评：(a) **TLR [10] 需要全局状态信息**周期性为每个源-目的对算最优路由，"It may cost a lot to collect global state information due to propagation delay between satellites"（L21），因此算出来的路由"cannot be absolutely real-time"；(b) **ELB [9] 没有考虑单条队列**（"did not consider individual queues"），"a part of link congestion still cannot be prevented"（L21）；(c) ELMDR [12] 依赖 mobile agent 回传，**难以跟上状态变化**（L21）。

**3. 方法骨架**
- **拓扑与虚拟节点（第 2.1 节）**：四邻居（两条 intra-plane + 两条 inter-plane）；cross-seam 与南北极区不能建 inter-plane ISL；采用 **Virtual Node (VN)** 策略把运动卫星映射成固定虚拟节点，**把动态拓扑变成静态拓扑**，handoff 时状态信息从旧星搬到新星（L44）。
- **链路状态三档 + 预测（第 2.2 节）**：
  - 用滑动滤波预测平均输入/输出速率：$I_{avg}=(1-\lambda_I)I_{avg}(t-t_c)+\lambda_I I_{avg}(t)$（式 1、2，L60/L64）；**权重 $\lambda_I,\lambda_O$ 按负载动态调**（式 3、4，L70/L74，靠 $\alpha_0,\alpha_1,\alpha_2$ 三个常数夹住）——论文自己说这是"filter"，目的是**滤掉短时轻负载**（L67）。
  - 预测队列占用率 $p=q+\frac{[I_{avg}-O_{avg}]t_c}{L_{max}}$（式 6，L88），当前占用率 $q=L(t)/L_{max}$（式 5）。
  - **阈值也是自适应算出来的**：$T_1=\min(\max(1-\frac{2[I_{avg}-O_{avg}]t_c}{L_{max}},0),1)$，$T_2=\min(\max(1-\frac{[I_{avg}-O_{avg}]t_c}{L_{max}},0),1)$（式 9、10，L108/L112）。$q<T_1$ 为 **FS**，$T_1\le q\le T_2$ 为 **BS**，$q>T_2$ 为 **CS**（L115）。
  - **背压式降速**：进入 BS/CS 就发通知要求邻居把输入速率降到 $I_{avg}\cdot X$，其中 $X=\min(\max(I_s/I_{avg},0),1)$（式 12，L126）；进入 CS 则 $X=0$，**立即停传**（L129）。
- **两跳状态维护（第 2.3 节，Algorithm 1，L149–182）**：每星存 LST（自己的）+ NLST（邻居的）。连通性用 **HELLO/ACK**（周期 $t_h$，超时 $t_d$ 未收到 ACK 则判 off）；状态变化时**广播**给邻居，邻居更新 NLST。
- **MDP 与 DDQN（第 3 节）**：
  - 状态 $S=[N_s,N_d,LST]$，动作 $A=N_{next}$（下一跳），转移概率 $P_{next}=(\sum_{i=1}^m s_i)^{-1}$（式 13）。
  - **奖励**（式 15，L213）：到目的 $r_d$；动作失败/拥塞 $-r_c$；否则 $-dif(N_s,N_d)$，其中 $dif=\alpha(RAAN_s-RAAN_d)^2+\beta\min[|\omega_s-\omega_d|^2,(2\pi-|\omega_s-\omega_d|)^2]$（式 14，L209）——**注意：这是一项纯粹的拓扑位置距离（升交点赤经 + 平近点角），不包含任何队列或时延项**。
  - DDQN（式 16、17，L227/L233）：目标值 $Y^{DDQN}=r+\gamma Q(s',\mathrm{argmax}_{a'}Q_i(s',a';\theta^{online});\theta^{target})$——**这个才是真正的 double 形式**（与同批 CMNCS52M、S85KQ4FC 写出 max 目标的写法不同）。在线网每步更新，目标网每 $N^{target}$ 步硬拷贝。
  - **每个目的节点一个 DDQN**，全网 DDQN 数量 = 卫星数（L259）。
- **离线训练 + 星上推理（第 3.2 节，L220）**：地上仿真训练，训练好的模型存到星上**不再更新**。
- **四种情形的处理（L285–L291）**：链路失效、链路恢复、链路状态变化、**无限环路**。防环做法很工程化：把 $[N_{next},N_d,NLST]$ 再喂一次网络得到"两跳后到达的星"$N_{two}$，**若 $N_{two}==N_c$ 就临时把该方向置为 off 并重算**（Algorithm 3 第 10 步，L277）。
- 作者对开销的论证（L293）：Dijkstra 需要全局路由表更新开销过大，而 DRL-THSA 只用局部两跳信息，**且链路状态变化时不需要重算**（因为 DDQN 已经学过所有情形）。同时承认"**it is not applicable to the networks where the number of disconnected links is destructive**"。

**4. 它声称的效果**
**重要事实：本文正文里几乎没有给出任何数值结果**——4.2.1–4.2.4 全部是"it can be seen that DRL-THSA is lower/higher than ELB, TLR and ELMDR"，数字只存在于 Fig 4–12 的曲线里。可提取的只有定性结论：
- **端到端时延**（Fig 4、5，L310）：DRL-THSA < ELB、TLR、ELMDR。作者给出的原因是它滤掉了短时轻负载，避免 ELB/TLR 被瞬时轻负载骗到拥堵链路上；并且"两跳内换路避免了更多排队时延"。
- **丢包率**（Fig 6、7，L322）：DRL-THSA 最低，ELMDR 最高（因为高负载下回传的路由信息可能过时），ELB 高于 TLR（因为 ELB 不考虑当前跳的拥塞，"packets might be dropped before sending"）。
- **吞吐**（Fig 8、9，L332）：DRL-THSA 最高。
- **流量分布指数**（式 18，L345）：$Index=(\sum x_i)^2/(n\sum x_i^2)$，越大越均匀；DRL-THSA 最好（Fig 10、11）。
- **平均队列占用率**（Fig 12，L356）：在"传输率固定 3.5 Mbps、流数固定 300"这一高负载点上，DRL-THSA **平均队列占用最低**。作者归因于两点：滤掉短时轻负载；**ε-greedy 取 0.9（即 90% 概率随机探索！）**使流量被进一步打散。
- 基线：**ELB [9]、TLR [10]、ELMDR [12]**（L304）。

**5. 实验条件**
NS-3.29，**Iridium-like：66 颗星、6 个轨道面**（L299）。ISL 容量 **25 Mbps**，上下行也 25 Mbps；**平均包长 1 KB**；**队列长度 100 个包**；高度 780 km；极区边界纬度 **70°**；**路由重算周期 600 ms**（Table 4，L302）。
**流量模型**：**200 条 On-Off 流，On-Off 周期服从 shape=1.5 的 Pareto 分布，平均 burst 与 idle 时间都设 500 ms**（L299）。**负载通过两个旋钮扫**：(a) 单流发送速率 **2.5 → 3.5 Mbps**（流数固定 200）；(b) 流数 **200 → 300**（速率固定 3.5 Mbps）（L310）。
DRL-THSA 参数：$\alpha_0=0.02$、$\alpha_1=0.1$、$\alpha_2=0.3$；$t_c=30$ ms；ISL 缓冲 100；$t_s=200$ ms；$t_h=t_d=30$ ms；**ε=0.9**（Table 4）。仿真时长 **60 s**，每个场景**跑 100 次取平均**（L299）。
**训练/评估**：DDQN 在地上训练，但**论文没有给出训练集的生成方式、训练轮数、网络结构、收敛判据**——第 3.2.1 节只给了 Algorithm 2 的伪码（L238–257）。评估在 NS-3 里，与训练环境是否一致**未说明**。

**6. 自述局限（逐字）**
- L293："**However, it is not applicable to the networks where the number of disconnected links is destructive.**"（对大面积断链不适用）
- L293 也自述适用边界："DRL-THSA makes full use of the two-hops link state information which is partially updated. It significantly reduces the updating overhead when only a few link states change."（**只有在少数链路变化时才省开销**）
- L363（结论/未来工作）："In future research, we will study the impact of deep learning network structure and parameter settings on routing strategy performance."——即**当前工作没有做网络结构与参数的敏感性研究**。
- L310 承认一条**反向现象**："the average end-to-end delay of DRL-THSA **increases** with the increasing of flows. Since the congestion of node is tried to be avoided, the packets will be transmitted on another routing path, **which increases the average end-to-end delay**."——即避堵会走更长的路，负载越高时延越差。
- **未见**作者说明：DDQN 的训练细节、训练与评估环境的一致性、"每目的一个网络"带来的模型总量（66 个网络）在星上是否可行（只在 L220 说"limited resources and processing capacity on the satellite"，把训练放地上）。

**7. 它没做但看起来能做的地方（基于内容）**
1. **奖励函数与论文主张不符（最大的一处）**：题目叫"state-aware"，链路状态三档是全文核心机制，但**奖励（式 15）只有 $-dif(N_s,N_d)$ 这一项拓扑距离，完全没有队列、时延或链路状态项**。也就是说 DDQN 是在"往目的地方向走"的引导下训练的，其"避堵"能力只能来自**状态里带了 LST** 这一间接通道。可以做一个直接对照：把 $d$ 型的 hop 时延加进奖励（CMNCS52M 后来正是这么做的，并在 L60 批评本文"**its advantages over a simpler one-hop strategy remain unclear given the additional overhead it introduces**"）。
2. **"两跳 vs 一跳"从未做消融**——CMNCS52M 的 L60 明确点名了这一点，而本文自己也没有任何 one-hop 对照。
3. **ε=0.9 被当成"优点"**（L356：0.9 的 ε 使流量被"autonomously"打散从而降低队列占用）——这在 RL 语义上是**90% 随机动作**，等价于"故意保留大量随机性来均摊流量"。这是一个可疑的解释，值得单独检验：**把 ε 调低后队列占用是否变差？**论文没测。
4. **正文无任何数值结果**（见第 4 项），所有结论只能从图上读——可复现性上是一个明显缺口。
5. **"每目的一个 DDQN"共 66 个模型**，但论文没有报告模型体积、推理时延、星上存储需求——而 L220 恰恰以"星上资源受限"为由把训练放到地上。**推理成本从未被量化**。
6. **四类异常里只做了机制描述，没有各自的单独评测**：链路失效/恢复/状态变化/防环四种情形在 4.2 节里**没有分别给出结果**，只在综合曲线里体现。
7. **60 s 的仿真时长**（L299）与 **600 ms 的重算周期**：60 s 内只有 100 次重算机会，而"滤掉短时轻负载"用的滤波窗口 $t_c=30$ ms——时间尺度上的匹配关系没有讨论。

**8. 和同批其他篇的关系**
- **被 CMNCS52M 直接引用并批评**：CMNCS52M 的文献 [18] 就是本文（L329 逐字："C. Wang, H. Wang, and W. Wang, 'A two-hops state-aware routing strategy based on deep reinforcement learning for LEO satellite networks,' Electronics, vol. 8, no. 9, 2019"），并在 L60 批评"两跳相对一跳的优势不明、开销却增加"。
- **与 CMNCS52M 是同一条技术线的先后两代**：都是"每星一个 agent + 局部观测 + DQN 家族 + 避堵"。差别清晰：CMNCS52M **把排队/传输时延写进奖励**（式 7）、**去掉最大跳数约束**、**扫星座规模**；本文**奖励是纯拓扑距离**、**用两跳状态 + 阈值背压**、**只做 66 星星座**。
- **与 BBNQ4EAQ（netgrid）共享"把动态拓扑静态化"这一手法**：BBNQ4EAQ 用空间立方格，本文用 **Virtual Node**（L44）——两篇是同一思想（把运动卫星映射到固定"位置"）的两种实现，且本文的 VN 思路直接来自 [20][21]（L411/L413）。
- **与 TLR/ELB 的关系是"被它批评又被它当基线"**：TLR 与 ELB 既是本文的两条主要基线（L304），也是 BBNQ4EAQ 和 CMNCS52M 共同引用的经典对照——**这三篇共享同一套祖先**。
- 与 **EG9X569M（鲁棒 DRL 路由）**同属"LEO + DRL 路由"，但本文早 3 年且方法更轻量。

**9. 对"负载变化下到达率/时延"的贡献**
**有直接且具体的贡献——这是本批少数显式扫描负载的论文之一。**
- **两个负载旋钮被显式扫描**：单流速率 2.5→3.5 Mbps、流数 200→300（L310）。这是**可控的负载强度**（不同于 CTWVLBCY 的不可调 trace、CMNCS52M 的"换队列分布图"）。
- **到达过程有明确模型**：**200 条 On-Off 流，ON/OFF 时长服从 shape=1.5 的 Pareto 分布，均值各 500 ms**（L299）。Pareto(1.5) 是**重尾**分布——这意味着突发性强，本身就是"负载变化"的一种刻画。
- **给出了可复用的"负载→拥塞"机制**：式 6（预测队列占用 $p$）+ 式 9/10（自适应阈值 $T_1,T_2$）**把"到达率减服务率 × 检查周期"直接换算成队列占用率的预测**，这是一个干净、可以直接搬用的排队判据。式 12 的降速比 $X$ 是一个**基于负载的背压**机制。
- **给出了"负载升高 → 时延上升"的实测方向**（Fig 5，L310），并且作者**给出了原因**：避堵导致绕路 → 平均时延上升。
- **给出了负载 → 排队占用的实测**：3.5 Mbps × 300 流时 DRL-THSA 的平均队列占用最低（Fig 12，L356）。
- **缺口**：正文无任何数值（只有图），因此**"负载 → 时延"的定量斜率无法从文中取得**；也没有把"到达率"作为独立自变量（ON-OFF 的均值固定 500/500 ms，只靠速率和流数两个旋钮改负载）；链路被假设为**无差错**（L322 逐字："the links between satellites are assumed as error-free. Thus, the packets are dropped when the queue buffer of the satellite is not enough"）——**丢包完全来自缓冲区溢出与 TTL 超时**，这使它的丢包口径与"负载"高度绑定，反而更适合研究负载。

**10. 一句话评价**
"**把链路队列状态做成可通行的三档信号 + 用两跳状态喂 DDQN**"这一组合的早期代表：机制层（自适应阈值、背压降速、HELLO 保活、防环）写得相当完整且工程可落地，但**学习层是薄的**——奖励里没有时延/队列项，训练细节缺失，全部结论只有曲线没有数字，因此它更应该被读作"**状态感知机制 + DQN 作为选路器的拼接**"，而不是一个真正的负载感知学习方案；它后来被 CMNCS52M 明确点名"两跳相对一跳的收益不明"，这一批评基本成立。


## DS9SPARV — OpenSN: An Open Source Library for Emulating LEO Satellite Networks

**1. 一句话**
一个**基于容器虚拟化**的 LEO 星座仿真/仿真平台（不是仿真器而是 emulator，跑真实内核协议栈和真实应用）：把"用户配置"与"容器网络管理"用一个 **KV 数据库**隔开，绕开 Docker CLI 和 Docker Network Manager 直接操纵 Linux 虚拟设备和 netlink，并用 **eBPF/XDP 虚拟链路**替代 Linux bridge，从而在单机和多机上都能高效地搭建/拆解大规模星座、快速切换星地链路。

**2. 问题设定**
LEO 网络研究**没法在真实系统上做实验**（"it is costly to carry out experiments in a real-world SN. Even for those commercial giants like SpaceX and Amazon, it also takes a few years to deploy their LEO constellations"，L17），因此依赖仿真/仿真。但既有平台有三个具体不足（L25）：(a) **对频繁状态变化（ISL 失效/恢复、GSL 切换）的仿真效率不够**，拖慢实验进度；(b) **可扩展性不足**，难以仿 Starlink 这种上千颗的星座；(c) **大多不完全开源**，无法提供可复现的评测平台。
作者进一步把已分类的三类技术路线摆出来（L19–L23）：轨道分析（STK，不做网络协议）、离散事件仿真（流级 StarPerf / 包级 Hypatia 等）、虚拟网络仿真（Mininet 系的 LeoEM、容器系的 StarryNet、VM 系的 Celestial/NEaaS/LORSAT），并指出包级仿真器有两条硬伤（L57）：**事件调度无法并行、耗时长**；**跑不了真实 OS 协议栈**，结果与真实系统有差距。

**3. 方法骨架**
**不是算法论文，是系统/工具论文**。核心是三个组件 + 三处效率改进。
- **架构（第 III.A 节，L77–L87）**：
  - **User-Defined Configurator**：用户写星座参数与规则（ISL 失效模型、GSL 切换策略、轨迹更新）。
  - **Key-Value Database（Etcd）**：中间层，记录机器/节点/链路/应用四类配置（Table III，L97）。**关键设计**：用户配置**不直接传给**容器网络管理器，而是写进 KV 库，由管理器去读——这就是"分离架构"，换来的是可扩展性（L33）。
  - **Container Network Manager**：多机经 VXLAN 互联，含 Container Runtime Manager（容器生命周期）、Virtual Link Manager（虚拟链路）、Message Forwarder（信息中转）。
- **效率改进 1：节点管理（L110）**：用官方 **Docker SDK** 替代 CLI（跳过 shell 与 docker-client 进程）；用**协程池**调度创建/销毁任务，池大小按 CPU 核数确定，避免过度进程切换。
- **效率改进 2：链路管理（L112–L123）**：**跳过 Docker Network Manager**，直接管 Linux 虚拟设备与 network namespace；Docker 建链需三步（建网、连第一个容器、连第二个容器）且每步内部还有解析/取信息等动作，OpenSN**一次调用建链**。
- **效率改进 3：节点与链路创建的依赖编排（L125）**：Docker/StarryNet 要等**所有**容器建好才开始建链；OpenSN 有个 waiting pool，**容器一建好就立刻建它的链路**。
- **多机扩展（第 III.C 节）**：控制面用**加权轮询（Weighted Round Robin）**把实例与链路分派到各机器（Algorithm 1，L148–167）；指令下发靠 Etcd 的 server-push；数据面用 **VXLAN** 跨机传以太帧。
- **eBPF 链路（第 III.D 节，核心创新）**：用挂在 XDP hook 上的 eBPF 程序做**帧重定向**。
  - **机内**：用 eBPF program + map 直接重定向，**完全取代 Linux bridge**；切换时只需**改 redirect map**，不需要删建设备，且**容器接口保持不变**（L196）。
  - **机间**：**直接改目的 MAC**转发，不做以太帧↔UDP 报文的转换（VXLAN 要做）——因为卫星网络链路是**点对点**的，"each source MAC address corresponds to a unique destination MAC address"（L225）。额外好处是**不依赖 Linux 内核的网络层协议**，因此用户可以在其上开发新的网络层架构（L227）。
- **可扩展性（第 III.E 节）**：镜像配置动作**下放给容器内的初始化程序**，因此换镜像不用改仿真器本身（StarryNet 因为用直接函数调用配 BIRD，只能用它那一张镜像，L235）。

**4. 它声称的效果**（这是平台性能指标，不是网络算法指标）
- **建网/拆网**（第 V.A 节，Fig 12，L346）：相对容器系的 **StarryNet 快 6×–10×**；相对 Mininet 系的 LeoEM **略慢**（因为 LeoEM 不跑分布式路由软件）；**eBPF 链路比传统虚拟链路建网快约 10–15%、拆网最多快 2×**。
- **链路状态更新**（第 V.B 节，Fig 14，L365）：GSL 切换配置相对 **Mininet 快 2×（10 个切换）/ 4×（100 个切换）**；**OpenSN 带 eBPF 比不带 eBPF 快 10×（10 个切换）/ 5×（100 个切换）**；规模到 1000 时**不带 eBPF 的版本因并发瓶颈耗时剧增，带 eBPF 的仍保持低耗时**。ISL 时延更新也比 StarryNet 和 Mininet 高效（靠并发执行 + **直接 netlink 交互**）。
- **运行期资源**（第 V.C 节，Fig 15，L373–L406）：三个时期（建网 / 路由收敛 / 稳定运行）。**OpenSN 更早进入稳定期**；StarryNet 在建网期 CPU 只有 10–40% 而 OpenSN 冲到 70%（说明 OpenSN 把资源用上了）；**收敛期 StarryNet 的 CPU 仍高达约 70%**，因为"StarryNet takes the ping command as the daemon process of each container, which will frequently trigger soft interruptions"（L404）；稳定期两者内存相近，OpenSN CPU 更低（用了轻量 daemon，收敛后进 idle）。
- **资源容量影响**（第 V.D 节，L410）：Case A/B/C（32/48/64 vCPU）下，OpenSN 的**路由收敛时间随资源增加而缩短**，而 **StarryNet 几乎不变**。
- **机器数影响**（第 V.E 节，L414–L416）：1 机 / 2 机 / 4 机（总资源相同）下，**机器越多建网与收敛越快**；原因被定位到**内核线程数**——机器越少，单机上平均跑的内核线程越多，建网越慢（Fig 19）。
- **规模验证**（第 V.F 节，L436–L441）：成功仿真 **五层 Starlink 共 4408 颗星**（硬件仅 96 核 / 256 GB），做法是**把每层切成独立 OSPF 区域**并把建网与路由配置分阶段。收敛时刻：Shell V 在 600 s、IV 在 800 s、III 在 900 s、II 和 I 在 1500 s。
- **最低需求**（L250）：**1 vCPU + 2 GB** 即可建 Iridium（6×11）并跑 OSPF。
- 基线：**StarryNet**（容器系）、**LeoEM / Mininet**（Mininet 系）。

**5. 实验条件**
三台 **DELL R7840**（Xeon Gold 5218、各 191.5 GB 内存）。OpenSN 与 StarryNet 用**三 VM 共 48 vCPU / 96 GB**；LeoEM/Mininet 用**单 VM 48 vCPU / 96 GB**（因为它不支持多机，L342）。资源实验另用四 VM 共 64 vCPU / 128 GB。
使用的星座（Table IV，L308）：**Iridium 780 km/11 面/66 星、OneWeb 1200 km/18 面/720 星、Kuiper 630 km/34 面/1156 星、Starlink Shell-I 550 km/72 面/1584 星**，以及 Shell-II~V（合计 4408 星）。内核版本 5.4（Ubuntu 20.04）到 6.8（Ubuntu 24.04）实测，预期兼容 4.1+。
**注意：没有网络流量负载模型。** 路由软件默认 **FRRouting**（支持 OSPF 等，L314）；案例场景是一个**视频流**（CP→卫星网→TU，三个 AS，L239），但不是性能评测的对象。评测指标全是**平台耗时与资源占用**（建网时间、切换时间、CPU/内存），**不是时延、吞吐、丢包**。
**训练/评估**：无学习环节；"评估"就是同一组星座在不同平台上跑，比较耗时。

**6. 自述局限（逐字）**
- L449（未来工作开头）："**The development of OpenSN is still in its early stage.**"
- L453：**"OpenSN is now built on host-centric IP networking architecture, which was initially designed for wired networks."**——即目前只支持 IP 架构，NDN/LIPSIN 等还没支持。
- L451：**收敛时间尚未研究**——"we would like to develop more state-of-the-art routing protocols (e.g., OPSPF and LoFi) on OpenSN, and then **investigate the convergence time in LEO mega-constellations**."（说明当前论文没有做收敛时间研究）
- L455：**"We will isolate the protocol logic from the kernel implementation for OpenSN"**——即新协议还得改内核栈代码。
- L436（规模验证的自述困难）："It poses significant challenges to emulate Starlink constellation with five shells **due to our limited hardware resources**"；为此不得不**把每层切成独立 OSPF 区域**——这是一个**为了跑得动而做的简化**，作者没有评估它对路由行为的影响。
- L320：承认 **LeoEM/Mininet 在若干方面比 StarryNet 和 OpenSN 更高效**（因为它不跑分布式路由软件）——比较并不完全公平，作者做了说明。
- L346：OpenSN 相对 LeoEM 建网是**略慢**的（"slightly increases"）。

**7. 它没做但看起来能做的地方（基于内容）**
1. **它完全没有"网络性能"评测**：全文没有一条关于时延/吞吐/丢包/排队的结果。所有指标都是"多久建好网、切换多快、占多少 CPU"。**平台存在的意义是让别人测这些**，但论文自己没有给出任何一个用它跑出来的网络层结论作示范（唯一的 case study 是视频流，且没有报告性能数字）。
2. **五层 Starlink 案例把每层切成独立 OSPF 区域**（L436）——这是一个**为了绕开硬件限制的路由域切分**，而"分域"本身会对路由最优性有影响。作者只报告了资源曲线，**没有比较分域前后的路径质量**。
3. **"收敛时间"被明确列为未来工作**（L451），而它恰恰是 LEO 路由最关键的指标之一（拓扑一直在变，收敛追不上变化就没有意义）。OpenSN 已经有能力测，只是这篇没测。
4. **没有队列/缓冲区建模**：虚拟链路只管**距离、时延、带宽**（Table III 的 Link 参数），**没有队列长度或丢包模型的配置项**。要做"负载变化下的时延"研究，需要在容器里自己配 tc/netem——平台没有内置。
5. **流量是"用户自己起的应用"**（视频流 case，L239），**没有内置的流量发生器或到达过程配置**（Poisson/ON-OFF/重尾等），也没有负载强度的扫描接口。这与本批其他论文（都要显式设定流量模型）之间的接口是空的。
6. **多机分派用加权轮询**（Algorithm 1），权重是**手工指定的机器权重**，不是按实际负载反馈调整——对异构机器或负载漂移没有自适应。
7. **eBPF 机间链路隐含依赖"点对点、源 MAC 唯一对应目的 MAC"**（L225）——这在卫星 ISL/GSL 上成立，但**一旦引入组播、广播或动态多径转发就不成立**，论文把这一点当成优势说了，却没讨论边界。

**8. 和同批其他篇的关系**
- **它是本批（乃至整个语料）的方法论底层设施**：CMNCS52M 用仿真、CYMQ2GLA 用 **NS-3**、EG9X569M/BBNQ4EAQ 用自研仿真器、CTWVLBCY 用自研离散事件仿真器——**每篇都自带一套仿真器**，OpenSN 正是针对这种不可复现现状提出的。它与这些论文是"工具 vs 使用者"的关系。
- **与 CTWVLBCY 的 CTWVLBCY 明确指出"most SN emulators are not fully open source"**——CTWVLBCY 也自建了仿真器并承诺开源（其 L222），两者是同一痛点的两次回应。
- **与 BBNQ4EAQ 的 LSNS 仿真器**（BBNQ4EAQ 的 L361，基于 ONE 扩展）是同类工作；但 BBNQ4EAQ 是**离散事件仿真**、OpenSN 是**真实协议栈仿真**，粒度不同。
- **引用关系**：OpenSN 的参考文献里有 **ELB [14]、OSPF [12]、LoFi [13]** 等路由工作，以及本批之外的大量 LEO 网络文献（Handley 的 HotNets 系列 [4][6]、Bhattacherjee 的拓扑设计 [8]、Hypatia [27]、StarPerf [26]）。**本批没有一篇引用它**（它 2024/2025 年才发，晚于多数）；它也没有引用本批任何一篇。
- **与 CMNCS52M 的间接关系**：CMNCS52M 引用的 [11]（Internet of satellites）是 OpenSN 作者之一 Ruiz-de-Azúa 的工作，同属一个研究脉络里的邻居。

**9. 对"负载变化下到达率/时延"的贡献**
**没有直接贡献——这是本批里与本主题关系最弱的一篇（除 ETTA3DIV 外）。** 理由具体：
- 全文的因变量是**平台耗时与资源占用**（建网/拆网/切换时间、CPU/内存），**自变量是星座规模与机器配置**（66/720/1156/1584/4408 星；1/2/4 机；32/48/64 vCPU）。**没有"到达率"、没有"排队时延"、没有"丢包"**。
- 它的链路配置项只有**距离、时延、带宽**（Table III），**没有队列**；因此"负载变化"在研究里没有落脚点。
- 唯一沾边的是它**能否支撑**这类研究：由于跑的是**真实内核协议栈**（队列、缓冲区、TCP 拥塞控制都是真的），它**原则上**能给出比离散事件仿真更可信的"负载→时延"数据——这正是它自己主张的价值（"the packet-level simulation results still exhibit differences compared to the real-world system"，L57）。但这是**能力**而不是**贡献**。
- 有一条**间接的可用事实**：**路由收敛时间是可测的**且被点名为未来工作（L451），而收敛时间直接决定"拓扑/负载变化后网络多快恢复到时延基线"——这是通往"负载变化下的时延"的一条现成接口。
- 另一条：**内核线程数会影响建网与操作速度**（Fig 19，L416）——说明**仿真环境的性能本身会随环境负载漂移**，这对任何用仿真器产出的时延数据的可信度是一个提醒（虽然作者只谈建网，不谈数据面）。

**10. 一句话评价**
一篇**系统/工具论文**：不提出任何路由或负载算法，而是用"**KV 库分离配置与容器网络管理 + 绕开 Docker CLI/Network Manager + eBPF 替代 bridge**"三招把容器化 LEO 仿真的效率与规模推上去（6–10× 建网提速、4408 星实测）；它在方法谱系里是**基础设施层**，对"负载变化下到达率/时延"这一具体问题**没有直接贡献**，但它是唯一能让别人那条结论**在真实协议栈上被复现和反驳**的平台，因此它的价值是条件性的：**取决于后续有没有人在它上面做负载实验**。


## DVS8C3CC — On-Demand Routing in LEO Mega-Constellations with Dynamic Laser Inter-Satellite Links

**1. 一句话**
把"**建立一条激光星间链路要花几秒**"这件事当成时延代价写进路由目标函数（而不是像前人那样预先建好静态拓扑），在这个前提下把"什么时候换路"形式化成整数线性规划（NP-hard），再给三个复杂度递增的启发式（ILPR / ALPR / ISASR）在同一个星座上比"平均时延 vs 换路率 vs 计算时间"的取舍。

**2. 问题设定**
LEO 巨型星座开始用**激光星间链路（LISL）**替代射频 ISL（容量 10 Gbps，未来到几百 Gbps 甚至 Tbps，L54）。但**LISL 的建链过程（PAT：指向-捕获-跟踪，见 Fig 1）需要几秒**，而 RF ISL 建链不到 1 ms（L63）。具体数字：**Mynaric 的 CONDOR 首次建链要 30 s，交换轨道参数后约 2 s**；Tesat 与 General Atomics 的终端建链在**数十秒**量级（L83）。
由此产生的基本矛盾（L69、L85）：**当前做法为了躲开建链时延，预先建好静态拓扑并离线算好路由——代价是"链路即使在空闲时也保持激活"，能量效率差**，而且算了过多的路由、占用了星上内存与算力（"they establish more links than necessary (and for longer), and compute an excessive number of routes"，L85）。作者的赌注是：随着 PAT 技术改进，**建链时延会从秒级降到毫秒级**，届时"按需建链 + 按需路由"才变得可行——但那时建链时延就必须作为代价显式进模型。
作者明确指出的文献缺口（L79 逐字）：**"there has been no previous work that takes into account the link setup delay as an important component contributing to latency in routing schemes."**

**3. 方法骨架**
**不是 RL，是组合优化 + 启发式**。
- **网络模型（第 II 节）**：再生载荷、源/目的地面站；距离 ≤ **LISL range** 才能建链 → **非网格网状拓扑（non-grid mesh）**，邻居数随时间变化。用 **虚拟拓扑（N 个快照）**离散时间，每槽内拓扑固定。每条边代价 = 传播时延（边长/c）+ **节点时延**（处理+发送+排队，"node delay is the sum of processing, transmission, and queuing delay"，L112）。
  **关键简化（L112 逐字）**："**we assume a negligible queuing delay in order to explore the effect of LISL setup delay on routing decisions**"——排队时延被显式设为零。
- **SDN 编排（L116）**：地面控制器集中算路并下发 $mathcal{A}^{[i]}$；**假设"两条相邻路由的时间戳间隔 > 算路+下发时间"**，即新路由总能提前就位。**卫星不留备用光终端**（为省 SWaP），因此**换路必然产生一次建链时延 $eta_s$**；且 $eta_s$ **只计一次**（因为新链路可并行建立）。
- **ILP 形式（第 III 节）**：目标式 11a = 时延项 + 惩罚项，代价函数为
  $\overline{\eta_{LE}} = \overline{\eta_{delay}} + \frac{\eta_s}{100}\lambda$（式 10，L180）——**这是全文最核心的一条关系：平均端到端时延 = 平均传播/节点时延 + 建链时延 × 换路率**。
  换路率 $\lambda = \frac1N\sum_{i=1}^{N-1}(1-\sum_r \alpha_r^{[i]}\alpha_r^{[i+1]})\times100\%$（式 9）。因为目标里有**两个二值变量的乘积**，先是非线性整数规划，用 $\beta_r^{[i]}\le\alpha_r^{[i]}$、$\beta_r^{[i]}\le\alpha_r^{[i+1]}$、$\beta_r^{[i]}\ge\alpha_r^{[i]}+\alpha_r^{[i+1]}-1$（式 12d–f）线性化后成 **ILP，NP-hard**（L223）。
- **四个算法（第 IV 节）**——两个正交维度：**怎么选路**（瞬时 vs 平均）× **保持多久**（每槽重选 vs 保持到断）：
  1. **ILSR**（基线）：每个时隙跑一次 Dijkstra（瞬时最短），复杂 $O(N(V+E)\log V)$。**不感知 $\eta_s$**。
  2. **ILPR**：首次跑 Dijkstra 选最短，**只要这条路由的边还在就保持不变**，断了才重算（Algorithm 1）。复杂度同 ILSR 量级。**不感知 $\eta_s$**。
  3. **ALPR**：**感知 $\eta_s$**。只枚举**边不相交（disjoint）**的候选路由（用"求最短→删其所有边→再求最短"迭代得到，L272），对每条算**含 $\eta_s$ 的平均时延** $\overline{\eta}_r^{[i]}=\frac{1}{l-i+1}(\eta_s+\sum_{k=i}^{l}\delta_r^{[k]})$（式 13），选最小者并保持到它失效。复杂度最坏 $O(NV(NV+(V+E)\log V))$。
     **论文给了一个很好的直观例子（Table II）**：4 条路由，$\eta_s=1$ ms 时选瞬时最优的 Route 1（均值 26.98 > 但）…；$\eta_s=1000$ ms 时改选**存在时间最长**的 Route 2（均值 118.84 最优）——**$\eta_s$ 一变，最优路由就换人**。
  4. **ISASR**：**感知 $\eta_s$** 且**每槽重选**。把每条边的代价改成 $cost_{mod}=cost_{old}+\gamma\{cost_{st}+cost_{act}\}$（式 14）：$cost_{st}$ **正比于 $\eta_s$、反比于该边剩余存活时隙数**（式 15 分段定义，边一旦过期设 $\infty$）；$cost_{act}$ 对**已激活**的边设 0、未激活的设 $\eta_s$。还会**把 $cost_{st}\ge cost_{thrsh}$ 的星间边从搜索空间删掉**（但保留所有 GS-卫星边以免失联，L327）。算完再跑 DSR。复杂度 $O(N(NE+(V+E)\log V))$。
  - **$\gamma$ 的选取（第 V.C 节）**：$\overline{\eta_{LE}}$ 关于 $\gamma$ **是凸的**（Fig 5），**最优 $\gamma$ 随 $\eta_s$ 增大而增大**，因此作者直接取 $\gamma=\eta_s$；并说明"找最优 $\gamma$ 超出本文范围，可用梯度下降之类的递归方法"。

**4. 它声称的效果**（图表为主，正文同样缺少成体系的数值）
- **平均端到端时延 vs $\eta_s$**（Fig 3，L379）：$\overline{\eta_{LE}}$ 随 $\eta_s$ 单调上升（对所有算法）；**除 $\eta_s$ 极小时，ILSR 最差**（因为它不感知 $\eta_s$）；**ISASR 在所有 $\eta_s$ 下最好**；**$\eta_s=1$ ms 时 ILSR 反而略优于 ILPR 和 ALPR**（因为后两者"黏"在旧路由上而换路代价已经很小了）。**NY-Hanoi 的平均时延高于 NY-London**（更长的连接 → 传播+节点时延更高、跳数更多、路由更易断 → $\lambda$ 更高）。
- **时延分解**（Fig 4，L388）：ILPR/ILSR 的 $\overline{\eta_{delay}}$ 与 $\lambda$ **不随 $\eta_s$ 变化**（不感知）；ALPR/ISASR **$\eta_s$ 高时牺牲 $\overline{\eta_{delay}}$ 换低 $\lambda$**，$\eta_s$ 降低时重点回到 $\overline{\eta_{delay}}$。ALPR 在中等以上 $\eta_s$ 时 $\overline{\eta_{delay}}$ 最大，ISASR 的 $\lambda$ 最小。
- **计算时间**（Fig 6，L404）：**ILPR 最省、ISASR 最贵**，且**复杂度越高性能越好**——"the higher the complexity, the better is the performance"。ILSR/ILPR 的计算时间不随 $\eta_s$ 变；ALPR 与 ISASR **$\eta_s$ 越大计算时间越低**（因为越倾向选长期稳定的路由，算法被调用的次数越少）。ISASR 内部还发生一次**反常的此消彼长**：$\eta_s$↑ → $cost_{st}$↑ → 删除更多边（$\tau_1$↑），但搜索空间变小使代价修改 $\tau_2$ 与 DSR $\tau_3$ 下降，**总体计算时间反而下降**。
- **中断概率**（Fig 7–11，L414–L416）：**瞬时端到端时延的直方图是双峰的**——**低时延那一坨是"没有换路"的时刻，高时延那一坨是"发生换路"的时刻，两坨之间的间隔量级正好是 $\eta_s$**（L414 逐字："The portion with lower end-to-end latencies are the occurrences where there is no route change, and higher end-to-end latencies are those with the route change events. In addition, the latency gap between these two portions is in the order of $\eta_s$ value"）。在中高 $\eta_s$（10/100/1000 ms）下，**中断概率基本上就等于换路率**；$\eta_s=1$ ms 时两坨重叠，这个对应关系失效。
  QoS 阈值取 $\eta_Q=$ 40/35/30/27 ms 对应 $\eta_s=$ 1000/100/10/1 ms（L416）。
- **平均抖动**（式 16，Fig 12，L453）：抖动 = 相邻时隙时延差的绝对值平均。$\eta_s$ 越大抖动越大；ILSR 抖动最大；中高 $\eta_s$ 下 ISASR 抖动最小，**但 $\eta_s$ 很小时 ISASR 反而比 ILPR/ALPR 差**（因为它换路更频繁）。
- 基线：**ILSR**（用时隙化的瞬时 Dijkstra，即"现状"）。
- **未给绝对数值**：全文结论均为曲线与相对比较，**平均时延的具体毫秒数、计算时间的具体秒数都只在图里**。

**5. 实验条件**
**Starlink Phase I version 2：1584 颗星、24 个轨道面 × 66 颗、高度 550 km、倾角 53°**（Table III，L367）；卫星速度 7.6 km/s；**LISL range 1500 km**、**GS range 1000 km**（作者说明 Starlink Phase I v2 的最大 LISL 距离是 5016 km，取 1500 km 是为了**保证不受地球遮挡**，L375）；**节点时延 1 ms**；**N = 600 个时隙，每槽 1 秒**；$cost_{thrsh}=100$；$\gamma=\eta_s$。
用 **Ansys STK** 生成星座并**与 Python 接口**导出 600 槽的顶点/边/边长数据，算法在 Python 里跑（L375）。**两个洲际连接：纽约-伦敦与纽约-河内**。仿真机：2.3 GHz i5 + 20 GB RAM。计算时间记录 **100 次迭代的平均**（L404）。
**关键简化（L375 逐字三条）**：
- "Considering very high data rate (tens of gigabits per second) LISLs, **the transmission delay is assumed to be negligible**."
- "**as congestion is beyond the scope of this paper, queuing delay is not considered**."
- 处理时延取 1 ms，故每颗星节点时延 = 1 ms。
**训练/评估**：无学习环节；评估即四个算法跑同一批 STK 导出的数据集。

**6. 自述局限（逐字）**
- **排队与拥塞被显式排除**（L375）："**as congestion is beyond the scope of this paper, queuing delay is not considered**"；第 II 节同样说明"we assume a negligible queuing delay in order to explore the effect of LISL setup delay on routing decisions"（L112）。
- L392（$\gamma$）："**Finding and using the optimal $\gamma$ in ISASR is beyond the scope of this study**, and one can easily build a recursive model such as gradient descent to find the optimal $\gamma$."
- L414：**所提算法不是为最坏时延设计的**——"**Although the proposed algorithms are not designed to handle worst-case delays**, we compare these algorithms from the outage probability perspective..."
- L116：**初始配置时延被排除**——"Although this initial configuration imposes a delay on the communication in the very beginning, **it can be considered as a configuration mode, which is beyond the scope of this paper**."
- L116：**假设所有 LISL 的建链时延相同**，与相对速度无关——"For the sake of simplicity, we assume the same LISL setup delay value to establish any new LISL irrespective of the relative velocity between the associated nodes."
- 未来工作清单（L465–L473）本身即自我承认的空白，逐条：**排队时延 + 用 ML 预测拥塞**；**异构建链时延**（不同代际/公司/轨道相对速度不同）；**多源多目的（site diversity）与不同流量负载**；**最坏时延与抖动优化**；**用非不相交的有限路由集替代只考虑 disjoint 路由**。

**7. 它没做但看起来能做的地方（基于内容）**
1. **排队时延被设为零**（L375、L112）——而作者自己在未来工作里第一条就说要把队列状态和 ML 拥塞预测加进来（L465）。**这几乎是明写的下一步**：把 $\eta_{LE}=\overline{\eta_{delay}}+\frac{\eta_s}{100}\lambda$（式 10）里的 $\overline{\eta_{delay}}$ 换成含排队的项，问题就变成"建链代价 vs 拥塞代价"的联合优化。
2. **$\gamma$ 直接取 $=\eta_s$ 而没有优化**（L392）：作者证明最优 $\gamma$ 随 $\eta_s$ 增大（Fig 5 是凸的），却把寻优留给了未来——**这是一个现成的、收益可测的空位**。
3. **ALPR 只考虑边不相交路由**（L272），作者承认这可能漏掉更好的路由（"there may exist a better route that shares edges between two disjoint routes, and due to considering only the disjoint shortest routes, we may lose a better route by not even considering it"，L309），并在未来工作里列出。
4. **只有两条洲际连接（NY-London、NY-Hanoi）**（L375）——样本量极小，没有做"连接长度/纬度分布"的系统扫描，而这直接决定 $\lambda$ 与跳数。
5. **$\eta_s$ 被假设为全网统一常数**（L116），未来工作里承认现实中会异构——**这是模型里最容易松动也最有现实意义的假设**。
6. **没有真正的流量维度**：全文只有"一个源-目的 GS 对、一条活跃路由"（L114 逐字："Considering a scenario with one source-destination GS pair connection in the network, only the edges associated with a particular route r will be active"）。**多流并存时的链路争用完全没建模**——而"按需建链"的现实吸引力恰恰来自多流共享终端资源。
7. **ISASR 删边用固定阈值 $cost_{thrsh}=100$**，正文说这是"观察 $cost_{st}$ 直方图后选的、以便**不删任何边**、展示 ISASR 的最高性能"（L375）——**这个参数在实验里被调成了什么都不做**，因此**删边带来的复杂度收益实际上没有被评估**（除第 V.D 节为做对比才固定为 1，L404）。

**8. 和同批其他篇的关系**
- **与 CTWVLBCY（Umbra）最像，也最值得对照**：两篇都是"**离线/集中式计划 + 时变拓扑 + 目标函数里有时延与切换代价的权衡**"，都用**时间离散化**（Umbra 用 TEN 的时隙层，本文用 N 个快照）。差别在于：Umbra 的代价是**地面站的排队**，本文的代价是**光链路的建链时延**；Umbra 用网络流求全局最优，本文用 ILP + 启发式求单流最优。
- **与 BBNQ4EAQ 共享"虚拟拓扑/快照"思想**：BBNQ4EAQ 用 netgrid 与 beacon 做时间连续模型，本文用 N 快照的虚拟拓扑（引 [34–36]）——**两篇都在治"离散化粒度 vs 精度"这个病**，且 BBNQ4EAQ 明确承认静态拓扑假设在路由时间长时非最优，本文的 $\lambda$ 恰好是对这个代价的量化。
- **与 CMNCS52M / CYMQ2GLA / EG9X569M 是"集中式 vs 分布式"的对立面**：那三篇坚持**分布式、只用局部信息**（CMNCS52M 的 L46 明确说集中式"infeasible due to excessive communication overhead"），本文明确采用 **SDN 集中式控制器**（L116）并假设"算路+下发总能赶在需要之前完成"。**这是本批里对"集中式可接受"这一立场最明确的论文**，正好可以做反面参照。
- 与 **DS9SPARV（OpenSN）**互补：OpenSN 是评测平台，本文的算法（尤其 ISASR 的删边逻辑与 Dijkstra 调用次数）是一个天然的 OpenSN 实验负载。
- **本批没有一篇引用它**（2024 年发表，晚于本批多数）；它引用的 [27]（RL 排队/带宽感知去中心化路由）与 [24–26]（拥塞排队时延）是本批 DRL 路线的邻居。

**9. 对"负载变化下到达率/时延"的贡献**
**对"时延"有直接贡献，对"负载/到达率"没有贡献，而且作者是明确排除的。**
- **有贡献的一面（可复用的事实与形式化）**：
  1. **式 10 $\overline{\eta_{LE}}=\overline{\eta_{delay}}+\frac{\eta_s}{100}\lambda$**：把时延拆成"**连续项 + 离散事件项**"，并指出**离散事件项 = 单次切换代价 × 切换频次**。这是一个可以直接搬到"负载变化"场景的形式：把 $\eta_s$ 换成"排队时延"，就得到"负载项 + 切换项"的同类结构。
  2. **双峰时延直方图**（L414）：**时延分布的形状由"是否发生换路"这一离散事件决定，两峰间隔恰为 $\eta_s$**。这条事实的推广形式很重要：**在多变的网络里，端到端时延可能不是被"负载的连续变化"支配，而是被"离散的拓扑/路由事件"支配**——这与本批多数论文默认的"时延随负载连续上升"的图景是冲突的，值得单独检验。
  3. **"中断概率 = 换路率"这一等价关系**（L416，在中高 $\eta_s$ 下）：说明**尾时延的成因可归因于切换事件计数**。
  4. **切换代价 × 切换频次的权衡有最优工作点**：$\eta_s$ 小则频繁换路（追瞬时最优）更划算，$\eta_s$ 大则黏住稳定路由更划算，**交叉点在 $\eta_s=1$ ms 附近**（Fig 3 的 zoom-in）。
- **没有贡献的一面**：
  - **排队时延被显式设为零**（L375、L112），**没有负载、没有到达率、没有缓冲区、没有拥塞**。
  - **网络里只有一条流**（L114），因此**没有多流争用**，也就没有"负载"的落脚点。
  - **发送时延也被假设可忽略**（L375，因 LISL 速率达数十 Gbps）——这进一步抽掉了"负载 → 时延"的通道。
  - 因此：本篇提供的是"**拓扑事件驱动**"的时延图景，而"**负载驱动**"的时延在本篇里被**结构性地删掉了**。作者自己在未来工作第一条（L465）承认并指定了补法。

**10. 一句话评价**
**首次把"光链路建链时延"作为一等时延代价引入 LEO 路由**，并用一条极简关系式（式 10）把问题变成"**平均时延 vs 换路率**"的两项权衡，再给出一条从轻到重的启发式谱系（ILPR→ALPR→ISASR）供按 QoS 预算选型；方法谱系上属于"**把经典最短路/ILP 用到新代价项上**"，理论干净、取舍讲得清楚，但其代价是**把排队与多流全部抽掉**——因此它回答的是"**切换代价有多大**"，而不是"**负载变化下时延怎么变**"，与本主题是相交而非覆盖的关系。


## E4NYGLGX — Safe and efficient off-policy reinforcement learning (Retrace(λ))

**1. 一句话**
把 IS、$Q^\pi(\lambda)$、TB(λ) 三种 off-policy return-based 算法写成**同一个算子形式**（式 3，区别只在 trace 系数 $c_s$），然后取 $c_s=\lambda\min(1,\pi/\mu)$ 得到新算法 **Retrace(λ)**——它同时做到"**方差低**、对任意 off-policy 程度**安全收敛**、在近似 on-policy 时**不浪费样本**"，并**首次**证明了无 GLIE 假设的 return-based off-policy 控制收敛，顺带补上了 1989 年以来悬空的 **Watkins' Q(λ) 收敛性证明**。

**2. 问题设定**
强化学习里一个根本权衡（L15）：**Monte Carlo 式 return 方法**与函数逼近结合时行为更好、探索传播更快，但**难以用到 off-policy 数据**；**自举（bootstrap）方法**容易处理 off-policy 数据，却在其他方面吃亏。作者要证明"**从 return 学习**"与"**off-policy 学习**"不必互斥。
已有的三条路线各有硬伤：
- **IS（重要性采样）**：$c_s=\pi/\mu$，理论对任意 $\pi,\mu$ 都收敛，但**方差可能极大甚至无穷**（"IS estimates can suffer from large – even possibly infinite – variance"，L79），因为它是 $\pi/\mu$ 连乘。
- **$Q^\pi(\lambda)$ / $Q^*(\lambda)$（Harutyunyan 等 2016）**：$c_s=\lambda$，方差低，但**只在 $\mu$ 与 $\pi$ 足够接近时**才在 $Q^\pi$ 附近收缩——条件是 $\lambda<\frac{1-\gamma}{\gamma\varepsilon}$，其中 $\varepsilon:=\max_x\|\pi-\mu\|_1$（L81）。作者直说这在控制场景下"**not safe**"，因为控制里目标策略是对当前 Q 贪心的，$\mu$ 与 $\pi$ 天然会拉开（L17）。
- **TB(λ)**：$c_s=\lambda\pi(a_s|x_s)$，对任意 $\pi,\mu$ 都安全，但**在 near on-policy 情况下会过早截断 trace**，用不上完整 return（L83）。

**3. 方法骨架**
**纯理论 + 一个算法，不是应用论文。**
- **统一算子（式 3，L74）**：
  $\mathcal{R}Q(x,a):=Q(x,a)+\mathbb{E}_\mu\big[\sum_{t\ge0}\gamma^t\big(\prod_{s=1}^{t}c_s\big)\big(r_t+\gamma\mathbb{E}_\pi Q(x_{t+1},\cdot)-Q(x_t,a_t)\big)\big]$
  ——**四种算法的差别全在 $c_s$**（Table 1，L93）：IS 用 $\pi/\mu$；$Q^\pi(\lambda)$ 用 $\lambda$；TB(λ) 用 $\lambda\pi(a_s|x_s)$；**Retrace(λ) 用 $\lambda\min(1,\pi(a_s|x_s)/\mu(a_s|x_s))$**。
- **Retrace 的直觉（L85）**：重要性比**截断在 1**——既不像 IS 那样方差爆炸，又在 on-policy 时**不截断**（因为 $\min(1,\cdot)$ 在 $\pi\approx\mu$ 时接近 1），off-policy 时**安全截断**；且 $\min(1,\pi/\mu)\ge\pi$，所以**截得比 TB(λ) 少**。
- **三个定理**：
  - **Theorem 1（策略评估）**（L107）：只要 $c_s\in[0,\pi/\mu]$，$\mathcal{R}$ 就以 $Q^\pi$ 为唯一不动点且是 $\gamma$-压缩：$\|\mathcal{R}Q-Q^\pi\|\le\gamma\|Q-Q^\pi\|$，**对任意 $\pi,\mu$**。
  - **Remark 1（L141）**：更精细的结论是**状态-动作相关的压缩系数** $\eta(x,a)\in[0,\gamma]$，$|\mathcal{R}Q-Q^\pi|\le\eta(x,a)\|Q-Q^\pi\|$；$c_1=0$（立即截断）时 $\eta=\gamma$，学完整 return（$c_t\approx1$）时**可以接近 0**。
  - **Definition 1（L153）**：引入**"increasingly greedy"策略序列**——$P^{\pi_{k+1}}Q_{k+1}\ge P^{\pi_k}Q_{k+1}$；$\varepsilon_k$-greedy（$\varepsilon_k$ 不增）与 softmax（温度不增）都属于此类（Lemma 2、3，Appendix B）。
  - **Theorem 2（控制）**（L165）：$Q_{k+1}=\mathcal{R}_kQ_k$ 下，$\|Q_{k+1}-Q^*\|\le\gamma\|Q_k-Q^*\|+\varepsilon_k\|Q_k\|$；**只要 $\varepsilon_k\to0$ 就 $Q_k\to Q^*$**。关键：**行为策略 $\mu_k$ 完全任意**。
  - **Theorem 3（在线算法）**（L217–L225）：给出每访形式的在线更新式（式 7），$Q_{k+1}(x,a)\gets Q_k(x,a)+\alpha_k\sum_{t\ge s}\delta_t^{\pi_k}\sum_{j=s}^{t}\gamma^{t-j}\big(\prod_{i=j+1}^{t}c_i\big)\mathbb{I}\{x_j,a_j=x,a\}$，并证明 a.s. 收敛到 $Q^*$。
- **核心卖点（L253）**：**Theorem 3 不需要 GLIE 假设**——作者称这是"**第一个**不需要 GLIE 的 λ-return（$\lambda>0$）收敛结果"；作为推论（L255）**首次证明 Watkins' Q(λ) a.s. 收敛**。
- **$c_s$ 的选取权衡（第 4.1 节，L237–L243）**：**低方差**要求 $c_s$ 小（且 $\mathbb{V}(c)<1/\gamma^2$，这直接排除了 IS），**快收缩**要求 $c_s$ 大（$c_s=1$ 时一步到位）；**Retrace(λ) 是这个权衡的折中**。
- **一个未证明的推广**（式 9，L248）：放松 Markov 假设后可以**在时间上互相补偿**——某一时刻用小 trace、另一时刻用大于 1 的 trace，只要乘积 < 1：$c_s=\lambda\min(\frac{1}{c_1\cdots c_{s-1}},\frac{\pi(a_s|x_s)}{\mu(a_s|x_s)})$。作者明确说这条**只在策略评估下被证明**（L245）。

**4. 它声称的效果**
**理论结论 + Atari 实验，与网络/时延无关。**
- **理论**：Theorem 1（$\gamma$-压缩，任意 $\pi,\mu$）、Theorem 2（控制收敛，任意行为策略）、Theorem 3（在线 a.s. 收敛，无 GLIE）；推论：Watkins' Q(λ) 收敛。
- **实验条件（Appendix F，L676）**：60 个 Atari 2600 游戏（ALE）；**16 线程 CPU 异步**（沿用 Mnih 2016 的框架），每线程私有 replay **62,500 transitions**（DQN 总容量的 1/16）；Shared RMSprop，步长退火到 0 共 $3\times10^8$ 帧；$\varepsilon$ 每 50 000 帧按概率 0.3/0.4/0.3 在三套退火表之间随机切换；**每个配置跑 4 个随机种子取平均**；minibatch 64；Retrace/TB/$Q^*$ 用 **4 条 16 步序列**的 minibatch。
- **结果（Table 2，L684）**：$\lambda$ 从 0.0 扫到 1.0。**Retrace 在每一个 $\lambda$ 上都不比 TB 差**（"Retrace always achieve a score higher than TB"）；**$\lambda=0.9$ 时 Retrace 0.9034 为全表最高**（TB 0.7753、DQN 0.7256、$Q^*$ **0.02926**）；$\lambda=1.0$ 时 Retrace 0.8698、TB 0.8158。**$Q^*(\lambda)$ 在 $\lambda\le0.5$ 时最好（0.8419）但 $\lambda>0.5$ 后崩塌**（0.0293、0.0432）——作者据此说它"**also not safe**"，且"the safe threshold of $\lambda$ is likely to be problem-dependent"（L682）。
- **正文的对比陈述（L286）**：Retrace 与 TB 都**大幅优于 Q-Learning**；Retrace 相比 TB 的优势"**narrower but still marked**"，在 **30 个游戏上最好，TB 拿下其余 15 个**。
- 基线：**DQN / one-step Q-learning**、**TB(λ)**、**$Q^*(\lambda)$**。

**5. 实验条件**
**与 LEO 网络、路由、负载、到达率毫无关系。** 环境是 **Arcade Learning Environment 的 60 个 Atari 2600 游戏**；"life lost" 视为 episode 终止（L678）；reward 裁剪到 $[-1,1]$；多步算法里把量裁剪到 $[-1,1]$ 后再除以序列长度（L678）。超参在 8 个游戏（Asterix, Breakout, Enduro, Freeway, H.E.R.O, Pong, Q*bert, Seaquest）上做**先粗后细的对数扫描**（L678）。
**训练/评估**：4 个随机种子平均；用 Bellemare 等的 **inter-algorithm score**（把每游戏在参与比较的算法集合内归一化到 [0,1]）——**注意作者自己警告"average scores are not directly comparable across different values of λ"**（Fig 2 图注，L689），因为每个 $\lambda$ 下的 worst/best 不同。**没有跨分布或跨任务泛化评估。**

**6. 自述局限（逐字）**
- L272（**Open questions**，逐字两条）："**(1) Removing the technical assumption that $P^{\pi_k}$ and $P^{\pi_k\wedge\mu_k}$ asymptotically commute, (2) Relaxing the Markov assumption in the control case in order to allow trace coefficients $c_s$ of the form (9).**"
- L245：式 9 的推广"**only the result for policy evaluation has been proven so far**"。
- L225：Theorem 3 的收敛证明**依赖一条"相当技术性"的额外假设**——"we make the additional (rather technical) assumption that $P^{\pi_k}$ and $P^{\pi_k\wedge\mu_k}$ commute at the limit"，虽然对 $\varepsilon$-greedy 等成立。
- L259（**代价**）："**Unlike Retrace(λ), $Q^\pi(\lambda)$ does not need to know the behaviour policy $\mu$.**"——即 Retrace **必须知道行为策略**用于所选动作的概率；L261 指出 TB(λ) 同样不需要。
- L268：$\mu$ 未知时可以**用样本估计 $\hat\mu$ 代替**（引用了一篇文献，但该处引文在转写里显示为 "?"，说明原文引用信息在此版本中缺失）。
- L682：$Q^*(\lambda)$ 的**安全 $\lambda$ 阈值"likely to be problem-dependent"**——这是对整类算法（包括它自己 $\lambda$ 取值）的一条自述性警告。

**7. 它没做但看起来能做的地方（基于内容）**
1. **"知道 $\mu$ 才能算 trace"这一条是落地成本**（L259）：在经验回放里 $\mu$ 是当时的行为策略，需要额外存储每一步行为策略的概率。**论文没有讨论存储/计算开销**——在星上资源受限场景（本批多篇论文反复强调）这是一个实际的接口问题。
2. **Theorem 3 的两条假设（渐近可交换、Markov trace）都没被放松**（L272），且作者承认是"相当技术性"的——**这是纯理论遗留**，与应用无关但影响算法在其变体下的可用性。
3. **只测了 Atari**（L678）：一个**确定性、离散动作、单智能体**的基准（作者自己在 L682 里说 $\lambda=1$ 至少在**确定性环境**下合理）。**完全没有测多智能体、非平稳环境或连续动作**——而 Theorem 1/2 声明可扩展到连续动作空间（L270），却**没有对应的实验**。
4. **没有与"多步目标 + 函数逼近"的稳定性理论挂钩**：实验里 reward 与 target 都做了裁剪（L678），这是一个**工程补丁**，论文没有把它纳入理论分析。
5. **$\lambda$ 的选择没有给出原则**：Table 2 显示 Retrace 各 $\lambda$ 都不差，但**为什么 $\lambda=0.9$ 最优、$\lambda=1$ 次之，没有解释**；作者只给了"Retrace 下 $\lambda=1$ 合理"这一句经验判断（L682）。
6. **没有报告方差**：论文核心主张之一是"**low variance**"，但实验里**只报了 inter-algorithm score（性能），没有报 trace 的方差或更新的方差**——主张与证据之间缺一条直接测量。

**8. 和同批其他篇的关系**
- **它与本批其余 10 篇毫无主题关系**：那些是 LEO 网络（路由/调度/负载均衡/仿真平台/AoI），这一篇是**纯 RL 理论**（NIPS 2016，DeepMind）。
- **它在语料里的位置是"算法祖先"**：本批中大量使用 DQN/DDQN 的论文（CMNCS52M、CYMQ2GLA，以及 S85KQ4FC、EG9X569M 等）所用的自举式 Q-learning 家族，其收敛性问题正是本文所处理的；但**本批没有任何一篇引用 Retrace(λ)**——我通读的 6 篇 LEO 论文（BBNQ4EAQ、BLFJ6CLV、BV4XI6CU、CMNCS52M、CTWVLBCY、CYMQ2GLA、DS9SPARV、DVS8C3CC）的参考文献里都没有 Munos 或 Retrace。它们用的都是 **DDQN + 经验回放 + 目标网**（CMNCS52M 的 L131、CYMQ2GLA 的 L224），即**单步 off-policy**，而不是 λ-return。
- **一个值得注意的反差**：本批多篇论文自称"DDQN"却写出 max 目标（S85KQ4FC 式 17、CMNCS52M 式 5），只有 CYMQ2GLA 式 17 写对了 double 形式——**而 Retrace 关心的正是这类 off-policy 目标值的偏差与收敛问题**。这篇论文恰好是那个"目标值该怎么写才安全"的问题的**理论权威出处**（虽然 DDQN 本身出自 van Hasselt，不是本文）。
- 与 **DS9SPARV（OpenSN）** 的关系：两篇都是"**给别人的研究提供基础**"的论文（一个是平台，一个是理论），都不解决具体的 LEO 问题。

**9. 对"负载变化下到达率/时延"的贡献**
**没有直接贡献。** 具体理由：
- 全文的**状态空间是 Atari 的游戏画面**，**奖励是游戏分数**，**没有网络、没有队列、没有到达过程、没有时延**。搜索全文，"queue/arrival/delay/latency/congestion" 这些概念**一个都不存在**（除 "delay scheduling" 之类无关词外）。
- 它的因变量是**"算法能否收敛、收敛多快、样本效率多高"**，自变量是 **$\lambda$、$\pi$ 与 $\mu$ 的差距、trace 截断方式**——全是 RL 内部量。
- **唯一可迁移的间接线索**：Theorem 1 的 Remark 1（L141）指出**压缩系数 $\eta(x,a)$ 是状态相关的**，且在"学到完整 return"时可以远小于 $\gamma$。若把 LEO 路由建模成 RL，这提示**不同网络状态下的收敛速度天然不同**（例如拥塞态与空闲态的收敛速度不同）——但**这是我从数学形式做的外推，论文本身完全没有谈到任何网络语义**，不应算作它的贡献。
- 同样地，Theorem 3 的"**不需要 GLIE**"对 LEO 场景有一层潜在意义：当网络持续非平稳时，行为策略不必渐近贪心——**但论文的例子全是 Atari，作者没有讨论非平稳环境**。

**10. 一句话评价**
**语料里的"工具书"型论文**：方法谱系位置是"**为 off-policy return-based RL 提供一个统一算子框架，并给出 Retrace(λ) 这一安全且高效的折中点 + 三条收敛定理**"，其价值（λ-return 在任意 off-policyness 下的安全性、无 GLIE 收敛、Watkins Q(λ) 收敛的补证）在 RL 领域是奠基性的；但**对"负载变化下的到达率/时延"这一具体问题，它的贡献是零**——本批出现它，只能说明语料在收集 LEO 路由工作的同时把 RL 理论源头一并纳入了，而**这一批 LEO 论文实际上并没有用到 Retrace**（它们停在 DDQN 单步自举）。


## EG9X569M — A Robust Routing Strategy based on Deep Reinforcement Learning for Mega Satellite Constellations (RRS-DRL)

**1. 一句话**
用 DQN 做 LEO 巨型星座的抗干扰路由，**把 AoI（信息年龄）而不是时延写进奖励**，并把"干扰"建模成**链路性能退化（而不仅仅是断链）**，让 agent 通过试错学会避开受扰链路；奖励 = 距离惩罚 + AoI 惩罚 + 队列增长率惩罚的加权和。

**2. 问题设定**
巨型星座（Starlink/OneWeb/Kuiper）下路由面临两类威胁（L23、L27）：**恶意干扰会让整个网络瘫痪**，以及用户数增长带来的**负载上升与拓扑变化**，路由表规模膨胀浪费星上资源。
作者对既有工作的三条具体批评（L27）：
- 文献 [3] 的 RL 路由"**assumes that the network topology is static and free from being jammed, which is clearly unrealistic**"；
- 文献 [4] 的 DRL 全局路由"**is simply used for the problem of finding path, without considering the load balancing problem arising from the degradation of link performance when subjected to continuous disturbances**"；
- 文献 [5]（DRL-ER 能效路由）"**Lack of consideration for jamming**"。
作者自己的定位（L29）：**把干扰的先验信息放进状态**，并**同时考虑链路失效与链路性能退化**，让策略"be aware of jamming through trial and error"。

**3. 方法骨架**
- **网络模型（L35）**：图 $G=\{\eta,\mathcal{L}\}$，边权 $e_{ij}=\lambda_{ij}^k[b]\cdot\psi_{ij}^k$——$\psi^k_{ij}$ 是第 k 个包到达时链路 $(i,j)$ 的**传播时延**，$\lambda^k_{ij}[b]$ 是**信道 b 上的链路连通性指示**（式 1，取值 0/1）。
- **干扰约束（式 2，L44）**：同信道上的接收不会同时被非预期发射机干扰。
- **链路容量（式 3，L54）**：**含干扰项的信干噪比**，分母中除噪声项 $n_0W_B(4\pi/c)$ 外还有**干扰机贡献** $(p_\chi f_\chi^2)/d_{ij}^2$——这是"性能退化"的数学载体：干扰使 SNR 下降 → 容量下降（L57）。
- **AoI 建模（式 5–7，L68–L80）**：作者推导出
  **AoI = 生成间隔项 $\frac{1}{2\nu^l}$ + 传输时延项 $\frac{d}{\mu_{s_la}}$ + 传播时延项 $\frac{d_{s_l,to,a}}{c}$**
  ——**注意：由此目标函数"最小化平均 AoI"在结构上等价于"最小化逐跳传输+传播时延之和"**，因为第一项与路径无关。时间平均 AoI 对全网会话求和得 $A_{ave}$（式 7）。
- **优化问题（L90）**：$\mathrm{OPT}\ \min(A_{ave})$，约束为干扰约束(2)、传输模型(4)、AoI 函数(7)、以及队列约束 $Pkt_{\Delta_T}\le Pk_{max}^{rev}+Pk_{max}^{send}$。
- **MDP（第 3.A 节，L101–L114）**：
  - **状态** $S=(Node_{currpos},Node_{dest},\chi_{t_i})$——**第三个分量是"受到的干扰形式"**，这是它相对前人的主要增量（L105："we add very few priori knowledge of jamming to the state"）。
  - **动作** $A=Node_{next}$（可达到的邻居）。
  - **奖励（式 8）**：$r=w_1\cdot Dis_i + w_2\cdot AoI_{s'} + w_3\cdot\vartheta_{s'}$，三项分别是**到目的地的距离惩罚**、**下一跳的 AoI 惩罚**、**队列增长率惩罚**（队列超阈值时按增长率成比例惩罚，L111）。**三项都是惩罚项，公式却用加号连接**——符号约定原文未交代。
- **算法（第 3.B 节）**：**DQN**（不是 DDQN），在线网 + 目标网，损失式 10 为带目标网的平方误差，梯度式 11，每 C 步同步目标网。**动态 $\varepsilon$-greedy**：$\varepsilon=\varepsilon_0\cdot\varepsilon_f^i$。网络结构：**两层全连接、每层 175 个神经元**，Tanh 激活（L149、L183）。
- **episode 定义（L149）**：一个 episode 内**所有包都到达目的地**时结束，统计目的节点的 AoI。

**4. 它声称的效果**
**重要：正文没有任何数值结果**——全部结论只有 lower/higher/better 的定性描述，数据都在 Fig 3、Fig 4 里。
- **平均 AoI（第 4.A 节，L192）**：在 **500–5000 个包**的负载扫描下，**RRS-DRL 随负载上升仍能维持较低时延且结果稳定**；**SPF 在负载 < 2500 包时表现良好，但负载继续上升后全网 AoI 高于 RRS-DRL**。归因：SPF 对网络适应能力差，"it is more difficult to adjust the impact of jamming when the number of loads increases"。
- **时延抖动（第 4.B 节，L209）**：箱线图比较下 **RRS-DRL 无数据离群点**，而 **SPF 不仅有时延离群点，抖动也更高**。
- **抖动的定义（式 12，L206）**：$\tau=\frac{AoI_j-AoI_i}{j-i}$——即**相邻包的 AoI 差除以序号差**，本质是 **AoI 的变化率**，不是通常意义的两包时延差。作者同句还给了另一种口径（相邻包时延差 / 序号差），**两种并列却只用了后者**。
- **基线：只有 SPF（最短路径优先）一个**（L188、L236）。

**5. 实验条件**
参数取自 **Starlink 的 FCC 文件**（L177）。**选中 175 颗卫星**做实验。Table 1（L179）给出 **轨道高度 550 km、最小仰角 25°、7 个轨道面、每面 25 颗、倾角 53°**（该表 OCR 严重错位，7 / 25 / 53° 与字段的对应需按 7×25=175 反推）。
用 **Python + networkx** 建网（L183）。超参：**γ=0.6、$\varepsilon_0$=0.7、$\varepsilon_f$=0.975、学习率 0.005、batch=16、replay pool N=1000、目标网更新步长 10、激活函数 Tanh**（L183）。
**流量模型（L188）**：环境中存在**扫频干扰（sweeping jamming）**使链路性能退化；网络产生大量包，**每个包的源和目的随机**；**每传一次就隔一定时间步初始化一个新包**；产生并传输到一定数量后仿真结束。
**负载扫描**：**500 / 1000 / 1500 / 2000 / 2500 / 3000 / 3500 / 4000 / 4500 / 5000 个包**，每个负载下**跑多轮**（L192）。
**训练/评估**：**未说明训练与评估是否分离**，也未给 episode 数或收敛判据；伪码写的是 "for episode = 1 to 无穷"。

**6. 自述局限（逐字）**
本篇**没有 Limitations 章节**，且**未见任何对自身方法的保留性陈述**。唯一的"不足"痕迹是引言里对**他人**工作的批评（L27），以及结论（L218）里的纯正面总结："According to the simulation results, the method obtains a lower average information age of the whole network and a lower delay jitter rate compared to SPF, which increases the robustness of the constellation."
**未见**作者讨论：权重 $w_1,w_2,w_3$ 如何选取、单基线是否足够、175 颗星能否代表 mega constellation、AoI 公式的推导边界、$\varepsilon$ 衰减与收敛的关系。

**7. 它没做但看起来能做的地方（基于内容）**
1. **加权系数 $w_1,w_2,w_3$ 全文从未给出数值**（式 8），也无敏感性分析——而这三项的相对大小**完全决定**策略偏向"趋近目的地"还是"避堵"还是"保新鲜"。**这是最大的不可复现缺口**。
2. **只有一个基线（SPF）**：文献 [6]（FRA 抗干扰路由）、[5]（DRL-ER）、[3]（RL 路由）都在它引言里出现过，**却一个都没做对比**——尤其 [6] 是直接的抗干扰对手。
3. **"退化的链路"与"断掉的链路"没有被分开评估**：作者在 L29 强调同时考虑两者，但实验里**没有给出这两种情形各自的贡献**。
4. **正文无任何数值**：AoI 具体值、抖动分位数、收敛所需 episode 数都只在图里；在一篇两页 letter 里，这使结论几乎不可核验。
5. **AoI 公式（式 5）的推导需检查**：从 $\frac{1}{T}\sum_{k=1}^{K}(\cdot)$ 到 $\frac{K}{T}\cdot\frac1K\sum(\cdot)$ 再到 $\nu^l(\cdot)$，这一步**隐含 $K/T=\nu^l$**，即"包生成率等于到达率"，而这**只在无丢包时成立**，文中未作说明。另外式 7 中 $\frac{d}{\mu_{s_la}}$ 与 $\frac{d}{\mu_{ij}}$ 的下标不一致（L80），原文或转写存在笔误。
6. **"175 颗星"与标题里的 mega constellation 不符**：Starlink Phase I 就有 1584 颗，本文只取 175 颗，且**没有做星座规模的扩展实验**。
7. **状态里的 $\chi_{t_i}$（干扰形式）缺少定义**（L101 仅写 "the form of jamming received"），既无维度也无取值空间——**这是它相对前人最核心的增量，却是全文最模糊的一处**。
8. 拼写与转写错误密集（标题 "Mege"、伪码 "Sence env and abtain s"、正文 "FRRSt" 应为 "First"、$Pk_{max}$ 与 $Pkt$ 混用），且作者列表在摘要页（Chu, Cheng, Zhu Lidong）与正文页（Chu, Cheng, Ying Yang）**不一致**——提示该稿校对质量较低。

**8. 和同批其他篇的关系**
- **与 CMNCS52M 是同一条技术线、且最直接可比**：两篇都是"每星一个 DQN 家族 agent + 局部观测 + 多目标奖励"，都**明确把 AoI 之外/之中的时延与队列写进奖励**（CMNCS52M 式 7 用 $t_P+t_{TX}+t_Q$；本文式 8 用距离 + AoI + 队列增长率）。差别在于 CMNCS52M 的**奖励是"真实一跳时延"**（可归因、可标定），而本文的 **AoI 项在数学上退化成逐跳时延和**（式 5 第一项与路径无关），且本文多了一个**抗干扰**维度。两篇都扫了负载：CMNCS52M 换"队列分布图"，本文扫"包总数 500–5000"。
- **与 EG 之外的 DRL 路由三篇（CYMQ2GLA、以及 S85KQ4FC/批外）共享同一祖先**：都建立在 **Mnih 等 2015 的 DQN** 之上（本文引 [9]，L240），都用经验回放 + 目标网 + $\varepsilon$-greedy。CYMQ2GLA 的**奖励是纯拓扑距离**（式 15，无队列/时延项），本文的**奖励含 AoI 与队列**——**这两篇正好构成"奖励里有没有负载项"的最小对照**，可用于评估"把负载写进奖励"到底值多少。
- **与 DVS8C3CC 的时延观恰恰相反、可互为边界**：DVS8C3CC **显式把排队时延设为零**并声明拥塞超出范围，专门隔离"建链时延"；本文则**把 AoI/队列当作核心**、刻意制造干扰导致的性能退化。把两篇并置，可得到"时延由离散拓扑事件主导（DVS8C3CC）vs 由负载/干扰主导（本文）"两种极端图景。
- **与 EG9X569M 引用的 DRL-ER（其 [5]，L232）的关系值得注意**：DRL-ER 同时出现在本批 S85KQ4FC 的对照名单里（作为"逐包 DRL 代表"被批评），本文则批评 DRL-ER "**Lack of consideration for jamming**"（L27）——**同一位被批评者，被两篇从不同角度批评**（一篇嫌它决策成本高，一篇嫌它没考虑干扰），说明 S85KQ4FC 与本文处于**正交的批评轴**上。
- **与 E4NYGLGX（Retrace）的关系**：本文用的是 DQN 单步自举（损失式 10），**没有用到 λ-return 或 Retrace**；批内所有 DRL 路由论文都停在单步 off-policy，这是本批的一个共同特征。
- **与 ETTA3DIV 无任何关系**（不同学科）。**本批其余各篇的参考文献中未见引用本文**，本文（2023 年 3 月预印本）也未引用本批任何一篇。

**9. 对"负载变化下到达率/时延"的贡献**
**有直接贡献，而且是本批里少数把"负载"当作显式自变量扫描的论文之一。**
- **显式的负载扫描**：**500→5000 个包、10 个负载点**（L192），比 CMNCS52M 的"换队列分布图"、CTWVLBCY 的"不可调 trace"更接近真正的负载实验。
- **给出了一条清晰的负载拐点**（L192）：**SPF 在 < 2500 包时优于 RRS-DRL，超过 2500 包后被反超**——这是一条可检验的定量交叉现象（虽数值只在图里），说明"**最短路的优势只存在于低负载区**"，与 CMNCS52M 中"traffic 场景下最优路径≈最小跳路径"的观察方向一致。
- **给了 AoI 的可计算分解**（式 5）：**AoI = 生成间隔 + 传输时延 + 传播时延**。其中**传输时延项 $\frac{d}{\mu}$ 直接是负载的函数**（$\mu$ 受式 3/4 的容量约束，而容量受干扰影响），因此这条公式**在结构上把"干扰/负载"与"AoI"连了起来**。
- **用了抖动而不只是均值**（式 12、Fig 4），还报告了离群点，比本批其他只报均值的论文多一个维度（但口径是 AoI 变化率，不是两包时延差）。
- **缺口**：
  - **"负载"在这里是"生成的包总数"，不是到达率（包/秒）**：文中只说 "a new packet is initialised after a certain time step"（L188），**没有给出到达过程的分布**，也没说明"时间步"的时长，因此**这条负载轴不可换算成 pps**。
  - **排队与目标函数脱节**：虽然有"队列增长率 $\vartheta_{s'}$"作为奖励项（L111），但**队列本身没有进入 AoI 公式（式 5）**——奖励里惩罚队列，目标里却没有队列。
  - 只有 SPF 一个基线，因此"负载上升后 RRS-DRL 更好"**无法排除是"任何非最短路算法都更好"**。

**10. 一句话评价**
**把 AoI 作为 LEO 抗干扰路由的优化目标、并把"链路性能退化"（而非只有断链）纳入建模**，问题设定有新意，且难得地做了**跨 500–5000 包的负载扫描**并给出 2500 包的交叉点；但作为一篇两页 letter，它的**实证薄弱**（单一基线、正文无数字、权重未给、干扰状态未定义），且**AoI 目标函数在数学上退化为"最小化逐跳时延和"**（式 5 第一项与路径无关），因此它更像一个**有价值的动机与设定**，而不是可复现的结论——方法论谱系上是"**DQN + 多目标奖励工程**"，与 CMNCS52M 同源但成熟度低一档。


## ETTA3DIV — Required toroidal confinement for fusion and omnigeneity (A. H. Boozer)

**1. 一句话**
一篇**磁约束聚变等离子体物理的理论论文**：论证自持氘氚（DT）燃烧要求离子/电子分布函数极接近局域麦克斯韦分布，而托卡马克/仿星器中无碰撞粒子轨迹若混沌会指数放大熵产生与输运，因此约束磁场必须满足**全向性（omnigeneity）**这一"最弱的一般条件"；论文用**纵向作用量 $J$（Northrop-Teller）**把这些约束化成可计算的积分形式，并给出构造全向平衡与量化偏离全向性的度量。

**2. 问题设定**
**与 LEO 卫星网络、路由、负载、到达率完全无关。** 具体问题（L15–L19）：DT 聚变的反应截面远小于库仑截面，要求**约束时间比碰撞时间长约数百倍（离子）/上万倍（电子）**，且功率密度正比于 $(nT)^2$ 的上限要求数密度足够低，使**平均自由程约为等离子体尺寸的 1000 倍**——于是等离子体处在一个"**既必须足够碰撞（保持近麦克斯韦）又必须足够无碰撞（轨迹问题）**"的悖论区间（L15、L165）。
矛盾的两面：一方面近麦克斯韦使非平衡态热力学可用（式 4、5 关联输运、熵产生、碰撞频率与偏离量）；另一方面 Fokker-Planck 方程是**对流-扩散型**，其**对流项（Vlasov 算子）以粒子轨迹为特征线**，若轨迹混沌则扩散效应被**指数放大**（L93），产生远超自持燃烧所能承受的输运。**全向性**就是保证"无碰撞俘获粒子的相继反弹点落在同一磁面上、且最大偏离正比于回旋半径"的最弱条件（L29、L305）。

**3. 方法骨架**
**纯理论解析（Boozer 坐标 + 作用量-角变量 + 漂移哈密顿量），无仿真、无数据集、无机器学习。**
- **约束在磁面上**：$2\pi\vec B=\vec\nabla\psi\times\vec\nabla\theta_0$（式 1），$\theta=\theta_0+\iota(\psi)\varphi$，$\iota$ 为旋转变换。
- **全向性的定义（式 2、3）**：基于 Northrop-Teller 的**纵向作用量** $J(\psi,\theta_0,u)\equiv m\int v_{||}d\ell$，全向性即 $\partial J/\partial\theta_0=0$；偏离程度用无量纲量 $(\partial J/\partial\theta_0)/J$ 度量（L41、式 37）。
- **粒子漂移（第 III 节）**：$\rho\to0$ 时回旋中心漂移 $\vec v_d=\frac{v_{||}}{B}\vec H$，$\vec H\equiv\vec B+\vec\nabla\times(\rho_{||}\vec B)$（式 12、13）；守恒量是磁矩 $\mu$ 与能量 $u$（式 14、15）。$\vec H$ 在 $v_{||}=0$（俘获粒子折返点）奇异，这正是俘获粒子会被推离磁面的根源（L207）。
- **三个层次的约束强度**（第 III.B–III.E 节）：
  1. **轴对称（最强）**：环向正则动量 $p_\varphi$ 守恒；
  2. **准对称（quasi-symmetry）**：$B=B(\psi,\zeta)$，$\zeta=N\varphi-M\theta$（式 19），漂移哈密顿量有守恒量 $P_h=NP_\theta+MP_\varphi$（式 20、21）；
  3. **全向性（最弱）**：只要求 $\partial J/\partial\theta_0=0$，允许 $B$ 不是准对称的。**全向性严格弱于准对称**。
- **全向性的两个几何条件（L309–L311）**：① 等 $B$ 线必须**在至少一个角度上无界**（不能在 θ 和 φ 上都闭合）；② 俘获粒子在相继折返点之间**净径向漂移为零**。
- **可计算的判据（第 IV 节）**：
  - $J=\sqrt{2mu}\frac{\mu_0(G+\iota I)}{2\pi}\int\sqrt{1-\frac{B}{B_t}}\frac{d\varphi}{B}$（式 34）；
  - 偏离度量 $\frac1J\frac{\partial J}{\partial\theta_0}$ 写成两个积分的比（式 37）；
  - 优化中常用的 $\gamma_c\equiv\frac2\pi\arctan\big(\frac{\partial J/\partial\theta_0}{\partial J/\partial\psi}\big)$（式 38）；
  - **充分条件（式 45、46）**：$S=0$ 对所有 $B_t,\theta_0$ 成立，等价于两个方向的 $\partial\varphi/\partial\theta_0$ 处处相等；**准对称下此式自动满足**（L485）。
  - 反弹时间 $\tau_b=\partial J/\partial u$（式 31、48），深俘获近似 $\tau_b=\frac{L_p}{\sqrt{2\epsilon}v}$（式 57）；进动频率见式 61。
- **构造全向平衡（第 V 节）**：用 Cary-Shasharina 函数 $g(\theta,\eta)$，$\eta=\zeta-g(\theta,\eta)$（式 62），把全向性条件化为式 63；展开到 $\eta^2$ 阶得式 72、73——**$g$ 的偶次幂系数任意，奇次幂系数必须被选定以消掉奇次项**（L653）。
- **主结论之一（第 VI.B 节）**：**全向但非准对称的仿星器，其自举电流等于等效准对称场下的值**（L773），即偏离准对称不改变自举电流。
- **输运估计（式 96）**：$D\approx\big(\frac{d\psi}{dt}\big)^2\frac{\nu_{eff}}{\nu_{eff}^2+\omega_{pr}^2}$，且作者**明确声明该式高度简化、只有定性正确**（L845）。

**4. 它声称的效果**
**没有实验、没有仿真、没有数值结果表**。作者在 L895 的数据可用性声明中逐字写道："Data sharing is not applicable to this article as **no new data were created or analyzed in this study**."
可称为"结论"的是若干解析命题与定性判断：
- 自持 DT 燃烧**在约 10 keV 最容易**，温度升到 35 keV 时难度**增加一个数量级**（Fig 1，L123、L865）。
- **精确全向性与解析性不相容**（除非是准对称）：Cary-Shasharina (1997) 的结果被本文重申与展开——场强极大值附近要求磁场精确呈准对称形式 $B_{max}(\psi,M\theta-N\varphi)$，否则场强必须**非解析**（L669、L873）。
- 因此现实做法是**近似全向**；第 VI.D 节讨论"在尽量少影响约束的前提下破坏全向性"，特别是**短波长波纹（ripple）**：当波纹强度超过约 $(\iota/N_c)\epsilon_t$ 时出现不可接受的波纹俘获粒子损失；而在约为 $(\iota/N_c)^2\epsilon_t$ 的**弱波纹区间**，破坏作用量守恒的影响**似乎很小**（L357–L359）。
- 给出定量标度：$\omega_{pr}/\nu_d\approx200\,T^{5/2}/(Bna^2)$（式 99）、$\omega_{pr}/\nu_e\approx2.5\,T^{5/2}/(Bna^2)$（式 100）。
- 提及**实验侧旁证**：W7-X 的设计与运行（L101、L313），以及 Jorge、Plunk、Drevlak 等近期演示了能精确满足全向性的仿星器位形（L881）。

**5. 实验条件**
**没有实验条件可言**——无仿真设置、无参数扫描、无可复现的数值实验。全文是解析推导 + 文献综合；坐标系设定为 **Boozer 坐标**（附录 A 给出完整定义与对偶关系，式 A1–A12），并在多处**假设 $M=0$、只保留 $g$ 的线性项或 $\eta^2$ 阶**以简化（L605、L619、L659）。
文中出现的等离子体参数只是**数量级锚点**（如平均自由程约 10 km、$\rho v_{th}\approx10^4(T/B)$），并非本文测量或仿真所得。

**6. 自述局限（逐字）**
- **L845（最重要的自述）**："The derivation of Equation (96) is **highly simplified, and this equation is only qualitatively correct.** A much more complete and accurate calculation of the transport with small departures from omnigeneity was given [27] by Vincent d'Herbemont, Parra, et al in 2022."
- **L671**："the extent of the implied deviations from omnigeneity **are unclear** as are the effects on transport at low collisionality."
- **L119**："**Relatively little work has been done on field-line breaking microturbulence.**"
- **L359**：弱波纹区间的结论带保留——该破坏"**appears to** have minimal effects"，且该区间"**is not discussed** in the review of ripple losses [20]"。
- **L363**："The design of coils that have minimal ripple transport while having the largest possible space between the coils for access is important but **relatively unexplored**."
- **L87**：关于同种粒子碰撞是否引起粒子输运这一"subtle question"，作者写道"The details **require too much space for this paper**."
- **L885（致谢中的自我修正）**：感谢 Per Helander、Matt Landreman 等人"**pointing out misconceptions that I made in earlier versions**"——即本工作是在他人纠正作者先前误解的基础上完成的。

**7. 它没做但看起来能做的地方（基于内容）**
**在它自己的领域内**（以下仅限等离子体物理，与 LEO 无关）：
1. **式 96 的输运系数被作者自评为"只有定性正确"**（L845），并指向 d'Herbemont 等 2022 的更完整计算——**用更准确的输运模型替换式 96、重算偏离全向性的容忍阈值**是最直接的下一步。
2. **弱波纹区间被既有综述忽略**（L359）而作者认为其影响很小——这是一个被明确指出的认识空白，值得专门研究。
3. **线圈设计与波纹输运的联合优化"相对未被探索"**（L363）。
4. **"全向性能否为准对称设计提供额外自由度"**（L877）被列为待研究问题——即全向性相对准对称到底多给了多少设计空间。
5. **非解析性的性能代价未被量化**（L671 逐字承认 unclear），尽管"精确全向性 ⇒ 非解析"在数学上已明确（L669、L873）。

**8. 和同批其他篇的关系**
**没有实质关系。** 这篇与批内其他 10 篇（LEO 路由 / 负载均衡 / 调度 / 仿真平台 / AoI / RL 理论）**分属完全不同的学科**：
- **研究对象的层次不同**：本篇是带电粒子在磁场中的**连续哈密顿动力学**（回旋半径趋于 0 的导心近似）；其他篇是**离散数据包在离散图上的转发决策**。
- **术语表面重合、语义完全不同**：本篇的 trajectory / chaotic / action / confinement / transport / drift / bottleneck 指的是粒子轨道、哈密顿混沌、作用量-角变量、等离子体约束、输运系数、漂移速度——**与"路由轨迹/混沌/动作空间/流量约束/传输/漂移/瓶颈"只是英文词形相同**。我通读后确认**不存在可迁移的数学结论**：它的核心对象（相空间作用量积分 $J=\oint v_{||}d\ell$）与 LEO 网络的任何量（时延、队列、到达率、跳数）之间**没有映射关系**。
- **引用关系**：参考文献 [1]–[28]（L959–L1022）全部是等离子体物理/磁约束聚变文献（Boozer 本人系列工作、Northrop & Teller 1960、Cary & Shasharina 1997、Helander & Nührenberg 2009、W7-X 实验等），**与 LEO 网络文献零交集**；本批其他篇也不可能引用它。
- **一个值得报告的语料事实**：它与 **E4NYGLGX（Retrace）** 一样属于"**非 LEO 文献被一并纳入**"的情形，但两者性质不同——Retrace 至少是批内多篇 DRL 路由论文所用算法家族的理论出处，**本篇连这种间接关系都没有**：批内没有一篇使用等离子体物理的方法或结果。因此它更像**检索/归档环节的误纳**（例如按 trajectory / routing / confinement 之类关键词被召回），而非刻意的周边文献。

**9. 对"负载变化下到达率/时延"的贡献**
**没有直接贡献。明确地没有。** 依据：
- 全文**不含任何**"到达率"、"排队"、"端到端时延"、"流量负载"语义的概念。本文的 transport 指**粒子/能量在磁面之间的输运**（式 4、5、96），是扩散过程而非网络传输。
- 它的因变量是**粒子径向偏离 $\Delta\psi$ 与熵产生率**，自变量是**磁场位形 $B(\psi,\theta,\varphi)$、粒子能量与磁矩、碰撞频率**——没有时间维度上的到达过程，也没有服务速率。
- 它确实有"时间尺度"（反弹时间 $\tau_b$、进动频率 $\omega_{pr}$、碰撞频率 $\nu$），但比较的是**三种物理过程的相对快慢**（式 99、100），**不是请求到达与服务速率的关系**。
- **不做硬扯的说明**：我不会因为"两者都存在多个时间尺度的竞争"就声称相关。那是**隐喻层面的相似**，不产生任何针对"负载变化下到达率/时延"的可检验事实或工具；强行转述只会污染读卡的结论层。

**10. 一句话评价**
**一篇与本研究主题完全无关的等离子体物理理论论文**（Boozer 关于仿星器全向约束的作用量表述，2023 年预印本）：在其本领域内，它把"约束磁场必须满足什么条件"还原成可计算的解析判据（式 2、37、45、96），并明确指出**精确全向性与解析性不相容**这一结构性障碍；但对"LEO 卫星网络 RL 路由选题"这一目标，它的贡献是**零**——它出现在本批语料中，本身是一条关于**语料构成与召回质量**的证据，值得主控在汇总时单列。


<!-- END-OF-CARDS -->
