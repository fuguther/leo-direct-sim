# 外部专家审阅合并（2026-08-16/17，6 路）

> 来源：E1 网络架构×2、E2 路由/RL×2、E3 验证/工程×2（GPT 网页端独立审阅，候选证据）。
> 处置状态：✔ 已修 / 🔧 待修（低风险可自主）/ ⚠ 需拍板（语义/设计）/ 📋 已列计划。
> 全文证据在 /tmp/expert_*.txt（本地留痕），关键项附仓库行号。

## A. 威胁研究结论（高优先）

| # | 发现 | 严重度 | 来源 | 处置 |
|---|---|---|---|---|
| A1 | **正奖励绕路漏洞**：转发奖励 (0,20]×γ^hops、到达 50、失败 0、无距离/时延/跳数成本 → 多走空闲跳可获更高累计回报 | blocking | E2×2 | ⚠ 奖励塑形需拍板（加跳数/时延成本或 shaping） |
| A2 | **动作掩码信息侧信道**：候选由 vis_k=12 完整缓存+静态图可达性生成，观测仅 obs_hops=2 → 掩码泄露观测外信息 | blocking | E2 独立、E3 | ⚠ 目标发现应与观测同一信息集 |
| A3 | **因果泄漏（未来端点）**：kernel 用全时域 trace 建全部 endpoints，未来端点提前参与槽位预置/控制广告/观测分母 | blocking | E3×2 | ✔ PR #28（惰性激活，已量化+回归，待 Kimi 复核） |
| A4 | **确定性不 fail-closed**：enable_op_determinism 失败仅记字符串，receipt 接受失败串，platform_check 不要求 True | major | E3×2 | ✔ 已修（见 PR 24） |

## B. 建模真实性（E1 网络架构）

| # | 发现 | 严重度 | 处置 |
|---|---|---|---|
| B1 | Walker 简化：无 F 相位/偏心率/星历；RAAN 等间隔+同 idx 同相位 → 结论限特定星座 | major | 📋 论文限制节；小时/天级实验需 SGP4 |
| B2 | 极区/接缝缺失：98.6° 近极轨 E/W 跨面链路无极区断开/重建、无天线转向约束 | major | 📋 建模待办 |
| B3 | 固定速率+链路预算未集成：6000km 旧 MCS=0 vs 新 1Gbps → 可达路径/拥塞位置失真 | major | 📋 B5 已列（MCS 表待拍板） |
| B4 | 无 Doppler/指向/真实信道/ARQ：几何可见=可用且恒速，高估边缘 GSL/跨面 ISL；无 ARQ 使链路失效=网络层丢包 | major | 📋 论文限制节；ARQ 属协议假设需声明 |
| B5 | K 槽≠波束/时频资源模型；接入抽象反向改变路由路径 | major | 📋 声明接入抽象边界 |
| B6 | **MBB 积压包语义偏差**：切换把未分配积压包钉在旧链；dual_connect 不限制为两链（retiring_link_limit=4） | major | 🔧 需对照实验后修（手over 承重） |
| B7 | 控制包固定 8000 bit 与 payload 大小脱钩；广播树静态、断链不重算 | major | 📋 控制面计费/树重算待办 |
| B8 | 正式实验仅 Malaga↔Tokyo 单 OD → 不足以支撑全局负载均衡结论 | major | 📋 论文范围限制 |

## C. 学习设定（E2 路由/RL）

| # | 发现 | 严重度 | 处置 |
|---|---|---|---|
| C1 | horizon 右删失：长等待/慢路径样本被选择性丢弃 | major | 📋 已显式计数；长跑/续训缓解 |
| C2 | deliver 被强制：出口可用即 deliver-only；下行满直接 overflow 不绕行 | major | ⚠ 需拍板（业务合同 or bug） |
| C3 | 奖励不计传播/接入/下行时延，γ 按转移次数而非物理秒 | major | ⚠ 奖励塑形设计 |
| C4 | 无历史状态（framestack/GRU 未实现）→ 无法区分“旧但上升/下降” | major | 📋 TEMPORAL 设计稿已列 |
| C5 | GAT/MPNN 32 节点静默截断（按 sat id 排序） | minor | 📋 overflow 应编码/报警 |
| C6 | TabularQ 精确浮点键 → 更新但不泛化 | major | ⚠ 基线处置待拍板（禁用/离散化） |
| C7 | hop 基线是缓存感知最短跳，非全局最短路；应并列 delay/capacity/oracle 基线 | major | 📋 实验设计 |

