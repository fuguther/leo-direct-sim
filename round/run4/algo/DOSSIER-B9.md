# DOSSIER-B9 — T4 通用 RL 方法级摘读（11 篇）

> **批次**：T4 → B9。分支 `agent/20260911-topic-loop-r2`，worktree `.worktrees/topic-loop-20260910`。
> **分配依据**：`round/run4/algo/TIER-ASSIGNMENT.md` L91–L101 —— 11 篇全部定档 T4「通用 RL 机制：迁移条件与反例」，产出文件 B9。
> **全文来源**：VM `ssh vm`，`/data/liguang13/topic-loop-r2/md/<itemKey>/<itemKey>/txt/<itemKey>.md`（MinerU MD）。
> **模板依据**：`round/run4/algo/EXTRACTION-TEMPLATE.md`（12 项）。本批按任务书收敛为 **4 项**：1) 机制（公式逐字+行号）2) 适用条件与理论保证 3) 迁移到 LEO 逐跳路由的条件与障碍 4) 作为**反例**的价值。模板第 12 项（负载相关实验设置）降为条件登记。
> **行号约定**：下文所有 `L<数字>` 均指该篇 MD 的行号，可用 `grep -n` / `sed -n 'a,bp'` 逐条复现。公式一律逐字抄 LaTeX 原文，未作任何自然语言改写。

---

## 0. 开工声明（六项体检）

| 项 | 状态 | 证据 |
|---|---|---|
| 环境 / cwd | **通过** | worktree 存在；`git rev-parse --abbrev-ref HEAD` → `agent/20260911-topic-loop-r2` |
| 关键文件在位 | **通过** | `round/run4/algo/` 含定档表（138 行）与拆解模板（35 行） |
| 依赖 / 二进制 | **通过** | `ssh vm` 可用；11 个 MD 全部存在，行数 271–9596，字节 57 KB–1.68 MB |
| 权限 / 沙箱 | **通过（有告警）** | workspace-write。**一次 [HOOK-BLOCK]**：首次读定档表被 perm 拦截（会话 ad38f6d1-61e6-48 未授权）；等 20 s 重试**成功**，未再复现。任务书只允许「重试一次」，故记录在案 |
| 网络 | **通过** | 全部检索经 `ssh vm`，无外网需求 |
| 额度 / 上下文 | **通过（受限）** | 单篇最长 9596 行（教材）；已按任务书对该篇只做定向章节读，见 §1 完成度表 |

**注意**：候选 MD 是 MinerU OCR 产物，含系统性 OCR 讹误。抄录时**保留原文讹误不做修正**，凡影响公式语义者在条目内以 `[OCR: …]` 标注。

---

## 1. 完成度声明（fail-loud，先声明再下结论）

**读完的**（逐行覆盖，可核验）：

| itemKey | 短名 | 已读行区间 | 占总行数 |
|---|---|---|---|
| 57EB6US5 | DQN (Nature 2015) | L135–271 | 137/271 |
| TAUEF8PF | Double DQN | L19–200、L259–356 | 280/356 |
| JSX5XG88 | GAE | L33–271、L362–420 | 298/469 |
| 9FLZ88LZ | QMIX | L60–161、L247–260、L329–395 | 208/437 |
| KPUZIMU5 | MAPPO | L39–55、L128–220、L224–300 | 188/673 |
| FGQSH4AI | MADDPG | L95–162、L238–247、L328–355 | 115/452 |
| E4NYGLGX | Retrace(λ) | L29–292 | 264/692 |
| I2WH9RRR | Asymmetric DQN | L33–372 | 340/429 |
| QGAREQUM | AD-RL 延迟反馈 | L40–245、L295–352 | 264/884 |
| 6C843JTS | TD(λ) | L111–135、L196–240、L488–545、L608–648 | 148/648 |
| LJG6ZW7B | Sutton & Barto | 定向章节 L1000–1012、L4588–4612、L5048–5110、L5682–5700、L6419–6433、L6801–6825、L7380–7457 | 定向 |

**未完成 / 未读，逐条列出（禁止用关键词扫描冒充通读）**：

- **6C843JTS（TD(λ)）是本批完成度最低的一篇**：L1–110（Introduction、§2.1 单步/多步预测、§2.2 计算问题）、L136–195（§3 博弈与随机游走例子）、**L241–487（§4.1 收敛定理证明主体、§4.2 最优性与学习率、§4.3 TD 作为梯度下降）**、L546–607（References）**均未逐行读**。§4 是本篇理论保证的承重章节，本报告对它的描述**只基于 L196–240 的引论段与 L608–648 的附录定理陈述**，**不足以支撑「收敛速度」「学习率最优性」这类细节结论，需要补读**。
- **JSX5XG88 L272–361（§6 实验主体：策略优化算法、架构、任务细节、结果）未读**。故本报告对其「适用条件」只写理论侧，不写实验侧结论。
- **9FLZ88LZ L1–59（标题/摘要/Introduction/Related Work）、L162–246（§6 实验设置、§7 结果）未读**。故 QMIX 的「它自己做了什么实验、赢了多少」本报告不写。
- **KPUZIMU5 L56–127（§4 主结果：MPE/SMAC/GRF/Hanabi 各 testbed）、L301–673 大部分未读**。故 MAPPO 的实验胜负本报告不写。
- **FGQSH4AI L163–237（§5 实验）、L248–327（References）未读**。
- **QGAREQUM L246–294（§5.3 收敛分析：AD-VI / AD-SPI 收敛证明）、L465–884（附录 A 实现、B 证明、C 随机 MDP 辅助延迟选择、D 补充实验）未读**。
- **E4NYGLGX L293–691（References 与附录 A–F 全部证明）未读**。故 Retrace 的定理**只引用陈述，不复现证明**。
- **57EB6US5 L1–134、TAUEF8PF L1–18、I2WH9RRR L1–32 / L373–429 未读**（均为标题/摘要/参考文献区）。
- **LJG6ZW7B（教材，9596 行）只做定向章节读**，这是任务书明确授权的（「对教材只取与信用分配/延迟奖励/部分可观测直接相关的章节」）。未读章节本报告一律不下结论。

---

## 2. 检索方法与负向声明登记表

**协议**（按主控核验协议更新执行）：
1. 每条负向声明写出**精确检索模式原文**；
2. 写出**实测计数**（`grep -a -c -i -E "<pat>" <file>`）；
3. 有命中则给**命中行号 + 为何不构成反例**。

**基线事实（用于 §3 与 §6 的反例判定）**：本批 11 篇**没有任何一篇是 LEO/卫星/路由论文**。证据：

```
grep -a -c -i -E "satellite|LEO|routing" <file>
LJG6ZW7B=0  57EB6US5=0  6C843JTS=0  TAUEF8PF=0  JSX5XG88=0  9FLZ88LZ=0
KPUZIMU5=1  FGQSH4AI=0  E4NYGLGX=0  I2WH9RRR=0  QGAREQUM=0
```

**唯一命中 KPUZIMU5=1 是假阳性**，命中在 L399 参考文献条目：
`[1] Marcin Andrychowicz, Anton Raichuk, Piotr Stanczyk, Manu Orsini, Sertan Girgin, Raphaël´ Marinier, Leonard Hussenot, ...`
—— 匹配的是人名 **"Leo**nard" 的子串，不是 LEO 卫星。**实质判断 0 篇，实测计数 1，命中位置与排除理由如上。**

### 2.1 逐篇负向声明（精确模式 + 实测计数）

| 模式（原文） | 11 篇计数 | 命中判定 |
|---|---|---|
| `grep -a -c -i -E "non-?stationar"` | LJG6ZW7B=24, TAUEF8PF=1, JSX5XG88=1, 9FLZ88LZ=4, KPUZIMU5=2, FGQSH4AI=6, QGAREQUM=1；其余 **0** | 57EB6US5 / 6C843JTS / E4NYGLGX / I2WH9RRR **实测 0 命中** |
| `grep -a -c -i -E "prioritized (experience )?replay|prioritised (experience )?replay"` | E4NYGLGX=1；其余 **0** | 唯一命中 E4NYGLGX **L322 参考文献**：`Schaul, T., Quan, J., Antonoglou, I., and Silver, D. (2016). Prioritized experience replay. In ICLR.` → **不构成对正文的考察** |
| `grep -a -c -i -E "dueling"` | KPUZIMU5=1；其余 **0** | 唯一命中 KPUZIMU5 **L505 参考文献**：`{QPLEX}: Duplex dueling multi-agent q-learning` → **参考文献，非正文** |
| `grep -a -c -i -E "double (q|dqn)|double q-?learning"` | TAUEF8PF=37, LJG6ZW7B=5；其余 **0** | 57EB6US5 实测 **0**（DQN 原文未提 double） |
| `grep -a -c -i -E "delayed reward|reward delay|delay in reward"` | QGAREQUM=6, LJG6ZW7B=9；其余 ≤1 | **TAUEF8PF=1 / 9FLZ88LZ=1 / E4NYGLGX=1 / I2WH9RRR=1 全部是参考文献**（Watkins 1989 博士论文标题 `Learning from delayed rewards`），**不构成正文考察**。JSX5XG88=1 是真命中：**L17** `A key source of difficulty is the long time delay between actions and their positive or negative effect on rewards; this issue is called the credit assignment problem` |
| `grep -a -c -i -E "credit assignment"` | LJG6ZW7B=7, 6C843JTS=5, JSX5XG88=2, QGAREQUM=2, 9FLZ88LZ=1；其余 **0** | 57EB6US5 / TAUEF8PF / KPUZIMU5 / FGQSH4AI / E4NYGLGX / I2WH9RRR **实测 0**（连词都不出现） |
| `grep -a -c -i -E "reward decompos|decompos[a-z]* .{0,25}reward"` | 9FLZ88LZ=1, QGAREQUM=1；其余 **0** | 9FLZ88LZ L48 是 `decomposing a global reward function into a sum of agent-local terms`（**求解便利性分解，不是失败原因分解**） |
| `grep -a -c -i -E "partial(ly)? observ|POMDP"` | I2WH9RRR=29, LJG6ZW7B=28, 9FLZ88LZ=10, 57EB6US5=2, KPUZIMU5=2, FGQSH4AI=2, QGAREQUM=2, JSX5XG88=1；其余 **0** | 6C843JTS / TAUEF8PF / E4NYGLGX **实测 0** |

---

## 3. G-A 对抗性检索结论（主控追加问题）

> **问题**：全库是否有任何工作，把**同一个失败事件**（丢包/超时/溢出）按**物理原因**拆成**不同的学习通道或惩罚项**（例如区分「决策缓存溢出」与「链路队列溢出」）？

### 3.1 检索模式与实测计数（范围：`/data/liguang13/topic-loop-r2/md/` 全库，113 个 itemKey，仅 `--include=*.md`）

```
grep -r -a -c -i -E "<pat>" --include=*.md /data/liguang13/topic-loop-r2/md/
```

| 模式（原文） | 命中文件数 | 实质命中 |
|---|---|---|
| `counterfactual` | 32 | 全部是 **QMIX/COMA 系列的多智能体反事实基线**（9FLZ88LZ、FGQSH4AI、I2WH9RRR、KPUZIMU5），**反事实的是「智能体贡献」，不是「失败原因」** |
| `counter-factual` | **0** | — |
| `reward decompos` | **0** | — |
| `per-cause` | **0** | — |
| `cause-specific` | **0** | — |
| `loss reason` | **0** | — |
| `drop reason` | **0** | — |
| `separate penalty` | **0** | — |
| `loss type|cause of (the )?(loss|drop)` | **0** | — |
| `multi-objective` | 55 | 实质命中见 3.2-A |
| `MORL` | `.md` 中 4 篇 | 实质命中见 3.2-A |
| `reward vector` | **4（全在 UKBSA7WN）** | 见 3.2-A |
| `overflow` | 40 | 见 3.2-D |
| `multi-head` | 22 | 命中为 **GATv2 多头注意力**（FLQLU3T4 L357）、**Transformer 多头注意力**（35T2JJRJ）—— **是注意力头，不是奖励/惩罚头** |
| `dropped due to|drop(ped)? (because|due)` | 12 | 见 3.2-B |

### 3.2 候选反例逐一评估

#### A. UKBSA7WN（QRLSN）—— 奖励向量 / MORL。**分解轴 = 目标类型，不是失败原因。不覆盖 G-A。**

- **L18（关键词）**：`LEO satellite networks; Mega constellation; Multi-objective optimization; Routing algorithm; Reinforcement learning`
- **L139（正文）**：`In QRLSN, we adopt a Multi-Objective Reinforcement Learning (MORL) algorithm to balance end-toend delay and network traffic overhead load.`
- **L141（正文）**：`MORL differs from typical RL, which considers several optimization objectives simultaneously in the learning process, where a reward vector is provided for the agent at each update step`
- **L144（公式逐字）**：
  ```latex
  Q _ { i } ( s , a ) \gets ( 1 - \alpha ) Q _ { i } ( s , a ) + \alpha \biggl [ r _ { i } + \gamma \operatorname* { m a x } _ { a ^ { \prime } \in A } Q _ { i } ( s ^ { \prime } , a ^ { \prime } ) \biggr ]
  ```
- **L147（正文）**：`where $i \in [ 1 , n ]$ and n represents the number of objectives; $r _ { i }$ is the i th feedback signal of the agent's reward vector` —— **每个目标一条独立 Q 表 + 独立反馈信号**，结构上确实是多学习通道。
- **L155（公式逐字）**：
  ```latex
  \mathrm { T Q } ( s , a ) = \sum _ { i = 1 } ^ { n } w _ { i } Q _ { i } ( s , a )
  ```
- **L161（公式逐字，目标 1 = 时延）**：
  ```latex
  f _ { r _ { 1 } } = \left\{ \begin{array} { c c } { { r _ { \mathrm { m a x } } } } & { { N _ { t + 1 } \mathrm { i s \ d e s t i n a t i o n } } } \\ { { r _ { \mathrm { m i n } } + \left( \frac { e } { 2 } \right) ^ { - d _ { i j } } } } & { { \mathrm { O t h e r w i s e } } } \end{array} \right.
  ```
- **L165（公式逐字，目标 2 = 队列负载）**：
  ```latex
  f _ { r _ { 2 } } = \left\{ \begin{array} { c c } { { r _ { \mathrm { m a x } } } } & { { N _ { t + 1 } \mathrm { i s \ d e s t i n a t i o n } } } \\ { { r _ { \mathrm { m i n } } + \left( \frac { e } { 2 } \right) ^ { - n _ { q } } } } & { { \mathrm { O t h e r w i s e } } } \end{array} \right.
  ```
- **L168（正文）**：`where $f _ { r _ { 1 } }$ and $f _ { r _ { 2 } }$ denote the reward function to optimize the end-to-end delay and network traffic overhead load respectively; $d _ { i j }$ is the transmission time between adjacent satellite nodes; $n _ { q }$ is the number of data packet queued in the current node.`

**判定**：分解轴 = **优化目标类型（时延 vs 队列长度）**。它给「负载」单开了一条学习通道，**但没有区分「丢包是因为缓存溢出还是因为链路不可用」**——两条通道都是**回报塑形**，不是**失败归因**。**不覆盖 G-A。**
**但它确实反驳一个更弱的主张**：不能说「LEO 路由 RL 库里没有任何多通道奖励设计」。

#### B. IXVSNEE3（DisCoRoute）—— **点名了两种失败原因，却把它们边缘化成一个标量。最接近 G-A 的「差一步」，也是最有力的 G-A 支持证据。**

