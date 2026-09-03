import re, subprocess, time
QUERIES = [
 ("RL+路由+卫星(不限LEO)", "all:reinforcement+AND+all:learning+AND+all:routing+AND+all:satellite"),
 ("深度RL+卫星路由", "all:%22deep+reinforcement+learning%22+AND+all:routing+AND+all:satellite"),
 ("RL+星座路由", "all:reinforcement+AND+all:learning+AND+all:routing+AND+all:constellation"),
 ("RL+LEO负载均衡", "all:reinforcement+AND+all:learning+AND+all:LEO+AND+all:%22load+balancing%22"),
 ("多智能体RL+卫星路由", "all:%22multi-agent%22+AND+all:reinforcement+AND+all:routing+AND+all:satellite"),
]
for label, q in QUERIES:
    url = f"https://export.arxiv.org/api/query?search_query={q}&max_results=6&sortBy=submittedDate&sortOrder=descending"
    subprocess.run(["curl", "-s", "--max-time", "30", url, "-o", "/tmp/qq.xml"], check=True)
    x = open("/tmp/qq.xml").read()
    m = re.search(r"opensearch:totalResults>(\d+)", x)
    print(f"== {label} ==  总量: {m.group(1) if m else '?'}")
    titles = [t for t in re.findall(r"<title>([^<]+)</title>", x)][1:]
    years = re.findall(r"<published>(\d{4})", x)
    for t, y in list(zip(titles, years))[:4]:
        print(f"   [{y}]", " ".join(t.split())[:85])
    time.sleep(4)
