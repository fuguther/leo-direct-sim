# NOTES.md

> ROLLING LOG；最后整理：2026-08-20。
> 本文件只记录最近操作、证据位置和下一步，不是平台状态真相源。
> 当前状态见 `ANALYSIS/CURRENT-EXPERIMENT-READINESS.md`；截至 2026-08-19 的原记录见
> `ANALYSIS/HISTORY/NOTES-THROUGH-20260819.md`。

## 2026-08-20：D1/D2 合入与 VM 工程 smoke

- PR #55（D1 动态链路速率）与 PR #56（D2 动态拓扑/holding）均已合入 main；当前 main
  为 `b037b6182bf16c9d406cabf4fa5dc8da8b441a2a`，PR #56 CI `pytest` SUCCESS。
- D2 合并前本地证据：`pytest -q` = `555 passed, 1 skipped, 3 subtests passed`；
  `git diff --check` 通过。VM 同一代码环境 `CODE/leo_sim/tests` = `494 passed, 1 skipped`；
  唯一 skip 是 macOS `/var` 别名反例在 Linux VM 不存在。
- 部署：canonical VM `/data/论文/leo-direct-sim`，source tree SHA
  `422b2c747d0a224daa3d786eff68cf8ff6a0fe1baf9aa6d69d16e4cbbbbfb175`，deployment receipt
  SHA `4866768f757eb1df3c3ac9f4b9539ed8b6dde728b668177472232ad869137aab`。
- 非正式工程 smoke：`smoke.yaml` 在 VM 自然结束，`DELIVERED=1`、
  `conservation_ok=true`、`IN_SYSTEM_AT_STOP=0`，`receipt verify`=`verified`。
- 边界：仓库当前没有 R02 的合法 `finalization.json`/`authorization.json`，因此没有伪造正式授权；
  本 smoke 证明“已部署版本可运行”，不证明 V2 正式分析链、真实流量诊断或论文结论已就绪。

## 2026-08-20：精确当前 main 部署复核

- 文档 PR #68 合入后的当前 main 为 `66be0adedbf96bcdad722ca6720851904b256129`；该 SHA
  已重新部署到 canonical VM。source tree SHA=`6291acba9c14d703c7758e7799fb51aae4a6a5eba0f84b16716cb846d1ba3345`，
  deployment receipt SHA=`24b0a4783a22960cc703faff0f6e46b4a7e077af7c9c86d3826423ed7878b06e`。
- 同一 SHA 的 `CODE/Results/_vm_smoke_66be0ad` 工程 smoke：自然结束、`DELIVERED=1`、
  `conservation_ok=true`、`IN_SYSTEM_AT_STOP=0`，`receipt verify`=`verified`。

## 2026-08-19（有限 holding queue：容量/面积/WAIT 语义）

- 分支：`codex/20260819-holding-queue`。
- 实现 `SatelliteHoldingQueue`，替代 kernel 内部无界 `pending` list 的运行时语义：
  每星 bits 容量、FIFO、`queued_bits`、`QueueArea` 面积、快照占用与 `holding_until`。
- 所有 pending 回退/重决策/Q0 WAIT 写入统一经 `_hold_packet`；容量不足记录独立
  `HOLDING_QUEUE_OVERFLOW` fate，进入数据守恒与 receipt；不再静默无界增长。
- pending ticker 增加 holding deadline sweep；WAIT 只在 `until` 到达后释放，快照可观察等待截止时间。
- 配置新增 `access.holding_queue_bits`，receipt `queue_area_bits_s` 新增 `holding`，机制计数新增
  `holding_queue_overflows`。
- 验证：`pytest -q CODE/leo_sim/tests` = **409 passed**；新增 holding queue/Q0 回归覆盖容量、FIFO、
  面积、overflow fate、快照、WAIT 和 deadline。
- 边界：尚未实现 Q0-I/Q0-F tiny 求解器、planned-vs-executed 回放门禁；D1/D2 仍需独立冷启动复核，
  本分支不得作为论文正式基线。
- 冷启动复核：初审发现 Q0 WAIT 未校验目标卫星，可能把包等待在错误节点；已在 `2d9581e` 修复并
  增加原子性回归。随后静态盘点确认生产路径均经 `_hold_packet`，Q0 位置索引、面积结算和 deadline
  sweep 无遗漏；复核后平台测试为 **411 passed**。

