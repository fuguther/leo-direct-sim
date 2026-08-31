# leo_sim V2 当前实验就绪状态

> **CURRENT-VOLATILE**：本文是最近一次仓库内状态快照，不是外部实时查询结果。引用其中的 branch、SHA、PR、CI、VM、run、完成状态或时间估计前，必须在当前 checkout、GitHub 和 VM 重新核验；过期检查由 `DOCUMENT-STATUS.json` 与 `scripts/check_document_governance.py` fail-loud。

## 2026-09-01 当前裁决：EXP-20260829-GLOBAL-PRESSURE-BRACKET-R02 已闭合描述性证据，研究问题尚未冻结（CURRENT）

- 仓库证据基线：`origin/main=79796b6d2bf9e471f951b6e4a6a80f11701eda81`（PR #192）。`EXP-20260829-GLOBAL-PRESSURE-BRACKET-R02` 的持久化分析为 `VERIFIED`，共 24 个 verified run；设计账本明确它们是 **12 个唯一 resolved config + 12 个相同配置精确重执行**，不能按 24 个独立条件或 24 个独立样本解释。
- 24/24 scene check 均为 `ACCESS_LIMITED`；claim gate 是 `READY_FOR_INDEPENDENT_CLAIM_REVIEW`，不是 `SUPPORTED`、论文可用或科研结论已成立。当前证据允许报告各 load 的描述值、运行完整性和精确重执行一致性；不能声称全球 ISL 压力阈值/响应曲线、因果效应、算法优越性、信息价值、RL 价值或新方法贡献。
- **当前最重要的项目任务不是继续挑旧实验跑。** 组会侧先按 2026-08-31 方向完成问题导向的强化学习路由/调度文献调研，从候选问题中收窄一个可证伪的中心问题；不预设新算法，不启动完整 RL 复现。实验侧保持暂停扩矩阵，先解释 `ACCESS_LIMITED` 对场景与可回答问题的约束，再由冻结后的研究问题决定最小新合同。
- GitHub、VM deployment 和本地 checkout 是不同状态：本节只确认已进入 `origin/main` 的证据工件，不据此宣称当前 main 已重新部署或 VM 可直接继续运行。任何新正式实验仍须重新走编译、审阅、授权、clean-main 部署、自然结束回执与分析重算。

> **历史分界**：从下一节开始均为按日期保留的历史设计或状态快照，只用于追溯证据与决策变化；其中的“当前”“下一步”和运行中状态均不得指导新任务，冲突时只采用本节。

## 2026-08-30 历史设计口径：全球 R02 是描述性场景/稳定性诊断

- `EXP-20260829-GLOBAL-PRESSURE-BRACKET-R02` 的 24 个计划 cell 只有 12 个唯一 resolved config；其余 12 个是同 load、同 seed、同配置的 a/b 精确重执行。a/b 只提供确定性/重复执行证据，不能计作额外 seed、独立样本或独立实验条件。
- 冻结 brief 已预注册：本 bracket 内最坏单链路漏斗利用率上界约 `0.135`，低于 ISL 压力门 `0.8`。因此该 cohort 能回答不同 load/seed 下的场景分类、描述性指标和重复一致性，不能回答全局 ISL 压力阈值、首个压力点或负载响应曲线；名称中的 `PRESSURE-BRACKET` 不扩大其 claim scope。
- acceptance `{1,0,true,true}` 是运行非退化与证据准入门，不是科研充分性门。只有后验 V2 analysis、冻结 scene classification、物理有效性和逐 claim 审阅全部通过后，结果才可进入相应科研结论；`governance research_eligible=true` 也不等于 paper-ready。
- 本节只冻结设计与解释边界，不提前填写运行结果。24-cell 串行 cohort 的完成状态、聚合指标和最终 scene 分类必须在自然结束、拉回和持久化重算后另行更新。

## 2026-08-29 历史快照：全球人口陆地场景后验分析与场景分类闭合

