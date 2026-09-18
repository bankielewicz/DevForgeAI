# QA Remediation Workflow (Sprint 5)

**Purpose:** Describe how the `/dev` skill behaves when `$REMEDIATION_MODE == true AND $REMEDIATION_SOURCE == "qa-recommendations"`. This file is a **cross-phase narrative**, not a set of parallel phase definitions. The inline conditionals live inside the normal phase markdown files (`phase-02-test-first.md`, `phase-03-implementation.md`, `phase-10-result.md`).

**When this file is read:** Optional reference during remediation-mode `/dev` runs. The orchestrator should already understand the flow from the phase files themselves. This file exists as a consolidated reference for debugging and documentation.

---

## Preconditions (Set by Phase 01 Step 01.9.6)

Before Phase 02 entry, Step 01.9.6 of `references/preflight/01.9-qa-failures.md` has established:

| Variable | Source | Value in remediation mode |
|----------|--------|---------------------------|
| `$REMEDIATION_MODE` | Phase 01.9.6 | `true` |
| `$REMEDIATION_SOURCE` | Phase 01.9.6 | `"qa-recommendations"` |
| `$OPEN_REC_IDS` | Phase 01.9.6 | List of REC-IDs from `qa_recommendations.open_rec_ids` |
| `$CURRENT_CYCLE` | Phase 01.9.6 | Integer assigned by `phase-cycle-start` (auto-increment) |

If any variable is missing at Phase 02 entry, remediation mode is inactive and all phases run in normal (full-story) mode.

---

## Phase 02 (Test-First / Red) — Step 1.5: Fetch REC Entries

At Phase 02 entry, Step 1.5 invokes:

```
devforgeai-validate qa-recommendations-get \
    --story-id=${STORY_ID} \
    --rec-ids="$(comma-join $OPEN_REC_IDS)" \
    --project-root=${PROJECT_ROOT} \
    --format=json
```

Exit 0 stores `payload.entries` as `$OPEN_REC_ENTRIES` — a list of full REC entry dicts with `id`, `severity`, `file`, `line`, `before_code`, `after_code`, `remediation_steps`, `verification.command`, `verification.expected`, etc.

Exit 1 with `missing_rec_ids` → HALT. Exit 2 (IO error) → HALT.

---

## Phase 02 — Step 2.3: Narrowed Test Generation

The `test-automator` subagent invocation gets a conditional preamble:

- Normal mode: `"Cover ALL acceptance criteria"` (unchanged from existing Phase 02).
- Remediation mode: `"Generate tests ONLY for the supplied REC entries. Use entry.verification.command to derive the test path and test function name; entry.verification.expected defines the passing assertion. entry.before_code (when present) describes the current defect — the new test MUST FAIL against current code."`

Phase 02's existing test-integrity snapshot (`create-test-snapshot`) runs unchanged; it overwrites any prior cycle's snapshot for this story (accepted behavior — each cycle defines its own RED state).

---

## Phase 03 (Green) — Step 2.5: Apply Remediation Entries

After test-automator delivers failing tests in Phase 02, Phase 03's Step 2.5 iterates `$OPEN_REC_ENTRIES`:

For each entry:
1. If `entry.before_code` is non-null → code-change path: Read the target file, verify `before_code` is present, Edit it to `after_code`.
2. If `entry.remediation_steps` is non-null → steps path: interpret each step as an imperative action (Edit/Write/Bash). Destructive git operations require AskUserQuestion per `.claude/rules/core/git-operations.md`.
3. Execute `entry.verification.command`. If output contains `entry.verification.expected`, append entry.id to `$CLOSED_REC_IDS`; else append to `$FAILED_REC_IDS`.

Partial success (some REC-IDs closed, others failed) → Phase 03 continues to Phase 04 with `$FAILED_REC_IDS` populated. Full failure (all entries failed) → HALT.

---

## Phases 04, 4.5, 05, 5.5, 06, 07, 08, 09 — Run As-Is

These phases execute their normal logic against whatever tests + code exist in the repo at phase entry. In remediation mode, that repo state is the narrowed subset from Phase 02-03. No remediation-specific branches are added to these phases.

- Phase 04 (Refactor) — optional tightening; LOW-severity-only cycles may skip refactor.
- Phase 4.5 / 5.5 (AC verification) — verifies all ACs still pass (story-wide, NOT narrowed). If a closed REC-ID broke an unrelated AC, AC verification catches it here.
- Phase 05 (Integration) — runs integration tests.
- Phase 06 (Deferral challenge) — operates on story DoD, independent of REC-IDs.
- Phase 07 (DoD update) — normal status transition to "Dev Complete".
- Phase 08 (Git workflow) — commit the remediation changes.
- Phase 09 (Feedback) — capture observations about the remediation cycle.

---

## Phase 10 — Step 2.5: Close the Cycle

