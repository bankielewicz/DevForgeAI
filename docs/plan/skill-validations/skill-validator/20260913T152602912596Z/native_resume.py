import json
import shutil
from qa_harness import RUN,execute,inventory,save
p=RUN/'trials/native/full-validator'
prior=RUN/'commands/native-full-validator-validator-001/stdout.txt'
events=[json.loads(x) for x in prior.read_text(encoding='utf-8').splitlines() if x.strip()]
thread=next(x['thread_id'] for x in events if x.get('type')=='thread.started')
before=json.loads((RUN/'trials/native/native-full-validator-validator-001-before.json').read_bytes())
now=inventory(p); old={x['path']:x for x in before['files']}; current={x['path']:x for x in now['files']}
selected=[x for x in old if x.startswith('candidate/') or x=='candidate-spec.md' or x.startswith('.agents/skills/skill-validator/')]
assert all(old[x]==current.get(x) for x in selected)
save(RUN/'trials/native/resume-plan.json',{'prior_thread':thread,'prior_attempt':'native-full-validator-validator-001','selected_inputs_unchanged':True,'before':now,'timeout_seconds':120,'expectation':'Preserve prior work and complete remaining assessment if feasible; otherwise retain explicit partial state. No old result promoted to changed bytes.'})
execute('native-resume-001',[shutil.which('codex'),'exec','--sandbox','workspace-write','--cd',str(p),'resume',thread,'--skip-git-repo-check','--json','--output-last-message',str(p/'.trial-output/resume-final.txt'),'-'],cwd=p,stdin='Continue the interrupted ordinary-skill assessment from its retained work. Recheck the selected target and specification identities before resuming; preserve existing evidence and finish remaining observations and the report under the original authorization. No repairs, installation, external services, or builder invocation.')
save(RUN/'trials/native/resume-after.json',inventory(p))
