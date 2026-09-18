---
id: DFF-AUTHORITY-WORKER-EVIDENCE-01
version: 0.1.0
status: specified-for-operator-attested-import
implementation_readiness: specified-not-implemented
updated: 2026-09-15
---

# First acceptance policy: Windows offline worker evidence

[Authority contract](acceptance-authority-v1.md) · [Worker requirements](codex-worker-feasibility-v1.md)

## Scope and fixed inputs

This adapter makes the first authority policy concrete. It covers the **existing independently retested offline candidate**, not future native-readiness changes or native Codex. A changed candidate requires a newly approved inventory/policy binding and matching fresh evidence. Operator-attested import is explicitly selected; raw reports are not cryptographic proof of execution.

Frozen reference corpus: `C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1901023951559Z-retest`. Its external manifest SHA-256 is `c216960995b9fc599b05d19d62704948ce1794b046ad9af4d73e7d0141050e01`; corrected candidate manifest SHA-256 is `3f65ade36cf8186fe711da73f1a2794a17d7fb51e02bf66261e9bba0ce158e39`. These identities select a reference input, not a service acceptance decision. Verify the full manifest before adapting it; never change the historical corpus to fit a parser.

The generated, reviewable inventory at `docs/plan/framework-native-readiness/20260915T1937559109498Z/authority-worker-inventory.proposed.json` fixes32 candidate paths/hashes,8 source paths (lib.rs is zero-executable),50 unique Rust test names and their classification,28 requirement groups, mandatory status and the exact reference artifact paths/hashes. It is not installed policy until the bootstrap operator approves it and the compiled parser build. No CLI option lets the agent replace that inventory during evaluate.

## Submitted normalized envelope

The Rust client imports raw files as immutable bundle artifacts and creates one closed `worker-evidence.json`:

`{schema_version:1, adapter:"worker-offline-qa-v1", candidate_manifest_sha256, platform:"windows-x86_64", normal_receipt, normal_stdout, normal_stderr, coverage_receipt, coverage_stdout, coverage_stderr, llvm_export, format_receipt, clippy_receipt, candidate_files, source_files, independent_records, boundary_records, error_records, operator_judgments}`.

All receipt/output/record values are validated artifact IDs, not filesystem paths or URLs. `candidate_files` is an array `{relative_path,artifact_id}` exactly covering the32 approved package files. `source_files` is the8-file subset with the same artifact IDs. `independent_records` is an array `{case_id,artifact_id}` covering exactly the13 IQ subfixtures listed below. `boundary_records` and `error_records` point to their exact JSON arrays and accompanying raw files. The bundle must include every reference corpus raw fixture/trace/journal/receipt/output and the helper/source bindings from the approved inventory; the adapter cannot omit failed historical attempts referenced for disposition. The full authority manifest identifies hashes/roles for all data; normalized envelope only maps IDs to responsibilities.

Canonical JSON rules and limits are inherited from DFF-AUTHORITY-01. Inputs with duplicate/unknown envelope keys, duplicate IDs, missing records, mismatched paths/hashes or unapproved adapter versions fail. Existing raw records are retained unchanged; the Rust parser has an explicit versioned field schema derived from the frozen reference corpus. Extra raw fields may be retained as opaque evidence but cannot supply policy, alter results, grant roles or bypass required checks. Required typed fields below must parse exactly; no truthy coercion or absent-default-PASS.

## Deterministic checks performed by Rust

### Build/test and coverage

For normal tests, formatting, Clippy and instrumented coverage, read `receipt.json` as bounded JSON; require integer `exit_code=0`, exact approved argv (normalization only for the bound output/evidence root), expected package cwd, matching candidate manifest hash, approved tool digest and matching stdout/stderr hashes. Commands are the already observed `cargo test --locked --offline --all-targets`, `cargo fmt --all -- --check`, `cargo clippy --locked --offline --all-targets -- -D warnings`, and `cargo llvm-cov --locked --offline --all-targets --json --output-path` with the imported LLVM export's bound origin path. No `--ignore-run-fail`, ignored exit or removed flags.

