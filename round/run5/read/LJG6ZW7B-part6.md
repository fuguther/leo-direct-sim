# LJG6ZW7B 分片 6（part6）

覆盖行号区间 **L6001–L7200**（全文 9596 行）。已逐字读完 L6001–L7200 全段，无跳跃、未越界读其他片。
文献：Sutton & Barto,《Reinforcement Learning: An Introduction》第二版（教材，非单篇论文）。
本片实际覆盖的章节（行号为原文绝对行号）：

| 行号 | 章节 |
|---|---|
| L6001–6069 | 13.6 Policy Gradient for Continuing Problems（含 continuing 情形策略梯度定理证明、actor–critic + eligibility traces 伪代码） |
| L6070–6119 | 13.7 Policy Parameterization for Continuous Actions（高斯策略、Exercise 13.4/13.5） |
| L6120–6151 | 13.8 Summary + 第13章 Bibliographical and Historical Remarks |
| L6152–6157 | Part III: Looking Deeper 引言 |
| L6158–6537 | 第14章 Psychology（14.1–14.7 + 书目注记 + Comments on Terminology） |
| L6538–6928 | 第15章 Neuroscience（15.1–15.13 + 书目注记） |
| L6929–7152 | 第16章 Applications and Case Studies（16.1 TD-Gammon、16.2 Samuel 跳棋、16.3 Watson 下注、16.4 DRAM 内存控制器、16.5 DQN 打 Atari） |
| L7153–7200 | 16.6 Mastering the Game of Go + 16.6.1 AlphaGo（**在 L7200 处被分片边界截断，AlphaGo 一节未读完**） |

---

## 1. 一句话

本片是教材的"收尾 + 第三部分"：先把第13章的策略梯度收敛到连续动作与 continuing 情形（L6001–6151），随后用三个整章把前 12 章的算法分别外推到**动物学习心理学**（第14章）、**多巴胺神经科学**（第15章）和**六个真实工程/博弈应用**（第16章）；它不提出新算法，而是主张"同一套 TD/actor–critic 机制能同时解释巴甫洛夫条件反射、多巴胺放电和 TD-Gammon/DQN/AlphaGo 的实战水平"（L6152–6155、L6929–6934）。

## 2. 问题设定

- 教材层面：前两部分只给了算法，本部分要回答"这些算法与生物学习、与真实系统落地是什么关系"（L6152–6155：survey their relationships with psychology and neuroscience, a sampling of applications, and some of the active frontiers）。
- 第14章要解决的矛盾：心理学实验中存在**时序/延迟/高阶强化**等试次级模型解释不了的现象（L6290–6294），需要一个实时的、能产生时序预测的模型（L6258–6262）。
- 第15章要解决的矛盾：多巴胺神经元既不编码运动也不编码感觉，其相位放电如何解释（L6635–6642）。
- 第16章要解决的矛盾：真实应用的状态空间远超查表能力，必须靠函数逼近 + 特征设计；而特征设计原本要人工完成（L7099–7103："Most successful applications of reinforcement learning owe much to sets of features carefully handcrafted based on human knowledge and intuition"）。
- 16.4 的领域矛盾（与本批课题最相关）：当时的 DRAM 控制器"uses policies that did not take advantage of past scheduling experience and did not account for long-term consequences of scheduling decisions"（L7059–7061）。

## 3. 方法骨架

本片不是单篇方法，而是多套机制；逐条列骨架：

