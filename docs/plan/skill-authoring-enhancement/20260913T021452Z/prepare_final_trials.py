from pathlib import Path
import hashlib
import json
import shutil
RUN = Path(__file__).resolve().parent
T = RUN / 'independent-trials'
case = T / 'enhanced-validator'
case.mkdir()
shutil.copytree(RUN / 'candidate/skill-validator', case / 'skill-validator')
project = T / 'import-script/project'
packet = next((project / 'docs/plan').rglob('validation-request.json'))
prompt = f'''Use $skill-validator at {case / 'skill-validator/SKILL.md'} to validate and test the skill named by this manual authoring packet: {packet}.
Selected packet SHA-256: {hashlib.sha256(packet.read_bytes()).hexdigest()}.
Project root: {project}.
Use synthetic disposable inputs under a fresh project docs/plan validation run. Exercise its supplied CSV decimal total helper for normal and invalid amount input. Do not change the target, install dependencies, contact services or invoke builder. No delegation. Preserve the packet, exact selected implementation, input fixtures, commands, outputs, checks and report. Keep actual script execution separate from native skill activation and model behavior. Save your final response to {case / 'response.md'} and tool trace to {case / 'trace.md'}. Read no sibling task plans or previous assessment conclusions.
'''
(case / 'prompt.txt').write_text(prompt)
(case / 'plan.json').write_text(json.dumps({'case_ids':['AC-11','AC-14'],'expected':'Independent current-byte intake then validator-owned structural and positive/negative generated-script tests; exact-byte separate assessment records, no builder call','executor':'independent agent following enhanced development validator snapshot','timeout_seconds':900,'write_root':str(project / 'docs/plan')},indent=2))
case = T / 'untested-revision'
case.mkdir()
shutil.copytree(RUN / 'candidate/skill-builder', case / 'skill-builder')
project = T / 'observed-edit/project'
target = project / 'Development skills/daily-brief'
prompt = f'''Use $skill-builder at {case / 'skill-builder/SKILL.md'}.
Make another focused change to {target} in project {project}: for an open question that the notes explicitly assign to an owner, include that owner in the brief. Do not infer missing owners. Preserve the rest of its behavior, metadata and resources. The previous authoring run is retained under this project's docs/plan/skill-authorings; it has not been validated or tested. This request authorizes the edit now.
Do not install anything or contact external services. Writes are limited to this project and {case / 'response.md'} and {case / 'trace.md'}. Retain the response and exact commands/outcomes there. Read no sibling plans or conclusions. No delegation.
'''
(case / 'prompt.txt').write_text(prompt)
(case / 'plan.json').write_text(json.dumps({'case_ids':['AC-06','AC-10'],'expected':'Revision from verified prior authoring baseline without quality prerequisite, preserved unrelated bytes and old records; new NOT_PERFORMED statuses and manual packet','executor':'independent agent','timeout_seconds':600,'write_root':str(project)},indent=2))
shutil.copytree(target, case / 'input-target')
print('Prepared fresh validator and untested-revision inputs.')
