"""Bind the QA inventory before product execution. Produces evidence only."""
import json
import re
from pathlib import Path
from record import ROOT, WORK, PACKAGE, sha, write

spec = WORK / 'docs/specs/framework/runtime/codex-worker-feasibility-v1.md'
cases = []
for line_no, line in enumerate(spec.read_text(encoding='utf-8').splitlines(), 1):
    found = re.match(r'\| (WF-\d\d) \| (.*) \|', line)
    if found:
        key, expected = found.groups()
        n = int(key[-2:])
        suite = 'protocol' if n <= 8 else 'recovery' if n <= 12 else 'process_windows' if n <= 16 else 'contract'
        cases.append({'id': key, 'spec': str(spec), 'line': line_no, 'expected': expected,
          'test': suite + '::' + key.lower().replace('-', '_'), 'level': 'compiled Windows integration/acceptance',
          'platform': 'Windows x64', 'readiness': 'READY', 'status': 'NOT_RUN',
          'fixture': 'published task/prompt/expected; developer peer case and all loop subfixtures inspected in source',
          'evidence': '01-tests and 04-coverage; retained case fixture journals/traces',
          'preconditions': 'verified candidate and cached dependency build', 'cleanup': 'owned Job Objects; preserve evidence'})
extra = [
 ('IQ-01','sections 4,5,8','Independent protocol peer validates exact outbound fields, IDs, order, one turn; valid result succeeds; incorrect/extra/duplicate/missing final result fails; policy mismatch blocks before turn.'),
 ('IQ-02','sections 4,5,6 / WF-16','A peer sends a permitted large string server request ID, then stops reading stdin. RPC/total deadline and cancellation must remain effective; owned processes stop within injected deadlines plus grace/teardown.'),
 ('IQ-03','section 6 / WF-13,14','Independently held peer and descendant handles signal after stdin cancel, real hidden-console Ctrl+C, and forced harness termination; no historical PID mutation.'),
 ('IQ-04','sections 4,7 / WF-10,11,12','Repeated compiled inspection of retained execution gives identical committed events, pagination without gaps, read-only bytes and no redispatch.'),
 ('IQ-05','sections 5,7','Unexpected structured error data containing synthetic private marker is rejected or sanitized before journal/stdout persistence.'),
 ('IQ-06','section 6','Static FFI review checks atomic job attachment, noninherited job handle, only pipe handles inherited, no breakaway; independent negative lifecycle checks use real OS handles.')]
for key, loc, expected in extra:
    cases.append({'id':key,'spec':str(spec),'location':loc,'expected':expected,'platform':'Windows x64',
       'level':'independent compiled/API/process evidence','readiness':'READY','status':'NOT_RUN',
       'preconditions':'build independent Rust peer/driver against unchanged candidate and inspect helper',
       'evidence':'independent/attempt directories','cleanup':'terminate only held owned process; verify child handles'})
write('cases.json', cases)
tests = []
for path in sorted((PACKAGE/'tests').glob('*.rs')):
    for name in re.findall(r'#\[test\]\s*fn (\w+)\(', path.read_text()):
        tests.append({'file':str(path),'name':name,'category':'mandatory' if re.fullmatch('wf_\\d\\d',name) else 'supplemental',
          'level':'unit' if path.name in ['oracle.rs','admission.rs','profile.rs'] else 'integration/API'})
write('test-inventory.json', tests)
write('source-denominator.json', {'eligible':[{'path':str(p),'sha256':sha(p)} for p in sorted((PACKAGE/'src').glob('*.rs'))],
     'exclusions':['tests, support and fixture code','third-party and generated dependency code','QA peer/driver'],
     'scope':'all executable lines in all eight src/*.rs; lib.rs declarations may have zero executable lines',
     'collection':'04-coverage runs complete all-targets developer suite, independently executed; extra exploratory QA not coverage contributors',
     'decision':'only after collector and every declared contributor terminates; no partial threshold verdict',
     'branch':'NOT_RUN on installed stable collector unless supported without installing/changing toolchain'})
paragraphs=[]
heading=''
for n,line in enumerate(spec.read_text().splitlines(),1):
    if line.startswith('## '): heading=line
    if line and not line.startswith('|'):
        paragraphs.append({'line':n,'section':heading,'text':line,
          'scope':'native prerequisite only' if heading.startswith('## 6.') and 'review' in line.lower() else 'contract review with case mapping by sections in plan'})
