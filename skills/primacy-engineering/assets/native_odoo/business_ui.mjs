import assert from 'node:assert/strict';
import {readFile, writeFile} from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const fixture = JSON.parse(await readFile(process.env.PRIMACY_NATIVE_FIXTURE));
const origin = process.env.PRIMACY_NATIVE_ORIGIN;
const target = new URL(origin);
if (target.hostname !== '127.0.0.1' || target.protocol !== 'http:' || !fixture.db.startsWith('primacy_native')) throw new Error('Disposable loopback QA only');
const {chromium} = await import(pathToFileURL(process.env.PRIMACY_PLAYWRIGHT_MODULE));
const browser = await chromium.launch({channel:'chrome', headless:true});
const context = await browser.newContext({viewport:{width:1440,height:1000}});
await context.route('**/*', route => new URL(route.request().url()).origin === origin ? route.continue() : route.abort());
const page = await context.newPage();
page.setDefaultTimeout(60000);
const errors = [];
page.on('pageerror', error => errors.push(error.message));
page.on('console', message => {if(message.type() === 'error') errors.push(message.text());});
const evidence = process.env.PRIMACY_NATIVE_EVIDENCE;
async function call(model, method, args, kwargs={}) {
    assert.ok(['read','search_read','search_count'].includes(method), 'Read-only verification RPC');
    const response = await context.request.post(origin+'/web/dataset/call_kw/'+model+'/'+method, {data:{jsonrpc:'2.0',method:'call',params:{model,method,args,kwargs},id:2}});
    const payload = await response.json();
    if(payload.error) throw new Error(JSON.stringify(payload.error));
    return payload.result;
}
async function clickAction(model, method, button) {
    await button.waitFor({state:'visible'});
    const [response] = await Promise.all([
        page.waitForResponse(response => response.request().method() === 'POST' && response.url().includes('/'+model+'/'+method)),
        button.click(),
    ]);
    const payload = await response.json();
    if(payload.error) throw new Error(JSON.stringify(payload.error));
    return payload.result;
}
async function screenshot(name) {await page.screenshot({path:path.join(evidence,`business-${fixture.series}-${name}.png`),fullPage:true,animations:'disabled'});}
try {
    const response = await context.request.post(origin+'/web/session/authenticate', {data:{jsonrpc:'2.0',method:'call',params:{db:fixture.db,login:fixture.login,password:fixture.password},id:1}});
    assert.ok((await response.json()).result?.uid, 'Synthetic login');
    const module = await call('ir.module.module','search_read',[[['name','=','prierp_core']]],{fields:['state','installed_version']});
    if(fixture.series === 20) assert.equal(module[0]?.state,'installed');
    await page.goto(origin+`/odoo/mrp.production/${fixture.production}`,{waitUntil:'domcontentloaded'});
    await clickAction('mrp.production','action_confirm',page.locator('button[name="action_confirm"]:visible'));
    console.log('Manufacturing confirmed through native UI');
    const quantity = page.locator('.o_field_widget[name="qty_producing"] input:visible');
    await quantity.fill('1');
    await quantity.press('Tab');
    await screenshot('manufacturing-before');
    await clickAction('mrp.production','button_mark_done',page.locator('button[name="button_mark_done"]:visible'));
    const production = (await call('mrp.production','read',[[fixture.production],['state','move_raw_ids','move_finished_ids']]))[0];
    assert.equal(production.state,'done');
    const raw = await call('stock.move','read',[production.move_raw_ids,['quantity','state']]);
    const finished = await call('stock.move','read',[production.move_finished_ids,['quantity','state']]);
    assert.equal(raw.reduce((sum,row)=>sum+row.quantity,0),2);
    assert.equal(finished.reduce((sum,row)=>sum+row.quantity,0),1);
    async function stock(product,location) {
        const rows = await call('stock.quant','search_read',[[['product_id','=',product],['location_id','=',location]]],{fields:['quantity']});
        return rows.reduce((sum,row)=>sum+row.quantity,0);
    }
    assert.equal(await stock(fixture.component,fixture.source_location),8);
    assert.equal(await stock(fixture.finished,fixture.destination_location),1);
    await page.locator('[name="state"] [data-value="done"][aria-checked="true"]:visible').waitFor();
    await screenshot('manufacturing-done');
    console.log('Manufacturing reconciled: consumed 2, produced 1, stock 8/1');
    await page.goto(origin+`/odoo/account.move/${fixture.bill}`,{waitUntil:'domcontentloaded'});
    await clickAction('account.move','action_post',page.locator('button[name="action_post"]:visible'));
    const bill = (await call('account.move','read',[[fixture.bill],['state','amount_total','line_ids','amount_residual']]))[0];
    assert.equal(bill.state,'posted');assert.equal(bill.amount_total,100);
    const billLines = await call('account.move.line','read',[bill.line_ids,['balance','account_id']]);
    assert.equal(billLines.reduce((sum,row)=>sum+row.balance,0),0);
    await page.locator('[name="state"] [data-value="posted"][aria-checked="true"]:visible').waitFor();
    await screenshot('bill-posted');
    await clickAction('account.move','action_reverse',page.locator('button[name="action_reverse"]:visible'));
    await page.getByRole('dialog').waitFor();
    await page.getByRole('dialog').locator('.o_field_widget[name="reason"] input').fill('Synthetic native browser QA');
    await clickAction('account.move.reversal','refund_moves',page.getByRole('dialog').locator('button[name="refund_moves"]'));
    await page.getByRole('dialog').waitFor({state:'hidden'});
    const credits = await call('account.move','search_read',[[['reversed_entry_id','=',fixture.bill]]],{fields:['state','move_type','amount_total','line_ids']});
    assert.equal(credits.length,1);assert.equal(credits[0].move_type,'in_refund');
    console.log('Native credit note wizard completed');
    await page.goto(origin+`/odoo/account.move/${credits[0].id}`,{waitUntil:'domcontentloaded'});
    await clickAction('account.move','action_post',page.locator('button[name="action_post"]:visible'));
    const credit = (await call('account.move','read',[[credits[0].id],['state','amount_total','amount_residual','line_ids']]))[0];
    assert.equal(credit.state,'posted');assert.equal(credit.amount_total,100);assert.equal(credit.amount_residual,0);
    const reconciledBill = (await call('account.move','read',[[fixture.bill],['amount_residual']]))[0];
    assert.equal(reconciledBill.amount_residual,0);
    const creditLines = await call('account.move.line','read',[credit.line_ids,['balance','account_id']]);
    assert.equal(creditLines.reduce((sum,row)=>sum+row.balance,0),0);
    assert.equal([...billLines,...creditLines].filter(row=>row.account_id[0]===fixture.expense).reduce((sum,row)=>sum+row.balance,0),0);
    await page.locator('[name="state"] [data-value="posted"][aria-checked="true"]:visible').waitFor();
    await screenshot('credit-posted');
    assert.deepEqual(errors,[],'No unexpected browser errors');
    const result = {status:'PASS',series:fixture.series,browser:browser.version(),core:module[0]||null,core_status:fixture.core_status||null,manufacturing:{state:'done',consumed:2,produced:1,component_stock:8,finished_stock:1},accounting:{bill:100,credit:100,bill_residual:0,credit_residual:0,balanced:true},browser_errors:0,ui_status_verified:true};
    await writeFile(path.join(evidence,`business-ui-${fixture.series}-result.json`),JSON.stringify(result,null,2));
    console.log(JSON.stringify(result));
} catch(error) {
    try {await page.screenshot({path:path.join(evidence,`business-${fixture.series}-failure.png`),fullPage:true,timeout:3000});} catch { /* Preserve original failure. */ }
    throw error;
} finally {await browser.close();}
