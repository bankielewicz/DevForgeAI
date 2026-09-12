# Phase 04: Authoring

**Classification:** Enforced, per the skill-authoring contract. **Applies:** whenever a candidate is created or enhanced.

## Purpose

Write the selected canonical candidate against the specification that already exists.

## Needed inputs

The working design document and specification from [phase 03](phase-03-design.md), the selected canonical target and write fence, and - for an enhancement - the frozen baseline bytes and the authorised change list.

## Substantive work

Write only the selected canonical candidate and the resources it genuinely needs.

The skill's own `SKILL.md` uses [assets/expert-skill.md](../assets/expert-skill.md): frontmatter carrying `name` and a `description` that states the user goal and the conditions that should select it, then focused instructions in the body and conditional detail in linked references. Keep the body short enough to stay useful when it is loaded on every turn; move long reference material into separate files the client loads only when it follows the link.

Content is what makes an expert worth having. Project-specific or framework-specific decision guidance, version-aware examples that match the approved dependency, the non-obvious rules a change must respect, how to handle uncertainty, and what the worker may decide versus what needs an amendment. Generic stack advice belongs to the model already. Add assets, scripts, phase files or extra references only for an actual need.

### Authoring a multi-step workflow skill

When the design gave the target a phase map, author it as an entry point plus package-local phase files:

- `SKILL.md` carries activation and scope, the authority and safety boundaries that must stay visible for the whole task, the phase map with direct package-relative links, when each phase and each conditional reference is needed, and the stopping condition.
- `phases/phase-NN-name.md` carries the detailed work, one file per phase, following [assets/phase-file.md](../assets/phase-file.md): purpose, needed inputs, substantive work, produced outputs, next-phase conditions.
- Nothing is duplicated between the entry point and a phase file. Link every phase file and every reference directly from `SKILL.md` so each is one level deep, and never instruct the reader to preload the whole package.
- Markdown phase files do not enforce progression. They describe obligations; the compiled DevForge CLI owns phase state, transitions, gates, validators, mutation permission and acceptance. Do not write phase acknowledgements, self-issued PASS labels, a copy-and-tick progress checklist or a simulated advance sequence into a skill as a substitute for a check that does not exist.

### Enhancing an existing skill

Preserve everything you were not asked to change - unrelated behaviour, resources, dependencies, identity and invocation policy. Do not reinitialise an existing skill, and reconcile against the frozen baseline before applying findings. The edited bytes are a new candidate; the former candidate and its reports stay intact and keep meaning what they meant. Applying a change means the source was edited; it does not close the finding. The evaluator has to evaluate the new bytes, and prior passing observations do not transfer to changed ones.

When the enhancement moves an inline workflow into phase files, carry out the mapping planned in design and write it down: old section to new phase file, what stayed in the entry point, and every sentence whose behaviour was omitted or changed, called out explicitly rather than left for a reader to notice. Preserve accepted decisions, stable workflow, phase, task and finding IDs, and the meaning of every reference; a link that now resolves somewhere else is a changed behaviour and gets named as one.

### Package rules that apply either way

Keep the package self-contained: package-relative links, no dependency on this framework's repository at runtime, and no developer home directory anywhere in it. Where you copy a shared template into a package, record the derivation - source path and revision, source and destination digests, the transformation and what would make it stale.

A skill grants no tool permissions and cannot redefine an external gate. A reference may explain what a gate checks; it must not restate it as something the skill enforces.

## Produced outputs

The authored or edited candidate at its canonical source, its complete file list, and - for an enhancement - the old-to-new mapping with the omitted or changed behaviour identified.

## Next phase

Continue to [phase 05, prepared transfer](phase-05-prepared-transfer.md). If a write fence, a collision or a missing authorisation stopped part of the authoring, record what landed and what did not, save that record to the assigned durable location and read it back, then continue to [phase 06](phase-06-completion-summary.md) with a partial or blocked outcome.
