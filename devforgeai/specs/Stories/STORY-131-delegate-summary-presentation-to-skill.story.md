---
id: STORY-131
title: Delegate Summary Presentation to Skill
epic: EPIC-028
sprint: Backlog
status: Backlog
points: 8
depends_on: ["STORY-133"]  # Subagent must exist before command can invoke it
priority: Medium
assigned_to: Unassigned
created: 2025-12-22
format_version: "2.3"
---

# Story: Delegate Summary Presentation to Skill

## Description

**As a** DevForgeAI command maintainer,
**I want** to remove the quick summary presentation from the /ideate command Phase 4 and delegate it to the ideation-result-interpreter subagent,
**so that** the command is streamlined toward the ~200 lines target (64% reduction), summary templates are centralized in one place (completion-handoff.md), and users receive a single, properly-formatted summary at the end of ideation instead of duplicated output.

## Acceptance Criteria

### AC#1: Phase 4 Removal Preserves Functionality

**Given** the current /ideate command with Phase 4 (quick summary presentation at lines 293-331),
**When** Phase 4 code is removed from the command,
**Then** all summary presentation logic is removed AND no functional gaps exist (summary will be handled by result interpreter in new Phase 3).

---

### AC#2: Command Invokes Existing ideation-result-interpreter Subagent

**Given** the ideation-result-interpreter subagent exists (created by STORY-133),
**When** the /ideate command's new Phase 3 executes after skill completion,
**Then** the command invokes the subagent via Task(subagent_type="ideation-result-interpreter"), passing skill output for formatting into user-facing summary.

---

### AC#3: Command Phase 3 Invokes Result Interpreter

**Given** the /ideate command completes the devforgeai-ideation skill execution (previous phases),
**When** new Phase 3 executes,
**Then** the command invokes Task(subagent_type="ideation-result-interpreter") to transform raw skill output into user-facing summary.

---

### AC#4: Command Size Reduction Achieved

**Given** the original /ideate command is 554 lines,
**When** Phase 4 removal and new Phase 3 addition are complete,
**Then** the command total is reduced toward approximately 200 lines (64% reduction target).

---

### AC#5: Summary Displays Once Per Session

**Given** a user runs the /ideate command,
**When** ideation workflow completes,
**Then** a single, formatted summary appears at the end (from result interpreter) AND no duplicate quick summary from command Phase 4 appears.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  reference_files:
    command_to_modify: ".claude/commands/ideate.md"
    skill_definition: ".claude/skills/devforgeai-ideation/SKILL.md"
    templates_source: ".claude/skills/devforgeai-ideation/references/completion-handoff.md"
    subagent_created_by: "STORY-133 (ideation-result-interpreter.md)"

  components:
    - type: "Command"
      name: "ideate"
      file_path: ".claude/commands/ideate.md"
      requirements:
        - id: "CMD-001"
          description: "Remove Phase 4 summary presentation section (search for '## Phase 4: Quick Summary')"
          testable: true
          test_requirement: "Test: Grep for 'Phase 4' or 'Quick Summary' returns no matches in ideate.md"
          priority: "Critical"
        - id: "CMD-002"
          description: "Add new Phase 3 to invoke ideation-result-interpreter subagent"
          testable: true
          test_requirement: "Test: ideate.md contains Task(subagent_type='ideation-result-interpreter')"
          priority: "Critical"
        - id: "CMD-003"
          description: "Pass skill output to result interpreter for formatting"
          testable: true
          test_requirement: "Test: Result interpreter receives complete skill output in prompt"
          priority: "High"

  # NOTE: Subagent creation is handled by STORY-133, not this story

  business_rules:
    - id: "BR-001"
      rule: "Summary must appear exactly once per ideation session"
      test_requirement: "Test: Complete ideation session produces single summary output"
    - id: "BR-002"
      rule: "Summary templates must come from completion-handoff.md only"
      test_requirement: "Test: No hardcoded summary formats in command or subagent"
    - id: "BR-003"
      rule: "Result interpreter must be stateless (no session caching)"
      test_requirement: "Test: Concurrent invocations produce isolated, correct outputs"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Result interpreter execution time under 500ms"
      metric: "<500ms from skill output to formatted display"
      test_requirement: "Test: Benchmark 10 runs with standard output; all <500ms"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Graceful degradation on malformed input"
      metric: "Zero crashes on any input; always returns valid presentation"
      test_requirement: "Test: Feed malformed JSON/missing sections; verify fallback message returned"
    - id: "NFR-003"
      category: "Maintainability"
      requirement: "Result interpreter under 200 lines"
      metric: "≤200 lines following lightweight subagent pattern"
      test_requirement: "Test: wc -l ideation-result-interpreter.md returns ≤200"
    - id: "NFR-004"
      category: "Consistency"
      requirement: "Output format matches completion-handoff.md templates exactly"
      metric: "100% template compliance"
      test_requirement: "Test: Diff formatted output against expected template output"
