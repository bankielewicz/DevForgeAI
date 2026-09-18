"""Prepare a test-only maintenance stage without changing runtime policy."""
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


task = '''# User request
Add focused tests for the uncovered cleanup and failure paths, while keeping the current coverage policy unchanged.
- Exercise real failure handling with meaningful assertions.
- Keep production code unchanged unless a test demonstrates a defect.
- Run existing regressions to check compatibility.
- Preserve the current >=95% aggregate line requirement; report branch and per-file gaps transparently.

Scope remains development source only. Operational promotion was performed by the user previously;
it does not authorize this task to edit .agents. This is explicitly authorized test maintenance,
not independent skill validation or a live Claude review. The user's test request takes precedence
over the skill-builder authoring-only test restriction. Existing policy denominator is scripts/ plus
evals/ Python executable lines; report branch coverage separately without adding a branch/per-file gate.
Tests first exercise unchanged production code. If behavior is already correct, preserve it and do
not invent a red phase. Retain any genuine failures and only repair demonstrated defects.
'''
(HERE / 'task-capture.md').write_text(task, encoding='utf-8')
design = {
    'schema_version': 'authoring-design-v1', 'target_name': 'advisor',
    'source_refs': [ref(HERE / 'task-capture.md')],
    'behaviors': [{
        'id': 'cleanup-evidence', 'requirement_ids': ['user-request'],
        'trigger': 'Run the advisor Python maintenance test suite',
        'inputs': ['Real local Python children, pipes and queues with controlled failure injection'],
        'completion': 'Assertions verify raw evidence retention, truthful errors, bounded cleanup and denial of advice after failure.',
        'outputs': ['unittest results and coverage in a fresh evidence directory'],
        'resource_paths': ['tests/test_cleanup.py'],
        'prerequisites': ['Native Windows Python >=3.10'],
        'effects': ['Temporary synthetic processes and files; owned resources cleaned in finally'],
        'failure': 'Retain failing assertions; do not weaken or replace actual cleanup behavior.',
        'recovery': 'Investigate retained results and fix production only when a test establishes a defect.'
    }],
    'resources': [{'path': 'tests/test_cleanup.py', 'kind': 'helper',
                   'purpose': 'Exercise cleanup and failure boundaries without running Claude',
                   'load_when': 'unittest discovers advisor tests',
                   'helper_contract': {'inputs': 'Synthetic process and OS fault fixtures',
                                       'outputs': 'Executed assertions and unittest exit status',
                                       'runtime': 'Python >=3.10 standard library',
                                       'effects': 'Local child processes and temporary pipes only',
                                       'errors': 'Nonzero test exit on failed assertions or fixture errors',
                                       'reuse_reason': 'Regression coverage for rare cleanup paths'}}],
    'adverse_conditions': [{'id': 'failure', 'behavior_id': 'cleanup-evidence',
                            'condition': 'Interrupted waits, queues or closes; pipe read failures; stale process races',
                            'expected_observation': 'Real resources cleaned where possible; uncertainty and failures retained; no valid advice',
                            'requirement_basis': 'user-request'}],
    'execution_limits': [], 'open_questions': []
}
write('workflow-design.json', design)
write('contract.json', {
    'schema_version': 'authoring-contract-v1', 'run_id': '20260916-cleanup-tests',
    'project_root': str(ROOT), 'target_root': str(TARGET), 'target_name': 'advisor',
    'operation': 'edit', 'authorization': 'User explicitly requests focused failure/cleanup tests, regression and coverage; preserve runtime unless defect proven. Development-only scope retained.',
    'history_review': 'Current 19-file source matches the published 20260916-api-retry-progress-02 candidate byte for byte.',
    'prior': ref(PARENT / '20260916-api-retry-progress-02/authoring-baseline.json'),
    'change_paths': ['tests/test_cleanup.py', 'artifact-manifest.json'],
    'requirements': [{'origin': 'user', 'outcome': 'Exercise uncovered cleanup paths with real resources, retain failure evidence, run regression and report unchanged coverage policy.',
                      'artifacts': ['tests/test_cleanup.py', 'artifact-manifest.json']}],
    'capabilities': [], 'expected_outputs': ['Cleanup regression cases and measured coverage'],
    'side_effects': ['Local synthetic child processes and temporary test files'],
    'inputs': [ref(HERE / 'task-capture.md'), ref(HERE / 'workflow-design.json')],
    'known_issues': ['Live terminal display, native Claude qualification, independent skill validation and installation are outside this focused test task.']
})
write('preservation-before.json', {
    'source': {p.relative_to(TARGET).as_posix(): ref(p)['sha256'] for p in TARGET.rglob('*') if p.is_file()},
    'operational': {p.relative_to(ROOT / '.agents/skills/advisor').as_posix(): ref(p)['sha256'] for p in (ROOT / '.agents/skills/advisor').rglob('*') if p.is_file()},
    'policy': ref(ROOT / 'AGENTS.md')
})
print(HERE)
