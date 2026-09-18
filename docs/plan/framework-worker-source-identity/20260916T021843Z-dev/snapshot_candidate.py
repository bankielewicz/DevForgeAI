"""Preserve exact frozen source bytes and describe the selected delta."""
import json
from pathlib import Path
import record
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'candidate-manifest.json').read_text())
baseline={e['path']:e for e in json.loads((ROOT/'baseline-manifest.json').read_text())}
destination=ROOT/'candidate-snapshot'
destination.mkdir(exist_ok=False)
changes=[]
for entry in manifest:
    assert entry['kind']=='file'
    source=record.PACKAGE/entry['path']
    data=source.read_bytes()
    import hashlib
    assert hashlib.sha256(data).hexdigest()==entry['sha256'],entry['path']
    target=destination/entry['path']
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('xb') as output: output.write(data)
    old=baseline.pop(entry['path'],None)
    if old is None or old['sha256']!=entry['sha256']:
        changes.append({'path':entry['path'],'before_sha256':None if old is None else old['sha256'],'after_sha256':entry['sha256']})
assert not baseline,baseline
with (ROOT/'changed-files.json').open('x',encoding='utf-8') as output:
    json.dump(changes,output,indent=2);output.write('\n')
assert record.package_manifest()==manifest
print(json.dumps({'snapshot_files':len(manifest),'changed_files':changes}))
