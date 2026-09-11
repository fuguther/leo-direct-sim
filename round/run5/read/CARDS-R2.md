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

## 5PYWVRC5 — Shaping Rewards, Shaping Routes: On Multi-Agent Deep Q-Networks for Routing in Satellite Constellation Networks

**1. 一句话**
用 12 星 / 24 星两个小簇做对照实验，**证伪式地**说明：全分布多智能体 DQN（FD-MADRL）的局部奖励设计会导致"最后几跳做出次优决策、把链路打饱和"，且规模一大训练就不稳；因此提出一个还没实现的混合方案 CL-DC（集中学习、分散控制）。

**2. 问题设定**
LEO 星座的流量需求**非均匀分布**（L17 逐字："traffic requirements are non-uniformly distributed. As the constellation moves relative to Earth, **hot spots are geographical rather than topological**"），且星上处理能力受限（L17）。FD-MADRL 的卖点是"变化和中断可以本地快速处理"，但代价是每个 agent 只有局部视野，**端到端一致性与稳定性存疑**，而且 agent 还得学着去预测其他 agent 的行为（L27 逐字："The end-to-end coherence and stability becomes questionable, the agents have to learn the behavior of other agents as well"）。全文核心问题：**在什么条件下 FD-MADRL 会失效，以及奖励该怎么设计**。

**3. 方法骨架**
（这是一篇短文/扩展摘要，无新算法，主要是奖励设计 + 对照实验）
- **FD-MADRL 的状态/动作**（L29）：状态 = 相邻链路负载 + 上一跳 + 目的地；动作 = 可用的 ISL（下一跳）。每星 4 条 ISL（L17）。
- **集中式复合奖励**（式 2，L39）：$r^G_{t+T} = w_1 U(t) - w_2 L(t) - w_3 D(t)$——链路利用率、流级时延、丢包率；**注意它带一个延迟 $T$**，因为多跳传播导致全局奖励到得很晚（L33 逐字："this reward is only received after a significant time lag, denoted by T, due to the multi-hop propagation delays"）。
- **局部奖励**（式 3，L45）：$r^L_{t+1} = w_4\delta^L_{th}(t) - w_5 l^L(t) - w_4 d^L(t)$——局部链路阈值、局部时延、饱和链路导致的丢包。**注意式 (3) 里第一项与第三项都用了 $w_4$，而正文说权重是 $w_4,w_5,w_6$（L42）——印误。**
- **本文实际采用的 FD-MADRL 奖励**（式 4，L53）：因为全分布设计通常不考虑复合奖励（L48 逐字："For fully decentralized designs, composite rewards are typically not considered"），作者改用**路径压缩量 ψ**（到目的地的距离减少，沿用 [4]）：到达目标 +Ψ；路径缩短 +ψ；路径变长 −ψ；路径没缩短且有环 −Ψ（|Ψ| ≫ |ψ|）；**再加三档链路负载阈值奖励**：负载 < 0.4 → +ξ₁；0.4 < 负载 ≤ 0.8 → −ξ₂；负载 > 0.8 → −ξ₃；链路饱和 → −Ξ（Ξ 与 Ψ 同量级）。
- 关键调参原则（L48、L50）：惩罚必须比奖励**大至少一个数量级**；"+Ψ 也给"能改善训练表现，**即使它没有沿路径回传给所有节点**（L48 逐字："Including a similarly large reward, so +Ψ, for a successful path improved training performance - even though it was not propagated to all nodes along the path"）。
- 提出的未来架构 **CL-DC**（Fig 5，L90–L92）：actor 在本地决策、critic 网络提供集中指导；作者认为 Q 函数在训练与执行时需要同样信息，因此建议转向 policy gradient / actor-critic。

**4. 它声称的效果**（这是一篇**负面结果为主**的论文）
- **规模效应**：24 星簇比 12 星簇需要**两倍以上**的 episode 才能稳定达到最大奖励（L66 逐字："more than twice as many episodes are required to achieve maximum rewards consistently"）。
- **局部视野的代价（具体反例）**：在 24 星簇里从节点 4 到节点 23，学出来的策略是**先往节点 8 走**（因为那条相邻链路负载更低），但这会导致路径经过节点 22，再走几乎饱和的链路到 23（L66 原文给出这个完整例子）。作者结论："the limited scope of individual nodes can result in costly end-to-end decisions."
- **与规则基线的对比（Fig 3，L74）**：作者自述 FD-MADRL **跳数更少**（"for most routes FD-MADRL requires fewer hops"），**但倾向于把链路打饱和**（"However, the approach tends to saturate links"）。基线是动态多代价 Dijkstra（SPF，主动避开负载 > 80% 的链路，L74）。
- **动态负载下的不稳定**（§2.2.2，L78–L83）：把每个上 episode 用过的链路加 **20% 额外负载**（episode 内特有，避免全饱和）。结果：奖励比静态情形更低更不稳；**12 星簇仍能高性能，24 星簇结果不稳定**（L83 逐字："While a high performance can be achieved for the 12-node cluster nonetheless, the results are unstable for the 24-node cluster"）。原因归纳为：更多场景会导致选到饱和链路，或无意中引入环路；**主动规避潜在瓶颈对全分布 agent 很难**（L83）。
- **总判定**（L94）："the investigated FD-MADRL approaches face scaling challenges, particularly in mastering complex scenarios **where they are expected to surpass state-of-the-art methods**"。
- **本文无任何具体数值**（时延 ms、利用率 %、丢包率），全部结论只由 Fig 2/3/4 的曲线支撑。

**5. 实验条件**
- 环境：自建 gym 环境（L60）；DQN 用 Keras/TensorFlow 实现（L60）。
- 拓扑：**12 星簇与 24 星簇**两个规模，作者明确说这是**星座的一个子网**（"a sub-network of an SCN, e.g. a cluster in a distributed architecture"，L60）——**不是完整星座**。
- 负载设置："While the loads are set randomly, they comply with observed link characteristics of plausible non-uniformly distributed traffic scenarios [6]"（L60）——**随机但有现实依据的链路负载**。
- 评价指标：以**逐跳时延（即跳数）**与**路径上的最大链路负载**为主（L60 逐字："we focus on the latency on a per-hop basis, i.e. the hop count, as well as the link loads"）。
- **动态负载机制**（L78）：每个上 episode 使用过的链路额外 +20% 负载，且仅在该 episode 生效。
- 作者明确声明范围限制（L60 逐字）："Due to the limited scope of this manuscript, **only the described reward design is investigated**."
- 训练/评估：同一环境；未做跨分布测试；未报告训练步数与 wall-clock。

**6. 它自己承认的局限**
**没有独立的 Limitations 章节**，但**自述局限异常充分**（这是本文最有价值的部分）：
- 范围，L60 逐字："Due to the limited scope of this manuscript, only the described reward design is investigated."
- 局部视野的固有问题，L87 逐字："For FD-MADRL, we have shown that **the limited scope of each agent negatively impacts the end-to-end routes, in both static and dynamic scenarios**. Moreover, with increasingly complex policies, the agents have to learn the behavior of other agents, **which is counterproductive for scalability**."
- 集中式的代价，L87 逐字："A CDRL-based scheme on the other hand, **loses the flexibility of decentralization, introduces a single point of failure, and needs additional signalling**."
- FD-MADRL 主动避障能力不足，L83 逐字："**learning to proactively avoid potential bottlenecks is difficult with fully decentralized agents**."
- 结论性自评，L94 逐字："while DQN-based architectures represent promising solutions..., they still have **practical limitations**... In-depth investigations are required to fully evaluate their actual viability."

**7. 它没做但看起来能做的地方（基于内容）**
1. **式 (3) 的权重印成 $w_4, w_5, w_4$，与正文的 $w_4,w_5,w_6$ 不一致**（L42 vs L45）——不是大问题，但说明这篇短文还没打磨完。
2. **CL-DC 只画在图里、没有任何实现或实验**（Fig 5，L90）：作者自己说"future research may consider"，这是全文最大的空白。
3. **三档负载阈值（0.4 / 0.8 / 饱和）是硬编码的**（L53），没有做阈值敏感性分析，也没有说明这两个阈值怎么来的。
4. **动态负载实验只做了 +20% 一种幅度**（L78）：没有扫 10%/30%/50%，也没有做负载的时间变化模式（阶跃、斜坡、正弦）——**这正是本选题最接近的空口**。
5. **指标只有跳数与最大链路负载**，没有端到端时延（ms）、没有到达率/丢包率曲线、没有吞吐——而它在式 (2)/(3) 里明明定义了 L(t) 和 D(t)。
6. **24 星就已经不稳，但没有给出规模-稳定性的定量边界**（多少星开始崩、崩在什么指标上），只有 Fig 2/4 的定性描述。
7. **奖励量级 ψ/ξ/Ψ/Ξ 全部是定性描述**（"in the domain of"、"at least a magnitude higher"，L48–L50），没有给出实际数值，也没有做权重扫描。

