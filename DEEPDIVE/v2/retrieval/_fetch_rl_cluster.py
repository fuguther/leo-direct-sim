#!/usr/bin/env python3
import json, re, subprocess, time, xml.etree.ElementTree as ET
import urllib.parse
from collections import defaultdict

OUT = "/private/tmp/leo-coldstart-deepdive-20260903/DEEPDIVE/v2/retrieval/rl-cluster.json"
failures = []

def curl(url, tag):
    for attempt in range(2):
        try:
            p = subprocess.run(["curl", "-sS", "-m", "45", url], capture_output=True, text=True, timeout=60)
            if p.returncode == 0 and p.stdout.strip():
                return p.stdout
            raise RuntimeError("rc=%s err=%s" % (p.returncode, p.stderr[:200]))
        except Exception as e:
            if attempt == 1:
                failures.append({tag: str(e)})
                print("[FAIL] %s: %s" % (tag, e), flush=True)
                return None
            time.sleep(3)

def clean(s, n=500):
    s = re.sub(r"\s+", " ", (s or "")).strip()
    return s[:n]

papers = {}
sources_of = defaultdict(set)

def add(key, rec, src):
    sources_of[key].add(src)
    if key not in papers:
        papers[key] = rec

NS = {"a": "http://www.w3.org/2005/Atom"}

def arxiv_q(qstr, tag):
    url = "https://export.arxiv.org/api/query?search_query=%s&max_results=20&sortBy=relevance" % qstr
    xml = curl(url, tag)
    if not xml: return
    try:
        root = ET.fromstring(xml)
    except Exception as e:
        failures.append({tag: "parse: %s" % e}); return
    n = 0
    for e in root.findall("a:entry", NS):
        raw = e.find("a:id", NS).text or ""
        m = re.search(r"abs/([0-9]+\.[0-9]+)", raw)
        if not m: continue
        aid = m.group(1)
        title = clean(e.find("a:title", NS).text, 300)
        if not title: continue
        pub = (e.find("a:published", NS).text or "")[:4]
        summ = clean(e.find("a:summary", NS).text)
        add("arx:" + aid, {"id": aid, "title": title, "year": pub, "venue": "arXiv",
                           "abstract": summ, "relation": "rl-leo-routing"}, tag)
        n += 1
    print("[ok] %s: %d" % (tag, n), flush=True)

def strip_jats(s):
    return clean(re.sub(r"<[^>]+>", " ", s or ""))

def crossref_q(qb, tag):
    url = ("https://api.crossref.org/works?query.bibliographic=" + urllib.parse.quote(qb) +
           "&rows=15&select=DOI,title,published,container-title,abstract")
    txt = curl(url, tag)
    if not txt: return
    try:
        items = json.loads(txt)["message"]["items"]
    except Exception as e:
        failures.append({tag: "parse: %s" % e}); return
    n = 0
    for it in items:
        doi = (it.get("DOI") or "").strip().lower()
        if not doi: continue
        t = (it.get("title") or [""])[0]
        if not t: continue
        dp = (it.get("published") or {}).get("date-parts", [[None]])[0]
        year = str(dp[0]) if dp and dp[0] else ""
        ven = (it.get("container-title") or [""])[0] or "Crossref"
        add("doi:" + doi, {"id": doi, "title": clean(t, 300), "year": year, "venue": clean(ven, 120),
                           "abstract": strip_jats(it.get("abstract")), "relation": "rl-leo-routing"}, tag)
        n += 1
    print("[ok] %s: %d" % (tag, n), flush=True)

def openalex_q(search, tag):
    url = ("https://api.openalex.org/works?search=" + urllib.parse.quote(search) +
           "&per-page=25&mailto=retr@example.com")
    txt = curl(url, tag)
    if not txt: return
    try:
        res = json.loads(txt).get("results", [])
    except Exception as e:
        failures.append({tag: "parse: %s" % e}); return
    n = 0
    for it in res:
        doi = (it.get("doi") or "").replace("https://doi.org/", "").strip().lower()
        t = it.get("display_name") or ""
        if not doi and not t: continue
        inv = it.get("abstract_inverted_index")
        ab = ""
        if inv:
            pos = {}
            for w, idxs in inv.items():
                for i in idxs: pos[i] = w
            ab = clean(" ".join(pos[i] for i in sorted(pos)))
        m = re.search(r"arxiv.org/abs/([0-9]+\.[0-9]+)", json.dumps(it.get("ids", {})))
        src = ((it.get("primary_location") or {}).get("source") or {}).get("display_name") or "OpenAlex"
        key = ("arx:" + m.group(1)) if m else ("doi:" + doi if doi else "oa:" + (it.get("id") or t))
        rid = m.group(1) if m else (doi or it.get("id", ""))
        add(key, {"id": rid, "title": clean(t, 300), "year": str(it.get("publication_year") or ""),
                  "venue": clean(src, 120), "abstract": ab, "relation": "rl-leo-routing"}, tag)
        n += 1
    print("[ok] %s: %d" % (tag, n), flush=True)

