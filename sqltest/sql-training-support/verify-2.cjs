const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const path=require('node:path');
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'msedge'});
 const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('dialog',d=>d.accept());
 await page.goto('file:///'+path.resolve(__dirname,'../2.html').replace(/\\/g,'/'));
 assert.equal(await page.locator('#total').textContent(),'120');
 // Old records still load; newest case drafts also survive validation.
 assert(await page.evaluate(()=>{const old={...blank(),answers:{0:1},graded:{0:true},drafts:{11:'SELECT 1;'},cases:{11:true}};const out=validate(old);return out.answers[0]===1&&out.drafts[11]==='SELECT 1;'&&out.cases[11]===true;}));
 await page.selectOption('#filter','new');assert.match(await page.locator('#range').textContent(),/60/);assert.equal(await page.locator('.question').first().getAttribute('id'),'q60');
 await page.selectOption('#filter','all');
 await page.locator('#q0 input[value="1"]').check();await page.locator('#q0 [data-check]').click();
 assert.match(await page.locator('#q0 .feedback').textContent(),/回答正确/);
 await page.locator('#q4 input[value="0"]').check();await page.locator('#q4 [data-check]').click();
 assert.match(await page.locator('#q4 .feedback').textContent(),/需要再练习/);
 await page.locator('#q4 input[value="2"]').check();await page.locator('#q4 [data-check]').click();
 assert.match(await page.locator('#q4 .feedback').textContent(),/回答正确/);
 await page.locator('#q0 [data-star]').click();await page.reload();
 assert(await page.locator('#q0 input[value="1"]').isChecked());
 await page.selectOption('#filter','star');assert.equal(await page.locator('.question').count(),1);
 await page.selectOption('#filter','all');await page.selectOption('#mode','exam');
 assert.equal(await page.locator('.feedback').count(),0);await page.locator('#submit').click();
 assert(await page.locator('#q0 input[value="1"]').isDisabled());await page.locator('#retry').click();
 assert(!(await page.locator('#q0 input[value="1"]').isDisabled()));await page.selectOption('#mode','practice');
 await page.locator('#search').fill('不存在测试XXXX');assert.equal(await page.locator('.empty').count(),1);
 await page.locator('#search').fill('');await page.locator('#next').click();assert.match(await page.locator('#pageinfo').textContent(),/2 \/ 10/);
 await page.locator('[data-tab="learn"]').click();assert.equal(await page.locator('.lesson').count(),6);
 await page.locator('[data-practice="窗口函数与分析"]').click();assert.match(await page.locator('#range').textContent(),/20/);
 await page.locator('[data-tab="lab"]').click();assert.equal(await page.locator('.case').count(),24);
 await page.locator('[data-draft="23"]').fill("SELECT '<script>test</script>';");await page.locator('[data-case="23"]').check();
 await page.reload();await page.locator('[data-tab="lab"]').click();
 assert.equal(await page.locator('[data-draft="23"]').inputValue(),"SELECT '<script>test</script>';");
 for(const id of ['dataset','solutions']){const d=page.waitForEvent('download');await page.locator('#'+id).click();assert.match((await d).suggestedFilename(),/sql-training-2-/);}
 await page.locator('[data-tab="review"]').click();assert.match(await page.locator('#review').textContent(),/1 \/ 24/);
 assert(await page.evaluate(()=>{let rejected=false;try{validate({...blank(),chapter:1})}catch{rejected=true}return rejected&&BANK.every(q=>q.a.every(a=>q.o[a]!==undefined))&&KEY!=='mysqlLearning.v2'}));
 await page.evaluate(()=>{state=blank();save();resetView();switchTab('quiz')});
 await page.screenshot({path:path.join(__dirname,'2-desktop.png')});
 await page.setViewportSize({width:390,height:844});await page.screenshot({path:path.join(__dirname,'2-mobile.png')});
 for(const tab of ['quiz','learn','lab','review']){await page.locator(`[data-tab="${tab}"]`).click();assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),tab+' overflow');}
 assert.deepEqual(errors,[]);await browser.close();console.log('PASS: 120 questions, grading, exam, new-question filter, paging, 6 lessons, 24 cases, old/new persistence, downloads, record isolation, responsive layout; no JS errors.');
})().catch(e=>{console.error(e);process.exit(1)});
