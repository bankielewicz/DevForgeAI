"""Retained adaptive cases; snapshot identity and a disjoint trial namespace."""
import importlib.util
import json
import os
from pathlib import Path
import sys
import unittest
from prepare_validation import ROOT,PROJECT,put,sha
out=ROOT/'observations/adaptive-regressions'
out.mkdir(parents=True,exist_ok=False)
original=PROJECT/'docs/plan/skill-builder-postmvp-maintenance/20260914T2108252255451Z/test_builder_adaptive.py'
raw=original.read_text(encoding='utf-8')
(out/'original-test.txt').write_bytes(original.read_bytes())
raw=raw.replace("PROJECT = RUN.parents[3]", "PROJECT = Path("+repr(str(PROJECT))+")").replace("BUILDER = PROJECT / 'src/agents/skills/skill-builder'", "BUILDER = Path("+repr(str(ROOT/'source'))+")")
test=out/'test_adaptive_retained.py'; test.write_text(raw,encoding='utf-8')
put(out/'builder-before.json',json.loads((ROOT/'source-manifest.json').read_bytes()))
os.environ['ADAPTIVE_TEST_ROOT']=str(ROOT/'trials/adaptive-regressions')
spec=importlib.util.spec_from_file_location('adaptive_retained',test)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
suite=unittest.defaultTestLoader.loadTestsFromModule(module)
def flatten(s):
    for t in s:
        if isinstance(t,unittest.TestSuite): yield from flatten(t)
        else: yield t.id()
put(out/'plan.json',{'expected':{name:'PASS' for name in flatten(suite)},'original_sha256':sha(original),'executed_sha256':sha(test),'adaptation':'Only project and source constants plus new snapshot/readback baseline; assertions preserved. No historical pre-maintenance equivalence claimed.','timeout_seconds':120})
rows=[]
class R(unittest.TextTestResult):
    def emit(self,t,s,detail=''):
        rows.append({'case_id':t.id(),'result':s,'detail':detail})
        with (out/'results.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(rows[-1],ensure_ascii=False)+'\n')
    def addSuccess(self,t):super().addSuccess(t);self.emit(t,'PASS')
    def addFailure(self,t,e):super().addFailure(t,e);self.emit(t,'FAIL',self._exc_info_to_string(e,t))
    def addError(self,t,e):super().addError(t,e);self.emit(t,'ERROR',self._exc_info_to_string(e,t))
    def addSkip(self,t,r):super().addSkip(t,r);self.emit(t,'NOT_RUN',r)
with (out/'stdout.txt').open('w',encoding='utf-8') as stream:result=unittest.TextTestRunner(stream=stream,resultclass=R,verbosity=2).run(suite)
put(out/'grade.json',{'required':result.testsRun,'passing':sum(r['result']=='PASS' for r in rows),'nonpasses':[r for r in rows if r['result']!='PASS']})
print(json.dumps({'required':result.testsRun,'passing':sum(r['result']=='PASS' for r in rows),'nonpasses':[r['case_id'] for r in rows if r['result']!='PASS']}))
sys.exit(0 if result.wasSuccessful() else 1)
