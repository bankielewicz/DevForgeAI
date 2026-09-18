"""Write-once final closure artifact index."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
output = root/'artifact-manifest.json'
assert not output.exists(), 'Closure already sealed'
entries = []
for path in sorted(root.iterdir()):
    if path.is_file() and path!=output:
        raw = path.read_bytes()
        entries.append({'path':path.name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
with output.open('x',encoding='utf-8') as stream:
    json.dump({'entries':entries,'self_exclusion':'artifact-manifest.json'},stream,indent=2)
assert all(hashlib.sha256((root/entry['path']).read_bytes()).hexdigest()==entry['sha256'] for entry in entries)
print(json.dumps({'entries_verified':len(entries),'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}))