## 2026-08-19（D1/D2 靠拢、旧平台账本与实验路线图）

- 用户已决定 D1 动态链路速率、D2 动态拓扑重匹配按旧平台行为继续推进。
- D1 独立分支 `codex/20260819-d1-dynamic-rate`：原实现 `c0a1f18` 经复核为
  REQUEST_CHANGES；本轮修复零速率快照除零、MCS/控制发送计数时机、ISL 合法掩码、
  GSL 零速率等待唤醒与 FIFO 越过，提交 `5e2d779`，`CODE/leo_sim/tests` 为
  406 passed。仍需不同模型冷启动复核，暂不合入。
- D2 独立分支 `codex/20260819-d2-dynamic-topology`：实现已提交 `7cb11e8`，
  `CODE/leo_sim/tests` 为 400 passed；尚无独立冷启动复核，暂不合入。
- 主分支文档提交 `101088b`：新增 `ANALYSIS/LEGACY-FEATURE-LEDGER-20260819.md`
  和 `ANALYSIS/EXPERIMENT-READINESS-ROADMAP-20260819.md`，并把 Q0 信息裁剪组合矩阵
  补入 `ANALYSIS/Q0-ALGO-RESEARCH-20260818.md`。
- 当前结论：已有基线/机制验收链可以继续做低风险平台验证；D1/D2 未复核版本不能作为
  正式论文实验基线。Q0 调研不再无限扩张，矩阵定稿后进入合同冻结与 tiny 原型。

## 2026-08-19（Q0 合同层与只读计划校验）

- 新增 `CODE/leo_sim/q0.py`：不可变 `PlanAction`/`JointPlan` 合同，版本绑定和未知/重复动作
  fail-closed；Kernel 新增只读 `validate_joint_plan`，校验当前版本、live packet 位置、
  拓扑邻接、服务中/在途不可操作和 ISL 容量预留。
- 回归：`CODE/leo_sim/tests/test_q0_contract.py` 4 passed；平台测试全量 402 passed。
- 明确未完成：`apply_joint_plan`、有限 holding queue、Q0-I/Q0-F tiny 求解器和
  planned-vs-executed 回放门禁仍未实现；本次只完成 Q0 实现顺序第 1 步的一部分。

## 2026-08-19（Q0 计划原子应用）

- `Kernel.apply_joint_plan()` 已接入：第一版只接受 pending 数据包，整份计划先复核版本、
  live 位置、拓扑/容量/GSL 条件，再一次性迁移；非法混合计划不会部分修改。
- 记录 `q0_plan_audit`，成功应用后递增 `state_version`；同一计划内 ISL/downlink 容量按总量校验。
- Q0 合同测试 6 passed；平台全量测试 404 passed。
- 明确边界：尚未把所有 pending 路径统一成有限 holding queue，尚未实现 Q0 tiny 求解器和
  planned-vs-executed 回放门禁；本提交不是正式 Q0 上界结果。

## 2026-08-19（R6-G2b 收口：台账置 fixed）
## 记录规则

- 任务级证据放 PR；本文件只在合并改变当前平台状态、风险或下一步时更新。
- 设计解释写入对应 CURRENT/SUPPORTING 文档，NOTES 只留链接。
- 当前周期结束后原样归档；不得通过压缩删除失败、REQUEST_CHANGES 或未验证记录。
- 实时问题状态只在 `ANALYSIS/FINDINGS-REGISTRY.md` 更新。

## 2026-08-21：拥塞/利用率最小观测层

- 分支：`codex/20260820-congestion-observability`；代码提交 `e68f265`。
- Kernel 记录每个数据包的 emission、queue enter、service start、propagation start/arrival、
  delivery；每个真实服务窗记录 link ID、rate、occupied interval、capacity bits、served bits
  与 outcome。holding residence 由相邻 queue admission 重算，未凭空补 horizon exit。
- `CODE/leo_sim/metrics.py` 从原始事件重算每包 queue/holding、tx、prop、E2E 以及逐链路服务窗
  utilization；`receipt.py` 把原始事件和重算结果写入/校验 `ledgers.json`，ledger SHA 继续绑定 receipt。
