# claim-map.md — RL-LEO 路由文献主张地图（47 篇精读笔记聚合）

> 条目格式：- 主张 ｜ from:[笔记ID] ｜ quote:引用编号或短引 ｜ confidence:级别
> confidence 口径：全文级=基于全文精读笔记；摘要级=仅摘要级笔记；检索级=仅标题级笔记。

## A. 仅路由（拓扑适应/最短路替代/学习型路由本身）

- 分布式 tabular Q-routing（2bit 邻居状态压缩）在稳态时延上与两个集中式最短路径基准相当，并把拥塞临界负载门限从 8–9 个网关推迟到 >14 个（ℓ=0.85，140 星）｜ from:[2306.01346] ｜ quote:"comparable in terms of E2E delay, while it supports a higher traffic load" ｜ confidence:全文级
- MA-DRL 两阶段（离线全局 DNN 训练 + 在线星上预训练 DNN 利用）能在 <1 秒仿真实时时间内收敛到最短路径，且学到一组替代路径供拥塞时切换（初步结果、单图定性）｜ from:[2402.17666] ｜ quote:"learns first sub-optimal paths and then converges to the shortest path in less than 1 second" ｜ confidence:全文级
- GAT(空间)+LSTM(时间)+DQN 的分布式路由在吞吐/丢包/队列长/E2E 时延上全面优于 Dijkstra、FDR-MARL、DQN-IR、GraphPR，重载下队列长度最多降 23.26%（45 星小规模）｜ from:[2605.02413] ｜ quote:"up to 23.26% queue reduction" ｜ confidence:全文级
- queue-aware MA-DRL（DDQN，集中预训练下发+在线更新）以约 50% 的 Dijkstra 决策开销换取时延 49.31 ms（Dijkstra 38.54 ms 为队列近理想条件下的数值），且 Dijkstra 重算间隔 >10 s 后路径失效率与时延反而恶化｜ from:[2605.04448] ｜ quote:"approximately 50% of Dijkstra at a 5 s recalculation interval" ｜ confidence:全文级
- 图约束 Transformer（邻接矩阵硬嵌入 attention）+ NFD 自蒸馏在随机失效/定向攻击下接近 Dijkstra 最优且吞吐显著高于主流算法；多域 C20 场景对 Δ-stepping 吞吐增益 23–101%，且低同步率区学习法有时优于全信息基线｜ from:[ieee-11556312] ｜ quote:"all neural models except TRACE-NFD-4 fall below the baseline"（D50 尺度反转现象）｜ confidence:全文级
- 分层"区域间 GNN-PPO 方向决策 + 区域内负载感知 Dijkstra"在 3600 星 TLE 仿真中成功率 0.9980（无故障）/0.9410（故障），全局法 GC/GGAP 故障下跌至 0.36/0.18；教师引导 warm start 是收敛的必要条件而非加速项｜ from:[ieee-11651610] ｜ quote:"training without teacher guidance fails to achieve comparable convergence under either learning rate" ｜ confidence:全文级
- 动作对齐局部图（每条候选边=一个动作表示 uij）的 hop-by-hop SAC 路由在 hub-inversion 场景总时延 47.64 ms、排队时延 5.81 ms、投递率 99.93%，排队时延从 MATMR 的 10.78 ms 减半；288→864 星扩展性能稳定｜ from:[ieee-11661488] ｜ quote:"cuts queueing delay from 10.78 ms to 5.81 ms" ｜ confidence:全文级
- 集中-分布联合路由（地面预训练 Q-table 上传 + 在轨在线微调 + 周期链路广播）在时延/丢包/负载方差/到达率上优于集中式 DR-BM 与 1993 版 Q-routing（49 星，表格 Q-learning，无 DRL 基线）｜ from:[doi-10.3390-app15094664] ｜ quote:"ground stations initialize Q-tables and upload them to satellites" ｜ confidence:全文级
- 联邦 Dueling-DQN（分簇半异步聚合 + PER 关键样本保护）把训练期累计通信开销较中心化 DQN 降 70.8%，收敛时延 46.1 ms（较 Dijkstra 74.0 ms 降 37.7%），288 星故障注入场景（5% 节点+10% ISL 随机失效）｜ from:[ieee-11565396] ｜ quote:"reduces cumulative communication overhead by 70.8%" ｜ confidence:全文级
- DDQN + "转发方向"动作空间（与星座规模解耦）在 66 星 HLA/EXata 平台实现 8 平均跳数、270 ms 收敛、0.96 s E2E 时延、20% 卫星失效下丢包 ≈0.3%（单场景自比，无基线对照）｜ from:[ieee-11638046] ｜ quote:"8 average hops, 270 ms maximum convergence time" ｜ confidence:全文级
- 两跳状态感知 DDQN（地面离线训练、星上只推理不更新）在 Iridium-like 66 星 NS-3 仿真中时延/丢包/吞吐均优于 ELB/TLR/ELMDR（每目的星存一个模型，模型数=卫星数）｜ from:[doi-10.3390-electronics8090920] ｜ quote:"the number of DDQN is equal to the number of satellites" ｜ confidence:全文级
- TEG 上的时空 QoS-A*（光速时延下界 admissible 启发式 + 剩余可见寿命剪枝 + 事件驱动重路由）相对传统最短路任务成功率提升 100–300%、最大链路负载降 60% 以上，代价是平均跳数增加；极轨下增益收窄｜ from:[ieee-11388857] ｜ quote:"increases the task success rate by over 100%, reduces ... maximum link load by more than 60%" ｜ confidence:全文级
- 配置得当的 OSPFv3（Hello/Dead=1/2 s、P2P 接口）在 Iridium 66 星容器级全栈仿真中收敛均值 2.18–2.35 s、丢包 1.62%，可维持鲁棒连通——但默认参数不适合高时变拓扑｜ from:[ieee-11308874] ｜ quote:"default behavior and timing parameters are not well suited for highly time-variant topologies" ｜ confidence:全文级
- 配置得当的 OSPF 在 Teledesic 288 星 Walker-star 连续移动场景下拓扑变化只影响局部节点子集且时间分散，可稳定运行并保持用户 QoE、信令开销低（DRL 路由增量价值的反方基线）｜ from:[tail-112555] ｜ quote:"topology changes affect only localized node subsets and occur temporally spaced" ｜ confidence:摘要级

