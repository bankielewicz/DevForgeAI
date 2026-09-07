---
name: skill-builder
description: "Design, create, or enhance Codex skills through user Q&A, existing-skill discovery, and a DevForgeAI specification; remediate a frozen validator handoff by editing the selected canonical source. Includes optional/enforced workflow choices and hook proposals. Does not test or validate skills."
---

# Skill Builder

Turn a user's workflow idea or a validator's findings into a populated specification and a new skill or focused enhancement. Reuse an existing skill when it meets the need. This is a DevForgeAI authoring utility; its availability does not add a runtime skill to the accepted 12-skill roster.

## Authoring boundary

Author instructions and supporting resources only. Do not run target skills, helper scripts, tests, validators, linters, compilation, or evaluations, directly or through another agent. Collect expected behavior for a separate validator. Reading source material and recording file identities or successful writes are authoring operations, not validation evidence. A target skill may itself perform validation when that is its requested purpose.

Hook work ends at a design proposal. Do not create executable hook handlers, install or activate hooks, edit active hook configuration, or claim enforcement is operating. Keep illustrative configuration in the specification.

## Managed operation

When runtime context identifies a managed builder assignment, use [the managed authoring reference](references/managed-authoring.md). Do the substantive work for the supplied phase and save evidence in the runtime-provided shape and destination. The runtime owns admission, transitions, waiting, bounded corrections and final receipt publication. Do not call advance/resume/complete/check/verify or a receipt helper as a fallback. Without an admitted builder adapter, useful authoring remains possible, but its handoff is prepared only.

## Recover framework authority and the target

Read [framework context](references/framework-context.md) and the selected [skill-authoring contract](references/contracts/skill-authoring-contract.md). Resolve all package links from the loaded SKILL.md directory, independently of the shell working directory. Resolve the consuming project and its artifact destinations separately; do not require the framework checkout at runtime.

Recover the current request, assignment scope, provider, accepted specification and source revisions, and applicable project instructions. Record actual source paths and revision or preserved-byte identities, contract/template SHA-256 values, and any missing inputs. A missing value remains unknown with a reason; do not fabricate a revision, hash, owner, or approval. Preserve the selected prior inputs when newer conflicting sources appear. Reconcile only the affected authoring before proceeding.

For a framework skill, the canonical Codex source is `providers/codex/plugins/devforgeai/skills/<name>` in the selected framework checkout. `.agents/skills/<name>` and exported plugin packages are generated runtime copies, not alternative authoring sources. Work only in the assigned provider and skill. Project-specific skills need an explicit source-to-installation mapping; do not assume a personal or installed path is canonical.

Do not modify sibling DevForge gates, shared contracts, installer policy, the accepted roster, or another skill to make this candidate pass. Report a contract or integration gap to its owner. Authoring completion is not framework adoption, release, native activation, or behavioral certification.

## Choose the entry path

Use the conversation and supplied materials before asking questions. Establish the workflow, typical request, result, and target environment. Distinguish design-only work from authorization to create or enhance files. Once the necessary decisions and authoring scope are settled, proceed without adding a blanket approval checkpoint.

- For a new idea or ordinary enhancement, use [the interview guide](references/interview-guide.md) and [the selection guide](references/existing-skill-selection.md).
- For findings from `skill-validator` or another supplied validation report, read [the validator handoff guide](references/validator-handoff.md). Preserve its frozen target/specification, finding IDs, expected behavior, evidence, and prior results. The validator evaluates; this builder owns edits. Do not restart settled Q&A or execute the validator.

## Search for an existing owner of the workflow

Search before choosing creation. Use the target environment's exposed catalog and relevant accessible project, user, system, and installed-plugin locations. For framework work, include the assigned provider's canonical inventory and map installed candidates back to their source. Account for aliases and symlinks. Read names/descriptions first, then the plausible candidates; do not execute them.

Compare purpose, activation, scope, inputs, outputs, process, and runtime. Shared names, roles, or tools alone do not establish duplication. Record searched locations, candidate paths/source identities, gaps, and limits in the specification.

Choose reuse when a candidate already meets the need, enhancement when its existing workflow can absorb the change coherently, or creation when no suitable candidate was found or a distinct boundary warrants it. Resolve material ambiguity through Q&A. Never silently edit a cache or claim the search establishes global uniqueness. Inspect collisions at the selected destination before writing.

For a bounded remediation, retain the settled enhancement decision and existing candidate search. Refresh only the relevant comparison if new findings change purpose, ownership, scope, or destination.

## Populate the specification through Q&A

