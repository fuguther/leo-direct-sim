# LJG6ZW7B 分片 part7（覆盖行号区间 L7201–L8400）

> 篇目：Sutton & Barto, *Reinforcement Learning: An Introduction* (2nd ed.)，全文 9596 行。
> 本片为第 16 章末（16.6.1 收尾 / 16.6.2 / 16.7 / 16.8）＋第 17 章 "Frontiers" 全章（17.1–17.6 及 Bibliographical and Historical Remarks）＋全书参考文献 A–M（L7569–L8400）。
> 覆盖声明：L7201–L8400 共 1200 行**逐字读完**，无跳读、无关键词检索、无越界。

---

## 1. 一句话
本片是这本 RL 教材的收尾段：先用四个应用（AlphaGo 组件消融、AlphaGo Zero、Adobe 广告投放策略、热气流滑翔）把前面所有方法落到真实系统上，再用第 17 章 "Frontiers" 把全书从"解一个给定的 MDP"推进到"连状态表示和奖励信号都得自己造"，最后 830 行是参考文献（L7569–L8400）。

## 2. 问题设定
主体问题是：**前面 16 章的方法在什么条件下不够用**。
- 应用侧的麻烦（L7201–L7310）：① 围棋的搜索/评估如何组合（价值网络 vs rollout，L7208）；② 不给人类数据能不能学到超人水平（L7214）；③ 推荐/广告场景里"点击稀疏、回报高方差"且新策略不能直接上线试（L7249、L7251）；④ 滑翔场景里"奖励信号怎么设计才学得出来"（L7289）。
- 理论侧的问题（L7312–L7533）：强化学习的标准假设（状态已知且固定、奖励由设计者给定、环境模型已知、任务由人设定）在通向通用人工智能时都站不住。
- 谁遇到麻烦：**应用者**（奖励设计反复试错，L7467）、**研究者**（options 的 off-policy＋函数逼近组合没人做过，L7543）、**部署方**（学习过程中的行为本身就有风险，L7531）。

