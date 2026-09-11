# LJG6ZW7B 分片 part1（覆盖行号区间 L1–1200）

> 读物身份：Sutton & Barto《Reinforcement Learning: An Introduction》第二版（MIT Press，2018/2020，CC BY-NC-ND 2.0；LCCN 2018023826；ISBN 9780262039246）——**教材，不是论文**（L1–L58）。
> 全文 9596 行；本片逐字读完 **L1–L1200**，覆盖：版权页与目录（L1–L245）、二版/一版前言（L246–L281）、记号总表（L282–L341）、第 1 章 Introduction（L342–L560）、Part I 引言（L561–L570）、第 2 章 Multi-armed Bandits（L571–L906）、第 3 章 Finite Markov Decision Processes 的前 3.6 节开头（L907–L1200）。
> 读法：按行序逐段通读，未做任何关键词检索；行号均指原文文件行号（本片与原文行号一一对应）。

---

## 1. 一句话

这一篇（本片范围）**没有提出新方法**，它做的是"立规矩"：把"从交互中学习以达到目标"形式化为**有限 MDP + 值函数估计**，并用 k-armed bandit 这一个只有单状态的特例，把**探索/利用冲突**的几种基本解法（ε-greedy、乐观初值、UCB、soft-max 梯度）摊开对比，同时在书中给出全书统一的记号体系（L282–L341、L342–L344、L907–L914）。

## 2. 问题设定

- 核心问题：智能体**不被告诉正确动作**，只能靠试错 + 延迟奖励去发现哪种动作能带来最多奖励；这两个特征被作者称为 RL 区别于其他机器学习的根本（L352）。
- 与监督/无监督学习的分野：监督学习有"教师给正确标签"，无监督是找隐藏结构，RL 是**最大化一个标量奖励信号**，作者主张把 RL 视为第三范式（L358–L360）。
- 全书的框架选择：把问题形式化为**不完全已知 MDP 的最优控制**，含三要素——感知（状态）、动作、目标（奖励）（L356）。
- 单状态特例（第 2 章）：反复在 k 个动作中选一个，每次得到该动作对应分布的一个数值奖励，目标是在（例如）1000 步内最大化期望总奖励（L583）。
- 冲突的正式表述：exploit 是单步最优，explore 是长期最优；"the exploration–exploitation dilemma has been intensively studied by mathematicians for many decades, yet remains unresolved"（L362）。作者明确声明本书**不追求精巧的平衡**："In this book we do not worry about balancing exploration and exploitation in a sophisticated way; we worry only about balancing them at all."（L601）
- MDP 层的问题设定：动作不仅影响即时奖励，还影响后续状态，从而影响后续所有奖励；因此要估计的是 q*(s,a) 或 v*(s)，而不是 bandit 里的 q*(a)（L911）。
- 现实约束：作者承认表述选择（状态/动作如何表示）"at present more art than science"，且本书**不解决状态表示问题**（L972–L974、L407 段落内 "we do not address the issues of constructing, changing, or learning the state signal"）。

## 3. 方法骨架

本片出现的机制主干（按原文顺序）：

**(a) 记号体系（L282–L341）**：随机变量大写、实例小写；值函数小写（v_π），表格式估计大写（Q_t(s,a)）；转移与奖励用四参数联合概率 p(s′,r|s,a) 而非一版的 P、R 两套记号（L246–L265 前言中说明改动理由）。

**(b) 第 1 章的 TD 直觉示例（tictactoe，L416–L463）**：
- 状态 = 棋盘局面，动作 = 落子，价值 = 该局面获胜概率估计；初始全设 0.5，终局（三连或平局）为 1/0（L430）。
- 更新律：V(S_t) ← V(S_t) + α[V(S_{t+1}) − V(S_t)]（L442），α 为步长；作者称这是 temporal-difference 方法，因为更新由**相邻两个时刻估计之差**驱动（L445）。
- 学习只发生在贪心走子之后，探索走子不学习（L432、图 1.1 说明 L437）。

