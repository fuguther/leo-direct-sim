# 读卡批次 R2

> 读法：逐篇逐字通读 VM MinerU MD 全文（每篇从第 1 行读到最后一行，含参考文献）。行号对应 VM MD 行号。
> 篇目（11）：53HEEK33 57EB6US5 5AZHJE7N 5HJ8ATR7 5N5LQPPP 5PYWVRC5 67CSKFK4 6C843JTS 6GWNYSTT 7AXASN73 7TASFUDR

## 53HEEK33 — Fast-Convergence Reinforcement Learning for Routing in LEO Satellite Networks

**1. 一句话**
把经典表格型 Q-routing 原样搬到 Iridium 类 LEO 星座上，唯一实质改动是把"有包才反馈"换成"周期性 hello 广播整张 Q 表"（空包收敛法），用控制面开销换收敛速度。

**2. 问题设定**
链路状态在星间是**串行扩散**的：只有直接相邻的两颗星先知道链路变化，再一圈圈传出去（L201；Fig 3 用 5 轨道×5 星示意，白点要到第 4 轮才收到消息，L203）。而传统 Q-routing 只在"本节点把包发给邻居"时才拿到邻居的 Q 表与链路状态反馈（L203 逐字："the agent receives the Q-table and link state information feedback from the neighbor nodes when and only when it sends a packet to its neighbor nodes"），于是出现"上一阶段还没收敛完，链路状态又变了"（L201 逐字："it is possible that the convergence of the previous stage is not yet complete and the link state has changed again"）。对照面：Dijkstra/OSPF 要全局信息，收完就已过时（L38、L272）。

