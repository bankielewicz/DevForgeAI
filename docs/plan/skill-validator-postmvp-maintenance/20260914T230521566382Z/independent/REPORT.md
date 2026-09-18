# Independent assessment of validator enhancements

**Overall independent assessment: INCOMPLETE.** Focused reproduced implementation defects were corrected and their targeted retests passed. After the first campaign inherited a read-only actor sandbox, the user authorized two fresh final-source trials with explicit workspace-write. **One of two selected native delivery scenarios completed:** ledger-c delivered a correct bounded assessment; ledger-d detected the seeded defect but timed out before report/revision delivery. No further retry was performed.

This is independent supporting-helper and workflow evidence, not a complete skill-validator assessment or protected framework acceptance. No production or operational source was edited by this evaluator.

## Frozen expectations and coverage

The original [cases.json](cases.json) was saved before interface execution, SHA256 `BFB34148ED030B1FD3DD8B92B8E56FEBB0A9575C92544C7418B1348D877DF763`. It contains 20 behavioral expectation groups, not a unit-test suite. A PARTIAL disposition means some expectations were exercised but the complete original group was not independently demonstrated.

| Case | Independent disposition | Evidence or remaining gap |
|---|---|---|
| IND-001 Valid minimal metadata | PARTIAL | Shared parser accepts; all format entrypoints not independently exercised. |
| IND-002 Standard optional fields/host separation | PARTIAL | String metadata and allowed-tools accepted; complete optional-field and installed-checker comparison not exercised. |
| IND-003 Numeric metadata value | PARTIAL | Shared parser rejects; consumer parity not independently rerun. |
| IND-004 allowed-tools sequence | PARTIAL | Shared parser rejects; consumer parity not independently rerun. |
| IND-005 Malformed/duplicate keys | PARTIAL | Mixed non-string and duplicate keys reject; all unhashable-key variants not executed here. |
| IND-006 Length boundaries | NOT_RUN | Root developer tests are separate evidence. |
| IND-007 Original snapshot identity | NOT_RUN | Not independently exercised. |
| IND-008 Advisory size/Unicode/quoted examples | NOT_RUN | Separate resource reviewer owns that assessment. |
| IND-009 Plan-before-launch | PARTIAL | Changed original plan rejected before started.json; all chronology variants not exercised here. |
| IND-010 Inventory completeness/duplicates | PARTIAL | Sealed-dependency omission reproduced and fixed; all duplicate inventory variants not exercised here. |
| IND-011 Missing output despite exit zero | PASS | Mechanical obligation fails as required. |
| IND-012 Semantically wrong JSON output | PASS | Wrong total fails; additional Boolean/numeric confusion reproduced and fixed. |
| IND-013 Correct delivered JSON | PASS | Readback succeeds and artifacts are digest-bound. |
| IND-014 Native/utility default limits | PARTIAL | Actual explicit 600-second native plans exercised; independent default-value comparison not run. |
| IND-015 Timeout/descendant cleanup | PASS | Real Windows descendant terminated; marker preserved; independent process-handle check. |
| IND-016 Blocked/dependent/independent continuation | NOT_RUN | No independently scored complete three-case campaign here. |
| IND-017 Attempts/resume/drift | PARTIAL | Old startup attempts retained; plan/input/post-run directory drift reject; full interrupted-resume sequence not exercised. |
| IND-018 Literal metacharacter prompt/argv | NOT_RUN | No dedicated independently scored literal-injection case here. |
| IND-019 Declared CLI failure interface | PARTIAL | Native actors ran actual helper help/missing-argument cases; remaining behavior was explicitly in-memory. |
| IND-020 Independent complete forward workflow | INCOMPLETE | Final-source ledger-c assessment delivery passed; ledger-d timed out before required adverse report/revision delivery. |

No synthetic aggregate pass percentage is assigned to partially exercised expectation groups. Root regression, coverage and resource-review evidence must be reported separately.

## Reproduced defects and retests

Original probes are retained in [probe-results.json](probe-results.json) and [findings.md](findings.md). Changes were made by the parent, not this evaluator.

- **Malformed/incomplete receipt acceptance:** omitted streams, altered timeout/schema, Boolean exit code and negative elapsed time accepted as PASS. Fresh [retest-001](retest-001/results.json) rejects them, also checking missing manifests and erased change accounting.
- **Sealed prerequisite omission:** summary omitted a recorded dependency and returned PASS. Fresh retest rejects the mismatch.
- **Missing side-effect observations:** unlisted created file absent from accounting. Fresh retest observes it and rejects subsequent drift.
- **JSON Boolean/numeric confusion:** `true` satisfied expected numeric `1`. Fresh [retest-002](retest-002/results.json) returns FAIL.
- **Native trial with no obligations:** completion prose alone received PASS. Fresh retest rejects empty native assertions.
- **Preexisting artifact credited as delivery:** no-op actor received PASS from a preexisting report. Fresh retest rejects preexisting expected outputs during sealing. This is a fresh-artifact contract; preservation/idempotent observations require a distinct explicitly designed scenario.

