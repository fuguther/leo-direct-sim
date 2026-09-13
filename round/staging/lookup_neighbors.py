import re, html, subprocess, sys

def curl(url):
    r = subprocess.run(["curl", "-sS", "--max-time", "30", "-L", url], capture_output=True, text=True)
    return r.stdout

def arxiv(q, n=5):
    t = curl("https://export.arxiv.org/api/query?search_query=" + q + f"&max_results={n}")
    out = []
    for m in re.finditer(r"<title>(.*?)</title>", t, re.S):
        ti = " ".join(m.group(1).split())
        if "arXiv Query" in ti: continue
        out.append(ti)
    ids = re.findall(r"arxiv.org/abs/([0-9.v]+)", t)
    return list(zip(out, ids))

for label, q in [
    ("A eligibility-traces adaptive routing", 'all:%22eligibility+traces%22+AND+all:%22adaptive+routing%22'),
    ("B failure-aware routing RL", 'all:%22failure-aware%22+AND+all:%22routing%22+AND+all:%22reinforcement%22'),
    ("C constrained DQN satellite", 'all:%22constrained%22+AND+all:%22DQN%22+AND+all:%22satellite%22'),
]:
    print("===", label, "===")
    for ti, aid in arxiv(q):
        print(f"  {aid}: {ti}")

print("=== D Wang-2019 MDPI two-hops state-aware ===")
t = curl("https://www.mdpi.com/2076-3417/8/9/920")
m = re.search(r'<meta name="description" content="([^"]+)"', t)
print(html.unescape(m.group(1))[:900] if m else "NO META (len %d)" % len(t))
