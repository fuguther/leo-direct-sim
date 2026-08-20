# 验收阶梯（Acceptance Ladder）v1

> **SUPPORTING PROTOCOL**：验收方法继续有效；当前门禁状态见 `CURRENT-EXPERIMENT-READINESS.md`。

> 日期：2026-08-16。判据来源：论文主线「路由状态信息的年龄对 LEO DRL 路由的影响」——一切验收以「是否服务信息年龄主线」为取舍标准。
> 已有支撑资产：`test_analytic_scenarios.py`（解析锚点）、`test_reward_migration.py`（reward/观测 golden）、`acceptance.py`（五机制验收）、`comparison.py` + 决策快照（双臂差分）、`receipt.py`（回执）、`fates.py`（双账本守恒）。

## 三层判据

### A 层：等价层——点对点可解析

**判据**：最小场景的正确值可由配置参数解析推出，平台输出与之精确相等（容差 ≤1e-9 或数学恒等）。

- 时延/计数锚点：`test_analytic_scenarios.py`（单星直连、两跳转发、槽满等待、horizon 在途结算）。
- 训练语义锚点：`test_reward_migration.py`（M1 队列奖励 golden、M2 逐方向观测 golden、deliver=ArriveReward）。
- 学习数学锚点：`ddqn_targets`（online argmax + target eval + next mask + terminal 不 bootstrap），`test_learning.py` / `test_acceptance_review.py`。
- 通过标准：全部精确断言绿；任一红 = 平台行为漂移，禁止口头解释带过。

### B 层：机制层——每个机制对自己的合同

**判据**：机制开启时，其合同声明的可观察效应必须真实出现在账本/事件流中（不是「跑完没崩」）；机制关闭时其效应必须完全消失。

| 机制 | 合同（可观察效应） | 现有验收点 |
|---|---|---|
| 接入（K 槽+DRR+租期） | 槽数上限永不超；等待 FIFO 有序；占用/等待时间入账 | acceptance k1：single_slot_never_exceeded 等 |
| BBM/MBB 切换 | BBM 先断后建不抢占在服务包；MBB 旧链 retiring 排空、硬退休兜底 | acceptance bbm/mbb |
| GE 随机中断 | 在传中中断产生 RANDOM_OUTAGE_IN_FLIGHT fate；计数器>0 | acceptance ge |
| 控制面 AoI/TTL | 过期条目不进观测（`test_expired_or_future_entries...`）；C1 只看一跳、C3–C7 同信息集（`test_c3_to_c7_share_exactly_the_same_information_set`） | test_learning.py |
| 学习合同 | 观测维度/掩码合法/reward 公式（任务 1 修复后语义） | test_learning.py + test_reward_migration.py |
| receipt/守恒 | offered = delivered + loss + in_system；每包唯一 fate | fates.py 每次 run 强制 |

### C 层：系统层——差异可归因

**判据**：整跑级别的任何指标差异，必须能归因到某个已知机制差异或已记录的语义差异（见 `REWARD-DIFF-20260816.md` 的「有意差异」清单）；出现「无法归因的差异」本身即验收失败。

- 双臂对照：`comparison.py` 同 trace 差分 + 逐跳决策快照（任务 3）：直臂逐跳（候选/动作/观测摘要）vs 旧臂路径级（只读约束下的最大粒度）。
- 归因链：指标差 → 决策快照 diff 定位首个分歧跳 → 该跳的候选集/观测/掩码 → 机制差异。
- 声明纪律：`scientific_effect_claim=False`（comparison summary 硬编码）；系统层 PASS 只声称「工程等价/差异已归因」，不声称算法优劣。

## 不变量清单（任何 run 必须满足；违反即 fail-loud 或验收失败）

1. **比特守恒**：offered = delivered + terminal_loss + in_system（fates.py:83-90 强制）。
2. **唯一终态**：每包恰好一个 fate；horizon 无 fate 包记 IN_SYSTEM_AT_STOP。
3. **无未来信息**：几何只在 `env.now` 查询（certified next-change 仅供调度器，模型 docstring 合同）；观测只含已到达且未过期控制条目（control.LocalCache）；学习掩码只用当前本地状态（build_action_mask 注释合同）。
4. **掩码合法**：学习所选动作 ∈ 掩码（deliver-only 掩码选非 deliver 即 KernelError，kernel.py:1432-1433）。
5. **reward 有界且语义固定**：逐跳 M1 ∈ (0, w1]；deliver = arrive_reward；fail terminal = 0.0；转移完结时 reward 未结算即 KernelError。
6. **确定性**：同 config+seed+trace → 同结果（同刻发射按 packet_id 排序等已有测试覆盖）。
7. **时间单调与 horizon 精确**：时钟必达精确 horizon（_horizon_closer）；在途服务占用结算到 stop 时刻（任务 2 场景 4 锚定）。
8. **fail-loud**：配置解析/trace/信息条件/receipt 不符即阻止运行，不允许静默回退（AGENTS.md 硬事实 4）。

## 机制逐个加挂的差分玩法

基线 = 全机制关（oracle 路由、无控制面、无 GE、geometry_loss 开、单星直连可解析场景）。每加挂一个机制，重跑同 trace 并回答三个问题：

1. 该机制合同声明的效应是否出现（B 层验收点）？
2. 相对上一档的 fate/时延/决策快照差异是否全部由该机制引起（C 层归因）？
3. 关掉它是否精确回到上一档（回归）？

加挂顺序（与信息年龄主线的相关度排序）：控制面（AoI/TTL/vis_k）→ 学习合同（C1→C3→C4–C7→GAT/MPNN）→ GE 中断 → MBB → 容量策略。每档产出：决策快照 diff 首个分歧点 + 归因说明（进 PR 正文）。

## 变异测试第一批注入清单

每个变异 = 一处单点语义破坏 + 指定期望捕获它的现有/新测试；注入后测试必须红，恢复后必须绿。

| # | 注入点 | 变异 | 期望捕获 |
|---|---|---|---|
| M-1 | learning.queue_reward | `w1·exp(−β·t)` 改为 `exp(−t)` | test_reward_migration golden 红 |
| M-2 | kernel._transmit reward 结算 | 用入队时刻占用比代替实测等待 | test_reward_migration 端到端红 |
| M-3 | kernel._decide 环回避 | 删除 `not in pkt.path` 过滤 | 新测试：构造回环场景断言无环 → 红 |
| M-4 | learning.build_action_mask | 掩码放行无 room 方向 | 新测试：掩码 ∩ 实际 room → 红 |
| M-5 | control.LocalCache | 观测读入过期条目（ttl 检查删除） | test_expired_or_future_entries 红 |
| M-6 | kernel._horizon_closer | 时钟停在上个事件不到 horizon | test_analytic_scenarios 场景 4（stop_time/occupied）红 |
| M-7 | fates 守恒 | close_at_stop 漏记在途包 | check_conservation 直接 raise |
| M-8 | geometry 未来信息 | 观测/路由读 t+Δ 几何（把 `now` 换成 `now+step`） | 新测试：观测对未来几何摄动不变 → 红 |
| M-9 | ISL 控制优先级 | 数据包越过排队控制包 | 新测试：控制优先顺序断言 → 红 |
| M-10 | ddqn_targets | terminal 也 bootstrap | test_acceptance_review / test_learning 红 |

执行方式：手工逐条注入（不提交），跑对应测试确认红，还原确认绿；结果记入晨报或后续变异测试工作包。M-3/M-4/M-8/M-9 的捕获测试当前不存在，是本清单自带的测试缺口，优先补。
