# Spec-driven engineering framework (Grok design pack)

This directory is a **design visualization** of the DevForgeAI Adaptive Spec-Driven Engineering Framework for product development. It is not a runtime specification, installer, or acceptance record.

Start with [spec-driven-engineering-framework.md](spec-driven-engineering-framework.md). That document holds the mermaid diagrams: an overview, then one expansion per lifecycle step with skill/command, templates, and upstream/downstream handoffs.

| Path | Role |
| --- | --- |
| [spec-driven-engineering-framework.md](spec-driven-engineering-framework.md) | Design, mermaid diagrams, handoff catalog |
| [templates/](templates/) | Fillable document contracts for each workflow that authors an artifact |
| [../specs/framework/index.md](../specs/framework/index.md) | Authoritative planning baseline (DFF-00 through DFF-12) |

## How to read the diagrams

1. The **overview** is not a waterfall. Work may enter at discovery, architecture, a selected story, a defect, or a resume checkpoint.
2. Each **step expansion** is a flowchart: upstream artifacts → command/skill → template → produced document → downstream consumer. Dotted arrows are return paths (gaps, findings, spec-change requests).
3. A **template** is the document contract for that producer. Filling a template is not implementation, QA, or release authorization.
4. Skills marked **current** exist under `src/agents/skills/`. Skills marked **planned core** are lifecycle responsibilities in the framework baseline that are not yet authored as portable Codex packages.

## Template index

| Workflow | Template | Downstream consumer |
| --- | --- | --- |
| Adapt / propose | [adaptation-proposal.md](templates/adaptation-proposal.md) | Human selection, then `skill-builder` author_set |
| Discover | [business-analysis.md](templates/business-analysis.md) | Requirements, architecture |
| Research (supporting) | [research-finding.md](templates/research-finding.md) | Discovery, architecture, stories |
| Specify requirements | [product-requirements.md](templates/product-requirements.md) | Architecture, work planning |
| Architect | [system-architecture.md](templates/system-architecture.md), [project-policy.md](templates/project-policy.md) | Work planning, development, QA |
| Plan work | [work-set.md](templates/work-set.md), [story.md](templates/story.md) | Development, QA |
| Implement | [development-context.md](templates/development-context.md), [development-slice-plan.md](templates/development-slice-plan.md), [development-traceability.md](templates/development-traceability.md), [development-delivery.md](templates/development-delivery.md) | Independent QA |
| Assess | [qa-test-plan.md](templates/qa-test-plan.md), [qa-report.md](templates/qa-report.md), [qa-fix.md](templates/qa-fix.md) | Development (repair) or delivery review |
| Deliver | [release-record.md](templates/release-record.md) | Feedback, operations |
| Follow-up | [feedback.md](templates/feedback.md), [rca.md](templates/rca.md) | Discovery, stories, policy realignment |
| Continuity (all stages) | [checkpoint.md](templates/checkpoint.md) | Resume of the selected workflow |

Operational skill templates remain the source of truth for those packages when they exist (`dev`, `qa`, `story-create`). The files here are the framework-level contracts the diagrams bind to.

## Status

Planning design pack. Current product-development skills: `story-create`, `dev`, `qa`. Current framework-authoring skills: `skill-builder`, `skill-validator`. Protected acceptance remains a compiled-Rust boundary and is not established by these diagrams or filled templates.
