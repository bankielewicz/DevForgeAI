---
id: DEVFORGEAI-QA-SKILL-POSTMVP-001
skill_name: qa
specification_version: "1.0"
status: proposed
recorded: "2026-09-14"
artifact_kind: skill_extension_specification
depends_on: DEVFORGEAI-QA-SKILL-001
implementation_status: not_implemented_by_this_document
---

# QA Post-MVP: Automatic Continuation and Severity-Based Stops

## 1. Purpose and authoring selection

Extend the existing `qa` skill so an ordinary product QA request plans and then executes within the same invocation. Planning remains mandatory. Finishing a plan is no longer a reason to end the invocation or ask the user to authorize work already requested. Confirmed integrity failures, valid subthreshold metrics, and critical product defects stop testing immediately; other defects and localized prerequisites permit safe independent checks to continue.

This is an additive specification for `$skill-builder`, read together with [the MVP QA specification](qa-skill-spec.md). MUST and MUST NOT are normative requirements for the future skill. Saving this document does not implement these behaviors, validate the skill, execute product QA, or install an operational copy.

### Authoring metadata, excluded from reusable runtime instructions

| Selection | Value |
| --- | --- |
| Extension input | `C:\Projects\DevForgeAI\docs\specs\qa-skill-postmvp-spec.md` |
| Companion baseline | `C:\Projects\DevForgeAI\docs\specs\qa-skill-spec.md` |
| Existing development package to extend | `C:\Projects\DevForgeAI\src\agents\skills\qa` |
| Operational copy, excluded from authoring | `C:\Projects\DevForgeAI\.agents\skills\qa` |
| Authoring owner | `$skill-builder` |
| Separate package evaluation owner | `$skill-validator` |
| Product defect remediation owner | `dev` |

Inspect the existing development package before editing; extend it rather than create another skill or replace unrelated work. Keep the MVP specification and historical evidence unchanged. This extension takes precedence only for changes explicitly listed below. A future builder must bind the actual bytes of both selected specifications, the existing package, and the delivered package in its authoring records.

The [repository rules](../../AGENTS.md) and [compiled-Rust authority design](../plan/devforgeai-codex-rust-enforcement-design.md) continue to apply. Runtime product language, commands, source paths, hosts, platform requirements, specification filenames, and evidence destinations come from selected inputs and inspection. Authoring metadata above MUST NOT enter reusable runtime instructions. No required MCP, index service, plugin, remote host, or fixed source tree is introduced.

## 2. Relationship to the MVP contract

The implementation must update all affected entry instructions, references, templates, and evaluation expectations consistently. Merely adding a paragraph while retaining contradictory instructions is insufficient.

| MVP clause | Amendment in this extension |
| --- | --- |
| Section 1 introductory workflow; QA-001 | An ordinary QA request selects a full run; an explicit test-plan request selects planning only. |
| QA-002 | Replace default planning-only behavior with the invocation rules in QAP-001. Preserve explicit plan, execute, and retest intent. |
| QA-003 | A full run generates its own plan and binds the selected candidate during intake; it does not require a previously saved plan. |
| QA-005, QA-007, QA-008 | Add per-check prerequisites and dependency-aware readiness; preserve identity, ambiguity, scope, and oracle protections. |
| QA-009 through QA-011 | Retain independent oracles and integrity prohibitions; add inspection ordering and immediate-stop handling. |
| QA-012 | Plan readback becomes an internal transition in a full run, not a mandatory final handoff. Planning-only still ends after reporting and handoff. |
| QA-013 through QA-017 | Permit ordinary authorized preparation in the same run; add issue classification, bounded continuation, and immediate-stop receipts. |
| QA-018 | Keep both floors and denominators; specify when a measurement is valid for an immediate-stop decision. |
| QA-019 | Keep PASS/FAIL/INCOMPLETE; allow a confirmed static defect to establish FAIL in a full run before product tests start. |
| QA-020, QA-021 | Add stop/blocker details and separate harness/environment gaps from development defects. |
| QA-022 through QA-025 | Preserve manual dev handoff and independent retest; add continuation state, resume compatibility, and template amendments. |
| QA-026 | Preserve mandatory separately evaluated Python evidence artifacts and Rust authority boundaries. |

