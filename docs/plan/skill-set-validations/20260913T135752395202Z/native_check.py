"""Bounded cold validator task; existing config/auth and normal child sandbox."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[3]
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
attempt=RUN/'native'/stamp
fixture=attempt/'project'
fixture.mkdir(parents=True)
tool=fixture/'tools/skill-validator'
shutil.copytree(ROOT/'.agents/skills/skill-validator',tool)
(fixture/'.trial-output').mkdir()
request=RUN/'trials-round2/selected-role/records/request/record.json'
prompt='Use $skill-validator at '+str(tool/'SKILL.md')+'. Assess the explicitly selected set request at '+str(request)+'. Determine whether its selected member and delivered skill agree and whether it can proceed to validation. Return the concrete intake observation and a concise evidence-backed explanation. Read the referenced synthetic inputs as needed. This is read-only assessment: do not repair any inputs, invoke builder, install anything or run product operations. Write any evidence only under '+str(fixture)+'.'
command=[shutil.which('codex'),'exec','--cd',str(fixture),'--sandbox','workspace-write','--skip-git-repo-check','--json','--output-last-message',str(fixture/'.trial-output/final.txt'),'-']
plan={'schema_version':'1','case':'C08','command':command,'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),'timeout_seconds':120,'permitted_write_root':str(fixture),'input_sha256':hashlib.sha256(request.read_bytes()).hexdigest(),'expected':'Assess actual selected/delivered agreement; expected labels are absent from cold prompt.','boundary':'Child workspace-write; no OS isolation claim.'}
(attempt/'prompt.txt').write_text(prompt)
(attempt/'plan.json').write_text(json.dumps(plan,indent=2))
before={p.relative_to(fixture).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in fixture.rglob('*') if p.is_file()}
(attempt/'before.json').write_text(json.dumps(before,indent=2))
with (attempt/'stdout.jsonl').open('wb') as stdout,(attempt/'stderr.txt').open('wb') as stderr:
    child=subprocess.Popen(command,cwd=fixture,stdin=subprocess.PIPE,stdout=stdout,stderr=stderr)
    try:
        child.communicate(prompt.encode(),timeout=120)
        plan.update(exit_code=child.returncode,timed_out=False)
    except subprocess.TimeoutExpired:
        cleanup=subprocess.run(['taskkill','/PID',str(child.pid),'/T','/F'],capture_output=True,timeout=15)
        (attempt/'cleanup.txt').write_bytes(cleanup.stdout+cleanup.stderr)
        child.wait(timeout=10)
        plan.update(exit_code=child.returncode,timed_out=True)
plan['ended_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(attempt/'receipt.json').write_text(json.dumps(plan,indent=2))
after={p.relative_to(fixture).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in fixture.rglob('*') if p.is_file()}
(attempt/'after.json').write_text(json.dumps(after,indent=2))
print(str(attempt),plan)
print((attempt/'stderr.txt').read_text(errors='replace')[-1000:])
