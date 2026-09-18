# Targeted independent retest

Native Windows synthetic subprocesses only; no model sessions. Source identities are captured before and after execution. Original evidence remains in the parent directory.

## Resolved on this candidate

- All five originally accepted malformed receipt variants now reject. Missing manifest bindings and erased changed-path accounting also reject.
- Summary rejects an inventory that removes a dependency recorded in its sealed plan.
- Created files appear in side-effect accounting; changing an unlisted file after execution invalidates readback.
- Input/plan drift rejects, including before launch without creating a start receipt.

The original input-root point was a **specification ambiguity**, clarified in SVE-04 and reliable-evaluation.md. Protected fixtures inside the disposable root are permitted when unchanged. This retest accepted the unchanged fixture and rejected its later drift. The original observation is retained; it is not counted as a production defect repaired in code.

## New observations requiring disposition

1. **JSON type confusion:** an output containing `{"total": true}` passes against expected `{"total": 1}`. Python equality merges Boolean and numeric types. Evidence: `boolean-json/plan.json`, `boolean-json/project/report.json`, `boolean-json/attempt/result.json`. Use type-aware JSON comparison so booleans cannot satisfy numeric expectations.
2. **Native success without obligations:** native plan with empty expected_outputs and a command printing only completion seals and returns PASS. This contradicts the instruction that every native scenario needs observable or independently graded obligations. Evidence: `no-native-obligations`. Reject empty native assertions or retain NOT_RUN until independently assessed; utility-only controls remain distinct.
3. **Preexisting artifact credited as delivery:** a correct report exists before execution; actor prints completion and performs no work. Runner returns PASS with empty changed_paths. The content observation is true, but does not prove requested delivery. Evidence: `preexisting-output`. Require fresh or demonstrably written delivery for delivery assertions, or support an explicit observation-only/preservation assertion and label its limited meaning. A blanket change requirement would incorrectly fail legitimate idempotent preservation, so the interface needs an explicit distinction or a clear fresh-fixture precondition.

There are 19 focused observations: 16 met the independently selected expectation and three exposed the issues above. These counts are helper observations, not skill scenario qualification or full package acceptance.
