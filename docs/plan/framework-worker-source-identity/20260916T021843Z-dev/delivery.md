# Delivery: bounded plugin-cache source identity

## Scope-qualified disposition

**Development status: COMPLETE for the selected bounded source-identity amendment.** The frozen Rust candidate implements the reviewed `chrome/latest` directory-junction exception, preserves rejection of every other reparse point, binds physical source bytes and directory membership, and performs the required identity checks before collection, after collection, and immediately before process creation.

**Independent QA: PASS for the selected offline scope.** The independent report found no product defect in that scope. This result qualifies the amendment and its offline worker regressions; it does not qualify an installed effective profile or an actual Codex launch.

The broader continuation remains **INCOMPLETE**: the effective profile has not been qualified, WN-01/WN-02 remain **0/2 NOT_RUN**, and framework acceptance is **NOT_EVALUATED**.

## Delivered candidate and contracts

- Candidate: `devforgeai/experiments/codex-worker-probe`, 56 files.
- Frozen candidate manifest SHA-256: `3108f976f7d51b734ab995ebf729302ef74a4386ddaafb5561cddbd6f588d65c`.
- Independent QA report SHA-256: `b2e8304c07a89a7c155669e1d0a9e9b93c8f5a0ac966b567fca1fee461b7f2d0`.
- Governing contracts: `codex-worker-feasibility-v1.md`, `codex-worker-native-readiness-v1.md`, `codex-worker-preflight-v1.md`, and [`codex-worker-source-identity-v1.md`](../../../specs/framework/runtime/codex-worker-source-identity-v1.md). Their QA-bound SHA-256 values are recorded in the [independent QA report](../../framework-worker-source-identity-qa/20260916T021843Z-retest/qa-report.md).
- Platform: native Windows x64, Windows 10.0.26200, NTFS workspace, default Cargo features.

The implementation adds a compiled source-identity record for the exact reviewed mapping `C:\Users\bryan\.codex\plugins\cache\openai-bundled\chrome\latest` to version `26.908.70816`, with directory-junction tag `0xA0000003`. It records schema-v2 inventory identity and junction metadata, inventories the physical version directory once, distinguishes junction membership in parent directory indices, and requires exact physical review bindings. The exception applies only at the fixed installed cache root. Synthetic or alternate roots do not acquire a runtime exemption.

No installed plugin, profile, operational skill, startup configuration, or dependency was changed. The candidate has no Git metadata, so the manifest and file hashes provide source identity.

## Qualification results

| Check | Result | Evidence |
| --- | --- | --- |
| Locked offline binary build | PASS | [Developer results](developer-results.md) |
| rustfmt check | PASS | `11-format-final/receipt.json` |
| Clippy, all targets, warnings denied | PASS | `10-clippy-refactor/receipt.json` |
| Complete original-package test suite | 123/123 PASS; 37 unit and 86 integration; zero failed or ignored | `13-full-tests/receipt.json`; QA `12-full-all-targets` |
| Documentation-test command | PASS; zero documentation tests discovered | `15-doc-tests/receipt.json`; QA `18-doc-tests` |
| First-party executed-line coverage | 3,191/3,339 = 95.5675351901767%, PASS | `16-full-coverage/coverage.json`; QA `coverage/coverage.json` |
| Development requirement groups | 30/30 PASS | [Developer results](developer-results.md) |
| Independent QA traceability groups | 42/42 PASS | [QA requirements matrix](../../framework-worker-source-identity-qa/20260916T021843Z-retest/requirements-matrix.md) |
| Candidate and four governing specifications | Unchanged at the independent QA readback and unchanged for this delivery | Development and QA readbacks |

The 30 development groups and 42 QA groups are overlapping traceability views; they must not be added together as unique cases. The unique all-target Rust-test denominator is 123. Coverage includes all executable lines in the 12 first-party `src/*.rs` files, with no first-party exclusion. `src/lib.rs` contains declarations only and contributes 0/0 executable lines. Branch coverage is **NOT_RUN** and is not used as a substitute for the required line metric.

Independent QA inspected the complete 56-file candidate and 123 physical Rust tests. It found no ignored tests, `should_panic` tests, mock framework, mock decorator, coverage suppression, or confirmed result manipulation. Independently authored real-junction negatives and a deliberate final-boundary mutant demonstrated that the relevant assertions can fail. Private test seams use real Windows filesystem operations; public collection and launch paths remain wired to the compiled policy and final checker.

