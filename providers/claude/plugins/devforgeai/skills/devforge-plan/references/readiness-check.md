# Checking readiness, and what no tool checks for you

Read this in Check readiness, and whenever a story looks blocked, a destination looks contested, or a
check you wanted to run will not run.

## What this check actually is

Every finding below is your own reading of documents you just wrote. That is worth doing — the errors
it catches are real and expensive — but be exact about what it is. No DevForge command inspects an
epic, a story, a requirement graph or a `devforge.artifact/v1` envelope at this revision.

The observed command surface is `delivery`, `expert`, `check`, `init`, `red`, `green`, `accept`,
`verify`, `status` and `isolate`. `devforge check` checks a project candidate's approved dependencies,
layout, tooling pins and expert provenance against an external policy JSON, and its own help says it
"does not certify semantic behavior". It is not a planning check and it takes no planning artifact.
The specification assigns deterministic graph and provenance checks to DevForge; that capability is a
**missing integration**, not something to narrate as if it ran.

So record what you checked as a reading, and record its limits. Do not write a command sequence into a
plan that only pretends to gate something, do not issue yourself a PASS, and do not treat the absence
of an error as one. If a requirement genuinely needs to block a dependent action, record it as a
requirement — the action, the evidence to be checked, and the intended allow or refuse behaviour — and
route it to the integration owner, who owns the actual check and its wiring.

## The five readings

**Coverage.** Walk the selected requirement IDs from the product brief. Each one is either covered by
at least one named story, or recorded in the epic's coverage table as an explicit deferral with its
reason and decision reference. A requirement that is neither is the finding. Coverage is about the
selected scope, not about every requirement in the brief: the delivery non-goals are exclusions, and
recording one as a gap is noise.

**Cycles.** Follow each story's `Prerequisite stories` edges. A cycle means at least one of those
dependencies is not real, or the partition put one behavioural change across two stories. Report the
cycle members and the edge you think is wrong. Do not break a cycle by deleting an edge that is
genuinely there — that produces a backlog that looks ready and deadlocks in execution.

**Unresolved decisions.** For each acceptance criterion, ask what a developer would have to invent to
implement it. An undefined authorization behaviour, an unspecified error path, a missing limit, an
unnamed actor: each is an open decision. Mark the dependent criterion unresolved in the story, route
the clarification to the owner who can answer, and leave the story blocked if the decision is
consequential. A consequential open decision is one where two reasonable implementations would both
satisfy the wording and produce different products.

**Source freshness.** Every upstream reference resolves to the revision and digest cited. See
`upstream-resolution.md` for what to do when one has moved. An unresolvable reference is not a small
formatting problem; it means nobody can check what the story was derived from.

**Capability gaps.** Each story's required-expertise table names capability IDs. For each, either an
existing expert package covers it, or it is an open gap. Name the gap as a gap. Do not name an expert
package that does not exist, do not describe a package as installed or evaluated when you have not
observed that, and do not manufacture a capability row to fill an org chart. Routing a real gap to
`devforge-project-expert-creator` is a useful result; a plausible skill name is not.

## Separating ready from blocked

A story is **ready** when its upstream references resolve, its acceptance criteria are observable and
have no unresolved consequential decision, its write scope and test policy are declared, its
prerequisite stories are themselves ready or accepted, and its required capabilities exist or are
explicitly not required before implementation.

A story is **blocked** when any of those fails. Say which one, in the story and in the handoff. "Nearly
ready" is not a state; it is a blocked story with an optimistic label.

Execution readiness is computed from current inputs, dependencies, assignment and expertise at the time
someone runs the story. It is not a status field you edit into the story later — recording it in the
story would make the story stale every time the world changed around it.

## Placeholders

Scan every required field of every document you are about to deliver for a surviving `{{...}}`. One
placeholder in a required field means the result is a draft. Say so; do not present it as ready and do
not fill it with something plausible. A fact you do not have goes in `missing_inputs`.

## When another writer owns the destination

If a session record, an ownership note or the filesystem shows that the epic or story destination
belongs to another writer, or that another session holds the worktree or branch you were assigned:

Stop the dependent writes. Report the collision, naming the record you saw and where you read it. Do
not delete, reset, revert, stash, rebase or force anything, and do not quietly write somewhere else —
relocating leaves the path someone is actually watching empty, and produces an artifact nobody
selected at a path nobody is checking.

A collision is a condition to report, not permission to overwrite and not permission to relocate. Say
what you found, where, and what you would need to proceed. Historical authorship does not establish a
current exclusive writer either: compare actual active assignment evidence before treating an old
producer as a collision.

## Resuming after an interruption

An interrupted session is not a fresh one, and it is not a continuation either until you have checked
which of the two it is.

Preserve first. The phase you had reached, the input identities you had frozen in Select, and any epic
or story bytes already written are the record that makes resuming possible. Do not delete a partial
output because it looks unfinished; a partial story with its provenance intact is worth more than a
clean start that has lost which revision it was derived from.

Then, before writing anything further, run this sequence:

1. **Re-read the session assignment.** Ownership can have changed while you were away. The worktree,
   branch or destination you held may now belong to someone else, in which case the collision rule above
   applies and the dependent writes stop.
2. **Re-check every recorded digest** against the bytes at the locator you recorded. An input that still
   hashes the same is still the thing you partitioned against.
3. **Re-check the base commit or run identity** if one was recorded for this work.

What each outcome means:

| Observation | What follows |
| --- | --- |
| Assignment unchanged, every digest matches | Continue the phase you were in. The preserved evidence carries forward. |
| A cited input's digest has moved | This is a new iteration, not a continuation. The staleness rule in `upstream-resolution.md` governs, evidence gathered before the change does not transfer to the changed bytes, and adopting the newer revision is still a decision that needs authorisation. |
| The assignment, worktree or base has changed | Re-establish the baseline before resuming, and record which prior evidence the change invalidated. |
| Another writer now holds the destination | Stop the dependent writes and report, as above. |
| You cannot recover what phase you were in | Say so. Re-deriving from the preserved inputs is honest; asserting a phase you cannot evidence is not. |

Record the resume itself: what was preserved, what was re-checked, what had moved. A reader who cannot
see that the re-check happened has no way to tell a resumed session from one that quietly carried stale
evidence across the gap.

## When a check cannot run

Record `COULD_NOT_RUN` with the actual cause, and block only the claim that depends on it. Continue the
work that does not. A blocked freshness check does not stop you from partitioning the scope; it stops
you from claiming the partition is traceable.

Use the words precisely. `NOT_RUN` is planned and unattempted. `COULD_NOT_RUN` is blocked, with the
cause. `NOT_APPLICABLE` is a stated scope exclusion. `NOT_EVALUATED` is behaviour nobody evaluated.
Blending them into one summary hides exactly the gaps this vocabulary exists to keep visible.

## Stop and hand back when

- A story cannot be made implementation-ready because a consequential acceptance behaviour is
  undefined and nobody has answered.
- A governing input is stale and adopting the newer revision is a decision nobody has authorised.
- The dependency graph has a cycle you cannot resolve without changing scope.
- A required capability is missing and the story cannot proceed without it.
- A product or architecture contradiction has surfaced — that routes through `devforge-change` to the
  owning skill, and is not yours to resolve by editing the governing source.
- Another writer owns the destination.

In each case say what is blocked, what would unblock it, and who owns that. Then stop. A partial
backlog with an honest account of what is blocked is a finished result of this skill; a complete-looking
backlog that hides an unresolved decision is not.
