# 片段 n5：leo_sim 治理链 / 验收 / 平台检查 / 对照 / 人口流量 / CLI

范围：`CODE/leo_sim/governance.py`、`CODE/leo_sim/acceptance.py`、`CODE/leo_sim/platform_check.py`、`CODE/leo_sim/comparison.py`、`CODE/leo_sim/population.py`、`CODE/leo_sim/__main__.py`、`CODE/leo_sim/__init__.py`。所有行号经 `wc -l` 实测与逐行通读核实。

---

## 文件 `CODE/leo_sim/governance.py`（实测 257 行）

模块级说明：
- 模块 docstring（第 1–9 行）声明本模块是「retained experiment compiler/authorization chain 引用 V2 runtime 的唯一预期入口」，不接受 shell 命令、不回退到旧 Gateway runtime，把 run intent 绑定到 config SHA、trace identity 和运行时代码 SHA；声明 compile → review → authorization → run-remote 的绑定仍是 VM 阶段门禁（FACT：docstring 原文如此；其中「唯一入口」是声明性表述，代码层面未见强制机制阻止其他模块直接调用 kernel）。
- imports（第 10–18 行）：`__future__.annotations`；stdlib `hashlib`、`json`、`pathlib.Path`；同包 `config`（别名 config_mod，第 16 行）、`receipt`（第 17 行）、`trace`（第 18 行）。
- 模块级常量（FACT）：
  - `RUNTIME_KIND = "leo_sim_v2"`（第 20 行）
  - `INTENT_SCHEMA = "leo-sim-run-intent/v1"`（第 21 行）
  - `REQUEST_SCHEMA = "leo-sim-experiment-request/v1"`（第 22 行）
  - `COMPILE_REPORT_SCHEMA = "leo-sim-experiment-compile-report/v1"`（第 23 行）
  - `RUN_MANIFEST_SCHEMA = "leo-sim-experiment-run-manifest/v1"`（第 24 行）
  - `ANALYSIS_REQUEST_SCHEMA = "leo-sim-analysis-request/v1"`（第 25 行）
  - `EXECUTION_CHAIN_PATHS`（第 26–31 行）：四个相对路径元组——`CODE/experiment_platform/authorize_experiment.py`、`CODE/scripts/remote/deployment_guard.py`、`CODE/scripts/remote/remote_job.py`、`CODE/scripts/remote/run-remote.sh`。
- 无环境变量读取。

### `class IntentError` — CODE/leo_sim/governance.py:34
- 定位：CODE/leo_sim/governance.py:34
- 职责：`ValueError` 子类，空体（`pass`，第 35 行），作为本模块所有校验失败的异常类型（FACT）。
- 关键状态/结构：无自有字段或方法。
- 关键流程/方法：无方法。
- 输入/输出：由 `execution_chain_sha256`（第 45 行）、`_write_json`（第 52 行）、`build_run_intent`（第 68/71/73/78/91/94/99 行）、`compile_experiment`（第 123/127/131/135/139/145/151/155/158/164/167/169 行）抛出。
- 依赖关系：被 `CODE/leo_sim/__main__.py:76` 捕获（experiment compile 失败返回退出码 2）；`__main__.py` 还在第 87/95/99/122/126/140/144 行自行抛出同一异常类。

### `def execution_chain_sha256()` — CODE/leo_sim/governance.py:38
- 定位：CODE/leo_sim/governance.py:38
- 职责：对 `EXECUTION_CHAIN_PATHS` 列出的四个授权/部署/启动文件逐一计算 SHA-256，返回 `{相对路径: hex digest}` 字典（FACT）。
- 关键流程：以 `Path(__file__).resolve().parents[2]`（即工作区根，第 40 行）为基准拼路径；任一文件是符号链接或不是常规文件即抛 `IntentError`（第 44–45 行）。
- 输入：无参数。输出：`dict[str, str]`。
- 依赖关系：调用 stdlib `hashlib.sha256`。被本文件 `compile_experiment`（第 193 行）调用写入 planned_run；被 `CODE/experiment_platform/authorize_experiment.py:346` 和第 511–512 行调用做授权复核；测试佐证 `CODE/leo_sim/tests/test_governance.py:26`。

### `def _write_json(path, value)` — CODE/leo_sim/governance.py:50
- 定位：CODE/leo_sim/governance.py:50
- 职责：把任意值以 `json.dumps(indent=2, sort_keys=True) + "\n"` 写入指定路径；路径是符号链接时抛 `IntentError` 拒绝写入（FACT，第 51–54 行）。
- 输入：`path: Path`、`value: object`。输出：无返回值，副作用是写文件。
- 依赖关系：仅被本文件 `compile_experiment` 调用（第 183、205、217、256 行）。外部调用方未确认。

### `def build_run_intent(request, *, project_root=None)` — CODE/leo_sim/governance.py:57
- 定位：CODE/leo_sim/governance.py:57
- 职责：校验一个 experiment-request 风格的 dict 并返回「封印的」run intent dict；docstring（第 58–66 行）声明除 `runtime_kind`/`config`/`profile` 外的字段一律拒绝（fail closed）（FACT）。
- 关键流程：
  - 非 dict 抛错（第 67–68 行）；未知字段抛错（第 69–71 行）。
  - `runtime_kind` 必须等于 `"leo_sim_v2"`，否则抛错，错误消息明示「legacy Gateway runtime 永不是隐式回退」（第 72–75 行）。
  - `config` 必须是 dict（第 76–78 行），随后调 `config_mod.resolve_config(user, profile=request.get("profile"))` 得到 resolved config（第 79 行）。
  - 按 `resolved["config"]["demand"]["mode"]` 分支（第 80 行）：`csv` 模式（第 82–95 行）解析 `csv_path`——相对路径基于 `project_root`（缺省 `Path.cwd()`），提供 `project_root` 时路径逃逸（`relative_to` 失败）抛错（第 87–92 行），文件不存在或是符号链接抛错（第 93–94 行），然后对文件字节算 SHA-256 得 `input_sha256`；`mlab` 模式（第 96–100 行）对 `trace_mod.REPO_MLAB_CSV`（`CODE/leo_sim/trace.py:28` 定义）做同样校验与哈希。其他 mode 时 `input_sha256` 保持空串 `""`（第 81 行，FACT——代码无 else 分支）。
  - 返回 dict（第 101–110 行）：`schema`、`runtime_kind`、`config_sha256`（取自 resolved）、`input_sha256`、`trace_identity_sha256`（调 `config_mod.trace_identity_sha256`，config.py:564）、`code_sha256`（调 `receipt_mod.code_sha256()`，receipt.py:95）、`resolved`（完整 resolved config 字典）。
- 输入：`request: dict`，关键字 `project_root: Path | None`。输出：intent dict。
- 依赖关系：调用 `config_mod.resolve_config`、`config_mod.trace_identity_sha256`、`receipt_mod.code_sha256`。被本文件 `compile_experiment`（第 159 行）调用；被 `CODE/experiment_platform/authorize_experiment.py:320` 和第 335 行调用（授权时重建 intent 比对）；测试佐证 `CODE/leo_sim/tests/test_governance.py:12-66`、`CODE/leo_sim/tests/test_acceptance_review.py:73-77`。

