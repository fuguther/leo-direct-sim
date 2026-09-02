# Fully-Distributed Dynamic Packet Routing for LEO Satellite Networks: A GNN-Enhanced Multi-Agent Reinforcement Learning Approach (GraphPR) (RAN-2025-GRAPHPR)

在问什么：能不能让每颗卫星只用一跳邻居信息做逐包分布式路由。声称：GAT 把一跳信息编码成隐含多跳表示，RSPH 残余最短跳数防环，丢包率/时延/吞吐/平均队长全面优于基线。凭什么信：仿真；摘要没给星座规模、流量模型、基线名单，letter 篇幅细节单薄。不舒服：RSPH 本身消费解析可得的最短跳数信息，它和 GNN 谁贡献大归因不清；逐包决策意味着每包都过一跳信息交换，通信量化缺失。连接：设定与我们的 POMDP+局部队列+全分布式最接近，但通篇没有"信息有多旧/值多少钱"的位置——正是我们 F0/F1 信息阶梯想问的。无公开代码（提示称未公开，未核实）。

> 状态: 摘要；未核实字段: 星座规模、流量模型、基线名单、RSPH 与 GNN 各自贡献、代码是否公开、逐包信息交换频率
