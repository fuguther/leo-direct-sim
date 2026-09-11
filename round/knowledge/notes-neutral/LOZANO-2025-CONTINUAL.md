# Continual Deep Reinforcement Learning for Decentralized Satellite Routing (LOZANO-2025-CONTINUAL)

在问什么：卫星在动、环境在变，星上 DRL 策略如何持续更新不过时。声称：离线用全局经验训全局 DNN，在线本地 DNN 靠"模型预演"（模型随轨道传给下一颗星）与联邦学习演进；低拥塞时仅一跳邻居反馈即可达到最短路径同等端到端性能，拥塞时绕开重负载链路。凭什么信：仿真+公开代码（SatCom-TELMA/MA-DRL_Routing_Simulator，155 stars、活跃更新、无 LICENSE——衍生进公开仓库有风险）。不舒服：低拥塞下"追平最短路径"是弱 claim——最短路径是解析下界，追平不稀奇；拥塞增益证据摘要没展开；"全局经验训全局网络"如何真分布式落地未细说。

> 状态: 摘要；未核实字段: 拥塞场景增益幅度、流量模型、两阶段训练通信开销、谱系关系细节


---

## 深读节（2026 全文精读增补）

**方法骨架**（节 II System Model / 节 III Learning framework，ar5iv 行 511-2010）：MA-DRL=每颗卫星一个独立 DQN agent，POMDP 四元组；状态 S^i={L_i 局部信息(目的地方位+ISL 连通+坐标), N_i 一跳邻居信息(4 邻居 × 4 队列的 log 压缩拥塞编码 C_j,k，共 28 字段：16 拥塞+8 邻居坐标+2 自坐标+2 目的坐标)}；动作=4 选 1 下一跳（东南西北邻居）；奖励 r=w1·r_q(队列占用) + w2·r_r(逼近日地) + w3·r*(投递+50、环路/不可用链路 -5)。训练两阶段：离线=全局 Q-Network Qg(θ)+target 用全局经验高探索训练；在线=预训练 DNN 上星、本地经验低探索续训；持续学习双机制=模型预演(沿轨道把本地模型传给后继星，短期对齐)+FL(集群聚合→GEO/地面 PS 全局聚合，长期对齐)，用 CKA 相似度量化模型发散。

**实验合同**（节 VI Performance evaluation，行 3669-4420）：自研 Python 仿真器；4 星座=Kepler 7 轨道面×20 星@600km(140 星,Walker star)、Iridium Next 6×11@780km、OneWeb 36×18@1200km、Starlink shell 72×22@550km(Walker delta)；8 个 KSAT 地面站(马拉加/洛杉矶/毛里求斯/挪威/格陵兰/希腊/亚速尔/班加罗尔)；载频 GSL 20/30GHz、ISL 26GHz、带宽 500MHz、包 64.8kbit(DVB-S2)、默认负载 ℓ=1（仅 8 网关实验用 ℓ=0.5 中载）；ISL 用 greedy matching；位置更新 15s、轨道周期 96min。基线=Dijkstra 最短路(权重 1/R(i,j)，全知 genie 上界)+前作 Q-routing(Q-Table，无位置信息)。指标=E2E 时延、CDF、CKA、热力图。关键数字：低拥塞时 MA-DRL 与最短路 50/90/95 百分位差距 1.7/3/9.1 ms（行 4220 附近）；离线收敛 Kepler/OneWeb≈2s、Iridium≈4s、Starlink≈1s；CKA 不对齐时均值 0.8 有降至 0.3，模型预演 +9.9%、集群 FL +22%、全局聚合达 1。

3. **状态无年龄语义**——邻居拥塞 C_j,k 假设每步即时可得，Q 函数未建模该信息的传播年龄/反馈延迟；

**可复用部件 + 危险信号**：可复用——log 压缩拥塞编码 C_j,k、相对坐标粒度化(σ=20)消 180° 边界、CKA 模型发散度度量、模型预演+分层 FL 双尺度对齐、greedy matching 建 ISL。ℓ=1 即"最大支持负载"且未给 Qmax 具体比特数(行 3899-3907 未核实)；"追平最短路"是低拥塞弱 claim(摘要行 22-24)；CKA 数值(0.8/0.3/+9.9%/+22%/+24.6%)来自单一数据集与图,无置信区间(行 4350+ 未核实)；四星座卫星高度/星数与真实运营参数差异未讨论。

> 深读状态: 全文已读[arXiv 2405.12308 v?, ar5iv HTML 全文 323KB, 2026-09-03]; 未核实: 训练 seed 数、Qmax 队列容量、CKA 显著性、2-4s 收敛的时间单位、ISL 利用率/丢包指标。

