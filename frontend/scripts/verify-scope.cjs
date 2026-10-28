/* Regression against the actual local app and immutable original report. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');

(async()=>{
  const browser=await chromium.launch({headless:true,...(process.env.PLAYWRIGHT_BROWSER_CHANNEL?{channel:process.env.PLAYWRIGHT_BROWSER_CHANNEL}:{})});
  const context=await browser.newContext({viewport:{width:1440,height:1000},timezoneId:'America/New_York',reducedMotion:'reduce'});
  const page=await context.newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  const runId=process.env.SCOPE_RUN_ID;
  assert(runId,'Set SCOPE_RUN_ID to the corrected completed run');
  try{
    const api='http://localhost:5173';
    const {result}=await (await context.request.get(api+'/api/research-runs/'+runId)).json();
    assert.equal(result.policy_version,'us-evidence-2026-10-27.v3');
    assert.equal(result.condition,'Type 2 diabetes');
    assert(!result.citations.some(c=>c.canonical_id==='NCT01954147'));
    for(const claim of result.claims){
      for(const ref of claim.references){
        const citation=result.citations.find(c=>c.id===ref.citation_id);
        assert(citation.eligible_sections.includes(claim.section),'Population/section leak');
      }
    }
    await page.goto(api+'/?run='+runId);
    await page.getByRole('heading',{name:'What the retrieved evidence supports'}).waitFor();
    assert(await page.getByText('Standard-of-care evidence unavailable',{exact:true}).count());
    assert(await page.getByRole('heading',{name:'Specific populations — separate evidence',exact:true}).count());
    const markdown=await (await context.request.get(api+`/api/research-runs/${runId}/export?format=markdown`)).text();
    assert(markdown.includes('## Standard of care'));
    assert(markdown.includes('## Specific populations'));
    assert(!markdown.includes('NCT01954147'));
    fs.mkdirSync('data',{recursive:true});
    await page.screenshot({path:'data/evidence-scope-corrected.png',fullPage:true});
    await page.goto(api+'/?run=d9e18095-7c51-4688-9e2f-96d682c52f98');
    await page.getByText('This saved briefing uses an older evidence policy.',{exact:false}).waitFor();
    await page.getByRole('tab',{name:/Citation register/}).click();
    await page.locator('.citation-row').filter({hasText:'NCT01954147'}).click();
    assert(await page.getByRole('dialog').isVisible());
    assert(await page.getByText('Feb 20, 2014',{exact:true}).count(),'Pure source date shifted in US timezone');
    await page.keyboard.press('Escape');
    assert.deepEqual(errors,[]);
    fs.writeFileSync('data/scope-ui-verification.json',JSON.stringify({runId,status:'passed',checks:['section scope gates','old trial absent from live result','separate population section','guideline gap wording','Markdown sections','historical-policy notice','date-only value in US timezone','no browser errors']},null,2));
    console.log('Scope UI verification passed for '+runId);
  }finally{await browser.close()}
})().catch(e=>{console.error(e.message);process.exitCode=1});
