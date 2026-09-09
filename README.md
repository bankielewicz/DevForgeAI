# DevForgeAI Adaptive Spec-Driven Framework

DevForgeAI is an adaptive, spec-driven software engineering framework in development. Its design combines reusable, project-agnostic workflows, project-specific AI expertise, traceable specifications, and independent checks to guide software delivery under human authority.

Current status: local proof of concept. The [adaptive design](docs/mvp/roster.md#adaptive-design) describes how workflow selection, expertise, and affected context and evidence respond to project needs. The complete adaptive lifecycle remains roadmap scope.

Intended repository: https://github.com/bankielewicz/DevForgeAI

This directory is a new local POC, not a clone or an overwrite of the existing remote repository. The companion [DevForge](../DevForge/README.md) directory owns the Rust CLI, policy, fixed runner, installation tooling, and GitHub workflows.

## Development language

[The development language policy](docs/development-language-policy.md) requires compiled Rust in the DevForge CLI for framework phases, gates, validators, mutation brokers and acceptance decisions. The skill-evaluation Python JSONL runner and deterministic graders are mandatory build artifacts that produce raw outputs and metrics; Rust validates the evidence and owns acceptance. Other framework implementation must use Rust. Existing Python framework logic and example applications are legacy/noncompliant and require migration to Rust. The policy preserves current evidence and does not claim completed migration or automatic enforcement.

## Start here

The following commands run unchanged existing POC tools, which remains allowed within the assigned scope during migration. Their use does not authorize new Python framework logic or shell implementation. From the sibling DevForge directory:

```bash
cargo build --locked
python3 scripts/verify_poc.py --framework ../DevForgeAI
python3 scripts/demo.py --framework ../DevForgeAI --prepare-only
```

The report prints the exact prepared project, external policy, and state paths. Continue using the [terminal runbook](../DevForge/docs/POC.md). The subscribed terminal does the AI work; the CLI makes no model calls.

## Included capabilities

| Skill | Purpose |
| --- | --- |
| `devforge-brainstorm` | Explore ideas and preserve proposals, assumptions, evidence, and decisions. |
| `devforge-project-expert-creator` | Discover, specify, author and refresh grounded expertise; prepare a user-mediated evaluation handoff. |
| `devforge-develop` | Follow a bounded story through external RED/GREEN checks. |
| `devforge-evaluate-expert` | Independently evaluate exact framework/project experts; return evidence and bounded repair guidance. |
| `devforge-review` | Review meaning and evidence without confusing structural checks with acceptance. |

Provider packages live separately in `providers/claude/plugins/devforgeai` and `providers/codex/plugins/devforgeai`. Claude agents travel with its plugin; Codex subagent definitions remain under `providers/codex/agents`. Native plugin manifests exist for both providers. The installer can instead place project-local copies in each provider's discovery directories, without changing global configuration.

The SQLite and JSON-file examples have different project expert skills, architecture choices, references, and implementations. Their tiny applications demonstrate a persistence round trip, not a production SaaS application. Their declarations are synthetic fixture decisions, not approved choices for your future application.

## Expertise lifecycle

Project goals and decisions -> expertise gap -> expert specification -> AI-authored skill -> structural provenance -> independent behavioral evaluation -> use -> targeted refresh.

Skills and agent roles do not confer authority to change the external gate. A hash binding proves which inputs a skill refers to; it does not prove that the instructions are correct or useful. The POC reports model behavior as NOT_EVALUATED until actual terminal evaluations are recorded.

See [POC scope](docs/POC.md) and the companion [contract/runbook](../DevForge/docs/POC.md).

The proposed [MVP authoring package](docs/mvp/README.md) contains the 12-skill roster, Mermaid provenance and worktree flows, one specification per skill, standardized output templates, and source notes. These are draft design artifacts; they do not install or certify the proposed skills.


The [authoring contract](docs/mvp/skill-authoring-contract.md) defines source ownership and A/B/C evaluation. Runtime installation/export excludes authored eval cases and fixtures. The Claude brainstorm candidate was preserved during migration and requires alignment with the refreshed contract; the Codex brainstorm draft retains the original POC baseline. Neither is behaviorally accepted. The immediate milestone is brainstorm in both terminals, then a product brief consuming its ledger.

For practical guidance on scope expansion, repeated approval/review cycles and recovering a clear delivery path, see [Learned behavior: keeping delivery bounded](docs/learned-behaviors/bounded-delivery.md).

Codex expert foundation: the promoted creator and evaluator replace the obsolete skill-builder/skill-validator packages. They are promotion candidates pending required verification and operational adoption. Claude packages and managed v1 workflow IDs remain unchanged. Manual invocation and handoffs are supported by the authored flow; automatic orchestration remains deferred. See the [creator](providers/codex/plugins/devforgeai/skills/devforge-project-expert-creator/references/manual-operation.md) and [evaluator](providers/codex/plugins/devforgeai/skills/devforge-evaluate-expert/references/manual-operation.md) command/handoff references for actual predicates and limitations.
