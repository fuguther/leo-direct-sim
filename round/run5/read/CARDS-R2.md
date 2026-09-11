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

## 57EB6US5 — Human-level control through deep reinforcement learning

**1. 一句话**
用同一个深度卷积网络 + 同一个 Q-learning 变体，直接从 210×160 的像素学 Atari 49 个游戏的控制策略，靠**经验回放**和**独立目标网**这两招把"非线性函数逼近 + 自举"必然发散的老问题压住。

**2. 问题设定**
RL 用神经网络逼近动作价值函数时"已知会不稳定甚至发散"（L17 逐字："Reinforcement learning is known to be unstable or even to diverge when a nonlinear function approximator such as a neural network is used to represent the action-value (also known as Q) function"）。作者列出三个具体成因（L17）：观测序列内的相关性、Q 的小改动会显著改变策略从而改变数据分布、Q 与目标值 $r+\gamma\max Q(s',a')$ 之间相关。此前 RL 的适用面被限制在"特征可手工设计"或"状态空间低维且完全可观测"的域（L5）。

**3. 方法骨架**
- **状态**：不是当前帧，而是**帧序列** $s_t = x_1,a_1,\dots,x_t$（L161），因为单帧是 POMDP 且有感知混叠；实际用 $\phi$ 取最近 4 帧（$m=4$，作者注明 3 或 5 也稳，L137）。
- **动作**：每个合法动作一个输出单元，因此**一次前向传播算出所有动作的 Q**（L141 明确对比了"历史-动作对做输入"的旧做法要按动作数线性次前向）。
- **网络**（L143）：输入 84×84×4 → conv 32×8×8 stride 4 → conv 64×4×4 stride 2 → conv 64×3×3 stride 1 → FC 512 → 线性输出层。每层后 ReLU。合法动作数 4–18。
- **奖励**：训练时**裁剪**，正奖 +1、负奖 −1、0 不变（L145）。
- **更新**（L22 损失、L180 梯度）：$L_i(\theta_i)=\mathbb{E}_{(s,a,r,s')\sim U(D)}[(r+\gamma\max_{a'}Q(s',a';\theta_i^-)-Q(s,a;\theta_i))^2]$。两个机制：
  1. **经验回放**（L189）：$e_t=(s_t,a_t,r_t,s_{t+1})$ 存进容量 N 的回放池，均匀随机抽 minibatch。好处作者列了三条：单步经验被多次复用（数据效率）、打破样本相关性降方差、"在线学"会因参数决定下一个样本而形成反馈环并可能卡在坏的局部极小或灾难性发散（L189 原文 "the parameters could get stuck in a poor local minimum, or even diverge catastrophically"）。回放必须 off-policy，因此选 Q-learning（L189 末）。
  2. **独立目标网**（L193）：每 C 次更新把 Q 克隆给 $\hat Q$，之后 C 次更新都用 $\hat Q$ 产生目标，等价于"给更新与目标之间加一段延迟"。
- **额外技巧**：误差项裁剪到 [−1,1]，等价于在 (−1,1) 外改用绝对值损失（L195）。
- Algorithm 1 完整伪码在 L197–L231。

**4. 它声称的效果**
- 在 49 个游戏里的 **43 个**上超过当时最好的 RL 方法，且未用任何游戏先验知识（L33）。
- 在 **29 个**游戏上达到人类专业测试者 75% 以上分数（L33）；"broadly comparable with or superior to"（L47）。
- 归一化口径明确定义（L46）：100×(DQN − random)/(human − random)。
- Extended Data Table 2（L260）给全 49 局逐局数字。极端例：Boxing **1707.9%**、Video Pinball **2539.4%**、Breakout 1327.2%；反例 Asteroids **7.3%**、Gravitar **5.3%**、Private Eye **2.5%**、**Montezuma's Revenge 0.0%（DQN 得分 0，random 也是 0）**。
- **消融**（Extended Data Table 3，L265）：10M 帧、三档学习率下，回放与目标网两两组合。Breakout：有回放有目标 316.8 / 有回放无目标 240.7 / 无回放有目标 10.2 / 两者皆无 3.2。**回放是主要贡献者，目标网是次要但正向的增益**。
- 线性函数逼近对照（Extended Data Table 4，L270）：Breakout 316.8 vs 3.00。
- 基线：Best Linear Learner、Contingency (SARSA)、random play、职业人类测试者（L259）。
- t-SNE 可视化（L51、Fig 4）显示表征会把"感知不同但期望回报相近"的状态映射到一起；Extended Data Fig 1（L241）显示对**人类策略产生的**状态也能泛化。

**5. 实验条件**
- 49 个 Atari 2600 游戏；**每个游戏单独训一个网络**，但架构/算法/超参完全一致（L145）。
- 训练：50M 帧（约 38 天游戏时间）、回放池 1M 帧、RMSProp、minibatch 32、γ=0.99、ε 从 1.0 线性退火到 0.1（前 1M 帧）后固定 0.1、帧跳过 k=4、每 4 步更新一次、目标网每 10000 次参数更新同步、学习率 0.00025（L147、L149、Extended Data Table 1 at L255）。
- **超参靠非正式搜索**：只在 Pong/Breakout/Seaquest/Space Invaders/Beam Rider 上试，未做系统网格搜索（L151、L257 逐字："We did not perform a systematic grid search owing to the high computational cost"）。
- 评估：每局 **30 次**、每次最多 5 分钟、不同初始随机条件（no-op）、**评估时仍用 ε-greedy 且 ε=0.05**（L155）。人类测试者约 20 局 × 5 分钟，每游戏约 2 小时练习（L157）。
- **训练与评估不是同一套**：训练用裁剪奖励（±1），评估用未修改的游戏（L145 逐字 "While we evaluated our agents on unmodified games, we made one change to the reward structure of the games during training only"）；且 ε 训练 0.1 → 评估 0.05。
- 消融实验用的是 10M 帧而非主结果的 50M 帧（L267），作者明确提示因此 Enduro 分数高于 Table 2。