**(c) 第 2 章 bandit 四类方法**：
- 动作价值 = 期望奖励 q*(a) ≐ E[R_t | A_t = a]（L590）；估计 Q_t(a)（L593）。
- 样本平均估计 Q_t(a) = Σ R_i·1_{A_i=a} / Σ 1_{A_i=a}（L608，式 2.1）；贪心选择 A_t ≐ argmax_a Q_t(a)（L616，式 2.2）；ε-greedy：以 1−ε 贪心、以 ε 等概率随机（L619）。
- 增量实现：Q_{n+1} = Q_n + (1/n)[R_n − Q_n]（L660，式 2.3）；作者把它抽象成全书通用形式 **NewEstimate ← OldEstimate + StepSize[Target − OldEstimate]**（L668，式 2.4），并给出完整 bandit 伪码（L677–L684：Q(a)←0、N(a)←0、循环 R←bandit(A)、N(A)++、Q(A)←Q(A)+(1/N(A))[R−Q(A)]）。
- 非平稳跟踪：常数步长 Q_{n+1} ≐ Q_n + α[R_n − Q_n]（L691，式 2.5），展开为指数近因加权平均（L697，式 2.6）；随机逼近收敛条件 Σα_n=∞ 且 Σα_n²<∞（L705，式 2.7），作者随即指出常数步长**不满足第二条**、估计永不真正收敛（L710）。
- 乐观初值：把 Q_1(a) 全设为 +5（真值 ~N(0,1)），用"失望"驱动探索（L720）。
- UCB：A_t ≐ argmax_a [ Q_t(a) + c·√(ln t / N_t(a)) ]（L748，式 2.10）；根号项作为不确定性度量，c 控制探索强度（L751–L753）。
- 梯度 bandit：不估价值而学偏好 H_t(a)，用 soft-max/Gibbs 分布 Pr{A_t=a} ≐ e^{H_t(a)}/Σ_b e^{H_t(b)} ≐ π_t(a)（L767，式 2.11）；更新 H_{t+1}(A_t) ≐ H_t(A_t) + α(R_t − R̄_t)(1 − π_t(A_t))，其余动作 H_{t+1}(a) ≐ H_t(a) − α(R_t − R̄_t)π_t(a)（L777，式 2.12），其中 R̄_t 是奖励基线（L780）；作者用商法则把该更新推导为**随机梯度上升**的样本形式（L789–L847），并说明基线可任取、只影响方差（L849）。
- 联想搜索/contextual bandit：动作只影响即时奖励但存在区分情境的线索，是 bandit 到全 RL 的中间态（L851–L857）。

**(d) 第 3 章 MDP 主干（L907–L1200）**：
- 交互序列 S_0,A_0,R_1,S_1,A_1,R_2,…（L922–L925，式 3.1）。
- 动力学 p(s′,r|s,a) ≐ Pr{S_t=s′,R_t=r | S_{t−1}=s,A_{t−1}=a}（L931，式 3.2），归一化 Σ_{s′}Σ_r p = 1（L937，式 3.3）；由此导出 p(s′|s,a)（L945，式 3.4）、r(s,a)（L951，式 3.5）、r(s,a,s′)（L957，式 3.6）。
- 马尔可夫性质：给定前一步状态与动作后，未来与更早历史无关（L940）；作者强调这是**对状态的约束而非对决策过程的约束**。
- 奖励假设（reward hypothesis）："That all of what we mean by goals and purposes can be well thought of as the maximization of the expected value of the cumulative sum of a received scalar signal (called reward)."（L1004）
- 回报：episodic G_t ≐ R_{t+1}+…+R_T（L1017，式 3.7）；continuing 用折扣 G_t ≐ Σ_{k≥0} γ^k R_{t+k+1}（L1029，式 3.8）；递归 G_t = R_{t+1} + γG_{t+1}（L1039，式 3.9）；常数奖励 +1 时 G_t = 1/(1−γ)（L1047，式 3.10）。
- 统一记号：把 episode 终止看作进入**只自环且只产生零奖励的吸收态**，从而用式 (3.11) G_t ≐ Σ_{k=t+1}^{T} γ^{k−t−1}R_k 同时覆盖 episodic 与 continuing（L1076–L1090）。
- 值函数：v_π(s) ≐ E_π[G_t | S_t=s]（L1103，式 3.12）；q_π(s,a) ≐ E_π[G_t | S_t=s, A_t=a]（L1111，式 3.13）。
- Bellman 方程（v_π）：v_π(s) = Σ_a π(a|s) Σ_{s′,r} p(s′,r|s,a)[ r + γ v_π(s′) ]（L1125，式 3.14）；v_π 是其 Bellman 方程的**唯一解**（L1139 段首）；备份图（backup diagram）的定义（L1132、L1139）。
- 最优性：π ≥ π′ 当且仅当对所有 s 有 v_π(s) ≥ v_{π′}(s)；存在至少一个最优策略 π*（L1182）；v*(s) ≐ max_π v_π(s)（L1185，式 3.15）；q*(s,a) ≐ max_π q_π(s,a)（L1193，式 3.16）；q*(s,a) = E[R_{t+1} + γv*(S_{t+1}) | S_t=s, A_t=a]（L1199，式 3.17）。
- 三个具体 MDP 例子：**回收机器人**（2 状态 high/low × 3 动作 search/wait/recharge，给全表 p 与 r，L986–L996）；**Gridworld**（4 动作，越界奖励 −1，从 A 任一动作 +10 并到 A′，从 B 任一动作 +5 并到 B′，L1141）；**高尔夫**（状态=球位置，动作=选杆，奖励=−1/杆，故价值 = 负的剩余杆数，L1154–L1156）。另有**杆平衡**例子说明 episodic（每步 +1，直到失败）与 continuing（失败时 1，其余 0）两种建模（L1052–L1058）。

