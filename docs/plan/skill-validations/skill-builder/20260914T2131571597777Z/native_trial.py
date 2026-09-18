"""Bounded cold CLI trials; parent owns process-tree timeout recovery."""
import datetime as dt
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from prepare_validation import ROOT, put, sha

case=sys.argv[1]
folder=ROOT/'trials'/(case + (('-' + sys.argv[2]) if len(sys.argv)>2 else ''))
folder.mkdir(parents=True,exist_ok=False)
project=folder/('Project café space' if case=='native-simple' else 'Another layout Ω')
project.mkdir()
package=project/'builder-source'/'skill-builder'
shutil.copytree(ROOT/'source',package)
(project/'.trial-output').mkdir()
if case=='native-simple':
    name='sort-lines'
    destination=project/'custom skills'/name
    task='Create a skill named sort-lines. It takes newline-separated text supplied in the user message, removes empty lines, sorts the remaining lines by Unicode code-point order, retains duplicate lines, and returns only the sorted lines. It does not read or write runtime files. No helper is needed. '
else:
    name='count-lines'
    destination=project/'tools'/'skills'/name
    task='Create a skill named count-lines. On a user-selected UTF-8 input file and literal output directory, support two modes: count writes count.json with {"nonempty_lines": integer}; list writes lines.txt containing nonempty lines in original order, retaining duplicates and writing LF separators. Do not load count-specific instructions for list or list-specific instructions for count. Create and read back the selected output. Never modify the input. Missing input or invalid UTF-8 must write and read back failure.json containing {"status":"FAILED","reason":string,"input":string} in the selected output directory; report incomplete delivery if that report cannot be written. Refuse to overwrite an existing result or failure.json and report the conflict. For interruption retain already-written artifacts and check them before any user-authorized retry; do not claim killed-process cleanup. A small deterministic helper is appropriate if it avoids repeating decoding/filtering/output-safety operations across the modes. '
prompt=f'Use the skill-builder instructions at {package / "SKILL.md"}. {task}Save the development package at {destination}. The selected project is {project}. Authoring and custody writes are authorized only inside this synthetic project. No installation, networking, external messaging or writes outside this project. Finish the authorized authoring workflow and return its artifacts.'
(folder/'prompt.txt').write_text(prompt,encoding='utf-8')
argv=[shutil.which('codex'),'exec','--cd',str(project),'--sandbox','workspace-write','--skip-git-repo-check','--json','--output-last-message',str(project/'.trial-output/final.txt'),'-']
def inventory():
    return [{'path':p.relative_to(project).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(project.rglob('*')) if p.is_file() and not p.is_symlink()]
put(folder/'plan.json',dict(schema_version='1',case_id=case,requirement_ids=['SBPV-01','SBPV-02','SBPV-03','SBPV-05','SBPV-06','SBPV-18'],fixture_refs=[{'path':str(folder/'prompt.txt'),'sha256':sha(folder/'prompt.txt')}],expected_outputs=['Design before staging, exact bound capture, authored skill at selected destination, manual validator handoff; no candidate execution by builder.'],expected_effects='Only this synthetic project; builder-source remains byte-identical.',executor='Installed Codex CLI, inherited existing model/config/auth; explicit source load not implicit discovery',command=argv,timeout_seconds=120,permitted_write_root=str(project),retry_policy='No automatic retry. Timeout leaves native scenario incomplete.'))
put(folder/'before.json',inventory())
started=dt.datetime.now(dt.timezone.utc).isoformat()
start=time.monotonic()
with (folder/'stdout.jsonl').open('xb') as out, (folder/'stderr.txt').open('xb') as err:
    proc=subprocess.Popen(argv,stdin=subprocess.PIPE,stdout=out,stderr=err,cwd=project)
    timeout=False
    recovery=None
    try:
        proc.communicate(prompt.encode('utf-8'),timeout=120)
    except subprocess.TimeoutExpired:
        timeout=True
        recovery=subprocess.run(['taskkill','/PID',str(proc.pid),'/T','/F'],capture_output=True,timeout=15)
        (folder/'recovery.stdout.txt').write_bytes(recovery.stdout)
        (folder/'recovery.stderr.txt').write_bytes(recovery.stderr)
        proc.wait(timeout=15)
put(folder/'after.json',inventory())
put(folder/'attempt-001.json',dict(command=argv,cwd=str(project),pid=proc.pid,started_at_utc=started,ended_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-start,exit_code=proc.returncode,timed_out=timeout,parent_recovery_exit=None if recovery is None else recovery.returncode,unfinished='Inspect actual artifacts before dependent generated-skill execution.'))
print(json.dumps({'case':case,'exit':proc.returncode,'timeout':timeout,'destination_exists':destination.exists()}))
