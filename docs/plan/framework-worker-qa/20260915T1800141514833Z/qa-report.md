# FAIL — independent Windows offline worker QA

Two independently reproduced product defects remain open: blocked worker-stdin writes defeat timeout/cancellation (F-01), and untyped error payloads cross the sanitized-evidence boundary (F-02). The normal and instrumented baseline suites pass. Their numeric success does not waive these failures.

## Identity and scope

- Mode: run; plan READY for offline work; execution STOPPED after F-02. This is not full/native/framework acceptance.
- Workspace: C:\Projects\DevForgeAI, no Git metadata at workspace root. Candidate `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`; all 31 manifest entries matched before and after. SHA-256 of selected manifest: `177b5894a236a02c7d322df7f04d647632094a4a3f3998e7f2a150db246e1604`.
- Specification: DFF-WORKER-FEAS-01 v1.0.0, `C:\Projects\DevForgeAI\docs\specs\framework\runtime\codex-worker-feasibility-v1.md`, SHA-256 `7cb5b0cb87e515bb4d59235b615922ab4ea07ef607b8111dde6cc73c8f101b23`. All 335 delivery/schema entries matched before and after.
- Governing rules: AGENTS.md and available `.agents/skills/qa/SKILL.md`; hashes and final readback in input-identities.json/boundary-after.json. Companion enforcement/runtime/MVP documents provide boundaries only; no index implementation selected.
- Plan: `C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1800141514833Z\test-plan.md`, SHA-256 `04c0aaf21a16c6e80e00193b55f6ec5ad2e4ec748e73ff58d29c99efc9c0b14c`. Predeclared cases.json, criterion-inventory.json, source-denominator.json and test-inventory.json retained unchanged.
- Developer handoff: docs/plan/framework-worker-implementation/20260915T1544548240203Z/independent-qa-handoff.md. Its supplied results were not treated as independent QA evidence.
- Host: Windows 11 Pro 10.0.26200 x64; PowerShell 7.6.6 at C:\Program Files\PowerShell\7\pwsh.exe; native C: NTFS. Cargo/rustc 1.97.1, LLVM 22.1.6, rustfmt 1.9.0, Clippy 0.1.97, cargo-llvm-cov 0.8.4. Tool version/hash receipts and host-escalated.json retained. Initial CIM/volume metadata reads were denied in sandbox, then approved read-only host queries succeeded; no product test retry occurred.
- Scope: WF-01..20 with subfixtures, 26 supplemental developer tests, independent IQ-01..06. Offline Windows only. Native WN-01/WN-02, model/account/profile effects, Linux/WSL, GUI, installation and deployment remain unselected/unqualified.

## Findings, ordered by security impact

### F-02 — High: unknown error payload persisted and emitted

Requirement: contract sections 5 and 7 permit typed observations and require unknown payloads/private data to be omitted. Captured v2/TurnCompletedNotification.json:54 defines the closed CodexErrorInfo variants. `{"unexpectedPrivateField":"QA_PRIVATE_SENTINEL_7159"}` matches none.

Observed: independent peer sends a failed turn with that object in error.codexErrorInfo. The harness copies the object into journal event `error_category` and emits it to stdout; it then exits 4/provider_failed. The sentinel appears in both retained files. The fixture is unchanged and the peer handle signals. No actual credential, account or private user data was accessed; the marker is synthetic.

