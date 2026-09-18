"""One-time maintenance construction of the selected design resources."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PACKAGE = ROOT / 'src/agents/skills/skill-builder'

def obj(properties):
    return {'type': 'object', 'required': list(properties), 'additionalProperties': False, 'properties': properties}

def array(item, minimum=0):
    return {'type': 'array', 'items': item, 'minItems': minimum}

string = {'type': 'string', 'minLength': 1, 'pattern': r'(?s).*\S.*'}
strings = array(string)
reference = obj({'path': string, 'sha256': {'type': 'string', 'pattern': '^[0-9a-f]{64}$'}})
helper = obj({key: string for key in ('inputs', 'outputs', 'runtime', 'effects', 'errors', 'reuse_reason')})
behavior = obj({
    'id': string, 'requirement_ids': array(string, 1), 'trigger': string, 'inputs': strings,
    'completion': string, 'outputs': strings, 'resource_paths': strings, 'prerequisites': strings,
    'effects': strings, 'failure': string, 'recovery': string})
resource = obj({'path': string, 'kind': {'enum': ['instruction', 'reference', 'template', 'helper']},
                'purpose': string, 'load_when': string,
                'helper_contract': {'anyOf': [{'type': 'null'}, helper]}})
schema = obj({
    'schema_version': {'const': 'authoring-design-v1'}, 'target_name': string,
    'source_refs': array(reference), 'behaviors': array(behavior, 1), 'resources': array(resource),
    'adverse_conditions': array(obj({key: string for key in ('id', 'behavior_id', 'condition', 'expected_observation', 'requirement_basis')})),
    'execution_limits': array(obj({'behavior_id': string, 'seconds': {'type': 'integer', 'minimum': 1},
        'kind': {'enum': ['specified_requirement', 'execution_ceiling']}, 'source_basis': string})),
    'open_questions': array(obj({'id': string, 'question': string, 'owner': string, 'affected_behavior_ids': array(string, 1)}))})
schema['$schema'] = 'https://json-schema.org/draft/2020-12/schema'
(PACKAGE / 'schemas/authoring-design.schema.json').write_text(json.dumps(schema, indent=2) + '\n', encoding='utf-8')
template = {
    'schema_version': 'authoring-design-v1', 'target_name': '', 'source_refs': [],
    'behaviors': [{'id': '', 'requirement_ids': [], 'trigger': '', 'inputs': [], 'completion': '',
        'outputs': [], 'resource_paths': [], 'prerequisites': [], 'effects': [], 'failure': '', 'recovery': ''}],
    'resources': [], 'adverse_conditions': [], 'execution_limits': [], 'open_questions': []}
(PACKAGE / 'assets/authoring-design-template.json').write_text(json.dumps(template, indent=2) + '\n', encoding='utf-8')
