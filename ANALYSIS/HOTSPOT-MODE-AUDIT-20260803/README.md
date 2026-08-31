# 热点流量模式专项审计（2026-08-03）

> **EVIDENCE-SNAPSHOT / HISTORICAL**：本文记录 2026-08-03 旧平台代码树与旧 VM 路径下的机制证据，不是 leo-direct-sim 当前运行入口、当前代码行为或当前实验方案。现行任务从 `AGENT-START-HERE.md` 进入；引用下列结论前必须在当前平台重新核验。

审计范围：uniform / h2 / gravity / gravity_corridors / mlab 五种 OD 模式在当前代码树（VM `/data/论文/LEO-Research-Workspace/CODE/`，新旧两树 `traffic_od.py` 逐字相同，diff exit 0）下的真实行为。
动机：用户要求保留四模式，但需确认"保留的东西能否适配新流量框架"。结论：**四模式机制可保留，但 h2 与 gravity_corridors 的所有现存触发路径都静默退化，必须修复后才可用。**

## 一、审计结论速览

| 模式 | 机制本身 | 现存触发路径 | 判定 |
|---|---|---|---|
| uniform | 正常 | 正常 | 可用 |
| h2 | 正常（dests 在 GT 集合内即生效，已数值验证） | **全部退化**：inline 路径必退化；配置文件路径在当前 4-GT 场景退化 | 需修复 |
| gravity | 正常 | 正常（当前 148 个正式 run 在用） | 可用 |
| gravity_corridors | 正常 | **全部退化**：inline 丢 corridors；repo 配置引用的城市不在 4-GT 集合 | 需修复 |
| mlab | 正常，缺 csv 时 fail-loud（ValueError） | 正常 | 可用，设计范本 |

## 二、证据（FACT，全部实机复核）

### E1 inline h2 必退化为 uniform
- `run.py:1423-1426` `_build_traffic_json`：inline h2 只返回 `{"mode","p","g"}`，**丢弃 sources/dests**。
- `traffic_od.py:355-358` dispatch：`sources = cfg.get("sources") or cfg.get("sources_hot") or []` → 空。
- `traffic_od.py:41-46` `_indices_for_subset`：空名单返回空索引，**静默不报错**。
- `traffic_od.py:95-156` `build_od_weights_h2`：S_idx/D_idx 为空 → 无任何条目被 boost → w_boost == uniform → `w_out = (1-p)*uniform + p*uniform` **精确等于 uniform**。
- default.yaml 默认 `traffic.mode: h2`（p:0.4, g:3.0）→ 不显式配置流量的实验走的就是这条必退化路径。

### E2 配置文件 h2 在当前 4-GT 场景退化
- `traffic_hotspot_h2.json`（p0.5,g2.0）与 `_heavy.json`（p0.7,g3.0）：sources=[Malaga, Los Angeles]，dests=[Mauritius]。
- GT 选择：RL 路径取 `inputRL.csv` 前 N 行（`SimulationRL.py` `locations[:GTnumber]`）。文件 31 行 GT，顺序为 Malaga(1)、LA(2)、Tokyo(3)、Hartebeesthoek(4)、**Mauritius(5)**、Vardø(6)。
- GTs=[4] → Mauritius 不在集合 → D_idx 空 → 退化同 E1。
- 数值验证（leo-i39 python，`build_od_weights_h2`）：repo 配置输出 == uniform 为 **True**；dests 改为 [Tokyo]（集合内）后为 **False**（真热点）。

### E3 8 个幸存旧 h2 run 的直接运行时证据
- `ANALYSIS/DELETED-RUN-SUMMARIES-20260803/explore_0716_legacy/` 8 个 run 的 logfile 全部打印 `Traffic OD: h2 (config=.../CODE/traffic_hotspot_h2.json)`。
- 同日志 GT 列表 = Malaga / LA / Tokyo / Hartebeesthoek（无 Mauritius）。
- 结论：这 8 个标注为 "m_h2 hotspot" 的实验实际是 uniform 流量。

### E4 gravity_corridors 双路径退化
- inline：`_build_traffic_json` 只保留 `{"mode","p_corridor"}`，**丢弃 corridors 数组** → `traffic_od.py:284` "no corridors; pure gravity"。
- repo 配置 `traffic_gravity_corridors.json`：corridors 引用 Mauritius / Vardø → 4-GT 集合下 `_corridor_boost_matrix`（`traffic_od.py:217-234`）无任何条目命中 → 数值验证：输出 == 纯 gravity 为 **True**。
- gravity 基底不依赖具名城市（用坐标+质量），本身正常——所以 corridors 退化的结果是"纯 gravity"，比 h2 的"纯 uniform"隐蔽性稍低，但 corridor 结构同样静默消失。

