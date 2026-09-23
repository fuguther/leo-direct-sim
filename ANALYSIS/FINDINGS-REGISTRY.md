# 问题台账 FINDINGS-REGISTRY（唯一来源）

> **CURRENT-VOLATILE**：编号和去重规则现行有效；每条 finding 的 open/fixed/dismissed、PR、commit 和复核状态会变化，使用前须核对当前 checkout 与对应精确证据。

> 建立：2026-08-18（工作流优化 0.1）。本文件是全项目问题发现与处置的唯一台账。
> 新挖问题 / 新审阅必须先查本台账去重：命中已有编号的不得重复计为新发现；
> 未命中才分配新编号 `R<轮次>-<序号>`（如 `R4C-F2`、`R5-G2`）。
> 状态：`open`（未修）/ `fixed`（已修，附 PR/commit）/ `dismissed`（驳回，附理由）。

## 过程规则（0.1–0.3 落地版）

1. **台账优先**：任何审阅/挖问题轮次开始前，审阅提示词必须要求 reviewer 先读
   `ANALYSIS/FINDINGS-REGISTRY.md`（派发时给精确 commit 的台账路径），
   已存在编号的观察一律引用编号、禁止重复计为新发现。
2. **轮次熔断**：每个 PR 每个连续审阅周期最多 3 轮；第 1 轮审全量 diff，
   第 2 轮起只审相对上一被审 commit 的增量。3 轮后仍有 blocking/major，
   必须停止“继续派一轮”，记录根因并重规划；只有形成实质性新候选后才能开启
   新周期。D1/D2 历史总轮次已经超过 3，不能把“新周期”写成原周期内合规收敛。
   连续两轮仅剩 minor/设计项时，不再自动开新轮，转 follow-up。
3. **独立审阅真实性**：承重改动（kernel/routing/receipt/governance/learning）
   的独立复核 = 不同模型子代理冷启动（fork_turns=none，模型与主代理不同族）
   或 Codex 独立冷启动自审；禁止同模型多开冒充独立。
4. **处置闭环**：每条 fixed 必须带 PR/commit 与验证证据；dismissed 必须带理由。

## 台账