- **L385（正文，逐字）**：`Considering packets may be dropped due to congestion or link unavailability, path survival probability is introduced to quantify the likelihood of a packet successfully reaching its intended destination.`

**判定**：它**明确命名了两个物理上不同的丢包原因**（congestion / link unavailability），但立刻把二者乘进同一个标量：
- **L387（公式逐字）**：`$P _ { 1 } = p ^ { H _ { h } } q ^ { H _ { \tau } }$`

即 `p`(inter-orbit link availability) 与 `q`(intra-orbit link availability) 只是**可靠性概率参数**，做的是**解析可靠性计算**，**没有进入任何学习通道，也没有任何学习算法**（该文非学习类）。

**结论**：**点名 ≠ 分解**。这是「原因被命名 → 被边缘化」的教科书式证据：全库最接近 G-A 的地方，恰恰是把两种原因**合并**掉的地方。

#### C. 39NJWBI7（PRIMAL）—— **奖励通道 / 代价通道分离 + 每约束独立拉格朗日乘子。分解轴 = QoS 约束类型。不覆盖 G-A，但是最强的「分通道惩罚」结构反例。**

- **L172（正文，逐字）**：`$r ( o , a , o ^ { \prime } )$ and $\{ c _ { k } ( o , a , o ^ { \prime } ) \} _ { k = 1 } ^ { K }$ are the reward (primary objective) and QoS cost functions (e.g., load balancing) for a given state transition.`
- **L180（正文，逐字）**：`For each packet p, we are interested in the two variables, the reward-return $Z _ { \pi } ^ { r } \equiv \sum _ { h = 0 } ^ { H - 1 } \gamma _ { r } ^ { h } r ( o _ { h } , a _ { h } , o _ { h + 1 } )$ and the cost-return $Z _ { \pi } ^ { c _ { k } } = \sum _ { h = 0 } ^ { H - 1 } \gamma _ { c } ^ { h } c _ { k } ( o _ { h } , a _ { h } , o _ { h + 1 } )$`
- **L222（正文，逐字）**：`Note that traditional methods for solving P2 often rely on reward engineering, where a hand-crafted reward function is designed as a weighted sum of the main objective $\mathcal { I } _ { r }$ and the cost components $\mathcal { I } _ { c _ { k } }$ . This approach relaxes the constraints by incorporating them as penalties into the objective function, using a set of fixed coefficients.`
- **L304（正文，逐字）**：`The update for $\lambda _ { k }$ in (27) increases the multiplier if the estimated cost exceeds the threshold $D _ { k }$ , thereby strengthening the penalty on costly actions in the actor's objective.`

**判定**：全库中**唯一的「K 条独立惩罚通道 + 每通道独立自适应系数」**结构。分解轴 = **QoS 约束类型**，**每个通道是一个「资源消耗量」，不是「失败原因」**。**不覆盖 G-A**，但它**直接反驳**「LEO 路由 RL 里没有人做过分通道惩罚」这一主张。

#### D. 其余高计数模式的排除（防止「靠关键词凑结论」）

| 模式 | 命中文件数 | 排除理由 |
|---|---|---|
| `intrinsic reward|auxiliary reward|auxiliary task` | 3 | 实质命中仅 KPUZIMU5（对照方法 `CDS` 用 intrinsic reward 做探索）与教材 §17.1（GVF/辅助**预测任务**）；**都不是失败原因分解** |
| `reward shaping` | 5 | 39NJWBI7 L25（批评启发式塑形）、5PYWVRC5 §1.3、JSX5XG88 §4（**λ 的解释，不是原因分解**）；**没有一篇把塑形项按失败原因拆开** |
| `multi.{0,3}task` | 9 | 命中为 Fuzzy-CNN 多任务路由、多任务学习文献；**与失败原因无关** |
| `separate (head|channel|branch|network)s?` | 3 | 命中为 DQN 目标网络（57EB6US5 L193）、Q-routing full-echo（47J2H748）、DQN 输出单元（教材）；**无奖励/惩罚头分离** |
| `queue overflow|buffer overflow` | 4 | 42E4NAQU L145：`the queue capacity in the simulation is set to 1 Gb/s, effectively preventing queue overflow` —— **主动消除溢出而非建模溢出**；GPDPLJNG / J68GU76W / JP79GMZS 均为流量/队列约束，**无按原因分通道** |

### 3.3 G-A 结论（可直接引用）

**全库 113 个 itemKey 中，没有任何一篇把同一个失败事件按物理原因拆成不同的学习通道或惩罚项。**

最近的三处，**分解轴全都不同**：
1. **UKBSA7WN**：按**目标类型**分解（时延 / 队列负载）→ n 张 Q 表 + 奖励向量 + 加权合成 TQ；
2. **39NJWBI7**：按**QoS 约束类型**分解 → K 条代价通道 + K 个自适应 λ_k；
3. **IXVSNEE3**：**点名**两种失败原因（congestion / link unavailability）后**合并成单一标量存活概率**，且未进入学习。

**净判断**：G-A（把「决策缓存溢出」与「链路队列溢出」这类同事件异原因拆成独立学习通道/惩罚项）**在库内是空白，且是被「绕开」而不是「被解决」的空白**。第 3 条尤其重要：库里已经有人意识到丢包有多种物理原因，却选择把它们边缘化——这正说明「按原因分解」不是显而易见的一步。

---

## 4. 逐篇拆解（11 篇 × 4 项）

> 每篇固定 4 项：**1) 机制**（公式逐字 + 行号）；**2) 适用条件与理论保证**；**3) 迁移到 LEO 逐跳路由的条件与障碍**（四轴：网络级 vs 逐包决策、非平稳、部分可观测、信用分配）；**4) 作为反例的价值**。
> 跨篇共同前提（§2 已证）：**这 11 篇没有一篇是 LEO/卫星/路由论文**，故第 3 项一律是**结构性外推**，不是原文结论；凡外推均标 `[外推]`。

---

### 4.1 57EB6US5 — DQN（Mnih et al., Nature 2015）

**1) 机制（公式逐字 + 行号）**

- **状态**：L161 逐字 —— `Because the agent only observes the current screen, the task is partially observed and many emulator states are perceptually aliased (that is, it is impossible to fully understand the current situation from only the current screen $x _ { t } )$ . Therefore, sequences of actions and observations, $s _ { t } = x _ { 1 } , a _ { 1 } , x _ { 2 } , . . . , a _ { t - 1 } , x _ { t }$ , are input to the algorithm ... This formalism gives rise to a large but finite Markov decision process (MDP) in which each sequence is a distinct state.`
  → **本篇处理部分可观测的唯一手段是把完整历史序列当作状态**，从而"恢复"马尔可夫性。
- **奖励**：L145 逐字 —— `As the scale of scores varies greatly from game to game, we clipped all positive rewards at 1 and all negative rewards at -1, leaving 0 rewards unchanged. Clipping the rewards in this manner limits the scale of the error derivatives and makes it easier to use the same learning rate across multiple games. At the same time, it could affect the performance of our agent since it cannot differentiate between rewards of different magnitude.`
- **Bellman 最优方程（L168 逐字）**：
  ```latex
  \begin{array} { r l } { Q ^ { * } ( s , a ) } & { { } = \mathbb { E } _ { s ^ { \prime } } \biggl [ r + \gamma \underset { a ^ { \prime } } { \operatorname* { m a x } } Q ^ { * } ( s ^ { \prime } , a ^ { \prime } ) | s , a \biggr ] } \end{array}
  ```
- **损失（L174 逐字）**：
  ```latex
  \begin{array} { r l } & { L _ { i } ( \theta _ { i } ) = \mathbb { E } _ { s , a , r } \left[ \left( \mathbb { E } _ { s ^ { \prime } } [ y | s , a ] - Q ( s , a ; \theta _ { i } ) \right) ^ { 2 } \right] } \\ & { \qquad = \mathbb { E } _ { s , a , r , s ^ { \prime } } \left[ \left( y - Q ( s , a ; \theta _ { i } ) \right) ^ { 2 } \right] + \mathbb { E } _ { s , a , r } [ \mathbb { V } _ { s ^ { \prime } } [ y ] ] . } \end{array}
  ```
- **梯度（L180 逐字）**：
  ```latex
  \begin{array} { r l } { \nabla _ { \theta _ { i } } L ( \theta _ { i } ) } & { { } = \mathbb { E } _ { s , a , r , s ^ { \prime } } \biggl [ \biggl ( r + \gamma \operatorname* { m a x } _ { a ^ { \prime } } Q ( s ^ { \prime } , a ^ { \prime } ; \theta _ { i } ^ { - } ) - Q ( s , a ; \theta _ { i } ) \biggr ) \nabla _ { \theta _ { i } } Q ( s , a ; \theta _ { i } ) \biggr ] . } \end{array}
  ```
- **目标网络（L193 逐字）**：`every C updates we clone the network Q to obtain a target network $\hat { \boldsymbol { Q } }$ and use $\hat { \boldsymbol { Q } }$ for generating the Q-learning targetsy for the following C updates to $Q .$`
- **经验回放（L189 逐字）**：`we store the agent's experiences at each time-step, $\boldsymbol { e } _ { t } = ( s _ { t } , a _ { t } , r _ { t } , s _ { t + 1 } )$ , in a data set $D _ { t } = \{ e _ { 1 } , . . . , e _ { t } \} ,$ pooled over many episodes ... to samples of experience, $( s , a , r , s ^ { \prime } ) \sim U ( D )$ , drawn at random from the pool ofstored samples.`
- **误差裁剪（L195 逐字）**：`We also found it helpful to clip the error term from the update $r + \gamma$ max 0 $Q ( s ^ { \prime } , a ^ { \prime } ; \theta _ { i } ^ { - } ) - Q ( s , a ; \theta _ { i } )$ to be between 21 and 1.` `[OCR: "21" 应为 "-1"]`
- **算法（L187 逐字）**：`Training algorithm for deep Q-networks. The full algorithm for training deep Q-networks is presented in Algorithm 1.`；Algorithm 1 正文自 L195 末句起至 L231（`## End For`）。
- **网络**（L141 区块）：3 卷积层（32@8×8 s4 / 64@4×4 s2 / 64@3×3 s1）+ 512 全连接 + 线性输出层；输入 $84 \times 84 \times 4$。

**2) 适用条件与理论保证**

- **原文自述的机制来源（L187）**：`The algorithm modifies standard online Q-learning in two ways to make it suitable for training large neural networks without diverging.` —— 两个修改是回放与目标网络。
- **原文自述回放的三条理由（L189 逐字）**：`First, each step ofexperience is potentially used in many weight updates, which allows for greater data efficiency. Second, learning directly from consecutive samples is inefficient, owing to the strong correlations between the samples ... Third, when learning onpolicy the current parameters determine the next data sample that the parameters are trained on ... It is easy to see how unwanted feedbackloops may arise and the parameters could get stuckin a poor local minimum, or even diverge catastrophica $\mathrm { l } \mathrm { y } .$`
- **理论保证：本篇正文未给出收敛性定理**。在已读区间（L135–271）内**未见任何定理陈述**；唯一接近的是 L171 对表格型值迭代的陈述（`Such value iteration algorithms converge to the optimal action-value function`），**这不是对 DQN 的保证**。**本篇的"保证"是经验性的**：Extended Data Table 3 的消融（有/无回放 × 有/无目标网络 × 3 组学习率）。
- **明确的自述局限（L191 逐字）**：`This approach is in some respects limited because the memory buffer does not differentiate important transitions and always overwrites with recent transitions owing to the finite memory size N. Similarly, the uniform sampling gives equal importance to all transitions in the replay memory. A more sophisticated sampling strategy might emphasize transitions from which we can learn the most, similar to prioritized sweeping.`
- **奖励裁剪的自述代价（L145 逐字）**：`it could affect the performance of our agent since it cannot differentiate between rewards of different magnitude.`

**3) 迁移到 LEO 逐跳路由的条件与障碍** `[外推]`

| 轴 | 条件 | 障碍（引原文为据） |
|---|---|---|
| 网络级 vs 逐包决策 | 需要把每个转发节点做成一个 agent，逐包出动作 | DQN 的动作空间是**固定大小**的（L159：`$\mathcal { A } = \left\{ 1 , \ldots , K \right\}$`），而 LEO 每跳可选邻居数**随轨道位置变化**；原文无动作掩码机制（`grep -a -c -i -E "action mask|invalid action"` 在 L135–271 区间 **0 命中**） |
| 非平稳 | 需要拓扑/负载变化不改变最优策略的表示 | L189 只保证**样本相关性**被回放打散（`randomizing the samples breaks these correlations`），**不保证环境非平稳**。LEO 的 ISL 通断是与动作**无关**的外生非平稳，回放对此无效 |
| 部分可观测 | 需要把历史序列喂进去 | L161 的方案是 `sequences of actions and observations ... are input to the algorithm`，即**状态维度随时长增长**；LEO 中一次端到端会话可达 10²–10³ 跳，序列不可行。原文实际用的是定长历史（L187：`our Q-function instead works on a fixed length representation ofhistories produced by the function w`），**定长窗口在 LEO 中不足以消除拓扑混叠** |
| 信用分配 | 需要把端到端时延/丢包归到具体跳 | L159 逐字：`feedback about an action may only be received after many thousands of time-steps have elapsed` —— **原文承认延迟可达数千步**；DQN 用的是**单步 TD**（L180 的 $\theta _ { i } ^ { - }$ 单步目标），**没有资格迹、没有 n-step、没有 λ**（`grep -a -c -i -E "eligibility trace|n-step"` 在 L135–271 区间 **0 命中**） |

**4) 作为反例的价值**

1. **反驳「奖励只要写对就行、不需要分通道」**：L145 原文自认裁剪后 `it cannot differentiate between rewards of different magnitude` —— **一个标量奖励天生丢失幅度区分度**。这直接支持"把不同失败原因拆成不同通道"的动机。
2. **反驳「回放能解决非平稳」**：L189 给出的三条理由**全部是样本相关性/数据效率角度**，没有一条针对环境非平稳。任何"我们用了经验回放所以能应对 LEO 拓扑动态"的论证在此失效。
3. **反驳「部分可观测只要堆历史帧就行」**：L161 的方案等价于把 POMDP 变成 MDP，代价是状态空间随时长增长；LEO 的跳数尺度使该方案不可行。
4. **正面反例（打我们自己）**：L191 明说 `the memory buffer does not differentiate important transitions`——**如果我们主张"用统一回放池存所有跳的经验"，DQN 原文已经指出这会让稀有但关键的失败经验被冲掉**。LEO 中"溢出丢包"恰是稀有事件，会被均匀回放淹没。

---

### 4.2 TAUEF8PF — Deep RL with Double Q-learning（van Hasselt et al., AAAI 2016）

**1) 机制（公式逐字 + 行号）**

- **Q-learning 参数更新（L32 逐字）**：
  ```latex
  \pmb { \theta } _ { t + 1 } = \pmb { \theta } _ { t } + \alpha \big ( Y _ { t } ^ { \mathrm { Q } } - \pmb { Q } ( S _ { t } , A _ { t } ; \pmb { \theta } _ { t } ) \big ) \nabla _ { \pmb { \theta } _ { t } } \pmb { Q } \big ( S _ { t } , A _ { t } ; \pmb { \theta } _ { t } \big )
  ```
- **Q-learning 目标（L38 逐字）**：
  ```latex
  Y _ { t } ^ { \mathrm { Q } } \equiv R _ { t + 1 } + \gamma \operatorname* { m a x } _ { a } Q ( S _ { t + 1 } , a ; \pmb { \theta } _ { t } ) .
  ```
