# Information Freshness of Updates Sent over LEO Satellite Multi-Hop Networks (ARXIV-2007.05449)

分析型 AoI 论文：把 LEO 多跳中继建模为 K 节点串联队列，推导端到端平均 AoI / PAoI 尾的闭式界与紧近似。

- **方法骨架**（解析，非 RL，无状态/动作/奖励/训练）：拓扑=串联队列网络，每个节点既是中继又是源（Sec III）；源为 Poisson(λ)，节点 k 有 cross traffic θk，其中 ψk 比例离开本连接，末节点经专用下行天线到地（downlink，DL）；错误信道 ε 下再分析（Sec III-B）。调度纪律三选一：FCFS、OPF（按生成时间而非到达时间排队→跨流公平）、HAF（按源当前年龄最高优先→AoI 优化），见 Sec II/III；界与 PAoI 尾在 Sec IV（IV-A FCFS 平均 AoI 界、IV-B OPF/HAF、IV-C PAoI 尾界）。
- **实验合同**（Sec V + Table II）：Monte Carlo 仿真两个实例——line（K_line∈{2,6,10} 中继，地面各节点聚合源）与 dumbbell（K_db=4 中继、共享单条 ISL 瓶颈、N_db∈{2,6,10} 个 cross 源）；μ_ISL=1、μ_DL=0.8（下行即瓶颈）、ψ=0、ε=0.01、N_pkt=100000；负载 ρ=(λ+Σθ)/μ_DL，令 λ=θj=ρμ_DL/K；指标=平均 AoI、PAoI 尾、源间公平性；无星座/轨道/seed 记载，稳态前丢弃预热。
- **与我们对账**：
  1. AoI 对负载呈 U 型（Fig.7，低负载时 AoI 由源生成间隔主导）——我们 ISL 利用率<3% 正落在 U 型左支：队列状态几乎无信息量，这就是 F0/F1 信息阶梯改了 1/3 路由却交付零差异的机理侧证据（信息不稀缺时路由决策不敏感）；
  2. 他们结论反指"年龄瓶颈节点"（加强关键链路速率/可靠性比改路由更影响 AoI，Abstract/VI）——与我们的 holding/access 瓶颈判定同构：瓶颈不在被选路径上的 ISL（<3%），而在接入/持有环节；
  3. OPF/HAF 证明不改路径、只改排队纪律即可换 AoI/公平（Sec II,V）——支持把年龄感知下沉到 holding/队列管理而非多径重路由；
  4. 本文 AoI 对象是"网络内传输的更新包"，无人把路由状态信息年龄当状态/分析对象——我们的 AoI-of-state 空白依旧成立。
- **可复用 + 危险信号**：串联队列 AoI 界与 U 型/最优负载区公式可直接做我们 holding 瓶颈的理论对照；OPF/HAF 可搬进 holding/access 调度器做年龄感知基准实验；PAoI 尾界可作最坏情形指标。数字存疑/未核实：μ_ISL=1、μ_DL=0.8 为归一化服务率（Table II，非真实星座速率）；N_pkt=10^5、无 seed 说明（TabII），仿真方差未报告；ε=0.01 对所有链路同值且重传机制未核实于正文。

> 深读状态: 全文已读[ar5iv.labs.arxiv.org/html/2007.05449]；未核实: 作者/出处元数据、真实服务率设定、重传模型细节、seed 与方差数据
