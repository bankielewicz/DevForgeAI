# Existing-skill selection

Discovery determines whether to reuse, enhance, or create. It is not validation: inspect instructions and resources only; do not execute candidates or test their behavior.

## Search the relevant inventory

Start with the skill catalog exposed by the current environment and any skill explicitly named by the user. Search relevant accessible project, personal, system, and enabled-plugin skill locations for the target runtime. Use filenames and name/description metadata to shortlist candidates, then read plausible matches.

For project scope, include applicable .agents/skills directories and any explicitly configured locations. Account for symlinked skills. Personal and plugin paths vary by runtime; resolve them from the actual environment instead of assuming that Windows and WSL share a home directory.

Use authorized repository or catalog sources the user supplies when relevant. Do not install plugins, scan unrelated directories or other people's files, or expand into an unbounded internet search. If an important location is unavailable, record it and ask for the source only when that limitation changes the decision.

Track locations actually searched, relevant candidates and their paths, and limitations. Say "No suitable skill found in the searched inventory" when that is the evidence.

## Compare behavior, not names

| Dimension | Compare |
|---|---|
| Purpose | The job and desired outcome |
| Activation | Requests and situations that should select the skill |
| Scope | Included work and exclusions |
| Inputs | Required data, files, context, and access |
| Outputs | Deliverables and their format |
| Process | Essential steps, decisions, and domain rules |
| Runtime | Relevant tools, environment, and dependencies |

Generic authoring skills are candidates when the requested target is an authoring workflow. They are not duplicates of every domain skill simply because they can create it.

## Select an approach

- Reuse: An existing skill already meets the need. Recommend it and avoid unnecessary edits or another skill.
- Enhance: A candidate owns the same workflow and can absorb a specific gap without confusing its triggers or scope.
- Create: No suitable candidate exists, or the requested workflow has a meaningfully distinct boundary. Explain that distinction when related skills exist.
- Resolve the target: Several candidates fit, or an inaccessible source materially affects the choice. Present the relevant differences during Q&A.

If a candidate is bundled, generated, read-only, or installed in a cache, locate its durable editable source. Do not silently alter cached or system files. If no editable source is available, preserve an enhancement proposal and explain the limitation; ask about an explicitly scoped alternative rather than silently creating a duplicate.

Preserve unrelated behavior during enhancement. A name collision at the chosen destination is a reason to inspect and resolve the target, not permission to overwrite it. Refresh only the relevant search if the workflow changes during the interview.

## Record the decision in the specification

Use the authoring record in the bundled template. Include:
- The search scope and inaccessible or excluded locations.
- Candidate paths, overlap, and gaps.
- The selected action and its rationale.
- The durable enhancement source or new destination.
- For enhancements, intended changes and existing behavior to preserve.
- Open questions and proposed defaults that affect the decision.

Do not claim candidates were tested or that the inventory is globally exhaustive.
