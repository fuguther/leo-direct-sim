## 生命周期

- 状态：`DRAFT`（可选：`REVIEW` / `READY` / `BLOCKED` / `ABANDONED`）
- Owner：
- Base SHA：
- Head SHA：
- Write set：
- Supersedes：无

## 改动与原因

- 改了什么：
- 为什么：
- 明确不包含：

## 验证证据

- 命令：
- 结果：`passed / failed / skipped`
- 行为对照或回执：

## 独立复核

- 是否属于承重改动：否
- Reviewer / 方法：
- 被审 exact full SHA：
- Verdict：`未要求 / 待复核 / APPROVE / REQUEST_CHANGES`

## Blocker / 恢复条件

- Blocker：无
- 恢复条件：无

## READY 检查

- [ ] diff 只包含声明的 write set 和主题
- [ ] 已与最新 `origin/main` 对账
- [ ] CI 绿，真实 passed/failed/skipped 已记录
- [ ] 必需独立复核绑定当前 Head SHA 并通过
- [ ] 没有未解决 blocker
- [ ] 不包含未获授权的删除、移动、force-push、仓库设置或 release 操作

> `push != READY`；`CI green != independent review`；`merged != deployed/receipt`。
