"""Assemble bounded assessment records from extant observations; no source writes."""
import datetime
import hashlib
import json
from pathlib import Path
import shutil

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[4]
OUT = RUN / 'assessment'
OWNER = RUN / 'assessment-owner/skill-validator'
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z')
base = {'schema_version': '1', 'run_id': RUN.name, 'target_name': 'skill-builder'}

def save(name, value):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)

def text(name, value):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        stream.write(value)

def copy(source, name):
    data = source.read_bytes()
    assert len(data) <= 8 * 1024 * 1024
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(data)

def ref(name):
    return {'path': name, 'sha256': hashlib.sha256((OUT / name).read_bytes()).hexdigest()}

manifest = json.loads((OUT / 'source-manifest.json').read_text())
digest = manifest['package_digest']
inputs = [
    (RUN / 'inputs/skill-builder-adaptive-enhancement-spec.md', 'governing-spec.md', 'governing'),
    (RUN / 'inputs/skill-validator-adaptive-enhancement-spec.md', 'companion-spec.md', 'companion'),
    (Path(r'C:\Users\bryan\.codex\skills\.system\skill-creator\SKILL.md'), 'skill-creator.md', 'creator'),
    (OWNER / 'SKILL.md', 'validator-entrypoint.md', 'validator'),
    (OWNER / 'references/rules.md', 'validator-rules.md', 'rules'),
    (OWNER / 'references/reporting.md', 'validator-reporting.md', 'reporting')]
sources = []
for source, name, ident in inputs:
    copy(source, 'inputs/' + name)
    sources.append({'source_id': ident, 'original_path': str(source), 'retrieved_at_utc': stamp, 'sha256': ref('inputs/' + name)['sha256'], 'snapshot_path': 'inputs/' + name, 'sections': ['Selected complete local document'], 'freshness': 'snapshot_only'})
copy(Path(r'C:\Users\bryan\.codex\skills\.system\skill-creator\scripts\quick_validate.py'), 'inputs/quick_validate.py')
for name in ['semantic-review.md', 'independent-review.md', 'request.md', 'identity-scan.json', 'source-delta.json', 'input-readback.json', 'builder-final.json', 'companion-before.json', 'companion-after.json', 'operational-builder-after.json', 'operational-validator-after.json']:
    copy(RUN / name, 'inputs/' + name)
save('sources.json', {**base, 'sources': sources})

attempts = []
commands = ['# Exact executed commands and retained attempts\n', 'These are actual argument vectors, not suggested shell strings. Raw logs remain beside each original receipt. Earlier failures are preserved and never relabeled.\n']
for family in ['attempts', 'native']:
    for path in sorted((RUN / family).glob('*/receipt.json')):
        value = json.loads(path.read_text())
        label = family + '/' + path.parent.name
        target = 'trials/' + label
        copy(path, target + '/receipt.json')
        for logfile in ['stdout.txt', 'stderr.txt', 'stdout.jsonl']:
            if (path.parent / logfile).exists():
                copy(path.parent / logfile, target + '/' + logfile)
        attempts.append((label, value, target))
        commands.append('## ' + label + '\n\n```json\n' + json.dumps(value.get('command', value), ensure_ascii=False, indent=2) + '\n```\n\nExit: ' + str(value.get('exit_code')) + '; timeout: ' + str(value.get('timed_out')) + '.\n')
text('command-log.md', '\n'.join(commands))

def latest(suffix):
    return [target for label, value, target in attempts if label.endswith('-' + suffix)][-1]

checks = []
rules = []
def check(ident, title, dimension, method, result, reason, evidence, subject='SKILL.md'):
    rule = 'MAINT-' + ident
    source = ref('inputs/governing-spec.md')
    source.update(source_id='governing', locator='Sections 8-9: requirement register and maintenance acceptance cases')
    rules.append({'rule_id': rule, 'revision': '1', 'title': title, 'source_refs': [source], 'authority_class': 'project_policy', 'applicability': 'applicable', 'method': method, 'expected_observation': title, 'required': True, 'limitation': 'Only the named method and retained evidence; no native/framework acceptance implication.'})
    checks.append({**base, 'check_id': ident, 'rule_id': rule, 'subject_path': subject, 'dimension': dimension, 'method': method, 'required': True, 'applicability': 'applicable', 'result': result, 'reason': reason, 'evidence': [ref(x) for x in evidence]})

