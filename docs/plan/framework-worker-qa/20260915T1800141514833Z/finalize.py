"""Post-stop assessment, byte readback and manual handoff only. No product execution."""
import datetime
import json
from pathlib import Path
from record import ROOT, WORK, PACKAGE, sha, write

now=datetime.datetime.now(datetime.timezone.utc).isoformat()
manifest=json.loads((ROOT/'selected-manifest.json').read_text(encoding='utf-8-sig'))
checks=[{'path':x['path'],'expected':x['sha256'],'actual':sha(x['path']),'matches':sha(x['path'])==x['sha256']} for x in manifest]
write('candidate-after.json',checks)
boundaries=json.loads((ROOT/'input-identities.json').read_text(encoding='utf-8-sig'))
write('boundary-after.json',[{'path':x['Path'],'expected':x['Hash'].lower(),'actual':sha(x['Path']),'matches':sha(x['Path'])==x['Hash'].lower()} for x in boundaries])
contracts=json.loads((ROOT/'contract-readback.json').read_text())
write('contract-after.json',[{'path':x['path'],'matches':sha(WORK/x['path'])==x['sha256']} for x in contracts])
metrics=json.loads((ROOT/'metrics.json').read_text())
case_results=[]
for case in json.loads((ROOT/'cases.json').read_text()):
    c=dict(case)
    if c['id'].startswith('WF-'):
        c.update(status='PASS',actual='All required developer subfixtures passed in both independent normal and instrumented executions. Original case table only; global bounds/sanitization assessed separately.')
    elif c['id']=='IQ-06':
        c.update(status='PASS',actual='Static FFI review and held-handle lifecycle observations; bounded claim in observations.md.')
    else:
        evidence=sorted((ROOT/'independent-attempts').glob(c['id']+'*/result.json'))
        values=[json.loads(p.read_text()) for p in evidence]
        c.update(status='PASS' if values and all(x['pass'] for x in values) else 'FAIL',
                 actual={'subfixtures':len(values),'passed':sum(x['pass'] for x in values)},
                 evidence=[str(p) for p in evidence])
    case_results.append(c)
write('case-results.json',case_results)
passed=sum(x['status']=='PASS' for x in case_results)
write('final-metrics.json',{'platform':'Windows 11 Pro x64','mandatory_spec_cases':{'pass':20,'total':20,'percentage':100},
   'supplemental_developer_tests':{'pass':26,'total':26,'percentage':100},
   'required_unit_cases':{'pass':6,'total':6,'percentage':100},
   'independent_groups':{'pass':4,'total':6,'percentage':100*4/6},
   'whole_declared_QA_suite':{'pass':passed,'total':len(case_results),'percentage':100*passed/len(case_results),'meets_95_percent':passed*100>=len(case_results)*95},
   'line_coverage':metrics['coverage'],
   'native':{'status':'NOT_RUN','demonstrated_passes':0,'total':2,'selected_for_execution':False}})

binary_paths=[ROOT/'target/debug'/name for name in ['devforgeai-codex-worker-probe.exe','protocol-peer.exe','console-driver.exe','crash-driver.exe']]
binary_paths += [ROOT/'independent-target/debug'/name for name in ['qa-driver.exe','protocol-peer.exe']]
write('binary-identities.json',[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in binary_paths])
raw=list((ROOT/'target/llvm-cov-target').rglob('*.profraw'))+list((ROOT/'target/llvm-cov-target').rglob('*.profdata'))
write('raw-profile-identities.json',[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in raw])
write('stop-decision.json',{'observed_at':now,'trigger':'F-02','class':'CRITICAL_PRODUCT_DEFECT',
 'meaning':'QA stop category for confirmed confidentiality/sanitization invariant violation, not a CVSS Critical claim',
 'evidence':'independent-attempts/IQ-05-private-error/result.json',
 'secondary_trigger':'M-01: finalized declared whole-QA-suite pass rate 24/26 is below 95%',
 'in_flight':[],'owned_processes':'all launched supervisors exited; independently held child handles signalled; no stored-PID cleanup',
 'allowed_remaining':'evidence preservation/readback, assessment and manual handoff only','further_product_execution':False})
write('checkpoint.json',{'intent':'run','plan':'READY for selected offline scope','execution':'STOPPED','verdict':'FAIL',
 'open_defects':['F-01','F-02'],'metric_failure':'M-01','owned_processes':[],
 'next_owner':'dev after user selects remediation; independent QA retest required after corrected candidate',
 'native_cases':'WN-01/WN-02 NOT_RUN and separately unselected','evidence_root':str(ROOT)})

