# leo_sim V2 当前实验就绪状态

> 状态最后核验：2026-08-20；GitHub/main、开放 PR、当前 worktree 与 VM deployment receipt 已现场读取。
> 判定词：`FACT` 为当前可核验证据；`INFERENCE` 为基于证据的判断；`ESTIMATE` 为带前提的工期范围，不是承诺。

## 1. 两个目标

| 目标 | 完成定义 | 当前位置 | 剩余工作的性质 | 时间估计 |
|---|---|---|---|---|
| A. 可可信跑正式实验 | 语义冻结；承重缺陷关闭；正式证据链可运行；冻结 main 经独立审阅并部署到 VM；E0 与全臂 pilot 通过 | **未达到，处于候选实现收口期** | 以关闭已知 blocker、合并 D1/D2、修实验链、Q0 tiny 和 VM 回执为主 | **ESTIMATE：8–15 个专注工作日**；若三方审计发现新 major，增加 5–10 日 |
| B. 面向本研究的高保真上限 | 不仅能跑，还覆盖计划 claim 所需的物理、信息、控制、负载、学习、测量与复现能力，并完成校准/敏感性验证 | **尚未达到；部分能力有旧平台参照，部分需新设计** | 长时窗动态性、细粒度测量、多业务/多 OD、训练韧性与选择性的物理层增强 | **ESTIMATE：目标 A 后 8–16 周**；范围扩大到数字孪生级则无固定终点 |

目标 B 必须定义为“本研究范围内的 practical ceiling”，不能定义成所有卫星网络机制都完美。未校准的 Doppler、天线、ARQ、天气或链路参数即使代码存在，也不自动提高科研可信度。

## 2. 当前事实快照

| 项目 | 当前事实 | 判定 |
|---|---|---|
| GitHub main | `12bf306de2dd7ca012feb59339262eb64913368c`；本地当前 CI 范围 `425 passed`，无参数全量 `470 passed, 1 skipped, 3 subtests passed` | FACT |
| D1 动态链路速率 | PR #55，head `408d368c...`，CLEAN，CI pytest SUCCESS；候选实现未合入 main | FACT |
| D2 动态拓扑/holding 语义 | PR #56，head `6be16cd2...`，CLEAN，CI pytest SUCCESS；候选实现未合入 main | FACT |
| 当前 VM | 部署 `a2a588d9...`，clean，2026-08-20 01:51+08:00；落后 main 且不含 D1/D2 | FACT |
| Q0 | snapshot 已在 main；planned-vs-executed、holding、Q0-I tiny 存在于未合入候选分支并收到 REQUEST_CHANGES；Q0-F 精确交叉验证未完成 | FACT |
| 正式分析链 | #64 已恢复 generic `experiment-run-manifest/v2` 的 paired analysis/claim 链并纳入 CI；`leo_sim_v2` 使用独立 request/manifest/result 合同，尚无 V2 artifact→指标重算→paired analysis→claim 闭环 | FACT，partial；R7-F1 仍 blocking |
| 三轮三方无新问题 | 只完成局部 PR/局部模块审阅，没有在最终冻结平台上完成连续三轮 | FACT，未满足 |

## 3. 目标 A：实验就绪的门禁与工期

工期按“代码和评审资源连续可用、VM 正常、没有新 blocking”估计；任务可部分并行，但最终审计与 VM 部署必须在冻结代码之后串行。

| 工作包 | 验收证据 | 当前状态 | ESTIMATE |
|---|---|---|---:|
| A0 文档与合同收敛 | 当前真相源唯一；实验清单、Q0 边界、claim 边界一致 | 本 PR 处理 | 1–2 日 |
| A1 D1/D2 入 main | 精确 head 复核有效；CI 绿；合入后 main 全量与行为对照绿 | 候选已实现、未合并 | 1–2 日 |
| A2 已知科学 blocker | 奖励正循环、mask 信息泄漏、deadline/Q0 控制范围有明确修复或冻结决策 | mask 已由 #62 关闭；其余 open | 2–5 日 |
| A3 正式证据链 | compile、review、authorize、run、receipt、analysis、claim 测试均存在并在 CI/本地通过 | generic 链已由 #64 恢复；V2 矩阵/结果分析/claim 仍 open | 2–4 日 |
| A4 Q0 最小闭环 | Q0-I tiny 与独立穷举/第二实现一致；Q0-F tiny；逐事件 replay 可归因且 receipt 持久化 | 部分候选、需返工 | 3–6 日 |
| A5 最终平台审计 | 冻结 commit 上三轮 Codex/不同模型/网页 GPT 无新增 blocking/major | 未开始最终三轮 | 2–5 日 |
| A6 VM 与 pilot | 部署同一 main SHA；VM/TF 门禁、真实 smoke、E0 重扫、全臂 pilot 自然结束 | VM 版本落后 | 2–4 日 |

最早可以先得到“工程 pilot 可跑”的时间通常短于严格平台可用门禁，约 **5–9 个工作日**；但它不能替代三轮审计和 Q0/分析链闭环，也不能直接生产论文结论。

## 4. 目标 B：研究高保真上限路线

| 层 | 需要补到什么程度 | 当前主要缺口 | 是否阻塞目标 A |
|---|---|---|---|
| 物理/拓扑 | D1/D2；长时窗接缝、极区、接入/切换边界；选择性加入 Doppler/ARQ/天线并校准 | D1/D2 未合；高级物理尚无实证校准 | D1/D2 是；高级物理否 |
| 信息 | 每类信息来源、传播、年龄、预测性与 mask 完全一致 | #62 已关闭已知 cache-hop 旁路；逐字段 AoI 尚待 EXP3 | 已知 mask blocker 已关；AoI 只阻塞 EXP3 |
| 控制 | 路由、等待、服务顺序、接入分配的权限分层 | Q0-I/Q0-J 控制范围未完全冻结 | Q0 是 |
| 流量 | uniform 主线、gravity 敏感性、多 OD/走廊/突发场景 | 命名走廊需 CSV；单 OD 结论外推有限 | 多 OD 不阻塞首批 |
| 学习 | 公平训练/评估、收敛诊断、断点恢复；按研究需要增加 temporal/path-credit/多智能体 | replay 不持久；temporal、FL/CKA 等未迁 | 长训韧性视 pilot；研究臂不阻塞 |
| 测量 | 端到端指标、丢包/积压、queue/tx/prop 分解、可重算分析 | D8 每包三分量缺失；正式分析入口缺失 | 分析入口是；D8 按 claim |
| 校准/反驳 | 旧新行为对照、极端反例、参数敏感性、外部数据校准 | 尚未形成覆盖各层的校准套件 | 部分在目标 A 后进行 |

目标 B 应以论文 claim 为边界逐项验收，而不是一次性把旧平台全部功能搬回。能力取舍见 `PLATFORM-CAPABILITY-LEDGER.md`。

## 5. 下一步顺序

1. 完成本轮文档收敛，冻结当前问题和实验程序。
2. 合入 D1/D2 后重新跑 main 行为对照与全量测试。
3. 修复正式分析链，并把相关测试纳入 CI。
4. 关闭奖励、deadline 与 Q0 replay blocker；保留 #62 的 mask 信息边界回归。
5. 实现并交叉验证 Q0-I/Q0-F tiny。
6. 在最终 commit 上执行三轮整平台审计。
7. 部署同一 commit 到 VM，跑门禁、smoke、E0 和全臂 pilot。
8. 冻结正式样本量，按 `EXPERIMENT-PROGRAM.md` 启动 EXP1。