## 4. 它声称的效果（数字/图与条件、基线）

- 图 2.2（L632–L637）：10-armed testbed 上比较 greedy 与 ε-greedy(ε=0.01, 0.1)，全部用样本平均、初值 0。数字：**greedy 长期只到约 1 奖励/步，而该 testbed 最优约 1.54**；greedy 只在约 **1/3** 的任务中找到最优动作，另 2/3 因早期采样不佳而再也不回去；**ε=0.1 探索更多、更早找到最优，但选中最优动作的比例从未超过 91%**；ε=0.01 改进更慢但最终在两个指标上都优于 ε=0.1。基线是 greedy。
- 图 2.3（L722–L725）：乐观初值（Q_1=+5，贪心）与 ε-greedy(Q_1=0) 对比，两者都用常数 α=0.1；乐观法**初期更差、后期更好**，因为其探索随时间递减。
- 图 2.4（L755–L758）：UCB 在 testbed 上"generally performs better than ε-greedy"，**唯一例外是最初 k 步**（此时它随机试未试过的动作）；L760 还留下一个现象——**第 11 步出现明显尖峰**（作为习题给出，未在正文解释）。
- 图 2.5（L782–L785）：把真值 q*(a) 从均值 0 平移到均值 **+4** 后重做梯度 bandit。有基线时**完全不受影响**（基线瞬时适配新水平）；去掉基线（R̄_t 取常数 0）则性能**明显退化**。
- 图 2.6（L865–L868）：**参数研究**（把学习曲线在 1000 步上取平均，横轴为各算法自己的参数并按 2 的倍数在对数尺度上取点）。结论：所有算法都呈**倒 U 形**，都在参数中间值最好；对参数**不敏感**（好参数区间跨约一个数量级）；**"Overall, on this problem, UCB seems to perform best."**
- 总结性判断（L870）："Despite their simplicity, in our opinion the methods presented in this chapter can fairly be considered the state of the art."（作者认为这些简单方法在**完整 RL 问题**上可算 state of the art，更复杂方法因复杂度和假设而不可行。）
- 第 1 章的 tic-tac-toe（L447）：若步长按合适方式递减，方法对**任意固定对手**收敛到各状态获胜真概率，且（除探索步外）走的确实是该对手下的最优着法；若步长不降到 0，则对**缓慢改变打法的对手**也表现良好。
- 第 1 章引用的外部结果（L455）：Tesauro 用神经网络 + 该 TD 方法学 backgammon，状态数约 **10^20**，最终"better than any previous program and eventually better than the world's best human players"。
- 历史性断言（L549）：TD 与最优控制两条线在 **1989 年 Watkins 的 Q-learning** 处才完全合流；1992 年 TD-Gammon 带来额外关注。