### `def compile_experiment(request_path, out_dir, project_root=None)` — CODE/leo_sim/governance.py:113
- 定位：CODE/leo_sim/governance.py:113
- 职责：把一份实验请求 JSON「编译」成一组可审阅的不变产物（request.json、resolved config、run-manifest.json、analysis-request.json、RUNBOOK.md、compile-report.json）；docstring（第 115–119 行）声明编译从不授权或启动运行，输出目录必须是新或空目录（FACT）。
- 关键流程：
  - 校验 `request_path` 非符号链接且是常规文件（第 122–123 行）；读取并 JSON 解析，失败抛 `IntentError`（第 124–127 行）。
  - 请求 dict 键集合必须恰好是 `{schema, experiment_id, runtime_kind, work_finalization, acceptance, config}`（第 128–133 行）；`schema` 必须等于 `REQUEST_SCHEMA`（第 134–135 行）。
  - `experiment_id` 必须是以 `EXP-` 开头、去掉 `-`/`_` 后全字母数字的字符串（第 136–139 行）。
  - `work_finalization` 必须是以 `CODE/work/` 开头、以 `/finalization.json` 结尾且路径分量不含 `..` 的字符串（第 140–146 行）。
  - `acceptance` 必须是键集合恰为 `{min_delivered_packets, min_multisat_deliveries, require_data_isl, require_control_delivery}` 的 dict（第 147–151 行）；前两者必须是非负 int 且非 bool（第 152–155 行），后两者必须是 bool（第 156–158 行）。
  - 用请求的 `runtime_kind`/`config` 调 `build_run_intent`（第 159–162 行）。
  - 输出目录：符号链接拒绝（第 163–164 行）；已存在但不是目录或非空拒绝（第 165–169 行）；不存在则 `mkdir(parents=True)`（第 170–171 行）；建 `resolved/` 子目录（第 172–173 行）。
  - `run_id = f"{experiment_id}-main-s{seed}"`，seed 取自 resolved config 的 `scenario.seed`（第 174 行）。
  - 写 `resolved/<run_id>.leo-sim.yaml`：内容为 `{"config_version": ..., **resolved["config"]}` 的 JSON（注释第 177 行说明「JSON 是 YAML 子集」）（第 175–181 行）。
  - 写 `request.json`（第 182–183 行）并对其字节算 `request_sha`（第 184 行）。
  - 组装 `planned_run`（第 185–196 行）：含 run_id、runtime_kind、config 相对路径、config_sha256、trace_identity_sha256、input_sha256、code_sha256、`execution_chain_sha256()` 的结果、acceptance 副本、seed。
  - 写 `run-manifest.json`（第 197–205 行）：`execution_authorized: False`、`planned_runs: [planned_run]`；算其 SHA-256（第 206–207 行）。
  - 写 `analysis-request.json`（第 208–217 行）：含 `comparison_contract: "same trace identity, seed and resource config"`。
  - 生成 `RUNBOOK.md` 文本（第 218–239 行）：内嵌授权命令（`CODE/experiment_platform/authorize_experiment.py`）与启动命令（`CODE/scripts/remote/run-remote.sh --runtime-kind leo_sim_v2 ...`）。
  - 对 `out_dir` 下所有文件算 `artifact_hashes`（第 241–244 行），写 `compile-report.json`（第 245–256 行）：`status: "COMPILED_REVIEW_REQUIRED"`、`execution_authorized: False`、`launcher_generated: False`。
- 输入：`request_path: Path`、`out_dir: Path`、可选 `project_root`。输出：compile-report dict（同时写出一目录产物）。
- 依赖关系：调用 `build_run_intent`、`execution_chain_sha256`、`_write_json`。被 `CODE/leo_sim/__main__.py:74`（CLI `experiment compile`）调用；被 `CODE/experiment_platform/tests/test_authorize_experiment.py:242` 调用；测试佐证 `CODE/leo_sim/tests/test_governance.py:96/126/145`。

---

## 文件 `CODE/leo_sim/acceptance.py`（实测 153 行）

模块级说明：
- 模块 docstring（第 1–7 行）声明这是「面向结果的验收运行器」，与单元测试不同：把若干真实 Walker 几何场景跑过公开 runtime，并检查所请求机制确实在事件/归宿账本中被观察到，仅到达时界不算通过（FACT：docstring 原文；具体检查逻辑见 `_case_checks`）。
- imports（第 8–15 行）：`__future__.annotations`；stdlib `hashlib`、`json`、`time`、`pathlib.Path`；同包 `config`、`kernel`、`receipt`、`trace`（第 15 行）。
- 模块级常量（FACT）：`PROFILE_DIR = <包目录>/profiles/acceptance`（第 18 行）；`SCENARIOS = ("direct", "k1", "bbm", "mbb", "ge")`（第 19 行）。`CODE/leo_sim/profiles/acceptance/` 目录实测存在 direct.yaml、k1.yaml、bbm.yaml、mbb.yaml、ge.yaml（另有 ddqn.yaml 等）。
- 无环境变量读取。

### `class AcceptanceError` — CODE/leo_sim/acceptance.py:22
- 定位：CODE/leo_sim/acceptance.py:22
- 职责：`RuntimeError` 子类，空体（第 23 行），本模块失败异常类型（FACT）。
- 关键状态/结构：无。关键流程/方法：无方法。
- 输入/输出：由 `_case_checks`（第 90 行）、`run_acceptance`（第 139/141 行）抛出。
- 依赖关系：被 `CODE/leo_sim/__main__.py:284` 捕获（CLI 退出码 2）。

### `def _max_satellite_occupancy(events)` — CODE/leo_sim/acceptance.py:26
- 定位：CODE/leo_sim/acceptance.py:26
- 职责：从切换事件序列计算单颗卫星同时关联 endpoint 数的峰值（FACT）。
- 关键流程：维护 `{sat: {endpoint集合}}`（第 27 行）；`type == "associate"` 时加入集合并刷新最大值（第 34–36 行），`type == "release"` 时 discard（第 37–38 行）；`sat` 非 int 或 `endpoint` 非 str 的事件跳过（第 32–33 行）。
- 输入：`events: list[dict]`。输出：`int`（峰值占用数）。
- 依赖关系：仅被本文件 `_case_checks` 的 `k1` 分支调用（第 66 行）。外部调用方未确认。

### `def _case_checks(name, result)` — CODE/leo_sim/acceptance.py:42
- 定位：CODE/leo_sim/acceptance.py:42
- 职责：按场景名返回该场景的通过条件字典 `{检查名: bool}`（FACT）。
- 关键流程：所有场景共享 `common` 三项（第 47–51 行）：`natural_end is True`、`conservation_ok is True`、`fates["DELIVERED"] > 0`。各场景附加项（FACT，均直接读 result 字段）：
  - `direct`（第 52–59 行）：`occupied["isl_s"] > 0`（多星数据服务）、控制计数 `arrived > 0`、`effective["control_plane"] is True`、`routing_label != "oracle"`。
  - `k1`（第 60–67 行）：access `requests > 0`、`wait_time_s_max > 0`、`grants > 0`、`_max_satellite_occupancy(events) <= 1`（单槽位不超限）。
  - `bbm`（第 68–73 行）：事件里存在 `type == "bbm"`、access `releases["bbm_switch"] > 0`。
  - `mbb`（第 74–82 行）：事件里存在 `type == "mbb"`、`effective["mbb"] is True`、access `releases` 中存在以 `mbb_` 开头且计数 > 0 的键。
  - `ge`（第 83–89 行）：`effective["ge"] is True`、`fates["RANDOM_OUTAGE_IN_FLIGHT"] > 0`、`effective["ge_failures"] > 0`。
  - 其他名字抛 `AcceptanceError`（第 90 行）。
- 输入：场景名 `name: str`、运行结果 dict（含 `handover`/`fate_counts`/`access`/`mechanisms`/`conservation_ok`/`routing_label` 等键）。输出：`dict[str, bool]`。
- 依赖关系：调用 `_max_satellite_occupancy`。仅被本文件 `_run_case` 调用（第 116 行）。

### `def _run_case(name, out_dir)` — CODE/leo_sim/acceptance.py:93
- 定位：CODE/leo_sim/acceptance.py:93
- 职责：加载 `PROFILE_DIR/<name>.yaml`，编译 trace、跑仿真、写回执并自校验，然后按 `_case_checks` 判定 PASS/FAIL，返回该用例的结果 dict（FACT）。
- 关键流程：`config.load_config_file`（第 95 行）→ 建输出目录（`exist_ok=False`，第 96 行）→ `trace.compile_trace`（第 97 行）→ 读 trace.csv 字节并把 `__trace_sha256`、`__sha256` 两个键补进 manifest dict（第 98–101 行）→ `trace.load_trace`（第 102–106 行，horizon 与 max_packets 取自 resolved config）→ `kernel.run_simulation` 并计 wall 时间（第 107–109 行）→ `receipt.write_run`（第 110–111 行）→ `receipt.verify_receipt_dir`（第 112 行）→ 把 receipt 的 `conservation_ok`/`routing_label` 并入 observed（第 113–115 行）→ `_case_checks` 加 `receipt_verified`（第 116–117 行）→ 返回含 status/profile（相对于工作区根，第 120 行）/result_dir/wall_seconds/checks/receipt_errors/outcomes 的 dict（第 118–133 行）。
- 输入：场景名与输出目录 `Path`。输出：用例结果 dict；副作用是写出一整个 run 目录。
- 依赖关系：调用 `config.load_config_file`、`trace.compile_trace`、`trace.load_trace`、`kernel.run_simulation`、`receipt.write_run`、`receipt.verify_receipt_dir`、`_case_checks`。仅被本文件 `run_acceptance` 调用（第 145 行）。

