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

### Step 1: User Feedback Hook (existing)

1. **Check user feedback hooks configuration**
   ```bash
   devforgeai-validate check-hooks --operation=dev --status=success --type=user
   # Exit code 0: User feedback hooks enabled
   # Exit code 1: Hooks disabled - skip step 2
   ```

2. **Invoke user feedback hooks if enabled**
   ```bash
   devforgeai-validate invoke-hooks --operation=dev --story=${STORY_ID} --type=user
   # Triggers devforgeai-feedback skill (conversation mode)
   ```

### Step 2: AI Analysis Hook (NEW)

3. **Invoke AI architectural analysis**
   ```bash
   devforgeai-validate invoke-hooks --operation=dev --story=${STORY_ID} --type=ai_analysis
   # Triggers devforgeai-feedback skill (ai_analysis mode)
   ```

4. **AI analysis captures:**
   - What aspects of the framework worked well
   - Areas for improvement (non-aspirational)
   - Specific, actionable recommendations
   - Patterns observed during workflow
   - Anti-patterns detected
   - Constraint effectiveness analysis

5. **AI analysis constraints:**
   - All recommendations MUST be implementable in Claude Code Terminal
   - Validate against claude-code-terminal-expert skill
   - Store in `devforgeai/feedback/ai-analysis/{STORY_ID}/`

### Step 3: Handle Results

6. **Handle hook results**
   - Non-blocking: Hook failures don't prevent workflow completion
   - Log any errors for debugging
   - Continue to Phase 10 regardless

**Reference:** See STORY-023 implementation notes, AI Analysis enhancement (2025-12-28)

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

- [ ] check-hooks command executed (user feedback)
- [ ] invoke-hooks command executed (if user hooks enabled)
- [ ] AI analysis hook invoked
- [ ] AI analysis stored in devforgeai/feedback/ai-analysis/ (if enabled)

**Note:** This checkpoint is NON-BLOCKING - hook failures are logged but don't halt workflow

**AI Analysis Output Example:**
```json
{
  "ai_analysis": {
    "what_worked_well": ["Context file validation prevented 2 violations"],
    "areas_for_improvement": ["Phase 06 deferral check duplicates Phase 03"],
    "recommendations": [{
      "description": "Consolidate deferral validation",
      "priority": "medium",
      "feasible_in_claude_code": true
    }]
  }
}
```

---

**Exit Gate:**
```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=09 --checkpoint-passed
# Exit code 0: Phase complete, proceed to Phase 10
# Note: Always succeeds (non-blocking phase)
```
