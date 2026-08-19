# NOTES.md

## 2026-08-19（有限 holding queue：容量/面积/WAIT 语义）

- 分支：`codex/20260819-holding-queue`。
- 实现 `SatelliteHoldingQueue`，替代 kernel 内部无界 `pending` list 的运行时语义：
  每星 bits 容量、FIFO、`queued_bits`、`QueueArea` 面积、快照占用与 `holding_until`。
- 所有 pending 回退/重决策/Q0 WAIT 写入统一经 `_hold_packet`；容量不足记录独立
  `HOLDING_QUEUE_OVERFLOW` fate，进入数据守恒与 receipt；不再静默无界增长。
- pending ticker 增加 holding deadline sweep；WAIT 只在 `until` 到达后释放，快照可观察等待截止时间。
- 配置新增 `access.holding_queue_bits`，receipt `queue_area_bits_s` 新增 `holding`，机制计数新增
  `holding_queue_overflows`。
- 验证：`pytest -q CODE/leo_sim/tests` = **409 passed**；新增 holding queue/Q0 回归覆盖容量、FIFO、
  面积、overflow fate、快照、WAIT 和 deadline。
- 边界：尚未实现 Q0-I/Q0-F tiny 求解器、planned-vs-executed 回放门禁；D1/D2 仍需独立冷启动复核，
  本分支不得作为论文正式基线。
- 冷启动复核：初审发现 Q0 WAIT 未校验目标卫星，可能把包等待在错误节点；已在 `2d9581e` 修复并
  增加原子性回归。随后静态盘点确认生产路径均经 `_hold_packet`，Q0 位置索引、面积结算和 deadline
  sweep 无遗漏；复核后平台测试为 **411 passed**。

## 2026-08-19（D1/D2 靠拢、旧平台账本与实验路线图）

- 用户已决定 D1 动态链路速率、D2 动态拓扑重匹配按旧平台行为继续推进。
- D1 独立分支 `codex/20260819-d1-dynamic-rate`：原实现 `c0a1f18` 经复核为
  REQUEST_CHANGES；本轮修复零速率快照除零、MCS/控制发送计数时机、ISL 合法掩码、
  GSL 零速率等待唤醒与 FIFO 越过，提交 `5e2d779`，`CODE/leo_sim/tests` 为
  406 passed。仍需不同模型冷启动复核，暂不合入。
- D2 独立分支 `codex/20260819-d2-dynamic-topology`：实现已提交 `7cb11e8`，
  `CODE/leo_sim/tests` 为 400 passed；尚无独立冷启动复核，暂不合入。
- 主分支文档提交 `101088b`：新增 `ANALYSIS/LEGACY-FEATURE-LEDGER-20260819.md`
  和 `ANALYSIS/EXPERIMENT-READINESS-ROADMAP-20260819.md`，并把 Q0 信息裁剪组合矩阵
  补入 `ANALYSIS/Q0-ALGO-RESEARCH-20260818.md`。
- 当前结论：已有基线/机制验收链可以继续做低风险平台验证；D1/D2 未复核版本不能作为
  正式论文实验基线。Q0 调研不再无限扩张，矩阵定稿后进入合同冻结与 tiny 原型。

## 2026-08-19（Q0 合同层与只读计划校验）

- 新增 `CODE/leo_sim/q0.py`：不可变 `PlanAction`/`JointPlan` 合同，版本绑定和未知/重复动作
  fail-closed；Kernel 新增只读 `validate_joint_plan`，校验当前版本、live packet 位置、
  拓扑邻接、服务中/在途不可操作和 ISL 容量预留。
- 回归：`CODE/leo_sim/tests/test_q0_contract.py` 4 passed；平台测试全量 402 passed。
- 明确未完成：`apply_joint_plan`、有限 holding queue、Q0-I/Q0-F tiny 求解器和
  planned-vs-executed 回放门禁仍未实现；本次只完成 Q0 实现顺序第 1 步的一部分。