The original input-root finding is retained as a **specification clarification**, not a product defect. SVE-04 now explicitly permits protected fixture inputs within the disposable root if unchanged. Fresh retest accepts unchanged fixtures and rejects drift.

These retests apply to the then-observed candidate hashes retained beside the results. Later changes to console encoding and unrelated resource checks require their separate root verification; earlier successful results do not automatically qualify changed bytes.

## Native forward campaign 001

See [adjudication.md](forward-001/adjudication.md) and [continuation.md](forward-001/continuation.md).

- Both attempt-001 launches failed before actor startup with app-server Access denied. No fixture changes; cleanup VERIFIED. Host-approved attempt-002 continuations preserved these failures and retained the same budgets.
- Both attempt-002 actors inherited **read-only** Codex configuration. They completed in 141.797 and 146.937 seconds, with no timeout, unchanged input digests and VERIFIED cleanup.
- Ledger-a, originally intended as a positive control, had a real fixture preservation defect when input/output identify the same file. The actor discovered it. It must not be reported as a qualified clean control; the original oracle remains unchanged.
- Ledger-b detected the seeded constant-zero defect and the same alias-preservation defect.
- Actors accurately distinguished source/in-memory observations from real-file behavior and explicitly reported all report/fix artifacts undelivered. Mechanical runner outcomes are FAIL due absent review.md; semantic adjudication attributes missing delivery to the read-only harness capability, not a demonstrated validator instruction defect.
- Snapshot was 86 files/767847 bytes, manifest SHA256 `4812bd979c0e1e262d960cc6dfe1f9746bec33e9cc3c79899d440d77832b44ea`. [Snapshot differences](forward-001/snapshot-current-differences.json) identify later source changes. Actual usage events are retained separately per actor without estimates.

Native sessions were fresh but inherited host configuration and memory. This is procedural independence, not a claim of complete informational or operating-system isolation.

## Final-source campaign 002 — completed positive, incomplete adverse

[forward-002](forward-002) contains independently corrected ledger-c and adverse ledger-d fixtures, explicit `--sandbox workspace-write` actor argv, 600-second budgets, fresh plans and attempt-001 seals. Both helpers have resolved-path/samefile source-preservation guards; only ledger-d retains the constant-zero defect. Actor prompts contain only selected validator path, target/specification, realistic task, permitted project and requested review.md delivery. Held-out semantic oracles remained outside actor context/root. User authorization and direct root host approvals are retained; a canceled pre-execution delegated request did not start or retry either actor.

Final-source snapshot: **89 files / 847974 bytes**. Snapshot manifest SHA256: `61CD1D0A024B0DEA100B2DA7751E1C2DAC76EF51F713CDDC3F54268433B94EE9`. Snapshot executable hashes match the parent's declared coverage-final-003 source capture; final readback found no changes to any captured evaluator file. Both actual actor receipts report unchanged protected inputs and VERIFIED cleanup.

The exact authorized commands executed by root were:

```powershell
python -B -X utf8 docs/plan/skill-validator-postmvp-maintenance/20260914T230521566382Z/independent/forward-002/evaluator/skill-validator/scripts/trial_runner.py run --attempt C:/Projects/DevForgeAI/docs/plan/skill-validator-postmvp-maintenance/20260914T230521566382Z/independent/forward-002/ledger-c/attempt-001
python -B -X utf8 docs/plan/skill-validator-postmvp-maintenance/20260914T230521566382Z/independent/forward-002/evaluator/skill-validator/scripts/trial_runner.py run --attempt C:/Projects/DevForgeAI/docs/plan/skill-validator-postmvp-maintenance/20260914T230521566382Z/independent/forward-002/ledger-d/attempt-001
```

Ledger-c completed in **582.328 seconds**, without timeout. The summary and full report exist; all 26 local report links resolve; 24/24 real helper observations and error-free record readback support its claims. The **validator assessment-and-delivery scenario passes**, while its **target ledger-c verdict remains INCOMPLETE** for explicitly unperformed nested native/discovery coverage. These are different assessment levels.

Ledger-d timed out at the selected 600-second limit (**602.891 elapsed including cleanup**, exit 124). Its 19 helper cases include 15 passes and four confirmed wrong-total failures, but review.md, validation-report.md and revision-spec.md remain absent. Defect detection is demonstrated; complete adverse report/revision delivery is **INCOMPLETE**. No completion or usage is invented from the last progress message.

Full independent semantic readback and source bindings are in [forward-002/adjudication.md](forward-002/adjudication.md) and the two per-case independent-grade.json files. Mechanical file existence alone was not used to qualify semantic workflow quality. The known startup restriction was handled through normal host approvals; no sandbox bypass, deadline extension, or additional native attempt occurred.
