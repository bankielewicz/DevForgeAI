"""Verify integrity of present member checks when report is missing."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

def main():
    root=Path(__file__).resolve().parent
    case=root/'attempt-04/IR-23'
    case.mkdir(parents=True,exist_ok=False)
    checks=case/'malformed.jsonl'
    checks.write_text('NOT JSON AND NOT A CHECK\n',encoding='utf-8')
    assessment=json.loads((root/'attempt-03/IR-21/set/assessment.json').read_text(encoding='utf-8'))
    assessment['members'][0]['checks']={'path':str(checks),'sha256':hashlib.sha256(checks.read_bytes()).hexdigest()}
    assessment.update(outcome='INCOMPLETE',required_total=29,required_evaluated=0)
    target=case/'set'
    target.mkdir()
    (target/'assessment.json').write_text(json.dumps(assessment,indent=2),encoding='utf-8')
    helper=root.parents[5]/'src/agents/skills/skill-validator/scripts/adaptive_observe.py'
    command=[sys.executable,'-B','-X','utf8',str(helper),'records','--run-root',str(target)]
    result=subprocess.run(command,cwd=case,capture_output=True,timeout=120)
    (case/'stdout.json').write_bytes(result.stdout)
    (case/'stderr.txt').write_bytes(result.stderr)
    (case/'receipt.json').write_text(json.dumps({'command':command,'exit_code':result.returncode,'helper_sha256':hashlib.sha256(helper.read_bytes()).hexdigest()},indent=2),encoding='utf-8')
    print(result.returncode,result.stdout.decode('utf-8'))

if __name__=='__main__':
    main()
