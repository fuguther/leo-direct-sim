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

## 2026-08-21：current main `ac0d019` VM deployment and smoke

- 通过 guarded `push-remote.sh` 部署 clean main `ac0d01965d91956b5d80df36dce5b351c1bdccc6`；
  deployment receipt SHA=`c43e711442195cc8f31025167784773562e3a71ddb8c3cca65f25e1b787aa66b`，
  source tree SHA=`bf9a90090e2d2ac82701483c08fcaebe1976a083a71315405fbb0f5ef683b98d`。
- VM 固定环境的 10 s M-Lab+burst smoke：config SHA=`38ee6b760b88829ee2751510755cb0fa1ded8c4c5cca0430d6527aeabbcbf110`、
  trace SHA=`21812f86b7883a47560bd15f9d7d2958a503fc71a7bc27d52dd3cfd252caea4d`、
  code SHA=`5d2ddec3fecfa0a8b83174eaf30aa1da8bf4e9a5d766ddfa6a387e4b8cc6a193`；18/18 delivered，
  natural end，守恒通过，receipt verify=`verified`。shell timer：real 6.41 s、user 11.33 s、sys 0.55 s。
- 同一 VM SHA 的 140 星 MCS/M-Lab 60 s smoke 也自然结束并 receipt verified：461 offered，
  440 delivered、20 ACCESS_REJECTED、1 IN_SYSTEM_AT_STOP、守恒通过；它仍是工程证据，不是授权论文样本。
- 边界：当前 `ac0d019` 已完成同 SHA VM 非学习验证；学习训练/评估 VM、formal authorization、
  available-capacity 利用率分母和正式 E0/PILOT 仍未完成。

## 2026-08-21：E0-REAL 50 Mbps 首次 M-Lab/MCS 长窗 smoke（候选）

- 分支：`codex/20260821-e0-calibration`，基线 main `743d05c`；新增
  `CODE/leo_sim/profiles/mlab_e0_calibration.yaml`（140 星、MCS、动态拓扑重算 1 s、
  M-Lab measurement-proxy 三 OD cycle、20--40 s burst）。
- 运行：60 s 本地自然结束，461 offered packets / 3.688 Gbit；440 delivered、20
  `ACCESS_REJECTED`、1 `IN_SYSTEM_AT_STOP`，守恒通过；修复后 `receipt verify=verified`。
  同一 trace SHA=`dfe47500712ddc353c4ba5b9564d943be7f10018d07e36bdeb52b4d35d166910`。
- 资源：macOS `/usr/bin/time` 记录 wall `78.66 s`、user `78.28 s`、sys `0.36 s`，约
  99.5% CPU busy；该测量没有可用 max-RSS 字段，不能伪造内存结论。
- 真实缺陷：receipt 重算没有把 `IN_SYSTEM_AT_STOP` 等合法未到达 fate 传给 metrics，导致
  截止时仍在传播中的包被错误报告为 `unmatched propagation starts`。本分支修复并新增回归，
  全量 `CODE/leo_sim/tests CODE/tests` = **524 passed**。
- 研究边界：当前 utilization 分母仍是“已记录服务窗容量”，本次六条 GSL 窗几乎均为 1.0，
  不能冒充几何可用容量利用率；E0 只能作为负载/守恒/资源工程诊断，DIAG-CONGESTION 前仍
  必须补 available-capacity 分母和 VM 同 SHA 验证。

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

## 2026-08-21：T0 M-Lab measurement-proxy OD + burst 闭环（候选）

- 分支：`codex/20260821-traffic-t0`，基线 main `51f832c`；本条记录对应当前未合入候选，
  不改变 main/VM 状态。
- `mlab` trace 编译现在 fail-closed 校验必需字段、小时范围、样本数和吞吐量，并在 manifest
  写入源 SHA、`row_count=44929`、`od_pair_count=4825`、完整 `hour_utc=0..23` 覆盖；显式
  burst 会记录 start/duration/multiplier。新增 schema、解释文档和
  `CODE/leo_sim/profiles/mlab_measured_od_burst.yaml`。
- 验证：`CODE/leo_sim/tests/test_config.py CODE/leo_sim/tests/test_trace.py` 为 **22 passed**；
  相关 receipt 回归 `205 passed`；profile validate 成功；本地 `run` 10 s 自然结束，
  18/18 delivered、0 in-system、`conservation_ok=true`，`receipt verify=verified`，
  trace SHA=`21812f86b7883a47560bd15f9d7d2958a503fc71a7bc27d52dd3cfd252caea4d`。
- 边界：这是可复现的 M-Lab **measurement_proxy**，不是原始用户流量或校准运营负载；尚未部署
  当前分支到 VM，也未完成 E0 负载标定、学习训练/检查点恢复和正式授权 cohort。

