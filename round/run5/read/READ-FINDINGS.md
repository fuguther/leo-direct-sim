# 通读中的重大发现登记（READ-FINDINGS，主控，2026-09-11）

> 来源：全库通读子代理在**逐字阅读中自然发现的**东西（不是检索出来的）。
> 处置原则：凡动摇前提的发现，一律登记为"方案必须回应的前置条件"，不得回避。

## F1【动摇前提·最高级】真实 Starlink 时延尖峰**不是拥塞引起的**（GGFJ3SEG，逐字核验）

VM MD 第 190 行逐字：
> "**RTT spikes are also not due to congestion.** The ground truth metrics report **no packet drop or drop in bandwidth** during sustained or standard latency spikes. Furthermore, we find that **spikes occur in multiples of 15 second**—aligning with Starlink's report..."

第 188 行逐字：
> "Sustained spikes in RTT are **not caused by distant satellite location and not always caused by satellite switches**."

**含义（必须直说）**：在真实 LEO 网络里，端到端时延变化的主导方差源**是拓扑/路由重配（15 秒整倍数的重配周期）**，不是负载。这直接冲击"负载变化导致时延/到达率劣化"这一叙事在**真实网络**中的普适性。

**处置**：
1. 任何"负载升高 ⇒ 时延升高"的主张，**必须先与卫星重配周期这一混杂源分离**，否则站不住；
2. 本项目的实验平台（leo_sim V2）恰好**可以**做这个分离（拓扑重算间隔有 0.5/1/2/5 s 四档、E0=1 s）——**这反而变成一个可做的实验设计要件**，而不是障碍；
3. 该文还给出可复用的滤波窗口（15 秒，对应卫星切换周期，第 152 行）。

## F2【动摇前提·次级】RTT 统计里能读出的主要是静态地理底，动态信息几乎不贡献（GJJQUMQ2）

R5 读卡：跨区域时延差异只体现在 min RTT（下界）；唯一度量短时变化的特征 F8（相邻秒均值绝对差）**区分力最弱**。

**处置**：涉及"时延"的指标设计不能只靠 RTT 均值；须区分**静态地理底**与**瞬态变化**，否则测不出负载效应。与本项目"瞬态窗条件指标"的设计方向一致。

## F3【候选方向·从阅读中自然浮现】"负载依赖反转"已被两篇独立观察到，但无人解释、无人定位

- **UKBSA7WN** L237 逐字："the VT-SPR routing method is superior to QRLSN in the end-to-end delay performance. It is indicated that VT-SPR is more applicable **under low-load network conditions**."
- **UKEKU5ZG** L232 逐字："**under low traffic loads**, DR-BM can rapidly acquire global information and select paths with shorter delays"

**含义**：低负载时静态/集中式最短路优于 RL；负载升高后 RL 反超。**两篇都只陈述、都不解释机理、都未定位交叉点**（哪个负载阈值/什么条件下反转）。

**处置**：登记为候选方向 N1（见候选台账），**但它是否够格做选题，要等其他读卡回来后再判**——现只有 2 篇的"陈述级"证据，且都是各自实验的副产物，不是被研究对象。

## F4【语料污染·已核实】5 篇领域外文献混入 111 篇语料

已核实 VACUFEHB = 1998 年《三阶自适应 Volterra 滤波器》论文（UIUC，参考文献仅 4 篇，无卫星/网络概念）。ZOTERO-MD-INDEX 已标注 **[无关·已移出]**，但 ZOTERO-INDEX 仍列在册（第 104 行）。

同类（通读中确认）：A7QNRKML（人脸关键点）、ETTA3DIV（聚变等离子体）、WT839JP7（代码膨胀）、35T2JJRJ（版权页级内容）。

**处置**：**有效语料 = 111 − 5 = 106 篇**。后续所有"全库 N 篇"的表述必须改用 **106 篇**（或明确写"111 篇含 5 篇领域外"）。此前的关键词计数若以 111 为分母，需按 106 复核。

## F5【检索质量·已核实】OCR 连字损失**只影响 LJG6ZW7B 一篇**