- 快照：`as_of_commit=c9ef45e`（origin/main；PR #172–#175 已合入，后验分析修复 #176 在合入流程中）；`last_verified_at=2026-08-29`；本文 2026-08-24/08-22 及更早节段按日期为历史快照，内容冲突处以本节为准。
- 全球人口陆地场景 `EXP-20260826-GLOBAL-PRESSURE-BRACKET-R01`（部署 `01c323a`、seed 7、双臂 `load10_a-s7`/`load10_b-s7`）：
  - VM 正式运行：双臂 natural end、conservation 通过、外部 launch witness 完整、governance v2 `research_eligible=true`、receipt code identity `daf695aff5ab…`（01c323a 时代代码）、双臂 trace 与 fate 完全一致；
  - 后验 V2 analysis（#176 语义；本地 Python 3.14 与 VM 3.11 身份差异下合法执行）：`status=VERIFIED`、verified_runs=2、`authorization_verification=bound_posterior`、`analysis_mode=posterior_governed_runtime`、双臂 `runtime_identity_binding=governance_bound_posterior`、`evidence_class=v2_external_witness`；delivery_rate=0.7764705882 双臂相同，重复对比 difference=0.0；`verify_persisted_analysis` ok=true；analysis manifest SHA=`c67c9c6c99f9d2f8b18eeb0da3dcabf58bcb2aff835fe075a2f03cd6fd60e9f7`、authorization 文件 SHA=`e60a19dc…`、deployment receipt SHA=`78d7c917…`；
  - scene classification（绑定上述 manifest；contract SHA=`574880a7…`）：双臂完全相同——`status=ACCESS_LIMITED`、scope=`global_populated_land`、integrity_ok/coverage_ok=true、observed 155 destinations、82 ISL 暴露包、route-stalled 11 pids、downlink 干净、0 ISL 压力候选；
  - 口径（claim_boundary）：10 Mbps 双臂=完整性/重复性检查点（差异 0.0），不升格为负载阈值、真实业务量、算法优越性或普适覆盖结论；负载分类须以多负载 bracket 数据为准。
- 其余科研状态：R02（500/50 MHz）双臂正式完成但无压力差异（否定性工程证据，不构成压力臂）；R03（5/2 MHz）单 seed 压力候选（#164）不升格；Q0 真实窗口 F/I 比较、信息消融、统一条件算法矩阵、RL 正式矩阵、论文 claim（`CLAIM_MAP.csv` 仅表头）均未完成。
- 文档治理：120/120 tracked Markdown 已纳入登记（#172）；2026-08-29 处置清单（as_of `a5cf727`）给出 4 份 update_now（含本文档）、13 个归档候选、1 consolidate、1 mark_superseded；归档/移动等受保护动作仍需用户逐项批准。
- `next_gate`：多负载 bracket 预注册（以 10 Mbps 重复点与 ACCESS_LIMITED 分类为基准设计 bracket 与多 seed）→ Q0-F/Q0-I 真实窗口 → 信息切断消融 → 统一条件算法比较。

## 2026-08-24 历史快照：EXP-20260824-ISL-BANDWIDTH-PILOT-R02 正式带宽双臂完成

本节覆盖下方较早快照中关于 exact main、VM deployment 和“V2 artifact→claim
仍未闭合”的状态描述；下方历史诊断数字仍须按各自日期理解。

- 当前 exact main 为 `d3a116a69912dd214d89582a7b29c947f2357bfa`（PR #159，CI
  `658 passed, 1 skipped, 3 subtests passed`）；canonical VM deployment receipt
  SHA=`dc1d7e0339ae3ee9c78025d863036f6d4d6ec261dea8b8a26f05f99233ae1291`。
- `EXP-20260824-ISL-BANDWIDTH-PILOT-R02` 的 500 MHz/50 MHz 两个授权 cell 已按
  serial fail-closed 顺序自然结束；双臂 governance `research_eligible=true`，VM 与本地
  精确环境 receipt verify 均通过，nonce-bound external witness 完整。
- V2 analysis 与 persisted recomputation 均 `VERIFIED`。这关闭了平台级
  compile→review→authorization→clean-main deployment→serial run→receipt/witness→paired
  analysis/claim-gate 的真实 cohort 证据缺口；不等于任何具体论文 claim 自动通过。