**6. 它自己承认的局限**
**没有独立的 Limitations 章节**（全文通读：正文至 L61 结束，之后是 Methods L135–L231、扩展数据 L239–L270，无 limitation 小节）。可逐字引用的自述有三处：
- 奖励裁剪的代价，L145 逐字："At the same time, it could affect the performance of our agent since it cannot differentiate between rewards of different magnitude."（承认裁剪后**无法区分不同量级的奖励**）
- 回放采样策略，L191 逐字："This approach is in some respects limited because the memory buffer does not differentiate important transitions and always overwrites with recent transitions owing to the finite memory size N."（承认均匀采样把所有转移等权，且有限容量会覆盖）
- 长时程规划仍是硬骨头，L59 逐字："Nevertheless, games demanding more temporally extended planning strategies still constitute a major challenge for all existing agents including DQN (for example, Montezuma's Revenge)."
- 超参未系统搜索，L257（见第 5 项）。

**7. 它没做但看起来能做的地方（基于内容）**
1. **奖励裁剪与"不同量级不可区分"之间的矛盾**（L145）：作者自己点出裁剪丢失量级信息，却仍用它换跨游戏同一学习率。对任何"惩罚项有物理量纲"的场景（例如时延毫秒数、丢包率），裁剪是**不可接受**的——这篇没解决的正是这个问题。
2. **优先回放**：作者在 L61 和 L191 两处点出 prioritized sweeping，但只说"未来重要"，没做。
3. **绝对成功 vs 绝对失败的分界未解释**：Asteroids 7.3% 与 Boxing 1707.9% 用同一套超参，论文没有做失败归因；只有一句"长时程规划难"。
4. **评估时仍带 ε=0.05 探索**（L155）：意味着报告的数字不是纯贪心策略的性能，greedy 策略的真实上限未被单独报出。
5. **帧跳过 k=4 是固定常数**（L149）：作者说这是为了省算力，但没测 k 与性能的关系——而"决策频率"恰是 LEO 路由里的核心约束（参见同批 53HEEK33 的"感知周期 t"）。

**8. 和同批其他篇的关系**
**这是本批唯一的基础方法论文，不是"网络"论文**。它与同批其他篇的关系是"被引用/被取代的底座"：同批的 LEO 路由类论文（如已读的 53HEEK33）用的还是**表格型 Q-learning + 手工离散状态**（53HEEK33 的 L90 Table 1、L109 明说因动作空间只有 4 而不用深度网络），而本篇正是"把 Q 表换成深度网络"的那一步。换言之：本篇是 53HEEK33 与后续所有 DRL 路由论文之间的**谱系断点**。在本批 11 篇里它不像任何一篇（不涉及卫星、拓扑、排队）；其余 10 篇是否引用它，待后续卡补证。

**9. 对"负载变化下到达率/时延"的贡献**
**没有直接贡献**——本篇不涉及网络、不涉及到达率、不涉及排队时延。但有四条**方法论级**、对做 LEO 路由 RL 时会被直接踩到的约束事实：
1. **奖励裁剪会摧毁量级信息**（L145 自述）：如果把排队/传播时延写进奖励，±1 裁剪后"10 ms 惩罚"和"200 ms 惩罚"在梯度里等价——这是把 DQN 直搬到路由奖励上时的真实陷阱。
2. **回放是防发散的第一要素，目标网是第二**：消融给出 Breakout 316.8→3.2（无回放无目标）的数量级差距（L265）。任何"在线、逐步、on-policy"的 LEO 路由学习方案都要回答它靠什么替代这两个机制。
3. **决策/动作重复频率是一个被显式选择的超参**（action repeat k=4、update frequency 4，L255）：与 LEO 路由"多久重算一次路由/多久推理一次"同构，且本篇没有对 k 做敏感性分析。
4. **评估口径含探索**（ε=0.05，L155）：提醒任何报告"负载变化下时延/到达率"的实验必须说清评估时用的是 greedy 还是 ε-greedy。

**10. 一句话评价**
**把"深度网络 + Q-learning 会发散"这个开放问题用两个工程机制（经验回放、目标网）关掉的开创性工作**——它不是为网络设计的，它的价值在于此后所有 DRL 路由论文都得先继承（或被裁剪版继承）它的这两个机制，同时也要继承它那份"奖励量级不可区分"的技术债。

## 5AZHJE7N — Network Simulators for Satellite-Terrestrial Integrated Networks: A Survey

**1. 一句话**
把 2012–2022 十年间做星地一体化网络（STIN）仿真的 31 个工具清点了一遍，首次分成六类（星向、5G 向、通用网络仿真器扩展、SDN、云化、其他），并给出一张"每个工具到底支持哪些仿真功能"的对照表——**结论是这块领域"仍在早期探索阶段、没有成熟方案"**（L464 逐字："the research of developing STIN simulators is still in an early exploration stage with no mature solutions"）。

