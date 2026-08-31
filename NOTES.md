# NOTES.md

> ROLLING LOG；入口说明最后整理：2026-09-01。
> 本文件只记录最近操作、证据位置和下一步，不是平台状态真相源。
> 当前状态见 `ANALYSIS/CURRENT-EXPERIMENT-READINESS.md`；截至 2026-08-19 的原记录见
> `ANALYSIS/HISTORY/NOTES-THROUGH-20260819.md`。

## 2026-08-30：本地 Git 资产与历史文档第一批收口（PR #189）

- 根入口保持 clean `main@b3a66d2`；10 个已合入或已建立恢复点的临时 worktree 已解除，worktree 总数由 15 降至 5。R02 driver、两个含忽略结果的 evidence worktree 与 Codex 管理的 b228 均未触碰。
- 43 个经 PR source/squash patch 或 main 祖先逐项核验的本地分支已删除，本地分支总数由 61 降至 18；11 个含独有增量或来源不明的分支继续保留。
- 三个 dirty DSH worktree 已分别保存为 stash `b66b08e…`（posterior 分析早期稿）、`3a4d811…`（Markdown disposition 审计）、`ddc738c…`（控制面文档源稿）；原 Q0/b228 用户内容继续由 stash `6318b7a…` 保护。
- 13 份已登记为 `HISTORICAL`/`SUPERSEDED` 的 Markdown 移入 `ANALYSIS/HISTORY/`，同步更新登记、历史索引与 `experiment-program.yaml` 证据路径；不删除历史内容，不改变现行合同或实验语义。
- 归档暴露出治理检查器用 `fnmatch` 解释 glob、与 `Path.glob` 展开语义不一致；已用先红后绿的回归测试改为路径语义匹配。归档后审计为 0 error / 0 warning / 0 archive candidate；本地全量 `843 passed / 2 skipped / 3 subtests passed`（另有 1 个既有未知 mark warning）。

## 2026-08-30：Q0 长版源稿与剩余资产收口（PR #190）

- 用户批准剩余资产按推荐收口：Q0 长版说明书不再作为第二权威入口，原文移入 `ANALYSIS/HISTORY/`；其中仍有价值的 oracle 边界、四层算法验证门、求解状态/最优性差距要求已提炼进当前 Q0 协议。
- 浏览器临时日志、已被 main/PR 吸收的旧草稿与测试修改不入库；相关 stash、旧分支和 b228 旧任务只在本 PR 合入后删除。
- 归档正文与 stash 原稿逐字 diff 一致；document governance 为 0 error / 0 warning / 0 archive candidate；文档专项 `19 passed`，本地全量 `843 passed / 2 skipped / 3 subtests passed`（另有 1 个既有未知 mark warning）。
- PR #190 CI `pytest` 通过并合入 main 后完成实体收口（结果留痕 PR #191）：旧 Codex 任务“明确并行实验规划需求 (2)”已归档，b228 worktree 已移除；15 个本地旧/任务分支与 9 个 GitHub 普通旧分支已删除，4 个 stash 已逐个核对哈希后删除。该次快照最终仅保留 main、R02/证据所需 3 个本地分支与 4 个 worktree；当时的 77 个 namespaced ProjectPilot 审阅证据分支继续保留，不作为当前工作入口。当前数量必须从 Git refs 实时重算，不由本日志维护。

## 2026-08-30：P1 实验设计记账与科研门分层（PR #186）

- matrix compiler 新增 `design_accounting`：分别记录 planned cells、唯一 resolved config、精确重执行 cell 与 run-id 分组；analysis request 和 RUNBOOK 同步绑定。完全相同配置的重执行明确只算重复性证据，不增加独立条件数；旧格式编译包继续由 exact-SHA/后验兼容链处理，不改写正在运行的 R02 授权工件。
- Run 产物契约明确拆分“运行/证据准入门”和“科研充分性门”：acceptance 与 governance `research_eligible=true` 不能替代场景、物理、统计和逐 claim gate。
- 当前 R02 管理口径冻结为一次性描述性场景/稳定性诊断：24 cells=12 唯一配置+12 精确重执行，且预注册上界表明当前 bracket 无法回答 ISL 压力阈值。运行结果尚未在本条提前填写。
- 独立 Luna 冷审发现一个 major：旧授权矩阵没有 compiler 预填的 `design_accounting` 时，analyzer 仍会省略独立条件记账；当前 R02 正属于该兼容路径。修复改为始终从授权 matrix cells 派生并输出，声明字段存在时仍严格核对，既不重写旧授权也不改变 exact-SHA 绑定。新增 sealed historical authorization 回归先以 `KeyError: design_accounting` 失败，最小修复后通过。
- 验证：首轮定向 matrix/v2-analysis/document-governance `94 passed`；首轮全量 `837 passed, 2 skipped, 1 warning, 3 subtests passed`。冷审修复后定向 matrix/v2-analysis `77 passed`，最终全量 `842 passed, 2 skipped, 1 warning, 3 subtests passed`；document governance `0 errors, 0 warnings`；`git diff --check` 通过。唯一 warning 为既有未注册 `scene_smoke` mark。

## 2026-08-29：Bracket R02 审阅链闭合与授权（PR #179-#183）

- 链路：请求编译（#179）→ 24-cell 判定性设计修订（#180）→ brief schema 修复（#181）→ revision_reason（#182）→ 链工件（#183）。
- 四轮三角色 Kimi 审阅（4096c2f / 7169192d / bd1dea4 / 609f9892）：round-1 两 REQUEST_CHANGES（跨负载配对合同阻断、零 acceptance）→ 设计修订；round-2 两 REQUEST_CHANGES（brief JSON 语法 + v2 schema 缺字段）→ 重写；round-3 cold/sat 命中 revision_reason 阻塞 → #182；round-4 三 PASS 闭链（矩阵字节级未动）。
- finalize_decision.py ACCEPTED；authorize_experiment.py AUTHORIZED（24 runs）。
- 同日 GitHub runner 池异常引起 CI 多次冻结，最终以本地全量 836 passed x2 佐证内容，远端 CI 各 PR 均已绿。

## 2026-08-29：R02 acceptance 尺度修正与链重建（PR #184/#185）

- Cell1 实跑（natural_end, conservation_ok, 170/132/38 同型 R01）证明 500 门不可满足；按 round-1 审阅者预案降级 {1,0,true,true}（#184）。round-5 三审 PASS（5e96b41）；链重建 rev4：decision/finalization ACCEPTED、authorization 24 runs 替换旧授权（#185）。

## 2026-08-30：Bracket R02 运行完成与验证分析（24/24 VERIFIED）

- 24 cells（新 limits config 全量重跑）全部自然结束：receipt 全绿（natural_end/conservation/research_eligible），v2_analysis VERIFIED 24/24（bound manifest 链）；确定性 a/b 对 12/12 差值恰为 0；delivery_rate 描述性：load10 ~0.76-0.78 / load20 ~0.78-0.81 / load40 ~0.72-0.76 / load80 ~0.60-0.65（load80 出现下降）。
- scene_check 24/24（manifest 绑定路径）：全 ACCESS_LIMITED（admission_rate < 0.95 门）；ISL 压力候选 0（与预注册期望一致：ISL 门在 bracket 物理不可达）；route-stalled 截断残留伴报（预注册披露）。
- claim-gate 状态：READY_FOR_INDEPENDENT_CLAIM_REVIEW。证据快照入库（本 PR 同批）。

## 2026-08-30：R02 执行上限修正与链 rev5（PR #187/#188）

- Cell 13（load40_a-s7）实跑被 CapExceeded（entities 2001 > max_entities=2000）中断（natural_end=false, conservation_ok, 7.3M events, 零丢包）——R01 遗留容量门。limits 提升 max_entities=20000 / max_events=1e8（#187）；round-6 三审 PASS（fb75e31）；链 rev5 重建（#188）。前 12 cells（load10/20 旧 config）superseded，24 cells 全量重跑。

## 2026-08-29：状态包原子更新（PR #177）

- 4 份 update_now 关闭：CURRENT-EXPERIMENT-READINESS / EXPERIMENT-PROGRAM / PLATFORM-CAPABILITY-LEDGER 新增 2026-08-29 CURRENT 快照节；experiment-program.yaml 补 preregistered 枚举并置 v2_formal_evidence_chain_verified / global_scene_repeat_analysis_verified=completed_verified；DOCUMENT-STATUS.json 4 条目 last_reviewed=2026-08-29。
- 证据：document-governance 0/0、test_document_governance 18 passed、YAML 解析通过、diff --check 干净。

## 2026-08-29：R02 round-2/3 审阅管线（PR #180/#181）
- 第三次冻结（11:23Z 起 run d4e8b92，Run test suite 22+ 分钟无进展、updated 冻结在启动时刻；池在 10:39Z-11:0xZ 曾恢复绿 2 轮）。关键路径受影响，继续以并发推送重启，直至一轮绿。
- CI 重启历程（PR #180/#181）：11 次 push 触发 run，其中 4 次在 Run test suite 冻结（runner 池异常，status 页 operational）；成功样例：main push run 与 #179 均绿；本地 836 passed 两次佐证。附注：冻结仅出现在 10:20 后 PR 侧 run。

- round-2 于 7169192d：cold PASS；sat/adv REQUEST_CHANGES——全部集中在 brief.json（JSON 语法错误 + 缺 agent-work-package/v2 必填字段 + v1 陈旧文案）；编译链 31 绑定哈希全绿。
- 修复：brief 重写（16 字段合法 JSON）→ PR #181。
- 同日 GitHub runner 池异常：10:20 起多次 pull_request run 在 Run test suite 冻结（status 页 operational 但实测 3/7 冻结），本地同树全量 836 passed 两次佐证内容无虞；用并发 cancel-in-progress 推新提交重启。

## 2026-08-29：R02 round-1 三角色 Kimi 审阅证据记录

- cold_start: REQUEST_CHANGES（major: acceptance 全零；minor: 无 per-cell execution_authorized 字段，与 R01 同构，非缺陷）。
- satellite_drl: PASS（major advisory: ISL 压力门在 10-80 Mbps bracket 物理不可达，单链路漏斗上界 ~0.135 < 0.8；major advisory: route-stalled 与 10s 截断混淆；minor: 截断指标披露；minor: acceptance 硬化）。
- adversarial: REQUEST_CHANGES（major: 分析器配对合同要求同 trace identity，跨负载 nested child trace 无法配对——设计级；minor: scenario 名 r01 残留、RUNBOOK 缺拉回/失败流程、determinism 措辞）。
- 处置：24-cell 逐负载 a/b 确定性设计 + 正式 acceptance + r02 命名 + brief 预注册期望（PR #180）。

## 2026-08-29：Bracket R02 请求包与 round-1 三角色审阅（PR #179/#180）

- PR #179 合入 18-cell 初版；round-1 Kimi 三审（cold_start REQUEST_CHANGES、satellite_drl PASS、adversarial REQUEST_CHANGES）发现：分析器配对合同阻断跨负载对比（设计级）、全零 acceptance 不 fail-loud（证据级）、scenario 名残留、claim 措辞。
- 修订为 24-cell 逐负载 a/b 确定性对 + 正式 acceptance {500,1,true,true} + scenario r02 命名（PR #180）。

## 2026-08-29：后验分析授权身份重准入（P0 闭环，PR #176）

- 根因：strict `verify_authorization` 用当前代码重推 code_sha256/execution_chain/config 身份，更新的分析 checkout 无法合法分析历史正式运行（01c323a 全球压力双臂），W6 分析闸门卡死。
- 修复（`CODE/experiment_platform/v2_analysis.py`）：新增私有 `_verify_authorization_bound()`（payload 封签 + work_finalization/绑定工件哈希 + 行结构身份，快照级校验，不重推当前身份）；`analyze()` `authorization_mode=auto` 仅在 strict 拒绝且 bound 校验通过时回退，manifest 记录 `authorization_verification=bound_posterior` 与 strict 原错误；`--authorization-mode strict` 永不回退；篡改工件/改写 finalization/重封签伪造身份全部 fail-closed，运行身份仍由 formal/governance v2/external witness/receipt 链强制绑定。
- 证据：
  - 焦点测试 `test_v2_analysis.py` 52 passed（新增 7 项反例：历史授权 bound 回退、strict 不回退、篡改工件、改写 finalization、重封签伪造、错误记录摘要、unsupported mode）；相邻六文件 131 passed；全量 pytest 以 PR #176 required CI 为准。
  - 真实样本端到端（历史 01c323a 授权 + VM 回执 + external witness，本地 3.14.2 vs VM 3.11.15）：status=VERIFIED、2 runs、`authorization_verification=bound_posterior`、`analysis_mode=posterior_governed_runtime`、双臂 `runtime_identity_binding=governance_bound_posterior`、evidence_class=v2_external_witness、重复对比差异 0.0；`verify_persisted_analysis` ok=true。
  - scene_check（`--analysis-manifest` 绑定后验清单）：双臂 status=ACCESS_LIMITED、integrity_ok/coverage_ok=true、双臂完全一致（155 目的地、82 ISL 暴露包、0 压力候选、route-stalled 11 pids、downlink 干净）。
- 科研口径：10 Mbps 双臂为完整性/重复性检查点（差异 0.0），不升格为负载阈值；global 场景当前 classify 为 access-limited，ISL 压力候选为 0，新负载 bracket 决策须以本证据为基础。
- 现场：分析详见独立工作树 `/private/tmp/leo-posterior-analysis-20260829`（`ANALYSIS/EXP-20260826-GLOBAL-PRESSURE-BRACKET-R01/v2-analysis/` 与 `scene-check-load10_{a,b}.json`），结果目录不入库。

## 2026-08-25：全球人口区域直连接入场景实施完成（DeepSeek Harness，PR_READY_FOR_INDEPENDENT_REVIEW）

- 2026-08-26 PR #167 首次 CI 在干净 Ubuntu runner 上为 `13 failed, 745 passed, 3 skipped, 3 subtests passed`；13 项同源于 workflow 未安装运行时已使用的 Pillow（`ModuleNotFoundError: PIL`），不是 13 个独立仿真缺陷。最小修复仅在 CI 安装清单钉住 `pillow==12.0.0`；受影响的 platform/receipt/trace 测试本地复验（排除约 4 分钟的 scene smoke）为 `51 passed, 1 deselected`，最终状态以修复提交后的 GitHub required CI 为准。

- 实施分支 `dsh/20260825-global-direct-access`，隔离 worktree `/private/tmp/leo-dsh-global-access-20260825`。
- 基线 SHA=`0290e93946bedcca4cca04e8199dba43d5509f92`（= supervisor 指定的 origin/main）；最终 HEAD=`29f78fb4809a73149bc6fb880e276d53341b0a1f`。
- 提交链（8 个，按任务）：`d77df0b` 配置契约冻结；`c21144b` 轨道相位块；`ec00dca` 全人口覆盖审计；`9bb7306` local-time 人口代理；`68713bc` alias 目的地采样；`f445a1f` 严格 nested 负载族；`b987578` 分层 scene 分类器；`29f78fb` 有界诊断 profile。
- 本次实施文件集（base..HEAD，共 20 个）：`config.py coverage.py kernel.py model.py receipt.py rng.py scene_check.py trace.py trace_family.py profiles/population_global_1deg_diagnostic.yaml` + 9 个测试文件；无 `.docx`/RL/Q0/learning/mentor/实验请求/授权/结果目录改动。
- 基线测试：`686 passed, 1 skipped, 3 subtests passed`（Task 0 记录）。最终全量 CI：`760 passed, 1 skipped, 3 subtests passed`；含唯一 5 Mbps 本地 smoke（约 4-5 分钟）。
- 文档治理 `--mode all`：`0 errors, 0 warnings`。
- 关键差异（相对计划）：
  - runner 身份：实际执行 harness 为 npm 安装的 DeepSeek Harness `0.1.1-rc.2`（源码 checkout 不携带 git 提交元数据），计划钉的 `0.1.0-rc.8@141eb6fe` 仅存在于 `/Users/lge/deepseek-harness` 的干净源码 checkout。经 Codex 裁决：接受差异并继续，回执如实记录、不声称 runner 等价。
  - Task 7 停止条件：计划要求按 `satellite_ingress` 事件把历史双义 fate `ACCESS_QUEUE_OVERFLOW` 拆成 pre-ingress(access-limited)/post-ingress(downlink-limited)，但既有 receipt v2 事件权威把 `satellite_ingress+ACCESS_QUEUE_OVERFLOW` 判为矛盾，使合法下行溢出 run 无法通过 L0 验证（实测 3 包均报 terminal access fate）。经 Codex 裁决：授权最小 receipt 修正（仅 `ACCESS_REJECTED+ingress` 保留为矛盾；`ACCESS_QUEUE_OVERFLOW+ingress` 作为合法下行溢出证据），证据全文见 `/tmp/leo-dsh-task7-stop-evidence.md`。
- 证据与回归：
  - legacy population profile `trace.csv` SHA=`0780da2fedea503d5f600830aecc805c95b1b8fc098395150ecaf2185846279a`（不变）；legacy identity/v2 仍可重建=`2715dfb316de48d958cd05fa09aafcf22e340766d186e7a0a9a9b6a4b0dd9ad4`。
  - 1° 600 s/60 s 覆盖 smoke 两次输出 SHA 完全相同=`0f6117bca0095adf28f28328b6c6e445585fd01df32d9819f23011a2b2c8407d`；endpoints=16988、samples=11、source raster SHA=`c5742d16fc01d454e8ac5c5345a7e7716883acd28ac4d0d34c24613bc315e59a`。
  - 5/10/20/40/80 trace 族：master 1073 包；child 60/123/268/541/1073 包，全部严格多重集子集，child 与 companion 独立 verifier 均空错误，五个 child 共享同一 family identity。
  - 5 Mbps 本地 smoke（isolated `/tmp/leo-5mbps-smoke-evidence.json`）：natural end、conservation、receipt verified；wall≈249 s、peak RSS≈1.59 GB、events=16,796,444；86 offered → 74 delivered / 12 in-system、0 access/route/downlink 失败。该 run 是唯一本地工程 smoke（cheap path），未跑 10/20/40/80 网络臂、未上 VM。
  - alias_rejection 基准：10,000 目的地抽样，1° 表 scan≈72.4 s、alias≈1.08 s（约 67×），零 self/invalid 目的地；201-source 采样最坏 10,000 次拒绝耗尽概率≈7.1e-12 < 1e-9。
- 限制（Not done by this package）：全 24 h 覆盖结果（资源门未超限，本次仅做 600 s/60 s 与一次基准推算，未跑 24 h 全量 41,102,126,240 比较）、VM 压力标定菜单、正式 load bracket、多 seed 统计、信息消融、RL/新算法比较、论文 claim、mentor 报告更新。全部承重改动按计划未经本仓自批，等待独立冷审。

## 2026-08-25：全球人口区域直连接入场景实施计划（仅计划）

