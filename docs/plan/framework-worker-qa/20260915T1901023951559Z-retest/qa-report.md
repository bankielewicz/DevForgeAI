# PASS — F-01/F-02 independent Windows offline retest

Both repairs are VERIFIED_FIXED for the selected Windows offline candidate. No new product defect was observed. This verdict does not qualify actual Codex/Pro integration or establish protected framework acceptance.

## Identity and scope

- Intent RETEST; plan READY; execution COMPLETED. Selected candidate `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`, version 0.1.0, independent Cargo workspace, Rust edition 2024/MSRV 1.97.1; no declared feature combinations. Native Windows code is the selected cfg target.
- Corrected candidate manifest: selected-manifest.json, SHA-256 `3f65ade36cf8186fe711da73f1a2794a17d7fb51e02bf66261e9bba0ce158e39`. All 32 package entries matched before and after execution. No Git metadata at workspace root; source snapshot and SHA-256 manifests bind candidate identity. Source, developer tests, lockfiles, operational copies and historical evidence were preserved.
- Contract: `C:\Projects\DevForgeAI\docs\specs\framework\runtime\codex-worker-feasibility-v1.md`, DFF-WORKER-FEAS-01 v1.0.0, SHA-256 `7cb5b0cb87e515bb4d59235b615922ab4ea07ef607b8111dde6cc73c8f101b23`. All 335 bound contract/schema records matched final readback. Companion Rust enforcement/runtime boundaries are context, not additional selected implementation scopes.
- Plan: test-plan.md, SHA-256 `af5e8e21f4f2145213d28a8faa5e2c858b7fb50de82aed9a484bd92a3719f544`. cases.json and source-denominator.json were declared before testing. case-results.json supplies full specification locations and final evidence mappings.
- Developer handoff: `../20260915T1834258428322Z-dev/handoff.md` and delivery.md; 322 delivery entries verified before/after. Original QA: `../20260915T1800141514833Z/qa-report.md`; its 34 handoff entries still match. Developer metrics were inputs only; reported results below are fresh executions.
- Windows 11 Pro build 26200 x64, PowerShell 7.6.6, native C: NTFS, workspace C:\Projects\DevForgeAI. Rust/Cargo 1.97.1, LLVM 22.1.6, cargo-llvm-cov 0.8.4. Exact paths/version outputs in environment.json, host.json and 00-* receipts. No Linux/WSL substitute, dependency installation, startup changes or native Codex launch.
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
| journal.rs | 216 | 220 | 98.18181818% |
| main.rs | 80 | 86 | 93.02325581% |
| oracle.rs | 7 | 7 | 100.00000000% |
| process_windows.rs | 287 | 300 | 95.66666667% |
| protocol.rs | 468 | 485 | 96.49484536% |
| request.rs | 250 | 263 | 95.05703422% |
| runner.rs | 113 | 126 | 89.68253968% |

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
| WF-01 | Peer checks handshake ordering, exact allowed methods/fields and one turn; emits valid completed output. Exit 0 and expected result match. | All required loop subfixtures passed in normal and instrumented executions. | PASS | 01-tests/stdout.txt; 04-coverage/stdout.txt |
| WF-02 | Peer returns approval policy `on-request` or sandbox `workspaceWrite` (both subfixtures required). No turn sent; exit 3. | All required loop subfixtures passed in normal and instrumented executions. | PASS | 01-tests/stdout.txt; 04-coverage/stdout.txt |
| WF-03 | Peer returns no account, API account, Plus account and absent model/effort (all required). No turn; exit 3; no credential/login fallback. | All required loop subfixtures passed in normal and instrumented executions. | PASS | 01-tests/stdout.txt; 04-coverage/stdout.txt |
| WF-04 | Wrong thread/turn IDs, malformed JSON, conflicting duplicate response and unknown response ID (all required). Exit 4, no second dispatch. | All required loop subfixtures passed in normal and instrumented executions. | PASS | 01-tests/stdout.txt; 04-coverage/stdout.txt |
| WF-05 | Completion/started notification before start response, plus an exact duplicate. One correlated result and one terminal only. | All required loop subfixtures passed in normal and instrumented executions. | PASS | 01-tests/stdout.txt; 04-coverage/stdout.txt |
| WF-06 | Command/file approvals and unknown server request (all required). Exact cancellation/error response, no accept/rule write, exit 4 with reason. | All required loop subfixtures passed in normal and instrumented executions. | PASS | 01-tests/stdout.txt; 04-coverage/stdout.txt |
| WF-07 | Peer sends `failed` with usage-limit category. Exit 4, preserve category and open work; spawn count one. | All required loop subfixtures passed in normal and instrumented executions. | PASS | 01-tests/stdout.txt; 04-coverage/stdout.txt |
| WF-08 | Repeated cumulative usage, then a separate absent-usage run. Latest counters once; absent null. Never sum or invent zero. | All required loop subfixtures passed in normal and instrumented executions. | PASS | 01-tests/stdout.txt; 04-coverage/stdout.txt |
| WF-09 | Existing run directory with exact/changed request (both). Reject before spawn, all prior bytes unchanged. | All required loop subfixtures passed in normal and instrumented executions. | PASS | 01-tests/stdout.txt; 04-coverage/stdout.txt |
| WF-10 | Crash after spawn intent and after turn intent (both). Inspect unknown/incomplete, zero redispatch and no stored-PID kill. | All required loop subfixtures passed in normal and instrumented executions. | PASS | 01-tests/stdout.txt; 04-coverage/stdout.txt |
| WF-11 | Durable terminal then lost stdout response. Repeated inspect returns the same terminal; pagination boundaries retain every event once. | All required loop subfixtures passed in normal and instrumented executions. | PASS | 01-tests/stdout.txt; 04-coverage/stdout.txt |
| WF-12 | Trailing partial JSON, interior corrupt record, sequence gap and missing input (all). Distinct incomplete/corrupt results; zero mutation. | All required loop subfixtures passed in normal and instrumented executions. | PASS | 01-tests/stdout.txt; 04-coverage/stdout.txt |
| WF-13 | Peer launches a descendant holding pipes; Ctrl+C and stdin cancellation (both). Both handles signal, job empty, exit 5 within grace/teardown bounds. | All required loop subfixtures passed in normal and instrumented executions. | PASS | 01-tests/stdout.txt; 04-coverage/stdout.txt |
| WF-14 | Force-kill the harness while its peer and grandchild run. Independent test-held handles signal within 5 seconds. No orphan, no PID inference. | All required loop subfixtures passed in normal and instrumented executions. | PASS | 01-tests/stdout.txt; 04-coverage/stdout.txt |
| WF-15 | Peer ignores interrupt, plus cancellation before thread/turn IDs. Forced tree teardown succeeds; no late start, exit 5. | All required loop subfixtures passed in normal and instrumented executions. | PASS | 01-tests/stdout.txt; 04-coverage/stdout.txt |
| WF-16 | Peer never responds, emits oversized line and floods stderr (all). Correct deadline/output-limit reason; bounded memory/output and no live child. | All required loop subfixtures passed in normal and instrumented executions. | PASS | 01-tests/stdout.txt; 04-coverage/stdout.txt |
| WF-17 | Invalid IDs/hash, path traversal/junction and overlapping roots (all). Exit 2 before worker launch and unchanged outside sentinels. | All required loop subfixtures passed in normal and instrumented executions. | PASS | 01-tests/stdout.txt; 04-coverage/stdout.txt |
| WF-18 | Wrong output, missing output and extra output keys despite completed turn (all). Exit 4, oracle mismatch; summary cannot override. | All required loop subfixtures passed in normal and instrumented executions. | PASS | 01-tests/stdout.txt; 04-coverage/stdout.txt |
| WF-19 | Peer alters fixture; separate injected evidence-write failure. Exit 4, preserve actual failure, no success terminal, stop tree. | All required loop subfixtures passed in normal and instrumented executions. | PASS | 01-tests/stdout.txt; 04-coverage/stdout.txt |
| WF-20 | Completion/cancel ordering in both orders plus cleanup timeout. Journal order determines first stop/completion; unknown cleanup always exit 7. | All required loop subfixtures passed in normal and instrumented executions. | PASS | 01-tests/stdout.txt; 04-coverage/stdout.txt |
| IQ-01 | Independent protocol peer validates exact outbound fields, IDs, order, one turn; valid result succeeds; incorrect/extra/duplicate/missing final result fails; policy mismatch blocks before turn. | {'subfixtures': 6, 'passed': 6} | PASS | independent-attempts\IQ-01-duplicate\result.json; independent-attempts\IQ-01-extra\result.json; independent-attempts\IQ-01-missing\result.json; independent-attempts\IQ-01-policy\result.json; independent-attempts\IQ-01-valid\result.json; independent-attempts\IQ-01-wrong\result.json |
| IQ-02 | A peer sends a permitted large string server request ID, then stops reading stdin. RPC/total deadline and cancellation must remain effective; owned processes stop within injected deadlines plus grace/teardown. | {'subfixtures': 2, 'passed': 2} | PASS | independent-attempts\IQ-02-cancel\result.json; independent-attempts\IQ-02-deadline\result.json |
| IQ-03 | Independently held peer and descendant handles signal after stdin cancel, real hidden-console Ctrl+C, and forced harness termination; no historical PID mutation. | {'subfixtures': 3, 'passed': 3} | PASS | independent-attempts\IQ-03-ctrlc\result.json; independent-attempts\IQ-03-kill\result.json; independent-attempts\IQ-03-stdin\result.json |
| IQ-04 | Repeated compiled inspection of retained execution gives identical committed events, pagination without gaps, read-only bytes and no redispatch. | {'subfixtures': 1, 'passed': 1} | PASS | independent-attempts\IQ-04-inspect\result.json |
| IQ-05 | Unexpected structured error data containing synthetic private marker is rejected or sanitized before journal/stdout persistence. | {'subfixtures': 1, 'passed': 1} | PASS | independent-attempts\IQ-05-private-error\result.json |
| IQ-06 | Static FFI review checks atomic job attachment, noninherited job handle, only pipe handles inherited, no breakaway; independent negative lifecycle checks use real OS handles. | FFI ownership inspection, atomic job attachment, restricted inheritance and actual held-handle lifecycle checks; see report. | PASS | candidate-snapshot/src/process_windows.rs; independent-boundary.json; independent-attempts/IQ-03-kill/result.json |
| RT-01 | Real owned pipe RPC write returns deadline/user_cancel/invalid_control within bound; uncertain write prevents any second send; blocked interrupt consumes a single grace budget; held peer/descendant handles signal after teardown. | {'subfixtures': 4, 'passed': 4} | PASS | independent-boundary.json |
| RT-02 | Approved typed categories/numeric/null/absent details retained; unknown nested data omitted; bad category and RPC code types rejected before persistence. Independent synthetic markers absent in stdout/stderr/journal. | {'subfixtures': 12, 'passed': 12} | PASS | independent-errors.json |

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

All artifacts are under the originally selected literal root `C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1901023951559Z-retest`. Final source/input/contract/developer/original readbacks are candidate-after.json, boundary-after.json, contract-after.json, developer-delivery-after.json and original-evidence-after.json. Test plan, case maps, metrics, defect lifecycle, checkpoint and this report are delivered and bound by handoff-manifest.json. qa-fix.md is inapplicable because this retest passed. The external manifest supplies exact file hashes without circular self-hashing; delivery-readback.json verifies it and all entries after publication.

Next owner: user/project reviewer for this independent result and the separately scoped native prerequisites. No dev remediation or automatic retest is requested. The qa and dev skills are available in the current host catalog, but only qa was applied for this independent assessment. Review this report and the separate native-trial handoff in C:\Projects\DevForgeAI on Windows. Native execution still needs its own concrete selection; no copyable execution prompt is issued for unselected effects.
