import {pathToFileURL} from 'node:url';
import path from 'node:path';
const {chromium}=await import(pathToFileURL(process.env.PRIMACY_PLAYWRIGHT_MODULE));
import {readFile,writeFile} from 'node:fs/promises';
const fixture=JSON.parse(await readFile(process.env.PRIMACY_NATIVE_FIXTURE));
const origin=process.env.PRIMACY_NATIVE_ORIGIN;
const target=new URL(origin);
if(target.hostname!=='127.0.0.1' || target.protocol!=='http:' || !fixture.db.startsWith('primacy_native'))throw new Error('Disposable loopback QA only');
const evidence=process.env.PRIMACY_NATIVE_EVIDENCE;
const browser=await chromium.launch({channel:'chrome',headless:true});
const context=await browser.newContext({viewport:{width:1440,height:1000}});

await context.route('**/*',route=>new URL(route.request().url()).origin===origin?route.continue():route.abort());
const page=await context.newPage();page.setDefaultTimeout(60000);
page.on('pageerror',error=>console.log('PAGE ERROR',error.message));
const errors=[];
page.on('console',message=>{if(message.type()==='error')errors.push(message.text());});
page.on('pageerror',error=>errors.push(error.message));
try {
 const response=await context.request.post(origin+'/web/session/authenticate',{data:{jsonrpc:'2.0',method:'call',params:{db:fixture.db,login:fixture.login,password:fixture.password},id:1}});
 const auth=await response.json();if(!auth.result?.uid)throw new Error('Synthetic login failed');
 await page.goto(origin+`/odoo/stock.picking/${fixture.picking}`,{waitUntil:'domcontentloaded'});
 await page.getByRole('button',{name:'Validate',exact:true}).first().waitFor();
 console.log('Native picking form loaded');
 await page.screenshot({path:path.join(evidence,'native-'+fixture.series+'-receipt-before.png'),fullPage:true});
 await page.getByRole('button',{name:'Validate',exact:true}).first().click();
 await page.getByRole('dialog').waitFor();
 console.log('DIALOG',await page.getByRole('dialog').innerText());
 await page.screenshot({path:path.join(evidence,'native-'+fixture.series+'-backorder.png'),fullPage:true});
 await page.getByRole('dialog').getByRole('button',{name:'Create Backorder',exact:true}).click();
 await page.getByRole('dialog').waitFor({state:'hidden'});
 async function call(model,method,args,kwargs={}) {
   const response=await context.request.post(origin+'/web/dataset/call_kw/'+model+'/'+method,{data:{jsonrpc:'2.0',method:'call',params:{model,method,args,kwargs},id:2}});
   const result=await response.json();if(result.error)throw new Error(result.error.message);return result.result;
 }
 const receipt=await call('stock.picking','read',[[fixture.picking],['state']]);
 if(receipt[0].state!=='done')throw new Error('Receipt not Done');
 const backorders=await call('stock.picking','search_read',[[['backorder_id','=',fixture.picking]]],{fields:['move_ids']});
 if(backorders.length!==1)throw new Error('Expected one backorder');
 const moves=await call('stock.move','read',[backorders[0].move_ids,['product_uom_qty']]);
 if(moves[0].product_uom_qty!==2)throw new Error('Expected backorder quantity 2');
 const quants=await call('stock.quant','search_read',[[['product_id','=',fixture.product],['location_id','=',fixture.location]]],{fields:['quantity']});
 if(quants.reduce((sum,row)=>sum+row.quantity,0)!==3)throw new Error('Expected received stock 3');
 await page.screenshot({path:path.join(evidence,'native-'+fixture.series+'-receipt-done.png'),fullPage:true});
 await page.goto(origin+`/odoo/res.partner/${fixture.contact}`,{waitUntil:'domcontentloaded'});
 await page.locator('.o_field_widget[name="name"] input').fill('Primacy Native Browser Saved');
 const saved=page.waitForResponse(response=>response.url().includes('/res.partner/web_save') && response.status()===200);
 await page.locator('.o_form_button_save').click();
 await saved;
 const contact=await call('res.partner','read',[[fixture.contact],['name']]);
 if(contact[0].name!=='Primacy Native Browser Saved')throw new Error('Native contact save failed');
 await page.setViewportSize({width:390,height:844});
 await page.reload({waitUntil:'domcontentloaded'});
 await page.locator('.o_field_widget[name="name"] input').waitFor();
 if(await page.locator('.o_field_widget[name="name"] input').inputValue()!=='Primacy Native Browser Saved')throw new Error('Mobile reopen did not retain save');
 await page.screenshot({path:path.join(evidence,'native-'+fixture.series+'-contact-mobile.png'),fullPage:true});
 if(fixture.chat_action) {
 const ledgerBefore=await call('ai.assistant.credit.ledger','search_count',[[]]);
 const pickingsBefore=await call('stock.picking','search_count',[[]]);
 await page.setViewportSize({width:1440,height:1000});
 await page.goto(origin+`/odoo/action-${fixture.chat_action}`,{waitUntil:'domcontentloaded'});
 await page.locator('textarea').first().fill('How do I process an inventory transfer?');
 await page.getByTitle('Send message',{exact:true}).click();
 await page.getByText('Nothing has been created or changed.',{exact:false}).first().waitFor();
 await page.screenshot({path:path.join(evidence,'native-'+fixture.series+'-guidance.png'),fullPage:true});
 if(await call('ai.assistant.credit.ledger','search_count',[[]])!==ledgerBefore || await call('stock.picking','search_count',[[]])!==pickingsBefore)throw new Error('Guidance changed business/credit records');
 }
 if(errors.length)throw new Error('Unexpected browser error: '+errors[0].slice(0,200));
 const result={status:'PASS',native_ui:['receipt Validate and Create Backorder','contact edit/save and mobile reopen',...(fixture.chat_action?['Primacy manual inventory guidance']:[])],received:3,backorder:2,browser:browser.version()};
 await writeFile(path.join(evidence,'browser-'+fixture.series+'-result.json'),JSON.stringify(result,null,2));
 console.log(JSON.stringify(result));

} catch(e) {
 try {await page.screenshot({path:path.join(evidence,'native-'+fixture.series+'-failure.png'),fullPage:true,timeout:3000});} catch { /* Preserve the original failure if evidence capture also fails. */ }
 throw e;
} finally {await browser.close();}
