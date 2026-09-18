# Updated validator / builder compatibility

**The updated validator supports basic handoffs, but does not yet fully meet the updated builder contract. Assessment: FAIL.** Five defects are demonstrated by eight differential counterexamples. No package was changed.

Validator digest: `d51703237abb4d015fbed30f8f03ef93040603a4ea0ec57a623db61e3c71f4b1` (75 files, loaded and development copies identical). Builder development digest: `338c70995e72637e0ce84991be110d6a371ab6965faf4009d570156ea0e13cf2` (43 files, unchanged since the earlier enhancement). The operational builder has the same 43 common files plus 26 legacy evaluation/test files; its distinct digest is `399fcd69e9560a0f4978e185b2d1dd4615e460574d8989d6ad4e8451b00d7777`. No operational cleanup was attempted.

## Confirmed findings

1. Update review rejects valid changed-input PROPOSED and accepts incorrect NO_CHANGE/nonvariant reviews.
2. Parent inventory requires references/adaptive-contract.md even for ordinary cores with an explicit complete SKILL.md table.
3. CRLF fenced parent inventories are rejected.
4. Delivered descriptor role and parent lineage are not bound to the selected proposal.
5. A descriptor can name a parent requirement absent from its contract disposition map.

These are reader implementation gaps: all 14 shared schemas are identical. The default validator test suite passed 229 tests but did not catch these cross-package cases.

## Actual coverage

| Case | Expected exit | Builder | Validator | Validator result |
| --- | --- | --- | --- | --- |
| baseline-variant | 0 | 0 | 0 | PASS |
| changed-equivalent-proposed | 0 | 0 | 1 | FAIL |
| changed-false-no-change | 1 | 1 | 0 | FAIL |
| review-nonvariant | 1 | 1 | 0 | FAIL |
| ordinary-parent | 0 | 0 | 1 | FAIL |
| crlf-parent | 0 | 0 | 1 | FAIL |
| wrong-delivered-role | 1 | 1 | 0 | FAIL |
| missing-parent-disposition | 1 | 1 | 0 | FAIL |
| actual-partial-custody-subset | 0 | 0 | 0 | PASS |
| actual-native-manual-request | 0 | not repeated | 0 | PASS |
| full-set | 0 | 0 | 0 | PASS |
| wrong-parent | 1 | 1 | 0 | FAIL |
| false-full-omission | 1 | 1 | 1 | PASS |

Positive handoff evidence includes the actual prior cold builder single-skill manual request and the actual per-member-custody partial-set request consumed unchanged by the updated validator. Full-set acceptance is additionally demonstrated with a retained-variant synthetic fixture. Intake is now exercised against the enhanced validator; complete new adaptive authoring-to-assessment and product producer/consumer workflows are still unverified.

The cold validator task independently detected the role mismatch in a partial message, then timed out at 120 seconds before final delivery. Its first attempt failed parent-sandbox app-server initialization; the approved retry preserved normal child workspace-write controls. Both attempts remain. No completed native or implicit-discovery PASS is claimed.

Final record checks passed: both schema-1 member runs and the closed supplemental selected-pair report are internally consistent. Overall FAIL takes precedence over retained NOT_RUN coverage. Required evaluated/total: 52/65; unknown applicability 0. This is a diagnostic pair, not an installed or generated operational set.

## Evidence and proposed next work

- [Validator report](../../skill-validations/skill-validator/20260913T135752395202Z/validation-report.md) and [findings](../../skill-validations/skill-validator/20260913T135752395202Z/findings.json).
- [Proposed complete revision](revision-spec.md): VC-001 through VC-005; no repairs authorized by this report.
- [Exact commands/results](command-log.md), [differential results](compatibility-results-round2.json), [additional results](additional-results.json), [independent review](independent-review.md), [set assessment](supplemental/set-assessment.json).

Initial differential fixtures used Windows path sort instead of sorted manifest-row paths; that rejected setup is preserved. Corrected fixtures were created under trials-round2, leaving original attempts intact. Source, operational copies, specifications and selected historical inputs were not edited. No installation, hooks, CI, binding setup or Rust qualification. Future revision must use the development validator package and a fresh validation run.