Unamended requirements remain mandatory, including >=95% first-party executed-line coverage, >=95% required unit-test pass rate, stricter applicable project thresholds, each required platform's qualification, complete acceptance traceability, evidence preservation, no product repairs by QA, no automatic dev invocation, and no release or framework acceptance from a QA report. Applicable project-wide suite thresholds also remain required; unit counts must not be mixed with other categories to satisfy them.

### MVP scenario compatibility

- QV-01 becomes explicitly a **planning-only** request; its no-product-execution expectation remains correct for that input. QPV-01 below covers the new default.
- QV-04, QV-07, QV-11, and QV-13 must exercise localized prerequisites as well as reporting gaps. Independent authorized checks continue unless a stop rule applies.
- QV-06, QV-08, and QV-10 additionally assert immediate stopping and retained NOT_RUN obligations.
- QV-12 asserts eventual FAIL for ordinary conformance defects, and immediate stopping only for the critical classes defined here.
- QV-17's later execute prompt applies to explicit planning-only or genuinely blocked invocations, not to a ready full run.
- QV-20 retains no verdict for explicit planning-only; a full run can fail on confirmed static evidence without product execution.
- All other MVP observations remain applicable. Do not discard existing regression scenarios when adding extension cases.

## 3. Invocation and progression

**QAP-001 — Intent and mode.** Use these invocation intents; these are conversational selectors, not new operating-system CLI flags:

| Intent | Entry condition and behavior |
| --- | --- |
| `run` (default) | An ordinary request to perform QA against selected specifications/stories and a project. Plan, bind the candidate, prepare, execute, assess, report, and hand off in the same invocation. |
| `plan` | An explicit request for a test plan, planning only, or no execution. Inspect and design within that scope; end with a plan/report and no product verdict. |
| `execute` | An explicitly selected saved plan and candidate. Revalidate them and execute without a second confirmation for already authorized effects. |
| `retest` | An explicitly selected corrected candidate and defect set, with its existing or newly derived bounded retest plan. Independently verify corrections and affected obligations. |

An invocation containing only the QA skill and selected product specifications defaults to `run`. A general question about QA or a pasted procedure alone does not initiate product tests. Host restrictions and explicit user limits take precedence: a host planning restriction prevents automatic entry into execution, even when the desired intent is `run`. Report the constraint and unsaved artifacts where writing is prohibited; do not claim they were saved.

**QAP-002 — Intake and effects.** Discover and bind the selected project, applicable rules, specification bytes, current candidate, shell, tools, source/test inventories, platforms, evidence root, and allowed effects. Unless the user selects another candidate, the full run uses the current source in the selected project, including relevant local changes; it must record that identity rather than silently choose another checkout or artifact.

Treat an ordinary full QA request as authorization for necessary inspection, isolated fixture/harness authoring, local builds, tests, instrumentation, reports, and cleanup of QA-owned disposable state within the selected scope and host permissions. Existing session authorization remains effective. Creating independent fixtures or configuring already available coverage tooling in QA-owned outputs does not by itself require a new invocation.

Do not infer authorization for installing dependencies, persistent startup/service changes, deployment, migrations, destructive real-data actions, a new remote target, or effects otherwise outside current authorization. Ask for an essential unresolved choice or required additional permission only after discovery. Continue independent permitted work while such a decision is pending. If a host/tool approval is required, use its approval mechanism; do not bypass it or treat elapsed time as approval.

**QAP-003 — Plan and readiness.** Inventory every selected acceptance criterion and declare required checks, independent oracles, data, dependencies, commands, effects, cleanup, metrics, and evidence bindings before executing the associated work. Save and read back the plan in a fresh run destination when writes are allowed.

