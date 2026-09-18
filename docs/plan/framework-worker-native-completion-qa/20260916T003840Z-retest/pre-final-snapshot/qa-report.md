# PASS — QA-F-COV-01 independent Windows x64 retest

## Verdict and scope

**PASS for the selected offline defect retest.** `QA-F-COV-01` is **VERIFIED_FIXED** on the exact 53-file candidate bound by `candidate-manifest.json` SHA-256 `c27d8ce1742ba7cd0955f0bd18aded8de5f14c898c989654d7298835c3256f9e`.

- Candidate: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`.
- Specifications: `codex-worker-feasibility-v1.md` SHA-256 `7cb5b0cb87e515bb4d59235b615922ab4ea07ef607b8111dde6cc73c8f101b23`; `codex-worker-native-readiness-v1.md` SHA-256 `c3c0673cbf95ae7aa056d9fd0009ce89947309b943013fd7838438d6ee66b06d`; `codex-worker-preflight-v1.md` SHA-256 `6e781f23f221d1033896716512e9162579653b529d107e0040d49c499574afd1`.
- Platform/configuration: native Windows 10.0.26200 x64, `x86_64-pc-windows-msvc`, PowerShell 7.6.6, package default features, locked and offline Cargo resolution.
- Scope: fresh coverage closure plus the full offline regression invalidated by the changed test candidate: all 114 Rust tests, WF-01..20 and subfixtures, F-01/F-02, affected offline NI-T05 and NI-T07..NI-T10 behavior, formatting, Clippy, documentation-test discovery, integrity review and final source readback.
- Excluded from execution: installed-profile source collection; live Codex/model work; live portions of NI-T05/NI-T09/NI-T10; NI-T11/NI-T12; WN-01/WN-02; authority provisioning and protected acceptance. Native trial attempts consumed: **0**.

Git metadata is absent under the governing repository instructions. Candidate identity therefore uses the frozen manifest, exact snapshot and SHA-256 bindings. Initial and final audits each matched 53/53 live candidate files, 53/53 snapshot files and 11/11 specification/handoff inputs. The final audit found no candidate change.

## Findings

### QA-F-COV-01 — VERIFIED_FIXED — mandatory line coverage now exceeds 95%

- Requirement: repository coverage floor and DFF-WORKER-FEAS-01 section 9 require at least 95% executed-line coverage of all first-party executable framework code.
- Original observation: 2,852/3,103 lines, `91.91105381888495004834031582%`; the preserved original QA result was FAIL.
- Independent retest: one complete fresh `cargo llvm-cov --locked --offline --all-targets` collection completed with exit 0. Independent analysis of the unchanged raw JSON measured **2,967/3,103 = 95.61714469867869803416048984853367708669%**.
- Denominator: all 12 frozen `src/**/*.rs` files; 11 contain executable-line records. `src/lib.rs` contains only a crate documentation comment and ten module declarations, so LLVM omitted it and QA records it as 0/0. First-party exclusions: **none**.
- Evidence: `09-full-coverage/receipt.json`, `09-full-coverage/coverage.json` SHA-256 `dac80cc9483db8c833d1cc7377af588679da4d96616254004cbd714d24b36850`, `10a-coverage-analysis/receipt.json`, `source-denominator.json`.

No unresolved product defect was observed in the selected offline scope.

## Required-case results

| Denominator | Passing / required | Rate | Result |
| --- | ---: | ---: | --- |
| Windows x64 unique executable Rust suite | 114/114 | 100% | PASS |
| Overall selected executable Rust suite | 114/114 | 100% | PASS |
| Library/unit subset | 28/28 | 100% | PASS |
| Integration subset | 86/86 | 100% | PASS |
| Selected offline requirements-matrix cases | 33/33 | 100% | PASS |
| Mandatory WF parents | 20/20 | 100% | PASS |
| F-01/F-02 regression groups | 2/2 | 100% | PASS |
| Added requirement-derived test subset | 25/25 | 100% | PASS |

These subsets are not added to the 114-test denominator. Cargo's independent list contained 114 unique cases, exactly matched the frozen developer inventory, and contained no ignored cases. Full execution reported 114 pass, 0 fail, 0 ignored and 0 filtered. The coverage repetition is an attempt, not an added pass.

## Coverage

- Executed lines: **2,967**.
- Executable lines: **3,103**.
- Percentage: **95.61714469867869803416048984853367708669%**.
- Threshold: 95%; result PASS at full precision.
- Declared first-party source: 12 files; collector-reported executable source: 11 files; zero-executable source: `src/lib.rs`.
- First-party exclusions: none.
- Raw profiles: 167 files, 3,468,152 bytes, retained under `target-coverage` and indexed by the final artifact manifest.
- Branch coverage: **NOT_RUN**. cargo-llvm-cov 0.8.4 reported a zero branch denominator, so no branch percentage is claimed.

Per-file results are retained in `10a-coverage-analysis/stdout.bin`. The lowest file result is `src/runner.rs` at 146/178; the mandatory metric applies to the complete declared source denominator and passes.

## Build, behavior and analysis results

| Check | Observed result | Evidence |
| --- | --- | --- |
| Candidate/test enumeration | 114 unique all-target cases; 28 unique unit cases; no ignored or inventory mismatch | `02-test-list/`, `02a-unit-list/`, `test-denominator.json` |
| Locked/offline build and full tests | Exit 0 in 158.454 s; 114/114 pass | `03-full-tests/receipt.json` and raw streams |
| WF-01..WF-20 | 20/20 parent tests pass; every required subfixture assertion remains inside its parent | `03-full-tests/stdout.bin`, retained fixtures |
| F-01 | Full-pipe deadline/cancellation and verified Windows process-tree cleanup pass | `03-full-tests/` |
| F-02 compiled and QA-owned supplement | Compiled regression passes; independent malformed-payload matrix passes 19/19 with exact exit 4, no private marker, unchanged fixture and nonempty closed journal | `03-full-tests/`, `05-f02-focused/` |
| Restrictive launch policy | Independent contract oracle passes exact policy digest, 116 ordered argv items, 56 config overrides and 35 unique disabled features | `04a-policy-oracle/` |
| rustfmt | Exit 0 | `06-format/` |
| Clippy | `--locked --offline --all-targets -- -D warnings`, exit 0 | `07-clippy/` |
| Documentation tests | Discovery/runner exit 0; package contains 0 documentation-test cases | `08-doc-tests/` |
| Instrumented suite | Exit 0 in 171.109 s; raw coverage written | `09-full-coverage/` |
| Final source/input readback | 53/53 candidate, 53/53 snapshot and 11/11 inputs match; unchanged | `11-final-readback/` |

The two retained `RT-source-type-*` directories created by independent execution are synthetic native-layout fixtures, not native Codex trials. Their task bytes match the frozen 307-byte task SHA-256 `b35366b508eea199c12142a8a4a8d13a083426c35c4b9ebaf9f0ccf168eeab3a` and their timestamps fall within the full-test and coverage receipts; see `external-fixtures-after.json`.

## Test-integrity assessment

- The candidate contains 114 physical `#[test]` attributes, matching both Cargo's list and the declared inventory.
- No ignored or `should_panic` test, coverage suppression, mock/fake/double dependency, prohibited mock-generating attribute, retry loop or unconditional passing path was found.
- The 25 added tests exercise distinct effective-profile, source-inventory, protocol and runtime/CLI failure behavior. They are not setup-only or vacuous. Shared fixtures construct inputs but do not decide acceptance.
- A deterministic peer isolates the external provider for offline protocol/process tests. It does not receive credit for native Codex/profile behavior.
- Expected policy bytes are derived independently from the selected contract. The focused F-02 oracle independently checks process exit, byte-canary absence, journal envelope and fixture immutability.
- Existing runtime function bodies and original tests are unchanged. The remediation adds characterization/negative tests, a test-peer Cargo registration and a private test-only module registration; it does not claim a runtime behavior repair.

