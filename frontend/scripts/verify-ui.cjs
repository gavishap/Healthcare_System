/* Set PLAYWRIGHT_MODULE to a bundled playwright module, or install playwright locally. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');

(async()=>{
  const browser=await chromium.launch({headless:true,...(process.env.PLAYWRIGHT_BROWSER_CHANNEL?{channel:process.env.PLAYWRIGHT_BROWSER_CHANNEL}:{})});
  const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
  const page=await context.newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  const api='http://localhost:5173';
  fs.mkdirSync('data',{recursive:true});
  try{
    const runs=await (await context.request.get(api+'/api/research-runs')).json();
    const live=runs.find(r=>r.mode==='live'&&r.status==='partial');
    assert(live,'The live smoke result must be saved before UI verification.');
    await page.goto(api+'/?run='+live.id);
    await page.getByRole('heading',{name:'What the retrieved evidence supports'}).waitFor();
    assert(await page.getByText('Standard-of-care evidence unavailable',{exact:true}).count());
    await page.getByRole('tab',{name:/Citation register/}).click();
    await page.locator('.citation-row').first().waitFor();
    assert((await page.locator('.citation-row').count())>=2);
    await page.locator('.citation-row').first().click();
    assert(await page.getByRole('dialog').isVisible());
    assert.match(await page.locator('.hash').textContent(),/^[a-f0-9]{64}$/);
    assert((await page.locator('.passage').count())>=1);
    await page.keyboard.press('Escape');
    assert(!(await page.getByRole('dialog').isVisible()));
    await page.screenshot({path:'data/evidence-desk-citations.png',fullPage:true});
    const markdown=await context.request.get(api+`/api/research-runs/${live.id}/export?format=markdown`);
    assert.equal(markdown.status(),200);
    assert((await markdown.text()).includes('snapshot SHA-256'));
    await page.getByRole('tab',{name:'Evidence policy',exact:true}).click();
    assert(await page.getByRole('heading',{name:'Source identity',exact:true}).count());
    await page.getByRole('button',{name:'Run synthetic policy example',exact:true}).click();
    await page.getByText('Synthetic policy demonstration',{exact:true}).waitFor();
    await page.getByRole('tab',{name:/Conflicting evidence/}).click();
    await page.getByRole('heading',{name:'Potential opposing findings'}).waitFor();
    assert.equal(await page.locator('.conflict-sides .claim-block').count(),2);
    await page.screenshot({path:'data/evidence-desk-conflicts.png',fullPage:true});
    await page.getByRole('tab',{name:/Citation register/}).click();
    await page.locator('.citation-row').first().click();
    assert(await page.getByText('Synthetic fixture — no original publication exists.',{exact:true}).count());
    assert.equal(await page.getByRole('link',{name:/Open original record/}).count(),0);
    await page.keyboard.press('Escape');
    await page.setViewportSize({width:375,height:812});
    await page.getByRole('tab',{name:'Briefing',exact:true}).click();
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),'Phone layout overflows horizontally');
    await page.screenshot({path:'data/evidence-desk-mobile.png',fullPage:true});
    await page.setViewportSize({width:812,height:375});
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),'Landscape layout overflows horizontally');
    await page.evaluate(()=>{document.documentElement.style.zoom='1.25'});
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));
    assert.deepEqual(errors,[],'Browser runtime errors occurred');
    fs.writeFileSync('data/ui-verification.json',JSON.stringify({status:'passed',liveRunId:live.id,checks:['citation register','snapshot hash and passage','dialog Escape','cited Markdown export','policy view','synthetic conflict retains both claims','no fake source link','375px and landscape overflow','reduced motion','browser runtime errors'],errors},null,2));
    console.log('UI verification passed: citations, evidence drawer, exports, policy, conflicts, phone/landscape, reduced motion; no runtime errors.');
  }finally{await browser.close()}
})().catch(e=>{console.error(e.message);process.exitCode=1});
