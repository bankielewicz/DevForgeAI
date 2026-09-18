# Issue Creation Workflow (Phase 10 — Skill Delegation Contract)

Phase 10 is the heart of `/create-incident-from-rca`. It's the only phase that produces irreversible side effects (live GitHub issues posted to `bankielewicz/DevForgeAI`). For that reason, ALL Phase 10 logic lives in the `github-incident-from-rca` skill, NOT in this slash command.

This file documents the **contract** between the slash command and the skill. The slash command treats Phase 10 as a black-box delegation — it does not call `gh`, format issue bodies, prompt for approval, or handle posting errors directly.

---

## The contract

### Invocation

```
Skill(command="github-incident-from-rca", args="--batch")
```

The `--batch` argument signals "skip any setup questions; expect inputs in shared context." This mirrors the `spec-driven-stories --batch` pattern used elsewhere in the framework.

### Inputs (shared context, set by slash command before invocation)

| Variable | Type | Source | Notes |
|----------|------|--------|-------|
| `${RCA_ID}` | string | argument parsing | e.g., `RCA-049` |
| `${RCA_FILE}` | path | Glob result | e.g., `devforgeai/RCA/RCA-049-batch-creation.md` |
| `selected_recommendations` | array | Phase 6-9 output | Each element has full metadata (id, priority, title, description, effort_hours, success_criteria) — see selection-workflow.md "Phase 9" |
| `repo` | string | hardcoded in skill | `bankielewicz/DevForgeAI` |

### Outputs (returned to slash command)

```json
[
  {
    "rec_id": "REC-1",
    "issue_number": 42,
    "issue_url": "https://github.com/bankielewicz/DevForgeAI/issues/42",
    "status": "success",
    "error_message": null
  },
  {
    "rec_id": "REC-2",
    "issue_number": null,
    "issue_url": null,
    "status": "failed",
    "error_message": "label 'priority:critical' does not exist on this repo"
  },
  {
    "rec_id": "REC-3",
    "issue_number": null,
    "issue_url": null,
    "status": "skipped",
    "error_message": "user excluded from subset post"
  },
  {
    "rec_id": "REC-4",
    "issue_number": null,
    "issue_url": null,
    "status": "cancelled",
    "error_message": "user cancelled at approval gate"
  }
]
```

**Status values:**
- `success` — issue posted, `issue_number` and `issue_url` populated
- `failed` — `gh issue create` returned non-zero; `error_message` populated
- `skipped` — user excluded from subset (Phase 4.4 of skill); `error_message` describes why
- `cancelled` — user picked "Cancel all" at the approval gate (Phase 4.1 of skill); whole batch is cancelled

The slash command's Phase 11 (linking) only processes entries with `status == "success"`.

---

## What the skill does internally (high-level)

The skill runs 6 phases. The slash command is unaware of these — they're an implementation detail:

| Phase | Purpose | User-visible? |
|-------|---------|--------------|
| 1. Setup | Validate inputs, `gh auth status` check, idempotency detection (BR-009) | Only on errors / idempotency prompt |
| 2. Drafting | Apply embedded template to each rec → markdown body + open questions | No (drafts saved to `tmp/${RCA_ID}/drafts/`) |
| 3. Summary preview | Compact table (REC ID, Title, Labels, Open-Qs count) | Yes — emitted to chat |
| 4. Drill-down approval | AskUserQuestion: post-all / inspect / subset / cancel | Yes — interactive |
| 5. Post | `gh issue create` per approved draft, continue-on-error | Yes — real-time progress |
| 6. Result | Final summary table + return value | Yes — emitted to chat |

For full details, see: [SKILL.md](../../../skills/github-incident-from-rca/SKILL.md) (Phase sections).

---

## Why the slash command does NOT do this work

Three reasons:

1. **Single Responsibility** — The slash command's responsibility is workflow orchestration: "parse RCA → user picks recs → produce issues → link results back." The "produce issues" step is itself a multi-phase workflow. Mixing both into one file would push the slash command past the 500-line max in the constitutional context files (`devforgeai/specs/context/anti-patterns.md` and the embedded template's "Size limits" section).

2. **Auditability** — `gh issue create` is irreversible. Every code path that can post issues should be in ONE place, easy to audit for security, label correctness, and approval-gate adherence. Dispersing posting calls across multiple files multiplies the audit surface.

3. **Reusability** — A future workflow ("post issues from a code-review report" or "post issues from a CI failure log") can call the same `github-incident-from-rca` skill if its inputs are shaped the same. The slash command's RCA-specific concerns (parsing, linking back to the RCA file) are isolated from the issue-creation logic.

---

## What the slash command DOES do at this phase

```
# Phase 10 — entire body of slash-command logic at this phase:

Skill(command="github-incident-from-rca", args="--batch")

# results variable now populated by skill, used in Phase 11
```

That's it. No `gh` calls. No issue body formatting. No approval prompts. No error handling. The skill owns all of it.

---

## What if the skill fails to be invoked at all?

If `Skill(command="github-incident-from-rca", ...)` itself errors (skill not installed, syntax error in SKILL.md, etc.), the slash command's invocation will fail and surface that error to the user. The slash command does NOT have a fallback path — if the skill is broken, the workflow halts.

This is intentional. The skill is the only sanctioned path for posting issues. A fallback that posts directly via slash-command logic would defeat the auditability goal in reason 2 above.

If the skill is missing/broken, the user must:
1. Verify the skill exists at `.claude/skills/github-incident-from-rca/SKILL.md`
2. Verify it's been sync'd from `src/claude/skills/github-incident-from-rca/SKILL.md`
3. Restart the Claude session if needed (skill registry caches)

---

## Cross-reference

For full details, see: [SKILL.md](../../../skills/github-incident-from-rca/SKILL.md) (full skill definition with all 6 phases, business rules, edge cases).
