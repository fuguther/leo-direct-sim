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

## F11【直击"负载变化"前提】PIXWFHAC 自述：用户数一变就要重训（R7 读卡）

PIXWFHAC L437 自述硬伤：用户数变化即需重新训练；**而其实验横轴恰恰就是用户数**。
另：该文只记传播时延，负载→时延的机制是**路径伸长**而非排队（R7 读卡第 3/4 项）。
→ 这是全库目前**最接近"负载变化下学习器失效"的一条自述证据**，且是作者自己写的，不是我推断的。
→ 处置：登记为**方案必须回应的对手**（若本项目主张"用学习应对负载变化"，必须先说明为何本方案不落入同一失效）。同时它比我此前的思路更朴素——**"负载变了就得重训"这件事本身可能就是缺口**。

## F12【同族方法但环境不真】MXQVNU3P 名为 LEO 路由，训练与评估全在 NSFNet（R7 读卡）

MXQVNU3P 与 LZKNZA8B 属同族（图算子 + 序列/空间建模），但 **MXQVNU3P 的 LEO 只停留在假设里，实验全在地面网（NSFNet / KDN 数据集）**。
→ 处置：可作为"同族方法 × 环境真实性"的对照对（同一方法族，一个在真 LEO、一个在地面网）。也提示全库存在**"声称 LEO、实测非 LEO"**的一类条目，需在汇总时统一标记。

## F13【教材层·非平稳是最常见情形】常数步长的定位（LJG6ZW7B part1，逐字）

- L710 逐字：effectively nonstationary 是 RL 中**最常见**的情形；
- L705/L710：常数步长**永不真正收敛**，但以此换取跟踪能力；
- L707–L708：收敛条件 Σα=∞ ∧ Σα²<∞（可作步长设计筛选门槛）；
- L755：UCB 在**非平稳与函数逼近下"usually not practical"**；
- L874/L878：Gittins 需完整先验、Bayes 最优计算不可行（2^2000 叶）。

→ 对本项目的意义：**"负载变化"在 RL 理论里就是"非平稳"**，而教材明确承认：常用的乐观探索方法（UCB）在非平稳下不实用、常数步长是"永不收敛换跟踪"。**这为本项目提供了理论定位**，也说明"负载变化"不是一个工程细节，而是触及 RL 基本设定的问题。
→ 另一条**增量空间**（教材原话的空白）：书中**没有**截止期、超时丢弃、队列长度、到达率这些量（part1 读卡明确写出）——本课题的量在教材体系里是缺的。

## F14【模式·从阅读中自然浮现，非检索所得】"负载升高 ⇒ 简单/静态方法反超 RL"已被多篇独立观察到

**四条独立观测（三篇为读卡发现，主控已逐字核验其中两条）**：

| # | 文献 | 逐字/读卡证据 | 交叉点是否定位 | 机理是否解释 |
|---|---|---|---|---|
| 1 | **UKBSA7WN** | L237 逐字："VT-SPR is more applicable **under low-load network conditions**" | ❌ 未定位 | ❌ 只陈述 |
| 2 | **UKEKU5ZG** | L232 逐字："**under low traffic loads**, DR-BM can rapidly acquire global information and select paths with shorter delays" | ❌ 未定位 | ❌ 只陈述 |
| 3 | **R37BNQQ8** | L394 逐字（负载升高→可选路径被阻断→时延反超）；L439 "little inferior in latency while network load is high" | ⚠️ 有趋势图，无阈值 | ⚠️ 归因于**路径可达性**（非排队；主控已核实其时延模型无排队项） |
| 4 | **PIXWFHAC** | L437 自述：用户数变化即需重训（R7 读卡） | ❌ | ⚠️ 自述局限 |

**共同结构**：负载/规模升高时，**静态最短路、集中式、或需重训的方法与 RL 的相对优劣发生反转**——而**没有任何一篇把这个反转当作研究对象**（不定位交叉条件、不解释机理、不做可复现的对照）。

**处置**：登记为候选方向 **N3**。它与 N1（F3 负载依赖反转）实为同一现象的两次独立浮现，**合并为 N1/N3 一条**。

## F15【机制层·关键区分】负载→时延的两条不同通路，文献里常被混淆

