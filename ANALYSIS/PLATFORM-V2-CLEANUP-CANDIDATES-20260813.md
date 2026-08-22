# LEO 平台 V2 旧机制清理候选清单（2026-08-13)

> **HISTORICAL CANDIDATES**：本文不是当前删除清单，任何路径都不得按本文自动移动或删除。当前能力取舍见 `PLATFORM-CAPABILITY-LEDGER.md`，实际清理仍须重新核对引用并逐路径取得用户批准。

**本文件只列候选，不执行任何删除。** 依据冻结任务书：新平台未通过正式 VM 验收前，旧 Gateway 运行时只冻结、不删除；任何 `git rm` 必须等用户逐路径批准。恢复依据对所有候选相同：tag `pre-platform-v2-20260812`(commit `4fe918f`）与已验证 bundle `~/Desktop/LEO-Research-Workspace-backups/LEO-Research-Workspace-pre-platform-v2-20260812.bundle`；更早还有 `legacy-baseline-20260803` 与其 bundle。

引用计数命令（工作树根目录）:`grep -rl "<name>" CODE --include='*.py'`。A/B 节引用簇于 2026-08-13 三轮修复后复核更新（排除被引文件自身、`__pycache__` 与 `CODE/leo_sim/`)。

## A. Gateway 业务路径（V2 已被 leo_sim 替代）

| 候选路径/符号 | 用途 | 删除原因 | V2 替代 | 剩余引用（实测） | 删除前验证 |
|---|---|---|---|---|---|
| `CODE/SimulationRL.py` 内 Gateway 类与 `linkSats2GTs`、Gateway→Gateway 数据路径 | 旧正式主线：Gateway 作为业务源/宿 | 新路径不允许 Gateway 充当源/宿/隐式兜底 | `CODE/leo_sim/kernel.py`(TrafficEndpoint+Satellite 接入/ISL/下行） | 本体 12332 行；被 `CODE/run.py` 等引用 | leo_sim VM 验收通过 + `grep -rn "Gateway" CODE` 只剩注释/历史 |
| `CODE/Gateways.csv` | Gateway 地理表 | 新路径用稀疏网格端点 | `leo_sim/grid.py` + trace manifest | 2026-08-13 复核共 **2 个引用文件**:`CODE/SimulationRL.py`、`CODE/experiment_platform/compile_experiment.py` | 上述引用全部迁移或同步删除后回归全绿 |
| `CODE/inputRL.csv`、`CODE/inputRL_20gt.csv`、`CODE/inputRL_legacy_4gt.csv`、`CODE/input.csv` | 旧流量/Gateway 输入 | 需求由不可变 trace 取代 | `leo_sim/trace.py` 编译产物 | 2026-08-13 复核共 **9 个引用文件**:`CODE/SimulationRL.py`、`CODE/config/default.yaml`、`CODE/run.py`、`CODE/experiment_platform/compile_experiment.py`、`CODE/scripts/experiments/job_runner.py`、`CODE/scripts/remote/remote_job.py`、`CODE/tests/test_remote_workspace_scripts.py`、`CODE/tests/test_run_config_safety.py`、`CODE/tests/validate_burst_rates.py`（与 Gateways.csv 簇不同，不得混并） | 同上 |
| `CODE/traffic_od.py`、`CODE/traffic_burst.py`、`CODE/traffic_diurnal.py` 的 Gateway 绑定运行时 | 旧在线流量生成 | 流量生成前移为离线 trace 编译 | `leo_sim/trace.py`(burst/diurnal/uniform/gravity/hotspot 已迁移） | 各有测试引用 | 行为等价由 trace 测试锁定后，旧运行时回归不再被引用 |

## B. 旧算法/开关（不进入 V2)

| 候选路径/符号 | 用途 | 删除原因 | V2 替代 | 剩余引用（实测） |
|---|---|---|---|---|
| `CODE/routing_mappo.py` | MAPPO 路由 | V2 明确排除 MAPPO | 无（dead 方向） | 2 个文件引用 |
| `CODE/routing_multistep.py` | multistep/temporal | V2 排除 | 无 | 1 个文件引用 |
| `CODE/routing_path_credit.py` | path-credit | V2 排除 | 无 | 4 个文件引用 |
| `CODE/temporal_encoder.py` | temporal/GRU 状态 | V2 排除（其 3 个本地环境失败测试属既有基线） | 无 | 5 个文件引用 |
| SimulationRL 内 Q-Learning、C2、`dataRate`/`dataRateOG` 重复入口、M1/M2/M3 开关、线性奖励、旧 checkpoint 兼容代码 | 旧补丁开关 | M1/M2 语义已吸收为统一基线，开关删除；M3/线性奖励不进入 V2 | `leo_sim/learning.py`(canonical DDQN 合同） | 均在 SimulationRL.py 内 |
| `CODE/routing_hooks.py` 中仅服务旧入口的钩子 | 旧插件点 | 新内核不使用 | 无 | 2 个文件引用 |

## C. 兼容层与外围

| 候选 | 用途 | 删除原因 | V2 替代 | 备注 |
|---|---|---|---|---|
| 大量 `SIM_*` 环境变量别名（散见于 `CODE/run.py`、`CODE/SimulationRL.py`) | 旧参数桥 | V2 子进程只接收密封配置路径+SHA | `leo_sim/config.py` resolved config | 需逐符号扫描后列精确清单 |
| 仿真内绘图代码 | 旧在线绘图 | V2 默认不绘图，离线分析 | `outputs.plotting=false` + ANALYSIS 离线脚本 | 与 monitor.py 区分：monitor 有 10 个引用文件（2026-08-13 复核），多数属运行收据链，**不在候选内** |
| `CODE/data/geoip`、旧静态网页、旧生成配置脚本 | 旧输入/展示 | 待无引用核查 | 无 | 2026-08-04 死代码盘点已列，未删 |

## 明确不清理（保留）

- 轨道/几何/ISL/链路预算计算中经测试确认正确的部分（V2 的 `leo_sim/model.py` 为独立重写，旧实现留作对照）。
- 人口栅格、M-Lab 原始数据（`CODE/data/traffic/`）及 provenance。
- 实验治理链：`CODE/experiment_platform/`、`CODE/work/`、`CODE/scripts/remote/`、scheduler、receipt、manifest、分析工具。
- `CODE/monitor.py`、`CODE/link_outage.py`、`CODE/traffic_mlab.py`（引用面大或是 V2 数据来源；link_outage 思想已由 `leo_sim/outage.py` 重实现，旧文件留待对照期结束后再评估）。
- 全部历史 EXPERIMENTS/、ANALYSIS/、Git 历史、VM Results。

## 执行门（冻结）

1. leo_sim 通过正式 VM 验收（三角色审阅+授权+自然结束收据）。
2. 正式入口切换为 `python -m CODE.leo_sim`。
3. 上表每项补"剩余引用=0"的扫描证据。
4. 用户逐路径书面批准后才允许 `git rm`；删除后立即全量回归 + VM smoke。
