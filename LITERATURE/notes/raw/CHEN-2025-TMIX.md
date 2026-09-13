# A Distributed Routing Algorithm for LEO Satellite Networks: A Multiagent Transformer-MIX Learning Approach (CHEN-2025-TMIX)

它在问：动态拓扑+突增流量下，每星只看局部观测做逐跳决策，CTDE 协作能否逼近全局最优 E2E 时延？声称：每星一个智能体、局部观测独立决策，「统一负载均衡奖励」+Transformer-MIX 聚合联合动作价值，训练更稳更快；ISL 失效 18% 时 E2E 时延 -13.6%、投递率 +5.4%。证据：自研仿真，星座规模/流量模型/基线都不给，无公开代码。关键假设「局部观测足以支撑全局负载均衡」：他们没度量局部状态里有多少过期信息。

> 状态: 摘要；未核实字段: 星座规模/流量模型/基线方案、仿真参数、公开代码