读卡汇总出两条互不相同的机制，**必须分开**：
1. **路径结构效应**：负载升高 → 可用路径减少/被推到跳数更多的路径 → 时延升高（**与排队无关**）。证据：9C6HB6AF L465（"被推到跳数更多的路径"）、R37BNQQ8（路径被阻断）、PIXWFHAC（只记传播时延，机制是路径伸长）。
2. **排队/拥塞效应**：负载升高 → 队列堆积 → 时延升高 + 丢包。证据：S2QZRBEJ 实测（中位 RTT 50→95/104ms，**作者明确归因排队**）。

**处置**：本项目若要主张"负载变化下的时延/到达率"，**必须先声明测的是哪条通路，并设法分离二者**——否则会出现 F8 的口径问题（分母不同）与 F1 的混杂问题（真实网络里主导方差是重配周期）。这三条（F1/F8/F15）合起来构成**方法论的入场券**。

## F16【语料构成·持续累积】离题文献已达 7 篇（有效语料 104 篇）

新增确认：A7QNRKML（人脸关键点定位，纯 CV）、9FLZ88LZ（QMIX，纯 MARL 算法）、QGAREQUM（通用延迟 RL，Acrobot/MuJoCo）。
连同 F4 的 5 篇（VACUFEHB/ETTA3DIV/WT839JP7/35T2JJRJ/A7QNRKML 中的前四）→ **累计 7 篇确认离题**。

**处置**：有效语料 = **104 篇**。另需在全库扫一遍剩余离题条目（已列入待办）。
**注意**：离题不等于无用——QMIX、MADDPG、Asymmetric DQN、GAE 这类是**方法供体**（可迁移的算法件），只是不能当 LEO 领域事实。

## F17【缺口·作者自己写出来的，本批最直接】SKYLINK 把"负载→时延"的连续过渡段整个删掉了

**K7U4TYJN 逐字（L82，主控核验）**：
> "Satellites and ground stations have limited data buffers... If the outgoing data rate $R^{out}_{v,t}$ is less than the incoming data rate $R^{in}_{v,t}$, the buffer at the receiving node fills up. **When the buffer is full, a uniform percentage of data from every incoming stream will be dropped** to align the incoming stream size with the outgoing rate."

**排队时延被写成台阶函数**（R6 读卡）：$\Delta_C \le 0$ 则 $D^q = 0$，否则直接跳到 $Q_{max}/$出速率。
→ 即：**缓冲的填充/排空过渡过程不建模**，负载一旦超过服务率，时延**从 0 跳到满值**，中间的连续过渡段不存在。

**为什么这条最重要**：这是全库目前**唯一由作者显式声明**的"负载→时延映射被简化"的缺口，而且**简化掉的恰好是本项目关心的那一段**（负载变化过程中的时延演变）。它比我此前登记的 N1/N2/N3 都更直接——那三条是观测到现象，这条是**指明了一个被删掉的研究对象**。

## F18【测量学·与 F8 呼应并升级】最短路"平均时延更低"是幸存者偏差（K7U4TYJN 自己承认）

**L364 逐字（主控核验）**：
> "shortest-path algorithms, such as Dijkstra and k-shortest paths, exhibit relatively low delays. However, this is primarily **because these algorithms deliver fewer data in general, favoring data that are closer to the ground**."

**与 F8 合起来**：F8 是分母口径问题（含不含被拒业务），F18 是**幸存者偏差**（只算成功送达的、且偏向近处的）。
→ 合起来构成一条硬约束：**任何"负载升高 → 时延升高/降低"的结论，必须同时报告丢包率与吞吐，否则结论可以反向**。这与我逐字核验的 F8 三篇证据方向一致，且这条是**作者自己承认的**。

## F19【实测数据·可直接用】SKYLINK 的负载扫描（12.7M → 127M 用户）

逐字（L348，主控核验）：
> "From 12.7 to 127 million users, the drop rate for Dijkstra increases from **15.6% to 72.4%**, while for k-shortest paths it increases even faster..."

→ 这是全库**跨度最大的一次负载扫描**（10 倍用户数），且**横轴是规模而非到达率**。可用作"负载—丢包"的量级参照与对照基线。

## F20【时间尺度夹缝】物理拓扑 70 ms 就变，工程重配只能做到分钟级

- **JLF7IEBQ 实测**：Starlink 拓扑保持时间平均仅 **70 ms**；
- **JS857IYN L252 明确**：拓扑重配**做不到亚秒级**（配置复杂度/服务连续性/稳定性）。