| ID | 模块 | 严重度 | 判定 | 状态 | 摘要 | 证据 | 处置 |
|---|---|---|---|---|---|---|---|
| R1-A1 | learning/reward | blocking | INFERENCE | fixed | 已关闭“额外转发跳数获得正收益”的已知风险；这不等价于已冻结 Q0 的物理字典序目标 | `4163226`：forward_step_penalty ≤ −reward_w1；零等待与非法覆盖反例；全量 `557 passed, 1 skipped, 3 subtests passed` | 训练转发奖励 = 原始 M1 queue reward + 非正逐跳成本；原始公式保留作诊断；R6-F3 继续约束 Q0 不能用 shaped reward 判最优 |
| R1-A2 | learning/information | blocking | FACT | fixed | action/decision gate 曾读取 `obs_hops` 外 cache：加入两跳目的地广告不改变观测，却会开启 forward 动作 | 修前反例 `learner.decisions=1`；#62 head `614fd23` 独立冷审 APPROVE、定向 `41 passed`、全量 `410 passed`、CI SUCCESS | #62 / main `758b606`：目的地、远端传播与队列指标共用 cache-hop 边界；C1 同时约束当前邻居来源与实际一跳传播 |
| R7-F1 | experiment_platform/PAPER | blocking | FACT | fixed | generic compile→paired analysis→claim-gate 链已由真实授权 cohort 闭合；这只关闭平台证据链缺口，不自动批准具体论文 claim | PR #159 / main `d3a116a69912dd214d89582a7b29c947f2357bfa`：R02 两个 serial VM cell 自然结束、governance eligible、双端 receipt verified；analysis manifest SHA `bc69740ec1cb5f201a79cf4749908c64e7ff4f49196b0dde7ee412bb95a6eb23`；`verify_persisted_analysis ok=true` | 平台 finding 关闭；每个实验继续执行独立 claim/value review。R02 单 seed 结果不得外推为统计、阈值或算法结论 |
| R4A2-F1 | learning | blocking | INFERENCE | fixed | sibling metadata 可重标 contract（C3/C4 同宽） | learning.py 校验链（#42 审阅） | #42 af4b115：metadata SHA 独立 config pin |
| R4A2-F2 | learning | major | FACT | fixed | metadata 非法 UTF-8 未统一转 LearningUnavailable | learning.py read_text 路径 | #42 af4b115：_read_json_bytes 统一捕获 |
| R4A2-F2i | learning | major | FACT | fixed | legacy TabularQ 不校验 state-key 宽度/表示 | test_qlearning_migration.py 16B fixture | #42 af4b115：key 宽度+有限性校验 |
| R4A2-F3 | learning | minor | FACT | fixed | TabularQ 加载端不校验 payload schema | learning.py loader | #42 af4b115：schema/顶层 key set 严格校验 |
| R4A3-F1 | learning | blocking | INFERENCE | fixed | JSON 工件 hash-then-reopen TOCTOU | metadata/payload 两次读取 | #42 af4b115：同 bytes 哈希+解析；DDQN 重开路径按威胁模型声明排除并发可写 |
| R4A3-N1 | learning | major | INFERENCE | fixed | canonical TabularQ eval 忽略 metadata pin，loader/receipt 语义不一致 | loader 分支 | #42 af4b115：canonical+pin 强制校验并记录 |
| R4A3-R1 | learning/receipt | major | INFERENCE | fixed | pin 非空时 ledger None 导致正常 eval receipt fail-closed | receipt 校验 | #42 af4b115：loader 记录实际 SHA，receipt 仅在 pin 非空时比对 |
| R4A3-F2SK | learning | major | FACT | fixed | 正确长度但不可达的 state key（NaN/Inf）静默退化 zero-row fallback | np.frombuffer 校验 | #42 af4b115：float64 表示+有限性校验 |
| R4A3-N2/F3 | learning | minor | FACT | fixed | 顶层未知字段不拒绝；显式 contract:null 被当 legacy | payload key set | #42 af4b115：精确 key set；legacy=字段缺失 |
| R4B2-A1 | kernel (snapshot) | major | FACT | fixed | 惰性 GSL GE 未物化时 snapshot 静默缺项 | snapshot_global/gsl_ge | #40 f64024c：关联时物化+显式 materialized |
| R4B2-A2 | kernel (snapshot) | major | FACT | fixed | pre-service down-wait 被报为已消耗服务时长（remaining 可为负） | _svc 相位 | #40 f64024c：_svc_phase+_tx_started_at |
| R4B2-A3 | kernel (snapshot) | major | FACT | fixed | _in_flight 仅 kind/sat/arrival_at，planner 读不到完整包状态 | _in_flight 写入口 | #40 f64024c：保留 pkt 引用+投影全字段 |
| R4B2-A3b | kernel (snapshot) | minor | INFERENCE | open(follow-up) | 控制包在途不跟踪；完整 checkpoint/resume 能力未做 | A3 审阅 | 设计 follow-up，不进 v1 |
| R4C-F1 | learning | major | FACT | fixed | 同宽 learning contract checkpoint 可跨合同加载并被重标 | #42 前 main | #42（根因同 R4A2-F1，去重引用） |
| R4C-F2 | kernel (reward) | major | FACT | fixed | ISL 服务开始后失败，_fail 把已实现 M1 奖励覆盖为 0 | kernel._fail + 复现测试 | #43 已合入 main；不等同于关闭更广的 R1-A1 奖励正循环风险 |
| R4C-F3 | learning | major | FACT | fixed | 结构无效 TabularQ checkpoint 被洗成 checkpoint_verified=true | #42 前 main | #42（与 R4A2-F2i/F3 同根，去重引用） |
| R4C-F4 | learning | minor | FACT | fixed | 畸形 JSON/entry/hex 与部分 DDQN load_model 失败未统一包装 | #42 前 main | #42 2eabd72：load_model 异常统一 LearningUnavailable |
| R4C-i-F4 | receipt | minor | FACT | fixed | field_authority 把 learning 标为 recomputed，实为 ledger_consistency | receipt.py FIELD_AUTHORITY | #42 2eabd72：改 ledger_consistency |
| R5-G1 | trace | minor | FACT | fixed | csv 模式 deadline_at_s="0" 被 `or ""` 当空处理，静默丢失 deadline | trace.py csv 分支 | #44（已合并）：strip 后判空串 |
| R5-G2 | governance | major | INFERENCE | fixed | 正式实验身份不绑定 learning.checkpoint 文件本体（仅绑定声明哈希），授权可先绿、加载时才失败 | governance.build_run_intent | #47（已合并）：seal 时校验文件存在+哈希+symlink（resolve 前逐级扫描）+metadata 未解析父目录语义 |
| R5-G3 | comparison | minor | INFERENCE | dismissed | legacy/direct 资源参数不等价（H2-13） | comparison.py 声明 | 工程对比范围明确声明 scientific_effect_claim=False，非隐藏缺陷 |
| R6-F1 | Q0 设计 | blocking | INFERENCE | open | Q0-I（在线最优）/Q0-J（联合调度）/Q0-F（clairvoyant 离线最优）的定义已冻结；真实窗口、planned-vs-executed 归因和独立求解验证仍未闭合，不能据此声称信息价值 | Q0 研究 op 13934832；`Q0-INFORMATION-ABLATION-PROTOCOL.md` | 定义不再重复设计；按协议关闭真实执行与求解证据门 |
| R6-F3 | Q0 设计 | blocking | INFERENCE | open | M1 逐跳 queue reward 与物理按时交付/时延目标不序等价，不能作 Q0 最优性判据 | 同上 | 冻结 lexicographic 物理目标 |
| R6-M1 | Q0 设计 | major | INFERENCE | open | 普通时间扩展网络流/min-cost flow 仅松弛/候选路径，不精确表达不可分/非抢占/deadline/中断 | 同上 | tiny 用 CP-SAT/event DP 交叉验证 |
| R4A4-F1RESIDUAL | learning | major | FACT/INFERENCE | fixed | save 侧仍 hash-parse 分离；DDQN save/reload 重开 pathname（威胁模型外） | R4A4 终审 | #42 2eabd72：save 单次读取；DDQN 重开按威胁模型声明 |
| R4A4-F4RUNTIME | learning | major | INFERENCE | fixed | save 不校验表状态可产出 verified 但 loader 拒收的 artifact | R4A4 终审 | #42 2eabd72：save 前复用 loader 语义校验 |
| R4A4-N3ENDIAN | learning | minor | INFERENCE | fixed | state-key 用 native-endian，跨主机可能静默 miss | R4A4 终审 | #42 2eabd72：统一 little-endian float64 |
| R6-A1 | kernel (snapshot) | minor | INFERENCE | open(follow-up) | state_version 粒度（事件级）与设计文档“任何写递增”口径不一致 | review40 子代理 | 第 3 步前统一文档口径 |
| R6-A2 | kernel (snapshot) | minor | INFERENCE | open(follow-up) | 真实传播中 in_flight 快照缺端到端回归（现为手工注入） | review40 子代理 | 补真实传播路径 E2E |
| R6-A3 | kernel (snapshot) | minor | INFERENCE | open(follow-up) | snapshot_global 对 GE 查询会推进内部状态（query-pattern 独立故安全） | review40 子代理 | 加一行注释说明只读语义层级 |
| R6-B2 | kernel (transmit) | minor | INFERENCE | open(follow-up) | down-wait 独占 server 与等待统计真空（Q0 holding-queue 同根） | #41 R4B 二审 | 设计缺口，Q0 holding-queue 一并处理 |
| R6-G2b | governance | minor | INFERENCE | fixed | 绝对路径下 macOS 系统级 symlink（/var→/private/var）会被误拒 | review47 复审 | #51（已合并）：词法根做扫描边界+解析根 containment；symlink 根绝对路径回归锁定 |
| R6-P02b | routing | minor | INFERENCE | open(follow-up) | hop 改 BFS 后 sorted_adj 未预传时仍会构建（kernel 已预计算，非逐决策成本） | review49 复审 | 可选清理：未预传时不构建 |
| R8-A1 | experiment/evidence | major | FACT | open | VM canonical 工作区 `CODE/Results/` 已不存在：`EXP-20260829-GLOBAL-PRESSURE-BRACKET-R02` 的 raw trace/ledger/receipt 在 VM 与本地均缺失，库内 24/24 `VERIFIED` 只覆盖已提交派生工件，raw event 级复现能力当前 UNVERIFIED | 2026-09-23 实测：`ls /data/论文/leo-direct-sim/CODE/Results` 不存在；全 `/data` `find -name 'EXP-20260829-...-load*'` 0 命中；`/data/liguang13/_archive-LEO-20260913/leo-direct-sim.tar.gz` 包内无 `Results`；Mac 侧同样无 `Results` | 待用户确认是否有离线备份；确认后决定是否把 raw 证据固化进 `push-remote.sh`/`pull-results-remote.sh` 的保留契约；本条不改变 R02 派生分析结论 |
| R8-A2 | CI/governance | blocking | FACT | fixed | `.github/workflows/test.yml` 在 `pytest` 前执行 `check_document_governance.py --mode all`，该步骤因 6 份 CURRENT 文档 review 过期而 `exit 1`，导致**任何 PR 都无法 CI 绿** | 2026-09-23 本地实测 `exit 1`，6 条 `STALE_CURRENT`；定时任务 `document-governance-weekly` 连续失败（2026-09-14、2026-09-21，run 34819970392 / 35575424542） | 本次 docs PR：重新核对外部状态后刷新 6 份文档的 `last_reviewed` 并更新内容；不削弱检查器 |
| R8-A3 | docs/state drift | major | FACT | fixed | CURRENT 文档记录的仓库基线与 VM 部署 SHA 双双过期，且把 `origin/main` 代码能力默认当成 VM 已部署能力 | 2026-09-23 实测：文档写 `origin/main=79796b6`，实为 `8a30409`；VM `.deployment_commit=b3a66d2`（2026-08-30），落后 7 个提交 | 本次 docs PR：三份 CURRENT 文档批量更新基线并显式区分 GitHub / VM / 本地三态 |
| R8-A4 | kernel (audit) | major | FACT | open | 决策审计字段 `peer_egress_queue_bits` 是邻居**全部方向** data+ctrl 求和，不代表包到达后实际竞争的出口队列；真正对应的是同一处的 `reverse_link_queue_bits` | `CODE/leo_sim/kernel.py:3218-3220`（求和）对比 `3212-3217`（`reverse_link_queue_bits`）；`ISLLink` 为单方向链路、data+ctrl 共享一个有限队列（`kernel.py:743-747`）；兄弟字段 `own_queue_bits` 是逐方向（`3180-3181`）；唯一相关测试仅在对称双星上断言 `==0`（`tests/test_decision_snapshot.py:65`），从未区分求和与逐方向 | 由 `T1-DOWNSTREAM-RESOURCE-PASS` 门关闭：新增候选动作级、固定 downstream policy 下的具体 egress / 到达前 workload / 在服务剩余量 / 控制积压真值 |
| R8-A5 | kernel (timing) | major | FACT | open | 每决策无唯一 `decision_id`，同一包的重决策在 decision sink 中不可区分；且 `_decide` 全段无 `yield`，观察→选择→提交共处一个 `env.now`，决策计算时延未进入模拟时间 | 全仓 `decision_id` grep 0 命中；`_decide` `kernel.py:3274-3437` 区间内 `yield` 计数为 0；sink 行仅以 `(t,pid,sat,kind)` 为键（`3168-3184`）；重决策入口 `_redecide_pending` `3439-3444`、`_redecide_cell_pending` `2762-2782` | 由 `T1-TIME-LEDGER-PASS`（`decision_id` + 完整时间链）与 `T1-COMPUTE-DELAY-PASS`（`decision_start → timeout → revalidate → commit`）两门关闭；均为 opt-in，关闭时须与旧行为等价 |