## 2026-08-21：拓扑重算间隔工程校准

- 分支：`codex/20260821-topology-cadence-docs`；基于已部署代码 `ac0d019` 的文档证据补录，未修改仿真内核。
- 本地固定同一 trace SHA=`dfe47500712ddc353c4ba5b9564d943be7f10018d07e36bdeb52b4d35d166910`，140 星、60 s、MCS、M-Lab 三 OD + burst，扫描 `0.5/1/2/5 s`。四档均自然结束、守恒通过、receipt 无错误，461 offered、440 delivered、20 `ACCESS_REJECTED`、1 `IN_SYSTEM_AT_STOP`；拓扑重算次数为 119/59/29/11，墙钟约 118.9/79.9/60.5/48.9 s。
- VM 固定同一部署代码 `5d2ddec3fecfa0a8b83174eaf30aa1da8bf4e9a5d766ddfa6a387e4b8cc6a193`，66 星、10 s 短 smoke 扫描四档；均自然结束、18/18 delivered、守恒通过、receipt verified。该 VM 扫描只验证部署合同和 cadence plumbing，不替代长窗 D2 语义证明。
- 暂定决策：E0 先用 1 s；2 s 作为成本敏感性对照，5 s 作为慢更新负对照。需在低/中/高负载、长窗上比较交付、积压、利用率和切换指标后再冻结。连续进程的 `ru_maxrss` 未作为逐 run 内存证据，独立资源剖析仍未完成。

## 2026-08-21：E0 多 OD + burst 负载标定

- 分支：`codex/20260821-e0-load-calibration`；代码未修改，使用当前已部署代码 SHA=`5d2ddec3fecfa0a8b83174eaf30aa1da8bf4e9a5d766ddfa6a387e4b8cc6a193`、140 星、60 s、MCS、拓扑 cadence 1 s、M-Lab 三 OD、20--40 s burst。
- 本地结果（同一运行合同、各自 trace/config SHA）：50 Mbps = 461 offered / 440 delivered / 20 `ACCESS_REJECTED` / 1 `IN_SYSTEM_AT_STOP`，config `e27ed88d83e8bb39f1b858cfe4e725d4291f2a9a4fe5d9d14d10973918c0a0e2`，trace `dfe47500712ddc353c4ba5b9564d943be7f10018d07e36bdeb52b4d35d166910`；100 Mbps = 944 / 877 / 60 / 7 `HOLDING_QUEUE_OVERFLOW`，config `a7acd58e141152bd00a347f737bacaab03653abe5db730c9f6b31684d058c953`，trace `9a41cd118c2c44fc76785047cafcaa194ea999c78d28fafed449588d721f65da`；200 Mbps = 1940 / 1816 / 96 / 28 `HOLDING_QUEUE_OVERFLOW`，config `6bd42a0d15ee1d5d0a18324d6a6f3679d8374dfdd0b948b325ad94abfca0c7ee`，trace `eba4359f12a9247ee85e32bd39a49cf404677d41dad2bfa6c7d7f39cab09bfe1`。三档均 natural end、conservation true、receipt verified；本地墙钟约 78.7/79.0/79.3 s。
- VM 结果（同一部署代码）：100 Mbps = 944 / 877 / 60 / 7 holding overflow，config `a7c4efd26dc6dd41064c7f066e2de005ce9495cf4453b423a0cf57cf26bcf9a4`，trace 与本地相同，wall `265.85 s`；200 Mbps = 1940 / 1816 / 96 / 28 holding overflow，config `1446e0bddfea67481995ffaa555e316627c4a91655d82b995f6a23101508def0`，trace 与本地相同，wall `264.48 s`。两档均 natural end、conservation true、receipt verified；50 Mbps 同部署的 140 星 60 s smoke 已在上一条记录中验证。
- 暂定候选：50 Mbps 低负载、100 Mbps 中负载、200 Mbps 高/压力负载；10 Mbps 只做 sanity。该表仍不是正式论文结果：available-capacity 分母、逐包三段时延、正式授权 E0 和资源 RSS 门禁仍未完成。VM 墙钟约为本地 3.4 倍，后续训练预算必须按 VM 实测调整。

## 2026-08-21：逐向物理可用容量分母（候选，待独立复核）

