# Hook 套件 v2（按 Codex 三项收口重做，2026-09-11）

> 状态：**已按 Codex 实测收口；未挂载**（用户决定不全局挂载）。所有脚本在本 worktree 内，零系统改动。
> 取证依据：`HOOK-CONTRACT.md`（hook 载荷字段、沙箱能力、三个反例复现）。

---

## 1. 能力分级（**先说边界，再说功能**）

| 访问方式 | 约束级别 | 机制 |
|---|---|---|
| `read`/`read_document`/`glob`/`grep` 等工具路径 | ✅ **可强制** | 载荷里有结构化路径 → realpath 归一化 → 角色授权表 |
| `write`/`edit` 工具路径 | ✅ **可强制** | 同上（写权限须派发端显式授予具体文件） |
| 越权**写**（沙箱外） | ✅ OS 级 | 现有 workspace-write 沙箱 |
| `bash`/`run_code` 内任意命令与代码 | ⚠️ **仅尽力检测** | 字面路径匹配；**任意 shell/Python 可绕过，不构成硬隔离** |
| 越权**读**（任意路径只读） | ❌ **不可约束** | 沙箱只限"写"范围；root 全盘 ro-bind → **读隔离在现有接口下不可得** |
| 角色/父会话身份 | ❌ 载荷不提供 | 只能由**派发端显式登记**（见 §3） |

**因此本套件的定位是**：把"可机械判定的路径类违规"从文档变成拦截；**不宣称**对任意代码的硬隔离。

---

## 2. 三个收口点的落实

### 收口 #1：角色权限（原缺陷：所有子代理同一对待，正常接地被拦）

- 新增 `perm.py`：run-scoped 权限清单，把 **角色 → 读/写范围** 绑定到运行时 `session_id`；
- 角色五类：`generator`（读中性资料，写**被授权的具体文件**）、`deepener`（读指定卡+反馈）、`history_reviewer`（读历史库与旧卡）、`reviewer`、`auditor`；
- **身份只认 `session_id`**：不再用任何环境变量判定；实测子代理**不会继承**父会话的 `DSH_HOOK_ORCHESTRATOR`（探针验证 ORCH=(empty)），且即便手工注入该变量，子代理仍按角色拦（用例通过）；
- **写权限改为必须显式授予**：真实身份测试发现"生成器可写 staging 下任意文件"（可覆盖他人卡）→ 已把 base write 置空，要求 `--extra-write` 指定确切文件。

### 收口 #2：实际访问边界（原缺陷：换写法就绕过）

- 路径统一 `realpath` 归一化：`./`、相对、绝对、符号链接 → **同一判定**；
- Codex 三个反例全部修复：`cat round/run2/...`、`./round/run1/...`、`open()` 读旧候选；
- **不再堆正则**：`bash`/`run_code` 明确降级为"尽力检测"，README 与本文件均标注，不再宣称硬隔离；
- 工作区外高危目标（`~/.dsh/sessions/`、其他 worktree、旧仓库）单独拦截。

### 收口 #3：推荐检查绑定台账（原缺陷：检查"目录里有什么"）

- **删除** `hook_delivery_gate.py`（扫目录式，会被无关 TODO 放行、被无关 BLOCK 误拦）；
- 新增 `round/tools/gate_verdict.py`：判定记录绑定 **候选 ID + 当前 content_hash + 卡文件 sha256**；
- **接入台账**：`ledger.py status --status recommended_pending_review` 现在强制校验该绑定；不通过即拒绝（`REJECTED`）；
- 实测五条路径：无判定→拒、BLOCK→拒、PASS→过、**卡改动后→拒（版本失效）**、无关候选的草稿/淘汰写入→正常；
- `hook_ledger_diagnostic.py` 由门禁降级为**事后诊断**（解析失败→记录并放行），不声称自动纠正。

---

## 3. 现行文件

| 文件 | 类型 | 作用 |
|---|---|---|
| `perm.py` | 工具 | 权限清单：init / bind / unbind / show / resolve / grants / audit |
| `permissions.json` | 运行时状态 | run-scoped 清单（含临时 session id，**已 gitignore**） |
| `lib_hook.py` | 库 | realpath 归一化、glob 匹配、角色解析、协议封装 |
| `hook_access_guard.py` | **门禁** | 角色化访问守卫（PreToolUse）；解析失败→保守阻塞 |
| `hook_prompt_scope.py` | **诊断（非门禁）** | 提示词携带历史全集字样 → **仅 stderr 提示，不阻塞**；载荷无角色字段，故**不提供角色隔离保证**（Codex 收口 #3） |
| `hook_dispatch_register.py` | 门禁（事后） | 派发后未登记角色 → 立即报错要求补 bind |
| `hook_ledger_diagnostic.py` | **诊断** | 台账操作事后提示（不阻断） |
| `selftest.py` | 测试 | 离线自测（Python 版，无 shell 重定向，不产生中间文件） |
| `hooks.json` | 配置草案 | 四个 hook 的事件/matcher 绑定 |

