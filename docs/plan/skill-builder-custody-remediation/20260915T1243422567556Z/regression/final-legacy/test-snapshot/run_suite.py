"""Executed-case evidence and all-source coverage; no acceptance authority."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
import unittest
import coverage

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[4]
PACKAGE = ROOT/'src/agents/skills/skill-builder'
parser=argparse.ArgumentParser()
parser.add_argument('attempt')
parser.add_argument('--modules', nargs='+')
args=parser.parse_args()
OUT=RUN/args.attempt
OUT.mkdir(exist_ok=False)
os.environ['REMEDIATION_ATTEMPT']=args.attempt
os.environ['ADAPTIVE_TEST_ROOT']=str(OUT/'adaptive-fixtures')
os.environ['AUTHORING_BUILDER_ROOT']=str(PACKAGE)
sys.path.insert(0,str(RUN))
sys.path.append(str(ROOT/'src/agents/skills/skill-validator/tests'))
os.environ['BUILDER_REVIEW_PROJECT']=str(ROOT)
os.environ['BUILDER_REVIEW_EVIDENCE']=str(OUT)
def dump(path,value): path.write_text(json.dumps(value,indent=2),encoding='utf-8')
def manifest(root): return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
source=manifest(PACKAGE)
tests={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in RUN.glob('*.py')}
(OUT/'test-snapshot').mkdir()
for p in RUN.glob('*.py'):(OUT/'test-snapshot'/p.name).write_bytes(p.read_bytes())
fixtures=ROOT/'src/agents/skills/skill-validator/tests'
dependencies={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [*(fixtures/n for n in ('fixture_data.py','adoption_fixture.py')),*(ROOT/'src/agents/skills/skill-validator/scripts').glob('*.py')]}
dump(OUT/'scope.json',{'denominator':'Every executable statement in every shipped first-party Python file including unimported modules and runtime asset. No exclusions. Branches separately.','files':list(str(p.relative_to(PACKAGE)) for p in PACKAGE.rglob('*.py')),'line_floor':95,'pass_floor':95,'platform':'Windows','source':source,'tests':tests,'readonly_fixture_dependencies':dependencies})
dump(OUT/'runtime.json',{'python':sys.version,'executable':sys.executable,'platform':platform.platform(),'cwd':str(Path.cwd()),'argv':sys.argv,'coverage':coverage.__version__})
cov=coverage.Coverage(data_file=str(OUT/'coverage-data'),source=[str(PACKAGE)],branch=True)
cov.set_option('report:exclude_lines',[])
cov.start()
# Instrument genuine Python CLI subprocesses without replacing their behavior.
real_run=subprocess.run
def measured(command,*positional,**kw):
    command=list(command) if isinstance(command,(list,tuple)) else command
    if isinstance(command,list) and command and str(command[0])==sys.executable:
        for i,item in enumerate(command[1:],1):
            path=Path(str(item))
            if path.suffix=='.py' and path.is_absolute() and path.is_relative_to(PACKAGE):
                command=command[:i]+['-m','coverage','run','--append','--branch','--data-file='+str(OUT/'coverage-cli'),'--source='+str(PACKAGE),str(RUN/'coverage_driver.py')]+command[i:]
                break
    return real_run(command,*positional,**kw)
subprocess.run=measured
modules=args.modules or ['test_remediation','test_legacy_maintenance','test_acceptance_edges','test_final_contract_edges','test_design','test_authoring','test_authoring_safeguards','test_builder_adaptive','test_runtime_original']
suite=unittest.defaultTestLoader.loadTestsFromNames(modules)
def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite):yield from flatten(item)
        else:yield item.id()
ids=list(flatten(suite))
dump(OUT/'expected.json',{i:'PASS' for i in ids})
class Result(unittest.TextTestResult):
    def startTest(self,test): self.start=time.monotonic();self.status='PASS';self.details=[];super().startTest(test)
    def addFailure(self,test,err):self.status='FAIL';self.details.append(self._exc_info_to_string(err,test));super().addFailure(test,err)
    def addError(self,test,err):self.status='ERROR';self.details.append(self._exc_info_to_string(err,test));super().addError(test,err)
    def addSkip(self,test,reason):self.status='SKIP';self.details.append(reason);super().addSkip(test,reason)
    def addSubTest(self,test,subtest,err):
        if err:self.status='FAIL';self.details.append(self._exc_info_to_string(err,subtest))
        super().addSubTest(test,subtest,err)
    def stopTest(self,test):
        rows.append({'case':test.id(),'status':self.status,'seconds':time.monotonic()-self.start,'detail':'\n'.join(self.details)})
        stream.write(json.dumps(rows[-1])+'\n');stream.flush();super().stopTest(test)
rows=[]
with (OUT/'results.jsonl').open('x',encoding='utf-8') as stream:
    result=unittest.TextTestRunner(resultclass=Result,verbosity=2).run(suite)
cov.stop();cov.save()
if (OUT/'coverage-cli').exists():cov.combine([str(OUT/'coverage-cli')],keep=True);cov.save()
# Ensure coverage includes runtime assets that coverage.py directory discovery omits.
cov.get_data().touch_files([str(p.resolve()) for p in PACKAGE.rglob('*.py')])
cov.save();cov.json_report(outfile=str(OUT/'coverage.json'))
report=json.loads((OUT/'coverage.json').read_text())
s=report['totals'];passed=sum(r['status']=='PASS' for r in rows)
grade={'required':len(ids),'observed':len(rows),'passed':passed,'pass_rate':100*passed/len(ids),'covered_lines':s['covered_lines'],'statements':s['num_statements'],'line_percent':100*s['covered_lines']/s['num_statements'],'covered_branches':s['covered_branches'],'branches':s['num_branches'],'source_unchanged':source==manifest(PACKAGE),'duplicate_cases':len(rows)!=len({r['case'] for r in rows}),'nonpasses':[r['case'] for r in rows if r['status']!='PASS']}
dump(OUT/'grade.json',grade)
print(json.dumps(grade))
sys.exit(0 if result.wasSuccessful() and grade['source_unchanged'] else 1)
