# Selection

**Purpose:** Choose the existing owner of the requested capability.

**Inputs:** Intake authority, target environment and accessible inventory; prior selection for remediation.

**Work (Enforced):**

Read [the selection guide](../references/existing-skill-selection.md) for this phase.

## Search for an existing owner of the workflow

Search before choosing creation. Use the target environment's exposed catalog and relevant accessible project, user, system, and installed-plugin locations. For framework work, include the assigned provider's canonical inventory and map installed candidates back to their source. Account for aliases and symlinks. Read names/descriptions first, then the plausible candidates; do not execute them.

Compare purpose, activation, scope, inputs, outputs, process, and runtime. Shared names, roles, or tools alone do not establish duplication. Record searched locations, candidate paths/source identities, gaps, and limits in the specification.

Choose reuse when a candidate already meets the need, enhancement when its existing workflow can absorb the change coherently, or creation when no suitable candidate was found or a distinct boundary warrants it. Resolve material ambiguity through Q&A. Never silently edit a cache or claim the search establishes global uniqueness. Inspect collisions at the selected destination before writing.

For a bounded remediation, retain the settled enhancement decision and existing candidate search. Refresh only the relevant comparison if new findings change purpose, ownership, scope, or destination.

## Outputs and continuation

Record the comparison and justified reuse/enhance/create decision, canonical destination, collisions and search limits. Compare provider explicitly alongside purpose, activation, inputs, outputs and behavior. A same-named Claude implementation is not a duplicate of a Codex target.

Continue to [Design](03-design.md) when the target decision is settled. For reuse, retain applicable existing design and record why no candidate edits are necessary; the required authoring disposition and PreparedTransfer still apply. Resolve material collisions before affected writes.
