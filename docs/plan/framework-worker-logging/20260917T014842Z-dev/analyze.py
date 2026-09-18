import hashlib,json,pathlib,re,sys
BASE=pathlib.Path(__file__).resolve().parent
ROOT=BASE.parents[3]
PKG=ROOT/'devforgeai/experiments/codex-worker-probe-logging'
inventory=(BASE/'attempts/16-case-inventory/stdout.txt').read_text()
required=re.findall(r'^(.+): test$',inventory,re.M)
log=(BASE/'attempts'/sys.argv[1]/'stdout.txt').read_text()
passed=re.findall(r'^test (.+) \.\.\. ok$',log,re.M)
failed=re.findall(r'^test (.+) \.\.\. (FAILED|ignored)',log,re.M)
assert len(set(required))==len(required), 'duplicate case names require binary-qualified mapping'
result={'required':len(required),'passed':len(passed),'failed':failed,'unexecuted':sorted(set(required)-set(passed)),'pass_rate':len(passed)*100/len(required),'units_required':49,'required_cases':required}
(BASE/'test-analysis.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='required_cases'}))
if (BASE/'coverage.json').exists():
    data=json.loads((BASE/'coverage.json').read_text())
    files=[]
    for row in data['data'][0]['files']:
        path=pathlib.Path(row['filename'])
        assert path.parent.resolve()==(PKG/'src').resolve(), str(path)
        files.append({'path':str(path.relative_to(PKG)),'lines':row['summary']['lines']})
    covered=sum(r['lines']['covered'] for r in files);total=sum(r['lines']['count'] for r in files)
    result={'covered':covered,'total':total,'percent':100*covered/total,'threshold_pass':100*covered>=95*total,'files':files,'source_inventory':[str(p.relative_to(PKG)) for p in sorted((PKG/'src').glob('*.rs'))],'exclusions':'tests and fixture binaries; dependencies; no first-party src exclusions','branches':'NOT_RUN: only stable Windows Rust toolchains installed; collector branch flag is unstable'}
    assert set(r['path'] for r in files) <= set(result['source_inventory'])
    assert set(result['source_inventory'])-set(r['path'] for r in files) <= {str(pathlib.Path('src/lib.rs'))}, 'executable source omitted'
    (BASE/'coverage-analysis.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
