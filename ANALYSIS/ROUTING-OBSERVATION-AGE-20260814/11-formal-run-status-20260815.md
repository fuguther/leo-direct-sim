# 正式实验运行状态（2026-08-15 凌晨）

## 已在跑

- **实验一**：GAT × obs_hops{1,2,3} × 档{50,100,200 Mbps} × 训练种子{41–45} ×
  流量种子{101,102}，共 90 cells；每 cell = train(120s) + eval(3 seeds × 60s)。
  - VM 后台 pid `4077806`（编排器 `run_formal_exp.py`，6 并行）。
  - 输出 `/tmp/leo-formal-exp1/matrix-summary.json`，日志 `/tmp/leo-formal-exp1.log`。
  - 监控：`ssh vm 'tail -20 /tmp/leo-formal-exp1.log'` 或读 matrix-summary.json。

## 关键事实

- 训练加速已落地：`LEO_FAST_TRAIN`（tf.function 编译训练步，等价性校验 max_dw=1.9e-9），
  单 120s GAT 训练 cell 墙钟约 5 min（旧 eager 约 30 min/60s）。
- 修复 eval 加载 checkpoint 缺 `custom_objects` 的 bug（GAT 反序列化）。
- E0 定档 50/100/200 Mbps（hop 完成率 1.0/0.99/0.94；GAT@130 实测 0.76）。
- pilot 合格：train_steps=11730（≥2000）、natural_end、守恒、checkpoint verified。

## 下一步（E1 完成后）

1. 收 E1，用 `analyze_formal_exp.py` 算 obs_hops 配对差 + bootstrap CI，定 h*。
2. 实验二（聚合）：`--contracts C3,MPNN,GAT`，固定 h*、中档 200(或按 E1 定档)。
3. hop 基线对照（同流量种子 101/102，非学习）——学习失败检查。
4. 实验三（年龄）：需先落地逐字段年龄数据层（未开始，标 UNVERIFIED）。

## 结果分级

- 正式结果 = 完整 train+eval、natural_end、守恒、checkpoint verified、多 seed。
- 进行中 = 已启动但未到自然结束或被中断的 cell。
- 调试 = /tmp 下的 pilot/smoke（不冒充正式）。
