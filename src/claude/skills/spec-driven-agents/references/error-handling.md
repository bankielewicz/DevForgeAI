# Error Handling Reference

**Purpose:** Error recovery patterns and graceful degradation for spec-driven-agents skill

---

## Graceful Degradation Priority

When errors occur, preserve data in this order (highest priority first):

1. **User specification data** - Never lose answers gathered in Phase 02
2. **Framework context** - Reference data loaded in Phase 01
3. **Generation results** - Agent file produced in Phase 04
4. **Validation results** - Compliance check data from Phase 05
5. **Reference file** - Optional reference file generation (can skip with approval)

---

## Error Types and Recovery

### 1. Checkpoint Write Failure

**Symptom:** `Write()` to checkpoint path fails
**Recovery:**
1. Retry write once
2. If retry fails: Try writing to `tmp/` directory as fallback
3. Display checkpoint data to user so they can manually save
4. Continue workflow (checkpoint is a convenience, not a hard requirement)

### 2. Reference File Load Failure

**Symptom:** `Read()` for phase reference file fails
**Recovery:**
1. Verify file path is correct (Glob for pattern match)
2. If file genuinely missing: HALT with specific error
3. If file exists but unreadable: Report WSL/filesystem issue
4. Do NOT proceed without reference -- reference loading is MANDATORY

### 3. Agent-Generator Subagent Failure

**Symptom:** `Task()` invocation returns error or empty result
**Recovery:**
1. Capture error message from Task result
2. Display to user: "Agent generation failed: {error}"
3. Offer options via AskUserQuestion:
   - Retry with same specification
   - Modify specification (return to Phase 02)
   - Cancel
4. If retry: Re-invoke Task() with same prompt
5. If modify: Reset checkpoint to Phase 02, re-gather requirements

### 4. Validation Failure (Non-Auto-Fixable)

**Symptom:** Phase 05 check returns FAIL for non-auto-fixable check
**Recovery:**
1. Display specific failure with check name and evidence
2. Offer options:
   - Accept with known issues (user acknowledges risk)
   - Regenerate (return to Phase 04)
   - Cancel
3. Record user decision in checkpoint for audit trail

### 5. Name Conflict

**Symptom:** Agent with same name already exists
**Recovery:**
1. Detected in Phase 02 Step 2.1
2. AskUserQuestion: Overwrite, Rename, or Cancel
3. If overwrite: Proceed (existing file will be replaced)
4. If rename: Ask for new name, re-validate

### 6. Template Not Found

**Symptom:** Template file path does not exist
**Recovery:**
1. List available templates via Glob
2. AskUserQuestion: Choose from available, use guided mode, or cancel
3. If guided: Switch checkpoint.parameters.creation_mode to "guided"

### 7. Custom Spec File Not Found

**Symptom:** `Read()` for spec file path fails
**Recovery:**
1. AskUserQuestion: Provide correct path, switch to guided, or cancel
2. If new path: Re-validate and continue
3. If guided: Switch mode

### 8. Context Window Approaching Limit

**Symptom:** Estimated context > 70% of window
**Recovery:**
1. Triggered in Phase Orchestration Loop context check
2. Write current checkpoint to disk
3. AskUserQuestion: "Context window getting large. Save and resume later?"
4. If save: Display resume command, EXIT skill
5. If continue: Proceed (user accepts risk of truncation)

---

## Error Message Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Error: {error_type}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase: {current_phase}
Step: {current_step}
Details: {error_message}

Recovery options:
  1. {option_1}
  2. {option_2}
  3. Cancel
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Checkpoint Recovery After Crash

If the skill exits unexpectedly (context window clear, API error, etc.):

1. User runs: `/create-agent --resume AGENT-NNN`
2. Skill reads checkpoint from disk
3. Restores to last completed phase
4. Resumes from next phase
5. All user data from Phase 02 is preserved in checkpoint
