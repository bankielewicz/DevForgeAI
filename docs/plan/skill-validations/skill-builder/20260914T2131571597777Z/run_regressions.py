"""Retained regression cases against captured source; fresh retained fixture roots."""
import contextlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import time
import unittest
from prepare_validation import ROOT,PROJECT,put,sha
import coverage
out=ROOT/'observations/regressions'
out.mkdir(parents=True,exist_ok=False)
inputs=ROOT/'inputs/regressions'
inputs.mkdir(parents=True,exist_ok=False)
origin=PROJECT/'src/agents/skills/skill-validator/tests'
for name in ['test_authoring.py','test_authoring_safeguards.py','fixture_data.py','adoption_fixture.py']:
    shutil.copyfile(origin/name,inputs/name)
put(out/'input-manifest.json',[{'original':str(origin/p.name),'snapshot':str(p),'sha256':sha(p)} for p in inputs.iterdir()])
os.environ['AUTHORING_BUILDER_ROOT']=str(ROOT/'source')
sys.path.insert(0,str(inputs)); sys.path.insert(0,str(PROJECT/'.agents/skills/skill-validator/scripts'))
cov=coverage.Coverage(data_file=str(out/'.coverage'),source=[str(ROOT/'source/scripts'),str(ROOT/'source/assets/adaptive-runtime')],branch=True)
cov.start()
import test_authoring
import test_authoring_safeguards
import fixture_data
fixture_data.PACKAGE=PROJECT/'src/agents/skills/skill-validator'
def setup(self):
    self.project=ROOT/'trials/regressions'/self.__class__.__name__/self._testMethodName
    self.project.mkdir(parents=True,exist_ok=False)
    self.target=self.project/'Custom skills with spaces/brief-note'
    self.counter=0
test_authoring.AuthoringTests.setUp=setup
test_authoring_safeguards.AuthoringSafeguards.setUp=setup
suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromModule(test_authoring),unittest.defaultTestLoader.loadTestsFromModule(test_authoring_safeguards)])
def cases(s):
    for t in s:
        if isinstance(t,unittest.TestSuite): yield from cases(t)
        else: yield t.id()
put(out/'expected.json',{name:'PASS' for name in cases(suite)})
put(out/'adaptation.json',dict(changes=['BUILDER resolved through supported AUTHORING_BUILDER_ROOT to retained source','fixture_data.PACKAGE points to original validator schemas/resources','setUp writes fresh per-case retained directories instead of TemporaryDirectory; no cleanup'],assertions='Unchanged',timeout_seconds=120))
rows=[]
class R(unittest.TextTestResult):
    def emit(self,t,s,detail=''):
        rows.append({'case_id':t.id(),'result':s,'detail':detail})
        with (out/'results.jsonl').open('a',encoding='utf-8') as f: f.write(json.dumps(rows[-1],ensure_ascii=False)+'\n')
    def addSuccess(self,t): super().addSuccess(t); self.emit(t,'PASS')
    def addFailure(self,t,e): super().addFailure(t,e); self.emit(t,'FAIL',self._exc_info_to_string(e,t))
    def addError(self,t,e): super().addError(t,e); self.emit(t,'ERROR',self._exc_info_to_string(e,t))
    def addSkip(self,t,r): super().addSkip(t,r); self.emit(t,'NOT_RUN',r)
with (out/'stdout.txt').open('w',encoding='utf-8') as stream:
    result=unittest.TextTestRunner(stream=stream,resultclass=R,verbosity=2).run(suite)
cov.stop(); cov.save(); cov.json_report(outfile=str(out/'coverage.json'))
grade=dict(required=len(json.loads((out/'expected.json').read_bytes())) ,passed=sum(r['result']=='PASS' for r in rows),nonpasses=[r for r in rows if r['result']!='PASS'])
put(out/'grade.json',grade)
print(json.dumps(grade))
sys.exit(0 if result.wasSuccessful() else 1)
