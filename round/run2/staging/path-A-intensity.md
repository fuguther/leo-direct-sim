# run2 · 路径A（流量整体强度变化）候选卡生成

- 生成者：run2 路径A 生成器（子代理，z-ai/glm-5.3-flash）
- 日期：2026-09-10 · 工作树：`.worktrees/topic-loop-20260910`
- 已锁定研究范围：低轨卫星网络中，负载变化下强化学习路由如何保持良好的到达率和端到端时延
- 本路径入口：流量整体强度变化——策略在某负载强度训练、部署到另一强度时到达率/时延为何退化（或文献声称不退化，核查其证据合同）；训练负载与评估负载的实际设置；强度变化改变学习问题的什么；塌陷是渐变还是突变、有无前兆
- 结论预告：3 张候选卡 + 6 条放弃线。核心发现：**库内 11 篇全文级抽查中，没有一篇报告"固定策略在强度 X 训练、在强度 Y≠X 评估"的直接实验**；监督学习一侧（SaTE）反而是唯一显式混强度训练并做 unseen 评估的对等物。

---

## 1. 阅读与检索诊断

### 1.1 篇目（浏览/精读清单）

浏览（标题级）：`round/zotero/ZOTERO-INDEX.md` 111 篇全部过目，按"负载/流量/拥塞/队列"轴选出 12 篇候选，其中 [新] 标记 8 篇优先。

全文级阅读（zotero_fulltext + 程序化关键词窗口提取，共 11 个不同 key、17 次调用；非逐行精读，提取窗口 ±170–260 字符）：

| itemKey | 篇名（简称） | 阅读焦点 |
|---|---|---|
| CMNCS52M | Traffic-Aware MARL Routing（Ferrer 2026，[新]） | 三种队列分布模型、训练合同、退化数字 |
| XLRW7XXN | DQN 负载均衡路由（Chen/Sun，[新]） | 流量模型、训练-评估合同、饱和曲线 |
| JLF7IEBQ | SaTE 流量工程（SIGCOMM'25，[新]） | 混强度训练合同、负载-满足需求曲线 |
| GPDPLJNG | MCF 路由 DRL-SR（Tsai WCNC'22，[新]） | 需求注入模型、约束式建模 |
| ZIUBKVPZ | Constrained DQN（Hegde WCNC'25，[新]） | 约束式学习、动态负载条件评估 |
| S85KQ4FC | Flow-Centric DRL（Liu 2024，[新]） | 推理瓶颈、到达率扫描、塌陷证据 |
| UKBSA7WN | QRLSN（Huang 2023，[新]） | Poi(5) 单负载训练合同 |
| 53HEEK33 | Fast-Convergence RL（Ding 2023，[新]） | 流量设置、奖励 |
| 42E4NAQU | Queue-Aware MARL（preprint 2026） | 流量生成模式、指标口径 |
| EG9X569M | RRS-DRL（Chu 2023） | "robust" 的实际指代 |
| UF8IQTA2 | Traffic-Predictive Routing（Liu 2023，[新]） | 预测+阈值切换判据 |

事实笔记（仅作线索，未回原文的断言一律标【笔记】）：`round/knowledge/notes-neutral/` 下 3 篇：CHOU-2026-STL（对应 Zotero LZKNZA8B 同篇预印本，笔记为全文级深读）、ZHOU-2026-DTAR（全文级深读；不在 Zotero 111 内）、LOZANO-2025-CONTINUAL（全文级深读；不在 Zotero 111 内）。其余 38 篇笔记未读。

### 1.2 检索渠道与查询词

- Undermind `search_papers` ×2（semantic，workspace eef99118-f623-4a47-a34a-05c6617b7ecb；预算 3 用 2）：
  - q1："Reinforcement learning based packet routing policies degrade when deployed at traffic load intensities different from training: measuring train-test traffic load mismatch, load sweep curves, delivery ratio collapse under increasing offered load, or generalization of RL routing across varying traffic intensity…"
  - q2："Learned or deep reinforcement learning routing policies trained on traffic demand matrices are evaluated on unseen demand matrices and different load levels: how training traffic distribution coverage affects routing generalization…"
  - 命中：Rot24（=Zotero L2VKYTAV/5PYWVRC5，库内）、Loz24、Heg25（=ZIUBKVPZ，库内）、Chu23（=EG9X569M，库内）、Man20（Manfredi，笔记在库）、You19/You22、Val17（Valadarsky《Learning To Route with Deep RL》2017，**库外**）、Din19（《DRL for Router Selection in Network With Heavy Traffic》2019，**库外**）、Son25（《Enabling Robust and Generalized DRL-Driven Routing Optimization…》2025，**库外**，无 PDF）、Kim22、Bha22。**两次检索均未命中"固定策略跨强度扫描 / 训练-部署负载失配审计"的直接先例**。
