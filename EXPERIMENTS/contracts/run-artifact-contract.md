# Run 产物契约

正式比较的最小 L0 产物：

- `run_trace/run_meta.json`：schema、run/experiment/attempt ID、自然结束、中断、seed、实际方法、信息条件、配置 hash、代码 commit、created/received/lost/in-flight。
- `config_used.json`：实际执行的 canonical 配置，不从文件名还原。
- `artifact_manifest.json`：每个必要输入和输出的相对路径、字节数、SHA256、schema 和完整性。

标准 L1 产物：`experiment_bundle/summary_metrics.csv`、per-block latency、per-OD tail。诊断 L2/L3 产物按分析请求声明。缺字段必须标 `NOT_ELIGIBLE`，不得静默填 0。