- **DQN 目标（L48 逐字）**：
  ```latex
  Y _ { t } ^ { \mathrm { D Q N } } \equiv R _ { t + 1 } + \gamma \operatorname* { m a x } _ { a } Q ( S _ { t + 1 } , a ; \pmb { \theta } _ { t } ^ { - } ) .
  ```
- **偏置来源（L55 逐字）**：`The max operator in standard Q-learning and DQN, in (2) and (3), uses the same values both to select and to evaluate an action. This makes it more likely to select overestimated values, resulting in overoptimistic value estimates. To prevent this, we can decouple the selection from the evaluation.`
- **Double Q-learning 目标（L66 逐字）**：
  ```latex
  Y _ { t } ^ { \mathrm { { D o u b l e Q } } } \equiv R _ { t + 1 } + \gamma Q ( S _ { t + 1 } , \operatorname* { a r g m a x } _ { a } Q ( S _ { t + 1 } , a ; \pmb { \theta } _ { t } ) ; \pmb { \theta } _ { t } ^ { \prime } ) .
  ```
- **Double DQN 目标（L108 逐字）**：
  ```latex
  Y _ { t } ^ { \mathrm { { D o u b l e D Q N } } } \equiv R _ { t + 1 } + \gamma Q ( S _ { t + 1 } , \underset { a } { \mathrm { a r g m a x } } Q ( S _ { t + 1 } , a ; \pmb { \theta } _ { t } ) , \pmb { \theta } _ { t } ^ { - } )
  ```
- **改动幅度（L112 逐字）**：`In comparison to Double Q-learning (4), the weights of the second network $\theta _ { t } ^ { \prime }$ are replaced with the weights of the target network $\pmb { \theta } _ { t } ^ { - }$ for the evaluation of the current greedy policy.`

**2) 适用条件与理论保证**

- **定理 1（L79 逐字）**：`Theorem 1. Consider a state s in which all the true optimal action values are equal at $Q _ { * } ( s , a ) = V _ { * } ( s )$ for some $V _ { * } ( s )$ Let $Q _ { t }$ be arbitrary value estimates that are on the whole unbiased in the sense that $\sum _ { a } ( Q _ { t } ( s , a ) - V _ { * } ( s ) ) = 0 ,$ but that are not all correct, such that $\frac { 1 } { m } \sum _ { a } ( Q _ { t } ( s , a ) - V _ { * } ( s ) ) ^ { 2 } = C$ for some $C > 0$ , where m $\geq 2$ is the number ofactions in s. Under these conditions, ma $\mathfrak { c } _ { a } Q _ { t } ( s , a ) \geq V _ { * } ( s ) + \sqrt { \frac { C } { m - 1 } } .$ This lower bound is tight. Under the same conditions, the lower bound on the absolute error ofthe Double Q-learning estimate is zero.`
- **定理 2（位于 L86–L102 区块内的定理陈述）**：`Theorem 2. Consider a state s in which all the true optimal action values are equal at $Q _ { * } ( s , a ) = V _ { * } ( s )$ . Suppose that the estimation errors $Q _ { t } ( s , a ) - Q _ { * } ( s , a )$ are independently distributed uniformly randomly in $[ - 1 , 1 ]$ . Then,` `$$\mathbb { E } \left[ \operatorname* { m a x } _ { a } Q _ { t } ( s , a ) - V _ { * } ( s ) \right] = \frac { m - 1 } { m + 1 }$$` —— **定理 2 的精确行号本批未 pin，引用时需复核。**
- **适用条件（关键，L75 逐字）**：`In this section we demonstrate more generally that estimation errors of any kind can induce an upward bias, regardless of whether these errors are due to environmental noise, function approximation, non-stationarity, or any other source.` —— **非平稳被明确列为产生向上偏置的来源之一。**
- **经验证据（L152 逐字）**：`Figure 3 only shows a few examples, but overestimations were observed for DQN in all 49 tested Atari games, albeit in varying amounts.`
- **保证的边界（L160 逐字）**：`Overoptimism does not always adversely affect the quality of the learned policy. For example, DQN achieves optimal behavior in Pong despite slightly overestimating the policy value.` —— **定理只保证"无偏"，不保证"策略更好"。**

**3) 迁移到 LEO 逐跳路由的条件与障碍** `[外推]`

| 轴 | 条件 | 障碍 |
|---|---|---|
| 网络级 vs 逐包决策 | 逐跳动作空间大（度 4–8）时 $m$ 大 | **原文逐字**：`More typically, the overoptimism increases with the number of actions as shown in Figure 1` → **LEO 节点度越大，DQN 的 Q 值越乐观，越容易把"看似空闲"的邻居当成好下一跳** |
| 非平稳 | 需要非平稳不制造额外的估计误差偏置 | L75 明说非平稳**是**产生向上偏置的来源；Double DQN 降偏置但**不消除非平稳本身** |
| 部分可观测 | 需要 Q 网络不因混叠产生系统性误差 | 本篇未处理（`grep -a -c -i -E "partial(ly)? observ|POMDP"` 实测 **0**）。混叠 → 估计误差 → 按定理 1 **必然**产生向上偏置 |
| 信用分配 | 与 DQN 同：单步 TD | 本篇不改信用分配（`grep -a -c -i -E "credit assignment|eligibility trace|n-step"` 实测 **0**） |

**4) 作为反例的价值**

1. **反驳「加个 Double DQN 就治好 Q 值高估」**：Double DQN 减的是**选择/评估耦合**引入的偏置；L75 逐字说明 `estimation errors of any kind can induce an upward bias`，**包括函数近似与非平稳**。
2. **反驳「过度乐观总是有害」**：L160 逐字 `Overoptimism does not always adversely affect the quality of the learned policy` —— **必须用策略质量而非 Q 值幅度来判**。
3. **反驳「动作数多没问题」**：原文逐字 `the overoptimism increases with the number of actions` —— 如果动作空间是"整条候选路径"而非"下一跳"，$m$ 会爆炸。
4. **打我们自己的点**：这篇的定理**全部假设"真值在所有动作上相等"**（$Q _ { * } ( s , a ) = V _ { * } ( s )$）。**LEO 路由里各下一跳的真值天然不等**。**我们不能直接引用定理 1 的数值来论证 LEO 的偏置**——这是本篇对"生搬结论"的反例价值。

---

### 4.3 JSX5XG88 — GAE（Schulman et al., ICLR 2016）

**1) 机制（公式逐字 + 行号）**

- **策略梯度通式（L45 逐字，eq 1）**：
  ```latex
  g = \mathbb { E } \left[ \sum _ { t = 0 } ^ { \infty } \Psi _ { t } \nabla _ { \theta } \log \pi _ { \theta } ( a _ { t } \mid s _ { t } ) \right] ,
  ```
  其 $\Psi_t$ 的 6 种取法（L47–L51 逐字）：`1. total reward of the trajectory. 2. reward following action $a _ { t }$ 3. baselined version of previous formula. 4. $Q ^ { \pi } ( s _ { t } , a _ { t } )$ : state-action value function. 5. $A ^ { \pi } ( s _ { t } , a _ { t } )$ : advantage function. 6. $r _ { t } + V ^ { \pi } ( s _ { t + 1 } ) - V ^ { \pi } ( s _ { t } )$ : TD residual.`
- **γ-just 定义（L85 逐字，Definition 1）**：`Definition 1. The estimator $\hat { A } _ { t }$ is γ-just if` `$$\begin{array} { r } { \mathbb { E } _ { a _ { 0 : \infty } } \left[ \hat { A } _ { t } ( s _ { 0 : \infty } , a _ { 0 : \infty } ) \nabla _ { \theta } \log \pi _ { \theta } ( a _ { t } \mid s _ { t } ) \right] = \mathbb { E } _ { a _ { 0 : \infty } } \left[ A ^ { \pi , \gamma } ( s _ { t } , a _ { t } ) \nabla _ { \theta } \log \pi _ { \theta } ( a _ { t } \mid s _ { t } ) \right] . } \end{array}$$`
- **k-step 优势估计（L144 逐字，eq 14）**：
  ```latex
  \hat { A } _ { t } ^ { ( k ) } : = \sum _ { l = 0 } ^ { k - 1 } \gamma ^ { l } \delta _ { t + l } ^ { V } = - V ( s _ { t } ) + r _ { t } + \gamma r _ { t + 1 } + \cdot \cdot \cdot + \gamma ^ { k - 1 } r _ { t + k - 1 } + \gamma ^ { k } V ( s _ { t + k } )
  ```
- **GAE 定义（L158 逐字，eq 16，末行即结论）**：
  ```latex
  \hat { A } _ { t } ^ { \mathrm { G A R } ( \gamma , \lambda ) } : = ( 1 - \lambda ) \bigg ( \hat { A } _ { t } ^ { ( 1 ) } + \lambda \hat { A } _ { t } ^ { ( 2 ) } + \lambda ^ { 2 } \hat { A } _ { t } ^ { ( 3 ) } + \ldots \bigg ) \quad \cdots \quad = \displaystyle \sum _ { l = 0 } ^ { \infty } ( \gamma \lambda ) ^ { l } \delta _ { t + l } ^ { V }
  ``` `[OCR: 标签印作 "GAR"，应为 "GAE"]`
- **两端特例（L166 逐字，eq 17；L170 逐字，eq 18）**：
  ```latex
  \mathrm { G A E } ( \gamma , 0 ) : \quad \hat { A } _ { t } : = \delta _ { t } \quad = r _ { t } + \gamma V ( s _ { t + 1 } ) - V ( s _ { t } )
  \mathrm { G A E } ( \gamma , 1 ) : \quad \hat { A } _ { t } : = \sum _ { l = 0 } ^ { \infty } \gamma ^ { l } \delta _ { t + l } = \sum _ { l = 0 } ^ { \infty } \gamma ^ { l } r _ { t + l } - V ( s _ { t } )
  ```
- **响应函数（L230 逐字，eq 26）**：
  ```latex
  \chi ( l ; s _ { t } , a _ { t } ) = \mathbb { E } \left[ r _ { t + l } \mid s _ { t } , a _ { t } \right] - \mathbb { E } \left[ r _ { t + l } \mid s _ { t } \right] .
  ```
- **信用分配的定量化（L233 逐字）**：`Note that $A ^ { \pi , \gamma } ( s , a ) = \sum _ { l = 0 } ^ { \infty } \gamma ^ { l } \chi ( l ; s , a )$ , hence the response function decomposes the advantage function across timesteps. The response function lets us quantify the temporal credit assignment problem: long range dependencies between actions and rewards correspond to nonzero values of the response function for $l \gg 0$`

**2) 适用条件与理论保证**

- **γ 与 λ 的分工（L176 逐字）**：`γ most importantly determines the scale of the value function $V ^ { \pi , \gamma }$ , which does not depend on λ. Taking $\gamma < 1$ introduces bias into the policy gradient estimate, regardless of the value function's accuracy. On the other hand, $\lambda < 1$ introduces bias only when the value function is inaccurate.`
- **γ-just 的充分条件（Prop 1，L99 逐字）**：`Proposition 1. Suppose that $\hat { A } _ { t }$ can be written in the form $\hat { A } _ { t } ( s _ { 0 : \infty } , a _ { 0 : \infty } ) = Q _ { t } ( s _ { t : \infty } , a _ { t : \infty } ) - b _ { t } ( s _ { 0 : t } , a _ { 0 : t - 1 } )$ such that for all $( s _ { t } , a _ { t } ) , \ \mathbb { E } _ { s _ { t + 1 : \infty } }$ ,a<sub>t+1:∞</sub> $\mid s _ { t } , a _ { t } \mid Q _ { t } ( s _ { t : \infty } , a _ { t : \infty } ) \mid \ = \ Q ^ { \pi , \gamma } ( s _ { t } , a _ { t } )$ Then $\hat { A } i s \gamma - j u s t .$`
- **奖励塑形解释（L194 逐字，eq 20）**：
  ```latex
  \tilde { r } ( s , a , s ^ { \prime } ) = r ( s , a , s ^ { \prime } ) + \gamma \Phi ( s ^ { \prime } ) - \Phi ( s ) ,
  ```
  并给出（§4 区块逐字）：`$$\sum _ { l = 0 } ^ { \infty } ( \gamma \lambda ) ^ { l } \tilde { r } ( s _ { t + l } , a _ { t } , s _ { t + l + 1 } ) = \sum _ { l = 0 } ^ { \infty } ( \gamma \lambda ) ^ { l } \delta _ { t + l } ^ { V } = \hat { A } _ { t } ^ { \mathrm { G A E } ( \gamma , \lambda ) } .$$`
- **原文自述的经验最优区间（L364 逐字）**：`As shown in our experiments, choosing an appropriate intermediate value of λ in the range [0.9, 0.99] usually results in the best performance.`
- **原文自述的开放问题（L366 逐字）**：`A possible topic for future work is how to adjust the estimator parameters γ, λ in an adaptive or automatic way.`
- **λ=0 的实测结论（A.2 节，标题在 L396；正文逐字）**：`We have found that the bias is prohibitively large when using a one-step estimate of the returns, i.e., the $\lambda = 0$ estimator, $\hat { A } _ { t } = \delta _ { t } ^ { V } = r _ { t } + \gamma V ( s _ { t + 1 } ) - V ( s _ { t } )$ .`

**3) 迁移到 LEO 逐跳路由的条件与障碍** `[外推]`

| 轴 | 条件 | 障碍 |
|---|---|---|
| 网络级 vs 逐包决策 | GAE 本质是 **on-policy** 的优势估计，需要"策略与环境交互产生轨迹" | 原文算法（L180，eq 19）只在**单条轨迹上按 t 求和**：`$\mathbb { E } \left[ \sum _ { t = 0 } ^ { \infty } \nabla _ { \theta } \log \pi _ { \theta } ( a _ { t } \mid s _ { t } ) \sum _ { l = 0 } ^ { \infty } ( \gamma \lambda ) ^ { l } \delta _ { t + l } ^ { V } \right]$`；LEO 逐包仿真里"轨迹"= 一个包的一串跳，**包与包之间环境在变** |
| 非平稳 | 需要 $V$ 的近似在 λ>0 时仍有效 | L176 逐字：`λ < 1 introduces bias only when the value function is inaccurate` —— **非平稳 → $V$ 不准 → λ<1 就有偏**；而 λ=1 又高方差 |
| 部分可观测 | $V(s_t)$ 的定义域是**状态** $s_t$ | 原文全篇用 $s_t$；`grep -a -c -i -E "partial(ly)? observ|POMDP"` 实测 **1**（L11 摘要语境，非 POMDP）。**LEO 逐跳只有局部观测，$V(s_t)$ 无处可算** |
| 信用分配 | **这正是本篇的核心**：λ 控制"往回看多远" | **条件成立**：L233 的响应函数 $\chi(l;s,a)$ 给出**可计算的判据**。**这是本篇对我们最有用的可复用机制** |

**4) 作为反例的价值**

1. **反驳「λ 可以随便调」**：L176 把 γ 与 λ 的偏置来源**分开**：γ<1 **无条件**引入偏置，λ<1 **只在 $V$ 不准时**引入偏置。
2. **反驳「单步 TD 就够」**：A.2 逐字 `the bias is prohibitively large when using a one-step estimate of the returns`。**LEO 逐跳路由若用 1 步 TD，原文实测判定为偏置不可接受。**
3. **反驳「响应函数只是理论装饰」**：L233 给出**可操作的诊断**。**我们可以直接在 LEO 仿真里测 $\chi(l)$**，这是可复用的实验设计。
4. **打我们自己的点**：GAE 是 **on-policy** 的。**若我们打算用经验回放（off-policy）来摊薄 LEO 的采样成本，GAE 的这一整套 γ-just 保证不适用**。若混用，需要 Retrace(λ)（§4.9）来补 off-policy 修正。