- 先写反例再实现：纯 metrics 的 queue/tx/prop/utilization 与 orphan queue ID 拒绝测试；真实单星
  端到端事件测试。验证：`python3 -m pytest -q` = **563 passed, 1 skipped, 3 subtests passed**。
- 边界：当前分母是“记录到的传输服务窗容量”，不是链路在几何上可用的全部时间容量；真实流量
  provenance、多 OD/突发和 VM 部署验证仍是下一包，不得把该分支直接称为论文就绪。

## 2026-08-20：奖励目标第一包

- 分支：`codex/20260820-reward-objective`；提交 `4163226`。
- 将训练侧 ISL 转发奖励改为“实测 M1 队列奖励 + 非正逐跳成本”，配置校验强制
  `forward_step_penalty <= -reward_w1`；原始 `queue_reward()` 保留作诊断对照，并把该参数
  写入 requested receipt 字段。
- 先写反例测试再实现：零等待转发奖励为 0，正等待严格为负，非法 `-19 > -20` 配置拒绝。
- 验证：`python3 -m pytest -q` = **557 passed, 1 skipped, 3 subtests passed**；
  `git diff --check` 通过。
- 边界：只关闭已知“额外跳数刷分”风险；Q0 物理字典序目标、拥塞观测、V2 分析闭环和 VM
  学习 smoke 仍未完成。

## 2026-08-20：D1 第 8 轮返工与 main 合并

- 第 8 轮 exact-SHA 审阅对 `0e1f2a8` 返回 `REQUEST_CHANGES`：constant 配置虽已
  忽略 RF/MCS 数值，Kernel 初始化仍无条件派生 MCS 门限，导致配置解析成功后启动崩溃。
- `a5dfb33` 扩充回归到真实 `Kernel` 构造；constant 分支完全跳过 RFParams/MCS range
  派生，MCS 分支保持原校验/派生路径。上一轮同时关闭 completion/retirement 竞态、
  精确服务时长、非 tick 恢复及 capacity 路由同源动态速率。
- 合并最新 main 时同时保留 R1-A2 的 `cache_hops` 信息边界与 D1 的
  `rate_from_propagation` 动态容量；两个回归组均作为合并验收门。

## 2026-08-20：文档真相源收敛

- PR #58 已 squash 合并为 `e15c457d71db42e279d3599ecbbe5969608e8261`；主题为
  实验就绪/Q0/平台能力/实验计划真相源收敛。GitHub CI `pytest` SUCCESS（15 s），
  本地 `411 passed`，diff 无删除或移动路径。
- 隔离分支：`codex/20260820-doc-consolidation`，基线 main
  `4c8d38ff38031ae134ae6738b3ebaa405e0f06f7`。
- 开工基线：`python3 -m pytest CODE/leo_sim/tests CODE/tests -q` =
  `411 passed`。
- 新 CURRENT 文档：
  - `ANALYSIS/CURRENT-EXPERIMENT-READINESS.md`：两个平台目标、门禁和带前提工期；
  - `ANALYSIS/PLATFORM-CAPABILITY-LEDGER.md`：当前能力差距与优先级；
  - `ANALYSIS/Q0-INFORMATION-ABLATION-PROTOCOL.md`：从最优向下裁剪为主、
    从现实向上增加为辅；
  - `ANALYSIS/EXPERIMENT-PROGRAM.md` 与
    `EXPERIMENTS/experiment-program.yaml`：实验总计划与机器清单。
- 已停止把不存在的 `ANALYSIS/paired_analysis.py` 写成可运行入口；正式分析链
  登记为 R7-F1 blocking。clean main 实测：experiment_platform+work =
  `21 passed, 5 failed, 3 subtests passed`；focused identity = `1 failed`，均为缺失绑定输入。
- FINDINGS 补入 R1-A1 奖励正循环与 R1-A2 mask 信息旁路；未把 #43 的局部奖励
  修复冒充为关闭 R1-A1。

## 2026-08-20：当前外部状态核验

- GitHub main = `4c8d38f`；#57 已合入。
- D1 PR #55：head `408d368c...`，CLEAN，CI pytest SUCCESS，未合入 main。
- D2 PR #56：head `6be16cd2...`，CLEAN，CI pytest SUCCESS，未合入 main。
- VM deployment receipt：commit `a2a588d9...`、clean、
  `2026-08-20T01:51:43+08:00`；落后 main 且不含 D1/D2。
