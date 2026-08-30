# 新基地（GitHub 新仓库）建设方案与取舍清单

> **SUPERSEDED**：新仓库建设已经完成，本文只保留当时的取舍证据，不是当前任务书。现行入口见 `../../AGENT-START-HERE.md`。

> 日期：2026-08-15。依据：工作区全量盘点（CODE/、ANALYSIS/ 17 子目录 + 15 散文件、EXPERIMENTS/ 43 个 EXP、PAPER/、LITERATURE/、ARCHIVE-20260803/）。
> 两条独立的轴：**(a) 进不进新库**（我提议，你确认）；**(b) 删不删本地**（只列出，逐条等你批准；不批准就永远保留）。
> 总原则：新库 = 新平台及其直接依赖 + 现行科研资产；旧平台代码不进新库（法律上它是无许可证第三方仓库的衍生作品，见下）。

## 1. 新库结构建议（白名单）

```
CODE/__init__.py                # 包结构锚点（leo_sim 以 CODE.leo_sim 被调用）
CODE/leo_sim/                   # 新平台全部：19 模块 + tests/ + profiles/（1.6M）
CODE/experiment_platform/       # 授权链（leo_sim/__main__.py:100 直接 import）
CODE/scripts/remote/            # 远程执行 4 脚本（governance.py:27-30 计入执行链 SHA）
CODE/legacy_trace_runtime.py    # 138 行，本工作区自研，comparison.py:22 硬 import
CODE/data/                      # 5.7M：M-Lab 流量、昼夜模式、geoip 站点
CODE/population_map/            # 1.9M：GPW TIFF + 人口图
CODE/tests/                     # 只保留与 leo_sim 相关的部分（见 §4 待定项）
ANALYSIS/PLATFORM-DOCUMENTATION/# 两平台说明书 + 差异对照（本次产出）
ANALYSIS/ROUTING-OBSERVATION-AGE-20260814/  # 当前科研最前线（E0/E1 正式结果）
ANALYSIS/HOTSPOT-MODE-AUDIT-20260803/       # AGENTS.md 硬事实 7 引用
ANALYSIS/PLATFORM-V2-*.md（LOCAL-IMPLEMENTATION / VM-HANDOFF / POPULATION-TRAFFIC-*）
EXPERIMENTS/contracts/ + EXPERIMENTS/README.md + EXP-20260813-LEO-V2-FORMAL-SMOKE-R02/
PAPER/                          # claim 门禁设施（现行）
LITERATURE/SOURCES.csv + related-work-notes/（不含论文全文 txt，见 §5 版权注意）
AGENTS.md / NOTES.md / DECISIONS.md（新库重写精简版，历史版留旧库）
.gitignore（Results/、leo_sim_out/、__pycache__/、.DS_Store、.env）
README.md / LICENSE（自己选）
```

legacy 对照臂：`comparison.py` 需要的 `CODE/SimulationRL.py` 留在旧私有仓库，以配置路径方式外部指向，缺失时 fail-closed（语义与现在一致）。

## 2. 不进新库但建议本地保留（旧库当档案馆）

- `CODE/SimulationRL.py` 及旧平台 13 个外围模块、`CODE/run.py`、`CODE/config/`、`input*.csv`、`Gateways.csv`、`CODE/monitor.py`、`CODE/work/`、`CODE/tools/`（除非确认 leo_sim 链不用）
- `ANALYSIS/REBUILD-20260803/`（VM 部署/删除回执、GitHub 盘点，唯一凭证）、`VM-CLEANUP-20260802/`（删除决策回执）、`LEGACY-RESULTS-SALVAGE-20260716/`（经验文档）
- `ANALYSIS/PLATFORM-V2-REMEDIATION*.md` 三轮审查链（过程凭证）
- `EXPERIMENTS/EXP-20260813-LEO-V2-FORMAL-SMOKE-R01`（被 R02 取代，但作为轮次史保留）
- `ARCHIVE-20260803/` 整体（pre-rebuild 归档，维持不动）

## 3. 建议删除候选（逐条等你批准；分组列出）

**G1 四网关流量校准时代（你点名的那类，共 8 目录 + 1 文件）**
- `EXPERIMENTS/EXP-20260715-TRAFFIC-CALIBRATION/`、`-R02`、`-R03`、`-R04`（4 网关 uniform/gravity/burst 校准批，结论不适用于 leo_sim）
- `EXPERIMENTS/EXP-20260715-VM-SMOKE/`、`-R02`、`-R03`、`-R04`（旧平台基建 smoke，已被 V2 smoke 链取代）
- `CODE/inputRL_legacy_4gt.csv`（文件名即标 legacy_4gt）

