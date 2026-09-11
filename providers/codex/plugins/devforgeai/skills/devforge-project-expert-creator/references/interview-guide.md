# Interview guide

Use these prompts to fill material gaps, not as a questionnaire to read verbatim. Ask one to three related questions per round. Preserve accepted requirements, Optional/Enforced answers, and named group decisions.

## Recover existing decisions first

Read the current request, accepted working specification, source/assignment identity, and any remediation handoff. Record the governing framework/provider/contract and the canonical-to-installed mapping using [framework context](framework-context.md). Do not ask users to reconstruct facts already available in the selected sources.

When resuming, continue the same specification. Revisit a settled answer only when the user changes it or identified evidence materially conflicts with it. Record the affected requirement IDs and reason. A newer checkout or template alone does not authorize replacing accepted inputs.

For validator remediation, use [validator-handoff.md](validator-handoff.md). Ask about an unapproved proposal or a new scope decision, not whether to repeat an already authorized repair. A missing native observation needs an evaluation prerequisite, not an invented source defect.

## Begin with a concrete use case

Establish the task to repeat and the desired result. A typical request and output are usually enough to begin related-skill discovery.

Useful prompts:
- What task should this skill complete, and what would you normally provide?
- What should the finished result look like?
- Which current behavior needs to change?

Do not demand another example when the task is already clear. Propose a concrete interpretation and ask about only the uncertain parts.

## Connect questions to the specification

| Section | Information to establish | Useful follow-up |
|---|---|---|
| Identity and purpose | Task, benefit, discovery description, relevant audience | What specialized guidance changes how Codex performs this task? |
| Scope and activation | Activating requests, boundaries, nearby exclusions | Which related work belongs to another workflow? |
| Inputs and results | Required inputs, missing-input behavior, deliverable, format, completion criteria | Can it proceed when this input is missing? |
| Workflow | Stable workflow/phase/task IDs, decisions, dependencies | What changes the path or must wait? |
| Task-specific rules | Requirements versus preferences, actual authorization boundaries | Which decisions are fixed and which may Codex make? |
| Tools and resources | Actual runtime/version, available integrations, resources and fallback | Which resources are available in the consuming project? |
| Validation examples | Representative cases and expected behavior, capture only | Which observable result expresses the requirement? |
| Placement and maintenance | Provider, canonical source, runtime destinations, owner | Who owns the durable source and installation mapping? |
| Authoring decision | Search scope, candidates, gaps, create/enhance/reuse rationale | Does an existing workflow own this change? |
| Framework authority | Selected contracts/specification bytes, assignment, source identities and gaps | Which conflicting source, if any, needs an owner decision? |
| Remediation and receipt | Frozen inputs, F/CHG IDs, permitted changes, retained requirements | Is this a required repair, authorized enhancement, proposal, or investigation? |

Derive routine details such as a proposed skill name and discovery description. Distinguish proposed defaults from user requirements. Never request credential or secret values.

## Ask Optional or Enforced only where unresolved

Decompose meaningful workflows, phases, and tasks; do not enumerate every internal model action. Give items stable IDs and parents.

For a genuinely new unclassified item, ask whether it is Optional or Enforced and identify the dependent action. Capture applicability and any allowed skip. Explain that this selects a requirement; it does not establish that runtime enforcement is possible or active.

An enforced parent does not classify all children. A user's explicit choice for a named group does classify its named members. Retain that decision across later rounds and remediation unless changed. Do not reopen an entire interview because a validator identified a narrow defect.

For enforced items, establish observable evidence and state freshness before selecting a hook event. For a subjective requirement, distinguish a concrete evidence or human-decision condition from proof of the entire task's quality. Keep hook proposals design-only.

## Keep the working document useful

After each material round, save accepted requirements, source references, proposals, unresolved questions, and the selection rationale. Preserve stable IDs when wording changes so validator findings and builder receipts remain traceable.

Keep an unanswered decision open. Continue independent discovery or draft work while waiting. When the gap blocks a particular change, save its status and ask the focused question; do not mark that part complete.

A build/enhancement authorization plus settled relevant decisions is enough to proceed. Do not add an approval ceremony or demand irrelevant optional metadata.

## Stop interviewing when authoring is possible

The necessary information is the task/activation boundary, inputs, output, core process and branches, material constraints, existing-skill decision, canonical destination/assignment, and classifications of all proposed workflow items.

Document unavailable contract/source information and enforcement limitations truthfully. Optional references, maintenance details, or additional examples need not block an otherwise sufficient design. Capturing evaluation prerequisites or examples does not authorize running them.

## Phased workflow design

Use section 13 of [the design template](../assets/skill-design-spec.md) for multi-step workflows and structural enhancements. Capture phase paths, applicability, start/stop conditions, actual enforcement owner, saved evidence and final display. Map old obligations to new locations separately from proposed behavior changes. Framework work needs its workflow/contracts, not unrelated application architecture. Reference-only experts need no artificial phases. Preserve settled classifications when moving instructions.
