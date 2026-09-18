# Independent QA plan — reviewed plugin-cache junction identity

## Identity, mode and present state

- Invocation intent: `retest` of the bounded source-identity amendment, with full selected offline regression.
- Planning status: `READY`; the frozen candidate is bound, with product execution held until an explicit GO after developer full-suite and coverage completion.
- Execution status: `NOT_STARTED`.
- Product QA verdict: not assigned while the required freeze is pending.
- Project: `C:\Projects\DevForgeAI` on native Windows x64, PowerShell, Windows-resident NTFS workspace.
- Candidate: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`.
- Evidence root: `C:\Projects\DevForgeAI\docs\plan\framework-worker-source-identity-qa\20260916T021843Z-retest`.
- Selected specifications: `docs/specs/framework/runtime/codex-worker-feasibility-v1.md`, `codex-worker-native-readiness-v1.md`, `codex-worker-preflight-v1.md`, and `codex-worker-source-identity-v1.md`.
- Applicable rules: root `AGENTS.md`, `docs/prompt/qa.md`, and the operational `.agents/skills/qa` package.
- Candidate Git identity: unavailable because the workspace is not a Git repository. A fresh scoped file manifest and SHA-256 binding will identify the frozen candidate.
- Freeze binding: 56 candidate files exactly match `candidate-manifest.json` SHA-256 `3108f976f7d51b734ab995ebf729302ef74a4386ddaafb5561cddbd6f588d65c`; no candidate reparse entry was found. Exact specification/input/source-denominator hashes are in `freeze-bindings.json`.

## Selected scope and boundaries

The selected offline scope is Windows x64, package default configuration, and no optional features. It contains:

1. SI-T01 through SI-T10, with every listed subfixture conjunctive.
2. WF-01 through WF-20 and every inherited subfixture.
3. The selected offline portions of NI-T01 through NI-T10 under the finalized preflight contract. This does not complete full NI readiness: NI-T05 still requires a real immediately-prelaunch Codex observation, and NI-T07 through NI-T10 retain actual effective-profile/runtime prerequisites outside this campaign.
4. F-01 blocked-write/cancellation/process-tree and F-02 typed-error/privacy regressions.
5. The complete frozen Rust test inventory, build, rustfmt, Clippy, documentation tests, and complete first-party executed-line coverage.
6. Independent QA negative fixtures for mapping scope, source/tag/target/member drift, schema/digest/review freshness, and final-boundary no-spawn ordering.

Excluded from execution:

- WN-01 and WN-02 remain a separate native denominator at `0/2 BLOCKED`; this run must not start Codex or consume either one-shot attempt.
- Installed-profile `profile-sources` collection is prohibited until this QA run passes. The installed cache/configuration is read back only with nonmutating metadata/hash inspection needed for SI-T10.
- Authority implementation, provisioning, protected acceptance, installation, deployment, startup changes, cache repair/refresh, configuration edits, dependency installation, network access, and Linux qualification are outside scope.
- Historical evidence is context only. The prior 114-test, 2,967/3,103 PASS is bound to older bytes and cannot qualify this candidate.

## Freeze entry conditions

The freeze is satisfied. Product execution remains held until the parent gives the separate explicit GO. QA freeze actions are:

1. Re-read the four specification files and applicable instructions. Completed for the frozen input hashes.
2. Independently compare the byte-exact 56-file candidate against the development manifest, excluding only Cargo output directories. Completed with `EXACT_MATCH_56`.
3. Bind specification, development handoff, recorder, and baseline evidence hashes without treating development results as QA outcomes. Completed in `freeze-bindings.json` for current inputs.
4. Copy the already inspected `record.py` into this QA root. Completed; its `ROOT = Path(__file__).resolve().parent` places every future command attempt under this QA root.
5. Create an immutable QA snapshot or isolated harness copy under this root with a manifest tying every copied byte to the frozen candidate. QA-only test additions will be separately manifested and will never be copied back into product source/tests.
6. Recheck that no unowned build/test process or unexpected reparse point overlaps the candidate, QA root, or planned target directories.

Candidate or specification drift after freeze blocks affected checks. QA will preserve the original manifest and will not silently rebind.

## Integrity inspection before tests

Inspect every frozen first-party Rust source/test/helper and every QA helper for mock-generating attributes, aliases, wrappers, skipped/ignored cases, vacuous assertions, swallowed failures, fake integration claims, retries, coverage suppression, omitted source, denominator manipulation, and hardcoded PASS output. Text search is only a locator; imports, attributes, helper calls, private seams, and actual assertions will be read.

The private source-collector seam is acceptable only for real Windows mapping behavior under synthetic owned roots. It cannot establish installed-profile or native-Codex behavior. The private runner callback is acceptable only to deterministically stimulate ordering at the real final boundary; public `run` and `preflight` must remain wired to the fixed compiled check with no caller-supplied callback or mapping. Any confirmed mock decorator or result gaming triggers immediate whole-run STOP/FAIL.

## Planned execution order

Every command runs through the copied recorder with exact argv, cwd, native exit code, duration, raw stdout/stderr, executable hash, and candidate before/after manifests.

1. Environment/tool discovery: OS/architecture, PowerShell, `rustc`, `cargo`, `rustfmt`, `clippy`, `cargo llvm-cov`, and resolved executable paths. No install attempt.
2. Integrity and source/test inventory publication/readback.
3. Build all binaries first with `cargo build --locked --offline --bins`, using a QA-owned absolute `CARGO_TARGET_DIR`. This is required before SI-T08 unit execution because the test uses `target/debug/protocol-peer.exe`.
4. Enumerate the complete all-target suite and the library/unit subset with Cargo's test lister. Reconcile Cargo names against physical `#[test]` functions and the development mapping; freeze the unique denominators before execution.
5. Run focused SI/private-seam and QA-owned negative controls only after the peer build and harness integrity review.
6. Run one `cargo test --locked --offline --all-targets` campaign against the frozen candidate and inspect retained real fixture outcomes.
7. Run the independent public-entry controls and the QA-owned disposable-copy source-identity matrix.
8. Run `cargo fmt --all -- --check`.
9. Run `cargo clippy --locked --offline --all-targets -- -D warnings`.
10. Run documentation-test discovery/execution using the actual package command established after freeze.
11. Run one complete `cargo llvm-cov --locked --offline --all-targets --json --output-path C:\Projects\DevForgeAI\docs\plan\framework-worker-source-identity-qa\20260916T021843Z-retest\coverage\coverage.json` collection over the full declared source denominator. Do not repeat a valid subthreshold result.
12. Analyze raw LLVM JSON independently, report executed/eligible lines per source file and in aggregate, and keep branch coverage separate.
13. Read back frozen candidate, specifications, and installed mapping metadata. Candidate/specification byte drift is a safety blocker; installed-profile collection is not attempted.
14. Finalize report/fix/checkpoint files, then create and read back the external artifact index exactly once after all referenced report bytes are final.

