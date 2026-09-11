# path-C 候选研究问题草图：方法迁移与假设检查（第1轮 staging）

> 生成器：path-C 隔离子代理（防锚定上下文）。知识来源仅限白名单 v2：NEUTRAL-KNOWLEDGE-VIEW.md、SOURCES.csv、
> notes/raw/*.md（14篇）、2篇原文回核（ar5iv / arXiv HTML）、Undermind 2次题录级检索（workspace eef99118）。
> 未读 out/、round/（除白名单 knowledge 文件）、LITERATURE/notes/ 禁读件、related-work-notes/（SOURCES.csv 的
> local_path 指向处一律未跟随）。Undermind 题录未回原文核对前一律标【待证·仅题录】。

## 诊断记录（阅读分配）
- 浏览 14/14（上限内）：GRAPHPR、POMAP、WEIL、LOZANO、PRIMAL、TMIX、SORET、GROUTING、RAOI、CHU、TALEB、SONG、DONG、CMADR——全部有 raw 笔记，**实际读过的论文中无笔记占比 0/14=0%**。
- 精读 2/5（本回合本人回原文）：WEIL arXiv:2402.05027（ar5iv 表4+§5.2 正文原句）、PRIMAL arXiv:2510.27506（HTML 表I+§III 目录与定义）。另有 4 篇（WEIL/LOZANO/PRIMAL/DONG）依赖笔记内既有全文深读记录，引用处标注其定位。
- Undermind：2次成功（backpressure/Lyapunov→LEO；陈旧状态/belief 路由），另2次参数错误未执行。
- 主线结论：Lyapunov/backpressure 与 safe-RL(CVaR) 的"裸迁移"均已被完成（见文末放弃清单）；存活候选都在迁移后剩下的缝里。

---

## 卡A Lyapunov/backpressure 迁移检查后的残差：陈旧队列观测下的 drift 计算

**迁移来源**：backpressure/Lyapunov drift-plus-penalty（吞吐最优在线路由的经典谱系）。

1) **场景与可观察现象**：卫星 s 在包到达/转发完成时刻 t 选下一跳。可用信息：本地队列 q_s(t)（实时）、邻居队列广播值 q̂_j(t−a_j)（年龄 a_j=信令间隔+传播+排队，ELB/TLR 式信令）、星历可预计算的时隙化链路容量 c_ij(t)。日志可观察：决策时刻 q̂ 与真实 q 的误差分布、每个 drift 项符号与随后队列实际变化的相关性、随信令周期 T_ctrl 扫描的到达率/时延曲线。

2) **困难与原因假设**：
- 【待证·仅题录】Nie25「Lyapunov Optimization Aided DRL for LEO routing」、Hua24/Hua25b「Robust Lyapunov…LEO」、Yin25b「GAT-Based Backpressure Routing LEO」、Han23、Kon18、Den26、Che16c 已把该范式迁入 LEO——裸迁移不成立为选题。注意：SOURCES L43 的 WCNC-2025 题名与 Nie25 存在版本差异，可能同篇或姊妹篇，未核实。
- 【原文事实·笔记级，摘要未核实】TALEB-2009（IEEE/ACM ToN 17(1)）ELB 用显式队列信令做负载均衡；SONG-2014（IEEE TWC 13(6)）TLR 用队列红绿灯+中间节点实时改道。两者信令值均为"过去式"，原文未量化陈旧代价。
- 【推演】上述 LEO 迁移工作沿用两个未检验前提：①drift 用"当前"队列差计算——信令年龄使 q̂ 系统性滞后，符号错判率随负载上升；②容量按平均速率——时隙化后容量是星历可预测的时间索引量，且信令与数据在同一拥塞 ISL 争容量（采样成本内生化）。
- 竞争解释：学习/解析方法的增益全部来自静态热点绕开（ELB/TLR 固定阈值即可），drift 结构与年龄感知本身无增益。

3) **拟议改动**：改奖励+观测。以 drift-plus-penalty 项作 potential-based shaping（保持最优策略集不变），drift 用带年龄折扣的 q̂ 计算，观测显式含年龄字段 a_j；对照同信息权限的 ELB 阈值式。机制：年龄大→drift 符号错判→绕行决策质量降→到达率降/时延升；年龄感知塑形应在该区间保住收益。

4) **初步近邻**：Nie25、Hua25b、Yin25b、Han23、Kon18、Den26（均【待证·仅题录】）；Fis05/Kam22/Yin11（地面网陈旧状态理论【待证·仅题录】）；LI-2025-POMAP（排队模型入环境但无信息年龄，S/A/R 付费墙未核）。

5) **简单替代**：ELB/TLR 固定阈值在中低负载可拿 60–80% 增益【推演】；DQN+邻居队列（DONG 式）再拿一部分；年龄感知塑形的净增益可能只剩重负载+大 T_ctrl 区间——若该区间在真实参数下不出现，卡片死。

6) **立即淘汰**：①核读 Nie25/Hua25b 发现其 drift 已建模陈旧观测或显式信令开销；②T_ctrl 注入扫描显示到达率对年龄平坦（各负载点差 <1%）。

7) **下一项廉价核验**：取 Nie25 或 Hua25b 全文（Undermind 题录显示 PDF ✓）核 drift 的信息假设；leo_sim 做 ELB 信令年龄注入扫描（见卡D核验，两者共用实验）。

8) **来源指针**：SOURCES.csv L36/L37/L43；notes/raw/TALEB-2009-ELB.md、SONG-2014-TLR.md、LI-2025-POMAP.md、DONG-2023-DQNLLRA.md；Undermind U1 题录（Nie25、Hua25b、Yin25b、Han23、Kon18、Den26）。

---

## 卡B 跨跳信用分配：信用随包走（CTDE 价值分解在逐包路由的断点检查）

**迁移来源**：CTDE/价值分解（QMIX/MAPPO 谱系）与多智能体信用分配。

1) **场景与可观察现象**：包 p 依次经过卫星 s1…sk，每跳由该星 agent 决定；终态（送达/丢弃/TTL超时）k 跳后才确定，只有目的端/丢弃点观测到。信息条件：各跳 agent 只有本地+一跳邻居观测（含陈旧队列），无跨 agent 在线通信（PRIMAL 式）或仅训练期共享（CTDE 式）。日志：包级决策轨迹（hop、agent、action、观测年龄）+终态；可按"哪一跳进入死胡同/环"分解失败原因。

2) **困难与原因假设**：
- 【原文事实】（本回合回原文：ar5iv 2402.05027 表4）无带宽限制下 Ours*(action masking) reward 1.74±0.00/吞吐 3.49，仍逊于 ShortestPath 1.77±0.00/3.54；正文原句 "Surprisingly, the effect of communication is very small"（§5.2）。→ 邻居消息（隐式协作）在最松合同下端到端无收益。
- 【原文事实】（本回合回原文：arXiv 2510.27506 表I）MADQN/PRIMAL-Avg/PRIMAL-CVaR 丢包均 0.00%，SPF 84.8%；笔记深读记录其"多智能体"实为各卫星独立学习、无 agent 间通信。
- 【原文事实·摘要级笔记，S/A/R 未核实】CHEN-2025-TMIX（IEEE IoT-J 12(11)）用 Transformer-MIX 聚合联合动作值；LI-2025-POMAP（IEEE IoT-J 12(22)）用 MAPPO。
- 【推演】价值分解假设断在两点：(a) 路由回报由*序列*耦合决策产生——上游动作改变下游队列状态，贡献跨时间而非跨团队；(b) 参与一个包决策的 agent 集合随拓扑运动逐包重组，mixing 网络无法绑定固定成员。
- 竞争解释：PRIMAL 式独立学习+局部奖励在其合同下已 0% 丢包——信用分配可能根本不是瓶颈，瓶颈是合同设计让"到达率"无差异空间。

3) **拟议改动**：改更新方式（不动网络结构）：包携带经历账本（每跳 action/obs/时刻），终态触发按路径回溯的延迟回报分配（eligibility 随跳龄/时延衰减），替代逐跳即时 TD 或团队 mixing。机制假设：失败包责任可定位到具体跳（如进入已拥塞下游），路径级信用把到达率变成可归因的每跳期望改善，直接优化到达率而非其代理量。

4) **初步近邻**：TMIX（LEO+CTDE 已存在，但价值分解≠路径信用）；PRIMAL（独立学习对照）；SORET-2024（ICMLCN，表格 Q-routing 的 per-hop bootstrap 天然逐跳信用）。未核：LEO 逐包 DRL 路由中是否有人做过 path/trajectory-level credit assignment。

5) **简单替代**：per-hop 分段加权奖励（DONG 式）≈隐式分配，可能解决约 70%【推演】；"终态回报均摊路径每跳"实现最简，可能已捕获大部分信号；CTDE 结构在无差异空间合同里无增益。

6) **立即淘汰**：同合同 A/B 中 per-hop TD 与路径回溯信用的到达率/时延差 <2%（seed≥5）；或先复现出"学习算法丢包全为 0%"的 PRIMAL 现象——说明合同无差异空间，卡片死。

7) **下一项廉价核验**：leo_sim 3–5 跳 toy 拓扑跑 per-hop vs path-credit 两版 DQN，看失败包归因直方图是否可分。

8) **来源指针**：notes/raw/WEIL-2024-RMP.md（+本回合回核）、HE-2025-PRIMAL.md（+回核）、CHEN-2025-TMIX.md、LI-2025-POMAP.md、SORET-2024-QLEARN.md、DONG-2023-DQNLLRA.md；SOURCES.csv L10/L13/L17/L23/L29。

---

## 卡C 星历先验+学习残差：把"可算的"从学习目标里剥出去（规划+残差迁移检查）

**迁移来源**：planning + learned residual policy（地面网络/控制谱系）。

1) **场景与可观察现象**：决策时刻=包到达或链路时隙切换。信息条件分两层：未来 W 时隙 ISL 通断/容量由星历预计算（时间扩展图，确定性）；队列/突发负载不可预测、只能陈旧观测。日志记录：策略输出对计划路径的分歧率、分歧跳位置、分歧后的时延/到达增益，以及残差动作被 mask 掉的比例。

2) **困难与原因假设**：
- 【原文事实·笔记深读级】LOZANO-2025（IEEE TCOM 73(10)，arXiv:2405.12308）：每星 DQN+一跳拥塞编码（28 字段），低拥塞追平 genie 最短路（50th 差 1.7ms），策略随轨道过时需 continual learning 对齐——学习在"可计算部分"上重复消耗样本。
- 【原文事实·摘要级笔记】WANG-2021-GRouting（HotICN）动作限 k-最短路径候选；XIANG-2025-MATGCIR 用最短路模仿预训练（SOURCES，原文未读）；BlockFlex 用鲁棒虚拟覆盖（SOURCES L52，未读）。
- 【推演】地面"规划+残差"假设规划器输出受控基线、残差在静态图上修正；LEO 断点：拓扑运动外生可预测（不该学），残差动作必须在时间扩展图上保证无环与 TTL 可行——残差空间要由星历约束生成（action masking 由星历算出，而非学习）。
- 竞争解释：时间扩展图最短路+队列阈值改道（TLR 式）已达上限，残差 RL 只加噪声。

3) **拟议改动**：改动作空间+学习目标：动作=星历生成的计划路径邻域内选下一跳（masking 排除环路/TTL 超限）；critic 只学排队+丢弃残差回报（传播时延解析扣除）。机制：学习容量集中到唯一不可预测分量（队列），到达率改善应集中在突发负载场景，训练样本需求随状态空间缩小下降。

4) **初步近邻**：GRouting（静态 k-SP 候选先行）；MATGCIR（模仿加速）；Zhou-2026-DTAR（域级动作）；BlockFlex；Undermind U1 [Kim26b]（题录【待证】）。未核：显式"contact-plan 上的 residual RL"是否已存在。

5) **简单替代**：k-SP 候选+队列阈值重选覆盖突发场景大部分【推演，需负载扫描验证】；纯 RL 全状态版本在低负载=SP，无增益空间。

6) **立即淘汰**：①检索发现"时间扩展图+residual RL"已有论文；②TE+ELB 组合在突发合同下达到 RL 残差 ≥95% 增益；③残差动作被选中率趋近 0。

7) **下一项廉价核验**：用 LOZANO 公开模拟器（SatCom-TELMA/MA-DRL_Routing_Simulator，笔记已核存在）统计 DRL 决策与时间扩展图最短路的分歧率，及分歧事件中学习正确/错误的比例。

8) **来源指针**：notes/raw/LOZANO-2025-CONTINUAL.md、WANG-2021-GROUTING.md；SOURCES.csv L19/L24/L28/L52。

---

## 卡D 路由状态信息的年龄-价值曲线：AoI 谱系换观测对象后的闭环断点

**迁移来源**：AoI 调度/采样理论（单监视器谱系）+ 陈旧信息路由（地面网）。

1) **场景与可观察现象**：卫星 s 维护邻居队列/链路状态的 belief（本地估计器），每个转发时刻用 belief 决策；可选决策"何时广播自己的状态摘要/轮询哪个邻居"——信令动作与转发共享 ISL 容量。日志：每条决策所用状态值的年龄 a、belief 误差 |q̂−q|、随信令策略（固定周期/阈值触发/学习调度）变化的到达率与时延曲线。

2) **困难与原因假设**：
- 【原文事实·笔记级】AoI 谱系优化对象是"被传输数据的新鲜度"：Yates-2021（arXiv:2111.09217，多跳无线数据 AoI）、Kadirvel-2020（arXiv:2007.05449，LEO 多跳更新 AoI）、GAO-2026-RAoI（IEEE/ACM ToN，被转发数据年龄）、CHU-2023（Electronics Letters，奖励含下一跳数据 AoI）——四篇均非"路由状态自身的年龄"。
- 【待证·仅题录】地面网早已研究陈旧状态路由：Fis05、Yin11、Kam22、Ari00、Nor09、Ded19——"陈旧信息有害"不是新命题。
- 【原文事实】（本回合回原文）WEIL 表4：无带宽限制下通信效应很小、带宽受限下学习反超 SP——"新鲜信息价值"在资源宽松时≈0、在资源紧张时出现，这给出可检验的机制预测。
- 【推演】LEO 断点：①信令与数据在同一 ISL 争容量（采样成本内生于被优化系统），地面 stale-info 文献多假设独立控制信道；②拓扑分量可由星历预测，真正需要"保鲜"的只有队列分量——观测维度可分是 LEO 特有结构；③PRIMAL 异步事件驱动天然产生年龄但无度量（笔记深读级）。
- 竞争解释：真实 ISL 容量（Gbps 级）下信令开销可忽略，固定周期+阈值触发已覆盖，学习调度无净增益空间。

3) **拟议改动**：改观测（+可选扩动作）：belief 端用年龄折扣估计器维护邻居队列，状态显式含年龄；实验主干是"年龄注入扫描"（把信令年龄当受控变量）而非先上学习调度。机制假设：到达率/时延对年龄的敏感度随负载出现拐点；若拐点存在，"多高的信令频率值得买"成为可计算权衡，学习调度才有净增益可言。

4) **初步近邻**：Fis05/Kam22/Yin11（地面网理论【待证·仅题录】）；WEIL（隐式 T_ctrl=1 步）；LOZANO（邻居拥塞信息假设每步即时可得——笔记深读级）；PRIMAL（异步无度量）。未核：LEO 场景的"状态年龄"直接研究。

5) **简单替代**：T_ctrl 网格扫描取最优（非学习）；阈值触发信令（TLR/ELB 式）——两者可能覆盖 80%+【推演】。

6) **立即淘汰**：①年龄注入扫描全负载段平坦（无拐点）→"状态年龄有价值"证伪；②地面网结果（Yin11/Fis05）给出与 LEO 同构的结论且 LEO 信令成本可忽略。

7) **下一项廉价核验**：leo_sim 给 ELB 式信令加人工陈旧注入，2–3 个负载点 × 5 个 T_ctrl 画到达率/时延曲线（与卡A核验共用）。

8) **来源指针**：notes/raw/ARXIV-2111.09217.md、ARXIV-2007.05449.md、GAO-2026-RAOI.md、CHU-2023-RRSDRL.md、TALEB-2009-ELB.md、WEIL-2024-RMP.md、LOZANO-2025-CONTINUAL.md、HE-2025-PRIMAL.md；SOURCES.csv L9/L40/L41；Undermind U2 题录。

---

## 已检查并放弃的迁移方向（charter 要求如实记录）

1. **backpressure/Lyapunov→LEO 裸迁移**：题录级证据（Nie25、Hua24/25b、Yin25b、Han23、Kon18、Den26、Che16c）显示已完成多次，Nie25 已是"Lyapunov-aided DRL"——放弃裸迁移，仅保留卡A的陈旧观测残差，其生死系于对 Nie25/Hua25b 的一次核读。【待证·仅题录】
2. **safe RL/CVaR→LEO**：PRIMAL（本回合回原文核实）用 IQN 分布 critic + primal-dual CVaR 约束已完成；其表I学习算法丢包全 0.00% 还提示"到达率指标在该合同无差异空间"——放弃。
3. **offline RL→LEO 路由**：本轮未检索到直接证据，也未证伪——未核，留待后续轮。
4. **belief-state/recurrent 裸迁移**：Weil 循环消息传递是"用记忆换新鲜度"的通用机制，无带宽限制下端到端无增益（回原文核实）——单靠它不构成 LEO 问题；并入卡D年龄视角。

## 最不确定的三点

1. **"差异空间"前提（全部卡共同）**：PRIMAL 表I学习算法丢包全 0.00%——若真实参数（Gbps 级 ISL）下到达率对策略普遍不敏感，卡A/B 的到达率主张全部失效；第一淘汰条件优先于一切精化。
2. **Undermind 题录均未回原文**：Nie25/Hua25b/Yin25b/Kam22/Fis05/Yin11 的真实内容可能推翻或覆盖卡A/D 的残差空间（每篇核读约半天）。
3. **卡B 信用分配是否"真问题"**：独立学习（PRIMAL）+ per-hop TD（Q-routing 谱系）可能已把它解决到无可测增益，目前无直接反证也无直接支持。

## 撞见声明

本回合仅在白名单入口内活动；NEUTRAL-KNOWLEDGE-VIEW 为候选无关切片；staging 目录现存其他 path 产物（path-A-scenario.md）未读。未撞见任何旧候选/旧实验/旧排序段落。