## 5. 它的实验条件（拓扑/规模/负载；训练与评估是否同一套）

本片没有真实系统实验，只有数值 testbed；条件如下（全部给出）：

- **10-armed testbed**（L625–L630）：k=10；2000 个**随机生成的 bandit 问题**；每个问题里 q*(a) 取自 N(0,1)；实际奖励 R_t 取自 N(q*(A_t),1)。一次运行 = 1000 步；对 2000 个独立问题各跑一次取平均。**评估集与训练集是同一批随机问题**（每个算法在同一 testbed 上跑，改变的是算法与参数）。
- 图 2.3 的额外条件：常数步长 α=0.1（L725）。
- 图 2.5 的额外条件：真值均值移到 **+4**（方差仍为 1）（L782、L785）。
- 图 2.6 的参数研究协议：每点 = **1000 步的平均奖励**，参数按 2 倍递增、画在对数横轴上（L865、L868）。
- 书中**留给读者**的非平稳与长跑设定（可直接照做）：习题 2.5——所有 q*(a) 起始相等，每步加 N(0, **0.01**) 的随机游走增量，ε=0.1，跑 **10,000** 步，比较样本平均与常数 α=0.1（L714）；习题 2.11——跑 **200,000** 步，性能取**最后 100,000 步的平均奖励**（L880）。
- Gridworld（L1146）：等概率随机策略，γ=0.9，v_π 由解线性方程组 (3.14) 得到——这是**精确解**，不是学习得到的。
- 杆平衡：episodic（每步 +1，直到失败；成功永远平衡则回报为 ∞）或 continuing（失败给 1、其余 0，回报与 −γ^{K−1} 相关）（L1052–L1058）。

## 6. 它自己承认的局限（逐字引用）

- L601："In this book we do not worry about balancing exploration and exploitation in a sophisticated way; we worry only about balancing them at all."
- L362（段末）："The exploration–exploitation dilemma has been intensively studied by mathematicians for many decades, yet remains unresolved."
- L599："However, most of these methods make strong assumptions about stationarity and prior knowledge that are either violated or impossible to verify in most applications and in the full reinforcement learning problem…The guarantees of optimality or bounded loss for these methods are of little comfort when the assumptions of their theory do not apply."
- L710："In the latter case, the second condition is not met, indicating that the estimates never completely converge but continue to vary in response to the most recently received rewards."（常数步长永不真正收敛）
- L755："UCB often performs well, as shown here, but is more dicult than "-greedy to extend beyond bandits…One diculty is in dealing with nonstationary problems…Another diculty is dealing with large state spaces, particularly when using function approximation…In these more advanced settings the idea of UCB action selection is usually not practical."
- L874（Gittins index）："it does require complete knowledge of the prior distribution of possible problems, which we generally assume is not available. In addition, neither the theory nor the computational tractability of this approach appear to generalize to the full reinforcement learning problem."
- L878（Bayes 最优平衡）："It is generally not feasible to perform this immense computation exactly…But that is a topic for research and beyond the scope of this introductory book."（并给出规模感：即使只有 2 个动作 2 种奖励，1000 步的树也有 **2^2000** 个叶节点）
- L972："In reinforcement learning, as in other kinds of learning, such representational choices are at present more art than science."
- L974："our primary focus is on general principles for learning how to behave once the representations have been selected."
- L407 段（第 1.4 节）："We do not address the issues of constructing, changing, or learning the state signal in this book (other than briefly in Section 17.3)."
- L453（诚实声明适用边界）：连续时间问题"the theory gets more complicated and we omit it from this introductory treatment."
- L1090：episodic/continuing 统一记号**不覆盖**后续第 10 章的"既 continuing 又无折扣"的设定（"Later, in Chapter 10, we will introduce a formulation that is both continuing and undiscounted."）。

## 7. 它没做但看起来能做的地方（基于本片内容，不是套话）