## D. 验证/工程（E3 验证）

| # | 发现 | 严重度 | 处置 |
|---|---|---|---|
| D1 | comparison PASS ≠ C 层归因（只查执行完整性，不自动比对分歧） | major | 📋 归因门禁待建 |
| D2 | 解析锚点共享生产 C_KM_S → 常数改错测试仍绿 | major | ✔ 已修（PR 24） |
| D3 | 控制报文 bit 未绑定配置（receipt 只验正整数） | major | ✔ 已修（PR 24） |
| D4 | population_gravity 输入未在 intent 阶段绑定 SHA | major | ✔ 已修（PR 24） |
| D5 | 变异测试 M-3/M-4/M-8/M-9 捕获测试缺失 | major | 📋 已列 |
| D6 | deadline 等时刻语义不统一（>= vs >；service_end==deadline 完成优先） | minor/major | 📋 统一语义待办 |
| D7 | C 层证据粒度不对称（direct 逐跳 vs legacy 仅路径） | major | 📋 对照设计 |
| D8 | 性能 profile 只测非学习臂；5s≈1h 未归因；几何缓存需 VM 验证 | major | 📋 VM 学习臂 profile（闸门） |

## E. 已确认正确的部分（专家背书）

- 逐包逐跳、5 动作、局部信息、真实控制包+TTL/AoI、到达缓存信息边界（设计较强）。
- 到达奖励/转移生命周期修复（hard-retire 白拿 50、horizon 丢弃计数、decisions==transitions+discarded）已被专家确认有效。
- 去预裁剪修复有效；GAT/MPNN 已含 AoI 特征（E2 纠正了旧表述）。

## F. 下一步（自动推进）

1. PR 24：op_determinism fail-closed、控制 bit 绑定、population SHA、C_KM_S 独立（已完成，待复核合并）。
2. 几何记忆化缓存 + hop BFS（等价优化第二批）。
3. A3 未来端点因果泄漏：改活跃集/惰性构建 + 对照实验。
4. B6 MBB 积压包语义：对照实验后修。
5. A1/C3 奖励塑形、A2/C2 掩码/出口语义：等专家结果已齐，列设计稿待拍板。

---

## G. 第 1 轮三方挖问题汇总（2026-08-17 夜）

> 来源：GPT 两路独立挖掘（网页对话已抓取留痕：`/tmp/gpt_h1_primary.txt`、
> `/tmp/gpt_h1_review.txt`）、Kimi 独立挖掘（`/tmp/kimi_hunt1_out.txt`，
> 输出部分截断）、Codex 本地独立复现/验证。状态标注：✔ 已修（分支/PR）、
> ⚠ 需拍板、📋 计划、✖ 未成立。

### G1 新发现（不在 A–D 已知清单内）

| # | 发现 | 严重度 | 验证 | 处置 |
|---|---|---|---|---|
| G1-1 | **DownlinkServer 无几何恢复唤醒**：队列头包遇临时 GSL 中断时只 `yield self.wake`，唯一 wake 来源是 put()；`_release`/`_associate` 也不唤醒下行服务端 → 可见性恢复后包仍睡眠到 horizon | major | ✔ 复现：time_step=1s、GSL [0.15,0.6) 中断，pkt2 修复前 IN_SYSTEM_AT_STOP / 修复后 DELIVERED | ✔ PR #25（待 Kimi 复核） |
| G1-2 | **接入 FIFO 被 `_try_grant` 插队**：endpoint ticker 先于 sat ticker 运行，后请求者可在持有者释放槽位同刻插队；跨星授予残留 stale waiter 并漏记等待时间 | major | ✔ 复现：jumper(t=0.10) 先于 waiter(t=0.05) 获授（0.2 < 0.4） | ✔ PR #26（待 Kimi 复核） |
| G1-3 | **delay/capacity 把「远端 metric 未知」折叠为 unreachable → 立即 NO_ROUTE**：信息不足被转换成不可逆丢包，夸大低信息臂劣势 | major | 代码确凿（routing.py 边权 +inf；kernel `unreachable` → NO_ROUTE） | ⚠ 需拍板：拆分 METRIC_UNKNOWN 与 TOPO_UNREACHABLE，后者才直接丢 |
| G1-4 | **max_hops 语义 off-by-one**：`len(pkt.path)`=访问卫星数=ISL 跳数+1，`> max_hops` 实际最多允许 max_hops-1 跳 | minor | 代码确凿（kernel.py:1518 + path.append 时序） | ⚠ 需拍板：冻结合同（按跳数修正 or 按访问卫星数改文档/字段名） |
| G1-5 | **seen_ctrl 去重集合无 TTL/窗口**：随 horizon×广告率×星座规模单调增长 | minor | 代码确凿（kernel.py seen_ctrl.add，无淘汰） | 📋 内存优化（按 origin 保留窗口） |
| G1-6 | **TabularQ eval 消耗 RNG**：epsilon roll 每次决策消耗一次随机数；未见过状态 `_row` 随机初始化并写入表 | minor | 代码确凿 + 动态复现（基线 table_size=1/rng_changed） | ✔ PR #30（待 Kimi 复核） |
| G1-7 | **occupied 停表可能计入下行等待**：`_transmit` 下行等待中 GE next_up>horizon 时 `_svc` 未清、settle 把等待计入占用 | minor | ✔ 动态复现（基线 occupied=1.0，包从未发 bit） | ✔ PR #29（待 Kimi 复核） |
| G1-8 | **LocalCache.expirations += 0 死代码** | info | 代码确凿 | 📋 顺手清理 |

