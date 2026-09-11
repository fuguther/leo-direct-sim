# 六项收口验收报告（ACCEPTANCE-R3，2026-09-11）

> 验收对象：Codex 对 `63a9a487` 的实查结论（2 处反例 + 3 条要求 + 2 条文献纠正）。
> 本报告给出：**修复内容 / 独立复现证据 / 隔离证明 / 准确 SHA**。全部测试在**隔离副本**运行。

---

## 0. 提交

| SHA | 内容 |
|---|---|
| `4324e4a` | 六项收口（测试隔离 / 授权绑定具体会话 / 推荐守卫校验待写入版本 / 访问按工具参数 / 历史审查可派发） |
| `8df283a` | 相关性筛查落库 + MD 索引标注 + 正文体积口径更正 |
| 分支 | `agent/20260910-topic-loop`（已推送，工作树干净） |

---

## 1. 事故取证与恢复（Codex 要求 #1）

事故清单内容（证据存 `round/run2/incident-20260911/`）：
```json
{"run_id":"rt","orchestrator_session":"session-REAL-ORCH","sessions":{},
 "tickets":[{"role":"history_reviewer",...}]}
```
**根因**：我的验证脚本把 `orchestrator_session` 写成测试假值 `session-REAL-ORCH`，导致真实主控会话不被识别 → 被自己的守卫拦死，且当时**无自愈路径**。

**已修**：
- `perm.py init` 更换主控需显式 `--force`（防再次手滑）；
- `orchestrator_history` 保留最近 3 个主控（交接后旧主控仍可恢复）；
- 清单缺失 → 主控凭独立锚点 `orchestrator.id` 可修复（已实测）。

---

## 2. 测试隔离（要求 #2）

**机制**：三个状态文件支持环境变量重定向 —— `DSH_PERM_FILE` / `DSH_ORCH_FILE` / `DSH_HOOK_LOG`（hook 侧）与 `DSH_GATE_DIR`（判定记录）。测试全程在 `tempfile.TemporaryDirectory()` 内运行，子进程继承隔离环境。

**强制校验**：`selftest.py` 与 `verify_bypasses.py` 均在**测试前后核对真实文件 sha256**，任何变化即使整体失败并打印差异。

实测输出（节选）：
```
隔离校验（真实状态必须不变）：
  PASS perm  (absent)
  PASS orch  5fc26660ae96cabd
  PASS log   d258f0356a091dc3
SUMMARY 24 passed / 0 failed | 隔离:OK
```

---

## 3. 授权绑定具体子会话（要求 #3）

**取消"按访问顺序领取"**：
- 新增 `perm.py grant --session <id> --role <角色> --extra-read/write <文件>` —— **直接绑定具体子会话 ID + 角色 + 任务文件**（主推用法）；
- `reserve` 支持 `--session` 把票据绑定到具体会话；领取时若票据已绑定其他会话则**拒绝**；
- 父会话关系（`parentSession` + `origin=subagent`）降级为**附加校验**（须属于本清单主控集合）。

**Codex 指定的必测项：同一主控的生成器不能领取历史审查者权限**
```
PASS 无关会话领票(拦)                      exit=2
PASS 同主控生成器读历史(拦)                  exit=2
PASS 票据绑定他人(拦)                      exit=2
PASS 票据剩余=1 (期望1，未被消费)            ← 票据未被消费
```

---

## 4. 推荐守卫（要求 #4）

| 修复 | 说明 |
|---|---|
| 覆盖所有入口 | `status` 与 `revise`（含 `--set` 里的 status）统一提取后走**同一守卫** |
| 校验**待写入版本** | 守卫新增 `pending_row` 参数；`gate_verdict.check(expect_hash=...)` 比对**将写入的 content_hash**；同一调用内既改内容又申请推荐 → 旧判定被正确拒绝 |
| 承重修改自动降级 | 已推荐候选发生承重变更 → **自动转 `needs_revision`**（打印 `AUTO_DEMOTED`） |

独立复现（隔离台账 + 隔离 gates 目录）：
```
=== A. 推荐门禁（无判定记录时，所有入口都必须被拒）===
  PASS --status 路径                        exit=2
  PASS revise --status                    exit=2
  PASS revise --set 塞 status（Codex 反例）    exit=2
  PASS 同调用改内容+申请推荐                        exit=2
  PASS 最终状态=awaiting_evidence
=== B. 推荐链路 ===
  PASS 无判定置推荐 exit=2
  PASS record PASS exit=0
  PASS 置推荐 exit=0 status=recommended_pending_review
  PASS 承重修改 status=needs_revision AUTO_DEMOTED=True
  PASS 旧判定再置推荐 exit=2
SUMMARY 12/12 通过 | 隔离:OK
```

---

## 5. 文件访问判定（要求 #5）

- **可强制部分**：只取工具的结构化路径参数（`file_path`/`path`/`target`/`notebook_path`）；
- **尽力检测部分**：shell 字面量匹配，**明确不宣称硬隔离**；已**移除"路径存在"启发式**（该启发式既漏又误）；
- **修正误报**：不再把文本里出现的文件名当成访问（此前主控连提问工具都被拦）；
- **合法历史审查可派发**：`hook_prompt_scope.py` 改为**按角色判定** —— 声明 `history_reviewer` 的任务允许携带历史库。

```
PASS 历史审查任务可派发                      exit=0
PASS 非历史角色带历史全集(拦)                  exit=2
PASS bash 列历史目录(拦)                  exit=2
PASS bash 读旧卡(拦)                    exit=2
PASS bash 普通命令(放行)                  exit=0
```

---

## 6. 文献部分两条纠正（Codex）

