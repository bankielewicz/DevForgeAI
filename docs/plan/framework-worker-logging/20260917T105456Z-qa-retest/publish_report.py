"""Publish the completed independent retest assessment; no product operations."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = Path('C:/Projects/DevForgeAI')
CANDIDATE = PROJECT / 'devforgeai/experiments/codex-worker-probe-logging-qa-fixes'
OLD = ROOT.parent / '20260917T023835Z-qa'
DEV = ROOT.parent / '20260917T102726Z-dev-qa-fixes'


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(path):
    return {'path': str(path), 'bytes': path.stat().st_size, 'sha256': sha(path)}


def write(name, value):
    with (ROOT / name).open('x', encoding='utf-8', newline='\n') as stream:
        if isinstance(value, str):
            stream.write(value)
        else:
            json.dump(value, stream, indent=2, ensure_ascii=True)
            stream.write('\n')


metrics = load(ROOT / 'metrics.json')
cases = load(ROOT / 'case-results.json')
attempts = load(ROOT / 'attempt-index.json')
assert metrics['verdict'] == 'PASS' and len(cases) == 178
assert all(case['status'] == 'PASS' for case in cases)
assert len(attempts) == 23 and not (ROOT / 'STOP.json').exists()
assert load(ROOT / 'final-preservation.json')['problems'] == []
assert sha(DEV / 'handoff-manifest.json') == '1e4e0800a737f07d658a50383ccdf98c6aa5237c73675d2539ccb7689065f9f5'
declared_ids = {case['id'] for case in cases}


def selected(*groups):
    result = []
    for group in groups:
        if isinstance(group, tuple):
            result += [f'PKG-{number:03d}' for number in range(group[0], group[1] + 1)]
        else:
            result.append(group)
    assert set(result) <= declared_ids
    return list(dict.fromkeys(result))


criteria = []


def criterion(ids, source, requirement, case_ids, actual, evidence, expected=None):
    criteria.append({
        'criterion': ids, 'source': source, 'requirement': requirement,
        'cases': case_ids, 'expected': expected or requirement,
        'actual': actual, 'status': 'PASS', 'scope': 'selected offline Windows retest',
        'evidence': evidence,
    })


criterion('QA-LOG-01; LG-02/03/06; LD-12', 'logging-contract; logging-design; original QA finding',
    'Successful current records require complete drain, both EOF observations, no reader error and no byte overflow.',
    selected('QA-09', (153, 159), 'RT-01', 'RT-02'),
    'Original drain/EOF/reader-error/overflow defects reject; both streams and all levels reject in the CLI matrix, including synthetic preflight interpretation. Positive and honest failure/history controls pass.',
    ['original-defect-retest.json', 'attempts/13-qa09/receipt.json', 'rt-01-observations.json', 'rt-02-observations.json'])
criterion('QA-LOG-02; LG-02/06; base sections 4/7', 'logging-contract; worker feasibility; original QA finding',
    'Require a typed post-stop worker_exit_code key; current successful terminals require matching observed zero exits.',
    selected('QA-09', (153, 157), (160, 162), 'RT-01', 'RT-02'),
    'Original missing-key and 29-versus-0 defects reject. Missing/null/type/range/contradiction/duplicate negatives reject for success; explicit null and observed nonzero failure controls remain inspectable.',
    ['original-defect-retest.json', 'rt-01-observations.json', 'rt-02-observations.json'])
criterion('LG-01; LD-09', 'logging-contract; logging-design',
    'Closed schema, literal config paths, 4096-byte bound, exact copied digest and final drift check.',
    selected((70, 72), (79, 81), 'QA-01', 'QA-02'),
    'Fresh denial, exact-boundary, real junction, copied-byte digest and legacy composition checks passed.',
    ['attempts/03-coverage/receipt.json', 'attempts/05-qa01/receipt.json', 'attempts/06-qa02/receipt.json'])
criterion('LG-02; LD-01/02/05', 'logging-contract; logging-design',
    'Ordered pre/post exit evidence and joined-reader capture; enforce success consistency when inspecting.',
    selected('PKG-074', 'PKG-093', 'PKG-143', 'SUP-01', 'QA-03', 'QA-04', 'QA-09', 'RT-01'),
    'Actual early exits and reader completion passed; previously accepted contradictory successful records now reject.',
    ['attempts/03-coverage/receipt.json', 'attempts/07-qa03/receipt.json', 'attempts/08-qa04/receipt.json', 'original-defect-retest.json', 'rt-01-observations.json'])
criterion('LG-03; LD-03/04/06/11 capture slice', 'logging-contract; logging-design',
    'Bounded independent pumps, exact full-byte hashes, explicit incomplete capture and rejection of incomplete successful observations.',
    selected((1, 4), 'PKG-073', 'PKG-097', 'PKG-126', 'SUP-01', 'QA-04', 'QA-05', 'QA-09', 'RT-01'),
    'Independent fixed UTF8/raw-byte/final-line hashes, budgets and drain checks passed; inconsistent successful summaries reject.',
    ['attempts/08-qa04/receipt.json', 'attempts/09-qa05/receipt.json', 'attempts/20-supplement/receipt.json', 'original-defect-retest.json', 'rt-01-observations.json'])
criterion('LG-04; LD-06/07/08/11 sink slice', 'logging-contract; logging-design',
    'Four levels, closed data, fixed optional sink/caps, privacy and mandatory evidence failure precedence.',
    selected((5, 6), (38, 41), 'PKG-069', 'PKG-077', 'QA-06', 'QA-07', 'QA-08'),
    'Level/privacy/canary and actual optional/mandatory write-failure assertions passed without changing cleanup semantics.',
    ['attempts/03-coverage/receipt.json', 'attempts/10-qa06/receipt.json', 'attempts/11-qa07/receipt.json', 'attempts/12-qa08/receipt.json'])
criterion('LG-05; LD-01/02/08 classification slice', 'logging-contract; logging-design',
    'Only two known startup Error patterns classify; lookalikes remain unclassified and truncation is explicit.',
    selected((1, 4), 'PKG-074', 'QA-03', 'QA-04', 'QA-05'),
    'Fresh positive/negative byte oracles passed; no native crash diagnosis is inferred.',
    ['attempts/07-qa03/receipt.json', 'attempts/08-qa04/receipt.json', 'attempts/09-qa05/receipt.json'])
criterion('LG-06; LD-12; history/pagination compatibility', 'logging-contract; logging-design; base inspection contract',
    'Validate current capture/status/log evidence across pagination while retaining sound historical and interrupted-prefix semantics.',
    selected('PKG-006', (75, 76), 'PKG-084', 'PKG-092', 'PKG-144', (153, 162), 'QA-09', 'QA-10', 'RT-01', 'RT-02'),
    'All nine original mutations reject as specified; both initial/end cursors preserve validation. Legacy, failure, dropped-detail and interrupted-prefix controls passed.',
    ['original-defect-retest.json', 'attempts/14-qa10/receipt.json', 'rt-01-observations.json', 'rt-02-observations.json'])
criterion('LG-07', 'logging-contract; restrictive policy contract',
    'Only the 15 policy key quote pairs change; 116 argv positions/values and review binding stay exact.',
    selected('PKG-045', (67, 68), (78, 81), 'QA-11'),
    'Independent literal vector comparison and schema3/native-profile composition denials passed without native launch.',
    ['attempts/03-coverage/receipt.json', 'attempts/15-qa11/receipt.json'])
criterion('LG-08; repository quality floors', 'logging-contract; AGENTS.md',
    'All mandatory selected cases, real query_failed checks, independent evidence, valid numeric floors and formatting/static checks pass.',
    selected((1, 162), 'SUP-01', *[f'QA-{number:02d}' for number in range(1, 14)], 'RT-01', 'RT-02'),
    '178/178 required cases, 49/49 units, 3872/4057 lines; build, fmt and Clippy passed.',
    ['case-results.json', 'metrics.json', 'attempt-index.json', 'coverage-analysis.json'])
criterion('DFF-WORKER-FEAS-01 sections 3..7; WF-01..08; LD-10', 'worker feasibility; logging-design',
    'Strict wire subset, policy gates, correlation, single turn and independent result oracle.',
    selected('PKG-050', (57, 68), 'PKG-086', (88, 91), (98, 125), 'QA-08', 'QA-11', 'QA-12'),
    'Fresh offline trace/denial/oracle assertions passed.',
    ['attempts/03-coverage/receipt.json', 'attempts/12-qa08/receipt.json', 'attempts/15-qa11/receipt.json', 'attempts/16-qa12/receipt.json'])
criterion('WF-09..12; F-01/F-02; base section 7', 'worker feasibility; inherited recovery regressions',
    'Exclusive persistence, intent before effect, no replay and honest read-only inspection.',
    selected('PKG-082', 'PKG-084', (128, 144), 'PKG-149', (153, 162), 'QA-09', 'QA-10', 'QA-12', 'RT-01', 'RT-02'),
    'Fresh persistence/recovery tests passed; read-only CLI byte snapshots match and inconsistent success is rejected.',
    ['attempts/03-coverage/receipt.json', 'original-defect-retest.json', 'rt-01-observations.json', 'rt-02-observations.json'])
criterion('WF-13..16', 'worker feasibility Windows process ownership',
    'Owned process-tree teardown on Ctrl+C/EOF/owner death and real production watchdog.',
    selected('PKG-085', (93, 97), 'PKG-132', 'PKG-133', 'PKG-135', 'PKG-137', 'PKG-142', 'QA-03', 'QA-04', 'QA-05'),
    'Actual Windows child/Job Object/descendant tests passed, including the fixed 120-second watchdog.',
    ['attempts/03-coverage/receipt.json', 'attempts/07-qa03/receipt.json', 'attempts/08-qa04/receipt.json', 'attempts/09-qa05/receipt.json'])
criterion('WF-17..20', 'worker feasibility failure and preservation obligations',
    'Reject unsafe input, oracle mismatch and fixture drift; retain evidence/cleanup precedence.',
    selected((52, 55), 'PKG-087', 'PKG-145', (147, 151), 'QA-01', 'QA-02', 'QA-07', 'QA-12'),
    'Fresh denied/failure-path and preserved-byte assertions passed.',
    ['attempts/03-coverage/receipt.json', 'attempts/05-qa01/receipt.json', 'attempts/06-qa02/receipt.json', 'attempts/11-qa07/receipt.json', 'attempts/16-qa12/receipt.json'])
criterion('NI-T01..10 offline; preflight companion', 'native-readiness; preflight contract',
    'Exact launcher junction/digest, fixed policy, source review and no-work preflight restrictions in synthetic offline fixtures.',
    selected((7, 15), (42, 48), (67, 68), (79, 81), (90, 92), (98, 115), 'PKG-138', 'QA-11', 'QA-12'),
    'Offline identity/review denials and preflight interpretation passed. Installed/native behavior is unqualified.',
    ['attempts/03-coverage/receipt.json', 'attempts/15-qa11/receipt.json', 'attempts/16-qa12/receipt.json'])
criterion('SI-T01..08', 'source-identity companion',
    'Single allowed source junction, complete source inventory and drift/final checks.',
    selected((16, 35), 'PKG-042', 'PKG-044', 'PKG-046', 'PKG-049', 'PKG-152', 'QA-11', 'QA-13'),
    'Real synthetic Windows junction and stale/malformed source tests passed.',
    ['attempts/03-coverage/receipt.json', 'attempts/15-qa11/receipt.json', 'attempts/17-qa13/receipt.json'])
criterion('SI-T09', 'source-identity inherited obligations',
    'Source limits, credentials, policy/identity and WF/F-01/F-02 remain valid with corrected inspection.',
    selected((7, 49), 'PKG-098', (128, 162), 'QA-09', 'QA-11', 'QA-12', 'QA-13', 'RT-01', 'RT-02'),
    'Inherited source restrictions and corrected current/history inspection all passed.',
    ['attempts/03-coverage/receipt.json', 'original-defect-retest.json', 'rt-01-observations.json', 'rt-02-observations.json'])
criterion('SI-T10 offline preservation slice; OUT-01', 'source-identity; selected preservation boundary',
    'Preserve corrected/failed/original/snapshot sources, inputs, old evidence and unchanged PowerShell helper.',
    selected('QA-13'),
    '68 corrected, 183 preserved source and 108 input bindings unchanged; 3689 prior QA and 9691 dev evidence files verified, plus binaries and 212 protected matrix seed files.',
    ['attempts/17-qa13/receipt.json', 'final-preservation.json'])
criterion('Diagnostic v1 all stages; query_failed addendum', 'diagnostic contract',
    'Same held-job guard, real query failure/null counts/no RPC, privacy and closed category precedence.',
    selected((36, 41), 'PKG-056', (101, 106), 'QA-08', 'QA-12'),
    'Fresh real restricted-handle QueryInformationJobObject error and null-count/no-work/cleanup assertions passed.',
    ['attempts/03-coverage/receipt.json', 'attempts/12-qa08/receipt.json', 'attempts/16-qa12/receipt.json', 'integrity.md'])
criterion('Documentation review', 'README, eight bound contracts and development delivery',
    'Factual scope/schema/acceptance statements and resolvable local Markdown links.',
    selected('QA-13'),
    'Ten documents and 60 local links reviewed; no broken local targets or native/authority acceptance inferred.',
    ['documentation-review.json'])
criteria.append({
    'criterion': 'NI-T11/12; WN-01/02; installed-profile qualification',
    'source': 'native-readiness and worker feasibility native contracts',
    'requirement': 'Actual native launch, installed-profile and operator evidence require separate selection.',
    'cases': [], 'expected': 'Excluded from the selected 178-case offline denominator.',
    'actual': 'NOT_RUN; native Codex was not launched.', 'status': 'NOT_APPLICABLE',
    'scope': 'Outside selected offline retest', 'evidence': ['plan.md'],
})
write('criterion-results.json', criteria)

now = datetime.now(timezone.utc).isoformat()
original = {item['id']: item for item in load(OLD / 'findings.json')}
resolutions = {item['id']: item for item in load(DEV / 'resolution-map.json')}
findings = []
for number in [1, 2]:
    finding_id = f'QA-LOG-{number:02d}'
    findings.append({
        'id': finding_id, 'state': 'VERIFIED_FIXED', 'original_classification': 'MANDATORY_PRODUCT_DEFECT',
        'original_summary': original[finding_id]['summary'],
        'requirements': resolutions[finding_id]['requirements'],
        'candidate_manifest': binding(ROOT / 'candidate-manifest.json'),
        'runtime_source': binding(CANDIDATE / 'src/journal.rs'),
        'rebuilt_probe': binding(ROOT / 'build-target/debug/devforgeai-codex-worker-probe.exe'),
        'independent_cases': ['QA-09', 'RT-01', 'RT-02'],
        'development_regression_cases': ['PKG-158', 'PKG-159', 'PKG-153'] if number == 1 else ['PKG-160', 'PKG-161', 'PKG-162'],
        'closure_evidence': ['original-defect-retest.json', 'rt-01-observations.json', 'rt-02-observations.json', 'case-results.json', 'metrics.json', 'integrity.md'],
        'verified_utc': now,
        'closure_scope': 'Independent Windows offline record-inspection correction and selected regressions only; synthetic preflight is interpretation evidence.',
        'native_codex': 'NOT_RUN', 'framework_acceptance': 'NOT_EVALUATED',
    })
write('findings.json', findings)
write('defect-lifecycle.json', [{
    'id': finding['id'], 'current_state': 'VERIFIED_FIXED',
    'transitions': [
        {'state': 'OPEN', 'run': OLD.name, 'evidence': binding(OLD / 'findings.json'), 'note': 'Original independent mandatory defects; original evidence remains unchanged.'},
        {'state': 'FIX_REPORTED', 'run': DEV.name, 'evidence': binding(DEV / 'resolution-map.json'), 'handoff': binding(DEV / 'handoff-manifest.json'), 'note': 'Development correction claim; no QA closure credited.'},
        {'state': 'VERIFIED_FIXED', 'run': ROOT.name, 'verified_utc': now, 'evidence': binding(ROOT / 'findings.json'), 'note': 'Original failure cases, fresh independent CLI matrices and affected full regressions passed; integrity and all mandatory metric floors satisfied.'},
    ],
    'prior_records_preserved': True, 'framework_acceptance': 'NOT_EVALUATED',
} for finding in findings])

prompt = f'''Open C:\\Projects\\DevForgeAI in native Windows PowerShell. Prepare only the next native worker diagnostic plan and review handoff for {CANDIDATE}. Read current AGENTS.md and the independent offline QA report at {ROOT / 'qa-report.md'}. Verify {ROOT / 'handoff-manifest.json'} and its entries for qa-report.md, candidate-manifest.json, specification-bindings.json and defect-lifecycle.json before using the candidate. Follow the bound native-readiness, preflight, source-identity and logging contracts; identify the required operator review, exact launch prerequisites, bounded commands and evidence destination. Preserve candidate, snapshots, prior evidence and PowerShell helper. Do not launch native Codex, install anything, change configuration, invent operator findings or issue framework acceptance in this planning task. Report unresolved prerequisites and provide the concrete request for a separately selected native trial.\n'''
write('next-review-prompt.txt', prompt)

specs = load(ROOT / 'specification-bindings.json')
spec_rows = '\n'.join(f"| `{item['path']}` | `{item['sha256']}` |" for item in specs)


def compact_cases(case_ids):
    groups = []
    for prefix in ['PKG', 'SUP', 'QA', 'RT']:
        numbers = sorted(int(case_id.split('-')[1]) for case_id in case_ids if case_id.startswith(prefix + '-'))
        width = 3 if prefix == 'PKG' else 2
        cursor = 0
        while cursor < len(numbers):
            first = last = numbers[cursor]
            cursor += 1
            while cursor < len(numbers) and numbers[cursor] == last + 1:
                last = numbers[cursor]
                cursor += 1
            label = f'{prefix}-{first:0{width}d}'
            if last != first:
                label += f'..{last:0{width}d}'
            groups.append(label)
    return ', '.join(groups) or 'Outside selected denominator'


criterion_rows = '\n'.join(
    f"| {row['criterion']} ({row['source']}) | {row['requirement']} | "
    + compact_cases(row['cases']) + f" | {row['expected']} | {row['actual']} | {row['status']} | "
    + '; '.join(f'[{name}]({name})' for name in row['evidence']) + ' |'
    for row in criteria
)
report = f'''# Independent QA retest report

**PASS for the selected Windows offline retest. QA-LOG-01 and QA-LOG-02 are VERIFIED_FIXED.** All 178 required cases passed, including 49 units. Fresh executed-line coverage is 3872/4057 (95.43998028099580971160956372%). Native Codex is NOT_RUN; framework acceptance is NOT_EVALUATED.

## Identity and scope

- Run: {ROOT.name}; mode **retest**; plan readiness **READY**; execution **COMPLETED**; QA verdict **PASS**. No unresolved selected prerequisite or mandatory offline case remains.
- Project: `{PROJECT}`. Candidate: `{CANDIDATE}`. Windows x64, Microsoft Windows 10.0.26200, native C: filesystem; native PowerShell 7.6.6. Git metadata is absent.
- Plan: `{ROOT / 'plan.md'}`; SHA256 `{sha(ROOT / 'plan.md')}`. [plan-binding.json](plan-binding.json) binds the exact original plan, cases, source and inputs. Its initial NOT_STARTED wording is retained; [checkpoint.json](checkpoint.json) records completion.
- QA candidate manifest: `{ROOT / 'candidate-manifest.json'}`; SHA256 `{sha(ROOT / 'candidate-manifest.json')}`; 68 files. The independently recomputed [changed-files.json](changed-files.json) has exactly README.md, src/journal.rs and added tests/inspection_consistency.rs. The other 65 files match the failed candidate.
- Rebuilt probe: `{ROOT / 'build-target/debug/devforgeai-codex-worker-probe.exe'}`; SHA256 `{sha(ROOT / 'build-target/debug/devforgeai-codex-worker-probe.exe')}`. [binary-manifest.json](binary-manifest.json) and [independent-binary-manifest.json](independent-binary-manifest.json) bind executable identities. No prior binary's results are credited to this candidate.
- Development handoff: `{DEV / 'handoff-manifest.json'}`; supplied and verified SHA256 `1e4e0800a737f07d658a50383ccdf98c6aa5237c73675d2539ccb7689065f9f5`. Its FIX_REPORTED states were inputs to this independent retest.
- Requested scope: both inspector corrections, affected logging/recovery/history regressions, integrity, offline Windows numeric floors, build/fmt/Clippy, documentation and preservation. Native WN-01/02, NI-T11/12, installed-profile collection, rendered UI, installation/deployment and protected acceptance are outside this invocation. No product or developer-test edits occurred.
- Decision basis: original independent failures now reject; positive and honest historical/failure controls pass; all fresh required behavior and static checks pass. This is a QA assessment, not an authoritative framework or release decision.

Exact contract bytes are bound in [specification-bindings.json](specification-bindings.json); dependency reading does not select native execution. The logging contract in the preserved failed candidate is byte-identical to the corrected copy.

| Specification path | SHA256 |
| --- | --- |
{spec_rows}

## Acceptance traceability

The complete machine-readable map is [criterion-results.json](criterion-results.json); [required-cases.json](required-cases.json) retains the declared 178 identities and [case-results.json](case-results.json) records their terminal results. PKG-001..152 preserve the original case IDs; PKG-153..162 are the ten correction regressions. Every selected criterion is accounted for below. RT-01/02 contain 145 conjunctive subcases and 435 control/cursor observations; these count as two required cases, not 435 additional passes.

| Criterion and source | Required behavior | Case IDs | Expected result | Actual result | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
{criterion_rows}

## Test integrity

The bounded review is retained in [integrity.md](integrity.md). Prior source/test integrity inspection was reused only for 65 verified byte-identical files; current dependency/include composition and corrected-root admission were checked. All changed journal control flow, unchanged Capture::validate and all 453 lines of the new tests were read. Built-in test attributes, imports, helpers, assertions, real library/CLI calls and before/after byte checks were inspected. No prohibited mock decorator, analogous mocking attribute, skipped case, weakened oracle or coverage suppression was found in the selected scope. No unresolved dynamic wrapper remains. This was not an exhaustive repository security scan.

The original independent Rust harness and fixed literal byte oracles were copied with only corrected-candidate path changes, documented in [helper-provenance.json](helper-provenance.json). Fresh execution supplies the results. The new CLI helper was read before use and its frozen plan binds expected states/errors independently of the inspector. It borrows fresh positive record bytes solely as seeds, first requires an accepted control, mutates one planned condition, verifies exact CLI status/error and checks read-only byte snapshots. [cli-matrix-plan-v2.json](cli-matrix-plan-v2.json) binds all 145 selections and 212 protected seed-file hashes. Raw outputs were independently reread by assess.py; no helper-authored PASS alone establishes the assessment.

One demonstrated preparation error, QA-H01, required a bounded helper-only correction. Its original helper, failed control and receipt remain intact; the v2 matrix retains exactly the same entries/oracles. See the gap and continuation sections. Synthetic preflight journals prove interpretation only. Python records and aggregates evidence; compiled Rust executes product behavior. Neither this report nor Python issues framework acceptance.

## Metrics and environments

| Platform | Metric | Numerator | Denominator | Exact percentage | Required floor | Result | Raw evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Windows x64 (also overall selected scope) | First-party executed lines | 3872 | 4057 | 95.43998028099580971160956372% | >=95% | PASS | [coverage.json](coverage.json), [coverage-analysis.json](coverage-analysis.json) |
| Windows x64 (also overall) | Required unit cases | 49 | 49 | 100% | >=95% | PASS | [package-results.json](package-results.json), [03-coverage stdout](attempts/03-coverage/stdout.txt) |
| Windows x64 (also overall) | All required behavioral cases | 178 | 178 | 100% | >=95% plus no mandatory failures | PASS | [case-results.json](case-results.json), [metrics.json](metrics.json) |

The executable-line fraction is exactly 3872/4057; the percentage above is a decimal rendering. Floor decisions use the unrounded counts. All 15 first-party src/*.rs files were declared before execution; 14 have executable lines and lib.rs is declaration-only. Test/support fixtures and third-party dependencies are excluded, with no uncovered first-party behavior excluded. [source-denominator.json](source-denominator.json) and the raw LLVM file inventory bind this denominator.

Coverage came only from the single complete, unfiltered 162-case package campaign: 49 units and 113 integration cases, all passed. The one supplemental raw-Windows-byte case, 13 original independent cases and two new CLI cases all passed separately and contribute no coverage credit. Build, formatting and all-target Clippy with -D warnings passed; inventory/list/build operations receive no behavioral case credit. Both complete numeric collection boundaries were satisfied before continuation. There was no metric stop and no second collection to improve a result.

The fresh campaign covered one more line than development, in protocol.rs (679/716 versus 678/716), with the same denominator. Development coverage is comparison only; no source change or imported coverage is credited. Raw coverage SHA256: `{metrics['coverage_sha256']}`.

Native Cargo/Rust 1.97.1, rustfmt 1.9.0, Clippy 0.1.97, cargo-llvm-cov 0.8.4 and LLVM 22.1.6 were discovered. Cargo resolves to `C:\\Users\\bryan\\.cargo\\bin\\cargo.exe`; PowerShell to `C:\\Program Files\\PowerShell\\7\\pwsh.exe`; Python 3.10 evidence support to `C:\\Program Files\\Python310\\python.exe`. Product commands ran from the corrected candidate on native C:, with distinct QA build/coverage/independent/supplemental targets. Exact argv arrays, cwd, overrides, tool hash, timing, exit and raw-output hashes are retained in each receipt indexed by [attempt-index.json](attempt-index.json).

The complete `cargo llvm-cov` command is recorded as its literal argv array in [03-coverage/receipt.json](attempts/03-coverage/receipt.json), including offline/locked/all-targets selection, the source-exclusion regex, the 95% line floor and serial test execution. It completed in 218.219 seconds (11:02:39.997578Z to 11:06:18.226657Z), including the real 120-second production watchdog. No attempt timed out. Branch coverage is **NOT_RUN**: the collector requires unstable support and no nightly toolchain is installed; no installation was selected. Linux was not a required platform. Native Codex is **NOT_RUN**. No required offline metric remains partial or unavailable.

## Defects and unresolved work

| Defect/gap ID | Criterion/policy | Issue class and demonstrated impact | Result | Exact artifact and owner | Evidence |
| --- | --- | --- | --- | --- | --- |
| QA-LOG-01 | LG-02/03/06; LD-12 | Previously confirmed mandatory product defect: inconsistent incomplete capture falsely inspected as completed | VERIFIED_FIXED by original and added independent negative/positive controls | Corrected src/journal.rs; correction owned by dev, closure assessed by this independent QA | [findings.json](findings.json), [original-defect-retest.json](original-defect-retest.json), [rt-01-observations.json](rt-01-observations.json) |
| QA-LOG-02 | LG-02/06; base sections 4/7 | Previously confirmed mandatory product defect: absent/contradictory post-stop exit falsely inspected as completed | VERIFIED_FIXED; presence/type/zero agreement enforced while honest failure null/nonzero remains valid | Corrected src/journal.rs; correction owned by dev, closure assessed by this independent QA | [findings.json](findings.json), [original-defect-retest.json](original-defect-retest.json), [rt-02-observations.json](rt-02-observations.json) |
| QA-H01 | Plan's single QA-only preparation correction allowance | Local harness prerequisite error: relocated positive control lacked canonical Windows verbatim path prefix | RESOLVED; retained ERROR, then corrected preparation passed without changing assertions or product bytes | QA-owned cli_matrix.py / cli_matrix_v2.py; QA helper preparation owner | [harness-gap-01.md](harness-gap-01.md), [initial receipt](attempts/18-rt01/receipt.json), [corrected receipt](attempts/18-rt01-corrected/receipt.json) |

[defect-lifecycle.json](defect-lifecycle.json) records OPEN -> FIX_REPORTED -> VERIFIED_FIXED with distinct old QA, development and current independent evidence bindings. Original findings/reports retain their historical states. There are no open selected product findings, unresolved offline gaps, advisory scope additions or remaining required cases. Native WN-01/02, NI-T11/12 and installed-profile/operator qualification remain separately unperformed, not passing cases.

## Continuation, stopping and remaining obligations

The retained order is build/list, the complete coverage campaign, independent helper build, QA-01..13, initial RT-01 preparation, corrected RT-01, RT-02, supplemental case, formatting and Clippy. All 23 attempt receipts are terminal; 22 completed checks/cases and one retained preparation ERROR. Build/list/helper-build/fmt/Clippy receipts do not inflate the 178-case denominator.

The original RT-01 control returned evidence_corrupt before any negative mutation. Readback showed v1 copied a plain C: run_dir, while request::resolve canonicalizes to a Windows verbatim path. v2 asserts the seed's canonical form, rebinds the copied path accordingly and recomputes its digest. Source/oracles, all 145 entries and selected seed criteria are unchanged. This was classified as a local preparation gap, not a demonstrated product failure or integrity stop. The plan had already allowed one such correction. [harness-gap-01.md](harness-gap-01.md) retains that decision; no retry erased the ERROR or increased case counts.

No confirmed integrity failure, completed deficient metric or critical preservation/authorization defect occurred; STOP.json was not created. Safe independent checks continued under the unchanged scope and identities. No test is stopped, blocked or NOT_RUN within the declared offline denominator. No product failure was reclassified away. No automatic product retry or second coverage run occurred.

All owned command invocations have terminal receipts and bounded synchronous CLI subprocesses returned. No known invocation from this run remains pending. Product tests exercised actual held Job Objects, process handles, teardown and reader drain; no global claim about unrelated processes or historical PID absence is made. No historical PID was targeted. QA retains its fixtures, owned junctions and Cargo targets as evidence; no cleanup deletion, rollback, product mutation or operational change was performed. The failed initial matrix control is also retained.

## Disposition

The selected offline QA outcome is **PASS**, and both findings are **VERIFIED_FIXED** for the bound corrected candidate. A qa-fix packet is not applicable because no current product defect requires repair. There is no dev remediation handoff.

[final-preservation.json](final-preservation.json) verifies 68 corrected files, 183 preserved failed/original/snapshot files and 108 bound inputs; all 3689 prior QA and 9691 development evidence files and their bound binaries remain unchanged. All 212 matrix seed-file hashes are unchanged. The PowerShell helper remains SHA256 `f69da72fb44737127dcfde3607fb0e027e4afeb2463a78ac8f844bc3abfc58a0`. Final sealing repeats identity checks. No unrelated bytes were edited by this QA session.

External framework acceptance is **NOT_EVALUATED**. Native Codex and installed-profile qualification are **NOT_RUN**. This report grants no release/deployment or native-launch authorization.

## Artifact delivery

Original evidence selection: `C:\\Projects\\DevForgeAI\\docs\\plan\\framework-worker-logging`. Required and actual run destination: `{ROOT}`. Plan, report, checkpoint, criteria/cases, findings/lifecycle, metrics, integrity, receipts and retained raw evidence are published in this one new root. Prior evidence is preserved in place.

The final external `{ROOT / 'handoff-manifest.json'}` binds exact required-versus-actual paths, sizes and hashes. Its entries `qa-report.md`, `plan.md`, `checkpoint.json`, `candidate-manifest.json`, `specification-bindings.json`, `defect-lifecycle.json`, `criterion-results.json`, `case-results.json`, `metrics.json`, `next-review-prompt.txt` and `evidence-manifest.json` bind the mutually referring artifacts without circular self-hashes. The evidence manifest covers regular evidence files, separately binds produced executables, and records untraversed reparse points; Cargo intermediates are excluded. The report's byte hash is the external manifest entry, not a self-claim.

The separate `final-readback.json` records literal-path publication/readback results after sealing. It must show READBACK_VERIFIED and an empty errors array before this handoff is treated as delivered. No write/readback failure was observed during report preparation; any sealing failure must be reported at the same selected destination rather than redirected. `qa-fix.md` is intentionally absent because the verdict is PASS. The initial checkpoint is preserved as `checkpoint-before-execution.json`.

## End-user handoff

Open `{PROJECT}` in Codex on native Windows PowerShell. The next possible owner is the project operator/native diagnostic reviewer under the bound native-readiness and preflight contracts, if that work is separately selected. The next action is to prepare and review a bounded native diagnostic request using this corrected candidate; this offline retest neither runs that trial nor defines a release decision. No extra skill or installed framework is assumed for the plain conversation prompt below. The current host exposes qa and dev, but no repair is requested and neither is auto-invoked.

The same resolved prompt is in [next-review-prompt.txt](next-review-prompt.txt). The final conversation supplies the sealed manifest SHA256 outside files that it hashes. Paste this into Codex only to select the planning task:

```text
{prompt.rstrip()}
```
'''
write('qa-report.md', report)

initial_checkpoint = (ROOT / 'checkpoint.json').read_bytes()
with (ROOT / 'checkpoint-before-execution.json').open('xb') as stream:
    stream.write(initial_checkpoint)
checkpoint = {
    'intent': 'retest', 'plan_readiness': 'READY', 'execution_status': 'COMPLETED', 'verdict': 'PASS',
    'timestamp_utc': now, 'candidate_manifest': binding(ROOT / 'candidate-manifest.json'),
    'input_manifest': binding(ROOT / 'input-manifest.json'), 'plan_binding': binding(ROOT / 'plan-binding.json'),
    'specifications': binding(ROOT / 'specification-bindings.json'),
    'case_results': binding(ROOT / 'case-results.json'), 'attempt_index': binding(ROOT / 'attempt-index.json'),
    'completed_attempts': 23, 'retained_harness_error': 'QA-H01: attempts/18-rt01; resolved by one permitted preparation correction',
    'required_cases': 178, 'passed_cases': 178, 'defect_states': {'QA-LOG-01': 'VERIFIED_FIXED', 'QA-LOG-02': 'VERIFIED_FIXED'},
    'defect_lifecycle': binding(ROOT / 'defect-lifecycle.json'), 'criterion_results': binding(ROOT / 'criterion-results.json'),
    'owned_pending_invocations': [], 'owned_operation_disposition': 'All command receipts terminal; no known pending invocation. No global process-absence claim.',
    'retained_owned_state': ['attempts and fixtures including failed preparation', 'QA-owned junctions recorded without traversal', 'build-target', 'coverage-target', 'independent-target', 'supplemental-target'],
    'remaining_required_cases': [], 'stop_trigger': None, 'report': binding(ROOT / 'qa-report.md'),
    'native_codex': 'NOT_RUN', 'framework_acceptance': 'NOT_EVALUATED',
    'delivery_readback': str(ROOT / 'final-readback.json'),
    'next_safe_action': 'No offline retest work remains. Optional separately selected native diagnostic planning/review only; no automatic launch or product repair.',
    'resume_rule': 'Verify current source, specs, evidence, permissions, tools and owned state before any separately selected new work; never replay old attempts or restore drift silently.',
}
(ROOT / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')
for name in ['qa-report.md', 'next-review-prompt.txt', 'checkpoint.json', 'criterion-results.json', 'findings.json', 'defect-lifecycle.json']:
    assert (ROOT / name).read_bytes(), name
print(json.dumps({'verdict': 'PASS', 'report': binding(ROOT / 'qa-report.md'), 'criteria': len(criteria), 'findings': {item['id']: item['state'] for item in findings}, 'checkpoint': binding(ROOT / 'checkpoint.json')}, indent=2))