| R8-A6 | kernel (audit) | major | FACT | fixed | 控制信息到达时刻 `t_control_rx` 在**目标配置**下恒为 MISSING：`_decision_info_audit` 只在 `learner is not None` 时填 `cache_entries`，而非学习运行的 `contract` 为 `None`，于是 2026-09-23 分层审查指定的 T1 第一版配置（deterministic router + learning off）拿不到该字段 | 280 星诊断 profile（`population_global_1deg_diagnostic.yaml`，`control_plane.enabled: true` + `routing.policy: hop` + `learning.algorithm: none`）实测 `t_control_rx` **0/534**；6 星环夹具 0/19；该字段是"邻居状态时间错位"的核心自变量 | 本 PR：`_decision_info_audit` 增 `elif self.cfg_cp["enabled"]` 分支，用 `caches[sat].valid_entries(now)` 记录节点实际已知的全部有效 cache 条目（非学习运行无 contract 可裁）；修后 6 星环 19/19、280 星 534/534；`test_decision_snapshot.py` 断言 `cache_entries == {}` 的场景控制面关闭，不受影响 |
| R8-A7 | kernel (audit) | major | FACT | fixed | hold / fail 决策**静默泄漏 decision_id**：`_decide` 入口无条件分配 id，但 `_record_decision` 只在 forward/deliver 两个提交点调用，故每次 hold（`no_info` 等广告、几何/GE 暂不可用、MCS 零速率）或 fail 都消费一个 id 却不留任何落盘痕迹——既无决策行，也无里程碑（`redecision` 里程碑只在 `pkt.decision_id is not None` 时写且携带新尝试的 id） | 精确 id 账目：强制 hold 场景（hop + 控制面开）`ROW ids=[12,13]` 而 **id 0..11 全部无痕**；连最简单的双星 oracle 场景也有 1 次无痕 hold（`ROW ids=[1,2]`，id 0 无痕） | 本 PR：`_hold_packet`/`_fail` 增 `decision_id` 形参并在 `timeline_sink` 上写 `hold`/`fail` 终止里程碑；`_decide` 内 10 个终止点显式传入。修后三个场景 **0 个无归属 id**。只写 timeline，不碰 `decision_sink`（其形状与条数被既有测试锁定） |

