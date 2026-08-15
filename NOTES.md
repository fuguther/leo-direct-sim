# NOTES.md

## 当前状态

- 2026-08-16 新基地建立：从旧私有工作区 `fuguther/leo-research-workspace` 分拆，只含新平台（leo_sim V2）及其治理链与现行科研资产；不带 git 历史，旧库保留全部历史与旧平台（Gateway 汇聚）代码。白名单与取舍依据见 `ANALYSIS/PLATFORM-DOCUMENTATION/05-new-repo-plan.md`。
- 已带证据状态（继承自旧库 NOTES，细节可回旧库查证）：五类机制验收 PASS；Gateway/直连同 trace 对照双臂可运行；DDQN train/eval 全链（VM，TF 2.13.1 CPU）PASS 且 receipt verified；GAT/MPNN 图编码器已接入学习热路径并通过验收；人口重力流量已实现并通过 platform-check。以上均只证明工程链可运行，不证明算法优越。
- 待办（按优先级）：
  1. 新平台 bug 分诊（用户报告训练异常，疑似迁移期 reward/观测语义漂移；方法见 ANALYSIS/PLATFORM-DOCUMENTATION/ 差异对照与说明书）。
  2. 验收阶梯落地（不变量 + 新旧差分 + 对抗复核 + 变异测试 + 分级验收声明）。
  3. 性能 profile 后再定 GPU/并行优化点（先测量，不猜）。
  4. 公开仓库前：确认 LITERATURE 无第三方论文全文、补 LICENSE、恢复 GitHub Actions（公开库免费）。
