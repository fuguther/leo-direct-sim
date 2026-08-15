## 结论先说

这次按“找反例、尽量推翻你的 novelty”来查，结论并不是“你的想法没了”，而是**必须把主张收得比现在窄很多**。

| 问题                           | 证伪结论                                   | 核心原因                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ---------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Q1 路由状态自身的年龄是否真空白？**       | **已有人做——宽主张被证伪**                       | DRL-THSA 2019 的 LEO+DDQN 路由已经在 Link State Table 中保存 `Timestamp`，并将 LST 纳入 RL 状态定义，还用 timestamp 判断收到的链路状态是否 up-to-date。([MDPI](https://www.mdpi.com/2079-9292/8/9/920?utm_source=chatgpt.com "A Two-Hops State-Aware Routing Strategy Based on Deep ..."))                                                                                                                                                                                                                                        |
| **Q2 年龄感知注意力是否没人做？**         | **部分重合，而且“age-aware attention”本身已经被占** | Zhu et al. 2023 明确提出 **AoI-based temporal attention GNN**，目的就是避免 message staleness。不是 LEO 路由，但足以否定“年龄进入 attention 是新的”。([arXiv](https://arxiv.org/abs/2208.08606 "[2208.08606] AoI-based Temporal Attention Graph Neural Network for Popularity Prediction and Content Caching"))                                                                                                                                                                                                                |
| **Q3 更广 k-hop + 自适应聚合是否饱和？** | **作为单独贡献基本饱和**                         | 2019 已有 two-hop DDQN；GraphPR 已用 GAT+邻居 hidden state 获得隐式 multi-hop；Weil 2024 专门讨论 neighborhood size 与 partial/outdated observations，并用 recurrent message passing 扩散全图信息；2025–26 又已有 temporal GNN、GAT+LSTM、Transformer attention。([ResearchGate](https://www.researchgate.net/publication/335372940_A_Two-Hops_State-Aware_Routing_Strategy_Based_on_Deep_Reinforcement_Learning_for_LEO_Satellite_Networks?utm_source=chatgpt.com "(PDF) A Two-Hops State-Aware Routing Strategy Based on ...")) |

**但我目前没有找到直接反例覆盖下面这个非常窄的交集：**

> 在 **LEO、逐包逐跳、分布式 DRL/DDQN、无未来星历/无全局状态** 条件下，对每个邻居/边遥测字段维护 **observation age**，并让该年龄作为可学习的可靠性变量，直接调制 destination-/edge-conditioned message passing 或 attention。

这才是目前值得保的主线。不能再写“首次考虑 AoI”“首次 age-aware attention”“首次多跳图聚合”。

---

# Q1：LEO DRL 路由真的没人显式考虑“路由状态自身的年龄”吗？

## 判决：**已有人做。原主张需要撤回。**

最关键反例不是 RAoI，而是你很容易忽略的老论文：

**Cheng Wang, Huiwen Wang, Weidong Wang, “A Two-Hops State-Aware Routing Strategy Based on Deep Reinforcement Learning for LEO Satellite Networks,” Electronics, 2019, 8(9):920, DOI 10.3390/electronics8090920.** ([MDPI](https://www.mdpi.com/2079-9292/8/9/920?utm_source=chatgpt.com "A Two-Hops State-Aware Routing Strategy Based on Deep ..."))

它有三个直接证据：

1. 它定义的 Link State Table 明确包含  
   `Node | Direction | Connectedness | Link State | Timestamp`。论文符号表还明确写 `t = timestamp of link state`。([MDPI](https://www.mdpi.com/2079-9292/8/9/920?utm_source=chatgpt.com "A Two-Hops State-Aware Routing Strategy Based on Deep ..."))

2. RL 状态集合被定义成

[  
S=[N_s,N_d,LST],  
]

运行流程也明确写把 `[N_c,N_d,LST]` 输入 DDQN。也就是说，形式定义中的 RL state 确实包含这个带 timestamp 的 LST。([ResearchGate](https://www.researchgate.net/publication/335372940_A_Two-Hops_State-Aware_Routing_Strategy_Based_on_Deep_Reinforcement_Learning_for_LEO_Satellite_Networks?utm_source=chatgpt.com "(PDF) A Two-Hops State-Aware Routing Strategy Based on ..."))

3. 更直接的是控制面更新算法：收到 HELLO/邻居链路状态变化消息后，它检查 timestamp 是否 “up to date”；不是最新的就丢弃。([ResearchGate](https://www.researchgate.net/publication/335372940_A_Two-Hops_State-Aware_Routing_Strategy_Based_on_Deep_Reinforcement_Learning_for_LEO_Satellite_Networks?utm_source=chatgpt.com "(PDF) A Two-Hops State-Aware Routing Strategy Based on ..."))

所以以下表述已经不能用了：

> “Prior LEO DRL routing methods do not explicitly represent the freshness/staleness of routing-state information.”

**这是假的。**

但这里有一个对你很重要的细分：DRL-THSA 更接近

[  
\text{timestamp} \rightarrow \text{freshness/order check} \rightarrow \text{hard accept/drop}  
]

而不是你想做的

[  
\Delta_{ij}^{f}(t)=t-\tau_{ij}^{f}  
\rightarrow  
\text{learned reliability}  
\rightarrow  
\alpha_{ij}^{f}(t)  
]

即“状态到底老了多少”连续地影响策略。

而且论文虽然形式上把带 Timestamp 的 LST 放进 (S)，**并没有足够清楚地证明 DDQN 把 timestamp 数值作为连续数值特征进行学习，而不是主要将其用于状态更新过程中的 freshness gate**。因此更安全的结论是：

> **LEO DRL 中 routing-state timestamp/freshness 并非空白；但把 field-wise observation age 作为连续可学习可信度，并直接作用于图聚合，目前仍未找到直接反例。**

这是 Q1 真正剩下的空间。

---

# Q2：“年龄感知注意力”撞车到什么程度？

## 判决：**机制层面已有人做；LEO-routing-specific 交集仍未发现。**

### 1. Zhu et al.：这是最危险的机制反例

**Jianhang Zhu et al., “AoI-Based Temporal Attention Graph Neural Network for Popularity Prediction and Content Caching,” IEEE Transactions on Cognitive Communications and Networking, 2023, 9(2):345–358, DOI 10.1109/TCCN.2022.3227920.** ([IEEE Xplore](https://ieeexplore.ieee.org/servlet/Login?logout=%2Fabstract%2Fdocument%2F9978680%2F&utm_source=chatgpt.com "AoI-Based Temporal Attention Graph Neural Network for ..."))

论文自己明确说提出 AoI-based attention mechanism，用于提取有用历史信息同时避免 **message staleness**；作者代码也把它概括成 “AoI-based message filter with the attention aggregator”。([arXiv](https://arxiv.org/abs/2208.08606 "[2208.08606] AoI-based Temporal Attention Graph Neural Network for Popularity Prediction and Content Caching"))

所以：

> “我们首次提出 age-aware attention，让旧信息权重下降”

**不能作为 novelty。**

你的差异只能是：

- 它：动态图历史 interaction/message freshness；

- 你：**LEO routing telemetry observation freshness**；

- 它：预测/缓存；

- 你：逐包逐跳 DRL routing；

- 你进一步把 age 与 destination、edge/action candidate 共同条件化。

换句话说，**应用域+状态语义+决策结构可以新，attention 中塞 age 这个数学动作本身不新。**

---

### 2. NGAT：名字容易误导，但并没有直接撞你的 age-attention

**Yanning Zhang et al., “Graph Attention Reinforcement Learning for Multicast Routing and Age-Optimal Scheduling,” arXiv:2404.18084，2024，v6 2025；正式期刊/会议状态本次未验证。** ([arXiv](https://arxiv.org/abs/2404.18084 "[2404.18084] Graph Attention Reinforcement Learning for Multicast Routing and Age-Optimal Scheduling"))

两个非常重要的澄清：

**NGAT 的 N 是 Normalized，不是 age/node-age。** 它提出 Normalized Graph Attention，主要目标是 contraction mapping/generalization。([arXiv](https://arxiv.org/html/2404.18084v6 "Graph Attention Reinforcement Learning for Multicast Routing and Age-Optimal Scheduling"))

它的 AoI 则是经典意义的数据新鲜度：

[  
\hat A_p(t)=t-t_p,  
]

其中 (t_p) 是**packet generation time**；destination AoI 在接收到新 packet 时刷新。([arXiv](https://arxiv.org/html/2404.18084v6 "Graph Attention Reinforcement Learning for Multicast Routing and Age-Optimal Scheduling"))

所以这是你要求严格区分的：

[  
\boxed{\text{payload/data AoI}}  
]

而不是

[  
\boxed{\text{routing observation age}}  
]

不过 NGAT 会占掉另外两个宽泛主张：

- GAT + AoI 已经存在；

- edge feature 直接进入 attention score 已经存在：

# [

\phi(h_i,h_j)

a^\top \operatorname{LeakyReLU}  
(W_1h_i+W_2h_j+W_e e_{ij}).  
]

([arXiv](https://arxiv.org/html/2404.18084v6 "Graph Attention Reinforcement Learning for Multicast Routing and Age-Optimal Scheduling"))

因此 **“edge-aware attention”也不能单独作为创新点。**

---

### 3. RAoI / ADRLRM：不撞你的 AoI 类型

**Ronghao Gao et al., “Toward the Age in Forwarding: A Deep Reinforcement Learning Enabled Routing Mechanism for Large-Scale Satellite Networks via Spatial–Temporal Graph Neural Networks,” IEEE/ACM Transactions on Networking, Vol. 34, pp. 292–307, 2026；DOI 10.1109/TON.2025.3597928.** ([IEEE Xplore](https://ieeexplore.ieee.org/document/11126166/?utm_source=chatgpt.com "Toward the Age in Forwarding: A Deep Reinforcement ..."))

论文定义的 Routing-aware AoI（RAoI）明确用于衡量 **data delivery freshness**，并把 RAoI 放进 reward，当成路由优化目标；同时用 PTSA-assisted STGNN 提取时空拓扑特征。([Harbin Institute of Technology](https://scholar.hit.edu.cn/en/publications/toward-the-age-in-forwarding-a-deep-reinforcement-learning-enable/?utm_source=chatgpt.com "Toward the Age in Forwarding: A Deep Reinforcement Learning ..."))

所以它解决的是：

[  
\text{“这个数据到目的端时有多旧？”}  
]

你解决的是：

[  
\text{“我现在用来选下一跳的这个 }q_j/B_{ij}/l_{ij}  
\text{ 是多久以前测到的？”}  
]

两者不是一回事。

这一关键区分**完全站得住**。

同类的 **RRS-DRL** 也明确说把 *AoI of packets* 作为优化目标，因此同样属于 payload AoI。([IET Research](https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/ell2.12820?utm_source=chatgpt.com "A robust routing strategy based on deep reinforcement ...") )

---

### 4. GraphPR：很接近你的图路由结构，但没有 explicit age

**Yongyi Ran et al., “Fully-Distributed Dynamic Packet Routing for LEO Satellite Networks: A GNN-Enhanced Multi-Agent Reinforcement Learning Approach,” IEEE Transactions on Vehicular Technology, 74(3), 2025, pp. 5229–5234；early access 2024.** ([IEEE Xplore](https://ieeexplore.ieee.org/document/10755127/?utm_source=chatgpt.com "Fully-Distributed Dynamic Packet Routing for LEO Satellite ..."))

它已经做了：

- 每颗卫星一个 Agent；

- POMDP；

- 只与一跳邻居通信；

- GAT 自适应聚合；

- 邻居共享 hidden states；

- 反复共享后 hidden state **隐式包含 multi-hop 信息**。([IEEE Xplore](https://ieeexplore.ieee.org/document/10755127/?utm_source=chatgpt.com "Fully-Distributed Dynamic Packet Routing for LEO Satellite ..."))

真正与你很相关的是：

[  
h_j(t-1)\rightarrow h_i(t),  
]

论文明确用邻居上一轮 hidden state 聚合；satellite-related state 又周期更新，实验设置甚至是 **1 min update period**。([Scribd](https://www.scribd.com/document/1065983162/Fully-Distributed-Dynamic-Packet-Routing-for-LEO-Satellite-Networks-a-GNN-Enhanced-Multi-Agent-Reinforcement-Learning-Approach "Fully-Distributed Dynamic Packet Routing For LEO Satellite Networks A GNN-Enhanced Multi-Agent Reinforcement Learning Approach | PDF | Routing | Satellite"))

但它没有给这个旧 hidden state 一个

[  
\Delta_j=t-\tau_j  
]

让 GAT 知道“这条信息到底旧了多久”。

这正好形成你的最好问题设置：

> GraphPR 已经证明局部隐藏状态交换可扩展视野，但其接收者把邻居 representation 当成等时效输入；在异步、丢包、不同更新周期下，这个假设会不会导致错误注意力？

另外，你提出“目的地进入 message passing”与 GraphPR 也确实有区别。GraphPR 是：

[  
G_i(s_i^n)  
\rightarrow h_i  
]

然后才把 packet-related state（含 destination）与 (h_i) 拼接给 FCNN：

# [

Q_i

F_i\big(G_i(s_i^n)\Vert s_i^p,a_i\big).  
]

也就是说，**destination 并没有参与 GAT 邻居聚合本身**。([Scribd](https://www.scribd.com/document/1065983162/Fully-Distributed-Dynamic-Packet-Routing-for-LEO-Satellite-Networks-a-GNN-Enhanced-Multi-Agent-Reinforcement-Learning-Approach?utm_source=chatgpt.com "Fully-Distributed Dynamic Packet Routing for LEO Satellite ..."))

这一点目前仍能保。

---

### 5. Chou et al. 2026：会占掉“temporal modeling”故事

**Po-Heng Chou et al., “Spatial-Temporal Learning-Based Distributed Routing for Dynamic LEO Satellite Networks,” arXiv:2605.02413v1, 2026；标注 submitted to IEEE GLOBECOM 2026，录用状态未验证。** ([arXiv](https://arxiv.org/abs/2605.02413 "[2605.02413] Spatial-Temporal Learning-Based Distributed Routing for Dynamic LEO Satellite Networks"))

它已经是：

[  
\text{GAT}\rightarrow\text{LSTM}\rightarrow\text{DQN}.  
]

每颗卫星独立决策，POMDP，state 为

[  
s_i(t)=  
[Q_i(t),{D_{ij}(t)}_{j\in N_i(t)},x_i(t)],  
]

action 是 next-hop neighbor，reward：

[  
r_i(t)=-  
\left[  
\alpha D_{i,a_i(t)}(t)+  
\beta Q_i(t)  
\right].  
]

GAT attention 根据节点 topology feature 计算，然后 LSTM 建模历史状态。([arXiv](https://arxiv.org/html/2605.02413v1 "Spatial-Temporal Learning-Based Distributed Routing for Dynamic LEO Satellite Networks"))

它没有显式 age/timestamp，但意味着：

> “LEO 动态路由需要同时考虑空间邻域和时间历史”

**已经不是新故事。**

所以不能把你的论文包装成“现有 GAT 只看空间，我加入时间”。

你的区别必须是：

> **不是学习 temporal correlation，而是显式知道 observation freshness/reliability。**

这是比 LSTM 更强、更具体的语义。

---

### 6. Weil et al.：对你的“POMDP + stale observation + k-hop”问题框架构成强碰撞

**Jannis Weil et al., “Towards Generalizability of Multi-Agent Reinforcement Learning in Graphs with Recurrent Message Passing,” AAMAS 2024; arXiv:2402.05027.** ([arXiv](https://arxiv.org/abs/2402.05027 "[2402.05027] Towards Generalizability of Multi-Agent Reinforcement Learning in Graphs with Recurrent Message Passing"))

它摘要第一段就讲：

> decentralized agents 基于 partial or outdated observations 行动；observed neighborhood size 会影响反应速度、动作质量、泛化和通信开销。

随后提出 recurrent message passing，随环境 step 持续传播信息，而不是每次硬做大 (k)-hop 聚合。([arXiv](https://arxiv.org/html/2402.05027v3 "Towards Generalizability of Multi-Agent Reinforcement Learning in Graphs with Recurrent Message Passing"))

而且实验本身就是通信网络 routing：packet agent 只能观察当前位置、destination、packet size，以及 outgoing edge delay/load/neighbor ID；通过 recurrent graph representation 补足局部可观测性。([arXiv](https://arxiv.org/html/2402.05027v3 "Towards Generalizability of Multi-Agent Reinforcement Learning in Graphs with Recurrent Message Passing"))

它不是卫星，也没有显式 (\Delta)。

但是它足以否定：

> “我们首次研究图路由中局部信息过时的问题。”

以及：

> “扩大 k-hop 并通过 message passing 自适应解决局部观测不足，是我们的主要创新。”

这两个都不安全。

---

### 7. Almasan et al.：你的 action-conditioned 部分已经有非常直接的先例

**Paul Almasan et al., “Deep Reinforcement Learning Meets Graph Neural Networks: Exploring a Routing Optimization Use Case,” Computer Communications 196 (2022):184–194, DOI 10.1016/j.comcom.2022.09.029.** ([科学直通车](https://www.sciencedirect.com/science/article/abs/pii/S0140366422003784?utm_source=chatgpt.com "Deep reinforcement learning meets graph neural networks"))

它直接构造 link-level MPNN，并将：

- available capacity；

- link betweenness；

- **routing action itself**

一起作为 link hidden-state 输入。

候选 action 是 source-destination 的 (k=4) 条候选路径；如果某条 edge 属于当前 candidate action，就把当前 demand bandwidth 编入该 edge，否则置 0，然后 MPNN 计算这个 (Q(s,a))。([ar5iv](https://ar5iv.labs.arxiv.org/html/1910.07421?utm_source=chatgpt.com "Deep Reinforcement Learning meets Graph Neural Networks"))

所以：

> **“action-conditioned graph representation/message passing”已经有人做过。**

你最后那个 “action-conditioned directional readout” 如果仅仅是

[  
Q(s,a)  
]

或把 candidate direction 编进去，基本不可能构成独立 novelty。

---

# 论文 × 机制对照表

“观测 AoI”这里专指**路由状态本身的年龄**，不是 packet AoI。

| 工作                                                                                                                                                                                                                                                                                                            | State / Observation                                                                                                                                                                                   | Action                               | Reward / objective                                       | Edge feature / 图聚合                                                                                                                                                                   | AoI 类型及处理                                                                                                                                                                             | 场景                    | 决策粒度                |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- | ------------------- |
| **DRL-THSA — Wang et al., Electronics 2019** ([ResearchGate](https://www.researchgate.net/publication/335372940_A_Two-Hops_State-Aware_Routing_Strategy_Based_on_Deep_Reinforcement_Learning_for_LEO_Satellite_Networks?utm_source=chatgpt.com "(PDF) A Two-Hops State-Aware Routing Strategy Based on ...")) | (N_s,N_d,LST)；2-hop link state；LST 有 Connectedness/Link State/**Timestamp**                                                                                                                           | next hop                             | destination/progress、失败/拥塞等                              | 无 GNN；2-hop table                                                                                                                                                                    | **路由状态 freshness**；timestamp + hard up-to-date filter；连续 age-learning 未证明                                                                                                             | LEO                   | 逐跳 DDQN             |
| **Continual DRL — Lozano-Cuadra et al., IEEE TCOM 2025** ([Aalborg Universitets forskningsportal](https://vbn.aau.dk/en/publications/continual-deep-reinforcement-learning-for-decentralized-satellite/?utm_source=chatgpt.com "Continual Deep Reinforcement Learning for Decentralized ..."))                | 28D：16 个一跳邻居 queue congestion、邻居坐标、本星坐标、destination 坐标、link connectivity                                                                                                                              | 4 邻居 next hop                        | queue time + destination progress + terminal terms       | 无 GNN；邻居反馈                                                                                                                                                                           | **无 explicit age**；16D congestion feedback 可周期更新 ([arXiv](https://arxiv.org/html/2405.12308v1 "Continual Deep Reinforcement Learning for Decentralized Satellite Routing"))           | LEO                   | 每星独立、逐包逐跳 DDQN      |
| **GraphPR — Ran et al., IEEE TVT 2025** ([IEEE Xplore](https://ieeexplore.ieee.org/document/10755127/?utm_source=chatgpt.com "Fully-Distributed Dynamic Packet Routing for LEO Satellite ..."))                                                                                                               | 本星位置/平均队列 + 邻居 hidden states；packet destination + instant queues                                                                                                                                      | 4 方向 next hop                        | RSPH + queue delay + propagation delay + terminal reward | GAT；邻居 (h_j(t-1))，反复传播隐式 multi-hop                                                                                                                                                   | **无 explicit age**；satellite state 周期更新                                                                                                                                               | LEO                   | 分布式逐包逐跳             |
| **Chou et al., arXiv 2026** ([arXiv](https://arxiv.org/abs/2605.02413 "[2605.02413] Spatial-Temporal Learning-Based Distributed Routing for Dynamic LEO Satellite Networks"))                                                                                                                                 | local queue、neighbor link delay、topology feature                                                                                                                                                      | next hop                             | (-\alpha D-\beta Q)                                      | GAT + LSTM                                                                                                                                                                           | 无 observation-age；**隐式 temporal memory**                                                                                                                                              | LEO                   | 每星独立逐跳 DQN          |
| **ADRLRM / RAoI — Gao et al., IEEE/ACM ToN 2026** ([Harbin Institute of Technology](https://scholar.hit.edu.cn/en/publications/toward-the-age-in-forwarding-a-deep-reinforcement-learning-enable/?utm_source=chatgpt.com "Toward the Age in Forwarding: A Deep Reinforcement Learning ..."))                  | PTSA + STGNN 的时空拓扑状态；完整字段本次未全部验证                                                                                                                                                                      | routing；细粒度字段**未验证**                 | RAoI 被放入 customized reward                               | STGNN                                                                                                                                                                                | **数据/转发 AoI**，不是 telemetry age                                                                                                                                                        | 大规模卫星网络               | routing             |
| **RRS-DRL — Chu et al., Electronics Letters 2023** ([EBSCO OpenURL](https://openurl.ebsco.com/fulltext/gcd%3A164232205?crl=f&id=ebsco%3Agcd%3A164232205&jrnl=00135194&sid=ebsco%3Aplink%3Acrawler-gcd&utm_source=chatgpt.com "A robust routing strategy based on deep reinforcement ..."))                    | 动态拓扑/链路性能等；完整状态字段本次未全部验证                                                                                                                                                                              | routing                              | packet AoI 等多目标                                          | 非重点                                                                                                                                                                                  | **packet AoI**                                                                                                                                                                        | mega constellation    | routing             |
| **NGAT — Zhang et al., arXiv:2404.18084, 2024/25** ([arXiv](https://arxiv.org/abs/2404.18084 "[2404.18084] Graph Attention Reinforcement Learning for Multicast Routing and Age-Optimal Scheduling"))                                                                                                         | graph + node type、importance、node AoI、# transmitting packets ([arXiv](https://arxiv.org/html/2404.18084v6 "Graph Attention Reinforcement Learning for Multicast Routing and Age-Optimal Scheduling")) | multicast tree/scheduling            | AoI / hop / energy 等                                     | NGAT；**edge feature (e_{ij}) 进入 attention** ([arXiv](https://arxiv.org/html/2404.18084v6 "Graph Attention Reinforcement Learning for Multicast Routing and Age-Optimal Scheduling")) | **packet/destination AoI**；非 observation age ([arXiv](https://arxiv.org/html/2404.18084v6 "Graph Attention Reinforcement Learning for Multicast Routing and Age-Optimal Scheduling")) | 一般动态 multicast 网络     | tree/scheduling     |
| **AoI-TGN — Zhu et al., IEEE TCCN 2023** ([IEEE Xplore](https://ieeexplore.ieee.org/servlet/Login?logout=%2Fabstract%2Fdocument%2F9978680%2F&utm_source=chatgpt.com "AoI-Based Temporal Attention Graph Neural Network for ..."))                                                                             | 动态交互图及历史消息                                                                                                                                                                                            | caching/prediction，不是 routing action | prediction/cache objective                               | temporal attention                                                                                                                                                                   | **历史 message age/staleness** 显式进入 attention                                                                                                                                           | ICN/content caching   | 非路由                 |
| **Weil et al., AAMAS 2024** ([arXiv](https://arxiv.org/abs/2402.05027 "[2402.05027] Towards Generalizability of Multi-Agent Reinforcement Learning in Graphs with Recurrent Message Passing"))                                                                                                                | agent local state + graph node/edge local observation                                                                                                                                                 | wait / outgoing edge                 | 到达 +10；容量不足 -0.2                                         | recurrent message passing                                                                                                                                                            | 明确讨论 **partial/outdated observations**；无 explicit age scalar                                                                                                                          | 有线通信图                 | 每 packet agent 逐跳   |
| **Almasan et al., Computer Communications 2022** ([ar5iv](https://ar5iv.labs.arxiv.org/html/1910.07421?utm_source=chatgpt.com "Deep Reinforcement Learning meets Graph Neural Networks"))                                                                                                                     | edge capacity、betweenness、**candidate-action feature**                                                                                                                                                | (k=4) candidate paths                | 最大化成功承载带宽                                                | edge-level MPNN                                                                                                                                                                      | 无 AoI                                                                                                                                                                                 | optical/wired network | 集中式 path-level      |
| **Trans-MADRL — Liang et al., ICIC 2026；Springer卷标2027** ([Springer Link](https://link.springer.com/chapter/10.1007/978-981-92-3400-4_8?utm_source=chatgpt.com "Filtering Transient Noise for Precise LEO Routing via Trans ..."))                                                                            | 完整字段公开摘要不足，**未验证**                                                                                                                                                                                    | distributed packet routing           | exponential delay penalty                                | multi-head self-attention 作为 **transient-noise filter**                                                                                                                              | 不是 explicit observation age                                                                                                                                                           | LEO                   | distributed routing |
| **Target-Aware GNN-DQN — Cai et al., ICIC 2026** ([ACM Digital Library](https://dl.acm.org/doi/10.1007/978-981-92-3381-6_46?utm_source=chatgpt.com "Target-Aware GNN-DQN Adaptive Routing for LEO ..."))                                                                                                      | **未验证**                                                                                                                                                                                               | adaptive LEO routing                 | **未验证**                                                  | GNN-DQN；destination 是否真正进入 MP **未验证**                                                                                                                                                | 未发现可核实 explicit age                                                                                                                                                                   | LEO                   | **未验证**             |

---

# Q3：“更广 k-hop + 自适应聚合”还剩多少？

## 判决：**作为论文核心 novelty，已经不够。**

这条路线已经至少被从四个方向包围：

[  
\text{explicit 2-hop}  
\rightarrow  
\text{GAT implicit multi-hop}  
\rightarrow  
\text{recurrent whole-graph propagation}  
\rightarrow  
\text{temporal/Transformer adaptive aggregation}.  
]

DRL-THSA 早在 2019 就直接使用 two-hop state；GraphPR 通过反复交换 GAT hidden state 隐式获得多跳状态；Weil 进一步把“观测 neighborhood 多大”本身视为 communication overhead / responsiveness / action quality 的 trade-off；LEO 领域又已经出现 GAT-LSTM-DQN 和 temporal graph convolution 路由。([ResearchGate](https://www.researchgate.net/publication/335372940_A_Two-Hops_State-Aware_Routing_Strategy_Based_on_Deep_Reinforcement_Learning_for_LEO_Satellite_Networks?utm_source=chatgpt.com "(PDF) A Two-Hops State-Aware Routing Strategy Based on ..."))

所以如果论文贡献写成：

> “我们将一跳扩展到 (k) 跳，并用 GAT 自动选择有用邻居。”

我认为会比较危险。

---

# 哪些主张已经被占，哪些还能站住

### 已经不要再主张

- **“首次在 LEO DRL 中考虑 routing-state freshness/staleness”**：DRL-THSA 2019 直接反例。([ResearchGate](https://www.researchgate.net/publication/335372940_A_Two-Hops_State-Aware_Routing_Strategy_Based_on_Deep_Reinforcement_Learning_for_LEO_Satellite_Networks?utm_source=chatgpt.com "(PDF) A Two-Hops State-Aware Routing Strategy Based on ..."))

- **“首次提出 age-aware attention”**：Zhu et al. 直接反例。([arXiv](https://arxiv.org/abs/2208.08606 "[2208.08606] AoI-based Temporal Attention Graph Neural Network for Popularity Prediction and Content Caching"))

- **“首次 GAT+AoI”**：NGAT 等已经存在，而且 NGAT 甚至把 AoI 放进 node feature。([arXiv](https://arxiv.org/html/2404.18084v6 "Graph Attention Reinforcement Learning for Multicast Routing and Age-Optimal Scheduling"))

- **“首次用时序模型处理动态 LEO 路由”**：Chou GAT+LSTM、ADRLRM STGNN 等已经占了。([arXiv](https://arxiv.org/html/2605.02413v1 "Spatial-Temporal Learning-Based Distributed Routing for Dynamic LEO Satellite Networks"))

- **“首次通过多跳 GNN 缓解局部可观测性”**：GraphPR/Weil 都会反驳。([IEEE Xplore](https://ieeexplore.ieee.org/document/10755127/?utm_source=chatgpt.com "Fully-Distributed Dynamic Packet Routing for LEO Satellite ..."))

- **“首次 action-conditioned graph routing”**：Almasan 2022 已经非常明确。([ar5iv](https://ar5iv.labs.arxiv.org/html/1910.07421?utm_source=chatgpt.com "Deep Reinforcement Learning meets Graph Neural Networks"))

### 目前仍站得住，但必须谨慎措辞

**第一，field-wise routing-observation age。**

定义最好不要直接叫普通 AoI，而是明确区分，例如：

# [

\Delta_{ij}^{(f)}(t)

t-\tau_{ij}^{(f)},  
\qquad  
f\in  
{q,;B,;\text{availability},;d,\ldots}.  
]

可以叫：

- **Age of Observation (AoO)**

- **Routing-State Age (RSA)**

- observation staleness

这样不会让审稿人首先想到 RAoI/RRS-DRL 那种 packet freshness。

**第二，让 age 表示“可信度”而不是只做 timestamp freshness check。**

这是你和 DRL-THSA 最重要的区别：

[  
\text{DRL-THSA: }  
\tau\rightarrow{\text{accept},\text{drop}}  
]

而你应该做成：

[  
\Delta  
\rightarrow  
g_f(\Delta,\text{content},d,e,a)  
\rightarrow  
\alpha_{ij}.  
]

也就是把 freshness 从**协议规则**变成**策略可以学习利用的 uncertainty signal**。

**第三，destination-conditioned message passing 目前仍有空间。**

GraphPR 的 destination 是在 GAT 后进入 FCNN，不参与邻居 representation 的形成。([Scribd](https://www.scribd.com/document/1065983162/Fully-Distributed-Dynamic-Packet-Routing-for-LEO-Satellite-Networks-a-GNN-Enhanced-Multi-Agent-Reinforcement-Learning-Approach?utm_source=chatgpt.com "Fully-Distributed Dynamic Packet Routing for LEO Satellite ..."))

所以你可以使：

# [

m_{j\rightarrow i}^{(a)}

\phi  
\left(  
h_i,h_j,  
e_{ij},  
z_d,  
\Delta_{ij},  
z_a  
\right),  
]

而不是先得到 destination-agnostic 的 (h_i)，最后再拼 destination。

但 **Target-Aware GNN-DQN Adaptive Routing for LEO Satellite Networks** 已于 2026 年出现；由于我没有获得足够的公开方法正文，目前无法验证它是否已经把 target 真正放进 message passing。([ACM Digital Library](https://dl.acm.org/doi/10.1007/978-981-92-3381-6_46?utm_source=chatgpt.com "Target-Aware GNN-DQN Adaptive Routing for LEO ..."))

因此目前绝不能写：

> “No prior LEO GNN routing method conditions graph representation on destination.”

最多写：

> “Among the fully verifiable methods examined here, GraphPR does not inject destination information into its GAT message-passing stage; the exact target-conditioning architecture of Cai et al. (2026) could not be verified from accessible material.”

---

# 我建议你把算法方向收成这样

不是：

> **Age-aware GAT for LEO routing**

这个太宽，而且 Zhu 2023 会直接撞。

而是：

> **Staleness-aware destination-conditioned local graph routing under asynchronous telemetry**

真正科学问题变成：

[  
\boxed{  
\text{当邻居状态异步、延迟、丢失且不同字段陈旧速度不同的时候，  
知道“这条状态有多旧”是否比单纯增加 }k\text{-hop、  
LSTM 和记忆式 GNN 更有价值？}  
}  
]

这个问题比“我加了一个 AoI feature”强很多。

---

## 还有几个你当前算法想法里的漏洞

### 1. “越旧权重越低”本身不成立

这是目前最大的问题。

一个 500 ms 前获得的链路容量可能仍然完全可靠，而一个 20 ms 前的 queue snapshot 可能已经因为 burst traffic 完全失效。

所以不能简单设计：

[  
\alpha_{ij}  
\propto e^{-\lambda\Delta_{ij}}.  
]

你真正需要的是**feature-dependent age semantics**：

# [

g_{ij}^{(f)}

g_f  
\left(  
x_{ij}^{(f)},  
\Delta_{ij}^{(f)}  
\right).  
]

甚至让：

[  
\lambda_q\neq  
\lambda_{\text{bandwidth}}\neq  
\lambda_{\text{availability}}.  
]

否则 reviewer 很容易问：为什么 age 与 reliability 单调对应？

---

### 2. 多跳 age 不能只记录“最后收到消息的时间”

假设 C 的 queue 在 (t_0) 被 B 获得，B 在 (t_1) 又把 embedding 发给 A。

如果 A 只记录：

[  
t-t_1,  
]

它会错误认为 C 的信息很新。

真正年龄应该保留 provenance：

# [

\Delta_{\text{effective}}

t-\tau_{\text{source observation}},  
]

或者让 age 随 message passing 传播。

**这一点反而很可能成为比单纯 age-attention 更有研究价值的部分。**

---

### 3. 不要把“动作条件读出”作为贡献

DQN 本质上就在估计

[  
Q(s,a),  
]

GraphPR FCNN 本身也写成 (F(h\Vert s^p,a))，Almasan 又已经显式把候选 action 注入 MPNN。([Scribd](https://www.scribd.com/document/1065983162/Fully-Distributed-Dynamic-Packet-Routing-for-LEO-Satellite-Networks-a-GNN-Enhanced-Multi-Agent-Reinforcement-Learning-Approach?utm_source=chatgpt.com "Fully-Distributed Dynamic Packet Routing for LEO Satellite ..."))

你可以保留这个结构，但应该把它降格为 architecture design，而不是 contribution。

---

### 4. “更大 k”甚至可能和你的主线冲突

(k) 越大：

[  
\text{coverage}\uparrow  
]

但通常也意味着：

[  
\text{signaling overhead}\uparrow,\qquad  
\text{propagation age}\uparrow,\qquad  
\text{state inconsistency}\uparrow.  
]

Weil 已经明确指出 neighborhood size 与 reactivity、action quality 和 communication overhead 之间的 trade-off。([arXiv](https://arxiv.org/html/2402.05027v3 "Towards Generalizability of Multi-Agent Reinforcement Learning in Graphs with Recurrent Message Passing"))

所以你的论文最好不是证明：

> (k=3) 比 (k=1) 好。

而是证明：

> **在相同通信预算下，age-aware aggregation 能从较广但不一致的局部信息中获得收益，而普通 GAT 随 (k) 增大反而因陈旧信息恶化。**

这会形成更有力的研究问题。

---

# 最后给你的 novelty 审判

按目前证据，我会这样给你的几个潜在 contribution 打分：

| 主张                                                                     | 现在还能不能写成主要创新                              |
| ---------------------------------------------------------------------- | ----------------------------------------- |
| Routing-state freshness/AoI                                            | ❌ 宽泛表述不行                                  |
| Timestamp 纳入 LEO DRL state                                             | ❌ DRL-THSA 已碰                             |
| **连续 field-wise observation age**                                      | **✅ 目前仍有空间**                              |
| Age-aware attention                                                    | ❌ 泛化机制已有                                  |
| **Observation-age-conditioned routing attention**                      | **✅ 有空间**                                 |
| GAT + LEO DRL                                                          | ❌ 很拥挤                                     |
| k-hop local graph                                                      | ❌                                         |
| 自适应邻居权重                                                                | ❌                                         |
| temporal modeling                                                      | ❌                                         |
| edge-aware message passing                                             | ❌ 泛化机制已有                                  |
| action-conditioned representation                                      | ❌                                         |
| **destination-conditioned message passing in distributed LEO routing** | **⚠️ 很可能有空间，但 Target-Aware 2026 必须进一步排雷** |
| **destination + edge + field-age 联合条件化**                               | **✅ 未找到直接重合，但“模块组合”本身不够成为论文理由**           |
| **固定通信预算下对 asynchronous/stale telemetry 的鲁棒逐包路由**                      | **✅ 我认为这是目前最值得收窄的核心问题**                   |

因此，如果现在让我替审稿人概括你真正还有机会站住的贡献，我不会说“提出一个新的 GAT”。

我会把它压成一句：

> **现有分布式 LEO DRL 路由已经使用局部、多跳、图注意力和时序表示，也已有工作显式维护链路状态 timestamp；真正尚未看到被解决的是：在异步且字段级陈旧的局部遥测下，让逐跳路由策略显式知道每条观测的实际年龄，并把这种 freshness 作为与 destination、candidate edge 联合条件化的决策可信度，而不是把所有收到的邻居状态等价地当作当前状态。**

这比你原来“**AoI + GAT + k-hop**”的 novelty 边界窄很多，但也明显更抗证伪。
