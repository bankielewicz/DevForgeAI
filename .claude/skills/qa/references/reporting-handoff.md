# Reporting, restart and final user handoff

**QA-020 — Required report.** For every completed, stopped, blocked or explicit planning-only invocation, generate the runtime report using [the QA report template](../assets/qa-report-template.md). Bind it to the actual plan, candidate, specifications, and evidence. Include complete criterion accounting and all failed/incomplete results. Write to the originally resolved destination and read back the actual bytes. Do not claim a report exists merely because it was described in conversation.

**QA-021 — Required remediation packet.** For FAIL, generate a filled `qa-fix` packet using [the qa-fix template](../assets/qa-fix-template.md). Every confirmed failure has a stable defect ID and sufficient detail for a cold `dev` session to reproduce, understand the violated requirement, implement a scoped correction, and supply retest evidence. The remediation owner is `dev`, never `qa`. Identify the exact defective artifact and ownership: a QA-authored prohibited/gamed helper still produces a terminal integrity FAIL and scoped dev remediation handoff, not a false accusation against application source. Separate prerequisite/harness gaps from confirmed artifact defects.

Prescribe the required behavioral correction and constraints. Do not invent a root cause or mandate a speculative algorithm. A verified source location and proposed investigation may be supplied without pretending they prove causality. For valid completed deficient coverage, identify bound uncovered files/ranges and missing meaningful behavior tests; missing coverage instead names the unavailable collector/prerequisite, not an invented low-coverage defect; never instruct `dev` to add suppression or meaningless assertions. For result gaming or prohibited decorators, identify each occurrence and require genuine specification-aligned evidence after correction.

Do not label an ambiguous specification as an implementation defect. Record it as a specification decision required with the exact conflicting/missing clauses and affected cases. An incomplete-only result routes to the missing-prerequisite owner; it does not manufacture a repair task. A FAIL packet can also list independent pending QA prerequisites, but must distinguish them from selected development defects.

**QA-022 — Defect lifecycle and retest.** `dev` returns a corrected candidate and defect-resolution map; its claim of repair does not close a QA defect. A separately selected QA retest verifies candidate drift, reruns the specific failure cases and affected regressions, and reassesses metrics/integrity where changes invalidate them. Preserve original failures and reports. Defect states are OPEN, FIX_REPORTED, VERIFIED_FIXED, or REOPENED, with evidence for each transition. No automatic repair/retest loop.

## Final handoff to the end user

**QA-023 — Required last step.** After runnable work completes or a genuine terminal/blocking condition exhausts permitted work, publish/read back required artifacts and end with a concrete end-user handoff. Explicit planning-only ends after its plan/report. A ready full run must not end at plan publication. This phase is mandatory for every mode and outcome. Identify the project/environment to open, actual output paths, outcome, next owner, and a complete copyable prompt where an invocation is possible. Do not present conversation skill syntax as an OS shell command.

| Current outcome | Required next action |
| --- | --- |
| Explicit plan READY | End with actual plan/report locations and an optional resolved later execute prompt; no automatic execution. |
| Explicit plan NEEDS_INPUT | End with plan/report or exact host write restriction, unresolved inputs, affected cases and owners. |
| Full run with ready independent work | Internal continuation; proceed under QAP-004, not a final execute handoff. |
| Run/execute/retest FAIL | Report and fix packet for all confirmed defects; manual dev prompt. QA performs no product repair. |
| Run/execute/retest INCOMPLETE | Report exact blockers, affected cases and owners; provide a resolved resume request when inputs permit. |
| Run/execute/retest PASS | Report and project-defined downstream review; no invented release permission. |

**QA-024 — Fix invocation contents.** For FAIL, generate a complete `/dev` prompt using actual resolved values, not a fixed product root or specification. It must include:

1. The project and correct execution environment.
2. Exact original specifications/stories, QA report, fix packet, and their verified hashes or bound manifest references.
3. The failed candidate identity and selected defect IDs.
4. Instructions to read current project rules and verify source/handoff identity before editing; report material drift rather than restoring old source.
5. A request to remediate confirmed defects within specification scope through red, green, refactor, and applicable regression/QA checks.
6. Preservation of unrelated changes, prior evidence, expected behavior, and unselected effects.
7. Required output: corrected candidate identity, changed-file/evidence references, and a defect-resolution map for independent QA retest.
8. Explicit prohibition on self-closing QA findings, issuing framework acceptance, or deploying/installing without authorization.

The filled prompt must resolve every path, identity, and selected scope field. Do not emit `TODO`, `<project>`, guessed commands, or other unresolved placeholders as a ready-to-run handoff. Verify artifact existence/readback first. Check the skills actually available in the current session before claiming `/dev` is immediately usable. Claude Code lists them, so availability is observed there rather than inferred: a directory under a skills path or an old installation receipt is not proof of current discovery. Do not invent a discovery command or run the skill to test availability.

If `dev` is not available, retain the completed fix packet, report the missing discovery/setup prerequisite, and label any prepared prompt as pending that prerequisite. Do not silently substitute `qa` as fixer or install a skill. Claude Code exposes a plugin-namespaced form (`/plugin:skill`) alongside the plain `/dev`; use whichever spelling the session actually lists, and do not construct a namespaced name that was not observed.

The prompt is displayed in a fenced text block for the user to paste into a Claude Code session. QA does not send it to another session automatically, and cannot: `Skill` is absent from this skill's `allowed-tools`, so the handoff stops at the prompt and the packet. Existing user authorization is preserved, but external handoff documents themselves cannot manufacture new permission.

