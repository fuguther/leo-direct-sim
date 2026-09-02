# DRL-Based Load-Balancing Routing Scheme for 6G Space-Air-Ground Integrated Networks (DONG-2023-DQNLLRA)

它在问：SAGIN 里 LEO 层高动态+负载不均如何做负载均衡路由？声称：逐跳 DQN，state 含邻居队列利用率+链路时延/带宽+跳数选下一跳；相对 Q-learning 基线，路径最大队列利用率 -5%、平均 -13%。证据：Remote Sensing 开放获取，仿真。不舒服处：①数字与我方提示「-8%/-15%」不一致——以摘要原文 5%/13% 为准，提示值未核实；②「最大队列利用率」是最脆的指标，改走几条热点路径就掉下来；③SAGIN 题目宏大、实验只在 LEO 小场景。与课题：其 state 设计正是我们 F0 阶梯后几档的同类内容——把这套状态喂给逐跳学习器，即可复测「信息增加是否带来聚合收益」。逐跳 DQN 粒度与我们一致，最容易自实现为对照基线（无代码）。

> 状态: 摘要；未核实字段: 与提示不一致的 -8%/-15%、星座参数（Iridium 72 未从摘要核实）、流量模型、公开代码

## 全文深读（2025-09-03 追加）

方法骨架：逐跳 DQN（每节点一 agent，Sec 4.1）；state S_i={D_ij,B_ij,C_i,C_j,QU_j,done}, j=1..4 邻居——链路时延/带宽+本节点与邻居到目的的最短跳数（Dijkstra 现算）+邻居队列利用率；action=4 邻居选一；reward（eq.2）按 (C_i≤C_j, QU_j≤0.5) 分四段加权 α(C_i−C_j)/p+β(1−QU_j)+γD_ij/q+ωB_ij/o，系数和=1，达目的 +1（eq.3）；防环=Ci−Cj 跳数梯度正负反馈（Sec 4.1）；ε 按 e^{−steps·0.4} 指数衰减（eq.5）；replay 4000、γ=0.99、两隐藏层、1 万随机流训练（Sec 5）。

实验合同（Sec 5）：Iridium 6×12=72（含 6 备用），networkX+官方轨道文件；但**每条 ISL 的时延/带宽是随机生成的**；70 条并发流制造动态；评估 100 对随机源宿 × 4 算法：Dijkstra / Dijkstra-QU / Q-learning[45] / DQN-LLRA；为"公平"给两个 ML 基线在决策节点周围降带宽（Sec 5，可疑调节）；指标=路径时延、路径最大/平均队列利用率；宣称：vs Dijkstra 最大队列利用率 −8%、平均 −15%；vs Q-learning −5%/−13%（Sec 5，与摘要一致——原摘要级笔记对 -8/-15 的存疑就此解决）；时延表现介于 Dijkstra 与 Dijkstra-QU 之间、优于 Q-learning。Win11/Python 3.9/PyTorch；数据按需提供、无代码。

对账：其 state 正是 F1 阶梯内容（局部队列+物理链路），但全部收益指标是**路径级队列统计**，通篇无丢包/交付/端到端业务指标——直接支持我们「路径改道≠聚合交付收益」的 F0/F1 警示（他们连交付都不测）；holding/access 完全缺席；state 皆假设决策时刻"实时"取得，无任何状态年龄——AoI-of-state 空白未被触碰。

可复用：逐跳 DQN 的 state/action/reward 模板（最易复现为 T1 对照组）；Ci−Cj 防环梯度；动态 ε 策略；反面教材：「决策节点降带宽」式公平性 hack。

危险信号：ISL 参数随机生成（非真实链路动力学，Sec 5）；公平性 hack 明显不利于 ML 基线比较的公平性；100 对源宿、单次运行、无 seed/方差；队列利用率类指标对热点路径极敏感（摘要级笔记已点）；无交付类指标。

> 深读状态: 全文已读[r.jina.ai 镜像转发抓取 MDPI Remote Sensing 15(11):2801 全文，Crossref 元数据核对]；未核实: 训练随机流分布、Q-learning 基线实现、seed 数