**8. 和同批其他篇的关系**
- **与 57EB6US5（DQN 原论文）**：直接继承，引用 Sutton & Barto [7] 与经验回放（L27），是 DQN 在星座路由上的应用与**压力测试**。
- **与 53HEEK33 / 5N5LQPPP（Ding 组两篇）**：**结论方向相反**。Ding 组两篇都声称分布式 DRL 路由优于 Dijkstra；本篇声称 FD-MADRL 相对规则基线"跳数更少但会把链路打饱和"且规模一大就不稳，并明确说"这些方法被期待超越 SOTA，但实际面临扩展挑战"（L94）。**本篇是这批里少见的对 DRL 路由持负面结论的论文**，与 5AZHJE7N 综述中"AI 方法无可比基准"的自述（其 L450）互相印证。
- 被引的直接前作 **[6] Roth, Brandt, Bischl（2022）** 与 **[4] Soret et al.（arXiv 2306.01346）** 是同一条线的：前者是"分布式 SDN 负载均衡路由"（本篇的规则基线与场景来源），后者提供了 ψ（路径压缩量）这一奖励形式。
- 与本批 5HJ8ATR7 / 5AZHJE7N：无关。

**9. 对"负载变化下到达率/时延"的贡献**
**这是本批至今对"负载变化"这一维处理得最直接的论文**，共四条可用事实：
1. **明确把"负载作为状态、且负载是自反馈的"**：§2.2.2 让上 episode 用过的链路 +20% 负载（L78），即"路由决策会改变未来的负载"（L78 逐字："routing decisions impact future states and link loads change dynamically"）。这是本批唯一一个把"决策→负载→下一轮决策"闭环建进仿真里的设计。
2. **给出了负载-规模的联合失败边界**：动态负载下 12 星仍稳、24 星不稳（L83）。虽然没给数值曲线，但**指出了失败随规模与负载复杂度共同发生**。
3. **给出了一个具体的"负载规避失败"机制**：agent 为了选低负载链路而绕路，结果走到下游的饱和链路上（节点 4→8→22→23 的例子，L66）。**这是"逐跳贪心看负载"在端到端上的反例**，对任何用局部负载信息做路由的方案都是直接警告。
4. **区分了负载的三个档位并给了阈值语义**：<0.4 奖励、0.4–0.8 惩罚、>0.8 重罚、饱和最重罚（式 4，L53）——这是一份可复用的"负载分级"设计。
5. **受限之处**：全文**没有到达率这个自变量**，也没有端到端时延/丢包曲线；负载只以"链路利用率"形式出现，且只有静态随机分布与 +20% 动态两种设置。**它证明了"负载变化会让 FD-MADRL 不稳"，但没有量化"负载变化幅度 → 时延/到达率退化多少"。**

**10. 一句话评价**
**一篇用极小规模对照实验对 FD-MADRL 做负面评估的短论文**——它的价值不在提出方法（CL-DC 只是一张图），而在于用可复现的反例把"局部奖励 + 逐跳负载规避"的两个失效模式钉死了，是本批里唯一敢说"DRL 路由还没证明能超越规则基线"的一篇。

## 67CSKFK4 — Delay is Not an Option: Low Latency Routing in Space

**1. 一句话**
用 SpaceX 向 FCC 提交的公开轨道参数搭了一个 Starlink 仿真器，论证**五条激光链路是构建低时延 LEO 骨干的最小必需数**，并给出「卫星路径在 >3000 km 距离上能打败任何地面光纤」的初步结论；**全文的关键价值在于它把「负载相关路由」明确列为未解问题**。

**2. 问题设定**
光纤里的光速比真空慢约 47%（L13 逐字："free-space lasers communicate at c, the speed of light in a vacuum, which is ≈ 47% higher than in glass"）。一旦拥塞控制与 bufferbloat 被解决，广域流量的剩余瓶颈就是「光在玻璃里不够快」（L11 逐字："once traffic engineering has mitigated congestion and buffer bloat has been addressed, for wide-area traffic the remaining problem is that the speed of light in glass simply isn't fast enough"）。问题：**在这种新拓扑上该怎么建网、怎么路由，能得到什么时延特性**。作者强调 FCC 文件只讲了 RF 与频谱，**没有讲任何星间通信细节**（L13）。

**3. 方法骨架**
- **自建仿真器**（L7、L15），基于 FCC 文件公开参数；未知参数「从第一性原理取合理值」（L15 逐字："Where details are not publicly available, we adopt reasonable parameters from first principles"）。
- **轨道配置推导（§2）**：Phase 1 = 1,600 星、32 个轨道面 × 50 星/面、高度 1,150 km、倾角 53°（Table，L31）。**相位偏移（phase offset）是全文第一个原创参数**：0–1 之间的 1/32 倍数，偶倍数会碰撞（L37），在奇数倍数中仿真最小星间距后得出 **5/32** 最优（L37）。Phase 2 再加 1,600 星（53.8° 倾角，低 40 km），最优相位偏移 **17/32**（L41）。最终 4,425 星（L43）。
- **可达性假设**：卫星「可达」的定义是地面看过去**距天顶 40° 以内**（L21）。伦敦上空约 30 颗星在这个范围内（L39）。
- **激光链路数量推导（核心贡献）**：从 FCC 里提到的 5 个碳化硅「通信组件」反推每星 5 条激光（L23），并论证 **5 条是构建低时延密集 LEO 网络的实际上限/最小值**（L23、L47）。分配方案（§3、Fig 4）：2 条给同轨前后（只需微调指向，uptime 最高），2 条给相邻轨道面（p→p±1 的**同序号**星，提供近乎东西向连接），第 5 条给**交叉轨道面的 NE-bound 与 SE-bound 两类星之间**的互联（快速追踪、频繁重建）。
- **路由（§4）**：**Dijkstra**，边权 = 链路时延。两个变体：(a) 只把卫星间激光链入图，地面对接「正上方」的星；(b) **RF 上下行链路与激光链路一起入图共同路由**（L95），此时通常选中距天顶接近 40° 的星，代价是 RF 信号低 3 dB、可能降低码率（L93）。
- **预测性路由**：每 10 ms 跑一次 Dijkstra 对笔记本 CPU 毫无压力（L78）；更关键的是「所有链路变化完全可预测」（L78 逐字："all the link changes are completely predictable"），因此**每 50 ms 跑一次「200 ms 后」的网络拓扑并缓存**，源端就能判断发出的包会不会走到那时已经断掉的链路上，从而实现源路由（L78）。
- **多路径**：迭代式 Dijkstra + 删除已用链路，取前 20 条不相交路径；假设激光与 RF 同容量（作者承认现实不会如此，故结果是**路径时延的上界**，L126）。

**4. 它声称的效果**
- **主结论**：距离 > 约 3,000 km 时，这样建的网能提供**比任何可能的地面光纤网络更低的时延**（L7）。
- **NYC–London RTT（Fig 7，L89）**：光纤大圆下界 55 ms，实际互联网 RTT 76 ms；卫星平均 RTT 明显低于两者。**但在 70–95 秒之间出现一个大的时延尖峰**（L89 逐字："the large delay spike between 70 and 95 seconds is certainly undesirable"）。
- **尖峰根因（自己诊断）**：两端城市正上方的星分别落在 NE-bound 与 SE-bound 两个子网里，第 5 条激光虽然连通两个子网，但**路径不够直接、且链路保持时间短**（L91）。
- **RF+激光联合路由（Fig 8，L105）**：NYC–London、SF–London、London–Singapore 三对城市「在所有情况下卫星 RTT 都显著低于光纤大圆下界」。
- **南北向是弱项**：London–Johannesburg 卫星路径约为最佳互联网路径 182 ms 的**近一半**，但「远非最优，因为它必须经由 SW 与 SE 链路之字形绕行」（L109）。加入 Phase 2 后改善约 **20%**（L122）。次优路径（紫色曲线）说明**时延不依赖任何单颗星或单条链路**（L122）。
- **多路径（Fig 11，L128）**：前 20 条不相交路径中**有 5 条低于光纤大圆下界，全部 20 条都低于当前互联网路径**；但**路径越差时延抖动越大**（第 20 条远比第 1 条抖）。第 20 条的 10% 抖动不足以触发 TCP 超时，但**时延快速下降会引起重排序，让 TCP 误判丢包并触发快速重传**（L128）。
- 重排序方案（§5，L134–L144）：接收端重排缓冲，把低时延路径上的包压到与高时延路径一致——这样做后**第 20 好的路径 RTT 仍约 74 ms，低于当前互联网 RTT**（L134）。更进一步的方案是发送端打序号 + 路径 ID + t_last 时间戳。

