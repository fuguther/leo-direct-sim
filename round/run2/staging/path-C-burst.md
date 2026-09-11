# run2 · 路径C候选卡：同均值不同突发程度/持续时间/变化速度（burst 路径）

生成：run2 生成器（路径C），2026-09-10。语料基准：worktree topic-loop-20260910，Zotero 白名单 v4（111 篇索引全扫）。
研究范围锁定：低轨卫星网络中负载变化下强化学习路由如何保持到达率与端到端时延。本路径考察：平均流量相近但突发程度、持续时间、变化速度不同时，队列动态与策略反应速度的错配。

**一句话结论**：在已核对子集（8 篇原文 + 12 篇笔记）内，没有任何一篇 LEO 路由工作在「同均值」下扫描突发强度/持续时间/变化速度；最好的一篇（SaTE, SIGCOMM'25）也只做到 1 秒粒度泊松流到达加均值强度扫描，而 2026 年的 MARL 路由（Traffic-Aware MARL）甚至把负载建模为无时间过程的外生空间队列采样。排队论经典层（自相似 ON-OFF）早已证明同均值不同突发会加重时延尾与瞬态缓冲溢出，而经典 Q-routing 原文记录了「上行适应快、下行适应慢且不收敛」的迟滞——两者拼起来构成一个未被 LEO RL 路由检验的机制链。产出 3 张卡（突发时长×反应时间错配、负载过程训练覆盖盲区、瞬时快照信息可辨识性），全部给出半天到两天的廉价核验。

---

## 1. 阅读与检索诊断

### 精读（zotero_fulltext 全文或定向窗口抽取，共 10 次调用、去重 8 篇）

