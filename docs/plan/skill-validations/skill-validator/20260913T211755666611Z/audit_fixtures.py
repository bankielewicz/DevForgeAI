"""Independent JSON Schema engine plus external-reference byte verification."""
import json
import warnings
from pathlib import Path
from harness import RUN, PRIOR, read, save, sha, inventory
with warnings.catch_warnings():
    warnings.simplefilter('ignore', DeprecationWarning)
    from jsonschema import Draft202012Validator, RefResolver

schemas=RUN/'source/schemas'
def schema_check(value):
    version=value['schema_version']
    schema=json.loads(read(schemas/(version+'.schema.json')))
    common=json.loads(read(schemas/'adaptive-common.schema.json'))
    resolver=RefResolver(base_uri=schemas.as_uri()+'/',referrer=schema,store={schemas.as_uri()+'/adaptive-common.schema.json':common},handlers={'http':lambda x:(_ for _ in ()).throw(ValueError('Network disabled')),'https':lambda x:(_ for _ in ()).throw(ValueError('Network disabled'))})
    return [e.message for e in Draft202012Validator(schema,resolver=resolver).iter_errors(value)]

def references(value):
    count=0
    if isinstance(value,dict):
        if set(value)=={'path','sha256'}:
            path=Path(value['path'])
            assert path.is_absolute(), 'External ref must be absolute'
            assert sha(read(path))==value['sha256'], 'Ref digest mismatch'
            count+=1
        else:
            for v in value.values(): count+=references(v)
    elif isinstance(value,list):
        for v in value: count+=references(v)
    return count

results=[]
paths=[]
for base in [RUN/'trials',PRIOR/'trials/independent/R06',PRIOR/'trials/independent/R07']:
    for row in inventory(base)['files']:
        if row['path'].endswith('.json'):
            paths.append(base/row['path'])
for path in paths:
    value=json.loads(read(path))
    if not isinstance(value,dict) or value.get('schema_version') not in ('standalone-set-input-v1','set-assessment-v1','set-validation-request-v1','project-evidence-v1','adaptation-proposal-v1','adaptation-selection-v1','set-authoring-v1'): continue
    errors=schema_check(value)
    references_count=references(value)
    if value['schema_version']=='standalone-set-input-v1':
        ids={m['member_id'] for m in value['members']}
        assert len(ids)==len(value['members'])
        for m in value['members']:
            assert set(m['depends_on'])<=ids
            package=m['package']
            actual=inventory(Path(package['root']))
            assert actual['files']==json.loads(read(Path(package['manifest']['path'])))
            assert actual['package_digest']==package['package_digest']
        for h in value['handoffs']:
            assert h['producer'] in ids and h['consumer'] in ids
            if h['required']: assert h['producer'] in next(m['depends_on'] for m in value['members'] if m['member_id']==h['consumer'])
    results.append(dict(path=str(path),schema_errors=errors,verified_references=references_count))
save(RUN/'fixture-audit.json',dict(engine='installed jsonschema 4.24.0',limitation='Candidate schemas are shared data; frozen-spec handoff and count obligations independently adjudicated. No schema check proves actual skill-quality evidence.',records=results))
assert all(not r['schema_errors'] for r in results)
print('Validated',len(results),'record shapes and',sum(r['verified_references'] for r in results),'reference occurrences; no errors.')
