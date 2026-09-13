# Hook 接入取证（HOOK-CONTRACT，2026-09-11）

> 目的：在动手改之前，把"Harness 究竟提供什么"钉死。全部结论来自**源码/运行日志实测**，非推测。

## 1. Hook 载荷里有什么身份信息（决定角色权限能否实现）

源码：`dsh-hooks-claude-code/lib/index.js`

**PreToolUse 载荷**（第 368-374 行）：
```js
{ ...base(ctx, exec.agent, "PreToolUse"), tool_name, tool_input, tool_use_id }
// base() = { session_id, transcript_path, cwd, hook_event_name }
```

| 字段 | 是否可用于身份判定 |
|---|---|
| `session_id` | ✅ **运行时提供**，模型无法伪造 |
| `cwd` | ✅ 运行时提供 |
| `tool_name` / `tool_input` | ⚠️ 模型可控（但这是被检查对象本身，正常） |
| **角色 / 父会话 / 是否子代理** | ❌ **载荷里没有** |
| `agent_id` | ❌ 只出现在 `SubagentStart`/`SubagentStop`（第 397-403 行），不在 PreToolUse |

**结论**：角色**无法从载荷推断**，必须由**派发端（主控）显式登记**，以 `session_id` 为键绑定。`session_id` 是唯一可靠的运行时身份。

## 2. 现有沙箱能做什么（决定"硬隔离"是否可取用）

- 存在 OS 级沙箱：`dsh-sandbox-local`（Linux 用 bwrap、macOS 用 seatbelt、Windows 用 ACL）；
- 模式三档：`read-only` / `workspace-write` / `danger-full-access`；
- 子代理的沙箱来自**继承**（会话日志实测：`sandbox/mode {"mode":"workspace-write","source":"delegation"}`）；
- `bwrapProfileArgs` 逻辑：**root 全盘 ro-bind（只读挂载），仅 workspaceRoot 可写**。

**结论（关键缺口）**：沙箱**只能控制"写"的范围，不能控制"读"的范围**——任何会话都能读整个文件系统（只读）。因此**无法用现有沙箱阻止生成器读取历史文件**。"路径级读隔离"在现有接口下**不可得**，必须如实上报。

## 3. 因此可达成的边界（诚实分级）

| 访问方式 | 能否可靠约束 | 手段 |
|---|---|---|
| `read`/`write`/`edit`/`glob`/`grep` 工具调用 | ✅ **可**（工具输入里有结构化路径） | 路径归一化 + 角色授权表 |
| `bash` 里的任意命令 | ❌ **不可**（无法可靠解析 shell） | 仅尽力检测；**不得宣称硬隔离** |
| `run_code` 里的任意代码 | ❌ **不可**（任意 Python/JS） | 同上 |
| 越权写入 | ✅ 可（沙箱 workspace-write 之外的写被 OS 拦） | 现有沙箱 |
| 越权读取 | ❌ 不可 | **缺口，须上报** |

## 4. Codex 实测复现（我这边已复现 2/3）

| 反例 | Codex 结果 | 我的复现 |
|---|---|---|
| `cat round/run2/TONIGHT-SCOPE.md` | 放行 | ✅ 放行（正则未覆盖 run2/） |
| 读 `./round/run1/card-B3-window.md` | 放行 | ✅ 放行（未归一化 `./`） |
| Python `open()` 读旧候选 | 放行 | 我这次巧合被拦（正则误命中）→ **恰好证明正则不可靠：同一语义两种结果** |

## 5. 修复方向（按 Codex 指令）

1. **角色权限**：主控派发时显式登记 `session_id → 角色 → 读写白名单`；hook 只认 `session_id`，**不再用环境变量判定身份**（父会话的 orchestrator 标记不得让子代理整体豁免）；
2. **路径边界**：对工具级路径做 `realpath` 归一化（`./`、相对、绝对、符号链接统一）；**bash/run_code 降级为"尽力检测"并明示**；
3. **推荐检查**：绑定 `候选 ID + 当前版本(content_hash) + 对应判定`，接入**现有台账命令**；废弃"扫目录"式检查；
4. **自测**：分开记录"离线自测"与"真实会话接入"结果；修 `chk` 文件 bug。
