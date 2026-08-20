# LEO 平台 V2 → VM 阶段交接文档（2026-08-13）

> **HISTORICAL HANDOFF**：本文不再是唯一交接面；当前部署与实验门禁见 `CURRENT-EXPERIMENT-READINESS.md`。

**性质**：本地实现已完成并通过冻结计划全部本地验证；本文档是进入"独立复核 → 三角色审阅 → 授权 → 部署 → VM 验收"阶段的唯一交接面。本文档不产生任何已完成 VM 工作的声明。

## 1. 当前状态基线（FACT）

- 工作树：`/private/tmp/m2-leo-platform-v2-runs/20260812T163928Z-22ae650a/worktree`，base commit `4fe918f`，分支 `m2/20260812T163928Z-22ae650a`，**全部改动未提交**。
- 交付物：`CODE/leo_sim/`（13 个运行时模块 + profiles/smoke.yaml + 17 个测试文件，266 测试）；6 份 ANALYSIS 报告；`NOTES.md`、`DECISIONS.md` 更新。
- 验证（解释器 `/private/tmp/m2-leo-platform-v2-verify/bin/python`，2026-08-13，Codex 接管封口后）：leo_sim **266 passed / 0 failed / 0 skipped**；旧回归 **337 passed / 17 skipped / 4 deselected / 21 subtests**；compileall、config validate、dry-run、tracked + untracked whitespace/conflict scan全过；开发栈与 VM 兼容栈 Walker smoke 均 `natural_end=true` + receipt verify `verified`；跨版本 receipt 按预期拒绝。
- 状态：**CODEX_LOCAL_ACCEPTANCE_CANDIDATE**。第四轮后发现的封口缺陷已由 Codex 直接修复；最终永久反例文件 93 passed。尚未提交、三角色审阅、部署或 VM 验收。

## 2. 提交策略建议（需用户批准后才执行；本轮约束禁止 commit/push）

工作树当前在 m2 分支上；按 Git 纪律应在源工作区建 `codex/20260812-platform-v2` 工作分支承载。**拆分已经过真实仿真验证**（2026-08-13,`/private/tmp/leo-v2-split-sim`：逐阶段复制文件子集并跑当时全部 leo_sim 测试）:import 图证明 `kernel.py` 依赖 `routing.py`/`learning.py`，两者不可分居不同 commit；故冻结计划书理想的 12 主题归并为可独立验收的 4 提交：

1. `feat: add leo_sim config, grid, trace and geometry model` — `__init__.py`、`config.py`、`grid.py`、`rng.py`、`trace.py`、`model.py`、`profiles/smoke.yaml` + 测试 `helpers.py`、`test_config/grid/trace/model`（仿真实测 **22 passed**;mlab 测试依赖已跟踪的 `CODE/data/traffic/mlab_2026-05-27.csv`，真实仓库中天然在场）。
2. `feat: add leo_sim kernel, routing and learning contracts` — `control.py`、`outage.py`、`fates.py`、`routing.py`、`learning.py`、`kernel.py` + 测试 `test_control/kernel/handover/fates_outage/outage_trace_gaps/routing/learning`（仿真实测累计 **88 passed**)。
3. `feat: add leo_sim receipt, CLI and governance surface` — `receipt.py`、`governance.py`、`__main__.py` + 测试 `test_cli/governance/review_regressions/review_round2/review_round3/review_round4`。此前拆分仿真 22/88/219 只对应 Codex 接管前版本，**已被本次封口改动作废**；提交前必须按当前 266 项重新验证拆分，不沿用旧数字。
4. `docs: platform-v2 reports, decisions and notes` — 6 份 ANALYSIS 报告 + NOTES.md + DECISIONS.md。

备选：代码+测试单 commit、文档单 commit 的两提交方案（牺牲粒度换简单）。每 commit 前 `git diff --check`，全部提交后跑完整 verify 电池再 push。

## 3. 独立复核入口（Codex / 三角色审阅）

- 复核对象：当前工作树未提交改动全体。建议 Codex 复核顺序：① `CODE/leo_sim/` 逐模块对照三份 REMEDIATION 报告的修复声明；② 重跑两个独立探针（`/private/tmp/leo_v2_review_round2.py`、`/tmp/leo_v2_round3_probe.py`）；③ 新的对抗性探针（如有）→ 转永久测试先红后绿。
- 三角色审阅（cold-start / satellite-DRL / adversarial）回执必须绑定**提交后的 commit hash**，故排在提交之后。
- 审阅重点提示：kernel.py 公平接入与 MBB 硬退休的竞争逻辑；model.py 几何认证的速率界合同；receipt.py 的 diagnostic vs authoritative 分级；learning.py 的信息边界。

## 4. VM 依赖对齐方案（进 VM 前必须解决，需用户批准）

实测差异：本地 SimPy **4.1.2** / NumPy **2.4.6**(leo-test-env 为 2.5.2)/ Python 3.12；VM(SimPy **4.0.1** / NumPy **1.24.3** / Python 3.11.15 / TF 2.13.1 仅见 CPU)。receipt 的 deps 精确绑定意味着 VM 产物必须在与 VM 一致的环境核验。

