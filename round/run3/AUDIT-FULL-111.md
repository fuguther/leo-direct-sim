# 全库负载模型审计（AUDIT-FULL-111，主控执行，2026-09-11）

> 触发：用户指正——完整 111 篇文献在 VM（MinerU MD），此前审计只覆盖 19 篇，"0/19" 不能代表全库。
> 本文把审计推到 **111/111**，并相应**收紧** C2 的三条主张。
> 取代：AUDIT-EXT-C2（14→19 的中间扩展；其发现已全部并入本文）。

## 0. 方法与口径

- **覆盖**：VM /data/liguang13/topic-loop-r2/md 下 111/111 篇 MinerU MD（2.0 GB），无遗漏。
- **方法**：两轮全库关键词扫描 + 重点行上下文核验：
  - Pass 1（全库）：poisson/bursty/burst/on-off/CBR/self-similar/heavy-tail/MMPP/traffic generation/traffic model/packet arrival/arrival rate/arrival process/traffic intensity/flows|packets per second/inter-arrival 等；
  - Pass 2（对 Pass1 ≤2 命中者）：traffic load/offered load/network load/load level/exponential/uniformly/every (second|interval)/each time slot/per second/traffic demand/generated at/we simulate 等；
  - 承重行（下表标 ✅ 者）已回 MD 取上下文行核验。
- **口径纪律**："未命中"= 两轮关键词级未发现，**不等于全文精读确认**；约 40 篇有上下文行级核验，其余为关键词级。逐篇全文精读未做（111 篇不现实），如需把某行升级为承重证据，按 C2-v2 的方式回原文取上下文。

## 1. 表 1：学习法路由/TE（31 篇，逐篇）

| itemKey | 文献（简称） | 负载过程形态 | 形状作自变量？ | 状态含过程特征？ | 训练-评估过程分离？ |
|---|---|---|---|---|---|
| CMNCS52M ✅ | Traffic-Aware MARL-DQN | 外生队列正态采样/填充，时间特征被删除（L89/L97/L177） | 否 | 否（瞬时/降维） | 否 |
| JLF7IEBQ ✅ | SaTE（监督 GNN-TE） | 1s 泊松流（L232）；扫描轴仅均值 125–500 flows/s（L292） | 否 | —（集中式 TE） | 否 |
| Y2H4NPLU ✅ | Q-learning 分布式路由 | 网关泊松（L44） | 否 | 否 | 否 |
| UKBSA7WN ✅ | RL 动态分布式路由 | 单位时间包数 x_k 随机（分布名截断为 P…，疑泊松，L89） | 否 | 否 | 否 |
| 42E4NAQU ✅ | Queue-Aware MARL（LIAQ） | 空间双模式（均匀/人口，L123）；无时间过程 | 否 | 否（瞬时 q） | 否 |
| LZKNZA8B ✅ | Spatial-Temporal Learning | NHPP+确定性正弦调制（L66），时变≠突发 | 否 | **弱**：序列网络学历史拥塞模式（L160） | 否 |
| 39NJWBI7 ✅ | PRIMAL（HE） | 训练=评估同为 10,000 pps 单速率泊松（L393） | 否 | 否 | 否 |
| S85KQ4FC ✅ | Flow-Centric DRL | 用户规则间隔发包（L105）+ 决策队列泊松（L138）；网络级 GPW 人口+负指数到达；强度扫描仅用于决策器实验 | 否 | 否 | 否 |
| J68GU76W ✅ | RL Opportunistic Routing（SDN LEO-地面） | 人口密度 × 日内正弦调制 M_tod(h)=αsin(2π(h−τ)/24)+β（L67）；平滑周期，非突发 | 否 | 否 | 否 |
| CYMQ2GLA ✅ | DRL-THSA（两跳状态感知） | 过程未描述（两轮未命中） | 否 | **弱**：EWMA 平均输入/输出速率（L65–67，设计意图是**滤掉**短期波动） | 否 |
| 6GWNYSTT ✅ | 激光/微波混合 Q-routing | M/M/1 泊松（L96–143） | 否 | 否 | 否 |
| 9C6HB6AF ✅ | Multipath DRL | 流级流量模型（§3.2）；只做强度扫描（图 6–8） | 否（仅强度） | 否 | 否 |
| UKEKU5ZG ✅ | 集中-分布联合 MARL | 恒定负载 3000 包（L255） | 否 | 否 | 否 |
| EG9X569M ✅ | Robust Routing DRL | 随机源宿发包（L188），过程未明 | 否 | 否 | 否 |
| GPDPLJNG ✅ | Multi-Commodity Flow DRL | 每用户每时隙定数请求（L236） | 否 | 否 | 否 |
| GPLEP83L ✅ | LLM 奖励设计 | 用 LOZANO 模拟器：网关 64,800 bit 块（L85） | 否 | 否 | 否 |
| 47J2H748 ✅ | Q-routing 原典（通用网） | 多负载**水平**扫描（L46/60）；无形状变量 | 否（仅强度） | 否 | 否 |
| TSV3IE8S ✅ | 多径+Q-learning | 业务流到离为"随机过程"未具体化（L165） | 否 | 否 | 否 |
| 5PYWVRC5 / L2VKYTAV | Shaping Rewards MADQN（重复入库） | 两轮未命中 | — | — | — |
| 53HEEK33 | Fast-Convergence RL | 两轮未命中 | — | — | — |
| 3MRQRWHU | Multi-QoS RL | 两轮未命中 | — | — | — |
| XLRW7XXN | DQN 负载均衡 | 离线=历史+仿真数据（L146）；过程未明 | 否 | 否 | — |
| X5Z98UPM | DRL 负载均衡 SAGIN | 计数 3 但未捕获行；未命中（本次） | — | — | — |
| YI9G7NR7 | 快收敛 RL（TransFun） | 两轮未命中 | — | — | — |
| MXQVNU3P | GNN+DQN | 流量需求（src,dst,bw）驱动（L240） | 否 | 否 | — |
| XM64YRAW | GNN+DRL | 每 ISL 平均负载 λ_ij（L62） | 否 | 否 | — |
| 5N5LQPPP | SDDRL-SR | 未命中（指标为 packet arrival ratio） | — | — | — |
| PIXWFHAC | RL 星地路由 | 未命中（Walker 48 星合同） | — | — | — |
| ZIUBKVPZ | Constrained DQN | 未命中 | — | — | — |
| WFA3CZLP | FlexSATE（监督 TE） | MCF 真值、需求驱动（L116–124） | 否 | — | — |
| 2FBBURX7 | GAT RL 组播+AoI | generate-at-will 每时隙（L106） | 否 | 否 | — |

