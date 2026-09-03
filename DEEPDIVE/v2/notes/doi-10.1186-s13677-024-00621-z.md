# 精读笔记：DOI:10.1186/s13677-024-00621-z

> Hu, Y., Qiu, F., Zheng, F., Zhao, J. "Multi-dimensional resource allocation strategy for LEO satellite communication uplinks based on deep reinforcement learning." *Journal of Cloud Computing* 13, 56 (2024). https://doi.org/10.1186/s13677-024-00621-z
> 收稿 2023-11-02，录用 2024-02-28，发表 2024-03-08。OA (CC BY 4.0)。作者单位：桂林电子科技大学认知无线电与信息处理教育部重点实验室。

## 七要素

1. **问题**：多波束 LEO 卫星上行链路的资源利用率低——星上资源受限 + 业务量在波束间/时间上分布不均，且 LEO 卫星高速移动导致网络复杂多变；传统资源分配策略难以应对，同频干扰进一步限制利用率。现状工作"只重眼前收益、忽视长期收益"（给新用户最优资源，损害后续用户接入）。
2. **场景/假设**：多波束 LEO 卫星系统上行链路；相控阵天线生成 37 个点波束，全频率复用；用户按泊松分布随机出现（200 用户）；用户为发射端、卫星为接收端；每用户同一时刻仅占一个信道；按业务类型设 SINR 门限 γ_k。
3. **模型**：波束集合 M、每波束用户 i、信道 n；信道占用矩阵 W^t；Bessel 函数天线接收增益 G_R(θ)、自由空间路损 L、接收功率 p_R、SINR（含邻波束同频干扰 I 与噪声 N0）、Shannon 速率。三指标：频谱效率 SE（式12）、能量效率 EE（式13）、阻塞率 VE（式15）。优化目标：SE、EE 加权极大化 + VE 极小化；约束 s1 功率上限、s2 SINR≥门限、s3 每用户仅占一个信道（式16）。
4. **方法（RL 建模）**：DQN。Agent=LEO 卫星，环境=波束。状态 S_t={W^t 信道占用矩阵, U^t 各波束用户数/业务分布, NU^t 新用户业务信息}；动作 a_t={信道 m, 功率 p}，功率离散化为多个功率域，a_t={0,0} 表示不分配；奖励 r_t=1 当 ΔZ>0 否则 0，其中 Z=a1·Ψ(SE)+a2·Ψ(EE)+a3·Ψ(1−VE)（归一化加权）。核心创新：**状态重构**——不只看周围两层同频干扰波束，而是合并当前服务波束与周围三层（DQN 用四层）波束及高业务量波束，降低状态维度并最大化长期收益；配合经验回放 + 目标 Q 网络 + ε-greedy。
5. **数据/实验**：纯仿真，37 点波束、200 用户泊松到达；对比算法为 Q-Learning（三层波束状态重构）与 DQN；权重 (1/3,1/3,1/3) 与 (1/4,1/4,1/2) 两组；学习率 0.01、折扣因子 0.9、探索率 1→0.01。基线是 RL（Q-learning）而非启发式/凸优化方法。
6. **结果**：用户数 200 时：阻塞率 Q-learning≈20%，DQN≈15%；阻塞率权重 1/2 时 DQN≈12%（降低至少 5 个百分点）。频谱效率：用户 200 时 1/4 权重 DQN≈350 Mbps/MHz > 1/3 权重 Q-learning≈345 Mbps/MHz。能量效率：用户 125 时 DQN(1/3)≈82.5 Mbps/W、DQN(1/4)≈75.6 Mbps/W、RL(1/3)≈77.8 Mbps/W。功耗：50–75 用户区间 Q-learning 比 DQN 多约 20 W；DQN(1/2 权重) 200 用户时功耗达 638 W 但接入更多用户。低用户数时两法差异不显著，高用户数时差异显现。
7. **局限/可反驳点**：(a) 仅上行、单星视角，无星间链路与切换；(b) 对比基线只有 Q-learning，未与启发式/凸优化/多智能体方法比较；(c) 仿真规模小（200 用户、37 波束）、未报告运行时间/收敛轮数与网络超参细节；(d) 结论仅由仿真支撑，无硬件/实测验证；(e) 奖励为二值 (0/1)，信用分配粗糙；(f) "至少降低 5%" 仅在高用户数场景成立。

