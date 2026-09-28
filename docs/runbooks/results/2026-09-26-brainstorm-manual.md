# Brainstorm manual test results, 2026-09-26

| Item | Value |
|---|---|
| Runbook | `docs/runbooks/brainstorm-manual-test.md` (version before the T5 fixture fix) |
| Plugin under test | copy of `src/claude/skills/devforgeai` (SKL-001 v3, SPEC-001 v7) at `/tmp/brainstorm-test/plugin` |
| Workspace | `/tmp/brainstorm-test/ws`, outside the project |
| Claude Code | 2.1.283, Opus 5.5, auto mode, user-level settings loaded |
| Driver | session devforgeai-e6, typing into the cmux tab devforgeai-worker2 and reading its screen. The driver played the user and also graded, so this is not an independent review |

## Results

| Test | Covers | Result | Notes |
|---|---|---|---|
| Setup | plugin load | pass | `/devforgeai:brainstorm` listed once |
| T1 | BEH-01, 03, 05–10 | pass | Fired on "Let's brainstorm…" with no slash command. See T1 details below |
| T2 | BEH-06 | pass | New BRN-002, owner taken from BRN-001. Answered "not converged" → `status: draft` with the confirmed dispositions. The first validator run failed; the skill fixed the file and re-ran → OK, then re-checked item 8 |
| T3 | ERR-01, BEH-11 | pass | Showed BRN-001 and asked extend vs new before writing; chose extend. All 22 v1 items unchanged; new items IDEA-13–22 and ASM-06–10; my idea recorded verbatim as IDEA-13; version 1 → 2; new Change Log row; validator OK |
| T4 | BEH-01 (VER-07) | pass | Asked "What topic should we brainstorm?"; no file; no checklist before a topic |
| T5 | VER-05 part 1 | pass, weak fixture | Picked `reverse-brainstorm` from INDEX.md because it was named; SKILL.md unchanged. It noticed the fixture was diverge-converge with only the title changed. The runbook now ships a real framework |
| T6 | VER-05 part 2, ERR-04 | pass | Index row kept, file deleted: named the missing file, fell back to diverge-converge, continued |
| T7 | ERR-02 (VER-09) | pass | Stopped after ideas were listed; offered a draft save with nothing written yet. Yes → BRN-003 `status: draft`, all 13 ideas `open` / `reason: null`, validator OK. The "no" path was exercised in T5: no file |
| T8 | ERR-05 (VER-09) | not run | Not reproducible by hand |
| T9 | VER-09, QR-01, QR-02 | pass | SKILL.md 214 lines; frontmatter keys exactly `argument-hint`, `description`, `metadata`, `name`; description 424 characters; no `<` or `>`; manifest parses; version 3 in both files |

T1 details:
- It asked 3 questions in one AskUserQuestion call.
- It named diverge-converge and said why.
- It recorded 5 problems, 12 ideas and 5 assumptions.
- My change was recorded with my reason (IDEA-02 parked instead of promoted), and it asked for the owner.
- `status: converged`.
- It reported creating `docs/specs/brainstorm/` and ran `validate_brn.py` → OK.
- The reply opened with the report block. The handoff said the PRD workflow (`/devforgeai:prd`) isn't built yet and gave the BRN path. It wrote no PRD.
- `generated_by.session` equals the real session ID.

## Observations

1. **Extending replaces the session ID.** It swaps `generated_by.session` for the extending session's ID, so the v1 session ID survives only in the Change Log. SPEC-001 doesn't say what to do here.
2. **User-level instructions leak into the test.** The test session loads the user's `~/.claude/CLAUDE.md`. In T7 it appended an entry to `~/code/papercuts.md` about the deliberately deleted `reverse-brainstorm.md`. That entry is false and should be removed. The runbook now warns about this.
3. **Unprompted git check.** In T2 the session ran `git status` on its own and reported "nothing committed". The skill doesn't mention git; harmless.
4. **The skill used the advisor** before generating ideas in T1 and T5. That's user-level tooling, not the skill.

## Leftovers

`/tmp/brainstorm-test/ws/docs/specs/brainstorm/` holds BRN-001 (v2), BRN-002 and BRN-003 for inspection.
Remove them with `rm -rf /tmp/brainstorm-test`.