**G2 旧平台论文批（UNVERIFIED_LEGACY，共 17 目录 + 9 文件）**
- `EXPERIMENTS/EXP-20260717-PAPER-12H-*`（MAIN/ABLATION/EVAL-S142·S143·S144-R01·R02 等 9 个）+ `EXP-20260718-PAPER-CROSS-EVAL-T42/T43/T44-R01` + `EXP-20260719-PAPER-SEED-EXT-R01`
- `ANALYSIS/PAPER-12H-EVAL-R02/`、`PAPER-CROSS-EVAL-R01/`、`PAPER-FIGURES-20260719/`
- `ANALYSIS/` 顶层 6 个旧出图 .py（compare_graph_execution_ab / paired_analysis / plot_cross_eval / plot_eval_r02 / plot_paper_figures / plot_seed_extension_eval）+ `ANALYSIS/tests/`（3 个文件，只测这 6 个脚本）

**G3 加速线（已 BLOCK 收口，共 15 目录 + 2 目录）**
- `EXPERIMENTS/EXP-20260716-GRAPH-CPU-*`（5 个，且用 h2 热点流量，后被审计为静默退化）、`EXP-20260717-EXEC-AB-*`（10 个）
- `ANALYSIS/GRAPH-EXECUTION-DIAGNOSTIC-20260716/`、`EXEC-AB-20260717/`

**G4 空目录/失效指针/使命完成（共 5 项）**
- `EXPERIMENTS/EXP-20260717-PAPER-12H-MATRIX-R01/`（空）、`ANALYSIS/requests/`（空）
- `EXPERIMENTS/manifests/`（指向已被 VM-CLEANUP 删除的数据）
- `ANALYSIS/PLATFORM-DIRECT-ACCESS-VM-AUDIT-20260731/`、`PLATFORM-MECHANISMS-20260802/`（pre-rebuild 审计，使命已由 leo_sim 完成）

**G5 可删可留（我建议留）**
- `EXPERIMENTS/EXP-20260717-RAAC-SMOKE-R01/R02/-020-R01`（旧平台算法 smoke，无后续引用）

## 4. 待定项（需要你或进一步核实）

- `CODE/tests/`（1.0M）：混有旧平台测试与 leo_sim 相关测试（test_runtime_effect_*、test_legacy_trace_runtime 等服务于对照臂）。进新库前需逐个分类。
- `CODE/scripts/` 里 remote/ 之外的部分（616K 总量）：需确认哪些属于现行部署链。
- `CODE/work/`、`CODE/tools/`：work 工具与杂项，需确认 leo_sim 链是否引用。
- `EXPERIMENTS/templates/experiment-request.example.json`：旧 compile 链模板，但 compile_experiment 仍在现行对照路径使用。
- `EXPERIMENTS/README.md`：引用了已不存在的路径 `PLATFORM/compile_experiment.py`，无论进不进新库都应修正。

## 5. 两个风险提示

1. **版权**：`LITERATURE/related-work-notes/` 内有论文全文 txt（papers-txt/）。若新库将来公开，第三方论文全文不能上传；SOURCES.csv 和自写笔记可以。
2. **许可证**：旧平台代码（SimulationRL.py 等）是无 LICENSE 第三方公开仓库（SatCom-TELMA/MA-DRL_Routing_Simulator）的衍生作品，公开再分发有法律风险——这是旧平台不进新库的硬理由之一。新库 README 应引用原始论文（arXiv 2405.12308、Zenodo 13885645）说明谱系。

## 6. 执行步骤（你批准清单后）

1. 处置当前工作区脏状态（NOTES.md 改动 + PLATFORM-DOCUMENTATION/ 未跟踪）：在旧库先 commit（需你授权）。
2. 新建目录按 §1 白名单拷贝；fresh `git init`（不带历史，历史留旧库）。
3. 新写 AGENTS.md/NOTES.md/DECISIONS.md 精简版、README（含谱系引用）、LICENSE、.gitignore。
4. 跑 leo_sim 测试套件，全绿才做第一个 commit；tag `v2.0.0-base`。
5. GitHub 建私有仓库并 push；公开与否等 bug 分诊和验收阶梯过后再定。
6. 旧仓库 README 加一行指向新库，本身归档只读。