## B. 拥塞感知 / 负载均衡路由

- 混合"离线 Dijkstra 表 + DQL 仅作回退"策略在所有负载上稳定优于纯 DQL：PDR 93–99% vs 72–97%、中位时延 60 vs 80 ms，且回退激活率 η≤0.4 时 <1%（160 星 MATLAB 包级仿真，唯一基线是纯 RL）｜ from:[2509.14909] ｜ quote:"RL is invoked only as a fallback mechanism" ｜ confidence:全文级
- DTAR（离线 NSGA-II 域划分 + 在线 GAT 边特征 + action-masked PPO）在 288 星故障场景 SR 比 Dijkstra 高 9.25pp、比 CDPAR 高 8.89pp；ELB/QRLSN 的 CV 反而高于 Dijkstra；负载均衡目标 CV 只经观测隐式优化而非奖励显式优化｜ from:[2604.12382] ｜ quote:"9.25 and 8.89 percentage points over Dijkstra and CDPAR" ｜ confidence:全文级
- KSP 候选路径压缩动作空间（K=20）+ PPO 在激光 LSN（42 星）全流量密度下阻塞率最低、链路利用率均衡（仅图无数字，基线只有 Dijkstra 与随机路由）｜ from:[ieee-11656129] ｜ quote:"When K=20, the algorithm performs best" ｜ confidence:全文级
- SAC 拥塞-路由联合优化（20 星随机网络、50 包）最终奖励略高于 TD3；Dijkstra 时延最低但拥塞最高，本方法在时延与拥塞/利用率之间可调（无量化数值表）｜ from:[ieee-10405470] ｜ quote:"The Dijkstra algorithm achieves the lowest average latency but incurs the highest congestion" ｜ confidence:全文级
- Pareto-MARL 包路由框架（MAPPO + 分解式加权标量化 + 邻域参数迁移，G/G/1/K+WPQ+AQM 队列模型）主张多目标 MARL 优于加权求和单目标与无队列感知基线——但实验章节在提取文件中截断，全部数字未报告｜ from:[ieee-11165331] ｜ quote:"the first work to incorporate multiobjective MARL into packet routing for satellite networks"（实验证据不可核验）｜ confidence:全文级
- CGR 在 TTL 过滤后改用最少跳数（CGR-Hops）或跳数/时间多目标（CGR-MO）可在不牺牲时延敏感流量的前提下显著提高投递率与能量效率，代价是推后无约束流量；ILP 上界恒为投递率 1｜ from:[2304.13501] ｜ quote:"CGR-Hops delays traffic that can be delayed ... allowing traffic that needs to be delivered earlier to reach on time" ｜ confidence:全文级
- 能量感知 E-CGR（发送前外推下一跳未来能量可行性）把高负载下 ADT 恶化从标准 CGR 的 +135% 压到 +63%，未送达比例从 6–29% 降到 6–18%（120 纳米卫星 NS-3）｜ from:[ieee-9023977] ｜ quote:"up to 135% by using the standard CGR and up to 63% by using the E-CGR" ｜ confidence:全文级

