VERDICT: PROCEED_WITH_CHANGES

ASK RESTATED:
Decide whether `qa-handoff.md` is ready as-is to drive an independent offline QA session of the frozen 58-file diagnostic candidate, or which specific corrections must be made to it first.

DO THIS:
1. Correct `qa-handoff.md:14` from "assess that error projection independently where feasible" to an explicit BLOCKED declaration. The `query_failed` projection is not testable under this handoff's own prohibitions: `devforgeai/experiments/codex-worker-probe/src/protocol.rs:89 -> "pub process: &'a mut OwnedProcess,"` is a concrete type, and `src/process_windows.rs:406 -> "pub(crate) fn process_counts(&self) -> Result<(u32, u32)>"` delegates straight to `src/process_windows.rs:386 -> "fn accounting(&self) -> Result<JOBOBJECT_BASIC_ACCOUNTING_INFORMATION>"` calling `QueryInformationJobObject`. There is no trait, no injectable double, and grep finds `QueryFailed` at exactly two sites — `src/diagnostic.rs:76 -> "    QueryFailed,"` and `src/protocol.rs:258 -> "            Err(_) => (None, None, ProcessPredicate::QueryFailed),"` — with zero references anywhere under `tests/`. Write the instruction as: "The `query_failed` predicate and its null/null count projection are NOT_RUN/BLOCKED: no injectable seam exists on `OwnedProcess::accounting`, and adding one would modify the frozen candidate. Record it as BLOCKED with this reason; do not count it as a pass and do not add a seam." This is required by `AGENTS.md:112 -> "Missing measurement is `NOT_RUN` or `BLOCKED`, never an estimated passing percentage."` Left as "where feasible", a QA session can silently mark it satisfied.
2. Resolve the source-modification contradiction inside the handoff. `qa-handoff.md:12` requires "Independently author negative stimuli/oracles"; `qa-handoff.md:7` says "Do not modify this candidate or prior evidence"; `qa-handoff.md:16` requires "Read back final candidate/input hashes before issuing a scoped QA result". Rust integration tests live inside the candidate — 39 of the 58 manifest entries are `tests/` paths. Add an explicit sentence: "Author new cases in a QA-owned working copy of the package at a QA-controlled path; the 58-file candidate at `devforgeai\experiments\codex-worker-probe` and its snapshot must still hash-match `419c98b4...` at the end of the session. Report the working-copy path and its delta from the manifest." Without this, QA either cannot execute step 2 or breaks the step 6 readback.
3. Add the pass-rate denominator rule to `qa-handoff.md:15`. `AGENTS.md:109` requires the denominator to be "all required cases" for "the declared QA suite"; if QA authors extra cases per step 2, the denominator is no longer 133. Write: "Declare the QA suite as the 133 mandatory inherited cases plus every QA-authored case; count each once; QA-authored failures are failures, not optional."
4. Add a coverage-margin instruction to `qa-handoff.md:15`. The delivered figure is 3335/3497; the 95% floor is 3322.15 lines, so the candidate has roughly 12 executed lines of slack. The long-running cases carry that slack — `attempts/21-final-offline/stdout.txt:178 -> "test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 132.77s"`. Write: "Run the identical `--all-targets` campaign; do not filter or time-box out slow process tests. Compare per-file counts against `final-coverage-analysis.json` and report any file whose executed lines regress, because total slack above the floor is about 12 lines."
5. Fix the branch-coverage wording at `qa-handoff.md:15 -> "Keep branch coverage separately reported."` against `delivery.md:59 -> "Branch coverage: **NOT_RUN**; no branch floor was selected."` State the expected disposition: "Report branch coverage as NOT_RUN/NOT_SUPPORTED with the tool version if cargo-llvm-cov produces no Rust branch data; no branch floor is selected; do not synthesize a branch percentage." `AGENTS.md:108` only requires branch reporting "where supported".

DO NOT:
- Do not treat this review as any part of independent offline QA, and do not let it supply a PASS for step 4 or 5 of `qa-handoff.md`.
- Do not add a trait or test seam to `OwnedProcess`/`process_counts` to make `query_failed` testable; that mutates the frozen candidate and is outside the selected scope.
- Do not relax `qa-handoff.md:20` prohibitions, launch native Codex, or prepare the native handoff before independent QA returns PASS.
- Do not rewrite `delivery.md` or the candidate manifest as a consequence of these corrections; only `qa-handoff.md` needs edits.
- Do not regenerate the 58-file manifest or recompute hashes into new files as part of applying these edits.

