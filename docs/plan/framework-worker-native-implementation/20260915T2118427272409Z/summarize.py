"""Retain measured developer observations; never an acceptance authority."""
import json
import re
import sys
from pathlib import Path
from record import ROOT, PACKAGE, sha, write

if sys.argv[1] == 'declare':
    raw = (ROOT/'17-final-test-inventory/stdout.txt').read_text()
    tests = re.findall(r'^(.+): test$', raw, re.M)
    assert len(tests) == len(set(tests)), 'duplicate case names must be disambiguated'
    write('test-inventory.json', [{'name': n, 'status': 'NOT_RUN'} for n in tests])
    write('source-denominator.json', {'platform':'Windows x86_64',
        'required_line_floor':95, 'files':[str(p) for p in sorted((PACKAGE/'src').glob('*.rs'))],
        'exclusions':['tests and tests/support: synthetic fixtures and test code only', 'third-party dependency code'],
        'normalization':'Path.resolve() before src membership; src/../tests is test source',
        'measurement':'LLVM executed lines, every first-party executable file under src; module declarations have no executable lines',
        'branches':'NOT_RUN: unstable option not selected'})
    manifest = [{'path':str(p), 'bytes':p.stat().st_size, 'sha256':sha(p)}
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and 'target' not in p.relative_to(PACKAGE).parts]
    write('candidate-manifest.json', manifest)
    print(json.dumps({'tests':len(tests), 'candidate_files':len(manifest), 'manifest_sha256':sha(ROOT/'candidate-manifest.json')}))
elif sys.argv[1] == 'metrics':
    raw = (ROOT/'04-coverage/stdout.txt').read_text()
    observed = dict(re.findall(r'^test (.+) \.\.\. (ok|FAILED|ignored)$', raw, re.M))
    tests = [{**t, 'status':observed.get(t['name'],'NOT_RUN')} for t in json.loads((ROOT/'test-inventory.json').read_text())]
    data = json.loads((ROOT/'coverage.json').read_text())
    included=[]
    excluded=[]
    for block in data['data']:
        for item in block['files']:
            path = Path(item['filename']).resolve()
            if path.is_relative_to(PACKAGE/'src'):
                included.append({'path':str(path),'sha256':sha(path), 'lines':item['summary']['lines'],
                    'uncovered_segments':[s for s in item['segments'] if s[2]==0 and s[3]]})
            else:
                excluded.append({'path':str(path),'reason':'test fixture/support or dependency source'})
    covered=sum(i['lines']['covered'] for i in included)
    total=sum(i['lines']['count'] for i in included)
    passed=sum(t['status']=='ok' for t in tests)
    write('metrics.json',{'platform':'Windows x86_64','tests':tests,'passed':passed,'required_tests':len(tests),
        'pass_percentage':100*passed/len(tests), 'line_covered':covered,'line_count':total,
        'line_percentage':100*covered/total,'line_floor_met':covered*100>=total*95,
        'files':included,'exclusions':excluded,'branches':'NOT_RUN: no supported stable branch collector selected',
        'framework_acceptance':'NOT_EVALUATED'})
    manifest=json.loads((ROOT/'candidate-manifest.json').read_text())
    write('final-source-readback.json',[{**e,'actual_sha256':sha(e['path']),'unchanged':sha(e['path'])==e['sha256']} for e in manifest])
    print(json.dumps({'passed':passed,'tests':len(tests),'covered':covered,'lines':total,'percentage':100*covered/total}))
