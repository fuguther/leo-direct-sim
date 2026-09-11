# 审查意见 | 证据审查者（Evidence）— card-B3
- 审查时刻: 2026-09-10 21:30:31 +0800
- 实算 sha256（终端 `sha256 -q` card-B3.md）: 28acb6351f00a1d5998095f3217f1fcad2d2376cb185ebf6d12c5f041323e2bc
- cand_id: cc72be0cbef（台账文件指纹前缀 sha256:28acb6351f00a1d5 与实算一致 ✓；台账 content_hash=haa9dadab679e 为 canonical 字段哈希，按禁读台账规则未复算，仅照录）
- 证据入口: LITERATURE/notes/raw 6 份；LITERATURE/papers 本地 PDF 5 份全文抽查（PyMuPDF 提取；STARTCAP-2024 无本地 PDF）；LITERATURE/SOURCES.csv
- 判定语义: 相似度=线索非结论；BLOCK=有依据否定 / INPUT_INSUFFICIENT=未能检查 / NOT_APPLICABLE=不适用；本轮=流程验证，非价值裁决

## 一、【原文事实】逐条核对（笔记 + 本地 PDF 抽查）
1. 【支持】LOZANO 28 维状态无星历寿命字段：原文逐字命中 "28 fields: 16 for the neighbors' congestion queue levels, 8 for the neighbour coordinates, 2 for the current coordinates, and 2 for the packet destination..."，枚举内无任何剩余寿命/星历字段。卡§1"均已核原文"属实。
2. 【支持】LOZANO §III 不可用编码：原文逐字命中 "If a link to a neighbour is unavailable, then the congestion levels of all its queue lengths are set to infinite and its coordinates to 0"。卡内推论"断了才看见/防不了刚选完就断"与原文一致：该编码是对已发生不可用的反应式编码；另原文奖励项 ru（不可用链路动作惩罚）同为事后性，全文未见预测性使用。
3. 【支持】LOZANO eq.(13) 模型继承：原文命中 "Qi−1(θ) ← ½(Qi(θ)+Qi−1(θ)) (13)"，并明言发给 "moving towards i's former position" 的相邻星、后继 "inherits the learned traffic flow patterns"。指针精确；细节：原式为均值混合，非整网直传。
4. 【支持】LOZANO 15s 快照 + Fig.9 + "most of the time"：Fig.9 题注逐字命中 "Satellite positions were updated every 15 seconds ... causing the path to change over time and fluctuations in the latency"；正文引语 "most of the time" 逐字命中。三项指针全部精确。注意：原文措辞为"位置每 15s 更新"，卡写"拓扑按 15s 快照更新"属合理转述（拓扑由位置+greedy matching 派生，15s 内冻结）。
5. 【支持】CHOU eq.(3)：原文命中 "si(t) = Qi(t), {Dij(t)}, xi(t) ∈Rd (3)"；xi 为拓扑特征（相对位置/连通指示），无寿命字段。公式编号属实。
6. 【支持】LIAQ §IV 状态：PDF 命中状态枚举（本星坐标+4 邻居坐标+各邻居队列+目的地坐标）；韧性分为失效概率/队列复合分（笔记深读记录），非星历剩余寿命。"无寿命字段"成立。
7. 【支持】HE 观测无年龄语义：原文命中 "O ... includes packet state and local node/neighbor statistics"；动作=4 出向 ISL（NSWE），无 wait/GSL 动作。
8. 【INPUT_INSUFFICIENT】"ISL 切换按星历完全可预测"（卡§1）：六份笔记与 LOZANO 原文均无此断言（LOZANO 仿真仅 15s 位置更新+greedy matching）。属领域常识性前提，本证据入口不可核 → 建议降格为"假设"或补星历侧锚点。

