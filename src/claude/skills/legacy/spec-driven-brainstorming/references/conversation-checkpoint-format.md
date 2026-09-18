---
description: Per-phase accumulating conversation checkpoint format for spec-driven-brainstorming. Reduces hallucination/drift across long Business Analysis sessions and supplies the HTML Session Transcript appendix.
version: "1.0"
created: 2026-05-16
type: reference
governing_adr: ADR-065
---

# Conversation Checkpoint Format

Governed by **ADR-065**. The 11-phase Business Analysis workflow can run long enough to
cross context-window boundaries. To prevent the model from forgetting or re-inventing
what the human-in-the-loop already said, every phase persists the actual question/answer
exchanges to a single accumulating JSON checkpoint. The same file is the resumption
artifact and the source for the Phase 11 HTML "Session Transcript" appendix.

This **replaces** the older single delete-at-end session checkpoint (which held only
session field values, not the conversation, and was deleted at synthesis).

---

## File Location

```
tmp/{BRAINSTORM_ID}/checkpoint.json
```

Project-scoped per `operational-safety.md` Rule 2 — never `/tmp/`. The `tmp/` directory
is resolved from the project root. The file is created in Phase 00 (init) and updated
at the close of every phase.

---

## Structure

```json
{
  "schema": "conversation-checkpoint-v1",
  "brainstorm_id": "BRAINSTORM-NNN",
  "topic": "user-provided session topic",
  "created": "2026-05-16T14:02:00Z",
  "last_updated": "2026-05-16T14:48:00Z",
  "current_phase": "04",
  "phases": [
    {
      "phase": "01",
      "name": "BA Planning & Approach",
      "completed": true,
      "started": "2026-05-16T14:02:00Z",
      "completed_at": "2026-05-16T14:11:00Z",
      "exchanges": [
        {
          "ts": "2026-05-16T14:03:00Z",
          "header": "Analysis scope",
          "q": "What is the scope of this analysis session?",
          "a": "MVP for an enterprise IT endpoint-monitoring platform"
        }
      ],
      "phase_summary": "Scoped the session to an MVP slice of a larger platform vision."
    }
  ]
}
```

### Field rules

- `schema` — const `conversation-checkpoint-v1`.
- `current_phase` — the phase in progress, or the last completed phase if none running.
- `phases[]` — append-only. One object per phase; never delete or rewrite a prior phase.
- `exchanges[]` — one entry per AskUserQuestion exchange: `q` is the question text, `a`
  is the user's selected/typed answer verbatim, `header` mirrors the question header,
  `ts` is ISO-8601 UTC.
- `phase_summary` — a 1–2 sentence factual summary written when the phase completes.
- `completed` — `false` while the phase is in progress, `true` once its exit criteria pass.

---

## Write Protocol

1. **Phase 00 (init):** create the file with `phases: []`, `current_phase: "00"`.
2. **On each AskUserQuestion answer:** append an `exchanges[]` entry to the current
   phase object; update `last_updated`.
3. **On phase completion:** set `completed: true`, `completed_at`, write `phase_summary`;
   advance `current_phase`.
4. Use native `Write`/`Edit` for the JSON file (operational-safety Rule 1). The file is
   small; full-rewrite on update is acceptable and avoids partial-write corruption.

---

## Resumption Protocol

On resume, read `checkpoint.json` first. `phases[]` with `completed: true` are settled —
their `exchanges[]` and `phase_summary` are GROUNDED facts; do **not** re-ask those
questions. Resume execution at `current_phase`. If the checkpoint and live session data
disagree, the checkpoint's recorded answers win (they are the verbatim human input).

---

## Relationship to the Output Document

Phase 11 renders `phases[].exchanges[]` into the collapsible "Session Transcript"
appendix of the HTML document (`{{TRANSCRIPT}}` placeholder in
`assets/templates/brainstorm-template.html`). Once the transcript is durably embedded in
the HTML, the checkpoint may be retired — its content is no longer the only copy.

---

## Anti-Hallucination Rationale

The checkpoint exists because a long multi-phase session is exactly where the model is
most likely to drift — paraphrasing the user's answers, inventing constraints, or losing
an early decision by Phase 09. Persisting verbatim exchanges at every phase makes prior
human input a re-readable GROUNDED artifact rather than a memory the model must hold.