**2. 问题设定**
LEO 巨星座（Starlink 规划 42000 颗，L80）让仿真变成刚需：真机试错成本极高（引 SpaceX Falcon 9 每公斤 2720 美元、单星约 62 万美元，L21）。而仿真本身遇到五个新增难点（L100–L102）：>40000 节点的算力/内存、LEO 时速超 27000 km/h 导致的频繁重连与切换、恶劣空间环境下的链路建模、卫星与地面协议标准（如 CCSDS）异构并存、拓扑高动态。核心矛盾：**做 STIN 仿真需要同时用天体动力学工具（算轨道）+ 包级网络仿真器（算协议），而这两类工具历来是割裂的**（L170 逐字："astrodynamics simulators must be used jointly with other tools"）。

**3. 方法骨架**（这是一篇综述，无算法；"方法"= 它的分类学与评估框架）
- **五条需求**（L106–L114）：Fidelity（保真）、Scalability（从几个到上万个节点）、Extensibility（可加新节点/链路模型）、Agility（可调拓扑与配置）、Real-time（实时）。
- **四层评估指标分类**（Fig 4，L128–L136）：
  - 应用层：QoS/QoE、支持的应用与用户类型、可扩展性；
  - **网络层：吞吐、PER、端到端时延、时延抖动**；且**专门列出路由与负载均衡算法类指标，包括路由协议收敛时间和避免拥塞的负载均衡能力**（L132 逐字："the routing and load balancing algorithms, which include the convergence time of routing protocols and the load balancing ability to avoid network congestion"）；
  - 物理层：SIR、频谱效率、BER、链路带宽；
  - 几何层：星座覆盖、系统冗余、**链路持续时间**。
- **通用 STIN 仿真框架四部件**（Fig 5，L144–L158）：infrastructure（含虚拟化/云、半实物）、input（用户配置 + 拓扑 + **生成的流量** + 天体动力学 + 离散事件发生器）、core（控制/SDN/AI 模块 + 传输 + 路由）、output（GUI + 评估模块）。
- **"三个关键仿真功能"**（L257–L263）：卫星轨道仿真、物理层建模、**网络协议与算法评估**。统计结果：轨道 11/31（35.48%）、物理层 21/31（67.74%）、协议算法 18/31（58.06%）（L265、Table 6 at L276）。
- **规模统计**（Table 7，L279）：绝大多数工具只支持 <10 颗星；支持 ≥1000 颗的只有 STK、LSNS[71]、Hypatia[55]、SILLEO-SCNS[69]、Celestial[58]、[53]、Stargaze[81]。
- **开放源码清单**（Table 5，L251）给了 17 个工具的 GitHub/GitLab 链接（OS3、ns-3 satellite mobility、OpenSAND、LSNS、Hypatia、SILLEO-SCNS、Trunks、ESTNeT、FLoRaSat、DLinkEm、SMN Simulator、Celestial、5G-SpaceLab、Stargaze 等）。
- **选型指南**（Table 8，L438）：逐工具列支持 OS、编程语言、文档完善度、典型用例。

**4. 它声称的效果**
综述类，无性能数字，但有三组**可核验的统计事实**：
- 功能覆盖统计：轨道 35.48% / 物理层 67.74% / 协议算法 58.06%（L265，分母 31）。
- 规模分布（Table 7）：<10 颗的工具占绝大多数；≥1000 颗的 7 个（L279）。
- 时间线（Fig 7，L239）：2010 GEMINI/MACHETE → 2012 SATSIM → 2013 OS³ → 2014 SNS3 → 2016 CogSWEL → 2017 OpenSAND → 2020 SGIN-Stack/Hypatia → 2021 Trunks/ESTNeT/OOSN-EP → 2022 SMN Simulator/Celestial；并标注引入 Hardware-in-the-loop / GUI / SDN / Virtualization / Cloud Computing 的时间点。
- 单点数字（转述自被引文献）：OOSN-EP 平均传输时延误差 0.4 ms、时间精度 5 ns（L309）；Starlink 至 2023-06-04 已发射 4543 颗（L80）；[53] 的仿真器扩展到 1500 颗星（L327）；LSNS 支持到 1000 颗 LEO（L315）。

**5. 它的"实验条件"**（综述 = 检索与分类口径）
- 时间范围：约 2012–2022 十年（L35）。
- 范围界定：**只收"系统级仿真器"（可独立运行、能研究系统性能、验证概念、评估实现选项）；基于 MATLAB 等通用语言的"算法级仿真"明确排除在外**（L227 逐字："Many studies are based on algorithm-level simulations... and are out of the scope of this survey"）。
- 分类维度（Table 4，L244）：年份、依赖项、地面网支持、SDN 支持、Hardware-in-the-loop、GUI、是否开源。
- 明确说明各工具的年份取自对应出版物、实际发布时间可能略早（L237）。
- **没有做**统一的横向实测对比（L411 逐字："The in-depth comparison and testing of the covered network simulators in this study are on-going works"）。

**6. 它自己承认的局限**
- 横向对比缺失，L411 逐字："The in-depth comparison and testing of the covered network simulators in this study are on-going works and would be presented in our future studies."
- 数据可用性，L195 逐字："However, there is still a lack of a real-world network traffic dataset for STIN simulation."
- 真实流量统计稀缺，L195 逐字："there are only some very limited real-world traffic statistics from a global scope for simulating satellite networks."
- 恶意/异常行为未被建模，L427 逐字："without considering malicious and abnormal user behaviors in more realistic scenarios."
- 硬件在环的可行域受限，L253：多数卫星系统由私企运营、不公开技术规格，因此**无法接入网络仿真器**。
- AI 方法无可比基准，L450 逐字："While AI models have been introduced in many studies, their performance is evaluated in different settings and without a unified dataset, e.g., ImageNet for image classification."

