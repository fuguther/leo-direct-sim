# LJG6ZW7B 分片 part5（覆盖行号区间 L4801–L6000）

> 覆盖区间：**L4801–L6000（1200 行，全文 9596 行）**，逐行读完（8 次 `sed` 全量输出，未做关键词检索替代）。
> 本片内容 = Sutton & Barto《Reinforcement Learning: An Introduction》第 2 版：
> **第 11 章收尾**（§11.6 尾–§11.10 + 历史注记，L4801–5030）、
> **第 12 章 Eligibility Traces 全章**（L5032–5733）、
> **第 13 章 Policy Gradient Methods 开篇**（§13.1–§13.5，L5735–6000）。
> 文本形态说明：源文件是 OCR 转 markdown，公式块有相当比例损坏/错拼（如 L5325、L5805–5820 的推导块），凡影响理解的处已在下文单独标注「OCR 损坏」。

---

## 1. 一句话

本片是教材的**「离策略稳定性 → 资格迹 → 策略梯度」三连段**：先把离策略+函数逼近下的三类目标函数（VE/RE/BE）按「可否从数据学到」分成可学与不可学，推出 Gradient-TD（GTD2/TDC）与 Emphatic-TD 两条稳定化路线（L4801–5030）；再用整章把「前向视图 / 后向视图」的等价性展开成完整算法族——λ-return、TD(λ)、TTD(λ)、online λ-return、true online TD(λ)、Sarsa(λ)、TB(λ)、GTD(λ)/GQ(λ)/HTD(λ)/Emphatic TD(λ)（L5032–5733）；最后转入策略梯度，给出策略梯度定理、REINFORCE、带 baseline 的 REINFORCE、one-step actor–critic 与带资格迹的 actor–critic（L5735–6000）。

## 2. 问题设定

本片不是一个「问题—方法—实验」的单篇论文，而是**教科书在为一个具体理论困境收口，并开出新分支**。三段的「要解决的问题」分别是：

- **(a) 离策略学习的可用目标是什么（L4801–4994）**。背景：半梯度 TD 在离策略 + 函数逼近下会发散（deadly triad）。人们想改用「真 SGD 最小化 Bellman error（BE）」这条看起来最自然的路。本片要回答的是：**哪些目标函数是「可学的」（learnable）**——即其最优参数向量是否由可观测数据分布唯一决定。
- **(b) 怎么在不炸算力的前提下同时拿到 TD 的增量效率和 Monte Carlo 的长视野（L5032–5733）**。n-step 方法（第 7 章）已能做这个权衡，但它要么需要缓存最近 n 个特征向量，要么把更新推迟 n 步。资格迹要解决的是**用 d 维短期记忆向量 z_t 换掉「未来序列的存储」**，并回答一个更硬的问题：前向视图（forward view）与后向视图（backward view）在什么条件下**严格等价**、在什么条件下只是近似等价。
- **(c) 能不能不学动作值、直接学参数化策略（L5735–6000）**。已有方法几乎全是动作值方法，策略是「从动作值里派生出来的」，因此存在两个死结：ε-greedy 永远无法逼近确定性最优策略；动作值方法**没有自然办法表达「以特定概率随机化」才是最优**的策略（例 13.1 的 switched corridor 就是反例）。

## 3. 方法骨架

### 3.1 目标函数的可学性分类（L4801–4945）

