# LEO Direct-Sim（leo_sim V2）

卫星直连架构的 LEO 网络路由仿真平台：不可变需求 trace、有界 SimPy 离散事件内核、显式控制平面、
位守恒 fate 账本、fail-closed 运行回执、C1/C3–C7 学习合同与 canonical Double-DQN（可选 GAT/MPNN 图编码器）。

Agent 或维护者开始工作前先读 `AGENT-START-HERE.md`；文档权威、替代关系和复核周期以 `ANALYSIS/DOCUMENT-STATUS.json` 为准。

## 谱系与引用

本平台是第三代实现：第一代为公开仓库
[SatCom-TELMA/MA-DRL_Routing_Simulator](https://github.com/SatCom-TELMA/MA-DRL_Routing_Simulator)
（Gateway 汇聚架构，Lozano-Cuadra 等），第二代为其私有演化版。本仓库为**全新实现**，
不包含第一/二代代码；如使用，请引用原始工作：

- F. Lozano-Cuadra, B. Soret, I. Leyva-Mayorga and P. Popovski, "Continual Deep Reinforcement
  Learning for Decentralized Satellite Routing," IEEE TCOM 2025, arXiv:2405.12308
- Lozano-Cuadra et al., "An open source MA-DRL routing simulator for satellite networks",
  SPAICE2024, doi:10.5281/zenodo.13885645

与旧平台（Gateway 汇聚）的逐行差异对照见
`ANALYSIS/PLATFORM-DOCUMENTATION/03-platform-diff-detailed-kimi.md`。

## 快速开始

```sh
pip install simpy numpy pyyaml  # 学习功能另需 tensorflow（无 TF 时学习路径 fail-closed）
python -m CODE.leo_sim config validate --config CODE/leo_sim/profiles/smoke.yaml
python -m CODE.leo_sim run --config CODE/leo_sim/profiles/smoke.yaml --out out/smoke
python -m CODE.leo_sim receipt verify --out out/smoke
python -m CODE.leo_sim platform check --out out/platform-check
```

测试：`python -m pytest CODE/leo_sim/tests CODE/tests -q`
（学习相关测试需要 TensorFlow；无 TF 环境下相应用例按设计 fail-closed 跳过或报错。）

## 目录

- `CODE/leo_sim/` — 平台内核与全部模块（config / trace / grid / model / kernel / control /
  outage / fates / routing / learning / receipt / governance / acceptance / platform_check /
  comparison / population），含 `tests/` 与 `profiles/`
- `CODE/experiment_platform/` — 实验编译与授权链（三角色审阅→授权→远程执行）
- `CODE/scripts/remote/` — VM 部署/运行/结果拉取脚本（配置模板见 `remote.env.template`）
- `CODE/work/` — 治理决策评估（授权链依赖）
- `CODE/legacy_trace_runtime.py` — 新旧对照臂的 trace 注入运行时；旧平台本体**不在本仓库**
  （为无许可证第三方仓库的衍生作品，存于私有旧仓库），`compare` 的 legacy 臂需外部指向它
- `CODE/data/`、`CODE/population_map/` — M-Lab 流量、geoip 站点、GPW 人口数据
- `EXPERIMENTS/` — 实验合同与正式 smoke 治理产物（原始结果永不入库）
- `ANALYSIS/` — 文档治理入口、当前研究/实验合同、平台说明书和历史证据；旧日期目录不自动代表当前科研线
- `PAPER/` — claim 门禁设施；`LITERATURE/` — 文献登记与笔记

## 硬规则

1. 实验结果（`CODE/Results/`、`leo_sim_out/` 等）永不入库。
2. 正式实验必须走：编译 → 审阅 → 授权 → 远程运行 → 自然结束回执 → 分析重算。
3. 一切承重 claim 过证据门；oracle/global 信息只标分析上界。
4. 详见 `AGENTS.md`。