| # | 篇名 | itemKey | 精读方式 | 与本入口的关系 |
|---|---|---|---|---|
| 1 | Traffic-Aware MARL-Based Distributed Routing for LEO Satellite Network (OJVT 2026, [新]) | CMNCS52M | 全文（80k 字符）+定向窗口 | 负载=外生空间队列采样，无时间过程（承重） |
| 2 | Fast-Convergence RL for Routing in LEO (Sensors 2023, [新]) | 53HEEK33 | 全文（50k）+定向窗口 | 快收敛卖点；时延评估剔除初始瞬态（承重） |
| 3 | SaTE: Low-Latency Traffic Engineering for Satellite Networks (SIGCOMM'25, [新]) | JLF7IEBQ | 目录+关键词窗口 | 1s 粒度泊松流+均值强度扫描；亚秒突发仅作动机（承重） |
| 4 | PRIMAL: Asynchronous Risk-Aware MARL Packet Routing ([新]) | 39NJWBI7 | 目录+关键词窗口 | 平稳泊松 10k pkts/s；CVaR 尾部学在平稳过程上（承重） |
| 5 | Packet Routing in Dynamically Changing Networks (Boyan & Littman 1993) | 47J2H748 | 全文（17k）+窗口 | 负载上/下行适应不对称、迟滞（承重） |
| 6 | Traffic-Predictive Routing Strategy for Satellite Networks (Electronics 2024, [新]) | UF8IQTA2 | 目录+窗口 | 预测侧引用自相似/长相关，评估只扫包转发速率（旁证） |
| 7 | LEO satellite networking relaunched: Survey ([新]) | T9X6QCLL | 窗口抽取后判定弱相关，弃用 | — |
| 8 | Transmitting, Fast and Slow (MobiCom'23, [新]) | CTWVLBCY | 窗口抽取后判定弱相关（分钟粒度调度），弃用 | — |

### 浏览（未回原文，仅索引/题录/笔记线索）
- round/zotero/ZOTERO-INDEX.md 111 篇全索引扫描一遍，重点排查 [新] 批次中与本入口相关的：Traffic-Aware MARL（CMNCS52M）、SaTE（JLF7IEBQ）、Constrained DQN（ZIUBKVPZ）、DQN 负载均衡（XLRW7XXN）、On-Demand Laser ISL 路由（DVS8C3CC）、PRIMAL（39NJWBI7）、Fast-Convergence（53HEEK33）、Delayed-Feedback RL（QGAREQUM）、Asymmetric DQN PORL（I2WH9RRR）、队列增长率入奖励（EG9X569M）等。
- LITERATURE/SOURCES.csv 52 行全读（local_path 字段确认悬空，未尝试按它取文件）。
- round/knowledge/notes-neutral/ 共读取 12 篇：ZHOU-2026-DTAR、LOZANO-2025-CONTINUAL、CHOU-2026-STL、LIAQ-2026-QARR、DONG-2023-DQNLLRA、TALEB-2009-ELB、SONG-2014-TLR、IZHIKEVICH-2024、STARTCAP-2024、SORET-2024-QLEARN（另目录列表核对总数 41）。
- round/knowledge/NEUTRAL-KNOWLEDGE-VIEW.md 全读（Assumption Map 第 1 条「流量平稳或统计已知，突发性……被简化」与全文阅读证据表为本入口的先验坐标）。

### 检索渠道与查询词
- Undermind（工作区 eef99118-f623-4a47-a34a-05c6617b7ecb）：
  - 搜索 1（semantic）：「Traffic burstiness at fixed mean load / ON-OFF / self-similar / transient buffer overflow / steady-state metrics hide transient loss」→ 命中排队论经典（Sch99、Sch07、Cro97、Zan11）、卫星终端突发模型（Yux14）、TCP 微突发（Jia04）、LEO 拥塞控制评估（Maz25/Maz26/Bar23/Val25）。**全部为库外检索线索，未回原文**。
  - 搜索 2（semantic）：「routing adaptation timescale vs load dynamics mismatch / Q-routing hysteresis / delayed feedback RL」→ 命中 Miid97/Kum99（Dual/Confidence DRQ-routing）、Kav17（自适应学习率+路由记忆）、Wan26d DRL-Adapt、Cla26 MARL-Converge、Nia26（多流量场景经验分析）。**库外线索，未回原文**。
- 失败渠道（如实）：search_papers 首次调用因缺 workspace_id 且 search_type 取值非法被拒（未执行，修正后成功 2 次，未超 3 次配额）；get_orientation 调用报 binding 错误 1 次；arXiv API 与 web 搜索未启用（Undermind 已覆盖，60 分钟预算内不再扩渠）。

---

## 2. 候选卡

### 卡 C1：突发持续时间 × 策略/信息反应时间常数错配 → 瞬态窗口内到达率塌陷与时延尾

**1) 场景与可观察现象**
- 决策时刻：逐包到达事件（或每 T 时隙）。信息条件：本星队列 + 四邻居队列（快照或 hello 周期广播），目的地坐标。
- 负载变化形式：ON-OFF 突发源，**均值锁定**（峰值速率 × 占空比 = 常数），扫描突发持续时间 T_on ∈ {亚秒, 1s, 10s, 100s} × 峰值强度，可加空间相关维度（同区域多源同启/独立）。
- 可观察/测量：每个突发窗口 W 内的条件丢包率与到达率、条件时延尾（p99/p99.9）、突发起点到策略首次改路的反应时延 t_react、改路后流量目标集中度（herd 指数）、改路振荡次数；对照同 runs 的时间平均指标。

**2) 困难与原因假设**
- 【原文事实】Boyan & Littman（47J2H748）§3.1（pp.675–676）：仿真中上调负载时 Q-routing「快速适应」绕开新瓶颈；**负载降回后适应慢得多，且始终未收敛回最优最短路**；流量模式周期切换时每次切换后都有「短暂劣化期」。§3.2：原因是贪心更新只更新最优邻居的估计，过估计长期滞留 → 策略存在迟滞。这是「负载变化速度 × 策略更新时间常数」错配的最早已知原文记录。
- 【原文事实】SaTE（JLF7IEBQ）§1 与 §2.3：用户面流量存在亚秒级 dynamics（引 RedTE），拓扑最快 70 ms 变一次（§2.3.1），而传统 TE 计算需分钟级（§1、§2.3.2 工作流瓶颈）——计算/反应时间与波动时间尺度错配在 TE 层已被明确指出，但其解法是算得快（17 ms GNN），不是研究错配本身。
- 【原文事实】PRIMAL（39NJWBI7）§IV：训练与评估用平稳泊松过程（10,000 pkts/s、30 s epoch、三城市等概率）；其 CVaR0.25 约束学到的是该平稳过程的排队时延尾部。突发负载过程的尾部不在训练分布内，CVaR 在突发下是否仍控得住尾【待证】。
- 【笔记】CHOU-2026-STL（round/knowledge/notes-neutral/CHOU-2026-STL.md，深读级）：负载为 NHPP 周期 λ0(1+sin(2πt/T))——变化速度只覆盖确定性慢正弦；240 Mbps 下时延≈498 ms 排队主导，说明该合同已进入排队敏感区，但无随机突发维度。
- 【推演】当 T_on ≲ t_react（信息传播 + Q 更新 + 路由安装之和）：(a) 策略的反应到达时突发已结束，改路只剩路径抖动与重排序开销；(b) 多 agent 看到同一上升沿、同向动作 → herd 到同一替代路径造成二次拥塞；(c) 时间平均指标被无突发时段稀释，瞬态窗口内到达率塌陷在均值指标中不可见——即「稳态指标掩盖瞬态塌陷」。
- 【推演】下行迟滞（Boyan）意味着突发结束后策略回位慢于进入错位：占空比越高、突发越密，迟滞残留越可能把一次突发固化成持续次优路由【待证】。

