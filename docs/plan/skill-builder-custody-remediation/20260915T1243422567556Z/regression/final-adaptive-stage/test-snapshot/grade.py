"""Independently reduce retained JSONL evidence; no authority or retries."""
import hashlib
import json
from pathlib import Path
import sys
import jsonschema
RUN=Path(__file__).resolve().parent
out=RUN/sys.argv[1]
schema=json.loads((RUN/'result.schema.json').read_text())
expected=json.loads((out/'expected.json').read_text())
rows=[json.loads(line) for line in (out/'results.jsonl').read_text().splitlines()]
for row in rows:jsonschema.validate(row,schema)
ids=[row['case'] for row in rows]
assert len(ids)==len(set(ids)), 'duplicate case rows'
assert set(ids)<=set(expected), 'unexpected cases'
coverage=json.loads((out/'coverage.json').read_text())
scope=json.loads((out/'scope.json').read_text())
assert len(coverage['files'])==len(scope['files']), 'coverage source files omitted'
assert all(not item['excluded_lines'] for item in coverage['files'].values()), 'excluded source lines'
s=coverage['totals']
passed=sum(row['status']=='PASS' for row in rows)
result={'required':len(expected),'passed':passed,'unexecuted':sorted(set(expected)-set(ids)), 'nonpasses':[row['case'] for row in rows if row['status']!='PASS'],'pass_rate':100*passed/len(expected),'covered_lines':s['covered_lines'],'statements':s['num_statements'],'line_percent':100*s['covered_lines']/s['num_statements'],'branch_percent':100*s['covered_branches']/s['num_branches'],'inputs':{name:hashlib.sha256((out/name).read_bytes()).hexdigest() for name in ('results.jsonl','expected.json','coverage.json','scope.json')}}
result['thresholds_met']=result['pass_rate']>=95 and result['line_percent']>=95
result['mandatory_cases_passed']=not result['nonpasses'] and not result['unexecuted']
(out/'independent-grade.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result))
sys.exit(0 if result['thresholds_met'] and result['mandatory_cases_passed'] else 1)
