# 证据审查意见（角色：证据）｜run1 批次：F1 + B3 + L1

> 实算 sha256：
> - draft-F1-deepened.md = 108099c19cbc20bc694ed49ec1f83dc0f7d4d712bd6a0bf45344f0c6c600bb1e
> - draft-B3-deepened.md = cc45f7f8fcc948c675195be59c66f8db62e89e9dd5f8c831625464c858239932
> - card-L1-lifetime.md  = bd31b6033692ee756bed210bbf7bc334ebc6f9fa2b0784abe757c89e88820495
> 证据入口：LITERATURE/notes/raw（14 篇笔记逐条比对）、LOZANO/CHOU PDF pdftotext 逐字核、SOURCES.csv、NEUTRAL-KNOWLEDGE-VIEW、leo_sim 代码、Undermind×2（配额用尽）、arXiv API。机械检查：BLOCK 无；TAP-DAR/Yan25b 类库外锚点 = INPUT_INSUFFICIENT（草案自标一致）。

## 总结论
- **F1：需修订**（证据标注准确率整体高，但 TAP-DAR 经外部核实为真实直接对手，空白类表述须立即收窄；另 2 处标签错位）。
- **B3：可信**（承重断言全部有原文支持，1 处措辞夸强）。竞争解释与公平性处理为三稿最佳。
- **L1：需修订（轻）**（库内锚点全部核实；2 条库内竞争证据未纳入；库外数字不得承重）。

## 重大发现（跨三稿，最高优先）
[M1] **TAP-DAR 已确认存在且摘要即显示与 F1 核心高度重叠**。Undermind 核得：Weidan Liu et al., "Distributed Routing for LEO Satellite Networks: A MADRL Approach With State Information Lag", IEEE TCCN 2026, pp.11116-11130, DOI:10.1109/TCCN.2026.3720213。摘要要点：显式建模星间传播时延导致的 state information lag；用**星历数据+队列预测**做时延补偿生成近实时邻居状态估计；**temporal reliability 多头注意力**聚合异步邻居状态；E2E -16.16%、丢包 ~-30%、吞吐 +19.41%、较全局泛洪开销 -90%。
  → F1 的第一淘汰条件从"假设风险"变为"现实对手"：全文核读必须执行；"AoI-of-state 空白/敏感度从未被报告"须收窄为"不含 TAP-DAR 的现役方法"。摘要未见受控 Δ 敏感度相图与信息阶梯负对照，F1 层①或仍有空间，但只能由全文核读裁决——**存在 ≠ 覆盖**，条件/机制比对未完成前不下淘汰结论。
  → L1 交叉影响：TAP-DAR 已把星历数据放进路由决策管线，L1"可预报性被闲置"类跨文献表述须对 TAP-DAR 开窗（其"唯一用点=eq.(13)"限定仅覆盖 LOZANO 一篇）。

