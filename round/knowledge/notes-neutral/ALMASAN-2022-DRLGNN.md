# Deep RL meets GNNs: Exploring a Routing Optimization Use Case (ALMASAN-2022-DRLGNN)

> 来源: https://doi.org/10.1016/j.comcom.2022.09.029（Computer Communications 2022；arXiv 1910.07421 全文开放）

它在治 DRL 路由的老病：拓扑一换就得重训。方案是 edge-level MPNN + 目标/动作条件化的隐状态，智能体在中间点做转发决策，声称能泛化到训练中未见的拓扑。证据是 OTN demand 级仿真（流量需求分配而非逐包）。edge-level/action-conditioned 与"232 个未见拓扑"等架构与数字来自清单提示，摘要只确认 demand 级 OTN 场景和泛化主张——【未核实】。它重金投在"图表示"而非"信息新鲜度"。全文 arXiv 开放，值得精读核对架构与泛化协议。

**评级**：C

> 状态: 摘要；未核实字段: edge-level/action-conditioned 架构细节、"232 未见拓扑"数字、SDN/OTN 场景的具体流量模型、是否开源。


---

## 深读节（2026 全文精读增补）

**方法骨架**（节 IV-A~IV-D, ar5iv 行 489-720）：DQN + edge-level MPNN。图实体=链路而非节点；状态=链路可用容量 x1 + 链路介数 x2（"路径经过计数/总路径数"，收敛加速，IV-A）+ 动作向量（one-hot 带宽）。动作=该 (src,dst) 的 k=4 最短路径候选（按跳数），以"路径上链路的带宽分配特征"注入状态（IV-B）。GNN：T=7 轮消息传递（M 全连接生成消息→element-wise sum 聚合→RNN 更新隐状态，IV-C），readout=链路隐状态逐元求和→DNN→Q(s,a)。训练：SGD lr=1e-4、momentum 0.9、batch 32、replay 4000(FIFO)、ε 从 1.0 保持 70 迭代后指数衰减、γ=0.95、l2+dropout=0.1（行 1242-1268）。

**实验合同**（节 V、VI）：OTN 光网 demand 级分配（非逐包）。训练拓扑 14 节点 Nsfnet（链路 200 ODU0），另有 24 节点 Geant2；demand 带宽 8/32/64 ODU0；1000 次评估实验。基线=SoA DRL（文献[15]）、LB 随机 k 路径、Theoretical Fluid（容量比例拆分，非可实现上界）。指标=分配带宽 score、相对 fluid CDF。结果：Nsfnet 比 SoA DRL 多 6.6% 带宽、Geant2 多 3%；泛化=单 Nsfnet 训练→180 个合成拓扑（20-100 节点，NetworkX 随机图，平均度≈Nsfnet 的 3）+ 232 个 Topology Zoo 真实拓扑，100 节点仅 15% 性能下降；韧性=Geant2 随机移除 1-10 条链路仍优于 fluid；算力=i5-8400 CPU 上决策几 ms、随拓扑线性增长（VI-B）。未见训练 seed 数/多次重复标准误说明。

这提示：交付率 0/1 饱和量对局部改道不敏感，改道影响应转向时延/路径熵等连续量测量。
2. **AoI 空白正面交锋**——状态含"链路可用容量+介数"快照，从未问这些特征的新鲜度/传播年龄；动作条件化使 Q(s,a) 只能表达"此刻已知的容量"，信息过期的代价从未建模。
3. **ISL 利用率无关但启发**——OTN 场景无 ISL 概念；

危险——"80% 实验 >45% 改进"是相对另一 DRL 的相对量，baseline 弱时易虚高（行 117-124）；"100 节点仅 15% 下降"基于与 Nsfnet 平均度相似的随机图，结构多样性有限（行 186-200）；6.6%/3% 是带宽分配量未报时延/丢包，数字存疑位置行 108-118；全文未交代网络流量模型具体参数与开源状态（摘要笔记原"未核实"字段仍缺）。

> 深读状态: 全文已读[arXiv 1910.07421 v2, ar5iv HTML 全文 212KB, 2026-09-03]; 未核实: 训练 seed 数、流量模型具体参数、开源仓库、6.6%/3% 的置信区间。