---

### 4.4 9FLZ88LZ — QMIX（Rashid et al., ICML 2018）

**1) 机制（公式逐字 + 行号）**

- **问题设定（L62 逐字）**：`A fully cooperative multi-agent task can be described as a Dec-POMDP (Oliehoek & Amato, 2016) consisting of a tuple $G = \langle S , U , P , r , Z , O , n , \gamma \rangle .$`；`At each time step, each agent $a \in A \equiv \{ 1 , . . . , n \}$ chooses an action $u ^ { a } \in U$ , forming a joint action $\mathbf { u } \in \mathbf { U } \equiv U ^ { n }$`
- **中心化训练/去中心化执行（L66 逐字）**：`Although training is centralised, execution is decentralised, i.e., the learning algorithm has access to all local actionobservation histories τ and global state s, but each agent's learnt policy can condition only on its own actionobservation history $\tau ^ { a }$`
- **DQN 损失（L73 逐字，eq 2）**：
  ```latex
  \mathcal { L } ( \theta ) = \sum _ { i = 1 } ^ { b } \left[ \left( y _ { i } ^ { \mathrm { D Q N } } - Q ( s , u ; \theta ) \right) ^ { 2 } \right] ,
  ```
  其中 `$y ^ { \mathrm { D Q N } } = r + \gamma \operatorname* { m a x } _ { u ^ { \prime } } Q ( s ^ { \prime } , u ^ { \prime } ; \theta ^ { - } )$`。
- **VDN 加性分解（L96 逐字，eq 3）**：
  ```latex
  Q _ { t o t } ( \tau , \mathbf { u } ) = \sum _ { i = 1 } ^ { n } Q _ { i } ( \tau ^ { i } , u ^ { i } ; \boldsymbol { \theta } ^ { i } ) .
  ```
- **QMIX 的 IGM 一致性条件（L105 逐字，eq 4）**：
  ```latex
  \underset { \mathbf { u } } { \arg \operatorname* { m a x } } Q _ { t o t } ( \pmb { \tau } , \mathbf { u } ) = \left( \begin{array} { c } { \mathrm { a r g m a x } _ { u ^ { 1 } } Q _ { 1 } ( \tau ^ { 1 } , u ^ { 1 } ) } \\ { \vdots } \\ { \mathrm { a r g m a x } _ { u ^ { n } } Q _ { n } ( \tau ^ { n } , u ^ { n } ) } \end{array} \right) .
  ```
- **单调性约束（L113 逐字，eq 5）**：
  ```latex
  \frac { \partial Q _ { t o t } } { \partial Q _ { a } } \geq 0 , \forall a \in A .
  ```
- **实现（L117–L131 逐字摘）**：`To enforce (5), QMIX represents $Q _ { t o t }$ using an architecture consisting of agent networks, a mixing network, and a set of hypernetworks`；`the weights (but not the biases) of the mixing network are restricted to be non-negative`；`Each hypernetwork takes the state s as input and generates the weights of one layer of the mixing network. Each hypernetwork consists of a single linear layer, followed by an absolute activation function, to ensure that the mixing network weights are non-negative.`
- **QMIX 损失（L134 逐字，eq 6）**：
  ```latex
  \mathcal { L } ( \boldsymbol { \theta } ) = \sum _ { i = 1 } ^ { b } \left[ \left( y _ { i } ^ { t o t } - Q _ { t o t } ( \tau , \mathbf { u } , s ; \boldsymbol { \theta } ) \right) ^ { 2 } \right] ,
  ```
  其中 `$y ^ { t o t } = r + \gamma \operatorname* { m a x } _ { \mathbf { u } ^ { \prime } } Q _ { t o t } ( \tau ^ { \prime } , \mathbf { u } ^ { \prime } , s ^ { \prime } ; \theta ^ { - } )$`。

**2) 适用条件与理论保证**

- **表示能力（L141 逐字）**：`The value function class representable with QMIX includes any value function that can be factored into a non-linear monotonic combination of the agents' individual value functions in the fully observable setting.`
- **表示能力的硬边界（L143 逐字）**：`However, the constraint in (5) prevents QMIX from representing value functions that do not factorise in such a manner. Intuitively, any value function for which an agent's best action depends on the actions of the other agents at the same time step will not factorise appropriately, and hence cannot be represented perfectly by QMIX.`
- **Dec-POMDP 下的额外崩溃（L333 逐字，附录 A.1）**：`In a Dec-POMDP, QMIX cannot necessarily represent the value function. This is because each agent's observations are no longer the full state, and thus they might not be able to distinguish the true state given their local observations. If the agent's value function ordering is then wrong, i.e., $Q _ { a } ( \tau ^ { a } , u ) > Q _ { a } ( \tau ^ { a } , u ^ { \prime } )$ when $Q _ { t o t } ( s _ { t } , ( \mathbf { u } ^ { - a } , u ) ) < Q _ { t o t } ( s _ { t } , ( \mathbf { u } ^ { - a } , u ^ { \prime } ) )$ , then the mixing network would be unable to correctly represent $Q _ { t o t }$ given the monotonicity constraints.`
- **IQL 的非平稳（L82 逐字）**：`This approach does not address the nonstationarity introduced due to the changing policies of the learning agents, and thus, unlike Q-learning, has no convergence guarantees even in the limit of infinite exploration.`
- **信用分配：QMIX 显式的对手是 COMA（L52 逐字）**：`COMA (Foerster et al., 2018) uses a centralised critic to train decentralised actors, estimating a counterfactual advantage function for each agent in order to address multi-agent credit assignment.`
- **原文自述的下一步（L251 逐字）**：`In the longer term, we aim to complement QMIX with more coordinated exploration schemes for settings with many learning agents.`

**3) 迁移到 LEO 逐跳路由的条件与障碍** `[外推]`

| 轴 | 条件 | 障碍 |
|---|---|---|
| 网络级 vs 逐包决策 | 智能体数 $n$ = 卫星数；联合动作 $\mathbf{u} \in U^n$ | **致命**：(eq 4) 的一致性使 $Q_{tot}$ 的 argmax **线性时间可解**（L136 逐字：`we can perform the maximisation of $Q _ { t o t }$ in time linear in the number of agents (as opposed to scaling exponentially in the worst case)`），但**这要求所有智能体在同一时刻决策**。**LEO 逐包路由是异步事件驱动的**——原文假设同步时间步（L62） |
| 非平稳 | 中心化训练可缓解（L48 逐字：`centralised learning of joint actions can naturally handle coordination problems and avoids nonstationarity, but is hard to scale, as the joint action space grows exponentially in the number of agents`） | **LEO 星座规模（数千颗）使联合动作空间 $U^n$ 完全不可用** |
| 部分可观测 | QMIX 用 DRQN（L86 逐字）：`in partially observable settings, agents can benefit from conditioning on their entire action-observation history` | 但 L333 逐字：**Dec-POMDP 下单调分解可能根本表示不了最优 $Q_{tot}$** |
| 信用分配 | **本篇的核心问题**：把团队回报分摊到每个 agent | **条件接近成立**：LEO 里"端到端时延/丢包"正是**共享的团队奖励**。**但有硬边界**：单调性约束（eq 5）要求**任一 agent 的动作变好，全局 Q 不能变差**。LEO 里这**不成立**——上游把包推给下游，下游排队变差，全局时延反而恶化（**拥塞转移**）。这正是 L143 描述的情形 |

**4) 作为反例的价值**

1. **直接反驳「用 QMIX 做 LEO 多星协同路由」**：L143 + L333 给出**双层否证**：① 若失败模式是"拥塞转移"，**单调分解表示不了**；② 若观测是局部的（LEO 必然），**连表示的前提都可能不成立**。
2. **反驳「中心化训练能解决非平稳」**：L48 承认中心化能避免非平稳，但代价是 `the joint action space grows exponentially in the number of agents`。
3. **反驳「单靠共享标量奖励就能做多星信用分配」**：L52 表明主流替代是**反事实基线（COMA）**，而 COMA 需要**逐 agent 的反事实回报**。**如果我们只有"这个包丢了"这一个标量信号，连反事实都构造不出来** —— 与 G-A 的动机一致。
4. **正面反例（借力）**：eq 5 的单调性约束 + hypernetwork 条件化是**可迁移的结构**。**代价是必须证明拥塞转移不破坏单调性——这可以直接被 L143 反驳，是一个干净的证伪设计。**

---

### 4.5 I2WH9RRR — Asymmetric DQN（Baisero, Daley & Amato, 2022）

**1) 机制（公式逐字 + 行号）**

- **POMDP 定义（L37 逐字）**：`A partially observable Markov decision process (POMDP) is a discrete-time control problem represented by tuple $\langle S , A , \mathcal { O } , b _ { 0 } , T , O , R , \gamma \rangle$`
- **历史空间与回报函数（L39 逐字）**：`The history space $\mathcal { H } \doteq ( \mathcal { A } \times \mathcal { O } ) ^ { * }$ represents such sequences. To simplify notation, we overload symbol R to also denote the expected reward function on histories $R ( h , a ) \doteq \mathbb { E } _ { s \mid h } \left[ R ( s , a ) \right]$`
- **历史值 Bellman 方程（L43 逐字，eq 1）**：
  ```latex
  Q ^ { \pi } ( h , a ) = R ( h , a ) + \gamma \mathbb { E } _ { o | h , a } \left[ Q ^ { \pi } ( h a o , \pi ( h a o ) ) \right]
  ```
- **最优性方程（L47 逐字，eq 2）**：
  ```latex
  Q ^ { * } ( h , a ) = R ( h , a ) + \gamma \mathbb { E } _ { o | h , a } \left[ \operatorname* { m a x } _ { a ^ { \prime } } Q ^ { * } ( h a o , a ^ { \prime } ) \right]
  ```
- **历史-状态值函数（L73 逐字，eq 4）**：
  ```latex
  \begin{array} { r } { U ^ { \pi } ( h , s , a ) = R ( s , a ) + \gamma \mathbb { E } _ { s ^ { \prime } , o \mid s , a } \left[ U ^ { \pi } ( h a o , s ^ { \prime } , \pi ( h a o ) ) \right] . } \end{array}
  ```
- **$U$ 与 $Q$ 的关系（L77 逐字，eq 5）**：
  ```latex
  \begin{array} { r } { Q ^ { \pi } ( h , a ) = \mathbb E _ { s \left| h \right. } \left[ U ^ { \pi } ( h , s , a ) \right] . } \end{array}
  ```
- **核心否定性事实（L79 逐字）**：`Among other things, this means that an optimal partially observable policy cannot be recovered by maximizing $U ^ { * } , \mathrm { i . e . } .$ , generally, there is no guarantee that $\pi ^ { * } ( h ) = \operatorname { a r g m a x } _ { a } U ^ { * } ( h , s , a )$ for any given value of s.`
- **互一致定义（§3.4 区块，Definition 3.4 逐字）**：`We say that functions Q and U are mutually consistent iff $Q = E U$ holds.`
- **ADQN 双损失（L261 / L265 逐字，eq 16 / eq 17）**：
  ```latex
  \mathcal { L } _ { \hat { U } } = \left( r + \gamma \operatorname { S G } \left[ \hat { U } ( h a o , s ^ { \prime } , \hat { \pi } ( h a o ) ) \right] - \hat { U } ( h , s , a ) \right) ^ { 2 } .
  \mathcal { L } _ { \hat { Q } } = \left( r + \gamma \operatorname { S G } \left[ \hat { U } ( h a o , s ^ { \prime } , \hat { \pi } ( h a o ) ) \right] - \hat { Q } ( h , a ) \right) ^ { 2 } ;
  ```
- **共享目标的机制说明（L267 逐字）**：`It is worth noting that $\mathcal { L } _ { \hat { U } }$ and $\mathcal { L } _ { \hat { Q } }$ use the same target to train $\hat { U }$ and $\hat { Q } .$ The crucial difference is that $\hat { U }$ is in able to model the target as a function of $s ,$ while $\hat { Q }$ is unable to do so, and can at only model the expectation of the target over values of $s .$ In a way, these losses approximately enforce a "loose" form of mutual consistency $\hat { Q } \approx E \hat { U } .$`
- **训练构造（L269–L272 逐字）**：`The total loss $\mathcal { L } _ { \hat { U } } + \mathcal { L } _ { \hat { Q } }$ can be jointly minimized with respect to the parameters by a single backpropagation step`；`each POMDP transition $( h , s , a , r , s ^ { \prime } , o )$ is deferred to a first-in first-out replay memory`
- **变体损失（L282 / L284 逐字，eq 18 / eq 19）**：
  ```latex
  \mathcal { L } _ { \hat { U } } = \left( r + \gamma \operatorname { S G } \left[ \hat { U } ( h a o , s ^ { \prime } , \hat { \pi } ( h a o ) ) \right] - \hat { U } ( h , s , a ) \right) ^ { 2 } ,
  \mathcal { L } _ { \hat { Q } } = \left( \operatorname { S G } \left[ \hat { U } ( h , s , a ) \right] - \hat { Q } ( h , a ) \right) ^ { 2 } .
  ```

**2) 适用条件与理论保证**

- **表格型下**：Theorem 4.1（API）、Theorem 4.3（AAVI）、Theorem 4.4（AQL）给出最优收敛。AQL 的步长条件（L245 逐字）：`Assume stepsizes $\alpha _ { k }$ satisfying the following asymptotic conditions,` `$$\sum _ { k = 0 } ^ { \infty } \alpha _ { k } = \infty , \qquad \sum _ { k = 0 } ^ { \infty } \alpha _ { k } ^ { 2 } < \infty .$$`
- **函数近似下保证失效（L254 逐字）**：`The use of approximation sacrifices the optimal convergence guarantee established by Theorem 4.4, but is necessary to scale algorithms to significantly more challenging partially observable environments.`
- **ADQN 为何有效（L302 逐字）**：`In ADQN, the issues associated with learning a proper history representation are alleviated by the fact that its training is bootstrapped not only on the history representation itself, but also on the state representation. Even when the history representation is poor, we can expect the state representation to contain sufficient contextual information to allow $\hat { U } ( \phi ( h ) , \phi ( s ) , \cdot )$ to model meaningful values`
- **state-only 变体的警告（L296 逐字）**：`Some prior work in asymmetric RL has adopted heuristic forms of asymmetry which uses state-only (i.e., history-less) value functions $U ( s , a )$ . Such form of asymmetry is however associated with fundamental theoretical issues which may severely compromise the learning performance, ranging from potentially being ill-defined, to introducing bias into the learning process`
- **经验结果（L352 逐字）**：`the stateonly variants fail to outperform even the DQN baseline in most environments (with a single exception discussed later)`
- **原文自述局限（L368 逐字）**：`Future work may focus on extending ADQN to the multi-agent control case, which poses further learning challenges`

**3) 迁移到 LEO 逐跳路由的条件与障碍** `[外推]`

