# Agent 实验协议

本平台的一等用户是 Agent。网页只用于人类查看同一份参数目录，不拥有独立默认值或规则。

## Agent 必须提交什么

复制 `EXPERIMENTS/templates/experiment-request.example.json`，只填写：

1. 研究问题、假设和可证伪条件；
2. 实验角色：探索、诊断、确认或全局信息上界；
3. 基础 profile；
4. 本次允许变化的参数路径；
5. 各 arm 的角色、方法族、信息条件、预算、checkpoint lineage 和少量差异；
6. seed、主指标、必要产物与完整的分析预注册。

Agent 不应复制整份配置，也不应从旧 run 名称猜参数。

## 编译

```bash
python3 CODE/experiment_platform/compile_experiment.py \
  EXPERIMENTS/templates/experiment-request.example.json \
  --out EXPERIMENTS/EXP-YYYYMMDD-NNN
```

编译器读取 `parameter-catalog.json`、`profiles.json` 和 `metric-catalog.json`，生成：

- `request.json`：进入编译的原始请求快照；
- `resolved/<arm>.s<seed>.config.json`：每个 arm×seed 唯一的不可变机器配置，直接交给 `run.py`；
- `run-manifest.json`：计划运行、seed、信息条件、完成契约和产物要求；
- `analysis-request.json`：分析问题、主指标、排除规则和不能推出什么；
- `compile-report.json`：阻塞错误、警告、使用的 profile 和 hash。

只要 `compile-report.json` 有 error，Agent 就不得生成启动命令。

## 设计规则

- strict 设计必须恰有一个无修改的 `control` arm、恰有一个变化因素，且不得使用 `coupled_parameters`。
- 技术耦合或多因素设计只能使用 `exploratory_multi_factor`，不得声称单因素因果。
- 编译器比较实际展开后的配置；未生效、未接线或控制因素外的差异会直接 BLOCK。
- 探索性多因素组合允许运行，但必须写 `one_change_policy=exploratory_multi_factor`，且不能声称单因素因果。
- 每个 arm 分别声明训练、评估、部署的信息集合；编译器根据实际配置推导并逐项核对。
- `oracle_global_dijkstra` 只能用于 `upper_bound` 角色。
- 当前训练恢复链未证明能可靠恢复完整状态；`warm_start` 与 `exact_resume` 都会被阻断。
- `code-compatibility-v1` 只是兼容性参考，不得用于 confirmatory 实验。
- 编译只产生 `execution_authorized=false` 的设计产物；独立设计复核通过前不能启动。
- 旧实验结论和旧 profile 不自动成为默认值。发现默认冲突时必须显式选择并记录。

## Agent 交接

设计者输出后，所有实验固定由三个独立角色审阅：`cold_start` 检查可理解性和合同完整性，`satellite_drl` 检查领域有效性、公平性与信息条件，`adversarial` 主动寻找反例和绕过。三者都绑定当前编译产物并 PASS 后才可授权；不能在 brief 中少声明角色来降低门槛。

## 从审阅通过到执行

1. 生产者把完整编译目录作为工作包产物，所有审阅回执绑定其 hash。
2. 决策者写入 ACCEPT 后，用 `CODE/work/finalize_decision.py` 生成可重算的
   `agent-work-finalization/v1` 回执。
3. 运行授权器：

```bash
python3 CODE/experiment_platform/authorize_experiment.py \
  --experiment EXPERIMENTS/EXP-... \
  --finalization ARCHIVE-20260803/WORK/WP-.../rNN/finalization.json \
  --out EXPERIMENTS/EXP-.../authorization.json
```

4. 逐个运行传入同一授权：

```bash
python3 CODE/run.py \
  --config EXPERIMENTS/EXP-.../resolved/<arm>.s<seed>.config.json \
  --authorization EXPERIMENTS/EXP-.../authorization.json
```

授权器和 `run.py` 都会重算 brief、decision、审阅回执、编译产物与逐 run
canonical config hash。只有 `status=AUTHORIZED` 而无法重建证据链的文件无效。
任何审阅后修改都使旧授权失效，需要新 revision 复审。`--dry-run` 可免授权，
但只表示配置预览；无 platform provenance 的真实运行会被明确拒绝。
