import difflib,hashlib,json,pathlib
BASE=pathlib.Path(__file__).resolve().parent
ROOT=BASE.parents[3]
PKG=ROOT/'devforgeai/experiments/codex-worker-probe-logging'
OLD=ROOT/'docs/plan/framework-worker-diagnostics/20260916T181820Z-dev'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
old=json.loads((OLD/'candidate-v2-manifest.json').read_text())
for row in old:
    for tree in [ROOT/'devforgeai/experiments/codex-worker-probe',OLD/'candidate-v2-snapshot']:
        assert digest(tree/row['path'])==row['sha256'],tree/row['path']
bindings=json.loads((BASE/'input-bindings.json').read_text())
for b in bindings: assert digest(pathlib.Path(b['path']))==b['sha256'],b['path']
manifest=[{'path':p.relative_to(PKG).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(PKG.rglob('*')) if p.is_file() and 'target' not in p.parts]
diff=[]
for row in manifest:
    previous=OLD/'candidate-v2-snapshot'/row['path']; current=PKG/row['path']
    if previous.is_file() and digest(previous)==row['sha256']: continue
    try:
        before=previous.read_text().splitlines(keepends=True) if previous.exists() else []
        after=current.read_text().splitlines(keepends=True)
        diff.extend(difflib.unified_diff(before,after,fromfile='a/'+row['path'],tofile='b/'+row['path']))
    except UnicodeError: raise
verified={'original_source_files':len(old),'frozen_snapshot_files':len(old),'selected_inputs':len(bindings),'candidate_path':str(PKG.resolve()),'evidence_path':str(BASE.resolve()),'root_console_helper_sha256':digest(ROOT/'Start-CodexAppServerDiagnostic.ps1'),'native_codex_launched_by_this_development':False}
(BASE/'candidate-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(BASE/'candidate.patch').write_text(''.join(diff),encoding='utf-8',newline='\n')
(BASE/'preservation-readback.json').write_text(json.dumps(verified,indent=2)+'\n')
print(json.dumps({**verified,'candidate_files':len(manifest),'manifest_sha256':digest(BASE/'candidate-manifest.json')}))
