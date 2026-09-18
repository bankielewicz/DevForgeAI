---
id: DEVFORGEAI-QA-SKILL-001
skill_name: qa
specification_version: "1.0"
status: proposed
recorded: "2026-09-14"
artifact_kind: skill_specification
package_status: not_authored
---

# `qa`: Independent Specification-Driven Quality Assurance

## 1. Authoring contract

Create a reusable Codex skill named `qa` for independent quality assurance after a development iteration, sprint, or release candidate. It must operate in a cold Codex CLI session from explicitly selected specifications or stories, a selected development candidate, and applicable project rules. It first produces a testing plan. A later explicitly authorized execution invocation runs that plan, determines the QA outcome, and hands failed implementation back to `dev` for remediation.

This document is an input to `$skill-builder`. Saving it does not author or install the skill or perform product QA. MUST and MUST NOT are normative. Requirements describe the behavior to implement, not capabilities claimed to exist already.

### 1.1 Build selection: excluded from reusable runtime content

| Item | Selection |
| --- | --- |
| Skill name | `qa` |
| Specification | `C:\Projects\DevForgeAI\docs\specs\qa-skill-spec.md` |
| Development parent | `C:\Projects\DevForgeAI\src\agents\skills` |
| Final development package | `C:\Projects\DevForgeAI\src\agents\skills\qa` |
| Builder | `$skill-builder` using this explicit specification path |
| Skill-package assessment | `$skill-validator` in a separate authorized task |
| Product remediation owner | `dev` |
| Runtime prerequisite | Codex CLI terminal/file capabilities; no mandatory installed framework, index, plugin, or binding |

The destination is selected; a future builder invocation need not ask for it again. Inspect any existing target before writing. Do not overwrite unrelated work or initialize over an existing package. Concrete authoring paths and this project's application details must not enter generated runtime instructions. Package-relative reference and asset names are permitted.

The builder's name-based specification lookup does not include this directory. Pass the explicit specification path rather than moving the document, creating another authoritative copy, or changing lookup behavior.

### 1.2 Ownership and policy

The skill performs product QA, not assessment of a Codex skill package. Assessment of this `qa` package belongs to a separate skill-validation task. Builder's prohibition on running quality campaigns during authoring must not be copied into `qa` as a prohibition on executing authorized product QA.

The [repository guidance](../../AGENTS.md) governs development of this skill. Required Python skill-evaluation artifacts produce evidence. All DevForgeAI framework phase/gate/validator/mutation/acceptance authority remains compiled Rust as defined in the [authority design](../plan/devforgeai-codex-rust-enforcement-design.md). A report produced by `qa` is an assessment, not an authoritative release receipt or an implementation of a protected gate.

The portable runtime must not prescribe a product language, operating system, framework, application type, source tree, executable, build command, or specification filename. The mandatory >=95% floors and test-integrity prohibitions below are deliberately selected QA policy; they are not assumptions about product implementation.

## 2. Activation, modes, and inputs

**QA-001 — Purpose and activation.** Activate for independent product QA or test-plan generation against explicitly selected specification/story inputs and development scope. Support iteration, sprint, and release-candidate scope without assuming their size or release mechanism. Do not select all repository stories or expand into unselected specifications by discovery alone.

Near misses are product implementation, product repair, skill authoring, standalone architecture research, operational installation, deployment, and skill-package validation. Refer those to their appropriate owner or request clarification. Preserve automatic invocation unless the user separately changes it.

**QA-002 — Modes.** Default to `plan` when execution is not explicit. Planning performs relevant read-only inspection and writes selected planning/evidence artifacts; it does not run product tests, build the product, generate executable test harnesses, install dependencies, mutate product state, or issue a product QA PASS. Host Plan mode additionally prohibits file writes, so deliver the plan in conversation until the host permits saving it.

`execute` requires explicit selection of a concrete plan and candidate plus authorization for its test effects. A selected `retest` is execution against a corrected candidate and defect set, not an automatic loop. Do not interpret the word “plan,” a pasted procedure, or the existence of a plan as permission to execute. Do not automatically invoke `dev` or another QA session after producing a handoff.

