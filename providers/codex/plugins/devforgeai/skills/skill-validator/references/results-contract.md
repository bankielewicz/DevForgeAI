# Result and handoff contract

This is the paired skill-builder/skill-validator authoring contract. JSON schema identifiers below identify these local record shapes; they are not new DevForge CLI gate schemas. The bundled helper checks only the fields documented for it.

## Identity and storage

Use an authority-selected evaluation directory, for example the assigned provider evaluation root's .poc/codex/<skill>-workspace/<run-id> directory. The example is a layout, not permission to pick an unassigned root. Keep reports outside the evaluated source.

Every input/evidence locator is {path, sha256}; optional kind, line, section and description fields explain the reference. SHA-256 covers complete exact file bytes. Relative paths in a JSON record resolve from that record's directory. Freeze records before downstream references hash them. No record includes its own complete-byte hash.

Preserve original candidate source, actual installed files, baseline, cases, fixtures, rubric, selected contracts, reviewer outputs and raw native evidence separately. Changed bytes invalidate dependent observations. Evidence references do not confer authority.

## Files and sequence

Workspace preparation has an earlier independent allocation: [workspace-allocation.json](../assets/workspace-allocation.json) freezes repository/common-directory/base, bounded count, destinations, permitted writes and authorization; [environment-setup.json](../assets/environment-setup.json) records actual preparation with nullable plan_ref and no invented attempts. Native inputs can remain pending. The experiment sequence below must be complete before measured native execution; it is not a prerequisite for creating allocated workspaces. Preserve allocation -> setup/readiness -> plan -> run references without cycles.

1. skill-design-spec.md: existing design supplied by skill-builder, or the actual selected equivalent specification.
2. test-cases.json: versioned requirement-derived tasks, multi-turn inputs, expected/forbidden behavior, artifact assertions, baseline treatment, repetitions and held-out designation. Freeze it before measuring.
3. validation-plan.json: binds specification/rubric/cases/framework contract references, scope, owner, runtime arrangement, budget, baseline and each expected check/attempt/arm. Complete every template placeholder.
4. structural-checks.json: source helper result with complete candidate file manifest; installed reports are additional evidence.
5. ai-review.json: independent criterion records R01-R10. This is static semantic review.
6. A separate run-manifest.json and case-grade.json for each native case, arm and attempt. Never reuse writable context across attempts.
7. validation-results.json: one result per planned check, with raw evidence references and case-grade references for native observed outcomes.
8. decision.json: immutable output from assess_evidence.py, binding the plan/results and required evidence groups.
9. verification-results.md and skill-enhancement-spec.md: human-readable report and builder-ready change specification.
10. handoff.md: hashes the completed outputs and assigns the next task. Its own digest is delivered externally.

Run manifests additionally bind validation_plan_ref, workspace_allocation_ref (null with a reason for non-Git environments), workspace_id, client_state_directory and environment_setup_ref. The complete plan maps every attempt to an unused workspace and independent state; allocation additions remain separately bounded. Protected runtime admission owns these checks; the current reducer does not enforce all of these extensions. Pending test budgets can leave its receipt unavailable without preventing allocation-backed preparation.

The source and installed package manifests are distinct. The candidate_root in the plan is the frozen source being evaluated. The structural_report reference in results must be the source-mode inspection of that root. Native run manifests separately bind the actual installed package.

## Outcomes and disposition

| Outcome | Exact meaning |
|---|---|
| PASS | The named condition was observed to satisfy its predefined requirement, with complete evidence for that claim. |
| FAIL | An observed result violates a predefined applicable requirement. |
| NOT_RUN | Planned observation was not attempted. |
| COULD_NOT_RUN | An attempted or prerequisite-dependent observation could not be established; record the cause. |
| NOT_APPLICABLE | Explicitly excluded from the frozen scope with a reason; cannot replace missing required work. |

Never blend structure, AI review, A, B and C into one percentage. Native behavior is NOT_EVALUATED while no complete behavioral conclusion is supported. A reported FAIL may coexist with incomplete coverage.

The plan's check expectation is:
- pass: applicable required assertion; must yield PASS.
- observation: baseline comparison that must be completed; either observed PASS or FAIL supplies comparison evidence. A failing baseline does not itself make the candidate fail.
- excluded: documented scope exclusion; result must be NOT_APPLICABLE. It cannot eliminate an entire required evidence group.

Required evidence groups are intake, structure, ai_review, C, B and A. Include each R01-R10 check as AI-R01 through AI-R10; an inapplicable rubric criterion needs a predefined exclusion reason. Every native attempt/arm gets a unique check ID and attempt_id before execution. An enhancement also includes regressions covering the prior findings and preserved behavior.

The reducer preserves raw outcomes and derives effective outcomes. Any applicable FAIL produces revise. Otherwise missing/unavailable required observations produce insufficient_evidence. All required observations passing produces suitable_for_stated_scope. A missing result is NOT_RUN. A missing/changed referenced file or inconsistent record makes that observation COULD_NOT_RUN. Expected baseline FAIL counts as completed observation, while its raw FAIL remains visible.

