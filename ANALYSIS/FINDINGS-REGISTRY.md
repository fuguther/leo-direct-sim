# 问题台账 FINDINGS-REGISTRY（唯一来源）

> 建立：2026-08-18（工作流优化 0.1）。本文件是全项目问题发现与处置的唯一台账。
> 新挖问题 / 新审阅必须先查本台账去重：命中已有编号的不得重复计为新发现；
> 未命中才分配新编号 `R<轮次>-<序号>`（如 `R4C-F2`、`R5-G2`）。
> 状态：`open`（未修）/ `fixed`（已修，附 PR/commit）/ `dismissed`（驳回，附理由）。

## 过程规则（0.1–0.3 落地版）

1. **台账优先**：任何审阅/挖问题轮次开始前，审阅提示词必须要求 reviewer 先读
   `ANALYSIS/FINDINGS-REGISTRY.md`（派发时给精确 commit 的台账路径），
   已存在编号的观察一律引用编号、禁止重复计为新发现。
2. **轮次上限**：每个 PR 独立审阅最多 3 轮；第 1 轮审全量 diff，
   第 2 轮起只审增量（相对上一被审 commit 的 diff）；连续两轮仅剩
   minor/设计项时，不再自动开新轮 → 合并 + 在台账记 `follow-up`；
   仅 blocking/major 触发下一轮。
3. **独立审阅真实性**：承重改动（kernel/routing/receipt/governance/learning）
   的独立复核 = 不同模型子代理冷启动（fork_turns=none，模型与主代理不同族）
   或 Codex 独立冷启动自审；禁止同模型多开冒充独立。
4. **处置闭环**：每条 fixed 必须带 PR/commit 与验证证据；dismissed 必须带理由。

## 台账

| ID | 模块 | 严重度 | 判定 | 状态 | 摘要 | 证据 | 处置 |
|---|---|---|---|---|---|---|---|
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
| R4C-F2 | kernel (reward) | major | FACT | fixed(待拍板) | ISL 服务开始后失败，_fail 把已实现 M1 奖励覆盖为 0 | kernel._fail + 复现测试 | #43（行为改变，留用户拍板） |
| R4C-F3 | learning | major | FACT | fixed | 结构无效 TabularQ checkpoint 被洗成 checkpoint_verified=true | #42 前 main | #42（与 R4A2-F2i/F3 同根，去重引用） |
| R4C-F4 | learning | minor | FACT | fixed | 畸形 JSON/entry/hex 与部分 DDQN load_model 失败未统一包装 | #42 前 main | #42 2eabd72：load_model 异常统一 LearningUnavailable |
| R4C-i-F4 | receipt | minor | FACT | fixed | field_authority 把 learning 标为 recomputed，实为 ledger_consistency | receipt.py FIELD_AUTHORITY | #42 2eabd72：改 ledger_consistency |
| R5-G1 | trace | minor | FACT | fixed | csv 模式 deadline_at_s="0" 被 `or ""` 当空处理，静默丢失 deadline | trace.py csv 分支 | #44（已合并）：strip 后判空串 |
| R5-G2 | governance | major | INFERENCE | fixed | 正式实验身份不绑定 learning.checkpoint 文件本体（仅绑定声明哈希），授权可先绿、加载时才失败 | governance.build_run_intent | #47（已合并）：seal 时校验文件存在+哈希+symlink（resolve 前逐级扫描）+metadata 未解析父目录语义 |
| R5-G3 | comparison | minor | INFERENCE | dismissed | legacy/direct 资源参数不等价（H2-13） | comparison.py 声明 | 工程对比范围明确声明 scientific_effect_claim=False，非隐藏缺陷 |
| R6-F1 | Q0 设计 | blocking | INFERENCE | open | 必须区分 Q0-I（在线最优）/Q0-J（联合调度）/Q0-F（clairvoyant 离线最优），否则未来信息优势被错误归因为当前信息优势 | Q0 研究 op 13934832 | 设计合同，§5 冻结后实现 |
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

## Open / Follow-up 清单

- R4B2-A3b：控制包在途跟踪、Q0 snapshot → 完整 checkpoint/resume（设计 follow-up）。
- R4C-F2：等待用户拍板（保留已实现奖励 vs 设计上失败=0）。
- R4C-F4 / R4C-i-F4：已改在 #42 分支工作区，随 #42 终审后并入。
- R5-G1：修复分支已建，待完成+测试+PR。
- R5-G2：治理链补 checkpoint 文件本体校验（建议下轮实现）。
- 跨轮历史项（R1–R3、专家审阅 A–D）：见 `ANALYSIS/EXPERT-REVIEW-20260816.md` §A–I 与 NOTES.md，不在本台账重复编号。

## 使用说明

- 新增发现：先 `rg "R\d+[A-Z]?-\d+" ANALYSIS/FINDINGS-REGISTRY.md` 查号，无命中则取下一序号。
- 修完：把状态改 `fixed`，补 PR/commit 与验证数字；驳回：改 `dismissed` 并写理由。
- 台账随每次审阅/修复轮次结束同步更新并提交，作为该轮 PR 的一部分或独立 docs PR。
