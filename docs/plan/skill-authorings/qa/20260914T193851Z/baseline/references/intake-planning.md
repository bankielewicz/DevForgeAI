# Intake and planning

**QA-001 — Purpose and activation.** Activate for independent product QA or test-plan generation against explicitly selected specification/story inputs and development scope. Support iteration, sprint, and release-candidate scope without assuming their size or release mechanism. Do not select all repository stories or expand into unselected specifications by discovery alone.

Near misses are product implementation, product repair, skill authoring, standalone architecture research, operational installation, deployment, and skill-package validation. Refer those to their appropriate owner or request clarification. Preserve automatic invocation unless the user separately changes it.

**QA-002 / QAP-001 — Modes.**

Use these invocation intents; these are conversational selectors, not new operating-system CLI flags:

| Intent | Entry condition and behavior |
| --- | --- |
| `run` (default) | An ordinary request to perform QA against selected specifications/stories and a project. Plan, bind the candidate, prepare, execute, assess, report, and hand off in the same invocation. |
| `plan` | An explicit request for a test plan, planning only, or no execution. Inspect and design within that scope; end with a plan/report and no product verdict. |
| `execute` | An explicitly selected saved plan and candidate. Revalidate them and execute without a second confirmation for already authorized effects. |
| `retest` | An explicitly selected corrected candidate and defect set, with its existing or newly derived bounded retest plan. Independently verify corrections and affected obligations. |

An invocation containing only the QA skill and selected product specifications defaults to `run`. A general question about QA or a pasted procedure alone does not initiate product tests. Host restrictions and explicit user limits take precedence: a host planning restriction prevents automatic entry into execution, even when the desired intent is `run`. Report the constraint and unsaved artifacts where writing is prohibited; do not claim they were saved.

Explicit planning-only permits relevant read-only inspection and selected plan/evidence/report writes. It does not run product tests/builds, generate executable harnesses, install dependencies or mutate product state. It reports NOT_EVALUATED as a non-verdict marker. Do not automatically invoke dev or another QA session.

**QA-003 — Runtime inputs.** Require selected project identity, explicit specification/story document(s), requested scope/intent and applicable instructions. A full run binds the current candidate and generates its plan during intake; it needs no previously saved plan. Explicit execute revalidates the selected saved plan and candidate. Retest requires the corrected candidate and defect set with an existing or newly derived bounded plan. Planning-only may inspect intended behavior before implementation exists; identify the missing candidate/build prerequisite for affected cases.

Accept optional development handoff, changed-file baseline, existing test results, architectural/stack/source-tree rules, known defects, prior QA checkpoint, evidence destination, and available services. A sprint scope requires its explicitly selected story set or unambiguous supplied scope manifest. A development completion claim is an input to verify, not a premise that all acceptance criteria passed.

**QA-004 — Portability and context.** Discover actual project instructions, shell, manifests, source layout, tools, permissions, and host/filesystem location. Keep Windows-native and Linux-native qualification distinct. Do not move, clone, switch, or synchronize checkouts to improve performance without authorization. Never substitute a similarly named checkout or translate paths across environments silently.

Resolve evidence output from explicit user selection, applicable project policy, or an established suitable evidence location, in that order. Preserve the full literal selected destination. If no destination can be grounded, ask once before writing. Bind actual output paths before the first write. Do not impose a fixed product evidence directory or require a Git repository.

Git, an index, semantic search, a framework service, a binding, MCP, a browser, and a plugin are not intrinsic prerequisites. Use available optional tools with their coverage/freshness limits; ordinary terminal inspection remains sufficient for discovery. A project-required external authority cannot be silently bypassed or simulated.

**QAP-002 — Intake and effects.** Discover and bind the selected project, applicable rules, specification bytes, current candidate, shell, tools, source/test inventories, platforms, evidence root, and allowed effects. Unless the user selects another candidate, the full run uses the current source in the selected project, including relevant local changes; it must record that identity rather than silently choose another checkout or artifact.