- **方案 B（本地已验证可行，推荐）**:leo_sim 已在 VM 同版本依赖栈上本地跑绿——`/private/tmp/leo-v2-vm-compat`(uv 安装的 CPython 3.11.14 + NumPy **1.24.3** + SimPy **4.0.1** + PyYAML **6.0.2**，全部落在 /private/tmp，未动系统/共享环境）:leo_sim **266 passed / 0 failed**、compileall、Walker smoke、receipt verify 与 dry-run 通过。非学习场景 VM 侧零依赖变更可行；唯一环境注意项是 SimPy 4.0.1 的 pkg_resources 弃用警告。
- **方案 A（备选）**:VM 新建独立 `leo-v2` 环境（venv 或 conda)，固定 SimPy 4.1.2 + NumPy 2.4.6 + PyYAML 6.0.3(+ TF 2.x 用于学习门）；共享 `leo-i39` 环境零改动。代价：一次安装审批与少量磁盘。仅在复核要求与本地开发栈完全对齐时采用。
- **学习门（两方案共同）**:TensorFlow 只在 VM leo-i39(TF 2.13.1，实测仅见 CPU;A100 空闲但不可见，不得声称 GPU)；其 NumPy 1.24.3 约束与方案 B 一致（TF 2.13 要求 numpy<1.25)。DDQN 的 TF 建模/训练/save-load 验收仍是 VM 专属门，本地不可替代。
- 进正式链前仍须在目标环境重跑 leo_sim 全测试 + Walker smoke 作为部署后验收步骤。receipt 的 deps 精确绑定已实测生效（2026-08-13)：用 verify-venv(NumPy 2.4.6/SimPy 4.1.2/Py3.12）核验 vm-compat 栈（1.24.3/4.0.1/3.11）产物，verify 退出码 2 并给出精确 deps 差异——**VM 产物必须用与 VM 一致的环境核验**。复核工具版本稳健性已实测：第二、三轮独立探针在 vm-compat 栈下复跑均 exit=0、判定一致。

## 5. VM 机制矩阵 runbook(20 项，每项独立 run)

前置：commit clean → push → 三角色审阅回执绑 hash → finalization → authorization → push-remote.sh 部署 main 干净 commit。

| # | 场景 | 关键配置（相对 smoke.yaml 的变更） | 通过判据 |
|---|---|---|---|
| 1 | 直连 endpoint→sat→ISL→sat→endpoint | 默认 smoke | natural_end + DELIVERED≥1 + 守恒 |
| 2 | K 槽与目的端接入限制 | `access.slots_k=1`，多端点竞争 | 有界服务、无永久饥饿、access 账本平衡 |
| 3 | 上/下行/ISL 队列溢出 | 小队列 cap + 高负载 trace | 溢出 fate 计数与账本一致 |
| 4 | 端点公平 | 异长包混合 | DRR bit 公平界内 |
| 5 | BBM | 默认 | 切换事件符合 hysteresis/dwell/acquisition |
| 6 | 能力门控 MBB | 终端 dual_connect=true | 新链走新包、旧链硬退休、无重复 fate |
| 7 | GSL 几何失效 | 移动星座+长 horizon | GEOMETRY_LOSS_IN_FLIGHT 与占用记账一致 |
| 8 | ISL 几何失效 | 同上（ISL 方向） | 同上（ISL 账本） |
| 9 | GSL GE 中断 | `links.gsl_ge` 启用 | RANDOM_OUTAGE 独立于几何损失计数 |
| 10 | ISL GE 中断 | `links.isl_ge` 启用 | 同上 |
| 11 | 中途掉线后恢复仍失败 | 短 bad 驻留 GE | 当前包失败、已耗服务记账、不续传 |
| 12 | 控制带宽竞争/非抢占 | 小 ISL 容量 + 控制开启 | 控制优先但不打断在传数据 |
| 13 | vis_k/TTL/AoI | 多跳拓扑 | 传播跳数 ≤vis_k、过期不人用 |
| 14 | stale cache | 长 TTL + 移动拓扑 | 无路由决策使用过期条目 |
| 15 | 数据 deadline | 短 deadline | DATA_DEADLINE_EXPIRED 正确命中 |
| 16 | no route/环路上限 | 隔断拓扑 | NO_ROUTE、无无限循环 |
| 17 | horizon 未完成 | 长包 + 短 horizon | IN_SYSTEM_AT_STOP、stop==horizon |
| 18 | 数据+控制守恒 | 任意 | 双账本守恒等式成立 |
| 19 | receipt 篡改拒绝 | 跑后改 receipt/ledgers | verify 非零退出 + 精确错误 |
| 20 | TensorFlow DDQN smoke | learning 启用（方案 A/B 环境） | 建模/推理/一步训练/mask/save-load/固定 seed 重现 |

每个 run 必须保存：resolved config、trace、seed、code/dependency identity、natural_end/interrupted 状态、receipt、ledgers。完成条件：natural_end=true、interrupted=false、SHA 一致、requested/effective 机制匹配、fate 唯一、守恒成立、产物闭环、research_eligible 明确。

## 6. 禁止事项（本阶段继续有效）

不覆盖共享 `leo-i39` 环境；不 rsync 半成品；不直接在 VM 改代码；不把 SSH smoke 当正式验收；不删除 VM Results 与历史证据；未经用户逐路径批准不 `git rm`；hosted CI 若仍受账单阻塞只能标 "hosted CI blocked"。

## 7. 立即需要用户的决定

1. 批准提交策略（第 2 节）并授权 commit/push；
2. 确认依赖对齐方案（**方案 B 已经本地验证可行并转为推荐**：VM 同版本栈 266 测试全绿；A 为备选）；
3. 确认 Codex 复核与三角色审阅的启动方式。
