"""Final read-only target verification and new delivery evidence; no package writes."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import sys

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
OUT = RUN / 'final-readback'
OUT.mkdir(exist_ok=False)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path):
    return {p.relative_to(path).as_posix(): {'bytes': p.stat().st_size, 'sha256': digest(p)}
            for p in sorted(path.rglob('*')) if p.is_file()}

def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

spec = ROOT / 'docs/plan/skill-builder-authoring-enhancement-spec.md'
assert digest(spec) == '43054bf9b3f97d48d479aeed2fe7b119629e6e717f0a55e1835714182844cb14'
summary = json.loads((RUN / 'verification-summary.json').read_text())
observer = ROOT / '.agents/skills/skill-validator/scripts/observe.py'
assert inventory(observer.parent.parent) == inventory(RUN / 'inputs/operational-validator')
receipt = {'schema_version': 'delivery-receipt-v1', 'timestamp_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
           'status': 'DELIVERED_DEVELOPMENT_ASSESSED', 'spec_sha256': digest(spec),
           'assessment_method': 'Primary author follows frozen operational validator; independent builder review and bounded cold workflows separately attributed.',
           'verification': {k: summary[k] for k in ('full_regression', 'supplemental_authoring_input_capture', 'structural', 'routing', 'scope')},
           'targets': {}}
for name in ('skill-builder', 'skill-validator'):
    target = ROOT / 'src/agents/skills' / name
    actual = inventory(target)
    assert actual == inventory(RUN / 'candidate' / name)
    assert actual == inventory(RUN / 'assessments' / name / 'source')
    if name == 'skill-builder':
        assert actual == inventory(RUN / 'operational-revalidation/skill-builder')
    argv = [sys.executable, '-B', '-X', 'utf8', str(observer), 'readback', '--source', str(target),
            '--manifest', str(RUN / 'assessments' / name / 'source-manifest.json')]
    write(OUT / (name + '-plan.json'), {'argv': argv, 'cwd': str(ROOT), 'timeout_seconds': 120})
    p = subprocess.run(argv, cwd=ROOT, capture_output=True, timeout=120)
    (OUT / (name + '-stdout.json')).write_bytes(p.stdout)
    (OUT / (name + '-stderr.txt')).write_bytes(p.stderr)
    write(OUT / (name + '-exit.json'), {'exit_code': p.returncode})
    result = json.loads(p.stdout)
    assert p.returncode == 0 and result['status'] == 'MATCH', result
    integrity = json.loads((RUN / 'assessment-commands' / (name + '-records-001-stdout.json')).read_text())
    assert integrity['errors'] == [], integrity
    before = json.loads((RUN / 'inputs' / (name + '-manifest.json')).read_text())['files']
    delta = {'added': sorted(set(actual) - set(before)), 'removed': sorted(set(before) - set(actual)),
             'modified': sorted(k for k in set(actual) & set(before) if actual[k] != before[k])}
    write(OUT / (name + '-file-delta.json'), delta)
    manifest = json.loads((RUN / 'assessments' / name / 'source-manifest.json').read_text())
    receipt['targets'][name] = {'target': str(target), 'package_digest': manifest['package_digest'],
        'readback': 'MATCH', 'record_integrity_errors': [], 'file_delta_counts': {k: len(v) for k, v in delta.items()},
        'authoring_record': 'authoring/' + name + '/authoring-record.json',
        'authoring_baseline': 'authoring/' + name + '/authoring-baseline.json',
        'manual_handoff': 'authoring/' + name + '/validator-request.md',
        'assessment': 'assessments/' + name + '/validation-report.md'}

report = '''# Delivered skill authoring enhancement

Implemented AB-001 through AB-014 in the two development packages against approved specification SHA-256 `43054bf9b3f97d48d479aeed2fe7b119629e6e717f0a55e1835714182844cb14`. Final target readbacks match the assessed source snapshots. This is development delivery and bounded assessment, not installation, native qualification or framework acceptance.

## Package changes

- **skill-builder:** conversational creation, portable destination selection, focused edits with or without builder history, bundled scaffolding and UI metadata helpers, proportionate resources, distinct versioned authoring records/baselines, and a digest-bound manual validator request. Custody still verifies origin, source drift, ownership, conflicts, safe writes, partial failures and readback. The resulting workflow performs no quality checks, generated-skill tests or automatic validator invocation.
- **skill-validator:** owns the transferred evaluation scripts, graders, schemas, profiles, fixtures and regression tests. New read-only authoring intake verifies request, record and current target bindings before assessment and rejects stale handoffs. Instructions and reports separate authoring, assessment, native execution and acceptance.

Exact added/modified/removed file lists are in [builder delta](final-readback/skill-builder-file-delta.json) and [validator delta](final-readback/skill-validator-file-delta.json). Bundled Skill Creator adaptations retain source notice/license; they have no runtime dependency on the personal installation path.

## Migration and provenance

Existing origins and baselines were inspected before mutation; see [history check](history-check.json). The actual builder schema-2 revision and validator schema-1 build matched their retained historical evidence. Legacy schema-1/schema-2 meanings remain unchanged. Their evaluator implementations and compatibility coverage moved to validator ownership; original validator routing cases remain separately named `validator-cases.jsonl`.

New `authoring-contract-v1`, `authoring-v1`, `authoring-baseline-v1` and `validation-request-v1` records distinguish authoring from quality results. Original authoring records retain NOT_PERFORMED quality statuses; subsequent assessment is separate. No history was invented or silently adopted.

| Package | Authoring record | Baseline | Manual request | Actual-byte assessment |
| --- | --- | --- | --- | --- |
| Builder | [record](authoring/skill-builder/authoring-record.json) | [baseline](authoring/skill-builder/authoring-baseline.json) | [request](authoring/skill-builder/validator-request.md) | [report](assessments/skill-builder/validation-report.md) |
| Validator | [record](authoring/skill-validator/authoring-record.json) | [baseline](authoring/skill-validator/authoring-baseline.json) | [request](authoring/skill-validator/validator-request.md) | [report](assessments/skill-validator/validation-report.md) |

## Acceptance scenario results

All planned applicable AC checks passed in the combined assessment. These labels do not imply that every method of testing was performed.

| Scenario | Result and evidence |
| --- | --- |
| AC-01 | PASS: independent conversational creation from a realistic request, without a separate specification. |
| AC-02 | PASS: independent ambiguity trial requested material decisions before generation. |
| AC-03 | PASS: supplied destination with spaces honored; missing location prompted a resolved project recommendation. |
| AC-04 | PASS: executed initializer rejects occupied destination and preserves its sentinel. |
| AC-05 | PASS: independent no-history edit limits changes and preserves unrelated reference/UI values. |
| AC-06 | PASS: a second independent edit uses the previous untested authoring baseline. |
| AC-07 | PASS: ownership, source drift, collisions, interrupted writes and publication failures exercised; safe partial outcome retained. |
| AC-08 | PASS: executed metadata edits preserve unrelated policy/dependency/color values; explicit policy changes tested. |
| AC-09 | PASS: proportionate one-file skill and concrete import resources; supported metadata preservation revalidated independently. |
| AC-10 | PASS: independent builder traces perform authoring only; quality code/tests transferred. |
| AC-11 | PASS: separate enhanced-validator invocation accepts the manual handoff and tests its synthetic target; stale bindings rejected in delivered regressions. |
| AC-12 | PASS: fresh legacy compatibility regressions and verified real historical origins; no reinterpretation of old success. |
| AC-13 | PASS: builder trials complete without validator loading; requests remain available for later manual invocation. |
| AC-14 | PASS: reports distinguish structural, deterministic, routing, independent execution, self-assessment and native coverage. |

Detailed evidence references and digest bindings for each scenario are in both package assessment directories, including `checks.jsonl`, `rule-set.json`, `sources.json` and `assessment.json`.

## Fresh verification and retained failures

- **202 regression tests passed**, zero failures/errors/skips on delivered bytes: [run](checks-005-delivered/). A supplemental run repeats the **28 authoring tests** with additional raw-input capture: [run](checks-006-authoring-inputs/). These are not 230 unique tests.
- Skill Creator's structural checker and the unchanged operational validator's structural observer passed for **both packages (4/4)**: [results](structural-003-delivered/).
- Independent routing classification matched **14/14** cases: [trial](independent-trials/routing/). Classification does not establish native activation.
- Independent operational builder assessment initially raised three findings. All three were repaired; **12 fresh revalidation cases passed** on the final builder bytes: [response](operational-revalidation/response.md). Its standalone report remains INCOMPLETE for coverage outside its assigned subtask; this combined assessment adds separately retained evidence.
- Independent cold workflows cover conversation, ambiguity, no-history editing, an untested follow-up edit, import and enhanced-validator execution: [raw trials](independent-trials/). Snapshot differences from final delivery are disclosed in [verification summary](verification-summary.json).
- Operational record-integrity checks report no errors for either final assessment; [final readbacks](final-readback/) are MATCH.
- Earlier structural/test/assessment failures and retries remain in their original fresh run directories. The enhanced-validator trial retains a **FAIL in the synthetic imported decimal helper**: a long decimal input rounds under its inherited default Decimal context. It is not an unresolved defect in either delivered enhancement package, and no unauthorized fixture repair was performed.
- Delivery used in-process `authoring.publish` from `deliver.py`. The original CLI-equivalent receipt is preserved with its explicit [correction](delivery-receipt-correction.json). Initial schema-1 preparation failure and corrected retry remain `delivery-preparation.json` and `delivery-preparation-002.json`.

## Scope and limitations

The audit records 96 changed file paths and zero unauthorized changes among 20,456 inventoried preexisting files. Inventoried operational copies, supplied documents and historical evidence remain unchanged. [Scope audit](scope-readback.json) lists 13 excluded task/backup/link boundaries; their contents were not byte-audited, and excluded path sets remained identical. New task evidence is contained in this directory.

No native implicit activation, separate cold specification-only campaign, other OS/runtime qualification, dependency/skill installation, hooks/CI, Rust implementation, OS-enforced isolation or framework acceptance was performed. Existing specification/import/adoption/regeneration compatibility was freshly tested in the regression suite. The primary author assessed the development validator using the unchanged operational validator instructions; independent execution of the enhanced validator on a separate target is not an independent full source audit or its self-review. Final structural/regression checks and readback use actual delivered bytes; earlier cold trials use disclosed frozen snapshots.

The machine-readable [final receipt](FINAL-RECEIPT.json) binds package digests, reports, verification and scope. Exact commands, input snapshots, outputs, failures and retries remain under this evidence root.
'''
(RUN / 'REPORT.md').write_text(report, encoding='utf-8')
receipt['report_sha256'] = digest(RUN / 'REPORT.md')
receipt['assessment_report_sha256'] = {n: digest(RUN / 'assessments' / n / 'validation-report.md') for n in receipt['targets']}
receipt['limitations_reference'] = 'REPORT.md#scope-and-limitations'
write(RUN / 'FINAL-RECEIPT.json', receipt)
print(json.dumps({'status': receipt['status'], 'targets': receipt['targets']}, indent=2))
