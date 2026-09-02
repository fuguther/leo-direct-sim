# 文献获取清单（谁负责下载）

> 规则：下载文件一律放 `LITERATURE/papers/<SOURCE_ID>.pdf`；本目录已 gitignore（公开仓库不入版权 PDF），克隆者按本清单自取。
> 状态：⏳ 等你下载 ｜ ✅ 已就位 ｜ 🔄 我自动抓取中/已抓

## A 档：精读队列必备 · ⏳ 需要你下载（付费墙）

| 优先级 | ID | 论文 | 出处/DOI | 备注 |
|---:|---|---|---|---|
| 1 | `RAN-2025-GRAPHPR` | GraphPR (GNN+MARL 逐包路由) | IEEE TVT 74(3):5229-5234 · doi:10.1109/TVT.2024.3499933 | 最近邻设定，深读第一优先 |
| 2 | `GAO-2026-RAOI` | RAoI (AoI 进 DRL 奖励+时空 GNN) | IEEE/ACM ToN 34:292- · doi:10.1109/TON.2025.3597928 | AoI 机制正面对标 |
| 3 | `ZHANG-2025-GRLR` | GRLR (GNN+AC 逐跳) | IEEE TVT 74(2):3225-3237 · doi:10.1109/TVT.2024.3471658 | 常见基线 |
| 4 | `LI-2025-POMAP` | POMAP (排队论+MAPPO) | IEEE IoT-J 12(22):46675-46691 · doi:10.1109/JIOT.2025.3610772 | S/A/R 需从原文核实 |
| 5 | `LYU-2024-CMADR` | CMADR (约束 MARL 天地一体化) | IEEE JSAC 42(5):1204-1218 · doi:10.1109/JSAC.2024.3365869 | JSAC 级工作 |
| 6 | `CHU-2023-RRSDRL` | RRS-DRL (AoI 入奖励先例) | IET Electronics Letters · doi:10.1049/ell2.12820 | 状态极简，注意对照 |
| 7 | `LI-2023-LUR` | LUR (LEO AoI 优化派基线) | IEEE IoT-J 10:7189- · doi:10.1109/JIOT.2022.3229028 | AoI 聚类基线 |
| 8 | `CHEN-2025-TMIX` | Transformer-MIX 路由 | IEEE IoT-J 12(11):15748-15763 · doi:10.1109/JIOT.2025.3530919 | A 级代表工作 |

## B 档：值得有但非生死 · ⏳ 需要你下载（如方便）

| ID | 论文 | 出处/DOI |
|---|---|---|
| `RAO-2025-DGAT` | Deep GAT+增量演化 RL | IEEE IoT-J 12(23) · ieeexplore 11165344 |
| `XIANG-2025-MATGCIR` | 时序图卷积+模仿加速 | IEEE Comm. Lett. 29(11):2521-2525（DOI 未验证） |
| `BAI-2025-GRLRR` | GRL-RR SDN 韧性路由 | Elsevier Computer Networks 259:111089 · doi:10.1016/j.comnet.2025.111089 |
| `HUANG-2024-GMR` | GNN 多径 TE | IEEE TVT 73(4):5454-5468 · doi:10.1109/TVT.2023.3333848 |
| `WANG-2021-GROUTING` | GraphPR 前作（line-graph MPNN） | IEEE HotICN 2021 · doi:10.1109/HotICN53262.2021.9680855 |
| `SORET-2024-QLEARN` | Q-learning 分布式路由前身 | IEEE ICMLCN 2024 · doi:10.1109/ICMLCN59089.2024.10624807 |
| `TALEB-2009-ELB` | ELB 经典负载均衡基线 | IEEE/ACM ToN 17(1):281-293 · doi:10.1109/TNET.2008.918084 |
| `SONG-2014-TLR` | TLR 红绿灯基线 | IEEE TWC 13(6):3380-3393 · doi:10.1109/TWC.2014.041014.130040 |
| `STARTCAP-2024` | Starlink 切换测量 | ACM APNet 2024 · doi:10.1145/3663408.3665803 |
| `WIGMORE-2025-MAGNN` | 多轴 GNN 排队网络 | ACM MobiHoc 2025 · doi:10.1145/3704413.3764422 |
| `BHAVANASI-2023-GNNMADRL` | GCN+MARL 韧性 | IEEE TNSM 20(3):2283-2294 · doi:10.1109/TNSM.2023.3287936 |
| `MANFREDI-2021-RELATIONAL` | 关系 DRL 路由 | IEEE WoWMoM 2021 · doi:10.1109/WoWMoM51794.2021.00029 |
| `ALMASAN-2022-DRLGNN` | edge-MPNN 表示研究 | Elsevier ComCom 196:184-194 · doi:10.1016/j.comcom.2022.09.029（作者主页可能有 OA 版） |
| `GANNON-2024` | make-before-break 切换 | IEEE ICC 2024 · doi:10.1109/ICC51166.2024.10622772 |

