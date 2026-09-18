import contextlib
import hashlib
import io
import json
from pathlib import Path
import runpy
import sys
import tempfile
import unittest
import run_evaluation

class RunnerTests(unittest.TestCase):
    def fixture(self, root, result='PASS'):
        root=Path(root); (root/'evaluation').mkdir();(root/'source').mkdir()
        (root/'source/SKILL.md').write_bytes(b'name: fixture\n')
        rows=[{'path':'SKILL.md','bytes':14,'sha256':hashlib.sha256(b'name: fixture\n').hexdigest()}]
        digest=hashlib.sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest()
        (root/'source-manifest.json').write_text(json.dumps({'files':rows,'package_digest':digest}))
        (root/'evidence.txt').write_bytes(b'observed')
        ref={'path':'evidence.txt','sha256':hashlib.sha256(b'observed').hexdigest()}
        case=[{'case_id':'QV-01'}]
        obs={'case_id':'QV-01','result':result,'reason':'Independent test fixture','method':'semantic','evidence':[ref]}
        (root/'evaluation/cases.json').write_text(json.dumps(case))
        (root/'evaluation/observations.jsonl').write_text(json.dumps(obs)+'\n')
        artifact={'path':'evaluation/cases.json','sha256':hashlib.sha256((root/'evaluation/cases.json').read_bytes()).hexdigest()}
        (root/'evaluation/bundle-manifest.json').write_text(json.dumps({'package_digest':digest,'artifacts':[artifact]}))
        return root

    def invoke(self, root, output='output.jsonl', as_script=False):
        old=sys.argv
        sys.argv=['run_evaluation.py','--run-root',str(root),'--output',str(root/output)]
        try:
            with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
                if as_script:
                    try: runpy.run_path(run_evaluation.__file__,run_name='__main__')
                    except SystemExit as e: return e.code
                return run_evaluation.main()
        finally: sys.argv=old

    def test_emits_bound_rows_and_summary(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.fixture(d)
            self.assertEqual(self.invoke(root),0)
            rows=[json.loads(x) for x in (root/'output.jsonl').read_text().splitlines()]
            self.assertEqual(len(rows),2)
            self.assertEqual(rows[0]['result'],'PASS')
            self.assertEqual(rows[1]['required'],1)
            self.assertEqual(rows[1]['framework_acceptance'],'NOT_EVALUATED')
            self.assertEqual(self.invoke(root,as_script=True),2)

    def test_fail_and_missing_coverage_are_distinct(self):
        for value,code in [('FAIL',1),('NOT_RUN',2)]:
            with tempfile.TemporaryDirectory() as d:
                root=self.fixture(d,value)
                self.assertEqual(self.invoke(root,as_script=True),code)
        with tempfile.TemporaryDirectory() as d:
            root=self.fixture(d)
            (root/'evaluation/observations.jsonl').write_text('\n')
            self.assertEqual(self.invoke(root),2)
            self.assertIn('No observation supplied',(root/'output.jsonl').read_text())

    def test_rejects_changed_bundle_source_and_package(self):
        mutations=[('evaluation/cases.json',b'[]'),('source/SKILL.md',b'changed'),('source-manifest.json',None)]
        for name,data in mutations:
            with tempfile.TemporaryDirectory() as d:
                root=self.fixture(d)
                if data is None:
                    value=json.loads((root/name).read_text());value['package_digest']='0'*64;data=json.dumps(value).encode()
                (root/name).write_bytes(data)
                with self.assertRaises(ValueError): self.invoke(root)

    def test_rejects_observation_shape_basis_and_evidence(self):
        for variant in ['shape','reason','method','missing','changed','duplicate']:
            with tempfile.TemporaryDirectory() as d:
                root=self.fixture(d)
                path=root/'evaluation/observations.jsonl';v=json.loads(path.read_text())
                if variant=='shape':v['extra']=True
                elif variant=='reason':v['reason']=''
                elif variant=='method':v['method']='guessed'
                elif variant=='missing':v['evidence']=[]
                elif variant=='changed':v['evidence'][0]['sha256']='0'*64
                text=json.dumps(v)+'\n'
                path.write_text(text*2 if variant=='duplicate' else text)
                with self.assertRaises(ValueError):self.invoke(root)

    def test_strict_json(self):
        for text in ['{"a":1,"a":2}','{"a":NaN}']:
            with tempfile.TemporaryDirectory() as d:
                p=Path(d)/'bad.json';p.write_text(text)
                with self.assertRaises(ValueError):run_evaluation.read(p)

if __name__=='__main__':unittest.main()