| 轴 | 条件 | 障碍 |
|---|---|---|
| 网络级 vs 逐包决策 | 需要"训练时可访问特权状态 $s$、执行时只能用历史 $h$" | **这个条件在 LEO 仿真里天然成立**：仿真器**知道**全局队列/拓扑真值，而路由器**只知道**本地观测。**ADQN 是本批 11 篇中与 LEO 逐跳路由结构化最贴合的一篇** |
| 非平稳 | 需要 $\hat U(h,s,a)$ 在 $s$ 突变时仍提供有意义的值 | $U$ 把 $s$ 当**输入特征**（L267），$s$ 突变 → $\hat U$ 输入分布漂移 → 与所有函数近似方法同病。**原文未处理非平稳**（`grep -a -c -i -E "non-?stationar"` 实测 **0**） |
| 部分可观测 | **本篇的全部内容** | **条件完全成立且是设计目标**。但代价明确：训练需要 $(h, s, a, r, s', o)$ **六元组**（L272），即**每条经验都要记录特权状态 $s$**。LEO 仿真可行，**真实星座不可行** |
| 信用分配 | 需要把端到端回报归到跳 | **本篇不解决**：它只处理"观测不全"下的值估计（$Q(h,a) = E_{s\|h}[U(h,s,a)]$），**奖励仍是单一标量 $r$，没有按失败原因分解**（`grep -a -c -i -E "credit assignment"` 实测 **0**） |

**4) 作为反例的价值**

1. **反驳「部分可观测可以用 state-only 的非对称糊过去」**：L296 + L352 明确说 state-only 变体 `associated with fundamental theoretical issues`，且 `fail to outperform even the DQN baseline in most environments`。
2. **反驳「非对称保证最优」**：L254 逐字 `The use of approximation sacrifices the optimal convergence guarantee`。**Theorem 4.4 的最优性只在表格型下成立**。
3. **反驳「历史表示学不好就没救」**：L302 给出**唯一一条被论述有效的补偿路径**（用状态表示 bootstrap 历史表示）。**这是可复用的正面机制**。
4. **打我们自己的点**：L79 逐字 `an optimal partially observable policy cannot be recovered by maximizing $U ^ { * }$`。**若我们打算"训练一个看全局状态的 oracle 再蒸馏出路由策略"，这篇直接否证该路线**。

---

### 4.6 FGQSH4AI — MADDPG（Lowe et al., NeurIPS 2017）

**1) 机制（公式逐字 + 行号）**

- **约束（L97 逐字）**：`we would like to operate under the following constraints: (1) the learned policies can only use local information (i.e. their own observations) at execution time, (2) we do not assume a differentiable model of the environment dynamics`
- **随机策略梯度（L111 逐字，eq 4）**：
  ```latex
  \begin{array} { r } { \nabla _ { \theta _ { i } } J ( \theta _ { i } ) = \mathbb { E } _ { s \sim p ^ { \mu } , a _ { i } \sim \pi _ { i } } [ \nabla _ { \theta _ { i } } \log \pi _ { i } ( a _ { i } | o _ { i } ) Q _ { i } ^ { \pi } ( \mathbf { x } , a _ { 1 } , . . . , a _ { N } ) ] . } \end{array}
  ```
- **确定性策略梯度（L119 逐字，eq 5）**：
  ```latex
  \nabla _ { \theta _ { i } } J ( \pmb \mu _ { i } ) = \mathbb { E } _ { \mathbf { x } , a \sim \mathcal { D } } [ \nabla _ { \theta _ { i } } \pmb { \mu } _ { i } ( a _ { i } | o _ { i } ) \nabla _ { a _ { i } } Q _ { i } ^ { \mu } ( \mathbf { x } , a _ { 1 } , . . . , a _ { N } ) | _ { a _ { i } = \pmb { \mu } _ { i } ( o _ { i } ) } ] ,
  ```
- **集中式 critic 的损失（L125 逐字，eq 6）**：
  ```latex
  \begin{array} { r } { \mathcal { L } ( \boldsymbol { \theta } _ { i } ) = \mathbb { E } _ { \mathbf { x } , a , r , \mathbf { x } ^ { \prime } } [ ( Q _ { i } ^ { \mu } ( \mathbf { x } , a _ { 1 } , \dots , a _ { N } ) - y ) ^ { 2 } ] , \quad y = r _ { i } + \gamma Q _ { i } ^ { \mu ^ { \prime } } ( \mathbf { x } ^ { \prime } , a _ { 1 } ^ { \prime } , \dots , a _ { N } ^ { \prime } ) \big | _ { a _ { j } ^ { \prime } = \mu _ { j } ^ { \prime } ( o _ { j } ) } , } \end{array}
  ```
- **非平稳消解的机制核心（L130 逐字）**：`A primary motivation behind MADDPG is that, if we know the actions taken by all agents, the environment is stationary even as the policies change, since $P ( s ^ { \prime } { \mid } s , a _ { 1 } , . . . , a _ { N } , \pi _ { 1 } , . . . , \pi _ { N } ) = P ( s ^ { \prime } | s , a _ { 1 } , . . . , a _ { N } ) = P ( s ^ { \prime } | s , a _ { 1 } , . . . , a _ { N } , \pmb { \pi } _ { 1 } ^ { \prime } , . . . , \pmb { \pi } _ { N } ^ { \prime } )$ for any $\pmb { \pi } _ { i } \neq \pmb { \pi } _ { i } ^ { \prime }$ . This is not the case if we do not explicitly condition on the actions of other agents, as done for most traditional RL methods.`
- **策略推断（L136 逐字，eq 7）**：
  ```latex
  \mathcal { L } ( \phi _ { i } ^ { j } ) = - \mathbb { E } _ { o _ { j } , a _ { j } } \left[ \log \hat { \pmb { \mu } } _ { i } ^ { j } ( a _ { j } | o _ { j } ) + \lambda H ( \hat { \pmb { \mu } } _ { i } ^ { j } ) \right] ,
  ```
  并（L138 逐字）`With the approximate policies, y in Eq. 6 can be replaced by an approximate value $\hat { y }$`，`$$\hat { y } = r _ { i } + \gamma Q _ { i } ^ { \pmb { \mu } ^ { \prime } } ( \mathbf { x } ^ { \prime } , \hat { \pmb { \mu } } _ { i } ^ { \prime 1 } ( o _ { 1 } ) , \dots , \pmb { \mu } _ { i } ^ { \prime } ( o _ { i } ) , \dots , \hat { \pmb { \mu } } _ { i } ^ { \prime N } ( o _ { N } ) ) ,$$`
- **策略集成（L158 逐字，eq 9）**：
  ```latex
  \nabla _ { \theta _ { i } ^ { ( k ) } } J _ { e } ( \mu _ { i } ) = \frac { 1 } { K } \mathbb { E } _ { \mathbf { x } , a \sim \mathcal { D } _ { i } ^ { ( k ) } } \left[ \nabla _ { \theta _ { i } ^ { ( k ) } } \mu _ { i } ^ { ( k ) } ( a _ { i } | o _ { i } ) \nabla _ { a _ { i } } Q ^ { \mu _ { i } } \left( \mathbf { x } , a _ { 1 } , \dots , a _ { N } \right) \Big | _ { a _ { i } = \mu _ { i } ^ { ( k ) } ( o _ { i } ) } \right] .
  ```
- **算法全文**：L334 起，`Algorithm 1: Multi-Agent Deep Deterministic Policy Gradient for N agents`，动作探索为 `$a _ { i } = \pmb { \mu } _ { \theta _ { i } } ( o _ { i } ) + \mathcal { N } _ { t }$`，target 软更新为 `$\theta _ { i } ^ { \prime } \to \tau \theta _ { i } + ( 1 - \tau ) \theta _ { i } ^ { \prime }$`。

**2) 适用条件与理论保证**

- **适用条件（L132 逐字）**：`Note that we require the policies of other agents to apply an update in Eq. 6. Knowing the observations and policies of other agents is not a particularly restrictive assumption ... However, we can relax this assumption if necessary by learning the policies of other agents from observations`
- **理论保证：本篇正文未给任何收敛性定理**。在已读区间（L95–162、L238–247、L328–355）内**未见定理或收敛性陈述**。作者的定位是经验性的（L21 摘要逐字：`We show the strength of our approach compared to existing methods in cooperative as well as competitive scenarios`）。
- **原文明说的非平稳根因（L61 逐字）**：`because agents are independently updating their policies as learning progresses, the environment appears non-stationary from the view of any one agent, violating Markov assumptions required for convergence of Q-learning. Another difficulty observed in [9] is that the experience replay buffer cannot be used in such a setting since in general, $P ( s ^ { \prime } | s , a , \pmb { \pi } _ { 1 } , . . . , \pmb { \pi } _ { N } ) \neq P ( s ^ { \prime } | s , a , \pmb { \pi } _ { 1 } ^ { \prime } , . . . , \pmb { \pi } _ { N } ^ { \prime } )$ when any $\pmb { \pi } _ { i } \neq \pmb { \pi } _ { i } ^ { \prime }$`
- **原文自述的最大局限（L240 逐字）**：`One downside to our approach is that the input space of Q grows linearly (depending on what information is contained in x) with the number of agents N. This could be remedied in practice by, for example, having a modular Q function that only considers agents in a certain neighborhood of a given agent. We leave this investigation to future work.`

**3) 迁移到 LEO 逐跳路由的条件与障碍** `[外推]`

| 轴 | 条件 | 障碍 |
|---|---|---|
| 网络级 vs 逐包决策 | critic 输入 $\mathbf{x}$ 含**所有 agent 的动作** $a_1,\dots,a_N$ | **致命**：L240 逐字，输入维度**随 $N$ 线性增长**；LEO $N$ = 星座卫星数（10³ 量级）。作者自己提出的补救（只考虑邻域）**未实现，留作 future work** |
| 非平稳 | 需要"知道所有 agent 的动作就恢复平稳" | L130 的等式在**执行时**不成立：MADDPG 执行时只用 $o_i$，critic 的平稳性**只存在于训练**。**LEO 里卫星随时可能失联，$a_j$ 在训练时也未必可得** |
| 部分可观测 | 执行时可只用 $o_i$（L97 约束 1） | critic 需要 $\mathbf x = (o_1,\dots,o_N)$（L115 逐字：`In the simplest case, x could consist of the observations of all agents, $\mathbf { x } = \left( o _ { 1 } , . . . , o _ { N } \right)$`）—— **训练期需要全网观测** |
| 信用分配 | 每个 agent 有**自己的** critic 和**自己的**奖励 $r_i$ | **这正是与 LEO 的结构差异**：MADDPG 允许 `arbitrary reward structures, including conflicting rewards`（L113 逐字：`Since each $Q _ { i } ^ { \pi }$ is learned separately, agents can have arbitrary reward structures, including conflicting rewards in a competitive setting`）。**LEO 目标是全局的** —— **MADDPG 的"每 agent 独立奖励"设置反而不能直接表达"共同的失败原因"** |

**4) 作为反例的价值**

1. **反驳「CTDE 在 LEO 星座规模上可扩展」**：L240 逐字 `the input space of Q grows linearly ... with the number of agents N`，且补救方案**只是 future work**。
2. **反驳「多智能体路由需要每个卫星有自己的奖励」**：MADDPG 的强项是**允许冲突奖励**（L113）。**LEO 路由的目标是全局的**，用 MADDPG 反而要人为给每颗星编一个局部奖励 —— **这会把"同一个失败事件"再拆成 N 个互不相关的标量**，与 G-A 的方向相反。**这是本篇作为"反面设计"的价值**。
3. **反驳「策略集成能治非平稳」**：L158 的 ensemble 只在**每个 episode 随机选一个子策略**（L156 逐字：`At each episode, we randomly select one particular sub-policy for each agent to execute`）。**它治的是"对其他 agent 策略的过拟合"，不是外生非平稳**。
4. **正面反例（借力）**：L61 给出**经验回放在多智能体下失效的精确条件**：$P(s'|s,a,\pi_1..\pi_N) \neq P(s'|s,a,\pi_1'..\pi_N')$。**这个不等式在 LEO 里逐字成立** → **直接移植 MADDPG 的回放池会踩这个坑**。

---

### 4.7 KPUZIMU5 — MAPPO（Yu et al., NeurIPS 2022）

**1) 机制（公式逐字 + 行号）**

- **问题设定（L41 逐字）**：`We study decentralized partially observable Markov decision processes (DEC-POMDP) with shared rewards. A DEC-POMDP is defined by $\langle \mathcal { S } , \mathcal { A } , O , R , \bar { P } , n , \gamma \rangle$ .`
- **共享回报目标（L43 逐字）**：`Agents use a policy $\pi _ { \boldsymbol { \theta } } ( a _ { i } | \boldsymbol { o } _ { i } )$ parameterized by θ to produce an action $a _ { i }$ from the local observation $o _ { i }$ and jointly optimize the discounted accumulated reward $J ( \theta ) = \mathbb { E } _ { A ^ { t } , s ^ { t } } \left[ \sum _ { t } \gamma ^ { t } R ( s ^ { t } , A ^ { t } ) \right]$`
- **MAPPO vs IPPO（L45 逐字）**：`$V _ { \phi } ( s )$ is used for variance reduction and is only utilized during training; hence, it can take as input extra global information not present in the agent's local observation, allowing PPO in multi-agent domains to follow the CTDE structure. For clarity, we refer to PPO with centralized value function inputs as MAPPO (Multi-Agent PPO), and PPO with local inputs for both the policy and value function as IPPO (Independent PPO).`
- **actor 目标（L267 逐字）**：`The actor network is trained to maximize the objective`
  `$$L ( \theta ) { = } [ \frac { 1 } { B n } \sum _ { i = 1 } ^ { B } \sum _ { k = 1 } ^ { n } \operatorname* { m i n } ( r _ { \theta , i } ^ { ( k ) } A _ { i } ^ { ( k ) } , \mathrm { c l i p } ( r _ { \theta , i } ^ { ( k ) } , 1 - \epsilon , 1 + \epsilon ) A _ { i } ^ { ( k ) } ) ] + \sigma \frac { 1 } { B n } \sum _ { i = 1 } ^ { B } \sum _ { k = 1 } ^ { n } S [ \pi _ { \theta } ( o _ { i } ^ { ( k ) } ) ) ]$$`
  其中 `$\begin{array} { r } { r _ { \theta , i } ^ { ( k ) } = \frac { \pi _ { \theta } ( a _ { i } ^ { ( k ) } | o _ { i } ^ { ( k ) } ) } { \pi _ { \theta _ { o l d } } ( a _ { i } ^ { ( k ) } | o _ { i } ^ { ( k ) } ) } . ~ A _ { i } ^ { ( k ) } } \end{array}$ is computed using the GAE method, S is the policy entropy, and σ is the entropy coefficient hyperparameter.`
- **critic 损失（L289 逐字）**：`The critic network is trained to minimize the loss function`
  `$$L ( \phi ) = \frac { 1 } { B n } \sum _ { i = 1 } ^ { B } \sum _ { k = 1 } ^ { n } ( \operatorname* { m a x } [ ( V _ { \phi } ( s _ { i } ^ { ( k ) } ) - \hat { R } _ { i } ) ^ { 2 } , ( \operatorname { c l i p } ( V _ { \phi } ( s _ { i } ^ { ( k ) } ) , V _ { \phi _ { o u l } } ( s _ { i } ^ { ( k ) } ) - \varepsilon , V _ { \phi _ { o u l } } ( s _ { i } ^ { ( k ) } ) + \varepsilon ) - \hat { R } _ { i } ) ^ { 2 } ] ,$$`
  `[OCR: "V_{\phi_{oul}}" 应为 "V_{\phi_{old}}"]`；`where $\hat { R } _ { i }$ is the discounted reward-to-go.`