- **参数研究法（L865、L868）搬到负载维度**：书中把"算法性能 vs 自身参数"画成倒 U 曲线并比较参数敏感度；同样可以直接画"性能 vs 负载水平/到达率"的曲面，把敏感度当作首要指标（作者自己说"attend not just to how well it does at its best parameter setting, but also to how sensitive it is"）。
- **非平稳跟踪的现成对照实验**：习题 2.5（L714）与 2.11（L880）给了一套完整的、可复现的协议（随机游走漂移 + 常数 α vs 样本平均 + 长跑分段统计），把它换成"负载突变/业务量阶跃"就是本课题最直接的落点。
- **UCB 的非平稳缺口（L755）**：作者直接点名 UCB 难处理非平稳与函数逼近——这正是"负载变化"场景下的公开缺口；本片之后（第 2 章书目注 L894）指出正文 UCB 即文献中的 UCB1（Auer et al. 2002），给了扩展的锚点。
- **奖励基线作为"整体漂移"吸收器（L780、L782、L849）**：证据显示基线能让算法对奖励整体平移**完全免疫**。凡是"负载抬升导致所有动作的奖励一起平移"的场景，这一机制可零成本复用。
- **Gittins / Thompson sampling 的先验问题（L874、L876）**：作者说 Gittins 需要完整先验分布因而不可用，而 Thompson sampling 常与最好的无分布方法持平。在 LEO 场景下先验可以从历史 trace 估出来——这是书中明确留下的空白。
- **把"时延/步数"直接编码为奖励的范式**：Golf 例子中价值 = 负的剩余杆数（L1154–L1156）；maze 例子用"逃离前每步 +1"来鼓励尽快逃离（L1008）。这给了"以时延为代价"的建模模板，但书中**没有任何截止期/超时/丢包**的对应物。
- **折扣的语义选择（L1032–L1034）**：γ=0（近视，只最大化 R_{t+1}）与 γ→1（远视）在排队/路由问题里对应"只看当前队列"与"看长期稳定性"，书中给出了二者对回报定义的精确差别，可直接用来论证参数选择。

## 8. 和同批其他篇的关系（本片视角）

- 本片是**教材的 1–3 章**，不是研究论文：它不引用同批任何文献（本片所见引用全部是 RL/最优控制/神经科学的历史文献）。是否与同批其他篇重合，**我无法从本片判定**（未读其他片）。
- 可确证的一点：这是 RL 领域的标准教科书与标准记号来源（L282–L341 记号表、L561–L570 Part I 定位）。任何把 RL 用到路由/调度/资源分配的文章，其 ε-greedy、Q-learning、Bellman 方程、折扣回报的写法都可追溯到本片这几章；因此它在同批文献里的角色更可能是**共同背景/引用源**而非可比方法。
- 本片提到的、可能在同批文献中再次出现的方法学锚点：UCB1（L894）、Thompson sampling（L876）、REINFORCE/Williams 1992（L896）、Q-learning/Watkins 1989（L549）、Dyna/模型规划（第 8 章，目录 L~110 与 L569）、average-reward 设定（第 10.3 节，目录与 L1090）。

## 9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实

**没有直接贡献**——本篇是教材，本片范围内没有任何网络/排队/到达率/时延的实验或结论。可迁移的事实有四条，且都可指回原文：

1. **非平稳是常态而非例外**："problems that are eectively nonstationary are the most common in reinforcement learning"（L710）；且在非平稳下**样本平均不合适、应给近期奖励更高权重**（L688）。这直接对应"负载变化"这一前提。
2. **常数步长的代价被写死**：α 常数时 Σα_n² 不收敛、估计**永不真正收敛**而持续跟踪最新奖励（L705、L710）——这正是"跟踪变化的负载"要付的代价，作者认为在该场景下是**可取的**。
3. **收敛条件给了可检验的门槛**：Σα_n(a)=∞ 且 Σα_n²(a)<∞（L707–L708，式 2.7），任何"步长调度"设计都可以先用这两条筛一遍。
4. **时延可以作为负奖励/步数代价直接进 MDP**：Golf（L1154–L1156，价值 = 负剩余杆数）、maze（L1008，"reward is often 1 for every time step that passes prior to escape; this encourages the agent to escape as quickly as possible"）、杆平衡（L1052–L1058）。但书中**没有**截止期、超时丢弃、队列长度、到达率这些量——这些是本课题相对本篇的增量空间。