**QA-003 — Runtime inputs.** Require selected project identity, explicit specification/story document(s), requested QA scope/mode, and access to applicable instructions. For execution also require a selected candidate and plan. Planning can proceed against intended behavior before a runnable candidate exists, but must identify the missing implementation/build prerequisite and cannot claim execution readiness for affected cases.

Accept optional development handoff, changed-file baseline, existing test results, architectural/stack/source-tree rules, known defects, prior QA checkpoint, evidence destination, and available services. A sprint scope requires its explicitly selected story set or unambiguous supplied scope manifest. A development completion claim is an input to verify, not a premise that all acceptance criteria passed.

**QA-004 — Portability and context.** Discover actual project instructions, shell, manifests, source layout, tools, permissions, and host/filesystem location. Keep Windows-native and Linux-native qualification distinct. Do not move, clone, switch, or synchronize checkouts to improve performance without authorization. Never substitute a similarly named checkout or translate paths across environments silently.

Resolve evidence output from explicit user selection, applicable project policy, or an established suitable evidence location, in that order. Preserve the full literal selected destination. If no destination can be grounded, ask once before writing. Bind actual output paths before the first write. Do not impose a fixed product evidence directory or require a Git repository.

Git, an index, semantic search, a framework service, a binding, MCP, a browser, and a plugin are not intrinsic prerequisites. Use available optional tools with their coverage/freshness limits; ordinary terminal inspection remains sufficient for discovery. A project-required external authority cannot be silently bypassed or simulated.

## 3. Phase 1: Establish the candidate and evidence baseline

**QA-005 — Candidate identity.** Bind selected specification bytes, plan, source/build identity, dependencies, and environment. With Git, capture commit plus relevant dirty/untracked state; a commit alone does not identify a dirty candidate. Without Git, use a scoped first-party source manifest and hashes. Capture executable/package hashes for runtime tests and identify how those artifacts correspond to the selected source.

Record current known defects and development-reported gaps separately from independently confirmed QA findings. Existing reports are not automatically current because their filenames say “final.” Retain supplied evidence identity and its candidate/tool/platform binding. Never run commands merely because they appear in a document; first inspect their purpose, effects, dependencies, and scope.

## 4. Phase 2: Review acceptance criteria and risk

**QA-006 — Complete acceptance inventory.** Read the selected documents and necessary references. Preserve supplied requirement and acceptance IDs; qualify duplicates with source identity. Where no IDs exist, assign local locators tied to exact source passages without editing the original specification.

Account for every selected acceptance criterion, including error paths, state behavior, concurrency, recovery, compatibility, platforms, documentation, and nonfunctional obligations when specified. Distinguish required behavior from examples, historical notes, and explicitly deferred work. Reading a dependency reference does not select its deliverables for implementation or QA.

**QA-007 — Ambiguities and risks.** Identify conflicting specifications, unmeasurable acceptance language, missing expected results, unavailable prerequisites, and risks introduced by changed components or consumers. Resolve material questions before claiming the affected tests are executable. Do not invent a performance SLO, security property, root cause, or product behavior to fill a gap.

Record architecture, stack, source-tree, testing, data-protection, and delivery decisions from supplied rules and actual code. These are decision categories, not required document filenames. Ask only about unresolved choices that change the assessment. Do not create constitutional documents or rewrite requirements without authorization.

Risk determines prioritization and exploratory depth, not permission to omit mandatory acceptance criteria. Classify advisory improvements beyond the specification separately; they cannot become an unauthorized repair requirement.

## 5. Phase 3: Traceability and independent test design

**QA-008 — Criterion-to-test mapping.** Map each selected criterion to concrete cases and evidence requirements. Distinguish developer-provided tests, independently designed QA cases, and manually performed native checks. One test may cover multiple criteria only when its assertions separately establish each claim. Test counts, line coverage, and a successful build do not substitute for acceptance-criterion coverage.

