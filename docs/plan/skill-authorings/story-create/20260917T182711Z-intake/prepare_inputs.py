"""One-run authoring intake capture; no generated-skill execution or grading."""
from pathlib import Path
import hashlib
import json
import os
import stat

ROOT = Path('C:/Projects/DevForgeAI')
INTAKE = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/claude/skills/legacy/spec-driven-stories'
RUN_ID = '20260917T182711Z'
TARGET = ROOT / 'src/agents/skills/story-create'

def save(name, value):
    path = INTAKE / name
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    return path

def ref(path):
    return {'path': str(path.resolve()), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

task = save('user-request.md', '''# Selected import request

Import the legacy spec-driven-stories skill into the DevForgeAI Adaptive Spec-Driven Engineering framework as story-create.
Destination: C:\\Projects\\DevForgeAI\\src\\agents\\skills\\story-create
The legacy framework contains references to the old legacy CLI which are not to be migrated over.

Source clarification supplied by the user:
"C:\\Projects\\DevForgeAI\\src\\claude\\skills\\legacy\\spec-driven-stories is what i meant"

Version direction supplied by the user:
"this can be version .01 or whatever the other versions state in the new devforgeai framework"

Resolved initial package and story-template version: 0.1.0.
Scope: development import and authoring custody, preserving source and operational copies. Skill-builder owns authoring; skill-validator owns independent evaluation and its mandatory external Python evidence bundle. An authored import is not an evaluated build or framework acceptance.
''')

resources = [
    ('SKILL.md', 'instruction', 'Entry, binding prerequisite, routing and ownership', 'Every invocation'),
    ('assets/devforgeai-skill.json', 'reference', 'Portable core role descriptor', 'Binding check and adaptive package discovery'),
    ('references/adaptive-contract.md', 'reference', 'Indexed reusable requirements and observable handoffs', 'Every invocation'),
    ('references/intake-and-scope.md', 'reference', 'Project context, input selection, metadata and ID allocation', 'Every story request'),
    ('references/batch-and-dependencies.md', 'reference', 'Epic and coverage-gap decomposition, clause ownership and dependency graph', 'Batch requests or shared prerequisites'),
    ('references/recommendations-and-gaps.md', 'reference', 'QA, RCA and deferred-work fidelity and source linkage', 'Recommendation, RCA or gap input'),
    ('references/architecture-seeds.md', 'reference', 'Development architecture JSON island and selected seed mapping', 'Architecture document or seed input'),
    ('references/acceptance-criteria.md', 'reference', 'Measurable XML acceptance criteria, provenance and refactor invariants', 'Requirements drafting'),
    ('references/domain-patterns.md', 'reference', 'Behavioral prompts for applicable feature families', 'Relevant domain behavior requires detail'),
    ('references/technical-specification.md', 'reference', 'Components, API contracts, data and test mappings', 'Technical design drafting'),
    ('references/ui-specification.md', 'reference', 'Interfaces, states, interactions and accessibility', 'Story has a user interface'),
    ('references/story-contract.md', 'reference', 'Versioned story field meanings and template consumption', 'Story assembly and review'),
    ('references/delivery-and-resume.md', 'reference', 'Readback, linked-document updates, interruption and final handoff', 'Before writes, on resume, and at delivery'),
    ('assets/templates/story-template.md', 'template', 'Single-file story output structure and section manifest', 'Story assembly'),
    ('assets/templates/session-record.md', 'template', 'External resumable batch/session evidence', 'Multiple stories, interruption or partial delivery'),
    ('scripts/check_project_binding.py', 'helper', 'Unchanged read-only adaptive binding observer', 'Before product actions and after resume or package/binding changes'),
]
paths = [x[0] for x in resources]

groups = {
    'intake-and-scope.md': ['story-discovery.md', 'story-discovery-interactive.md', 'parameter-extraction.md', 'context-validation.md', 'story-type-classification.md', 'user-input-integration-guide.md', 'phase-01-story-discovery.md'],
    'batch-and-dependencies.md': ['story-discovery-batch.md', 'batch-mode-configuration.md', 'gap-to-story-conversion.md', 'custody-chain-workflow.md'],
    'recommendations-and-gaps.md': ['story-discovery-from-recommendations.md'],
    'acceptance-criteria.md': ['acceptance-criteria-core.md', 'acceptance-criteria-patterns.md', 'acceptance-criteria-refactor.md', 'refactor-quality-checks.md', 'requirements-analysis.md', 'phase-02-requirements-analysis.md', 'requirements-analyst-contract.yaml'],
    'domain-patterns.md': ['acceptance-criteria-domains.md', 'story-examples.md'],
    'technical-specification.md': ['technical-specification-creation.md', 'technical-specification-guide.md', 'technical-specification-guide-rest.md', 'technical-specification-guide-graphql.md', 'technical-specification-guide-grpc.md', 'phase-03-technical-specification.md', 'api-designer-contract.yaml'],
    'ui-specification.md': ['ui-specification-creation.md', 'ui-specification-guide.md', 'phase-04-ui-specification.md'],
    'story-contract.md': ['story-structure-guide.md', 'story-file-creation.md', 'phase-05-story-file-creation.md', 'template-consumer-contract.yaml'],
    'delivery-and-resume.md': ['checkpoint-schema.md', 'error-handling.md', 'epic-sprint-linking.md', 'completion-report.md', 'integration-guide.md', 'story-validation-workflow.md', 'validation-checklists.md', 'template-version-validation.md', 'validator-traps.md', 'fix-resolution-patterns.md', 'phase-06-epic-sprint-linking.md', 'phase-07-self-validation.md', 'phase-08-completion-report.md', 'phase-output-schema.json'],
}
originals, exclusions, inventory, texts = [], [], [], {}
for directory, dirs, files in os.walk(SOURCE, followlinks=False):
    base = Path(directory)
    for name in list(dirs):
        path = base / name
        if 'backup' in name.lower() or name.lower() in {'devforgeai_cli', '__pycache__', '.git'}:
            dirs.remove(name)
            exclusions.append({'path': path.relative_to(SOURCE).as_posix(), 'reason': 'Excluded before recursion by import boundary'})
        elif path.lstat().st_file_attributes & 0x400:
            raise ValueError('Link or junction rejected')
    for name in sorted(files):
        path = base / name
        rel = path.relative_to(SOURCE).as_posix()
        if 'backup' in name.lower():
            exclusions.append({'path': rel, 'reason': 'Backup excluded before content read'})
            continue
        info = path.lstat()
        if not stat.S_ISREG(info.st_mode) or info.st_file_attributes & 0x400:
            raise ValueError('Nonregular source rejected')
        if name.lower().startswith('.env') or path.suffix.lower() in {'.pem', '.key', '.pfx', '.p12', '.ppk'} or name.lower() in {'id_rsa', 'id_dsa', 'id_ecdsa', 'id_ed25519'}:
            raise ValueError('Private source filename rejected')
        if info.st_size > 32 * 1024 * 1024:
            raise ValueError('Source file exceeds capture limit')
        data = path.read_bytes()
        inventory.append({'path': rel, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
        originals.append(path)
        texts[rel] = data.decode('utf-8-sig')
if len(inventory) > 2000 or sum(x['bytes'] for x in inventory) > 32 * 1024 * 1024:
    raise ValueError('Source capture exceeds limits')
inventory.sort(key=lambda x: x['path'])
save('source-manifest.json', {'source_root': str(SOURCE), 'files': inventory, 'exclusions': exclusions, 'package_digest': hashlib.sha256(json.dumps(inventory, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()})
dispositions = []
for row in inventory:
    name = Path(row['path']).name
    destinations = ['references/' + k for k, v in groups.items() if name in v]
    reason = 'Preserve domain requirements; consolidate repeated phases; replace provider mechanics and legacy CLI gates with explicit ordinary authoring behavior and honest authority limits.'
    disposition = 'adapted'
    if row['path'] == 'SKILL.md':
        destinations = ['SKILL.md', 'references/adaptive-contract.md', 'references/architecture-seeds.md']
    elif row['path'] == 'assets/templates/story-template.md':
        destinations = ['assets/templates/story-template.md', 'references/story-contract.md']
        reason = 'User authorized initial 0.1.0 version; preserve useful field names and XML/structured technical content, resolve contradictory section guidance, remove old tool claims and historical boilerplate.'
    elif not destinations:
        disposition = 'not_migrated'
        reason = 'Historical migration, command generation, validator implementation, fixtures or examples depend on superseded schemas/host infrastructure. Retained as import evidence; no runtime consumer in story-create. Current requirements/examples live in the new references and template.'
    consumers = sorted(p for p, text in texts.items() if p != row['path'] and (row['path'] in text or name in text))
    dispositions.append({'source': row['path'], 'sha256': row['sha256'], 'disposition': disposition, 'destinations': destinations, 'reason': reason, 'observed_text_consumers': consumers})
save('source-dispositions.json', {'source_root': str(SOURCE), 'rows': dispositions, 'exclusions': exclusions, 'consumer_limit': 'Textual callers and links inspected; external historical consumers are outside scope and compatibility is not asserted.'})

requirement_rows = [
    ('SC-001', 'Publish only the selected story-create development package at version 0.1.0; preserve original source and operational copies.', ['SKILL.md']),
    ('SC-002', 'Remove old CLI commands, hooks, phase enforcement, slash-command mechanics and provider-specific overrides from runtime instructions.', ['SKILL.md', 'references/delivery-and-resume.md']),
    ('SC-003', 'Use a portable adaptive core descriptor and the unchanged generic binding helper before product effects.', ['assets/devforgeai-skill.json', 'scripts/check_project_binding.py', 'SKILL.md']),
    ('SC-004', 'Discover current project rules, layout, quality policy and selected sources; ask only for unresolved material decisions.', ['references/intake-and-scope.md']),
    ('SC-005', 'Support feature, epic batch, architecture seed, QA/RCA recommendation and deferred-gap entry points without silently broadening selection.', ['references/intake-and-scope.md', 'references/batch-and-dependencies.md', 'references/recommendations-and-gaps.md', 'references/architecture-seeds.md']),
    ('SC-006', 'Allocate collision-safe story identities across active and archived work; preserve explicit metadata, Backlog defaults and story-type semantics without TDD bypass.', ['references/intake-and-scope.md']),
    ('SC-007', 'Decompose independently assessable outcomes with clause ownership, acceptance mapping, concrete acyclic prerequisites and integration obligations.', ['references/batch-and-dependencies.md']),
    ('SC-008', 'Preserve selected recommendation IDs, exact verification expectations, RCA traceability and blocking/advisory distinctions without claiming fixes.', ['references/recommendations-and-gaps.md']),
    ('SC-009', 'Read the architecture data island as data, map the selected seed and retain source/feature provenance and explicit dependency decisions.', ['references/architecture-seeds.md']),
    ('SC-010', 'Write source-grounded measurable XML acceptance criteria with boundary, error, security and applicable refactor invariants.', ['references/acceptance-criteria.md', 'references/domain-patterns.md']),
    ('SC-011', 'Specify applicable components, APIs, data rules, constraints, failure behavior and bidirectional AC-to-technical/test traceability.', ['references/technical-specification.md']),
    ('SC-012', 'Include UI states, interactions, component interfaces, terminal-readable layouts and accessibility only when applicable.', ['references/ui-specification.md']),
    ('SC-013', 'Deliver one complete story file per outcome with current template fields, provenance, scope, NFRs, dependencies, edge cases, test strategy and unchecked DoD.', ['assets/templates/story-template.md', 'references/story-contract.md']),
    ('SC-014', 'Update explicitly selected epic/sprint/source links idempotently after story readback and preserve unrelated or concurrent edits.', ['references/delivery-and-resume.md']),
    ('SC-015', 'Retain resumable selected-input identities, actual writes, batch results, uncertain effects and the next safe action; never treat cached prose as authority.', ['assets/templates/session-record.md', 'references/delivery-and-resume.md']),
    ('SC-016', 'Review authored documents and deliver literal read-back paths, unresolved gaps and explicit manual development/QA handoffs without claiming evaluated or protected acceptance.', ['references/delivery-and-resume.md']),
]
save('requirements.json', [{'id': i, 'origin': 'user' if i in {'SC-001', 'SC-002'} else 'derived', 'outcome': s, 'artifacts': a} for i, s, a in requirement_rows])

policy = [ROOT / 'AGENTS.md', ROOT / 'docs/specs/framework/core-workflows.md', ROOT / 'docs/specs/framework/work-items-and-dependencies.md', ROOT / 'docs/specs/framework/skills-and-project-expertise.md', ROOT / 'docs/specs/framework/guardrails-and-rust-runtime.md', ROOT / 'src/agents/skills/dev/SKILL.md', ROOT / 'src/agents/skills/qa/SKILL.md', ROOT / '.agents/skills/skill-builder/assets/adaptive-runtime/check_project_binding.py', ROOT / '.agents/skills/skill-builder/references/adaptive-contracts.md', ROOT / '.agents/skills/skill-builder/references/project-binding.md', ROOT / '.agents/skills/skill-builder/references/validation-handoff.md']
inputs = [ref(p) for p in [task, INTAKE / 'source-manifest.json', INTAKE / 'source-dispositions.json', INTAKE / 'requirements.json', INTAKE / 'import-decisions.md', *policy, *sorted(originals)]]
behaviors = []
for i, s, a in requirement_rows[3:]:
    behaviors.append({'id': i.replace('SC', 'B'), 'requirement_ids': [i], 'trigger': s, 'inputs': ['Current selected request, current project context and applicable source artifacts'], 'completion': s, 'outputs': ['Selected story document or explicit missing-input/partial-delivery report'], 'resource_paths': a, 'prerequisites': ['Runtime binding MATCH/BOUND before product effects', 'Selected source and authorized destination available'], 'effects': ['Only requested story/session documents and explicitly selected link updates'], 'failure': 'Report the exact failed requirement and actual written artifacts; do not claim dependent completion.', 'recovery': 'Reread selected inputs and existing outputs, resolve drift and pending decisions, then continue only authorized unfinished work.'})
design_resources = []
for p, k, purpose, when in resources:
    helper = None
    if k == 'helper':
        helper = {'inputs': '--project-root selected project; --skill-root actually loaded package', 'outputs': 'One binding-observation-v1 JSON object, sanitized reason and nullable digests', 'runtime': 'Python 3.10+ standard library, -B -X utf8; no network or installation', 'effects': 'Read-only; no cache, bytecode or binding writes', 'errors': '0 MATCH/BOUND; 1 MISMATCH; 2 UNAVAILABLE or CLI usage error; all nonzero outcomes prevent product effects', 'reuse_reason': 'Shared exact package/root/role binding contract, copied byte-for-byte from installed skill-builder template'}
    design_resources.append({'path': p, 'kind': k, 'purpose': purpose, 'load_when': when, 'helper_contract': helper})
design = {'schema_version': 'authoring-design-v1', 'target_name': 'story-create', 'source_refs': inputs, 'behaviors': behaviors, 'resources': design_resources, 'adverse_conditions': [
    {'id': 'A01', 'behavior_id': 'B-004', 'condition': 'Binding missing, relocated or changed', 'expected_observation': 'No product writes; sanitized mismatch/unavailable reason; separately owned setup prerequisite', 'requirement_basis': 'SC-003 and binding contract'},
    {'id': 'A02', 'behavior_id': 'B-007', 'condition': 'Missing decision, duplicate owner or cycle', 'expected_observation': 'Dependent stories remain unresolved; independent selected work can continue; no ready claim', 'requirement_basis': 'SC-007 and framework work-items contract'},
    {'id': 'A03', 'behavior_id': 'B-008', 'condition': 'Recommendation missing a required field, unknown ID or stale source cycle', 'expected_observation': 'Named affected entries blocked before dependent writes; exact source facts are not fabricated', 'requirement_basis': 'SC-008 and legacy recommendation fidelity'},
    {'id': 'A04', 'behavior_id': 'B-013', 'condition': 'Destination exists, permission denied or write/readback interrupted', 'expected_observation': 'Preserve current bytes and partial outputs; no overwrite, relocation or delivered claim without readback', 'requirement_basis': 'SC-006, SC-013 and SC-015'},
    {'id': 'A05', 'behavior_id': 'B-014', 'condition': 'Story written but epic/source update fails or has concurrent changes', 'expected_observation': 'Report story delivery separately from pending links and retain exact next action without rollback claim', 'requirement_basis': 'SC-014 and SC-015'},
    {'id': 'A06', 'behavior_id': 'B-016', 'condition': 'Only template or proposed output path exists; native workflow unexecuted', 'expected_observation': 'No claim of observed generated-story behavior, test PASS or framework acceptance', 'requirement_basis': 'SC-016 and AGENTS.md authority boundary'}
], 'execution_limits': [], 'open_questions': []}
design_path = save('authoring-design.json', design)
contract = {'schema_version': 'authoring-contract-v1', 'run_id': RUN_ID, 'project_root': str(ROOT), 'target_root': str(TARGET), 'target_name': 'story-create', 'operation': 'import', 'authorization': 'User selected legacy source clarified in user-request.md, destination src/agents/skills/story-create, excluded legacy CLI and authorized new version 0.1.0. Development authoring only.', 'history_review': 'no_known_history: target absent and no prior story-create authoring directory at initial inspection', 'change_paths': paths, 'requirements': json.loads((INTAKE / 'requirements.json').read_text(encoding='utf-8')), 'capabilities': ['Native Windows PowerShell; Python 3.10.11 observed; terminal read/search/write tools; loaded builder custody helper. Generated workflow not executed.'], 'expected_outputs': ['Portable story-create 0.1.0 development package', 'Source-file dispositions, bound design, authoring record/baseline and manual validator request'], 'side_effects': ['At runtime: create selected stories and session records; update explicitly selected related records after readback; no implementation, acceptance, operational installation or automatic downstream invocation'], 'inputs': inputs + [ref(design_path)], 'known_issues': ['Validation and testing NOT_PERFORMED; separate skill-validator must author and run the mandatory external Python JSONL runner, deterministic graders, fixtures, expected results, schema, dependency/runtime declarations and digest-bound manifests.', 'No native workflow qualification or downstream parser compatibility claim; adaptive runtime requires separately installed and bound package.', 'Legacy source version/manifest/phase discrepancies are resolved explicitly in import-decisions.md; historical files remain unchanged.']}
save('authoring-contract.json', contract)
print(json.dumps({'intake': str(INTAKE), 'target': str(TARGET), 'source_files': len(inventory), 'source_bytes': sum(x['bytes'] for x in inventory), 'excluded': exclusions, 'candidate_paths': len(paths)}, indent=2))
