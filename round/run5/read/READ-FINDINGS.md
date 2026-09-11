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