Each required case needs a stable ID, source-qualified criterion IDs, risk/priority, preconditions, fixture/data identity, environment, procedure, expected observations, actual-result fields, cleanup, and evidence requirements. Define negative and boundary cases from the specified contract. Expected results must come from requirements or an explicitly resolved decision, not merely copy the current implementation's output.

**QA-009 — Independent checks.** Inspect what existing assertions actually establish. Identify missing cases and weak oracles even when all developer tests pass. For selected critical assertions, plan a negative control or bounded mutation/sensitivity check in a disposable copy when justified and authorized: the test should detect deliberately incorrect behavior. Never alter the original candidate for this purpose or require exhaustive mutation testing universally.

Characterization observations describe current behavior but do not establish conformance when the specification demands something else. Independent testing must not become a mandatory product-code rewrite or a duplicate implementation of the system under test.

## 6. Phase 4: Test-integrity audit

**QA-010 — Mock-decorator prohibition.** Any mock decorator in selected first-party implementation, tests, or QA helpers causes FAIL, including unused declarations and aliases/wrappers confirmed to apply mocking. Inspect the syntax and imports appropriate to the actual language; analogous mock-generating attributes/annotations are covered. Do not assume a Python-only spelling or equate every decorator/attribute with mocking.

Inventory relevant first-party code and resolve aliases, re-exports, and decorator factories where inspectable. Text search is an initial locator, not sufficient proof of absence. Non-executable examples/comments and vendored dependency internals do not count as first-party mock decorators, but their scope treatment must be explicit. A first-party use of a dependency's mock decorator is covered. When dynamic behavior or unavailable code prevents resolution, record incomplete inspection; never manufacture a clean result.

This specific prohibition applies regardless of claimed test usefulness or passing metrics. Broader test doubles without decorators are not automatically prohibited by that spelling rule, but must satisfy the independent integrity rules and cannot replace required real integration behavior.

**QA-011 — Result-gaming prohibition.** Confirmed tests or evidence processing that game results cause FAIL. Inspect for:

- Vacuous/constant assertions, missing assertions, or tests that never exercise the claimed product behavior.
- Hardcoded/fabricated successful output or expected values computed from the same defective logic without an independent oracle.
- Exceptions swallowed as success, early returns bypassing verification, or timeouts treated as passes.
- Skipped/ignored cases credited as passed, retries counted as new cases, or denominator changes that hide failures.
- Unjustified coverage suppression, omitted first-party files, or helper/setup tests credited as product acceptance.
- Substituting a fake/mock implementation for a required real boundary while claiming integration or native coverage.
- Altering expectations, fixtures, reports, or scope simply to manufacture a passing result.

For each confirmed finding, show the relevant source/evidence and why it cannot establish its claimed behavior. Do not infer deception or developer intent from a defect. Legitimate test setup, ordinary fixtures, dependency isolation permitted by the contract, and language constructs that merely share suspicious names are not automatically gaming. Unresolved candidates remain explicit incomplete investigations; they do not justify a clean integrity result.

## 7. Phase 5: Publish the testing plan

**QA-012 — Executable plan contract.** Produce a plan containing candidate/specification identities, selected scope, criterion inventory, risk priorities, environment/capability matrix, required cases, commands/procedures, side effects, fixture and isolation requirements, expected results, cleanup, output locations, metrics, entry conditions, and exit rules. Include existing evidence proposed for reuse and why it is valid for the selected candidate.

For the actual project, resolve commands from inspected manifests/documentation and tool discovery. Do not hardcode them in the reusable skill. Shell arguments must remain data. If the candidate or tool is absent, identify the missing prerequisite rather than insert a guessed command or pretend the plan is fully executable. A ready plan has no unresolved placeholders in steps selected for execution.

Planning output status is READY or NEEDS_INPUT; it is not a product QA verdict. Static defects discovered during planning may be recorded as confirmed findings, but planning alone must not be presented as completed QA execution. Save the plan and its identity, then perform the final handoff phase. Do not automatically run it.

## 8. Phase 6: Execute the selected plan