### `def run_acceptance(out_dir)` — CODE/leo_sim/acceptance.py:136
- 定位：CODE/leo_sim/acceptance.py:136
- 职责：对 `SCENARIOS` 五个场景逐个跑 `_run_case`，汇总写 `acceptance-summary.json`，返回汇总 dict（FACT）。
- 关键流程：输出目录为符号链接（第 138–139 行）或已存在且非空/非目录（第 140–141 行）时抛 `AcceptanceError`；否则建目录（第 142 行），循环跑用例（第 143–145 行）；汇总 schema 为 `"leo-sim-acceptance/v1"`，全部用例 PASS 才总 PASS（第 146–150 行），落盘（第 151–152 行）。
- 输入：`out_dir: str | Path`。输出：`{"schema", "status", "cases"}` dict。
- 依赖关系：调用 `_run_case`。被 `CODE/leo_sim/platform_check.py:222`（mechanisms 阶段）与 `CODE/leo_sim/__main__.py:283`（CLI `acceptance run`）调用；测试中以 monkeypatch 替身出现于 `CODE/leo_sim/tests/test_platform_check.py:29、45`。

---

## 文件 `CODE/leo_sim/platform_check.py`（实测 270 行）

模块级说明：
- 模块 docstring（第 1–7 行）声明这是「面向用户的闭环检查路径，不是又一个评审层」：跑真实机制场景、保留的 Gateway/direct 同 trace 对照、以及 TensorFlow DDQN train/save/load/eval 链；首个失败阶段即停并记入 `platform-summary.json`（FACT：docstring 原文；阶段编排见 `run_platform_check`）。
- imports（第 8–18 行）：`__future__.annotations`；stdlib `copy`、`hashlib`、`importlib.metadata`、`json`、`platform`、`datetime/timezone`、`pathlib.Path`；同包 `acceptance`、`comparison`、`config`、`kernel`、`receipt`、`trace`（第 18 行）。
- 模块级常量（FACT）：`DDQN_PROFILE = profiles/acceptance/ddqn.yaml`（第 21 行）、`COMPARISON_PROFILE = profiles/comparison.yaml`（第 22 行）、`POPULATION_PROFILE = profiles/population_gravity.yaml`（第 23 行），三者均基于包目录拼接；三个文件实测存在。
- 无环境变量读取。

### `class PlatformCheckError` — CODE/leo_sim/platform_check.py:26
- 定位：CODE/leo_sim/platform_check.py:26
- 职责：`RuntimeError` 子类，空体（第 27 行），本模块失败异常类型（FACT）。
- 关键状态/结构：无。关键流程/方法：无方法。
- 输入/输出：由 `_run_population`（第 104 行）、`_run_ddqn_chain`（第 148/156 行）、`run_platform_check`（第 199/204/226/234/242/249 行）抛出。
- 依赖关系：被 `CODE/leo_sim/__main__.py:307` 捕获（CLI 退出码 9）；测试佐证 `CODE/leo_sim/tests/test_platform_check.py:72、81`。

### `def _utc_now()` — CODE/leo_sim/platform_check.py:30
第 30–31 行：返回 `datetime.now(timezone.utc).isoformat()`（FACT）。输入无；输出 ISO 格式 UTC 时间字符串。仅被本文件 `run_platform_check` 调用（第 210、257、262 行）。

### `def _write_summary(root, summary)` — CODE/leo_sim/platform_check.py:34
第 34–36 行：把 summary dict 以 `json.dumps(indent=2, sort_keys=True) + "\n"` 写到 `<root>/platform-summary.json`（FACT）。输入为目录 `Path` 与 dict；无返回值。仅被本文件 `run_platform_check` 调用（第 218、224、232、240、258、269 行）。

### `def _dependency_snapshot()` — CODE/leo_sim/platform_check.py:39
第 39–46 行：返回依赖版本快照 dict——`python` 取 `platform.python_version()`；对 `numpy`、`simpy`、`pyyaml`、`tensorflow` 逐包用 `importlib.metadata.version` 取版本，未安装时记 `None`（捕获 `PackageNotFoundError`）（FACT）。输入无；输出 dict。仅被本文件 `run_platform_check` 调用（第 212 行）。

### `def _compile_trace(resolved, trace_dir)` — CODE/leo_sim/platform_check.py:49
第 49–60 行：调 `trace.compile_trace`（第 50 行），读回 trace.csv 与 manifest.json 字节并把 `__trace_sha256`、`__sha256` 补进 manifest dict（第 51–54 行），再按 resolved config 的 duration/max_packets 调 `trace.load_trace`（第 55–59 行），返回 `(manifest, trace_bytes, rows)` 三元组（FACT）。输入：resolved config dict 与输出目录；输出三元组。被本文件 `_run_population`（第 106 行）与 `_run_ddqn_chain`（第 150 行）调用。

### `def _run_learning_arm(name, resolved, rows, trace_bytes, manifest, out_dir)` — CODE/leo_sim/platform_check.py:63
- 定位：CODE/leo_sim/platform_check.py:63
- 职责：跑一个带学习机制的仿真臂（train 或 eval），写回执并按学习账本判定 PASS/FAIL（FACT）。
- 关键流程：`kernel.run_simulation(..., learning_out_dir=out_dir/"ddqn")`（第 65–66 行）→ `receipt.write_run`（第 67–68 行）→ `receipt.verify_receipt_dir`（第 69 行）→ 取 `result["learning"]` 账本与期望 mode（第 70–71 行）→ 公共检查七项（第 72–80 行：natural_end、data_conservation、receipt_verified、delivered_data、learning_effective、mode_exact、model_save_load_verified 即 `checkpoint_verified is True`）→ train 模式加查 `train_steps > 0`（第 81–82 行）；eval 模式加查 `decisions > 0`、`train_steps == 0`、`loaded_checkpoint_sha256` 等于配置请求的 `checkpoint_sha256`（第 83–88 行）→ 返回含 status/name/result_dir/trace_sha256/fate_counts/learning/checks/receipt_errors 的 dict（第 89–98 行）。
- 输入：臂名、resolved config、trace 行、trace 字节、manifest、输出目录。输出：臂结果 dict。
- 依赖关系：调用 `kernel.run_simulation`、`receipt.write_run`、`receipt.verify_receipt_dir`。仅被本文件 `_run_ddqn_chain` 调用（第 152、168 行）。

### `def _run_population(profile, out_dir)` — CODE/leo_sim/platform_check.py:101
- 定位：CODE/leo_sim/platform_check.py:101
- 职责：用 population_gravity 配置编译 trace 并跑一臂 satellite_direct 仿真，验证人口代理流量相关声明与运行结果（FACT）。
- 关键流程：`config.load_config_file`（第 102 行）→ demand mode 必须是 `"population_gravity"`，否则抛 `PlatformCheckError`（第 103–105 行）→ `_compile_trace`（第 106–107 行）→ `kernel.run_simulation`（第 109 行）→ `receipt.write_run` + `verify_receipt_dir`（第 110–112 行）→ 从 trace 行统计源/目的 grid 集合（第 113–114 行）→ 八项检查（第 115–125 行）：manifest `provenance == "population_proxy"`、`not_calibrated_user_demand is True`、源区域数 > 1、目的区域数 > 1、natural_end、data_conservation、`DELIVERED > 0`、receipt_verified → 返回含 status/profile/result_dir/trace_sha256/offered_packets/活跃源与目的区域数/manifest 的 `population.candidate_regions` 与 `total_population`/fate_counts/checks/receipt_errors 的 dict（第 126–140 行）。
- 输入：profile 路径与输出目录。输出：阶段结果 dict。
- 依赖关系：调用 `config.load_config_file`、`_compile_trace`、`kernel.run_simulation`、`receipt.write_run`、`receipt.verify_receipt_dir`。仅被本文件 `run_platform_check` 调用（第 229 行）。

