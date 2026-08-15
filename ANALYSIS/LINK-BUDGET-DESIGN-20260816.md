# 链路预算（香农/MCS 速率）集成设计稿

> 日期：2026-08-16。范围：设计稿 + 表征测试（`test_link_budget_characterization.py`），**集成代码留后续工作包**（任务 7 明示）。
> 主线动机（MIGRATION-BACKLOG B5）：新平台链路速率是配置常数；E1 已发现瓶颈在接入侧，速率建模直接影响信息年龄主线结论。计划原文要求「经表征测试确认正确的链路预算计算」明确保留。

## 1. 旧侧行为（表征测试已固定）

| 函数 | 位置 | 语义 |
|---|---|---|
| `los_slant_range` | SimulationRL.py:8282 | 距离矩阵逐元素与 per-class 上限比较，超限置 `inf` |
| `get_data_rate` | SimulationRL.py:8295 | FSPL → SNR → **MCS 量化速率**：`B·max{speff_i : lin_i ≤ snr}`，无可行 MCS 记 0 |
| `RFlink` 派生量 | :1798-1811 | `G=2·Gtx−2·pointingLoss`、`No=10log10(B·k)+NF+…`（常数 :297-299，interISL 参数 :8353-8363） |

关键事实（golden 测试钉死）：
- **`get_data_rate` 计算的 `shannonRate`（:8315）不进入返回值**——返回的是 MCS 门限表量化速率（:8318-8326）。集成时若直接接香农速率将偏离旧行为。
- 旧 RF 参数下速率随距离阶梯衰减：1000 km→1.81 Gbps，2000 km→0.99 Gbps，4000 km→0.44 Gbps，**6000 km（新平台默认 max_isl_km）→ 0**（SNR 0.49 < 最低门限 0.5188）。即「常数 1 Gbps」的新平台默认在长距 ISL 上不可由旧链路预算复现——差分时必须说明。
- 表征测试出处：`CODE/leo_sim/tests/test_link_budget_characterization.py`（公式按说明书行号以 math/numpy 重算，golden 值钉死；单调性/峰值/零速率性质断言）。

## 2. 新平台集成方案

### 2.1 接入点

服务时长三处（当前 `dur = bits / rate_bps`）：
- `ISLLink._run`（kernel.py:529 一带）：ISL 服务时长；
- `UplinkServer` / `DownlinkServer`（kernel.py:255/343 一带）：GSL 服务时长。

接入方式：速率改为**每次服务开始时**按当时斜距采样一次（`geometry.isl_range_km(sat, peer, t)` / `slant_range_km(sat, lat, lon, t)`——两者已是传播时延的现有查询点，服务期间速率固定）。理由：`_transmit` 的竞态语义（服务完成 vs 失效）以固定 dur 为前提，服务中途变速会污染「已占用服务时间」记账；逐服务采样保留了距离依赖且不动竞态单点。

### 2.2 配置面（草案）

```yaml
links:
  rate_model: "constant" | "mcs"      # 默认 constant（现状，不破坏既有回执）
  rf:                                  # rate_model=mcs 时必填，缺省 fail-loud
    frequency_hz: 26e9
    bandwidth_hz: 500e6
    max_ptx_w: 10.0
    antenna_diameter_m: 0.26
    pointing_loss_db: 0.3
    noise_figure_db: 2.0
    noise_temperature_k: 290.0
    min_rate_bps: 10000.0             # 低于此速率视为不可用（见 2.3）
  mcs_table: "legacy-dvbs2x"          # 门限表选择；先只支持旧表（表征测试钉死）
```

校验（fail-loud）：`rate_model=mcs` 时 rf 字段缺/非正 → ConfigError；`constant` 时忽略 rf。

### 2.3 零速率/低速率的语义（必须先拍板再实现）

旧平台速率 0 的边在选路权重里天然不可用；新平台服务模型里「速率 0」没有对应物（dur=∞）。方案：**速率 < min_rate_bps 的链路在服务开始点视为不可用**（等同链路 down：排队等待恢复，deadline 到期由 `_expire_waiting`/`_transmit` 既有路径收 fate）。这保持守恒与 fail-loud，且与 los_clamp 置 inf 的旧语义对应。选路层（routing.choose_next_hop 的 capacity 策略）若要用速率，同源读取，不另开信息通道。

### 2.4 对 receipt / 守恒 / 观测的影响

- **守恒**：速率只改变时序不改变比特账目，`check_conservation` 不受影响；horizon 在途结算（occupied）按实际服务时间入账，既有断言（任务 2 场景 4）在 constant 默认下不变。
- **receipt**：rf 参数经 resolved config 自动进 receipt；新增 mechanism counter（如 `mcs_rate_samples` 分布摘要或 min/median/max）进 ledgers，保证 C 层可归因。`mechanisms.requested/effective` 增 `rate_model` 项。
- **观测**：own_state / origin features 目前不含速率——v1 不进观测（避免再次改合同维度）；capacity 路由若用速率需单独评审信息合同（不得引入未来信息：只用当前时刻斜距）。
- **决策快照**：decision_sink 可附所选链路的采样速率（纯输出，便于差分归因）。

## 3. 验证计划（实现 PR 的完成标准）

1. 表征测试直接复用 `test_link_budget_characterization.py` 的 golden：新实现 `rate = f(slant)` 与四个钉死值一致（rel 1e-9）。
2. 解析场景：固定几何下 mcs 模式的单跳时延 = 传播 + bits/rate(slant) 手算值（容差 1e-9）。
3. 差分：同 trace constant vs mcs 两臂，时延/决策差异可归因到速率采样记录。
4. 零速率：slant > 门限的链路服务不开始、包排队、fate 正确。
5. 默认 `constant` 下全部既有测试与回执行为不变（回归）。

## 4. 待用户决定

- MCS 门限表是否就用旧平台这张（疑似 DVB-S2X 变体，出处未在旧库注明）——用旧表可差分对照，用标准表更可辩护但偏离旧数值。
- 速率是否进学习观测（v1 不进）。
