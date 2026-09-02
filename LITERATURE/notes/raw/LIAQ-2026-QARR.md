# Queue-Aware and Resilient Routing in LEO Satellite Networks Using Multi-Agent Reinforcement Learning (LIAQ-2026-QARR)

在问什么：队列感知+韧性打分能否让大规模 LEO 分布式路由抗链路失效。声称：per-sat DDQN（state=坐标+邻居队列+目的地+韧性分，提示称），重算开销约为 Dijkstra（5s 间隔）的一半且扩展性好；但摘要自认 Dijkstra 理想条件下时延最低。凭什么信：仿真；基线只有 SARSA+Dijkstra，无 DRL/GNN 同类对照，是清单里证据链最弱的一篇。不舒服：韧性分定义未获取；"queue-aware"我们在 F0 已做过且是负结果——队列感知本身卷不出差异，缺的正是一个信息价值/陈旧度维度。连接：可作弱基线；它的盲区恰是我们的机会点。

> 状态: 摘要；未核实字段: 韧性分定义、星座规模（提示称 Starlink shell1 1584 星）、流量模型、训练细节
