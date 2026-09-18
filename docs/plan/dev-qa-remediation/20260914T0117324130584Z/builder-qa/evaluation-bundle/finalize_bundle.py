"""Bind the completed reduction and runner development attempts without rerunning QA."""
import json
from pathlib import Path
import reduce as r

root = Path(__file__).resolve().parent
output = (root / 'reduction-002/stdout.txt').read_bytes()
rows = [json.loads(line) for line in output.decode().splitlines() if line]
if len(rows) != 3 or any(row['status'] != 'PASS' for row in rows):
    raise ValueError('incomplete reduction')
with (root / 'results.jsonl').open('xb') as stream:
    stream.write(output)
files = ['manifest-v2.json', 'results.jsonl', 'reduce.py', 'test_reduce.py', 'runtime.json',
         'expected-v2.json', 'scenarios.jsonl', 'result-schema.json']
for attempt in ('red-001', 'red-002', 'green-001', 'reduction-001', 'green-002', 'reduction-002'):
    files.extend(str(p.relative_to(root)) for p in (root / attempt).iterdir() if p.is_file())
refs = [{'path': str(root / name), 'sha256': r.sha((root / name).read_bytes())} for name in sorted(files)]
receipt = {'schema_version': 'helper-evaluation-receipt-v1', 'state': 'EVIDENCE_REDUCED',
           'case_results': rows, 'references': refs,
           'test_accounting': 'Eight reducer tests PASS in green-002; repeated attempts preserve history and do not inflate denominator. Helper71 are contained in full regression292.',
           'limitations': ['Retained-execution evidence reduction; not fresh native skill execution.', 'Full skill behavioral qualification not performed by this bundle.', 'No installation or operational changes.', 'Framework acceptance NOT_EVALUATED.']}
with (root / 'FINAL-RECEIPT.json').open('x') as stream:
    json.dump(receipt, stream, indent=2)
print(json.dumps({'receipt_sha256': r.sha((root / 'FINAL-RECEIPT.json').read_bytes()), 'manifest_sha256': r.sha((root / 'manifest-v2.json').read_bytes()), 'results_sha256': r.sha(output)}))