**3) 拟议改动（先辨因再选法）**
- 辨因：策略无法区分「将持续的拥塞」与「即将过去的突发」，且改路动作无驻留约束 → 抖振/herd。
- 改动（决策结构+状态，不预设课程/门控网络）：状态扩为 s_i = (q_own, {q_j}, dest, Δq_τ = q(t) − q(t−τ), 突发龄计数器 t_since_onset)；动作 = 下一跳 + 改路后最小驻留时间 T_dwell（与观测突发时长先验同量级）。学习更新仍为 Bellman 形式，仅奖励扩展：
  Q_i(s,a) ← (1−α)Q_i(s,a) + α[ r − κ·1{窗口 W 内丢包} + γ·max_{a'} Q_j(s',a') ]，W 与 T_dwell 对齐。
- 作用机制：Δq 把「正在上升的队列」与「高而稳的队列」分开，避免把突发尾部当稳态拥堵永久改路（对应 Boyan 下行迟滞）；T_dwell 抑制 herd 抖振；κ 项把瞬态窗内到达率直接写进目标，补「均值奖励看不见瞬态」的缺口。
- 何时不奏效：(i) T_on ≫ t_react（有充足时间收敛，标准负载均衡已够用）；(ii) 缓冲大到突发期不丢包只有时延（κ 项无可罚对象，问题退化为时延削峰）；(iii) 突发空间高度分散，单星 Δq 信噪比过低；(iv) T_dwell 定错量级（短于突发→抖振依旧，长于负载周期→错失下一次突发窗口）。

**4) 初步近邻（Zotero 111 全索引已扫，含 [新]）**
- 53HEEK33 FRL-SR [新]：hello 邻居发现 + 在线微调（lr 0.2）以「快收敛」为卖点——是反应时间侧的最近邻，但无突发时长维度，且其时延对比明确剔除初始瞬态（见卡 C2）。
- 39NJWBI7 PRIMAL [新]：事件驱动异步半 MDP，时间语义最现实；差异=负载平稳、无突发自变量。
- 47J2H748 Boyan：迟滞现象与探索-稳定权衡的原始记录；差异=36 节点地面网、表格 Q。
- QGAREQUM（Boosting RL with Strongly Delayed Feedback Through Auxiliary Short Delays）[新]：学习侧延迟反馈的方法基础；差异=非路由专用、无 LEO 场景。
- JLF7IEBQ SaTE [新]：亚秒突发动机+快计算；差异=TE 流量分配层，非逐跳逐包路由。
- 库外线索（未回原文）：Wan26d DRL-Adapt、Cla26 MARL-Converge（收敛性优化）、Miid97/Kum99/Kav17（自适应 Q-routing 谱系）。**未发现任何工作把突发持续时间作为自变量扫描。**

**5) 简单替代猜想（百分比均为待验证假设；条件对齐=同均值、同缓冲、同信息与信令预算，不许弱化基线）**
- 同一策略只用混合 ON-OFF 负载重新训练（不改结构）：猜想吃掉 40–60% 瞬态收益。理由：大部分瞬态损失源于训练分布中没有上升沿/下降沿，见过即能反应；但 herd 与迟滞是机制性的，仍会残留。
- 带滞回+驻留时间的队列阈值规则（ELB/TLR 思路 + T_dwell）：50–70%。理由：C1 的改动本质上是把这条规则学习化；若规则版已够，学习只剩边际贡献。
- Dijkstra/ECMP + 大缓冲：30–50%。理由：短突发被缓冲吸收，损失只剩时延尾；但到达率差异被缓冲掩盖不等于不存在。
- 逐包 delivery-time 反馈（Boyan 式，让包带回实测时延）替代快照：60–80%。理由：直接测量 realized congestion，天然包含突发信息，无需预测。
- 在线微调（合理 lr 的 Q-table 微调，如 FRL-SR 式）：30–50%。理由：对 T_on > 收敛时间的突发有效，对亚秒突发基本无效。

