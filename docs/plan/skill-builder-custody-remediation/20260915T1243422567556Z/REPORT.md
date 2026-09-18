# Skill-builder remediation result

## Outcome

**Confirmed custody bug: repaired. Final deterministic Windows/Linux regression: PASS. Selected generated-skill behavior: PASS with execution-method limits. Complete native workflow qualification: INCOMPLETE.**

The development package now rejects the demonstrated design-to-legacy downgrade before destination writes. The repair also rejects reuse of failed stages, supplies fresh-run recovery guidance, and prevents a first-path integrity failure from leaving an empty occupied destination. Source action: edited; operational skills and installation were not changed.

## Changes

The five changed development files are scripts/authoring.py, references/authoring.md, references/evidence-format.md, references/regeneration.md and package-manifest.json. See [implementation report](implementation-report.md), changes.patch, changes.json and before/delivered snapshots.

The internal stage-integrity receipt binds the original mode, run/name and origin bytes. Begin writes/readbacks it before STAGED. Publication checks it before legacy/design dispatch, before each changed path, after delivery and through baseline/handoff publication. Failures preserve actual effects and unsuccessful attempts. These are editable consistency records, not protected authority.

Compatibility consequence: pre-revision staged records with a design_capture_requested marker but no integrity receipt require a fresh linked run. Canonical older no-marker/no-design stages, fresh no-design calls, published historical baselines and closed validator packet schemas retain their specified behavior. No old evidence or baseline was rewritten.

## Final-source deterministic evidence

| Platform | Required cases passed | Executed lines | Executed-line coverage | Branch coverage |
| --- | --- | --- | --- | --- |
| Windows, Python 3.10.11 | 319/319, 100% | 2202/2302 | 95.65595134665509% | 89.69465648854961% |
| Ubuntu/WSL2, Python 3.12.3 | 319/319, 100% | 2202/2302 | 95.65595134665509% | 89.69465648854961% |

Both final collections include all eight shipped Python files, including the runtime asset and locally adapted metadata/scaffolding helpers, with no line exclusions or skipped required cases. Each platform has its own disjoint case inventory, JSONL observations, deterministic grade, source hashes and coverage. The 638 required platform-case executions all pass; no cross-platform averaging qualifies an untested target. These figures describe the deterministic regression scope, not the separate native workflow cases below.

Windows evidence: [REPORT-V3.md](regression/REPORT-V3.md) and [independent grade](regression/v3-combined/independent-grade.json). Linux evidence: [combined grade](linux-regression-002/regression/linux-combined/independent-grade.json) and linux-regression-002/REPORT.md. Both bind the same final package bytes; source and archive verification accompany the results.

Covered workflows include creation/publication, focused editing/regeneration, imports, adoption, adaptive operations, metadata, source/contract drift, invalid records, missing/corrupted receipt fields, legacy compatibility, write/interruption failures, destination preservation and runtime binding checks. Assertions examine actual returned states, files, hashes and readback. Independent [repair review](repair-review.md) found no additional substantiated source defect.

## Generated-skill behavior

The previously authored meeting-actions skill passed seven distinct requirement-derived behavior cases: missing fields, uncertainty, conflicting notes, Markdown escaping, a literal Unicode/spaced file destination, failed delivery to an existing directory, and preserving input when the output path equals it. [Independent supplemental report](generated-behavior/supplement-001/REPORT.md).

Four chat cases used the native CLI with the exact skill instructions provided. Three file cases used an independent subagent followed by independent artifact/response review. Original native file attempts remain blocked/incomplete. Raw subagent command receipts were unavailable to the final reviewer; delivered/preserved bytes and the returned response were independently checked. This qualifies the seven selected behaviors, not native CLI file execution, arbitrary generated skills, or generation by the final repaired builder.

## Native authoring outcomes

| Trial | Observed result | Qualification |
| --- | --- | --- |
| Windows simple, explicit source | 120.547-second timeout after staging; no delivered skill/handoff | INCOMPLETE; earlier V1 source fixture, not final-byte qualification |
| Windows branching, implicit discovery, final V3 | 120.469-second timeout; no delivered skill | INCOMPLETE |
| Linux simple, explicit source, final V3 | Exit 0; valid authored skill, baseline, PUBLISHED readback and manual handoff artifacts; final reply had a malformed/wrong path and omitted required handoff details | Artifact publication PASS; user-facing completion FAIL |
| Linux branching, implicit discovery, final V3 | 120.040-second timeout; no delivered skill | INCOMPLETE |

None of the four cases qualifies the complete requested cold authoring workflow. The [native assessment](native/native-report.md) records implicit selection/source loading on both platforms separately from complete delivery. Native receipts, raw JSONL, exact prompts, source manifests and owned-process cleanup are retained under native/ and linux-campaign-001/. Timeouts are execution ceilings, not demonstrated builder performance defects. The Linux simple final reply is an observed execution failure; the source already requires actual destination, status and handoff, so this run did not invent another instruction rule or claim a proven source cause.

Remaining work is native end-to-end qualification: investigate the incomplete authoring paths and final-response compliance, then select fresh bounded trials under an explicit execution budget. No automatic timeout retry was performed. Protected Rust/framework acceptance remains NOT_EVALUATED.

## Retained attempts and environment limits

The original failing review, selected repair proposal and pre-repair source remain unchanged. Red/green evidence and all failed intermediate attempts are retained. Earlier-source coverage never contributes to the final-source totals.

Two legacy fault injectors assumed the destination directory existed before the callback. After the repair moved directory creation, those callbacks failed to create their intended competing-write/unreadable-directory condition. The independent reviewer confirmed the setup issue; fresh copies now create that directory inside the injectors while preserving the original assertions. The failed V3 attempt remains in place.

Native Windows runs use PowerShell and the discovered Python/Codex executables on C:. Linux regression runs use hash-verified disposable /tmp source/fixture snapshots of the selected Windows package, then copy evidence back; this does not select or modify another checkout. Initial Linux setup reported success but its /tmp snapshot was absent in the next WSL invocation, so three launch attempts executed no tests. Those errors are preserved in linux-campaign-001. The successful linux-regression-002 keeps preparation, execution and archival within one WSL invocation. No cause for the disappearing temporary state is asserted.

Some native launches first encountered sandbox access denial; escalated attempts and interrupted approval waits are separately retained. No failed command, timeout, wrapper exit, model-written status or structural check was promoted to complete acceptance.

## Readback and delivery

The final static checks cover skill-creator quick_validate.py, exact package manifest, local Markdown links and Python parsing. Source before/after manifests, a delivered snapshot, changes.patch, preservation.json and artifact-manifest.json retain exact bytes and scope. The artifact manifest excludes itself and records links/junctions without traversing them. Python JSONL runners, graders, case inventories, schemas, fixtures, runtime/dependency records and coverage data are included as evaluation evidence.

This report provides the implemented repair and measured results. It does not claim that all four originally listed areas have complete native/framework acceptance.
