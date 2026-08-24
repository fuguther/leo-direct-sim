# EXP-20260824-ISL-BANDWIDTH-PILOT-R02 结果与 claim 审阅

> **EVIDENCE-SNAPSHOT**：绑定 exact main
> `d3a116a69912dd214d89582a7b29c947f2357bfa` 与 analysis manifest SHA
> `bc69740ec1cb5f201a79cf4749908c64e7ff4f49196b0dde7ee412bb95a6eb23`。
> 原始 `CODE/Results/` 不入库；本文件不能脱离 manifest、raw artifact hash、external
> witness 和双端 receipt verification 单独作为结果来源。

## 核证事实

- 两个授权 cell 均 natural end、conservation 通过，governance
  `research_eligible=true`，且 VM 与本地精确 Python 3.11.15/锁定依赖环境的
  `receipt verify` 均为 `verified`。
- 两臂实际 trace SHA 均为
  `f6981c327f4c36e659d3f7b5ef66128f94a199d0203591401c88ed0e8ab22de4`；
  trace identity、input、code 和 controlled signature 相同。预注册的唯一声明干预为
  `links.rf_isl.bandwidth_hz` 的 500 MHz→50 MHz。
- `isl_link_utilization_max` 为 `0.005871255030063291`→
  `0.020761875237929505`，b50−b500=`0.014890620207866214`，`n_pairs=1`。
  最大 link 两臂均为 `isl:222:242`，served bits 均为 `131000000`，sampled
  available-capacity bits 为 `22312095000`→`6309642000`。
- 1120 条有向 ISL 均未饱和；MCS zero-rate holds 均为 0。数据 fate 完全相同：
  1,299 offered、1,295 delivered、4 `NO_ROUTE`、0 in-system；control counters
  也完全相同。
- 全部 link 的 served bits、service-window 数和逐 link available time（均 30 s）相同；
  224/1120 link 的 available sample count 相差 1--2。b500 的 sample-count 分布为
  `{30:840,31:224,32:56}`，b50 为 `{30:952,31:168}`。独立冷审后的原始 ledger
  重算否定了“retired-generation drain 导致总 available time 不同”的初始解释；差异
  更符合 bandwidth 改变 SNR/MCS threshold 分段数量。主指标最大 link 的 sample count
  在两臂均为 30。
- raw `receipt.json` 的 `research_eligible=false` 与 governance 的 `true` 不矛盾：
  `receipt.expected_research_eligible()` 和 kernel 明确禁止本地 artifact 自授权；
  `remote_job.build_v2_governance_receipt()` 才在外部 review/authorization/deployment、
  receipt 重验、execution-chain 和 nonce witness 通过后赋予正式资格。

## 当前裁决

最强可支持表述为：在这个固定 topology、routing、traffic trace、horizon 与 seed 的
工程场景内，将声明的 ISL RF bandwidth 从 500 MHz 改为 50 MHz，与最大
horizon-aggregate 有向 ISL 利用率由约 0.59% 增至约 2.08% 同时出现；两臂仍无
ISL 饱和，数据包命运没有变化。

不能写成：纯容量乘数因果效应、拥塞开始阈值、50 MHz 已是 pressure arm、算法优越性、
信息价值、Q0 最优性、一般化结论或论文统计证据。bandwidth 同时改变噪声、SNR、MCS、
控制包服务时间和部分 retired-generation drain/denominator window；单 seed 和单 scenario
也无法排除流量映射、路由热点与时间窗口偶然性。

## 下一步与停止条件

- 不直接扩成大矩阵。先做预编译、审阅、授权的小型低带宽 bracket，保持现有 trace、
  seed、routing、topology、access、demand 和 horizon 不变；每次只降低 bandwidth，按
  serial fail-closed 顺序运行。
- 分析前筛选优先考虑 `5/2/1 MHz`，而不是直接采用信息量偏低的 `25/12.5 MHz`。
  依据当前最大 link 的 `131000000` served bits、30 s horizon 和 MCS 最大谱效
  `5.900855`，若该 link served bits 不变，则 5/2/1 MHz 的理论利用率下界约为
  `0.148/0.370/0.740`；0.5 MHz 的全时窗理论最大容量仅 `88512825` bits，不能维持
  同一 link 的 131 Mbit 服务量。它们只是预运行 bracket 设计依据，不是实测预测；正式
  候选值和 pressure 判据仍必须在新 request 中冻结并审阅，不能看完结果后改阈值。
- 找到 bracket 前只用一个固定 seed 做成本控制的工程扫描；找到候选 onset 后才在相邻
  两档补至少 3 个预注册 seed，并同时报告逐有向 link 分子/分母、饱和标记、queue area、
  fate、MCS 和 control 诊断。若达到 zero-rate hold、非自然结束、receipt/witness 不合格，
  立即停止 cohort，不把失败点包装成拥塞数据。
- 如果降低 bandwidth 仍只改变分母而不改变 served bits、queue 或 fate，应转向“增加与
  当前路径相交的预注册 offered load / OD hotspot”作为独立第二轴，不能在同一小扫描中
  同时改 bandwidth 与 traffic 而丢失归因。

## 审阅状态

- Codex 本地证据复核：完成。
- 独立冷审：`PASS_WITH_LIMITS`。通过范围仅是上述单 scenario/seed 工程描述；冷审提出的
  “本地 Python 版本不匹配”open item 未被终判采纳，因为本轮已另建精确 Python 3.11.15
  与锁定依赖环境，且 VM/本地均实际返回 `verified`。
- Kimi 外审：ProjectPilot host 的 endpoint/锁与 backend 选择故障修复后，已派发
  operation `offload-operation:0e5d47be8640e25dae9756dda39fa545`，绑定 exact code
  `d3a116a69912dd214d89582a7b29c947f2357bfa`。主审通道返回
  `EVIDENCE_READY/PASS_WITH_LIMITS`；独立通道两次在证据中写入非
  typed-reference 的 `github.com`，被校验器 fail-closed 拒收，整个 operation
  终态为 `FAILED`。因此只记“Kimi 主审候选证据已返回，独立通道未通过合同”，
  不冒充双通道外审通过。主审提出“先扩 seed/再转 demand 轴”的路线未被 Codex
  采纳：它会偏离本轮只改 bandwidth 的预注册问题，且现有 `5/2/1 MHz`
  bracket 证据更直接；仍先定位 onset，再在相邻档补预注册 seed。
