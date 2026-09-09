# MVP use-case inventory

Status: proposed support decisions, 2026-09-04. This inventory is a test plan for the requested MVP, not a claim that the plugin already supports every row.

Following the [OpenAI use-case guide](https://developers.openai.com/plugins/plan/use-case), each skill specification records the user goal, direct and indirect requests, expected result, required context, capability choice, action boundary, and support decision.

| User expectation | Skill / full use case | MVP boundary |
| --- | --- | --- |
| I have three ideas and cannot decide what problem is worth solving. | [devforge-brainstorm](specifications/skill-001-devforge-brainstorm.md) | Required for an undeveloped idea; reuse an existing ledger for later discussion. |
| What is the smallest version worth shipping, and how would we know it helped? | [devforge-define-product](specifications/skill-002-devforge-define-product.md) | Required when defining or changing a release scope; includes proportionate discovery and feasibility research. |
| Show how a customer would complete signup, including errors and empty states. | [devforge-design](specifications/skill-003-devforge-design.md) | Conditional for UI or interaction changes. Pure backend stories can record why design is not applicable. |
| Can this approach support the interaction or performance we need? | [devforge-prototype](specifications/skill-004-devforge-prototype.md) | Conditional when an experiment could change a decision. Skip when the uncertainty can be resolved reliably by inspection or existing evidence. |
| How should we structure this SaaS so later sessions do not introduce incompatible libraries? | [devforge-architect](specifications/skill-005-devforge-architect.md) | Required before governed production development; existing projects begin with an evidence-backed inventory rather than a replacement architecture. |
| What should we implement first, and what does done mean for each change? | [devforge-plan](specifications/skill-006-devforge-plan.md) | Required for a delivery slice; revises affected stories without regenerating an entire backlog. |
| Our next story needs someone who knows this codebase's data access rules and pinned APIs. | [devforge-project-expert-creator](specifications/skill-007-devforge-project-expert-creator.md) | Required when a real capability gap exists; reuse suitable current expertise and refresh only when changes or observed failures justify it. |
| Does this expert actually help, or does its SKILL.md just look convincing? | [devforge-evaluate-expert](specifications/skill-008-devforge-evaluate-expert.md) | Required before a generated expert is treated as evaluated; record results separately for Codex and Claude when claiming support for both. |
| Build this approved behavior and show the failing test before the implementation passes. | [devforge-develop](specifications/skill-009-devforge-develop.md) | Required for production changes. Non-code work follows the applicable accepted verification policy rather than inventing a failing test. |
| Is this change ready, and what evidence supports that conclusion? | [devforge-review](specifications/skill-010-devforge-review.md) | Required for delivery readiness; expert behavioral evaluation moves to evaluate-expert, while review may inspect that report as evidence. |
| Package this accepted change for delivery, including recovery and verification. | [devforge-release](specifications/skill-011-devforge-release.md) | MVP guarantees preparation and local verification when its inputs are available. Authorized PR creation is conditional on existing Git tooling/authentication; automatic production deployment is deferred. |
| A new library version or customer request changes our assumptions; what does that invalidate? | [devforge-change](specifications/skill-012-devforge-change.md) | Required for changes affecting adopted intent or governing context; small implementation fixes inside unchanged criteria return directly to develop. |

## Intentional exclusions and supporting tooling

| Expectation | Decision | Reason and useful next step |
| --- | --- | --- |
| Install, inspect, and safely refresh the framework | Required tool path, not another core skill | Use native packaging and the accepted installer; inspect actual installed versions and collision handling. |
| Multiple AI writers in one repository | Required worktree contract | Separate assignments and bases; serialize shared Git operations/integration; see execution contract. |
| Automatically create every organizational role | Excluded | Create expertise only for an observed task need. |
| Automatically enforce any language/package manager | Deferred until adapters are implemented and tested | Start with a named supported stack; unsupported checks stay visible. |
| Automatically run model reviews in GitHub Actions under a terminal subscription | Deferred | The linked Codex Action documents API-key prerequisites; use local model sessions and deterministic CI. |
| Automatic production deployment and incident remediation | Deferred | Prepare concrete release/recovery artifacts; execute only existing authorized operations. |
| Sprints as a mandatory prerequisite | Optional | Dependency-ordered stories suffice for MVP. |
| Scheduled rewriting of project experts | Deferred | Refresh on relevant accepted changes or observed failures; preserve evaluation history. |
| A custom visual application for framework operation | Deferred | Markdown, Mermaid, local mockups, and native terminals are sufficient for the first workflows. |

## Common end-to-end acceptance

A supported request must yield a useful artifact, an honest outcome when information/tools are missing, and a next step the user can actually invoke. Each specification includes direct, indirect, edge, and out-of-scope cases; the handoff points to real available capabilities or to their authoring task.

The package must separately prove discovery and behavior in each supported terminal. A native manifest, a placeholder template, a successful scripted fixture, or a hook configuration is insufficient evidence by itself.