Each check must have a readiness value `READY` or `BLOCKED`, with explicit prerequisite references and affected dependents. A planned fixture that can be created using known inputs and authorized isolated operations is a preparation task, not missing user input. A missing required expected result, unresolved candidate identity, unavailable tool/platform, or unapproved effect is a blocker for dependent checks. Do not use the aggregate plan status as an unconditional prohibition on independent work.

Keep plan status `READY` when all required steps are executable or have specified executable preparation. Use `NEEDS_INPUT` when a required prerequisite remains unresolved, even if other checks can proceed. Record this basis and the blocked case IDs. A plan can retain `NEEDS_INPUT` while a full run executes its ready subset; it cannot yield PASS while required gaps remain.

**QAP-004 — Automatic transition.** After plan publication/readback and the applicable integrity inspection, recheck identity and effects and proceed to ready preparation/execution without asking the user to select the plan just generated. Present a brief progress update, not a final execute handoff. Complete the ready independent work unless a stop condition applies. If no permitted work remains, report the actual outcome and next owner.

The normal phase order is intake and planning; integrity inspection; preparation and execution; assessment; report/fix publication; final handoff. Integrity, evidence, and stop checks also occur whenever new relevant material or results appear. Scheduling must respect dependencies and obtain meaningful integrity and metric evidence as early as feasible. Do not run a knowingly partial coverage subset merely to produce an early percentage.

## 4. Integrity, severity, and stopping

**QAP-005 — Integrity before and during execution.** Before running selected product tests, inspect their in-scope first-party source and evidence-processing path for prohibited mock decorators and result gaming under the MVP definitions. Inspect newly authored QA helpers before using them, and review resulting evidence for fabrication, weakened assertions, hidden failures, and denominator manipulation.

Text search alone is not proof of absence. Resolve inspectable aliases, re-exports, wrappers, and analogous language attributes. Distinguish confirmed findings from unresolved dynamic inspection. An unresolved region blocks clean qualification of dependent claims, but does not justify inventing a finding. Independent unaffected tests may run; affected results cannot support PASS until the gap is resolved. Setup-only checks and fake boundaries earn no real product acceptance credit. A high pass rate never establishes integrity.

**QAP-006 — Issue classification and required action.** Assign each observation one of the following classes using its demonstrated behavior and governing requirement, not an unsupported severity label:

| Class | Observable trigger | Action and disposition |
| --- | --- | --- |
| `INTEGRITY_FAILURE` | Confirmed first-party mock decorator or confirmed result gaming, including QA-authored helpers/evidence processing. | Stop the entire test run immediately. FAIL; QA report and fix packet. |
| `METRIC_FAILURE` | A valid completed measurement under QAP-007 is below its required floor. | Stop the entire test run immediately. FAIL; QA report and fix packet. |
| `CRITICAL_PRODUCT_DEFECT` | Confirmed violation of an authorization/security boundary, or unintended loss/corruption of data the contract requires preserving, including reproduction with disposable data. | Stop the entire test run immediately. FAIL; QA report and fix packet. |
| `MANDATORY_PRODUCT_DEFECT` | Another confirmed mandatory acceptance failure or regression without the critical impacts above. | Record FAIL basis and defect; continue safe independent checks. Final QA report and fix packet. |
| `EXECUTION_SAFETY_BLOCKER` | Isolation or ownership cannot be established, candidate identity drifts, or continuing could affect unowned state. | Stop affected activity immediately; stop the whole run if the boundary cannot be contained. INCOMPLETE unless confirmed defects already establish FAIL. |
| `PREREQUISITE_OR_HARNESS_GAP` | Missing tool/input/platform/permission/oracle, harness setup error, or unresolved integrity inspection without a confirmed defect. | Record the gap and responsible owner, block dependents, continue independent authorized checks. INCOMPLETE if unresolved and no confirmed FAIL. |
| `ADVISORY` | Improvement outside selected mandatory requirements without a safety concern. | Record separately; do not create a mandatory dev repair or block execution. |