**5. 实验条件**
- 星座：Starlink Phase 1（1,600 星）+ Phase 2（再 1,600 星）→ 共 4,425 星（L19、L31、L43）。**只研究 LEO 部分，不含 7,518 颗 VLEO（340 km）**（L19 逐字："In this paper, we examine only the LEO constellation"）。
- 每星 5 条激光（L23）；地面可达角 40°（L21）。
- 路由算法：Dijkstra，每 10 ms 可跑一次全网；预测性路由每 50 ms 跑一次 200 ms 后的拓扑（L78）。
- 对比基线：光纤沿大圆的 RTT 下界（55 ms，NYC–LON）、当前互联网实测 RTT（76 ms，L89）；London–Johannesburg 用 182 ms（L109）。
- **明确声明不建模容量**（L25 逐字："in this paper we will refrain from modelling network capacity, as this is too speculative, and focus instead on latency, which is constrained only by topology and the speed of light"）。
- **所有仿真假设卫星内部没有明显排队**（L150 逐字："All the simulations above assume that no significant queuing happens in the satellites themselves"）。
- 作者提到配有仿真视频（[8]，L172）。

**6. 它自己承认的局限**
**没有独立的 Limitations 章节**，但自述限制非常明确：
- 不建模容量，L25（逐字见上）。
- 不建模排队，L150（逐字见上）。
- 多路径结果的乐观性，L126 逐字："This implicitly assumes that laser links and RF links have the same capacity - this is unlikely in reality; whichever turns out to be the bottleneck, a real network will allow more paths than this, so the figure effectively shows an **upper bound** on path latency."
- 南北向路由不佳，L109（逐字见第 4 项）。
- 第 5 条链路（跨子网）保持时间短，L91。
- 重排序的处置方案仍是设想，L142–L144 用 Suppose、we would hope 等假设语气。

**7. 它没做但看起来能做的地方（基于内容）**
1. **§5 Load-Dependent Routing 是全文自己点出的最大空白，且是逐字可引的**（L150–L154）："All the simulations above assume that no significant queuing happens in the satellites themselves." 作者进一步指出：高优先级流量可靠准入控制保证，**但普通互联网流量得不到这种待遇**，因此 LEO 运营商需要主动流量工程来避免热点；还引 [6] 指出「网状网络上的最短路径路由特别容易制造热点」（L150）。
2. **它自己给出了一个具体且未被验证的混合方案假设**（L154）：高优先级低时延流量走显式路由 + 准入控制；其余流量由卫星监测链路负载并**全球广播**给所有地面站，地面站**在略差的路径间随机化**以把流量从热点引开。作者还论证为什么 LEO 与传统拓扑不同、**不容易出现「在最优与次优路径间反复横跳」的不稳定**：因为密集 LEO 有极多时延相近的路径，地面站可以用比负载广播时延**长得多**的时间尺度慢回切（L154）。——这是一条完整的、可实验的假设，作者说 "We believe this is an interesting direction for future routing work"。
3. **地面集中式负载相关路由（B4[9]、LDR[7]）被作者判定为「太慢」**：它们按分钟级做决策，对密集 LEO 星座不够快；能否扩展或控制器-地面站时延是否永远太高，作者明确称为 open question（L152）。
4. **时延尖峰（Fig 7 的 70–95 s）只被解释、未被解决**（L89–L91）：根因是两端落在不同子网，但作者没有给出避免方案。
5. **失败场景只讨论了 5 个收发器坏 1 个**（L146），没有做「链路批量失效」或「热点区域星群拥塞」的情形。
6. **重排序与 TCP 的交互只是定性推断**（L128），没有任何仿真或传输层实验。

**8. 和同批其他篇的关系**
- **与 5HJ8ATR7**：5HJ8ATR7 的 Related Work 明确引用了本篇（其 [100] 即 "Handley, Mark. Delay is Not an Option: Low Latency Routing in Space"），并把 "network-layer routing [98–100]" 划归他人工作。**本篇是 5HJ8ATR7 的上游引用**。
- **与 53HEEK33 / 5N5LQPPP**：方式相反。Ding 组两篇用 RL 取代 Dijkstra 以求「适应动态」；本篇全用 Dijkstra，并论证**因为拓扑变化完全可预测，预测性 Dijkstra 就够了**（L78）。**这是本批里对「是否需要用 RL 做 LEO 路由」最直接的一种反问姿态**——虽然本篇从未提及 RL。
- **与 5PYWVRC5**：两者结论方向一致且互补。5PYWVRC5 用实验证明 FD-MADRL 会「为了低负载绕路而最终打饱和下游链路」，本篇 L150 引用 [6]（Gvozdiev 等，Handley 也是作者之一）指出「网状网最短路径路由特别容易制造热点」——**同一个失效模式的两种证据**。
- **与 57EB6US5**：无关（本篇不涉及 RL）。
- 与本批 5AZHJE7N：无关（本篇是算法/拓扑论文，不是仿真器综述）。

**9. 对「负载变化下到达率/时延」的贡献**
**这是本批至今唯一一篇把「负载变化下的路由」当作核心 open problem 明确写出来的论文**，即使它自己没做实验：
1. **明确的负向声明**：全文所有仿真**假设卫星内无排队**（L150），所以本篇给出的所有时延数字都是**无负载的纯传播时延下界**，与负载无关。
2. **明确的任务定义**："the network must be capable of routing with low delay, **even when traffic levels are high enough to saturate the best paths**"（L132）——这是对选题最直接的一句话需求陈述。
3. **失败机制的先验陈述**：网状网上的最短路径路由**特别容易制造热点**（引 [6]，L150）；且**热点在 LEO 里是地理的而不是拓扑的**（L154 逐字："these hotspots tend to be geographic rather than topological"）——与 5PYWVRC5 的 L17 表述完全一致（同一研究传统）。
4. **给出了一个可检验的稳定性论证**：密集 LEO 有极多时延相近路径，因此可以用**远长于负载广播时延的时间尺度**慢速回切，从而避免传统拓扑中「最优/次优反复横跳」的不稳定（L154）。**这是本批中唯一一条关于「负载相关路由为何在 LEO 中可能比在地面更稳定」的正面论证。**
5. **给出了负载相关方案的时标约束**：B4/LDR 的分钟级决策对密集 LEO 太慢（L152）——为「负载变化必须多快响应」提供了一个下界参照（需要远快于分钟级）。
6. **给出了可用的路径多样性事实**：NYC–LON 有 20 条不相交路径、其中 5 条优于光纤下界（L128）；50°N 附近单点可见约 60 颗星（L124）。**路径冗余是负载均衡的物质基础**，这个数量级是可复用的。

**10. 一句话评价**
**LEO 低时延路由的开山之作**——它自己只做了「无负载、无排队」的 Dijkstra 时延分析，但它把后面十年这批论文要做的事（负载相关路由、热点、稳定性、准入控制、多路径）**在一节 Research Agenda 里全部点名了**，是整批语料的时间与问题源头。

## 6C843JTS — Learning to Predict by the Methods of Temporal Differences

**1. 一句话**
提出并第一次从数学上证明 TD(λ) 这一族"用**相邻两次预测之差**而不是"预测与最终结果之差"来分配信用"的增量式预测学习方法——证明了线性 TD(0) 的渐近收敛性（定理 2）、以及在重复呈现训练集时收敛到**最大似然最优预测**（定理 3），并证明线性 TD(1) 与 Widrow-Hoff 监督学习产生完全相同的权重更新（定理 1）。

**2. 问题设定**
"学习预测"= 用与一个**不完全已知系统**的过往经验预测其未来行为（L15、L19）。传统做法是把预测问题硬塞进监督学习框架：把每个观测和**最终结果**配成对 $(x_t, z)$（L39、L65）。作者认为这**忽略了序列的时间结构**（L39 逐字："Although this pairwise approach ignores the sequential structure of the problem"），并主张：**大多数被当作单步预测的问题，本质上都是多步预测问题**（L47）。多步预测的定义（L43）：预测的正确性**不在预测时立即揭晓，而是在其后的多步中逐步透露部分信息**。天气、选举、棋局、棒球击球手判断好坏球都是多步问题的例子（L21、L45）。

