---
name: qa
description: >
  Plan and run independent specification-driven QA: assess a development candidate against
  explicitly selected specifications or stories and report an evidence-backed verdict. Use
  when the user asks to test, QA, verify or validate what was built, for iteration, sprint
  or release-candidate testing, for a test plan, for test-integrity review, or to retest
  selected defects after a fix. Also use when they describe the need without naming it, as
  in "check whether this actually meets the spec" or "is this ready to ship". Do not use for
  repairing the product, validating a skill package, skill authoring, installation,
  deployment, or standalone architecture research.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# Independent Specification-Driven QA

Assess the selected product against its requirements, independently of development completion claims. Work from explicit inputs in a cold Claude Code session. Discover the actual language, project layout, tools, platforms and evidence destination; no installed framework, binding, index, plugin, browser or Git repository is intrinsically required.

## Select the mode and scope

Default to **run** for an ordinary product QA request, including this skill with selected product specifications alone. Require the project, selected specifications/stories, scope and applicable rules. Bind current source including relevant local changes unless another candidate is selected; a saved plan is not required for a full run. A sprint needs its selected story set or an unambiguous scope manifest. Read dependency references for context without selecting their deliverables. A general QA question or pasted procedure alone does not initiate tests.

**Plan** means an explicit test-plan, planning-only or no-execution request: inspect and write selected planning/report artifacts without product builds, tests, executable harness generation or product-state mutation. Host planning/write restrictions override desired run intent; report unsaved artifacts where writes are prohibited. Claude Code's Plan mode is such a restriction, and it is stricter than planning-only intent: it prohibits the plan and report writes this skill would otherwise perform, so report those artifacts as unsaved with their intended paths rather than relocating them. **Execute** selects a saved plan and candidate. **Retest** selects a corrected candidate and defect set with a saved or newly derived bounded plan. These are conversational intents, not flags. Never promote earlier planning-only intent into execution or automatically invoke dev or another QA session.

An ordinary full QA request authorizes necessary inspection, isolated QA fixtures/harnesses, local builds, tests, instrumentation, reports and cleanup of QA-owned disposable state within the selected scope and host permissions. Preserve existing session authorization. Discover before asking for essential missing decisions or additional effects; where the options are known and bounded, ask with `AskUserQuestion`, and continue independent permitted work while a decision is pending. Installation, persistent startup/service changes, deployment, migrations, destructive real-data actions and new remote targets need applicable authorization. Use host approval mechanisms when required.

`Bash` is granted unscoped, because the build, test, coverage and static-analysis commands come from the runtime project and cannot be fixed in a command pattern here. That breadth means the allowlist enforces none of the prohibitions above: no product repair, no installation, no deployment, no persistent startup change. Those are obligations this workflow keeps, not boundaries the host checks.

## Follow the selected workflow

1. Read [intake and planning](references/intake-planning.md). Bind exact input/candidate bytes and literal output paths, inventory every selected criterion and design independent oracles. Use [the test-plan template](assets/test-plan-template.md). Declare each check READY or BLOCKED with prerequisites/dependents, authorized preparation and complete metric collection boundaries. Plan NEEDS_INPUT blocks only dependent work, not the ready independent subset.
2. Read [execution and integrity](references/execution-integrity.md) and [assessment](references/assessment.md). Save/read back the plan, then inspect selected first-party code, tests and evidence processing for integrity failures before product tests; inspect new QA helpers before use. Explicit plan mode remains read-only inspection/design plus allowed plan/report writes and ends with the planning-only handoff.
3. For run, execute or retest, recheck identity and effects. After plan readback and applicable integrity inspection, give a brief progress update and proceed into ready preparation/execution in the same invocation. Do not ask the user to select the plan just generated or end with an execute prompt while ready independent work remains. Preserve candidate bytes and prior attempts; QA must not repair product source or developer tests.
4. Classify each issue using demonstrated behavior. Confirmed integrity failure, valid completed subthreshold metric, or critical authorization/security/data-preservation defect immediately stops the whole test run. Launch no further tests, builds, coverage campaigns or investigative reproductions; safely contain owned in-flight work and preserve remaining NOT_RUN obligations with the trigger ID. Ordinary mandatory defects retain eventual FAIL while safe independent checks continue. Local prerequisite/harness gaps block dependents only; uncontained safety/ownership or identity problems stop the run. Apply these rules as new material/results arrive.
5. Assess valid evidence. Both first-party executed-line coverage and required **unit-test** pass rate must meet >=95%, or stricter project floors, per required platform and overall. Keep other test categories and applicable project-wide suite thresholds separate. Do not finalize partial collection as a failing percentage. FAIL takes precedence over INCOMPLETE; PASS requires all mandatory obligations, integrity and valid metrics with no required gaps.
6. Read [reporting, restart and user handoff](references/reporting-handoff.md). Fill [the QA report](assets/qa-report-template.md) for every completed, stopped, blocked or planning-only invocation; on FAIL also fill [the qa-fix packet](assets/qa-fix-template.md). Read back artifacts at the bound destination and deliver the outcome-specific handoff after ready work is exhausted or a genuine stop/blocker prevents continuation. Report exact delivery failures without changing destination silently.

Track intent, plan readiness, execution status (NOT_STARTED/IN_PROGRESS/COMPLETED/STOPPED) and verdict separately. Explicit planning-only uses NOT_EVALUATED as a non-verdict marker, never NOT_EXECUTED as a verdict. A full run can establish FAIL from confirmed static evidence with execution NOT_STARTED. Gaps alone yield INCOMPLETE; a stopped run never claims complete testing.

## Preserve evidence and ownership

Bind the literal selected evidence destination before writing. Keep input/plan/candidate identities, criterion/case maps, receipts, findings, report/fix paths and a checkpoint with owned process/fixture state and next safe action. On resume, reread identities, permissions, tools and state; invalidate affected evidence on drift and never blindly replay uncertain effects.

Any confirmed first-party mock decorator, including resolved aliases or analogous mocking attributes, is prohibited even when unused. Unresolved dynamic inspection is a gap. Search alone cannot establish absence. Confirm gaming from the source and claimed behavior, without inferring developer intent; legitimate setup is not automatically gaming and earns no product acceptance credit by itself.

Keep FAIL repair ownership with **dev**. Return a complete, resolved conversation prompt after verifying host skill availability and artifact identities. If dev is unavailable, retain the fix packet and report the discovery prerequisite. Never substitute QA as fixer, auto-send a handoff or install the missing skill. Only independent QA retest can establish QA defect closure.

Two of those boundaries are structural here rather than asserted: `Skill` is absent from `allowed-tools`, so this workflow cannot invoke `dev` or the package validator even when a later instruction asks it to — the handoff necessarily stops at the prompt and the packet. `Task` is absent too, which means QA independence from development completion claims is a discipline this session keeps, not a fresh context the host supplies.

Reports are QA assessments, not protected framework acceptance or release authorization. Respect any project-required external authority without simulating it. Do not install, deploy, change startup settings or broaden effects beyond current authorization. This skill's own package evaluation is a separate skill-validator task; authorized product QA execution remains this skill's responsibility.
