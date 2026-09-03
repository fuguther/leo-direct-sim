#!/usr/bin/env python3
import json, time, urllib.request, urllib.parse, re

def get(url, ua="novelty-check/1.0 (mailto:agent@example.org)"):
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8","replace"), None
    except Exception as e:
        return None, str(e)

# diagnose arXiv format
for sq in ["all:Starlink", "all:Starlink+AND+all:latency"]:
    txt, err = get("http://export.arxiv.org/api/query?search_query="+sq+"&max_results=3")
    if txt:
        total = re.search(r"totalResults[^>]*>(\d+)", txt)
        titles = re.findall(r"<title>(.*?)</title>", txt, re.S)[1:4]
        print(f"DIAG [{sq}] total={total.group(1) if total else '?'} titles={titles}", flush=True)
    else:
        print(f"DIAG [{sq}] ERR {err}", flush=True)
    time.sleep(2)

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
    parts = [f"all:{p.strip()}" for p in q.split(" AND ")]
    sq = "+AND+".join(parts)
    txt, err = get("http://export.arxiv.org/api/query?search_query="+sq+"&max_results=8")
    time.sleep(2)
    if not txt:
        print(f"GROUP {i} ERR {err}", flush=True); continue
    total = re.search(r"totalResults[^>]*>(\d+)", txt)
    titles = [t.strip().replace("\n"," ")[:110] for t in re.findall(r"<title>(.*?)</title>", txt, re.S)[1:]]
    print(f"GROUP {i}: {q} | arXiv total={total.group(1) if total else '?'}", flush=True)
    print("  top3:", json.dumps(titles[:3], ensure_ascii=False), flush=True)

def s2(url, tries=5):
    for k in range(tries):
        txt, err = get(url, ua="novelty-agent")
        if not err: return json.loads(txt), None
        wait = 15*(k+1)
        print(f"  s2 {err} retry {wait}s", flush=True)
        time.sleep(wait)
    return None, err

for ax in ["2310.09242","2605.27717"]:
    d, err = s2(f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{ax}?fields=title,citationCount,citations.title,citations.year")
    time.sleep(4)
    if d:
        print(f"ANCHOR {ax}: {d.get('title')} | citationCount={d.get('citationCount')}", flush=True)
        for c in (d.get("citations") or []):
            t = c.get("title","")
            flag = " <<< SUSPECT" if any(k in t.lower() for k in ["spectral","period","decompos","break","queue","buffer","variance","on-demand","congestion","ground segment","drop","bottleneck"]) else ""
            print(f"   - {t[:120]} ({c.get('year')}){flag}", flush=True)
    else:
        print(f"ANCHOR {ax}: FAILED {err}", flush=True)

d, err = s2("https://api.semanticscholar.org/graph/v1/paper/search?query="+urllib.parse.quote("Starlink ground network topology routing policy PoP measurement")+"&fields=title,year,venue,citationCount,citations.title&limit=5")
time.sleep(4)
if d:
    for p in (d.get("data") or []):
        print(f"ANCHOR-CAND ieee-11143359: {p.get('title')} | {p.get('venue')} {p.get('year')} | cites={p.get('citationCount')}", flush=True)
        for c in (p.get("citations") or []):
            t = c.get("title","")
            flag = " <<< SUSPECT" if any(k in t.lower() for k in ["spectral","period","decompos","queue","buffer","ground","pop","latency","variance","breakdown"]) else ""
            print(f"   - {t[:120]}{flag}", flush=True)
else:
    print(f"ANCHOR ieee-11143359: SEARCH FAILED {err}", flush=True)
print("DONE3", flush=True)
