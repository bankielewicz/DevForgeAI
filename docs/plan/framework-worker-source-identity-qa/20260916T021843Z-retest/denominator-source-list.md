# Declared denominators and source list (pre-freeze)

## Required-case accounting

- SI amendment: 10 groups.
- WF regression: 20 groups.
- Selected offline portions of NI-T01..NI-T10: 10 traceability groups. NI-T05's actual prelaunch observation and the actual effective-profile/runtime portions of NI-T07..NI-T10 remain outside this campaign.
- F-01/F-02: 2 groups.
- Overall selected offline requirement-group accounting: 42 source-qualified groups. This is a transparent overlapping traceability view, not an additive Rust-test count and not a claim of full NI readiness; the developer's base denominator remains 30 WF+SI groups with NI/F supplemental coverage inside SI-T09.
- WN native: 2 groups, separately `BLOCKED/NOT_RUN`, zero attempts authorized in this run.

These are source-qualified requirement groups. An executable test can support multiple requirements, but each unique Rust test function is counted only once in the test-rate denominators. Parameter variants are conjunctive assertions within their parent requirement and do not inflate passes. Retries and coverage repetitions are attempts, never additional cases.

At freeze QA will publish:

- the unique all-target Rust function denominator from Cargo listing plus physical-source reconciliation;
- the unique library/unit function denominator;
- ignored/skipped inventory (required occurrences are nonpasses);
- mappings from every SI/WF/NI/F group and subfixture to one or more frozen executable tests or QA-owned controls.

Current preparation observed 117 physical `#[test]` attributes, but this count is explicitly nonqualifying because development is ongoing. The earlier 114-test QA result is stale for this candidate.

## First-party executed-line source denominator

Every executable line in these 12 files is eligible:

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

There are no first-party source exclusions. If LLVM omits `src/lib.rs` because it contains only module declarations, QA will inspect it and record 0/0 rather than silently omit it. Embedded `src/native-executable-identity.json`, `src/plugin-source-identity.json`, and `src/restrictive-launch-policy.json` are candidate-bound policy/data inputs with hashes and behavioral assertions; they are not executable-line files. Tests, test support binaries, fixture data, Cargo-generated output, and third-party dependencies are outside the source-line denominator by ownership, not by coverage outcome.

The coverage completion condition is one usable LLVM JSON result from the complete declared all-target collection, reconciled against all 12 files. A crashed/incomplete collector yields unavailable coverage, never an estimated percentage. A valid final value below 95% triggers immediate stop and is not rerun to seek a better result.

## Final observed denominators

- Cargo and physical-source reconciliation found 123 unique all-target tests and 123 physical `#[test]` attributes, with no duplicates, ignored tests, or `should_panic` attributes.
- The library/unit subset contains 37 unique required tests; integration targets contain 86 tests.
- The one original-package full campaign passed 123/123; the library/unit portion passed 37/37. Focused, coverage, disposable-copy, and sensitivity attempts do not increase these denominators.
- LLVM reported 3,191 executed of 3,339 executable first-party lines across all 12 declared source files: 95.56753519017669961066%. `src/lib.rs` is explicitly 0/0. There are zero first-party exclusions.
- The selected offline traceability denominator is 42/42 PASS: SI 10, WF 20, offline portions of NI 10, and F 2. These groups overlap executable tests and are not an additive test-rate metric.
- WN-01/WN-02 remain a separate 0/2 BLOCKED/NOT_RUN native denominator.

## Candidate and input identity at freeze

The frozen manifest will include `Cargo.toml`, `Cargo.lock`, `README.md`, every `src/` file, every `tests/` Rust/helper/fixture file, byte size, SHA-256, and file kind. `target/` is excluded as generated output. Reparse points inside the candidate are recorded and treated as an identity/safety blocker unless explicitly expected by the selected contract.

Specification hashes, the development handoff/manifest, the inspected recorder, and the prior baseline report will be bound separately. Development and prior QA evidence remain context; none contributes a pass to this run.
