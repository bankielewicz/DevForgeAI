# Independent follow-up review

All four original findings are fixed on their original unchanged inputs. Fresh `attempt-03` outputs show IR-02 and IR-03 returning 0/OBSERVED, and malformed helper cases IR-08 and IR-09 returning 1/MISMATCH. Original failed outputs remain retained. `attempt-03/script-hashes.json` identifies the newly inspected validator scripts.

Three additional supported issues remain in the inspected set-assessment reader:

1. **F-IR05 — supported schema-1 dimension aliases rejected (IR-20; VA-001/VA-014, AV-E01, VAT-01/VAT-24).** Existing `observe.py` explicitly accepts `standards_compliance`, `workflow_correctness`, `instruction_quality`, and `behavioral_evaluation`, and normalizes them for dimension reductions. New `adaptive_observe.py:check_rows` accepts only canonical DIMENSIONS, rejecting an otherwise valid selected member's existing check rows as `unknown dimension`. Preserve the aliases when consuming legacy member checks; normalize only for interpretation without rewriting retained bytes. The equivalent canonical control IR-16 is accepted.

2. **F-IR06 — missing report suppresses validation and reduction of available member checks (IR-21 and IR-23; VA-003/VA-014, AV-E01, VAT-04/VAT-24).** `assess_record` takes the missing-report/checks branch whenever either reference is null, synthesizes 29 NOT_RUN rows and ignores a present checks file. IR-21 has an actual required FAIL plus justified inapplicable rows, report null, member INCOMPLETE as required, set FAIL and evaluated1/total1. It is rejected as `set outcome reduction mismatch` because the available failed check was replaced by synthetic NOT_RUN coverage. More decisively, IR-23 binds `checks` to a retained file containing `NOT JSON AND NOT A CHECK`, with report null, member/set INCOMPLETE, total29/evaluated0. The records command accepts it with exit 0/OBSERVED and says record shapes, coverage and reductions were verified. Validate any present checks file and retain its observed failures/counts; missing reports must remain visible without laundering malformed checks or erasing evaluated coverage.

3. **F-IR07 — escaping member subject paths accepted (IR-22; VA-001/VA-014, AV-E01, VAT-24).** Existing `observe.py:records` rejects check `subject_path` that fails `normalized_relative`. The new set reader tests only that it is a nonempty string. IR-22 substitutes `../outside.md` for one member check subject and is accepted with 0/OBSERVED. This does not execute a path traversal, but it admits an invalid legacy member locator and contradicts preservation of schema-1 meanings. Enforce the existing relative subject-path contract for members; logical integration locators retain their separately specified membership checks.

New expectations were retained before execution in `set-expectations.json` and `missing-report-integrity-expectation.md`. Exact candidate commands/results are in `attempt-03/<IR-id>/receipt.json`, stdout/stderr beside them, and `attempt-04/IR-23/receipt.json`. Inputs and previous attempts were not modified. All writes remained under this independent-review folder.

The positive and negative controls behaved as expected: IR-16 accepts a complete ordinary-member set with 19 applicable PASS and 10 justified adaptive NOT_APPLICABLE rows; IR-17 accepts honest unknown applicability with INCOMPLETE/evaluated18/total19/unknown1; IR-18 accepts required FAIL precedence over unknown applicability and advisory failure with the same counts; IR-19 rejects a tampered required total. These are synthetic record-integrity observations, not semantic endorsements of fixture skills.

Executed harnesses, both exit 0:

```powershell
python -B -X utf8 docs/plan/skill-adaptive-implementations/skill-validator/20260913T085122108787Z/independent-review/followup_review.py
python -B -X utf8 docs/plan/skill-adaptive-implementations/skill-validator/20260913T085122108787Z/independent-review/missing_report_probe.py
```

The original four-case retest has four expected outcomes. The eight new set probes have four expected outcomes and four mismatches, corresponding to the three findings above. No source package edits, native CLI task executions, operational binding tests, dependency installs or broader acceptance claims were made. Native behavior, full legacy suite execution and final delivered-byte readback remain outside this independent follow-up.