**3. 方法骨架**
- 每颗星一个 agent，**表格型 Q-learning（非 DRL）**，作者明说因为动作空间只有 4 所以不用深度网络（L109 逐字："the action space is up to four. Therefore, we chose reinforcement learning rather than deep reinforcement learning to achieve this"）。
- Q 表是二维：行 = (本节点, 目的节点)，列 = 邻居端口（Table 1，L90）。
- 状态 S = { N_c, N_d, q_1^t, ..., q_P^t }，即当前节点、目的节点、P 个节点的当前队列长度（L113）。
- 动作 = 从邻居里选一个端口，最多 4 个（L115）。
- 奖励 Eq(3)（L128）：下一跳是目的星 → 20N；否则 q_max − (q_r + q_t) − w1·g_j − w2·D_j。其中 g_j 是**上一阶段的接收队列长度**，作者称其为"负载增长/拥塞水平"（L123 逐字："we record the receiving queue length in the previous stage as the load growth of the satellite"）。
- 更新就是标准 Q-routing 式 Eq(2)（L84）：Q_i(s,a) ← (1−α)Q_i(s,a) + α[r + γ·max_{a'} Q_j(s',a')]，注意目标是**邻居 j 的 Q 表**，这也是它必须交换 Q 表的原因。
- 三段式训练：邻居发现（hello 包带 Q 表/链路信息/可用资源，久收不到就判邻居下线，L140）→ **离线训练**（地面网络、随机生成包、ε-greedy 且 ε 递减、lr=0.8，L131/L148/L242）→ **在线训练**（不用 ε-greedy，只微调，lr=0.2，L187/L242）。
- 核心机制"empty packet convergence method"（L203）：邻居按**周期 t** 主动广播状态，而不是等收到包；传统做法一次只更新二维表的一项，空包法**一次更新一个节点整个动作空间**；且 **t 与节点流量密度成反比**（L203 逐字："we designed t to be inversely proportional to the node traffic density; the higher the traffic density, the smaller the t"）。
- 复杂度对比（L232）：本算法时间 O(1)（查表）vs Dijkstra O(n²)；空间 O(4N) vs O(E+4N)；通信开销只到邻居、不泛洪（L234）。

**4. 它声称的效果**
- Fig 4（L247–L261）：只含距离的 reward1（Eq 7）不如含队列的 reward2（Eq 8），故选 reward2，**无任何数值**。
- Fig 5 / Fig 6（L264–L270）：初始包数 3000 与 5000 两档下，FRL–SR 平均时延均低于 Dijkstra。
- Fig 7（L274–L279）：累计成功送达包数更多。
- Fig 8（L285，Eq 9 用总体标准差）：节点负载更均衡。
- **全文正文没有出现任何一个结果数字**，全部结论都由曲线图承载；基线只有一个 Dijkstra。
- L272 自述一个反常现象并自己解释：平均时延随时间**缓慢上升**，因为星间链路易故障丢包，而算法**没有重传**，丢包的时延被一直累计进平均值。

**5. 实验条件**
- 49 星 = 7 轨道 × 7 星（L242；Table 3 L245）。
- 传播时延按**正弦曲线**变化以模拟链路失效与恢复（L242）；"Delay type = sinusoidal"（Table 3）。
- 3 次重复取平均（L238、Table 3）。
- 关键参数（Table 3，L245）：离线训练网络负载 3000、在线训练初始负载 3000、最大队列长度 150、单次最多发 10 包、30 episodes × 200 steps、γ=0.9、lr 离线 0.8 / 在线 0.2。
- **训练与评估不是同一套**：离线在"地面网络环境"里预训练（L131、L144 逐字 "we perform the initial training of the agents in a ground-based network environment"），在线才在卫星网络上微调，报告的是在线阶段结果。
- 负载口径只有"网络里初始包数"（3000 / 5000），**不是到达率**，也没有扫多个负载点。

**6. 它自己承认的局限**
**没有独立的局限章节**（第 1–5 节通读，无 Limitations 段）。能找到的自述只有两处：
- L272 逐字："The algorithm in this paper does not have a data retransmission function, which means the delay of lost packets will keep increasing, resulting in a rising average delay."（承认无重传、丢包时延累积）
- L296 未来工作只有一句"继续做多智能体强化学习"，未指出具体缺口。
此外全文**没有状态字段消融、没有 t 的敏感性分析、没有数值表**。

**7. 它没做但看起来能做的地方（基于内容）**
1. "t 与流量密度成反比"是纯断言：没给函数形式、没给上下界、没做敏感性扫描（L203）。这是本文卖点的核心参数，却零实验。
2. 奖励里的 g_j（负载增长）从未单独消融——Fig 4 只比较了"有队列 vs 无队列"，没有回答"增长项相对瞬时队列项贡献多少"（L123 vs L247–L259）。
3. 复杂度分析只跟 Dijkstra 比，没有把"空包带来的额外通信量"计入（L234 承认会增加邻居间通信，但没量化）。
4. **没读懂：第 3.1 节状态定义里 P 的范围**——写成"q_p^t represents the current queue length of the p-th node for p = 1 to p = P"（L113），但每星只有 4 个邻居，P 是全星座节点数还是邻居集，全文未界定。
5. 无重传被承认（L272），却没有把"丢包"和"时延"两个口径分开记账，导致平均时延曲线被丢包污染，读者无法分辨是排队恶化还是丢包统计效应。

**8. 和同批其他篇的关系**
第 2 节把谱系摆得很清楚：虚拟拓扑派（Mauger 虚拟节点[4]、DV–DVTR[5]、TNM[7]）、分布式负载均衡派（Ekici[8]、队列长度拥塞信息[9]）、SDN 集中派（[10][11][12]）、RL 派（Q-routing[16]、DRL 集中式[17]、分布式 RL[18]）。参考文献 [3] 是 DRL-ER——是"逐包 DRL 路由"这条线的代表，本批其他篇很可能把它当基线（截至写完本卡，我尚未读完本批其余 10 篇，互引关系待后续卡补证）。

**9. 对"负载变化下到达率/时延"的贡献**
两点沾边、但都没给可用事实：
- (a) **控制面刷新率随负载自适应**：t 与流量密度成反比（L203），是"负载变 → 感知频率变"的明确设计，但只有一句话，没有实验。
- (b) **两个负载水平的并列实验**：3000 与 5000 初始包两档（Fig 5/6），但结论只有"consistent performance"（L264），既没有到达率轴，也没有负载→时延的量化关系。
- 奖励含队列长度说明它把排队时延纳入决策（L121），但结果里从不把排队时延与传播时延分开记账。
- **没有直接贡献**：全文没有到达率（pps/包每秒）这个自变量，负载是"初始包数"这种一次性快照量，无法回答"到达率上升时时延怎么变"。

**10. 一句话评价**
把已有 Q-routing 用到 LEO 上、只改了信息扩散方式（周期性广播替代按需反馈），"快收敛"的卖点全靠控制面开销换，且无任何数值对照——方法谱系里属于**工程改型的复现派**，不是新机制。

<!-- END-CARDS-R2 -->