- 单 seed 工程诊断的最大 horizon-aggregate 有向 ISL 利用率为 500 MHz
  `0.0058712550`、50 MHz `0.0207618752`，差 `0.0148906202`；1120 条有向 ISL
  均未饱和，两臂数据 fate 完全相同。50 MHz 因此仍不是已验证的 pressure arm，不能
  据此冻结拥塞阈值或扩成大矩阵。
- 当前下一门从“修平台证据链”转为“成本受控的压力 bracket 预注册”。本地独立冷审
  verdict=`PASS_WITH_LIMITS`，仅覆盖单 scenario/seed 工程描述。ProjectPilot 修复后的
  Kimi 主审通道已返回 `EVIDENCE_READY/PASS_WITH_LIMITS`；第二个独立通道因非
  typed-reference 证据被 fail-closed 拒收，整个 operation 为 `FAILED`。这证明主审候选证据
  可用，不等于 Kimi 双通道外审通过；最终路线仍由 Codex 裁决为先做小型低带宽
  bracket，不先扩 seed、不转 demand 轴、不扩成大矩阵。

## 2026-08-22 历史诊断：280/14 E0 完整信息参考（10M 已完成）

这是一项配置/证据边界修正，不是内核或 trace schema 变更。动态 280/14 图在
`t={0,1,5,10,20,30}` 均连通、每星 degree=4、diameter=17；因此 E0 完整信息参考
使用 `control_plane.vis_k=17`。该值只适用于当前 280/14 E0 参考臂，不是所有实验的
默认值，信息裁剪实验仍可显式使用较小的 `k`。

已完成同一 trace 的 10M 对照：trace SHA 为
`e2b469b984a7fc677f4ae8a61621f7e1e9c93ff3b3ade097461a68f365a2d23`，两次
`resolved_config` 唯一差异为 `/config/control_plane/vis_k: 12 → 17`。旧
`vis_k=12` 与新 `vis_k=17` 的 offered/admitted/delivered/in-system 分别为
`250/240/192/58` 与 `250/240/233/17`；total delivery `0.768 → 0.932`，
conditional delivery `0.8 → 0.9708333`。停止时 holding 包 `48 → 7`，uplink 包
均为 `10`；holding queue area `930416301.5258671 → 124326178.47600535 bit*s`，
uplink area 完全相同；vis17 ISL 最大利用率为 `0.0011653`。两次均 natural end、
conservation 通过，VM receipt verify 通过，vis17 wall time 为 `649.276 s`。

该结果是单 seed、同 trace 的诊断证据：它支持“`vis_k=12` 会显著混淆 10M
holding/in-system 诊断”的判断，但不能单独宣称普遍因果结论。vis17 的
`research_eligible=false`，且没有 external launch witness，因此不是正式论文结果。
25M/50M 的 vis17 运行正在 VM 并行执行，结果尚未返回，不提前填写数字；三档完成后
才重新标定 E0。完成三档前不把旧 `vis_k=12` 曲线用于拥塞分档，也不因低交付率直接
加星；只有在完整信息参考下仍暴露容量压力时，才进入 long-haul/容量压力轴。

> **2026-08-22 historical diagnostic snapshot（非当前可用状态）**：平台当时达到“可做真实流量、可审计、可重复的工程 pilot”门槛，但还没有达到“学习算法正式论文数据可直接采信”的门槛。以下 main/VM/E0 数字均为历史诊断证据，不是 access boundary 变更后的当前可用性声明；由于接入语义已改变，E0 R02 必须 `rerun_required`。
>
> **当前不能混淆的两件事**：50/100/200 只是第一轮负载扫描，不是最终冻结值；三档实测交付率约 `0.472/0.455/0.429`，按预注册规则都落入 medium，机械候选为 50 Mbps，但必须补两个 seed，必要时扩大低端 bracket。学习正式矩阵、学习专用 CPU/RSS profile、完整三段时延 gate、Q0 真实 kernel 闭环和最终论文 claim 仍未完成。因此现在可以开始小规模非学习诊断和工程 pilot；不能把当前结果直接写成论文算法优越性或因果拥塞结论。

