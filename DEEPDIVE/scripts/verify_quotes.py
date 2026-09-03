#!/usr/bin/env python3
"""深潜质量门B：逐字引用核对器（金丝雀 v1.1 教训固化）
用法: python3 verify_quotes.py <notes_dir> <fulltext_dir>
规则: 笔记中 '> [§x] "quote"' 行，归一化后与全文比对；忽略句尾标点差异(金丝雀补遗§1)。
退出码: 全部通过=0；有未命中=1（列出明细）。
"""
import re, sys, glob, os
PUNCT = '.,;:!?。，；：！？'
def norm(s):
    s = re.sub(r'\s+', ' ', s).strip().lower()
    for a, b in [('\u2019',"'"),('\u2018',"'"),('\u201c','"'),('\u201d','"'),('\u2013','-'),('\u2014','-')]:
        s = s.replace(a, b)
    return s.strip(PUNCT + ' ')
def main(nd, fd):
    total = ok = 0; bad = []
    for note in sorted(glob.glob(os.path.join(nd, '*.md'))):
        pid = os.path.basename(note)[:-3]
        fp = os.path.join(fd, pid + '.txt')
        if not os.path.exists(fp):
            print(f'{pid}: 缺全文文件'); bad.append((pid,'NO-FULLTEXT','')); continue
        ft = norm(open(fp, encoding='utf-8', errors='ignore').read())
        for line in open(note, encoding='utf-8'):
            m = re.match(r'^>\s*\[§?[^\]]+\]\s*"([^"]+)"', line.strip())
            if not m: continue
            total += 1
            if norm(m.group(1)) in ft: ok += 1
            else: bad.append((pid, 'MISS', m.group(1)[:110]))
    print(f'核对: {ok}/{total} 逐字真实')
    for pid, kind, q in bad: print(f'  [{kind}] {pid}: {q}')
    sys.exit(0 if ok == total else 1)
if __name__ == '__main__': main(sys.argv[1], sys.argv[2])