**7. 它没做但看起来能做的地方（基于内容）**
1. **"三个关键仿真功能"里根本没有"流量/负载建模"**（L257–L263）。它的框架 Fig 5 里明明有 "generated traffic" 这一格（L154），但 Table 6 的统计维度只有轨道/物理层/协议三列——也就是说，**"仿真器怎么产生负载"这件事在这篇最全的盘点里从未被系统性核查过**。这是本文自己结构里露出的洞。
2. **五条需求中没有一条涉及负载强度的可配置性/可标定**（L106–L114）：Agility 只说"调整网络拓扑和配置"，未提流量。
3. **网络层指标里已有时延抖动（delay jitter）和负载均衡能力**（L132），但全文没有一处给出"到达率 → 时延/丢包"这类负载-性能曲线的评测实践。
4. SatSysSim 是全文**唯一**明确写出泊松到达 + 到达率的工具（L301：用户按泊松分布到达，每用户流量需求 <100 kbits/s，按 SNR 优先级贪心分配），但它只覆盖 DVB-RCS2 返回链路、星数 <10——这个"有到达率建模"的样本没有被作者当作一条线索追下去。
5. DLinkEm 能改链路属性（容量与时延，L381）、Hypatia 能可视化链路利用率与可用带宽随时间变化（L317），二者都在"链路层"层面接近我们关心的东西，但都没有把**负载变化**作为自变量。
6. 作者自己列的"未来方向 AI 集成"（L446）只提到 ns3-gym 把 OpenAI Gym 接进 ns-3（L448）和 benchmark 数据集缺失（L450），**没有提到"RL 训练需要可复现的负载场景"这一更底层的前提**。

**8. 和同批其他篇的关系**
- 与 53HEEK33：53HEEK33 是自建 49 星仿真环境 + 表格 Q-routing，按本篇的界定属于**被排除的"算法级仿真"**（L227）；本篇正好给出了"这类工作所在生态位"的元视角——不难看出 53HEEK33 那类工作不会出现在这张表里。
- 与 57EB6US5：本篇引用了 ns3-gym（[106]）这条"网络仿真器 + RL"的线，与 DQN 所属的通用 DRL 方法谱系是两条平行线（本篇不引 DQN）。
- 本批其余 9 篇是否被本篇收录或引用，待后续卡补证。

**9. 对"负载变化下到达率/时延"的贡献**
**这是本批至今与本选题最相关的一篇"元证据"，但它的贡献是负向的（指出缺口），不是正向的（给出事实）。**三条可引用的硬事实：
1. **指标侧：本选题关心的量已经被明确列为 STIN 仿真的网络层标准评测指标**——端到端时延、时延抖动、PER、吞吐，外加"路由协议收敛时间"与"避免拥塞的负载均衡能力"（L132）。也就是说，评测口径不缺；缺的是把这些口径组织成"负载扫描"的实践。
2. **工具侧：31 个工具的核对表里没有"负载/到达率建模"这一列**（Table 6，L276），且"三个关键功能"不含流量（L257–L263）。这直接说明：**在 STIN 仿真这块，负载是被当作输入随便给的，不是被当作可标定、可复现的自变量**。
3. **数据侧：作者两次强调真实流量数据缺失**（L195），这解释了为什么"负载变化"研究难以对齐——没有共享的负载场景，跨论文的"到达率"数字不可比。
4. 旁证细节：全文只有 SatSysSim 一处出现"到达率"这个词（L301）；DLinkEm 能改容量/时延但不能改负载强度（L381）；Hypatia 能看链路利用率随时间变化（L317）。

**10. 一句话评价**
**一份把"仿真工具"当成研究对象的领域盘点，它的最大价值不在推荐了哪个工具，而在于它的统计表把整个领域"重拓扑/物理层、轻流量负载"的偏向暴露了出来**——恰好为我们"负载变化下到达率/时延"的选题提供了一条外部旁证：这个自变量在 STIN 仿真生态里至今没有被制度化地对待。

## 5HJ8ATR7 — Democratizing Direct-to-Cell Low Earth Orbit Satellite Networks

**1. 一句话**
把蜂窝网的"逐跳有状态会话"换成"预付一次性代币"（借鉴离线现金的 restrictive blind signature + SIM 卡本地扣款），让 LEO 直连手机卫星可以**不联系远端运营商就地自助服务**，从而把多租户共享从 GEO 透明管道时代推进到 4G/5G LEO 时代。

**2. 问题设定**
多租户 LEO 直连手机卫星（MNO 租 SNO 的星、把自己的授权频谱借给它）三方都想要，但现有两条路都堵死（L94、L36–L38）：
- **透明管道（GEO 老办法）** 在 LEO 上三条死因（L120–L130）：(1) 覆盖不完整——UE 和地面站必须同时落在同一颗星覆盖内（L122）；(2) **错过 4G/5G 无线截止期**——每个 IQ 采样必须 250 µs 内送到地面站（对应 80 km 星地距离），而 LEO 距离至少 340 km（L128）；(3) **带宽不可承受**——单星承载的所有 UE 的 IQ 采样要 7.86 Gbps（5 MHz 信道），而 ISL 通常只有 20 Gbps，会累积拥塞（L130）。
- **在轨蜂窝功能（Starlink Gen2 的 option-2 拆分、3GPP NTN 的 option-1/2）** 虽然解决了截止期问题，但带来**紧耦合**与**频繁变化的 SNO-MNO-UE 多对多关系**（L145–L169）。

