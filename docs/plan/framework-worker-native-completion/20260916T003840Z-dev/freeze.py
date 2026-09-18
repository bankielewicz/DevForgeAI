"""Freeze the integrated development candidate and retain scoped differences."""
import difflib
import json
import shutil
from pathlib import Path
import record

ROOT = Path(__file__).resolve().parent
if (ROOT/'candidate-manifest.json').exists() or (ROOT/'candidate-snapshot').exists():
    raise SystemExit('Frozen candidate already exists; refusing replacement')
baseline = json.loads((ROOT/'baseline-package.json').read_text(encoding='utf-8'))
current = record.package_manifest()
before = {entry['path']:entry for entry in baseline}
after = {entry['path']:entry for entry in current}
changes = {'added':sorted(after.keys()-before.keys()), 'removed':sorted(before.keys()-after.keys()),
           'changed':sorted(path for path in before.keys() & after.keys() if before[path]!=after[path])}
manifest = []
for entry in current:
    if entry['kind'] != 'file':
        raise SystemExit('Cannot freeze reparse:' + entry['path'])
    source = record.PACKAGE/entry['path']
    target = ROOT/'candidate-snapshot'/entry['path']
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    manifest.append({'path':str(source), 'bytes':entry['bytes'], 'sha256':entry['sha256']})
record.atomic_json(ROOT/'candidate-manifest.json', manifest)
record.atomic_json(ROOT/'candidate-package.json', current)
record.atomic_json(ROOT/'changes.json', changes)
diff = []
for name in changes['changed'] + changes['added']:
    old = (ROOT/'baseline-snapshot'/name).read_text(encoding='utf-8').splitlines(keepends=True) if name in before else []
    new = (record.PACKAGE/name).read_text(encoding='utf-8').splitlines(keepends=True)
    diff.extend(difflib.unified_diff(old,new,fromfile='baseline/'+name,tofile='candidate/'+name))
(ROOT/'candidate.patch').write_text(''.join(diff),encoding='utf-8')
inputs = json.loads((ROOT/'baseline-inputs-manifest.json').read_text(encoding='utf-8'))
for entry in inputs:
    if record.sha256(Path(entry['path'])) != entry['sha256']:
        raise SystemExit('Input changed:' + entry['path'])
record.atomic_json(ROOT/'inputs-manifest.json', [{key:entry[key] for key in ['path','bytes','sha256']} for entry in inputs])
source = [entry for entry in manifest if Path(entry['path']).is_relative_to(record.PACKAGE/'src') and entry['path'].endswith('.rs')]
record.atomic_json(ROOT/'source-denominator.json', {'source_files':source,
    'coverage_rule':'All first-party executable lines in src/**/*.rs; no production source exclusion. Test/support/fixture and dependencies excluded by resolved ownership.',
    'platform':'Windows x64','features':'default; no optional package features','required_minimum_percent':95})
print(json.dumps({'candidate_files':len(manifest),'candidate_manifest_sha256':record.sha256(ROOT/'candidate-manifest.json'),
                  'source_files':len(source),'changes':changes}))