At Phase 10 Step 2.5 (Sprint 5), the orchestrator invokes the three-step closure sequence:

```
# (a) Close the cycle in phase-state.json
devforgeai-validate phase-cycle-close \
    --story-id=${STORY_ID} \
    --cycle=${CURRENT_CYCLE} \
    --findings-closed="$(comma-join $CLOSED_REC_IDS)" \
    --completed-phase=10 \
    --project-root=${PROJECT_ROOT} \
    --format=json

# (b) Update qa-recommendations.md (Cycle History + remove closed entries)
devforgeai-validate mark-recommendations-closed \
    --story-id=${STORY_ID} \
    --rec-ids="$(comma-join $CLOSED_REC_IDS)" \
    --cycle=${CURRENT_CYCLE} \
    --project-root=${PROJECT_ROOT} \
    --format=json
```

After both succeed, Phase 10 displays:

```
Cycle ${CURRENT_CYCLE} closed
Closed: ${len($CLOSED_REC_IDS)} recommendations
Failed: ${len($FAILED_REC_IDS)} (remain open for next cycle)
Next: Run /qa ${STORY_ID} to validate and regenerate qa-recommendations.md (cycle ${CURRENT_CYCLE} + 1).
```

---

## Re-QA Loop (Archive-and-Regenerate)

When the user invokes `/qa ${STORY_ID}` after Phase 10, the QA skill's Phase 05 Step 5.4.5 (Sprint 5) runs:

```
devforgeai-validate archive-qa-recommendations \
    --story-id=${STORY_ID} \
    --project-root=${PROJECT_ROOT} \
    --format=json
```

This moves the current `{STORY_ID}-qa-recommendations.md` (which still has `cycle_number: 1` in its frontmatter — `mark-recommendations-closed` did NOT update that; only Cycle History and Blocking/Advisory sections) to `devforgeai/qa/recommendations/archive/{STORY_ID}-cycle-N.md`. N is read from the file's YAML frontmatter (with `/dev` cycle overrides available via `--cycle`).

Then Phase 05 Step 5.5 runs `generate-qa-recommendations` against the fresh findings of the re-QA pass. The generator's Sprint 2 "refuse to overwrite" safeguard passes because the file has been moved. The new file is a fresh cycle 1 (`cycle_number: 1` in frontmatter).

**Cycle-number semantics:** `/dev` cycle numbers (tracked in `phase-state.json` `cycles[]`) increase monotonically per story. `/qa` cycle numbers (tracked in `qa-recommendations.md` frontmatter + Cycle History) restart at 1 after each archive. These two numbering systems are intentionally decoupled.

---

## Error Scenarios

| Scenario | Detection | Recovery |
|----------|-----------|----------|
| All REC-IDs fail application in Phase 03 | Phase 03 Step 2.5 HALTs | User inspects failures; re-run `/dev --fix` after fix OR defer via Phase 06 |
| Specific REC-ID verification fails 3 consecutive attempts | `.claude/rules/workflow/diagnosis-before-fix.md` triggers | Invoke `spec-driven-rca` skill; apply prescription; retry |
| `phase-cycle-close` rejects `--findings-closed` (subset violation) | Phase 10 HALT | Cycle's `rec_ids` in phase-state doesn't match `$CLOSED_REC_IDS`. Inspect `$OPEN_REC_IDS` vs `$CLOSED_REC_IDS`. |
| `mark-recommendations-closed` reports a rec_id missing from file | Phase 10 HALT | Manual inspection of qa-recommendations.md. Rec may have been closed out-of-band or deferred. |
| `archive-qa-recommendations` reports target collision | QA Phase 05 Step 5.4.5 HALT | Pre-existing `archive/{STORY_ID}-cycle-N.md` from a prior failed run. Manually move or delete before retrying. |

---

## Cross-References

- Phase 01 Step 01.9.6: `references/preflight/01.9-qa-failures.md`
- Phase 02 Step 1.5 + Step 2.3 conditional: `phases/phase-02-test-first.md`
- Phase 03 Step 2.5: `phases/phase-03-implementation.md`
- Phase 10 Step 2.5: `phases/phase-10-result.md`
- QA Phase 05 Step 5.4.5 archive hook: `src/claude/skills/spec-driven-qa/phases/phase-05-reporting.md`
- `qa-recommendations-get` CLI: `src/claude/scripts/devforgeai_cli/validators/qa_recommendations_get.py`
- `mark-recommendations-closed` / `archive-qa-recommendations` CLIs: `src/claude/scripts/devforgeai_cli/validators/qa_recommendations_mutator.py`
- Sprint 3 `phase-cycle-close` CLI: `src/claude/scripts/devforgeai_cli/commands/phase_commands.py`
- Schema for REC entries: `src/claude/skills/spec-driven-qa/assets/schemas/qa-recommendations-schema.json`
