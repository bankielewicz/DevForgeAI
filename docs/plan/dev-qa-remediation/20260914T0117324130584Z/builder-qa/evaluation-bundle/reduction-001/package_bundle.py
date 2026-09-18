"""Create a fresh manifest and retained snapshots for the external helper bundle."""
import hashlib
import importlib.metadata
import json
from pathlib import Path
import sys
import reduce as r

root = Path(__file__).resolve().parent
qa = root.parent
remediation = qa.parent
project = remediation.parents[3]

def save(name, value):
    with (root / name).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2)

save('expected.json', {
    'HELPER-REGRESSIONS': {'required_count': 71},
    'VALIDATOR-REGRESSIONS': {'required_count': 292},
    'HELPER-COVERAGE': {'file': r'src\agents\skills\skill-builder\scripts\authoring.py', 'total_statements': 453, 'minimum_line_percent': 95},
})
scenarios = [
    {'id': 'HELPER-REGRESSIONS', 'kind': 'retained_unittest', 'receipt': 'helper_receipt', 'stderr': 'helper_stderr'},
    {'id': 'VALIDATOR-REGRESSIONS', 'kind': 'retained_unittest', 'receipt': 'regression_receipt', 'stderr': 'regression_stderr'},
    {'id': 'HELPER-COVERAGE', 'kind': 'retained_coverage', 'coverage': 'coverage'},
]
with (root / 'scenarios.jsonl').open('x', encoding='utf-8') as stream:
    for row in scenarios:
        stream.write(json.dumps(row) + '\n')
save('result-schema.json', {'$schema': 'https://json-schema.org/draft/2020-12/schema', 'type': 'object',
    'required': ['schema_version', 'case_id', 'status', 'assessment_kind', 'manifest_sha256', 'details', 'framework_acceptance'],
    'properties': {'schema_version': {'const': 'helper-evidence-result-v1'}, 'case_id': {'type': 'string'},
        'status': {'const': 'PASS'}, 'assessment_kind': {'const': 'retained_evidence_reduction'},
        'manifest_sha256': {'type': 'string', 'pattern': '^[0-9a-f]{64}$'}, 'details': {'type': 'object'},
        'framework_acceptance': {'const': 'NOT_EVALUATED'}}, 'additionalProperties': False})
save('runtime.json', {'python': sys.version, 'platform': sys.platform, 'runner_dependencies': {'jsonschema': importlib.metadata.version('jsonschema')},
    'underlying_qa_dependencies': {'coverage': importlib.metadata.version('coverage'), 'PyYAML': importlib.metadata.version('PyYAML')},
    'installation': 'No installation performed; existing runtime only.'})
paths = {'helper_receipt': qa / 'attempt-002/0-receipt.json', 'helper_stderr': qa / 'attempt-002/0-stderr.txt',
         'regression_receipt': remediation / 'commands/regression-001/receipt.json', 'regression_stderr': remediation / 'commands/regression-001/stderr.txt',
         'coverage': qa / 'attempt-002/coverage.json', 'raw_coverage': qa / 'attempt-002/coverage.data',
         'scenarios': root / 'scenarios.jsonl', 'expected': root / 'expected.json', 'result_schema': root / 'result-schema.json',
         'runtime': root / 'runtime.json', 'runner': root / 'reduce.py', 'runner_tests': root / 'test_reduce.py',
         'synthetic_fixture_expectations': root / 'test_reduce.py', 'qa_plan': qa / 'attempt-002/plan.json', 'readback': qa / 'final-result.json'}
builder = project / 'src/agents/skills/skill-builder'
builder_rows = r.package_rows(builder)
for package in ('skill-builder', 'skill-validator'):
    source = project / 'src/agents/skills' / package
    for row in r.package_rows(source):
        name = row['path']
        current = source / name
        paths[package + ':' + name] = current
        copy = root / 'snapshots' / package / name
        copy.parent.mkdir(parents=True, exist_ok=True)
        with copy.open('xb') as stream:
            stream.write(current.read_bytes())
        paths['snapshot:' + package + ':' + name] = copy
artifacts = [{'id': name, 'reference': {'path': str(path), 'sha256': r.sha(path.read_bytes())}} for name, path in sorted(paths.items())]
save('manifest.json', {'schema_version': 'helper-evaluation-bundle-v1', 'scope': 'Retained supporting-helper QA and validator regression evidence only; no native skill or framework qualification',
     'builder_root': str(builder), 'builder_files': builder_rows,
     'builder_package_digest': r.sha(json.dumps(builder_rows, ensure_ascii=False, separators=(',', ':')).encode()),
     'artifacts': artifacts, 'case_overlap': 'The 71 helper cases occur within the 292 full-suite cases; reductions are not additive test counts.'})
print(r.sha((root / 'manifest.json').read_bytes()))
