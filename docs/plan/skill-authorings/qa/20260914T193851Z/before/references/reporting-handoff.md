# Reporting, restart and final user handoff

**QA-020 — Required report.** Generate the runtime report using [the QA report template](../assets/qa-report-template.md). Bind it to the actual plan, candidate, specifications, and evidence. Include complete criterion accounting and all failed/incomplete results. Write to the originally resolved destination and read back the actual bytes. Do not claim a report exists merely because it was described in conversation.

**QA-021 — Required remediation packet.** For FAIL, generate a filled `qa-fix` packet using [the qa-fix template](../assets/qa-fix-template.md). Every confirmed failure has a stable defect ID and sufficient detail for a cold `dev` session to reproduce, understand the violated requirement, implement a scoped correction, and supply retest evidence. The remediation owner is `dev`, never `qa`.

Prescribe the required behavioral correction and constraints. Do not invent a root cause or mandate a speculative algorithm. A verified source location and proposed investigation may be supplied without pretending they prove causality. For low coverage, identify uncovered files/ranges and missing meaningful tests; never instruct `dev` to add suppression or meaningless assertions. For result gaming or prohibited decorators, identify each occurrence and require genuine specification-aligned evidence after correction.

Do not label an ambiguous specification as an implementation defect. Record it as a specification decision required with the exact conflicting/missing clauses and affected cases. An incomplete-only result routes to the missing-prerequisite owner; it does not manufacture a repair task. A FAIL packet can also list independent pending QA prerequisites, but must distinguish them from selected development defects.

**QA-022 — Defect lifecycle and retest.** `dev` returns a corrected candidate and defect-resolution map; its claim of repair does not close a QA defect. A separately selected QA retest verifies candidate drift, reruns the specific failure cases and affected regressions, and reassesses metrics/integrity where changes invalidate them. Preserve original failures and reports. Defect states are OPEN, FIX_REPORTED, VERIFIED_FIXED, or REOPENED, with evidence for each transition. No automatic repair/retest loop.

## Final handoff to the end user

**QA-023 — Required last step.** After plan/report/fix publication and readback, end with a concrete end-user handoff. This phase is mandatory for every mode and outcome. Identify the project/environment to open, actual output paths, outcome, next owner, and a complete copyable prompt where an invocation is possible. Do not present conversation skill syntax as an OS shell command.

| Current outcome | Required next action |
| --- | --- |
| Plan READY | Provide a resolved prompt selecting this plan and candidate for a later QA execute invocation. |
| Plan NEEDS_INPUT | Name the exact decisions/inputs needed; do not present the plan as executable. |
| Execute/retest FAIL | Hand back to `dev` with the QA report and fix packet. QA performs no product repair. |
| Execute/retest INCOMPLETE | Identify the actual missing prerequisite/evidence and its owner; no invented development defect. |
| Execute/retest PASS | Provide the project's defined downstream review/acceptance handoff, without inventing release permission. |

**QA-024 — Fix invocation contents.** For FAIL, generate a complete `$dev` prompt using actual resolved values, not a fixed product root or specification. It must include:

1. The project and correct execution environment.
2. Exact original specifications/stories, QA report, fix packet, and their verified hashes or bound manifest references.
3. The failed candidate identity and selected defect IDs.
4. Instructions to read current project rules and verify source/handoff identity before editing; report material drift rather than restoring old source.
5. A request to remediate confirmed defects within specification scope through red, green, refactor, and applicable regression/QA checks.
6. Preservation of unrelated changes, prior evidence, expected behavior, and unselected effects.
7. Required output: corrected candidate identity, changed-file/evidence references, and a defect-resolution map for independent QA retest.
8. Explicit prohibition on self-closing QA findings, issuing framework acceptance, or deploying/installing without authorization.

The filled prompt must resolve every path, identity, and selected scope field. Do not emit `TODO`, `<project>`, guessed commands, or other unresolved placeholders as a ready-to-run handoff. Verify artifact existence/readback first. Check the host's actual available skill catalog or supported skill selection mechanism before claiming `$dev` is immediately usable. A directory or old installation receipt alone is not proof of current host discovery. Do not invent a discovery command or run the skill to test availability.

If `dev` is not available, retain the completed fix packet, report the missing discovery/setup prerequisite, and label any prepared prompt as pending that prerequisite. Do not silently substitute `qa` as fixer or install a skill. Namespaced plugin syntax must be verified on the actual host before use; no assumed Claude-style namespace.

The prompt is displayed in a fenced text block for the user to paste into a Codex conversation. QA does not send it to another session automatically. Existing user authorization is preserved, but external handoff documents themselves cannot manufacture new permission.

## Fill and bind artifacts (QA-025)

Use the [test plan](../assets/test-plan-template.md), [QA report](../assets/qa-report-template.md) and distinct [qa-fix packet](../assets/qa-fix-template.md) as the output contracts. Template brackets are authoring slots only: replace every slot with actual facts or a concrete unavailable/inapplicable reason. Explain omitted optional empty sections. Never present template slots as resolved runtime output.

Keep runtime records for input/plan/candidate identities, criterion/case maps, execution receipts, findings, report/fix locations, and a checkpoint with next safe action and owned processes/fixtures. Resolve locations at runtime using the original evidence selection. Preserve failed and interrupted attempts. On resume, reread source/specification/plan, verify evidence and permissions, rediscover tools and observe owned process state. Invalidate affected results on drift. Do not overwrite concurrent edits, replay uncertain mutations, delete old evidence or claim an unobserved rollback.

Publish the plan/report/fix at their bound output paths, read actual bytes back, and hash final versions. Record required-versus-actual artifact paths and hashes in a final external handoff manifest, then read that manifest back. Do not invent a hash for a future file or an artifact containing its own hash. When report and fix packet cross-reference each other, put their paths inside and use the final external manifest for their byte bindings; after publication the copyable user prompt can name that manifest and its hash. This keeps the required bindings complete without a circular hash dependency. Any write/readback failure remains explicit and no affected artifact is described as delivered.

For prompts embedded inside the report or fix packet, resolve the external manifest's absolute path and the exact entry names for report/fix bindings; do not embed that manifest's eventual hash inside files it hashes. In hash fields for those cross-references, cite the exact external manifest entry. Finalize and read back the files and manifest before displaying the prompt as ready. Bind the manifest's actual SHA-256 in the final conversation handoff, which is outside those files.

The final prompt belongs in a fenced text block for the user's Codex conversation. For READY, select the actual saved plan, candidate, specification identities, evidence destination and intended test effects; this proposes a later execute invocation and does not authorize it itself. For FAIL, include all eight QA-024 fields and exact selected defects. Check the current host catalog or supported selection mechanism for the relevant skill. Missing dev discovery leaves its prompt pending and the fix packet intact. For INCOMPLETE or NEEDS_INPUT, give the exact unresolved input/evidence, affected cases and responsible owner. For PASS, use the project's defined downstream review; if none is defined, report that decision as unspecified without granting release permission.

For a selected retest, record OPEN -> FIX_REPORTED only when dev supplies the correction evidence. Independently rerun selected failures and affected regressions and reassess invalidated integrity/metrics before VERIFIED_FIXED. A persisting defect becomes REOPENED with the new case evidence. Never overwrite the original failure or close a defect solely on dev's report.
