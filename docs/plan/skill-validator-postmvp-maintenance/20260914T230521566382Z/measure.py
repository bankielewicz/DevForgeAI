"""Freeze artifact inventory and combine only exact-byte matching execution coverage."""
import argparse
import hashlib
import json
from pathlib import Path
import coverage

RUN = Path(__file__).resolve().parent
TARGET = RUN.parents[3] / 'src/agents/skills/skill-validator'
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path, value): path.write_text(json.dumps(value, indent=2), encoding='utf-8')
parser = argparse.ArgumentParser()
parser.add_argument('command', choices=['freeze','combine'])
parser.add_argument('name')
args = parser.parse_args()
folder = RUN / args.name
if args.command == 'freeze':
    folder.mkdir(exist_ok=False)
    (folder/'identities').mkdir()
    manifest_path = TARGET/'evals/build-manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    manifest['artifacts'] = {p.relative_to(TARGET).as_posix():sha(p) for p in sorted(TARGET.rglob('*'))
                             if p.is_file() and p != manifest_path and '__pycache__' not in p.parts}
    write(manifest_path, manifest)
    write(folder/'source.json',{str(p):sha(p) for p in sorted((TARGET/'scripts').glob('*.py'))})
    (folder/'coverage.ini').write_text('[run]\nbranch = True\nparallel = True\ninclude = */scripts/*.py\ndata_file = '+str(folder/'.coverage')+'\n',encoding='utf-8')
else:
    sources = json.loads((folder/'source.json').read_text())
    assert all(sha(Path(path)) == digest for path,digest in sources.items()), 'source changed during execution'
    by_identity = {(Path(path).name,digest):path for path,digest in sources.items()}
    combined = coverage.CoverageData(basename=str(folder/'combined'))
    combined.add_arcs({path:[] for path in sources})
    included, excluded = [], []
    for data_path in folder.glob('.coverage.*'):
        pid = data_path.name.split('.')[-2]
        identity_file = folder/'identities'/f'{pid}.json'
        identities = json.loads(identity_file.read_text()) if identity_file.exists() else {}
        data = coverage.CoverageData(basename=str(data_path)); data.read()
        for path in data.measured_files():
            target = by_identity.get((Path(path).name,identities.get(path)))
            if target:
                combined.add_arcs({target:data.arcs(path) or []})
                included.append(dict(data=data_path.name,source=path,target=target))
            else:
                excluded.append(dict(data=data_path.name,source=path,reason='No captured exact-byte source match'))
    combined.write()
    cov = coverage.Coverage(data_file=str(folder/'combined'));cov.load()
    cov.json_report(morfs=list(sources),outfile=str(folder/'coverage.json'))
    with (folder/'coverage.txt').open('w') as stream: cov.report(morfs=list(sources),file=stream)
    report=json.loads((folder/'coverage.json').read_text())
    totals=report['totals']
    write(folder/'measurement.json',dict(statements=totals['num_statements'],covered_lines=totals['covered_lines'],
          line_percent=100*totals['covered_lines']/totals['num_statements'],branches=totals['num_branches'],
          covered_branches=totals['covered_branches'],branch_percent=100*totals['covered_branches']/totals['num_branches'],
          included=included,excluded=excluded))
    print(json.dumps({k:v for k,v in json.loads((folder/'measurement.json').read_text()).items() if k not in ('included','excluded')},indent=2))