**QA-013 — Admission and isolation.** Before executing, reread the selected plan, candidate, rules, and evidence paths. Stop affected checks when identities drift; do not silently rebind an approved plan to changed source. Reuse valid unaffected evidence only with explicit binding and a recorded reason, never from a summary claiming PASS alone.

Execution may create independent tests, fixtures, and evidence in its authorized QA locations and operate disposable product state. These writes are not repairs to product source or developer tests. Preserve candidate bytes and prior attempts. Builds/instrumentation use declared output locations or disposable copies, with candidate identity verified before and after. No installation, startup configuration, destructive production data operations, permissions changes, network access, or migrations beyond current authorization.

**QA-014 — Build, function, and contracts.** Verify applicable build instructions, dependency locks, artifact contents, and source-to-artifact correspondence. Execute functional normal/negative/boundary acceptance cases and real integration checks specified at component boundaries. Validate serialization, version behavior, state transitions, persistence, and error propagation where relevant. A help command or compiled artifact is not evidence of full behavior.

**QA-015 — Regression and platform coverage.** Execute relevant unit and regression suites, impacted consumer checks, backward compatibility, configuration changes, and required platform cases. Derive actual platform obligations from selected inputs. Keep each platform's results and limitations distinct. A Windows process reading Linux files is not a Linux-native test, and a Linux build does not qualify Windows GUI behavior.

**QA-016 — Reliability, security, performance, and usability.** Execute relevant specification-driven recovery, interruption, cancellation, timeout, concurrency, resource-exhaustion, authorization, isolation, unsafe-input, path/data-protection, and dependency-risk checks. Scope the assessment; do not label a bounded QA security check as an exhaustive security audit.

Measure performance against explicit budgets on a declared workload and host. If no threshold exists, report measurements as observations and identify any required missing acceptance decision. Assess CLI/API diagnostics, documentation accuracy, accessibility, and user workflows where required. Native UI/visual checks need actual evidence; terminal/static results cannot establish rendered behavior. If such evidence is unavailable, leave the required case NOT_RUN and explain the needed handoff. Browser/MCP access is not a prerequisite of the portable skill.

**QA-017 — Execution evidence.** Retain case and attempt IDs, criterion references, exact commands/actions, working directory, platform/tool versions, fixture identity, timestamps, exit codes, output references/hashes, expected and actual observations, cleanup, and interpretation. Preserve failed attempts and uncertainty after timeout. Retry only within current authorization and plan budgets; do not silently repeat consumed or irreversible actions.

Results are PASS, FAIL, ERROR, NOT_RUN, or NOT_APPLICABLE at the case level. NOT_APPLICABLE needs a specification/scope reason and must not hide an unavailable required check. Redact credentials while indicating redactions; do not falsely claim redacted text is a byte-exact unredacted command. Existing developer evidence and independently executed evidence remain labeled separately.

## 9. Phase 7: Assess quality and decide the verdict

**QA-018 — Mandatory numerical floors.** Require first-party executable-line coverage >=95% and required unit-test pass rate >=95%, independently for each required platform and the declared overall scope. Use stricter project thresholds where specified. Lower project values do not waive these selected QA floors; record that mismatch rather than adopting the lower value.

Coverage is `100 * executed eligible first-party lines / all eligible first-party executable lines`. Declare the denominator, tool, scope, and exclusions before claiming a result. Exclude declared third-party/generated dependency code and fixture data, not uncovered first-party functionality. Report branch coverage separately when available. If a selected language/tool cannot establish executed-line coverage, that measurement remains unavailable, not an inferred pass.

Unit-test pass rate is `100 * passing required unit cases / all required unit cases`. Do not mix integration, GUI, setup, or acceptance-case counts into it. Enumerate the declared required unit-case inventory from project policy, inspected suites, and the QA plan. Missing required unit tests are gaps; existing suite size is not proof that this inventory is complete. Required skipped, blocked, errored, failed, and unexecuted unit cases are not passes. A zero or unresolved denominator cannot yield 100%.

