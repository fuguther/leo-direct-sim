# F-III 压力测试报告（子代理 7d1cf1f1 交付全文，2026-09-03）

> 家族：切片化静态近似的误差方向。本文件为子代理交付物忠实归档（主会话零改写）。

## 1. 查询日志（arXiv 23 行 + Crossref 8 行，全量）

### arXiv（export.arxiv.org/api/query，词 AND 组合，max_results=5）—— 关键行见下，含 12 组增补
1. arXiv | time-expanded+graph+network | 436340* | Learning Universal GNN Embeddings / 1909.10086 / 2019；Counting cliques / 2311.15289 / 2023；Graph-Powered IoT / 2410.21006 / 2024；GraphFPN / 2108.00580 / 2021；Distributed Linear Op / 1510.03947 / 2015
2. arXiv | time-varying+graph+routing+approximation | 416420* | Prescribed-time controllers / 2311.02473 / 2023；Learning to Route Electric Trucks / 2604.26566 / 2026；Four Principles Geographic Routing / 1403.3007 / 2014；Optimal Transport Coverage / 2601.21753 / 2026
3. arXiv | snapshot+topology+LEO | 172199* | immediate snapshot complexes / 1404.5813 / 2014；persistence modules / 1802.08117 / 2018；Hawaiian Groups / 1111.0733 / 2011（数学噪声）
4. arXiv | temporal+graph+routing+network | 518654* | A map of approaches to temporal networks / 2103.13615 / 2021；TKG Encoder / 2112.07791 / 2021；**Time Granularity on Temporal Graphs / 2311.12255 / 2023**；Percolation M2M / 1403.8123 / 2014
5. arXiv | snapshot+approximation+error+dynamic | 753010* | ADP approximation errors / 1412.6095 / 2014；Trotter errors / 2312.13282 / 2023△；Snapshot Spectral Anti-Spoofing / 2405.18853 / 2024（噪声）
6. arXiv | discretization+granularity+simulation+error | 592882* | Measuring Dataset Granularity / 1912.10154 / 2019；DES vs ABS / 1003.4141 / 2010；Retail ABM / 1003.3784 / 2010
7. arXiv | topology+snapshot+period+routing | 310630* | 数学/拓扑学噪声（immediate snapshot complexes 等）
8. arXiv | time+step+accuracy+satellite | 945036* | Temporal Risk on Satellites / 2608.20575 / 2026；Dark Quiet Sky / 2412.08244 / 2024；Spectrum Prediction SatCom / 1912.04716 / 2019；SpaceMeta LEO / 2402.09720 / 2024
9† | arXiv | snapshot+routing+satellite | 63746* | Gateway Placement ISTN / 2002.03071 / 2020；**Snapshot Partition Polar LEO / 1411.0372 / 2014**；Potential Edges WROSN / 2304.00708 / 2023
10† | arXiv | time-expanded+graph+satellite | 172296* | Handover Framework LEO / 2211.07872 / 2022；其余噪声
11† | arXiv | temporal+graph+discretization | 318902* | TKG Encoder / 2112.07791 / 2021；**2311.12255**；temporal networks map / 2103.13615 / 2021
12† | arXiv | contact+graph+routing | 211708* | Geographic Routing / 1403.3007 / 2014；M2M Multipath / 1002.1162 / 2010（无领域内命中）
13† | arXiv | journey+planning+temporal+graph | 268804* | HDDL temporal HTN / 2306.07353 / 2023（无路由误差命中）
14† | arXiv | 精确短语×6组（整句 quoted） | 0 | 全部 0（精确短语语法过严，空结果非抓取失败）
15✗ | arXiv 首批 8 组 | 故障→已恢复 | heredoc 内 URL 含引号截断字符串致输出为空；定位后用 urllib.parse.quote 重建查询重跑成功

### Crossref（api.crossref.org/works?rows=5）
16 | Crossref | time-expanded graph network routing | 5 | 10.1109/dsa56465.2022.00070 / Time-varying Graph Model for LEO Routing / 2022；10.1109/mnet.012.2300052 / G-Routing GNN / 2023
17 | Crossref | time-varying graph routing approximation error | 5 | 同 DSA2022；10.1109/wcsp.2015.7341072 / TVG DTN routing / 2015；10.1109/gcwkshps58843.2023.10464840 / TVG Inter-Orbit LEO / 2023
18 | Crossref | snapshot topology LEO satellite routing | 5 | 10.1109/cse.2014.93 / Virtual Topology Snapshot / 2014；10.1109/icct.2008.4716089 / ISL states+snapshot / 2008；10.1109/wcncw67598.2026.11555331 / Adaptive Snapshot DQN / 2026；10.1117/12.2617959 / snapshot uploading / 2022
19 | Crossref | temporal graph routing network | 5 | 10.1016/j.comnet.2017.09.012 / EAODR Temporal Graph / 2017；10.1109/hpsr57248.2023.10148029 / 2023
20✗ | Crossref | snapshot approximation error dynamic network | HTTP 429 | Too Many Requests（2s 间隔仍限流；记失败继续，未补跑）
21 | Crossref | discretization granularity simulation error | 5 | 10.1109/wsc.2016.7822095 / 2016；10.1109/wsc60868.2023.10408088 / 2023
22 | Crossref | topology snapshot period routing satellite | 5 | 同 CSE2014、ICCT2008；10.1109/comcomap51192.2020.9398876 / Adaptive Snapshot SDN / 2020
23 | Crossref | time step accuracy satellite network simulation | 5 | **10.1016/j.proenv.2011.09.142 / Accuracy Evaluation of Satellite Network Simulation / 2011**