## 10. 一句话评价

这是把"目标导向的交互式学习"标准化为**有限 MDP + 值函数 + Bellman 方程**的奠基教材第 1–3 章：不提出新算法，而是**定义整个领域的问题、记号与基线**（ε-greedy / 乐观初值 / UCB / 梯度 bandit 四种探索策略，以及回报、折扣、策略、值函数、Bellman 方程与最优性）；在方法谱系中的位置是"所有后续 RL 方法的公共祖先与记号来源"。

---

## 本片要点（供主控合并）

1. **本篇是教材不是论文**（Sutton & Barto 二版，MIT Press 2018/2020，L1–L58）；本片 L1–L1200 覆盖第 1 章全文、第 2 章全文、第 3 章至 3.6 节开头（L342–L344、L571–L573、L909–L914）。全书的三个部分划分与 17 章目录在 L51–L245。
2. **第 2 章给出了四个探索策略及其关键数字**：10-armed testbed（k=10，2000 个随机问题，q*~N(0,1)，奖励~N(q*,1)，1000 步，L625–L630）上，greedy 长期约 1 奖励/步 vs 最优约 1.54，只在约 1/3 任务找到最优；ε=0.1 从未在超过 91% 的步选中最优；参数研究（L865）显示各算法都呈倒 U 形且对参数不敏感，**UCB 在该问题上最好**（L868）；UCB 的唯一短板是最初 k 步（L758）和第 11 步的尖峰（L760）。
3. **非平稳是本片最可迁移的一条**：作者明说"effectively nonstationary 的情形在 RL 中最常见"（L710），并给出常数步长永不收敛的准确表述（L705、L710）与随机逼近收敛条件 Σα=∞ ∧ Σα²<∞（L707–L708）；习题 2.5/2.11（L714、L880）给出了完整可复现的非平稳对照协议。
4. **UCB 在非平稳与函数逼近下"通常不实用"**（L755），Gittins 需要完整先验分布且不可推广（L874），Bayes 最优平衡的计算被明确判定为不可行（L878，2^2000 叶节点）——这三条是书**自己承认的缺口**，也是"负载变化"场景的入口。
5. **第 3 章是问题定义而非结果**：p(s′,r|s,a)（L931）、回报与折扣（L1017、L1029、L1039，常数奖励时 1/(1−γ) 见 L1047）、episodic/continuing 统一记号（L1085，式 3.11）、v_π/q_π（L1103、L1111）、Bellman 方程（L1125，式 3.14，L1139 声明唯一解）、最优值函数与 π*（L1182–L1199）。**奖励信号只表达"要什么"不表达"怎么做"**（L1010），奖励假设原文见 L1004。

---

## 覆盖自述与阅读质量说明

- **实际覆盖：L1–L1200，全部 1200 行逐行读过**（分 7 次顺序读取；无跳读、无关键词检索）。原文该区间共 1200 行 / 约 233 KB。
- **OCR 损伤（非我漏读，如实标注）**：
  - L844：梯度 bandit 求导中一步（∂π/∂H 的商法则展开）在本篇 md 中**严重乱码**，公式已不可复原；但结论（L847 "the expected update of the gradient bandit algorithm is equal to the gradient of expected reward…an instance of stochastic gradient ascent"）是完整可读的。
  - L1141、L1146：Gridworld 段落出现**双栏 OCR 交错**（两段文字互相插入），个别句子需重排才能读通；关键数字（A 任一动作 +10 到 A′、B 任一动作 +5 到 B′、越界 −1、γ=0.9、中心值 +0.7、邻值 +2.3/+0.4/−0.4/+0.7）均可辨认。
  - L992：回收机器人的转移表在 md 中以 HTML 表格呈现，部分单元格（低电量 search 的两行奖励）错位，需要对照 L990 正文才能确定"救援奖励为 −3"。
  - L4、L473 等处存在公式中的空格丢失（如 "V ( S _ { t } )"），不影响阅读。
- **本片结束位置**：L1200 停在式 (3.17) 之后，第 3.6 节"Optimal Policies and Optimal Value Functions"尚未读完（Bellman 最优方程尚未出现），应由下一片（L1201 起）接续。