- 基于 clean `origin/main@98d9092751abd84a3d3ad6b39e932e5e501740c0` 新建隔离分支 `codex/20260825-global-access-plan`；基线 `python3 -m pytest CODE/leo_sim/tests CODE/tests -q` 为 `598 passed, 1 skipped`。用户原工作树保持只读且未处置其中改动。
- 新计划 `docs/superpowers/plans/2026-08-25-global-direct-access-scene.md` 将场景口径冻结为：1° 全球正人口候选区域、有限运行中动态稀疏活跃、population + local-time proxy 流量、coverage/access/route/ISL 分层判定、严格 nested master trace 负载族。当前 GPW 工件 SHA=`c5742d16fc01d454e8ac5c5345a7e7716883acd28ac4d0d34c24613bc315e59a`，1° 候选数为 16,988；0.5° 仅保留后续敏感性。
- 本工作单元不改平台代码、不跑正式矩阵、不改两份导师报告；用户后续指定由 DeepSeek Harness 执行。计划已加入 runner 版本锁定、隔离工作树、逐任务 TDD、越界停机与 exact-SHA 交接合同；DeepSeek Harness 必须停在独立复核就绪的 PR，不得自批承重改动。后续算法比较必须等全球覆盖、接入清洁和真实 ISL 压力候选依次关闭。
- Kimi 第一冷审轮判定 `REQUEST_CHANGES`；Codex 已逐项核对并收紧计划：全球 vector coverage 使用独立且有限的 20,000 端点/500 亿比较/4 GiB 上限，不放宽 legacy scalar cap；nested 仅允许 population-gravity，补齐 `nested_filter` RNG/receipt 与 companion 文件防护；决策比例写死 offered/admitted 分母；ISL 压力改为同一有向链路三个连续窗口且同链路队列等待为正。另保留旧 trace identity，补 alias 接受率/耗尽概率和浮点边界回退验收。
- 本地继续核对发现内核历史上把源端 uplink 与目的端 downlink 队列溢出都记成 `ACCESS_QUEUE_OVERFLOW`。计划不扩大到改 fate 合同，而要求 scene checker 用已核验的 `satellite_ingress` 事件分流：入网前计 access-limited，入网后计 downlink-limited；另把已入网但停在 holding、从未暴露于 ISL 的包判作 route-limited，避免把接入、路由或下行故障误叫 ISL 压力。
- Kimi 第二审阅视角再次命中 trace identity 与 RNG 证据链问题。最终计划采用显式 identity/v3，并冻结 identity/v2 重算器以保证旧 v2 receipt 可复核；`nested_filter` 追加为 canonical child 7，禁止与既有 child 1 `ge_gsl` 复用。scene checker 的八个单运行状态、低样本阈值语义、data-only ISL 利用率边界以及与现有 paired `isl_pressure_decision.py` 的职责也已写死。
- PR #166 的 head `eb7fad516275de68767750efd132e10d8b949096` 已通过 required `pytest` CI（run `32835577615`，job `97763554393`，19 s）。本条合并留痕提交后仍须重新通过 required CI，方可 squash 合入；合入只表示计划就绪，不表示 DeepSeek Harness 已实现、平台已完成或实验已运行。

## 2026-08-24：ISL RF 带宽正式双臂已完成并闭合 V2 重算

- PR #159 经 CI `658 passed, 1 skipped, 3 subtests passed`、文档治理 `0 errors, 0 warnings` 后 squash 合入；正式运行与分析器绑定 exact main `d3a116a69912dd214d89582a7b29c947f2357bfa`。canonical VM deployment receipt SHA=`dc1d7e0339ae3ee9c78025d863036f6d4d6ec261dea8b8a26f05f99233ae1291`；authorization 文件 SHA=`9442f778558d2467f2fc08c30c208a9ed5da38fae64e7f6f557c19332d8178ee`。
- `EXP-20260824-ISL-BANDWIDTH-PILOT-R02-b500-s7` 与 `...-b50-s7` 均由 canonical runner 严格串行启动、自然结束、exit 0、conservation 通过，外部 launch witness 与 governance receipt 均验证成功。governance receipt SHA 分别为 `92abea2a149dff76492249de75e15d4b64f7cd166a31619ea2255573fc5233ed`、`c2d7306cd3ef1892c06b14b486b85fc1760a5f4b315e689017bcb817a585c863`；VM 与本地精确 Python 3.11.15/锁定依赖环境的 `receipt verify` 均返回 `verified`。
- raw `receipt.json` 的 `research_eligible=false` 是合同要求，不是失败：本地 kernel 永不自授权；正式资格只由外部 governance v2 在 receipt、review/authorization、clean-main deployment、execution chain 和 nonce-bound witness 全部通过后给出 `research_eligible=true`。
- 持久化 V2 analysis status=`VERIFIED`、verified runs=`2`、claim status=`READY_FOR_INDEPENDENT_CLAIM_REVIEW`；`verify_persisted_analysis` 返回 `ok=true, errors=[]`。analysis manifest SHA=`bc69740ec1cb5f201a79cf4749908c64e7ff4f49196b0dde7ee412bb95a6eb23`，分析器绑定同一 main。
- 单 seed、同 trace 的工程结果：`isl_link_utilization_max` 为 b500 `0.005871255030063291`、b50 `0.020761875237929505`，预注册 b50−b500 差=`0.014890620207866214`。两臂 trace SHA 同为 `f6981c327f4c36e659d3f7b5ef66128f94a199d0203591401c88ed0e8ab22de4`；数据 fate 完全相同（1,299 offered、1,295 delivered、4 `NO_ROUTE`、0 in-system），1120 条有向 ISL 无饱和，MCS zero-rate holds 均为 0。
- 最大 link 两臂均为 `isl:222:242`，served bits 均为 `131000000`；sampled available-capacity bits 从 `22312095000` 降到 `6309642000`。全部 link 的 served bits、service-window 数和逐 link available time（均 30 s）一致，但 224/1120 link 的 available sample count 相差 1--2：b500 分布为 `{30:840,31:224,32:56}`，b50 为 `{30:952,31:168}`。独立冷审后重算否定了“drain 裁剪导致总时窗不同”的初始解释；差异更符合 bandwidth 改变 SNR/MCS threshold 分段数量。该差异不改变最大 link 的 30 个 sample，但再次说明干预不是纯容量乘数。
- 运行过程保留一个 fail-loud 基础设施证据：b50 首次 prepare 因原 `REMOTE_PYTHON=python3` 在环境激活前执行 predecessor verifier，找不到 TensorFlow 而在仿真启动前退出；随后只用临时、未入库的 remote config 指向 canonical Python 3.11.15，原 `remote.env` 与仓库代码均未修改，正式 nonce 重新通过全部 gate 后运行。
- 当前最强边界只是“在这个固定 scenario/seed 中，50 MHz 相对 500 MHz 提高了最大 horizon-aggregate 有向 ISL 利用率，但两臂仍远离饱和且包命运相同”。不能写成纯带宽因果乘数、拥塞阈值、算法优越性、Q0 结论或论文统计证据；50 MHz 不能据此冻结为 pressure arm。独立冷审 verdict=`PASS_WITH_LIMITS`；其“本地版本不匹配”open item 被精确 Python 3.11.15 双端 `verified` 证据驳回。ProjectPilot 修复后，Kimi 主审通道返回 `EVIDENCE_READY/PASS_WITH_LIMITS`；独立通道两次因非 typed-reference 的 `github.com` 证据被 fail-closed 拒收，operation `offload-operation:0e5d47be8640e25dae9756dda39fa545` 终态为 `FAILED`。本地已在 #160/#161 后 main 重验主审所指的结果归档缺口；未采纳其“先扩 seed/转 demand 轴”建议，仍先做仅改 bandwidth 的小型 onset bracket，再在相邻档补 seed。
- 合并留痕：结果归档 PR #160 的 GitHub Actions `pytest` 为 `SUCCESS`（run `32717549102`，job `97401900189`），squash 合入 main=`e9ccd87345596fd5727843a938143119a5f176d0`，远端结果分支已删除。
- 收尾留痕：PR #161 为仅补记 #160/#161 合并证据的 docs-only PR；以该 PR 最终 GitHub Actions `pytest` 绿和 squash merge receipt 为准，不改变实验、分析或 claim 内容。

## 2026-08-24：ISL RF 带宽敏感性候选包（精确包冷审通过，未授权）