### `def _run_ddqn_chain(profile, out_dir)` — CODE/leo_sim/platform_check.py:143
- 定位：CODE/leo_sim/platform_check.py:143
- 职责：执行 DDQN train → 保存 checkpoint → 构造 eval 配置 → eval 的闭环链，并验证两段跑的是同一 trace、eval 加载的是训练出的 checkpoint（FACT）。
- 关键流程：加载配置并强制要求 `learning.algorithm == "ddqn"` 且 `mode == "train"`，否则抛 `PlatformCheckError`（第 144–148 行）→ `_compile_trace`（第 150–151 行）→ `_run_learning_arm("ddqn_train", ...)`（第 152–154 行），train 不 PASS 直接抛错并附检查 JSON（第 155–158 行）→ 取训练产物 `train/ddqn/online.keras` 的绝对路径与其 SHA-256（第 160–161 行）→ `copy.deepcopy` 配置改 eval：场景名加 `-eval` 后缀、`mode="eval"`、写入 checkpoint 路径与 SHA（第 162–166 行）→ `config.resolve_config` 重新解析（第 167 行）→ `_run_learning_arm("ddqn_eval", ...)`，注意复用同一 `rows`/`trace_bytes`/`manifest`（第 168–170 行）→ 四项汇总检查（第 172–180 行：train_passed、eval_passed、same_immutable_trace 即两臂 trace_sha256 相等、eval_loaded_trained_checkpoint）→ 返回含 status/trace_sha256/trained_checkpoint(及 SHA)/checks/train/eval 的 dict（第 181–189 行）。
- 输入：profile 路径与输出目录。输出：链式结果 dict。
- 依赖关系：调用 `config.load_config_file`、`config.resolve_config`、`_compile_trace`、`_run_learning_arm`。仅被本文件 `run_platform_check` 调用（第 245 行）。

### `def run_platform_check(out_dir, comparison_config=..., ddqn_config=..., population_config=...)` — CODE/leo_sim/platform_check.py:192
- 定位：CODE/leo_sim/platform_check.py:192
- 职责：按固定顺序编排四个阶段并汇总为单一最终结果；docstring（第 196 行）「Run every executable platform path and return one final outcome」（FACT）。
- 关键流程：
  - 输出目录：符号链接拒绝（第 198–200 行）；resolve 后已存在且非目录/非空则抛 `PlatformCheckError`（第 201–205 行）；建目录（第 206 行）。
  - 初始化 summary（第 207–217 行）：schema `"leo-sim-platform-check/v1"`、status RUNNING、起始时间、result_dir、依赖快照、以及 `evidence_scope` 声明「仅工程执行证据；本检查不证明算法优越性或经校准的物理保真度」（FACT，第 213–215 行原文）；立即落盘（第 218 行）。
  - 阶段 `mechanisms`（第 220–226 行）：调 `acceptance.run_acceptance`，写入 summary 并落盘，非 PASS 抛错。
  - 阶段 `population_traffic`（第 228–234 行）：调 `_run_population`，同样模式。
  - 阶段 `gateway_vs_direct`（第 236–242 行）：调 `comparison.run_comparison`，同样模式。
  - 阶段 `ddqn_train_eval`（第 244–249 行）：调 `_run_ddqn_chain`；注意该阶段结果写入 summary 后未立即落盘即检查（FACT：第 247–249 行之间无 `_write_summary`，失败路径由 except 分支统一落盘）。
  - 任一异常（`except Exception`，第 250–259 行）：status 置 FAIL、记录 `failed_stage` 与异常 type/message、写完成时间、落盘并返回 summary。
  - 全部通过（第 261–270 行）：status PASS、写完成时间与四项布尔 checks（all_mechanisms_ran / population_gravity_traffic_ran / same_trace_gateway_and_direct_ran / ddqn_train_save_load_eval_ran），落盘返回。
- 输入：`out_dir` 及三个可选配置路径（默认取模块级三个 PROFILE 常量）。输出：summary dict；副作用是整棵结果目录与逐阶段更新的 `platform-summary.json`。
- 依赖关系：调用 `acceptance.run_acceptance`、`comparison.run_comparison`、`_run_population`、`_run_ddqn_chain`、`_dependency_snapshot`、`_utc_now`、`_write_summary`。被 `CODE/leo_sim/__main__.py:303`（CLI `platform check`）调用；测试佐证 `CODE/leo_sim/tests/test_platform_check.py:35、61`（及 monkeypatch 第 29–30、45、55、88 行）。

---

## 文件 `CODE/leo_sim/comparison.py`（实测 271 行）

模块级说明：
- 模块 docstring（第 1–8 行）声明这是「同一条不可变需求 trace 上的一命令诊断对照」：direct 臂用 leo_sim V2，保留臂（retained arm）调 SimulationRL、关闭其内生 Gateway 流量并把同一 trace 注入其真实 Gateway 上行；声明这是需求受控的工程对照，不是算法效果实验，也不声称两套几何实现物理一致（FACT：docstring 原文）。
- imports（第 9–21 行）：`__future__.annotations`；stdlib `csv`、`hashlib`、`json`、`os`、`subprocess`、`sys`、`time`、`dataclasses.dataclass`、`pathlib.Path`；同包 `config`、`kernel`、`receipt`、`trace`（第 21 行）；第 22 行 `from CODE.legacy_trace_runtime import load_and_project_trace`（该文件存在，其 docstring 自述为「保留 Gateway runtime 的不可变需求适配器」）。
- 无模块级常量；无环境变量读取（但 `_legacy_arm` 会向子进程注入大量 `SIM_*` 环境变量，见下）。

### `class ComparisonError` — CODE/leo_sim/comparison.py:25
- 定位：CODE/leo_sim/comparison.py:25
- 职责：`RuntimeError` 子类，空体（第 26 行），本模块失败异常类型（FACT）。
- 关键状态/结构：无。关键流程/方法：无方法。
- 输入/输出：由 `_legacy_constellation`（第 59 行）、`_legacy_pathing`（第 82 行）、`_write_legacy_input`（第 90 行）、`_direct_arm`（第 112 行）、`_legacy_arm`（第 177/181/186/188 行）、`run_comparison`（第 206/211/213 行）抛出。
- 依赖关系：被 `CODE/leo_sim/__main__.py:294` 捕获（CLI 退出码 8）；测试佐证 `CODE/leo_sim/tests/test_comparison.py:47、71`。

### `class _GatewaySite` — CODE/leo_sim/comparison.py:30
- 定位：CODE/leo_sim/comparison.py:30（`@dataclass` 装饰器在第 29 行）
- 职责：承载一个旧平台 Gateway 站点的名称、经纬度与在 Gateways.csv 中的行号（FACT：字段定义如此）。
- 关键状态/结构：四个字段——`name: str`（第 31 行）、`latitude: float`（第 32 行）、`longitude: float`（第 33 行）、`active_index: int`（第 34 行）。
- 关键流程/方法：无自定义方法（dataclass 自动生成 `__init__` 等）。
- 输入/输出：由 `_gateway_sites` 构造（第 68–76 行）；被 `run_comparison` 经 `load_and_project_trace` 的投影结果按 `active_index` 筛选（第 230–232 行）；`_legacy_arm` 消费其实例列表。
- 依赖关系：仅本文件内使用。外部调用方未确认。

### `def _canonical_sha(value)` — CODE/leo_sim/comparison.py:37
第 37–39 行：对 dict 做 `json.dumps(ensure_ascii=False, sort_keys=True, separators=(",", ":"))` 序列化后取 SHA-256 hex（FACT）。输入 dict；输出 hex 字符串。仅被本文件 `_legacy_arm` 调用（第 160 行，用于构造 `SIM_EXPECTED_TRAFFIC_CONFIG_SHA256`）。

