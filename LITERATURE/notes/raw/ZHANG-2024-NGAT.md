# Graph Attention Reinforcement Learning for Multicast Routing and Age-Optimal Scheduling (ZHANG-2024-NGAT)

> 来源: https://arxiv.org/abs/2404.18084（2024 preprint）

它问的是组播路由（Steiner 树）与调度的联合优化如何最小化期望平均 AoI，用分层 RL 把两级决策拆开，图嵌入用带收缩映射证明的 NGAT。声称比传统组播算法最高快 9.85 倍，近似比 1.1–1.3 与 SOTA 相当，且在 AS-733 等四个数据集上泛化到未见拓扑。证据：四个数据集上的仿真。注意它的 AoI 仍是接收端数据龄，与 LUR 同类，和我们的"路由状态年龄"空白无关。真正与我们相关的是两处机制：NGAT 的归一化+收缩映射为图注意力的稳定性提供了理论抓手，值得移植进我们 GAT 臂；分层路由/调度拆解与我们的联合路由-调度方向结构相似（但它是集中式分层，我们是一体的）。非 LEO、有线 ISP 图，方法价值大于应用价值。摘要之外的分层细节与超参未核实，精读 arXiv 全文可补。

**评级**：B

> 状态: 摘要；未核实字段: 分层 RL 的具体两级目标划分、NGAT 超参、数据集规模细节、是否开源。
