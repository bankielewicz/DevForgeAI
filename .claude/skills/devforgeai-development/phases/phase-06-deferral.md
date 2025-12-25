# Phase 06: Deferral Challenge Checkpoint

**Entry Gate:**
```bash
devforgeai-validate phase-check ${STORY_ID} --from=05 --to=06
# Exit code 0: Transition allowed
# Exit code 1: Phase 05 not complete - HALT
# Exit code 2: Missing subagents from Phase 05 - HALT
```

---

## Phase Workflow

**Purpose:** Challenge ALL deferrals - prevent autonomous deferral approval

**Required Subagents:**
- deferral-validator (Deferral validation) [CONDITIONAL]

**Steps:**

1. **Review DoD for incomplete items**
   ```
   Grep(pattern="- \\[ \\]", path="${STORY_FILE}")
   # List all unchecked DoD items
   ```

2. **Detect deferrals**
   - Check for DEFERRED markers
   - Check for incomplete items without justification

3. **IF deferrals exist: Invoke deferral-validator**
   ```
   Task(
     subagent_type="deferral-validator",
     description="Validate deferrals for ${STORY_ID}",
     prompt="""
     Validate that all deferrals are properly justified.

     Story: ${STORY_FILE}

     For each deferral, check:
     1. Technical justification exists
     2. Follow-up story referenced
     3. Not a circular deferral
     """
   )
   ```

4. **Attempt implementation for each deferral**
   - "Attempt First, Defer Only If Blocked" pattern
   - Try to implement before accepting deferral

5. **If still blocked: Challenge with user**
   ```
   AskUserQuestion(
     questions=[{
       question: "How should we handle this incomplete item?",
       header: "Deferral",
       options: [
         {label: "HALT and implement NOW (Recommended)", description: "Stop and implement this item"},
         {label: "Defer with follow-up story", description: "Create follow-up story and continue"},
         {label: "Mark as out of scope", description: "Document as intentionally excluded"}
       ],
       multiSelect: false
     }]
   )
   ```

6. **AskUserQuestion for EVERY deferral** [ENFORCED]
   - First option MUST be "HALT and implement NOW"
   - No autonomous deferral approval

c.1. **Record user approval timestamp** [MANDATORY]
   ```
   Edit(
     file_path="${STORY_FILE}",
     old_string="DEFERRED: {item}",
     new_string="DEFERRED: {item}\n   User approved: ${CURRENT_DATE}"
   )
   ```

7. **Update AC Checklist (deferral items)**

**Reference:** `references/phase-06-deferral-challenge.md` for complete workflow

---

## Validation Checkpoint

**Before proceeding to Phase 07, verify:**

- [ ] DoD reviewed for incomplete items
- [ ] IF deferrals exist: deferral-validator invoked
- [ ] AskUserQuestion invoked for EVERY deferral
- [ ] User approval timestamp recorded for each kept deferral
- [ ] AC Checklist (deferral items) updated

**IF AskUserQuestion SKIPPED:**
- AUTONOMOUS DEFERRAL DETECTED - HALT
- Claude MUST use AskUserQuestion for EVERY deferral
- First option MUST be 'HALT and implement NOW'

**IF timestamp MISSING:**
- DEFERRAL WITHOUT USER APPROVAL - HALT
- Every kept deferral MUST have 'User approved: timestamp'

---

**Exit Gate:**
```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=06 --checkpoint-passed
# Exit code 0: Phase complete, proceed to Phase 07
# Exit code 1: Cannot complete - deferrals not properly approved
```
