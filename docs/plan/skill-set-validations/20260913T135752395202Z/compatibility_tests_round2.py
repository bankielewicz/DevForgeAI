"""Independent contract fixtures and differential read-only CLI observations.

Expected outcomes come from the retained governing specification, not agreement
between the implementations. Source packages and prior evidence are read-only.
"""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys
from run_checks import execute

RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[3]
BUILDER=ROOT/'src/agents/skills/skill-builder'
VALIDATOR=ROOT/'.agents/skills/skill-validator'
PY=[sys.executable,'-B','-X','utf8']
results=[]

def sha(data): return hashlib.sha256(data).hexdigest()
def ref(path): return {'path':str(path.resolve()),'sha256':sha(path.read_bytes())}
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes((json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())
    return ref(path)
def package_ref(root,evidence,label):
    # Only the known regular synthetic fixture files are enumerated here.
    rows=[{'path':p.relative_to(root).as_posix(),'bytes':len(p.read_bytes()),'sha256':sha(p.read_bytes())} for p in sorted(root.rglob('*')) if p.is_file()]
    rows.sort(key=lambda row: row['path'])
    return {'name':root.name,'root':str(root),'manifest':write(evidence/(label+'-manifest.json'),rows),'package_digest':sha(json.dumps(rows,ensure_ascii=False,separators=(',',':')).encode())}
def package(root,role,parent=None,index_location='contract',crlf=False,ids=('R1','R2','R3')):
    root.mkdir(parents=True)
    requirements=[{'id':x,'statement':{'R1':'Preserve facts.','R2':'Use local files.','R3':'Preserve inputs.'}[x]} for x in ids]
    text='---\nname: '+root.name+'\ndescription: Summarize supplied synthetic facts.\n---\n'
    if index_location=='ordinary':
        text+='| ID | Requirement |\n| --- | --- |\n'+''.join('| '+r['id']+' | '+r['statement']+' |\n' for r in requirements)
        (root/'SKILL.md').write_bytes(text.encode())
        return
    text+='Read [contract](references/adaptive-contract.md) and [descriptor](assets/devforgeai-skill.json).\nRun scripts/check_project_binding.py before product writes; non-MATCH stops writes.\n'
    (root/'SKILL.md').write_bytes(text.encode())
    contract='# Contract\nInput notes.txt. Output out/summary.txt. Preserve supplied facts; no network.\n```devforgeai-requirements\n'+json.dumps(requirements)+'\n```\n'
    if crlf: contract=contract.replace('\n','\r\n')
    (root/'references').mkdir()
    (root/'references/adaptive-contract.md').write_bytes(contract.encode())
    (root/'scripts').mkdir()
    shutil.copyfile(BUILDER/'assets/adaptive-runtime/check_project_binding.py',root/'scripts/check_project_binding.py')
    write(root/'assets/devforgeai-skill.json',{'schema_version':'adaptive-skill-v1','name':root.name,'role':role,'binding_required':True,'parent_core':parent,'contract_path':'references/adaptive-contract.md','required_capabilities':['Python 3.10+'],'resource_roles':[{'path':'scripts/check_project_binding.py','role':'runtime','reason':'Checks before product actions.'}]})
def variant_case(case,index_location='contract',crlf=False):
    root=RUN/'trials-round2'/case
    root.mkdir(parents=True)
    auth=root/'authorization.txt'
    auth.write_text('Assess selected synthetic notes variant, preserving facts and inputs; local files only.\n')
    loc={'ref':ref(auth),'start_line':1,'end_line':1}
    evidence={'schema_version':'project-evidence-v1','run_id':'fixture','project_root':str(root),'scope_roots':[str(root)],'inputs':[ref(auth)],'facts':[{'id':'domain','category':'domain','statement':'Summarize selected notes.','basis':'user_supplied','sources':[loc]}],'exclusions':[],'complete':True,'capabilities':[],'gaps':[]}
    core=root/'parents/original/notes-core'
    package(core,'core',index_location=index_location,crlf=crlf)
    parent=package_ref(core,root,'parent')
    variant=root/'skills/notes-variant'
    package(variant,'project_variant',{'name':'notes-core','package_digest':parent['package_digest'],'requirement_ids':['R1','R2','R3']})
    member={'id':'A','name':'notes-variant','role':'project_variant','action':'retain','target_root':str(variant),'existing_package':package_ref(variant,root,'variant'),'parent_core':parent,'responsibility':'Summarize notes.','exclusions':['HTTP'],'triggers':['Summarize supplied notes'],'near_misses':['Install skills'],'requirement_ids':['R1','R2','R3'],'fact_ids':['domain'],'rationale':'Selected local note responsibility.','depends_on':[],'capabilities':[],'lineage_delta':[{'requirement_id':x,'disposition':'retained','reason':'Unchanged requirement.','replacement_requirement_ids':[x]} for x in ['R1','R2','R3']]}
    requirements=[{'id':x,'origin':'user','statement':s,'source_refs':[loc],'rationale':None,'verification':'Inspect preserved output.'} for x,s in [('R1','Preserve facts.'),('R2','Use local files.'),('R3','Preserve inputs.')]]
    p={'schema_version':'adaptation-proposal-v1','run_id':'fixture','mode':'propose','project_evidence':write(root/'evidence.json',evidence),'prior_proposal':None,'requirements':requirements,'members':[member],'handoffs':[],'gaps':[],'state':'NO_CHANGE'}
    return root,p
def observe(case,path,expected,kind='record'):
    before=sha(path.read_bytes())
    command=PY+[str(BUILDER/'scripts/adaptive.py'),'inspect','--record',str(path)]
    bpath,b=execute(case+'-builder',command,'Exit '+str(expected)+' from governing contract.')
    if kind=='set':
        command=PY+[str(VALIDATOR/'scripts/adaptive_observe.py'),'intake-set','--request',str(path),'--request-sha256',before]
    else:
        # Directory contains only this chosen top-level record, linked inputs elsewhere.
        command=PY+[str(VALIDATOR/'scripts/adaptive_observe.py'),'records','--run-root',str(path.parent)]
    vpath,v=execute(case+'-validator',command,'Exit '+str(expected)+' from governing contract.')
    assert sha(path.read_bytes())==before
    results.append({'case':case,'expected_exit':expected,'builder_exit':b['exit_code'],'validator_exit':v['exit_code'],'builder_evidence':str(bpath),'validator_evidence':str(vpath),'input':ref(path),'kind':kind})
def record(root,name,value): return Path(write(root/'records'/name/'record.json',value)['path'])

# Positive retained variant and equal-semantics update. Each record is immutable.
root,p=variant_case('update-review')
prior=record(root,'prior',p)
observe('baseline-variant',prior,0)
current=root/'parents/current/notes-core'
shutil.copytree(root/'parents/original/notes-core',current)
(current/'editorial.md').write_text('Explanatory change; requirement statements remain unchanged.\n')
review=copy.deepcopy(p)
review.update(mode='review_updates',prior_proposal=ref(prior),state='PROPOSED')
review['members'][0]['parent_core']=package_ref(current,root,'current')
observe('changed-equivalent-proposed',record(root,'changed',review),0)
observe('changed-false-no-change',record(root,'false-no-change',{**review,'state':'NO_CHANGE'}),1)
bad=copy.deepcopy(p)
bad.update(mode='review_updates')
bad['members'][0].update(role='expertise',parent_core=None,lineage_delta=[])
observe('review-nonvariant',record(root,'nonvariant',bad),1)

for name,location,crlf in [('ordinary-parent','ordinary',False),('crlf-parent','contract',True)]:
    root,p=variant_case(name,location,crlf)
    observe(name,record(root,'proposal',p),0)

# Make full set request with a self-consistent retained package but incorrect selected role.
root,p=variant_case('selected-role')
m=p['members'][0]
m.update(role='expertise',parent_core=None,lineage_delta=[])
proposal_ref=ref(record(root,'proposal',p))
selection={'schema_version':'adaptation-selection-v1','proposal':proposal_ref,'member_ids':['A'],'destinations':[{'member_id':'A','target_root':m['target_root']}],'authorization':ref(root/'authorization.txt'),'permitted_effects':['Read-only assessment']}
selection_ref=write(root/'selection.json',selection)
authored={'schema_version':'set-authoring-v1','run_id':'fixture','selection':selection_ref,'ordered_member_ids':['A'],'members':[{'member_id':'A','status':'RETAINED','authoring_record':None,'validation_request':None,'package':m['existing_package'],'reason':'Unchanged retained package.','applied_paths':[]}],'state':'NO_CHANGE','validation_status':'NOT_PERFORMED','testing_status':'NOT_PERFORMED','issues':[]}
request={'schema_version':'set-validation-request-v1','run_id':'fixture','selection':selection_ref,'set_authoring':write(root/'set-authoring.json',authored),'scope':'full_set','members':[{'member_id':'A','package':m['existing_package'],'request':None,'adaptive_descriptor':ref(Path(m['target_root'])/'assets/devforgeai-skill.json')}],'handoffs':[],'omitted_member_ids':[],'omitted_handoff_ids':[],'permission':'No external effects.'}
observe('wrong-delivered-role',record(root,'request',request),1,'set')

# Descriptor with a selected parent ID that is absent from its linked contract.
root,p=variant_case('missing-disposition')
variant=Path(p['members'][0]['target_root'])
contract=variant/'references/adaptive-contract.md'
contract.write_text('Input notes.txt; output out/summary.txt. Preserve facts.\nR1 retained; R2 retained.\n')
observe('missing-parent-disposition',variant/'assets/devforgeai-skill.json',1)

# Existing real manual builder artifacts are consumed unchanged, not rewritten fixtures.
previous=ROOT/'docs/plan/skill-adaptive-implementations/skill-builder/20260913T083452607505Z'
actual=previous/'attempts/20260913T133923855869Z-helpers/fixtures/test_BAT10_independent_continuation_and_subset/record-1.json'
observe('actual-partial-custody-subset',actual,0,'set')
single=previous/'native/20260913T131539650116Z-ordinary/project/docs/plan/skill-authorings/release-brief/20260913T1330251688074Z/validation-request.json'
attempt,receipt=execute('actual-native-manual-request',PY+[str(VALIDATOR/'scripts/authoring_intake.py'),'--request',str(single),'--request-sha256',ref(single)['sha256']],'Actual completed cold builder handoff binds current target; exit 0.')
results.append({'case':'actual-native-manual-request','expected_exit':0,'validator_exit':receipt['exit_code'],'validator_evidence':str(attempt),'input':ref(single)})

# Identical schemas and operational/development overlap are separate inventories.
schemas=[]
for path in sorted((BUILDER/'schemas').glob('*.json')):
    other=VALIDATOR/'schemas'/path.name
    if other.exists():
        schemas.append({'path':path.name,'json_equal':json.loads(path.read_bytes())==json.loads(other.read_bytes()),'builder_sha256':sha(path.read_bytes()),'validator_sha256':sha(other.read_bytes())})
write(RUN/'schema-comparison-round2.json',{'schema_version':'1','schemas':schemas})
write(RUN/'compatibility-results-round2.json',{'schema_version':'1','cases':results})
print(json.dumps(results,indent=2))
