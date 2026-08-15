# 迁移精华清单（旧平台 → 新平台）

> 日期：2026-08-16。依据：用户原始计划《LEO仿真平台V2_卫星直连与旧机制清理计划》（2026-08 中旬，已存 `ANALYSIS/LEO-V2-ORIGINAL-PLAN.md`）、两平台逐行说明书（02-kimi-platform-spec）、差异对照（03）。
> 核心原则（计划原文）：**V2 的变更是为了更仿真；训练侧语义（奖励、观测）与旧平台修正版保持一致**——「M1 的正确队列奖励和 M2 的本地出向队列观测吸收为统一基线；删除开关」。

## A 类：计划已判删除 → 不迁移（无需再议）

| 能力 | 旧平台位置 | 备注（说明书证据） |
|---|---|---|
| Q-Learning 表 | SimulationRL.py:5682 | 计划删除项；新平台用解析基线（hop/delay/capacity/oracle）替代 |
| MAPPO | routing_mappo.py | 计划删除项；且实测为未完成死代码（RecurrentMAPPOAgent 无实例化、train_ppo_update 仅 raise NotImplementedError:564-567） |
| path-credit | routing_path_credit.py:341/1014 | 计划删除项 |
| temporal/multistep（GRU 时序编码、n-step/TD-λ） | temporal_encoder.py、routing_multistep.py | 计划删除项 |
| M3、线性奖励、旧 checkpoint 兼容 | SimulationRL.py 多处 | 计划删除项（原文：「不进入 v1，所有模型重新训练」） |
| C2、dataRate/dataRateOG 重复入口 | — | 计划删除项 |
| Gateway 全家（类、4/31 网关流量入口、inputRL*） | SimulationRL.py:2573 等 | 新架构已替代（计划第 1 节） |
| SIM_* 兼容别名、仿真内绘图 | — | 计划删除项（改离线分析） |
| legacy 切换模式 | SimulationRL.py:744-751 | 新 BBM/MBB 状态机替代 |
| FSOlink | SimulationRL.py:1827 | 计划未点名，但实测从未实例化（死代码）→ 不迁 |
| monitor dashboard | monitor.py | 操作工具，非仿真语义；需要时可另写 |
| save_on_interrupt | SimulationRL.py:11356 | 新平台以自然结束回执为唯一完成形态，语义不兼容 |

## B 类：计划明确保留/要求一致 → 迁移或核验（按优先级）

| # | 能力 | 旧平台位置 | 新平台现状 | 建议 |
|---|---|---|---|---|
| B1 | **M1 正确队列奖励** `w1·exp(−β·t)` | SimulationRL.py:10269（docstring 记 M1 fix） | 待核验（疑似漂移，用户报告的 training bug 嫌疑点） | **最高优先**：逐分量差分对照，今夜任务 1 的锚点 |
| B2 | **M2 本地出向队列观测** | SimulationRL.py（_appendOwnQueueM2:9866 等） | 待核验 | 同上，与 B1 同包核验 |
| B3 | 真正 Double-DQN（online argmax + target eval + next mask） | DDQNAgent:6190 | 已实现（learning.py:276、ddqn_targets:804） | 已一致，差分测试固化防漂移 |
| B4 | C1/C3–C7 合同语义（计划定义：C1=自身+一跳；C3–C7 同 vis_k 缓存，差别仅在表示/聚合/AoI） | DDQNAgent + getDeepState 家族 | 已实现（learning.py:593/724） | 核验合同逐条等价；测试 test_learning.py 已有部分覆盖 |
| B5 | **链路预算/香农速率**（计划原文：「经表征测试确认正确的轨道、几何、ISL 和链路预算计算」明确保留） | get_data_rate:8295、los_slant_range:8282 | **缺口**：新平台链路速率为配置常数 | **高优先迁移**：先用表征测试固定旧数值，再作为可选速率模型迁入（E1 已发现瓶颈在接入侧，速率建模直接影响主线结论） |
| B6 | tffunc + fast_train | DDQNAgent fast_train | 已有 _build_fast_train_fn（learning.py:446） | 计划要求「重新做逐位/容差等价 A/B，旧加速数字不继承」→ 归性能 profile 工作包 |
| B7 | 人口栅格、M-Lab 数据与 provenance | — | 已在新平台（population_gravity、mlab 模式） | 已完成 |
| B8 | 实验链（编译/三角色审阅/授权/远程/scheduler/receipt） | — | 已在新库 | 已完成 |
| B9 | MBB、随机中断、AoI 机制思想 | — | 已在新平台重实现 | 已完成 |

## C 类：计划未明说 → 待用户逐项拍板

| # | 能力 | 说明 | 我的倾向 |
|---|---|---|---|
| C1 | 确定性 link_outage 调度表（link_outage.py:50） | 可控中断实验可能服务信息年龄主线（如「中断后信息陈旧」场景） | 低优先迁移（新平台 GE 随机中断已覆盖一般情形） |
| C2 | visK 状态编码旧实现（getDeepStateVisK 等，SimulationRL.py:9566-9952） | 不迁移，但作为 C1–C7 旧实现的**参照物**保留在旧库供差分 | 不迁，仅参照 |
| C3 | replay buffer 跨运行持久化/续训（save_replay_buffer:10475 等） | 长训练分段续跑可能有用 | 低优先 |
| C4 | 旧后处理/绘图函数群 | 论文出图风格参考 | 不迁，需要时按新账本数据重写 |

## 用户确认项

- A/B 两类如无异议即按此执行；C 类四项请逐项批复（迁/不迁/暂缓）。
