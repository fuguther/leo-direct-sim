# ARXIV-2111.09217 · Information Freshness in Multi-Hop Wireless Networks（深读笔记）

> 深读日期：2026-09-03（深读助手）｜作者：Roy D. Yates 等（Rutgers，AoI 谱系权威）｜arXiv:2111.09217（ACM MSWiM 2021 版）｜来源：ar5iv.labs.arxiv.org/html/2111.09217

## 深读节

- **方法骨架**（非学习，控制=每时隙链路"发哪个流的包"，调度+路由联合）：
 ① 平稳随机化（III，行~122）：动作按固定概率 i.i.d. 激活，限单播+已知固定路径；闭式平均 AoI（等价单跳年龄问题，III-B1 Eq.9，行~209）；线网最小年龄 f_ej=1/(N−1) → A*=(N−1)²（IV 示例，行~320）。
 ② Age Difference（IV，行~262）：每时隙调度年龄差最大的链路 j*=argmax[A_j−A_{j−1}]，只用邻居年龄差，局部可实现。
 ③ Age Debt（V-A，行~338）：AoI 目标 α 转虚拟债务队列 Q(t+1)=[Q(t)+A(t+1)−α]⁺，Lyapunov drift 稳定化（V-B，行~394）；支持非线性代价（g_j^k）、单播/组播/广播、无需预指定路由；α 未知时梯度下降（V-C1，行~534）/流控（V-C2，行~605）在线逼近。
- **实验合同**：N 节点无向图 + 一般干扰约束；每边每时隙 1 包、时隙归一化；不可靠链路（成功概率 γ_e）；指标=加权和平均 AoI A_ave（II，Eq.2）与非线性年龄 B_ave（II，Eq.4）；数值（VI，行~652）为**单跳广播网络**（可靠/不可靠信道，N 节点，权重 w_i=i/N，链路概率均匀取自 [0.6,1]），基线=文献[15] max-weight 与 Whittle index；**无星座/LEO、无流量负载模型、seed 未报告**。结论：平稳随机化显著劣于其余；Age Difference 居中；Age Debt 以 max-weight 平均代价为目标向量时复现近最优（Fig.3）；流控/梯度下降版无需 α、小差距（Fig.3-4）。
- 保留"Age Difference 将局部年龄差用于调度决策"事实；保留"多跳平均年龄 O(hops²)（A*=(N−1)²，行~320）"；保留对论文 AoI 语义的刻画；保留 future work 列表（VII 行~693）；
- **可复用部件**：保留"Age Debt（Lyapunov drift+虚拟队列）、无需分布知识、支持流控"；Whittle/max-weight 基线命名（[15]）。**危险信号**：数值仅单跳广播（Fig.3-4），多跳无可比具体数字；链路仅 γ_e 概率抽象，无排队/时延分布；分析假定**时不变拓扑**（时变在 future work）；平稳随机化闭式依赖固定路径与 i.i.d.。

> 深读状态: 全文已读[ar5iv]; 未核实: Fig.3-5 具体数值与曲线、多跳数值实验细节、Whittle index 定义（文献[15]）
