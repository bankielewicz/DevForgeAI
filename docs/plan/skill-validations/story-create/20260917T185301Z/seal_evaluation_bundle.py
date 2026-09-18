"""Hash declared evaluation artifacts and independently check retained originals."""
import datetime
import hashlib
import json
from pathlib import Path

RAW=Path(__file__).resolve().parent
PROJECT=RAW.parents[4]
CAPSULE=RAW.with_name(RAW.name+'-records')

def write(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as stream:
        json.dump(value,stream,indent=2,ensure_ascii=False,allow_nan=False)
        stream.write('\n')

def main():
    files=[]
    # Exhaustive within these selected trees; no measured target executable exclusion.
    for name in ('source','inputs','evaluator','evaluation','trials','guidance'):
        files.extend(p for p in (RAW/name).rglob('*') if p.is_file())
    files.extend(p for p in RAW.iterdir() if p.is_file() and p.name not in ('evaluation-bundle-manifest.json','evaluation-bundle-readback.json'))
    rows=[]
    for path in sorted(set(files)):
        data=path.read_bytes()
        rows.append(dict(path=path.relative_to(RAW).as_posix(),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
    bundle=dict(schema_version='story-evaluation-bundle-v1',run_id=RAW.name,created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),target_package_digest=json.loads((RAW/'source-manifest.json').read_bytes())['package_digest'],purpose='Byte binding of external evaluation artifacts, not a skill build or protected acceptance.',included=['source/**','inputs/**','evaluator/**','evaluation/**','trials/**','guidance/**','top-level raw files except this manifest and its readback'],exclusions=['test-work/** retains redundant Windows unit synthetic runtime fixtures; original test code, results and captured target are bound.','Sibling final report/supplemental records have their own integrity checks; they are not runner inputs.'],files=rows)
    write(RAW/'evaluation-bundle-manifest.json',bundle)
    mismatches=[]
    for row in rows:
        path=RAW/row['path']
        data=path.read_bytes()
        if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:mismatches.append(row['path'])
    operational=[]
    for captured in (RAW/'evaluator').rglob('*'):
        if not captured.is_file():continue
        rel=captured.relative_to(RAW/'evaluator')
        original=Path('C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py') if rel.as_posix()=='installed-creator-quick_validate.py' else PROJECT/'.agents/skills/skill-validator'/rel
        operational.append(dict(original_path=str(original),sha256=hashlib.sha256(original.read_bytes()).hexdigest(),unchanged=original.read_bytes()==captured.read_bytes()))
    assert all(row['unchanged'] for row in operational)
    write(CAPSULE/'operational-readback.json',dict(schema_version='1',checked=len(operational),result='MATCH',files=operational))
    write(RAW/'evaluation-bundle-readback.json',dict(schema_version='story-evaluation-bundle-readback-v1',manifest_sha256=hashlib.sha256((RAW/'evaluation-bundle-manifest.json').read_bytes()).hexdigest(),checked=len(rows),mismatches=mismatches,result='MATCH' if not mismatches else 'MISMATCH'))
    assert not mismatches
    print(json.dumps({'bound_files':len(rows),'bytes':sum(r['bytes'] for r in rows),'operational_files_unchanged':len(operational),'readback':'MATCH'}))

if __name__=='__main__':main()
