# GRLR: Routing With Graph Neural Network and Reinforcement Learning for Mega LEO Satellite Constellations (ZHANG-2025-GRLR)

在问什么：mLEO 只用解析稳定的 4 条 ISL 做分布式逐跳路由，GNN 提特征、Actor-Critic 决策。声称：收敛快，时延与网络动态适应性优于基线。凭什么信：仿真，基线名单和星座规模摘要都没给。不舒服：建 MDP 而非 POMDP，等于默认每颗星拿全知精确状态，绕过了部分观测这个核心难题；队列/AoI 未建模（提示称），拥塞表现是空窗；"动态适应性"指拓扑还是流量动态，含糊。连接：与 GraphPR 同刊，可作"无队列感知、纯拓扑+启发式决策"的对照——我们 F0/F1 负结果（加队列+广告不改变聚合交付率）恰好给这类设计泼冷水。无公开代码（未核实）。

> 状态: 摘要；未核实字段: 基线名单、星座规模、流量/故障模型、代码是否公开
