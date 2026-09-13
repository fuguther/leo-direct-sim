# Age-Optimized Multihop Information Update Mechanism on the LEO Constellation via Continuous Time-Varying Graphs (LI-2023-LUR)

> 来源: https://doi.org/10.1109/JIOT.2022.3229028（IEEE IoT-J 2023）

它在问：多跳 ISL 转发里怎么选路，才能让数据到达得最"新鲜"。做法是连续时变图上求（传输时延, 到达率）的最优配对，LUR 扫满足有效约束的到达率、取最小龄的路径集。声称平均 AoI 比最短时延路径（SDP）最大降 12.66%、比 MST 降 75.28%、比 MAoIG 降 69.3%。证据是集中式数值仿真，非学习、非分布式。

**评级**：B

> 状态: 摘要；未核实字段: 星座规模/ISL 中断模型细节、LUR 复杂度与运行成本、是否开源（大概率无）。
