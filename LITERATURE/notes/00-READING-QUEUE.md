# 阅读队列与筛选台账（36 篇）

> 两遍法：全量过摘要 → 选出精读队列 → 读全文 → 写笔记。本表是唯一筛选台账。
> 分级：A=直接相关（LEO+路由+DRL/GNN）｜B=机制相关（AoI/部分观测/拥塞）｜C=方法基础｜D=测量/模型。
> 状态：queued（未筛）→ abstracted（已过摘要）→ full-read（已读全文）→ notes-done（笔记已写）。

## 精读队列（第一批）

按"离我们战场最近"排序，前 8 优先全文精读：

1. **GraphPR**（最近邻设定逐点对齐，多方基线）
2. **RAoI**（AoI 机制正面对标，ToN）
3. **Continual DRL**（开源可复现，本平台谱系直接前身）
4. **GRLR**（GNN 特征逐跳，常见基线）
5. **POMAP**（排队论+MARL，付费墙需谨慎）
6. **CMADR**（JSAC，约束 MARL）
7. **Chou-STL**（状态设计与我们最接近，预印本）
8. **Weil-RMP**（陈旧观测机制核心文献）
9. **PRIMAL**（异步/尾部时延，与 F0/F1 信息问题对口）
10. **LUR**（LEO AoI 派基线）

## 全表

| ID | 标题简 | 级 | 访问/核验 | 状态 | 备注 |
|---|---|---|---|---|---|
| `RAN-2025-GRAPHPR` | GraphPR：GAT+MADRL 全分布式逐包路由 | A | dblp/IEEE 已核，无公开代码 | notes-done | 精读候选 |
| `GAO-2026-RAOI` | RAoI：路由感知 AoI 进奖励 + 时空 GNN | A | IEEE/ACM ToN 2026 | notes-done | 精读候选 |
| `LI-2025-POMAP` | POMAP：排队论+MAPP档 Pareto MARL | A | IoT-J 2025，付费墙 | notes-done | 精读候选 |
| `LOZANO-2025-CONTINUAL` | Continual DRL：持续学习+模型预期+联邦（本平台前身系列） | A | TCOM 2025，代码公开 | full-readnotes-done 精读候选 |
| `ZHANG-2025-GRLR` | GRLR：GNN 特征+Actor-Critic 逐跳 | A | TVT 2025 | notes-done | 精读候选 |
| `LYU-2024-CMADR` | CMADR：约束 MARL 天地一体化路由 | A | JSAC 2024 | notes-done | 补读 |
| `CHU-2023-RRSDRL` | RRS-DRL：AoI 入奖励的罕见先例 | A | Electronics Letters 2023 | notes-done | 补读 |
| `CHOU-2026-STL` | Chou STL：时空学习分布式路由（预印本） | A | arXiv:2605.02413 | full-readnotes-done 补读 |
| `HE-2025-PRIMAL` | PRIMAL：异步 CVaR 尾部时延 MARL（预印本） | B | arXiv:2510.27506 | full-readnotes-done 补读 |
| `LIAQ-2026-QARR` | QARR：队列感知韧性路由（预印本） | A | arXiv:2605.04448 | full-readnotes-done 补读 |
| `CHEN-2025-TMIX` | Transformer-MIX：CTDE 多智能体路由 | A | IoT-J 2025 | notes-done | 补读 |
| `RAO-2025-DGAT` | DGAT：深度图注意力+增量演化 RL | A | IoT-J 2025 | notes-done | 补读 |
| `XIANG-2025-MATGCIR` | MATGCIR：时序图卷积+模仿加速 | A | Comm. Lett. 2025，DOI 未核 | notes-done | 补读 |
| `BAI-2025-GRLRR` | GRL-RR：SDN 域控 GNN 链路权重韧性路由 | A | Computer Networks 2025 | notes-done | 补读 |
| `HUANG-2024-GMR` | GMR：GNN 多径流量工程 | A | TVT 2024 | notes-done | 补读 |
| `HAN-2024-DMR` | DMR：GNN+PPO 多径流量工程 | A | Electronics 2024 | full-readnotes-done 补读 |
| `SORET-2024-QLEARN` | Q-learning 分布式路由（MA-DRL 系列前身） | A | ICMLCN 2024 | notes-done | 补读 |
| `WANG-2021-GROUTING` | GRouting：line-graph MPNN+DQN（GraphPR 前作） | A | HotICN 2021 | notes-done | 补读 |
| `DONG-2023-DQNLLRA` | DQN-LLRA：负载均衡逐跳 DQN | A | Remote Sensing 2023 | full-readnotes-done 补读 |
| `SHI-2024-GNNDQN` | GNN+DQN（GraphSAGE，NSFNet 训练） | A | Applied Sciences 2024 | full-readnotes-done 补读 |
| `ZHOU-2026-DTAR` | DTAR：流量感知域划分+域间路由（预印本） | A | arXiv:2604.12382 | full-readnotes-done 补读 |
| `WEIL-2024-RMP` | Weil：循环消息传递抗陈旧观测（泛图） | B/C | AAMAS 2024，代码公开 | full-readnotes-done 补读 |
| `LI-2023-LUR` | LUR：LEO 多跳 AoI 最小化（集中式） | B | IoT-J 2023 | notes-done | 补读 |
| `ZHANG-2024-NGAT` | NGAT：GAT 组播路由+年龄最优调度 | B | arXiv:2404.18084 | full-readnotes-done 补读 |
| `ALMASAN-2022-DRLGNN` | Almasan：edge-MPNN 路由表示（232 拓扑泛化） | C | Computer Communications 2022 | full-readnotes-done 补读 |
| `BHAVANASI-2023-GNNMADRL` | Bhavanasi：GCN+多智能体韧性路由 | C | TNSM 2023 | notes-done | 补读 |
| `MANFREDI-2021-RELATIONAL` | Manfredi：关系 DRL 无线路由（排队等待显式建模） | C | WoWMoM 2021 | notes-done | 补读 |
| `WIGMORE-2025-MAGNN` | Wigmore：多轴 GNN 排队网络（平均+最坏时延） | C | MobiHoc 2025 | notes-done | 补读 |
| `TALEB-2009-ELB` | ELB：经典队列占用负载均衡基线 | B | ToN 2009 | notes-done | 补读 |
| `SONG-2014-TLR` | TLR：红绿灯拥塞指示绕行 | B | TWC 2014 | notes-done | 补读 |
| `STARTCAP-2024` | StarTCP：Starlink 切换感知传输（测量） | D | APNet 2024 | notes-done | 补读 |
| `IZHIKEVICH-2024` | Izhikevich：Starlink 路径测量 | D | SIGMETRICS 2024 | full-readnotes-done 补读 |
| `MA-2022` | Ma：时变传输距离马尔可夫信道 | D | TVT 2022 | notes-done | 补读 |
| `GUVEN-2023` | Güven：多态 ISL 信道模型 | D | arXiv:2305.07207 | notes-done | 补读 |
| `GANNON-2024` | Gannon：make-before-break 波束切换 | D | ICC 2024 | notes-done | 补读 |
| `GILBERT-ELLIOTT` | Gilbert-Elliott 两态突发错误模型 | D | 标准模型 | notes-done | 补读 |

