# NOTES.md

> ROLLING LOG；最后整理：2026-08-20。
> 本文件只记录最近操作、证据位置和下一步，不是平台状态真相源。
> 当前状态见 `ANALYSIS/CURRENT-EXPERIMENT-READINESS.md`；截至 2026-08-19 的原记录见
> `ANALYSIS/HISTORY/NOTES-THROUGH-20260819.md`。

## 记录规则

- 任务级证据放 PR；本文件只在合并改变当前平台状态、风险或下一步时更新。
- 设计解释写入对应 CURRENT/SUPPORTING 文档，NOTES 只留链接。
- 当前周期结束后原样归档；不得通过压缩删除失败、REQUEST_CHANGES 或未验证记录。
- 实时问题状态只在 `ANALYSIS/FINDINGS-REGISTRY.md` 更新。

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