- 分支：`codex/20260821-available-capacity`；新增可选的 `execution.available_capacity_interval_s`（默认关闭，E0/诊断 profile 显式设 1 s）和独立的 `link_available_windows` ledger。每个固定区间按拓扑重匹配、已认证的几何上下线根和 MCS 距离阈值切成稳定片段，再在片段中点做速率积分；空闲链路也进入利用率分母；不把队列占用、服务窗口或学习观测混进容量定义。采样间隔下限为 0.01 s，且按拓扑切分后的单次运行最多 100000 个区间，避免误配置造成 CPU/ledger 爆炸。
- `metrics.summarize` 现在同时重算 service capacity 与 physical available capacity，输出 `available_capacity_bits`、`available_time_s`、`available_samples` 和 `utilization=served/available`；无新采样的手写旧 fixture 保持旧分母兼容。receipt 将原始 availability ledger 纳入 `ledgers_sha256`，验证时重新计算 metrics。
- 验证：定向 `28 passed`；`pytest -q CODE/leo_sim/tests CODE/tests` = **530 passed**；新增回归覆盖窗口内 GSL 上下线和退役 ISL 代际。M-Lab 10 s smoke 仍需在本 SHA 重跑；先前 18/18 delivered、conservation true、receipt verified 的结果来自上一版候选实现，不能替代本次验证。
- 边界：分母是明确的固定间隔、几何/MCS 分段物理机会估计，不是连续时间解析积分；GE outage 不从物理容量中扣除，而由独立 fate/队列指标解释。仍需独立冷审、长窗 MCS VM 验证和资源成本评估后才能合入主线。

## 2026-08-21：容量窗口按拓扑事件切分（候选，待独立复核）

- 独立冷审指出：容量间隔 1 s、拓扑重算 0.5 s 时，若只按中点记录会漏掉窗口后半段新装 ISL。修复后 ticker 按拓扑重算边界切分；已排空旧代只保留在包含其排空时刻的窗口，避免旧代跨窗口继续充当可用链路。
- 验证：定向 `28 passed`；全量 `pytest -q CODE/leo_sim/tests CODE/tests` = **530 passed**。新增回归明确断言旧 `isl:0:1` 只在 `[0,0.5]`、新 `isl:0:2` 只在 `[0.5,1]`。
- 独立冷审上一轮三项 blocker（退役 ISL、窗口内上下线/MCS 阈值、采样下限/上限）已关闭；本轮需复核拓扑事件切分后再决定合入。
- 第二轮复核又发现旧代链路在窗口中途排空时会把容量计到窗口末尾；已改为按 `drained_at` 截断，并新增回归。待第三轮复核。
- 处理方式：采样器先保留窗口内的候选片段，模拟自然结束、所有退役代际排空后，用确定的 `drained_at` 截断原始 availability ledger，再交给 metrics/receipt 重算；不会修改服务事件或数据包语义。

## 2026-08-21：physical available-capacity 合入并完成同 SHA VM E0 工程校准

- PR #91 已合入 main，merge SHA=`b356d03d205e0b0851ca998874d6b3256c2b9640`；独立冷审绑定前一提交 `396c2ee`，定向 `29 passed`，审查确认窗口内几何/MCS 分段、拓扑边界、新旧 ISL 代际和 `drained_at` 截断均无容量窗口跨界膨胀。合入前相关全量为 `531 passed`。
- 部署：canonical VM `/data/论文/leo-direct-sim`，source tree SHA=`d391dff5431c44c8af6b42302b2611b8ba4c1dc06b64a871d5f6a569cfcb64a8`，deployment receipt SHA=`ea343bc8d9b7fefbe2f88cddf594dfe97d7fce850db66a8170b46759c6e11578`。VM 使用固定 `leo-i39` 环境（Python 3.11.15、PyYAML 6.0.2、NumPy 1.24.3、SimPy 4.0.1）；系统 `python3` 缺 PyYAML，不能作为运行环境。
- VM 工程 E0（非 formal、非论文结果）：140 星、60 s、MCS、1 s 拓扑 cadence、M-Lab 三 OD + 20--40 s burst、50 Mbps；natural_end=`true`，`conservation_ok=true`，`receipt verify=verified`，461 offered / 440 `DELIVERED` / 20 `ACCESS_REJECTED` / 1 `IN_SYSTEM_AT_STOP`，0 queue overflow，wall=`267 s`；`link_available_windows=29,656`，ledgers=`93 MB`。结果证明同一 SHA 的非学习测量链可以在 VM 跑通，不证明正式 E0 或论文结论。
- 当前边界：available-capacity 分母代码和 VM ledger 已有证据；逐窗口独立重算、每包 queue/tx/prop 三段时延和三段和 gate、D1 旧平台 MCS 对照、D2 长窗语义、R1-A1、学习 VM smoke、formal authorization cohort 仍是后续门禁。

## 2026-08-21：PR #93 合入与 M-Lab 多 OD T0 闭环

