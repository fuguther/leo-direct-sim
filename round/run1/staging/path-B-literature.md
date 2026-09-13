# Path-B｜候选研究问题草图（charter：文献实际行为）——第1轮生成器产出

- 生成：冷启动生成器，round1/staging。研究目标指标：到达率（成功送达比例）与端到端时延。
- 知识来源：LITERATURE/SOURCES.csv、LITERATURE/notes/raw/*.md（41 篇）、round/knowledge/NEUTRAL-KNOWLEDGE-VIEW.md（程序化切片）、LITERATURE/papers/*.pdf 本地核对、Undermind 定向补查（search_papers×2 + get_paper_info×1）、web_search。
- 防火墙声明：未读取 out/、round/（知识视图切片外）、notes/ 下禁读清单（COLDSTART/READING-QUEUE/FETCH-LIST/related-work-notes/KNOWLEDGE-MAP）、ANALYSIS/、PAPER/、CODE/ 等禁路径；SOURCES.csv 中指向 LITERATURE/notes/related-work-notes/ 的本地路径一律未打开。未撞见任何"本项目旧实验/旧候选"段落。
- 阅读台账：浏览（读 raw 笔记）13 篇 = RAN/LOZANO/DONG/CHOU/HE/LIAQ/WEIL/IZHIKEVICH/STARTCAP/ZHOU/CHEN-TMIX/SONG/TALEB；精读（本次亲自回原文 pypdf 抽取+定点核对）4 篇 = LOZANO-2025、HE-2025-PRIMAL、WEIL-2024、LIAQ-2026；CHOU-2026 本地 PDF 截断损坏核对未完成，公式转引笔记深读记录（逐处声明）。notes/raw 无笔记论文占比：0/13 = 0%。
- 环境限制：本会话 web_fetch 对 arxiv.org / ar5iv.labs.arxiv.org / export.arxiv.org / elib.dlr.de 均被"非公网 IP"DNS 策略拒绝；CHOU/Rot24/Liu26 原文细节只能依赖笔记深读与 Undermind 摘要，逐处标注。
- 4 张卡，不排序、不推荐。每卡钉住：决策时刻+信息条件+机制假设；每卡挂至少一篇具体论文（身份+定位）。

---

## 卡B1｜邻居状态"刷新合同"：新鲜度×量化开销×负载的相图

**1) 场景与可观察现象**
- 决策时刻：逐包转发时刻 t，卫星 i 基于本星队列+一跳邻居队列/拥塞特征选下一跳。LOZANO-2025 状态为 28 字段向量，其中 16 个是邻居拥塞队列级。【原文事实】（Lozano-Cuadra, Soret, Leyva-Mayorga, Popovski, "Continual Deep Reinforcement Learning for Decentralized Satellite Routing", IEEE TCOM 73(10):8996-9012, 2025；本次 PDF 全文核对原句："a vector of 28 fields: 16 for the neighbors' congestion queue levels, 8 for the neighbour coordinates, 2 for the current coordinates, and 2 for the packet destination"）。
- 信息条件：邻居特征是上一次状态交换/刷新时刻的快照，信息年龄 Δ = 刷新周期 + 传播与处理时延。Δ 在各论文中是隐式常量：LOZANO 状态每步即时可得（全文检索 age/stale 无命中——pypdf 抽取事实）；WEIL-2024 消息每环境步刷新一轮（arXiv:2402.05027 §3.2）；HE-2025-PRIMAL 事件驱动异步但观测无时间戳/年龄语义（arXiv:2510.27506 §III）。
- 日志/仿真观察：记录"决策所用邻居队列值 vs 决策时刻真实值"的偏差分布；偏差与错选率、下游丢包率关联；扫描刷新周期 Δ×负载，得到到达率/时延对 Δ 的曲线（相图）。

**2) 困难与原因假设**
- 【原文事实】WEIL-2024 表2（Weil, Bao, Abboud, Meuser, AAMAS 2024, arXiv:2402.05027；本次 PDF 核对）：无带宽限制下 ShortestPath/DQN/DQNR/CommNet/DGN 五种方法指标完全相同（reward 2.26±0.0、delay 4.39±0.0、throughput 4.52±0.0）——无拥塞时邻居状态信息端到端价值为零；带宽受限后学习方法才在 3 张测试图中 1 张胜出。
- 【原文事实】LOZANO-2025 Sec VI（本次 PDF 核对）：低拥塞下 MA-DRL 与全知最短路的 50/90/95 百分位差距仅 1.7/3/9.1 ms；改道增益只发生在拥塞场景——16 个邻居拥塞值在重载合同下即可追平 genie 最短路。
- 【作者解释】Liu, Liu, Xiao, Feng, Zhou, Jiang, "Distributed Routing for LEO Satellite Networks: A MADRL Approach With State Information Lag"（TAP-DAR），IEEE TCCN 2026, pp.11116-11130（Undermind 摘要，原文未读）："large inter-satellite propagation delays lead to severe state information lag in agent interactions, giving rise to decision biases"；用星历+队列预测补偿，报告时延最高 -16.16%、丢包率平均 -30%。
- 机制假设【推演】：Δ 过大→多上游节点同追一个"陈旧空闲"邻居（羊群/振荡）→时延增益转化为丢包；Δ 过小→状态交换流量挤占业务容量→时延/丢包上升。相图存在随负载移动的最优 Δ；四篇锚点论文各固定一档 Δ，无一报告性能对 Δ 的敏感度。
- 竞争解释：(a) ISL 传播时延 ms 级远小于队列动态时间常数，真实损伤可忽略，起作用的是刷新周期与突发到达的对齐而非传播时延本身；(b) TAP-DAR 的预测补偿已把该问题解决，残余敏感度不构成研究空间。

**3) 拟议改动**
- 改观测+更新方式：把邻居状态刷新周期 Δ 与每字段量化位数从隐式常量升格为可调实验合同，扫 (Δ, 量化位数, 负载) 三维；对比"直接用陈旧值 / 年龄修正的队列预测值"两种观测。
- 影响机制：若相图存在且最优 Δ 随负载移动，则固定 Δ 的现役方法在部分负载带把到达率损失在羊群丢包上、在另一部分负载带把时延损失在状态交换开销上。

**4) 初步近邻**：TAP-DAR（Liu et al. 2026，预测补偿——直接碰撞，须先读原文判断其是否已含 Δ 敏感度分析）；WEIL-2024（记忆缓解陈旧观测，刷新间隔隐式固定）；LOZANO-2025（log 压缩拥塞编码，固定刷新）；GraphPR（Ran et al., IEEE TVT 74(3), 2025，逐包一跳信息交换，通信量化缺失——摘要级笔记，未核）。

**5) 简单替代**
- 固定规则：ELB/TLR 的阈值信令同样受陈旧度影响，调阈值能吃掉部分增益，但没有"开销-新鲜度"权衡概念。
- 成熟 RL 合理调参：降学习率/换目标网节奏不触及观测陈旧。
- 给原方法加同等信息：TAP-DAR 即此路（预测入状态）；猜想其解决"补偿"侧大半，但"花多少钱买多新的信息"的标定问题仍在。

**6) 立即淘汰条件**：合理 Δ 范围（0–200ms）内到达率/时延曲线平坦（对 Δ 不敏感）；或 TAP-DAR 原文已含同型相图/敏感度分析。

**7) 下一项廉价核验**：在自研/开源仿真器给邻居队列观测注入人为延迟 Δ，扫 Δ×负载网格看交付率是否出现悬崖；半天~一天级。

**8) 来源指针**：LOZANO-2025 PDF 全文（状态 28 字段句，Sec III 状态定义；1.7/3/9.1 ms 在 Sec VI）；WEIL-2024 表2（arXiv:2402.05027，本次核对）；HE-2025-PRIMAL §III（arXiv:2510.27506）；Liu et al. 2026 TCCN pp.11116-11130（Undermind 摘要，未核）；RAN-2025-GRAPHPR（TVT 74(3):5229，摘要级）。

---


## 卡B2｜丢弃事件的跨节点归因断裂：到达率在奖励合同里"没人负责"

**1) 场景与可观察现象**
- 决策时刻：卫星 i 在 t 把包转发给邻居 j；j 队列近满，包随后在 j（或更下游、或 TTL 超时）被丢。
- 信息条件：决策者观测不到"这个包最终是否送达"；丢弃发生在别的节点、别的时刻，不回传给 i。
- 日志/仿真观察：按丢弃位置分桶（源/第1跳/中间/出口）统计路由决策可影响的丢弃占比；对比各方法训练奖励项与实际交付率的相关性；同负载下比较"队列代理奖励"与"丢弃反传奖励"的交付-时延前沿。

**2) 困难与原因假设**
- 【原文事实】HE-2025-PRIMAL 表I（He, Vu, He, Fan, Chatzinotas, Ottersten, "PRIMAL", arXiv:2510.27506；本次 PDF 核对）：SPF 丢包 84.8%、吞吐 27.0 Mbps；MADQN/PRIMAL-Avg/PRIMAL-CVaR 丢包全部 0.00%——学习方法之间交付零差异，收益全落在时延（排队 17.6→4.8 ms，-72.7%）。拥塞是工程化的：ISL 仅 50 Mbps、GSL 1000 Mbps、节点/链路缓冲各 16 Mbit（§IV-A 原文核对）。
- 【原文事实】DONG-2023（Dong, Song, Zhang et al., "DRL-Based Load-Balancing Routing Scheme for 6G SAGIN", Remote Sensing 15(11):2801, 2023；笔记深读记录）：收益指标全部是路径队列统计，通篇无交付/丢包指标。
- 【原文事实→口径异常】CHOU-2026（Chou, Wang, Chen, Wang, arXiv:2605.02413；笔记深读记录，本地 PDF 损坏未复现）：240 Mbps 负载下吞吐≈210 Mbps（≈87.5% 交付）与同节丢包最高 46.81% 互相矛盾——到达率口径在文献内部就不可靠。
- 【作者解释】LOZANO-2025 奖励 r_i = r_q(队列占用) + r_d(逼近日的) + r⋆(事件项：环路惩罚/GSL 直达奖励/不可用动作惩罚；eq.8 结构本次核对；量值 +50/-5 录自笔记，本次抽取未复现，未核实)——交付只有终点奖励项，路径级丢弃归因未展开。
- 机制假设【推演】：丢弃责任分散在路径上多个决策者；各 agent 以队列/占用为代理最优化自身 → 系统性"把满队列邻居踢给下游"或"囤积"，到达率在中等负载带劣于可达值；队列代理与交付在特定缓冲/TTL 配置下解耦。
- 竞争解释：(a) 丢弃主要发生在源/接入接纳环节，路由端归因改善不动到达率；(b) 这是 Pareto 权重问题而非归因问题——加丢弃惩罚只会挪前沿，不产生新交付。

**3) 拟议改动**
- 改奖励+更新方式：把丢弃/超时事件沿包路径反传给途中决策者（multi-step return 或路径级信用分配），或加"下游丢弃风险预测"辅助头；对照纯队列代理奖励。
- 影响机制：决策者把"我的转发导致的下游丢弃风险"计入自身价值 → 中负载带丢包下降、时延不显著变差。

**4) 初步近邻**：HE-2025-PRIMAL（送达为主奖励+CVaR 代价，但其合同丢包恒 0，无法检验归因）；Roth, Hegde, Delamotte, Knopp, "Shaping Rewards, Shaping Routes: On Multi-Agent Deep Q-Networks for Routing in Satellite Constellation Networks", arXiv:2408.01979, 2024（奖励塑形对路由行为——细节未核，须先读）；CHEN-2025-TMIX（Chen, Ji, Wu et al., IEEE IoT-J 12(11), 2025，投递率 +5.4% 仅在 18% ISL 失效场景报告——摘要级，未核）。

**5) 简单替代**
- 固定规则：无对应物（启发式不做信用分配）。
- 成熟 RL 合理调参：奖励权重扫描可部分对齐交付-时延，但不解决"丢弃不回传"。
- 给原方法加同等信息：把 TTL 余量/下游缓存占用入状态——补了观测，仍没补归因。

**6) 立即淘汰条件**：丢弃分桶显示路由可影响丢弃（中间跳）占比 <5%；或丢弃反传奖励在负载扫描下到达率改善不超噪声。

**7) 下一项廉价核验**：现有仿真加丢弃位置日志，按桶统计占比；半天级。

**8) 来源指针**：HE-2025-PRIMAL 表I+§IV-A（本次核对）；LOZANO-2025 奖励定义（Sec III/eq.8，结构核对）；DONG-2023（笔记深读，MDPI 开放获取）；CHOU-2026 §IV-C/IV-D（笔记深读，未复现）；Roth et al. 2024（arXiv:2408.01979，Undermind/web_search 元数据，未核）。

---

## 卡B3｜队列感知路由的隐式改道阈值：负载体制迁移时的失标定

**1) 场景与可观察现象**
- 决策时刻：负载从轻爬向重（日模式/突发爬坡）过程中，队列感知策略须决定"何时离开最短路绕行"；切换点隐含在 Q 值差里，标定由训练负载合同决定。
- 信息条件：观测=队列/链路负载瞬时值。与卡B1不同：不是信息旧，而是价值函数在训练分布外的队列状态区间外推。
- 日志/仿真观察：负载扫描下画交付率/时延曲线，找"RL 恰在体制边界劣于两个基线"的窗口；对 Q 差做敏感度分析得到隐式阈值随负载的漂移轨迹。

**2) 困难与原因假设**
- 【原文事实·四篇拼图】(1) LOZANO-2025：增益只在拥塞场景，低载 50th 差 1.7 ms≈无差异（本次核对）；(2) HE-2025-PRIMAL：把 ISL 压到 50 Mbps 造出 SPF 84.8% 丢包的极端合同，才有排队时延 -72.7%（本次核对）；(3) LIAQ-2026（Liaq, Tajeri, Hu, "Queue-Aware and Resilient Routing in LEO Satellite Networks Using MARL", arXiv:2605.04448；本次 PDF 核对原句）："To ensure a fair comparison and isolate latency performance, the queue capacity in the simulation is set to 1 Gb/s, effectively preventing queue overflow and allowing Dijkstra's algorithm to operate under near-ideal conditions"，且摘要自认 "Dijkstra achieves the lowest end-to-end latency under ideal conditions"——卖 queue-aware 的论文在自己的时延比较里主动关掉了队列溢出；(4) WEIL-2024：无带宽限制学习方法=SP 完全相同，带宽受限才分出差异（本次核对）。
- 【作者解释】LIAQ 把防溢出设为"公平比较"手段；LOZANO 把拥塞场景设为增益适用域。
- 机制假设【推演】：队列感知路由的价值存在一个窄负载带；带边界处隐式改道阈值失标定→过早绕行（时延↑）或过晚绕行（丢包↑）。各论文只测带内或带外，无一测量跨体制迁移时策略的阈值行为。
- 竞争解释：(a) 调好阈值的显式启发式（TALEB-2009 ELB、SONG-2014 TLR）在体制切换时同样劣化，RL 不比它们差→无空间；(b) ZHOU-2026-DTAR（Zhou, Luo, Ran, arXiv:2604.12382；笔记深读）已用 surge 场景覆盖——但其 normal/surge 场景无交付量化收益、仅 fault 场景有 pp 级收益，恰好佐证"窄带"而非否定。

**3) 拟议改动**
- 改训练合同+评估协议：负载课程/随机化训练；把隐式阈值显式化（Q 差敏感度分析）并检验跨体制稳定性；对照 ELB/TLR 显式阈值的切换响应速度。
- 影响机制：若失标定成立，课程训练应把交付率-负载曲线的"塌陷窗"移走，同时不牺牲带内时延。

**4) 初步近邻**：ZHOU-2026-DTAR（surge/fault 场景，域级粒度）；Roth et al. 2024（奖励塑形影响路由行为，未核）；TALEB-2009-ELB（ToN 17(1)，显式阈值经典，超出时间窗的例外基线，笔记未获原文摘要）；SONG-2014-TLR（TWC 13(6)，笔记摘要级）；通用 OOD/课程学习在 LEO 路由内的应用（未核）。

**5) 简单替代**
- 固定规则：ELB/TLR 阈值调参可覆盖部分带宽，但阈值静态、不随负载合同迁移。
- 成熟 RL 合理调参：多负载混合训练+多 seed——猜测能消除部分失标定，恰是"合理调参能解决多少"的对照点。
- 给原方法加同等信息：把当前负载数率本身作为状态特征喂给策略——对症的信息增补，竞争力最强，本卡必须赛过它。

**6) 立即淘汰条件**：负载扫描下 RL 交付/时延曲线与 ELB/TLR 同步劣化、无阈值错位证据；或"负载数率入状态"后差异消失（卡并入观测合同问题）。

**7) 下一项廉价核验**：训练于单一负载，测试 5 点负载扫描 ×（RL、ELB、SPF），画交付率-负载曲线找塌陷窗；两天级；LOZANO 仿真器开源（SatCom-TELMA/MA-DRL_Routing_Simulator）可改。

**8) 来源指针**：LOZANO-2025 Sec VI（核对）；HE-2025-PRIMAL 表I/§IV-A（核对）；LIAQ-2026 摘要+§V（核对原句）；WEIL-2024 表2/§5.2（核对）；ZHOU-2026-DTAR（笔记深读，arXiv:2604.12382）；TALEB-2009（未核原文）；SONG-2014（笔记摘要级）。

---


## 卡B4｜链路剩余寿命：切换可预测性在路由观测合同中的缺位

**1) 场景与可观察现象**
- 决策时刻：时刻 t 包在卫星 i 的出链路 l 上排队/转发，l 将在 τ 后因切换/重配消失；i 决定是否把"注定赶不上"的包提前改道。
- 信息条件：τ 由轨道动力学确定可预测（星历可算）；现役 RL 路由状态向量只含当前连通/队列/时延，无 time-to-link-change 特征。
- 日志/仿真观察：统计"排队时延 > 链路剩余寿命"的包占比随负载的曲线；切换边界前后到达率/时延的瞬态剖面。

**2) 困难与原因假设**
- 【原文事实】STARTCAP-2024（Jiang, Zhang, Hu, Cui, Zhang, "StarTCP", ACM APNet 2024；笔记+Sources 元数据）：Starlink 实测 ~15s 周期 GSL 切换造成突发丢包，TCP 误判为拥塞；方案=预测切换主动 stall——可预测性已被消费的先例，但在传输层。
- 【原文事实】IZHIKEVICH-2024（SIGMETRICS 2024，arXiv:2306.07469；笔记深读）：持续时延尖峰呈 15s 倍数、与切换/卫星位置/拥塞均无关，归因于运营方重路由——真实网络状态里有仿真不建模的不可见运营方动作。
- 【原文事实】仿真合同拓扑更新粒度相差 150 倍：LOZANO 位置更新 15 s；PRIMAL 100 ms（均本次 PDF 核对）——切换语义无统一合同。
- 机制假设【推演】：决策不消费剩余寿命 → epoch 边界附近"排队时延超过链路剩余寿命"的包必遇重配：被丢（到达率损失）或事后重路由绕远（时延损失）；策略条件化于 τ 可提前改道兑现可预测性。
- 竞争解释：(a) ISL 拓扑准静态，切换集中在 GSL 段，星上路由影响小（IZHIKEVICH：ISL 依赖是低频边缘事件）；(b) 链路/传输层已解决（STARTCAP stall、GANNON-2024 make-before-break），路由层属重复建设；(c) 快照式仿真的切换语义（队列保留）本就不产生该损失——卡可能是仿真人造物。

**3) 拟议改动**
- 改观测+动作：状态加 time-to-link-change 通道（星历确定性可算）；或动作屏蔽"剩余寿命 < 单跳转发时延+残余队列清空时间"的出链路。
- 影响机制：避免对"注定赶不上"链路的承诺 → 到达率↑（少丢）、事后绕行↓（时延↓）。

**4) 初步近邻**：路由层直接同构工作未检索到（Undermind 定向检索：最近邻为 Yan et al. 2025 切换感知 DRL 拥塞控制——传输侧；Kim et al. 2026 故障韧性路由；均未核原文）；STARTCAP/GANNON-2024 为传输/链路层先例。

**5) 简单替代**
- 固定规则："切换前 X 秒冻结受影响链路"的启发式即可实现同机制——若它就够，卡降级为基线比较。
- 成熟 RL 合理调参：不给该信息时策略学不出星历（不可从队列观测恢复），调参无效。
- 给原方法加同等信息：把星历/切换调度喂给 agent 即本卡改法本身；仿真器侧多数已内置切换调度，缺的是交给 agent。

**6) 立即淘汰条件**："排队时延>剩余寿命"包占比在合理负载下 <1%；或加 τ 特征后到达率/时延无可测差异；或确认传输层方案已把该瞬态吃干净。

**7) 下一项廉价核验**：自研仿真加该统计量，跑一次负载扫描；一天级。

**8) 来源指针**：STARTCAP-2024（APNet 2024，笔记）；IZHIKEVICH-2024（笔记深读，arXiv:2306.07469）；LOZANO-2025/HE-2025-PRIMAL 实验合同参数（本次核对）；GANNON-2024（IEEE ICC 2024，Sources 元数据，未核）；Yan25b（Undermind 检索命中，未核）。

---

## 交叉备注与最大不确定点

1. **卡B1 与 TAP-DAR（Liu et al. 2026, IEEE TCCN pp.11116-11130）的碰撞深度未知**：仅读到摘要；若其正文已含 Δ 敏感度/损伤曲线，卡B1 应淘汰或收缩为"开销-新鲜度权衡"。本环境无法访问 arXiv/IEEE 原文（web_fetch 被 DNS 策略拒绝），需有外网权限的一轮补读。
2. **卡B2 依赖 Roth et al. 2024（arXiv:2408.01979）细节未核**：若其已系统做过"奖励塑形→交付/丢包行为"，卡B2 的归因主张须重新定位。
3. **卡B4 三重竞争解释并存且机制占比从未被测量**：任何一档成立即淘汰。
4. CHOU-2026 的口径矛盾数字（吞吐 vs 丢包）本次未回原文复现（本地 PDF 损坏+外网被拒）；CHU-2023（Chu, Cheng, Zhu, Electronics Letters 2023，奖励=距离+next-hop AoI+队列增长率）是"AoI 入奖励"先例，本次仅元数据级，卡B1/B2 若推进须补读。
5. Undermind 检索另提示两篇 SOURCES.csv 未收录工作（Din23 "Fast-Convergence RL for Routing in LEO"；Wu24 "Throughput and Link Utilization Improvement"），未读；若开卡应纳入近邻清单。

