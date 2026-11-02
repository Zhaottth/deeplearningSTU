(()=>{'use strict';
const $=(s,root=document)=>root.querySelector(s),all=(s,root=document)=>[...root.querySelectorAll(s)];
// 共享知识工具箱：独立页、实验室与阅读入口都能随时补基础。
const dialog=$('#toolbox-dialog');
document.addEventListener('click',event=>{
  const button=event.target.closest('[data-tool]');if(!button)return;
  const key=button.dataset.tool;
  all('[data-tool-panel]').forEach(panel=>panel.hidden=panel.dataset.toolPanel!==key);
  all('.tool-layout [data-tool]').forEach(tab=>{const active=tab.dataset.tool===key;tab.classList.toggle('active',active);tab.setAttribute('aria-pressed',String(active))});
  if(!dialog.open)dialog.showModal();
});
// 每章开头的现场题：先作判断，再给这条选项专属的解释；允许反复换答案。
document.addEventListener('click',event=>{
  const choice=event.target.closest('[data-episode-choice]');if(!choice)return;
  const scene=choice.closest('.episode-scene');if(!scene)return;
  const correct=choice.dataset.right==='true';
  all('[data-episode-choice]',scene).forEach(button=>{
    const selected=button===choice;button.setAttribute('aria-pressed',String(selected));
    button.classList.toggle('picked',selected);
  });
  scene.dataset.result=correct?'right':'try-again';
  const feedback=$('.episode-feedback',scene);feedback.hidden=false;
  $('[data-episode-verdict]',feedback).textContent=correct?'这条判断站得住 ✓':'这个直觉很常见，我们来找漏掉的那一步。';
  $('[data-episode-reply]',feedback).textContent=choice.dataset.reply;
});
function updateKnowledge(target){
  const shelf=$('.knowledge-shelf');if(!shelf)return;
  const items=JSON.parse(target?target.dataset.knowledge:shelf.dataset.overviewKnowledge);
  $('.shelf-label strong',shelf).textContent=target?'本节用到':'本页用到';
  $('.shelf-chips',shelf).replaceChildren(...items.map(([key,symbol,label])=>{
    const button=document.createElement('button');button.className='tool-chip';button.dataset.tool=key;
    const sign=document.createElement('span');sign.className='math';sign.textContent=symbol;
    const text=document.createElement('span');text.textContent=label;button.append(sign,text);return button;
  }));shelf.hidden=items.length===0;
}
$('[data-close-tool]')?.addEventListener('click',()=>dialog.close());
dialog?.addEventListener('click',event=>{if(event.target===dialog){const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close()}});

// 逐步推导：只隐藏尚未请求的步骤，不移除内容；无脚本时全部可读。
all('.walkthrough').forEach(section=>{
  const steps=all('[data-step]',section),controls=$('.step-controls',section);let shown=1;
  function paint(){steps.forEach((step,i)=>step.hidden=i>=shown);$('.step-status',section).textContent=`已展开 ${shown} / ${steps.length} 步`;
    $('[data-next-step]',section).disabled=shown===steps.length;$('[data-next-step]',section).textContent=shown===steps.length?'这一段推完了 ✓':'再往前一步 →';
    $('[data-all-steps]',section).hidden=shown===steps.length;
  }
  if(!controls)return;controls.hidden=false;paint();
  $('[data-next-step]',section).addEventListener('click',()=>{shown=Math.min(shown+1,steps.length);paint()});
  $('[data-all-steps]',section).addEventListener('click',()=>{shown=steps.length;paint()});
});
let printDetails=[],printSteps=[];
window.addEventListener('beforeprint',()=>{printDetails=all('details:not([open])');printSteps=all('[data-step][hidden]');printDetails.forEach(d=>d.open=true);printSteps.forEach(s=>s.hidden=false)});
window.addEventListener('afterprint',()=>{printDetails.forEach(d=>d.open=false);printSteps.forEach(s=>s.hidden=true)});
all('[data-print]').forEach(b=>b.addEventListener('click',()=>window.print()));
all('[data-copy-code]').forEach(b=>b.addEventListener('click',async()=>{
  const code=b.closest('.code-section').querySelector('code').textContent;
  try{if(!navigator.clipboard?.writeText)throw Error();await navigator.clipboard.writeText(code);b.textContent='已复制 ✓'}catch{const range=document.createRange();range.selectNodeContents(b.closest('.code-section').querySelector('code'));const selection=window.getSelection();selection.removeAllRanges();selection.addRange(range);b.textContent='代码已选中，请复制'}
}));

// 首页小实验：参照范围与被计数的结果分别呈现。
let mode='union';const A=n=>n%2===0,B=n=>n>3;
const demos={union:{formula:'P(A∪B) = 4 / 6 = 2 / 3',explanation:'4 和 6 重复了。3+3−2=4 个，分母仍是全部 6 个。',selected:n=>A(n)||B(n),scope:()=>true},intersection:{formula:'P(A∩B) = 2 / 6 = 1 / 3',explanation:'同时在两份名单里的只有 4、6。数 2 个，分母仍为全部 6 个。',selected:n=>A(n)&&B(n),scope:()=>true},conditional:{formula:'P(A|B) = 2 / 3',explanation:'已知 B，先只留下 4、5、6。其中偶数有 4、6，分子 2，分母 3。',selected:n=>A(n)&&B(n),scope:B}};
function drawDice(){const d=demos[mode];all('[data-mode]').forEach(b=>{const active=b.dataset.mode===mode;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active))});all('[data-die]').forEach(b=>{const n=+b.dataset.die;b.classList.toggle('selected',d.selected(n));b.classList.toggle('outside',!d.scope(n));b.setAttribute('aria-pressed',String(d.selected(n)));b.setAttribute('aria-label',`点数 ${n}，${d.scope(n)?'在当前分母范围内':'不在当前分母范围内'}，${d.selected(n)?'符合要求':'不符合要求'}，点击查看所属事件`)});if($('#demo-equation')){$('#demo-equation').textContent=d.formula;$('#demo-explanation').textContent=d.explanation}}
all('[data-mode]').forEach(b=>b.addEventListener('click',()=>{mode=b.dataset.mode;drawDice();$('#die-inspect').textContent='点任意一枚骰子，看看它属于哪份名单。'}));
all('[data-die]').forEach(b=>b.addEventListener('click',()=>{const n=+b.dataset.die;$('#die-inspect').textContent=`点数 ${n}：${A(n)?'属于 A（偶数）':'不属于 A'}；${B(n)?'属于 B（大于 3）':'不属于 B'}。${demos[mode].scope(n)?'它在当前分母范围里。':'已知 B 后，它被排除在分母之外。'}`}));drawDice();

