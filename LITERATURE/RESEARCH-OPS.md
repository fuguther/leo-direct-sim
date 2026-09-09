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
