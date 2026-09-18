"""Run selected predeclared cold cases once, two at a time, retaining all receipts."""
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys

RUN = Path(__file__).resolve().parent
HELPER = RUN.parents[4] / '.agents/skills/skill-validator/scripts/trial_runner.py'

def execute(ident):
    if ident not in {'N14','N15'}:
        raise ValueError('Unselected case')
    case=RUN/'trials'/ident
    attempt=case/'attempt-001'
    for action, args in [('seal',['--plan',str(case/'plan.json'),'--attempt',str(attempt)]),('run',['--attempt',str(attempt)]),('check',['--attempt',str(attempt)])]:
        argv=[sys.executable,'-B','-X','utf8',str(HELPER),action,*args]
        result=subprocess.run(argv,capture_output=True)
        (case/(action+'.stdout.txt')).write_bytes(result.stdout)
        (case/(action+'.stderr.txt')).write_bytes(result.stderr)
        (case/(action+'.execution.json')).write_text(json.dumps({'argv':argv,'exit_code':result.returncode}),encoding='utf-8')
        if action=='seal' and result.returncode:
            return {'case_id':ident,'state':'SEAL_ERROR','exit_code':result.returncode}
    value=json.loads((attempt/'result.json').read_bytes())
    return {k:value[k] for k in ['case_id','outcome','exit_code','timeout','cleanup','elapsed_seconds']}

if __name__=='__main__':
    cases=sys.argv[1:]
    if not cases or len(cases)!=len(set(cases)):
        raise SystemExit('Select unique predeclared cases')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for value in pool.map(execute,cases):
            print(json.dumps(value),flush=True)
