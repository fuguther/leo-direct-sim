# A Robust Routing Strategy Based on Deep Reinforcement Learning for Mega Satellite Constellations (RRS-DRL) (CHU-2023-RRSDRL)

在问什么：链路性能劣化时，把数据 AoI 当优化目标能否做鲁棒路由。声称：RRS-DRL 平均 AoI 更低、资源利用更好，比最短路径更鲁棒（提示称 Starlink 175 星；奖励含到目的距离+下一跳 AoI+队列增长率——均未核实）。凭什么信：仿真，对照只有最短路径——最弱的单一基线。不舒服：AoI 是被转发数据的年龄，与路由决策所用状态的信息不是同一对象；"为何 AoI 目标能抗干扰"的机制解释缺失。

> 状态: 摘要；未核实字段: 奖励函数细节、jamming 模型、星座规模与具体数值