## 2026-08-19（Q0 计划原子应用）

- `Kernel.apply_joint_plan()` 已接入：第一版只接受 pending 数据包，整份计划先复核版本、
  live 位置、拓扑/容量/GSL 条件，再一次性迁移；非法混合计划不会部分修改。
- 记录 `q0_plan_audit`，成功应用后递增 `state_version`；同一计划内 ISL/downlink 容量按总量校验。
- Q0 合同测试 6 passed；平台全量测试 404 passed。
- 明确边界：尚未把所有 pending 路径统一成有限 holding queue，尚未实现 Q0 tiny 求解器和
  planned-vs-executed 回放门禁；本提交不是正式 Q0 上界结果。

## 2026-08-19（R6-G2b 收口：台账置 fixed）

- #51（governance symlink 词法根边界）复核两轮收敛（第 1 轮 REQUEST_CHANGES → 修复
  → 第 2 轮 APPROVE），全量 402 pytest；本次把台账 R6-G2b 由 open(follow-up) 收口为 fixed。
- 口径：#48 记的 follow-up「只扫描 project_root 内用户可控后缀分量」由 #51 实现（lexical
  project_root 边界 + containment 用解析根）；「或只收相对路径」为备选方案未采纳，正式流程
  仍可用绝对路径（不被系统级 symlink 误拒）。

## 2026-08-19（旧平台设计深审：新平台「忘记/想不到/做得不如」）

- 产出：`ANALYSIS/LEGACY-DESIGN-AUDIT-20260819.md`（只读审计，未改平台代码）。
- 方法：先读比对/迁移文档（02-kimi-platform-spec、MIGRATION-BACKLOG、REWARD-DIFF、LINK-BUDGET、
  TEMPORAL-MULTISTEP），再逐行读旧库 SimulationRL.py（12556 行）+ routing_*/temporal_encoder/link_outage，
  对照本库 leo_sim kernel/learning/routing/model/config。
- 结论速览（FACT 已核实）：D1 动态链路速率（B5，未实现）、D3 多步/TD-λ/temporal（M2，只设计稿）、
  D4 path-credit（M3，未迁）均为既有清单项；**新发现**：D2 动态 ISL 拓扑重匹配、D5 每星模型+FL+CKA、
  D7 M3 队列动态特征、D10 步进 vs 时间 ε 调度 / stopLoss；D8 per-block 时延三分量为未验证项。
- 待办：D1 落地、D5 出设计稿、D9 回放持久化升级、D2/D6/D7/D8/D10 记 follow-up（详见报告 §8/§9）。
- 未动平台；文档在分支 codex/20260819-legacy-design-audit（worktree /tmp/audit-wt-20260819）。

## 2026-08-19 凌晨（P0-2 hop BFS 完成 + 第 5/6 轮审计收口）

- P0-2（hop 策略多源 BFS 替代 Dijkstra）合并 #49：等价验收=acceptance 5 场景
  ledgers 逐字节一致 + 显式多跳 hop 双端一致（921e51d4…，delivered 均 301）；
  deepseek 独立复核 APPROVE（50k 随机图差分等价）；全量 400 pytest。
- R6-P02b（sorted_adj 未预传时仍构建）记 minor follow-up。

## 2026-08-19 凌晨（第 1 阶段启动：R5-G2 修复 + 第 5/6 轮本地审计）

- R5-G2（governance 不绑定 checkpoint 文件）已修复并合并 #47：seal 时校验
  checkpoint 存在/非 symlink/项目根内/SHA 一致 + metadata pin；glm 子代理
  第 1 轮 BLOCK（resolve 前 is_symlink 死代码 + metadata 路径错位）→ 修复
  （resolve 前逐级 symlink 扫描 + 未解析父目录语义 + 对抗测试）→ 第 2 轮
  PASS（1 minor：macOS 绝对路径 /var symlink 假阳性，记 R6-G2b）。
