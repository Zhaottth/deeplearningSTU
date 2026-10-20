"""Fill explicitly audited gaps and add a navigable coverage report to the workbook."""
from pathlib import Path
import html,json,re
from audit_coverage import ROOT,catalog,read_bank

path=ROOT/'2.html'
s=path.read_text(encoding='utf-8')
assert '// SQL_COVERAGE_AUDIT' not in s,'Coverage already installed'
bank=read_bank();assert len(bank)==400
def js(v):return json.dumps(v,ensure_ascii=False).replace('</','<\\/')
sections={}
for line in (ROOT/'coverage_supplements.txt').read_text(encoding='utf-8').splitlines():
    if not line.strip():continue
    if line.startswith('['):key=line.strip('[]');sections[key]=[]
    else:sections[key].append(line)
new=[]
for k in catalog:
    needed=max(0,3-len(k['original']))
    additions=sections.get(k['id'],[])
    assert len(additions)==needed,(k['id'],needed,len(additions))
    k['questions']=list(k['original'])
    for line in additions:
        q,correct,w1,w2,w3,explain=line.split('|')
        opts=[correct,w1,w2,w3];rotate=len(new)%4;opts=opts[rotate:]+opts[:rotate]
        new.append(dict(topic='补齐 / '+k['name'],type='s',q=html.escape(q),o=opts,a=[(-rotate)%4],e=html.escape(explain),batch='coverage'))
        k['questions'].append(400+len(new))
    assert len(k['questions'])>=3
assert len(new)==119
assert {i for k in catalog for i in k['questions']}==set(range(1,520))
assert all(len(set(q['o']))==4 and len(q['e'])>=40 for q in new)
gaps=sum(len(k['original'])<3 for k in catalog)
absent=sum(not k['original'] for k in catalog)
report={'scope':'MySQL 8.0.18+ 核心查询、分析与数据库工程；特定小版本差异在题干中单独约定。',
 'method':'逐题语义映射，只有题干或作答所必需的知识点才计入；一题可对应多个实际考点；原有结果推导变式计为独立练习，不当作新知识点。实战及工程挑战不计入三道客观题门槛。',
 'limits':'这是一份明确范围的核心清单，不宣称覆盖所有 SQL 标准、数据库方言或内部实现。空间/GIS、向量检索、插件、分布式共识实现、专业 DBA 全部调优参数等未列入。题量达标不证明技能已经掌握。',
 'originalQuestions':400,'addedQuestions':len(new),'totalQuestions':519,'knowledgePoints':len(catalog),
 'originalGaps':gaps,'originalAbsent':absent,'remainingGaps':0,'points':catalog}
