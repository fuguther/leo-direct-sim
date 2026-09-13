
import csv, os
from pathlib import Path
rows = list(csv.DictReader(open('LITERATURE/SOURCES.csv')))
notes = {p.stem for p in Path('LITERATURE/notes/raw').glob('*.md')}
pdfs = {p.stem for p in Path('/Users/lge/Desktop/leo-direct-sim/LITERATURE/papers').glob('*.pdf')}
print('catalog=%d notes=%d pdfs=%d' % (len(rows), len(notes), len(pdfs)))
no_note, note_no_pdf = [], []
for r in rows:
    sid = r['source_id']
    if sid not in notes:
        no_note.append((sid, r['title'][:50], r['access_status'], r.get('notes','')[:40]))
    elif sid not in pdfs:
        note_no_pdf.append(sid)
print()
print('=== 只有题录、无笔记 (%d) ===' % len(no_note))
for s,t,a,n in no_note: print(' ', s, '|', t, '|', a, '|', n)
print()
print('=== 有笔记但无本地PDF (%d) ===' % len(note_no_pdf))
print(' ', ', '.join(note_no_pdf))
print()
print('=== 有PDF的 (%d) ===' % len(pdfs))
print(' ', ', '.join(sorted(pdfs)))