- **参数共享（L51 逐字）**：`In benchmark environments with homogeneous agents (i.e. agents have identical observation and action spaces), we utilize parameter sharing`
- **GAE（L53 逐字）**：`We also adopt common practices in implementing PPO, including Generalized Advantage Estimation (GAE) [29] with advantage normalization and valueclipping.`
- **死亡掩码（L337 逐字，C.3 标题）**：`Death Masking`；L344：`Justification of Death Masking Let $\mathbf { 0 } _ { a }$ be a zero vector with agent a's agent ID...` —— **把"该 agent 已死"这一状态在输入/损失中显式屏蔽**，是本批与本项目最接近"结构化屏蔽"的机制。

**2) 适用条件与理论保证**

- **无新定理**：本篇是**经验性再评估**，非新算法。原文自述（L216 逐字）：`This work demonstrates that PPO, an on-policy policy gradient RL algorithm, achieves strong results in both final returns and sample efficiency that are comparable to the state-of-the-art methods on a variety of cooperative multi-agent challenges, which suggests that properly configured PPO can be a competitive baseline for cooperative MARL tasks.`
- **五条超参发现（原文自加粗的 Suggestion）**：
  - L133 逐字：`We find that using value normalization never hurts training and often improves the final performance of MAPPO significantly.` → `Suggestion 1: Utilize value normalization to stabilize value learning.`
  - L159 逐字：`Suggestion 2: When available, include both local, agent-specific features and global features in the value function input. Also check that these features do not unnecessarily increase the input dimension.`
  - L172 逐字：`in multi-agent domains, MAPPO's performance degrades when samples are re-used too often. Thus, we use 15 epochs for easy tasks, and 10 or 5 epochs for difficult tasks. We hypothesize that this pattern could be a consequence of non-stationarity in MARL` → `Suggestion 3: Use at most 10 training epochs on difficult environments and 15 training epochs on easy environments. Additionally, avoid splitting data into mini-batches.`
  - L192 逐字：`we hypothesize that policy and value clipping can limit the non-stationarity which is a result of the agents' policies changing during training` → `Suggestion 4: For the best PPO performance, maintain a clipping ratio under 0.2`
  - L214 逐字：`Suggestion 5: Utilize a large batch size to achieve best task performance with MAPPO. Then, tune the batch size to optimize for sample-efficiency.`
- **非平稳的处理方式（关键）**：本篇**不解析非平稳，而是用"限制每次更新策略变化幅度"来压制它**（L172、L192）。**这是启发式的，原文自己用的是 "we hypothesize"。**

**3) 迁移到 LEO 逐跳路由的条件与障碍** `[外推]`

| 轴 | 条件 | 障碍 |
|---|---|---|
| 网络级 vs 逐包决策 | MAPPO 是 **on-policy 批式**：采一批轨迹→更新→丢掉 | L168 逐字：`PPO samples a batch of on-policy trajectories ... the accumulation of the batch is constrained by the amount of available compute and memory`。**LEO 逐包仿真里"一批轨迹"= 一批包的完整路径；包连续到达，没有天然的 episode 边界** |
| 非平稳 | 用 clip（ε<0.2）+ 少 epoch 压制 | **原文自己的假设（L172/L192）是 "we hypothesize"**，不是定理。且 L192 明说 clip 只能**限制**（`limit`），不能消除 |
| 部分可观测 | **MAPPO 的核心设计就是非对称 critic**（L45） | **条件良好**。但 L147 逐字指出取值风险：`using the CL state, which is much higher dimensional than the other global states, is ineffective, particularly in maps with many agents` —— **LEO 星座规模下，把全局状态直接拼接进 critic 会重蹈 CL state 的覆辙** |
| 信用分配 | actor 更新用 $A_i^{(k)}$（per-agent 优势） | **条件成立且是原文做法**（L267 的损失对 $i=1..B$、$k=1..n$ 双层求和）。**但每 agent 的优势来自同一个共享 $V_\phi(s)$ 与同一个共享 $R$**，**没有按失败原因分通道**（`grep -a -c -i -E "credit assignment|reward decompos"` 实测 **0**） |

**4) 作为反例的价值**

1. **反驳「必须用 off-policy 才能省样本」**：L216 逐字 `properly configured PPO can be a competitive baseline`。
2. **反驳「超参是次要的」**：整篇结论就是**同一算法在五组超参下的表现差异巨大**（L172 逐字：`when using 4 mini-batches, MAPPO fails to solve any of the selected maps while using 1 mini-batch produces the best performance on 22/23 maps`）。**任何 LEO 路由算法报告若不做同等的超参敏感性分析，其"效果好"的证据强度不足。**
3. **反驳「多智能体就是给每个 agent 一个独立优势就行」**：本篇用**共享** $V_\phi(s)$ + **共享** $R$ + per-agent advantage。**这是"共享一个标量回报"路线的最强版本**。**若我们的主张是"必须按失败原因分通道才能做信用分配"，MAPPO 就是最好的反驳者——我们必须证明在 LEO 里共享标量回报确实不够。** 这是本篇对我们最硬的挑战。
4. **正面机制（可复用）**：**Death Masking（L337）**。LEO 里卫星/链路失效时，"某些动作不可用"与"某些 agent 不参与"可以直接照搬这套屏蔽做法。

---

### 4.8 6C843JTS — Learning to Predict by the Methods of Temporal Differences（Sutton, 1988）

> **完成度警告**：本篇是本批完成度最低的一篇，**§4 理论主体（L241–487）未读**。以下理论保证部分**只基于 L196–240 的引论段与 L608–648 的附录定理陈述**，**不足以支撑收敛速度、学习率最优性等细节结论**。

**1) 机制（公式逐字 + 行号）**

- **TD(λ) 更新（L121 逐字，eq 4）**：
  ```latex
  \Delta \boldsymbol { w } _ { t } = \alpha ( P _ { t + 1 } - P _ { t } ) \sum _ { k = 1 } ^ { t } \lambda ^ { t - k } \nabla _ { \boldsymbol { w } } P _ { k } .
  ```
- **λ=1 的等价性（L125 逐字）**：`Note t h a t for λ = 1 tills is equivalent to (3), the TD implementation of the prototypical supervised-learning method. Accordingly, we call this new procedure TD(λ) and we will refer to the procedure given by (3) as TD(1).` `[OCR: "tills" 应为 "this"]`
- **资格迹的增量递推（L127–L133 逐字）**：
  ```latex
  \begin{array} { r c l } { \displaystyle e _ { t + 1 } } & { = } & { \displaystyle \sum _ { k = 1 } ^ { t + 1 } \lambda ^ { t + 1 - k } \nabla _ { w } P _ { k } } \\ & & { = } & { \displaystyle \nabla _ { w } P _ { t + 1 } + \sum _ { k = 1 } ^ { t } \lambda ^ { t + 1 - k } \nabla _ { w } P _ { k } } \\ & { = } & { \displaystyle \nabla _ { w } P _ { t + 1 } + \lambda e _ { t } . } \end{array}
  ```
- **TD(0) 特例（L133 逐字）**：
  ```latex
  \Delta \boldsymbol { w } _ { t } = \alpha ( P _ { t + 1 } - P _ { t } ) \nabla _ { \boldsymbol { w } } P _ { t } .
  ```
- **与监督学习的唯一差别（L133 逐字）**：`The two equations are identical except that the actual outcome z in (2) is replaced by the next prediction $P _ { t + 1 }$ in the equation above.`
- **结构化 vs 时序化信用分配的划分（L488 逐字）**：`The purt)ose of bolh backprot)agation and TD methods is accurate credit assignment. ... Backpropagation addresses a ,slr\~u:tural ('re(iil-assignment issue whereas TD metho(ts ad(lr(,ss a temporal cr,;dit-asslgnuient issue.` `[OCR 严重损坏，语义可辨：structural credit-assignment vs temporal credit-assignment]`
- **与 bucket brigade 的对照（L500 逐字）**：`The most important of these is that the bucket brigade assigns credit based on the rules that cau,sed other rules to become active, whereas T D methods assign credit based solely on temporal succession.` —— **TD 只用"时间先后"分配信用，不用"因果关系"。**

**2) 适用条件与理论保证**

- **保证的对象（L200 逐字）**：`The theory presented here is for data sequences generated by absorbing Markov procea\~e8 such as the random-walk process`——**只对吸收马尔可夫过程**。
- **保证的范围（L196 逐字）**：`Tile theory developed here concerns the linear TD(0) procedure and a class of tasks typified by the random walk example` —— **只对线性 TD(0)**；**TD(λ) 在本文中没有收敛定理**。
- **原文自述的理论空白（L198 逐字，极重要）**：`"Bootstrapping" in this way may be what makes TD methods efficient, but it can also make them difficult to analyze and to have confidence in. In fact, hitherto no TD method has ever been proved stable or convergent to the correct predictions.` —— **1988 年写作时，TD 方法一个稳定性证明都没有。**
- **Theorem 2（L608–L648 附录区块内的定理陈述）**：`T h e o r e m 2 For any absorbing Markov chain, for any distribution of starting probabilities $\mu _ { i }$ for any outcome distributions with finite expected values $\bar { z } _ { j { \mathrm { : } } }$ and for any linearly independent set of observation vectors $\{ \mathbf { x } _ { i } \ \} \ i \in N \}$ there exists an $\epsilon > 0$ such that, for all positive $\alpha \ < \ \epsilon$ and for any initial weight vector, the predictions of linear $T \bar { D ( \theta ) }$ (with weight updates after each sequence) converge in expected value to the ideal predictions (5).` `[Theorem 2 的精确行号本批未 pin，引用需复核]`
- **原文自述的收益定位（L532 逐字）**：`Overall, TD methods appear to be computationally cheaper and to learn faster than conventional approaches to prediction learning.`

**3) 迁移到 LEO 逐跳路由的条件与障碍** `[外推]`

| 轴 | 条件 | 障碍 |
|---|---|---|
| 网络级 vs 逐包决策 | TD(λ) 是**预测**方法，不是控制方法 | 原文标题即 `Learning to Predict`；**它预测的是"从状态 i 出发到终止的期望结果"，不是选下一跳**。要用在 LEO 路由上，必须先把它嵌进 actor-critic 或 Q-learning 的值估计里 |
| 非平稳 | 需要吸收马尔可夫过程 | L200 逐字：理论只对 `absorbing Markov procea\~e8` 成立。**LEO 的会话有终止（包到达），这一点勉强满足；但拓扑动态使转移概率本身随时间变**，原文未覆盖 |
| 部分可观测 | **本篇完全不涉及** | `grep -a -c -i -E "partial(ly)? observ|POMDP"` 实测 **0**。观测向量 $\mathbf{x}_i$ 直接对应**非终止状态 i** —— **状态是完全可观测的** |
| 信用分配 | **这是本篇的历史贡献**：资格迹 $e_{t+1} = \nabla_w P_{t+1} + \lambda e_t$ 把"多久以前的预测要改"参数化 | **条件成立**：这一条递推式**可直接搬到 LEO 逐跳**。$\lambda$ 控制回溯多少跳；$e_t$ 只需常数内存增量更新，适合逐包在线运行 |

**4) 作为反例的价值**

1. **反驳「TD 类方法有收敛保证」**：L198 逐字 `hitherto no TD method has ever been proved stable or convergent to the correct predictions`。**TD 的收敛性是被后来补上的，且依赖线性 + 独立特征 + 吸收马尔可夫链三条件**。**深度网络 + 非线性 + LEO 非平稳，三条件一个都不满足。**
2. **反驳「TD 会因果归因」**：L500 逐字 `T D methods assign credit based solely on temporal succession` —— **TD 的信用分配是纯时间先后的，与"物理因果"无关**。**这直接支撑 G-A 的动机**：要区分"缓存溢出"和"队列溢出"，**TD(λ) 本身不提供任何因果信息**，必须从外部注入。
3. **反驳「λ 越大越好」**：L125 表明 λ=1 退化为监督学习式的 MC。**本报告未读 §4，不能给出"最优 λ"的定量结论，需要补读。**
4. **正面机制（可复用且本批最实在）**：**资格迹增量式（L133）**：$e_{t+1} = \nabla_w P_{t+1} + \lambda e_t$。**LEO 逐包在线场景下，这是唯一一个"常数内存 + 常数时间 + 显式控制回溯深度"的机制。**

---

### 4.9 E4NYGLGX — Safe and efficient off-policy RL（Retrace(λ)，Munos et al., NeurIPS 2016）

**1) 机制（公式逐字 + 行号）**

- **一般算子（L74 逐字，eq 3）**：
  ```latex
  \mathcal { R } Q ( x , a ) : = Q ( x , a ) + \mathbb { E } _ { \mu } \Big [ \sum _ { t \geq 0 } \gamma ^ { t } \Big ( \prod _ { s = 1 } ^ { t } c _ { s } \Big ) \big ( r _ { t } + \gamma \mathbb { E } _ { \pi } Q ( x _ { t + 1 } , \cdot ) - Q ( x _ { t } , a _ { t } ) \big ) \Big ] ,
  ```
- **四种迹系数的定义（L79 / L81 / L83 / L85 逐字）**：
  - `Importance sampling (IS): $\begin{array} { r } { c _ { s } = \frac { \pi ( a _ { s } | x _ { s } ) } { \mu ( a _ { s } | x _ { s } ) } } \end{array}$`
  - `Off-policy $\mathbf { Q } ^ { \pi } ( \lambda )$ and $\mathbf { Q } ^ { * } ( \lambda ) \colon c _ { s } = \lambda .$`
  - `Tree-backup, TB(λ): $c _ { s } = \lambda \pi ( a _ { s } | x _ { s } )$`
  - **Retrace(λ)（L83 逐字）**：`Retrace(λ): ${ c _ { s } = \lambda }$ min $\left( 1 , \frac { \pi ( a _ { s } | x _ { s } ) } { \mu ( a _ { s } | x _ { s } ) } \right)$`
- **Retrace 的动机（L85 逐字）**：`Our contribution is an algorithm – Retrace(λ) – that takes the best of the three previous algorithms. Retrace(λ) uses an importance sampling ratio truncated at 1. Compared to IS, it does not suffer from the variance explosion of the product of IS ratios. Now, similarly to $Q ^ { \pi } ( \lambda )$ and unlike TB(λ), it does not cut the traces in the on-policy case, making it possible to benefit from the full returns. In the off-policy case, the traces are safely cut, similarly to TB(λ).`
- **在线更新（L219 逐字，eq 7）**：
  ```latex
  Q _ { k + 1 } ( x , a ) \gets Q _ { k } ( x , a ) + \alpha _ { k } \sum _ { t \geq s } \delta _ { t } ^ { \pi _ { k } } \sum _ { j = s } ^ { t } \gamma ^ { t - j } \Big ( \prod _ { i = j + 1 } ^ { t } c _ { i } \Big ) \mathbb { I } \{ x _ { j } , a _ { j } = x , a \} ,
  ```
  其中 `$\delta _ { t } ^ { \pi _ { k } } : = r _ { t } + \gamma \mathbb { E } _ { \pi _ { k } } Q _ { k } ( x _ { t + 1 } , \cdot ) - Q _ { k } ( x _ { t } , a _ { t } ) , \alpha _ { k } = \alpha _ { k } ( x _ { s } , a _ { s } )$`
- **Replay 下的目标（§5 区块逐字）**：
  `$$\Delta Q ( x _ { t } , a _ { t } ) = \sum _ { s = t } ^ { t + k - 1 } \gamma ^ { s - t } \Big ( \prod _ { i = t + 1 } ^ { s } c _ { i } \Big ) \big [ r ( x _ { s } , a _ { s } ) + \gamma \mathbb { E } _ { \pi } Q ( x _ { s + 1 } , \cdot ) - Q ( x _ { s } , a _ { s } ) \big ] .$$`

