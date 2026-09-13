# Gilbert-Elliott Two-State Markov Burst-Error Model (GILBERT-ELLIOTT)

这是通信理论的奠基件而非卫星论文:Gilbert(1960)提出、Elliott(1963)推广的两态 Markov 突发错误模型——好/坏两态(G/B),坏态下误码率更高,错误成串出现;通常设好态无误码,另外三个参数由成功/失败序列反推,Gilbert 当年的例子序列太短推不出 h(出现负概率),只好假设 h=0.5。这本身就是"模型参数难标定"的活例证。NTIA TM-23-565 引它作建模基础,但该文档具体章节未获取到。无"公开代码"一说,实现极简。

> 状态: 摘要(二手来源:Wikipedia/NTIA 引注)；未核实字段: 原始两篇的准确卷期页码、NTIA TM-23-565 引用原文与章节