- Q0 replay/tiny 是未合入候选并有 REQUEST_CHANGES；Q0-F 尚未完成。
- 上述状态是 2026-08-20 核验快照，后续变化必须更新 CURRENT 文档，不能只追加 NOTES。

## 2026-08-20：R1-A2 信息边界修复合入

- 隔离分支 `codex/20260820-r1-mask-information` 复现为 FACT：在学习观测不变时，
  `obs_hops` 外的两跳目的地广告会让旧代码开启 forward 动作。
- 修复让学习选路的目的地广告、远端传播与队列指标和 observation 共用 cache-hop
  边界；C1 同时约束当前邻居来源与实际一跳传播。
- #62 head `614fd23` 独立冷启动复核 APPROVE；定向 `41 passed`、仿真内核全量
  `410 passed`、GitHub pytest SUCCESS；squash 合入 main `758b606`，R1-A2 已 fixed。

## 2026-08-20：R7 generic 证据链部分恢复

- PR #64 head `4e6d665` 经独立冷启动复核 APPROVE，Hosted CI pytest SUCCESS；
  squash 合入 main `12bf306`。
- main fresh 验证：当前 CI 范围 `425 passed`；无参数全量
  `470 passed, 1 skipped, 3 subtests passed`。
- 恢复范围仅为 generic `experiment-run-manifest/v2` 的持久化 paired analysis、
  claim schema、严格重验和 CI bridge；`leo_sim_v2` 使用不同合同及结果布局，
  因此 R7-F1 仍为 `open`（generic 部分恢复），不得据此授权正式 V2 实验。
- V2 矩阵 Stage 1 候选 `4664a223` 已收到 REQUEST_CHANGES：真实 launch 授权路径、
  acceptance、配对完整性、checkpoint 血缘、控制变量和 symlink containment 均需返工。

## 2026-08-20：研究主线与实际顺序重排

- 用户锁定主线为“拥塞控制与链路利用率”，执行方法为真实流量优先、先实验诊断、
  再理论推导、最后提出新方案；旧 EXP1→EXP3 不再是默认主线。
- 本轮更新 `ANALYSIS/EXPERIMENT-PROGRAM.md`、
  `EXPERIMENTS/experiment-program.yaml`、`ANALYSIS/CURRENT-EXPERIMENT-READINESS.md`
  和 `ANALYSIS/PLATFORM-CAPABILITY-LEDGER.md`，把全部指定能力按最早真实依赖分门：
  D1/D2/V2 证据链为平台门；真实流量、多 OD/突发、逐向利用率、每包三段时延为诊断门；
  Q0-I/F、逐候选物理特征、逐字段 age 为理论门；replay/optimizer/target/RNG 恢复为长训门。
- exact main `5b3ec5f...` 的 Luna 只读审计确认：CSV 多 OD、M-Lab/人口代理、burst、
  GAT/MPNN 骨架已存在；利用率分母、每包三段时延、逐字段 age、完整续训、Q0-I/F
  与 V2 分析闭环仍缺。网页 GPT 四通道首轮 1 个通过、3 个运行/证据门失败；重试又回收一份
  同方向的计划审阅，方法调研仍未形成合格信封。按用户最新指令已取消继续重试；失败通道不计作三方通过。
- 本分支 fresh 验证：CI 范围 `425 passed`；无参数全量
  `470 passed, 1 skipped, 3 subtests passed`；YAML 解析、实验 ID 唯一性和依赖引用检查通过，
  `git diff --check` 通过。

## 2026-08-20：V2 矩阵编译与授权 Stage 1 收口

- PR #67 候选新增 V2 多 cell 矩阵 request/manifest/analysis 编译、完整 cohort 授权、
  配对/acceptance/control signature/checkpoint/path 身份门；不包含 Stage 2 的
  artifact→metrics→paired analysis→claim。
- 两轮独立冷审均先返回 `REQUEST_CHANGES` 并复造真实缺口；最终 bearing SHA
  `290e31da543b3ab366a9a7e83b2b9d6b18a9173c` 获 `APPROVE`。关闭项包括
  runtime config path、acceptance、pairing 完整性、checkpoint 内容身份、精确 intervention leaf、
  symlink/alias containment、compile-report 重绑定及空 override 映射。
