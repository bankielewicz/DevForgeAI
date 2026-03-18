---
description: Execute full story lifecycle end-to-end
argument-hint: [STORY-ID]
model: opus
allowed-tools: Read, Glob, Skill, AskUserQuestion
---

# /orchestrate - Complete Story Lifecycle Orchestration

Execute automated end-to-end workflow: Development → QA → Staging → Production

Orchestrates story from "Ready for Dev" through full deployment with automatic checkpoint resume and QA retry handling.

**Reference:** `references/orchestrate/orchestrate-reference.md` for detailed docs.

---

## Quick Reference

```bash
# Full orchestration (dev → QA → staging → production)
/orchestrate STORY-042

# Resume from checkpoint (auto-detected)
/orchestrate STORY-042    # Skill detects previous progress and resumes
```

---

## Command Workflow

### Phase 0: Argument Validation and Story Loading

**Validate story ID format:**
```
STORY_ID = $1

IF $1 is empty OR does NOT match pattern "STORY-[0-9]+":
  AskUserQuestion:
    Question: "Story ID format invalid. What story should I orchestrate?"
    Header: "Story ID"
    Options:
      - label: "List stories in Ready for Dev status"
        description: "Show stories ready to begin development"
      - label: "List stories in Dev Complete status"
        description: "Show stories ready for QA validation"
      - label: "List stories in QA Approved status"
        description: "Show stories ready for release"
      - label: "Show correct /orchestrate syntax"
        description: "Display usage examples"
    multiSelect: false

  Extract STORY_ID from user response OR exit if cancelled
```

**Verify story file exists:**
```
Glob(pattern="devforgeai/specs/Stories/${STORY_ID}*.story.md")

IF no matches found:
  AskUserQuestion:
    Question: "Story ${STORY_ID} not found. What should I do?"
    Header: "Story Not Found"
    Options:
      - label: "List all available stories"
        description: "Show all stories in devforgeai/specs/Stories/"
      - label: "Cancel orchestration"
        description: "Exit command"
    multiSelect: false

  IF user selects "List":
    Glob(pattern="devforgeai/specs/Stories/*.story.md")
    Display story list

  Exit command
```

**Load story via @file reference:**
```
@devforgeai/specs/Stories/${STORY_ID}*.story.md

(Story content now loaded in conversation context)
```

**Validation summary:**
```
Display:
"✓ Story ID: ${STORY_ID}
 ✓ Story file loaded
 ✓ Starting orchestration...
"
```

---

### Phase 1: Invoke Orchestration Skill

**Set context markers for skill:**
```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DevForgeAI Story Lifecycle Orchestration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Command:** orchestrate
**Story ID:** ${STORY_ID}
**Auto-Resume:** Enabled

Delegating to devforgeai-orchestration skill...
"
```

**Invoke skill:**
```
Skill(command="devforgeai-orchestration")
```

**After skill invocation:**
- Skill's SKILL.md content expands inline in conversation
- **YOU execute the skill's workflow phases** (not waiting for external result)
- Follow the skill's instructions phase by phase
- Produce output as skill instructs

**The skill executes:**
- **Phase 0:** Load story, detect checkpoints, determine starting phase
- **Phase 1:** Validate story and workflow state
- **Phase 2:** Invoke spec-driven-dev skill (TDD workflow)
- **Phase 3:** Invoke devforgeai-qa skill (deep validation)
- **Phase 3.5:** Handle QA failures with intelligent retry (max 3 attempts)
- **Phase 4:** Invoke devforgeai-release skill (staging deployment)
- **Phase 5:** Invoke devforgeai-release skill (production deployment)
- **Phase 6:** Finalize workflow, update story status, generate summary

**Skill returns:** Structured summary with orchestration results

---

### Phase 2: Display Orchestration Results

**Receive result from skill and display:**
```
Skill returns structured summary:
{
  "status": "success|halted|max_retries|already_released|blocked",
  "story_id": "STORY-NNN",
  "final_status": "Released|QA Failed|Dev Complete",
  "summary_message": "Complete message for user with metrics",
  "next_steps": [...]
}

Display orchestration results:
  {result.summary_message}

Next Steps:
  {FOR step in result.next_steps:}
    - {step}
  {END FOR}
```

---

### Phase 3: Handle Orchestration Outcomes

**Success (status = "success"):**
```
Display result.summary_message

Example:
"🎉 Story STORY-042 Orchestration Complete!

✅ Development: Code implemented, 45 tests passing
✅ QA: All quality gates passed
✅ Staging: Deployed and validated successfully
✅ Production: Live with green health checks

Duration: 75 minutes
Status: Released

Monitor production metrics for 24 hours."
```

**QA Max Retries (status = "max_retries"):**
```
Display:
"❌ Orchestration Halted - QA Max Retries Exceeded

Story: {result.story_id}
Status: QA Failed (3 attempts)

This indicates story scope is too large.

Recommended Actions:
1. Split story into 2-3 smaller stories
2. Review DoD items for proper estimation
3. Escalate blockers to leadership

QA Report: devforgeai/qa/reports/{STORY_ID}-qa-report.md"
```

**User Halted (status = "halted"):**
```
Display:
"⏸️  Orchestration Paused - User Intervention

Story: {result.story_id}
Reason: {result.halt_reason}

Resume: /orchestrate {STORY_ID} (will continue from checkpoint)"
```

**Already Released (status = "already_released"):**
Display story already released with completion date.

**Blocked (status = "blocked"):**
Display block reason and resolution guidance.

---

## Error Handling

### Story ID Invalid
```
ERROR: Invalid story ID format

Expected: STORY-NNN (e.g., STORY-001, STORY-042)
Received: '$1'

Usage: /orchestrate [STORY-ID]
```

### Story File Not Found
```
ERROR: Story file not found

Path: devforgeai/specs/Stories/${STORY_ID}*.story.md

Available stories:
{Glob(pattern="devforgeai/specs/Stories/*.story.md")}

Use /create-story to create new story.
```

### Orchestration Skill Failed
```
ERROR: Orchestration skill execution failed

Story: ${STORY_ID}
Error: {skill_error_message}

This may indicate:
- Invalid story state
- Missing prerequisites (context files)
- System issue

Review error above and retry or contact support.
```

---

## Success Criteria

- [ ] Story progresses through all required phases
- [ ] Checkpoints detected and resume works correctly
- [ ] QA failures handled with retry logic (in skill)
- [ ] All quality gates enforced
- [ ] Workflow history updated with complete timeline
- [ ] Story status = "Released" on successful completion
- [ ] Token usage: Command ~2.5K overhead + skill in isolated context

---

## Integration

**Invoked by:** User via `/orchestrate [STORY-ID]` command

**Invokes:** `devforgeai-orchestration` skill which coordinates:
- spec-driven-dev (Phase 2: TDD implementation)
- devforgeai-qa (Phase 3: Quality validation)
- devforgeai-qa retry handling (Phase 3.5: Intelligent retry with loop prevention)
- devforgeai-release (Phases 4-5: Staging and production deployment)

**Updates:**
- Story status (workflow state transitions)
- Story workflow history (timeline, checkpoints, phase results)
- Story YAML frontmatter (completed_date, orchestration metadata)

**Quality Gates Enforced:**
- Gate 1: Context Validation (before development)
- Gate 2: Test Passing (before QA)
- Gate 3: QA Approval (before release)
- Gate 4: Release Readiness (deployment validation)

---

**Version:** 3.0 - Lean Orchestration | **Pattern:** Command delegates to skill | **Reference:** `references/orchestrate/orchestrate-reference.md`