if(!document.body.classList.contains('course-app'))return;
// 延续上一版记录格式，避免重写页面导致笔记丢失。
const KEY='probability-course-v1';let state={version:1,completed:[],notes:{},last:2};
function validate(s){if(!s||s.version!==1||!Array.isArray(s.completed)||!s.notes||typeof s.notes!=='object'||Array.isArray(s.notes))throw Error('格式不正确');return{version:1,completed:[...new Set(s.completed.filter(i=>Number.isInteger(i)&&i>=0&&i<=101))],notes:Object.fromEntries(Object.entries(s.notes).filter(([k,v])=>/^\d+$/.test(k)&&+k<=101&&typeof v==='string').map(([k,v])=>[k,v.slice(0,50000)])),last:Number.isInteger(s.last)&&s.last>=0&&s.last<=101?s.last:2}}
try{const saved=localStorage.getItem(KEY);if(saved)state=validate(JSON.parse(saved))}catch{$('#storage-status').textContent='浏览器暂不能读取记录；可继续学习，并导出当前会话备份。'}
function save(){try{localStorage.setItem(KEY,JSON.stringify(state));$('#storage-status').textContent='已保存在当前浏览器，建议定期导出。';return true}catch{$('#storage-status').textContent='浏览器未能保存；离开前请导出当前会话记录。';return false}}
function progress(){const original=state.completed.filter(i=>i<99).length,bonus=state.completed.length-original;
  $('#home-progress').textContent=`已掌握 ${original} / 99 节`;$('#bonus-progress').textContent=`补充课 ${bonus} / 3`;$('#progress-label').textContent=`已掌握 ${original} / 99`;$('#progress-fill').style.width=original/99*100+'%';
  all('[data-card]').forEach(c=>{const done=state.completed.includes(+c.dataset.card);c.classList.toggle('mastered',done);$('.card-check',c).textContent=done?'✓':'↗'});
  all('[data-complete]').forEach(b=>{const done=state.completed.includes(+b.dataset.complete);b.textContent=done?'已掌握 ✓（点击可取消）':'我能解释这一节了 ✓';b.setAttribute('aria-pressed',String(done))});
  const resume=$('#continue-learning');resume.href=`#lesson-${String(state.last).padStart(2,'0')}`;resume.textContent=state.last===2?'从概率定义开始 →':`接着学 · 第 ${String(state.last).padStart(2,'0')} 节 →`;
}
let current=null,searchOpenState=null;
function filterLessons(){const q=$('#course-search').value.trim().toLocaleLowerCase();let count=0;
  if(q&&!searchOpenState)searchOpenState=new Map(all('.module').map(m=>[m.id,m.open]));
  all('[data-card]').forEach(c=>{const match=c.dataset.search.toLocaleLowerCase().includes(q);c.hidden=!match;if(match)count++});
  all('.module').forEach(m=>{m.hidden=!m.querySelector('[data-card]:not([hidden])');if(q)m.open=true;else if(searchOpenState)m.open=searchOpenState.get(m.id)});
  if(!q)searchOpenState=null;
  $('#search-status').textContent=q?`找到 ${count} 节${count?'。':'；试试“方差”或“似然”。'}`:'99 节基础讲义 + 3 节深度学习桥梁课。点击章节可收起或展开。';
}
function navigate(){let hash;try{hash=decodeURIComponent(location.hash)}catch{hash=''}const m=hash.match(/^#lesson-(\d{2,3})$/),id=m?+m[1]:null,target=id!==null?$(`#lesson-${String(id).padStart(2,'0')}`):null;
  all('.lesson').forEach(x=>x.hidden=true);const reading=Boolean(target);$('#overview').hidden=reading;$('#reader').hidden=!reading;document.body.classList.toggle('is-reader',reading);
  updateKnowledge(target);
  if(reading){target.hidden=false;current=id;state.last=id;save();const title=$('h1',target).textContent;document.title=title+' · 概率手记';$('#reader-position').textContent=id<99?`第 ${id} 节 / 99 节基础`:`补充 ${id-98} / 3`;
    $('#standalone-link').href='课程/'+String(id).padStart(2,'0')+'_'+title.replace(/[\\/:*?"<>|]/g,'')+'.html';$('[data-note]',target).value=state.notes[id]||'';
    all('[data-module]').forEach(a=>{const k=id<=29?'01':id<=56?'02':id<=76?'03':id<=98?'04':'＋';a.classList.toggle('active',a.dataset.module===k)});window.scrollTo({top:0,behavior:'instant'});
  }else{current=null;document.title='开始学习 · 概率手记';all('[data-module]').forEach(a=>a.classList.remove('active'));
    if(hash.startsWith('#module-')){if($('#course-search').value){$('#course-search').value='';filterLessons()}const module=document.getElementById(hash.slice(1));if(module){module.hidden=false;module.open=true;requestAnimationFrame(()=>module.scrollIntoView())}}
    else if(hash==='#catalog')requestAnimationFrame(()=>$('#catalog').scrollIntoView());else window.scrollTo({top:0,behavior:'instant'});
  }progress();
}
all('[data-complete]').forEach(b=>b.addEventListener('click',()=>{const id=+b.dataset.complete;if(state.completed.includes(id))state.completed=state.completed.filter(x=>x!==id);else state.completed.push(id);const ok=save();progress();$('.save-state',b.closest('.reflection')).textContent=ok?'已保存':'请导出备份'}));
all('[data-note]').forEach(t=>t.addEventListener('input',()=>{state.notes[t.dataset.note]=t.value;save()}));
$('#course-search').addEventListener('input',filterLessons);
document.addEventListener('keydown',e=>{if(e.ctrlKey||e.altKey||e.metaKey||dialog?.open||['INPUT','TEXTAREA','SELECT','BUTTON','SUMMARY'].includes(document.activeElement.tagName))return;if(e.key==='/'){e.preventDefault();if(location.hash)location.hash='catalog';requestAnimationFrame(()=>$('#course-search').focus())}if(current!==null&&e.key==='ArrowRight'&&current<101)location.hash=`lesson-${String(current+1).padStart(2,'0')}`;if(current!==null&&e.key==='ArrowLeft'&&current>0)location.hash=`lesson-${String(current-1).padStart(2,'0')}`});
$('#export-progress').addEventListener('click',()=>{const blob=new Blob([JSON.stringify({...state,exportedAt:new Date().toISOString()},null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='概率手记-学习进度与笔记.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)});
$('#import-progress').addEventListener('change',async e=>{const f=e.target.files[0];if(!f)return;try{if(f.size>10000000)throw Error('文件太大');const incoming=validate(JSON.parse(await f.text()));state.completed=[...new Set([...state.completed,...incoming.completed])];state.notes={...state.notes,...incoming.notes};state.last=incoming.last;save();progress();if(current!==null)$('[data-note]',$('#lesson-'+String(current).padStart(2,'0'))).value=state.notes[current]||'';$('#storage-status').textContent='已合并导入；同一节笔记采用导入版本。'}catch{$('#storage-status').textContent='导入失败：请选择本课程导出的 JSON 文件。'}e.target.value=''});
window.addEventListener('hashchange',navigate);navigate();
})();
