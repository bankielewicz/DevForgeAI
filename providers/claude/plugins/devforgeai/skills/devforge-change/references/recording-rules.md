# Recording the change-request honestly

Read this when you fill the envelope in [assets/change-request.md](../assets/change-request.md), and again before you hash anything.

The change-request is a proposal. Everything in this file exists to keep it readable as one - so that a person six weeks from now can tell what the project actually decided from what this skill suggested.

## The envelope

[assets/change-request.md](../assets/change-request.md) already carries the `devforge.artifact/v1` frontmatter. These are the fields whose meaning matters when you fill one in.

| Field | What to put in it |
| --- | --- |
| `schema_version` | `devforge.artifact/v1`, unchanged. It is the framework document schema, not the CLI's policy schema. |
| `artifact_id` | `CHG-<number>`. Allocate the next unused number in the project's change store when nothing was selected for you; where an ID was selected, that ID governs, and a conflict at that identity is a blocker to report rather than a number to substitute. |
| `artifact_type` | `change-request`, unchanged. |
| `project_id` | The consuming project, not this framework. |
| `revision` / `status` | A positive integer, and one of `draft`, `in_review`, `accepted`, `superseded`, `retired`. A change-request you just wrote is `draft`. It does not become `accepted` because the analysis is finished - `accepted` describes the user's adoption of this proposal, and you are not the user. |
| `created_at_utc` | The actual UTC time of this revision. Read the clock; do not approximate and do not carry a previous value forward. |
| `producer.skill` | `devforge-change`. |
| `producer.skill_revision` | The SHA-256 of the installed `SKILL.md` file's bytes - one file. Not a digest of the package, and not a plugin version, which can be identical across two different drafts and therefore identifies nothing. Say which one you have, in the artifact and not only in your message. Where nothing observable gives you the value, `unknown` is the honest entry; a plausible-looking digest is not. |
| `execution_ref` | The authority-selected session record and revision. `null` plus an entry in `missing_inputs` where none exists - and its absence does not establish that you own the destination. Never fabricate a session ID. |
| `upstream` | The **causal** inputs: the artifacts whose content this assessment actually rests on. Each one carries `artifact_id`, `revision`, `store`, `path`, `sha256` and the stable section IDs you actually relied on. |
| `evidence` | Locators for actual observations: the report or release note that triggered this, a command receipt an owner supplied, a retrieved page with its date. Things you looked at, as opposed to things you reasoned from. |
| `supersedes` | A prior change-request's ID, revision and digest when this one replaces it, otherwise `null`. Retain the prior bytes. |
| `decision_ref` | The user's actual adoption, or a previously delegated authority whose scope reaches this change. `null` while none exists - which is the normal state of a change-request at the moment it is written. |
| `missing_inputs` | Every required fact you could not resolve, named specifically enough to go and get. |

`upstream` and `evidence` are not interchangeable. The architecture contract whose rule is changing is upstream; the review report that noticed the conflict is evidence. Putting everything in one of them loses the distinction between what the proposal is derived from and what was observed.

Section IDs in an upstream entry must name sections that actually exist in that artifact. A stand-in word is worse than omitting the key, because it looks like a reference and resolves to nothing.

## The body

The template's own headings carry the requirements; these are the ones with a failure mode worth naming.

**Trigger and requested outcome.** `Decision state` starts at `proposed` and `Adoption or rejection reference` at `null`. Change them only when the user has actually adopted or declined this proposal, in this conversation or under a standing instruction of theirs whose scope reaches it. Enthusiasm is not adoption. A supplied document's own `accepted` status is a decision recorded in that document's process, about that document - not the user adopting this.

**Direct and transitive impact.** One row per affected item, with its current identity, the dependency path from the changed source, the expected impact, the required owner action, and the confidence or missing edge. That last column is a required field, not a garnish: an empty coverage column asserts complete coverage. [Tracing impact](impact-tracing.md) covers what belongs in the table and how to state a limit.

**Routing decision.** Name the owning skill for the first revision, and check what is actually installed before naming it. Say which work can continue under its existing valid context and which must stay stale or blocked - and say plainly that nothing in this document enforces that; it is a requirement for the owners named in it. [What the CLI can and cannot tell you](cli-boundaries.md) covers which freshness facts a command can actually report.

**Refresh and verification plan.** Every row's `State` starts at `proposed`. A row is not `done` because you described it well. Include the generated expert source, the installed copies, the affected evaluations and the downstream candidates wherever they are affected - a refresh that changed only a source `SKILL.md` is not complete.

**Completion and preservation.** Superseded artifacts get an immutable reference to bytes that are actually reachable. Declined and deferred work is retained here with its rationale, not deleted.

## Proposals and decisions

Keep them visibly distinct, at the strength each was actually given.

A proposal recorded as a decision becomes a production constraint two skills later, and by then nobody can tell where it came from. That is the specific harm this skill is most able to cause, because a change-request is read downstream as the origin of an amendment.

So: what the user said is theirs, at the scope they gave it. What you inferred is yours, labelled. What a supplied document asserts is a fact about that document. A newer library release is a proposal for a controlled refresh and never permission to replace an approved stack. Where you rely on a standing instruction rather than something said now, cite it - which record, its revision, and the scope it grants - and keep that separate from the trigger whose content you applied.

## Digests, in this order

No artifact contains its own complete-byte digest. The write order is what keeps the references true:

1. Write the change-request. Then hash it.
2. Write the handoff from [assets/handoff.md](../assets/handoff.md), putting the change-request's digest in its output row and binding the change-request in the handoff's own `upstream` - artifact ID, revision, `store: project`, its actual path, that digest, and the sections you relied on. The output row and the upstream entry are separate claims and a correct row does not supply the causal one.
3. Hash last. A digest computed before one more edit describes bytes that no longer exist, so if you touch a file again, hash it again. The handoff's own digest never goes inside the handoff, and a handoff does not list itself among its own outputs; deliver it in the terminal response or a permitted receipt instead.
4. Read every reference back after your last write. `upstream`, `supersedes`, `evidence`, output rows, impact-table identities, refresh-plan pins and invalidation conditions all have to resolve, right now, to bytes that match at that locator. The same file typically appears in several of those, and a stale copy in any one is the same defect as a wrong primary reference, just harder to notice. Check each occurrence, not only the first.

A digest is only true while the bytes behind it are reachable. If you are about to overwrite a file whose digest you cite, preserve the old bytes at a stable authorized location first and point the reference at the preserved copy. If you cannot preserve them, record that in `missing_inputs` and cite only what exists. A hash does not preserve content.

## Placeholders

A `{{placeholder}}` left in a required field means the result is a draft and cannot be presented as ready. A missing fact goes in `missing_inputs`, never into template filler, and never into a plausible-sounding invention that happens to fit the field.

This is the most common way a change-request becomes actively misleading: the shape is complete, every heading is populated, and three of the identities were never verified.

## What none of this establishes

A completed envelope proves that a document was written carefully. It is not evidence that the impact analysis is correct, that the routing is right, that any named owner has agreed, or that any check ran. Structural conformance and semantic quality are separate observations. Report only the commands you actually ran, and leave everything else at `NOT_RUN`, `COULD_NOT_RUN` with its cause, or `NOT_EVALUATED`.
