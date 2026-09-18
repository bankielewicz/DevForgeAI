"""Read sealed development evidence and live bytes; no build or product invocation."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEV = ROOT.parent/'20260916T003840Z-dev'
PACKAGE = Path(r'C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe')
def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1048576),b''):
            value.update(chunk)
    return value.hexdigest()

manifest_path = DEV/'artifact-manifest.json'
assert digest(manifest_path) == 'db85dcaea35608c8948568b50c745e70c304682efcc46d35116edd3901939fa5'
manifest = json.loads(manifest_path.read_text())
errors = []
for entry in manifest['entries']:
    path = DEV/entry['path']
    assert path.is_relative_to(DEV) and '..' not in path.parts
    if entry['kind']=='reparse':
        if os.readlink(path)!=entry['target']:
            errors.append(str(path))
    elif not path.is_file() or path.stat().st_size!=entry['bytes'] or digest(path)!=entry['sha256']:
        errors.append(str(path))
for entry in manifest['external_rt_source_fixture_files']:
    path = Path(entry['path'])
    assert path.is_relative_to(PACKAGE.parents[2]/'docs/plan/framework-worker-trials')
    if digest(path)!=entry['sha256']:
        errors.append(str(path))
candidate = json.loads((DEV/'candidate-manifest.json').read_text())
expected = set()
for entry in candidate:
    path = Path(entry['path'])
    expected.add(path.relative_to(PACKAGE).as_posix())
    if digest(path)!=entry['sha256']:
        errors.append(str(path))
actual = set()
for base,dirs,files in os.walk(PACKAGE,followlinks=False):
    if Path(base)==PACKAGE:
        dirs[:] = [name for name in dirs if name!='target']
    for name in files:
        actual.add((Path(base)/name).relative_to(PACKAGE).as_posix())
if actual!=expected:
    errors.append({'added':sorted(actual-expected),'missing':sorted(expected-actual)})
inputs = json.loads((DEV/'inputs-manifest.json').read_text())
for entry in inputs:
    if digest(Path(entry['path']))!=entry['sha256']:
        errors.append(entry['path'])
result = {'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'developer_manifest_sha256':digest(manifest_path),
    'developer_entries_verified':len(manifest['entries']),'external_fixture_files_verified':len(manifest['external_rt_source_fixture_files']),
    'candidate_files_verified':len(candidate),'input_files_verified':len(inputs),'errors':errors}
output = ROOT/'developer-seal-readback.json'
with output.open('x',encoding='utf-8') as stream:
    json.dump(result,stream,indent=2)
print(json.dumps(result))
raise SystemExit(bool(errors))
