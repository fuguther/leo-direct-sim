#!/usr/bin/env python3
import json, time, urllib.request, urllib.parse, re

def get(url, ua="novelty-check/1.0 (mailto:agent@example.org)"):
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8","replace"), None
    except Exception as e:
        return None, str(e)

def arxiv(q):
    parts = q.split(" AND ")
    sq = "+AND+".join("all:"+urllib.parse.quote(p.strip()) for p in parts)
    url = "http://export.arxiv.org/api/query?search_query=" + sq + "&max_results=8"
    txt, err = get(url)
    if err: return None, err
    titles = re.findall(r"<title>(.*?)</title>", txt, re.S)[1:]
    total = re.search(r"totalResults[^>]*>(\d+)", txt)
    return [t.strip().replace("\n"," ")[:110] for t in titles], (total.group(1) if total else "?")

queries = [
 "Starlink AND spectral AND periodicity AND latency",
 "LEO AND satellite AND network AND variance AND decomposition",
 "Starlink AND queue AND buffer AND bottleneck AND measurement",
 "satellite AND constellation AND reconfiguration AND periodic AND delay",
 "laser AND inter-satellite AND fixed AND on-demand AND topology",
 "satellite AND network AND congestion AND collapse AND threshold",
 "Starlink AND ground AND station AND handover AND latency AND periodic",
 "LEO AND supply AND demand AND mismatch AND routing",
]
for i,q in enumerate(queries,1):
    a, ta = arxiv(q)
    time.sleep(2)
    print(f"GROUP {i}: {q} | arXiv total={ta}", flush=True)
    print("  top3:", json.dumps(a[:3], ensure_ascii=False) if a else f"ERR {ta}", flush=True)

def s2(url, tries=4):
    for k in range(tries):
        txt, err = get(url, ua="novelty-agent")
        if not err: return json.loads(txt), None
        wait = 10*(k+1)
        print(f"  s2 err {err}, retry in {wait}s", flush=True)
        time.sleep(wait)
    return None, err

anchors = [("2310.09242","arXiv:2310.09242"),("2601.08439","arXiv:2601.08439"),("2605.27717","arXiv:2605.27717")]
for ax, sid in anchors:
    d, err = s2(f"https://api.semanticscholar.org/graph/v1/paper/{sid}?fields=title,citationCount,citations.title,citations.year")
    time.sleep(3)
    if d:
        print(f"ANCHOR {ax}: {d.get('title')} | citationCount={d.get('citationCount')}", flush=True)
        for c in (d.get("citations") or []):
            t = c.get("title","")
            flag = " <<< SUSPECT" if any(k in t.lower() for k in ["spectral","periodic","decompos","breakdown","queue","buffer","variance","on-demand","congestion","ground segment","spectr"]) else ""
            print(f"   - {t[:120]} ({c.get('year')}){flag}", flush=True)
    else:
        print(f"ANCHOR {ax}: FAILED {err}", flush=True)

for key, tq in [("ieee-11143359","Starlink ground station network latency PoP measurement"),
                ("ieee-10375570","deep reinforcement learning inter-satellite link scheduling energy LEO")]:
    d, err = s2("https://api.semanticscholar.org/graph/v1/paper/search?query="+urllib.parse.quote(tq)+"&fields=title,year,venue,citationCount,citations.title&limit=3")
    time.sleep(3)
    if not d:
        print(f"ANCHOR {key}: SEARCH FAILED {err}", flush=True); continue
    for p in (d.get("data") or []):
        print(f"ANCHOR-CAND {key}: {p.get('title')} | {p.get('venue')} {p.get('year')} | cites={p.get('citationCount')}", flush=True)
        for c in (p.get("citations") or []):
            t = c.get("title","")
            flag = " <<< SUSPECT" if any(k in t.lower() for k in ["spectral","periodic","decompos","breakdown","queue","buffer","variance","on-demand","congestion","fixed","utilization"]) else ""
            print(f"   - {t[:120]}{flag}", flush=True)
print("DONE2", flush=True)