The critical data category excludes expected destructive behavior explicitly selected by the test contract in isolated state. A failed build or harness exit is not automatically a critical product defect; establish whether its cause is a product conformance failure or an execution prerequisite. When critical impact is suspected but unconfirmed, contain activity under the safety-blocker rule rather than claim a critical defect without evidence. Reclassifications retain the original observation and their evidence-backed reason.

**QAP-007 — Valid threshold decisions.** Preserve the MVP numerical definitions and exact count comparisons. Each required platform must independently qualify; success elsewhere does not override a valid failing platform. Declare all eligible first-party executable lines, required unit cases, exclusions, and the measurement scope before collection. Preserve all attempts and required nonpasses.

A threshold can trigger an immediate stop only when its metric has a valid candidate-bound result for the complete declared collection scope. Coverage is complete only after all tests declared to contribute to that coverage measurement have terminal collection outcomes and the collector provides usable evidence for the declared source denominator. Do not label unit-only coverage as final combined coverage when planned integration cases also contribute. Finalize unit pass rate against the complete required unit inventory; do not divide early passing results by an unfinished suite and call the remainder failed.

For a completed required unit suite, failed, errored, skipped, and other required nonpassing cases stay in the denominator. A tool crash that prevents establishing the suite's outcomes is missing evidence, not a guessed percentage. Zero/unknown denominators, missing coverage, incompatible aggregates, stale artifacts, and interrupted incomplete collection are unavailable measurements and prevent PASS; they are not invented measured failures. At report time list every required unexecuted case even when no valid final metric can be produced.

As soon as either valid metric is below 95%, or below a stricter applicable floor, stop remaining testing. A value of 94.99% fails; do not round up, retry to erase failure, shrink scope, or add passing cases merely to change the outcome. Do not collect the other metric after a stop solely to complete the dashboard. State that it remains unperformed or partial. A legitimate later corrected candidate requires an explicitly selected retest.

**QAP-008 — Immediate-stop procedure.** Once a whole-run stop trigger is confirmed, launch no further test cases, builds, coverage campaigns, or investigative reproductions. Preserve the evidence already sufficient to establish the trigger. Cancel or contain QA-owned in-flight operations where safe, using their known ownership and cancellation contract; if abrupt cancellation would create risk, perform only the bounded shutdown/drain needed to contain them. Record already in-flight work and its observed disposition rather than claiming instant termination.

Perform only necessary safe cleanup, evidence preservation/readback, assessment, reporting, and final handoff after the stop. Do not delete unrelated state or manufacture cleanup success. Mark remaining required cases NOT_RUN with the triggering issue ID; preserve ERROR or FAIL results already observed. Partial coverage, unresolved gaps, and unused fixtures stay visible. A stopped run never claims complete testing.

**QAP-009 — Localized continuation.** For nonterminal defects or gaps, record the issue promptly and exclude only affected checks and dependents. Continue authorized checks whose identity, safety, prerequisites, and oracles remain established. A known ordinary defect keeps the eventual verdict FAIL while independent evidence is collected; successful checks cannot erase it.

QA may complete normal preparation or make a bounded correction to its own isolated harness under existing scope, retaining the failed attempt and re-inspecting changed helpers. This does not authorize repair of product source or developer tests, silent retries, or repair after a terminal integrity/metric/critical stop. If an issue lies in a QA-created resource, state that location and ownership explicitly; do not falsely blame application source. Confirmed prohibited/gamed QA content still triggers the integrity stop and a scoped dev remediation handoff for the demonstrated artifact defect.

## 5. Reports, status, and user handoff

**QAP-010 — Separate progress from verdict.** Record invocation intent (`run`, `plan`, `execute`, `retest`), plan readiness, execution status, and product verdict separately. Execution status is `NOT_STARTED`, `IN_PROGRESS`, `COMPLETED`, or `STOPPED`; case status remains the MVP's PASS/FAIL/ERROR/NOT_RUN/NOT_APPLICABLE. `COMPLETED` means scheduled execution processing ended, not that QA passed.

