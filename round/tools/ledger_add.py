#!/usr/bin/env python3
"""[DEPRECATED 2026-09-10 R2] 本工具已被 ledger.py 取代（幂等/唯一当前版本/修订留痕/中断恢复）。
缺陷复现: round/logs/repro-ledger-cli.txt；保留本文件仅为复现记录配套，勿再使用。

候选入账工具：复刻 topic_harness/pool.py 的 add() 语义（只读引用其实现），外加对旧台账的复现对账。

用法: python3 ledger_add.py cards.json [--ledger round/CANDIDATE-LEDGER.csv] [--old OLD_LEDGER.csv]
cards.json: [{"title","conditions","difficulty","cause_hypothesis","possible_change",
              "strongest_alternative","decision_shift","next_cheap_check","new_evidence","source"}]
逻辑：
  - merge_key=(困难,原因,决策变化) 归一化比对（导入 pool.py 真实现，保证语义一致）；
  - 与本轮 open 卡同键且无 new_evidence → merged（不入新行，stdout 报告）；
  - 与旧台账（--old）同键：有 new_evidence → 入账并标 reopened(旧卡ID)；无 → 判 reproduces(旧卡ID)，不入账；
  - 否则 added。
只追加，绝不修改既有行。
"""
import json, sys, csv, os, importlib.util, time

RO = "/Users/lge/Desktop/leo-direct-sim/.worktrees/research-ops"
spec = importlib.util.spec_from_file_location("pool", RO + "/scripts/topic_harness/pool.py")
pool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pool)

def row_key(r):
    C = pool.CandidateCard(card_id="", title="", conditions=r.get("conditions",""),
                           difficulty=r.get("difficulty",""), cause_hypothesis=r.get("cause_hypothesis",""),
                           possible_change=r.get("possible_change",""), strongest_alternative=r.get("strongest_alternative",""),
                           decision_shift=r.get("decision_shift",""))
    return pool.merge_key(C)

def main():
    args = sys.argv[1:]
    cards = json.load(open(args[0], encoding="utf-8"))
    ledger = args[args.index("--ledger")+1] if "--ledger" in args else "round/CANDIDATE-LEDGER.csv"
    old_path = args[args.index("--old")+1] if "--old" in args else None
    olds = []
    if old_path and os.path.exists(old_path):
        with open(old_path, newline="", encoding="utf-8") as f:
            olds = list(csv.DictReader(f))
    mine = []
    if os.path.exists(ledger):
        with open(ledger, newline="", encoding="utf-8") as f:
            mine = list(csv.DictReader(f))
    for c in cards:
        C = pool.CandidateCard(card_id="", title=c["title"],
            conditions=c.get("conditions",""), difficulty=c.get("difficulty",""),
            cause_hypothesis=c.get("cause_hypothesis",""), possible_change=c.get("possible_change",""),
            strongest_alternative=c.get("strongest_alternative",""), decision_shift=c.get("decision_shift",""),
            next_cheap_check=c.get("next_cheap_check",""), new_evidence=c.get("new_evidence",""))
        key = pool.merge_key(C)
        # old-ledger recurrence judgment
        hit_old = next((o for o in olds if row_key(o) == key), None)
        if hit_old and not pool._norm(C.new_evidence):
            print(f"REPRODUCES old[{hit_old['card_id'][:30]}] :: {c['title'][:40]}")
            continue
        dup = next((m for m in mine if m["status"]=="open" and row_key(m)==key), None)
        if dup and not pool._norm(C.new_evidence):
            print(f"MERGED_INTO {dup['card_id'][:30]} :: {c['title'][:40]}")
            continue
        C.card_id = pool.new_card_id(C.title)
        C.created_at = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        C.source_run = c.get("source","topic-loop-20260910")
        if hit_old and pool._norm(C.new_evidence):
            C.merged_into = hit_old["card_id"]  # reopened of old card
            C.status = "open"
            print(f"REOPENED(old {hit_old['card_id'][:20]}) as {C.card_id[:30]}")
        elif dup:
            C.status = "open"; C.merged_into = dup["card_id"]
            print(f"REOPENED(new {dup['card_id'][:20]}) as {C.card_id[:30]}")
        else:
            C.status = "open"
            print(f"ADDED {C.card_id[:40]}")
        newfile = not os.path.exists(ledger)
        with open(ledger, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(pool.CARD_FIELDS))
            if newfile: w.writeheader()
            w.writerow(C.to_row())

if __name__ == "__main__":
    main()