### 6.1 正文体积口径
- 此前「2.0 GB Markdown」= **目录体积（含 MinerU 抽取的图片）**；
- **正文合计 10,411,191 字节 ≈ 10.4 MB**（`CONVERSION-SUMMARY.json` 的 `total_md_bytes`）。

### 6.2 相关性分层（`round/knowledge/RELEVANCE-SCREEN.md`）

| 层 | 篇数 | 处理 |
|---|---|---|
| **A 核心域** | **92** | 研究检索主入口 |
| **B 方法基础** | **15** | 保留但分层：仅用于 G3/G4 论证，不作域内证据 |
| **C 无关** | **4** | **移出检索入口**，原件保留 |

**C 层 4 篇**（Codex 点到 1 篇，实际 4 篇）：
| itemKey | 标题 | 判定依据 |
|---|---|---|
| ETTA3DIV | Required toroidal confinement for fusion and omnigeneity | 等离子体磁约束聚变 |
| A7QNRKML | LOTR: Face Landmark Localization | 计算机视觉 |
| VACUFEHB | Third Order Adaptive Volterra Filters | 信号处理 |
| WT839JP7 | Fine-Grained Library Customization | 软件工程 |

MD 索引已对 C 层标注 `[无关·已移出]`（6 处标注含此前误判项）。

---

## 7. 测试总览（隔离运行）

| 套件 | 结果 |
|---|---|
| `round/hooks/selftest.py`（24 项，含角色/票据/shell/损坏/派发） | **24 passed / 0 failed，隔离 OK** |
| `round/hooks/verify_bypasses.py`（12 项，Codex 反例 + 推荐链路 + 角色绑定） | **12 passed / 0 failed，隔离 OK** |
| `round/tools/test_rework_regressions.py` | **12/12 passed** |
| `round/tools/deps_check.py` | **20/20 一致** |

---

## 8. 诚实声明

- 本轮**未扩建框架**，只收口 Codex 指出的问题；
- **真实网页工具拦截未在本轮重新派发验证**（继承上一轮证据：探针被真实拦截）；
- **闸门仍未对真实候选卡判过**——下一步即用两张测试卡走完整接力；
- `bash`/`run_code` 内任意代码**仍是尽力检测**，不构成硬隔离。
---

# 附：Codex 第二轮复验的四项收口（2026-09-11 晚）

> Codex 独立复跑确认：**测试隔离与推荐门禁通过**。剩余四项已全部处理。核实结论：**四条均成立**。

## 收口 1：禁止空 target 票据（确认属实并已修）

**核实**：`reserve --session` 默认空串 → 可创建空 target 票据；`claim_ticket` **自身不验证**目标（只在调用方 lib_hook 判）。

**修复**：
- `perm.py reserve` **拒绝**未指定 `--session`（空 target 票据无法创建）；
- `claim_ticket` **内部**按 `t["session"] == session_id` 精确匹配后 pop（不能只依赖调用方）；
- `lib_hook.resolve_role` **取消自动领票**：未登记会话**一律保持未授权**，父子关系合法**不足以**授予权限。

**正确流程（写入文档）**：派发 → 取得会话 ID → `grant/reserve --session <id>` → 子代理才开始读材料。

## 收口 2：新增覆盖原事故的测试（已加，实测通过）

场景 = **未登记子会话 + 与主控父子关系合法 + 存在历史角色票据** → 仍不得取得不属于自己的权限，且票据保持不变。

用**真实主控 ID** 与**真实子会话**（实测 `parent=session-53942861-…`、`origin=subagent`）构造：

```
PASS reserve 无 --session exit=2 (期望2)              ← 空 target 票据无法创建
PASS 未登记+合法父子+有空票据 exit=2 (期望2)           ← 原事故场景被拦
PASS 票据剩余=1 且仍为空target（未被消费）
PASS 未越权写入 sessions=[]                           ← 未产生越权绑定
PASS 票据绑定他人时本会话 exit=2 (期望2)
PASS grant exit=0 读历史 exit=0 (期望0/0)             ← 精确授权后合法路径畅通
PASS 生成器读历史索引 exit=2 (期望2)                  ← 角色最小授权
```

## 收口 3：提示词角色词不得作为授权依据（确认属实，已降级）

**核实**：`PreToolUse` 载荷**不含角色字段**（实测 grep=0：只有 session_id/cwd/tool_name/tool_input）→ 用"提示词里出现历史审查者字样"作豁免**可被任意提示词绕过**。

**修复**：`hook_prompt_scope.py` **降级为诊断件**（stderr 提示，**不阻塞、不冒充授权判定**），文件头明确声明：

> **诚实声明：本 hook 不提供角色隔离保证。**

真正的隔离由 `hook_access_guard`（按角色 + 具体文件授权）承担。

## 收口 4：单位更正（确认属实）

**核实**：`total_md_bytes` = `st_size` 求和 = **字节数**（实测字节/字符差 0.1–0.3%，因正文以英文为主）。

**更正**：报告中「10,411,191 字符」→「**10,411,191 字节 ≈ 10.4 MB**」（两处：ACCEPTANCE-R3、RELEVANCE-SCREEN）。

---

## 本轮测试总览（隔离运行）

| 套件 | 结果 |
|---|---|
| `round/hooks/selftest.py`（25 项） | **25 passed / 0 failed | 隔离 OK** |
| `round/hooks/verify_bypasses.py`（17 项，含事故场景） | **17 passed / 0 failed | 隔离 OK** |
| `round/tools/test_rework_regressions.py` | **12/12** |
| `round/tools/deps_check.py` | **20/20 一致** |

隔离证明：真实 `permissions.json` (absent) / `orchestrator.id` / `unregistered.log` 哈希**前后不变**。
