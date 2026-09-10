# 研究证据脚手架 v1

> CURRENT-CONTRACT：本页定义文献证据记录与交付接口。研究方向与内容裁决以 `README.md` 和用户当前任务为准。

## 职责与存放

项目技能 `.dsh/skills/leo-research-ops/SKILL.md` 按任务加载短规范；`scripts/research_ops.py` 用 Python 标准库实现本地版本化证据存储；`scripts/research_ops_hook.py` 是可选的 Harness CC PreToolUse 适配器。Zotero管理书目/附件，本工具是证据 sidecar，不另建自动下载库。

数据放在被忽略的 `out/research-ops/` 或本地研究目录；PDF、MD、笔记正文和审查结果不提交公开 Git。原输入只读，按 SHA256 保存 blob。`state.json` 是当前快照；`history/` 保留旧快照。失败事务可留下无引用 blob，不影响当前状态，不自动删除。

## 命令与数据合同

```sh
python3 scripts/research_ops.py --store out/research-ops status
python3 scripts/research_ops.py --store out/research-ops apply /absolute/path/patch.json
python3 scripts/research_ops.py --store out/research-ops validate
python3 -m pytest CODE/tests/test_research_ops.py -q
```

补丁：`expected_revision`、`actor`、`reason`、`operations`。先读取 revision 再构造补丁；冲突须重读合并，不能改数字盲重试。机器可跑例子见测试 `EvidenceTests.setUp`；真实论文演示记录保存在本地数据目录。

弱模型默认不手写完整事务补丁。阅读 worker 先提交一个小型“语义候选”：`statement`、`scope`、`verbatim`、`locator`、支持判断、与现有主张的重复性判断和 caveat。主控回到原文核查内容价值，随后才把获准候选规范化为下表字段，补齐 read/note 继承关系、受控枚举、路径、哈希和 revision，并在隔离副本 apply+validate。语义正确但重复的主张应判 revise/reject；机械校验通过不能替代内容审核。

| 操作 | 核心字段与行为 |
|---|---|
| paper | id/title/metadata_source，doi 可选，规范化并拒绝重复 DOI；无 DOI 身份人工核验，Zotero/其他标识可附存 |
| source | id/paper_id/path/sha256/media_type/version/origin/identity_status；checked 附 identity_by/identity_basis；PDF 附 pages；代码附 exact commit |
| derived | id/source_id/source_sha256/path/sha256/parser/parser_version/parameters/defects/page_convention/binding_status；checked 附 checked_by/binding_basis。MD与页映射JSON分别登记 |
| read | id/source_id/source_sha256/session_id/question/mode(original/derived/both)/truncated/unread/coverage；身份/方法/结果/限制各有status及locators；派生层附derived_id |
| claim | id/paper_id/source_id/source_sha256/statement/scope/support/interpretation/evidence_type；已核状态附read_id、checked_by/checked_at/basis及read已核范围内locator。图附value_method，估读附digitization_note |
| activate_source | paper_id/source_id：明确切换当前依据才把旧源相关主张和直接依赖任务标needs_recheck |
| note | paper_id/parent_note_revision/path/sha256/claim_ids/reason；追加正文快照，claim纠正另加新记录并用supersedes关联 |
| task | id/worker_session/question/claim_ids/execution=queued；只跟踪直接claim依赖，不替代Harness调度 |
| task_transition | task_id/execution/resume_from；delivered附artifact_path/artifact_sha256；ready为内容待审，不是用户已接受 |
| review | id/task_id/reviewer_session/verdict/rationale/artifact_sha256；accept/revise/reject/unavailable都是可记录结果，拒绝不是执行失败 |

support=unverified/supported/partial/contradicted，与 interpretation=author_report/our_inference/hypothesis 分开。checked 是核验人的声明，程序不认证科学正确。页数与论文身份须回原文核验；错误MD靠hash/关联检查与原页核对共同防止，不声称仅凭hash能识别错文。

待复核恢复采用追加式：重新核验后建立新read和新claim（supersedes旧claim），建立引用新claim的新task，并更新本地binding。v1不把旧任务原地重新认证为current，保留其当时证据和审查历史。

## Hook接线