**表 1 小结**：31 篇学习法路由/TE 中——突发族过程（ON-OFF/MMPP/自相似/重尾）**0 篇**；同均值形状参数化 **0 篇**；状态含突发形状语义 **0 篇**（弱时间聚合 2 篇：CYMQ2GLA、LZKNZA8B）；训练-评估过程分离 **0 篇**。

## 2. 表 2：经典/仿真路由中的流量模型（重点行）

| itemKey | 文献 | 核验所见 | 对本题的含义 |
|---|---|---|---|
| **JP79GMZS** ✅ | ELB（Taleb 2009，启发式） | **"600 non-persistent On-Off flows… On/Off periods derived from a Pareto distribution with shape 1.2. The average burst time and the average idle time are set to 200 ms"（L215 逐字）**；源速率 0.8–1.5 Mbps 为负载轴 | **突发模型在前 RL 时代的 LEO 路由评估中存在**；但形状固定（1.2/200ms），扫描轴是速率——形状从未成为自变量 |
| TQF59BD7 ✅ | IDLB（Roth，SDN 负载均衡） | 仿真器同时具备 ON-OFF 与 CBR 会话，评估聚焦 CBR"for more coherent results"（L371 逐字）；自知 bursty spikes 可致链路饱和（L341） | "有工具、被排除"的最硬证据 |
| 9GPFG5U3 ✅ | LiR 链路标识路由 | OMNeT++ 包级；单流/一对多模式 + 强度（L491） | 强度轴 |
| AF674CSF ✅ | LPIH 分层路由 | 同上平台族，流量模式+强度（L316） | 强度轴 |
| IXVSNEE3 ✅ | 最小跳数星地协同 | 到达率扫描至饱和（L525–549） | 强度轴 |
| 9KZDXPKC ✅ | DB-R（CUBIC/BBR 在空间） | 泊松流 + 经验流长分布（L252） | 泊松 |
| SBCHGBCP ✅ | 段路由 TE | 均匀/美国边界两种流量矩阵（L244） | 需求矩阵 |
| X5K285MW ✅ | 源路由分析（Roth） | 会话模型；非均匀 UT 分布热点（L90–92） | 空间轴 |
| VFS59FHI | 段路由网关拥塞 | 地理流量小区（L62） | 空间轴 |
| BBNQ4EAQ | Temporal Netgrid 动态路由 | 承认随机包到达（L22） | 未具体化 |
| AIH4GK37 | 区域几何与 LS 路由扩展性 | **Pareto 故障**模型（L348）——是链路事件不是流量 | 不误计 |
| AJJI57M9 | Ekici 数据报路由（2001） | 缓冲占用判拥塞，不交换负载信息（L269–271） | 无过程 |
| TSV3IE8S ✅（引用级） | — | 参考文献 [3]：Gragopoulos 等 2000《…LEO satellite constellations under **Self-Similar and Poisson traffic**》（L309） | **2000 年已有自相似 vs 泊松对照研究**（引用级，全文未取） |
| 其余（DVS8C3CC、36RZKNW5、TRM2HPFN、K7U4TYJN、2W8BJ7ME、R37BNQQ8、XM6NUPM4、JS857IYN、YD4JUT7G、LBMABZJ7、JZA5SEQA、WHS8Z44C、X2FCSU4S、CTWVLBCY、K93SCUF2、67CSKFK4、W5Z39E25、UF8IQTA2、XM64YRAW 等） | — | 两轮扫描未见突发族过程 | 未命中（关键词级） |