Source/root cause: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe\src\protocol.rs:419` copies arbitrary serde_json::Value from turn.error.codexErrorInfo before typed validation/sanitization. The observed rejected-turn result does not undo the already persisted payload. Related RPC error-code retention at line 165 warrants bounded development review but was not independently reproduced and is not a separate finding.

Evidence: independent-attempts/IQ-05-private-error/result.json, run/journal.jsonl and stdout.txt; independent/peer.rs supplies the fixture. Reproduction executed once, 0.297 seconds. Classification CRITICAL_PRODUCT_DEFECT is the QA rule's security-invariant stop category, not a CVSS Critical rating. Owner: dev; state OPEN.

Required correction: validate supported structured errors and persist only approved typed fields; reject or summarize unknown data before any append/emit. Retain legitimate structured error categories. Add negative regressions with unknown nested fields and markers; separately retest the correction.

### F-01 — High: synchronous pipe write defeats bounded dispatch and cancellation

Requirement: sections 4–6 require total/RPC deadlines, cancellation and verified teardown; tests may inject shorter limits. A received string server-request ID has no maxLength in captured ServerRequest.json:1708; the test line is below the 1 MiB line and 8 MiB total budgets.

Stimulus: peer sends an unsupported request with a 262,144-character ID immediately after initialize, then stops reading stdin. The harness attempts its rejection on that full pipe. The independent Rust driver uses total=750 ms, RPC=500 ms, grace=200 ms, teardown=500 ms. A separate cancellation subfixture sets control at 300 ms. Either bounded rejection or bounded timeout/cancellation must finish without an external watchdog.

Observed in both predeclared subfixtures: still alive at 3.000 seconds, peer handle still unsignalled, no stop_requested/process_exit/terminal. The QA supervisor force-terminates only its owned driver; peer handles then signal, verifying containment. Original fixture bytes remain unchanged. Actual exit 1 is supervisor termination, not a product timeout result. This reproduces a product hang under test limits, not a generic build/tool timeout.

Source/root cause: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe\src\process_windows.rs:283–291` uses synchronous write_all/flush; `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe\src\protocol.rs:98` calls it on the deadline/control thread. RPC send and interrupt share the same path. No independent job watchdog can act during the blocked call. The native adapter uses this code, but no actual Codex or production-duration blocked-write trial was run.

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
| journal.rs | 216/220 | 98.18181818181819% |
| main.rs | 80/86 | 93.02325581395348% |
| oracle.rs | 7/7 | 100.0% |
| process_windows.rs | 241/254 | 94.88188976377953% |
| protocol.rs | 404/418 | 96.65071770334929% |
| request.rs | 250/263 | 95.05703422053232% |
| runner.rs | 113/126 | 89.68253968253968% |

Normal suite took 144.812 seconds including build; instrumented suite 145.359 seconds. Formatting 0.203 seconds; Clippy 2.313 seconds. Each receipt records exact absolute cwd, argv, start/end, exit, duration, executable hash and output hashes. No normal-test failures/retries were erased. Raw profile identities are in raw-profile-identities.json; compiled artifact identities in binary-identities.json.

## Acceptance traceability

Full expected results, source locators, readiness and evidence paths are in the immutable cases.json and final case-results.json. Criteria from all contract sections are inventoried in criterion-inventory.json; native/production claims remain separate.