requirements = [
('BA-001', 'Authoring-only/manual handoff', 'SKILL.md; references/adaptation.md; unchanged authoring.py', 'BAT-01, BAT-12'),
('BA-002', 'Bounded discovery without project execution', 'references/adaptation.md; scripts/adaptive.py; runtime Capture', 'BAT-02, BAT-03'),
('BA-003', 'Evidence-grounded roles and explicit gaps', 'references/adaptation.md; schemas/project-evidence-v1.schema.json; proposal schema; adaptive.py', 'BAT-04, BAT-05'),
('BA-004', 'Source/operational identity separation', 'references/project-binding.md; adaptive descriptor and binding schemas; runtime', 'BAT-06, BAT-07'),
('BA-005', 'Closed schemas, exact digests/references', 'schemas/* new families; scripts/adaptive.py', 'BAT-08, BAT-09'),
('BA-006', 'Sequential selected sets and dependencies', 'references/adaptation.md; adaptive.py; selection/result/request schemas', 'BAT-10, BAT-11'),
('BA-007', 'Core preservation and complete lineage', 'references/adaptive-contracts.md; adaptive.py', 'BAT-05, BAT-13'),
('BA-008', 'Ground expertise and project conventions', 'references/adaptation.md; proposal semantics', 'BAT-04, BAT-14'),
('BA-009', 'Portable descriptors and runtime template', 'assets/adaptive-runtime/check_project_binding.py; descriptor schema; project-binding.md', 'BAT-06, BAT-07, BAT-15'),
('BA-010', 'Explicit update proposals, no automatic repair', 'references/adaptation.md; adaptive.py review branch', 'BAT-13, BAT-16'),
('BA-011', 'Legacy history/schema/custody meanings', 'unchanged scripts/authoring.py, custody.py, build_evidence.py and legacy schemas', 'BAT-09, BAT-11, BAT-17'),
('BA-012', 'Terminal-local capabilities and honest failure', 'references/adaptation.md; project-binding.md; runtime', 'BAT-03, BAT-15'),
('BA-013', 'Discriminating routing and progressive resources', 'SKILL.md; three routed adaptive references', 'BAT-12, BAT-14'),
('BA-014', 'Truthful authoring states, no quality/enforcement claims', 'references/adaptation.md; set schemas; adaptive.py reductions', 'BAT-10, BAT-12, BAT-17')]
for ident, title, paths, cases in requirements:
    check(ident, title, 'instructions' if ident in ('BA-001', 'BA-008', 'BA-012', 'BA-013') else 'workflow', 'semantic', 'PASS', 'Delivered implementation mapped and statically reviewed; this does not mark associated BAT/native cases passed. Paths: ' + paths, ['inputs/semantic-review.md', 'inputs/source-delta.json'])
text('requirement-coverage.md', '# BA implementation mapping\n\nAll fourteen requirements are authored and mapped below. Static delivery PASS is distinct from complete behavioral verification. See case-coverage.md for explicit gaps.\n\n| Requirement | Delivered responsibility | Paths | Cases |\n| --- | --- | --- | --- |\n' + '\n'.join('| ' + ' | '.join(row) + ' |' for row in requirements) + '\n')

check('STRUCTURE', 'Installed creator and existing validator structure', 'standards', 'deterministic', 'PASS', 'Installed quick_validate exits 0; pinned observe structure exits 0, 33 links. Local snapshots only.', [latest('quick') + '/stdout.txt', latest('structure') + '/stdout.txt'])
check('HELPERS', 'New helper positive/negative branch tests', 'workflow', 'deterministic', 'PASS', '21 independent terminal tests passed, including lineage, stale bytes, binding, full/subsets and actual per-member custody. Controller orchestration is scripted.', [latest('helpers') + '/stderr.txt'])
check('LEGACY', 'Original validator regressions against delivered builder', 'workflow', 'deterministic', 'PASS', '202 tests passed against pinned original validator and final builder. Earlier concurrent live companion attempt retained separately.', [latest('legacy-pinned') + '/stderr.txt'])
check('IDENTITY', 'Portable source identity scan and operational preservation', 'workflow', 'deterministic', 'PASS', 'No concrete UUID/root constant or binding copy in 43 source files; both operational digests unchanged. Companion changed externally.', ['inputs/identity-scan.json', 'inputs/operational-builder-after.json', 'inputs/operational-validator-after.json'])
check('CLASSIFY', 'Explicit mode and negative description classification', 'instructions', 'semantic', 'PASS', 'Six independent classifications matched; not native implicit activation.', ['inputs/independent-review.md'])
check('LINUX', 'Selected Linux runtime branch execution', 'behavior', 'behavioral', 'PASS', 'Five selected WSL Ubuntu binding/path/link/relocation tests passed; full-suite Linux ceiling attempt timed out.', [latest('linux') + '/receipt.json', latest('linux') + '/stderr.txt'])
for label, value, target in attempts:
    if not label.startswith('native/') or '085649' in label:
        continue
    case = value['case']
    passed = value.get('exit_code') == 0 and not value.get('timed_out')
    check('NATIVE-' + case, 'Cold ' + case + ' task', 'behavior', 'behavioral', 'PASS' if passed else 'ERROR', 'Completed on retained intermediate builder snapshot; applicable ordinary custody bytes unchanged.' if passed else '120-second timeout; partial trace retained. Required completed native behavior is NOT_RUN.', [target + '/receipt.json', target + '/stdout.jsonl'])