→ 对本项目：任何"按拓扑变化重算策略"的设计，必须落在这个夹缝里——**物理上 70 ms 就过期，工程上分钟级才允许重配**。这为"何时更新"提供了硬约束（与 S85KQ4FC 的抖动触发门、R5QTFKD2 的阈值结构定理呼应）。

## F21【"时延最优 ≠ 负载均衡"实测】L2VKYTAV

FD-MADRL 学出的路径**跳数更少但把链路用饱和**；把用过的链路加 20% 负载后，**12 节点仍稳、24 节点不稳**。
另：**全局奖励要等多跳传播延迟 T 后才到达（滞后），局部奖励即时**（L33 逐字）。
→ 与本项目"奖励设计"支直接相关：**全局信号的滞后性是被实测记录的，不是假设**。

## F22【缺口·重量级，2018 年就写明且至今未做】Handley 把"负载相关路由"列为开放问题并给出假设方案

**67CSKFK4（HotNets'18，"Delay is Not an Option"）主控逐字核验**：

L132：
> "it must be capable of routing with low delay, **even when traffic levels are high enough to saturate the best paths**."

L150（**全文假设星上无排队**）：
> "**All the simulations above assume that no significant queuing happens in the satellites themselves.** For high-priority traffic, this can be ensured by admission control, so long as it forms a minority of the traffic."

L152（**明确说现有方案太慢**）：
> "In terrestrial networks, centralized load-dependent routing schemes such as B4[9] and LDR[7] can pro-actively route so as to achieve low latency without causing congestion. These schemes, however, make routing decisions on a **minute-by-minute basis — too slow for routing on dense LEO constellations**. **It is an open question whether such schemes can be extended for this use**, or if the latency between the controller and groundstations will always be too high."

L154（**给出完整假设方案，但未实现**）：高优先级流量走准入控制+显式路由；其余流量由**卫星监测链路负载 → 全球广播 → 地面站感知热点（热点是地理性的而非拓扑性的）→ 在近似路径间处理**。

**三条含义**：
1. **"负载相关路由在 LEO 上怎么做"被 2018 年就点名为开放问题，至今无人做**；
2. 该文自己**假设星上无排队**（L150）——即它把本项目的核心机制排除在外了；
3. 它给出了**完整的候选方案骨架**（监测-广播-地面站决策），可作为对照臂或出发点。

## F23【独立确认·综述背书】7AXASN73 把同一空白列为 "yet unexplored"

R2 读卡记录（其 L377）：负载均衡 + 最短端到端传播时延被列为 "yet unexplored areas in the literature"（2022 年 NGSO 综述）。
→ 与 F22 指向**同一空白**，但**该综述漏引 Handley**（R2 实测）。这是一条可直接引用的"综述遗漏 + 空白被两次确认"。

## F24【唯一把排队论写进路由代价的工作】6GWNYSTT（主控部分核验）

- 显式用 **M/M/1/N** 与 **M/M/c** 建模决策/转发队列，λ 进入时延式；
- 负载阈值：每批 2000–10000 包（L242）；**每批 >10000 包时延破 20ms**；
- 改进算法**跳数最多但时延最低**（绕路降时延的实证）。
- **但**：排队参数**全部未给数值**、式 (11) 在 MD 中渲染为乱码（R2 读卡）。

→ 含义：**排队进入路由代价这件事在 LEO 文献里有先例（一篇，且是表格式 Q-routing、参数不全）**；本项目若做"排队感知"必须与它划界。

## F25【控制面与数据面抢 ISL 带宽】5HJ8ATR7 定量边界

L149 逐字（R2 读卡）：LEO 移动引发的信令风暴"**可占用最多 15.75% 的总 ISL 带宽**"；
L359：400 UEs/km² 下寻呼负载**超过 4G/5G 信道容量**。
→ 与本项目锚件（S85KQ4FC 的决策队列）**同族**：都是"控制/管理开销挤占数据通道"的定量证据。

## F26【失效模式的两种证据】最短路路由特别容易制造热点

- **67CSKFK4 §5 引 [6]** 指出"网状网最短路径路由特别容易制造热点"；
- **5PYWVRC5 用实验复现了它**（节点 4→8→22→23 反例），且动态负载（上 episode 用过的链路 +20%）下 **12 星稳、24 星不稳**。

