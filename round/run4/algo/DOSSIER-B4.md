# DOSSIER-B4：T1 算法级全拆（9 篇）

> 批次：round/run4/algo，B4（本次派发）。分支 `agent/20260911-topic-loop-r2`，worktree `.worktrees/topic-loop-20260910`。
> 覆盖：3MRQRWHU、EG9X569M、YI9G7NR7、X5Z98UPM、8N9QJHC2、47J2H748、JLF7IEBQ、WFA3CZLP、UF8IQTA2（TIER-ASSIGNMENT.md L34–L42 全部 9 篇，无遗漏）。
> 格式：按 `EXTRACTION-TEMPLATE.md` 的 12 项逐篇填满。**所有结论均带 MD 行号 + 逐字英文原文**；公式逐字抄 LaTeX 原文（含 MinerU 转换留下的上标错位/乱码，保持原样，不以"看起来更合理"改写）。
> 行号基准：VM `/data/liguang13/topic-loop-r2/md/<key>/<key>/txt/<key>.md`，与本地副本 `/tmp/b4md/<key>.md` 字节一致（scp）。
> "未见"判定的检索范围统一为：该篇 Markdown 全文（行号区间在条目内注明），方式 `grep -c -i -E "<pattern>" <file>`，命中数 0 方判"未见"。
> **纪律声明**：负载/流量/评测设置一律只登记在第 12 项，不作为算法贡献。
>
> **引文保真度声明（重要，供核验者使用）**：
> 1. **LaTeX 公式一律逐字复制，未做任何归一化**——包括 MinerU 的上标错位、缺字、乱码（如 X5Z98UPM 公式 (5) 的 @@y@@、8N9QJHC2 的 @@@@$e@@、JLF7IEBQ Fig.7 的 "dding"、EG9X569M 公式 (10)(11) 里未定义的 @@mathcal{V}@@）；本批 32 条公式已用 @@grep -qF@@ 逐条回查 VM 原文（31 条 HIT；发现并已修正 3 处笔误：3MRQRWHU 公式 (3) 的 @@leqslant@@/@@leq@@、47J2H748 更新式 overbrace 的精确写法、WFA3CZLP Algorithm 1 递推式的 @@big(@@ 内层括号）。
> 2. **英文散文引文保留原用词、标点与大小写，但把 MinerU 输出的连续多空格归一化为单空格**（MinerU 对两端对齐正文会输出 "the total  number  of" 这类双空格；这是排版产物，不是原文用词差异）。若核验者发现某句引文与原文只差空格，即属此类，非改写。
> 3. 行号取 read 工具/sed 的行号，可用 @@sed -n 'Np' <file>@@ 原样复现。

---

## 1. 3MRQRWHU — Multi-QoS routing algorithm based on reinforcement learning for LEO satellite networks

（JSEE，DOI 10.23919/JSEE.2024.000041；正文 L1–362，参考文献 L363–L469 未逐条读）

### 1) MDP 定义
- 形式化：L184 — "The routing process is modeled as a Markov decision process (MDP), represented by $`M = ( S , P , R , A )`$, where S represents the state space, $`P`$ represents the state transition probability, R represents the reward, and A represents the action[31,32]."
- **状态 s_t（逐字段）**：L187 公式 (11)，逐字：
  ```latex
  S _ { \tau _ { p } } = \{ \mathrm { d e l a y } ( e _ { i , j } ) , \mathrm { l o s s } ( e _ { i , j } ) , \mathrm { b a n d } ( e _ { i , j } ) \} , \forall e _ { i , j } \in E _ { \tau _ { p } } , \forall \tau _ { p } \in T .\tag{11}
  ```
  三个分量 = 逐条 ISL 的 delay / loss / band（L101 Table 1：`delay(·)`="Time delay calculation function"，`loss(·)`="Bit error rate calculation function"，`band(·)`="Bandwidth calculation function"）。**维度**未给（未给节点/链路特征维数、未给神经网络输入维度——本文无神经网络，见第 2 项）。**归一化**：状态本身未归一化，归一化发生在奖励侧（第 3 项公式 15）。**随时间聚合**：状态带时间片下标 $\tau_p$，即"按时间片给出的瞬时链路快照"，L46 — "It is assumed that the network topology is static in a time snapshot."
- **动作 a_t**：L190 — "Action space A represents the process in which the agent moves from the current satellite node to the next satellite node during the routing decision process."；动作选择规则 L193 公式 (12)，逐字：
  ```latex
  a ( s _ { t } ) = \left\{ \begin{array} { l l } { \arg \operatorname* { m a x } _ { a _ { t } } Q ( s _ { t } , a _ { t } ) , \ \mathrm { r a n d } \gtrsim \varepsilon } \\ { \quad \mathrm { r a n d o m l y ~ a c t i o n } , \ \mathrm { r a n d } < \varepsilon } \end{array} \right.\tag{12}
  ```
  动作空间大小 = 当前卫星的可选下一跳集合（四 ISL 拓扑，L41 — "Each satellite has four inter-satellite links (ISLs), including two intra-orbit interfaces and two inter-orbit interfaces."），但**无显式掩码变量**（检索 `multi-?agent|decentraliz|decentralis`、`action mask|invalid action|impossible action|mask` 全文 hits=0）；掩码以"临时删点/断邻接"的算法步骤实现（见第 5 项）。
- **奖励 r_t**：L259 公式 (19)，逐字：
  ```latex
  \begin{array} { c } { { r ( a ) = \alpha \cdot r ^ { \mathrm { d e l a y } } ( a ) + \beta \cdot r ^ { \mathrm { l o s s } } ( a ) + } } \\ { { \lambda \cdot r ^ { \mathrm { b a n d } } ( a ) + k \cdot \gamma \cdot r ^ { \mathrm { v a r } } ( a ) . } } \end{array}\tag{19}
  ```
  四项系数出自 L75 公式 (2)，逐字：
  ```latex
  \left\{ \begin{array} { l l } { \alpha = \frac { \phi _ { \mathrm { d e l a p } } \left( u \right) } { \phi ^ { \mathrm { m a x } } } } \\ { \beta = \frac { \phi _ { \mathrm { l o s s } } \left( u \right) } { \phi ^ { \mathrm { m a x } } } } \\ { \lambda = \frac { \phi _ { \mathrm { b a n d } } \left( u \right) } { \phi ^ { \mathrm { m a x } } } } \\ { \gamma = \frac { \phi ^ { \mathrm { m a x } } - \phi \left( u \right) } { k \cdot \phi ^ { \mathrm { m a x } } } } \end{array} \right.\tag{2}
  ```
  （原文 L75 的 $\phi_{\mathrm{delap}}$ 系 MinerU 把 `delay` 转坏的写法，照抄；L78 约束 $\alpha + \beta + \lambda + k \cdot \gamma = 1$，且 L78 — "$\phi^{\max}$ represents the maximum priority, that is, all QoS requirement levels are the highest, and $k$ is an integer greater than 1. Its function is to reduce the impact proportion of the load balancing."）
  三项归一化分项 L227 公式 (15)，逐字：
  ```latex
  \left\{ \begin{array} { l l } { r ^ { \mathrm { d e l a y } } ( a ) = \displaystyle \frac { \operatorname* { m a x } ( \mathrm { d e l a y } ( e _ { q , p } ) ) - \mathrm { d e l a y } ( a ) } { \operatorname* { m a x } ( \mathrm { d e l a y } ( e _ { q , p } ) ) - \operatorname* { m i n } ( \mathrm { d e l a y } ( e _ { m , n } ) ) } } \\ { r ^ { \mathrm { l o s s } } ( a ) = \displaystyle \frac { \operatorname* { m a x } ( \mathrm { l o s s } ( e _ { q , p } ) ) - \mathrm { l o s s } ( a ) } { \operatorname* { m a x } ( \mathrm { l o s s } ( e _ { q , p } ) ) - \operatorname* { m i n } ( \mathrm { l o s s } ( e _ { m , n } ) ) } } \\ { r ^ { \mathrm { b a n d } } ( a ) = \displaystyle \frac { \mathrm { b a n d } ( a ) - \operatorname* { m i n } ( \mathrm { b a n d } ( e _ { m , n } ) ) } { \operatorname* { m a x } ( \mathrm { b a n d } ( e _ { q , p } ) ) - \operatorname* { m i n } ( \mathrm { b a n d } ( e _ { m , n } ) ) } } \end{array} \right.\tag{15}
  ```
  负载均衡项 L237/245/251，逐字：公式 (16) `\operatorname { V a r } ( E ) = { \frac { \sum ( l ( e _ { i , j } ) - { \overline { { l ( e _ { i , j } ) } } } ) ^ { 2 } } { \operatorname { n u m } ( e _ { i , j } ) } } , \ e _ { i , j } \in E\tag{16}`；公式 (17) `\mathrm { V a r } ^ { \operatorname* { m a x } } = \left( \frac { \mathrm { B a n d } ( e _ { i , j } ) } { 2 } \right) ^ { 2 } , ~ e _ { i , j } \in E .\tag{17}`；公式 (18) `r ^ { \mathrm { v a r } } ( a ) = { \frac { \mathrm { V a r } ^ { \mathrm { m a x } } - \mathrm { V a r } ( E ) } { \mathrm { V a r } ^ { \mathrm { m a x } } } }\tag{18}`。
  **折扣 γ**：更新式中另有折扣系数 $\gamma_0$（L208 — "$\gamma _ { 0 }$ is the discount coefficient, which determines the impact of future actions on the $\mathcal { Q }$ value."）。**注意符号冲突（原文如此，非本报告笔误）**：公式 (2) 用 $\gamma$ 表示负载均衡权重，公式 (13) 用 $\gamma_0$ 表示折扣。
- **转移/终止**：episode = 一次从源到宿的寻路。L218 — "Taking the starting node of the service as the initial state, continuously select the optimal action until reaching the destination node, and then we get the final optimal routing path." 外层对同一服务做 $\mathrm{maxepoch}$ 次重启（L283 "forj=1:maxepoch do"），L302 — "find the optimal path based on the total return R (j)"，即**多起点多次寻路取总回报最优**，非资格迹、非 n-step（检索 `eligibility|n-step|multi-step|multistep` 全文 hits=0）。

### 2) 学习算法与更新式
- 算法名：QLRA（L175 节标题 `## 3.1 QLRA`；L271 "Based on the Q-learning algorithm, we propose an auxiliary converge QLRA (AQLRA)"）。
- 更新式 L205 公式 (13)，逐字：
  ```latex
  \begin{array} { r l } & { \mathrm { ~ } Q ( s _ { t } , a _ { t } ) = Q ( s _ { t } , a _ { t } ) + \alpha \cdot ( r ( t ) + } \\ & { \mathrm { ~ } \gamma _ { 0 } \cdot Q ( s _ { t + 1 } , a _ { t } ) - Q ( s _ { t } , a _ { t } ) ) } \end{array}\tag{13}
  ```
  **逐字照抄要点**：右端 TD 项用的是 $Q(s_{t+1},\mathbf{a_t})$（写作 $a_t$，不是 $\max_{a}Q(s_{t+1},a)$，也不是 $a_{t+1}$）——原文如此。L208 — "$\alpha$ is the learning factor, which determines the speed of the agent to learn the optimal value."
- 网络结构：**无神经网络**。L202 — "The Q table is a matrix that stores the values of all $Q ( s _ { t } , a _ { t } )$."（表格型 Q）。因此无层数/宽度/激活/共享参数/图算子可登记；无 target net、无 replay（检索 `target network|target q|replay|experience pool|double q|double dqn` 全文 hits=0）。
- 收敛判据：L210 — "By repeatedly calculating $Q ( s _ { t } , a _ { t } )$ and iteratively updating the $\boldsymbol { Q }$ table, we finally get the converged $\boldsymbol { Q }$ table"，策略 L215 公式 (14) `a ^ { * } ( s _ { t } ) = \arg \operatorname* { m a x } _ { a _ { t } } { Q ^ { * } ( s _ { t } , a _ { t } ) } .\tag{14}`。

### 3) 信用分配
- **逐跳（逐链路）即时奖励**，且动作与链路一一对应：L230 — "where a represents the action performed by the agent, which is equivalent to the agent passing through the ISL $e$."
- 奖励是"当前动作所选链路相对全网最好/最差链路"的归一化值（公式 15 中的 $e_{q,p}$ / $e_{m,n}$，L230 — "$e _ { q , p }$ and $e _ { m , n }$ represent the ISL with the best performance and the worst performance in the current satellite networks available satellite link set"）。**因此信用分配依赖全网极值**，不是纯局部量。
- 路径级汇总：Algorithm 1 第 20 步 L302 — "record the total return R (j) of this pathfinding"；第 22 步 L304 — "find the optimal path based on the total return R (j)"。
- **是否区分损失原因**：不区分"丢失原因"（状态/奖励只有 loss 这一统计量），但**分维度**（delay/loss/band/var 四项）并按服务优先级加权。失败步的特殊赋值见 Algorithm 1 第 16 步 L297 — "`Q ( s _ { t n } , a _ { t } ) = 0` and update $\boldsymbol { Q }$ value according to (13)"。

### 4) 状态里有没有时间信息
- **只有"切片索引"这一时间标记，没有历史/趋势/差分/EWMA**。证据：状态定义公式 (11) 仅含三个瞬时链路量；检索 `EWMA|exponential moving|moving average|history|historical|previous state|trend` 全文仅 1 处命中 L21，且是**综述句**（"[6], a routing algorithm based on historical information prediction is proposed"），与本算法状态无关。
- 时间确实以另一种方式进入系统：**服务等待时间等级**（在服务优先级模型里，不在 MDP 状态里）L80 — "When the service is not processed within the time slice $\tau _ { p }$, the service will enter the next time slice $\tau _ { p + 1 }$, and the corresponding service waiting time level $\phi _ { \mathrm { t i m e } } ( u )$ will also become 1."；公式 (3) L83 `\phi \left( u \right) = \phi _ { \mathrm { t i m e } } \left( u \right) + \phi \left( u \right) , \ \phi _ { \mathrm { t i m e } } \left( u \right) \leqslant \phi _ { \mathrm { t i m e } } ^ { \mathrm { m a x } } .\tag{3}`；上限动机 L80 — "Its function is to avoid the low-priority services in turn seizing high-priority traffic resources after a long time, and limit the resource capture to a reasonable range."

### 5) 动作有没有时间结构
- **决策粒度是"每个服务一次"，不是每包一次**：Algorithm 1 外层 L280-281 "for $i { = } 1 { : } N$ do / $u _ { s \to d }$ = argmax($\phi$(User))"，即按优先级依次取服务；L306-307 第 24 步 — "update the networks topology according to the best path $G _ { \tau _ { n } } \left( V , E \right)$"——**每次决策后把该路径对链路容量的占用写回拓扑**（这是动作对环境的持久影响）。
- **有动作掩码（以算法步骤实现，非显式 mask 变量）**：L266 — "we mark all the nodes that the agent passes through. As shown in Fig. 3, for the passing node D, the node D and the adjacent node H will be regarded as an impassable link until the agent reaches the destination node, thus avoiding the node being repeatedly selected. In addition, another advantage is that when the agent reaches the adjacent node H, the agent's optional action in node H changes from 3 to 2..."；Algorithm 1 第 11–12 步 L289-293 — "temporarily delete node $s _ { t }$ from $G(V,E)$ by auxiliary converge algorithm / temporarily disconnect adjacent nodes of $s _ { t }$ by auxiliary converge algorithm"。
- **无动作驻留、无流级缓存、无切换代价**（第 3 项之外的检索：`action mask|...` hits=0；正文亦未见 switch/handover cost 相关公式）。

### 6) 多智能体设定
- **未见多智能体设定**：全文检索 `multi-?agent|decentraliz|decentralis` hits=1，唯一命中 L23 是**他人工作**的句子——"[12], an intelligent decentralized load balancing routing algorithm based on deep reinforcement learning is proposed"。
- 本算法是**单智能体 + 全局 Q 表**（L202 "The Q table is a matrix that stores the values of all $Q ( s _ { t } , a _ { t } )$."）；无参数共享、无非平稳处理、无智能体通信、无动作同步可登记。

### 7) 训练协议
- 负载/拓扑生成见第 12 项（L318）。
- **训练与评估是同一套仿真**：全文无 train/test 划分语句；L314 — "In this section, we verify the effectiveness of the proposed AQLRA algorithm."
- episode 采样方式：Algorithm 1 以"服务集合 User 的优先级排序"逐条寻路，同一服务内做 $\mathrm{maxepoch}$ 次寻路重启（L283），$\mathrm{maxepoch}$ **未给数值**（L276 仅写 "maximum number of iterations maxepoch"；全文未出现其取值）。
- **超参未报告**：$\alpha$、$\gamma_0$、$\varepsilon$ 的取值在 L316–L353 的仿真设置段内均未见（L318 只给了星座/带宽/服务强度）。
- 对比算法：Dijkstra、蚁群（L318、L320、L322）。

### 8) 该文的算法贡献
- L29 – "(i) This paper proposes a priority queue model based on differential services (DiffServ), which ensures that high-priority services can be processed first. For low-priority services, the waiting time is weighted to solve the problem that low-priority services will not be processed for a long time."
- L31 – "(ii) Aiming at the problem of dynamic change of satellite networks topology and poor convergence speed of routing algorithm, an effective auxiliary learning algorithm is proposed. By removing the passing nodes, the convergence process of the reinforcement learning algorithm can be accelerated..."
- L33 – "(iii) While optimizing QoS, the load balancing performance of satellite networks is optimized by adopting the improved Q-learning algorithm..."
> 对应关系：(i)↔第 4 项的服务等待时间等级 + 第 3 项的分服务权重；(ii)↔第 5 项的删点掩码；(iii)↔第 3 项公式 (16)–(18) 的方差型负载均衡奖励项。

### 9) 该文自述的局限
L361（Conclusions 末段）逐字："In future research, we will consider making the algorithm update the networks model in time when the networks topology changes. At the same time, we also incorporate cross-layer information transmission between different satellite orbital planes into future research topics."

### 10) 该文没有考察的算法选择
（均基于第 1–7 项实际内容 + 全文检索）
1. 函数近似/神经网络 — 状态与动作全是表格型 Q（L202）；检索 `target network|target q|replay|experience pool|double q|double dqn` 全文 hits=0，故也未考察 replay、target net、double Q。
2. 多智能体分解/分布式学习 — 全文单智能体（第 6 项检索）。
3. 资格迹 / n-step / 多步回报 — 检索 `eligibility|n-step|multi-step|multistep` hits=0；episode 内只用单步 TD（公式 13）。
4. 队列/缓存状态入状态 — 状态只有 delay/loss/band（公式 11），排队时延未作为独立状态分量（与 47J2H748 的 Q-routing 恰成对照）。
5. 动作驻留/路由抖动代价 — 未考察（见第 5 项）。
6. 探索策略的调参 — $\varepsilon$ 是固定阈值（公式 12），无衰减计划，且取值未报告（第 7 项）。
7. 超参敏感性 — $\alpha$、$\gamma_0$ 取值未报告（第 7 项），故无法评估。

### 11) 可复用的具体机制
1. **"归一化的链路相对优劣 + 方差型负载均衡"复合奖励**（公式 15 + 16–18）：用当前动作链路相对全网最优/最差链路的 min-max 归一化得到 $r^{delay},r^{loss},r^{band}$，再用 $r^{var}=(\mathrm{Var}^{\max}-\mathrm{Var}(E))/\mathrm{Var}^{\max}$ 且 $\mathrm{Var}^{\max}=(\mathrm{Band}(e_{i,j})/2)^2$ 作为负载均衡项——**归一化分母有显式闭式定义**，可直接搬到我们平台作为 reward 塑形（尤其 $\mathrm{Var}^{\max}$ 的取法）。
2. **服务等待时间等级 + 上限**（公式 3）：$\phi_{\mathrm{time}}(u)$ 每跨一个时间片 +1、封顶 $\phi_{\mathrm{time}}^{\max}$，用来防止低优先级流量饿死同时也防止其长期抢占高优先级资源——可直接作为我们多业务优先级的防饿死机制。
3. **删点式动作掩码（auxiliary converge）**：把已过节点及其邻接边临时设为不可通行（L266、Algorithm 1 步 11–12），既消除重复队列又缩小动作空间——在任何基于图上逐跳搜索的 RL 路由里都是即插即用的加速项。

### 12) 实验合同里与"负载"相关的设置（仅登记，非贡献）
- L318 逐字要点：66 颗卫星、6 条极轨、轨道高度 720 km、倾角 $86.4^\circ$、轨面间距 $31.6^\circ$、相位因子 0.5；纬度大于 70° 时相邻轨间不建链；运行周期 100.45 min，故"each time slice is set to 1 min"；"this paper generates a set of user requests with different QoS requirements that constitute the priority level of the requests"；源/宿在 66 个节点中随机选；"the minimum bandwidth requirement of the service is set between 10 Mb/s and 100 Mb/s according to the demand level, and the maximum available bandwidth of each satellite link is set to 4000 Mb/s"；服务起止时间服从正态分布。
- 对比算法：Dijkstra（L320）、蚁群（L322）+ 本文 AQLRA。
- 图 5 的负载形态 L340 — "we set a large number of high priority services in all time slices, while the number of default services increases with the increase of the time slice. Starting from the 3rd time slice, the default services cannot be processed in time within a time slice, so the average processing delay begins to rise."；机制生效后 L340 — "after the 5th time slice, our service waiting time mechanism starts to play a role, and the priority of some default services is promoted, so that the average total delay of low priority services is kept near 80 ms."
- 报出的改进口径（仅登记数字）：L346 负载均衡效用比 Dijkstra 提升 200%、比蚁群提升 50%；L353 综合效用比 Dijkstra 提升约 88%、比蚁群提升约 43%。

---

## 2. EG9X569M — A Robust Routing Strategy based on Deep Reinforcement Learning for Mege Satellite Constellations

（RRS-DRL，UESTC，March 2, 2023；正文 L1–L221，References L222–L241 未逐条读。**注意：本 MD 里正文出现两遍**——L1–L13 摘要页 + L15–L21 起的正文，行号引用一律取后者）

### 1) MDP 定义
- L97 — "For packets, the node selection in the given link depends only on the node selection in the previous link. The action taken by each packet is only related to the current state of the network.It can typically be described as a Markov Decision Process (MDP) [8]."
- **状态 s_t（逐字段）**：L101 — "i): Status \S \colon \ ( N o d e _ { c u r r p o s } , N o d e _ { d e s t } , \chi _ { t _ { i } } )\, N ode<sub>currpos</sub> indicates the number of the current node, \Node_{dest}\ is the number of the destination \, \chi _ { t _ { i } }\ the form of jamming received, which provides sufficient information to learn the best strategy for routing."
  三字段：① 当前节点编号 ② 目的节点编号 ③ 干扰形态 \chi_{t_i}\。**维度/归一化**：全文无归一化语句；状态无维度声明。**随时间聚合**：否，当前时刻快照。
- **动作 a_t**：L103 — "ii): Action \A \colon N o d e _ { n e x t }\ , the next-hop neighbour node reachable by the satellite node(generated according to the network topology)." 动作空间 = 可达邻居集合（大小随拓扑变）；**无动作掩码**（见第 10 项计数）。
- **奖励 r_t**：L114 公式 (8)，逐字：
  `\mathrm { r } = w _ { 1 } * D i s _ { i } + w _ { 2 } * A o I _ { s ^ { \prime } } + w _ { 3 } * \vartheta _ { s ^ { \prime } }\(8)`
  （原 `\tag{8}`，为便于阅读此处用 (8) 记；下同，凡"公式 (N)"均对应原文 `\tag{N}`。）
  三项逐字：L107 — "The distance between the next satellite node and the destination node \Dis_i\. To train the agent to know how to send packets to the destination without passing through redundant satellite nodes, we should add a distance penalty so that the agent automatically chooses the shorter path."；L109 — "AoI of the packet which arrives at the next hop \AoI_{s^\prime}\. Aol is designed to quantify time-critical updates at the receiving end, characterising the timely delivery of information at the destination, and increasing the Aol penalty ensures that information is fresh."；L111 — "The queue growth rate \vartheta _ { s ^ { \prime } }\, which sets a penalty proportional to the queue growth rate when the queue size exceeds the threshold, is set to reduce packet buildup and increase the probability that traffic will be distributed evenly."
  **三项都是惩罚项却以加号相连**（原文如此）；**\w_1,w_2,w_3\ 取值全文未给**。
- **折扣 \gamma\**：L120 公式 (9) `P : \operatorname* { m a x } _ { \pi ^ { * } } \left( \sum _ { \tau = 0 } ^ { \infty } \gamma ^ { \tau } r _ { t + \tau } \mid s _ { t } = s , a _ { t } = a \right)\(9)`；L123 — "\gamma \in [ 0 , 1 )\ is the discount factor,the weight between immediate and subsequent rewards."；取值 L183 — "discount factor γ is \0 . 6\".
- **AoI 定义式（第二个奖励源）**：公式 (5) L68 逐字（MinerU 三段等价变形，末式最简）：
  `\begin{array} { l } { { \displaystyle { \cal A } _ { a } ^ { l } = \frac { 1 } { T } \sum _ { k = 1 } ^ { K } \left( \frac { 1 } { 2 \nu ^ { l 2 } } + \frac { d } { \nu ^ { l } \mu _ { s l a } } + \frac { d _ { s l , t o , a } } { \nu ^ { l } c } \right) } } \{ \displaystyle ~ = \frac { K } { T } \frac { 1 } { K } \sum _ { k = 1 } ^ { K } \left( \frac { 1 } { 2 \nu ^ { l 2 } } + \frac { d } { \nu ^ { l } \mu _ { s l a } } + \frac { d _ { s l , t o , a } } { \nu ^ { l } c } \right) } } \{ \displaystyle ~ = \nu ^ { l } \left( \frac { 1 } { 2 \nu ^ { l 2 } } + \frac { d } { \nu ^ { l } \mu _ { s l a } } + \frac { d _ { s l , t o , a } } { \nu ^ { l } c } \right) } } \{ \displaystyle ~ = \frac { 1 } { 2 \nu ^ { l } } + \frac { d } { \mu _ { s l a } } + \frac { d _ { s l , t o , a } } { c } } } \end{array}\
  下一跳 AoI 公式 (6) L74：`A _ { d _ { l } } = \frac { 1 } { 2 \nu ^ { l } } + \sum _ { i \not = d _ { l } , \lambda _ { i j } ^ { l } = 1 } ( \frac { d } { \mu _ { s _ { l } a } } + \frac { d _ { i \_ t o _ { - } j } } { c } ) .\`
  全网平均 AoI 公式 (7) L80：`A _ { a v e } = \sum _ { l \in \cal L } { \cal A } _ { d _ { l } } = \sum _ { l \in \cal L } { \left( \frac { 1 } { 2 \nu ^ { l } } + \sum _ { \substack { i \neq d _ { l } , \lambda _ { i j } ^ { l } = 1 } } ( \frac { d } { \mu _ { i j } } + \frac { d _ { i , t o \_ j } } { c } ) \right) } } = \sum _ { l \in \cal L } { \frac { 1 } { 2 \nu ^ { l } } } + \sum _ { \substack { i \in \eta _ { j } \in \cal T _ { i } , \lambda _ { i j } ^ { l } = 1 } } ( \frac { d } { \mu _ { i j } } + \frac { d _ { i , t o \_ j } } { c } )\`
- **转移/终止**：L149 — "The episodic interaction ends once all the packets reach the destination node. And we obtain the AoI of all packets at the destination node." **无资格迹/n 步**（检索见第 10 项）。

### 2) 学习算法与更新式
- 算法名 RRS-DRL，基于 DQN：L93 — "we propose a robust routing algorithm based on deep Q-network(DQN) to obtain the perception of satellite link delay with respect to the age of node information without precise knowledge of the propagation delay."
- **损失** 公式 (10) L130 逐字：
  `L ( \theta ) = E _ { \pi _ { \theta } } \left[ \sum \left( r + \gamma * \mathcal { V } \left( Q ^ { * } \left( s ^ { \prime } , a , \theta ^ { - } \right) \right) - Q ( s , a , \theta ) \right) ^ { 2 } \right]\
