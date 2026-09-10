# Recording rules for a release record

Read this when you write either artifact's frontmatter, when a reference will not resolve, or when one of these comes up: no session record exists (the usual case), an assignment record names someone else as the writer, an upstream input no longer matches the revision you cited, or a check you wanted to run could not run.

This is a narrowed restatement of the framework's shared artifact contract, selected for the situations this skill actually meets. It restates; it does not extend or waive it. Where the two differ, the contract governs. `derivation.json` records what this was distilled from.

## The envelope

Both outputs carry a `devforge.artifact/v1` YAML envelope. The `assets/` templates already contain it; these are the fields whose meaning matters when you fill one in.

| Field | Meaning for a release record |
| --- | --- |
| `schema_version` | `devforge.artifact/v1`. A proposed schema for these documents, not the CLI's policy schema. |
| `artifact_id` | `REL-<number>` for the release record, `HANDOFF-<identity>` for the handoff. Allocate the next unused number only when no identity was selected for you. |
| `artifact_type` | `release-record` or `handoff`. |
| `project_id` | The project whose delivery this describes. |
| `revision` / `status` | Positive integer; `draft`, `in_review`, `accepted`, `superseded` or `retired`. A record describing a draft nobody published is still `draft`. |
| `created_at_utc` | The actual UTC time this revision was created. Not a rounded guess and not the time you started. |
| `producer` | `devforge-release` plus the exact loaded skill revision or digest. |
| `execution_ref` | The authority-selected session record and revision. Use `null` plus an entry in `missing_inputs` when none was supplied; its absence does not establish ownership, and a session ID you invent is not one. |
| `upstream` | Causal inputs: the QA review-report, and the development-record, story, epic and architecture-contract you actually relied on. Each carries `artifact_id`, `revision`, `store`, `path`, `sha256` and the stable section IDs used. |
| `evidence` | Locators for actual observations: verification receipts, CI result locators, PR and merge references, deployment records. |
| `supersedes` | The prior release record's ID, revision and digest when this revises one; otherwise `null`. Retain the prior bytes. |
| `decision_ref` | The user's actual adoption or a previously delegated authority. `null` while none exists. A readiness recommendation is not one. |
| `missing_inputs` | Explicit unresolved required information. A missing fact goes here, never into template filler. |

## Digests, and the order of the writes

Three rules, because this is where these documents most often go wrong.

**No artifact contains its own complete-byte digest.** Hash a file only after its bytes are final, then put that digest in the document that references it. The handoff carries the release record's digest; the handoff's own digest belongs in an external receipt or in what you say to the user, never inside itself. A handoff does not list itself among its own outputs.

**A digest is only true while the bytes behind it are reachable.** If you are about to overwrite a release record whose digest you cite, preserve the old bytes at a stable authorized location first - the project's archive convention if it has one, otherwise a sibling such as `REL-007.r1.md` - verify the copy hashes to what you are citing, and point the reference at the copy. If you cannot preserve them, record that in `missing_inputs` and cite only what exists. A digest with no reachable bytes behind it is a claim the next reader cannot check.

**Every reference must resolve after your last write.** So the ordering is: write the release record, hash it, write the handoff with that digest in its output row and in its `upstream` entry, hash the handoff last. If you touch a file again afterwards, hash it again - a digest computed before one more edit describes bytes that no longer exist.

Then read them all back. Digests get repeated: the same file typically appears in an output row, an upstream entry and an invalidation condition, and a stale copy in any one of them is the same defect as a wrong primary reference, just harder to notice. Check each occurrence, not only the first.

`producer.skill_revision` is the SHA-256 of the installed `SKILL.md` file's bytes - one file. It is not a digest of the package and not the plugin version, which can be identical across two different drafts and therefore identifies nothing. Say which one you have, in the artifact and not only in your message: a bare 64-character string tells a later reader nothing about what was hashed. Where nothing observable gives you the value, `unknown` is the honest entry; a plausible-looking digest is not.

## Resolving an upstream reference

The receiving skill checks that each reference resolves to the selected revision and digest before using it. That is you, for the QA report and everything behind it.

Resolve each one before you rely on it. If the current worktree bytes differ from the digest the reference names, either use the preserved referenced version - where it was archived and still hashes correctly - or report the staleness. Never relabel newer bytes as the old revision. A task excerpt keeps its source section IDs and digest.

Record the stable section IDs you actually relied on, not the whole document. "QA-014 revision 2, sections `Readiness recommendation` and `Findings and ownership`" tells a reader what your record is standing on. A bare artifact ID does not.

The causal graph is acyclic across immutable revisions. Handoff backlinks, epic membership and next-step links are relationships, not causal upstream dependencies - do not add them to `upstream` to make the record look better connected.

## Placeholders and missing facts

Templates deliberately contain placeholders and start as drafts. No completed result may retain a placeholder in a required field.

If `{{observed targets}}` is still sitting in the record when you finish, the result is a draft and cannot be presented as ready. That is not a formatting nit: a placeholder reads as content to a person scanning the document, and it will be quoted back at you as though you had written something there.

The fix is one of two things, never a third. Fill it with an observed fact, or record the fact as missing - in `missing_inputs`, with what it blocks. Do not fill it with a plausible value, an inferred value, or `TBD`.

## Where the artifacts go

If a destination was selected for you - by the task, by the user, or by the project's accepted artifact map - that is the destination. The default applies only when nothing was selected: `docs/devforge/releases/` for the release record and `docs/devforge/handoffs/` for the handoff, from the artifact contract's suggested directories. A project's own accepted map outranks that default.

Where the identities were selected too, those govern the envelope exactly as a selected path governs where you write. Allocating the next unused number is what you do when nothing was selected.

If the selected destination is unwritable, already holds someone else's artifact, or falls outside a fence you were given, that is a condition to report, not a reason to write somewhere else. A collision does not transfer the path to you. Relocating quietly is the worse failure: the session then has an artifact nobody selected, at a path nobody is checking, while the path that is being checked stays empty.

## Bootstrap, and what it does not license

Most sessions have no session record. That is ordinary, and it does not stop you working. It also does not establish that you are the single writer for anything.

So: `execution_ref: null`, the reason in `missing_inputs`, the task authorization you actually hold recorded in the record, and a collision check before dependent writes. Do not fabricate a session ID, a Git base or an owner. `null` with a stated reason is the correct entry for a fact that genuinely does not exist.

## Vocabulary

Fixed, and never blended into a single score, percentage or status word.

| Term | Means |
| --- | --- |
| `NOT_RUN` | Planned, unattempted. |
| `COULD_NOT_RUN` | A required observation was blocked; the actual cause is recorded. |
| `NOT_APPLICABLE` | Excluded from the stated scope, with the reason. |
| `NOT_EVALUATED` | Behaviour nobody has evaluated. |

The absence of an error is not a pass. A hash binding or a structural check proves which inputs were referenced, never that the result is correct. Preserve earlier records' original labels; explaining a later reclassification is fine, rewriting their history is not.