### `def _legacy_constellation(cfg)` — CODE/leo_sim/comparison.py:42
- 定位：CODE/leo_sim/comparison.py:42
- 职责：把 scenario 配置的五元组（卫星数、平面数、高度、倾角、最小仰角，第 44–48 行）映射到旧平台星座壳名称（FACT）。
- 关键流程：内置映射表（第 49–55 行）：`(32,4,1000.0,53.0,30.0)→"small"`、`(140,7,600.0,98.6,30.0)→"Kepler"`、`(66,6,780.0,86.4,30.0)→"Iridium_NEXT"`、`(648,18,1200.0,86.4,30.0)→"OneWeb"`、`(1584,72,550.0,53.0,25.0)→"Starlink"`；查不到抛 `ComparisonError`（第 56–61 行）。测试佐证 `CODE/leo_sim/tests/test_comparison.py:47`（未知星座被拒）。
- 输入：`cfg`（含 `scenario` 段的 dict）。输出：星座名字符串。
- 依赖关系：仅被本文件 `_legacy_arm` 调用（第 134 行）。

### `def _gateway_sites(code_dir)` — CODE/leo_sim/comparison.py:64
- 定位：CODE/leo_sim/comparison.py:64
- 职责：读 `<code_dir>/Gateways.csv`，把每行（DictReader 字段 `Location`/`Latitude`/`Longitude`）转成 `_GatewaySite`，`active_index` 为行号（FACT，第 64–76 行）。`CODE/Gateways.csv` 实测存在。
- 输入：`code_dir: Path`。输出：`list[_GatewaySite]`。
- 依赖关系：仅被本文件 `run_comparison` 调用（第 226 行）。

### `def _legacy_pathing(policy)` — CODE/leo_sim/comparison.py:79
第 79–84 行：把 V2 路由策略名映射为旧平台 pathing 名——`{"hop": "hop", "delay": "slant_range", "capacity": "dataRate"}`；不在表内抛 `ComparisonError`（错误消息说明「无对应非 oracle 等价物」）（FACT）。输入策略名；输出旧平台 pathing 字符串。仅被本文件 `_legacy_arm` 调用（第 143 行）。

### `def _write_legacy_input(path, gateway_names, constellation, duration_s)` — CODE/leo_sim/comparison.py:87
- 定位：CODE/leo_sim/comparison.py:87
- 职责：生成旧平台 SimulationRL 的 inputRL CSV 文件（FACT）。
- 关键流程：站点数少于 2 抛 `ComparisonError`（第 89–90 行）；写表头 `Locations,Constellation,Fraction,Test type,Test length`（第 93 行）；第一站写 `[别名, constellation, 0.5, "Latency", duration_s]`（第 96–97 行），其余站写别名加四个空字段（第 98–99 行）；别名 = 全名第一个逗号前部分（第 95 行）。
- 输入：输出路径、站点全名列表、星座名、时长秒。输出：无返回值，写 CSV 文件。
- 依赖关系：仅被本文件 `_legacy_arm` 调用（第 135 行）。

### `def _direct_arm(resolved, rows, trace_bytes, manifest, out_dir)` — CODE/leo_sim/comparison.py:102
- 定位：CODE/leo_sim/comparison.py:102
- 职责：跑 V2 内核这一臂：仿真、写回执、自校验，失败即抛错，成功返回臂摘要 dict（FACT）。
- 关键流程：建目录（`exist_ok=False`，第 104 行）→ `kernel.run_simulation` 计时（第 105–107 行）→ `receipt.write_run`（第 108–109 行）→ `receipt.verify_receipt_dir`（第 110 行）→ 非 natural_end 或有校验错误抛 `ComparisonError`（第 111–114 行）→ 返回 `runtime="satellite_direct"`、wall_seconds、trace_sha256、natural_end、conservation_ok、fate_counts、totals、mechanisms、result_dir（第 115–125 行）。
- 输入：resolved config、trace 行、trace 字节、manifest、输出目录。输出：臂摘要 dict。
- 依赖关系：调用 `kernel.run_simulation`、`receipt.write_run`、`receipt.verify_receipt_dir`。仅被本文件 `run_comparison` 调用（第 234 行）。

### `def _legacy_arm(resolved, trace_path, trace_sha, selected, out_dir, code_dir)` — CODE/leo_sim/comparison.py:128
- 定位：CODE/leo_sim/comparison.py:128
- 职责：以子进程方式跑旧平台 SimulationRL 这一臂：准备输入、注入受控环境变量、执行、校验其运行回执消费了同一 trace，返回臂摘要 dict（FACT）。
- 关键流程：
  - 建 `out_dir/results`（第 131–132 行）；调 `_legacy_constellation`（第 134 行）与 `_write_legacy_input` 生成 inputRL.csv（第 133–138 行）。
  - 构造 `trace_cfg = {"mode": "trace", "trace_sha256": trace_sha}`（第 139 行）。
  - 复制当前环境并注入变量（第 140–166 行）：`MPLBACKEND=Agg`、`SIM_PATHING`（`_legacy_pathing` 结果）、`SIM_FAST=1`、`SIM_FAIL_CLOSED=1`、`SIM_GTS=选中站点数`、`SIM_TIME_LIMIT=时长`、`SIM_MOVEMENT_TIME=步长`、`SIM_MOVEMENT_SPEEDUP=1`、`SIM_WALKER_PATTERN=delta`（第 149–152 行注释说明：旧默认约 290 倍压缩轨道时间且 Kepler 用 Walker-star 半 RAAN 布局，此处显式对齐物理秒与 Walker-delta 而不改动旧运行时其他处的默认值）、`SIM_INPUT_RL_PATH`、`SIM_TRAFFIC_TRACE_PATH`、`SIM_EXPECTED_TRAFFIC_TRACE_SHA256`、`SIM_TRAFFIC_TRACE_MAX_PACKETS`、`SIM_REQUESTED_TRAFFIC_MODE=trace`、`SIM_EXPECTED_TRAFFIC_CONFIG_SHA256`（`_canonical_sha(trace_cfg)`）、`SIM_RESULTS_ROOT`、`SIM_SEED`、`SIM_GSL_KEEP_STABLE=1`、`SIM_GSL_HANDOVER_MODE`（access.association 为 mbb 时 `"mbb"`，否则 `"legacy"`）。
  - 子进程执行 `[sys.executable, <code_dir>/SimulationRL.py]`，cwd=code_dir，stdout/stderr 并入 `legacy.log`，`check=False`（第 167–174 行）；退出码非 0 抛错（第 176–178 行）。
  - 在 `legacy_root` 下 glob `*/run_trace/run_meta.json`，必须恰好一个（第 179–182 行）；解析后要求 `trace_traffic` 是 dict 且 `valid` 为真（第 183–186 行）、其 `trace_sha256` 与本臂 trace SHA 一致（第 187–188 行）。
  - 返回 `runtime="legacy_gateway"`、wall_seconds、trace_sha256、natural_end、conservation_ok（= `trace_traffic.errors` 为空）、packets、bits、projection、result_dir、log（第 189–200 行）。
- 输入：resolved config、trace 文件路径与其 SHA、选中 `_GatewaySite` 列表、输出目录、代码目录。输出：臂摘要 dict。
- 依赖关系：调用 `_legacy_constellation`、`_write_legacy_input`、`_legacy_pathing`、`_canonical_sha`；经 `subprocess` 调 `CODE/SimulationRL.py`。仅被本文件 `run_comparison` 调用（第 238 行）。

