"""Capture the selected maintenance request and existing package custody."""
import hashlib
import json
from pathlib import Path

ROOT = Path('C:/Projects/DevForgeAI')
INTAKE = Path(__file__).resolve().parent
PRIOR = ROOT / 'docs/plan/skill-authorings/advisor/20260916T134000Z-streaming'
TARGET = ROOT / 'src/agents/skills/advisor'


def ref(path):
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def write(name, value):
    (INTAKE / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


task = '''# Selected request
User supplied the proposed system/api_retry progress branch and asked for integer-only
retry counts and optional numeric status without server-controlled error text.
Assistant: "The patch is reasonable, with one adjustment: use type(value) is int so
booleans cannot appear as retry counts or status codes. Should I apply and test it in
src/agents/ only, or both development and operational copies?"
User: "src/ tree only"

Scope: implement and test the selected maintenance fix in the development advisor
package only. Preserve operational bytes and prior evidence. Update the matching
execution reference and artifact manifest. User authorization to apply and test,
plus repository mandatory TDD, takes precedence over the builder authoring-only
testing restriction for this maintenance task. Independent skill validation remains
separate and unperformed; do not invoke Claude or install the changed package.

Requirements:
R1: system/api_retry emits retry A/M when attempt and max_retries are actual integers.
R2: append status S only when error_status is an actual integer; bool is not an integer here.
R3: ignore malformed count fields; never emit error text, arbitrary fields, or terminal escapes.
R4: preserve raw evidence, result interpretation, limits, authentication, and existing progress.
'''
(INTAKE / 'task-capture.md').write_text(task, encoding='utf-8')
source = ref(INTAKE / 'task-capture.md')
design = {
    'schema_version': 'authoring-design-v1', 'target_name': 'advisor',
    'source_refs': [source],
    'behaviors': [{
        'id': 'retry-progress', 'requirement_ids': ['R1', 'R2', 'R3', 'R4'],
        'trigger': 'A parsed system event with subtype api_retry during streaming progress',
        'inputs': ['attempt', 'max_retries', 'optional error_status'],
        'completion': 'Emit elapsed retry A/M with optional integer status S; ignore invalid counts and exclude all arbitrary text.',
        'outputs': ['Allowlisted progress on stderr; unchanged captured raw JSONL'],
        'resource_paths': ['scripts/advisor_stream.py', 'references/execution.md'],
        'prerequisites': ['Python >=3.10 and selected streaming mode'],
        'effects': ['Progress presentation only'],
        'failure': 'Ignore malformed retry fields; existing progress sink error handling preserves evidence capture.',
        'recovery': 'Continue consuming events under the existing process deadline; do not initiate retries.'
    }],
    'resources': [
        {'path': 'scripts/advisor_stream.py', 'kind': 'helper',
         'purpose': 'Capture streams and display safe progress',
         'load_when': 'Advisor streaming mode is selected',
         'helper_contract': {'inputs': 'Parsed JSONL events', 'outputs': 'Numeric retry progress and unchanged raw evidence',
                             'runtime': 'Python >=3.10 standard library', 'effects': 'Write existing progress sink',
                             'errors': 'Suppress invalid metadata without changing execution outcome',
                             'reuse_reason': 'Expose retries for every streaming invocation'}},
        {'path': 'references/execution.md', 'kind': 'reference', 'purpose': 'Document allowed retry progress',
         'load_when': 'Preparing an advisor invocation', 'helper_contract': None}
    ],
    'adverse_conditions': [{
        'id': 'invalid-fields', 'behavior_id': 'retry-progress',
        'condition': 'Boolean/string/list/missing counts or arbitrary status/error text',
        'expected_observation': 'No invalid count line; optional invalid status omitted; no arbitrary text disclosure',
        'requirement_basis': 'R2 and R3'
    }],
    'execution_limits': [], 'open_questions': []
}
write('workflow-design.json', design)
write('authoring-contract.json', {
    'schema_version': 'authoring-contract-v1', 'run_id': '20260916-api-retry-progress',
    'project_root': str(ROOT), 'target_root': str(TARGET), 'target_name': 'advisor',
    'operation': 'edit', 'authorization': 'User selected src/ tree only in response to apply-and-test scope question.',
    'history_review': 'Prior published streaming authoring record and baseline inspected; bind and preserve that history.',
    'prior': ref(PRIOR / 'authoring-baseline.json'),
    'change_paths': ['scripts/advisor_stream.py', 'tests/test_streaming.py', 'references/execution.md', 'artifact-manifest.json'],
    'requirements': [{'origin': 'user', 'outcome': 'R1-R4: safe integer-only retry progress with focused regression tests; development only.',
                      'artifacts': ['scripts/advisor_stream.py', 'tests/test_streaming.py', 'references/execution.md', 'artifact-manifest.json']}],
    'capabilities': [], 'expected_outputs': ['Numeric retry progress when streaming'],
    'side_effects': ['Progress sink writes only; no new retries or network requests'],
    'inputs': [source, ref(INTAKE / 'workflow-design.json')],
    'known_issues': ['Independent skill validation and live native retry qualification are not part of this focused maintenance fix.']
})
operational = ROOT / '.agents/skills/advisor'
write('operational-before.json', {
    str(p.relative_to(operational)).replace('\\', '/'): ref(p)['sha256']
    for p in sorted(operational.rglob('*')) if p.is_file()
})
print(INTAKE)