s=s.replace('const KEY=','// SQL_COVERAGE_AUDIT\nBANK.push(...'+js(new)+');\nconst COVERAGE='+js(report)+';\nBANK.forEach(q=>q.knowledge=[]);\nCOVERAGE.points.forEach(k=>k.questions.forEach(n=>BANK[n-1].knowledge.push(k.id)));\nconst KEY=',1)
s=s.replace('400 道','519 道').replace('400 题 / 48','519 题 / 48')
s=s.replace('本轮新增 120 道结果推导 + 80 道并发与性能，逐题讲解。','111 个核心知识点均至少 3 道题，已补齐 119 道薄弱点练习，每题有讲解。')
s=s.replace('<button data-tab="review">','<button data-tab="coverage">知识点覆盖</button><button data-tab="review">')
s=s.replace('<section id="review" hidden>','<section id="coverage" hidden></section><section id="review" hidden>')
s=s.replace("['learn','quiz','lab','engineering','review']","['learn','quiz','lab','engineering','coverage','review']")
s=s.replace("if(t==='engineering')renderEngineering();","if(t==='engineering')renderEngineering();if(t==='coverage')renderCoverage();")
s=s.replace("let topic='all',","let knowledge='all';\nlet topic='all',",1)
s=s.replace('<option value="latest">本轮新增 200 题</option>','<option value="coverage">覆盖补齐 119 题</option><option value="latest">上一轮新增 200 题</option>')
s=s.replace('<input type="search" id="search"','<select id="knowledge" aria-label="具体知识点筛选"></select><input type="search" id="search"',1)
s=s.replace("return(topic==='all'||q.topic===topic)","return(knowledge==='all'||q.knowledge.includes(knowledge))&&(topic==='all'||q.topic===topic)",1)
s=s.replace("filter==='latest'&&q.id>=200", "filter==='latest'&&q.id>=200&&q.id<400||filter==='coverage'&&q.batch==='coverage'",1)
s=s.replace("function resetView(){topic=", "function resetView(){knowledge='all';$('#knowledge').value='all';topic=",1)
s=s.replace("topic=b.dataset.topic;applyFilter();","knowledge='all';$('#knowledge').value='all';topic=b.dataset.topic;applyFilter();")
s=s.replace("topic=b.dataset.practice;filter=", "knowledge='all';$('#knowledge').value='all';topic=b.dataset.practice;filter=")
s=s.replace("topic='all';filter=f;query='';", "knowledge='all';$('#knowledge').value='all';topic='all';filter=f;query='';")
s=s.replace("${q.id>=200?'<span class=\"chip\">本轮新增</span>'", "${q.id>=400?'<span class=\"chip\">覆盖补齐</span>':q.id>=200?'<span class=\"chip\">上一轮新增</span>'")
s=s.replace('本轮 #201–320 为结果推导，#321–360 为并发，#361–400 为性能。','新增 #401–519 补齐薄弱考点；“知识点覆盖”可查看 111 个考点的题数并直接练习。#201–320 为结果推导，#321–360 为并发，#361–400 为性能。')
s=s.replace('已有基础可直接筛选“本轮新增 200 题”。','本次审计以 111 个明确列出的核心知识点为范围，原有 59 个考点不足三题（其中 16 个无客观题），已新增 119 题补齐。到“知识点覆盖”查看逐项证据和范围说明。')
coverage_ui='''
function selectKnowledge(id){
 knowledge=id;topic='all';filter='all';query='';
 $('#knowledge').value=id;$('#filter').value='all';$('#search').value='';applyFilter();switchTab('quiz');
}
$('#knowledge').innerHTML='<option value="all">全部具体知识点</option>'+COVERAGE.points.map(k=>`<option value="${k.id}">${esc(k.area)} · ${esc(k.name)}（${k.questions.length}题）</option>`).join('');
$('#knowledge').onchange=e=>selectKnowledge(e.target.value);
function renderCoverage(){
 $('#coverage').innerHTML=`<div class="panel"><h2>111 个核心知识点 · 每点至少三道客观题</h2><p>审计前 400 题中，59 个考点不足三题，其中 16 个没有客观题。现已补入 119 题，总计 519 题；清单内未达三题的考点为 0。</p><p>${esc(COVERAGE.method)}</p><div class="notice">${esc(COVERAGE.scope)} ${esc(COVERAGE.limits)}</div><button id="coverage-download">下载逐题覆盖清单 JSON</button><p class="muted">“题数达标”仅衡量训练覆盖；掌握情况按当前已提交且答对的题数独立显示。同一题多考点映射不会增加题库总量。实战与工程挑战未用于凑够三题。</p></div><div class="tablewrap panel" style="margin-top:16px"><table><thead><tr><th>领域 / 考点</th><th>原有 → 当前</th><th>当前答对</th><th>题号（1 起算）</th><th>练习</th></tr></thead><tbody>${COVERAGE.points.map(k=>{
 const correct=k.questions.filter(n=>state.graded[n-1]&&right(BANK[n-1])).length;
 return `<tr><td><span class="muted">${esc(k.area)} · ${k.id}</span><br><strong>${esc(k.name)}</strong></td><td>${k.original.length} → ${k.questions.length}<br><span class="chip">≥3 达标</span></td><td>${correct} / ${k.questions.length}</td><td><details><summary>查看 ${k.questions.length} 个题号</summary>${k.questions.map(n=>'#'+n).join('、')}</details></td><td><button data-knowledge="${k.id}">练这项</button></td></tr>`;
 }).join('')}</tbody></table></div>`;
 $('#coverage-download').onclick=()=>download('sql-knowledge-coverage.json',JSON.stringify(COVERAGE,null,2),'application/json');
 $('#coverage').querySelectorAll('[data-knowledge]').forEach(b=>b.onclick=()=>selectKnowledge(b.dataset.knowledge));
}
'''
s=s.replace('setInterval(()=>{',coverage_ui+'\nsetInterval(()=>{',1)
s=s.replace("if(tab==='engineering')renderEngineering();", "if(tab==='engineering')renderEngineering();if(tab==='coverage')renderCoverage();")
path.write_text(s,encoding='utf-8')
(ROOT/'sql-knowledge-coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# SQL 知识点覆盖审计','',report['scope'],'',report['method'],'',report['limits'],'',
       f'审计前：400 题，{len(catalog)} 个考点中 {gaps} 个不足三题，其中 {absent} 个为零题。',
       '补齐后：519 题，111 个考点全部至少三题；新增 119 题均含讲解。',
       '范围是明确列出的核心考点，不是所有 SQL 特性的穷尽清单。题号为页面的一起算题号。','',
       '|编号|领域|具体知识点|原有题数|补齐后|对应题号|','|---|---|---|---:|---:|---|']
for k in catalog:lines.append(f"|{k['id']}|{k['area']}|{k['name']}|{len(k['original'])}|{len(k['questions'])}|"+', '.join('#'+str(n) for n in k['questions'])+'|')
(ROOT/'SQL知识点覆盖审计.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(f'Covered {len(catalog)} points; original gaps {gaps}, absent {absent}; added {len(new)}; total {400+len(new)}. All original question IDs preserved.')