主控实测（python 遍历 111 篇）：含 U+21B5（↵）的文件**只有 1 个**（LJG6ZW7B，1352 处）；其余 110 篇为 0。
- 该篇内：off-policy 正确 64 / 损坏 189；difference 336/164；effect 729/205；differs 18/7；efficient、sufficient、confirmed 损坏 0。

**含义**：**此前基于全库的 grep 计数未被污染**（除教材一篇）。子代理对"全库检索需加归一化层"的建议，实际只对 LJG6ZW7B 适用——**但这条必须以实测为准，不能凭单篇现象推断全库**。这本身是一次"局部现象误推全库"的教训。

## F6【两个作者自认空白】可直接作选题依据（逐字）

- **2QRYMWBI L798**："we could not identify any previous work where a tradeoff in terms of ML potential performance benefit versus added cost and complexity on the satellite device."
- **2QRYMWBI L822**：开放高分辨率数据集"pretty rare"（除卫星影像）；
- **GPLEP83L**：把 "traffic loads" 写入 future work（自认未做负载）。

## F7【复现性警告】两篇论文内部自相矛盾，引用需避坑

- **GPLEP83L**：§IV.F Discussion 把 Table I 的数字**写反**（说 GPT 时延更低，实际是 Opus 85.13 vs GPT 88.41）。→ 只用 §IV.D / Table I。
- **GPDPLJNG**：**§IV 整节缺失**、从 III 直接跳 V；**全文无任何具体数值、无表格**；基线只有最短路一个。→ 不可作为定量依据。

## F8【跨篇口径缺陷·动摇可比性】"平均时延"的分母在不同论文里不一样，导致"负载↑→时延↑"不自动成立

主控逐字核验的三条证据（全部已在 VM 原文核对）：
1. **VFS59FHI L269 逐字**：
   > "However, the average delay **decreases** as u increases with some sizes. This phenomenon is caused by **big rejection ratio**, and only part of traffic can occupy resources. When the rejection ratio is small, the average delay increases as the size extends."
   → 被拒绝的业务**不进入时延统计**，负载升高时平均时延反而下降。
2. **UKEKU5ZG L232 逐字**：
   > "By dividing the total latency by the number of **transmitted** data packets, the average latency can be obtained."
   → 分母是"已发送"包数，同样把未成功者排除在外。
3. **UKBSA7WN L204**：超时包仍留在队列缓冲、直到出队时才判定丢弃 → 丢包判定滞后，同样影响时延口径。

**结论**：在存在拒绝/丢包的 LEO 路由研究里，**"负载↑ ⇒ 平均时延↑"不是自动成立的常识，完全取决于分母定义**（含拒绝 vs 仅成功业务）。
**处置（两条，都要做）**：
1. 本项目任何时序延指标必须**显式声明口径**（分母、是否含被拒/丢弃业务），并在实验设计里同时报告**到达率（PDR）与时延**——这一点恰好与本项目"主指标=到达率+端到端时延"的固定边界一致；
2. **登记为候选方向 N2**：把"负载-时延曲线的口径依赖"本身做成一个被测量、被显式化的命题。**是否够格做选题，待全部读卡回来后再判**（现为 3 篇的独立观测，且都是各自实验的副产物）。

## F9【候选方向·从阅读中浮现】拒绝率与时延是对立指标，可分离（VFS59FHI）

VFS59FHI L294/L302：Dijkstra 时延最低但拒绝率最高；HRA 拒绝率改善但时延最高；"拒绝率小的前提下，可绕行区域越大，平均时延越高"。
→ 与 F8 合起来指向同一个问题域：**负载升高时，系统在"丢/拒"与"慢"之间如何取舍**，而这个取舍点从未被作为研究对象显式刻画。

## F10【教材层可迁移判据】"收敛最优 ≠ 在线表现最好"（LJG6ZW7B Cliff Walking，L2409–L2419）

Q-learning 学到最优贴崖策略，但因 ε-greedy 偶发掉崖，**在线回报反而差于学到次优绕路策略的 Sarsa**。
→ 对本项目的意义：若评价指标是"在线到达率/时延"，**"训练收敛到最优策略"不足以作为结论**；必须报告部署期（冻结策略）的在线表现。这与本项目"固定训练后部署"的暂用设定直接相关。
