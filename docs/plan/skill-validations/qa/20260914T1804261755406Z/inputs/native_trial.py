"""One retained native attempt with a 120s process-tree deadline."""
import datetime as dt
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
from bootstrap import RUN, ROOT, write
sys.path.insert(0,str(ROOT/'.agents/skills/skill-validator/scripts'))
import observe

def main():
    case_id = sys.argv[1]
    attempt_id = sys.argv[2] if len(sys.argv)>2 else '001'
    case_root = RUN/'trials'/case_id
    case = json.loads((case_root/'case.json').read_text(encoding='utf-8'))
    budget = RUN/'inputs/native-budget-authorization.json'
    if budget.exists():
        case['timeout_seconds']=json.loads(budget.read_text())['timeout_seconds']
    project = Path(case['project'])
    attempt = case_root/('attempt-'+attempt_id)
    attempt.mkdir(exist_ok=False)
    command = [shutil.which('codex'),'exec','--cd',str(project),'--sandbox','workspace-write','--skip-git-repo-check','--json','--output-last-message',str(project/'.trial-output'/('final-'+attempt_id+'.txt')),'-']
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    receipt = {'case_id':case_id,'attempt_id':attempt_id,'command':command,'cwd':str(project),'started':started,'timeout_seconds':case['timeout_seconds'],'permitted_write_root':str(project),'package_digest':json.loads((RUN/'source-manifest.json').read_text())['package_digest'],'prompt_sha256':observe.sha256((case_root/'prompt.txt').read_bytes()),'case_sha256':observe.sha256((case_root/'case.json').read_bytes()),'budget_authorization_sha256':observe.sha256(budget.read_bytes()) if budget.exists() else None,'state':'STARTED'}
    write(str(attempt.relative_to(RUN)/'before-manifest.json'),observe.make_manifest(project))
    write(str(attempt.relative_to(RUN)/'receipt.json'),receipt)
    with (attempt/'stdout.jsonl').open('wb') as out, (attempt/'stderr.txt').open('wb') as err:
        p = subprocess.Popen(command,cwd=project,stdin=subprocess.PIPE,stdout=out,stderr=err)
        receipt['pid']=p.pid
        try:
            p.communicate((case_root/'prompt.txt').read_bytes(),timeout=case['timeout_seconds'])
            receipt.update(state='EXITED',exit_code=p.returncode)
        except subprocess.TimeoutExpired:
            kill = subprocess.run(['taskkill','/PID',str(p.pid),'/T','/F'],capture_output=True,timeout=15)
            (attempt/'termination.stdout').write_bytes(kill.stdout)
            (attempt/'termination.stderr').write_bytes(kill.stderr)
            receipt.update(state='TIMEOUT',exit_code=None,termination_exit=kill.returncode)
            try: p.wait(timeout=5)
            except subprocess.TimeoutExpired: receipt['process_state']='unresolved after tree termination'
    receipt['ended']=dt.datetime.now(dt.timezone.utc).isoformat()
    write(str(attempt.relative_to(RUN)/'receipt.json'),receipt)
    write(str(attempt.relative_to(RUN)/'after-manifest.json'),observe.make_manifest(project))
    print(json.dumps(receipt))

if __name__ == '__main__': main()
