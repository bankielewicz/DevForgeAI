# Focused finding validation — FAIL for assessed behavior

**All four QA findings are genuine and merit correction.** Each original reproducer failed again against unchanged delivered bytes, and an independently constructed fixture reproduced each mechanism. No repairs were made.

| Finding | Verdict | Severity | Repair priority |
| --- | --- | --- | --- |
| QA-01: Duplicate check executions inflate totals | CONFIRMED | major | First: record integrity |
| QA-02: Required handoff obligation disappears as N/A | CONFIRMED | major | First: record integrity |
| QA-03: Exact protocol value has no Unicode candidate | CONFIRMED | minor | Then: focused text scanner correction |
| QA-04: Premature fence closure corrupts resource edges | CONFIRMED | major | Then: focused text scanner correction |

## Findings and merit

### QA-01 — Duplicate check executions inflate totals

The helper accepts the same artifact across member/integration roles (including a Windows case alias) and accepts copied rows preserving the same run/check identity. D01/D02/D03 declare 87 required/evaluated rows although only 58 distinct check identities exist.

Misleading coverage and accepted invalid records. This does not prove a false native task success. Shared citations and distinct checks are valid controls, not defects.

Location: [captured source](source/scripts/adaptive_observe.py) line 112. Stable ID: `F-0b5c4676e917c304c39f8339e6536ba54a08ec05f7d410ab6c4c83a12791ddba`. Contract: VA-003, VA-014; AV-E01; VAT-24.
Fresh reproductions: D01, D02, D03. Controls: D04, D05. Exact expectations precede execution in [case plans](expectations-before-execution.json); H11 has [its separate plan](expectations-H11-before-execution.json).

### QA-02 — Required handoff obligation disappears as N/A

A required selected transfer is represented only by required NOT_APPLICABLE. The helper accepts PASS and 58/58, removing the required integration obligation. A valid required observation would produce 59 total; unavailable execution must remain NOT_RUN/INCOMPLETE.

Invalid full-set success can be accepted despite missing required integration assessment. This is record coverage validation, not an executed producer/consumer failure.

Location: [captured source](source/scripts/adaptive_observe.py) line 119. Stable ID: `F-451f9ac54c52d553ee8d83d14dd69b0487d7a66ed6da8003b8eebe25af0ff720`. Contract: VA-003, VA-014; AV-A10, AV-E01; VAT-04, VAT-05, VAT-24.
Fresh reproductions: H01. Controls: H02, H03, H04, H05, H06, H07, H08, H09, H10, H11. Exact expectations precede execution in [case plans](expectations-before-execution.json); H11 has [its separate plan](expectations-H11-before-execution.json).

### QA-03 — Exact protocol value has no Unicode candidate

Literal U+FF54 in JSON schema_version is unreported. All three fresh layouts and the original P08 return OBSERVED/exit 0 with no candidate; the required result is a located unresolved candidate and INCOMPLETE/exit 2, absent other failures.

A specific required scanner signal is missing. Severity is narrowed from prior major to minor: no runtime acceptance of the malformed protocol was demonstrated, and manual review or an exact downstream schema check can still reject it. It remains a required defect worth fixing.

Location: [captured source](source/scripts/text_resources.py) line 84. Stable ID: `F-423b36f0fa4378d0d426892377bea79335327a3b1507d05d7c5459de655252aa`. Contract: VA-004; AV-U01; VAT-06.
Fresh reproductions: U01, U02, U03. Controls: U04, U05, U06, U07. Exact expectations precede execution in [case plans](expectations-before-execution.json); H11 has [its separate plan](expectations-H11-before-execution.json).

### QA-04 — Premature fence closure corrupts resource edges

A fence-like code line with trailing nonspace content toggles the fence off. Literal example links become false missing-resource failures. F08 additionally reports line 3 inside code while omitting the genuine missing link on line 5 after the valid closer.

Both unsupported resource failures and missed real resource edges are reproduced. F08 exits 1 as expected but fails the content/line oracle, demonstrating why exit-only comparison is inadequate.

Location: [captured source](source/scripts/text_resources.py) line 107. Stable ID: `F-fb4a957d8ef5cf9a369515aa9a44ca736024f52c57fa25f06bdb25248953af48`. Contract: VA-005; AV-F05, AV-R01; VAT-08.
Fresh reproductions: F01, F02, F08, F09. Controls: F03, F04, F05, F06, F07, F10. Exact expectations precede execution in [case plans](expectations-before-execution.json); H11 has [its separate plan](expectations-H11-before-execution.json).