> 状态最后核验：2026-08-22；当前代码基线 main 为 `66c5a68`，已部署到 canonical VM。20 s 10/25/50 Mbps 运行均为 `diagnostic_truncated_horizon`，不能用于负载分类；新 drain-aware profiles 使用 emission window 20 s、simulation horizon 30 s。280/14/25° 仍是 E0 工程基线而非 paper-ready 全局冻结；下一步须完成各负载分别复用其 20 s run 精确 trace 的 10/25/50 drain-aware VM 三 cell。V2 artifact→claim 闭环、正式三段时延 gate 和正式授权 cohort 仍未完成。
> 判定词：`FACT` 为当前可核验证据；`INFERENCE` 为基于证据的判断；`ESTIMATE` 为带前提的工期范围，不是承诺。

> **Access boundary（E0 前门禁）**：当前默认 `access.unavailable_policy=reject` 保持历史兼容；新增显式 `queue` 仅是工程诊断语义，使用有限源端/上行队列，停止时未入网包记为 `IN_SYSTEM_AT_STOP`。新运行可由 raw events 重算 `access_admission_rate` 与 `network_delivery_rate_by_horizon`。旧 20 s 50/100/200 诊断保留原证据但不是 paper-ready；切换 queue 后必须重新做 coverage/horizon audit、VM 小样、E0 标定和训练，不能沿用旧曲线。
> 因此 access boundary 的 coverage/horizon 与可用速率联合校准已支持 280/14/25° E0 工程基线；E0-LOAD-CALIBRATION 仍 `in_progress`。10M 的 vis17 同 trace 诊断已完成，25M/50M vis17 正在 VM 并行执行；三档 drain-aware cell 全部返回后再判定负载区间，不能按历史扫描关闭正式门禁。

> **2026-08-22 coverage candidate → E0 engineering baseline（非 paper-ready）**：旧 140/7/30° VM smoke 已完成但覆盖不足；
> 280/14/25°（每面 20 星）的 20 s/1 s 与 6000 s/20 s 几何/RF 条件已由 exact-main VM trial 复核，现升级为 E0 工程基线。
> 它仍不是容量证明或 paper-ready 全局冻结；50 Mbps 仅为较高负载候选，10/25/50 结果齐全后再判定负载区间。

> **E0 工程基线（非 paper-ready 全局冻结）**：当前 exact-main `66c5a68`；此前 `29e41c8` 的 VM trial 已有 deployment receipt
> `11688f2f2fae23c250b535aa439057c01eebd8b386f132c00ba654c4003b31a8` 与
> `SMOKE-20260822-COVERAGE-280X14-E25-29e41c8` VM 回执。该 run 为 1299 offered、1233 admitted、978 delivered、
> 16 holding overflow、1 no-route、304 in-system，access admission `0.9491916859`、network delivery by horizon
> `0.7931873479`，natural end/conservation/receipt verified；wall/user/sys `424.1882/429.4386/2.0247 s`，max RSS
> `1869052 KiB`，events `9618761`。50 Mbps 是较高负载候选而非无损低负载；10/25/50 的 low/medium/high 标签待同口径 VM
> 结果后判定，旧 50/100/200 仅 historical-only。

## 2026-08-22 历史规划 1：两个目标

| 目标 | 完成定义 | 当前位置 | 剩余工作的性质 | 时间估计 |
|---|---|---|---|---|
| A. 可可信跑真实流量诊断/pilot | D1/D2 与核心语义冻结；V2 证据链闭合；真实流量、多 OD/突发、利用率和三段时延可重算；同一 SHA 经审阅部署 VM | **真实授权 R02 cohort 已闭合 V2 artifact→paired analysis→claim-gate；工程 pilot 基础门已达到。仍缺正式三段时延 gate、完整 replay 续训、全基线 pilot 与逐 claim 独立价值审阅** | 先做压力 bracket 与正式测量门，再跑学习/全基线 pilot | **R02 是单 seed 工程敏感性证据，不是论文统计结果** |
| B. 可支撑论文主结论 | 目标 A 通过；完成 Q0-I/Q0-F、候选方向物理特征、逐字段 AoI、replay 续训；诊断后提出方案并完成配对正式矩阵 | **尚未达到；Q0 只有快照，信息/续训能力未闭合** | 理论归因、机制反例、长训恢复、正式统计与外部有效性 | **ESTIMATE：目标 A 后 4–10 周**；取决于诊断是否支持明确机制及训练成本 |

