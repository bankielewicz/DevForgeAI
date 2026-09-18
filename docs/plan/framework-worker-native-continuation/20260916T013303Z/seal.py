"""Write-once custody index for this bounded prerequisite observation."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
destination = root/'artifact-manifest.json'
assert not destination.exists()
entries = []
for path in sorted(root.rglob('*')):
    if path.is_file() and path!=destination:
        raw = path.read_bytes()
        entries.append({'path':path.relative_to(root).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
bindings = json.loads((root/'bindings.json').read_text())
fixture = Path(bindings['fixture'])/'task.json'
assert hashlib.sha256(fixture.read_bytes()).hexdigest()==bindings['task_sha256']
payload = {'entries':entries,'external_fixture':{'path':str(fixture),'bytes':fixture.stat().st_size,'sha256':bindings['task_sha256']},
           'self_exclusion':'artifact-manifest.json'}
with destination.open('x',encoding='utf-8') as stream:
    json.dump(payload,stream,indent=2)
assert all(hashlib.sha256((root/entry['path']).read_bytes()).hexdigest()==entry['sha256'] for entry in entries)
print(json.dumps({'entries_verified':len(entries),'external_fixtures_verified':1,'sha256':hashlib.sha256(destination.read_bytes()).hexdigest()}))
