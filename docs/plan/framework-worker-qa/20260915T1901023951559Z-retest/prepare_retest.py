import datetime,json,re,shutil
from pathlib import Path
from record import ROOT,WORK,PACKAGE,sha,write
OLD=ROOT.parent/'20260915T1800141514833Z'
DEV=ROOT.parent/'20260915T1834258428322Z-dev'
rows=[]
for entry in json.loads((ROOT/'selected-manifest.json').read_text(encoding='utf-8-sig')):
    p=Path(entry['path']); actual=sha(p)
    rows.append({**entry,'actual':actual,'matches':actual==entry['sha256']})
write('candidate-before.json',rows)
assert len(rows)==32 and all(x['matches'] for x in rows),'candidate drift'
assert sha(ROOT/'selected-manifest.json')=='3f65ade36cf8186fe711da73f1a2794a17d7fb51e02bf66261e9bba0ce158e39'
assert sha(OLD/'handoff-manifest.json')=='b40d23c3f5751881ca563bbd47c8ce82330420aed3e0e273c13f67f54017daf6'
delivery=[]
for e in json.loads((DEV/'delivery-manifest.json').read_text()):
    p=Path(e['actual_path']);actual=sha(p)
    delivery.append({'path':str(p),'actual':actual,'expected':e['sha256'],'matches':actual==e['sha256']})
write('developer-delivery-readback.json',delivery)
assert all(x['matches'] for x in delivery),'developer delivery drift'
original=[]
for name,e in json.loads((OLD/'handoff-manifest.json').read_text()).items():
    original.append({'entry':name,'path':e['actual_path'],'expected':e['sha256'],'actual':sha(e['actual_path']),'matches':sha(e['actual_path'])==e['sha256']})
write('original-evidence-readback.json',original)
assert all(x['matches'] for x in original),'original evidence drift'
bound=[WORK/'AGENTS.md',WORK/'.agents/skills/qa/SKILL.md',WORK/'devforgeai/Cargo.toml',WORK/'devforgeai/Cargo.lock',WORK/'docs/specs/framework/runtime/codex-worker-feasibility-v1.md']
write('input-identities.json',[{'path':str(p),'sha256':sha(p)} for p in bound])
snapshot=ROOT/'candidate-snapshot'
snapshot.mkdir(exist_ok=True)
for x in rows:
    p=Path(x['path']); dest=snapshot/p.relative_to(PACKAGE);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
cases=json.loads((OLD/'cases.json').read_text())
for c in cases:
    c['status']='NOT_RUN';c['evidence']='fresh receipts and independent-attempts in this retest root'
cases.extend([
 {'id':'RT-01','expected':'Real owned pipe RPC write returns deadline/user_cancel/invalid_control within bound; uncertain write prevents any second send; blocked interrupt consumes a single grace budget; held peer/descendant handles signal after teardown.',
  'spec':'DFF-WORKER-FEAS-01 sections 4-6; F-01','status':'NOT_RUN','readiness':'READY','platform':'Windows x64','evidence':'independent-boundary.json'},
 {'id':'RT-02','expected':'Approved typed categories/numeric/null/absent details retained; unknown nested data omitted; bad category and RPC code types rejected before persistence. Independent synthetic markers absent in stdout/stderr/journal.',
  'spec':'DFF-WORKER-FEAS-01 sections 5,7; F-02','status':'NOT_RUN','readiness':'READY','platform':'Windows x64','evidence':'independent typed error attempts'}])
write('cases.json',cases)
tests=[]
for p in sorted((PACKAGE/'tests').glob('*.rs')):
    for name in re.findall(r'#\[test\]\s*fn (\w+)\(',p.read_text()):
        tests.append({'file':str(p),'name':name,'category':'mandatory' if re.fullmatch(r'wf_\d\d',name) else 'remediation' if p.name=='remediation.rs' else 'supplemental',
          'level':'unit' if p.name in ['oracle.rs','admission.rs','profile.rs'] else 'integration/API'})
write('test-inventory.json',tests)
write('source-denominator.json',{'files':[{'path':str(p),'sha256':sha(p)} for p in sorted((PACKAGE/'src').glob('*.rs'))],
 'eligible':'every executable first-party src line; includes Windows/native adapter, CLI, error paths; lib.rs declarations may count zero',
 'exclusions':['tests/support/fixtures','third-party generated/vendored dependencies','independent QA helper code'],
 'collection':'complete all-targets instrumented suite, all 50 test functions terminal plus usable full JSON. Extra independent probes are not contributors.',
 'floors':'coverage >=95%; declared six unit tests >=95%; original20 mandatory all pass; whole28-group suite >=95% with no mandatory failure'})