→ 与本项目"负载变化下的到达率/时延"直接相关：**这是"负载变化导致退化"的一条独立实测复现**，且机制是"最短路制造热点"而非排队。

## F27【模式·四篇独立复现】"低负载区算法无差别、收益随负载放大"（R10 汇总，主控部分核验）

R10 读卡记录四篇独立观测：XLRW7XXN L174 / XM64YRAW L236 / X5K285MW L92 / YI9G7NR7 L160。
**主控核验状态（如实）**：X5K285MW 的 L92 经我核验**内容是"非均匀流量需求使源路由更易受热点影响"**（与"低负载无差别"不同题，但同属负载效应）；XLRW7XXN/XM64YRAW/YI9G7NR7 三条**未逐条核验**（子代理标注的行号与其描述未逐一对照）。
→ **口径**：该模式记为"R10 读卡汇总，未经主控逐条复核"，引用前须回原文核对。

**但模式本身与另两组证据一致**：
- Y2H4NPLU 的归一化负载定义 $\ell = \sum\lambda/\lambda^*$（相对网络容量）—— 全库唯一的规范化负载轴；
- YI9G7NR7 给出负载扫描的绝对值（$\ell=0.8$ 时 241 ms / 送达率 98.6%；$\ell=0.9$ 时优势放大到 27.6%/18.6%）。

## F28【方法学·必须回应的第三条】零负载下 RTT 本身就随卫星运动涨 2.5 倍（W6M3GU7L，主控逐字核验）

L19 逐字：
> "the smallest achievable RTT between a pair of ground stations **can grow by up to 2.5× as satellites move in their orbits**... we find the variability to be **high only when the communicating ground stations are within 1500-3000km of each other and the travel direction between them isn't along any of the orbital**..."

L178：抖动有**空间结构**（低纬站对环状/对角带状分布的站高抖动）。
L147：**贪心最短路使全部连接挤到同一条路径**（纽约↔伦敦 2000×2000 节点），只为约 1–2% 的时延差。

→ **这是与 F1（重配周期）、F8/F18（口径与幸存者偏差）并列的第三条方法学约束**：
任何"负载 → 时延"实验，**必须先扣掉零负载运动性抖动（可达 2.5 倍）**，否则信号被淹没；且**源目的对的选择会系统性决定结论**（1500–3000 km 且非沿轨方向才是高抖动区），而全库论文普遍随机选源目的对、无人讨论这一点。

## F29【第四条时延口径陷阱】时延分辨率与物理尺度差三到四个数量级（WHS8Z44C）

R9 读卡：端到端时延 = $\tau \times$ 时隙数，而 $\tau = 100$ 秒 → **时延分辨率 100 秒**，而 LEO 星地传播时延是**毫秒级**。
主控核验：L66 确认时隙模型存在（"the length of each time slot $t \in \tau$ is $\tau$"），具体 $\tau$ 值在表内（R9 报 100 s）。
→ 与该文自称"最小化服务端到端时延"形成**量级矛盾**。
→ 连同 F8（分母）、F18（幸存者偏差），**"时延口径"已是四篇独立命中**（VFS59FHI / UKEKU5ZG / K7U4TYJN / WHS8Z44C）。

## F30【三处"反复出现却无人做的消融"】（R10 汇总）

1. **2-bit 邻居状态编码**：Y2H4NPLU 自己承认它是传播时延偏大的原因之一（L151 段），**却没做消融**；同族的 YI9G7NR7 沿用同样编码；
2. **奖励权重**：X5Z98UPM 用 4 组共 16 个**手工设定**的奖励权重，无敏感性分析；
3. **Yen k-最短路 k 值**：XM64YRAW 全文未给。

→ 与 B1–B4 批的拆解结论**一致**（"0/34 做过奖励分项消融"）。这是**两条独立路径（读卡 + 拆解）指向同一结论**，可信度高于单一来源。

## F31【一条被两篇独立指认的失败机理】（R10 汇总）

ZIUBKVPZ L137（主控核验）：DQN 在 ε-greedy 探索下**路由环路不可避免**，成因是**四条 ISL 负载完全相同 ⇒ agent 认为所有动作等价** ≈ S85KQ4FC 的"决策队列饱和"。
→ **状态表征的对称性缺陷**（O（观测）分不出动作）+ **决策资源饱和**（动作来不及做）是两条**尚未被合并处理**的线索。
→ 登记为**候选 N4**：把"观测对称性导致的动作等价"作为独立于"资源饱和"的失败原因，二者可分离验证。