### `def run_comparison(config_path, out_dir)` — CODE/leo_sim/comparison.py:203
- 定位：CODE/leo_sim/comparison.py:203
- 职责：编译一条不可变 trace，先后跑 satellite_direct（V2 内核）与 legacy_gateway（旧 SimulationRL 子进程）两臂，按八项检查汇总对照结论并写 `comparison-summary.json`（FACT）。
- 关键流程：
  - 输出目录 resolve 后：符号链接或已存在且非空/非目录抛 `ComparisonError`（第 204–206 行）；建目录（第 207 行）。
  - `config.load_config_file`（第 208 行）；拒绝 learning 算法非 `"none"`（第 210–211 行）；拒绝开启 GE（错误消息：断链参数未跨 runtime 校准，第 212–213 行）。
  - `code_dir = Path(__file__).resolve().parents[1]`，即 `CODE/` 目录（第 214 行）。
  - 编译 trace 到 `immutable_trace/`：与 acceptance/platform_check 相同的 manifest 补键模式（第 215–224 行）。
  - `_gateway_sites(code_dir)` 读全部站点（第 226 行）；调 `load_and_project_trace`（`CODE/legacy_trace_runtime.py`，带 `expected_sha256` 与 max_packets）把 trace 投影到站点（第 227–229 行）；收集投影实际用到的源/目的站点 `active_index`，取 `selected` 子列表（第 230–232 行）。
  - 先跑 `_direct_arm`（第 234–235 行），再建 `legacy_gateway/` 目录跑 `_legacy_arm`（第 236–239 行）。
  - 八项检查（第 240–252 行）：same_trace（两臂 SHA 均等于编译 SHA）、same_offered_bits（direct totals.offered_bits == legacy bits.offered）、direct_natural_end、legacy_natural_end、direct_conservation、legacy_conservation、direct_delivered（DELIVERED > 0）、legacy_delivered（packets.delivered > 0）。
  - 汇总 dict（第 253–268 行）：schema `"leo-sim-access-comparison/v1"`；`comparison_scope` 声明「同一不可变需求、物理时间尺度、Walker-delta 模式与壳参数；两个 runtime 的几何实现仍然不同」；`alignment`（movement_speedup=1.0、walker_pattern=delta、topology_tick_s）；`scientific_effect_claim: False`（FACT，第 262 行硬编码）；seed；两臂摘要。
  - 写 `comparison-summary.json`（第 269–270 行）并返回 summary。
- 输入：配置文件路径与输出目录。输出：summary dict。
- 依赖关系：调用 `config.load_config_file`、`trace.compile_trace`、`trace.load_trace`、`_gateway_sites`、`load_and_project_trace`、`_direct_arm`、`_legacy_arm`。被 `CODE/leo_sim/platform_check.py:237`（gateway_vs_direct 阶段）与 `CODE/leo_sim/__main__.py:293`（CLI `compare run`）调用；测试佐证 `CODE/leo_sim/tests/test_comparison.py:47、71`；monkeypatch 见于 `CODE/leo_sim/tests/test_platform_check.py:30、55`。

---

## 文件 `CODE/leo_sim/population.py`（实测 139 行）

模块级说明：
- 模块 docstring（第 1 行）：「Deterministic GPW population aggregation for V2 traffic endpoints」（FACT：原文）。其中 GPW 所指数据源在本文件内无进一步说明（未确认）。
- imports（第 2–11 行）：`__future__.annotations`；stdlib `hashlib`、`math`、`dataclasses.dataclass`、`pathlib.Path`；第三方 `numpy`（第 9 行）；同包 `grid`（第 11 行）。PIL（`from PIL import Image`）在 `load_population_regions` 内惰性导入（第 102 行）。
- 无模块级常量；无环境变量读取。

### `class PopulationError` — CODE/leo_sim/population.py:14
- 定位：CODE/leo_sim/population.py:14
- 职责：`ValueError` 子类，空体（第 15 行），本模块校验失败异常类型（FACT）。
- 关键状态/结构：无。关键流程/方法：无方法。
- 输入/输出：由 `aggregate_population_array`（第 49/55/57/62/67/74/92 行）与 `load_population_regions`（第 100/107/112/120/128 行）抛出。
- 依赖关系：测试佐证 `CODE/leo_sim/tests/test_population.py:29、50`（pytest.raises 匹配）。

### `class PopulationRegion` — CODE/leo_sim/population.py:19
- 定位：CODE/leo_sim/population.py:19（`@dataclass(frozen=True)` 在第 18 行）
- 职责：不可变记录一个聚合地理网格的人口：grid_id、中心纬度、中心经度、人口数（FACT：字段定义如此）。
- 关键状态/结构：`grid_id: str`（第 20 行）、`lat: float`（第 21 行）、`lon: float`（第 22 行）、`population: float`（第 23 行）。
- 关键流程/方法：无自定义方法。
- 输入/输出：由 `aggregate_population_array` 构造（第 90 行）；作为 `PopulationTable.regions` 的元素类型。
- 依赖关系：测试直接构造见 `CODE/leo_sim/tests/test_trace.py:122-124、164-165`。

### `class PopulationTable` — CODE/leo_sim/population.py:27
- 定位：CODE/leo_sim/population.py:27（`@dataclass(frozen=True)` 在第 26 行）
- 职责：不可变记录一次人口栅格聚合的完整结果与来源指纹（FACT：字段定义如此）。
- 关键状态/结构：`regions: tuple[PopulationRegion, ...]`（第 28 行）、`source_path: str`（第 29 行）、`source_sha256: str`（第 30 行）、`source_shape: tuple[int, int]`（第 31 行）、`source_resolution_deg: tuple[float, float]`（第 32 行）、`aggregation_deg: float`（第 33 行）、`total_population: float`（第 34 行）。
- 关键流程/方法：无自定义方法。
- 输入/输出：由 `load_population_regions` 构造返回（第 129–138 行）。
- 依赖关系：测试直接构造见 `CODE/leo_sim/tests/test_trace.py:126、167`。

### `def aggregate_population_array(values, *, west, north, pixel_lon_deg, pixel_lat_deg, aggregation_deg)` — CODE/leo_sim/population.py:37
- 定位：CODE/leo_sim/population.py:37
- 职责：把「自北向南」的二维人口栅格按规范地理网格聚合为 `PopulationRegion` 元组（FACT：docstring 第 46 行与实现一致）。
- 关键流程：
  - 转 float64 数组，必须非空二维（第 47–49 行）；五个标量参数必须有限（第 50–55 行）；像元尺寸与聚合度必须为正（第 56–57 行）。
  - `aggregation_deg` 必须是两个像元尺寸的整数倍（容差 1e-9，第 58–63 行）；且必须能整除 180 与 360（第 64–67 行）。
  - 由宽高与像元尺寸推出 east/south，范围越出地球（±180/±90，容差 1e-9）抛错（第 69–74 行）。
  - 非有限或 ≤0 的像元清零（第 76 行）；逐像元算中心经纬度（`lat = north - (row+0.5)*pixel_lat_deg`，第 79 行；`lon = west + (col+0.5)*pixel_lon_deg`，第 84 行），正人口像元经 `grid.grid_id`（`CODE/leo_sim/grid.py:21`）归入网格累加（第 77–86 行）。
  - 按 grid_id 排序，用 `grid.grid_center`（grid.py:33）取中心构造 `PopulationRegion`（第 87–90 行）；区域数少于 2 抛错（第 91–92 行）。
- 输入：二维 numpy 数组 + 栅格地理参数（仅关键字参数）。输出：`tuple[PopulationRegion, ...]`。
- 依赖关系：调用 `grid.grid_id`、`grid.grid_center`。被本文件 `load_population_regions` 调用（第 122 行）；测试直接调用见 `CODE/leo_sim/tests/test_population.py:18、30`。

### `def load_population_regions(path, aggregation_deg)` — CODE/leo_sim/population.py:96
- 定位：CODE/leo_sim/population.py:96
- 职责：读取一个全球北向 WGS84 GeoTIFF 人口栅格，聚合为 `PopulationTable` 并附来源 SHA-256 等指纹（FACT）。
- 关键流程：路径必须是常规文件且非符号链接（第 98–100 行）；函数内 `from PIL import Image` 打开，任何异常包装为 `PopulationError`（第 101–107 行）；读 GeoTIFF tag 33550（像元尺度）与 33922（tie point），缺失抛错（第 108–112 行）；取 `pixel_lon_deg/pixel_lat_deg/west/north`（第 113–114 行）；强制全球幅面校验：宽 ≈360/pixel_lon、高 ≈180/pixel_lat、west=-180、north=90（容差 1e-6，第 115–121 行）；调 `aggregate_population_array`（第 122–125 行）；总人口必须有限且 >0（第 126–128 行）；构造 `PopulationTable`（第 129–138 行）——其中 `source_path` 保留配置原拼写，第 131–132 行注释说明原因（绝对检出路径会让相同 manifest 跨机器不一致）；`source_sha256` 为文件字节 SHA-256（第 134 行）。
- 输入：GeoTIFF 路径与聚合度。输出：`PopulationTable`。
- 依赖关系：调用 `aggregate_population_array`、PIL.Image。被 `CODE/leo_sim/trace.py:329` 调用（population_gravity 流量模式的 trace 编译路径）；测试佐证 `CODE/leo_sim/tests/test_population.py:38、51`，monkeypatch 见于 `CODE/leo_sim/tests/test_trace.py:130、171`。

