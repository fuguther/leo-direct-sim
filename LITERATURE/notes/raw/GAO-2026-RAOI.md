# Toward the Age in Forwarding: A Deep Reinforcement Learning Enabled Routing Mechanism for Large-Scale Satellite Networks via Spatial–Temporal Graph Neural Networks (ADRLRM) (GAO-2026-RAOI)

在问什么：高时效业务能否把"数据转发新鲜度"直接做成路由优化目标。声称：提出 RAoI（Routing-aware AoI）塞进 DRL 奖励，配 PTSA 分槽的时空 GNN 提取拓扑特征，时延/跳数/平均 RAoI 胜过 OSPF、DQN-IR、GraphPR。凭什么信：仿真，基线含 GraphPR，对标意识强。不舒服：RAoI 度量被转发数据的年龄，不是路由决策信息的年龄——它是我们已知空白的镜像而非答案；RAoI 自身的计时/携带开销摘要没说。连接：与 CHU 的 RRS-DRL 构成"数据 AoI 入奖励"小谱系；同一机制把对象换成"路由状态"就是我们想做的实验【我的推测：把奖励从数据 AoI 换成状态 AoI 的工程改动不大，但问题语义与实验设计完全不同】。

> 状态: 摘要；未核实字段: 星座规模、RAoI 精确定义与开销、PTSA 机制细节、具体性能数值