def s2_cites(pid, tag):
    url = ("https://api.semanticscholar.org/graph/v1/paper/%s/citations?limit=40&"
           "fields=title,abstract,year,externalIds,venue" % pid)
    txt = curl(url, tag)
    if not txt: return
    try:
        data = json.loads(txt).get("data", [])
    except Exception as e:
        failures.append({tag: "parse: %s body[:120]=%s" % (e, txt[:120])}); return
    n = 0
    for c in data:
        p = c.get("citingPaper") or {}
        ext = p.get("externalIds") or {}
        aid = ext.get("ArXiv"); doi = (ext.get("DOI") or "").lower()
        t = p.get("title") or ""
        if not t: continue
        key = ("arx:" + aid) if aid else ("doi:" + doi if doi else "s2:" + (p.get("paperId") or t))
        rid = aid or doi or p.get("paperId", "")
        add(key, {"id": rid, "title": clean(t, 300), "year": str(p.get("year") or ""),
                  "venue": clean(p.get("venue") or "SemanticScholar", 120),
                  "abstract": clean(p.get("abstract")), "relation": "s2-citation-expansion"}, tag)
        n += 1
    print("[ok] %s: %d" % (tag, n), flush=True)

arxiv_queries = [
    ("all:reinforcement+AND+all:routing+AND+all:satellite", "ax1-rl-routing-satellite"),
    ("all:reinforcement+AND+all:LEO+AND+all:routing", "ax2-rl-leo-routing"),
    ("all:deep+AND+all:reinforcement+AND+all:LEO+AND+all:routing", "ax3-drl-leo"),
    ("all:multi-agent+AND+all:reinforcement+AND+all:satellite+AND+all:routing", "ax4-marl-satellite"),
    ("all:graph+AND+all:reinforcement+AND+all:routing+AND+all:satellite", "ax5-gnn-rl-satellite"),
    ("all:load+AND+all:balancing+AND+all:LEO+AND+all:reinforcement", "ax6-loadbalancing-leo"),
    ("all:delay+AND+all:aware+AND+all:routing+AND+all:satellite", "ax7-delay-aware-satellite"),
    ("all:reward+AND+all:reinforcement+AND+all:satellite+AND+all:routing", "ax8-reward-design-satellite"),
    ("all:traffic+AND+all:LEO+AND+all:constellation", "ax9-traffic-leo"),
    ("all:Q-learning+AND+all:satellite+AND+all:routing", "ax10-qlearning-satellite"),
]
for q, tag in arxiv_queries:
    arxiv_q(q, tag); time.sleep(2.5)

crossref_queries = [
    ("reinforcement learning LEO satellite routing", "cr1"),
    ("deep reinforcement learning satellite network routing", "cr2"),
    ("load balancing LEO satellite constellation reinforcement learning", "cr3"),
    ("delay aware routing satellite reinforcement learning", "cr4"),
    ("graph neural network routing satellite network reinforcement", "cr5"),
]
for q, tag in crossref_queries:
    crossref_q(q, tag); time.sleep(2.5)

openalex_queries = [
    ("reinforcement learning routing LEO satellite", "oa1"),
    ("deep reinforcement learning satellite routing load balancing", "oa2"),
    ("multi-agent reinforcement learning satellite network routing", "oa3"),
    ("delay aware routing LEO constellation machine learning", "oa4"),
    ("traffic offloading LEO satellite reinforcement learning", "oa5"),
]
for q, tag in openalex_queries:
    openalex_q(q, tag); time.sleep(2.5)

s2_cites("ARXIV:2605.02413", "s2a-cites-2605.02413"); time.sleep(3)
s2_cites("ARXIV:2310.07646", "s2b-cites-2310.07646")

out = []
for k, rec in papers.items():
    rec["sources"] = sorted(sources_of[k])
    out.append(rec)

result = out + [{"_failures": failures}]
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)

print("TOTAL=%d FAILURES=%d" % (len(out), len(failures)))
for fl in failures: print("F:", fl)