## F32【确证·升级 F1】15 秒全局重配置被三方独立测量确认，且**不是负载驱动的**

**三篇独立测量论文，主控逐字核验**：

1. **L63JISQN L57 逐字**（主控核验）：
   > "major changes in latency characteristics **occur every 15 seconds** — specifically, at the 12th, 27th, 42nd, and 57th second past every minute. **Notably, these changes are observed from all our measured locations for all periods of time.**"
   且 R7 读卡记录该文明确：**"these effects were noticed even when our terminals were running well under capacity"** → **该台阶与负载无关**。

2. **NPF75WS5 L211 逐字**（主控核验）：
   > "**Disproving Satellite Handoff Hypothesis.** Previous works have suggested satellite or beam changes at reconfiguration interval boundaries to be the root-cause of network degradation. To investigate this hypothesis, **we deliberately obstructed the field-of-view of our UK terminal**..."
   → 用遮挡实验**证伪了卫星切换假说**（德国+苏格兰两地独立复现）。

3. **P6XJZNQK L172**（主控核验）：把 15 秒与吞吐**恢复时间**挂钩；Starlink 吞吐恢复中位 ~15 s vs 非 Starlink ~5 s；且明确 Starlink 的丢包**不是拥塞信号**（FQ-CoDel + 链路随机丢包）。

**含义（与 F1 合并，升级为确证）**：
> 在真实 Starlink 网络里，**时延与吞吐的主要周期性变化来自全局调度/重配置（15 s 台阶），不是负载**；且已有工作用遮挡实验**否定了卫星切换是成因**。

→ **对本项目的硬约束**：任何"负载 → 时延"的实验，**必须把 15 s 调度周期这一来源分离出去**，否则会把调度台阶误记成负载效应。这与 F1（重配周期）、F28（运动性抖动 2.5 倍）合起来，构成**三个必须扣除的非负载来源**。

## F33【干净口径的排队时延实测锚点】NPF75WS5（主控逐字核验）

L144 逐字：
> "during active downloads, Starlink experiences **≈ 2–4× increased RTTs, reaching almost 400–500 ms**"

**口径为什么干净**（R7 读卡）：基线取 **minRTT**，作者明说它 "not affected by queuing delays" → **这个膨胀量就是排队时延本身**；且上下行不对称（上行 60 分位 ≤100ms，下行 ≈200ms）。
→ **这是全库目前唯一口径干净、可直接引用的"排队时延"实测量**，可作为本项目实验的对照量级。

## F34【两篇领域外文献的入库机制已定位】（R9）

R9 查明 WT839YP7（库代码瘦身）的入库机制：**"library customization" 与 LEO 领域的 "VNF placement / network function" 在检索层面易混淆**。
→ 处置：据此排查检索式；汇总时把这两篇标为"主题外"，不稀释 LEO 路由方向的统计。

## F35【"负载不均"的两个独立成因，现有工作各处理一种】（R9）

- **地理成因**：VFS59FHI（信关站只能布在有限区域 → 回传汇聚拥塞）；
- **算法成因**：W6M3GU7L L147（贪心最短路使全部连接挤同一条路径）+ WFA3CZLP L132（"unbalanced traffic load distribution may lead to network congestion, resulting in a significant increase in average end-to-end delay"）。

→ 与 F26（最短路制造热点）**互为见证**。含义：LEO 负载不均**既有地理成因也有算法成因**，而现有工作**各自只处理一种**。

## F36【"到达率"直接入状态的一篇，但半成品】W5Z39E25（R9 读卡）

把**业务到达率 λ 直接作为状态变量**、三态划分（λ>β 忙 / λ<α 闲 / 中间过渡，L43）；
**写清了"降排队时延 vs 增跳数"的对冲**（L115：绕行后单星排队时延下降，但跳数与排队次数上升、路径变长，**净效应可能时延不降反升**）；
90 分位时延在同负载下跨 **98 ms → 790 ms**（近一个数量级，L126）。
**但**：α、β **从未给定值**（作者自认 L140），且**只测单一负载点**。
→ 含义：**"到达率入状态"有人试过（一篇，且不完整）**，本项目须与它划界；它给出的"对冲"机制（绕行降单跳排队时延但增跳数）是**可直接复用的机理解释**。

