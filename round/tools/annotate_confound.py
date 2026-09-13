#!/usr/bin/env python3
import json
from pathlib import Path
NOTE = Path('round/run2/ANCHOR-NOTE-CMNCS52M.txt').read_text(encoding='utf-8').strip()
p = Path('round/run2/cards.json')
cards = json.loads(p.read_text(encoding='utf-8'))
n = 0
for c in cards:
    t = c.get('title', '')
    if any(t.startswith('run2-' + k) for k in ('A1', 'A2', 'B1', 'B3')):
        for f in ('difficulty', 'cause_hypothesis'):
            if '锚件已复核' not in c[f]:
                c[f] = c[f] + ' ' + NOTE
                n += 1
p.write_text(json.dumps(cards, ensure_ascii=False, indent=1), encoding='utf-8')
print('fields annotated:', n)