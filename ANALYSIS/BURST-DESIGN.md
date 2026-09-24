# BURST-DESIGN — Burstiness 实验合法性设计与两个模式

> 本文件即任务书第六阶段要求的 `burst_experiment_design.md`（文件名为验收标准所列的
> `BURST-DESIGN.md`）。

| 字段 | 值 |
| --- | --- |
| MAIN_SHA | `549acd8b7cb7a1bb573e7146653f55273999086d` |
| 日期 | 2026-09-24 |
| 取证 | 全部数字为 **[EXEC]** 实跑所得，命令见 §6 |
| 涉及代码 | `CODE/leo_sim/trace.py`（`_rate_multiplier` 302-321、生成 733-770）、`CODE/leo_sim/config.py`（83-98、570-597、291-293） |

---

## 1. 问题：现有 burst 旋钮是**混淆**的

平台的 burst 机制是一个**两级阶跃速率乘子**：

```
_rate_multiplier(mode, t, src_lon, dm)                     trace.py:302-307
    if start <= t < start + dur:  return burst_multiplier      # B
    return 1.0

generation:  max_mult = max(1.0, burst_multiplier)             trace.py:757
             draw  ~ exponential(1 / (base_rate * max_mult))   trace.py:765-770
             thin  ~ m(t) / max_mult
base_rate:   lambda_i = (offered_mbps*1e6/packet_bits) * w_i/sum(w)   trace.py:733-737
```

即：瞬时到达率 `λ_i · m(t)`，其中 `m(t) ∈ {1, B}`，突发窗 `[start, start+W)`。

**地平线 `[0,T)` 上的平均乘子**：

```
mean_mult = 1 + W·(B − 1) / T          ⇒     平均 offered load = offered_mbps × mean_mult
```

因此：

- 固定 `(W, T)` 只改 **B** → 平均负载 **和** 突发幅度**同时**变；
- 固定 `(B, T)` 只改 **W** → 平均负载 **和** 突发时长**同时**变。

> **结论：任何"只动一个 burst 旋钮"的实验都无法把效应归因于 burstiness。**

---

## 2. 实测证据（混淆是真的，不是推理）

固定 `duration_s=40`、`offered_mbps=50`、`packet_bits=1e6`、`seed=7`、`burst_start_s=8`
（`mode=burst`，均匀目的）。统计量：1 s 分箱到达数的**方差/均值比（Fano 因子）**，
Poisson 基准 = 1。

| B | W | mean_mult | 实测 offered (Mbps) | 预测 offered×mult | **Fano** | 峰值箱 | 空闲箱 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0 | 8 | 1.00 | 49.150 | 50.00 | **0.808** | 61 | 0 |
| 2.0 | 8 | 1.20 | 58.975 | 60.00 | **9.438** | 115 | 0 |
| 3.0 | 8 | 1.40 | 70.100 | 70.00 | **27.160** | 176 | 0 |
| 2.0 | 16 | 1.40 | 69.025 | 70.00 | **10.838** | 115 | 0 |
| 5.0 | 4 | 1.40 | 69.475 | 70.00 | **56.138** | 277 | 0 |

**读法**：

1. **负对照成立**：`B=1`（无突发）Fano = 0.808 ≈ 1，与 Poisson 一致 —— 统计量没有系统性偏差。
2. **混淆被证实**：只把 `B` 从 2 改到 3（`W=8` 不动），实测负载 **58.975 → 70.100 Mbps（+18.9%）**，
   同时 Fano **9.44 → 27.16（+188%）**。只看这一个旋钮的实验**不能**说"效应来自 burstiness"。
3. **Mode A 的可行解已经存在**：`(B=3,W=8)`、`(B=2,W=16)`、`(B=5,W=4)` 三者
   `mean_mult` 全为 **1.40**，实测负载落在 **69.0–70.1 Mbps**（极差 ≈1.6%），
   而 Fano 依次 **27.2 / 10.8 / 56.1** —— **在几乎相同的平均负载下得到 5.2 倍的突发度范围**。
   即：**沿双曲线 `W·(B−1) = const` 联动，就能用现有旋钮实现"固定平均负载、只变突发度"。**

---

## 3. 两个模式（设计定义）

### Mode A —— 固定平均负载，改变 burst 系数

**做法**：令 `C = W·(B − 1)` 为常数（`mean_mult = 1 + C/T` 恒定），在超曲线上取若干点。

可直接使用的三个点（已实测，`T=40`，`C=16`，`offered_mbps=50`，`burst_start_s=8`）：

| arm | burst_multiplier B | burst_duration_s W | mean_mult | 实测 Mbps | Fano |
| --- | --- | --- | --- | --- | --- |
| A0（负对照，无突发） | 1.0 | 8 | 1.00 | 49.150 | 0.808 |
| A1 | 3.0 | 8 | 1.40 | 70.100 | 27.160 |
| A2 | 2.0 | 16 | 1.40 | 69.025 | 10.838 |
| A3 | 5.0 | 4 | 1.40 | 69.475 | 56.138 |

**A1/A2/A3 之间平均负载一致（±1.6%），突发度相差 5.2 倍。** 这是 Mode A 的合法对照骨架。

