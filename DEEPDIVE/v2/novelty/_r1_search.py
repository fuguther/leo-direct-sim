#!/usr/bin/env python3
import json, time, urllib.request, urllib.parse, sys

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent":"novelty-check/1.0 (mailto:agent@example.org)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", "replace"), None
    except Exception as e:
        return None, str(e)

def arxiv(q):
    url = "http://export.arxiv.org/api/query?search_query=all:" + urllib.parse.quote(q) + "&max_results=8"
    txt, err = get(url)
    if err: return None, err
    import re
    titles = re.findall(r"<title>(.*?)</title>", txt, re.S)[1:]
    total = re.search(r"totalResults[^>]*>(\d+)", txt)
    return [(t.strip().replace("\n"," ")[:110]) for t in titles], (total.group(1) if total else "?")

def crossref(q):
    url = "https://api.crossref.org/works?rows=8&select=title,DOI&query.bibliographic=" + urllib.parse.quote(q)
    txt, err = get(url)
    if err: return None, err
    d = json.loads(txt)
    items = d.get("message",{}).get("items",[])
    return [(i.get("title",[""])[0][:110], i.get("DOI","")) for i in items], d.get("message",{}).get("total-results","?")

def openalex(q):
    url = "https://api.openalex.org/works?per-page=8&search=" + urllib.parse.quote(q)
    txt, err = get(url)
    if err: return None, err
    d = json.loads(txt)
    return [(w.get("display_name","")[:110], w.get("publication_year")) for w in d.get("results",[])], d.get("meta",{}).get("count","?")

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

out = []
for i,q in enumerate(queries,1):
    rec = {"group": i, "query": q}
    a, ta = arxiv(q); time.sleep(2)
    c, tc = crossref(q); time.sleep(2)
    o, to = openalex(q); time.sleep(2)
    rec["arxiv"] = {"total": ta, "top3": a[:3] if a else None, "error": None if a else ta if not isinstance(ta,str) else ta}
    rec["crossref"] = {"total": tc, "top3": c[:3] if c else None}
    rec["openalex"] = {"total": to, "top3": o[:3] if o else None}
    if a is None: rec["arxiv"]["error"] = ta
    out.append(rec)
    print(f"=== GROUP {i}: {q}", flush=True)
    print(f"arXiv total={ta} top3={json.dumps(a[:3],ensure_ascii=False) if a else 'ERR:'+str(ta)}", flush=True)
    print(f"Crossref total={tc} top3={json.dumps(c[:3],ensure_ascii=False) if c else 'ERR'}", flush=True)
    print(f"OpenAlex total={to} top3={json.dumps(o[:3],ensure_ascii=False) if o else 'ERR'}", flush=True)

anchors = {
 "2310.09242": "arXiv:2310.09242",
 "2601.08439": "arXiv:2601.08439",
 "2605.27717": "arXiv:2605.27717",
 "ieee-11143359": None,
 "ieee-10375570": None,
}
# resolve anchors via S2
def s2_by_id(axid):
    url = f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{axid}?fields=title,citationCount,citations.title,citations.year&limit=20"
    txt, err = get(url)
    if err: return None, err
    return json.loads(txt), None

resolved = {}
for ax in ["2310.09242","2601.08439","2605.27717"]:
    d, err = s2_by_id(ax)
    time.sleep(3)
    if d:
        resolved[ax] = {"title": d.get("title"), "citationCount": d.get("citationCount"),
                        "citations": [c.get("title","")[:110] for c in (d.get("citations") or [])]}
        print(f"ANCHOR {ax}: {d.get('title')} | citations={d.get('citationCount')}", flush=True)
        print("  citing-top20:", json.dumps(resolved[ax]["citations"], ensure_ascii=False), flush=True)
    else:
        print(f"ANCHOR {ax}: ERR {err}", flush=True)

# find IEEE anchors by title search in S2
for key, titleq in [("ieee-11143359","Starlink ground network topology routing measurement"),
                    ("ieee-10375570","dynamic inter-satellite link scheduling routing energy reinforcement learning")]:
    url = "https://api.semanticscholar.org/graph/v1/paper/search?query=" + urllib.parse.quote(titleq) + "&fields=title,year,venue,citationCount,citations.title&limit=5"
    txt, err = get(url)
    time.sleep(3)
    if err:
        print(f"ANCHOR {key}: search ERR {err}", flush=True); continue
    d = json.loads(txt)
    for p in (d.get("data") or [])[:3]:
        print(f"ANCHOR-CAND {key}: {p.get('title')} | {p.get('venue')} {p.get('year')} | cites={p.get('citationCount')}", flush=True)
        if p.get("citations"):
            print("   citing-top20:", json.dumps([c.get('title','')[:100] for c in p['citations']], ensure_ascii=False), flush=True)

print("DONE", flush=True)
