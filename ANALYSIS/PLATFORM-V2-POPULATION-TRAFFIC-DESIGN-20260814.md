# V2 人口重力流量设计合同

> **SUPPORTING DESIGN**：流量设计细节保留；当前实验是否启用该模式以 `EXPERIMENT-PROGRAM.md` 为准。

## 目标与边界

将仓库内 GPW 2020 人口栅格直接转换为卫星直连业务区域。人口只决定外生业务需求，不决定卫星关联、路由或链路状态，也不重新汇聚到 Gateway。

这是人口代理流量，不是真实互联网 OD 测量。输出必须标记 `population_proxy`，不得据此宣称真实用户流量已经校准。

## 数据与区域

- 输入：`CODE/population_map/gpw_v4_population_count_rev11_2020_15_min.tif`。
- 原始分辨率：0.25°，无数据值和负值按 0 处理。
- 按配置的 `endpoints.aggregation_deg` 聚合，首个版本使用 5°。
- 每个正人口聚合格成为候选 `TrafficEndpoint`，位置为聚合格中心，人口为格内人口之和。
- trace 没有出现的候选格不进入运行时，维持稀疏激活。

## 概率模型

总发包率仍由 `demand.offered_mbps / packet_bits` 决定，发包过程为固定 seed 的泊松过程。

源区域发包率：

`lambda_i = lambda_total * population_i^beta / sum(population_k^beta)`

目的区域条件概率：

`P(j|i) ∝ population_j^gamma / max(distance_ij, distance_floor_km)^alpha, j != i`

默认 `beta=1`、`gamma=1`、`alpha=1.25`、距离下限 100 km。每个包按该分布随机抽样目的地，不固定选择最大概率目的地。

## 可复现与失败边界

- TIFF 原始字节 SHA、人口相关配置和 seed 全部绑定 trace identity。
- 同配置、同 TIFF、同 seed 必须生成字节相同的 trace。
- 文件缺失、TIFF 非二维、地理范围/分辨率异常、总人口非正、聚合后不足两个区域均 fail closed。
- manifest 记录人口文件 SHA、有效人口、候选区域数、模型参数和 `not_calibrated_user_demand=true`。
- Gateway 与卫星直连对照只能消费编译后的同一 immutable trace。

## 验收

1. 仓库 GPW 数据可聚合，人口总量与原始有效像元和一致。
2. 生成 trace 的源频率随人口增加，目的地不是恒定且符合人口/距离权重抽样。
3. 相同 seed 字节一致，修改 TIFF 字节或人口参数会改变 trace identity。
4. 人口 trace 可进入真实卫星直连接入、守恒并通过 receipt。
5. 一键 `platform check` 增加人口流量阶段并在完整 VM 环境通过。
