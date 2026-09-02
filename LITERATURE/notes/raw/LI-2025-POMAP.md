# Efficient Packet Routing for Large-Scale LEO Satellite Networks: A Pareto-Optimal MARL Approach With Queueing Theory (POMAP) (LI-2025-POMAP)

在问什么：时延+能耗+丢包多目标冲突时，如何让 MAPPO 稳定收敛且折衷可解释。声称：卫星建模为 G/G/1/K+AQM+加权优先级队列入环境，配 Pareto 优化，收敛稳定性与 Pareto 覆盖优于 SOTA。凭什么信：仿真（realistic 拓扑），基线名单摘要未点名。不舒服：排队状态多久同步一次、会不会过期，摘要没提——大概率没有信息陈旧度的位置；G/G/1/K 的泊松近似在 M-Lab 真实流量下未必成立【我的推测】。连接：与我们 holding/access 瓶颈分析同一工具箱，恰好对照"接入排队是瓶颈、ISL 利用率<3%"的实证；联合路由-调度方向的强参照。

> 状态: 摘要；未核实字段: 基线名单、星座规模与流量模型、S/A/R 细节（付费墙）、排队信息同步频率