**3. 方法骨架**（系统设计，无 RL；核心是协议/密码学重构）
- **三条设计原则**（L180–L186）：松耦合（卫星不联系远端 MNO 就地服务）、简化的 SNO-MNO-UE 关系（代币取代会话状态）、保留电信级服务（漫游/QoS/计费策略嵌进代币）。
- **§5.1 自足在轨蜂窝功能**：每颗星跑完整 4G/5G RAN + UPF；加一个**会话状态代理（session state proxy）**模拟核心网控制面（NGAP/GTP-U），用 UE 付的代币喂状态（L206）。采用 **Earth-fixed 地理小区**（继承 SpaceCore）——小区按地理定义而非按卫星定义，用仿射球坐标对齐轨道参数把映射线性化（L210）。
- **§5.2 代币**：MNO 用私钥 x 与公私钥对生成；UE 持 SIM 生成第三随机数 o2 算出 (A,B)；MNO 把 (A,B) 与**会话状态 p**（位置相关漫游、QoS、计费、接入控制）通过哈希绑定并签名，UE 存 <A,B,sign(A,B)> 作为代币（L225–L227）。**一次性**靠 SIM 卡本地强制：挑战-响应必须用到存在 SIM 里、永不外泄的 o2，用完后 SIM 删除 o2，重复花费即挑战失败（L236）。清结算可在线或离线（卫星攒 token bucket，飞到地面站再结算），SIM 被破解的最坏情况由 MNO 事后比对数据库检测并拉黑（L238）。
- **§5.3 带内控制自服务**：UE 先按广播身份选任意可信卫星、用基于身份的密码学做认证与密钥协商，再用标准 ULInformationTransfer/DLInformationTransfer 容器捎带（**不改 COTS UE 硬件、不改标准接口**，L242、L248）。下行靠把 UE 的 IP 地址设计成 PLMN.cell-ID.UE-identity，用地理小区定位 UE 从而避免全小区寻呼（L255）。
- **部署**（§6）：MOSAIC 作为**外挂代理**不修改蜂窝功能（L277）；MNO 侧复用 HSS/UDM 与 OCS/CHF（L290）；UE 侧做成 SIM applet + 手机 App（L281、L292）。

**4. 它声称的效果**（全部相对 NTN / Starlink / SpaceCore 三个基线）
- **可服务区域 +116%**，在星座自身地面覆盖内达到 100% service ratio（L334、L42）。
- **服务建立时延**降低：相比 NTN，Starlink **5.19×**、Globalstar **1.33×**、Iridium **2.33×**（L332）；比 SpaceCore 略高 0.33×（为兼容 COTS UE 付出的代价）。
- **ISL 上的信令风暴**：省下 850–7,640 倍信令成本、**4.71–14.25 倍**服务恢复时延（L370）。
- **寻呼信道负载**降低 23×/4×/8×（Starlink/Globalstar/Iridium）；假设 5 MHz 频段、**400 UEs/km²**；NTN 与 SpaceCore 的寻呼负载**甚至超过 4G/5G 信道容量**（L359）。
- **动态重映射 CPU 周期**降低 100×/63×/73×（对比 H3 六边形与经纬矩形小区，L336）。
- **代币开销**：消费时延 16.4 / 41.9 / 34.8 ms（L340）；单张商用 SIM 可存 3,279–19,661 个代币的 160-bit 元数据（L349）；单核 2.30 GHz Xeon Gold 5218 上每 MNO 生成 1,175 token/s、验证 1,401 token/s（L351）。
- **最坏代币滥用时长**被限制在 0.2–0.88 个轨道周期（22.8–87.7 分钟）（L353）。

**5. 实验条件**
- 三类证据组合（L296）：定性分析 + 原型微基准 + **数据驱动的大规模 what-if 仿真**。
- **真实数据**（Fig 3，L79）：TLE 50,922,755 条；自建 IridiumRF 接收机 943,003 条 RF 链路测量；RIPE Atlas 上 50 个 Starlink 碟形终端的 7,800,177 条 ping 与 382,464 条 traceroute；Thuraya X5-Touch 与 Tiantong T900 手机的 3,903,065 条 PHY/MAC/RLC/RRC/NAS 日志。
- **原型**（Fig 13，L292）：Amarisoft Callbox NR-4-U Ultimate 两台（一台当 SNO 卫星、一台当 MNO 地面核心网），sysmoISIM-SJA2 可编程 SIM，Android App，COTS 手机含华为 Mate 60 Pro（天通 GEO 2G GMR 直连）与 Mate 50（北斗 GEO 短报文）。
- 星座：Starlink Phase II、Globalstar、Iridium（L334）；单星覆盖 3 分钟（7.6 km/s，L149）。
- 默认负载假设：**400 UEs/km²**（引 [91]，L359）、5 MHz 4G/5G 频段、ISL 20 Gbps（L130）。

**6. 它自己承认的局限**（**有独立的 §8 Limitations，L372–L374，逐字**）
"(1) For SNOs, while MOSAIC's pay-as-you-go token grants service access, **it does not guarantee verifiable carrier-grade service**. Selfish SNOs may not offer carrier-grade services after gaining tokens, thus causing overbilling."
"(2) For MNOs, ... the offloaded cellular functions to satellites still cannot be directly managed by MNOs. How to enhance MNOs' configurability and manageability of on-board satellite cellular functions deserves further research."
"(3) For UEs, MOSAIC's tokens suppress signaling overhead **at the cost of some UE-to-satellite bandwidths** due to its in-band control. It is worth exploring how to compress tokens for more bandwidth-efficient pay-as-you-go services."
另：§A 承认 SNO 拒不服务的问题"在陆地蜂窝网已存在数十年"（L641）。

