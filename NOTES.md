# NOTES.md

## 当前状态

- 2026-08-16 任务 4（验收阶梯成文）完成：`ANALYSIS/ACCEPTANCE-LADDER-20260816.md`——三层判据（A 点对点解析等价 / B 机制各对合同 / C 系统差异可归因）+ 8 条不变量清单 + 机制逐个加挂差分玩法 + 变异测试第一批 10 条注入清单（标出 4 个待补捕获测试缺口：M-3/M-4/M-8/M-9）。
- 2026-08-16 任务 3（决策级差分快照）完成：kernel 加 output-only decision sink（每跳：候选集/所选动作/自身队列/观测摘要 dim+sha256_16+L2），comparison.py 直臂写 decisions.jsonl；旧臂只读不可改，开 SIM_LOG_LEVEL=1 解析其 packet_fate dump 归一化为逐跳 JSONL（候选/观测字段该 runtime 不记录，置 null 并注明）。行为不变由 test_decision_snapshot.py 双跑对照（fates/totals/deliveries/occupied 等 9 键全等）证明。
- 2026-08-16 任务 2（手工可算最小场景解析断言）完成：`CODE/leo_sim/tests/test_analytic_scenarios.py` 4 场景——单星直连精确时延（2·(0.08+PROP_GSL)，abs 1e-9）、两跳转发精确总时延、接入槽满等待计数（slots=1 被 8s 服务占死：requests=1/preposition_grants=1/waiting_at_stop=1/双包 IN_SYSTEM）、horizon 在途结算（occupied isl_s = horizon − t_start 精确到账）。推导全部写进 docstring。
- 2026-08-16 任务 1（reward/观测迁移对照）完成：确认三处漂移 bug（队列奖励 exp(-占用比)→M1 实测队列奖励 w1·exp(−β·t)、deliver 1.0→arrive_reward=50、own_state 聚合→M2 逐方向 4 维缺方向=1.0），已修复并合并 PR #11（CI pytest pass 14s；本地 319 passed/0 failed，基线 313）。逐分量对照表：`ANALYSIS/REWARD-DIFF-20260816.md`；golden 防漂移：`CODE/leo_sim/tests/test_reward_migration.py`。另发现：`CODE/experiment_platform/tests` 5 个失败为 main 既有（缺 EXPERIMENTS/ANALYSIS 文件，不在 CI 范围），待处置。
- 2026-08-16 VM 根分区清理完成：/tmp 下 39 个 leo-* 实验项（37G，含 8-15 正式学习实验 formal-exp1/exp2 的 receipt 与检查点）整体迁至 `/data/leo-tmp-results-salvage-20260816/`（mv 逐项校验，0 失败）；根分区从 100% 满恢复至 10% 占用。教训记入纪律：任何 `--out` 一律指向 /data 下路径；salvage 目录内容的去留待用户逐条批准。
- 2026-08-16 VM 部署链适配并首验通过：规范 VM 根改为 `/data/论文/leo-direct-sim`（PR #1，7 文件 9 处）、deployment_guard 顶层布局适配（PR #2）；已从 main `de5dc92` 部署到 VM 新独立目录（200 文件，本地/远端 tree SHA `800bfe77…` 一致，部署回执 `8e98cc0a…`）。VM 冒烟：config validate OK、dry-run OK、真实 smoke run 守恒（conservation_ok=true、IN_SYSTEM_AT_STOP=0）且 receipt verify 通过。**注意：VM 根分区 `/` 已 100% 满（40G/40G），/tmp 不可用**——本次唯一失败就是 /tmp 写盘触发 fail-closed（行为正确）；/data 仍有 431G。/tmp 清理待用户决定。
- 2026-08-16 仓库已公开（https://github.com/fuguther/leo-direct-sim）：公开前扫描无密钥/内网地址/第三方论文全文；MIT LICENSE 已加；GitHub Actions CI 已启用（公开库免费），首次 run success（23s，313 测试）。待办 4 中「公开」相关项已完成。
- 2026-08-16 新基地建立：从旧私有工作区 `fuguther/leo-research-workspace` 分拆，只含新平台（leo_sim V2）及其治理链与现行科研资产；不带 git 历史，旧库保留全部历史与旧平台（Gateway 汇聚）代码。白名单与取舍依据见 `ANALYSIS/PLATFORM-DOCUMENTATION/05-new-repo-plan.md`。
- 已带证据状态（继承自旧库 NOTES，细节可回旧库查证）：五类机制验收 PASS；Gateway/直连同 trace 对照双臂可运行；DDQN train/eval 全链（VM，TF 2.13.1 CPU）PASS 且 receipt verified；GAT/MPNN 图编码器已接入学习热路径并通过验收；人口重力流量已实现并通过 platform-check。以上均只证明工程链可运行，不证明算法优越。
- 待办（按优先级）：
  1. 新平台 bug 分诊（用户报告训练异常，疑似迁移期 reward/观测语义漂移；方法见 ANALYSIS/PLATFORM-DOCUMENTATION/ 差异对照与说明书）。
  2. 验收阶梯落地（不变量 + 新旧差分 + 对抗复核 + 变异测试 + 分级验收声明）。
  3. 性能 profile 后再定 GPU/并行优化点（先测量，不猜）。
  4. 公开仓库前：确认 LITERATURE 无第三方论文全文、补 LICENSE、恢复 GitHub Actions（公开库免费）。

- 2026-08-16 GitHub 工作流规则落地并硬执行：AGENTS.md 扩充为完整 Git/GitHub 规则（分支/提交/PR/合并/授权/收尾十诫 + 三端职责 + 多 Agent 写入仲裁，继承旧库《三端工作流与边界》与治理草案 v0.3）；main 远端 ruleset `main-protection` 已启用（必须 PR + pytest 必过 + 禁 force-push/删除），实测直推 main 被远端拒绝；仓库设置仅允许 squash merge、合并后自动删分支。PR #3 为此规则自身的首次全程验证。
