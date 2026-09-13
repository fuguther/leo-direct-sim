
from pathlib import Path
p = Path('round/knowledge/notes-neutral/CHU-2023-RRSDRL.md')
t = p.read_text(encoding='utf-8')
old = 'AoI 是被转发数据的年龄，与路由状态信息年龄两码事'
new = 'AoI 是被转发数据的年龄，与路由决策所用状态的信息不是同一对象'
assert old in t
p.write_text(t.replace(old, new, 1), encoding='utf-8')
print('fixed')
