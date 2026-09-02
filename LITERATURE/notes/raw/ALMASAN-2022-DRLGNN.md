# Deep RL meets GNNs: Exploring a Routing Optimization Use Case (ALMASAN-2022-DRLGNN)

> 来源: https://doi.org/10.1016/j.comcom.2022.09.029（Computer Communications 2022；arXiv 1910.07421 全文开放）

它在治 DRL 路由的老病：拓扑一换就得重训。方案是 edge-level MPNN + 目标/动作条件化的隐状态，智能体在中间点做转发决策，声称能泛化到训练中未见的拓扑。证据是 OTN demand 级仿真（流量需求分配而非逐包）。edge-level/action-conditioned 与"232 个未见拓扑"等架构与数字来自清单提示，摘要只确认 demand 级 OTN 场景和泛化主张——【未核实】。不舒服处：需求级抽象意味着队列、丢包、时延动态基本缺席，网络性能只体现为"需求能否满足"，与我们逐包仿真中"瓶颈在接入排队"的结论天然不可比。它重金投在"图表示"而非"信息新鲜度"，与 AoI-of-state 空白无关；但它是 GNN 路由泛化被引用最多的方法底座，edge-level 消息传递+动作条件化值得移植进我们的 GAT/MPNN 臂。全文 arXiv 开放，值得精读核对架构与泛化协议。

**评级**：C

> 状态: 摘要；未核实字段: edge-level/action-conditioned 架构细节、"232 未见拓扑"数字、SDN/OTN 场景的具体流量模型、是否开源。