## Subsequent installed-source observation

After the scoped QA PASS, the QA-built original-package executable performed the separately authorized read-only installed `profile-sources` collection. It exited 0 without timeout and produced schema-v2 inventory containing 137 entries: 36 files, 56 directory indices, and 45 absences. The receipt records 30,774 stdout bytes, empty stderr, and an unchanged candidate manifest. See the [collection receipt](../../framework-worker-native-continuation/20260916T034357Z-source-identity/source-observation-001/receipt.json).

This observation proves that the compiled collector could inventory the then-observed installed sources through the reviewed junction. It does not establish semantic or effective-profile qualification, inactive hooks/plugins/MCP/apps, permission behavior, authentication, a Codex launch, or framework acceptance.

After that observation, workspace `AGENTS.md` changed from the historically bound 13,954-byte SHA-256 `d47868fef2b87df0b2c065cfe235cfe9f12fcf9eeffa7af1f0973d7d21916fa7` to SHA-256 `3b8e2a112c438b536ab59db2abbcfd6e08ebdd7f41caa13cdf6d5c49866fab86`. The parent did not make that change. The development and QA readbacks remain valid historical observations of their frozen inputs, while the installed-source observation must not be treated as current launch evidence after this instruction drift. The [native continuation](../../framework-worker-native-continuation/20260916T034357Z-source-identity/) owns any required fresh collection and profile review.

## Retained attempts and evidence limitations

- The valid behavioral Red attempts and their passing Green successors are retained. Earlier collector and runner attempts that failed during setup are classified as setup failures, not product failures.
- A first Clippy run retained three style findings. Minimal borrow and iterator refactoring was followed by passing Clippy, formatting, full tests, and coverage.
- Early discovery notes describe a PowerShell parse error and an unavailable Rust metadata method, but do not retain their complete original console bytes and exact source revisions. Fresh decisive metadata and directory-type observations replaced them before implementation.
- Independent QA attempt 13 is excluded because the original pre-correction public-helper bytes were unavailable. Fresh byte-bound attempt 15 supplies the qualifying public controls. QA attempt 35 is retained as a QA-oracle failure caused by the wrong seam; the corrected attempt 38 passed without changing the frozen candidate.
- Raw test and coverage outputs, including coverage JSON SHA-256 `3d56e45cb8c7dc4dcecb2c118ee5c5a9f1d18eb186444fcb2b8a68d85d985dd0`, are retained. The [receipt readback](receipt-readback.json) found no stream readback errors.
- No Linux result, native Codex execution, effective-profile result, or branch-coverage measurement is claimed.

These limitations do not reduce the selected offline PASS. They prevent broader native-readiness or protected-acceptance claims.

## Remaining work and next action

The [native continuation directory](../../framework-worker-native-continuation/20260916T034357Z-source-identity/) is the current source for profile and launch readiness. It is separately reviewing the inherited `ANTHROPIC_API_KEY` environment-variable name guard prerequisite with an advisor. No Codex trial has been launched. That review and any source recollection must finish before deciding whether the selected one-shot native trials can proceed.

WN-01 must demonstrate an actual bounded Codex completion under the qualified profile. WN-02 must demonstrate cancellation and verified process-tree cleanup. Until both prerequisites and both trials are completed, native readiness remains **INCOMPLETE** and the trial count remains **0/2 NOT_RUN**.

Protected framework acceptance is a separate authority decision. No qualified compiled-Rust authority has evaluated this delivery or issued a protected receipt, so framework acceptance remains **NOT_EVALUATED** and is not established.

## Evidence index

- [Developer results](developer-results.md)
- [Development handoff](handoff.md)
- [Receipt readback](receipt-readback.json)
- [Independent QA report](../../framework-worker-source-identity-qa/20260916T021843Z-retest/qa-report.md)
- [Independent QA artifact index](../../framework-worker-source-identity-qa/20260916T021843Z-retest/artifact-index.json)
- [Installed-source collection receipt](../../framework-worker-native-continuation/20260916T034357Z-source-identity/source-observation-001/receipt.json)
- [Current native continuation](../../framework-worker-native-continuation/20260916T034357Z-source-identity/)

This report is the new development closeout artifact. The parent closeout must include it in the final exclusive evidence seal; this report does not create or replace that seal.
