# PRIMAL: Asynchronous Risk-Aware Multi-Agent Packet Routing for Ultra-Dense LEO Satellite Networks (HE-2025-PRIMAL)

在问什么：超密星座同步假设不成立时，事件驱动+风险感知能否化解最短路径与拥塞回避的冲突。声称：各 agent 学完整代价分布、primal-dual 约束尾部风险（CVaR）；1584 星仿真，排队时延较 risk-oblivious 基线降超 70%，负载场景端到端减约 12ms。凭什么信：仿真；risk-oblivious 基线身份与对照口径未点名，-70% 要看是否同流量合同。不舒服：异步事件驱动天然产生陈旧信息，它容忍陈旧而不度量陈旧的价值；异步本身的训练稳定性也存疑。

> 状态: 摘要；未核实字段: risk-oblivious 基线身份、星座/流量细节、异步与同步机制、CVaR 实现

---

## 深读节（2026-09-03 全文深读）

**方法骨架**（§III-A–D）：包级 POCSMDP，状态=网络物理状态+包信息快照；动作=4 条出向 ISL（NSWE，无 wait/无 GSL 动作）；转移带可变时长 τ=单跳时延（半马尔可夫）；观测=包状态+本地节点/邻居统计（无任何年龄语义）；奖励=主目标（送达），K 个 QoS 代价函数 c_k（负载均衡）；§III-D 用 IQN（分布 RL）学习代价回报全分布，primal-dual 施加 CVaR 尾部约束（PRIMAL-CVaR），对照 PRIMAL-Avg 只约束期望。**"多智能体"实为各卫星独立学习（包轨迹回放），无智能体间通信**。训练采 max-entropy 约束 RL（§III-B）。

**实验合同**（§IV-A）：自研 Python+PyTorch 事件驱动仿真（github.com/skypitcher/risk_aware_marl）；Walker-Delta 22×72=1584 星、600km、倾角 53°、仰角≥15°、100ms 位置更新；GSL 1000Mbps / ISL **仅 50Mbps**、星/链缓冲各 16Mbit；包流 80% 64.8Kbit+20% 16.2Kbit，TTL=64；3 地面站（卢森堡/迪拜/北京）等概率收发=9 流量对；Poisson 10k 包/s、30s epoch、30 万包/run；基线=SPF、MADQN；指标：吞吐/丢包率/E2E 时延/排队时延/CVaR0.25 违反率（§IV-B 表 I）。








**危险信号**：ISL 50Mbps/3 站 9 流与真实星座数量级不符（§IV-A），-72.7% 排队时延需同口径复算；"异步"仅指各卫星独立训练、无 MARL 协同机制细节（§III）；SPF 84.8% 丢包=基线崩溃而非公平对照（表 I）。

> 深读状态: 全文已读[arxiv.org/html 2510.27506, 367KB HTML，Abstract/I/II/III/IV/V+表I 提取阅读]; 未核实: 表I 数字口径（E2E 62.0±85.0 等 std 异常）、async 训练稳定性细节、CVaR0.25 定义与种子数

