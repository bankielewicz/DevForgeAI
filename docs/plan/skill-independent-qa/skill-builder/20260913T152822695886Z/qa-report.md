# Independent QA audit: FAIL, with incomplete coverage

This exact development-source skill-builder does **not** meet the complete selected acceptance contract. Four confirmed implementation defects are demonstrated by independent positive/negative fixtures. Required native workflows and several compound subcases remain unverified. Audit reporting is complete; skill acceptance is not granted.

Target: `C:/Projects/DevForgeAI/src/agents/skills/skill-builder`

Package SHA-256: `338c70995e72637e0ce84991be110d6a371ab6965faf4009d570156ea0e13cf2` (43 files, 276,781 bytes). Both supplied specification hashes matched. Current bytes match the historical delivered receipt. The independently recomputed pre-enhancement snapshot digest also matched; 26 old files, including all legacy helpers/schemas, are unchanged, two changed and 15 were added. F-02/F-04 are inherited defects rather than demonstrated adaptive regressions.

## Consequential findings

1. **F-01:** The set reader accepts invalid linked authoring/request fields, fabricated quality statuses, and requests with the wrong target or manifest.
2. **F-03:** Both native OS helpers return MATCH for packages containing excluded synthetic private-key filenames.
3. **F-04:** Legacy adoption intake accepts a selected pointer naming another skill and run.
4. **F-02:** Authoring intake accepts unlisted fields despite its closed legacy contract.

See [findings-ledger.md](findings-ledger.md) for exact source locators, expected/actual behavior, individual reproductions, counterevidence, impact and proposed corrections. No repairs were applied. D-01 separately records the ambiguous PARTIAL label after an external concurrent edit.

## Executed observations and limits

Ordinary helper create/edit/import/spec-build/adopt, exact manual requests, B/C/N retention/conflicts, parent requirement inventories with LF/CRLF and alternate resources, topological selection, real per-member C publication, partial/eligible-subset envelopes, update-review equality/stale checks, metadata preservation and initializer/spec lookup branches were exercised independently. Static review decoded all 43 files, parsed all Python/JSON, checked the package's own artifact hashes and found no missing local Markdown link target.

Windows and native Ubuntu/Python helper executions covered binding outcomes, hostile argv paths, junction/symlink refusal and capture boundaries. Linux I/O denial passed. Linux exact/over-count cases timed out at 120 seconds on the Windows-mounted evidence path; they are NOT_RUN, not product FAIL. Synthetic credential fixture values and UUIDs stay in their disposable operational scope; UUIDs were absent from helper output. A read-only helper/controller does not establish a generated skill's suppression of product effects.

Cold CLI: installed `codex-cli 0.154.0`, existing gpt-6-astra configuration, normal workspace-write/ephemeral child invocation, no bypass flags or configuration edits. One initial create attempt failed host app-server permissions; the approved fresh create reached custody staging then timed out. All four fresh convention proposals also timed out at 120 seconds. No completed native PASS, implicit discovery PASS, autonomous set orchestration, adaptive runtime product-write gate or resume behavior is claimed. Child context was not fully held out (see E-01).

All **14 BA requirements**, **17 BAT parents**, **45 explicit compound observations**, and **178 complete-spec paragraph/table entries** are mapped in [traceability-matrix.md](traceability-matrix.md) and [complete-spec-traceability.json](complete-spec-traceability.json). BAT parent outcomes: 0 PASS, 7 FAIL, 10 NOT_RUN. Compound observations: 20 PASS, 7 FAIL, 18 NOT_RUN. Parent required-case pass rate is 0.00% (passing complete BAT cases / 17); helper subchecks and retries cannot inflate it.

Supplemental measured Windows line coverage: **1218/2093 = 58.19%**; branch coverage: **423/938 = 45.10%**. Denominator is all seven first-party Python files, no excluded executable lines. This partial instrumented campaign is below 95%; earlier uninstrumented runs cannot be retroactively counted. Linux line coverage and compiled-Rust framework qualification are NOT_RUN. The measured pass/coverage floors do not grant acceptance, and both required 95% floors remain unmet in this declared audit coverage.

The audit retained harness layout and instrumentation failures, then used fresh corrected fixtures. Those setup errors are not implementation defects or valid red tests. Some initial cases lack the full requested pre-execution digest/effect receipt, which is an explicit audit evidence gap rather than retrospective proof. Raw attempts, commands, fixtures, output and coverage data remain in this run.

## Work still required

Correct F-01 through F-04 in a separately authorized development task, then independently rerun positive and negative cases. Complete cold create/edit, monorepo and four-convention proposals (including contradictory same-scope instructions), storage/HTTP preservation, authorized/unauthorized variant dispositions, autonomous A/B/C continuation, material core update, changed-input resume, and generated-skill non-MATCH/no-product-effects trials. Complete the legacy generated-after-adoption/history and full-set/handoff/fault-interruption grids. Rerun Linux count limits on an authorized native filesystem with the same timeout, and obtain complete pre/post receipts and >=95% required suite pass rate/line coverage without excluding uncovered behavior.

Builder-to-validator execution is explicitly outside this audit. The prior compatibility report was examined only after independent planning/review, and its validator verdicts were not used as an oracle. No validator package, grader or test was loaded/executed. No operational installation, real project binding, hooks/CI, remote publication or Rust implementation was performed.

Artifacts: [findings](findings-ledger.md), [BA/BAT mapping](traceability-matrix.md), [complete specification mapping](complete-spec-traceability.json), [source review](source-review.md), [exact commands](command-log.json), [evidence index](evidence-index.json), [final readback receipt](final-readback-receipt.json). The final receipt records byte preservation and the precise evidence-index exclusions; it is an audit receipt, not framework acceptance.