## C. 资源调度（波束/功率/信道/链路调度，非纯路由）

- 多波束上行 DQN（状态重构：合并服务波束与周围三/四层同心波束）在 200 用户高负载时阻塞率从 Q-learning 的 ~20% 降到 ~15%（权重 1/2 时 ~12%），代价是更高功耗（唯一基线为 Q-learning）｜ from:[doi-10.1186-s13677-024-00621-z] ｜ quote:"reduces the blocking rate by at least 5% compared to reinforcement learning methods" ｜ confidence:全文级
- 288 星域间"图-时间"联合缓存放置与路由（GT-SAC，2 层时空 GNN 编码进 SAC 状态）较 Cloud/PCF 提升成功率 59–66%/23–27%，但对无 GNN 的 SAC 优势仅 2.5–2.6%（单次运行无方差）｜ from:[2508.16184] ｜ quote:"improved by approximately 59.2%, 23.3%, and 2.5% compared to the cloud, PCF, and SAC schemes" ｜ confidence:全文级
- 残差 RL（DDQN 叠加 backpressure 基线 + LG 感知项）相对 backpressure 降均值队列 1.6%（小邻域）→12.1%（大邻域），跨 Starlink/Iridium/OneWeb 平均 7.6–16.1%（真实 TLE+人口流量，5 seeds）｜ from:[2601.13662] ｜ quote:"1.6% ... 12.1%" ｜ confidence:全文级
- MADRL 动态激光 ISL 调度（3 固定+1 动态链路、奖励按链路贡献分解、CS 压缩状态）相对固定 4-LISL 降能耗 ~15%、降时延约 2 跳（720 星，Double Dueling DQN 参数共享，GEO 数据中心训练）｜ from:[ieee-10375570] ｜ quote:"reduce energy consumption by over 15% and delay by approximately two hops" ｜ confidence:全文级
- 预测驱动双时间尺度波束跳变资源分配（TFT 预测 + capped-utility 凸规划 + Lyapunov 队列纠错 + FP）较 Myopic 基线长期满意度 +40%、边缘速率 +35%、吞吐几乎无代价——但作者明示结论仅限 7 小区 14 用户设置｜ from:[ieee-11588585] ｜ quote:"the results and conclusions in this paper are restricted to the considered setting" ｜ confidence:全文级
- 柔性波束图选择 + 功率/关联/调度联合优化（分式规划+swap 局部搜索）较 Best-channel 降容量-需求错配 27.7–44.9%，自适应波束图最多降 91.6%；"信道好需求高的用户被窄波束服务"｜ from:[ieee-10486925] ｜ quote:"reduce the capacity-demand gap by 27.67% and 44.92%" ｜ confidence:全文级

## D. 联合（路由+切换/功率、路由+缓存、多层）

