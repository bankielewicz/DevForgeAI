# FAIL — restrictive native worker preflight qualification

Independent finding: **QA-F-COV-01**, high-severity mandatory metric failure.

The selected Rust changes are implemented, but the frozen candidate failed independent QA's mandatory executed-line coverage requirement: **2,852 / 3,103 = 91.91105381888495%**, below 95%. The complete collector succeeded; this is a valid measurement, not a tooling failure. The required stop condition was applied. No further product tests, native preflight or model trials were executed after that decision. No repair or metric-improving rerun was attempted.

## Candidate and scope

- Candidate: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`.
- Frozen package: 48 files; [candidate manifest](candidate-manifest.json) SHA-256 `809a8beb50f8b57198a963725fd0d2ccd5e586a1243e177284bff3d6dfa471dd`. [Snapshot](candidate-snapshot/) is retained separately. No Git metadata exists.
- Selected inputs: [manifest](inputs-manifest.json), SHA-256 `3fafe784e180b37cabaf8e276c8f324ea464fd568dcfa9a05688a55db9e88288`.
- Contracts: DFF-WORKER-FEAS-01 v1.0.0, DFF-WORKER-NATIVE-01 v0.1.0, and new DFF-WORKER-PREFLIGHT-01 v0.1.0. The compiled-Rust enforcement design remains the separate authority boundary.
- Scope: implement NI-T05 and NI-T07–T12 prerequisites, independent offline qualification, and the already-selected WN-01/WN-02 only if prerequisites pass. Protected acceptance authority implementation/provisioning remains deferred.
- Platform: native Windows x64, local C: filesystem, PowerShell 7.6.6, Rust/Cargo 1.97.1, cargo-llvm-cov 0.8.4. The filesystem type was not independently established; the volume query was denied. Package has no optional feature combinations. Linux and native tray UI are outside this selected experiment.

## Implemented behavior

1. Compiled, digest-bound launch policy supplies the exact shell-free argument vector. It disables 35 selected features, known plugins/MCP entries/apps, web search and alternate provider/login selection; it fixes read-only sandbox and never approvals. Callers cannot supply arbitrary argv or configuration.
2. Compiled `profile-sources` inventory covers fixed workspace/user/system/ancestor/plugin control inputs, complete file/membership/absence bindings, bounded sizes and strict reparse rejection. It records hashes, not credential contents.
3. Closed review v2 binds policy, source inventory and every file source. `preflight` can inspect false findings without granting work; `run` still requires all four operator findings true.
4. Compiled preflight inspects effective configuration, requirements, features, hooks, plugins, installed apps, MCP state, Pro account and exact model/effort before any thread/turn. Unknown/active state, protocol work events and unexpected descendants reject. Sources and pinned identity are rechecked; runtime inspection repeats before work.
5. Distinct journal/inspection semantics prevent `preflight_checked` from being treated as a completed model turn. Detached worker creation retains atomic Job Object ownership and explicit stdio handles; real lifecycle regressions ran.

The package has 12 added files and nine changed files, with no removals; see [changes](changes.json). Original tests, Cargo.lock, operational copies and historical evidence were preserved. Focused Red/Green records and setup failures remain in their original attempt directories.

## Independent QA results

Full findings, requirements mapping and stop handoff are in the [independent QA report](../../framework-worker-native-completion-qa/20260915T2325371896643Z/qa-report.md). Root independently checked the raw coverage JSON, test summary, five command receipts and ten stream hashes in [retained-evidence readback](qa-evidence-readback.json), with zero mismatches.

| Measure | Observed result |
| --- | --- |
| Library unit functions | 20/20 passed — 100% |
| All Rust test functions | 89/89 passed — 100%; zero failed/ignored |
| Mandatory WF regression parents | 20/20 passed, including required subfixtures |
| F-01/F-02 suite regressions | Passed; additional QA-authored F-02 probe was NOT_RUN after the stop |
| Launch-policy independent oracle | Passed: exact 116 arguments, 56 overrides, 35 required disables |
| Formatting / Clippy | Passed, native exit 0 |
| Executed-line coverage | **2,852/3,103 — 91.91105381888495%, FAIL** |
| Branch coverage | NOT_MEASURED; JSON contains no instrumented branches, not a 0% or 100% result |
| Native trials | 0/2 passed — 0%; both NOT_RUN, zero attempts consumed |

Coverage includes all first-party executable Rust source under `src/`, with no production exclusions. Eleven files contain reported executable lines; `lib.rs` stays in scope with no reported executable lines. Tests/support/fixtures, declarative JSON and dependencies are outside this executable-source definition. [Raw coverage JSON](../../framework-worker-native-completion-qa/20260915T2325371896643Z/08a-coverage/coverage.json) SHA-256: `271212ab24ab2939f4a595103c9978c2d451dc826fecfe341da06d5d4c3dc3b8`.

Largest absolute gaps: effective_profile.rs 485/573, profile_sources.rs 420/462, protocol.rs 594/627, runner.rs 145/178. Passing assertions do not demonstrate the unexecuted paths. This is a qualification failure, not proof that each uncovered path is defective.

Commands ran from the package directory with QA-owned target/fixture directories: `cargo test --locked --offline --all-targets` (157.656 s), `cargo fmt --all -- --check` (0.234 s), `cargo clippy --locked --offline --all-targets -- -D warnings` (5.516 s), and `cargo llvm-cov --locked --offline --all-targets --json --output-path <retained coverage.json>` (169.578 s). Exact executable paths, argv arrays, environment overrides, timing, native exits and raw streams are in the linked QA receipts. Compilation was exercised by these commands; no separate release-build claim is made.

## Readiness and blockers

Observed functional case results are separate from overall qualification:

- Full readiness: seven offline-resolvable groups have passing functional evidence (NI-T01–T04, NI-T06–T08); five groups remain BLOCKED/NOT_RUN. Thus 7/12 = 58.333333333333336% functional completion, with no overall readiness pass.
- Changed selected scope: NI-T07/T08 have passing functional evidence; NI-T05/T09/T10/T11/T12 remain nonpasses. Thus 2/7 = 28.571428571428573%. Mixed groups are not fractionally counted as passes.
- NI-T05 requires a positive final identity recheck at actual pinned Codex launch; NI-T09/T10 require real effective-profile/account/model/sandbox evidence. Synthetic peers cannot supply those results.
- Before the freeze, compiled source collection exited 3 on `C:\Users\bryan\.codex\plugins\cache\openai-bundled\chrome\latest`. That strict reparse denial is expected behavior. It is evidence from the evolving development candidate; final-candidate live source collection was NOT_RUN because independent QA stopped on coverage.
- WN-01/WN-02 were not launched. Both the mandatory quality stop and unresolved source/profile prerequisites prevent proceeding. See the [native prerequisite handoff](native-prerequisite.md).

## Integrity, preservation and limits

Independent inspection found no confirmed result gaming, ignored-test inflation or first-party coverage suppression. Compiled synthetic peers exercise real Windows pipes/jobs, but establish only offline protocol behavior. Existing privacy and process regressions passed; any planned independent probe not executed before the stop remains NOT_RUN.

Fresh final qualification commands have separate byte-exact streams and native metadata. Earlier development evidence includes two incompletely captured setup/formatting invocations, and the first QA coverage recorder attempt failed before launching Cargo. These are preserved separately; they are not passing tests, behavioral Red results or retries of a failed product measurement. See [provenance and limitations](provenance-and-limitations.md) and the QA attempt records. The successful complete coverage collection was not rerun after its below-threshold result.

Upstream documentation informed the policy, but its raw downloaded body/digest was not retained. Pinned local schemas/feature output are bound; actual installed integration inactivity remains unproven. Missing provider fields are not positive proof of internal endpoint selection.

[Final source readback](post-qa-source-readback.json), [input readback](post-qa-inputs-readback.json), [external evidence bindings](external-evidence-bindings.json), and [evidence manifest](evidence-manifest.json) bind this delivery. [Remediation/retest handoff](handoff.md) defines the next separate development assignment.

**Framework acceptance: NOT_EVALUATED; not established.** No qualified protected compiled-Rust authority issued a decision. This report, operator profile review and passing tests cannot substitute for such a decision.
