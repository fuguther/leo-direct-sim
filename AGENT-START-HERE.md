# Agent 开工入口

本页是仓库内研究、实验、平台修改和审阅任务的统一入口。先确定文档权威和证据时效，再安排工作；不要从搜索结果中随便挑一份日期稿继续执行。

## 开工检查

先在当前 checkout 运行：

```bash
python3 scripts/check_workspace_hygiene.py --phase start
python3 scripts/check_document_governance.py --mode all --report /tmp/leo-document-governance.json
```

检查失败时：

- 工作区检查返回 `1`：先读清单。`DIRTY`、`EVIDENCE_PRESENT` 或 `UNEXPECTED_IGNORED` 时，新写入者不得开工，也不得回收 worktree；已声明的唯一 owner 续作同一任务时也必须保留并核对该分类，工具不会替人推断所有权。检查器只读，不授权删除。
- `STALE_CURRENT`：实时核对对应代码、GitHub、VM 或实验回执；在完成核对前把相关状态写成 `UNVERIFIED`，不能沿旧结论执行。
- `UNCLASSIFIED_DOCUMENT`：先把新指导/记录文件登记到 `ANALYSIS/DOCUMENT-STATUS.json`。
- `PROTECTED_CONTENT_CHANGED`：停止修改 `AGENTS.md`；只有经过明确设计和用户确认的稳定规则变化才能更新受保护哈希。
- `SUPERSEDED` 或历史文件：只用于追溯当时证据，转到登记的 replacement 再判断当前工作。

## 最短阅读顺序

1. `AGENTS.md`：稳定、长期的仓库硬规则。
2. `ANALYSIS/DOCUMENT-STATUS.json`：每份指导和记录文档的状态、用途、替代入口及复核周期。
3. **论文选题任务**：先读 `LITERATURE/README.md`，按其中的方向地图 → 方向比较 → 具体问题 → 近邻核验逐层收敛，遵守证据防火墙。在独立问题形成和直接近邻核验完成前，不读取详细实验计划、历史结果、旧候选排序或平台功能清单。
4. **实验、实现和复核任务**：读取 `ANALYSIS/CURRENT-EXPERIMENT-READINESS.md`、`ANALYSIS/EXPERIMENT-PROGRAM.md` 与 `EXPERIMENTS/experiment-program.yaml`，实时核对其中的外部状态。
5. 选题候选已经独立形成后，才可把上一步的 CURRENT 文档作为本地证据揭示，用于反证、边界和可行性判断，不得据此生成或排序候选。
6. 按任务读取当前专题合同：
   - Q0/信息裁剪：`ANALYSIS/Q0-INFORMATION-ABLATION-PROTOCOL.md`
   - 平台能力与迁移取舍：`ANALYSIS/PLATFORM-CAPABILITY-LEDGER.md`
   - 已知问题与复核：`ANALYSIS/FINDINGS-REGISTRY.md`
   - 正式实验：`CODE/experiment_platform/AGENT_EXPERIMENT_PROTOCOL.md`

## 论文选题材料隔离

- 冷启动草图不得出现仅由项目历史产生的实验编号、内部候选名、既有算法清单或平台现成功能。
- 旧实验必须拆成“原始观测”和“历史解释”；前者可在本地证据揭示阶段检验候选，后者只能作为待攻击解释。
- `SUPPORTING`、`ROLLING-LOG`、`EVIDENCE-SNAPSHOT`、`HISTORICAL` 和 `SUPERSEDED` 文档不得推荐、冻结或否决中心问题。
- 证据不足时保留候选和下一项廉价核验，不强制推荐一个中心问题，也不得把用户反馈本身当作杀题证据。

## 权威顺序

发生冲突时按以下顺序判断：

1. 当前 checkout 的代码、配置 schema、测试和可重算 receipt 决定实际行为。
2. `CURRENT-CONTRACT` 决定现行定义、边界和流程。
3. `CURRENT-VOLATILE` 只提供最近一次状态快照；其中的 branch、SHA、PR、CI、VM、run、完成状态和时间估计必须实时复核。
4. `SUPPORTING` 提供方法和证据，不能覆盖现行合同或状态。
5. `ROLLING-LOG`、`EVIDENCE-SNAPSHOT`、`HISTORICAL`、`SUPERSEDED` 只能回答“当时记录了什么”，不能决定当前下一步。

任何层级都不能把“本地测试通过”自动升级成“已独立审阅、已合入、已部署、已授权或论文可用”。

## 文档生命周期

- 新增或修改指导/记录文件时，同步登记状态、owner、替代关系和复核周期。
- PR 与每周定时任务运行同一个检查器；不另外维护第二套规则。
- 过期文档先复核，再更新 `last_reviewed` 或降级状态；禁止只改日期而不核对内容。
- 检查器可以报告建议降级和归档候选，但不得自动移动、删除或改写结论。
- 物理归档必须逐路径检查引用并取得用户批准；生成证据继续留在原 revision 目录。
- `AGENTS.md` 是稳定规则，不记录项目进度。正常实验推进只更新状态表和对应事实文档。
- 项目负责人审计全部 worktree 时使用 `python3 scripts/check_workspace_hygiene.py --all-worktrees --report /tmp/leo-workspaces.json`；该命令只做清单，退出成功不表示其中 worktree 可回收。