目标 B 必须定义为“本研究范围内的 practical ceiling”，不能定义成所有卫星网络机制都完美。未校准的 Doppler、天线、ARQ、天气或链路参数即使代码存在，也不自动提高科研可信度。

## 2026-08-22 历史规划 2：当时事实快照

| 项目 | 当前事实 | 判定 |
|---|---|---|
| GitHub main | `7f29ea3`（PR #93、#94、#95、#96、#97、#98、#99、#100、#101、#102、#103、#104、#105 合入）；当前代码 CI 绿；1 秒拓扑/MCS/M-Lab 多 OD profile 本地和 VM 可跑 | FACT |
| D1 动态链路速率 | 已合入、测试通过；VM E0 使用 MCS 并已自然结束，但旧平台 MCS 表征与逐距离对照尚未完成 | FACT；正式论文支撑未确认 |
| D2 动态拓扑/holding 语义 | 已合入；退役链路、在途包、等待语义有测试；60 秒、100 Mbps、56-cell M-Lab VM 长窗自然结束、守恒、receipt 和 raw metrics 重算通过 | FACT；正式论文支撑仍需跨负载/授权分析 |
| 包守恒/FIFO/等待/在途 | 基础能力和回归测试已有，VM smoke 守恒通过；正式 artifact/分析链和长窗覆盖未闭合 | FACT；论文证据未闭合 |
| 奖励/学习语义 | 已关闭额外跳数正回报风险（R1-A1/`ce2566b`）；Q0 物理目标和正式学习结论仍未冻结 | FACT；阻塞正式结论，不阻塞工程 pilot |
| 信息公平 | 已修复明确 cache-hop 偷看；逐动作物理特征、逐字段 AoI 未完成 | FACT；硬阻塞信息归因 |
| 当前 VM | 已部署精确 main `7f29ea3ee21280722885bedc3efda3d98c56bd98`；本轮部署 receipt SHA=`6b916fbfab1debb0a65113d3c78be47f619463683ac0d4017791b4e72a8d0289`，source tree SHA=`b0fb2db50d30338a68351eb0ea754332d43144624bf39bdfab655e7ca282644f` | FACT |
| VM 工程 smoke | 新 56-cell M-Lab 多 OD T0：20 s、1,299 offered、613 delivered、579 `ACCESS_REJECTED`、107 `IN_SYSTEM_AT_STOP`；另完成 50/100/200 Mbps 三档 20 s 工程标定、60 s D2 长窗、capacity 负对照和 20 s DDQN train→checkpoint→eval，均 natural end、conservation true、receipt verified、raw metrics `validation.ok=true` | FACT；非正式、非授权运行 |
| 真实流量/测量 | M-Lab 快照 44,929 行、4,752 OD、2,604 聚合单元；PR #93 新增显式有界强连通多 OD 选择，manifest 记录选中 56-cell 规则和源 SHA；新三档 E0 工程标定已重跑 | FACT；不能当原始真实包回放 |
| Q0 | snapshot 与 kernel `JointPlan` 原子校验/注入接口已有；Q0-I/Q0-F tiny 已合入 main；信息阶梯 tiny 合同已合入；可选 `--decision-log` 会流式输出带 config/trace/code/receipt SHA sidecar 的 `leo-sim-decision-info/v1` truth/cache-age 审计。真实 trace planned-vs-executed 归因、实际 learner 向量逐字段映射和信息价值实验仍未完成。Q0 不阻塞工程 smoke，但阻塞信息 vs 决策归因 | FACT |
| 正式分析链 | R02 已以 exact main、clean VM deployment、两臂外部 witness、治理回执和持久化 V2 analysis 闭合真实授权 cohort；逐实验 claim/value review 仍单独执行 | FACT；平台链已闭合，具体论文 claim 未自动通过 |
| 测量层 | 新多 OD trace 的 0.5/1/2/5 s VM cadence 四档均自然结束、receipt verified、raw metrics 重算通过；1/2/5 s packet/link metrics 逐项相同，1 s 暂定主候选。三档 E0 工程标定已完成；正式逐包三段时延 artifact、独立重算和三段和 gate 仍未完成 | FACT；阻塞拥塞论文诊断 |
| 接入边界 | PR #150 已合入 main；默认 reject 与显式 queue、receipt v4/metrics v2、历史 v3/v1 兼容已通过独立冷审。main `63a1099` 已部署并完成 1,299 包 VM queue smoke：762 admitted、656 delivered、39 access overflow、604 in-system，natural end/守恒/VM receipt verified；max RSS 约 850 MiB | FACT；VM 小样已完成，仍需 coverage/horizon 与正速率可用性联合校准后才能关闭 E0 前门禁 |
| 续训 | continuation bundle 已绑定 replay、optimizer、target network、训练计数器、NumPy/TF RNG、schema/config/SHA；VM 已验证恢复后继续一步的动作/计数/权重一致；完整长窗中断/不间断等价仍未跑 | FACT；完整长训前仍需等价门 |
| 三轮三方无新问题 | 只完成局部 PR/局部模块审阅，没有在最终冻结平台上完成连续三轮 | FACT，未满足 |