**2) 适用条件与理论保证**

- **Theorem 1（L107 逐字）**：`The operator R defined by (3) has a unique fixed point $Q ^ { \pi }$ . Furthermore, if for each $a _ { s } \in { \mathcal { A } }$ and each history $\mathcal { F } _ { s }$ we have $c _ { s } = c _ { s } ( a _ { s } , \mathcal { F } _ { s } ) \in \left[ 0 , \frac { \pi \left( a _ { s } \left| x _ { s } \right. \right) } { \mu \left( a _ { s } \left| x _ { s } \right. \right) } \right]$, thenfor any Q-function Q` `$$\lVert { \mathcal { R } } Q - Q ^ { \pi } \rVert \leq \gamma \lVert Q - Q ^ { \pi } \rVert .$$` —— **对任意 $\pi,\mu$ 都是 γ-压缩。**
- **Theorem 2（L165 逐字）**：`Consider an arbitrary sequence of behaviour policies $\left( \mu _ { k } \right)$ (which may depend on $( Q _ { k } ) )$ and a sequence of target policies $\left( \pi _ { k } \right)$ that are increasingly greedy w.r.t. the sequence $( Q _ { k } ) .$` `$$Q _ { k + 1 } = \mathcal { R } _ { k } Q _ { k } ,$$` `... Then for any $k \geq 0 ,$` `$$\lVert Q _ { k + 1 } - Q ^ { * } \rVert \leq \gamma \lVert Q _ { k } - Q ^ { * } \rVert + \varepsilon _ { k } \lVert Q _ { k } \rVert .$$` `In consequence, i $i f \varepsilon _ { k } \to 0$ then $Q _ { k } \to Q ^ { * }$`
- **Theorem 3（L217 逐字）**：`Consider a sequence of sample trajectories, with the $k ^ { t h }$ trajectory $x _ { 0 } , a _ { 0 } , r _ { 0 } , x _ { 1 } , a _ { 1 } , r _ { 1 } , . . .$ generated by following $\mu _ { k }$ ... Assume that $\left( \pi _ { k } \right)$ are increasingly greedy w.r.t. $\left( Q _ { k } \right)$ and are each ε<sub>k</sub>-awayfrom the greedy policies ... with $\varepsilon _ { k } \to 0$ ... Then $\dot { Q } _ { k } \to Q ^ { * }$ a.s.`
- **不需要 GLIE（L259 逐字）**：`The crucial point of Theorem 2 is that convergence to $Q ^ { * }$ occurs for arbitrary behaviour policies. Thus the online result in Theorem 3 does not require the behaviour policies to become greedy in the limit with infinite exploration (i.e. GLIE assumption, Singh et al., 2000). We believe Theorem 3 provides the first convergence result to $Q ^ { * }$ for a λ-return (with $\lambda > 0 )$ algorithm that does not require this (hard to satisfy) assumption.`
- **方差约束（L241 逐字）**：`assuming independence and stationarity of $\left( c _ { s } \right)$ , we have that $\mathbb { V } \big ( \sum _ { t } \gamma ^ { t } c _ { 1 } \dots c _ { t } \big )$ is at least $\sum _ { t } \gamma ^ { 2 t } \mathbb { V } ( c ) ^ { t }$ , which is finite only if $\mathbb { V } ( c ) < 1 / \gamma ^ { 2 }$ . Thus, an important requirement for a numerically stable algorithm is for $\mathbb { V } ( c )$ to be as small as possible, and certainly no more than $1 / \gamma ^ { 2 }$ This rules out importance sampling` —— **这是"为什么必须截断到 min(1, π/μ)"的定量理由。**
- **原文自述的开放问题（L269 逐字）**：`Open questions include: (1) Removing the technical assumption that $P ^ { \pi _ { k } }$ and $P ^ { \pi _ { k } \wedge \mu _ { k } }$ asymptotically commute, (2) Relaxing the Markov assumption in the control case`
- **一句话定位（L288 逐字）**：`Conclusion. Retrace(λ) can be seen as an algorithm that automatically adjusts – efficiently and safely – the length of the return to the degree of "off-policyness" of any available data.`

**3) 迁移到 LEO 逐跳路由的条件与障碍** `[外推]`

| 轴 | 条件 | 障碍 |
|---|---|---|
| 网络级 vs 逐包决策 | 需要 $\mu(a\|x)$ 已知（对所选动作） | L263 逐字：`Retrace(λ) uses its knowledge of $\mu$ (for the chosen actions) to cut the traces and safely handle arbitrary policies π and $\mu$`。**在 LEO 里 $\mu$ 就是路由器自己的行为策略**（ε-greedy），可知；**但如果多个卫星同时探索、互相作为对方的"环境"，则 $\mu$ 不再是单一策略** |
| 非平稳 | **本篇的强项**：Theorem 2 对**任意行为策略序列** $\left( \mu _ { k } \right)$ 成立，且**不需要 GLIE** | **条件良好**：这是本批 11 篇中**唯一一个显式允许行为策略任意变化**的收敛结果 |
| 部分可观测 | **完全不涉及** | `grep -a -c -i -E "partial(ly)? observ|POMDP"` 实测 **0**。全部定理在 $(\mathcal X, \mathcal A, \gamma, P, r)$ 的 **MDP** 上（L31 逐字：`We consider an agent interacting with a Markov Decision Process $( \mathcal { X } , \mathcal { A } , \gamma , P , r )$`） |
| 信用分配 | **这正是 Retrace 的核心机制** | **条件成立**：L85 逐字 `in the off-policy case, the traces are safely cut, similarly to TB(λ)`。**这是把"资格迹回溯"从 on-policy 推广到 off-policy 的关键补丁**，直接对应 LEO 逐跳 + 经验回放的组合 |

**4) 作为反例的价值**

1. **反驳「off-policy + 资格迹不安全」**：Theorem 1 给出**对任意 $\pi,\mu$ 的 γ-压缩**，Theorem 3 给出 **a.s. 收敛到 $Q^*$ 且不需要 GLIE**。
2. **反驳「用重要性采样做 off-policy 修正就行」**：L241 逐字给出**定量否证**：$\mathbb { V } ( c ) < 1 / \gamma ^ { 2 }$ 是数值稳定的必要条件，而 `This rules out importance sampling`。
3. **反驳「λ 越接近 1 越好」**：§5 逐字 `Across values of $\lambda , \lambda = 1$ performs best, save for $Q ^ { * } ( \lambda )$ where $\lambda = 0 . 5$ obtains slightly superior performance. However, is highly sensitive to the choice of λ` `[OCR: 该句主语缺失，疑为 "Q*(λ) is highly sensitive"]` —— **原文自己承认对 λ 高度敏感**。
4. **打我们自己的点**：L269 逐字列出**两个未解决的技术假设**。**LEO 的拓扑动态正好会破坏这些交换性假设**——**引用 Retrace 的收敛性时，必须声明这些假设在 LEO 下未经检验。**

---

### 4.10 QGAREQUM — Boosting RL with Strongly Delayed Feedback Through Auxiliary Short Delays（AD-RL）

**1) 机制（公式逐字 + 行号）**

- **延迟建模（L78 逐字）**：`We assume that delay-free MDP is endowed with a constant delay variable $\Delta \in \mathbb { N }$ . In this setting, the state of environment $s _ { t }$ is only observed by the agent at a later timestep $t + \Delta$ . In other words, the real state of the environment is $s _ { t } ,$ but the agent's observation is $s _ { t - \Delta }$ . To retrieve the Markov property in this Delayed MDP (DMDP) ... we need to augment the state space $\mathcal { X } = \mathcal { S } \times \mathcal { A } ^ { \Delta }$ ... An augmented state $x _ { t } = ( s _ { t - \Delta } , a _ { t - \Delta } , \dotsc , a _ { t - 1 } ) \in \mathcal { X }$`
- **延迟信念（L128 逐字，eq 2）**：
  ```latex
  \begin{array} { l } { \displaystyle b _ { \Delta } ( \boldsymbol { x } _ { t } ^ { \tau } | \boldsymbol { x } _ { t } ) = } \\ { \displaystyle \int _ { S ^ { \Delta } } \Pi _ { i = 0 } ^ { \Delta - \Delta ^ { \tau } - 1 } \mathcal { P } ( s _ { t - \Delta + i + 1 } | s _ { t - \Delta + i } , a _ { t - \Delta + i } ) \mathrm { d } s _ { t - \Delta + i + 1 } } \end{array}
  ```
- **辅助延迟 Bellman 算子（L157 逐字，eq 3）**：
  ```latex
  \begin{array} { r l } & { \mathcal { T } Q ( x _ { t } , a _ { t } ) \triangleq \mathcal { R } _ { \Delta } ( x _ { t } , a _ { t } ) } \\ & { + \gamma \underset { x _ { t + 1 } ^ { \tau } \sim b _ { \Delta } ( \cdot \vert x _ { t + 1 } ) } { \mathbb { E } } \left[ Q ^ { \tau } ( x _ { t + 1 } ^ { \tau } , \underset { a _ { t + 1 } } { \mathrm { a r g m a x } } Q ( x _ { t + 1 } , a _ { t + 1 } ) ) \right] } \\ & { \quad \quad \quad \quad \quad \quad \quad x _ { t + 1 } \sim \mathcal { P } _ { \Delta } ( \cdot \vert x _ { t } , a _ { t } ) } \end{array}
  ```
  `[OCR: 该式在 MD 中排版错位，"argmax" 的角色需回原文核对]`
- **辅助延迟软 Bellman 算子（§4.3 区块逐字，eq 4）**：
  `$$\begin{array} { r l } & { \mathcal { T } ^ { \pi } Q ( x _ { t } , a _ { t } ) \triangleq \mathcal { R } _ { \Delta } ( x _ { t } , a _ { t } ) } \\ & { + \gamma \underset { \stackrel { a _ { t + 1 } \sim \pi ( \cdot | x _ { t + 1 } ) } { x _ { t + 1 } ^ { \tau } \sim b _ { \Delta } ( \cdot | x _ { t + 1 } ) } } { \mathbb { E } } \left[ Q ^ { \tau } ( x _ { t + 1 } ^ { \tau } , a _ { t + 1 } ) - \log \pi ( a _ { t + 1 } | x _ { t + 1 } ) \right] } \end{array}$$`
- **策略改进（L175 逐字，eq 5）**：
  ```latex
  \begin{array} { r } { \arg \operatorname* { m i n } _ { \pi ^ { \prime } \in \Pi } \mathbf { K L } ( \pi ^ { \prime } ( \cdot | x _ { t } ) \middle| | \frac { \exp ( \mathbb { E } _ { x _ { t } ^ { \tau } \sim b _ { \Delta } ( \cdot | x _ { t } ) } [ Q ^ { \tau } ( x _ { t } ^ { \tau } , \cdot ) ] ) } { Z ( x _ { t } ^ { \tau } , \cdot ) } ) } \end{array}
  ```
- **AD-SAC 策略梯度（L181 逐字，eq 6）**：
  ```latex
  \begin{array} { r } { \nabla _ { \psi } \underset { \hat { a } \sim \pi _ { \psi } ( \cdot | x _ { t } ) } { \mathbb { E } } \ [ \log \pi _ { \psi } ( \hat { a } | x _ { t } ) - Q ^ { \tau } ( x _ { t } ^ { \tau } , \hat { a } ) ] } \\ { x _ { t } ^ { \tau } { \sim } b _ { \Delta } ( \cdot | x _ { t } ) \ } \end{array}
  ```
- **算法框架（L139 起）**：`Algorithm 1 Auxiliary-Delayed RL Framework`，步骤为 `# Learning ∆τ-delayed task` → `# Learning ∆-delayed task based on Q^τ` → `Bootstrapping Q based on $Q ^ { \tau }$ via Eq. (3) # discrete` / `Improving π based on $Q ^ { \tau }$ via Eq. (5)# continuous`
- **关键实用注记（L133 逐字，Remark 4.1）**：`Practically, we do not need to learn the delayed belief $b _ { \Delta }$ explicitly. As in the CDMDP, every state will be observed by the agent eventually. In other words, given an entire trajectory collected by the agent, we can create the synthetic augmented state for any required delay.`

**2) 适用条件与理论保证**

- **Lipschitz 假设（L98 逐字）**：`In this work, we assume the MDPs, policies and Q-functions satisfy the following Lipschitz Continuity (LC) property, where Euclidean distance is adopted in a deterministic space ... and L1-Wasserstein distance (Villan et al., 2009), denoted as $W _ { 1 }$ , is used in a probabilistic space`；Definition 3.1（L100）给 $\left( L _ { \mathcal { P } } , L _ { \mathcal { R } } \right) - \mathrm { L C }$ 定义；Definition 3.3 给 $L _ { Q } = \frac { L _ { R } } { 1 - \gamma L _ { P } \left( 1 + L _ { \pi } \right) }$ 并要求 `$\gamma L _ { P } ( 1 + L _ { \pi } ) < 1$`。
- **样本效率（L192 逐字）**：`We can conclude that the sample complexity of augmented Q-learning in the augmented state space with delay $\Delta$ is $\mathcal { O } \left( \frac { \log ( | \mathcal { S } | | \mathcal { A } | ^ { \tilde { \Delta } + 1 } ) } { \epsilon ^ { 2 . 5 } ( 1 - \gamma ) ^ { 5 } } \right)$ . Then our AD-RL makes bootstrapping in the auxiliary $\Delta ^ { \prime }$ -augmented statespace instead of the original ∆-augmented state-space, the sample efficiency is improved by $\bar { \mathcal { O } } ( \vert \mathcal { A } \vert ^ { \Delta - \Delta _ { \tau } } )$`
- **样本效率的自述代价（L194 逐字，Remark 5.1）**：`in the stochastic environment with longer delays $\Delta ,$ we need to set relatively longer auxiliary delays $\Delta ^ { \tau }$ to achieve better performance while somewhat compromising the sample efficiency.`
- **性能差的界（§5.2 区块逐字，Theorem 5.3）**：`the performance difference between policies can be bounded asfollow` `$$\underset { x _ { t } ^ { \tau } \sim b _ { \Delta } ( \cdot \vert x _ { t } ) } { \mathbb { E } } \left[ V ^ { \tau } ( x _ { t } ^ { \tau } ) - Q ^ { \tau } ( x _ { t } ^ { \tau } , a _ { t } ) \right] \leq L _ { Q } \underset { x _ { t } ^ { \tau } \sim b _ { \Delta } ( \cdot \vert x _ { t } ) } { \mathbb { E } } \left[ \mathcal { W } _ { 1 } ( \pi ^ { \tau } ( \cdot \vert x _ { t } ^ { \tau } ) \vert \vert \pi ( \cdot \vert x _ { t } ) ) \right]$$`
- **确定性 MDP 无代价（§5.2 区块逐字，Remark 5.5）**：`For deterministic MDP, $b _ { \Delta }$ is also deterministic and becomes injection function meaning that given the $x ,$ the $x ^ { \tau }$ is determined` ... `$\mathbb { E } _ { \boldsymbol { x } _ { t } ^ { \tau } \sim b _ { \Delta } ( \cdot | \boldsymbol { x } _ { t } ) } \left[ Q _ { ( * ) } ^ { \tau } ( \boldsymbol { x } _ { t } ^ { \tau } , \boldsymbol { a } _ { t } ) \right] = Q _ { ( * ) } ( \boldsymbol { x } _ { t } , \boldsymbol { a } _ { t } )$`
- **随机 MDP 有代价（§5.2 区块逐字，Remark 5.6）**：`In the case of stochastic MDP, the performance gap might become larger as the difference between $\Delta$ and $\Delta ^ { \tau }$ increases. Using a moderate auxiliary delays $\Delta ^ { \tau }$ could trade-off the sample efficiency (closer to 0) and performance consistency (closer to $\Delta )$ .`
- **三条自述局限（L341 / L343 / L345 逐字）**：
  - L341：`It is worth noting that the performance of AD-RL is subject to the selection of the auxiliary delays $\Delta _ { b e s t } ^ { \tau }$ . Such selection is deeply related to the specific tasks and even the delay $\Delta ,$ and is highly challenging: Fig. 3(c) demonstrates that the relation between $\Delta _ { b e s t } ^ { \tau }$ and $\Delta$ is not linear or parabolic.`
  - L343：`Learning delayed belief, especially in stochastic environments, proves to be challenging. AD-RL implicitly represents the belief function by sampling in two augmented state spaces ... leading to additional memory cost compared to conventional augmentation-based approaches.`
  - L345：`Sample efficiency remains a critical challenge, especially in environments characterized by long delays or stochasticity. In both cases, AD-RL needs to set relatively longer auxiliary delays $\Delta ^ { \tau }$ to carry more information ... While a longer auxiliary delay achieves better performance, it brings back the sample inefficiency issue`