**6) 立即淘汰条件**
- 同均值扫描中，固定策略（完全不改路）的瞬态窗口丢包 <1% 且条件时延尾与基线差 <5%（缓冲吸收了一切，错配无后果）。
- 实测 t_react ≪ 最短 T_on（策略总是来得及，错配不存在）。
- herd 效应测不出（改路后二次拥塞不出现，多 agent 同步性无后果）。
- 训练分布里加入突发后，平稳负载指标回退 >10% 且无法用随机化比例挽救。

**7) 下一项廉价核验（1.5 天）**
在现有仿真合同上加 ON-OFF 源（均值锁定 rate=duty×peak），T_on ∈ {0.2, 1, 10} s × duty ∈ {0.2, 0.5}，跑 Dijkstra、ELB、一个已训 Q/DQN 策略各 ≥5 seeds，输出三件东西：(a) 瞬态窗口条件指标 vs 全程时间平均指标的对比表（若差 ≥2×，即证实「稳态掩盖瞬态」）；(b) t_react 分布；(c) herd 指数与改路振荡计数。三者任一为零，本卡即触发淘汰线。

**8) 来源指针**
Boyan & Littman 47J2H748 §3–§3.2 pp.675–677；SaTE JLF7IEBQ §1、§2.3.1–2.3.2、§4、§5.4；PRIMAL 39NJWBI7 §I、§III、§IV（Poisson 10k/s、Dnorm=100 ms）；FRL-SR 53HEEK33 §3.2–3.3、§4 Table 3；CHOU-2026-STL 笔记（NHPP 合同、498 ms）；QGAREQUM 索引行（未读原文）；Undermind 搜索 1/2 记录（库外线索）。

---

### 卡 C2：负载过程是训练与评估的共享盲区——「同均值突发扫描协议」与外生队列模型的断裂

**1) 场景与可观察现象**
- 场景=训练/评估合同本身：决策时刻与信息条件沿用各文献设定；负载变化形式=负载过程族 𝒫(均值 μ, 突发度 CV, 突发时长 T_on, 占空比, 空间相关 ρ)。
- 可观察/测量：同一策略在 𝒫 网格上的到达率/时延响应面；「均值移位」与「突发度移位」两种扰动的敏感度对比；训练-评估过程错配度与性能退化的关系曲线。