- **梯度** 公式 (11) L136 逐字（**原文此式无平方、无 \nabla_\theta\ 记法外的定义，行末接 "where \alpha > 0\ is the learning rate."——照抄**）：
  `\nabla _ { \boldsymbol { \theta } } L ( \boldsymbol { \theta } ) \approx E _ { e } \left[ \left( r + \gamma * \mathcal { V } \left( Q ^ { * } \left( s ^ { \prime } , a , \theta ^ { - } \right) \right) - Q ( s , a , \theta ) \right) \right]\
- **target net**：有。L133 — "\Q ^ { * }\ is the target q-value and \theta ^ { - }\ is the parameter for the target q-value."；L173 — "Update network every \C\ steps"；L183 — "The target network update step is 10"。**Double Q：未见**（第 10 项计数）。
- **replay**：有。L127 — "The transitions in the memory replay pool are then stored \boldsymbol { e } = ( s , a , r , s ^ { \prime } )\ ."；L183 — "memory batch size is 16, and size of memory replay pool N is 1000"。
- **探索**：L144 — "\varepsilon = \varepsilon _ { 0 } \cdot \varepsilon _ { f } ^ { i }\"；L183 — "\varepsilon _ { 0 }\ is 0.7, ε<sub>f</sub> is 0.975"。
- **网络结构**：L149 — "Usually, it contains two fully connected layers (of size 175) for extracting the features of the satellite network. The output features are sequentially input to the output layer to obtain the final value function."；L183 — "the activation function is Tanh"，"learning rate is 0.005"。无图算子（全文无 GNN/GCN/GAT 语句）。
- Algorithm 框（L156–L175）逐字关键行：L160 "3: for step= 1 to step − num do"；L173 "15: Update network every \C\ steps"；L159 "2: for episode = 1 to \infty\ do"。

### 3) 信用分配
- L105 — "iii):Reward r: The reward is defined as a function \R \left( a , s ^ { \prime } \right)\ a denotes the selected action, and \s ^ { \prime }\ denotes the next node number reached after the node selection action."——**奖励全部归因到被选中的下一跳 \s'\**。
- **逐跳即时 + 目的节点处的终局观测量**：L154 — "Every time a packet arrives at a new node, the satellite communication network updates its internal state, feeding back a reward r, an experience term \left( { { s _ { t } } , { a _ { t } } , { r _ { t } } , { s _ { t + 1 } } } \right)\ is stored in the experience pool, and the model parameters are updated with the sampled values therein."；L149（终局 AoI，见上）。
- **是否区分损失原因**：不区分丢包原因；但把拥塞拆成两个通道——"队列增长率"（超阈值才罚，L111）与"信息年龄"（L109）。L111 — "which sets a penalty proportional to the queue growth rate when the queue size exceeds the threshold"。

### 4) 状态里有没有时间信息
- **没有**。状态只有当前节点/目的节点/干扰形态（L101）。检索 \grep -ciE "EWMA|exponential moving|moving average|history|historical|previous state|trend"\ → **0 命中**（全文 241 行）。
- 时间以**奖励项**而非状态分量进入：AoI（公式 5/6）与队列增长率 \vartheta_{s'}\。
- 干扰带时间标记但不进状态：L41 — "we denote Li as the set of links in L that are within the jamming range at the time of \t _ { i }\"；状态里只保留其"形态" \chi_{t_i}\。

### 5) 动作有没有时间结构
- **每包逐跳独立决策**（L97、L154）。
- **无动作驻留、无流级缓存、无切换代价**（全文无相应语句）。
- 唯一"时间结构"在训练侧：\varepsilon = \varepsilon_0 \varepsilon_f^i\（L144）随迭代衰减。
- 包生成节拍 L188 — "Each time a packet is transmitted, a new packet is initialised after a certain time step."

### 6) 多智能体设定
- **未见**。检索 \grep -ciE "multi-?agent|decentraliz|decentralis"\ → **0 命中**。
- 学习单位是单代理（L127 "the agent selects a random batch of transitions and calculates the loss"）；无参数共享、无非平稳处理、无通信、无动作同步。

### 7) 训练协议
- 拓扑/参数 L177 — "The parameters in this paper are taken from Starlink's FCC file, and the bilinear element set coordinates of Starlink's satellites in different orbits are also available... During the simulation, 175 satellites were selected as experiments."；表 1（L179）逐字：Track height 550km / Minimum angle of elevation 25° / Number of tracks 7 / Number of satellites per orbit 25 / Inclination 53°。
- episode 采样 L188 — "many packets are generated on the network (network load), each with a random source and destination node."
- **训练与评估同分布**：全文只有一套仿真（L183/L188），无 train/test 划分语句。
- **训练步数/时长未给**（Algorithm 只有 "for episode = 1 to \infty\"，L159）。
- 对比算法 SPF（L188 — "we compare the traditional routing algorithms: shortest path fRRSt (SPF) [10]"）。

### 8) 该文的算法贡献
- L29 逐字 — "For scenarios where jamming is considered, we propose a robust routing strategy based on deep reinforcement learning (RRS-DRL). We use a priori information about the jamming as part of the state, enabling the routing algorithm to deal with dynamic network changes. Secondly, as it is also crucial for meeting timely responses to emergency events. We combine the Age of information (AoI) of packets to reward and punish the selection of the next hop, ensuring the effectiveness of messages collection and transmission across the network and realising the time value of information."
- 对应：① 状态加干扰形态（第 1 项）；② 奖励加 AoI 项与队列增长率项（第 1、3 项）；③ 目标从"链路断开"扩展到"链路性能退化"：L105 — "in practice, in LEO constellations, not only jamming avoidance but also load balancing is required using routing strategies when sweeping jamming is encountered and when nodes are partially available but with degraded performance"。

### 9) 该文自述的局限
**未见自述**。检索 \grep -ciE "limitation|future work|future research|drawback|shortcoming"\ → **0 命中**（全文 241 行）；L218 的 Conclusion 只列增益。

### 10) 该文没有考察的算法选择
**检索范围 = 该篇 MD 全文 241 行**，逐条给模式与实测计数：

| 模式 | 计数 | 判读 |
|---|---|---|
| \grep -ciE "multi-?agent\|decentraliz\|decentralis"\ | **0** | 无多智能体 |
| \grep -ciE "double q\|double dqn\|dueling\|prioritiz"\ | **0** | 无 double/dueling/优先回放 |
| \grep -ciE "mask\|invalid action\|feasible"\ | **0** | 无动作掩码/可行性处理 |
| \grep -ciE "EWMA\|exponential moving\|moving average\|history\|historical\|previous state\|trend"\ | **0** | 状态无历史 |
| \grep -ciE "eligibility\|n-step\|multi-step\|multistep"\ | **0** | 无资格迹/n 步 |
| \grep -ciE "normaliz\|normalis"\ | **0** | 无归一化 |
| \grep -ciE "target network\|target q\|replay\|experience pool"\ | **5** | **有命中，但构不成"未考察"的反例**：均为本文自身机制（L127 replay 池、L133 target q、L169 采样） |

1. Double/dueling/优先回放、软更新：未考察。
2. 多智能体分解与参数共享：未考察。
3. 状态的历史/趋势编码：未考察。
4. 动作掩码与不可达兜底：未考察（L103 只说 "the next-hop neighbour node reachable by the satellite node"）。
5. 状态归一化：未考察。
6. 资格迹/n 步：未考察。
7. **原文内部缺口（登记，用于复现）**：公式 (10)(11) 里的 \mathcal{V}(\cdot)\ 全文无定义；公式 (9) 的 \P\ 无定义；公式 (11) 行末文字称 \alpha\ 为 learning rate，但该式左端是 \nabla_\theta L(\theta)\。**要复现必须自行补定义**。

### 11) 可复用的具体机制
1. **AoI 作为逐跳可计算奖励项**：公式 (6) L74 把"下一跳处信息年龄"拆成 \frac{1}{2\nu^l} + \sum(\frac{d}{\mu_{s_l a}} + \frac{d_{i\_to\_j}}{c})\——生成间隔项 + 传输时延项 + 传播时延项，全部是本地可算量。可直接作为我们平台的 AoI 塑形项。
2. **队列"增长率"而非"队列长度"作拥塞惩罚**：L111 — "sets a penalty proportional to the queue growth rate when the queue size exceeds the threshold"。对突发更敏感，且需显式阈值——阈值取值原文未给，需自行标定。
3. **把"退化"与"断开"分开建模**：L101 的 \chi_{t_i}\（干扰形态入状态）+ L105 的动机句。
4. **受扰链路容量算子**（若要加"链路性能退化"实验条件，这是现成写法）：L54 公式 (3) 逐字 `C _ { i j } = W _ { i j } \mathrm { l o g } _ { 2 } \left( 1 + \frac { ( p _ { i } { f _ { i } } ^ { 2 } ) / { d _ { i j } } ^ { 2 } } { n _ { 0 } W _ { B } ( 4 \pi / c ) + ( p _ { \chi } { f _ { \chi } } ^ { 2 } ) / { d _ { i j } } ^ { 2 } } \right) ,\`；配合公式 (4) L60 `\mu _ { i j } \leq C _ { i j } \cdot \sum _ { b \in B } \lambda _ { i j } ^ { k } [ b ] .\`

### 12) 实验合同里与"负载"相关的设置（仅登记，非贡献）
- 星座：550 km / 7 轨 / 每轨 25 星 / 倾角 53° / 最小仰角 25°（L179）；仿真用 175 颗（L177）。
- **10 档负载扫描**（本批唯一）：L192 — "the two algorithms are simulated under the load of 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000 packets, and multiple rounds of tests are conducted under each load."
- 流量形态：L188 — "many packets are generated on the network (network load), each with a random source and destination node."
- 压力条件：L188 — "In the simulations, the presence of sweeping jamming in the environment causes the link performance degrade."
- 指标：平均 AoI（Fig.3）+ 时延抖动，公式 (12) L206 `\tau _ { [ s l , d l ] } = \frac { A o I _ { j } - A o I _ { i } } { j - i }\`；L203 — "It is obtained by dividing the delay time difference of adjacent packets by the difference of packet sequence number, or by the information age difference of adjacent packets."
- 对比算法 SPF（L188）。
- 报告口径（登记）：L192 — "the RRS-DRL algorithm can still maintain relatively low delay with the increase of load, and the results are stable"；交叉点 L192 — "Although, the SPF algorithm performs well when the number of loads is less than 2500 packets, as the number of loads continues to increase, the age of the full network information is higher compared to the RRS algorithm."

---

## 3. YI9G7NR7 — DQDRA: A Dyna-Q-Enhanced Distributed Routing Algorithm for Heterogeneous LEO Constellations

（IEICE Trans. Fundamentals LETTER，DOI 10.1587/transfun.2026EAL2018；正文 L1–L167，References L168–L195 未逐条读）

### 1) MDP 定义
- 形式为 **POMDP**：L109 — "We formulate the problem as a Partially Observable Markov Decision Process (POMDP) defined by the tuple \( S , \mathcal { A } , P ( s , a ) , \mathcal { R } ( s , a ) )\ . S is the state space, \mathcal { A }\ is the action space and \P ( s , a )\ and \{ \mathcal { R } } ( s , a )\ are the state-transition probabilities and its reward function. At each time \t ,\ the \v _ { i }\ takes an action \^ { a _ { t } , }\ observes the reward \r _ { t }\ , and enters a new state \s _ { t + 1 }\"
- **状态 s_t（逐字段）**：L111 — "We define the state space of agent 𝑖 as \{ \sf S } _ { i } = \{ L _ { i } , N _ { i } \}\ where \L _ { i }\ is the local information of 𝑖 and \N _ { i }\ is the information received from its neighboring satellites. \L _ { i }\ denotes the destination information extracted from the packet header. \N _ { i }\ reflects the link quality and buffer congestion state, encoded with two bits. Specifically, \s _ { t } = 0 0 , 0 1 , 1 0\ , and 11 correspond to four queue-occupancy levels: 0-20% as an uncongested state, 20-80% as a lightly loaded state, 80-100% as a heavily loaded state, and an unavailable link."
  维度：\N_i\ = **2 bit 离散档**；\L_i\ = 目的标识；**无需归一化**（已离散化）；**无时间聚合**。动作空间 = "selecting the next hop, either a neighboring satellite via ISL or CLL, or a link to a ground station"（L111）。**无动作掩码变量**；"unavailable link" 被编码进状态（\s_t=11\）而非屏蔽动作。
  ⚠ 原文符号冲突（照抄不改）：\L_i\ 同时被称作 "the local information of i" 与 "the destination information extracted from the packet header"。
- **奖励 r_t**：公式 (7) L116 逐字：
  `r _ { t } = \left\{ { \begin{array} { l l } { r _ { \mathrm { d } } , } & { { \mathrm { w h e n ~ r e a c h i n g ~ t h e ~ d e s t i n a t i o n } } } \{ r _ { \mathrm { l o o p } } , } & { { \mathrm { w h e n ~ e n t e r i n g ~ a ~ l o o p } } } \{ r _ { \mathrm { q u e u e } } + r _ { \mathrm { d i s t } } , } & { { \mathrm { o t h e r w i s e } } } \end{array} } \right.\
  分项公式 (8)(9) L120/L124 逐字：
  `r _ { \mathrm { q u e u e } } = w _ { 1 } \cdot \left( 1 - e ^ { t _ { q } ( j ) } \right)\ ／ `r _ { \mathrm { d i s t } } = w _ { 2 } \cdot \frac { | | i d | | - | | j d | | + | | s d | | } { | | s d | | }\
  说明 L127 — "where \w _ { 1 }\ and \w _ { 2 }\ are weighting coefficients, \t _ { q } ( j )\ is the time spent in the queue, and \r _ { \mathrm { l o o p } }\ and \r _ { \mathrm { d e l } }\ are additional penalties or rewards for loops and successful delivery. The first exponential term increases the penalty rapidly as the queueing delay grows. The second term, based on the slant range, measures and normalizes the distance toward the destination."
  ⚠ **三处原文不一致（登记，不改写）**：(a) \r_{\mathrm{queue}}=w_1(1-e^{t_q(j)})\ 在 \t_q>0\ 时为负且指数增长，与 "increases the penalty rapidly" 语义一致但**式中无负号**；(b) L127 提到 \r_{\mathrm{del}}\，公式 (7) 用的是 \r_{\mathrm d}\；(c) \w_1,w_2,r_{\mathrm d},r_{\mathrm{loop}}\ **取值全文未给**。
- **折扣 \gamma\**：L150 — "where 𝛾 is the discount factor."；**取值未给**。
- **转移/终止**：无 episode 边界定义（只有"到达目的地"分支与"进入环"分支）；缓冲满则丢包 L70 — "the satellite enqueues it if buffer space is available; otherwise dropped"，**丢弃后如何终止未定义**。**无资格迹/n 步**（第 10 项计数）。

### 2) 学习算法与更新式
- 算法名 **Dyna-Q**：L142 — "Dyna-Q is a model-based RL algorithm that improves policy learning by combining real experiences with simulated experiences generated from the learned model. In each step, a previously visited state 𝑠 is selected. An action 𝑎 that was previously executed in this state is chosen. The model predicts the next state \s ^ { \prime }\ and reward 𝑟. The simulated transition \( s , a , r , s ^ { \prime } )\ is then used to update the action-value function with the Dyna-Q rule."
- **更新式** 公式 (10) L147 逐字：
  `\begin{array} { r l } & { \mathcal { Q } _ { i } ^ { \ast } ( s _ { t } , a _ { t } ) = ( 1 - \alpha ) \mathcal { Q } _ { i } ( s _ { t } , a _ { t } ) } \& { \qquad + \alpha \big [ r _ { t } + \gamma \underset { a ^ { \prime } } { \operatorname* { m a x } } \mathcal { Q } _ { j } ( s _ { t + 1 } ^ { \prime } , a _ { t } ^ { \prime } ) \big ] } \end{array}\
  ⚠ **关键逐字细节**：TD 项取 max 的是**邻居 j 的 Q 函数** \mathcal{Q}_j\（不是 \mathcal{Q}_i\），与本批 47J2H748 的 Q-routing \Q_y(d,z)\ 同源；原文未解释该跨节点索引。
- 策略读出 L150 — "During exploitation, the agent selects \a _ { t } ^ { * } = \arg \operatorname* { m a x } _ { a _ { t } \in \mathcal { A } } Q ( s _ { t } , a _ { t } )\ , which is the action estimated to maximize the long-term cumulative reward."
- **网络结构：无神经网络**——表格型 Q（图题 L105 "Fig. 4: Q-Table update process in DQDRA"；基线描述 L156 "each satellite maintains a Q-table"）。**无 target net / replay / double**（第 10 项计数）。
- 探索：L144 — "The agent explores with probability 𝜖 new paths, and with probability \( 1 - \epsilon )\ chooses the one that maximizes the expected reward."；表 1（L140）"Probability €" = 0.1（MinerU 把 \epsilon\ 转成 €）。
- **Dyna-Q 的模拟步数 n、模型形式、模型更新规则全文未给**——复现关键缺口。

### 3) 信用分配
- **逐跳即时奖励，按三种结局分流**（公式 7）：投递成功 \r_{\mathrm d}\ / 进入环 \r_{\mathrm{loop}}\ / 常规推进 \r_{\mathrm{queue}}+r_{\mathrm{dist}}\。**这是本批中对"失败原因"区分度最高的一处**（成环 vs 成功 vs 常规）。
- 分项归因：\r_{\mathrm{queue}}\ 归因到**下一跳 j 的排队时间** \t_q(j)\；\r_{\mathrm{dist}}\ 归因到**下一跳相对源/目的的几何进展** \||id||-||jd||+||sd||\ 归一化于 \||sd||\（L124）。
- **无路径级终局回报分解**、无逐跳折扣分摊机制。

### 4) 状态里有没有时间信息
- **没有**。状态仅 \{L_i,N_i}\，\N_i\ 是 2-bit 队列占用档（L111）。检索 \grep -ciE "EWMA|exponential moving|moving average|history|historical|previous state|trend"\ → **0 命中**。
- 时间只出现在奖励（\t_q(j)\、成环判定）与更新式的下标 \s'_{t+1}\ 中。

### 5) 动作有没有时间结构
- **逐包逐跳**，每步 argmax（L150）。
- **无动作驻留/流级缓存/切换代价**（同类检索 0 命中）。
- **触发式转发**：L70 — "Whenever the buffer is non-empty and at least one outgoing link is idle, the satellite dequeues the head-of-line packet and forwards it to the selected neighboring node according to the routing algorithm."

### 6) 多智能体设定
- **完全分散**：L15 — "we design a Dyna-Q-Enhanced Distributed Routing Algorithm (DQDRA), a fully decentralized reinforcement learning(RL) approach that enables each satellite to autonomously make low-delay next-hop decisions without requiring global network state."
- 局部观测：L109 — "Each satellite obtains only local observations of the network environment. These observations are derived from its own queue state, link conditions, and limited information exchanged with neighboring nodes."
- **有一跳邻居信息交换**（\N_i\ 的定义即 "information received from its neighboring satellites"，L111）；**无参数共享声明、无非平稳处理、无动作同步**。

### 7) 训练协议
- 拓扑 L154 — "we consider a heterogeneous LEO constellations with the following parameters: 1000 km, 60<sup>◦</sup>: 1000/36/1, and 500 km, \7 5 ^ { \circ } { \mathrm { : } }\ : 300/15/1."
- 训练与评估同分布：收敛曲线在 \ell=0.8\ 下测（L158 图题），性能扫描 \ell\ 0.5→0.9（L160 — "under stationary network conditions as the trafic load ℓ increases from 0.5 to 0.9"）。
- 训练量：**无步数/时长**；只有 episode 口径 L158 — "The baseline distributed method requires 240 episodes to approach its steady-state... In contrast, DQDRA converges faster with average E2E latency stabilizing at episode 160, about 33% faster than the baseline distributed method."
- 对比算法 L156：(a) Centralized（Dijkstra，边权 \w_{i,j}=\frac{1}{R(i,j)}\）；(b) Baseline distributed（"a model-free RL approach in which each satellite maintains a Q-table. Packets are forwarded to the neighbor with the highest Q-value."）。**消融轴正是"加不加模型生成的模拟经验"**。

### 8) 该文的算法贡献
- L29 — "this paper proposes an optimal time-matching algorithm for CLL establishment and a Dyna-Q-Enhanced Distributed Routing Algorithm (DQ-DRA)."
- L158（Dyna-Q 侧）— "This improved convergence performance stems from the Dyna-Q framework, which augments real transition experiences with model-generated simulated samples, enabling more eficient exploration and accelerated policy improvement."
- L102（CLL 时间匹配侧，**非 RL 部分**）— "The algorithm fully exploits the characteristics of the heterogeneous constellation by solving for the minimum sufficient cross-layer contact duration that meets the traffic demand, thereby distributing traffic more evenly..."；其选择式 L95 公式 (6) `i ^ { * } = \arg \operatorname* { m i n } _ { v _ { j } \in C _ { i } } \tau ( i , j )\
- 对应：① 状态简化为 2-bit 队列档 + 包头目的信息（第 1 项）；② 三段式奖励含成环惩罚（第 1、3 项）；③ Q-learning → Dyna-Q（第 2 项）；④ 本地 Q 表 + 一跳邻居信息（第 6 项）。

### 9) 该文自述的局限
- L162 — "The proposed DQDRA trades increased algorithmic complexity for improved routing performance under high traffic loads. While this may lead to marginal performance degradation in lightly loaded networks, it enables significantly better scalability, adaptability, and latency reduction in heterogeneous LEO constellations."
- L166 — "Future work will focus on ensuring QoS under link failure scenarios."

### 10) 该文没有考察的算法选择
**检索范围 = 该篇 MD 全文 195 行**：

| 模式 | 计数 | 判读 |
|---|---|---|
| \grep -ciE "multi-?agent\|decentraliz\|decentralis"\ | **2** | **有命中，构不成反例**：L15 是本文自述 "fully decentralized"（性质描述）；L184 是**参考文献 [8]** IEEE TCOM 的题目 "…multi-agent deep reinforcement learning approach"。二者都不是本文的多智能体机制 |
| \grep -ciE "target network\|target q\|replay\|experience pool\|double q\|double dqn"\ | **0** | 无 replay/target net/double |
| \grep -ciE "EWMA\|exponential moving\|moving average\|history\|historical\|previous state\|trend"\ | **0** | 状态无时间历史 |
| \grep -ciE "action mask\|invalid action\|impossible action\|mask"\ | **0** | 无掩码 |
| \grep -ciE "eligibility\|n-step\|multi-step\|multistep"\ | **0** | 无资格迹/n 步 |
| \grep -ciE "discount\|gamma"\ | **2** | L150 定义 + L147 公式内 |

1. **Dyna-Q 自身超参与模型**：模拟步数 n、模型形式、模型更新规则全文未给 → 不可复现。
2. 函数近似 / 状态泛化：无神经网络（纯 Q 表）。
3. Double / replay / target net：未考察。
4. **动作掩码 vs 状态编码**：把"不可用链路"编码成 \s_t=11\ 是一种设计，但未与掩码方案对比。
5. QoS / 链路失效：作者自述为 future work（L166）。
6. 参数共享 / 非平稳 / 动作同步：无相关机制。

### 11) 可复用的具体机制
1. **2-bit 队列占用档同时编码"拥塞程度 + 可用性"**（L111）：\s_t=00,01,10,11\ ↔ 0-20% / 20-80% / 80-100% / 链路不可用。信令开销极低，适合卫星间仅允许极窄带信令的设定。
2. **三段式奖励 + 显式成环惩罚**（公式 7）：把"进入环"单列为奖励分支 \r_{\mathrm{loop}}\，与"投递成功" \r_{\mathrm d}\ 分开——本批中对失败类型区分度最高的一处。
3. **队列惩罚用指数而非线性**：\r_{\mathrm{queue}}=w_1(1-e^{t_q(j)})\（公式 8）。
4. **以源-目的斜距归一化的进展项**：\r_{\mathrm{dist}}=w_2\frac{||id||-||jd||+||sd||}{||sd||}\（公式 9），量纲无关。
5. **Dyna-Q 收敛效率的可复用度量**：以"到达稳态所需 episode 数"对比（240 → 160，33% faster，L158）。
6. **邻居回传式 TD 目标**：\\mathcal{Q}_j(s'_{t+1},a'_t)\（公式 10）——一行信令换取一跳的 bootstrapping 估计。

### 12) 实验合同里与"负载"相关的设置（仅登记，非贡献）
- 拓扑：1000 km/60°：1000/36/1 与 500 km/75°：300/15/1（L154）。
- 参数表（L140）：天线半锥角 55°、地面站最小仰角 15°、卫星发射功率 20 W、地面站 50 W、ISL/CLL/S2G 载频 18/40/65 GHz、**Traffic Load l = 0.5 to 0.9**、Probability € = 0.1、系统带宽 800 MHz、包长 64 kbit。
- **无量纲负载定义（本批唯一）**：L70 — "Let \dot { \lambda } ^ { ( v _ { R } ) }\ denote the packet generation rate at each remote-sensing satellite and \lambda ^ { * }\ represent the maximum aggregate traffic load sustainable by the network calculated from the \varepsilon _ { S 2 G }\ rate. We define the network traffic load as \ell = \sum _ { v _ { R } \in \mathcal { V } _ { R } } \lambda ^ { ( v _ { R } ) } / \lambda ^ { * }\"
- 队列规则：L70 — "Each satellite maintains a transmission buffer of maximum capacity \Q _ { \mathrm { m a x } }\ and operates under a First-In-First-Out (FIFO) policy. Upon receiving a packet \p ( d )\ destined for ground station \d ,\ the satellite enqueues it if buffer space is available; otherwise dropped."（\Q_{\max}\ 数值未给）
- 指标：E2E 时延公式 (5) L80 `L ( i , j ) = \frac { q _ { i } \cdot B } { R ( i , j ) } + \frac { B } { R ( i , j ) } + \frac { \| i j \| } c\`；投递成功率 L154 — "The delivery success rate is defined as \frac { p _ { \mathrm { s u c c e s s } } } { p _ { \mathrm { a l l } } }\"
- 报告口径（登记）：L160 — \ell=0.8\ 时 DQDRA 平均 E2E 时延 241 ms vs centralized 266 ms / baseline distributed 256 ms，成功率 98.6%；\ell=0.9\ 时相比两基线降时延 27.6% / 18.6%、提成功率 8.4% / 15.0%。

---

## 4. X5Z98UPM — DRL-Based Load-Balancing Routing Scheme for 6G Space–Air–Ground Integrated Networks（DQN-LLRA）

（通读 L1–L341 正文全部；L342–L433 为 References，未逐条精读。本地副本与 VM 副本 md5 相同：`3f9d6706e874e1fdb93812ff3ffc709b`，均 433 行。）

### 1) MDP 定义
- 声明：L46 — "(1) The satellite routing process is modeled as a Markov decision process (MDP) [6], and its state space, decision space, and reward function are defined."；L112 — "The Markov decision process is a mathematical framework used to model decision-making processes, where only the immediate state affects the outcome of a current decision, rather than previous states."
  \grep -n -i "transition probability"\ → **0 命中**（未给 \P(s'|s,a)\，也未给排队/拓扑演化方程）。
- **状态 s_t（逐字段）**：L123 逐字 — "(1) The state space: The state of satellite node i at time t is represented as \S _ { t } ^ { i } ,\ , where \S _ { t } ^ { i } = \{ D _ { i j } , B _ { i j } , C _ { i } , \hat { C } _ { j } , Q U _ { j } , d o n e \}\ , with \j = 1 , 2 , 3 , 4 .\"
  逐字段（同一句内）：\D_{ij}\ = "the delay of the intersatellite link between node i and neighboring node j"；\B_{ij}\ = "the bandwidth of the inter-satellite link between node i and neighboring node j"；\C_i\ = "the shortest hop count from the current node i to the destination node"；\C_j\ = "the shortest hop count from neighbor node j to the destination node"；\QU_j\ = "the queue utilization of neighboring node \j ,\ which indicates a load of node j."；\done\ = "a two-valued Boolean number that indicates whether the current node is the destination node or not."
  \QU\ 定义式 L103：`Q U _ { i } = { \frac { \mathrm { N u m b e r ~ o f ~ p a c k e t s ~ i n ~ q u e u e ~ o f ~ n o d e ~ } i } { \mathrm { T o t a l ~ q u e u e ~ s i z e ~ o f ~ n o d e ~ } i } } .\`
  维度：**未给**（\grep -n -i "dimension"\ → 0；"vector" → 0）。归一化：**未声明**（\grep -n -i "normaliz"\ → 0；"normalis" → 0）。随时间聚合：**否**（见第 4 项）。
  势函数来源 L123 — "\C _ { i }\ and \C _ { j }\ are calculated by the shortest path algorithm, \mathrm { i . e . , }\ the Dijkstra algorithm."；动机 L123 — "The pair of numbers \C _ { i } , C _ { j }\ was introduced to enhance the algorithm's convergence rate and avoid undesired ping-pong routing."
- **动作 a_t**：L125 — "(2) The action: The action of the current satellite node i is expressed as \a _ { i } = \{ { \mathrm { n e i g h b o r } } _ { j } \}\ \j = 1 , 2 , 3 ,\ 4..."→ 离散、|A|=4。**无掩码**（\grep -n -i "mask"\ → 0；"masking" → 0；"invalid action" → 0）；L95 却明说 ISL "最多 4" 且极缝无直连但**未给邻居不足 4 时的兜底**。
- **奖励 r_t**：四段式公式 (2) L130 逐字：
  `r _ { i } = \left\{ \begin{array} { l l } { \alpha _ { 1 } \frac { C _ { i } - C _ { j } } { p } + \beta _ { 1 } ( 1 - Q U _ { j } ) + \gamma _ { 1 } \frac { D _ { i j } } { q } + \omega _ { 1 } \frac { B _ { i j } } { o } , C _ { i } \leq C _ { j } , Q U _ { j } \leq 0 . 5 } \{ \alpha _ { 2 } \frac { C _ { i } - C _ { j } } { p } + \beta _ { 2 } ( 1 - Q U _ { j } ) + \gamma _ { 2 } \frac { D _ { i j } } { q } + \omega _ { 2 } \frac { B _ { i j } } { o } , C _ { i } \leq C _ { j } , Q U _ { j } > 0 . 5 } \{ \alpha _ { 3 } \frac { C _ { i } - C _ { j } } { p } + \beta _ { 3 } ( 1 - Q U _ { j } ) + \gamma _ { 3 } \frac { D _ { i j } } { q } + \omega _ { 3 } \frac { B _ { i j } } { o } , C _ { i } > C _ { j } , Q U _ { j } \leq 0 . 5 } \{ \alpha _ { 4 } \frac { C _ { i } - C _ { j } } { p } + \beta _ { 4 } ( 1 - Q U _ { j } ) + \gamma _ { 4 } \frac { D _ { i j } } { q } + \omega _ { 4 } \frac { B _ { i j } } { o } , C _ { i } > C _ { j } , Q U _ { j } > 0 . 5 } \end{array} \right. ,\
  系数约束 L133 — "\alpha _ { i } + \beta _ { i } + \gamma _ { i } + \omega _ { i } = 1 . \ o , p ,\ and \q\ are adjustment factors, which keep each state value at the same order of magnitude."；**取值**（L261 表 1）：0.45,0.35,0.1,0.1 / 0.50,0.30,0.1,0.1 / 0.40,0.40,0.1,0.1 / 0.50,0.30,0.1,0.1；\o,p,q\ = 10,20,20。
  终点覆盖式公式 (3) L136：`r _ { t } = \left\{ \begin{array} { l l } { 1 , d o n e = T r u e } \{ r _ { t } , d o n e = F a l s e } \end{array} \right. .\；折扣累积公式 (4) L142：`R _ { t } = \sum _ { t = 0 } ^ { \infty } \gamma ^ { t } r _ { t + 1 } ,\；折扣 \gamma\ = 0.99（L256/L261）。
- **转移/终止**：L173–174 算法第 9–10 步 "if next node is destination then / \y _ { t } = r _ { t }\ "；episode 结构 L165 "1: for episode = 1 to M do"、L168 "4: for step = 1 to k do"——**M 与 k 的数值全文未给**。**无资格迹/n 步**（\eligibility\→0；"n-step"→0；"multi-step"→0；"lambda"→0）。**无超时/TTL 终止**（"timeout"→0；"TTL" 唯一命中为 L296 "little" 子串）。

### 2) 学习算法与更新式
- 算法名 DQN-LLRA：L48 — "(2) A Deep Q-Network (DQN)- [7] based load-balancing routing algorithm for LEO satellites (DQN-LLRA) is proposed."
- **损失** 公式 (6) L232 逐字：`L = \frac { 1 } { N _ { b } } { \sum _ { t } { \left( y _ { t } - Q ( s _ { t } , a _ { t } \Big | \theta ^ { Q } ) \right) } ^ { 2 } } .\
- **TD 目标** 公式 (7) L238 逐字：`y _ { t } = r _ { t } + \gamma \operatorname* { m a x } _ { a _ { t + 1 } } Q ^ { \prime } ( s _ { t + 1 } , a _ { t + 1 } \Big | \theta ^ { Q ^ { \prime } } ) ,\
- **参数更新** 公式 (8) L246 逐字：`\theta _ { t + 1 } ^ { Q } = \theta ^ { Q } + \alpha [ r _ { i } + \gamma \operatorname * { m a x } _ { a _ { i + 1 } } Q ^ { \prime } ( s _ { i + 1 } , a _ { i + 1 } \Big \vert \theta ^ { Q ^ { \prime } } ) - Q ( s _ { i } , a _ { i } \big \vert \theta ^ { Q } ) ] \nabla Q ( s _ { i } , a _ { i } \big \vert \theta ^ { Q } ) ~ .\
- **target net**：有，周期硬复制——L181 "17: Update the target Q network every C steps, let \theta ^ { Q } = \theta ^ { Q ^ { \prime } }\"；**C 取值未给**。**Double：无**（\grep -n -i "double"\ → 0）。**软更新/Polyak：无**（→0）。**优先回放：无**（\prioritiz\ → 0）。
- **网络结构** L256 — "The DQN algorithm in this paper was configured with a neural network that consisted of an input layer, an output layer, and two hidden layers."；**宽度未给**（"neuron"→0）、**激活未给**（"activation"→0；"ReLU"→0）；回放池 4000；输入 (s,a)、输出 Q(s,a)（L211）。**无图算子**（"convolution"→0）。
- **探索**（公式 (5) L155 逐字，注意采样用 target 网 argmax）：`\pi _ { i } = \left\{ \begin{array} { l l } { \mathrm { r a n d o m a c t i o n w i t h ~ p r o b a b i l i t y } e ^ { - s t e p s \cdot 0 . 4 } } \{ \mathrm { a r g } \underset { a _ { t + 1 } } { \mathrm { m a x } } Q ^ { \prime } ( s _ { t + 1 } , a _ { t + 1 } \Big \vert \theta ^ { Q ^ { \prime } } ) \mathrm { w i t h } \mathrm { p r o b a b i l i t y } 1 - e ^ { - s t e p s \cdot 0 . 4 } } \end{array} \right. ,\；学习率 \alpha\=0.005（L261）。
- **原文内部不一致（登记）**：(a) L180 损失的自变量写作 \(s_{t+1},a_{t+1})\，公式 (6) 写作 \(s_t,a_t)\；(b) L158/L218 称存四元组，L172 第 8 步存五元组 \(s_t,a_t,r_t,s_{t+1},done)\；(c) L243 称更新式为 "Equation (4)"，实际标 \\tag{8}\。

### 3) 信用分配
- **逐跳即时奖励：是**。L127 — "The reward value was calculated by the reward function when the current agent made a decision, and the state transition occurred."
- **路径级终局：仅终点 +1**（公式 3 L136 + L139）。
- **是否分解到节点/链路**：语义上分到邻居 \QU_j\ 与链路 \D_{ij},B_{ij}\（L133），但**无显式回报分摊机制**：\grep -n -i "credit"\ → 0；"blame" → 0；"decompos" → 0；"shapley" → 0；"per-hop"/"per hop" → 0。
- **是否区分损失原因**：**只区分两类二值状况**——(i) 跳数是否向终点推进（\C_i\leq C_j\ / \C_i>C_j\），(ii) 邻居是否拥塞（\QU_j\leq 0.5\ / >0.5），由此得四段权重（L130/L133）。**没有**针对丢包/排队溢出/链路失效/能量的分项惩罚（\grep -n -i "failure"\ → 1 命中，为 L74 相关工作转述）。
- 跨跳信用靠 \gamma\=0.99 与 target 网 bootstrap（L142/L238）。

### 4) 状态里有没有时间信息
**没有**（检索范围：全文 433 行）：\historical\→0；\history\→0；\EWMA\→0；\exponential\→0；\moving average\→0；\window\→0；\differential\→0；\LSTM\→0；\GRU\→0；\convolution\→0；\trend\→1 命中（L263 图题，训练曲线）；\attention\→1 命中（L36 普通用法）。
显式"瞬时性"表述 L112（见第 1 项）；状态里唯一的"差"是跳数差（空间，非时间），L123 — "When \C _ { i } - C _ { j } > 0 ,\ , the reward function gave positive feedback. When \C _ { i } - C _ { j } \leq 0 .\ , the reward function gave negative feedback."

### 5) 动作有没有时间结构
- **每包/每节点独立决策**：L209 — "each node needed to send the current data packet to a suitable node among the four surrounding nodes according to the current service requirement."；L186 — "The algorithm checked whether the next node was the destination node. If it was, the decision-making process was completed, and the path is output."
- **无驻留/迟滞/切换代价**：\dwell\→0；\hysteresis\→0；\handover\→0；\switch\→2（均在参考文献）。
- **无流级缓存/摊销**：\amortiz\→0；\per-packet\/\per packet\→0。
- 唯一带时间索引的是训练期探索衰减 \e^{-steps\cdot 0.4}\（L155/L158）。

### 6) 多智能体设定
- **"每个决策卫星即一个 agent"**：L112 — "In our approach, each decision-making satellite was treated as an agent and interacted with the surrounding nodes to gather information about the current state in order to make informed routing decisions."；L296 — "In the DQN-LLRA scheme, each routing node is controlled by a DQN agent"。
- 观测仅局部：L48 — "The algorithm relies only on the state information of the surrounding nodes of the current satellite node"；L209 — "the current satellite could only receive the status of the four surrounding nodes and links."
- **参数是否共享：全文未声明**（\parameter sharing\→0；\shared parameter\→0；\identical\→0；\same network\→0）。
- **非平稳：无讨论**（\non-stationar\→0）；**无智能体间学习通信**（\message passing\→0；\communication overhead\→0）；**无动作同步**（\synchron\ 3 命中均为 time-sensitive/Geosynchronous/参考文献）。

### 7) 训练协议
- 拓扑 L95 — "the Iridium constellation has six polar orbits, and 12 LEO satellites are distributed on each orbit... In total, there are \6 \times ( 1 1 + 1 ) = 7 2\ satellites"；生成方式 L251 — "the Iridium satellite topology was generated by using the official satellite data files of the Iridium constellation and Python networkX."；链路参数随机 L251 — "the delay and bandwidth were randomly generated for each inter-satellite link."（表 1：10–20 ms / 10 Mbps）。
- 负载变化方式 L251 — "70 streams of data flow were generated in a loop at the same time to propagate in the topology, so that the agent could obtain dynamic queue utilization and link bandwidth."
- episode 采样 L152 — "The Iridium satellite topology constellation randomly generated source and destination node pairs, and the routing decision was made by the source node acting as the agent with an initialized state."；**M/k 未给**。
- **训练分布 vs 评估分布：未声明差异，也无迁移测试**（\generaliz\→0；\unseen\→0；\held-out\→0；\test set\→0；\split\→0；\curriculum\→0）。
- 训练量 L256 — "trained the network with 10,000 randomly generated data streams"；平台 Win11 + PyTorch + Python3.9（L251）。评估规模 L271 — "100 pairs of the source and destination nodes were generated... For each algorithm, 100 routing paths were calculated, resulting in a total of 400 paths."

### 8) 该文的算法贡献
- L46 — "(1) The satellite routing process is modeled as a Markov decision process (MDP) [6], and its state space, decision space, and reward function are defined."
- L48 — "(2) A Deep Q-Network (DQN)- [7] based load-balancing routing algorithm for LEO satellites (DQN-LLRA) is proposed."
- 对应：① 状态里塞入 Dijkstra 跳数势 \(C_i,C_j)\ 与邻居队列利用率 \QU_j\（第 1 项，L123）；② 奖励按 \C_i\ 相对 \C_j\ 的符号与 \QU_j\ 对 0.5 的门槛切成四段（第 1、3 项，L130）；③ 学习算法**本身是标准 DQN**（回放 + 周期硬复制 target 网 + 逆步数指数衰减探索），无新算子（L211/L256/L155/L181）；④ 每节点一个 agent、仅用四邻居局部状态（第 6 项）。

### 9) 该文自述的局限
- L296 — "This paper also found that when the number of satellite nodes increased to thousands, the routing path exceeded 20 hops, and then the convergence speed of the DQN-LLRA algorithm decreased, and the accuracy of the decision model also decreased. Therefore, using more effective neural network structures such as Graph Neural Networks (GNN) for network feature extraction is an important direction for future research."
- L298 — "Although the proposed load-balancing routing algorithm for LEO satellites based on Deep Q-Network shows promising performance improvements compared to traditional routing algorithms, there are still some limitations and areas for further research. Firstly, the proposed algorithm is evaluated through simulations, and it remains unclear how well it would perform in real-world scenarios... Secondly, the proposed algorithm considers delay, bandwidth, and queue utilization of the surrounding satellite nodes as factors for selecting the best routing results. Other factors, such as link reliability, congestion level, and energy efficiency, may also be considered in future work. Lastly, while deep reinforcement learning has shown great potential in improving network routing, it is a computationally expensive approach that requires significant training time and resources..."

### 10) 该文没有考察的算法选择
检索范围 = 全文 433 行；逐条模式与实测计数（凡有命中均说明为何不构成反例）：

| 模式 | 计数 | 判读 |
|---|---|---|
| \grep -n -i "double"\ | **0** | 无 Double DQN |
| \grep -n -i "dueling"\ | **0** | 无 Dueling |
| \grep -n -i "prioritiz"\ / "prioritized"\ | **0** | 无优先回放（注：此模式**刻意排除裸 "priorit"**，避免命中散文词） |
| \grep -n -i "soft update"\ / "polyak"\ / "tau"\ | **0** | 无软更新 |
| \grep -n -i "n-step"\ / "multi-step"\ / "eligibility"\ / "lambda"\ | **0** | 无多步/资格迹 |
| \grep -n -i "mask"\ / "masking"\ / "invalid action"\ | **0** | 无动作掩码（而 L95 明说 ISL 最多 4、极缝无直连） |
| \grep -n -i "parameter sharing"\ / "shared parameter"\ / "decentralized"\ / "non-stationar"\ / "message passing"\ | **0** | 无参数共享/CTDE/非平稳/通信 |
| \grep -n -i "normaliz"\ / "normalis"\ | **0** | 无状态归一化（仅奖励侧 o,p,q 量级对齐） |
| \grep -n -i "handover"\ / "hysteresis"\ / "dwell"\ | **0**；\switch\ **2** | 切换/驻留未考察（"switch" 两处均在参考文献） |
| \grep -n -i "transition probability"\ / "arrival"\ / "Poisson"\ | **0** | 未建模排队动力学/到达过程 |
| \grep -n -i "ablation"\ → 0；"baseline"\ → 0 | **0/0** | 四段权重与 0.5 门槛**未做敏感性/消融**（仅 L267/L269 "benchmark" 2 次） |
| \grep -n -i "attention"\ → **1** | **1** | **有命中，不构成反例**：L36 "gained significant attention and interest in recent years"，普通英文用法，非注意力机制 |
| \grep -n -i "trend"\ → **1** | **1** | **有命中，不构成反例**：L263 图题 "Figure 11 shows the variation trend of the reward..."，训练曲线描述 |

### 11) 可复用的具体机制
1. **跳数势 shaping 防乒乓**：状态放 \(C_i,C_j)\（Dijkstra 计算，L123），奖励第一项 \alpha_k\frac{C_i-C_j}{p}\（L130），符号语义 L123。
2. **以邻居队列 0.5 为门槛的四段权重**（公式 2 + L261 实测取值）。
3. **量级对齐因子 \o,p,q\**：L133 — "adjustment factors, which keep each state value at the same order of magnitude."（取值 10,20,20）
4. **逆训练步数指数衰减探索** \e^{-steps\cdot 0.4}\（L155）。
5. **最小局部状态集**：\S _ { t } ^ { i } = \{ D _ { i j } , B _ { i j } , C _ { i } , \hat { C } _ { j } , Q U _ { j } , d o n e \}\（L123）。
6. **负载感知的对照构造**（Dijkstra-QU）L267 — "The Dijkstra-QU algorithm was used to find the shortest path after transforming the queue utilization into the link weight."

### 12) 实验合同里与"负载"相关的设置（仅登记，非贡献）
- 拓扑：Iridium \6\times(11+1)=72\ 星（L95/L251）；链路时延 10–20 ms 随机、带宽 10 Mbps（L261）。
- **负载模型**：L251 — "70 streams of data flow were generated in a loop at the same time to propagate in the topology"；**无到达过程**（\arrival\→0；\Poisson\→0；\traffic intensity\→0）。
- 训练负载量：10,000 条随机数据流（L256）。
- 评估：100 组源宿对 / 每算法 100 条路径 / 共 400 条（L271）。三张图题均写 "under various test flows"（L278/L281/L286），但**负载档位数值正文未给**。
- 对比算法（L267）：Dijkstra、Dijkstra-QU、Q-learning（来自 [45]）、DQN-LLRA。
- 公平性设定 L269 — "we decreased the bandwidth around the decision node in both the Q-Learning-based intelligent routing scheme and the proposed routing scheme. This promoted the fairness of the comparison with other benchmark algorithms."
- 指标：路径时延、路径最大队列利用率、路径平均队列利用率（L273/L283/L288）。
- 报告数字（登记）：L15/L292 — 相对 Q-learning 基线，最大队列利用率降 5%、平均降 13%；相对 Dijkstra，最大降 8%、平均降 15%。

---

## 5. 8N9QJHC2 — Recovery Routing Based on Q-Learning for Satellite Network Faults（IDBB 检测 + MFDR 抗毁路由）

（正文 L1–L375 逐行读完；L376–L439 为参考文献表，未逐条读。**RL 主体在 Section 4（L174–L272），但其"动作来源"完全由 Section 3 的故障检测结果驱动**。）

### 1) MDP 定义
- **状态 s_t（逐字段，仅 2 个）**：L184 — "The state space is a two-dimensional state space \( n _ { i } , d _ { k } )\ The current node \n _ { i }\ and the destination node \d _ { k }\ jointly describe the system state."；L31 — "The collected information is used to update the Q-value table composed of two-dimensional state space and one-dimensional action space."；L227 — "\d _ { k } \colon\ Destination nodes, including \d _ { 1 }\ and \d _ { 2 } ;\ the specific number depends on the number of network nodes."
  维度：2 个离散节点标识；**无归一化**（\grep -n -i -E 'normaliz|scal'\ → 4 命中，L39/L286/L300/L302，全部与状态无关）；**无时间聚合**。
- **动作 a_t**：L186 — "The action space is \Y ( V , n _ { i } )\ , which is composed of the neighboring node set of the current node \n _ { i }\"；L225 — "\y _ { z } \mathrm{:}\ Neighbors of node \n _ { i } ,\ including \y _ { 1 }\ and \y _ { 2 } ;\ the specific number depends on the number of neighbors of node \n _ { i }\"。**无 mask 变量**（\grep -n -i -E 'mask|feasible|invalid'\ → 0），但有**值级硬屏蔽**（见下）。值域约束公式 (13) L216：`Q _ { i } \left( d _ { k } , y _ { z } \right) \leq 0 .\
- **奖励 r_t**（L263 内逐字）：`r = - \big ( t _ { q } + t _ { t } + t _ { n } - t _ { c } \big ) ,\
  项含义（L180/L182/L266）：\t_q\ = queue delay；\t_n\ = current time；\t_c\ = "the moment of the last on/of change of a link"；\t_k\ = "the length of time during which the link remains connected"。**\t_t\ 全文无定义**（\grep -n -o -E 't _ \{ t \}\'\ 仅 L263 一处；"transmission time" 仅 L31），只能按 L31 "the reward function consists of queuing time, transmission time, and link lifetime" 推断。**无权重系数、无归一化。**
- **折扣 \gamma\ 是时间的函数**（L263 逐字）：`\gamma = \bigg [ \frac { \big ( t _ { c } - t _ { n } \big ) } { t _ { k } } \bigg ] ^ { 3 } .\；约束公式 (12) L212：`\Delta t \le t _ { c } - t _ { n } \le \operatorname* { m a x } t _ { k } ,\；动机 L219 — "Equation (12) ensures that the time direction is positive... At the same time, constraint 1 also ensures that the return value table of related nodes is updated before the network topology changes."
  【算术展开，论文未展开】由 (12) 得 \t_c-t_n>0\，故 \r=-t_q-t_t+(t_c-t_n)\：剩余链路寿命越长奖励越大；\gamma\in(0,1]\ 随"距下次拓扑变化时间/链路总寿命"三次方衰减。**原文未解释为何取三次方。**
- **转移/终止**：**无 episode/终止状态/reset**（\grep -n -i -E 'episode|terminal|horizon'\ → 1 命中 L334 "ground station terminals"；\eligib|trace|n-step|temporal difference|bellman|reset|done\ → 1 命中 L278 "preset"）。流程是**无限循环的事件驱动松弛**：L255 — "(6) Organize the fault situation, rebuild the topology at each moment, and go to (1)."；唯一"终止"是数值收敛判据（迭代指标 \l\）公式 (11) L204：`Q _ { i } ^ { l } ( d _ { k } , y _ { z } ) = Q _ { i } ^ { l + 1 } ( d _ { k } , y _ { z } ) .\；无收敛证明（\proof|theorem|guarantee\ → 仅 L91 三处 guarantees，讲检测先验）。

### 2) 学习算法与更新式
- 算法名：L31 — "based on the Q-learning algorithm in reinforcement learning, we propose a route recovery technology based on the above-mentioned fault detection."；L221 — "a Q-learning-based routing algorithm [28]"（[28] = L434 Boyan & Littman，即本批 47J2H748，**直接继承 Q-routing**）。
- **正常运行更新式**，L263 逐字：
  `\begin{array} { r l } & { \mathrm { Q } _ { x } ^ { \mathrm { n e w } } \big ( d _ { k } , y _ { z } \big ) = \mathrm { Q } _ { x } ^ { \mathrm { 0 d } } \big ( d _ { k } , y _ { z } \big ) + \alpha \Delta \mathrm { Q } _ { x } \big ( d _ { k } , y _ { z } \big ) , } \& { } \& { \Delta \mathrm { Q } _ { x } \big ( d _ { k } , y _ { z } \big ) = r + \gamma \operatorname* { m a x } \mathrm { Q } _ { y _ { z } } \big ( d _ { k } , y _ { m } \big ) - \mathrm { Q } _ { x } ^ { \mathrm { 0 d } } \big ( d _ { k } , y _ { z } \big ) , } \& { } \& { \qquad r = - \big ( t _ { q } + t _ { t } + t _ { n } - t _ { c } \big ) , } \& { } \& { \qquad \gamma = \bigg [ \frac { \big ( t _ { c } - t _ { n } \big ) } { t _ { k } } \bigg ] ^ { 3 } . } \end{array}\
- **故障触发更新式**，公式 (14) L248 逐字（前两行为 \-\infty\ 硬禁）：
  `\begin{array} { r l } & { Q _ { F } ^ { \mathrm { o d d } } ( d _ { i } , F ^ { \prime } ) = - \infty , } \& { Q _ { F ^ { \prime } } ^ { \mathrm { o d d } } ( d _ { i } , F ) = - \infty , } \& { Q _ { Y } ^ { \mathrm { n e w } } ( d _ { i } , F ) = Q _ { Y } ^ { \mathrm { o d d } } ( d _ { i } , F ) + \alpha \Delta Q _ { Y } ( d _ { i } , F ) , } \& { \Delta Q _ { Y } ( d _ { i } , F ) = t _ { q } + \gamma \operatorname* { m a x } Q _ { F } ^ { \mathrm { o d d } } ( d _ { i } , Y ) - Q _ { Y } ^ { \mathrm { o d d } } ( d _ { i } , F ) , } \& { Q _ { Y ^ { \prime } } ^ { \mathrm { n e w } } ( d _ { i } , F ^ { \prime } ) = Q _ { Y ^ { \prime } } ^ { \mathrm { o d d } } ( d _ { i } , F ^ { \prime } ) + \alpha \Delta Q _ { Y ^ { \prime } } ( d _ { i } , F ^ { \prime } ) , } \& { \Delta Q _ { Y ^ { \prime } } ( d _ { i } , F ^ { \prime } ) = t _ { q } + \gamma \operatorname* { m a x } Q _ { F ^ { \prime } } ^ { \mathrm { o d d } } ( d _ { i } , Y ^ { \prime } ) - Q _ { Y ^ { \prime } } ^ { \mathrm { o d d } } ( d _ { i } , F ^ { \prime } ) . } \end{array}\
  配套 L251 — "F and \F ^ { \prime }\ indicate nodes at both ends of the faulty link, the data trafic sending end is F, the receiving end is \F ^ { \prime } ,\ and Y and \Y ^ { \prime }\ represent the remaining neighbors of F and \F ^ { \prime }\ except the other party."
  ⚠ 两式状态下标不一致（式 14 用 \d_i\，式 15 用 \d_k\）。
- **损失函数：无**（\grep -n -i -E 'loss|gradient|backprop|bellman'\ → 0）。**double/target net/replay：无**（\replay\ 单独 → 0；\double|dqn|deep\ 3 命中均为他文的 neural network）。**网络结构：无神经网络，纯二维查表**（L221 + L223 + L190/L191 表 1）。**\alpha\ 数值未给**。
- 路由读出（贪心）L198：`\mathrm { r o u t e } = \{ \arg \operatorname* { m a x } Q _ { n _ { s } } ( n _ { d } , x _ { 1 } ) , \arg \operatorname* { m a x } Q _ { x _ { 1 } } ( n _ { d } , x _ { 2 } ) , \ldots , \arg \operatorname* { m a x } Q _ { x _ { m - 1 } } ( n _ { d } , x _ { m } ) \} ,\；L201 — "where \x _ { m } = n _ { d } ;\ for the formula, \m = 3 , 4 , . . . , n .\"（MinerU 注：该式无 \\tag{}\，式号 "(10)" 掉到 L229 单独一行）。

### 3) 信用分配
- **逐跳即时奖励：有**（L263 每次正常更新用一次）；\t_q\ 是**本节点**排队时延，L239 — "the satellite node sends the queuing time \t _ { q }\ of data transmission of each node to the ground station used to update Q-value table in real time."
- **路径级终局奖励：未见**（检索证据见第 1 项）。
- **分解到节点/链路**：故障情形按 \F/F'\ 两端点及其剩余邻居 \Y/Y'\ **局部**更新（公式 14 + L251）；正常情形只更新转发节点 \x\ 的 \Q_x\（公式 15）。
- **是否区分损失原因（本篇的独特之处）**：**奖励函数本身不区分**，但**区分靠"用哪一阶段检测结果驱动哪一组更新"实现**——L243 — "(4) Update the Q-value table according to the detection result of the first stage of the fault detection mechanism."；L253 — "(5) Update the Q-value table according to the detection results in the second stage of fault detection mechanism."；类别定义 L164（非缝隙区 vs 缝隙区）与 L166（"obtain the fault link location and fault type"）。⚠ **但公式 (14) 对两类故障用的是同一套公式**，论文**未给第二类故障的另一条更新式**。

### 4) 状态里有没有时间信息
- **状态无时间信息**（仅两个节点标识，L184）。\grep -n -i -E 'history|ewma|moving average|window'\ → **0 命中**。
- 时间以**折扣与奖励**间接进入：\gamma=[(t_c-t_n)/t_k]^3\ 与 \(t_n-t_c)\（L263）。
- **真正带时间窗聚合的是检测前端（非 MDP 状态）**：L29 — "collects and splits relevant information for successful transmission paths within Δt time"；L111 — "(2) Collect the path information of the successfully transmitted data within Δt."；仿真 \\Delta t\ = 3 s（L278）。

### 5) 动作有没有时间结构
- **每次转发独立决策**，策略恒为 argmax（L198），Q 表按 (目的地, 下一跳) 索引。**无驻留/无流级缓存/无摊销**（\dwell|residence|cache\ → 0）。
- **唯一的时间结构是事件触发的更新**：L235（初始化）、L237（交换管理信息与确认时间）、L239（地面站下发 Q 表/\gamma\/\alpha\，节点回传 \t_q\）、L241（是否有路由失败触发检测）、L257（正常时持续更新）、L270–L272（拓扑变化触发）。
  **关键缺口**：L272 — "(9) Perform a Q-transfer of the relevant link to the relevant node where the link switch occurs."——\grep\ 显示 "transfer" **全文仅此一处，无任何公式/伪码说明如何搬值**。
- **切换代价：动作里没有**；最接近的是 \-\infty\ 硬禁（L248）与 \gamma\ 三次方衰减（L263）。

### 6) 多智能体设定
- **全文未出现 "agent" 一词**：\grep -n -i -E 'agent'\ → **0 命中**；\multi-agent|multiagent\ → 0 命中。
- 每节点独立一张 Q 表、**不共享参数**（L221/L223）。
- 但**不是纯分散**：地面站参与同步（L239 下发 Q 表/\gamma\/\alpha\）；检测层汇总上报路径集合（L117 — "we could get reported path set \P = \left\{ p _ { 1 } , p _ { 2 } , \ldots , p _ { p } \right\ }\"）。可概括为"**本地表 + 地面站集中派发超参与表副本**"的混合架构。
- **动作同步/CTDE/联合动作：未见**。

### 7) 训练协议
- **无独立训练阶段，纯在线学习**（L221/L257）。
- 训练分布与评估分布**未区分**：\grep -n -i -E 'train'\ → 3 命中，全为 \Cons-train-t\（Constraint）误命中；**学习发生在被评测的同一次仿真中**。
- 超参 \alpha\、\gamma\ 由地面站下发（L239），**数值未给**。
- 时长：L321 — "the simulation time is 6000 s, the fault link is set at 2040 s, and the sampling interval is 60 s."；资源利用率实验另有一套 1800 s（L334）。
- **流量到达过程未说明**：\grep -n -o -i -E '.{0,55}(arrival|poisson|packet size|bandwidth|capacity|bit rate|data rate).{0,55}'\ → **0 命中**。

### 8) 该文的算法贡献
- (i) **把链路剩余寿命写进折扣与奖励**：\gamma=[(t_c-t_n)/t_k]^3\、\r=-(t_q+t_t+t_n-t_c)\（第 1、4 项，L263/L212），使同一张 \(n_i,d_k)\ 查表在拓扑切换前自动缩短有效视界；
- (ii) **把"故障类型"接进更新回路**：用检测结果决定触发哪一组更新（第 3、5 项，L243/L253），对故障链路两端做 \-\infty\ 硬禁并向剩余邻居 \Y/Y'\ 局部传播 \t_q\ 项（第 1、2、3 项，公式 14），从而不再"整节点绕开"；配合地面站集中派发（第 6 项，L239）与切换时 Q-transfer（第 5 项，L272，无公式）。
- **即：学习规则本身未变**（仍是 Vanilla Q-learning 单步 TD + \alpha\ 步长，第 2 项），改的是**奖励/折扣的时变化**与**"何时对谁更新"的事件触发结构**。

### 9) 该文自述的局限
- **无 Limitations / Future Work 小节**：\grep -n -i -E 'limitation|future work|drawback|shortcoming'\ → **0 命中**；L356 的结论段只写 "It has the following advantages."
- **正文中自述的弱点（逐字）**：
  - L132 — "It should be noted that, in order to meet the special needs of satellite networks, this mechanism assumes that the receiving end node of the failed path belongs to the set of unreachable area R. This assumption will cause an increase in suspected faulty links compared to the original definition, and the accuracy rate may decrease."
  - L282 — "when the failure rate is less than 10%... the IDBB mechanism proposed in this paper has a slightly lower accuracy rate in the first stage than the SLD method and DFDS algorithm"
  - L317 — "When the failure rate exceeds 20%, the accuracy of the fault classification in the first stage drops sharply."
  - L319 — "As the failure rate increases, after the topology changes, the fault probability of the new neighbor node and the newly established connection also increases... the detection accuracy of the second stage will decrease accordingly."
  - L342 — "as the failure rate increases, the accuracy rate of the fault type detection in the second stage will also decrease, and some temporary faults cannot be identified..."
- **客观报告缺口（登记，非"自述"）**：\alpha\/\gamma\ 无数值；\t_t\ 无定义；Q-transfer 无算法。

### 10) 该文没有考察的算法选择
| 模式（全文 440 行） | 计数 | 判读 |
|---|---|---|
| \replay\ 单独 | **0** | 无经验回放 |
| \grep -n -i -E 'replay\|target net\|double\|dqn\|deep'\ | **3** | **有命中，不构成反例**：L37/L386/L396 均为**他文**的 "neural network"（相关工作/参考文献） |
| \grep -n -i -E 'loss\|gradient\|backprop\|bellman'\ | **0** | 无损失/无梯度 |
| \grep -n -i -E 'mask\|feasible\|invalid'\ | **0** | 无掩码变量（仅 \-\infty\ 值屏蔽 L248） |
| \grep -n -i -E 'explor\|greedy\|epsilon\|random\|stochastic'\ | **2** | **有命中，不构成反例**：L278 "30 flows are randomly set"（**流量布置**，非动作探索）、L384 参考文献标题中的 "exploratory method"。策略恒为 argmax（L198），故无 \varepsilon\ 衰减/softmax/乐观初始化 |
| \grep -n -i -E 'eligib\|trace\|n-step\|temporal difference\|bellman\|reset\|done\|terminal state'\ | **1** | **有命中，不构成反例**：L278 的 "preset"（词内子串） |
| \grep -n -i -E 'episode\|terminal\|horizon'\ | **1** | **有命中，不构成反例**：L334 "ground station terminals"（地面站终端，非终止状态） |
| \grep -n -i -E 'normaliz\|scal'\ | **4** | **有命中，不构成反例**：L39 可扩展性、L286/L300/L302 仿真叙述，与状态归一化无关 |
| \grep -n -i -E 'proof\|theorem\|guarantee'\ | **3** | **有命中，不构成反例**：L91 三处 guarantees 讲式(3)(4)(5) 检测先验，与 Q 收敛无关 |
| \agent\ | **0** | 无多智能体层面任何选择被比较 |
| \load\ | **5** | **有命中，不构成反例**：L39/L380/L412/L418/L430 全为他文/参考文献标题词 |

结论：1) 无函数近似；2) 无 replay/target net/double；3) **无任何探索策略**；4) 无资格迹/n 步，**连 episode 边界概念都未设**；5) 无动作掩码变量；6) 无状态归一化；7) 无收敛性分析；8) 无多智能体层面选择；9) **无消融**（L328 的两个对比算法 BPRP 与 LRRS **都是非 RL 的**）；10) 无负载/拥塞项进入状态或奖励。