**7. 它没做但看起来能做的地方（基于内容）**
1. **性能评估里没有任何"负载随时间的动态变化"**：论文的所有负载都是稳态假设（400 UEs/km²、固定 UE 数）。而它的整个动机恰恰是"卫星 3 分钟扫过一个区域，所有活跃 UE 会话要转交"（L149）——这是一个**负载在时间和空间上剧烈波动**的场景，论文却只用信令条数和 CPU 周期度量它，从未把"负载波动幅度"作为自变量。
2. **§8(3) 提到的"代币占用 UE-卫星带宽"从未被量化**：只承认存在，没给数字，也没与"信令省下的开销"做净额核算（L374）。
3. **代币消费时延（16.4–41.9 ms）与 §5.3 声称的"最小化信令"之间没有联合分析**：L340 只说"相对于 Fig 15 的节省是边际的"，没做端到端时延分解。
4. **离线清结算的 token bucket 容量与结算延迟未建模**（L238 只说"最终会飞到地面站"）。
5. Fig 15/17/18/21 的具体数值都藏在图里，正文只给倍数（L332、L334、L336、L370），**没有一张数值表**——复现门槛高。

**8. 和同批其他篇的关系**
- 与 **5AZHJE7N（STIN 仿真器综述）**：本篇是 5AZHJE7N 所说的"系统级仿真器"的典型用户（自建 what-if 仿真 + Amarisoft 商用协议栈），而非被综述覆盖的工具本身；5AZHJE7N 提到 STIN 仿真"缺少真实流量数据集"（其 L195），本篇恰好是一个**用真实卫星数据（TLE/RIPE/自建 RF）驱动仿真**的正面样本。
- 与 **53HEEK33**：两者都用 Iridium 作背景（53HEEK33 全部用 Iridium-like 49 星），但路径完全相反——53HEEK33 是"网络层路由算法 + 表格 Q"，本篇是"接入网/核心网协议 + 密码学"，**两者不在同一层**，没有可比基线。
- 与 **57EB6US5**：无关。
- 本篇 §9 Related Work（L378）明确把"network-layer routing [98–100]"划归他人的工作、自己不做；引用了 Handley 的 "Delay is Not an Option: Low Latency Routing in Space"（[100]）。
- 本批其余 7 篇是否与它互引，待后续卡补证。

**9. 对"负载变化下到达率/时延"的贡献**
**没有直接贡献（研究的是多租户架构，不是路由或负载响应）**，但有四条**可用的负载相关事实**：
1. **信令负载的绝对量级**：LEO 移动引发的会话迁移信令"可占用最多 **15.75% 的总 ISL 带宽**"（L149）——这是一个"控制面带宽随负载增长"的实测级数字，说明**在高负载下控制面会与时延敏感的数据面抢 ISL**。
2. **服务恢复时延被量化**：MOSAIC 相对 SOTA 省 4.71–14.25 倍（L370）；服务建立时延相对 NTN 省 5.19×/1.33×/2.33×（L332）——这些是"切换瞬间的时延"，与负载无关但与拓扑变化强相关。
3. **寻呼负载存在容量悬崖**：在 400 UEs/km² 下 NTN 与 SpaceCore 的寻呼负载"可能超过 4G/5G 信道容量"（L359）——这是本批至今少见的一条**"负载 → 系统崩溃"的明确定量边界**。
4. **负载在 LEO 下天然非平稳**：单星覆盖某区域仅 3 分钟（7.6 km/s，L149），意味着任一地面小区的到达率都在周期性跳变；但论文只把这个事实当作"信令风暴的原因"，**没有把它转成"负载变化下的性能曲线"**——这恰好是空档。

**10. 一句话评价**
**把密码学离线现金方案（Brands 1994）搬到 LEO 多租户接入上的系统重构**，方法谱系里属于"用计费/信任模型的替换来绕开移动性带来的状态管理"，与路由无关；它对本选题的价值是提供了一份"控制面开销随 LEO 移动被放大"的定量证据，以及一个明确的空白——**它自己承认负载场景是稳态假设的，却从未验证**。

## 5N5LQPPP — SDDRL-SR: A High-Reliability Satellite Routing Algorithm based on Deep Reinforcement Learning

**1. 一句话**
在 53HEEK33 同一作者组的下一步工作里，把"加速收敛"从控制面广播改成两招：**训练期用 Dijkstra 当老师做蒸馏**（称 DIRL），**执行期把 Q 目标改成两跳回收**（Two-Hop Convergence），据称收敛步数从 >1000 降到约 400。

**2. 问题设定**
DRL 路由收敛慢有两个来源（L17 逐字）："Firstly, in the pre-training phase, the agent needs a lot of trial-correction process... Secondly, in the satellite execution phase, if the ISL fails, the agent needs much time to sense it. It is because **information transfer between agents is linear**, resulting in a lag in the transfer of information between satellites."——与 53HEEK33 的动机完全同源（链路状态串行扩散）。作者自称两项首创：首个用传统算法引导 RL 学习阶段的工作、首个引入**两跳范围**信息提高 Q 值预测精度的工作（L17 末）。

