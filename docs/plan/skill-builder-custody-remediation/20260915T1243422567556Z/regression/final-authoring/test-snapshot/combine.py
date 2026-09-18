"""Disjoint final case inventory; retain superseded attempts separately."""
import hashlib
import json
from pathlib import Path
import sys
import coverage
RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[4]
PACKAGE=ROOT/'src/agents/skills/skill-builder'
out=RUN/sys.argv[1]
out.mkdir(exist_ok=False)
inputs=sys.argv[2:]
rows=[];expected={};sources=[]
for name in inputs:
    folder=RUN/name
    scope=json.loads((folder/'scope.json').read_text())
    sources.append(scope['source'])
    selected=[json.loads(line) for line in (folder/'results.jsonl').read_text().splitlines()]
    wanted=json.loads((folder/'expected.json').read_text())
    if name=='qa-01':
        prefixes=('test_remediation.','test_legacy_maintenance.','test_acceptance_edges.','test_final_contract_edges.')
        selected=[r for r in selected if r['case'].startswith(prefixes)]
        wanted={k:v for k,v in wanted.items() if k.startswith(prefixes)}
    assert not set(expected)&set(wanted),'overlapping final case inventory'
    expected.update(wanted);rows.extend(selected)
assert all(s==sources[0] for s in sources),'changed source across attempts'
actual={p.relative_to(PACKAGE).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in PACKAGE.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
assert actual==sources[0],'source changed since execution'
cov=coverage.Coverage(data_file=str(out/'coverage-data'),source=[str(PACKAGE)],branch=True)
cov.set_option('report:exclude_lines',[])
cov.combine([str(RUN/name/'coverage-data') for name in inputs],keep=True,strict=True)
cov.get_data().touch_files([str(p.resolve()) for p in PACKAGE.rglob('*.py')]);cov.save()
cov.json_report(outfile=str(out/'coverage.json'))
(out/'results.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows),encoding='utf-8')
(out/'expected.json').write_text(json.dumps(expected,indent=2),encoding='utf-8')
(out/'scope.json').write_text(json.dumps({'source':actual,'files':[str(p.relative_to(PACKAGE)) for p in PACKAGE.rglob('*.py')],'inputs':inputs,'selection':'qa-01 first four unchanged passing modules; remaining selected module attempts disjoint. All earlier failures retained, never counted as new cases. Coverage includes every executed line from same unchanged source; no exclusions.'},indent=2),encoding='utf-8')
print(json.dumps({'cases':len(rows),'coverage_files':len(cov.get_data().measured_files())}))
