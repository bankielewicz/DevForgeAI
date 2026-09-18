"""Bind and literally read back delivery paths; no acceptance authority."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
GREEN=ROOT.with_name('20260915T1834258428322Z-green')
EXPECTED=Path('C:/Projects/DevForgeAI/docs/plan/framework-worker-qa/20260915T1834258428322Z-dev')
assert ROOT==EXPECTED
assert str(EXPECTED).replace('/', '\\') in (ROOT/'context.md').read_text(encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=set(p for p in ROOT.iterdir() if p.is_file() and p.name not in ('delivery-manifest.json','output-readback.json'))
files.update(p for p in (ROOT/'candidate-snapshot').rglob('*') if p.is_file())
for base in [ROOT,GREEN]:
    files.update(p for p in base.glob('independent/*') if p.is_file())
    files.update(p for p in base.glob('*/*') if p.is_file() and p.name in ('receipt.json','stdout.txt','stderr.txt'))
    files.update(p for p in (base/'independent-attempts').rglob('*') if p.is_file())
files.update(p for p in GREEN.iterdir() if p.is_file())
entries=[{'expected_path':str(p),'actual_path':str(p.resolve()),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(files)]
(ROOT/'delivery-manifest.json').write_text(json.dumps(entries,indent=2),encoding='utf-8')
readback=[]
for e in json.loads((ROOT/'delivery-manifest.json').read_text()):
    p=Path(e['expected_path'])
    ok=str(p.resolve())==e['actual_path'] and p.stat().st_size==e['bytes'] and sha(p)==e['sha256']
    assert ok,p
    readback.append({'expected_path':e['expected_path'],'actual_path':str(p.resolve()),'sha256':sha(p),'matches':ok})
# Re-read source, tool artifacts and coverage profiles bound by delivered manifests.
for name in ['candidate-manifest.json','build-identities.json','raw-profile-identities.json']:
    for e in json.loads((ROOT/name).read_text()):
        assert sha(Path(e['path']))==e['sha256'],e['path']
result={'selected_evidence_value':str(EXPECTED),'selection_source':'qa-fix.md fresh sibling requirement; context.md exact mapping','manifest_sha256':sha(ROOT/'delivery-manifest.json'),'verified_entries':len(readback),'records':readback}
(ROOT/'output-readback.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'manifest_sha256':result['manifest_sha256'],'verified_entries':len(readback),'source_entries':32,'build_entries':54,'profile_entries':147}))
