# Completion summary template

The closing terminal response for a workflow skill. It is presentation, not an artifact: no envelope, no identity, no digest, and nothing in it that is not already saved somewhere retrievable.

Use it for the final phase of this skill, and copy it into any multi-step workflow skill you author so that skill finishes the same way.

## The shape

```text
{{Outcome}} - {{one sentence saying what is now useful that was not before}}

- {{Primary artifact}}: {{path that resolves for the reader}}
- {{Handoff or report}}: {{path}}
- {{Material decision or blocker}}: {{one sentence}}   <- omit this line when there is none
- Next: {{one action}} ({{owner}})
```

Five things, in this order: the actual outcome, the one-sentence useful result, links to the primary artifact and the handoff or report, the material decision or blocker if there is one, and one next action with its owner.

## Rules

- **Say what happened.** The outcome word must match the evidence. `draft-ready`, `completed`, `partial`, `blocked` and a reuse recommendation are different results and none of them substitutes for another.
- **60 to 120 words where that is practical.** It is a target for a summary that is padding itself, never a reason to drop a failure, a blocker, an unobserved result or a missing input. If honesty needs more words, use more words.
- **No inventories by default.** No file manifests, digest tables, research narratives, verification matrices or run bookkeeping in the terminal response. They belong in the saved artifacts, which is where they stay retrievable. When a receipt has to leave the session, use the permitted evidence or outbox route.
- **Link, do not restate.** Every path must resolve for the person reading it. A path that only exists inside your sandbox is not a link.
- **Omit empty slots.** No blocker means no blocker line. Do not write "None" into four fields to make the shape look complete.
- **No extra call.** Write it from what you already have. Do not spend another model call, agent or tool run solely to format it.
- **Never a status the evidence does not support.** Authoring is not evaluation; behavioural status stays `NOT_EVALUATED` until someone records an actual evaluation.

## Examples

Illustrative, with synthetic paths.

### Draft-ready

> Draft-ready - the persistence expert is saved against the specification, with accepted requirements and one proposed unknown-field rule identified separately.
>
> - Candidate: `project/experts/notes-storage/SKILL.md`
> - Specification and handoff: `docs/devforge/expertise/XSPEC-004.md`, `docs/devforge/handoffs/HANDOFF-004.md`
> - Open: the unknown-field rule is drafted from RULE-003 but has no recorded approval.
> - Next: approve or amend the drafted rule, then evaluate the candidate (project owner).

*(Draft-ready example; proposed rule remains unapproved.)*

### Completed

> Completed - the notes-storage expert now covers listing ids without loading note text, and the public `load` and `save` names are unchanged.
>
> - Candidate: `project/experts/notes-storage/SKILL.md` (revision 2)
> - Package record and handoff: `docs/devforge/expertise/XPKG-002.md`, `docs/devforge/handoffs/HANDOFF-006.md`
> - Next: evaluate revision 2 against the cases in XSPEC-002 (independent evaluator).
>
> Validation status: not performed. Behavioural status: `NOT_EVALUATED` - revision 1's passing observations do not transfer to these bytes.

*(64 words.)*

### Partial

> Partial - three of the four authorised repairs are applied; CHG-004 is not, because the architecture rule it depends on is still a proposal.
>
> - Candidate: `project/experts/notes-export/SKILL.md`
> - Change record and handoff: `docs/devforge/expertise/XPKG-007.md`, `docs/devforge/handoffs/HANDOFF-009.md`
> - Blocker: CHG-004 needs a decision on whether export preserves unknown fields; it is recorded as deferred, not applied.
> - Next: decide the export rule, then reissue CHG-004 (architecture owner).

*(64 words.)*

### Blocked

> Blocked - no candidate files were changed. The intake and selection record was saved in its assigned artifact location. The assignment record shows `fixture-other-writer` holds `project/experts/notes-storage/**`, and that is the fence this task needs.
>
> - Read at: `docs/devforge/sessions/SESSION-014.md`, record `SESSION-FIXTURE-014@2`
> - Produced: the intake and selection record only, at `docs/devforge/expertise/design-notes-storage.md`
> - Next: confirm who owns that fence, or reassign this task to a free one (the operator who issued both assignments).
>
> The conflicting candidate fence was untouched; no candidate file was deleted, reset or redirected. Design status: `COULD_NOT_RUN` for the authoring step, with the collision as the recorded cause.

*(Blocked example; only the assigned intake record was saved.)*
