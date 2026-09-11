# Recording rules for the architecture contract

Read this when you fill the artifact envelope, when an upstream input no longer matches the revision you referenced, when no session record exists, or when a check you wanted to run could not run.

## The artifact envelope

Framework artifacts - the architecture contract and the handoff - carry a `devforge.artifact/v1` YAML envelope. The `assets/` templates already contain it; these are the fields whose meaning matters when filling one in.

| Field | Meaning |
| --- | --- |
| `schema_version` | `devforge.artifact/v1`. A proposed schema for these documents, not the CLI's policy schema. |
| `artifact_id` / `artifact_type` / `project_id` | Stable identity (`ARCH-<number>`), the declared type `architecture-contract`, and the project whose facts the document describes. |
| `revision` / `status` | Positive integer; `draft`, `in_review`, `accepted`, `superseded` or `retired`. |
| `created_at_utc` | Actual UTC creation time for this revision. Not a date you assumed. |
| `producer` | `devforge-architect` and the exact loaded skill revision or digest. |
| `execution_ref` | The authority-selected session record and revision. Use `null` plus `missing_inputs` in pre-assignment bootstrap; its absence does not establish ownership. |
| `upstream` | Causal inputs: `artifact_id`, `revision`, `store`, `path`, `sha256`, and the stable section IDs actually relied on. |
| `evidence` | Locators for actual observations, manifest and lockfile reads, verified references and external receipts. |
| `supersedes` | Prior artifact ID, revision and digest, or `null`. Retain the prior bytes. |
| `decision_ref` | The user's actual adoption or previously delegated authority; `null` while none exists. |
| `missing_inputs` | Explicit unresolved required information. |

A template placeholder left in a required field means the result is a draft and cannot be presented as ready. A missing fact goes in `missing_inputs`, never into template filler.

## Numbering and destinations

If a destination or an artifact identity was selected for you - by the task brief, the user, or an existing project artifact map - that selection governs. Allocating the next unused `ARCH` number is what you do when nothing was selected.

**Proposed default when nothing is selected:** the project's `docs/devforge/architecture/` for the contract and `docs/devforge/handoffs/` for the handoff, matching the suggested artifact directories in the shared artifact contract. Check the project's own conventions first (`CLAUDE.md`, `AGENTS.md`, an existing `docs/devforge/` tree, or an accepted artifact map); an existing project map wins over this default.

If the selected destination is unwritable, already holds someone else's artifact, or falls outside a fence you were given, that is a condition to report - not a reason to write somewhere else. Relocating quietly leaves the path someone is actually checking empty.

## Stable IDs

| Prefix | Used for |
| --- | --- |
| `ADR-` | An architecture decision, with its requirement references, alternatives and decision state. |
| `RULE-` | An approved stack pin, a source tree or dependency boundary rule, or a verification and operations rule. |
| `API-` | A data, API or integration contract with its owner, errors, authorization and compatibility rule. |
| `CAP-` | A capability the project needs, its concrete task and the required behaviour. |

IDs are stable and never reused. A superseded decision keeps its ID and its row; the revision that replaced it references it. Preserve IDs when wording changes, so later findings, change records and downstream references stay traceable.

## Digests, and the order that keeps them true

Three rules, because this is where these documents most often go wrong.

**No artifact contains its own complete-byte digest.** Hash a file only after its bytes are final, then put that digest in the document that references it - never in the file itself. A handoff does not list itself among its own outputs, and its own digest belongs in an external receipt or the terminal response.

**A digest is only true while the bytes behind it are still reachable.** If you are about to overwrite a contract whose digest you cite, preserve the old bytes at a stable authorised location first - the project's archive convention if it has one, otherwise a sibling like `ARCH-001.r1.md` next to the contract - verify the copy's digest against what you are about to cite, and point the reference at the preserved copy. If you cannot preserve them, record that in `missing_inputs` and cite only what exists.

