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

## run2 派发记录（2026-09-10）

| 角色 | subagentId | 任务 | 模型路线 | 预算 |
|---|---|---|---|---|
| 生成器路径A | 30a9d220-37de-414f-a2cc-65ad0de35d4f | 流量整体强度变化入口，0-4卡 → round/run2/staging/path-A-intensity.md | 配置默认子代理（非Pro） | Undermind≤3, read_pdfs≤2 |
| 生成器路径B | 48f746d6-0315-4fd2-975f-89354cf60db8 | 热点/OD分布变化入口 → path-B-hotspot.md | 同上 | 同上 |
| 生成器路径C | 55ba9d13-2423-48c9-82d0-00fbd7172ec5 | 突发程度/速度变化入口 → path-C-burst.md | 同上 | 同上 |

共同约束：白名单 v3（notes-neutral 替代 raw）；黑名单含 run1 产物/台账/reviews/history；八节卡格式+四档标注；诚实放弃线+防火墙声明必写。

### run2 生成器首派失败取证（2026-09-10 02:00-02:22）

- **现象**：3 个后台 continuable 子代理（30a9d220/48f746d6/55ba9d13）在建卡前失败，通知为 failed/no closing message；随后向其发送「只回报诊断」的纯文字请求同样立即失败且无收尾消息；前台完整路径A任务亦 abort。
- **取证**（五步法第2步，读真实日志）：子会话日志 `~/.dsh/sessions/--Users-lge-Desktop-leo-direct-sim--/55ba9d13-.../session.jsonl.zstd` 尾部 turn/end 原文：
  `403 {"error":{"type":"permission_error","message":"You've reached your 5-hour usage limit. Your quota will reset when the current 5-hour window ends...","type":"error"},"code":"AUTH"}`
- **结论**：失败原因是**模型路线配额耗尽**，与任务内容、提示词、工具权限、沙箱无关。
- **路线探测**（显式 provider+model，最小探针）：`deepseek/deepseek-v4-flash` OK；`z-ai/glm-5.3-flash` OK；`Qwen/Qwen3.8-Flash` 失败；`meta/muse-spark-1.3-contributor` 失败。自动选路把生成器分到了耗尽路线。
- **处置**：三路生成器改显式绑定 `commandcode-goat-autosync/deepseek/deepseek-v4-flash` 重派（新 id：33536acc / 90dff8f9 / 3f435255）。旧三个子代理标记 ABANDONED（无产物，仅遗留一个临时 grep 脚本已清理）。
- **对费用/授权约束的影响**：仍在既有非 Pro flash 授权范围内，未启用任何 Pro 路线。
### run2 生成器第三次派发（glm-5.3-flash，2026-09-10 02:3x）

- 用户要求子代理全部改用 `deepseek/deepseek-v4.1-flash`。配置文件 `~/.dsh/settings.yaml` 第 109-110 行已由用户加入该路线（核实通过）。
- **但本会话无法使用 4.1**，证据链：
  1. 运行态：`list_subagent_models` 仍只返回 4 条（Qwen3.8-Flash / v4-flash / glm-5.3-flash / muse-spark），无 4.1；
  2. 显式调用报错原文：`child LLM route "commandcode-goat-autosync/deepseek/deepseek-v4.1-flash" is not allowed for this Session`；
  3. 源码定位 `@deepseek-ai/dsh-tool-subagent/lib/index.js:585-600`：`selectForAgent()` **仅在 `freshSession`（会话首个实时事件）时**调用 `settings.current()` 读取 allowedModels，随后 `recordSubagentModelSelection()` 将该策略作为 `subagent/model-selection-policy` 事件**写入会话并永不覆盖**；子会话继承父会话已冻结策略。
  4. 结论：白名单为**会话级快照**，运行中改配置文件不生效；4.1 需**新建会话**。
- CLI 新会话路线亦被沙箱拒绝：`dsh --profile headless` 启动时写 `~/.dsh/profiles/headless/cordis.yml` 报 `EPERM`（工作区外，未申请升级）。
- 处置：本会话改用**唯一合规可用路线** `z-ai/glm-5.3-flash`（非 v4、非 Pro，探针 ROUTE-OK）派三路生成器：6dd5881f / b77deb91 / 4e787df3。用户若坚持 4.1，需新开会话并按下述交接包执行。
- 费用口径：仍在非 Pro 授权范围内。