A report status such as draft/in_review/accepted, external adoption, structural freshness, and behavioral outcome are separate facts. suitable_for_stated_scope is a recommendation, not acceptance.

## Deterministic helper interfaces

inspect_skill.py: see structural-checks.md. Python 3.11+; YAML checks also require PyYAML. It never executes target scripts. Output creation is exclusive and outside the target. Retain exit status and errors.

assess_evidence.py --plan FILE --results FILE --output NEW_FILE:
- Requires populated local plan/results schemas, matching run ID and exact plan binding, and pinned specification/rubric/cases/framework-contract references.
- Requires Codex provider, old_skill/without_skill baseline, and positive integer max_attempts/max_seconds. Repetition choice belongs in the frozen case/check plan; expand every planned attempt to a unique check.
- Checks unique planned/result IDs, required groups, AI criteria, applicability, evidence identities and required baseline observation.
- Binds source structural outcome and current source file manifest. A changed source is not fresh evidence.
- Matches AI criterion outcomes to the independent review record and checks per-criterion evidence locators.
- For native PASS/FAIL, matches case ID, arm, attempt ID and outcome to the case grade and run manifest, verifies tier/provider/runtime/assignment fields and the transcript digest.
- Writes decision.json exclusively. Exit 0 means required declared results and record checks support the scoped recommendation; exit 1 means observed required failure; exit 2 means unavailable/incomplete/invalid input or output error.
- Invalid top-level inputs or output I/O can produce stderr with exit 2 and no decision file. Preserve that error and write an insufficient-evidence report; do not claim a receipt exists.

Neither helper proves reviewer honesty, actual native consultation, context independence, fixture validity, causal improvement, or completeness of the chosen test plan. The validator must inspect those substantive claims against raw observations. The reducer does not launch tests, contact AI, authenticate a log, install hooks, or grant external acceptance.

## Native grade binding

Use devforge.skill-run/v1 with the supplied extensions case_id, attempt_id, arm and transcript_sha256. Keep original provider output intact, and reference it rather than rewriting it as a better-looking transcript. Core source/installed/baseline/case/fixture identities, runtime, context isolation and execution_ref must remain populated for observed runs.

Use devforge.skill-case-grade/v1 for each grade. outcome in the run manifest and overall in the grade record represent the final observed case outcome, distinct from the terminal's raw exit status. The observation extension records raw terminal completion/exit, target selection, actual resource consultation and its evidence. A successful process alone does not prove a case PASS.

Grade named behavior, artifact delivery, constraints and activation separately. A dimension is NOT_APPLICABLE only when genuinely outside that case's purpose, with its reason. Compute the case outcome from all applicable required assertions and complete observation; never average away a failed requirement. Record short evidence-based rationale, not hidden model reasoning.

## Findings and severity

Each finding has a stable F-### ID, type defect/enhancement/evaluation_gap, criterion/requirement IDs, affected source revision and file/section/lines, evidence locators, confidence/uncertainty, impact, recommendation and affected case IDs.

| Severity | Meaning |
|---|---|
| BLOCKER | Candidate cannot be safely or meaningfully exercised, violates authority boundaries, or has a package defect that prevents the required operation. |
| MAJOR | A required behavior, deliverable or constraint is demonstrably wrong. |
| MINOR | A contained defect with a narrower demonstrated consequence. |
| ADVISORY | Optional improvement or new proposed behavior; does not fail an accepted requirement by itself. |

Choose severity from the demonstrated consequence, not the rubric label. Separate an unavailable runtime from a target defect. Uncertainty and disagreement cannot become a fabricated failure. A required failure still requires correction regardless of its severity label.

## Builder remediation contract

skill-enhancement-spec.md uses an authoring-specific artifact_type skill-enhancement-spec in the shared devforge.artifact/v1 envelope. This is a paired utility extension, not an assertion that the existing DevForge artifact CLI validates it.

For each proposed CHG-###, provide finding IDs, exact source identity, accepted requirement versus new proposal, evidence/reproduction, bounded desired behavior, file/section targets, preserved behavior, forbidden scope changes, acceptance conditions and affected reruns. Provide enough information to implement without rerunning the entire discovery conversation.

Unknown causes become investigation tasks with a bounded question and evidence target; do not fabricate patches. Baseline/candidate/runtime problems may require evaluation repair rather than target changes. Declare no target edit when evidence supports none.

skill-builder verifies selected identities, retains the old candidate, resolves consequential ambiguity and applies only authorized changes. It reports changed files and new candidate identity without running validation. skill-validator then assesses the new revision and closes findings only using new matching evidence. Preserve finding history; do not overwrite an earlier FAIL.

## Required closure

A complete delivered evaluation has a saved report and builder specification even when blocked or no changes are recommended. Each missing observation has a cause and next owner. No acceptance label, successful hook, numerical score or template completion substitutes for the required evidence.