### G2 Q0 就绪度（GPT 两路一致，blocking）

- G2-1 **无统一全局状态快照接口**：S_t^global 分散在 endpoints/slots/caches/pending/
  各链路队列/server._svc/DRR deficit/GE 等对象；decision_sink 明确 output-only。
- G2-2 **无 planner 联合方案注入接口**：只能逐包逐跳 next-hop；`put_data`/`put`/
  `_associate` 不自带容量/K 守卫，需受校验的 `apply_joint_plan`（原子预留、过期 fail-closed）。
- G2-3 **无显式 WAIT 动作**：pending 只在 no_info/临时不可用时被动触发；
  routing.py「oracle may decide to wait」是文档-实现不一致。
- G2-4 **pending 为无容量 list、不计 queue_area**：Q0 的 WAIT 必须映射到有限
  holding queue（容量/bits 记账/queue-area/deadline sweep/overflow 语义）。
- G2-5 **物理约束底座可复用**：room/K/geometry/GE/deadline/retirement 均在现有
  执行路径强制；Q0 安全架构=planner 只决定、Kernel 唯一执行/裁决。

### G3 Q0 实验设计（GPT 建议，blocking 级）

- G3-1 拆分 **Q0-I**（仅解除信息传播限制、保持逐包动作/调度能力）/ **Q0-J**
  （+显式 WAIT+联合调度）/ **Q0-F**（+完整未来信息），否则 gap 无法归因到
  「信息不足 vs 决策能力不足」。
- G3-2 主诊断 Q0 保留与控制臂相同的控制业务流量（隔离「状态可见性」与
  「信令开销」两个因素）；去控制开销版本单独命名、不得用于纯信息归因。
- G3-3 冻结跨臂一致的性能目标（delivered bits / deadline 成功率 / 端到端时延
  tail），不拿逐跳 shaped return 与另一目标的 Q0 直接比较。
- G3-4 A2/A3 等信息边界 bug 必须清零后再做 Q0 对比，否则 Q0 会把泄漏「合理化」。

### G4 已知清单重分类（GPT 两路一致）

- **应修 bug**：A2（掩码信息集越权）、A3（未来端点因果泄漏）、D6（deadline
  等时刻语义）、B6（若 MBB 合同确为双连接+正确积压迁移）。
- **目标规格缺陷**：A1（正奖励绕路）、C3（奖励不计物理时延）——训练 return 与
  物理性能指标不一致，实验比较前须修正或统一。
- **设计选择需声明**：B1–B5、B7–B8（建模抽象）、C2（当前逐跳出口强制 deliver）、
  C4（无历史）、C6（TabularQ 表示）、C7（hop 基线定义）。
- **验证缺口**：D1、D5、D7、D8（归因/变异/证据粒度/VM 学习臂 profile）。

---

## H. 第 2 轮三方挖问题（2026-08-17，GPT 两路 + Kimi + Codex）

> 覆盖第 1 轮盲区模块（receipt/governance/trace/config/rng/fates/comparison/
> platform_check/experiment_platform）+ 5 个修复分支的交叉回归审查。
> 状态：✔ 已修（PR）/ ⚠ 需拍板 / 📋 计划。