| Case | Outcome | Actual result |
| --- | --- | --- |
| WF-01 | PASS | All required developer subfixtures passed in both independent normal and instrumented executions. Original case table only; global bounds/sanitization assessed separately. |
| WF-02 | PASS | All required developer subfixtures passed in both independent normal and instrumented executions. Original case table only; global bounds/sanitization assessed separately. |
| WF-03 | PASS | All required developer subfixtures passed in both independent normal and instrumented executions. Original case table only; global bounds/sanitization assessed separately. |
| WF-04 | PASS | All required developer subfixtures passed in both independent normal and instrumented executions. Original case table only; global bounds/sanitization assessed separately. |
| WF-05 | PASS | All required developer subfixtures passed in both independent normal and instrumented executions. Original case table only; global bounds/sanitization assessed separately. |
| WF-06 | PASS | All required developer subfixtures passed in both independent normal and instrumented executions. Original case table only; global bounds/sanitization assessed separately. |
| WF-07 | PASS | All required developer subfixtures passed in both independent normal and instrumented executions. Original case table only; global bounds/sanitization assessed separately. |
| WF-08 | PASS | All required developer subfixtures passed in both independent normal and instrumented executions. Original case table only; global bounds/sanitization assessed separately. |
| WF-09 | PASS | All required developer subfixtures passed in both independent normal and instrumented executions. Original case table only; global bounds/sanitization assessed separately. |
| WF-10 | PASS | All required developer subfixtures passed in both independent normal and instrumented executions. Original case table only; global bounds/sanitization assessed separately. |
| WF-11 | PASS | All required developer subfixtures passed in both independent normal and instrumented executions. Original case table only; global bounds/sanitization assessed separately. |
| WF-12 | PASS | All required developer subfixtures passed in both independent normal and instrumented executions. Original case table only; global bounds/sanitization assessed separately. |
| WF-13 | PASS | All required developer subfixtures passed in both independent normal and instrumented executions. Original case table only; global bounds/sanitization assessed separately. |
| WF-14 | PASS | All required developer subfixtures passed in both independent normal and instrumented executions. Original case table only; global bounds/sanitization assessed separately. |
| WF-15 | PASS | All required developer subfixtures passed in both independent normal and instrumented executions. Original case table only; global bounds/sanitization assessed separately. |
| WF-16 | PASS | All required developer subfixtures passed in both independent normal and instrumented executions. Original case table only; global bounds/sanitization assessed separately. |
| WF-17 | PASS | All required developer subfixtures passed in both independent normal and instrumented executions. Original case table only; global bounds/sanitization assessed separately. |
| WF-18 | PASS | All required developer subfixtures passed in both independent normal and instrumented executions. Original case table only; global bounds/sanitization assessed separately. |
| WF-19 | PASS | All required developer subfixtures passed in both independent normal and instrumented executions. Original case table only; global bounds/sanitization assessed separately. |
| WF-20 | PASS | All required developer subfixtures passed in both independent normal and instrumented executions. Original case table only; global bounds/sanitization assessed separately. |
| IQ-01 | PASS | {'subfixtures': 6, 'passed': 6} |
| IQ-02 | FAIL | {'subfixtures': 2, 'passed': 0} |
| IQ-03 | PASS | {'subfixtures': 3, 'passed': 3} |
| IQ-04 | PASS | {'subfixtures': 1, 'passed': 1} |
| IQ-05 | FAIL | {'subfixtures': 1, 'passed': 0} |
| IQ-06 | PASS | Static FFI review and held-handle lifecycle observations; bounded claim in observations.md. |

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

Original evidence root `C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1800141514833Z` preserved literally. QA report, fix packet, case/metric/readback files, checkpoint and manual handoff are bound by handoff-manifest.json; exact file identities are external to the mutually referencing documents. No output delivery gap remains if manifest readback succeeds.

## End-user handoff

Open C:\Projects\DevForgeAI in native Windows Codex. The current host skill catalog exposes `dev` at `.agents/skills/dev/SKILL.md`; QA did not invoke or install it. Remediation requires the user's next selected development assignment; QA cannot self-repair or self-close findings.

```text
Use $dev in C:\Projects\DevForgeAI on native Windows to remediate only F-01 and F-02 in devforgeai/experiments/codex-worker-probe, then reestablish M-01 through meaningful regression checks.
Read AGENTS.md, C:\Projects\DevForgeAI\docs\specs\framework\runtime\codex-worker-feasibility-v1.md, C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1800141514833Z\qa-report.md, and C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1800141514833Z\qa-fix.md. Verify their bytes using the report, fix and specification entries in C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1800141514833Z\handoff-manifest.json before editing. Failed candidate: C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1800141514833Z\selected-manifest.json, SHA-256 177b5894a236a02c7d322df7f04d647632094a4a3f3998e7f2a150db246e1604. Verify current source against it; report drift without restoring old bytes.
Follow red -> green -> refactor -> QA. Preserve production behavior, original tests, unrelated files and every prior attempt; add meaningful regression coverage for blocked pipe writes and untyped error-payload retention. Preserve the selected 20-case inventory, all required subfixtures and >=95% coverage/pass-rate floors. Do not alter the index workspace, operational copies, launcher-identity contract or live Pro profile; do not launch Codex, install, deploy or issue framework acceptance.
Return corrected source/build identities, changed-file manifest, per-defect correction/evidence map and fresh raw regression/coverage results. Do not self-close these QA findings; a separately selected independent retest must verify closure.
```
