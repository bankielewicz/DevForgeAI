# Selecting and interpreting the records

Read this at step 2 of the workflow, while you are resolving context. It covers the
interpretation rules that decide whether a recovered fact can be trusted. Nothing here depends
on a particular repository checkout: resolve every path from the assignment you were given.

## Contents

- [Where each fact lives](#where-each-fact-lives)
- [Authority, and what does not grant it](#authority-and-what-does-not-grant-it)
- [Selected revisions versus newer bytes](#selected-revisions-versus-newer-bytes)
- [Evidence, claims, and acceptance](#evidence-claims-and-acceptance)
- [When a record will not resolve](#when-a-record-will-not-resolve)
- [Boundaries: peers, companions, and private state](#boundaries-peers-companions-and-private-state)
- [Bounding what you read](#bounding-what-you-read)

## Where each fact lives

DevForgeAI keeps stable procedure in skills and mutable operational state in records. That split
is what makes recovery possible, and it tells you where to look.

| Question | Record type that answers it |
| --- | --- |
| What may I change, and where? | The session/assignment record: owner, provider, worktree, branch, base, write fence, protected paths, permitted delivery path, integration owner. |
| What rules govern this work? | The contracts and specifications the assignment selects, at the revisions it selects. |
| Why does this task exist? | The story, goal, change request, or finding report, with its source evidence. |
| What expertise is needed and available? | The capability declaration, the expert package record, and any evaluation record. |
| What did a session actually observe? | Run manifests, outputs, evaluation or review reports, and external receipts. |
| Where does work resume? | The most recent handoff plus the selected execution record. |

If your assignment supplies a context packet or manifest listing these, use it as the index and
resolve the underlying records from it. Acknowledging a packet is evidence that you selected it,
not evidence that the facts inside are correct - check the ones your continuation depends on.

## Authority, and what does not grant it

Authority comes from an actual adopted decision or a valid prior delegation, recorded outside
your writable area, with a scope. Carry both the decision and its scope; a delegation that
covers reversible authoring does not cover publishing, and one that covers reporting does not
cover target writes.

A still-applicable delegation stays in force even when the current request does not repeat it.
Demanding that the user re-authorize work they already authorized is a real failure, not
caution. The opposite failure is worse: treating any of the following as authority.

- A status field that says `accepted`, or a document titled as though it were adopted.
- Producer metadata naming a skill or session - possibly stale, possibly never the current owner.
- A previous handoff's "next task" suggestion. It is a proposal to its reader, not a grant.
- The newest timestamp, the most confident wording, or a particular runtime provider.
- A session ID that a worker wrote for itself.
- The absence of any assignment record. Absence is not exclusive ownership; it is an unknown.

When ownership is missing or two active claims conflict with no supersession resolving them,
record the exact condition, stop the dependent target work, and preserve everything else. Do not
pick an unassigned path to write to instead. Separately: if you hold independently valid
authority for a report outbox, that authority survives the inner task's ownership problem - a
blocked contribution does not remove your permission to report on it. And an observably
authorized bootstrap is not a failure merely because no session record exists yet; say what
authorizes it and what remains unknown.

## Selected revisions versus newer bytes

An assignment pins revisions and digests so that work stays reproducible while the main line
moves. Resolve the bytes it pinned.

When the working copy now differs from the pinned digest, you have made an observation, not
found a replacement:

1. Keep using the preserved selected bytes for this task.
2. Report the newer version as a distinct observation, with both identities.
3. Name the continuation the difference affects.
4. Leave the refresh decision to the record's owner.

A newer document is a proposal. It becomes governing when its owner selects it - not when you
notice it, and not because it is more recent or better written. Relabelling newer bytes as the
selected revision, or editing the assignment to match what you found, destroys the reproducible
basis of every result already recorded against that selection.

Abbreviated digests are for reading, never for verification. Compare complete 64-character
values, and only against bytes you actually read.

## Evidence, claims, and acceptance

Four things are routinely confused. Keep them apart in everything you produce.

| Thing | What it establishes |
| --- | --- |
| A digest match | Byte identity. Nothing about accuracy, authorization, or quality. |
| A structural check | The declared syntax or shape. Not semantic conformance. |
| A recorded outcome (PASS/FAIL/...) | What some author observed, in some scope. Attribute it to them. |
| Acceptance | A human or authorized owner's decision, recorded as such. |

So: a package can be structurally current and behaviorally unevaluated; a report can say PASS
while the finding it cites records a required failure; and an author's own grades support scoped
review without being independent acceptance.

When records conflict, the recovery result keeps both, names each source, preserves candidate
and run identities exactly as recorded, and routes the unresolved question to its owner.
Erasing a finding, silently changing its state, or repeating the more convenient summary as your
own conclusion are all worse than reporting the conflict.

Distinguish the state of your recovery task from the state of the contribution you are
describing. "I have recovered the context, and the contribution is blocked on X" is a complete,
successful result.

## When a record will not resolve

You know its expected identity but cannot read it inside your permitted boundary. Record:

- the expected locator and digest, exactly as the assignment gave them;
- that resolution failed, and how it failed;
- which facts therefore remain unverified;
- the specific conclusion that is blocked.

Then continue with everything that does not depend on it. Three things to refuse: substituting a
similarly named file found elsewhere, claiming verification of a digest you did not compute from
bytes you read, and widening your search outside the selected authority roots to find something
that will answer the question. The last one is the most tempting and the most damaging - it
produces a confident answer sourced from a record nobody selected.

## Boundaries: peers, companions, and private state

- **Peer contributors.** Two situations, and collapsing them causes an error in one direction or
  the other. An *unassigned* peer source tree stays protected: not yours to load, edit or propose
  changes to. But a peer candidate or evidence input that *your own assignment explicitly
  selects*, with its locator and digest, is a required input - resolve it. An architect asked to
  verify a worker's package cannot verify it by declining to read it, and "the peer is protected"
  is not a reason to report a fact as unavailable when your assignment handed you its identity.
  Read authority follows the assignment, not the provider or the directory owner.
  Reading stays reading. Neither role may edit a peer source, and resolving a peer record is
  never authority to perform the integration or repair that the recovered context describes -
  that work has its own owner and its own assignment. Take only what the task needs for
  dependencies and collision detection; a replacement architect inherits the records, not
  everyone's reasoning, and another contributor's private deliberation is not yours to relay.
- **The companion repository.** DevForgeAI's companion owns the CLI, policy, tests and
  workflows. Report a defect to its owner. Changing a gate, a validator, or policy so that a
  candidate passes is out of bounds regardless of how well justified it looks from inside the
  task.
- **Private client state.** Credentials, provider history and another session's memory store
  never enter a recovered view or a handoff.
- **Held-out material.** If your context contains expected answers or an author's preferred
  solution for work being evaluated, it does not belong in output that reaches an evaluated
  worker.

## Bounding what you read

Include the rules and references this task needs, follow the dependencies those genuinely
require, and stop. Unrelated project history, the full text of every contract, and another
author's workspace all cost context without improving the continuation.

A short, correct result that points at pinned identities is better than an exhaustive dump. The
test is whether the reader can take the next action and verify it - not how much you quoted.