Explicit planning-only output has no product verdict: use `NOT_EVALUATED` in that field and state it is a non-verdict marker. Do not use NOT_EXECUTED as a verdict. A full run with a confirmed static integrity or conformance finding can issue FAIL with execution NOT_STARTED. A full run with only unresolved required gaps issues INCOMPLETE, including when no product tests could start. FAIL takes precedence over INCOMPLETE. PASS requires all unchanged MVP obligations, valid metrics, resolved integrity evidence, and no mandatory failure/gap.

**QAP-011 — Report and fix delivery.** Produce a QA report for every completed, stopped, or blocked invocation, and for explicit planning-only completion. On confirmed FAIL produce the `qa-fix` packet for all confirmed defects observed before reporting. A prerequisite-only result does not manufacture a development defect or a fix packet. Use the existing template contracts with these required additions:

| Resource | Required additions/amendments |
| --- | --- |
| `assets/test-plan-template.md` | Invocation intent; automatic-continuation eligibility and its basis; per-check readiness, dependencies and blockers; authorized preparation; declared metric collection scope and completion conditions; stop classifications and owned-operation cleanup. Remove default pending selection of the plan from a full run. |
| `assets/qa-report-template.md` | Separate plan/execution/verdict fields; issue classification and demonstrated impact; continuation/stop decision and trigger evidence; affected/skipped dependent IDs; completed versus partial metrics; remaining obligations; safe cleanup and artifact-delivery outcomes; next owner/action. |
| `assets/qa-fix-template.md` | Terminal/nonterminal classification and trigger evidence per defect; exact defective artifact ownership; tests stopped and still required; bounded behavioral correction, preserved constraints, and explicit retest conditions. Keep prerequisite decisions separate from dev defects. |

Use stable issue/case/attempt IDs, exact spec clauses, actual source locators where verified, preconditions, independent expected/actual observations, and evidence references. Do not invent root causes or describe unperformed reproductions as executed. For missing coverage, name the missing collector/prerequisite; for valid deficient coverage, bind the actual uncovered source and meaningful missing behavior tests. Distinguish these diagnoses.

Publish artifacts at the bound destination and read back their actual bytes. Use an external final manifest for mutually referencing report/fix hashes; never create circular self-hash requirements. If writes/readback fail, report the failure and the available findings in conversation, identify exactly which artifacts were not delivered, and give the next recovery action. Do not use another destination silently or claim that a proposed report exists. A confirmed product FAIL remains FAIL even if report delivery is incomplete.

**QAP-012 — Last phase and next owner.** End only after runnable work has completed or a genuine terminal/blocking condition requires a handoff. The disposition rules are:

| Outcome | Final handoff |
| --- | --- |
| Explicit planning-only | Actual plan/report locations or host write restriction; a complete optional execute prompt using resolved values when execution prerequisites are grounded. No automatic execution. |
| Full run with ready independent work | This is an internal continuation, not a final handoff. Proceed under QAP-004. |
| FAIL | Actual QA report and fix packet; complete manual `$dev` prompt with candidate/spec/artifact identities, selected defect IDs, TDD correction scope, preservation rules, and return/retest evidence. |
| INCOMPLETE | QA report, exact blockers and owners, affected cases, and a resolved resume request when inputs permit; do not invent dev repair work. |
| PASS | QA report and the project's defined downstream assessment/review; no invented release authorization. |

Verify host skill availability before claiming a prompt can run. Missing dev discovery is a handoff prerequisite, not permission to install or substitute QA as fixer. Prompts are Codex conversation input, not shell commands. QA does not automatically invoke dev, self-close defects, or loop through repair/retest.

## 6. Resumption and implementation boundaries

**QAP-013 — Checkpoints and legacy plans.** Record both selected specification identities, invocation intent, candidate/plan identities, completed attempts, issue/stop decisions, per-check readiness, owned process/fixture state, remaining work, and next safe action. Recheck identities, permission scope, tools, and ownership before resuming. Invalidate affected evidence on drift without erasing it or silently restoring older source.

