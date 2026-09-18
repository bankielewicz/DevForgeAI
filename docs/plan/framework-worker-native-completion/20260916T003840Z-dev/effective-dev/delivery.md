# Effective-profile coverage remediation delivery

## Result

**Bounded slice COMPLETE; QA-F-COV-01 remains OPEN pending the root full-source measurement and independent QA.**

Added eight meaningful integration tests in `tests/effective_profile_edges.rs`, SHA-256 `a1c8ff3852e788afba78ec66218d9c282880626e0470dde1260032c04c2b3e5c`. The tests exercise the selected preflight contract's reviewed config-source binding, closed provider/session policy, feature completeness and pagination, disabled hook/plugin/app/MCP state, bounded inventories, redacted projections and typed fail-closed errors.

All eight tests passed on their first behavioral execution. This is an expected characterization result for an already-correct path under a coverage metric finding; no Red was fabricated. No functional defect was reproduced, so no production repair was made. `src/effective_profile.rs` remains byte-identical at SHA-256 `33edc40ceb050be3ce0195de0c5ca7176475b2b0d14d8b730fe0ebe41872302c`. The existing `tests/effective_profile.rs` also remains byte-identical at SHA-256 `90676312ab3b73af79760bedd5337b05af72f85a231dc8bc306c20d4f9119d52`.

## Requirement and case accounting

The declared focused denominator was eight test functions in `case-map.md`:

| Case | Result |
| --- | --- |
| EP-EDGE-01 reviewed config sources and exactly one session layer | PASS |
| EP-EDGE-02 provider endpoints and closed session policy | PASS |
| EP-EDGE-03 complete bounded feature pages and enabled allowlist | PASS |
| EP-EDGE-04 disabled typed hook shapes and redacted projection | PASS |
| EP-EDGE-05 disabled bounded plugin sources and policies | PASS |
| EP-EDGE-06 unique disabled non-callable apps | PASS |
| EP-EDGE-07 inactive empty unique MCP pages | PASS |
| EP-EDGE-08 requirements and public typed-error boundaries | PASS |

Focused required-case pass rate: **8/8 = 100%**. No test is ignored, conditional, `should_panic`, retry-based or coverage-suppressed. The test file contains no mock framework or replacement validator. It calls the public compiled Rust validators with independent fixed expected projections and error categories derived from the selected contracts.

## Executed checks

- `01-focused-characterization`: `cargo test --locked --offline --test effective_profile_edges`; exit 0, 8/8 passed. The recorder detected concurrent package drift limited to sibling-owned `tests/support/profile_sources_edges.rs`; the attempt is preserved and is not the final stable receipt.
- `02-owned-format-check`: direct rustfmt check; exit 1 with formatting-only diffs in the new file. This original result is preserved.
- `03-owned-format-apply`: direct rustfmt application to the owned file; exit 0.
- `04-owned-format-check`: direct rustfmt check; exit 0, candidate unchanged.
- `05-focused-clippy`: `cargo clippy --locked --offline --test effective_profile_edges -- -D warnings`; exit 0, candidate unchanged.
- `06-focused-final`: `cargo test --locked --offline --test effective_profile_edges`; exit 0, 8/8 passed, candidate unchanged during execution. Its package manifest SHA-256 is `14af7c879e7d5735cd31c947d59fc6ae7d2982595008a56db07711cdfa9d6b74` and includes parallel agents' disjoint changes; it is evidence for this focused target, not the root's final frozen candidate.

Every attempt retained exact argv, cwd, executable/recorder hashes, environment override, timestamps, monotonic duration, native exit, raw stdout/stderr hashes and before/after package manifests. The slice-owned target directory is evidence-local and excluded from product identity.

## Scope limits and handoff

No slice coverage collection was run because the root campaign owns the single complete full-source measurement. This slice therefore makes no coverage percentage claim and does not self-close `QA-F-COV-01`. Root must integrate all disjoint tests, freeze the full candidate, and run the complete locked/offline suite, formatting, Clippy and full first-party line coverage. The separately selected independent QA retest alone may mark `QA-F-COV-01` `VERIFIED_FIXED`.

Native Codex/profile trials remain untouched with zero attempts consumed. Framework acceptance is **NOT_EVALUATED**.
