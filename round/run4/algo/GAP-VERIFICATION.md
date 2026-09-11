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