- 层感知 MARL（MAPPO+TarMAC 关联决策 + 每 slot CVXPY 凸功率闭环）达 greedy SNR 方案 ~92% 吞吐、切换次数从 28.5 降到 6.2（>4 倍），出现 95% LEO + 5% MEO/GEO 涌现式卸载；stay 基线切换更少但吞吐低 14%｜ from:[2608.14335] ｜ quote:"92% of the throughput ... more than four times fewer handovers" ｜ confidence:全文级
- 大规模 SFC 约束路由（GCN+PPO，6048 星、用户按 WorldPop 铺设、TR 38.811 信道）较三类基线降时延 >11.3%、降负载 >14.1%、成功率 +19.1%、容量 ×2（自称现有文献最大仿真规模）｜ from:[doi-10.3390-s25041232] ｜ quote:"the size of the simulation network we used is the largest among the papers available so far" ｜ confidence:全文级
- LLM 闭环自动奖励设计（LARGE：三 agent + 仿真器在环迭代）能在 3 次迭代内达到 goodput 距专家奖励基线 ~3% 以内且时延略低，无手工奖励工程；更有价值的产出是暴露吞吐-时延-路由效率的替代性权衡而非单指标超越｜ from:[2608.01649] ｜ quote:"within approximately 3% of the baseline ... without manual reward engineering" ｜ confidence:全文级

## E. 优化参照 / 非学习基线与测量锚点

- 平均奖励 SMDP 的 actor-critic 与乐观策略迭代（RL 路线）比 MAXMIN 高 30.6–7.1% 收益、合计最高 56.6%，且 C≥20 时精确 DP 计算上不可行——"DP 不可行 → RL 近似"的经典论证（2007，36 节点快照拓扑）｜ from:[ieee-4200818] ｜ quote:"up to 56% higher average revenue ... with reasonable storage and computational requirements" ｜ confidence:全文级
- 接触计划层：path-private 评估在共享接触下最多低估完成时间 154.3 s 甚至误报"有限完成"；残余服务计账 + 有界 two-way striping 把对受限穷举参考的差距从 ~47 s 降到 ~28 s（P90 尾部不变，源于计划选择分歧）｜ from:[2607.04405] ｜ quote:"under-counts completion by up to 154 s" ｜ confidence:全文级
- 导航-通信双目标接触计划存在内在冲突：通信最优计划 BDT=4.5 s/定位误差 >10 m，导航最优 BDT=6 s（差 25%）/误差 6 m（好 40%）；模拟退火可描出 Pareto 前沿（月轨 12 星）｜ from:[ieee-10521114] ｜ quote:"BDT of 4.5 seconds ... positioning error of over 10 meters" ｜ confidence:全文级
- Starlink 端用户实测：时延均值仅比地面高 ~10% 但波动 ~3.8 倍、吞吐 ~80 Mb/s（std 50.71%）、降水降吞吐 27%、bent-pipe 单跳始终接最近地面站——为仿真提供经验锚点而非控制主张｜ from:[2212.13697] ｜ quote:"around 3.8 times that of the terrestrial network" ｜ confidence:全文级
- Starlink 每 15 s 全局同步重配置造成边界处亚秒级时延/吞吐劣化，且该效应与卫星切换无关（19.2M M-Lab + 1.8M 探针 + 双国受控实验交叉验证）｜ from:[2310.09242] ｜ quote:"Hand-offs between satellites are not the cause of these effects" ｜ confidence:全文级
- Starlink 队列实测：单一共享队列（无 per-flow 公平排队）+ drop-front 缓冲管理 + ~1500 包队列上限，1.33 ms 帧级 drain——解释 Cubic 低吞吐异常的背景但未确立因果｜ from:[2605.27717] ｜ quote:"does not employ per-flow fair queuing or drop-tail buffers, but it does use drop-front" ｜ confidence:全文级
- 车载 Starlink：一旦移动吞吐约降 10%，车速本身无显著影响；城区遮挡丢包至 10%、山区 45%；FHP 碟均功耗 113 W 超出车载 90 W 充电能力｜ from:[2403.13497] ｜ quote:"the vehicle speed does not have a direct effect on the download throughput" ｜ confidence:全文级
- Starlink E2E 时延呈确定性 15 s 周期 + 边界尖峰（前 140 ms/后 75 ms，尖峰高出均值 ~74 ms）结构；轻量统计模型（GMM/EVT）1.6–3.5 s 采样即可 AUPRC 0.95，无需 RL/深度学习｜ from:[2601.08439] ｜ quote:"a statistical analysis might provide an equally accurate and more explainable solution" ｜ confidence:全文级
- Starlink 地面网：PoP 周期性切换（160.63→411.93 ms）与骨干路由策略周期性变化（135.20 vs 170.21 ms）是时延一阶因子；23.5K /28 前缀、137 GS/27 PoP 资产库｜ from:[ieee-11143359] ｜ quote:"These two factors were both observed to cause significant variations in network latency" ｜ confidence:全文级
- IPv6 地址规律扫描发现 ~3.2M Starlink 用户路由器（102 国），inside-out traceroute 测绘骨干 PoP 拓扑（数据集公开）｜ from:[2412.18243] ｜ quote:"approximately 3.2 million IPv6 addresses across 102 countries" ｜ confidence:全文级