### 11) 可复用的具体机制
- **(a) 寿命感知折扣因子** \gamma = \bigg[ \frac{t_c-t_n}{t_k} \bigg]^3\（L263）+ 约束 (12) L212——把 bootstrap 权重设为"距下次计划拓扑变化的时间 / 链路总寿命"的幂，视界在切换前自动收缩。**原文未解释三次方。**
- **(b) 含寿命项的奖励** \r=-(t_q+t_t+t_n-t_c)\（L263），在 (12) 下等价于 \-t_q-t_t+(t_c-t_n)\。**\t_t\ 需自行补定义。**
- **(c) 值级硬禁代替动作掩码**：\Q_F^{\mathrm{odd}}(d_i,F')=-\infty\、\Q_{F'}^{\mathrm{odd}}(d_i,F)=-\infty\（L248）——无需掩码基础设施，argmax 永不选中故障方向。
- **(d) 故障触发的 1 跳局部再松弛**：公式 (14)（L248），更新集合 = \{F,F'}\ 及其剩余邻居 \Y/Y'\；故障情形即时项退化为纯 \t_q\。**"局部修复而非全路径重路由"的公式化写法。**
- **(e) 表松弛的不动点停机准则**：公式 (11) L204。
- **(f) 控制面设计**：L239（地面站下发 Q 表/\gamma\/\alpha\，节点回传 \t_q\）。
- **(g) 低开销信息采集**：L111/L113/L117——只收集 \\Delta t\ 窗口内**成功**传输的路径与链路（仿真 \\Delta t\=3 s，L278），替代广播探测。**这是让 \-\infty\ 更新有信息可用的前置条件。**
- **(h) 拓扑切换时的 Q-transfer**：L272 仅一句、**无公式，只能当概念参考，不可直接复现**。

### 12) 实验合同里与"负载"相关的设置（仅登记，非贡献）
- **检测侧（5.1，L276–L278）**：先验链路故障概率 0.1；1–4 号端口故障先验 0.08/0.005/0.001/0.0005；"the link delay is set to about 20 ms, and the information collection time is set to 3 s."；"The topology adopts a static topology, and **30 flows are randomly set** to simulate a real satellite network communication environment."；拓扑 6×6；阈值：链路故障概率指标 0.01、端口故障概率指标 0.002。
  对比算法 L280：SLD 与 DFDS。指标：检测准确率（图 3）、检测完整率（图 4）、开销＝检测包数（L300）、故障分类准确率（图 6）；故障率扫描 15%/25%/35%/45%（L315，含 MinerU 乱码字符）。
- **路由侧（5.2，L321）**：仿真时间 6000 s、故障链路设在 2040 s、采样间隔 60 s；发端北京地面站（117°13′E, 40°05′N）、收端洛杉矶（120°26′W, 34°05′N）；路径上**两条**故障链路（一条端口永久故障、一条介质干扰临时故障，L321–L328）。对比算法 L328：BPRP 与 LRRS（**均非 RL**）。指标：恢复路径时延-时间（图 7）、有效资源利用率-故障率（图 8）。
- 资源利用率实验的负载 L334 — "Participating in the simulation of efective resource utilization are all 20 ground station terminals; 10 ground station terminals are set as data sending ends, 10... receiving ends, and the simulation time is 1200 s to 3000 s for a total of 1800 s; each emulates 20 times under the failure rate and the efective resource utilization is averaged."
- **故障率是被扫的唯一"压力"旋钮**（L336、L340–L344）。
- **未登记项（论文未给）**：到达过程、包长/带宽/容量、队列调度规则、每流速率、业务量分布（检索见第 7 项）。

---

## 6. 47J2H748 — Packet Routing in Dynamically Changing Networks: A Reinforcement Learning Approach（Q-routing）

（Boyan & Littman, CMU/Bellcore；正文 L1–L99 读完，References L100–L119 未逐条读。**本批唯一的基础性 RL 路由原典，也是 8N9QJHC2 的直接源头（8N9QJHC2 L434 引其 [28]）**。）

### 1) MDP 定义
- **无显式 MDP 元组**：全文未出现 "MDP"/"state space"/"action space"/"reward function"（第 10 项计数）。形式化以 Q 函数给出。
- **状态（原文的等价物）**：**（当前节点 x, 目的节点 d）**，即按 (目的地, 下一跳) 索引的查表：L25 — "Let \Q _ { x } ( d , y )\ be the time that a node x estimates it takes to deliver a packet P bound for node d by way of \x'\s neighbor node \y ,\ including any time that P would have to spend in node \x'\s queue."（**注意：状态里显式包含了"在 x 队列里要花的时间"这一排队项**）
- **动作 a_t**：选择邻居 \y\。动作空间 = 邻居集合；**无掩码变量**（第 10 项计数）。决策规则是 argmin：L25–L28 的候选评估 \t = \operatorname*{m i n}_{z \in \mathrm{neighbors~of~} y} Q_y(d,z)\（见第 2 项）。
- **奖励 r_t（本文的"奖励"= 实际经历的时间）**：**无显式 \r_t\ 记号，也无折扣 \gamma\**（第 10 项计数：\discount|gamma\ → 0）。等价形式是更新式里的 \q+s+t\，其中 L31 — "If the packet spent q units of time in x's queue and s units of time in transmission between nodes x and \y ,\ then x can revise its estimate as follows:"。
- **转移/终止**：**无 episode、无终止折扣设定**。学习是**持续的在线异步松弛**：L37 — "The resulting algorithm can be characterized as a version of the Bellman-Ford shortest paths algorithm [1, 3] that (1) performs its path relaxation steps asynchronously and online; and (2) measures path length not merely by number of hops but rather by total delivery time."
  **无资格迹/n 步**（第 10 项计数）。
- **无折扣 \gamma\**：代价本身就是"送达时间"，是未折扣的累计量——这一点与后续所有 DRL 路由论文（都用 \gamma\<1）形成根本差异。

### 2) 学习算法与更新式
- 算法名 **Q-routing**：L39 — "We call our algorithm "Q-routing" and represent the Q-function \Q _ { x } ( d , y )\ by a large table."
- **更新式（L34 逐字，含原文的 overbrace 标注）**：
  `\Delta Q _ { x } ( d , y ) = \eta ( { \overbrace { q + s + t } ^ { \mathrm { n e w \ e s t i m a t e } } } - { \overbrace { Q _ { x } ( d , y ) } ^ { \mathrm { o l d \ e s t i m a t e } } } )\
  其中 \t\ 由邻居的估计给出（L28 逐字）：`t = \operatorname* { m i n } _ { z \in { \mathrm { n e i g h b o r s ~ o f ~ } } y } Q _ { y } ( d , z )\
  L37 — "where 17 is a "learning \mathrm{rate}^{\mathrm{5}}\ parameter (usually 0.5 in our experiments)."（**MinerU 把 \eta\ 转成了 "17"；学习率通常取 0.5**）
- **TD 目标 = \q+s+t\（实际排队+传输+邻居估计）**；**无损失函数、无 target net、无 replay、无 double**（第 10 项计数；本文 1994 年，早于 DQN）。
- **网络结构：表格型**：L39 — "represent the Q-function \Q_x(d,y)\ by a large table"。
  **但作者试过神经网络并明确报告了负面结果**（L39，逐字）："We also tried approximating \Q _ { x }\ with a neural network (as in e.g. [8, 4]), which allowed the learner to incorporate diverse parameters of the system, including local queue size and time of day, into its distance estimates. However, the results of these experiments were inconclusive."
  **这是本批中唯一明确把"函数近似+额外状态特征（队列长度、时段）"判为 inconclusive 的论文——对 G-A（状态该放什么）是一条直接反证。**

### 3) 信用分配
- **逐跳即时（一跳）信用**：节点 x 收到 y 的估计后立即更新自己的 \Q_x(d,y)\（L25–L34）。**信用只传播一跳**，靠持续在线松弛逐跳扩散。
- **无路径级终局奖励**（无 episode）；路径级表现只在实验里以"平均送达时间"度量（L46/L60）。
- **分解到链路/节点**：分解到 **(节点 x, 目的地 d, 下一跳 y)** 三元组；**不区分损失原因**（只有时间量）。
- **原文明确指出的信用分配缺陷**（L77，逐字）："However, a close look at the algorithm reveals that Q-routing cannot fine-tune a policy to discover shortcuts, since only the best neighbor's estimate is ever updated. For instance, if a node learns an overestimate of the delivery time for an optimal route, then it will select a suboptimal route as long as that route's delivery time is less than the erroneous estimate of the optimal route's delivery time."
  **即：只更新最优邻居 ⇒ 系统性高估无法被修正。** 这是"探索-信用"矛盾的经典陈述。
- **对随机探索的负面结论（对 RL 路由选题极重要）**（L79，逐字）："A common one is to have the algorithm select actions with some amount of randomness during the initial learning period[10]. But this approach has two serious drawbacks in the context of distributed routing: (1) the network is continuously changing, thus the initial period of exploration never ends; and more significantly, (2) random traffic has an extremely negative effect on congestion. Packets sent in a suboptimal direction tend to add to queue delays, slowing down all the packets passing through those queues, which adds further to queue delays, etc. Because the nodes make their policy decisions based on only local information, this increased congestion actually changes the problem the learners are trying to solve."

### 4) 状态里有没有时间信息
- **无显式的历史/趋势/EWMA 状态分量**（第 10 项计数：\history|EWMA|moving average|trend\ → 0）。
- **但状态里含"排队时间"这一时间量**：\Q_x(d,y)\ 的定义包含 "any time that P would have to spend in node x's queue"（L25）；更新的 TD 目标显式含 \q\（在 x 队列中花费的时间）与 \s\（传输时间）（L31）。
- **时间是"被估计的期望值"而非"窗口统计量"**——这是与 EWMA 式做法最本质的差别：\Q\ 本身就是一个隐式的长期平均。
- 作者认为"时段"（time of day）这类时间特征值得试，但神经网络实验 inconclusive（L39）。

### 5) 动作有没有时间结构
- **每包逐跳独立决策**（L23 — "to which adjacent node should the current node send its packet to get it as quickly as possible to its eventual destination?"）。
- **无动作驻留、无流级缓存、无切换代价**（第 10 项计数）。
- **"full echo" 变体引入了一条显式的旁路信令时间结构**（L81，逐字）："Instead of sending actual packets in a random direction, a node using the "full echo" modification of Q-routing sends requests for information to its immediate neighbors every time it needs to make a decision. Each neighbor returns a single number-using a separate channel so as to not contribute to network congestion in our model-giving that node's current estimate of the total time to the destination. These estimates are used to adjust the \Q _ { x } ( d , y )\ values for each neighbor y."
- **探索期的"策略振荡"被实测到**（L83，逐字）："Our analysis indicates that "full echo" Q-routing constantly changes policy under high load, oscillating between using the upper bottleneck and using the central bottleneck for the majority of crossnetwork traffic. This behavior is unstable and generally leads to worse routing times under high load."
- **原文的结论句（对"要不要探索"的罕见坦诚）**（L88，逐字）："Ironically, the "drawback" of the basic Q-routing algorithm-that it does no exploration and no fine-tuning after initially learning a viable policy-actually leads to improved performance under high load conditions. We still know of no single algorithm which performs best under all load conditions."

### 6) 多智能体设定
- **每个节点内嵌一个学习模块**：L11 — "a reinforcement learning module is embedded into each node of a switching network. Only local communication is used by each node to keep accurate statistics on which routing decisions lead to minimal delivery times."
- **独立学习、无参数共享**（每节点自己的表；L39 "by a large table"）。
- **通信 = 一跳估计回传**（L25 — "Upon sending P to y, x immediately gets back \y'\s estimate for the time remaining in the trip"）。
- **非平稳：明确承认，但采取"不探索"的应对**（L79 与 L88，见上）。
- **无动作同步**；L37 强调异步："performs its path relaxation steps asynchronously and online"。
- **迭代式的多体耦合被明确点出**（L81 的 full echo 论证）：策略同时变化导致振荡。

### 7) 训练协议
- **无训练/评估划分，纯在线持续学习**：L17 — "The learning is continual and online, uses only local information, and is robust in the face of irregular and dynamically changing network connection patterns and load."
- **多种拓扑**：L46 — "We tested the Q-routing algorithm on a variety of network topologies, including the 7-hypercube, a 116-node LATA telephone network, and an irregular 6 x 6 grid. Varying the network load, we measured the average delivery time for packets in the system after learning had settled..."
- **负载动态变化是主要实验轴**（L46、L60、L67–L73）。
- **统计口径**：L60 — "Each point represents the median (over 19 trials) of the mean packet delivery time after learning has settled."
- **仿真器**：L19 — "The experiments in this paper were carried out using a discrete event simulator to model the transmission of packets through a local area network and are described in detail in [5]."

### 8) 该文的算法贡献
- L17 — "Our "Q-routing" algorithm, related to certain distributed packet routing algorithms [6, 7], learns a routing policy which balances minimizing the number of "hops" a packet will take with the possibility of congestion along popular routes. It does this by experimenting with different routing policies and gathering statistics about which decisions minimize total delivery time."
- L37 — "The resulting algorithm can be characterized as a version of the Bellman-Ford shortest paths algorithm [1, 3] that (1) performs its path relaxation steps asynchronously and online; and (2) measures path length not merely by number of hops but rather by total delivery time."
- **对应**：① 状态 = (目的地, 下一跳) 表索引，且 Q 值**内含排队时延**（第 1、4 项）；② 更新 = 邻居回传的一跳 TD，学习率 0.5（第 2 项）；③ 信用一跳传播、只更新最优邻居（第 3 项）；④ 每节点一模块、无参数共享、无探索（第 5、6 项）。

### 9) 该文自述的局限
- L92 — "Although the simulations described here are not fully realistic from the standpoint of actual telecommunication networks, we believe this paper has shown that adaptive routing is a natural domain for reinforcement learning. Algorithms based on Q-routing but specifically tailored to the packet routing domain will likely perform even better."
- L88 — "We still know of no single algorithm which performs best under all load conditions."
- L83 — "This behavior is unstable and generally leads to worse routing times under high load."
- L77 — "Q-routing cannot fine-tune a policy to discover shortcuts, since only the best neighbor's estimate is ever updated."
- L39 — 神经网络近似"the results of these experiments were inconclusive."

### 10) 该文没有考察的算法选择
检索范围 = 全文 119 行：

| 模式 | 计数 | 判读 |
|---|---|---|
| \grep -ciE "discount\|gamma"\ | **0** | **无折扣因子**（代价即送达时间，未折扣） |
| \grep -ciE "multi-?agent\|decentraliz\|decentralis"\ | **0** | 无多智能体术语（虽实为多体，但未按 MARL 形式化） |
| \grep -ciE "target network\|target q\|replay\|experience pool\|double q\|double dqn"\ | **0** | 无 replay/target net/double |
| \grep -ciE "EWMA\|exponential moving\|moving average\|history\|historical\|previous state\|trend"\ | **0** | 状态无时间窗特征 |
| \grep -ciE "action mask\|invalid action\|impossible action\|mask"\ | **0** | 无掩码 |
| \grep -ciE "eligibility\|n-step\|multi-step\|multistep"\ | **0** | 无资格迹/n 步 |

1. **折扣因子**：未考察（这也意味着不存在 \gamma\ 调参问题）。
2. **函数近似**：**试过且报告 inconclusive**（L39）——不是"未考察"，而是**有负面考察结果**。
3. **探索策略**：**试过随机探索与 full echo 两种，并给出负面结论**（L79/L83/L88）——同样**不是"未考察"**。
4. **多智能体形式化/参数共享/非平稳**：未考察（未用 MARL 语言）。
5. **动作掩码/目标节点条件下的非法动作**：未考察。
6. **队列状态作为显式特征**：仅在神经网络实验中提过（L39 "including local queue size and time of day"），结果 inconclusive。
7. **策略梯度/actor-critic 族**：1994 年，全文未考察。

### 11) 可复用的具体机制
1. **邻居回传式一跳 TD 目标**（本批 3 篇共用的核心机制）：\t = \operatorname*{min}_{z \in \mathrm{neighbors~of~} y} Q_y(d,z)\（L28）+ \\Delta Q _ { x } ( d , y ) = \eta ( q + s + t - Q _ { x } ( d , y ) )\（L34）。**只要一跳信令，就能把"下游的最优剩余时间"带回来**——本批 YI9G7NR7 的 \\mathcal{Q}_j(s'_{t+1},a'_t)\ 与 8N9QJHC2 的 \Q_{y_z}(d_k,y_m)\ 都是它的后代。
2. **把"本节点排队时间"写进 Q 值定义**（L25），使策略天然避开自身排队——比"状态里放队列长度"更省特征工程。
3. **"full echo" 旁路信令**（L81）：用**独立信道**向所有邻居索取估计，不产生探索流量。**代价与风险均被实测**（高负载下策略振荡，L83）。
4. **对"随机探索在路由中"的反面结论**（L79/L88）：可直接引用为我们方案"不该用 \varepsilon\-greedy 探索真实包"的论据。

### 12) 实验合同里与"负载"相关的设置（仅登记，非贡献）
- 拓扑：7-hypercube、116 节点 LATA 电话网、不规则 6×6 网格（L46，图 1 L42）。
- **负载是主变量**：L60 — "This compares the performances of the shortest path policy and Q-routing learned policy at various levels of network load."；L73 — "However, when network traffic levels were then lowered again, adaptation was much slower, and never converged on the optimal shortest paths."（**负载下降时不收敛——一条重要的非对称适应性事实**）
- 动态变化三维度（L67–L73）：拓扑断链（"We manually disconnected links from the network during simulation."）、流量模式周期振荡（上下半区 ↔ 左右半区）、负载水平升降。
- 统计：19 次试验的中位数（L60）。
- 对比算法：静态最短路径（L46/L48/L60）。
- 报告口径（登记）：L46 — "in all cases, Q-routing is able to sustain a higher level of network load than could shortest paths."；L50 — 高负载下最短路径"ignores the rising levels of congestion and soon floods the network with packets"，Q-routing 学会了把流量绕到"a longer than necessary path (across the top of the network) so as to avoid congestion in the center"。

---

## 7. JLF7IEBQ — SaTE: Low-Latency Traffic Engineering for Satellite Networks（SIGCOMM '25）

（正文 L1–L338 与附录 L509–L714 逐行读完；L339–L508 为参考文献表 [1]–[83]，未逐条读。**前置结论：本文不含任何 RL/MDP 成分**——算法本体是"用 Gurobi 最优解做标签的监督学习 + 异构图注意力 GNN 回归器"，推理是单次前向，不是序贯决策。故第 1、3、4、5、6 项所问的 MDP/奖励/信用分配/时序状态/动作时间结构/多智能体**全部未见**；下文每项先给"未见"的检索证据（范围＝全书 714 行含参考文献），再给最接近的替代物逐字原文。）

**全书检索证据（E1–E11，后文引用）**
- **E1** \grep -n -i -E "markov|MDP|Q-learning|DQN|PPO|actor|critic|policy gradient|reinforcement"\ → 正文唯一相关命中 L136（**描述他人工作**），其余命中全部落在参考文献标题（如 L359 [10] AuTO: Scaling Deep Reinforcement Learning…）。本文自身算法无一处 RL。
- **E2** \grep -n -i -E "reward|discount|episode|episodic|terminal|horizon|eligibility trace|n-step"\ → 命中仅 L591（变量 \gamma\，卫星编号）、L668/L671（人口平滑因子 \gamma\）。**reward / discount / episode / terminal / horizon 零命中**。
- **E3** \grep -n -i -E "target network|replay buffer|replay|double DQN|epsilon-greedy|exploration"\ → 唯一命中 L473，为公司名 "Space Exploration Technologies Corp. (SpaceX)"。**target network / replay / double 零命中**。
- **E4** \grep -n -i -E "state space|action space|observation|credit assignment"\ → 仅 L136 一处（他人工作）。**均为零命中（除 L136）**。
- **E5** \grep -n -i "action"\ → 全部命中均为 reaction(L41)、allocation(L85)、reconfiguration(L327)、Transactions(刊名) 等同形词，**无一处把 action 当决策变量**。
- **E6** \grep -n -i -E "mask|infeasible|projection|clip"\ → **exit=1，零命中**（无掩码、无可行域投影、无梯度裁剪）。
- **E7** \grep -n -i -E "EWMA|history|historical|past|previous|sliding|trend|temporal|time series|sequence model|differenc"\ → 仅 L72（"Historically, satellite communication…"）、L163（"time-varying trafic matrices"）、L313（"We previously trained…"）与 L405/L423/L455（参考文献标题）。**EWMA / sliding window / history feature 零命中**。
- **E8** \grep -n -i -E "dwell|per-packet|per packet|hop-by-hop|hop by hop|switchover|handover|oscillat|churn"\ → 仅 L361（参考文献 [11] 标题）。**dwell / per-packet / switching cost 零命中**。
- **E9** \grep -n -i -E "recurrent|LSTM|GRU|transformer|self-attention|multi-head"\ → 仅 L282 与 L505（**描述基线 HARP**）。本文模型无时序网络。
- **E10** \grep -n -i -E "epoch|learning rate|optimizer|Adam|SGD|batch"\ → 唯一命中 L387 参考文献 "Gurobi Optimizer Reference Manual"。**训练超参全文未给**。
- **E11** \grep -n -i -E "normaliz|standardiz|feature scaling"\ → 仅 L545/L691 的 "Min-Max Link Utilization"（**目标函数名，非特征归一化**）。

### 1) MDP 定义
- **未见 MDP 定义**（E1/E2/E4）。等价接口是**每个 TE slot 一次的"输入图 → 分配向量"监督回归**，不存在 \(s_t,a_t,r_t,s_{t+1})\ 结构。
- **输入（= 状态位）逐字段**：L222 — "SaTE's model uses trafic matrix, network topology, and ten pre-calculated shortest paths between each source-destination pair to compute optimal trafic allocation."；L163 — "SaTE constructs a heterogeneous satellite TE graph to represent the entire TE problem. This graph captures changes in topology, time-varying trafic matrices, and path reconfigurations."
  六个字段（L183 — "We empirically select the embedding dimension to be 768 for nodes and edges... each embedding is initialized by multiplying its respective TE input with a 1×768 learnable weight matrix W, randomly initialized at the start."；Fig. 7 表 L189 逐字）：NE1 卫星嵌入 = \mathsf{W}_{\mathsf{NE1}}\ · #Neighbors；NE2 路径嵌入 = \mathsf{W}_{NE2}\ · Path Length；NE3 流量嵌入 = \w_{\scriptstyle \mathrm{NE3}}\ · Traffic Demand；EE1 边嵌入 = WEE1 · Link Capacity；**EE2 边嵌入 = 原文单元格仅剩 "dding"（MinerU 缺字，照抄不改）**；EE3 边嵌入 = \mathsf{W}_{EE3}\ · #Candidate Paths。
  **归一化：未见任何特征归一化**（E11 的 Min-Max 命中是 MLU 目标名）。**时间聚合：字段本身是瞬时快照**；唯一的跨时间聚合在负载侧——L232 — "The trafic matrix is generated by aggregating the total demands of both new and ongoing flows between each satellite pair."
- **动作 a_t**：对每个 \(flow j, path p)\ 输出连续带宽分配量 \x_{jp}\。L197 — "an MLP decoder computes the trafic allocation \x _ { j p } ,\ which represents the amount of trafic 𝑗 assigned to path \p .\"；规模 = 非零需求源-目的对 × 每对 10 条路径（L234 — "10 shortest paths are precomputed per satellite pair for routing."；L205 给出 4236×4236 流量矩阵 72 GB 与路径矩阵 263 GB）。
  **既非下一跳、亦非单纯比例**：路径预先给定——L94 — "(3) Network Path Preconfiguration: Trafic paths (e.g., from source A to destination B) are precomputed based on the determined network topology."
  **无动作掩码**（E6 零命中）：约束靠软约束+事后裁剪，L199 — "they cannot guarantee that the total bandwidth allocated to a flow will not exceed its demand or that trafic allocation will remain within link capacity limits. As a result, the computation outcome \x _ { j p }\ may violate TE constraints. To address this, we trim overloaded trafic, ensuring the final TE solution is feasible."
- **奖励（原文无 r_t；E2 零命中）——等价目标逐字抄**：附录 A 的 TE 问题 (2)：
  `\operatorname* { m a x i m i z e } \mathcal { U } = \sum _ { f \in \mathcal { F } _ { t } } \sum _ { p \in \mathcal { P } _ { f } } x _ { f p }\(2.a)`
  `{ \mathrm { s u b j e c t ~ t o } } \sum _ { f \in { \mathcal { F } } _ { t } } \sum _ { p \in { \mathcal { P } } _ { f } } \Phi _ { p e } x _ { f p } \leq C _ { e } , \forall e\(2.b)`
  `\sum _ { f : f \uparrow n } \sum _ { p \in \mathcal { P } _ { f } } x _ { f p } \leq C _ { n } ^ { u p } , \forall n\(2.c)`
  `\sum _ { f : f \downarrow n } \sum _ { p \in \mathscr { P } _ { f } } x _ { f p } \leq C _ { n } ^ { d n } , \forall n\(2.d)`
  `\sum _ { p \in \mathcal { P } _ { f } } x _ { f p } \leq d _ { f } , \forall f\(2.e)`；`variables \ x _ { f p } \geq 0 , \forall f , p`
  符号 L543 — "\mathcal { U }\ represents network throughput, \mathcal { F } _ { t }\ includes all ongoing flows at time 𝑡 and \mathcal { P } _ { f }\ represents all feasible paths for flow \f\"；目标可替换 L545 — "Min-Max Link Utilization: min \underset { e } { \mathrm { \arg x } } \sum…\frac { \Phi _ { p e } x _ { f p } } { C _ { e } }\ , Maximize Network Utility: max \sum… u _ { f } ( \sum… x _ { f p } )\"
  **是否归一化**：\mathcal U\ 直接带宽求和（未归一化）；只有实验指标归一化（L251 satisfied demand）。**折扣 \gamma\：无**（E2）。
- **转移/终止**：**无 episode、无终止条件**（E2）。系统节拍是周期 workflow，L100 — "The workflow operates periodically over fixed time intervals, with the duration primarily determined by the runtime of TE computation step."；环境演化与动作无关 L92 — "Satellite network topologies change over time but are predefined by satellites' designated orbits."；L232 — "In each 1-second interval, a Poisson process with trafic intensity lambda (flows per second) generates new flows between randomly selected user pairs or between a gateway and a user." 即**没有"动作导致下一状态"的转移建模**。**无资格迹/多步回报**（E2）。

### 2) 学习算法与更新式
- 范式 L201 — "Training Method: We train the GNN model using supervised learning, with ground-truth labels for trafic allocation generated by the commercial solver Gurobi [24]... During training, we iteratively calculate the loss between the label \x _ { j p } ^ { * }\ and the trafic allocation \x _ { j p }\ computed by SaTE."
- **消息传递更新式**（正文式 (1) = 附录 F 式 (6)）逐字，L644（原文此处无 \\boldsymbol\，且 \^\prime\ 后是两个空格，MinerU 丢了赋值箭头，照抄不改）：
  `\begin{array} { r l } & { v _ { i } ^ { \prime }  \Theta _ { s } \cdot v _ { i } + \| _ { k = 1 } ^ { K } \Bigg ( \displaystyle \sum _ { j \in r ( i ) } \alpha _ { j , i } ^ { k } ( \Theta _ { n } ^ { k } \cdot v _ { j } + \Theta _ { e } ^ { k } \cdot e _ { j , i } ) \Bigg ) ,  } \& { v _ { i } ^ { \prime }  \mathrm { L e a k y R e L U } ( v _ { i } ^ { \prime } ) , } \end{array}\
- **注意力系数式**，L650 逐字：
  `\begin{array} { r l } & { \alpha _ { j , i } ^ { k } = { \mathrm { s o f t m a x } } _ { i } ( \mathrm { L e a k y R e L U } ( } \& { \quad \quad a ^ { T } \left[ \Theta _ { n } ^ { k } \cdot v _ { i } \ \lVert \ \Theta _ { n } ^ { k } \cdot v _ { j } \ \rVert \ \Theta _ { e } ^ { k } \cdot e _ { j , i } \right] ) ) , } \end{array}\；L653 — "with 𝑎 corresponding to a learnable vector."
- **损失函数（训练侧"更新式"）**，L565 逐字：
  `\mathcal { L } = \mathcal { L } _ { \mathrm { s u p e r v i s e d } } + \frac { - \lambda _ { \mathrm { f l o w } } \cdot \mathrm { t o t a l \_ f l o w } + \sum _ { i } \alpha _ { i } \cdot \mathrm { o v e r \_ f l o w } _ { i } } { \lambda _ { \mathrm { b a l a n c e } } \cdot \lambda _ { \mathrm { f l o w } } \cdot \mathrm { t o t a l \_ d e m a n d } } ,\
  `\alpha _ { i } = \exp \left( \operatorname* { m i n } \left( \frac { \mathrm { u t i l i z a t i o n } _ { i } } { \mathrm { c a p a c i t y } _ { i } } , \alpha _ { \mathrm { m a x } } \right) \right) .\
  语义 L574 — "total\_\flow represents the sum of allocated trafic bounded by constraints, and over\_\flow represents the overloaded trafic that exceeds the capacity of each link."；动机 L576 — "combining supervised learning and penalized optimization enables SaTE to learn from the reference value while being guided by the penalty term for constraint violations."
- **无 TD 目标 / 无 double / 无 target net / 无 replay**（E3）。
- **网络结构**：三个模块化 **GAT**，L181 — "SaTE uses three GNN modules, each applied to process a type ofrelation. The architecture for all GNN modules is based on the graph attention network [9]…The three GNN modules sequentially aggregate and propagate information according to their respective relations"；分工 L197 — "'GNN for R1' module computes satellite embeddings. 'GNN for R2' module updates satellite and path embeddings concurrently…'GNN for R3' module refines path embeddings and trafic embeddings together."
  宽度固定 768（L183）；激活 LeakyReLU（L644）；K 头拼接（L647 — "𝐾 attention heads are utilized"）。**层数未给数值**：L578 — "we determine it based on inference time rather than validation performance. Specifically, we use the minimum number of layers possible without incurring performance degradation."；**K 数值亦未给**。
- **唯一非图算子**是末端 MLP decoder（L197），与全文卖点 L45 — "This design eliminates the need for DNN layers, allowing GNNs to learn and solve TE entirely." 并存。

### 3) 信用分配
- **未见逐跳即时奖励/路径级终局奖励/按损失原因分类**（E1/E2/E4）。两条"分配信号"通道：
  (a) **全局监督信号逐元素摊到决策变量**：L201（同上）——信用直接落在 \x_{jp}\ 上，由 Gurobi 最优解逐元素给标签；**不按跳、不按源-目的对分解，也不区分失败原因**。
  (b) **唯一的按元素分解项：逐链路溢出惩罚**（式 4 的 \sum_i\ 项 + 式 5）：L565/L571（原文见上），语义 L574 — "over\_\flow represents the overloaded trafic that exceeds the capacity of each link."
  (c) **后处理层的"信用"**：L199 — "we trim overloaded trafic, ensuring the final TE solution is feasible."（**裁剪的优先级/分配规则原文未描述**）。
- **是否区分损失原因：未见**。作者把与上界的差距归为**混合因素而非可分解原因**——L679 — "The performance gap between SaTE and the upper bound achieved by Gurobi arises from multiple factors, including post-correction adjustments and model degradation on unseen inputs."

### 4) 状态里有没有时间信息
**没有**（E7 零命中；E9 显示本文模型无 recurrent/LSTM/GRU/transformer）。输入是当前时刻瞬时快照的 6 个字段，每个只乘一个 1×768 矩阵（L183），**无时间窗、无帧堆叠、无差分特征**。
- 唯一与时间有关的耦合在**负载本身**：L232（"ongoing flows" 使 Traffic Demand 隐式带流历史残留）；L236 表给出流持续时间 "Voice / 64 Kbps / 1 to 10 minutes"、"Video / 8Mbps / 5 to 30 minutes"、"File Transfer / 50 Mbps / 26 to 130 minutes"，即 traffic matrix 的记忆长度由流的生存期（1–130 分钟）决定，**而非模型设计**。
- 时间维靠**每个 slot 重新前向一次**被动处理：L245 — "we collect 10,000 time-varying topologies at an 1-second interval"；L292 — "For SaTE, this occurs every second, while for other baselines, it occurs at intervals corresponding to their average computational latency…specifically 47 s, 25 s, and 54 s for Gurobi, PoP, and ECMP with WF."
- 原文对"时间"的唯一显式论证是**为什么不需要时序建模**：L207 — "the inductive learning capabilities of GNNs [9] allow SaTE to generalize to unseen topologies, enabling training on a small set of representative topologies instead of all possible snapshots."

### 5) 动作有没有时间结构
- **不是每包独立决策**，而是集中控制器周期性下发的"每流在预配置路径上的带宽"：L85 — "a control center that periodically gauges trafic demands (by a bandwidth broker [35]), computes trafic allocation, and translates the results into router configurations deployed through SDN"；L98 — "(4) Trafic Rule Distribution and Loading: Trafic allocation results are converted into trafic rules for onboard satellites switches."
- **动作驻留（隐式，非显式建模）**：L251 — "the current trafic allocation remains in efect until the new one is computed."；L292 — "the existing trafic allocation remains active until a new one is computed."
  **驻留时长实测**：SaTE 1 s，基线 47/25/54 s（L292）。现实控制面节奏 15 s：L327 — "Recent studies reveal that Starlink operates on a globally synchronized 15-second workflow interval for periodic network reconfigurations [52]"
- **无流级缓存/摊销**（E8 零命中）。**触发式更新只发生在路径集合层面**：L234 — "Instead of recalculating all paths every interval, only those impacted by topology changes—such as newly consistent ISLs or removed links—are updated."；L243 — "than 2% of paths per second, with an average computation time of 56 ms."
- **切换代价：未见**（E8 零命中）；重配置代价既未进目标函数也未测量。

### 6) 多智能体设定
- **未见多智能体设定**（E4）；正文唯一的 "multi-agent reinforcement learning" 出现在 L136 **描述他人工作**。
- **完全集中式、单一模型、单一控制器**：L329 — "SaTE's TE computation operates within the centralized SDN for satellite networks [6, 19, 36], where satellites are managed by a centralized control center"；L148 — "we transform classic TE optimizations into an inference process of neural networks, which can be accelerated by GPU"。
- **分布式方案被明确排除在延迟对比之外**：L247 — "We compare only performance for this scheme, not computational latency, since its computation is distributed across the routers rather than on a centralized controller."
- **非平稳**不是在 MARL 意义上处理，而是"分布外泛化 + 是否要重训练"：L315 — "The observed performance decline also suggests the need to retrain the model on the up-to-date constellation state, when feasible, to maintain optimal performance."；L140 — "This requires extensive re-training (e.g., 6-10 hours [78]) whenever the topology changes."
- **通信只有控制面消息**：L612 — "trafic rule distribution requires message propagation between the control center and satellites…"；L619 — "For the 4,236-satellite constellation, the propagation delays range from 2.3 ms to a maximum of 174 ms…This results in a sub-second timescale for both trafic matrix collection and rule distribution."

### 7) 训练协议
- **训练分布 vs 评估分布：刻意不同**。L245 — "We train separate models for diferent satellite constellations. For each constellation, we collect 10,000 time-varying topologies at an 1-second interval…We maintain a training to testing data size ratio of 4:1. For all experiments, the testing dataset consists of completely unseen topologies and trafic matrices from the trained model."；跨尺度泛化 L313 — "we train a model on 396 satellites and test it on various scales"；每个尺度单独训一个模型 L259。
- **无 episode 采样**（E2 零命中）；采样单位 = 1 秒间隔的拓扑快照 + 对应流量矩阵。
- **训练前数据剪枝**：流量/路径剪枝 L209 — "we retain only the non-zero elements in the trafic matrix and exclude idle paths with zero trafic input from the training dataset…pruning reduces Starlink data volumes by up to 22,381×, shrinking a data point from 335 GB to 15 MB."；等价性论证 L558 — "removing such variables and their associated constraints—including the corresponding candidate paths—does not change the feasible region, the optimal solution, or the optimal objective value of the TE problem."；拓扑剪枝 L218 — "Instead of traversing all possible topology snapshots, we train the model on a small set of representative topologies with diverse structures…when trained with 512 representative topologies for Starlink, the model can already outperform state-of-the-art approaches…using Determinantal Point Process sampling [42]."
- **训练时长有、步数无**：L282 — "SaTE outperforms Teal by 1.06× (0.284 h/0.268 h) in Iridium (66 satellites) and by 2.8× (6.28 h/2.25 h) in Mid-Size 1 (396 satellites). Additionally, SaTE achieves a 1.7× improvement over HARP (8.7 h/5.1 h) in Starlink."；**epoch/batch/LR/优化器全文未给**（E10）。硬件 L222（Azure + A100 24 核 220 GB）。超参用 grid search（L578）。
- 标签来源 Gurobi（L201）；L134 — "Commercial solvers [24] take 46 seconds for Starlink"。

### 8) 该文的算法贡献
- L45 — "SaTE formulates a heterogeneous graph that models the entire TE problem. This design eliminates the need for DNN layers, allowing GNNs to learn and solve TE entirely. This approach generalizes to unseen topologies and accommodates dynamic changes in key satellite TE components, such as varying input dimensions for network paths and trafic demands. SaTE also reduces computational latency by removing redundant relations from the graph."
- L175（关系削减）— "This simplification reduces the learning complexity, leaving three types of relational pairs: (R1) Inter-Satellite connections; (R2) Path-Satellite; and (R3) Path-Trafic."；效果 L261 — "SaTE's graph design makes computational latency primarily dependent on the number of heterogeneous graph relations—reduced in Sec. 3.2—and the number of GNN layers."
- 对应：① 输入侧＝异构图 6 字段（第 1 项）；② 网络＝纯 GAT 堆叠 + MLP decoder（第 2 项）；③ 损失＝监督回归 + 逐链路指数溢出惩罚（第 2、3 项）；④ 训练数据＝流量/路径剪枝 + 拓扑剪枝（第 7 项）。**全部围绕推理延迟与泛化性**；第 1、3、4、5、6 项的"无"即其边界证据。

### 9) 该文自述的局限
- L325 — "SaTE's model trained on a specific scale has the potential to generalize to other scales, with slight performance degradation. To further improve performance in such cases, appropriate fine-tuning using techniques like curriculum learning [25] … may be considered."
- L216 — "The pruning method is applicable only to fully GNN-based frameworks. It cannot be applied to hybrid models with DNNs."
- L199 — "Neural networks including GNNs are inherently soft constraint models, meaning they approximate solutions but do not strictly enforce hard constraints during optimization."
- L309/L714 — "some flows experience partial satisfaction—a common limitation of centralized TE algorithms focused on global objectives."；L714 — "Over 30% of satellite pairs fully meet their trafic demands, while others achieve partial satisfaction"
- L679 — "SaTE records the second-highest ofline satisfied demand, 12.8% (with laser) and 12.3% (with ground relays) lower than the theoretical upper bound [24]."
- L710 — "We observe that the loss remains below 5.2% without any rerouting when the link failure rate is under 1%."
- L595 — "An in-depth discussion on routing and access strategies is beyond the scope of this paper."

### 10) 该文没有考察的算法选择
1. **完全没有任何 RL 类选择**：无 on/off-policy、无探索、无 target network、无 replay、无 double、无 \varepsilon\-greedy（E1/E3）。"探索策略、奖励塑形、折扣因子、GAE/资格迹、episode 长度"这一整类在本文件中**不存在**（E2）。
2. **无时序建模选择**：状态侧无历史/趋势/差分/EWMA/帧堆叠（E7），也无 RNN/LSTM/GRU/时序注意力（E9 的 transformer 命中属**基线 HARP**）。
3. **无动作约束的硬处理**：无掩码/投影/剪切（E6）；只有软约束 + 事后 trim（L199），且 **trim 规则未描述**。
4. **无动作时间结构选择**：无最短驻留/驻留上限、无切换代价、无事件触发决策、无流级缓存（E8）。
5. **无信用分配的结构选择**：无逐跳/逐链路折扣回报、无反事实基线（第 3 项）。
6. **无多智能体/分布式学习选择**（第 6 项；L329）。
7. **监督学习内部亦半空白**：\\mathcal{L}_{\mathrm{supervised}}\ 的具体形式（MSE/L1/Huber/交叉熵）未给；**epoch/batch/LR/优化器全部未给**（E10）；**GNN 层数未给数值**（L578）；**注意力头数 K 未给数值**（L647）。
8. **无在线/持续学习选择**：离线训练 + 在线纯前向（L148）；对漂移的处方只有重训练/微调（L315/L325）。
9. **无鲁棒性选择**：故障只通过"容量置零"被动处理（L183 — "Link or satellite failures are handled by setting the corresponding capacities to zero"）。

### 11) 可复用的具体机制
- **M1 关系削减后的异构 TE 图**：L175 — "the 'access' relation between Satellite and Trafic is redundant because it is implicitly covered by the 'crosses' and 'transports' relations…the representation of Link can be merged into the 'connect' relation, with its link incorporated into the weight of the 'connect' relation, facilitating the use of edge-weighted attention mechanism [40]."
- **M2 边加权 GAT 消息传递 + 注意力式**（L644/L650 原文见第 2 项）+ 残差（L576 — "we incorporate residual connections into our GNN modules."）。
- **M3 标量 TE 输入到 768 维嵌入的极简初始化**（L183 + Fig.7）；**把"容量=0"当统一的节点/链路失效编码**（L183 末句）。
- **M4 混合损失 = 监督回归 + 逐链路指数加权溢出惩罚**（L565 + L571 原文，见第 2 项）。可搬点：\\alpha_i=\exp(\min(\mathrm{utilization}_i/\mathrm{capacity}_i,\alpha_{\max}))\ 实现"越接近饱和惩罚越陡"的软约束。
- **M5 可行性事后修正（trim）**：L199，且"Evaluation results in Sec. 5 account for this trimming."（**评测必须计及该修正**）。
- **M6 剪枝等价性论证模板**：L558。
- **M7 拓扑代表性采样：Graph2Vec + DPP，d=128**：L627/L629/L633 — "we use \d = 1 2 8 .\"
- **M8 网格星座快速 k 短路径（曼哈顿跳数枚举 + 跨壳拼接）**：L584 — "the minimum number of hops is the Manhattan distance \left| x _ { 1 } - x _ { 2 } \right| + \left| y _ { 1 } - y _ { 2 } \right|\ . Up to \k \stackrel { \circ } { = } \binom { | x _ { 1 } - x _ { 2 } | + | y _ { 1 } - y _ { 2 } | } { | x _ { 1 } - x _ { 2 } | }\ paths with the minimum hops can then be computed."；L586（跨壳三步法）。

### 12) 实验合同里与"负载"相关的设置（仅登记，非贡献）
- **到达过程（核心负载模型）**：L232 — "In each 1-second interval, a Poisson process with trafic intensity lambda (flows per second) generates new flows…The parameter lambda controls trafic loads…Uplink and downlink capacities are set to 50 Mbps per connection."
- **负载强度取值**：L292 — "four levels of trafic intensity: 125, 250, 375, 500 flows/s"；高负载点 L286 — "under high trafic intensity (500 flows/s)"。
- **空间负载分布（不平坦）**：L668 公式 \p _ { \alpha } = \frac { \mathrm { P o p u l a t i o n ~ D e n s i t y ~ i n ~ G r i d } \alpha + \gamma } { \sum _ { \alpha } ( \mathrm { P o p u l a t i o n ~ D e n s i t y ~ i n ~ G r i d } \alpha + \gamma ) } ,\；L671 — "The trafic intensity between grids 𝛼 and \beta\ is \lambda p _ { \alpha } p _ { \beta } .\ , aligned with user distribution."；3M 用户 + 1000 网关。
- **业务混合（Table 2）**：Voice 64 Kbps / 1–10 min；Video 8 Mbps / 5–30 min；File Transfer 50 Mbps / 26–130 min（脚注 G.711 / 1080P / 10–50 GB）。
- **拓扑规模**：L224 — "Starlink (Phase 1), with 4,236 satellites."；L228 — Iridium 66 星单壳 781 km；Mid-Size 396 与 1584；L661 Table 4 四壳 540/550/560/570 km。
- **ISL 容量**：L226 — "All links via lasers and ground relay have a capacity limit of 200 Mbps"（对照物理能力 L72 "up to 200 Gbps"，仿真取值保守）。
- **路径预配置规模**：每对 10 条（L234）；L205 流量矩阵 4236×4236（72 GB）与路径矩阵（263 GB）。
- **在线评测口径**：L251 + L292（基线重算周期 47/25/54 s）。
- **对比算法（6 个）**：L247 — Gurobi、POP、ECMP with Water Filling、Satellite Routing（backpressure）、Teal、HARP。
- **指标**：computational latency（L249）、satisfied demand（L251）、MLU（L697）、flow 级 CV（L714）。
- **故障压力条件**：L708 — "We randomly induce link failures in Starlink at rates of 0.1%, 1%, and 5% per TE interval, making 1.2%, 8.7%, and 18.6% configured paths invalid."
- 结果口径（登记）：L294 — "an average improvement of 23.5% (via lasers) and 46.6% (via ground relays) over the respective best-performing baselines [24, 35]"。

---

## 8. WFA3CZLP — FlexSATE: Flexible and Distributed Traffic Engineering with Supervised Learning in Ultra-Dense Low-Earth-Orbit Satellite Networks

（正文 L1–L158 读完；References L160–L177 未逐条读。**前置结论：本文不是 RL 论文**——它是"集中式 MHBT 多路径预计算 + 离线监督学习（标签由 MCF 线性规划给出）+ 分布式前向推理"。因此第 1–7 项中的 MDP/奖励/更新式/信用分配等要素**全部为"未见"，其替代物是回归/线性规划接口**。）

### 1) MDP 定义
- **未见 MDP**。检索：\grep -ciE "reinforcement|q-learning|reward|exploration|mdp"\ 对该篇全文 → **4 命中，全部在参考文献标题**（L164 ref[2] "…with reinforcement learning in software-defined networks"、L168 ref[4] "Experience-driven networking: A deep reinforcement learning based approach"、L170 ref[5] "…combining destination-based routing with reinforcement learning"、L178 ref[9] "Distributed and adaptive traffic engineering with deep reinforcement learning"）。**正文零命中**。
- **输入的"状态"（逐字段，来自 L109 逐字）**：L109 — "The encoder takes two inputs into consideration: node features and a node adjacency matrix. The node features represent a series of demands originating from each network node, while the adjacency matrix provides information about the neighbors of each node."
  即：① **流量矩阵 TM**（"a traffic demand represents the aggregate traffic entering the network from an entry satellite and exiting the network from an exit satellite. A traffic matrix (TM) encompasses the collection of demands between all possible pairs of different satellites"，L35）；② **邻接矩阵**（拓扑连通性）。
  **维度**：嵌入维 128、注意力头 4、FFN 256、注意力层 H=4（L128）。**归一化**：未见（全文无 normaliz）。**时间聚合**：TM 逐次生成（"The traffic volume for each demand varying over time"，L35），**无历史/窗口**。
- **动作（= 输出）**：**多路径流量分配比例**。L109 — "a decoder consists of one readout function R, which is used to decode the corresponding multipath traffic distribution from the graph embedding. For a given network node \v ,\ R interprets the graph embedding as multipath traffic split ratio \sigma _ { p } ^ { v , d } , d \in D _ { v } , p \in P ^ { v , d }\ , where \D _ { v }\ is the destination node set of node \v , P ^ { v , d }\ is the preconfigured path set of pair \< v , d >\ satisfying \sum _ { p \in P ^ { v , d } } \sigma _ { p } ^ { \bar { v , d } } = 1\ ."
  **动作空间** = 每对 (v,d) 上的路径**比例单纯形**；**无动作掩码**；解码器输出维 = \| V | * | P |\（L128）。
- **奖励：未见**。等价目标是 MLU 最小化。L35 — "The objective of TE is to efficiently deliver these dynamic traffic demands, aiming to optimize a specific objective, such as minimizing the maximum link utilization (MLU)."；离线标签来源 L116 — "we address a modified MCF problem to obtain the ground truth optimal path traffic split ratios…aiming to minimize the MLU. Upon solving the aforementioned problem using LP solvers \( \mathrm { e . g . } ,\ Gurobi [5]), the optimal explicit path traffic split ratios for each flow can be obtained."
  **无折扣 \gamma\**（全文无 discount/gamma）。
- **转移/终止：未见**。系统是两阶段周期结构：**路径选择（集中、慢、按拓扑变化触发）** + **速率自适应（分布、快、持续）**。L40 — "We deploy the relatively slow and costly operation of path selection in the centralized controller…Due to the relatively fast operation of rate adaptation, it can be performed continuously as network conditions evolve."
- **拓扑/routing 约束（本文的"环境模型"）**：L35 — "Each satellite establishes 4 links, two for intra-orbit links and two for inter-orbit links."；最短跳数分解 L48 — "\H _ { M H } = H _ { x } + H _ { y }\"

### 2) 学习算法与更新式
- **算法名与范式**：监督学习（SL）+ GNN。L107 节标题 "A. Customized SL Approach Coupled with GNN Architecture"；L29 — "We propose a customized supervised learning (SL) approach coupled with Graph Neural Network (GNN) architecture that predicts the optimal multipath traffic distribution for each satellite."
- **网络结构**（L109 逐字）："FlexSATE consists of a encoder that performs node-wise message exchange, and a decoder interprets desired multipath traffic distribution from updated and encoded node features… The encoder employs a shared feed-forward layer to compute an initial node embedding. Subsequently, each node's embedding is updated through message exchange with its neighboring nodes. The embedding update module, inspired by the transformer model introduced in [8], consists of a stack of H identical attention layers. Once message exchange phases are done, we need to concatenate all node embeddings outputted by the encoder to form a graph embedding \h _ { G } ,\ because each node's embedding \h _ { v }\ only includes partial information of the whole network."
  **层数/宽度**：L128 — "The encoder of the prediction model is configured with an embedding dimension of 128 and attention heads of 4. The feed-forward sub-layer in each attention layer has a dimension of 256, and the model consists of 4 attention layers H. The decoder's readout function R is designed with an output dimension equal to \| V | * | P |\ . During training, we set the initial learning rate to \1 0 ^ { - 4 }\ and the batch size to 64."
  **激活函数：未给**。**参数共享：明确共享**——L109 末句 — "in our approach, each node can share and reuse the encoder and decoder model, thereby significantly simplifying the complexity and substantially reducing training and inference time."
  **图算子**：message passing + attention（transformer 式）。
- **更新式/损失：未见**。检索 \grep -n -i -E "loss function|loss|cross-entropy|MSE|mean squared"\ → **0 命中**。训练是"标签回归"：L118 — "We generate a dataset of training samples that includes different input network states and their corresponding target output distributions. Each training sample includes the network-wide traffic matrix and the adjacency matrix as input. The output comprises the target traffic distribution which is determined by calculating the global optimal path traffic split ratios based on the given inputs."
  即**监督回归 + 逆优化标签（MCF/LP）**，无 TD 目标、无 loss 公式、无 target net、无 replay（后者亦无检索命中可查——见第 10 项计数）。
- **推理契约（重要）**：L124 — "Each LEO satellite floods traffic demand messages periodically over the entire network and connectivity messages once the link interruption/reestablishment occurs. Each satellite inputs the converted state matrix into FlexSATE to output the predicted optimal traffic distribution. In this way, each LEO satellite performs the local routing decision in a distributed manner."

### 3) 信用分配
- **未见任何"信用分配"机制**：既无逐跳即时奖励，也无路径级终局奖励。所有学习信号来自**标签的逐元素回归**（L118：target = 全局最优 split ratios）。
- 可类比为"信用"的只有**逐链路占用被计入路径代价**这一点，且它是**路由算法侧**（非学习侧）的：L68 — "The cumulative usage of that edge contained in the selected path is factored into the path cost, ensuring good load balancing."
- **是否区分损失原因：未见**（无失败原因相关概念）。

### 4) 状态里有没有时间信息
- **没有显式时间特征**（嵌入维度 128 的描述 L128 只给维度，不给时间窗；全文无 EWMA/sliding window 语句）。
- 时间进入系统的方式是**周期重算 + 拓扑变化触发**：L124（周期性洪泛需求、链路中断时洪泛连通性）；L120 — "we can periodically conduct the process of offline training, thereby updating the FlexSATE model with newly collected samples."
- 时变本身由环境提供：L35 — "with the traffic volume for each demand varying over time"；L128 — "Random link failures are introduced at specific times to simulate dynamic topology changes."

### 5) 动作有没有时间结构
- **动作是流量分配比例，且能"连续"调整**：L40 — "The system has the capability to update weights to rebalance the load when traffic demands change."
- **两级时间结构（本文最明确的一处时间设计）**：**慢**——"the relatively slow and costly operation of path selection…should be executed infrequently, such as when topology changes occur."（L21/L40）；**快**——"Since updating path weights is a relatively fast operation, rate adaptation can be performed continuously to accommodate changes in states."（L21）
- **切换代价：未见**（无 handover/switch cost 语句）。

### 6) 多智能体设定
- **严格说不是 MARL，但是"分布式部署 + 共享模型"**：L40 — "A GNN-based model, denoted as an agent, is distributed on each satellite in the network."；L124 — "FlexSATE deploys the trained model in each satellite to predict the optimal traffic distribution to perform local routing decision distributedly, so as to achieve near-optimal TE performance with low computation/communication overhead."
- **共享参数：是**（L109 — "each node can share and reuse the encoder and decoder model"）。
- **非平稳：以"卫星同构"为由回避**。L120 — "Due to the symmetrical and uniform characteristics of the constellation configuration, each satellite plays an equivalent role in constructing the network topology. That is, the network-wide traffic demand distribution and topology connectivity seen from any satellite at one time may be seen by any other satellite at other times. Inspired by the above findings, we can design and modify the input and output of the neural network from the perspective of satellite observation and decision-making… we can only predict the distribution of traffic demands originated from the current node based on the satellite homogeneity, which can greatly simplify the design of the neural network model."
  坐标规范化做法 L120 — "For building new views, the current satellite label is 0 by default, and the other satellite labels are changed to new labels based on the symmetrical and uniform constellation configuration."
- **通信**：**周期性全网洪泛 + 事件触发的连通性洪泛**（L124）。
- **动作同步：未见**（无同步机制描述）。

### 7) 训练协议
- **训练分布 = 随机 TM + 随机链路故障**：L128 — "At 570 km altitude, 720 satellites are evenly distributed on 36 orbits at a 70-degree orbit inclination. Random link failures are introduced at specific times to simulate dynamic topology changes. For each TM generation, we randomly select satellite pairs to generate traffic demand between 10 Mbps and 400 Mbps. In addition, we set the capacity of inter-satellite laser link to 11 Gbps."
- **训练/评估划分：未见明确划分声明**（无 train/test split 语句）；评估以不同 flow 数扫描：L132 — "we generate different flow numbers in each experiment."
- **训练量/时长：未给**（只给学习率 \10^{-4}\、batch 64，L128）。
- **对比算法（L130）**：Top-K（K = 需求数的四分之一 — "In the experiment, we let the value of K be one quarter of the demand number."）、ECMP、Greedy。
- 计算开销测量口径 L134 — "We use the same 4-core Intel 2.4GHz CPU to measure all the computation overheads, with Gurobi utilized as an LP solver"

### 8) 该文的算法贡献
- L25 — "We propose a new TE system called FlexSATE for large-scale LEO satellite networks… The centralized controller computes forwarding paths considering cumulative path occupation from a global view. The rate adaptation is performed distributedly in each LEO satellite."
- L27 — "We develop a simple yet efficient multipath routing algorithm for the grid topology of Walker-delta type LEO satellite networks… By constructing a MHBT, we propose an MHBT-based k-segment Routing algorithm, which flexibly restricts the path search to the minimum hop path (MHP) region and is capable of promptly discovering multiple paths."
- L29 — "We propose a customized supervised learning (SL) approach coupled with Graph Neural Network (GNN) architecture that predicts the optimal multipath traffic distribution for each satellite. To achieve global optimal performance, FlexSATE utilizes offline centralized learning guided by optimal multipath traffic split ratios obtained from a modified Multi-Commodity Flow (MCF) problem."
- 对应：① 输入＝TM+邻接矩阵（第 1 项）；② 网络＝128 维 transformer 编码器 + readout 解码器（第 2 项）；③ 标签＝MCF/LP 最优比例（第 1、3 项）；④ 部署＝每星共享同一模型分布式推理（第 6 项）；⑤ 两级时间结构＝慢路径选择 + 快速率自适应（第 5 项）。

### 9) 该文自述的局限
**未见 Limitations/Future Work 小节**。检索 \grep -n -i -E "limitation|future work|future direction"\ → **唯一命中 L134**，且是在**评价对比算法**（"KMCF can achieve near-optimal MLU performance, however, it faces limitations in accommodating traffic fluctuations in time as the network size increases."），不是自述。结论段（L151）只重述贡献。

### 10) 该文没有考察的算法选择
**检索范围 = 该篇 MD 全文 178 行**：

| 模式 | 计数 | 判读 |
|---|---|---|
| \grep -ciE "reinforcement\|q-learning\|reward\|exploration\|mdp"\ | **4** | **有命中，全部构不成反例**：L164/L168/L170/L178 的 4 处均在 **REFERENCES 的论文标题**里（他文），正文 0 命中 |
| \grep -n -i -E "loss function\|loss\|cross-entropy\|MSE\|mean squared"\ | **0** | **监督损失的函数形式完全未给**（只有"regression to labels"的定性描述 L118） |
| \grep -ciE "target network\|replay\|experience pool\|double q"\ | **0** | 无 replay/target net/double |
| \grep -ciE "EWMA\|exponential moving\|moving average\|history\|historical\|previous state\|trend"\ | **0** | 状态无时间历史 |
| \grep -ciE "action mask\|invalid action\|impossible action\|mask"\ | **0** | 无动作掩码（比例输出靠什么保证满足容量约束**未说明**） |
| \grep -ciE "eligibility\|n-step\|multi-step"\ | **0** | 无资格迹/n 步 |
| \grep -ciE "discount\|gamma"\ | **0** | 无折扣 |

1. **RL 全套**：未考察（正文 0 命中）——包括探索、奖励、折扣、价值 bootstrap、非平稳处理。
2. **监督损失的函数形式**：未给（第 2 项）。
3. **约束满足机制**：输出是比例（\sum\sigma=1\）但**如何保证不超链路容量、超了怎么办，正文未说明**（与 SaTE 的 trim 形成对照）。
4. **激活函数、正则化、优化器**：未给。
5. **训练/评估分布划分**：未声明。
6. **切换/重配置代价**：未考察。
7. **状态的时间编码**：未考察。

### 11) 可复用的具体机制
1. **MHBT 枚举 + 候选路径过滤三准则**（低时延/高多样性/负载均衡）。L68 — "the minimum-hop path can guarantee the low-latency property. Diversity requirements can be achieved by choosing as many paths as disjoint as possible. The cumulative usage of that edge contained in the selected path is factored into the path cost, ensuring good load balancing."；构造细节 L61 — "there exists a unique root node that represents the source satellite, along with several leaf nodes that represent the destinations satellites. The leaf node number is equivalent to the number of paths connecting the source to the destination… each node's left branch corresponds to movement along the x-axis… the right branch indicates the right child-node can be reached after a single hop along the y-axis. Moreover, the level \H _ { T }\ of destination node can be obtained by \H _ { T } = H _ { M H } + 1\"（Algorithm 1 全文见 L70–L103 代码块，含递推 \v _ { h , j } = \Big ( \big ( x _ { v _ { h - 1 , i } } + M + \vec { H } _ { x } / | \vec { H } _ { x } | \big ) \% M , y _ { v _ { h - 1 , i } } \Big )\ L81）。
2. **曼哈顿街网跳数闭式**（L50）：\H _ { x } = \operatorname* { m i n } \{ \left| s _ { x } - d _ { x } \right| , M - \left| s _ { x } - d _ { x } \right| \}\、\H _ { y } = \left\{ \left| s _ { y } - d _ { y } \right| , N - \left| s _ { y } - d _ { y } \right| \right\}\——**可直接搬到我们平台的网格星座最短跳数与方向判定**。
3. **"卫星同构 ⇒ 以本星为标签 0 做坐标规范化"的输入构造**（L120）：把"全网 TM+邻接矩阵"降为"以本星视角的规范型"，从而只需要一个共享模型。**这是解决"分布式部署 + 全局信息"矛盾的实用手法。**
4. **两级控制节拍**：慢（拓扑变化才重算路径）+ 快（速率自适应持续）——L21/L40。**与本批 JLF7IEBQ 的 1 s/15 s 节拍一起，构成我们平台"控制周期"设计的可引用基线。**
5. **逆优化标签生成**：L116 — 用 MCF/LP 生成 \sigma\ 标签（Gurobi），把"难解但可离线"的优化问题蒸馏成"快但近似"的网络。

### 12) 实验合同里与"负载"相关的设置（仅登记，非贡献）
- 拓扑：L128 — "At 570 km altitude, 720 satellites are evenly distributed on 36 orbits at a 70-degree orbit inclination."（镜像 Starlink shell 2）
- 链路容量：ISL 11 Gbps（L128）。
- 故障：L128 — "Random link failures are introduced at specific times to simulate dynamic topology changes."
- **负载生成**：L128 — "For each TM generation, we randomly select satellite pairs to generate traffic demand between 10 Mbps and 400 Mbps."
- **负载扫描（flow 数）**：L132 — "In order to simulate different traffic distributions and patterns, we generate different flow numbers in each experiment."；图中给出 100 / 500 / 900 flows（L137/L140/L143 图题），文中提及 900 与 1100 flows 的拥塞点（L132 — "when 900 flows are injected into the network, ECMP will cause severe network congestion…with a significant increase in the presence of 900 and 1100 flows, respectively."）
- 指标：**MLU 的 CDF**（图 5，L132）、平均端到端时延（图 6，L132）、计算开销（图 7，L134）。
- 对比算法：Top-K（K = 需求数的 1/4）、ECMP、Greedy（L130）；对照的全局最优由 KMCF（K = 总需求数时）给出（L132 — "Note that if the K value is equal to the total number of flows, it is the KMCF scheme."）。
- 报告口径（登记）：L134 — "With an inference time of only tens of milliseconds, FlexSATE's GNN architecture enables it to promptly predict the optimal traffic distribution in less than one second… centralized TE schemes such as KMCF, Greedy, and Top-k take several minutes to solve global optimal routing"

---

## 9. UF8IQTA2 — Traffic-Predictive Routing Strategy for Satellite Networks（G-AODV）

（正文 L1–L313 全部读完；L314–L369 References 未逐条读，仅查 L364–L368 核对基线出处。**前置结论：本文不是 RL 论文**——它是对 AODV 的启发式协议改进（流量预测门控 + 拥塞信号改路 + 基于稳定性的断链修复）。判定证据：`grep -n -oiE 'reinforcement|\brl\'` → **0 命中**；`grep -n -oiE '\bmdp\|markov|bellman|q-value|value function'` → **0 命中**；`grep -n -oiE '\bagent\|\bagents\'` → **0 命中**。故第 1–7 项按"RL 要素有/无" + "原文实际存在的结构替身"两层写。）

### 1) MDP 定义
- **未见 MDP 定义**（检索范围：全文 369 行）：`\bmdp\|markov|bellman|q-value|q function|value function` → **0**；`gamma|discount|horizon|episode|step size|learning rate` → **0**；`reward|penalt|payoff|utility|return` → **2 命中，均非奖励**（L61 "the destination node returns a response packet (RREP packet)"、L132 "an RREP packet is returned to the source node along the reverse request path"——动词 returns/returned，**不构成反例**）；`eligibility|n-step|multi-step|bootstrap|temporal difference|td error|trace|credit assign` → **0**。
- **"状态"逐字段（协议字段，非张量）**：
  - **A Curr_traffic_i**（当前流量负荷）：L101 — "Curr\_\tra\f f i c _ { i }\ represents the current traffic load value of the satellite node \i\ "；Table 1（L49）— "Current traffic load value."。标量；无归一化；瞬时值。
  - **B Next_traffic_i**（下一时刻预测流量）：L49 — "The traffic load value for the next moment"；L90 — "each satellite node utilizes the traffic prediction model from the literature [23] to forecast the traffic value Next\_\traffic_i\ for the next time step."。标量；无归一化；**单步前瞻**。
  - **C 邻居列表（per-neighbor 的 A+B，经 HELLO 采集）**：L86 — "Each satellite node sends HELLO packets to the neighbor node to detect the current traffic value and the predicted traffic value."；Table 2 "Improving the HELLO package"（L93）逐字含 Curr_traffic 与 Next_traffic 两个字段。维度 = 2n 标量；**每条记录只有当前值与一步预测值两项，无历史**。
  - **D 阈值 L（由 A+B 派生）**：L95 — "The traffic threshold L is defined based on the arithmetic average of the actual traffic values and prediction values of all neighboring nodes in the neighbor list."
  - **E 路由表 10 字段（Table 5, L145）**，其中新增 4 个：L142 — "In the routing table, add four fields: hop count, number of hops required to reach the destination node, next two-hop nodes and upper two-hop node. ... Compared with the original routing table, 16 bytes of data are added to the improved routing table."
  - **F hopS/hopD**：L49 — "The number of hops a data packet takes from the source node to the broken node." / "The number of hops required for a data packet to travel from the broken node to the destination node."；使用规则 L149 — "By comparing hopS and hopD, select the corresponding route repair method."
  - **G STA_i（节点稳定性，唯一的"两时刻"量）**：见第 4 项公式。
  - **H TAG_CONGEST（粘滞布尔路由状态）**：L113 — "The G-AODV protocol adds routing congestion status (TAG\_\CONGEST) and congestion control signal (RCS) based on the original AODV routing protocol."
- **归一化总检索**：`grep -n -oiE 'normaliz|normalis|standardiz'` → **0 命中**；`'rescal|min-max'` → **0 命中**。**全文无任何输入归一化**。**随时间聚合**：仅字段 G；`grep -n -oiE 'ewma|exponentially weighted|moving average|sliding window|time window|timestamp|window size'` → **0 命中**。
- **动作（无"动作空间"的形式定义，只有决策规则）**，实为三类：
  (a) **逐 RREQ 二值门控** {转发, 拒绝并回发 RCS}：L105 — "packet is forwarded; otherwise, a congestion control signal is sent to the upstream node, and the upstream node performs path replacement at the same time."；判据 L107（**该行行首有一个 0x1A 控制字节，属 MinerU 乱码，逐字照抄**）— " Next\_\tra\f f i c _ { i } > L\ , The node is congested and the path needs to be replaced. \Next \_ t r a f f i c _ { i } \leq L\ , Receive RREQ packet and forward it"。
  ⚠ **原文自相出入**：L103 写 "is less than"，L107 写 "\leq\"。**照抄并列，不替作者消歧。**
  (b) **下一跳重选**：L113 — "The upstream node will use this information to reselect neighbor nodes to forward the routing request packet."——**无选择规则/打分函数**（这正是 RL 化的天然缺口）。
  (c) **断链修复二选一** {source node repair, local repair}，local repair 再选发起方：L153 — "when ho\9 S < h o p D .\ , the source node repair is used"；L160 — "when h\p S \geq h o p D ,\ local repair is used"；L181 — "If the stability of the upstream node at the break is greater than that of the downstream node, the upstream node initiates the route local repair process."
- **动作掩码**：无形式化掩码（`grep -n -oiE 'mask|feasib'` → 仅 1 命中于 L203 的 "feasibility"，与动作空间无关）；但 L107 的门控在效果上等价于一个**硬掩码**。
- **奖励：无 r_t**（`grep -n -oiE 'reward|penalt|payoff|utility'` → **0 命中**）。全文 6 个编号式全部是门限/稳定性/评测 KPI，逐字列出：
  - 公式 (1) L98：`L = \frac { 1 } { n } { \sum _ { i = 1 } ^ { n } \frac { C u r r \_ t r a f f i c _ { i } + N e x t \_ t r a f f i c _ { i } } { 2 } }\（**求和下标 i 是邻居，而 L101 把 Curr_traffic_i 描述为 "of the satellite node i"——原文未消歧，我不替它选**）
  - 公式 (3) L174：`S T A _ { i } = \frac { V _ { i } ( t _ { 1 } ) \cap V _ { i } ( t _ { 2 } ) } { V _ { i } ( t _ { 1 } ) \cup V _ { i } ( t _ { 2 } ) }\
  - 公式 (4)(5)(6) L217/L227/L237：`P d e l i v e r y = \frac { P _ { R } } { P _ { S } }\、`A v d e l a y = \frac { 1 } { N } { \sum _ { i = 0 } ^ { N } } ( R _ { t i m e } ( i ) - S _ { t i m e } ( i ) )\、`P l o s s = \frac { P _ { l } } { P _ { S } }\
  **无奖励系数、无折扣 \gamma\、无归一化**。
- **转移/终止**：无 episode（`grep 'episode'` → 0）；协议终止条件 L132（Table 4）— "Step 10: Data transmission is completed, and an effective route from the source node to the destination node is obtained."；维护终止 L199 — "Step 11: The maintenance process is completed."

### 2) 学习算法与更新式
- **判定：无学习算法、无 TD 目标、无损失、无 target net、无 replay**。检索（全文 369 行）：`grep -n -oiE 'target network|replay|double|experience buffer|off-policy|on-policy'` → **0 命中**；`grep -n -oiE 'train(ing|ed)?\b\'` → **0 命中**（唯一 "train" 子串在 L328 参考文献标题 "constraint" 内——**不构成反例**）；`grep -n -oiE 'epoch|batch|gradient|loss function|backprop|learning rate'` → **0**；`grep -n -oiE 'hidden layer|neuron|activation function|relu|sigmoid|softmax|fully connected'` → **0**；`grep -n -oiE 'graph neural|\bgnn\|adjacency|message passing|graph convolution'` → **0**。
- **唯一"模型"是外借的黑箱预测器（不是本文贡献）**：L88 — "the literature [23] proposes an innovative satellite network traffic prediction strategy based on an improved Gated Recurrent Unit (GRU) neural network. This forecasting method cleverly integrates attention mechanisms with the GRU neural network ... To further optimize model performance, a Particle Swarm Optimization (PSO) algorithm is introduced..."；L90 — "each satellite node utilizes the traffic prediction model from the literature [23]"。**网络结构规格（层数/宽度/激活/是否共享）本文一概未给**；引文 [23]（L360）才有。
- **最接近"更新式"的是协议状态更新**：L199 — "Step 3: Add 1 to the destination node sequence number in the routing table, and set the routing flag bit to the route invalid state."
- **唯一的"收敛"陈述**：L298 — "After 280 iterations, the algorithm successfully achieved a satisfactory convergence state."（**"iterations" 优化什么、步长多少，全文未定义**）。

### 3) 信用分配
- **判定：无奖励、无信用分配机制**。但有一条**显式的一跳反向信令**在结构上扮演"信用回传"角色——这是本文真正可搬的部分。
- L122 逐字 — "The satellite node sends a congestion control signal to inform the upstream node that its downstream node may become a congested node and therefore cannot accept new business traffic. After the downstream node constructs a congestion control signal and sends it out, it sets the routing status in the routing table to the TAG\_\CONGEST status. In the route congestion state, the upstream node will cache the data packets sent to the downstream node, and the downstream node will not accept any RREQ packets. Therefore, the downstream nodes have enough time to relieve their heavy load conditions."
- 报文仅 3 字段（L118/L120）— "rc\_\dst: the previous hop address of the current data packet. rc\_\S\_\address: The source node address of the current packet. rc\_\D\_\address: The destination node address of the current data packet."
- **分解到节点而非链路**（第 1 项字段 A–D）；链路只以 STA（公式 3）形式在维护阶段出现。
- **是否区分损失原因**：**只在叙述层面**（L234 — "some data packets will be lost due to network congestion, route breaks and other reasons."），机制上分流为拥塞→RCS/TAG_CONGEST（L113/L122）、断链→RERR（L199 Step 4），**没有任何信号或损失函数把原因区分开**。

### 4) 状态里有没有时间信息
- **有，但只有"单步前瞻"一种，且来自外借模型**（字段 B，L90/L95 — "traffic prediction values provide an estimate of future load trends."）；**窗口长度/采样周期/预测时域数值全文未给**。
- **趋势/differencing/EWMA：无**（`grep -n -oiE 'ewma|exponentially weighted|moving average|sliding window|time window|timestamp|window size'` → **0 命中**；`'history|historical'` → 1 命中于 L59，指文献 [15] 的 "historical delivery success rate"，**与本文状态无关**；`'trend'` 的命中均为"曲线趋势"叙述词，**不是状态差分项**）。
- **唯一跨时刻状态量是 STA_i**（公式 3 L174），时间间隔定义 L177 — "the time interval for calculating node stability is set as the survival time of the link after the node receives the HELLO message sent by the neighbor node."

### 5) 动作有没有时间结构
- **路由发现期：每 RREQ 独立门控**（L86/L107）；**路由建立后：路径级驻留**，不再逐包决策 — L138 — "In the G-AODV protocol, once a transmission path is established, the path enters the routing maintenance phase."
- **无驻留计时器/迟滞/摊销**：`grep -n -oiE 'dwell|hysteres|amortiz|per-packet|flow-level|session|stickiness|minimum duration'` → **0 命中**。
- **切换有明确代价（原文唯一一处"切换代价"）**：改路时上游缓存数据包（L122/L124 — "the upstream node caches the data packets of the route ... and sends an RREQ request to the neighbor node."）；**但缓存容量/时延/丢弃量均未建模**（`grep 'queue length|buffer occupancy|backlog'` → 0）。
- **触发式与周期式并存**：周期 HELLO（L86/L90）+ 事件触发（断链 L199 Step 1、RCS 到达 L113/L124）。

### 6) 多智能体设定
- **判定：不存在多智能体学习设定**（`grep -n -oiE 'agent\b|\bagents\b'` → **0 命中**）。
- 每节点独立按同一套规则本地决策，**无集中控制器、无集中 critic**：L90 — "individual satellite nodes broadcast HELLO packets to neighboring nodes to probe the network traffic load in their vicinity."
- **"共享"是算法同构式的**（所有节点用同一个 [23] 预测模型，L90），**不是学习参数共享**——路由器里没有可学习参数。
- **非平稳：未处理**（`grep -n -oiE 'non-stationar'` → 0）；作者把拓扑/负载漂移列为**局限**（第 9 项 L304）。
- **通信是唯一协调手段**：HELLO（携带 Next_traffic，L90/L93）、RCS（L113–L124）、RREQ/RREP/RERR（Table 1 L49、L199）。**无动作同步**（`grep 'synchron'` → 0）。

### 7) 训练协议
- **判定：没有训练协议**（无可学习的路由策略）。此处登记评估协议与唯一的迭代陈述。
- **训练分布 vs 评估分布**：不存在训练，故无二者之分。
- 平台：L203 — "This article uses STK (Satellite Tool Kit) to build simulated Iridium constellation data. Build a satellite network simulation model in NS2 (Network Simulator Version 2)..."
- **拓扑规模：无具体节点数**（仅符号 \N\，L169；L298/L302/L304 只有 "large-scale"/"a large number of nodes" 定性词）。
- 运动学：L246 — "the operational speed of the satellite nodes is set to 7.9 km\/\s\ ,\ equivalent to the first cosmic velocity... a pause time of 0 s is set."
- **无训练步数**；唯一数值 L298 的 "280 iterations"（含义未定义）。单次仿真时长未给。
- **无统计协议**：`grep -n -oiE 'seed|repeat|average over|confidence interval|variance|statistical signific'` → **0 命中**（而 L302 仍写 "provide robust statistical evidence for our experiments"，**原文如此，我照抄不背书**）。

### 8) 该文的算法贡献
- **贡献 1**（对应第 1 项动作门控 + 第 4 项状态输入）L40 — "During the route discovery phase, a traffic prediction mechanism is introduced. Predicting the satellite's traffic load for the next moment in advance is achieved through a neural network model. Based on the predicted traffic load and a comparison with a traffic threshold, data packets are selectively forwarded to prevent heavily loaded nodes from being included in the final established route."
  具体改动：把 AODV 的"无条件转发"（L61 — "the intermediate node receiving the routing request packet will continue to forward the packet, namely the RREQ packet, regardless of the current load intensity"）改成公式 (2) 门控（L107），并把 Next_traffic 加进 HELLO/邻居表。
- **贡献 2**（对应第 3 项信用回传 + 第 5 项切换代价）L42 — "Add a path change mechanism during routing. In this mechanism, congestion control signals are designed. Nodes that may be congested inform upstream nodes of changing paths in advance to avoid increasing congestion and achieve load balancing."
- **贡献 3**（对应第 1 项字段 E/F/G + 第 5 项动作集）L44 — "the routing table is improved, and the concept of node stability is introduced in the route maintenance stage. According to the location of the fracture, choose the source node repair or local repair. In the local restoration, the stability of the upstream and downstream nodes of the fracture was compared."
- **一句话**：给 AODV 打三个协议级补丁：(i) 外借 GRU 预测值 + 自校准阈值做逐跳准入门控；(ii) 一跳反向 RCS + 上游缓存做拥塞前改路；(iii) 2 跳路由表 + 邻居集合 Jaccard 稳定性选择断链修复方。**第 1–7 项中"学习/MDP/奖励/信用分配/时间抽象"的要素，本文一个都没有。**

### 9) 该文自述的局限
L304 逐字 — "After simulation verification, this method has greatly improved performance, but it also has some limitations. In real-time applications, such as video communications or emergency communications, routing decisions based on traffic prediction may introduce some additional delays... Additionally, using neural networks for traffic prediction may require substantial energy and computing resources, especially in satellite networks with a large number of nodes and limited resources. It should be noted that the satellite network topology changes frequently, including the addition and departure of nodes, the interruption of links, etc. In this case, the predictive model needs to be adjusted in time to adapt to changes, otherwise its accuracy will be affected."
另有 L298（复杂度代价，该行 MinerU 双写、含 "atention" 拼写错误，照抄）与 L310 — "Data Availability Statement: The processed data required to reproduce these findings cannot be shared as the data also form part of an ongoing study."

### 10) 该文没有考察的算法选择
统一检索范围：全文 369 行。**下表逐条给模式与实测计数；凡有命中一律说明为何不构成反例。**

| # | 未考察的选择 | 检索模式 → 实测计数（判读） |
|---|---|---|
| 1 | 任何 RL 形式化（MDP/状态-动作-奖励三元组） | `\bmdp\|markov|bellman|q-value|q function|value function` → **0**；`reinforcement|\brl\\ → **0** |
| 2 | 学习型价值/策略网络 | 同上 → 0；全文无可学习参数 |
| 3 | TD 目标/Bellman 备份/损失/梯度 | `eligibility|n-step|multi-step|bootstrap|temporal difference|td error|trace|credit assign` → **0**；`epoch|batch|gradient|loss function|backprop|learning rate` → **0** |
| 4 | target network / replay / double | `target network|replay|double|experience buffer|off-policy|on-policy` → **0**（**连 'double' 都 0**） |
| 5 | 折扣因子 \gamma\ / 时域 / episode | `gamma|discount|horizon|episode|step size` → **0** |
| 6 | 探索-利用权衡 | `epsilon|explor` → **0** |
| 7 | 奖励塑形/多目标加权 | `reward|penalt|payoff|utility` → **0**（仅 returns/returned 动词） |
| 8 | 状态归一化 | `normaliz|normalis|standardiz` → **0**；`rescal|min-max` → 0 |
| 9 | 状态含历史/EWMA/滑窗/差分 | `ewma|exponentially weighted|moving average|sliding window|time window|timestamp|window size` → **0** |
| 10 | 图算子/邻接矩阵建模 | `graph neural|\bgnn\|adjacency|message passing|graph convolution` → **0** |
| 11 | 神经网络结构（含外借预测器） | `hidden layer|neuron|activation function|relu|sigmoid|softmax|fully connected` → **0** |
| 12 | 多智能体设定 | `\bagent\|\bagents\\ → **0**；`multi-agent|multiagent|centraliz|decentraliz|independen|shared parameter|synchron|non-stationar` → **0**（仅 L65/L348/L354 命中 "cooperat"，属相关工作/参考文献，**不构成反例**） |
| 13 | 动作驻留/迟滞/最小驻留 | `dwell|hysteres|amortiz|stickiness|minimum duration` → **0** |
| 14 | 队列/缓存占用作为状态 | `queue length|buffer occupancy|backlog` → **0**（"buffer" 仅 L252 定性提及） |
| 15 | 能量作为状态 | `energy|residual` → **2 命中，均非状态**：L304（自述局限）、L338（参考文献标题 "…Energy Systems"） |
| 16 | 训练协议/超参搜索 | 预测器来自 [23]（L88/L90）；**本文无任何训练超参** |
| 17 | 统计显著性协议 | `seed|repeat|average over|confidence interval|variance|statistical signific` → **0** |
| 18 | 动作掩码形式化 | `mask|feasib` → **1 命中，不构成反例**：L203 的 "feasibility" 指算法可行性，与动作空间无关 |

### 11) 可复用的具体机制
- **M1 自校准动态阈值（相对门控，无需全局超参常数）**：公式 (1) L98 逐字 `L = \frac { 1 } { n } { \sum _ { i = 1 } ^ { n } \frac { C u r r \_ t r a f f i c _ { i } + N e x t \_ t r a f f i c _ { i } } { 2 } }\ + L95。**门限与被控量同量纲、随邻域负载漂移**，天然免疫"全局阈值在不同拓扑规模下失效"；移植到 RL 可直接当**动作掩码或归一化基线**。⚠ 原文求和下标是邻居还是本节点未消歧（L101 冲突），移植时须自定义清楚。
- **M2 预测驱动的二值准入门控（把"未来值"变成硬约束而非奖励项）**：L107（原文见第 1 项）+ 载体 L90 — "The G-AODV routing protocol necessitates the allocation of new storage space Next\_\traffic_i\ in the HELLO packets of the original AODV."。**一个额外字段 + 一条比较就把时序预测接进控制回路，无需重训任何东西。**
- **M3 邻接集合 Jaccard 稳定性**：公式 (3) L174 `S T A _ { i } = \frac { V _ { i } ( t _ { 1 } ) \cap V _ { i } ( t _ { 2 } ) } { V _ { i } ( t _ { 1 } ) \cup V _ { i } ( t _ { 2 } ) }\——**天然归一化 \[0,1]\、无单位、仅依赖拓扑观测，可直接作为 RL 状态特征**。
- **M4 一跳反向拥塞信令 + 上游缓存背压**：L122（原文见第 3 项），代价仅 3 个地址字段 + 一次反向发送。**RL 里可当局部 reward 通道或 advantage 广播。**
- **M5 断链修复的二段式选择器**：L199（Table 6）— "Step 2: Determine whether hopS \geq\ hopD is satisfied. If satisfied, execute Step 6 to perform local repair; otherwise, execute Step 3 to repair the source node." + "Step 6: Calculate the stability of the nodes upstream and downstream of the fracture according to Formula (3)."——**两个标量 + 一个比值构成 2×2 选择器，可作分层控制器的高层动作，把底层动作压缩到 3 个离散选项。**
- **M6 前向/后向 2 跳路由表缓存（开销显式可算）**：L142 — "The data packets transmitted per second increase the bandwidth by up to 16 ∗ R, where R is the packet transmission rate (packets/s)."

### 12) 实验合同里与"负载"相关的设置（仅登记，非贡献）
- 平台：STK + NS2（L203）；拓扑**无节点数**（仅 \N\）；卫星速度 7.9 km/s、pause time 0 s（L246）。
- **容量参数（Table 7, L206 逐字全表）**：Satellite processing rate 1000 (packet/s)；Satellite inter-satellite link bandwidth 10 (Mb/s)；Uplink bandwidth 9 (Mb/s)；Downlink bandwidth 9 (Mb/s)。附加开销 16R bytes/s（L142）。
- **到达过程：未建模**（`grep -n -oiE 'poisson|pareto|on-off|self-similar|CBR|UDP|TCP|exponential|arrival|burst'` → 命中仅 L67 的 "self-similarity"（描述被引文献）、L73 的 "arrival of congested nodes"（**节点到达，非包到达**）及参考文献中的 TCP。**无任何到达分布/强度设定**）
- **负载扫描两旋钮**：Scenario 1 变包转发速率（标题 L248；**具体速率取值正文未给**，只在图 6/7/8 横轴）；Scenario 2 固定 4500 packets/s 变连接对数 10/20/30/40/50/60（L275，该行含 MinerU 双写乱码）。
- 对比算法（L246）：G-AODV、E-AODV、DS-DSR、NCMDSDV（出处 L244）。
- 指标：包投递率（4）、平均端到端时延（5）、丢包率（6）（见第 1 项公式）。
- 报告数值（登记，**注意口径不一致**）：Scenario 1 — L254 "packet delivery rates 10%, 12%, and 20%"、L268 "packet loss rate ... reduced by 5%, 19%, and 22%"；Scenario 2 — L279 "increased by 15%, 18%, and 20%"、L293 "reduced by 4%, 10%, and 18%"；时延**仅定性**（L261/L286）。摘要口径 L13 "up to 20% / 22%"。

---

# 篇末小结：B4 批（9 篇）共同范式、共同盲区、最可复用机制

## 一、共同范式（逐条有本批行号支撑）

1. **学习信号几乎全是"加性加权标量"**：3MRQRWHU 公式 (19) `r(a)=\alpha\cdot r^{delay}+\beta\cdot r^{loss}+\lambda\cdot r^{band}+k\cdot\gamma\cdot r^{var}\；EG9X569M 公式 (8) `r=w_1*Dis_i+w_2*AoI_{s'}+w_3*\vartheta_{s'}\；X5Z98UPM 公式 (2) 四段式；YI9G7NRY 公式 (7)–(9) 三分支；8N9QJHC2 的寿命项奖励。**9 篇中 0 篇使用向量奖励或多通道惩罚**（唯一的多目标向量奖励出现在本批之外的 UKBSA7WN）。
2. **状态 = 瞬时快照，且不含任何历史编码**：9 篇逐篇检索 `EWMA|exponential moving|moving average|history|historical|previous state|trend` 全部为 0 命中（唯一例外是 8N9QJHC2 把"链路剩余寿命"放进 **折扣因子** \gamma=[(t_c-t_n)/t_k]^3\，以及 UF8IQTA2 外借 GRU 的**一步**预测）。**时间要么不进模型，要么只以一步前瞻的形式从外部模型借入。**
3. **信用分配清一色"逐跳即时 + 折扣传播"**：没有任何一篇做反事实、Shapley 或回报分解。**唯一替代方案是用监督标签替代信用分配**——JLF7IEBQ（Gurobi 逐元素标签，L201）与 WFA3CZLP（MCF/LP 给出 \sigma\ 目标，L116/L118）。
4. **episode 概念普遍缺失**：3MRQRWHU 用"单服务一次寻路 + maxepoch 重启"；8N9QJHC2 连 episode 都没有（检索 0 命中）；UF8IQTA2/JLF7IEBQ/WFA3CZLP 根本不是序贯决策。**9 篇中 0 篇使用资格迹或 n 步回报。**
5. **折扣因子存在三种极端**：无折扣（47J2H748，代价即送达时间）、常数（EG9X569M \gamma\=0.6、X5Z98UPM \gamma\=0.99）、**时变**（8N9QJHC2 \gamma=[(t_c-t_n)/t_k]^3\）。**第三种是本批最有信息量的设计。**
6. **负载几乎都不建模到达过程**：9 篇中只有 JLF7IEBQ 明确用 Poisson 到达（L232），WFA3CZLP 用随机 TM（L128），其余多为"随机源宿 + 定长包 + 循环流"。**只有 YI9G7NRY 给出无量纲负载定义** \ell=\sum_{v_R}\lambda^{(v_R)}/\lambda^*\（L70）。

## 二、共同没考察什么（跨篇盲区，按覆盖率排序）

| 盲区 | 覆盖情况 | 关键证据 |
|---|---|---|
| **动作的时间结构**（驻留/迟滞/切换代价/摊销） | **0/9 考察** | 9 篇逐篇 dwell/hysteresis/handover/switch cost 类检索 0 命中；唯一给出**控制周期实测值**的是 JLF7IEBQ（SaTE 1 s vs 基线 47/25/54 s vs Starlink 全局 15 s，L292/L327）与 WFA3CZLP（慢路径选择 + 快速率自适应，L21/L40） |
| **失败原因分通道惩罚（G-A）** | **0/9 考察** | 见下节对抗性检索；本批最近的是 YI9G7NRY 的"成环"单分支与 8N9QJHC2 的"故障类型驱动哪组 Q 表更新"（但公式 14 对两类故障完全相同） |
| **状态的历史/趋势编码** | **0/9 考察** | 见共同范式第 2 条 |
| **多智能体形式化（参数共享、非平稳、动作同步）** | **0/9** | 声称"分布式/每星一个 agent"的有 YI9G7NRY、X5Z98UPM、WFA3CZLP，但**三篇均未声明参数共享策略**，也无一篇讨论非平稳性 |
| **训练分布 vs 评估分布分离** | **0/9**（唯一做对的是非 RL 的 JLF7IEBQ） | JLF7IEBQ L245 — "the testing dataset consists of completely unseen topologies and trafic matrices from the trained model."（4:1 划分）；其余 8 篇训练与评估共用同一套仿真，且大多无划分声明 |
| **超参可复现性** | **大面积缺失** | 3MRQRWHU 的 \alpha\/\gamma_0\/\varepsilon\ 全缺；EG9X569M 的 \w_1,w_2,w_3\ 缺；YI9G7NRY 的 \w_1,w_2,r_{\mathrm d},r_{\mathrm{loop}},\gamma\ 缺；8N9QJHC2 的 \alpha\/\gamma\ 缺；X5Z98UPM 的网络宽度/激活/target 更新周期 C 缺；UF8IQTA2 全缺；JLF7IEBQ 的 epoch/batch/lr/优化器缺 |

## 三、最可复用的 2–3 条机制（含公式原文）

### 机制 A：邻居回传式一跳 TD 目标（本批 3 篇共用的内核）
- 47J2H748 L28 逐字：`t = \operatorname* { m i n } _ { z \in { \mathrm { n e i g h b o r s ~ o f ~ } } y } Q _ { y } ( d , z )\；L34 逐字：`\Delta Q _ { x } ( d , y ) = \eta ( { \overbrace { q + s + t } ^ { \mathrm { n e w \ e s t i m a t e } } } - { \overbrace { Q _ { x } ( d , y ) } ^ { \mathrm { o l d \ e s t i m a t e } } } )\
- 后代：YI9G7NRY 公式 (10) 的 \mathcal{Q}_j(s'_{t+1},a'_t)\；8N9QJHC2 公式 (15) 的 \Q_{y_z}(d_k,y_m)\。
- **可搬点**：一跳信令即可把"下游的最优剩余时间"带回本节点；47J2H748 同时给出**两个反面证据**——只更新最优邻居导致"系统性高估无法修正"（L77），以及随机探索在路由中"extremely negative effect on congestion"（L79），并明确"basic Q-routing（不探索）在高负载下反而更好"（L88）。**这组结论直接约束我们方案里 \varepsilon\-greedy 的使用方式。**

### 机制 B：寿命感知折扣因子 + 值级硬禁（8N9QJHC2，本批唯一的时变折扣）
- 折扣 L263 逐字：`\gamma = \bigg [ \frac { \big ( t _ { c } - t _ { n } \big ) } { t _ { k } } \bigg ] ^ { 3 } .\；约束 L212 逐字：`\Delta t \le t _ { c } - t _ { n } \le \operatorname* { m a x } t _ { k } ,\
- 奖励 L263 逐字：`r = - \big ( t _ { q } + t _ { t } + t _ { n } - t _ { c } \big ) ,\
- 硬禁 L248 逐字：`Q _ { F } ^ { \mathrm { o d d } } ( d _ { i } , F ^ { \prime } ) = - \infty\ 与 `Q _ { F ^ { \prime } } ^ { \mathrm { o d d } } ( d _ { i } , F ) = - \infty\
- **可搬点**：把 bootstrap 权重设成"距下一次**计划**拓扑变化的时间 / 链路总寿命"的幂，让视界在切换前自动收缩；**用 \-\infty\ 值屏蔽替代动作掩码基础设施**。⚠ 原文未解释三次方，且 \t_t\ 无定义，搬运需自行标定。

### 机制 C：归一化链路相对优劣 + 方差型负载均衡 + 防饿死等待等级（3MRQRWHU）
- 分项归一化 L227 公式 (15) 逐字（min-max 分母有显式闭式定义）：
  `r ^ { \mathrm { d e l a y } } ( a ) = \frac { \operatorname* { m a x } ( \mathrm { d e l a y } ( e _ { q , p } ) ) - \mathrm { d e l a y } ( a ) } { \operatorname* { m a x } ( \mathrm { d e l a y } ( e _ { q , p } ) ) - \operatorname* { m i n } ( \mathrm { d e l a y } ( e _ { m , n } ) ) } }\