- Undermind `read_pdfs`：0 次（未动用预算）。
- 失败与失败处理（如实记录）：`get_orientation` 首次调用因缺空对象参数报错、`search_papers` 首次调用缺 workspace_id 且 search_type 取值错误——均为参数绑定错误，重试成功，未返回结果的失败不计入查询次数。
- `LITERATURE/papers/*.pdf`：ls 未列出任何 PDF（与任务书"14 篇本地 PDF"不符），本次未依赖该层；`LITERATURE/SOURCES.csv` 仅读了表头 3 行。
- web_search / arXiv API：未使用（库内证据在时间预算内已饱和，外部核查由 Undermind 承担）。

### 1.3 语料观察：训练-评估负载合同快查表（路径A 主证据）

| 论文 | 训练负载合同 | 评估负载合同 | 跨强度证据 |
|---|---|---|---|
| UKBSA7WN QRLSN | 单一强度：`xk~Poi(5)`（其 Table 2 "User request xk Poi(5)"，1000 episodes×1500 steps） | 同一模型 | 无跨强度；维护相有在线 Q 更新【原文事实】 |
| XLRW7XXN | Poisson 初始负载、8×8 网格、单一设置（Table 1） | 同一设置；Fig 4/5 给出随包数增加的对比曲线 | 未报告训练-评估分离【原文事实】 |
| GPDPLJNG | 用户请求随机注入、单一线速设置 | 同一设置 | 无【原文事实】 |
| 53HEEK33 | 单一设置 | 单一设置+链路失效 | 无【原文事实】 |
| CMNCS52M | 训练曲线以 population-based 队列分布模型给出（Fig 3），500k episodes | 三种队列分布模型（zone/population/traffic）×多拓扑尺寸 | 跨拓扑泛化有实测；**跨队列分布模型（≈跨负载分布）迁移未见报告**【原文事实+待证】 |
| 42E4NAQU | uniform 与 population-based 两种背景流量 | 同两种 | 摘要声称 "under increasing traffic load" 有效，合同未披露【原文事实+待证】 |
| ZIUBKVPZ | 链路负载作为状态输入，约束式 DQN | "dynamically changing link load conditions"（其 §III–IV） | 有动态负载条件评估；负载生成模型细节未提取到【原文事实+待证】 |
| S85KQ4FC | 单一策略；推理实验对到达率 13k–21k pps 扫描 | 同上 | 到达率扫描测的是**推理时延瓶颈**，不是策略泛化【原文事实】 |
| JLF7IEBQ SaTE | 训练 TM 显式覆盖"varying overall traffic loads (e.g., arrival intensity)" | unseen 拓扑 + unseen 流 | **监督侧唯一对等合同**：混强度训练+unseen 评估【原文事实】 |
| LZKNZA8B（CHOU 笔记） | NHPP 周期负载 λ0(1+sin(2πt/T))，120/180/240 Mbps | 同一回合内周期负载 | 强度变化内嵌于回合内周期，非训练/评估分离【笔记（全文级）】 |
| DTAR（笔记） | 日模式时空不均矩阵；surge=μ=5× 局部热点 | normal/surge/fault 三场景 | surge 是**空间**热点放大而非全局强度；且不同场景用不同指标展示【笔记（全文级）】 |

横向结论【推演，基于上表】：(a) RL 路由侧"训练单强度、评估同强度"是默认做法且多数不披露合同；(b) 做负载扫描的论文把扫描当对比曲线而非泛化测试；(c) 唯一把整体强度作为训练覆盖维度的相邻工作是监督 TE（SaTE）；(d) 真正的跨强度失配退化曲线在库内 11 篇中缺失——这正是路径A 的可下手空间，也是本文件三张卡的公共前提。

---

## 2. 候选卡（3 张）

### 卡 A1「负载合同审计 + 固定策略强度扫描 + 强度条件化输入」

