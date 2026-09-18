"""Independent retained-copy readback; preserve original Linux locator bytes."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOLDER = ROOT / 'linux-campaign-001/linux-simple-v3'
PROJECT = FOLDER / 'Project space'
ORIGINAL = '/tmp/devforgeai-custody-native-20260915T1243422567556Z/linux-simple-v3/Project space/'
errors = []
checked = []

def refs(value, document):
    if isinstance(value, dict):
        if set(value) == {'path', 'sha256'} and isinstance(value['path'], str):
            locator = value['path']
            if not locator.startswith(ORIGINAL):
                errors.append({'document':document, 'unmapped_locator':locator})
                return
            retained = PROJECT / locator[len(ORIGINAL):]
            actual = hashlib.sha256(retained.read_bytes()).hexdigest() if retained.is_file() else None
            checked.append({'document':document, 'original_locator':locator, 'retained_locator':str(retained), 'matches':actual == value['sha256']})
            if actual != value['sha256']:
                errors.append({'document':document, 'locator':locator, 'error':'digest/missing mismatch'})
        for child in value.values():
            refs(child, document)
    elif isinstance(value, list):
        for child in value:
            refs(child, document)

for path in sorted((PROJECT / 'docs').rglob('*.json')):
    refs(json.loads(path.read_text()), path.relative_to(PROJECT).as_posix())

run = PROJECT / 'docs/plan/skill-authorings/sort-lines/create-01'
record = json.loads((run/'authoring-record.json').read_text())
readback = json.loads((run/'publication-readback.json').read_text())
record_state = record['authoring_state']
package = PROJECT / 'result-skill/sort-lines'
rows = [{'path':p.relative_to(package).as_posix(), 'bytes':p.stat().st_size, 'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(package.rglob('*')) if p.is_file()]
digest = hashlib.sha256(json.dumps(rows, ensure_ascii=False, separators=(',',':')).encode()).hexdigest()
declared = json.loads((run/'delivered-manifest.json').read_text())
result = {'scope':'Independent retained Linux artifact readback, not runtime generated-skill execution', 'reference_count':len(checked), 'reference_errors':errors, 'checked_references':checked, 'delivered_manifest_matches':rows == declared['files'], 'package_digest_matches':digest == readback['package_digest'], 'authoring_state':record_state, 'readback_state':readback['state'], 'final_text':(PROJECT/'final.txt').read_text(), 'full_native_workflow':'FAIL: final response has incorrect destination link and omits manual handoff/status', 'artifact_publication':'PASS' if not errors and digest == readback['package_digest'] and rows == declared['files'] else 'FAIL'}
(ROOT/'native/linux-simple-artifact-readback.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k:v for k,v in result.items() if k!='checked_references'}, indent=2))
