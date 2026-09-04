# 文献矩阵：全表 + 精选（2026-09-04）

> 池 430 篇 → RL 相关 142 篇（精读 24 + 题录级 118）+ 非 RL 参照若干。
> 精读七环详表见 algo-pipeline-matrix.md；本文件 = 精选 10（含理由）+ 题录级 118 全表。

## 一、精选 10 篇（核心清单）

> 遴选准则：方法形态代表性 × 证据等级 × 对幸存选题卡的锚点作用 × 谱系位置（奠基/前沿）。
> 全部经过全文精读+引用核对（见 notes/ 与 batch-ledger.md）。

### RL 方法线（6 篇）
| # | 论文 | 为什么核心 |
|---|---|---|
| 1 | **2306.01346** 分布式 tabular Q-routing（2023） | 谱系奠基：最早把"无地面依赖的分布式学习路由"做完整；拥塞的操作化定义（回归斜率 t 检验）可直接复用；genie 基线讨论是全池最诚实的 |
| 2 | **2402.17666** MA-DRL 两阶段（2024） | CTDE 形态代表：离线全局探索+在线星上执行；同时是"证据最弱却被引用"的典型（一张定性图），评审价值高 |
| 3 | **2605.02413** GAT+LSTM 时空 DRL（2026） | 最新形态代表：图注意力+时序+分布式；同时是 D8 病灶样本（合成正弦流量） |
| 4 | **2604.12382** 流量感知域划分+负载均衡（2026） | **全池唯一开源**的完整 RL 路由工作（代码可得）——复现与重测的锚点 |
| 5 | **2509.14909** 混合"Dijkstra 表+RL 回退"（2025） | 经典/RL 边界样本：RL 被关进"回退牢笼"——回答"RL 到底该在哪个决策位"的关键对照 |
| 6 | **ieee-11565396** FedDQN 联邦重路由（2026） | 联邦学习形态代表；其 non-IID 盲区（第 46-50 轮性能下降无机制解释）是现成攻击面 |

### 优化参照线（2 篇）
| # | 论文 | 为什么核心 |
|---|---|---|
| 7 | **ieee-11308874** OSPFv3 LEO 分析（2025） | 传统协议在 LEO 的收敛/稳定性量化（2.18-2.35s），且是唯一报告快照粒度敏感性（5s/20s 反例）的——F-I 与 F-III 双锚 |
| 8 | **ieee-10375570** 动态 LISL 调度×路由联合优化（TCOM 2023） | 非 RL 强优化参照：奖励分解相关系数>0.98、固定 vs 动态建链能耗-跳数权衡——F-II 策略边界的单侧锚点 |

### 实测底座线（2 篇）
| # | 论文 | 为什么核心 |
|---|---|---|
| 9 | **2310.09242** Starlink 多面实测（2023） | **15s 全局同步重配置**的发现者——所有环境保真讨论的底座；开源 300GB 数据集 |
| 10 | **2605.27717** Starlink 队列结构刻画（2026） | drop-front/~1500 包/1.33ms drain 的唯一实测来源——"击穿语义"的全部参数来源 |

**备选一席（视方向替换）**：2212.13697（首个 Starlink 网络特性实测）、2601.08439（GMM/EVT 统计基线——任何 RL 预测的及格线）、2601.13662（唯一用真实人口流量的 RL 路由）、2410.15546（CGR 容量/缓存约束改进，DTN 线）、2608.01649（LLM 自动奖励设计前沿）。

## 二、题录级全表（118 篇，RL 相关但未精读——诚实标注：仅题录级判断）

