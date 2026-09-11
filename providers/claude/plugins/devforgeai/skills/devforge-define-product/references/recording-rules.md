# Recording rules

Read this when you write the brief's frontmatter, when an upstream reference has to be resolved, or when one of these comes up: no session record exists (the usual case), an ownership record names someone else as the writer, an upstream input no longer matches the revision you referenced, or a check you wanted to run could not run.

Everything below is a narrowed restatement of the framework's shared artifact and execution contracts, selected for the situations this skill actually meets. It restates; it does not extend or waive them. Where the two differ, the contracts govern. `derivation.json` records the exact sources this was distilled from.

## The artifact envelope

`assets/product-brief.md` and `assets/handoff.md` already carry the `devforge.artifact/v1` envelope. These are the fields whose meaning decides whether the document is honest.

| Field | What it must hold |
| --- | --- |
| `schema_version` | `devforge.artifact/v1`. A proposed schema for these documents, not the CLI's policy schema. |
| `artifact_id` / `artifact_type` / `project_id` | `PROD-<number>` and `product-brief` for the brief; the project whose facts it describes. A selected identity governs; allocate the next unused number only when nothing was selected. |
| `revision` / `status` | Positive integer. `draft`, `in_review`, `accepted`, `superseded` or `retired`. A revision of the same logical brief keeps its `artifact_id`. |
| `created_at_utc` | The actual UTC time this revision was written. |
| `producer` | `devforge-define-product` and the exact loaded skill revision - see the digest scope note below. |
| `execution_ref` | The authority-selected session record and revision. Use `null` plus an entry in `missing_inputs` in pre-assignment bootstrap; its absence does not establish ownership, and a worker-authored session ID is not proof of one. |
| `upstream` | The causal inputs: `artifact_id`, `revision`, `store`, `path`, `sha256` and the stable section IDs you actually relied on. |
| `evidence` | Locators for actual observations, source checks and external receipts. |
| `supersedes` | The prior artifact ID, revision and digest, or `null`. The prior bytes stay reachable. |
| `decision_ref` | The user's actual adoption, or a standing instruction of theirs whose scope covers this change. `null` while none exists. |
| `missing_inputs` | Unresolved required information, stated explicitly. Never replaced by template filler. |

A template placeholder left in a required field means the result is a draft and cannot be presented as ready.

`producer.skill_revision` is the SHA-256 of the installed `SKILL.md` file's bytes - one file. It is not a digest of the package and not the plugin version, which can be identical across two different drafts and therefore identifies nothing. Say which one you have; a bare 64-character string tells a later reader nothing. Where nothing observable gives you the value, `unknown` is the honest entry, and a plausible-looking digest is not.

## Upstream entries for a brief

A brief usually cites an idea ledger, sometimes a prior brief, sometimes a change request. Each entry names the artifact's own ID and revision, not a filename standing in for one:

```yaml
upstream:
  - artifact_id: IDEAS-001
    revision: 2
    store: project
    path: docs/devforge/ideas/IDEAS-001.md
    sha256: "<sha256 of the exact referenced bytes>"
    sections:
      - IDEA-003
      - DEC-001
```

`sections` names the stable IDs you actually relied on - the selected idea rows, the adoption record, the requirement IDs of a superseded brief. If you cannot name real sections, omit the key and say so; a stand-in word is worse than an absence.

A file with no envelope of its own - a pasted export, a supplied spreadsheet, a retrieved page - is not an artifact reference. It belongs in `evidence` with its native locator, its retrieval date and the claim it supports.

## Resolving a reference before you use it

1. Read the bytes at the recorded path and hash them.
2. Compare against the digest and revision the reference records.
3. If they match, the reference is resolvable; say that you checked it, not merely that it exists.
4. If they do not match, you have found a staleness condition, not a value to update.

Nothing in the DevForge CLI performs this resolution for you. Its current command surface (`delivery`, `expert`, `check`, `init`, `red`, `green`, `accept`, `verify`, `status`, `isolate`) has no artifact-reference or brief-structure check; `devforge check` inspects a project candidate's dependencies, layout, tooling pins and expert provenance, which is a different question. Resolution here is reading and reporting, and the missing integration - deterministic upstream-reference resolution and product-brief structural admission, compiled into the CLI and wired by the integration owner - is a gap to name rather than a check to imply. Confirm any command against its own `--help` before naming it.

## When a session is interrupted, and how it resumes

An interruption is not a failure and not a finish. What it costs you is the assurance that the bytes you read at the start of the phase are still the bytes on disk.

**On interruption, preserve.** Keep the phase you had reached, the brief as far as it exists, the evidence rows already recorded, and each decision state at the strength it actually had. Do not round a half-gathered phase up to a finished one, and do not discard an unfinished brief because it is unfinished - a draft with `missing_inputs` populated is a usable resumption point and a deleted one is not.

**On resuming, re-establish before continuing.** In this order, before any further requirement is written:

1. Re-read every upstream reference the brief records and re-hash the bytes at each recorded path, exactly as the four steps above describe. A digest that no longer matches is the staleness condition, handled below.
2. Re-check the session assignment: the record, the owner it names, the fence, and whether it is still active. An assignment that has changed hands while you were away is an ownership collision, handled under *Ownership and concurrent writers*, not a formality.
3. Re-check the selected destination and artifact identity. Something else may hold that path now.

A changed upstream identity, a changed assignment or a changed destination starts a new iteration: re-establish the baseline and the evidence for the affected part rather than continuing as though the pause had not happened. Only the affected part - a superseded ledger revision behind one requirement does not invalidate the evidence rows or the requirements that do not rest on it.

Two things this is not. It is not a licence to redo settled work: a decision the user made before the pause is still theirs, at the same strength, and asking again for an authorisation they already gave wastes their attention. And it is not a substitute for the completion readback, which still happens after the last write.

## When the upstream has moved on

Two separate things follow from finding a mismatch, and running them together is how a brief quietly gains a commitment nobody made.

**Repairing the reference is mechanical.** If the revision you cite is preserved somewhere reachable - a project archive convention, a sibling like `IDEAS-001.r1.md` - find it, verify it hashes to the digest you cite, and point the locator at the preserved copy. That fixes a broken path and changes nothing about what has been adopted. If the referenced bytes are not reachable anywhere, record that in `missing_inputs` and cite only what exists.

**Adopting the newer revision is a decision.** It needs actual authorisation that covers this change: the user asking for it now, or a standing instruction of theirs that reaches this artifact at this scope. What cannot stand in for it: finding the old bytes, the newer document's `accepted` status, or its own `decision_ref` - that field records a decision made about that document, not the user's adoption of it into this brief.

So report the mismatch naming both identities, mark the dependent requirement or outcome stale, and leave the adopted scope standing at the strength the user gave it. Never write the newer bytes into the upstream entry under the old revision number. What this rules out is the tempting version: advance the reference, fold the newer scope into the requirements, and tell the user to say so if they disagree. That is adoption with an undo button, and it puts the user in the position of reversing a commitment they never made.

Scope the stop correctly. Staleness in the ledger revision behind `REQ-004` blocks `REQ-004`, not the whole brief and not unrelated evidence gathering.

## Ownership and concurrent writers

A session record in the authority store names one writer for an assigned worktree, branch and fence. Before dependent writes, check for one and read it.

If a record names someone else as the writer for the path you were about to write, stop those writes and report the collision - naming the record, where you read it, the owner it names and your own identity. Do not delete, reset, revert, force, switch branch, or write to an unassigned path instead; relocating leaves the path someone is watching empty. A report saved into an explicitly permitted outbox is correct behaviour, not an escape path. The absence of a base commit or a repository does not make an assignment void.

The reverse case matters just as much. A different producer and `execution_ref` in an earlier revision is history, not a competing owner. When you hold a current assignment covering that path, revise the artifact normally: preserve revision 1's bytes at a stable locator, record a resolvable `supersedes`, and leave the earlier session's attribution standing rather than rewriting it as your own. Stopping here would make every artifact unrevisable.

Missing session metadata does not prove exclusive ownership either. In bootstrap, record the actual task authorisation, inspect the destination for a collision, and use `null` plus `missing_inputs` for facts you genuinely do not have. Do not fabricate a session ID or a base commit.

## Digest order, and reading references back

No artifact contains its own complete-byte digest.

1. Write the brief. Hash it after its bytes are final.
2. Write the handoff. Put the brief's digest in the handoff's output row, and bind the completed brief in the handoff's `upstream` - one entry carrying the brief's artifact ID, revision, `store: project`, its selected path, that digest, and the sections you relied on. The output row and the upstream entry are separate claims; a correct row does not supply the causal one.
3. Hash last. If you touch a file again, hash it again.
4. Read every reference back after the last write. Each `upstream`, `supersedes`, output row, custody line, invalidation condition and continuation note that names a revision, a path or a digest must resolve, right now, to bytes that match at that locator. The same file typically appears in three places; check each occurrence rather than only the first.

A digest is only true while the bytes behind it are reachable. Before overwriting a file whose digest you cite, preserve the old bytes at a stable authorised location and point the reference at the preserved copy.

The handoff does not list itself among its own outputs and does not carry its own digest. Compute that digest after saving and reading the handoff back, then deliver the path and digest in the permitted outbox or in your message to the user - never inside the document.

## Result vocabulary

Fixed, and never blended into a single score or percentage.

| Term | Means |
| --- | --- |
| `NOT_EVALUATED` | Behaviour nobody has evaluated. |
| `NOT_RUN` | Planned, unattempted. |
| `COULD_NOT_RUN` | A required observation was blocked; the actual cause is recorded. |
| `NOT_APPLICABLE` | Excluded from the stated scope, with the reason. |
| `NOT_VALIDATED` / `NOT_OBSERVED` | Contract-header states for admission and for native activation or delivery. |

The absence of an error is not a pass. A hash match proves byte identity, never semantic accuracy, authorisation or effectiveness. Preserve an earlier report's original labels; explaining a later reclassification is fine, rewriting its history is not.
