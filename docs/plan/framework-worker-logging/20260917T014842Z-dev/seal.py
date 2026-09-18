import datetime,hashlib,json,pathlib,re
BASE=pathlib.Path(__file__).resolve().parent
ROOT=BASE.parents[3]
PKG=ROOT/'devforgeai/experiments/codex-worker-probe-logging'
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def binding(p):return {'path':str(p.resolve()),'bytes':p.stat().st_size,'sha256':digest(p)}
def write(name,value):
    with (BASE/name).open('x',encoding='utf-8',newline='\n') as f:json.dump(value,f,indent=2);f.write('\n')
manifest=json.loads((BASE/'candidate-manifest.json').read_text())
for r in manifest: assert digest(PKG/r['path'])==r['sha256'],r['path']
for attempt in ['23-full-coverage','24-windows-byte-capture','25-final-format','26-final-build','22-static-check']:
    receipt=json.loads((BASE/'attempts'/attempt/'receipt.json').read_text());assert receipt['exit_code']==0,attempt
    recorded=json.loads((BASE/'attempts'/attempt/'source-manifest.json').read_text())
    assert {r['path'].replace('\\','/'):r['sha256'] for r in recorded}=={r['path']:r['sha256'] for r in manifest},attempt
tests=json.loads((BASE/'test-analysis.json').read_text());coverage=json.loads((BASE/'coverage-analysis.json').read_text())
assert tests['required']==tests['passed']==152 and not tests['unexecuted'] and not tests['failed']
assert coverage['covered']*100>=coverage['total']*95
extra='real_windows_invalid_utf8_and_unterminated_line_preserve_exact_bytes'
extra_log=(BASE/'attempts/24-windows-byte-capture/stdout.txt').read_text()
assert f'test {extra} ... ok' in extra_log
write('suite-summary.json',{'scope':'Windows x64 offline development; no acceptance authority','candidate_manifest':binding(BASE/'candidate-manifest.json'),'package_required':152,'package_passed':152,'unit_required':49,'unit_passed':49,'supplemental_required':1,'supplemental_passed':1,'supplemental_case':extra,'overall_required':153,'overall_passed':153,'pass_percent':100,'line_coverage':coverage,'framework_acceptance':'NOT_EVALUATED','independent_qa':'NOT_RUN','native_codex':'NOT_RUN'})
bins=[BASE/'target/debug'/name for name in ['devforgeai-codex-worker-probe.exe','protocol-peer.exe','profile-peer.exe','protocol-edges-peer.exe','console-driver.exe','crash-driver.exe']]
write('binary-manifest.json',[binding(p) for p in bins])
prior=[('docs/plan/framework-worker-native-diagnostics/20260916T202125Z/artifact-index.json','1a22ca36d2fe92f86b7ebded1c6345db0d969ee39e600d5d79502fed1d708750'),('docs/plan/framework-worker-diagnostics-qa/20260916T191731Z/artifact-index.json','552912696c5260091a8cb2305b13d1f1987e53630b610dd66afec55f84d132d9')]
for name,sha in prior:assert digest(ROOT/name)==sha,name
write('prior-index-readback.json',[binding(ROOT/name) for name,_ in prior])
# Source/fixture/receipt/report artifacts are indexed. Compiler caches remain on disk;
# raw coverage profiles from BOTH the failed and successful campaigns are included.
paths=[]
for p in sorted(BASE.rglob('*')):
    if not p.is_file() or p.name in ['artifact-index.json','post-seal-readback.json']:continue
    relative=p.relative_to(BASE)
    if relative.parts[0]=='target' or relative.parts[0].startswith('coverage-target'):
        if p.suffix not in ['.profraw','.profdata']:continue
    paths.append(binding(p))
write('artifact-index.json',{'schema_version':1,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'evidence_only':True,'candidate_manifest':binding(BASE/'candidate-manifest.json'),'cache_exclusions':'Compiler caches retained but not indexed; raw coverage profiles included; compiled candidate binaries separately bound in binary-manifest.json','artifacts':paths})
for row in paths:assert digest(pathlib.Path(row['path']))==row['sha256'],row['path']
write('post-seal-readback.json',{'artifact_index':binding(BASE/'artifact-index.json'),'verified_artifacts':len(paths),'candidate_files_verified':len(manifest),'prior_indexes_verified':len(prior),'required_candidate_path':str(PKG),'observed_candidate_path':str(PKG.resolve()),'required_evidence_path':str(BASE),'observed_evidence_path':str(BASE.resolve())})
print(json.dumps({'verified_artifacts':len(paths),'candidate_files':len(manifest),'index_sha256':digest(BASE/'artifact-index.json'),'candidate_manifest_sha256':digest(BASE/'candidate-manifest.json')}))
