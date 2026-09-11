# Phase 02: Selection

**Classification:** Enforced, per the skill-authoring contract. **Applies:** always; a repair refreshes only the comparison its findings actually affect.

## Purpose

Decide between reuse, enhancement and creation against what already exists, so the result is not a second skill competing with a first.

## Needed inputs

The intake record from [phase 01](phase-01-intake.md), the existing expertise map or skill inventory, and the write fence and destination rows named in `SKILL.md`.

## Substantive work

Search before you create. Another skill that already owns this workflow is the cheapest correct answer, and a duplicate is worse than nothing because two skills now compete for the same requests and drift apart.

[Existing-skill selection](../references/existing-skill-selection.md) covers where to look in a Claude environment, how to map an installed copy back to its durable source, and how to compare purpose, activation, provider, scope, inputs, outputs, behaviour and authority rather than matching on names. Read names and descriptions first, then the plausible candidates. Do not run them.

Two comparisons that are routinely got wrong:

- **Within one provider**, a skill that already owns this workflow is a reuse or enhancement candidate even when the requested name differs. Overlapping subject matter is not enough on its own, and neither is a matching name.
- **Across providers**, the Claude and Codex implementations of the same framework skill are intentional provider implementations, not duplicates. Do not propose deleting, merging or re-pointing one because the other exists, and do not edit a provider you were not assigned.

Come out of this with one of: **reuse** (something already meets the need - recommend it and stop), **enhance** (a candidate owns this workflow and can absorb the gap without blurring its activation), or **create** (nothing suitable was found, or a genuinely distinct boundary warrants a new skill). Record the locations you actually searched, the locations you could not reach, the candidates and their source identities, and the limit of the comparison. "No suitable skill found in the searched inventory" is an honest result. "No such skill exists" is a claim you cannot support.

Inspect the destination for a collision before writing to it. A collision needs reconciliation, not overwriting.

## Produced outputs

The selection decision with its rationale, the searched and unreachable locations, the candidate identities and the chosen canonical target, plus its generated installation or export mapping - the durable source and the project-local copy or plugin export generated from it, as the recorded-outputs list in the reference sets out. These go into the working design document in the next phase.

For a reuse result there is no next phase, and this record is the deliverable: save it to the assigned durable artifact location and read it back, so the summary links a path that resolves.

## Next phase

- **Reuse:** skip authoring entirely and go to [phase 06, completion summary](phase-06-completion-summary.md). A recorded reuse recommendation is a complete result.
- **Enhance or create:** continue to [phase 03, design](phase-03-design.md).
- **Unresolved:** put the relevant differences in front of the user as one focused question, then continue to [phase 03, design](phase-03-design.md) with the part of the design that depends on the answer left open.
