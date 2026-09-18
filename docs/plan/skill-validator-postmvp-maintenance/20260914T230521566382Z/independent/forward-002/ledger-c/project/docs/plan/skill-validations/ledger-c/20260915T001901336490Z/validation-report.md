# ledger-c validation report

## Identity and conclusion

**Overall: INCOMPLETE. Assessment completed: true.** The Python helper performed the specified task in all 24 declared utility cases. No target defect was demonstrated. Native actor workflow, corrections/readback/delivery, and discovery remain NOT_RUN under current host effects restrictions. Primary validator self-review; no independent reviewer or cold actor was used.

- Run: `20260915T001901336490Z`
- Package digest: `7415f86d569107d72d5fdb70554f23e3fb14b334fb3d5572bdd77b3da4ec0376`
- Pinned rule-set digest: `1ea7010182df8ddf92dd9f64ae87e983e85b33fff5196654f3d69d6c1d8e838f`
- Specification digest: `66df398d2b01b2cf3d6ebc990d0032f7946f68bab13a40bf306b462416b83130`
- Builder readiness: **BLOCKED** by unperformed required capability evidence; proposal review: **not_needed**. No source change is proposed.

## Origin, sources and preservation

Explicit [specification](inputs/specification.md), observed history with unknown historical origin. [Origin record](origin-record.json), [exact snapshot](source/SKILL.md), [manifest](source-manifest.json), [source readback](observations/readback.stdout.txt), [after manifest](source-after-manifest.json). Both captured files are unchanged; no exclusions. Original specification, selected local rule sources, rules and source bindings rechecked unchanged in [input readback](observations/input-readback.json).

Rules were pinned before observations. [Sources](sources.json) include local AV policy and dated fallback guidance. Read-only official refresh redirected to [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills); returned excerpts are retained under inputs/official-refresh-*.txt. The initial response was dominated by navigation and Markdown retrieval failed. Later useful excerpts are supplemental; they did not replace pinned expectations. This report claims only selected snapshot/profile coverage, not comprehensive current-live standards compliance.

## Assessment dimensions

| Dimension | Outcome | Required evaluated/total |
| --- | --- | --- |
| standards | PASS | 8/8 |
| workflow | INCOMPLETE | 0/2 |
| instructions | INCOMPLETE | 4/5 |
| behavior | INCOMPLETE | 7/10 |

Total: **19/25** applicable required check rows evaluated, zero unknown applicability. Native scenarios are separate check rows, not extra successful helper cases. Adaptive-only rules and absent optional configuration are justified NOT_APPLICABLE. [Checks](checks.jsonl) and [machine assessment](assessment.json) retain all gaps. Enforcement recommendations: [no candidates](enforcement-recommendations.md).

## Findings and contextual instruction review

[Finding F-1786df21ab10c50e72385460032f889b2813783a6b6c07ec88239a5775ecde98](findings.json) records an evidence limitation, not a target implementation defect. The native CLI is present but even help attempted global temporary writes and reported access denied; no contained native host execution was established without prohibited configuration changes. [Capability details](observations/native-capability.md).

[Semantic review](observations/semantic-review.md) and [workflow map](workflow-map.json) trace input selection, invocation, validity/alias rejection, total-file creation, readback and error delivery. The input preservation/readback instructions are useful and retained. Inline scripts/total.py routing is real despite the conservative helper graph reporting no edge. The source-directory identity NOT_RUN in raw package output is independently resolved using the original ledger-c root and bound manifest. Raw observations remain unchanged.

## Trials and limits

**Helper behavior: 24/24 PASS.** Positive totals, negative numbers, empty arrays, zero, whitespace, integers beyond JavaScript's safe range, selected overwrite, nonarrays, bool/float/string/null/nested elements, malformed JSON, instruction-like data, missing input/arguments, --help, spaced paths, same-path and hardlink aliases. Invalid-input cases returned nonzero with useful stderr and created no new result. Every source and unrelated sentinel remained byte-identical. Output JSON contents were read back and compared with fixed independent expectations.

- [Frozen cases/oracles](trials/helper-suite/cases.json), [sealed plan](trials/helper-suite/plan.json), [24 per-case results with commands and streams](trials/helper-suite/work/results.jsonl), [summary](trials/helper-suite/work/summary.json).
- [Actual sealed runner receipt](trials/helper-suite/attempt-001/result.json): exit 0, no timeout, unchanged protected inputs, Windows Job cleanup VERIFIED. [Runner check](trials/helper-suite/check.stdout.txt), before/after manifests and all artifacts retained in attempt-001 and work. No retries.
- Eight [grader controls](trials/helper-suite/grader-controls.json) passed, including wrong totals, Boolean totals, absent results, source changes, unrelated writes and invalid-input output creation. These are grader checks, not target coverage.
- Python 3.10.11 Windows; target helper used `-S` to exclude site packages. Helper and whole suite limits: 120 seconds. [Evaluation bundle](evaluation-bundle.json) binds runtime, schema, fixtures, grader and results to exact inputs.
- [Native inventory](trials/native-inventory.json) and [planned obligations](trials/native-plan.json): positive, invalid-input and discovery NOT_RUN, selected 600-second limit; no native attempt launched. Description routing has a manual positive/two-near-miss review only, without blinded independent classification or discovery evidence.
- Atomic interruption, disk-full/output-permission errors, concurrent hostile path replacement and other Python/OS versions were not exercised. No universal performance, race safety or exhaustive runtime coverage claim. Framework line coverage/acceptance is not applicable to this supporting utility assessment; target line coverage was not measured.

## Proposed changes and next action

No revision-spec.md is warranted by observed target evidence. Preserve the original skill and specification. [Handoff](handoff.json) records BLOCKED execution readiness and no selected repair. To establish full workflow conformance, run fresh native positive, rejection, corrections and discovery observations in an already authorized environment that contains host effects. No installation, external mutation or permission change was attempted to force those observations.

Reports and evidence are development observations, not compiled-Rust framework acceptance. Record-integrity verification is delivered separately in observations/records.stdout.txt; it validates references and reductions, not semantic truth or native execution.