Parse each test stream into lines. For each approved test name require exactly one complete `test NAME ... ok` outcome. Recognize `FAILED`/`ignored` as nonpasses; absent or multiple conflicting outcomes fail completeness. Reject extra test names unless a new inventory was approved. Require the terminal test-result summaries to agree with the selected test inventory and0 failed/ignored. A normal+instrumented execution is two predeclared campaigns, not two sets of passing cases. The six unit cases remain a separately computed metric. Never infer that Rust panic-free compilation proves a case executed.

Parse LLVM coverage JSON with export `type="llvm.coverage.json.export"`, format `version="3.1.0"` observed in the reference corpus, a files array, and summary line counts as nonnegative integers. Match each filename to one approved source path using a policy-bound original package prefix; do not read that path. Seven executable files must appear exactly once; lib.rs may be absent only because the approved source shows declarations only. Every exported first-party file must be represented, including an unexpected added src path (which rejects the stale inventory). Count covered<=count, sum with checked arithmetic, and enforce floor by cross multiplication. Cross-check the covered/count values against that file's retained LLVM summary; do not use the model-authored metrics.json percentage. Zero totals reject. Branch coverage is separately available or NOT_RUN; no branch floor is invented.

The operator attests actual collector execution and completeness of raw-profile artifacts/tool identity. Rust verifies byte/schema/arithmetic/candidate consistency; it does not pretend to rerun LLVM or independently prove machine execution from a document.

### IQ-01: content/protocol variants (six records)

Exact case IDs: IQ-01-valid, IQ-01-wrong, IQ-01-extra, IQ-01-duplicate, IQ-01-missing, IQ-01-policy. Required actual exits:0,4,4,4,4,3 respectively. Terminal reasons: completed, oracle_mismatch for the four result negatives, profile_unqualified for policy denial. Require `deadline_overrun=false`, `fixture_unchanged=true`, `peer_stopped_after=true`, matching candidate hash, and raw stdout/stderr/fixture hashes. Reparse raw journal to require one terminal matching the record, one turn maximum, and no turn for policy denial. For success compare actual final object to the frozen expected.json using the closed result schema; wrong/extra/duplicate/missing must not match. Do not trust `pass` or `contract_trace_matches` alone: inspect raw outbound trace for the base contract's fixed method order/one-turn fields; unsupported method or policy escalation fails. Count the six variants as one group.

### IQ-02: original blocked reply (two records)

Deadline: actual_exit6, terminal timed_out/deadline, <=1.4 seconds. Cancel: actual_exit5, terminal cancelled/user_cancel, <=1.2 seconds. Both: `deadline_overrun=false`, `large_request_sent=true`, unchanged fixture, stopped peer, terminal.tree_stopped=true, exactly initialize/no redispatch in raw trace. Require the large-string-ID raw stimulus bound to the known independent peer source and request deadlines. Do not accept the old exit4 expectation. Interpret measured decimal seconds as bounded decimal rational, not rounded percentage or fabricated wall time.

### IQ-03/IQ-04: process and recovery (four records)

IQ-03-stdin and IQ-03-ctrlc require exit5; IQ-03-kill requires the deliberately terminated supervisor exit1. Every record requires two held process IDs, initial_waits=[258,258], final waits=[0,0] and matching binary/source evidence. A persisted PID alone is insufficient; the operator attests the held-handle observation provenance from the independently reviewed helper.

IQ-04-inspect: run exit0, both inspect exits0, identical returned terminal, unchanged stored evidence, completed state, contiguous sequences1..11 and one turn. Reparse raw journal/inspection JSON, compare returned events and verify exact-once pagination; `identical`/`unchanged` booleans alone do not establish it.

### IQ-05: confidentiality (one record)