## F. 跨节主题

### F1. 评估方法论
- 多数 RL-LEO 路由工作以单点曲线值报告、无多种子/置信区间（例外：2601.13662 用 5 seeds、2608.01649 用 10 seeds mean±std、ieee-11661488 用 3 seeds、ieee-4200818 报 98% 置信区间、ieee-11656129 每点 10 次独立仿真）｜ from:[2605.02413, 2508.16184, doi-10.3390-app15094664, ieee-11565396, 2601.13662, 2608.01649, ieee-11661488, ieee-4200818, ieee-11656129] ｜ quote:"无置信区间/多次种子统计报告，全部为单点曲线数值" ｜ confidence:全文级
- "拥塞"的操作化定义各异：回归斜率 t 检验（2306.01346）、队列占比阈值 0.7（2509.14909）、50% 硬阈值（ieee-11638046）、M/M/1 利用率函数（ieee-11388857）、CV 变异系数（2604.12382）、高负载节点占比（ieee-11565396）——跨文献不可直接比较｜ from:[2306.01346, 2509.14909, ieee-11638046, ieee-11388857, 2604.12382, ieee-11565396] ｜ quote:"queue usage exceeds 50% capacity and 0 otherwise" ｜ confidence:全文级
- ILP/受限穷举作性能上界、而非只比弱基线，是评估方法学的正面范例｜ from:[2304.13501, 2607.04405, ieee-4200818] ｜ quote:"ILP 投递率恒为 1" ｜ confidence:全文级
- 评测协议可复用模板：路径 stretch（跳数/Dijkstra 最短跳数）、学习介入频率 p_fb(η)、同步率阈值 R_sync^95、决策开销-重算间隔-路径失效率三角、层关联占比｜ from:[2608.01649, 2509.14909, ieee-11556312, 2605.04448, 2608.14335] ｜ quote:"pfb<1% for η≤0.4" ｜ confidence:全文级

### F2. 仿真保真
- 47 篇中无一篇做硬件在环或在轨验证；sim-to-real 普遍"未处理也未讨论"；实测锚点全部来自独立测量文献（2212.13697/2310.09242/2601.08439/2605.27717/2403.13497/2412.18243/ieee-11143359），且测量文献均未与 RL 控制文献闭环｜ from:[2604.12382, doi-10.3390-s25041232, 2605.27717, ieee-10016705] ｜ quote:"sim-to-real 未处理也未讨论" ｜ confidence:全文级
- 真实 TLE/星历已进入部分 RL 工作（2601.13662、2608.14335、ieee-11651610、doi-10.3390-s25041232），但真实流量 trace 仅 2601.13662（GPW 人口流量）；真实 PoP/GS 拓扑（2412.18243、ieee-11143359）尚无 RL 工作采用｜ from:[2601.13662, 2608.14335, ieee-11651610, doi-10.3390-s25041232, 2412.18243, ieee-11143359] ｜ quote:"Space-Track TLE 真实轨道 + 2020 Gridded Population of the World" ｜ confidence:全文级
- 仿真队列模型普遍理想化（FIFO 定容/无界），与实测 drop-front + ~1500 包 + 15 s 重配置 + 1.33 ms 帧 drain 的 Starlink 真实队列动态不匹配——reward 信号统计特性因此失真｜ from:[2605.27717, 2310.09242, 2601.13662, 2509.14909] ｜ quote:"队列配置错误会显著扭曲 CC（含可学习 CC）性能对比结论" ｜ confidence:全文级
- 快照离散化本身引入伪影：Δt=5 s 快照生成期路径选择不准导致 ~5 s 瞬态时延尖峰；粗快照（20 s）收敛均值反而略高｜ from:[ieee-11308874] ｜ quote:"快照生成期路径选择不准" ｜ confidence:全文级

