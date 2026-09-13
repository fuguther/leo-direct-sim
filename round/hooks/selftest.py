#!/usr/bin/env python3
"""Isolated regression suite: never swaps a running permission manifest."""
import csv, importlib.util, json, os, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
SOURCE = Path(__file__).resolve().parents[2]

class ClosureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='research-closure-')
        self.root = Path(self.tmp.name)
        shutil.copytree(SOURCE/'round/hooks', self.root/'round/hooks', ignore=shutil.ignore_patterns('__pycache__','permissions*','orchestrator.id','unregistered.log'))
        shutil.copytree(SOURCE/'round/tools', self.root/'round/tools', ignore=shutil.ignore_patterns('__pycache__'))
        self.h = self.root/'round/hooks'
        self.cli('perm.py','init','--run','test','--orchestrator','main')
    def tearDown(self): self.tmp.cleanup()
    def cli(self, script, *args, ok=0):
        folder=self.h if script=='perm.py' else self.root/'round/tools'
        p=subprocess.run([sys.executable,str(folder/script),*map(str,args)],capture_output=True,text=True,cwd=self.root)
        self.assertEqual(p.returncode,ok,p.stdout+p.stderr)
        return p.stdout
    def hook(self,sid,path,tool='read',ok=0):
        payload={'session_id':sid,'cwd':str(self.root),'tool_name':tool,'tool_input':{'file_path':str(self.root/path)}}
        p=subprocess.run([sys.executable,str(self.h/'hook_access_guard.py')],input=json.dumps(payload),capture_output=True,text=True)
        self.assertEqual(p.returncode,ok,p.stdout+p.stderr)
    def bind(self,sid='child',role='deepener'):
        self.cli('perm.py','bind','--session',sid,'--role',role,'--extra-read','card.md','--extra-write','draft.md')
    def test_no_anonymous_ticket(self):
        self.cli('perm.py','reserve','--role','generator',ok=2)
        self.hook('unrelated','card.md',ok=2)
        self.assertEqual(json.loads((self.h/'permissions.json').read_text())['sessions'],{})
    def test_exact_permissions(self):
        self.bind(); self.hook('child','card.md'); self.hook('child','other.md',ok=2)
        self.hook('child','draft.md','write');self.hook('child','other.md','write',ok=2)
        self.cli('perm.py','bind','--session','child','--role','reviewer',ok=2)
    def test_external_read_requires_explicit_grant(self):
        self.bind()
        self.hook('child','/tmp/old-research.md',ok=2)
        self.hook('unrelated','/tmp/other.md')
    def test_resume_requires_reconciled_receipt(self):
        self.bind(); self.cli('perm.py','pause')
        receipt=self.root/'resume.json'
        receipt.write_text(json.dumps({'run_id':'test','active_sessions':['child'],'tasks':[]}))
        self.cli('perm.py','resume','--run','test','--orchestrator','new','--receipt',receipt,ok=2)
        self.hook('child','card.md',ok=2)
    def test_pause_resume_revokes_old_worker(self):
        self.bind();self.cli('perm.py','pause');self.hook('child','card.md',ok=2)
        self.hook('unrelated','/tmp/other.md')
        receipt=self.root/'resume.md';receipt.write_text(json.dumps({'run_id':'test','active_sessions':[],'tasks':[]}))
        self.cli('perm.py','resume','--run','test','--orchestrator','new-main','--receipt',receipt)
        self.hook('child','card.md',ok=2);self.hook('new-main','card.md')
    def test_init_cannot_reset_active(self):
        self.bind();self.cli('perm.py','init','--run','other','--orchestrator','new',ok=2)
        self.hook('child','card.md')
    def test_corrupt_manifest_blocks(self):
        (self.h/'permissions.json').write_text('{broken')
        self.hook('child','card.md',ok=2);self.hook('main','card.md')
    def test_recommendation_all_paths(self):
        cards=self.root/'cards.json';cards.write_text(json.dumps([{'title':'test','difficulty':'original'}]))
        ledger=self.root/'ledger.csv'; reviews=self.root/'reviews.csv'
        self.cli('ledger.py','add','--cards',cards,'--ledger',ledger)
        def current():
            with ledger.open() as f: return list(csv.DictReader(f))[-1]
        cid=current()['cand_id'];card=self.root/'card.md';card.write_text('test')
        args=['--cand-id',cid,'--ledger',ledger]
        self.cli('ledger.py','revise',*args,'--set',json.dumps({'status':'recommended_pending_review'}),'--reason','test','--reviews',reviews,ok=2)
        self.cli('gate_verdict.py','record',*args,'--card',card,'--verdict','PASS')
        self.cli('ledger.py','status',*args,'--status','recommended_pending_review','--reason','test')
        self.cli('ledger.py','revise',*args,'--set',json.dumps({'difficulty':'changed'}),'--reason','test','--reviews',reviews)
        self.assertEqual(current()['status'],'needs_revision')
        self.cli('ledger.py','status',*args,'--status','recommended_pending_review','--reason','test',ok=2)
        self.cli('gate_verdict.py','record',*args,'--card',card,'--verdict','PASS')
        self.cli('ledger.py','revise',*args,'--set',json.dumps({'difficulty':'changed again'}),'--status','recommended_pending_review','--reason','test','--reviews',reviews)
        self.assertEqual(current()['status'],'needs_revision')
        self.cli('gate_verdict.py','record',*args,'--card',card,'--verdict','PASS')
        card.unlink()
        self.cli('ledger.py','status',*args,'--status','recommended_pending_review','--reason','test',ok=2)

if __name__=='__main__': unittest.main(verbosity=2)