write('criterion-inventory.json',paragraphs)
plan = f'''# Independent offline worker QA plan

Intent: run. Plan readiness: READY for offline work. Execution: NOT_STARTED.
Selected evidence value: fresh timestamped child of docs/plan/, selected by user repository evidence policy.
Resolved root: `{ROOT}`. Product source: `{PACKAGE}`.
Selected manifest SHA-256: `{sha(ROOT/'selected-manifest.json')}` (31 files match).
Contract: DFF-WORKER-FEAS-01 v1.0.0 at `{spec}`, SHA-256 `{sha(spec)}`.
Input identities, 335 contract/schema readbacks and source denominator are adjacent JSON files.

## Scope and obligations

Windows x64, native PowerShell/Cargo on C:. All WF-01..20 and required subfixtures; independent IQ-01..06.
WN-01/WN-02 remain NOT_RUN, separately unselected; no Codex process, live account/config/profile inspection or model launch.
Linux/WSL, index implementation, protected authority, installation and native GUI qualification are not this unit.
The public library test seam permits injected shorter monotonic limits. The production watchdog remains exercised by WF-16.
Parent design constraints do not expand deliverables; Rust controls product behavior, Python records QA evidence only.

## Matrix and measurement

`cases.json` binds requirements, independent expected behavior, readiness, evidence and cleanup for 26 required QA cases.
The specification denominator remains 20 WF cases, each counted once; all subfixtures must pass.
Additional independent case rate is reported separately and overall 26-case rate retains all required nonpasses.
`test-inventory.json` contains all 46 developer test functions: 20 mandatory, 26 supplemental.
Unit-level inventory is the oracle/admission/profile test functions (6); integration/API test binaries remain separate.
Both 95% thresholds apply independently. All mandatory cases must pass even when numeric floors pass.
Coverage: full all-targets suite, no production exclusions; see `source-denominator.json`. IQ exploratory probes are separately assessed, not used to inflate baseline coverage.

## Execution order and commands

1. Inspect all 31 package inputs including all first-party Rust implementation/tests/support, attributes/imports and recorder; freeze fixture hashes and manifests.
2. `python -B -X utf8 {ROOT/'record.py'} test`: Cargo test --locked --offline --all-targets, bound 360s including compilation and production 120s watchdog.
3. `record.py format`, then `record.py clippy`: Cargo fmt --all -- --check; Cargo clippy --locked --offline --all-targets -- -D warnings.
4. `record.py coverage`: Cargo llvm-cov --locked --offline --all-targets --json --output-path {ROOT/'coverage.json'}, bound 360s. Independent collection; preserve raw profiles/output.
5. Build QA-owned Rust peer/driver with path dependency on unchanged package into fresh evidence output; inspect code before launch. Execute IQ cases once per declared subfixture with external bounded process containment. Large server-request ID stays below 1MiB input line and 8MiB cumulative limits; peer stops reading only owned pipe. Expected result lives outside worker fixture.
6. Rehash original candidate and input boundaries; report/fix packet and manual handoff.

No product or developer-test edits. All build outputs/fixtures under this QA root. No downloads or dependency installation; missing cache is a setup gap.
Safety containment uses only current owned subprocess handles/tree; never a historical PID. Preserve failed attempts. Do not silently retry product tests.

## Integrity inspection and stop rules

Reviewed all package test functions and peer/console/crash drivers. Ordinary serde derive/test attributes; no mock-generating decorators, ignores or coverage suppression found. Synthetic external peer is expressly permitted; does not qualify native Codex. Fault injection remains library-only and is not real disk failure evidence.
Reviewed process FFI: job list supplied to CreateProcessW, kill-on-close, only three pipe handles listed, no breakaway. Independent lifecycle observation still required.
Known concern pending independent reproduction: synchronous worker stdin write may block deadline/control loop. No product defect yet inferred from a timeout alone.
Whole-run stop on confirmed integrity failure, complete subthreshold metric, critical security/data-loss defect, or uncontained ownership/identity problem. Ordinary functional defects retain FAIL while safe independent checks continue.
After a stop: containment, evidence readback and reporting only. Remaining required cases stay NOT_RUN with trigger ID.

## Artifact paths

Plan: test-plan.md; criteria: criterion-inventory.json; cases: cases.json; candidate: selected-manifest.json/candidate-before.json;
commands: per-attempt receipt.json/stdout.txt/stderr.txt; findings: qa-report.md/qa-fix.md; checkpoint: checkpoint.json;
final candidate: candidate-after.json; delivery: handoff.md. Report is independent QA assessment, never framework acceptance.
'''
(ROOT/'test-plan.md').write_text(plan,encoding='utf-8')
write('checkpoint.json', {'intent':'run','plan':'READY','execution':'NOT_STARTED','next':'01-tests', 'owned_processes':[]})
print(json.dumps({'cases':len(cases),'developer_tests':len(tests),'unit_tests':sum(x['level']=='unit' for x in tests),'plan_sha256':sha(ROOT/'test-plan.md')}))
