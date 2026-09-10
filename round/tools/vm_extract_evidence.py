#!/usr/bin/env python3
"""跨论文证据抽取（VM 端）：从转换后的全文里抽取与本课题相关的结构化证据。
方向：低轨卫星网络中，负载变化下 RL 路由如何保持到达率与端到端时延。
输出：per-paper JSON + 聚合 CSV + Evidence Atlas Markdown。自包含、无外部依赖。
用法: python3 vm_extract_evidence.py <txt_dir> <manifest.json> <out_dir> [workers]
"""
import csv, json, re, sys, time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

# 关键词组：命中即截取上下文窗，供人工/LLM 判读，不做自动结论
GROUPS = {
  "traffic_model": ["poisson", "on-off", "on/off", "self-similar", "self similar", "pareto", "cbr",
                    "constant bit rate", "bursty", "burstiness", "inter-arrival", "packet arrival",
                    "traffic model", "traffic matrix", "gravity model", "hotspot", "hot spot",
                    "uniform traffic", "non-uniform", "diurnal", "time-varying traffic", "real trace"],
  "load_level": ["load level", "traffic load", "offered load", "utilization", "saturation", "overload",
                 "light load", "heavy load", "high load", "low load", "load balancing", "congestion",
                 "queue occupancy", "buffer occupancy"],
  "train_eval": ["we train", "training", "trained with", "training scenario", "training environment",
                 "evaluation scenario", "test scenario", "unseen", "generalization", "transfer",
                 "fine-tune", "retrain", "curriculum"],
  "metrics": ["packet delivery ratio", "delivery ratio", "pdr", "packet loss", "loss rate", "drop rate",
              "end-to-end delay", "latency", "rtt", "jitter", "throughput", "goodput"],
  "load_scan": ["different load", "varying load", "various load", "load variation", "vary the load",
                "under different traffic", "load from", "loads of", "as the load increases",
                "sweep", "sensitivity analysis"],
  "burst_handle": ["burst", "spike", "flash crowd", "sudden", "transient", "steady state", "steady-state",
                   "short-term", "time scale", "timescale", "adaptation speed", "react"],
  "rl_mech": ["reward", "state space", "action space", "q-value", "policy", "actor", "critic", "dqn",
              "ppo", "mappo", "experience replay", "exploration", "convergence"],
}

WIN = 220  # 上下文窗口字符数

def contexts(text, kws, limit_per_kw=6):
    hits = {}
    low = text.lower()
    for kw in kws:
        out = []
        start = 0
        while len(out) < limit_per_kw:
            i = low.find(kw, start)
            if i < 0: break
            s = max(0, i - WIN); e = min(len(text), i + len(kw) + WIN)
            snip = re.sub(r"\s+", " ", text[s:e]).strip()
            out.append(snip)
            start = i + len(kw)
        if out: hits[kw] = out
    return hits

def numbers_near(text, pattern, window=120):
    out = []
    for m in re.finditer(pattern, text, re.I):
        s = max(0, m.start()-window); e = min(len(text), m.end()+window)
        out.append(re.sub(r"\s+", " ", text[s:e]).strip())
    return out[:8]

def process(args):
    itemKey, txt_path = args
    try:
        text = Path(txt_path).read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return {"itemKey": itemKey, "error": repr(e)[:120]}
    pages = text.count("===== PAGE ")
    rec = {"itemKey": itemKey, "chars": len(text), "pages": pages, "groups": {}}
    for g, kws in GROUPS.items():
        hits = contexts(text, kws)
        rec["groups"][g] = {"keywords_hit": sorted(hits.keys()), "n_keywords": len(hits), "samples": hits}
    # 负载数值（Mbps/Gbps/%）附近上下文
    rec["load_numbers"] = numbers_near(text, r"\d+(?:\.\d+)?\s*(?:Mbps|Gbps|kbps|%)")
    rec["page_hint"] = {}
    for g in GROUPS:
        kws = sorted(rec["groups"][g]["keywords_hit"])
        ph = {}
        for kw in kws[:4]:
            idx = text.lower().find(kw)
            if idx >= 0:
                ph[kw] = text.count("===== PAGE ", 0, idx) + 1
        rec["page_hint"][g] = ph
    return rec

def main():
    txt_dir = Path(sys.argv[1]); man = json.load(open(sys.argv[2])); out_dir = Path(sys.argv[3])
    out_dir.mkdir(parents=True, exist_ok=True)
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 64
    meta = {m["itemKey"]: m for m in man}
    jobs = [(m["itemKey"], str(txt_dir / (m["itemKey"] + ".txt"))) for m in man
            if (txt_dir / (m["itemKey"] + ".txt")).exists()]
    print("jobs:", len(jobs), flush=True)
    recs = []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for f in as_completed([ex.submit(process, j) for j in jobs]):
            recs.append(f.result())
    (out_dir / "evidence-per-paper.json").write_text(json.dumps(recs, ensure_ascii=False), encoding="utf-8")
    # 聚合 CSV
    with open(out_dir / "evidence-summary.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["itemKey","year","title","pages","chars","traffic_model_hits","load_level_hits",
                    "train_eval_hits","metrics_hits","load_scan_hits","burst_hits","rl_mech_hits"])
        for r in sorted(recs, key=lambda x: (meta.get(x["itemKey"],{}).get("year") or "", x["itemKey"]), reverse=True):
            m = meta.get(r["itemKey"], {})
            g = r.get("groups", {})
            w.writerow([r["itemKey"], m.get("year",""), m.get("title","")[:120], r.get("pages",0), r.get("chars",0)] +
                       [g.get(k,{}).get("n_keywords",0) for k in
                        ["traffic_model","load_level","train_eval","metrics","load_scan","burst_handle","rl_mech"]])
    print("wrote per-paper json + summary csv to", out_dir)

if __name__ == "__main__":
    main()