**2) 困难与原因假设**
- 【原文事实】Traffic-Aware MARL（CMNCS52M）§III.B「Queue-Distribution Model」：卫星队列**不是由到达过程生成**，而是按三个空间分布模型采样（zone 模型中占用率 ~ N(μz, 0.1μz)）；§VI.A 明言「zone 模型不是时间相关的，时间观测特征已从状态中移除」；§V：转移函数与奖励被定义为确定性的。即 2026 年的 MARL 路由中，负载没有时间过程，只有空间快照——策略学到的映射是在无闭环反馈的队列场上拟合的，外推到真实突发负载【待证，且方向不明】。
- 【原文事实】FRL-SR（53HEEK33）§4 Table 3：负载=「offline/online training network load 3000」（初始包数），另一组 5000；时延类型=正弦；无随机到达过程参数。§4 且声明时延对比「取网络相对稳定后的时段，而非系统刚投入运行时」——瞬态窗被显式排除出评估。
- 【原文事实】SaTE（JLF7IEBQ）§4：最好情况是 1 秒间隔内 λ flows/s 的泊松流到达 + §5.4 satisfied demand vs traffic intensity 的**均值**扫描；亚秒级突发仅作动机引用（RedTE）。§4 明言「该过程引入流量生成的随机波动」但波动维度未被扫描。
- 【原文事实】PRIMAL（39NJWBI7）§IV：平稳泊松 10,000 pkts/s，单负载档（loaded scenario）。
- 【笔记】DTAR（notes-neutral/ZHOU-2026-DTAR.md，全文深读级）：surge = μ×5 局部热点，flow 级 3 flows/步、无排队建模；且 NEUTRAL-KNOWLEDGE-VIEW 证据表记录其「normal、surge、fault 场景使用不同指标展示收益」——突发场景存在但指标口径与正常场景不可比。
- 【笔记】CONTINUAL：默认负载 ℓ=1 一档 + 中载 0.5；QARR：200 站/1584 星接入极宽松，流量=均匀/人口分布背景流量；DONG-2023：ISL 时延/带宽随机生成、70 条并发流。
- 【推演】汇总：核对子集内**零篇**同均值扫描突发强度/时长/速度；负载维度普遍只有「均值档位」（1 档或 2–3 档）或外生静态队列。因此「负载变化→到达率/时延」这条链上的突发性维度是完全未测自由度；训练覆盖里没有任何上升沿/下降沿样本，策略对突发性的行为（保守/过敏/herd）不可预测【待证】。
- 【推演】外生队列模型（CMNCS52M 类）还有一层断裂：队列不是策略行为的果，策略无法从奖励中学到「我改路 → 队列变化 → 观测变化」的闭环；在闭环突发场景下，这类策略的失误模式（如正反馈聚集）在训练分布中从未出现【待证】。

**3) 拟议改动（先辨因）**
- 辨因：不是网络结构问题，是**训练分布与测量协议问题**——负载过程从未被参数化，突发维度从未进入训练与报告。
- 改动一（测量协议）：同均值突发扫描标准——对每个 μ，在 (CV × T_on × ρ) 网格上评估，报告 per-process 曲线与「过程敏感度」（响应面曲率），禁止只报单点或只报均值移位。
- 改动二（训练覆盖）：域随机化——训练目标 J(θ) = E_{P∼𝒫}[ E Σ r ]，𝒫 为过程族上的分布（可先均匀，后按实测校准）；不设课程。
- 改动三（可辨识性，联动卡 C3）：状态从单点 q 扩为 (q, Δq_τ, EWMA_τ(q)) 三通道——外生静态队列模型下这三者退化为常数，恰好使「模型是否真的有时间信息」变成可检验量。
- 何时不奏效：(i) 实测 LEO 流量被证明近似泊松且缓冲充足（突发维度无现实意义，卡片降级为审计结论）；(ii) 域随机化使平稳负载性能回退 >10%（覆盖-性能权衡不可接受）；(iii) 平台仿真合同不支持包级到达过程（无法实施）。

**4) 初步近邻（Zotero 111 已扫）**
- 近邻即被审计对象本身：CMNCS52M、JLF7IEBQ、39NJWBI7、53HEEK33、UF8IQTA2（预测侧引用自相似/长相关，评估只扫包转发速率——动机与评估脱节的直接样本）。
- GPDPLJNG（Multi-Commodity Flow Routing DRL）[新]：以流量矩阵为中心的 DRL 路由，TM 生成方式是同类审计对象（未读原文，标待查）。
- 5N5LQPPP SDDRL-SR [新]、XLRW7XXN DQN-LB [新]、ZIUBKVPZ Constrained DQN [新]：题录与索引层判断为同合同家族，未读原文，列入审计清单。
- 库外线索：Nia26「ML for Network Optimization: empirical performance analysis across diverse traffic scenarios」(2026)——标题最接近「多负载过程评估」，须查其是否含突发维度【待证】；Sch99/Sch07/Cro97/Zan11 提供同均值突发效应的排队论先验。

