"""Write-once source binding and descriptive coverage arithmetic, not authority."""
from pathlib import Path
import hashlib, json, sys
import record
ROOT = Path(__file__).resolve().parent
PACKAGE = record.PACKAGE
WORKSPACE = record.WORKSPACE

def write(name, value):
    with (ROOT/name).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2); f.write('\n')

if sys.argv[1] == 'freeze':
    entries = record.package_manifest()
    write('candidate-manifest.json', entries)
    sources = [entry for entry in entries if entry['path'].startswith('src/') and entry['path'].endswith('.rs')]
    write('coverage-source-denominator.json', {'platform':'Windows x64', 'features':'default; package has no optional features',
        'files':sources, 'exclusions':['tests and test-support fixtures','third-party dependencies'],
        'first_party_exclusions':[], 'required_executed_line_percent':95,
        'line_denominator':'LLVM measured executable lines over every listed src file; lib.rs may report 0 executable lines because it contains only module declarations'})
    selected = json.loads((ROOT/'input-manifest.json').read_text())
    path = 'docs/specs/framework/runtime/codex-worker-source-identity-v1.md'
    selected.append({'path':path,'sha256':record.sha256(WORKSPACE/path),'bytes':(WORKSPACE/path).stat().st_size})
    write('selected-inputs-final.json', selected)
    print(json.dumps({'files':len(entries),'rust_source_files':len(sources),'manifest_sha256':record.sha256(ROOT/'candidate-manifest.json')}))
elif sys.argv[1] == 'coverage':
    raw = Path(sys.argv[2])
    report = json.loads(raw.read_text(encoding='utf-8'))
    definitions = json.loads((ROOT/'coverage-source-denominator.json').read_text())['files']
    actual = {}
    for unit in report['data']:
        for file in unit['files']:
            path = Path(file['filename'])
            try: relative = path.relative_to(PACKAGE).as_posix()
            except ValueError: continue
            if relative.startswith('src/') and relative.endswith('.rs'):
                assert relative not in actual, relative
                actual[relative] = file['summary']['lines']
    rows = []
    for entry in definitions:
        relative = entry['path']
        assert record.sha256(PACKAGE/relative) == entry['sha256'], relative
        if relative == 'src/lib.rs' and relative not in actual:
            assert all(not x.strip() or x.startswith('//!') or x.startswith('pub mod ') for x in (PACKAGE/relative).read_text().splitlines())
            lines = {'count':0,'covered':0,'percent':0}
        else: lines = actual.pop(relative)
        rows.append({'path':relative,'covered':lines['covered'],'count':lines['count']})
    assert not actual, actual
    covered = sum(row['covered'] for row in rows)
    count = sum(row['count'] for row in rows)
    status = 'PASS' if covered*100 >= count*95 else 'FAIL'
    result = {'raw':str(raw),'raw_sha256':record.sha256(raw),'covered':covered,'count':count,'percent':covered*100/count,
        'status':status,'files':rows,'first_party_exclusions':[], 'branch':'NOT_RUN (no branch instrumentation selected; report separately)'}
    write('coverage-summary.json',result)
    print(json.dumps(result))
    sys.exit(0 if status == 'PASS' else 1)
elif sys.argv[1] == 'readback':
    before = json.loads((ROOT/'candidate-manifest.json').read_text())
    after = record.package_manifest()
    inputs = json.loads((ROOT/'selected-inputs-final.json').read_text())
    changed = [entry['path'] for entry in inputs if record.sha256(WORKSPACE/entry['path']) != entry['sha256']]
    write('candidate-readback.json',{'candidate_unchanged':before==after,'changed_selected_inputs':changed,'candidate':after})
    assert before == after and not changed
    print('Candidate and all selected inputs unchanged')
else:
    raise SystemExit('unknown operation')
