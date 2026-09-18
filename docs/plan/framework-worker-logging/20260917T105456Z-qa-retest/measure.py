"""Independent recomputation from raw Cargo/LLVM reports; evidence only."""
import hashlib,json,re
from pathlib import Path
from decimal import Decimal
root=Path(__file__).resolve().parent
cases=json.loads((root/'required-cases.json').read_text())
raw=(root/'attempts/03-coverage/stdout.txt').read_text()
found=re.findall(r'^test ([\w:]+) \.\.\. (ok|FAILED|ignored)$',raw,re.M)
names=[n for n,_ in found]
expected=[c['name'] for c in cases if c['id'].startswith('PKG-')]
assert len(names)==len(set(names))==len(expected) and set(names)==set(expected),(len(names),len(expected),set(expected)-set(names))
outcomes=dict(found)
units=[c for c in cases if c['category']=='unit']
unit_pass=sum(outcomes[c['name']]=='ok' for c in units)
data=json.loads((root/'coverage.json').read_text())
eligible=json.loads((root/'source-denominator.json').read_text())
wanted={str(Path(v['path']).resolve()).lower() for v in eligible}
files=data['data'][0]['files']
observed={str(Path(v['filename']).resolve()).lower():v for v in files}
missing=wanted-set(observed)
extra=set(observed)-wanted
assert not extra,extra
assert missing<={str(Path(v['path']).resolve()).lower() for v in eligible if Path(v['path']).name=='lib.rs'},missing
counts=[{'path':v['filename'],'covered':v['summary']['lines']['covered'],'count':v['summary']['lines']['count']} for v in files]
covered=sum(v['covered'] for v in counts);denominator=sum(v['count'] for v in counts)
assert denominator>0
ratio=lambda a,b:str(Decimal(100)*a/b)
result={'platform':'Windows x64','collection':'complete unfiltered162-case campaign','per_file':counts,
'line_covered':covered,'line_count':denominator,'line_percent':ratio(covered,denominator),'line_floor_pass':100*covered>=95*denominator,
'unit_passed':unit_pass,'unit_required':len(units),'unit_percent':ratio(unit_pass,len(units)),'unit_floor_pass':100*unit_pass>=95*len(units),
'package_passed':sum(v=='ok' for v in outcomes.values()),'package_required':len(expected),
'candidate_manifest_sha256':hashlib.sha256((root/'candidate-manifest.json').read_bytes()).hexdigest(),
'coverage_sha256':hashlib.sha256((root/'coverage.json').read_bytes()).hexdigest(),
'branch_coverage':'NOT_RUN: collector marks branch unstable; only stable toolchains installed',
'declaration_only_omitted':sorted(missing)}
with (root/'coverage-analysis.json').open('x') as f:json.dump(result,f,indent=2)
for c in cases:
    if c['id'].startswith('PKG-'):
        c['status']='PASS' if outcomes[c['name']]=='ok' else 'FAIL'
        c['attempt']='03-coverage'
with (root/'package-results.json').open('x') as f:json.dump(cases[:162],f,indent=2)
print(json.dumps({k:v for k,v in result.items() if k!='per_file'},indent=2))
if not result['line_floor_pass'] or not result['unit_floor_pass']:
    with (root/'STOP.json').open('x') as f:json.dump({'trigger':'QA-METRIC-01','class':'METRIC_FAILURE','evidence':'coverage-analysis.json'},f)
    raise SystemExit(1)