spec=WORK/'docs/specs/framework/runtime/codex-worker-feasibility-v1.md'
manifest_hash=sha(ROOT/'selected-manifest.json')
prompt=f'''Use $dev in C:\\Projects\\DevForgeAI on native Windows to remediate only F-01 and F-02 in devforgeai/experiments/codex-worker-probe, then reestablish M-01 through meaningful regression checks.
Read AGENTS.md, {spec}, {ROOT/'qa-report.md'}, and {ROOT/'qa-fix.md'}. Verify their bytes using the report, fix and specification entries in {ROOT/'handoff-manifest.json'} before editing. Failed candidate: {ROOT/'selected-manifest.json'}, SHA-256 {manifest_hash}. Verify current source against it; report drift without restoring old bytes.
Follow red -> green -> refactor -> QA. Preserve production behavior, original tests, unrelated files and every prior attempt; add meaningful regression coverage for blocked pipe writes and untyped error-payload retention. Preserve the selected 20-case inventory, all required subfixtures and >=95% coverage/pass-rate floors. Do not alter the index workspace, operational copies, launcher-identity contract or live Pro profile; do not launch Codex, install, deploy or issue framework acceptance.
Return corrected source/build identities, changed-file manifest, per-defect correction/evidence map and fresh raw regression/coverage results. Do not self-close these QA findings; a separately selected independent retest must verify closure.'''

