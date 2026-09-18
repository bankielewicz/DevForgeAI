"""Additional selected-set public-interface positives and counterexamples."""
import copy
import hashlib
import json
from pathlib import Path
import sys
from run_checks import execute
RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[3]
B=ROOT/'src/agents/skills/skill-builder'
V=ROOT/'.agents/skills/skill-validator'
PY=[sys.executable,'-B','-X','utf8']
out=RUN/'additional'
out.mkdir()
def ref(path): return {'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2))
    return ref(path)
results=[]
origin=RUN/'trials-round2/update-review'
original=origin/'records/prior/record.json'
for name,wrong_parent,malformed,expected in [('full-set',False,False,0),('wrong-parent',True,False,1),('false-full-omission',False,True,1)]:
    target=out/name
    p=json.loads(original.read_text())
    if wrong_parent:
        current=json.loads((origin/'records/changed/record.json').read_text())
        p['members'][0]['parent_core']=current['members'][0]['parent_core']
    proposal=write(target/'inputs/proposal.json',p)
    member=p['members'][0]
    selected=write(target/'inputs/selection.json',{'schema_version':'adaptation-selection-v1','proposal':proposal,'member_ids':['A'],'destinations':[{'member_id':'A','target_root':member['target_root']}],'authorization':ref(origin/'authorization.txt'),'permitted_effects':['Read-only synthetic assessment.']})
    authored=write(target/'inputs/set.json',{'schema_version':'set-authoring-v1','run_id':'fixture','selection':selected,'ordered_member_ids':['A'],'members':[{'member_id':'A','status':'RETAINED','authoring_record':None,'validation_request':None,'package':member['existing_package'],'reason':'Retained unchanged.','applied_paths':[]}],'state':'NO_CHANGE','validation_status':'NOT_PERFORMED','testing_status':'NOT_PERFORMED','issues':[]})
    request={'schema_version':'set-validation-request-v1','run_id':'fixture','selection':selected,'set_authoring':authored,'scope':'full_set','members':[{'member_id':'A','package':member['existing_package'],'request':None,'adaptive_descriptor':ref(Path(member['target_root'])/'assets/devforgeai-skill.json')}],'handoffs':[],'omitted_member_ids':['A'] if malformed else [],'omitted_handoff_ids':[],'permission':'No external effects.'}
    path=Path(write(target/'request.json',request)['path'])
    ba,br=execute(name+'-builder',PY+[str(B/'scripts/adaptive.py'),'inspect','--record',str(path)],'Contract expected exit '+str(expected))
    va,vr=execute(name+'-validator',PY+[str(V/'scripts/adaptive_observe.py'),'intake-set','--request',str(path),'--request-sha256',ref(path)['sha256']],'Contract expected exit '+str(expected))
    results.append({'case':name,'expected_exit':expected,'builder_exit':br['exit_code'],'validator_exit':vr['exit_code'],'builder_evidence':str(ba),'validator_evidence':str(va),'input':ref(path)})
write(RUN/'additional-results.json',{'schema_version':'1','cases':results})
print(json.dumps(results,indent=2))
