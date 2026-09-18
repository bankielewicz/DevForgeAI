"""Finalize resource adjudication, readbacks and exact artifact receipts."""
from prepare import *
import ast

R=ROOT/'assessment'
supp=ROOT/'supplemental'
supp.mkdir()
raw=json.loads((ROOT/'observations/package.stdout').read_bytes())
def absolute_ref(path): return {'path':str(path.resolve()),'sha256':observe.sha256(path.read_bytes())}
resources=raw['observations']['resources']
for row in resources:
    row['role']='runtime' if row['path']=='SKILL.md' else 'template' if row['path'].startswith('assets/') else 'reference'
    row['usage']='used'
    row['evidence']=[absolute_ref(R/'source'/row['path']),absolute_ref(R/'semantic-observations.json')]
    row['reason']='Entrypoint workflow consumer' if row['path']=='SKILL.md' else 'Loaded by SKILL.md workflow and linked reference consumers' if row['role']=='reference' else 'Named logical record consumer in references/evidence-resume.md and associated workflow reference'
value={'schema_version':'adaptive-observations-v1','run_id':ROOT.name,'target_digest':json.loads((ROOT/'source-manifest.json').read_bytes())['package_digest'],'unicode_candidates':raw['observations']['unicode_candidates'],'resources':resources,'edges':raw['observations']['edges'],'context':raw['observations']['context'],'bindings':[],'limitations':['Primary validator semantic self-review, not independent cold execution.','Original helper stdout is retained unchanged.','Ordinary skill: no adaptive binding or set applies.','Actual runtime loads, tokenizer values and native activation were not observed.']}
write(supp/'resource-observations.json',value)
run('supplemental-records',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/adaptive_observe.py'),'records','--run-root',str(supp)])
# Recheck every pinned local rule/intake input, independently of a rejected packet.
index=json.loads((ROOT/'inputs/input-index.json').read_bytes())
rechecks=[]
for row in index:
    actual=observe.sha256(observe.read_stable(observe.safe_path(row['original_path'])))
    rechecks.append({'original_path':row['original_path'],'expected_sha256':row['snapshot']['sha256'],'observed_sha256':actual,'match':actual==row['snapshot']['sha256']})
assert all(row['match'] for row in rechecks)
write(ROOT/'observations/final-input-readback.json',{'inputs':rechecks,'all_match':True})
run('final-current-source',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/observe.py'),'readback','--source',str(PROJECT/'src/agents/skills/dev'),'--manifest',str(ROOT/'source-manifest.json')])
assert json.loads((ROOT/'observations/final-current-source.stdout').read_bytes())['status']=='MATCH'
# Syntax and observed output-schema verification are evidence, not cold behavior.
compiled=[]
for path in [ROOT/'bundle/runner.py',ROOT/'bundle/graders.py',ROOT/'test_bundle.py',ROOT/'test_graders.py']:
    ast.parse(path.read_text(encoding='utf-8'),filename=str(path)); compiled.append(str(path))
schema=json.loads((ROOT/'bundle/evidence.schema.json').read_bytes())
result_rows=[json.loads(line) for line in (ROOT/'trials/bundle-attempt-001/results.jsonl').read_text(encoding='utf-8').splitlines()]
for row in result_rows:
    assert set(row)==set(schema['required'])
    assert row['result'] in schema['properties']['result']['enum']
    assert row['schema_version']=='dev-evaluation-v1' and row['required'] is True
    assert len(row['package_digest'])==len(row['scenario_sha256'])==64
write(ROOT/'observations/final-static-review.json',{'python_ast_parse':compiled,'result_schema_checked_rows':len(result_rows),'method':'Explicit required-field, enum, const and digest-length checks; not a full JSON Schema engine','limitations':['No evaluator coverage percentage measured','No Rust runtime qualification','No cold task outputs available']})
checks=json.loads((ROOT/'observations/records-attempt-001.stdout').read_bytes())
supp_checks=json.loads((ROOT/'observations/supplemental-records.stdout').read_bytes())
assert not checks['errors'] and supp_checks['status']=='OBSERVED'
# Source paths have been reviewed; enumerate bounded run tree before each descent.
paths,excluded=observe.inventory(observe.safe_path(ROOT))
assert not excluded
rows=[{'path':name,'bytes':info.st_size,'sha256':observe.sha256(observe.read_stable(path,info))} for name,path,info in paths]
write(ROOT/'artifact-ledger.json',{'run_id':ROOT.name,'purpose':'Exact retained artifacts, including executed bundle, all cases, attempts and report. Ledger and final receipt self-excluded.','files':rows,'count':len(rows),'total_bytes':sum(row['bytes'] for row in rows)})
write(ROOT/'FINAL-RECEIPT.json',{'run_id':ROOT.name,'assessment':'INCOMPLETE','assessment_completed':True,'report':ref(R/'validation-report.md'),'checks':ref(R/'checks.jsonl'),'handoff':ref(R/'handoff.json'),'selected_request_sha256':EXPECTED,'request_digest_verified':True,'request_intake':'REJECTED','rejection_reason':'Exact target_root spelling mismatch between contract and request/record','package_digest':json.loads((ROOT/'source-manifest.json').read_bytes())['package_digest'],'source_readback':'MATCH','local_inputs_readback':'MATCH','mandatory_bundle_artifacts':'CREATED_AND_EXECUTED','evaluated_build':'INCOMPLETE','bundle_manifest':ref(ROOT/'bundle/artifact-manifest.json'),'bundle_results':ref(ROOT/'trials/bundle-attempt-001/results.jsonl'),'artifact_ledger':ref(ROOT/'artifact-ledger.json'),'evaluator_tests':{'passing':23,'required':23,'prior_red_failures':2,'not_skill_behavior':True},'dv_cases':{'passing':1,'required':18,'not_run':17},'record_integrity':{'schema1_errors':len(checks['errors']),'schema1_references_checked':checks['references_checked'],'supplemental_status':supp_checks['status']},'installation':'NOT_PERFORMED','framework_acceptance':'NOT_EVALUATED','cold_native_trials':'NOT_RUN','native_implicit_activation':'NOT_RUN','operational_changes':'NOT_PERFORMED','skill_revision_proposed':False})
print('FINAL',str(ROOT/'FINAL-RECEIPT.json'),'artifacts',len(rows),'bytes',sum(row['bytes'] for row in rows))