No test-result manipulation was established. Details are in `test-integrity.md` and `01-integrity-locators/`.

## Preserved QA execution issues

Four nonproduct errors remain visible in `failed-attempts.md`:

1. `00-freeze-audit` passed a binding as two arguments and failed before product execution; corrected identity audit is `00a-freeze-audit`.
2. `04-policy-oracle` used a stale Python path and failed before spawning the helper; recorded execution is `04a-policy-oracle`.
3. `10-coverage-analysis` rejected LLVM's omission of module-only `src/lib.rs`. The QA analyzer was narrowed to permit an omitted source only when every meaningful line is a strict public module declaration, then reran against the same raw JSON as `10a-coverage-analysis`. The product coverage suite was not repeated.
4. The first artifact-seal shell command omitted PowerShell's call operator and failed during parsing before the seal helper ran. The corrected command created the manifest after final report bytes were bound.

None is counted as a product case or pass. All original bytes/partial records were preserved.

## BLOCKED and NOT_RUN

- Native readiness remains **7/12 = 58.33333333333333%** based on the prior selected full-readiness assessment. This coverage retest does not grant additional live credit.
- NI-T05's final identity observation immediately before a real Codex launch is BLOCKED/NOT_RUN.
- Installed-profile live portions of NI-T09 and NI-T10, including the real profile-source collector, are BLOCKED/NOT_RUN.
- WN-01 successful Codex work and WN-02 cancellation/verified cleanup are NOT_RUN; native attempts remain 0/2.
- Branch coverage is NOT_RUN because no branch denominator was produced.
- Linux is not a required platform for this selected Windows-native worker retest and was not run.

## Framework acceptance

Framework acceptance is **NOT_EVALUATED** and is not established. No qualified compiled-Rust acceptance authority independently evaluated this candidate or issued a protected receipt. This QA PASS, Cargo results, Python evidence helpers and developer report cannot substitute for that authority decision.

## Evidence and handoff

Fresh evidence root: `C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion-qa\20260916T003840Z-retest`.

Key records: `input-bindings.json`, `candidate-bindings.json`, `qa-plan.md`, `case-matrix.json`, `case-results.json`, `source-denominator.json`, `test-denominator.json`, `test-integrity.md`, `failed-attempts.md`, command receipts/raw streams, `external-fixtures-after.json`, `checkpoint.json`, `handoff-manifest.json` and `artifact-manifest.json`.

No further product remediation is required for `QA-F-COV-01`. The next work is a separate prerequisite-gated native phase: resolve and review the actual installed profile/source inputs and execute the already selected WN-01/WN-02 native trials. Implementing, independently qualifying and provisioning the deferred compiled-Rust acceptance authority remains a separate assignment under its own contract. This PASS may be used as the offline regression and metric input to those phases; it does not make native readiness complete or establish framework acceptance.
