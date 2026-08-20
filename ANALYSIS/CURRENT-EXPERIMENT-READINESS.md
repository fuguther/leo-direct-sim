# leo_sim V2 当前实验就绪状态

> 状态最后核验：2026-08-21；当前 main 为 `29c158349caf33c313d9ec0940f8eefc13f91485`，已部署到 canonical VM。代码可做同 SHA 非学习工程 smoke；M-Lab measurement-proxy 的有界多 OD + burst T0、topology cadence 校准、逐向 physical available-capacity 分母和三档 E0 工程负载标定已有 VM receipt/重算证据。奖励 blocker、V2 artifact→claim 闭环、学习 VM smoke、正式三段时延 gate 和正式授权 cohort 仍未完成，不能把当前状态称为论文实验就绪。
> 判定词：`FACT` 为当前可核验证据；`INFERENCE` 为基于证据的判断；`ESTIMATE` 为带前提的工期范围，不是承诺。

## 1. 两个目标

| 目标 | 完成定义 | 当前位置 | 剩余工作的性质 | 时间估计 |
|---|---|---|---|---|
| A. 可可信跑真实流量诊断/pilot | D1/D2 与核心语义冻结；V2 证据链闭合；真实流量、多 OD/突发、利用率和三段时延可重算；同一 SHA 经审阅部署 VM | **部分达到：D1/D2、M-Lab provenance/burst 和 physical available-capacity 代码已合入；同 SHA VM E0 工程校准已自然结束且 receipt verified。仍缺奖励 blocker、V2 artifact→claim、学习 VM smoke、三段时延正式 gate、授权 cohort 与 pilot** | 先做 D1/D2 长窗对照、三段时延/资源剖析和正式证据链，再跑正式 E0/PILOT | **当前测试/工程 smoke 不能当论文数据** |
| B. 可支撑论文主结论 | 目标 A 通过；完成 Q0-I/Q0-F、候选方向物理特征、逐字段 AoI、replay 续训；诊断后提出方案并完成配对正式矩阵 | **尚未达到；Q0 只有快照，信息/续训能力未闭合** | 理论归因、机制反例、长训恢复、正式统计与外部有效性 | **ESTIMATE：目标 A 后 4–10 周**；取决于诊断是否支持明确机制及训练成本 |

目标 B 必须定义为“本研究范围内的 practical ceiling”，不能定义成所有卫星网络机制都完美。未校准的 Doppler、天线、ARQ、天气或链路参数即使代码存在，也不自动提高科研可信度。

## 2. 当前事实快照

| 项目 | 当前事实 | 判定 |
|---|---|---|
| GitHub main | `29c1583`（PR #93、#94 合入）；当前代码 CI 绿；1 秒拓扑/MCS/M-Lab 多 OD profile 本地和 VM 可跑 | FACT |
| D1 动态链路速率 | 已合入、测试通过；VM E0 使用 MCS 并已自然结束，但旧平台 MCS 表征与逐距离对照尚未完成 | FACT；正式论文支撑未确认 |
| D2 动态拓扑/holding 语义 | 已合入；退役链路、在途包、等待语义有测试；长时间 VM 验证尚未完成 | FACT；正式论文支撑未确认 |
| 包守恒/FIFO/等待/在途 | 基础能力和回归测试已有，VM smoke 守恒通过；正式 artifact/分析链和长窗覆盖未闭合 | FACT；论文证据未闭合 |
| 奖励/学习语义 | R1-A1 仍是 blocker；不能开始学习算法正式实验 | FACT；硬阻塞 |
| 信息公平 | 已修复明确 cache-hop 偷看；逐动作物理特征、逐字段 AoI 未完成 | FACT；硬阻塞信息归因 |
| 当前 VM | 已部署精确 main `29c158349caf33c313d9ec0940f8eefc13f91485`；deployment receipt SHA=`6519847a3a866e7342d8aa36360ed2e68d3cb98ef51d4458d390420925271cc6`，source tree SHA=`8a9ab6f570585567efba1c675fe12dd4687c4c917bdabab24aedeaf6ca32866c` | FACT |
| VM 工程 smoke | 新 56-cell M-Lab 多 OD T0：20 s、1,299 offered、613 delivered、579 `ACCESS_REJECTED`、107 `IN_SYSTEM_AT_STOP`；另完成 50/100/200 Mbps 三档 20 s 工程标定，均 natural end、conservation true、receipt verified、raw metrics `validation.ok=true`。学习算法 VM smoke 尚未完成 | FACT；非正式、非授权运行 |
| 真实流量/测量 | M-Lab 快照 44,929 行、4,752 OD、2,604 聚合单元；PR #93 新增显式有界强连通多 OD 选择，manifest 记录选中 56-cell 规则和源 SHA；新三档 E0 工程标定已重跑 | FACT；不能当原始真实包回放 |
| Q0 | snapshot 已在 main；计划注入/执行归因候选未通过审阅；Q0-I/Q0-F tiny 闭环未完成。Q0 不阻塞工程 smoke，但阻塞信息 vs 决策归因 | FACT |
| 正式分析链 | 矩阵编译/授权 Stage 1 已完成；artifact→指标→配对分析→claim 的真实授权产物和闭环仍缺 | FACT，partial；仍 blocking |
| 测量层 | 新多 OD trace 的 0.5/1/2/5 s VM cadence 四档均自然结束、receipt verified、raw metrics 重算通过；1/2/5 s packet/link metrics 逐项相同，1 s 暂定主候选。三档 E0 工程标定已完成；正式逐包三段时延 artifact、独立重算和三段和 gate 仍未完成 | FACT；阻塞拥塞论文诊断 |
| 续训 | replay、optimizer、target network、RNG 完整恢复未实现 | FACT；阻塞昂贵长训 |
| 三轮三方无新问题 | 只完成局部 PR/局部模块审阅，没有在最终冻结平台上完成连续三轮 | FACT，未满足 |