## 2026-08-22 历史规划 3：目标 A——真实流量诊断/pilot 就绪门禁

工期按“代码和评审资源连续可用、VM 正常、没有新 blocking”估计；任务可部分并行，但最终审计与 VM 部署必须在冻结代码之后串行。

| 工作包 | 验收证据 | 当前状态 | ESTIMATE |
|---|---|---|---:|
| A0 文档与合同收敛 | 主线、阶段门禁、机器清单和 claim 边界一致 | 本 PR 处理 | <1 日 |
| A1 D1/D2 入 main | 精确 head 复核有效；CI 绿；合入后 main 全量与行为对照绿 | **代码已完成**；同 SHA VM E0 已覆盖 MCS/动态拓扑，60 s D2 长窗验收已通过；仍缺旧平台 MCS 对照和跨负载语义对照 | 待验证 |
| A2 已知科学 blocker | 奖励、mask、deadline/Q0 控制范围有明确修复或冻结决策 | 已知额外跳数刷分风险已由 `ce2566b` 修复并有反例回归；Q0 物理目标、逐动作信息和 AoI 未完成 | 正式结论前关闭 |
| A3 正式证据链 | compile、review、authorize、run、receipt、analysis、claim 全链路真实产物 | **R02 真实 cohort 已完成至 `READY_FOR_INDEPENDENT_CLAIM_REVIEW`，持久化重算通过**；后续实验复用同一链，claim 仍逐项审 | 平台门已关闭；逐 claim 持续 |
| A4 真实流量与测量 | provenance、多 OD/突发；逐向利用率分子/分母；每包 queue/tx/prop；拥塞指标可从 artifact 重算 | 新 56-cell M-Lab/burst T0、cadence 四档、三档 E0 工程标定、60 s D2 长窗和 raw metrics 重算已在 `8e2f1df` VM 完成；正式三段时延 artifact、独立重算和授权 gate 仍 open | 1–2 日 |
| A5 最终平台审计 | 冻结 commit 上三轮 Codex/不同模型/网页 GPT 无新增 blocking/major | 未开始最终三轮 | 2–5 日 |
| A6 VM 与 pilot | 部署同一 main SHA；VM/TF 门禁、真实 smoke、E0-REAL、基线诊断与 pilot 自然结束 | `69c40b1` 同 SHA 已部署；非学习多 OD/burst T0、cadence 校准、三档工程 E0、60 s D2 长窗、capacity 负对照、资源剖析及 Q-learning/DDQN/GAT/MPNN train→eval smoke 已完成；**formal VM E0、全基线 pilot 尚未开始** | 待执行 |

