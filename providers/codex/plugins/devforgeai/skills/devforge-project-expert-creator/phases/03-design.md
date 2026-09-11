# Design

**Purpose:** Turn settled requirements into a detailed authoring specification.

**Inputs:** Selection decision, accepted constraints, source identities and material open questions.

**Work (Enforced):**

Read [the interview guide](../references/interview-guide.md) for material design questions; reuse settled answers.

## Populate the specification through Q&A

Use a user-selected governing template if supplied; otherwise derive the working document from [assets/skill-design-spec.md](../assets/skill-design-spec.md). Never populate the blank package template in place. Record its source identity and any transformation; a changed template does not silently change an accepted specification.

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

## Design phase files and completion

For multi-step workflow skills, use package-relative phases/ files and a concise SKILL.md phase map. Choose meaningful target phases, not this creator's five-phase count by default. A simple reference-only expert may remain inline; record that choice and its reason.

Populate section 13 of [the design template](../assets/skill-design-spec.md): phase applicability, inputs/work/outputs, start/stop and continuation conditions, classifications, actual enforcement owner and support, saved evidence and final display. Use the [phase template](../assets/phase.md) for substantial phases. Optional phases need explicit selection/skip conditions; skipping one must not bypass required work or its dependencies.

For enhancements, map every prior obligation to its new location. Separate structural moves from proposed behavior changes; preserve accepted IDs, decisions and duties. Do not treat a new file as a new requirement or reopen classifications for unchanged actions. Propose hook/gate designs only for enforced requirements, preserving existing accepted proposals and marking unavailable support honestly.

## Outputs and continuation

Save the detailed specification, proposed cases, phase map, preservation map and material open decisions. Continue to [Authoring](04-authoring.md) when the required design/classifications and write scope are settled. Missing enforcement support limits the corresponding claim, not independent authoring. An unanswered material choice blocks only the affected design.