- 第 5/6 轮本地审计：routing/control/outage/model/rng/fates/grid/acceptance/
  comparison/population/trace/experiment_platform 全过，未新增隐藏 bug；
  台账 R5-G1/G2 fixed、G3 dismissed、R6-G2b open(follow-up)。
- #48 台账状态更新 PR（R5-G2 fixed + R6-G2b）。

## 2026-08-18 夜 → 08-19 晨（第 0 阶段工作流优化 + 第 4/5 轮收口）

- 工作流优化（0.1–0.5）全部落地：
  - 0.1 问题台账 `ANALYSIS/FINDINGS-REGISTRY.md`（#45，含 R4A2/R4A3/R4B2/R4C/R5/R6）。
  - 0.2 审阅轮次上限 3 + 增量审阅 + minor 收敛规则（台账 + 僚机 prompt playbook）。
  - 0.3 独立审阅改不同模型子代理/Codex 冷启动自审：deepseek 终审 #40 APPROVE（3 minor follow-up）；
    glm 子代理未交付终稿 → #42 以 R4A4 网页终审 + Codex 自审收敛。
  - 0.4 僚机调度恢复（ProjectPilot feature/web-agent-offload-backend 9ed0f3e）：死租约 DISPATCHING
    自动回收为 FAILED + retry 放行；桌面测试 550/550；实测 R4B3/R4A4 重试成功。
  - 0.5 VM/TF 验证前置清单 `ANALYSIS/VM-TF-VERIFICATION-20260818.md`（#45）。
- 合并：#40 Q0 快照（A1/A2/A3）、#41 _transmit 退休、#42 checkpoint 契约（R4A2→R4A4 全闭合，
  384 pytest）、#44 trace deadline=0、#45 工作流 docs。main=4ff7987。
- Q0 算法选型双路终稿 `ANALYSIS/Q0-ALGO-RESEARCH-20260818.md`：Q0-I=SMDP/DP（tiny）、
  Q0-F=事件时间 MILP/CP-SAT、min-cost flow 仅松弛、M1 奖励不可作最优性判据。
- 第 5 轮 Codex 本地挖：R5-G1（csv deadline=0，已修 #44）、R5-G2（governance 不绑定
  checkpoint 文件，open follow-up）、R5-G3（comparison 资源不等价=已声明范围，dismissed）。
- 待拍板：PR #43（奖励保留 vs 失败=0）、#25/#26/#28（P1 行为修正）、Q0 合同 §5 五问、
  R5-G2 与 R6-A1/A2/A3/B2 follow-up、VM/TF 清单实跑。

## 当前状态
- 2026-08-17 自主合并留痕（AGENTS.md 授权，全部 CI pytest 绿）：PR #29
  （occupied 停表口径 + expiry 超 horizon 走 stalled）、#34（GE bool 拒绝 +
  意图 sites 要求）、#30（TabularQ eval RNG）、#31（几何记忆化缓存）、
  #32（账本 bit 绑定）、#33（burst 窗口）、#35（acceptance 死门）、#36
  （receipt verify 崩溃）、#37（forward 掩码断言 + peek fail-loud）、#38
  （正式门改 recomputed）、#27（文档 §G/H + Q0 调研/接口设计 + 晨报）。
  第 1 轮 P1 项 #25/#26/#28 按目标规则留待用户确认后合并。