## F37【1993 年就写明、至今无人回应】负载**回落**时策略不收敛（47J2H748，主控逐字核验）

**L73 逐字**：
> "When the overall level of network traffic was **raised** during simulation, Q-routing **quickly adapted** its policy to route packets around new bottlenecks. However, when network traffic levels were then **lowered** again, adaptation was **much slower, and never converged on the optimal shortest paths**."

**L88 逐字（更狠）**：
> "Ironically, the 'drawback' of the basic Q-routing algorithm—that it **does no exploration** and no fine-tuning after initially learning a viable policy—**actually leads to improved performance under high load conditions**."

**L79 段（探索污染问题）**：把真实数据包随机发往某方向做探索，会**让网络的拥塞状况变差**——即"**改变了学习器要解决的那个问题本身**"；该文的对策是 full-echo（不发真包、只发问询）。

**含义（对本项目是前置约束，不是可选细节）**：
1. **负载变化是不对称的**：升载适应快、降载适应慢且不收敛。任何"负载变化下的适应性"主张，**必须分别报告升载与降载**，只报升载会系统性高估能力；
2. **探索本身污染被测环境**：在真实网络上做在线学习/探索，会改变要测量的那个负载状态——**这为"离线训练+冻结部署"提供了独立于工程考虑的合法性理由**（本项目 BOUNDARY-TABLE 中"固定训练后部署 vs 在线更新"暂用项，此处有了文献依据）；
3. **实验方法学**：该文负载扫描每点取 **19 次试验的中位数**（L60）——**1993 年的论文就做重复取中位数**，可作本项目统计纪律的对照基准。

**与已有发现的关系**：F1/F28/F32（非负载来源主导）说的是"测量的混杂"；F37 说的是"**被测量对象本身会因学习行为而改变**"。两者合起来意味着：在真实/在线场景研究"负载→时延"，既要扣掉非负载来源，又要保证测量行为不改变被测状态。

## F38【三条跨篇独立印证：负载上升时受害最大的是尾部而非均值】（R1 汇总）

| 篇 | 指标 | 负载效应 |
|---|---|---|
| 39NJWBI7 | 均值 vs CVaR | 均值 8.9 ms，**CVaR₀.₂₅ = 16.0 ms** |
| 36RZKNW5 | 时延方差 | RSFFA 1.62→18.62；随机分配 2.35→**101.97** |
| 2W8BJ7ME | 带宽标准差 | 分流**降低拥塞条数却抬高**剩余带宽标准差，差距随负载扩大 |

→ 与本项目"主指标=到达率+端到端时延"（固定边界）的关系：**时延指标若只报均值，会系统性掩盖负载效应**。这与 F8/F18（口径与幸存者偏差）方向一致但角度不同——**建议实验设计同时报告均值与尾部（P95/P99 或 CVaR）**。

## F39【缺口·两篇互为镜像】形式化最讲究的只测一个负载点，算完整条曲线的却不做学习

- **39NJWBI7（PRIMAL）**：事件驱动半马尔可夫 + CVaR 约束排队时延，**只测一个到达率（10 000 pps）**；
- **4QG5VYHQ**：把**整条 ρ 曲线解析算完**（AoI 对负载呈 **U 形，存在最优 ρ\***），**但不做学习、不做路由**。

→ **"约束/风险感知型 LEO 路由 × 到达率扫描"目前无人做**（R1 判断，主控未逐条复核两篇的扫描范围，引用前须核对）。

## F40【技术教训·影响数据完整性】read-modify-write 会静默丢数据（R1 实测事故）

R1 报告：用 `read` 取文件 → 拼接 → `write` 回写的方式追加读卡时，**read 返回的是截断视图**，导致 write **覆盖掉已写好的 4 张卡、并把 1 张截半**。已用 bash 校验 + edit 锚点插入修复。

**规则（写入通读纪律）**：
1. **禁止用 read→write 回写大文件**，一律用 `edit` 锚点插入；
2. 每次写入后立即用 `wc -l` + `grep -c '^## '` 校验；
3. 该事故此前在 B7 批次也发生过一次（文件被截断）——**同一坑两次，列入必检项**。

## F41【最硬的一类证据：实测证伪同批仿真假设】（AZ72LM9Z vs AF674CSF/AIH4GK37，主控逐字核验）

