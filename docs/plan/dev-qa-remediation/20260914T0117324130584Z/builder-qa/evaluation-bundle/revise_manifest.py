"""Preserve v1 and bind corrected statement-accounting reduction as v2."""
import coverage
import json
from pathlib import Path
import reduce as r

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'manifest.json').read_bytes())
expected = json.loads((root / 'expected.json').read_bytes())
c = coverage.Coverage(data_file=str(root.parent / 'attempt-002/coverage.data'))
c.load()
analysis = c.analysis2(str(Path(manifest['builder_root']) / 'scripts/authoring.py'))
expected['HELPER-COVERAGE']['statement_lines'] = analysis[1]
with (root / 'expected-v2.json').open('x') as stream:
    json.dump(expected, stream, indent=2)
manifest['previous_manifest'] = {'path': str(root / 'manifest.json'), 'sha256': r.sha((root / 'manifest.json').read_bytes())}
manifest['revision_reason'] = 'Count covered executable statements; coverage traced line1 module docstring is not in the statement denominator. Retain initial failed reduction.'
for row in manifest['artifacts']:
    if row['id'] == 'expected':
        row['reference']['path'] = str(root / 'expected-v2.json')
    if row['id'] in {'expected', 'runner', 'runner_tests', 'synthetic_fixture_expectations'}:
        row['reference']['sha256'] = r.sha(Path(row['reference']['path']).read_bytes())
with (root / 'manifest-v2.json').open('x') as stream:
    json.dump(manifest, stream, indent=2)
print(r.sha((root / 'manifest-v2.json').read_bytes()))
