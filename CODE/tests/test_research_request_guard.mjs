import test from 'node:test';
import assert from 'node:assert/strict';
import { apply } from '../../scripts/research_request_guard.mjs';

function setup(overrides={}) {
 const log=[];
 const broker={
  binding: async()=>({run:'fixture'}),
  reserve: async r=>{log.push(['reserve',r]); return {...r,routeAttested:true,costBoundVerified:true};},
  beforeDispatch:async id=>log.push(['dispatch',id]),
  finish:async(id,c)=>log.push(['finish',id,c]),
  uncertain:async id=>log.push(['uncertain',id]), ...overrides
 };
 let listener;
 apply({get:()=>broker,on:(name,fn)=>{assert.equal(name,'llm/stream');listener=fn;}});
 return {log,listener};
}
const opts={sessionId:'fixture',provider:'fixture',model:'fixture',maxTokens:20};
async function collect(g){const a=[];for await(const c of g)a.push(c);return a;}
async function* output(){yield {type:'text',text:'ok'};yield {type:'finish',reason:{kind:'completed'}};}

test('reservation precedes stream and settlement precedes finish',async()=>{
 const {log,listener}=setup();await collect(listener(opts,()=>{log.push(['next']);return output();}));
 assert.deepEqual(log.map(r=>r[0]),['reserve','dispatch','next','finish']);
});
test('retry is a new reservation',async()=>{
 const {log,listener}=setup();await collect(listener(opts,output));await collect(listener(opts,output));
 const ids=log.filter(r=>r[0]==='reserve').map(r=>r[1].requestId);assert.notEqual(ids[0],ids[1]);
});
test('budget rejection never calls provider',async()=>{
 const {listener}=setup({reserve:async()=>{throw Error('budget');}});let called=false;
 await assert.rejects(collect(listener(opts,()=>{called=true;return output();})),/budget/);assert.equal(called,false);
});
test('stop after reserve retains uncertain reservation',async()=>{
 const {log,listener}=setup({beforeDispatch:async()=>{throw Error('stopped');}});
 await assert.rejects(collect(listener(opts,output)),/stopped/);
 assert.equal(log.at(-1)[0],'uncertain');
});
test('lost response retains reservation',async()=>{
 const {log,listener}=setup();await assert.rejects(collect(listener(opts,async function*(){throw Error('lost');})),/lost/);
 assert.equal(log.at(-1)[0],'uncertain');
});
test('unbound sessions unchanged; unavailable broker fails',async()=>{
 const {log,listener}=setup({binding:async()=>null});assert.equal((await collect(listener(opts,output))).length,2);assert.equal(log.length,0);
 assert.throws(()=>apply({get:()=>null}),/MISSING/);
});
test('invalid route attestation blocks dispatch',async()=>{
 const {listener}=setup({reserve:async r=>({...r,routeAttested:false,costBoundVerified:true})});let calls=0;
 await assert.rejects(collect(listener(opts,()=>{calls++;return output();})),/INVALID/);assert.equal(calls,0);
});
