# Relational Deep RL for Routing in Wireless Networks (MANFREDI-2021-RELATIONAL)

> 来源: https://doi.org/10.1109/WoWMoM51794.2021.00029（IEEE WoWMoM 2021；arXiv 2012.15700 全文开放）

它把每个包当智能体（packet-centric），拓扑/邻居关系用关系特征喂网络，并用 extended-time actions 显式建模"包在队列里要等多久"。声称跨拥塞水平、拓扑、链路动态泛化，优于最短路与 backpressure。证据：packet-level 仿真。这一手和我们实测的"瓶颈在对接入排队"直接呼应——十篇里极少有把排队等待时长当决策一等公民的。舒服处：它承认"等待时长本身是高信息量状态"，与我们把 holding/access 排队识别为瓶颈互为印证；跨拥塞泛化与我们压力合同实验同构。不舒服处：地面无线场景，规模比 280×14 差一个量级；关系特征仍是静态图结构+局部状态，没有"信息年龄"分量；它回避陈旧性而不是建模它。可作为"排队等待作为信息"的对照参考，提示我们在 AoI 实验里把"预计等待"也写成显式状态分量。全文公开可作基线移植候选。

**评级**：B

> 状态: 摘要；未核实字段: 关系特征的具体定义、extended-time actions 的量化细节、无线信道/干扰模型、是否开源。