`round/tools/gate_verdict.py` + `ledger.py`（状态守卫）构成推荐门禁，不依赖 hook。

---

## 4. 验证结果（**离线与真实分开记录**）

### 4.1 离线自测：`python3 round/hooks/selftest.py` → **25 passed / 0 failed**

覆盖：三个 Codex 反例、正常接力五类（生成器写自己产出/读中性、深化者读反馈与指定卡、历史审查者读历史）、越权四类（读淘汰台账/写台账/读未授权旧卡/写非本职路径）、身份隔离（子代理带 ORCHESTRATOR=1 仍拦、主控全权）、未登记会话放行、非法载荷保守阻塞、派发登记强制、台账诊断。

**并已修复**：旧 bash 版自测的错误重定向（会生成 `chk` 文件）——新版为 Python 实现，且结束时不产生任何中间文件（已核 `git status`）。

### 4.2 真实 Harness 会话验证（**已做**）

| 验证项 | 方法 | 结果 |
|---|---|---|
| 运行时身份链 | 派发真实探针子代理，比对返回值与其自身 `DSH_SESSION_ID` | ✅ **一致**（`d98202af-…`），即"派发端登记的 id = 子会话身份" |
| 父会话标记不泄漏 | 探针内 `echo $DSH_HOOK_ORCHESTRATOR` | ✅ 空（即便泄漏也不影响，因身份不依赖环境变量） |
| 真实身份判定 | 用**真实 session_id** 跑守卫五例 | ✅ **5/5**（读旧卡拦、读中性放、写授权放、写他人拦、写根目录拦） |
| 无关会话不受影响 | 未登记会话访问 | ✅ 放行并计入 `unregistered.log`（`perm.py audit` 可查） |

### 4.3 真实接入**未验证**（如实上报）

| 项 | 状态 | 原因 |
|---|---|---|
| 真实工具调用被 hook 拦截 | ❌ **未验证** | hook 未挂载；挂载需改 `~/.dsh/profiles/web/`（全局配置），用户决定不挂载 |
| 沙箱对越权写的实际拦截 | ⚠️ 未单独验证 | 依赖现有沙箱行为，非本套件控制 |
| `bash` 绕过的实际发生率 | ⚠️ 不可测 | 无拦截则无日志 |

---

## 5. 上报的具体缺口（Codex 要求：接口不支持则报缺口）

1. **角色不由运行时提供**：`PreToolUse` 载荷仅含 `session_id`/`cwd`/`tool_name`/`tool_input`，**无角色、无父会话、无子代理标记**（`agent_id` 只在 SubagentStart/Stop）。→ 已用"派发端登记 + 派发后强制补登记"绕过，但这依赖派发端不遗漏；
2. **读隔离不可得**：现有沙箱（bwrap/seatbelt）在 workspace-write 下 **root 全盘 ro-bind**，只能限写不能限读。→ 无法用现有接口阻止"读取历史文件"，只能靠 hook 拦工具级路径 + 尽力检测；
3. **任意代码不可约束**：`bash`/`run_code` 内可构造任意访问；除非提供"只读工作目录 + 受限工具集"的沙箱档位，否则**无法宣称硬隔离**；
4. **实时拦截无法自测**：不挂载即无真实拦截数据，故 §4.3 标注未验证。

---

## 6. 使用方式（派发端每次必做的两步）

```bash
# ① 初始化（每轮一次）
python3 round/hooks/perm.py init --run run2-20260911

# ② 先创建待命会话取得真实 ID，再**精确授权**（未授权 = 保持未授权，不会自动获得权限）
#    顺序很重要：授权必须在"启动材料读取"之前完成
grant() { python3 round/hooks/perm.py grant --session "$1" --role "$2" \
    ${3:+--extra-read "$3"} ${4:+--extra-write "$4"}; }
grant <subagentId> generator   ""                                  round/run2/staging/path-A-intensity.md
grant <subagentId> deepener    round/run2/feedback/A3-feedback.md  round/run2/drafts/A3.md
grant <subagentId> history_reviewer ""                            round/run2/op-history-review.md

# ③ 轮末审计未登记访问
python3 round/hooks/perm.py audit
```

> **语义（2026-09-11 更正）**：
> - **未授权子会话不会"不受约束"**——它会**保持未授权**：任何对研究区的读/写都被拦并提示补授权；
>   仅"区外路径"的操作放行并记入 `unregistered.log`。
> - 空 target 票据**已禁止创建**（`reserve` 必须带 `--session`）。
> - `bind` 为兼容保留；日常请用 `grant`（显式绑定会话 + 角色 + 任务文件）。