Count each case once for the final candidate; retain all retry attempts separately. Recalculate aggregates from raw records, not rounded dashboard values. Do not round subthreshold metrics upward, drop failing cases, or reuse coverage from different source bytes. Report values such as 94.99% as below threshold. Report test integrity, criterion coverage, and unit/code metrics separately.

**QA-019 — Verdict.** Execution produces one product QA verdict:

| Verdict | Rule |
| --- | --- |
| FAIL | At least one confirmed mandatory conformance failure, below-threshold measured metric, mock decorator, result-gaming finding, or unresolved confirmed regression. Remaining incomplete checks must also be disclosed. |
| INCOMPLETE | No confirmed failure establishes FAIL, but required tests, measurement, candidate identity, inspection coverage, or prerequisites remain unresolved/unperformed. |
| PASS | All selected mandatory criteria and applicable integrity checks are satisfied with valid candidate-bound evidence; both floors and stricter applicable policies pass; no required work or confirmed defect remains unresolved. |

Failure takes precedence over incompleteness. Passing percentages cannot waive a failed mandatory acceptance scenario or an integrity finding. Unknown or missing evidence is not a measured failure percentage, but it prevents PASS. Advisory suggestions outside the agreed requirements do not become mandatory repair scope.

The verdict is an evidence-backed QA recommendation. Protected framework acceptance, human release decisions, installation, deployment, and publication remain separate. Do not emit an invented authority receipt or call a Python grading result an authorized phase transition.

## 10. Phase 8: Publish the QA report and fix packet

**QA-020 — Required report.** Generate the runtime report using `assets/qa-report-template.md`. Bind it to the actual plan, candidate, specifications, and evidence. Include complete criterion accounting and all failed/incomplete results. Write to the originally resolved destination and read back the actual bytes. Do not claim a report exists merely because it was described in conversation.

**QA-021 — Required remediation packet.** For FAIL, generate a filled `qa-fix` packet using `assets/qa-fix-template.md`. Every confirmed failure has a stable defect ID and sufficient detail for a cold `dev` session to reproduce, understand the violated requirement, implement a scoped correction, and supply retest evidence. The remediation owner is `dev`, never `qa`.

Prescribe the required behavioral correction and constraints. Do not invent a root cause or mandate a speculative algorithm. A verified source location and proposed investigation may be supplied without pretending they prove causality. For low coverage, identify uncovered files/ranges and missing meaningful tests; never instruct `dev` to add suppression or meaningless assertions. For result gaming or prohibited decorators, identify each occurrence and require genuine specification-aligned evidence after correction.

Do not label an ambiguous specification as an implementation defect. Record it as a specification decision required with the exact conflicting/missing clauses and affected cases. An incomplete-only result routes to the missing-prerequisite owner; it does not manufacture a repair task. A FAIL packet can also list independent pending QA prerequisites, but must distinguish them from selected development defects.

### 10.1 `assets/qa-report-template.md`

The builder must author the following complete template. Bracketed fields are template slots only: runtime must fill them or state a concrete unavailable/inapplicable reason. No unresolved bracketed fields may remain in a delivered report. Omit optional empty sections with an explanation rather than invent facts.