IQ-05-private-error requires exit4, terminal failed/protocol_error, fixture unchanged and stopped peer. Independently scan retained product journal/stdout/stderr for the literal synthetic marker `QA_PRIVATE_SENTINEL_7159`; any occurrence fails. The marker's expected presence in the peer source/fixture is not a disclosure. Require no untyped error_category persisted. Preserve original failing candidate's evidence as historical; do not scan it as if produced by the corrected candidate.

### IQ-06 and mandatory loop subfixtures: authenticated human judgment

Source/FFI/test-integrity interpretation cannot be established by counting strings. A closed `operator-judgments.json` artifact requires `{schema_version:1,candidate_manifest_sha256,scope_id:"worker-windows-offline-v1",ffi_ownership_review:"PASS",test_integrity_review:"PASS",mandatory_subfixtures_complete:true,independent_qa_review:"PASS",unresolved_defects:[],reviewed_evidence_manifest_sha256}`. All hashes must match the sealed bundle/reference bindings. The operator attests this exact artifact through the separate identity. Alternative values retain rejection/gap; the client cannot rewrite values during import.

WF-01..20 each requires its approved compiled test outcome **and** this explicit operator judgment of full subfixture execution/provenance, supported by the raw fixtures and source. IQ-06 depends on the judgment and successful IQ-03/RT-01 handle observations. The receipt exposes operator-attested provenance for these judgments; it must not claim that Rust inferred FFI safety or test integrity from source text.

### RT-01: four blocked-pipe variants

Exact variants deadline, cancel, invalid, interrupt; no duplicates. Parse actual observations, not `pass`. Each `initial_waits=[258,258]`, `final_waits=[0,0]`, `job_active=0`, elapsed_ms<1200 and interrupt_ms<400. Deadline/cancel/invalid send reasons respectively deadline/user_cancel/invalid_control and second_reason=pipe_write_pending. Interrupt has send_reason=filled, second_reason=null, interrupt_ms>=170; require raw helper/peer source bound to the known4096-byte full-pipe setup and selected180ms grace. Require each raw invocation receipt exit0 and stdout observation equal to the array entry. Group passes only when all four meet conditions.

### RT-02: twelve typed-error variants

WF-07-91..96 categories respectively `[httpConnectionFailed{httpStatusCode:65535}]`, `[responseStreamDisconnected{httpStatusCode:0}]`, `[responseTooManyFailedAttempts{httpStatusCode:null}]`, `[responseStreamConnectionFailed{}]`, `[activeTurnNotSteerable{turnKind:"compact"}]`, and `["usageLimitExceeded"]`. These are singleton arrays of the actual category values; each terminal reason is provider_failed. WF-07-97..99 require no retained category and protocol_error. WF-04-94 requires no category, rpc_error and retained RPC code[-32010]; WF-04-95/96 require no category and protocol_error. Every case exits4 with stopped peer and unchanged fixture; synthetic marker absent from product journal/stdout/stderr. Reparse raw journals and compare actual approved categories; do not accept the helper's supplied expected_category as policy. Group passes only if all12 meet the fixed table.

## Decision and qualification

All28 groups mandatory for this first policy;50 regression functions and6 unit cases retain distinct denominators. Both floors>=95% apply, with no mandatory failure allowed. No native case is selected for this offline scope. AU-20 tests the policy engine with a separately synthetic native-required policy to prove that offline evidence cannot grant broader scope; it does not pretend the worker native trials ran.

Development must preserve the frozen corpus and create new negative fixture copies under its own evidence root: remove/mismatch artifact; replace source; omit mandatory variant; alter exit6 to4; set pass=true while corrupting actual result; retain marker; forge operator SID; remove a source file from LLVM export; use94.999% counts; duplicate tests/retries; claim native scope with only offline records. Each must reject for the specific expected predicate. These are meaningful input mutations for the Rust parser/authority, not changes to historical evidence.

Operator attestation is an explicit trust input, not a force-accept switch. Build the envelope adapter, validation and policy evaluation in Rust. A preparatory Python inventory script merely binds existing files and cannot install policy, attest or issue acceptance.