**1) 场景与可观察现象**
逐包/逐流路由决策时刻；决策信息=本星与邻居队列观测（CMNCS52M 用 4 邻居队长+历史观测；LOZANO 笔记中为 16 个 log 压缩拥塞字段）。负载变化形式=全局强度缩放（到达率/请求期望 k/占用率的整体升降）。可观察量：PDR、E2E 时延、队列占用分布随强度的曲线；以及一个元层面的可观察量——**每条曲线是"训练强度处"测的，还是"冻结策略跨强度"测的**。

**2) 困难与原因假设**
- 【原文事实】§1.3 快查表：11 篇中无一报告固定策略跨强度部署实验；UKBSA7WN 训练合同锁死 Poi(5)；XLRW7XXN 未报训练-评估分离；CHOU-2026-STL 的强度变化内嵌于回合内周期（笔记）。
- 【原文事实】CMNCS52M（Vol.7 2026, p.1372–1378）：同一算法族在静态 zone 队列分布下 NMB≈15%，在因地球自转而时变的 population/traffic 分布下 DQN-BL NMB 达 70%/55%，DQN-LSNR 亦达 40%/20%——**负载/拥塞分布漂移本身已实质性伤害策略**，即使不跨模型迁移。
- 【推演】"跨强度退化"的真实幅度可能被三种惯常做法系统性掩盖：每强度重训（合同不披露时读者无法区分）、回合内周期化负载（CHOU 型）、指标口径差异（42E4NAQU "negligible packet loss **under their respective definitions**"）。
- 【待证】强度失配下退化曲线是悬崖还是缓坡；库内无人测量过。

**3) 拟议改动**
先辨因：退化可能来自 (i) 状态分布漂移（占用分布随强度整体平移）、(ii) 奖励尺度漂移、(iii) 物理饱和/推理瓶颈（卡A3）。本卡处理"可辨识性"通道——让策略显式感知强度，并给出一套可证伪的测量协议：
- 测量协议（诊断件）：固定策略强度扫描协议——冻结策略在 {0.25, 0.5, 1, 2, 4}× 训练强度上评估，输出 PDR/时延 vs 强度曲线，并与"每强度重训"曲线同图对比；两曲线的差值=可归因于学习问题变化的份额。报告合同标准字段：训练强度集合、评估强度集合、策略是否冻结、指标口径。
- 学习更新（方法件，强度条件化输入）：状态量增加标量 λ̂/λ_ref（当前回合的实测到达强度/参考强度，可用滑动估计）；一次具体更新：s′ = [s, λ̂/λ_ref]，Q 网络直觉上可学到"同一队长观测在不同强度下应选不同动作"。目标函数与更新式不变（仍 DQN 时序差分）。
- 作用机制：消除 (i) 中"状态对强度不可辨识"的成分——同样 60% 队长在 0.06 与 0.5 平均占用网络里含义完全不同（CMNCS52M 的 8× 占用摆动），条件化后策略可按强度分区行为。
- 什么情况下不起作用：若部署侧本可每强度重训或在线更新（Q-routing 维护相本就持续更新），失配问题不成立；若退化主要由 (iii) 物理瓶颈主导（见卡A3），条件化输入无效；λ̂ 估计若滞后于真实强度突变，条件化反而引入振荡【待证】。

**4) 初步近邻（均查自 Zotero 111）**
- JLF7IEBQ（SaTE，SIGCOMM'25）：监督 TE，训练 TM 显式覆盖变化的整体负载（arrival intensity），评估 unseen 拓扑+流；差异=监督/集中式 TE，非逐包 RL，且未讨论强度条件化输入。
- CMNCS52M：三队列分布模型同文评估；差异=未报告跨模型迁移实验，状态含时间信息但无强度标量。
- ALMASAN-2022-DRLGNN（笔记）：在未见拓扑上评估泛化——泛化轴是拓扑而非负载。
- LOZANO-2025-CONTINUAL（笔记）：持续学习对齐时间尺度；拥塞轴收益声明未展开，默认负载 ℓ=1 单强度。
- 库外【待证】：Val17（Valadarsky 2017，demand matrix 训练）、Din19（heavy traffic router selection）——未读全文，仅作线索。

