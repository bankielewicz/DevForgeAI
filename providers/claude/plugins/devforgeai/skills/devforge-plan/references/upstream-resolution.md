# Resolving upstream sources, staleness, and evidence

Read this in Select, and any time a revision you are citing might have moved. Planning is the phase
where the project's adopted decisions stop being a conversation and start being the thing developers
build against, so a reference that resolves to the wrong bytes here becomes a wrong implementation two
skills later.

## Resolve before you partition

For each supplied input, establish four things and record them:

1. **The artifact ID and revision** you were given, or the one the existing backlog already cites.
2. **The locator** — store and path — where those exact bytes live.
3. **The digest** of the bytes at that locator, computed now.
4. **The stable section IDs** you will actually rely on: the REQ and NFR IDs from the product brief,
   the RULE, ADR, API and CAP IDs from the architecture contract, the flow or state IDs from a design
   spec, the observation and disposition from a prototype report.

Consume only what each input is for. From a product brief, the selected requirement IDs and the
delivery non-goals. From an architecture contract, the applicable rule IDs, the test policy, the source
roots and the capability requirements. From a design spec or prototype report, the relevant flows,
states, observations and hardening disposition. From an existing backlog and an accepted change
request, the dependencies, the completed work and the accepted amendment.

Reading a document is not the same as being authorised by it. A brief that says "build all of this" is
scope you were given; it is not permission to add a requirement it does not contain.

## When a cited revision no longer matches

You will meet this: the story or epic cites `ARCH-001@2`, and the file at that path now contains
revision 3. Two separate things follow, and running them together is how a plan quietly acquires a
constraint nobody adopted.

**Repairing the reference is mechanical.** If revision 2 is archived somewhere reachable, find it,
check that it hashes to the digest cited, and point the locator at the archive. That fixes a broken
path and changes nothing about what has been adopted.

**Adopting revision 3 is a decision.** It needs actual authorisation from the user that covers this
change — asked for here, or a standing instruction of theirs that has not been withdrawn and whose
scope reaches this artifact. What cannot stand in for it: finding the old bytes, the newer document's
own `accepted` status, or its `decision_ref`. That field records a decision made about that document,
not the user's adoption of it into your plan.

So when the newer revision exists and nobody authorised adopting it: name it, state its scope, mark the
prior evidence that it affects as stale, and flag exactly which stories and which acceptance criteria
would change and why. Put that in the unresolved decisions and in the handoff's continuation. Do not
relabel newer bytes as the old revision, and do not silently substitute them — the receiving skill
checks that each reference resolves to the selected revision and digest before using it, and a
substituted reference fails that check while looking like it passed.

What this rules out is the tempting version: advance the citation, rewrite the affected criteria, and
tell the user to say so if they disagree. That is adoption with an undo button, and it puts the user in
the position of having to notice and reverse a commitment they never made.

None of which makes an adopted input unusable. If the task genuinely is "bring the backlog up to
CHG-004", or the user told you to keep doing exactly that, then that is the authorisation and you do
it — recording which one you relied on, kept separate from the change request whose content you
applied. Authority and source are two different facts about the same act.

## Revising rather than regenerating

An accepted amendment revises the affected stories. It does not regenerate the backlog.

Preserve prior acceptance criteria: keep their AC IDs and their wording where the amendment does not
touch them, and record what changed where it does. Increment the story's `revision`, set `supersedes`
to the prior identity with its digest, and preserve the prior bytes at a reachable locator first.
Invalidate the downstream evidence the change actually affects — a development record, a review report
or an evaluation bound to the old story — and say which. Do not invalidate everything to be safe;
that destroys the distinction between evidence that is stale and evidence that is fine.

Stories the amendment does not touch stay exactly as they are, at the revision they already have.

## The bounded context packet

A story carries excerpts so a developer does not have to resolve six documents to start work. Excerpts
are a convenience, never an authority.

Include only what the story actually needs. Each excerpt carries its source artifact, revision, digest
and stable section ID. Never paraphrase a rule into an excerpt — a paraphrase that drifts is
indistinguishable from an invented rule to everyone downstream. Where the excerpt is too long to be
useful, cite the section and let develop and review resolve the full source, which they can do.

If you find yourself excerpting most of a document, the story's scope is probably wrong.

## Research and external evidence

Research is optional here and only for factual claims that change a decision. When you do it, record
the source URL, the retrieval date, the applicable version and the specific claim supported. That goes
in `evidence` and stays distinguishable from inference.

A newer library release is a proposal for a controlled refresh routed to the architecture owner. It is
never permission to change an approved stack, and a story that quietly assumes the newer version has
broadened the project's permissions without anyone deciding to.

Where you could not verify a claim, it stays unresolved rather than becoming confident prose in an
acceptance criterion.

## What to record

In the epic and story envelopes, and in the handoff's input rows:

- Every input's artifact ID, revision, store, path, digest and the sections actually used.
- Every reference you could not resolve, and the work it blocks.
- Every staleness finding: which revision was cited, what is there now, which stories and criteria it
  affects, and who owns the decision.
- The distinction between what was adopted, what you propose, and what the user has not answered.
