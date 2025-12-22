---
id: STORY-135
title: Display-Only Architecture Handoff
epic: EPIC-028
sprint: Backlog
status: Backlog
points: 2
depends_on: ["STORY-132"]
priority: Medium
assigned_to: Unassigned
created: 2025-12-22
format_version: "2.3"
---

# Story: Display-Only Architecture Handoff

## Description

**As a** framework user,
**I want** to control when the architecture skill runs without auto-invocation,
**so that** I can avoid token overflow, maintain explicit command orchestration boundaries, and have clear separation where command ends and user decides next action.

## Acceptance Criteria

### AC#1: Remove Auto-Architecture Invocation from Command

**Given** the /ideate command has completed the ideation skill execution,
**When** the command Phase 5 logic would previously trigger auto-invocation of architecture skill,
**Then** the auto-invocation is removed and command does NOT invoke the architecture skill.

---

### AC#2: Skill Phase 6.6 Displays Recommended Next Action

**Given** the devforgeai-ideation skill has completed all phases,
**When** Phase 6.6 executes (next steps synthesis),
**Then** the skill displays the text "Run `/create-context [project-name]`" as the recommended next action to the user.

---

### AC#3: Command Displays Recommendation Without Invoking Architecture

**Given** the /ideate command receives skill output with the recommended next action,
**When** command processes the skill output,
**Then** the command displays the skill's recommendation to the user but does NOT automatically invoke the architecture skill.

---

### AC#4: User Maintains Control Over Architecture Skill Execution

**Given** a user has completed ideation and seen the recommended next action,
**When** the user chooses whether to run `/create-context` or another command,
**Then** the decision to invoke the architecture skill is completely up to the user (no automatic execution).

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  reference_files:
    command_to_modify: ".claude/commands/ideate.md"
    skill_handoff_workflow: ".claude/skills/devforgeai-ideation/references/completion-handoff.md"

  context:
    W3_definition: |
      BRAINSTORM-001 Code Smell W3: "Auto-invokes architecture skill (token overflow)"

      Problem: The /ideate command previously auto-invoked the devforgeai-architecture
      skill after ideation completed, causing potential token overflow in long sessions.

      Solution: Commands should orchestrate (display next steps), not auto-execute chains.
      The user must manually run `/create-context` when ready.

      This story ensures W3 compliance by removing auto-invocation.

  components:
    - type: "Command"
      name: "ideate"
      file_path: ".claude/commands/ideate.md"
      requirements:
        - id: "CMD-001"
          description: "Remove any Skill() or Task() calls that auto-invoke architecture skill"
          testable: true
          test_requirement: "Test: Command executes without calling architecture skill invocation tools"
          priority: "Critical"
        - id: "CMD-002"
          description: "Display skill's recommended next action without auto-execution"
          testable: true
          test_requirement: "Test: Recommendation displayed; no Skill('devforgeai-architecture') call"
          priority: "Critical"
        - id: "CMD-003"
          description: "Preserve user control over next command execution"
          testable: true
          test_requirement: "Test: Command exits after display; user manually runs next command"
          priority: "Critical"

  business_rules:
    - id: "BR-001"
      rule: "Commands orchestrate, not auto-execute chains (W3 compliance)"
      test_requirement: "Test: No automatic skill chaining from /ideate to /create-context"
    - id: "BR-002"
      rule: "Clear command boundary: /ideate ends, user decides next action"
      test_requirement: "Test: Command completes without invoking another command/skill"
    - id: "BR-003"
      rule: "Skill recommendation is display-only, not execution trigger"
      test_requirement: "Test: Recommendation shown as text, not as auto-invoked skill"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "No additional skill invocation overhead"
      metric: "Command Phase 5 response time <100ms (display only)"
      test_requirement: "Test: Time from skill return to display; verify <100ms"
    - id: "NFR-002"
      category: "Token Efficiency"
      requirement: "Prevent token overflow from skill chaining"
      metric: "Phase 5 uses <500 tokens (display only, no skill execution)"
      test_requirement: "Test: Token count for Phase 5 execution"
    - id: "NFR-003"
      category: "User Experience"
      requirement: "Clear separation and user control"
      metric: "Zero automatic skill invocations after ideation"
      test_requirement: "Test: End-to-end ideation produces no automatic skill calls"
    - id: "NFR-004"
      category: "Architecture Compliance"
      requirement: "W3 violation prevention"
      metric: "Commands do not auto-chain skills"
      test_requirement: "Test: Grep for auto-invocation patterns returns empty"
```

## Technical Limitations

```yaml
technical_limitations: []
# No technical limitations identified for this story
```

## Edge Cases

1. **Skill fails to provide next action:** Display fallback message: "Next step: Review your output and run `/create-context [project-name]` when ready."

2. **User runs /ideate without brainstorm file:** Display both completion summary AND recommended next action to prevent confusion.

3. **Token budget constraints:** Display of recommended next action remains lightweight (no extra skill invocations).

4. **Brownfield vs. greenfield modes:** Different recommendations apply. Skill must determine mode and display appropriate recommendation (/orchestrate vs /create-context).

5. **Network or API failures during skill execution:** Display available recommendations up to failure point rather than leaving user with no guidance.

## UI Specification

**Not applicable** - This story involves command logic with no visual UI components.

## Definition of Done

### Implementation Checklist
- [ ] Auto-architecture invocation removed from ideate.md
- [ ] Skill recommendation displayed as text only
- [ ] No Skill() or Task() calls for architecture skill
- [ ] Command exits cleanly after display
- [ ] Fallback message for missing recommendation

### Testing Checklist
- [ ] Test: No architecture skill invocation after ideation
- [ ] Test: Recommendation displayed correctly
- [ ] Test: User can manually run /create-context after
- [ ] Test: Fallback message works when recommendation missing
- [ ] Test: Brownfield/greenfield recommendations correct

### Documentation Checklist
- [ ] EPIC-028 updated with story reference
- [ ] No additional documentation required

### Quality Checklist
- [ ] W3 compliance (no auto-chaining)
- [ ] Lean orchestration pattern followed
- [ ] No regressions in /ideate functionality
- [ ] Story marked as "Dev Complete" upon implementation

## AC Verification Checklist

### AC#1: No Auto-Invocation
- [ ] Skill() call for architecture removed
- [ ] Task() call for architecture removed
- [ ] Grep confirms no auto-invocation patterns

### AC#2: Skill Recommendation
- [ ] Phase 6.6 displays next action text
- [ ] Format: "Run `/create-context [project-name]`"
- [ ] Displayed before skill returns

### AC#3: Display Only
- [ ] Command shows recommendation
- [ ] No automatic execution
- [ ] User sees clear next step

### AC#4: User Control
- [ ] Command exits after display
- [ ] User manually runs next command
- [ ] No forced workflow