**5) 简单替代猜想（百分比均为猜想，待验证假设）**
- 普通混载训练（episode 强度 λ~U{λmin..λmax} 采样，状态不加强度标量）：若退化由状态分布漂移主导，预计吃掉本卡方法件收益的 60–80%——混载直接把训练分布覆盖到部署分布，条件化输入的增量只在"同一策略跨强度在线切换"场景保留。
- 合理在线微调（Q-routing 延续更新，UKBSA7WN 维护相已有雏形）：中等漂移下预计再吃 10–20%，但 LOZANO 笔记记录了持续更新的模型发散（CKA 0.8→0.3）风险。
- 规则路由：CMNCS52M 中 SP 是全知上界（不允许弱化），ELB/TLR 有显式队长阈值、天然对占用漂移有一定鲁棒性【原文事实（CMNCS52M 引用段）+推演】。

**6) 立即淘汰条件**
- 系统检索（约半周）发现已有论文做了固定策略跨强度扫描、且 PDR/时延退化 <5% 无悬崖；
- 或平台仿真器无法支持"冻结策略跨强度评估"这一最低实验形态；
- 或混载训练对照与强度条件化输入的差距 <2%（统计噪声内），则方法件死，仅剩审计协议价值。

**7) 下一项廉价核验（1–2 天）**
在开源仿真器（SatCom-TELMA，LOZANO 笔记记载 155 stars、活跃）上复现单强度 DQN 训练（Poi(5) 或等价到达过程），冻结策略做 0.25–4× 强度扫描，画出第一条 LEO RL 路由跨强度退化曲线；同图叠加重训曲线。产出=退化形状（悬崖/缓坡）+可归因份额。

**8) 来源指针**
CMNCS52M（§III.B QUEUE-DISTRIBUTION MODEL、Fig 2、Fig 3、Table 2/3、p.1372–1378）；UKBSA7WN（Table 2）；XLRW7XXN（Table 1、Fig 4/5）；42E4NAQU（流量生成模式段、Fig 2）；JLF7IEBQ（§1 评估段、§5）；GPDPLJNG（约束式 (1)–(6)）；LZKNZA8B/ZHOU-2026-DTAR/LOZANO-2025-CONTINUAL（对应笔记）；Undermind q1/q2（§1.2）。

---

### 卡 A2「强度进入学习问题的三个通道：占用分布、奖励尺度、最优结构 → 相对化状态 + 溢出约束更新」

**1) 场景与可观察现象**
同卡A1 的决策时刻与信息条件。负载变化形式：全局强度缩放 + 拥塞分布的时空漂移（地球自转驱动的昼夜占用漂移，CMNCS52M population/traffic 模型）。可观察量：跨强度下冻结策略的 NMB（相对最优的归一化平均时延差）、Q 值分布、邻居占用秩分布。

**2) 困难与原因假设**
- 【原文事实】强度变化改变**占用分布**：CMNCS52M 三模型的平均占用率 zone=0.5、population≈0.06（≈8× 摆动），且队列容量被反调以维持 ~1s 平均排队时延（§III.B）→ 绝对队长的"同一读数"在强度/模型间语义漂移。
- 【原文事实】强度变化改变**最优结构**：CMNCS52M population 场景中 SP 选择"traversing longer but less congested paths"——强度不只缩放时延，还改变哪条路径最优；静态 zone 下 DQN-BL NMB≈15% vs 时变下 70%（Table 3 上下文）。
- 【原文事实】强度变化改变**奖励尺度**的免疫方案存在：ZIUBKVPZ（WCNC'25）明言其约束式设计"constraints are independent of scaling of the immediate reward function and eventually an optimal Q-function is learnt which adheres to the constraints"——约束形式对奖励尺度漂移免疫；且其评估明确识别"约束不可满足的条件"，届时切换规则路由。
- 【推演】通道假设：冻结策略跨强度退化 = 占用分布漂移（状态语义变）+ 奖励尺度漂移（Q 目标移动）+ 结构变化（最优路径本身变）三通道叠加；库内文献没有把三通道拆开测量。
- 【待证】相对化状态能否吸收通道 1 而不丢失拥挤结构信息（低占用 0.06 场景秩可能退化）。

