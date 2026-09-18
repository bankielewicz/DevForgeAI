"""Verify selected inputs and retain a baseline; evidence only."""
import json
import platform
import shutil
from pathlib import Path
import record

ROOT = Path(__file__).resolve().parent
PRIOR = ROOT.parent / '20260915T2306060954875Z'
HANDOFF = ROOT.parent / '20260916T000205Z-resume-audit'
errors = []
bindings = []
for name in ['candidate-manifest.json', 'inputs-manifest.json']:
    entries = json.loads((PRIOR/name).read_text(encoding='utf-8'))
    result = []
    for entry in entries:
        path = Path(entry['path'])
        actual = record.sha256(path)
        row = {**entry, 'actual_sha256': actual, 'matches': actual == entry['sha256']}
        result.append(row)
        if not row['matches']:
            errors.append(str(path))
    record.atomic_json(ROOT/('baseline-' + name), result)
    bindings.append({'path':str(PRIOR/name), 'sha256':record.sha256(PRIOR/name)})
manifest = json.loads((HANDOFF/'handoff-manifest.json').read_text(encoding='utf-8'))
for name, entry in manifest['entries'].items():
    path = Path(entry['actual_path'])
    actual = record.sha256(path)
    bindings.append({'name':name,'path':str(path),'sha256':actual,'expected_sha256':entry['sha256']})
    if actual != entry['sha256']:
        errors.append(str(path))
record.atomic_json(ROOT/'input-and-handoff-bindings.json', bindings)
live = record.package_manifest()
record.atomic_json(ROOT/'baseline-package.json', live)
for entry in live:
    if entry['kind'] != 'file':
        errors.append('unexpected reparse:' + entry['path'])
        continue
    source = record.PACKAGE / entry['path']
    target = ROOT/'baseline-snapshot'/entry['path']
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
tools = {name: shutil.which(name) for name in ['python','powershell','pwsh','cargo','rustc','rustfmt','cargo-clippy','cargo-llvm-cov','git','rg']}
record.atomic_json(ROOT/'initial-environment.json', {'cwd':str(Path.cwd()),'workspace':str(record.WORKSPACE.resolve()),
    'platform':platform.platform(),'machine':platform.machine(),'python':platform.python_version(),
    'git_metadata':(record.WORKSPACE/'.git').exists(),'tools':tools,
    'ancestor_instructions':[str(path) for path in [Path('C:/AGENTS.md'),Path('C:/Projects/AGENTS.md'),record.WORKSPACE/'AGENTS.md'] if path.is_file()]})
record.atomic_json(ROOT/'preparation-result.json', {'errors':errors,'candidate_file_count':len(live), 'baseline_manifest_sha256':record.sha256(PRIOR/'candidate-manifest.json')})
print(json.dumps({'errors':errors,'candidate_files':len(live),'tools':tools}))
raise SystemExit(bool(errors))
