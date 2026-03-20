# Phase 04: Skill Invocation

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=03 --to=04
```

## Contract

PURPOSE: Invoke the appropriate spec-driven skill based on story status. This is the core orchestration phase that delegates work to specialized skills. Story Management mode only.
REQUIRED SUBAGENTS: (none - delegates to skills which manage their own subagents)
REQUIRED ARTIFACTS: Skill invocation completed, story progressed to next state
STEP COUNT: 4 mandatory steps

---

## Mandatory Steps

### Step 1: Confirm Target Skill

EXECUTE: Verify the target skill determined in Phase 03 is still valid.
```
# Re-read story to confirm status hasn't changed
story_files = Glob(pattern="devforgeai/specs/Stories/${STORY_ID}*.story.md")
Read(file_path=story_files[0])

# Extract current status
Grep(pattern="^status:", path=story_files[0])

# Confirm target_skill matches current status
Display:
"Target Skill: {target_skill}
 Story Status: {current_status}
 Action: {target_action}"
```

VERIFY: target_skill still matches story status.
```
IF status changed since Phase 03:
  HALT -- "Story status changed during orchestration. Re-run Phase 03."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=04 --step=1`

### Step 2: Set Context Markers for Skill

EXECUTE: Set explicit context markers that the target skill can extract.
```
Display:
"**Story ID:** ${STORY_ID}
 **Skill:** ${target_skill}
 **Action:** ${target_action}
 **Orchestrated:** true"
```

VERIFY: Context markers are visible in conversation.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=04 --step=2`

### Step 3: Invoke Skill

EXECUTE: Invoke the target skill. The skill expands inline and YOU execute its phases.
```
IF target_skill == "spec-driven-architecture":
  Skill(command="spec-driven-architecture")

ELSE IF target_skill == "spec-driven-dev":
  Skill(command="spec-driven-dev")

ELSE IF target_skill == "spec-driven-qa":
  Skill(command="spec-driven-qa")

ELSE IF target_skill == "spec-driven-release":
  Skill(command="spec-driven-release")
```

**After skill invocation:**
- The skill's SKILL.md content expands inline
- YOU execute the skill's workflow phases sequentially
- Follow the skill's instructions phase by phase
- Complete with the skill's success/failure report

**The invoked skill manages its own:**
- Subagent invocations
- Phase state tracking
- Quality gate enforcement
- Story status updates (within its scope)

VERIFY: Skill execution completed. Check for skill result/status.
```
IF skill returned error or HALT:
  Capture error details: skill_error = {error_message}
  Display: "Skill {target_skill} returned: {skill_error}"
  # Error handling continues in Phase 06 (QA Retry) if applicable
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=04 --step=3`

### Step 4: Capture Skill Result

EXECUTE: Record the skill execution result for downstream phases.
```
skill_result = {
  "skill": target_skill,
  "status": "success" OR "failed" OR "halted",
  "story_status_after": Read story status after skill execution,
  "summary": Skill's summary output
}

# Re-read story to get updated status
Read(file_path=story_files[0])
Grep(pattern="^status:", path=story_files[0])

Display:
"Skill Execution Complete:
 Skill: {target_skill}
 Result: {skill_result.status}
 Story Status: {skill_result.story_status_after}"
```

VERIFY: skill_result is populated with a valid status.
```
IF skill_result.status is empty: HALT -- "Skill execution result not captured."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=04 --step=4`

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=04 --checkpoint-passed
```
