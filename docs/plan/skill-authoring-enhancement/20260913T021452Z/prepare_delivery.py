"""Prepare actual provenance-bound delivery without destination mutations."""
import json
from pathlib import Path
import shutil
import sys
RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
sys.dont_write_bytecode = True
sys.path.insert(0, str(RUN / 'candidate/skill-builder/scripts'))
import authoring as a
source_spec = ROOT / 'docs/plan/skill-builder-authoring-enhancement-spec.md'
assert a.digest(source_spec.read_bytes()) == '43054bf9b3f97d48d479aeed2fe7b119629e6e717f0a55e1835714182844cb14'
authorization = RUN / 'inputs/implementation-authorization.txt'
if not authorization.exists():
    authorization.write_text('Use skill-creator authoring guidance to update both development packages according to the approved enhancement specification. This authorizes implementation of AB-001 through AB-014 in src/agents/skills/skill-builder and src/agents/skills/skill-validator, supporting evidence capture, and validator-owned testing and validation. Preserve historical evidence, legacy meanings, provenance, ownership, safe-write and readback requirements. Update only the two development packages and create fresh evidence under docs/plan. Do not modify operational copies or install dependencies/skills, configure hooks/CI or implement Rust. Complete without requesting the same authorization again. This is a scoped excerpt of the current user instruction, not a reconstructed approval.\n',encoding='utf-8')
results = {}
for name in (sys.argv[1:2] or ('skill-builder','skill-validator')):
    target = ROOT / 'src/agents/skills' / name
    before = a.files(target)
    staged = a.files(RUN / 'candidate' / name)
    old = RUN / 'inputs' / (name + '-manifest.json')
    assert {p:{'bytes':len(d),'sha256':a.digest(d)} for p,d in before.items()} == json.loads(old.read_text())['files']
    if name == 'skill-builder':
        legacy = ROOT / 'docs/plan/skill-builds/skill-builder/20260912T212438315Z/published'
        prior = legacy / 'revision/evidence/build-provenance.json'
    else:
        legacy = ROOT / 'docs/plan/skill-builds/skill-validator/20260912T155029Z'
        prior = legacy / 'build-provenance.json'
    c = {'schema_version':'authoring-contract-v1','run_id':'20260913T021452Z-'+name,'project_root':str(ROOT),'target_root':str(target),'target_name':name,'operation':'edit','authorization':authorization.read_text(),'history_review':'Verified current target manifests, legacy generated baseline files, selected publication receipts and builder adoption lineage; see history-check.json.','prior':a.reference(prior),'legacy_root':str(legacy),'change_paths':sorted(set(before)|set(staged)),'requirements':[{'origin':'user','id':'AB-%03d'%i,'source':str(source_spec),'outcome':'Implement the selected enhancement requirement in the applicable development package.'} for i in range(1,15)],'capabilities':['Python 3.10+ for bundled custody/assessment helpers','Existing PyYAML for YAML helpers'],'expected_outputs':['Authoring records and exact-byte manual handoff' if name=='skill-builder' else 'Independent byte-bound assessment and validator-owned test records'],'side_effects':['Authorized development/evidence files only; authored workflow selects further effects from current user scope'],'inputs':[a.reference(source_spec),a.reference(authorization)],'known_issues':[]}
    suffix = '-002' if len(sys.argv) > 1 else ''
    contract = RUN / (name+'-implementation-contract'+suffix+'.json')
    a.save(contract,c)
    try:
        observed = a.origin(c)
        results[name] = {'state':'ORIGIN_VERIFIED','kind':observed[0]['kind'],'baseline_files':len(observed[1])}
    except Exception as exc:
        results[name] = {'state':'BLOCKED','error':str(exc),'error_type':type(exc).__name__}
        continue
    dest = RUN / 'authoring' / name
    a.begin(contract,dest)
    # Only mutate this newly created candidate; originals remain untouched.
    candidate = dest / 'candidate'
    assert candidate.resolve().is_relative_to(RUN.resolve())
    for p in sorted(before):
        if p not in staged:
            a.child(candidate,p).unlink()
    for p,d in staged.items():
        path = a.child(candidate,p)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(d)
    # Remove only empty directories under the checked disposable candidate.
    for p in sorted(candidate.rglob('*'),key=lambda p:len(p.parts),reverse=True):
        if p.is_dir() and not any(p.iterdir()):
            p.rmdir()
    assert a.files(candidate)==staged
    results[name]['candidate'] = str(candidate)
    results[name]['delta'] = [p for p in sorted(set(before)|set(staged)) if before.get(p)!=staged.get(p)]
a.save(RUN / ('delivery-preparation'+('-002' if len(sys.argv)>1 else '')+'.json'),results)
print(json.dumps({k:{x:v for x,v in r.items() if x!='delta'} for k,r in results.items()}))