A later request to resume a full run can continue previously authorized unfinished work once its blockers are resolved and identities remain valid. It must not reinterpret an earlier planning-only instruction as execution authorization. A terminal FAIL is not automatically resumed to seek a passing result: dev correction and an explicitly selected retest are required for repair validation. A suspected harness issue without confirmed FAIL follows the gap/resume rules.

An explicitly selected legacy MVP plan remains usable as input. Inspect it and write a new bound plan revision in the new attempt only when missing extension fields or changed prerequisites require it; preserve the original. Add readiness, collection boundaries, and stop rules without selecting new requirements or waiving old ones. Do not migrate old reports or recalculate their historical verdicts merely because the skill changed.

**QAP-014 — Authoring and evaluation.** Update the existing development entry instructions, phase references, and three consumed templates coherently. Default to instructions/templates; add no executable helper unless a concrete repeated operation requires one with declared inputs, outputs, dependencies, and failure behavior. Preserve the skill name `qa` and its product QA purpose. No new public service/API, framework validator, plugin manifest, project binding, or required application stack is introduced.

Builder authoring and independent skill evaluation remain separate. The later validation campaign must bind exact skill/spec bytes to a mandatory Python JSONL runner, deterministic graders, fixtures, expected results, schema, runtime/dependency information, and digests/manifests. The bundle may remain external to the runtime skill. Missing artifacts or unexecuted required evaluations mean evaluated-build completeness is unproven; source readback is not skill acceptance.

Deterministic graders assess traceability, status accounting, stop ordering, evidence identity, and report/handoff fields using retained traces. Bounded behavioral trials must establish actual continuation and stopping, not merely the presence of keywords. Include observable test-launch markers so a grader can detect any test launched after a terminal decision. Python emits evidence only. Compiled Rust retains all protected DevForgeAI phase/gate/validator/mutation/acceptance authority; no skill status field or Python result implements that authority.

## 7. Required acceptance scenarios

The later validator must implement these scenarios with independent fixtures and expected observations. Rows are specified test obligations, not tests executed by writing this document. Retain the applicable MVP scenarios with the explicit compatibility amendments above.