## 3. 方法骨架
本片没有提出新算法，主干是"逐节推进的开放问题清单＋四个案例的方法细节"：
- **16.6.1 AlphaGo（收尾）**：价值网络结构同 SL/RL 策略网但单输出单元，多一个"当前执子颜色"二值特征；用 RL 策略自对弈数据做蒙特卡洛策略评估训练；30M 局面（每局随机取一个）、50M 个 32 样本的 mini-batch、50 GPU 训一周（L7202）。rollout 策略是线性网络，从 800 万人类棋谱监督学习，约 1000 局完整模拟/秒/线程（L7204）。APV-MCTS 展开阶段用 SL 策略而非 RL 策略；价值函数则相反用 RL 策略派生的更好（L7206）。混合系数 η（式 16.4）：η=0 只用价值网络，η=1 只用 rollout（L7208）。
- **16.6.2 AlphaGo Zero**：自对弈 RL，除规则外**不用人类数据/特征**，输入是棋盘的"raw"表示；实现的是策略迭代（策略评估＋策略改进交替）（L7214）。与 AlphaGo 的关键差别：**自对弈学习全程都用 MCTS 选子**（AlphaGo 只在实战用 MCTS）、只用 1 个深度卷积网、MCTS 更简单（L7214）。MCTS 不含完整对局 rollout，模拟止于当前搜索树的叶节点而非终局，因此不需要 rollout 策略（L7216）。网络 $f_\theta$ 输入棋盘原始表示，输出两部分：标量 v（当前执子方获胜概率估计）＋动作概率向量 p（每个落子点＋pass/resign）（L7216）。**不按 p 直接选子**，而是用 p 与 v 指导 MCTS，MCTS 返回新的策略 $\pi_i$；原文引用 "MCTS may therefore be viewed as a powerful policy improvement operator"（L7218）。网络输入 $19\times19\times17$ 的二值特征堆叠（当前方/对手各 8 个历史平面＋1 个颜色平面），因为围棋有禁重复和贴目，当前盘面不是马尔可夫状态（L7223）。网络"双头"：一头 362 输出（$19^2+1$ 走子概率），一头 1 输出（标量 v）；分裂前 41 个卷积层＋批量归一化＋残差跳连，走子概率与价值分别经 43、44 层算出（L7225）。随机初始化，带动量/正则/递减步长的 SGD，样本均匀取自最近 500,000 局自对弈；输出 p 加噪声促探索；每 1000 步做一次 checkpoint，用最新网络策略对当前最优策略模拟 400 局（每步 1600 次 MCTS 迭代），胜出（含噪声抑制的边际）才成为新的 best policy；网络权重被更新去逼近 MCTS 返回的策略和"当前最优策略获胜概率"（L7227）。规模：4.9M 局自对弈约 3 天，每步 MCTS 1600 迭代约 0.4 秒，权重更新 700,000 个 batch × 2,048 盘面（L7229）。
- **16.7 个性化 Web 服务**：A/B 测试 = 非联想的两臂老虎机，不个性化（L7243）；加用户/内容特征后形式化为 contextual bandit（L7243）。Theocharous, Thomas, Ghavamzadeh (2015) 把它形式化为 **MDP**，目标是最大化用户多次访问的累计点击；贪心策略把每次访问当作从总体中均匀抽出的新访客，因此不利用长期交互（L7245）。两种算法对比：greedy optimization（随机森林估点击概率＋ε-greedy，L7255）与 **LTV optimization**（批次式 RL：fitted Q iteration，FQI，是 fitted value iteration 适配 Q-learning 的变体，L7257）。**关键技术约束**：新策略不能直接上线（风险），必须用**离线策略评估（off-policy evaluation）**在旧策略收集的数据上高置信地估计新策略表现（L7249）。
- **16.8 热气流滑翔**：Reddy, Celani, Sejnowski, Vergassola (2016, PNAS) 把滑翔建成带折扣的持续 MDP；环境是 1 km 边长的三维立方体（一面为地面），用含速度/温度/压力的偏微分方程模拟，加小随机扰动即产生热气流与湍流；滑翔机用速度/升力/阻力等气动方程建模（L7280）。动作：把当前**倾侧角（bank angle）±5°**、**攻角（angle of attack）±2.5°**，或保持不变 → $3^2=9$ 个动作；倾侧角限制在 $-15°\sim+15°$（L7285）。状态：先做状态聚合（Section 9.3），四维（局部垂直风速、局部垂直风加速度、左右翼垂直风速差得到的 torque、局部温度），每维离散成 3 个 bin（正高/负高/小）（L7287）。学习：**一步 Sarsa**，softmax 选动作，动作偏好由近似动作值归一化到 [0,1] 后除以温度参数 τ 得到（L7291、L7294）；τ 从 2.0 递减到 0.2，步长 0.1，折扣 0.98（L7297）。每回合 2.5 分钟模拟、1 秒步长，几百回合后收敛（L7299）。
- **第 17 章（六个小节，都是"把假设拿掉"）**：
  - **17.1 GVF 与辅助任务**：把价值函数里的"奖励"推广成任意信号——cumulant $C_t$，得 GVF $v_{\pi,\gamma,C}(s)$（式 17.1，L7320、L7323）；不需要与奖励有任何联系，或许该叫 forecast（Ring, in preparation，L7326）。辅助任务有用的三条理由：共享表示（多头网络 + 共享 body，Jaderberg et al. 2017，L7332）、类比经典条件反射的"内置反射"（预测学出来、预测到动作的连接是设计死的，如预测到撞车就刹车，L7334）、以及最重要的一条——用来**拿掉"状态表示固定且给定"这一全书假设**（L7336）。
  - **17.2 Options 时间抽象**：option = 策略 π + 状态相关终止函数，可与低层动作互换；action-value 自然推广为 option-value，策略推广为分层策略；最简情况下学习只在 option 终止时更新，更精细的 intra-option 学习**一般需要 off-policy**（L7346）。option model 分两部分：奖励部分 $r(s,\omega)$（式 17.2，L7351）与状态转移部分 $p(s'|s,\omega)$（式 17.3，L7357）——注意后者带 $\gamma^k$ 因子，**已不再是转移概率、不对 $s'$ 求和为 1**（L7360）。分层策略的 Bellman 方程（式 17.4，L7365）；带 options 的值迭代（L7371）。只考虑部分 option 集合时会收敛到受限集合下的最优分层策略：次优但**收敛快得多**，因为考虑的 option 少、且每个 option 能跳过很多时间步（L7374）。option model 可以表述成一组 GVF 再用本书方法学（L7376）。练习 17.1 要求给出平均奖励设定下的对应形式（L7378）。
  - **17.3 观测与状态**：本书一直把近似价值函数写成环境状态的函数，这是大限制；参数化函数逼近其实**已经隐含地包含**了部分可观测的一部分（不可观测的状态变量，只要参数化让近似值不依赖它即可）（L7384）。四个步骤：① 环境只发观测不发状态，交互序列退化为 $A_0,O_1,A_1,O_2,\dots$（L7388、L7391）；② 从观测-动作序列里恢复"状态"概念：history $H_t \doteq A_0,O_1,\dots,A_{t-1},O_t$，状态必须是 history 的函数 $S_t=f(H_t)$，保持全部信息者称 Markov state（L7396）。用 test $\tau=a_1o_1a_2o_2\dots$ 与 $p(\tau|h)$（式 17.5，L7401）形式化：$f(h)=f(h')\Rightarrow p(\tau|h)=p(\tau|h')$（式 17.6，L7407）；Markov 状态足以确定任何预测（含任何 GVF），也足以最优决策（L7410）；③ 计算可行性：要紧凑、要能增量递归更新 $S_{t+1}\doteq u(S_t,A_t,O_{t+1})$（式 17.7，L7415），u 称 state-update function（L7418）；Figure 17.1 给出含 model / planner / state-update function 的智能体架构图（L7421）。**关键事实**：若 f 可增量更新，则 f 是 Markov 的**当且仅当**所有"一步 test"能被准确预测（式 17.8，L7426），即只需准确的一步预测（L7423）。POMDP 的 belief state $\mathbf{s}_t[i]\doteq\Pr\{X_t=i|H_t\}$（式 17.9，L7433）与其 Bayes 更新（式 17.10，L7440）；PSR 与 OOM（L7445）；④ 重新引入近似：最简单是 $S_t\doteq O_t$，更好是最近 k 步观测与动作的 k 阶历史（L7449）。
  - **17.4 奖励信号设计**：RL 相对监督学习的最大优势是不需要"正确答案"信息，但成败强依赖奖励信号是否框住了设计者的目标（L7459）。稀疏奖励问题（L7465）；实践中常是"设计者反复试错调奖励"（L7467）。**反直觉但重要**：给子目标加补充奖励可能让 agent 偏离总目标；更好的做法是**不动奖励信号，而是给价值函数一个初始猜测** $\hat v(s,\mathbf w)\doteq\mathbf w^\top\mathbf x(s)+v_0(s)$（式 17.11，L7472），但"并不保证总能加速学习"（L7475）。shaping（Skinner）（L7477）、模仿/示教/学徒学习与逆强化学习（Ng & Russell 2000）（L7479）、把奖励信号当作超参数自动搜索（双层优化，Sorg/Lewis/Singh，L7481、L7483）、"agent 的目标不应当总是等于设计者的目标"（L7485）、奖励信号可以依赖智能体内部状态（动机、记忆、甚至幻觉）（L7487）。
  - **17.5 遗留问题（六个）**：① 需要能真正在线增量的参数化函数逼近——现有深度学习方法只适合大批量离线训练，**"An honest assessment has to be that current deep learning methods are not well suited to online learning."**（L7493）；② 表示学习/meta-learning（L7495）；③ 用**学到的**环境模型做可扩展规划（几乎没人做成）（L7497、L7499）；④ 自动选择任务（含自动设计 GVF 的 cumulant/策略/终止函数）（L7501、L7503）；⑤ 好奇心/内在奖励驱动行为与学习的交互（L7505）；⑥ 把 RL agent 嵌入物理世界的安全性（L7507）。
  - **17.6 RL 与 AI 的未来**：模拟器提供安全环境与海量数据（L7521）；真实世界嵌入才可能释放全部潜力（L7523）；优化本身的双刃剑——《魔法师的学徒》与 Wiener 引用的《猴爪》"it grants what you ask for, not what you should have asked for or what you intend"（L7527）；与控制工程的风险管理类比（L7531）；收尾引 Herbert Simon 的 Prometheus/Pandora 与"我们是未来的设计者而非旁观者"（L7519、L7533）。
- **参考文献（L7569–L8400）**：按字母序 A（Abbeel）到 M（McMahan），约 830 条，条目本身不承载论证。

## 4. 它声称的效果（含基线与条件）
- **AlphaGo 组件消融（L7208）**：仅用价值网络（η=0）的 AlphaGo 已胜过纯 rollout 版（η=1），并胜过当时最强的其他围棋程序；**最好成绩出现在 η=0.5**，说明价值网络与 rollout 互补。
- **SL vs RL 策略（L7206）**：对**人类**对手，展开阶段用 SL 策略更好；而价值函数用 RL 策略派生的更好——同一个 RL 策略在两处一优一劣。
- **AlphaGo Zero（L7229）**：Elo —— Zero 4308、胜 Fan Hui 的 AlphaGo 3144、胜 Lee Sedol 的 AlphaGo 3739；在与击败 Lee Sedol 的完全同条件 100 局比赛中 **100:0** 全胜。
- **与监督学习基线对比（L7231）**：用同架构网络在近 3000 万局面（16 万局）上监督学习预测人类走子，该选手**初期**比 AlphaGo Zero 强、更会预测人类专家走子，但 Zero 训练一天后就被反超。
- **AlphaGo Zero 大版本（L7233）**：2900 万局自对弈、约 40 天，Elo **5185**；对 AlphaGo Master（Elo 4858，曾 60:0 击败最强人类职业选手）**89:11**。
- **AlphaZero（L7237）**：Silver et al. (2017b)，连围棋知识都不需要，通用 RL 算法，在围棋/国际象棋/将棋上超越当时最好的程序。
- **个性化推荐（L7243）**：Li, Chu, Langford, Schapire (2010) 的 contextual bandit 在 Yahoo! Front Page Today（当时互联网访问量最大的页面之一）上，以 CTR 为目标，**比标准非联想 bandit 提升 12.5%**。
- **CTR vs LTV（L7269、L7274）**：Figure 16.8 的例子中同一批访问序列 CTR=0.35 而 LTV=1.5（因为 LTV 只按访客数作分母）。**实测结果：greedy optimization 在 CTR 指标上最好，LTV optimization 在 LTV 指标上最好**——即两个指标互不相容；高置信离线策略评估给出了"LTV 方法将以高概率产出优于当前已部署策略"的概率保证；Adobe 于 2016 年宣布 LTV 算法成为 Adobe Marketing Cloud 的标准组件。
- **热气流滑翔（L7299、L7301、L7306）**：性能在不同模拟气流时段上波动很大，但**触地次数随学习推进稳定降到近零**；特征消融结果：只用"垂直风加速度 + torque"最好，垂直风速只反映热气流强度但无助于留在气流内，温度信息帮助很小，控制攻角对留在热气流内无益（用于热气流之间的长途滑翔更有用）；不同湍流强度下学到的策略不同（强湍流偏好小倾侧角、弱湍流偏好猛转），作者建议以"垂直风加速度越过某阈值"作为切换策略的判据。**基线：学前的随机策略**（L7299 左图轨迹迅速掉高度）。
- **奖励信号对照（L7289）**：以"回合结束时按净升高给奖励 + 触地给大负奖励 + 其余为 0"这个直观奖励，在真实回合时长下**学习失败**，且 **eligibility trace 也没帮上忙**；最终有效的是**每步对上一时刻垂直风速与垂直风加速度的线性组合**。

## 5. 它的实验条件
- **AlphaGo / AlphaGo Zero**：全是自对弈与程序间对局，评估用的是 **Elo 差**与固定局数的比赛（100 局，L7229、L7233）。训练与评估不是同一套：训练用自对弈（Zero 是最近 50 万局，L7227），评估是 checkpoint 时对 current best policy 模拟 400 局（L7227）以及最终锦标赛。硬件/时长明确：AlphaGo 价值网络 50 GPU 一周（L7202）；Zero 4.9M 局 3 天、每步 0.4 s（L7229）；大版本 29M 局约 40 天（L7233）。
- **个性化推荐（L7253）**：**真实银行业数据**，两个数据集——A 银行一个月约 200,000 次交互、7 种 offer 随机分配；B 银行 4,000,000 次交互、12 种 offer。特征含距上次访问时间、累计访问次数、上次点击时间、地理位置、兴趣类别、人口统计特征。点击奖励 1、否则 0。测试集是"由随机策略服务的真实银行网站交互"，用高置信离线策略评估，**新策略并未真正上线**（L7249、L7274）。
- **热气流滑翔（L7280、L7299）**：仿真环境（PDE 气流 + 气动方程），1 km 立方体；每回合独立生成一段湍流时段，2.5 分钟模拟、1 秒步长；从弱到强湍流都训过（L7306）。每个 episode 的气流独立生成——即**训练与评估用的是同族但不同的随机实现**（L7299）。
- 第 17 章无实验（纯论述与练习）。

## 6. 它自己承认的局限（逐字引用）
- POMDP（L7443）："This approach is popular in theoretical work and has many significant applications, but **its assumptions and computational complexity scale poorly, and we do not recommend it as an approach to artificial intelligence.**"
- 近似状态的长期预测（L7451）："Unfortunately, **long-term prediction performance can degrade dramatically when one-step predictions become even slightly inaccurate.** Longer-term tests, GVFs, and state-update functions may or may not approximate better. The short-term and long-term approximation objectives are just different, and **there are no useful theoretical guarantees at present.**"
- 值函数初始猜测（L7475）："This initialization can also be done for arbitrary nonlinear approximators and arbitrary forms of $v_0$, **though it is not guaranteed to always accelerate learning.**"
- 深度学习与在线学习（L7493）："**An honest assessment has to be that current deep learning methods are not well suited to online learning.** We see no reason that this limitation is insurmountable, but algorithms that address it, while at the same time retaining the advantages of deep learning, have not yet been devised."
- 表示学习（L7495）："This is an old problem, dating back to the origins of artificial intelligence and pattern recognition in the 1950s and 1960s. **Such age should give one pause. Perhaps there is no solution.**"
- 用学到的模型规划（L7497）："Planning methods have proven extremely effective in applications such as AlphaGo Zero and computer chess in which the model of the environment is known... But cases of **full model-based reinforcement learning, in which the environment model is learned from data and then used for planning, are rare.**"
- options 的早期工作（L7543）："**An important limitation of these early works is that they did not treat the off-policy case with function approximation.** Intra-option learning in general requires off-policy learning, which could not be done reliably with function approximation at that time."
- 用 GVF 实现 option model（L7545）："**Using GVFs to implement option models has not previously been described.**"
- options 的平均奖励推广（L7549）："**The extension of options and option models to the average-reward setting has not yet been developed in the literature.**"
- 逆强化学习（L7479）："Unfortunately, strong assumptions are required, including knowledge of the environment's dynamics and of the feature vectors in which the reward signal is linear. The method also requires completely solving the problem (e.g., by dynamic programming methods) multiple times."
- 奖励设计的经验性（L7467）："In practice, designing a reward signal is often left to an **informal trial-and-error search** for a signal that produces acceptable results."
- 热气流滑翔（L7299）："Although Reddy et al. found that **performance varied widely over different simulated periods of air flow**, the number of times the glider touched the ground consistently decreased to nearly zero as learning progressed."（本片内对滑翔实验最接近"自述局限"的一句；未见作者对奖励信号设计失败给出理论解释。）

## 7. 它没做但看起来能做的地方（基于本片内容）
1. **options × off-policy × 函数逼近的组合**：教材明说三者合起来"had not been significantly explored"（L7543），且 intra-option 学习一般需要 off-policy（L7346）——现在（本书写作时）有稳定的 off-policy 方法了（L7543）。这是直接可做的空缺。
2. **options/option model 的平均奖励版**：Exercise 17.1 已经把问题问出来了，正文说文献里没有（L7378、L7549）。平均奖励正是"长期运行、不设折扣"的工程场景（如持续运行的系统），折扣不适用（L7378 引 Section 10.4 的观点）。
3. **用 GVF 实现 option model**：教材自称这是它首次这样表述（L7545），并用 Modayil/White/Sutton (2014) 的"预测策略终止时的信号"技巧（L7545）；但"用 GVF 学 option model 在函数逼近下是否稳定"未见实验。
4. **自动化奖励/任务设计**：GVF 的 cumulant、策略、终止函数目前全靠人工选（L7503）；双层优化（进化在上一层、RL 在下层）只有少量计算实验（L7481、L7483），且结论是"直觉不足以设计出好奖励"（L7483）。
5. **稀疏奖励的方向性结论**：教材主张"改初始值函数而不是改奖励"（L7472、L7477），但没有给出何时初始化有效的判据（"not guaranteed to always accelerate learning"，L7475）——这是一个可被实验回答的问题。
6. **选择性模型学习**：为了让"用学到的模型规划"可行，模型学习必须是选择性的（L7499）；"如何选"在正文被截断，未见具体准则。
7. **案例里未被探索的评估维度**：AlphaGo/Zero 全部用 Elo 与对局胜负评估，**没有报告任何计算/时延-精度权衡曲线**（唯一的时间数字是 L7229 的 0.4 s/步与 L7204 的 1000 局模拟/秒）；推荐案例只报 CTR/LTV 两个比值，未报策略切换成本或响应时延（L7262、L7266、L7274）。把"单位时间的决策数"当作与 Elo 并列的评估轴，是这篇天然没做但从内容上接得上的下一步。

## 8. 和同批其他篇的关系
- 本片只有教材本体与参考文献，**看不到同批其他篇的卡片**，因此无法点名"像谁/不像谁"，也未发现对本批其他篇的引用（本片范围内引用全部是外部文献）。
- 从内容接口看，若同批里有"用 bandit/RL 做自适应选择（路由、切换、资源分配）"的工作，其直接祖先是本片 **16.7 的 contextual bandit 与 LTV/off-policy 评估**（L7243、L7245、L7249、L7257）；若同批里有"奖励塑形/多目标权衡"的工作，接口是本片 **17.4**（L7465–L7487）；若同批里有"部分可观测/用有限观测窗口近似状态"的工作，接口是本片 **17.3** 的 k 阶历史与 state-update function（L7449、L7418）。
- 与典型"网络仿真+优化"论文的结构差异：本片是**教科书式的开放问题清单**，不提供可复现实验设定与基线代码；除 16.7 的真实银行数据外，其余案例都是仿真或游戏。

## 9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实
**没有直接贡献**——本片不涉及任何网络/排队/负载模型，没有到达率、时延、丢包的任何测量或公式（本片全部 1200 行中未出现此类实验）。可迁移的间接事实有四条：
1. **优化指标互不相容是实测过的**：同一份数据上，"点击率"与"按访客的长期价值"两个指标的最优策略不是同一个，贪心方法在 CTR 上赢、LTV 方法在 LTV 上赢（L7274）。对应到"吞吐/时延"这类指标对，提示**多指标必须分别报告，不能用一个代理指标宣称全面更优**。
2. **离线评估是上线前的硬约束**：因为新策略可能表现很差，必须在旧策略数据上做高置信的 off-policy 评估才敢部署（L7249、L7274）。这与"新调度策略不能直接打到生产网络"是同构的约束。
3. **奖励信号不能随便加子目标**：给中间目标加奖励可能让策略偏离总目标，"A better way ... is to leave the reward signal alone and instead augment the value-function approximation with an initial guess"（L7477、L7472）。对应"不要为了让时延数字好看而给中间 KPI 加权"。
4. **部分可观测下用最近 k 步观测近似状态**（L7449）以及"一步预测不准会显著毁掉长期预测"（L7451），是"用最近 k 个到达/队列样本做决策"这类做法的标准表述与其风险提示；且 17.3 指出短期与长期逼近目标是**不同**的目标（L7451）。
5. （安全侧）学习**过程中的**行为也必须安全，不能只看收敛后的策略（L7531）。

## 10. 一句话评价
本片是这本教材的"收尾与开放问题清单"：把全书方法谱系从"解给定 MDP"推到"连状态和奖励都要学"，用 AlphaGo Zero（MCTS 作为策略改进算子）和 Adobe 广告（离线策略评估才敢上线）两个案例示范，**没有提出新算法**；其价值主要在它明确点名的缺口（options 的平均奖励版、GVF 版 option model、off-policy＋options＋函数逼近的三合一、学到的模型做规划、在线增量深度学习）——这是一份可直接当选题清单用的、由领域奠基者自己写的 gap 列表。

---

## 本片要点（供主控合并）
1. **AlphaGo Zero 的结构性差别 + 成绩**（L7214、L7216、L7229、L7233）：不用任何人类数据/特征、只 1 个双头卷积网（41 层＋BN＋残差，$19\times19\times17$ 输入，L7223、L7225）、**自对弈学习全程用 MCTS**（AlphaGo 只在实战用），MCTS 不含完整 rollout。4.9M 局自对弈约 3 天 → Elo 4308，对击败 Lee Sedol 版 AlphaGo **100:0**；大版本 29M 局/约 40 天 → Elo **5185**，对 AlphaGo Master（4858）**89:11**。
2. **AlphaGo 组件消融的反直觉事实**（L7206、L7208）：展开阶段用**较弱**的 SL 策略对人类对手反而更强，而价值函数用 RL 策略派生的更好；只用一个组件时，**仅价值网络（η=0）已胜过纯 rollout 版并胜过当时最强其他围棋程序**，但最优是 η=0.5——两组件互补。
3. **教材自陈的未解决问题清单（可直接当选题缺口）**（L7549、L7545、L7543、L7497、L7493）：options/option model 的**平均奖励版文献中没有**；**用 GVF 实现 option model 此前无人描述**；option＋off-policy＋函数逼近的组合"had not been significantly explored"；**用学到的模型做规划极少成功**（Dyna 类工作多为表格模型）；"current deep learning methods are not well suited to online learning"。
4. **真实业务数据的双指标不相容 + 离线评估**（L7253、L7249、L7274）：Theocharous et al. (2015) 用真实银行数据（约 20 万次交互/7 offer 与 400 万次/12 offer），贪心优化在 **CTR** 上最好、LTV 优化在 **LTV** 上最好，**新策略未上线**而是用高置信离线策略评估给概率保证；Adobe 2016 年宣布 LTV 算法进入 Adobe Marketing Cloud。这是本片唯一的真实部署案例。
5. **一次完整的"奖励设计失败→改奖励"记录**（L7289、L7301、L7306）：热气流滑翔中，"回合末按净升高给奖励＋触地大负奖励"在真实回合时长下**学习失败且 eligibility trace 无效**；有效奖励是每步对上一时刻垂直风速与垂直加速度的线性组合；最佳特征集仅是"垂直风加速度 + torque"。同一任务在**不同湍流强度下学到不同策略**（强湍流保守小倾侧角、弱湍流猛转）。

> 附注（非要点，供主控判断数据可用性）：L7569–L8400 为参考文献，约 830 条；PDF→文本转换在多处把条目**从中间截断**（如 L7595、L7699、L7835、L7847、L7871、L7881、L7891、L7905、L7917、L8063、L8069、L8079、L8081、L8287、L8351、L8379），且 L7283/L7285/L7287（Figure 16.9 及正文）出现**双栏文字交织**。若后续要做引文抽取或按句引用，这几行不可直接采信。