---

## 文件 `CODE/leo_sim/__main__.py`（实测 397 行）

模块级说明：
- 模块 docstring（第 1–11 行）列出五条 canonical CLI 用法（config validate / trace compile / run / receipt verify / platform check），并声明「处处 fail closed：未知字段、哈希不匹配、机制缺失、学习依赖不可用均以非零退出码报错」（FACT：docstring 原文；实际子命令共八个，含 docstring 未列出的 experiment compile / acceptance run / compare run，见 `main`）。
- imports（第 12–24 行）：`__future__.annotations`；stdlib `argparse`、`hashlib`、`json`、`sys`、`pathlib.Path`；同包 `acceptance`、`comparison`、`config`、`governance`、`kernel`、`learning`、`platform_check`、`receipt`、`trace`（第 20–24 行，均起 `*_mod` 别名，governance/kernel/learning 除外）。另有两处函数内惰性 import：`tempfile`（第 208 行）、`CODE.experiment_platform.authorize_experiment.verify_authorization_for_leo_sim_v2_config`（第 100–102 行）。
- 无模块级常量；无环境变量读取。

### `def _load(path)` — CODE/leo_sim/__main__.py:27
第 27–28 行：`config_mod.load_config_file(path)` 的薄封装（FACT）。输入配置路径；输出 resolved config dict。被本文件 `_cmd_config_validate`（第 33 行）、`_cmd_trace_compile`（第 59 行）、`_cmd_run`（第 185 行）调用。

### `def _cmd_config_validate(args)` — CODE/leo_sim/__main__.py:31
- 定位：CODE/leo_sim/__main__.py:31
- 职责：实现 `config validate <file.yaml> [--show]` 子命令：加载并严格校验配置，打印状态 JSON（FACT）。
- 关键流程：`ConfigError`/`FileNotFoundError` 时打印 `CONFIG INVALID: ...` 返回 2（第 32–36 行）；成功打印 `{"status": "ok", "version", "sha256"}`（第 37–38 行）；`--show` 时再打印完整 resolved config（第 39–40 行）；返回 0。
- 输入：argparse namespace（`args.file`、`args.show`）。输出：退出码 int。测试佐证 `CODE/leo_sim/tests/test_cli.py:27、33`。

### `def _compile(resolved, out_dir)` — CODE/leo_sim/__main__.py:44
第 44–54 行：调 `trace_mod.compile_trace`，读回 trace.csv 与 manifest.json 字节，把 `__trace_sha256`、`__sha256` 补进 manifest，再按 duration/max_packets `load_trace`，返回 `(manifest, trace_bytes, rows)`（FACT；与 `platform_check._compile_trace` 逻辑相同）。输入 resolved config 与输出目录；输出三元组。被本文件 `_cmd_trace_compile`（第 60 行）与 `_cmd_run`（第 216 行）调用。

### `def _cmd_trace_compile(args)` — CODE/leo_sim/__main__.py:57
- 定位：CODE/leo_sim/__main__.py:57
- 职责：实现 `trace compile --config <yaml> --out <dir>` 子命令（FACT）。
- 关键流程：`_load` + `_compile`；`ConfigError`/`TraceError`/`FileNotFoundError` 打印 `TRACE COMPILE FAILED` 返回 2（第 58–63 行）；成功打印 trace_sha256、manifest_sha256、offered_packets、offered_bits、provenance（第 64–68 行），返回 0。测试佐证 `CODE/leo_sim/tests/test_cli.py:41`（字节级可复现）。

### `def _cmd_experiment_compile(args)` — CODE/leo_sim/__main__.py:72
- 定位：CODE/leo_sim/__main__.py:72
- 职责：实现 `experiment compile --request <json> --out <dir>` 子命令：调 `governance.compile_experiment`，`project_root` 固定为 `Path.cwd()`（FACT，第 74–75 行）。
- 关键流程：`governance.IntentError` 打印 `EXPERIMENT COMPILE FAILED` 返回 2（第 76–78 行）；成功打印 compile-report JSON 返回 0（第 79–80 行）。

### `def _project_root_for(path)` — CODE/leo_sim/__main__.py:83
第 83–87 行：从 `path` 自身向上逐级找同时含 `CODE/leo_sim/` 与 `EXPERIMENTS/` 目录的祖先，作为项目根返回；找不到抛 `governance.IntentError`（FACT）。输入路径；输出 `Path`。仅被本文件 `_verify_formal_args` 调用（第 104 行）。

### `def _verify_formal_args(args, resolved)` — CODE/leo_sim/__main__.py:90
- 定位：CODE/leo_sim/__main__.py:90
- 职责：处理正式运行（formal run）的授权参数：三参数（`--authorization`/`--launch-nonce`/`--expect-run-id`）要么全不给（返回 `None`，非正式运行，第 91–93 行），要么全给（缺一抛 `IntentError`，第 94–96 行）（FACT）。
- 关键流程：`launch_nonce` 必须是 32 位小写十六进制（第 97–99 行）；惰性导入 `verify_authorization_for_leo_sim_v2_config`（第 100–102 行）；解析 config 绝对路径、项目根、授权文件路径并调该函数验证（第 103–107 行）；返回 formal dict：run_id、launch_nonce、authorization_sha256（授权文件字节哈希）、config_sha256、code_sha256（`receipt_mod.code_sha256()`）、results_dir（`<根>/CODE/Results`）（第 108–115 行）。
- 输入：args namespace 与 resolved config。输出：`dict | None`。
- 依赖关系：调用 `_project_root_for`、`CODE/experiment_platform/authorize_experiment.py` 的 `verify_authorization_for_leo_sim_v2_config`、`receipt_mod.code_sha256`。仅被本文件 `_cmd_run` 调用（第 191 行）。

### `def _write_formal_witness(out_dir, formal, receipt_payload)` — CODE/leo_sim/__main__.py:118
- 定位：CODE/leo_sim/__main__.py:118
- 职责：正式运行自然结束后写「证人」文件 `formal_run.json` 并在结果目录的兄弟目录 `_run_receipts/` 下写以 launch_nonce 命名的指针文件（FACT）。
- 关键流程：输出目录 resolve 后必须等于 `<results_dir>/<run_id>`，否则抛错（第 120–123 行）；先自校验回执目录，有错抛错（第 124–127 行）；写 `formal_run.json`：schema `"leo-sim-formal-run/v1"` + formal 除 results_dir 外的字段 + receipt_sha256 + natural_end + conservation_ok（第 128–137 行）；`_run_receipts` 目录是符号链接则抛错（第 138–141 行）；指针文件是符号链接也抛错（第 142–144 行）；写入输出目录绝对路径（第 145 行）。
- 输入：输出目录、formal dict、回执 dict。输出：无返回值，写两个文件。
- 依赖关系：调用 `receipt_mod.verify_receipt_dir`。仅被本文件 `_cmd_run` 调用（第 260 行）。

### `def _load_precompiled(resolved, trace_dir)` — CODE/leo_sim/__main__.py:148
- 定位：CODE/leo_sim/__main__.py:148
- 职责：消费已编译的不可变 trace（docstring 第 149–150 行声明：trace scope 身份与 resolved config 不符即 fail closed）（FACT）。
- 关键流程：`manifest.json`/`trace.csv` 必须都是常规文件且非符号链接（第 151–156 行）；manifest 必须是 JSON object（第 157–162 行）；用 `config.trace_identity_sha256(resolved, manifest["input_sha256"])` 重算期望身份，与 manifest 的 `trace_identity_sha256` 不等即抛 `TraceError`（第 163–169 行）；trace.csv 字节哈希与 manifest `trace_sha256`（若存在）不符抛错（第 170–173 行）；补 `__trace_sha256`/`__sha256` 键（第 174–175 行）；`load_trace` 返回 `(manifest, trace_bytes, rows)`（第 176–180 行）。测试佐证 `CODE/leo_sim/tests/test_cli.py:108`。
- 输入：resolved config 与 trace 目录。输出：三元组。
- 依赖关系：调用 `config.trace_identity_sha256`（经第 163 行函数内 `from . import config as _config`）、`trace_mod.load_trace`。仅被本文件 `_cmd_run` 调用（第 214 行）。

