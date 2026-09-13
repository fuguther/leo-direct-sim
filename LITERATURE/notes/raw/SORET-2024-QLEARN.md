# Q-learning for Distributed Routing in LEO Satellite Constellations (SORET-2024-QLEARN)

它在问：星座路由能否不依赖地面段、只靠邻居局部信息做得不逊于集中式？声称：多智能体 POMDP；表格 Q-routing 现代化版，利用邻居信息与节点决策相关性；稳态时延与两个集中式最短路径基准相当（含吃瞬时排队时延的 genie 上界），支撑负载更高、信令开销最小。证据：仿真。把时延拆成传播+排队两段；同组 MA-DRL 模拟器公开（SatCom-TELMA/MA-DRL_Routing_Simulator，已核存在）。不舒服处：表格 Q 状态空间极小，「邻居信息」的时间维度装不进去。

> 状态: 摘要；未核实字段: 星座规模/流量/队列模型、论文与公开模拟器的对应关系（模拟器存在已核于 2026-08-13 survey）
