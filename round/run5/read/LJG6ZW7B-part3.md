# LJG6ZW7B 分片 part3（覆盖行号区间 L2401–L3600）

> 对象：Sutton & Barto《Reinforcement Learning: An Introduction》第二版（全文 9596 行）。
> 本片覆盖 L2401–L3600，**已逐字读完，无跳读、无缺口**（中途一次输出截断已定位并补读 L3272–3315）。
> 本片实际内容 = 第 6 章尾 + 第 7 章全章 + 第 8 章全章 + 第 9 章前半。
>
> **提取质量提示（供合并者注意）**：该 md 由 PDF 转换而来，存在系统性字符丢失：`di↵erence`=difference、`o↵-policy`=off-policy、`e cient`=efficient、`su cient`=sufficient（连字 "ff"/"fi" 丢失，显示为 ↵ 或空格）；ε 多处显示为 `"`。下文逐字引用保留原样。

---

## 1. 一句话

本片是一本 RL 教材的连续四章：把已有一阶 TD 方法推广成 **n-step 自助法（Ch7）**、把有模型规划与无模型学习统一成 **Dyna 架构与规划维度体系（Ch8）**，再把整套方法从表格搬到 **参数化函数逼近（Ch9 上半）**——它本身不做新实验，而是给出这一族方法的方程、伪代码、收敛性结论与一份"方法空间维度表"。

## 2. 问题设定

- 承接"没有模型也能学"的一阶 TD（Sarsa/Q-learning），本片要解决三件事：
  1. **一阶 TD 与 Monte Carlo 之间的空档**：一步 TD 把"多久改一次动作"和"多久做一次自助"绑死在同一个时间步上，必须折中（L2533–L2535，"free you from the tyranny of the time step"）。
  2. **有模型 vs 无模型的割裂**：DP/启发式搜索要模型，MC/TD 不要模型；本书要说明二者其实是同一件事的两个来源（L2953–L2955）。
  3. **表格法的状态空间爆炸**：目标任务的"状态空间是组合爆炸的"，例如"the number of possible camera images … is much larger than the number of atoms in the universe"，只能要近似解（L3378–L3382）。
- 谁在什么条件下遇到麻烦：在**超大状态空间**、**环境会变**、**目标策略与行为策略不同（off-policy）**、**计算/响应时间受限**这四种条件下，前几章的算法会失效或退化（L3047–L3053、L3079、L3169、L3243）。

## 3. 方法骨架

状态/动作/奖励/更新四要素在本片的主干（按行号顺序）：