## Metrics and stop policy

- Amendment group denominator: 10 (`SI-T01..SI-T10`).
- Regression group denominator: 32 (`WF-01..WF-20`, the selected offline portions of `NI-T01..NI-T10`, `F-01`, `F-02`). These are traced separately even where one executable observation satisfies overlapping requirements.
- Overall selected offline contract-group accounting: 42 source-qualified groups; subfixtures are conjunctive and never extra passes. This transparent traceability view overlaps the developer's 30-group WF+SI denominator and does not inflate the unique Rust test denominator or claim full NI readiness.
- Native denominator: 2 (`WN-01`, `WN-02`), both `BLOCKED/NOT_RUN`, separate from the selected offline verdict.
- Required unit-test denominator: every unique frozen library/unit test from Cargo and source reconciliation. Failed, errored, ignored, skipped, blocked, or unexecuted required unit tests are nonpasses.
- Project suite denominator: every unique frozen `--all-targets` Rust test. Subsets and coverage repetitions are not additional cases.
- Coverage denominator: every executable line in all 12 frozen `src/*.rs` files. `src/lib.rs` may be 0/0 if LLVM reports no executable lines. There are no first-party source exclusions.
- Mandatory floors: executed-line coverage `>=95%`, required unit pass rate `>=95%`, and project required-suite pass rate `>=95%`, all at full precision. Mandatory and security failures cannot be waived by percentages.

A confirmed mock decorator/result gaming, valid complete subthreshold metric, or critical authorization/security/data-loss defect immediately stops all further tests/builds/coverage. A normal mandatory defect establishes eventual FAIL while safe independent checks continue. A harness or prerequisite gap blocks only dependents unless identity or containment cannot be established. WN-01/WN-02 remain unlaunched regardless of offline results.

## Evidence map and completion

Planned files under this root: `qa-plan.md`, `requirements-matrix.md`, `denominator-source-list.md`, `independent-negative-fixture-plan.md`, freeze-time input/candidate manifests, copied `record.py`, integrity records, per-command attempt directories, raw coverage, case results, source readback, `qa-report.md`, conditional `qa-fix.md`, `checkpoint.json`, and final `artifact-index.json`.

PASS is available only if all selected offline obligations pass, all integrity questions are resolved, the complete metrics meet their floors, and frozen source/specification readback is unchanged. The installed-profile and native `0/2` state will remain explicitly separate. Protected framework acceptance remains `NOT_EVALUATED` unless a separately qualified compiled-Rust authority issues a decision.
