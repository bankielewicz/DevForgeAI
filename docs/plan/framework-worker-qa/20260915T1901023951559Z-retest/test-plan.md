# F-01/F-02 independent retest plan

Intent RETEST; plan READY; execution NOT_STARTED. User selected corrected candidate and F-01/F-02, including M-01 and affected regressions.
Evidence selection: fresh sibling under docs/plan/framework-worker-qa/ as required by the selected handoff. Literal root `C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1901023951559Z-retest`.
Candidate `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`, manifest `C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1901023951559Z-retest\selected-manifest.json`, SHA256 3f65ade36cf8186fe711da73f1a2794a17d7fb51e02bf66261e9bba0ce158e39; all32 files verified. Preserved snapshot under candidate-snapshot/.
Contract DFF-WORKER-FEAS-01 v1.0.0 at docs/specs/framework/runtime/codex-worker-feasibility-v1.md, SHA256 7cb5b0cb87e515bb4d59235b615922ab4ea07ef607b8111dde6cc73c8f101b23.
Original findings and failed attempts remain under `C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1800141514833Z`; development under `C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1834258428322Z-dev`. Their readbacks are adjacent; supplied metrics do not qualify this retest.

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

From C:\Projects\DevForgeAI: `python -B -X utf8 C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1901023951559Z-retest\record.py environment`, then `test`, `format`, `clippy`, `coverage`. Commands resolved from actual Cargo manifest: test --locked --offline --all-targets; fmt --all -- --check; clippy --locked --offline --all-targets -- -D warnings; llvm-cov --locked --offline --all-targets --json --output-path C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1901023951559Z-retest\coverage.json. Cargo cwd is the original package; builds under this root/target; each suite has disjoint retained fixture roots. Test/coverage command bounds360s including compile/watchdog. Finalize metrics before further probes; valid subthreshold result stops run.

Build independently authored peer/driver in this root/independent with path dependency on unchanged candidate, offline cache only. Execute original protocol/result, corrected backpressure, lifecycle, inspect and privacy modes, then RT-01/RT-02 once each with external bounded safety containment. Distinct variant attempts are not retries. Treat any newly confirmed confidentiality/security violation as immediate stop; no further probes after it. No real secrets in fixtures.

Independent expected errors derived from captured CodexErrorInfo/JSON-RPC schemas; varied uint16 bounds, category allowlist, nested unknown data and field types. Independent held handles obtained while live; never kill historical PIDs. Original terminal/trace and exact fixture bytes verified, include worker exit and zero-job observations where available. Expected-positive category tests prevent suppress-all sanitizer from passing.

## Stop, disposition and paths

Confirmed integrity failure, valid complete subthreshold metric or critical security/data-loss defect stops all tests; ordinary functional finding retains FAIL while safe checks continue. No source repair. Preserve original failures and distinguish harness gaps. All final readbacks and stop decisions explicit.
Roles: test-plan.md, cases.json/case-results.json, selected-manifest.json/candidate-before.json/candidate-after.json, per-command receipt/stdout/stderr, metrics.json/final-metrics.json, qa-report.md, qa-fix.md on FAIL, checkpoint.json, handoff-manifest.json. Verify bytes at these literal paths before reporting delivery. F-01/F-02 start FIX_REPORTED; only valid fresh independent retest permits VERIFIED_FIXED. Framework acceptance NOT_EVALUATED; release/native decisions separate.