CLAIM AUDIT:
- AGENTS.md:108/109/49/123 constraint anchors -> CONFIRMED (all four verbatim at the stated lines; `AGENTS.md:108`, `:109`, `:49`, `:123`)
- qa-handoff.md:3, :5, :14, :15, :20 anchors -> CONFIRMED (all verbatim at stated lines)
- native-diagnostic-handoff.md:20 and :22 anchors -> CONFIRMED (verbatim at stated lines)
- delivery.md:58 and :65 anchors -> CONFIRMED (verbatim at stated lines)
- diagnostic-contract.md:9 anchor -> CONFIRMED (verbatim; `other_rpc_failure` fallback matches `src/diagnostic.rs:99 -> "            _ => Self::OtherRpcFailure,"`)
- protocol.rs:235 and :249 anchors -> CONFIRMED (verbatim at stated lines)
- tests/support/diagnostic_cases.rs:90 anchor -> CONFIRMED (verbatim at stated line)
- attempts/21-final-offline/stdout.txt:44 "40 passed" -> CONFIRMED (verbatim at line 44)
- "Required complete suite: 133/133" (delivery.md:57) -> CONFIRMED independently by summing every `test result:` line in `attempts/21-final-offline/stdout.txt` (40+1+1+4+3+8+2+3+6+2+2+1+1+4+3+15+8+4+4+4+12+5 = 133; zero failed, zero ignored)
- "13 src/*.rs files, zero first-party exclusions" (delivery.md:58) -> CONFIRMED (recursive glob of `src/**/*.rs` returns exactly 13 files; no `src/bin/`; the 3 extra `src/` manifest entries are JSON data files, e.g. `candidate-v2-manifest.json:88 -> "path": "src/restrictive-launch-policy.json"`). No first-party Rust is hidden outside the denominator.
- "58-file candidate" -> CONFIRMED (`candidate-v2-manifest.json` contains exactly 58 `"path"` entries, 39 under `tests/`)
- Coverage arithmetic 3335/3497 = 95.367% -> CONFIRMED (computation; clears the floor by ~12 executed lines)
- Contract claim "total_processes and active_processes ... both null if query fails" (diagnostic-contract.md:8) -> CONFIRMED (`src/diagnostic.rs:115-116` declare `Option<u32>` with no `skip_serializing_if`, so serde emits explicit `null`)
- "Diagnostics cannot authorize work / denial preserved" -> CONFIRMED at the guard (`src/protocol.rs:269-272` returns `Err("profile_unqualified")` unchanged after emitting; `src/protocol.rs:240-247` returns the original `check()` result untouched)
- "No native launch permission hidden in the handoff" -> CONFIRMED (`qa-handoff.md:22 -> "Do not launch as part of this QA task."`, consistent with `:20`)
- Assumption "133 is a baseline, not a cap" -> UNVERIFIED as written; the handoff never says so. `qa-handoff.md:12` implies additions are expected but `:15` names a fixed 133 denominator. Fix per DO THIS 3 rather than assuming.
- Assumption "private seam tests + public wiring adequately assess offline behavior without native launch" -> PARTIALLY CONTRADICTED: it does not hold for the accounting-query failure branch, which has no seam at all (see DO THIS 1). It holds for source_review and RPC branches, where `tests/support/diagnostic_cases.rs:107 -> "assert_eq!(session.dispatch(&native), Err(\"profile_unqualified\".into()));"` exercises the public dispatch path, not only the private seam.
- Assumption "hash-bound records represent the candidate that was tested" -> UNVERIFIED (read-only; I did not compute SHA256 of any file, and the briefing's own fresh-readback claim is self-reported)
- ATTEMPTS narrative (attempt-001 ConnectionRefused, attempts 01/02/03/05/06/16/17 pattern) -> UNVERIFIED (not read; not load-bearing for handoff readiness, and a transport failure is not a handoff defect)

RISKS:
1. `query_failed` silently scored as a pass - triggered by: a QA session reading "where feasible" as discretionary and omitting it from the required-case ledger - detect early by: the QA report containing no BLOCKED entry for `process_accounting`/`query_failed` while claiming full diagnostic-branch coverage.
2. Candidate hash readback fails at the end of QA - triggered by: QA authoring new tests directly under `devforgeai\experiments\codex-worker-probe\tests\` per step 2 - detect early by: a pre-test hash snapshot of the 58 files taken before the first `cargo test`, re-checked immediately after the first authored case.
3. Coverage falls below 95% on the QA re-run - triggered by: dropping, filtering, or timing out the 132.77s and 18.27s process test binaries - detect early by: comparing the QA run's per-binary test counts to 133 before reading the coverage number.
4. Denominator inflation/deflation dispute under AGENTS.md:109 - triggered by: QA counting only the inherited 133 while executing more cases, or counting instrumented and normal campaigns twice - detect early by: requiring the QA report to print the declared case list and its size before results.
5. Contradiction between "no first-party exclusions" and any QA-authored helper placed under `src/` - triggered by: QA adding a seam module to `src/` to reach `query_failed` - detect early by: `src/**/*.rs` file count moving off 13.

COULD NOT VERIFY:
- Actual SHA256 of the 58 candidate files and the manifest - would need: execution of a hashing command, which is outside read-only tooling.
- Whether `final-coverage-analysis.json` per-file counts sum to 3335/3497 - would need: a read of the large coverage artifacts, deliberately deferred under the ~20-read budget.
- Whether `query_failed` is among the 162 uncovered lines - would need: the per-line coverage record for `src/protocol.rs`.
- attempt-001 `execution.json`/`result.json` contents - would need: reads under `advisor-runs`, excluded as self-echo per the briefing's own instruction and not load-bearing.

FLIP CONDITIONS:
- If a test double or `cfg(test)` seam for `OwnedProcess::accounting` exists that my grep for `QueryFailed`/`process_counts` missed, DO THIS 1 collapses to "require the case outright" and the verdict weakens toward PROCEED.
- If `qa-handoff.md` elsewhere (or `review-notes.md`) already designates a QA-owned working-copy path for authored tests, DO THIS 2 is unnecessary.
- If the QA skill's own contract already fixes the declared-denominator rule for added cases, DO THIS 3 is redundant.
- If any predicate in `src/protocol.rs` or the config validator is shown to have changed relative to the 56-file baseline manifest `3108f976...`, this becomes STOP_REDIRECT: the handoff would be freezing a candidate that violates `native-diagnostic-handoff.md:20`.