Use a user-selected governing template if supplied; otherwise derive the working document from [assets/skill-design-spec.md](assets/skill-design-spec.md). Never populate the blank package template in place. Record its source identity and any transformation; a changed template does not silently change an accepted specification.

Save the working specification in the chosen project artifact/document location, outside installed skill instructions unless it is a needed runtime resource. Resume that same document across turns. Preserve all applicable original design sections, framework authority/source mapping, and authoring records.

Ask one to three focused related questions per round, concentrating on unknowns that change the design. Capture supplied requirements, proposed defaults, and unresolved choices distinctly. Do not turn silence into approval. Collect completion criteria and representative cases for later evaluation without executing them. Optional detail need not delay authoring.

## Classify workflows, phases, and tasks

Give meaningful workflow items stable IDs and parent relationships. For each genuinely new, unclassified item, ask:

"Should [item] be optional, or should its completion be enforced before [dependent action]?"

Record Optional or Enforced, applicability, dependent action, and permitted skip conditions. Preserve previous explicit answers and named group decisions across revisions and remediation. A parent classification does not automatically classify children; an explicit group answer covers its named items unless the user changes it. Ask only about additions or a material conflict.

Treat the classification as a requirement, not an assertion of runtime support. Continue independent work while an answer is pending, but do not invent the classification or finalize the affected dependent design.

## Propose hooks for enforced items

Map every enforced item to a hook proposal; one proposal may cover distinct traceable items. Capture protected action, runtime/version, event/matcher, observable evidence, state ownership and freshness, allow/block rule, errors, recovery, permitted exceptions, configuration needs, and uncovered paths.

Use current official Codex hook documentation for the selected runtime, recording the source/version/date supporting the proposal. If relevant capability cannot be established, mark it Unknown rather than inventing an event. A self-reported marker does not prove substantive completion.

Record feasibility as Supported, Partial, Unsupported, or Unknown, separately from the requirement. Always record proposal status as "Design only; not installed, activated, executed, or validated." Retain unmet enforcement requirements and discuss feasible alternatives; do not silently downgrade them to advisory text.

## Author or enhance canonical files

Proceed when the boundary, required inputs, output, essential process, material constraints, source destination, selection decision, and item classifications are settled. Document unresolved runtime support as a gap, never as delivered enforcement.

Use available skill-creator authoring guidance with the settled specification and this authoring-only boundary. Do not invoke its helpers, validators, forward tests, or evaluation delegates. Author directly when it is unavailable.

Write SKILL.md with YAML name/description and focused instructions. Use a concise lowercase hyphenated name, precise discovery triggers, essential instructions in the body, and linked references for conditional detail. Add assets, scripts, or metadata only for an actual need. Authored scripts remain unexecuted. Preserve normal automatic selection unless the user requests explicit-only invocation.

Enhance the selected durable source; preserve unrelated behavior, resources, dependencies, identity, and invocation policy. Do not reinitialize an existing skill, overwrite concurrent work, or replace another author's changes. Reconcile a changed target against the frozen baseline before applying findings. Preserve the former candidate and reports; the edited bytes are a new candidate.

Keep package resources self-contained and record derivations from selected shared contracts/templates. Leave installation/export generation and shared integration changes to the assigned integration owner. An installed copy's presence cannot substitute for provenance or behavioral evidence.

## Deliver useful authoring content

At actual authoring completion, transfer or a recovery checkpoint, populate [assets/handoff.md](assets/handoff.md). Do not create a new handoff for ordinary read-only discussion. Include the exact skill/specification references, decisions versus proposals, remaining issues, carried authority, next owner and copyable continuation task. Use [the managed authoring reference](references/managed-authoring.md) for creation-time observations and receipt boundaries.

Record creation/enhancement/reuse rationale and search limits, canonical-to-installed mapping, before/after candidate references and per-F-###/CHG-### applied, deferred or declined dispositions. Preserve requirement IDs and former bytes. Partially authored work remains deferred with its missing scope. Source changes do not resolve old evaluation results.

The builder change record is substantive authoring evidence, not an authoritative runtime receipt. In managed operation the runtime computes final identities, preserves inspected bytes and publishes/readbacks its receipt. A containing document never includes its own complete-byte digest. Runtime observations absent at creation remain explicit; do not rewrite the handoff to claim later completion.

Return the new candidate and prepared handoff to the allocated next owner. Shared adapter gaps go to integration before any dependent runtime claim; separate validation is not launched automatically. Report "Validation status: Not performed." and "Hook status: Design only." Authoring is not adoption, native activation, enforced transition or receiving-skill invocation.
