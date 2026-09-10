# 集中验收包（ACCEPTANCE-PACKAGE，2026-09-11）

> 对 Codex 实查（版本 4d3b5c9）五项问题的收口结果。
> **测试与离线自测分列**；**测试卡不进入研究候选池**（独立台账 `round/run2/acceptance/TEST-LEDGER.csv`）。

---

## A. 逐项收口

### #1 hook 尚未接上真实工具调用 —— ✅ **已通过（真实会话实测）**

| 项 | 结果 |
|---|---|
| 挂载 | ✅ 配置写入 `~/.dsh/profiles/web/cordis.patch.yml`（`hooks-research-guard`）；**用户重启 web 服务后生效** |
| 生效证据 | ✅ 子会话日志出现 `hook/invoked` / `hook/result` 事件（8 条），`handlerId=claude-code:PreToolUse:*` |
| **真实拦截** | ✅ 未登记探针读 `round/zotero/ZOTERO-INDEX.md` → `[HOOK-BLOCK] 本研究运行中的会话身份/权限异常（未登记且无可用票据）` |
| **真实越界拦截** | ✅ 已登记生成器 shell 列 `round/run1/` → `[HOOK-BLOCK] 角色 generator 不允许访问：round/run1（shell-dir）` |
| **真实正向放行** | ✅ 生成器读中性索引成功 + 写授权草稿成功（文件实际落盘 `REAL-CHAIN-OK`） |
| 提示词边界 | ✅ 主控派发含历史索引字样的任务被真实拦下 |
| 票据机制 | ✅ 首次访问原子领取：`pending 1 → bound 1`，无登记空窗 |

**修复过程中实测发现并修掉的三处真实缺陷**：
1. **目录列举漏拦**：子代理曾成功 `find` 列出历史目录文件名（PATHLIKE 只认带扩展名的文件）→ 增补敏感目录检测；
2. **shell 来源匹配错**：`collect` 产出 `shell-file`/`shell-dir`，而 `main` 只判 `shell-literal` → shell 派生目标完全未校验；
3. **过度拦截**：早期 shell 扫描把路径中间段（裸 `round`）当访问目标 → 改为"具体文件 + 敏感目录"两类精确抽取。

**另修一处设计缺口（本次亲历事故）**：用临时清单覆盖真实清单后，**主控自身失去权限且无自助恢复路径**。已加：
- `init` 更换主控需显式 `--force`；
- `orchestrator_history` 保留最近 3 个主控 ID（交接后旧主控仍可恢复）；
- 清单 `missing` 时主控凭独立副本 `orchestrator.id` 仍可操作。

### #2 子代理先启动、权限后登记（首次访问空窗）

| 项 | 状态 |
|---|---|
| 复现 | ✅ 未登记会话原为「放行」 |
| 修复 | **票据机制**：`perm.py reserve --role R --count N` 预留学生名额；子代理**首次访问研究区文件时原子领取**；无票据 → **暂停并报告** |
| 附带发现 | 子代理 session cwd = **主仓库**（非本 worktree）→ 按 cwd 判定会漏判；已改为**按访问路径判定**（受控区 = hook 所在 worktree，固定） |
| 验证 | 离线用例：未登记读研究区=拦 / 只读区外=放行 / 有票据=受控启动 / 票据耗尽=拦 |
| 判定 | ✅ 修复完成（离线通过）；真实生效仍待 #1 重启 |

### #3 "只读本卡"未落实

| 项 | 状态 |
|---|---|
| 复现 | ✅ deepener 可读他人卡反馈；history_reviewer 可写 `op-history-review-*.md` 通配范围内他人报告 |
| 修复 | **最小授权**：所有角色的读/写基础授权收紧为「中性资料 + 空」；具体卡/报告一律由派发端 `--extra-read/--extra-write` 按**确切文件**授予 |
| 验证 | 10/10 用例：读本卡✓/读他人卡✗/写自己✓/写他人✗（deepener、history_reviewer、reviewer 三类角色） |
| 判定 | ✅ 完成 |

### #4 换运行、异常恢复不可靠

| 项 | 状态 |
|---|---|
| 复现 | ✅ 新 run `init` 保留旧 sessions；权限文件损坏 → unknown → **静默放行** |
| 修复 | ① `init` 默认**清空**旧会话绑定（`--keep` 可显式保留）；② 清单 `missing/corrupt` → **研究会话失败关闭**，主控凭独立副本 `orchestrator.id` 仍可修复；③ 写入改**原子替换**（避免半写） |
| 验证 | 研究会话损坏=拦(2) / 主控损坏=放行(0) / 区外会话=放行(0) / 新 run 后 bound=0 |
| 判定 | ✅ 完成 |

### #5 推荐检查有旁路

