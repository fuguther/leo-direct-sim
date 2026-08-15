# 分析区

分析必须从已验证 run ID 和 hash 开始，不从目录名、截图或手工汇总开始。每项正式分析只有三个核心产物：

- `manifest.json`：输入、脚本、命令、cohort、纳入/排除规则、指标定义和 hash；
- `summary.csv`：arm/scenario/seed/n/metric/estimate/uncertainty 的整洁表；
- `report.md`：问题、方法、结果、局限、替代解释、能支持与不能支持的 claim、科研价值。

分析不能直接写入 `ARCHIVE-20260803/GUIDANCE/`；只能提出 claim candidate。

## 配对分析执行

`paired_analysis.py` 只接受 `run_id=结果目录` 的显式映射，并重新验证完整 v2 预注册、request/manifest 绑定、实际 config、controlled signature、seed、scenario、run identity、effective receipt、artifact manifest、每个产物 hash 与主指标。所有计划 run 必须到齐；缺失配对会 BLOCK，不会被填零或悄悄排除。

```bash
python3 ANALYSIS/paired_analysis.py \
  --analysis EXPERIMENTS/EXP-.../analysis-request.json \
  --manifest EXPERIMENTS/EXP-.../run-manifest.json \
  --run EXP-...-control-s41=/path/to/run \
  --run EXP-...-treatment-s41=/path/to/run \
  --out ANALYSIS/EXP-...
```

只有 `analysis-manifest.json.status=VERIFIED` 且当前论文入口重新执行后仍得到同一 cohort、contrast、统计量和输出时，才可作为 claim 的实验依据。每次分析还会保存 `analysis-code.py` 快照，保留当时的可复现代码；任意手写 `VERIFIED` 字符串没有效力。