- 最终本地证据：matrix `20 passed`；CI 范围 `445 passed`；无参数全量
  `490 passed, 1 skipped, 3 subtests passed`；`git diff --check` 通过。

## 下一步

1. 关闭 R7-F1 的 V2 矩阵、artifact 指标重算、paired analysis 与 claim gate；
   generic #64 只作为可复用基础，不代表 V2 完成。
2. 获得所需语义/冲突授权后合入 D1/D2，关闭 R1-A1，并更新 CURRENT 中的精确 main/VM 状态。
3. 补真实流量 provenance、多 OD/突发验收、逐向利用率分子/分母和每包 queue/tx/prop 事件。
4. 冻结同一 main SHA 并部署 VM，按 E0-REAL→PILOT-BASELINES→DIAG-CONGESTION 做实验诊断。
5. 再完成 Q0-I/F、逐候选物理特征、逐字段 age；基于诊断提出方案，长训前完成 replay 完整恢复。
6. 平台关键门禁不再被文档/Git 清理抢占；回收 worktree时继续保护 dirty、orphan 与 detached 项。

## 2026-08-21：V2 结果到成对分析适配器

- 分支：`codex/20260821-v2-analysis-chain`；基线 main `2f577a5`。
- 新增 `CODE/experiment_platform/v2_analysis.py`：对 V2 矩阵的授权 cohort 逐 run 校验
  `receipt.json`、`ledgers.json`、`formal_run.json`、`governance_receipt.json`、
  `resolved_config.json`、`manifest.json`；从 receipt/原始事件重算 delivery、时延和服务窗利用率，
  按 preregistered pairing 做差值，并写出 `analysis-manifest.json`、`summary.json`、`report.md`、
  `claim-gate.json`。
- `CODE/leo_sim/matrix.py` 生成的 RUNBOOK 现在包含 V2 分析命令；该命令只在所有授权 cell
  自然结束并产出结果后执行，不能跳过授权或把 fixture 变成论文结论。
- 验证：V2 定向 `22 passed`；全量 `565 passed, 1 skipped, 3 subtests passed`；`git diff --check` 通过。
- 边界：这是 V2 分析入口和本地真实 receipt fixture，不是 VM 授权 cohort 证据；R7-F1 继续保持
  `open`，下一步部署同一 SHA，跑真实流量/E0 与持久化分析闭环。

## 2026-08-21：trace provenance 与 offered-load 合同

- 分支：`codex/20260821-trace-provenance`；代码提交 `3878862`，基线 main `91a6604`。
- 每个 trace manifest 新增 `provenance_contract`：源类型/路径/SHA、时间/坐标/bits 单位、CSV
  坐标到 aggregate grid 的映射规则、目标 offered Mbps、实际 trace offered Mbps、包/bit 账本。
  `receipt.py` 会按 resolved config 和 manifest 账本重验，缺字段或篡改时 fail closed。
- CSV 输入保留 source packet ID 并绑定输入文件 SHA；M-Lab/人口模式继续明确标记为代理，不得写成
  校准用户需求。
- 验证：trace/receipt/acceptance 定向 `119 passed`；全量 `565 passed, 1 skipped, 3 subtests passed`；
  `git diff --check` 通过。
- 边界：还没有当前 SHA 的 VM receipt，也没有整段几何可用时间分母；下一步合入、部署并跑真实 CSV
  多 OD/突发与 E0 smoke。

## 2026-08-21：main 499d2e6 VM 工程 smoke

- 从 clean full clone 固定 `499d2e6fb6b9aea0883aa57781f55b8655fe7638` 部署到 canonical VM。
- deployment receipt：`ba705741be0cc700acd392106651fe01faeba93cff0333e3d8543bd8421a00df`；
  source tree SHA `718a5268f736f77a9f4b749e5edc2ee2551041710cc07b8ee57eac247161d09d`。
- 非正式工程 smoke：`CODE/Results/_codex_vm_smoke_499d2e6`；natural end、`DELIVERED=1`、
  `conservation_ok=true`、`IN_SYSTEM_AT_STOP=0`；receipt verify=`verified`；36 packet events、
  4 service windows，trace provenance contract 含 source/units/offered-load。
