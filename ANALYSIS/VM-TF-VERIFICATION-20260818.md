# VM/TF 验证前置清单（正式实验门，2026-08-18）

> 工作流优化 0.5：DDQN 动态负例与学习臂 profile 不再作为永远挂账的 open item，
> 而是正式实验门（编译 → 审阅 → 授权 → 部署 → 跑实验）的固定一步。

## 1. 门定义

当实验配置 `learning.algorithm == "ddqn"`（train 或 eval）时，部署与正式运行前
必须完成以下 VM 步骤并把回执写入实验目录；未完成的授权请求应视为不完整。

## 2. VM 前置步骤（在部署好代码的 VM 上执行）

```bash
# 0) 环境确认（TF 版本是回执的一部分）
python3 - <<'PY'
import tensorflow as tf, sys
print("python", sys.version.split()[0])
print("tf", tf.__version__)
PY

# 1) DDQN 动态负例（#42 checkpoint 契约：metadata pin/非法 UTF-8/contract mismatch）
python3 -m pytest CODE/leo_sim/tests/test_qlearning_migration.py \
  CODE/leo_sim/tests/test_config.py -q -k "metadata or contract or utf8 or schema or key"

# 2) 学习臂全量回归（含 #43 奖励语义，若已合并）
python3 -m pytest CODE/leo_sim/tests CODE/tests -q

# 3) 学习臂 profile（P2 设计稿配套）
python3 -m cProfile -o /data/leo-prof/learn_profile.prof \
  -m CODE.leo_sim --config <experiment-resolved.yaml> --learning-out /data/leo-prof/learn-out
python3 - <<'PY'
import pstats
pstats.Stats("/data/leo-prof/learn_profile.prof").sort_stats("cumulative").print_stats(30)
PY
```

## 3. 回执步骤（写回实验目录）

在实验目录生成 `vm-tf-receipt.json` 并纳入授权材料：

```json
{
  "schema": "leo-sim-vm-tf-verification/v1",
  "code_commit": "<部署回执 SHA>",
  "tensorflow_version": "2.x.x",
  "python_version": "3.x",
  "negative_tests": {"command": "...", "exit_code": 0, "passed": N, "failed": 0},
  "full_suite": {"exit_code": 0, "passed": N, "failed": 0},
  "profile": {"artifacts": ["/data/leo-prof/learn_profile.prof"], "top_cumulative": "..."},
  "run_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

授权门在 `authorize_experiment.py` 侧的可选增强（后续 PR）：
校验 `vm-tf-receipt.json` 存在且 `negative_tests.failed == 0`、`full_suite.failed == 0`。

## 4. 相关台账

- R4A2-F1 / R4A3-F1 / R4A3-N1（DDQN metadata pin）：负例命令见第 2 节第 1 步。
- R4C-F4（DDQN load_model 异常统一包装）：在 TF 主机上由第 2 节第 1 步覆盖。
- P2 设计稿（VM 学习臂 profile）：第 2 节第 3 步。