**(a) continuing 情形的策略梯度/actor–critic（L6001–6069）**
- 性能定义改为平均奖励率 $J(\theta) \doteq r(\pi) = \lim_{h\to\infty}\frac1h\sum_{t=1}^h \mathbb E[R_t]$，并要求存在与 $S_0$ 无关的稳态分布 $\mu$（遍历性假设，13.15–13.16，L6006–6016）。
- 返回值改为**微分回报** $G_t \doteq R_{t+1}-r(\pi)+R_{t+2}-r(\pi)+\cdots$（13.17，L6046）；在此定义下（13.5）的策略梯度定理对 continuing 情形仍成立，书中给出完整证明（L6050–6068）。
- 伪代码（L6022–6037）：$\delta \gets R-\bar R+\hat v(S',w)-\hat v(S,w)$；$\bar R \gets \bar R+\alpha^{\bar R}\delta$；$z^w \gets \lambda^w z^w+\nabla\hat v(S,w)$；$z^\theta \gets \lambda^\theta z^\theta+\nabla\ln\pi(A|S,\theta)$；$w\gets w+\alpha^w\delta z^w$；$\theta\gets\theta+\alpha^\theta\delta z^\theta$。状态/动作/奖励/更新齐全，是后文 15.8 神经实现所依据的那套式子。

**(b) 连续动作的策略参数化（L6070–6119）**
- 策略取高斯密度 $\pi(a|s,\theta)=\frac{1}{\sigma(s,\theta)\sqrt{2\pi}}\exp(-\frac{(a-\mu(s,\theta))^2}{2\sigma(s,\theta)^2})$（13.19，L6091）。
- $\mu(s,\theta)\doteq\theta_\mu^\top x_\mu(s)$，$\sigma(s,\theta)\doteq\exp(\theta_\sigma^\top x_\sigma(s))$（13.20，L6099）——均值线性、标准差取指数保证正性。
- 资格向量两部分（Exercise 13.4，L6103–6108）。核心动机：大动作空间甚至连续动作空间下，学分布统计量而不是每个动作的概率（L6072）。

**(c) Rescorla–Wagner 模型 → 线性函数逼近（L6206–6257）**
- 状态用特征 $x(s)$，$x_i(s)=1$ 当且仅当第 $i$ 个 CS 成分出现（L6220）；聚合联结强度 $\hat v(s,w)=\mathbf w^\top\mathbf x(s)$（14.1，L6224）。
- 更新 $\mathbf w_{t+1}=\mathbf w_t+\alpha\delta_t\mathbf x(S_t)$（14.2），$\delta_t=R_t-\hat v(S_t,\mathbf w_t)$（14.3，L6230–6234）。**是误差校正型监督学习，等同 LMS/Widrow-Hoff**（L6240–6244）。

**(d) TD 模型（L6258–6289）**
- 把"试次"换成"时间步"：$\mathbf w_{t+1}=\mathbf w_t+\alpha\delta_t\mathbf z_t$（14.4，L6272），$\delta_t=R_{t+1}+\gamma\hat v(S_{t+1},\mathbf w_t)-\hat v(S_t,\mathbf w_t)$（14.5，L6276），$\mathbf z_t=\gamma\lambda\mathbf z_{t-1}+\mathbf x(S_t)$（14.6，L6286）。
- 关键：$\gamma=0$ 时退化为 Rescorla–Wagner（除 t 的含义与目标 R 领先一步）；整体等价于**线性逼近下的半梯度 TD(λ) backward view**（L6288）。

**(e) 神经 actor–critic 的 actor/critic 学习规则（L6735–6784）**
- critic：$\hat v(s,w)=w^\top x(s)$（15.1，L6752），权重增量 $\alpha^w\delta_t z^w_t$；其资格迹**只依赖突触前活动**，称 non-contingent eligibility trace（L6762–6764）→ **two-factor 学习规则**。
- actor：每个单元是 Bernoulli-logistic 单元，$\pi(1|s,\theta)=\frac{1}{1+\exp(-\theta^\top x(s))}$（15.2，L6774），$\nabla\ln\pi(A_t|S_t,\theta)=(A_t-\pi(1|S_t,\theta))x(S_t)$（15.3，L6776）；资格迹**同时依赖突触前后活动**，称 contingent eligibility trace → **three-factor 学习规则**；"the postsynaptic contingency in the eligibility traces of actor units is the only difference between the critic and actor learning rules"（L6780）。
- 对应生物学：reward-modulated STDP，多巴胺脉冲需在 STDP 条件满足后**最长可达 10 秒**的时间窗内到达（Yagishita et al. 2014，L6782）。

**(f) 16.1 TD-Gammon 骨架（L6935–7003）**
- 状态=棋盘局面，$\hat v(s,w)$ 估计**胜率**；奖励除获胜时刻外全为 0（L6949）。
- 网络：198 输入单元（每点白/黑各 4 个单元 + bar + borne-off + 轮到谁），隐藏层→单输出单元，sigmoid（L6957–6973）。
- 学习规则（16.1，L6975）：$\mathbf w_{t+1}=\mathbf w_t+\alpha[R_{t+1}+\gamma\hat v(S_{t+1},w_t)-\hat v(S_t,w_t)]\mathbf z_t$，$\mathbf z_t=\gamma\lambda\mathbf z_{t-1}+\nabla\hat v(S_t,w_t)$，梯度由**误差反传**算，$\gamma=1$（L6985）。
- 动作选择：对掷骰后约 20 种走法得到的 **afterstate**（6.8 节）估值，取最高者（L6989）。自对弈生成数据，每个局面走一步就更新一次（fully incremental，L6991）。

**(g) 16.3 Watson 下注骨架（L7027–7058）**
- 动作值 $\hat q(s,bet)=p_{DD}\times\hat v(S_W+bet,\dots)+(1-p_{DD})\times\hat v(S_W-bet,\dots)$（16.2，L7043）；$p_{DD}$ 是"该类目 DD 答对信心"。
- $\hat v$ 由 TD-Gammon 式非线性 TD(λ)+ANN 学到，但**不是自对弈**，而是对着精心构造的人类对手模型（Average / Champion / Grand Champion 三档）的**数百万次模拟对局**（L7037–7039、L7051）。
- 风险控制：从 (16.2) 中减去正确/错误 afterstate 估值标准差的一小部分，并禁止使错误答案后价值跌破某阈值的下注（L7047）。

**(h) 16.4 RL 内存控制器骨架（L7059–7096）**
- MDP：状态=**memory transaction queue 的内容**；动作=precharge / activate / read / write / NoOp；**奖励=1 当且仅当动作是 read 或 write，否则 0**（L7072）。
- 合法动作集 $\mathcal A(S_t)$ 被**预先按硬件时序/资源约束定义**，使探索永不越界（L7075–7079）；NoOp 在某状态是唯一合法动作时发出。
- 学习算法：**Sarsa**；状态由 6 个整型特征表示；线性函数逼近用 **tile coding + hashing**，32 个 tiling，每个存 256 个动作值（16-bit 定点）；ε-greedy，ε=0.05（L7085–7088）。
- 特征先由领域知识列长清单，再用仿真做 stepwise feature selection 砍到 6 个（L7088）。
- 硬件：两条五级流水线，每处理器时钟周期算并比较两个动作值；4GHz 4 核，10 个处理器周期对应 1 个 DRAM 周期，每 DRAM 周期最多可评估 12 个动作（L7090）。

**(i) 16.5 DQN 骨架（L7097–7152）**
- 网络：3 个卷积隐层（32@20×20、64@9×9、64@7×7，整流非线性）+ 1 个全连接隐层（512）+ 输出层 18 个单元（每个对应 Atari 一个动作）；输入 **84×84×4** 归一化灰度帧堆叠（L7107–7121）。
- 更新（16.3，L7130）：$\mathbf w_{t+1}=\mathbf w_t+\alpha[R_{t+1}+\gamma\max_a\hat q(S_{t+1},a,w_t)-\hat q(S_t,A_t,w_t)]\nabla\hat q(S_t,A_t,w_t)$。
- 三处改动：① experience replay（Lin 1992），把 $(S_t,A_t,R_{t+1},S_{t+1})$ 存进 replay memory，每步从记忆里**均匀随机抽**一个小批量（32 帧）更新（L7134–7142）；② 目标网络：每 C 次更新把当前权重复制到副本网络 $\tilde q$ 并冻结 C 次，用 $\max_a\tilde q$ 做目标（L7144–7148）；③ 把误差裁剪到 $[-1,1]$（L7148）。
- 奖励信号被标准化为"分数变化"：+1 / −1 / 0，从而使**同一组超参**跨游戏可用（L7124）。
- 其它：RMSProp 加速、mini-batch 平滑梯度（L7132）；ε 在前 100 万帧线性退火（L7126）。

**(j) 16.6.1 AlphaGo 骨架（L7177–7200，截断）**
- APV-MCTS：树扩展的边按 **SL-policy 网络**（13 层深度卷积，在近 3000 万人类专家着法上监督学习）给出的概率选；新节点估值 $v(s)=(1-\eta)v_\theta(s)+\eta G$（16.4，L7195），$G$ 是 rollout 回报，$\eta$ 控制混合；最终取根节点**访问次数最多**的边走子（L7195）。
- 价值网络与 SL 策略网络同构但单输出；训练分两段：先由 RL policy network（从 SL 权重初始化、策略梯度自对弈）产生对局，再用 Monte Carlo policy evaluation 训练价值网络（L7197）。全部离线训练，实战中权重冻结。

## 4. 它声称的效果（数字/图）

- **TD-Gammon**（Table 16.1，L7002）：0.0（40 隐单元、30 万局自对弈）→ 与其他程序并列最佳；1.0（80 单元、30 万局）对 Robertie/Magriel 等 −13 分/51 局；2.0（40 单元、80 万局）对若干大师 −7 分/38 局；2.1（80 单元、150 万局）对 Robertie −1 分/40 局；3.0（80 单元、150 万局）对 Kazaros **+6 分/20 局**。结论：3.0/3.1 接近甚至可能超过最强人类（L7004）。3.1 在走子决策上对人类顶尖有"lopsided advantage"、在加倍决策上有"slight edge"（L7004）。Tesauro & Galperin 1997 的 trajectory sampling 把 live play 错误率降低 **4–6 倍**，思考时间 5–10 秒/步（L7000）。
- **Watson DD 下注**（L7053）：仿真胜率 基线启发式 **61%** → 学到的价值 + 默认信心 **64%** → 加上实时 in-category 信心 **67%**；而 DD 每局只用约 1.5–2 次。作者称该方法"achieve a level of quantitative precision and real-time performance that exceeds human capabilities"（L7057）。
- **RL 内存控制器**（L7090–7092，Figure 16.4）：9 个访存密集型并行负载（科学与数据挖掘应用）上，RL 相对 FR-FCFS 提升 **7%–33%**，**几何平均 +19%**；相对不可实现的 Optimistic 上界把差距缩小 **27%**；**在线学习比训练后固定策略平均好 8%**。基线：FR-FCFS（当时平均最优）、in-order（最简）、Optimistic（不可实现的上界）。
- **DQN**（L7134）：49 个 Atari 2600 游戏，每游戏 5000 万帧（≈38 天经验），权重每游戏重置；除 6 个游戏外优于当时最好的 RL 系统，22 个游戏超过人类测试者；按"≥75% 人类得分即算人类水平"的标准，**46 个游戏中 29 个达到或超过人类水平**。消融：experience replay 与目标网络各自单独都明显提升，合起来提升"very dramatically"；深度卷积版显著优于单线性层版（L7150）。
- **AlphaGo**（L7174）：以 5:0 击败欧洲冠军樊麾；随后 4:1 击败 18 次世界冠军李世石。SL 策略网络在留出测试集上预测专家着法准确率 **57%**（当时其他团队最好 44.4%，仅用原始棋盘+走子历史时 55.7%，L7198）；RL 策略网络对 SL 策略胜率 **>80%**，对每步模拟 10 万局的 MCTS 围棋程序胜率 **85%**（L7198）。
- **14.2.4 的 TD 模型仿真**（L6318–6330）：presence 表示下复现 ISI 依赖（正 ISI 才有效、存在最优 ISI、之后衰减到 0）、serial compound 下 remote association 促进（与 Kehoe 1982 一致）、Egger–Miller 效应；**图 14.2** 给出 TD 模型的"时间优先性压过 blocking"预测，后由 Kehoe, Schreurs & Graham (1987) 在兔瞬膜制备上实验证实（L6331）。**图 14.4** 是三种刺激表示下 US 预测的时间进程（US 在第 25 步，$\alpha=.05,\lambda=.95,\gamma=.97$，L6347）。

## 5. 它的实验条件（拓扑/规模/负载；训练与评估是否同一套）

- **TD-Gammon**：训练与评估分离——自对弈训练，评估是对人类/其他程序；表 16.1 逐版本给出隐藏单元数与训练局数，评估对手与比分单列（L7002）。后版本加选择性 2-ply/3-ply 搜索，搜索**只影响着法选择，学习过程不变**（L6998）。
- **Samuel 跳棋**（L7004–7026）：lookahead 搜索 + 线性"scoring polynomial"；rote learning 存局面→回传值；generalization learning 每步都更新，目标是从第二个 on-move 局面发起搜索的 minimax 值。**无显式奖励**，改把"棋子优势"特征权重固定（L7015）。1967 版用 alpha-beta、book learning、signature tables（L7026）。作者自述：generalization 版"better-than-average"、"tricky but beatable"，中局强但开局与残局弱（L7026）。
- **Watson**：训练用三类人类对手模型（全部约 30 万条线索的粉丝档案），评估用同样的模型 + 实际比赛；**训练与评估不是同一套**——学习用模型仿真，落地是真实直播对局（L7049–7053）。时间约束：只有几秒做下注/选题/抢答（L7055）。
- **RL 内存控制器**：全部由**仿真**完成（未被流片），4GHz 4 核配置，9 个访存密集型并行负载；训练与评估同属仿真环境，但做了"在线学习 vs 学好后冻结"的对照（L7090–7094）。
- **DQN**：49 游戏各自独立训练（权重重置），但**超参与架构完全共享**；每局评估 30 次、每次最长 5 分钟、从随机初始状态开始；人类测试者经 2 小时练习后每游戏约 20 局（关声音以免不公平）（L7134）。训练与评估都是同一模拟器。
- **AlphaGo**：SL 训练约 3 周、50 个处理器上的分布式随机梯度上升（L7198）；RL 策略网络用 50 个处理器并行自对弈、**一天训练一百万局**（L7198）；全部网络在实战前训练完毕并在实战中冻结（L7197）。
- **14/15 章**：条件反射实验是兔瞬膜/猴/鼠/果蝇等动物实验，与 RL 仿真对照，两套"数据"性质不同（L6290–6368、L6635–6666）。

## 6. 它自己承认的局限（逐字引用）

- 策略梯度整体："Today they are less well understood in some respects, but a subject of excitement and ongoing research."（L6144）
- Rescorla–Wagner 与 TD 模型："it is far from being a perfect model. To generate other details of classical conditioning the model needs to be extended, perhaps by adding model-based elements and mechanisms for adaptively altering some of its parameters."（L6362）
- TD 模型对反应时序："The TD model does not include as part of its definition any mechanism for translating the time course of the US prediction … into a profile that can be compared with the properties of an animal's CR."（L6343）；presence 表示下"the TD model with the presence representation cannot recreate many features of CR timing"（L6349）。
- 强化程序（Skinner schedule）建模："Modeling results from experiments likes these using the reinforcement learning principles we present in this book is not well developed"（L6374）。
- 第15章自陈："we are not neuroscientists. We do not try to describe—or even to name—the very many brain structures and pathways, or any of the molecular mechanisms, believed to be involved in these processes."（L6550）以及"We also do not do justice to hypotheses and models that are alternatives"（L6550）。
- 多巴胺/TD 失配："there are situations, however, in which predictions based on the hypothesis do not match what is observed in experiments."（L6592）；早奖励情形："at the later time when the reward is expected but omitted, the TD error is negative whereas, in contrast to this prediction, dopamine neuron activity does not drop below baseline in the way the TD model predicts (Hollerman and Schultz, 1998). Something more complicated is going on in the animal's brain than simply TD learning with a CSC representation."（L6693）
- 多巴胺信号是否标量广播："modern evidence is pointing to the more complicated picture that different subpopulations of dopamine neurons respond to input differently"（L6630）；"the assumption that dopamine is released at all the corticostriatal synapses under the same conditions and at the same times is likely an oversimplification"（L6807）。
- actor–critic 神经假设："Although the actor–critic neural implementation illustrated in Figure 15.5b may be correct on some counts, it clearly needs to be refined, extended, and modified to qualify as a full-fledged model of the function of the phasic activity of dopamine neurons."（L6732）；"Results from experiments like these indicate that the actor–critic hypothesis described above is too simple in placing the actor in the dorsal striatum."（L6829）
- 模型基/模型自由是否可分："The evidence is not pointing to a positive answer to this last question."（L6839，引 Doll, Simon & Daw 2012 的"model-based influences appear ubiquitous more or less wherever the brain processes reward information"）
- 成瘾模型："Addictive behavior is much more complicated than this result from Redish's model, but the model's main idea may be a piece of the puzzle. Or the model might be misleading."（L6847）
- **RL 内存控制器**："This learning memory controller was never committed to physical hardware because of the large cost of fabrication."（L7094）
- **DQN**："DQN is not a complete solution to the problem of task-independent learning."（L7150）；"DQN's performance on some of the Atari 2600 games fell considerably short of human skill levels… The games most difficult for DQN—especially Montezuma's Revenge on which DQN learned to perform about as well as the random player—require deep planning beyond what DQN was designed to do."（L7150）
- **Samuel 跳棋**（作者转述 Samuel 的自陈）：值函数可能"consistent merely by giving a constant value to all positions"（L7019）；"it should have been possible for it to become worse with experience. In fact, Samuel reported observing this during extensive self-play training sessions."（L7021）
- **Watson**：自对弈不可用，因为"Watson was so different from any human contestant"、且"Jeopardy! is a game of imperfect information"（L7051）；"Making all the decisions via Monte-Carlo trials might have led to better wagering decisions, but this was simply impossible given the complexity of the game and the time constraints of live play."（L7055）
- 应用整体："Applications of reinforcement learning are still far from routine and typically require as much art as science."（L6934）

## 7. 它没做但看起来能做的地方

1. **RL 内存控制器只做了仿真**（L7094）。9 个负载、4 核配置足以支撑"在线学习优于固定策略 8%"的结论，但没有任何功耗/面积/时序收敛的实测；书中把后续（Mukundan & Martínez 2012：更多动作、能效准则、用遗传算法构造奖励函数）列为已发生，**没有做"负载突变/到达率突变下的适应速度"这类刻画**——而这恰是本批课题关心的量。可做的自然下一步：把"负载切换后性能恢复时间"作为显式指标测出来（本片未见到该指标）。
2. **动作合法集与学习状态特征被刻意分离**（L7088）：tile coding 输入来自 transaction queue，约束集 $\mathcal A(S_t)$ 来自硬件时序。书中称之为保证物理安全的技巧，但没有研究"约束收紧/放松时策略迁移"。
3. **DQN 的超参是"informal searches"在小部分游戏上定的**（L7126），然后固定到全部 49 个游戏；没有做超参迁移/自适应。所有 49 个游戏仍共享"视频帧"这一模态，作者自己说这是选择卷积网的自然理由（L7150）。
4. **值网络训练的两段式（先策略梯度训 RL policy，再 MC policy evaluation 训价值网）**（L7197）替代了 TD-Gammon 式的纯 TD(λ) 自对弈，书中只说后者"held more promise"，未给对照实验。
5. **Daw–Niv–Dayan 的模型自由/模型基仲裁机制**只说"以置信度择信"（L6460–6466），**书中没有给出该仲裁的可运行算法形式**；这是第14章到算法层的一个明显缺口。
6. **团队问题（15.10）的两个必要条件是"contingent eligibility + 各自探索"**（L6811–6821），且"the relationship between a single team member's action and changes in the team's reward signal is a statistical correlation that has to be estimated over many trials"（L6813）——即收敛速度与团队规模的关系未处理，而 Williams (1992) 只证明了梯度上升方向正确。
7. **奖励信号的"标量单值"假设**被作者自己指出与生物系统不符："using a single number as a reward or a penalty signal, depending only on its sign, is at odds with the fact that animals' appetitive and aversive systems have qualitatively different properties"（L6535）——作者明确说这是"a direction in which the reinforcement learning framework might be developed in the future"，未做。

## 8. 和同批其他篇的关系

本片是教材章节，**无法核对同批其他篇是否引用它**（我未读到同批材料，不越界）。只能标注本片自身引用/依赖的关键源文献，供主控做交叉比对：

- 策略梯度与 actor–critic 源流：Williams (1987, 1992)、Barto, Sutton & Anderson (1983)、Sutton, McAllester, Singh & Mansour (2000)、Marbach & Tsitsiklis (1998, 2001)、Degris, White & Sutton (2012)（L6144–6150）。
- 心理学线：Rescorla & Wagner (1972)、Kamin (1968/1969)、Pavlov (1927)、Thorndike (1898)、Skinner (1938/1958)、Hull (1943)、Tolman (1948)、Adams & Dickinson (1981)、Adams (1982)、Daw, Niv & Dayan (2005)（L6488–6537）。
- 神经科学线：Montague, Dayan & Sejnowski (1996)、Schultz, Dayan & Montague (1997)、Schultz et al. (1993)、Tsai et al. (2009)、Steinberg et al. (2013)、Yagishita et al. (2014)、Klopf (1972, 1982)（L6875–6928）。
- 应用线：Tesauro (1992/1994/1995/2002)、Samuel (1959, 1967)、Ipek et al. (2008)、Mnih et al. (2013, 2015)、Silver et al. (2016, 2017a)（L7003、L7026、L7096、L7152、L7200）。
- 与本片最"像"的同批对象（如果本批含深度 RL / 调度类论文）：16.4（RL 做调度器）与 16.5/16.6（深度 RL 做决策）最可能被同批论文引用为"经典 RL 落地"背景。
- 与本片最"不像"的：第14章是纯心理学对照，不含任何网络/调度/负载指标。

## 9. 对"负载变化下到达率/时延"这件事，本片贡献的事实

**直接贡献只有一处：16.4（L7059–7096）。** 具体：

- 该工作是**明确以"动态变化的请求模式"为问题设定**的：控制器要"deal with dynamically changing patterns of read/write requests while adhering to a large number of timing and resource constraints"（L7054），状态就是 transaction queue 的内容（到达队列），性能指标是**平均访存时延与吞吐**（L7068–7070）。
- 奖励设计本质是"吞吐型"：只有 read/write 走外部数据总线，只有它们给 +1；precharge/activate 虽无即时奖励，却是未来拿到奖励的必要前置（L7081）。这一点对"时延 vs 吞吐"的权衡有直接借鉴意义：**把时延/资源占用编码成动作约束，而不是编码进奖励**（L7075–7079），作者称这使探索被限制在"safe region"。
- 量化：RL 相对 FR-FCFS 提升 7%–33%，几何平均 19%；相对上界缩小 27% 差距；在线学习比固定策略平均好 8%（L7090–7094）。**"在线学习优于固定策略 8%"是本片对"负载变化"这一议题最硬的一个数字。**
- 但本片**没有给出任何"负载切换后多快恢复/多快适应"的时间尺度数字**，也没有到达率（request arrival rate）作为自变量的曲线；9 个负载是固定的 benchmark，不是变负载（L7090）。若要用于"负载变化下的到达率/时延"，只能引用其奖励/约束设计范式与 8%/19% 这两个量级，不能引用其适应速度。

**间接相关：**
- 16.3 Watson 展示了**硬实时约束下的决策**（几秒内完成下注/抢答，L7055），并给出"用 ANN 快速估值 → 残局改用 Monte-Carlo 平均"的两级时延–精度折中（L7055）。
- 16.1 TD-Gammon 的 5–10 秒/步思考时间与 4–6 倍错误率改进（trajectory sampling，L7000）是"计算预算 ↔ 决策质量"的另一组数据点。
- 第14、15 章对负载/到达率/时延**没有直接贡献**（这两章的对象是动物行为与神经信号）。

## 10. 一句话评价

本片在方法谱系中的位置是"**整合与外推，而非新方法**"：第13章末把策略梯度的连续动作与 continuing 情形补齐（L6001–6151），第14/15章把已有算法当作**解释性框架**去对齐心理学与神经科学（Rescorla–Wagner≈LMS、TD≈多巴胺、actor–critic≈背侧/腹侧纹状体），第16章则给出六个"算法不改、靠表征与工程细节取胜"的案例；其中 16.4 的 RL 调度器是本片对"负载变化 / 到达率 / 时延"唯一可引用的直接证据（19% 平均提升、在线学习 +8%），其余应用（TD-Gammon、DQN、AlphaGo）贡献的是"表征与搜索如何替代人工特征"这一条方法论结论。

---

## 本片要点（供主控合并）

1. **16.4 RL 内存控制器是本片唯一直接命中"负载变化/时延/吞吐"的案例**（L7059–7096）：状态=访存请求队列，动作={precharge, activate, read, write, NoOp}，奖励=read/write 记 1 否则 0；用 Sarsa + tile coding（32 tilings × 256 值）+ ε=0.05；**RL 相对 FR-FCFS 提升 7%–33%（几何平均 +19%），把与不可实现上界 Optimistic 的差距缩小 27%，在线学习比固定策略平均好 8%**（L7090–7094）。**局限：从未流片，纯仿真；无负载切换适应速度指标**（L7094）。
2. **"动作合法集按物理约束预定义、学习只在安全区进行"是 16.4 的关键工程范式**（L7075–7079）：约束集 $\mathcal A(S_t)$ 与函数逼近输入特征**刻意分离**，使探索不会危及硬件。这一条可直接迁移到任何有硬时序约束的调度/接入问题。
3. **第13章末补齐了 continuing 情形**（L6001–6068）：性能定义为平均奖励率 $r(\pi)$，返回值改为微分回报 $G_t=R_{t+1}-r(\pi)+\cdots$（13.17），在此定义下策略梯度定理形式不变并给出完整证明；给出带资格迹的 actor–critic continuing 伪代码（$\bar R$ 为奖励率估计，L6022–6037）。这是全书唯一显式处理"无回合边界、持续运行"的算法形式。
4. **第15章建立了"奖励信号 $R_t$ ≠ 强化信号 $\delta_t$"这一区分**（L6570–6585、L6688–6693）：TD 误差 $\delta_{t-1}=R_t+\gamma V(S_t)-V(S_{t-1})$ 才是驱动学习的标量；多巴胺神经元的相位放电对应 $\delta$ 而非 $R$；其标志性现象是**预测的奖励被省略时放电跌到基线以下**（图 15.3/15.4，L6669）。已知失配：奖励提前到达时 TD 会预测负误差而多巴胺不下跌（L6693）。
5. **第16章的三条可引用量化结论**：① TD-Gammon 3.0 对世界冠军级人类 +6 分/20 局，且改变了人类顶尖选手的开局下法（L7002–L7004）；② DQN 用同一套超参在 49 个 Atari 游戏中的 29 个（46 个有对照的游戏中）达到或超过人类水平，消融显示 experience replay 与目标网络合用提升"very dramatically"（L7134、L7150）；③ AlphaGo 的 SL 策略网络专家着法预测准确率 57%（当时最好 44.4%），RL 策略网络对 SL 胜率 >80%、对 10 万局/步的 MCTS 程序胜率 85%（L7198）。
