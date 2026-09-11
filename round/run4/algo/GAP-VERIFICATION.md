# 缺口主张的对抗性核验（GAP-VERIFICATION，主控执行，2026-09-11）

> 目的：不让自己"找到一个缺口"就收工。系统地去**找能推翻缺口主张的反例**。任何"全库没有 X"的主张，
> 必须先经本文件的核验。核验中发现的反例一律登记，并据此**收窄或撤销**主张。

## 主张 G-A（初版）：全库无人做"损失归因"——丢包罚是单一标量，决策缓存溢出与链路溢出不可分

### 反例 1：UKBSA7WN（QRLSN）——**存在奖励向量**（部分反例，已核验）

L158 逐字：原文用**多目标 RL（MORL）**：
$$
\mathrm{TQ}(s,a) = \sum_{i=1}^{n} w_i Q_i(s,a)  \tag{7}
$$
> "In the proposed QRLSN, two optimization targets are obtained by a reward vector $f_r = [f_{r_1}, f_{r_2}]$"（L158）

$$
f_{r_1} = \begin{cases} r_{max} & N_{t+1}\ \text{is destination} \\ r_{min} + (e/2)^{-d_{ij}} & \text{Otherwise} \end{cases}  \tag{8}
$$
$$
f_{r_2} = \begin{cases} r_{max} & N_{t+1}\ \text{is destination} \\ r_{min} + (e/2)^{-n_q} & \text{Otherwise} \end{cases}  \tag{9}
$$
> "$f_{r_1}$ and $f_{r_2}$ denote the reward function to optimize **the end-to-end delay** and **network traffic overhead load** respectively; $d_{ij}$ is the transmission time between adjacent satellite nodes; $n_q$ is the number of data packet queued in the current node."（L160）

**判定**：反例成立，但**不覆盖本缺口**。理由是**分解轴不同**：
- UKBSA7WN 分解的是**目标类型**（时延 vs 负载）——标准 MORL，两个 Q 头加权求和；
- G-A 指的是分解**失败事件的原因**（这次丢包是决策缓存溢出，还是链路溢出）——只有当**同一个负事件有多个物理原因、且规避行为不同**时才有意义。

**对本缺口的影响**：**G-A 必须收窄表述**——不能说"全库奖励都是标量"（UKBSA7WN 有向量），
只能说"**全库未见把同一失败事件按物理原因分通道的学习信号**"。同时必须承认：MORL 的技术手段（多头 Q、加权合成）**已存在且可复用**——这不削弱缺口，反而说明**实现路径现成**。

### 反例 2：39NJWBI7（PRIMAL）——**约束式奖励（CMDP）**（不构成反例，已核验）

L397 逐字：cost 为归一化排队时延 $c_h = D_h^Q / D_{norm}$（单通道约束量），乘子 λ_k 更新（式 27）。
丢包惩罚在 $B_p$ 内为标量合成：$-5\tau_p^{ttl}/D_{norm} - \sum_{j=0}^{h} \Delta d_{GCD}$（式 36）。
**判定**：约束通道是**代价类型**（排队时延），不是**失败原因标签**；丢包仍是标量。不构成反例。

### 反例 3：S85KQ4FC（锚件）——奖励把决策时延单列，但丢包仍单通道

式 14：未丢包分支含 $\mathcal{D}^{dec}_{j,k}$（决策时延，原文自述"overlooked in the previous studies"）；
丢包分支只有 $-\psi$。**信息（Θ_i 转发队列、Ω_i 邻居决策队列）在状态里，学习信号未用**。
**判定**：这是 G-A 的**正面证据**，不是反例。

## 主张 G-A 的收窄版（据此更新）

> **在"决策资源与链路资源同时被建模"的合同下，全库未见任何工作把同一失败事件（丢包）按物理原因
> 拆成独立学习通道**；已有的多信号机制（MORL 目标分解、CMDP 约束通道）分解的是**目标/代价类型**，不是**失败原因**。
> 该缺口的可操作性前提是：状态里**已经同时含两类队列信息**（S85KQ4FC 的 Θ_i/Ω_i 即满足）。

## 待办：把同一核验做在其余 33 篇 T1 上

- 检索词（精确模式，报告计数与命中位置）：`credit assignment`、`counterfactual`、`reward decompos`、`multi-objective|MORL`、
  `separate (reward|penalty)`、`cause of (the )?(drop|loss)`、`drop (reason|cause)`、`overflow`（区分决策/链路）。
- 每批 dossier 交回后，主控按本文件格式逐条核验并登记反例。

---

# 附录：B4/B5 批次带回的近邻复核（主控亲验，2026-09-11）

