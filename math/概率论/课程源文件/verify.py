"""检查课程完整性、离线引用及全部本地跳转，不依赖第三方库。"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent.parent
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True);self.ids=[];self.links=[];self.tags=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs);self.tags.append((tag,a))
        if 'id'in a:self.ids.append(a['id'])
        for k in ('src','href'):
            if k in a:self.links.append(a[k])
pages={f.resolve():Page(f.read_text(encoding='utf-8')) for f in ROOT.rglob('*.html')}
issues=[];refs=0
for path,p in pages.items():
    if len(p.ids)!=len(set(p.ids)):issues.append(f'重复 ID: {path.name}')
    for link in p.links:
        refs+=1;u=urlsplit(link)
        if u.scheme or u.netloc:issues.append(f'非离线引用: {path.name}: {link}');continue
        dest=(path.parent/unquote(u.path)).resolve() if u.path else path
        if not dest.is_relative_to(ROOT):issues.append(f'超出课程目录: {link}');continue
        if not dest.exists():issues.append(f'目标不存在: {path.name}: {link}');continue
        if u.fragment and dest in pages and unquote(u.fragment) not in pages[dest].ids:issues.append(f'锚点不存在: {path.name}: {link}')
directory=json.loads((ROOT/'课程源文件/课程目录.json').read_text(encoding='utf-8'))
assert len(directory)==102
assert [x['id'] for x in directory if x['original']]==list(range(99))
assert len(list((ROOT/'课程').glob('*.html')))==102
for row in directory:
    p=pages[(ROOT/row['file']).resolve()]
    for t in ('article','details','summary'):
        assert any(tag==t for tag,_ in p.tags),(row['id'],t)
    assert f'lesson-{row["id"]:02d}' in p.ids
app=pages[(ROOT/'开始学习.html').resolve()]
assert len([1 for t,a in app.tags if 'data-card' in a])==102
assert len([1 for t,a in app.tags if 'data-note' in a])==102
assert len([1 for t,a in app.tags if 'data-complete' in a])==102
for filename in ('notebook.js','labs.js','visual-math.js','math-visuals.js'):
    js=(ROOT/'资源'/filename).read_text(encoding='utf-8')
    assert 'fetch(' not in js and 'http://' not in js and 'https://' not in js
from interactive_visuals import KINDS
for row in directory:
    page=pages[(ROOT/row['file']).resolve()]
    kinds=[a['data-visual-kind'] for _,a in page.tags if 'data-visual-kind' in a]
    assert kinds==([KINDS[row['id']]] if row['id'] in KINDS else [])
assert len([a for _,a in app.tags if 'data-visual-kind' in a])==len(KINDS)
from pedagogy import GUIDES, TOOLS, CODE
assert set(GUIDES)==set(range(102))
for i,guide in GUIDES.items():
    assert guide['question'] and guide['example']
    assert all(key in TOOLS for key in guide['tools'])
    p=pages[(ROOT/directory[i]['file']).resolve()]
    assert any('data-step' in a for _,a in p.tags)
    assert any('data-tool' in a for _,a in p.tags)
for text in ((ROOT/'开始学习.html').read_text(encoding='utf-8'),):
    assert '你已经学过反向传播' not in text
    assert '你学过的链式法则' not in text
# 执行交付给学习者的完整示例，核对关键中间结果与一次更新。
from contextlib import redirect_stdout
from io import StringIO
from math import isclose
for i,code in CODE.items():
    namespace={}
    with redirect_stdout(StringIO()):exec(code[1],namespace)
    if i==1:assert namespace['frequency']==0.75
    if i==66:
        assert isclose(namespace['w'],0.1) and isclose(namespace['b'],0.05)
        assert -__import__('math').log(namespace['new_p'])<namespace['loss']
    if i==68:assert isclose(namespace['new_prediction'],3.5) and isclose(namespace['new_loss'],1.125)
    if i==101:
        assert isclose(sum(namespace['new_q']),1)
        assert namespace['new_q'][1]>namespace['q'][1]
assert not issues,'\n'.join(issues)
print(f'PASS: {len(pages)} HTML files, 102 guided lessons, {refs} local references, offline assets, a single learning entry, and 4 runnable Python examples.')
