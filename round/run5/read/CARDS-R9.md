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


