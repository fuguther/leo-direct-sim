import re, subprocess

def curl(url):
    r = subprocess.run(["curl", "-sS", "--max-time", "30", "-L", url], capture_output=True, text=True)
    return r.stdout

for label, q in [
    ("Mao20 reward design cooperative MARL packet routing", 'all:%22reward+design%22+AND+all:%22packet+routing%22'),
    ("You fully distributed multiagent DRL packet routing", 'all:%22fully+distributed%22+AND+all:%22packet+routing%22+AND+all:%22reinforcement%22'),
]:
    t = curl("https://export.arxiv.org/api/query?search_query=" + q + "&max_results=6")
    print("===", label, "===")
    entries = re.findall(r"<entry>(.*?)</entry>", t, re.S)
    for e in entries[:6]:
        ti = re.search(r"<title>(.*?)</title>", e, re.S)
        sm = re.search(r"<summary>(.*?)</summary>", e, re.S)
        aid = re.search(r"arxiv.org/abs/([0-9.v]+)", e)
        if ti:
            print(" ", aid.group(1) if aid else "?", "|", " ".join(ti.group(1).split()))
            if sm: print("   ABS:", " ".join(sm.group(1).split())[:600])
