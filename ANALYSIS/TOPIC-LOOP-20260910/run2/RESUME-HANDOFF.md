# 研究接续说明（RESUME-HANDOFF v1.0，2026-09-11）

> 用途：新主控会话**只读这一份**即可接续本研究，不需历史候选全集，不需旧对话。
> 纪律：本文件**不含**任何候选内容/排序/淘汰理由（那些在台账与淘汰台账里，按角色受限访问）。

## 1. 实际启动方式

```bash
cd /Users/lge/Desktop/leo-direct-sim/.worktrees/topic-loop-20260910
# ① 确认工作区与版本
git rev-parse --short HEAD && git status -sb | head -2
# ② 初始化本轮权限（新主控会话默认即主控）
python3 round/hooks/perm.py init --run run2-20260911
python3 round/hooks/perm.py show          # 确认 orchestrator = 当前会话
# ③ 自检（离线）
python3 round/hooks/selftest.py           # 期望 24 passed
python3 round/tools/test_rework_regressions.py   # 期望 12/12
```

**派发子代理前后必做**（票据机制，消除"登记前空窗"）：
```bash
# 派发前：预留学生名额（同批必须同角色）
python3 round/hooks/perm.py reserve --role generator --count 3 \
    --extra-write round/run2/staging/path-A-intensity.md \
    --extra-write round/run2/staging/path-B-hotspot.md \
    --extra-write round/run2/staging/path-C-burst.md
# 子代理首次访问研究区文件时**原子领取**票据；无票据 → 暂停并报告
# 事后审计
python3 round/hooks/perm.py audit
```

## 2. 适用工作区与版本

| 项 | 值 |
|---|---|
| 受控工作区 | `/Users/lge/Desktop/leo-direct-sim/.worktrees/topic-loop-20260910`（**仅此目录**） |
| 分支 | `agent/20260910-topic-loop` |
| 权限清单 | `round/hooks/permissions.json`（运行时状态，已 gitignore） |
| 主控锚点 | `round/hooks/orchestrator.id`（清单损坏时的恢复凭据） |
| 候选台账 | `round/CANDIDATE-LEDGER.csv`（append-only） |
| 淘汰台账 | `round/history/ELIMINATED-REGISTER.md` |
| **不适用** | 主仓库 / 其他 worktree / 其他会话（hook 按**访问路径**自限，不受影响） |

## 3. 运行身份与状态位置

| 概念 | 位置 | 说明 |
|---|---|---|
| 主控身份 | `permissions.json:orchestrator_session` + `orchestrator.id` | 由 `init` 写入当前 `DSH_SESSION_ID` |
| 角色绑定 | `permissions.json:sessions` | `session_id → {role, extra_read, extra_write}` |
| 待领票据 | `permissions.json:tickets` | `reserve` 写入；子代理首次访问时原子消费 |
| 未登记访问 | `round/hooks/unregistered.log` | 区外放行记录 + 研究区拦截记录 |

**角色权限**（详见 `python3 round/hooks/perm.py grants --role <角色>`）：

| 角色 | 可读 | 可写 |
|---|---|---|
| `orchestrator` | 全部 | 全部 |
| `generator` | 中性资料（Zotero 索引/notes-neutral/原文） | 仅 `--extra-write` 指定的文件 |
| `deepener` | 中性资料 + `--extra-read` 指定的卡与反馈 | 仅指定的深化稿 |
| `history_reviewer` | 中性资料 + 历史库（索引/台账/run1 旧卡/审查） | 仅指定的报告 |
| `reviewer` | 中性资料 + 指定的被审材料 | 仅指定的意见文件 |
| `auditor` | 全部（只读） | 仅指定的审计报告 |

## 4. 当前候选与证据版本

**候选台账当前状态**（`round/tools/ledger.py show --ledger round/CANDIDATE-LEDGER.csv --all`）：
- 池子 8 项：A2、A3（含 B2 资产）、B1、B3（含 A1 资产）、C1、C2 + run1 的 L1、F1（含 C3 资产）
- 已合并：A1→B3、B2→A3、C3→F1（均在台账留 `merged` 行与理由）
- 无任何候选处于 `recommended_pending_review`

**证据版本**：
- 语料索引 `round/zotero/ZOTERO-INDEX.md`（111 篇）
- 证据勘误 `round/run2/ERRATA-RUN2-01.md`（CMNCS52M 五变量混淆，**必读**）
- 锚件核验规则 EFFECTIVE-RULES-R2 §8.0.1

## 5. 未完成任务

| # | 任务 | 状态 |
|---|---|---|
| 1 | 历史碰撞审查（9 卡的 five-class 裁决） | ✅ 完成（`round/run2/op-history-review.md`） |
| 2 | 批内对账（§8.0） | ✅ 完成（`round/run2/op-intra-batch.md`，合并 3 卡） |
| 3 | 收窄（筛出可深化卡） | ⏳ **待做** |
| 4 | 死因回传（must-address） | ⏳ 待做 |
| 5 | 深化（≤3 并行，三问） | ⏳ 待做 |
| 6 | 三角色审查 + G1–G5 闸门 | ⏳ 待做（**闸门从未对真实卡判过**） |
| 7 | VM MinerU 111 篇转换 | 🔄 后台进行（约 30/111） |

## 6. 下一动作（唯一推荐起点）

1. `python3 round/tools/ledger.py show --ledger round/CANDIDATE-LEDGER.csv --all | tail -20` 掌握当前状态；
2. 读 `round/run2/op-history-review.md` 的汇总表与"最可能真撞车"节；
3. 按 §8.0/§8.0.1 做收窄：保留判 ①②③ 且现象有原文锚点者；淘汰者写入 `ELIMINATED-REGISTER §6`；
4. 为保留卡写 `round/run2/feedback/<卡ID>.md`（**只含本卡**）；
5. `reserve` + 派发深化者（≤3 并行）。

## 7. 停止与恢复方法

**停止**：直接结束会话即可。运行时状态都在 `round/hooks/`（gitignore），台账为 append-only，**不丢数据**。

**恢复（三种情形）**：
| 情形 | 做法 |
|---|---|
| 同一主控会话续跑 | `perm.py show` 确认 orchestrator 是自己 → 直接继续 |
| **新主控会话接续** | `perm.py init --run <新runId>`（**默认清空旧会话绑定，不继承旧权限**）→ 按 §6 继续 |
| 权限清单损坏 | 研究会话会被暂停并报告；**主控凭 `orchestrator.id` 仍可操作** → 重新 `init` 修复 |

**关闭 hook 强制**（如遇误拦）：从 `~/.dsh/profiles/web/cordis.patch.yml` 删除 `hooks-research-guard` 段并重启 web 服务。

## 8. 已知限制（不得当成"已验证"）

1. **hook 尚未实际生效**：配置已写入 profile，但运行中的 web 服务未加载（无 `hook/invoked` 事件）。**在重启 web 服务前，"真实拦截"未经实测**；
2. `bash`/`run_code` 内的任意代码**只做尽力检测**，不是硬隔离；
3. 沙箱只能限"写"范围，**不能限"读"**——读取历史文件的最终防线是 hook，而 hook 依赖重启生效；
4. 台账中 `c9bbc1f6604` 的 v2/v3 行为 #5a 复现测试痕迹，v4 为回滚行（append-only 不删）。
