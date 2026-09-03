# 三图模式与对抗轮模板（放量用，2026-09-03）

## 地图模式（门C 承重格式）
每条目严格四字段，缺一回炉：
- claim/assumption/evidence: 一句话陈述
- from: [笔记ID列表]（≥1，回引 DEEPDIVE/notes/<id>.md）
- quote: 笔记中的逐字引用编号（如 n2410.15546#q3）
- confidence: 全文级 / 摘要级 / 检索级
承重测试：对抗代理必须能仅引用地图条目完成一轮猎杀；引不了则地图重建。

## 对抗第 2 轮弹药清单（来自金丝雀对抗轮自报"弹药不足"四类）
放量检索时并入以下词表组：
1. 星历误差传播：TLE error propagation / ephemeris uncertainty / orbital prediction error
2. SDN/控制稳定性理论：control loop stability delay / SDN consistency update / control plane oscillation
3. 非同源实测 trace：Starlink measurement dataset / RIPE Atlas satellite / real trace LEO routing
4. 分布式 CGR 收敛：distributed CGR / contact plan dissemination delay / CGR convergence

## 对抗轮任务书模板（异源强模型）
输入：三图 + 被攻选题卡 → 输出：猎杀记录（每论点引地图条目ID）+ 判定（淘汰/再收窄/存活+改写）+ 弹药不足声明。
禁止：为杀而杀；无引用论点无效。