- 2026-08-17 夜第 1 轮三方挖问题闭环：GPT 两路 12+12 条发现、Kimi 49 条观察、Codex 本地复现验证。确认 5 条真 bug 并修复（均待复核/待拍板合并）：PR #25 downlink 恢复唤醒（Kimi APPROVE + 整队排空改进）、#26 接入 FIFO（Kimi REQUEST_CHANGES→已修 pop 缺陷+白盒测试）、#28 未来端点惰性激活（Kimi REQUEST_CHANGES→已移激活点+反例测试）、#29 occupied 停表口径（GE 恢复超 horizon 走 stalled）、#30 TabularQ eval RNG。P0-1 几何缓存完成（357 绿+等价验收，分支 codex/20260816-geom-cache 待 Kimi 复核）。Q0 算法选型三方调研完成（GPT 两路 + Kimi 交叉修正 §6），文档 ANALYSIS/Q0-ALGO-RESEARCH-20260817.md。汇总文档 ANALYSIS/EXPERT-REVIEW-20260816.md §G（PR #27）。第 2 轮 GPT 挖问题已派发（op 636052b2…，聚焦盲区模块+修复回归）。
- 2026-08-17 P0-1 几何记忆化缓存：实现 `model.MemoizedGeometry`（精确 t 分槽 LRU，位级等价；组合查询由缓存 ecef 重算；非 Constellation 委托+缓存），kernel 接入。验收：smoke/geometry_loss 两组改前改后 ledgers 逐字节一致；全量 357 passed（+3 测试）；性能：acceptance 3.42→2.97s、dense-oracle 1.07→0.80s、140 星 hop 6.36→5.91s。分支 codex/20260816-geom-cache（commit a34d2d3）已推送，待 Kimi 复核后开 PR。
- 2026-08-17 夜第 1 轮三方挖问题：GPT 两路（H1 primary/review）完整回收（各 12 条发现，网页抓取留痕 /tmp/gpt_h1_*.txt）；Kimi 独立挖出 49 条观察（输出截断，核心候选已纳入清单）；Codex 本地复现验证确认两条新 bug 并修复（PR #25 downlink 恢复唤醒、PR #26 接入 FIFO 插队，均 355 passed + acceptance PASS，待 Kimi 冷启动复核）。第 1 轮汇总已并入 `ANALYSIS/EXPERT-REVIEW-20260816.md` §G（新发现 G1-1..8、Q0 就绪度 G2、Q0 实验设计 G3、已知清单重分类 G4）。Q0 算法选型调研已派发 GPT（op 8fde67c8…，webResearch）。
- 2026-08-17 P0-1 几何记忆化缓存：实现 `model.MemoizedGeometry`（精确 t 分槽 LRU，位级等价；组合查询由缓存 ecef 重算；非 Constellation 委托+缓存），kernel 接入。验收：smoke/geometry_loss 两组改前改后 ledgers 逐字节一致；全量 357 passed（+3 测试）；性能：acceptance 3.42→2.97s、dense-oracle 1.07→0.80s、140 星 hop 6.36→5.91s。分支 codex/20260816-geom-cache（commit a34d2d3）已推送，待 Kimi 复核后开 PR。
- 2026-08-16 夜：夜间自主工作启动。起点 main c8c84f56（#24 已合并），工作区干净，全量 354 passed。队列：P0-1 几何记忆化缓存 → P0-2 hop BFS → P1-3 未来端点泄漏 → P1-4 MBB 积压 → P2 设计稿/分析。
- 2026-08-16 等价优化第一批（PR 待合并）：①oracle_targets 仅 oracle 策略时计算（学习/非 oracle 路径不再每次白扫服务星）；②决策快照 policy 标签改用真实 algorithm（qlearning 不再误标 ddqn）；③路由反向邻接/排序邻接表初始化时预计算（不再每次决策重建）。验收：改前/改后同配置 smoke 的 ledgers_sha256 逐字节一致（fee84a04…），全量 350 passed。下一步：几何记忆化缓存（P0-1）、hop 用 BFS（B-2）、VM 学习臂 profile。
- 2026-08-16 学习动作空间去预裁剪（用户拍板问题7选A，PR 待合并）：kernel 学习路径 best_only 恒 False，DDQN 动作空间=全部本地合法方向（不再被启发式最优预裁剪）；新增回归测试（E 最优/W 合法更远场景断言掩码同时含 E、W），修复前失败/修复后通过；Kimi 独立复核通过（无 blocking/major）。顺带修正 test_routing 因本次改动而过时的命名/注释（best_only 现为 routing 库参数，kernel 学习路径不再使用）。本地 350 passed。
- 2026-08-16 六项训练信号修复（Kimi 实现 + Codex 独立验收，PR 待合并）：①到达奖励改实际送达时结算（修下行硬退休白拿50）；②horizon 在途学习转移显式丢弃并计入回执（decisions==transitions+discarded 恒等式校验）；③fast_train 入 resolved config、op-determinism 失败记录、DDQN 回执 pin tensorflow 版本；④GAT/MPNN 根位置改由几何直传；⑤图节点特征补接入负载/可见小区/AoI（15→18维）；⑥修 C6 假绿测试。本地 349 passed（基线 342+7 回归，stash 对照修复前失败/修复后通过）。待办：VM 补 DDQN 真实冒烟、spec 文档重生成、config SHA 漂移是否 bump 版本待定。