**⚠️ 设计规则限制（必须如实声明）**：Mode A **同时改动两条参数路径**
（`demand.burst_multiplier` 与 `demand.burst_duration_s`）。
平台的严格设计规则要求「恰有一个变化因素」，因此 Mode A 只能编译为
`exploratory_multi_factor`，并且：

> **Mode A 允许运行，但不得声称单因素因果。**（AGENTS.md / AGENT_EXPERIMENT_PROTOCOL.md「设计规则」）

这**不是**平台缺陷 —— 平台把"平均负载"显式建模为两个旋钮的函数，因此"固定均值改形状"
在参数空间里本来就是二维路径。要求之一维化等于要求新增一个 `scv`/`cv2` 旋钮，
那属于**新增机制**，任务书明确禁止。

### Mode B —— 固定 burst，改变平均 offered load

**做法**：固定 `burst_start_s` / `burst_duration_s` / `burst_multiplier` 三个字段**完全不动**，
只扫 `demand.offered_mbps`。

- 只改 **1** 条参数路径 → 满足严格单因素设计 → 可声明单因素因果。
- 保持的是"突发形状"（窗长、幅度、位置），变化的是整体负载水平。

推荐 arm 骨架（`W=8, B=2, start=8, T=40`，即 `mean_mult=1.20`）：

| arm | offered_mbps | 预期平均负载 Mbps |
| --- | --- | --- |
| B1 | 25 | 30.0 |
| B2 | 50 | 60.0 |
| B3 | 100 | 120.0 |

> **Mode B 的声明边界**：三个 arm 的**平均**负载不同，但**瞬时峰值率同样成比例变化**
> （峰值 ≈ `offered_mbps×B`）。因此 Mode B 建立的是"负载水平效应"，
> **不是**"突发度效应"。任何跨 Mode B arm 的差异都不得归因于 burstiness。

---

## 4. 归因矩阵：哪个模式支持哪种声明

| 想要的声明 | 用哪个模式 | 允许？ |
| --- | --- | --- |
| 「在固定平均负载下，突发度变化导致 X」 | **Mode A** | ✅ 可运行；**只能**作为 exploratory 描述，**不得**声称单因素因果 |
| 「负载水平变化导致 X」 | **Mode B** | ✅ 严格单因素，可声明 |
| 「burst 导致 X」（只动 `burst_multiplier`） | 两者都不是 | ❌ **禁止** —— 实测已证明该旋钮同时改变平均负载（+18.9%） |
| 「突发度与负载的交互效应」 | A×B 因子设计 | ⚠️ 需显式声明为多因素；当前平台无此预注册模板 |

---

## 5. 汇报纪律（写进论文前必须遵守）

1. **报告实测负载，不报告配置值**。`offered_mbps` 在 burst 开启时**不等于**实际负载
   （实测 49.15 / 58.98 / 70.10 vs 配置 50）：必须从 trace manifest 的
   `offered_bits` / `offered_packets` 反算，或按 §2 的方式统计。
2. **同时报告突发度统计量**（Fano 或到达间隔 CV²）与**其定义与分箱宽度**。
   本文件使用 1 s 分箱 Fano；换分箱宽度会改变数值。
3. **Mode A 的结论必须写明"平均负载在 ±x% 内固定"**，并给出各 arm 的实测负载。
4. **不得**用 `t1_pressure_corridor.yaml:69-73` 的 "duty cycle" 措辞描述比特比 —— 该措辞
   与 goodput 利用率混淆（见 `PLATFORM-AUDIT-REPORT.md` §2 L6 / B5）。

---

## 6. 复现命令

```bash
cd <repo>   # MAIN_SHA 549acd8b7cb7a1bb573e7146653f55273999086d
python3 /Users/lge/Desktop/topic/leo-runs/probe_burst.py     # §2 全表
# 逻辑：对每组 (B, W) 解析配置 -> compile_trace -> load_trace
#       -> 1 s 分箱到达计数 -> Fano = pvariance/mean
#       实测 Mbps = sum(bits)/duration/1e6
```

单点最小复现（B=3, W=8, T=40, offered=50）：

```python
demand = {"mode": "burst", "offered_mbps": 50, "packet_bits": 1_000_000,
          "burst_start_s": 8.0, "burst_duration_s": 8.0,
          "burst_multiplier": 3.0}
# -> mean_mult = 1 + 8*(3-1)/40 = 1.40 ; 实测 70.100 Mbps ; Fano 27.160
```

---

## 7. 与既有测试的关系

- `CODE/leo_sim/tests/test_micro_mechanism.py` 中的 burst 排序反转场景使用固定 burst 配置；
  本文件不改变其判据，只补充"该配置在同一平均负载下还有哪些等价点"。
- `config.py:570-597` 对 burst 字段做 fail-loud 校验：`mode=burst` 必须有
  `burst_start_s` 与 `burst_duration_s`；窗口必须与地平线相交（"非观测处理必须 fail closed"）；
  `burst_multiplier > 0`。这些条件**不得**放宽。
- 本文件**不新增任何代码**，只定义实验设计；任何 `scv`/`cv2` 一维参数化属于新增机制，
  不在本次审计授权范围内。
