"""Reviewed maintenance preparation: schemas are data, no companion runtime import."""
import json
from pathlib import Path
import shutil
from capture import ROOT, RUN, save

TARGET = ROOT / 'src/agents/skills/skill-validator'
BUILDER = ROOT / 'src/agents/skills/skill-builder'
S = {'type': 'string', 'minLength': 1}
I = {'type': 'integer', 'minimum': 0}
B = {'type': 'boolean'}
def ref(name):
    return {'$ref': 'adaptive-common.schema.json#/$defs/' + name}
def array(item, minimum=0, unique=False):
    return {'type': 'array', 'items': item, 'minItems': minimum, **({'uniqueItems': True} if unique else {})}
def enum(*values):
    return {'enum': list(values)}
def nullable(item):
    return {'anyOf': [item, {'type': 'null'}]}
def obj(**fields):
    return {'type': 'object', 'additionalProperties': False, 'required': list(fields), 'properties': fields}
def record(version, **fields):
    return {'$schema': 'https://json-schema.org/draft/2020-12/schema', **obj(schema_version={'const': version}, **fields)}
def emit(name, value):
    path = TARGET / 'schemas' / (name + '.schema.json')
    if path.exists():
        raise ValueError('new schema already exists')
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

if __name__ == '__main__':
    for name in ('adaptive-common', 'project-evidence-v1', 'adaptation-proposal-v1', 'adaptation-selection-v1', 'adaptive-skill-v1', 'set-authoring-v1', 'set-validation-request-v1', 'project-binding-v1', 'binding-observation-v1', 'adaptive-observation-v1'):
        shutil.copyfile(BUILDER / 'schemas' / (name + '.schema.json'), TARGET / 'schemas' / (name + '.schema.json'))
    emit('standalone-set-input-v1', record('standalone-set-input-v1', run_id=ref('Id'), authorization=ref('Ref'), members=array(obj(member_id=ref('Id'), package=ref('PackageRef'), specifications=array(ref('Ref')), adaptive_descriptor=nullable(ref('Ref')), depends_on=array(ref('Id'), unique=True)), 1), handoffs=array(ref('Handoff')), requirements=array(ref('Requirement')), gaps=array(ref('Gap'))))
    outcome = enum('PASS', 'FAIL', 'INCOMPLETE')
    emit('set-assessment-v1', record('set-assessment-v1', run_id=ref('Id'), input=ref('Ref'), scope=enum('full_set', 'eligible_subset'), omitted_member_ids=array(ref('Id'), unique=True), omitted_handoff_ids=array(ref('Id'), unique=True), members=array(obj(member_id=ref('Id'), package_digest=ref('Digest'), report=nullable(ref('Ref')), checks=nullable(ref('Ref')), outcome=outcome, source_state=enum('UNCHANGED', 'SOURCE_CHANGED', 'NOT_RUN'), reason=S)), integration_checks=ref('Ref'), outcome=outcome, assessment_completed=B, required_evaluated=I, required_total=I, unknown_applicability=I, limitations=array(S), prior_assessment=nullable(ref('Ref'))))
    candidate = obj(path=ref('RelPath'), start_byte=I, end_byte={'type': 'integer', 'minimum': 1}, line={'type': 'integer', 'minimum': 1}, column={'type': 'integer', 'minimum': 1}, codepoint=S, unicode_name=S, escaped_excerpt={**S, 'maxLength': 160}, context=enum('prose', 'metadata', 'command', 'path', 'fixture', 'unknown'), disposition=enum('defect', 'legitimate', 'unresolved'), reason=S)
    resource = obj(path=ref('RelPath'), role=enum('runtime', 'template', 'reference', 'fixture', 'license', 'unknown'), reachable=B, usage=enum('used', 'intentional_nonruntime', 'orphan', 'unresolved_usage'), evidence=array(ref('Ref')), reason=S)
    edge = obj(source=ref('RelPath'), line={'type': 'integer', 'minimum': 1}, target=S, kind=enum('link', 'image', 'instruction', 'script_call', 'template_use'), resolution=enum('resolved', 'missing', 'outside_scope', 'dynamic', 'unsupported_anchor'))
    context = obj(tokenizer=nullable(obj(name=S, version=S, encoding=S)), files=array(obj(path=ref('RelPath'), bytes=I, characters=I, lines=I, tokens=nullable(I))), loads=array(obj(case_id=ref('Id'), path=ref('RelPath'), occurrences={'type':'integer','minimum':1}, basis=enum('observed_full_file','observed_excerpt','static_estimate'), tokens=nullable(I), evidence=array(ref('Ref')))), budget=nullable(obj(unit=enum('bytes','characters','tokens'), scope=enum('entrypoint','unique_branch_content','observed_total_loads'), maximum={'type':'integer','minimum':1}, case_id=nullable(ref('Id')), source=ref('Ref'))), budget_result=enum('PASS','FAIL','NOT_RUN','NOT_APPLICABLE'), reason=S)
    emit('adaptive-observations-v1', record('adaptive-observations-v1', run_id=ref('Id'), target_digest=ref('Digest'), unicode_candidates=array(candidate), resources=array(resource), edges=array(edge), context=context, bindings=array(obj(case_id=ref('Id'), binding_sha256=nullable(ref('Digest')), observation=ref('Ref'), expected=enum('MATCH','MISMATCH','UNAVAILABLE'), observed=enum('MATCH','MISMATCH','UNAVAILABLE','NOT_RUN'), effects_match=nullable(B))), limitations=array(S)))
    check = obj(schema_version={'const':'1'}, run_id=ref('Id'), check_id=ref('Id'), rule_id=ref('Id'), subject_path=S, method=enum('deterministic','semantic','behavioral'), required=B, applicability=enum('applicable','not_applicable','unknown'), result=enum('PASS','FAIL','NOT_RUN','ERROR','NOT_APPLICABLE'), reason=S, evidence=array(ref('Ref')))
    helper_observations = {'anyOf': [obj(unicode_candidates=array(candidate), resources=array(resource), edges=array(edge), context=context), obj(input_kind=enum('set-validation-request-v1','standalone-set-input-v1'), ordered_member_ids=array(ref('Id'), unique=True), member_bindings=array(obj(member_id=ref('Id'), package_digest=ref('Digest'), valid=B, reason=S))), obj(checked_records=array(S), errors=array(S))]}
    emit('adaptive-check-observation-v1', record('adaptive-check-observation-v1', command=enum('package','intake-set','records'), status=enum('OBSERVED','MISMATCH','INCOMPLETE'), checks=array(check), observations=helper_observations, limitations=array(S)))
    save('implementation-map.json', {'requirements': {f'VA-{i:03}': {'instructions':['SKILL.md','references/adaptive-validation.md','references/text-resource-checks.md','references/set-trials.md'], 'helpers':['scripts/adaptive_contracts.py','scripts/adaptive_observe.py','scripts/text_resources.py'], 'cases': list(range(1,26))} for i in range(1,16)}, 'legacy': 'Existing files preserved except additive routing; self-review explicitly required.'})
