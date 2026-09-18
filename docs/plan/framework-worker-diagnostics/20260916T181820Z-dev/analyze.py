"""Measure recorded development evidence; this never issues framework acceptance."""
from record import ROOT, PACKAGE, digest, manifest, write
from decimal import Decimal
import difflib
import json
import re
import sys

FINAL = len(sys.argv) > 2 and sys.argv[2] == 'final'
PREFIX = 'final-' if FINAL else ''
INVENTORY_ATTEMPT = '20-final-inventory' if FINAL else '09-test-inventory'

if sys.argv[1] == 'inventory':
    listing = (ROOT/'attempts'/INVENTORY_ATTEMPT/'stdout.txt').read_text()
    cases = re.findall(r'^(.+): test$', listing, re.M)
    assert len(cases) == len(set(cases))
    baseline = json.loads((ROOT/'baseline-manifest.json').read_text())
    current = manifest()
    old = {e['path']:e for e in baseline}
    changed = [e['path'] for e in current if e['path'] not in old or e['sha256'] != old[e['path']]['sha256']]
    write(ROOT/f'{PREFIX}test-inventory.json', {'required_test_count':len(cases),'required_tests':cases,
        'source_denominator':[str(p) for p in sorted((PACKAGE/'src').glob('*.rs'))],
        'first_party_exclusions':[], 'branch_coverage':'NOT_RUN', 'changed_files':changed,
        'candidate_manifest_sha256':digest(ROOT/'attempts'/INVENTORY_ATTEMPT/'candidate.json')})
    with (ROOT/f'{PREFIX}candidate.diff').open('x',encoding='utf-8') as stream:
        for path in changed:
            old_path = ROOT/'baseline-snapshot'/path
            before = old_path.read_text().splitlines(keepends=True) if old_path.exists() else []
            after = (PACKAGE/path).read_text().splitlines(keepends=True)
            stream.writelines(difflib.unified_diff(before,after,fromfile='baseline/'+path,tofile='candidate/'+path))
    print(json.dumps({'required_tests':len(cases),'changed':changed}))
elif sys.argv[1] == 'coverage':
    coverage = json.loads((ROOT/f'{PREFIX}coverage.json').read_text())
    expected = {str(p.resolve()).lower(): p for p in (PACKAGE/'src').glob('*.rs')}
    files = []
    for data in coverage['data']:
        for entry in data['files']:
            filename = str(__import__('pathlib').Path(entry['filename']).resolve()).lower()
            if filename in expected:
                line = entry['summary']['lines']
                files.append({'path':str(expected[filename]),'covered':line['covered'],'count':line['count']})
    seen = {f['path'].lower() for f in files}
    # lib.rs has declarations only; LLVM can omit a zero-executable-line module.
    for missing in set(expected)-seen:
        assert expected[missing].name == 'lib.rs', missing
        files.append({'path':str(expected[missing]),'covered':0,'count':0})
    assert len(files) == len(expected)
    covered = sum(f['covered'] for f in files)
    count = sum(f['count'] for f in files)
    required = json.loads((ROOT/f'{PREFIX}test-inventory.json').read_text())['required_tests']
    test_runs = {}
    for attempt in (['21-final-offline','22-final-coverage'] if FINAL else ['12-full-offline','15-coverage']):
        stdout = (ROOT/'attempts'/attempt/'stdout.txt').read_text()
        passing = re.findall(r'^test (.+) \.\.\. ok$',stdout,re.M)
        assert len(passing) == len(set(passing))
        assert set(passing) == set(required), (attempt,set(required)-set(passing))
        assert not re.search(r'\d+ failed',stdout.replace('0 failed',''))
        receipt = json.loads((ROOT/'attempts'/attempt/'receipt.json').read_text())
        assert receipt['exit_code'] == 0
        test_runs[attempt] = {'passed':len(passing),'required':len(required),'percentage':'100',
                             'receipt_sha256':digest(ROOT/'attempts'/attempt/'receipt.json')}
    result = {'files':files,'covered':covered,'count':count,
        'percentage':str(Decimal(covered)*100/Decimal(count)),
        'floor_met':covered*100>=count*95,'excluded_first_party':[],
        'branch_coverage':'NOT_RUN','test_runs':test_runs,'raw_sha256':digest(ROOT/f'{PREFIX}coverage.json')}
    write(ROOT/f'{PREFIX}coverage-analysis.json',result)
    print(json.dumps(result))
