"""合并 QUALITY-GATE-R2 + LOOP-CONTROLLER -> QUALITY-GATE-R3（消除重复、明确两级轮次的区别）。"""
from pathlib import Path
R = Path("round/rules")
qg = (R / "QUALITY-GATE-R2.md").read_text(encoding="utf-8")
lc = (R / "LOOP-CONTROLLER.md").read_text(encoding="utf-8")

# 取 LOOP-CONTROLLER 的正文（去掉标题行，保留全部内容）
lc_body = lc.split("\n", 1)[1].strip()

# 把 LOOP-CONTROLLER 的 §1/§2 与 QUALITY-GATE 的 §3 合并：明确两级轮次
header = """# 质量闸门与循环控制（QUALITY-GATE-R3，2026-09-11 合并版）

> 本文件 = 原 `QUALITY-GATE-R2.md`（G1–G5 判据 + 致命项）与 `LOOP-CONTROLLER.md`（循环、并行度、终止条件、材料清单）的**合并版**。
> 合并原因：两者都定义"轮次上限"，分散在两处导致口径不一致（R5 体检发现）。
> **两级轮次的区别（本节为唯一权威）**：
> - **卡级轮次**：单张卡的"深化→审查→修订→复审"循环，≤3 轮，超限淘汰该卡（见 §3）；
> - **轮级（Round）**：整个选题循环的轮次，≤3 轮，超限触发如实报告（见 §5）。
> 两级独立计数；卡级计数由 `round/tools/gate_rounds.py` 硬记录。

---

## 第一部分：闸门（原 QUALITY-GATE-R2）
"""
# 去掉原 QG 的标题与引言，保留 §0 起正文
qg_body = qg.split("## 0.", 1)[1]
qg_body = "## 0." + qg_body
merged = header + "\n" + qg_body.rstrip() + "\n\n---\n\n## 第二部分：循环控制与材料清单（原 LOOP-CONTROLLER）\n\n" + lc_body + "\n"
(R / "QUALITY-GATE-R3.md").write_text(merged, encoding="utf-8")
print("merged ->", len(merged), "chars")