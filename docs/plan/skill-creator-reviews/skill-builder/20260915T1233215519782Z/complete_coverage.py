"""Account for unimported Python files omitted by coverage's directory discovery."""
import json
from pathlib import Path
import coverage

RUN = Path(__file__).resolve().parent
scope = json.loads((RUN / 'scope.json').read_bytes())
cov = coverage.Coverage(data_file=str(RUN / '.coverage'))
cov.load()
rows = []
for relative in scope['coverage_files']:
    path = str(Path(scope['coverage_source']) / relative)
    filename, statements, excluded, missing, formatted = cov.analysis2(path)
    rows.append({'path': relative, 'statements': len(statements),
                 'covered': len(statements) - len(missing), 'missing': len(missing),
                 'exclusions': excluded})
total = sum(r['statements'] for r in rows)
covered = sum(r['covered'] for r in rows)
result = {'files': rows, 'total_statements': total, 'covered_statements': covered,
          'line_percent': 100 * covered / total, 'threshold': 95,
          'threshold_met': 100 * covered / total >= 95,
          'note': 'Same executed attempt; full denominator analysis only, no test retry.',
          'branch_scope': 'coverage.json covers measured modules only; full-package branch coverage NOT_RUN.'}
(RUN / 'full-source-coverage.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result))
