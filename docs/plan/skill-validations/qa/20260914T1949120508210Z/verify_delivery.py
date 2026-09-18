"""Final reference, schema and literal-path readback checks."""
from bootstrap import ROOT, PROJECT, VALIDATOR, write, run, observe
from prepare_trials import ref, put
import hashlib
import json
import sys
import jsonschema

# Correct source identity, preserving the original derived records for audit.
for name in ['sources.json','findings.json','handoff.json']:
    (ROOT/'inputs'/('pre-delivery-'+name)).write_bytes((ROOT/name).read_bytes())
sources=json.loads((ROOT/'sources.json').read_bytes())
source_path=ROOT/'source/references/reporting-handoff.md'
sources['sources'].append(dict(source_id='qa-runtime-reporting',original_path=str(PROJECT/'src/agents/skills/qa/references/reporting-handoff.md'),retrieved_at_utc=None,sha256=ref(source_path)['sha256'],snapshot_path=ref(source_path)['path'],sections=['Separate package evaluation'],freshness='snapshot_only'))
write(ROOT/'sources.json',sources)
findings=json.loads((ROOT/'findings.json').read_bytes())
findings['findings'][0]['source_refs'][0]['source_id']='qa-runtime-reporting'
write(ROOT/'findings.json',findings)
handoff=json.loads((ROOT/'handoff.json').read_bytes())
handoff['findings']=ref(ROOT/'findings.json')
write(ROOT/'handoff.json',handoff)

schema=json.loads((ROOT/'inputs/evaluation-result.schema.json').read_bytes())
rows=[json.loads(line) for line in (ROOT/'evaluation/results-001.jsonl').read_text(encoding='utf-8').splitlines()]
for row in rows:
    jsonschema.validate(row,schema)
    for item in row['evidence']:
        assert hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256']
bundle=json.loads((ROOT/'evaluation/bundle-manifest.json').read_bytes())
for item in bundle['inputs']:
    assert hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256'],item['path']
manifest=json.loads((ROOT/'source-manifest.json').read_bytes())
assert observe.make_manifest(PROJECT/'src/agents/skills/qa')['files']==manifest['files']
assert ROOT == PROJECT/'docs/plan/skill-validations/qa/20260914T1949120508210Z'
write(ROOT/'delivery-verification.json',dict(schema_version='1',run_id=ROOT.name,target_name='qa',jsonl_schema_rows=70,jsonl_schema_status='PASS',bundle_inputs_verified=len(bundle['inputs']),literal_root=str(ROOT),target_readback='UNCHANGED',delivered_artifacts=[ref(ROOT/name) for name in ['validation-report.md','checks.jsonl','findings.json','handoff.json','source-manifest.json','source-after-manifest.json','evaluation/bundle-manifest.json','evaluation/results-001.jsonl']],limits='Schema/reference checks do not establish semantic or native skill acceptance. Corrected one finding source ID to identify the runtime file actually cited; no finding content or outcome changed.'))
run('records-final',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/observe.py'),'records','--run-root',str(ROOT)])
value=json.loads((ROOT/'observations/records-final.stdout').read_bytes())
assert value['status']=='OBSERVED',value['errors']
print(json.dumps({'record_integrity':value['status'],'errors':value['errors'],'references_verified':value['references_checked'],'schema_rows':len(rows),'bundle_inputs':len(bundle['inputs']),'assessment':'INCOMPLETE'},indent=2))
