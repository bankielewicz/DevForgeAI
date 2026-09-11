# Existing-skill selection

Discovery chooses reuse, enhancement, or creation. Inspect instructions and resources only; do not execute candidates or test their behavior.

## Search the relevant inventory

Start with the exposed skill catalog and a target explicitly named by the user. For framework work, search the selected provider's canonical source inventory before interpreting installed matches. Then include relevant accessible project, personal, system, and enabled-plugin locations in the target runtime.

Account for .agents/skills, configured locations, symlinked skills, and generated/exported copies. Windows and WSL may have separate inventories; resolve actual locations instead of assuming shared storage. A generated copy and its canonical source are one candidate lineage, not two independent capabilities.

Use filenames and name/description metadata to shortlist matches, then read plausible instructions and necessary resources. Include authorized repository or catalog sources supplied by the user. Do not install plugins or expand into an unbounded internet search. Record unavailable relevant locations, and ask for missing source only when it materially changes the choice.

Track actual searched paths, candidate identity/provider, source-to-installed mapping, and search limits. Use "No suitable skill found in the searched inventory" when warranted; never claim global absence.

## Compare behavior and authority

| Dimension | Compare |
|---|---|
| Purpose | Job and intended outcome |
| Activation | Requests and situations selecting the workflow |
| Scope | Included work, exclusions, and ownership |
| Inputs and outputs | Required context/access and delivered artifacts |
| Process | Essential steps, decisions, and rules |
| Runtime | Provider, tools, environment, dependencies |
| Authority | Accepted contract/specification, durable source, assignment and integration owner |

Shared names, roles, or tools do not establish duplication. Generic creator skills are relevant when the requested target is an authoring workflow; they are not duplicates of every skill they could generate.

A framework utility can be distinct from a roster skill when their outcomes, scope, or authority differ. That distinction does not authorize adding it to the accepted roster or altering sibling gates.

## Select the appropriate action

- **Reuse:** The existing skill already meets the requested need. Recommend it without unnecessary changes.
- **Enhance:** The candidate owns the same workflow and can absorb the gap without confusing scope or activation.
- **Create:** No suitable candidate was found, or a meaningfully distinct boundary warrants a new skill. Explain the distinction.
- **Resolve the target:** Several candidates fit or missing source materially affects the choice. Present the relevant differences in Q&A.

Locate the durable editable source for a generated, bundled, cached, or read-only candidate. For Codex framework work, that is the selected checkout's providers/codex/plugins/devforgeai/skills/<name> path. Installed .agents copies and plugin exports are generated artifacts.

If the durable source or assignment is unavailable, preserve an enhancement proposal and record the gap. Do not silently edit a cache, select an unrelated destination, or create a duplicate. A collision requires inspection and reconciliation, not overwrite permission. Preserve unrelated existing behavior, supporting resources, dependencies, identity, and invocation policy.

## Retain settled selection during remediation

A frozen validator handoff identifies an existing target and normally implies enhancement of that same source. Preserve the prior search/decision rather than repeating the full inventory. Refresh only the relevant comparison when findings change purpose, ownership, scope, or destination.

Compare the current source to the supplied frozen target manifest before applying changes. If it drifted, identify affected files and requirements and reconcile with current ownership/user scope. Do not apply stale findings blindly or silently overwrite concurrent edits.

A report that lacks native activation evidence does not prove duplicate selection or a source defect. Record the missing observation as an evaluation prerequisite unless other evidence supports a bounded authoring change.

## Record the decision

Include in the specification:

- Search scope, excluded/unavailable locations, and limits.
- Candidate paths, provider/source identity, overlap and gaps.
- Chosen action and rationale.
- Canonical target and generated installation/export mapping.
- For enhancements, intended changes and preserved requirements/behavior.
- Contract, ownership, or integration gaps and unresolved decisions.

Candidate inspection is not validation. Do not report testing or global uniqueness.

Compare provider explicitly. Same-named Claude and Codex packages are intentional independent implementations; neither is an accidental duplicate solely because their names or purposes match. For structural enhancements, carry the settled selection into the old-to-new obligation map in the specification.
