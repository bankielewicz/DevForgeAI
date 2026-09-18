"""Freeze the selected advisor candidate and preserve exact source identity."""
import hashlib
import json
from pathlib import Path

ROOT = Path('C:/Projects/DevForgeAI')
EVIDENCE = Path(__file__).resolve().parent
CANDIDATE = ROOT/'docs/plan/skill-authorings/advisor/20260916T134000Z-streaming/candidate'
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def rows(root):
    return [{'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
            for p in sorted(root.rglob('*')) if p.is_file()]

manifest_path = CANDIDATE/'artifact-manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
manifest['files'] = {row['path']:row['sha256'] for row in rows(CANDIDATE) if row['path'] != 'artifact-manifest.json'}
assert not any('__pycache__' in path for path in manifest['files'])
manifest['runtime'] = 'Native Windows, Python >=3.10 standard library; optional Windows PowerShell 5.1 or PowerShell 7 launcher; authenticated native Claude CLI for live reviews'
assert sha(Path(manifest['external_contract']['path'])) == manifest['external_contract']['sha256']
manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=True)+'\n', encoding='utf-8')
source = rows(CANDIDATE)
digest = hashlib.sha256(json.dumps(source, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
before = json.loads((ROOT/'docs/plan/skill-authorings/advisor/20260916T134000Z-streaming-intake/preservation-before.json').read_text())
operational = {row['path']:row['sha256'] for row in rows(ROOT/'.agents/skills/advisor')}
assert operational == before['operational']
assert sha(ROOT/'advisor-test.ps1') == before['example']['sha256']
result = {'candidate':str(CANDIDATE),'files':source,'package_digest':digest,
          'operational_unchanged':True,'user_example_unchanged':True,'git_metadata_present':(ROOT/'.git').exists()}
with (EVIDENCE/'candidate-freeze.json').open('x', encoding='utf-8') as out:
    json.dump(result,out,indent=2)
    out.write('\n')
print(json.dumps({'files':len(source),'package_digest':digest,'preservation':'PASS'}))
