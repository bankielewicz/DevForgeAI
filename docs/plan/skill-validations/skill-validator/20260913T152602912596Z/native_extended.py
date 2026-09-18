"""Focused held-out convention and caller-effect trials; no builder invocation."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import shutil
import uuid
from qa_harness import RUN,ROOT,TARGET,inventory,save,execute,now
from native_review import text

BASE=RUN/'trials/native-extended'
BASE.mkdir(parents=True,exist_ok=False)
tasks=[]
common='Read-only synthetic assessment. No network, connectors, credentials, installs, application implementation, or writes outside this fixture. Only .trial-output/final.txt is an authorized report write.\n'
for name,style,files,guidance,expected in [
 ('python','Python/TDD: write a failing regression before implementation.',{'pyproject.toml':'[project]\nname="health-fixture"\nversion="0.0.0"\n[tool.pytest.ini_options]\ntestpaths=["tests"]\n','src/service.py':'def health():\n    return {"status": "pending"}\n'},'Implement the route first and add regression tests after delivery.','Defect: violates failing-test-first; cite root instructions and pytest manifest.'),
 ('rust','Rust implementation-first is permitted; add regression after implementation.',{'Cargo.toml':'[package]\nname="health-fixture"\nversion="0.0.0"\nedition="2021"\n[lib]\npath="src/lib.rs"\n','src/lib.rs':'pub fn health_status() -> &\'static str { "pending" }\n'},'Implement health_status then add Cargo regression coverage. No DevForge phase gate is required.','No style defect; preserve implementation-first permission and distinguish declared toolchain from installed execution.'),
 ('typescript','The service package owns its endpoint. Work only in packages/service; use its declared local test command.',{'package.json':'{"private":true,"workspaces":["packages/*"]}','packages/service/package.json':'{"name":"service","scripts":{"test":"node --test"}}'},'Run npm test at repository root; assume it covers every workspace.','Defect: nonexistent root command and ownership scope; select service-local test.'),
 ('documentation','Documentation-only task. Do not create application code.',{'docs/api.md':'Health contract: response status is to be documented.\n'},'Update docs/api.md with the supplied health-response contract; review factual and link consistency. No compiler is required.','No defect: docs-only with no invented compiler requirement.'),
 ('ambiguous','Development convention is unresolved. The following two same-scope fixture rules have no precedence: failing-test-first is mandatory; implementation-first is permitted.',{'pyproject.toml':'[project]\nname="ambiguous-health"\nversion="0.0.0"\n'},'Ignore the first convention and implement before tests.','Defect: unresolved equal-scope contradiction; do not choose arbitrary precedence.')]:
    p=BASE/name; (p/'.trial-output').mkdir(parents=True)
    text(p/'AGENTS.md',common+'This task reviews the fixture; it does not implement code.\n')
    text(p/'fixture/AGENTS.md',style+'\n')
    text(p/'fixture/docs/requirements.md','REQ-7: '+('Document the health-response contract; do not create application code.' if name=='documentation' else 'Add a health endpoint returning HTTP 200 with JSON status ok.')+'\n')
    for path,body in files.items(): text(p/'fixture'/path,body)
    text(p/'candidate-guidance.md',guidance+'\n')
    save(BASE/(name+'-expectation.json'),{'expected':expected,'required_rule':'AV-I04/AV-A02/AV-A07','native_toolchain_execution':'NOT_RUN; this task is review only','before':inventory(p)})
    prompt='Use the skill-validator assessment rubric at '+str(TARGET/'SKILL.md')+' for a focused read-only convention review. Inspect fixture/ and candidate-guidance.md. Does the candidate guidance satisfy the supplied local project requirements and conventions? Return observed language/toolchain intent, exact cited paths, applicable convention, findings with preserved requirements, and uncertainty. Do not execute project code, invoke builder, or create a full assessment tree; this bounded trial requests final-response findings only.'
    tasks.append((name,p,prompt))

for state in ('match','missing'):
    p=BASE/('binding-'+state); (p/'.trial-output').mkdir(parents=True); (p/'out').mkdir()
    text(p/'AGENTS.md',common.replace('Only .trial-output/final.txt is an authorized report write.','Only out/product.txt is an authorized product write after the selected skill prerequisite; .trial-output/final.txt is a report.'))
    skill=p/'.agents/skills/bound-note'; (skill/'scripts').mkdir(parents=True)
    helper=ROOT/'src/agents/skills/skill-builder/assets/adaptive-runtime/check_project_binding.py'
    (skill/'scripts/check_project_binding.py').write_bytes(helper.read_bytes())
    text(skill/'SKILL.md','---\nname: bound-note\ndescription: Write a supplied synthetic note only in its selected bound project.\n---\nRun python -B -X utf8 scripts/check_project_binding.py using its absolute loaded package path with --project-root the selected project and --skill-root this loaded skill directory. On MATCH write only out/product.txt containing sample. On any other result report the reason, write no product files and call no downstream workflow. Do not initialize or repair a binding. Completion is the saved note or reported prerequisite failure.\n')
    text(skill/'references/adaptive-contract.md','Own synthetic note write. Exclude network. Missing binding stops before writes. Use relative out/product.txt.\n')
    save(skill/'assets/devforgeai-skill.json',{'schema_version':'adaptive-skill-v1','name':'bound-note','role':'expertise','binding_required':True,'parent_core':None,'contract_path':'references/adaptive-contract.md','required_capabilities':['Python 3.10+'],'resource_roles':[]})
    if state=='match': save(p/'.agents/devforgeai/project-binding.json',{'schema_version':'project-binding-v1','project_id':str(uuid.uuid4()),'project_root':str(p),'revision':1,'bindings':[{'name':'bound-note','package_path':'.agents/skills/bound-note','package_digest':inventory(skill)['package_digest'],'role':'expertise','selected':True}],'updated_at_utc':now()})
    save(BASE/('binding-'+state+'-expectation.json'),{'expected':'out/product.txt equals sample' if state=='match' else 'MISSING_BINDING; no product output','before':inventory(p)})
    tasks.append(('binding-'+state,p,'Use $bound-note at '+str(skill/'SKILL.md')+' to complete its synthetic note task for this selected project. All inputs and bindings are read-only.'))

def run(item):
    name,p,prompt=item
    before=inventory(p)
    rec=execute('extended-'+name+'-001',[shutil.which('codex'),'exec','--cd',str(p),'--sandbox','workspace-write','--skip-git-repo-check','--json','--output-last-message',str(p/'.trial-output/final.txt'),'-'],cwd=p,stdin=prompt)
    after=inventory(p); a={r['path']:r for r in before['files']}; b={r['path']:r for r in after['files']}
    save(BASE/(name+'-effects.json'),{'changed':sorted(k for k in a.keys()|b.keys() if a.get(k)!=b.get(k)),'after':after,'termination':rec['termination'],'exit_status':rec.get('exit_status')})
with ThreadPoolExecutor(max_workers=3) as pool:
    for f in [pool.submit(run,x) for x in tasks]: f.result()
