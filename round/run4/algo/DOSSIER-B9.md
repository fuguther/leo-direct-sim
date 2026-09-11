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