### `def _cmd_run(args)` — CODE/leo_sim/__main__.py:183
- 定位：CODE/leo_sim/__main__.py:183
- 职责：实现 `run --config <yaml> [--out <dir>] [--dry-run] [--expect-trace-sha256 <hex>] [--authorization <f> --launch-nonce <h> --expect-run-id <id>]` 子命令——V2 仿真的主入口（FACT）。
- 关键流程：
  - 加载配置失败打印 `CONFIG INVALID` 返回 2（第 184–188 行）。
  - `_verify_formal_args` 抛任何异常打印 `RUN REFUSED (formal authorization)` 返回 3（第 190–194 行）。
  - 输出目录取 `--out` 或配置 `outputs.out_dir`（第 195 行）；formal 模式下目标已存在且非空/符号链接/非目录则拒绝返回 3（第 196–204 行）。
  - `--dry-run` 且未指定 `--out` 时用 `tempfile.TemporaryDirectory()` 作输出，注释说明 dry-run 不在工作区写运行产物（第 205–210 行）。
  - 配置含 `outputs.trace_path` 时走 `_load_precompiled`，否则 `_compile` 现编译；`TraceError`/`FileNotFoundError` 返回 2（第 211–219 行）。
  - `--expect-trace-sha256` 与实际不符返回 2（第 220–224 行）。
  - 组装 plan dict（第 225–241 行）：config_sha256、trace_sha256、code_sha256、offered_packets/bits、active_endpoints、horizon_s、三项执行上限（max_events/max_entities/max_packets）、机制五元组（routing policy、access association、control_plane enabled、ge_enabled、learning algorithm）。
  - `--dry-run`：打印 `{"status": "DRY RUN", **plan}` 返回 0，不跑仿真（第 242–244 行）。
  - `kernel.run_simulation`（learning 算法为 ddqn 时传 `learning_out_dir=<out>/ddqn`）（第 245–250 行）；`learning.LearningUnavailable` 返回 3、`kernel.CapExceeded` 返回 4（第 251–256 行）。
  - `receipt_mod.write_run` 写回执（第 257 行）；formal 且 natural_end 时 `_write_formal_witness`，失败返回 6（第 258–263 行）。
  - 打印结果 JSON（status ok/interrupted + plan + natural_end + fate_counts + conservation_ok），natural_end 返回 0，否则返回 5（第 264–269 行）。
- 输入：args namespace。输出：退出码 int（0/2/3/4/5/6）。
- 依赖关系：本文件内调 `_load`、`_verify_formal_args`、`_load_precompiled`、`_compile`、`_write_formal_witness`；跨模块调 `kernel.run_simulation`、`receipt_mod.write_run`/`code_sha256`、`trace_mod` 编译/加载。被 `main` 经 `set_defaults` 绑定（第 348 行）；测试佐证 `CODE/leo_sim/tests/test_cli.py:52、60、83、98、108`。VM 上由 `CODE/scripts/remote/remote_job.py:250` 以 `python -m CODE.leo_sim run --config ... --authorization ...` 形式发起（另见 `CODE/tests/test_remote_workspace_scripts.py:261` 的命令前缀断言）。

### `def _cmd_receipt_verify(args)` — CODE/leo_sim/__main__.py:272
第 272–278 行：实现 `receipt verify <dir>`：调 `receipt_mod.verify_receipt_dir`，有错误打印 `FAILED` + 错误列表返回 2，否则打印 `verified` 返回 0（FACT）。测试佐证 `CODE/leo_sim/tests/test_cli.py:60、70`（篡改后校验失败）。

### `def _cmd_acceptance_run(args)` — CODE/leo_sim/__main__.py:281
第 281–288 行：实现 `acceptance run --out <dir>`：调 `acceptance_mod.run_acceptance`；`AcceptanceError` 打印 `ACCEPTANCE REFUSED` 返回 2；成功打印 summary，PASS 返回 0 否则返回 7（FACT）。

### `def _cmd_compare_run(args)` — CODE/leo_sim/__main__.py:291
第 291–298 行：实现 `compare run [--config <yaml>] --out <dir>`：调 `comparison_mod.run_comparison`；`ComparisonError` 打印 `COMPARISON FAILED` 返回 8；成功打印 summary，PASS 返回 0 否则返回 8（FACT：失败与拒跑同为 8）。

### `def _cmd_platform_check(args)` — CODE/leo_sim/__main__.py:301
第 301–311 行：实现 `platform check --out <dir> [--comparison-config ...] [--ddqn-config ...] [--population-config ...]`：调 `platform_check_mod.run_platform_check` 并透传三个配置路径；`PlatformCheckError` 打印 `PLATFORM CHECK REFUSED` 返回 9；成功打印 summary，PASS 返回 0 否则返回 9（FACT）。

### `def main(argv=None)` — CODE/leo_sim/__main__.py:314
- 定位：CODE/leo_sim/__main__.py:314
- 职责：argparse 入口，注册全部子命令并分发到各 `_cmd_*` 处理器，外加两层兜底异常网（FACT）。
- 关键流程：prog 名 `"python -m CODE.leo_sim"`（第 315 行）；子命令树（第 318–379 行）：`config validate`（位置参数 file + `--show`）、`trace compile`（`--config`/`--out` 必填）、`experiment compile`（`--request`/`--out` 必填）、`run`（参数见 `_cmd_run`，第 339–348 行）、`receipt verify`（位置参数 dir）、`acceptance run`（`--out` 必填）、`compare run`（`--config` 默认 `profiles/comparison.yaml`、`--out` 必填）、`platform check`（`--out` 必填，三个配置默认值分别指向 `profiles/comparison.yaml`、`profiles/acceptance/ddqn.yaml`、`profiles/population_gravity.yaml`，第 369–379 行）。分发（第 381–383 行）；兜底一：`ConfigError`/`TraceError` 打印 `FAILED` 返回 2（第 384–388 行，注释称其为各处理器遗漏路径的 fail-closed 网）；兜底二：`ValueError`/`TypeError`/`KeyError`/`OSError`/`JSONDecodeError` 打印 `FAILED (fail closed)` 返回 2（第 389–393 行，注释称公共入口不得暴露裸 traceback）。
- 输入：可选 argv 列表。输出：退出码 int。
- 第 396–397 行：`if __name__ == "__main__": sys.exit(main())`。
- 依赖关系：分发到本文件全部 `_cmd_*`。调用方：命令行 `python -m CODE.leo_sim`（文档 `CODE/README.md:10` 示例为 `platform check`；VM 正式路径 `CODE/scripts/remote/remote_job.py:250`）；测试中直接 `main([...])` 见 `CODE/leo_sim/tests/test_cli.py` 多处与 `CODE/leo_sim/tests/test_review_round4.py:20`（import main）。

---

## 文件 `CODE/leo_sim/__init__.py`（实测 11 行）

模块级说明：
- 包 docstring（第 1–9 行）：声明 `leo_sim` 是「formal LEO simulation platform V2 runtime」，并给出正式数据路径：不可变需求 trace → 稀疏地理 TrafficEndpoint → 有限卫星接入服务 → 卫星 ingress → ISL 路由 → 本地目的可见性发现 → 有限下行 → 目的 TrafficEndpoint；末行声明「旧 runtime 的 Gateway 概念在本包中不存在」（FACT：docstring 原文；其中 Gateway 概念缺席这一点与本片段范围一致——`comparison.py` 的 Gateway 相关代码全部位于对旧运行时的进程外调用侧）。
- 唯一语句：`__version__ = "2.0.0"`（第 11 行，FACT）。
- 无 imports、无常量、无环境变量读取、无符号定义。
- 依赖关系：作为包初始化文件被所有 `CODE.leo_sim.*` / `leo_sim.*` 导入间接触发；`__version__` 的直接读取方在 CODE/ 下未确认（grep 未见引用）。
