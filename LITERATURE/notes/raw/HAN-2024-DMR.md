# DRL-Based Multipath Routing for LEO Megaconstellation Networks (HAN-2024-DMR)

它在问：mega 星座下多径发现与流量调度怎么做？声称：拆成最小跳多径发现（MHMRD）+GNN 流量调度（GMTS）；GMTS 依据 ISL 状态与流量需求为每条流分配各路径流量；相对 SPF，吞吐 +42.64%、完成率 +17.39%、时延也「提升 3.66%」（原文如此，方向存疑）；可跨星座免重训。证据：MDPI 开放获取仿真，可补读全文。不舒服处：「时延提升 3.66%」在吞吐大涨 42% 背景下疑似吞吐换时延；与 GMR 高度同源，独立性有限；集中式流级动作；MHMRD 按最小跳发现路径，对时变链路速率不敏感——与我们 MCS 动态链路速率设定直接相关。与课题：ISL 状态进 GNN 的输入时刻正是状态年龄问题的切片；无公开代码，作多径方法论参照，不作基线。

> 状态: 摘要；未核实字段: 仿真星座规模/流量模型、「时延 +3.66%」数值方向、公开代码；MDPI 开放获取可补读全文

## 全文深读（2025-09-03 追加）

方法骨架：DMR=MHMRD+GMTS 两段解耦（Sec 4）。MHMRD：Walker Delta 轨道几何闭式跳数（eq.11-21：跨轨 Hh、轨内 Hv 四方向）求最小跳路径集，备用路径用链路占用率阈值+随机权 r1<r2<r3（无 seed 说明）逐条剔除生成，O(N logN)，集中 NCC/SDN 执行。GMTS：GNN+PPO(actor-critic)+优先经验回放（TD-error 优先级与 IS 权重，eq.32-39）；state s_t={C_t 剩余带宽、TR_t 需求矩阵、G_t、P_t 路径矩阵}（Sec 4.2.1）；action=各候选路径流量比例向量 ω（Sec 4.2.2）；reward r_t=效用 U(吞吐,时延)（eq.26，Sec 4.2.3）；「GNN 使模型对变拓扑/变规模免重训」为设计卖点（Sec 4.4），但 GNN 具体结构描述很薄。

实验合同（Sec 5）：NS3；Iridium 66（极轨）+ OneWeb 648（18 轨×36）；流量按地面人口密度生成、50 个源宿对；训练用倾斜轨道星座+MAWI 流量矩阵[J37]；基线 SPF/NCMCR/AMBRLB/DDPG-TE + MHMRD 等分共 5 方案；指标=平均吞吐/流完成率/端到端时延，每数据点=5 个连续拓扑快照平均（Sec 5.2.1）；Python 3.9+PyTorch 1.14。宣称：Iridium 上吞吐 +30.26% vs SPF、+8.45% vs NCMCR（上限负载）、时延 −3.67% vs SPF；OneWeb @8Gbps 吞吐 +42.64% vs SPF、+9.55% vs NCMCR；完成率 +17.39%（Iridium）/+11.52%（OneWeb）vs SPF；低负载时 SPF 时延最低（Sec 5.2.3）；Iridium 训练直接部署 OneWeb（免重训）。

对账：state 含 ISL 剩余带宽+需求矩阵，全为"实时"假设值、无状态年龄——AoI-of-state 空白未被触碰；其收益靠集中式完美状态+流级拆分，与 F0/F1 零差异形成直接张力：关键差异在**场景**——他们 ISL 受限、无接入瓶颈，我们压力在 holding/access，info 价值取决于瓶颈位置，这正支持瓶颈感知方向；ISL 利用率未报告；unidirectional flow 级，无包级动态。

可复用：MHMRD 的 Walker 闭式跳数公式（eq.11-21）可作我们 280×14 的解析路径枚举/校验基准；PPO+优先回放训练协议；「5 快照平均」协议（警示：样本太少）。

危险信号：摘要把 OneWeb 的 42.64% 与 Iridium 的 17.39%/3.66% 混作一句宣称（误导性聚合）；「时延提升 3.66%」实为高负载下 −3.67%、低负载 SPF 最优（摘要措辞误导，摘要 3.66% 与正文 3.67% 还不一致）；备用路径随机权重无 seed；结论称"每路由节点由 DQN agent 控制"与正文 PPO actor-critic 矛盾（Sec 4.2 vs Sec 6）；无 seed/方差；代码仅邮件索取（hanchi@hgd.edu.cn）非公开。

> 深读状态: 全文已读[r.jina.ai 镜像转发抓取 MDPI Electronics 13(15):3054 全文，Crossref 元数据核对]；未核实: 流量生成细节/负载档、MHMRD 随机权重 seed、训练曲线