## Opt-in VPR-2 records and advisory reduction

The earlier v1 sections govern only legacy records. For an explicitly selected VPR-2 validator assignment, the exact keys and version matrix in [execution-contract.md](contracts/execution-contract.md#vpr-2-record-contract) govern. These assets now instantiate unpopulated v2 records: validation-plan, ai-review, validation-results, run-manifest and case-grade. For a newly requested legacy record, use its exact v1 shape from that matrix (omit only the listed v2 additions, retain legacy plan checks/groups/budgets and criterion/native obligations); never relabel an existing v1 record or mix its authority chain with v2.

V2 Pins are exactly canonical absolute `{path, sha256}`; existing typed input_refs retain `{kind, path, sha256}`. Reject unknown/missing/duplicate keys and identities, nonfinite numbers, bool-as-integer budgets, escaping paths, stale pins and unsupported versions. Plan -> delivery -> actual independent T04 review -> observations/results is acyclic. No review is prewritten by the author, and no helper output supplies external authority.

T01/T02 select the actual Routine/Full claim, accepted baseline/scope, candidate/environment identity, unchanged qualified anchor or accepted unqualified anchor, current Routine acceptance and complete acceptance chain. Include both immediate and cumulative diffs and dependency union. Routine never upgrades UNKNOWN/ABSENT qualification. The exact input lineage is copied to results/decision; new owner decisions create successor records separately. All matching CI rules apply. CP-01–CP-04 require evidence about used capabilities, not version labels. Changed executable evidence includes actual installed load/completed task and affected denial/activation/failure probes. Unknown changed dependencies prevent Routine eligibility; consequential trust/control/transfer or unbounded impact requires Full.

Preserve every original catalog case/assertion/variant/arm/repetition and required D/S/N kind. T04 independently reviews the complete projection and all R01–R10 invariants. Full selects every applicable original assertion; Routine may record reviewed NOT_SELECTED, and genuine NOT_APPLICABLE retains its source scope basis. The seventeen VPI cases are an additional source-only regression supplement, never a replacement or automatic inner suite. Original SV-009, SV-012 and SV-024–SV-028 native requirements remain applicable.

Record twelve task_results with frozen Enforced classification/selection and separate disposition/outcome. SATISFIED_BY_REVIEWED_SELECTION can satisfy an unselected native obligation while its observation remains NOT_RUN/NOT_OBSERVED. Every catalog assertion gets exactly one assertion_results row. Missing observations remain NOT_RUN or COULD_NOT_RUN. Required candidate/protocol FAIL takes precedence over missing evidence; a baseline FAIL under expectation=observation completes an intact comparison only. Pair summaries cannot overwrite arm-specific judgments.

`report_completion` (COMPLETE/PARTIAL/BLOCKED), `validation_disposition` (ROUTINE_PASS/FULL_PASS/FAIL/INSUFFICIENT_EVIDENCE), owner acceptance and qualified identity are separate. Complete honest P5/P6 reporting can coexist with failed/unavailable observations. `routine_adoption_eligible` requires ROUTINE_PASS plus exact accepted scope, lineage, compatibility and required destination/post-install evidence; it grants no human approval. Unselected C/B/A groups remain NOT_RUN. `external_acceptance=NOT_GRANTED` is mandatory in the advisory decision.

The helper preserves the v1 branch and separately parses v2 input. It mechanically derives summary values from selected assertion evidence and independent review, leaving malformed input as exit 2 without a decision and honest unattempted v2 as a typed NOT_RUN/INSUFFICIENT_EVIDENCE decision with exit 2. Its output has no protected receipt authority. Native collector origin, real isolation, semantic adequacy, effective timestamps and actual receiving execution require independent observation and protected runtime adjudication; a synthetic fixture or helper PASS cannot supply them.

A run/observation binds the exact frozen identity, inputs, prompt/forcing, arm/variant/repetition, source visibility, freshness and earliest consuming task. Only compatible observations can be shared; opposite arms, forced-versus-implicit prompts and late evidence cannot. Preserve complete raw outputs and per-arm/assertion grades with explicit reuse/correlation limits. A grade must come from the selected independent producer and cannot be an aggregate-only or prewritten substitute.

Full target receiving evidence belongs before T09: eligible actual target-produced output, receiver contract, actual load and completed action/expected negative disposition. Bind the four exact pins and actual observation time in receiving_transfer. T12 only prepares the evaluator handoff; it does not generate this evidence or recursively enqueue qualification.

This enforcement implementation requires CI-05 Full before operational adoption. Unknown native authentication/isolation/interactive or nested transport support remains unresolved. Auth lifecycle reuse is separate from fresh writable evidence state; no copying of credentials or reuse of writable worker history is authorized. Original clocks/charges persist; the v2 call graph counts every selected review, worker, grader, meaningful parent return and continuation under separate external native funding. Engineering generations and exhausted historical ledgers are not native funding.
