# 精读笔记：10.3390/electronics8090920

全文不可取得=否（MDPI HTML 页 Access Denied，改从 res.mdpi.com 官方 PDF 提取全文，存 ../fulltext/doi-10.3390-electronics8090920.txt）

- 题目：A Two-Hops State-Aware Routing Strategy Based on Deep Reinforcement Learning for LEO Satellite Networks
- 作者：Cheng Wang*, Huiwen Wang, Weidong Wang（北京邮电大学电子工程学院）
- 出处：Electronics 2019, 8(9), 920；Received 15 Jul 2019 / Accepted 20 Aug 2019 / Published 22 Aug 2019
- 方法名：DRL-THSA（Two-Hops State-Aware Routing Strategy Based on DRL）

## 七要素

1. **问题**：LEO 星座（类 Iridium）中任意流到达与区域负载不均导致流量分布失衡，路由需能随网络状态变化自适应调整路径；集中式重算开销大，星上资源受限。
2. **假设**：拓扑可用虚拟节点（VN）法转成时变图/2D 平面快照；每星只需两跳范围内的链路状态即可做出足够好的下一跳决策；业务可由 Pareto On-Off 流近似；链路状态可离散分级。
3. **方法**：每星维护本星链路状态表 LST + 邻居链路状态表 NLST（两跳状态）；链路状态按队列占用阈值 T1/T2 分三级，不同级别对应不同转发策略（TLR/ELB/ELMDR 风格的等待/重路由机制处理中断与拥塞）；用 Double-DQN（DDQN）离线在地面上训练，训练好的模型按目的节点存储到每颗卫星，星上只推理不再更新；输入 [当前星, 目的星, LST]，输出最优下一跳。
4. **数据/环境**：NS-3.29 仿真，类 Iridium 星座 66 星 6 面（780 km，极区边界 70°），ISL 25 Mb/s，包长 1 kB，队列 100 包，200 条 Pareto(shape=1.5) On-Off 流，burst/idle 各 500 ms，仿真 60 s，每场景跑 100 次取均值，ε=0.9。
5. **结果**：在传输率 2.5→3.5 Mbps（流数固定 200）和流数 200→300（速率固定 3.5 Mbps）两组扫描下，DRL-THSA 的端到端时延、丢包率、吞吐量三项指标均优于 ELB、TLR、ELMDR；归因于过滤短期轻负载波动、两跳范围内按状态换路避免排队时延、DDQN 预训练给出更优路由。
6. **局限**：DDQN 模型离线训练后星上固定不更新（no longer updated during the satellite routing process），无法适应训练分布外的流量模式；每颗卫星需按目的节点存储模型（the number of DDQN is equal to the number of satellites），可扩展性存疑；仅仿真验证，无实物/星上实验；阈值 T1/T2、奖励权重 α/β 等靠经验设定。
7. **可迁移点**：两跳局部状态感知 + 分级链路状态广播是降低状态收集开销的轻量设计；地面离线训练 + 星上只推理是早期 DRL-路由的典型部署范式；四类动态情况处理（链路失效/恢复/状态变化/死循环路由，含两跳回环检测）值得复用。

## RL 领域块

- **RL-Formulation**：MDP 记为 {S, A, P, R}。S = [Ns, Nd, LST]（源、目的、当前星链路状态表）；A = Nnext（邻居下一跳）；P = Pnext（由邻居链路状态数按式(13)归一化）；R 按式(15)：到达目的给 +rd，下一跳失败/拥塞给 -rc，其他给 -dif(Ns,Nd)（dif 由 RAAN 与平近点角差加权的球面距离式(14)，体现层间/面间 ISL 权重 α、β）。
- **RL-Setup**：DDQN：online 网 θonline 每步更新，target 网 θtarget 每 Ntarget 步硬同步；损失 L=[Y-Q]^2，Y = r + γ·Q(s', argmax Q(s',a';θonline); θtarget)；ε-greedy（ε=0.9，偏利用），experience replay 记忆 M，mini-batch Nb 训练；discount γ 数值未报告。训练在地面离线完成，逐目的星各存一个模型。
- **Baselines**：ELB [9]、TLR [10]、ELMDR [12]（极学习机分布式路由），在同一 NS-3 场景下对比。
- **Metrics**：平均端到端时延、总丢包率（队列溢出 + TTL 归零，星间链路假设无差错）、系统吞吐量；另给每星平均队列占用（Figure 12）。
- **Reality-Gap**：全部在 NS-3.29 仿真完成；星座为 Iridium-like 而非真实星座参数；星间链路假设无差错、ISL 固定 25 Mb/s；无天线指向/姿态等物理层损伤建模；DDQN 在地面用仿真流量训练，星上不在线学习——sim-to-real 与分布漂移均未讨论。未报告：训练耗时与星上推理开销。
- **Reproducibility**：系统参数表（Table 4）相当完整（高度、极区纬度、ISL/馈电带宽、包长、队列、tc=30ms、th=30ms、td=30ms、ε=0.9、ELB/TLR/ELMDR 参数均给出），且每场景重复 100 次；但 DNN 结构（层数/单元数）、学习率、batch size、Ntarget、Nb、γ 未报告，且无代码/模型发布。部分可复现：仿真场景可重建，DDQN 训练细节需自行猜测。

## 逐字引用

> [Abstract] "the routing strategy in LEO networks should have the ability to adjust routing paths based on changes in network status adaptively."

> [Abstract] "In this strategy, each node only needs to obtain the link state within the range of two-hop neighbors, and the optimal next-hop node can be output."

> [3.2 Routing Algorithm] "Due to limited resources and processing capacity on the satellite, we simulate the flows of the satellite networks and complete the DDQN training process on the ground. The off-line training process enables the DDQN model to cope with all the link states that may be encountered. Then the trained DDQN models are stored on the satellite and no longer updated during the satellite routing process."

> [3.2.1] "Because the network topology environment changes with the destination node. For the whole LEO satellite networks, the number of DDQN is equal to the number of satellites."

> [4.1 Parameters Setup] "we use NS-3.29 (Network Simulator 3, Version 3.29) as the simulation tool to construct the simulations in an Iridium-like satellite network with 66 satellites distributed over six planes."

> [4.2.1] "the DRL-THSA alternates path according to route state within two-hops, which avoids more queuing delay."

> [5. Conclusions] "When the link states changes, it may broadcast the changes to its neighbors for updating the LST."

## 与选题空间的关系

- **直接同类**：这是 LEO 星座 + DRL（DQN 系）+ 局部状态感知路由的早期代表作（2019），与 RL for LEO routing 选题空间正面重叠；其 DDQN 离线训练/星上固定推理范式正是后续在线/分布式 DRL 路由工作要改进的基线。
- **可对比基线**：若复现 DRL-THSA 类方法，其 NS-3 参数集（Table 4）可作为仿真配置参照；本平台若强调在线学习/分布漂移/回执可验证，本文离线训练、永不更新的设定恰好是可指认的 gap。
- **方法要素可借用**：两跳状态表 + 链路状态分级（阈值 T1/T2）是低开销状态表征，可作为状态空间设计的下限基线；奖励设计（到达奖励/失败惩罚/球面距离塑形）是可复用的 reward shaping 起点。
- **反面教训**：逐目的星存模型（模型数=卫星数）不可扩展，提示应考察 per-destination 泛化或单模型条件输入目的节点的设计。
- **证据等级**：纯 NS-3 仿真、无统计检验说明、DNN 超参缺失，引用其数值结论时应注明仅仿真、细节不完整。
