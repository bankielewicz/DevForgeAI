"""Combine retained coverage without deleting inputs or excluding source lines."""
import json
import coverage
from evidence import RUN

output = RUN / 'coverage-maintenance'
assert not output.exists()
cov = coverage.Coverage(data_file=str(output), source=[str(RUN.parents[3]/'src/agents/skills/skill-builder')], branch=True)
cov.combine(data_paths=[str(RUN/'coverage-focused-02'), str(RUN/'regression-01/coverage-data')], strict=True, keep=True)
cov.save()
cov.json_report(outfile=str(RUN/'coverage-maintenance.json'))
value = json.loads((RUN/'coverage-maintenance.json').read_text())
for name, data in value['files'].items():
    s = data['summary']
    print(name, s['covered_lines'], '/', s['num_statements'], 'missing', data['missing_lines'])
s = value['totals']
print('TOTAL', s['covered_lines'], '/', s['num_statements'], 'LINE', 100*s['covered_lines']/s['num_statements'], 'BRANCH', s['covered_branches'], '/', s['num_branches'])