**3) 迁移到 LEO 逐跳路由的条件与障碍** `[外推]`

| 轴 | 条件 | 障碍 |
|---|---|---|
| 网络级 vs 逐包决策 | 需要"状态观测延迟 Δ"这一结构 | **LEO 逐包路由里这个结构天然存在**：包在时刻 $t$ 于卫星 i 被转发，其效果（到达/丢失/排队）在若干跳之后才被 i 观测到。**"延迟 = 跳数"是可直接映射的** |
| 非平稳 | 需要 DMDP 的结构稳定 | 原文是**定常延迟** $\Delta \in \mathbb { N }$（L78 逐字 `a constant delay variable`）。**LEO 的延迟本身随路径长度和拥塞波动 → 延迟是随机的，落在原文未覆盖的区间**（原文只在实验里测了 `stochastic delays`，理论是定常的） |
| 部分可观测 | 需要信念 $b(s_t\|x_t)$ 可算 | L133 逐字：`given an entire trajectory collected by the agent, we can create the synthetic augmented state for any required delay.` —— **这要求能回看完整轨迹**。**LEO 逐包仿真可以（记录轨迹），在线真实网络不行** |
| 信用分配 | **这正是本篇的核心**：用短延迟辅助任务 bootstrap 长延迟任务 | **条件成立且高度相关**：LEO 端到端时延是**长延迟**信号；每一跳的本地排队/链路时延是**短延迟**信号。**AD-RL 的 eq (3) 恰好是"用短延迟的 $Q^\tau$ 去 bootstrap 长延迟的 $Q$"** —— 这是本批 11 篇中与本项目信用分配问题**结构最同构**的一篇 |

**4) 作为反例的价值**

1. **反驳「长延迟必须靠加长回溯或加资格迹解决」**：本篇给出**第三条路**——**用一个人造的短延迟辅助任务去 bootstrap**（eq 3），并把样本效率提升量化到 $\bar { \mathcal { O } } ( \vert \mathcal { A } \vert ^ { \Delta - \Delta _ { \tau } } )$（L192）。
2. **反驳「辅助延迟越小越好」**：L194 + L345 逐字给出**双向代价**；L341 更进一步说 **$\Delta_{best}^\tau$ 与 $\Delta$ 的关系 "not linear or parabolic"**。**任何"我们设了个小辅助延迟就好了"的说法都是过度简化。**
3. **反驳「确定性环境下的结论可以外推到随机环境」**：Remark 5.5 与 Remark 5.6 给出**明确的条件分界**：确定性 MDP 下最优值**完全相等**（差为 0），随机 MDP 下**差距随 $\Delta - \Delta^\tau$ 增大而增大**。**LEO 路由的排队过程是随机的 → 落在 Remark 5.6 的坏情形。**
4. **打我们自己的点**：**本篇不解决"失败原因"问题**——`grep -a -c -i -E "credit assignment"` 实测 **2**，但均为泛述；`grep -a -c -i -E "reward decompos"` 实测 **1**，来自 §1 背景综述，**不是本篇方法**。**AD-RL 处理的是"延迟"，不是"多原因"。如果我们要主张 G-A，本篇是"最接近但确实没做"的标杆。**

---

### 4.11 LJG6ZW7B — Sutton & Barto, *Reinforcement Learning: An Introduction* (2nd ed.)

> **任务书限定**：只取与**信用分配 / 延迟奖励 / 部分可观测**直接相关的章节。以下条目全部来自定向阅读区间。

**1) 机制（公式逐字 + 行号）**

- **延迟奖励是 RL 的定义性特征（L352 逐字）**：`Reinforcement learning is learning what to do—how to map situations to actions—so as to maximize a numerical reward signal. The learner is not told which actions to take, but instead must discover which actions yield the most reward by trying them. In the most interesting and challenging cases, actions may a↵ect not only the immediate reward but also the next situation and, through that, all subsequent rewards. These two characteristics—trial-and-error search and delayed reward—are the two most important distinguishing features of reinforcement learning.`
- **信用分配的必要性（L911 逐字）**：`MDPs involve delayed reward and the need to trade o↵ immediate and delayed reward. Whereas in bandit problems we estimated the value $q _ { * } ( a )$ of each action $^ { a , }$ in MDPs we estimate the value $q _ { * } ( s , a )$ of each action a in each state s ... These state-dependent quantities are essential to accurately assigning credit for long-term consequences to individual action selections.`
- **奖励假设（L1004 逐字）**：`That all of what we mean by goals and purposes can be well thought of as the maximization of the expected value of the cumulative sum of a received scalar signal (called reward).` —— **注意：假设的是"单个标量信号"（a received scalar signal）。**
- **奖励信号的正确定位（L1010 逐字）**：`It is thus critical that the rewards we set up truly indicate what we want accomplished. In particular, the reward signal is not the place to impart to the agent prior knowledge about how to achieve what we want it to do. For example, a chess-playing agent should be rewarded only for actually winning, not for achieving subgoals such as taking its opponent's pieces or aining control of the center of the board. If achieving these sorts of subgoals were rewarded, then the agent might find a way to achieve them without achieving the real goal.`
- **λ-回报（L5067 逐字，eq 12.2）**：
  ```latex
  G _ { t } ^ { \lambda } \doteq ( 1 - \lambda ) \sum _ { n = 1 } ^ { \infty } \lambda ^ { n - 1 } G _ { t : t + n } .
  ```
  其 n 步回报（L5054 逐字，eq 12.1）：
  ```latex
  G _ { t : t + n } \doteq R _ { t + 1 } + \gamma R _ { t + 2 } + \cdot \cdot \cdot + \gamma ^ { n - 1 } R _ { t + n } + \gamma ^ { n } \hat { v } ( S _ { t + n } , { \mathbf w } _ { t + n - 1 } ) , ~ 0 \le t \le T - n ,
  ```
  离线 λ-回报的更新（§12.1 区块逐字，eq 12.4）：`$$\mathbf { w } _ { t + 1 } \doteq \mathbf { w } _ { t } + \alpha \Bigl [ G _ { t } ^ { \lambda } - \hat { v } ( S _ { t } , \mathbf { w } _ { t } ) \Bigr ] \nabla \hat { v } ( S _ { t } , \mathbf { w } _ { t } ) , t = 0 , \ldots , T - 1 .$$`
- **资格迹是对延迟奖励的"第一道防线"（L5686 逐字）**：`Because eligibility traces make TD methods more like Monte Carlo methods, they also can have advantages in these cases. If one wants to use TD methods because of their other advantages, but the task is at least partially non-Markov, then the use of an eligibility trace method is indicated. Eligibility traces are the first line of defense against both long-delayed rewards and non-Markov tasks.`
- **信用分配问题的经典表述（L6421 逐字）**：`The Law of E↵ect requires a backward e↵ect on connections ... We call this the problem of delayed reinforcement, which is related to what Minsky (1961) called the "credit-assignment problem for learning systems": how do you distribute credit for success among the many decisions that may have been involved in producing it? The reinforcement learning algorithms presented in this book include two basic mechanisms for addressing this problem. The first is the use of eligibility traces, and the second is the use of TD methods to learn value functions that provide nearly immediate evaluations of actions.`
- **集体 RL 的结构性信用分配（L6809 逐字）**：`What makes a team problem interesting and challenging is that the common reward signal sent to each agent evaluates the pattern of activity produced by the entire population ... This means that any individual agent has only limited ability to a↵ect the reward signal because any single agent contributes just one component of the collective action evaluated by the common reward signal. E↵ective learning in this scenario requires addressing a structural credit assignment problem: which team members, or groups of team members, deserve credit for a favorable reward signal, or blame for an unfavorable reward signal?`
- **POMDP 信念状态（L7431 逐字）**：`The natural Markov state, $S _ { t }$ , for a POMDP is the distribution over the latent states given the history, called the belief state. ... Then the belief state is the vector $S _ { t } \doteq \mathbf { s } _ { t } \in [ 0 , 1 ] ^ { d }$ with components` `$$\mathbf { s } _ { t } [ i ] \doteq \operatorname* { P r } \{ X _ { t } = i \mid H _ { t } \} , \quad \text{for all possible latent states } i$$`
- **信念更新（L7440 逐字，eq 17.10）**：
  ```latex
  u ( \mathbf { s } , a , o ) [ i ] \doteq \frac { \sum _ { x = 1 } ^ { d } \mathbf { s } [ x ] p ( i , o | x , a ) } { \sum _ { x = 1 } ^ { d } \sum _ { x ^ { \prime } = 1 } ^ { d } \mathbf { s } [ x ] p ( x ^ { \prime } , o | x , a ) } , \quad \mathrm { f o r ~ a l l ~ } a \in \mathcal { A } , o \in \mathcal { O } ,
  ```
- **状态-更新函数（§17.3 区块逐字，eq 17.7）**：`$S _ { t + 1 } \doteq u ( S _ { t } , A _ { t } , O _ { t + 1 } ) , \mathrm { ~ f o r ~ a l l ~ } t \ge 0 ,$`
- **"致命三元组"（L4588 区块逐字）**：`the danger of instability and divergence arises whenever we combine all of the following three elements, making up what we call the deadly triad:` `Function approximation` / `Bootstrapping` / `O↵-policy training` —— 并逐字：`If any two elements of the deadly triad are present, but not all three, then instability can be avoided.`

**2) 适用条件与理论保证（教材版）**

- **教材对"信用分配"给的两条基本机制（L6421 逐字）**：`The first is the use of eligibility traces, and the second is the use of TD methods to learn value functions that provide nearly immediate evaluations of actions.` —— **注意：两条机制都是关于"时间"的，没有一条是关于"原因"的。**
- **结构 vs 时序信用分配的划分（L6809 逐字）**：团队问题是 `structural credit assignment problem`；时序问题由 eligibility trace 处理。**教材自己把两者分开。**
- **λ 的经验结论（§12.13 区块逐字）**：`On tasks with many steps per episode, or many steps within the half-life of discounting, it appears significantly better to use eligibility traces than not to ... On the other hand, if the traces are so long as to produce a pure Monte Carlo method, or nearly so, then performance degrades sharply. An intermediate mixture appears to be the best choice. Eligibility traces should be used to bring us toward Monte Carlo methods, but not all the way there.`
- **何时不该用资格迹（§12.13 区块逐字）**：`in o↵-line applications in which data can be generated cheaply, perhaps from an inexpensive simulation, then it often does not pay to use eligibility traces. In these cases the objective is not to get more out of a limited amount of data, but simply to process as much data as possible as quickly as possible.`
- **部分可观测下函数近似的覆盖范围（L3392 逐字）**：`extending reinforcement learning to function approximation also makes it applicable to partially observable problems ... If the parameterized function form for vˆ does not allow the estimated value to depend on certain aspects of the state, then it is just as if those aspects are unobservable. In fact, all the theoretical results for methods using function approximation presented in this part of the book apply equally well to cases of partial observability. What function approximation can't do, however, is augment the state representation with memories of past observations.`
- **对 POMDP 信念法的评价（§17.3 逐字）**：`This approach is popular in theoretical work and has many significant applications, but its assumptions and computational complexity scale poorly, and we do not recommend it as an approach to artificial intelligence.`

**3) 迁移到 LEO 逐跳路由的条件与障碍** `[外推]`

| 轴 | 教材原话 | 对 LEO 的直接影响 |
|---|---|---|
| 网络级 vs 逐包决策 | L911 逐字：`we estimate the value $q _ { * } ( s , a )$ of each action a in each state s` | **教材的 MDP 框架要求"状态-动作对"可枚举或可泛化**。LEO 逐包路由的"状态"含全网队列 → 必须靠函数近似，落入 L4588 的**致命三元组** |
| 非平稳 | L4588 逐字：`If any two elements of the deadly triad are present, but not all three, then instability can be avoided.` | **LEO 逐跳路由几乎必然同时具备三要素**：函数近似（Q 网络）+ bootstrapping（TD）+ off-policy（经验回放）。**教材把这三者同时出现直接判定为"不稳定与发散的危险"。这是对我们方案最硬的教材级反驳。** |
| 部分可观测 | 信念状态（L7431）+ 明示不推荐（§17.3）；L3392 说函数近似"自动覆盖"部分可观测 | **两条路都不能直接用**：信念状态 $\in [0,1]^d$ 在 LEO（$d$ = 全网队列维）下不可算；函数近似的"自动覆盖"**只是说结果仍然成立，不是说结果好** |
| 信用分配 | L6421 逐字：两条机制**都只针对时间**；L6809 逐字：团队问题需要 `structural credit assignment` | **教材在结构层面只提出问题，不给方法**。**这为 G-A 提供了教材级的空白背书** |

**4) 作为反例的价值**

1. **教材级反驳「三要素齐上没关系」**：L4588 把"函数近似 + bootstrapping + off-policy"命名为 **deadly triad**，并说三者同时出现**就会**不稳定/发散。**LEO 逐跳 RL 路由方案若三者齐备，必须显式处理**，不能只靠实验调参。
2. **反驳「奖励写成一个标量就够了」**：L1004 的**奖励假设**原文限定为 `a received scalar signal`；L1010 紧接着逐字说 `the reward signal is not the place to impart to the agent prior knowledge about how to achieve what we want it to do`，并警告 `the agent might find a way to achieve them without achieving the real goal`。**这是对朴素惩罚塑形的直接反驳，也是 G-A 必须回答的诘问**：分通道惩罚若被当作"subgoal 奖励"，同样有被钻空子的风险。
3. **反驳「资格迹越长越好」**：逐字 `if the traces are so long as to produce a pure Monte Carlo method, or nearly so, then performance degrades sharply`。**LEO 端到端回报很长，很容易把 λ 设到接近 1，正好落进教材说的"急剧退化"区间。**
4. **反驳「用仿真所以可以用资格迹」**：逐字 `in o↵-line applications in which data can be generated cheaply, perhaps from an inexpensive simulation, then it often does not pay to use eligibility traces`。**LEO 逐跳仿真正是 "cheap simulation"。**
5. **G-A 的教材级背书**：L6809 逐字提出 `structural credit assignment problem: which team members, or groups of team members, deserve credit for a favorable reward signal, or blame for an unfavorable reward signal?`，而 L6421 列出的**两条机制全部是时间维度的**。**教材在"按来源/成员分解功劳与责任"这一维度上停在提问——这是 G-A 的权威立足点。**

---