## F1 逐条
[F1-1] 支持。LOZANO 28 字段/16 值 log 拥塞编码、每步即时可得、Q 未建模年龄（LOZANO 笔记 L12/L16 逐字）；PRIMAL 观测无年龄语义（HE 笔记 L11/L15）；CHOU/DONG/HAN 零龄（CHOU L14、DONG L13、HAN L13）。"多篇独立深读复现空白"成立（LIAQ L14 同）。
[F1-2] 支持。PRIMAL 表 I 学习算法丢包≈0.00%、排队 17.6→4.8ms(-72.7%)、E2E≈60ms(61.5)、ISL 50Mbps/缓冲 16Mbit/GSL 20×、SPF 丢包 84.8%（HE 笔记 L13-15）。F1 将 SPF 84.8% 正确用作"差异空间可被合同造出/造没"论据，且 HE 笔记 L18 自标"基线崩溃而非公平对照"——草案未犯基线崩溃误用。
[F1-3] **不支持（标签错位）**。L16"600km 邻星单向传播约 2–10ms"标【原文事实】，但库内 notes/PDF/NKV 无任何传播时延数字；该值只能由几何推出（600km 是高度非星间距；面内邻星 ~2000km→~7ms、面间 ~600km→~2ms），应改标【推演】。数值本身合理，杀手①论证不受影响，但承重位置标签必须改。
[F1-4] 支持（一处类名错误）。control.py 实为 **CacheEntry**（L14）携带 generated_at/received_at/ttl_s/hops，无 ControlEntry 类——【代码事实】引用字段全对、类名错，小问题须改。control_broadcast_children（routing.py L38）、capacity 首跳自观测/远端缓存/未知记 inf（L13-15/L270 注释"unknown queue state is not assumed free"）、TensorflowDDQN+target_update_interval（learning.py L246/L481）均核实。
[F1-5] 支持。info_ladder_tiny 的 field_age 级、fixed_age_s 负对照原语、模块自述"does not train an agent and does not estimate an algorithm effect"（docstring+tests L117-129）逐字命中；草案"扩展进学习管线属待做工程"的限定正确。
[F1-6] 支持。NGAT 调度状态含 A_u(t) 但年龄是优化目标（NGAT 笔记 L16）；Yates Age Difference/Debt 局部新鲜度入调度决策、数据更新龄（ARXIV-2111.09217 L9-12）。"邻近但不同物，不构成无先例"的鉴别与笔记一致。
[F1-7] 支持但留意强度。SONG-TLR"防死循环防守机制"在库（L3）；"已自证分布式贪心改道易乒乓"是笔记作者的解释性推断，草案已自降为"弱锚"——可接受，正式引用时须写成"作者意识到"而非"已证明"。
[F1-8] 已核实缺失=处理正确。tao25 flapping 库内零命中（grep 全库），降级处理正确；Nie25/Hua25b 不在库、层③挂起不背书——正确；WEIL 隐式年龄旋钮、无 age↔性能实验（WEIL L24）支持。
[F1-9] 信息条件/公平性：层②同等信息对照（shuffle/常数替换）设计直接对应平台原语，公平；层①"只有测量价值、无方法价值须如实陈述"的自我限定诚实。杀手①②③均给出可测判别结构而非口头排除——竞争解释被认真对待。

## B3 逐条
[B3-1] 支持。四锚逐字核：LOZANO 低载 50th 差 1.7ms（L14/16）；HE 50Mbps 极端合同/SPF 84.8%/-72.7%（L13-15）；LIAQ 队容 1Gb/s"隔离排队"+摘要自认 Dijkstra 理想时延最低（L3/L14）；LOZANO 默认 ℓ=1 仅 8 网关实验 ℓ=0.5（L14）；HE GSL 比 ISL 快 20×（L15）。
[B3-2] **轻微夸强（小问题）**。L10 称 WEIL"无带宽限制时各方法指标完全相同"——笔记原文为 Ours* 仅追平 SP（reward 1.74 vs 1.77）、"DQN 与 DGN 几乎无差"、"effect of communication is very small"（WEIL L24）。建议改"几乎无差/仅追平"，避免被回原文时抓字面。
[B3-3] 支持。ZHOU-DTAR 288 星(12×24)/18 域/GAT+action-masked PPO/normal,surge,fault 三合同/fault 成功率 +9.25pp vs Dijkstra/normal,surge 只报 CV 与时延无交付量化/域级粒度错位（ZHOU 笔记 L14-16 逐字）。作"窄带佐证而非否定"的使用方式与笔记证据强度匹配。
[B3-4] 支持。SatCom-TELMA 155★活跃无 LICENSE（LOZANO L3）；E0 负载扫描 profile（CODE/leo_sim/profiles/e0_load_scan.yaml）与 GLOBAL-PRESSURE-BRACKET 工作包（R01 brief 含 load cell 与负载门）均在位。
[B3-5] 负断言公平。"无一测量跨体制迁移的阈值行为"限定在四锚+DTAR 范围，笔记层面成立（各文均单一合同评估；DTAR 三合同但域级、无阈值轨迹提取）。未越界为全称空白。
[B3-6] 竞争解释与信息条件：(a)(b)(c) 继承 T-C2 并配可执行判别结构；(c) 指标伪影有明确淘汰条款；最强对照"负载数率入状态"把信息缺位 vs 训练合同两个解释做成可判别双臂——比较公平，无合同错位；(d) ELB/TLR 失标定形态差异为第二判别点，机制上成立【推演标注一致】。