- 负载均衡项 L251 公式 (18) + L245 公式 (17) 逐字：`r ^ { \mathrm { v a r } } ( a ) = \frac { \mathrm { V a r } ^ { \mathrm { m a x } } - \mathrm { V a r } ( E ) } { \mathrm { V a r } ^ { \mathrm { m a x } } }\、`\mathrm { V a r } ^ { \operatorname* { m a x } } = \left( \frac { \mathrm { B a n d } ( e _ { i , j } ) } { 2 } \right) ^ { 2 } ,\
- 防饿死等级 L83 公式 (3) 逐字：`\phi \left( u \right) = \phi _ { \mathrm { t i m e } } \left( u \right) + \phi \left( u \right) , \ \phi _ { \mathrm { t i m e } } \left( u \right) \leqslant \phi _ { \mathrm { t i m e } } ^ { \mathrm { m a x } } .\
- **可搬点**：把 reward 塑形建立在一套**有闭式归一化分母**的相对量上（而不是手调系数），并用"每跨一个时间片 +1、封顶"的等待等级做**防饿死**——这两点直接对应我们平台里"多业务优先级 + 负载均衡"的双目标。

（次选可搬项：**YI9G7NRY 的 2-bit 队列占用档** \s_t=00,01,10,11\ 同时编码"拥塞程度 + 链路可用性"（L111）——信令开销最低的状态设计；**JLF7IEBQ 的 trim 后处理 + 剪枝等价性论证模板**（L199/L558）——任何"软约束网络输出必须投影回可行域"的场景通用。）

---

# 对抗性检索：缺口主张 G-A 的反例排查

**G-A 主张**：全库是否有任何工作，把**同一个失败事件**（丢包/超时/溢出）按**物理原因**拆成**不同的学习通道或惩罚项**（例如区分"决策缓存溢出"与"链路队列溢出"）？

## 检索词与实测计数（范围：全库 /data/liguang13/topic-loop-r2/md/ 全部 113 篇 MinerU MD，grep -rniE 输出行数）

| 检索模式 | 全库命中行数 | 命中位置与判读 |
|---|---|---|
| credit assignment | **10** | **全部 10 处在通用 RL 论文里**：6C843JTS（Sutton TD 原文，L13/L488/L500/L536/L588）、9FLZ88LZ（QMIX，L52）、JSX5XG88（GAE，L17/L233）、QGAREQUM（L329/L435）。**在 LEO 路由类论文中 0 命中**——即"信用分配"作为术语从未进入本领域路由工作 |
| counterfactual | **6** | **全部是 COMA 的引用条目**：9FLZ88LZ（L28/L52/L273）、FGQSH4AI（L262）、I2WH9RRR（L390）、KPUZIMU5（L432）。**无任何路由论文使用反事实基线** |
| reward decompos | **0** | 全库零命中 |
| separate (reward|penalty)|separate reward | **0** | 全库零命中 |
| multi-objective|multiobjective|MORL | **41** | 绝大多数是参考文献标题或多目标优化（非 RL）。**唯一实质使用者是 UKBSA7WN**（见下"近邻 1"） |
| reward vector|vector reward|multi-head|multi head | **16** | **唯一与"奖励向量"相关的实质命中是 UKBSA7WN L141/L147/L158**；其余 13 处是 Transformer 的 multi-head attention（35T2JJRJ/A7QNRKML/FLQLU3T4）——**同形词，不构成反例** |
| drop (reason|cause)|dropping (reason|cause)|reason for the (drop|loss) | **2** | 2 处均在 9KZDXPKC（见下"近邻 3"） |
| packet loss cause|loss cause|failure cause|cause of the (loss|drop|failure) | **22** | 逐条查看后归为三类：(a) 8N9QJHC2 的故障类型**检测/分类**（L27/L105/L160–L166/L319/L342）；(b) 9KZDXPKC 的丢包成因澄清（L13/L128/L152）；(c) 7TASFUDR 把"能量耗尽致丢包"作为**目标之一**（L134）。**无一处按原因建独立学习通道** |
| overflow | **11** | 逐条查看：X2FCSU4S（缓存溢出，L15）、TQF59BD7（buffer limitations，L482）、R37BNQQ8（MSB overflow factor \eta(t)\，L209）、GPDPLJNG（flow imbalance，L82）、9C6HB6AF（traffic overflow，L435）等。**均为物理/成本描述，无一是"学习通道"** |

## 找到的三个"近邻"及其分解轴（明确写出，均**不覆盖** G-A）

**近邻 1 — UKBSA7WN（Multi-Objective RL / QRLSN）**：全库最接近"多通道奖励"的工作。
- L141 逐字 — "MORL differs from typical RL, which considers several optimization objectives simultaneously in the learning process, where a reward vector is provided for the agent at each update step"
- L147 逐字 — "where \i \in [ 1 , n ]\ and n represents the number of objectives; \r _ { i }\ is the i th feedback signal of the agent's reward vector obtained from the interaction with the environment."
- 每目标一套 Q：公式 (6) `Q _ { i } ( s , a ) \gets ( 1 - \alpha ) Q _ { i } ( s , a ) + \alpha \biggl [ r _ { i } + \gamma \operatorname* { m a x } _ { a ^ { \prime } \in A } Q _ { i } ( s ^ { \prime } , a ^ { \prime } ) \biggr ]\；合成公式 (7) `\mathrm { T Q } ( s , a ) = \sum _ { i = 1 } ^ { n } w _ { i } Q _ { i } ( s , a )\（L158 — "where w is the weight vector value and the sum of w equals 1."）
- 两个目标逐字：公式 (8) \f_{r_1}\（"the reward function to optimize the end-to-end delay"）、公式 (9) \f_{r_2}\（"network traffic overhead load"）。
- **分解轴 = 优化目标类型（时延 vs 流量开销负载），不是失败原因。不覆盖 G-A。**

**近邻 2 — 39NJWBI7（PRIMAL，约束 RL / primal-dual）**：按**约束类型**设独立乘子。
- L172 逐字 — "\r ( o , a , o ^ { \prime } )\ and \\{ c _ { k } ( o , a , o ^ { \prime } ) \} _ { k = 1 } ^ { K }\ are the reward (primary objective) and QoS cost functions (e.g., load balancing) for a given state transition."
- L224 逐字 — "traditional methods for solving P2 often rely on reward engineering, where a hand-crafted reward function is designed as a weighted sum of the main objective \mathcal { I } _ { r }\ and the cost components \mathcal { I } _ { c _ { k } }\ ."
- 每约束一个拉格朗日乘子，公式 (27) `\mathcal { L } _ { \lambda _ { k } } = \underset { o \sim \mathcal { D } } { \mathbb { E } } \left[ \lambda _ { k } \left( \pi _ { \theta } ^ { \top } ( o ) Q _ { \psi _ { k } } ^ { c } ( o ) - D _ { k } \right) \right] ,\；更新语义 L304 — "The update for \lambda _ { k }\ in (27) increases the multiplier if the estimated cost exceeds the threshold \D _ { k }\ , thereby strengthening the penalty on costly actions in the actor's objective."
- 代价的一个具体定义 L397 — "\c _ { h } = D _ { h } ^ { Q } / D _ { n o r m }\ , where \D _ { h } ^ { Q }\ is the queuing delay experienced when packet \p\ is forwarded over a link at hop \h\"
- **分解轴 = 约束/代价类型（每个 QoS 约束一条通道），不是失败原因；且按"代价超阈"调乘子，不区分丢包的物理来源。不覆盖 G-A。**

