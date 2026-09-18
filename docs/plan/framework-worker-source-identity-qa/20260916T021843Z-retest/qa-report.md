# QA Report

## Identity and scope

- QA run and mode: independent `retest` of the frozen reviewed plugin-cache junction identity candidate, with the selected offline worker regression scope.
- Plan readiness: `READY`; the candidate was frozen before execution and the parent supplied explicit GO after development completion.
- Execution status: `COMPLETED`.
- Plan: `C:\Projects\DevForgeAI\docs\plan\framework-worker-source-identity-qa\20260916T021843Z-retest\qa-plan.md`, SHA-256 `eea917839b45a2db094d08e487de3265432454e25656f40617a625514bb2ce05`.
- Project and environment: `C:\Projects\DevForgeAI`, native Windows x64 10.0.26200.0, PowerShell 7.6.6, Python 3.10.11, Rust/Cargo 1.97.1, cargo-llvm-cov 0.8.4, Windows-resident NTFS workspace.
- Candidate: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`; 56-file manifest SHA-256 `3108f976f7d51b734ab995ebf729302ef74a4386ddaafb5561cddbd6f588d65c`.
- QA-built original-package executable: `C:\Projects\DevForgeAI\docs\plan\framework-worker-source-identity-qa\20260916T021843Z-retest\target-original\debug\devforgeai-codex-worker-probe.exe`; 2,280,960 bytes; SHA-256 `b63a0dfb0a48adfc5977a75d145fa766345a9d948e99b3a5bbdf5d5ce74079b2`.
- Specifications: `codex-worker-feasibility-v1.md` SHA `7cb5b0cb87e515bb4d59235b615922ab4ea07ef607b8111dde6cc73c8f101b23`; `codex-worker-native-readiness-v1.md` SHA `c3c0673cbf95ae7aa056d9fd0009ce89947309b943013fd7838438d6ee66b06d`; `codex-worker-preflight-v1.md` SHA `6e781f23f221d1033896716512e9162579653b529d107e0040d49c499574afd1`; `codex-worker-source-identity-v1.md` SHA `34160ff675f886aeeebd3a7d131fd973b86a375fb64def7604db419c79db1f8c`.
- Requested scope: SI-T01..SI-T10, WF-01..WF-20, selected offline portions of NI-T01..NI-T10, F-01/F-02, complete original-package tests/static checks/docs/coverage, independently authored negatives, sensitivity, and final readback.
- Exclusions: installed-profile `profile-sources`, Codex launch, WN-01/WN-02, actual effective-profile/native-runtime credit, installation, deployment, and protected authority decisions.
- Development handoff: `C:\Projects\DevForgeAI\docs\plan\framework-worker-source-identity\20260916T021843Z-dev\handoff.md`; development observations supplied context only.
- QA verdict: **PASS for the selected offline scope**.
- Decision basis: 42/42 selected overlapping requirement groups passed; the original-package suite passed 123/123, unit subset 37/37, complete line coverage reached 3191/3339 (95.56753519017669961066%), mandatory static/build checks passed, independent negative and sensitivity controls passed, and final source/specification/mapping readback passed. This does not establish native readiness or framework acceptance.

## Acceptance traceability

| Criterion and source | Required behavior | Case IDs | Expected result | Actual result | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Source-identity amendment | Exact selected junction and physical identity admit; target/tag/type/path/member/schema/review drift reject; final check precedes spawn | SI-T01..SI-T08 | Every conjunctive positive/negative oracle holds | Original focused campaigns passed; corrected independent matrix 3/3 passed; deliberate final-check bypass made the protected assertion fail | PASS | `09-focused-collector`, `10-focused-review`, `11-focused-final-boundary`, `38-independent-negative-matrix-corrected`, `44-final-check-sensitivity` |
| Amendment regressions | Limits, credentials, strict paths, executable/policy, WF/NI/F behavior remain valid | SI-T09 | Complete regression and quality checks pass | 123/123 suite, format, Clippy, docs and coverage passed | PASS | `12-full-all-targets`, `16-fmt`, `17-clippy`, `18-doc-tests`, `22-coverage-analysis` |
| Final identity/readback | Candidate/spec bytes unchanged and installed metadata equals the one compiled mapping | SI-T10 | Exact hashes and exact selected junction/tag/target | Candidate 56/56 and four specs unchanged; installed mapping metadata exact; no collection or launch | PASS | `50-final-readback`, `final-readback.json` |
| Base worker regression | All specified protocol/process/oracle/cancel/recovery/privacy behavior passes | WF-01..WF-20 | Every frozen test and subfixture passes | Complete frozen suite passed with no ignored or filtered required case | PASS | `08-test-inventory`, `12-full-all-targets` |
| Native-readiness offline slice | Identity/policy/review/synthetic protocol/effective-state denial behavior passes without native credit | Offline portions of NI-T01..NI-T10 | Every selected offline oracle passes | Complete frozen suite plus focused and independent controls passed | PASS | `09`..`12`, `15-public-source-identity-attempt2`, `38-independent-negative-matrix-corrected` |
| Focused regressions | Pipe-pressure cancellation/deadline and typed-error privacy remain valid | F-01/F-02 | Required process tree and privacy assertions pass | Original-package remediation tests passed inside complete suite | PASS | `12-full-all-targets` |
| Native Codex trials | Actual installed-profile and Codex-native observations | WN-01/WN-02 | Separate one-shot trials after prerequisites | Not run; installed profile was not collected and Codex was not launched | BLOCKED / NOT_RUN | `final-readback.json` |

The detailed 42-group accounting is in `requirements-matrix.md`. Its group count is a traceability view and does not inflate the unique Rust-test denominator.

## Test integrity

- Inspected scope: all 56 frozen candidate files, all 123 physical Rust tests, all first-party source, selected helpers, and QA helpers. The complete inventory is `test-inventory.json`.
- Mock-decorator result: none found. There were no ignored tests, `should_panic` tests, mock frameworks, coverage suppressions, or first-party exclusions.
- Result-gaming assessment: no confirmed gaming. Test names, setup, private seams, public wiring, fixture types, assertions, and retained outputs were inspected. Independent real-junction negatives and a deliberate final-boundary mutant showed outcome sensitivity.
- Private seams: collector mapping injection is test-only and exercises real Windows mapping/collector code; runner callback is test-only and exercises ordering. Public collection and runner entrypoints remain wired to compiled policy/checks. Synthetic evidence does not prove the installed profile or native Codex.
- Supplied versus executed: development results did not contribute passes. Attempts 05..22 and 29..50 are fresh QA observations as applicable; copied-package attempts are supplemental and excluded from original-package metrics.
- Attempt 13's positive product call is excluded because the pre-correction public helper bytes were not bound or retained. Fresh bound attempt 15 supplies the qualifying public controls.
- Attempt 35 is a retained QA oracle failure, not a product result. The review seam used `|_| Ok(())`, which bypassed inventory mapping verification. The exact pre-test helper was recovered and verified at 16,627 bytes/SHA `06975d49d6ed74d672d67c161d3985b45ea94a480cc2752f604e8a1830ad40d5`. The correction kept wrong-tag coverage in the real collector/inventory validators and added omitted/extra review-binding negatives; attempt 38 then passed.

## Metrics and environments

| Platform | Metric | Numerator | Denominator | Exact percentage | Required floor | Result | Raw evidence |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| Windows x64 | Required unit pass rate | 37 | 37 | 100% | 95% | PASS | `07-list-lib`, `12-full-all-targets` |
| Windows x64 | Complete all-target pass rate | 123 | 123 | 100% | 95% | PASS | `06-list-all-targets`, `08-test-inventory`, `12-full-all-targets` |
| Windows x64 | First-party executed-line coverage | 3191 | 3339 | 95.56753519017669961066% | 95% | PASS | `20-coverage`, `coverage/coverage.json`, `22-coverage-analysis`, `coverage/analysis.json` |

- Coverage included every executable line in all 12 declared `src/*.rs` files with zero first-party exclusions; `src/lib.rs` is explicitly 0/0.
- Branch coverage was not enabled in the selected line-coverage collection and is `NOT_RUN`; it is not a selected threshold or a substitute for the complete executed-line metric.
- Documentation tests completed with 0 discovered, 0 failed. Original package build, rustfmt check, Clippy `-D warnings`, and documentation command all exited 0.
- The coverage collection was complete and usable. No second collection was run after the valid metric.
- Linux and native Codex environments were outside this Windows-only selected campaign.

## Defects and unresolved work

| Defect/gap ID | Criterion/policy | Issue class and demonstrated impact | Confirmed failure or missing evidence | Exact artifact and owner | Evidence |
| --- | --- | --- | --- | --- | --- |
| GAP-NATIVE-01 | Native readiness | Missing prerequisite/native evidence; full native readiness cannot be claimed | WN-01/WN-02 remain 0/2 BLOCKED/NOT_RUN | Native-readiness owner | `final-readback.json`, selected specifications |
| GAP-INSTALLED-01 | Source-identity SI-05 sequencing | Deliberate scope boundary; actual installed source inventory/effective profile remains unknown | Installed mapping metadata passed, but installed `profile-sources` was prohibited during QA | Native-readiness owner after this scoped PASS | `50-final-readback` |
| LIMIT-EVIDENCE-13 | QA evidence provenance | Non-product evidence limitation | Original pre-correction public helper bytes/digest are unavailable; attempt 13 positive call is excluded | QA historical evidence; superseded by fresh attempt 15 | `13-public-source-identity`, `14-public-helper-identity`, `15-public-source-identity-attempt2` |

- Confirmed product defects: none in the selected offline scope.
- Advisory items outside mandatory scope: branch coverage was not collected; no acceptance conclusion depends on it.
- Remaining obligations: installed-profile source collection/preflight and WN-01/WN-02 under their separate authorization and one-shot rules.

## Continuation, stopping and remaining obligations

- No terminal stop trigger fired. The complete valid coverage result exceeded 95%; all complete test-rate metrics exceeded 95%; no gaming or critical security/data-loss issue was confirmed.
- Retained non-product setup/oracle attempts: 01/02 environment setup, 13 unbound public helper normalization, 24 snapshot copied generated targets, 27 absolute-executable recorder prerequisite, 30 QA formatting, 35 wrong-seam QA assertion, and 47 PowerShell quoting. Each was preserved and classified before a distinct corrected attempt.
- Attempt 24 contained 6,374 generated `target/` extras, with no source missing or source hash mismatch. A new manifest-driven 56-file source-only snapshot was created and passed in attempt 29; attempt 24 was not overwritten.
- The first seal-helper invocation rejected the intentionally retained public-control junction fixture and created no artifact index. `seal-attempt1-error.txt` preserves the setup error; the corrected helper records reparse metadata without traversing the junction and remains subject to the final exclusive-create seal.
- Independent checks continued only after confirming each issue was contained to QA setup/oracles and the frozen candidate remained unchanged.
- No owned process remains. QA target directories, copied packages, fixtures, raw attempts, and failed attempts are intentionally retained under the evidence root.

## Disposition

- Product QA outcome: **PASS for the selected offline 42-group scope**, with 123/123 complete suite, 37/37 units, and 95.56753519017669961066% line coverage.
- Remediation owner on FAIL: not applicable; no `qa-fix.md` is produced.
- Source/candidate drift: final candidate 56/56 and all four specification hashes match the freeze.
- External framework acceptance: **NOT_EVALUATED**.
- Release/deployment authorization: not granted by this QA result.

## Artifact delivery

- Evidence root: `C:\Projects\DevForgeAI\docs\plan\framework-worker-source-identity-qa\20260916T021843Z-retest`.
- Required artifacts: `qa-plan.md`, `qa-report.md`, `checkpoint.json`, `requirements-matrix.md`, `test-inventory.json`, `test-integrity.md`, `coverage/analysis.json`, `final-readback.json`, attempt receipts/raw output, and `artifact-index.json`.
- Fix packet: not applicable for PASS.
- Final external manifest: `artifact-index.json`; use entries `qa-report.md`, `checkpoint.json`, `requirements-matrix.md`, `coverage/analysis.json`, and `final-readback.json` for final byte bindings. The manifest intentionally has no self-hash entry.
- Recovery action for failed writes/readback: none pending. All failed attempts remain evidence and their corrected successors are distinct.

## End-user handoff

- Open `C:\Projects\DevForgeAI` on native Windows.
- Next owner: project/native-readiness reviewer.
- Next action: review this scoped PASS and the external artifact index. The specification now permits a separately controlled read-only installed-profile source collection; it remains distinct from this QA run and must not be treated as native readiness or framework acceptance.
- Skill availability: the operational QA skill was available and applied. No remediation skill is needed.
- Resolved continuation prompt:

```text
In C:\Projects\DevForgeAI on native Windows, review the independent QA report and artifact index under docs\plan\framework-worker-source-identity-qa\20260916T021843Z-retest. The selected offline QA result is PASS; framework acceptance remains NOT_EVALUATED and WN-01/WN-02 remain 0/2 BLOCKED/NOT_RUN. If the installed-profile continuation is separately selected, use the QA-built original-package executable at docs\plan\framework-worker-source-identity-qa\20260916T021843Z-retest\target-original\debug\devforgeai-codex-worker-probe.exe, SHA-256 b63a0dfb0a48adfc5977a75d145fa766345a9d948e99b3a5bbdf5d5ce74079b2, for the read-only source collection. Preserve all QA and development evidence, do not modify the installed profile, do not launch Codex or consume WN-01/WN-02, and report the exact collection receipt and prerequisite outcome separately.
```
