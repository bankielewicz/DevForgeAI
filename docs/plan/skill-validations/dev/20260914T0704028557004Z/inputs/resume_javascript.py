"""One explicitly approved warm delivery continuation; no automatic retry."""
import continue_evaluation as c
from pathlib import Path
import shutil
base=c.RUN/'trials/DV-03-javascript'
project=base/'project'
prompt_path=c.RUN/'inputs/javascript-continuation-prompt.txt'
assert c.h.sha(prompt_path.read_bytes())=='5310ea55230604da954efac4f727274e8b3e047f868bcdb160bd7d3603474b9e'
before=c.h.inventory(project)
assert before['files']==c.load(base/'attempt-002/after.json')['files']
host=c.load(c.RUN/'commands/javascript-host-qa-002/command.json')
assert host['exit_status']==0 and host['termination']=='exited'
assert c.load(c.RUN/'trials/javascript-host-qa/readback-002.json')['unchanged']
c.save(c.RUN/'inputs/javascript-continuation-authorization.json',{
 'user_response':'Authorize the bounded continuation',
 'scope':'One 600-second warm continuation; same thread/model/product; new evidence files only.',
 'proposal_path':str(c.RUN/'inputs/javascript-continuation-proposal.md'),
 'prompt_sha256':c.h.sha(prompt_path.read_bytes()),'recorded_at_utc':c.h.now()})
cmd=[shutil.which('codex'),'exec','--cd',str(project),'--sandbox','workspace-write','resume',
     '01a09ec6-d503-7070-95ee-12d31aebdbac','--skip-git-repo-check','--json','--output-last-message',
     str(project/'.trial-output/final-003.txt'),'-']
c.save(base/'attempt-003/before.json',before)
c.save(base/'attempt-003/plan.json',{'command':cmd,'task_prompt':prompt_path.read_text(encoding='utf-8'),
 'timeout_seconds':600,'permitted_write_root':str(project/'evidence'),'model_override':None,
 'basis':'Approved warm continuation after separately executed exact host QA; original cold record remains PARTIAL.'})
result=c.h.execute('DV-03-javascript-003',cmd,cwd=project,stdin=prompt_path.read_text(encoding='utf-8'),timeout=600)
after=c.h.inventory(project)
old={x['path']:x for x in before['files']};new={x['path']:x for x in after['files']}
changed=[p for p in sorted(old.keys()|new.keys()) if old.get(p)!=new.get(p)]
immutable=[p for p in old if old[p]!=new.get(p)]
unexpected=[p for p in changed if p not in old and not p.startswith(('evidence/','.trial-output/'))]
c.save(base/'attempt-003/after.json',after)
c.save(base/'attempt-003/effects.json',{'changed_paths':changed,'immutable_changes':immutable,
 'unexpected_new_paths':unexpected,'exclusions':after['exclusions'],'command_receipt':str(c.RUN/'commands/DV-03-javascript-003/command.json')})
c.save(base/'attempt-003/result.json',result)
print('WARM_CONTINUATION_FINISHED',result['termination'],result['exit_status'],'IMMUTABLE_CHANGES',immutable,'UNEXPECTED',unexpected)

