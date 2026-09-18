import datetime, json, re
from bootstrap import ROOT, PROJECT, write, inventory, digest
from verification import reference

target=PROJECT/'src/agents/skills/skill-validator'
manifest=inventory(target); expected=json.loads((ROOT/'destination-manifest.json').read_text())
assert manifest['files']==expected['files']
assert manifest['files']==inventory(ROOT/'generated-baseline')['files']
provenance=json.loads((ROOT/'build-provenance.json').read_text())
assert provenance['result']=='COMPLETE'
assert provenance['contract_sha256']==digest((ROOT/'build-contract.json').read_bytes())
assert {r['path']:r['sha256'] for r in provenance['outputs']}=={r['path']:r['sha256'] for r in manifest['files']}
for row in provenance['outputs']:
    assert digest((ROOT/row['baseline_path']).read_bytes())==row['baseline_sha256']
for row in provenance['evidence']:
    assert digest((ROOT/row['path']).read_bytes())==row['sha256']
evaluators=[]
for name in ['candidate-001','delivered-001','final-publication-001']:
    folder=ROOT/'evaluations'/name; root=folder/'snapshot'
    before=json.loads((folder/'input-before-manifest.json').read_text())
    assert inventory(root)['files']==before['files']
    observed=[]
    for row in [json.loads(l) for l in (folder/'results.jsonl').read_text().splitlines()]:
        assert row['cases_sha256']==digest((folder/'cases.jsonl').read_bytes())
        assert row['profile']=='spec-v1' and row['expectation_met'] and row['status']=='PASS'
        for path,sha in row['candidate_digests'].items(): assert digest((root/path).read_bytes())==sha
        observed.append({'case_id':row['case_id'],'measured_files':len(row['candidate_digests']),'status':row['status']})
    evaluators.append({'name':name,'observations':observed,'input_snapshot_unchanged':True,'case_file_unchanged':True})
links=[]
for file in ['build-report.md']:
    for match in re.finditer(r'\[[^\]]+\]\(([^)]+)\)',(ROOT/file).read_text()):
        path=match[1]
        if '://' in path: continue
        assert (ROOT/path.split('#')[0]).exists(), path
        links.append(path)
assert len(json.loads((ROOT/'acceptance-case-observations.json').read_text())['cases'])==20
contract=json.loads((ROOT/'build-contract.json').read_text())
for row in contract['inputs']: assert digest(__import__('pathlib').Path(row['resolved_path']).read_bytes())==row['sha256']
for before,path in [('builder-before-manifest.json',PROJECT/'.agents/skills/skill-builder'),('development-builder-before-manifest.json',PROJECT/'src/agents/skills/skill-builder'),('preserved-blocked-build-manifest.json',PROJECT/'docs/plan/skill-builds/skill-validator/20260912T140148003Z')]: assert inventory(path)['files']==json.loads((ROOT/before).read_text())['files']
write(ROOT/'delivery-audit.json',{'audited_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'package_files':len(manifest['files']),'package_bytes':sum(r['bytes'] for r in manifest['files']),'package_digest':digest(json.dumps(manifest['files'],ensure_ascii=False,separators=(',',':')).encode()),'evaluators':evaluators,'report_links_checked':len(links),'provenance':reference(ROOT/'build-provenance.json'),'source_inputs_and_protected_existing_packages_unchanged':True,'result':'MATCH','authority':'NONE'})
print(json.dumps({'audit':'MATCH','files':len(manifest['files']),'evaluators':len(evaluators),'report_links':len(links)}))
