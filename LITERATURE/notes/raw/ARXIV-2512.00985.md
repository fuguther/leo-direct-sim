# ARXIV-2512.00985 · Age-Optimal Sampling and Routing under Intermittent Links and Energy Constraints（深读笔记）

> 深读日期：2026-09-03（深读助手）｜作者：A. U. Atasayar, Aimin Li, Ç. Arı, Elif Uysal（METU CNG）｜arXiv:2512.00985（前身 ACM MobiHoc 2025，ref[1]）｜来源：arxiv.org/html/2512.00985

## 深读节

- **方法骨架**：单源→多路由状态更新系统，无限时域约束半马尔可夫决策过程（CSMDP，III Problem 1，行~375）：目标=最小化长期平均单调非线性 AoI 惩罚 f(Δ)（II-D，Eq.4），受长期平均能量约束（传输+每次采样代价 C_s·N_s(T)，Eq.5）与路由可用性约束；混合状态空间（连续年龄 y + 离散路由可用性向量 l，支持相关随机时延）。解法=二分 Lagrange 乘子 λ + 相对期望动作值迭代 Bisec-ReaVI（V-B，行~743）+ Dinkelbach 分数规划改写（III-A）。结构定理：最优采样=分段线性等待（阈值）策略、路由=阈值型（IV Theorem 1，行~570，证明仅 sketch）。非学习方法：无 GNN/RL，需已知各路由时延分布 Q_r。
- **实验合同**：非星座仿真——仅 N=2~3 条抽象路由（VII-C Table I：Route1 固定可用 Gamma(6,2,1)，Route2 间歇 Log-normal(5,4,p)，Route3 Gamma(3,7,p)）；LEO 路由时延=对数正态（VII-B1 Eq.48-49），地面=Gamma（VII-B2）；无队列/争用/流量负载模型；**seed 未报告**。基线：MAD-Optimal（最小均时延路由+AoI 最优等待）、MAD-Zero Wait、单路由最优（VII-A，行~1102）。指标=平均惩罚代价（Table II/III），Ycap=50、多数 Emax=∞。
- **与我们对账**：① 我们最刺痛的点（信息阶梯改道~1/3 但交付率零差异）此文恰好反向佐证：路由选择的价值只在 AoI 惩罚度量、且惩罚陡峭时显现——α=1 时最优比最佳单路由惩罚低 ~60%（VII-D1 行~1340），时延/交付率度量下改道无收益 → 度量-决策解耦是共性现象，不是我们仿真独有的；② 路由可用性 p_k（II-A 行~289）即我们 holding/access 瓶颈的显式随机化：p 小时 MAD-Zero Wait 反劣于简单策略、与最优差距收窄（VII-D3 行~1358）→ 支持把接入可用性作为状态分量而非仅链路几何；③ AoI 仍是"数据更新年龄"（对端收到的最新样本年龄），与"路由决策状态年龄"无关 → AoI-of-state 空白依旧成立。
- **可复用部件**：p_k 可用性 on/off 建模、能量约束 Lagrange 处理、阈值策略作 RL 行为先验。**危险信号**：只有 2~3 条抽象路由、无真实星座/争用，Table II/III（惩罚代价 α=0.1→1）、VII-D2 能量数（联合最优 E=4.14 vs 单路由 E1=3.4/E2=2.75，行~1348）均系玩具参数下数值，不可外推；"高方差路由反而有益"结论强依赖特定分布配置；无 seed/重复实验报告。

> 深读状态: 全文已读[arxiv.org/html/2512.00985]；未核实: Table I-III 完整数值、Fig.4-7 曲线细节、Theorem 1 完整证明、Fig.5 的 Emax 具体取值
