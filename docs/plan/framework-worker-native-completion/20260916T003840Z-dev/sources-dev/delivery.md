# Source-inventory coverage remediation delivery

## Status and scope

**COMPLETE for the selected source-inventory developer-test slice.** The parent QA-F-COV-01 remediation and independent QA retest remain in progress. This slice changed no runtime behavior: it registered one private `cfg(test)` module and added eight requirement-derived unit cases.

Owned candidate paths:

- `devforgeai/experiments/codex-worker-probe/src/profile_sources.rs`: appended private test-module registration; final SHA-256 `8b6633486c6828452aa2aec0f969a82207ad2f6a61ffe360531fd57ea33b42f0`.
- `devforgeai/experiments/codex-worker-probe/tests/support/profile_sources_edges.rs`: new test source; final SHA-256 `8a6ec6e67b0c555706a726fb80ec70b2575b59f947124efd904b8258c2b9a522`.

The original `profile_sources.rs` was `9707a9a944672e1385707fa3c8fd570c22dd85803457b61e6d7833f5c9b75fc2`. The only production-source difference is the private module registration. Runtime functions, public API, original tests, contracts, lockfile, operational configuration, credentials and native-trial state were not changed.

## Requirement coverage

The eight cases in `matrix.md` exercise the closed inventory schema, entry/byte/member/depth limits, invalid source types, closed plugin control grammar, credential-name rejection, file-size/hash drift, absolute-path enforcement, explicit absence and deterministic membership ordering. Expected values use the selected contract's literal limits and error categories. Real temporary Windows directories/files exercise filesystem behavior, including accumulation of eight real 1 MiB sources before rejecting a further byte. Direct private-state construction is limited to the 2,048-entry boundary and introduces no runtime seam.

## Executed results

| Attempt | Result | Interpretation |
| --- | --- | --- |
| `01-characterization` | 7 passed, 1 failed, exit 101 | Preserved test-oracle setup error: the intended scope-mismatch leaf also exceeded 32 levels, so the correct earlier result was `profile_source_limit`. This is not a product Red. |
| `02-oracle-fixture-correction` | 8/8 passed, exit 0 | The shallow outside-root fixture isolates and verifies `profile_source_fixture_scope`. |
| `03-format-check` | exit 1 | Whole-package check found formatting in this new file and independently changing `tests/runtime_edges.rs`; no files changed by this command. |
| `04-rustfmt-owned` | exit 0 | Formatted only the owned new test file. |
| `05-post-format-tests` | 8/8 passed, exit 0 | Post-format focused result. |
| `06-profile-sources-regression` | 15/15 matching filtered tests passed, exit 0 | Includes all six original source-inventory tests, eight new cases and the review-v2 profile-source binding test. |
| `07-owned-format-check` | exit 0 | `rustfmt --check` passed for both owned paths. |
| `08-clippy-lib-tests` | exit 0 | Locked/offline Clippy with warnings denied passed for library and tests. |
| `09-rustfmt-owned-retention` | exit 0 | Scoped formatting after adding retained-fixture handling and real aggregate-byte inputs. |
| `10-final-profile-sources-regression` | 15/15 matching filtered tests passed, exit 0 | Final affected regression; retains 10 source-tree roots, 1,047 files and 9,437,272 fixture bytes. |
| `11-final-owned-format-check` | exit 0 | Final format readback for both owned paths. |
| `12-final-clippy-lib-tests` | exit 0 | Final locked/offline Clippy with warnings denied after the retained-fixture change. |

All commands used native Windows, package cwd, the exact installed Rust tool path, `--locked --offline` for Cargo, and fresh target/fixture paths beneath this evidence slice. Each attempt retains exact argv, environment overrides, monotonic duration, native exit, raw stdout/stderr and before/after package manifests.

The required-case result for this slice is **8/8 = 100%**. A development coverage run was intentionally **NOT_RUN** because the parent assignment reserved the complete final measurement for the integrated candidate. This slice does not claim QA-F-COV-01 closed; development may report it only after the integrated result, and independent QA alone may mark it `VERIFIED_FIXED`.

## Limitations and handoff

- The whole-package format result in attempt 03 is historical and failed before the owned formatting correction; it also contained another concurrently owned new file. The parent must run a fresh integrated formatting check.
- Attempts 01 through 08 used the first fixture helper revision, whose `TempDir` cleanup removed generated source trees after each process. Their receipts and raw console streams remain complete, but their filesystem fixtures are not retained. The corrected helper keeps fixture directories whenever `WF_TEST_EVIDENCE` is set; attempt 10 retains 10 source-tree roots, 1,047 files and 9,437,272 bytes under `sources-dev/fixtures`.
- No native Codex process, operational cache/configuration, credentials, startup setting, installation or protected authority was touched.
- Native WN-01/WN-02 attempts remain unconsumed by this slice.
- Framework acceptance is **NOT_EVALUATED**.

Next safe action: parent integrates all disjoint remediation slices, runs the declared full regression/static/coverage campaign, freezes the corrected candidate, and hands that exact manifest to fresh independent QA.