- PR #93 `feat: add bounded M-Lab multi-OD endpoint mapping` 已通过 CI（全量 `582 passed, 1 skipped, 3 subtests passed`）并合入 main；merge SHA=`4e89b5c4d0de789b1d89043e5be5fd98b6fa7ea9`。
- 新增显式 `endpoints.mlab_auto=true` 与 `mlab_max_sites`：从完整快照的 44,929 行、4,752 个有向 OD 对、2,604 个聚合单元中选择最大测量强连通子图；默认上限 64，本 profile 选中 56 个单元。选择规则、单元列表、候选规模和 measured-outgoing source weighting 写入 trace manifest；显式端点模式不受影响。
- canonical VM 已部署该 exact SHA；deployment receipt SHA=`8b22597b548eea77ffa5dce79694ad9c4c690b598270127b5b3cae71c85b6178`，source tree SHA=`1c231110c23d2236cc6667a9cb551b2a9a4ae69b4ed4718b1696f16f5789546f`。
- VM T0 profile `mlab_multiod_burst_t0.yaml`（140 星、20 s、MCS、1 s cadence、50 Mbps、8--16 s burst、1 Mbps packets）：trace SHA=`f6981c327f4c36e659d3f7b5ef66128f94a199d0203591401c88ed0e8ab22de4`，1,299 offered、613 delivered、579 `ACCESS_REJECTED`、107 `IN_SYSTEM_AT_STOP`；natural end、conservation、receipt verify 均通过。
- T0 原始 ledgers：20,935 packet events、1,648 service windows、10,932 availability windows；独立 metrics 重算与存档完全相等。该运行是工程 T0，不是 formal 或论文结果。

## 2026-08-21：同一 M-Lab 多 OD trace 的 VM topology cadence 校准

- 四档只改变 `topology.recompute_interval_s`，保持 config 之外的流量/seed/端点选择和 trace identity 不变；四档 trace SHA 均为 `f6981c327f4c36e659d3f7b5ef66128f94a199d0203591401c88ed0e8ab22de4`。
- `0.5 s / 1.0 s / 2.0 s / 5.0 s` 均 natural end、conservation true、receipt verified，fates 均为 `613 delivered / 579 ACCESS_REJECTED / 107 IN_SYSTEM_AT_STOP`；四档 raw ledgers 独立重算 metrics 均 `validation.ok=true`。
- VM wall-clock / topology recomputes / availability samples：`0.5 s = 171 s / 39 / 21,726`；`1.0 s = 120 s / 19 / 10,932`；`2.0 s = 107 s / 9 / 10,932`；`5.0 s = 94 s / 3 / 10,932`。1/2/5 s 的每包指标和链路指标逐项相同；0.5 s 仅增加 availability 采样（capacity 浮点差在采样表示层），不改变交付/时延汇总。
- 暂定决策：E0 主候选保留 `1.0 s`；`2.0 s` 做成本敏感性，`5.0 s` 做慢更新负对照。该 20 s 校准不能替代 D2 长窗语义证明；下一阶段为同 exact SHA 的 E0 低/中/高负载标定。

## 2026-08-21：main 29c1583 上完成 M-Lab 多 OD + burst 三档 E0 工程标定

- 分支：`codex/20260821-e0-load-docs`；代码未修改，仅更新实验真相源和机器索引。基于 main `29c158349caf33c313d9ec0940f8eefc13f91485`，canonical VM deployment receipt SHA=`6519847a3a866e7342d8aa36360ed2e68d3cb98ef51d4458d390420925271cc6`，source tree SHA=`8a9ab6f570585567efba1c675fe12dd4687c4c917bdabab24aedeaf6ca32866c`。
- 固定 profile：140 星、20 s、MCS、1 s topology cadence、M-Lab 最大强连通 56-cell、8--16 s burst；三档只改变 `offered_mbps`。VM 三档均自然结束、`conservation_ok=true`、`receipt verify=verified`、原始 packet/service/availability ledger 重算 `validation.ok=true`。
- 结果：50 Mbps = 1,299 offered / 613 delivered / 579 `ACCESS_REJECTED` / 107 `IN_SYSTEM_AT_STOP` / 0 overflow，wall 119 s，trace `f6981c327f4c36e659d3f7b5ef66128f94a199d0203591401c88ed0e8ab22de4`；100 Mbps = 2,756 / 1,253 / 1,270 / 233 / 0，wall 129 s，trace `e6e7bd329f6822046f5d57611690d609a3647e1dca7639e170e985d891000e09`；200 Mbps = 5,551 / 2,382 / 2,597 / 405 / 167 holding overflow，wall 134 s，trace `f009c98d8be5757a4ba1afe585fed32d6974143582eb3c9d8657344413a834c6`。
- 暂定解释：50 为低负载候选，100 为中负载候选，200 为压力/过载对照。它们是工程标定，不是正式论文效果结果；formal E0 仍需资源 RSS、三段时延 artifact/独立重算、学习 pilot、授权与 paired analysis 门禁。相关文档同步为 `ANALYSIS/EXPERIMENT-PROGRAM.md`、`ANALYSIS/CURRENT-EXPERIMENT-READINESS.md` 和 `EXPERIMENTS/experiment-program.yaml`。

