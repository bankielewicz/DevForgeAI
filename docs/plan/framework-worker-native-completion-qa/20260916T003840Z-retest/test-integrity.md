# Frozen corrected candidate test-integrity review

Candidate: 53-file manifest `c27d8ce1742ba7cd0955f0bd18aded8de5f14c898c989654d7298835c3256f9e`.

## Admission result

Static integrity review found no prohibited mock decorator or confirmed result gaming. The later executable-list, full-suite and coverage results all retained the exact frozen candidate identity.

## Identity and reused unchanged evidence

- Independent freeze audit matched 53/53 live files, 53/53 snapshot files and 11 selected input bindings.
- The developer baseline has the same 48 paths, sizes and hashes as the prior failed candidate. Those unchanged bytes retain the prior independent semantic source/test review in `docs/plan/framework-worker-native-completion-qa/20260915T2325371896643Z/test-integrity.md`; no old runtime result or coverage metric is reused.
- Independent manifest comparison found exactly five added test/support files, zero removals and two changed existing files. `Cargo.toml` only registers the new `protocol-edges-peer` test binary. `src/profile_sources.rs` only adds a private `#[cfg(test)]` path module for the new source-inventory tests. No runtime behavior changed.

## Frozen inventory and attributes

- 53 total files; 43 Rust files; 114 physical `#[test]` attributes.
- No `#[ignore]`, `#[should_panic]`, coverage suppression, mock/fake/double dependency, mock-generating attribute, procedural attribute macro or macro definition was found.
- Five conditional attributes are private `#[cfg(test)]` module seams: one native-identity module, two profile-source modules and two review-v2 modules. Every path is static and inspectable.
- Two text locators are benign: the production process comment prohibits retries, and an invalid-input fixture uses the literal scenario `retry`. Neither schedules a retry or changes counting.
- The 114 physical attributes equal both the developer-declared inventory and Cargo's independent executable list. The frozen denominator is 114 unique tests, including 28 library/unit tests; Cargo listed no ignored tests.

## New-test semantic review

- `effective_profile_edges.rs` adds eight public-library tests with distinct positive/negative fixtures for disk/session origins, provider endpoints, session restrictions, feature pagination, hooks, plugins, apps, MCP state and typed error projection. Expected projections and stable error categories are literal. Product constants are used to construct a valid 35-feature fixture, so these tests alone cannot prove the exact list; the separate contract-derived policy oracle remains required.
- `profile_sources_edges.rs` adds eight private unit/filesystem tests for closed inventory tuples, entry/aggregate byte limits, rule/ancestor depth, directory membership/type limits, plugin-control grammar, credential/non-Unicode names, hash/path drift and explicit absence/order. The limits are independently restated from the specification and compared with runtime constants. The tests create real files, including the 8 MiB aggregate and 1,025-member boundary. Ignored errors occur only while preserving already-completed test fixtures in `Drop`; they do not change assertions or product outcomes.
- `protocol_edges.rs` and `protocol_edges_peer.rs` add four test functions covering nine protocol cases. They use a real compiled external child, owned Windows process, pipes, journal, exact outbound trace and tree-stop checks. Server approvals are denied exactly; unsupported/malformed requests cannot grant work; stderr content is omitted with typed size/digest; pagination and rate-limit failures remain bounded/sanitized. The peer is a deterministic offline dependency and earns no live Codex/profile credit.
- `runtime_edges.rs` adds five tests for a disappearing fixture, exclusive evidence writes, compiled source-CLI diagnostics, peer rejection by public preflight review and missing/oversized/digest-mismatched/malformed review bytes. Each checks no successful work, preserved source/fixture bytes and contract-derived exit/error behavior. The profile-source CLI fixture uses the specification-required workspace trial layout; any retained synthetic directory must be indexed separately and cannot be called a native attempt.
- No new test is setup-only or vacuous. No test computes its expected error/result by calling the same product predicate it is assessing. Shared fixture construction does not receive acceptance credit by itself.

## Executed integrity result and proof limits

- Independent execution passed 114/114 unique tests, including all 20 WF parents, F-01/F-02 and all 25 added requirement tests. Rustfmt, Clippy and the QA-owned F-02 byte-canary matrix passed.
- Independent coverage measured 2,967/3,103 lines, 95.61714469867869803416048984853367708669%, with no first-party exclusions. This closes `QA-F-COV-01` as `VERIFIED_FIXED` for the selected offline scope.
- Synthetic protocol/profile checks do not satisfy live NI-T05/NI-T09/NI-T10 or WN-01/WN-02. Native attempts remain zero.
- Framework acceptance remains `NOT_EVALUATED`.

Evidence: `00-freeze-audit/`, `00a-freeze-audit/`, `01-integrity-locators/`, `02-test-list/`, `02a-unit-list/`, `03-full-tests/`, `05-f02-focused/`, `09-full-coverage/`, `10a-coverage-analysis/`, `candidate-bindings.json`, `source-denominator.json` and the frozen source files.
