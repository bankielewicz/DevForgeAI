# QA-F-COV-01 developer remediation

**FIX_REPORTED — independent retest pending.** The selected Windows x64 coverage remediation meets the developer thresholds. No product runtime behavior changed. The original independent QA FAIL remains preserved.

## Candidate and contracts

- Candidate: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`.
- Frozen manifest: `candidate-manifest.json`, 53 files, SHA-256 `c27d8ce1742ba7cd0955f0bd18aded8de5f14c898c989654d7298835c3256f9e`; snapshot `candidate-snapshot/`.
- Selected contracts: `docs/specs/framework/runtime/codex-worker-feasibility-v1.md`, `codex-worker-native-readiness-v1.md`, and `codex-worker-preflight-v1.md`, bound unchanged in `inputs-manifest.json`.
- Platform: native Windows x64, PowerShell 7.6.6, Rust/Cargo 1.97.1, cargo-llvm-cov 0.8.4. Package cwd and exact tool hashes/arguments are recorded per command. No Git metadata exists; candidate identity is manifest-bound.

## Change and defect-resolution map

QA-F-COV-01 reported 2,852/3,103 executed lines, 91.91105381888495%. This was a coverage failure, not an established functional defect.

Added 25 meaningful test functions: eight effective-profile, eight source-inventory, four protocol functions containing nine explicit scenarios, and five runner/CLI/review functions. They cover malformed/active profile observations, real filesystem limits, denied requests and pagination, omitted stderr, unavailable quota, fixture/evidence failure, CLI errors and invalid review bytes. Existing assertions remain unchanged.

Only two existing files changed: `Cargo.toml` registers the synthetic test peer; `src/profile_sources.rs` registers a private `cfg(test)` module. Five test/support files were added. `candidate.patch` and `changes.json` retain the exact diff. No runtime function body, lockfile, operational copy or specification changed. Characterization tests initially passing do not constitute a fabricated Red. The two focused setup failures and formatting attempts remain preserved and classified in the slice reports.

## Executed developer results

| Check | Result | Raw evidence |
| --- | --- | --- |
| Locked/offline full build and tests | 114/114 required functions, 100%; 28/28 unit, 86/86 integration; WF 20/20 subset with all subfixtures; F-01/F-02 regressions pass | `full-tests`, exit 0, 160.172 s |
| rustfmt | PASS | `final-fmt`, exit 0 |
| Clippy all targets, warnings denied | PASS | `final-clippy`, exit 0 |
| Documentation tests | Successful discovery; 0 cases present | `doc-tests`, exit 0 |
| Full instrumented suite | 114/114, zero ignored or failed | `full-coverage`, exit 0, 171.234 s |
| First-party executed-line coverage | **2,967/3,103 = 95.61714469867869803416048985%** | `coverage-analysis.json`, `full-coverage/coverage.json` |
| Branch coverage | NOT_RUN; raw branch records were not instrumented | Raw JSON retained |
| Frozen source/input readback | 53/53 candidate files and all 9 selected inputs unchanged | `final-source-readback.json` |

All 12 first-party Rust source files were declared before measurement; 11 contribute executable lines, while `lib.rs` contains module declarations. The line denominator remains 3,103, with no first-party exclusions. Test/support and third-party files are excluded by resolved ownership. Raw coverage JSON SHA-256: `4a41720c591c6239814c33ff297492efa1738b7e2fa594153085806ee9b62b16`; raw profiles remain under `target-coverage/llvm-cov-target/` and are included in the artifact manifest.

`qa-contract.md`, `required-cases.json`, `source-denominator.json` and the slice matrices declare the expected results and denominators. The instrumented repetition does not add passes to the 114-case denominator. `developer-integrity-review.md` records scope and oracle limitations.

## Remaining limits and next action

Only fresh independent QA may mark QA-F-COV-01 `VERIFIED_FIXED`. It must verify this exact candidate, rerun the full offline checks and coverage, retain its own raw evidence, and stop on any valid subthreshold measurement or mandatory failure.

Native trials remain 0/2 with no new attempts. Real Codex source/profile prerequisites remain unresolved; synthetic tests provide no native credit. No configuration/cache/credential/startup/installation changes, source-inventory reparse exception or native model launch occurred. Protected authority is deferred; framework acceptance is **NOT_EVALUATED** and is not established.