## 2026-08-21：main 0fc9427 资源剖析与四学习臂工程闭环

- 部署：main `0fc9427520eb1d67e3493a521ea767c69b69575f`，canonical VM deployment receipt SHA=`c318945c852182c2d34e4d255a0ba79715ca31f030fb7f7c76be48065f0baae3`，source tree SHA=`390fd14375ab95aff885fe6de3758d5ea8638c74abd33a6e827da6832a987c94`。固定环境仍为 `/data/liguang13/conda-envs/leo-i39/bin/python`。
- 资源剖析：同一 2 s、100 Mbps、56-cell M-Lab/burst 配置，1/2/4/8 线程均 natural end、conservation true、事件数 286,671、trace SHA=`f69b73b3e8bd02ff2b9e22c05d0c369d2bf1c36e7c7f8eab0bbe5c22f5165b02`；墙钟约 `14.298/14.412/15.648/14.707 s`，峰值 RSS `465,996/461,260/459,948/461,652 KiB`。没有可重复的多线程加速，后续 pilot 采用 1 线程串行，避免空耗 CPU。
- 学习工程闭环：同一 2 s、100 Mbps、seed=7/41、`fast_train=true` 配置完成 Q-learning、DDQN(C3)、GAT、MPNN 各自 train→checkpoint→eval；8 个 run 均 natural end、`conservation_ok=true`、`receipt verify=verified`，8 个 raw ledger 独立 `metrics.validation.ok=true`。训练步数：Q-learning 112、DDQN(C3) 104、GAT 102、MPNN 103；每个 eval 均记录实际加载的训练 checkpoint SHA。
- 训练—评估不是论文效果结果，只证明当前 main/VM 的学习执行链可跑通。仍未完成 replay/optimizer/target/RNG 完整续训、formal authorization cohort、V2 artifact→claim、逐包三段时延正式 gate 和 Q0 物理上界。

## 2026-08-21：D2 60 秒长窗与 20 秒 DDQN 训练起步

- 长窗：main runtime code SHA=`d2247140312396cbf111e54239ec5274f22257c024d4f0909f50a6c4232454c0`，140 星、60 s、100 Mbps、56-cell M-Lab/burst、1 s cadence。VM 输出 `engineering-d2-long-60s-0fc9427`：`natural_end=true`、`conservation_ok=true`、`receipt verify=verified`、metrics `validation.ok=true`；8,510,023 events、216,243 packet events、7,908 service windows、33,137 availability windows、2,792 delivered、3,211 `ACCESS_REJECTED`、194 `HOLDING_QUEUE_OVERFLOW`、537 `IN_SYSTEM_AT_STOP`，输出约 139 MB。该轮是 D2 长窗工程验证，不是论文效果结果。
- 20 s DDQN：同一 100 Mbps/56-cell M-Lab trace，训练与评估 trace SHA 均为 `e6e7bd329f6822046f5d57611690d609a3647e1dca7639e170e985d891000e09`。训练 natural/conservation/receipt/metrics 全通过，1,220 train steps、1,227 transitions、checkpoint SHA=`9554170451d2f1866bcc23e381772189014e3f9e64c8ba5e931a46ce19312e97`；评估重新加载该 checkpoint，natural/conservation/receipt/metrics 全通过，0 train steps。20 s 负载下 3 `HOLDING_QUEUE_OVERFLOW`、约 375 个 `IN_SYSTEM_AT_STOP`，说明起步时长已进入真实拥塞压力区。
- 边界：本轮仍是 engineering/pilot；没有授权 cohort、paired claim、replay/optimizer/target/RNG 断点恢复或正式论文统计，不能直接写入论文结论。

## 2026-08-21：容量锚点与最新 VM 证据文档同步

- 分支：`codex/20260821-capacity-anchor-docs`；仅同步实验真相源和机器索引，不修改仿真内核。
- 当前 main `0f7249fb085ea05576c04d8b2b1f9e55be9e12a0` 已部署到 canonical VM；deployment receipt SHA=`89e70f943ef7c19b4f615e56cbf7cf2c349d49f572b916a97d2f816e4a33a4a9`，source tree SHA=`6dc0afec1070002fe83c5ddd0955c40c7ba5a2316cffa01fe1d01f8bc047d2fd`。
- 文档补录：capacity policy 负对照、D2 60 秒长窗、20 秒 DDQN train→checkpoint→eval、当前 main/deployment SHA；明确这些仍是 engineering/pilot，formal V2 artifact→claim、replay 续训、正式 E0/PILOT 和 Q0 闭环仍未完成。
- 验证：`git diff --check` 通过；`EXPERIMENTS/experiment-program.yaml` 可由 PyYAML 解析（22 experiments、23 requirements）。待本分支 CI 绿后合入并重新确认 VM SHA。

