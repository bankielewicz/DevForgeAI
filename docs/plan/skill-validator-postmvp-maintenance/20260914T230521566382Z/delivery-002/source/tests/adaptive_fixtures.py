"""Synthetic raw contract inputs. No operational identity literals."""
import hashlib
import json
from pathlib import Path

def write(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
    return reference(path)

def reference(path):
    return {'path':str(path.resolve()),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def package(root, name):
    target = root / name
    target.mkdir(parents=True)
    raw = ('---\nname: '+name+'\ndescription: Convert the selected local requirement into a task card.\n---\nRead the input requirement; write its observable verification as JSON to the selected output.\n').encode()
    (target / 'SKILL.md').write_bytes(raw)
    rows = [{'path':'SKILL.md','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}]
    manifest = write(root / (name+'-manifest.json'),rows)
    return {'name':name,'root':str(target.resolve()),'manifest':manifest,'package_digest':hashlib.sha256(json.dumps(rows,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()}

def standalone(root):
    root.mkdir(parents=True,exist_ok=True)
    auth = root / 'authorization.txt'
    auth.write_text('Assess exactly A and B in disposable fixtures. No external effects.',encoding='utf-8')
    a,b = package(root,'producer'),package(root,'consumer')
    schema = write(root / 'task-card.schema.json', {'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','additionalProperties':False,'required':['schema_version','requirement_id','task','verification'],'properties':{'schema_version':{'const':'task-card-v1'},'requirement_id':{'const':'REQ-7'},'task':{'type':'string','minLength':1},'verification':{'type':'array','minItems':1,'items':{'type':'string','minLength':1}}}})
    return {'schema_version':'standalone-set-input-v1','run_id':'standalone-test','authorization':reference(auth),'members':[{'member_id':'A','package':a,'specifications':[],'adaptive_descriptor':None,'depends_on':[]},{'member_id':'B','package':b,'specifications':[],'adaptive_descriptor':None,'depends_on':['A']}],'handoffs':[{'id':'card','producer':'A','consumer':'B','artifact_role':'task-card','format':'json','schema_ref':schema,'contract':'task-card-v1 REQ-7 with nonempty task and observable verification','required':True,'failure_behavior':'block_consumer'}],'requirements':[],'gaps':[]}

def shared(root):
    selected = standalone(root)
    auth = selected['authorization']
    locator = {'ref':auth,'start_line':1,'end_line':1}
    evidence = {'schema_version':'project-evidence-v1','run_id':'golden-evidence','project_root':str(root.resolve()),'scope_roots':[str(root.resolve())],'inputs':[auth],'facts':[{'id':'domain','category':'domain','statement':'Selected task-card responsibility.','basis':'user_supplied','sources':[locator]}],'exclusions':[],'complete':True,'capabilities':[],'gaps':[]}
    evidence_ref = write(root/'project-evidence.json',evidence)
    req = {'id':'REQ-7','origin':'user','statement':'Convert selected requirement into a task card.','source_refs':[locator],'rationale':None,'verification':'Inspect task and verification fields.'}
    members = [{'id':row['member_id'],'name':row['package']['name'],'role':'core','action':'retain','target_root':row['package']['root'],'existing_package':row['package'],'parent_core':None,'responsibility':'Produce card' if row['member_id']=='A' else 'Consume card','exclusions':['Network'], 'triggers':['Selected local task card'],'near_misses':['Installation'],'requirement_ids':['REQ-7'],'fact_ids':['domain'],'rationale':'Selected existing responsibility.','depends_on':row['depends_on'],'capabilities':[],'lineage_delta':[]} for row in selected['members']]
    proposal = {'schema_version':'adaptation-proposal-v1','run_id':'golden-proposal','mode':'propose','project_evidence':evidence_ref,'prior_proposal':None,'requirements':[req],'members':members,'handoffs':selected['handoffs'],'gaps':[],'state':'NO_CHANGE'}
    proposal_ref = write(root/'adaptation-proposal.json',proposal)
    selection = {'schema_version':'adaptation-selection-v1','proposal':proposal_ref,'member_ids':['A','B'],'destinations':[{'member_id':row['member_id'],'target_root':row['package']['root']} for row in selected['members']],'authorization':auth,'permitted_effects':['Read-only assessment']}
    selection_ref = write(root/'adaptation-selection.json',selection)
    authored = {'schema_version':'set-authoring-v1','run_id':'golden-authored','selection':selection_ref,'ordered_member_ids':['A','B'],'members':[{'member_id':row['member_id'],'status':'RETAINED','authoring_record':None,'validation_request':None,'package':row['package'],'reason':'Selected unchanged retained member.','applied_paths':[]} for row in selected['members']],'state':'NO_CHANGE','validation_status':'NOT_PERFORMED','testing_status':'NOT_PERFORMED','issues':[]}
    authored_ref = write(root/'set-authoring.json',authored)
    request = {'schema_version':'set-validation-request-v1','run_id':'golden-request','selection':selection_ref,'set_authoring':authored_ref,'scope':'full_set','members':[{'member_id':row['member_id'],'package':row['package'],'request':None,'adaptive_descriptor':None} for row in selected['members']],'handoffs':selected['handoffs'],'omitted_member_ids':[],'omitted_handoff_ids':[],'permission':'Packet grants no external effects.'}
    return request