## 二、【实测，经笔记】断言（标注 + 承重评估）
9. 【待回原文·承重=高】STARTCAP "GSL≈15s 周期中断+突发丢包+传输层误判拥塞"：无本地 PDF，仅摘要级笔记，笔记逐字支撑三要素；出处 APNet'24 已由 SOURCES.csv 证实。风险：笔记自身警告"固定 15s 可能只是单终端样本特征"未被卡继承；该断言是卡内唯一的"切换期丢包"实测锚 → 回原文须核 15s 的测量覆盖面。
10. 【待回原文·承重=中】IZHIKEVICH "15s 倍数持续尖峰、与拥塞/切换不完全对应"：按规程标注；本人已用本地 PDF 抽查，关键句逐字命中（"spikes occur in multiples of 15 second—aligning with Starlink's reported satellite reconfiguration period"；"not due to congestion ... no packet drop"；"satellite switches are not the ultimate cause behind latency spikes"）→ 经本次抽查可解除待回原文。两点降格：15s 周期在原文系引 [10] 的 "reported" 周期，非本文独立测量；全文只测时延、无丢包/吞吐 → 不能直接承重"交付坑"。SIGMETRICS'24 出处已由 SOURCES.csv 证实。
11. 【支持但弱】"运营商重路由动作引发尖峰"：原文为案例级间接证据（尼日利亚 ISL 远端中继、游艇 42% 时间被重路由），"工程师确认"系对话式证据（笔记危险信号已注明）→ 卡引用该子断言时应带"案例级"限定。

## 三、竞争解释与比较公平性
12. 【认真对待 ✓】卡§2 明列三大竞争解释且均与证据相符：(a) 模型预期已吸收可预报性——与 eq.(13) 机制核对一致；(b) 损失在传输/接入层——与 STARTCAP（GSL/传输层）、IZHIKEVICH（接入段为主）证据一致；(c) "拥塞=∞"编码隐式避开断链——已核原文，卡正确指出其事后性。
13. 【公平性 ✓】卡§5 主动引入对己不利的替代解释（"下一快照拓扑入观测≈寿命字段、增量薄""固定规则可拿走大部分收益"），并给出可证伪的淘汰条件与廉价核验——比较框架公平，无选择性引用迹象。
14. 【层级错位·修订项】实测锚（STARTCAP GSL 15s 中断、IZHIKEVICH 接入段尖峰）都在 GSL/接入层；拟议改动在 ISL 观测/动作层；"ISL 在途包撞上将死链路→交付坑"目前纯推演，无任何数字支撑。卡§7"切换窗口 vs 非窗口丢包统计"正是对该缺口的证伪动作，建议升格为§3 拟议改动的前置门槛。
15. 【INPUT_INSUFFICIENT】近邻指针 He20/Zha26l、Jin26、Yan25b：本证据入口不可核；卡已自标 Jin26/Yan25b"未核"，He20/Zha26l 未标 → 建议补标。BlockFlex（ARXIV-2512.09453）、SKYLINK（2509.08455）、2601.21914 均在 SOURCES.csv 在案，"虚拟覆盖/架构层、链路管理"定性与标题相符。

## 四、结论
16. 总判定：**可信**（线索级候选卡，流程验证通过）——未发现任何 BLOCK 级证据反驳；承重断言经原文抽查全部命中，指针精确度（§III 编码/eq.(13)/Fig.9/eq.(3)/15s/"most of the time"）为本次抽查最高档。
17. 修订项（均属"证据不足"而非"证据反驳"）：(a) 第 8 条补锚或降格"完全可预测"；(b) 第 9 条继承 STARTCAP 的 15s 非普适警告；(c) 第 10 条将 15s 写明"对齐已报道周期"；(d) 第 14 条把切换窗口丢包统计设为前置；(e) 第 15 条补标 He20/Zha26l"未核"；(f) 卡§2 将推论（"可预报性的唯一用点=模型继承"）与原文事实同列一条，建议分层标注（该"唯一"在"观测/动作层无寿命字段"前提下成立，对原文全文未穷尽）。
18. 流程声明：本次审查未读取 out/**、他人 .worktrees 产物、COLDSTART-*、00-READING-QUEUE.md、任何候选台账、KNOWLEDGE-MAP.md、ANALYSIS/**；除本意见文件外未写入任何路径。