**5) 简单替代猜想（均为待验证假设）**
- 只做混合负载训练、不做扫描协议：30–50%。理由：增益有了但归因不了，审稿与机理链都立不住。
- 只加 EWMA/Δq 特征、训练分布不变：20–40%。理由：信息有了但策略从未被要求用它。
- 把现有论文的负载加倍复跑（均值移位）：0–20%。理由：均值移位 ≠ 突发度变化，两个轴正交。
- 什么都不做、只报现有单点结果：0%。这是现状。

**6) 立即淘汰条件**
- 审计（≥20 篇）发现 ≥3 篇已做同均值突发/方差扫描，且结论一致为「策略排序对突发度不敏感」→ 本卡问题不存在，只保留审计附录。
- 本平台无法实现包级到达过程或同均值控制。
- 同均值 ON-OFF 对照中所有策略（含 Dijkstra）性能变化 <3%。

**7) 下一项廉价核验（1 天）**
(a) 审计表：对 20 篇（Zotero 内优先 [新]）逐篇提取 traffic-model 段落，四列记录：到达模型（CBR/泊松/NHPP/外生队列/无到达过程）/ 时间粒度 / 是否扫均值 / 是否扫突发或方差；(b) 对照实验：一个已训策略在 CBR vs ON-OFF（同均值同缓冲）下的到达率/时延差。两者合计一天，产出即可支撑或击毙本卡。

**8) 来源指针**
CMNCS52M §III.B、§V、§VI.A；53HEEK33 §4 Table 3 与时延对比声明；JLF7IEBQ §4、§5.4；39NJWBI7 §IV；UF8IQTA2 §2（自相似引用）、§6.2.1；DTAR/CONTINUAL/QARR/DONG 笔记；NEUTRAL-KNOWLEDGE-VIEW Assumption Map 行 1 与证据表 ZHOU-2026-DTAR 行；Undermind 搜索 1 命中清单（Sch99/Sch07/Cro97/Zan11/Yux14/Nia26）。

---

### 卡 C3：突发负载下瞬时队列快照的信息可辨识性——陈旧/偏样本观测系统性误导逐跳策略

**1) 场景与可观察现象**
- 决策时刻：逐包/逐时隙。信息条件=决策时可得的邻居队列快照 q_j(t−δ)，δ ∈ [0, hello 周期]；突发负载下快照与「下一 τ 秒实际拥塞」的相关性随 duty、δ、T_on 变化。
- 可观察/测量：以决策时信息为条件的下一跳实际时延分布；人工陈旧化（把观测延迟 δ、量化、置零）下的性能退化曲线；误改路率（突发未到/已走仍改路）与漏改路率（突发中未改）；平稳 vs 突发负载两条退化曲线的形状差。

**2) 困难与原因假设**
- 【原文事实】Traffic-Aware MARL（CMNCS52M）§III.A：假设卫星「知道四邻居的当前队列长度」——零延迟、零噪声理想信息；全文无信息年龄语义。
- 【笔记】CONTINUAL 深读（notes-neutral/LOZANO-2025-CONTINUAL.md）：「邻居拥塞 C_j,k 假设每步即时可得，Q 函数未建模该信息的传播年龄/反馈延迟」——状态无年龄语义；【笔记】QARR：「状态全部取瞬时值，无信息年龄维度」。
- 【笔记】ELB/TLR（notes-neutral/TALEB-2009-ELB.md、SONG-2014-TLR.md）：队列占用经信令传播必然陈旧，**陈旧度代价从未被量化**（该笔记自身标注此点含推测成分，引用前须回原文核对信令协议——标【笔记+待证】）。
- 【原文事实】Boyan（47J2H748）§3.1–3.2：即便用 delivery-time 反馈（信息本身最真实），贪心更新仍造成迟滞——说明时间错配有两条腿：**信息年龄**与**更新惯性**，本卡只攻前者，C1 攻后者。
- 【推演】突发下快照是偏样本：占空比低时决策时刻多半看到 q≈0（突发未到）或 q 满（峰已过），快照与未来拥塞的相关性系统性下降；以平稳负载训练出的「q 大→绕行」映射会误触发（突发已走仍在绕）或漏触发（上升沿未反映在快照）；多 agent 读同一陈旧快照同步动作产生相关错误。到达率损失的两条通路：误改路（路径变长、抖动、二次拥塞）与漏改路（突发窗内直接丢包）。
- 【推演】ELB/TLR 类信令的陈旧量级可估：单跳传播 ~几 ms、hello 周期 ~百 ms 到秒级，对 T_on<1s 的突发，快照到达时突发已过半——错配窗口恰好落在真实流量动态（Izhikevich 实测的 15s 级持续尖峰、StarTCP 的 15s 切换中断）与亚秒应用突发之间【量级估算=推演，待实测】。

