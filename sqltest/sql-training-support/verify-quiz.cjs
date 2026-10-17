const {chromium}=require('playwright');
const fs=require('node:fs');const assert=require('node:assert/strict');
process.chdir(require('node:path').resolve(__dirname,'..'));
(async()=>{
const browser=await chromium.launch({headless:true,channel:'msedge'});
const page=await browser.newPage({viewport:{width:1440,height:1000}});const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('dialog',d=>d.accept());
await page.goto('file:///'+process.cwd().replace(/\\/g,'/')+'/1.html');
await page.evaluate(()=>{localStorage.removeItem(KEY);state=blank();resetView();});
assert.equal(await page.locator('#total').textContent(),'233');
assert.equal(await page.locator('.question').count(),12);
await page.locator('#q0 input[value="1"]').check();await page.locator('#q0 [data-check]').click();assert.match(await page.locator('#q0 .feedback').textContent(),/回答正确/);
await page.locator('#q1 input[value="0"]').check();assert.equal(await page.locator('#q1 .feedback').count(),0);await page.locator('#q1 input[value="1"]').check();await page.locator('#q1 [data-check]').click();assert.match(await page.locator('#q1 .feedback').textContent(),/回答正确/);
await page.locator('#q1 input[value="2"]').check();assert.equal(await page.locator('#q1 .feedback').count(),0);await page.locator('#q1 [data-check]').click();assert.match(await page.locator('#q1 .feedback').textContent(),/需要再练习/);
await page.locator('#q0 [data-star]').click();await page.reload();assert.equal(await page.locator('#q0 input[value="1"]').isChecked(),true);assert.match(await page.locator('#q0 [data-star]').textContent(),/已收藏/);
await page.selectOption('#mode','exam');assert.equal(await page.locator('.feedback').count(),0);assert.equal(await page.locator('[data-check]').count(),0);await page.locator('#submit').click();assert.equal(await page.locator('#q0 input[value="1"]').isDisabled(),true);assert.match(await page.locator('#result').textContent(),/未答/);
await page.locator('#retry').click();assert.equal(await page.locator('#q0 input[value="1"]').isDisabled(),false);assert.equal(await page.locator('.feedback').count(),0);await page.selectOption('#mode','practice');
const logic=await page.evaluate(()=>{
 const fill=BANK.find(q=>q.q.includes('删除 student 表中 id 为 1 的记录'));
 const check=a=>{state.answers[fill.id]=a;return right(fill);};
 const r=[check('DELETE FROM student WHERE id=1;'),check('delete from student'),check('delete from student where id=1 OR 1=1'),norm("select 'A B'")!==norm("select 'AB'"),norm("select 'ABC'")!==norm("select 'abc'"),norm('select 1;select 2')!==norm('select 1 select 2')];
 let rejected=false;try{validate({version:1});}catch{rejected=true;}
 return {r,rejected,bank:BANK.every(q=>q.q&&q.e&&q.a.length&&(q.type==='f'||q.a.every(a=>q.o[a]!==undefined)))};
});assert.deepEqual(logic.r,[true,false,false,true,true,true]);assert(logic.rejected&&logic.bank);
await page.locator('#search').fill('不存在的知识点XXXX');assert.equal(await page.locator('.empty').count(),1);assert.equal(await page.locator('#submit').isDisabled(),true);await page.locator('#search').fill('');await page.locator('#next').click();assert.match(await page.locator('#pageinfo').textContent(),/2 \/ 20/);
await page.locator('[data-tab="learn"]').click();assert.equal(await page.locator('.lesson').count(),6);await page.locator('[data-practice="窗口函数"]').click();assert.equal(await page.locator('#quiz').isVisible(),true);assert.equal(await page.locator('.question').count(),6);
await page.locator('[data-tab="lab"]').click();assert.equal(await page.locator('.case').count(),8);await page.locator('[data-draft="0"]').fill("SELECT '<script>alert(1)</script>';");await page.reload();await page.locator('[data-tab="lab"]').click();assert.equal(await page.locator('[data-draft="0"]').inputValue(),"SELECT '<script>alert(1)</script>';");await page.locator('[data-case="0"]').check();
const dl=page.waitForEvent('download');await page.locator('#dataset').click();assert.equal((await dl).suggestedFilename(),'sql-training-data.sql');
await page.locator('[data-tab="review"]').click();assert.match(await page.locator('#review').textContent(),/实战自评完成 1 \/ 8/);
await page.evaluate(()=>{state=blank();save();resetView();switchTab('quiz');});await page.screenshot({path:'sql-training-support/quiz-desktop.png',fullPage:false});await page.setViewportSize({width:390,height:844});await page.screenshot({path:'sql-training-support/quiz-mobile.png',fullPage:false});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));assert.deepEqual(errors,[]);
await browser.close();console.log('PASS: rendering, selection, multi-answer submission, persistence, exam visibility/lock/retry, strict SQL matching, data validation, filters/paging, lessons, lab drafts/downloads, review, mobile overflow, no JS errors.');
})().catch(e=>{console.error(e);process.exit(1);});
