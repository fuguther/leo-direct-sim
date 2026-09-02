# PRIMAL: Asynchronous Risk-Aware Multi-Agent Packet Routing for Ultra-Dense LEO Satellite Networks (HE-2025-PRIMAL)

在问什么：超密星座同步假设不成立时，事件驱动+风险感知能否化解最短路径与拥塞回避的冲突。声称：各 agent 学完整代价分布、primal-dual 约束尾部风险（CVaR）；1584 星仿真，排队时延较 risk-oblivious 基线降超 70%，负载场景端到端减约 12ms。凭什么信：仿真；risk-oblivious 基线身份与对照口径未点名，-70% 要看是否同流量合同。不舒服：异步事件驱动天然产生陈旧信息，它容忍陈旧而不度量陈旧的价值——绕开了我们最关心的问题；异步本身的训练稳定性也存疑。连接：与我们极端拥塞压力合同最接近之一，CVaR 尾部约束可移植；异步=信息陈旧的自然来源，属机制近邻而非设定继承。

> 状态: 摘要；未核实字段: risk-oblivious 基线身份、星座/流量细节、异步与同步机制、CVaR 实现