适配器只处理 `PreToolUse` 的 `update_goal(action=complete)`：检查绑定任务是否交付、审查有无结果、产物与依赖是否有效。reject允许结束执行；不拦pause/blocked；不配置Stop无限续跑。

本地bindings JSON格式：`{"sessions":{"实际session_id":{"cwd":"绝对工作区","store":"绝对证据库","task_id":"实际任务ID"}}}`。未绑定会话不受影响。以下处理项置于`hooks.PreToolUse`数组，由Harness的`dsh-hooks-claude-code`显式加载配置：

```json
{"matcher":"^update_goal$","hooks":[{"type":"command","command":"python3 /ABS/REPO/scripts/research_ops_hook.py --bindings /ABS/LOCAL/bindings.json","timeout":10}]}
```

文件在位不等于hook生效。验收分三层：命令输入输出；已安装桥的typed deny/next；真实profile会话。桥遇加载失败可能不注册，必须核验。全局profile不由此脚本自动修改。

## 可靠性与边界

flock+expected_revision串行合并，先校验、保留旧快照再原子替换。校验关联、定位、文件hash及审查产物；不是全文理解器。

worker若有任意shell写权限，就能绕过脚本或伪造session，这些是防误操作机制而非隔离安全系统。用户接受与关键内容审查仍由主控负责。v1未实现跨任务DAG传播、自动唤醒、Zotero写回、全文覆盖语义识别，不宣称完整科研自动化。

真实验收显示，要求 Flash worker 同时阅读、判断并拼装完整事务补丁会产生明显无效推理开销；语义候选接口是默认路径。完整补丁只适用于已有固定模板的机械执行任务。

## 可见运行适配：开发中，尚不可启动真实研究

`scripts/research_harness.py` 通过本机 Harness 的 `/api/session/*` RPC 管理会话，
不写会话数据库。`probe` 只读列出会话；`prepare --root <目录>` 创建总会话和阶段会话，
统一 cwd 并逐一检查 list/page 可读；`reconcile` 只读对账；`cancel` 保存停止请求后
逐会话取消。API 可读不是网页像素验收，取消请求确认不是任务已经停止。

认证由调用方通过 `RESEARCH_HARNESS_COOKIE` 注入内存；禁止将 Cookie 写入日志或提交。
当前匿名本机接口实测 401，尚未验证认证后的网页链路。不要从数据库复制认证信息。
`selectModel` 的已装实现同时保存部署默认选择，因此本适配器暂不调用它，避免改变
用户其他任务的默认模型。总任务与阶段的关系目前只记录在 VISIBLE-RUN.json 中，
尚未实现网页原生父子层级和总任务停止传播。

授权文件须包含 provider/model/destination/project_cwd、expires_at（含时区）、
budget_fen（正整数，最大1000）、source_scope_sha256、plan_sha256；PLAN.json 中
对应值必须一致。旧夜跑授权不自动迁移到新任务。授权与文件指纹仅用于检测变化，
不宣称不可篡改。SOURCES.md 列表仍是任务合同，不是文件访问沙箱。

预算 SQLite 账本原子预留单请求最大费用（分），并发共享，重试使用新的请求ID。
未知响应保留全额预留；相同请求ID禁止再次发送；结算幂等，超出预留记录实际费用并冻结。
这是账本单元，不是已部署的费用熔断。源码存在 `llm/stream` waterfall 接入点，
但请求级插件、实际目的地绑定、计费上限、重试覆盖均未联调；不得用调用后 usage
统计代替发送前限制。所有真实 prompt admission 当前明确阻止，旧 research_night.py
CLI 也禁止自动回退 headless。显式 command 参数仅保留已有模拟回归调用。

故障恢复：先保留 RUN/回执/SQLite 和会话ID，再执行 reconcile。网络结果不明时
不重发；取消失败记 cancel_unconfirmed 并再次核查；.visible-owner 是崩溃占用标志，
禁止自动删除。输出写入失败停止流程，不覆盖旧交付。恢复真实研究前必须完成：
认证接口与网页打开验证、请求级预算/路由插件、停止事件传播及两阶段真实接力验收。

回归：`python3 -m unittest discover -s CODE/tests -p 'test_research*.py' -q`。
本轮真实模型调用0次；未使用10元联调预算。旧夜跑产物保持原样。
