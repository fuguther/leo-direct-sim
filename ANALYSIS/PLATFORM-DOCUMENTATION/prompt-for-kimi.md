# 给 Kimi 的独立平台说明书任务提示词

> 本文件是「派给 Kimi 的任务描述」原文。主脑（Codex）另有一份自己的说明书，
> 两份独立产出、最后对照。Kimi 只做事实性通读说明，不做任何迁移/优劣判断。

## 你的角色

你是一名严谨的代码考古学家。你的唯一任务是：通读一个卫星网络路由仿真平台的两套实现（旧实现 + 新实现），各自产出一份结构化、可追溯到代码行的说明书。

你不评判哪个好、哪个该删、哪些东西丢了没丢。那些是主脑的终判，你只负责把「代码里到底有什么、每部分做什么、怎么做」讲清楚、讲全。

## 硬性纪律（违反即不合格）

1. 不编造：每一句「这个模块做什么」都必须能在代码里找到对应实现，并标注 `文件:行号`。找不到就写「未确认」，不许猜。
2. 不跳过：所有顶层 `class` 和顶层 `def` 都必须覆盖到，不许只挑「重要的」讲。
3. 不评价：不写「这个设计好/差」「这个应该保留/删除」「旧版比新版强」。
4. 不推断未实现的：代码里没有的功能，不要凭名字或注释脑补出行为。
5. 区分事实与推测：能确定的写 FACT，从命名/注释/上下文推测的写 INFERENCE，两者必须分开标注，不许混成一段。

## 通读范围

### 旧平台（Gateway 汇聚路径，主文件约 1.2 万行）

位于仓库 `CODE/` 下，主文件 + 它 import 的本地模块都要覆盖：

- `CODE/SimulationRL.py`（约 12556 行，核心单体）
- `CODE/traffic_od.py`、`CODE/traffic_burst.py`、`CODE/traffic_diurnal.py`、`CODE/traffic_mlab.py`（流量/需求生成）
- `CODE/link_outage.py`（链路中断）
- `CODE/routing_mappo.py`、`CODE/routing_multistep.py`、`CODE/routing_path_credit.py`（路由/学习算法扩展）
- `CODE/temporal_encoder.py`（时序编码）
- `CODE/legacy_trace_runtime.py`（trace 注入运行时）
- `CODE/monitor.py`、`CODE/runtime_effect_receipt.py`（监控/回执）

### 新平台（卫星直连，模块化内核，约 7000 行）

位于仓库 `CODE/leo_sim/` 下，全部覆盖：

- `config.py`（版本化 YAML 配置 + SHA）
- `trace.py`（不可变需求 trace 编译器 + manifest）
- `grid.py`（规范地理网格 ID）
- `model.py`（Walker-delta 星座几何）
- `kernel.py`（有界 SimPy 离散事件内核）
- `control.py`（控制平面 / ControlPacket）
- `outage.py`（几何失效 + Gilbert-Elliott 中断）
- `fates.py`（数据包 fate 账本 + 位守恒）
- `routing.py`（hop/delay/capacity/oracle 路由）
- `learning.py`（C1/C3-C7 学习合同 + Double-DQN）
- `receipt.py`（运行回执 + fail-closed 验证）
- `governance.py`（治理链接口）
- `acceptance.py`、`platform_check.py`、`comparison.py`、`population.py`

（`leo_sim/tests/` 不要求逐行读，但可作为行为佐证引用。）

## 产出格式

两份说明书合并在一个 Markdown 里，分两卷：第一卷「旧平台说明书」、第二卷「新平台说明书」。

每一卷内部，按「文件 → 模块/类/顶层函数」三级组织。对每一个类或顶层函数，写一段，固定包含以下字段（缺一不可）：

1. 定位：`文件:行号`（类/函数定义处）。
2. 职责：一句话说清它管什么。
3. 关键状态/结构：它持有或操作的核心数据（队列、缓存、图、账本、权重等）。
4. 关键流程/方法：它的主要方法各自做什么（逐方法一句话）。
5. 输入/输出：吃什么、吐什么。
6. 依赖关系：它调用谁、被谁调用（至少指出同文件内或跨文件的主要调用边）。

对纯工具函数（哈希、日志、绘图、序列化等），可以归成一小节批量说明，但不能漏掉，也要给 `文件:行号`。

## 你最后交付什么

一份 Markdown，开头写明：你实际读到了哪些文件、每个文件多少行（用 `wc -l` 实测，不许写约数）；你覆盖了多少个类、多少个顶层函数（数出来）；哪些地方你标注了 INFERENCE（列出清单）；哪些地方你标注了「未确认」（列出清单）。

正文就是第一卷 + 第二卷的逐项说明。

## 禁止出现

- 「大体上」「基本就是」「主要是」「差不多」这类模糊措辞。
- 没有 `文件:行号` 的「这个模块做 X」陈述。
- 对「新旧哪个好、东西丢没丢、该不该迁移」下结论。

## 你的工作方式

先用 `wc -l` 和 `rg` 提取每个文件的顶层 `class`/`def` 清单，确认总数，再逐个定位、通读、写说明。顺序建议：先旧平台主文件 `SimulationRL.py`（按行号从上到下），再旧平台依赖模块，最后新平台 `leo_sim`（按模块）。
