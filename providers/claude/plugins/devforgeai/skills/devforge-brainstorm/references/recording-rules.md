# Recording rules: envelope, session, and honest reporting

Read this while filling artifact frontmatter, or when one of the awkward conditions below occurs. The governing sources are the DevForgeAI artifact contract and execution contract; this file distills only the parts a brainstorming session actually hits.

## Envelope fields

Every artifact this skill writes carries the `devforge.artifact/v1` envelope from the template. What to put in each field:

| Field | What goes here |
| --- | --- |
| `artifact_id` | `IDEAS-001`, `HANDOFF-001` - next unused number in the project's store. Never reuse an ID for different content. |
| `revision` | `1` for a new ledger. Revising an existing ledger increments its revision and keeps the same `artifact_id`. |
| `status` | `draft` while the user is still exploring. Only the user's actual adoption moves anything toward `accepted`. |
| `created_at_utc` | The real current UTC time for this revision. |
| `producer.skill_revision` | The SHA-256 of this skill's installed `SKILL.md`, or the plugin version if you can observe it. If you can observe neither, write `unknown` - not a plausible-looking digest. |
| `execution_ref` | The session record ID, when one exists. Usually none does; see below. |
| `upstream` | Real inputs you consumed: an existing ledger, a change request. Each entry needs `artifact_id`, `revision`, `store`, `path`, `sha256`, and the `sections` you actually used. |
| `evidence` | Sources you actually retrieved: URL, retrieval date, version if relevant, and the claim it supports. |
| `supersedes` | The prior revision you replaced, with its digest. Keep the prior bytes; do not overwrite an accepted record. |
| `decision_ref` | `null` until the user adopts something. This field is the difference between a proposal and a commitment. |
| `missing_inputs` | Everything required that you could not resolve. This is the correct home for gaps. |

Placeholders (`{{...}}`) are the template's, not yours. A required field still holding one means the artifact is a draft.

## When no session record exists

This is the normal case for someone with a new idea, and it is not an error. The execution contract's bootstrap mode covers it: a single writer, no concurrency, no Git base required yet.

Record it as it is:

```yaml
execution_ref: null
missing_inputs:
  - "session assignment: none recorded; single-writer bootstrap mode"
```

Do not invent a `SESSION-001`, do not invent a base commit SHA, and do not run `git init` or commit the user's work to manufacture a baseline. A worker-authored session ID proves nothing about ownership - assignment records come from the external authority, not from you.

If the user does supply a session record, use its ID and revision and respect the write fence it declares.

## Concurrent writers

If another session owns the worktree or branch you were about to write in: stop the dependent writes and report the collision, naming what you observed. Do not delete, reset, or force past anyone's work, and do not switch to a different branch to make the write succeed. Both sessions' work is preserved; the operator resolves the ownership.

## Stale inputs

If an upstream artifact's current bytes no longer match the revision and digest you referenced, you have a staleness condition, not a silent upgrade. Either use the preserved referenced version or report the staleness - never relabel newer bytes as the old revision. The same applies when the installed skill, base commit, or candidate changed under you: mark the affected prior evidence stale and say what needs re-running.

## Checks that could not run

A check outcome is `PASS`, `FAIL`, `NOT_RUN`, `COULD_NOT_RUN`, or `NOT_APPLICABLE`. The absence of an error is not `PASS`.

When something could not run, record `COULD_NOT_RUN` with the actual cause - tool absent, permission denied, no network, capability not implemented. Then block only the claim that actually depended on it; brainstorming itself can continue with the uncertainty written down.

Note that no available check validates brainstorming quality. `devforge check` inspects structural policy and provenance and explicitly does not certify semantic behavior. Do not describe a structural pass as evidence that the ideas are sound.

## Where things are stored

Default project artifact paths, unless the project has adopted a different map:

- `docs/devforge/ideas/` - idea ledgers
- `docs/devforge/handoffs/` - handoffs
- `docs/devforge/changes/` - change requests

Never claim a file is saved until you have observed its path and bytes.