check('IMPLICIT', 'Native implicit activation', 'behavior', 'behavioral', 'NOT_RUN', 'Cold prompts explicitly selected the source entrypoint; no implicit activation trial.', ['inputs/independent-review.md'])
check('NO-PYTHON', 'Missing Python host behavior', 'behavior', 'behavioral', 'NOT_RUN', 'Instructions and capability failure inspected; no interpreter-removal cold host task executed.', ['inputs/semantic-review.md'])
check('DOMAIN', 'BAT-02/BAT-04 complete grounded project proposal', 'behavior', 'behavioral', 'NOT_RUN', 'No completed monorepo/retained HTTP plus storage proposal; manual instruction inspection and helper fixtures are partial evidence only.', ['inputs/semantic-review.md'])
check('INTEGRATION', 'Builder to enhanced validator actual integration', 'behavior', 'behavioral', 'NOT_RUN', 'Companion changed concurrently and no immutable enhanced target was selected. Shared fixtures and pinned old validator are not integration.', ['inputs/companion-before.json', 'inputs/companion-after.json'])
save('rule-set.json', {**base, 'rules': rules})
text('checks.jsonl', ''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in checks))
save('findings.json', {**base, 'findings': [], 'limitation': 'No unresolved material implementation defect established by bounded static review. Explicit coverage gaps remain in checks; no complete independent behavioral assurance.'})
save('origin-record.json', {**base, 'original_source_root': str(ROOT / 'src/agents/skills/skill-builder'), 'manifest': ref('source-manifest.json'), 'specification': ref('inputs/governing-spec.md'), 'origin_kind': 'existing_spec', 'history_kind': 'observed', 'historical_origin': 'unknown', 'prior_evidence': None, 'completeness': 'complete', 'uncertainties': ['This maintenance snapshot is not adoption or a generated baseline.'], 'source_readback_state': 'UNCHANGED'})
steps = []
for ident, entry, action, failure, outcome in [
    ('proposal', 'references/adaptation.md#proposal-and-discovery', 'Capture bounded evidence, resolve retained coverage, write proposal and report.', 'Specific gaps, BLOCKED proposal; preserve independent work.', 'Exact proposal reference and unresolved choices.'),
    ('set', 'references/adaptation.md#sequential-selected-set-authoring', 'Preflight selection, run existing custody sequentially, publish per-member and aggregate records.', 'Block dependents, continue independent members, retain partial effects.', 'Manual full_set or eligible_subset request; no validator invocation.'),
    ('review', 'references/adaptation.md#selected-update-review', 'Compare selected prior/current core and evidence; author impact proposal.', 'Missing or stale inputs become explicit gaps.', 'Linked fresh proposal; no automatic core/variant edits.'),
    ('runtime', 'references/project-binding.md', 'Copied helper checks exact operational binding before product actions.', 'Non-MATCH stops product writes and downstream calls.', 'Sanitized observation and separately authorized setup prerequisite.')]:
    steps.append({'step_id': ident, 'entrypoint': entry, 'entry_conditions': 'Explicitly applicable mode and bounded selected inputs.', 'inputs': ['Current instruction', 'Selected records and files'], 'executor': 'Codex with local terminal; runtime helper where specified', 'action': action, 'outputs': [outcome], 'completion_evidence': 'Retained outputs and exact digest readback', 'next': 'terminal delivery', 'failure_route': failure, 'terminal_user_outcome': outcome})
save('workflow-map.json', {**base, 'steps': steps})
dimensions = {d: ('INCOMPLETE' if any(c['dimension'] == d and c['result'] in ('NOT_RUN', 'ERROR') for c in checks) else 'PASS') for d in ['standards', 'workflow', 'instructions', 'behavior']}
save('assessment.json', {**base, 'assessment_completed': True, 'overall_assessment': 'INCOMPLETE', 'dimensions': dimensions, 'required_checks': len(checks), 'pass_checks': sum(c['result'] == 'PASS' for c in checks), 'coverage_limitation': 'Attempts ending in ERROR are retained, not successful completed native trials.'})
save('handoff.json', {**base, 'builder_readiness': 'NO_CHANGE', 'proposal_review_state': 'not_needed', 'selected_finding_ids': [], 'deferred_finding_ids': [], 'proposed_spec': None, 'target_package_digest': digest, 'report': ref('assessment.json'), 'explanation': 'No additional builder repair selected. This is not a passed assessment or permission to install. Finish missing native/integration checks separately.'})
text('enforcement-recommendations.md', '# Enforcement boundary\n\nPython shape, digest and binding observations provide development evidence. Static safe-path checks are not OS isolation and an editable binding is not protected identity. No Rust authority, privileged gate, installation, hook or immutable acceptance receipt was implemented or qualified. Future Rust enforcement belongs to a separately specified task; this maintenance proposes no additional source change.\n')
print('assessment records:', len(checks), 'required;', sum(c['result'] == 'PASS' for c in checks), 'PASS;', dimensions)
