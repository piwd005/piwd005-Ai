// Exercise the actual small Owl trigger class with lifecycle/service fakes.
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import path from 'node:path';
import vm from 'node:vm';
const source=await readFile(path.join(process.env.PRIMACY_SOURCE_ROOT,'pi_erp_agentic_ai/static/src/js/ai_chat_page.js'),'utf8');
const start=source.indexOf('class AiChatTrigger extends Component {');
const end=source.indexOf('// ── CSS',start);
assert.ok(start>=0 && end>start);
for(const fails of [false,true]) {
 let mounted;
 let events=0;
 const Trigger=vm.runInNewContext(source.slice(start,end)+';AiChatTrigger',{
  Component:class {}, xml:()=>'',
  useProps:()=>({action:{context:{}}}), standardActionServiceProps:{},
  useService:()=>({restore:async()=>{if(fails)throw new Error('No controller to restore');}}),
  onMounted:callback=>{mounted=callback;},
  CustomEvent:class {},document:{dispatchEvent:()=>{events++;}},
 });
 const trigger=new Trigger();trigger.props={action:{context:{}}};trigger.setup();
 await assert.doesNotReject(mounted);
 assert.equal(events,1);
}
console.log('PASS: actual trigger awaits and handles restore success/rejection');
