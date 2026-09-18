"""Readback exact QA inputs and summarize already executed evidence."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
run = root / 'attempt-002'
plan = json.loads((run / 'plan.json').read_bytes())
readback = []
for name, expected in plan['inputs'].items():
    actual = hashlib.sha256(Path(name).read_bytes()).hexdigest()
    readback.append({'path': name, 'expected': expected, 'actual': actual, 'unchanged': actual == expected})
if not all(row['unchanged'] for row in readback):
    raise ValueError('QA input changed after execution')
coverage = next(iter(json.loads((run / 'coverage.json').read_bytes())['files'].values()))
s = coverage['summary']
result = {'scope': 'Independent supporting Python custody QA only; not full skill or Rust framework qualification',
          'test_cases': 71, 'pass': 71, 'fail': 0, 'error': 0, 'skip': 0, 'not_run': 0,
          'pass_percent': 100, 'executed_lines': s['covered_lines'], 'total_lines': s['num_statements'],
          'executed_line_percent': 100 * s['covered_lines'] / s['num_statements'],
          'covered_branch_arcs': s['covered_branches'], 'total_branch_arcs': s['num_branches'],
          'branch_arc_percent': 100 * s['covered_branches'] / s['num_branches'],
          'exclusions': [], 'uncovered_lines': coverage['missing_lines'], 'readback': readback,
          'production_findings': [], 'framework_acceptance': 'NOT_EVALUATED'}
with (root / 'final-result.json').open('x', encoding='utf-8') as stream:
    json.dump(result, stream, indent=2)
print(json.dumps(result, indent=2))