rows='\n'.join(f"| {x['id']} | {x['status']} | {str(x.get('actual','')).replace('|','/')} |" for x in case_results)
coverage_rows='\n'.join(f"| {Path(x['file']).name} | {x['lines']['covered']}/{x['lines']['count']} | {x['lines']['percent']}% |" for x in metrics['coverage']['files'])
report=f'''# FAIL — independent Windows offline worker QA

Two independently reproduced product defects remain open: blocked worker-stdin writes defeat timeout/cancellation (F-01), and untyped error payloads cross the sanitized-evidence boundary (F-02). The normal and instrumented baseline suites pass. Their numeric success does not waive these failures.

## Identity and scope

- Mode: run; plan READY for offline work; execution STOPPED after F-02. This is not full/native/framework acceptance.
- Workspace: C:\\Projects\\DevForgeAI, no Git metadata at workspace root. Candidate `{PACKAGE}`; all 31 manifest entries matched before and after. SHA-256 of selected manifest: `{manifest_hash}`.
- Specification: DFF-WORKER-FEAS-01 v1.0.0, `{spec}`, SHA-256 `{sha(spec)}`. All 335 delivery/schema entries matched before and after.
- Governing rules: AGENTS.md and available `.agents/skills/qa/SKILL.md`; hashes and final readback in input-identities.json/boundary-after.json. Companion enforcement/runtime/MVP documents provide boundaries only; no index implementation selected.
- Plan: `{ROOT/'test-plan.md'}`, SHA-256 `{sha(ROOT/'test-plan.md')}`. Predeclared cases.json, criterion-inventory.json, source-denominator.json and test-inventory.json retained unchanged.
- Developer handoff: docs/plan/framework-worker-implementation/20260915T1544548240203Z/independent-qa-handoff.md. Its supplied results were not treated as independent QA evidence.
- Host: Windows 11 Pro 10.0.26200 x64; PowerShell 7.6.6 at C:\\Program Files\\PowerShell\\7\\pwsh.exe; native C: NTFS. Cargo/rustc 1.97.1, LLVM 22.1.6, rustfmt 1.9.0, Clippy 0.1.97, cargo-llvm-cov 0.8.4. Tool version/hash receipts and host-escalated.json retained. Initial CIM/volume metadata reads were denied in sandbox, then approved read-only host queries succeeded; no product test retry occurred.
- Scope: WF-01..20 with subfixtures, 26 supplemental developer tests, independent IQ-01..06. Offline Windows only. Native WN-01/WN-02, model/account/profile effects, Linux/WSL, GUI, installation and deployment remain unselected/unqualified.

## Findings, ordered by security impact

### F-02 — High: unknown error payload persisted and emitted

Requirement: contract sections 5 and 7 permit typed observations and require unknown payloads/private data to be omitted. Captured v2/TurnCompletedNotification.json:54 defines the closed CodexErrorInfo variants. `{{"unexpectedPrivateField":"QA_PRIVATE_SENTINEL_7159"}}` matches none.

Observed: independent peer sends a failed turn with that object in error.codexErrorInfo. The harness copies the object into journal event `error_category` and emits it to stdout; it then exits 4/provider_failed. The sentinel appears in both retained files. The fixture is unchanged and the peer handle signals. No actual credential, account or private user data was accessed; the marker is synthetic.

Source/root cause: `{PACKAGE/'src/protocol.rs'}:419` copies arbitrary serde_json::Value from turn.error.codexErrorInfo before typed validation/sanitization. The observed rejected-turn result does not undo the already persisted payload. Related RPC error-code retention at line 165 warrants bounded development review but was not independently reproduced and is not a separate finding.

Evidence: independent-attempts/IQ-05-private-error/result.json, run/journal.jsonl and stdout.txt; independent/peer.rs supplies the fixture. Reproduction executed once, 0.297 seconds. Classification CRITICAL_PRODUCT_DEFECT is the QA rule's security-invariant stop category, not a CVSS Critical rating. Owner: dev; state OPEN.

Required correction: validate supported structured errors and persist only approved typed fields; reject or summarize unknown data before any append/emit. Retain legitimate structured error categories. Add negative regressions with unknown nested fields and markers; separately retest the correction.

### F-01 — High: synchronous pipe write defeats bounded dispatch and cancellation

Requirement: sections 4–6 require total/RPC deadlines, cancellation and verified teardown; tests may inject shorter limits. A received string server-request ID has no maxLength in captured ServerRequest.json:1708; the test line is below the 1 MiB line and 8 MiB total budgets.

Stimulus: peer sends an unsupported request with a 262,144-character ID immediately after initialize, then stops reading stdin. The harness attempts its rejection on that full pipe. The independent Rust driver uses total=750 ms, RPC=500 ms, grace=200 ms, teardown=500 ms. A separate cancellation subfixture sets control at 300 ms. Either bounded rejection or bounded timeout/cancellation must finish without an external watchdog.

Observed in both predeclared subfixtures: still alive at 3.000 seconds, peer handle still unsignalled, no stop_requested/process_exit/terminal. The QA supervisor force-terminates only its owned driver; peer handles then signal, verifying containment. Original fixture bytes remain unchanged. Actual exit 1 is supervisor termination, not a product timeout result. This reproduces a product hang under test limits, not a generic build/tool timeout.

Source/root cause: `{PACKAGE/'src/process_windows.rs'}:283–291` uses synchronous write_all/flush; `{PACKAGE/'src/protocol.rs'}:98` calls it on the deadline/control thread. RPC send and interrupt share the same path. No independent job watchdog can act during the blocked call. The native adapter uses this code, but no actual Codex or production-duration blocked-write trial was run.

Evidence: independent-attempts/IQ-02-deadline/ and IQ-02-cancel/, including result.json, request.json, qa-trace.jsonl, large-request-sent, stdout.txt and run/journal.jsonl. Classification MANDATORY_PRODUCT_DEFECT; safe independent work continued because owned containment remained available. Owner: dev; state OPEN.

Required correction: keep write backpressure from blocking deadline/cancel/teardown, including server replies, normal RPC writes and interrupt writes. Preserve one-turn/no-retry and exact wire behavior. Add real full-pipe regressions with independently held child handles and bounded external safety cleanup.

### M-01 — Declared whole-QA-suite pass rate below floor

All 26 predeclared offline groups reached an outcome: 24 PASS, F-01/IQ-02 and F-02/IQ-05 FAIL. 24/26 = 92.3076923076923%, below 95%. This is a valid completed project-wide metric, not an early partial-suite estimate. Its repair depends on F-01/F-02; do not inflate the denominator or suppress cases. Baseline 20 WF outcomes and six unit cases remain separate passing metrics.

## Metrics and executed checks

| Windows metric/check | Result | Evidence |
| --- | --- | --- |
| Normal baseline tests | 20/20 WF, 26/26 supplemental; no failed/ignored required cases | 01-tests |
| Instrumented baseline tests | 20/20 WF, 26/26 supplemental; no failed/ignored required cases | 04-coverage |
| Declared unit-level cases | 6/6 = 100% | test-inventory.json, metrics.json |
| Independent requirement groups | 4/6 = 66.66666666666667% | case-results.json |
| Overall declared offline QA suite | 24/26 = 92.3076923076923%, FAIL | final-metrics.json |
| Executed-line coverage | 1311/1374 = 95.41484716157206%, PASS numeric floor | coverage.json, metrics.json |
| Formatting | exit 0 | 02-format |
| Clippy --all-targets -D warnings | exit 0 | 03-clippy |
| Offline locked build | compiled all targets during normal/instrumented tests | 01-tests, 04-coverage |
| Independent QA peer/driver build | exit 0, offline path dependency on unchanged candidate | 05-independent-build |
| Branch coverage | NOT_RUN; installed help marks option unstable, no toolchain installation selected | coverage-help/stdout.txt |
| Native Codex WN-01/WN-02 | NOT_RUN, 0/2 demonstrated passes; separate prerequisites/selection | original handoff |

Coverage includes all executable lines in src (7 measured files); lib.rs has only declarations. Exclusions: tests/support/fixtures, third-party/generated dependencies, QA driver/peer. No runtime exclusions. Collection includes the complete all-targets suite, ended successfully before any independent failure; all raw profiles/merged profile retained with hashes. Additional IQ probes were preregistered as separate exploratory evidence, not coverage contributors. The single covered-line difference from developer results is a fresh execution observation, not reuse or rounding.

| Source file | Covered/executable | Collector percentage |
| --- | --- | --- |
{coverage_rows}

Normal suite took 144.812 seconds including build; instrumented suite 145.359 seconds. Formatting 0.203 seconds; Clippy 2.313 seconds. Each receipt records exact absolute cwd, argv, start/end, exit, duration, executable hash and output hashes. No normal-test failures/retries were erased. Raw profile identities are in raw-profile-identities.json; compiled artifact identities in binary-identities.json.

## Acceptance traceability

Full expected results, source locators, readiness and evidence paths are in the immutable cases.json and final case-results.json. Criteria from all contract sections are inventoried in criterion-inventory.json; native/production claims remain separate.

| Case | Outcome | Actual result |
| --- | --- | --- |
{rows}

IQ-03 independently opened both live process handles before triggering cancellation/kill, checked unsignalled before and signalled after, and observed stdin/real Ctrl+C exits 5 in 5.016 seconds, force-kill descendants signalled within clock resolution. The console signal generator is the inspected developer driver; held-handle/timing assertions are independently authored. IQ-06 combines FFI source review with these real lifecycle observations, not a claim of arbitrary file/network isolation.

## Test integrity and limitations

Inspected all first-party Rust implementation and test/support files in the frozen 31-file package, syntax/imports/serde attributes, peer behavior, console/crash drivers, and QA scripts/driver/peer. No first-party mock-generating attributes, ignored required tests, vacuous acceptance assertions or unjustified coverage exclusions were confirmed. External peer is expressly allowed by the contract. Injected evidence-write/cleanup failures are test seams, not proof of a real disk/OS failure. Passing suites do not prove complete native integration.

Existing developer cases cover receive-side timeouts/output limits, but omit full outgoing-pipe backpressure. The usage sanitization regression covers token counters, but not malformed structured error categories. These are concrete coverage gaps, not claims of deceptive intent. Independent negative result fixtures changed values, duplicate/extra keys and missing output; all were rejected with oracle_mismatch after actual dispatch.

IQ helpers derive expected messages/data from the frozen contract fixtures and captured schemas, not runtime predicates. The library and production binaries remain unchanged. Python is an evidence recorder/independent OS observer; it has no framework authority. Broad fuzzing, Miri, real native profile/sandbox/hook testing and production-duration blocked-write timing are NOT_RUN. No documentation tests exist in the inspected public sources; no separate doc-test campaign was selected.

## Stop, containment and remaining obligations

F-01 was confirmed 18:17:31 UTC after its two declared subfixtures; safe lifecycle/inspection continued. F-02 was confirmed by the final probe starting 18:19:00 UTC and ending within 0.297 seconds. No product test/build/reproduction was launched afterward. All scheduled offline groups already had terminal outcomes; no offline case is silently dropped. M-01 finalization independently confirms the below-threshold whole-suite rate.

Security stop under qa QAP-006/QAP-008: record arbitrary error-payload retention as F-02, preserve evidence, final readback/report only. No in-flight processes remained at stop. Containment used live owned process handles; no historical PID kill or cleanup deletion. All tested fixtures/evidence are retained. WN-01/WN-02 stay NOT_RUN due to unselected native authorization, captured launcher reparse admission and unresolved reviewed model/effort profile. No launcher amendment or profile inspection was attempted.

## Disposition and artifact delivery

Verdict FAIL; dev owns F-01/F-02 correction and M-01 meaningful metric restoration. No product repairs performed. Candidate readback: 31/31 unchanged. Contract readback: 335/335 unchanged. Index Cargo.toml/Cargo.lock and selected operational QA skill/AGENTS hashes unchanged. Framework acceptance NOT_EVALUATED: no qualified compiled-Rust authority decision observed. No installation/deployment authorization supplied.

Original evidence root `{ROOT}` preserved literally. QA report, fix packet, case/metric/readback files, checkpoint and manual handoff are bound by handoff-manifest.json; exact file identities are external to the mutually referencing documents. No output delivery gap remains if manifest readback succeeds.

## End-user handoff

Open C:\\Projects\\DevForgeAI in native Windows Codex. The current host skill catalog exposes `dev` at `.agents/skills/dev/SKILL.md`; QA did not invoke or install it. Remediation requires the user's next selected development assignment; QA cannot self-repair or self-close findings.

```text
{prompt}
```
'''
(ROOT/'qa-report.md').write_text(report,encoding='utf-8')

