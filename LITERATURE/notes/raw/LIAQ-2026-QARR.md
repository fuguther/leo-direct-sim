# Queue-Aware and Resilient Routing in LEO Satellite Networks Using Multi-Agent Reinforcement Learning (LIAQ-2026-QARR)

在问什么：队列感知+韧性打分能否让大规模 LEO 分布式路由抗链路失效。声称：per-sat DDQN（state=坐标+邻居队列+目的地+韧性分，提示称），重算开销约为 Dijkstra（5s 间隔）的一半且扩展性好；但摘要自认 Dijkstra 理想条件下时延最低。凭什么信：仿真；基线只有 SARSA+Dijkstra，无 DRL/GNN 同类对照，是清单里证据链最弱的一篇。不舒服：韧性分定义未获取；"queue-aware"我们在 F0 已做过且是负结果——队列感知本身卷不出差异，缺的正是一个信息价值/陈旧度维度。连接：可作弱基线；它的盲区恰是我们的机会点。

> 状态: 摘要；未核实字段: 韧性分定义、星座规模（提示称 Starlink shell1 1584 星）、流量模型、训练细节


## 深读追加（全文级）

**方法骨架**：MA-DRL/DDQN（IV节）。状态=本星坐标+4邻居坐标+各邻居队列+目的地坐标，另加4条链路韧性分特征(0~1)；动作=下一跳四方向（上/下/左/右）；奖励四组件=本星排队时延+距目的地距离缩减+环路惩罚+所选路径韧性分（IV）；韧性分 R^all=ω1(1−P_out^all)+ω2·max_{i,j}(max(1−q_i,1−q_j)·S_(i,j))（III-C，公式已核实，填补上稿"韧性分未获取"）；训练=全局Q网集中训练→下发各星+星上在线学习，DDQN+目标网+replay（表I：iter 10万、replay仅2000、batch128、ε0.99→0.1、Huber、Adam1e-4、3层DNN）。

**实验合同**：Starlink Shell1=72面×1584星、550km、Walker Delta；200地面站，星/地链路功率20/10W，带宽500MHz，fc30GHz，包64kb；流量=均匀/按人口分布的地面站背景流量，队列容量默认1Gb/s（V，表I）。基线 SARSA（集中训后拷贝）+Dijkstra；指标=时延/韧性分/丢块/开销；全文无 seed 与重复声明。

**对账**：① 队列感知正面交锋——这正是"邻居队列入状态"的同类方案，但 Abstract 自认 Dijkstra 理想时延最低，Fig.4 自证韧性分也输给 Dijkstra，且主比较显式把队容设 1Gb/s "隔离排队"（V）——等于默认队列信息不转化端到端性能，与我们 F0/F1 零差异互为印证；② 200 站配 1584 星，接入极宽松、无 holding 建模，卖点只剩开销（≈50% Dijkstra/5s重算），反衬 ISL 利用率<3%/holding-access 瓶颈判断；③ AoI-of-state 空白：状态全部取瞬时值，无信息年龄维度；其"缺全局视图所以输"的败因正是信息完整性梯度——我们的 AoI-of-state 恰是该梯度中间带。

**可复用**：集中训-分散部署+星上在线学习流程；韧性分公式可直接进我们奖励；均匀/人口双流量合同。**危险信号**：replay 2000 配 10万 iter（表I，稳定性存疑）；结果全在 Fig1-4 留图无数字、"丢包 negligible"无定义（V）；Fig.4 自证韧性分低于 Dijkstra；ε 衰减率1000语义含糊；正文含 GitHub issue 页眉噪声。

> 深读状态: 全文已读[arxiv.org/html/2605.04448]；未核实: seed/重复(未报告)、Fig1-4 具体数值、丢包定义、ω1/ω2 取值、在线学习超参