### F3. 基线公平性
- "让基线处于近理想条件"的选择性公平：Dijkstra 对比时把队列容量设为 1 Gb/s 防溢出（2605.04448）；TarMAC-LEO 加大 LEO 候选池以隔离多层收益（2608.14335，正面范例）；hub-inversion 下 SPF 投递率仅 10.82% 疑为极端配置放大对比（ieee-11661488）；DRL 基线同训练预算（2604.12382、2608.01649，正面范例）｜ from:[2605.04448, 2608.14335, ieee-11661488, 2604.12382, 2608.01649] ｜ quote:"人为让基线处于近理想条件" ｜ confidence:全文级
- 基线过弱是普遍模式：仅对比 1993 版 Q-routing 与速率基准（doi-10.3390-app15094664）、仅 Q-learning（doi-10.1186-s13677-024-00621-z）、仅 Dijkstra+随机（ieee-11656129、ieee-10405470）、单场景无基线自比（ieee-11638046）、无任何对照（ieee-11638046, tail-112555 未披露）｜ from:[doi-10.3390-app15094664, doi-10.1186-s13677-024-00621-z, ieee-11656129, ieee-10405470, ieee-11638046] ｜ quote:"未与最短路径基线或其他 RL 方法的对照实验" ｜ confidence:全文级
- 用地面默认配置评估改造协议会得出误导性结论——调参后的传统协议是必须的基线（ieee-11308874/tail-112555 与 DRL 路线共同指向）｜ from:[ieee-11308874, tail-112555] ｜ quote:"default terrestrial configurations ... often leads to misleading conclusions" ｜ confidence:全文级
- Dijkstra 通信开销 <0.1 MB 完胜所有学习方法——学习方法的开销优势只在"学习方法之间"成立，绝对开销叙事被弱化陈述｜ from:[ieee-11565396] ｜ quote:"Dijkstra 通信开销 <0.1 MB 完胜所有学习方法" ｜ confidence:全文级

### F4. 状态-动作-奖励设计模式
- 状态压缩谱系：2bit 邻居编码（2306.01346）→ 两跳状态表（doi-10.3390-electronics8090920）→ 星形局部图动作对齐（ieee-11661488）→ 全域 GAT 集中式观测（2604.12382）；压缩换算力但损失最优性（2bit 编码正是传播时延略差的归因）｜ from:[2306.01346, doi-10.3390-electronics8090920, ieee-11661488, 2604.12382] ｜ quote:"2 bit 编码把状态空间压到卫星算力可承受，但正是它让传播时延略大" ｜ confidence:全文级
- 动作空间解耦技术：转发方向代替节点 ID（ieee-11638046）、KSP K 选 1（ieee-11656129）、域级四方向（ieee-11651610）、action masking 屏蔽不可行动作（2604.12382、doi-10.3390-s25041232、2505.07290）｜ from:[ieee-11638046, ieee-11656129, ieee-11651610, 2604.12382, doi-10.3390-s25041232, 2505.07290] ｜ quote:"sets the output probability of each invalid action to 0" ｜ confidence:全文级
- 奖励模式库：距离塑形（斜距缩减/距离平方惩罚）、队列指数惩罚、拥塞项权重>时延项（β>α）、到达/成环/失败固定奖惩、Dijkstra 参照差分奖励、全局奖励按链路贡献分解（相关系数>0.98）、三目标加权增量阈值化、LLM 自动生成奖励结构｜ from:[2306.01346, ieee-11638046, 2605.02413, ieee-10375570, ieee-10405470, doi-10.1186-s13677-024-00621-z, 2608.01649] ｜ quote:"β>α 偏置拥塞避免" ｜ confidence:全文级
- 保底+学习修正范式：residual RL 叠加可证稳定 backpressure、确定性表 + RL 回退、教师引导 warm start、Lyapunov 队列纠预测之偏——"可证稳定组件 + 有界学习修正"反复独立出现｜ from:[2601.13662, 2509.14909, ieee-11651610, ieee-11588585] ｜ quote:"retains a stabilizing backpressure bias" ｜ confidence:全文级