## 3. 目标 A：真实流量诊断/pilot 就绪门禁

工期按“代码和评审资源连续可用、VM 正常、没有新 blocking”估计；任务可部分并行，但最终审计与 VM 部署必须在冻结代码之后串行。

| 工作包 | 验收证据 | 当前状态 | ESTIMATE |
|---|---|---|---:|
| A0 文档与合同收敛 | 主线、阶段门禁、机器清单和 claim 边界一致 | 本 PR 处理 | <1 日 |
| A1 D1/D2 入 main | 精确 head 复核有效；CI 绿；合入后 main 全量与行为对照绿 | **代码已完成**；同 SHA VM E0 已覆盖 MCS/动态拓扑基础运行；仍缺旧平台 MCS 对照和专门 D2 长窗/退役链路验收 | 待验证 |
| A2 已知科学 blocker | 奖励、mask、deadline/Q0 控制范围有明确修复或冻结决策 | mask 已修复；**R1-A1 奖励 blocker 未关闭**；逐动作信息和 AoI 未完成 | 先关闭 |
| A3 正式证据链 | compile、review、authorize、run、receipt、analysis、claim 全链路真实产物 | Stage 1 矩阵编译/授权已完成；artifact→paired analysis→claim 仍 open | 1–2 日 |
| A4 真实流量与测量 | provenance、多 OD/突发；逐向利用率分子/分母；每包 queue/tx/prop；拥塞指标可从 artifact 重算 | 新 56-cell M-Lab/burst T0、cadence 四档、三档 E0 工程标定和 raw metrics 重算已在 `29c1583` VM 完成；正式三段时延 artifact、独立重算和授权 gate 仍 open | 1–2 日 |
| A5 最终平台审计 | 冻结 commit 上三轮 Codex/不同模型/网页 GPT 无新增 blocking/major | 未开始最终三轮 | 2–5 日 |
| A6 VM 与 pilot | 部署同一 main SHA；VM/TF 门禁、真实 smoke、E0-REAL、基线诊断与 pilot 自然结束 | `29c1583` 同 SHA 非学习多 OD/burst T0、cadence 校准和三档工程 E0 已完成；**学习 smoke、formal VM E0、全算法 pilot 尚未开始** | 待执行 |

最早的真实流量 smoke 会早于目标 A 完成，但它只能暴露工程问题。Q0 不阻塞这个 smoke 或 E0-REAL；V2 分析链、利用率分母和三段时延才是把诊断升级为论文证据的硬门。

## 4. 目标 B：论文主结论就绪路线

| 层 | 需要补到什么程度 | 当前主要缺口 | 是否阻塞目标 A |
|---|---|---|---|
| 物理/拓扑 | D1/D2；长时窗接缝、极区、接入/切换边界；选择性加入 Doppler/ARQ/天线并校准 | D1/D2 已合入；D1 MCS 对照、D2 长窗 VM 和高级物理校准未完成 | D1/D2 证据是；高级物理否 |
| 信息 | 每类信息来源、传播、年龄、预测性与 mask 完全一致 | #62 已关闭已知 cache-hop 旁路；逐候选物理特征和逐字段 AoI 未完成 | 不阻塞 E0；阻塞信息归因/相应学习臂 |
| 控制 | 路由、等待、服务顺序、接入分配的权限分层 | Q0-I/Q0-J 控制范围未完全冻结 | 不阻塞诊断；阻塞理论归因 |
| 流量 | 真实/代理 trace 为主，uniform 为控制；多 OD 与突发 | 基础 M-Lab/CSV 骨架和 proxy smoke 已有；正式 provenance 合同、多 OD/突发、`hour_utc` 尚未闭合 | 阻塞 E0-REAL |
| 学习 | 公平训练/评估、收敛诊断、完整断点恢复 | R1-A1 未关闭；学习 VM smoke 和 replay/optimizer/target/RNG 恢复未完成 | 阻塞正式学习实验 |
| 测量 | 端到端指标、丢包/积压、逐向利用率、queue/tx/prop 分解、V2 可重算分析 | 局部事件骨架已有；可信利用率分母、正式逐包三段时延、artifact→claim 闭环未完成 | 阻塞论文级拥塞诊断 |
| 校准/反驳 | 旧新行为对照、极端反例、参数敏感性、外部数据校准 | 尚未形成覆盖各层的校准套件 | 部分在目标 A 后进行 |

目标 B 应以论文 claim 为边界逐项验收，而不是一次性把旧平台全部功能搬回。能力取舍见 `PLATFORM-CAPABILITY-LEDGER.md`。

## 5. 下一步顺序

1. **先关闭 R1-A1 奖励 blocker**，在此之前不跑学习算法正式实验。
2. available-capacity 分母代码已合入并有新多 OD VM T0 ledger；三档 E0 工程标定已完成。下一步补齐逐窗口独立重算、每包 queue/tx/prop 三段时延及三段和校验，并在资源剖析后冻结低/中/压力档。
3. 在已部署 `29c1583` 上完成 D1 VM MCS 对照和 D2 长时间拓扑/holding VM 验证。
4. 闭合 V2 artifact→指标→配对分析→claim，并完成至少一个学习训练/评估 VM smoke。
5. 在已完成标定的新 56-cell M-Lab profile 上先做 CPU/内存剖析和非学习诊断，再跑 formal VM E0-REAL；之后进入全算法 pilot。Q0-I/Q0-F、逐动作物理特征、逐字段 AoI 按信息归因阶段完成。
7. 长训前补 replay/optimizer/target/RNG 完整恢复；通过后才冻结论文正式矩阵。
