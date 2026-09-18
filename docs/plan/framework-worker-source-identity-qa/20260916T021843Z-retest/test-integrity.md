# Pre-execution test-integrity assessment

Status: **PASS for bounded execution**. No confirmed result gaming, mock decorator, first-party coverage exclusion, silent skip, or replacement of an operating-system/process boundary was found in the frozen 56-file candidate.

## Frozen intake

- Candidate manifest SHA-256: `3108f976f7d51b734ab995ebf729302ef74a4386ddaafb5561cddbd6f588d65c`.
- Independent live comparison: exact match for all 56 files; no candidate reparse entries.
- Coverage denominator: all 12 `src/*.rs` files; zero first-party exclusions.
- Physical Rust test inventory: 123 `#[test]` attributes. Nine are new in the amendment: six collector cases, one review alias case, and two final runner check cases.

## Integrity review

- No `ignore`, `should_panic`, `mock`, `mockall`, `automock`, `double`, fake/stub framework, or coverage-suppression mechanism was present in executable source/tests.
- `tests/support/mod.rs` uses `#![allow(dead_code)]` for helpers shared through `#[path]` integration-test modules. It does not mark a test skipped and earns no acceptance credit by itself.
- The new source-identity cases create real Windows junctions/symlinks, assert setup success, and use content-, hash-, tag-, target-, membership-, schema-, and staleness-sensitive oracles.
- The deterministic protocol peer remains an external test dependency for offline process/protocol checks. It is not counted as a Codex-native launch.
- `profile_sources::collect_with_policy_using` is private. The public `collect` entry fixes the compiled policy and a no-op callback. The callback seam deterministically retargets a real junction between traversal and the second real operating-system mapping check.
- `runner::execute_with_final_check` is private. Public `run` and `preflight` supply the fixed compiled source check. The callback seam isolates check ordering; public execution performs that check after `spawn_intent`/argument construction and immediately before `OwnedProcess::spawn`.
- The collector verifies the compiled junction policy both before traversal and after collection. The final verification re-observes the live Windows reparse tag and target.
- The compiled exception is fixed to the pinned absolute cache mapping. A disjoint derived profile receives an empty applicable mapping set; an identically relative alias under that other root remains ordinary inventory input and is rejected.

## Independence boundaries

- Qualifying package commands use the original frozen candidate with QA-owned `CARGO_TARGET_DIR` and fixture roots.
- The copied package is reserved for a QA-authored public CLI negative fixture. Its compile-time workspace derivation differs because `CARGO_MANIFEST_DIR` is relocated; that fixture is supplemental and cannot qualify the original package root derivation.
- Installed-profile collection and Codex launch remain prohibited in this campaign.

## Superseded pre-freeze concern

PFR-01 identified the lack of a post-collection mapping observation in a moving preview. The frozen candidate adds both the second operating-system check and a deterministic retarget case. Execution will verify these exact bytes.

## Post-execution integrity and sensitivity result

- The original candidate remained byte-exact to the 56-file frozen manifest in every qualifying receipt and in final readback.
- The original-package test inventory reconciled 123 Cargo tests to 123 physical `#[test]` functions, with 37 unit tests, 86 integration tests, no duplicates, no ignored tests, and no `should_panic` attributes.
- The independently authored disposable-copy matrix passed 3/3 after one retained oracle correction. Mapping/tag/target/member/schema checks execute real collector/inventory validators; review checks execute the review-binding seam; final ordering executes the private runner seam while public entrypoints remain fixed to the compiled check.
- Attempt 35's wrong-mapping assertion was a QA oracle error: its review helper intentionally supplied `|_| Ok(())` to isolate review binding, so it bypassed inventory mapping validation. The failed raw attempt remains retained. Its pre-test helper was recovered into `harness/historical/attempt35-review_v2_cases.rs` and verified as 16,627 bytes, SHA-256 `06975d49d6ed74d672d67c161d3985b45ea94a480cc2752f604e8a1830ad40d5`. The corrected 16,982-byte helper SHA-256 is `ef6ea262a55e91a7558068124e227aff919ae16ce6673ecc2df6e3f41213d5ab`.
- The correction did not waive mapping behavior. Attempt 38 separately rejects a symlink-tag claim for a real junction and rejects a retained inventory whose junction tag is relabeled; the review seam gained requirement-derived omitted/extra physical binding negatives while retaining stale digest/source, schema, and missing-reference negatives.
- Sensitivity attempt 44 used a separately bound disposable mutation that ignored the final-check error. The exact order/no-spawn test failed with outcome 4 instead of 3, establishing that the QA assertion detects this protected-boundary defect. The mutant contributes no product pass or coverage credit.
- Public control attempt 13 is excluded because the pre-correction helper bytes were not bound or retained. The raw failure remains. The independently bound corrected helper then passed fresh public controls in attempt 15.
- No confirmed product result gaming, prohibited mock decorator, coverage suppression, or critical defect was found. No stop trigger fired.
