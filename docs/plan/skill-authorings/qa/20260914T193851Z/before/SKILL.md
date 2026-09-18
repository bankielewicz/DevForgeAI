---
name: qa
description: Plan and execute independent product QA against explicitly selected specifications or stories and a development candidate. Use for iteration, sprint, or release-candidate testing, test-integrity review, evidence-backed assessment, and selected defect retests. Product repair, skill-package validation, authoring, installation, deployment, and standalone architecture research are separate tasks.
---

# Independent Specification-Driven QA

Assess the selected product against its requirements, independently of development completion claims. Work from explicit inputs in a cold Codex CLI session. Discover the actual language, project layout, tools, platforms and evidence destination; no installed framework, binding, index, plugin, browser or Git repository is intrinsically required.

## Select the mode and scope

Default to **plan** unless execution is explicit. Require the project, selected specifications/stories, scope and applicable rules. A sprint needs its selected story set or an unambiguous scope manifest. Read dependency references for context without selecting their deliverables. Ask only for missing decisions that affect the assessment.

Planning permits relevant read-only inspection and selected plan/evidence writes. Do not run product tests, build, generate executable harnesses, install dependencies or mutate product state. Under host Plan mode, provide the plan in conversation without file writes. Planning status is READY or NEEDS_INPUT, never product QA PASS.

**Execute** additionally requires a concrete selected plan and candidate and authorization for test effects. **Retest** requires a selected corrected candidate and defect set; it is a separate execution invocation. A pasted procedure or saved plan does not authorize execution. Do not automatically invoke dev or another QA session.

## Follow the selected workflow

1. Read [intake and planning](references/intake-planning.md). Bind exact input/candidate bytes and output paths, inventory every selected criterion, identify risks and missing decisions, and design independent oracles. Use [the test-plan template](assets/test-plan-template.md).
2. Read [execution and integrity](references/execution-integrity.md) and [assessment](references/assessment.md) while designing the plan. Inspect relevant test assertions and syntax within read-only planning limits. Include the actual required execution, integrity and metric procedures in the plan. In plan mode, publish/read back the plan and go directly to the final handoff.
3. In authorized execute/retest mode, reread the selected plan, rules and candidate; stop affected checks on drift. Follow execution/integrity instructions, preserve candidate bytes and prior attempts, and record exact case-bound observations. QA may author independent tests and fixtures in authorized QA locations; it must not repair product source or developer tests.
4. Apply assessment rules. Both first-party executed-line coverage and required **unit-test** pass rate must meet >=95%, or stricter project floors, per required platform and overall. Keep other test categories separate. Confirmed mandatory failures, prohibited mock decorators, gaming or unresolved confirmed regressions cause FAIL. Otherwise missing required evidence causes INCOMPLETE. PASS requires all mandatory obligations and both metrics with current evidence. Failure takes precedence over incompleteness.
5. Read [reporting, restart and user handoff](references/reporting-handoff.md). Fill [the QA report](assets/qa-report-template.md); on FAIL also fill [the qa-fix packet](assets/qa-fix-template.md). Read back actual artifacts at the originally resolved destination, then deliver the outcome-specific user handoff. Every mode ends with this step.

## Preserve evidence and ownership

Bind the literal selected evidence destination before writing. Keep input/plan/candidate identities, criterion/case maps, receipts, findings, report/fix paths and a checkpoint with owned process/fixture state and next safe action. On resume, reread identities, permissions, tools and state; invalidate affected evidence on drift and never blindly replay uncertain effects.

Any confirmed first-party mock decorator, including resolved aliases or analogous mocking attributes, is prohibited even when unused. Unresolved dynamic inspection is a gap. Search alone cannot establish absence. Confirm gaming from the source and claimed behavior, without inferring developer intent; legitimate setup is not automatically gaming and earns no product acceptance credit by itself.

Keep FAIL repair ownership with **dev**. Return a complete, resolved conversation prompt after verifying host skill availability and artifact identities. If dev is unavailable, retain the fix packet and report the discovery prerequisite. Never substitute QA as fixer, auto-send a handoff or install the missing skill. Only independent QA retest can establish QA defect closure.

Reports are QA assessments, not protected framework acceptance or release authorization. Respect any project-required external authority without simulating it. Do not install, deploy, change startup settings or broaden effects beyond current authorization. This skill's own package evaluation is a separate skill-validator task; authorized product QA execution remains this skill's responsibility.
