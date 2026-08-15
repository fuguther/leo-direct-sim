# 性能 profile 基线（acceptance 场景）

> 日期：2026-08-16。方法：本机（macOS, Python 3.14）`cProfile` 跑 `acceptance.run_acceptance` 五场景（direct/k1/bbm/mbb/ge），全 PASS。只产报告，未改代码。
> 规模：wall 13.353 s（含 receipt 写入），8815 万次函数调用。
> **NN 调用列为 N/A**：本机无 TensorFlow，DDQN 学习臂只能本地 fail-closed；学习热路径（观测构建/NN 前向/训练）的 profile 须 VM 补测——本节数字全部来自非学习臂。

## 热点排序（cumtime / tottime，占比按 wall 13.353s）

| # | 热点 | tottime | cumtime | 占比 | 归因 |
|---|---|---|---|---|---|
| 1 | 路由最短路（`routing._multi_source_dist:93` → `fwd_cost:177` → `model.isl_range_km:226` → `ecef`） | 0.38+0.22+0.32 | 6.48 s | **~49%** | 每次 `_decide`（6386 次）全图 Dijkstra，每边每次查询都重算两端 ECEF（`ecef` 被调 290 万次） |
| 2 | 接入/切换可见性扫描（`kernel._evaluate_handover:1278` → `_visible_sats:1215` → `model.elevation_deg:204`） | 0.63 | 3.47 s | **~26%** | 每 tick 每端点扫全部卫星的仰角（70.7 万次 elevation_deg） |
| 3 | 事件循环开销（simpy `step`/`_resume`/`schedule`） | ~0.38 | 13.0 s | ~2-3%（自身） | 44.4 万事件；框架自身开销很小，时间都在回调里 |
| 4 | 观测构建 | — | 未上榜 | <1% | 非学习臂不触发；学习臂待 VM 测 |
| 5 | NN 调用 | N/A | N/A | N/A | 本机无 TF（fail-closed 设计） |

几何三角函数合计（sin/cos/radians/degrees/asin/atan2，全部从 model.py 几何查询调入）tottime ≈ 2.88 s（~22%）——热点 1、2 的共同根因都是**同一 (sat, t) 的 ECEF/仰角被反复重算**：`subpoint` 单函数 tottime 2.92 s（21.8%）、`_sph_to_ecef` 1.84 s（13.8%）。

## 结论（先测量后优化的依据）

1. 优化预算应优先给**几何查询缓存**（按 (sat, 量化 t) 缓存 ecef/elevation，决策与切换在同一时刻重复查询同一几何）——理论可消去热点 1、2 中约 70% 的重复计算；任何缓存必须保持「只在当前时刻查询、不读未来」合同（model.py docstring）。
2. 其次是路由侧**每决策一次全量 Dijkstra**（`choose_next_hop` best_only 时仍全图算距）：可按 (t, 拓扑快照) 缓存距离矩阵。
3. simpy 事件循环本身不是瓶颈；观测构建/NN 在非学习臂可忽略。
4. GPU/并行暂不成立：瓶颈是 CPU 几何重算，不是 NN。

## 复现

```bash
python3 - <<'EOF'
import cProfile, pstats, tempfile
from CODE.leo_sim import acceptance
pr = cProfile.Profile(); pr.enable()
acceptance.run_acceptance(tempfile.mkdtemp())
pr.disable(); pstats.Stats(pr).sort_stats("cumulative").print_stats(25)
EOF
```