**近邻 3 — 9KZDXPKC（CUBIC/BBR in space，T2 非 RL）**：**诊断**了丢包成因，但只用于修正拥塞控制，不是学习通道。
- L128 逐字 — "The packet loss caused by GSL handover and ISL failure will be mistakenly detected as the congestion signal by CUBIC, leading to unnecessary congestion window..."
- L55 逐字 — "We propose a novel DB-R routing mechanism to mitigate the impact of GSL handover and ISL failure."
- **分解轴 = 丢包的物理来源（GSL 切换 vs ISL 失效 vs 真拥塞）——全库唯一明确按物理原因区分丢包的工作，但它是 TCP 层的成因澄清 + 备份路由机制，既不产生学习通道也不产生分项惩罚，且论文本身不是 RL 论文。仍不覆盖 G-A。**

## 结论

**未发现反例。** 全库 113 篇中：
1. **按"目标类型"分解**有（UKBSA7WN 的 reward vector + 每目标一套 Q；另 WFA3CZLP/R37BNQQ8/7TASFUDR 的多项加权代价）但那是目标维，不是失败原因维；
2. **按"约束/代价类型"分解**有（39NJWBI7 的逐约束 \lambda_k\）但那是 QoS 约束维；
3. **按"结局类型"分解**有（YI9G7NRY 公式 (7) 把"进入循环"与"成功投递"分成不同奖励分支）但那是**成功/成环/常规**三分，不含任何物理溢出原因；
4. **按"物理失败原因"分解**——**全库唯一沾边的是 9KZDXPKC（非 RL，只做成因诊断）**；在 RL 路由工作里 **0 篇**。
5. 本批内部最接近的 8N9QJHC2：**故障类型确实驱动力"更新哪一组 Q 表"**（L243 "Update the Q-value table according to the detection result of the first stage"；L253 "…second stage"），但 ⚠ **公式 (14) 对端口永久故障与介质干扰临时故障用的是同一套更新式**，论文未给第二类故障的第二条更新式——**即"分类只用于触发，未用于分通道惩罚"**。

