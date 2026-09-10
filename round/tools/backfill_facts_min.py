
from pathlib import Path
NEU = Path('round/knowledge/notes-neutral')
add = {
 "WEIL-2024-RMP.md": "\n- **表 4（无带宽限制）**：Ours*（action masking）reward 1.74 / throughput 3.49，静态 SP 1.77 / 3.54；§5.2 明言 \"effect of communication is very small\"，DQN 与 DGN 几乎无差。\n",
 "ARXIV-2512.00985.md": "\n- **数值（VII-D1 行~1340）**：惩罚陡峭（α=1）时，联合最优路由+等待策略的惩罚比最佳单路由低约 60%；度量取时延/交付率时改道收益不明显。\n",
 "IZHIKEVICH-2024.md": "\n- **地面段占比（Sec 7.2 方程）**：尼日利亚实测 154ms 中约 110ms 来自地面段（地面站-POP 距离被 ISL 路径拉长）。\n",
}
for fn, txt in add.items():
    p = NEU / fn
    t = p.read_text(encoding='utf-8').rstrip() + "\n" + txt
    p.write_text(t, encoding='utf-8')
    print("appended:", fn)