**3) 拟议改动**
两个可独立成立的变更（可组合）：
- 状态相对化：把邻居绝对队长替换为局部分位数特征——该星 4 邻居占用率的秩 + 相对均值的偏移（rank(s_i,·), mean-shift(s_i,·)）。跨强度下状态分布近似不变（对 8× 占用摆动不敏感）。动作与网络不变。
- 溢出约束更新：把"时延最小化"目标改写为约束式——最小化传播/传输项，约束 P(queue overflow)≤ε；一次具体更新：L(θ,μ)=E[(r_prop+r_tx)−μ·1{overflow}]，θ←θ−η∇θL（DQN 拟目标内嵌 μ 惩罚），μ←[μ+η_μ(overflow_rate−ε)]⁺（对偶上升）。借鉴 C-DQN 的尺度免疫论证，把约束对象从"环/负载"换成"溢出率"。
- 作用机制：状态相对化打掉通道 1（占用漂移），约束式打掉通道 2（奖励尺度漂移，溢出指示 0/1 不随时延量级缩放）；通道 3（结构变化）不声称解决——由卡A1 的"重训差值"判别其份额。
- 什么情况下不起作用：结构变化主导时（population 型绕路需求），相对化状态仍会选错结构；ε 取固定值跨强度可能不可行（ZIUBKVPZ 自己发现约束不可满足区）→ 需 ε(λ) 随强度调度，否则系统退化为规则回退；低占用场景（0.06）下邻居秩信息量不足，区分度塌缩【待证】。

**4) 初步近邻（均查自 Zotero 111）**
- ZIUBKVPZ（C-DQN，WCNC'25）：约束式 DQN 已存在；差异=其约束对象是环/负载可行性，未做跨强度泛化声明，也未与强度扫描联动。
- LOZANO-2025-CONTINUAL（笔记）：log 压缩拥塞编码 C_j,k 就是一种有损归一化——最接近的"相对化"先例；差异=未检验跨强度不变性，也未做约束式更新。
- CMNCS52M（DQN-LSNR）：加 4 个历史观测防环；差异=防的是回访不是漂移。
- MXQVNU3P / XM64YRAW（GNN+DQN 系）：表示学习路线；中性视图已注明"表示能力、特征工程、参数量和训练预算的贡献通常未完全分离"。

**5) 简单替代猜想（百分比均为猜想，待验证假设）**
- 混载训练+原绝对状态：若漂移主导，预计吃掉 50–70%（同卡A1 替代项；对通道 2 无直接作用但重训覆盖可部分吸收尺度漂移）。
- LSTM/历史窗（CHOU-2026-STL 的 GAT+LSTM+DQN 管线）：对时变部分预计吃掉 30–50%，但笔记记录其危险信号——Proposed 推理 2.70ms 实为四者最慢、且数字内部矛盾（吞吐 87.5% vs 丢包 46.8%）→ 开销与可靠性存疑。
- 规则阈值路由（ELB/TLR）：对占用漂移免费鲁棒，但不吃结构变化收益；CMNCS52M 中 CA-DRP（队列感知版）把 NMB 从 0.5/1.8/2.3 降到 0.3/1.4/2.1——说明"邻居队列信息"这一已可获得信息本身已吃掉相当份额【原文事实】。

**6) 立即淘汰条件**
- 卡A1 扫描显示退化由结构变化主导（冻结策略在低强度反而接近重训策略，且 SP 等规则法同样退化）→ 通道 1/2 假设死；
- 分位数状态在低占用下与随机等价（秩无区分度）；
- 溢出约束式在与普通 DQN 的对照中无显著差（溢出事件本身稀少到无法驱动对偶更新）。

**7) 下一项廉价核验（1.5 天）**
在卡A1 平台上，同一训练预算训两个状态变体（绝对队长 vs 邻居相对秩），冻结后跨强度扫描，比较两曲线族间距与逐强度 NMB；再加一个溢出约束变体验证对偶更新收敛性。产出=三通道中可被状态/更新修复的份额。

**8) 来源指针**
CMNCS52M（§III.B、Table 3、Fig 3）；ZIUBKVPZ（§II 约束设计段、贡献 (iii)、Abstract）；LOZANO-2025-CONTINUAL 笔记（状态编码段）；中性视图 Assumption Map（"流量平稳或统计已知，突发性和多源目的业务被简化"）；CHOU-2026-STL 笔记（奖励 r=−(α·D+β·Q)，β>α）。

---

### 卡 A3「塌陷先发生在决策器：推理排队瓶颈、塌陷形状与前兆」

**1) 场景与可观察现象**
星上 DNN 逐包推理的决策器；到达率 λ_in（强度参数）；可观察量：决策排队时延、决策缓存占用、决策丢包、PDR、E2E 时延。负载变化形式：强度上升（13k→21k pps 量级）或突增。可观察方式：把决策器建成可观测的排队系统（M/D/C/N）后逐项计量。