```

## Technical Limitations

```yaml
technical_limitations: []
# No technical limitations identified for this story
```

## Edge Cases

1. **Large ideation session output:** If skill produces output exceeding 10,000 characters, result interpreter must truncate gracefully with "..." indicators and note that full details are in artifacts. Presentation must remain under 4,000 characters.

2. **Malformed skill output:** If skill returns output missing sections or with invalid format, result interpreter must display fallback message: "Ideation completed. Review detailed output in artifacts." without crashing.

3. **Multiple brainstorm input formats:** Result interpreter must normalize variations (single vs. multiple ideas, varying complexity levels) before presentation.

4. **Empty or minimal ideation results:** If session yields no viable ideas, display appropriate message: "Exploration complete. No immediate actionable items. Recommendations documented in artifacts."

5. **Greenfield vs. Brownfield transitions:** Result interpreter must read completion-handoff.md templates to select correct next-action message based on epic_type field.

6. **Concurrent ideation sessions:** Each result interpreter invocation must be stateless and isolated.

## UI Specification

**Not applicable** - This story creates a subagent (Markdown documentation) and modifies command file. No visual UI components.

## Definition of Done

### Implementation Checklist
- [ ] Phase 4 summary presentation removed from ideate.md
- [ ] ideation-result-interpreter.md subagent created in .claude/agents/
- [ ] Subagent follows dev-result-interpreter pattern
- [ ] New Phase 3 added to command to invoke result interpreter
- [ ] completion-handoff.md templates used for formatting
- [ ] Command line count reduced toward target

### Testing Checklist
- [ ] Test: Grep confirms no Phase 4 code in command
- [ ] Test: Subagent parses valid skill output correctly
- [ ] Test: Subagent handles malformed output gracefully
- [ ] Test: Greenfield/brownfield templates applied correctly
- [ ] Test: Output truncation works for large outputs
- [ ] Test: Single summary appears per session (no duplicates)

### Documentation Checklist
- [ ] Subagent includes YAML frontmatter (name, description, tools, model)
- [ ] Subagent registered in CLAUDE.md subagent registry
- [ ] EPIC-028 updated with story reference

### Quality Checklist
- [ ] Subagent under 200 lines
- [ ] Execution time under 500ms
- [ ] No regressions in /ideate functionality
- [ ] Story marked as "Dev Complete" upon implementation

## AC Verification Checklist

### AC#1: Phase 4 Removal
- [ ] Lines 293-331 removed from ideate.md
- [ ] No "Phase 4" header remains
- [ ] No summary presentation logic in command
- [ ] Grep verification complete

### AC#2: Command Invokes Subagent (Created by STORY-133)
- [ ] Subagent exists at .claude/agents/ideation-result-interpreter.md (via STORY-133)
- [ ] Command invokes via Task(subagent_type="ideation-result-interpreter")
- [ ] Skill output passed correctly to subagent
- [ ] Formatted result displayed to user

### AC#3: Command Invocation
- [ ] New Phase 3 added to ideate.md
- [ ] Task() call with correct subagent_type
- [ ] Skill output passed in prompt
- [ ] Formatted output displayed to user

### AC#4: Size Reduction
- [ ] Initial line count documented (554)
- [ ] Final line count measured
- [ ] Progress toward 200-line target documented

### AC#5: Single Summary
- [ ] End-to-end test confirms single summary
- [ ] No duplicate output observed
- [ ] Summary comes from result interpreter only
