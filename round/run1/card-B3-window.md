# 候选卡 B3（深化输入 v1）

## title
run1-B3 队列感知价值的负载带塌陷窗：体制切换时的阈值失标定

## conditions
四篇拼图：LOZANO 低载1.7ms无差异/HE 50Mbps 工程化拥塞才有大收益/LIAQ 自认隔离排队防溢出+Dijkstra 理想时延最低/WEIL 无带宽限制=SP

## difficulty
队列感知价值存在窄负载带；带边界隐式改道阈值失标定→过早绕行时延↑或过晚绕行丢包↑；无一测量跨体制迁移的阈值行为

## cause_hypothesis
训练合同单一负载→策略阈值在体制切换时失标定

## possible_change
负载课程/随机化训练；隐式阈值显式化（Q差敏感度）+跨体制稳定性检验；对照 ELB/TLR 切换响应速度

## strongest_alternative
负载数率入状态（对症信息增补，最强对照）；ELB/TLR 阈值调参

## decision_shift
训练合同+评估协议

## next_cheap_check
单负载训练×5点负载扫描×（RL/ELB/SPF）画交付率-负载曲线找塌陷窗，2天

> cand_id=cc029fa6119 content_hash=hc029fa611910 status=awaiting_evidence
