# Git worktree / branch 对账（2026-08-20）

> **状态：当前治理清理审计快照，不是持续自动更新的真相源。** 采集时间：2026-08-20 14:48:22 +0800。任何删除前必须重新 fetch、复查 PR、HEAD、dirty 状态，并逐条取得用户批准。

## 1. 结论

| 分类 | 数量 | 本轮动作 |
|---|---:|---|
| `ACTIVE` | 3 | 保留；D1/D2 继续各自复核门，本治理分支继续当前 PR 流程 |
| `DIRTY-PROTECT` | 3 | 保留；不得 stash/reset/覆盖，先确认 owner 和未提交内容 |
| `MERGED-CLEANUP-CANDIDATE` | 24 | 只列候选；本轮不删除，待用户逐条批准 |
| `ORPHAN-UNVERIFIED` | 2 | 保留；存在 PR head 不一致或无远端 PR 的唯一提交风险 |
| `DETACHED-VERIFY` | 5 | 保留；需证明只是验证/deploy checkout 后才能回收 |
| **合计** | **37** | 与 `git worktree list --porcelain` 数量一致 |

事实边界：

- GitHub PR 状态来自 `gh pr list --repo fuguther/leo-direct-sim --state all ...` 官方查询。
- `MERGED` 证明 PR 已进入 GitHub 合并历史，但 worktree 删除仍是另一项破坏性操作，不能自动执行。
- `origin/*: gone` 只表示远端引用不存在，不能单独证明已合并。本表仅在 GitHub PR 为 `MERGED`、本地 HEAD 与 PR head 相同且 worktree clean 时列为回收候选。
- `reviewDecision` 为空不等于独立复核通过；D1/D2 仍按项目 exact-SHA 复核记录判断。

## 2. 逐 worktree 分类

