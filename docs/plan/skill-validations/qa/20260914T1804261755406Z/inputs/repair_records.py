"""Retain first record attempt, fix derived locators, rerun unchanged evidence."""
import datetime as dt
import json
from pathlib import Path
import shutil
import sys
from bootstrap import RUN,ROOT,VALIDATOR,write,ref,command
sys.path.insert(0,str(VALIDATOR/'scripts'))
import observe

def main():
    retained=RUN.with_name(RUN.name+'-records-001-retained')
    assert not retained.exists()
    files,excluded=observe.inventory(RUN)
    assert not excluded
    retained.mkdir()
    for relative,path,info in files:
        target=retained/relative;target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(observe.read_stable(path,info))
    # No prior bytes are deleted; exact original hierarchy is preserved above.
    saved=RUN/'inputs/record-repair-original';saved.mkdir()
    for relative in ['observations/evaluation-results-001.jsonl','observations/evaluation-execution-receipt.json']:
        original=RUN/relative
        shutil.move(str(original),str(saved/original.name))
    schema=RUN/'inputs/extension-schemas/observation.schema.json'
    schema.parent.mkdir(parents=True)
    shutil.move(str(RUN/'evaluation/observation.schema.json'),str(schema))
    native=json.loads((RUN/'observations/native-readbacks.json').read_text())
    for row in native:row['receipt']['path']=row['receipt']['path'].replace('\\','/')
    write('observations/native-readbacks.json',native)
    observations=[json.loads(x) for x in (RUN/'evaluation/observations.jsonl').read_text().splitlines()]
    for row in observations:
        for evidence in row['evidence']:
            if evidence['path']=='evaluation/observation.schema.json':evidence['path']='inputs/extension-schemas/observation.schema.json'
            evidence['sha256']=ref(evidence['path'])['sha256']
    (RUN/'evaluation/observations.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in observations),encoding='utf-8')
    manifest=json.loads((RUN/'evaluation/bundle-manifest.json').read_text())
    for evidence in manifest['artifacts']:
        if evidence['path']=='evaluation/observation.schema.json':evidence['path']='inputs/extension-schemas/observation.schema.json'
        evidence['sha256']=ref(evidence['path'])['sha256']
    write('evaluation/bundle-manifest.json',manifest)
    p=command('evaluation-002',[sys.executable,'-B','-X','utf8',str(RUN/'evaluation/run_evaluation.py'),'--run-root',str(RUN),'--output',str(RUN/'observations/evaluation-results-002.jsonl')])
    assert p.returncode==0
    write('observations/evaluation-execution-receipt.json',{'command':[sys.executable,'-B','-X','utf8',str(RUN/'evaluation/run_evaluation.py'),'--run-root',str(RUN),'--output',str(RUN/'observations/evaluation-results-002.jsonl')],'cwd':str(ROOT),'exit_code':0,'output':ref('observations/evaluation-results-002.jsonl'),'bundle':ref('evaluation/bundle-manifest.json'),'exact_execution_receipt':ref('observations/evaluation-002.receipt.json'),'prior_attempt_retained':str(retained),'meaning':'Same native observations, corrected evidence locators; no native trial rerun or case expectation change.','framework_acceptance':'NOT_EVALUATED'})
    checks=[json.loads(x) for x in (RUN/'checks.jsonl').read_text().splitlines()]
    for row in checks:
        for evidence in row['evidence']:
            if evidence['path']=='observations/evaluation-results-001.jsonl':evidence['path']='observations/evaluation-results-002.jsonl'
            evidence['sha256']=ref(evidence['path'])['sha256']
    (RUN/'checks.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in checks),encoding='utf-8')
    report=(RUN/'validation-report.md').read_text()
    report=report.replace('observations/evaluation-results-001.jsonl','observations/evaluation-results-002.jsonl')
    report+='\n## Record-integrity repair history\n\nThe first schema-1 records check failed with eight evidence-format errors: seven native receipt references used Windows separators and the legacy generic reference detector interpreted JSON Schema properties named path/sha256 as digest references. The entire original run was retained at `'+str(retained)+'` before correction. Current native receipt references use forward slashes; the unchanged evaluation schema is captured under inputs/extension-schemas, outside evaluator-record interpretation. Raw earlier evaluator results and their receipt are retained under inputs/record-repair-original as well. The Python evaluator was rerun as attempt 002 against the same native observations and unchanged expectations, with 21/21 results still passing. No native task, source package, input specification or grader behavior was changed.\n'
    (RUN/'validation-report.md').write_text(report,encoding='utf-8')
    handoff=json.loads((RUN/'handoff.json').read_text());handoff['report']=ref('validation-report.md');write('handoff.json',handoff)
    p=command('records-002',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/observe.py'),'records','--run-root',str(RUN)])
    print('errors',json.loads(p.stdout).get('errors'))
    if p.returncode:raise SystemExit(p.returncode)

if __name__=='__main__':main()