**实测方（AZ72LM9Z，LEO-Net'25，Roman/HitchHiking）L141 逐字**：
> "Large-scale **clustered outage events occur on a daily basis**. On May 27, **597 outages occurred simultaneously**, each lasting between 70 and 75 seconds—**accounting for 73.5% of all outages that day**. On May 29, we observe two similar clusters... These events suggest **centralized failures**, likely at the satellite link level, that **affect many users at once**."

**被证伪的仿真假设方**：
- **AIH4GK37 L298 逐字（主控核验）**："ISL instability is modeled as discrete link down/up events, **with at most one ISL down at a time** to isolate individual disruptions... we use a **single Pareto distribution** for both down-interval and up-interval durations (shape k=2.5, scale xm=7.2 s, mean 12 s)."
- **AF674CSF（LPIH）L305**：ISL 失效"randomly and independently"，用 Poisson。

**证伪内容（三条）**：
1. **独立性被证伪**：真实是**成簇同时发生**（597 次同时），不是独立随机；
2. **"至多一条失效"被证伪**：真实是**大规模同时失效**；
3. **分布形状被证伪**：真实中断时长有**明确众数区间（50–75 s）**，而 Pareto(k=2.5) 是重尾——**形状假设方向错了**。

**含义（对本项目极重要）**：
> 把链路失效建成独立随机过程，会**系统性低估"同时多链路失效"的概率 → 低估拥塞与丢包的尾部**。
> 而 **"成簇失效在同一时刻把流量挤向剩余链路"，正是负载突变的物理来源**——这是一个**由实测支撑的负载变化机制**，不是我推的。

→ 与 F38（尾部非均值）**独立呼应**：一个从指标角度、一个从事件模型角度，都指向"尾部被系统性低估"。

## F42【作者自己把"负载依赖建模"列为缺口】（AIH4GK37 Future Work，主控核验）

L435 逐字：
> "**Congestion with mixed control/data traffic requires load-dependent costs and transient end-to-end evaluation**... Delay-triggered updates and concurrent events require a richer event model for λ."

→ 该文成本模型**全是常数**，作者自己承认需要"负载依赖成本 + **瞬态端到端评估**"。
→ 与本项目"瞬态窗条件指标"的设计方向**直接一致**，且这是**作者自认**的缺口（不是我推的）。

## F43【三条"测量行为污染被测对象"的证据，构成第二条前置约束】

1. **AZ72LM9Z L73/L98**：**测量强度本身触发被测网络的 ICMP 限速**（朴素方法丢包 50%→79.7%）→ 做负载-时延实验前必须先排除这个混杂；
2. **AF674CSF L437**（主控核验）只统计成功送达的包 → **系统性偏袒丢包率高的协议**（与 F8/F18 同族，此处由作者自曝）；
3. **47J2H748（F37）**：探索行为改变被测网络的拥塞状态。

→ 三条合起来：**"测量/学习行为会改变被测状态"是本项目必须正面处理的第二类前置约束**（第一类是 F1/F28/F32 的非负载来源）。

## F44【反面事实·噪声底】负载完全不变时时延照样剧烈波动（8AYW2Y78 Hypatia）

R3 读卡：换路导致 96→111 ms 的时延变化，**而负载完全没变**。
→ **delay 作为拥塞信号被结构性污染**——这与 F1/F32 的实测证据同向，但这条是在**仿真平台**（Hypatia）里也成立，说明**不是真实网络独有的问题**。

## F45【引用网络已确证：Hypatia 从"论点来源"变成"标准基础设施"】（R3）

- Hypatia(8AYW2Y78) 被本批 4 篇引用：LiR[2]、DB-R[4]、PBAR[10]、Roman-HitchHiking[24]；
- **PBAR 直接把它当仿真基座**（"Our constellation topological state is generated using Hypatia"）；
- 两个课题组主导：**北航组**（LiR/DB-R/LPIH，改造但保留 IP/OSPF 栈）、**UCLA 组**（PBAR + Roman-HitchHiking，设计+测量姊妹篇）；
- 谱系链完整：**Hypatia → ASER → {LPIH, PBAR}**；AJJI57M9(Ekici 2001) 是 ASER 祖先被双引。

→ 意义：**做本项目实验设计时，Hypatia 是既成的基础设施标准**；且北航组的"保留 IP/OSPF 栈"路线与本项目"RL 路由"路线形成明确对照。
