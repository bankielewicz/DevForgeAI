"""All-source line and branch coverage for final-byte Windows maintenance."""
import json
import sys
import coverage
from evidence import RUN, PACKAGE, identity, dump, sha

label = sys.argv[1]
inputs = [RUN/name for name in ('coverage-release-focused-02','coverage-release-legacy','coverage-release-edges','regression-release/coverage-data','coverage-release-runtime')]
inputs.extend(RUN/name for name in sys.argv[2:])
output = RUN/label
assert not output.exists() and not output.with_suffix('.json').exists()
dump(RUN/(label+'-plan.json'), {'platform':'Windows','source':identity(),'denominator':'All executable lines in all eight first-party Python files, including runtime template and record_schema; zero exclusions. Branches separate.','inputs':[{'path':str(p),'sha256':sha(p.read_bytes())} for p in inputs],'line_threshold':95,'evidence_scope':'Maintenance helper tests; not complete BAT acceptance.'})
cov=coverage.Coverage(data_file=str(output),source=[str(PACKAGE)],branch=True)
cov.combine(data_paths=[str(p) for p in inputs],strict=True,keep=True)
cov.save()
cov.json_report(outfile=str(output)+'.json')
value=json.loads((RUN/(label+'.json')).read_text())
for name,data in value['files'].items():
    print(name, data['summary']['covered_lines'],'/',data['summary']['num_statements'],'missing',data['missing_lines'])
s=value['totals']
print('TOTAL',s['covered_lines'],'/',s['num_statements'],'LINE',100*s['covered_lines']/s['num_statements'],'BRANCH',s['covered_branches'],'/',s['num_branches'])
