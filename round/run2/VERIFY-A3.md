# A3 独立核验记录（主控执行，2026-09-11）

> 目的：独立复核 A3 深化稿的关键主张（**must-address#1 锚件核验**），不采信其自证。

## 1. 锚件逐字核实：**通过**

**论文**：S85KQ4FC（Flow-Centric DRL for High-Throughput LEO Routing）
**位置**：MinerU MD 第 77 行（§III 实验设置段）

**原文逐字**（两处关键句）：
> "We set N_s to 12 and N_a to 4, with **F assumed to be 8**. The maximum capacity of the cache M is set at **300 packets**, and the packet arrival rate ranges from **13 000 to 21 000 packets per second (pps)**."

> "For instance, when the packet arrival rate reaches **21 000 pps** (approximately 300 Mb/s, assuming a packet size of 1500 bytes), the packet routing decision delay and packet loss ratio increase to **17.5 milliseconds (ms)** and **21%**, respectively."

| A3 主张 | 原文 | 判定 |
|---|---|---|
| F = 8（并行推理上限） | "F assumed to be 8" | ✅ 逐字一致 |
| 决策缓存 M = 300 包 | "maximum capacity of the cache M is set at 300 packets" | ✅ 逐字一致 |
| 到达率扫描 13k–21k pps | "ranges from 13 000 to 21 000 pps" | ✅ 逐字一致 |
| 21k pps 时决策时延 17.5 ms | "decision delay ... increase to 17.5 milliseconds" | ✅ 逐字一致 |
| 21k pps 时丢包 21% | "packet loss ratio ... and 21%" | ✅ 逐字一致 |
| 边界：21% 为单路由器决策缓存口径 | 原文语境为**单路由器**仿真（"simulate the DRL-based packet routing process on the router"） | ✅ **边界声明正确** |

**A3 的边界声明也对**：原文是**单路由器**实验（非网络级），且绑定该文的 DNN 参数（L_nn=3、H_l=256、N_s=12、N_a=4）——**不可外推到其他模型/硬件**。A3 写明"数字绑定 i7 合同不可外推"，正确。

## 2. 我自己的核验方法缺陷（记录）

初次抽查报 3 项 FAIL，**实为我的检索串错误**：
- 我搜 `21k` / `13k`，原文写作 **`21 000` / `13 000`**（MinerU 保留的**细空格**排版）；
- 我搜 `F = 8` 用固定串，实际含 LaTeX 包裹（`$F$`）；
- 且 `grep -c -F "300"` 这类**短串计数会产生假阳性**（匹配到任意位置的 300）。

**教训（写入核验纪律）**：
1. 核验承重数字必须**取上下文行**，不能只做子串计数；
2. 数字类断言须容忍**排版差异**（细空格、LaTeX 包裹、逗号分隔）；
3. **PASS 与 FAIL 都要复核**——假阳性与假阴性同样危险。

## 3. A3 的四层判定（主控）

| 层 | 判定 | 依据 |
|---|---|---|
| **现象有文献支持** | ✅ 成立 | 锚件 L77 逐字核实；该文**明确以"推理时延被忽视"为研究动机**（摘要首段："a crucial aspect often overlooked...pertains to the inference time of DNN models"） |
| **原因有依据** | ✅ 成立 | 机制链可写：到达率↑→推理排队→决策缓存溢出→**独立于链路拥塞的丢包通道**；锚件给出该通道的实测数字 |
| **改动对症** | ✅ 成立 | 双粒度决策（flow 级复用 + 前兆门）直接降低推理调用频次；降级规则路由作地板 |
| **简单替代仍不足** | ⚠️ **需对抗检查** | A3 自述"最强替代 = flow-centric + 静态 θ（即 S85KQ4FC 完整机制），本卡增量 = 前兆信号/滞回/准入/双通道记账四点补丁" → **须判定这四点是否够格成为研究贡献** |

## 4. 待办

- A3 的第③问需**对抗性挑战**（特别是：S85KQ4FC 本身已解决该问题，A3 只是"补丁"的话，研究贡献是否成立）；
- 该挑战应在 B3 完成后与三卡比较裁决一起做。