**Every reference must resolve after your last write.** Digests get repeated - the same file often appears in an output row, an upstream entry and an invalidation condition - and a stale copy in any one of them is the same defect as a wrong primary reference, just harder to notice. Read them all back, not only the first.

So the ordering is: write the contract, hash it, write the handoff with that digest in its output row and in its `upstream` entry, hash the handoff last and deliver that digest outside the handoff. If you touch a file again, hash it again.

`producer.skill_revision` is the SHA-256 of the installed `SKILL.md` file's bytes: one file. It is not a digest of the package and not the plugin version, which can be identical across two different drafts and therefore identifies nothing. Say which one you have, in the artifact and not only in your message to the user. Where nothing observable gives you the value, `unknown` is the honest entry; a plausible-looking digest is not.

## Resolving an upstream reference

Before you rely on an upstream input, check that the bytes at its locator still hash to the revision you are citing. If they do not, you have found staleness, and two separate things follow. Running them together is how a contract quietly gains a commitment nobody made.

- **Repairing your reference is mechanical.** If the revision you cite is archived somewhere reachable, find it, confirm it hashes to the digest you cite, and point the locator at the archive. That fixes a broken path and changes nothing about what has been adopted.
- **Adopting the newer revision is a decision,** and it needs actual authorization from the user that covers this change - asked for in this request, or a standing instruction of theirs that has not been withdrawn and whose scope reaches this change.

What cannot stand in for authorization: finding the old bytes, the newer document's own `accepted` status, or its own `decision_ref` - that field records a decision made about that document, not the user's adoption of it here. When you do act on a prior authorization, cite it as the authority (which record, its revision, the scope it grants) and keep that separate from the source whose content you applied.

When the task in front of you is not "adopt the newer revision", record the newer revision as observed context: name it, state its scope, and flag exactly which of your recorded decisions it would affect and why - in the open questions, and in the handoff continuation. The adopted decision stays standing at the strength the user gave it. Never silently relabel newer bytes as the old revision.

An accepted change-request is the ordinary route for an approved amendment. A change produces a change request, a revised contract, and an affected-consumer review; it does not overwrite prior accepted evidence.

## Decisions versus proposals

Keep them at the strength they were actually given, in the row's decision state and in `decision_ref`.

- A row is `proposed` until the user adopts it. Enthusiasm is not adoption; "yes, pin it at that version" about a specific statement is.
- A user-stated constraint is theirs even when it arrives early and informally. "It has to run on their existing SQL Server" and "I'd probably reach for Dapper, but I'm not attached" are both the user's, and they are not the same commitment. Do not widen a preference into a decision or soften a decision into a preference.
- Your own comparison of alternatives is an AI proposal. Recording it is useful; recording it as the project's decision is the failure this separation exists to prevent.
- `decision_ref` in the frontmatter stays `null` while no adoption exists. Where an adoption rests on a standing instruction rather than something said in this conversation, `decision_ref` names that record so a later reader can see the actual basis.

## When no session record exists

The absence of a session record does not establish exclusive ownership, and a worker-authored session ID is not proof of ownership. In pre-assignment bootstrap, use `execution_ref: null` with the reason in `missing_inputs`; do not fabricate a session ID or a base commit.

Before writing, inspect the destination for a collision. A collision needs inspection and reconciliation, not overwriting. If an assignment or ownership record names someone else as the writer for what you were about to write, stop the dependent writes and report it, naming the record you saw and where you read it. Do not delete, reset, revert, force or relocate.

## When a check could not run

Record the check, the outcome `COULD_NOT_RUN`, the actual cause, and the claim it blocks. A missing binary, an unavailable policy file, an unsupported adapter or an unreachable source is a cause; "no errors observed" is not a pass. Missing, stale or invalid evidence blocks the claim that depends on it - it does not block reporting, and it does not authorise weakening the requirement so the gap disappears.
