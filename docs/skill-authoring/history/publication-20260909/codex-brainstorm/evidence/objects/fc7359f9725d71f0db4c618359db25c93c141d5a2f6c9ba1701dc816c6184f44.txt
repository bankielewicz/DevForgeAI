# Interview guide

Use these prompts to fill gaps in the specification, not as a questionnaire to read verbatim. Ask one to three related questions in each round and preserve answers already given.

## Open with a concrete use case

Establish what the user wants to repeat and why the current process is insufficient. A typical request and the desired result usually provide enough context to begin searching for related skills.

Useful prompts:
- What task should this skill complete, and what would you normally provide?
- What should the finished result look like?
- Can you describe a real request it should handle?

Do not demand an example when the task is already clear. Propose one and ask about only the uncertain parts.

## Connect questions to the template

| Specification section | Information to establish | Useful follow-up |
|---|---|---|
| Identity and purpose | Task, benefit, discovery description, relevant audience | What specialized guidance would change how Codex performs this task? |
| Scope and activation | Triggering requests, boundaries, meaningful exclusions | Which nearby tasks should it leave to another workflow? |
| Inputs and results | Necessary inputs, missing-input handling, deliverable, format, completion criteria | If this input is missing, can the skill proceed, or must it ask? |
| Workflow | Meaningful workflow/phase/task IDs, actions, decisions, dependencies | What happens next, and what changes the path? |
| Task-specific rules | Actual requirements versus preferences, conventions, authorization boundaries | Which choices are fixed, and which may Codex make? |
| Tools and resources | Actual runtime, integrations, references, templates, supporting scripts, fallback | Which resources are available where the skill will run? |
| Validation examples | Representative requests and expected behavior for future use only | What result would communicate the intended behavior? |
| Placement and maintenance | Existing source or new destination, project/personal/plugin scope | Where should this skill be available? |

Generate routine details such as a proposed name and concise discovery description from the answers. Mark assumptions clearly. Do not ask the user to supply credentials or secret values.

## Ask about optional versus enforced items

Decompose only meaningful stages; do not turn every internal model action into a separate task. Give each item a stable ID and, when relevant, a parent ID.

For each item lacking an explicit answer, ask whether it is Optional or Enforced. Explain the consequence in terms of the action that would have to wait. Ask when a conditional item applies and when it may be skipped.

An answer that a phase is enforced does not classify every child. Offer named groups when the user can make one clear decision for several items. Do not assume a default for an unanswered classification.

For an enforced item, ask about the protected action and observable completion evidence before choosing a hook event. Use the hook-proposal fields in the specification to develop the design. Where a requirement is subjective, explain what a concrete evidence or human-decision condition would establish and what it would leave unproven.

## Keep the working document useful

Update the specification after each material round, using the user's language where it conveys a requirement precisely. Record the current draft status, settled choices, proposed defaults, and questions still open. Preserve the selected existing-skill candidate and comparison rationale.

When resuming, read the working specification and current request rather than starting the interview again. Revisit settled answers only when new information conflicts with them or the user changes scope.

If a question is unanswered, keep the affected decision open. Continue independent drafting or discovery while awaiting an answer. If the remaining gap blocks authoring, save the draft and ask the focused question; do not label it complete.

Do not require a separate approval ceremony when the user already authorized building and the relevant decisions are settled.

## Stop collecting when the design is sufficient

The essential information is a defined task and activation boundary; needed inputs; expected output; core process and important branches; real constraints and dependencies; a reuse/enhancement/creation decision; a resolved destination; and an explicit classification for every proposed workflow item.

Optional references, ownership details, or additional examples need not block an otherwise sufficient design. Clearly label unresolved runtime support in hook proposals. Capturing examples and completion criteria does not authorize executing them.
