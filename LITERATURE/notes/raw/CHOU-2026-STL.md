# Spatial-Temporal Learning-Based Distributed Routing for Dynamic LEO Satellite Networks (CHOU-2026-STL)

在问什么：GAT（空间）+LSTM（时间）进 DQN，分布式路由能否预判并避开拥塞。声称：吞吐/丢包/队长/时延全面优于 conventional 与 learning-based 基线（含 GraphPR，提示称），队列最多减 23.26%，开销低、绿色。凭什么信：仿真。不舒服：规模小（提示称 45 星），比我们 280×14 小两个数量级，结论外推存疑；奖励 r=-(αD+βQ)、β>α（提示称，未核实）把队列权重压过时延，与我们的 F0 负结果（局部队列不改变聚合交付率）正面打架【我的推测：分歧多半来自流量压力合同不同】。连接：状态组成、奖励权重都是可直接对照的变量，适合进我们的对照实验表。

> 状态: 摘要；未核实字段: 星座规模、奖励权重、状态组成、基线与流量模型