**3. 方法骨架**
- **形式化（§II–III）**：二元整数优化（L85 式 7），目标是最小化 $\sum_t\sum_i\sum\alpha^{v_x,v_y}_{t,i}D^{v_x,v_y}_i(t)$，约束为：链路容量（式 1，每 ISL 同时处理的 event 数 ≤ $C_{max}$）、单事件唯一路径（式 2）、节点存储（式 3，接收包数 ≤ 剩余空间 $S_{max}$）、包只能"被转发或存着"二选一（式 5）。**每个路由请求 = 单个数据包**（L29 逐字："each event is configured to involve a singular packet exclusively"）。
- **时延式（式 6，L73）**：到达目的节点时为 0；否则 $D = d_{v_x,v_y}/C + \lceil \sum\beta^{v_x}_{t,i}/C_{max}\rceil - 1$，即**传播时延 + 用包数除以链路容量向上取整得到的排队时延**（注意：排队项用的是**节点已占用存储里包的数量**，不是到达率）。
- **状态**（L98）：$s_t = \{l^{v_0}_t, l^{v_d}_t, S^{v_0}_t, N^{v_0}\}$——本节点位置、目的节点位置、**本节点可用存储**、邻居信息。动作空间 ≤4（L103）。
- **奖励（式 8，L108）**：$a_t$ 是目的节点 → $+D_{avg}|V|$；无转发路径 → $-D_{avg}|V|$；否则 → $-D^{v_0,a_t}_i(t)$。第二项与第一项**等幅反号**，作者说是为了"防止数据包在 agent 之间循环"（L111）。
- **DIRL 离线训练（§IV.B）**：Dijkstra 作为 teacher，agent 作为 student。关键改动是把 ε-greedy 里的"最优动作"替换成 **Dijkstra 给出的动作**：ε 概率随机、1−ε 概率用 Dijkstra（式 9，L124）。作者明确与"监督式 RL"划界（L119 逐字）："instead of using historical data to pretrain the agents, DIRL uses the Dijkstra function as a target strategy and the agents learn on **future real data**"——避免历史数据难收集与过拟合。
- **Two-Hop Convergence（§IV.C）**：用 DDQN（主网 + 目标网，L131）；**目标值改为两跳**：若两跳内可达目的则 $y_j = r_j + r_{j+1} + Q'(s_{j+2},a_{j+2},\theta')$；若一跳就到目的则 $y_j = r_j + Q'(s_{j+1},a_{j+1},\theta')$；若当前已是目的则 $y_j = r_j$（Algorithm 1，L157/L159/L162）。目标网**软更新** $\theta' \leftarrow l_r\theta + (1-l_r)\theta'$，$l_r=0.5$（L168、Table I）。

**4. 它声称的效果**
- **收敛速度**：带 Dijkstra 辅助的 SDDRL-SR **约 400 步收敛**；不带辅助的版本到 **1000 步仍未收敛**，且性能持续改善（L199）。
- **平均时延**：长期运行下 SDDRL-SR 明显优于 DQN 与 random routing；与 Dijkstra **都能满足每条流的端到端时延约束**（L208）——注意这句话的意思是与 Dijkstra 打平，而不是超过。
- **丢包率/到达率**：无链路故障时（Fig 5），稳定运行后 SDDRL-SR 比 Dijkstra 与 DQN 更稳定更高；**random routing 只有 25%**（L218）。有 0.1 概率 ISL 突发故障时（Fig 6），SDDRL-SR 的到达率接近无故障情形，而 DQN 与 Dijkstra 下降更明显（L218）。
- 基线三个：DQN（L193，只用 $r_t+Q(s_t,a_t)$ 不做两跳预测）、Dijkstra（L195）、random routing（L197）。
- **全文正文无任何数值结果**（时延、到达率的具体数字都不给），只有 Fig 3–6 的曲线；唯一给的数字是 random routing 的 25% 到达率与 400/1000 收敛步数。

**5. 实验条件**
- 工具：Python + PyTorch + Gym（L175）。
- 拓扑：**7×7 = 49 星**，每星 2 条同轨 + 2 条异轨 ISL（L183）——与 53HEEK33 完全相同的规模。
- Table I（L206）：ISL 链路容量 $C_{max}$ = **1 Gbps**；每星存储 $S_{max}$ = **15 GB**；**每个请求 100 MB**；因此单星同时最多处理 **10 个请求**、最多存 **150 个请求**（L183）；**链路故障概率 0.1**；每 episode 事件数 I = **3000**；episode 数 M = **1000**；DDQN 学习率 η = 0.005；mini-batch K = 16；隐层 3 层；ε = 0.8 并随训练轮数递减；软更新因子 $l_r$ = 0.5。
- **负载口径**："Number of events in an episode (I) = 3000"——即每 episode 固定注入 3000 个请求，**是一个固定总量，不是到达率，也没有扫多个负载点**（L206、L175）。
- **数据来源自述**："Due to the scarcity of authentic satellite communication datasets, **synthetic data** representative of user requests is generated for experimental purposes"（L175）。
- 训练与评估：同一仿真环境；Fig 3 是训练期，Fig 4–6 是"runtime"长期运行；未见跨分布测试。

**6. 它自己承认的局限**
**没有独立的 Limitations 章节**（全文通读：§I–§VI + Acknowledgment + References，无局限小节）。可引用的自述三处：
- 数据，L175 逐字："Due to the scarcity of authentic satellite communication datasets, synthetic data representative of user requests is generated for experimental purposes."
- 未来工作只有一句，L226 逐字："In future work, we expect to improve the way agents collaborate with each other to achieve better satellite routing results."
- 隐含承认：L208 说 SDDRL-SR 与 Dijkstra **都能满足时延约束**——即在这条最关键的指标上并没有拉开与经典算法的差距，论文没有对此展开讨论。

