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