**2) 困难与原因假设**
- 【原文事实】S85KQ4FC（2024）：逐包 DNN 推理在到达率 21k pps（≈300 Mb/s @1500B）时，路由决策时延达 17.5 ms、丢包率 21%；决策排队为 M/D/C/N 模型、缓存 M=300 包、F=8 路并行推理；原文明言"ignoring the DNN inference time may threaten the correctness of conclusions drawn in prior works"——**高强度下塌陷先发生在决策器（物理排队溢出），而非策略变差**；缓存有限 → 该瓶颈是硬悬崖。
- 【原文事实】SaTE（SIGCOMM'25 §5）：satisfied demand 随负载上升**渐进**下降，归因是链路 200 Mbps 容量"successive saturation"；分布式 backpressure 在重载下最差（无全局视图）——瓶颈在链路容量时塌陷是渐变形状。
- 【原文事实】XLRW7XXN（Fig 4/5 讨论）：最短路吞吐"reaching and maintaining the maximum value first"后饱和最低；最大流吞吐更高但时延高——同样是饱和渐变形状。
- 【推演】塌陷形状由主导瓶颈决定：决策器排队（硬缓存 300 包）=悬崖且有可测前兆（决策缓存占用率、决策队列长度）；链路饱和=渐变；多数 RL 路由论文不建模决策器排队，其"高强度退化"结论可能把物理瓶颈误归因为学习失败（或反之）。
- 【待证】库内除 S85KQ4FC 外无第二篇把决策时延项纳入度量（本路径 11 篇提取中未再出现）；真实星座到达率是否落入推理瓶颈区间未知。

**3) 拟议改动**
决策结构变更（不预设新网络、不改学习问题本体）：
- 双粒度决策：到达包先查 flow table——命中且本星决策缓存占用 ≤ θ_dec 时沿用缓存的下一跳；miss、表项过期（TTL/拥塞标志）或 θ_dec 超限时触发 DNN 推理并把结果写回 flow table。
- 学习侧：目标函数加决策排队时延项 E[D_dec]（S85KQ4FC 已把归一化决策时延计入奖励；本卡差异在于双粒度+失效判据+与强度扫描/前兆联动），更新式不变。
- 作用机制：把推理需求从 O(包) 降到 O(流)，M/D/C/N 的有效到达率成倍下降 → 悬崖右移；决策缓存占用率成为塌陷前兆（悬崖前可测、可触发降级）。
- 与前兆联动的降级运行：θ_dec 超限持续 T 秒 → 回退规则路由（k 短路查表，零推理）——近邻 ZIUBKVPZ 已有"约束不可满足→规则回退"先例，本卡把回退触发器换成决策器前兆。
- 什么情况下不起作用：流寿命短（LEO 接入切换频繁 → flow table 失效率高，退化回逐包）；流内拥塞异质要求逐包差异决策；真实到达率远离推理瓶颈区间（则问题仅存在于高吞吐假设，价值缩水）【待证】。

**4) 初步近邻（均查自 Zotero 111）**
- S85KQ4FC（最直接）：flow-centric DRL；差异=它证明"流级可省推理"的可行性，未研究跨强度的塌陷形状、前兆指标与回退判据。
- UF8IQTA2（Traffic-Predictive Routing）：NN 预测下一时刻负载 + 动态阈值切换转发控制——"阈值切换判据"的近邻；差异=非 RL、AODV 框架。
- ZIUBKVPZ：约束不可满足时回退规则路由——降级运行近邻；差异=触发器是约束可行性不是决策器前兆。
- CTWVLBCY（《Transmitting, Fast and Slow: Scheduling Satellite Traffic through Space and Time》）：标题级线索【待证，未读】——"快慢双系统"与双粒度决策疑似同构，立项前必须精读排除撞车。
- JLF7IEBQ（SaTE）：GPU 17ms 集中式 TE 计算时延——决策时延意识的另一侧先例（集中式）。

**5) 简单替代猜想（百分比均为猜想，待验证假设）**
- 更小/蒸馏的决策网络：同样右移悬崖，预计吃掉 60%+ 收益且工程代价更低——本卡必须与之对比并说清"流级缓存+前兆降级"的增量在"网络仍不够快+流寿命够长"的交集里。
- 纯规则路由（k 短路查表）：零推理瓶颈，但 CMNCS52M 显示 SP 类在高占用下绕不开拥塞（NMB 2.3×）、SaTE 显示分布式 backpressure 重载最差【原文事实】——规则法吃不饱满负载收益，但作为回退层免费。
- 加大 F（并行推理数）：纯工程解，不改学习问题，可作为对照上界。

