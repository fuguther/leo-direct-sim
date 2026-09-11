# 读卡批次 R9

> 读法：R9 通读者逐字通读全文（VM MinerU MD，`/data/liguang13/topic-loop-r2/md/<KEY>/<KEY>/txt/<KEY>.md`）。行号均对应 VM MD 原文行号。
> 批次：UF8IQTA2 UKBSA7WN UKEKU5ZG UMKF328H VACUFEHB VFS59FHI W5Z39E25 W6M3GU7L WFA3CZLP WHS8Z44C WT839JP7（11 篇）

## UF8IQTA2 — Traffic-Predictive Routing Strategy for Satellite Networks (G-AODV)

> Electronics 2024, 13, 6 (MDPI)。作者：Zhiguo Liu, Zhengxia Liu, Lin Wang, Weijie Li（大连大学）。全文 369 行，逐行读完（1–130 / 131–275 / 276–369 三段）。

**1. 一句话**
把 AODV 的 RREQ 转发加一道"预测闸门"：每颗星用 GRU+attention（**直接复用作者自己上一篇论文 [23]**）预测下一时刻负载，若预测值超过**邻居均值型的动态阈值 L**，该星就不转发 RREQ 而是向上游发拥堵信号让上游改路——再叠一个按 hopS/hopD 选"源修复 / 本地修复"、并按"邻居集合 Jaccard 相似度"挑修复发起节点的维护机制。

**2. 问题设定**
LEO 星座的两难：负载不均 + 星间链路(ISL)不稳。论文在相关工作里把 AODV 类按需路由的病灶写得很直白（L62 附近逐字）："Some intermediate nodes ignore their load status and directly forward packets after receiving them, which makes the load of heavier intermediate nodes not alleviated. This causes a large number of data packets to be discarded, increasing the average end-to-end delay and packet loss rate." 即：**中间节点收到 RREQ 就转发，完全不看自己有多忙**，于是重载节点持续被选中、缓存填满、丢包、时延上升，最终"network fragmentation"（L62–L66 一带）。谁遇到麻烦：被选作中转的过载卫星，以及端到端用户。

**3. 方法骨架（非 RL，纯协议工程 + 外借预测器）**
- **探测**：HELLO 包扩两个字段 Curr_traffic / Next_traffic（Table 2，L103–L110 附近），邻居把预测值记进邻居表。
- **阈值**（式 1，L95–L99）：$L=\frac{1}{n}\sum_{i=1}^{n}\frac{Curr\_traffic_i+Next\_traffic_i}{2}$。**注意：这是一个纯相对阈值**——它只在"本节点比邻居平均更忙"时才触发，不含任何绝对容量/队列占用基准。
- **判决**（式 2，L105 附近）：$Next\_traffic_i>L$ → 认定将拥堵，构造 RCS 拥塞控制信号（Table 3，字段 rc_dst / rc_S_address / rc_D_address，L118–L125）发给上游；否则收下并转发 RREQ。
- **上游反应**（L111–L133）：上游缓存发往该下游的包、把路由表状态置 TAG_CONGEST、重新选邻居、重发 RREQ。下游在被标记期间"不接收任何 RREQ"（给重载节点喘息时间）。
- **路由表改造**（L140–L142）：加 hop count / 到目的跳数 hopD / 下两跳 / 上两跳四个字段，**每表项多 16 字节**。
- **修复模式选择**（L149–L163）：$hopS<hopD$ → 源节点修复；$hopS\ge hopD$ → 本地修复。
- **节点稳定性**（式 3，L165–L177）：$STA_i=\frac{|V_i(t_1)\cap V_i(t_2)|}{|V_i(t_1)\cup V_i(t_2)|}$，即两个时刻邻居集合的 Jaccard 比。断链处**稳定性更高的那一侧**发起本地修复（L179–L197，Table 6 给完整状态机）。
- 无状态/动作/奖励，无学习更新——"学习"部分整个外包给文献 [23]。

**4. 它声称的效果（全部只有相对百分比，无绝对数）**
- 场景 1（扫描 packet forwarding rate）：PDR 相对 E-AODV / DS-DSR / NCMDSDV 提升 **10% / 12% / 20%**（L254）；丢包率分别降 **5% / 19% / 22%**（L268）；时延只说"has been reduced"（L264 段）—— **一个数字都没给**。
- 场景 2（连接对数 10→60，固定 4500 pkt/s）：PDR 提升 **15% / 18% / 20%**（L279）；丢包降 **4% / 10% / 18%**（L293）；时延同样只有"reduced"。
- 收敛：L298 逐字 "After 280 iterations, the algorithm successfully achieved a satisfactory convergence state."（但本方法并不迭代学习，这句话像是从别处套来的，且与全文方法不对应）。
- 三个基线全是 **MANET 协议**（E-AODV / DS-DSR / NCMDSDV），不是任何 LEO 专用路由，也不是 DRL 路由。
- 图 6–11 的曲线在 MD 里不可读，正文也没给任何坐标值 → **全篇没有一个可复现的数值点**。

**5. 实验条件**
- 拓扑：STK 生成 Iridium 星座，NS2 承载仿真（L203）。卫星速度 7.9 km/s、pause time 0 s（L246 附近）。
- Table 7（L206）**总共只有 4 行**：处理速率 1000 pkt/s、ISL 10 Mb/s、上行 9 Mb/s、下行 9 Mb/s。**没有**：星座规模（卫星数）、包长、缓存长度、仿真时长、流量到达过程（Poisson？CBR？）、源目的对如何摆放。
- 场景 1：扫描"packet forwarding rate"——**扫描范围正文从未给出**，只有图 6/7/8。
- 场景 2：固定 4500 pkt/s，连接对数 10/20/30/40/50/60（L275）。
- 训练与评估：预测器直接引用 [23]，**没有说明是否在本环境重新训练、是否同一套数据**——即"训练/评估同分布"这件事在本文里根本没被提出。

**6. 自述局限（L304 逐字，全段）**
"After simulation verification, this method has greatly improved performance, but it also has some limitations. In real-time applications, such as video communications or emergency communications, routing decisions based on traffic prediction may introduce some additional delays. These additional delays can negatively impact user experience. Additionally, using neural networks for traffic prediction may require substantial energy and computing resources, especially in satellite networks with a large number of nodes and limited resources. It should be noted that the satellite network topology changes frequently, including the addition and departure of nodes, the interruption of links, etc. In this case, the predictive model needs to be adjusted in time to adapt to changes, otherwise its accuracy will be affected."
（三条：预测本身引入额外时延；星上算力/能耗；拓扑变化会让预测失准。**都没有做实验去量化**。）

**7. 它没做但看起来能做的地方（基于内容）**
1. **L 是相对阈值，从未在"全网齐涨"下测过**。L 取邻居 (Curr+Next)/2 的均值，负载整体抬升时 L 跟着抬升，判决退化成"谁比邻居更忙"——绝对容量约束被抹掉。论文扫的恰恰是全网单调增压（场景 1 提 forwarding rate），此时相对阈值应逐渐失效，但论文没有做这个消融，也没给 L 的敏感性分析。
2. **它自己算出了自伤成本却从不扣账**：L142 说每表项多 16 字节、"increase the bandwidth by up to $16*R$"。代入它自己的场景 2（R=4500 pkt/s）：16×4500 = 72 kB/s = **576 kb/s ≈ ISL 10 Mb/s 的 5.8%**，而 HELLO 还多带一个 Next_traffic 字段没算。**一个做负载均衡的协议在给自己增负**，这条从未回到结果里扣掉。
3. **"预测引入额外时延"与"预测减少排队时延"是两个反号项，论文有 delay 指标却从不拆分**——式 5 定义了平均端到端时延，全文却没给过一个值。这是一个现成的、可直接测的实验。
4. **节点稳定性定义含糊**：L177 附近把时间间隔定义为"the survival time of the link after the node receives the HELLO message"，t1/t2 怎么取、间隔多长完全没定，STA 的取值因此不可复现——可换成显式的链路持续时间估计。
5. **RCS 是逐节点 on/off 的二值信号**，且被打标的下游"不接收任何 RREQ"——在均匀高压下可能引发整片区域同时闭锁（论文完全没讨论这种集体行为）。
6. 场景 1 的**扫描范围缺失**，导致那条"到达率→性能"曲线不可重建。

**8. 和同批其他篇的关系**
本批（R9）其余 10 篇尚未读，暂无法逐篇比对。就内容而言它属于"经典按需路由 + 启发式负载规避"谱系（对应相关工作 L51–L68 的 AODV/MPTCP/多径一族），**不含任何 RL**，与 DRL-LEO 路由那一条线无交集；被引的 [23] 是同一作者团队的前作，属于自我复用而非外部对照。它的三个基线也全部来自 MANET 文献 [25][26][27]，说明它没打算和 LEO 专用路由比。

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**有关系，但只有设计、没有事实。** 它恰好是全库里少数**显式把"到达率"当自变量**的论文：场景 1 扫 packet forwarding rate，场景 2 扫连接对数（两者的物理效果都是提高注入负载），所以"负载变化"这个轴它确实占了。但：
- 时延在**两个场景里都只写了"reduced"**，没有任何数值或曲线值 → 拿不到"到达率→时延"的函数形状；
- 没有队列模型、没有到达过程说明、没有缓存长度 → 连趋势都无法从机制上重算；
- 唯一可迁移的机制性事实是一条**定性张力**：预测性改路（本意降排队时延）和预测本身的开销（自述增时延）方向相反，论文承认后者却从未把两者分开测。

**10. 一句话评价**
**把"邻居均值相对阈值 + 上游通告"这一套成熟的拥塞规避启发式移植到 AODV 上**，预测器直接搬自己上一篇的 GRU+attention，真正的原创只落在"按 hopS/hopD 选修复模式 + 用邻居 Jaccard 挑修复发起方"；方法谱系上它是一篇协议工程论文而非学习论文，且实验报告连仿真参数和绝对时延数字都没给全，**可复现性弱于它声明的结论强度**。

## UKBSA7WN — Reinforcement learning based dynamic distributed routing scheme for mega LEO satellite networks (QRLSN)

> Chinese Journal of Aeronautics（2022 在线，Elsevier，CC BY-NC-ND）。作者：Yixin Huang, Shufan Wu, Zeyu Kang, Zhongcheng Mu 等（上海交大 / 北航 / 悉尼大学 / 二院 X-Lab）。全文 310 行，逐行读完（1–120 / 121–240 / 241–310 三段）。

**1. 一句话**
把 1993 年的 Q-Routing 原封不动搬进兆级 LEO 星座：每颗星一张 Q 表、逐包做 $arepsilon$-greedy 选下一跳，训练分两段——"路由发现"阶段用**稀疏二值奖励**（到终点给 $r_{max}=100$、否则给 $r_{min}=1$）把可达性学出来，"路由维护"阶段换成一个**两目标奖励向量**（链路传输时延 + 本节点排队包数），用线性加权把两个 Q 表合成一个 TQ 再决策。

**2. 问题设定**
兆级 LEO（作者举例 Starlink/OneWeb/Telesat）的路由表算不起也维护不起。引言把两类传统方案都判了死刑（L28–L30 一带）：VT/VN 静态方案"rely on centralized routing calculation, and each satellite stores various route tables according to time and position, so it is difficult to update the whole network's route tables simultaneously"，且节点/链路故障时"unable to adjust routing strategies timely and result in service interruption"；DSDV/AODV 类动态方案则"rely on data packets flooding and broadcasting, consuming too much satellite computational resource and network bandwidth"（L32 附近）。作者还明确写"Although RL has gained a rapid development in terrestrial networks, there are almost no relevant studies on LSN systems"（L34 附近）——**这就是它给自己划的空位：LEO 上还没人用 RL 做路由**。谁遇到麻烦：需要全网点对点转发的兆级星座运维方。

