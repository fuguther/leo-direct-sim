# PRIMAL: Asynchronous Risk-Aware Multi-Agent Packet Routing for Ultra-Dense LEO Satellite Networks (HE-2025-PRIMAL)

在问什么：超密星座同步假设不成立时，事件驱动+风险感知能否化解最短路径与拥塞回避的冲突。声称：各 agent 学完整代价分布、primal-dual 约束尾部风险（CVaR）；1584 星仿真，排队时延较 risk-oblivious 基线降超 70%，负载场景端到端减约 12ms。凭什么信：仿真；risk-oblivious 基线身份与对照口径未点名，-70% 要看是否同流量合同。不舒服：异步事件驱动天然产生陈旧信息，它容忍陈旧而不度量陈旧的价值——绕开了我们最关心的问题；异步本身的训练稳定性也存疑。连接：与我们极端拥塞压力合同最接近之一，CVaR 尾部约束可移植；异步=信息陈旧的自然来源，属机制近邻而非设定继承。

> 状态: 摘要；未核实字段: risk-oblivious 基线身份、星座/流量细节、异步与同步机制、CVaR 实现

---

## 深读节（2026-09-03 全文深读）

**方法骨架**（§III-A–D）：包级 POCSMDP，状态=网络物理状态+包信息快照；动作=4 条出向 ISL（NSWE，无 wait/无 GSL 动作）；转移带可变时长 τ=单跳时延（半马尔可夫）；观测=包状态+本地节点/邻居统计（无任何年龄语义）；奖励=主目标（送达），K 个 QoS 代价函数 c_k（负载均衡）；§III-D 用 IQN（分布 RL）学习代价回报全分布，primal-dual 施加 CVaR 尾部约束（PRIMAL-CVaR），对照 PRIMAL-Avg 只约束期望。**"多智能体"实为各卫星独立学习（包轨迹回放），无智能体间通信**。训练采 max-entropy 约束 RL（§III-B）。

**实验合同**（§IV-A）：自研 Python+PyTorch 事件驱动仿真（github.com/skypitcher/risk_aware_marl）；Walker-Delta 22×72=1584 星、600km、倾角 53°、仰角≥15°、100ms 位置更新；GSL 1000Mbps / ISL **仅 50Mbps**、星/链缓冲各 16Mbit；包流 80% 64.8Kbit+20% 16.2Kbit，TTL=64；3 地面站（卢森堡/迪拜/北京）等概率收发=9 流量对；Poisson 10k 包/s、30s epoch、30 万包/run；基线=SPF、MADQN；指标：吞吐/丢包率/E2E 时延/排队时延/CVaR0.25 违反率（§IV-B 表 I）。

**与我们对账**：
1. **F0/F1 零差异的镜像证据**：所有学习算法丢包率都 ≈0.00%（表 I）——路由决策在变（MADQN 73.4ms→PRIMAL-CVaR 61.5ms、排队时延 17.6→4.8ms，-72.7%），但**交付(丢包)零差异**，收益只落在时延/排队指标。直接反哺我们："信息阶梯零交付差异"或需在时延/队列指标下复查，或我们的网络比其 50Mbps-ISL+10k包/s 更不拥塞。
2. **ISL 利用率<3% 的工程注脚**：其拥塞是**刻意工程化**的（ISL 仅 50Mbps 远低于真实 Starlink ~10Gbps），SPF 丢包 84.8% 说明环境重度拥塞才有 RL 增益；我们的 M-Lab 分散流量+动态 MCS 天然不拥塞——呼应"ISL<3% 时信息增益=0"。
3. **holding/access 瓶颈反向**：其 GSL(1000Mbps)比 ISL(50Mbps)快 20 倍，瓶颈在星间链路而非我们实测的 holding/access；其卫星仅 FIFO+丢包，无 holding 概念。
4. **AoI-of-state 空白确认**：异步事件驱动天然容忍陈旧，观测"本地邻居统计"无时间戳/年龄字段，全文不量化陈旧损伤——仍是空白。

**可复用部件**：IQN 分布批判器 + CVaR 约束（可移植到我们 DDQN/GAT 的队列代价）；包级 episode+事件驱动（与 SimPy 事件驱动同构）；3 城市 Poisson 10k 包/s 作工程拥塞压力测试；primal-dual 约束 RL 写法。
**危险信号**：ISL 50Mbps/3 站 9 流与真实星座数量级不符（§IV-A），-72.7% 排队时延需同口径复算；"异步"仅指各卫星独立训练、无 MARL 协同机制细节（§III）；SPF 84.8% 丢包=基线崩溃而非公平对照（表 I）。

> 深读状态: 全文已读[arxiv.org/html 2510.27506, 367KB HTML，Abstract/I/II/III/IV/V+表I 提取阅读]; 未核实: 表I 数字口径（E2E 62.0±85.0 等 std 异常）、async 训练稳定性细节、CVaR0.25 定义与种子数