**(a) Ch6 尾部三种控制算法（L2401–L2479）**
- Q-learning（表格尾部 L2401–L2405，备份图说明 L2407）：off-policy，target 取 max_a Q(S',a)。
- **Expected Sarsa（L2427–L2443）**：把 max 换成对下一状态动作的期望，更新式 (6.9) L2430：Q(S_t,A_t) ← Q(S_t,A_t) + α[R_{t+1} + γ Σ_a π(a|S_{t+1})Q(S_{t+1},a) − Q(S_t,A_t)]；"Given the next state, this algorithm moves deterministically in the same direction as Sarsa moves in expectation"（L2433）。
- **Double Q-learning（L2454–L2479）**：把样本一分为二、用 Q1 选 argmax、用 Q2 估值，更新式 (6.10) L2459："double learning doubles the memory requirements, but does not increase the amount of computation per step"（L2454）。

**(b) Ch7 n-step 自助法（L2531–L2950）——本片最核心的一章**
- n-step return (7.1) L2573：G_{t:t+n} ≐ R_{t+1} + γR_{t+2} + ⋯ + γ^{n−1}R_{t+n} + γ^n V_{t+n−1}(S_{t+n})；n-step TD 更新 (7.2) L2581。
- **误差缩减性质 (7.3) L2615**：max_s |E_π[G_{t:t+n}|S_t=s] − v_π(s)| ≤ γ^n max_s |V_{t+n−1}(s) − v_π(s)|——这是"n-step 也是一族可靠方法"的理论依据（L2618）。
- n-step Sarsa (7.4)(7.5) L2638/L2644；n-step Expected Sarsa (7.7)(7.8) L2689/L2695，其中期望近似值 V̄_t(s) ≐ Σ_a π(a|s)Q_t(s,a)。
- **off-policy：重要性采样比值 (7.10) L2711**，off-policy n-step TD (7.9) L2705、off-policy n-step Sarsa (7.11) L2717——注意 Sarsa 的比值"starts and ends one step later"，因为第一个动作已被执行、不需纠正（L2720）。
- **per-decision + control variate (7.13) L2762**：G_{t:h} ≐ ρ_t(R_{t+1} + γG_{t+1:h}) + (1−ρ_t)V_{h−1}(S_t)；动作值版本 (7.14) L2776。
- **树回溯 (tree backup) (7.16) L2820**：完全不用重要性采样，用 π 的概率给叶节点加权。
- **n-step Q(σ)（编号在 md 中损坏为 (7.16')）L2887**：σ_t ∈ [0,1] 在"采样"与"期望"之间连续滑动，σ=1 得 Sarsa，σ=0 得树回溯，只最后一步期望得 Expected Sarsa（L2869–L2876）——"Q(σ) algorithm is new to this text"（L2949）。

**(c) Ch8 规划与学习的统一（L2951–L3372）**
- 模型二分为 **分布模型 / 样本模型**（骰子例子，L2959）；规划定义 model →(planning) policy（L2963–L2971）。
- **Dyna-Q（L2993–L3026）**：同一时间步内四个进程——acting (b)(c)、direct RL (d) L3020、model-learning (e) L3021、planning (f) 重复 n 次 L3022–L3026；"If (e) and (f) were omitted, the remaining algorithm would be one-step tabular Q-learning"（L3012）。
- **Dyna-Q+（L3067）**：给久未尝试的转移加探索奖励 r + κ√τ（τ = 距上次真实尝试的步数）。
- **优先扫描 prioritized sweeping（L3083–L3101）**：优先级 P ← |R + γ max_a Q(S',a) − Q(S,A)|（L3092），超过阈值 θ 入队，反向传播到前驱（L3093–L3101）。
- **期望更新 vs 样本更新（8.1 L3143 / 8.2 L3149）**：期望更新代价约为样本更新的 b 倍（b = 分支因子，L3154）；样本更新误差按 √((b−1)/(bt)) 下降（L3158）。
- **轨迹采样（L3169–L3190）**：按 on-policy 分布采样轨迹做更新。
- **RTDP（L3196–L3233）**：on-policy 轨迹采样版的值迭代，用 (4.10) 的期望更新，更新顺序由轨迹访问顺序决定。
- **决策时刻规划（L3237–L3243）**：background planning vs decision-time planning 的二分。
- **启发式搜索（L3247–L3258）**、**rollout（L3262–L3274）**、**MCTS（L3278–L3303）**：MCTS 四步 = Selection / Expansion / Simulation / Backup（L3289–L3295），树内用 tree policy、树外用 rollout policy（L3282）。
- **Part I 维度表（L3319–L3352）**：三个主轴 = 样本/期望（宽）× 更新深度（自助程度，Fig 8.11 L3326）× on/off-policy；外加 8 个次级维度（回报定义、值类型、探索方式、同步/异步、真实/模拟、更新位置、更新时机、更新记忆留存）。

**(d) Ch9 函数逼近（L3386–L3600）**
- 逼近对象 v̂(s,w) ≈ v_π(s)，d ≪ |S|（L3390）；把每次更新 s ↦ u 当作一条监督学习样本（L3396–L3398）。
- **目标函数 VE (9.1) L3407**：V̄E(w) ≐ Σ_s μ(s)[v_π(s) − v̂(s,w)]²；μ 取 on-policy 分布（L3410），episodic 情形由 (9.2)(9.3) L3417/L3423 给出。
- **SGD (9.5) L3449 / 通用形式 (9.7) L3465**：w_{t+1} ≐ w_t + α[U_t − v̂(S_t,w_t)]∇v̂(S_t,w_t)。
- **半梯度 (semi-gradient)**：自助目标依赖 w_t ⟹ 有偏 ⟹ 只含部分梯度，L3482 "Bootstrapping methods are not in fact instances of true gradient descent (Barnard, 1993)"。
- **线性方法 (9.8) L3518**：v̂(s,w) ≐ wᵀx(s)，梯度就是 x(s)（L3528）；收敛到 **TD 不动点 (9.12) L3562**：w_TD ≐ A⁻¹b，其中 b ≐ E[R_{t+1}x_t]、A ≐ E[x_t(x_t − γx_{t+1})ᵀ]（(9.11) L3556）。

## 4. 它声称的效果（数字 + 条件 + 基线）

| 声称 | 数字 | 条件 | 基线 | 行号 |
|---|---|---|---|---|
| Q-learning 学到最优策略但**在线性能更差** | 无量化数字，靠学习曲线 | Cliff Walking，ε=0.1，undiscounted episodic | Sarsa（学到更长的安全绕路） | L2409–L2419 |
| Q-learning 受最大化偏差影响 | 渐近仍比最优多走 left 约 **5%** | 2 状态 MDP，ε=0.1, α=0.1, γ=1，10,000 runs | Double Q-learning（基本不受影响） | L2449–L2452 |
| Expected Sarsa 优于 Sarsa | 在**很宽的 α 范围**上显著更好；确定性转移下可安全取 **α=1** | Cliff Walking | Sarsa（只能在小 α 下长期表现好） | L2435–L2438 |
| n-step 优于两端 | 中等 n 最好（无逐点数字） | 19 状态 random walk | n=1（TD）与 n=∞（MC） | L2624–L2627 |
| Dyna 规划加速 | n=0 约 **25** episodes 到近最优；n=5 约 **5**；n=50 约 **3** | 47 状态迷宫，γ=0.95, α=0.1, ε=0.1 | 非规划 agent（n=0，纯 one-step Q-learning） | L3029 |
| 优先扫描加速 | **5–10 倍** | 同结构迷宫，分辨率变化，每步 ≤5 次更新 | 无优先级 Dyna-Q | L3104 |
| RTDP 比 DP 省一半更新 | DP **252,784** 次更新 / 28 sweeps；RTDP **127,600** 次 / 4000 episodes（31.9 次/episode） | racetrack，9,115 可达状态 / 599 相关状态，25 runs，Gauss-Seidel | 常规值迭代（穷举扫描） | L3223–L3231 |
| RTDP 更新高度集中 | **98.45%** 状态更新 ≤100 次，**80.51%** ≤10 次，**3.18%** 更新 0 次（约 290 个状态） | 同上 | — | L3225–L3227 |
| 样本更新误差衰减 | √((b−1)/(bt)) | b 个后继等概率，初始误差 1，样本平均（α=1/t） | 期望更新（代价 ≈ b 倍） | L3158 |
| 线性 TD(0) 的 VE 有界 | V̄E(w_TD) ≤ (1/(1−γ)) min_w V̄E(w) (9.14) | 持续型任务，线性逼近，on-policy | 全局最优 VE | L3597–L3600 |
| MCTS 的战绩 | 围棋从 2005 年弱业余 → 2015 年**大师级（6 dan 以上）**；AlphaGo 2016 | 博弈 | 此前方法 | L3278 |

## 5. 它的实验条件（拓扑/规模/负载；训练与评估是否同一套）

本片是教材，没有"拓扑/负载"，但有相当明确的算例规模与参数。逐条列出：

- **Cliff Walking（L2409–L2419）**：标准 undiscounted episodic gridworld，四动作，除进入悬崖外奖励 −1，进悬崖 −100 并立刻回起点；ε=0.1。
- **最大化偏差 MDP（L2449）**：两个非终态 A、B；A 选 left→B（奖励 0），B 上所有动作立即终止、奖励 ~ N(0.1, 1.0)；A 选 right→立即终止奖励 0。参数 ε=0.1, α=0.1, γ=1；平均 10,000 runs；初始值全 0；ε-greedy 平局随机破。
- **n-step random walk（L2620–L2627）**：先在 5 状态版说明，正式实验用 **19 状态**版（左端结果 1，所有值初始化为 0）；指标 = 19 个状态预测值与真值的均方根误差，对**前 10 个 episode** 与 **100 次重复**取平均。
- **Dyna 迷宫（L3027–L3039）**：**47 个状态** ×4 动作，撞墙/边界原地不动，进目标 +1，回到起点开始新 episode；γ=0.95，α=0.1，ε=0.1，贪心平局随机破；每 n 条曲线取 **30 次重复**平均。
- **Blocking maze（L3051）**：前 **1000 步**用短路径环境，之后封死并打开左侧长路径。
- **Shortcut maze（L3058）**：前 **3000 步**用左侧绕行最优，之后右侧打开更短路径（原长路径仍通）。
- **优先扫描迷宫（L3104）**：与 Fig 8.2 同结构、仅改变网格分辨率；两系统每步最多 **n=5** 次更新。
- **Rod maneuvering（L3116–L3119）**：4 个动作；**14,400 个潜在状态**（部分被障碍不可达）；平移步长约工作空间的 1/20 并量化到 20×20 位置，旋转增量 10°。
- **期望 vs 样本更新分析（L3158）**：b 个后继状态等概率、下一状态估值假定正确、初始误差为 1。**注意这是解析模型，不是仿真实验**。
- **轨迹采样对比实验（L3177–L3181）**：随机生成 undiscounted episodic 任务；每状态 **2 个动作**，各通向 b 个等概率后继（每个 state-action pair 的 b 个后继独立随机选）；所有转移有 **0.1 概率**进入终止态；期望奖励 ~ N(0,1)。主结果 **200 个任务 × 1000 状态**，b=1,3,10；另有 **10,000 状态**、b=1 的一组。评估量是"当前 Q 下贪心策略在起点状态的**真值** v_π̃(s0)"（L3179）——即用穷举计算做评估，与训练用的采样更新不是同一套。
- **RTDP racetrack（L3217–L3231）**：小车绕弯到终点，起点为起跑线零速状态，无速度上限（状态集潜在无穷，实际取从起点可达的 **9,115** 个状态，其中 **599** 个"相关"）；每步奖励 −1，撞墙送回随机起点。**25 次不同随机种子**。DP = 穷举扫描 + 原地更新（Gauss-Seidel，实测约比 Jacobi 快 **2 倍**）；DP 收敛判据为一次扫描内最大状态值变化 < 10⁻⁴，RTDP 判据为 20 个 episode 的平均过线时间趋于稳定。**两者都以"过线步数 14–15 步"作为最终策略质量的对照**（L3227）。
- **1000 状态 random walk（L3502–L3509）**：状态 1–1000，episode 从 500 附近出发；每步向左右各 100 个邻居等概率转移，边界缺失的概率质量转为终止概率；左端奖励 −1、右端 +1，其余 0。梯度 Monte Carlo + 状态聚合，**100,000 episodes**，α = 2×10⁻⁵，1000 个状态聚成 **10 组 × 100**。
- **训练/评估是否同一套**：教材层面两处明确"同一套"——random walk 的 n-step 实验 "the same sets of walks were used for all parameter settings"（L2624），Dyna 迷宫每个重复里 "the initial seed … was held constant across algorithms"（L3029）。反之，RTDP 的"最优策略何时出现"是用**额外跑的测试 episode** 事后估出来的（L3231），与训练不同套。

## 6. 它自己承认的局限（逐字引用）

> 说明：以下均逐字摘自本片，保留 md 的连字丢失原貌（`di↵erent`/`e cient`）。

1. **n-step 的代价（L2931）**："All n-step methods involve a delay of n time steps before updating, as only then are all the required future events known. A further drawback is that they involve more computation per time step than previous methods. Compared to one-step methods, n-step methods also require more memory to record the states, actions, rewards, and sometimes other variables over the last n time steps."
2. **重要性采样 off-policy 慢（L2791）**："The importance sampling that we have used in this section, the previous section, and in Chapter 5, enables sound o↵-policy learning, but also results in high variance updates, forcing the use of a small step-size parameter and thereby causing learning to be slow. It is probably inevitable that o↵-policy training is slower than on-policy training—after all, the data is less relevant to what is being learned."
3. **两种 off-policy 路线各自的死穴（L2937）**："If the target and behavior policies are very di↵erent it probably needs some new algorithmic ideas before it can be e cient and practical. The other, based on tree-backup updates, … It involves no importance sampling but, again if the target and behavior policies are substantially di↵erent, the bootstrapping may span only a few steps even if n is large."
4. **优先扫描的期望更新浪费（L3112–L3121）**："One of prioritized sweeping’s limitations is that it uses expected updates, which in stochastic environments may waste lots of computation on low-probability transitions." 以及 "Prioritized sweeping is just one way of distributing computations to improve planning e ciency, and probably not the best way."（L3112）
5. **轨迹采样结论不确定（L3190）**："These results are not conclusive because they are only for problems generated in a particular, random way, but they do suggest that sampling according to the on-policy distribution can be a great advantage for large problems…"
6. **VE 未必是对的目标（L3430）**："It is not completely clear that the VE is the right performance objective for reinforcement learning. Remember that our ultimate purpose—the reason we are learning a value function—is to find a better policy. The best value function for this purpose is not necessarily the best for minimizing VE. Nevertheless, it is not yet clear what a more useful alternative goal for value prediction might be."
7. **函数逼近可能发散（L3432）**："Still, for many cases of interest in reinforcement learning there is no guarantee of convergence to an optimum, or even to within a bounded distance of an optimum. Some methods may in fact diverge, with their VE approaching infinity in the limit."
8. **半梯度不是真梯度（L3482）**："Bootstrapping methods are not in fact instances of true gradient descent (Barnard, 1993). They take into account the e↵ect of changing the weight vector w_t on the estimate, but ignore its e↵ect on the target."
9. **TD 之外的 TD 应用未被探索（L2507）**："Even so, these other potential applications of TD learning methods have not yet been extensively explored."
10. **Rod 问题规模（L3119）**："This problem is probably too large to be solved with unprioritized methods."

## 7. 它没做但看起来能做的地方

（基于本片内容，不用套话）

1. **n-step 的 n 与 α 的联合选择没有任何自动方法**。L2624 只给了"中等 n 最好"的经验曲线，作者在 L2931 承认 n-step 有 n 步延迟的开销，但全书到本片结束都没有"如何在线选 n"的机制——这正是后来 eligibility trace / λ 要补的洞（作者自己在 L2537、L2931 明说 Ch12 才讲）。**自然的下一步：把 n 当作可自适应调节的量。**
2. **Dyna-Q+ 的探索奖励 κ√τ（L3067）只有一个自由度，且没有任何调参结果**。L3073（Exercise 8.4）甚至把"奖励加在更新里 vs 只加在动作选择里"当成留给读者的开放题——本片没有实验回答它。
3. **"模型错了"只处理了确定性表格模型**。L3075（Exercise 8.5）明确把"如何改造表格 Dyna-Q 以处理随机环境、以及这种改造为何在变化环境下表现差"留成开放题；L3110 给了随机版优先扫描的改造方向（存计数、用期望更新），但没有实验。
4. **决策时刻规划与背景规划的比例没有指导原则**。L3243 只说"低延迟优先就后台规划、可容忍延迟就决策时刻规划"，没给出在给定计算预算下如何配比——而 L3311 承认 "the division can be handled almost arbitrarily"。
5. **函数逼近部分只做到线性 TD 的不动点与有界性**（9.12–9.14），本片结束在 (9.14) 就截断了（L3600），非线性/神经网络只在 L3390 一句带过。**自然下一步：把 L3567–L3595 那套正定矩阵证明推广到非线性，或反过来找反例。**
6. **off-policy + 函数逼近的组合在本片完全没碰**。L3384 明确把它推到 Chapter 11（"The challenging problem of o↵-policy learning with function approximation is treated in Chapter 11"）——这是本片自己划出的最大空白。

## 8. 和同批其他篇的关系

**必须先声明证据边界**：我**没有**读同批其他 110 篇的正文，只读了同批读卡汇总文件的**标题行**来确认批次构成（该汇总文件名本身没有读取授权，故此处不写字面名）。因此下面区分"可核验"与"推断"。

- **方向（可核验）**：本片是一本**教科书**，不是研究论文。教材（2nd ed，2018）不可能引用本批 2020 年后的 LEO/DRL 论文；关系只能是**单向的：本批论文引用它，而不是它引用本批**。所以第 8 项"是否引用同批其他篇"的答案是：**否，零引用**。
- **推断的谱系连接（基于批次标题，未读正文）**：
  - 键 57EB6US5（Human-level control through deep reinforcement learning / DQN）：DQN 的基座正是本片 L2401–L2407 的 **Q-learning**；DQN 的两大改进之一 **Double DQN** 直接对应本片 L2445–L2479 的 **maximization bias / Double Q-learning**（后者是**本片内**的内容，不是别处）。
  - 键 XLRW7XXN（DQN-based Routing for Load Balancing in LEO）、8N9QJHC2（Recovery Routing Based on Q-Learning）、53HEEK33（Fast-Convergence RL for Routing）：标题层面均指向 Q-learning 族，即本片 L2401–L2407。
  - 键 JSX5XG88（High-Dimensional Continuous Control Using Generalized Advantage Estimation / GAE）：GAE 是 **n-step return / λ-return** 在优势函数上的推广，概念祖先就在本片 L2550–L2618（n-step return 与误差缩减性质）。
  - 键 QGAREQUM（Boosting RL with Strongly Delayed Feedback）：延迟反馈正是本片 L2931 自述的 n-step 固有代价 "a delay of n time steps before updating" 的极端情形。
  - 键 FGQSH4AI（MADDPG）：actor–critic 路线，本片 L2503 明确把它推给 Chapter 13，故本片**不含**其祖先内容。
- **不像谁**：本批多数篇是"把某 RL 算法用到 LEO 路由/负载均衡上"的应用论文，有拓扑、有仿真、有端到端指标；本片**完全没有网络场景、没有任何到达率或时延指标**，是纯方法论。

## 9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实

**直接贡献：没有。** 本片 1200 行内不含任何网络/排队系统的到达率、时延、丢包实验；L2491–L2493 只在讲 afterstate 时**顺带提到**排队任务（"in queuing tasks there are actions such as assigning customers to servers, rejecting customers, or discarding information"），但只是举例子说明"动作由即时效果定义"，没有任何实验，也没有出现 load/arrival 的量化。

**间接但确实可用的事实有四条**（都带行号）：

1. **"学到最优策略" ≠ "在线表现最好"**（L2409–L2419）。Cliff Walking 里 Q-learning 学到最优（贴悬崖走）策略，但因为 ε-greedy 会偶尔掉下去，**在线累积回报反而比学到次优绕路策略的 Sarsa 差**。对"负载变化下的在线时延"这件事，这是本片最直接可迁移的一条：**评估指标若是在线性能，就不能只看收敛到的策略是否最优。** 教材原文甚至补了一句 "if ε were gradually reduced, then both methods would asymptotically converge to the optimal policy"（L2419）——即这个差距是探索策略的产物，不是算法优劣。
2. **环境变化需要显式的"过期激励"**（L3045–L3075）。当环境从"更差"变"更好"时，Dyna-Q **永远发现不了**（Shortcut maze，L3058：常规 Dyna-Q "never switched to the shortcut … the more it planned, the less likely it was to step to the right and discover it"）。解法是给久未验证的状态–动作对加 r + κ√τ（L3067），τ 是**距上次真实尝试的步数**。对 LEO 场景（拓扑/负载随时间变化），这是一个可直接搬的机制：**用"距上次实测的时长"作为重探激励**。
3. **计算延迟 vs 决策质量的权衡被显式写成设计原则**（L3243）："if low latency action selection is the priority, then one is generally better o↵ doing planning in the background to compute a policy that can then be rapidly applied to each newly encountered state." 注意这里的 "latency" 指的是**算法自身响应延迟**，不是网络时延——但对"星上算力受限、必须快速出决策"的场景，这条原则是可用的。
4. **收敛所需的计算量级有具体数字**（L3223–L3231）：同一 racetrack 任务，穷举 DP 需 252,784 次更新收敛，RTDP 只需 127,600 次且 **98.45% 的状态更新不超过 100 次、3.18% 的状态一次都没更新**。对"状态空间巨大、只能更新一小部分"的星上路由问题，这组数字给出了"on-policy 轨迹采样能把更新集中到什么程度"的量化参照。

## 10. 一句话评价

**这是一本教材的方法论骨架章节：把我们这批论文当成黑箱在用的那些 RL 算法（Q-learning / Sarsa / Expected Sarsa / Double Q-learning / n-step 返回 / GAE 的思想祖先 / Dyna / 优先扫描 / MCTS / 半梯度 TD）的原始定义、方程、伪代码和收敛条件，一次给全；它自己不做网络实验，因而对"负载变化下的到达率/时延"零直接贡献——它的价值是让本批论文里"用了 DQN / 用了 n-step / 用了 on-policy 采样"这类表述可以被追溯到确切的行号级定义。**

---

## 本片要点（供主控合并）

1. **本片 = Ch6 尾 + Ch7 全 + Ch8 全 + Ch9 前半**（L2401–L3600），无缺口。关键锚点：Expected Sarsa L2427、Double Q-learning L2454、n-step return (7.1) L2573、误差缩减性质 (7.3) L2615、off-policy 重要性采样 (7.10) L2711、树回溯 (7.16) L2820、Q(σ) L2887、Dyna-Q L3012–L3026、Dyna-Q+ L3067、优先扫描 L3092、RTDP L3196、MCTS 四步 L3289–L3295、VE (9.1) L3407、semi-gradient L3482、线性 TD 不动点 (9.12) L3562。
2. **本片是量化数据最集中的一段，可直接被主控引用**：Dyna 规划把迷宫求解从 ~25 episodes 压到 3–5（L3029）；优先扫描快 5–10 倍（L3104）；RTDP 比穷举 DP 少一半更新（127,600 vs 252,784），98.45% 状态更新 ≤100 次、3.18% 一次未更新（L3225–L3231）；样本更新误差按 √((b−1)/(bt)) 衰减（L3158）；线性 TD 的 VE 有界 ≤ (1/(1−γ))·min_w V̄E(w) (9.14) L3600。
3. **对本批主题（负载变化下的时延/到达率）唯一强相关的两条**：① Cliff Walking 证明**"收敛到最优策略"与"在线表现最优"可以相反**（L2409–L2419，Q-learning 在线更差）；② Shortcut maze 证明**环境变好时常规 Dyna-Q 永远发现不了**，必须加 r + κ√τ 这类按"距上次实测时长"计的重探激励（L3058–L3067）。这两条是本片能迁移到 LEO 动态场景的最实质内容。
4. **本片对同批论文是"被引用的源头"而非"引用者"**：批次内 DQN（键 57EB6US5）、各类 Q-learning 路由、GAE（键 JSX5XG88）、延迟反馈（键 QGAREQUM）的算法祖先均可回溯到本片行号；教材零引用本批论文。（此判断仅依据批次**标题行**，未读那些篇正文。）
5. **提取质量警告（务必转达后续处理者）**：该 md 由 PDF 转换，系统性丢连字——`di↵erence`=difference、`o↵-policy`=off-policy、`e cient`=efficient、`su cient`=sufficient；ε 大量渲染为 `"`（如 L2413 的 `"-greedy`）；大量公式被 OCR 破坏（例：L2887 的 (7.16) 编号被截断为 `(7)`，L2433 出现两段文本互相穿插的乱序）。**凡引用本片公式必对照原始 PDF。**
