"""One-off authoring input capture; does not execute or evaluate Brainstorm."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path('C:/Projects/DevForgeAI')
INTAKE = Path(__file__).resolve().parent
RUN_ID = '20260918T020654Z'


def reference(path):
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def write_json(path, value):
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    with path.open('xb') as stream:
        stream.write(raw)
    if path.read_bytes() != raw:
        raise RuntimeError('Input capture readback mismatch: ' + str(path))


sources = [ROOT / name for name in [
    'docs/specs/framework/workflows/phase-1-brainstorm-spec.md',
    'docs/specs/framework/index.md',
    'docs/specs/framework/core-workflows.md',
    'docs/specs/framework/project-context-and-policy.md',
    'docs/specs/framework/roadmap-and-decisions.md',
    'docs/specs/framework/work-items-and-dependencies.md',
    'docs/specs/framework/skills-and-project-expertise.md',
    'docs/specs/framework/expert-health-and-realignment.md',
    'docs/specs/framework/installation-and-integrations.md',
    'docs/specs/dev-skill-spec.md',
    'AGENTS.md',
]] + [INTAKE / 'request.md']
snapshot_dir = INTAKE / 'originals'
snapshot_dir.mkdir(exist_ok=False)
snapshots = []
for index, source in enumerate(sources):
    raw = source.read_bytes()
    destination = snapshot_dir / (str(index).zfill(2) + '-' + source.name)
    with destination.open('xb') as stream:
        stream.write(raw)
    if destination.read_bytes() != raw or source.read_bytes() != raw:
        raise RuntimeError('Source drift or capture failure: ' + str(source))
    snapshots.append({'source': reference(source), 'snapshot': reference(destination)})
write_json(INTAKE / 'source-capture.json', snapshots)

skill = 'SKILL.md'
evidence = 'references/evidence-and-decisions.md'
saved = 'references/saved-briefs.md'
template = 'assets/discovery-brief-template.md'
ui = 'agents/openai.yaml'
paths = [skill, evidence, saved, template, ui]


def behavior(identity, requirements, trigger, inputs, completion, outputs, resources, prerequisites, effects, failure, recovery):
    return dict(id=identity, requirement_ids=requirements, trigger=trigger, inputs=inputs,
                completion=completion, outputs=outputs, resource_paths=resources,
                prerequisites=prerequisites, effects=effects, failure=failure, recovery=recovery)


behaviors = [
    behavior('intake', ['BR-001', 'BR-002', 'BR-003', 'BR-004', 'BR-005'],
             'An uncertain idea, comparison, selected discovery resume, or near-miss request.',
             ['Current request, supplied answers, selected root and permitted effects when known.'],
             'Selected uncertainty and scope are identified or the appropriate near-miss responsibility is named without invocation; preliminary dialogue needs no root or setup.',
             ['Conversational scope and persistence choice; no file unless saving is selected.'],
             [skill, ui], [], ['Conversation; relevant reads only after root selection.'],
             'An ambiguous root blocks only dependent project reads or writes; a near miss does not authorize product or setup effects.',
             'Ask only for the missing material selection; reuse existing authorization and supplied answers.'),
    behavior('discovery', ['BR-006', 'BR-007', 'BR-008', 'BR-009', 'BR-010'],
             'Selected discovery uncertainty needs evidence, decisions, alternatives or architectural questions.',
             ['Selected sources, relevant interfaces and conventions, user decisions and observed experiments.'],
             'Problem, users, observable outcome, scope and meaningful direction choices have attributed evidence; unanswered decisions and follow-ups remain visible.',
             ['Discussion and, when selected, substantive brief sections with source inventory and decision/question records.'],
             [skill, evidence], ['Selected root before project reads; available user-input or ordinary chat interface.'],
             ['Bounded relevant nonsecret reads; interview and documentation drafting.'],
             'Essential unavailable sources or governing contradictions block affected conclusions; optional unavailable research is disclosed; document instructions do not grant effects.',
             'Continue useful independent work, retain alternatives and question owners, and propose separately scoped experiments without executing them.'),
    behavior('handoff', ['BR-004', 'BR-011', 'BR-012', 'BR-014'],
             'A discovery result or useful partial result is ready to return.',
             ['Current selected outcome, existing artifact adequacy, open questions, decisions and provenance.'],
             'Reuse is checked first; remaining discovery blockers yield NEEDS_INPUT; sufficient inputs yield READY_FOR_PRD with explicit later-stage questions and next responsibility.',
             ['Plain-English summary, exact disposition/reason, actual artifact link when saved, material gaps and suggested manual next request.'],
             [skill, template], [], ['Conversation; no downstream workflow invocation.'],
             'Unknown or uninstalled consumers are named as responsibilities, never invented commands; document delivery does not prove agreement or implementation readiness.',
             'Return the actual incomplete state and appropriate owner; wait for separately selected downstream work.'),
    behavior('save', ['BR-005', 'BR-011', 'BR-013', 'BR-014'],
             'Current user scope includes saving discovery documentation.',
             ['Selected output scope, completed or partial discussion, safe brief identity, input identities and current destination state.'],
             'One exclusively created Markdown revision contains exactly six metadata fields and nine required sections; full intended bytes are read back before linking delivery.',
             ['Selected convention/path or docs/plan/discovery/<brief-id>/brainstorm-brief-rNNN.md; safe 1-64 character local ID, positive padded revision.'],
             [skill, saved, template], ['Unambiguous selected root/output scope and document-write authorization; filesystem inspection/hash/read/write capabilities.'],
             ['Create only the selected discovery directory and new brief; preserve old briefs and source documents.'],
             'Collision, source drift, reparse escape, write denial or readback mismatch prevents a successful-delivery claim; retain/report actual partial state.',
             'Reconcile drift; inspect actual destination after interruption; choose a safe unused revision inside authorized scope or report unresolved permission without overwrite.'),
    behavior('resume', ['BR-006', 'BR-010', 'BR-013'],
             'User selects an existing brief or clarifies/changes the discovery objective.',
             ['Selected prior brief, current governing sources, current user objective and historical decisions.'],
             'Affected claims reflect changed/unavailable inputs, unchanged supported observations remain, explicit objective supersession is recorded, and any saved successor preserves its predecessor.',
             ['Updated discussion or selected new revision with supersedes, changed input identities and change notes.'],
             [skill, evidence, saved, template], ['Selected brief and root; independent selection of any saved successor.'],
             ['Relevant reads and authorized new brief revision only.'],
             'Missing, inconsistent or superseded prior inputs cannot silently serve as current decisions; uncertain interrupted write is inspected before retry.',
             'Preserve prior artifacts, name affected gaps/owners, reconcile lineage and save only to an unused safe destination when authorized.'),
]
resources = [
    dict(path=skill, kind='instruction', purpose='Activation, ownership, interview, dispositions and resource routing.', load_when='Every Brainstorm invocation.', helper_contract=None),
    dict(path=evidence, kind='reference', purpose='Source attribution, conflicts, decisions, architecture, experiments and feedback.', load_when='Inspecting project/external evidence, comparing options or revisiting evidence and decisions.', helper_contract=None),
    dict(path=saved, kind='reference', purpose='Exact Markdown artifact contract, exclusive creation, readback and resume recovery.', load_when='Saving or resuming a saved brief.', helper_contract=None),
    dict(path=template, kind='template', purpose='The six metadata fields and nine required brief sections.', load_when='Drafting an authorized saved brief; not mandatory for conversation-only dialogue.', helper_contract=None),
    dict(path=ui, kind='instruction', purpose='Display title and illustrative explicit invocation for the host UI.', load_when='Host skill metadata discovery.', helper_contract=None),
]
adverse_rows = [
    ('A01', 'intake', 'No repository, binding or daemon exists.', 'Continue preliminary discovery without setup effects.', 'BR-001/002/005; BV-01/13/16'),
    ('A02', 'intake', 'Requested work is specified repair, activation, PRD authoring/review or stories.', 'Name the owner and avoid unselected discovery/product/setup effects.', 'BR-003/004; BV-04/18'),
    ('A03', 'discovery', 'Supplied answers are complete or a material answer is declined.', 'Reuse supplied answers; declined decisions remain gaps and do not become agreement.', 'BR-007/008/012; BV-05/06'),
    ('A04', 'discovery', 'Code conflicts with governing requirements or a source contains malicious instructions.', 'Preserve the conflict as data; exclude secrets; no policy or binding changes.', 'BR-003/006; BV-07/08'),
    ('A05', 'discovery', 'Attractive unselected feature or an unsettled stack decision.', 'Preserve objective; separate follow-up and later PRD design decisions.', 'BR-008/009/010; BV-09/10'),
    ('A06', 'discovery', 'Observed experiment contradicts a hypothesis or an expert claim appears stale.', 'Attribute observations and propose revision to its owner without executing experiments or changing policy.', 'BR-006/009/010; BV-11/20'),
    ('A07', 'handoff', 'Adequate existing artifact without selected new uncertainty.', 'Return REUSE_EXISTING with exact reference and manual next responsibility.', 'BR-004/012/014; BV-03'),
    ('A08', 'handoff', 'Essential source unavailable versus optional external research unavailable.', 'Block the dependent discovery conclusion only in the essential case; disclose optional limitation.', 'BR-006/012; BV-19'),
    ('A09', 'save', 'Collision, link/reparse escape, denied or partial write, or announced output absent.', 'Preserve existing/outside files, report path/error and partial state, never claim delivery without readback.', 'BR-011/013/014; BV-12/15'),
    ('A10', 'resume', 'One source changed, another unchanged; clarification then explicit objective change.', 'Revise affected claims, preserve supported observations/prior revision, record superseded objective.', 'BR-006/010/013; BV-14/17'),
]
design = dict(schema_version='authoring-design-v1', target_name='brainstorm',
              source_refs=[reference(p) for p in sources], behaviors=behaviors, resources=resources,
              adverse_conditions=[dict(zip(['id', 'behavior_id', 'condition', 'expected_observation', 'requirement_basis'], row)) for row in adverse_rows],
              execution_limits=[], open_questions=[])
design_path = INTAKE / 'authoring-design.json'
write_json(design_path, design)

spec = sources[0].read_text(encoding='utf-8')
clauses = re.findall(r'\*\*(BR-\d{3}) — ([^\n]+)\n(.*?)(?=\n\*\*BR-|\n## 6\.|\Z)', spec, re.S)
mapping = {
    'BR-001': [skill, ui], 'BR-002': [skill], 'BR-003': [skill, evidence],
    'BR-004': [skill], 'BR-005': [skill, saved], 'BR-006': [skill, evidence],
    'BR-007': [skill], 'BR-008': [skill, evidence], 'BR-009': [evidence],
    'BR-010': [skill, evidence, saved], 'BR-011': [saved, template],
    'BR-012': [skill], 'BR-013': [saved], 'BR-014': [skill],
}
requirements = [dict(origin='DFF-WF-01 ' + identity, outcome=title + '\n' + body.strip(), artifacts=mapping[identity]) for identity, title, body in clauses]
contract = dict(
    schema_version='authoring-contract-v1', run_id=RUN_ID, project_root=str(ROOT),
    target_root=str(ROOT / 'src/agents/skills/brainstorm'), target_name='brainstorm', operation='spec_build',
    authorization=(INTAKE / 'request.md').read_text(encoding='utf-8'), history_review='no_known_history',
    change_paths=paths, requirements=requirements,
    capabilities=['Conversational user input with small batches and ordinary-chat fallback.', 'Bounded filesystem reads and SHA256 observations after root selection.', 'Exclusive new Markdown revision creation and complete readback when saving is authorized.', 'Optional external research only when relevant and available under current authorization.'],
    expected_outputs=['Conversation-only result and disposition with zero filesystem writes, or one requested discovery brief per saved revision.', 'Manual handoff to appropriate responsibility; no automatic next workflow.'],
    side_effects=['Read relevant selected nonsecret sources.', 'Write only authorized discovery documentation inside the selected output scope; no product code, configuration, installation or operational bindings.'],
    inputs=[reference(p) for p in sources] + [reference(design_path)],
    known_issues=['Independent evaluation NOT_PERFORMED; all BV-01 through BV-20 and required subcases remain NOT_RUN, including explicit and natural-language activation.', 'Evaluated-build completion INCOMPLETE: the independent evaluator must supply a bound Python JSONL runner, deterministic graders, fixtures, expected results, schema, runtime/dependency information and artifact digests/manifests.', 'Initial qualification target is native Windows/PowerShell in disposable fixtures; other hosts remain unqualified. Package executable denominator is zero: coverage NOT_APPLICABLE, never 100%; evaluator/helper coverage is separate.'],
    purpose='Portable standalone product discovery from uncertain idea to grounded brief, named input gaps or reuse.',
    activation='Brainstorm/explore an uncertain product or feature, compare directions, or resume selected discovery; distinguish implementation/setup/PRD/story near misses.',
    dependencies=['Host conversation tools; filesystem/hash capabilities only for selected local evidence or saving. No executable package helper or binding prerequisite.'],
    operational_constraints=['Author development source only.', 'Dispositions are advisory observations, not protected Rust acceptance.', 'No forced stack, fixed project policy or runtime root.'],
    recovery='Preserve prior evidence; reconcile changed inputs and collisions, inspect uncertain writes and report partial delivery rather than retry blindly.',
)
write_json(INTAKE / 'authoring-contract.json', contract)
print(json.dumps({'contract': str(INTAKE / 'authoring-contract.json'), 'design': reference(design_path), 'requirement_ids': [row['origin'] for row in requirements], 'input_count': len(contract['inputs'])}, indent=2))
