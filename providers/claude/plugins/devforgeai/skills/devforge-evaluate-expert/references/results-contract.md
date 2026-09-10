# Result and handoff contract

This is the record shape for an evaluation and its return to the builder. The JSON schema identifiers below name these local record shapes; they are not DevForge CLI gate schemas, and no command in the CLI validates them.

## Identity and storage

Use the authority-selected evaluation directory - for example the assigned evaluation root's `.poc/claude/<skill>-workspace/<run-id>` - and keep every report outside the evaluated candidate.

Every input and evidence locator is `{path, sha256}`, optionally with `kind`, `line`, `section` and `description`. The digest covers complete exact file bytes. Relative paths inside a record resolve from that record's own directory. Freeze a record before anything downstream hashes it. **No record contains its own complete-byte digest**, and a handoff never lists itself among its own outputs.

Preserve the original candidate source, the actual installed files, the baseline, the cases, fixtures, rubric, selected contracts, reviewer outputs and the raw native evidence separately. Changed bytes invalidate the observations that depended on them. An evidence reference confers no authority.

## Files and sequence

Workspace preparation has its own earlier allocation, so the sequence below governs measured execution rather than worktree creation. Preserve allocation → setup → plan → run references without cycles.

1. The governing specification - supplied by the builder, or the actual selected equivalent.
2. `test-cases.json` - versioned requirement-derived cases, multi-turn inputs, expected and forbidden behaviour, artifact assertions, baseline treatment, repetitions and held-out designation. Frozen before measuring.
3. `validation-plan.json` - binds the specification, rubric, cases and contract references, the scope, owner, runtime arrangement, budget, baseline and every expected check, attempt and arm.
4. Structural observations - the manual rows from [missing DevForge CLI capabilities](missing-rust-capabilities.md), plus any runner observations file, each labelled with its method.
5. `ai-review.json` - independent criterion records R01–R10. Static semantic review.
6. A separate `run-manifest.json` and `case-grade.json` per native case, arm and attempt. Never reuse writable context across attempts.
7. `validation-results.json` - one result per planned check, with raw evidence references and case-grade references for native outcomes.
8. `verification-results.md` and `skill-enhancement-spec.md` - the human-readable report and the builder-ready change specification.
9. `handoff.md` - references the completed outputs and assigns the next task. Its own digest is delivered externally.

There is deliberately no decision-receipt file in this sequence. Evidence reduction is one of the two capabilities not implemented in the DevForge CLI, so the disposition is adjudicated against this contract directly and the report records that.

Keep the source and installed manifests distinct. The plan's `candidate_root` is the frozen source being evaluated; native run manifests separately bind the actual installed package.

## Outcomes and disposition

| Outcome | Exact meaning |
| --- | --- |
| `PASS` | The named condition was observed to satisfy its predefined requirement, with complete evidence for that claim. |
| `FAIL` | An observed result violates a predefined applicable requirement. |
| `NOT_RUN` | A planned observation was not attempted. |
| `COULD_NOT_RUN` | An attempted or prerequisite-dependent observation could not be established; the cause is recorded. |
| `NOT_APPLICABLE` | Explicitly excluded from the frozen scope, with a reason. It cannot replace missing required work. |

Never blend structure, review, A, B and C into one percentage. Behaviour stays `NOT_EVALUATED` while no complete behavioural conclusion is supported. A reported `FAIL` may coexist with incomplete coverage, so a consumer must read every row rather than assuming a single headline covered them.

A planned check's expectation is one of:

- **pass** - an applicable required assertion that must yield `PASS`.
- **observation** - a baseline comparison that must be completed. Either `PASS` or `FAIL` supplies comparison evidence, and a failing baseline does not itself fail the candidate.
- **excluded** - a documented scope exclusion whose result must be `NOT_APPLICABLE`. It cannot eliminate an entire required evidence group.

