"""Native Linux/POSIX custody matrix against same captured checkout; no installs."""
import importlib.util
import json
from pathlib import Path
import platform
import sys
import unittest
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from prepare_validation import put,sha
out=ROOT/'observations/linux-checks'
out.mkdir(parents=True,exist_ok=False)
text=(ROOT/'test_independent_design.py').read_text(encoding='utf-8').replace("ROOT/'trials'/'independent'/", "ROOT/'trials'/'independent-linux'/")
source=out/'test_linux_design.py'
source.write_text(text,encoding='utf-8')
spec=importlib.util.spec_from_file_location('test_linux_design',source)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
suite=unittest.defaultTestLoader.loadTestsFromModule(module)
def flatten(s):
    for t in s:
        if isinstance(t,unittest.TestSuite): yield from flatten(t)
        else: yield t.id()
put(out/'plan.json',{'expected':{name:'PASS' for name in flatten(suite)},'fixture_adaptation':'Only fresh fixture namespace changes; exact source retained. Assertions unchanged.','timeout_seconds':120,'platform':platform.platform(),'python':sys.version,'cwd':str(Path.cwd()),'filesystem':'/mnt/c selected Windows checkout accessed by native Linux tools for bounded platform checks; no checkout relocation','test_sha256':sha(source)})
rows=[]
class Result(unittest.TextTestResult):
    def emit(self,t,s,detail=''):
        rows.append({'case_id':t.id(),'result':s,'detail':detail})
        with (out/'results.jsonl').open('a',encoding='utf-8') as f: f.write(json.dumps(rows[-1],ensure_ascii=False)+'\n')
    def addSuccess(self,t): super().addSuccess(t); self.emit(t,'PASS')
    def addFailure(self,t,e): super().addFailure(t,e); self.emit(t,'FAIL',self._exc_info_to_string(e,t))
    def addError(self,t,e): super().addError(t,e); self.emit(t,'ERROR',self._exc_info_to_string(e,t))
    def addSkip(self,t,r): super().addSkip(t,r); self.emit(t,'NOT_RUN',r)
with (out/'stdout.txt').open('w',encoding='utf-8') as stream:
    result=unittest.TextTestRunner(stream=stream,resultclass=Result,verbosity=2).run(suite)
put(out/'grade.json',{'required':35,'passing':sum(r['result']=='PASS' for r in rows),'nonpasses':[r for r in rows if r['result']!='PASS'],'line_coverage':'NOT_RUN on Linux; Windows measurement is separate'})
print(json.dumps({'required':35,'passing':sum(r['result']=='PASS' for r in rows),'nonpasses':[r['case_id'] for r in rows if r['result']!='PASS']}))
sys.exit(0 if result.wasSuccessful() else 1)