**3. 方法骨架（真 RL，tabular Q-learning）**
- **状态**：**没有显式定义**。MDP 只在 L2.2（L51–L76）以 $(S, A, P_t, R)$ 符号列出，此后再没出现过 $s$ 的具体内容；实际被携带的信息只有"当前节点 + 目的节点"（Q 表的下标就是这两者）。
- **动作** $A_i$：当前星 $i$ 的邻居集合（式 4，L123–L131），$arepsilon$-greedy，$arepsilon=0.1$。
- **Q 表**（Table 1，L101–L109）：$Q_i(j,d)$ = 在节点 $N_i$、以邻居 $j$ 为下一跳、送往目的 $d$ 的价值；每颗星**只存到"目的地"维度的表**（表中 $D_1,D_2,D_3$ 即目的节点）。
- **更新**（式 2，L66–L70）：$Q_i(j,d)\leftarrow(1-\alpha)Q_i(j,d)+\alpha[r+\gamma Q_j(d)]$，其中 $Q_j(d)=\max_{k\in Ng(j)}Q_j(k,d)$（式 3）——这是**原始 QR 的邻居回传式**，不含 double 目标。
- **路由发现阶段奖励**（式 5，L133–L137）：到终点 $r_{max}=100$，否则 $r_{min}=1$。作者自述 $r_{min}$ 的作用是"prevent the updating delay of Q-values due to the sparse reward feedback"（L135）。
- **路由维护阶段 = MORL**（3.2 节，L137–L170）：奖励向量 $f_r=[f_{r_1},f_{r_2}]$，
  - 式 8：$f_{r_1}=r_{min}+(e/2)^{-d_{ij}}$（$d_{ij}$ = 相邻星间传输时间）→ 优化端到端时延；
  - 式 9：$f_{r_2}=r_{min}+(e/2)^{-n_q}$（$n_q$ = 当前节点排队包数）→ 优化"网络流量开销负载"；
  - 合成（式 7）：$\mathrm{TQ}(s,a)=\sum_{i=1}^{n}w_iQ_i(s,a)$，$\sum w_i=1$，取 TQ 最大的动作。**$w$ 的取值全文未给**（只在评价里说"pre-designed reward vector"，L180 附近）。
- **队列**：每星一个队列 $q_i$，算法 1 第 8–11 行是"若 $q_i\neq0$ 则选出下一跳、出队、转发"（L112–L120）。
- **两阶段架构**（Fig 2 / 3.0 节）：
  - 路由发现（Algorithm 1，L110–L120）：**发射前**在地面把初始 Q 表训出来，$M$ episodes × $N$ steps，每步注入 $x_k\sim\mathrm{Poi}(\lambda)$ 个包到随机源目的对（L89）；
  - 路由维护（Algorithm 2，L182–L194）：用训好的 Q 表在线跑，邻居发现周期性发 Hello（**不带 Q 表内容？**L79–L83 说 Hello 含 "neighbor status, nodes Q-tables and link information"，但式 2 的更新又要求读到 $Q_j(d)$——这一条信息通道的带宽代价论文完全没算)，事件触发（包到即决策）。

**4. 它声称的效果**
- **路由发现**：Fig 4 丢包比（"delivery loss ratio"）随 episode 收敛下降、Fig 5 平均端到端时延也随之下降（L215–L217）。星座规模越大收敛越慢，作者解释是"more Q-tables on satellite nodes need to be updated"（L217）。**均为曲线趋势，无坐标值。**
- **路由维护**：Fig 6 —— 1152 星星座下**最大丢包比低于 0.07%**（L223，这是全文唯一一个绝对数字）；Fig 7 —— 平均时延持续下降，且 1152 星场景到一天仿真结束时**仍在下降**（L225–L227 附近）。作者估计图 5 与图 7 时延差异源于"more satellite nodes in a routing path"导致处理时间更长（L227）。
- **对基线 VT-SPR**（虚拟拓扑 + Dijkstra 最短路径，时间片 20 min）：
  - **VT-SPR 的 delivery loss ratio 恒为 0**——作者自己解释："because the Dijkstra is a static routing algorithm and can always find a reachable shortest path"（L235）。**即 QRLSN 在"可达/丢包"这一项上没有赢，甚至输给基线**，论文只用时延/队列开销作为胜场。
  - **低负载（k=5）时 VT-SPR 时延优于 QRLSN**（L237 逐字："the result under k 5 condition in Fig. 9 indicates that the VT-SPR routing method is superior to QRLSN in the end-to-end delay performance. It is indicated that VT-SPR is more applicable under low-load network conditions."）；
  - **k=20 / k=35 时**：早期仍是 VT-SPR 时延更低，"However, QRLSN gradually achieves a better performance during the optimization process"（L239）——即交叉点存在，但论文**没给交叉发生的时间点或负载阈值**。
- **复杂度**（4.3 节，L241–L249）：QRLSN 发现 $O(n^3)$、维护 $O(n)$；VT-SPR $O(n^2)$。QRLSN 空间 $O(n)$，VT-SPR 空间 $O(n)$。作者据此宣称 QRLSN 更适合分布式（VT-SPR "relies on centralized calculation"）。
- 图 8/9 曲线在 MD 不可读，正文无数值坐标。

**5. 实验条件**
- 星座：Walker Delta，**53° 倾角、550 km 高度**（L198），规模取 **288 / 512 / 1152** 颗（L202）。每星 4 条激光 ISL（同轨 2 + 异轨 2，L44–L48）。
- 工具链：STK + NetworkX（L198）——**没有网络仿真器**，即没有 MAC/信道模型，队列行为是自造的抽象。
- 流量：$x_k\sim\mathrm{Poi}(\lambda)$ 个包/单位时间注入**随机**源目的对（L89）。发现阶段 $\lambda=5$；维护阶段 $\lambda=20$（Table 2/3，L187–L206）。
- 时延口径：**包若 2000 ms 内未收到即判丢**，且超时包仍留在缓存里直到被出队时才判定（L204 附近逐字："data packets are considered to be lost if they are not received within 2000 ms. The time-out packets are still in the queue buffer until they are out of the queue and judged to be dropped."）。
- 时间粒度：维护阶段**时隙 1 min、邻居发现周期 1 min**（Table 3，L206），每周期最多 500 步；仿真窗 2022-01-29 04:00 → 01-30 04:00（24 小时）。
- 学习超参（Table 2，L188）：1000 episodes × 1500 steps、$\alpha=0.8$、$\gamma=0.95$、$\varepsilon=0.1$、包处理时间 1 ms。
- **训练 vs 评估不是同一套**：发现阶段 $\lambda=5$ 训出初始 Q 表，维护阶段 $\lambda=20$ 起跑并继续在线学——即**在线阶段是在分布外起步的**，论文没把这一点当风险讨论过（只在 L215–L217 提到"at the beginning of training, there is no deterministic policy"）。
- 负载扫描只有 $k=5/20/35$ 三个点（Fig 8/9，L231–L239），且 $k$ 与 $\lambda$ 的关系（$k$ 就是 $\mathrm{Poi}$ 的期望？）论文没写清楚。

**6. 自述局限（L255 逐字，末尾）**
"In our future works, we will improve the QRLSN's robustness in the presence of node failures and inter-satellite link instability. Additionally, in-depth research on congestion awareness will be the focus for further investigation."
（只有这一处，两句：节点失效/ISL 不稳的鲁棒性未做；**拥塞感知未做**。注意：它自己在式 9 里已经用了 $n_q$ 做奖励，却把"congestion awareness"列为未来工作——这两个说法之间存在张力，说明作者认为 $n_q$ 这一项还不构成真正的拥塞感知。）

**7. 它没做但看起来能做的地方（基于内容）**
1. **低负载下被基线打败这件事只被陈述、没被解释**。L237 承认 k=5 时 VT-SPR 更优，机理解释可以现成地给出：QRLSN 用 $\varepsilon=0.1$ 恒定探索，低负载时探索带来的绕路成本 > 静态最短路的收益。**但论文从没做过 $\varepsilon$ 退火、也没做过随负载调 $\varepsilon$ 的实验**——这是一个明确、便宜、杀伤力大的实验空位。
2. **$w_1,w_2$ 从未给出取值，也没有做任何 Pareto/敏感性分析**。式 7 的加权和是它唯一的"多目标"机制，权重却不可见——多目标在这里名不副实（真正的 MORL 应给 Pareto 前沿，而不是固定线性标量化，更不是把 $Q_i$ 与 $w_i$ 混为一谈）。
3. **状态没定义**，$d_{ij}$/$n_q$ 到底描述发送方还是接收方含糊不清。式 8/9 的奖励是在转移后由"current node"计算（L166 附近），而 $n_q$ 被写成"the number of data packet queued in the current node"——若指**发送方自己的队列**，则这个奖励根本不反映所选下一跳的拥塞，$f_{r_2}$ 就失去意义；若指接收方则表述应为 next hop。**这一个字的歧义决定了方法是否成立**，而论文没有澄清。
4. **$f_{r_1}$ 用的是 $d_{ij}$（链路传输时间）而非排队时延**，但端到端时延的大头在高压下恰恰是排队——它把"时延"目标退化成了近似跳数/传播时延目标，而排队只进了 $f_{r_2}$ 且被当成"traffic overhead load"。**两个目标的分工与它自己的指标名不匹配。**
5. **丢包口径可疑**：VT-SPR 恒为 0 丢包（L235），而 QRLSN 有非零丢包——在 1152 星下声称 0.07% 很低，但**基线是 0**。真正该做的是在同样的 k=35 高压下比丢包，而不是在"最大丢包比"这一个标量上自我表扬。
6. **Hello 交换 Q 表信息的开销没有计入任何指标**，而 VT-SPR 的对比里恰恰强调了"traffic overhead load"。
7. **2000 ms 超时阈值是硬编码常数**，没有做阈值敏感性——而这个阈值直接决定了图 4/6 的丢包曲线形状。

**8. 和同批其他篇的关系**
本批（R9）其余篇尚未读完，暂无法逐篇比对。就谱系看：它是**本批唯一明确自称"首次把 RL 用于兆级 LSN 路由"**的论文（L34），把自己摆在 Q-Routing（Boyan & Littman 1993）、PQ-Routing、QELAR、QLFR、QGrid、QGeo 这条地面/水下/车载的 Q-learning 路由族里，**方法上零改造**——式 2 就是 1993 年 QR 的更新式，其增量只在"换了个奖励向量"。它与 UF8IQTA2 构成对照：UF8IQTA2 是纯协议工程不含 RL，本篇是纯 tabular RL 不含协议细节。

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**有直接贡献，且是本批少见的"给出了负载依赖反转"的论文。** 具体三条：
1. 它**显式把负载当自变量扫了三个档**（$k=5/20/35$，Fig 8/9），并用 $\mathrm{Poi}(\lambda)$ 建模到达过程（L89）——这是本批里少数把"到达率"写进模型而非只写进实验轴的论文。
2. **它给出了一个方向明确的反转结论**（L237/L239）：低负载（k=5）→ 静态最短路径（VT-SPR）时延更优；高负载（k=20/35）→ QRLSN 经在线优化后反超。**这是"负载变化下，路由策略的优劣本身会翻转"的一个直接证据**，对选题极有价值：说明任何单一负载下的对比结论都不能外推。
3. 时延被拆成**排队时间（Fig 8）与端到端时延（Fig 9）两条曲线**分别报——在高压下这正是最需要的分解，尽管它没给数值。
**缺口也很明确**：交叉点在哪（负载阈值、时间点）完全没定位；$\lambda$ 与 $k$ 的映射没说清；上线前的初始策略在 $\lambda=5$ 训、上线后 $\lambda=20$ 跑，**"负载突变时策略要不要重训、多久恢复"这个问题被它的实验设置绕过去了**。

**10. 一句话评价**
**一篇"把 1993 年的 Q-Routing 原样搬进兆级 LEO 并诚实报出低负载下输给静态 Dijkstra"的移植型工作**——方法谱系上它不改算法本体，只在奖励上叠了一个加权和式的伪多目标；真正有价值的不是它的方法，而是它无意中留下的那条**负载依赖反转曲线**和"初始策略训练负载 ≠ 运行负载"这个被绕开的设置。

## UKEKU5ZG — A Centralized–Distributed Joint Routing Algorithm for LEO Satellite Constellations Based on Multi-Agent Reinforcement Learning (MARL-JR)

> Appl. Sci. 2025, 15, 4664（MDPI）。作者：Licheng Xia, Baojun Lin, Shuai Zhao, Yanchun Zhao（上海科技大学 / 中科院微小卫星创新研究院）。全文 333 行，逐行读完（1–115 / 116–230 / 231–333 三段）。

**1. 一句话**
把"**地面集中预训练 Q 表 + 在轨分布式继续学**"拼成一个混合体：地面站用 Iridium-like 初始拓扑把各星 Q 表训好上传，卫星上天后靠**周期性广播本地链路状态**（而非只在转发数据包时被动获取）来保持 Q 表新鲜，奖励把"邻居负载"和"传播时延"按 5:1 加权相减。

**2. 问题设定**
LEO 路由的老问题：拓扑快变 + 负载不均。引言把传统方案分两类各打一板（L38–L46 一带）：虚拟拓扑/虚拟节点类"rely on centralized routing calculation"，集中式最短路径"often neglect the impact of traffic load on routing performance and struggle to adapt to rapid link-state variations"（摘要 L11–L13 逐字）；而纯分布式 RL 类（点名 Huang [10] = 本批 UKBSA7WN）的毛病是"**this method had relatively slow convergence**"（L63 逐字）。**这篇的定位就是夹在两者之间**：用集中式解决"起步差/收敛慢"，用分布式解决"反应慢"。谁遇到麻烦：卫星刚入轨、Q 表还没学出来的那段时间里的用户。

