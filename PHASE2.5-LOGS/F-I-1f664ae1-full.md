# F-I 压力测试报告（子代理 1f664ae1 交付全文，2026-09-03，第3次尝试成功）

> 家族：拓扑动态×决策失配。本文件为子代理交付物忠实归档（主会话零改写）。

## 1. 查询日志（arXiv 8 组 + Crossref 8 组，全量成功）

> 说明：arXiv totalResults 在本环境解析返回 -1（接口未含该标签），以实际返回条目计"≥6 条命中"。

1. arXiv|LEO+routing+convergence|≥6 | 2601.21921 Duality-Guided Graph Learning; 2601.21914 ISL Matching & Traffic Flow Routing; 2512.09453 BlockFlex
1b. CR|LEO routing convergence|5 | 10.3390/s23115180 Fast-Convergence RL Routing LEO (2023); 10.1109/ictc66702.2025.11388042 Feeder Link Constraints ISL Routing (2025)
2. arXiv|satellite+control+plane+delay|4（弱相关）| 2609.00875 Federated Learning Orbital Edge; 2604.09306 SatQNet; 2605.20875 Spare Strategy
2b. CR|satellite control plane delay|5 | 10.23919/chicc.2017.8027527 卫星编队时延协同控制 (2017); 10.1109/p2p.2013.6688714（非卫星）
3. arXiv|dynamic+topology+routing+satellite|≥6 | **2006.12242 Exploiting topology awareness for routing in LEO**; 2605.02413; 2509.14909 Hybrid Table-Assisted RL NGSO
3b. CR|dynamic topology routing satellite|5 | 10.1109/tnet.2024.3397613 Dynamic Discrete Topology Design & Routing STIN; 10.22541/au.174229431 Dynamic Predictive Routing Megaconstellations
4. arXiv|SDN+satellite+latency|≥6 | **2108.09176 Controller Placement SDN 5G STN**; 2310.07646 LEO Survey; 2509.02149 Segment Routing FlexAlgo
4b. CR|SDN satellite latency|5 | 10.1145/3050220.3050237 Tight Control Plane Latency Guarantees SDN (2017, 非卫星); 10.2514/6.2016-5755 SDN Enhancements LEO
5. arXiv|predictable+topology+routing+deviation|3（漂移）| 全部不相关
5b. CR|predictable topology routing deviation|5 | 10.1109/icnp.2008.4697039 Topology dynamics & routing for predictable mobile networks (2008); 10.1016/j.comcom.2016.07.009 incompletely predictable ad-hoc
6. arXiv|ephemeris+aware+routing|0 | 无命中
6b. CR|ephemeris aware routing|5 | 无直接相关
7. arXiv|satellite+network+decision+delay+topology|≥6 | 2103.13197 GNSS Topology; **2209.08565 Distributed Probabilistic Congestion Control LEO**; 2604.13361 Semantic Routing
7b. CR|satellite network decision delay topology|5 | 10.1109/acp66871.2025.11350546 马尔可夫决策星间光网拓扑优化; 其余弱相关
8. arXiv|control+loop+stability+satellite|≥6 | 2511.23014 低推力轨道转移闭环控制（轨道动力学非网络）; 2406.00402 FPGA Sparse Satellite Control（航天器控制）
8b. CR|control loop stability satellite|5 | 经典控制/电力 HIL，非星座网络

## 2. Top 邻居判定表

| 标识 | 题名 | 现象 | 机制判别 | 直接答复? | 关键证据句(原文) | 等级 |
|---|---|---|---|---|---|---|
| arXiv:2006.12242 | Exploiting topology awareness for routing in LEO (2020) | 近（时延构成） | 无 | 否 | "we provide the formulations to calculate the total latency considering the predictable propagation and packet transmission times" | 全文级 |
| arXiv:2310.07646 | LEO Satellite Networking Relaunched: Survey (2023) | 近（快照路由时标假设） | 近（快照更新 vs 拓扑演化时标） | 部分 | "the topology … is supposed to be static for the duration of a snapshot … a new routing table is populated for the next snapshot"; "the length of time a snapshot is stable is rather short" | 全文级 |
| arXiv:2108.09176 | Controller Placement in SDN 5G STN (2021) | 近（控制面时延） | 无（只最小化时延，不给失效模式） | 否 | "jointly minimizing the average controller-to-gateway latency and the average control path error" | 全文级 |
| arXiv:2209.08565 | Distributed Probabilistic Congestion Control in LEO (2022) | 近（集中式信令→信息过时） | 近（邻居最新流量信息决策） | 部分 | "a centralized algorithm for minimum-delay packet routing would incur significant signaling and computational overhead"; "decision … based on the latest traffic information received from the neighbors" | 全文级 |
| 10.1109/icnp.2008.4697039 | Topology dynamics & routing for predictable mobile networks (2008) | 近 | 无 LEO/控制回路 | 否 | （付费墙-仅摘要级） | 摘要级 |

## 3. 判定结论：存活（附收窄）

- 未见命中给出"控制回路时延/拓扑变化时间尺度之比"的相图，也未给出比值到三种失效模式（过时决策/振荡/决策缺失）的边界刻画。
- "轨道预测拓扑 vs 实际转发行为"的解释力落差未见直接量化。
- 机制要素零散存在：快照静态假设（2310.07646）、集中式信令不可行→邻居最新信息（2209.08565）、控制器-网关时延最小化（2108.09176）。

**收窄后判别核心**：在 LEO 巨型星座中定义 ρ = 控制决策回路时延（信令往返+计算）/ 拓扑显著变化间隔（快照稳定期、ISL 切换周期），刻画 ρ 跨越哪些阈值时集中/半集中控制依次进入"过时决策—振荡—决策缺失"三种失效模式，给出相图边界与各边界处可观测症状（用户侧时延/路径行为异常）；同时量化"按轨道预测的拓扑知识"对实际转发决策的解释力落差的结构与失效条件。证据等级：存活判定基于 4 篇全文级 + 12 组检索级扫描；核心相图问题在全部命中中零覆盖。

## 4. 自我怀疑

1. 词表盲区：相图/稳定性可能藏在 handover management、time-triggered scheduling、DetNet satellite、contact plan 文献（contact plan 最可能部分覆盖"拓扑知识 vs 行为落差"）。
2. 时间盲区：2025-2026 Starlink 实测类论文可能未被命中。
3. 判别错位风险：2209.08565 的"latest traffic information"与本族"过时决策"控制对象不同（拥塞 vs 路由）。
4. totalResults 解析失败使命中数为下界。

## 5. 检索覆盖边界
系统：arXiv API + Crossref 各 8 组；未覆盖 IEEE Xplore 全库、ACM DL、ScienceDirect 全文、DBLP、Google Scholar 引文链。时间：未限年份。语言：仅英文。失败记录：totalResults 正则全组失效（-1）；ephemeris+routing 零命中；前两次尝试 Crossref 传参 bug 与输出未打印（已重跑补齐），无数据丢失。