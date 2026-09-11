# LJG6ZW7B 分片 P2（覆盖行号 L1201–L2400）

> 篇目：Sutton & Barto《Reinforcement Learning: An Introduction》(2nd ed.) 教材全文 markdown。
> 本片覆盖：第 3 章末（MDP / Bellman 最优方程 / 最优性与近似）、第 4 章全（动态规划）、第 5 章全（蒙特卡洛）、第 6 章前半（TD 学习至 Q-learning 伪码开头）。
> 覆盖声明：**L1201–L2400 逐行读完，无跳读、无关键词检索**。首次拉取时工具有三处输出截断，已回头补读补齐：L1558–1600、L1839–1845、L2000。全片内容均在本卡中有行号落点。

---

## 1. 一句话：这篇（本片）做了什么

本片覆盖的是 RL 教科书的"基础理论三连"：先用 Bellman 最优方程把 MDP 的最优性刻画清楚（L1210–L1300），再用动态规划给出"有模型时的精确解"模板 (4.1)–(4.10)（L1432–L1629），然后剥掉模型假设换成蒙特卡洛的采样平均（第 5 章，L1651–L2162），最后剥掉"必须等回合结束"这条限制、换成 TD 的自举更新（第 6 章前段，L2166–L2400）。

## 2. 问题设定

- **要解决什么**：智能体在与环境交互中学会"最大化长期回报"的行为。本片三类方法的差别**只在于它们如何解决预测问题**（policy evaluation）：DP 用模型做期望更新、MC 用完整回合回报、TD 用下一步估计自举（L2170 原文："The di↵erences in the methods are primarily di↵erences in their approaches to the prediction problem."）。
- **谁在什么条件下遇到什么麻烦**：
  - 有模型但状态多：backgammon 约 $10^{20}$ 状态，即使每秒更新一百万状态，跑完一遍 sweep 也要一千多年（L1581）。第 3 章指出精确解依赖三个现实中很少成立的假设：(1) 动力学精确已知；(2) 算力足够完成计算；(3) 状态具备 Markov 性质（L1289）。
  - 没模型但能采样：MC 只要求"能生成样本转移"，不要求显式转移概率分布（L1651）。
  - 回合很长或没有回合：MC 必须等回合结束才知道 return，TD 只需等一步（L2180、L2265）。

## 3. 方法骨架（状态/动作/奖励/更新）

本片是教科书，主干是一串**更新式**，按依赖顺序排如下（全部逐字核对）：