## 反例 4：9KZDXPKC / DB-R——**按丢包物理原因分支，但走的是路由通路而非学习通道**（不覆盖，已逐字核）

L55 逐字：
> "DB-R mechanism leverages default routing to address the packet loss caused by **GSL handover**. Moreover, DB-R mechanism configures backup routing to address the packet loss caused by **ISL failure**."

**判定**：分解轴 = **失败原因** ✅（GSL 切换丢包 vs ISL 失效丢包），这是全库**第一个**"按物理原因分流"的实例，但：
- 该文**不含 RL**（B5 实测 reinforcement=0 / reward=0）；
- 分流动作是**选择哪条路由通路**（默认 vs 备份），不是**维护哪条学习通道/惩罚项**。

**对本缺口的影响**：G-A 的措辞必须写明"**接进学习信号**"这一限定——否则会被 DB-R 的"按原因分流"抢占。**正面价值**：它提供了**失败原因在线标注器**（B5 §14 指出 L198–204 用前缀命中 GSL Array 判 GSL 切换、L230 用接口失效判 ISL 故障）——这正是 G-A 落地所需的**标签来源**，可复用。

## 反例 5：9GPFG5U3 / LiR——**代价项分解存在、但立刻加和为单一标量**（不覆盖，已逐字核）

L121 / L123 逐字：
> "we let $f_{IFO}(\cdot)$ denote the **incorrect forwarding overhead** … caused by false positives"
> "we let $f_{CFO}(\cdot)$ denote the **correct forwarding overhead** … caused by the M-bit BF along the planned route"

L181 式 (7) 逐字：
$$
f_{FO}(N,M,K) = f_{IFO}(N,M,K) + f_{CFO}(N,M)
$$

**判定**：分解轴 = **代价来源**（错误转发开销 vs 正确路径开销），**但分解后立刻加和为单一标量**用于 BF 参数设计 → 不存在独立学习通道，且该文不含 RL。**不覆盖 G-A**。

**措辞风险**：G-A 不能写成"首次分解代价"——LiR 已在 2021 年分解过代价项。正确措辞限定为"**分解失败原因、且各原因维护独立学习通道**"。

## 反例 6：SaTE（JLF7IEBQ）——**明确断言 RL 不适合卫星网**（对"用 RL"本身的挑战，已逐字核）

L136 逐字：
> "Recent studies [23, 61] use deep neural networks and multi-agent reinforcement learning to accelerate TE in terrestrial WANs but **struggle with topology changes in satellite networks, requiring frequent retraining following topology changes**."

**判定**：这是对"把 RL 用于卫星网"的**已发表质疑**（SIGCOMM'25 级别的出处）。但注意：
- 该文**只断言、未验证**——它没有做 RL 的对照实验，是"推断不适合"；
- 它的替代方案是监督学习（Gurobi 标签，L201 逐字），**不是在线 RL 路由**；
- 其质疑的对象是"TE 计算加速"（集中式、拓扑变化触发重训），**不直接命中逐包逐跳在线路由**——后者本来就在线适应，不存在"每次拓扑变化重训"。

**处置**：作为**必须在方案中正面回应**的对手主张登记，不作否定。回应要点：本方案的训练-部署协议需明确给出"拓扑变化下的适应证据"（这正是 C2 训练分布件与 B3 强度轴要产出的东西）。

## 反例 7：47J2H748（1994 Q-routing 原典）——**探索与真实包的冲突**

B4 指出该文 L77/L79/L88 有"ε-greedy 探索真实包"的反面结论（探索会损害真实流量）。
**判定**：不覆盖 G-A；但属**方案设计约束**——任何在真实包上做探索的设定都需说明探索代价或改用离线预训练 + 冻结部署（B1 实测 7 篇中 6 篇正是离线训练+冻结）。

## G-A 收窄后的最终口径（三次收窄后）

> **在含学习成分的 LEO 路由工作中，未见任何一篇把同一个失败事件（丢包/超时/溢出）按 ≥2 个物理原因
> 归因，并为每个原因维护独立的学习通道或独立惩罚项；已有的分解分别落在目标类型（UKBSA7WN）、
> 代价类型（PRIMAL 的 λ_k、LiR 的 f_IFO/f_CFO）、代价来源标注（DB-R，未进学习）、智能体（COMA/QMIX）、
> 时间（GAE）五个不同轴上。**

**前提件（可复用，非贡献）**：失败原因标签来源（DB-R 的 GSL/ISL 标注器；本方案锚件的决策缓存 vs 转发队列标签）。
**最近的未满足者**：8N9QJHC2（按故障类型触发不同 Q 表更新，但式 (14) 对两类故障完全相同）。