**3) 拟议改动（信息可辨识性三件套，皆为一行式改动）**
- (i) 观测加信息年龄戳 a_j = t − t_j^{last}（hello 到达时间差）；(ii) 邻居队列以 EWMA_τ(q) 替代瞬时值，τ 与 hello 周期同量级；(iii) 学习更新按年龄加权：Q_i ← (1−α_i)Q_i + α_i[r + γ max_{a'} Q_j(s',a')]，α_i = α0·f(a_j)，f 随 a_j 单调递减（陈旧 bootstrap 少信）。
- 作用机制：直接作用于「快照≠未来拥塞」这条因果链——让策略对新鲜信息敏感受、对陈旧信息保守，并以 EWMA 恢复快照在突发下丢失的时间结构。
- 何时不奏效：(i) δ ≪ T_on（信息本就新鲜，年龄戳无增益）；(ii) 信令预算充足——直接缩短 hello 周期即可，无需学习侧改动（此情形下本卡收益被工程手段吃掉）；(iii) EWMA 引入上升沿滞后反而更晚改路（τ 取大了；需 τ 扫描，本身也是核验内容）；(iv) 突发空间上极其分散，单星视角的任何局部统计量都无法预测。

**4) 初步近邻（Zotero 111 已扫）**
- WEIL-2024-RMP（索引 #97 附近，题录 LOZANO 同族之前身）：循环消息传递缓解陈旧观测——通用图上最直接的「陈旧观测缓解」先例（笔记层，未回原文）。
- I2WH9RRR Asymmetric DQN for Partially Observable RL [新]：部分观测的结构化处理方法基础（未读原文）。
- EG9X569M Chu-2023 RRSDRL（SOURCES.csv 全文核对级）：reward = 距离 + next-hop AoI + **队列增长率**——「把时间性放进目标」的最近先例；差异=其 AoI 是数据包年龄语义，且无突发扫描。
- TALEB-2009-ELB、SONG-2014-TLR：信令陈旧的启发式鼻祖（笔记层）。
- Kum99 Confidence-based DRQ-Routing（库外线索，未回原文）：给 Q 估计加置信度——与年龄戳同构。
- 42E4NAQU QARR [新]：队列感知状态（瞬时值），无年龄维度（笔记层确认）——近邻反例。

**5) 简单替代猜想（待验证假设；条件对齐=同信令预算）**
- 直接缩短 hello 周期（频率换新鲜度）：同信令预算对齐后若不允许加频，此路不通；若允许，猜想吃掉 60–80%——所以对比必须在「同信令预算」下做，否则基线被削弱。
- delivery-time 反馈（Boyan 式）：50–70%。理由：实测拥塞天然含突发信息，不依赖快照新鲜度。
- 只加大缓冲不改信息：20–40%。理由：把到达率问题转化为时延尾问题。
- 不做任何信息侧改动、仅在动作侧加随机化（ε 提高）：10–20%。理由：缓解同步错误但不解决偏样本。

**6) 立即淘汰条件**
- 人工陈旧化实验中，δ 从 0 扫到 2×hello 周期，性能退化 <3%（信息年龄不重要）。
- 平稳与突发负载下退化曲线形状无显著差异（突发性没有放大陈旧问题——则本卡被 C1 吸收）。
- EWMA/年龄戳在平稳负载下造成 >5% 回退且 τ 扫描无法挽救。

