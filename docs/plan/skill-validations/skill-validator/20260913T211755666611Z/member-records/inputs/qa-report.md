# Fresh repair QA

**QA-01 through QA-04 are RESOLVED on the delivered candidate. Full package acceptance remains FAIL.**

## Remaining findings first

1. **Existing regression assertion mismatch:** one unchanged authoring test method fails in seven subtests. It expects `must be an array`; the current companion reader emits `$.<field>: wrong type`. The exact same seven failures reproduce on the untouched pre-repair 75-file validator snapshot with the same companion. This is not introduced by the selected repairs. No assertion was weakened and no companion file was changed. [Current run](commands/FULL-REGRESSION/stderr.txt), [pre-repair control](commands/PRE-REPAIR-FAILURE-CONTROL/stderr.txt), [controlled input identity](baseline-failure-plan.json).
2. **Coverage requirement unmet:** executed-line coverage is 2608/3459 = **75.3975%**, below 95%. Branch coverage is 1182/1822 = 64.8738%. All nine first-party executable support scripts were declared before collection; no first-party exclusions or aliasing of temporary code copies to pristine paths. This is Windows Python coverage, not Rust coverage. [Measurement](coverage-summary.json), [denominator](coverage/denominator-before-run.json).

## Selected repairs

| Finding | Result | Evidence |
| --- | --- | --- |
| QA-01 duplicate execution/artifact counts | RESOLVED | D01-D05, REPLAY-R06; new duplicate/different-run/shared-citation regressions |
| QA-02 required handoff excluded as N/A | RESOLVED | H01-H11, REPLAY-R07; contradictory-N/A and unknown regressions |
| QA-03 missing protocol Unicode candidate | RESOLVED | U01-U07, REPLAY-P08; JSONL, multiline locations and redaction regressions |
| QA-04 premature fence closure | RESOLVED | F01-F10, REPLAY-P07; true line-5 edge, literal line-3 example and anchor regressions |

All **37 retained cases pass**, with zero observed false positives or missed expected detections in that selected corpus. Expected outcomes were retained before execution; originals were replayed read-only and independent fixtures were reconstructed in this fresh run. The complete suite discovered **249 test methods**, versus the previous 229: the increase is exactly 20 new focused methods. **248/249 methods pass**; one method has seven failing subtests, all reproduced before the repair. Counting 249 minus seven would incorrectly mix method and subtest denominators. All 20 added methods pass; their initial run retained 13 requirement failures and no setup errors.

The independent reviewer used a separate agent context, verified candidate identity, reviewed record-integrity changes, and executed 16 additional JSON/fence/anchor probes: all matched. Its accounting/handoff review is static; root's retained public-interface probes supply executed coverage. Same-model review is not enforced isolation or protected acceptance. [Independent report](independent-review/independent-review.md).

Installed quick_validate.py passes on the captured candidate. The bound evaluator ran the actual legacy-import-v1 profile and emitted two matching JSONL observations after validating artifact binding. Full regression tests also exercised the existing compatibility profiles. A valid structural/profile result does not override the failed regression or coverage requirement.

## Identity, scope and effects

Target: `C:/Projects/DevForgeAI/src/agents/skills/skill-validator`; **76 files**, package digest `5a3ea08fdbf7ff5f8b9e36d7015e61967c56dd1debdf548f3e1c23b8aed8a57b`. Changes are exactly two production scripts, one added test file, and the evaluation manifest. Existing tests and schemas were preserved. Both frozen specification hashes match. The operational evaluator remains the original 75-file package; it was loaded as instructions but was not installed or updated. Target helpers assessing target behavior are self-review, supplemented by independent expectations and the separate reviewer.

Executed with native Windows Python on the C: checkout, with installed coverage.py and PyYAML. Temporary roots and coverage startup helper are confined to this QA run; no installed sitecustomize or environment configuration was changed. No WSL checkout switch, dependency installation, real binding, operational-copy edit, remote publication, or Rust change occurred. Target candidate, companion and operational evaluator match final readback; replay receipts verify fixture preservation. Whole operational homes/historical trees were not captured.

## Closure

Selected defect remediation: **PASS**. Full regression: **FAIL (existing mismatch)**. Line-coverage floor: **FAIL**. Full package acceptance: **FAIL**. Native whole workflow/resume, activation, lifecycle integration, tokenizer qualification, installation and Rust qualification remain NOT_RUN or NOT_PERFORMED in this scoped maintenance.

Next work is a separately scoped reconciliation of the authoring test's expected error contract, additional meaningful coverage for uncovered first-party behavior, and the previously unperformed acceptance scenarios. The four repaired defects do not need reopening on the evidence available. [Resolution map](resolution-map.json), [commands](command-log.md), [final readback](final-input-readback.json).