## 2026-08-21：PR #98 合入并重新部署主线

- PR #98 已通过 pytest CI 并 squash 合入，当前 main=`69c40b158abeabd6c7ccd0bbbead5ab646b51905`。
- canonical VM 已重新部署同一 main；deployment receipt SHA=`76244c2f62a49d748f213f6aa1544a122bd01d978ea53037bdc76ac46499e22c`，source tree SHA=`b5a95f4d253cd6bb154fc22d590c8331d2a5c4e835b0f1d8ac2a3a653a21f578`。
- 本次仍是文档同步和部署，不改变仿真行为；formal E0/PILOT、replay 续训、V2 artifact→claim 和 Q0 闭环继续保持未完成状态。

## 2026-08-21：exact-resume 实现与 VM 恢复验证

- PR #100--#104 已通过 CI 合入；当前 main=`bfae7616897bb56c92c87904427926f78c93d666`。
- 新增 `leo-sim-ddqn-resume/v1` 与 `leo-sim-qlearning-resume/v1` continuation bundle：DDQN 保存 replay、online/target、optimizer、训练计数器、NumPy/TF RNG；Q-learning 保存 Q 表、计数器和 NumPy RNG；manifest 绑定 schema、身份和每个 artifact SHA。
- canonical VM 部署 receipt SHA=`279522bf75404f16d4041bdb23539a71f4bb4b801fcb961de32af64b26b0360d`，source tree SHA=`261c185f59d7019ecc9e1bc546e7f441470be5c7ef09d8590d817eea3d1bd3ad`。
- VM 验证：DDQN exact-resume 恢复 replay/optimizer/target/RNG 后，继续同一 transition 的下一动作、训练步数、online/target 权重一致；Q-learning 恢复测试通过。相关定向测试 `2 passed`，学习/Q-learning VM 回归 `51 passed`。
- 边界：这是状态恢复和短续接证据，不是完整长窗“中断续训 vs 不间断”论文等价；该门仍未关闭。

## 2026-08-21：PR #105 后主线文档同步部署

- PR #105 已合入；当前 main=`7f29ea3ee21280722885bedc3efda3d98c56bd98`。
- canonical VM 已部署同一 main；deployment receipt SHA=`6b916fbfab1debb0a65113d3c78be47f619463683ac0d4017791b4e72a8d0289`，source tree SHA=`b0fb2db50d30338a68351eb0ea754332d43144624bf39bdfab655e7ca282644f`。
- 本次为文档同步部署，不改变 exact-resume 运行行为；完整长窗中断/不间断等价、formal E0/PILOT、V2 artifact→claim 和 Q0 仍是后续门。

## 2026-08-21：PR #107 formal E0 桥接运行完成

- 正式包 PR #107 已通过 CI 并 squash 合入，当前 main=`c6c18d0122b7251abe3a8b30b07e0dee746e0405`。该包绑定单个 `leo_sim_v2` 非学习 E0：140 星、20 s、M-Lab measurement-proxy 多 OD、50 Mbps、8--16 s burst、MCS、1 s 拓扑重匹配、control plane、seed 7；它是工程到正式链的桥接，不是算法比较或论文结果。
- canonical VM 已部署同一 main；deployment receipt SHA=`6f9ad082a15e372fe93ce16dbabfaeaa7009e7c9e08cbaa7598e9946c076171a`，source tree SHA=`ecc2e3a03c4237115e8821d7c6669acbfbf3b8f766cdd88123574362bfc50956`。授权 SHA=`19917bd8bc0e88c50b7c2e54c8e69c4360bb3edd53f88cccf09d549cde1492ca`，run id=`EXP-20260821-E0-FORMAL-R01-main-s7`。
- VM 正式回执：`natural_end=true`、`conservation_ok=true`、`research_eligible=true`、治理 `verification_errors=[]`、`receipt verify=verified`；1,299 offered、613 `DELIVERED`、579 `ACCESS_REJECTED`、107 `IN_SYSTEM_AT_STOP`、0 queue overflow；正式运行 wall-clock 约 123 s。原始结果目录为 `CODE/Results/EXP-20260821-E0-FORMAL-R01-main-s7`（不入库）。
- 当前明确边界：单运行 E0 使用 `leo-sim-experiment-run-manifest/v1`，而 `CODE/experiment_platform/v2_analysis.py` 的 paired analyzer 只接受 matrix manifest；因此本次正式回执链已闭合到自然结束/守恒/授权，但 **V2 artifact→paired-analysis→claim** 仍未闭合。下一组比较实验必须使用 matrix contract（至少一对受控 cells），不能把本次单运行直接写成论文对比。

## 2026-08-21：PR #109 paired V2 analysis bridge 完成