| `OPENALEX-FSO-SCHED-ROUT` | FSO 链路调度+路由联合（引 GraphPR，联合调度候选线） | IEEE IoT-J 2025 · doi:10.1109/jiot.2025.3566744 |
| `OPENALEX-HIER-MWC2026` | 多层星座分层智能路由 | IEEE Wireless Comm. 2026 · doi:10.1109/mwc.2026.3654918 |
| `OPENALEX-LYAPUNOV-WCNC` | Lyapunov 分布式路由（非学习对照候选） | IEEE WCNC 2025 · doi:10.1109/wcnc61545.2025.10978609 |
| `OPENALEX-ANTIJAM-TAES` | 抗干扰 GNN 路由 | IEEE TAES 2026 · doi:10.1109/taes.2026.3677860 |
| `OPENALEX-AI-SATCOM-SURVEY` | AI 卫通综述（查缺补漏用） | IEEE COMST 2025 · doi:10.1109/comst.2025.3534617 |
| `OPENALEX-SENSORS-DRL-ROUT` | DRL 路由（MDPI，OA 我可自取，无需你） | Sensors 2025 · doi:10.3390/s25041232 |

## MDPI 转档（2026-09-03：本机 IP 被 MDPI 反爬全拒，以下开放获取论文需要你用浏览器下载，很快）

- `DONG-2023-DQNLLRA`（10.3390/rs15112801）｜`SHI-2024-GNNDQN`（10.3390/app14093840）｜`HAN-2024-DMR`（10.3390/electronics13153054）｜`OPENALEX-SENSORS-DRL-ROUT`（10.3390/s25041232）｜`OPENALEX-CENTRAL-DIST-JOINT`（10.3390/app15094664）｜`OPENALEX-HIER-TE-3D`（10.3390/electronics14051045）｜另有两篇 arXiv 失败待重试：`MA-2022`、`ZHOU-2026-DTAR`

## C 档：开放获取 · 🔄 我自己抓 arXiv（无需你管）

- `LOZANO-2025-CONTINUAL` arXiv:2405.12308 ｜ `CHOU-2026-STL` arXiv:2605.02413 ｜ `LIAQ-2026-QARR` arXiv:2605.04448
- `ZHOU-2026-DTAR` arXiv:2604.12382 ｜ `HE-2025-PRIMAL` arXiv:2510.27506 ｜ `ZHANG-2024-NGAT` arXiv:2404.18084
- `WEIL-2024-RMP` arXiv:2402.05027 ｜ `IZHIKEVICH-2024` arXiv:2306.07469 ｜ `MA-2022` arXiv:2206.05428 ｜ `GUVEN-2023` arXiv:2305.07207
- `DONG-2023-DQNLLRA` MDPI 10.3390/rs15112801 ｜ `SHI-2024-GNNDQN` MDPI 10.3390/app14093840 ｜ `HAN-2024-DMR` MDPI 10.3390/electronics13153054
- 反向检索新增：`ARXIV-2512.00985`（采样+路由年龄最优）｜`ARXIV-2007.05449`（LEO 多跳更新新鲜度）｜`ARXIV-2111.09217`（多跳无线新鲜度）｜`ARXIV-2310.03969`（NTN AoI 分析）

## 交接说明

- 你下载完：把 PDF 丢进 `LITERATURE/papers/`，文件名 = 上面的 ID（如 `RAN-2025-GRAPHPR.pdf`）。告诉我一声，我会核对并登记进 SOURCES.csv 的 local_path。
- 下载不动的（如 IEEE 页面 403）：留言，我换通道（作者主页/ResearchGate 镜像/替代版本）。