**→ G-A 在本批与全库扫描下均成立（未被反例覆盖）。** 建议表述为：现有 LEO-RL 路由工作把失败建模为单一标量代价（丢包率/队列长度/时延），最多按"目标类型"或"约束类型"分通道；尚未有工作把同一失败事件按物理原因（决策缓存溢出 / 链路队列溢出 / 链路失效 / 切换中断）拆成独立的学习通道或分项惩罚。这一空白的**可行入口证据**是 8N9QJHC2 的"检测分类 → 驱动更新"结构（L243/L253）与 9KZDXPKC 的成因三分（L128/L152）。

---

# 读取与核验记录（本批）

- 行号基准：VM \/data/liguang13/topic-loop-r2/md/<key>/<key>/txt/<key>.md\，与本地副本 \/tmp/b4md/<key>.md\ 经 scp 同步（字节一致）。
- **由本报告撰写者逐行通读的 5 篇**：3MRQRWHU（L1–L362 正文）、EG9X569M（L1–L221）、YI9G7NR7（L1–L167）、47J2H748（L1–L99）、WFA3CZLP（L1–L158）。
- **由深读代理通读、其引文与计数已随报告一并提交的 4 篇**（均附 md5 两侧一致、逐行读取范围、以及每条负向声明的 grep 模式与计数）：X5Z98UPM（md5 3f9d6706e874e1fdb93812ff3ffc709b，L1–L341）、8N9QJHC2（L1–L375）、JLF7IEBQ（L1–L338 + 附录 L509–L714）、UF8IQTA2（md5 59ee892396b4239e9f8ea27056ab9e8c，L1–L313）。
- 全部 9 篇的**参考文献表均未逐条精读**，各篇条目内已注明区间。
- 所有"未见"判定均给出了**精确检索模式 + 实测计数**，并按主控 2026-09-11 的核验协议，对**每一个命中**说明了"为何不构成反例"（本批共处理此类命中 10 余处，最典型的是 X5Z98UPM 的 attention/trend 各 1 处、8N9QJHC2 的 replay|target net|double|dqn|deep 3 处、UF8IQTA2 的 train 3 处与 reward 2 处、WFA3CZLP 的 reinforcement|q-learning|reward 4 处）。
- 公式一律逐字抄 LaTeX 原文，MinerU 的上标错位/缺字/乱码（如 X5Z98UPM 的 \y\（17）、8N9QJHC2 的 \$e\、JLF7IEBQ 的 Fig.7 "dding"、EG9X569M 的 \mathcal{V}\）**保持原样**，并以"⚠ 原文如此"标注。
- 本报告**只写这一个文件**；未修改任何其他路径。