fix=f'''# QA failure handoff — F-01, F-02 and M-01

## Candidate, contracts and ownership

QA verdict FAIL. Source `{PACKAGE}`. Frozen manifest `{ROOT/'selected-manifest.json'}`, SHA-256 `{manifest_hash}`. Governing specification `{spec}`, DFF-WORKER-FEAS-01 v1.0.0, SHA-256 `{sha(spec)}`. Read current AGENTS.md. Windows 11 Pro x64, PowerShell 7.6.6, Rust/Cargo 1.97.1 on C: NTFS. Report `{ROOT/'qa-report.md'}`; exact report/fix/input hashes in `{ROOT/'handoff-manifest.json'}` entries report/fix/specification.

Dev is the remediation owner. This packet proposes the next bounded development selection; it does not itself authorize QA to repair, change operational copies, amend native identity rules, inspect live profiles, run Codex, install or deploy. Preserve all prior evidence and unrelated bytes. No historical independent finding is closed.

## F-01 — Blocking write prevents deadline/cancel handling

- State OPEN; high severity; MANDATORY_PRODUCT_DEFECT. Contract sections 4–6 and IQ-02. Complete reproduction in qa-report.md and two independent-attempts/IQ-02-* directories.
- Application ownership: src/process_windows.rs::OwnedProcess::send (283–291), src/protocol.rs::Session::receive/rpc/interrupt (98/148/452 onward).
- Real peer emits 262,144-character string request ID, then does not read stdin. Injected total/RPC/grace/teardown are 750/500/200/500 ms; cancellation variant sets control at 300 ms. Expected bounded failure/timeout/cancel with stopped tree. Both still active at 3s, no terminal, requiring supervisor termination. Peer handle signals after that; no orphan after containment.
- Root cause demonstrated by source and stimulus: synchronous write on the control/deadline thread. Restore bounded write cancellation and verified termination for server replies, normal RPC and interrupt. Do not merely enlarge deadlines, drop the case or label the external kill a timeout pass.
- Original reproduction command from C:\\Projects\\DevForgeAI: `python -B -X utf8 docs/plan/framework-worker-qa/20260915T1800141514833Z/independent_run.py backpressure`. It is intentionally one-shot and now refuses existing attempt directories. For an authorized development Red/retest, copy the QA-only scripts and independent fixture project into a fresh sibling timestamped evidence root, preserving relative directory depth, build with independent_run.py build, then use the backpressure mode there. Verify helper/oracle bytes and candidate drift before execution; do not overwrite this run. The selected tests are data/OS observations and never authorize native Codex.
- Regression/retest: both deadline and cancellation full-pipe cases, real child/descendant handles, outbound interruption under backpressure, unchanged fixtures, deterministic terminal semantics; then affected WF-01..20, required supplemental cases and fresh all-src coverage. No automatic native trial.

## F-02 — Unknown structured error copied into retained evidence

- State OPEN; high severity, CRITICAL_PRODUCT_DEFECT under QA's security-invariant stop rule. This classification is not an observed real credential disclosure or CVSS rating.
- Contract sections 5,7; captured TurnCompletedNotification.json:54 CodexErrorInfo; IQ-05.
- Application source src/protocol.rs:419 copies untyped turn.error.codexErrorInfo to persisted/emitted error_category.
- Independent fixture: failed turn with codexErrorInfo={{unexpectedPrivateField: QA_PRIVATE_SENTINEL_7159}}. Expected schema rejection or sanitized summary before persistence/emission. Actual marker in run/journal.jsonl and stdout.txt, exit4/provider_failed. No real secrets involved. Peer termination verified.
- Original one-shot command: `python -B -X utf8 docs/plan/framework-worker-qa/20260915T1800141514833Z/independent_run.py privacy`; authorized reproductions require a fresh sibling evidence root as above. Evidence independent-attempts/IQ-05-private-error/.
- Restore typed error validation/sanitization before append/emit. Preserve legitimate categories and approved numeric details. Review analogous error_code retention at protocol.rs:165 as related risk, explicitly untested here. Add content-level negative controls with synthetic private markers in malformed/unknown nested error fields and verify absence from journal/stdout/diagnostics; current usage-only sanitizer tests do not prove this boundary.
- Retest must independently check exact source/binary identities, field typing, permitted category retention, negative controls and affected protocol/inspection regression. Do not self-issue QA closure.

## M-01 — Whole declared QA suite 24/26 below 95%

Both product findings explain the missing passes; restore actual behavior. No denominator inflation, threshold relaxation, replacement oracle or suppression is permitted. The frozen 20 WF cases passed their original subfixtures, but do not waive the two extra requirement failures. All-src coverage 1311/1374 (95.41484716157206%) and declared unit cases 6/6 passed before the stop; recollect after changed runtime bytes. Keep branch coverage limitations explicit.

## Stop and return contract

No further tests ran after F-02. All 26 declared offline groups reached outcomes; WN-01/WN-02 remain NOT_RUN and unselected. All owned children observed stopped, no cleanup deletion, every attempt retained. Launcher reparse identity and reviewed Pro profile remain separate owner decisions, not fixes authorized by this packet.

Return corrected candidate/build manifest, changed-file list, per-defect correction/evidence map, Red/Green/refactor results, fresh mandatory/supplemental/unit outcomes and coverage numerator/denominator/raw profiles, explicit gaps and a separate independent QA retest handoff. Only independently executed retest can close F-01/F-02. Framework acceptance remains NOT_EVALUATED.

## Copyable next assignment

Current host catalog exposes dev. Paste this into the native Windows Codex conversation only when selecting remediation:

```text
{prompt}
```
'''
(ROOT/'qa-fix.md').write_text(fix,encoding='utf-8')
(ROOT/'handoff.md').write_text('# Manual development selection\n\n```text\n'+prompt+'\n```\n',encoding='utf-8')

