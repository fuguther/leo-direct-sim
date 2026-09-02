# Dynamic Routing for Integrated Satellite-Terrestrial Networks: A Constrained Multi-Agent Reinforcement Learning Approach (CMADR) (LYU-2024-CMADR)

在问什么：地面站参与转发的天地一体化里，能耗/丢包约束下如何压时延。声称：Lagrangian 约束 MARL，策略与乘子同步更新，OneWeb/Telesat 上时延最少降 21%/15% 且约束满足，有消融。凭什么信：仿真+真实星座参数。不舒服：乘子更新收敛出了名地难，风险被跳过；地面站参与改变了问题边界，与纯 ISL 直连脱耦，可借鉴的只剩约束处理本身；"最少 21%/15%"的基线是谁摘要没点名。连接：瓶颈感知拥塞控制可抄它的 Lagrangian 法；精读优先级低于 GraphPR/POMAP。年期未核实（S2 记 2023，DOI 标 JSAC 2024）。

> 状态: 摘要；未核实字段: 基线名单、约束具体取值、乘子收敛细节、发表年期
