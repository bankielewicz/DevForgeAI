"""Verify final independent QA custody and candidate readback after QA sealing."""
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
QA = Path(r'C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion-qa\20260916T003840Z-retest')
DEV = ROOT.parent/'20260916T003840Z-dev'
def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1048576),b''):
            value.update(chunk)
    return value.hexdigest()

manifest_path = QA/'artifact-manifest.json'
assert digest(manifest_path)==sys.argv[1], 'QA manifest differs from independent return'
manifest = json.loads(manifest_path.read_text())
errors = []
for entry in manifest['entries']:
    path = QA/entry['path']
    assert path.is_relative_to(QA) and '..' not in path.parts
    if not path.is_file() or path.stat().st_size!=entry['bytes'] or digest(path)!=entry['sha256']:
        errors.append(str(path))
external_entries = manifest.get('external_entries',[])
external_root = Path(r'C:\Projects\DevForgeAI\docs\plan\framework-worker-trials')
for entry in external_entries:
    path = Path(entry['path'])
    resolved = path.resolve()
    assert resolved.is_relative_to(external_root)
    relative = resolved.relative_to(external_root)
    assert len(relative.parts)==3 and relative.parts[0].startswith('RT-source-type-') and relative.parts[1:]==('fixture','task.json')
    if not path.is_file() or path.stat().st_size!=entry['bytes'] or digest(path)!=entry['sha256']:
        errors.append(str(path))
candidate = json.loads((DEV/'candidate-manifest.json').read_text())
for entry in candidate:
    if digest(Path(entry['path']))!=entry['sha256']:
        errors.append(entry['path'])
inputs = json.loads((DEV/'inputs-manifest.json').read_text())
for entry in inputs:
    if digest(Path(entry['path']))!=entry['sha256']:
        errors.append(entry['path'])
result = {'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'qa_manifest_sha256':digest(manifest_path),
    'qa_entries_verified':len(manifest['entries']),'candidate_files_verified':len(candidate),
    'qa_external_fixture_files_verified':len(external_entries),
    'input_files_verified':len(inputs),'errors':errors}
with (ROOT/'independent-qa-readback.json').open('x',encoding='utf-8') as stream:
    json.dump(result,stream,indent=2)
print(json.dumps(result))
raise SystemExit(bool(errors))
