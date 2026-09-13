# Generalizable Policy Learning using GNNs (WIGMORE-2025-MAGNN)

> 来源: https://doi.org/10.1145/3704413.3764422（ACM MobiHoc 2025，OA）

它把路由策略定成输出"路由系数"（静态或状态依赖的流拆分比例），而非逐包动作——连续、类 OSPF 权重、可直接部署。Multi-Axis GNN 跨流量类别交换矩阵值节点/边特征、保置换不变性，用 model-free 的 Network Performance Gradient Algorithm 训练，目标含平均/最坏时延与功耗。声称在多样未见网络上超过最短路与 backpressure。证据：多跳多商品随机排队网络仿真。控制粒度特点：路由系数级决策天然避免逐包动作维度爆炸。不舒服处：它面向平稳排队均衡的最优分流，对 MCS 动态速率、ISL 中断、以及"状态信息本身会过时"都不建模；多类别矩阵特征与简化单级流量抽象存在错位。OA PDF 可下。

**评级**：B

> 状态: 摘要；未核实字段: MA-GNN 消息传递的具体公式、NPGA 的方差/收敛细节、拓扑规模与流量分布设定、是否开源（ACM OA 全文可查）。
