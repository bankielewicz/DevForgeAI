"""Assess completed evidence and bind final readbacks; no product execution."""
import datetime,json
from pathlib import Path
from record import ROOT,WORK,PACKAGE,sha,write

def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8-sig'))
def verify(rows,key='sha256',relative=False):
    out=[]
    for row in rows:
        path=WORK/row['path'] if relative else Path(row['path'])
        actual=sha(path)
        out.append({'path':str(path),'expected':row[key],'actual':actual,'matches':actual==row[key]})
    return out

for name,rows,key,relative in [
 ('candidate-after.json',read('selected-manifest.json'),'sha256',False),
 ('boundary-after.json',read('input-identities.json'),'sha256',False),
 ('contract-after.json',read('contract-readback.json'),'sha256',True),
 ('developer-delivery-after.json',read('developer-delivery-readback.json'),'expected',False),
 ('original-evidence-after.json',read('original-evidence-readback.json'),'expected',False)]:
    checked=verify(rows,key,relative);write(name,checked)
    assert all(x['matches'] for x in checked),f'drift: {name}'
metrics=read('metrics.json')
assert metrics['01-tests']['passed']==metrics['01-tests']['total']==50
assert metrics['04-coverage']['passed']==metrics['04-coverage']['total']==50
assert metrics['coverage']['meets_floor']
for name in ['01-tests','02-format','03-clippy','04-coverage','05-independent-build']:
    assert read(name+'/receipt.json')['exit_code']==0
results=[]
for c in read('cases.json'):
    c=dict(c);cid=c['id']
    if cid.startswith('WF-'):
        test='wf_'+cid[3:]
        a=[x for x in metrics['01-tests']['entries'] if x['name']==test]
        assert len(a)==1 and a[0]['result']=='ok'
        c.update(status='PASS',actual='All required loop subfixtures passed in normal and instrumented executions.',evidence=['01-tests/stdout.txt','04-coverage/stdout.txt'])
    elif cid=='IQ-06':
        c.update(status='PASS',actual='FFI ownership inspection, atomic job attachment, restricted inheritance and actual held-handle lifecycle checks; see report.',evidence=['candidate-snapshot/src/process_windows.rs','independent-boundary.json','independent-attempts/IQ-03-kill/result.json'])
    elif cid.startswith('IQ-'):
        paths=sorted((ROOT/'independent-attempts').glob(cid+'*/result.json'))
        values=[json.loads(p.read_text()) for p in paths]
        assert values and all(x['pass'] for x in values),cid
        c.update(status='PASS',actual={'subfixtures':len(values),'passed':len(values)},evidence=[str(p.relative_to(ROOT)) for p in paths])
    else:
        name='independent-boundary.json' if cid=='RT-01' else 'independent-errors.json'
        values=read(name)
        assert len(values)==(4 if cid=='RT-01' else 12) and all(x['pass'] for x in values)
        c.update(status='PASS',actual={'subfixtures':len(values),'passed':len(values)},evidence=[name])
    results.append(c)
assert len(results)==28
write('case-results.json',results)
counts=lambda n:{'passed':n,'required':n,'percentage':100,'status':'PASS'}
write('final-metrics.json',{'platform':'Windows 11 Pro x64','overall_platforms':['Windows 11 Pro x64'],
 'mandatory_spec':counts(20),'original_offline_groups':counts(26),'expanded_offline_groups':counts(28),
 'developer_test_functions':counts(50),'original_supplemental':counts(26),'remediation_test_groups':counts(4),'unit_level_cases':counts(6),
 'line_coverage':metrics['coverage'],'native':{'WN-01':'NOT_RUN','WN-02':'NOT_RUN','selected':False},
 'duplicate_counting':'Normal and coverage executions count the same functions once. Subfixtures cannot inflate group denominator.'})
