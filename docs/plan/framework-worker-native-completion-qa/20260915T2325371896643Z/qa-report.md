# Independent QA report — FAIL

## Identity and scope

- **Verdict:** **FAIL**. The complete first-party executed-line measurement is `2,852/3,103 = 91.91105381888495004834031582%`, below the mandatory `95%` floor.
- **Execution:** `STOPPED` at `QA-F-COV-01` immediately after the first complete coverage collection and independent denominator analysis. No metric-improving rerun was made.
- **Candidate:** `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`, frozen 48-file manifest `809a8beb50f8b57198a963725fd0d2ccd5e586a1243e177284bff3d6dfa471dd` at `docs/plan/framework-worker-native-completion/20260915T2306060954875Z/candidate-manifest.json`. The recorder's separately defined canonical package inventory remained `613ba90f571065865a797e57b4e0ddf7e63716cc0ffbec84c1ccab4a8568163a` before and after every recorded command.
- **Specifications:** `codex-worker-feasibility-v1.md` `7cb5b0cb87e515bb4d59235b615922ab4ea07ef607b8111dde6cc73c8f101b23`; `codex-worker-native-readiness-v1.md` `c3c0673cbf95ae7aa056d9fd0009ce89947309b943013fd7838438d6ee66b06d`; `codex-worker-preflight-v1.md` `6e781f23f221d1033896716512e9162579653b529d107e0040d49c499574afd1`; `AGENTS.md` `d47868fef2b87df0b2c065cfe235cfe9f12fcf9eeffa7af1f0973d7d21916fa7`.
- **Selected scope:** Windows x64; NI-T05 and NI-T07 through NI-T12; WF-01 through WF-20 and all required subfixtures; F-01 and F-02 regressions; full tests, format, Clippy, line coverage and test-integrity review. Protected acceptance authority was expressly deferred.
- **Environment:** Microsoft Windows `10.0.26200`, x64; PowerShell `7.6.6`; Cargo/rustc `1.97.1` (`x86_64-pc-windows-msvc`, LLVM `22.1.6`); rustfmt `1.9.0-stable`; Clippy `0.1.97`; cargo-llvm-cov `0.8.4`; Python `3.10.11`; working tree `C:\Projects\DevForgeAI`. Git metadata is absent. Filesystem type was not established because the nonessential volume query was denied.
- **Authority result:** framework acceptance is **NOT_EVALUATED** and is not established.

## Findings

### QA-F-COV-01 — High — mandatory line coverage is below 95%

- **Requirement:** repository `AGENTS.md`, “Mandatory framework quality thresholds”; base feasibility quality requirement; the frozen denominator in `denominators.md`.
- **Location:** all first-party executable Rust under `src/`; the largest measured gaps are `effective_profile.rs` (`485/573`), `runner.rs` (`145/178`), `profile_sources.rs` (`420/462`) and `main.rs` (`122/132`).
- **Reproduction:** from the package directory, with a fresh QA target and fixture directory, run the exact argv in `08a-coverage/receipt.json`: `cargo llvm-cov --locked --offline --all-targets --json --output-path <raw-json>`.
- **Expected:** at least `95%` executed-line coverage over every first-party executable source line, with no production exclusions.
- **Actual:** collector exit `0`, all embedded tests passed, but independent path-resolved analysis found `2,852/3,103 = 91.91105381888495004834031582%`. At the current denominator, at least `2,948` lines must be covered; the result is short by `96` covered lines.
- **Impact:** the frozen candidate fails a mandatory quality gate. Passing tests and static checks cannot waive it. This is a `METRIC_FAILURE`; no functional product root cause is inferred.
- **Evidence:** `08a-coverage/coverage.json` SHA-256 `271212ab24ab2939f4a595103c9978c2d451dc826fecfe341da06d5d4c3dc3b8`; `08a-coverage/receipt.json`; `09-coverage-analysis/stdout.bin`; 160 retained `.profraw` files totaling `3,158,960` bytes, individually hashed in the analysis output.

