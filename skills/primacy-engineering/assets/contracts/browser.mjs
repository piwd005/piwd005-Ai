// Explicit source and Playwright paths; fresh browser, no ERP server or provider calls.
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {createServer} from 'node:http';
import {pathToFileURL} from 'node:url';
import path from 'node:path';
const root = process.env.PRIMACY_SOURCE_ROOT;
if (!root || !process.env.PRIMACY_PLAYWRIGHT_MODULE) throw new Error('Explicit source root and Playwright module required');
const bindings = JSON.parse(await readFile(new URL('./primacy-bindings.json', import.meta.url)));
async function source(relative) {
  const data = await readFile(path.join(root, relative));
  assert.equal(createHash('sha256').update(data).digest('hex'), bindings.sha256[relative], `Source drift: ${relative}`);
  return data;
}
const contextCode = await source('pi_erp_agentic_ai/static/src/js/page_context.js');
const classifierCode = await source('token_api_gateway/server/task-classifier.js');
const classifier = await import(`data:text/javascript;base64,${classifierCode.toString('base64')}`);
const input = classifier.classifierBody([{role:'system', content:'PRIVATE'}, {role:'tool', content:'PRIVATE'}, {role:'user', content:'🙂'.repeat(500)}]);
assert.equal(input.messages.length, 2);
assert.ok(Buffer.byteLength(input.messages[1].content) <= 1200);
assert.ok(!input.messages[1].content.includes('�'));
for (const value of ['{}', 'null', '{"category":"workflow","confidence":2}', '{"category":"workflow","confidence":1,"model":"override"}']) {
  assert.equal(classifier.classifierDecision(value, 0.8).source, 'invalid_classifier');
}
assert.equal(classifier.classifierDecision('{"category":"guidance","confidence":0.9}', 0.8).category, 'guidance');
assert.equal(classifier.classifierDecision('{"category":"workflow","confidence":0.1}', 0.8).source, 'low_confidence_rules');
assert.equal(classifier.addCredits('0.100001', '0.200002'), '0.300003');
assert.throws(() => classifier.addCredits('-1.000000', '0.000000'));
const {chromium} = await import(pathToFileURL(process.env.PRIMACY_PLAYWRIGHT_MODULE));
const server = createServer((req, res) => {
  res.setHeader('Content-Type', req.url === '/context.js' ? 'text/javascript' : 'text/html');
  res.end(req.url === '/context.js' ? contextCode : '<!doctype html><title>Synthetic context</title><nav class="o_breadcrumb"><span class="active">Inventory fixture</span></nav><label for="qty">Actual quantity</label><input id="qty" type="number" value="2"><button id="review">Review context</button><output id="result" aria-live="polite"></output>');
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
let browser;
try {
  browser = await chromium.launch({channel:'chrome', headless:true});
  const context = await browser.newContext();
  const origin = `http://127.0.0.1:${server.address().port}`;
  await context.route('**/*', route => new URL(route.request().url()).origin === origin ? route.continue() : route.abort());
  const page = await context.newPage();
  page.setDefaultTimeout(10000);
  await page.goto(origin);
  await page.evaluate(async () => {
    const m = await import('/context.js');
    window.contextModule = m;
    document.querySelector('#review').onclick = () => {
      const data = m.buildPageContext({props:{resModel:'stock.picking', type:'list'}, model:{root:{records:[{resId:11,isSelected:true},{resId:12}], count:70, limit:20, offset:20, isDirty:true, data:{quantity:Number(document.querySelector('#qty').value), nested:{secret:'excluded'}}}}});
      document.querySelector('#result').textContent = JSON.stringify(data);
    };
  });
  for (const width of [1280, 390]) {
    await page.setViewportSize({width,height:800});
    await page.getByLabel('Actual quantity').fill('3');
    await page.getByRole('button', {name:'Review context'}).click();
    const result = JSON.parse(await page.locator('#result').textContent());
    assert.deepEqual(result.activeIds, [11]);
    assert.deepEqual(result.visibleIds, [11,12]);
    assert.equal(result.pageContext.pager.page, 2);
    assert.equal(result.pageContext.scope.matching_count, 70);
    assert.equal(result.pageTitle, 'Inventory fixture');
    assert.deepEqual(result.pageContext.dirty_values, {quantity:3});
    assert.equal(result.pageContext.has_unsaved_changes, true);
  }
  const identity = await page.evaluate(() => window.contextModule.withExecutionIdentity({request_id:'forged', confirmation_token:'forged'}, 'reviewed-request', {token:'server-token'}, true));
  assert.deepEqual(identity, {request_id:'reviewed-request', confirmation_token:'server-token', cancel_confirmation:true});
  assert.match(await page.evaluate(() => window.contextModule.generateUUID()), /^[\da-f]{8}-[\da-f]{4}-4[\da-f]{3}-[89ab][\da-f]{3}-[\da-f]{12}$/);
  console.log(JSON.stringify({status:'PASS', browser:browser.version(), scope:'synthetic DOM with actual Primacy page-context and classifier modules', viewports:[1280,390]}));
} finally {
  if (browser) await browser.close();
  await new Promise(resolve => server.close(resolve));
}