- PR #109 已通过 CI 并 squash 合入，当前 main=`40dfa39c50964c0f271ca428810f03865dc54290`；canonical VM 部署 receipt SHA=`c2a998ddd74866bcc706ae4f139050768e4a90cf95bb90a78d2489da1884e3b2`，source tree SHA=`b145900fbd80386ed75f9762666122a1d92242f92df1f978301b216dbc10a32e`。
- matrix `EXP-20260821-E0-PAIRED-R01` 的 control 与 baseline_copy 两个 cell 均在同一部署、同一 config SHA=`7ede74b936ad49e7a8e9b21779a6f6afc54cc2671f3e5f87670c14aed13c123d`、同一 trace identity、seed=7 下正式运行；两次均 `natural_end=true`、`conservation_ok=true`、`research_eligible=true`、VM `receipt verify=verified`。
- VM `v2_analysis` 已生成 `ANALYSIS/EXP-20260821-E0-PAIRED-R01/v2-paired/analysis-manifest.json`、`summary.json`、`claim-gate.json`；再次 `verify_persisted_analysis` 返回 `ok=true, errors=[]`。两臂 `delivery_rate=0.4719014626635874`，预注册 `baseline_copy-control` 配对差=`0.0`。
- 这一步正式闭合了“授权 cell → 原始 receipt/ledger → 主指标重算 → paired analysis → claim boundary”链，但仍只是同配置一致性校验；claim gate 明确禁止算法优越性、拥塞控制效果、Q0 最优性和论文统计结论。下一步才进入第一组有真实处理差异的算法/策略对照。

## 2026-08-21：PR #111 EXP1 capacity-routing 正式配对运行完成

- PR #111 已通过 CI 并 squash 合入，当前 main=`b6b975f5230c86460076b1549d2b680f23c79994`；canonical VM 已部署同一 SHA，deployment receipt SHA=`8fcbbd3f2a466ae718634a51439e281656c048de871c36f0224a66a5eb8b1701`，source tree SHA=`f6a11148ac25388f1e67957b2f5813689e233edca4d53324f26b0fa93bce31d5`。
- 矩阵 `EXP-20260821-EXP1-CAPACITY-R01` 固定同一 M-Lab measurement-proxy trace、100 Mbps（20 s、140 星、MCS、1 s 拓扑重匹配、control plane、seed=7），只改变 `routing.policy`：control=`hop`，treatment=`capacity`。授权 SHA=`9d0e189504bbd2669a88721bb92c58cfb36ead2154afb424b4cd452fbd58fa28`；两 cell 均在 VM 上自然结束、守恒通过、`research_eligible=true`，且 VM `receipt verify=verified`。
- 两臂结果：均为 2,756 offered、1,253 `DELIVERED`、1,270 `ACCESS_REJECTED`、233 `IN_SYSTEM_AT_STOP`、0 queue overflow；`delivery_rate=0.454644412191582`，预注册 `capacity-control` 配对差=`0.0`。两臂 ledger SHA 不同，说明策略确实走了不同的服务/时序路径，但在这一负载、这一 seed 和这一单配对下，交付数量没有变化。
- 从原始 ledger 独立重算：已交付包平均 `e2e_s` 为 control `0.294096`、capacity `0.292419`；平均 `total_queue_wait_s` 两臂均 `0.281647`；平均 propagation 为 `0.010584/0.009209`，平均 transmission 为 `0.001865/0.001563`。546 条链路的平均物理可用容量利用率为 `0.0002409/0.0002063`，最大值两臂均约 `0.01508`；metrics validation 均为 `ok=true`。
- VM `v2_analysis` 生成并验证 `ANALYSIS/EXP-20260821-EXP1-CAPACITY-R01/v2-paired/`，`verify_persisted_analysis` 返回 `ok=true, errors=[]`。这组证据可支持“固定 M-Lab burst profile 下的描述性零差异”，不能支持算法优越性、因果拥塞控制结论、Q0 最优性或论文统计结论；仍需多 seed/多负载和独立 claim review。

## 2026-08-21：正式 E0 低/中/高负载矩阵完成并闭合 V2 重算

