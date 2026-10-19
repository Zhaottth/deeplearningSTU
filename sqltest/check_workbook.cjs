// Offline UI wiring / persistence checks. No database or browser is emulated.
const fs=require('fs'), vm=require('vm'), assert=require('assert');
const html=fs.readFileSync(__dirname+'/2.html','utf8');
assert(html.includes('id="lab-range"'));
assert(html.includes('预期结果：0 行'));
const source=html.match(/<script>([\s\S]*?)<\/script>/)[1];
function run(saved){
 const nodes=new Map();
 const node=key=>{if(!nodes.has(key))nodes.set(key,{textContent:'',innerHTML:'',value:'',hidden:false,dataset:{},classList:{toggle(){},remove(){}},setAttribute(){},querySelectorAll(){return []},querySelector(){return null},scrollIntoView(){},addEventListener(){}});return nodes.get(key);};
 const ctx={document:{querySelector:node,querySelectorAll:()=>[],hidden:false,getElementsByName:()=>[]},localStorage:{getItem:()=>saved?JSON.stringify(saved):null,setItem(){}},window:{addEventListener(){}},setInterval(){},setTimeout(){},console,Blob,URL,confirm:()=>true};
 vm.createContext(ctx);vm.runInContext(source,ctx);
 const evaluate=s=>vm.runInContext(s,ctx);
 assert.equal(evaluate('BANK.length'),400);assert.equal(evaluate('CASES.length'),48);
 assert.equal(evaluate('new Set(BANK.map(q=>q.q)).size'),400);
 assert.equal(evaluate('BANK.every(q=>q.a.length>0&&q.a.every(a=>Number.isInteger(a)&&a>=0&&a<q.o.length))'),true);
 assert.equal(evaluate('BANK.every(q=>typeof q.e==="string"&&q.e.trim().length>0)'),true);
 assert.equal(evaluate('BANK.slice(200).every(q=>new Set(q.o).size===4&&q.e.length>60)'),true);
 evaluate("filter='new';applyFilter()");assert.equal(evaluate('activeIds.length'),80);
 for(const [filter,n] of [['latest',200],['reasoning',120],['systems',80],['concurrency',40],['performance',40]]){
   evaluate(`filter='${filter}';topic='all';query='';applyFilter()`);
   assert.equal(evaluate('activeIds.length'),n);
 }
 evaluate("filter='concurrency';query='死锁';applyFilter()");assert(evaluate('activeIds.length')>0);
 assert.equal(evaluate("activeIds.every(id=>BANK[id].batch==='concurrency')"),true);
 evaluate("switchTab('engineering')");assert.equal(nodes.get('#engineering').hidden,false);assert(nodes.get('#engineering').innerHTML.includes('P8'));
 evaluate("switchTab('lab')");assert(nodes.get('#lab').innerHTML.includes('实战 48 / 48'));
 assert(nodes.get('#lab').innerHTML.includes('只下载新电商数据'));
 evaluate("state.projects[7]={note:'实验记录',checks:[0,1,2,3]};state.drafts[47]='SELECT 1;';state.cases[47]=true;state=validate(JSON.parse(JSON.stringify(state)));renderReview();");
 assert.equal(evaluate('state.drafts[47]'),'SELECT 1;');assert.equal(evaluate('state.projects[7].note'),'实验记录');
 assert(nodes.get('#review').innerHTML.includes('工程自评达标 1 / 8'));
 evaluate("const q=BANK[120];state.answers[q.id]=q.a[0];grade(q);");assert.equal(evaluate('right(BANK[120])'),true);
 evaluate("for(const q of BANK.slice(200)){state.answers[q.id]=q.a[0];grade(q);}state.stars[399]=true;state=validate(JSON.parse(JSON.stringify(state)));");
 assert.equal(evaluate('BANK.slice(200).every(q=>right(q)&&state.graded[q.id])'),true);
 assert.equal(evaluate('state.stars[399]'),true);
 evaluate("state.answers[399]=(BANK[399].a[0]+1)%4;delete state.graded[399];grade(BANK[399]);");
 assert.equal(evaluate('right(BANK[399])'),false);assert.equal(evaluate('state.history[399].errors'),1);
 evaluate("filter='wrong';topic='all';query='';applyFilter()");assert.equal(evaluate('activeIds.includes(399)'),true);
 return evaluate;
}
run();
const old={version:2,chapter:2,answers:{0:1},graded:{0:true},stars:{0:true},history:{},drafts:{23:'old SQL'},cases:{23:true},seconds:30};
const e=run(old);assert.equal(e('state.answers[0]'),1);assert.equal(e('state.drafts[23]'),'old SQL');
console.log('PASS: syntax, 400 question schemas/explanations, 48 labs, six batch filters, tabs, 200 new answers, wrong-answer grading, export/import validation and legacy progress.');
