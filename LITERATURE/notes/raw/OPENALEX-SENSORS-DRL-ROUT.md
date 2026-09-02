# Deep Reinforcement Learning-Based Routing Method for LEO Mega-Constellation Satellite Networks with Service Function Constraints (OPENALEX-SENSORS-DRL-ROUT)

## 全文深读（2025-09-03 追加；raw/ 下原无此篇摘要级笔记，本文件为深读笔记新建）

方法骨架：GDRL-SFCR = GCN（L=2，嵌入 d=6）+ PPO(actor-critic)，集中式训练于 NCC（Sec 4.3）。state 六元组=源/目的/当前节点/节点负载/已过 SFC 功能节点数/邻居集（Sec 4.1a）；action=下一跳 one-hot（Sec 4.1b），探索期直接屏蔽违反 SFC 顺序的动作并把 SFC 元数据嵌入 GNN 消息传递（Sec 3.4）；reward 分段（eq.19）：成环（u∈Vis）罚 −1，到目的且 RF=FN 加 +1，常规 −(RL+RF+RT)（负载/功能数/时延三奖励）；防环=Vis 集合惩罚。

实验合同：6048 星（84 轨×72、倾角 53°、550km，仿 Starlink，Sec 5.1.1）+ 地面站 + WorldPop v4 用户终端；SGP4/TLE 轨道（Sec 3.1）；ISL 自由空间损耗（eq.4-6）、星地链路按 3GPP TR 38.811 市区模型（Sec 3.2）；流量 size 服从 lognormal [5,100]Mb、双向端到端；1000 次仿真（Sec 5.1.1）；基线 SFC-APS（图论）/DQN-LBR/DQR（Sec 5.2）；指标：接入成功率/平均负载/端到端时延/网络容量/运行时间；PPO clip 0.2、γ=1、Adam lr 1e-4、OpenRL 加速（Sec 5.1.2）。宣称：接入率 +19.1%、负载 −14.1%、时延 −11.3%、容量 2 倍+（Sec 5.4）。

对账：它是四篇里唯一把用户接入链路+NTN 端到端双向流量建进模型的（贴近我们 holding/access 瓶颈），但指标是路径级可达率/容量，未做瓶颈归因，"路径改变≠交付收益"的 F0/F1 警示对它依然成立；state 全为实时值、无状态年龄——AoI-of-state 空白无一处被触碰（其引文 [45] 是 LEO 信息更新年龄优化，属另一问题，可作我们 AoI 引证素材）。

可复用：Vis 防环+终局 bonus 奖励整形（eq.19）；SFC 违例动作屏蔽机制；6048 节点图上的 GNN+PPO+OpenRL 训练管线；θ1 权重敏感性协议（Fig.7）。

危险信号：Fig.3-6 图注把基线 DQN-LBR 标为"本文提出"（Sec 5.4 图注误标）；γ=1 无折扣；1000 次仿真未见 seed/方差说明；TM/gNB/NGC 功能节点随机分配削弱 SFC 场景真实性；"容量翻倍"按缓存占用率口径（eq.18）而非真实吞吐；无公开代码（Data Availability 仅"data contained within article"）。

> 深读状态: 全文已读[r.jina.ai 镜像转发抓取 MDPI Sensors 25(4):1232 全文，Crossref 元数据核对标题/DOI]；未核实: seed 数与方差统计、功能节点部署真实性、实验结果分布、开源代码