| # | 发现 | 严重度 | 验证 | 处置 |
|---|---|---|---|---|
| H2-1 | **acceptance `non_oracle_routing` 恒真死门**：`routing_label != "oracle"` 恒 True（label 实为 analysis_upper_bound/None），direct 场景误配 oracle 仍 PASS | major | FACT（字符串推理）+ Codex 复现 | ✔ PR #35 |
| H2-2 | **receipt verify 遇畸形 packet_fates 键崩溃**：`sorted(key=int)` 对 `"abc"` 抛 ValueError，违反「绝不 raise」契约（CLI/remote 兜底 fail-closed） | minor | FACT+实跑复现 | ✔ PR #36 |
| H2-3 | **正式验收门踩 diagnostic occupied**：remote_job `require_data_isl` 用 occupied.isl_s（FIELD_AUTHORITY=diagnostic，不重算） | major | FACT | ✔ PR #38（改用 recomputed 多星交付数） |
| H2-4 | **fast_train「bit-equivalent」声明不成立**：eager float64 vs fast float32；非终态全 False mask eager raise / fast 静默回退 | minor | FACT（代码读定，未数值对照） | 📋 改注释+fast 补 fail-closed |
| H2-5 | **forward 分支缺「学习动作∈掩码」断言**：越掩码动作直接 put_data（ISLLink.put_data 不查 room）静默超容（deliver 分支有断言） | minor→major 防御缺口 | FACT+Codex 复现（主库抛原始 KeyError） | ✔ PR #37 |
| H2-6 | **run 循环吞 peek 异常当自然结束**（fail-open 形状） | minor | FACT | ✔ PR #37 |
| H2-7 | **pending 等待不进任何 queue-area**：等待时间无独立可观测口径（与端到端时延对不上账） | major | FACT | 📋 Q0-WAIT 前置（已入 Q0-INTERFACE-DESIGN） |
| H2-8 | **comparison `legacy_conservation` 名不副实**：实际只查 trace 摄入无错，非包级守恒 | minor | FACT | 📋 改标签/补守恒 |
| H2-9 | **账本 bit 身份不绑定（GPT F1）**：record 的 bits 可≠登记值，一增一减伪造守恒（receipt 层用 trace 逐包兜底） | minor | FACT+复现 | ✔ PR #32 |
| H2-10 | **burst 窗口可完全落窗外（GPT F3）**：multiplier 恒 1 仍声明 burst | major | FACT+复现 | ✔ PR #33 |
| H2-11 | **GE dwell 接受 bool（GPT F3-review）**：True 属 int 通过校验 | major | FACT+复现 | ✔ PR #34 |
| H2-12 | **非 csv 意图 sites 可空/不足（GPT F1-review）**：密封意图在不可生成 demand 上假绿 | major | FACT+复现 | ✔ PR #34（governance 密封前要求 ≥2 sites） |
| H2-13 | **comparison 未绑定资源参数（GPT F2）**：direct/legacy 两臂资源不等价，差异不可归因 | major | FACT+INFERENCE | ⚠ 需拍板（不能映射的资源 fail-closed） |
| H2-14 | **rng named-streams 位置相关（GPT F4）**：子集/重排改变同名流 | minor | FACT | 📋 按 canonical name 派生 |
| H2-15 | **governance project_root 可省略（GPT F5）**：csv/pop 输入 containment 仅在传入时强制 | minor | FACT | 📋 强制 project_root |
| H2-16 | **experiment_platform NaN schema（GPT F6）** | minor | INFERENCE 未复现 | 📋 待负例确认 |
| H2-17 | **CSV 微秒量化排序拒绝合法输入（GPT F7）** | minor | FACT | ⚠ 声明精度 or 保持高精度 |
| H2-18 | **future-endpoints 残留观测侧信道（GPT F8）**：own_state 分母 len(endpoints) 随远端激活瞬变，本地 obs 在控制传播前变化 | major | INFERENCE（分支回归） | ⚠ 需拍板：obs 信息集统一（抵达缓存 or 声明） |
| H2-19 | **TabularQ eval 全零行 tie 偏置（GPT F9）**：未见状态恒取 ACTIONS 序首合法 | minor | INFERENCE | 📋 声明（deliver 优先） |
| H2-20 | **FIFO 双定义分叉（Kimi）**：_try_grant 用 (req_t,cell) vs _access_tick_sat 用插入序；与惰性端点合并后同 req_t 可不同「最老」 | minor | FACT+INFERENCE | 📋 统一为插入序 |
| H2-21 | **occupied 分支 fate 错标边界（Kimi）**：GE 恢复超 horizon 且 deadline>horizon → 误标 DATA_DEADLINE_EXPIRED（main 几何路径同样问题） | major | FACT+复现 | ✔ PR #29 f800415（统一走 stalled） |
| H2-22 | **access FIFO wait 口径变化（GPT F10）**：跨星撤销等待计入 total，口径从「grant 等待」变「请求生命周期」 | minor | FACT | 📋 区分 granted/cancelled 统计 |

