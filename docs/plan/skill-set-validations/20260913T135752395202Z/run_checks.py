"""Retain each read-only/test command as a fresh bounded attempt."""
import argparse
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
VALIDATOR = ROOT/'.agents/skills/skill-validator'
BUILDER = ROOT/'src/agents/skills/skill-builder'

def execute(label, command, expected='observation'):
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    attempt = RUN/'attempts'/(stamp+'-'+label)
    attempt.mkdir(parents=True)
    temp = attempt/'temp'
    temp.mkdir()
    env = os.environ.copy()
    env.update(TMP=str(temp),TEMP=str(temp),TMPDIR=str(temp),PYTHONDONTWRITEBYTECODE='1',AUTHORING_BUILDER_ROOT=str(BUILDER))
    plan = {'schema_version':'1','label':label,'command':command,'expected':expected,'timeout_seconds':120,'permitted_write_root':str(attempt),'started_at_utc':stamp}
    (attempt/'plan.json').write_text(json.dumps(plan,indent=2))
    try:
        result = subprocess.run(command,cwd=ROOT,env=env,capture_output=True,timeout=120)
        stdout,stderr=result.stdout,result.stderr
        plan.update(exit_code=result.returncode,timed_out=False)
    except subprocess.TimeoutExpired as exc:
        stdout,stderr=exc.stdout or b'',exc.stderr or b''
        plan.update(exit_code=None,timed_out=True)
    (attempt/'stdout.txt').write_bytes(stdout)
    (attempt/'stderr.txt').write_bytes(stderr)
    plan['ended_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (attempt/'receipt.json').write_text(json.dumps(plan,indent=2))
    print(str(attempt),plan.get('exit_code'),plan['timed_out'])
    print(stderr.decode('utf-8',errors='replace')[-1400:])
    return attempt,plan

if __name__=='__main__':
    mode=sys.argv[1]
    py=[sys.executable,'-B','-X','utf8']
    if mode=='unit':
        execute(mode,py+['-m','unittest','discover','-s',str(VALIDATOR/'tests'),'-v'],'All applicable existing regression assertions pass.')
    elif mode in ('structure','package','quick'):
        for name,target in [('validator',VALIDATOR),('builder',BUILDER)]:
            if mode=='quick':
                command=py+[r'C:\Users\bryan\.codex\skills\.system\skill-creator\scripts\quick_validate.py',str(target)]
            else:
                command=py+[str(VALIDATOR/'scripts'/('observe.py' if mode=='structure' else 'adaptive_observe.py')),mode,'--source',str(target)]
            execute(mode+'-'+name,command,'Limited raw structural/text observation; unresolved semantics remain visible.')
    elif mode=='host':
        execute('version',['codex','--version'])
        execute('cli-help',['codex','exec','--help'])