## Evidence and scope

- 33 fresh cases: **22 matched, 11 mismatched** the specification-derived expectations. The 11 mismatches are repeated manifestations of four findings, not eleven new findings.
- Four original replays: all four reproduce their previously reported failures. They are reported separately from fresh case counts.
- Fresh false-positive cases: F01, F02, F08, F09 (4). Missed required rejections/candidates/edges: D01, D02, D03, H01, U01, U02, U03, F08 (8). F08 belongs to both groups; these counts must not be added as distinct cases.
- Original replays: P07 false positive; R06/R07 missed rejections; P08 missed candidate. No native-model reliability rate is inferred.
- Independent installed jsonschema 4.24.0 audit: **42 record shapes and 180 reference occurrences verified**, including original R06/R07. Source package manifests and required dependency references were independently reconciled. Shared schemas are input data; semantic expectations derive separately from frozen specifications.
- **27/27 affected regression tests passed** (`test_adaptive.py`); installed quick_validate.py passed on exact captured bytes. Both are limited observations. The full historical 229-case suite was not repeated in this focused assessment; its prior result remains a prior claim, with no new repairs to qualify.
- Fresh Python line/branch coverage: **NOT_RUN**. The previous 67.7758% line measurement is not refreshed or relabeled as current coverage. Coverage improvement and full regression/acceptance are requirements of the later maintenance QA, not evidence of whether these four defects exist.
- Fresh-case conformance is 22/33 = 66.6667%, below 95%; each reproduced mandatory failure independently prevents a scoped PASS. Original replays and self-tests are not pooled to improve this percentage.
- Both specification hashes match. Target and loaded evaluator each remain 75 files with package digest `d51703237abb4d015fbed30f8f03ef93040603a4ea0ec57a623db61e3c71f4b1`; their helpers therefore remain self-review. Independent harnesses import no target test/helper functions as oracles.
- Native Windows Python 3.10, PyYAML 6.0.2. No WSL execution or checkout relocation; the added AGENTS.md performance guidance was read and followed.
- No candidate fixture writes were observed. The target, loaded evaluator, companion package, checker, AGENTS.md, specifications and selected prior-evidence files match final readback. Whole operational homes and historical trees were not captured.
- The CommonMark fence interpretation was checked against [CommonMark 0.31.2 §4.5](https://spec.commonmark.org/0.31.2/#fenced-code-blocks); a bounded paraphrase and retrieval identity are [retained](inputs/commonmark-notes.md). No full Markdown renderer certification is claimed.

## Remediation decision

Recommend the four focused fixes in [revision-spec.md](revision-spec.md). QA-01 and QA-02 are first priority because invalid coverage records can be accepted. QA-04 also deserves correction because the parser both invents and misses edges. QA-03 merits a localized scanner fix, with severity narrowed to minor; missing a candidate is not proof of runtime acceptance of an invalid protocol.

The proposal preserves public interfaces and closed schemas. It explicitly avoids banning shared citations, treating all Unicode as defects, rejecting valid FAIL/INCOMPLETE records, or suppressing real links to avoid false positives. No optional enhancement or broad coverage campaign is bundled.

A later authorized $skill-creator maintenance task must retain red tests, implement the selected corrections, and hand delivered bytes to fresh $skill-validator QA. Known provenance must be checked before changes; this assessment establishes an exact observed source capture, not generated/adopted custody. Proposal review and execution custody are separately represented in the handoff.

## Separate conclusions and remaining work

**Focused implementation conformity: FAIL. Finding-verification work: completed. Repairs: NOT_PERFORMED.** The four findings remain persistent on current bytes.

Native whole-workflow/resume, implicit activation, complete lifecycle integration, tokenizer availability, Linux behavior, installation and Rust qualification were not exercised. Their previous gaps remain open. Closing these four issues would not establish full package acceptance.

Review the proposed corrections; then authorize only the selected repair scope against its exact digest. Fresh QA must check unchanged reproducers, new controls, the full regression suite and required coverage measurements. See [command log](command-log.md), [finding matrix](finding-matrix.json), and [final input readback](final-input-readback.json).
