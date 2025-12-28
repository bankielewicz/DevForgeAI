# Phase 09: Feedback Hook Integration

**Entry Gate:**
```bash
devforgeai-validate phase-check ${STORY_ID} --from=08 --to=09

Examples:
 - Correct: devforgeai-validate phase-init ${STORY_ID} --project-root=.
 - Incorrrect: python -m devforgeai.cli.devforgeai_validate phase-init ${STORY_ID} --project-root=.
# Exit code 0: Transition allowed
# Exit code 1: Phase 08 not complete - HALT (commit not done)
```

---

## Phase Workflow

**Purpose:** Invoke feedback hooks for retrospective insights

**Required Subagents:** None (CLI invocation)

**Execution:** After Phase 08 (Git commit) completes

**Steps:**

1. **Check hooks configuration**
   ```bash
   devforgeai-validate check-hooks --operation=dev --status=success
   # Exit code 0: Hooks enabled
   # Exit code 1: Hooks disabled - skip step 2
   ```

2. **Invoke hooks if enabled**
   ```bash
   devforgeai-validate invoke-hooks --operation=dev --story=${STORY_ID}
   # Triggers devforgeai-feedback skill
   ```

3. **Handle hook results**
   - Non-blocking: Hook failures don't prevent workflow completion
   - Log any errors for debugging
   - Continue to Phase 10 regardless

**Reference:** See STORY-023 implementation notes

---

## Progress Indicator

Display at start of Phase 09:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 09/10: Feedback Hook (89% → 95% complete)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Validation Checkpoint

**Before proceeding to Phase 10, verify:**

- [ ] check-hooks command executed
- [ ] invoke-hooks command executed (if hooks enabled)

**Note:** This checkpoint is NON-BLOCKING - hook failures are logged but don't halt workflow

---

**Exit Gate:**
```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=09 --checkpoint-passed
# Exit code 0: Phase complete, proceed to Phase 10
# Note: Always succeeds (non-blocking phase)
```
