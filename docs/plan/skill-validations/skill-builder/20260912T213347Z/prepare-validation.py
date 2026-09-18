import datetime as dt
import hashlib
import importlib.util
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path('C:/Projects/DevForgeAI')
RUN = Path(__file__).parent
RID = RUN.name
OLD = ROOT / 'docs/plan/skill-validations/skill-builder/20260912T161842Z'
BUILD = ROOT / 'docs/plan/skill-builds/skill-builder/20260912T212438315Z'
VALIDATOR = ROOT / '.agents/skills/skill-validator'
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def ref(path): return {'path':path.relative_to(RUN).as_posix(),'sha256':digest(path)}
def cp(source, target):
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('xb') as out: out.write(source.read_bytes())
    assert digest(source)==digest(target)
module_spec=importlib.util.spec_from_file_location('observe',VALIDATOR/'scripts/observe.py')
observe=importlib.util.module_from_spec(module_spec); module_spec.loader.exec_module(observe)
def tree(source,target):
    files,excluded=observe.inventory(observe.safe_path(source))
    assert not excluded, excluded
    for name,path,info in files: cp(path,target/name)
    return len(files)

tree(OLD/'inputs/specs',RUN/'inputs/specs')
for name in ('revision-spec.md','source-manifest.json','findings.json','origin-record.json','validation-report.md','handoff.json'):
    cp(OLD/name,RUN/'inputs/prior-validation'/name)
for name in ('final-delivery-readback.json','pointer-publication-readback.json','published-cases.jsonl','published-results.jsonl','published-input-readback.json','environment.json'):
    cp(BUILD/name,RUN/'inputs/build'/name)
publication_files=tree(BUILD/'published',RUN/'inputs/build/published')
for name in ('SKILL.md','scripts/observe.py','references/origin.md','references/rules.md','references/trials.md','references/reporting.md','references/handoff.md'):
    cp(VALIDATOR/name,RUN/'inputs/validator'/name)
checker=Path('C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py')
cp(checker,RUN/'inputs/installed-checker/quick_validate.py')
manifest=json.loads((RUN/'source-manifest.json').read_text())
delivery=json.loads((RUN/'inputs/build/final-delivery-readback.json').read_text())
assert manifest['files']==delivery['files']
pub=RUN/'inputs/build/published'
prov=pub/'revision/evidence/build-provenance.json'
pointer=pub/'revision/evidence/active-baseline.json'
contract=pub/'revision/evidence/build-contract.json'
assert digest(prov)==delivery['provenance']['sha256']
assert digest(pointer)==delivery['pointer']['sha256']
p=json.loads(prov.read_text()); pointer_data=json.loads(pointer.read_text())
assert p['result']=='COMPLETE' and p['contract_sha256']==digest(contract)
assert pointer_data['origin']['sha256']==digest(prov)
assert sorted(pointer_data['baseline'],key=lambda x:x['path'])==[{'path':x['path'],'sha256':x['sha256']} for x in manifest['files']]
save(RUN/'trials/delivery-identity/observation.json',{'schema_version':'1','run_id':RID,'complete_rows_match':True,'publication_files_copied':publication_files,'provenance_sha256':digest(prov),'pointer_sha256':digest(pointer),'contract_sha256':digest(contract),'package_digest':manifest['package_digest'],'status':'MATCH'})
save(RUN/'origin-record.json',{'schema_version':'1','run_id':RID,'target_name':'skill-builder','original_source_root':str(ROOT/'src/agents/skills/skill-builder'),'manifest':ref(RUN/'source-manifest.json'),'specification':ref(RUN/'inputs/prior-validation/revision-spec.md'),'origin_kind':'existing_spec','history_kind':'generated','historical_origin':'unknown before the explicit adopted origin; current generated revision verified','prior_evidence':ref(prov),'completeness':'complete','uncertainties':['Generated revision follows an adopted unknown-history origin; neither ordinary file publication nor static records constitute protected enforcement.'],'source_readback_state':'NOT_RUN'})
sources=json.loads((OLD/'sources.json').read_text())
sources['run_id']=RID
for row in sources['sources']:
    row['sha256']=digest(RUN/row['snapshot_path'])
    if row['source_id'] in ('openai-skills','agent-skills'):
        row['retrieved_at_utc']=dt.datetime.now(dt.timezone.utc).isoformat();row['freshness']='live_verified'
