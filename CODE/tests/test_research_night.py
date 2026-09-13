import importlib.util
import json
import os
import signal
import subprocess
from pathlib import Path
import sys
import tempfile
import time
import unittest

SPEC = importlib.util.spec_from_file_location('night', Path(__file__).resolve().parents[2] / 'scripts/research_night.py')
night = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(night)


class NightTests(unittest.TestCase):
    def plan(self):
        return {'parallel': 2, 'total_seconds': 60, 'contract': 'Synthetic integration test; no model.',
                'stages': [{'id': 'produce', 'depends': [], 'seconds': 5, 'prompt': 'produce', 'outputs': ['result.json']},
                           {'id': 'review', 'depends': ['produce'], 'seconds': 5, 'prompt': 'review', 'outputs': ['result.json']},
                           {'id': 'rework', 'depends': ['review'], 'seconds': 5, 'prompt': 'record decision', 'outputs': ['result.json']}]}

    def test_reject_is_delivered_and_next_stage_runs(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / 'SOURCES.md').write_text('Synthetic fixture only, no research material.')
            command = [sys.executable, '-c', "from pathlib import Path; import json; Path('result.json').write_text(json.dumps(dict(outcome='reject',summary='Reject is a valid review result',open_questions=[])))"]
            result = night.run(self.plan(), Path(d), command)
            self.assertEqual(result['status'], 'awaiting_content_review')
            self.assertEqual(result['stages']['review']['result']['outcome'], 'reject')
            self.assertEqual(result['stages']['rework']['state'], 'delivered')
            self.assertTrue(result['stages']['review']['input_hashes'])
            self.assertEqual(result['scientific_acceptance'], 'requires_content_review')

    def test_zero_exit_missing_delivery_blocks_successors(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / 'SOURCES.md').write_text('Synthetic fixture only, no research material.')
            result = night.run(self.plan(), Path(d), [sys.executable, '-c', 'pass'])
            self.assertEqual(result['status'], 'execution_blocked')
            self.assertEqual(result['pending'], ['review', 'rework'])

    def test_timeout_is_bounded_and_receipt_survives(self):
        with tempfile.TemporaryDirectory() as d:
            stage = self.plan()['stages'][0]
            start = time.monotonic()
            result = night.execute(Path(d), stage, self.plan(), start + .1,
                                   [sys.executable, '-c', 'import time; time.sleep(10)'])
            self.assertEqual(result['state'], 'timeout')
            self.assertLess(time.monotonic() - start, 5)
            self.assertTrue((Path(d) / 'jobs/produce/receipt.json').exists())

    def test_artifact_escape_rejected(self):
        p = self.plan()
        p['stages'][0]['outputs'].append('../escape')
        with self.assertRaises(ValueError): night.check(p)

    def test_duplicate_id_and_forward_dependency_rejected(self):
        p = self.plan(); p['stages'][1]['id'] = 'produce'
        with self.assertRaises(ValueError): night.check(p)
        p = self.plan(); p['stages'][0]['depends'] = ['review']
        with self.assertRaises(ValueError): night.check(p)

    def test_existing_run_never_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'RUN.json'; p.write_text('{"original":true}')
            with self.assertRaises(ValueError): night.run(self.plan(), Path(d))
            self.assertEqual(json.loads(p.read_text()), {'original': True})

    def test_missing_scope_prevents_model_launch(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError, 'source-scope'):
                night.run(self.plan(), Path(d))
            self.assertFalse((Path(d) / 'jobs').exists())

    def test_changed_delivered_dependency_blocks_launch(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            command = [sys.executable, '-c', "import json; open('result.json','w').write(json.dumps(dict(outcome='findings',summary='fixture',open_questions=[])))"]
            night.execute(root, self.plan()['stages'][0], self.plan(), time.monotonic()+5, command)
            (root/'jobs/produce/result.json').write_text('changed')
            with self.assertRaisesRegex(ValueError, 'dependency changed'):
                night.execute(root, self.plan()['stages'][1], self.plan(), time.monotonic()+5, command)
            self.assertFalse((root/'jobs/review/stdout.txt').exists())

    def test_controller_sigterm_preserves_cancelled_receipt(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root/'SOURCES.md').write_text('Synthetic fixture only.')
            code = "import importlib.util,pathlib,sys; s=importlib.util.spec_from_file_location('n',sys.argv[1]); n=importlib.util.module_from_spec(s); s.loader.exec_module(n); n.run(" + repr(self.plan()) + ",pathlib.Path(sys.argv[2]),[sys.executable,'-c','import time; time.sleep(30)'])"
            proc = subprocess.Popen([sys.executable, '-c', code, str(SPEC.origin), d])
            try:
                receipt = root/'jobs/produce/receipt.json'
                limit = time.monotonic()+5
                while time.monotonic()<limit:
                    if receipt.exists() and 'pid' in json.loads(receipt.read_text()): break
                    time.sleep(.02)
                else: self.fail('worker did not start')
                pid = json.loads(receipt.read_text())['pid']
                proc.send_signal(signal.SIGTERM)
                proc.wait(timeout=6)
                self.assertEqual(json.loads((root/'RUN.json').read_text())['status'], 'cancelled')
                with self.assertRaises(ProcessLookupError): os.kill(pid, 0)
            finally:
                if proc.poll() is None: proc.kill(); proc.wait()

    def test_source_scope_mutation_blocks_run(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root/'SOURCES.md').write_text('Original scope')
            command = [sys.executable, '-c', "from pathlib import Path; Path('../../SOURCES.md').write_text('Expanded scope')"]
            result = night.run(self.plan(), root, command)
            self.assertEqual(result['status'], 'execution_blocked')
            self.assertIn('scope_error', result)
            self.assertFalse((root/'jobs/review').exists())


if __name__ == '__main__': unittest.main()
