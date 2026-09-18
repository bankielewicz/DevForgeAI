"""Cold explicit validator task over a tiny synthetic standalone skill."""
import datetime as dt
import json
from pathlib import Path
import shutil
import subprocess
from capture import ROOT, RUN, scan

attempt = len(list((RUN/'native-trials').glob('validator-attempt-*')))+1
project = RUN/('native-trials/validator-project-'+str(attempt).zfill(3))
project.mkdir()
(project/'.trial-output').mkdir()
target = project/'src/skills/card-summary'
target.mkdir(parents=True)
(target/'SKILL.md').write_text('---\nname: card-summary\ndescription: Summarize a supplied local requirement as one JSON task card.\n---\nRead the user-selected UTF-8 requirement. Return JSON with requirement and verification nonempty string fields. On missing input, report the missing path and produce no card. Do not modify inputs, write files, install tools or use network. Completion is delivery of the JSON in the response.\n',encoding='utf-8')
(project/'spec.md').write_text('# Selected card-summary contract\nRead one user-selected UTF-8 requirement and return a JSON object with exactly requirement and verification, both nonempty strings. Missing input is reported without a card. No file writes, dependencies or network effects are part of the target workflow.\n',encoding='utf-8')
(project/'AGENTS.md').write_text('Synthetic assessment workspace. Use local terminal tools only; no network, connectors, credentials, installation, or writes outside this project. Target and spec are read-only. Validator evidence may be written under docs/plan/. This explicit current request selects the supplied specification.\n',encoding='utf-8')
skill = project/'validator-source/skill-validator'
shutil.copytree(ROOT/'src/agents/skills/skill-validator',skill)
folder = RUN/('native-trials/validator-attempt-'+str(attempt).zfill(3))
folder.mkdir()
prompt = 'Use $skill-validator at '+str(skill/'SKILL.md')+' to assess '+str(target)+' against '+str(project/'spec.md')+'. Write the standalone assessment evidence and report under this disposable project docs/plan. Do not repair the target. Use local terminal observations and manual review; no network, connectors, credential access, dependency installation or additional writable roots. Report actual coverage and limitations.'
argv = [shutil.which('codex'),'exec','--cd',str(project),'--sandbox','workspace-write','--skip-git-repo-check','--json','--output-last-message',str(project/'.trial-output/final.txt'),'-']
plan = {'argv':argv,'prompt':prompt,'timeout_seconds':120,'expected':{'target_unchanged':True,'ordinary_adaptive_metadata':'not required','specification':'explicit existing source','outputs':'actual report/evidence with honest status; no automatic repair'},'before':scan(project),'validator_manifest':scan(skill),'start':dt.datetime.now(dt.timezone.utc).isoformat()}
(folder/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
with (folder/'stdout.jsonl').open('wb') as out,(folder/'stderr.txt').open('wb') as err:
    process = subprocess.Popen(argv,cwd=project,stdin=subprocess.PIPE,stdout=out,stderr=err)
    try:
        process.communicate(prompt.encode(),timeout=120)
        code,termination = process.returncode,'exited'
    except subprocess.TimeoutExpired:
        result = subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],stdout=err,stderr=err,timeout=15)
        if result.returncode:
            process.kill()
        process.wait(timeout=15)
        code,termination = None,'timeout-tree-terminated' if result.returncode==0 else 'timeout-parent-killed-tree-unverified'
(folder/'result.json').write_text(json.dumps({'exit_code':code,'termination':termination,'after':scan(project),'end':dt.datetime.now(dt.timezone.utc).isoformat()},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'exit_code':code,'termination':termination,'evidence':str(folder)}))