| 项 | 状态 |
|---|---|
| 复现 | ✅ `revise --status recommended_pending_review` 可绕过；`gate_verdict` 在被审卡文件缺失时仍 PASS |
| 修复 | ① 抽出共同入口 `_guard_recommendation()`，`status` 与 `revise` **两条路径共用**；② `gate_verdict.check` 卡文件缺失 → **失败**（不再跳过校验） |
| 验证 | 无判定→拒 / BLOCK→拒 / PASS→过 / 承重修订后→两路径均拒 / 重审后→过 |
| 判定 | ✅ 完成 |

---

## B. 测试卡跑通记录（**独立台账，不入研究候选池**）

卡：`【测试卡·非研究候选】负载变化下的验证链路测试`（`c2abb1b7225`，台账 `round/run2/acceptance/TEST-LEDGER.csv`）

| 路径 | 步骤 | 结果 |
|---|---|---|
| **正常完成** | 入账 → 无判定置推荐 | REJECTED（无判定记录）✅ |
| | 记录 BLOCK → 置推荐 | REJECTED（当前判定 BLOCK）✅ |
| | 补证后记录 PASS → 置推荐 | STATUS → recommended_pending_review ✅ |
| | 承重字段修订 → 再置推荐（status 路径） | REJECTED（版本不匹配）✅ |
| | 承重字段修订 → 再置推荐（**revise 旁路**） | REJECTED（版本不匹配）✅ |
| | 重新判定 PASS → 置推荐 | STATUS → recommended ✅ |
| **失败返工** | 判定 INPUT_INSUFFICIENT → 置推荐 | REJECTED ✅ |
| | 置 `needs_revision`（返工状态） | STATUS → needs_revision ✅（**不被推荐门禁误伤**） |
| **恢复** | 返工后判定 PASS → 置推荐 | STATUS → recommended ✅ |
| **主控接续** | `init --orchestrator <新会话>` | 主控切换成功；**旧会话绑定被清空** ✅ |
| **异常恢复** | 清单损坏 → 研究会话访问 | exit=2（暂停）✅ |
| | 清单损坏 → 主控访问 | exit=0（可修复）✅ |

**必须实际验证的四点对照**：
| 要求 | 结果 |
|---|---|
| 登记前的研究子代理不能先读材料 | 离线 ✅（票据机制）；**真实生效待重启** |
| 合法工作能完成、越界读取被拒 | ✅ 离线 24/24 |
| 缺材料/审查失败进入明确补证或返工状态 | ✅ `needs_revision`/`INPUT_INSUFFICIENT`，非假通过、非无故结束 |
| 修改候选后所有推荐路径都重新检查 | ✅ status 与 revise 两条路径均拒 |
| 新会话能接续、不重派已完成任务、不继承旧权限 | ✅ `init` 清空旧绑定 |

---

## C. 离线测试与真实测试分列（**不得混同**）

| 类别 | 内容 | 结果 |
|---|---|---|
| **离线自测** | `python3 round/hooks/selftest.py`（24 项：最小授权/票据/路径判定/workdir/损坏关闭/非法载荷） | **24 passed / 0 failed** |
| **离线路径判定专项** | 12 项（含 cwd=主仓库 + 绝对路径、bash workdir 相对路径） | **12/12** |
| **离线 workdir 专项** | 6 项 | **6/6** |
| **回归** | `test_rework_regressions.py` | **12/12** |
| **真实会话·身份链** | 探针子代理 vs 其 `DSH_SESSION_ID` | ✅ 一致（派发端 id = 子会话身份） |
| **真实会话·父标记不泄漏** | 探针内 `$DSH_HOOK_ORCHESTRATOR` | ✅ 空 |
| **真实会话·hook 拦截** | 未登记探针读研究区 / 生成器越界读旧卡 | ✅ **均被拦截**（含 shell 目录列举） |
| **真实会话·正向链路** | 生成器读中性 + 写授权草稿 + 越界被拒 | ✅ **三步全部符合预期** |

---

## D. 明确的接口缺口（Codex 要求：不支持则报缺口）

1. **角色不由运行时提供**：`PreToolUse` 载荷仅 `session_id/cwd/tool_name/tool_input`，无角色/父会话/子代理标记 → 只能由派发端登记 + 票据机制；
2. **热加载不生效**：`patchReload: live` 在运行中的 web 服务上未加载新增补丁段 → **必须重启服务**（这是 #1 未达成的直接原因）；
3. **读隔离不可得**：沙箱仅限写范围（root 全盘 ro-bind），**无法阻止任意读取**；读侧防线只能是 hook；
4. **任意代码不可约束**：`bash`/`run_code` 内可构造任意访问 → 已降级为"尽力检测"，**不宣称硬隔离**。

---

## E. 范围与纪律声明

- 仅修复影响该闭环的接缝，**未扩展功能**；
- **未删除任何研究证据**（台账 append-only；测试痕迹与回滚行如实保留）；
- **不把测试通过称为选题质量通过**：本次只证明"研究按正确流程做"，**不证明结论正确**；
- 内容审查仍须分别判断：原文是否支持事实 → 事实是否支持原因解释 → 改动是否针对原因（引用定位成功 ≠ 论证成立）。
