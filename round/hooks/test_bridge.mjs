// Real installed hook bridge + real Python subprocess; synthetic session/tool host.
// This is adapter integration, not a running-web/model-session acceptance test.
import {mkdtempSync, cpSync, writeFileSync, readFileSync, rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {resolve, dirname} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {spawn} from 'node:child_process';
import assert from 'node:assert/strict';
const root=resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const modulePath=process.argv[2] || '/opt/homebrew/lib/node_modules/@deepseek-ai/dsh/node_modules/@deepseek-ai/dsh-hooks-claude-code/lib/index.js';
const {apply}=await import(pathToFileURL(modulePath));
const temp=mkdtempSync(resolve(tmpdir(),'research-bridge-'));
try {
 cpSync(resolve(root,'round/hooks'),resolve(temp,'round/hooks'),{recursive:true});
 const h=resolve(temp,'round/hooks');
 writeFileSync(resolve(h,'permissions.json'),JSON.stringify({run_id:'probe',run_status:'active',orchestrator_session:'main',sessions:{child:{role:'deepener',extra_read:['allowed.md'],extra_write:['draft.md']}}}));
 const events=[], handlers=new Map();
 const ctx={effect:fn=>fn(),logger:{warn:console.warn},get:()=>undefined,on:(name,fn)=>handlers.set(name,fn),sessionProjections:{stateOf:()=>({lastTurn:1})},shell:{
  resolve:r=>r,
  run:r=>new Promise((res,rej)=>{
   const p=spawn('/bin/sh',['-c',r.command],{cwd:r.workdir,env:{...process.env,...r.env,PYTHONDONTWRITEBYTECODE:'1'},signal:r.signal});
   let stdout='',stderr='';p.stdout.on('data',x=>stdout+=x);p.stderr.on('data',x=>stderr+=x);p.on('error',rej);
   p.on('close',exitCode=>res({exitCode,stdout:{text:stdout},stderr:{text:stderr}}));p.stdin.end(r.stdin);
  })
 }};
 apply(ctx,{configPath:resolve(h,'hooks.json'),projectDir:temp});
 assert(handlers.has('tools/pre-execute'));
 async function call(sid,path,expected,tool='read') {
  let executed=false;
  const agent={session:{header:{id:sid,cwd:temp},append:(type,payload)=>events.push({type,...payload})}};
  const result=await handlers.get('tools/pre-execute')({agent,name:tool,arguments:{file_path:path},callId:'probe',signal:new AbortController().signal},async()=>{executed=true;return {kind:'allow'}});
  assert.equal(result.kind,expected);assert.equal(executed,expected==='allow');
 }
 await call('child',resolve(temp,'allowed.md'),'allow');
 await call('child',resolve(temp,'history.md'),'deny');
 await call('child',resolve(temp,'draft.md'),'allow','write');
 await call('child',resolve(temp,'other.md'),'deny','write');
 await call('unknown',resolve(temp,'allowed.md'),'deny');
 await call('unrelated','/tmp/unrelated.md','allow');
 const state=JSON.parse(readFileSync(resolve(h,'permissions.json')));state.run_status='paused';writeFileSync(resolve(h,'permissions.json'),JSON.stringify(state));
 await call('child',resolve(temp,'allowed.md'),'deny');
 assert.equal(events.filter(x=>x.type==='hook/invoked').length,7);
 assert.equal(events.filter(x=>x.type==='hook/result').length,7);
 console.log(JSON.stringify({adapter_integration:'PASS',cases:7,hook_events:events.length,live_web:false,model_requests:0}));
} finally {rmSync(temp,{recursive:true,force:true});}