sources['sources'].append({'source_id':'approved-revision','original_path':str(OLD/'revision-spec.md'),'retrieved_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'snapshot_path':'inputs/prior-validation/revision-spec.md','sha256':digest(RUN/'inputs/prior-validation/revision-spec.md'),'sections':['Required editorial correction','Requirement register and file mapping','Acceptance cases'],'freshness':'local_verified'})
save(RUN/'sources.json',sources)
rules=json.loads((OLD/'rule-set.json').read_text());rules['run_id']=RID;rules['selected_at_utc']=dt.datetime.now(dt.timezone.utc).isoformat();rules['selection_timing']='Pinned before deterministic execution, routing tasks and final results; semantic intake and cold-task planning had begun. Expected cold outcomes were retained before cold task dispatch.'
for rule in rules['rules']:
    for source in rule['source_refs']:source['sha256']=digest(RUN/source['path'])
    rule['limitation']='Bounded development assessment; selected live guidance and retained project specifications; no framework acceptance or future execution guarantee.'
    if rule['rule_id']=='SB-CUSTODY':rule['expected_observation']='Actual delivered bytes match published generated revision, contract, original approved revision input and adoption lineage; preserve origin distinctions.'
    if rule['rule_id']=='SB-CONSISTENCY':
        rule['source_refs']=[dict(ref(RUN/'inputs/prior-validation/revision-spec.md'),source_id='approved-revision',locator='REV-001 and AC-01/AC-02')]
    if rule['rule_id']=='SB-COLD':rule['expected_observation']='Complete the authorized fresh instruction-only task-card specification build from minimal inputs, with required checks and delivery readback.'
rules['rules'].extend([
 {'rule_id':'SB-DELTA','title':'Exact approved two-file correction','method':'deterministic','expected_observation':'Only the specified evidence row and its matching manifest artifact digest change; every other file and detailed trial/routing requirement remains identical.'},
 {'rule_id':'SB-ROUTING','title':'Predeclared independent routing classification','method':'behavioral','expected_observation':'Independent description classification matches all positive and near-miss declared routes; native activation remains separate.'},
 {'rule_id':'SB-RECORDS','title':'Evidence integrity and complete readback','method':'deterministic','expected_observation':'References and input hashes match, required record shapes are coherent and actual target/spec readback remains unchanged.'}])
for rule in rules['rules'][-3:]:rule.update({'revision':'2026-09-12.2','source_refs':[dict(ref(RUN/'inputs/prior-validation/revision-spec.md'),source_id='approved-revision',locator='REV-001 through REV-003; acceptance cases')],'authority_class':'project_policy','applicability':'applicable','required':True,'limitation':'Current authorized bounded correction; no new campaign requirement.'})
save(RUN/'rule-set.json',rules)
import yaml
save(RUN/'environment.json',{'schema_version':'1','run_id':RID,'target_name':'skill-builder','os':platform.platform(),'python':sys.version,'pyyaml':yaml.__version__,'shell':'PowerShell via exec_command; exact parent host identification retained under inputs/build/environment.json','checker':str(checker),'checker_sha256':digest(checker),'validator_sha256':digest(VALIDATOR/'SKILL.md'),'host_task_runner':'collaboration.spawn_agent available; cold workflow fork_turns none','authorized_effects':'Fresh evidence plus disposable synthetic project writes only. Current user expressly supersedes validation-only builder prohibition for bounded trials; no target or operational copy writes.'})
for case,argv in [
 ('structure',['python','-B','-X','utf8',str(VALIDATOR/'scripts/observe.py'),'structure','--source',str(RUN/'source')]),
 ('installed-checker',['python','-B','-X','utf8',str(checker),str(RUN/'source')])]:
    folder=RUN/'trials'/case;folder.mkdir(parents=True)
    save(folder/'plan.json',{'schema_version':'1','case_id':case,'requirement_ids':['REV-003','AC-04'],'fixture_inputs':[ref(RUN/'source-manifest.json')],'expected_outputs':'exit 0; supported deterministic/structural checks pass','expected_effects':'stdout/stderr observations only','executor':'Python subprocess','command':argv,'timeout_seconds':120,'permitted_write_root':str(folder)})
    start=dt.datetime.now(dt.timezone.utc).isoformat();c=subprocess.run(argv,capture_output=True,text=True,encoding='utf-8',timeout=120,cwd=ROOT)
    (folder/'attempt-001.stdout.txt').write_text(c.stdout,encoding='utf-8');(folder/'attempt-001.stderr.txt').write_text(c.stderr,encoding='utf-8')
    save(folder/'attempt-001.json',{'argv':argv,'cwd':str(ROOT),'start':start,'end':dt.datetime.now(dt.timezone.utc).isoformat(),'exit':c.returncode,'stdout_sha256':digest(folder/'attempt-001.stdout.txt'),'stderr_sha256':digest(folder/'attempt-001.stderr.txt')})
    print(case,c.returncode,c.stdout[:250])
print('publication files',publication_files,'rule-set',digest(RUN/'rule-set.json'))
