# Issue Creation Workflow (Phase 10 — Skill Delegation Contract)

Phase 10 is the heart of `/create-incident-from-recommendations`. It's the only phase that produces irreversible side effects (live GitHub issues posted to `bankielewicz/DevForgeAI`). For that reason, ALL Phase 10 logic lives in the `github-incident-from-recommendations` skill, NOT in this slash command.

This file documents the **contract** between the slash command and the skill. The slash command treats Phase 10 as a black-box delegation — it does not invoke the gh CLI, format issue bodies, prompt for approval, or handle posting errors directly.

---

## The contract

### Invocation

```
Skill(command="github-incident-from-recommendations", args="--batch")
```

The `--batch` argument signals "skip any setup questions; expect inputs in shared context". Mirrors the `--batch` pattern used by other framework skills.

To exercise the skill in eval mode (mock-only, no real posting), the slash command can pass `args="--batch --eval"` instead. The slash command itself never sets `--eval` — that flag exists for the skill's own evaluation harness in `evals/`. Production invocations from the slash command always omit it.

### Inputs (shared context, set by slash command before invocation)

| Variable | Type | Source | Notes |
|----------|------|--------|-------|
| `${STORY_ID}` | string | argument parsing | e.g., `STORY-661` |
| `${QA_RECS_FILE}` | path | resolved from STORY_ID | e.g., `devforgeai/qa/recommendations/STORY-661-qa-recommendations.md` |
| `selected_recommendations` | array | Phase 6-9 output | Each element has the full QA-recs schema — see `parsing-workflow.md` Phase 4 |
| `repo` | string | hardcoded in skill | `bankielewicz/DevForgeAI` per BR-007 |

### Outputs (returned to slash command)

```json
[
  {
    "rec_id": "REC-STORY-661-M-001",
    "issue_number": 42,
    "issue_url": "https://github.com/bankielewicz/DevForgeAI/issues/42",
    "status": "success",
    "error_message": null
  },
  {
    "rec_id": "REC-STORY-661-M-002",
    "issue_number": null,
    "issue_url": null,
    "status": "failed",
    "error_message": "label 'severity:medium' does not exist on this repo"
  },
  {
    "rec_id": "REC-STORY-661-L-001",
    "issue_number": null,
    "issue_url": null,
    "status": "skipped",
    "error_message": "already linked: Issue-37 (idempotency)"
  },
  {
    "rec_id": "REC-STORY-661-L-002",
    "issue_number": null,
    "issue_url": null,
    "status": "cancelled",
    "error_message": "user cancelled at approval gate"
  }
]
```

**Status values:**
- `success` — issue posted, `issue_number` and `issue_url` populated
- `failed` — gh-CLI invocation returned non-zero; `error_message` populated
- `skipped` — user excluded from subset OR already-linked (BR-009 idempotency); `error_message` describes why
- `cancelled` — user picked "Cancel all" at the approval gate (skill Phase 4); whole batch is cancelled

The slash command's Phase 11 (linking) only processes entries with `status == "success"`.

---

## What the skill does internally (high-level)

The skill runs 6 phases. The slash command is unaware of these — they're implementation details:

| Phase | Purpose | User-visible? |
|-------|---------|--------------|
| 1. Setup | Validate inputs, gh auth check, repo accessibility check, idempotency detection from QA_RECS_FILE (BR-009) | Only on errors / idempotency prompt |
| 2. Drafting | Apply embedded template to each rec → markdown body + open questions. QA recs are richer than RCA recs: `file:line` directly populates `## Files to change`, `before_code`/`after_code` map to `## Current behavior`/`## Required behavior`, `verification.command`+`expected` populate `## Test plan`, `classification` maps to `classification:regression`/`classification:pre-existing` label per BR-010, `## Labels` body section is mandatory per BR-015 | No (drafts saved to `tmp/${STORY_ID}/drafts/` per BR-006) |
| 3. Summary preview | Compact table (REC ID, Severity, Title, Labels count, Open-Qs count) | Yes — emitted to chat |
| 4. Drill-down approval | AskUserQuestion: post-all / inspect / subset / cancel | Yes — interactive |
| 5. Post | Per-rec gh-CLI invocation (hardcoded `--repo bankielewicz/DevForgeAI` per BR-007), continue-on-error (BR-004) | Yes — real-time progress |
| 6. Result | Final summary table + audit-trail update to QA_RECS_FILE (last_posted_at frontmatter + `## Posting Audit Trail` section per BR-014) + return value | Yes — emitted to chat |

For full details, see: [SKILL.md](../../../skills/github-incident-from-recommendations/SKILL.md) (Phase sections).

---

## Why the slash command does NOT do this work

Three reasons (the same reasons the RCA-pathway sibling delegates):

1. **Single Responsibility** — The slash command's responsibility is workflow orchestration: "parse QA recs → user picks subset → produce issues → link results back." The "produce issues" step is itself a multi-phase workflow with 10 business rules (BR-001 through BR-015). Mixing both into one file would push the slash command past the 500-line max in `devforgeai/specs/context/anti-patterns.md`.

2. **Auditability** — Posting GitHub issues is irreversible. Every code path that can post issues should be in ONE place, easy to audit for security (the `--repo bankielewicz/DevForgeAI` hardcoded flag — BR-007), label correctness, and approval-gate adherence (BR-005). Dispersing posting calls across multiple files multiplies the audit surface.

3. **Reusability** — A future workflow ("post issues from a code-review report" or "post issues from a CI failure log") can call the same `github-incident-from-recommendations` skill if its inputs are shaped the same. The slash command's QA-recs-specific concerns (parsing, linking back to the QA-recs file, audit-trail mutation) are isolated from issue-creation logic.

---

## What the slash command DOES do at this phase

```
# Phase 10 — entire body of slash-command logic at this phase:

Skill(command="github-incident-from-recommendations", args="--batch")

# results variable now populated by skill, used in Phase 11
```

That's it. No `gh` calls. No issue body formatting. No approval prompts. No error handling. The skill owns all of it.

---

## What if the skill fails to be invoked at all?

If `Skill(command="github-incident-from-recommendations", ...)` itself errors (skill not installed, syntax error in SKILL.md, etc.), the slash command's invocation will fail and surface that error to the user. The slash command does NOT have a fallback path — if the skill is broken, the workflow halts.

This is intentional. The skill is the only sanctioned path for posting issues. A fallback that posts directly via slash-command logic would defeat the auditability goal in reason 2 above.

If the skill is missing/broken, the user must:
1. Verify the skill exists at `.claude/skills/github-incident-from-recommendations/SKILL.md`
2. Verify it's been sync'd from `src/claude/skills/github-incident-from-recommendations/SKILL.md` (sandbox-restricted; user runs `cp -r` from their terminal)
3. Restart the Claude session if needed (skill registry caches)

---

## Cross-reference

For full details, see: [SKILL.md](../../../skills/github-incident-from-recommendations/SKILL.md) (full skill definition with all 6 phases, 15 business rules, edge cases, and the iter-3 enforcement points: ## Labels mandatory, classification: namespacing, body == join(labels), release:blocking namespacing).
