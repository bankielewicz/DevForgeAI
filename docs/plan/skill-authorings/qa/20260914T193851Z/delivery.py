"""Retain final publication byte readback and delivery notes, not quality results."""
import difflib
import json
import platform
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
PROJECT = RUN.parents[3]
sys.path.insert(0, str(PROJECT / '.agents/skills/skill-builder/scripts'))
import authoring as custody

INPUTS = RUN.with_name(RUN.name + '-inputs')
target = PROJECT / 'src/agents/skills/qa'
record = custody.parse(custody.read_bytes(RUN / 'authoring-record.json'))
published = custody.parse(custody.read_bytes(RUN / 'publication-readback.json'))
request = custody.parse(custody.read_bytes(RUN / 'validation-request.json'))
actual = custody.files(target)
manifest = custody.manifest(actual)
bound_manifest = custody.parse(custody.referenced(record['delivered_manifest']))
before = custody.files(RUN / 'before')
candidate = custody.files(RUN / 'candidate')
operational = custody.manifest(custody.files(PROJECT / '.agents/skills/qa'))
original_operational = custody.parse(custody.read_bytes(INPUTS / 'operational-before-manifest.json'))
for ref in record['inputs']:
    custody.referenced(ref)
readback = {
    'purpose': 'Publication byte custody only; no structural, behavioral or quality assessment.',
    'package_digest': manifest['package_digest'],
    'delivered_matches_bound_manifest': manifest == bound_manifest,
    'delivered_matches_candidate': actual == candidate,
    'operational_copy_unchanged': operational == original_operational,
    'input_references_unchanged': True,
    'file_count': len(actual), 'byte_count': sum(map(len, actual.values())),
    'applied_paths': record['applied_paths'], 'publication': published,
    'validation': 'NOT_PERFORMED', 'testing': 'NOT_PERFORMED', 'framework_acceptance': 'NOT_EVALUATED',
}
custody.save(RUN / 'delivery-readback.json', readback)
if not all([readback['delivered_matches_bound_manifest'], readback['delivered_matches_candidate'], readback['operational_copy_unchanged']]):
    raise ValueError('Delivery or preservation mismatch; inspect retained readback')
diffs = []
for name in record['applied_paths']:
    diffs.extend(difflib.unified_diff(before[name].decode('utf-8').splitlines(True), actual[name].decode('utf-8').splitlines(True), fromfile='before/' + name, tofile='delivered/' + name))
(RUN / 'applied.diff').write_text(''.join(diffs), encoding='utf-8')
commands = [
    {'command': 'python -B -X utf8 docs/plan/skill-authorings/qa/20260914T193851Z-inputs/prepare.py', 'exit_code': 0, 'observed': 'Authoring contract, input references, requirement mapping and external manual evaluation obligations saved.'},
    {'command': 'python -B -X utf8 .agents/skills/skill-builder/scripts/authoring.py begin --contract docs/plan/skill-authorings/qa/20260914T193851Z-inputs/authoring-contract.json --run-root docs/plan/skill-authorings/qa/20260914T193851Z', 'exit_code': 0, 'observed': 'STAGED; prior authored baseline resolved; before and candidate captured.'},
    {'command': 'python -B -X utf8 docs/plan/skill-authorings/qa/20260914T193851Z/stage.py', 'exit_code': 0, 'observed': 'Nine existing resources staged; subsequent focused patch clarified verdict versus stop rules and report-row fields.'},
    {'command': 'python -B -X utf8 .agents/skills/skill-builder/scripts/authoring.py publish --run-root docs/plan/skill-authorings/qa/20260914T193851Z', 'exit_code': 0, 'observed': 'AUTHORED; nine applied paths; no conflicts/issues; baseline/request/readback published.'},
]
custody.save(RUN / 'authoring-command-receipts.json', {'cwd': str(PROJECT), 'host': platform.platform(), 'python': sys.version, 'records': commands, 'scope': 'Authoring and custody commands only. Source Get-Content/rg reads and apply_patch edits are retained in the session tool transcript. No evaluator, test suite, grader, cold trial or product QA ran.'})
mapping = custody.parse(custody.read_bytes(INPUTS / 'requirement-resource-map.json'))
rows = ['| Requirement | Changed or retained resources |', '| --- | --- |']
for req in mapping['requirements'][:14]:
    key = req['outcome'].split(' ', 1)[0].replace('**', '')
    rows.append('| ' + key + ' | ' + ', '.join('`' + p + '`' for p in req['artifacts']) + ' |')
