# DECISIONS.md

> 本库为 2026-08-16 分拆后的新基地。旧决策全量存于旧私有仓库 `fuguther/leo-research-workspace` 的
> `DECISIONS.md` 与 `ARCHIVE-20260803/`。此处只记录新基地建立后的新决策。

- **DEC-20260816-001 新基地范围**：只含 leo_sim V2 平台、治理链（experiment_platform / scripts/remote / work）、
  数据资产与现行分析文档；旧平台代码不进本库（其为无 LICENSE 第三方公开仓库的衍生作品，公开再分发有法律风险）。
  legacy 对照臂经 `comparison.py` 配置外部指向旧库 checkout，缺失时 fail-closed。
- **DEC-20260816-002 不带 git 历史**：新库 fresh init；provenance 由旧库 + 本库 README 谱系声明承载。
- **DEC-20260816-003 私密配置不入库**：`remote.env` 等机器配置只保留模板。