**7. 它没做但看起来能做的地方（基于内容）**
1. **式 (11) 与式 (12) 的写法与 Algorithm 1 相互矛盾**（L211 vs L215 vs L157/L159）。正文 L208 说"SDDRL-SR 按 (11) 更新、DQN 按 (12) 更新"，但印出来的 (11) 是 $r_t + r_{t+1} + Q'(s_{i+1},a_{i+1},\theta')$（两跳奖励配一跳状态），(12) 是 $r_t + Q'(s_{i+2},a_{i+2},\theta')$（一跳奖励配两跳状态）；而 Algorithm 1 的正确形式是两跳时 $r_j+r_{j+1}+Q'(s_{j+2})$、一跳时 $r_j+Q'(s_{j+1})$。**两处公式至少有一处印错**，且 DQN 的定义（L193 说它只用 $r_t+Q(s_t,a_t)$）与 (12) 也对不上。
2. **两跳只写死了 2**，没有论证为什么不是 3 跳或 k 跳，也没有做 n-hop 的消融对比（L133）。这是全文卖点，却零敏感性分析。
3. **Dijkstra 老师用的是什么权重？** L195 只说基线 Dijkstra 用 "least-weight path"，但 DIRL 里 Dijkstra 在**训练期**给的"最优动作"是否用了真实的队列/存储状态（也即 Dijkstra 在有排队时延的图上是否真最优）完全没有说明（L115）。这直接决定蒸馏出来的策略上界。
4. **奖励 (8) 中 ±$D_{avg}|V|$ 这一对等幅反号的大奖励没有消融**：作者说防止包循环，但没测去掉它会怎样，也没说明 $D_{avg}$ 是否在训练中随策略变化而漂移（L108–L111）。
5. **排队时延模型 (6) 用的是当前存储占用除以链路容量**（L73），而不是到达率——这意味着**负载强度只能通过"存了多少包"间接进入模型**，模型里没有到达过程。
6. **与 53HEEK33 的对照实验缺失**：两篇同一作者组、同一 49 星拓扑，53HEEK33 用周期性 hello 广播换收敛，本篇用 Dijkstra 蒸馏 + 两跳换收敛，但本篇未把 53HEEK33 列为基线（References L234–L252 中无此文）。

**8. 和同批其他篇的关系**
- **与 53HEEK33（同批，同一作者组 Ding/Liu/Tian/Yang）**：这是**同一个课题的第二篇**。共同点：49 星 7×7、链路故障、队列长度进入奖励、都批评"信息串行传播导致收敛慢"。差异：53HEEK33 靠**控制面**（周期性 hello 广播整张 Q 表，t 与流量密度成反比）加速感知；本篇靠**算法面**（Dijkstra 蒸馏 + 两跳目标）。53HEEK33 是表格 Q-learning（因为动作只有 4 个），本篇明确上 DDQN + 3 隐层。**两篇的"加速收敛"是同一个问题的两种解法，且互不引用**。
- 相关工作里点名了同一条线的代表：DRL-THSA（[8]，两跳状态感知 DRL）、DQN-IR（[9]）、DRL-ER（[10]）；本篇自认 (1) 首创用传统算法引导 RL 训练，(2) 首创两跳进入 Q 更新（L17）。**但 [8] DRL-THSA 标题里就有 "Two-Hops State-Aware"**——两条"两跳"主张的关系（是状态两跳还是更新两跳）论文没有辨析。
- 与 **57EB6US5**：本篇的 DDQN、目标网软更新（$l_r=0.5$）、经验回放都直接继承自 DQN 一脉，但没有引用 Mnih 等原文。
- 与 **5HJ8ATR7 / 5AZHJE7N**：无关（一个是接入网多租户，一个是仿真器综述）。

**9. 对"负载变化下到达率/时延"的贡献**
**有边际贡献，但只贡献了"故障"这一维，没有贡献"负载"这一维。**
1. **明确把"到达率"写进目标**：摘要与 §IV.A 两次说目标是"minimize the routing delay ... while ensuring the packet arrival rate"（L7、L111），Fig 5/6 的纵轴就是 packet arrival ratio——这是本批目前唯一**把到达率当作被优化指标并画成曲线**的论文。
2. **但它没有把负载当自变量**：负载固定在"每 episode 3000 个事件"（Table I，L206），Fig 5/6 的横轴是运行时间而非负载强度。所以它给出的是"**到达率随时间**"的曲线，不是"**到达率随负载**"的曲线。
3. **有一处真实的负载-时延耦合机制**：式 (6) 的排队时延 $\lceil \sum\beta/C_{max}\rceil - 1$ 直接由**节点已存储的包数**决定（L73），加上式 (3) 的存储上限 $S_{max}$，构成"负载 → 排队时延 → 拒收"的链条。这是可用的建模组件。
4. **容量与负载的绝对标定是明确的**：1 Gbps ISL / 15 GB 存储 / 100 MB 请求 → 单星同时 10 个请求、最多存 150 个（L183）。**这是本批少见的、把"负载"折算成具体包数与字节数的标定**，可以直接复用做负载扫描的边界设定。
5. **最接近选题的一条**：L218 的链路故障实验（概率 0.1）显示 SDDRL-SR 到达率几乎不降而 DQN/Dijkstra 明显下降——这说明**"扰动下的鲁棒性"是它唯一测过的抗扰维度**；把"故障扰动"换成"负载扰动"（到达率阶跃/斜坡）在方法上几乎不需要改动，但论文没做。

**10. 一句话评价**
**把"用传统算法当老师"（Dijkstra 蒸馏）和"把 TD 目标拉长到两跳"这两个现成技巧缝到 LEO 路由 DRL 上的工程改进**；相对同作者前作 53HEEK33 是从控制面转向算法面的一次尝试，但它把卖点（两跳）只固定为 2、把负载只固定为 3000、把结果只画成曲线，**恰好把"负载变化下的到达率/时延"这一维完整地留空**。

<!-- END-CARDS-R2 -->