**6) 立即淘汰条件**
- 实测显示真实星座参数（F=8、包长 1500B、单星到达率 ≤ 数 k pps）下决策器永不排队（决策时延≪平均包间隔）；
- 流级缓存命中率 <50% 且时延劣化超过决策排队收益；
- 精读 CTWVLBCY 后确认其已完整覆盖"快慢双粒度+前兆降级"。

**7) 下一项廉价核验（1–2 天）**
在仿真器加 M/D/C/N 决策器模块（参数对齐 S85KQ4FC：D_dec、C=F、N=300），对逐包 vs 流级两粒度做到达率扫描，测决策缓存占用曲线与塌陷点偏移，并输出"前兆指标曲线"（占用率轨迹 vs 塌陷时刻）。产出=悬崖是否存在、右移多少、前兆可测性。

**8) 来源指针**
S85KQ4FC（Fig 2 到达率实验、M/D/C/N 段、奖励含 D_dec 段）；JLF7IEBQ（§5 负载-满足需求曲线、§2.3.2 THT）；XLRW7XXN（Fig 4/5 饱和讨论）；ZIUBKVPZ（§III–IV 回退段）；UF8IQTA2（贡献段、阈值机制）；CTWVLBCY（仅标题，Zotero #44，待证）。

---

## 3. 诚实放弃线

- **按强度的课程学习训练**：SaTE 已把 curriculum learning 用于跨尺度微调（其 §5.5），与卡A1 混载对照重叠、无独立机理链，放弃。
- **AoI 路由**（R5QTFKD2、GV9PPNZT、83 4QG5VYHQ 等）：优化对象是业务数据年龄而非路由状态，与"到达率/时延"机理链不同轴，放弃。
- **容量规划/拓扑瘦身**（25 XM6NUPM4、88 K93SCUF2）：离线容量层问题，不改变在线路由学习问题的结构，放弃。
- **链路故障/干扰鲁棒**（61 EG9X569M、27 5N5LQPPP、54 JZA5SEQA）：库内 "robust" 多指链路退化/干扰而非负载强度（EG9X569M 全文提取证实），属其他路径分工，放弃。
- **模型基快适应**（10 YI9G7NR7 Dyna-Q 系）：逻辑上依赖"跨强度退化存在"先成立（卡A1 结论），且时间预算内未精读，记待证后放弃。
- **星地接入段负载耦合**（75 PIXWFHAC 等）：接入建模是另一层仿真合同问题，与强度机理链耦合但超出本路径预算，放弃。

## 4. 防火墙声明

- **白名单文件**：round/zotero/ZOTERO-INDEX.md（全读）；round/knowledge/NEUTRAL-KNOWLEDGE-VIEW.md（全读）；round/knowledge/notes-neutral/ 3 篇（CHOU-2026-STL、ZHOU-2026-DTAR、LOZANO-2025-CONTINUAL；目录文件名清单经 ls 获取一次）；LITERATURE/SOURCES.csv（仅表头 3 行）；round/zotero/ 与 round/run2/ 顶层 ls。
- **zotero_fulltext**：11 个不同 itemKey、共 17 次调用（CMNCS52M×3、XLRW7XXN×2、JLF7IEBQ×1、GPDPLJNG×2、UF8IQTA2×1、ZIUBKVPZ×2、S85KQ4FC×1、UKBSA7WN×2、53HEEK33×1、42E4NAQU×1、EG9X569M×1）。zotero_item 未调用（索引已含元数据）。
- **Undermind**：get_orientation ×1、list_workspaces ×1、search_papers ×2（预算 ≤3，合规）；失败参数绑定调用 ×2（无结果返回，不计查询）；read_pdfs ×0。查询词全文见 §1.2。
- **web_search / arXiv API**：0 次。
- **黑名单**：未接触任何黑名单路径；未对 LITERATURE/notes/raw/**、ANALYSIS/**、round/run1/**、round/reviews/**、round/history/** 及任何黑名单文件执行 ls/find/glob/read；意外接触：无。
- **产出**：本文件 round/run2/staging/path-A-intensity.md（唯一写入）。