### F5. 非平稳与信息时效
- 时标分离是 RL-LEO 的核心合法性论证：学习（亚秒级）远快于轨道运动（分钟级），故快照 POMDP 建模可行——但所有学习法对拓扑/流量联合快变的适应性未被系统检验｜ from:[2306.01346, 2402.17666] ｜ quote:"learn the new paths in less than 0.5 s, therefore at a much faster pace than the movement of the constellation" ｜ confidence:全文级
- 轨道准周期性是 RL 可利用的先验（而非纯负担）——quasi-periodic 拓扑模式使学习型调度可超越纯反应式规则｜ from:[2601.13662] ｜ quote:"quasi-periodic patterns driven by orbital mechanics, allowing the reinforcement learning agent to exploit these patterns" ｜ confidence:全文级
- 全网实时信息不可行：反馈消息拥塞 + 传播时延使全网瞬时状态过期——这是分布式/局部信息路线的存在理由，同时 genie 基线自身因信息过期而非最优｜ from:[2306.01346, 2402.17666] ｜ quote:"it is impractical to have real time information about the whole LSatC" ｜ confidence:全文级
- 15 s 全局重配置是仿真未建模的强非平稳源：任何把性能波动归因于卫星切换的仿真假设与实测矛盾，应建模为全网统一时间步的资源重分配｜ from:[2310.09242, 2601.08439] ｜ quote:"The reconfigurations are synchronized globally and are not caused by satellite handovers" ｜ confidence:全文级
- 训练分布外泛化声明依赖硬可行性保证而非策略泛化：仅训练单一失效模式（定向攻击 p≤0.382）即声称对随机失效与全比例外推稳健（ieee-11556312）；离线训练后星上永不更新（doi-10.3390-electronics8090920）无法适应分布漂移｜ from:[ieee-11556312, doi-10.3390-electronics8090920] ｜ quote:"训练失效模式单一却声称外推稳健" ｜ confidence:全文级

## 张力与空白（tensions）

