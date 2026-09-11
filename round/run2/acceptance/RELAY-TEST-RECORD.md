# 真实接力测试验收记录（RELAY-TEST，2026-09-11）

> 目的：**开工检查**——用两张测试卡验证"派发→授权→读取→审查→返工→重审→推荐"短链真实可用。
> 纪律：测试卡**不进入正式候选池**（独立台账 `round/run2/acceptance/RELAY-LEDGER.csv`）；不额外检索、不写长报告。

---

## 1. 会话与授权（授权先于材料读取）

| 卡 | 真实会话 ID | 角色 | 授权文件 | 顺序 |
|---|---|---|---|---|
| T1 | `9ec90a0b-e315-4e67-90d3-94b730e28b15` | generator | read `round/zotero/ZOTERO-INDEX.md`；write `CARD-T1-draft.md` | ✅ **grant 完成 → 才发材料指令** |
| T2 | `fd379668-82b4-47d6-8a71-d9b59faef522` | generator | read 同上；write `CARD-T2-draft.md` | ✅ 同上 |

- 实际模型：`commandcode-goat-autosync/z-ai/glm-5.3-flash`（非 Pro 路线）；
- 授权由主控**串行执行**（`perm.py grant --session <id> --role ... `），与派发分离；
- **授权前未发送任何研究材料**（首条消息仅"待命，勿读文件"）。

## 2. T1：正常完成路径 ✅

| 步骤 | 结果 |
|---|---|
| 读取授权资料 | ✅ 成功（返回 ZOTERO-INDEX.md 前 5 行原文） |
| 写入授权草稿 | ✅ 成功（`CARD-T1-draft.md`，operation=create） |
| 审查登记 | ✅ `RT1-builder`，绑定 `h06a1015b773f` + 卡 sha256 `79233e3d…` |
| 闸门判定 | ✅ `PASS @h06a1015b773f v1` |
| 推荐待审 | ✅ `STATUS → recommended_pending_review (v2)` |

## 3. T2：失败返工路径 ✅

**预置错误**：卡片证据行写"本库共 **47** 篇"，而原文实为"**111** 篇"（子代理按要求照抄未更正，并主动 fail-loud 报告矛盾）。

| 步骤 | 结果 |
|---|---|
| 审查发现 | ✅ 判定 **BLOCK**（证据引用与原文不符：47 vs 111） |
| BLOCK 下推荐 | ✅ **REJECTED**（"当前版本判定为 BLOCK"） |
| 转返工 | ✅ `STATUS → needs_revision (v2)` |
| 修订卡片 | ✅ 47 → 111 |
| 台账修订 | ✅ `REVISED v3`，**REVIEWS_INVALIDATED: ['RT2-builder']** |
| 旧审查失效核对 | ✅ `RT2-builder status = needs_review` |
| 重审 | ✅ `RT2-recheck` 绑定新 hash `h873b768d2a39` |
| 重审判定 | ✅ `PASS @h873b768d2a39 v3` |
| 推荐待审 | ✅ `STATUS → recommended_pending_review (v4)` |

**版本链完整**：v1 add → v2 needs_revision → v3 revise（承重变更）→ v4 recommended。

## 4. 本轮实测发现并修复的缺陷（1 处，属"影响研究推进的具体故障"）

**缺陷**：shell 通道解析出**裸文件名**时与授权路径不匹配 → **合法访问被误拦**。
- 现象：T2 首轮用 `cd round/zotero && cat ZOTERO-INDEX.md` 形式，被拦（`shell-file`），提示"需要 --extra-read 授予"——但该文件**已被授权**；
- 影响：正常接力被阻断（子代理零读写，需人工干预）；
- 修复：`hook_access_guard` 的授权匹配增加"**裸文件名 ↔ 授权文件同名**"分支（授权范围未放宽，仍是具体文件）；
- 验证：`bash cat 完整路径` / `cd+裸文件名` / `写授权文件` 均放行；`读未授权历史` 仍拦。

## 5. 记录要素（Codex 要求）

| 要求 | 记录 |
|---|---|
| 真实会话 ID | T1 `9ec90a0b…`；T2 `fd379668…`（另有已废弃的 `0abef1d0…`，因一次性会话不可续而弃用） |
| 实际模型 | `z-ai/glm-5.3-flash`（非 Pro） |
| 授权与首次读取顺序 | **grant → 派发材料指令**（未出现"授权前读取"） |
| 候选版本 | T1 c06a1015b77 v1→v2；T2 cce244f2fe9 v1→v2→v3→v4 |
| 审查记录 | `round/run2/acceptance/RELAY-REVIEWS.csv`（RT1-builder、RT2-builder[失效]、RT2-recheck） |
| 状态变化 | 见 §2/§3 表 |
| 实际用量 | 子代理调用 6 次（3 待命 + 2 材料执行 + 1 废弃）；模型调用均为非 Pro flash 路线；无额外检索 |

## 6. 结论

**短链验证通过**：授权绑定、材料读取、审查、返工、审查失效、重审、推荐——全链真实执行，状态与版本可追溯。
**测试卡未进入正式候选池**（独立台账，标题标注"测试卡·非研究候选"）。

**已知边界（如实声明）**：
- `bash`/`run_code` 任意代码仍为**尽力检测**，不构成硬隔离；
- 提示词角色检查为**诊断件**，不提供角色隔离保证；
- 本测试为**开工检查**，不构成选题质量或研究结论的验证。
