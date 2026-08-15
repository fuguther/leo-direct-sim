# 论文素材区

论文只消费同时满足以下条件的 claim：

- claim `status` 为 `SUPPORTED` 或 `SUPPORTED_LIMITED`；
- 证据门为 `PASS`；
- 价值门为 `KEEP` 或 `PROMOTE`；
- 两道门引用两份不同的、hash 可核的独立审阅回执；
- 回执绑定的 claim candidate 和 evidence 产物在当前工作区内存在且 hash 相符。
- 每条 evidence 都是 `ANALYSIS/**/analysis-manifest.json`；其预注册输入、run 产物和分析输出 hash 仍全部有效。
- 两份回执的 `subject_sha256` 都等于当前 Claim 承重字段的 canonical hash；不能“审 A、发表 B”。

使用：

```bash
python3 PAPER/eligible_claims.py
```

脚本的 stdout 只是 eligible claim 的 JSON 数组。当前登记表为空时输出 `[]`。不满足门槛的 claim 不会被“带警告输出”，而是直接排除。

临时会议图、无 manifest 的截图、缺 cohort 的表和历史 `RESEARCH_TRUTH` 文字不得直接进入正式稿。

这里验证的是可审计的文件与流程身份声明，并不声称字符串形式的 Agent 身份具有密码学不可伪造性。实际生产者、证据审阅者和价值审阅者必须在不同任务中运行。
