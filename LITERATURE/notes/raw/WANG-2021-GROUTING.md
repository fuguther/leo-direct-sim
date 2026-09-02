# GRouting: Dynamic Routing for LEO Satellite Networks with Graph-based Deep Reinforcement Learning (WANG-2021-GROUTING)

它在问：时变拓扑+链路切换+负载不均下能否动态找最优路径？声称：line-graph MPNN 学网络表示（称可泛化任意拓扑以对付时变），DQN 在候选路径上选最优路由，最大化资源利用并保时延。证据：仿真，泛化依赖表示学习。不舒服处：动作是路径级而非逐跳——在 k-最短路径候选上选，最优路径不在候选集就无解；2021 年论文，规模与流量建模偏简单。谱系价值大于方法价值：二作 Yongyi Ran 即 GraphPR（TVT 2025，我们最近邻基线）核心作者，这是那条进化线的起点。与课题：line-graph 把链路特征织进表示，与我们 F1「第一跳物理链路显式加入」角度互补——他们隐式带，我们显式加，正好对照。

> 状态: 摘要；未核实字段: 星座规模、k 候选路径数、流量模型、公开代码