最早的真实流量 smoke 会早于目标 A 完成，但它只能暴露工程问题。Q0 不阻塞这个 smoke 或 E0-REAL；V2 分析链、利用率分母和三段时延才是把诊断升级为论文证据的硬门。

## 2026-08-22 历史规划 4：目标 B——论文主结论就绪路线

| 层 | 需要补到什么程度 | 当前主要缺口 | 是否阻塞目标 A |
|---|---|---|---|
| 物理/拓扑 | D1/D2；长时窗接缝、极区、接入/切换边界；选择性加入 Doppler/ARQ/天线并校准 | D1/D2 已合入；D1 MCS 对照、D2 长窗 VM 和高级物理校准未完成 | D1/D2 证据是；高级物理否 |
| 信息 | 每类信息来源、传播、年龄、预测性与 mask 完全一致 | #62 已关闭已知 cache-hop 旁路；逐候选物理特征和逐字段 AoI 未完成 | 不阻塞 E0；阻塞信息归因/相应学习臂 |
| 控制 | 路由、等待、服务顺序、接入分配的权限分层 | Q0-I/Q0-J 控制范围未完全冻结 | 不阻塞诊断；阻塞理论归因 |
| 流量 | 真实/代理 trace 为主，uniform 为控制；多 OD 与突发 | 基础 M-Lab/CSV 骨架和 proxy smoke 已有；正式 provenance 合同、多 OD/突发、`hour_utc` 尚未闭合 | 阻塞 E0-REAL |
| 学习 | 公平训练/评估、收敛诊断、完整断点恢复 | 已完成同 SHA 的 Q-learning、DDQN、GAT、MPNN 工程 smoke；DDQN 20 s 训练 1,220 步并完成 eval；continuation bundle 与 VM 单步等价已通过；长窗中断/不间断等价和收敛仍未完成 | 阻塞正式学习实验 |
| 测量 | 端到端指标、丢包/积压、逐向利用率、queue/tx/prop 分解、V2 可重算分析 | 局部事件骨架已有；可信利用率分母、正式逐包三段时延、artifact→claim 闭环未完成 | 阻塞论文级拥塞诊断 |
| 校准/反驳 | 旧新行为对照、极端反例、参数敏感性、外部数据校准 | 尚未形成覆盖各层的校准套件 | 部分在目标 A 后进行 |

目标 B 应以论文 claim 为边界逐项验收，而不是一次性把旧平台全部功能搬回。能力取舍见 `PLATFORM-CAPABILITY-LEDGER.md`。

## 2026-08-22 历史规划 5：当时下一步顺序（已被顶部裁决取代）

1. 已知 R1-A1 额外跳数刷分风险已关闭；下一硬门是把 shaped reward 与 Q0 的物理目标分离，并在正式实验前冻结 claim 目标。
2. available-capacity 分母代码已合入并有新多 OD VM T0 ledger；10M vis17 已证明完整信息参考会改变 holding/in-system 诊断，25M/50M vis17 正在运行。待三档完成后再补齐逐窗口独立重算、每包 queue/tx/prop 三段时延及三段和校验，并冻结低/中/压力档。
3. 在已部署 `8e2f1df` 上完成 D1 VM MCS 对照；D2 60 s 长窗已通过，仍需正式 cohort 的跨负载语义对照。
4. 复用已闭合的 V2 artifact→指标→配对分析→claim-gate 链；先预注册小型压力 bracket 并完成独立 claim/value review，不因 R02 50 MHz 仍低利用率而直接扩成大矩阵。
5. 先完成 access boundary 的 coverage/horizon audit 和 VM 小样，再在完整信息参考 profile 上做 CPU/内存剖析和非学习诊断，随后依据 10/25/50 vis17 结果重新标定 E0-REAL；之后才进入全算法 pilot。Q0-I/Q0-F、逐动作物理特征、逐字段 AoI 按信息归因阶段完成。
7. 长训前完成中断/不间断长窗等价和收敛门；continuation bundle 的实现与 VM 单步恢复已通过，但尚未替代该门。
