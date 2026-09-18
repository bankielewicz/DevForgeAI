# Frozen QA denominators

Bound candidate: 48-entry manifest SHA-256 `809a8beb50f8b57198a963725fd0d2ccd5e586a1243e177284bff3d6dfa471dd`.

## First-party executable source

Coverage includes every executable line reported for every frozen Rust file under `src/`:

1. `src/effective_profile.rs`
2. `src/journal.rs`
3. `src/launch_policy.rs`
4. `src/lib.rs`
5. `src/main.rs`
6. `src/native_identity.rs`
7. `src/oracle.rs`
8. `src/process_windows.rs`
9. `src/profile_sources.rs`
10. `src/protocol.rs`
11. `src/request.rs`
12. `src/runner.rs`

No first-party source file or uncovered behavior is excluded. Test/support binaries, fixtures, the two embedded JSON records, QA helpers and dependency/generated code are outside the contract's first-party executable-source denominator. `lib.rs` remains in scope even if llvm-cov reports zero executable lines. Paths in the raw llvm-cov JSON must be resolved before classification; lexical `src/../tests` paths cannot enter the production denominator.

The line threshold is `executed eligible lines / all eligible executable lines >= 95%` at full precision. Branch coverage is separate and may not substitute for this measurement.

## Rust test inventories

The frozen `cargo test --locked --offline --all-targets -- --list --format terse` receipt lists 89 executable test instances and no ignored entries:

- Required library unit tests: 20/20 denominator. These are the nine native-identity tests, six profile-source inventory tests and five review-v2 tests included through the private `#[cfg(test)]` seams.
- Required full Rust suite: 89/89 denominator, comprising the 20 units plus 69 integration tests. This project-wide rate is reported separately from the unit rate.
- Physical `#[test]` attributes: 89, matching the executable list. Support and main/bin unit targets contain zero additional tests.

Failed, errored, ignored, skipped, blocked and unexecuted required tests are nonpasses. Attempts do not change either denominator.

## Acceptance inventories

- WF regression denominator: 20 parent cases. Every specified subfixture must pass for its one parent to pass. Subfixtures are also itemized but do not inflate the 20.
- Selected native-readiness denominator: 7 groups, exactly NI-T05 and NI-T07 through NI-T12. Synthetic checks cannot pass NI-T11/NI-T12 or live portions of NI-T05/NI-T09/NI-T10.
- Native-trial denominator: 2, WN-01 and WN-02. A blocked, denied, raced, unexecuted or errored trial is not a pass. Each permits one attempt and zero automatic retries.
- Focused repair denominator: 2 findings, F-01 and F-02; both must remain closed under the frozen candidate.

Evidence: `02-test-list/receipt.json`, byte-exact `02-test-list/stdout.bin`, and `02-test-list/stderr.bin`.

