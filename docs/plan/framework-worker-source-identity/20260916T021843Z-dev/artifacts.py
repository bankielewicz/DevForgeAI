"""Append-only evidence inventory; no product authority or operational effects."""
import json, os, sys
from pathlib import Path
import record
ROOT = Path(__file__).resolve().parent
TRIALS = record.WORKSPACE/'docs/plan/framework-worker-trials'
def write(name, value):
    with (ROOT/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,indent=2); f.write('\n')
def names():
    return sorted(p.name for p in TRIALS.iterdir() if p.is_dir() and p.name.startswith(('NI-sources-','RT-source-type-')))
def files(base):
    for directory, dirs, entries in os.walk(base,followlinks=False):
        for name in list(dirs):
            path=Path(directory)/name
            if path.lstat().st_file_attributes & 0x400:
                dirs.remove(name)
                yield path, {'kind':'reparse','target':os.readlink(path)}
        for name in entries:
            path=Path(directory)/name
            if path.lstat().st_file_attributes & 0x400:
                yield path, {'kind':'reparse','target':os.readlink(path)}
            else:
                yield path, {'kind':'file','bytes':path.stat().st_size,'sha256':record.sha256(path)}
if sys.argv[1]=='before':
    write('external-fixtures-before.json',names())
elif sys.argv[1]=='after':
    before=json.loads((ROOT/'external-fixtures-before.json').read_text())
    write('external-fixtures-owned.json',[str(TRIALS/name) for name in names() if name not in before])
elif sys.argv[1]=='seal':
    rows=[]
    for path,entry in files(ROOT):
        assert path.name != 'artifact-manifest.json', 'Seal is write-once'
        rows.append({'path':str(path),**entry})
    for value in json.loads((ROOT/'external-fixtures-owned.json').read_text()):
        base=Path(value)
        assert base.parent==TRIALS and base.name.startswith(('NI-sources-','RT-source-type-'))
        for path,entry in files(base): rows.append({'path':str(path),**entry})
    rows.sort(key=lambda r:r['path'].casefold())
    write('artifact-manifest.json',rows)
    errors=[]
    for row in rows:
        if row['kind']=='file' and record.sha256(Path(row['path']))!=row['sha256']: errors.append(row['path'])
    assert not errors,errors
    print(json.dumps({'entries':len(rows),'sha256':record.sha256(ROOT/'artifact-manifest.json'),'readback_errors':errors}))
else: raise SystemExit('unknown operation')