- 2026-08-16 隔夜任务队列（1–8）全部收束，晨报：`ANALYSIS/OVERNIGHT-REPORT-20260816.md`。合并 PR #11–#18（全部 CI 绿自动合并）。核心结果：任务 1 确认并修复三处 reward/观测迁移漂移 bug（详见 REWARD-DIFF-20260816）；新增 TabularQLearning 基线、决策级差分快照、解析最小场景、链路预算表征、验收阶梯、temporal/multistep 与链路预算两份设计稿、性能基线。待用户决定 5 项（experiment_platform 5 个 main 既有失败处置、MCS 表选择、速率是否进观测、任务 6 实现启动时机、VM 遗留）。本地全量 342 passed / 0 failed。
- 2026-08-16 任务 8（性能 profile 基线）完成：`ANALYSIS/PERF-PROFILE-20260816.md`——cProfile 跑 acceptance 五场景（PASS，wall 13.35s）：路由最短路几何重算 ~49%、接入/切换可见性扫描 ~26%、事件循环自身 ~2-3%、观测构建 <1%（非学习臂）、NN 本机无 TF 记 N/A 待 VM 补测。结论：优先几何查询缓存，GPU/并行不成立。
- 2026-08-16 任务 7（链路预算）完成：`test_link_budget_characterization.py` 钉死旧 get_data_rate(:8295)/los_slant_range(:8282) 数值行为（RF 派生量 + 4 距离点 MCS 速率 golden + 单调/零速率性质）；关键发现：旧 shannonRate 不进返回值（MCS 量化才是输出）、旧参数下 6000km 速率=0（新平台默认 1Gbps 长距不可由旧预算复现）。`ANALYSIS/LINK-BUDGET-DESIGN-20260816.md` 集成设计稿（接入点=服务开始采样、配置面、零速率语义、receipt/守恒影响、验证计划），集成代码留后续。
- 2026-08-16 任务 6（M2 temporal/multistep）交设计稿：`ANALYSIS/TEMPORAL-MULTISTEP-DESIGN-20260816.md`——旧侧清点（routing_multistep 三函数无运行时调用，以 SimulationRL.py:6980-7062 内联版为准；temporal_encoder 三模式）、新平台接入点（remember 需 packet_key 合同扩展、MultistepLearner 包装器方案、framestack 观测管线）、配置面草案、五条验证计划。评估后按任务授权的降级路径只交设计稿：实现涉 learning 合同承重改动且 DDQN 臂本地无 TF 不可验收，拆 PR-1（纯回报换算+golden）/PR-2（接线+差分）留后续。
- 2026-08-16 任务 5（迁移 M1 Q-Learning 表）完成：`learning.TabularQLearning`（纯 numpy，无需 TF）。表征 golden：更新规则 (1−α)Q+α(r+γ·maxQ)（旧 5791-5794）、终结直写（5743）、均匀初始化（5703-5704）、合法集 argmax/探索（5758-5769）；合同适配全部 docstring 声明。config/receipt/__main__ 全链接入（algorithm="qlearning"，checkpoint=q_table.json+sha 校验，eval 不更新表）。E2E：真控制面+hop 路由+qlearning 跑通且 receipt verify 通过。
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
