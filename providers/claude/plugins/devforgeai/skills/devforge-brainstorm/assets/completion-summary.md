# Completion summary template

The closing terminal response for this skill. It is presentation, not an artifact: no envelope, no identity, no digest, not a checkpoint, and nothing in it that is not already saved somewhere retrievable.

## The shape

```text
{{Outcome}} - {{one sentence saying what is now useful that was not before}}

- Ledger: {{path that resolves for the reader}}
- Handoff: {{path}}
- Proposed vs adopted: {{what is newly proposed, what the user actually adopted, what stays open}}
- {{Blocker}}: {{one sentence}}   <- omit this line when there is none
- Next: {{one action}} ({{owner}})

{{One sentence on what was and was not checked.}}
```

Six things, in this order: the actual outcome, the one-sentence useful result, links to the ledger and the handoff, what is proposed versus adopted and what remains open, the blocker if there is one, and one next action with its owner - then one sentence on what was and was not checked.

## Rules

- **Say what happened.** The outcome word must match the evidence. `draft-ready`, `completed`, `partial` and `blocked` are different results and none of them substitutes for another. A genuinely blocking question is not an outcome: it pauses the phase you were in, and the summary comes later.
- **The proposed-versus-adopted line is never omitted.** Every other content line can be empty and dropped; this one cannot. A summary that lets a proposal read as a decision has committed the silent promotion the whole skill exists to prevent. If nothing was adopted, say nothing was adopted.
- **60 to 120 words where that is practical.** It is a target for a summary that is padding itself, never a reason to drop a failure, a blocker, an unadopted proposal, an unobserved result or a missing input. If honesty needs more words, use more words.
- **No inventories by default.** No file manifests, digest tables, research narratives, verification matrices or run bookkeeping in the terminal response. They belong in the saved artifacts, which is where they stay retrievable.
- **Link, do not restate.** Every path must resolve for the person reading it. A path that only exists inside your sandbox is not a link.
- **Omit empty slots.** No blocker means no blocker line. Do not write "None" into four fields to make the shape look complete.
- **No extra call.** Write it from what you already have. Do not spend another model call, agent or tool run solely to format it.
- **Never a status the evidence does not support.** If no runtime verified these artifacts they are unverified drafts, and completion and any receipt stay `NOT_RUN`. Do not announce a receipt and do not write one; a runtime that published one returns its locator and digest itself.

## Examples

Illustrative, with synthetic paths.

### Draft-ready

> Draft-ready - the foster-handoff ledger now holds three competing framings of the problem with the alternatives you rejected still in the table.
>
> - Ledger: `docs/devforge/ideas/IDEAS-003.md` (revision 1)
> - Handoff: `docs/devforge/handoffs/HANDOFF-005.md`
> - Proposed vs adopted: all three framings are `proposed`; you adopted none, and `decision_ref` is null. Open: whether the real problem is the handoff or that nobody writes anything down.
> - Next: run the one-week paper-log experiment in the ledger's next step (you).
>
> Checked: locators and digests read back and match. Not checked: nothing verified these drafts - completion and receipt are `NOT_RUN`.

*(93 words.)*

### Completed

> Completed - revision 2 records your offline-on-iOS constraint as a user decision and keeps Postgres as the stated preference it actually is.
>
> - Ledger: `docs/devforge/ideas/IDEAS-001.md` (revision 2; revision 1 preserved at `IDEAS-001.r1.md`)
> - Handoff: `docs/devforge/handoffs/HANDOFF-007.md`
> - Proposed vs adopted: you adopted IDEA-002's scope in this session; the sync-conflict rule stays `proposed`. Open: what happens to edits made on two devices offline.
> - Next: decide the offline conflict rule before any architecture work (you).
>
> Checked: the supersedes digest resolves to the preserved bytes. Semantic quality is not checked by anything.

*(89 words.)*

### Partial

> Partial - the ledger is updated, and CHANGE-003's newer revision is recorded as observed context rather than applied.
>
> - Ledger: `docs/devforge/ideas/IDEAS-002.md` (revision 3)
> - Handoff: `docs/devforge/handoffs/HANDOFF-009.md`
> - Proposed vs adopted: the new idea is added and `proposed`. Your earlier adoption of IDEA-004 stands unchanged.
> - Blocker: CHANGE-003 revision 2 narrows IDEA-004's scope, and no authorization of yours covers adopting it. It is flagged, not applied.
> - Next: say whether to adopt CHANGE-003 revision 2 into the ledger (you).
>
> Checked: locators read back. The conflict is recorded, not resolved.

*(88 words.)*

### Blocked

> Blocked - no ledger was written. `docs/devforge/ideas/IDEAS-005.md` already holds another owner's artifact under a different `artifact_id`, and that is the destination this task selected.
>
> - Read at: `docs/devforge/ideas/IDEAS-005.md`, `artifact_id` `IDEAS-005@2`, producer recorded as `session-b10`
> - Produced: nothing at the selected destination; the recovery record is at `docs/devforge/handoffs/HANDOFF-011.md`
> - Proposed vs adopted: nothing proposed and nothing adopted this session - the exploration was not written down.
> - Next: confirm the destination or reassign it, then rerun (the operator who selected it).
>
> The existing artifact was not deleted, reset or relocated, and nothing was written elsewhere. Ledger status: `COULD_NOT_RUN`, with the collision as the recorded cause.

*(104 words; the collision detail is worth the overrun.)*
