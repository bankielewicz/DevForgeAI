# Document templates

Fillable contracts for each workflow that authors a document in the [spec-driven engineering design](../spec-driven-engineering-framework.md). Every template has the same envelope: producer, consumer, failure behavior, non-claims, upstream locators, and a manual downstream handoff.

These are framework-level contracts. Where a current skill already ships an operational template, that package file remains the authoring source of truth; the file here is the handoff shape the diagrams bind to.

| # | Template | Producer | Primary consumer |
| --- | --- | --- | --- |
| 0 | [adaptation-proposal.md](adaptation-proposal.md) | `skill-builder` propose | human → author_set |
| 1 | [business-analysis.md](business-analysis.md) | planned `discover` | `specify` |
| 1b | [research-finding.md](research-finding.md) | planned `research` | discover / specify / architect |
| 2 | [product-requirements.md](product-requirements.md) | planned `specify` | `architect`, work planning, QA oracle |
| 3 | [system-architecture.md](system-architecture.md) | planned `architect` | work planning, `dev`, `qa` |
| 3b | [project-policy.md](project-policy.md) | architect + user selection | every product skill |
| 4 | [work-set.md](work-set.md) | plan work | `story-create`, human selection |
| 4b | [story.md](story.md) | `story-create` | `dev`, `qa` |
| 5 | [development-context.md](development-context.md) | `dev` | slices / resume |
| 5b | [development-slice-plan.md](development-slice-plan.md) | `dev` | TDD cycle |
| 5c | [development-traceability.md](development-traceability.md) | `dev` | delivery, QA inventory |
| 5d | [development-delivery.md](development-delivery.md) | `dev` | `qa` |
| 6 | [qa-test-plan.md](qa-test-plan.md) | `qa` | same-run execution |
| 6b | [qa-report.md](qa-report.md) | `qa` | `dev` / delivery review |
| 6c | [qa-fix.md](qa-fix.md) | `qa` on FAIL | `dev`, then `qa` retest |
| 7 | [release-record.md](release-record.md) | planned `release` | operations, feedback |
| 8 | [feedback.md](feedback.md) | planned `feedback` | discover / story-create |
| 8b | [rca.md](rca.md) | planned `rca` | story-create / policy |
| * | [checkpoint.md](checkpoint.md) | any stopping workflow | same workflow on resume |

Filling a template is not implementation, independent QA, framework acceptance, or release authorization.
