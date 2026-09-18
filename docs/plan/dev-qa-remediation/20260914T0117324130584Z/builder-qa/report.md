# Independent builder custody QA

Bounded Python regression assessment completed on native Windows. The final
declared authoring suite has **71 unique cases, 71 PASS, 0 FAIL/error/skip/NOT_RUN
(100%)**. The complete first-party `authoring.py` denominator is 453 statements;
435 executed, **96.02649006622516% line coverage**, with no exclusions. Branch
arc coverage is separately **225/244 = 92.21311475409836%**. Coverage.py's blended
percentage is not the required executed-line metric.

Both mandatory numeric floors for this selected supporting Python scope are met.
No production defect was observed by these tests. This is not a complete skill
assessment or Rust framework qualification. Framework acceptance: NOT_EVALUATED.

## Changes and cases

Added only `src/agents/skills/skill-validator/tests/test_authoring_safeguards.py`:
35 independent cases complement the 36 existing authoring cases. Fixtures verify
literal paths and reference boundaries, actual 2001-file and oversized-file
ceilings, changed source reads, interrupted capture/publication, preserved
concurrent edits, deletion, retained user changes versus generated baselines,
baseline recovery, original and adopted legacy histories, rejected stale legacy
evidence, and terminal begin/publish/read behavior.

Fault injection occurs at filesystem I/O or the existing before-write seam and
models corruption, concurrent writers, or unavailable storage. Tests do not skip
schema validation, fabricate successful custody results, or weaken assertions.
All writable product fixtures are synthetic temporary directories beneath each
attempt's declared evidence root; they are removed by normal fixture cleanup.
Source/test snapshots, expected contracts/assertions, commands, timestamps,
outputs, exit codes, raw coverage data and JSON remain retained for both attempts.

## Executed attempts

- `attempt-001`: 67/67 PASS; 427/453 lines (94.26048565121413%). This remained
  below the floor. Four additional substantive legacy/provenance tests were
  added before the next attempt; the first results were preserved unchanged.
- `attempt-002`: 71/71 PASS; 435/453 lines (96.02649006622516%). Final suite counts
  each declared case once; repeated cases do not inflate the 71-case denominator.

Exact commands, source digests, Windows/Python identity, timeout and write scope
are in each attempt's `plan.json`; command outcomes in `0-receipt.json` and
`1-receipt.json`. Test stdout/stderr and coverage data are siblings. The entire
authoring.py and both selected test files were byte-read back unchanged after
execution; `final-result.json` retains their expected and actual digests.

## Remaining measurement gaps

Unexecuted lines are **58, 69, 168, 171, 174, 220, 230, 232, 234, 237, 249, 255,
257, 266, 269, 352, 398, 437**. They remain in the denominator. These comprise
link/junction refusal, relative escape defense, additional legacy/authored origin
inconsistencies, duplicated field checks already preceded by schema validation,
supplied/effective consistency defense, late input-race handling, and unavailable
baseline-byte recovery. No claim is made that every uncovered branch is
unreachable; no validation rule was bypassed solely to execute a defense.

Native cold skill trials and installation are outside this bounded assignment.