| `ARXIV-2512.00985` | Age Optimal Sampling and Routing（间歇链路+能量） | B | arXiv | full-readqueued 反向检索新增 |
| `ARXIV-2007.05449` | LEO 多跳更新包新鲜度（2007.05449） | B | arXiv | full-readqueued 反向检索新增 |
| `ARXIV-2111.09217` | Multi-Hop 无线网络信息新鲜度（Yates） | B | arXiv | full-readqueued 反向检索新增 |
| `ARXIV-2310.03969` | NTN AoI 分析（2310.03969） | B | arXiv | full-readqueued 反向检索新增 |

| `OPENALEX-LEOCC` | LeoCC：LEO 拥塞控制鲁棒性（SIGCOMM 2025） | B | ACM gold | queued | 渠道扩展新增 |
| `OPENALEX-SENSORS-DRL-ROUT` | DRL 路由（Sensors 2025，OA） | A | gold | full-readqueued 渠道扩展新增 |
| `OPENALEX-FSO-SCHED-ROUT` | FSO 调度+路由联合（IoT-J 2025） | A | 付费墙 | queued | 联合调度候选线 |
| `OPENALEX-HIER-MWC2026` | 多层星座分层智能路由（MWC 2026） | A | 付费墙 | queued | 2026 最新线 |
| `OPENALEX-LYAPUNOV-WCNC` | Lyapunov 分布式路由（WCNC 2025） | B | 付费墙 | queued | 非学习对照 |
| `OPENALEX-HIER-TE-3D` | 3D 分层 TE 图 DRL（Electronics 2025，OA） | C | gold | queued | 引用链发现 |
| `OPENALEX-CENTRAL-DIST-JOINT` | 集中-分布联合路由（Appl. Sci. 2025，OA） | A | gold | queued | 渠道扩展新增 |
| `OPENALEX-AI-SATCOM-SURVEY` | AI 卫通综述（COMST 2025） | D | 付费墙 | queued | 查缺补漏 |
| `OPENALEX-ANTIJAM-TAES` | 抗干扰 GNN 路由（TAES 2026） | A | 付费墙 | queued | 安全线 |

## 变更日志
- 2026-09-03（第五轮）：深读批 17/17 全部完成（全文级）；9 关定稿+中心问题拟冻结；T1 设计 v0.3；CLOSED：空白点 4 重证据、共性证据 7 家同构。
- 2026-09-03（第四轮）：36/36 笔记全部落地；OpenAlex/引用链新增 9 篇（含 LeoCC SIGCOMM2025、FSO 调度+路由、MWC2026 分层路由）；MATGCIR DOI 修正为 10.1109/lcomm.2025.3601011；DONG 队列值以摘要 5%/13% 为准。
- 2026-09-03（第三轮）：sa1+sa3 两批 20 篇笔记落地（raw/），空白点经 sa1 逐篇复核+arXiv API 双重确认。
- 2026-09-03（第二轮）：arXiv 反向检索复核空白点 → 新增 4 篇队列文献（详见 KNOWLEDGE-MAP 空白点独立复核）。

- 2026-09-03：从 SOURCES.csv + 2026-08-13 调研笔记初始化台账；全 36 篇进入筛选（子代理并行，摘要笔记写入 raw/）。