**3. 方法骨架**
- **形式化（§2.2）**：经验以"观测-结果序列" $x_1,x_2,\dots,x_m,z$ 给出，每个 $x_t$ 是实值特征向量，$z$ 是实值标量结果；学习器产生预测序列 $P_1,\dots,P_m$，每个都是对 $z$ 的估计；这里简化为 $P_t = P(x_t, w)$（L55）。
- **监督学习原型（式 2）**：$\Delta w_t = \alpha(z-P_t)\nabla_w P_t$；线性情形 $P_t = w^Tx_t$ 退化为 **Widrow-Hoff / delta 规则 / LMS**（L75–L81）。**关键缺陷：式 (2) 的所有 $\Delta w_t$ 都依赖 $z$，因此在序列结束前无法计算，不能增量实现**（L85 逐字："(2) cannot be computed incrementally"）。
- **TD 的出发点（核心恒等式）**：把误差写成预测变化之和 $z - P_t = \sum_{k=t}^{m}(P_{k+1}-P_k)$，其中 $P_{m+1} \equiv z$（L90）。代入并交换求和次序后得到 **TD(1)**（式 3）：$\Delta w_t = \alpha(P_{t+1}-P_t)\sum_{k=1}^{t}\nabla_w P_k$——**可以增量计算**，因为每个增量只依赖一对相邻预测与梯度的历史累加和（L102–L105）。**定理 1**：多步预测问题上，线性 TD(1) 与 Widrow-Hoff 产生相同的按序列权重变化（L109）。
- **TD(λ) 族（式 4，L116）**：$\Delta w_t = \alpha(P_{t+1}-P_t)\sum_{k=1}^{t}\lambda^{t-k}\nabla_w P_k$，$0\le\lambda\le1$——对越久远的观测向量，改动按 $\lambda^k$ **指数衰减**（L113）。λ=1 即 TD(1)。
- **可增量实现的关键（eligibility trace 前身）**：$e_{t+1} = \nabla_w P_{t+1} + \lambda e_t$（L124）——这就是后来的资格迹递推。
- **TD(0)**（L130）：$\Delta w_t = \alpha(P_{t+1}-P_t)\nabla_w P_t$，与监督学习式 (2) 形式完全相同，**只是把 $z$ 换成 $P_{t+1}$**（L133）。
- **理论部分（§4）**：假设数据由**吸收马尔可夫过程**生成（L202）。理想预测 $E\{z|i\} = [(I-Q)^{-1}h]_i$（式 5，L215）。**定理 2**（L222）：对任意吸收马氏链、任意起始分布、任意有限期望的结果分布、任意线性无关的观测向量集，存在 $\epsilon>0$，使得对所有 $0<\alpha<\epsilon$ 和任意初始权重，**线性 TD(0) 的预测在期望意义下收敛到理想预测**。**定理 3**（L358）：在线性无关观测向量下，反复呈现训练集且每次呈现后更新，**线性 TD(0) 收敛到最大似然最优预测** $(I-\hat Q)^{-1}\hat h$（式 8）。
- **TD 作为梯度下降（§4.3，L376–L404）**：定义 $J(w)=E_x\{(E\{z|x\}-P(x,w))^2\}$；关键分歧点在于**如何估计 $E\{z|x_t\}$**——用实际的 $z$ 估计 → 监督学习 (2)；用紧随其后的预测 $P(x_{t+1},w)$ 估计 → TD(0)（L404）。作者在此点出全文核心论点："our real goal is for each prediction to match the **expected value** of the subsequent outcome, not the **actual outcome** occurring in the training set"（L404）。
- **推广（§5）**：§5.1 累积结果（预测剩余累积代价，$\Delta w_t = \alpha(c_{t+1}+P_{t+1}-P_t)\sum\lambda^{t-k}\nabla_w P_k$，L419，三个定理"带有显然的修改后"依然成立，L422）；§5.2 序列内权重更新（L438–L449，并指出如果序列内改 $w$，预测变化会同时来自 $w$ 与 $x$，**极端情况下可能导致不稳定**，L446）；§6 与其他研究的关系（含 Adaptive Heuristic Critic，L520–L528）。

**4. 它声称的效果**
- **计算/存储优势**：若 M 是序列最大长度，TD(1) 在很多情形下**只需监督学习 1/M 的内存与速度**（L105 逐字："(3) will require only 1/M th of the memory and speed required by (2)"）。
- **随机游走实验（§3.2，L161–L194）**：5 状态有界随机游走（B–F，从 D 出发，A/G 吸收），真实右端终止概率为 1/6, 1/3, 1/2, 2/3, 5/6（L176）；100 个训练集 × 每集 10 条序列；λ 取 1 / 0 / 0.1 / 0.3 / 0.5 / 0.7 / 0.9（L169）。
- **实验一（重复呈现，Fig 3，L176）**：性能随 λ 从 1 下降而**快速改善，且在 λ=0 时最好**；各点标准误约 σ=0.01，故 TD 与 Widrow-Hoff 的差异"高度显著"（L172）。作者特意指出这**与常识矛盾**：Widrow-Hoff 在训练集上最小化 RMS 误差，却比其他所有 TD 方法都差（L181）——解释是它只最小化**训练集**误差，不一定最小化**未来经验**的误差（L181）。
- **实验二（单次呈现，Fig 4/5，L183–L190）**：所有 λ<1 的方法在绝对表现与 α 的可接受范围上都优于监督学习；但**最佳 λ 不是 0，而是约 0.3**（L190）。原因（L192）：λ=0 沿序列反向传播预测值很慢——举例：D、E、F 初始预测都是 0.5，序列 $x_D,x_E,x_F,1$ 中 TD(0) 只改 F，而其他方法会以递减幅度同时改 E 和 D。
- **反向遍历的替代方案**（L194）：单次呈现时若从序列末尾往前更新可以一步传播到序列开头，但**会丧失增量实现的优势**（"it has no incremental implementation"）。
- **一般性结论（§7，L532）**：TD 方法"计算更便宜、学得更快"；其中一个 TD 方法（TD(1)）与监督学习产生完全相同的预测与学习变化，同时保留计算优势；另一个（TD(0)）虽学习变化不同，但已被证明渐近收敛到同样的正确预测。

**5. 实验条件**
- 唯一的计算实验是**有界随机游走**（bounded random walk）：5 个非终态 B–F，从 D 出发，每步等概率左右移动，进入 A 或 G 即终止（L151、L165）。
- 观测向量是 5 维单位基向量（每个状态一个），因此 $P_t$ 就是 $w$ 的第 i 个分量（L167）——**极简设定，目的是让方法差异最清晰**（L167 逐字："We use this particularly simple case to make this example as clear as possible"）。
- 100 个训练集 × 每集 10 条序列（L169、L172）。
- 实验一：重复呈现直到权重不再显著变化（L174）；实验二：每个训练集只呈现一次，且每条序列后即更新，初始权重全设 0.5（L183）。
- **理论假设**：吸收马尔可夫过程、观测向量线性无关、$\alpha$ 足够小（L202、L220、L222）。
- 作者明确说明游戏例子"太复杂，无法详细分析"（L163），随机游走的目的是把问题压到最简以免混入无关因素（L163）。

**6. 它自己承认的局限**
**没有独立的 Limitations 章节**，但§3.1、§4.2、§5 中有明确的自我限定，逐字引用如下：
- TD 可能失败的反例，L157 逐字："This game-playing example can also be used to show how TD methods can fail. Suppose the bad state is usually followed by defeats except when it is preceded by the novel state... In this odd case, TD methods could not perform better and might perform worse than supervised-learning methods." 并接着说 "it remains a **greater difficulty for TD methods** than it does for supervised-learning methods"。
- 游戏例子不构成证明，L155 逐字："The example does not prove TD methods will be better on balance, but it does demonstrate that a subsequent prediction can easily be a better performance standard than the actual outcome."
- 学习率理论缺口，L374 逐字："That TD(0) converges to a better set of estimates with repeated presentations helps explain how and why it could learn better estimates from a single presentation, **but it does not prove that**. What is still needed is a characterization of the learning rate of TD methods"。
- 最优估计本身不可实现，L354：最大似然最优程序需要 $O(n^2)$ 内存与每步多达 $O(n^3)$ 计算，而监督学习与 TD 方法只要 $O(n)$。
- 推广部分不保证理论适用，L408 逐字："Except where explicitly noted, the theorems presented earlier **do not strictly apply** to these extensions."
- 序列内更新可能导致不稳定，L446（逐字见第 3 项）。
- 理论只覆盖线性 TD(0)：§4 开头明确"The theory developed here concerns the linear TD(0) procedure"（L198），并在 L222 强调只有**线性** TD(0) 被证明。