**3. 方法骨架（tabular Q-learning，非真正的 MARL）**
- **状态**（L134 逐字）：$se_t=\{N_c, N_a, q_1^t, q_2^t,\dots, q_{Num_v}^t\}$——当前节点、目的节点、**以及全网每一颗星的队列长度**。⚠️ 这在字面上是**全局状态**，与它自称的"分布式、只交换本地信息"直接冲突；实际能拿到的只有邻居广播的信息，论文没解释这个落差怎么消解。
- **动作**：转发给某个邻居，$max(p)=4$（Iridium 每星最多 4 条 ISL，L136–L139）。
- **奖励**（式 3，L143）：邻居是目的节点 → $q_{max}$；否则 $q_{max}-w_1 g_j-w_2 D_{ij}$。**注意奖励以 $q_{max}$ 为上界、以负载/时延为扣减项**，是一个"满分为准的扣分制"。
- **负载量**（式 4，L147）：$g_j=q_{receive}+q_{send}+q_{occupied}$——把接收队列、发送队列、已占用空间三者相加。这是全文唯一涉及拥塞的核心量。
- **Q 更新**（式 1，L~108）：$Q_i(s,a)=(1-\alpha)Q_i(s,a)+\alpha[r+\gamma\max_{a'\in A_c}Q_j(s',a')]$，即**原始 QR 的邻居回传式**，邻居的 Q 通过广播拿到。
- **运行阶段的目标式**（式 6，L~181）：$Q_i(s,a)=(1-\alpha)R_i+\alpha\gamma(R_{i+1}+R_{i+2}+\cdots+R_n)$，式 7：$Q_{sum}=\sum_i^n Q_i(s_i,a_i)$。**这两式不是标准 Q-learning 更新**（把沿途奖励的裸和当回报、且没有对 $Q$ 取 max），与式 1 并存且未被调和——**没读懂：第 3.4 节，式 6/7 与式 1 的关系作者没有交代**。
- **探索**（式 5，L~168）：$\varepsilon$ 带**衰减因子 $\mu^t$**，随机动作概率 $\mu^t\varepsilon$，$\mu=0.998$——针对 UKBSA7WN 那样的恒定 $\varepsilon$ 做了改进。
- **信息交换**（3.2 节，L150–L153）：周期 $T$ 广播本地邻居/链路状态；**并额外广播 Q 表**（L189 逐字："Upon receiving a data packet, a node actively broadcasts its Q-table and link-state information"）。超时收不到 ISL 状态即判该星故障、相关链路全部停用。
- **Q 表初始化**（3.3 节，L154–L173）：地面基于 $G_{t_0}$ 预训练，随机源目的对，包在**上一个包到达时**生成；接收队列满或节点/链路故障则包进入等待。作者强调由于卫星轨道可预测，"can be **periodically reapplied**"（L~171）——即必要时可周期性重新下发。

**4. 它声称的效果（全部无数值）**
- 基线两条：**DR-BM**（Data Rate Benchmark，集中式，[25,26] = Dijkstra 1959 + Soret 2024）与 **Q-routing**（[27] = Boyan & Littman 1993）。
- **Fig 6 平均时延 vs 流量负载**（L232）：低负载下 **DR-BM 更好**（逐字："under low traffic loads, DR-BM can rapidly acquire global information and select paths with shorter delays due to the small number of data packets"）；负载升高后 DR-BM 与 QR 双双恶化——DR-BM "suffers from inefficient packet forwarding decisions and increased queuing delays"，QR "demonstrates limitations in handling highly dynamic networks under high traffic loads"。
- **Fig 7 丢包率 vs 流量负载**：MARL-JR "significantly lower packet loss rate ... superior robustness as compared to the Q-routing algorithm"（L~239）。注意**这句只跟 QR 比，没跟 DR-BM 比丢包**。
- **Fig 8 负载均衡**：固定 3000 包，用**各节点包数的方差**衡量均衡度，MARL-JR 方差更低（L245–L247）。
- **Fig 9 包到达率**：固定 3000 包，DR-BM 因集中式无需训练收敛，故"其初始阶段性能不必考虑"（逐字："the routing performance of DR-BM during the initial satellite deployment phase need not be considered"）——**这是一个把基线从比较中剔除的操作**；MARL-JR 靠地面预训练从部署第 0 天就有好策略。
- **Fig 10 PDR vs 链路失效数**（固定 3000 包，单次路由过程最多 5 条链路同时失效）：三者都随失效数下降，DR-BM 退化最快，MARL-JR 优于 QR。归因于两点创新，其中第一点写作"**(1) incorporation of a residual load factor for congestion-aware routing**"（L255）——⚠️ **"residual load factor"（剩余负载因子）这个术语在全文正文中从未定义过**，式 3/式 4 用的是 $g_j$。术语与内容脱节。
- 全文**没有任何绝对数值**：没有时延毫秒数、没有丢包百分比、没有 PDR 数值，只有曲线。
- 复杂度（4.3 节，L212–L218）：集中式为 $O(N^2)$ 时间、$O(N_E+N)$ 空间；本方法更省——**但文中没有给出本方法的具体复杂度表达式**，只有定性比较。

**5. 实验条件**
- 星座（L200，Table 4）：Iridium-like，**49 颗星（7 轨道 × 7 星）、780 km、86.4° 倾角**。
- 工具链：**未说明用了什么仿真器**（无 STK/NS2/OMNeT++ 字样）。链路失效用"图上随机删边/恢复"模拟（L230），单次路由过程最多 5 条同时失效。
- 超参（L206–L210，Table 5）：$q_{max}=200$、**负载权重 $w_1=5$、时延权重 $w_2=1$**、$\gamma=0.9$、$\varepsilon$ 初值 0.8、衰减 $\mu=0.998$、**40 episodes × 300 steps**、学习率预训练 0.7 / 运行 0.3。
- 负载：只报了两个情境标量——"3000 packets in the network"（Fig 8/9/10 用）与 Fig 6/7 的"varying traffic load"（**范围未给**）。到达过程未说明。
- 时延口径（L232 逐字）："The total latency is defined as the cumulative time required for all data packets to traverse from the source node to the destination node. By dividing the total latency by the number of **transmitted** data packets, the average latency can be obtained." ⚠️ **分母是"发送"的包数而非"收到"的包数** → 丢包越多，这个"平均时延"被压得越低，**丢包与时延两个指标在此口径下被人为耦合**。
- **训练与评估不同源**：预训练在 $G_{t_0}$（初始拓扑）上做，运行阶段在持续变拓扑 + 随机删边上做；论文把它当作优点（"reduces computational burden"），没做分布偏移的量化。
- 论文 40 episodes × 300 steps 的预训练量级，相对 UKBSA7WN 的 1000×1500 小了两个数量级——"convergence"是否真达成无法从文中判断。

**6. 自述局限（L264 逐字，唯一一处）**
"Furthermore, MARL-JR exhibits exceptional resilience in handling link failures. Future research will focus on extending the reinforcement learning framework to diverse satellite network scenarios and complex link connectivity conditions to further enhance its applicability and performance."
（**严格说这不算局限自述**——只有"未来会扩到更多场景"一句方向性表述，没有承认任何具体缺陷。**未见**对全局状态 vs 局部信息的矛盾、式 6/7 的非标准性、时延分母口径、以及"residual load factor"未定义的任何说明。）

**7. 它没做但看起来能做的地方（基于内容）**
1. **低负载下集中式（DR-BM）再次取胜**（L232）——这与 UKBSA7WN 的 k=5 结论**独立复现了同一现象**。两篇都只陈述、都不解释。这是一个已经出现两次、可以立刻做成正式命题的规律：**负载低时全局最短路径占优，负载高时局部反馈占优，中间有交叉点**。交叉点在本文里同样没被定位。
2. **时延分母用"发送包数"** 使得丢包越多、平均时延越好看——把分母改成"到达包数"（或同时报两者）即可，成本极低，且直接影响 Fig 6 的结论方向。
3. **式 6/7 与式 1 并存**：同一个 Q 值有两个互不相容的定义。要么式 6/7 只是用来事后算路径总分（$Q_{sum}$ 评估路径优劣），要么就是错的——文中没有任何一处使用 $Q_{sum}$ 做决策的说明。这是可以直接查证的表述缺陷。
4. **状态 $se_t$ 含全网队列** 与"只广播本地信息"冲突。若真按局部信息执行，则式 4 的 $g_j$（$q_{receive}+q_{send}+q_{occupied}$）只能反映**一跳邻居**，这正是可以定量的问题：**一跳负载信息够不够？** 论文没做这个消融（对比同类工作 Wang [11] 专门用两跳信息）。
5. **$w_1:w_2=5:1$ 是手设常数**，且作者自述目的是"to effectively reduce satellite congestion"（L207）。但没有做权重敏感性——$w_1$ 再大下去会退化成纯负载均衡、时延崩坏，这个拐点在 Fig 6 上应该可见却未给。
6. **"periodically reapplied" 的地面重训**：作者说轨道可预测所以可以周期性重新下发 Q 表（L~171），但**下发周期多长、下发本身占多少带宽**完全没算，而这恰恰是"集中式"的成本项。
7. **Fig 9 把 DR-BM 从初始阶段比较中排除**——若换成"卫星刚入轨的头 N 分钟"这个真实痛点场景，正是应该比的地方。

**8. 和同批其他篇的关系**
- **与 UKBSA7WN（本批第 2 篇）是直系关系**：L63 点名 Huang [10] 就是 UKBSA7WN 的 QRLSN，批评其"relatively slow convergence"；参考文献 [10] 即 Huang et al., Chin. J. Aeronaut. 2023, 36, 284–291。两者的 Q 更新式几乎同源（都是原始 QR 的邻居 max 回传），差异集中在三处：**$\varepsilon$ 加了衰减 $\mu^t$、加了周期性广播（而非被动随包学习）、加了地面预训练**。**可以说本文 = UKBSA7WN + 三个工程补丁。**
- 与 UF8IQTA2（本批第 1 篇）：无引用关系，谱系不同（UF8IQTA2 是纯协议工程无 RL，本文是纯 RL 无协议细节）。
- 引用 Soret [26]（ICMLCN 2024, "Q-learning for distributed routing in LEO satellite constellations"）作为 DR-BM 的一半出处——**该引用是否恰当存疑**：Soret 那篇是分布式 Q-learning，而本文把 DR-BM 描述成全集中式。**这是一个值得复核的引用问题。**
- 其余 R9 篇目尚未读，暂无法比对。

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**有直接贡献，且是本批第二篇给出"负载依赖反转"的论文。** 具体：
1. **Fig 6 是一次显式的"流量负载 → 平均时延"扫描**，并且给出了方向明确的机制解释：低负载时集中式全局最短路径更快；负载升高后集中式因"inefficient packet forwarding decisions and increased queuing delays"而恶化，分布式 QR 也因"highly dynamic networks under high traffic loads"而次优（L232–L234）。**排队时延被点名为负载升高后的主导劣化项**——这是与本主题最直接相关的一句话。
2. **它与 UKBSA7WN 独立地、从不同实验设置出发得到同一个反转结论**（低负载集中式赢 / 高负载分布式赢）。两篇互为外部复现，这比任何单篇的自述都更可信。
3. **Fig 8 用"各节点包数方差"量化负载均衡**——给出了一个可迁移的负载不均衡度量，虽然只有 3000 包这一个负载点。
4. **Fig 9 触及了"初始阶段"的到达率**——即部署初期策略未收敛时的表现，但通过把 DR-BM 排除在外而回避了真正的对比。
**缺口**：负载只以"3000 packets"这类总量标量出现，**没有到达率（pps）、没有到达过程、没有队列-到达率关系**；时延分母口径把丢包混进时延；所有结论都没有数值。

**10. 一句话评价**
**"集中式预训练 + 分布式在线学"这一乘积式组合的清晰实现**，方法本体仍是 1993 年的 tabular QR（补了 ε 衰减、周期广播、地面初始化三处工程件），"Multi-Agent"只是"每星一个独立 Q 表"的叫法而非真正的多智能体算法（无协调机制、无非平稳性处理）；它最有价值的地方不是方法，而是**用另一套实验独立复现了 UKBSA7WN 那条"低负载集中式赢、高负载分布式赢"的反转**。


## UMKF328H — LEO Satellites in 5G and Beyond Networks: A Review From a Standardization Perspective

> IEEE Access, vol. 10, 2022（DOI 10.1109/ACCESS.2022.3162243）。作者：Tasneem Darwish, Gunes Karabulut Kurt, Halim Yanikomeroglu, Michel Bellemare, Guillaume Lamontagne（Carleton 大学 / Polytechnique Montréal / MDA Space）。全文 624 行，逐行读完（1–105 / 106–215 / 216–330 / 331–440 / 441–545 / 546–624 六段；**546–624 行全部是参考文献 [20]–[45]，无正文**）。

**1. 一句话**
一篇**标准化综述而非技术论文**：把 3GPP 从 Release 14 到 Release 18 关于"卫星接入 5G"的全部 Study Item / Work Item 梳理成一条时间线，再把卫星给 NR（5G 空口）造成的冲击逐项列表（传播时延、多普勒、移动小区、HARQ、PRACH、TA、功控、PAPR……），最后给出 6G 时代还缺什么标准化。

**2. 问题设定**
卫星与地面蜂窝历史上是"两个独立生态、各自标准化"（L88 附近逐字："satellites and terrestrial networks have always been considered two independent ecosystems, and their standardization efforts have proceeded independently of each other"）。5G 要卖全球无缝覆盖，就必须把卫星拉进同一套规范。它要回答的是：**3GPP 已经做到哪一步、哪些还只是 Study Item、哪些根本没人管**。谁遇到麻烦：想把卫星接入塞进 5G 核心网/空口的运营商与设备商，以及因为"没有统一标准"而被迫做封闭实现的厂商（L441 提到 DVB 的专有特性导致"interoperability problems among satellite access networks from different solution vendors, and it has led to a fragmented SatCom market"）。

**3. 方法骨架（这是综述，没有算法；骨架 = 它的分类框架）**
- **按 release 逐条梳理 3GPP 工作**（III.A，L172–L226；汇总表 Table 2）：R15 启动 TR 38.811（RAN，"Study on NR to support NTN"）+ TR 22.822（SA，"Study on using satellite access in 5G"）；R16 有 4 项（含 WI#800010-5GSAT 与 TR 28.808 的编排研究）；R17 有 TR 23.737 两阶段 + TR 28.808 + TR 38.821；R18（5G-Advanced 起点）有 920035(5GSATB)、920034(SCVS)，并列了 RAN 主题清单，其中含"**NTN evolution, including both NR and IoT aspects**"（L~215）。
- **用例分类框架**（III.B，L~228–L248，Figure 2 / Table 3）：把卫星接入 5G 的用例归为**三大类——service continuity / service ubiquity / service scalability**，Table 3 逐条列出 17 个用例及其应用（漫游、广播组播叠加、边缘内容分发、公共安全、IoT、临时卫星组件、网络韧性、回传、跨境服务连续、全球卫星叠加层、离岸风电场……）。
- **架构分类**（IV，L~252–L~270，Figure 4）：TR 38.811 的两类接入网（VSAT 宽带 / 手持窄带）；TR 38.821 的三种 NG-RAN 架构：**透明（bent-pipe）**、**再生（regenerative，又分 gNB-CU+DU 全处理 / 仅 gNB-DU）**、**多连接（multi-connectivity）**。
- **NR 冲击清单**（V，L~294–L~372）：先列设计约束（V.A，L~296–L~320），再列受影响 NR 特性与潜在对策（V.B + Table 4）。
- **管理与编排**（VI，L~350–L~368）：TR 28.808 的两套参考管理架构（3GPP RAN 融合卫星 NR-RAT / 非 3GPP 卫星 RAN），三类需求（网络切片管理、卫星组件管理、卫星组件监控）。
- **非 3GPP 组织**（VII，L~370–L~452；Table 5）：ITU-R WP 4A/4B/4C、WRC-19、IETF（MPTCP RFC 8684）、ETSI（NFV/MEC/TC-SES/OSM）、5G PPP、ECC、NICT Japan、IEEE INGR、**CCSDS**、**AEEC/ARINC**、DVB。
- **6G 未来标准化方向**（VIII，L~456–L~504，Figure 7）：A 移动性管理、B 路由、C SDN/NFV 采纳、D 智能管理与编排（ENI/SON/**SEN**）、E 容错、F 动态频谱管理。

**4. 它声称的效果**
综述没有"效果"，只有**汇总结论与它点出的空白**：
- 3GPP 的 NTN 工作"从 Release 14 就开始了"（L~170），到 R17 时 RAN1 物理层规范冻结排在 2021 年 12 月、Stage 3（RAN2/3/4）2022 年 3 月、ASN.1 与性能规范 2022 年 9 月（L~190）——**这是一篇有时效性的文档地图**。
- 明确判定管理/编排方向"**the standardization work on NTN management is nevertheless quite limited within the 3GPP working groups**"（L366 逐字）。
- 明确判定 SDN/NFV 方向"the use of SDN/NFV in an LEO SatNet **has not yet been fully investigated**"（L482 逐字）。
- 明确判定智能管理与编排：ENI 与 SON 概念"are still limited to the 5G context and may not be sufficiently agile"，而 SEN（Self-Evolving Network）"is quite a recent concept and **has not yet been considered by standardization organizations**"（L~495 一带）。
- 动态频谱管理："this issue is **not covered sufficiently** in the standardization works"（L~503）。
- **没有仿真、没有实验、没有任何性能数值**。

**5. 实验条件**
**无实验**。它的"数据"是 3GPP 文档号、release 号、会议日期（Table 6 列了 R18 Workshop 2021-06-28~07-02、RAN#93-e 2021-09、TSGs#94-e 2021-12、WRC-19 2019-10-28~11-22、AEEC KSAT 会议）。
唯一带数字的是它引述的标准指标与物理事实：
- **RTT 要求**（L250 逐字）：GEO 600–800 ms、MEO 125–250 ms、**LEO 30–50 ms**，并注明这些值"include the delays of processing on both ground and orbit as well as the variable propagation delays"。
- **单星覆盖**（L311）：550 km 高度、40° 仰角下覆盖 **1.05 百万 km²**、半径约 580 km；作为对照 5G 微蜂窝约 12.5 km²。
- **多普勒**（L315）：600 km 高度卫星在 20 GHz 下行产生 **400 kHz** 多普勒、30 GHz 上行 **600 kHz**；而 NB-IoT 系统带宽只有 180 kHz。
- **单向传播时延**（L340）：LEO 600 km 轨道**连续变化 2–7 ms**。
- 频谱（L~305）：S 波段 2×15 MHz，Ka 波段上行 2×2.5 GHz、下行 2×2.4 GHz。
- UE 速度需支持到 **1000 km/h**（L~320）。

**6. 自述局限**
**未见自述局限**——综述体裁，通篇（L84–L504 正文全部段落我已逐段读过，L506–L624 为参考文献）没有任何"本文的不足"段落。它只承认**被综述对象的不足**（3GPP 在管理编排上很有限、SDN/NFV 未充分研究、频谱管理覆盖不足、SEN 尚无标准化组织考虑）。

**7. 它没做但看起来能做的地方（基于内容）**
1. **它点名"路由"是 6G 标准化方向之一（VIII.B，L478），却只给了半页、零技术细节**。而路由恰恰是它列出的"ISL 会因高流量负载在星座某些分区拥塞"（L478 逐字："some ISLs may get congested due to high traffic loads at certain partitions of the SatNet"）这一问题的唯一解。**这篇综述把"路由"识别为一个标准化缺口，却没有梳理任何一条既有路由方案的技术谱系**（既没提虚拟拓扑、也没提 Q-routing/DRL）。这是一个明确的补白位置。
2. **它引用的 QoS 指标里明确含"packet delivery delay, packet delivery ratio"（L478）**，但没有给出这两个指标在 LEO 负载变化下的任何目标值或数据——标准里应该定什么阈值，综述没说。**给"到达率/时延"定一个可辩护的目标区间，是这篇综述逻辑上直接指向的下一步。**
3. **ITU/IETF/CCSDS 三条线（VII）各只写一两段**，其中 IETF 侧只提了 MPTCP，**完全没提 IETF 关于拥塞控制的既有标准工作**（而它在 L~426 明确说 transport area 的工作涵盖"congestion control and (active) queue management"）——这一条与路由/拥塞主题直接相关却被一笔带过。
4. **Table 1 的对比表**自我定位为"唯一同时覆盖 3GPP 活动 / 其他组织 / NR 影响 / 管理编排 / 用例 / 架构"的综述（L~108）。这是一个可被后续工作直接检验和被超越的定位声明。
5. **时效性硬伤**：正文冻结在 2022 月初（收稿 2022-02-23），R17 当时"still open"、R18 刚批准包。**R18 之后的 NTN 演进（含 IoT NTN）在这篇里完全没有内容**——L~215 只列了主题名。
6. **三大用例分类（continuity / ubiquity / scalability）从未被用来做任何定量权衡**——例如"scalability 类用例（广播/组播卸载）与 ubiquity 类用例（窄带回传）对路由的要求是否冲突"，这一层分析本可由分类框架自然导出。

**8. 和同批其他篇的关系**
本批（R9）其余篇目尚未读完，暂无法逐篇比对。**就体裁而言它与本批其他所有论文都不同**：其余是算法/协议论文，这篇是标准化综述，**没有任何算法、没有仿真、没有基线**。它与路由类论文的交集只在一处——VIII.B 节（L478）承认路由是 6G 的标准化方向，并点出 ISL 拥塞与 QoS（时延、投递率）需求，**但不引用任何一篇具体路由工作**。因此它对本批的价值是"**背景与约束的可信来源**"（LEO RTT 30–50 ms、单向时延 2–7 ms、多普勒量级、覆盖面积），而不是"方法参照"。

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**有间接但可引用的贡献——提供的是"约束数字"而非"负载-时延关系"。** 具体：
1. **它给出了 LEO 卫星接入的 RTT 目标区间 30–50 ms（L250）**，且明确这个数**包含地面与在轨处理时延**——这是任何"负载变化下的时延"研究都必须对齐的口径基准。
2. **它给出了单向传播时延在 600 km 轨道上连续变化 2–7 ms（L340）**——即"即使零负载，时延本身也是时变的"，这对"把负载导致的排队时延从总时延中分离出来"这件事直接相关。
3. **它明确把"ISL 拥塞"归因于"high traffic loads at certain partitions of the SatNet"（L478）**——这是一个标准化综述对"负载→拥塞"因果链的正式背书，可作为选题动机的外部引用。
4. **它把 QoS 要求明确表述为"packet delivery delay"与"packet delivery ratio"两个指标（L478）**——与本主题的"到达率/时延"提法几乎同构，**说明这两个指标是标准语境下的既有口径，不需要自己另造**。
5. **它指出 LEO 下"thousands of UE being connected to an LEO satellite"需要几乎同时切换（L~468）**——这是"负载在时间上高度突发且相关"的一个物理来源。
**缺口**：全文没有任何"到达率 → 时延/投递率"的曲线、模型或数据。

**10. 一句话评价**
**一篇 2022 年初冻结的 3GPP NTN 标准化地图**：价值在于把"卫星接入 5G"的制度进展、NR 冲击清单和 6G 缺口做成可检索的索引，并提供了少量可直接引用的物理约束数字（RTT 30–50 ms、单向时延 2–7 ms、多普勒 400/600 kHz）；但它**在方法谱系上不占位置**——它识别出"ISL 负载拥塞"和"路由"是缺口，却没有、也不打算梳理任何一条路由技术路线。


## VACUFEHB — Computationally Efficient Algorithms for Third Order Adaptive Volterra Filters

> 会议短文（Asilomar 系）。作者：Xiaohui Li, W. Kenneth Jenkins（UIUC Coordinated Science Lab）、Charles W. Therrien（Naval Postgraduate School）。全文 250 行，逐行读完（1–125 / 126–250 两段；L229–L232 为计算机实验、L233–L236 致谢、L237–L250 参考文献与图）。

**⚠️ 先给结论：这篇与本批主题（LEO 卫星网络 RL 路由 / 负载变化下的到达率与时延）没有任何关系。** 它是一篇**纯数字信号处理**论文，讲三阶 Volterra 自适应滤波器的快速算法。全文没有出现卫星、轨道、星座、路由、网络、队列、到达率中的任何一个概念。我不做任何强行联系。

**1. 一句话**
利用三阶（立方）Volterra 自适应滤波器在输入为**高斯过程**时自相关矩阵的**块对角结构**（式 9），把准牛顿更新解耦成三块（式 13），再用**预条件共轭梯度**（PCG）算其中那块非 Toeplitz 子矩阵的 Kalman 增益，从而把复杂度压下来。

**2. 问题设定**
带记忆长度 $N$ 的三阶 Volterra 滤波器（式 1）要建模强非线性，但输入向量 $X(n)$ 由线性项、二阶互积、三阶互积拼成后，**自相关矩阵 $R_X$ 的特征值扩散极其严重，且是非 Toeplitz 的**（L~30 附近逐字："the eigenvalue spread of the autocorrelation matrix of the third order filter input is increased dramatically. Because of this, many LMS based linear adaptive algorithms are not very effective in increasing the convergence speed. Also, because the matrix is non-Toeplitz, it is even more difficult to develop a fast adaptive algorithm"）。谁遇到麻烦：要用 Volterra 滤波器做非线性系统辨识、又跑不动传统 LMS 收敛速度的人（二阶情形的解法是作者团队自己前作 [2]，本文是三阶推广）。

**3. 方法骨架（无 RL，全是线性代数 + 自适应滤波）**
- **滤波器定义**（式 1，L~18）：$y(n)=\sum h_1 x(n-m_1)+\sum\sum h_2 x(n-m_1)x(n-m_2)+\sum\sum\sum h_3 x(n-m_1)x(n-m_2)x(n-m_3)$。
- **向量化**（式 2）：$y(n)=W^T(n)X(n)$，$X(n)$ 由六类数据向量拼成（式 3–8）：线性项 $x_1$、平方项 $x_2$、立方项 $x_3$、相邻互积 $x_{2c}$、三阶连续互积 $x_{3c}$、平方乘相邻 $x_{sqc}$。
- **关键结构发现**（式 9，L~63）：对零均值独立高斯输入，$R_X=\mathrm{diag}(R_t, R_{sq}, R_c)$ —— **块对角**，且 $R_c$ 还是**对角阵**，$R_t$ 是 $(N^2+N)\times(N^2+N)$ 非 Toeplitz，$R_{sq}$ 是 $N\times N$ 非 Toeplitz。
- **预处理链**（Fig 1，L~80 附近）：彩色高斯输入先进**线性变换去相关**，再逐路**功率归一化**，使进入 Volterra 滤波器的信号近似 i.i.d. 高斯——**这是让式 9 成立的前提假设**。
- **准牛顿更新**（式 12，L~92）：$W(n+1)=W(n)+\mu R_X^{-1}(n)X(n)e(n)$，因 $R_X$ 块对角而**解耦成三条独立更新**（式 13）：$W_t$（用 $R_t^{-1}$）、$W_{sq}$（用 $R_{sq}^{-1}$）、$W_c$（用 $R_c^{-1}$）。
- **第一块最简单**（式 14，L~130）：$R_c$ 是对角阵 → $w_{c,k}(n+1)=w_{c,k}(n)+\mu\frac{1}{\sigma_{c,k}^2}x_{c,k}(n)e(n)$。
- **第二块直接抄前作**（L~136）：$R_{sq}$ 的快速 Kalman 增益更新算法已在 [2] 的**二阶**滤波器里给出，"can be directly applied to $3^{rd}$ order"。
- **第三块是本文真正的新内容**：$R_t$ 非 Toeplitz，快速准牛顿法"simply not applicable here"（L~140），故改用**共轭梯度**（CG，2.1 节）——CG 不利用结构，所以恰好适用于非 Toeplitz 矩阵。为加速收敛再加**预条件**（2.2 节）：
  - $M_1$（式 21a）：取 $R_t$ 但把 $E[x_1 x_{2c1c}^T]$、$E[x_3 x_{2c1c}^T]$ 置零，保留左上块——**但对角上那块仍是非 Toeplitz，逆仍难算**；
  - $M_2$（式 21b）：进一步简化，只用 $E[x_{2c1c}x_{2c1c}^T]$ 沿对角线的 $N$ 个子块 → $M_2$ 成**块对角**（左上三对角 + 其余为标量 $E[x^6]$），逆极好算。**实验只用 $M_2$**。
- 完整的四步算法在 L~118–L~128 列出（Step 0 初始化 → Step 1 变换+功率归一化 → Step 2 构造三阶输入并算误差 → Step 3 分别更新三条 Kalman 增益 → Step 4 循环）。

**4. 它声称的效果**
- 只有定性结论、**没有任何数字**（L231 逐字）："the new adaptive algorithm shows dramatic improvement in convergence rate in comparison to the LMS algorithm. The results also illustrate that the chosen preconditioner chosen is very effective in improving the convergence rate."
- 唯一的对照基线是 **LMS**（学习曲线画在同一张 Fig 2 上）。
- **没有复杂度表达式**：文中反复说"computationally efficient""much simplified""dramatic improvement"，但**从头到尾没有给出新的 $O(\cdot)$ 阶数**（只提到用传统求逆需 $O(N^3)$ 量级的乘法数，L~138 一带写作"o(Nq multiplications"，OCR 有损坏）。

**5. 实验条件**
- 任务：辨识一个**三阶非线性系统**（L231）。
- 输入：**彩色高斯信号**，由一个**二阶低通滤波器**产生。
- 变量：每次更新时用 **1 次迭代 / 2 次迭代 / PCG 全迭代** 三档，比较收敛速度。
- 预条件器：只用 $M_2$。
- 基线：LMS。
- **训练与评估**：就是一次系统辨识仿真，没有训练/测试划分概念。
- **全文只有一张结果图（Fig 2）**，MD 中不可读，正文没有任何坐标值。

**6. 自述局限**
**未见自述**。全文（L1–L250）没有任何 limitations / future work 段落，也没有讨论 $M_1$ 与 $M_2$ 的取舍代价、或 CG 迭代次数与收敛的权衡。

**7. 它没做但看起来能做的地方（基于内容）**
1. **$M_1$ 被提出来但没被实验**：作者说 $M_1$ 的对角块仍是非 Toeplitz"so it is still computationally intensive to calculate its inverse"（L~215），于是跳到 $M_2$。**$M_1$ 与 $M_2$ 之间"逼近程度 vs 求逆成本"的定量权衡从来没做**。
2. **"dramatic improvement"没有任何数字**——收敛速度提升了几倍、达到同一误差需多少样本，均未给。
3. **没有复杂度阶数**：既然标题就叫"computationally efficient"，给出新算法的乘法数/迭代数与 LMS、与全矩阵求逆的对照是分内之事。
4. **彩色高斯 + 线性变换去相关这个前提从未被检验**：式 9 的块对角性依赖"线性变换能完美去相关"（L~85 逐字"If the input signal x(n) is stationary..."与前面"Assuming the linear transform can perfectly decorrelate"）。**去相关不完美时结构退化多少、算法是否还成立，全文没测**。
5. **只辨识三阶非线性系统、只测一种输入谱**，没有扫输入相关性强度（即低通滤波器的极点位置）——恰好这是最能暴露"去相关假设是否脆弱"的轴。

**8. 和同批其他篇的关系**
**与同批任何一篇都没有关系。** 本批（R9）其余篇目围绕 LEO 卫星网络路由/标准化展开（UF8IQTA2、UKBSA7WN、UKEKU5ZG、UMKF328H 等），本篇属于 IEEE 信号处理社区，引用文献只有 4 篇（[1] 作者前作 Asilomar 1996、[2] Marshall & Jenkins 1992 快速准牛顿、[3] Hull 博士论文 1994、[4] Golub & Van Loan 矩阵计算），**没有一篇与网络/通信/卫星相关**，也不被本批任何论文引用。它在语料中的存在更像是**检索/归档环节误入的条目**——这本身是一条关于语料构成的观察，值得主控记录。

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**没有直接贡献，也没有间接贡献。** 它处理的"信号"是**音频/一般时间序列意义上的输入样本**，不是网络流量；它优化的"收敛速度"是**自适应滤波器系数收敛到维纳解的样本数**，不是端到端时延或投递率；它的"条件数/特征值扩散"是**数值线性代数概念**，与队列拥塞不是同一件事。
**唯一需要说明的是我为何不做联想**：本主题里有"到达率"和"队列"两个词，本篇里有"输入过程"和"能量/功率"，表面词汇可以搭桥（例如把流量到达建模成有色高斯过程），但那是**本文完全没有做、也完全没有声称的事**。按任务纪律，我如实写"没有直接贡献"，不硬扯。

**10. 一句话评价**
**一篇与 LEO 路由主题无关的数字信号处理短文**——用"高斯输入下三阶 Volterra 自相关矩阵块对角"这一结构性质 + PCG 预条件 $M_2$ 来替代无法用于非 Toeplitz 矩阵的快速准牛顿法；方法谱系上它是作者团队二阶工作 [2] 的三阶推广，**且通篇无一个数值**。放入本语料属误入条目。


## VFS59FHI — Load-Balancing Routing Algorithm Based on Segment Routing for Traffic Return in LEO Satellite Networks

> IEEE Access, vol. 7, 2019（DOI 10.1109/ACCESS.2019.2934932）。作者：Wei Liu, Ying Tao, Liang Liu（中国空间技术研究院 通信卫星研究所）。全文 365 行，逐行读完（1–120 / 121–250 / 251–365 三段；L307–L365 为参考文献与作者简介）。

**1. 一句话**
针对"**地面信关站集中在有限区域内**"这一真实部署约束造成的回传汇聚拥塞，把 LEO 星座按"信关站 + 反向缝（reverse slot）"的相对位置**动态切成轻载区与重载区**，轻载区用预均衡最短路径、重载区用基于**拥塞指数 $c(e)=F(e)/r(e)$** 的最小权路径，再用 **Segment Routing** 把跨区路径串成一致转发。

**2. 问题设定**
LEO 星座（Iridium NEXT / Starlink）的地面信关站**只能布在有限地理区域内**，而各类业务的回传流量（IoT 回传、数据回传）会向这一小片区域汇聚 → 信关站周边链路"severe link congestion and excessive link load"（L19 段附近）。作者在相关工作里明确点出这个前提**以往研究重视不足**（L35 逐字："the restriction that ground gateway stations are arranged within a limited area does not receive enough attention"）。物理上还有第二个麻烦：Walker 星座首末轨道间存在**反向缝**，那里的卫星之间不建 ISL（L~56），它会**切断**本来可用的绕行路径。谁遇到麻烦：信关站上空那几颗卫星及其周边链路，以及因此被拒绝的回传业务。

**3. 方法骨架（非 RL，协议/图论工程）**
- **系统模型**（III 节，L52–L58）：Walker 星座 $N=n\times m$（$n$ 轨道 × $m$ 星/轨道），极轨均布；节点集 = 卫星 $V_S$ + 信关站 $V_{GW}$（$X$ 个）+ 中心站 $v$；链路集 = 星间链路 $E_{ISL}$（带宽 $B_{ISL}$）+ 馈电链路 $E_F$（带宽 $B_F$）+ 地面链路 $E_G$（**带宽视为无限**）。除反向缝附近外每星 4 条有向星间链路。用 **VT（虚拟拓扑）** 处理动态性，地面按**地理栅格（traffic cell）**离散化。
- **流量模型**（III.B，L60–L74）：每个栅格绑定一颗星；栅格 $k$ 有**流量密度 $f^{(k)}$**（= 该栅格业务需求 / 系统最大流量需求，按地理位置和人口**预测**标定），实际需求 = $u\times f^{(k)}$，$u$ 为单位业务值。链路 $e$ 承载总流量 $F[e]$（式 2、3）。**优化目标**（III.C，L76–L84）：最大化相对吞吐 $T$，约束是 $F[e_{ISL}]\le B_{ISL}$、$F[e_F]\le B_F$。
- **负荷分区**（IV.A，L121–L135）：把信关站所在区域按地面栅格**外扩成矩形**，矩形内 = 重载区（$y_n$ 轨道 × $y_m$ 星/轨道），矩形外 = 轻载区。分区**动态**取决于反向缝位置：反向缝穿过信关站区域时以信关站为中心扩展；反向缝在信关站区域外时，**只把含信关站但不含反向缝的区扩进重载区**，以避免反向缝割裂重载区（Fig 4(a)(b)）。
- **轻载区路由**（L~137）：路径必须经过重载区最外圈节点（outermost nodes）。用 **最小生成树（MST）** 生成最短路（作者理由："traffic of light load zone is at a low level, which can improve the delay performance and reduce SR overhead"）；再做**预均衡**——统计各 outermost node 被占用次数 $x_i$，把链路权值调成 $(0.5+0.1\times x_i)$（0.5 是初始权值、0.1 压量级防过调），然后在**预均衡后的网络**上重算以中心站为源的 MST，取反向后截取轻载区部分。
- **重载区路由**（L~139–L~160）：重载区节点只在区内路由、不进入轻载区；outermost node 承载"本地业务 + 轻载区汇入业务"两部分，按**流量从大到小排序优先路由**（"the larger the traffic, the shorter the path"）。
  - **拥塞指数**（式 4，L143）：$c(e)=F(e)/r(e)$，$r(e)=b(e)-F(e)$ 为剩余带宽；$r=0$ 时 $c=\infty$，空链路时 $c=0$。
  - ⭐ 作者对选 $c(e)$ 而非链路利用率 $F(e)/b(e)$ 给了明确理由（L145 逐字）："Compared with link utilization $F(e)/b(e)$, $c(e)$ is more monotonically incremental to $F(e)$ and more sensitive to load change. $c(e)$ would increases sharply if the traffic is too larger which is good to balance the network load."
  - **链路权值**（式 5，L154）：$w(e)=0.01+c(e)$（空链路 = 0.01，剩余带宽为 0 时 $w=\infty$）；路径权值 $w(P)=\sum_{e\in P}w(e)$（式 6），路径剩余带宽 $r(P)=\min_{e\in P}r(e)$（式 7）。
  - 剩余带宽不足的链路**直接删除**，再在权值网络上跑 **Dijkstra**（起点为卫星、终点为中心站）。**找不到路 → 该业务被拒绝并丢弃**（L~160）。
- **Segment Routing**（II.B，L37–L50）：用 Node SID / Adjacency SID / Service SID 三种段标识 + CONTINUE / PUSH / NEXT 三种操作，把跨区路径压成段列表（SL），使中间路由器不必维护全路径信息——**这是让"分区不同策略"能无缝拼接的机制**。
- **复杂度**（IV.B，L~172）：轻载区 $O(N^2)$，重载区 $O((y_n y_m)\times(y_n y_m+X+1)^2)=O((y_n y_m)^3)$，合计 $O(N^2+(y_n y_m)^3)$。极端情形 $y_n=y_m=0$ 时退化为 $O(N^2)$。

**4. 它声称的效果**
- 场景：Table 1（L174）**6 轨道 × 12 星 = 72 颗**、极轨 90°、轨道间隔 30°、**4 个信关站**、$B_{ISL}=25$、$B_F=100$。
- 重载区尺寸扫描（Table 2，L180–L186）：$y_n\in\{3,4,5,6\}$，各种 $y_m$，直到 $(6,12)$ 即**全网都是重载区**。
- 五种指标（V.A，L~200）：平均拒绝率、平均相对吞吐、最大链路利用率、平均时延、平均抖动。
- 结果：
  - **$(6,12)$ 在均匀分布下五个指标全是最优/阈值**（L207、L~211、L~215 等）；预测分布下 $(6,12)$ 的**平均拒绝率为 0%**（L209）。
  - 规律：拒绝率随重载区尺寸扩大而下降、吞吐上升、最大链路利用率下降；**但平均时延随尺寸扩大而上升**（成本项）。
  - **单维度扩展收益很小**（L~302 逐字："The increase of one dimension only can get little benefit, such as (3,2), (4,2), (5,2), (6,2)"）——必须两个维度同时扩。
  - ⭐ **一条反直觉结论**（L269 逐字）："However, the average delay decreases as u increases with some sizes. This phenomenon is caused by **big rejection ratio, and only part of traffic can occupy resources**. When the rejection ratio is small, the average delay increases as the size extends." —— **负载升高反而使"平均时延"下降，因为被拒绝的业务不计入统计**。
  - 对比（Fig 17，L294）：**Dijkstra 平均时延最小但拒绝率最高**；HRA 拒绝率改善但**时延最高**；JDDA 拒绝率更小但时延更高；本方法**拒绝率最小且时延较小**。对比时选尺寸 $(6,5)$ 以平衡收益/成本/复杂度（L300）。
- 抖动（式 12）：随尺寸波动、"acceptable when the rejection ratio is small"（L~290）。
- ⚠️ **全文没有一个绝对数值**：所有指标都只有曲线（Fig 7–17），正文只给相对趋势和"0%"这一个例外。

**5. 实验条件**
- 星座与带宽见上（Table 1）。
- **流量栅格**（Fig 6，L~176）：一张 6×12 的栅格图，格内数字是**预测得到的流量密度**（图在 MD 中严重损坏，只能看出量级 $10^{-3}\sim10^{-1}$ 与个别大值如 0.86、0.938）。
- 两种分布：**均匀分布**（所有密度 = 1）与**预测分布**（Fig 6）。
- 单位业务值 $u$：均匀分布取 **1, 2, 3**；预测分布取 **4, 5**（作者理由：预测分布里有些密度很小，网络有足够余量）。
- 仿真用 **C++** 自写（L~200）。
- **评估的是静态快照式的路由结果**，没有排队过程、没有到达过程、没有时间演化——"到达"只以栅格需求 $u\times f^{(k)}$ 的形式出现。
- 无训练环节（非学习算法）。

**6. 自述局限（L306 逐字，全文唯一一处）**
"The results could be a solution for congestion problem in LEO satellite networks, and the entry point is traffic return. **The extension to all types of traffic and the design of on-satellite router** could get more attention in further discussion."
（两条：只处理了"回传"这一类流量；星上路由器的设计未涉及。**未见**对时延口径问题、$u$ 缺绝对单位、反向缝建模简化等的任何自述。）

**7. 它没做但看起来能做的地方（基于内容）**
1. ⭐ **它自己发现并写出了"拒绝率升高 → 平均时延下降"这个统计假象（L269），但只把它当作现象解释了一句，没有修正口径**。式 11 的 $D_T$ 分母是"成功传输的栅格数 $|S_S|$"——**分母随负载变化**。作者甚至观察到"当拒绝率小时，时延随尺寸增大而上升"这一相反趋势，**却把两者并列陈述而不追问哪个才是真实趋势**。这是本文最锋利、也最容易补的一刀：**同时报"含拒绝的端到端时延"与"仅成功业务的时延"**，或明确把拒绝写成独立维度。
2. **拥塞指数 $c(e)=F(e)/r(e)$ 是有理函数，在 $r\to0$ 时发散**，作者只用一句"more sensitive to load change"作为优点（L145）。**发散行为的后果（权值数值爆炸、Dijkstra 的数值稳定性）从未被检验**，也没给与 $F/b$ 的对照实验——而这本是一个一页就能做的消融。
3. **$(6,12)$ 即"全网重载区"在几乎所有指标上最优**，这意味着**分区机制本身带来的收益可疑**：如果最优解是"不分区"，那么轻载区/重载区这套划分的价值主要体现在**复杂度**（$O(N^2)$ vs $O((y_ny_m)^3)$）而非性能。作者选了 $(6,5)$ 做对比是出于折中，**但没有做"$(6,12)$ 与 $(6,5)$ 的指标差值 vs 复杂度差值"的显式权衡曲线**。
4. **0.5 与 0.1 两个常数是手调**（L~137："0.5 is the initial link weight... 0.1 is used to reduce the order of magnitude for $x_i$ avoiding over-adjustment"），**未做敏感性**。
5. **$u$ 的单位被作者刻意剥离**（III.B 逐字："Units of traffic value and u are the same as units of $B_{ISL}$ and $B_F$, so the traffic in this paper can be considered as the relative traffic based on 1 unit bandwidth"）。这使得**结果无法与任何真实业务量对齐**，也无法与其他论文的数字比较。
6. **反向缝的处理是硬约束**（那里没有 ISL），但**没有测反向缝扫过网络时的瞬态**——分区是"动态"划分的，可全文只给了静态情形下的结果，**切换瞬间的路由抖动/重路由代价完全没测**（式 12 的 jitter 是时延标准差，不是重路由代价）。
7. 业务**不可拆分**（要么全过要么被拒绝），而 SR 本身支持段列表——**做部分分流/多路径回传是现成的机制**，作者没做。

**8. 和同批其他篇的关系**
本批（R9）其余篇目尚未读完，暂无法逐篇比对。就谱系看，它与 UF8IQTA2 同属"**非学习的经典路由/负载均衡**"一线（都靠启发式规则而非学习），但**切入角度完全不同**：
- UF8IQTA2 的驱动因素是"星间链路不稳 + 负载不均"，用**预测**做前馈避让；
- 本篇的驱动因素是"**地面信关站地理集中**"这一**部署约束**（这是本批迄今唯一以信关站布点为第一性问题的论文），用**分区 + Dijkstra 权值**做反应式分流。
它把 MIRA[8]、DT-TTAR[9]、DTBR[10]、HRA[11]、JDDA[12] 列为相关工作，其中 HRA 与 JDDA 是它的对比基线。**它不引用本批其他任何一篇。**

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**有强直接贡献，而且是本批迄今对本主题最"扎心"的一篇。** 三条：
1. ⭐ **它实测并写出了一个会污染整个子领域的统计陷阱**（L269）：在式 11 的时延口径（分母 = 成功传输的栅格数）下，**负载 $u$ 升高时平均时延反而下降，因为被拒绝的业务不进入统计**。它同时观察到"拒绝率小时，时延随尺寸（承载能力）扩大而上升"。**这两条放在一起意味着：在存在拒绝/丢包的系统中，"负载 ↑ → 平均时延 ↑" 这条常识并不自动成立，取决于分母怎么定义。** 这对任何要做"到达率 → 时延"曲线的工作都是必须先定的口径问题——**主控在汇总时应把这条单列**。
2. **拒绝率 vs 时延构成一对显式的对立指标**（L294）：Dijkstra 时延最低但拒绝率最高、HRA 拒绝率改善但时延最高——**说明"降时延"和"降拒绝"在拥塞路由里是可分离甚至对立的目标**，不能只报一个。
3. **给出了一条"承载能力 → 时延"的单调关系**：在拒绝率小的前提下，**重载区（即可用于绕行的区域）越大，平均时延越高**（L~302、L~316）——即**负载均衡能力是用时延买来的**，这为"负载 vs 时延"的权衡提供了机制性证据。
**口径缺口**：它的"负载"是**静态的栅格需求 $u\times f^{(k)}$**，不是到达率；链路带宽只有 25/100 两个抽象单位，没有 pps、没有队列、没有到达过程——**所以它给的是"负载水平 → 稳态指标"，不是"到达率 → 时延"的动态关系**。

**10. 一句话评价**
**一篇把"信关站地理集中"当作第一性问题、用"分区 + 拥塞指数权值 + SR 拼接"求解的经典（非学习）负载均衡路由论文**；它在本批里的独特价值不在方法（Dijkstra + 手调权值，基线也全是同类启发式），而在于它**诚实地记录下了"高负载下平均时延反而下降"这一指标口径假象**——这是全库少见的、关于"怎么测"的自觉。


## W5Z39E25 — A Wised Routing Protocols for Leo Satellite Networks

> 会议短文（OPNET 仿真）。作者：Saeid Aghaei Nezhad Firouzja（上海交大）、Muhammad Yousefnezhad（南京航空航天大学）、Masoud Samadi, Mohd Fauzi Othman（马来西亚理工大学 UTM）。全文 167 行，逐行读完（一次读完全文；L143–L167 为参考文献）。

**1. 一句话**
把星上**分组调度**（PQ + WRR 混合，实时业务走严格优先级、非实时业务按权重分剩余带宽）与**基于卫星忙/闲状态的备用路径绕行**合起来：用**业务到达率 $\lambda$ 与两个阈值 $\alpha$（闲）/ $\beta$（忙）** 判定每颗星的状态，忙星被通告给邻居与路由控制中心（控制中心把它从拓扑里删掉并重算备用路由表），低优先级业务改走备用路径。

**2. 问题设定**
两类麻烦叠加（L23 逐字）："the resource onboard is constrained, **load distribution on satellite is unbalanced in terms of time and space**, traffic on board is constantly changing with the moving of sub-satellite point, these lead to congestion of some satellite node in the network, due to which network throughput drops"。多业务 QoS 差异化是第二个约束：实时业务（class A）要"three low one guarantee"（低时延、低抖动、低丢包、带宽保证），非实时业务（class B）"usually use **traffic arrival rate** as its QoS measure"（L27）。作者还担心一件事：纯优先级调度会让**低优先级业务被"饿死"**（"avoid low priority traffic to be 'starve' due to their weak resource competitiveness"，摘要 L9–L10）。谁遇到麻烦：被抢占到几乎没带宽的 class B 业务，以及因热点汇聚而过载的那几颗星。

**3. 方法骨架（非 RL，排队调度 + 状态路由）**
- **星上调度：PQWRR**（I.A 节，L25–L33，Fig 1）。class A 进**高优先级队列**（严格优先级 PQ）；class B 按服务等级进多个低优先级队列，**仅当 A 队列为空时**才按 **WRR** 分剩余带宽。作者自述这是"combines the advantages of algorithms WRR and PQ, overcomes their both shortcomings"（L33）。
- **双路由表**（L36–L46，Fig 2）：
  - **最短路径路由表（route table1）**：基于**虚拟拓扑（VT）**、按每个时隙的拓扑结构**离线计算**（L38 逐字："established based on virtual topology and calculated offline according to the network topology structure within each timeslot"）。
  - **备用路由表**：基于拥塞控制。
- **⭐ 状态判定与阈值**（L43 逐字，全文核心机制）："For satellite traffic arrival rate $\lambda$ set two state thresholds: **idle threshold $\alpha$ and busy threshold $\beta$**; Satellite nodes keep track of their own traffic arrival rate, when $\lambda>\beta$ namely determining satellite into busy state, when $\lambda<\alpha$ determining satellite into idle state, defining $\alpha<\lambda<\beta$ as a transition state."
  - ⚠️ **$\alpha$ 与 $\beta$ 的具体取值全文从未给出**（我逐段检查了 I.A、II、III、IV 各节，无任何数值或选取规则）。
- **状态传播**（L43–L44）：状态变化时通告邻居与路由控制中心；邻居收到"busy"信号后减少发往该星的流量；**控制中心把忙星从网络拓扑中移除并重算备用路由表**。
- **转发判决**（L45 逐字）：先按最短路径表找下一跳 → 若下一跳**闲** → 直接转发；若**忙** → 按业务类别分流：**class A 仍然直接转发**（不绕行），**class B 查备用路由表找新下一跳**；若找不到符合条件的下一跳，class B **进入 routing waiting queue** 等待路由表更新。
- **拓扑约束**（L38–L40）：每星 4 条链路 = 2 条 ISL（同轨，长度基本恒定、连接常驻）+ 2 条 IOL（异轨，长度随卫星移动变化、**过境高纬度且可见角过小时会关闭**、**跨缝（cross-seam）卫星之间没有 IOL**）。
- 无学习、无 RL；拥塞控制是**规则式**的（阈值 + 拓扑删点 + 重算）。

**4. 它声称的效果**
- **丢包**（Fig 8–10，L89–L91）：卫星 S-1-1 在第 **11 min 和 20 min** 丢包；S-1-4 在第 **10 min**；S-5-4 在第 **4 min**。
- ⭐ **一条明确的时空相关结论**（L91 逐字）："At the same time packet loss status on different satellites is **significantly different**, existing traffic unbalance in time and space, **packet loss rate is a function of time and space**."
- **分级丢包**：class A 丢包率**恒为 0**（抢占权）；class B 在资源紧张时丢包；**拥塞较轻时只有最低权重的 B0 丢包**，拥塞加重后**所有 B 类都不同程度丢包**（L91）。
- **跳数**（Fig 11，L~101）：class A 恒走最短路径，跳数在 6–7 之间；**第 12 个路由跳时 A 跳到 9**，原因是"time-slot updates during the traffic routing process, route table changes, routing path shifts"；拥塞时 class B 跳数增加，**多数情况下增幅不超过 2，但某些时刻备用路径跳数极大，class B 最大跳数达 14**（L~101）。
- **端到端时延（CDF 的 90 分位，L126，全文唯一一组绝对数值）**：
  - PQWRR（不绕行）：class A **< 102 ms**、B2 **< 98 ms**、B1 **< 567 ms**、B0 **< 790 ms**。
  - 复合策略（PQWRR + 备用路径）：B2 **< 136 ms**、B1 **< 145 ms**、B0 **< 460 ms**。
  - ⚠️ **注意 B2 从 98 ms 恶化到 136 ms**，而论文只写"ETE delay performance of traffic class B with different weights has been significantly improved"（L126），**对这一处恶化未作任何说明**。
  - class A 的 ETE 时延"remains around **100 ms**"、抖动较小（L~103）。
- **吞吐**（Fig 16/17，L~132）：纯 PQWRR 下 class B0 吞吐**仅约 15 packets/s、吞吐率仅 60%**；复合策略下各类业务吞吐"more than 90"（单位疑为 %，原文截断）。
- **时延抖动**：class B 抖动严重（结论 L138 自认："although under this policy the delay jitter of class B is severe"）。

**5. 实验条件**
- **星座**（L79）：Iridium 模型，**6 个轨道面 × 每面 11 星**（= 66 颗）、**780 km**、纬度阈值 **60°**、最小仰角 **8.2°**；轨道文件用 **STK** 生成后导入 **OPNET**。
- **星上参数**（L79）：**包长 1000 bits**、**星上处理速率 500 packets/s**、**缓存队列长度 50 packets**。
- **业务构成**（L79）：class B 分 B0/B1/B2，权重依次增大；A、B2、B1、B0 **各占 25%**。
- **业务背景**（L81）：用文献 [10] 把地球分成 **12×24 栅格**并给出每格业务需求预测（Fig 7）；用文献 [11] 的**洲际流量比**（Table 1，如北美→北美 86.18、欧洲→欧洲 55.88 等）确定目的地址。
- **源/目的**（L81）：源 (56°S, 26°E)、目的 (65.2°N, 58°W)，**两点间总业务需求 100 packets/s**。
- **两个仿真场景**：分别验证 PQWRR 调度与复合路由算法，**各仿真 30 min**。
- **训练/评估**：无训练（非学习算法）。
- ⚠️ **只有单一负载点（100 packets/s）**——全文没有扫过到达率。

**6. 自述局限（L140 逐字，全文唯一一处）**
"But in this paper **how to choose state threshold, has not been discussed**, the selection method will be the focus of our future research."
（即承认 $\alpha$、$\beta$ 的选取方法没做。**未见**对 B2 时延恶化、单负载点、3 个方向状态（闲/过渡/忙）中"过渡态"如何处理等的任何说明。）

**7. 它没做但看起来能做的地方（基于内容）**
1. ⭐ **$\alpha$ 与 $\beta$ 从未给定值，而整个机制（忙/闲判决 → 删点 → 重算路由）完全建立在它们之上**（L43）。作者把这一点写进了局限。**这是本文最大、也最容易补的缺口**：阈值敏感性、阈值与负载水平的关系、阈值是否需要随星座位置自适应——全是现成的实验。
2. **"过渡态"被定义了但从未被使用**：L43 定义 $\alpha<\lambda<\beta$ 为 transition state，可**后文的转发判决只用"idle"和"busy"两个分支**（L45）。**过渡态在机制里没有任何作用**——定义与用法脱节。
3. **只测了一个负载点 100 packets/s**，而全文的核心机制（阈值判定）恰恰是**负载的函数**。没有到达率扫描，就无法知道阈值机制在什么负载区间才起作用。
4. **它自己写了多径的代价，却没把它纳入决策**（L36 逐字）："if only a small amount of traffic needs to be transported, using multipath routing may cause waste of network resources"。即**低负载下绕行是浪费**——这是一个明确的、作者已经识别出的"负载依赖"开关，但转发判决里**没有任何基于负载水平启用/禁用备用路径的逻辑**。
5. ⭐ **它给出了排队时延与路径长度的显式权衡**（L115 逐字）："although the **queuing delay on single satellite reduced**, but the **routing hop count get larger, times of queued get larger, path length get longer**, these lead to the increase of delay"。**这是"降排队但增跳数"的清晰机制描述**，但作者只当解释用，没有把它做成优化目标或分离测量。
6. **B2 的 90 分位时延从 98 ms 恶化到 136 ms**（L126），与全文结论相反，**未解释**。
7. **class A 时延 ~100 ms 在 Iridium 780 km 下偏高**（若纯传播，源目的跨半球约 4–6 跳、单跳 ~10 ms 量级），暗示排队/处理占比不小——**但论文没做时延分解**。
8. 控制中心**全局重算备用路由表**是集中式的，**重算频率与信令开销未计**。

**8. 和同批其他篇的关系**
本批（R9）其余篇目尚未读完，暂无法逐篇比对。就谱系看：
- 它与 **VFS59FHI（本批第 6 篇）最接近**——两者都是**非学习的经典拥塞路由**，都用"虚拟拓扑 + 离线最短路 + 拥塞触发的绕行"，**且都以"排队时延 vs 绕路成本"的权衡为隐患**。差别在触发信号：VFS59FHI 用**链路拥塞指数 $c(e)=F(e)/r(e)$**（连续量、算在链路上），本篇用**节点到达率 $\lambda$ 对阈值**（离散三态、算在节点上）。
- 它与 **UF8IQTA2（本批第 1 篇）也同源**：都是"节点自报拥塞状态 → 上游改路"（UF8IQTA2 用预测流量 vs 邻居均值阈值 + RCS 信号；本篇用实测到达率 vs 固定阈值 + busy 信号），**且两篇的阈值都是手设常数、都不做敏感性分析**。
- 本篇不引用本批其他任何一篇；其参考文献 [1]–[11] 大量为中文文献与教科书。

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**⭐ 有直接且强相关的贡献——本批迄今"到达率"出现得最实质的一篇。** 三条：
1. **它把"业务到达率 $\lambda$"直接作为状态变量**（L43），并给出三态划分（$\lambda>\beta$ 忙 / $\lambda<\alpha$ 闲 / 中间过渡）。这是全批少见的**把到达率写进判决逻辑而非只写进实验轴**的做法。**但阈值从未给值，因此这条贡献是"机制存在、参数缺失"的半成品。**
2. **它给出了带绝对数值的时延-负载分级结果**（L126）：同一网络、同一负载（100 packets/s）下，**不同优先级业务的 90 分位时延跨越 98 ms → 790 ms 近一个数量级**。这直接说明：**在拥塞的 LEO 网络里谈"时延"必须绑定业务类别**，单一平均数会掩盖一个数量级的差异。
3. ⭐ **它写清了"降排队时延"与"增路径长度"的对冲机制**（L115）：绕行到空闲星后**单星排队时延下降，但跳数与排队次数上升、路径变长**，净效应可能是**时延不降反升**（"at some point the time delay of class B has not been improved obviously"）。**这正是"负载变化下时延"问题的核心张力**，而作者是把它当作现象解释、而非研究对象。
4. **"packet loss rate is a function of time and space"**（L91）——给出丢包率随卫星/时刻显著不同的实测观察，是"负载时空不均"的直接证据。
**口径缺口**：只有**一个负载点**（100 packets/s）、无到达率扫描、无队列-到达率关系、阈值未定值；时延用 CDF 的 90 分位报告（比均值好），但**未说明被拒绝/丢包的业务是否计入 CDF**。

**10. 一句话评价**
**一篇用"到达率阈值三态 + 双路由表 + PQWRR 调度"处理多业务拥塞的工程型路由短文**；机制上它同时触及了本主题最关心的两件事——**把到达率当状态变量**、**指出降排队会以增跳数为代价**——但两件都停在半途（阈值从不给值、单负载点验证），属于"**问题提得准、证据给得少**"的一类。


## W6M3GU7L — A Characterization of Route Variability in LEO Satellite Networks

> 测量/表征类论文（Georgia Tech；NSF 2212098 + Google/Cisco/VMware 资助）。作者：Vaibhav Bhosale, Ahmed Saeed, Ketan Bhardwaj, Ada Gavrilovska。全文 510 行，逐行读完（1–110 / 111–225 / 226–340 / 341–510 四段；**L341–L510 全部是参考文献**）。

**1. 一句话**
不做新算法，而是**用实测把 LEO 星座路由的"抖动"本身量化清楚**：星间链路（ISL）其实很稳、地面-卫星链路（GSL）才是抖动之源；由此产生的**路径频繁切换（route churn）既普遍、又大多无必要、还有害**——贪心最短路径会让同一城市对的全部流量挤到同一条路上，把网络利用率与拥塞控制性能一起拖坏。

**2. 问题设定**
LEO 星座每 100 分钟绕地一圈、卫星时速 27 000 km/h（L13 附近），单颗星对任一地面站最长可见仅 **4.5 分钟**（L~50）。于是路径特性不断变化、触发**重路由事件**。作者要问的是：这些重路由**值不值**？谁遇到麻烦（摘要 L9 逐字）："Frequent rerouting can cause poor performance for **path-adaptive algorithms** (e.g., congestion control)." 即所有根据路径状态调整发送速率的传输层算法（BBR/Cubic/Vegas/PCC 等）会被这种抖动坑掉；此外高 churn 也让流量工程难做（L15）。

**3. 方法骨架（无算法创新，是"测量学 + 反例构造"）**
- **工具链**（§3，L75–L79）：**Hypatia** 仿真框架生成 **TLE** 并确定 ISL/GSL 连通性（用 SGP4 模型逐时刻算卫星位置）；**不使用 Hypatia 的包级仿真器**（L77 逐字："We do not use the packet-level simulator provided by Hypatia"）；把 Hypatia 采到的时延喂给 **Mahimahi** 做网络条件仿真，再叠 **Pantheon** 跑真实拥塞控制实现。
- **路由口径**（L77）：Hypatia 的最短路每 **100 ms** 重算一次，作者**降采样到 1 s** 以加速仿真。
- **拓扑假设**（§2.2，L~58–L72）：**+Grid** 配置（每星连本轨 2 颗 + 相邻轨各 1 颗）、**相位偏移 0.5**（贴合 Starlink 参数）、**静态 ISL 配置不做重配置**（理由：ISL 建立需数十秒到约一分钟，频繁重配会使其失去价值）。作者还额外做了**+Grid 变体对照实验**（§2.2 末，L~69）：若改为"连最近邻"的朴素 +Grid，最坏情况下路径长 5 倍以上、最大/最小 RTT 比可 **>7**，而他们采用的变体只有约 **2.7**——据此选定"最小化路径长度抖动"的那个变体。
- **⭐ 两个核心度量**（§4.1，L85–L88）：
  - **lifetime（寿命）**：一条路径保持**可用**的时长——由拓扑动力学决定；
  - **usage time（使用时长）**：一条路径**被路由算法选中**的时长——由算法决定。
  - 两者之比就是"churn 被算法额外放大了多少"的度量。
- **"最长最短路"（longest shortest path）**（L129）：在所有被选中的最短路里挑最长的那条。**最小 RTT 与它的比值 = 高 churn 所能带来的最大收益上界**。
- **三个研究问题**：§4 churn 有多普遍/是否必要/有没有害；§5 RTT 抖动的来源（ISL/GSL 分解）；§6 加卫星能不能减少抖动。

**4. 它声称的效果（本批迄今数字最密的一篇）**
- **churn 之普遍**（L99、L111）：**15%（Starlink）/ 20%（Kuiper）/ 约 8%（Telesat）** 的路径**使用时长不足 10 秒**；Telesat 更低是因为轨道更高、可见更久。**至少 50% 的路径，使用时长不到其寿命的一半**。
- **churn 之不必要**（L129）：**70% 的源目的对的"最大可能收益"小于 25%**（即放弃一条路最多省 25% 时延）。具体案例 **Jakarta–Bogotá**（L136）：200 秒内 **8 次路径切换**，前 42 秒就切了 4 次，其中第二次切换是因为两条路径时延差 **0.005 ms**；**最大时延收益仅约 3.5 ms（约为总 RTT 的 2.5%）**。
- ⭐ **churn 之有害**（§4.3，L143–L163）：
  - **流量集中**：构造纽约 2000 节点 ↔ 伦敦 2000 节点的场景（各均匀分布在半径 22 km 圆内），结果是"**all connections flock to the same path**"（L147 逐字）——**全部连接挤到同一条路径上**，只为了约 0.5 ms（约 1–2%）的时延差，且 28 秒后又集体切回来。作者据此指出**贪心最短路径制造热点、浪费网络容量，并带来潜在安全隐患**（L15 提到 [34]）。
  - **拥塞控制受害**（Table 2，L163）：在 Pune–Lahore 路径上做 60 秒实验，带宽在 204/48 Mbps 之间切换（贴合 Starlink 规格），三种情形（恒定带宽/变 RTT/变带宽/两者都变）下测 **BBR、Cubic、PCC-Allegro、PCC-Vivace、Vegas** 的利用率、95 分位单向时延与 power（利用率/时延）。结论逐字："**No single algorithm optimizes both delay and utilization**"；BBR 利用率最高（95.4%）但时延大，Vegas 时延低但利用率最差（10.1%），PCC 两兄弟利用率 60–85% 且时延较低。
- **RTT 抖动幅度**（摘要 L9、L19）：同一对地面站之间**最小可达 RTT 可增大到 2.5 倍**。
- ⭐ **抖动有空间结构**（§5.1，L171–L178）：用 3 个源站（Null Island 0°、Darfur 14.4°N、Kyiv 50.45°N）× 2700 个均匀分布目的站做热力图。**高抖动只出现在两站间距 1500–3000 km、且连线方向不沿任何轨道面时**；低纬源站形成"环 + 斜带"，高纬源站只有斜带。作者强调该结论**与源站经度无关**，同纬度源站会重复出现相同结构。
- **构件分解**（§5.2）：**ISL 很稳**——intra-orbit ISL 长度几乎恒为 **约 1970 km**；inter-orbit ISL 有**两类**，中位数分别为 **约 760 km 与 1384 km**，每个卫星各有一条（相位结构的产物）；100 分钟内所有 intra-orbit ISL 与 50% 的 inter-orbit ISL 长度变化极小（**0.2% / 6%**），另 50% 的 inter-orbit ISL 可变 **达 21%**（高纬轨道面更近）。**GSL 才是抖动之源**——以东京为例，GSL **寿命最短仅 6 秒、最长 4.5 分钟**；长度在 **550–1254 km** 之间近似均匀分布。
- **加卫星不等于更好**（§6，L292–L311）：把 Starlink 第一壳与整个星座（5 壳）比。**Starlink V1（旧 FCC 方案）优于 V2（新方案）**，因为 V1 壳层高度更高、**倾角多样性更大（4 种 vs 3 种）**。单纯增加同构壳层"**improves the RTT variability a little, but after that, there is no tangible difference**"；而**让各壳层倾角不同（53°/27°/72°/13°/40°/62°/82°/53°）可使 RTT 抖动的中位数降低 3 倍**（L311）。

**5. 实验条件**
- **星座**：Starlink 第一壳为主（550 km / 53° / 72 轨道 / 1584 星），并复现 Kuiper、Telesat 的第一壳；§6 用整个 Starlink 星座的 V1/V2 两版 FCC 方案（Table 3，壳层高度 550/1110/1130/1275/1325 km）。
- **地面站**：全球**人口最多的 100 座城市**，**全部 4950 个源目的对**（L~75）。作者特意**不剔除彼此接近的城市对**（因为关心卫星网作为主干网的场景，如偏远与灾区）。
- **仿真时长**：Starlink / Kuiper **100 分钟**，Telesat **110 分钟**——均为覆盖各自一整圈轨道周期（96 / 97 / 105 分钟），并假设 TLE 在仿真窗内恒定（TLE 实际每几天更新一次）。
- **空间结构实验**（§5.1）：3 个源站 × 2700 个均匀分布目的站。
- **+Grid 变体对照**（§2.2）：100 分钟、top 100 城市、4950 对、每秒采 RTT。
- **拥塞控制实验**：Mahimahi 模拟 60 秒、带宽在 204/48 Mbps 间切换、距离用 Pune–Lahore 实采 RTT。
- **训练/评估**：无训练（非学习）。**这是纯测量**。

**6. 自述局限（§7 Discussion，L313–L321，逐字三段）**
1. **拓扑变体**："our simulations use a specific variant of the +Grid topology... there are several other inter-satellite network topologies with desirable properties... **We leave it for future work to explore the impact of such variants on route variability.**"
2. **路由算法变体**："our study **didn't look into the impact of path length variability on routing algorithms that use more complicated metrics**. We leave such studies to future work."
3. **地面中继**："**Our study does not take into account satellite networks that rely on ground relays**... A network with ground relays... **will likely exhibit a higher degree of variability** than the network we studied."
（另在 §3 承认：用 1 s 而非 100 ms 的路由重算间隔、不使用 Hypatia 的包级仿真器。）

**7. 它没做但看起来能做的地方（基于内容）**
1. ⭐ **它是"零负载下 RTT 本身就抖动 2.5 倍"的直接证据，但全篇没有引入任何负载维度**。所有 RTT 都是路径传播时延（Hypatia 路由层），拥塞控制那节用 Mahimahi **人为注入**带宽/时延变化，**真实排队时延从未出现**。**"移动致抖动"与"负载致排队"这两个来源从未被放在一起分解**——而这恰好是"负载变化下时延"研究必须先做的减法。
2. ⭐ **它自己的 +Grid 变体对照实验（L69）已经是一个"抖动 vs 时延"的权衡证据**：朴素最近邻 +Grid 有超过 40% 的场景路径更短（最大增益 43%），但变长时可长 5 倍以上、RTT 比高达 7；它选了抖动最小的变体。**它只报了长度/时延，完全没报这个选择对负载分布的影响**——而"路径长度"与"流量集中"正是它 §4.3 批评的对象，两者在同一篇里互不照面。
3. **§4.3 的"all connections flock to the same path"是全文最有价值的现象，却只有一个 2000↔2000 的构造场景**（纽约-伦敦）。**没有做"热点程度 vs 城市对数量/地理密度"的扫描**，也没给链路利用率的绝对数值（Table 2 用的是 Pune–Lahore 单条路径，不是那个 2000 连接场景）。
4. **"70% 的路径收益 < 25%" 只支持"降低 churn 频率"，没有给出**该用什么阈值/迟滞（hysteresis）**。作者自己说"routing algorithms should be designed to balance churn and performance"（L~127），但没做这个平衡的任何设计或实验。
5. **Table 2 的带宽只在 204/48 Mbps 两个值间切换**（作者理由：贴合 Starlink 规格），**是二值跳变而非连续变化**——与真实卫星链路的连续衰落不符。
6. **GSL 抖动被归为主因，但缓解手段只有"选第一跳"**（§5.2 末，L~238：选错第一跳可使 RTT 翻倍）。**作者没测"用更长的 GSL 换更稳的 GSL"能否降低 churn**——这正是一个现成的设计空间。
7. §6 的结论（**倾角多样性比卫星数量更重要**）非常强，但**只有 Starlink V1/V2 两个真实方案 + 一组手选倾角**，没有系统的倾角/壳层数二维扫描。

**8. 和同批其他篇的关系**
本批（R9）其余篇目尚未读完，暂无法逐篇比对。就谱系看，**它在本批里是异类也是基准**：
- 它**不做算法**，做的是**测量与反例**，而本批已读的其他篇（UF8IQTA2、UKBSA7WN、UKEKU5ZG、VFS59FHI、W5Z39E25）全部在提算法。
- §2.3 与 §8 明确把自己与**最短路径族**（Bhattacherjee & Singla 的拓扑设计、Hypatia、ECMP+OARST、MPLS TE、延迟界内随机分流等）划在一起，并指出"**All proposed algorithms covered in this brief survey rely on path length either primarily or partially in selecting routes**"（L~73）——**这是对本批所有"以时延/跳数为目标"的路由工作的一句共同批评**，包括 UF8IQTA2（hopS/hopD 修复）、VFS59FHI（Dijkstra 权值）、W5Z39E25（最短路+备用路径）。
- 它点名引用 **Hypatia [46]**（本批多篇 LEO 论文常用的仿真器来源）与 **Bhattacherjee 的 "Network topology design at 27,000 km/hour" [20]**。
- **不引用本批其他任何一篇。**

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**有重要且不可替代的贡献——它定义了"负载之外的那部分时延抖动有多大"。** 具体：
1. ⭐ **给出了零排队条件下时延抖动的量级**：同一对地面站的**最小可达 RTT 可涨到 2.5 倍**（仅由卫星运动导致）。**任何声称"负载升高导致时延上升"的研究，必须先把这 2.5 倍的运动性抖动从总时延里扣掉**，否则信号会被淹没。
2. ⭐ **给出了抖动的空间结构**（L178）：**只在两站相距 1500–3000 km、且连线方向不沿任何轨道面时**才高。这意味着**选择实验的源目的对会系统性地决定结论**——这是一个可操作的方法学约束（本批其他论文普遍随机或随意选源目的对，均未讨论这一点）。
3. ⭐ **给出了"最短路径贪心 → 流量集中 → 利用率损失"的实测链条**（L147）：全部 2000 条连接为约 1–2% 的时延差挤到同一条路径。**这是"负载不均"的一个纯路由侧成因**，与 VFS59FHI 的"信关站地理集中"成因完全不同——两篇合起来说明 LEO 的负载不均**既有地理成因也有算法成因**。
4. **给出拥塞控制层面的时延-利用率对立**（Table 2）：**没有任何单一拥塞控制算法能同时优化时延与利用率**，且这种对立在"带宽变 + RTT 变"同时发生时最严重。这把"负载 → 时延"的问题从路由层延伸到了传输层。
5. **给出了 GSL 抖动的一手分布**（寿命 6 s–4.5 min、长度 550–1254 km）与 **ISL 的稳定性**（长度几乎恒定）——**说明 LEO 的链路级不确定性集中在星地侧而非星间侧**，这对"瓶颈在哪"的判断很关键。
**缺口**：**全篇没有到达率、没有队列、没有负载**。它给的是"零负载基线抖动"，不是"负载-时延关系"。这恰恰使它成为本主题的**必要的对照基准**而非竞争工作。

**10. 一句话评价**
**本批唯一一篇"不造算法、只测真相"的测量论文**，且是质量最高的一篇：用 Hypatia + Mahimahi + Pantheon 把 LEO 路由的 churn、RTT 抖动的空间结构与物理成因、以及"加卫星不如调倾角"三件事用一手数据钉死；它的真正分量在于提出了一个**所有以路径长度为目标的路由工作都必须回答的反问**——**当时延只值 25%、甚至 2.5%，值得为此把全部流量挤到一条路上吗？**