No critical security, authority, data-loss or result-gaming defect was confirmed before the metric stop.

## Acceptance traceability

| Criterion | Actual result | Status | Evidence |
| --- | --- | --- | --- |
| NI-T05 | Synthetic final-identity drift/recheck behavior passed. The required final recheck immediately before a real Codex launch was not reached. | BLOCKED | `03-full-tests/`; stop `QA-F-COV-01` |
| NI-T07 | Exact native launch policy independently matched 116 argv entries, 56 config overrides and 35 unique required feature disables; policy digest `1dbc48c4a3627f7c5fc7a996935ec507426e4cd90adac058eb81100ac9b526b5`. | PASS (offline) | `04-policy-oracle/` |
| NI-T08 | Review-v2, inventory binding, source limits and reparse fail-closed cases passed in the frozen suite. | PASS (offline) | `03-full-tests/` |
| NI-T09 | Compiled synthetic preflight order, pagination, inactive hooks/plugins/apps/MCP and forbidden-work cases passed. Installed-profile live preflight was not reached. | BLOCKED | `03-full-tests/`; stop `QA-F-COV-01` |
| NI-T10 | Compiled synthetic account/model/effort/rate-limit/profile conflicts passed, including explicit unmeasured-rate handling. Live effective-profile observation was not reached. | BLOCKED | `03-full-tests/`; stop `QA-F-COV-01` |
| NI-T11 / WN-01 | No native Codex completion attempt was launched. | NOT_RUN | attempt count `0`; `checkpoint.json` |
| NI-T12 / WN-02 | No native cancellation attempt was launched. | NOT_RUN | attempt count `0`; `checkpoint.json` |
| WF-01..20 | All 20 parent cases and their required subfixtures passed; any subfixture assertion fails its parent. | PASS | `03-full-tests/stdout.bin`; retained fixtures |
| F-01 | Full-pipe deadline/cancellation and verified tree-stop regression tests passed with real Windows processes. | PASS | `03-full-tests/stdout.bin` |
| F-02 | The compiled 19-canary regression function passed and asserted exit/error/journal/stdout redaction. The additional QA-owned focused harness was authored but not run after the terminal metric stop. | PASS (regression); independent supplement NOT_RUN | `03-full-tests/stdout.bin`; `focused_f02.py` |

The selected remaining-readiness rate is `2/7 = 28.57142857142857%`; blocked and unexecuted groups are not passes. Current overall readiness is `7/12 = 58.33333333333333%`: NI-T01 through NI-T04 and NI-T06 remain supported by the fresh regression, and NI-T07/NI-T08 are newly supported offline. This readiness count does not override `QA-F-COV-01`.

## Metrics and command results

| Windows x64 metric/check | Numerator | Denominator | Exact result | Required | Outcome |
| --- | ---: | ---: | ---: | ---: | --- |
| Frozen full Rust suite | 89 | 89 | 100% | >=95% | PASS |
| Library unit tests | 20 | 20 | 100% | >=95% | PASS |
| WF parents | 20 | 20 | 100% | >=95% | PASS |
| F-01/F-02 repair groups | 2 | 2 | 100% | both mandatory | PASS |
| Selected NI groups | 2 | 7 | 28.57142857142857% | >=95% and mandatory cases | NOT MET / incomplete live evidence |
| Native trials | 0 | 2 | 0% | both required | NOT_RUN |
| First-party line coverage | 2,852 | 3,103 | 91.91105381888495004834031582% | >=95% | **FAIL** |
| Branch coverage | 0 reported | 0 reported | unavailable | separate report | NOT_RUN |

Per-file line results:

| File | Covered / executable | Exact percentage |
| --- | ---: | ---: |
| `effective_profile.rs` | 485/573 | 84.64223385689354% |
| `journal.rs` | 262/266 | 98.49624060150376% |
| `launch_policy.rs` | 21/23 | 91.30434782608696% |
| `lib.rs` | 0/0 | no executable lines reported |
| `main.rs` | 122/132 | 92.42424242424242% |
| `native_identity.rs` | 94/97 | 96.90721649484536% |
| `oracle.rs` | 7/7 | 100% |
| `process_windows.rs` | 316/331 | 95.46827794561934% |
| `profile_sources.rs` | 420/462 | 90.90909090909091% |
| `protocol.rs` | 594/627 | 94.73684210526316% |
| `request.rs` | 386/407 | 94.84029484029484% |
| `runner.rs` | 145/178 | 81.46067415730337% |

`cargo fmt --all -- --check` and `cargo clippy --locked --offline --all-targets -- -D warnings` both exited `0`. Compilation occurred successfully in the complete test, Clippy and coverage commands; a standalone build was not launched before the stop. The first coverage setup failed before Cargo launch because the recorder was given a relative executable; `failed-attempts.md` distinguishes it from the single complete `08a-coverage` collection.

## Test integrity

All 48 frozen candidate files, 38 Rust files, 89 physical `#[test]` attributes and the executable test list were inspected. The 89 physical tests matched 89 listed executable tests. No ignored tests, prohibited mock decorators, mock-generating dependencies, coverage suppression, retry inflation, unconditional passing path or confirmed result manipulation was found. Four conditional attributes are bounded private `#[cfg(test)]` seams. Compiled support peers exercise real Windows processes and pipes for offline protocol behavior, but they receive no live-Codex credit. Details are in `test-integrity.md` and `01-integrity-locators/`.

## Stopping decision and unperformed work

The first complete coverage measurement was terminal under the selected QA contract. No live `profile-sources` command was run against the frozen candidate in this QA campaign. A prior developer-side observation of an installed `chrome/latest` reparse is contextual only and is not an independent current result. The QA-owned `focused_f02.py` and `verify_retained_evidence.py` were prepared but remain **NOT_RUN** because executing further checks after the metric stop would violate the campaign rule.

NI-T05 live launch recheck, installed-profile portions of NI-T09/NI-T10, WN-01 and WN-02 remain blocked or not run. Both native attempt counters remain zero. No Codex model process was launched. There was no in-flight product work at the stop, and final readback matched all 48 live and snapshot files plus all six input/specification bindings.

## Disposition and retest handoff

Development must restore meaningful full-source coverage to at least 95% without excluding first-party behavior, weakening assertions or changing thresholds. Return a new frozen candidate manifest and test evidence. Independent QA must rerun integrity review, the complete locked all-target suite, formatting, Clippy and a fresh full-source coverage collection; the old coverage result cannot qualify changed bytes. Only after those gates pass should QA independently collect the installed profile sources and consider the bounded live preflight and zero-retry native trials.

Framework acceptance remains **NOT_EVALUATED**. This report is a product QA verdict and cannot issue protected acceptance or deployment authorization.

## Evidence delivery

- Evidence root: `C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion-qa\20260915T2325371896643Z`.
- Frozen identity and final readback: `00-freeze-audit/` and `10-final-readback/`.
- Test inventory and raw full-suite evidence: `02-test-list/` and `03-full-tests/`.
- Independent policy result: `04-policy-oracle/`.
- Formatting and Clippy: `05-format/` and `06-clippy/`.
- Preserved setup failure: `08-coverage/` and `failed-attempts.md`.
- Complete raw coverage: `08a-coverage/coverage.json`, `08a-coverage/stdout.bin`, `08a-coverage/stderr.bin`, and `target-coverage/llvm-cov-target/*.profraw`.
- Independent coverage denominator and per-profraw hashes: `09-coverage-analysis/stdout.bin`.
- Final immutable index: `artifact-manifest.json`; it excludes itself to avoid a circular digest and records every delivered evidence file other than disposable Cargo build products.
