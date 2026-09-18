"""Stage selected integrity tests and test-resource cleanup maintenance."""
import hashlib
import json
from pathlib import Path

ROOT = Path('C:/Projects/DevForgeAI')
HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
TARGET = ROOT / 'src/agents/skills/advisor'


def ref(path):
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


task = '''# Selected maintenance request
The user requested five validate_prior_attempt rejection-path tests for these listed guards:
receipt versus raw output; launch record versus receipt; final envelope versus raw output;
unexpected extracted response; invalid stream receipt format. Each fixture must first be
accepted as pristine, mutate one semantic field (updating a dependent hash only when necessary
to reach the intended comparison), and assert the specific ValueError. Mutant guard removal
must be detected rather than relying on an unrelated earlier hash error.

Also fix the ResourceWarning from the flood-reader test instead of documenting it, and provide
an entry-point-excluded coverage view. Preserve the existing all-first-party baseline separately
so the requested exclusion does not alter or hide the >=95% aggregate-line requirement.
Reconcile evaluator scope by retaining unit-only coverage before appending the standalone JSONL run.
Do not chase unrelated streaming parser/type/timing coverage gaps. Development-only scope persists.
No live Claude call, operational installation, budget change, or production behavior change is requested.
Tests and retained evidence are explicitly authorized; independent skill validation remains separate.
'''
(HERE / 'task-capture.md').write_text(task, encoding='utf-8')
design = json.loads((PARENT / '20260916-cleanup-tests-intake/workflow-design.json').read_text())
design['source_refs'] = [ref(HERE / 'task-capture.md')]
design['behaviors'][0].update(
    id='integrity-tests', trigger='Run advisor integrity and stream-resource tests',
    inputs=['Pristine synthetic attempt files and one-field tampering; real flood-reader child'],
    completion='Five precise rejection assertions pass and kill their corresponding guard-removal mutants; no ResourceWarning remains in the full suite.',
    resource_paths=['tests/test_integrity.py', 'tests/test_streaming.py'],
    outputs=['Fresh regression, mutation and coverage evidence'],
    failure='Retain failed assertions and warning evidence; do not mask warnings or weaken checks.')
design['resources'] = [{
    'path': p, 'kind': 'helper', 'purpose': purpose, 'load_when': 'unittest discovers advisor tests',
    'helper_contract': {'inputs': 'Synthetic local evidence and real local process resources',
                        'outputs': 'Assertions and unittest status', 'runtime': 'Python >=3.10 standard library',
                        'effects': 'Temporary test files and owned child resources only',
                        'errors': 'Failed assertions remain visible', 'reuse_reason': 'Prevent evidence-integrity and resource-ownership regressions'}}
    for p, purpose in [('tests/test_integrity.py', 'Detect specific evidence tampering'),
                       ('tests/test_streaming.py', 'Own and release flood-test resources')]]
design['adverse_conditions'] = [{
    'id': 'tamper', 'behavior_id': 'integrity-tests',
    'condition': 'Receipt/artifact disagreement, stray advice or invalid stream format',
    'expected_observation': 'Exact ValueError before another invocation; preserved prior evidence',
    'requirement_basis': 'user-request'}]
write('workflow-design.json', design)
write('contract.json', {
    'schema_version': 'authoring-contract-v1', 'run_id': '20260916-integrity-tests',
    'project_root': str(ROOT), 'target_root': str(TARGET), 'target_name': 'advisor', 'operation': 'edit',
    'authorization': 'User requested tamper guard tests, ResourceWarning repair and entry-point coverage reporting. Development-only scope retained.',
    'history_review': 'Current 20-file source matches the published 20260916-cleanup-tests candidate.',
    'prior': ref(PARENT / '20260916-cleanup-tests/authoring-baseline.json'),
    'change_paths': ['tests/test_integrity.py', 'tests/test_streaming.py', 'evals/coverage-entrypoints.ini', 'references/evaluation.md', 'artifact-manifest.json'],
    'requirements': [{'origin': 'user', 'outcome': 'Five independent guard-rejection cases, warning-free resource fixture, baseline and diagnostic coverage reconciliation.',
                      'artifacts': ['tests/test_integrity.py', 'tests/test_streaming.py', 'evals/coverage-entrypoints.ini', 'references/evaluation.md', 'artifact-manifest.json']}],
    'capabilities': [], 'expected_outputs': ['Specific rejection assertions; warning-free tests; two labeled coverage views'],
    'side_effects': ['Temporary test files and owned synthetic process resources'],
    'inputs': [ref(HERE / 'task-capture.md'), ref(HERE / 'workflow-design.json')],
    'known_issues': ['Live Claude qualification and framework acceptance remain unevaluated.']
})
write('preservation-before.json', {
    'source': {p.relative_to(TARGET).as_posix(): ref(p)['sha256'] for p in TARGET.rglob('*') if p.is_file()},
    'operational': {p.relative_to(ROOT / '.agents/skills/advisor').as_posix(): ref(p)['sha256'] for p in (ROOT / '.agents/skills/advisor').rglob('*') if p.is_file()},
    'policy': ref(ROOT / 'AGENTS.md')
})
