# LEO Satellite Network Routing Algorithm Based on GNNs and DQN (SHI-2024-GNNDQN)

> 来源: https://doi.org/10.3390/app14093840（Applied Sciences 2024）

它在问：用 GraphSAGE 的归纳式嵌入把拓扑塞给 DQN，LEO 路由能不能学到可迁移策略。声称吞吐比 Dijkstra 高 29.47%、比纯 DQN 高 18.42%，时延分别降 39.76%/15.29%，且能适应拓扑变化。证据是仿真，但摘要没有任何星座动力学、流量模型与统计细节；据清单提示其训练/评估用地面 NSFNet 而非真实星座，此点未能从公开源核实【未核实】。队列、丢包、AoI 全线缺席，是典型的"只看拓扑"的信号级评估。与我们课题的连接：可作 GraphSAGE+DQN 逐跳的对照基线，它信息贫乏的状态恰好反衬我们 F0/F1 阶梯里"加了局部队列+广告后 1/3 ISL 路径变了但聚合交付率零差异"的结论——说明路径改变并不等于收益。风险：宣称的百分比缺乏方差与场景细节，基线可比性存疑，不能直接引用数字。MDPI 开放获取，值得精读核对实验设置。

**评级**：A

> 状态: 摘要；未核实字段: 训练/评估拓扑（据提示为 NSFNet）、星座动力学模型、百分比统计细节、是否开源。

## 全文深读（2025-09-03 追加）

方法骨架：GNN-DRL=GraphSAGE（2 层、均值聚合、q 邻居采样）+ DQN，逐节点分布式决策+集中式训练（Sec 2.2/4）；因 GraphSAGE 不吃边特征，先把边属性聚合成节点特征（Algorithm 1，Sec 2.1），节点特征 x_i=[q_i, v'_i]（流量+链路容量/时延聚合）；state=链路时延/容量/利用率零填充向量+用户侧 (src,dst,bw)（Sec 2.2）；action=邻居选下一跳；reward R=α·W−β·L（吞吐与速率，eq.2）；**方法混用**：先写 DQN，又引入 advantage A=Q−V=R−V(π) 与 policy-gradient 更新（eq.9-10，Sec 4）；T=5 轮消息传递、batch 50、Adam 2e-4 指数衰减（Sec 5）。

实验合同（Sec 5）：**核心场景造假级替代——训练与评估都用 NSFNet 地面拓扑（KDN 数据集，OMNeT++ 生成）代替 LEO 星座**，原文明言 "Since the LEO networks lack of the dataset for training, we use NSFNet dataset instead"；"拓扑变化"=禁用 NSFNet 节点；每链固定 100Mbps；基线 Dijkstra/DQN；指标=平均吞吐、平均端到端时延；宣称：吞吐 +29.47%/+18.42%、时延 −39.76%/−15.29%（vs Dijkstra/DQN）；节点失效场景时延 −29.46%/−17.29%；30 节点规模 −30%/−22%（Fig.7-11）；TensorFlow+OpenAI Gym、Ubuntu 20.04、AMD 3950X、GTX 3080。

对账：在 14 节点级地面拓扑上验证"LEO 路由"、与真实星座动力学无关——其百分比是场景伪影，不能支撑 LEO 主张，直接佐证我们「文献收益多为场景产物」的判断；flow 级分配粒度报出收益，与我们 F0/F1 包级动态、聚合交付零差异形成对照：收益宣称对粒度/瓶颈位置高度敏感；holding/access/AoI 全线缺席——AoI-of-state 空白维持。

可复用：边→节点特征重构图技巧（Algorithm 1）；GraphSAGE+DQN 逐跳模板；KDN/NSFNet 数据集可作非 LEO 对照组参照。

危险信号：场景替代无误差讨论；DQN 与 policy-gradient/advantage 混用（Sec 4）；无星座、无 seed、百分比无方差；"适应拓扑变化"实为 14 节点图上禁用节点的弱测试；结论称其方法"more suitable for real networks"（Sec 6）——过度声称。

> 深读状态: 全文已读[r.jina.ai 镜像转发抓取 MDPI Applied Sciences 14(9):3840 全文，Crossref 元数据核对]；未核实: KDN/NSFNet 节点数、seed/随机性、DQN 与 policy 的具体实现
