#!/usr/bin/env python3
"""深潜质量门B v2：逐字引用核对器（严格→宽松两级）
宽松级处理 arXiv HTML 数学双写伪影（MathML+alttext 双份，如 "c k ck"、"25 x 10 6 25times 106"）。
用法: python3 verify_quotes.py <notes_dir> <fulltext_dir>
输出三级: VERBATIM(逐字) / ARTIFACT(数学伪影,内容真实) / UNVERIFIABLE(需人工)
退出码: 有 UNVERIFIABLE=1
"""
import re, sys, glob, os
def norm(s):
    s = re.sub(r'\s+', ' ', s).strip().lower()
    for a, b in [('\u2019',"'"),('\u2018',"'"),('\u201c','"'),('\u201d','"'),('\u2013','-'),('\u2014','-')]:
        s = s.replace(a, b)
    return s.strip('.,;:!? ')
def norm_loose(s):
    s = norm(s).replace('\u00d7','x').replace('×','x')
    return re.sub(r'[^a-z0-9 ]', '', s)
def dedup_tokens(s):
    # 折叠相邻重复 token 序列（数学双写伪影特征）
    t = s.split(); out = []; i = 0
    while i < len(t):
        # 检测 t[i:i+k] == t[i+k:i+2k] 的重复段
        skipped = False
        for k in range(1, min(6, (len(t)-i)//2 + 1)):
            if t[i:i+k] == t[i+k:i+2*k]:
                i += k; skipped = True; break
        out.append(t[i]); i += 1
    return ' '.join(out)
def main(nd, fd):
    counts = {"VERBATIM": 0, "ARTIFACT": 0, "UNVERIFIABLE": 0}; bad = []
    for note in sorted(glob.glob(os.path.join(nd, '*.md'))):
        pid = os.path.basename(note)[:-3]
        fp = os.path.join(fd, pid + '.txt')
        if not os.path.exists(fp):
            print(f'{pid}: 缺全文文件'); counts["UNVERIFIABLE"] += 1; continue
        ft = norm(open(fp, encoding='utf-8', errors='ignore').read())
        ftl = dedup_tokens(norm_loose(open(fp, encoding='utf-8', errors='ignore').read()))
        for line in open(note, encoding='utf-8'):
            m = re.match(r'^>\s*\[§?[^\]]+\]\s*"([^"]+)"', line.strip())
            if not m: continue
            q = m.group(1)
            if norm(q) in ft: counts["VERBATIM"] += 1
            elif dedup_tokens(norm_loose(q)) in ftl: counts["ARTIFACT"] += 1
            else:
                counts["UNVERIFIABLE"] += 1; bad.append((pid, q[:100]))
    print(f'核对: 逐字 {counts["VERBATIM"]} / 伪影真实 {counts["ARTIFACT"]} / 待人工 {counts["UNVERIFIABLE"]}')
    for pid, q in bad: print(f'  [UNVERIFIABLE] {pid}: {q}')
    sys.exit(1 if counts["UNVERIFIABLE"] else 0)
if __name__ == '__main__': main(sys.argv[1], sys.argv[2])
