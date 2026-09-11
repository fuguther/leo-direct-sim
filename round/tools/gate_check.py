#!/usr/bin/env python3
"""闸门判定器：把 G1-G5 中可机械化的部分做成硬检查。

设计哲学（沿用 patched_checks 的四态）：
  PASS  / BLOCK / INPUT_INSUFFICIENT
  —— "输入不足"绝不等于通过；"脚本没检查"绝不记 PASS。

用法: python3 gate_check.py <卡稿.md> [--json]
"""
import argparse, json, re, sys
from pathlib import Path

CITE = re.compile(r"itemKey|cite_key|\[\w{2,8}\d{2}\]|[A-Z]{2,}-\d{4}|arXiv:\d{4}\.\d{4,5}|§\s*[IVX0-9]|Table\s*\d|表\s*\d|Fig\.?\s*\d|p\.\s*\d")
FACT_TAG = re.compile(r"【原文事实】")
NOTE_TAG = re.compile(r"【笔记】")
GUESS_TAG = re.compile(r"【推演】")
UNVER_TAG = re.compile(r"【待证】")
Q1 = re.compile(r"(现有方法|为什么做不好|在什么.{0,6}条件下|困难与原因)")
Q2 = re.compile(r"(针对.{0,4}(什么)?原因|机制链|一次具体|决策或学习更新|更新式|动作|奖励|状态)")
Q3 = re.compile(r"(简单|规则路由|混合负载|微调|近邻|替代猜想|不能同样解决|为何不足)")
COUNTER = re.compile(r"(竞争解释|反方|替代解释|其他解释|竞争假设|排除)")
KILL = re.compile(r"(立即淘汰|淘汰条件|放弃条件|失效条件|不成立时)")
NOVELTY = re.compile(r"(patched_novelty|查新|最近邻|新颖性|novelty)")
NO_HIT_CLAIM = re.compile(r"(无人(做|研究)过|没有任何人|首次提出|领域空白|no prior work)")
CONTAM = re.compile(r"(对账|淘汰台账|旧卡|历史候选|run1)")

def check(text: str):
    res = []
    n = len(text)
    if n < 1500:
        res.append(("G0", "BLOCK", "卡稿过短（%d 字符），不足以保证论证完整" % n))
    else:
        res.append(("G0", "PASS", "篇幅 %d 字符" % n))

    # G1 现象成立：必须有原文事实 + 出处
    facts = FACT_TAG.findall(text)
    cites = CITE.findall(text)
    long_cites = [c for c in re.findall(r"(itemKey|cite_key)\s*[:=]?\s*\w+|\[\w{2,8}\d{2}\]", text)]
    if not facts:
        res.append(("G1", "INPUT_INSUFFICIENT", "未标注任何【原文事实】——现象无一手证据"))
    elif not cites:
        res.append(("G1", "BLOCK", "有【原文事实】但无可定位出处（篇名/节号/表号/itemKey）"))
    else:
        res.append(("G1", "PASS", "【原文事实】%d 处，可定位引用 %d 处" % (len(facts), len(cites))))
    if NO_HIT_CLAIM.search(text):
        res.append(("G1", "BLOCK", "出现领域级空白断言（无人做过/首次/领域空白）——须改为检索范围内未命中"))

    # G2 原因有依据：机制 + 竞争解释
    if not COUNTER.search(text):
        res.append(("G2", "BLOCK", "未列出竞争解释——无法排除他因"))
    else:
        res.append(("G2", "PASS", "含竞争解释/反方检查"))

    # G3 改动对症：须有可执行的决策或更新描述 + 失效条件
    if not Q2.search(text):
        res.append(("G3", "INPUT_INSUFFICIENT", "未见针对原因的改动描述"))
    elif not KILL.search(text):
        res.append(("G3", "BLOCK", "未写明失效/淘汰条件"))
    else:
        res.append(("G3", "PASS", "含改动描述与失效条件"))

    # G4 简单办法比较：须出现基线族关键词
    bases = [w for w in ("混合负载", "混载", "在线微调", "规则路由", "阈值", "最短路", "ELB", "直接近邻", "基线") if w in text]
    if len(bases) < 2:
        res.append(("G4", "INPUT_INSUFFICIENT", "简单替代比较不足（仅命中 %s）" % (bases or "无")))
    else:
        res.append(("G4", "PASS", "简单替代命中：%s" % "、".join(bases)))

    # G5 最近邻：须有查新记录
    if not NOVELTY.search(text):
        res.append(("G5", "INPUT_INSUFFICIENT", "未见最近邻/查新记录"))
    else:
        res.append(("G5", "PASS", "含最近邻/查新记录"))

    # 污染自检：深化稿不应出现历史候选身份
    if CONTAM.search(text):
        res.append(("X", "WARN", "出现历史候选相关字样（对账/run1/旧卡）——核对是否越界"))
    return res

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("card")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    text = Path(a.card).read_text(encoding="utf-8")
    res = check(text)
    bad = [r for r in res if r[1] in ("BLOCK", "INPUT_INSUFFICIENT")]
    verdict = "BLOCK" if any(r[1] == "BLOCK" for r in bad) else ("INPUT_INSUFFICIENT" if bad else "PASS")
    if a.json:
        print(json.dumps({"card": a.card, "verdict": verdict, "checks": res}, ensure_ascii=False, indent=1))
    else:
        for g, st, why in res:
            print("%-4s %-18s %s" % (g, st, why))
        print("VERDICT:", verdict)
    return 0 if verdict == "PASS" else 1

if __name__ == "__main__":
    sys.exit(main())