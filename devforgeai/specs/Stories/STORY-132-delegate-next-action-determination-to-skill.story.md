---
id: STORY-132
title: Delegate Next Action Determination to Skill
epic: EPIC-028
sprint: Backlog
status: Backlog
points: 3
depends_on: []
priority: Medium
assigned_to: Unassigned
created: 2025-12-22
format_version: "2.3"
---

# Story: Delegate Next Action Determination to Skill

## Description

**As a** user executing the /ideate command,
**I want** to answer "What's next?" only ONCE (in the skill's Phase 6.6, not repeated in command Phase 5),
**so that** the workflow feels streamlined, context-aware decisions are made by the specialized skill, and I'm not asked the same question twice.

## Acceptance Criteria

### AC#1: Command Phase 5 Removed from /ideate

**Given** the /ideate command implementation with Phase 5 "Verify Next Steps Communicated",
**When** a user completes the ideation skill invocation,
**Then** the command does NOT execute Phase 5 next-action questions (lines 350-437 removed).

---

### AC#2: Skill Phase 6.6 Owns Next Action Determination

**Given** the devforgeai-ideation skill has Phase 6.6 "Completion & Handoff" that asks user for next action,
**When** the ideation skill completes Phase 6.4 self-validation,
**Then** the skill presents summary AND determines next action (greenfield→/create-context, brownfield→/create-sprint), handing off context-aware decision to user.

---

### AC#3: Command Shows Brief Confirmation Only

**Given** Phase 5 is removed from the /ideate command,
**When** the ideation skill returns output to the command,
**Then** the command displays a single confirmation message (e.g., "Ideation complete. Follow the next steps shown above.") without re-asking about next action.

---

### AC#4: No Duplication of Questions Across Command-Skill Boundary

**Given** a user runs /ideate to completion,
**When** the ideation skill (Phase 6.6) and the command execute sequentially,
**Then** the user is asked "What's next?" exactly once (by the skill, not both skill and command).

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  reference_files:
    command_to_modify: ".claude/commands/ideate.md"
    skill_definition: ".claude/skills/devforgeai-ideation/SKILL.md"
    skill_handoff_workflow: ".claude/skills/devforgeai-ideation/references/completion-handoff.md"

  grep_patterns_to_verify_removal:
    description: "After refactoring, grep for these patterns in ideate.md should return NO matches"
    patterns:
      - "## Phase 5"                  # Phase header
      - "Verify Next Steps"           # Section title
      - "AskUserQuestion"             # Duplicate question asking
      - "Ready to proceed"            # Next step question
      - "create context files"        # Next action option (skill handles this)

  components:
    - type: "Command"
      name: "ideate"
      file_path: ".claude/commands/ideate.md"
      requirements:
        - id: "CMD-001"
          description: "Remove Phase 5 next-action section (search for '## Phase 5: Verify Next Steps Communicated')"
          testable: true
          test_requirement: "Test: Grep for patterns in grep_patterns_to_verify_removal returns no matches"
          priority: "Critical"
        - id: "CMD-002"
          description: "Remove AskUserQuestion call for next-action options"
          testable: true
          test_requirement: "Test: Zero AskUserQuestion invocations in Phase 5 section (after deletion)"
          priority: "Critical"
        - id: "CMD-003"
          description: "Replace Phase 5 with single confirmation message"
          testable: true
          test_requirement: "Test: Command displays brief summary without asking user to choose next action"
          priority: "High"
        - id: "CMD-004"
          description: "Preserve skill Phase 6.6 as authoritative next-action determination"
          testable: true
          test_requirement: "Test: Skill presents next action; command does not override or re-ask"
          priority: "Critical"

  business_rules:
    - id: "BR-001"
      rule: "Next-action question must appear exactly once per ideation session"
      test_requirement: "Test: Complete ideation session produces single next-action question (from skill)"
    - id: "BR-002"
      rule: "Command must not duplicate skill's next-action logic"
      test_requirement: "Test: No AskUserQuestion about next steps in command after refactoring"
    - id: "BR-003"
      rule: "Skill Phase 6.6 is authoritative for handoff instructions"
      test_requirement: "Test: Command trusts and displays skill's next-action recommendation"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Command execution time from skill return to confirmation"
      metric: "<100ms from skill return to confirmation display"
      test_requirement: "Test: Time command Phase 5 (now just confirmation); verify <100ms"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Graceful handoff from skill to command"
      metric: "Skill MUST execute Phase 6.6 before returning; command trusts output"
      test_requirement: "Test: Verify skill completes Phase 6.6; command displays confirmation only"
    - id: "NFR-003"
      category: "User Experience"
      requirement: "Single question principle"
      metric: "User receives exactly one next-action question per session"
      test_requirement: "Test: End-to-end ideation produces single question from skill"
```

## Technical Limitations

```yaml
technical_limitations: []
# No technical limitations identified for this story
```

## Edge Cases

1. **User ignores skill's Phase 6.6 question:** Command should NOT re-ask. Skill's completion summary is final; command trusts skill output.

2. **Brownfield project with existing context files:** Skill determines next action (e.g., "/create-sprint 1" not "/create-context"). Command confirmation should reflect actual path selected by skill.

3. **Skill fails to ask next-action question (Phase 6.6 error):** Skill's error-handling must catch failures and present fallback question before returning to command.

4. **User selects "Review requirements first" in skill:** Skill hands back with instruction to edit files, then run next command manually. Command should not provide different options.

## UI Specification

**Not applicable** - This story involves command file refactoring with no visual UI components.

## Definition of Done

### Implementation Checklist
- [ ] Phase 5 next-action section removed from ideate.md (lines 350-437)
- [ ] AskUserQuestion calls removed from Phase 5
- [ ] Brief confirmation message added
- [ ] Command trusts skill Phase 6.6 output

### Testing Checklist
- [ ] Test: Grep confirms no Phase 5 next-action code in command
- [ ] Test: End-to-end ideation produces single next-action question
- [ ] Test: Confirmation message displays correctly
- [ ] Test: No duplicate questions observed

### Documentation Checklist
- [ ] EPIC-028 updated with story reference
- [ ] No additional documentation required

### Quality Checklist
- [ ] Code follows lean orchestration pattern
- [ ] No regressions in /ideate functionality
- [ ] Story marked as "Dev Complete" upon implementation

## AC Verification Checklist

### AC#1: Phase 5 Removal
- [ ] Lines 350-437 removed from ideate.md
- [ ] No "Phase 5" header remains
- [ ] No next-action logic in command

### AC#2: Skill Ownership
- [ ] Skill Phase 6.6 asks next-action question
- [ ] Skill provides context-aware recommendation
- [ ] Command does not override skill decision

### AC#3: Confirmation Only
- [ ] Brief confirmation message displays
- [ ] No AskUserQuestion in command Phase 5
- [ ] Message acknowledges skill completion

### AC#4: No Duplication
- [ ] Single question per session verified
- [ ] Question comes from skill only
- [ ] No command-level duplicate