## Open / Follow-up 清单

- R7-F1 已由 R02 真实授权 cohort 关闭；逐实验 claim/value review 是持续治理要求，不再作为同一平台缺陷重复登记。
- R4B2-A3b：控制包在途跟踪、Q0 snapshot → 完整 checkpoint/resume（设计 follow-up）。
- R6-F1/R6-F3/R6-M1：Q0-I/J/F、物理目标和精确算法合同。
- R6-A1/R6-A2/R6-A3/R6-B2/R6-P02b：已登记的 snapshot/holding/routing follow-up。
- R8-A1：R02 raw 证据缺失，待用户确认离线备份后决定保留契约（不阻塞 T1 工程，但阻塞 raw event 级复现声明）。
- R8-A4/R8-A5：T1 测量能力缺口，分别由 `T1-DOWNSTREAM-RESOURCE-PASS` 与 `T1-TIME-LEDGER-PASS` + `T1-COMPUTE-DELAY-PASS` 关闭。
- R8-A6/R8-A7 已 fixed（见上表）；二者是 `T1-TIME-LEDGER-PASS` 判定为"未通过"的直接原因，修后该门禁的能力项才齐备。
- `EXPERT-REVIEW` 与 NOTES 只作证据来源；任何仍需处置的历史项必须先在本表分配 ID，
  不允许只存在于其他文档的“隐形 open item”。本轮已先迁入 R1-A1/R1-A2；其余历史项
  需逐条核验后再登记，不能批量假设仍 open 或已 fixed。

## 使用说明

- 新增发现：先 `rg "R\d+[A-Z]?-\d+" ANALYSIS/FINDINGS-REGISTRY.md` 查号，无命中则取下一序号。
- 修完：把状态改 `fixed`，补 PR/commit 与验证数字；驳回：改 `dismissed` 并写理由。
- 台账随每次审阅/修复轮次结束同步更新并提交，作为该轮 PR 的一部分或独立 docs PR。
