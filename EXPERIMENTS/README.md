# 实验区

Agent 不在这里手写完整配置。先提交一个紧凑请求，再由 `CODE/experiment_platform/compile_experiment.py` 生成完整配置、run manifest 和分析请求。

```text
EXP-.../
├── request.json
├── compile-report.json
├── run-manifest.json
├── analysis-request.json
├── resolved/             # <arm>.s<seed>.config.json（唯一机器真相源）
├── attempts/
└── raw/                 # 默认不进 Git
```

`RUNS.csv` 是索引，不是结论真相源。每个 arm×seed 必须有独立 resolved config 与 hash；配置和结果归属来自 manifest、run identity、effective receipt 与 artifact manifest，禁止从目录名解析科研参数。

`authorization.json` 只能由 `PLATFORM/authorize_experiment.py` 根据 ACCEPTED 工作包
finalization 生成。它是可重算的执行凭证，不是可手写的状态标记；任何被绑定的
request、manifest、analysis、config、brief、decision 或 review receipt 变化都会使其失效。
