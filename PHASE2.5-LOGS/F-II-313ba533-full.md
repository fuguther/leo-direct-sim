# F-II 压力测试报告（子代理 313ba533 交付全文，2026-09-03）

> 家族：供需/资源-流量错配的结构与策略边界。本文件为子代理交付物的忠实归档（主会话零改写）。

## 1. 查询日志（16 组，全量）
见下（格式：系统 | 短语 | 命中数 | Top5）

1. arXiv | LEO+constellation+capacity+demand | 8 | ①Estimated Demand for Mega-Constellation Internet Service / 2608.08851 / 2026 ②Duality-Guided Graph Learning for Real-Time Joint Connectivity and Routing / 2601.21921 / 2026 ③Starfield: Demand-Aware Satellite Topology Design / 2601.10083 / 2026 ④Latency Optimization with Hybrid Beam Pattern / 2411.09600 / 2024 ⑤Your Mega-Constellations Can Be Slim / 2407.03799 / 2024
2. arXiv | satellite+traffic+diurnal | 1 | ①Sustainability or Survivability? in LEO Constellations / 2508.17763 / 2025
3. arXiv | orbital+period+traffic+satellite | 10 | ①In-Orbit Optical SSA for Space Traffic Monitoring / 2605.01241 / 2026 ②Stochastic modeling of drag coefficient / 2210.08364 / 2022 ③Cislunar SSA Phasing and Tasking / 2503.16617 / 2025 ④LEO Orchestration with Heterogeneous GNN / 2606.31950 / 2026 ⑤Carrier Aggregation Testbed / 2508.19439 / 2025（全部偏 SSA/轨道力学，无 QoS 拍频类）
4. arXiv | mega+constellation+load+imbalance | 2 | ①Small-World Beneath LEO Coverage: Ground Hubs / 2508.14335 / 2025 ②HYDRA: Black Swan Vulnerabilities / 2602.06612 / 2026
5. arXiv | on-demand+laser+inter-satellite+link | 4 | ①On-Demand Routing with Dynamic LISLs / 2406.01953 / 2024 ②Starfield / 2601.10083 / 2026 ③Links Assignment Potential Edges Importance / 2304.00708 / 2023 ④Duality-Guided Graph Learning / 2601.21921 / 2026
6. arXiv | temporary+laser+inter-satellite+links | 2 | ①Temporary LISLs in FSOSN / 2208.11225 / 2022 ②LISLs in a Starlink Constellation / 2103.00056 / 2021
7. arXiv | satellite+congestion+spatial+distribution | 3 | ①Spatial-Temporal Learning Distributed Routing / 2605.02413 / 2026 ②Joint LISL Matching and Traffic Flow Routing / 2601.21914 / 2026 ③Intelligent Backhaul Link Selection / 2501.09123 / 2025
8. arXiv | dynamic+ISL+energy+efficiency | 2 | ①Dynamic Multi-region Division Task Management / 2507.09926 / 2025 ②Flexible Duplex ISL Performance / 2603.16217 / 2026
9. Crossref | LEO constellation capacity demand | 541593 | ①Capacity Analysis of LEO Mega-Constellation Networks / 10.1109/ACCESS.2022.3149961 / 2022 ②Demand-Driven LEO Constellation for Satellite IoT / 10.1109/GCWKSHP.2024.11101681 / 2024 ③Capacity Estimation MF-CDMA LEO / 10.1109/WICOM.2006.97 / 2006 ④Demand-Aware Flexible Handover / 10.1109/ICCWORKSHOPS.2023.10283793 / 2023 ⑤The Constellation Leo（噪声）/ 10.2307/J.CTV1ZJG7VD.10 / 2020
10. Crossref | satellite traffic diurnal | 425695 | ①Cloud Cover Diurnal Cycles / 10.1127/0941-2948/2012/0423 / 2012 ②MAIA PM2.5 / 10.1021/ACSESTAIR.3C00008.S001 / 2024 ③GPS 轨道周期与日月赤纬 / 10.59313/JSR-A.1503888 / 2024 ④Tropospheric NO2 / 10.5194/EGUSPHERE-EGU23-4729 / 2023 ⑤Air Traffic Mgmt Satellite Navigation / 10.5772/9847 / 2010（均为气象/导航噪声）
11. Crossref | orbital period traffic satellite | 756459 | ①Satellite Orbital Motion / 10.1515/9783110200089.62 / 2003 ②Sputnik 4 / 10.1038/187866A0 / 1960 ③Impulsive Formation Control / 10.3182/20100906-5-JP-2022.00063 / 2010 ④GMDSS / 10.4324/9780080928579-11 / 2012 ⑤Alouette I / 10.1016/0032-0633(66)90001-8 / 1966（均无关）
12. Crossref | mega constellation load imbalance | 306513 | ①Double-Layer Load Balancing Partition Routing / 10.2139/SSRN.5615371 / 2025 ②Pre-Coded ISL Routing with Load Balancing / 10.34133/SPACE.0103 / 2024 ③Load Balancing Partition Routing / 10.1109/VTC2025-FALL.2025.11310657 / 2025 ④Fundamentals of Mega-Constellation Resilience / 10.2514/6.2022-1468 / 2022 ⑤Load-Adaptive and Energy-Efficient Topology Control / 10.1109/GLOBECOM.2022.10001189 / 2022［付费墙-仅摘要级］
13. Crossref | on-demand laser inter-satellite link | 1530704 | LISL 专著章节（10.1002/9781119910749.CH6/CH9/CH8/CH2/CH4，2022），非按需建链边界研究
14. Crossref | temporary laser inter-satellite links | 1319866 | 同上专著章节，无相关
15. Crossref | satellite congestion spatial distribution | 1611439 | 卫星影像贫困/洪水制图噪声（10.22617/TCS210112-2/2021），无相关
16. Crossref | dynamic ISL energy efficiency | 3921054 | 地面能耗文献噪声，无相关