### 第 2 轮干净背书（三方一致）

- fates 双账本语义闭合；trace 序列化再校验保证「编译成功⟹加载成功」；
  authorize/deployment_guard 严密；model certified next-change fail-closed；
  Gateways.csv 无别名冲突（latent 风险当前不可达）。
- downlink（#25）与 occupied（#29）修复经交叉回归未见新正确性错误
  （occupied 的 fate 错标边界已按 H2-21 修复）；TabularQ（#30）干净，
  DDQN eval 惰性 rng 消耗无需同类修正。

---

## I. 第 3 轮三方挖问题（2026-08-17，Kimi + GPT + Codex，基于合并后 main 1599d3e）

> 前置更正：**#25/#26/#28 未合入 main**（git 证据；main 的 12 个修复是
> #22/#24/#29/#30/#31/#32/#33/#34/#35/#36/#37/#38）。G1-1（downlink 恢复
> 唤醒）与 A3（未来端点预建）在 main 上仍是开放状态。

| # | 发现 | 严重度 | 验证 | 处置 |
|---|---|---|---|---|
| K1 | **_transmit down-wait 不竞退休中断**：退休链路被钉死到链路恢复（复现 retire_at=1.5 但 5.009 才释放、交付 7.786 vs 应 ~1.6；期间整星服务停摆） | major | Kimi 动态复现 + Codex 复核 | ✔ PR #41（待复核） |
| K2 | **occupied 停表计入服务前 down-wait**（G1-7 残留）：_svc 调用时刻盖戳，停表结算把等待计入（复现 0.6033 vs 真实 0.5） | minor→Q0 major | Kimi 动态复现 + Codex 复核 | ✔ PR #41（_svc 传输开始时重盖戳） |
| K3 | **down-wait fail-fast 提前判死**：deadline 未到即记 DATA_DEADLINE_EXPIRED（复现 0.6s 判死，早于 deadline 2.0 与退休 1.5） | major | Kimi 动态复现 + Codex 复核 | ✔ PR #41（取消提前判死，到点才判） |
| I3-4 | **#38 正式门换的「recomputed」判据本身不可重算**：deliveries[].path 是 kernel 自报（receipt 只查 int 列表，不对拓扑/service_log 重算） | minor | FACT+INFERENCE | 📋 authority 改标或 receipt 补 path 重算 |
| I3-5 | **burst/diurnal 无 effectiveness 观测**：窗口与 horizon 相交 ≠ 有包落入窗口，正式门无法察觉处理未发生 | minor | FACT | 📋 加 burst_packets_in_window 计数并入 effective/门 |
| I3-6 | **acceptance 仍用 diagnostic occupied 做门**（multi_satellite_data_service） | info | FACT | 📋 一致性注记（方向偏安全侧） |
| I3-7 | **Q0 快照缺几何可用性**（isl/gsl 当前可用 + 下一几何变化时刻） | major（Q0-I 阻塞） | FACT（设计稿 §2 行 1 要求） | 📋 PR #40 后续补齐 |
| I3-8 | **Q0 快照 remaining_service_s 继承 K2 的 _svc 陈旧时间戳**（down-wait 期间失真/为负） | Q0 major | FACT（同 K2 根） | ✔ PR #41 修复后快照受益 |
| I3-9 | **Q0 快照 GE next_flip 暴露 RNG 未来 vs 设计稿「只含当前时刻」** | 设计选择需拍板 | 设计稿自相矛盾 | ⚠ Q0-A/Q0-B 分界 |

### 第 3 轮干净背书（Kimi）

- TabularQ eval × decision-snapshot：eval 不耗 RNG/不写表，decisions==transitions+
  discarded 闭合，无新缺陷。
- 账本 bit 绑定 × receipt 校验：链闭合（kernel FateError→interrupted→natural_end
  false→verify 拒；receipt 独立 trace bits 重算 + 双向比对）。
- burst × trace 编译：窗口相交门 + thinning 确定性 + 序列化二次校验正确
  （除 I3-5 外）。
