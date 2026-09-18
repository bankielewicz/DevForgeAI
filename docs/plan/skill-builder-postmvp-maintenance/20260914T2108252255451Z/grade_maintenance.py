"""Reduce complete required-case observations; never framework acceptance."""
import json
from pathlib import Path
import sys

root = Path(sys.argv[1])
expected = json.loads((root / 'expected.json').read_bytes())
observed = {}
for line in (root / 'results.jsonl').read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    observed.setdefault(row['case'], []).append(row['status'])
unknown = sorted(set(observed) - set(expected))
passed = sum(observed.get(case) == ['PASS'] for case in expected)
result = {'required': len(expected), 'passing': passed,
          'pass_percent': 100 * passed / len(expected),
          'nonpasses': {case: observed.get(case, ['NOT_RUN']) for case in expected if observed.get(case) != ['PASS']},
          'unknown_cases': unknown, 'kind': 'maintenance-evidence-only'}
(root / 'grade.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result))
sys.exit(0 if passed == len(expected) and not unknown else 1)