Required evidence groups are **intake**, **structure**, **ai_review**, **C**, **B** and **A**. Include each rubric criterion as `AI-R01` through `AI-R10`; an inapplicable criterion needs a predefined exclusion reason. Every native attempt and arm gets a unique check ID and attempt ID before execution. An enhancement also carries regressions covering the prior findings and the behaviour being preserved.

Adjudication, performed by hand: any applicable `FAIL` produces **revise**; otherwise missing or unavailable required observations produce **insufficient evidence**; all required observations passing produces **suitable for the stated scope**. A missing result is `NOT_RUN`. A missing or changed referenced file, or an inconsistent record, makes that observation `COULD_NOT_RUN`. An expected baseline `FAIL` counts as a completed observation while its raw `FAIL` stays visible.

A document's status - draft, in review, accepted - external adoption, structural freshness and behavioural outcome are separate facts. *Suitable for the stated scope* is a recommendation, not acceptance.

## Native grade binding

Run manifests use `devforge.skill-run/v1` with the extensions `case_id`, `attempt_id`, `arm` and `transcript_sha256`. Keep the original client output intact and reference it rather than rewriting it into a tidier transcript. Source, installed, baseline, case and fixture identities, runtime, context isolation and the execution reference stay populated for observed runs.

Case grades use `devforge.skill-case-grade/v1`. The manifest's `outcome` and the grade's `overall` are the final observed case outcome, distinct from the terminal's raw exit status. The observation fields record raw completion and exit, target selection, actual resource consultation and its evidence. A successful process is not a case `PASS`.

Grade named behaviour, artifact delivery, constraints and activation separately. A dimension is `NOT_APPLICABLE` only when genuinely outside that case's purpose, with the reason. Compute the case outcome from all applicable required assertions and complete observation; never average away a failed requirement. Record short evidence-based rationale, not hidden reasoning.

## Findings and severity

Each finding carries a stable `F-###` ID, a type of `defect`, `enhancement` or `evaluation_gap`, criterion or requirement IDs, the affected revision and file or section, evidence locators, confidence and uncertainty, impact, a recommendation and the affected case IDs.

| Severity | Meaning |
| --- | --- |
| `BLOCKER` | The candidate cannot be safely or meaningfully exercised, violates an authority boundary, or has a package defect preventing the required operation. |
| `MAJOR` | A required behaviour, deliverable or constraint is demonstrably wrong. |
| `MINOR` | A contained defect with a narrower demonstrated consequence. |
| `ADVISORY` | An optional improvement or a new proposal; it does not by itself fail an accepted requirement. |

Choose severity from the demonstrated consequence, not from a criterion's label. Separate an unavailable runtime from a target defect. Uncertainty and disagreement never become a fabricated failure, and a required failure still needs correction whatever its severity.

## Builder remediation contract

`skill-enhancement-spec.md` uses `artifact_type: skill-enhancement-spec` inside the shared `devforge.artifact/v1` envelope. This is a paired authoring extension, not an assertion that any CLI validates it.

For each proposed `CHG-###`, give the finding IDs, the exact source identity, the accepted requirement versus a new proposal, the evidence and reproduction, the bounded desired behaviour, the file and section targets, the behaviour to preserve, the forbidden scope changes, the acceptance conditions and the affected reruns - enough to implement without replaying the discovery conversation.

An unknown cause becomes a bounded investigation task with a question and an evidence target. Do not fabricate a patch. A baseline, candidate or runtime problem may need evaluation repair rather than a target change, and where the evidence supports no target edit, say so explicitly.

The builder verifies the selected identities, retains the old candidate, resolves consequential ambiguity and applies only authorised changes, reporting the changed files and the new candidate identity without running validation. This skill then assesses the new revision and closes a finding only with new matching evidence. Preserve the finding history; never overwrite an earlier `FAIL`.

## Required closure

A complete delivered evaluation has a saved report and a builder specification even when it was blocked and even when no changes are recommended. Each missing observation has a cause and a next owner. No acceptance label, successful command, numeric score or completed template substitutes for the required evidence.
