import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor

spec = importlib.util.spec_from_file_location('rh', Path(__file__).resolve().parents[2] / 'scripts/research_harness.py')
rh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rh)


class Fake:
    def __init__(self):
        self.rows = {}; self.calls = []; self.hidden = False; self.fail_cancel = False
    def rpc(self, method, payload):
        self.calls.append((method, payload))
        sid = payload.get('sessionId')
        if method == 'session/create':
            self.rows[sid] = dict(sessionId=sid, cwd=payload['cwd'])
            return {'sessionId': sid}
        if method == 'session/list':
            return {'items': [] if self.hidden else list(self.rows.values())}
        if method == 'session/cancel' and self.fail_cancel:
            raise rh.Blocked('disconnected')
        return {}
    visible = rh.Harness.visible


class Tests(unittest.TestCase):
    def fixture(self, root):
        plan = dict(provider='commandcode-goat-autosync', model='z-ai/glm-5.3-flash',
                    destination='https://api.commandcode.ai/provider/v1', project_cwd=str(root),
                    budget_fen=1000, stages=[{'id': 'produce'}, {'id': 'review'}])
        rh.atomic(root/'PLAN.json', plan)
        (root/'SOURCES.md').write_text('Synthetic fixture only')
        auth = dict(plan, expires_at='2099-01-01T00:00:00+00:00',
                    source_scope_sha256=rh.fingerprint(root/'SOURCES.md'),
                    plan_sha256=rh.fingerprint(root/'PLAN.json'))
        rh.atomic(root/'AUTHORIZATION.json', auth)
        return plan

    def test_prepare_and_restart_never_resend(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); self.fixture(root); c=Fake()
            state=rh.prepare(root,c)
            self.assertEqual(state['status'],'prepared_control_only')
            self.assertEqual(len(state['sessions']),3)
            with self.assertRaises(rh.Blocked):rh.prepare(root,c)
            rh.reconcile(root,c)
            self.assertEqual(sum(m=='session/create' for m,p in c.calls),3)
            self.assertFalse(any(m=='session/prompt' for m,p in c.calls))

    def test_invisible_blocks_next_stage(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root);c=Fake();c.hidden=True
            with self.assertRaises(rh.Blocked):rh.prepare(root,c)
            self.assertEqual(sum(m=='session/create' for m,p in c.calls),1)
            self.assertEqual(json.loads((root/'VISIBLE-RUN.json').read_text())['status'],'execution_blocked')

    def test_scope_and_route_mismatch_before_create(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=self.fixture(root);c=Fake()
            (root/'SOURCES.md').write_text('changed')
            with self.assertRaises(rh.Blocked):rh.prepare(root,c)
            self.assertEqual(c.calls,[])
            p=self.fixture(root);p['model']='other'
            with self.assertRaises(rh.Blocked):rh.validate_authorization(root,p)

    def test_cancel_records_unconfirmed_without_hiding_failure(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root);c=Fake();rh.prepare(root,c)
            c.fail_cancel=True
            s=rh.cancel(root,c)
            self.assertEqual(s['status'],'cancel_unconfirmed')
            self.assertEqual(len(s['cancel_unconfirmed']),3)

    def test_no_real_admission(self):
        with self.assertRaisesRegex(rh.Blocked,'LIVE_REQUEST_GUARD'):
            rh.Harness().admit_prompt('task')
        with self.assertRaises(rh.Blocked):rh.Harness('https://example.org')

    def test_concurrent_budget_restart_and_unknown_response(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'budget.sqlite';b=rh.Budget(p,10)
            def reserve(i):
                try:b.reserve(str(i),6);return True
                except rh.Blocked:return False
            with ThreadPoolExecutor(2) as pool:
                self.assertEqual(sum(pool.map(reserve,range(2))),1)
            b=rh.Budget(p,10)
            with self.assertRaises(rh.Blocked):b.reserve('new',6)
            with self.assertRaises(rh.Blocked):rh.Budget(p,100)

    def test_settlement_idempotence_and_retry_charged(self):
        with tempfile.TemporaryDirectory() as d:
            b=rh.Budget(Path(d)/'b.sqlite',10);b.reserve('a',6)
            with self.assertRaises(rh.Blocked):b.reserve('a',6)
            b.settle('a',2);b.settle('a',2)
            with self.assertRaises(rh.Blocked):b.settle('a',1)
            b.reserve('retry',6)
            with self.assertRaises(rh.Blocked):b.reserve('third',3)
            with self.assertRaises(rh.Blocked):b.settle('retry',7)
            with self.assertRaisesRegex(rh.Blocked,'frozen'):b.reserve('after-overrun',1)

if __name__=='__main__':unittest.main()
