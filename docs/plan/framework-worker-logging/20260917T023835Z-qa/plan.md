# Independent QA Test Plan

## Identity, selection and authorization

Run: 20260917T023835Z-qa. Intent: run (ordinary $qa request for the delivered logging candidate). Planning status: READY, subject to integrity and unchanged identities. Execution status at publication: NOT_STARTED. No additional user decision is required for the selected offline scope.

Project: C:\Projects\DevForgeAI, native Windows x64 / Microsoft Windows 10.0.26200, PowerShell 7.6.6, native Windows filesystem. No .git exists. Candidate: C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging, 67 files, exact current bytes match the development candidate-manifest.json. QA candidate-manifest.json contains absolute paths, byte lengths and SHA256. source-denominator.json binds all 15 src/*.rs files. Cargo.toml/Cargo.lock are bound; own workspace, default features only.

Selected contracts: candidate logging-contract.md (LG-01..08); original logging-design.md acceptance cases 1..12 and investigation-report.md temporal-exit/privacy clarifications; codex-worker-feasibility-v1.md v1.0.0; codex-worker-native-readiness-v1.md v0.1.0 offline slices; codex-worker-preflight-v1.md v0.1.0; codex-worker-source-identity-v1.md v1.0.0; retained diagnostic-contract.md. Exact paths and digests are in input-manifest.json and candidate-manifest.json. The delivered qa-handoff.md explicitly selects these dependencies and the amended logging/policy behavior. This does not select full framework implementation or authority.

Rules: current AGENTS.md and installed .agents/skills/qa, their references/templates, all bound in input-manifest.json. Rust owns runtime behavior. Python QA helpers only collect independent evidence. QA edits no product or developer tests and issues no framework acceptance. This is an independent conversation; no claim of a second native Codex child/session launch.

Developer claims are inputs only: 153/153 cases, 3858/4041 executable lines, native NOT_RUN. Prior failure attempts are preserved. Previous query_failed gap is claimed fixed by a test-only restricted duplicate handle; inspect real production API mapping before accepting its runtime evidence.

Authorized effects: QA-owned fixtures/harnesses, cached offline builds, tests, instrumentation, reports and disposal of owned temporary state. No dependency installation, installed-profile collection, native Codex, credential reads, configuration/operational changes, startup changes or deployment. Native WN-01/WN-02 and NI-T11/12 are NOT_APPLICABLE to this offline invocation, remain NOT_RUN for native qualification.

## Output and checkpoint binding

selected_evidence_value: C:\Projects\DevForgeAI\docs\plan\framework-worker-logging
Selection source: established logging evidence family and project policy requiring fresh disjoint evidence.
Fresh literal destination: C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T023835Z-qa

Relative paths below resolve only against that fresh destination:
- plan.md, plan-binding.json
- candidate-manifest.json, source-denominator.json, input-manifest.json, preserved-manifest.json, identity-check.json
- required-cases.json, criterion-results.json, case-results.json
- attempts/<unique-id>/receipt.json, stdout.txt, stderr.txt, fixtures/
- coverage-target/, coverage.json, coverage-analysis.json; build-target/
- qa-harness/ for independent Rust tests; supplemental-target/ for the unchanged developer harness
- integrity.md, findings.json, checkpoint.json, qa-report.md, qa-fix.md on FAIL, handoff-manifest.json, final-readback.json

Bindings already checked: 67 candidate files, 58 original files, 58 snapshot files and 37 inputs; zero mismatches. No build artifact exists for this QA run yet. Each produced executable is hashed with its source/lock binding before attribution.

Checkpoint before execution: no owned process, candidate untouched, no tests launched. Next action: save/read back plan and hash externally, inspect code/test/helper integrity and then execute ready work in this invocation.

## Acceptance inventory and independent oracles

All rows are mandatory within offline scope. Existing criterion IDs are source qualified. Numbered design cases use LD-01..12 local locators from logging-design.md's TDD and acceptance cases section.

| Criteria | Requirement / risk | Cases and independent oracle |
| --- | --- | --- |
| LG-01; LD-09 | Closed schema-3 config, 4096-byte limit, absolute strict paths, immutable digest-bound copy, final pre-spawn recheck; legacy off and native v2 composition | Package config/admission/final-boundary cases; QA-01, QA-02. Direct malformed byte/config/path stimuli; absence of server_started and preserved sentinels, copied bytes equal independently hashed input. |
| LG-02; LD-01,02,05 | Both owned readers joined; pre-stop temporal status distinct from post-stop; no relaxed guard/RPC; mandatory process_exit before terminal | Package early exit, ownership/recovery; SUP-01; QA-03,04. Real synthetic Windows children; literal independent stdout/stderr hashes, EOF, exited handle, empty job, ordered journal. |
| LG-03; LD-03,04,06,11 | Independent bounded pipes, exact stream hashes, 8 MiB combined / 1 MiB stdout line, bounded 128/32 queues, 64 chunks, 64 KiB classifier, overflow explicit | Package capture/limits/WF-16; SUP-01; QA-04,05. Real child with delayed consumer and byte literals; exact/over limits; no indefinite pipe wait; explicit error and stopped tree. |
| LG-04; LD-06,07,08,11 | Four levels; fixed optional file; 512 event / 1 MiB budget; no arbitrary text; optional failure visible and nonauthoritative; mandatory failure precedence | Package logging, query_failed-write and privacy cases; QA-06,07,08. Unique canaries and closed key checks across journal/log/emitted records; denied file handle, exact caps and outcome/cleanup assertions. |
| LG-05; LD-01,02,08 | Only known Error patterns, unknown stays unclassified, classification truncation explicit | Capture classifier suite and QA-03,04,05. Independent byte messages with near-match negatives, no diagnosis inferred from exit number. |
| LG-06; LD-12 | New capture/status/file binding required; legacy compatibility; malformed/missing/incomplete evidence rejected; interrupted prefix stays unknown | Package recovery/inspection; QA-09,10. Independently mutate isolated evidence copies and observe inspector rejection; positive unchanged control; no historical PID action. |
| LG-07; LD-10 | v3 policy differs only in 15 quoted key pairs and policy ID; all 116 argv positions/values preserved; review must rebind | Package policy/native profile and QA-11. Independent old/new JSON vector comparison, exact allowed keys, no additional argument, schema/policy mismatch denials. |
| LG-08 | All inherited cases, real query_failed, fmt/Clippy, >=95% line and case rates, preserved source | All package cases, SUP-01, QA-01..13, BUILD/FMT/CLIPPY/METRICS/PRESERVE. Raw reports recomputed; API call/source mapping and same held job for query failure. |
| DFF-WORKER-FEAS-01 sections 3..7; WF-01..08 | Strict input/layout; ordered exact wire subset, auth/model/no-tool gates, correlation/duplicates, one turn, usage, deny requests | All protocol/admission/profile/requirements package cases; QA-08,12. Independent fixed expected JSON from specification, inspect outgoing no-work/no-second-turn trace and rejection reasons. |
| WF-09..12, F-01/F-02 regression names in required-cases | Exclusive persistence, intent before effects, no replay, full-pipe bounded writes, error privacy, honest inspection | Recovery/remediation package cases, QA-09,10,12. Byte snapshots, journal sequencing, actual handles and bounded duration. |
| WF-13..16 | Windows Job Object atomic lifetime, Ctrl+C/stdin/abrupt owner death/descendants, ignored interrupt and full 120-second watchdog | process_windows/process_ownership/remediation cases, QA-03..05. Real Windows processes and held handles; timeout alone is not a PASS. |
| WF-17..20 | Denied unsafe inputs, oracle mismatch, fixture mutation and mandatory evidence failures, stop ordering/uncertain cleanup precedence | Contract/negative/runtime package cases, QA-01,02,07,12. Independent wrong results and sentinels; no success derived from worker claim. |
| NI-T01..10 (offline); SI-T01..10 | Exact two executable junctions; fixed policy and review composition; complete fixed-source inventory, single allowed source junction, final freshness, no work on unqualified profile | All native_identity/source/review/effective_profile/preflight package cases; QA-11,12,13. Synthetic roots only; strict rejection of unselected identities, exact no-work trace and source/policy byte diff. No native qualification credit. |
| Diagnostic v1 stages | Same held-job query total/active, preserve 1/1 predicate, real query_failed null counts/no RPC; first failing config category; closed labels/error precedence | diagnostic_cases/profile_protocol/effective_profile suites, QA-08,12. Independent denied/unknown canaries; source mapping of restricted handle to actual QueryInformationJobObject; no intercepted API result. |
| OUT-01 | Fresh candidate/evidence; immutable original, frozen snapshot, prior evidence/console helper | PRESERVE + QA-13. Before/after hashes and literal output-path readback. |

No unresolved scope decision. Historical specification wording declaring an interface proposed is interpreted against the current implemented manifest, not repeated as a capability claim. The explicit LG amendments control schema-3, v3 policy and privacy behavior. Other framework deliverables and Linux qualification are excluded.

## Environment and capability

Discovered cargo/rustc/rustup at C:\Users\bryan\.cargo\bin; Rust/Cargo 1.97.1, LLVM22.1.6, rustfmt1.9.0, Clippy0.1.97, cargo-llvm-cov0.8.4. Python3.10 at C:\Program Files\Python310\python.exe supports evidence helpers. PowerShell at C:\Program Files\PowerShell\7\pwsh.exe. Installed toolchains: stable Windows MSVC and 1.93; no nightly. Collector help marks --branch unstable: branch coverage NOT_RUN; no branch floor or installation implied. Offline cache availability is to be verified by the declared build; missing dependencies block dependents only.

Windows builds/process/junction checks: READY, local preparation authorized. Native Codex/installed-profile tests: excluded by explicit handoff, not a missing prerequisite for scoped offline PASS. No GUI qualification selected.

## Required cases, preparation, procedures and evidence

required-cases.json enumerates 152 package cases (49 units, 103 integration), SUP-01 and 13 independently designed acceptance cases: 166 unique required behavioral cases. Subfixtures are conjunctive and count once. Confirm the package inventory against source and Cargo listing before campaign; any discrepancy remains a gap rather than discarded cases.

All entries initially NOT_RUN. The following are READY once preceding integrity/identity prerequisites hold:
- BUILD: candidate manifest, cached lock; cargo build --offline --locked --bins --manifest-path C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe-logging/Cargo.toml; CARGO_TARGET_DIR=fresh build-target. Expected exit0 and bound binaries, timeout180s.
- FMT: cargo fmt --all --manifest-path same manifest -- --check; expected exit0, timeout60s.
- CLIPPY: cargo clippy --offline --locked --all-targets --manifest-path same manifest -- -D warnings; QA build target, expected exit0, timeout180s.
- LIST: cargo test --offline --locked --all-targets --manifest-path same manifest -- --list; QA target. This inventories only and earns no pass credit.
- PKG-001..152/METRICS: from selected candidate root, cargo llvm-cov --offline --locked --all-targets --json --output-path C:/Projects/DevForgeAI/docs/plan/framework-worker-logging/20260917T023835Z-qa/coverage.json --ignore-filename-regex [/\\]tests[/\\] --fail-under-lines 95 -- --test-threads=1. CARGO_LLVM_COV_TARGET_DIR=fresh coverage-target; WF_TEST_EVIDENCE=fresh attempt fixtures. Unfiltered campaign; timeout420s includes production watchdog. Expected all required tests including subfixtures pass; any zero case or skipped case remains visible.
- SUP-01: cargo test --offline --locked --manifest-path C:/Projects/DevForgeAI/docs/plan/framework-worker-logging/20260917T014842Z-dev/qa-harness/Cargo.toml --test raw-windows-capture -- --test-threads=1. Fresh supplemental-target and fixtures; unchanged developer harness, public OwnedProcess mapping only; timeout180s.
- QA-01 config schema/size/path/digest matrix; QA-02 last-boundary drift and legacy/version composition; QA-03 early/silent exit and closed classification; QA-04 malformed UTF8/final line and argv round trip; QA-05 delayed-consumer/queue/byte/line budgets; QA-06 four-level lifecycle/privacy; QA-07 optional sink and mandatory evidence failures; QA-08 untrusted protocol/config/privacy and closed labels; QA-09 complete-evidence mutation rejection; QA-10 historical/interrupted inspection; QA-11 exact policy comparison/native schema composition; QA-12 inherited trace/denial/cleanup independent oracles; QA-13 preservation/documentation/input inventory review.

QA preparation: author new Rust package in qa-harness with path dependency on unchanged candidate, copied locked dependency resolution, synthetic fixed child and requirement-derived expected literals. External public APIs may test process/capture/sink/Session directly; these do not replace request-admission tests or claim native execution. Use independent fixtures/requests with known existing approved peer for runner/CLI cases, and separate arbitrary byte child only for public process API checks. Freeze helper sources, fixture hashes and per-case command mappings in a supplement before their execution. No product-copy private seam is planned; existing query_failed private tests are reviewed/rerun against exact candidate.

Concrete independent procedures use cargo test --offline --locked --manifest-path <this run>/qa-harness/Cargo.toml --test independent -- <case name> --exact --test-threads=1. Fully resolved per-case vectors, child budgets <=10s, and expected byte/event predicates will be retained before execution. These are known authorized preparation, not unresolved user input. Critical/privacy violations immediately stop before the next case. Sensitivity check: mutated isolated journal/config bytes must be rejected while identical controls pass; never change candidate production bytes.

Each attempt gets exact executable/argv/cwd, start/end/elapsed/exit, environment overrides (no credentials), stdout/stderr, fixture hashes, expected/actual observations and cleanup status. Hash produced binaries before use. Product can reject a stimulus successfully; test PASS requires its independent expected reason and cleanup/absence assertions, not process exit alone.

Safety: use Job Objects and process handles for owned children. Retain fixtures, logs and failed attempts. Timeout is ERROR with owned-process observation/containment, not a product PASS. At most one corrected attempt for a demonstrated QA-only preparation fault before any terminal stop, preserving both; never automatically retry product failures or reset budget. No native attempts.

## Integrity inspection

Bound scope: all selected Rust src/tests/support, Cargo dependencies/attributes/macros/re-exports and execution/evidence helpers, plus developer supplemental harness and QA helpers. Inspect all language-level attributes and includes, imports/aliases, test body assertions, exception/return paths, fixture cleanup and metric parsing. Search is a locator only. Explicit fixtures/shorter library deadlines and denied handles are legitimate when they exercise the stated production boundary; no setup-only credit.

Preliminary reads: capture, logging, journal, runner, process owner, logging tests/support and supplemental byte harness. Remaining source/assertion inspection is required before its tests. Look especially for mock-generating attributes, cfg coverage exclusions, empty/tautological assertions, same-logic oracles, fake API return values, skipped subfixtures and sanitized output leakage. Record weak oracle gaps separately from confirmed gaming; infer no intent. Test-only private source checks cannot qualify unchanged public production wiring without source mapping.

## Metric collection and stop rules

Executed-line denominator: every first-party executable line in the 15 src/*.rs files, including Windows, CLI, errors, capture and logging. Declaration-only lib.rs expected zero executable lines; no first-party executable exclusion. Test/support fixture and dependency code excluded by path. Recompute per-file and total covered/count from raw LLVM JSON and check exact file coverage against source-denominator.json.

Coverage collection scope is the complete unfiltered 152-case package campaign. SUP-01 and QA-01..13 are separate evidence and do not contribute to that coverage figure. Do not finalize coverage if any declared contributing tests lack terminal collection or collector output is invalid. Required unit metric: all49 package unit cases; integration/acceptance/setup cases never inflate it. Check missing meaningful unit requirements during integrity review.

Each applicable floor independently >=95%, exact integer comparison (100*numerator >=95*denominator), Windows and overall identical for this single platform. Overall behavioral suite: all166 required cases, including failed/errored/skipped/blocked/unexecuted; once each. No percentage based on incomplete collection can trigger a metric failure. Complete unit or coverage subthreshold result immediately stops remaining testing. Missing measurements remain NOT_RUN/BLOCKED, not estimated FAIL. No extra passing cases or suppression to repair a metric.

INTEGRITY_FAILURE (confirmed mock decorator/gaming), valid complete METRIC_FAILURE, or CRITICAL_PRODUCT_DEFECT (authorization/security boundary or unintended protected-data loss) stops the entire run immediately. Launch no additional build/test/coverage/reproduction. Record trigger and in-flight disposition; only bounded containment, evidence, assessment and reporting continue. Ordinary mandatory conformance defects retain final FAIL while independent safe checks continue. Local prerequisite/harness gaps block only dependents; uncontained identity/ownership drift stops the run. Preserve remaining NOT_RUN IDs and observed failures.

## Final disposition and handoff

Recheck all candidate/input/preserved hashes and actual literal artifact paths. Read report/fix/checkpoint and final external manifest after writing; put cross-reference hashes there without circular self-hashes. PASS only if all mandatory offline obligations, integrity and valid floors are satisfied. FAIL takes precedence over INCOMPLETE; no ready work is left merely at planning.

On FAIL: qa-report.md and qa-fix.md, manual complete $dev prompt selecting exact defects/specifications/candidate/handoff bindings, TDD and scoped correction, preserve original failures; only separately selected independent retest closes findings. Host skill catalog currently exposes dev at C:\Projects\DevForgeAI\.agents\skills\dev\SKILL.md; no invocation or installation by QA. On INCOMPLETE route exact prerequisite and resume work to its owner. On scoped PASS the defined next step is separately selected native diagnostic preparation/authorization, without launch here.

Framework acceptance: NOT_EVALUATED. Release/deployment authorization: not granted.