- **"分布式"叙事 vs 集中式事实**：2605.02413 推理分布式但训练需全网仿真环境、无显式协调机制，为何能全局负载均衡无理论解释；2604.12382 的 GAT 是集中式全局观测却自称解决分布式问题；2608.14335 功率子问题每 slot 集中求解（MOSEK）与"分散执行"叙事冲突；doi-10.3390-s25041232 集中式控制器回避控制面时延 ｜ from:[2605.02413, 2604.12382, 2608.14335, doi-10.3390-s25041232] ｜ quote:"推理分布式，但训练仍需全网仿真环境" ｜ confidence:全文级
- **重载下的相对优势 vs 全员失效区间**：2605.02413 在 240 Mbps（负载/容量 0.8）丢包仍 >46.81%，"显著优于基线"是在系统深度过载区间内的相对排序；11651610 的 0.94/0.998 成功率与 11556312 定向攻击 43.64% 丢包并存——学习法增益区间与失效区间的边界无人刻画 ｜ from:[2605.02413, ieee-11651610, ieee-11556312] ｜ quote:"显著优于基线是在全员失效区间内的相对优势" ｜ confidence:全文级
- **学习法吞吐优势对尺度非单调**：D50+C20 中除 TRACE-NFD-4 外全部神经方法吞吐增益为负（Δ-stepping 反超），小模型救回该区间——"学习路由可扩展"叙事在中等尺度出现反转，机制未被解释 ｜ from:[ieee-11556312] ｜ quote:"all neural models except TRACE-NFD-4 fall below the baseline" ｜ confidence:全文级
- **静态划分 vs 动态前提的循环论证**：2604.12382 以"频繁拓扑变化"为动机，解法却是离线固定域划分 + "域间边集不变"绕开问题；类似地 4200818 的快照分片训练依赖拓扑周期精确重现 ｜ from:[2604.12382, ieee-4200818] ｜ quote:"静态离线划分与频繁拓扑变化的挑战前提存在张力" ｜ confidence:全文级
- **实测知识与 RL 环境完全脱节（无人覆盖的空白）**：Starlink 的 15 s 重配置、drop-front 队列、PoP 切换、遮挡丢包分布均已实测在案（2212.13697/2310.09242/2605.27717/ieee-11143359），但没有任何一篇 RL 路由工作把这些动态纳入训练/评测环境；反之测量文献指出仿真不可替代 ｜ from:[2212.13697, 2310.09242, 2605.27717, ieee-11143359, ieee-10016705] ｜ quote:"real-world measurement ... is irreplaceable" ｜ confidence:全文级
- **混合法的隐藏脆弱点**：2509.14909 把 RL 关进"回退牢笼"，但 RL 只在表失效的分布外尾部学习、每次回退仅一次 TD 更新是否足够未深究；表权重基于平均时延与动态队列存在时效性张力 ｜ from:[2509.14909] ｜ quote:"RL 只在表失效的分布外尾部学习" ｜ confidence:全文级
- **联邦层的 non-IID 盲区**：11565396 批评 DQN 经验相关性破坏 IID，但联邦平均本身假设各星数据可平均——non-IID 联邦难题只字未提；第 46–50 轮性能下降被无机制解释地称为"正则化" ｜ from:[ieee-11565396] ｜ quote:"non-IID 联邦难题只字未提" ｜ confidence:全文级
- **预测-决策联合收益未与"纯掩码"分离**：2505.07290 的掩码收益（时延降 72.05%）远大于预测器收益（奖励 +35.99%），但框架捆绑呈现，缺"纯掩码无预测器"消融；2605.02413 批评解耦设计也只有端到端结果无受控对照 ｜ from:[2505.07290, 2605.02413] ｜ quote:"无法从实验分离纯掩码 MAPPO 这一消融" ｜ confidence:全文级
- **切换成本仅标量抽象**：2608.14335 的层差罚系数 α=0.6/0.8/0.9 外生给定、无敏感性分析，"涌现式卸载"仅由 5% 关联支撑；无信令时延/中断/QoS 违约率建模 ｜ from:[2608.14335] ｜ quote:"卸载行为的出现对 α 敏感性未报告" ｜ confidence:全文级
- **故障模型普遍过弱且互不兼容**：随机独立删边 ≤5 条（app15094664）、5%+10% 独立注入（11565396）、两态 Bernoulli 保连通（2604.12382）、无空间相关失效；真实失效（太阳风暴、遮挡、PoP 切换）测量文献已给出参数区间却未被采用 ｜ from:[doi-10.3390-app15094664, ieee-11565396, 2604.12382, 2212.13697, ieee-11143359] ｜ quote:"故障为随机独立注入，无空间相关性" ｜ confidence:全文级
- **credit assignment 证据没区分机制**：2306.01346 的跨层 Q 更新（用邻居 Q 表）、2402.17666 的包视角 SARS、10375570 的链路贡献分解（相关系数>0.98）是三种不同的多跳信用分配机制，但无任何工作对它们做受控比较——"分布式 MARL 为何能全局协调"在机制层面未被区分 ｜ from:[2306.01346, 2402.17666, ieee-10375570] ｜ quote:"从包视角构造经验缓解多跳 credit assignment 模糊" ｜ confidence:全文级
- **轻量统计基线逼近上限，RL 增量存疑处**：2601.08439 显示 GMM/EVT 1.6–3.5 s 采样即 AUPRC 0.95，任何用 RL 做时延预测/链路自适应的工作必须与该统计基线对比否则增量存疑（尚无 RL 工作做过此对比）｜ from:[2601.08439] ｜ quote:"统计基线已接近上限" ｜ confidence:全文级
- **摘要/标题级文献的覆盖空洞**：tail-132263（DRL 路由综述）、tail-102884（CGR 教程）、tail-67514-1_39（CGR 改进）、tail-sat.70043（path-based DRL）、tail-6864517（SDSN 控制器放置 Q-STGCN）五篇仅有摘要/标题，其主张无法进入本地图的证据链——CGR 传统路线 vs DRL 路线的系统性对比在本文献池内不完整 ｜ from:[tail-132263, tail-102884, tail-67514-1_39, tail-sat.70043, tail-6864517] ｜ quote:"摘要未披露" ｜ confidence:摘要级