失败行：无。唯一降级：2103.00056 全文 HTML 不可用，经 ar5iv 仅摘要级。

## 2. Top 邻居判定表

| 标识 | 题名 | 现象覆盖 | 机制判别覆盖 | 直接答复? | 关键证据句(原文) | 证据等级 |
|---|---|---|---|---|---|---|
| arXiv:2601.21914 | Joint LISL Matching and Traffic Flow Routing via Lagrangian Duality | 近 | 近 | 部分 | "Existing LISL schemes often overlook mechanical limitations of laser communication terminals (LCTs) and non-uniform global traffic profiles caused by uneven user and gateway distributions, leading to suboptimal throughput and underused LCTs/LISLs" | 全文级 |
| arXiv:2406.01953 | On-Demand Routing in LEO Mega-Constellations with Dynamic LISLs | 近 | 近 | 部分 | "Since the process of establishing these links incurs a setup delay on the order of seconds, a static network topology is generally established well in advance… The results show the benefit of adaptive routing schemes according to the link setup delay." | 全文级 |
| arXiv:2208.11225 | Temporary Laser Inter-Satellite Links in FSOSN | 近 | 近 | 部分 | "The current setup times to establish LISLs between satellites range from a few seconds to tens of seconds due to the pointing, acquisition, and tracking (PAT) process… Due to these high LISL setup times, TLs are currently considered undesirable." | 全文级 |
| arXiv:2601.10083 | Starfield: Demand-Aware Satellite Topology Design | 近 | 近 | 部分 | "A fundamental shortcoming of the grid topology is its agnosticism to network traffic demand patterns, which are inherently non-uniform due to the sparse clustering of populations and the isolation of rural areas on Earth." | 全文级 |
| 10.1109/GLOBECOM.2022.10001189 | Load-Adaptive and Energy-Efficient Topology Control in LEO | 近 | 近 | 部分 | [付费墙-仅摘要级，标题级判断负载驱动拓扑切换] | 摘要级 |
| arXiv:2103.00056 | Laser ISLs in a Starlink Constellation | 近（每星可建链数/链路范围约束） | 无（无流量/拥塞机制） | 否 | "we study the effect of varying a satellite's LISL range on the number of different types of LISLs it can establish with other satellites" | 摘要级 |

## 3. 判定结论（三维度，部分相邻→收窄，无淘汰）

- **时间维度（轨道周期×昼夜节律拍频）→ 存活（全文核验级）**：16 组查询与 5 篇全文核验均无该机制。判别核心：轨道周期（~1.5-2h）与 24h 节律的非整数比拍频是否在 QoS 指标中产生可测周期印记/相位漂移。
- **空间维度 → 收窄**：2601.21914 已做"不均流量×LCT 机械约束"的拥塞权重联合缓解，但目标是缓解而非刻画击穿位置与结构形式。判别核心收窄为：**在硬约束与不均匀时空流量剖面下，定位负载失衡的结构性击穿点（哪些星间对/哪些时段成瓶颈），而非新联合优化算法。**
- **策略维度 → 收窄**：2406.01953/2208.11225 以标量建链时延为可行域判据；2601.10083 证明固定拓扑可按空间需求定制；均无"资源紧张度时空联合分布"判据。判别核心收窄为：**适用域判据从单一建链时延阈值推广为资源紧张度二维时空分布（热点位置×时长×与轨道节拍耦合）。**

## 4. 检索覆盖边界

系统仅 arXiv API + Crossref REST；未用 IEEE Xplore/Scopus/Semantic Scholar/Google Scholar/知网。词表为基础 8 短语未增补。未限年份，命中集中 2021-2026。未覆盖：付费期刊全文（GLOBECOM 2022 仅摘要级）、预印本版本差异、逆向引文链扩展。

## 5. 自我怀疑

① 拍频维度可能藏于 IEEE 全文或 Starlink 运营测量类文献，"存活"仅在本检索边界内成立；② Crossref bibliographic 噪声极大（40 万-390 万命中），Top5 未必最相关，中文/IEEE TWC 文献可能被淹没；③ 2601.21914 实验节若已量化"失配何时导致吞吐塌陷"，空间维度收窄幅度需进一步收紧。

## 6. 失败恢复记录
无查询失败；2103.00056 回退 ar5iv 降级摘要级（1 次）。