### E5 第三条静默退化路径（异常兜底）
- `SimulationRL.py:3844`：OD 初始化抛任何异常 → 打印一行后回退 uniform（除非 `_SIM_FAIL_CLOSED`）。运行时不会失败，只会悄悄变成 uniform。

### E6 旧时代实验受影响范围（INFERENCE，高置信）
- 存档 plans 中 510 处 `[4]_GTs`，仅 2 处 `gateways: 12`。
- 用 h2_heavy 的 77 个 plan、h2 的 51 个 plan、inline h2 的 23 个 plan：inline 必退化；配置文件路径在 4-GT 下必退化。
- 推论：**旧时代几乎全部"hotspot h2"实验实际跑的是 uniform 流量**（仅 2 个 12-GT plan 若走配置文件路径则可能真热点）。
- 影响：旧结论中凡涉及"hotspot 与 uniform 对比"的，证据基础很可能实为 uniform-vs-uniform。旧结果本就全部 UNVERIFIED_LEGACY，此发现是其下一条具体机制级注脚，不改变"旧结论不可引用"的总判决。

## 三、保留清单与冗余变体盘点

机制代码（保留，全部在 `CODE/traffic_od.py` / `traffic_mlab.py` / `traffic_burst.py`）：
- 五模式 builder + dispatch + `load_traffic_config_from_env` 优先级链。

配置文件（5 个 h2 变体 + 2 个 gravity 系）：

| 文件 | 内容 | 判定 |
|---|---|---|
| `traffic_gravity.json`（a2.0_df100_bu0.05） | 当前正式实验基准的参考样例 | 保留 |
| `traffic_gravity_corridors.json` | corridor 引用缺席城市 | 保留文件但**需改写**为集合内城市 |
| `traffic_hotspot_h2.json` | dests=[Mauritius]，4-GT 下退化 | 保留一个 canonical h2 样例但**需改写** |
| `traffic_hotspot_h2_heavy.json` | 仅 p/g 与上不同，同样退化 | 冗余，可归置 |
| `traffic_hotspot_h2.example.json` | 文档用样例，dests=[Mauritius,Vardø] | 冗余，可归置 |
| default.yaml inline h2 (p0.4, g3.0) | 第 6 个变体，inline 必退化 | 随修复一并处理 |
|  rescued `gnn_baseline_hotspot.json`（hot_dest_weight 4） | 第 7 个变体，旧 GNN baseline 用 | 已在封存区，不动 |

冗余本质：7 个"热点配置"只是同一退化模式的 p/g 参数排列，没有一个在当前 4-GT 场景产生真热点。

## 四、修复方案（第二轮 CODE 重构时执行，本轮只审计不改）

最小修复（两处，均 fail-loud 化）：
1. `run.py:_build_traffic_json`：h2 保留 sources/dests；gravity_corridors 保留 corridors 数组。
2. `traffic_od.py`：h2/corridors 在 sources/dests 解析后为空集且原名单非空时 raise（城市名拼错/不在集合 = 配置错误，不应静默继续）；原名单即为空时同样 raise（h2 无热点目标无意义）。

配套：
3. canonical h2 配置改为集合内城市（如 dests=[Tokyo] 或按论文场景重新设计），文件名与参数单一来源。
4. default.yaml 的默认 `mode: h2` 改为 `uniform`（无配置时取最诚实默认），或强制要求显式 config_path。
5. 修复后加单测：h2/corridors 空解析必须 raise；inline payload 必须含 sources/dests/corridors。

## 五、复核方法与可复验命令

- 数值验证脚本：`/tmp/hotspot_check.py`（执行当日会话生成，经 `ssh vm python -` 在 leo-i39 环境运行；核心断言即本文 E1/E2/E4）。
- 旧 run 证据：`ssh vm "grep -A8 'Traffic generated per GT' .../explore_0716_legacy/*/logfile.log"`。
- 两树一致性：`diff` 新旧树 `traffic_od.py` exit 0；5 个配置 json 逐字相同。

## 六、未验证项（如实列出）

- 2 个 `gateways: 12` 旧 plan 的实际流量行为（未找到幸存日志，无法确认是否真热点）。
- mlab 的 hourly 路径未做数值验证（仅代码走读，其 fail-loud 设计可信）。
- `traffic_burst.py` 突发叠加层未审计（与四模式正交，建议第二轮一并看）。