request_hash = custody.reference(RUN / 'validation-request.json')['sha256']
extension_ref, baseline_ref = record['inputs'][:2]
report = f'''# QA post-MVP authoring delivery

Authoring: AUTHORED. Destination: `{target}`.

Updated the existing nine resources for ordinary QA `run` intent, same-invocation planning/preparation/execution, dependency-aware readiness, integrity-first inspection, evidence-based stop classification, complete-collection metric decisions, report/fix ownership and retained resume/retest state. Explicit planning-only, >=95% floors, stricter project policy, independent oracles and platform qualifications remain required. No runtime helper was added.

## Bound inputs and history

- Extension: `{extension_ref['path']}`; SHA-256 `{extension_ref['sha256']}`.
- Companion MVP: `{baseline_ref['path']}`; SHA-256 `{baseline_ref['sha256']}`.
- Precedence: extension only supersedes its listed MVP clauses; all unamended requirements and applicable QV scenarios remain selected.
- Prior authored baseline: `20260914T1748018341005Z`; original package digest `{custody.manifest(before)['package_digest']}`. Its published record and baseline snapshot were verified by the custody helper; prior files remain in place.
- Delivered package: {len(actual)} files, {sum(map(len, actual.values()))} bytes; SHA-256 package digest `{manifest['package_digest']}`.
- All nine paths changed; no additions/removals. See [applied.diff](applied.diff) and [authoring record](authoring-record.json).
- The operational `.agents/skills/qa` manifest matches its pre-authoring capture. Both supplied specifications and all bound source inputs still match their recorded bytes.

## Requirement-to-resource mapping

''' + '\n'.join(rows) + f'''

QA-001 through QA-026 remain the companion contract; unchanged criterion inventory/oracles, source bindings, test-integrity definitions, execution categories, numerical floors, manual dev ownership and independent retest lifecycle remain in their existing references. The bound [manual evaluation obligations](../{INPUTS.name}/manual-evaluation-obligations.md) preserve QV-01 through QV-21 with compatibility amendments and require QPV-01 through QPV-21. These are future evaluation requirements, not executed cases.

## Authoring review and custody

Read the entry instructions, four phase references, all three templates and UI metadata before editing and after staging. Reviewed mode routing, stop versus continuation decisions, complete versus partial metrics, explicit plan non-verdict, artifact-delivery failures, literal path preservation and legacy-plan resume. Existing package-relative links still name the same consumed resources; no new runtime dependency or concrete authoring path was introduced. A requested `rg` prose search found old broad patterns only in ordinary-run lines mentioning planning; those lines were inspected directly. This was authoring text review, not a structural checker or behavioral test.

The publication helper rechecked original input and current package bytes, compared baseline/current/candidate, rechecked each written path and read back the complete delivery before publishing the next baseline. [Delivery readback](delivery-readback.json) independently records byte correspondence and operational preservation. [Command receipts](authoring-command-receipts.json) record exact custody commands, host, interpreter and outcomes.

Validation: NOT_PERFORMED. Testing: NOT_PERFORMED. Framework acceptance: NOT_EVALUATED. No red/green, native-behavior, coverage or skill-acceptance result is claimed. No structural checker, grader, test suite, generated skill sample, cold trial or product QA was executed. No authoring conflict remains. Evaluated-build completeness remains unproven until the separate validator produces and executes the required exact-byte-bound Python bundle.

## Manual validator handoff

Request: `{RUN / 'validation-request.json'}`

Request SHA-256: `{request_hash}`

Use [the generated manual request](validator-request.md), or paste this into a Codex conversation in `{PROJECT}`:

```text
$skill-validator Validate and test C:\\Projects\\DevForgeAI\\src\\agents\\skills\\qa using C:\\Projects\\DevForgeAI\\docs\\plan\\skill-authorings\\qa\\20260914T193851Z\\validation-request.json (SHA-256 {request_hash}). Bind the exact delivered package and both selected specifications. Apply qa-skill-postmvp-spec.md precedence over qa-skill-spec.md only where amended; retain applicable QV-01 through QV-21 and add QPV-01 through QPV-21. Read the bound manual-evaluation-obligations.md input. Produce and execute the mandatory Python JSONL runner, deterministic graders, independent fixtures/expected results, schema, runtime/dependency information and digests/manifests in fresh evidence. Observe actual continuation and stop ordering with test-launch markers. Preserve old evidence and source; do not repair or install the skill. Report unavailable coverage honestly and retain compiled-Rust authority boundaries.
```

The request is a manual assessment proposal; the builder has not invoked it. Existing historical validation results do not qualify these edited bytes.
'''
(RUN / 'DELIVERY.md').write_text(report, encoding='utf-8')
custody.save(RUN / 'delivery-artifacts.json', {'artifacts': [custody.reference(RUN / name) for name in ['DELIVERY.md', 'delivery-readback.json', 'applied.diff', 'authoring-command-receipts.json', 'validator-request.md', 'validation-request.json']]})
print(json.dumps(readback, ensure_ascii=False))