| Path | Branch / HEAD | Dirty | GitHub / 远端证据 | 分类与原因 |
|---|---|---:|---|---|
| `/Users/lge/Desktop/leo-direct-sim` | `codex/20260819-q0-replay-gate` / `bfa08982e30924cb913ac4a23f5de26f7a0a6668` | 4 | upstream 存在；无对应 PR | `DIRTY-PROTECT`：主工作区含 3 个修改和 1 个未跟踪文件 |
| `/private/tmp/leo-d1-baseline` | detached / `b6204ebb8df8896adebf813200eaba1c764a219c` | 0 | 无 branch/PR 归属 | `DETACHED-VERIFY`：D1 同步基线，先证明用途已结束 |
| `/private/tmp/leo-d1-rate` | `codex/20260819-d1-dynamic-rate` / `408d368cd31f0990d39480eff962dd53f49bb95b` | 0 | PR #55 OPEN，head 相同 | `ACTIVE`：D1 承重改动，未达到可回收或自动合并状态 |
| `/private/tmp/leo-d2-holding` | `codex/20260819-d2-holding-integration` / `6be16cd2f471f4a343fc7e788ac7a9d6e13ff76d` | 0 | PR #56 OPEN，head 相同 | `ACTIVE`：D2 承重改动，标题仍标待复核 |
| `/private/tmp/leo-d2-topo` | `codex/20260819-d2-dynamic-topology` / `7cb11e8bc624139eb09a6f9f0e140b72b739cfbe` | 1 | 跟踪 `origin/main`，无对应 PR | `DIRTY-PROTECT`：旧 D2 原型仍有未提交测试改动 |
| `/private/tmp/leo-deploy-main` | detached / `a2a588d9f2c66f801871f762b629d183a6bab2af` | 0 | 无 branch/PR；历史 VM marker | `DETACHED-VERIFY`：需确认不再承担部署证据入口 |
| `/private/tmp/leo-doc-consolidation` | `codex/20260820-git-lifecycle-governance` / `36692d59b38cb810cab159fce2becf846290bafc` | 0 | 当前治理任务，尚未开 PR | `ACTIVE`：本表所在任务 |
| `/private/tmp/leo-exp-baseline` | `codex/20260819-experiment-baseline` / `2bf385870a06c2aa710cca93b528809b10f9c05e` | 3 | upstream 存在；无对应 PR | `DIRTY-PROTECT`：kernel/q0/q0_tiny 有未提交修改 |
| `/private/tmp/leo-fix-acclabel` | `codex/20260817-fix-acceptance-label` / `69eda44c31b09a72c98fec86ebe0ced32d3cd256` | 0 | PR #35 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-fix-burst` | `codex/20260817-fix-burst-window` / `621174ff3244883387eacfafcda5348551b57973` | 0 | PR #33 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-fix-configval` | `codex/20260817-fix-config-validation` / `274b33b85e4bcca8f1118d177f47cf5e1522a730` | 0 | PR #34 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-fix-contract` | `codex/20260817-fix-checkpoint-contract` / `2eabd729b8574f970a89b36e1e8043ec338f41af` | 0 | PR #42 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-fix-defend` | `codex/20260817-kernel-defense` / `c9921dc8a3142814b1ca717a859db7f48a071e97` | 0 | PR #37 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-fix-downlink` | `codex/20260817-fix-downlink-wake` / `7cc4ae96a74fc7329e3edcd64746367b4dc62a4f` | 0 | PR #25 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-fix-endpoints` | `codex/20260817-fix-future-endpoints` / `49cd1d8fde5d74ab31aa7a16e0d179ed2fe9cd84` | 0 | PR #28 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-fix-fifo` | `codex/20260817-fix-access-fifo` / `f1d1a1c2edabba7263d8ecfd08dc2666f0d1009a` | 0 | PR #26 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-fix-gov` | `codex/20260819-gov-checkpoint-seal` / `79e570ac60c27cb3c0bc5db2861d753ea51ac260` | 0 | PR #47 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-fix-gov2` | `codex/20260819-gov-symlink-scope` / `494b9cd131fdbef416775b69207f2344cbe62a11` | 0 | PR #51 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-fix-ledger` | `codex/20260817-fix-ledger-bits` / `a0a240d2080fabb6c780c55537754fbb5f6539df` | 0 | PR #32 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-fix-occupied` | `codex/20260817-fix-occupied-stop` / `f8004158f9febf9f2d60c5907175b2f564d42eb8` | 0 | PR #29 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-fix-remotegate` | `codex/20260817-fix-remote-gate` / `4aadb5bb898ca16a1995cae20e1ae332fa4db320` | 0 | PR #38 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-fix-reward` | `codex/20260818-fix-reward-fail` / `666c54ceaffa144fc66ad56b081be70071eb22a0` | 0 | PR #43 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-fix-snap` | `codex/20260819-snapshot-followups` / `07a42429cfa707af95a5b5b0c0e1e1f421edb903` | 0 | PR #53 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-fix-tabq` | `codex/20260817-fix-tabularq-eval` / `7d80c37d30943f38862ee221b161bd2be36d88f7` | 0 | PR #30 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-fix-trace` | `codex/20260818-fix-trace-deadline-zero` / `fc1b0a281bef460f2326c8a2dc7ef6f70a106335` | 0 | PR #44 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-fix-transmit` | `codex/20260817-fix-transmit-retire` / `cfd524cdce744e991ce2ac10f1979845bea63e1b` | 0 | PR #41 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-fix-verify` | `codex/20260817-fix-receipt-verify` / `3aa7a75d944ecc5a057433f994d2dbf21e598573` | 0 | PR #36 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-geom-cache` | `codex/20260816-geom-cache` / `16d213896fdc4bce32095458aeaffd004d7841eb` | 0 | PR #31 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-hop-bfs` | `codex/20260819-hop-bfs` / `c814e799f80832a8b698bc8520403afdf3f612b6` | 0 | PR #49 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-hunt1-doc` | `codex/20260817-hunt1-consolidation` / `10d49f7124cb4dd2ba8ddffe41dad2936a883489` | 0 | PR #27 MERGED head=`384ee6ed...`，与本地 HEAD 不同 | `ORPHAN-UNVERIFIED`：本地可能含 PR 后唯一提交 |
| `/private/tmp/leo-hunt1-review` | detached / `c8c84f56e26f90c638759a7a21d874f6db8924f7` | 0 | 无 branch/PR 归属 | `DETACHED-VERIFY` |
| `/private/tmp/leo-main-check` | detached / `522bc1ebbb5235854b0fa08adce9b3525f2a131d` | 0 | 无 branch/PR 归属 | `DETACHED-VERIFY` |
| `/private/tmp/leo-notes-dedup` | `codex/20260817-notes-dedup` / `f504c3812acfac1f491548eaa1b54f69ee2c74db` | 0 | PR #39 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-q0-merge-test` | detached / `a486c97550b3f15865ed88b2e5dc00ce182d8cfc` | 0 | 无 branch/PR；名称表示合并验证但未独立证明 | `DETACHED-VERIFY` |
| `/private/tmp/leo-q0-snapshot` | `codex/20260817-q0-snapshot` / `f64024c4cffa83a3e5b2fe09d5335e84498c1b46` | 0 | PR #40 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |
| `/private/tmp/leo-q0-tiny` | `codex/20260819-q0-tiny` / `30a84436a248695a18ef1b31538523ac92c6e9b1` | 0 | 无 upstream、无 PR | `ORPHAN-UNVERIFIED`：有唯一提交风险 |
| `/private/tmp/leo-vm-tf-fix` | `codex/20260820-vm-tf-test-contract` / `e158f9d97e28069d68b4e5669abc2ffcad2b1808` | 0 | PR #57 MERGED，head 相同 | `MERGED-CLEANUP-CANDIDATE` |

## 3. Dirty 保护清单

以下状态在本轮采集时真实存在，不能由其他任务擅自提交：

1. `/Users/lge/Desktop/leo-direct-sim`
   - `M ANALYSIS/LEGACY-FEATURE-LEDGER-20260819.md`
   - `M CODE/leo_sim/tests/test_learning.py`
   - `M NOTES.md`
   - `?? Q0_完全信息性能参照_研究目的边界与实现要求说明书.md`
2. `/private/tmp/leo-d2-topo`
   - `M CODE/leo_sim/tests/test_routing.py`
3. `/private/tmp/leo-exp-baseline`
   - `M CODE/leo_sim/kernel.py`
   - `M CODE/leo_sim/q0.py`
   - `M CODE/leo_sim/q0_tiny.py`

这些修改的作者/意图未在本轮重新确认，因此只能报告，不能替 owner 提交。

## 4. 下一步门禁

1. 先合入 Git 生命周期规则；不让治理清理与 D1/D2/Q0 行为改动混在同一 PR。
2. 对 24 个 `MERGED-CLEANUP-CANDIDATE` 在执行前重新核验 clean/HEAD/PR，然后把精确路径清单交用户批准。
3. 对两个 `ORPHAN-UNVERIFIED` 做 commit 差分审计，判断唯一内容应续作、归档还是已被 squash 等价吸收。
4. 对五个 detached checkout 查明创建目的和是否仍被部署/复核流程引用。
5. 三个 `DIRTY-PROTECT` 由其 owner 按新状态机处理：形成 checkpoint/Draft PR、明确 blocker，或保持原样并登记接手门；其他 Agent 不得代交。