## 3. 表 3：范围外归组（不计入分母）

- **测量/平台（13）**：5HJ8ATR7、AZ72LM9Z、GGFJ3SEG、GJJQUMQ2、L63JISQN、MYBALQ2D、NPF75WS5、P6XJZNQK、S2QZRBEJ、W6M3GU7L、8AYW2Y78、IEI3BYFF、DS9SPARV。其中 **S2QZRBEJ 实测 Starlink 丢包突发分布**（L129–133）——真实网突发存在的测量级支持。
- **综述（13）**：2QRYMWBI、LNA28YZY、7AXASN73、IP7RRM3A、LRSXMWX9、QSNRQ8PF、T9X6QCLL、Z74SR656、L5F3DK68、5AZHJE7N、524XNF29、UMKF328H、BV4XI6CU。
- **通用 RL 方法（11）**：LJG6ZW7B、57EB6US5、6C843JTS、TAUEF8PF、JSX5XG88、9FLZ88LZ、KPUZIMU5、FGQSH4AI、E4NYGLGX、I2WH9RRR、QGAREQUM。
- **AoI/调度理论（4）**：4QG5VYHQ、BLFJ6CLV、GV9PPNZT、R5QTFKD2（泊松/M/M/1 解析模型）。
- **领域外（5）**：A7QNRKML（人脸关键点）、ETTA3DIV（聚变等离子体）、VACUFEHB（Volterra 滤波）、WT839JP7（代码膨胀）、35T2JJRJ（版权页级内容）。
- **经典路由其余**：见表 2 末行。

## 4. 结论：C2 三条主张的全库修订版

| # | 修订后主张（全库口径） | 计数 |
|---|---|---|
| R1 | **同均值形状参数化（锁均值扫形状）在任何文献类型中均未见** | **0/111** |
| R2 | **突发族过程（ON-OFF/MMPP/自相似/重尾）进入学习法路由的训练或评估：未见**；前 RL 时代存在（ELB 2009 ON-OFF Pareto 固定形状；Gragopoulos 2000 自相似 vs 泊松，引用级） | **0/31**（学习法）；2 篇前 RL 经典 |
| R3 | **状态含突发形状语义特征（相对 T_on 的趋势/占空语义）：未见**；弱时间聚合 2 篇（CYMQ2GLA 的 EWMA 速率——设计意图是**滤掉**短期波动；LZKNZA8B 的序列网络编码——过程是平滑 NHPP） | **0/31**（强语义）；2/31（弱聚合） |

## 5. 对三卡论证的影响

1. **C2（主线）**：G1 证据基座从 19 篇升为全库 111 篇；主张按 R1–R3 收紧（学习法子文献 0/31 + 全库 0/111 同均值合同）。**裁决不变**：同均值合同与突发入 RL 两个核心空白都存活；但"现象非新发现"的名单从 [Shi03] 扩到 [Shi03] + ELB 2009 + Gragopoulos 2000——C2 的贡献定位（合同化 + 协议 + 训练/状态件）更加依赖"RL 时代 + 同均值参数化"的精确表述。
2. **A3（备选）**：不受影响（决策资源轴，锚件不变）。
3. **新增近邻登记**：CYMQ2GLA（弱 EWMA 状态特征，设计意图相反）与 LZKNZA8B（已列）进入 C2 的近邻表；JP79GMZS 的突发模型事实进入 READING-GUIDE。
4. **B3 不变**（本轮已退出，强度轴并入主线设计）。

## 6. 边界与未决

- 两轮关键词扫描对"未命中"行不构成全文级排除；若某篇对裁决变为承重，须先回全文取上下文行升级核验。
- Gragopoulos 2000 为引用级线索（经 TSV3IE8S 参考文献），全文未取；[Shi03] 同。
- X5Z98UPM 已补查（2026-09-11 第二批）：流量=100 对随机源宿（L271），无过程族描述、无突发、无同均值扫描——维持表 1"未命中"行，**不构成反例**。至此全库无悬空待核项。