## L1 逐条
[L1-1] 支持（PDF 逐字）。LOZANO 28 字段无寿命字段（笔记 L12）；CHOU eq.(3) si(t)=[Qi(t),{Dij(t)},xi(t)] 无寿命字段（CHOU PDF 行 270-281 逐字核）；LIAQ/HE 状态无寿命字段（笔记）。"拥塞=∞"=LOZANO PDF 行 541-543"congestion levels...set to infinite"；"不可用链路 −5"（笔记 L12）；eq.(13)=模型预演权重平均式（PDF 行 948 上下文，"leverages the predictability of the constellation movement"），草案"唯一用点"表述自带"全文未穷尽"限定——诚实。
[L1-2] 支持（测量锚）。IZHIKEVICH 15s 平滑窗"对齐 Starlink dish 重配周期"、尖峰呈 15s 倍数、全篇只测时延无丢包（笔记 L9/L11/L17）；草案"不直接承重交付坑"的免责声明正确。快照粒度 150×=LOZANO 15s（笔记 L14）vs PRIMAL 100ms（笔记 L13），均核实。
[L1-3] **竞争解释缺口①（库内现成证据未用）**。IZHIKEVICH 笔记 L11 明确记录尖峰"与切换无关（5 尖峰中 2 次同星）、与拥塞无关"——这是对"切换窗口→丢包坑"机制的库内反证方向，L1 未引。其免责声明覆盖大半，但修订时应显式列入竞争解释。
[L1-4] **竞争解释缺口②（库内现成证据未用）**。GANNON-2024（库内笔记）以 make-before-break 双波束实测挑战"GSL 切换必然断流"——直接威胁"切换窗口丢包坑"的前提。笔记自带"LEO-GEO 中继、别过度引申"警告，故不反驳 L1，但 strongest_alternative 应纳入并写明边界。
[L1-5] INPUT_INSUFFICIENT（标签诚实）。Yan25b（ICC'25，-60.5%/+55%）、Ort25（NetSoft'26）、SHORT/MobiCom'24、He20/Zha26l/Jin26 在 SOURCES.csv/notes/NKV 零命中，arXiv API 亦未检到 Yan+Starlink+handover。草案自标"摘要级/未核"一致；**-60.5%/+55% 数字在核读前不得承重**（目前位于"完整替代栈"叙述中，属覆盖判定的组成证据，覆盖结论必须等核读）。
[L1-6] STARTCAP"单终端样本警告"实为笔记"不舒服"段的质疑（"15s 可能只是某个终端样本的特征"）而非 STARTCAP 原文结论；L1 已标"待回原文"，可接受但措辞宜写清出处是笔记质疑。
[L1-7] "快照模式下机制贡献恒 0（前提待对模拟器代码核实）"自标待核，未承重——处理正确。

## 覆盖判定合规性复核
三稿均未把"相似"当"覆盖"：F1 对 TAP-DAR 冻结空白表述并设全文核读为淘汰门（正确）；B3 对 DTAR 做条件/能力/不能三段比对后得出"核心问题未被解决"（有据，见 [B3-3]）；L1 替代栈含未核成员故覆盖结论悬空（正确悬空）。M1 之后，TAP-DAR 全文核读成为本轮最高优先核验动作。
