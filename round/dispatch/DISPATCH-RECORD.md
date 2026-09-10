# 实际派发记录（DISPATCH-RECORD，2026-09-10）

> 来源：从当前 Harness 会话记录补取（返工包第一组第 6 条）。取不到的字段如实标"未取得"，不补造历史回执。
> 提示词全文：`round/dispatch/D123-prompts.md`（自会话记录重建，非平台导出）。

## 三路生成器（run-test 本轮，试运行性质）

| 字段 | D1 路径A | D2 路径B | D3 路径C |
|---|---|---|---|
| 执行体 | subagent（后台 continuable） | 同左 | 同左 |
| subagentId | c50de73b-7a75-4e36-8ccb-68701007692a | 3e83c394-05d6-4577-a88b-f82657083144 | aaf17ff2-83e1-459b-8c0a-b9092877e8f5 |
| 派发时刻 | 2026-09-10 18:51 前后（会话时钟） | 同左 | 同左 |
| 任务输入 | 工作包 charter A（场景与学习原理推演）+ 公共模板（目标/防火墙/证据规范/阅读配额/产出合同/白黑名单） | charter B（文献实际行为） | charter C（方法迁移与假设检查） |
| 输出位置 | round/staging/path-A-scenario.md | round/staging/path-B-literature.md | round/staging/path-C-transfer.md |
| 完成状态 | completed（settle 通知+结果消息） | completed（同左） | completed（同左） |
| 产出规模 | 101 行/4 卡 | 119 行/4 卡 | 76 行/4 卡（C2 为弃卡检验记录） |
| 模型路由 | 配置的子代理默认路由（Harness child default）；**具体 provider/model id：未取得**（派发时未显式指定，平台未回传路由字段） | 同左 | 同左 |
| 用量（token/时长） | **未取得**（平台未暴露 per-subagent 用量） | 未取得 | 未取得 |
| 合规自报 | 无笔记占比 73%；Undermind 3/3；撞见声明（KNOWLEDGE-MAP 旧候选段） | 55%；2/3；同左+CHOU PDF 截断改 arXiv HTML | 75%；3/3；同左+本地 HE/ZHOU PDF 损坏改 arXiv HTML |
| R2 状态标签 | 接触过旧候选信息的试运行材料（文件头已加横幅） | 同左 | 同左 |

## 其他派发（本轮架构期）

| 用途 | 执行体 | 状态 | 备注 |
|---|---|---|---|
| 组件实测/证据链抽查 | 主控本地 bash（无子代理） | completed | 日志 round/logs/repro-group2.txt |
| chatgpt_dispatch 异模型探活 | chatgpt_dispatch health | **失败**（插件输出契约错误 missing "value.note"） | 未重试第二次；异模型通道不可用已记录 |