- 正式包 PR #113（矩阵）与 PR #114（授权）已合入；六个 cell 使用同一授权 cohort、同一 VM 部署主线 `b39f0a72f4b02d34ccbf3592a4e68113795904dc`，deployment receipt SHA=`6d3b6ca1f6681248fe5881ac08102eb7d211a00b3430a25cd0b31af9214c855c`，authorization SHA=`d0337c35b247d6f548936cf7495bf2584352b7f644f8b5ada5e4bdd92779dcb3`。六次均自然结束、`research_eligible=true`，逐次 `receipt verify=verified`。
- 设计含义：50/100/200 Mbps 是 burst 前的 base offered rate；20 s 运行在 8--16 s 施加 2x burst，因此时间平均目标分别是 70/140/280 Mbps。每档 control/copy 是完全相同的非学习重复单元，不是算法比较。
- 六个原始回执的成对结果（control 与 copy 完全一致）：
  - low/load-50：1,299 offered，613 delivered，579 `ACCESS_REJECTED`，107 `IN_SYSTEM_AT_STOP`，0 overflow，delivery rate=`0.4719014626635874`；墙钟约 121/120 s。
  - medium/load-100：2,756 offered，1,253 delivered，1,270 `ACCESS_REJECTED`，233 `IN_SYSTEM_AT_STOP`，0 overflow，delivery rate=`0.454644412191582`；墙钟约 123/126 s。
  - high/load-200：5,551 offered，2,382 delivered，2,597 `ACCESS_REJECTED`，167 `HOLDING_QUEUE_OVERFLOW`，405 `IN_SYSTEM_AT_STOP`，delivery rate=`0.42911187173482257`；墙钟约 131/134 s。
- 原始 ledger 独立重算均通过；低/中/高档平均物理可用容量利用率约为 `0.00011595/0.00024093/0.00044596`，最大链路利用率约为 `0.00782/0.01508/0.02972`。中档已交付包平均 `e2e_s=0.294096`、排队等待=`0.281647`、传播=`0.010584`、传输=`0.001865`；其余档位同样保留逐包三段字段。
- 首次 V2 分析发现分析器把低档 contrast 错套到所有 pairing key，正确拒绝了该错误分析。PR #115 修复为“每个 contrast 只计算包含其左右臂的 pairing key；若某 key 只有一侧则继续 fail-loud”，CI 为 `546 passed, 1 skipped, 3 subtests passed`。合入主线 `e83653c907427f6b6bd2410119b914a330808755` 后重新部署，VM `v2_analysis` 返回 `VERIFIED`（6 runs），`verify_persisted_analysis` 返回 `ok=true, errors=[]`。
- 本组可支持：三档负载的重复一致性、原始负载/突发/端点选择/包命运和指标可重算证据；200 Mbps 已出现 holding overflow，可作为压力档。不能支持：最终 E0 阈值、跨档因果拥塞结论、算法优越性、Q0 最优性或论文统计结论。下一步是基于这张负载表冻结 E0 主档/压力档，再运行真实学习算法的正式 pilot。

## 2026-08-21：中负载真实流量四学习臂 train→checkpoint→eval 工程 pilot

- 运行范围：canonical VM 上已部署主线 `e83653c907427f6b6bd2410119b914a330808755`，deployment receipt SHA=`d7baa84dda74501132130f7b9aaf84a844b0336e1fb4a695e35668423adf096f`；固定 140 星、20 s、100 Mbps base + 8--16 s 2x burst、MCS、1 s 拓扑重算、M-Lab 56-cell measurement-proxy、seed=7，训练和评估均使用 trace SHA=`e6e7bd329f6822046f5d57611690d609a3647e1dca7639e170e985d891000e09`。
- DDQN/C3：训练自然结束、守恒、receipt verified，4,716 train steps，checkpoint verified SHA=`17ee9ae7b89a416f6fd667c4a168cdf4e4cb75ea6a973391bb4858326a989862`；评估 0 train steps、2,017 decisions，加载 SHA 与训练一致，receipt verified。
- Q-learning/C3：训练自然结束、守恒、receipt verified，5,086 train steps，checkpoint verified SHA=`943fda8cd60817040b7af9dd0e6680cfaf66e904344eb1a7a680c7145d7fd8b1`；评估 0 train steps、加载 SHA 与训练一致，receipt verified。
- DDQN/GAT：训练自然结束、守恒、receipt verified，4,975 train steps，checkpoint verified SHA=`59552ee9bafeb0051eb3fe7a49b143ef2cfd37eb3dbb2d5ecc3290b90f75dff6`；评估 0 train steps、3,252 decisions，加载 SHA 与训练一致，receipt verified。
- DDQN/MPNN：训练自然结束、守恒、receipt verified，5,068 train steps，checkpoint verified SHA=`727cee5fd512962154c90f336202095f90b82c670038bfb9f8e5b0c489534da9`；评估 0 train steps、3,332 decisions，加载 SHA 与训练一致，receipt verified。
- 这八个 run 是工程 pilot，不是正式授权矩阵，也不支持算法优越性或论文统计结论；它们证明当前 VM/依赖下四个学习路径在主负载上能真实训练、保存、重载、评估，且不会静默退化为无学习。下一步把同一 train/eval 证据装进正式 matrix/授权链，再进入拥塞/利用率诊断；正式评估仍需按 60--120 s 和多 seed 预算重新规划。
