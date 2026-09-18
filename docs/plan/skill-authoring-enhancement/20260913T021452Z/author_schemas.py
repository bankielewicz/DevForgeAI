from pathlib import Path
import json
RUN = Path(__file__).resolve().parent
B = RUN / 'candidate/skill-builder'
V = RUN / 'candidate/skill-validator'
ref = {'type':'object','required':['path','sha256'],'additionalProperties':False,'properties':{'path':{'type':'string','minLength':1},'sha256':{'type':'string','pattern':'^[0-9a-f]{64}$'}}}
strings = {'type':'array','items':{'type':'string'}}
def schema(version, fields, required=None):
    fields = {'schema_version':{'const':version}, **fields}
    return {'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','required':required or list(fields),'properties':fields,'additionalProperties':False,'$defs':{'reference':ref}}
r = {'$ref':'#/$defs/reference'}
refs = {'type':'array','items':r}
text = {'type':'string','minLength':1}
common = {key:text for key in ('run_id','project_root','target_root','target_name')}
contract = schema('authoring-contract-v1', {**common,'operation':{'enum':['create','edit','import','spec_build','adopt']},'authorization':text,'history_review':text,'change_paths':{**strings,'uniqueItems':True},'requirements':{'type':'array','minItems':1},'capabilities':{'type':'array'},'expected_outputs':{'type':'array'},'side_effects':{'type':'array'},'inputs':refs,'known_issues':strings,'prior':r,'legacy_root':text,'retry_of':r})
contract['required'] = [k for k in contract['properties'] if k not in ('prior','legacy_root','retry_of')]
contract['properties'].update({'purpose':text,'activation':{},'dependencies':{'type':'array'},'operational_constraints':{'type':'array'},'recovery':{}})
record = schema('authoring-v1', {**common,'record_kind':{'const':'authoring'},'operation':text,'authorization':text,'contract':r,'inputs':refs,'prior_origin':{'type':'object','required':['kind'],'properties':{'kind':{'enum':['observed','adopted','legacy_generated','authored']},'reference':r,'historical_origin':{'const':'unknown'}}},'managed_paths':strings,'retained_user_paths':strings,'before_manifest':r,'candidate_manifest':{'anyOf':[r,{'type':'null'}]},'delivered_manifest':r,'baseline_manifest':r,'applied_paths':strings,'authoring_state':{'enum':['AUTHORED','PARTIAL','BLOCKED']},'validation_status':{'const':'NOT_PERFORMED'},'testing_status':{'const':'NOT_PERFORMED'},'unresolved_issues':strings,'rows':{'type':'array'}})
record['required'].remove('baseline_manifest')
baseline = schema('authoring-baseline-v1', {'record_kind':{'const':'authoring_baseline'},'run_id':text,'target_root':text,'target_name':text,'authoring_record':r,'baseline_manifest':r,'baseline_root':text})
request = schema('validation-request-v1', {'record_kind':{'const':'validation_request'},'authoring_run_id':text,'project_root':text,'target_root':text,'target_name':text,'target_manifest':r,'package_digest':{'type':'string','pattern':'^[0-9a-f]{64}$'},'authoring_record':r,'specification_refs':refs,'changed_paths':strings,'known_issues':strings,'capabilities':{'type':'array'},'expected_outputs':{'type':'array'},'side_effects':{'type':'array'},'permission':text})
for name, value in [('authoring-contract',contract),('authoring-record',record),('authoring-baseline',baseline),('validation-request',request)]:
    for root in (B,V):
        path = root / 'schemas' / (name + '.schema.json')
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print('Wrote distinct schemas for authoring contracts, records, baselines and handoff.')
