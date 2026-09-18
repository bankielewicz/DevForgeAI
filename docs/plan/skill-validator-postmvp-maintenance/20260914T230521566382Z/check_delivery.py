"""Byte-bound delivery, syntax and documentation checks. No acceptance authority."""
import hashlib,json,shutil,sys
from pathlib import Path
RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[3]
TARGET=ROOT/'src/agents/skills/skill-validator'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,value):path.write_text(json.dumps(value,indent=2),encoding='utf-8')
preservation=json.loads((RUN/'preservation.json').read_text())
drift=[row['path'] for row in preservation if not Path(row['path']).is_file() or sha(Path(row['path']))!=row['sha256']]
assert not drift,drift
files={p.relative_to(TARGET).as_posix():sha(p) for p in TARGET.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
before={p.relative_to(RUN/'before').as_posix():sha(p) for p in (RUN/'before').rglob('*') if p.is_file() and '__pycache__' not in p.parts}
syntax=[]
for p in (TARGET/'scripts').glob('*.py'):
    compile(p.read_bytes(),str(p),'exec');syntax.append(str(p))
catalog=json.loads((TARGET/'assets/standards-catalog.json').read_text())
for row in catalog['sources']:
    assert sha(ROOT/'docs/Agentskills'/row['document'])==row['sha256']
manifest=json.loads((TARGET/'evals/build-manifest.json').read_text())
assert manifest['artifacts']=={k:v for k,v in files.items() if k!='evals/build-manifest.json'}
delivery=RUN/(sys.argv[1] if len(sys.argv)>1 else 'delivery')
delivery.mkdir(exist_ok=False)
shutil.copytree(TARGET,delivery/'source',ignore=shutil.ignore_patterns('__pycache__'))
shutil.copyfile(ROOT/'docs/specs/skill-validator-postmvp-spec.md',delivery/'specification.md')
write(delivery/'source-manifest.json',files)
write(delivery/'checks.json',dict(preserved_files=len(preservation),preservation_drift=drift,
     syntax_checked=syntax,standards_sources=len(catalog['sources']),build_manifest='PASS',
     changed=[k for k,v in files.items() if before.get(k)!=v],removed=sorted(set(before)-set(files))))
print(json.dumps(dict(preserved_files=len(preservation),changed=len([k for k,v in files.items() if before.get(k)!=v]),syntax=len(syntax))))
