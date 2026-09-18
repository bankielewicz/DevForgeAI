# Independent offline QA report

## Identity and scope

**PASS — the selected offline diagnostic changes on Windows x64.** All 146 required cases passed, all mandatory offline invariants were resolved, and executed-line coverage is 3334/3497 (95.33886188161281098084072061767229053474%). Native Codex was not launched. Framework acceptance is **NOT_EVALUATED**.

- Run: `20260916T191731Z`; intent `run`; plan readiness `READY`; execution `COMPLETED`.
- Project: `C:\Projects\DevForgeAI`; original package: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`. No Git metadata is present.
- Plan: [test-plan.md](test-plan.md), SHA256 `48c33e0e2a3376b63f416e7330cda6237854bad20449f51258906a4d6a6051aa`.
- Frozen candidate: `C:\Projects\DevForgeAI\docs\plan\framework-worker-diagnostics\20260916T181820Z-dev\candidate-v2-manifest.json`, SHA256 `419c98b437a44ce479554170bda36b40f4b8a05b3f2307361680d44fab039540`; all 58 files retained unchanged.
- Selected instructions: [developer handoff](../../framework-worker-diagnostics/20260916T181820Z-dev/qa-handoff.md), [reviewed addendum](../../advisor-runs/20260916T185825Z-diagnostic-handoff/qa-handoff-addendum.md), diagnostic contract, original native diagnostic handoff, current AGENTS.md and four worker companion contracts. Exact paths, sizes and hashes are in [input-bindings.json](input-bindings.json); source identities are in [source-inventory.json](source-inventory.json).
- Environment: native Windows NT 10.0.26200.0 x64, C: NTFS, PowerShell 7.6.6 at `C:\Program Files\PowerShell\7\pwsh.exe`. Cargo 1.97.1 and rustc 1.97.1, host `x86_64-pc-windows-msvc`, LLVM 22.1.6; cargo-llvm-cov 0.8.4; Python 3.10.11. Actual executable paths and versions are retained in [environment.json](environment.json) and command receipts. No WSL run, network dependency acquisition or installation.

This assessment covers the bounded diagnostic change, original regressions, independent negative cases, source/test integrity and documentation consistency. It does not qualify installed-profile behavior, WN-01/WN-02, authentication/model availability, or a protected framework authority. No product source, developer test, operational skill, installed configuration, credential, cache or junction was edited. Synthetic true-review values in inherited tests are fixture data, not issued operator findings.

## Acceptance traceability

D/H/A identifiers are the plan's explicit mapping to diagnostic contract clauses, original handoff requirements and addendum clarifications. [case-results.json](case-results.json) records every unique logical test and outcome; all subfixtures are conjunctive parts of those cases.

| Criterion | Required behavior and independent expectation | Cases/checks | Actual result | Status and evidence |
| --- | --- | --- | --- | --- |
| D1/H1 | Preserve predicate order, strict errors, launch vector/identities, limits, review semantics and dispatch authority | Complete baseline/current production comparison, original 133, QI07 | Diagnostic additions preserve rejecting behavior; protected launch/identity/request files match baseline; public runner retains compiled verification | PASS; [predicate audit](predicate-audit.md), [diff](independent-baseline.diff), original log |
| D2/H2 | Real source review rejection at both boundaries; closed labels, original error, no dispatch | QI03 and inherited private/public rejection cases | Both boundaries report review_rejected; original denial persists; journal failure takes precedence; no work trace | PASS; [runtime readback](independent-runtime-readback.json), attempt 07 |
| D3/H2/A1 | One accounting query supplies both counts; exited descendants counted; query error gives query_failed/null counts | QI01, QI02, QI05 and inherited process cases | Four real denied-access query subfixtures preserve windows_error_5; journal-failure case returns evidence_write_failed; exited child yields total=2, active=1 at initialize and config | PASS; [query evidence](query-failed-evidence.json), source audit, attempt 07 |
| D4/H3 | Closed RPC categories; unknown reason cannot become label; fallback does not claim transport cause | QU06, QI04, QI06, inherited protocol cases | Literal expected labels/errors match; arbitrary error maps to other_rpc_failure without payload retention | PASS; independent source/oracles, attempt 07 |
| D5/H2/H3 | Config shape, active-policy rejection, exact session keys/cardinality, all origin/source paths and first-failure order | QU01–QU05, QI04, inherited effective-profile cases | Independent absent/malformed/unknown/active and multi-failure fixtures match literal expected rejection and ordering; sanitized success projection matches exact output | PASS; [harness](harness/config_cases.rs), case results |
| D6/H3/H4 | Closed fields/privacy; no operator finding or work authorization from diagnostics | QU05, QI03, QI04, QI07; inherited exact all-false gate unit; public wiring audit | Unique canaries absent; contaminated negative control rejected; recording diagnostics does not alter review; untrusted extra fields reject | PASS with the cause-specific limits below; runtime records, predicate/integrity audits |
| D7/H4 | Evidence-write precedence, cancellation/deadline/cleanup, no thread/turn during synthetic preflight | QI01–QI07; inherited F-01/F-02 and recovery/WF tests | Required error/cleanup assertions passed; all 19 retained independent runtime fixtures stopped with active=0 and no thread/turn | PASS; runtime readback, original/independent raw logs |
| H5/A3/A4 | All 133 inherited cases/subfixtures plus new required cases; original package coverage and quality checks | 146 unique cases, original instrumented 133, fmt/Clippy/build/docs | 146/146 required; 46/46 units; coverage floor met; quality commands exit 0 | PASS; test/coverage analyses and command ledger |
| H6/A2 | Integrity, sensitive oracles, unchanged original, exact wrapper mapping and input readback | Syntax/import/assertion review, negative control, compiler dependencies, hashes | No confirmed mock/gaming finding; compiler dependency file maps all 11 wrapped original modules; 230 candidate/snapshot and 123 selected/prior-input checks match | PASS; [integrity review](integrity-review.md), source mapping/readbacks |
| A5 | Report branch collection independently, with actual capability evidence | Attempt 01, installed toolchain inventory | Collection NOT_RUN: cargo-llvm-cov --branch requires nightly; only stable toolchains installed | Reporting requirement satisfied; no branch percentage or threshold fabricated |

### Resolution of the required query_failed case

Development's missing runtime evidence is resolved in this QA scope. The QA-only wrapper includes the actual original Rust files by absolute path; no source copy, production seam or replacement API is used. It legally duplicates the same owned Windows Job Object with TERMINATE access but without QUERY access, retains the original handle, and restores it before cleanup. Actual `QueryInformationJobObject` returns Windows error 5. The unchanged production accounting/guard code emits the closed `query_failed` diagnostic with `total_processes:null` and `active_processes:null`, then preserves `windows_error_5`.

QI01 exercises initialize/before_send through public `Session::preflight` on the mapped source, config_read/before_send through the original private RPC path, and config_read/after_receive and final_check through the original private guard entry. All four fixture traces are empty and all real jobs finish at active=0. QI02 independently confirms that failed diagnostic persistence takes precedence. [query-failed-evidence.json](query-failed-evidence.json) binds the actual observations, stimuli and journals; [harness-source-mapping.json](harness-source-mapping.json) binds compiler dependency evidence.

These are runtime tests of the frozen implementation through the declared QA access wrapper. They do not demonstrate a spontaneous installed-host failure or full native runner execution. Wrapper path-sensitive `CARGO_MANIFEST_DIR` behavior is not treated as equivalent to the original package; original CLI/admission/wiring evidence comes from the original campaign and source comparison. Wrapper profiles were not merged into line coverage. The original coverage collection still does not execute the query_failed expression; its supplemental runtime proof is stated separately.

QI07's public review calls use an all-false review with an intentionally absent inventory. That rejection alone cannot distinguish false-findings rejection from missing-inventory rejection. The specific all-false policy is separately proven by inherited `request::review_v2_cases::preflight_accepts_false_findings_while_run_requires_all_true`, the unchanged review predicate and public runner wiring. QI07 proves diagnostics leave review bytes unchanged and fail to make those unqualified/extra-field inputs acceptable. No broader cause is inferred from its ambiguous rejection.

## Test integrity

[integrity-review.md](integrity-review.md) records inspection of the 58-file candidate, 47 Rust files, attributes/imports, assertions, fixture peers, process drivers, review seams and QA helpers. Standard Rust/serde derives were resolved against the pinned dependencies. No ignored tests, coverage suppression, mock-generating attributes, custom test macros or failure-to-pass retry logic were found in this bounded review. `allow(dead_code)` in shared fixture support does not suppress executable coverage.

Independent expected errors, event field sets, policy tables and canary oracles were authored in the new harness. Tests use real synthetic peer processes and owned files/jobs; they do not return fabricated production results. QU05 deliberately contaminates an observation and confirms the same privacy oracle rejects it. Setup-only helpers receive no separate passing credit. Private fixture seams and their limits are identified in the integrity report. Developer results are comparisons only; no historical pass is substituted for current execution.

## Metrics and environment

| Selected platform | Metric | Numerator | Denominator | Percentage | Floor | Result |
| --- | --- | ---: | ---: | --- | --- | --- |
| Windows x64 (also overall selected scope) | First-party executed lines | 3334 | 3497 | 95.33886188161281098084072061767229053474% | >=95% | PASS |
| Windows x64 | Required units | 46 | 46 | 100% | >=95% | PASS |
| Windows x64 | Required integration/regression cases | 100 | 100 | 100% | All mandatory cases | PASS |
| Windows x64 | Overall required suite | 146 | 146 | 100% | >=95% and all mandatory cases | PASS |
| Windows x64 | Branch coverage | unavailable | unavailable | NOT_RUN | No new numeric floor | Nightly prerequisite unavailable |

The unique inventory is 133 inherited (40 unit +93 integration) plus 13 independent (6 unit +7 integration). The instrumented 133/133 repetition earns no extra cases. There are no unresolved failed, errored, skipped, blocked or unexecuted required behavioral cases. Attempt 07 filters 40 duplicate inherited definitions out of the QA wrapper; every one is executed in the original unfiltered 133-case campaign. The separate doctest command discovers zero cases and earns no behavioral credit.

Coverage uses the completed original `--all-targets` campaign on all 13 declared `src/*.rs` files. `lib.rs` has only module declarations and 0 executable lines; none of the first-party executable behavior is excluded. Dependencies, fixture peers, tests and the QA harness are outside this declared production denominator. Raw [coverage.json](coverage.json), [coverage-analysis.json](coverage-analysis.json), [test-analysis.json](test-analysis.json), the original logs and terminal receipt bind the finalized collections. Integer floor comparison was used; no below-floor value was rounded upward. At 3497 lines the minimum is 3323; 3334 exceeds it by 11. No metric triggered a stop or further collection.

| Production file | Fresh covered/total | Developer covered/total | Covered delta |
| --- | ---: | ---: | ---: |
| diagnostic.rs | 19/19 | 19/19 | 0 |
| effective_profile.rs | 623/633 | 623/633 | 0 |
| journal.rs | 263/266 | 263/266 | 0 |
| launch_policy.rs | 21/23 | 21/23 | 0 |
| main.rs | 124/132 | 124/132 | 0 |
| native_identity.rs | 95/97 | 95/97 | 0 |
| oracle.rs | 7/7 | 7/7 | 0 |
| process_windows.rs | 316/335 | 316/335 | 0 |
| profile_sources.rs | 641/671 | 641/671 | 0 |
| protocol.rs | 662/694 | 663/694 | -1 |
| request.rs | 393/407 | 393/407 | 0 |
| runner.rs | 170/213 | 170/213 | 0 |
| lib.rs | 0/0 | 0/0 | 0 |

[coverage-comparison.json](coverage-comparison.json) compares identical protocol segment layouts. The only zero/nonzero segment difference is line 469, column 10: developer count 1, QA count 0, at the closing expression of `initialize`'s `initialized` send. This accounts for the observed one-line difference; the evidence does not establish why the executions differed. No speculative timing explanation or per-file 95% floor is imposed, and no coverage retry was performed.

## Executed commands and retained attempts

Every command has its actual argv, executable hash, cwd, selected environment overrides, start/end timestamps, elapsed time, exit, stdout/stderr hashes and timeout in `attempts/<id>/receipt.json`. [execution-ledger.json](execution-ledger.json) indexes them. Original commands ran from the frozen original package; harness commands ran from the separate declared harness. Outputs use only fresh QA target/evidence locations, with `--offline` and the lockfile where applicable. Outer test timeout was 600 seconds; the production 120-second WF-16 watchdog was executed normally.

| Attempt | Command after cargo | Outcome |
| --- | --- | --- |
| 01-branch-capability | llvm-cov show-env --branch | Exit 0; explicit nightly-required warning, no branch collection |
| 02-original-inventory | test --locked --offline --all-targets -- --list | Exit 0; 133 names, no behavior credit |
| 03-harness-lock | generate-lockfile --offline | Exit 0; 33 packages resolved from cache |
| 04-harness-build | build --locked --offline --bins | Exit 0; synthetic peer built |
| 05-harness-inventory | test --locked --offline --lib qa_ -- --list | Exit 101, QA compilation gap HG-01; no tests ran |
| 06-harness-inventory | test --locked --offline --lib qa_ -- --list | Exit 0 after bounded QA helper correction; 13 names |
| 07-independent-cases | test --locked --offline --lib qa_ -- --test-threads=1 | Exit 0; 13/13, 1.235 seconds |
| 08-format | fmt --all -- --check | Exit 0 |
| 09-clippy | clippy --locked --offline --all-targets -- -D warnings | Exit 0 |
| 10-build | build --locked --offline --bins | Exit 0 |
| 11-doctests | test --locked --offline --doc | Exit 0; 0 discovered |
| 12-original-all-targets | test --locked --offline --all-targets | Exit 0; 133/133, 160.656 seconds |
| 13-original-coverage | llvm-cov --locked --offline --all-targets --json --output-path C:/Projects/DevForgeAI/docs/plan/framework-worker-diagnostics-qa/20260916T191731Z/coverage.json | Exit 0; 133/133, 172.687 seconds |

Documentation review checked diagnostic meanings, unchanged denial/authority boundaries, available command forms and cross-document consistency. All eight local Markdown links discovered in the selected README/handoff/contract/addendum resolve; [documentation-links.json](documentation-links.json) records them. No documentation-only check is represented as runtime acceptance.

## Defects, gaps and continuation decisions

No confirmed product defect or unresolved mandatory offline case was found. [findings.json](findings.json) retains these distinct records:

| ID | Class and impact | Disposition and owner | Evidence |
| --- | --- | --- | --- |
| HG-01 | QA-owned prerequisite/harness gap: windows-sys did not export the imported JOB_OBJECT_TERMINATE constant; compilation stopped before testing | Resolved before initial behavioral execution by using the installed SDK's documented 0x0008 constant in the QA helper only. No product repair or oracle relaxation | Attempt 05 raw error, complete input snapshot and assessment; attempt 06 compile; attempt 07 runtime |
| ME-01 | Branch measurement unavailable with installed stable toolchains | NOT_RUN, disclosed per addendum; no required branch floor or request to install nightly | Attempt 01 warning and environment inventory |

The attempt-05 gap was observed and classified before follow-on execution. The first harness inputs and failed receipt remain intact; only the QA-owned constant declaration changed. No product behavior case failed and no result was erased. No confirmed integrity failure, critical defect or valid completed below-floor metric occurred. Safe independent work continued under the saved plan. All scheduled processing is complete; no required offline tests remain.

All 19 retained independent process fixtures report stopped=true and active=0. The inherited recovery/cleanup assertions passed. Final [process-readback.json](process-readback.json) observed no process image under the QA output root; all command receipts are terminal. No unrelated process was terminated. Retained build outputs/fixtures are evidence and were not deleted. Three original CLI test families created six fresh retained roots in `docs/plan/framework-worker-trials`; their exact names and the absence of removed pre-existing roots are in [trial-ownership.json](trial-ownership.json). Child-only synthetic USERPROFILE/PROGRAMDATA were used for source CLI tests; installed user/system profile collection was not performed.

## Disposition and preservation

Offline product QA: **PASS** for this exact candidate and Windows scope. A fix packet is not applicable because there are no confirmed defects to hand to dev. Source mapping is supplemental with its stated limits; the required inherited campaign ran against the frozen original.

[candidate-readback-after.json](candidate-readback-after.json) records 230 matching file checks: baseline snapshot, first diagnostic snapshot, final snapshot and original candidate. [input-readback-after.json](input-readback-after.json) records 123 matching selected/prior input bindings. Prior evidence was preserved; this statement relies on scoped readbacks and writes confined to new QA outputs, not a claimed recursive rehash of every historical artifact. All 131 produced executable bindings are retained in [build-manifest.json](build-manifest.json).

Framework acceptance: **NOT_EVALUATED**. Native qualification and WN-01/WN-02: **NOT_RUN**. Release/deployment authorization is not granted by this report. The next project-defined step is one separately authorized, bounded, no-work native diagnostic attempt, following [native-diagnostic-handoff.md](native-diagnostic-handoff.md).

## Artifact delivery

Original and actual evidence root: `C:\Projects\DevForgeAI\docs\plan\framework-worker-diagnostics-qa\20260916T191731Z`. Required output paths are `test-plan.md`, `qa-report.md`, `case-results.json`, `findings.json`, `checkpoint.json`, and `artifact-index.json`; the downstream handoff is `native-diagnostic-handoff.md`. The initial checkpoint is retained as `checkpoint-initial.json`. No alternative destination was substituted.

The final external [artifact-index.json](artifact-index.json) binds the actual bytes using `artifacts` entries keyed by relative path, including `qa-report.md`, `test-plan.md`, `checkpoint.json`, `native-diagnostic-handoff.md`, raw receipts/logs, coverage, harness inputs and final source readbacks. Large generated build trees are represented by executable bindings in build-manifest.json rather than a claim to seal every intermediate object. Reparse entries are recorded without following them. `publication-readback.json` records literal-path readback of the manifest and every indexed file. Neither report nor index embeds its own digest. Any failure during publication prevents claiming completed delivery; final conversation reports actual readback only.

## End-user handoff

Open `C:\Projects\DevForgeAI` on native Windows in Codex. Next owner: the user/operator selects the native diagnostic task; the following executor must honor that bounded selection. No new skill, installation or automatic follow-up was invoked. The current host exposes qa/dev/advisor, but this downstream task is a direct project diagnostic selection, not a new QA run or fabricated skill command.

The following is a conversation prompt for a **separate authorization**, not an executed shell command:

```text
In C:\Projects\DevForgeAI on native Windows, authorize one bounded no-work native diagnostic attempt under docs/plan/framework-worker-diagnostics-qa/20260916T191731Z/native-diagnostic-handoff.md. Verify artifact-index.json entries qa-report.md, native-diagnostic-handoff.md, input-bindings.json and build-manifest.json before preparation, and verify the frozen candidate manifest SHA256 419c98b437a44ce479554170bda36b40f4b8a05b3f2307361680d44fab039540. Use a fresh evidence directory and bind exact fresh fixture/request/all-false review/inventory digests; refresh affected source bindings after any host permission change. Preserve all prior evidence. Launch at most one bounded no-work attempt, with no thread/turn, true operator findings, retries, policy relaxation or installed-state changes. Report the observed predicate and whether it indicates a defect, prerequisite or contract gap; do not implement a repair or claim WN-01/WN-02 or framework acceptance.
```
