import datetime, hashlib, importlib.util, json, pathlib, platform, shutil, sys
ROOT=pathlib.Path('C:/Projects/DevForgeAI')
RUN=ROOT/'docs/plan/skill-validations/skill-builder/20260912T161842Z'
VALIDATOR=ROOT/'src/agents/skills/skill-validator'
BUILD=ROOT/'docs/plan/skill-builds/skill-validator/20260912T155029Z'
PRIOR=ROOT/'docs/plan/skill-builder-adoption-verification-20260912'
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('observer',VALIDATOR/'scripts/observe.py'); mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
rows=[]
def copy(src,dest,expected=None):
    src=mod.safe_path(src); data=mod.read_stable(src); digest=hashlib.sha256(data).hexdigest()
    if expected and digest!=expected: raise ValueError('digest mismatch '+str(src))
    dest=RUN/dest;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    assert dest.read_bytes()==data
    rows.append({'original_path':str(src),'retained_path':dest.relative_to(RUN).as_posix(),'sha256':digest,'bytes':len(data)})
def tree(src,dest):
    files,excluded=mod.inventory(mod.safe_path(src))
    if excluded: raise ValueError(str(excluded))
    for rel,path,info in files: copy(path,pathlib.Path(dest)/rel)
    return mod.make_manifest(mod.safe_path(src))
validator_manifest=tree(VALIDATOR,'inputs/validator')
(RUN/'inputs/validator-manifest.json').write_text(json.dumps(validator_manifest,indent=2)+'\n',encoding='utf-8')
copy(pathlib.Path('C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py'),'inputs/quick_validate.py')
for name in ['skill-builder-adoption-spec.md','skill-builder-enhancement-spec.md','claude-to-codex-skill-import-spec.md']:
    copy(ROOT/'docs/plan'/name,'inputs/specs/'+name)
copy(BUILD/'publication-receipt.json','inputs/validator-publication-receipt.json')
publication=json.loads((BUILD/'publication-receipt.json').read_text())
for key in ['provenance','evaluated_provenance','final_results']:
    r=publication[key];copy(BUILD/r['path'],'inputs/validator-build/'+r['path'],r['sha256'])
copy(PRIOR/'FINAL-RECEIPT.json','inputs/prior/FINAL-RECEIPT.json')
receipt=json.loads((PRIOR/'FINAL-RECEIPT.json').read_text())
for r in receipt['selected_evidence']:
    src=(PRIOR/r['path']).resolve();copy(src,'inputs/prior-selected/'+src.relative_to(ROOT/'docs/plan').as_posix(),r['sha256'])
prior_manifest=tree(PRIOR/'builder-final-release','inputs/prior-builder-final-release')
current=json.loads((RUN/'source-manifest.json').read_text())
(RUN/'observations').mkdir()
(RUN/'observations/prior-byte-comparison.json').write_text(json.dumps({'same_file_rows':current['files']==prior_manifest['files'],'current_package_digest':current['package_digest'],'prior_package_digest':prior_manifest['package_digest'],'history_claim':'Verified enhancement snapshot match only; not generated or adopted baseline.'},indent=2)+'\n')
copy(BUILD/'guidance/sources.json','inputs/build-guidance-sources.json')
sources=[]
for r in json.loads((BUILD/'guidance/sources.json').read_text())['sources']:
    if r['source_id'] not in ['openai-skills','agent-skills']: continue
    copy(BUILD/r['snapshot_path'],r['snapshot_path'],r['sha256']);r['freshness']='snapshot_only';sources.append(r)
(RUN/'guidance-sources-selected.json').write_text(json.dumps({'sources':sources},indent=2)+'\n')
(RUN/'input-capture-manifest.json').write_text(json.dumps({'schema_version':'1','captured_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':rows},indent=2)+'\n')
import yaml
(RUN/'environment.json').write_text(json.dumps({'os':platform.platform(),'python':sys.version,'python_executable':sys.executable,'pyyaml':yaml.__version__,'shell':'PowerShell 7','host':'Codex collaboration task tools available; target workflow execution prohibited in this task','checker_original':'C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py','effects':'All assessment writes under fresh run; target and evaluator packages read-only; no dependency installation'},indent=2)+'\n')
print(json.dumps({'retained_input_files':len(rows),'prior_byte_match':current['files']==prior_manifest['files']}))