Treat an ordinary full QA request as authorization for necessary inspection, isolated fixture/harness authoring, local builds, tests, instrumentation, reports, and cleanup of QA-owned disposable state within the selected scope and host permissions. Existing session authorization remains effective. Creating independent fixtures or configuring already available coverage tooling in QA-owned outputs does not by itself require a new invocation.

Do not infer authorization for installing dependencies, persistent startup/service changes, deployment, migrations, destructive real-data actions, a new remote target, or effects otherwise outside current authorization. Ask for an essential unresolved choice or required additional permission only after discovery. Continue independent permitted work while such a decision is pending. If a host/tool approval is required, use its approval mechanism; do not bypass it or treat elapsed time as approval.

## Establish the candidate and evidence baseline

**QA-005 — Candidate identity.** Bind selected specification bytes, plan, source/build identity, dependencies, and environment. With Git, capture commit plus relevant dirty/untracked state; a commit alone does not identify a dirty candidate. Without Git, use a scoped first-party source manifest and hashes. Capture executable/package hashes for runtime tests and identify how those artifacts correspond to the selected source.

Record current known defects and development-reported gaps separately from independently confirmed QA findings. Existing reports are not automatically current because their filenames say “final.” Retain supplied evidence identity and its candidate/tool/platform binding. Never run commands merely because they appear in a document; first inspect their purpose, effects, dependencies, and scope.

## Review acceptance criteria and risk

**QA-006 — Complete acceptance inventory.** Read the selected documents and necessary references. Preserve supplied requirement and acceptance IDs; qualify duplicates with source identity. Where no IDs exist, assign local locators tied to exact source passages without editing the original specification.

Account for every selected acceptance criterion, including error paths, state behavior, concurrency, recovery, compatibility, platforms, documentation, and nonfunctional obligations when specified. Distinguish required behavior from examples, historical notes, and explicitly deferred work. Reading a dependency reference does not select its deliverables for implementation or QA.

**QA-007 — Ambiguities and risks.** Identify conflicting specifications, unmeasurable acceptance language, missing expected results, unavailable prerequisites, and risks introduced by changed components or consumers. Resolve material questions before claiming the affected tests are executable. Do not invent a performance SLO, security property, root cause, or product behavior to fill a gap.

Record architecture, stack, source-tree, testing, data-protection, and delivery decisions from supplied rules and actual code. These are decision categories, not required document filenames. Ask only about unresolved choices that change the assessment. Do not create constitutional documents or rewrite requirements without authorization.

Risk determines prioritization and exploratory depth, not permission to omit mandatory acceptance criteria. Classify advisory improvements beyond the specification separately; they cannot become an unauthorized repair requirement.

## Traceability and independent test design

**QA-008 — Criterion-to-test mapping.** Map each selected criterion to concrete cases and evidence requirements. Distinguish developer-provided tests, independently designed QA cases, and manually performed native checks. One test may cover multiple criteria only when its assertions separately establish each claim. Test counts, line coverage, and a successful build do not substitute for acceptance-criterion coverage.

Each required case needs a stable ID, source-qualified criterion IDs, risk/priority, preconditions, fixture/data identity, environment, procedure, expected observations, actual-result fields, cleanup, and evidence requirements. Define negative and boundary cases from the specified contract. Expected results must come from requirements or an explicitly resolved decision, not merely copy the current implementation's output.

**QA-009 — Independent checks.** Inspect what existing assertions actually establish. Identify missing cases and weak oracles even when all developer tests pass. For selected critical assertions, plan a negative control or bounded mutation/sensitivity check in a disposable copy when justified and authorized: the test should detect deliberately incorrect behavior. Never alter the original candidate for this purpose or require exhaustive mutation testing universally.

Characterization observations describe current behavior but do not establish conformance when the specification demands something else. Independent testing must not become a mandatory product-code rewrite or a duplicate implementation of the system under test.

