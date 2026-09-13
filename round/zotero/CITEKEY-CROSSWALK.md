# Undermind cite_key 与 Zotero itemKey 对照表（v2 分级）

> 用途：引用关系检索（citing / referenced 模式）需要 cite_key；Zotero 与 MinerU 精读需要 itemKey。本表打通二者。
> 分级纪律：只把 confident 档（Jaccard >= 0.75）当作可信对照使用；
> 待确认档（0.5 - 0.75）必须人工核对标题后才能用；未匹配档视为 Zotero 中尚无该论文（需下载 PDF 并转 MD）。
> 理由：误配会静默污染下游（引用检索查错论文、证据对错条目）。

生成 2026-09-10：共 29 篇 → confident 7 / 待确认 8 / 未匹配 14

## A. confident（可信对照）

| cite_key | 年份 | Undermind 标题 | Zotero itemKey | 匹配度 |
|---|---|---|---|---|
| Cho26 | 2026 | Spatial-Temporal Learning-Based Distributed Routing for Dynamic LEO  | LZKNZA8B | 1.00 |
| Din23 | 2023 | Fast-Convergence Reinforcement Learning for Routing in LEO Satellite | 53HEEK33 | 1.00 |
| Fer26 | 2026 | Traffic-Aware Multi-Agent Reinforcement Learning-Based Distributed R | CMNCS52M | 1.00 |
| Heg25 | 2025 | Routing in Low Earth Orbit Satellite Networks: Constrained DQN-Based | ZIUBKVPZ | 1.00 |
| Kri26 | 2026 | Reinforcement Learning for Opportunistic Routing in Software-Defined | J68GU76W | 1.00 |
| Rot24 | 2024 | Shaping Rewards, Shaping Routes: On Multi-Agent Deep Q-Networks for  | 5PYWVRC5 | 1.00 |
| Sor23 | 2023 | Q-learning for distributed routing in LEO satellite constellations | Y2H4NPLU | 1.00 |

## B. 待人工确认（核对标题前不得使用）

| cite_key | 年份 | Undermind 标题 | 候选 itemKey | 候选标题 | 匹配度 |
|---|---|---|---|---|---|
| Fu23 | 2023 | Reinforcement Learning Based Intelligent Routing for So | 3MRQRWHU | Multi-QoS Routing Algorithm Based on Reinforc | 0.55 |
| He25 | 2025 | SRv6-Enabled Routing Optimization in LEO Satellite Netw | 53HEEK33 | Fast-Convergence Reinforcement Learning for R | 0.50 |
| Li25 | 2025 | Reinforcement Learning Based Minimum Hop Routing Strate | 3MRQRWHU | Multi-QoS Routing Algorithm Based on Reinforc | 0.60 |
| Li26 | 2026 | Load-Balanced and Congestion-Aware Routing for LEO Lase | CYMQ2GLA | A Two-Hops State-Aware Routing Strategy Based | 0.53 |
| Loz24 | 2024 | Multi-Agent Deep Reinforcement Learning for Distributed | UKEKU5ZG | A Centralized–Distributed Joint Routing Algor | 0.54 |
| Sun26 | 2026 | Hybrid SRv6 and Reinforcement Learning Routing for Dyna | 53HEEK33 | Fast-Convergence Reinforcement Learning for R | 0.56 |
| Tan24 | 2024 | Congestion Control and Routing Optimization for LEO Sat | 3MRQRWHU | Multi-QoS Routing Algorithm Based on Reinforc | 0.50 |
| Wei26 | 2026 | STG-SR: Spatio-Temporal Graph based Load Balancing Rout | XLRW7XXN | A DQN-Based Routing Algorithm for Load Balanc | 0.60 |

## C. 未匹配（Undermind 库内有、Zotero 无）

| cite_key | 年份 | 标题 | 最佳本地候选 | 匹配度 |
|---|---|---|---|---|
| Bar26 | 2026 | Unlocking Resilience and Load Balancing: Toward Hop-By-Hop R | A Load Balancing Routing Strategy for LE | 0.27 |
| Cao19 | 2019 | Congestion Control Based on OSPF in LEO Satellite Constellat | IDLB: An SDN‐Based Load‐Balancing Routin | 0.23 |
| Che26 | 2026 | A Double Deep Q-Network Reinforcement Learning Method for Lo | A Load Balancing Routing Strategy for LE | 0.38 |
| Gre26 | 2026 | Dynamic Predictive Routing for Satellite Megaconstellations | Traffic-Predictive Routing Strategy for  | 0.38 |
| Gri22 | 2022 | Rethinking LEO Constellations Routing with the Unsplittable  | On-Demand Routing in LEO Mega-Constellat | 0.19 |
| K23 | 2023 | Enhancing Network Performance in LEO Satellite Networks thro | Recovery Routing Based on Q-Learning for | 0.33 |
| Kim26 | 2026 | Learning-Based Resilient Dynamic Routing for Fault-Tolerant  | Spatial-Temporal Learning-Based Distribu | 0.46 |
| Kim26b | 2026 | Toward Wide-Area LEO Backbones: Distributed End-to-End Routi | Distributed On-Demand Routing for LEO Me | 0.33 |
| Wan23 | 2023 | An Intelligent Area-segmentation Enabled Hybrid Routing Meth | Distributed On-Demand Routing for LEO Me | 0.21 |
| Yan25 | 2025 | Secure and Scalable Rerouting in LEO Satellite Networks | SkyLink: Scalable and Resilient Link Man | 0.33 |
| Yin25 | 2025 | A Hybrid Routing Strategy for Congestion Mitigation in LEO M | Traffic-Predictive Routing Strategy for  | 0.20 |
| Zha21 | 2021 | ASER: Scalable Distributed Routing Protocol for LEO Satellit | A distributed routing algorithm for data | 0.40 |
| Zha26 | 2026 | Dynamic routing optimization and management in low Earth orb | Routing in Low Earth Orbit Satellite Net | 0.46 |
| Zha26b | 2026 | Reinforcement learning-based robust routing strategies again | Multi-QoS Routing Algorithm Based on Rei | 0.46 |