**7. 它没做但看起来能做的地方（基于内容）**
1. **只有 TD(0) 有权重收敛定理，TD(λ)（0<λ<1）没有**（L198、L222）：而实验里最好的恰恰是 λ≈0.3（L190）——**被实验证明最好的参数，正是理论没覆盖的区间**。这是本文最明显的理论与实验裂缝。
2. **非线性/多层网络的收敛性完全没碰**：作者只在 L31 说 TD 方法"can be directly extended to multi-layer networks (see Section 6.2)"，但第 6 节通读后并未给出任何收敛结果（L29–L31、L530–L540）。
3. **学习率（收敛速度）没有定理**：作者自己承认（L374）。这直接关系到后续所有 DRL 路由论文"收敛慢"的抱怨。
4. **反向遍历方案被承认更优但被放弃**（L194）："when learning is done offline from an existing database, working backward in this way should produce the best predictions"——离线场景下这条建议从未被后续工作系统验证。
5. **λ 的选择没有理论指导**：实验一最优 λ=0、实验二最优 λ≈0.3（L176 vs L190），作者只给出定性解释（TD(0) 反向传播慢，L192），没有给出"该选多大 λ"的判据。
6. **唯一的实验是 5 状态的玩具问题**（L165），所有结论都在这个尺度上得出。

