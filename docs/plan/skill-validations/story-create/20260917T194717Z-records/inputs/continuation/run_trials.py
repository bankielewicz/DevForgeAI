"""Execute selected sealed native attempts with retained independent receipts."""
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys

RUN=Path(__file__).resolve().parent
HELPER=RUN.parents[4]/'.agents/skills/skill-validator/scripts/trial_runner.py'

def execute(ident):
    if ident not in {'N02','N03','N04','N05','N10','N12','N13','G01','G02','G03'}:raise ValueError('Unselected case')
    case=RUN/'trials'/ident
    attempt=case/('attempt-002' if ident.startswith('N') and ident!='N13' else 'attempt-001')
    for action,args in [('seal',['--plan',str(case/'plan.json'),'--attempt',str(attempt)]),('run',['--attempt',str(attempt)]),('check',['--attempt',str(attempt)])]:
        argv=[sys.executable,'-B','-X','utf8',str(HELPER),action,*args]
        result=subprocess.run(argv,capture_output=True)
        for name,data in [('stdout',result.stdout),('stderr',result.stderr)]:
            with (case/(action+'.'+name+'.txt')).open('xb') as stream:stream.write(data)
        with (case/(action+'.execution.json')).open('x',encoding='utf-8') as stream:json.dump({'argv':argv,'exit_code':result.returncode},stream,indent=2)
        if action=='seal' and result.returncode:return {'case_id':ident,'status':'SEAL_ERROR','exit_code':result.returncode}
    value=json.loads((attempt/'result.json').read_bytes())
    return {k:value[k] for k in ['case_id','outcome','elapsed_seconds','timeout','cleanup','input_unchanged']}

if __name__=='__main__':
    cases=sys.argv[1:]
    if not cases or len(cases)!=len(set(cases)):raise SystemExit('Select unique prepared cases')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures={pool.submit(execute,case):case for case in cases}
        for future in concurrent.futures.as_completed(futures):print(json.dumps(future.result()),flush=True)