# Evidence-only readback manifest: no circular self-hash, no build output inventory inflation.
named={'report':ROOT/'qa-report.md','fix':ROOT/'qa-fix.md','handoff':ROOT/'handoff.md','plan':ROOT/'test-plan.md',
 'specification':spec,'candidate_manifest':ROOT/'selected-manifest.json','candidate_after':ROOT/'candidate-after.json',
 'contract_after':ROOT/'contract-after.json','boundary_after':ROOT/'boundary-after.json','case_results':ROOT/'case-results.json',
 'metrics':ROOT/'final-metrics.json','checkpoint':ROOT/'checkpoint.json','stop':ROOT/'stop-decision.json',
 'binary_identities':ROOT/'binary-identities.json','raw_profiles':ROOT/'raw-profile-identities.json','coverage':ROOT/'coverage.json',
 'independent_python':ROOT/'independent_run.py','independent_driver':ROOT/'independent/driver.rs','independent_peer':ROOT/'independent/peer.rs',
 'independent_manifest':ROOT/'independent/Cargo.toml','independent_lock':ROOT/'independent/Cargo.lock'}
entries={k:{'expected_path':str(p),'actual_path':str(p.resolve()),'bytes':p.stat().st_size,'sha256':sha(p)} for k,p in named.items()}
for p in (ROOT/'independent-attempts').glob('*/result.json'):
    entries['result_'+p.parent.name]={'expected_path':str(p),'actual_path':str(p.resolve()),'bytes':p.stat().st_size,'sha256':sha(p)}
write('handoff-manifest.json',entries)
actual=json.loads((ROOT/'handoff-manifest.json').read_text())
assert all(sha(v['actual_path'])==v['sha256'] for v in actual.values())
print(json.dumps({'verdict':'FAIL','candidate_matches':sum(x['matches'] for x in checks),'candidate_total':len(checks),
                 'whole_suite_pass':passed,'whole_suite_total':len(case_results),'raw_profile_files':len(raw),
                 'manifest':str(ROOT/'handoff-manifest.json'),'manifest_sha256':sha(ROOT/'handoff-manifest.json')}))