write('defect-lifecycle.json',{'candidate_manifest_sha256':sha(ROOT/'selected-manifest.json'),
 'F-01':{'prior':'OPEN','delivered':'FIX_REPORTED','retest':'VERIFIED_FIXED','evidence':['independent-attempts/IQ-02-deadline/result.json','independent-attempts/IQ-02-cancel/result.json','independent-boundary.json']},
 'F-02':{'prior':'OPEN','delivered':'FIX_REPORTED','retest':'VERIFIED_FIXED','evidence':['independent-attempts/IQ-05-private-error/result.json','independent-errors.json']},
 'M-01':{'historical':'FAIL 24/26; unchanged','current':'PASS 26/26 original groups; 28/28 expanded groups'},
 'scope':'Independent Windows offline retest only; no framework or native acceptance'})
binary_paths=[ROOT/'target/debug'/n for n in ['devforgeai-codex-worker-probe.exe','protocol-peer.exe','console-driver.exe','crash-driver.exe']]
binary_paths += [ROOT/'independent-target/debug'/n for n in ['qa-driver.exe','protocol-peer.exe']]
write('binary-identities.json',[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in binary_paths])
raw=list((ROOT/'target').rglob('*.profraw'))+list((ROOT/'target').rglob('*.profdata'))
assert raw,'raw profiles missing'
write('raw-profile-identities.json',[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in raw])
write('checkpoint.json',{'intent':'retest','plan':'READY','execution':'COMPLETED','verdict':'PASS',
 'F-01':'VERIFIED_FIXED','F-02':'VERIFIED_FIXED','owned_processes':[],
 'fixtures':'Retained under this root; held process handles signalled and all supervisors exited.',
 'stop_trigger':None,'selected_remaining':[],'unselected':'WN-01/WN-02 NOT_RUN',
 'framework_acceptance':'NOT_EVALUATED','next_owner':'User/project review of independent retest and separate native prerequisites',
 'evidence_root':str(ROOT),'completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()})
coverage_rows='\n'.join(f"| {Path(x['file']).name} | {x['lines']['covered']} | {x['lines']['count']} | {x['lines']['percent']:.8f}% |" for x in metrics['coverage']['files'])
case_rows='\n'.join(f"| {x['id']} | {x['expected'].replace('|','/')} | {str(x['actual']).replace('|','/')} | PASS | {'; '.join(x['evidence'])} |" for x in results)
report=f'''# PASS — F-01/F-02 independent Windows offline retest

Both repairs are VERIFIED_FIXED for the selected Windows offline candidate. No new product defect was observed. This verdict does not qualify actual Codex/Pro integration or establish protected framework acceptance.

## Identity and scope

- Intent RETEST; plan READY; execution COMPLETED. Selected candidate `{PACKAGE}`, version 0.1.0, independent Cargo workspace, Rust edition 2024/MSRV 1.97.1; no declared feature combinations. Native Windows code is the selected cfg target.
- Corrected candidate manifest: selected-manifest.json, SHA-256 `{sha(ROOT/'selected-manifest.json')}`. All 32 package entries matched before and after execution. No Git metadata at workspace root; source snapshot and SHA-256 manifests bind candidate identity. Source, developer tests, lockfiles, operational copies and historical evidence were preserved.
- Contract: `{WORK/'docs/specs/framework/runtime/codex-worker-feasibility-v1.md'}`, DFF-WORKER-FEAS-01 v1.0.0, SHA-256 `7cb5b0cb87e515bb4d59235b615922ab4ea07ef607b8111dde6cc73c8f101b23`. All 335 bound contract/schema records matched final readback. Companion Rust enforcement/runtime boundaries are context, not additional selected implementation scopes.
- Plan: test-plan.md, SHA-256 `{sha(ROOT/'test-plan.md')}`. cases.json and source-denominator.json were declared before testing. case-results.json supplies full specification locations and final evidence mappings.
- Developer handoff: `../20260915T1834258428322Z-dev/handoff.md` and delivery.md; 322 delivery entries verified before/after. Original QA: `../20260915T1800141514833Z/qa-report.md`; its 34 handoff entries still match. Developer metrics were inputs only; reported results below are fresh executions.
- Windows 11 Pro build 26200 x64, PowerShell 7.6.6, native C: NTFS, workspace C:\\Projects\\DevForgeAI. Rust/Cargo 1.97.1, LLVM 22.1.6, cargo-llvm-cov 0.8.4. Exact paths/version outputs in environment.json, host.json and 00-* receipts. No Linux/WSL substitute, dependency installation, startup changes or native Codex launch.
- Scope: F-01/F-02 and affected offline regression/authority-preservation checks. WF-01..20, original IQ-01..06, added RT-01/RT-02. Linux, tray, index daemon, native WN-01/WN-02, launcher amendment and Pro profile review are outside this selected retest.

## Findings and defect disposition, ordered by original impact

### F-02 — High confidentiality finding: VERIFIED_FIXED

Requirement: contract sections 5 and 7; captured CodexErrorInfo/JSON-RPC field types. Only approved typed data may be retained; unknown private payloads must not cross journal/stdout boundaries.

Location: src/protocol.rs error_category, Session::rpc, and turn-completion handling. Original QA demonstrated an unknown object copied into error_category and emitted. The corrected code validates category shape and projects only approved fields before append/emit, and validates numeric RPC error code before retention.

Reproduction: `independent_run.py privacy` uses the original synthetic marker scenario against the corrected compiled library. Expected exit 4/protocol_error, no marker in journal/stdout/stderr and stopped peer; all observed. Twelve additional independent typed-error variants (`extended_probes.py errors`) cover valid uint16 endpoints, null and absent optional HTTP status, compact turn kind, known string category, invalid status and turn-kind types, and numeric versus malformed RPC codes. Exact allowed categories survive; extra nested marker fields and free-form message/data do not. All 12 passed. The original private-marker fixture passed as well. Tests used synthetic data only.

Evidence: independent-attempts/IQ-05-private-error/result.json and raw journal/output, independent-errors.json, each RT-02 attempt's raw journal/trace/output. Original failed evidence remains unchanged. Lifecycle OPEN -> FIX_REPORTED -> VERIFIED_FIXED is bound in defect-lifecycle.json.

### F-01 — High timeout/cancellation finding: VERIFIED_FIXED

Requirement: contract sections 4–6 and WF-13..16; deadlines/cancellation remain actionable under backpressure; process-tree teardown is verified. Deadline exit is 6, cancellation exit is 5; protocol failure exit is 4.

Location: src/process_windows.rs::send_until/wait_stopped and src/protocol.rs::rpc/receive/interrupt. The corrected writer thread owns stdin; the control thread polls completion with the same deadline/control state. An uncertain pending write rejects a second send. Interrupt send/wait shares a grace deadline. Cleanup includes writer completion and zero active job members.

Original reproduction: a peer emits a 262,144-character server request ID and stops reading, filling the reply pipe. Shorter injected limits are contract-permitted. Fresh deadline result: exit 6, timed_out/deadline, 0.781 seconds, within the declared 1.4-second bound. Cancellation at 300 ms: exit 5, cancelled/user_cancel, 0.546 seconds, within 1.2 seconds. Both emitted terminal evidence, preserved fixture bytes, sent one initialize without redispatch, and independently held peer handles signalled. No external watchdog termination was needed.

Four extra direct compiled boundary variants exercise ordinary RPC-shaped large writes with deadline/cancel/invalid control, pending-send rejection, and a separately filled interrupt pipe. Observed total durations were 463/287/290/213 ms. The full-pipe interrupt consumed 193 ms for a selected 180-ms shared grace (under the predeclared 400-ms scheduling bound). Every held peer and descendant handle transitioned from running (258) to signalled (0); every owned job reported zero active members after teardown.

Evidence: independent-attempts/IQ-02-deadline/ and IQ-02-cancel/, independent-boundary.json, RT-01-*/receipt.json and stdout.txt. Real CLI stdin/Ctrl+C and abrupt supervisor termination also passed in IQ-03, with independent held descendant handles.

### M-01 and the earlier 25/26 helper result

The historical 24/26 QA failure and developer's unchanged-helper 25/26 failure are preserved. The old deadline oracle expected exit 4. Contract section 4 requires exit 6 for a deadline; this was a QA expectation defect, not a remaining product failure. Before execution, this retest changed only its new helper copy to expect exit 6 and strengthened terminal reason, bounded completion and process-state checks. No product assertion/threshold or original helper was changed. Fresh original-scope accounting is 26/26; expanded accounting is 28/28. Historical records were not recalculated.

## Metrics and environments

Windows x64 is the only selected required platform, so its results equal the overall selected scope.

| Metric | Passing/covered | Required/eligible | Percentage | Result |
| --- | ---: | ---: | ---: | --- |
| Mandatory specification cases, all subfixtures | 20 | 20 | 100% | PASS |
| Original offline QA groups | 26 | 26 | 100% | PASS |
| Expanded declared offline QA groups | 28 | 28 | 100% | PASS |
| Developer test functions | 50 | 50 | 100% | PASS |
| Original supplemental functions | 26 | 26 | 100% | PASS |
| Remediation integration groups | 4 | 4 | 100% | PASS |
| Unit-level cases (separate skill metric) | 6 | 6 | 100% | PASS |
| Executed first-party lines | 1421 | 1487 | 95.56153328850034% | PASS >=95% |

All normal and instrumented collection contributors terminated successfully; each test function counts once, never once per run. The six unit-level cases use direct library behavior and are a subset of the 50 functions. Native cases are expressly unselected, not silently excluded failures. Neither numeric floor waives a mandatory/security case.

| Source file | Covered lines | Executable lines | Coverage |
| --- | ---: | ---: | ---: |
{coverage_rows}

Every first-party src executable line is included, including CLI/native adapter/error paths. lib.rs only declares modules (zero executable lines). Exclusions are test/fixture/QA-helper code and third-party dependencies, not uncovered production behavior. 66 executable lines remain uncovered; metrics.json retains collector segments and coverage.json retains raw LLVM export. No per-file floor is specified. Branch coverage is NOT_RUN (unstable collector option not selected); no estimated branch pass. Raw profraw/profdata files are retained and hashed in raw-profile-identities.json. The one-line difference from developer coverage is reported as observed, not used to modify historical measurements.

## Build, analysis and execution

Exact command arguments, cwd, tool hash, candidate hash, exit, start/end, duration and output hashes are retained in each receipt. Product commands ran from the selected package, with isolated target/fixture directories in this evidence root.

- `cargo test --locked --offline --all-targets`: PASS, 50/50, 148.703 seconds; compiles and executes the selected package and support binaries.
- `cargo fmt --all -- --check`: PASS, exit 0.
- `cargo clippy --locked --offline --all-targets -- -D warnings`: PASS, exit 0.
- `cargo llvm-cov --locked --offline --all-targets --json --output-path .../coverage.json`: PASS, 50/50 and valid complete line export, 150.594 seconds.
- Independent driver/peer `cargo build --offline --manifest-path .../independent/Cargo.toml`: PASS; only the QA-owned dependency lock was resolved for its direct Windows test dependency. Product lockfiles remain unchanged.
- Independent protocol/result negative cases, profile denial, reply backpressure, lifecycle/descendants, repeated read-only inspection/pagination, private payload and added boundary/error probes: all PASS. Each required variant executed once. Instrumented execution was a predeclared separate measurement, not a failure retry.
- Doc-tests were not invoked by all-targets; no documentation-test cases were selected. Fuzzing, Miri, concurrency-model testing and native UI were NOT_RUN, not required for this bounded retest. Windows handles/FFI were assessed with source inspection and real process evidence.

## Acceptance traceability

Detailed specification locations, fixtures/preconditions and independent expected results are in cases.json; outcomes below refer to retained outputs, not model-authorized acceptance.

| Case | Required observable behavior | Actual | Status | Evidence relative to this root |
| --- | --- | --- | --- | --- |
{case_rows}

## Test integrity

Reviewed changed production paths, all new remediation tests and peer branches; verified unchanged original source/tests against preserved manifests and retained their prior independent review. No mock decorators, bypass wrappers, ignored original cases, vacuous passing paths, weakened thresholds or coverage exclusions were found in this bounded inspection. External peers are synthetic protocol stimuli explicitly allowed by the offline contract; they execute actual compiled writer/protocol/process behavior and cannot prove native Codex authentication or effects.

Independent oracles use contract exit codes, fixed expected JSON categories, exact fixture hashes, real OS handles and bounded elapsed time. Positive sanitizer cases prevent a suppress-everything implementation from passing. Wrong/extra/duplicate/missing result cases exercise the content oracle. Test-only shorter deadline seams do not replace the production120-second watchdog, which ran in WF-16. The prior helper's deadline mismatch is explicitly disclosed above. QA helper source was inspected before use. No retries or duplicate variants were used to improve a pass rate.

FFI review (IQ-06): CreateProcessW uses STARTUPINFOEX with atomic job-list attachment; only child stdin/stdout/stderr handles are listed for inheritance. The job handle is noninherited, kill-on-close is set, and breakaway is not enabled. Parent handles are RAII-owned. Newly added writer owns its File; confirmed job termination and writer-finished observation precede successful wait_stopped. Held-handle cancellation, descendants and abrupt-supervisor-death observations support this bounded ownership assessment; this is not exhaustive formal proof of all Win32 failure paths.

## Continuation, cleanup and gaps

Normal suite -> formatting -> Clippy -> full coverage/metric assessment -> independent build/protocol/backpressure/lifecycle/inspect/privacy -> extra boundary/error probes -> final readback. Receipts preserve ordering and timestamps. No terminal stop condition occurred in this corrected-candidate retest. No required selected cases remain BLOCKED, FAILED, ERROR, skipped or NOT_RUN.

All supervised processes returned. IQ-02/IQ-03/RT-01 held handles verified stopped children; RT-01 additionally observed empty jobs. Fixtures/builds/evidence are retained. No historical-PID cleanup, source repair, installation or deletion was performed. There was no unresolved cleanup failure.

WN-01/WN-02 remain NOT_RUN and unselected. Captured launcher reparse identity and reviewed Pro profile require their separate resolution/review before explicit selection of native trials. Actual Pro authentication, model/effort availability, effective permissions, hook/tool effects and cancellation of Codex work remain unproven. This retest made no native feasibility verdict beyond those limitations.

## Disposition and artifact delivery

Product QA: PASS for this exact Windows offline repaired candidate; F-01/F-02 VERIFIED_FIXED. Framework acceptance: NOT_EVALUATED and not established; no qualified compiled-Rust acceptance decision was observed. No release/deployment authorization is inferred.

All artifacts are under the originally selected literal root `{ROOT}`. Final source/input/contract/developer/original readbacks are candidate-after.json, boundary-after.json, contract-after.json, developer-delivery-after.json and original-evidence-after.json. Test plan, case maps, metrics, defect lifecycle, checkpoint and this report are delivered and bound by handoff-manifest.json. qa-fix.md is inapplicable because this retest passed. The external manifest supplies exact file hashes without circular self-hashing; delivery-readback.json verifies it and all entries after publication.

Next owner: user/project reviewer for this independent result and the separately scoped native prerequisites. No dev remediation or automatic retest is requested. The qa and dev skills are available in the current host catalog, but only qa was applied for this independent assessment. Review this report and the separate native-trial handoff in C:\\Projects\\DevForgeAI on Windows. Native execution still needs its own concrete selection; no copyable execution prompt is issued for unselected effects.
'''
(ROOT/'qa-report.md').write_text(report,encoding='utf-8')
files=[]
for p in ROOT.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(ROOT)
    if rel.parts[0] in ['target','independent-target']:continue
    if p.name in ['handoff-manifest.json','delivery-readback.json']:continue
    files.append(p)
manifest={str(p.relative_to(ROOT)):{'required_path':str(p),'actual_path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(files)}
write('handoff-manifest.json',manifest)
loaded=read('handoff-manifest.json')
checked=[{'entry':k,'matches':sha(v['actual_path'])==v['sha256']} for k,v in loaded.items()]
assert all(x['matches'] for x in checked)
write('delivery-readback.json',{'manifest_sha256':sha(ROOT/'handoff-manifest.json'),'entries':checked,'all_match':True})
print(json.dumps({'verdict':'PASS','report':str(ROOT/'qa-report.md'),'report_sha256':sha(ROOT/'qa-report.md'),'manifest_sha256':sha(ROOT/'handoff-manifest.json'),'entries':len(checked),'source_entries_unchanged':32,'raw_profiles':len(raw)}))