- 分支 `codex/20260824-advisor-reports`，基线 `origin/main@e75b26c08c96b4507fc2c7d4682fb3e7893c8240`；本工作单元新增带宽敏感性 matrix 候选包、ISL-only horizon 聚合利用率分析指标及回归测试，并把 experiment-platform 测试纳入 CI；不修改 kernel、RF 公式、receipt 或历史实验。
- 新增 `EXP-20260824-ISL-BANDWIDTH-PILOT-R01`：两臂固定 280/14/25°、20 s 发包+10 s 排空、M-Lab measurement-proxy 多 OD、50M 配置标签+8 s 2× burst、seed 7、hop 路由和 `vis_k=17` propagation-cache 工程参考，只改 `links.rf_isl.bandwidth_hz=500/50 MHz`。该干预同时影响噪声、SNR、MCS 和服务时间，不写成纯容量乘数。
- 三轮精确冷审先后为 `REQUEST_CHANGES`：依次关闭会筛掉真实低带宽结果的硬 acceptance、delivery rate/全 stage 平均无法表征 ISL 压力、把 horizon link aggregate 误称 service-window utilization 三类问题。当前主指标 `isl_link_utilization_max` 只统计 `stage=isl`，含义是每条有向 ISL 在整段 horizon 聚合 `served_bits / sampled available_capacity_bits` 后跨 link 取最大值；无 ISL 数据 fail-loud。两轮 TDD 均保留 RED→GREEN 证据，最终 CI 同口径命令为 `634 passed, 1 skipped, 3 subtests passed`，文档治理 `0 errors, 0 warnings`。
- 第四轮独立冷审对精确工件为 `PASS`：source raw SHA=`37f305eb0ffc1cc0ac700d6febf8a1dcd5460ea38940c234c11ed52935f3fe47`，compiled request SHA=`add16c3410e9cca2aa04e5d67401a20b571954121575207d530fe08bdde42286`，run-manifest SHA=`c36ba8d2d9ef5ff09c81ce9b8ee59295ddbdc60324511257a778c59d7d3fd840`，analysis-request SHA=`4f62864ff4635f6b28a2765754f7ddf1f526120dd2223f1d3068110e1f7fcab7`。两臂 trace identity 同为 `effb467639ce8d0b73f60cde249eb6a792ec890b21d3e4e91ffee84143577309`，controlled signature 同为 `d6d9cac717206bfd5ef4d295c1addb322708fb7f03e9d953dc72ec3af725807f`；逐叶比较唯一差异是 ISL RF bandwidth。
- 精确提交冷启动复核为 `PASS_BOUND_TO_SHA`，绑定生产 commit `34f8149214a79204d9d3d2fa9e5fba5177b3ad4b`；PR [#158](https://github.com/fuguther/leo-direct-sim/pull/158)。PR 证据包含审阅边界、测试计数和 2-cell/7-artifact matrix 复验结果。
- 边界：该 PASS 只覆盖 compiled/analysis contract。本包仍为 `COMPILED_REVIEW_REQUIRED`，没有 finalization、authorization、latest-main VM deployment 或 analyzer-SHA 分析工件绑定，尚未运行。正式分析前须把 analyzer 的精确 Git commit 纳入 finalization/证据链；未关闭前不得手工启动或作为论文结果。

## 2026-08-22：E0 vis17 同 trace 诊断登记（当前工作单元）

- docs-only 分支 `codex/20260822-e0-vis17-result`，基线 `main@34c68b4bdc5e5d91a3b5e5ccdf2c3e339473db18`；不改 kernel、trace schema、nested trace 或历史目录。
- 已核证 10M 同 trace 对照：trace SHA=`e2b469b984a7fc677f4ae8a61621f7e1e9c93ff3b3ade097461a68f365a2d23`；`resolved_config` 唯一差异为 `/config/control_plane/vis_k` `12→17`。vis12/vis17 offered/admitted/delivered/in-system=`250/240/192/58`、`250/240/233/17`；total delivery `.768→.932`，conditional delivery `.8→.9708333`；holding-at-stop `48→7`，uplink-at-stop `10→10`；holding area `930416301.5258671→124326178.47600535 bit*s`，uplink area完全相同；vis17 ISL max util=`0.0011653`。
- 两次均 `natural_end=true`、`conservation_ok=true`、VM `receipt verify` 通过；vis17 wall=`649.276 s`。该结果是单 seed 同 trace 诊断证据，支持 vis12 混淆 holding/in-system 的判断，但不能宣称普遍因果。vis17 `research_eligible=false` 且无 external launch witness，不是正式论文结果。
- 25M/50M vis17 正在 VM 并行执行，结果未返回，不填入未核证数字；三档完成后重标 E0，再决定是否进入 long-haul/容量压力轴，不能因旧 vis12 低交付率直接加星。
- 历史 f328e85 `E0DRAIN-20260822-{10,25,50}M` 继续标记 `diagnostic_info_truncated`，不用于拥塞分档。此前 profile/diameter contract 的 RED→GREEN 和全量 `655 passed, 2 skipped, 3 subtests passed` 证据保留在下方历史记录。

## 2026-08-22：280/14/25° E0 工程基线与负载重标定（本分支）

- 分支 `codex/20260822-e0-recalibration`，基线 `main@29e41c84dfe7353f484e36596f00f49508d0bdb2`；profile `mlab_multiod_burst_t0_queue_280x14_e25.yaml` 登记为 **E0 工程基线**，不是 paper-ready 全局冻结。
- exact-main VM deployment receipt：`11688f2f2fae23c250b535aa439057c01eebd8b386f132c00ba654c4003b31a8`；run `SMOKE-20260822-COVERAGE-280X14-E25-29e41c8`，trace `f6981c327f4c36e659d3f7b5ef66128f94a199d0203591401c88ed0e8ab22de4`。
- VM FACT：1299 offered、1233 admitted、978 delivered、16 holding overflow、1 no-route、304 in-system；access admission `0.9491916859`、network delivery by horizon `0.7931873479`；natural end、conservation、VM receipt verified；wall/user/sys `424.1882/429.4386/2.0247 s`、max RSS `1869052 KiB`、events `9618761`。
- 新增 10 Mbps 与 25 Mbps 工程 E0 profiles；E0-LOAD-CALIBRATION arms 改为 10/25/50，状态 `in_progress`。50 Mbps 只是较高负载/扫描上界候选，不能预标 high；low/medium/high 等三档结果齐全后再判定。旧 50/100/200 标为 `historical_only`。
- 该条历史计划已由本文件顶部的 vis17 诊断登记 supersede；不创建正式授权矩阵，不改变 kernel/routing/receipt/governance/learning。

## 2026-08-22：emission window 与 drain-aware E0 重标定（本分支）

- 证据边界：此前 20 s 10/25/50 Mbps 的 `scenario.duration_s` 同时承担发包窗和停止窗，标记为 `diagnostic_truncated_horizon`，不能用于负载分类。10 Mbps：250 offered、240 admitted、192 delivered、58 in-system，wall/user/sys `401.3503/405.0936/2.3318 s`、max RSS `1775096 KiB`；25 Mbps：685/684/527/156，wall/user/sys `414.9082/418.2221/2.7069 s`、max RSS `1836412 KiB`；均 natural end、conservation、receipt verified。
- 新合同：`demand.emission_end_s: null` 向后兼容为 `scenario.duration_s`；显式值必须 finite、>0、≤ simulation horizon。trace 仅生成 `[0, emission_end_s]` 的新包，仍按 simulation horizon 验证/运行；manifest/provenance 记录 `simulation_horizon_s`、`emission_end_s`、`drain_s`。
- 新 E0 profiles 固定 `emission_end_s=20`、`scenario.duration_s=30`，下一步 VM 只跑同一 trace 的 10/25/50 三个 drain-aware cell。10/25/50 标签待完整排空窗口结果后判定。

## 2026-08-22：access boundary 冷审修复（pending）

- 分支：`codex/20260822-access-boundary`，基线 `main@339a1f4`；PR：pending。
- 提交：`d34ae0a`（配置/有限 queue/kernel）、`5bcab85`（satellite ingress/raw metrics v2/analysis）、`0e55cac`（coverage/文档）、`befb39f`（profile diff、coverage 预算、E0 状态、v1 receipt 回归）及本轮独立 fix（receipt v4 合同、入网交叉约束、历史文档边界、冷审反例）。
- RED→GREEN：第一轮冷审对精确 `befb39f` 为 `REQUEST_CHANGES`；本轮新增的无 uplink arrival、v4/v1 downgrade、ACCESS_REJECTED 伪 ingress 反例先失败后通过，旧 v3 v1 fixture 和合法 v4 v2 flow 仍通过。
- 当前验证事实：receipt/metrics/access targeted 与全量均通过；全量 `622 passed, 2 skipped, 3 subtests passed`；同轨迹 A/B reject=`offered 1/admitted 0/delivered 0/pending 0/rejected 1`，queue=`offered 1/admitted 0/delivered 0/pending 1/rejected 0`。
- 风险：queue 改变访问语义，旧 20 s 50/100/200 结果仅保留历史证据，不能 paper-ready；需 coverage/horizon audit、VM 小样、重新 E0/训练和独立冷启动复核。coverage audit 只报告几何证据，不决定加星或容量充分性。
- 冷审状态：第一轮对 `befb39f` 为 `REQUEST_CHANGES`；修复 receipt v4 合同、事件/终局交叉约束及 historical v1 delivered compatibility 后，第二轮对精确 `80bc237d67bb9df4fa516e47c81b6013f3b04956` 为 `PASS`。独立复核 targeted `41 passed`、全量 `622 passed, 2 skipped, 3 subtests passed`，两个伪造/降级反例均被拒绝。
- 本地真实流量诊断（非 VM、非论文证据）：在 `80bc237` 用新增 queue profile 消费既有 M-Lab trace `f6981c327f4c36e659d3f7b5ef66128f94a199d0203591401c88ed0e8ab22de4`，20 s、1,299 包自然结束且 receipt verified、守恒通过；762 包入网、656 包送达、39 `ACCESS_QUEUE_OVERFLOW`、604 `IN_SYSTEM_AT_STOP`，因此 `access_admission_rate=0.5866050808`、`network_delivery_rate_by_horizon=0.8608923885`。该结果只证明阶段拆分和运行链可执行，不关闭 coverage/horizon 或 E0 门禁。
- 几何诊断（非容量结论）：同 55 端点、6000 s/5 s 扫描下，140 星/7 面/30° 全端点最终均可见，但可见比例中位数约 0.476、最大无覆盖间隔约 5710 s；粗粒度候选扫描显示增加轨道面比只向原 7 面加星更有效。正式星座/仰角选择仍需 VM 成本与容量联合校准。PR：pending；VM 尚未执行。

### 合并与 VM 工程 smoke

- PR #150 已由 CI `pytest` 绿后自动 squash 合入；main=`63a10990f63f5529c14594ce47bafcda64022f10`。部署到 canonical VM 后，deployment receipt SHA=`8f31142bbf6a80b764fe66cd27e36b6e805ccad8de48b585a8436dae66b3f7a9`，远端回执确认 source clean、branch=main。
- VM 工程 smoke（非 formal、非论文证据）：`SMOKE-20260822-ACCESS-QUEUE-63a1099` 使用 M-Lab trace `f6981c327f4c36e659d3f7b5ef66128f94a199d0203591401c88ed0e8ab22de4`，20 s、1,299 offered、762 admitted、656 delivered、39 `ACCESS_QUEUE_OVERFLOW`、604 `IN_SYSTEM_AT_STOP`；natural end、conservation true、VM receipt verified，receipt v4/metrics v2。
- 阶段指标：`access_admission_rate=0.5866050808314087`，`network_delivery_rate_by_horizon=0.8608923884514436`。由终局与入网事件交叉可得：498 包仍在入网前等待、106 包已入网但在停止时仍在系统。总交付率低不能再直接归因于网络拥塞。
- VM 资源：wall `127.7769 s`、user `133.9099 s`、sys `1.0053 s`、max RSS `869,920 KiB`（约 850 MiB）。在 24 vCPU/64 GiB 下，非学习 cell 仍按 1 vCPU/job、先 10--12 jobs 并行；学习 cell 另做 profile，不能沿用该内存数字。
- 结果已拉回本地 ignored `CODE/Results/SMOKE-20260822-ACCESS-QUEUE-63a1099/`。VM 同环境复核通过；Mac 本地严格 verifier 因 Python/NumPy/SimPy/PyYAML 版本不同而按设计拒绝，不能把该拒绝误写成 artifact 损坏。

## 2026-08-20：D1/D2 合入与 VM 工程 smoke

- PR #55（D1 动态链路速率）与 PR #56（D2 动态拓扑/holding）均已合入 main；当前 main
  为 `b037b6182bf16c9d406cabf4fa5dc8da8b441a2a`，PR #56 CI `pytest` SUCCESS。
- D2 合并前本地证据：`pytest -q` = `555 passed, 1 skipped, 3 subtests passed`；
  `git diff --check` 通过。VM 同一代码环境 `CODE/leo_sim/tests` = `494 passed, 1 skipped`；
  唯一 skip 是 macOS `/var` 别名反例在 Linux VM 不存在。
- 部署：canonical VM `/data/论文/leo-direct-sim`，source tree SHA
  `422b2c747d0a224daa3d786eff68cf8ff6a0fe1baf9aa6d69d16e4cbbbbfb175`，deployment receipt
  SHA `4866768f757eb1df3c3ac9f4b9539ed8b6dde728b668177472232ad869137aab`。
- 非正式工程 smoke：`smoke.yaml` 在 VM 自然结束，`DELIVERED=1`、
  `conservation_ok=true`、`IN_SYSTEM_AT_STOP=0`，`receipt verify`=`verified`。
- 边界：仓库当前没有 R02 的合法 `finalization.json`/`authorization.json`，因此没有伪造正式授权；
  本 smoke 证明“已部署版本可运行”，不证明 V2 正式分析链、真实流量诊断或论文结论已就绪。

## 2026-08-20：精确当前 main 部署复核

- 文档 PR #68 合入后的当前 main 为 `66be0adedbf96bcdad722ca6720851904b256129`；该 SHA
  已重新部署到 canonical VM。source tree SHA=`6291acba9c14d703c7758e7799fb51aae4a6a5eba0f84b16716cb846d1ba3345`，
  deployment receipt SHA=`24b0a4783a22960cc703faff0f6e46b4a7e077af7c9c86d3826423ed7878b06e`。
- 同一 SHA 的 `CODE/Results/_vm_smoke_66be0ad` 工程 smoke：自然结束、`DELIVERED=1`、
  `conservation_ok=true`、`IN_SYSTEM_AT_STOP=0`，`receipt verify`=`verified`。

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
## 记录规则

- 任务级证据放 PR；本文件只在合并改变当前平台状态、风险或下一步时更新。
- 设计解释写入对应 CURRENT/SUPPORTING 文档，NOTES 只留链接。
- 当前周期结束后原样归档；不得通过压缩删除失败、REQUEST_CHANGES 或未验证记录。
- 实时问题状态只在 `ANALYSIS/FINDINGS-REGISTRY.md` 更新。

## 2026-08-21：拥塞/利用率最小观测层

- 分支：`codex/20260820-congestion-observability`；代码提交 `e68f265`。
- Kernel 记录每个数据包的 emission、queue enter、service start、propagation start/arrival、
  delivery；每个真实服务窗记录 link ID、rate、occupied interval、capacity bits、served bits
  与 outcome。holding residence 由相邻 queue admission 重算，未凭空补 horizon exit。
- `CODE/leo_sim/metrics.py` 从原始事件重算每包 queue/holding、tx、prop、E2E 以及逐链路服务窗
  utilization；`receipt.py` 把原始事件和重算结果写入/校验 `ledgers.json`，ledger SHA 继续绑定 receipt。
- 先写反例再实现：纯 metrics 的 queue/tx/prop/utilization 与 orphan queue ID 拒绝测试；真实单星
  端到端事件测试。验证：`python3 -m pytest -q` = **563 passed, 1 skipped, 3 subtests passed**。
- 边界：当前分母是“记录到的传输服务窗容量”，不是链路在几何上可用的全部时间容量；真实流量
  provenance、多 OD/突发和 VM 部署验证仍是下一包，不得把该分支直接称为论文就绪。

## 2026-08-20：奖励目标第一包

- 分支：`codex/20260820-reward-objective`；提交 `4163226`。
- 将训练侧 ISL 转发奖励改为“实测 M1 队列奖励 + 非正逐跳成本”，配置校验强制
  `forward_step_penalty <= -reward_w1`；原始 `queue_reward()` 保留作诊断对照，并把该参数
  写入 requested receipt 字段。
- 先写反例测试再实现：零等待转发奖励为 0，正等待严格为负，非法 `-19 > -20` 配置拒绝。
- 验证：`python3 -m pytest -q` = **557 passed, 1 skipped, 3 subtests passed**；
  `git diff --check` 通过。
- 边界：只关闭已知“额外跳数刷分”风险；Q0 物理字典序目标、拥塞观测、V2 分析闭环和 VM
  学习 smoke 仍未完成。

## 2026-08-20：D1 第 8 轮返工与 main 合并

- 第 8 轮 exact-SHA 审阅对 `0e1f2a8` 返回 `REQUEST_CHANGES`：constant 配置虽已
  忽略 RF/MCS 数值，Kernel 初始化仍无条件派生 MCS 门限，导致配置解析成功后启动崩溃。
- `a5dfb33` 扩充回归到真实 `Kernel` 构造；constant 分支完全跳过 RFParams/MCS range
  派生，MCS 分支保持原校验/派生路径。上一轮同时关闭 completion/retirement 竞态、
  精确服务时长、非 tick 恢复及 capacity 路由同源动态速率。
- 合并最新 main 时同时保留 R1-A2 的 `cache_hops` 信息边界与 D1 的
  `rate_from_propagation` 动态容量；两个回归组均作为合并验收门。

## 2026-08-20：文档真相源收敛

- PR #58 已 squash 合并为 `e15c457d71db42e279d3599ecbbe5969608e8261`；主题为
  实验就绪/Q0/平台能力/实验计划真相源收敛。GitHub CI `pytest` SUCCESS（15 s），
  本地 `411 passed`，diff 无删除或移动路径。
- 隔离分支：`codex/20260820-doc-consolidation`，基线 main
  `4c8d38ff38031ae134ae6738b3ebaa405e0f06f7`。
- 开工基线：`python3 -m pytest CODE/leo_sim/tests CODE/tests -q` =
  `411 passed`。
- 新 CURRENT 文档：
  - `ANALYSIS/CURRENT-EXPERIMENT-READINESS.md`：两个平台目标、门禁和带前提工期；
  - `ANALYSIS/PLATFORM-CAPABILITY-LEDGER.md`：当前能力差距与优先级；
  - `ANALYSIS/Q0-INFORMATION-ABLATION-PROTOCOL.md`：从最优向下裁剪为主、
    从现实向上增加为辅；
  - `ANALYSIS/EXPERIMENT-PROGRAM.md` 与
    `EXPERIMENTS/experiment-program.yaml`：实验总计划与机器清单。
- 已停止把不存在的 `ANALYSIS/paired_analysis.py` 写成可运行入口；正式分析链
  登记为 R7-F1 blocking。clean main 实测：experiment_platform+work =
  `21 passed, 5 failed, 3 subtests passed`；focused identity = `1 failed`，均为缺失绑定输入。
- FINDINGS 补入 R1-A1 奖励正循环与 R1-A2 mask 信息旁路；未把 #43 的局部奖励
  修复冒充为关闭 R1-A1。

## 2026-08-20：当前外部状态核验

- GitHub main = `4c8d38f`；#57 已合入。
- D1 PR #55：head `408d368c...`，CLEAN，CI pytest SUCCESS，未合入 main。
- D2 PR #56：head `6be16cd2...`，CLEAN，CI pytest SUCCESS，未合入 main。
- VM deployment receipt：commit `a2a588d9...`、clean、
  `2026-08-20T01:51:43+08:00`；落后 main 且不含 D1/D2。
- Q0 replay/tiny 是未合入候选并有 REQUEST_CHANGES；Q0-F 尚未完成。
- 上述状态是 2026-08-20 核验快照，后续变化必须更新 CURRENT 文档，不能只追加 NOTES。

## 2026-08-20：R1-A2 信息边界修复合入

- 隔离分支 `codex/20260820-r1-mask-information` 复现为 FACT：在学习观测不变时，
  `obs_hops` 外的两跳目的地广告会让旧代码开启 forward 动作。
- 修复让学习选路的目的地广告、远端传播与队列指标和 observation 共用 cache-hop
  边界；C1 同时约束当前邻居来源与实际一跳传播。
- #62 head `614fd23` 独立冷启动复核 APPROVE；定向 `41 passed`、仿真内核全量
  `410 passed`、GitHub pytest SUCCESS；squash 合入 main `758b606`，R1-A2 已 fixed。

## 2026-08-20：R7 generic 证据链部分恢复

- PR #64 head `4e6d665` 经独立冷启动复核 APPROVE，Hosted CI pytest SUCCESS；
  squash 合入 main `12bf306`。
- main fresh 验证：当前 CI 范围 `425 passed`；无参数全量
  `470 passed, 1 skipped, 3 subtests passed`。
- 恢复范围仅为 generic `experiment-run-manifest/v2` 的持久化 paired analysis、
  claim schema、严格重验和 CI bridge；`leo_sim_v2` 使用不同合同及结果布局，
  因此 R7-F1 仍为 `open`（generic 部分恢复），不得据此授权正式 V2 实验。
- V2 矩阵 Stage 1 候选 `4664a223` 已收到 REQUEST_CHANGES：真实 launch 授权路径、
  acceptance、配对完整性、checkpoint 血缘、控制变量和 symlink containment 均需返工。

## 2026-08-20：研究主线与实际顺序重排

- 用户锁定主线为“拥塞控制与链路利用率”，执行方法为真实流量优先、先实验诊断、
  再理论推导、最后提出新方案；旧 EXP1→EXP3 不再是默认主线。
- 本轮更新 `ANALYSIS/EXPERIMENT-PROGRAM.md`、
  `EXPERIMENTS/experiment-program.yaml`、`ANALYSIS/CURRENT-EXPERIMENT-READINESS.md`
  和 `ANALYSIS/PLATFORM-CAPABILITY-LEDGER.md`，把全部指定能力按最早真实依赖分门：
  D1/D2/V2 证据链为平台门；真实流量、多 OD/突发、逐向利用率、每包三段时延为诊断门；
  Q0-I/F、逐候选物理特征、逐字段 age 为理论门；replay/optimizer/target/RNG 恢复为长训门。
- exact main `5b3ec5f...` 的 Luna 只读审计确认：CSV 多 OD、M-Lab/人口代理、burst、
  GAT/MPNN 骨架已存在；利用率分母、每包三段时延、逐字段 age、完整续训、Q0-I/F
  与 V2 分析闭环仍缺。网页 GPT 四通道首轮 1 个通过、3 个运行/证据门失败；重试又回收一份
  同方向的计划审阅，方法调研仍未形成合格信封。按用户最新指令已取消继续重试；失败通道不计作三方通过。
- 本分支 fresh 验证：CI 范围 `425 passed`；无参数全量
  `470 passed, 1 skipped, 3 subtests passed`；YAML 解析、实验 ID 唯一性和依赖引用检查通过，
  `git diff --check` 通过。

## 2026-08-20：V2 矩阵编译与授权 Stage 1 收口

- PR #67 候选新增 V2 多 cell 矩阵 request/manifest/analysis 编译、完整 cohort 授权、
  配对/acceptance/control signature/checkpoint/path 身份门；不包含 Stage 2 的
  artifact→metrics→paired analysis→claim。
- 两轮独立冷审均先返回 `REQUEST_CHANGES` 并复造真实缺口；最终 bearing SHA
  `290e31da543b3ab366a9a7e83b2b9d6b18a9173c` 获 `APPROVE`。关闭项包括
  runtime config path、acceptance、pairing 完整性、checkpoint 内容身份、精确 intervention leaf、
  symlink/alias containment、compile-report 重绑定及空 override 映射。
- 最终本地证据：matrix `20 passed`；CI 范围 `445 passed`；无参数全量
  `490 passed, 1 skipped, 3 subtests passed`；`git diff --check` 通过。

## 下一步

### 2026-08-22：280/14/25° coverage provisional candidate（本分支）

- 分支 `codex/20260822-coverage-candidate`，基线 `main@392d972`；新增候选 profile 与 resolved-diff 回归。
- 固定 trace `f6981c327f4c36e659d3f7b5ef66128f94a199d0203591401c88ed0e8ab22de4`：20 s/1 s、6000 s/20 s 均 55/55 达标；长窗 min visible fraction `0.6345514950`、median `0.9734219269`、max gap `1760 s`。
- 可见样本最大 slant `1213.2078115 km`；min positive MCS uplink/downlink `2532845000/1317618000 bps`，均未出现 0 速率；positive range `12067.9044812/4482.1358470 km`。
- 本地真实 run 已自然结束、守恒通过：1299 offered、978 delivered、16 holding overflow、1 no-route、304 in-system；wall/user/sys `133.93/132.47/1.06 s`。macOS max RSS 因 `/usr/bin/time -l` 权限限制未核验。
- 结论边界：仅 provisional VM candidate；不是 capacity proof、不是 paper-ready；VM trial pending，须同 trace 资源/阶段指标后冻结并重跑 E0。旧 140/7/30° VM smoke 已完成但覆盖不足。

1. 关闭 R7-F1 的 V2 矩阵、artifact 指标重算、paired analysis 与 claim gate；
   generic #64 只作为可复用基础，不代表 V2 完成。
2. 获得所需语义/冲突授权后合入 D1/D2，关闭 R1-A1，并更新 CURRENT 中的精确 main/VM 状态。
3. 补真实流量 provenance、多 OD/突发验收、逐向利用率分子/分母和每包 queue/tx/prop 事件。
4. 冻结同一 main SHA 并部署 VM，按 E0-REAL→PILOT-BASELINES→DIAG-CONGESTION 做实验诊断。
5. 再完成 Q0-I/F、逐候选物理特征、逐字段 age；基于诊断提出方案，长训前完成 replay 完整恢复。
6. 平台关键门禁不再被文档/Git 清理抢占；回收 worktree时继续保护 dirty、orphan 与 detached 项。

## 2026-08-21：V2 结果到成对分析适配器

- 分支：`codex/20260821-v2-analysis-chain`；基线 main `2f577a5`。
- 新增 `CODE/experiment_platform/v2_analysis.py`：对 V2 矩阵的授权 cohort 逐 run 校验
  `receipt.json`、`ledgers.json`、`formal_run.json`、`governance_receipt.json`、
  `resolved_config.json`、`manifest.json`；从 receipt/原始事件重算 delivery、时延和服务窗利用率，
  按 preregistered pairing 做差值，并写出 `analysis-manifest.json`、`summary.json`、`report.md`、
  `claim-gate.json`。
- `CODE/leo_sim/matrix.py` 生成的 RUNBOOK 现在包含 V2 分析命令；该命令只在所有授权 cell
  自然结束并产出结果后执行，不能跳过授权或把 fixture 变成论文结论。
- 验证：V2 定向 `22 passed`；全量 `565 passed, 1 skipped, 3 subtests passed`；`git diff --check` 通过。
- 边界：这是 V2 分析入口和本地真实 receipt fixture，不是 VM 授权 cohort 证据；R7-F1 继续保持
  `open`，下一步部署同一 SHA，跑真实流量/E0 与持久化分析闭环。

## 2026-08-21：trace provenance 与 offered-load 合同

- 分支：`codex/20260821-trace-provenance`；代码提交 `3878862`，基线 main `91a6604`。
- 每个 trace manifest 新增 `provenance_contract`：源类型/路径/SHA、时间/坐标/bits 单位、CSV
  坐标到 aggregate grid 的映射规则、目标 offered Mbps、实际 trace offered Mbps、包/bit 账本。
  `receipt.py` 会按 resolved config 和 manifest 账本重验，缺字段或篡改时 fail closed。
- CSV 输入保留 source packet ID 并绑定输入文件 SHA；M-Lab/人口模式继续明确标记为代理，不得写成
  校准用户需求。
- 验证：trace/receipt/acceptance 定向 `119 passed`；全量 `565 passed, 1 skipped, 3 subtests passed`；
  `git diff --check` 通过。
- 边界：还没有当前 SHA 的 VM receipt，也没有整段几何可用时间分母；下一步合入、部署并跑真实 CSV
  多 OD/突发与 E0 smoke。

## 2026-08-21：main 499d2e6 VM 工程 smoke

- 从 clean full clone 固定 `499d2e6fb6b9aea0883aa57781f55b8655fe7638` 部署到 canonical VM。
- deployment receipt：`ba705741be0cc700acd392106651fe01faeba93cff0333e3d8543bd8421a00df`；
  source tree SHA `718a5268f736f77a9f4b749e5edc2ee2551041710cc07b8ee57eac247161d09d`。
- 非正式工程 smoke：`CODE/Results/_codex_vm_smoke_499d2e6`；natural end、`DELIVERED=1`、
  `conservation_ok=true`、`IN_SYSTEM_AT_STOP=0`；receipt verify=`verified`；36 packet events、
  4 service windows，trace provenance contract 含 source/units/offered-load。
- 边界：这不是 formal authorization、不是真实 CSV/E0、不是论文结果；下一步补正式授权
  cohort 与真实多 OD/突发 load calibration。

## 2026-08-21：burst/diurnal provenance 补齐

- VM burst plumbing smoke 暴露一个真实缺口：旧 `provenance_contract` 只记录 mode 和 realized load，
  没有把 burst start/duration/multiplier（或 diurnal amplitude/phase）写入结果，因此无法仅凭 trace
  artifact 复核负载变换。
- 分支：`codex/20260821-burst-provenance`；代码提交 `eba3c97`。新增并校验
  `traffic_transform`，burst/diurnal 参数与 resolved config 不一致时 receipt fail closed。
- 验证：trace/receipt 定向 `119 passed`；全量 `565 passed, 1 skipped, 3 subtests passed`。
- 之前 `499d2e6` 的 burst smoke 仍只算工程 plumbing，不能当已关闭证据；待本修复合入并重新部署后重跑。

## 2026-08-21：0c378a5 修复版 VM burst 重验

- 修复版 main `0c378a5c7538536d4ea65f4a3ac1e2b7c542ade9` 已部署；deployment receipt
  `7a3c06a61b851b2ae282f83749931bb5f6ee7ab7abd3a63ca0492201669835f7`；source tree SHA
  `abf0c04963564ad4bd9e9c61e5de0971c669ed85fafa71146f21573562c38ccd`。
- `CODE/Results/_codex_vm_burst_smoke_0c378a5`：natural end、85/85 delivered、守恒通过、
  receipt verify=`verified`；`traffic_transform.burst={start_s:10,duration_s:20,multiplier:3}`，
  offered-load 账本 `85,000,000 bits / 60 s` 可重算。
- 同一部署还完成 MCS smoke：receipt `effective.mcs=true`，服务窗速率出现
  `283.9025 Mbps / 2.103214 Gbps / 2.9504275 Gbps`；结果仍为工程证据，不是正式论文样本。

## 2026-08-21：最终文档版 main 部署

- 文档合并后的 clean main `42ff519d6caed3c9666f55e3390989c6943d1093` 已再次部署，确保后续
  formal run 使用当前主线 SHA；deployment receipt `ab047f09ec66088d7ab6af93bf8fdc6e989d6d087b1d0651a47383423888f6f9`，
  source tree SHA `a1e6a5730dd8e7ed51881d89166c79073c6f5d72bca35d57ed4a4ccac8c274de`。
- 该次仅为版本一致性部署；`0c378a5` 同代码已完成的 MCS/burst smoke 证据仍适用于代码行为，
  但正式授权 cohort/E0 仍未运行。

## 2026-08-21：current main `ac0d019` VM deployment and smoke

- 通过 guarded `push-remote.sh` 部署 clean main `ac0d01965d91956b5d80df36dce5b351c1bdccc6`；
  deployment receipt SHA=`c43e711442195cc8f31025167784773562e3a71ddb8c3cca65f25e1b787aa66b`，
  source tree SHA=`bf9a90090e2d2ac82701483c08fcaebe1976a083a71315405fbb0f5ef683b98d`。
- VM 固定环境的 10 s M-Lab+burst smoke：config SHA=`38ee6b760b88829ee2751510755cb0fa1ded8c4c5cca0430d6527aeabbcbf110`、
  trace SHA=`21812f86b7883a47560bd15f9d7d2958a503fc71a7bc27d52dd3cfd252caea4d`、
  code SHA=`5d2ddec3fecfa0a8b83174eaf30aa1da8bf4e9a5d766ddfa6a387e4b8cc6a193`；18/18 delivered，
  natural end，守恒通过，receipt verify=`verified`。shell timer：real 6.41 s、user 11.33 s、sys 0.55 s。
- 同一 VM SHA 的 140 星 MCS/M-Lab 60 s smoke 也自然结束并 receipt verified：461 offered，
  440 delivered、20 ACCESS_REJECTED、1 IN_SYSTEM_AT_STOP、守恒通过；它仍是工程证据，不是授权论文样本。
- 边界：当前 `ac0d019` 已完成同 SHA VM 非学习验证；学习训练/评估 VM、formal authorization、
  available-capacity 利用率分母和正式 E0/PILOT 仍未完成。

## 2026-08-21：E0-REAL 50 Mbps 首次 M-Lab/MCS 长窗 smoke（候选）

- 分支：`codex/20260821-e0-calibration`，基线 main `743d05c`；新增
  `CODE/leo_sim/profiles/mlab_e0_calibration.yaml`（140 星、MCS、动态拓扑重算 1 s、
  M-Lab measurement-proxy 三 OD cycle、20--40 s burst）。
- 运行：60 s 本地自然结束，461 offered packets / 3.688 Gbit；440 delivered、20
  `ACCESS_REJECTED`、1 `IN_SYSTEM_AT_STOP`，守恒通过；修复后 `receipt verify=verified`。
  同一 trace SHA=`dfe47500712ddc353c4ba5b9564d943be7f10018d07e36bdeb52b4d35d166910`。
- 资源：macOS `/usr/bin/time` 记录 wall `78.66 s`、user `78.28 s`、sys `0.36 s`，约
  99.5% CPU busy；该测量没有可用 max-RSS 字段，不能伪造内存结论。
- 真实缺陷：receipt 重算没有把 `IN_SYSTEM_AT_STOP` 等合法未到达 fate 传给 metrics，导致
  截止时仍在传播中的包被错误报告为 `unmatched propagation starts`。本分支修复并新增回归，
  全量 `CODE/leo_sim/tests CODE/tests` = **524 passed**。
- 研究边界：当前 utilization 分母仍是“已记录服务窗容量”，本次六条 GSL 窗几乎均为 1.0，
  不能冒充几何可用容量利用率；E0 只能作为负载/守恒/资源工程诊断，DIAG-CONGESTION 前仍
  必须补 available-capacity 分母和 VM 同 SHA 验证。

## 2026-08-21：M-Lab 真实测量代理与高负载 VM smoke

- 来源核对：旧工作区任务记录确认 `CODE/data/traffic/mlab_2026-05-27.csv` 来自公开
  M-Lab NDT7 GCS 测量归档，按客户端/服务端城市与 UTC 小时聚合；文件 SHA256
  `f15cf8b9845c195046a4566d31ab9eb0137e16270ea98ee6a06b871a6f578437`。它是测量代理，
  不是用户包级真实流量，当前 V2 `mlab` 模式只使用空间 OD 权重。
- 修复：`6936d10` 使指标层只对账本明确标记为仍在系统/途中丢失/截止时未到达的包放行未匹配
  propagation start；真正孤立事件仍 fail closed。新增回归测试。
- 验证：本地全量 `566 passed, 1 skipped, 3 subtests passed`；该干净 commit 已部署 VM，
  deployment receipt SHA `38782c8a5a0fc11ef7751f421aae55219b8b1be1badeffe3552c936b7c8bbe66`。
- VM 工程 smoke（30 s、24 星、Amagasaki→Tokyo、M-Lab proxy）：50 Mbps 为 1,533 包、
  456 delivered、1 in-system、自然结束且 metrics=`ok`；100 Mbps 为 2,990 包、719 delivered、
  88 in-system、自然结束且 metrics=`ok`；两次均守恒，未再出现 `unmatched propagation starts`。
- 边界：这是部署一致性与负载暴露 smoke，不是 formal authorization 或论文样本；M-Lab 的
  `hour_utc` 尚未进入当前 V2 mlab 变换，正式 E0/PILOT 仍需走编译→审阅→授权→回执链。

## 2026-08-21：T0 M-Lab measurement-proxy OD + burst 闭环（候选）

- 分支：`codex/20260821-traffic-t0`，基线 main `51f832c`；本条记录对应当前未合入候选，
  不改变 main/VM 状态。
- `mlab` trace 编译现在 fail-closed 校验必需字段、小时范围、样本数和吞吐量，并在 manifest
  写入源 SHA、`row_count=44929`、`od_pair_count=4825`、完整 `hour_utc=0..23` 覆盖；显式
  burst 会记录 start/duration/multiplier。新增 schema、解释文档和
  `CODE/leo_sim/profiles/mlab_measured_od_burst.yaml`。
- 验证：`CODE/leo_sim/tests/test_config.py CODE/leo_sim/tests/test_trace.py` 为 **22 passed**；
  相关 receipt 回归 `205 passed`；profile validate 成功；本地 `run` 10 s 自然结束，
  18/18 delivered、0 in-system、`conservation_ok=true`，`receipt verify=verified`，
  trace SHA=`21812f86b7883a47560bd15f9d7d2958a503fc71a7bc27d52dd3cfd252caea4d`。
- 边界：这是可复现的 M-Lab **measurement_proxy**，不是原始用户流量或校准运营负载；尚未部署
  当前分支到 VM，也未完成 E0 负载标定、学习训练/检查点恢复和正式授权 cohort。

## 2026-08-21：拓扑重算间隔工程校准

- 分支：`codex/20260821-topology-cadence-docs`；基于已部署代码 `ac0d019` 的文档证据补录，未修改仿真内核。
- 本地固定同一 trace SHA=`dfe47500712ddc353c4ba5b9564d943be7f10018d07e36bdeb52b4d35d166910`，140 星、60 s、MCS、M-Lab 三 OD + burst，扫描 `0.5/1/2/5 s`。四档均自然结束、守恒通过、receipt 无错误，461 offered、440 delivered、20 `ACCESS_REJECTED`、1 `IN_SYSTEM_AT_STOP`；拓扑重算次数为 119/59/29/11，墙钟约 118.9/79.9/60.5/48.9 s。
- VM 固定同一部署代码 `5d2ddec3fecfa0a8b83174eaf30aa1da8bf4e9a5d766ddfa6a387e4b8cc6a193`，66 星、10 s 短 smoke 扫描四档；均自然结束、18/18 delivered、守恒通过、receipt verified。该 VM 扫描只验证部署合同和 cadence plumbing，不替代长窗 D2 语义证明。
- 暂定决策：E0 先用 1 s；2 s 作为成本敏感性对照，5 s 作为慢更新负对照。需在低/中/高负载、长窗上比较交付、积压、利用率和切换指标后再冻结。连续进程的 `ru_maxrss` 未作为逐 run 内存证据，独立资源剖析仍未完成。

## 2026-08-21：E0 多 OD + burst 负载标定

- 分支：`codex/20260821-e0-load-calibration`；代码未修改，使用当前已部署代码 SHA=`5d2ddec3fecfa0a8b83174eaf30aa1da8bf4e9a5d766ddfa6a387e4b8cc6a193`、140 星、60 s、MCS、拓扑 cadence 1 s、M-Lab 三 OD、20--40 s burst。
- 本地结果（同一运行合同、各自 trace/config SHA）：50 Mbps = 461 offered / 440 delivered / 20 `ACCESS_REJECTED` / 1 `IN_SYSTEM_AT_STOP`，config `e27ed88d83e8bb39f1b858cfe4e725d4291f2a9a4fe5d9d14d10973918c0a0e2`，trace `dfe47500712ddc353c4ba5b9564d943be7f10018d07e36bdeb52b4d35d166910`；100 Mbps = 944 / 877 / 60 / 7 `HOLDING_QUEUE_OVERFLOW`，config `a7acd58e141152bd00a347f737bacaab03653abe5db730c9f6b31684d058c953`，trace `9a41cd118c2c44fc76785047cafcaa194ea999c78d28fafed449588d721f65da`；200 Mbps = 1940 / 1816 / 96 / 28 `HOLDING_QUEUE_OVERFLOW`，config `6bd42a0d15ee1d5d0a18324d6a6f3679d8374dfdd0b948b325ad94abfca0c7ee`，trace `eba4359f12a9247ee85e32bd39a49cf404677d41dad2bfa6c7d7f39cab09bfe1`。三档均 natural end、conservation true、receipt verified；本地墙钟约 78.7/79.0/79.3 s。
- VM 结果（同一部署代码）：100 Mbps = 944 / 877 / 60 / 7 holding overflow，config `a7c4efd26dc6dd41064c7f066e2de005ce9495cf4453b423a0cf57cf26bcf9a4`，trace 与本地相同，wall `265.85 s`；200 Mbps = 1940 / 1816 / 96 / 28 holding overflow，config `1446e0bddfea67481995ffaa555e316627c4a91655d82b995f6a23101508def0`，trace 与本地相同，wall `264.48 s`。两档均 natural end、conservation true、receipt verified；50 Mbps 同部署的 140 星 60 s smoke 已在上一条记录中验证。
- 暂定候选：50 Mbps 低负载、100 Mbps 中负载、200 Mbps 高/压力负载；10 Mbps 只做 sanity。该表仍不是正式论文结果：available-capacity 分母、逐包三段时延、正式授权 E0 和资源 RSS 门禁仍未完成。VM 墙钟约为本地 3.4 倍，后续训练预算必须按 VM 实测调整。

## 2026-08-21：逐向物理可用容量分母（候选，待独立复核）

- 分支：`codex/20260821-available-capacity`；新增可选的 `execution.available_capacity_interval_s`（默认关闭，E0/诊断 profile 显式设 1 s）和独立的 `link_available_windows` ledger。每个固定区间按拓扑重匹配、已认证的几何上下线根和 MCS 距离阈值切成稳定片段，再在片段中点做速率积分；空闲链路也进入利用率分母；不把队列占用、服务窗口或学习观测混进容量定义。采样间隔下限为 0.01 s，且按拓扑切分后的单次运行最多 100000 个区间，避免误配置造成 CPU/ledger 爆炸。
- `metrics.summarize` 现在同时重算 service capacity 与 physical available capacity，输出 `available_capacity_bits`、`available_time_s`、`available_samples` 和 `utilization=served/available`；无新采样的手写旧 fixture 保持旧分母兼容。receipt 将原始 availability ledger 纳入 `ledgers_sha256`，验证时重新计算 metrics。
- 验证：定向 `28 passed`；`pytest -q CODE/leo_sim/tests CODE/tests` = **530 passed**；新增回归覆盖窗口内 GSL 上下线和退役 ISL 代际。M-Lab 10 s smoke 仍需在本 SHA 重跑；先前 18/18 delivered、conservation true、receipt verified 的结果来自上一版候选实现，不能替代本次验证。
- 边界：分母是明确的固定间隔、几何/MCS 分段物理机会估计，不是连续时间解析积分；GE outage 不从物理容量中扣除，而由独立 fate/队列指标解释。仍需独立冷审、长窗 MCS VM 验证和资源成本评估后才能合入主线。

## 2026-08-21：容量窗口按拓扑事件切分（候选，待独立复核）

- 独立冷审指出：容量间隔 1 s、拓扑重算 0.5 s 时，若只按中点记录会漏掉窗口后半段新装 ISL。修复后 ticker 按拓扑重算边界切分；已排空旧代只保留在包含其排空时刻的窗口，避免旧代跨窗口继续充当可用链路。
- 验证：定向 `28 passed`；全量 `pytest -q CODE/leo_sim/tests CODE/tests` = **530 passed**。新增回归明确断言旧 `isl:0:1` 只在 `[0,0.5]`、新 `isl:0:2` 只在 `[0.5,1]`。
- 独立冷审上一轮三项 blocker（退役 ISL、窗口内上下线/MCS 阈值、采样下限/上限）已关闭；本轮需复核拓扑事件切分后再决定合入。
- 第二轮复核又发现旧代链路在窗口中途排空时会把容量计到窗口末尾；已改为按 `drained_at` 截断，并新增回归。待第三轮复核。
- 处理方式：采样器先保留窗口内的候选片段，模拟自然结束、所有退役代际排空后，用确定的 `drained_at` 截断原始 availability ledger，再交给 metrics/receipt 重算；不会修改服务事件或数据包语义。

## 2026-08-21：physical available-capacity 合入并完成同 SHA VM E0 工程校准

- PR #91 已合入 main，merge SHA=`b356d03d205e0b0851ca998874d6b3256c2b9640`；独立冷审绑定前一提交 `396c2ee`，定向 `29 passed`，审查确认窗口内几何/MCS 分段、拓扑边界、新旧 ISL 代际和 `drained_at` 截断均无容量窗口跨界膨胀。合入前相关全量为 `531 passed`。
- 部署：canonical VM `/data/论文/leo-direct-sim`，source tree SHA=`d391dff5431c44c8af6b42302b2611b8ba4c1dc06b64a871d5f6a569cfcb64a8`，deployment receipt SHA=`ea343bc8d9b7fefbe2f88cddf594dfe97d7fce850db66a8170b46759c6e11578`。VM 使用固定 `leo-i39` 环境（Python 3.11.15、PyYAML 6.0.2、NumPy 1.24.3、SimPy 4.0.1）；系统 `python3` 缺 PyYAML，不能作为运行环境。
- VM 工程 E0（非 formal、非论文结果）：140 星、60 s、MCS、1 s 拓扑 cadence、M-Lab 三 OD + 20--40 s burst、50 Mbps；natural_end=`true`，`conservation_ok=true`，`receipt verify=verified`，461 offered / 440 `DELIVERED` / 20 `ACCESS_REJECTED` / 1 `IN_SYSTEM_AT_STOP`，0 queue overflow，wall=`267 s`；`link_available_windows=29,656`，ledgers=`93 MB`。结果证明同一 SHA 的非学习测量链可以在 VM 跑通，不证明正式 E0 或论文结论。
- 当前边界：available-capacity 分母代码和 VM ledger 已有证据；逐窗口独立重算、每包 queue/tx/prop 三段时延和三段和 gate、D1 旧平台 MCS 对照、D2 长窗语义、R1-A1、学习 VM smoke、formal authorization cohort 仍是后续门禁。

## 2026-08-21：PR #93 合入与 M-Lab 多 OD T0 闭环

- PR #93 `feat: add bounded M-Lab multi-OD endpoint mapping` 已通过 CI（全量 `582 passed, 1 skipped, 3 subtests passed`）并合入 main；merge SHA=`4e89b5c4d0de789b1d89043e5be5fd98b6fa7ea9`。
- 新增显式 `endpoints.mlab_auto=true` 与 `mlab_max_sites`：从完整快照的 44,929 行、4,752 个有向 OD 对、2,604 个聚合单元中选择最大测量强连通子图；默认上限 64，本 profile 选中 56 个单元。选择规则、单元列表、候选规模和 measured-outgoing source weighting 写入 trace manifest；显式端点模式不受影响。
- canonical VM 已部署该 exact SHA；deployment receipt SHA=`8b22597b548eea77ffa5dce79694ad9c4c690b598270127b5b3cae71c85b6178`，source tree SHA=`1c231110c23d2236cc6667a9cb551b2a9a4ae69b4ed4718b1696f16f5789546f`。
- VM T0 profile `mlab_multiod_burst_t0.yaml`（140 星、20 s、MCS、1 s cadence、50 Mbps、8--16 s burst、1 Mbps packets）：trace SHA=`f6981c327f4c36e659d3f7b5ef66128f94a199d0203591401c88ed0e8ab22de4`，1,299 offered、613 delivered、579 `ACCESS_REJECTED`、107 `IN_SYSTEM_AT_STOP`；natural end、conservation、receipt verify 均通过。
- T0 原始 ledgers：20,935 packet events、1,648 service windows、10,932 availability windows；独立 metrics 重算与存档完全相等。该运行是工程 T0，不是 formal 或论文结果。

## 2026-08-21：同一 M-Lab 多 OD trace 的 VM topology cadence 校准

- 四档只改变 `topology.recompute_interval_s`，保持 config 之外的流量/seed/端点选择和 trace identity 不变；四档 trace SHA 均为 `f6981c327f4c36e659d3f7b5ef66128f94a199d0203591401c88ed0e8ab22de4`。
- `0.5 s / 1.0 s / 2.0 s / 5.0 s` 均 natural end、conservation true、receipt verified，fates 均为 `613 delivered / 579 ACCESS_REJECTED / 107 IN_SYSTEM_AT_STOP`；四档 raw ledgers 独立重算 metrics 均 `validation.ok=true`。
- VM wall-clock / topology recomputes / availability samples：`0.5 s = 171 s / 39 / 21,726`；`1.0 s = 120 s / 19 / 10,932`；`2.0 s = 107 s / 9 / 10,932`；`5.0 s = 94 s / 3 / 10,932`。1/2/5 s 的每包指标和链路指标逐项相同；0.5 s 仅增加 availability 采样（capacity 浮点差在采样表示层），不改变交付/时延汇总。
- 暂定决策：E0 主候选保留 `1.0 s`；`2.0 s` 做成本敏感性，`5.0 s` 做慢更新负对照。该 20 s 校准不能替代 D2 长窗语义证明；下一阶段为同 exact SHA 的 E0 低/中/高负载标定。

## 2026-08-21：main 29c1583 上完成 M-Lab 多 OD + burst 三档 E0 工程标定

- 分支：`codex/20260821-e0-load-docs`；代码未修改，仅更新实验真相源和机器索引。基于 main `29c158349caf33c313d9ec0940f8eefc13f91485`，canonical VM deployment receipt SHA=`6519847a3a866e7342d8aa36360ed2e68d3cb98ef51d4458d390420925271cc6`，source tree SHA=`8a9ab6f570585567efba1c675fe12dd4687c4c917bdabab24aedeaf6ca32866c`。
- 固定 profile：140 星、20 s、MCS、1 s topology cadence、M-Lab 最大强连通 56-cell、8--16 s burst；三档只改变 `offered_mbps`。VM 三档均自然结束、`conservation_ok=true`、`receipt verify=verified`、原始 packet/service/availability ledger 重算 `validation.ok=true`。
- 结果：50 Mbps = 1,299 offered / 613 delivered / 579 `ACCESS_REJECTED` / 107 `IN_SYSTEM_AT_STOP` / 0 overflow，wall 119 s，trace `f6981c327f4c36e659d3f7b5ef66128f94a199d0203591401c88ed0e8ab22de4`；100 Mbps = 2,756 / 1,253 / 1,270 / 233 / 0，wall 129 s，trace `e6e7bd329f6822046f5d57611690d609a3647e1dca7639e170e985d891000e09`；200 Mbps = 5,551 / 2,382 / 2,597 / 405 / 167 holding overflow，wall 134 s，trace `f009c98d8be5757a4ba1afe585fed32d6974143582eb3c9d8657344413a834c6`。
- 暂定解释：50 为低负载候选，100 为中负载候选，200 为压力/过载对照。它们是工程标定，不是正式论文效果结果；formal E0 仍需资源 RSS、三段时延 artifact/独立重算、学习 pilot、授权与 paired analysis 门禁。相关文档同步为 `ANALYSIS/EXPERIMENT-PROGRAM.md`、`ANALYSIS/CURRENT-EXPERIMENT-READINESS.md` 和 `EXPERIMENTS/experiment-program.yaml`。

## 2026-08-21：main 0fc9427 资源剖析与四学习臂工程闭环

- 部署：main `0fc9427520eb1d67e3493a521ea767c69b69575f`，canonical VM deployment receipt SHA=`c318945c852182c2d34e4d255a0ba79715ca31f030fb7f7c76be48065f0baae3`，source tree SHA=`390fd14375ab95aff885fe6de3758d5ea8638c74abd33a6e827da6832a987c94`。固定环境仍为 `/data/liguang13/conda-envs/leo-i39/bin/python`。
- 资源剖析：同一 2 s、100 Mbps、56-cell M-Lab/burst 配置，1/2/4/8 线程均 natural end、conservation true、事件数 286,671、trace SHA=`f69b73b3e8bd02ff2b9e22c05d0c369d2bf1c36e7c7f8eab0bbe5c22f5165b02`；墙钟约 `14.298/14.412/15.648/14.707 s`，峰值 RSS `465,996/461,260/459,948/461,652 KiB`。没有可重复的多线程加速，后续 pilot 采用 1 线程串行，避免空耗 CPU。
- 学习工程闭环：同一 2 s、100 Mbps、seed=7/41、`fast_train=true` 配置完成 Q-learning、DDQN(C3)、GAT、MPNN 各自 train→checkpoint→eval；8 个 run 均 natural end、`conservation_ok=true`、`receipt verify=verified`，8 个 raw ledger 独立 `metrics.validation.ok=true`。训练步数：Q-learning 112、DDQN(C3) 104、GAT 102、MPNN 103；每个 eval 均记录实际加载的训练 checkpoint SHA。
- 训练—评估不是论文效果结果，只证明当前 main/VM 的学习执行链可跑通。仍未完成 replay/optimizer/target/RNG 完整续训、formal authorization cohort、V2 artifact→claim、逐包三段时延正式 gate 和 Q0 物理上界。

## 2026-08-21：D2 60 秒长窗与 20 秒 DDQN 训练起步

- 长窗：main runtime code SHA=`d2247140312396cbf111e54239ec5274f22257c024d4f0909f50a6c4232454c0`，140 星、60 s、100 Mbps、56-cell M-Lab/burst、1 s cadence。VM 输出 `engineering-d2-long-60s-0fc9427`：`natural_end=true`、`conservation_ok=true`、`receipt verify=verified`、metrics `validation.ok=true`；8,510,023 events、216,243 packet events、7,908 service windows、33,137 availability windows、2,792 delivered、3,211 `ACCESS_REJECTED`、194 `HOLDING_QUEUE_OVERFLOW`、537 `IN_SYSTEM_AT_STOP`，输出约 139 MB。该轮是 D2 长窗工程验证，不是论文效果结果。
- 20 s DDQN：同一 100 Mbps/56-cell M-Lab trace，训练与评估 trace SHA 均为 `e6e7bd329f6822046f5d57611690d609a3647e1dca7639e170e985d891000e09`。训练 natural/conservation/receipt/metrics 全通过，1,220 train steps、1,227 transitions、checkpoint SHA=`9554170451d2f1866bcc23e381772189014e3f9e64c8ba5e931a46ce19312e97`；评估重新加载该 checkpoint，natural/conservation/receipt/metrics 全通过，0 train steps。20 s 负载下 3 `HOLDING_QUEUE_OVERFLOW`、约 375 个 `IN_SYSTEM_AT_STOP`，说明起步时长已进入真实拥塞压力区。
- 边界：本轮仍是 engineering/pilot；没有授权 cohort、paired claim、replay/optimizer/target/RNG 断点恢复或正式论文统计，不能直接写入论文结论。

## 2026-08-21：容量锚点与最新 VM 证据文档同步

- 分支：`codex/20260821-capacity-anchor-docs`；仅同步实验真相源和机器索引，不修改仿真内核。
- 当前 main `0f7249fb085ea05576c04d8b2b1f9e55be9e12a0` 已部署到 canonical VM；deployment receipt SHA=`89e70f943ef7c19b4f615e56cbf7cf2c349d49f572b916a97d2f816e4a33a4a9`，source tree SHA=`6dc0afec1070002fe83c5ddd0955c40c7ba5a2316cffa01fe1d01f8bc047d2fd`。
- 文档补录：capacity policy 负对照、D2 60 秒长窗、20 秒 DDQN train→checkpoint→eval、当前 main/deployment SHA；明确这些仍是 engineering/pilot，formal V2 artifact→claim、replay 续训、正式 E0/PILOT 和 Q0 闭环仍未完成。
- 验证：`git diff --check` 通过；`EXPERIMENTS/experiment-program.yaml` 可由 PyYAML 解析（22 experiments、23 requirements）。待本分支 CI 绿后合入并重新确认 VM SHA。

## 2026-08-21：PR #98 合入并重新部署主线

- PR #98 已通过 pytest CI 并 squash 合入，当前 main=`69c40b158abeabd6c7ccd0bbbead5ab646b51905`。
- canonical VM 已重新部署同一 main；deployment receipt SHA=`76244c2f62a49d748f213f6aa1544a122bd01d978ea53037bdc76ac46499e22c`，source tree SHA=`b5a95f4d253cd6bb154fc22d590c8331d2a5c4e835b0f1d8ac2a3a653a21f578`。
- 本次仍是文档同步和部署，不改变仿真行为；formal E0/PILOT、replay 续训、V2 artifact→claim 和 Q0 闭环继续保持未完成状态。

## 2026-08-21：exact-resume 实现与 VM 恢复验证

- PR #100--#104 已通过 CI 合入；当前 main=`bfae7616897bb56c92c87904427926f78c93d666`。
- 新增 `leo-sim-ddqn-resume/v1` 与 `leo-sim-qlearning-resume/v1` continuation bundle：DDQN 保存 replay、online/target、optimizer、训练计数器、NumPy/TF RNG；Q-learning 保存 Q 表、计数器和 NumPy RNG；manifest 绑定 schema、身份和每个 artifact SHA。
- canonical VM 部署 receipt SHA=`279522bf75404f16d4041bdb23539a71f4bb4b801fcb961de32af64b26b0360d`，source tree SHA=`261c185f59d7019ecc9e1bc546e7f441470be5c7ef09d8590d817eea3d1bd3ad`。
- VM 验证：DDQN exact-resume 恢复 replay/optimizer/target/RNG 后，继续同一 transition 的下一动作、训练步数、online/target 权重一致；Q-learning 恢复测试通过。相关定向测试 `2 passed`，学习/Q-learning VM 回归 `51 passed`。
- 边界：这是状态恢复和短续接证据，不是完整长窗“中断续训 vs 不间断”论文等价；该门仍未关闭。

## 2026-08-21：PR #105 后主线文档同步部署

- PR #105 已合入；当前 main=`7f29ea3ee21280722885bedc3efda3d98c56bd98`。
- canonical VM 已部署同一 main；deployment receipt SHA=`6b916fbfab1debb0a65113d3c78be47f619463683ac0d4017791b4e72a8d0289`，source tree SHA=`b0fb2db50d30338a68351eb0ea754332d43144624bf39bdfab655e7ca282644f`。
- 本次为文档同步部署，不改变 exact-resume 运行行为；完整长窗中断/不间断等价、formal E0/PILOT、V2 artifact→claim 和 Q0 仍是后续门。

## 2026-08-21：PR #107 formal E0 桥接运行完成

- 正式包 PR #107 已通过 CI 并 squash 合入，当前 main=`c6c18d0122b7251abe3a8b30b07e0dee746e0405`。该包绑定单个 `leo_sim_v2` 非学习 E0：140 星、20 s、M-Lab measurement-proxy 多 OD、50 Mbps、8--16 s burst、MCS、1 s 拓扑重匹配、control plane、seed 7；它是工程到正式链的桥接，不是算法比较或论文结果。
- canonical VM 已部署同一 main；deployment receipt SHA=`6f9ad082a15e372fe93ce16dbabfaeaa7009e7c9e08cbaa7598e9946c076171a`，source tree SHA=`ecc2e3a03c4237115e8821d7c6669acbfbf3b8f766cdd88123574362bfc50956`。授权 SHA=`19917bd8bc0e88c50b7c2e54c8e69c4360bb3edd53f88cccf09d549cde1492ca`，run id=`EXP-20260821-E0-FORMAL-R01-main-s7`。
- VM 正式回执：`natural_end=true`、`conservation_ok=true`、`research_eligible=true`、治理 `verification_errors=[]`、`receipt verify=verified`；1,299 offered、613 `DELIVERED`、579 `ACCESS_REJECTED`、107 `IN_SYSTEM_AT_STOP`、0 queue overflow；正式运行 wall-clock 约 123 s。原始结果目录为 `CODE/Results/EXP-20260821-E0-FORMAL-R01-main-s7`（不入库）。
- 当前明确边界：单运行 E0 使用 `leo-sim-experiment-run-manifest/v1`，而 `CODE/experiment_platform/v2_analysis.py` 的 paired analyzer 只接受 matrix manifest；因此本次正式回执链已闭合到自然结束/守恒/授权，但 **V2 artifact→paired-analysis→claim** 仍未闭合。下一组比较实验必须使用 matrix contract（至少一对受控 cells），不能把本次单运行直接写成论文对比。

## 2026-08-21：PR #109 paired V2 analysis bridge 完成

- PR #109 已通过 CI 并 squash 合入，当前 main=`40dfa39c50964c0f271ca428810f03865dc54290`；canonical VM 部署 receipt SHA=`c2a998ddd74866bcc706ae4f139050768e4a90cf95bb90a78d2489da1884e3b2`，source tree SHA=`b145900fbd80386ed75f9762666122a1d92242f92df1f978301b216dbc10a32e`。
- matrix `EXP-20260821-E0-PAIRED-R01` 的 control 与 baseline_copy 两个 cell 均在同一部署、同一 config SHA=`7ede74b936ad49e7a8e9b21779a6f6afc54cc2671f3e5f87670c14aed13c123d`、同一 trace identity、seed=7 下正式运行；两次均 `natural_end=true`、`conservation_ok=true`、`research_eligible=true`、VM `receipt verify=verified`。
- VM `v2_analysis` 已生成 `ANALYSIS/EXP-20260821-E0-PAIRED-R01/v2-paired/analysis-manifest.json`、`summary.json`、`claim-gate.json`；再次 `verify_persisted_analysis` 返回 `ok=true, errors=[]`。两臂 `delivery_rate=0.4719014626635874`，预注册 `baseline_copy-control` 配对差=`0.0`。
- 这一步正式闭合了“授权 cell → 原始 receipt/ledger → 主指标重算 → paired analysis → claim boundary”链，但仍只是同配置一致性校验；claim gate 明确禁止算法优越性、拥塞控制效果、Q0 最优性和论文统计结论。下一步才进入第一组有真实处理差异的算法/策略对照。

## 2026-08-21：PR #111 EXP1 capacity-routing 正式配对运行完成

- PR #111 已通过 CI 并 squash 合入，当前 main=`b6b975f5230c86460076b1549d2b680f23c79994`；canonical VM 已部署同一 SHA，deployment receipt SHA=`8fcbbd3f2a466ae718634a51439e281656c048de871c36f0224a66a5eb8b1701`，source tree SHA=`f6a11148ac25388f1e67957b2f5813689e233edca4d53324f26b0fa93bce31d5`。
- 矩阵 `EXP-20260821-EXP1-CAPACITY-R01` 固定同一 M-Lab measurement-proxy trace、100 Mbps（20 s、140 星、MCS、1 s 拓扑重匹配、control plane、seed=7），只改变 `routing.policy`：control=`hop`，treatment=`capacity`。授权 SHA=`9d0e189504bbd2669a88721bb92c58cfb36ead2154afb424b4cd452fbd58fa28`；两 cell 均在 VM 上自然结束、守恒通过、`research_eligible=true`，且 VM `receipt verify=verified`。
- 两臂结果：均为 2,756 offered、1,253 `DELIVERED`、1,270 `ACCESS_REJECTED`、233 `IN_SYSTEM_AT_STOP`、0 queue overflow；`delivery_rate=0.454644412191582`，预注册 `capacity-control` 配对差=`0.0`。两臂 ledger SHA 不同，说明策略确实走了不同的服务/时序路径，但在这一负载、这一 seed 和这一单配对下，交付数量没有变化。
- 从原始 ledger 独立重算：已交付包平均 `e2e_s` 为 control `0.294096`、capacity `0.292419`；平均 `total_queue_wait_s` 两臂均 `0.281647`；平均 propagation 为 `0.010584/0.009209`，平均 transmission 为 `0.001865/0.001563`。546 条链路的平均物理可用容量利用率为 `0.0002409/0.0002063`，最大值两臂均约 `0.01508`；metrics validation 均为 `ok=true`。
- VM `v2_analysis` 生成并验证 `ANALYSIS/EXP-20260821-EXP1-CAPACITY-R01/v2-paired/`，`verify_persisted_analysis` 返回 `ok=true, errors=[]`。这组证据可支持“固定 M-Lab burst profile 下的描述性零差异”，不能支持算法优越性、因果拥塞控制结论、Q0 最优性或论文统计结论；仍需多 seed/多负载和独立 claim review。

## 2026-08-21：正式 E0 低/中/高负载矩阵完成并闭合 V2 重算

- 正式包 PR #113（矩阵）与 PR #114（授权）已合入；六个 cell 使用同一授权 cohort、同一 VM 部署主线 `b39f0a72f4b02d34ccbf3592a4e68113795904dc`，deployment receipt SHA=`6d3b6ca1f6681248fe5881ac08102eb7d211a00b3430a25cd0b31af9214c855c`，authorization SHA=`d0337c35b247d6f548936cf7495bf2584352b7f644f8b5ada5e4bdd92779dcb3`。六次均自然结束、`research_eligible=true`，逐次 `receipt verify=verified`。
- 设计含义：50/100/200 Mbps 是 burst 前的 base offered rate；20 s 运行在 8--16 s 施加 2x burst，因此时间平均目标分别是 70/140/280 Mbps。每档 control/copy 是完全相同的非学习重复单元，不是算法比较。
- 六个原始回执的成对结果（control 与 copy 完全一致）：
  - low/load-50：1,299 offered，613 delivered，579 `ACCESS_REJECTED`，107 `IN_SYSTEM_AT_STOP`，0 overflow，delivery rate=`0.4719014626635874`；墙钟约 121/120 s。
  - medium/load-100：2,756 offered，1,253 delivered，1,270 `ACCESS_REJECTED`，233 `IN_SYSTEM_AT_STOP`，0 overflow，delivery rate=`0.454644412191582`；墙钟约 123/126 s。
  - high/load-200：5,551 offered，2,382 delivered，2,597 `ACCESS_REJECTED`，167 `HOLDING_QUEUE_OVERFLOW`，405 `IN_SYSTEM_AT_STOP`，delivery rate=`0.42911187173482257`；墙钟约 131/134 s。
- 原始 ledger 独立重算均通过；低/中/高档平均物理可用容量利用率约为 `0.00011595/0.00024093/0.00044596`，最大链路利用率约为 `0.00782/0.01508/0.02972`。中档已交付包平均 `e2e_s=0.294096`、排队等待=`0.281647`、传播=`0.010584`、传输=`0.001865`；其余档位同样保留逐包三段字段。
- 首次 V2 分析发现分析器把低档 contrast 错套到所有 pairing key，正确拒绝了该错误分析。PR #115 修复为“每个 contrast 只计算包含其左右臂的 pairing key；若某 key 只有一侧则继续 fail-loud”，CI 为 `546 passed, 1 skipped, 3 subtests passed`。合入主线 `e83653c907427f6b6bd2410119b914a330808755` 后重新部署，VM `v2_analysis` 返回 `VERIFIED`（6 runs），`verify_persisted_analysis` 返回 `ok=true, errors=[]`。
- 本组可支持：三档负载的重复一致性、原始负载/突发/端点选择/包命运和指标可重算证据；200 Mbps 已出现 holding overflow，可作为压力档。不能支持：最终 E0 阈值、跨档因果拥塞结论、算法优越性、Q0 最优性或论文统计结论。下一步是基于这张负载表冻结 E0 主档/压力档，再运行真实学习算法的正式 pilot。

## 2026-08-21：中负载真实流量四学习臂 train→checkpoint→eval 工程 pilot

- 运行范围：canonical VM 上已部署主线 `e83653c907427f6b6bd2410119b914a330808755`，deployment receipt SHA=`d7baa84dda74501132130f7b9aaf84a844b0336e1fb4a695e35668423adf096f`；固定 140 星、20 s、100 Mbps base + 8--16 s 2x burst、MCS、1 s 拓扑重算、M-Lab 56-cell measurement-proxy、seed=7，训练和评估均使用 trace SHA=`e6e7bd329f6822046f5d57611690d609a3647e1dca7639e170e985d891000e09`。
- DDQN/C3：训练自然结束、守恒、receipt verified，4,716 train steps，checkpoint verified SHA=`17ee9ae7b89a416f6fd667c4a168cdf4e4cb75ea6a973391bb4858326a989862`；评估 0 train steps、2,017 decisions，加载 SHA 与训练一致，receipt verified。
- Q-learning/C3：训练自然结束、守恒、receipt verified，5,086 train steps，checkpoint verified SHA=`943fda8cd60817040b7af9dd0e6680cfaf66e904344eb1a7a680c7145d7fd8b1`；评估 0 train steps、加载 SHA 与训练一致，receipt verified。
- DDQN/GAT：训练自然结束、守恒、receipt verified，4,975 train steps，checkpoint verified SHA=`59552ee9bafeb0051eb3fe7a49b143ef2cfd37eb3dbb2d5ecc3290b90f75dff6`；评估 0 train steps、3,252 decisions，加载 SHA 与训练一致，receipt verified。
- DDQN/MPNN：训练自然结束、守恒、receipt verified，5,068 train steps，checkpoint verified SHA=`727cee5fd512962154c90f336202095f90b82c670038bfb9f8e5b0c489534da9`；评估 0 train steps、3,332 decisions，加载 SHA 与训练一致，receipt verified。
- 这八个 run 是工程 pilot，不是正式授权矩阵，也不支持算法优越性或论文统计结论；它们证明当前 VM/依赖下四个学习路径在主负载上能真实训练、保存、重载、评估，且不会静默退化为无学习。下一步把同一 train/eval 证据装进正式 matrix/授权链，再进入拥塞/利用率诊断；正式评估仍需按 60--120 s 和多 seed 预算重新规划。

## 2026-08-21：正式学习基线 evaluation-only pilot 完成

- 授权矩阵：PR #120（矩阵/审阅/定案）与 PR #121（派生授权）均通过 pytest CI 并合入；执行主线 `b6175ab8022c0f17ee88b1f393780c510bd4018e`，VM deployment receipt SHA=`2747b95acd1819a446c566fe020c7a650e4708d20140bd215b64caa8d41ab61f`，authorization SHA=`7048dee403951d51db1005d217237f8a38ecd57a88c9b7fa2ef0c1f3b335f770`。cold-start、satellite-DRL、adversarial 三份独立审阅均 PASS；八个 cell 共享同一不可变 M-Lab trace（trace identity=`4b726ee1370d1762d15275bd8f4965925b840548d2880db37296ebb4b32ac281`）。
- VM 执行：八个 evaluation cell 串行、`--cpu-list 0` 完成；每个均 `status=success`、`exit_code=0`、`natural_end=true`、`conservation_ok=true`、`research_eligible=true`，逐个 `python -m CODE.leo_sim receipt verify` 通过。八个学习元数据均 `mode=eval`、`train_steps=0`、`checkpoint_verified=true`，实际加载 checkpoint SHA 与授权一致：Q-learning `943fda8d...`（两臂）；DDQN/C3 `4f3d9ef5...`、`e8c8e41c...`；GAT `40da0753...`、`b1fd2dc9...`；MPNN `aebf1664...`、`51fd1a3d...`。本轮记录了单核串行运行，但没有逐 run RSS 采样，不能把它当资源剖析证据。
- V2 重算：VM `v2_analysis` 返回 `status=VERIFIED`、`verified_runs=8`；再次 `verify_persisted_analysis` 返回 `ok=true, errors=[]`。当前配对仅是同 checkpoint 的 duplicate consistency（四个 b-minus-a delivery-rate 差均为 `0.0`），claim gate 明确禁止算法优越性、因果拥塞控制效果、最终 E0 阈值、Q0 最优性和论文统计结论。
- 独立拥塞诊断：20 s、100 Mbps 这轮的 546 条链路可用容量总和约 `10,804.261 Gb`，各臂已服务约 `3.503--7.245 Gb`；加权平均利用率约 `0.000324--0.000671`，最大链路利用率约 `0.015081`。因此这八臂只证明 train/eval 和证据链可运行，不能作为拥塞饱和或算法排序证据；后续拥塞主线应优先使用 E0 已出现 holding overflow 的 200 Mbps 压力档，并补正式多 seed/长窗及三段时延重算。

## 2026-08-21：200 Mbps pressure evaluation 正式诊断完成

- 矩阵 PR #123 与授权 PR #124 均通过 CI 并合入；执行主线 `7645f4bb20c6aa6148f012cf83f4e2e0eb3a3777`，VM deployment receipt SHA=`d37a2383cc1a3d48679d1a6d3af0117d2cf7cfc0a2e990da28cf4963fe8837d2`，authorization SHA=`d6e04d03aafb224949616c4a4555790e85b52691cb1d6084bac326ddb2d66851`。矩阵为 6 个 evaluation-only cells、3 个严格两单元配对；三类独立冷审均 PASS。
- 固定 140 星、20 s、MCS、1 s 拓扑重匹配、M-Lab measurement-proxy 多 OD + burst、seed=7，仅把 base offered rate 设为 200 Mbps。6/6 均串行在同一 VM SHA 上自然结束，`conservation_ok=true`、`research_eligible=true`，逐个 `receipt verify=verified`；V2 analysis 返回 `VERIFIED`/`verified_runs=6`，再次 `verify_persisted_analysis` 返回 `(True, [])`。分析 manifest SHA=`d18c088dd4cba6c0dcfe24335fb5f41f0b358be37396d2be6cc0688fc54bf7e3`。
- 从原始 ledger 独立重算，所有臂均为 5,551 offered、2,597 `ACCESS_REJECTED`、167 `HOLDING_QUEUE_OVERFLOW`；Q-learning 为 2,215 delivered / 562 `IN_SYSTEM_AT_STOP` / 10 `NO_ROUTE`，DDQN 为 2,309 / 468 / 10，GAT comparison 为 2,285 / 473 / 29，MPNN comparison 为 2,254 / 487 / 46。V2 描述性 delivery-rate 差分别为 DDQN−Q-learning=`0.0169338858`、GAT−Q-learning=`0.0126103405`、MPNN−Q-learning=`0.0070257611`；每个只有单 seed/单 pair，不能解释为优越性或因果效果。
- 逐向物理可用容量分母存在且验证通过：downlink 可用约 `1,050.270 Gb`、uplink `1,827.995 Gb`、ISL `8,023.145 Gb`；各臂最大链路利用率约 `0.029719`，最高链路为 `gsl:downlink:128:G1:125:319`。压力档已经真实暴露 holding overflow、在系统积压和长尾等待，适合进入下一步拥塞机制/Q0 归因；但它仍不是最终论文样本。
- 资源边界：本次 formal receipt 没有逐 run CPU/RSS 字段；运行中人工观察到单核约 99% CPU，RSS 约 0.56--0.88 GB，不能冒充完整资源 profiling。已有 1/2/4/8 线程 profiling 仍是资源选择证据；正式长训前仍需按同一方法保存逐 run wall/CPU/RSS/steps/s。
- 结论边界：本组只证明高负载压力可复现、拥塞指标/利用率/逐包三段时延可从原始 ledger 重算；claim gate 继续禁止算法优越性、因果拥塞控制效果、最终 E0 阈值、Q0 最优性和论文统计结论。下一步进入 Q0-I/Q0-F 与信息阶梯，不先提出新方案。

## 2026-08-21：Q0-I/Q0-F 有界 tiny 交叉验证候选

- 基线：`fd3ef5d496d42a77553de29d2288cbd476968d71`（当前 main，候选改动尚未合入或部署）；工作内容仅在独立候选工作区完成，未修改用户主工作区。
- 新增 `CODE/leo_sim/q0_tiny.py` 与 `CODE/leo_sim/tests/test_q0_tiny.py`：依赖无关的离散 tick 小场景。Q0-F 使用完整未来可用边日历做精确枚举；Q0-I 每个 tick 只接收当前窗口并滚动求解，不读取未来日历；另有独立无记忆枚举器、planned replay 和 online replay。
- 证据：Q0-I 首动作 `(0, 1)`、目标 `(0, 0, -1, -4)`；Q0-F 首动作 `(0, 2)`、目标 `(1, 0, 0, -2)`；`V_F >= V_I`；Q0-F 与独立枚举目标和动作轨迹一致；两种 replay 均无违规，Q0-F delivered packet 为 `(1,)`。CLI 输出为 `{'q0_i': (0, 0, -1, -4), 'q0_f': (1, 0, 0, -2), 'q0_i_first': (1, (0, 1)), 'q0_f_first': (1, (0, 2)), 'vf_ge_vi': True}`。
- 产物：`ANALYSIS/Q0-TINY-20260821.json` SHA=`f076c650a6a754a5f7d11c5955ddc90ab6022c8c456c0695818970ab25bcf5c8`；说明 `ANALYSIS/Q0-TINY-20260821.md` SHA=`4755a07ea1b699fab3dc2ecfc1776f7447fc82b25a588083290d6f13a76b2d1b`；source SHA=`74792731f074fd6869969f1655bc2a59a943645a7d2780df3213c0260e96c11c`；test SHA=`175be5019ee51f2eec35cf83098fcd8f9caa6e2fe7cdb8242994abeef224c177`。
- 验证：Q0/tiny/contract/snapshot/topology 定向 `28 passed`；相关全量 `568 passed, 1 skipped, 3 subtests passed in 7.37s`（文档修改后需重跑）；`git diff --check` 需在提交前复核。
- 边界与下一步：这是 tiny 正确性/因果信息合同证据，不是真实 M-Lab trace 的 Q0 上界、不是可扩展 CP-SAT/MILP，也没有闭合真实 kernel 的逐事件 planned-vs-executed receipt。下一工作单元继续实现信息阶梯 tiny 负对照，然后接真实压力窗口抽取；在真实 Q0/信息阶梯完成前不提出新方案、不写论文优越性结论。

## 2026-08-21：信息阶梯 tiny 合同候选

- 新增 `CODE/leo_sim/info_ladder_tiny.py` 与 `CODE/leo_sim/tests/test_info_ladder_tiny.py`，把四级视图固定为：本地队列+方向 → 速率/可用性 → 远端队列/拓扑 → 逐字段年龄。
- 验证结果：每一级只暴露协议声明的字段；修改隐藏远端队列/拓扑/年龄不影响低级视图及动作；远端队列 shuffle 保持多重集合但改变归属；fixed-age 负对照把所有年龄设为 1.0；未知等级和不适用负对照 fail-loud。定向 `5 passed`。
- 运行证据：`python3 -m CODE.leo_sim.info_ladder_tiny` 选择轨迹为 `(0,1) → (0,2) → (0,2) → (0,1)`，shuffle/fixed-age 均为真。source SHA=`865d9a8bfe9944f66a8b3750e9f1eee25e43a0eb76317c8673d4fbcfae263925`，test SHA=`dfc63280baac0bed90b8b943d7df84c22d4f95bf9ebd97b6d0fd31e11019c7d2`，机器证据 `ANALYSIS/INFO-LADDER-TINY-20260821.json`。
- 边界：这是信息 mask/负对照合同，不是训练、真实 trace、Q0 信息价值或拥塞控制效果。真实 V2 decision sink 的逐动作物理字段和逐字段年龄仍未实现；下一步必须接 200 Mbps 压力窗口/不可变 trace 后再做真实信息阶梯。

## 2026-08-21：真实决策信息审计通道实现候选

- 在 kernel 的可选 decision sink 中加入 `leo-sim-decision-info/v1`：每个合法转发方向记录 direct kernel truth（edge、distance_km、rate_bps、available、remote_queue_bits、topology_available）及字段 `source/observed_at/age_s`；learning 决策另记录实际可见 control-cache entry 的 generated/received/age/hops 和 payload 字段年龄。审计流只读输出，不改变 learner 输入或路由行为。
- CLI 新增诊断参数 `--decision-log <new.jsonl>`；正式授权运行和 dry-run 明确拒绝该参数，避免未绑定 artifact 混入正式证据。普通诊断运行可保存逐决策 JSONL。
- 验证：decision/CLI/Q0 定向 `42 passed`；相关全量 `575 passed, 1 skipped, 3 subtests passed in 7.04s`；`git diff --check` 通过。
- 边界：当前只是把真实 decision audit 接通，尚未在 VM 生成 200 Mbps 压力窗口的完整 audit，也未证明 learner 向量逐字段等价或信息价值。下一步在同一已部署 SHA 上跑诊断性压力 trace，检查 audit 字段覆盖/年龄分布，再决定真实 INFO/AGE-LADDER 实验臂。

## 2026-08-21：独立冷审修正 decision audit

- 冷审在 exact `f2a8589` 发现并要求修正：日志路径必须在仿真前 fail-closed；父目录链不得含 symlink；长跑不能把 rows 全部存内存；日志必须有 config/trace/code/receipt SHA 血缘；truth 字段不能冒充 learner tensor。
- 修正内容：`_DecisionLogWriter` 改为临时文件流式追加、内存 O(1)（只保留 row_count）；目标和 `.manifest.json` 在运行前检查且拒绝已有目标/任一父级 symlink；发布使用不替换现有目标的 hard-link；sidecar 绑定 config/trace/trace identity/code/result/receipt/log SHA 和 row_count；formal/dry-run 仍拒绝诊断日志。
- 审计语义修正：记录所有候选方向而不只记录已通过 legal mask 的方向；将下游语义命名为 `peer_egress_queue_bits`，另保留 `reverse_link_queue_bits`；顶层明确 `mapping_status=truth_audit_not_learner_tensor`。
- 新增回归：已有目标和 symlink 父目录均在仿真前拒绝且不留下运行 artifact；decision/CLI 定向 `10 passed`（修正后需重跑相关全量）。
- 当前仍未宣称完成真实信息实验：需要在修正版合入并部署后生成 200 Mbps 压力 trace 的 audit，核对字段覆盖/年龄分布，再决定真实 INFO/AGE-LADDER 实验臂。

## 2026-08-21：main bf625a9 的 VM 真实决策审计 smoke

- PR #129 已合入 main，执行 SHA=`bf625a9a94bc7532bba86c2d0cad3eefedacdd87`；canonical VM 部署 receipt SHA=`485869b40f5e0901fb0c3f942838f36afe07c50ff250b7c8c5ac2baf2274e3d8`，本地/VM source tree SHA=`5638c366510d188c641e0ad25222167fa26e6fb0880429e80b24c42c90229b5c`。
- 使用 VM 已配置的 `leo-i39` 环境运行 20 s、140 星、M-Lab 多 OD+burst、MCS、1 s 拓扑 smoke；默认系统 Python 缺 YAML 的首次尝试未启动仿真，未修改 VM 依赖；切换到 canonical 环境后成功。
- VM 回执：`natural_end=true`、`conservation_ok=true`、1,299 offered、613 delivered、579 `ACCESS_REJECTED`、107 `IN_SYSTEM_AT_STOP`、0 queue overflow；`receipt verify=verified`。
- 决策审计：929 行（316 forward、613 deliver），316/316 forward 含 candidate truth；schema 全为 `leo-sim-decision-info/v1`，`mapping_status=truth_audit_not_learner_tensor`，sidecar `row_count` 与日志 SHA 均核对一致。该结果是 VM 诊断 smoke，不是正式授权矩阵或论文数据；下一步需为当前 main 重新编译/审阅/授权正式压力矩阵。

## 2026-08-21：decision audit sidecar/hash 修正与本地真实流量 smoke

- PR #129 最新候选 exact SHA=`b910e675187fa3c297994e577f1ce3b874270f16`；独立冷审终裁 `APPROVE`。修正两个 fail-closed 问题：`.manifest.json` 在 trace/simulation 前预检；decision log SHA 在 append 时增量计算，关闭时不再一次性 `read_bytes()` 整个日志。
- 验证：新增回归后 decision/CLI/Q0 定向 `29 passed`；相关 `CODE/leo_sim/tests CODE/tests` 为 `550 passed, 1 skipped`；`git diff --check` 通过。
- 同一 SHA 本地真实 M-Lab 多 OD+burst smoke：140 星、20 s、55 个活动端点、1,299 offered packets、MCS、1 s 拓扑；`natural_end=true`、`conservation_ok=true`、receipt verify 通过；613 delivered、579 access rejected、107 in-system-at-stop、0 queue overflow。
- 同一运行的 decision audit：929 行，其中 316 条 forward、613 条 deliver；全部 `leo-sim-decision-info/v1`，316/316 forward 行含 candidate truth；sidecar `row_count=929`，日志 SHA 与实际文件一致。该运行是本地诊断 smoke，不是 VM 正式论文结果；最新 SHA 尚未确认合入 main/部署。

## 2026-08-21：R02 200 Mbps pressure matrix 编译、三方审阅与授权

- 基于当前 main `40bc27bcd2097bc64a77ea0ffc70970ff295ca2d` 新建 `EXP-20260821-CONGESTION-PRESSURE-EVAL-R02`，避免复用旧 R01 授权。修正一次真实发现的 R01/R02 `analysis_id` 残留后重新编译，source/request/analysis-request 统一为 `AN-CONGESTION-PRESSURE-EVAL-R02`。
- 三份独立冷审均 PASS，且均绑定同一组 13 个 R02 artifact hashes：cold-start `eeb409a05c21f252eb8aba23fe9411321f385b4335ffc1157c82cad195576317`、satellite-DRL `91bb9071fcdf8c46897a7de8d1ad9beb2c4ddddef01f789f5e5e97c09f3ffc84`、adversarial `acc1bae734cf8e8fc44c085a100f834b577a9c50f6bac72c83d3b743eabb44e1`；`verify_compiled_matrix` 为 6 cells / 3 exact pairs，相关测试与 schema/hash 校验通过。
- `finalize_decision` 返回 `ACCEPTED`；`authorize_experiment` 返回 `AUTHORIZED`（6 runs）。该授权只覆盖同一干净主线上的一次 200 Mbps 描述性 pressure diagnostic，不代表 VM 已运行，也不代表算法优越性、因果拥塞结论、最终 E0、Q0 或论文统计结论。
- 下一步：将 R02 包经 PR/CI 合入后，以合入后的 exact main SHA 部署 canonical VM，再串行跑 6 个 evaluation cells；逐个核验 natural end、守恒、checkpoint lineage、资源边界和 V2 paired analysis，任一 cell 失败即停止矩阵。

## 2026-08-21：R02 200 Mbps pressure matrix 已在 VM 串行完成并重算

- PR #131 已合入，执行主线 exact SHA=`00813e9570bb6a0bdeb6c38562c2e95b519ae8a9`；canonical VM deployment receipt SHA=`2da5be1df5515b62ae65de05d3026530a01478e0814704e72db1ebc77db6eab5`，source tree SHA=`ca098c0a8c4e30cf3bd24719962037859060e22b3b38a350873ff1834c417d82`，authorization SHA=`a3395cc3435112cff6299e577f862575daf57197ccf30297f8053a0ccd038886`。
- 6/6 evaluation cells 严格串行执行；每个 remote status 为 `success`、`natural_end=true`、`conservation_ok=true`、治理回执 `research_eligible=true`，六个 `python -m CODE.leo_sim receipt verify <dir>` 均返回 `verified`。没有发生训练、静默回退或资源错误。
- 固定 5,551 offered packets、200 Mbps base + 8--16 s 2x burst、140 星、M-Lab multi-OD/burst、MCS、1 s 动态拓扑、seed=7。Q-learning 三个 copy 臂的 delivery rate 均 `0.3990272023`；DDQN/C3=`0.4159610881`、GAT=`0.4116375428`、MPNN=`0.4060529634`。所有臂均有 167 `HOLDING_QUEUE_OVERFLOW`，`IN_SYSTEM_AT_STOP` 为 468--562；这确认压力档会暴露积压和长尾，但不证明算法优越性。
- 原始 ledger 可重算的物理量：总可用容量约 `10,901.410 Gb`；最大单链路利用率约 `0.029719`；三类链路可用/服务容量（Gb）为 downlink `1050.270/2.216--2.310`、uplink `1827.995/2.954`、ISL `8023.145/1.428--7.917`。已交付包平均 `e2e_s` 约 `0.354--0.361`，其中 holding wait 约 `0.341--0.346`，queue wait 约 `0.0019--0.0020`，propagation 约 `0.0066--0.0149`，transmission 约 `0.0012--0.0024`；这些是诊断指标，不是最终统计结果。
- VM V2 分析返回 `VERIFIED`、`verified_runs=6`；独立 `verify_persisted_analysis` 返回 `ok=True, errors=[]`。分析 manifest SHA=`bf19ffb07e306d2e2147207183d548d99a1882b23064b7709b21874b26580bea`，三个单 seed 描述性 paired differences 为 DDQN−Q-learning=`0.0169338858`、GAT−Q-learning=`0.0126103405`、MPNN−Q-learning=`0.0070257611`。
- 结论边界：R02 现在闭合了“当前主线 → 授权 → 同 SHA VM → 6 个自然结束回执 → ledger/V2 重算”的工程证据链，可以作为拥塞诊断和下一步实验设计输入；仍不能作为论文统计、因果拥塞控制、算法 superiority、最终 E0 阈值或 Q0 最优性证据。下一步应先做多 seed/重复和真实信息阶梯，再提出新方案。

## 2026-08-21：R03 两 seed pressure repeat 编译、复审与授权

- 基于合入 R02 证据后的 main `3fa26956da44d03c8b94c3ec2dfed5afc1615eb5` 新建 `EXP-20260821-CONGESTION-PRESSURE-EVAL-R03`；seed=7/11，各有 DDQN/C3、GAT、MPNN 与同 checkpoint Q-learning copy，形成 12 cells / 6 个 seed-specific exact pairs。修正一次真实的 `work_finalization` 残留和 single-seed 文案后重新编译。
- 三类独立审阅均 PASS，均绑定最新 19 artifact hashes：cold-start receipt SHA=`0e4eb66944268f0b4e5009e94840926d783b9ace303855e54cc69affa7eb0592`、satellite-DRL=`8ea089ad8792b3150a28c59316079ebfac8734ce96ec77e9410b40974b9b6c42`、adversarial=`14183f1d2139694e0b3579422102074573fc7a9dbcd5cbb4783f33d50ae67cc3`；`verify_compiled_matrix` 为 12 rows / 17 compiled artifacts，相关 schema/hash/定向测试通过。
- `finalize_decision` 返回 `ACCEPTED`；`authorize_experiment` 返回 `AUTHORIZED`（12 runs）。R03 只授权同一压力合同下的两 seed 稳定性重复，不是论文效果或 superiority 授权；尚未部署和执行。
- 下一步：R03 包经 PR/CI 合入后，用合入后的 exact main SHA 部署 VM，严格串行执行 12 cells；两 seed 若出现不稳定或资源问题，先修复/缩小实验，不进入新方案结论。

## 2026-08-21：R03 两 seed pressure repeat 已在 VM 完成并通过 V2 重算

- 执行主线 exact SHA=`a3fb1d7a42bbc330ac8dd33ef524894efbdc3f95`；canonical VM deployment receipt SHA=`0ca9f09632ecea678665c0fd7889479c12410acb6258301099bbdef57f7429e2`，source tree SHA=`67ff7e6e2e96207c6779917b51e84a6dd71e4aa1293b8bc675c9b05f1a4282ca`，authorization SHA=`dfd8269e98f0694c9a21560645379a31a2a6f4140d303992aab74a71044fdd12`。
- 12/12 cells 严格串行执行；每个 remote status 为 `success`、`exit_code=0`、`natural_end=true`、`conservation_ok=true`、治理回执 `research_eligible=true`，12 个 `python -m CODE.leo_sim receipt verify <dir>` 均返回 `verified`。没有发生失败、重跑、训练静默退化或依赖错误。
- VM V2 配对分析返回 `VERIFIED`、`verified_runs=12`；分析摘要状态为 `READY_FOR_INDEPENDENT_CLAIM_REVIEW`，独立 `verify_persisted_analysis` 返回 `{'ok': True, 'errors': []}`。analysis manifest SHA=`643f8df7a92b6269ca6575fb90d13c17bced9ae5d2763515caaa229631ad24d3`。
- 两 seed 的 delivery-rate 配对差（seed 7、seed 11）分别为：DDQN−Q-learning=`0.0169338858`、`0.0182436058`（均值=`0.0175887458`）；GAT−Q-learning=`0.0126103405`、`0.0150241459`（均值=`0.0138172432`）；MPNN−Q-learning=`0.0070257611`、`0.0089429440`（均值=`0.0079843526`）。这些只是同一 200 Mbps 压力合同下的两 seed 描述性重复，不做显著性或 superiority 解释。
- 两 seed 均保持压力现象：5,551 offered、167 `HOLDING_QUEUE_OVERFLOW`/臂，保留 `IN_SYSTEM_AT_STOP`、`NO_ROUTE` 和逐包 queue/transmission/propagation/holding 时延字段；可从 raw ledger 重新计算。资源仍只保留工程边界，未形成逐 run CPU/RSS 正式 profiling。
- 结论边界：R03 闭合了“同一 exact SHA → 授权 → VM 双 seed 运行 → 12 个自然结束/守恒回执 → V2 配对与持久化重算”的稳定性证据链；仍不能支持算法 superiority、因果拥塞控制效果、最终 E0 阈值、Q0 最优性或论文统计结论。下一步进入 Q0-F→Q0-I→信息裁剪阶梯的真实压力窗口设计，不在压力重复结果上直接提出新方案。

## 2026-08-21：信息阶梯 F0/F1 诊断锚点候选

- 在独立分支 `codex/20260821-info-ladder-policy` 实现两个确定性诊断 policy：`info_queue`（F0：本星各方向队列 + 已到达目的地服务广告 + 剩余跳数）和 `info_physical`（F1：再加入本星第一跳斜距、几何可用性、动态速率）。两者均禁止远端当前队列、未来几何和 oracle 真值，不改变学习器 observation tensor。
- 先写测试并确认未知 policy 失败，再实现；routing/config 定向测试 `28 passed`，相关全量 `554 passed, 1 skipped`，`git diff --check` 通过。代码提交 `65347d5`；独立冷审和 CI 尚未完成，不能称已合入或已部署。
- 配对设计已写入 `ANALYSIS/INFO-LADDER-REAL-DESIGN-20260821.md`：固定 R03 200 Mbps M-Lab multi-OD + burst 合同，先以 hop/F0/F1 做双 seed 诊断；必须保留本地队列置换、第一跳物理字段固定/置换负对照；在正式 request/审阅/授权前不启动 VM，不产生数值结论。
- 独立冷审发现并修正一个 P1：F1 所有第一跳暂时零速时不能返回空候选（否则内核会把等待误记为 `NO_ROUTE`）。`f65b3cb` 增加可达候选 deferred fallback 与 MCS/holding 集成回归；修复后相关全量为 `555 passed, 1 skipped`。本地 `info_physical` 20 s M-Lab smoke：1,299 offered、613 delivered、579 access rejected、107 in-system、`NO_ROUTE=0`，`natural_end=true`、`conservation_ok=true`、receipt verify=verified；这是候选分支 smoke，不是 VM/论文结果。

## 2026-08-21：INFO-LADDER F0 正式矩阵完成三方复核并授权

- 基于 exact candidate `058e5433ad14b7390028a542e4e86b3dbd2b0d15` 编译 `EXP-20260821-INFO-LADDER-FORMAL-R01`；本轮范围明确为 F0 `hop` vs `info_queue`，两个 trace seed（7/11）、4 个 non-learning cells、1 个 `info_queue_minus_hop` paired contrast；`info_physical` 延后为独立 R02，避免重复基线造成配对歧义。
- 三份真实独立复核均 PASS：cold-start `3c66c8748275e6372e0b9ce68f9c2c7cf5e69b21dd399f402a8a062ef8c0e465`、satellite-DRL `c5f5e98acf34dc116b4c9913ab0ce26f562240d0c0be45dd5fc6ae7fc238c94c`、adversarial `835326e8e5d1b39bf799d2f5ff121831d14af13ff618480d0f373b8262f722b1`；三者均绑定同一 11-artifact hash map，`verify_compiled_matrix` 4 rows/9 hashes 通过，相关测试均绿。
- `finalize_decision` 返回 `ACCEPTED`；`authorize_experiment` 返回 `AUTHORIZED`（4 runs）。授权仅表示可在合入后 exact main、干净部署的同一 SHA 上执行该 F0 诊断，不代表已部署、已运行或已有论文结果。
- 当前待办：将本 package 经 PR/CI 合入 main；合入后部署 canonical VM，严格串行运行 4 cells，逐个核验 natural_end、conservation、research_eligible、资源边界和 receipt verify，再做 V2 paired analysis。任一 cell 失败即停止矩阵；F1 `info_physical` 另起 R02。

## 2026-08-22：INFO-LADDER F0 已完成同 SHA VM 实跑与 V2 重算

- PR #136 已合入；执行主线 exact SHA=`c34fac937e865cb2f5543bacba2223eb4f34477e`。canonical VM deployment receipt SHA=`2d5535cea66aa3bac4065ace991d5cccdced5d3813df72902947cd3bf6378ce0`，source tree SHA=`1d4830e0a8f4850d333dce5f4d01fdd50e98ee369f8e26d6c0f225d9eedcd17a`，authorization SHA=`69019af696ff81e7ebeb3e35a3a3527c9590082de1e00beae11ef659e2181d77`。
- 4/4 cells 严格串行执行并自然结束，receipt verify 全部为 `verified`，守恒通过，治理回执 `research_eligible=true`。本地运行 receipt 的 `research_eligible=false` 是预期语义，不是失败。
- seed 7：hop 与 info_queue 均 delivery rate=`0.4291118717`（2,382 delivered，167 holding overflow，405 in-system）；seed 11：两臂均=`0.4408871400`（2,465 delivered，180 holding overflow，389 in-system）。V2 `VERIFIED`、4 runs；manifest SHA=`a5bba6f34b66700bf9e356723aaa615b1c8040b43914de0ea064371b4b1fd4f2`；paired differences `[0.0, 0.0]`；V2 persisted verifier `ok=True`。
- 路线审计补充：该零差异不是证明 `info_queue` 没有作用。seed 7 有 3/352 个出现 ISL 路径差异，seed 11 有 4/401 个；只是当前压力瓶颈由 access/holding 终态主导，尚未改变聚合交付率。下一步检查路线选择与队列占用，随后另起 F1，保留负对照；F0 仍仅作诊断，不进入论文 claim。

## 2026-08-22：INFO-LADDER F1 R02 已完成同 SHA VM 实跑与 V2 重算

- R02 为 `info_queue`（F0）vs `info_physical`（F1）的四格非学习诊断，seed=7/11，唯一干预为 `routing.policy`。三方复核 PASS，PR #138 与 authorization PR #139 均已合入。
- 执行 main exact SHA=`fead4a594a916258b1063ea63621b58076a60b51`；deployment receipt SHA=`636a535ce44824998b4e9fd3cad7dc268f76f4321ce1b47a5e701e737aca3233`；source tree SHA=`39da2af8a3a499675f487ea93dff8b1210080d3762b9a28033eecf500a0a47f6`；authorization SHA=`4d896398c475f461fc8402301fbc1f8de160cb76051825f1abbfe6eea92ad9cc`。
- 4/4 cells 严格串行运行并自然结束，exit=0、守恒通过、receipt verify=`verified`、治理回执 `research_eligible=true`。单进程约满 1 CPU 核，观察 RSS 约 556--657 MB；未形成正式 resource profile。
- V2 `VERIFIED`、`verified_runs=4`；`verify_persisted_analysis(.../analysis-manifest.json)` 返回 `(True, [])`；analysis-manifest SHA=`86133383ae3b18fdcc6990aeb938a22bcb54893540781e625d277335a4c0d491`，summary SHA=`d166e19044028233a81d8b9f31ddc9b27e90b57380fb24c633968b707fd57ae6`。
- delivery-rate paired differences `info_physical - info_queue`=`[0.0, 0.0]`。路线审计：seed 7 路径差异 `125/352=0.3551`，seed 11 `146/401=0.3641`；但两臂包命运完全相同：seed 7 delivered/access_rejected/holding_overflow/in_system=`2382/2597/167/405`，seed 11=`2465/2557/180/389`。
- 边界：F1 确实改变了约三分之一包的 ISL 路线，但在当前压力合同下未改变交付终态；这不是物理字段无效、因果拥塞控制或论文 superiority 结论。下一步是逐向利用率/队列差异与负对照，再做 learner/Q0 归因。
- raw ledger 瓶颈聚合：holding queue area=`5.125385/5.068272` Gbit·s（seed 7/11），ISL data queue area=`0.002320--0.002373` Gbit·s；seed 7 ISL max utilization F0/F1=`0.004831/0.004831`，seed 11=`0.005056/0.005636`，downlink/uplink max utilization 未变（约 `0.0292--0.0297` / `0.0183--0.0184`）。这说明当前压力主要在 holding/access，不足以单独检验 ISL 拥塞控制；下一实验需拆分接入压力与 ISL 压力合同。

## 2026-08-22：E0 load R02 schema-valid authorization chain prepared

- PR #143 合入当前 M-Lab multi-OD + burst 六 cell 矩阵，main merge SHA=`06e195a76639ee33a166b1ea2b8c523ac2b903f2`；PR #144 修复 R02 work brief 的 JSON 尾逗号，main merge SHA=`07e914f4a29375103af548b46fd8bb0a1949cb7b`；PR #145 新增严格 schema 兼容的 R03 authorization brief，main merge SHA=`1ec9a71449c83dbd58c07dc1c7ed4b2bccd73d4c`。
- R03 brief 将 R01/R02 不混算、validity gate、`HOLDING_QUEUE_OVERFLOW / sum(fate_counts)` 分母、pair min-delivery/max-overflow 聚合、互斥穷尽的 load labels 和两 additional-seed confirmation 规则写入 schema 允许字段；R02 request/manifest/config 未改变。
- 三角色 review 已重新绑定 R03 brief 与 R02 matrix 工件；本地 `evaluate_decision` 与 `_load_verified_finalization` 均通过。R02 编译矩阵 authorization 使用 R02 request 固定的 finalization 路径，由 R02 finalization shim 指向 schema-valid R03 brief/decision；不得把 R01 结果混入。
- 当前工作树仍在授权分支，待 commit→PR→CI→合入后，部署 main exact SHA，再严格串行执行六 cell；authorization 尚未作为 VM 运行证据，不能宣称 E0 已完成或已冻结论文负载。

## 2026-08-22：E0 load R02 六 cell VM 扫描完成（候选，不冻结）

- 授权链已修复并合入：当前 main exact SHA=`54f277e68576725b1386c86690940961f2ca5db9`；canonical VM deployment receipt SHA=`f201ae6773fec97d85651b97e59f9c42997ba3721c26f123a0aac31921615bf8`；authorization SHA=`fc1ba2532cd4a02050addf298ec69fd78b9103052843500a2fa38741ee964d59`。本轮使用同一 SHA、同一授权、同一 M-Lab multi-OD + 8--16 s 2x burst 合同，140 星、20 s、MCS、1 s 拓扑重匹配、seed=7。
- 六个 cell 严格串行完成：`low_control`、`low_copy`、`medium_control`、`medium_copy`、`high_control`、`high_copy` 均 remote status=`success`、`exit_code=0`、`natural_end=true`、`conservation_ok=true`、治理回执 `research_eligible=true`，逐个 `receipt verify` 均返回 `verified`。运行中单个 Python 进程约占一个 CPU 核；观察 RSS 约 `0.55--0.80 GB`，这只是工程观察，不是正式逐 run resource profile。
- V2 分析状态=`VERIFIED`、`verified_runs=6`；`verify_persisted_analysis(.../analysis-manifest.json)` 返回 `(True, [])`。analysis manifest SHA=`b57f6bdab64382cff907edeaae566c8629374b4a7c5a1cbe44b81a907413a799`，summary SHA=`e116e86a158129640dc145e76973e6e6a0762401f9024e1d26abb585a089918b`，report SHA=`c856ba4bd0d814089a0e86d567f70ad514ddb9b169b55d6130369acbbd3e9c32`。三组 copy/control 的 paired delivery-rate difference 均为 `0.0`，仅是同 seed/同配置的重复一致性证据。
- 从六个原始 receipt 独立重算的 pair 聚合如下（两臂数值相同）：50 Mbps：`613/1299=0.4719014627`，`HOLDING_QUEUE_OVERFLOW=0`，溢出率 `0`；100 Mbps：`1253/2756=0.4546444122`，溢出率 `0`；200 Mbps：`2382/5551=0.4291118717`，`HOLDING_QUEUE_OVERFLOW=167`，溢出率 `0.0300846694`。所有 cell 均通过 validity gate，未出现零分母、命运计数不一致或守恒失败。
- 预注册分档结果：没有一档达到“低负载”交付率 `>=0.80`；50/100/200 三档均落入“中负载”区间（`0.20--0.80` 且溢出率 `<=0.20`）。按机械规则，最低有效中档是名义 50 Mbps；但因为低负载区没有被扫描出来，不能把这个结果说成最终 E0 边界，也不能用名义 low/medium/high 标签冒充真实三段。下一步先用至少两个新 trace seed 复核 50 Mbps；若仍低于 0.80，再扩大低端 bracket，而不是直接冻结。
- 结论边界：本轮证明了真实 M-Lab 多 OD + burst 合同在当前主线可授权、可在 VM 串行自然结束、可由 receipt/V2 分析重算，且 200 Mbps 开始出现 holding overflow；仍不能支持最终负载阈值、算法优越性、因果拥塞结论、Q0 最优性或论文统计结论。R02 原始结果留在 VM `CODE/Results/`，不入库；本记录只保存可追溯哈希与聚合摘要。

## 2026-08-22：按 VM cgroup 做 CPU/内存资源标定（诊断，不是论文结果）

- 纠正资源口径：宿主机可见 256 CPU/约 628 GB，不能代表用户 VM。canonical VM cgroup v1 实测 `cpu.cfs_quota_us=2400000`、`cpu.cfs_period_us=100000`，即 24 vCPU；`memory.limit_in_bytes=68719476736`，即 64 GiB；`cpuset.cpus=0-255` 仅是宿主机编号集合，不是可用核数。
- 单个非学习 20 s 高负载诊断进程约 14/44/83/122 s 时 RSS=`406/456/524/608 MB`，CPU 约 `100%`；说明 RSS 会随事件/包记录增长，但进程退出后匿名 RSS 回落，未观察到本轮进程级持续泄漏。
- 同配置、不同 CPU 绑定的并行诊断：2/4/8/12 个进程均约各占一个核，单进程中后段 RSS 约 `0.43--0.63 GB`；12 并行时 cgroup 总内存约 7 GB 级别、CPU `nr_throttled` 无新增。输出在 VM `/tmp/leo-resource-profile-*`，不属于 formal results。
- 当前工程建议：非学习先采用 `cpu_per_job=1`、`max_parallel_jobs=12` 的候选调度；学习任务必须另测 TensorFlow 线程池/模型 RSS 后再定，暂不能套用 12 并发。正式资源合同还需对 8/12 并发各做至少三次精确 wall/CPU/RSS/throttle 重复。
- 详细口径、采样值、内存 guard 和边界见 `ANALYSIS/RESOURCE-PROFILE-20260822.md`。本轮不得把宿主机资源、一次性诊断 wall time 或非学习并发结论写成论文性能结论。

## 2026-08-22：V2 外部 launch witness 成为论文分析硬门

- 当前分支继续修复 cold review P1：`pull-results-remote.sh --run/--plan/--all-latest` 对包含 `formal_run.json` 的 V2 结果，按其中的 nonce 从 canonical VM `.remote_runtime/launches/<nonce>.json` 单独取外部状态，保存为 `CODE/Results/_external_launch_witness/<run_id>.json`；不从结果目录生成或替代，且对 nonce、run_id、符号链接和路径穿越 fail-loud。
- `v2_analysis` 对 receipt/v5 + governance/v2 强制读取该外部 witness，验证成功状态、exit code、nonce/run/auth、远端 `last_results_dir`、governance receipt SHA 和五项 governance witness 绑定。v3/v4 只走显式 `legacy_v3_v4_internal_only` 分支，混合 cohort 拒绝，不能冒充 v5 正式证据。
- 本轮 targeted tests 覆盖 external witness 缺失、nonce/run/auth/receipt-SHA 错配、五个 witness 字段各自错配和正常路径；仍需在本分支完成全量测试、cold review、CI/PR 后再部署。

## 2026-08-24：ISL 带宽 R02 两格串行 pilot 完成复审与授权

- 代码与矩阵复核基线为 exact SHA=`4b007bff3969be10e062bad723bdbae0ffd15040`；R02 只比较同一 seed/trace/路由/负载合同下的 ISL RF 带宽 500 MHz 与 50 MHz。三类最终独立复核均 PASS，Kimi 另做只读候选复核；旧 BLOCK 与逐轮修复历史保留在 `pre-fix-review-history.json`，没有被覆盖。
- final brief SHA=`14e33e7f0b95e398acc29cee92871f9598127c37899255320161c8548f065d3d`。固化时实际发现并修复 schema 必需的 `revision_reason` 缺失；措辞经三类 reviewer 与 Kimi 重新确认，区分 R01 初始 blocker 和后续 R02 rereview，且不扩大科学 claim scope。三份 receipt SHA 为 cold-start `675c5baa062202c62cbbe0919550e6d706686f6bfe43dc31da5a480976ca8536`、satellite-DRL `b23983fc4c34e4f908b5b3a4fa8c723f663a9eeab2f9edb8fc0677a38052f75a`、adversarial `451418b03433b77e94b3b28613ccf58490b26a6b4947c4a39ecba2cd68c96f7f`。
- `finalize_decision.py` 返回 `ACCEPTED`；`authorize_experiment` 返回 `AUTHORIZED`（2 runs），authorization payload SHA=`71c3052e1af50475dc31b4c247c91e63475f53572b2e15ab12f61d1c3470f526`。两份 resolved config 均通过运行时授权重算。
- 串行门真实反例符合预注册合同：b500 在无 predecessor 时返回 `READY`；b50 在尚无合格 b500 结果时退出码 2 并 fail-closed。提交前代码全套验证仍需在本治理工件加入后重跑。
- PR #159（`fix: 闭合 ISL 带宽串行实验门`）首轮 required `pytest` CI 已通过，run=`32711384104`、job=`97383326826`。当前仍只是“审阅与授权完成”，尚未合入/部署，也没有 VM 自然结束回执或分析结果；最终 NOTES 提交仍须重新通过 CI 后才可 squash 合并。合入后部署 exact merge SHA，然后严格执行 b500；仅在其 natural end、守恒、governance、nonce witness、部署身份、主指标和 zero-rate gates 全通过后才运行 b50，最后做 V2 持久化配对分析。单 seed 结果不得解释为算法优越性、普适阈值、Q0 或论文统计证据。

## 2026-08-24：ISL 压力 R03 预注册与一秒窗口分析进入精确提交复审

- R02 实测 50 MHz 的最大全程聚合有向 ISL 利用率仅约 2.08%，不足以形成压力。现有 matrix v1 不能让同一 2 MHz cell 同时属于 5→2 和 2→1 两个配对；R03 因此不扩共享对照合同，改为先做 5 MHz vs 2 MHz，只有预注册结果为 `NO_PRESSURE_PHYS_VALID` 才另建 R04 2 MHz vs 1 MHz。
- 新增 receipt-bound 一秒有向 ISL 重算：按原始 service/available 区间的精确重叠分别累计 served bits 与 available capacity，重建已匹配 queue_enter→service_start 的同链路等待；未匹配队列只报告为截尾，不伪造等待。异常容量、重叠服务和 malformed 时间证据 fail-loud。
- 首轮精确提交审阅期间，Codex 自查发现两个会造成假 bracket 的设计漏洞，并在授权前修正：高利用和排队必须重叠于同一持续 episode，不能把同链路不同时段拼成拥塞；5 MHz 对照也必须按同一规则证明无压力，不能只看 2 MHz 候选。`pressure-decision.json` 现冻结五类动作：`PHYS_INVALID`、`DRAIN_INCOMPLETE`、`CONTROL_PRESSURE_UNBRACKETED`、`PRESSURE_CANDIDATE`、`NO_PRESSURE_PHYS_VALID`。只有“5 MHz 无压力、2 MHz 有同 episode 压力”才允许称 5--2 MHz 候选区间；5 MHz 已有压力则停止并回到上侧 bracket。
- Kimi 两路旧提交审阅均给出 `PASS_WITH_LIMITS`；Codex 独立裁决后接受并修复显式 drain 字段、episode 时间对齐、事件时间界、service-start/service-window 身份交叉核对、阈值双源漂移和人工分类风险，新增受测五路 pair classifier；拒绝“非零 MCS 低速必属物理失败”的泛化，因为 `min_rate_bps` 在当前实现中是零速率截止门而非正速率地板，合法非零容量上的持续占满与同时排队正是待寻找的 ISL 压力。当前相关测试扩至全套 `706 passed, 2 skipped, 3 subtests passed`；旧评审及裁决保留在 R03 candidate review history，新 exact commit 仍须重新审阅后才能授权。
- 编译验证为 2 cells / 7 hashes，逐字段差异只有 `links.rf_isl.bandwidth_hz`；两格 trace identity、input 和 controlled signature 一致。当前全套测试 `692 passed, 2 skipped, 3 subtests passed`，document governance `0 errors, 0 warnings`，`git diff --check` 通过。
- 当前状态仍是 `COMPILED_REVIEW_REQUIRED`：尚无 R03 独立三角色 PASS、finalization、authorization、main 合入、部署或 VM 结果。下一步先让 Kimi 对精确提交做只读挑错，再由 Codex 复核并完成正式独立审阅；任何 blocker 都在授权前修正。

## 2026-08-24：R03 决策合同与操作手册形成可重编译闭环

- Kimi 在 exact commit `e1106c883b16d03eb3ee8ae49c5c50404d0d1176` 上完成 satellite-DRL 与 cold-start 只读复核，均为 `PASS_WITH_LIMITS`；Codex 接受两个窄问题：生成的 RUNBOOK 漏掉持久化分类命令，以及“5 MHz 已有局部压力时优先停止”与“未定位 ISL overflow 阻断”的文字优先级不够明确。旧复核只作为修订依据，不能授权新提交。
- matrix request 的 `analysis.decision_contract` 现在显式绑定冻结决策合同；编译器读取并校验安全的 canonical `python -m` 命令，把合同路径、SHA-256 和命令写入分析请求与 RUNBOOK。验证器重新读取合同并重算身份，同时从请求重新渲染 RUNBOOK 逐字比较；即使同时伪造 RUNBOOK 与编译报告中的哈希也会 fail-loud。授权工件映射也包含该外部决策合同。
- 分类行为、五分支顺序、阈值、5/2 MHz 场景和矩阵规模均未改变。新增回归覆盖“5 MHz 已有局部压力 + 2 MHz 未定位 ISL overflow”仍停在 `CONTROL_PRESSURE_UNBRACKETED`，以及持久化分析验证失败时分类器拒绝输出。
- R03 已在一次性副本中由 canonical matrix compiler 重编译并与工作树逐文件同步；两个 resolved 配置内容哈希保持不变。`verify_compiled_matrix` 返回 2 cells / 8 bound hashes，其中包含 decision-contract SHA `fa0493b722e3bd119ed516543e4429b2bbc30986d3e5479f24f4d81f5194460e`。
- 本地证据：全套 `712 passed, 2 skipped, 3 subtests passed`；document governance `0 selected errors, 0 warnings`；`git diff --check` 通过。当前仍未生成正式 review receipts、finalization 或 authorization，未合入、部署或运行；下一步将本修订提交推送后，对新的 exact commit 重新做 cold-start、satellite-DRL、adversarial 三类复核。

## 2026-08-24：R03 精确提交三方复核完成并生成两格授权

- 最终承重代码与冻结工件基线为 exact commit `95d28051696ccaa6e75a46bb552e60874f5da256`。cold-start、satellite-DRL、adversarial 三类 Kimi 只读复核均返回 `PASS_WITH_LIMITS`，会话分别为 `session_46138f46-c820-4fed-9376-c1b249daf30e`、`session_1b4c85bd-b97b-4802-9952-976150af8169`、`session_d06fa03e-ca73-43c8-ae65-5449e9977d75`；Codex 独立复核后确认无 blocker，不把 worker 结论直接当正式证据。
- 三份正式 receipt 均绑定同一组 26 个 exact artifact hashes，SHA 分别为 cold-start `6621b43ca1649892805d3932a022db8ab579225e88e6e5c99fe93d751a77c7bf`、satellite-DRL `051c820e198a43b4d08c1c95f4eac58c347f359067ea526a3b40f5b46f64c056`、adversarial `9a29c1df83ab01761f1d5702dfbd5c03f612ad04bcd397e855b645388ad2d663`。`finalize_decision.py` 返回 `ACCEPTED`；decision SHA=`036af4674b30e7fa5697f2bd3f89396a7cb36e5f7014e0e70f5acf8d099e0971`，finalization SHA=`c9cbb6b866d143e2faca4d195494b40ede9bb318c84a5af2caf76afb546901d3`。
- 已生成 R03 两格派生授权：`authorize_experiment` 返回 `AUTHORIZED`（2 runs），authorization SHA=`22bf215289ae2a04db63b81ec354b3bf0f43663a8643ed5bb367b41b772329a3`，payload SHA=`c1077db863c9d87552cc5a99daaeec0a4d211d2a7a385851ea9288d4a6709e12`；重新验签通过，首格 b5 的串行门为 `READY`、predecessors 为空。
- 非阻断限制仍保留：少数畸形 persisted manifest 会以裸 traceback 而非干净错误信封失败，但不会写出分类；零时长 interrupted service 可锚定真实 queue wait，但不贡献利用率且没有专项回归；episode 边缘重叠的完整 wait 与 episode 内面积是预注册的不对称。任何正式分类错误、未定位 overflow、物理无效或未排空都必须停止，不能改写成 no-pressure。
- 当前只完成了“承重版本复核 → 治理定案 → 派生授权”，尚未 PR/CI 合入、clean-main 部署或执行 VM。下一步提交本治理包并经 required pytest CI 合入；部署 exact merge SHA 后严格串行运行 b5，只有其 natural end、守恒、治理、外部 witness、身份、ISL 指标和 zero-rate 门全通过才允许 b2。单种子分类不能直接进入论文或算法比较。
- PR #163（`fix: 闭合 ISL 压力标定与串行授权`）首轮 required `pytest` CI 已通过，run=`32742920625`、job=`97481422740`。本条 NOTES 留痕提交后仍须重新通过 required CI 才可 squash 合入；截至本条记录仍未部署或执行 VM。

## 2026-08-24：R03 正式运行定位到 5--2 MHz 单 seed 压力候选

- PR #163 已经 required CI 通过并 squash 合入 main，执行 exact SHA=`0280de3ba0e27551bc7a737a028f5154743051ce`；main 合入后 pytest job `97482210294` 成功。canonical VM 部署 source tree SHA=`ade9dd4e5221fd57b025428965058721de5369189596fcbe3b75f028f1db152a`，deployment receipt SHA=`393b812b2eb8d10cac8be9f7cfc574223bbb3054ab6b0fbebdbfb94e3320bfec`。
- 5 MHz 与 2 MHz 两格严格串行自然结束，exit code=0、conservation=true、governance `research_eligible=true`，外部 nonce witness 与 VM 原始 Python 3.11.15 环境 receipt verification 均通过。governance receipt SHA 分别为 b5 `a0246e850ccf3c4f3de8fe6f3787559c8a5253479cea90964df24c1c573d9639`、b2 `1dad81f86c4f37661dc5d15ddc0c1bc86718e4d620a27d7bd2f3b6122f988271`。
- V2 analysis 为 `VERIFIED`、2 runs，persisted verification 为 `ok=true/errors=[]`；analysis manifest SHA=`5ee795b366b87977cb27bb2e4e90504791b4c8273592b687c8face1e416429d7`。全运行期最大有向 ISL 利用率为 5 MHz `0.15252027036759927`、2 MHz `0.3813006759189982`，配对差 `0.22878040555139892`。
- 冻结五路分类器返回 `PRESSURE_CANDIDATE`，classification SHA=`c0075a3647f4f821bf043e734a6c2ffec9dd8984e4da82e4d0f5a477b56cf5b8`。5 MHz 无合格 episode；2 MHz 在 `isl:147:167`、`isl:167:187`、`isl:222:242` 上形成连续 4/5/4 个一秒高利用窗且同 episode 有匹配排队，最大等待约 5.130/0.336/0.784 s。两臂均为 1,295 delivered、4 `NO_ROUTE`、59 access grants、0 zero-rate holds、0 ISL overflow、0 data in-system at stop、0 unmatched ISL queue entry，control failure counters 也相同，因此未观察到由接入差异、断链增长或未排空伪造的臂间压力信号。
- claim 边界：这只把 5--2 MHz 冻结为固定场景、seed 7 下的工程 onset 候选，不是普适阈值、纯容量效应、信息价值、算法优越性、Q0 或论文统计结论。按预注册动作停止降低带宽，不运行 1 MHz；下一步先独立审阅并预注册相邻 5/2 MHz 的 seeds 11、19 复核，总计三个 seeds，方向不一致必须如实报告。
- 执行中有一次准备阶段 fail-closed：默认远程 Python 未进入正式 TensorFlow 环境，仿真未启动、无结果目录。显式绑定 formal VM Python 后，同一授权与部署上的前驱验证和正式运行均通过。该事件不污染结果，但默认解释器/环境激活不一致仍是平台可用性缺口，应在独立小修复中加回归并闭合。
- 结果提交 `dd892b3a…` 的两路 Kimi 冷审均为 `PASS_WITH_LIMITS`、无 blocker。Codex 接受阈值邻接限制：5 MHz 存在约 0.9675 的单高窗与最多 1.941 s 的匹配等待但不满足连续窗规则；2 MHz 的 `isl:187:207` 有 5 个连续高窗但最大重叠等待约 0.0807 s，距 0.1 s 门槛仅约 0.0193 s。因此链路数量和控制臂无压力都不能外推为稳定结论，seeds 11/19 必须逐分支报告、禁用多数票。
- 本地确认 `0280de3…` 是结果提交祖先，四个 analyzer 文件在两提交间无差异且哈希与 manifest 完全一致。结果提交因 Git identity 改变而按设计拒绝原地重放；在 exact 源提交、VM 正式 Python 3.11.15、原始结果与外部见证上重跑成功，classification 仍为 `PRESSURE_CANDIDATE`，SHA 仍为 `c0075a36…`。

## 2026-08-25：远程正式准备检查统一使用已激活环境

- R03 暴露的启动缺口已复现到 `run-remote.sh`：tmux 内的正式子进程会先执行 `REMOTE_ENV_ACTIVATE`，但 tmux 外的 `remote_job.py prepare` 直接调用 `REMOTE_PYTHON`，因此配置为 `python3` 时会落到未激活的系统解释器，并在仿真启动前因缺少正式依赖 fail-closed。
- 本修复只在远程 prepare/fail 所在的同一 shell 中、执行 prepare 之前加入现有 `REMOTE_ENV_ACTIVATE`；正式 tmux 子进程的激活与执行逻辑不变，实验参数、授权、回执和分析语义均未修改。
- TDD 证据：新增 shell 模板回归先在当前代码上以 `substring not found` 失败，随后最小修复转绿。两轮两路 Kimi exact-commit 冷审均为 `PASS_WITH_LIMITS`、无 blocker；Codex 接受其“纯字符串断言可被注释伪装、未覆盖 fail/tmux、外层未锁定严格错误模式先于激活”意见，把回归加固为只认未注释独立命令行，并同时锁定外层 `set -euo pipefail → activation → prepare → fail` 与 tmux `set -euo pipefail → activation → run`。`bash -n` 通过，定向 `2 passed`，全套测试为 `714 passed, 2 skipped, 3 subtests passed`。当前最终修订仍需 PR/CI 合入和 clean-main 部署，不得写成默认远程路径已正式闭环。

## 2026-08-28：全球压力实验授权链合入后补齐标准启动路径

- PR #169 经重新触发 required `pytest` 后通过（run `33157858299`，job `98804853217`，约 9m6s），已 squash 合入 main，merge SHA=`2009e1c75fab50f7c441ce5a8dd57aeba4ae6d57`。该 PR 只闭合三类复核、decision、finalization 与派生 authorization 证据，不代表 VM 已部署或实验已运行。
- 合入后启动前检查发现：RUNBOOK、`run-remote.sh` 与 `v2_serial_gate` 均要求 `EXPERIMENTS/<experiment_id>/authorization.json`，但 PR #169 只保存了 `CODE/work/.../authorization.json`，正式命令会在仿真启动前 fail-closed。PR #170 将已审核 authorization 按原字节补入标准实验目录；两文件 `cmp` 一致，`verify_authorization` 返回 `AUTHORIZED`（2 runs），首格 serial gate 返回 `READY`。旧 work 工件保留，未删除或移动。
- 当前仍未部署 PR #170 的最终 main，也未启动全球压力 cell；只有 PR #170 CI 通过并合入、合并后 main CI 绿、canonical VM 部署回执绑定该 exact SHA 后，才允许严格串行启动 `load10_a`、核验自然结束与场景分类，再决定是否启动 `load10_b`。

## 2026-08-28：覆盖审计跨环境末位舍入误报修复

- 全球压力首格自然结束后，冻结 coverage ledger 的 16,988 个区域重新求和得到 `0.8600828566012921`，审计生成环境保存的汇总为 `0.8600828566012908`；差值约 `1.33e-15`，原 verifier 因逐位相等要求误判无效。
- 本修复仅把两项人口加权比例的复算比较改为绝对误差 `2e-15`；候选区域、人口、逐区域可见率、总数、哈希和其他字段仍逐项核验，明显篡改 `1.0` 的既有反例仍拒绝。实验配置、场景阈值、授权和结果均未改动。
- TDD 证据：新回归在修复前按预期失败，修复后 `test_coverage.py` 为 `14 passed`、`test_scene_check.py` 为 `15 passed`；冻结全球 coverage audit 的 L1 复核返回空错误列表。仍须 required CI 通过并合入 main 后，才能作为正式分析路径使用。
