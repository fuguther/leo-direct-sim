# GRouting: Dynamic Routing for LEO Satellite Networks with Graph-based Deep Reinforcement Learning (WANG-2021-GROUTING)

它在问：时变拓扑+链路切换+负载不均下能否动态找最优路径？声称：line-graph MPNN 学网络表示（称可泛化任意拓扑以对付时变），DQN 在候选路径上选最优路由，最大化资源利用并保时延。证据：仿真，泛化依赖表示学习。不舒服处：动作是路径级而非逐跳——在 k-最短路径候选上选，最优路径不在候选集就无解；2021 年论文，规模与流量建模偏简单。二作 Yongyi Ran 即 GraphPR（TVT 2025）核心作者。

> 状态: 摘要；未核实字段: 星座规模、k 候选路径数、流量模型、公开代码