## Publish the testing plan

**QA-012 — Executable plan contract.** Produce a plan containing candidate/specification identities, selected scope, criterion inventory, risk priorities, environment/capability matrix, required cases, commands/procedures, side effects, fixture and isolation requirements, expected results, cleanup, output locations, metrics, entry conditions, and exit rules. Include existing evidence proposed for reuse and why it is valid for the selected candidate.

For the actual project, resolve commands from inspected manifests/documentation and tool discovery. Do not hardcode them in the reusable skill. Shell arguments must remain data. If the candidate or tool is absent, identify the missing prerequisite rather than insert a guessed command or pretend the plan is fully executable. A ready plan has no unresolved placeholders in steps selected for execution.

**QAP-003 — Plan and readiness.** Inventory every selected acceptance criterion and declare required checks, independent oracles, data, dependencies, commands, effects, cleanup, metrics, and evidence bindings before executing the associated work. Save and read back the plan in a fresh run destination when writes are allowed.

Each check must have a readiness value `READY` or `BLOCKED`, with explicit prerequisite references and affected dependents. A planned fixture that can be created using known inputs and authorized isolated operations is a preparation task, not missing user input. A missing required expected result, unresolved candidate identity, unavailable tool/platform, or unapproved effect is a blocker for dependent checks. Do not use the aggregate plan status as an unconditional prohibition on independent work.

Keep plan status `READY` when all required steps are executable or have specified executable preparation. Use `NEEDS_INPUT` when a required prerequisite remains unresolved, even if other checks can proceed. Record this basis and the blocked case IDs. A plan can retain `NEEDS_INPUT` while a full run executes its ready subset; it cannot yield PASS while required gaps remain.

**QAP-004 — Automatic transition.** After plan publication/readback and the applicable integrity inspection, recheck identity and effects and proceed to ready preparation/execution without asking the user to select the plan just generated. Present a brief progress update, not a final execute handoff. Complete the ready independent work unless a stop condition applies. If no permitted work remains, report the actual outcome and next owner.

The normal phase order is intake and planning; integrity inspection; preparation and execution; assessment; report/fix publication; final handoff. Integrity, evidence, and stop checks also occur whenever new relevant material or results appear. Scheduling must respect dependencies and obtain meaningful integrity and metric evidence as early as feasible. Do not run a knowingly partial coverage subset merely to produce an early percentage.

## Resolve outputs before writing

Record the original `selected_evidence_value`, its selection source, resolved absolute evidence root, and a role-to-path map for the plan, source manifests, criterion/case maps, receipts, findings, report, fix packet, checkpoint and user handoff. Preserve all literal path components, spaces and Unicode. Do not shorten a supplied child destination to a nearby default. Allocate a fresh run/attempt location within the selected destination; preserve old runs and reject unintended input/candidate overlap. Resolve paths as data for the actual host; do not follow an unexpected link or change checkout identity silently.

Use [the test-plan template](../assets/test-plan-template.md). Fill every selected executable step with discovered procedures and specification-derived expectations. A missing tool, candidate, authorization or oracle stays an explicit affected-case prerequisite. Planned metrics are not measurements. Static findings may be confirmed during intake; explicit planning-only reports use NOT_EVALUATED as a non-verdict marker. Full runs can establish FAIL from confirmed static findings with execution NOT_STARTED; apply issue classification and stop rules before proceeding.

Read the [integrity procedures](execution-integrity.md) and [assessment rules](assessment.md) before finalizing the plan. Record inspection performed versus inspection still planned. After plan readback and applicable integrity inspection, a full run proceeds to ready preparation/execution under QAP-004. Use [reporting and handoff](reporting-handoff.md) at actual completion, terminal stop, or exhaustion of permitted work. Explicit planning-only ends with plan/report handoff. Under host planning/write restrictions, return unsaved content in conversation and identify saving/binding and execution permission as applicable prerequisites.