- **VE（value error）**：$\overline{\mathrm{VE}}(\mathbf w)=\|\hat v_{\mathbf w}-v_\pi\|_\mu^2$。不可从数据学（两个不同 MRP 可有相同数据分布但不同 VE），但其**最优参数向量 w\*** 可学——因为另一个目标 **RE（return error）** $\overline{\mathrm{RE}}(\mathbf w)=\mathbb E[(G_t-\hat v(S_t,\mathbf w))^2]$ 与之只差一个与 w 无关的方差项：$\overline{\mathrm{RE}}(\mathbf w)=\overline{\mathrm{VE}}(\mathbf w)+\mathbb E[(G_t-v_\pi(S_t))^2]$（**L4806，(11.24)**）。RE 明显可观测 ⇒ RE 与 VE 同最优解 ⇒ w\* 可学（L4801–4809、Figure 11.4 左）。
- **BE（Bellman error）**：$\overline{\mathrm{BE}}$ 可在已知 MDP 时计算，**但既不可学、其最小解也不可学**。反例见 **Example 11.4（L4815–4836）**：一对 MRP，数据分布完全相同（都以 $2^{-k}$ 的概率出现 k 个 B），但 (i) 同一 w=0 在左 MRP 上 BE=0、在右 MRP 上 $\overline{\mathrm{BE}}=\mu(B)\cdot 1+\mu(B')\cdot 1=2/3$；(ii) 最小化 w 也不同（右 MRP 在 γ→1 时最优为 $(-\tfrac12,0)^\top$）。结论：**BE 不是数据的函数**，它把 BE 限制在 model-based 场景；residual-gradient 能做 BE 只是因为它被允许对**同一个底层状态**双重采样（L4837–4839）。
- **PBE / TDE 可学**：$\overline{\mathrm{PBE}}(\mathbf w)=\|\Pi\bar\delta_{\mathbf w}\|_\mu^2$ 及其梯度可由特征向量直接估计（L4840–4845、Figure 11.4 右）。

### 3.2 Gradient-TD：对 PBE 做真 SGD（L4840–4950）

推导主干：把 (11.22) 展开成矩阵形式（**L4853，(11.25)**、(11.26)），取梯度得三个期望之积（**L4883，(11.27)**）：

$$\nabla\overline{\mathrm{PBE}}(\mathbf w)=2\,\mathbb E[\rho_t(\gamma\mathbf x_{t+1}-\mathbf x_t)\mathbf x_t^\top]\,\mathbb E[\mathbf x_t\mathbf x_t^\top]^{-1}\,\mathbb E[\rho_t\delta_t\mathbf x_t]$$

三个因子的第一与第三**不独立**（都依赖 $\mathbf x_{t+1}$），直接采样相乘会有偏——这正是 residual-gradient 的病根。解法：**存后两个因子的乘积**，它是一个 d 维向量 $\mathbf v$：

$$\mathbf v\approx \mathbb E[\mathbf x_t\mathbf x_t^\top]^{-1}\mathbb E[\rho_t\delta_t\mathbf x_t] \quad(\text{L4893, (11.28)})$$

用 LMS 规则增量学 v（$O(d)$ 存储与每步计算）：$\mathbf v_{t+1}\doteq\mathbf v_t+\beta\rho_t(\delta_t-\mathbf v_t^\top\mathbf x_t)\mathbf x_t$（L4895–4899）。

- **GTD2**：$\mathbf w_{t+1}=\mathbf w_t+\alpha\rho_t(\mathbf x_t-\gamma\mathbf x_{t+1})\mathbf x_t^\top\mathbf v_t$（L4915–4921，(11.29) 一路代下去）。
- **TDC / GTD(0)**：先多做几步解析变形再代入 $\mathbf v_t$，得 $\mathbf w_{t+1}=\mathbf w_t+\alpha(\mathbb E[\rho_t\delta_t\mathbf x_t]-\gamma\mathbb E[\rho_t\mathbf x_{t+1}\mathbf x_t^\top]\mathbf v_t)$（L4923–4937）。两者都是 $O(d)$（先算内积 $\mathbf x_t^\top\mathbf v_t$）。
- **级联（cascade）与双时间尺度**：主学习（w）依赖次学习（v）已收敛，反之不然；收敛证明通常要求 $\beta\to0$ 且 $\alpha/\beta\to0$（L4942–4944）。
- 扩展：GQ（动作值+控制）、GTD(λ)/GQ(λ)（资格迹）、非线性逼近、hybrid-TD、proximal+control variates（L4946–4950）。

### 3.3 Emphatic-TD（L4951–4978）

思路：离策略下状态分布 $\mu_b$ 与目标策略的转移不匹配；那就**重新加权状态**，把更新分布拉回某个 on-policy 分布。核心机制是**伪终止（pseudo termination）**：把折扣 γ 理解为「每步以 $1-\gamma$ 的概率终止并立即从转移到的状态重启」，重启方式任选（L4955–4961）。一步 Emphatic-TD：$\delta_t=R_{t+1}+\gamma\hat v(S_{t+1},\mathbf w_t)-\hat v(S_t,\mathbf w_t)$，$\mathbf w_{t+1}=\mathbf w_t+\alpha M_t\rho_t\delta_t\nabla\hat v(S_t,\mathbf w_t)$，$M_t=\gamma\rho_{t-1}M_{t-1}+I_t$，$I_t$ 是 interest，$M_t$ 是 emphasis，$M_{-1}=0$（L4963–4974）。

### 3.4 第 12 章：资格迹主干（L5032–5733）

- **λ-return**（**L5083，(12.2)**）：$G_t^\lambda\doteq(1-\lambda)\sum_{n=1}^\infty\lambda^{n-1}G_{t:t+n}$；等价拆分形式 (12.3) 把终端后的项分离出来，因此 λ=1 ⇒ 纯 MC，λ=0 ⇒ 一步 TD（L5085–5087）。权重按 $(1-\lambda)\lambda^{n-1}$ 指数衰减（Figure 12.2，L5080）。
- **off-line λ-return**（**L5095，(12.4)**）：回合内不改权重，回合末统一按 $G_t^\lambda$ 做半梯度更新。
- **TD(λ)**（§12.2，L5108–5177）：资格迹 $\mathbf z_{-1}\doteq\mathbf 0$，$\mathbf z_t\doteq\gamma\lambda\mathbf z_{t-1}+\nabla\hat v(S_t,\mathbf w_t)$（**L5119，(12.5)**）；$\delta_t\doteq R_{t+1}+\gamma\hat v(S_{t+1},\mathbf w_t)-\hat v(S_t,\mathbf w_t)$（**L5125，(12.6)**）；$\mathbf w_{t+1}\doteq\mathbf w_t+\alpha\delta_t\mathbf z_t$（**L5131，(12.7)**）。**这就是「前向视图 = 后向视图」的最古老等价**（L5034–5046 章首、L5152 Figure 12.5）。TD(1) 可在线、增量地实现 MC，并可用于带折扣的 continuing 任务（L5158–5164）。线性 TD(λ) on-policy 收敛，误差界 $\overline{\mathrm{VE}}(\mathbf w_\infty)\le\frac{1-\gamma\lambda}{1-\gamma}\min_{\mathbf w}\overline{\mathrm{VE}}(\mathbf w)$（**L5170，(12.8)**）。
- **TTD(λ) / n-step truncated λ-return**（§12.3，L5179–5212）：把 (12.3) 的 T 换成视野 h 得 (12.9)（L5186）；关键恒等式 $G_{t:t+k}^\lambda=\hat v(S_t,\mathbf w_{t-1})+\sum_{i=t}^{t+k-1}(\gamma\lambda)^{i-t}\delta_i'$ 使每步计算量不随 n 增长（**L5203，(12.10)**）。
- **online λ-return**（§12.4，L5214–5251）：每步「把本回合至今所有更新从头重做一遍」，权重向量记为 $\mathbf w_t^h$（horizon h 的第 t 个权重）；$\mathbf w_{t+1}^h\doteq\mathbf w_t^h+\alpha[G_{t:h}^\lambda-\hat v(S_t,\mathbf w_t^h)]\nabla\hat v(S_t,\mathbf w_t^h)$，$\mathbf w_t\doteq\mathbf w_t^t$。代价是每步回扫一次本回合，但**这是当时表现最好的 TD 算法**（L5255）。
- **true online TD(λ)**（§12.5，L5253–5310）：找到 online λ-return 的**精确**后向实现（仅线性逼近下）。权重三角阵列中只有对角线 $\mathbf w_t^t$ 真正需要；算法 $\mathbf w_{t+1}\doteq\mathbf w_t+\alpha\delta_t\mathbf z_t+\alpha(\mathbf w_t^\top\mathbf x_t-\mathbf w_{t-1}^\top\mathbf x_t)(\mathbf z_t-\mathbf x_t)$，迹为 **dutch trace** $\mathbf z_t\doteq\gamma\lambda\mathbf z_{t-1}+(1-\alpha\gamma\lambda\mathbf z_{t-1}^\top\mathbf x_t)\mathbf x_t$（**L5272，(12.11)**）。内存同 TD(λ)，每步计算约多 50%，仍是 $O(d)$（L5282–5286）。另列 **replacing trace**（**L5305，(12.12)**），并断言 dutch trace 基本取代之；accumulating trace 在非线性逼近下仍有用（L5307–5309）。
- **§12.6 唯一被完整演示的前向/后向等价**（L5310–5342）：把线性 MC/LMS 更新 $\mathbf w_{t+1}\doteq\mathbf w_t+\alpha[G-\mathbf w_t^\top\mathbf x_t]\mathbf x_t$（**L5317，(12.13)**）用 dutch trace（$\gamma\lambda=1$ 特例）加辅助向量 $\mathbf a_t$ 重写成 $O(d)$/步的增量算法，得到与 MC 完全相同的最终 $\mathbf w_T$（**L5325，(12.14)** 及两侧）。结论句（L5338–5340）：**资格迹根本不是 TD 特有的，它更基本；只要想高效地学长期预测，就会出现资格迹。**
- **Sarsa(λ)**（§12.7，L5342–5452）：把全部状态值公式换成动作值即可；动作值 off-line λ-return (12.15)（L5353）、TD 误差 (12.16)（L5367）、动作值资格迹 $\mathbf z_t\doteq\gamma\lambda\mathbf z_{t-1}+\nabla\hat q(S_t,A_t,\mathbf w_t)$。给出「二值特征 + accumulating/replacing trace」的高效伪代码（L5400–5414）。**true online Sarsa(λ)** 伪代码同页（L5432–5450）。另有 truncated 版 **forward Sarsa(λ)**（van Seijen 2016），被点名「适合与多层神经网络配合的 model-free 控制方法」（L5452）。
- **§12.8 可变 λ 与 γ**（L5454–5490）：把 λ、γ 升格为状态/动作的函数 $\lambda_t\doteq\lambda(S_t,A_t)$、$\gamma_t\doteq\gamma(S_t)$。一般化回报 (12.17)（L5461），要求 $\prod_{k=t}^\infty\gamma_k=0$ a.s.；于是**回合制、伪终止、折扣连续任务被统一成「单一经验流」**，终端态 = $\gamma(s)=0$ 且转移到起始分布的状态（L5463–5467）。可变自举的 λ-return：状态式 (12.18)、Sarsa 式 (12.19)、Expected Sarsa 式 (12.20)（**L5469–5487**）。
- **§12.9 离策略资格迹 + control variates**（L5492–5584）：非截断 λ-return 没有「把重要性采样乘在目标上」的实用选项，于是直接用 per-decision IS with control variates 的自举推广 (12.22)（**L5499**）；写成 TD 误差和 (12.24)（**L5511**）；用求和规则交换求和次序，导出**一般离策略 accumulating trace**（**L5539，(12.25)**）：

$$\mathbf z_t\doteq\rho_t\bigl(\gamma_t\lambda_t\mathbf z_{t-1}+\nabla\hat v(S_t,\mathbf w_t)\bigr)$$

  on-policy 时 ρ≡1，退化为普通 TD(λ)。动作值侧（从 Expected Sarsa 形式出发更简洁）得 (12.26)–(12.28)，迹为 $\mathbf z_t\doteq\gamma_t\lambda_t\rho_t\mathbf z_{t-1}+\nabla\hat q(S_t,A_t,\mathbf w_t)$（**L5571，(12.29)**），作者称由此得到的 **Expected Sarsa(λ) 是当前最好的一类算法**，但强调「我们不知道文献里是否已被描述或测试过」（L5573–5575、L5723–5725）。λ=1 时与 MC 只有**期望意义**上的等价，不是逐回合等价；要严格等价需要 provisional weights 向量（PTD(λ)/PQ(λ)，L5578–5582）。
- **§12.10 Watkins's Q(λ) → Tree-Backup(λ)**（L5586–5618）：Watkins 的 Q(λ) 在首个非贪心动作处把迹清零；TB(λ) 的迹折减因子换成目标策略概率 $\mathbf z_t\doteq\gamma_t\lambda_t\pi(A_t|S_t)\mathbf z_{t-1}+\nabla\hat q(S_t,A_t,\mathbf w_t)$（**L5618**）。作者称 TB(λ) 「arguably the true successor to Q-learning」，因为它保留了 Q-learning 不用重要性采样的优点（L5588–5590）。
- **§12.11 带迹的稳定离策略方法**（L5620–5676），四个，全部假设线性逼近：
  - **GTD(λ)**：$\mathbf w_{t+1}\doteq\mathbf w_t+\alpha\delta_t^s\mathbf z_t-\alpha\gamma_{t+1}(1-\lambda_{t+1})(\mathbf z_t^\top\mathbf v_t)\mathbf x_{t+1}$，配 $\mathbf v_{t+1}\doteq\mathbf v_t+\beta\delta_t^s\mathbf z_t-\beta(\mathbf v_t^\top\mathbf x_t)\mathbf x_t$（**L5633，(12.30)**）。
  - **GQ(λ)**：动作值版，用平均特征 $\bar{\mathbf x}_t\doteq\sum_a\pi(a|S_t)\mathbf x(S_t,a)$。
  - **HTD(λ)**：GTD(λ) 与 TD(λ) 的混合，最大卖点是 **on-policy 时严格退化为 TD(λ)**（GTD(λ) 不是），因此只需一个步长；代价是第二套权重 $\mathbf v_t$ 加第二套迹 $\mathbf z_t^b$。
  - **Emphatic TD(λ)**：$\mathbf z_t\doteq\rho_t(\gamma_t\lambda_t\mathbf z_{t-1}+M_t\mathbf x_t)$，$M_t\doteq\lambda_tI_t+(1-\lambda_t)F_t$，followon trace $F_t\doteq\rho_{t-1}\gamma_tF_{t-1}+I_t$，$F_0\doteq i(S_0)$。**on-policy 下它对任意状态依赖的 λ 函数都保证收敛，而 TD(λ) 只对常数 λ 保证收敛**（L5668–5670，引 Ghiassian/Rafiee/Sutton 2016 的反例）。
- **§12.12 实现问题**（L5676–5680）：朴素实现要每步更新所有状态的迹，串行机不可接受；但典型 λ、γ 下绝大多数迹≈0，只更新少数显著非零的迹即可，表格情形用迹的代价常只是一步法的几倍。**表格情形反而是迹计算复杂度的最坏情形**；用 ANN+反向传播时迹大致只带来内存与计算翻倍。
- **§12.13 结论**（L5682–5697）：迹是「长延迟奖励与非马尔可夫任务的第一道防线」；λ 应放在 MC 与一步 TD 之间，**推向 MC 但不要推到底**（纯 MC 端性能急剧下降）；数据稀缺、不能反复处理时用迹，离线可廉价生成数据时不用。Figure 12.14 用四个任务佐证「中间 λ 最好」（**L5699**）。

### 3.5 第 13 章：策略梯度（L5735–6000）

- **通用 schema**：$\boldsymbol\theta_{t+1}=\boldsymbol\theta_t+\alpha\widehat{\nabla J(\boldsymbol\theta_t)}$（**L5744，(13.1)**）；用策略参数 $\boldsymbol\theta\in\mathbb R^{d'}$，值函数权重仍记 $\mathbf w\in\mathbb R^d$（L5739–5743）。
- **§13.1 策略参数化与优点**（L5749–5783）：离散动作空间常用 **soft-max in action preferences** $\pi(a|s,\boldsymbol\theta)\doteq e^{h(s,a,\boldsymbol\theta)}/\sum_b e^{h(s,b,\boldsymbol\theta)}$（**L5756，(13.2)**），偏好可为线性 $h(s,a,\boldsymbol\theta)=\boldsymbol\theta^\top\mathbf x(s,a)$（**L5764，(13.3)**）或深度网络。三个优点：(i) 可逼近确定性策略（ε-greedy 永远留 ε）；(ii) 可表达**任意概率的随机最优策略**（扑克诈唬）；(iii) 策略函数可能比动作值函数更简单、更易逼近；此外参数化本身就是注入先验的手段（L5766–5781）。
- **Example 13.1 短走廊换向任务**（**L5773–5781**）：三非终端态只有左右两动作，第二态左右反转；特征 $\mathbf x(s,\text{right})=[1,0]^\top$、$\mathbf x(s,\text{left})=[0,1]^\top$ 对所有 s 相同（状态在逼近下不可分辨）。ε=0.1 时 ε-greedy 动作值法只能二选一，值分别 <44 与 82；**最优是「以约 0.59 的概率选右」，值约 11.6**。
- **§13.2 策略梯度定理**（L5785–5829）：回合制定义 $J(\boldsymbol\theta)\doteq v_{\pi_{\boldsymbol\theta}}(s_0)$（**L5794，(13.4)**），文中假设无折扣 γ=1。定理（**L5824，(13.5)**）：

$$\nabla J(\boldsymbol\theta)\propto\sum_s\mu(s)\sum_a q_\pi(s,a)\nabla\pi(a|s,\boldsymbol\theta)$$

  关键是**梯度里不含状态分布的导数**。比例常数在回合制下是平均回合长度，continuing 下是 1（即等式）。证明在 **L5801–5827 的 box**（unrolling，用 $\Pr(s\to x,k,\pi)$）。⚠️ **OCR 损坏**：该 box 的前半段（L5805–5820 左右）公式已被 OCR 打乱成乱码，只有末尾收敛到 (13.5) 的那几行可读。
- **§13.3 REINFORCE**（L5829–5892）：从 (13.6) 出发，把动作求和对 $\pi(a|S_t,\boldsymbol\theta)$ 乘除，换成对 $A_t\sim\pi$ 的期望，再用 $\mathbb E_\pi[G_t|S_t,A_t]=q_\pi(S_t,A_t)$ 替换，得到经典更新

$$\boldsymbol\theta_{t+1}\doteq\boldsymbol\theta_t+\alpha G_t\frac{\nabla\pi(A_t|S_t,\boldsymbol\theta_t)}{\pi(A_t|S_t,\boldsymbol\theta_t)} \quad(\textbf{L5854，(13.8)})$$

  伪代码用**资格向量** $\nabla\ln\pi(A_t|S_t,\boldsymbol\theta_t)$（由 $\nabla\ln x=\nabla x/x$，L5860–5864），并含 $\gamma^t$ 因子（正文用 γ=1，伪代码给一般折扣式，L5866–5877）。REINFORCE 是 MC 方法，**方差高、学得慢**（L5884–5885、L5879–5882 Figure 13.1）。Exercise 13.3 给出线性 soft-max 偏好下的资格向量 (13.9)：$\nabla\ln\pi(a|s,\boldsymbol\theta)=\mathbf x(s,a)-\sum_b\pi(b|s,\boldsymbol\theta)\mathbf x(s,b)$（**L5889**）。
- **§13.4 REINFORCE with Baseline**（L5894–5940）：定理可推广到减任意 baseline $b(s)$（**L5899，(13.10)**），因为 $\sum_a b(s)\nabla\pi(a|s,\boldsymbol\theta)=b(s)\nabla 1=0$。更新 $\boldsymbol\theta_{t+1}\doteq\boldsymbol\theta_t+\alpha(G_t-b(S_t))\frac{\nabla\pi(A_t|S_t,\boldsymbol\theta_t)}{\pi(A_t|S_t,\boldsymbol\theta_t)}$（**L5911，(13.11)**）。baseline 不改变期望、但可**大幅降方差**；自然选择是学出来的状态值 $\hat v(S_t,\mathbf w)$（可用 MC 或 TD 学）。需要两个步长 $\alpha^{\boldsymbol\theta}$、$\alpha^{\mathbf w}$，作者明说**值步长有经验法则（如 $\alpha^{\mathbf w}=0.1/\mathbb E[\|\nabla\hat v\|_\mu^2]$），策略步长怎么设则「much less clear」**（L5928–5930）。短走廊上加 baseline 显著更快（Figure 13.2，L5938–5940），此处 baseline 用单分量 $\hat v(s,\mathbf w)=w$。
- **§13.5 Actor–Critic**（L5942–6000）：与 REINFORCE-with-baseline 的关键差别是**critic 也作用在转移的第二个状态上**，因此一步回报 $G_{t:t+1}$ 可用于评价刚做的动作。一步 actor–critic：$\boldsymbol\theta_{t+1}\doteq\boldsymbol\theta_t+\alpha(G_{t:t+1}-\hat v(S_t,\mathbf w))\frac{\nabla\pi(A_t|S_t,\boldsymbol\theta_t)}{\pi(A_t|S_t,\boldsymbol\theta_t)}=\boldsymbol\theta_t+\alpha\delta_t\frac{\nabla\pi(\cdot)}{\pi(\cdot)}$（**L5949/5953/5957，(13.12)–(13.14)**），critic 用半梯度 TD(0)。**明确说明梯度偏差不是自举本身造成的——即使用 MC 学 critic，actor 仍有偏**（L5946）。伪代码给出一-step actor–critic（L5960–5975，含折扣因子 $I\leftarrow\gamma I$）与**带资格迹的 actor–critic**（L5980–6000，actor 用 $\mathbf z^{\boldsymbol\theta}\gets\gamma\lambda^{\boldsymbol\theta}\mathbf z^{\boldsymbol\theta}+I\nabla\ln\pi(A|S,\boldsymbol\theta)$，critic 用 $\mathbf z^{\mathbf w}\gets\gamma\lambda^{\mathbf w}\mathbf z^{\mathbf w}+\nabla\hat v(S,\mathbf w)$）。

## 4. 它声称的效果（本片出现的数字/图与条件）

| 断言 | 依据行 |
|---|---|
| 一对数据分布相同的 MRP：w=0 时左 MRP 的 BE=0，右 MRP 的 $\overline{\mathrm{BE}}=\mu(B)\cdot1+\mu(B')\cdot1=2/3$ | L4815–4825（Example 11.4） |
| 右 MRP 的 BE 最小解在 γ→1 时为 $(-\tfrac12,0)^\top$，与左 MRP 的 w=0 不同 ⇒ BE 最优解不可学 | L4827–4831 |
| 出现 k 个 B 的概率两 MRP 都是 $2^{-k}$，$\mu(s)=1/3$ | L4821 |
| TDC 在 Baird 反例上 PBE 降到 0，但 1000 次迭代后 VE 仍≈2，参数远未到最优（最优 w 需正比于 $(1,1,1,1,1,1,1,4,-2)^\top$）；步长 α=0.005、β=0.05 | L4940–4944、Figure 11.5 (L4945) |
| 一步 Emphatic-TD 在 Baird 反例上**期望轨迹**收敛、VE→0，步长 α=0.03；但**直接跑算法方差极高，实际中不收敛** | L4976–4977、Figure 11.6 (L4978) |
| 19 状态随机游走上，off-line λ-return 与 n-step 法整体相当，**中间的自举参数最好**；λ-return 在最优 α 与高 α 处略好 | L5098–5101、Figure 12.3 (L5101) |
| TD(λ) 与 off-line λ-return 在 ≤最优 α 时几乎完全一致；α 超过最优后 λ-return 只略差，**TD(λ) 明显更差甚至可能不稳定** | L5163–5165、Figure 12.6 (L5165) |
| 线性 TD(λ) 收敛误差界 $\frac{1-\gamma\lambda}{1-\gamma}$ 倍最优，λ→1 时界最紧（λ=0 最松），但**实践中 λ=1 常是最差选择** | L5170–5174、(12.8) |
| online λ-return 在随机游走上（连 VE 这个对 off-line 最有利的指标）**仍略优于 off-line λ-return** | L5249–5251、Figure 12.8 (L5251) |
| true online TD(λ) 与 online λ-return **产生完全相同的权重序列**（van Seijen et al. 2016）；内存同 TD(λ)，每步计算约多 50%，仍 O(d) | L5282–5286 |
| Mountain Car 上 Sarsa(λ)（replacing traces）比 n-step Sarsa 学得更高效 | L5417–5421、Figure 12.10 (L5422) |
| true online Sarsa(λ) 在 Mountain Car 上优于 regular Sarsa(λ)（accumulating 与 replacing 两种迹都比不过）；λ=0.9 | Figure 12.11 (L5428–5430) |
| 离策略 Expected Sarsa(λ)（(12.29)）「可能是当前最好的一类算法」 | L5573–5575 |
| 短走廊：ε-greedy 两个候选策略值 <44 与 82；最优「以 0.59 概率选右」值约 11.6 | L5777–5781、Example 13.1 (L5773) |
| 加 baseline 的 REINFORCE 在短走廊上比不加学得快得多 | L5938–5940、Figure 13.2 |
| 迹的代价：表格法通常只是一步法的几倍；ANN+反向传播大致内存与计算翻倍 | L5676–5680 |
| λ 效果：四个测试任务上**中间 λ 最好**；纯 MC 端性能急剧下降 | L5686–5694、Figure 12.14 (L5699) |

## 5. 它的实验条件（本片涉及的实验设置）

本片横跨**五种互不相同**的实验装置，主控合并时不要混为一谈：

1. **解析反例（MRP/MDP 对）**，不涉及采样噪声：A-split（L4837–4839 提到的 page 273 例）、Baird's counterexample（Figure 11.5）、Example 11.4 的两 MRP 对（Figure 11.4 附图）。这类「实验」是**期望轨迹的迭代计算**（Emphatic-TD 的结果明确说是「iteratively computing the expectation of the parameter vector trajectory without any of the variance」，**L4976**）。
2. **19-state Random Walk（Example 7.1，page 144）**：第 12 章沿用第 7 章同一任务，性能指标 = **回合结束时刻**每个状态真值与估计值之间的**估计 RMSE，对前 10 个回合与 19 个状态取平均**（L5096–5098）；比较对象：n-step TD 变 n、λ-return 变 λ；Figure 12.3（L5101）、Figure 12.6（L5165）、Figure 12.8（L5251）全部基于它。**这保证了与第 7 章结果可直接数值对比。**
3. **Mountain Car（Example 10.1）**：Sarsa(λ) 的**函数逼近、动作选择、环境细节与第 10 章完全一致**，因此可与第 10 章的 n-step Sarsa 结果数值对比（**L5417–5419**）。Figure 12.10 里的 n-step Sarsa 曲线是**从 Figure 10.4 复制过来的**；训练/评估：平均前 10 回合、100 次独立运行（L5424–5426）。
4. **短走廊（Example 13.1）**：三非终端态、每步奖励 1、第二态左右反转、特征对所有状态相同（L5773–5777）。REINFORCE/带 baseline 的结果见 Figure 13.1/13.2（L5882、L5938），baseline 用单分量 $\hat v(s,\mathbf w)=w$（L5940）。
5. **Figure 12.14 的四个任务**是转载自四份不同旧工作（两块 Sarsa(λ)+tile coding 的连续状态控制、TD(λ) 的随机游走策略评估、pole-balancing 未发表数据），**不是同一套条件**，作者自己标了出处（L5699）。

## 6. 它自己承认的局限（逐字引用）

- BE 的不可学是**原理性**的，不是工程问题：*"Thus, the BE is not learnable; it cannot be estimated from feature vectors and other observable data. This limits the BE to model-based settings. There can be no algorithm that minimizes the BE without access to the underlying MDP states beyond the feature vectors."*（**L4833–4834**）——并且点明 residual-gradient 唯一能做 BE 靠的是双采样：*"Minimizing the BE requires some such access to the nominal, underlying MDP."*（**L4836**）
- Emphatic-TD 的实践失败写得很直白：*"We do not show the results of applying the Emphatic-TD algorithm directly because its variance on Baird's counterexample is so high that it is nigh impossible to get consistent results in computational experiments. The algorithm converges to the optimal solution in theory on this problem, but in practice it does not."*（**L4976**）
- 离策略本质高方差、且无法消除：*"Off-policy learning is inherently of greater variance than on-policy learning... You can't expect to learn how to drive by cooking dinner, for example."*（**L4980–4982**）；*"High variance will probably always remains a challenge for off-policy learning."*（**L5002**）
- 整个离策略领域尚无定论：*"The whole area of off-policy learning is relatively new and unsettled. Which methods are best or even adequate is not yet clear. Are the complexities of the new methods introduced at the end of this chapter really necessary? ... The potential for off-policy learning remains tantalizing, the best way to achieve it still a mystery."*（**L5004–5006**）
- true online TD(λ) 的推导被作者自己省略：*"The derivation of true online TD(λ) is a little too complex to present here"*（**L5261**）
- Expected Sarsa(λ) 的新颖性/验证缺口由作者自述：*"Although it is a natural algorithm, to our knowledge it has not previously been described or tested in the literature."*（**L5723–5725**）；*"The practical consequences of all these new off-policy methods have not yet been established."*（**L5580**）
- λ 的选择没有理论答案：*"Where shall we place them? We do not yet have a good theoretical answer to this question"*（**L5688**）；*"In the future it may be possible to more finely vary the trade-off between TD and Monte Carlo methods by using variable λ, but at present it is not clear how this can be done reliably and usefully."*（**L5692–5694**）
- TD(λ) 只对常数 λ 保证收敛：*"whereas Emphatic-TD(λ) is guaranteed to converge for all state-dependent λ functions, TD(λ) is not. TD(λ) is guaranteed convergent only for all constant λ."*（**L5668–5670**）
- 迹 vs 一步法的取舍是有条件的：*"in off-line applications in which data can be generated cheaply, perhaps from an inexpensive simulation, then it often does not pay to use eligibility traces."*（**L5696**）
- 两个步长难调：*"It is much less clear how to set the step size for the policy parameters, α^θ, whose best value depends on the range of variation of the rewards and on the policy parameterization."*（**L5928–5930**）
- actor 的偏差与自举无关：*"Note that the bias in the gradient estimate is not due to bootstrapping as such; the actor would be biased even if the critic was learned by a Monte Carlo method."*（**L5946**）

## 7. 它没做但看起来能做的地方

1. **Expected Sarsa(λ) 的实证空白**（L5723–5725 自述未被测试过）。本片给出了完整算法式与迹式 (12.29)，却**没有任何一张它的实验图**；Mountain Car/随机游走那几张图全是 Sarsa(λ)/true online Sarsa(λ)。这是最直接的「作者亲手标出的空白」。
2. **真·逐回合等价**。λ=1 时这批离策略算法与 MC 只在期望意义上等价（L5578）；PTD(λ)/PQ(λ) 用 provisional weights 做到严格等价，但作者说「实践后果尚未确立」（L5580）。→ 在一个含零概率动作的离策略回合上，逐条比较 MC / TD(λ) / PTD(λ) 的更新差异，是个明确可做的小实验。
3. **Emphatic-TD 的方差治理**。作者把它的失败原因直接归给方差（L4976），而 §11.9 恰好列了一批方差手段（momentum、Polyak-Ruppert 平均、逐分量自适应步长、importance-weight-aware 更新，L4986–4990）。**把 Emphatic-TD 与其中任一条组合并在 Baird 反例上跑出稳定曲线，是本片自然指向的下一步。**
4. **可变 λ 的可操作化**。作者说「不清楚怎么可靠又有用地做」（L5692–5694），但 (12.18)–(12.22) 已把可变 λ/γ 的递归形式与离策略形式都写全了。→ 用状态依赖 λ（例如按状态访问次数或 TD 误差量级设 λ）做对照实验，是公式已备、实验未做。
5. **§12.4 的 online λ-return 复杂度**。「每步重扫本回合」是 $O(T)$/步；作者只说 true online TD(λ) 在线性情形下有精确后向实现（L5257–5261）。→ 非线性/神经网络逼近下能否有廉价近似，本片明确留空。
6. **把 (12.10) 那条恒等式推广**：$G_{t:t+k}^\lambda=\hat v+\sum(\gamma\lambda)^{i-t}\delta_i'$ 是 TTD(λ) 高效实现的关键（L5203），而 Exercise 12.5（L5212）只要求证明它。→ 能否据此为任意 *truncated + off-policy + control variate* 组合构造 O(d)/步实现，本片没展开。
7. **策略梯度与资格迹的结合只给了伪代码**（L5980–6000）：actor–critic with eligibility traces 有完整的迹方程，但**本片没有给它的任何实验结果**，也没有讨论 $\lambda^{\boldsymbol\theta}$ 与 $\lambda^{\mathbf w}$ 该不该分开设。
8. **§13.7（连续动作空间）被本片截断**：L5762 承诺「as we describe later in Section 13.7」，但 Section 13.7 落在下一片。→ 主控合并时注意这条跨片引用。

## 8. 和同批其他篇的关系

- **它自己是教材，不是论文**。因此「引用同批其他篇」这件事基本不成立——它的参考文献是 RL 领域的经典谱系（Klopf 1972、Sutton 1988、Watkins 1989、Baird 1995、Tsitsiklis & Van Roy 1996/1997、Precup et al. 2000、Maei 2011、van Seijen et al. 2016 等）。
- 但本片**密集引用了本教材自己的前序章节**，这些引用是跨片接口，主控合并时必须对齐：第 3 章（return 递归式 (3.9)）、第 5 章（MC、weighted IS (5.13)、recognizers）、第 6 章（TD(0) (6.2)、Q-learning/Expected Sarsa 统一、$G_t$ 的 TD 误差和 (6.6)）、**第 7 章（n-step (7.1)/(7.3)、Tree Backup §7.5、per-decision IS §7.3、control variates §7.4、(7.8)/(7.13)/(7.14)/(7.16)）——本片对第 7 章的引用最密集**、第 9 章（线性逼近、TD 不动点 §9.4、最小二乘 §9.8、特征构造 §9.5、步长法则 §9.6、Emphatic-TD 初版 §9.11、(9.3)/(9.7)/(9.11)/(9.14)/(9.15)）、第 10 章（Mountain Car Example 10.1、平均奖励 §10.3）、第 11 章前半（deadly triad §11.3、page 273 的 A-split 例、(11.1)/(11.2)/(11.9)/(11.13)/(11.14)/(11.22)）。
- **谱系上「像谁/不像谁」**：本片后半（Ch12）明显是「van Seijen 学派」的写法（forward/backward view 术语、true online、dutch trace 命名、truncated TD），作者在历史注记里逐节点名（L5701–5733）；Ch13 开头则是标准的 Williams(1992) REINFORCE + Sutton et al.(2000) policy gradient theorem + actor–critic 一线。

## 9. 对「负载变化下到达率/时延」这件事，它贡献了什么事实

**没有直接贡献。** 本片是 RL 算法理论，全片没有出现 arrival rate、queueing、delay/latency 的任何实验或分析。擦边接口只有两处：

- §12.13 明确讨论了**「在线（数据稀缺、不可反复处理）↔ 离线（可廉价生成大量数据）」**这一取舍（L5696）：在线应用中用资格迹换取「每个数据点学到更多」；离线模拟廉价时不用迹、改为「尽可能快地处理尽可能多的数据」。**这是本片唯一与「负载/数据生成速率」沾边的论断，且它是定性的、没有给出任何速率—性能曲线。**
- 策略梯度/actor–critic 被描述为「fully online, incremental, states, actions, and rewards processed as they occur and then never revisited」（L5962）——这描述的是**单样本处理延迟**（每步 O(d)，无需回扫或等待回合结束），对「在线时延敏感系统」是可用的性质，但作者没有从时延角度论证。
- 若要把它接到「负载变化下的到达率/时延」，本片能提供的只有**算法层面的计算复杂度事实**：GTD2/TDC 为 O(d)（L4921、L4937）、true online TD(λ) 内存同 TD(λ) 而每步计算 +50%（L5284–5286）、表格迹「通常只是一步法的几倍」、ANN 下约翻倍（L5680）、online λ-return 每步回扫本回合因而是最贵的（L5246–5247）。**这些是「每步计算成本」，不是「端到端时延」。**建议主控在合并时把本片在第 9 项标为「无直接贡献 + 提供计算复杂度佐证」。

## 10. 一句话评价

本片在方法谱系里的位置是：**为「离策略 + 函数逼近」这一失败区给出完整的目标函数分类学（哪些能学、哪些原理上不能学），再把资格迹从「TD 的一个技巧」重新定位成「高效长期预测的通用机制」，最后把整本书从「学值、再从中导出策略」扭转到「直接对策略求梯度」的分水岭章节。** 三段里最硬的是 §11.6 的 BE 不可学定理（含 Example 11.4 的反例）与 §12.6 的前向/后向等价演示；最诚实的是它在 §11.10/§12.13 反复承认「哪个方法最好仍不清楚」。**它没有给出新算法与对应实验的自洽闭环——Expected Sarsa(λ)、actor–critic with traces 都只到伪代码为止。**

---

## 本片要点（供主控合并）

1. **BE 原理上不可学，且其最小解也不可学（本片最硬的理论结论）。** Example 11.4（**L4815–4836**）给出一对**数据分布完全相同**的 MRP：出现 k 个 B 的概率都是 $2^{-k}$、$\mu(s)=1/3$，但 w=0 时左 MRP 的 BE=0 而右 MRP 的 $\overline{\mathrm{BE}}=2/3$；更关键的是**最小化 w 也不同**（右 MRP 在 γ→1 时最优为 $(-\tfrac12,0)^\top$）。原文结论逐字：*"the solution that minimizes BE cannot be estimated from data alone... it is impossible in principle to pursue the BE as an objective for learning."*（L4829–4831）；而 VE 虽然也不可学，但**其最优参数 w\* 可学**，因为 RE = VE + 与 w 无关的方差项（**L4806，(11.24)**）。

2. **资格迹不是 TD 特有的，而是「高效学长期预测」的通用机制**——这是 §12.6 唯一被完整演示的前向/后向等价所证明的（**L5310–5342**）。用 dutch trace 加辅助向量 $\mathbf a_t$，能把线性 MC/LMS 的存储式离策略更新 (12.13) 重写成 $O(d)$/步的增量算法，(12.14) 给出**完全相同的最终 $\mathbf w_T$**（L5325–5336，⚠️ 该式 OCR 严重损坏）。原文：*"It seems eligibility traces are not specific to TD learning at all; they are more fundamental than that."*（L5338–5340）。

3. **true online TD(λ) 是 online λ-return 的精确后向实现（内存同 TD(λ)，每步计算 +50%，仍 O(d)）**，关键新机制是 **dutch trace** $\mathbf z_t\doteq\gamma\lambda\mathbf z_{t-1}+(1-\alpha\gamma\lambda\mathbf z_{t-1}^\top\mathbf x_t)\mathbf x_t$（**L5272，(12.11)**；算法式 L5266–5270；伪代码 L5288–5304；同性质声明 L5282–5284）。作者直接称 online λ-return 是 "currently the best performing temporal-difference algorithm"（**L5255**），且它在随机游走上连 VE 这个对离线法最有利的指标都被在线法略胜（**L5251**，Figure 12.8）。

4. **离策略资格迹的完整一般式与两个「作者亲口说的空白」。** 一般离策略 accumulating trace：$\mathbf z_t\doteq\rho_t(\gamma_t\lambda_t\mathbf z_{t-1}+\nabla\hat v(S_t,\mathbf w_t))$（**L5539，(12.25)**，状态值）；动作值侧用 Expected Sarsa 形式最简洁，得 $\mathbf z_t\doteq\gamma_t\lambda_t\rho_t\mathbf z_{t-1}+\nabla\hat q(S_t,A_t,\mathbf w_t)$（**L5571，(12.29)**），据此得到的 Expected Sarsa(λ) 被作者称为 "probably the best algorithm of this type at the current time"（L5573–5575）。**空白一**：*"Although it is a natural algorithm, to our knowledge it has not previously been described or tested in the literature."*（**L5723–5725**）——即该算法**没有实验**。**空白二**：λ=1 时这批方法与 MC **只在期望意义上等价**，需 provisional weights 才能严格等价（PTD(λ)/PQ(λ)），且「其实践后果尚未确立」（**L5578–5582**）。

5. **第 13 章的分水岭：策略梯度定理 + REINFORCE + baseline + actor–critic 的完整链条，以及「策略参数化优于动作值参数化」的反例式论据。** 定理 (13.5)：$\nabla J(\boldsymbol\theta)\propto\sum_s\mu(s)\sum_a q_\pi(s,a)\nabla\pi(a|s,\boldsymbol\theta)$（**L5824**），关键是指梯度不含状态分布导数。Example 13.1 短走廊给出**动作值方法无法表达随机最优策略**的具体数字：ε=0.1 的 ε-greedy 只能二选一（值 <44 或 82），而**最优是「0.59 概率选右」，值约 11.6**（**L5777–5781**）。随后 REINFORCE (13.8)（**L5854**）→ 带 baseline 的泛化 (13.11)（**L5911**，baseline 不减期望但大降方差，**L5913–5915**）→ one-step actor–critic (13.12)–(13.14)（**L5949–5957**）→ 带资格迹的 actor–critic 伪代码（**L5980–6000**）。**注意两条局限**：actor 的梯度偏差**不是**自举造成的（*"the actor would be biased even if the critic was learned by a Monte Carlo method"*，**L5946**）；策略步长 $\alpha^{\boldsymbol\theta}$ 没有经验法则，作者明说 "much less clear"（**L5928–5930**）。

---

### 覆盖与诚实声明

- **覆盖区间：L4801–L6000，全部 1200 行逐行读完**（8 次 `sed` 全量输出：4801-4950、4951-5100、5101-5250、5251-5400、5401-5550、5551-5700、5701-5850、5851-6000），未越界读本片以外的行。
- 除本片外，仅按 READ-ALL-SPEC 允许的用途使用了 `grep`：**定位章节/图/习题/公式编号的起始行**（得到上文所有行号锚点），未用检索替代阅读。
- **没读懂的段落（如实标注）**：
  1. **L5801–5827 的策略梯度定理证明 box**：OCR 把前半段公式打乱成不可复原的乱码（$\nabla\kappa_\tau\{\mathfrak{s}\}$ 之类的符号噪声），只有末尾收敛到 (13.5) 的三行可读。**证明的整体思路（unrolling + $\Pr(s\to x,k,\pi)$）能看懂，逐步代数不能。**
  2. **L5325 的 (12.14)** 及 §12.6 的 dutch-trace 展开：同样是 OCR 乱码，公式主体不可复原；但结论（$\mathbf z_t$ 由 $\mathbf z_{t-1}+(1-\alpha\mathbf z^\top\mathbf x)\mathbf x$ 更新、$\mathbf a_t$ 由 $\mathbf a_{t-1}-\alpha\mathbf x_t\mathbf x_t^\top\mathbf a_{t-1}$ 更新）从可读的旁注与 L5330–5336 的行文能确认。
  3. **L5266–5270 true online TD(λ) 主更新式**的排版略有错位（$+$ 号与括号位置从伪代码 L5296 反推确认）。
- 本片为教材而非论文，故第 5、8 项（实验条件、与同批篇关系）按「教材章节」语境改写；第 9 项按题面要求如实回答「无直接贡献」。
