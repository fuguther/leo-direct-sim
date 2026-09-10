#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""返工包第四组离线回归（10 项）。纯离线、无网络、无模型。
运行: python3 test_rework_regressions.py   → 全过 exit 0，任一失败 exit 1。
"""
from __future__ import annotations
import csv, importlib.util, json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import patched_checks as pc
import patched_audit as pa
import patched_novelty as pn
import ledger as ld

RESULTS = []

def case(n, name):
    def deco(fn):
        RESULTS.append((n, name, fn))
        return fn
    return deco

def run_cli(*argv, expect=0):
    r = subprocess.run([sys.executable, os.path.join(HERE, "ledger.py"), *argv],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == expect, f"exit {r.returncode} != {expect}: {r.stderr[-400:]}"
    return r

CARD_A = {"title": "卡A 观测加入链路剩余寿命", "conditions": "星历可预报拓扑", "difficulty": "断链事后才可见",
          "cause_hypothesis": "寿命不在观测向量", "possible_change": "寿命特征+掩码", "strongest_alternative": "时间展开图规划",
          "decision_shift": "动作屏蔽", "next_cheap_check": "丢弃原因三分解", "source": "test"}
CARD_B = {"title": "卡B 陈旧状态驱动振荡", "conditions": "周期状态更新", "difficulty": "羊群式过矫正振荡",
          "cause_hypothesis": "龄期不入观测", "possible_change": "age-conditioned policy", "strongest_alternative": "滞回阈值",
          "decision_shift": "观测特征", "next_cheap_check": "两队列小算例", "source": "test"}

# T1 入账与重复识别
@case(1, "实际 CLI 完成新增与重复识别")
def t1(tmp):
    L = os.path.join(tmp, "l.csv")
    cards = os.path.join(tmp, "c1.json")
    json.dump([CARD_A, CARD_B], open(cards, "w", encoding="utf-8"), ensure_ascii=False)
    run_cli("add", "--cards", cards, "--ledger", L)
    rows, _ = ld._read_ledger(L)
    assert len(rows) == 2 and all(r["op"] == "add" for r in rows)
    r = run_cli("add", "--cards", cards, "--ledger", L)
    assert "added=0 skipped=2" in r.stdout, r.stdout
    rows2, _ = ld._read_ledger(L)
    assert len(rows2) == 2  # 幂等：无新行

# T2 身份与相似度分离：同键不同内容=不同候选+线索；重试幂等
@case(2, "同批同键不同内容=不同候选身份；重复执行幂等；相似只报线索")
def t2(tmp):
    L = os.path.join(tmp, "l.csv")
    k1 = dict(CARD_A); k2 = dict(CARD_A); k2["title"] = "卡A 变体（同键不同标题，实为不同候选）"
    cards = os.path.join(tmp, "c2.json")
    json.dump([k1, k2], open(cards, "w", encoding="utf-8"), ensure_ascii=False)
    r = run_cli("add", "--cards", cards, "--ledger", L)
    assert "SIMILAR_CANDIDATES" in r.stdout, r.stdout  # 同键线索必须报告
    run_cli("add", "--cards", cards, "--ledger", L)  # 重复执行
    rows, _ = ld._read_ledger(L)
    assert len(rows) == 2 and len({r["cand_id"] for r in rows}) == 2, "同键不同内容必须是两个候选身份"
    assert all(r["version"] == "1" for r in rows), "相似不得变成另一候选的新版本"
    assert any(r["similar_to"] for r in rows), "相似线索必须写入 similar_to（后到者指向先到者）"
    proj = ld.current_projection(rows)
    assert len(proj) == 2  # 两个独立当前候选
    # 合并必须显式：merge 后 A1 归档
    cid1, cid2 = sorted(proj)
    run_cli("merge", "--cand-id", cid1, "--into", cid2, "--reason", "主控裁决：实为同一题", "--ledger", L)
    rows2, _ = ld._read_ledger(L)
    proj2 = ld.current_projection(rows2)
    assert proj2[cid1]["status"] == "merged" and proj2[cid1]["merged_into"] == cid2
    assert proj2[cid2]["status"] != "merged"

# T3 修订 → 唯一当前版本，旧记录保留
@case(3, "修订后唯一当前版本正确，旧记录保留")
def t3(tmp):
    L = os.path.join(tmp, "l.csv")
    cards = os.path.join(tmp, "c3.json")
    json.dump([CARD_A], open(cards, "w", encoding="utf-8"), ensure_ascii=False)
    run_cli("add", "--cards", cards, "--ledger", L)
    _rows, _ = ld._read_ledger(L)
    cid = _rows[0]["cand_id"]
    run_cli("revise", "--cand-id", cid, "--set", json.dumps({"difficulty": "断链只在状态里事后编码为拥塞=∞"}, ensure_ascii=False),
            "--reason", "承重字段精化", "--ledger", L)
    rows, _ = ld._read_ledger(L)
    assert len(rows) == 2
    proj = ld.current_projection(rows)
    assert len(proj[cid : ] if False else proj) == 1
    cur = proj[cid]
    assert cur["version"] == "2" and cur["op"] == "revise" and cur["supersedes_row"] == "1"
    assert cur["difficulty"].startswith("断链只在状态")
    assert rows[0]["difficulty"] == CARD_A["difficulty"]  # 旧记录保留
    run_cli("status", "--cand-id", cid, "--status", "needs_revision", "--reason", "流程验证：状态变更", "--ledger", L)
    rows3, _ = ld._read_ledger(L)
    proj3 = ld.current_projection(rows3)
    assert proj3[cid]["status"] == "needs_revision" and proj3[cid]["op"] == "status_change"
    assert len(rows3) == 3  # 只追加，不覆盖
    r = run_cli("show", "--ledger", L, "--all")
    assert "rows=3" in r.stdout

# T4 检索四态：失败/超时/解析/成功无命中 均不产生新颖性结论
@case(4, "检索 429/超时/解析错误/成功无命中分别报告，均不自动产生新颖性")
def t4(tmp):
    card = {"title": "ephemeris aware exploration gating for packet routing", "conditions": "c", "difficulty": "d", "cause_hypothesis": "h", "possible_change": "p"}
    # 服务失败（429 → keyword_query None）
    def svc(q): return {"status": pn.ST_SERVICE, "papers": [], "error": "HTTP 429", "channel": "s2"}
    out = pn.novelty_assess(card, search_fn=svc)
    assert out["verdict"] == "incomplete" and out["overall_status"] == "degraded"
    assert len(out["queries_not_executed"]) >= 1  # 断点：后续查询未执行
    # 执行异常
    def boom(q): raise TimeoutError("simulated timeout")
    out2 = pn.novelty_assess(card, search_fn=boom)
    assert out2["verdict"] == "incomplete"
    # 成功无命中
    def empty(q): return {"status": pn.ST_OK_EMPTY, "papers": [], "error": None, "channel": "s2"}
    out3 = pn.novelty_assess(card, search_fn=empty)
    assert out3["verdict"] == "no_hit_in_scope" and "限定" in out3["note"]
    # 成功有命中（低相似）→ 线索
    def hits(q): return {"status": pn.ST_OK_HITS, "papers": [{"paperId": "x", "title": "totally unrelated paper about cookies", "year": 2020}], "error": None, "channel": "s2"}
    out4 = pn.novelty_assess(card, search_fn=hits)
    assert out4["verdict"] in ("leads_only", "no_hit_in_scope")
    for o in (out, out2, out3, out4):
        assert o["verdict"] != "novel" and "novel" not in o["verdict"]

# T5 相似标题不同条件 ≠ 同一贡献
@case(5, "相似标题但不同条件不能被自动判为同一贡献")
def t5(tmp):
    t1 = "DQN routing for LEO satellite networks under congestion"
    t2 = "DQN routing for LEO satellite networks under handover"
    card = {"title": t1, "conditions": "拥塞工程化合同", "difficulty": "d", "cause_hypothesis": "h", "possible_change": "p"}
    j, ev = pn.heuristic_lead_judge(card, {"title": t2})
    assert j == "high_similarity_lead", j  # 相似 → 高相似**线索**
    assert "same" not in j
    def hits(q): return {"status": pn.ST_OK_HITS, "papers": [{"paperId": "p1", "title": t2, "year": 2025, "abstract": "handover focused"}], "error": None, "channel": "s2"}
    out = pn.novelty_assess(card, search_fn=hits, judge_fn=pn.heuristic_lead_judge)
    assert out["verdict"] == "leads_only", out["verdict"]  # 不自动 collision / 不自动 novel
    assert "已覆盖" in out["note"]  # 线索注记：相关≠已覆盖
    # 文档化旧行为（已修复）：原件对 title-only 卡会输出 collision（repro-group2.txt §B）

# T6 检查器异常 + expected=BLOCK → 审计仍失败
@case(6, "检查器异常且 expected BLOCK 时，审计失败")
def t6(tmp):
    d = os.path.join(tmp, "cases"); os.makedirs(d)
    json.dump({"id": "x1", "check": "queue_divergence", "params": {"mu": "nan", "rhos": {"a": 0.5}, "claimed_W": {"a": 1.0}},
               "expected_verdict": "BLOCK"}, open(os.path.join(d, "a.json"), "w"))
    rep = pa.run_audit(d)
    assert rep["all_ok"] is False and (rep["exec_errors"] + rep["param_errors"]) == 1, rep
    json.dump({"id": "x2", "check": "no_such_check", "params": {}, "expected_verdict": "BLOCK"},
              open(os.path.join(d, "a.json"), "w"))
    rep2 = pa.run_audit(d)
    assert rep2["unknown_checkers"] == 1 and rep2["all_ok"] is False

# T7 缺参数/空网格/占位文本不能被描述为论证成立
@case(7, "缺参数、空网格和占位文本 → 输入不足/不适用，不得 PASS")
def t7(tmp):
    assert pc.check_queue_divergence({"mu": 1.0, "rhos": {}, "claimed_W": {}})["verdict"] == pc.VERDICT_INSUF
    assert pc.check_queue_divergence({"mu": 1.0, "rhos": {"a": 0.5}, "claimed_W": {}})["verdict"] == pc.VERDICT_INSUF
    assert pc.check_correlation_causality({"causal_claim": True, "intervention_design": "TODO"})["verdict"] == pc.VERDICT_INSUF
    assert pc.check_correlation_causality({"causal_claim": False})["verdict"] == pc.VERDICT_NA
    assert pc.check_fallback_lossless({"claims_lossless": True, "significance_evidence": "TODO", "dropped_experience_analysis": "待补"})["verdict"] == pc.VERDICT_INSUF
    assert pc.check_fallback_lossless({"claims_lossless": False})["verdict"] == pc.VERDICT_NA
    assert pc.check_grid_completeness({"required_arms": [], "provided_arms": []})["verdict"] == pc.VERDICT_INSUF
    assert pc.check_grid_completeness({"required_arms": ["SP"], "provided_arms": ["TODO"]})["verdict"] == pc.VERDICT_INSUF
    assert pc.check_bounded_negative({})["verdict"] == pc.VERDICT_NA
    # 缺必需输入经 run_check → INPUT_INSUFFICIENT（非异常外泄）
    out = pc.run_check("queue_divergence", {})
    assert out["verdict"] == pc.VERDICT_INSUF

# T8 承重修订 → 相关审查失效；标点级修订不触发
@case(8, "候选承重修订后相关审查失效；标点修改不触发")
def t8(tmp):
    L = os.path.join(tmp, "l.csv"); RV = os.path.join(tmp, "rv.csv")
    cards = os.path.join(tmp, "c8.json")
    json.dump([CARD_A], open(cards, "w", encoding="utf-8"), ensure_ascii=False)
    run_cli("add", "--cards", cards, "--ledger", L)
    rows, _ = ld._read_ledger(L)
    cid, ch = rows[0]["cand_id"], rows[0]["content_hash"]
    run_cli("review-register", "--review-id", "R1", "--cand-id", cid, "--content-hash", ch,
            "--role", "evidence", "--file", "op.md", "--reviews", RV)
    run_cli("revise", "--cand-id", cid, "--set", json.dumps({"cause_hypothesis": "寿命不在观测向量（修订表述）"}, ensure_ascii=False),
            "--reason", "机制表述承重修订", "--ledger", L, "--reviews", RV)
    rrows, _ = ld._read_ledger(RV)
    assert rrows[0]["status"] == "needs_review", rrows
    # 标点级：加句号
    run_cli("review-register", "--review-id", "R2", "--cand-id", cid,
            "--content-hash", ld._read_ledger(L)[0][1]["content_hash"],
            "--role", "builder", "--file", "op2.md", "--reviews", RV)
    run_cli("revise", "--cand-id", cid, "--set", json.dumps({"title": CARD_A["title"] + "。"}, ensure_ascii=False),
            "--reason", "仅标点", "--ledger", L, "--reviews", RV)
    rrows, _ = ld._read_ledger(RV)
    st = {r["review_id"]: r["status"] for r in rrows}
    assert st["R1"] == "needs_review" and st["R2"] == "active", st
    # R3 修复1：符号改变必须触发（τ<15s → τ≤15s）
    rows_r3, _ = ld._read_ledger(L)
    run_cli("review-register", "--review-id", "R3", "--cand-id", cid,
            "--content-hash", rows_r3[-1]["content_hash"],
            "--role", "evidence", "--file", "op3.md", "--reviews", RV)
    run_cli("revise", "--cand-id", cid, "--set", json.dumps({"conditions": "屏蔽阈值 T*：τ_ho<15s"}, ensure_ascii=False),
            "--reason", "符号级承重修订", "--ledger", L, "--reviews", RV)
    rrows, _ = ld._read_ledger(RV)
    assert {r["review_id"]: r["status"] for r in rrows}["R3"] == "needs_review", "符号改变必须触发重审"
    # 纯空白差异不触发
    rows_r4, _ = ld._read_ledger(L)
    run_cli("review-register", "--review-id", "R4", "--cand-id", cid,
            "--content-hash", rows_r4[-1]["content_hash"],
            "--role", "builder", "--file", "op4.md", "--reviews", RV)
    cond_now = rows_r4[-1]["conditions"]
    run_cli("revise", "--cand-id", cid, "--set", json.dumps({"conditions": cond_now.replace(" ", "  ", 1)}, ensure_ascii=False),
            "--reason", "仅空白", "--ledger", L, "--reviews", RV)
    rrows, _ = ld._read_ledger(RV)
    assert {r["review_id"]: r["status"] for r in rrows}["R4"] == "active", "纯空白差异不得触发重审"

# T9 依赖指纹漂移被明确识别
@case(9, "依赖缺失或指纹变化被明确识别")
def t9(tmp):
    spec = importlib.util.spec_from_file_location("deps_check", os.path.join(HERE, "deps_check.py"))
    dc = importlib.util.module_from_spec(spec); sys.modules["deps_check"] = dc; spec.loader.exec_module(dc)
    manifest = os.path.join(HERE, "..", "deps", "DEPENDENCIES.md")
    assert dc.main(["--manifest", manifest]) == 0  # 真实清单应全对
    bad = os.path.join(tmp, "bad.md")
    with open(bad, "w", encoding="utf-8") as f:
        f.write("| t | " + os.path.join(HERE, "ledger.py") + " | x | " + "0" * 64 + " | y |\n")
    assert dc.main(["--manifest", bad]) == 1  # 指纹不符 → drift
    with open(bad, "w", encoding="utf-8") as f:
        f.write("| t | /nonexistent/file.py | x | " + "0" * 64 + " | y |\n")
    assert dc.main(["--manifest", bad]) == 1  # 文件缺失 → missing

# T10 中断恢复：原件不动 + 可恢复路径；多行字段不被破坏
@case(10, "CSV 含合法多行字段及损坏尾部时，原件不被破坏")
def t10(tmp):
    L = os.path.join(tmp, "l.csv")
    cards = os.path.join(tmp, "c10.json")
    card = dict(CARD_A)
    card["conditions"] = "多行条件第一行\n第二行（合法引号内换行）"
    json.dump([card], open(cards, "w", encoding="utf-8"), ensure_ascii=False)
    run_cli("add", "--cards", cards, "--ledger", L)
    with open(L, "a", encoding="utf-8") as f:
        f.write('25,cabc12345,1,add,awaiting_evidence,"残尾行被中')  # 模拟中断半行
    corrupt = open(L, "rb").read()
    r = run_cli("doctor", "--ledger", L, expect=1)
    assert open(L, "rb").read() == corrupt, "默认 doctor 不得修改原件"
    # 旧破坏性 --repair 已移除（argparse 前缀匹配 --repair-out 需参数→exit 2；无论哪种解析都不得截断台账）
    rb = subprocess.run([sys.executable, os.path.join(HERE, "ledger.py"), "doctor", "--ledger", L, "--repair"],
                        capture_output=True, text=True)
    assert rb.returncode == 2, rb.stderr
    assert open(L, "rb").read() == corrupt, "探针后原件仍不得被修改"
    rout = os.path.join(tmp, "repaired.csv")
    run_cli("doctor", "--ledger", L, "--backup", "--repair-out", rout, expect=1)
    assert open(L, "rb").read() == corrupt, "--repair-out 也不得修改原件"
    assert os.path.exists(rout)
    rep_rows, rep_bad = ld._read_ledger(rout)
    assert not rep_bad and len(rep_rows) == 1
    assert "第二行（合法引号内换行）" in rep_rows[0]["conditions"], "多行字段必须完整保留"
    # 采纳（人工 mv 模拟）后重试幂等
    os.replace(rout, L)
    run_cli("add", "--cards", cards, "--ledger", L)
    rows2, _ = ld._read_ledger(L)
    assert len(rows2) == 1, "恢复采纳后重试不得重复入账"


# T12 解析失败 ≠ 成功无命中（走 safe_search 真实分类路径）
@case(12, "检索记录解析失败被记为解析错误，不冒充成功无命中")
def t12(tmp):
    orig = pn._retrieve.keyword_query
    pn._retrieve.keyword_query = lambda q, limit=20: [{"junk": True}, {"junk2": True}]
    try:
        out = pn.safe_search("any query")
    finally:
        pn._retrieve.keyword_query = orig
    assert out["status"] == pn.ST_EXEC, out
    assert "解析失败" in (out["error"] or "")
    card = {"title": "x", "conditions": "c", "difficulty": "d", "cause_hypothesis": "h", "possible_change": "p"}
    orig2 = pn._retrieve.keyword_query
    pn._retrieve.keyword_query = lambda q, limit=20: [{"junk": True}]
    try:
        out2 = pn.novelty_assess(card)  # 默认 search_fn=safe_search
    finally:
        pn._retrieve.keyword_query = orig2
    assert out2["verdict"] == "incomplete" and out2["overall_status"] == "degraded"


def main():
    failures = []
    for n, name, fn in RESULTS:
        with tempfile.TemporaryDirectory() as tmp:
            try:
                fn(tmp)
                print(f"PASS T{n} {name}")
            except AssertionError as e:
                failures.append((n, name, str(e)))
                print(f"FAIL T{n} {name}: {e}")
            except Exception as e:
                failures.append((n, name, repr(e)))
                print(f"FAIL T{n} {name}: {e!r}")
    print(f"\nSUMMARY {len(RESULTS) - len(failures)}/{len(RESULTS)} passed")
    return 1 if failures else 0

if __name__ == "__main__":
    sys.exit(main())