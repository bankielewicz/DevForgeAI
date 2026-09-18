---
id: DFF-08
status: planning-baseline
implementation_readiness: not-ready
updated: 2026-09-17
---

# Quality, evidence, and delivery

## Purpose and ownership

This document owns the relationship between development verification, independent QA, defect remediation, delivery readiness, protected framework acceptance, and release authorization. It is a planning baseline and does not qualify a candidate or activate a gate. The [index](index.md) and [foundation](foundation.md) define the documentation boundary; [Rust guardrails](guardrails-and-rust-runtime.md) owns proposed authoritative decisions.

The framework must report what was actually established. Completed source edits, passing tests, a QA verdict, an authority receipt, and permission to deploy are distinct facts. A missing runtime cannot be replaced by a report containing an `accepted` field. An agent stopping with unresolved work does not complete that work.

## Inputs, outputs, and dependencies

Inputs include the selected [work items](work-items-and-dependencies.md), governing requirements, declared project quality policy, exact candidate and dependency identities, required platform/case inventory, independent expected outcomes, and existing defect evidence. Applicable tools, commands, permitted effects, measurement boundaries, and evidence destinations must be discovered before execution.

Outputs are executed observations, retained raw reports, case/requirement mappings, findings, explicit gaps, and the corresponding bounded handoff. Producer identity, command, working directory, platform, tool versions, exit/timeout status, timestamps, and relevant input/output digests make evidence assessable. A setup failure is reported as setup failure; it cannot demonstrate the intended product defect.

[Core workflows](core-workflows.md) connects development and assessment. [Project policy](project-context-and-policy.md) owns how a selected project's rules are identified. [Skills and project expertise](skills-and-project-expertise.md) owns specialist guidance, not the authority to waive obligations.

## Confirmed decisions and proposed behavior

DevForgeAI's own framework implementation remains subject to its [repository rules](../../../AGENTS.md): compiled Rust authority, applicable red/green/refactor/QA execution, executed-line coverage and required-case pass rate independently at least 95%, and separate required-platform reporting. This planning baseline does not change those rules.

A portable framework must identify the selected project's applicable quality policy instead of silently requiring every managed product to use Rust or inheriting every DevForgeAI development convention. This portability direction does not override current skill contracts. Any conflict is resolved explicitly before relying on a different policy.

For programming under the repository's rules, retain the focused expected failure before production changes, the passing implementation result, and affected post-refactor/regression evidence. Refactoring does not require needless edits when no justified improvement exists. Test changes require an explanation of what expectation changed and which evidence remains applicable. This baseline does not adopt an automatic rule that every test edit restarts every earlier phase; impact and invalidation semantics remain to be specified.

Independent QA derives its oracle from requirements and relevant contracts, not development completion claims. It preserves candidate bytes and independent fixtures, records demonstrated findings, and returns repairs to development. Only an independent retest can establish QA finding closure. Earlier failing attempts remain retained; a later pass is new evidence rather than a rewritten history.

| Outcome | Meaning and boundary |
| --- | --- |
| Candidate delivered | Identified source/artifacts exist and were read back; quality is separate. |
| Checks completed | The declared executions finished with recorded results; completion can include failures. |
| QA assessment | Independent assessment of the selected candidate and scope; gaps and failures remain visible. |
| Delivery readiness | Required checks, candidate identity, and delivery prerequisites are satisfied under the selected policy, with no unmet mandatory obligations; this is not permission to act. |
| Framework acceptance | A qualified Rust authority has validated its protected predicates and issued a verifiable result. |
| Release authorization | The selected publication/deployment effect is permitted through the applicable authorization boundary. |

The eventual runtime must bind decisions to the evaluated candidate and reject stale or missing required evidence. Hooks, model summaries, and editable manifests cannot establish acceptance. Exact transition predicates and protected actor identities belong to the Rust contract, not this table.

## Integration, user-interface evidence and authorized delivery

Parallel story or branch assessments do not establish the behavior of their combined candidate. The work set must retain shared integration acceptance and identify who assembles and assesses that candidate. Changed source, dependencies or merge results require applicable evidence for the actual delivered combination; historical branch passes remain attributed to their original scope. Exact evidence-invalidation rules remain DFF-08-Q3.

Where an application has selected UI acceptance requirements, exercise the real required interactions and verify their observable effects across the relevant frontend, API and persistence boundaries. For example, a submitted form may require checking the response, stored state and subsequent retrieval rather than merely recording a successful click. Browser automation such as Playwright is a tool choice when available and appropriate, not a universal CLI-product gate. Missing required runtime/visual checks remain NOT_RUN or BLOCKED, and terminal/backend tests do not prove rendered behavior.

QA PASS supplies an assessment, not newly created merge rights. A delivery workflow may perform an explicitly authorized merge/release under the selected policy, including authorization already supplied earlier; a new human prompt is not intrinsically required after every pass. Verify the exact candidate, target, required evidence and applicable permission. Current QA scope is not expanded by this proposal, and policy-based automation still requires its actual implementation and authority. A failed QA finding returns to dev and only independent retest closes it.

## Concrete success and failure scenarios

For fictional OrderDesk, development demonstrates that cancellation is allowed before dispatch and denied afterward. QA then exercises competing cancellation/dispatch requests and finds contradictory final states. The original happy-path pass remains valid evidence of that limited behavior; it does not close the race defect. Development repairs the selected issue, supplies a new candidate, and independent QA retests the defect and affected regressions.

If a required Linux run is unavailable while Windows passes, the missing platform remains unqualified. If a coverage report is incomplete, report the missing collection rather than inventing a final percentage. If a valid completed report is below its governing floor, preserve that failure and apply the selected workflow's stop policy. Another platform's result cannot substitute for it.

An edited candidate invalidates claims tied to different bytes; it does not delete their historical evidence. Missing fixture state blocks dependent execution. A user pause stops work without a completion receipt. Passing all checks still does not authorize installation, persistent startup changes, a remote source synchronization, or production deployment.

## Reusable assets and compatibility

Current [qa](../../../src/agents/skills/qa/SKILL.md) imposes at least 95% line coverage and unit-test pass rate, prohibits confirmed first-party mock decorators, and stops the whole QA run on specified integrity failures or valid subthreshold metrics. Current [dev](../../../src/agents/skills/dev/SKILL.md) derives thresholds from project inputs and continues independent authorized work. These are concrete compatibility issues for a portable policy model, not permission to weaken either current contract or silently merge their stop rules.

Skill-package validation remains distinct from product QA. The [skill validator](../../../src/agents/skills/skill-validator/SKILL.md) assesses skill behavior and evidence; its Python utilities do not perform protected acceptance. Existing QA reports, fix packets, source manifests, and retained executions remain reusable evidence subject to identity/applicability checks. No source, oracle, operational skill, or prior report is rewritten by this baseline.

## Open questions and next bounded expansion

- **DFF-08-Q1:** Which quality rules are framework invariants, project-selected policy, or current skill-specific restrictions, including mock use and metric denominators?
- **DFF-08-Q2:** Which failures stop an entire QA invocation, and which block only dependent work, for each supported mode?
- **DFF-08-Q3:** What exact dependency rules determine evidence invalidation after source, test, fixture, policy, or tool changes?
- **DFF-08-Q4:** What protected identities and predicates distinguish independent closure, delivery readiness, acceptance, and release authorization?

Next, specify one candidate-to-QA-to-repair-to-retest exchange for OrderDesk, including one stale-evidence rejection and one unavailable required platform. Resolve its policy compatibility decisions in [roadmap and decisions](roadmap-and-decisions.md) before defining machine-enforced quality transitions.
