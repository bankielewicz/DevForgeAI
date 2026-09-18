import copy
import json
import sys
from pathlib import Path
import independent_probes as q
from qa_harness import RUN,ROOT,TARGET,PRIOR,execute,inventory,save,sha

BASE=RUN/'trials/additional'
BASE.mkdir(parents=True,exist_ok=True)

def shared(root,omit_lineage=False):
    s=q.standalone(root)
    loc={'ref':s['authorization'],'start_line':1,'end_line':1}
    ev={'schema_version':'project-evidence-v1','run_id':'external-evidence','project_root':str(root),'scope_roots':[str(root)],'inputs':[s['authorization']],'facts':[{'id':'F1','category':'domain','statement':'Local task-card transformation.','basis':'user_supplied','sources':[loc]}],'exclusions':[],'complete':True,'capabilities':[],'gaps':[]}
    evref=q.js(root/'evidence.json',ev)
    req=[{'id':'R'+str(i),'origin':'derived','statement':'Preserve requirement '+str(i)+'.','source_refs':[],'rationale':'Independent synthetic requirement.','verification':'Compare exact output.'} for i in range(1,4)]
    members=[{'id':m['member_id'],'name':m['package']['name'],'role':'core','action':'retain','target_root':m['package']['root'],'existing_package':m['package'],'parent_core':None,'responsibility':'Produce' if m['member_id']=='A' else 'Consume','exclusions':['External operations'],'triggers':['Local card'],'near_misses':['Deployment'],'requirement_ids':[r['id'] for r in req],'fact_ids':['F1'],'rationale':'Distinct direction.','depends_on':m['depends_on'],'capabilities':[],'lineage_delta':[]} for m in s['members']]
    proposal={'schema_version':'adaptation-proposal-v1','run_id':'external-proposal','mode':'propose','project_evidence':evref,'prior_proposal':None,'requirements':req,'members':members,'handoffs':s['handoffs'],'gaps':[],'state':'NO_CHANGE'}
    pref=q.js(root/'proposal.json',proposal)
    sel={'schema_version':'adaptation-selection-v1','proposal':pref,'member_ids':['A','B'],'destinations':[{'member_id':m['member_id'],'target_root':m['package']['root']} for m in s['members']],'authorization':s['authorization'],'permitted_effects':['Read-only assessment']}
    selref=q.js(root/'selection.json',sel)
    authored={'schema_version':'set-authoring-v1','run_id':'retained-set','selection':selref,'ordered_member_ids':['A','B'],'members':[{'member_id':m['member_id'],'status':'RETAINED','authoring_record':None,'validation_request':None,'package':m['package'],'reason':'Explicit retained synthetic member.','applied_paths':[]} for m in s['members']],'state':'NO_CHANGE','validation_status':'NOT_PERFORMED','testing_status':'NOT_PERFORMED','issues':[]}
    aref=q.js(root/'authoring.json',authored)
    request={'schema_version':'set-validation-request-v1','run_id':'external-request','selection':selref,'set_authoring':aref,'scope':'full_set','members':[{'member_id':m['member_id'],'package':m['package'],'request':None,'adaptive_descriptor':None} for m in s['members']],'handoffs':s['handoffs'],'omitted_member_ids':[],'omitted_handoff_ids':[],'permission':'No external effects.'}
    return request,proposal

results=[]
for cid,mut,expected in [('G01',None,0),('G02','subset',0),('G03','unclosed-subset',1),('G04','extra',1),('G05','bad-digest',1),('G06','version',1),('G07','lineage-good',0),('G08','lineage-omitted',1)]:
    root=BASE/cid; req,proposal=shared(root)
    value=req
    if mut=='subset': value.update(scope='eligible_subset',members=value['members'][:1],handoffs=[],omitted_member_ids=['B'],omitted_handoff_ids=['card'])
    if mut=='unclosed-subset': value.update(scope='eligible_subset',members=value['members'][1:],handoffs=[],omitted_member_ids=['A'],omitted_handoff_ids=['card'])
    if mut=='extra': value['extra']=1
    if mut=='bad-digest': value['selection']['sha256']='0'*64
    if mut=='version': value['schema_version']='set-validation-request-v2'
    if mut and mut.startswith('lineage'):
        core=q.package(root,'core-review'); q.write(core/'references/adaptive-contract.md','| ID | Requirement |\n| --- | --- |\n'+''.join('| '+r['id']+' | '+r['statement']+' |\n' for r in proposal['requirements']))
        m=proposal['members'][1]; m.update(role='project_variant',action='create',existing_package=None,parent_core=q.pkgref(core),lineage_delta=[{'requirement_id':r['id'],'disposition':'retained','reason':'Preserved verbatim.','replacement_requirement_ids':[r['id']]} for r in proposal['requirements']])
        if mut=='lineage-omitted': m['lineage_delta'].pop()
        proposal['state']='PROPOSED'; value=proposal
    path=root/'selected.json'; q.js(path,value)
    save(root/'expectations.json',{'expected_exit':expected,'oracle':'Frozen shared contract '+str(mut)+'; exact selected dependencies and three requirement dispositions.','before':inventory(root)})
    outputs=[]
    for reader,script,args in [('validator',TARGET/'scripts/adaptive_observe.py',['records','--run-root',str(root/'records')]),('builder',ROOT/'src/agents/skills/skill-builder/scripts/adaptive.py',['inspect','--record',str(path)])]:
        if reader=='validator': q.js(root/'records/selected.json',value)
        name=cid+'-'+reader
        r=execute(name,['python','-B','-X','utf8',str(script),*args])
        outputs.append({'reader':reader,'exit_status':r['exit_status'],'matched':r['exit_status']==expected})
    results.append({'case_id':cid,'expected':expected,'readers':outputs})
save(BASE/'shared-results.json',results)

# Optional tokenization stays offline in the target's inspected cached-only reader.
small=q.package(BASE/'tokens')
for encoding in ['cl100k_base','r50k_base','p50k_base','o200k_base','gpt2']:
    execute('token-'+encoding,['python','-B','-X','utf8',str(TARGET/'scripts/adaptive_observe.py'),'package','--source',str(small),'--tokenizer','tiktoken','--encoding',encoding])

before=json.loads((PRIOR/'before-validator.json').read_bytes())
current=json.loads((RUN/'target-before.json').read_bytes())
old={x['path']:x for x in before['files']}; new={x['path']:x for x in current['files']}
save(RUN/'baseline-compatibility.json',{'baseline_count':len(old),'baseline_digest':sha(json.dumps(before['files'],ensure_ascii=False,separators=(',',':')).encode()),'added':sorted(new.keys()-old.keys()),'removed':sorted(old.keys()-new.keys()),'modified':sorted(k for k in old.keys()&new.keys() if old[k]!=new[k]),'unchanged_preexisting_scripts_tests_schemas':all(old[k]==new[k] for k in old if k.startswith(('scripts/','tests/','schemas/'))),'provenance':'Baseline manifest from retained implementation evidence; no generated/adopted history inferred. Old bytes verified where retained in prior snapshots separately.'})
print(json.dumps({'shared':results}))
