# C2 负载模型审计扩展（AUDIT-EXT-C2，主控执行，2026-09-11）

> **状态：已被 AUDIT-FULL-111.md 取代**（全库 111 篇审计，2026-09-11 晚些）。本文件保留作中间记录；其发现（TQF59BD7 等）已全部并入全库版。

> 对应 C2-v2 §4 M0 先行步①「审计表 14→20 篇」的文献侧部分（实验侧部分本轮不执行）。
> 方法：对 VM MinerU 全库（111 篇）做过程关键词扫描（poisson/burst/ON-OFF/CBR/self-similar/heavy-tail/MMPP/traffic model/arrival rate 等），
> 取命中最高且未入 C2 14 篇的前 6 篇，回 MD 取上下文行。检索词与 C2 原审计一致，口径相同（"未命中"仅指本次检索）。

## 新增审计行（5 篇入表 + 1 篇排除）

| itemKey | 文献 | 负载过程形态（核验所见，含行号） | 过程参数入状态或扫描？ |
|---|---|---|---|
| 4QG5VYHQ | Information Freshness of Updates Sent over LEO Satellite Multi-Hop Networks（Chiariotti 等，AoI） | 源=Poisson 过程 rate λ，各节点 Poisson cross traffic（L58）；M/M/1 串联排队网（L60） | 无（解析模型，无过程形状变量） |
| TQF59BD7 | IDLB: SDN-Based Load-Balancing Routing Protocol for Autonomous Satellite Constellation Networks（Roth 等） | **仿真器同时具备 ON-OFF 与 CBR 会话**，但 "we focus on the latter for more coherent results"（L371 逐字）；自知突发存在："bursty traffic spikes may result in saturated links"（L341）；会话开始均匀采样、时长指数分布（L371） | 无（ON-OFF 能力存在但未用于评估） |
| 2QRYMWBI | AI for Satellite Communication and NTN: A Survey（Fontanesi 等） | 综述，无自评合同；提及 Poisson 仅作随机接入解析假设（L566） | —（综述） |
| LNA28YZY | Satellite Communications in the New Space Era: A Survey（Kodheli 等） | 综述；承认 "packet traffic in broadband services is bursty"（L414 逐字）作为调度设计动机 | —（综述，承认突发但未参数化） |
| BLFJ6CLV | Analysis of Age of Information in Non-terrestrial Networks（Lu 等） | 本次关键词检索未命中过程描述（解析式 AoI 论文，未核全文） | 未命中 |
| ~~LJG6ZW7B~~ | Sutton & Barto《Reinforcement Learning: An Introduction》 | **排除**：教科书，非 LEO 路由评测合同 | — |

## 对 C2 主张的影响

1. **审计计数**：14 篇 → **19 篇**（5 新增有效行），"同均值过程形状作自变量"仍为 **0/19**。
2. **TQF59BD7 是最强新增证据**：它证明"突发能力在工具链中存在、但被评估侧主动排除"（ON-OFF 可用却聚焦 CBR，理由竟是"结果更一致"）——这把 C2 的盲区从"没做过"推进到"**有工具、被排除**"，比 0/14 的纯缺失表述更硬。
3. **两篇综述**（2QRYMWBI/LNA28YZY）确认"突发"在卫星通信领域是公认动机，但参数化扫描在路由 RL 评测中缺位——支持 C2 §6 反证 2 的口径（现象是老命题，贡献在合同化）。
4. BLFJ6CLV 未命中不解读（仅指本次检索词未命中，不外推）。

## 边界
- 本扩展只覆盖"过程形状是否作自变量/入状态"一个维度；未逐篇核读全文（上下文行级核验）。
- 14→19 的口径仍是"本次语料 + 本次检索范围内"，不作领域级空白声明。