## Fill and bind artifacts (QA-025)

Use the [test plan](../assets/test-plan-template.md), [QA report](../assets/qa-report-template.md) and distinct [qa-fix packet](../assets/qa-fix-template.md) as the output contracts. Template brackets are authoring slots only: replace every slot with actual facts or a concrete unavailable/inapplicable reason. Explain omitted optional empty sections. Never present template slots as resolved runtime output.

Keep runtime records for input/plan/candidate identities, criterion/case maps, execution receipts, findings, report/fix locations, and a checkpoint with next safe action and owned processes/fixtures. Resolve locations at runtime using the original evidence selection. Preserve failed and interrupted attempts. On resume, reread source/specification/plan, verify evidence and permissions, rediscover tools and observe owned process state. Invalidate affected results on drift. Do not overwrite concurrent edits, replay uncertain mutations, delete old evidence or claim an unobserved rollback.

Publish the plan/report/fix at their bound output paths, read actual bytes back, and hash final versions. Record required-versus-actual artifact paths and hashes in a final external handoff manifest, then read that manifest back. Do not invent a hash for a future file or an artifact containing its own hash. When report and fix packet cross-reference each other, put their paths inside and use the final external manifest for their byte bindings; after publication the copyable user prompt can name that manifest and its hash. This keeps the required bindings complete without a circular hash dependency. Any write/readback failure remains explicit and no affected artifact is described as delivered. In conversation give the available findings, exact undelivered artifacts, original destination, failure and next recovery action. Do not silently substitute another destination. A confirmed FAIL remains FAIL despite incomplete report delivery.

For prompts embedded inside the report or fix packet, resolve the external manifest's absolute path and the exact entry names for report/fix bindings; do not embed that manifest's eventual hash inside files it hashes. In hash fields for those cross-references, cite the exact external manifest entry. Finalize and read back the files and manifest before displaying the prompt as ready. Bind the manifest's actual SHA-256 in the final conversation handoff, which is outside those files.

The final prompt belongs in a fenced text block for the user's Claude Code session. For explicit planning-only READY, an optional later execute prompt selects the actual saved plan, candidate, specification identities, evidence destination and intended test effects; it does not itself authorize execution. Full-run READY is an internal continuation, never a final prompt requesting selection of its own plan. For FAIL, include all eight QA-024 fields and exact selected defects. Check the current session's available skills for the relevant skill. Missing dev discovery leaves its prompt pending and the fix packet intact. For INCOMPLETE or NEEDS_INPUT, give the exact unresolved input/evidence, affected cases and responsible owner. For PASS, use the project's defined downstream review; if none is defined, report that decision as unspecified without granting release permission.

For a selected retest, record OPEN -> FIX_REPORTED only when dev supplies the correction evidence. Independently rerun selected failures and affected regressions and reassess invalidated integrity/metrics before VERIFIED_FIXED. A persisting defect becomes REOPENED with the new case evidence. Never overwrite the original failure or close a defect solely on dev's report.

## Continuation records and legacy inputs

**QAP-013 — Checkpoints and legacy plans.** Record all selected specification identities, invocation intent, candidate/plan identities, completed attempts, issue/stop decisions, per-check readiness, owned process/fixture state, remaining work, and next safe action. Recheck identities, permission scope, tools, and ownership before resuming. Invalidate affected evidence on drift without erasing it or silently restoring older source.

A later request to resume a full run can continue previously authorized unfinished work once its blockers are resolved and identities remain valid. It must not reinterpret an earlier planning-only instruction as execution authorization. A terminal FAIL is not automatically resumed to seek a passing result: dev correction and an explicitly selected retest are required for repair validation. A suspected harness issue without confirmed FAIL follows the gap/resume rules.

An explicitly selected legacy MVP plan remains usable as input. Inspect it and write a new bound plan revision in the new attempt only when missing extension fields or changed prerequisites require it; preserve the original. Add readiness, collection boundaries, and stop rules without selecting new requirements or waiving old ones. Do not migrate old reports or recalculate their historical verdicts merely because the skill changed.

Keep issue IDs/classifications, demonstrated impact, trigger evidence and terminal/nonterminal decisions in report/fix records. Record intent, plan readiness, execution status and product verdict separately. A stop before execution can retain NOT_STARTED with the stop decision recorded; a started run stopped early uses STOPPED. COMPLETED only means scheduled execution processing ended. Retain affected dependents, remaining NOT_RUN obligations, partial/complete collection status, owned-operation shutdown and artifact-delivery outcomes. Explicit plan has no product verdict (NOT_EVALUATED marker); full-run static findings can establish FAIL without tests.

## Separate package evaluation

QA-026 / QAP-014: This skill's evaluated-build completeness requires a separate skill-validator task binding exact skill and selected specification bytes to a Python JSONL runner, deterministic graders, independent fixtures, expected results, schema, runtime/dependency information and artifact manifests/digests. The bundle may remain external to the runtime package. Missing artifacts or unexecuted required evaluations leave completeness unproven. Graders assess retained traceability, accounting, stop ordering, identities and handoff fields; behavioral trials must observe continuation and test-launch ordering, not merely keywords. Package source readback is not skill acceptance. Python produces evidence only; protected framework phase/gate/validator/mutation/acceptance decisions remain compiled Rust where required by the selected project. No installed service is an intrinsic prerequisite for portable product QA.