- 边界：这不是 formal authorization、不是真实 CSV/E0、不是论文结果；下一步补正式授权
  cohort 与真实多 OD/突发 load calibration。

## 2026-08-21：burst/diurnal provenance 补齐

- VM burst plumbing smoke 暴露一个真实缺口：旧 `provenance_contract` 只记录 mode 和 realized load，
  没有把 burst start/duration/multiplier（或 diurnal amplitude/phase）写入结果，因此无法仅凭 trace
  artifact 复核负载变换。
- 分支：`codex/20260821-burst-provenance`；代码提交 `eba3c97`。新增并校验
  `traffic_transform`，burst/diurnal 参数与 resolved config 不一致时 receipt fail closed。
- 验证：trace/receipt 定向 `119 passed`；全量 `565 passed, 1 skipped, 3 subtests passed`。
- 之前 `499d2e6` 的 burst smoke 仍只算工程 plumbing，不能当已关闭证据；待本修复合入并重新部署后重跑。

## 2026-08-21：0c378a5 修复版 VM burst 重验

- 修复版 main `0c378a5c7538536d4ea65f4a3ac1e2b7c542ade9` 已部署；deployment receipt
  `7a3c06a61b851b2ae282f83749931bb5f6ee7ab7abd3a63ca0492201669835f7`；source tree SHA
  `abf0c04963564ad4bd9e9c61e5de0971c669ed85fafa71146f21573562c38ccd`。
- `CODE/Results/_codex_vm_burst_smoke_0c378a5`：natural end、85/85 delivered、守恒通过、
  receipt verify=`verified`；`traffic_transform.burst={start_s:10,duration_s:20,multiplier:3}`，
  offered-load 账本 `85,000,000 bits / 60 s` 可重算。
- 同一部署还完成 MCS smoke：receipt `effective.mcs=true`，服务窗速率出现
  `283.9025 Mbps / 2.103214 Gbps / 2.9504275 Gbps`；结果仍为工程证据，不是正式论文样本。

## 2026-08-21：最终文档版 main 部署

- 文档合并后的 clean main `42ff519d6caed3c9666f55e3390989c6943d1093` 已再次部署，确保后续
  formal run 使用当前主线 SHA；deployment receipt `ab047f09ec66088d7ab6af93bf8fdc6e989d6d087b1d0651a47383423888f6f9`，
  source tree SHA `a1e6a5730dd8e7ed51881d89166c79073c6f5d72bca35d57ed4a4ccac8c274de`。
- 该次仅为版本一致性部署；`0c378a5` 同代码已完成的 MCS/burst smoke 证据仍适用于代码行为，
  但正式授权 cohort/E0 仍未运行。

## 2026-08-21：M-Lab 真实测量代理与高负载 VM smoke

- 来源核对：旧工作区任务记录确认 `CODE/data/traffic/mlab_2026-05-27.csv` 来自公开
  M-Lab NDT7 GCS 测量归档，按客户端/服务端城市与 UTC 小时聚合；文件 SHA256
  `f15cf8b9845c195046a4566d31ab9eb0137e16270ea98ee6a06b871a6f578437`。它是测量代理，
  不是用户包级真实流量，当前 V2 `mlab` 模式只使用空间 OD 权重。
- 修复：`6936d10` 使指标层只对账本明确标记为仍在系统/途中丢失/截止时未到达的包放行未匹配
  propagation start；真正孤立事件仍 fail closed。新增回归测试。
- 验证：本地全量 `566 passed, 1 skipped, 3 subtests passed`；该干净 commit 已部署 VM，
  deployment receipt SHA `38782c8a5a0fc11ef7751f421aae55219b8b1be1badeffe3552c936b7c8bbe66`。
- VM 工程 smoke（30 s、24 星、Amagasaki→Tokyo、M-Lab proxy）：50 Mbps 为 1,533 包、
  456 delivered、1 in-system、自然结束且 metrics=`ok`；100 Mbps 为 2,990 包、719 delivered、
  88 in-system、自然结束且 metrics=`ok`；两次均守恒，未再出现 `unmatched propagation starts`。
- 边界：这是部署一致性与负载暴露 smoke，不是 formal authorization 或论文样本；M-Lab 的
  `hour_utc` 尚未进入当前 V2 mlab 变换，正式 E0/PILOT 仍需走编译→审阅→授权→回执链。
