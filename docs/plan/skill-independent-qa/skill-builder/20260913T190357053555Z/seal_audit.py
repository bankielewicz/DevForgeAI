"""Index small primary evidence and native records without traversing huge fixtures."""
from pathlib import Path
import datetime
import hashlib
import json
import stat

RUN=Path(__file__).resolve().parent
excluded={'evidence-index.json','evidence-index-readback.json'}
paths=[]
for folder in (RUN,RUN/'reports',RUN/'inputs'):
    for p in folder.iterdir():
        mode=p.lstat()
        if stat.S_ISREG(mode.st_mode) and p.name not in excluded:
            paths.append(p)
for attempt in (RUN/'native').iterdir():
    assert not attempt.is_symlink()
    for name in ('plan.json','result.json','prompt.txt','output/final.txt','output/stdout.jsonl','output/stderr.txt','output/termination.txt'):
        p=attempt/name
        if p.exists(): paths.append(p)
assert len(paths)<=1000
rows=[]
for p in sorted(set(paths)):
    info=p.lstat()
    assert stat.S_ISREG(info.st_mode) and not getattr(info,'st_file_attributes',0)&1024
    assert info.st_size<=16*1024*1024
    data=p.read_bytes()
    assert len(data)==info.st_size
    rows.append({'path':p.relative_to(RUN).as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
assert sum(r['bytes'] for r in rows)<=64*1024*1024
cases=json.loads((RUN/'case-results.json').read_bytes())
requirements=json.loads((RUN/'requirement-results.json').read_bytes())
clauses=json.loads((RUN/'complete-clause-results.json').read_bytes())
assert len(cases)==100 and len({r['id'] for r in cases})==100
assert len(requirements)==14 and len(clauses)==137
for row in cases:
    for value in row['platform_results'].values():
        for evidence in value['evidence']: assert (RUN/evidence).is_file(),evidence
for row in requirements+clauses:
    for evidence in row['evidence']: assert (RUN/evidence).is_file(),evidence
value={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Primary audit files, report/input direct files, native prompts/plans/results/raw outputs. Synthetic fixtures are retained but not recursively indexed here; exact native before/after manifests and source snapshot manifests are separate.','files':rows,'count':len(rows),'bytes':sum(r['bytes'] for r in rows),'mapping_checks':{'unique_cases':100,'requirements':14,'other_clauses':137,'evidence_paths_exist':True},'limits':{'files':1000,'per_file_bytes':16*1024*1024,'total_bytes':64*1024*1024}}
(RUN/'evidence-index.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
assert all(hashlib.sha256((RUN/r['path']).read_bytes()).hexdigest()==r['sha256'] for r in rows)
(RUN/'evidence-index-readback.json').write_text(json.dumps({'status':'MATCH','files':len(rows),'evidence_index_sha256':hashlib.sha256((RUN/'evidence-index.json').read_bytes()).hexdigest(),'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n',encoding='utf-8')
print('MATCH',len(rows),'files; 100 cases/14 requirements/137 clauses; all mapped evidence paths exist')
