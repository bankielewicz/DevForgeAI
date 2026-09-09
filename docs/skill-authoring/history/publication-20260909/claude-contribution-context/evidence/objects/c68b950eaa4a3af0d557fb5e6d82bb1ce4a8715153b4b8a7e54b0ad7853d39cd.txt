# Standardized output templates

These templates define artifacts produced by the proposed MVP skills. They are not installed skills or completed project records. Copy them into a skill's package-local assets during authoring, then resolve all required placeholders when producing a real artifact.

Use the [artifact contract](../artifact-contract.md) for the common envelope, causal upstream references, and decision/evidence rules. Use the [execution contract](../execution-contract.md) for worktree ownership and external report storage.

| Producing skill | Template | Output |
| --- | --- | --- |
| devforge-brainstorm | [idea-ledger.md](devforge-brainstorm/idea-ledger.md) | idea-ledger |
| devforge-define-product | [product-brief.md](devforge-define-product/product-brief.md) | product-brief |
| devforge-design | [design-spec.md](devforge-design/design-spec.md) | design-spec |
| devforge-prototype | [experiment-plan.md](devforge-prototype/experiment-plan.md) | experiment-plan |
| devforge-prototype | [prototype-report.md](devforge-prototype/prototype-report.md) | prototype-report |
| devforge-architect | [architecture-contract.md](devforge-architect/architecture-contract.md) | architecture-contract |
| devforge-plan | [epic.md](devforge-plan/epic.md) | epic |
| devforge-plan | [story.md](devforge-plan/story.md) | story |
| devforge-project-expert-creator | [expert-spec.md](devforge-project-expert-creator/expert-spec.md) | expert-spec |
| devforge-project-expert-creator | [expert-package.md](devforge-project-expert-creator/expert-package.md) | expert-package |
| devforge-project-expert-creator | [expert-skill.md](devforge-project-expert-creator/expert-skill.md) | native skill instructions |
| devforge-evaluate-expert | [expert-evaluation-plan.md](devforge-evaluate-expert/expert-evaluation-plan.md) | expert-evaluation-plan |
| devforge-evaluate-expert | [expert-evaluation-report.md](devforge-evaluate-expert/expert-evaluation-report.md) | expert-evaluation-report |
| devforge-develop | [development-record.md](devforge-develop/development-record.md) | development-record |
| devforge-review | [review-report.md](devforge-review/review-report.md) | review-report |
| devforge-release | [release-record.md](devforge-release/release-record.md) | release-record |
| devforge-change | [change-request.md](devforge-change/change-request.md) | change-request |

Shared templates:
- [Session and worktree assignment](shared/session-record.md): maintained by the external operator before dependent writes.
- [Handoff](shared/handoff.md): current phase, exact inputs/outputs, observed checks, and one immediate next task.

The first idea ledger can have no upstream artifact because the user's statement is its origin. Other outputs populate upstream according to their skill specification. Empty upstream arrays are not a universal exemption.

Native expert instructions use name/description frontmatter; their provenance lives in XPKG. Results, runtime bindings, and later evaluation reports do not mutate frozen source specifications merely to update readiness.

For post-GREEN reports, use the permitted report path from the session record; adding a report to a frozen production candidate changes that candidate.

## Shared skill authoring templates

[Eval cases](skill-authoring/evals.json), [trigger queries](skill-authoring/trigger-queries.json), [run manifest](skill-authoring/run-manifest.json), and [evaluation report](skill-authoring/evaluation-report.md) implement the [authoring contract](../skill-authoring-contract.md). They are four additional authoring templates, separate from the 17 skill-output and 2 shared workflow templates. Fill observed facts only; null/unavailable is not a passing result. Case files paths resolve relative to the containing evals directory.
