# Independent offline QA plan

## Identity, selection and authorization

Intent **run**: plan and execute in this invocation. Execution NOT_STARTED; plan READY for isolated preparation and execution. Selected host is native Windows x64, build 10.0.26200, PowerShell 7.6.6, C: NTFS. Project is `C:\Projects\DevForgeAI`, with no Git metadata. Scope is only the frozen worker diagnostic candidate and its offline regressions. Applicable rules are root AGENTS.md and the operational qa skill/references, all bound in input-bindings.json.

Candidate package: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`. Selected manifest: `C:\Projects\DevForgeAI\docs\plan\framework-worker-diagnostics\20260916T181820Z-dev\candidate-v2-manifest.json`, SHA256 **419c98b437a44ce479554170bda36b40f4b8a05b3f2307361680d44fab039540**. All 58 original and 58 snapshot file bindings match at intake. The 99 development input bindings also match. Cargo.toml/Cargo.lock are selected unchanged dependencies. Current native tools: cargo/rustc 1.97.1, LLVM 22.1.6, cargo-llvm-cov 0.8.4; pinned dependencies are discovered from Cargo.toml. Offline cache/build availability is verified by preparation, with no installation authorized.

Normative selected inputs are the user's qa-handoff.md and reviewed qa-handoff-addendum.md, final diagnostic-contract.md, original native-diagnostic-handoff.md, delivery.md and review-notes.md. Four worker companion contracts supply unchanged constraints and regression criteria (DFF-WORKER-FEAS-01, DFF-WORKER-NATIVE-01, DFF-WORKER-PREFLIGHT-01, DFF-WORKER-SOURCE-IDENTITY-01). Native WN-01/WN-02, installed source collection, framework acceptance, installation and policy relaxation are excluded. Previous development reports are context and comparison evidence only, never reused QA passes.

Authorized effects: fresh local QA fixtures, independent Rust harnesses, synthetic local peers, local offline builds/tests/coverage and reports. No native Codex process, installed configuration/cache/skills, alternate CODEX_HOME, credential or persistent changes. No candidate or original developer-test edits. No agent delegation is selected. Source and evidence are preserved.

## Output and checkpoint binding

Selected evidence value and resolved fresh destination: `C:\Projects\DevForgeAI\docs\plan\framework-worker-diagnostics-qa\20260916T191731Z`. This sibling QA evidence family follows repository docs/plan policy and the user's fresh-disjoint requirement.

Paths relative to that root: test-plan.md; input-bindings.json; candidate-readback-before.json and candidate-readback-after.json; first-party-inventory.json; source-inventory.json; inherited-inventory.json; case-inventory.json; integrity-review.md; predicate-audit.md; harness/; attempts/<unique-id>/{started.json,stdout.bin,stderr.bin,receipt.json}; target/; coverage-target/; coverage.json; coverage-analysis.json; fixtures/<attempt>/; case-results.json; findings.json; checkpoint.json; qa-report.md; qa-fix.md only on FAIL; artifact-index.json. The plan's digest is recorded externally before product execution. Build hashes will be captured from QA-owned target directories.

## Acceptance inventory and independent oracles

Local D IDs bind the ordered clauses of diagnostic-contract.md; H IDs bind qa-handoff required scope 1..6; A IDs bind addendum 1..5. All rows are mandatory, except separate branch reporting has no numeric threshold.

| Criteria | Required behavior and risk | Cases/evidence |
|---|---|---|
| D1/H1 | Diagnostic additions preserve predicate order, strict errors, launch vector, identities, review semantics, limits, cleanup and dispatch authority; high authorization risk | Complete baseline/current production diff and unchanged hashes; inherited regression inventory; QI07 |
| D2/H2 | Source rejection has closed post_spawn/post_preflight labels, original error and no RPC/work after denied source | QI03; original dispatch/runner audit; inherited private and CLI cases |
| D3/H2/A1 | One held-job query supplies both counts; exited descendants counted; real query error projects query_failed and both counts null, preserves error | QI01, QI02, QI05, inherited process cases; static single-query audit |
| D4/H3 | RPC labels closed; other_rpc_failure is a cause-neutral fallback; unknown server values absent | QU06, QI04, QI06; inherited profile protocol |
| D5/H2/H3 | Config absent/malformed/unknown/active data, exact keys/cardinality, origin/path coverage and first failure order retain original errors and closed labels | QU01..QU05; QI04; inherited effective-profile cases with every subfixture |
| D6/H3/H4 | Unique nested canaries absent from success/denial diagnostics; no raw config/server errors; diagnostics cannot issue findings or permit work | QU05, QI03, QI04, QI07; exact serialized field-set oracles and preserved review bytes |
| D7/H4 | Evidence-write failure precedence, cancellation, deadlines, real process cleanup, synthetic traces have no thread/turn | QI01..QI07 and inherited recovery/F-01/F-02/WF-13..16/19..20 |
| H5/A3/A4 | Complete original 133 logical Rust cases and all subfixtures, format/Clippy/build/docs; all 13 first-party src files in line denominator | inherited-inventory.json and normal/coverage raw logs; quality receipts |
| H6/A2 | Integrity and sensitivity, no candidate mutation, no relocated identity assumptions, exact input/source readback | integrity-review.md, harness mapping, independent literal oracles with negative controls, final readback |
| A5 | Separately report branch collection capability/result | installed compiler/tool help; branch NOT_RUN if nightly unavailable; no fabricated percentage |

No additional deliverables are selected from dependency references. Baseline source preservation and every old WF/NI/SI/F-01/F-02 scenario remain required. Native qualification remains excluded and unperformed. No performance SLO is invented; the production 120-second watchdog remains in the campaign.

## Required case inventory and readiness

The inherited-inventory.json contains all **133** named inherited Rust cases; 40 are units, 93 integration/regression. All subfixtures in those bodies are conjunctive parts of their parent case. Static source inventory will cross-check that inventory; actual --list will verify the compiled names before tests. Every inherited case is READY with prerequisites: candidate match, completed integrity review, offline build and QA-owned output binding. They run with their original setup from the original package. No skip or filtered inherited test run is permitted.

New required cases (each logical case counted once; 6 unit and 7 integration cases):

| ID / Rust name suffix | Category | Criteria | Procedure and independent expected result |
|---|---|---|---|
| QU01 qa_u01_config_shape_and_absence | unit | D5 | Independent valid config then missing/null/wrong-type roots/fields; literal protocol_error/profile_unqualified and first location table |
| QU02 qa_u02_policy_precedence | unit | D5 | Independently specified active provider/endpoint/settings/features/apps/MCP/plugins; multi-failure inputs select earliest contract group |
| QU03 qa_u03_session_keys_and_count | unit | D5 | Missing/extra session keys, zero/two session layers; exact fixed_keys/session_flags_count ordering and original denial |
| QU04 qa_u04_origin_layer_paths | unit | D5 | Unknown/uncovered origin/layer source, invalid cwd/source path, all origins including unselected keys checked |
| QU05 qa_u05_projection_privacy | unit | D5,D6 | Unique canaries at every unknown nested scope; exact success projection and closed rejection metadata contain none; deliberately contaminated output must fail the canary oracle |
| QU06 qa_u06_rpc_closed_labels | unit | D4 | All documented reason labels plus unique arbitrary error -> literal cause-neutral other_rpc_failure; no unknown input becomes a serialized label |
| QI01 qa_i01_query_failed_runtime | integration | D3,D7 | Real Windows denied-access Job Object query through unchanged process accounting and Session guard; both counts null, query_failed, windows_error_5 returned, no send/dispatch, restore ownership and verify tree empty |
| QI02 qa_i02_query_failed_write_precedence | integration | D3,D7 | Same real API failure with journal failpoint; evidence_write_failed wins, no successful diagnostic emitted, restored real cleanup |
| QI03 qa_i03_source_review_boundaries | integration | D2,D6,D7 | Real missing-review rejection at both boundaries through frozen source; closed literal events, unchanged input, no work; source diagnostic write failure remains failure |
| QI04 qa_i04_rpc_and_config_privacy | integration | D4,D5,D6 | Independently authored peer sends initialize/config RPC errors and nested config canaries; exact stage/error/diagnostic and sanitized success projection, no thread/turn |
| QI05 qa_i05_exited_descendant | integration | D3,D7 | Independent peer launches and waits for detached child to exit before response; guard rejects total=2, active=1 at initialize and config response |
| QI06 qa_i06_cancel_deadline | integration | D4,D7 | Cancellation/invalid control and a nonresponding peer hit literal stop categories; bounded teardown, no thread/turn, evidence failure retained |
| QI07 qa_i07_false_review_no_authority | integration | D1,D6,D7 | All-false v2 review rejects through actual public review validator before inventory collection; recording diagnostic observations does not change findings or allow review; unknown diagnostic/authority fields cannot turn review valid |

All new cases are READY for authorized preparation. QI01/QI02 have a concrete technique to validate, not a proven runtime result. If technique cannot be safely implemented without changing production bytes, mark NOT_RUN/BLOCKED with concrete prerequisite and continue independent checks. No absence-of-seam inference or waiver is permitted.

Every case requires fresh QA-owned fixture paths, retained literal stimulus/expected/error/trace/journal evidence, empty real process tree at teardown, and candidate/input recheck. Failure to set up a fixture is ERROR/harness gap, never product Red or PASS. No rerun erases its first attempt. Only a corrected QA-owned harness may be retried before a terminal stop, retaining both attempts and hashes.

Pre-execution discovery clarification: three inherited tests create fresh tempfile roots under `C:\Projects\DevForgeAI\docs\plan\framework-worker-trials` with NI-admission-, NI-sources-, and RT-source-type- prefixes because their original CLI validates this location. Preserve those fresh owned roots and record directory membership before/after; never reuse existing trial evidence. Synthetic profile-sources subprocesses explicitly set child-only USERPROFILE/PROGRAMDATA to owned synthetic directories, so they do not collect the installed user/system Codex profile. They still inspect applicable workspace/ancestor instruction identities under the original CLI contract. Native identity admission hashes the fixed executable but does not execute it; the original invalid-policy runner test must reject before spawn. Original tests' synthetic true review values are test data, not human operator findings or native authorization. These effects are part of the specifically required original 133-case campaign.

## Independent harness boundary

Absolute harness root: `C:\Projects\DevForgeAI\docs\plan\framework-worker-diagnostics-qa\20260916T191731Z\harness`. Public-interface tests prefer a dependency on the original package. For private process/session access, a test-only crate wrapper may compile original modules directly by absolute #[path] / include! references. All 13 production files remain byte unchanged. The wrapper contains only harness functions/tests; it does not substitute production functions or rewrite predicates. Declared test-only delta: wrapper module topology, a private helper temporarily exchanging the test process's held job handle for a duplicate of the SAME job without query permission, and QA assertions/stimuli. The original handle remains owned and is restored before teardown; no arbitrary memory writes or handle closing behind Rust ownership.

Path-sensitive production uses of CARGO_MANIFEST_DIR are request::validate native/peer admission, profile_sources native roots, and main CLI source collection. Private-wrapper tests will not qualify these relocated behaviors. Original-package inherited campaign and public dependency calls/audit supply their evidence. Include-relative records/fixtures resolve at original production paths and are hash-bound. Main and lib entry wiring are qualified on the original package. Copy/wrapper evidence is supplemental until exact source mapping, affected paths and intended source correspondence are verified. No new production injection seam is authorized.

## Commands, environment, effects and sequence

Native cargo is `C:\Users\bryan\.cargo\bin\cargo.exe`; Python recorder is `C:\Program Files\Python310\python.exe` with `-B -X utf8`, evidence only. Cwd for inherited commands is the original package. Commands originate in inspected Cargo.toml and delivery.md; dependency resolution is locked/offline. A recorder sets only scoped CARGO_TARGET_DIR, CARGO_LLVM_COV_TARGET_DIR, WF_TEST_EVIDENCE and color/no-network options, retaining argv, cwd, timestamps, exit and byte hashes. No credentials/environment values are collected.

1. Save/read back this plan; record its digest and full case map. Inspect first-party attributes/imports, assertions/control flow, helpers, fixture peers and evidence processing; inspect each new QA helper before use.
2. Record versions/help and tool hashes. `cargo test --locked --offline --all-targets -- --list` builds/lists inventory only (no behavioral credit). `cargo build --locked --offline --bins` establishes standalone private-test peers. Discover branch capability from installed help/compiler before deciding branch collection.
3. `cargo fmt --all -- --check`; `cargo clippy --locked --offline --all-targets -- -D warnings`; `cargo test --locked --offline --doc`; `cargo build --locked --offline --bins` with QA target.
4. Build and execute all 13 new required independent cases in harness; retain per-case assertions/raw output. Selected private-only test filters exclude inherited duplicate definitions, never the original campaign. Exact harness commands and helper hashes are bound in the pre-execution harness manifest/receipt.
5. `cargo test --locked --offline --all-targets` with normal QA target; allow 120-second WF-16 plus suite/build overhead (outer 600-second bound). No native Codex launch.
6. `cargo llvm-cov --locked --offline --all-targets --json --output-path C:/Projects/DevForgeAI/docs/plan/framework-worker-diagnostics-qa/20260916T191731Z/coverage.json` with fresh coverage target and fixtures. Same 133 cases, not an additional case denominator. Coverage is finalized only when all declared inherited contributors finish and usable JSON covers the full inventory.
7. Recompute raw metrics and per-file counts, compare developer counts, review docs/links, read back candidate/snapshot/input/prior evidence identities, persist report/results/checkpoint and artifact bindings.

Independent test evidence supplements original coverage; its profiles are NOT merged from a different crate layout. Required line measurement is explicitly the full inherited campaign on original frozen package, including every original+added developer case. All independent cases are mandatory for behavioral acceptance even where outside that collector.

No automatic batch may launch follow-on tests after observing a whole-run stop. Sequential assessment boundaries follow each terminal suite/command. An ordinary mandatory failure permits safe independent continuation but keeps final FAIL. Any confirmed mock decorator/gaming, critical authorization/privacy/preservation defect or valid completed below-floor metric stops the whole run immediately. Contain owned in-flight work, then only preserve/read back/report. Timeouts never imply a product failure without evidence.

## Metrics and exit rules

First-party source denominator: exactly all 13 src/*.rs in source-inventory.json, including lib.rs at 0/0 when reported. No first-party exclusions. Test/support/QA harness/dependency code is outside this runtime denominator. Developer 3335/3497 is comparison only; fresh LLVM determines actual counts. At denominator 3497, 3323 lines are necessary for >=95%. No per-file 95% floor is imposed. Report numerator/denominator, full-precision comparison, per-file deltas, branch separately. No nightly toolchain is installed at intake; stable --branch feasibility will be checked without installing or RUSTC_BOOTSTRAP.

Unique required Rust suite: **146 = 133 inherited + 13 independent**. Required units: **46 = 40 inherited + 6 independent**. Integration/acceptance: **100 = 93 inherited + 7 independent**. Format/Clippy/build/docs, integrity, identity and every mandatory invariant are separate gates, not extra passing tests. Both unit rate and project-wide suite rate >=95%, separately from executed-line >=95%, all on Windows x64 (also overall selected scope). Repeated instrumented executions and retries never increase denominators; failures remain visible. Partial collection has no final failing percentage. Missing required case or unresolved integrity gap forbids PASS even if floors are met.

PASS requires every mandatory requirement and invariant, complete valid metrics, no unresolved required gap. FAIL precedes INCOMPLETE for demonstrated defects. Framework acceptance NOT_EVALUATED; no release authorization. On PASS, report a separately authorized native-diagnostic preparation/launch next step only. On INCOMPLETE, give exact prerequisite and offline resume scope; do not propose proceeding native. On FAIL, deliver dev-owned fix packet after skill availability/identities are verified. Initial checkpoint: no processes owned, no product tests executed, next action integrity review and harness preparation under this plan.
