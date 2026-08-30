# 旧平台功能差距账本（V2 可实验门禁版）

> **SUPERSEDED**：本文的实现状态已经过期，只保留旧平台差距证据。当前迁移状态与取舍见 `PLATFORM-CAPABILITY-LEDGER.md`。

日期：2026-08-19。参照：`ANALYSIS/LEGACY-DESIGN-AUDIT-20260819.md`、
`ANALYSIS/PLATFORM-DOCUMENTATION/02-kimi-platform-spec.md`、
`ANALYSIS/MIGRATION-BACKLOG-20260816.md` 及当前 `CODE/leo_sim/`。

## 判定规则

- `已合入`：主分支有代码、测试和提交证据。
- `分支实现/待复核`：代码在独立分支，但未完成独立冷启动复核，不能用于正式结论。
- `已知未实现`：差异已确认，尚无实现。
- `有意取舍`：新平台明确选择不同语义，并有文档依据；不是遗漏。
- `未验证`：已有线索，但还没有当前平台的直接证据。
- `需补枚举`：不是说没有该功能，而是旧平台全量对照尚未达到可宣布完备的程度。

## 功能对照表

| 功能/旧平台优点 | 旧平台证据 | V2 当前证据 | 状态 | 对近期实验影响 | 处置 |
|---|---|---|---|---|---|
| 距离→SNR→MCS 动态速率 | `SimulationRL.py:8295`, `:2361`, `:5038` | D1 分支 `c0a1f18` 有 `link_budget.py` 与集成测试；主分支仍为常数速率 | 分支实现/待复核 | 高，影响时延、拥塞、AoI | 修正服务/队列语义后独立复核 |
| 跨面 ISL 邻居随轨道重匹配 | `:5183`, `:8330` | D2 分支 `7cb11e8` 已实现周期重算；未独立复核、未合主 | 分支实现/待复核 | 5 秒窗低，长时窗高 | 独立复核；默认保持静态 |
| 面内 N/S 邻居 | `findIntraNeighbours` | `Constellation.neighbors` | 已合入/等价 | 中 | 保持 |
| 未来/多步回报、TD-λ、temporal/GRU | `:6980-7062`, `temporal_encoder.py` | 只有设计稿 `TEMPORAL-MULTISTEP-DESIGN` | 已知未实现 | 对长信用分配高 | 先不阻塞基线；另立研究臂 |
| Path-credit 轨迹信用分配 | `routing_path_credit.py` | 未见运行时接线 | 已知未实现 | 仅影响 path-credit 研究臂 | 先不阻塞平台基线 |
| 每星独立策略、FL、CKA | `:1499-1679` | V2 明确单共享模型，无 FL/CKA | 已知未实现 | 仅影响分布式研究臂 | 先出设计稿，不混入默认路径 |
| per-action 斜距/速率/目的地方向特征 | `getDeepStateRAACGraph:9791` | V2 图观测无等价 4×9 action_feats | 已知未实现 | 影响观测消融解释 | 冻结信息合同后决定 |
| M3 队列速度与 EMA 趋势 | `getDeepStateDiff:10041` | V2 只有瞬时队列/AoI | 已知未实现 | 影响拥塞趋势臂 | 单独观测消融 |
| 每包 queue/tx/prop 三分量时延 | `getBlockTransmissionStats:1324` | V2 有 queue area/occupied，但等价 per-block 输出未逐字段确认 | 未验证 | 影响论文 KPI | 当前先补核验，不猜测补零 |
| replay buffer 保存/加载/续训 | `:10475-10492`, `SIM_REPLAY_PATH` | V2 仅 checkpoint，无 replay 持久化 | 已知未实现 | 长训可靠性高，短基线低 | 中优先基础设施 |
| 按决策步/GT 数 epsilon 调度 | `alignEpsilon:7315` | V2 按仿真时间 `epsilon(now)` | 有意差异/需评估 | 影响训练动力学 | 在实验合同中显式声明 |
| stopLoss 早停 | `train:7559` 附近 | V2 未实现 | 已知未实现 | 长训成本 | 后续 |
| 中断安全保存 | `save_on_interrupt:11356` | V2 formal 以自然结束回执为完成条件 | 有意取舍 | 长训中断会损失中间产物 | 可做 opt-in，不改变 formal 门 |
| MAPPO / centralized critic / frame stack | `routing_mappo.py` | V2 无运行时实现 | 已知未实现 | 仅 MAPPO 研究臂 | 不阻塞 DDQN/Q-learning 基线 |
| FSOlink、旧链路容器与旧 dashboard | 旧平台依赖模块 | V2 无对应物；当前目标是直连仿真 | 有意范围差异 | 不影响当前直连目标 | 不迁移，需在论文范围声明 |
| 旧平台 burst/diurnal 运行时乘子 | 旧平台运行时调度器 | V2 在 trace 编译期表达流量机制 | 有意实现差异 | 需确认实验合同是否要求运行时变化 | 做一组等价验收 |
| 旧平台大量未接线变体/死代码 | `kimi-platform-spec` 未确认清单 | V2 只保留已接线机制 | 有意清理 | 不应把死代码当优点 | 不迁移 |
| 旧平台错误的重排队/过程更新语义 | `updateSatelliteProcessesRL` 注释承认不正确 | V2 D2 选择 pending 回退并保留退役链路 | 有意改进，待复核 | 长时窗需差分说明 | 保留设计理由和守恒测试 |

## 仍可能遗漏的类别

以下不是已确认缺口，而是三轮完备性审计必须逐项打勾的目录：

1. 物理链路：RF 参数、天线/噪声、FSO、遮挡、传播、链路中断、速率表和边界。
2. 拓扑与调度：邻居匹配、路径重算、服务优先级、不可抢占、队列容量、重排队、接入槽和切换。
3. 观测：节点、边、动作级特征、AoI、缓存 TTL、远端队列、未来信息、历史堆叠。
4. 学习：奖励、终止、n-step/TD-λ、探索调度、replay、checkpoint、每星模型、FL、早停。
5. 需求与流量：trace 编译、burst/diurnal/hotspot、人口重力、deadline、OD、seed/RNG。
6. 工程与证据：自然结束、receipt、守恒、artifact、VM 资源、失败重试、分析重算和 claim 门。

当前结论：D1-D10 不是“旧平台全部功能清单”，只是第一版高价值差距清单。
在三轮三方审计完成前，不能宣称“没有更多旧平台优点遗漏”。
