"""Bind final reports, runners, receipts and command streams in bounded scopes."""
import json
import stat
from evidence import RUN, ROOT, PACKAGE, dump, identity, manifest, sha

assert identity()['package_digest']=='7715f8b80a9b089a4349f6bbb3b502a52d55a03bb2eb2ec65f861ea4be77ff3a'
destination=RUN/'artifact-manifests'
destination.mkdir(exist_ok=False)
scopes=[]

def files_only(folder):
    rows=[];total=0
    for path in sorted(folder.iterdir()):
        info=path.lstat()
        assert not stat.S_ISLNK(info.st_mode) and not getattr(info,'st_file_attributes',0)&0x400
        if stat.S_ISDIR(info.st_mode):continue
        assert stat.S_ISREG(info.st_mode) and len(rows)<2000 and total+info.st_size<=32*1024*1024
        data=path.read_bytes();assert len(data)==info.st_size
        total+=len(data);rows.append({'path':path.name,'bytes':len(data),'sha256':sha(data)})
    return rows

def scope(folder,recursive=True):
    rows=manifest(folder,synthetic=True) if recursive else files_only(folder)
    value={'root':str(folder.relative_to(RUN)),'scope':'recursive' if recursive else 'direct files only','files':rows}
    output=destination/('%04d.json'%len(scopes))
    dump(output,value)
    scopes.append({'path':output.relative_to(RUN).as_posix(),'bytes':output.stat().st_size,'sha256':sha(output.read_bytes()),'root':value['root'],'files':len(rows)})

scope(RUN,False)
for folder in sorted((RUN/'commands').iterdir()):
    if folder.is_dir():scope(folder)
scope(RUN/'regression-release',False)
for folder in sorted((RUN/'regression-release/commands').iterdir()):
    if folder.is_dir():scope(folder)
for name in ('evaluations/release-02','trials/release-02/receipts','legacy-trials/release/receipts','legacy-trials/contract-edges-03/receipts','release-readback','source-before','source-before-env-fix','specifications','runtime-plans'):
    scope(RUN/name)

results=[json.loads(line) for line in (RUN/'evaluations/release-02/results.jsonl').read_text().splitlines()]
expected=json.loads((RUN/'evaluations/release-02/expected-results.json').read_text())
schema=json.loads((RUN/'evaluation-result.schema.json').read_text())
import jsonschema
for row in results:jsonschema.Draft202012Validator(schema).validate(row)
assert len(results)==len(expected)==52
assert {r['case_id'] for r in results}=={r['case_id'] for r in expected}
assert all(r['status']=='PASS' and r['package_digest']==identity()['package_digest'] for r in results)
plan=ROOT/'docs/plan/skill-builder-qa-remediation-plan.md'
dump(RUN/'artifact-manifest.json',{'schema_version':'maintenance-artifact-index-v1','source':identity(),'plan':{'path':str(plan),'sha256':sha(plan.read_bytes())},'scopes':scopes,'jsonl_check':{'rows':52,'unique_expected_cases':52,'schema':'evaluation-result.schema.json','status':'PASS'},'limits':'Each receipt scope <=2000 files and32MiB; nofollow, regular files only. This index and its constituent manifests are excluded from their own inputs.','coverage':'Source snapshots, final runner/graders/schema/output, every maintenance command receipt and retained script snapshot, final fixture pre/post receipts and final historical replay command streams.','not_indexed':'Raw synthetic fixture trees are retained separately and represented by fixture receipts where available; large limit fixtures and intermediate fixture trees are not recursively included. Independent audit has its own evidence inventory. Filesystem timestamps and out-of-scope operational packages are not attested.'})
receipt=RUN/'artifact-manifest.json'
print(json.dumps({'scopes':len(scopes),'referenced_files':sum(s['files'] for s in scopes),'manifest_sha256':sha(receipt.read_bytes()),'jsonl_rows':52,'source_digest':identity()['package_digest']}))