## RL 领域块

- **问题形式化**：把卫星无线资源分配视为序列决策问题（sequential decision-making），卫星=agent，波束=environment，信道+功率=动作。
- **状态设计**：信道占用矩阵 W^t + 业务分布矩阵 U^t + 新用户业务信息 NU^t；终端态定义为"所有用户均已分配或无可分配资源"。
- **动作设计**：离散信道选择 + 离散化功率域；显式包含"不分配"动作 {0,0}，即拒绝始终是可选动作——这对阻塞率优化至关重要。
- **奖励设计**：三指标归一化加权的增量阈值化：ΔZ>0 → r=1，否则 r=0；权重可随业务负载动态调整（低负载偏向 SE/EE，高负载偏向阻塞率）。
- **网络与训练**：CNN+全连接层（复杂度分析式 25–27）；经验回放 + 目标 Q 网络（隔固定步同步 ω→ω⁻）+ ε-greedy。
- **核心贡献——状态重构（state reconstruction）**：同频干扰只来自相邻两层同心波束，但只看两层会做出"损人利己"的信道选择（占掉邻波束后续新用户必需的信道）；重构为包含新用户波束周围三层（Q-learning）/四层（DQN）同心波束的状态 s*，以换取长期收益。这是该文区别于一般 DQN 资源分配的关键，也是其降低高负载阻塞率的来源。
- **复杂度**：DQN 状态维度高于 Q-learning（四层 vs 三层波束），复杂度更高，但训练收敛后复杂度下降，声称适应 LEO 高动态环境。

## 逐字引用

1. > [Abstract] "Simulation experiments show that in scenarios with a high number of users, the proposed resource allocation strategy reduces the blocking rate by at least 5% compared to reinforcement learning methods, effectively enhancing resource utilization."
2. > [Introduction] "Taking co-frequency interference and traffic distribution into account between beams, a joint channel-power allocation strategy based on deep reinforcement learning is proposed."
3. > [Related work] "Currently, the existing literature on resource management mainly emphasizes immediate gains while neglecting long-term benefits. For example, whenever a new user accesses the system, the system allocates the best communication resources to achieve high QoS, which is not conducive to subsequent new user access."
4. > [Resource allocation strategy] "However, if we consider the surrounding three concentric beams, we can allocate channel w2 to the new users in beam a. The co-frequency interference for new users in beam b is relatively weaker."
5. > [Simulation analysis] "When the number of users reaches 200, the blocking rate of the Q-learning algorithm is about 20% when the weight value is 1/3, and the blocking rate of the DQN algorithm is reduced to about 15%."
6. > [Conclusion] "Moreover, state integration is performed by merging beams with high user traffic and the current service beam to avoid bias towards current users while neglecting subsequent new users, in order to maximize long-term benefits."

## 与选题空间的关系

- **直接相关**：本文是"LEO 多波束 + DRL 资源分配"方向的代表性 OA 论文，其"状态重构换取长期收益"思想与本平台关注的 LEO 直连仿真中负载不均/冷启动场景的资源决策模块高度可对接——特别是高业务量波束合并的思想可映射到仿真平台的波束级负载建模。
- **可借鉴**：①"不分配/阻塞"作为显式动作 + 三指标加权增量的奖励阈值化，简单且易在仿真平台复现；②权重随负载动态切换（低负载 SE/EE、高负载阻塞率）可作为实验自变量设计。
- **可反驳/差异空间**：①仅单星上行、无切换与星间协作——多星/星间视角留白；②基线弱（仅 Q-learning），缺少与多智能体 DRL、波束跳变 (beam-hopping)、启发式方法的对比；③奖励二值化导致信用分配粗糙，可研究更细粒度奖励或 PPO/SAC 类策略梯度；④无真实星座参数/实测验证，仿真结论需在自有平台复现核验（符合"科研结论必须可复现、可反驳"的仓库铁律）；⑤训练收敛行为、超参敏感性"未报告"，是可做的消融空间。
- **注意**：发表时间 2024-03，属于近两年工作；引用其数值结论时应注明是 37 波束/200 用户特定仿真场景下的结果，不可泛化。
