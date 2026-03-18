# Phase 06: Deferral Challenge

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=5.5 --to=06
# Exit 0: proceed | Exit 1: Phase 5.5 incomplete
```

## Contract

PURPOSE: Review Definition of Done for incomplete items. Challenge every deferral — attempt implementation first, defer only if blocked with explicit user approval.
REQUIRED SUBAGENTS: deferral-validator (conditional — only if deferrals exist)
REQUIRED ARTIFACTS: None
STEP COUNT: 7 mandatory steps (Steps 2-6 conditional on deferrals existing)

**CRITICAL: NO AUTONOMOUS DEFERRAL APPROVAL.** Every deferral requires AskUserQuestion. Skipping AskUserQuestion = HALT.

---

## Mandatory Steps

### Step 1: Review DoD for Incomplete Items

EXECUTE: Scan story file for unchecked DoD items.
```
Grep(pattern="- \\[ \\]", path="${STORY_FILE}")
```
VERIFY: Count incomplete items.
```
IF count == 0: No deferrals needed. Skip to Step 7, then Exit Gate.
IF count > 0: Proceed to Step 2.
```

### Step 2: Invoke Deferral Validator (CONDITIONAL)

EXECUTE: If deferrals exist, invoke validator subagent.
```
Task(
  subagent_type="deferral-validator",
  prompt="Validate deferred DoD items for ${STORY_ID}.
  Story file: ${STORY_FILE}
  Check: technical justification, follow-up story reference, circular deferral detection, implementation feasibility."
)
```
VERIFY: Task result returned with validation assessment per deferral.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=06 --subagent=deferral-validator`

### Step 3: Attempt Implementation First (CONDITIONAL)

EXECUTE: For each incomplete item, attempt to implement it NOW before deferring.
```
# "Attempt First, Defer Only If Blocked" pattern
FOR each incomplete_item:
  Attempt implementation using appropriate subagent
  IF successful: Mark [x] and skip deferral flow for this item
  IF blocked: Proceed to Step 4 for this item
```
VERIFY: Each item either implemented or documented as blocked with specific reason.

### Step 4: Challenge with User (CONDITIONAL — MANDATORY for each remaining deferral)

EXECUTE: Use AskUserQuestion for EVERY remaining deferral. First option MUST be "implement now".
```
AskUserQuestion(questions=[{
  question: "DoD item '{item}' is incomplete. How should we handle it?",
  header: "Deferral",
  options: [
    {label: "HALT and implement NOW (Recommended)", description: "Return to implementation phase"},
    {label: "Defer with follow-up story", description: "Create follow-up story for this item"},
    {label: "Mark as out of scope", description: "Remove from this story's DoD"}
  ],
  multiSelect: false
}])
```
VERIFY: User response received for each deferral.
```
IF AskUserQuestion was SKIPPED for any deferral: HALT — "AUTONOMOUS DEFERRAL DETECTED."

IF user selects "HALT and implement NOW":
  iteration_count += 1
  IF iteration_count >= 5: HALT — "Maximum TDD iterations (5) reached."
  GOTO Phase 02 (loop back)
```

### Step 5: Record User Approval Timestamp (CONDITIONAL)

EXECUTE: For each kept deferral, record user approval in story file.
```
Edit(file_path="${STORY_FILE}",
  old_string="DEFERRED: {item}",
  new_string="DEFERRED: {item}\n   User approved: ${CURRENT_DATE}")
```
VERIFY: Timestamp exists in story file.
```
Grep(pattern="User approved:", path="${STORY_FILE}")
IF deferral exists WITHOUT timestamp: HALT — "DEFERRAL WITHOUT USER APPROVAL."
```

### Step 6: Update Technical Debt Register (CONDITIONAL — UNCONDITIONAL when deferral approved)

EXECUTE: When user approves a deferral, update the technical debt register. This is UNCONDITIONAL (BR-001 per STORY-286).
```
Read(file_path="references/technical-debt-register-workflow.md")
# Follow Step 6.6 of the workflow
# Write debt entry with DEBT-NNN ID
```
VERIFY: Debt register updated. Display confirmation with DEBT-NNN ID.
```
IF user approved deferral AND register NOT updated: HALT — "Debt register update is UNCONDITIONAL."
```

### Step 7: Update AC Checklist (Deferral Items)

EXECUTE: Mark deferral-related items in AC checklist if applicable.
```
# Only required if deferrals were processed
Edit(file_path="${STORY_FILE}", old_string="- [ ] <deferral item>", new_string="- [x] <deferral item>")
```
VERIFY: If deferrals were processed, Grep confirms updates.
```
IF deferrals_existed:
  Grep(pattern="- \\[x\\].*[Dd]eferr", path="${STORY_FILE}")
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=06 --checkpoint-passed
# Exit 0: proceed to Phase 07 | Exit 1: deferrals not properly approved
```

## Optional Captures (Non-Blocking)

- Capture observations about deferral patterns
- Update session memory with deferral decisions