**7) 下一项廉价核验（1 天）**
在现有已训策略上把邻居队列观测人为延迟 δ ∈ {0, 0.5, 1, 2}×hello 周期（纯评估侧干预，不动训练），平稳泊松与同均值 ON-OFF 各跑一条性能-陈旧度曲线；若突发曲线显著更陡（交互效应显著），本卡成立且自动给出 EWMA/τ 的设计窗口。半天搭干预钩子，半天跑数。

**8) 来源指针**
CMNCS52M §III.A；Boyan 47J2H748 §3.1–3.2；CONTINUAL/QARR/ELB/TLR 笔记（notes-neutral 对应文件）；EG9X569M 经 SOURCES.csv（fulltext_checked 行）；WEIL-2024-RMP 笔记与 NEUTRAL-KNOWLEDGE-VIEW 证据表行；Izhikevich/StarTCP 笔记（真实尖峰量级旁证）；Undermind 搜索 2（Kum99/Miid97/Kav17，库外）。

---

## 3. 诚实放弃线（考虑过但放弃的方向）

1. **拥塞控制微观突发（TCP/BBR micro-burst, Jia04、9KZDXPKC）与路由联动**——跨层问题，超出「负载变化→路由」范围，且库内已有 CC-路由专门线（How to Route CUBIC and BBR Packets in Space）。
2. **切换导致的容量侧突发（StarTCP 的 15s 周期中断、Izhikevich 15s 尖峰）作为主变量**——这是容量/可达性扰动，属其他路径；本卡只在 C3 用作「真实动态时间量级」旁证。
3. **把路由信息年龄形式化为 AoI 并以 AoI 为优化目标**——目标函数从到达率/时延偏移到信息新鲜度，LUR/RAoI 谱系已有专门工作；只取「年龄语义」作为 C3 的一个特征，不成卡。
4. **LLM/自动化奖励设计解决突发奖励整定（GPLEP83L 等）**——先辨因后选法原则下，奖励整定不是本入口的因；且机制归因不清。
5. **非平稳多智能体学习的收敛性理论分析**——理论门槛高，60 分钟预算内无法形成可核验命题；Boyan 的经验迟滞已足够作为现象锚点。
6. **「稳态指标掩盖瞬态」单独成评估方法学卡**——已并入 C1 的观察设计（第 1/7 节）；若 C1 被淘汰，该观察可降级为审计附录独立存活。

---

## 4. 防火墙声明

- **读过的白名单文件**：round/zotero/ZOTERO-INDEX.md（全）；LITERATURE/SOURCES.csv（全 52 行）；round/knowledge/NEUTRAL-KNOWLEDGE-VIEW.md（全）；round/knowledge/notes-neutral/ 下 12 个 .md（目录列表 + 10 篇内容）；round/zotero/ 目录名列表（仅文件名，未打开 index-raw.json / raw-*.json / unmatched.json）。
- **zotero_fulltext 调用**：10 次（CMNCS52M×2、53HEEK33×2、JLF7IEBQ、39NJWBI7、47J2H748、UF8IQTA2、T9X6QCLL、CTWVLBCY），去重 8 篇；zotero_item 未调用（索引已含元数据）。
- **Undermind**：get_orientation 1 次（binding 错误，失败）；list_workspaces 1 次；search_papers 成功 2 次（semantic，工作区 eef99118-f623-4a47-a34a-05c6617b7ecb），另 1 次因参数缺失被拒（未执行）。未用 launch_deep_search、read_pdfs（0 次）。arXiv API、web 搜索未使用。
- **黑名单接触**：无。未对 LITERATURE/notes/raw/**、LITERATURE/KNOWLEDGE-MAP.md、ANALYSIS/**、NOTES.md、round/run1/**、round/CANDIDATE-LEDGER.csv、round/reviews/**、round/history/**、round/ROUND-LOG.md、round/knowledge/notes-neutral-manifest.json、round/knowledge/P0-SEMANTIC-SPOTCHECK.md、round/rules/QUALITY-GATE-R2.md 及任何旧候选台账/评审文件执行读取或列目录；round/run2/ 仅列顶层目录名（dryrun/feedback/gates/staging，非黑名单）。
- **本文件为唯一产出**：round/run2/staging/path-C-burst.md。