plan=f'''# F-01/F-02 independent retest plan

Intent RETEST; plan READY; execution NOT_STARTED. User selected corrected candidate and F-01/F-02, including M-01 and affected regressions.
Evidence selection: fresh sibling under docs/plan/framework-worker-qa/ as required by the selected handoff. Literal root `{ROOT}`.
Candidate `{PACKAGE}`, manifest `{ROOT/'selected-manifest.json'}`, SHA256 {sha(ROOT/'selected-manifest.json')}; all32 files verified. Preserved snapshot under candidate-snapshot/.
Contract DFF-WORKER-FEAS-01 v1.0.0 at docs/specs/framework/runtime/codex-worker-feasibility-v1.md, SHA256 {sha(bound[-1])}.
Original findings and failed attempts remain under `{OLD}`; development under `{DEV}`. Their readbacks are adjacent; supplied metrics do not qualify this retest.

## Oracle disposition before execution

The old IQ-02-deadline helper expects exit4. Section4 explicitly maps deadline to exit6, and the original fix packet permits bounded failure/timeout/cancel. This retest corrects only the new QA-owned copy to expect exit6, terminal timed_out/deadline, tree_stopped true, fixture_unchanged true, one initialize/no retry, and actual completion within injected RPC500ms + grace200ms + teardown500ms plus200ms scheduling margin (1.4s). Cancellation remains exit5/user_cancel, <=1.2s after launch (control set at300ms). Both independently held process handles and no external termination are required. The earlier raw FAIL is preserved, never relabeled or erased. This is a contract-grounded QA oracle correction, not a product repair or waiver.

## Scope, case matrix and metrics

`cases.json` preserves WF-01..20 and IQ-01..06 and adds RT-01/RT-02 for the selected repaired boundaries. Twenty original mandatory cases count once with all required subfixtures. Original26-group rate and expanded28-group rate reported separately, no inflation to hide failures.
`test-inventory.json`: 50 developer test functions =20 mandatory+26 original supplemental+4 remediation integration groups. Six original unit-level functions remain their own metric. Test filenames, expected requirements, preconditions and fixture data derive from the source and immutable prior plan.
All-src coverage denominator fixed in source-denominator.json; no uncovered production exclusions. Final collection only when all50 contributing tests and collector terminate. Branch coverage NOT_RUN (installed stable collector option unstable); no new toolchain installation. Native WN-01/WN-02 remain NOT_RUN and expressly unselected, not part of offline28-group denominator.

## Environment and authorized effects

Windows x64, PowerShell7.6.6/C:NTFS; discover tool versions again with record.py environment. No Git metadata at workspace root. Isolated Cargo workspace and lock unchanged. Read-only source/operational boundaries; QA-owned builds, fixtures, harnesses and retained evidence only. No Codex launch/account/profile review, launcher amendment, native trial, index repair, dependency installation, startup or deployment. Library injection of shorter deadlines explicitly allowed; baseline WF-16 still runs production120s watchdog.

## Integrity and readiness

All original implementation/tests reviewed in prior QA; unchanged files verified by manifests. Re-read full changed writer/protocol paths, new remediation tests and peer stimuli. Writer owns only stdin and one outstanding message; control polls bounded completion; pending send cannot be retried; job teardown precedes writer-finished observation. Atomically attached job, restricted inherited pipe handles and no breakaway preserved. New error helper projects captured types before append. No mock/ignore/coverage-suppression attributes or vacuous claims found in changed code. Injection seams remain test-only; external peer is explicitly permitted, not native Codex proof. QA-owned helper copies and new probes require source inspection before execution.

## Planned commands and order

From C:\\Projects\\DevForgeAI: `python -B -X utf8 {ROOT/'record.py'} environment`, then `test`, `format`, `clippy`, `coverage`. Commands resolved from actual Cargo manifest: test --locked --offline --all-targets; fmt --all -- --check; clippy --locked --offline --all-targets -- -D warnings; llvm-cov --locked --offline --all-targets --json --output-path {ROOT/'coverage.json'}. Cargo cwd is the original package; builds under this root/target; each suite has disjoint retained fixture roots. Test/coverage command bounds360s including compile/watchdog. Finalize metrics before further probes; valid subthreshold result stops run.

Build independently authored peer/driver in this root/independent with path dependency on unchanged candidate, offline cache only. Execute original protocol/result, corrected backpressure, lifecycle, inspect and privacy modes, then RT-01/RT-02 once each with external bounded safety containment. Distinct variant attempts are not retries. Treat any newly confirmed confidentiality/security violation as immediate stop; no further probes after it. No real secrets in fixtures.

Independent expected errors derived from captured CodexErrorInfo/JSON-RPC schemas; varied uint16 bounds, category allowlist, nested unknown data and field types. Independent held handles obtained while live; never kill historical PIDs. Original terminal/trace and exact fixture bytes verified, include worker exit and zero-job observations where available. Expected-positive category tests prevent suppress-all sanitizer from passing.

## Stop, disposition and paths

Confirmed integrity failure, valid complete subthreshold metric or critical security/data-loss defect stops all tests; ordinary functional finding retains FAIL while safe checks continue. No source repair. Preserve original failures and distinguish harness gaps. All final readbacks and stop decisions explicit.
Roles: test-plan.md, cases.json/case-results.json, selected-manifest.json/candidate-before.json/candidate-after.json, per-command receipt/stdout/stderr, metrics.json/final-metrics.json, qa-report.md, qa-fix.md on FAIL, checkpoint.json, handoff-manifest.json. Verify bytes at these literal paths before reporting delivery. F-01/F-02 start FIX_REPORTED; only valid fresh independent retest permits VERIFIED_FIXED. Framework acceptance NOT_EVALUATED; release/native decisions separate.
'''
(ROOT/'test-plan.md').write_text(plan,encoding='utf-8')
write('checkpoint.json',{'intent':'retest','execution':'NOT_STARTED','plan':'READY','F-01':'FIX_REPORTED','F-02':'FIX_REPORTED','owned_processes':[]})
print(json.dumps({'root':str(ROOT),'files':len(rows),'developer_delivery_entries':len(delivery),'original_entries':len(original),'tests':len(tests),'cases':len(cases),'plan_sha256':sha(ROOT/'test-plan.md')}))