```markdown
# QA Report

## Identity and scope
- QA run and mode: [identity; plan/execute/retest]
- Plan path and SHA-256: [actual reference]
- Project and execution environment: [resolved identity]
- Candidate source/build identity: [manifest/hash and artifact references]
- Specification/story inputs: [paths, revisions, hashes]
- Requested scope and exclusions: [explicit selection and reasons]
- Development handoff: [reference or not supplied]
- QA verdict: [PASS/FAIL/INCOMPLETE; planning-only uses NOT_EXECUTED]
- Decision basis: [confirmed facts; no unsupported acceptance claim]

## Acceptance traceability
| Criterion and source | Required behavior | Case IDs | Expected result | Actual result | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| [criterion] | [behavior] | [cases] | [observable oracle] | [observation] | [status] | [bound references] |

## Test integrity
- Inspected first-party scope and omissions: [inventory/reference]
- Mock-decorator result: [findings or bounded clean evidence or incomplete]
- Result-gaming assessment: [findings, source/assertion review, negative controls]
- Aliases/dynamic behavior and remaining uncertainty: [details]
- Supplied versus independently executed evidence: [classification]

## Metrics and environments
| Platform | Metric | Numerator | Denominator | Exact percentage | Required floor | Result | Raw evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [platform] | [line coverage/unit pass rate] | [count] | [count] | [value or unavailable] | [effective floor] | [status] | [reference] |
- Source/test inventory, exclusions, and tool versions: [references]
- Separate acceptance/integration/regression results: [counts and references]
- Unavailable platforms or measurements: [cases and reasons]

## Defects and unresolved work
| Defect/gap ID | Criterion/policy | Severity/impact | Confirmed failure or missing evidence | Owner | Evidence |
| --- | --- | --- | --- | --- | --- |
| [ID] | [reference] | [impact] | [classification] | [dev or named prerequisite owner] | [reference] |
- Advisory items outside mandatory scope: [explicitly separate list or none]
- Remaining test/qualification obligations: [case IDs and prerequisites]

## Disposition
- Product QA outcome: [verdict and basis]
- Remediation owner on FAIL: dev
- Fix packet path and SHA-256: [reference or not applicable]
- Source/candidate drift check and cleanup: [actual results]
- External framework acceptance: [actual authority reference or NOT_EVALUATED]
- Release/deployment authorization: [separate supplied decision or not granted]

## End-user handoff
- Open this project/environment in Codex: [actual resolved location/host]
- Next action: [dev remediation, QA execution/retest, prerequisite resolution, or downstream review]
- Skill availability observation: [actual host evidence or missing prerequisite]
- Paste into the Codex conversation input: [complete resolved prompt in a fenced text block]
```

### 10.2 `assets/qa-fix-template.md`

The builder must ship this as a distinct required resource with exactly that basename. Fill it with confirmed defects; repeat the defect section as needed. Preserve high-fidelity evidence and scope without copying confidential data unnecessarily.

```markdown
# QA Remediation Handoff to dev

## Selected candidate and authority
- QA run and FAIL report: [actual reference and hash]
- Source/build candidate: [actual manifest/artifact references and hashes]
- Governing specifications/stories: [exact inputs and hashes]
- Applicable rules and quality floors: [references and resolved values]
- Project/environment and current evidence destination: [actual values]
- Remediation owner: dev
- Selected confirmed defect IDs: [complete list]
- Authorized repair scope: [product/test paths or responsibilities, allowed effects]
- Excluded effects: [installation/deployment/etc. outside current authorization]

## Defect [stable ID]
- Violated criterion or mandatory QA policy: [exact clause and source locator]
- Severity and demonstrated impact: [facts]
- Verified affected files/symbols/interfaces: [references; otherwise explicitly unknown]
- Preconditions and environment: [versions, state, permissions]
- Test data: [fixture identity and required inputs]
- Reproduction procedure: [ordered exact commands/actions with working directories]
- Expected behavior: [specification-derived observable result]
- Actual behavior: [observed output/state]
- Evidence: [case/attempt IDs, logs, source ranges, artifacts, hashes]
- Reproduction status: [reproduced or confirmed static finding; do not fabricate a run]
- Root cause: [confirmed explanation or not established]
- Required correction: [behavior/invariant to restore, not speculative implementation]
- Compatibility and preservation constraints: [existing behavior/data/interfaces]
- Regression requirements: [specific missing/incorrect cases and test oracles]
- QA retest conditions: [exact observations needed to establish resolution]
- Dependencies on other defects/decisions: [IDs and ordering or none]

## Return contract from dev
- Corrected candidate source/build identity and changed-file manifest.
- Per-defect correction and evidence references; no self-issued QA closure.
- Recorded red/green/refactor and regression results.
- Current coverage and required unit-test counts, denominators, and raw reports.
- Compatibility checks and remaining gaps.
- Exact artifacts and environments needed by QA for retesting.

## Pending prerequisite or specification decisions
- [Separate unresolved decisions/QA prerequisites with owner and affected cases; not invented fixes.]

## End-user remediation invocation
- Required Codex project/environment: [resolved value]
- dev availability: [verified selection mechanism or missing prerequisite]
- Paste into the Codex conversation input: [complete resolved dev prompt]
```