**8. 和同批其他篇的关系**
- **与 57EB6US5（DQN）**：**这是 DQN 的理论上游**。DQN 论文里的 $y = r + \gamma\max_{a'}Q(s',a';\theta^-)$ 就是 TD 目标；DQN 用"独立目标网 + 经验回放"解决的那个"自举导致发散"的问题（其 L17），其根源正是本篇 L198 所说的"most of their learning is done on the basis of previously learned quantities... it can also make them difficult to analyze and to have confidence in"。**本篇只对线性 TD(0) 给出了收敛保证；DQN 用非线性网络把这个保证丢掉了**。
- **与 53HEEK33 / 5N5LQPPP（Ding 组）**：53HEEK33 的式 (2) 是标准 Q-learning 表格更新（其 L84）；5N5LQPPP 的 DDQN 软更新（其 L168）——都是本篇 TD 谱系的下游。53HEEK33 的"空包收敛法"（周期性广播更新整张 Q 表）在概念上**非常接近本篇 §5.2 讨论的"何时更新权重"的问题**，但 53HEEK33 未引用本篇。
- **与 5PYWVRC5**：5PYWVRC5 关于"奖励设计决定成败"（其 §1.3）与本篇 §4.3 的"$J(w)$ 该怎么定义"是同一个问题的两种提法：本篇从理论上说明目标应该是**期望结果**而非**实际结果**，5PYWVRC5 则用实验证明**局部奖励会诱导次优的端到端决策**。
- **与 67CSKFK4 / 5HJ8ATR7 / 5AZHJE7N**：无关。
- 在本批 11 篇里，本篇与 57EB6US5 是**唯二的方法论基础论文**（其余 9 篇是 LEO 领域应用）。

**9. 对"负载变化下到达率/时延"的贡献**
**没有直接贡献**——本篇不涉及网络、不涉及到达率、不涉及排队时延。但有一条**可直接迁移的建模工具**，这在做"负载变化下的时延预测"时是关键：
1. **§5.1 累积结果预测（L410–L428）明确把"包交换电信网中预测一个包的总时延"列为应用场景**（L412 逐字："in a packet-switched telecommunications network one may want to predict the total delay in sending a packet"）。并给出形式：$\Delta w_t = \alpha(c_{t+1}+P_{t+1}-P_t)\sum_{k=1}^{t}\lambda^{t-k}\nabla_w P_k$（L419），其中 $c_{t+1}$ 是第 t 到 t+1 步之间的**实际代价**（可以是时延、可以是排队时长）。**这给了"时延作为累积代价被 TD 学习"一个现成的理论接口**，且作者声明三个定理在此情形下依然成立（L422）。
2. **"预测剩余累积代价"而非"整段总代价"**（L414）——对应到路由里就是**预测"从当前节点到目的地的剩余时延"**，这正是所有 Q-routing 类方法的 Q 值语义。本篇给出了它的理论依据。
3. **一句话的建模警告**（L404）：目标是让预测匹配**期望值**，而不是匹配**训练集中实际发生的那一次**。在负载变化场景下，这句话直接对应"**不能拿单次高负载下的时延样本去拟合，要拟合该负载水平下的期望时延**"——而本批多篇 LEO 论文（如 5N5LQPPP）恰恰是用单次仿真轨迹做奖励。
4. **时序结构被显式利用**：本篇的全部卖点就是"利用序列的时间结构"（L532），而负载变化本身就是一种时间结构——**这为"把负载的时间演化作为 TD 学习对象"提供了方法论许可**，尽管本篇自己从未涉及负载。

**10. 一句话评价**
**RL 的信用分配从"等结果"变成"看下一步"的那一步**——它是本批 11 篇里两篇方法论源头之一，为后来所有 Q-learning/DQN 类 LEO 路由工作提供了更新的合法性（TD(1)≡监督学习）、收敛保证的范围（线性 TD(0)）以及一个至今仍被忽视的警告：**要拟合的是期望，不是那一次实际发生的结果**。

## 6GWNYSTT — LEO laser microwave hybrid inter-satellite routing strategy based on modified Q-routing algorithm

**1. 一句话**
把"同轨激光 + 异轨微波"的混合星间链路与"星上 CPU 资源池"两个新硬件假设写进路由代价模型，**用排队论（M/M/1/∞、M/M/1/N、M/M/c）把星上处理时延算出来**，再用 Dijkstra 引导 Q-routing 找最短时延路径；声称时延比 Dijkstra 低 83.3%。

**2. 问题设定**
LEO 通信网需要巨大负载容量与信息处理速度（L15）。现状是**所有 LEO 星座都没有完整星间链路**，相邻星之间靠地面站中继（L23）。技术约束是：激光链路带宽大、功耗低、轻量（L23），但**异轨卫星之间相对运动巨大，激光对准极难（数千公里距离上要求厘米级误差）**，Starlink 到 2020 年 9 月才宣布**同轨**激光链路测试成功（L23、L130）。因此作者主张的形态是：**同轨用激光、异轨用微波**（L23、L126–L130）。另一半动机是星上算力稀缺："一颗卫星覆盖面积大而负载小，导致计算资源受限"，地面站资源池技术已成熟但**星上资源池还停留在纸面**（L25 逐字："the resource virtualization technology of satellite ground station has been relatively mature, while the on-board resource virtualization technology is still remaining on paper"）。

**3. 方法骨架**
- **拓扑（§3.1）**：有向图 $G(V,E,P)$；**南北纬 70° 以上不存在异轨链路**（L58）。
- **传播时延（§3.2，式 1–3）**：由经纬度算地心夹角 $\xi = \arccos[\sin\varphi_A\sin\varphi_B + \cos\varphi_A\cos\varphi_B\cos(\lambda_A-\lambda_B)]$，星间距离 $d_{AS} = R_A\sqrt{2(1-\cos\xi)}$，传播时延 $T_l = d_{AS}/c$。
- **处理时延（§3.3，核心）**：用三个排队模型建模三段流程（Fig 5）：
  - **接收端**：激光接收机用 $M/M/1/N/\infty$（**有限容量**），微波接收机用 $M/M/1/\infty/\infty$（无限容量）（L139）；
  - **CPU 资源池**：$M/M/c/\infty/\infty$，$c$ = CPU 单元数（本文 5 个）（L112、L132、L141）；
  - **发射端**：$M/M/1/\infty/\infty$（L143）。
  原文给出三段的平均服务时延公式：式 (4) $W_s = 1/(\mu-\lambda)$；式 (5) $W_s = L_s/[\mu(1-P_0)]$，含 $L_s = \rho/(1-\rho) - (N+1)\rho^{N+1}/(1-\rho^{N+1})$；式 (6) $W_s = L_S/\lambda$。**总处理时延 $W_S = W_{S1}+W_{S2}+W_{S3}$**（式 7，L148）。
- **到达过程假设**：每秒包数服从**泊松分布**，因此每条路径上包数仍服从泊松（L137 逐字："Per second packets number obeys Poisson distribution, so that in each path, the packets number still obey Poisson distribution"）；并利用"独立泊松过程之和仍为泊松"得资源池前强度 $\lambda_2 = \sum_{i=1}^{5}\lambda_{1i}$（L141）。
- **路由数学建模（§4.2）**：拓扑切片把连续变化切成 n 个离散静态拓扑（L158）。三条约束：路径传播时延上界 $T_{l_{max}}$（式 8）、路径处理时延上界 $W_{S_{max}}$（式 9）、总时延阈值 $T_{max}$（式 10）。目标式 (11) 最小化 $\sum T_l + \sum W_S$。**注意式 (11) 在 MD 里渲染成了一团乱码**（L183），无法逐字核对。
- **改进型 Q-routing（§4.3）**：Q 值 $Q_{u_i}(u_{N_P}, u_{i+1})$ 表示"从邻居 $u_{i+1}$ 送到目的地 $u_{N_P}$ 的估计代价"（式 12）。迭代式 (13)：$NewQ = (1-\alpha)Q + \alpha(T_l(u_i,u_{i+1}) + W_S(u_i) + \min_{u_{i+2}} Q_{u_{i+1}}(u_{N_P},u_{i+2}))$。**Dijkstra 的角色**：因为传播时延在每个拓扑切片内是常数，Dijkstra 只用传播时延就能给出一个"近似方向"，$O(N^2)$ 且每切片只算一次；Q-routing 则负责把**动态的处理时延**纳入（L206 逐字："the Dijkstra algorithm only take transmission delay into consideration, the reinforcement learning algorithm can use the dynamic processing delay to find the approximate optimal solution"）。
- **复杂度对比（Table 1，L224）**：Dijkstra 全网空间 $O(N^2)$/时间 $O(N^3)$，每节点 $O(N)$/$O(N^2)$；Q-routing 全网 $O(NAH)$/时间 $O(NKH)$，每节点 $O(AH)$/$O(KH)$。

**4. 它声称的效果**
- **主结论（摘要，L15）**：改进算法的时延**比 Dijkstra 低 83.3%**，且"网络越大、流量越大，优势越明显"。
- **收敛**：最短路径收敛约 **20 ms**，"满足 Oneweb 和 Starlink 的预期"（L240）。
- **负载阈值（Fig 8，L242）**——**本节最关键的负载相关结论**：每批 2,000 到 10,000 个包时时延最终收敛到 **20 ms 以下**；**每批超过 10,000 个包时时延升到 20 ms 以上**。所有批次在**网络迭代轮数接近 30 时收敛到最小值**。**"随着负载增加，收敛时延也随之增加"**（逐字："As the load increases, the convergence delay also increases"）。**2,000 包/批是一个阈值**（逐字："The rate of delay convergence is slow at 2000 per batch but fast at 3000, which shows that 2000 is a threshold value"）。
- **改进算法 vs 原版 Q-routing**：任意拓扑规模下改进算法收敛都更快（Fig 9 vs Fig 8，L244）。
- **规模效应（Fig 10，L248）**：$5\times5, 10\times10, 15\times15, 20\times20, 25\times25$ 五档。随着网络变大，包的路由距离变长，但**传播时延反而呈下降趋势**——作者解释为传播时延的增幅跟不上处理时延的降幅；但下降趋势在减弱，"如果再变大，时延会重新上升"（L248）。收敛速度随规模变慢：前两个网络几乎立即收敛，$20\times20$ 与 $25\times25$ 分别在第 10 与第 20 轮收敛。
- **跳数与直觉相反（Fig 11，L259）**：Dijkstra 跳数**最少**，其次 Q-routing，改进算法**最多**；但时延顺序**完全相反**。作者结论："智能算法通过增加跳数换取更低时延，绕开处理时延高的路径"（逐字："the smart algorithm increases the hop number to get a lower delay, the packets bypass the path with high processing delay and achieve a total delay reduction"）。
- **学习率（Fig 12/13，L261–L269）**：大学习率时 20–40 批收敛；学习率越小收敛越慢。**同一网络中，$\alpha$ 越小收敛时延越小**，作者称"大学习率在小网络中会让流量变慢"（L269）。
- **复杂度实算（Table 3，L235）**：Dijkstra 全网 $5.2\times10^5$、每节点 756；Q-routing 全网 $2.0\times10^6$、每节点 2880。

**5. 实验条件**
- 星座：Walker 构型，**轨道高度 1200 km、18 个轨道面、每面 40 星、倾角 87.9°**（Table 2，L229）——即 **720 星**。
- 主实验规模报为 $18\times40$ 网络（L221、L242）；规模扫描用 $5\times5$ 到 $25\times25$（L248）。
- 流量：**共路由 200 万个包**；**每批 20,000 包**（Fig 7）；Fig 8 的批次范围是**每批 2,000 到 10,000+ 包**；起点与终点**随机**（L221）。
- **拓扑切片**：连续变化的拓扑切成 n 个离散静态拓扑，切片内视为常数（L158）；未给出具体的 n 值或切片长度。
- 每星 5 个收发器：2 个激光（同轨）+ 3 个微波（异轨与地面）（L128）；CPU 资源池 5 个 CPU 单元（L132）。
- 对比基线三个：Dijkstra、原版 Q-routing、改进 Q-routing（L219）。
- **数据可用性声明（L293）**："Data sharing is not applicable to this article as no datasets were generated or analyzed during the current study."

**6. 它自己承认的局限**
**没有独立的 Limitations 章节**（全文通读，第 6 节 Results and discussion 只有两段总结）。可引用的自述：
- 星上资源虚拟化仍停留在纸面，L25 逐字："the resource virtualization technology of satellite ground station has been relatively mature, while the on-board resource virtualization technology is still remaining on paper."（即本文所依赖的硬件前提尚未实现）
- 规模-时延非单调，L248：传播时延随规模下降的趋势"is getting smaller, **if the network size increases again, the delay will increase**"。
- 复杂度代价，Table 1/3：Q-routing 的全网空间复杂度 $O(NAH)$ 与实算值**都高于 Dijkstra**（Table 3：$2.0\times10^6$ vs $5.2\times10^5$）——作者没有讨论这个代价。
- 数据无法共享，L293（逐字见上）。

**7. 它没做但看起来能做的地方（基于内容）**
1. **式 (11) 在 MD 中渲染为乱码（L183）**，无法核对目标函数的确切形式；这是 MinerU 解析问题，但意味着**该式的可复现性为零**。
2. **排队模型的参数（$\lambda, \mu, c, N$）从未给出具体数值**（§3.3、§4.1 通读）：式 (4)(5)(6) 里所有符号都只有定义没有取值，$N$（激光接收缓存容量）与 $\mu$（CPU 处理速率）在实验部分完全没出现。**这是全文最大的复现障碍**。
3. **"20,000 包/批"与"2,000–10,000 包/批"两套口径并列出现但从未统一说明**（L221 vs L242）：Fig 7 的批次是 20,000，Fig 8 的批次是 2,000–10,000+，读者无法判断哪个是主实验设置。
4. **拓扑切片数 n 未给出**（L158），而切片粒度直接决定 Dijkstra 预计算的有效性与路由误差。
5. **CPU 资源池的"5 个单元"是硬编码常量**（L132），没有任何 $c$ 的敏感性分析——而 $c$ 恰恰是 $M/M/c$ 模型里最关键的服务台数。
6. **"处理时延随规模下降"这一反直觉结论没有分解验证**（L248）：只说是传播时延增幅跟不上处理时延降幅，但没有分别画出两个分量随规模的变化曲线。
7. **改进算法跳数最多这一事实（L259）没有进一步讨论副作用**：更多的跳数意味着更多的星上处理次数与更多的排队点，在高负载下这个交换是否仍然成立，论文没有测。
8. **未做与 53HEEK33 那类"控制面加速"方案的对比**（见第 8 项）。

**8. 和同批其他篇的关系**
- **与 53HEEK33（Ding 组，Fast-Convergence RL）**：**53HEEK33 把本篇列为参考文献 [27]**（53HEEK33 的 L367 逐字："Zheng, F.; Wang, C.; Zhou, Z. LEO laser microwave hybrid inter-satellite routing strategy based on modified Q-routing algorithm"）。因此本篇是 53HEEK33 的**上游引用**。两者都做 Q-routing + Dijkstra 对比 + 49/720 星规模，但**加速手段不同**：本篇用 Dijkstra 只在拓扑切片时预计算一次传播时延方向；53HEEK33 用周期性 hello 广播在运行中持续刷新整张 Q 表。
- **与 5N5LQPPP（Ding 组，SDDRL-SR）**：**同一个"Dijkstra 引导 RL"思想的两种实现**。5N5LQPPP 的 DIRL 是把 Dijkstra 当 teacher 做蒸馏、把 ε-greedy 里的最优动作换成 Dijkstra 动作（其 L119–L124）；本篇是让 Dijkstra 只算传播时延方向、Q-routing 补处理时延（L206）。**5N5LQPPP 没有引用本篇**，但两条路线几乎撞车。
- **与 67CSKFK4（Handley）**：**恰好是 Handley 所批评的那种"静态最短路"方案的后继**。Handley 在 L150 指出"网状网上的最短路径路由特别容易制造热点"，本篇给出的正是"用处理时延绕行来规避高负载节点"的机制（式 13 里的 $W_S(u_i)$ 项），并在 Fig 11 中用"跳数增多、时延反降"佐证了这一规避确实在发生。**这是本批唯一一篇给出了"负载规避"实证的论文。**
- **与 5PYWVRC5**：5PYWVRC5 用实验证明 FD-MADRL 会为了低负载链路绕路最终打饱和下游；本篇的绕行是**由排队时延驱动**的，不是由链路利用率驱动，因此机制不同但风险同源。
- **与 57EB6US5 / 6C843JTS**：本篇的 Q-routing 迭代（式 13）就是标准 Q-learning 形式；参考文献 [27] 指向 **Boyan & Littman 1993 的 Q-routing 原始论文**（L367），即 6C843JTS 的直接后继工作。
- **与 5AZHJE7N / 5HJ8ATR7**：无关。

**9. 对"负载变化下到达率/时延"的贡献**
**这是本批 11 篇里对"到达率 → 时延"关系处理得最实的一篇**，因为它是唯一一个**把排队论写在路由代价里、并且真的扫了负载**的论文：
1. **到达率是显式建模变量**：$\lambda$ 直接出现在三个排队模型的时延公式里（式 4/5/6，L99–L118），且明确声明到达过程为**泊松**（L137）。这是本批唯一一处把"到达率"写成模型符号而非实验设置的论文。
2. **给出了负载-时延的阈值行为**：每批 ≤10,000 包 → 时延收敛 <20 ms；每批 >10,000 包 → 时延 >20 ms（L242）。**并且明确指出"负载越大，收敛时延越大"**（L242）。
3. **给出了一个具体的负载阈值数**：**2,000 包/批是"收敛快慢"的分界**（L242 逐字："which shows that 2000 is a threshold value"）——虽然这个"阈值"的物理含义（是服务能力饱和还是别的）论文没有解释。
4. **给出了时延对负载的传导机制**：$$W_S = W_{S1}+W_{S2}+W_{S3}$$（式 7）三段串联，且**资源池前的到达强度是五个接收端之和** $\lambda_2=\sum_{i=1}^{5}\lambda_{1i}$（L141）——这是"多路流量汇聚到单一星上算力"的显式拥塞点建模，**对"负载上升时星上处理成为瓶颈"这一假设给出了数学形式**。
5. **给出了一个反直觉但重要的实证**：改进算法**跳数最多但时延最低**（L259）——即在高处理时延节点存在时，**绕路是降低总时延的正确策略**。这直接支持了"时延 = 传播 + 排队"而非"时延 ∝ 跳数"的建模取向。
6. **受限之处**：它的负载是**每批包数（一次性批量注入）**，不是持续到达率（pps）；没有画出"到达率 → 稳态时延"的连续曲线；也没有扫 α 之外的任何系统参数；**且排队参数 $\mu$、$c$、$N$ 全部未给值**，导致这条曲线无法被任何人复现或复用。

**10. 一句话评价**
**本批唯一把"星上排队"真正建成路由代价的论文**——它用 M/M/1/N 与 M/M/c 把"激光接收缓存有限"和"CPU 资源池五单元"这两个硬件约束写进了 Q 值，并给出了负载阈值与"绕路降时延"的实证；但把所有排队参数留空、把目标函数式 (11) 留成乱码，使它成为**思路可用、数字不可用**的一篇。

## 7AXASN73 — A Survey on Nongeostationary Satellite Systems: The Communication Perspective

**1. 一句话**
从物理层一直到应用层，把 NGSO（非静止轨道）卫星通信做了一次全栈综述——天线/链路预算/星间链路/波形/多址/空间信息网络/SDN/切片/资源管理/干扰/频谱共享/安全，再加监管共存、星座设计、用户设备、运行问题四大部署挑战，最后给出 7 个未来方向。

**2. 问题设定**
NGSO 相比 GSO 的核心卖点是**传播时延更低、体积更小、信号损耗更低**，从而能把时延敏感应用搬到天上去（L5、L17）。作者自陈现有综述的缺口（L46 逐字）："there still lacks a survey providing comprehensive discussions on the whole multi-orbit NGSO communication system aspects"，并特别指出监管共存问题此前只被高层提及、**用户设备需求在公开文献里根本没人梳理**（L46 逐字："the user equipment requirements and advances have not been explored in the open literature"）。

**3. 方法骨架**（综述类，无算法；结构 = 分类框架 + 参数对照 + 挑战清单）
论文结构（L71）：§II NGSO 系统特征与分类（按服务分"天基互联网提供商"与"空间任务"两类）；§III 通信前景（物理层与无线接入 → 网络方面 → 系统与架构）；§IV 部署挑战（监管共存 / 星座设计 / 用户设备 / 运行问题）；§V 未来方向；§VI 结论。
关键的分类与对照表：
- **Table I**（L57）与 14 篇既有综述逐项对比覆盖范围（天基互联网、空间任务、监管共存、星座设计、运行挑战、用户设备、星间连通性、有源天线、波形与接入、软件定义卫星、空间回传、网络切片、资源优化、干扰管理、安全、宽带连接、Open RAN）。
- **Table II**（L88）缩略语表。
- **Table III**（L170）**GSO vs LEO 的链路预算数值对照**——本卡最有用的一张表，见第 9 项。
- **Table IV**（L323）ITU 关于 NGSO-GSO 频谱共享的规则（Ku/Ka/Q-V 三段的频率范围与优先级）。
三条贯穿全文的技术判断：
- **ISL 是降低对地面站依赖的关键**（L178）；RF ISL 成熟但速率低、有干扰；FSO/激光速率高但要复杂捕获跟踪；**THz 在太空无大气衰减是优势，但半导体器件是瓶颈**（L180）。
- **控制架构的集中 vs 分散权衡**（L258）：集中式（控制器在地面服务器）管理效率高但复杂度与 OPEX 高，**控制器到每个节点的控制信道本身还要占带宽**；分散式各星自主调节但**难达全局最优**。
- **资源管理的特殊性**（L262）：NGSO 可用资源比 GSO 少得多（载荷小），且**优化参数"很快过时"**，因此需要降维、低复杂度元启发式或机器学习方法（L262 逐字："the optimization parameters quickly become outdated"）。

**4. 它声称的效果**（综述，给出的是整理后的对照事实）
- **LEO 的 RTD 约为 GSO 的 1/36**（L174 逐字："the RTD in the LEO link is about 36 times lower than in the GSO link"）：Table III 给出 GSO 前向链路 **515.18 ms** vs LEO **14.35 ms**（600 km 高度、仰角 30°）。
- **LEO 链路预算在手持终端上明显更好**：S 波段手持终端下 GSO 的 CNR 仅 **0.51 dB**（下行）/ −14.86 dB（上行），而 LEO 达 **6.61 dB** / −1.66 dB；VSAT（Ka 波段）下两者都不错但 **LEO 上行仍优于 GSO 达 16 dB**（L172）。
- **空间段规模事实**（L103–L114）：Starlink 初期近 12,000 颗（后续可能扩到 42,000），分 550 km/1,110 km/340 km 三层；单星吞吐 17–23 Gbps；用户终端最小仰角 40°。OneWeb 648 颗、18 个极轨面、1,200 km、倾角 87°、最小仰角 55°。O3b 20 颗赤道轨道 8,000 km、用户级约 500 Mbit/s。Kuiper >3,000 颗、LeoSat 108 颗、Telesat 177 颗、Boeing 2,956 颗、华为 Massive VLEO 10,000 颗（300 km）。
- **UCS 数据库**：在轨运行卫星已超 4,000 颗，NGSO 数量远多于 GSO（Fig 1，L22）。
- **全球仍有 39% 人口无法接入地面宽带**（L94）。
- **时延对比的物理根据**：真空光速比光纤高约 50%（$3\times10^8$ vs $2\times10^8$ m/s），所以带 ISL 的低轨星座时延也低于地面光纤（L82）。
- **天文与碎片风险**：粗略估计未来可能另有 **50,000 颗以上**卫星进入地球轨道（L347）。

**5. 实验条件**
综述类，无实验；其"条件"体现为引用与数据口径：
- 链路预算采用 **3GPP 技术说明 [6], [7]** 的参数（L172）；示例 LEO 取 **600 km 高度、仰角 30°**（L174、Table III）。
- 两类用户终端：**S 波段手持终端**（全向天线、线极化）与 **Ka 波段 VSAT**（定向相控阵、圆极化、60 cm 等效口径）（L343）。
- 时间范围：Table I 显示既有综述覆盖 2016–2021，本文为 **2022**（L57）。
- 参考文献数量极大（[1]–[307]，L419–L1030），是典型的 IEEE 综述体量。
- **作者没有做任何自己的仿真或数值实验**；Table III 是转述 3GPP 参数的计算结果。

**6. 它自己承认的局限**
**没有独立的 Limitations 章节**（全文通读：§I–§VI，无 limitation 小节）。但自述缺口极多，且都很具体：
- 用户设备在公开文献中无人梳理，L46（逐字见第 2 项）。
- NGSO-NGSO 干扰刚起步，L268 逐字："most of the prior works focus mainly on the inter-system interference between GSO and NGSO, while the serious issue of NGSO-NGSO interference was recently addressed only in [210]–[213]."
- **ISL 之间的干扰需要更多研究**，L275 逐字："However, the interference between ISLs needs more investigation, which is a serious problem in the NGSO networks as it may occur not only in the overlap of coverage areas but also wherever inter-satellite communications take place."
- 区域星座设计未被深入研究，L333 逐字："This topic has not been deeply investigated in the literature, and thus, new sophisticated approaches to design optimal constellation patterns are needed."
- 边缘计算的实际限制未明，L381 逐字："While this application seems very promising, its practical limitations and requirements are not yet fully understood."
- 网络切片在 NGSO 上仍处早期，L245 逐字："network slicing is still at an early stage of its application into 5G systems and requires novel algorithms and solutions to involve the NGSO systems."
- 物理层安全在卫星上仍是婴儿期，L291 逐字："this method applied to satellite communications is still in its infancy."
- SDN 缺少面向小卫星的架构，L241 逐字："there is a lack of SDN-based architecture solution specifically designed for small satellites."

**7. 它没做但看起来能做的地方（基于内容）**
1. **全篇没有任何"负载"作为自变量的讨论**：资源管理、回传、路由全都在谈"需求非均匀""参数很快过时"（L262、L235），但**没有一处给出负载强度 → 性能的量化关系**。这是这篇全栈综述最一致的空洞。
2. **§V.B 明确把"负载均衡 + 最短端到端传播时延路径"列为尚待探索**，L377 逐字："However, the expected connectivity improvement will be achieved at the cost of higher complexity that is essential for **load balancing between satellite links** and for **finding paths with the shortest end-to-end propagation delay**, as well as tackling the dynamicity of the nodes (e.g., high relative speeds, frequent handovers), **which are yet unexplored areas in the literature**."——这是全篇与本选题最贴近的一句话。
3. **§III.B.2 列出了"空天回传"需要建模的全部输入项**（L235）：拓扑变化、带宽、链路时延、**异构业务/类别的流量生成剖面**、节点的计算与存储能力——**这是一份完整的负载场景要素清单，但论文只列举未组织**。
4. **Table III 只给了静态链路预算**（L170）：没有随仰角、随可见星数、随用户密度变化的任何曲线。
5. **干扰管理一节完全没有容量/负载维度**（L268–L275）：所有讨论都是功率、角度、频段，没有"干扰随负载增长"的分析。
6. **作者自己指出 NGSO 的优化参数"很快过时"**（L262），但**没有给出过时的时间尺度**——而这恰恰是判断"需要多快的在线算法"的关键数字。

**8. 和同批其他篇的关系**
- **与 5AZHJE7N（STIN 仿真器综述）**：**同批的两篇综述，但分工完全不同**。5AZHJE7N 关心"用什么工具做仿真"（工具盘点 + 功能矩阵），本篇关心"系统本身有哪些技术"（物理层到应用层 + 部署挑战）。两者的共同缺口都是**流量/负载**：5AZHJE7N 的三个关键仿真功能不含流量（其 L257–L263），本篇的通信前景与挑战清单也不含负载建模。
- **与 67CSKFK4（Handley）**：本篇是 Handley 之后 5 年的综述，**却完全没有引用 Handley 那篇**（参考文献 L419–L1030 通读未见 "Delay is Not an Option"）。同时本篇在 §V.B（L377）把"负载均衡 + 最短时延路径"称为"yet unexplored areas"——**而 Handley 在 2018 年已经把这个问题明确提出来了并给出了假设方案**。这是一处可以直接指出来的**综述遗漏**。
- **与 53HEEK33 / 5N5LQPPP / 6GWNYSTT（Q-routing 与 DRL 路由）**：本篇把路由归入 §III.B 的"网络方面"，只用两段话概括（SDN 与集中/分散控制，L239–L241、L258），**没有引用任何一篇 RL/DRL 路由论文**，与那几篇不构成对话。
- **与 5PYWVRC5**：本篇 L377 的"负载均衡与最短时延路径尚未探索"与 5PYWVRC5 的实验结论（FD-MADRL 打饱和链路）**恰好对得上**——但两篇互不引用（5PYWVRC5 发表于 2024 年前后，时间上晚于本篇）。
- **与 5HJ8ATR7（MOSAIC）**：本篇 §III.C.3 关于 SDN 控制平面带宽开销的论断（L258："The control channels between a controller and each node will also require additional bandwidth resources"）与 5HJ8ATR7 实测的"信令占 15.75% ISL 带宽"（其 L149）是同一条事实的两种表述。
- **与 57EB6US5 / 6C843JTS**：无关（本篇不涉及 RL 方法论）。

**9. 对"负载变化下到达率/时延"的贡献**
**有可引用的负向证据 + 一份参数底表，但没有正向贡献。**
1. **最直接的一条**：本篇 §V.B **把"负载均衡 + 最短端到端传播时延路径"明确称为 "yet unexplored areas in the literature"**（L377）——这是**一篇 2022 年的 IEEE 全栈综述对选题正当性的背书**：到 2022 年为止，这个方向在综述作者眼中仍是空白。
2. **可引用的时延底表（Table III，L170）**：GSO 前向链路 RTD 515.18 ms vs LEO 14.35 ms（600 km、30° 仰角）；S 波段手持终端下行 CNR：GSO 0.51 dB / LEO 6.61 dB；上行 GSO −14.86 dB / LEO −1.66 dB；VSAT Ka 波段上行 LEO 比 GSO 好 16 dB。**这是一份"同等条件下 LEO 比 GSO 好多少"的量化底表**，可用于说明为什么时延敏感业务要放到 LEO。
3. **一条关于负载性质的关键论断**：LEO 的**需求是非均匀且不确定的**，传统星座设计（极轨、Walker-Delta、flower）**没有考虑地面需求特征**，因此在"全球非均匀且不确定的需求"下是低效的（L329 逐字："these design approaches do not take into consideration the demand characteristics on Earth, which makes them inefficient strategies when bearing in mind the non-uniform and uncertain demand over the globe"）。作者推荐的替代是**分阶段弹性部署**（适应需求演化）。
4. **一条关于算法时效性的论断**：NGSO 的资源管理"优化参数很快过时"（L262），加上 LEO 可见窗口短（用户设备必须在很短可见窗口内完成接入，L337、L285 提到 "short visibility window"）——**这为"在线/快速响应负载变化"提供了动机，但没有给出时间尺度数字**。
5. **限制**：全篇没有到达率（pps）、没有排队模型、没有负载-时延曲线、没有负载作为自变量的任何图。

**10. 一句话评价**
**一份覆盖面极广但深度均匀偏浅的 NGSO 通信全栈地图**——它的价值在于用 Table III 给出了 LEO/GSO 的时延与链路预算基准、并用一句话（L377）确认了"负载均衡 + 最短时延路径"是空白；它的不足在于**通篇不谈负载强度**，且漏引了 Handley 那篇早已提出同一问题的论文。

<!-- END-CARDS-R2 -->









