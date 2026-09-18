---
name: prd-create
description: Create a product or feature requirements document (PRD) from a selected discovery brief or equivalent requirements; complete a partial PRD, revise an identified PRD against authorized changes or review findings, or resume that authoring work. Use for PRD authoring, not pure idea exploration, independent PRD review, epic/story creation, sprint planning, implementation, product QA or project activation.
---

# PRD Create

Turn selected requirements into one reviewable product/feature PRD with inline
provenance, acceptance and a manual handoff to **prd-review**. Preserve the
selected outcome; referencing a broad source does not select all its work.

This is a portable standalone responsibility. Use the selected project's actual
language, domain, architecture, document conventions and quality policy. Require
no Git repository, worktree, daemon, index, framework identity, project binding,
constitution pack or prior brainstorm run. Do not create setup prerequisites.

## Resolve the selected work

Read [intake and evidence](references/intake-and-evidence.md) when consuming a
brief, requirements, existing PRD or conversation decisions. Resolve the project,
outcome, scope, sources, existing artifact, destination and permitted effects
before dependent reads/writes. Reuse supplied answers and the active root.

Before deriving claims, acquire each selected local source's interpreted content
and raw-byte digest from the same captured bytes, following the intake reference.
An exploratory text read followed by hashing the live path is not a bound source
version. Before persistence and at final readback, use the artifact reference's
drift reconciliation: changed bytes require inspecting and reconciling affected
claims, acceptance and provenance, not merely refreshing the source hash.

A create/save request permits ordinary PRD documentation delivery within its
selected scope. Interview-only work creates no files. With no selected root,
continue useful clarification and identify the missing destination before saving.
Ask only material unanswered questions, normally one to three together, using
the available user-input interface or ordinary terminal conversation. Continue
independent drafting while dependent decisions remain pending; silence is not
consent.

For a near miss, name its appropriate responsibility and return the bounded
handoff: brainstorm for unresolved idea exploration, independent PRD review for
review-only work, the relevant planning/story owner for decomposition, dev for
implementation, QA for product assessment, or setup for project activation. Do
not invoke these workflows from this skill.

## Author the requirements

Use [requirements and acceptance](references/requirements-and-acceptance.md)
while drafting or changing substantive content. Capture outcomes, selected scope,
functional and applicable quality obligations, interactions, data/interfaces,
architecture decisions and independently challengeable acceptance. Material
choices need actual sources or decision authority. Identify missing business
rules and thresholds; do not invent them to complete the document.

Use [artifact and revision](references/artifact-and-revision.md) for selecting
the format/destination, saving, revising, resuming and reporting delivery. Use the
[PRD template](assets/prd-template.md) only for a new document without a governing
compatible convention. The artifact guidance owns required content and metadata;
the template is a writing aid. Preserve valid existing formats and IDs.

## Deliver and transfer review

Complete selected documentation delivery and full readback before claiming a
saved candidate. Report source action `CREATED`, `REVISED` or `UNCHANGED`
separately from disposition and actual delivery state. When an existing PRD
already satisfies the requested authoring scope, reference its exact path/digest
and current limitations without producing a duplicate revision.

`READY_FOR_REVIEW` means authoring inputs and selected product semantics are
sufficient for independent review. `NEEDS_INPUT` names unresolved authoring
blockers and preserves useful content. Both may be delivered and inspected;
neither means reviewed, approved, implementation-ready or accepted. Explicit
architecture questions assigned to review/design may remain open; an undefined
product rule cannot be hidden that way.

Return a concrete manual request for prd-review naming the PRD identity, exact
candidate digest, selected scope, governing sources, design references and open
questions. If that workflow is unavailable, describe the independent review
responsibility without inventing an installed command. Review owns findings and
closure; an authorized author correction returns for independent retest.

Stop after this responsibility's outputs. Do not run a prototype, product tests,
another workflow or a validator; create stories, worktrees or sprint assignments;
install components; alter configuration, bindings, canonical policy or separate
architecture documents; merge or deploy. Broader existing authorization belongs
to its owning later workflow. Documentation and filesystem observations cannot
grant protected framework acceptance.