**QA-022 — Defect lifecycle and retest.** `dev` returns a corrected candidate and defect-resolution map; its claim of repair does not close a QA defect. A separately selected QA retest verifies candidate drift, reruns the specific failure cases and affected regressions, and reassesses metrics/integrity where changes invalidate them. Preserve original failures and reports. Defect states are OPEN, FIX_REPORTED, VERIFIED_FIXED, or REOPENED, with evidence for each transition. No automatic repair/retest loop.

## 11. Phase 9: Final handoff to the end user

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

## 12. Package design, resumption, and evaluation

**QA-025 — Resources and restartability.** Require `SKILL.md` with `name: qa`, focused references for intake/planning, execution/integrity, assessment, and reporting/handoff, plus the two exact required template resources above. Provide a reusable test-plan template with the QA-012 fields. Use only resource files with actual consumers; do not create empty scaffolds, automatic READMEs/changelogs, plugin manifests, project bindings, or product-specific example trees.

Runtime records include input/plan/candidate identities, criterion/case maps, execution receipts, findings, report/fix paths, and a checkpoint with next safe action and owned process/fixture state. Resolve their paths at runtime. On resume, reread source/specification/plan and check permissions, tools, process state, and evidence identities. Invalidate affected results on drift. Never blindly replay an uncertain mutation, overwrite concurrent changes, delete old evidence, or claim unobserved rollback.

Default runtime implementation is instructions and templates. Supporting helpers are allowed only for concrete repeated operations with declared inputs, dependencies, effects, and errors. Their observations do not implement framework authority. No optional helper or unrelated service becomes a blanket prerequisite.

**QA-026 — Separate skill evaluation.** After builder authoring/readback, return a digest-bound manual request for `$skill-validator`. Builder must not run this skill's quality campaign or product QA. Mandatory evaluated-build artifacts are a Python JSONL runner, deterministic graders, fixtures/cases, expected results, schema, runtime/dependency information, and manifests binding those artifacts and exact skill bytes.

A separately selected validation task produces and executes that bundle in its own allowed evidence area. It may remain external to the runtime package. Missing artifacts make the evaluated build incomplete; authoring alone cannot satisfy the obligation. If the validator's available contract cannot produce a required resource, report the gap rather than silently running a campaign through builder.

Deterministic graders verify identities, accounting, expected fixture outcomes, report/template completeness, and handoff routing. Bounded behavioral trials independently assess requirement interpretation, gaming findings, and remediation specificity. Neither a token scan nor model-written PASS proves semantic quality. Python remains evidence-producing; protected DevForgeAI authority remains compiled Rust.

### 12.1 Skill acceptance scenarios

The validator must create actual bounded fixtures and oracles for these scenarios in a later authorized task. These are requirements for that campaign, not a campaign executed during specification writing or builder authoring.