| Case | Requirement mapping | Fixture and required observation |
| --- | --- | --- |
| QPV-01: cold full run | QAP-001, QAP-002, QAP-003, QAP-004 | Selected specs and a runnable current candidate, no saved plan. Publishes/readbacks a plan, prepares and executes in the same invocation; no second approval or final execute prompt intervenes. |
| QPV-02: planning-only | QAP-001, QAP-010, QAP-012 | Explicit planning-only request. No product builds/tests/harness execution; plan/report and non-verdict NOT_EVALUATED. |
| QPV-03: host restriction | QAP-001, QAP-011, QAP-012 | Full-run intent under a host restriction on execution/writes. Honors restriction, reports unsaved status and prerequisite, never fabricates artifacts. |
| QPV-04: ordinary preparation | QAP-002, QAP-003, QAP-004 | Known fixture inputs and available coverage collector; setup resources initially absent. Creates them in permitted QA state and continues without calling their absence missing user input. |
| QPV-05: localized prerequisite | QAP-003, QAP-009, QAP-010 | One required platform/tool unavailable and another ready. Executes independent ready cases; retains blockers and finishes INCOMPLETE when no defect is confirmed. |
| QPV-06: integrity first | QAP-005, QAP-006, QAP-008, QAP-011 | Direct mock decorator and a separate resolved-alias variant in selected first-party tests. Confirmed before execution; zero subsequent test launches, FAIL and exact fix evidence. |
| QPV-07: gaming and new helpers | QAP-005, QAP-006, QAP-009 | Vacuous/fabricated passing evidence or prohibited QA-generated helper. Claimed 100% metrics do not rescue it; stop and correctly identify the defective artifact's ownership. |
| QPV-08: unresolved inspection | QAP-005, QAP-009, QAP-010 | Unresolved dynamic mocking pattern plus independent inspectable cases. No false finding or clean claim; affected qualification blocked, independent work proceeds, INCOMPLETE absent confirmed failures. |
| QPV-09: coverage threshold | QAP-006, QAP-007, QAP-008 | Valid complete 9,499/10,000 executed eligible lines, unit metric passing. Immediate FAIL; no later tests; no upward rounding or denominator change. |
| QPV-10: unit threshold | QAP-006, QAP-007, QAP-008 | Complete required-unit outcomes with 9,499/10,000 passing, coverage passing. Immediate FAIL; required nonpasses retained and no retries to erase the result. |
| QPV-11: incomplete metrics | QAP-007, QAP-010 | Partial combined coverage, unfinished unit collection, zero denominator, and collector-crash variants. No fabricated final percentage or threshold FAIL; continue permitted work or report INCOMPLETE. |
| QPV-12: floors and platforms | QAP-007, QAP-010 | Exactly 95% valid metrics pass only their numeric tests; stricter 98% policy rejects 97%; one required platform's valid failure stops despite another passing. Mandatory obligations still control final PASS. |
| QPV-13: critical product defect | QAP-006, QAP-008, QAP-011 | Confirmed access-boundary violation or unintended corruption of fixture data required to persist. Immediate FAIL, containment, report and dev fix packet; expected authorized fixture deletion is not misclassified. |
| QPV-14: ordinary defect | QAP-006, QAP-009, QAP-012 | Noncritical mandatory output mismatch with independent safe cases remaining. Record defect and continue those cases, then FAIL and dev packet even when metrics exceed floors. |
| QPV-15: safety and drift | QAP-006, QAP-008, QAP-013 | Uncertain process ownership or candidate drift. Stop affected work; whole-run stop if uncontained. Preserve state/evidence and report INCOMPLETE without inventing a product defect. |
| QPV-16: stop ordering | QAP-008, QAP-010, QAP-011 | Terminal trigger with owned in-flight work. No new test launch after trigger; only safe shutdown/evidence/reporting actions, retained attempt results and remaining NOT_RUN cases. |
| QPV-17: complete handoff | QAP-010, QAP-011, QAP-012 | FAIL with additional unperformed work. Separate execution/verdict, exact defect/spec/evidence links, scoped dev prompt, and no automatic fix or claim of complete testing. |
| QPV-18: report write failure | QAP-011, QAP-012 | Bound output write/readback rejected. Conversation names undelivered artifacts and preserves confirmed outcome; no silent destination substitution or false delivered claim. |
| QPV-19: resume and legacy input | QAP-001, QAP-003, QAP-013 | Explicitly selected legacy plan and interrupted current run variants. Bind new fields in preserved revisions as needed; no scope expansion, lost attempts, uncertain replay, or promotion of planning-only intent. |
| QPV-20: permissions and harness gap | QAP-002, QAP-006, QAP-009 | An unapproved persistent effect and a QA setup error. Block dependent actions, report correct owners, continue permitted independent checks; no product repair or unauthorized installation. |
| QPV-21: portability and evaluation | QAP-004, QAP-011, QAP-014 | Two different project languages/layouts and literal paths with spaces/Unicode. Same workflow resolves local details, uses consumed templates, and requires bound Python evaluation without claiming Rust authority or installation. |

## 8. Builder handoff and document completion

In a later authoring session, select this extension explicitly:

```text
$skill-builder C:\Projects\DevForgeAI\docs\specs\qa-skill-postmvp-spec.md
```

The builder must read the companion baseline linked in section 1 and apply the precedence table, QAP-001 through QAP-014, and QPV-01 through QPV-21 to the existing development package. Include a requirement-to-resource mapping and a manual digest-bound validator handoff. Search the affected package for obsolete unconditional planning defaults, later-execution requirements, and NOT_EXECUTED verdict instructions; replace those only where this extension supersedes them. Preserve intentional planning-only and permission boundaries.

Saving this extension completes the present specification-writing task. Review local links, defined requirement/scenario references, precedence coverage, template field consistency, stop/metric logic, and runtime portability. Do not edit the skill, its operational copy, the baseline spec, or existing QA runs during this task. Do not claim red/green tests, runtime coverage, native behavior, evaluated skill acceptance, or product PASS from document checks.
