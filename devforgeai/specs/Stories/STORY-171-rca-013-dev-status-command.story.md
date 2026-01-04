---
id: STORY-171
title: "RCA-013 /dev-status Command"
type: feature
priority: Medium
points: 3
status: Dev Complete
epic: N/A
sprint: N/A
created: 2025-12-31
source_rca: RCA-013
source_recommendation: REC-5
tags: [rca-013, slash-command, progress-tracking, user-experience]
---

# STORY-171: RCA-013 /dev-status Command

## User Story

**As a** DevForgeAI framework user,
**I want** a `/dev-status` command to show current story progress,
**So that** I can understand "where am I?" without re-running `/dev`.

## Background

RCA-013 identified user confusion about story progress when workflow stops at 87%. REC-5 creates a lightweight command that displays:
- Current phase
- DoD completion percentage
- Remaining items
- Iteration count (if multiple TDD passes)

This helps users understand their current position without invoking the full development workflow.

## Acceptance Criteria

### AC#1: Command Displays Current Phase
**Given** STORY-057 is in development
**When** I run `/dev-status STORY-057`
**Then** it should show: "Current Phase: 4.5 (Deferral Challenge)"

### AC#2: Command Displays DoD Completion
**Given** a story with 30 DoD items, 26 complete
**When** I run `/dev-status STORY-XXX`
**Then** it should show: "DoD Completion: 26/30 (87%)"

### AC#3: Command Lists Remaining Items
**Given** a story with incomplete DoD items
**When** I run `/dev-status STORY-XXX`
**Then** it should list remaining items by category:
- Implementation: 2 remaining
- Quality: 1 remaining
- Testing: 1 remaining

### AC#4: Command Shows Iteration Count
**Given** a story that has gone through 2 TDD iterations
**When** I run `/dev-status STORY-XXX`
**Then** it should show: "TDD Iteration: 2"

### AC#5: Suggests Next Action
**Given** the current story state
**When** I run `/dev-status STORY-XXX`
**Then** it should suggest next action:
- "Run `/dev STORY-XXX` to continue development"
- OR "Run `/resume-dev STORY-XXX 2` to resume from Phase 2"
- OR "Run `/qa STORY-XXX` - development complete"

## Technical Specification

### File to Create

**`.claude/commands/dev-status.md`**

### Command Structure

```markdown
# /dev-status - Show Development Progress

Display current development progress for a story without invoking full workflow.

## Usage

```bash
/dev-status STORY-NNN
```

## Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Development Status: STORY-057
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Story:** Additional Skill Integrations
**Status:** In Development

**Progress:**
- Current Phase: 4.5 (Deferral Challenge)
- DoD Completion: 26/30 (87%)
- TDD Iteration: 2

**Remaining DoD Items:**
- Implementation: 2 items
  - [ ] Skill X integration
  - [ ] Skill Y integration
- Quality: 1 item
  - [ ] Code review complete
- Testing: 1 item
  - [ ] Integration tests passing

**Suggested Next Action:**
Run `/dev STORY-057` to continue development
OR
Run `/resume-dev STORY-057 2` to resume from Implementation phase
```

## Workflow

### Phase 0: Argument Validation
- Validate STORY-NNN format
- Locate story file
- Load YAML frontmatter

### Phase 1: Extract Current State
- Read workflow status section
- Count DoD items by category
- Get iteration count if present

### Phase 2: Display Status
- Format output with progress indicators
- List remaining items
- Suggest appropriate next action

### Phase 3: Return
- No side effects (read-only command)
```

## Definition of Done

### Implementation
- [x] Command file created at `.claude/commands/dev-status.md`
- [x] Command validates story ID argument
- [x] Command reads story file and extracts DoD status
- [x] Command displays formatted progress output
- [x] Command suggests appropriate next action
- [x] Both .claude/ and src/claude/ versions updated

### Testing
- [x] Test with story in development (partial DoD)
- [x] Test with story that has multiple iterations
- [x] Test with complete story (suggest /qa)
- [x] Test with non-existent story (error handling)

### Documentation
- [x] Added to commands-reference.md
- [x] RCA-013 updated with implementation status

## Non-Functional Requirements

### Performance
- Command should execute in <2 seconds (read-only)

### Read-Only
- Command must NOT modify story file
- Command must NOT invoke any skills

## Effort Estimate

- **Story Points:** 3 (1 SP = 4 hours)
- **Estimated Hours:** 1-2 hours
- **Complexity:** Low-Medium (read and display only)

## Dependencies

- Story files must have consistent DoD format

## References

- Source RCA: `devforgeai/RCA/RCA-013-development-workflow-stops-before-completion-despite-no-deferrals.md`
- REC-5 Section: Lines 635-640

---

## Implementation Notes

- [x] Command file created at `.claude/commands/dev-status.md` - Completed: 236 lines with YAML frontmatter
- [x] Command validates story ID argument - Completed: Phase 0 validates STORY-NNN format
- [x] Command reads story file and extracts DoD status - Completed: Phase 1 parses DoD checkboxes
- [x] Command displays formatted progress output - Completed: Phase 2 formats with progress indicators
- [x] Command suggests appropriate next action - Completed: Phase 3 suggests /dev, /resume-dev, or /qa
- [x] Both .claude/ and src/claude/ versions updated - Completed: Copied to distribution sync folder
- [x] Test with story in development (partial DoD) - Completed: test-ac2, test-ac3 validate
- [x] Test with story that has multiple iterations - Completed: test-ac4 validates iteration display
- [x] Test with complete story (suggest /qa) - Completed: test-ac5 validates /qa suggestion
- [x] Test with non-existent story (error handling) - Completed: Command includes error handling
- [x] Added to commands-reference.md - Completed: Entry added with full documentation
- [x] RCA-013 updated with implementation status - Completed: REC-5 marked complete in checklist

**Developer:** DevForgeAI AI Agent (claude/opus)
**Implemented:** 2026-01-04

### TDD Workflow Summary
- 27 tests generated across 5 test suites (100% passing)
- 4-phase workflow: Argument Validation → Extract State → Display → Suggest
- Read-only command using haiku model for fast execution

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | /create-stories-from-rca | Story created from RCA-013 REC-5 |
| 2026-01-04 | claude/opus | Development completed - /dev-status command implemented |