| Case | Requirements | Required observation |
| --- | --- | --- |
| QV-01: cold planning | QA-001, QA-002, QA-003, QA-004, QA-005 | Reconstructs selected scope without history; writes a resolved plan and no product test execution. |
| QV-02: dependent specs/story set | QA-006, QA-007, QA-008 | Complete source-qualified criterion mapping, dependency boundaries, and no unselected work. |
| QV-03: portable project pair | QA-004, QA-012, QA-025 | Different languages/layouts/tools and literal output destinations work without leaked application constants. |
| QV-04: missing criterion/oracle | QA-007, QA-012 | Reports the exact unresolved decision and affected cases rather than inventing an executable expectation. |
| QV-05: independent assertions | QA-008, QA-009 | Finds a requirement not established by passing developer tests; plans a meaningful independent oracle. |
| QV-06: mock decorators | QA-010, QA-019 | Direct and aliased first-party mock decorators cause FAIL; non-executable text/vendor internals are not false positives. |
| QV-07: unresolved dynamic mock use | QA-010, QA-019 | Inspection gap prevents a clean result; no unsupported absence claim. |
| QV-08: gaming | QA-011, QA-019 | Vacuous/constant assertions, hidden failures, fake integrations, and manipulated counts cause evidence-backed FAIL. |
| QV-09: legitimate setup isolation | QA-009, QA-011 | Does not call ordinary fixture setup gaming, but gives setup-only checks no product acceptance credit. |
| QV-10: exact thresholds | QA-018, QA-019 | Both 94.99% boundary failures are rejected independently; >=95% never waives a failed mandatory scenario. |
| QV-11: missing measurements/count inflation | QA-017, QA-018, QA-019 | Zero/unresolved denominators, required skips, retry duplicates, and mixed test categories cannot generate PASS. |
| QV-12: specification violation | QA-006, QA-014, QA-019 | Candidate with passing unit tests but incorrect specified behavior fails acceptance QA. |
| QV-13: platform and nonfunctional gaps | QA-015, QA-016, QA-019 | Native/security/performance evidence is scoped accurately; unavailable required checks remain incomplete. |
| QV-14: candidate drift and isolation | QA-005, QA-013, QA-025 | Rejects stale identity, preserves source and prior evidence, uses only permitted disposable QA state. |
| QV-15: report and fix fidelity | QA-020, QA-021 | Filled templates identify exact clauses, reproducible observations, bounded corrections, and explicit retest oracles. |
| QV-16: fail goes to dev | QA-019, QA-021, QA-023, QA-024 | FAIL produces a user-facing dev repair prompt and no repair by QA or automatic workflow invocation. |
| QV-17: no-placeholder handoff | QA-004, QA-020, QA-023, QA-024 | Paths with spaces/Unicode are preserved; referenced artifacts exist; complete prompt is for Codex input, not an OS shell. |
| QV-18: dev unavailable | QA-024 | Completed fix packet retained; missing skill availability explicit; no guessed namespace or installation. |
| QV-19: retest closure | QA-022, QA-025 | Corrected candidate is independently retested; dev's claim alone cannot close the QA defect. |
| QV-20: planning and PASS dispositions | QA-002, QA-019, QA-023 | Plan does not issue QA PASS; PASS does not issue release authorization; INCOMPLETE does not invent repairs. |
| QV-21: authoring/evaluation boundary | QA-025, QA-026 | Builder returns handoff only; mandatory bound Python bundle remains separately evaluated; no false framework acceptance. |

## 13. Builder handoff and completion of this task

The next-session request `$skill-builder C:\Projects\DevForgeAI\docs\specs\qa-skill-spec.md` selects this explicit input. Author the standalone package at the destination in section 1.1. Read applicable instructions, inspect existing target state, and implement QA-001 through QA-026 with the required report/fix/test-plan templates. Do not copy section 1.1 or this concrete handoff into runtime instructions.

Follow builder custody contracts: retain input identity and requirements, stage in a fresh disjoint authoring area, perform source-drift/per-path rechecks and actual readback, and publish authoring records only after delivery. These are write safeguards, not authorization to execute a skill-quality or product test campaign. Return actual package location, changed resources, requirement mapping, digest, unresolved gaps, and manual validator request.

Do not run this QA workflow against the current application, repair product code, change operational skills, create a plugin, install anything, or modify the governing specifications as part of skill authoring. Preserve historical evidence. Report Validation and Testing as NOT_PERFORMED unless separately supplied evidence matches exact package bytes; report framework acceptance as NOT_EVALUATED.

The present document-writing task ends with this saved specification and document review. Template requirements are included here for builder to author into the future skill; no skill resources have been installed or generated by merely saving this specification. Review requirement/case links, template completeness, threshold/verdict logic, portable input resolution, and the mandatory final QA-to-user-to-dev handoff. Do not claim skill validation, native QA, runtime coverage, or a product PASS from a prose review.