| id | 年 | 题名 | 桶 | 来源查询 |
|---|---|---|---|---|
| 2602.01087 | 2026 | Photonic spiking reinforcement learning for intelligent routing | 仅路由 | ax1-rl-routing-sat |
| 2602.13210 | 2026 | Large Language Model (LLM)-enabled Reinforcement Learning for Wire | 调度/资源 | ax4-marl-satellite,ax5-gnn-rl-satelli |
| 10.23919/csiteccps00081.2026.00029 | 2026 | Energy-Aware Routing for LEO Satellite Networks Based on Graph Rei | 仅路由 | cr1,cr4 |
| 10.1002/sat.70043 | 2026 | Path‐Based Deep Reinforcement Learning for On‐Board Routing in Sat | 仅路由 | cr2 |
| 10.1109/t | 2026 | Graph Neural Network Assisted Deep Reinforcement Learning Based Hi | 仅路由 | cr2,cr5 |
| 10.1016/j.neucom.2025.132263 | 2026 | Deep reinforcement learning for network routing optimization: A sy | 仅路由 | cr2 |
| 10.2514/6.2026-0135 | 2026 | Autonomous Task Rescheduling in a Heterogeneous LEO Satellite Cons | 调度/资源 | cr3 |
| 10.21203/rs.3.rs-8455670 | 2026 | QoS-Aware Reinforcement Learning Routing for Entanglement Networks | 调度/资源 | cr4 |
| 10.1016/j.adhoc.2026.104368 | 2026 | Delay-aware satellite networks traffic optimization using GNN-base | 仅路由 | cr4 |
| 10.2139/ssrn.6561121 | 2026 | Disturbed Delay-Aware Reinforcement Learning | 仅路由 | cr4 |
| 10.1109/ojcoms.2026.3727117 | 2026 | Lightweight Q-Exchange Multi-Agent Reinforcement Learning for QoE- | 仅路由 | cr4 |
| 10.21203/rs.3.rs-9250810 | 2026 | Predictive Fidelity-Aware Routing and Adaptive Scheduling in Distr | 调度/资源 | cr4 |
| 10.3390/electronics15122664 | 2026 | Accelerated Graph Neural Networks on an SoC FPGA for Onboard LEO S | 仅路由 | cr5,s2b-cites-2310.076 |
| 10.2139/ssrn.6551274 | 2026 | Multi-graph Decoupled Heterogeneous Graph Neural Network with Rein | 仅路由 | cr5 |
| 10.1109/icns69853.2026.11570640 | 2026 | Adaptive AI Routing in LEO CubeSat Networks to Ensuring Integrity  | 仅路由 | s2b-cites-2310.076 |
| 10.3390/aerospace13030277 | 2026 | Efficient Inference of Neural Networks with Cooperative Integer-On | 仅路由 | s2b-cites-2310.076 |
| 10.1109/ojcoms.2026.3710911 | 2026 | Decentralized MARL for SDN Ground Station Cluster Selection in LEO | 仅路由 | s2b-cites-2310.076 |
| 2605.03382 | 2026 | CRT: Collision-Tolerant Residence Time for Deterministic Transmiss | 仅路由 | arxiv_q04 |
| 2601.21383 | 2026 | KubeSpace: A Low-Latency and Stable Control Plane for LEO Satellit | 仅路由 | arxiv_q06 |
| 2605.12536 | 2026 | Information as Maximum-Caliber Deviation: A bridge between Integra | 仅路由 | arxiv_q11 |
| doi:10.1007/s10586-026-05959-4 | 2026 | Deep reinforcement learning-based resource orchestration algorithm | 仅路由 | cite-ARXIV:2209.08 |
| 2512.20835 | 2025 | QoS- and Physics-Aware Routing in Optical LEO Satellite Networks v | 调度/资源 | ax1-rl-routing-sat,ax2-rl-leo-routing |
| 2508.04288 | 2025 | Challenges in Applying Variational Quantum Algorithms to Dynamic S | 仅路由 | ax1-rl-routing-sat |
| 2501.11198 | 2025 | Energy-Efficient Satellite IoT Optical Downlinks Using Weather-Ada | 仅路由 | ax1-rl-routing-sat,ax10-qlearning-sat |
| 2505.19053 | 2025 | Structured Reinforcement Learning for Combinatorial Decision-Makin | 调度/资源 | ax2-rl-leo-routing |
| 2508.14335 | 2025 | The Small-World Beneath LEO Satellite Coverage: Ground Hubs in Mul | 仅路由 | ax9-traffic-leo |
| 10.1109/globecom59602.2025.11431922 | 2025 | Reinforcement Learning-Based Dynamic Routing Strategy for LEO Sate | 仅路由 | cr1 |
| 10.1109/icct67417.2025.11374242 | 2025 | SRv6-Enabled Routing Optimization in LEO Satellite Networks: A Rei | 仅路由 | cr1 |
| 10.22541/au.175672477.72924085 | 2025 | Path-based Deep Reinforcement Learning for On-board Routing in Sat | 仅路由 | cr2 |
| 10.23919/jcc.fa.2023-0457.202512 | 2025 | A load-balancing routing algorithm based on ant colony optimizatio | 仅路由 | cr3 |
| 10.2139/ssrn.5127607 | 2025 | Constraint-Aware Deep Reinforcement Learning for Generalizable Dro | 仅路由 | cr4 |
| 10.1109/ucom67224.2025.11337020 | 2025 | Dynamic Topology-Aware Routing for LEO Satellite Networks: A Knowl | 仅路由 | cr4 |
| 10.21203/rs.3.rs-7728035 | 2025 | Adaptive Reinforcement Learning with Temporal Prediction for Routi | 拥塞/负载 | cr4 |
| 10.1109/jiot.2025.3568454 | 2025 | Quantum Reinforcement Learning for Lightweight LEO Satellite Routi | 仅路由 | oa1 |
| 10.1109/jiot.2025.3607492 | 2025 | Dynamic LEO Satellite Routing Approach Based on Deep Graph Attenti | 仅路由 | oa1 |
| 10.1007/s10462-025-11340-5 | 2025 | Multi-agent reinforcement learning for resources allocation optimi | 调度/资源 | oa3 |
| 10.1109/ojcoms.2025.3556318 | 2025 | UE Context Dissemination in Sparse LEO Constellations for 5G/6G Ce | 仅路由 | s2b-cites-2310.076 |
| 2507.15307 | 2025 | Joint Optimisation of Electric Vehicle Routing and Scheduling: A D | 调度/资源 | arxiv_q11 |
| 2502.15552 | 2025 | Starlink in Northern Europe: A New Look at Stationary and In-motio | 仅路由 | arxiv_q12 |
| doi:10.59704/dbeee167d32187b0 | 2025 | Starlink, the Cloud, and Corporate Dependency | 调度/资源 | cr_c07 |
| 2407.11047 | 2024 | An open source Multi-Agent Deep Reinforcement Learning Routing Sim | 仅路由 | ax1-rl-routing-sat,ax10-qlearning-sat |
| 2405.12308 | 2024 | Continual Deep Reinforcement Learning for Decentralized Satellite  | 仅路由 | ax1-rl-routing-sat,ax4-marl-satellite |
| 10.1109 | 2024 | Joint Optimization of Computing and Routing in LEO Satellite Const | 联合 | cr1,cr2 |
| 10.1109/auteee62881.2024.10869716 | 2024 | Congestion Control and Routing Optimization for LEO Satellite Netw | 拥塞/负载 | cr1 |
| 10.61951/sciencepaperonline.202401.0 | 2024 | Traffic Engineering in Segment Routing Network Based on Deep Reinf | 仅路由 | cr2 |
| 10.1109/icmlcn59089.2024.10624767 | 2024 | Multi-Agent Deep Reinforcement Learning for Distributed Satellite  | 仅路由 | cr2 |
| 10.2139/ssrn.5070797 | 2024 | Deterministic Delay-Aware Reinforcement Learning | 仅路由 | cr4 |
| 10.1016/j.jnca.2024.103927 | 2024 | GROM: A generalized routing optimization method with graph neural  | 仅路由 | cr5 |
| 10.1109/jiot.2024.3468642 | 2024 | Multipath Cooperative Routing in Ultradense LEO Satellite Networks | 仅路由 | oa1 |
| 10.1109/jiot.2024.3403756 | 2024 | Enabling High-Throughput Routing for LEO Satellite Broadband Netwo | 仅路由 | oa1 |
| 10.1109/tccn.2024.3522579 | 2024 | Routing for Space-Air-Ground Integrated Network With GAN-Powered D | 调度/资源 | oa2 |
| 10.1109/jsac.2024.3365869 | 2024 | Dynamic Routing for Integrated Satellite-Terrestrial Networks: A C | 仅路由 | oa3 |
| 10.1109/jsac.2024.3365878 | 2024 | Stigmergy and Hierarchical Learning for Routing Optimization in Mu | 仅路由 | oa3 |
| 10.1109/wcsp62071.2024.10826849 | 2024 | Routing Strategy in LEO Satellite Networks: A Multi-Agent Reinforc | 仅路由 | oa3 |
| 10.1109/icmlcn59089.2024.10624807 | 2024 | Q-learning for distributed routing in LEO satellite constellations | 拥塞/负载 | oa4,oa5 |
| 10.1109/jsac.2024.3369665 | 2024 | SpaceRIS: LEO Satellite Coverage Maximization in 6G Sub-THz Networ | 仅路由 | oa4 |
| 10.3390/su16219239 | 2024 | Graph Neural Networks for Routing Optimization: Challenges and Opp | 仅路由 | oa4 |
| 10.1109/access.2024.3368503 | 2024 | Handover Strategies for Emerging LEO, MEO, and HEO Satellite Netwo | 仅路由 | oa4 |
| 10.1109/access.2024.3367128 | 2024 | Task Offloading With Service Migration for Satellite Edge Computin | 仅路由 | oa5 |
| 10.1109/taes.2024.3427612 | 2024 | Dynamic Caching in Space Over Heterogeneous Mega-Constellations: A | 仅路由 | s2b-cites-2310.076 |
| 2402.00091 | 2024 | Nash Soft Actor-Critic LEO Satellite Handover Management Algorithm | 仅路由 | arxiv_q06 |
| doi:10.1145/3589334.3645328 | 2024 | A Multifaceted Look at Starlink Performance | 仅路由 | oa_o04 |
| 2401.09455 | 2023 | Dynamic Routing for Integrated Satellite-Terrestrial Networks: A C | 仅路由 | ax1-rl-routing-sat,ax4-marl-satellite |
| 2304.00789 | 2023 | Combinatorial Optimization enriched Machine Learning to solve the  | 仅路由 | ax2-rl-leo-routing |
| 2307.15469 | 2023 | SpaceRIS: LEO Satellite Coverage Maximization in 6G Sub-THz Networ | 仅路由 | ax2-rl-leo-routing,ax3-drl-leo |
| 10.20944/preprints202304.0656. | 2023 | Fast-Convergence Reinforcement Learning for Routing in LEO Satelli | 仅路由 | cr1 |
| 10.3390/s23115180 | 2023 | Fast-Convergence Reinforcement Learning for Routing in LEO Satelli | 仅路由 | cr1,oa1 |
| 10.1109/wcnc55385.2023.10118680 | 2023 | A Deep Reinforcement Learning based Routing Scheme for LEO Satelli | 仅路由 | cr1,oa1 |
| 10.1109/globecom54140.2023.10436727 | 2023 | Reinforcement Learning Based Intelligent Routing for Software Defi | 仅路由 | cr1,oa1 |
| 10.22541/au.167773143.34984973 | 2023 | A Robust Routing Strategy based on Deep Reinforcement Learning for | 拥塞/负载 | cr2,cr4 |
| 10.1109/icc45041.2023.10279521 | 2023 | Reinforcement Learning-Based Load Balancing Satellite Handover Usi | 拥塞/负载 | cr3 |
| 10.1109/iccc59590.2023.10507285 | 2023 | Graph Neural Network and Reinforcement Learning Based Routing for  | 仅路由 | cr5,oa1 |
| 10.1016/j.ejor.2023.01.017 | 2023 | A general deep reinforcement learning hyperheuristic framework for | 仅路由 | oa2 |
| 10.1145/3603703 | 2023 | Reinforcement Learning Methods for Computation Offloading: A Syste | 调度/资源 | oa2 |
| 10.1080/13658816.2023.2279975 | 2023 | A reinforcement learning-based routing algorithm for large street  | 仅路由 | oa2 |
| 10.3390/electronics12030518 | 2023 | Random Routing Algorithm for Enhancing the Cybersecurity of LEO Sa | 仅路由 | oa4 |
| 2307.16246 | 2023 | DRL4Route: A Deep Reinforcement Learning Framework for Pick-up and | 调度/资源 | arxiv_q11 |
| 2304.09535 | 2023 | LEO-PNT With Starlink: Development of a Burst Detection Algorithm  | 仅路由 | arxiv_q12 |
| doi:10.1109/plans53410.2023.10140066 | 2023 | Navigation with Multi-Constellation LEO Satellite Signals of Oppor | 仅路由 | oa_o04 |
| 2206.06568 | 2022 | Distributed and Distribution-Robust Meta Reinforcement Learning (D | 仅路由 | ax1-rl-routing-sat |
| 2201.05393 | 2022 | Reinforcement Learning to Solve NP-hard Problems: an Application t | 仅路由 | ax2-rl-leo-routing |
| 10.1109/cbd54617.2021.00045 | 2022 | Applying Graph Neural Network in Deep Reinforcement Learning to Op | 仅路由 | cr5 |
| 10.3390/electronics11030368 | 2022 | An Approach to Combine the Power of Deep Reinforcement Learning wi | 调度/资源 | cr5 |
| 10.1016/j.cja.2022.06.021 | 2022 | Reinforcement learning based dynamic distributed routing scheme fo | 仅路由 | oa1,oa3 |
| 10.1109/wcnc51071.2022.9771734 | 2022 | Multi-Commodity Flow Routing for Large-Scale LEO Satellite Network | 仅路由 | oa1,oa3 |
| 10.1007/s10458-022-09552-y | 2022 | A Practical Guide to Multi-Objective Reinforcement Learning and Pl | 仅路由 | oa1,oa2 |
| 10.3390/s22083031 | 2022 | Deep Reinforcement Learning for Resource Management on Network Sli | 仅路由 | oa2,oa3 |
| 10.1016/j.rser.2022.113052 | 2022 | Reinforcement learning for electric vehicle applications in power  | 调度/资源 | oa2 |
| 10.3390/math10163017 | 2022 | Reinforcement Learning-Based Routing Protocols in Flying Ad Hoc Ne | 仅路由 | oa2 |
| 10.1109/tnse.2022.3171600 | 2022 | Trajectory Design and Resource Allocation for Multi-UAV Networks:  | 调度/资源 | oa3 |
| doi:10.23919/irs54158.2022.9905046 | 2022 | The STARLINK-based passive radar: preliminary study and first illu | 仅路由 | oa_o04 |
| 10.1109/icet51757.2021.9451072 | 2021 | LEO Satellite Network Routing Algorithm Based on Reinforcement Lea | 仅路由 | cr1,cr2 |
| 10.1109/hoticn53262.2021.9680855 | 2021 | GRouting: Dynamic Routing for LEO Satellite Networks with Graph-ba | 仅路由 | oa1 |
| 10.3390/electronics10090999 | 2021 | Drone Deep Reinforcement Learning: A Review | 仅路由 | oa3 |
| 10.1109/access.2021.3133301 | 2021 | LEO Mega-Constellations for 6G Global Coverage: Challenges and Opp | 调度/资源 | oa4 |
| 10.1109/jiot.2021.3112907 | 2021 | Deep Dyna-Reinforcement Learning Based on Random Access Control in | 仅路由 | oa5 |
| 10.1109/access.2021.3135464 | 2021 | Heterogeneous Traffic Offloading in Space-Air-Ground Integrated Ne | 仅路由 | oa5 |
| 2111.05259 | 2021 | Reinforcement Learning for Security-Aware Computation Offloading i | 仅路由 | arxiv_q04 |
| 2106.09837 | 2021 | Future Ultra-Dense LEO Satellite Networks: A Cell-Free Massive MIM | 仅路由 | arxiv_q06 |
| doi:10.21203/rs.3.rs-760203 | 2021 | Factual Demonstration of Blockchain Routing in Delay Tolerant Netw | 仅路由 | cr_c03 |
| 10.1109/gcwkshps50303.2020.9367476 | 2020 | Heterogeneous Satellite Network Routing Algorithm Based on Reinfor | 仅路由 | cr2 |
| 10.5220/0009095207660772 | 2020 | Production Scheduling based on Deep Reinforcement Learning using G | 调度/资源 | cr5 |
| 10.1109/access.2020.3038605 | 2020 | A Gentle Introduction to Reinforcement Learning and its Applicatio | 仅路由 | oa2,oa3 |
| 10.3390/app10114011 | 2020 | Application of Deep Reinforcement Learning in Traffic Signal Contr | 拥塞/负载 | oa2 |
| 2004.13378 | 2020 | Downlink Coverage and Rate Analysis of Low Earth Orbit Satellite C | 仅路由 | arxiv_q04 |
| doi:10.1109/tgcn.2020.2978296 | 2020 | E-CGR: Energy-Aware Contact Graph Routing Over Nanosatellite Netwo | 仅路由 | oa_o01 |
| 10.1109/tits.2019.2947408 | 2019 | Operating Electric Vehicle Fleet for Ride-Hailing Services With Re | 仅路由 | oa2 |
| 10.1186/s13174-018-0087-2 | 2018 | A comprehensive survey on machine learning for networking: evoluti | 仅路由 | oa2,oa3 |
| 1808.08315 | 2018 | A Deterministic Self-Organizing Map Approach and its Application o | 仅路由 | arxiv_q04 |
| doi:10.1109/jiot.2015.2487046 | 2015 | Satellite Communications Supporting Internet of Remote Things | 仅路由 | oa_o01 |
| doi:10.1109/globalsip.2013.6736883 | 2013 | Contact graph based routing in opportunistic networks | 仅路由 | cr_c02 |
| 1107.1937 | 2011 | Scale-Free Opportunistic Networks: is it Possible? | 仅路由 | arxiv_q10 |
| doi:10.1109/jsac.2003.819977 | 2004 | Supporting IP/LEO Satellite Networks by Handover-Independent IP Mo | 仅路由 | oa_o02 |
| 10.31979/etd.h7jx-ca2n |  | Explainable Reinforcement Learning for Network Routing Optimizatio | 仅路由 | cr2 |
| 10.70675/e02b7a6cz150az4b0azac87z305 |  | Deep reinforcement learning for the vehicle routing problem | 仅路由 | cr2 |
| 10.32657/10356/164058 |  | Deep reinforcement learning for intractable routing &amp; inverse  | 仅路由 | cr2 |
| doi:10.4271/as6802 | None | Time-Triggered Ethernet | 仅路由 | cr_c08 |
| doi:10.4271/as6802a | None | Time-Triggered Ethernet | 仅路由 | cr_c08 |