**(a) Chapter 3 的最优性刻画**
- Bellman 最优方程（状态值）：$v_*(s)=\max_a \sum_{s',r} p(s',r|s,a)[r+\gamma v_*(s')]$ — (3.19)，L1233。
- Bellman 最优方程（动作值）：$q_*(s,a)=\sum_{s',r} p(s',r|s,a)[r+\gamma \max_{a'} q_*(s',a')]$ — (3.20)，L1237。
- 有限 MDP 下 (3.19) 有唯一解；n 个状态 = n 个方程 n 个未知数（L1250）。
- $v_*$ 存在时，一步前瞻的贪心策略即最优策略；有 $q_*$ 则连一步前瞻都不需要——$q_*$ 把"所有一步前瞻的结果缓存起来"，且**不需要知道环境动力学**（L1260）。
- 问题定制：gridworld（Ex 3.8, L1274）、recycling robot 的最优方程显式展开（Ex 3.9, L1276–L1286）。

**(b) Chapter 4 动态规划**（假设完美模型、有限 MDP）
- 政策评估（预测）：$v_{k+1}(s)=\sum_a \pi(a|s)\sum_{s',r} p(s',r|s,a)[r+\gamma v_k(s')]$ — (4.5)，L1360。迭代式政策评估，终止判据 $\max_s|v_{k+1}(s)-v_k(s)|<\theta$（伪码 L1401–L1410）。
- 政策改进：$q_\pi(s,a)=\sum_{s',r}p(s',r|s,a)[r+\gamma v_\pi(s')]$ — (4.6)，L1432；政策改进定理 (4.7)(4.8) L1440/L1446；贪心策略 $\pi'(s)=\arg\max_a q_\pi(s,a)$ — (4.9)，L1466。
- 政策迭代 = 评估/改进交替，有限 MDP 下**有限步收敛**（L1491）；伪码 L1495–L1512。
- 值迭代：把 Bellman 最优方程直接改成赋值语句，$v_{k+1}(s)=\max_a\sum_{s',r}p(s',r|s,a)[r+\gamma v_k(s')]$ — (4.10)，L1536；伪码 L1545–L1558。
- 异步 DP：任意顺序、就地更新，只要每个状态仍被无限次更新即收敛（L1583、L1585）。
- GPI（广义政策迭代）：评估与改进两个过程以任意粒度交错，稳定即最优（L1591–L1600）。

**(c) Chapter 5 蒙特卡洛**（无模型，仅回合式任务）
- 首次访问 / 每次访问 MC 预测，伪码 L1665–L1679；误差标准差按 $1/\sqrt{n}$ 下降（L1681）。
- MC ES（exploring starts）控制，伪码 L1774–L1788。
- 同策略 $\varepsilon$-soft 控制，伪码 L1807–L1823；改进定理证明 (5.2) L1828。
- 异策略重要性采样比 $\rho_{t:T-1}=\prod_{k=t}^{T-1}\frac{\pi(A_k|S_k)}{b(A_k|S_k)}$ — (5.3)，L1874（轨迹概率中的转移概率上下约掉，**只依赖两个策略**，L1877）。
- 普通重要性采样 (5.5) L1888；加权重要性采样 (5.6) L1896。
- 增量实现：$V_{n+1}=V_n+\frac{W_n}{C_n}[G_n-V_n]$ — (5.8) L1966，$C_{n+1}=C_n+W_{n+1}$ L1972；伪码 L1981–L1997。
- 异策略 MC 控制伪码 L2007–L2025（注意 $W\leftarrow W\frac{1}{b(A_t|S_t)}$，因目标策略是贪心的故 $\pi=1$，Ex 5.11 L2029）。
- 折扣感知 IS (5.9)(5.10) L2057/L2063；逐决策 IS (5.11)–(5.15) L2073–L2117。

**(d) Chapter 6 TD 学习**（无模型 + 自举）
- 常数 $\alpha$ MC：$V(S_t)\leftarrow V(S_t)+\alpha[G_t-V(S_t)]$ — (6.1)，L2177。
- TD(0)：$V(S_t)\leftarrow V(S_t)+\alpha[R_{t+1}+\gamma V(S_{t+1})-V(S_t)]$ — (6.2)，L2183；伪码 L2188–L2201。
- TD 误差 $\delta_t \doteq R_{t+1}+\gamma V(S_{t+1})-V(S_t)$ — (6.5)，L2224；MC 误差可写成 TD 误差之和 (6.6) L2230。
- Sarsa：$Q(S_t,A_t)\leftarrow Q(S_t,A_t)+\alpha[R_{t+1}+\gamma Q(S_{t+1},A_{t+1})-Q(S_t,A_t)]$ — (6.7)，L2344；五元组 $(S_t,A_t,R_{t+1},S_{t+1},A_{t+1})$ 得名；伪码 L2357–L2368。
- Q-learning：$Q(S_t,A_t)\leftarrow Q(S_t,A_t)+\alpha[R_{t+1}+\gamma\max_a Q(S_{t+1},a)-Q(S_t,A_t)]$ — (6.8)，L2389；直接逼近 $q_*$，与所遵循的策略无关（L2392）；伪码自 L2394 起（**在本片边界处被截断**）。

## 4. 它声称的效果（数字/图 + 条件 + 基线）

- **Fig 4.1 / Example 4.1**（L1416、L1429）：4×4 gridworld，14 个非终态、4 动作、每步奖励 −1、无折扣回合式。随机策略下迭代政策评估的收敛过程；$v_\pi$ 等于"到终止的期望步数的负数"。第 3 次迭代起贪心策略即最优。基线：等概率随机策略。
- **Example 4.2 Jack's Car Rental**（L1514）：两地点，租出赚 $10，夜间调车 $2/辆，需求/归还为 Poisson（需求 λ=3、4，归还 λ=3、2），每地点上限 20 辆，一夜最多调 5 辆，$\gamma=0.9$，连续式有限 MDP。政策迭代**只用少数几次迭代**就收敛；Fig 4.2 给出前 5 个策略与最终状态值函数（L1517、L1519）。
- **Example 4.3 Gambler's Problem**（L1562–L1569）：资产 $s\in\{1..99\}$，下注 $a\in\{0..\min(s,100-s)\}$，仅在到达目标时奖励 +1，$p_h=0.4$。最优策略**不唯一**（argmax 平局构成一整个策略族）；资本 50 时孤注一掷、资本 51 时不这样（Ex 4.8, L1571–L1573）。图 4.3 给出值迭代逐次 sweep 的值函数与最终策略。
- **§4.7 效率**（L1611）：DP 最坏情况是状态数与动作数的多项式时间，而确定性策略总数是 $k^n$——**比策略空间直接搜索指数级快**；线性规划方法在大约小 100 倍的状态规模上就变得不可行；实践中 DP 可解百万状态的 MDP。
- **Example 5.1 Blackjack**（L1689）：状态 200 个（玩家和 12–21 × 庄家明牌 A–10 × 是否可用 A）；采用"20 或 21 才停"的策略；**50 万局后值函数已被很好逼近**；可用 A 的状态估计更不确定、更不规则（因为更少见）。Fig 5.1。
- **Example 5.3 Solving Blackjack**（L1794）：MC ES 找到的最优策略与 Thorp(1966) 的"基本策略"**相同，唯一例外是可用 A 时最左侧的一个凹口**，作者表示"不确定差异原因，但确信本文所示确实是该版本 blackjack 的最优策略"。
- **Example 5.4 异策略黑杰克单状态估值**（L1907）：目标策略下该状态真值 **≈0.27726**（由一亿局目标策略独立生成求得）。行为策略为等概率 hit/stick。两种异策略方法在 **1000 个异策略回合**后都接近真值；为验证可靠性做了 **100 次独立运行、每次 10000 回合**。结论：两者误差都趋零，但**加权 IS 在初期误差低得多**（Fig 5.3）。基线：普通 IS。
- **Example 5.5 无限方差**（L1912–L1937）：单状态 s，动作 right（确定性终止）/ left（0.9 回 s，0.1 终止且奖励 +1），$\gamma=1$，目标策略恒选 left（真值 = 1），行为策略 50/50。**普通 IS 即使跑数百万回合仍不收敛到 1**；加权 IS 在第一个以 left 结束的回合之后**永远给出精确的 1**。方差无穷的推导：$0.1\sum_k 0.9^k 2^k 2 = 0.2\sum_k 0.8^k=\infty$（L1936）。
- **Example 6.2 Random Walk**（L2271–L2284）：5 状态 MRP（A–E），中心出发，两端终止，右端奖励 +1，无折扣；真值 1/6,2/6,3/6,4/6,5/6；初始化 $V(s)=0.5$ 对所有 s；$\alpha=0.1$；度量 = 五状态 RMS 误差，**100 次运行平均**。结论："The TD method was consistently better than the MC method on this task."（L2284）基线：常数 $\alpha$ MC。
- **Example 6.3 批更新下的随机游走**（L2300–L2306）：把每回合后已见到的所有回合当一批反复呈现至收敛，Fig 6.2。结论：**批 TD 一致优于批 MC**；100 次独立重复。
- **Example 6.4 You are the Predictor**（L2310–L2323）：8 个回合的数据。$V(B)=3/4$（六次得 1、两次得 0）。$V(A)$ 有两个合理答案：**3/4**（先建模 Markov 过程再求值 —— 批 TD(0) 的答案）与 **0**（A 只见过一次、其后 return 为 0 —— 批 MC 的答案，且在训练数据上误差为零）。作者判断第一个答案更好（若过程确为 Markov，在未来数据上误差更低）。
- **§6.3 一般性结论**（L2325）：批 MC 总是给出**训练集上均方误差最小**的估计；批 TD(0) 总是给出**最大似然 Markov 模型下恰好正确**的估计，即 certainty-equivalence estimate。直接算该解需 $O(n^2)$ 内存、$O(n^3)$ 计算，而 TD 只需 $O(n)$ 内存加对训练集的重复计算（L2329）。
- **Example 6.5 Windy Gridworld**（L2370–L2378）：标准 gridworld 加中段向上的"风"，每列风强不同；四动作；无折扣回合式、到达目标前恒定奖励 −1（原文 L2372 写 "constant rewards of 1 until the goal state is reached"，符号疑为 −1 的排版丢失）。$\varepsilon$-贪心 Sarsa，$\varepsilon=0.1$、$\alpha=0.5$、$Q(s,a)=0$ 初始化。**到 8000 时间步时贪心策略早已最优**；持续的 $\varepsilon$-贪心探索把平均回合长度保持在约 **17 步，比最小 15 步多两步**。
- **§6.2 收敛性主张**（L2267）：TD(0) 对任意固定策略被证明收敛到 $v_\pi$——常数步长下依均值收敛（步长足够小），步长按随机逼近条件 (2.7) 递减时以概率 1 收敛。
- **§6.4 Sarsa 收敛性**（L2353）：在通常步长条件 (2.7) 下，只要所有状态–动作对被访问无限次、且策略极限上收敛到贪心，Sarsa 以概率 1 收敛到最优策略与最优动作值函数（例如 $\varepsilon$-贪心取 $\varepsilon=1/t$）。
- **§6.5 Q-learning**（L2392）：在"所有对持续被更新"的假设下加通常随机逼近条件，Q 被证明以概率 1 收敛到 $q_*$。

## 5. 它的实验条件（拓扑/规模/负载怎么设；训练与评估是否同一套）

本片是教材，无自采数据实验，"实验条件"即各例子的设定，逐条列出：

| 例子 | 规模/拓扑 | 负载/随机性 | 折扣 | 训练=评估？ |
|---|---|---|---|---|
| Ex 4.1 gridworld (L1416) | 4×4，14 非终态 | 等概率随机策略；越界留在原地 | 无折扣（$\gamma$ 未给，回合式） | 评估随机策略本身 |
| Ex 4.2 Jack's Car (L1514) | 2 地点，各 ≤20 辆 | Poisson 需求(3,4)/归还(3,2)；最多调 5 辆 | $\gamma=0.9$ | 连续式有限 MDP，政策迭代求最优 |
| Ex 4.3 Gambler (L1562) | 资本 1–99 | 抛硬币，$p_h=0.4$ | 无折扣 | 值迭代求最优 |
| Ex 5.1/5.3 Blackjack (L1687,L1794) | 200 状态 | 无限牌堆（有放回） | $\gamma=1$ | 5.1 是评估固定策略；5.3 是 ES 控制 |
| Ex 5.4 异策略黑杰克 (L1907) | 单状态估值 | 行为策略 50/50 hit/stick | 未特别说明 | 行为策略 ≠ 目标策略（**训练分布与评估目标刻意不同**） |
| Ex 5.5 无限方差 (L1912) | 1 状态 2 动作 | left: 0.9 回环 / 0.1 终止 | $\gamma=1$ | 行为策略 ≠ 目标策略 |
| Ex 6.2/6.3 Random Walk (L2279) | 5 状态链式 MRP | 左右各 1/2 | 无折扣 | 训练=评估（度量对真值的 RMS），100 次运行平均 |
| Ex 6.5 Windy Gridworld (L2370) | 网格 + 中段风 | 确定性风（按列位移）；Ex 6.10 才引入随机风 | 无折扣回合式 | Sarsa 在线学习，贪心策略轨迹另画（关掉噪声） |

要点：**唯一一处"训练分布与评估目标刻意分离"的设定是异策略（5.4/5.5 与 §5.5 全节）**。其余例子训练与评估同源。

## 6. 它自己承认的局限（逐字引用）

本片承认的局限非常多，逐字摘录（含行号）：

- **精确解依赖三个假设**：L1289 — "This solution relies on at least three assumptions that are rarely true in practice: (1) the dynamics of the environment are accurately known; (2) computational resources are su**cient to complete the calculation; and (3) the states have the Markov property."
- **必须退而求近似**：L1289 — "In reinforcement learning one typically has to settle for approximate solutions." L1311 — "optimal policies can be generated only with extreme computational cost … it is an ideal that agents can only approximate."
- **算力是核心约束**：L1311 — "A critical aspect of the problem facing the agent is always the computational power available to it, in particular, the amount of computation it can perform in a single time step."
- **DP 的适用边界**：L1611 — "DP may not be practical for very large problems"；L1613 — "DP is sometimes thought to be of limited applicability because of the curse of dimensionality … Large state sets do create di**culties, but these are inherent di**culties of the problem, not of DP as a solution method."
- **政策迭代伪码有 bug（作者自陈）**：L1521 — "The policy iteration algorithm on page 80 has a subtle bug in that it may never terminate if the policy continually switches between two or more policies that are equally good. This is okay for pedagogy, but not for actual use."
- **MC ES 收敛性未证明**：L1792 — "Convergence to this optimal fixed point seems inevitable as the changes to the action-value function decrease over time, but has not yet been formally proved. In our opinion, this is one of the most fundamental open theoretical questions in reinforcement learning (for a partial solution, see Tsitsiklis, 2002)."
- **异策略 MC 控制学得慢**：L2027 — "A potential problem is that this method learns only from the tails of episodes, when all of the remaining actions in the episode are greedy. If nongreedy actions are common, then learning will be slow, particularly for states appearing in the early portions of long episodes. Potentially, this could greatly slow learning. There has been insu**cient experience with o**-policy Monte Carlo methods to assess how serious this problem is."
- **异策略 IS 的方差问题**：L1901 — "Ordinary importance sampling is unbiased whereas weighted importance sampling is biased (though the bias converges asymptotically to zero). On the other hand, the variance of ordinary importance sampling is in general unbounded … In practice, the weighted estimator usually has dramatically lower variance and is strongly preferred."
- **逐决策加权 IS 无一致估计**：L2122 — "Is there a per-decision version of weighted importance sampling? This is less clear. So far, all the estimators that have been proposed for this that we know of are not consistent (that is, they do not converge to the true value with infinite data)."
- **异策略 MC 整体未定**：L2138 — "Despite their conceptual simplicity, o**-policy Monte Carlo methods for both prediction and control remain unsettled and are a subject of ongoing research."
- **"谁学得更快"是未解问题**：L2269 — "At the current time this is an open question in the sense that no one has been able to prove mathematically that one method converges faster than the other. In fact, it is not even clear what is the most appropriate formal way to phrase this question!"
- **在线 TD vs MC 效率结论有限**：L2327 — "At the current time nothing more definite can be said about the relative e**ciency of online TD and Monte Carlo methods."
- **黑杰克策略与 Thorp 的差异**：L1794 — "We are uncertain of the reason for this discrepancy, but confident that what is shown here is indeed the optimal policy for the version of blackjack we have described."
- **MC 不能用于风网格**：L2378 — "Note that Monte Carlo methods cannot easily be used here because termination is not guaranteed for all policies."

## 7. 它没做但看起来能做的地方（基于本片内容）

1. **把 TD 误差 (6.5) 当成"时延预测的在线残差"来用**。Example 6.1 Driving Home（L2239–L2255）本质就是一个**时延预测**任务：状态=行程阶段，奖励=各段耗时，值=剩余时间的期望。作者明确点出 TD 的价值在于"不必等到抵达终点就能修正预测"（L2253）。教材只把它当直觉例子，**没有把它形式化成可部署的在线时延/到达时刻预测器**（例如带时变负载的排队系统）。这是最直接可接的一步。
2. **§6.2 的"哪个学得更快"判据缺失**（L2269 自陈）。可以构造一个受控实验：在同一 MRP 上扫描 $\alpha$ 网格，把 TD(0) 与常数 $\alpha$ MC 的样本效率画成 Pareto 前沿，并给出"在何种非平稳程度下 TD 优势消失"的边界——教材只给了单一 $\alpha=0.1$ 的图（Fig 6.2 附近，L2284），且 Ex 6.4（L2288）自己就在问"换一组 $\alpha$ 会不会改变结论"。
3. **确定性等价解的可计算近似**。§6.3 指出批 TD(0) 收敛到 certainty-equivalence estimate，直接算需 $O(n^2)$ 内存/$O(n^3)$ 时间，而 TD 只要 $O(n)$（L2329）。**没人给出"用 TD 逼近该解时的误差–内存权衡曲线"**——这是一个可以立刻量化的实验。
4. **加权 IS 的方差–偏差折中缺乏系统刻画**。L1901 只给"加权在实践中方差低得多"这一定性结论，Fig 5.3 只有一个状态、一条曲线。可以扫 $\rho$ 分布的重尾程度做一个可复现的方差对照实验。
5. **异步 DP（§4.5）的更新调度策略**。L1587 明确说"可以通过选择要更新的状态来加速、可以跳过与最优行为无关的状态，一些想法在第 8 章讨论"，但本片内**没有给出任何调度启发式或性能界**。给定一个状态访问分布，最优更新顺序是什么，看起来是一个开放且可实验的问题。
6. **GPI 的收敛粒度**（§4.6, L1593–L1601）：教材说"只要两个过程都持续更新所有状态，最终结果通常相同"，用词是 "typically"。**什么条件下 GPI 会不收敛**，本片只给了肯定性的直觉图，没给反例或界。

## 8. 和同批其他篇的关系

- 本片是**方法论底座**，不是同类应用论文。若同批有做"强化学习用于卫星/网络资源调度"的篇目，它们大概率是本片第 4–6 章方法的下游使用者（尤其 Sarsa(6.7)/Q-learning(6.8)，因为这两者是 model-free 控制的标准入口）。
- **本片内部**：Ch.4 的 DP → Ch.5 的 MC → Ch.6 的 TD 是一条显式的"逐步去假设"链，第 6 章开头自己写明 TD 是 MC 与 DP 的结合（L2168），并预告第 7 章 n-step 算法是 TD 到 MC 的桥、第 12 章 TD(λ) 把两者统一。
- **引用同批其他篇**：无法从本片判断（本片只有本书内部的章节交叉引用与历史文献引用，未见与本批其他文献的互引）。
- **像谁/不像谁**：本片引出的历史线索（L1255–L1272, L1635）：MDP 理论承自最优控制（Bellman 1957a、Howard 1960、Puterman 1994）；多臂赌博机线索接 Thompson(1933,1934)、Robbins(1952) —— **这暗示本批若有赌博机/bandit 的文献，与本片的第 2 章是同一谱系**。Watkins(1989) 是把 RL 与 MDP 及增量 DP 连起来的关键节点（L1272、L1297、L1635、L2386）。

## 9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实

**没有直接贡献**——本片是 RL 理论教材，全片未出现任何卫星、链路、排队、到达率或时延指标（这一点是逐行读完后的事实，不是检索结论）。

但有三条**可迁移的事实**，是本片真正给出的：

1. **一个时延预测的完整 RL 形式化样例存在于本片**：Example 6.1 Driving Home（L2239–L2242）明确把"剩余时间"当状态值、"各段耗时"当奖励、$\gamma=1$ 使 return 恰等于实际剩余时间、状态值等于期望剩余时间。这是本片里唯一一个把"时延"直接当值函数语义的例子，且作者给出了逐段的 TD 修正表（L2240 表格：预测总时 30→40→35→40→43→43）。**对"时延预测"这件事，这是一个可直接套用的建模模板**。
2. **在线/单步更新对长时延反馈是必需的**：L2265 指出若回合很长或根本没有回合（continuing task），"把所有学习推迟到回合结束"就太慢。卫星链路这类连续运行系统正属于此类，这条直接支持选 TD 而非 MC。
3. **非平稳性下的步长权衡有明确表述**：L2284 指出常数步长 $\alpha$ 下值估计会"无限期地随最近回合的结果波动"（fluctuate indefinitely），这与"负载变化"场景下必须持续跟踪而非收敛到固定点的需求一致——但**本片没有给出针对非平稳负载的跟踪误差界**，只说"在实践中 TD 通常比常数 $\alpha$ MC 收敛更快"（L2269，且限定 "on stochastic tasks"）。

另有一处**必须标注的排版问题**：L2276 的随机游走 MRP 图示被 OCR 成了一段无意义的公式 $\boxed{1+\sqrt[0]\alpha+\cdots=0}$，真实拓扑靠 L2279 的文字描述（5 状态 A–E、中心 C 出发、两端终止）恢复。

## 10. 一句话评价（在方法谱系里的位置）

本片是"RL 方法谱系的正典坐标系"：Ch.4 把 Bellman 最优方程 (3.19)(3.20) 直接改写成赋值语句得到 DP（**有模型 + 期望更新 + 自举**），Ch.5 换成采样平均得到 MC（**无模型 + 完整回报 + 不自举**），Ch.6 换成就地单步自举得到 TD/Sarsa/Q-learning（**无模型 + 采样 + 自举**）——三者不是三套新方法，而是同一组 Bellman 方程在"模型/采样 × 自举/不自举"两个正交维度上的四个格点；本片的价值在于把这张格子图连同每格的收敛条件（或"尚未证明"的诚实标注，如 L1792、L2122、L2269）一起交代清楚。

---

## 本片要点（供主控合并）

1. **本片确立了三类方法的分工坐标**：DP（有模型、期望更新、自举）→ MC（无模型、完整回报、不自举）→ TD（无模型、采样、自举）。第 6 章开头 L2168 自陈 TD 是"Monte Carlo 想法与 DP 想法的结合"，且三类方法的差别**仅在预测问题的解法**（L2170）。关键更新式：DP 政策评估 (4.5) L1360、值迭代 (4.10) L1536、MC 增量式 (5.8) L1966、TD(0) (6.2) L2183、TD 误差 (6.5) L2224、Sarsa (6.7) L2344、Q-learning (6.8) L2389。

2. **本片反复自陈的"未证明/未定"清单是本篇最硬的诚实信号**，共 8 处：政策迭代伪码有终止性 bug（L1521）；MC ES 收敛性未证明，作者称其为"RL 最基本的开放理论问题之一"（L1792）；逐决策加权 IS 无一致估计（L2122）；异策略 MC 整体"unsettled … ongoing research"（L2138）；"谁学得更快"数学上未证且"连怎么形式化提问都不清楚"（L2269）；在线 TD vs MC 效率"nothing more definite can be said"（L2327）。**引用本片时不应把 TD 优于 MC 当成定理，那是经验观察。**

3. **批 TD(0) 收敛到 certainty-equivalence estimate，这是 TD 快于 MC 的机制性解释**（L2325–L2329）：批 MC 最小化训练集均方误差，批 TD(0) 给出最大似然 Markov 模型下恰好正确的解；Example 6.4（L2310–L2323）用 8 个回合的最小反例说明两者给出 $V(A)=3/4$ vs $0$。直接算该解需 $O(n^2)$ 内存 / $O(n^3)$ 时间，而 TD 只需 $O(n)$ 内存。

4. **异策略重要性采样的方差问题是本片给出的最锋利的负面结果**：Example 5.5（L1912–L1937）构造单状态 MDP（left 以 0.9 回环、0.1 终止得 +1，目标策略恒选 left，$\gamma=1$），**普通 IS 即使跑数百万回合仍不收敛到真值 1**，而加权 IS 在第一个合格回合后就恒等于 1；方差无穷的推导 $0.2\sum_k 0.8^k=\infty$ 在 L1936。教材结论：加权 IS "通常方差低得多，被强烈推荐"，但**有偏**（L1901）。

5. **本片对"负载变化下到达率/时延"无直接贡献，但 Example 6.1 Driving Home（L2239–L2255）是一个现成的时延预测形式化模板**：状态=行程阶段、奖励=各段耗时、$\gamma=1$ 使 return 等于实际剩余时间、状态值=期望剩余时间；作者给出 30→40→35→40→43→43 的逐段 TD 修正表并强调"不必等到终点就能修正预测"。配套事实：长回合/无回合任务必须用 TD 而非 MC（L2265）；常数 $\alpha$ 下估计会随最近回合无限波动，适合作非平稳跟踪但**本片未给跟踪误差界**（L2284）。
