"""Independent read-only reduction of archived Linux observations and current source."""
import hashlib
import json
from pathlib import Path
import sys
import jsonschema
RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[3]
OUT=RUN/'linux-regression-002'
REG=OUT/'regression'
COMBINED=REG/'linux-combined'
def read(path):return json.loads(path.read_text(encoding='utf-8'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def manifest(root):return {p.relative_to(root).as_posix():sha(p) for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
assert (OUT/'linux-fixture-inputs').is_dir(),'archive fixture copy not finished'
snapshot=read(REG/'linux-snapshot.json')
win=read(RUN/'regression/v3-combined/scope.json')['source']
live=manifest(ROOT/'src/agents/skills/skill-builder')
assert snapshot['source']==win==live,'Linux/Windows/current package bytes differ'
schema=read(REG/'result.schema.json')
rows=[];expected={};runtime=[];receipts=[]
for name in ('linux-legacy','linux-authoring','linux-adaptive-stage'):
    folder=REG/name
    scope=read(folder/'scope.json')
    assert scope['source']==live,'source changed between Linux batches'
    assert all(sha(folder/'test-snapshot'/path)==digest for path,digest in scope['tests'].items()),'test snapshot hash mismatch'
    wanted=read(folder/'expected.json')
    actual=[json.loads(line) for line in (folder/'results.jsonl').read_text().splitlines()]
    assert not set(expected)&set(wanted),'duplicate batch inventory'
    expected.update(wanted);rows.extend(actual)
    runtime.append(read(folder/'runtime.json'))
    receipt=read(REG/(name+'-process.json'))
    assert receipt['exit_code']==0 and not receipt['timeout'],'non-successful process'
    receipts.append({'batch':name,'cases':len(wanted),'seconds':receipt['elapsed_seconds'],'exit':receipt['exit_code']})
ids=[r['case'] for r in rows]
assert len(ids)==len(set(ids)) and set(ids)==set(expected),'missing, duplicate, or unexpected observations'
for row in rows:jsonschema.validate(row,schema)
assert all(r['status']=='PASS' for r in rows),'required nonpass'
combined_rows=[json.loads(line) for line in (COMBINED/'results.jsonl').read_text().splitlines()]
assert combined_rows==rows and read(COMBINED/'expected.json')==expected,'combined case mismatch'
coverage=read(COMBINED/'coverage.json')
names={key.replace('\\','/').split('src/agents/skills/skill-builder/',1)[1] for key in coverage['files']}
assert names=={p for p in live if p.endswith('.py')},'missing first-party module'
assert all(not f['excluded_lines'] and f['summary']['excluded_lines']==0 for f in coverage['files'].values()),'coverage exclusions'
keys=('covered_lines','num_statements','covered_branches','num_branches')
totals={key:sum(f['summary'][key] for f in coverage['files'].values()) for key in keys}
assert all(coverage['totals'][key]==value for key,value in totals.items()),'coverage totals mismatch'
fixture_manifest=snapshot['fixture_manifest']
archived_audit=OUT/'linux-fixture-inputs/skill-builder/20260913T152822695886Z'
assert manifest(archived_audit)==fixture_manifest,'setup fixture bytes changed or archive incomplete'
line_rate=100*totals['covered_lines']/totals['num_statements']
assert line_rate>=95 and len(rows)==319,'required coverage or case inventory not met'
result={'status':'PASS','required':len(expected),'passed':len(rows),'pass_rate':100.0,'covered_lines':totals['covered_lines'],'statements':totals['num_statements'],'line_percent':line_rate,'covered_branches':totals['covered_branches'],'branches':totals['num_branches'],'branch_percent':100*totals['covered_branches']/totals['num_branches'],'excluded_lines':0,'source_files':len(live),'python_files':len(names),'same_bytes_as_windows_v3_and_current_source':True,'linux_fixture_files':len(fixture_manifest),'batches':receipts,'runtime':runtime,'adaptations':snapshot['test_adaptations'],'input_hashes':{name:sha(COMBINED/name) for name in ('expected.json','results.jsonl','coverage.json','scope.json')},'schema_sha256':sha(REG/'result.schema.json')}
(OUT/'independent-archive-verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('runtime','input_hashes','adaptations')}))