## 2. Top 邻居判定表

| 标识 | 题名 | 现象覆盖 | 机制判别覆盖 | 直接答复? | 关键证据句 | 证据等级 |
|---|---|---|---|---|---|---|
| arXiv 2311.12255 | Exploring Time Granularity on Temporal Graphs for Dynamic Link Prediction | 近（粒度影响结果） | 近（4 级粒度受控对比；输出=预测精度非路由误差方向） | 否 | "Coarser time granularities may sacrifice critical temporal information, whereas finer granularities could introduce noise into the training process." | 全文级 |
| arXiv 1411.0372 | Link Reassignment based Snapshot Partition for Polar-orbit LEO | 近（LEO 快照粒度/时长影响路由与时延） | 无（优化分割本身，不对照连续动态量化切片误差） | 否 | "Snapshot is a fundamental notion proposed for routing in mobile LEO satellite networks… Its distribution has a great impact on the routing performance and on-board storage." | 摘要级 |
| 10.1109/dsa56465.2022.00070 | Time-varying Graph Model for LEO Routing (DSA 2022) | 近（时变图 vs 快照范式） | 无 | 否 | [付费墙-仅摘要级] | 摘要级 |
| 10.1016/j.proenv.2011.09.142 | Accuracy Evaluation of Satellite Network Simulation | 近（卫星网仿真精度） | 无 | 否 | [付费墙-仅摘要级] | 摘要级 |
| 10.1109/wcncw67598.2026.11555331 | Adaptive Topology Snapshot Updating in LEO Using DQN | 近（快照更新周期自适应） | 无 | 否 | [付费墙-仅摘要级] | 摘要级 |
| arXiv 2002.03071 | Joint Satellite Gateway Placement and Routing | 无（LP 近似 vs MILP 算法近似，非时域切片） | 无 | 否 | "the performance of our approximation algorithm is very close to the exact approach" | 全文级 |

## 3. 判定结论 + 收窄后判别核心

判定：部分相邻 → 收窄声明（存活，非淘汰）。未见公开命中直接答复三问：①切片近似系统性误差方向（低估时延尖峰/高估吞吐）；②粒度-收敛定量判据；③动态速率×流量时间尺度不可忽略边界。2311.12255 只覆盖"粒度影响结果"现象外壳，机制与输出量不同。

**收窄后判别核心**：原声明收窄为——"在 LEO 星座路由/仿真中把可预测快变拓扑切为静态快照序列时，针对路由性能指标（端到端时延尖峰、吞吐）的切片近似误差，相对连续时变参考是否存在系统性方向、随切片粒度的定量收敛关系与一致性判据、以及动态速率×流量时间尺度的不可忽略组合边界"。现有 LEO 快照文献均把切片当默认工程选择，未对照连续动态报告误差方向；时变图/时序图社区只研究粒度对结构表达力/预测精度的影响。

## 4. 检索覆盖边界

仅 arXiv API + Crossref；未覆盖 IEEE Xplore / Semantic Scholar / Scopus / DBLP 全文检索。词表 8 基础+6 增补；"contact graph routing" 在 arXiv 仅宽匹配噪声；未限时间（2008-2026）；付费墙仅摘要级；非英文、专利、3GPP/CCSDS 标准、未索引 PDF 未覆盖。

## 5. 自我怀疑

① 词表盲区风险："contact graph routing"/"time-expanded network"（运筹学）等词眼可能藏于付费墙；② arXiv 相关性排序失效 + Top5 截断可能漏真邻居；③ 1411.0372 正文未读（PDF 未解析）；④ Crossref 第 20 行因 429 未补跑；⑤ totalResults 虚高，命中数仅作日志不作覆盖率依据。

## 6. 失败恢复记录
arXiv 引号故障 1 次（行 15，已恢复重跑）；Crossref 429 1 次（行 20，未补跑）。