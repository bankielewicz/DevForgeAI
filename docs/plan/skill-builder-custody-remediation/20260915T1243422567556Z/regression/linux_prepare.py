"""Digest-bound disposable native-filesystem regression snapshot and Linux fixtures."""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
ROOT=Path('/mnt/c/Projects/DevForgeAI')
REL=Path('docs/plan/skill-builder-custody-remediation/20260915T1243422567556Z/regression')
DEST=Path(sys.argv[1])
assert str(DEST).startswith('/tmp/devforgeai-regression-')
DEST.mkdir(exist_ok=False)
def manifest(root):return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
before=manifest(ROOT/'src/agents/skills/skill-builder')
for name in ('skill-builder','skill-validator'):
    source=ROOT/'src/agents/skills'/name
    shutil.copytree(source,DEST/'src/agents/skills'/name,ignore=shutil.ignore_patterns('__pycache__'))
run=DEST/REL
run.mkdir(parents=True)
for source in (ROOT/REL).glob('*.py'):shutil.copyfile(source,run/source.name)
for name in ('builder-before.json','result.schema.json'):shutil.copyfile(ROOT/REL/name,run/name)
assert before==manifest(DEST/'src/agents/skills/skill-builder')==manifest(ROOT/'src/agents/skills/skill-builder')
source=run/'test_authoring.py'
text=source.read_text()
text=text.replace("        if os.name != 'nt':\n            self.skipTest('Windows separator equivalence requires Windows')\n",'')
text=text.replace('test_windows_path_spellings_round_trip_to_intake','test_linux_literal_path_spellings_round_trip_to_intake')
text=text.replace("for spelling in ('native', 'forward', 'mixed'):","for spelling in ('native', 'forward'):")
text=text.replace('test_old_noncanonical_stage_requires_fresh_run','test_linux_changed_stage_requires_fresh_run')
source.write_text(text)
os.environ['ADAPTIVE_TEST_ROOT']=str(run/'unused-adaptive-fixtures')
sys.path.insert(0,str(run))
import test_builder_adaptive as t
import authoring
audit=DEST/'docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z'
factory=audit/'factory'
factory.mkdir(parents=True)
fixture=t.AdaptiveTests()
fixture.root=factory
fixture.sequence=0
proposal=fixture.proposal()
member=copy.deepcopy(proposal['members'][0])
member.update(id='B',name='notes-b',target_root=str(factory/'skills/notes-b'),depends_on=['A'])
proposal['members'].append(member)
# Handoff semantics needs a proposed, unoccupied graph independent of published set.
graph=copy.deepcopy(proposal)
for member in graph['members']:member['target_root']=str(factory/'graph-skills'/member['name'])
t.write(audit/'fixtures/followup-02/records/proposal.json',graph)
selection=fixture.selection(proposal)
selection_ref=t.write(factory/'selection.json',selection)
members=[]
for member in proposal['members']:
    target=Path(member['target_root'])
    contract={'schema_version':'authoring-contract-v1','run_id':member['id'],'project_root':str(factory),'target_root':str(target),'target_name':target.name,'operation':'create','authorization':'Create synthetic Linux regression fixtures only.','history_review':'no_known_history','change_paths':['SKILL.md','references/adaptive-contract.md','assets/devforgeai-skill.json','scripts/check_project_binding.py'],'requirements':proposal['requirements'],'capabilities':[],'expected_outputs':[],'side_effects':[],'inputs':[],'known_issues':[]}
    cp=factory/(member['id']+'-contract.json');t.write(cp,contract)
    stage=factory/'docs/plan'/member['id'];authoring.begin(cp,stage)
    staging=factory/'staging'/target.name;t.package(staging,'expertise')
    shutil.copytree(staging,stage/'candidate',dirs_exist_ok=True)
    result=authoring.publish(stage)
    assert result['state']=='AUTHORED',result
    members.append({'member_id':member['id'],'status':'AUTHORED','authoring_record':t.reference(stage/'authoring-record.json'),'validation_request':t.reference(stage/'validation-request.json'),'package':fixture.package_ref(target),'reason':'Actual synthetic fixture publication','applied_paths':result['applied_paths']})
record={'schema_version':'set-authoring-v1','run_id':'linux-fixture','selection':selection_ref,'ordered_member_ids':['A','B'],'members':members,'state':'AUTHORED','validation_status':'NOT_PERFORMED','testing_status':'NOT_PERFORMED','issues':[]}
t.write(audit/'fixtures/extended-04/valid/set.json',record)
t.a.Reader().record(record)
t.a.Reader().record(graph)
(run/'linux-snapshot.json').write_text(json.dumps({'source':before,'source_root':str(ROOT/'src/agents/skills/skill-builder'),'snapshot_root':str(DEST/'src/agents/skills/skill-builder'),'test_adaptations':['Windows mixed separator case becomes native/forward POSIX literal-path counterpart. Changed-stage case runs same mutation on POSIX.','Historical absolute Windows linked fixtures replaced by newly authored synthetic Linux records; unchanged negative test oracles.'],'fixture_manifest':manifest(audit),'python':sys.version},indent=2))
print(json.dumps({'snapshot':str(DEST),'source_files':len(before),'fixture_files':len(manifest(audit))}))
