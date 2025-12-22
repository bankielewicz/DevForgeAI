---
id: STORY-134
title: Smart Greenfield/Brownfield Detection
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

# Story: Smart Greenfield/Brownfield Detection

## Description

**As a** command user,
**I want** the /ideate command to automatically detect whether my project is greenfield or brownfield based on context file existence,
**so that** I receive intelligent next steps without manual mode specification and reduce friction in the development workflow.

## Acceptance Criteria

### AC#1: Brownfield Mode Detection

**Given** a project with all 6 context files present (tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md),
**When** the /ideate command executes Phase 1 (argument validation),
**Then** the command detects brownfield mode and passes `mode: brownfield` context marker to the skill, which skips architecture handoff and suggests /orchestrate as next step.

---

### AC#2: Greenfield Mode Detection

**Given** a project with fewer than 6 context files present,
**When** the /ideate command executes Phase 1 (argument validation),
**Then** the command detects greenfield mode and passes `mode: greenfield` context marker to the skill, which provides guidance to run /create-context.

---

### AC#3: Smart Mode Context Passing

**Given** the command has determined project mode (greenfield or brownfield),
**When** Phase 1 completes and control transfers to the skill,
**Then** the context marker contains the detected mode in a format parseable by Phase 6.6 (next action suggestion), and the skill references this marker to customize its final output.

---

### AC#4: Performance and Consistency

**Given** a project with mixed or partial context file states,
**When** the /ideate command performs the glob check,
**Then** the detection uses exact count comparison (== 6 for brownfield, < 6 for greenfield), completes in <50ms, and produces consistent results across multiple invocations.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  reference_files:
    command_to_modify: ".claude/commands/ideate.md"
    skill_definition: ".claude/skills/devforgeai-ideation/SKILL.md"
    context_files_location: "devforgeai/specs/context/*.md"

  context_marker_format:
    description: "How to pass mode marker from command to skill"
    location: "Inline text block displayed before Skill() invocation"
    format_example: |
      **Project Mode Context:**
      - **Mode:** {greenfield|brownfield}
      - **Context Files Found:** {count}/6
      - **Detection Method:** Filesystem glob

      The skill's Phase 6.6 will read this mode to determine next-action recommendation:
      - Greenfield → recommend `/create-context [project-name]`
      - Brownfield → recommend `/create-sprint` or `/create-story`
    skill_consumption: |
      The skill reads the **Mode:** line during Phase 6.6 (completion-handoff.md)
      to customize the next-action message. No parsing required - just pattern match
      on "**Mode:** greenfield" or "**Mode:** brownfield" in context.

  components:
    - type: "Command"
      name: "ideate"
      file_path: ".claude/commands/ideate.md"
      requirements:
        - id: "CMD-001"
          description: "Add context file detection in Phase 1 after argument validation"
          testable: true
          test_requirement: "Test: Phase 1 includes Glob(pattern='devforgeai/specs/context/*.md')"
          priority: "Critical"
        - id: "CMD-002"
          description: "Count context files and determine mode (6 = brownfield, <6 = greenfield)"
          testable: true
          test_requirement: "Test: Mode correctly determined based on file count"
          priority: "Critical"
        - id: "CMD-003"
          description: "Pass mode marker to skill in context"
          testable: true
          test_requirement: "Test: Skill receives 'mode: greenfield' or 'mode: brownfield' marker"
          priority: "Critical"
        - id: "CMD-004"
          description: "Detection completes in <50ms"
          testable: true
          test_requirement: "Test: Glob and count operation completes in <50ms"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Exactly 6 context files = brownfield mode"
      test_requirement: "Test: 6 files present returns 'brownfield'"
    - id: "BR-002"
      rule: "Fewer than 6 context files = greenfield mode"
      test_requirement: "Test: 0-5 files present returns 'greenfield'"
    - id: "BR-003"
      rule: "Detection is filesystem-based, not git-based"
      test_requirement: "Test: Gitignored files still detected if present in filesystem"
    - id: "BR-004"
      rule: "Mode affects skill's Phase 6.6 next-action recommendation"
      test_requirement: "Test: Greenfield → /create-context; Brownfield → /orchestrate"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Detection latency"
      metric: "<50ms for glob operation (p95)"
      test_requirement: "Test: Measure elapsed time; verify <50ms on large projects"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Glob failure handling"
      metric: "Graceful error message if directory inaccessible"
      test_requirement: "Test: Permission error returns user-friendly message"
    - id: "NFR-003"
      category: "Consistency"
      requirement: "Deterministic detection"
      metric: "Same project state always produces same mode"
      test_requirement: "Test: Multiple invocations return identical mode"
```

## Technical Limitations

```yaml
technical_limitations: []
# No technical limitations identified for this story
```

## Edge Cases

1. **Partial/Corrupted Context Files:** Project has 6 file names but some are empty or corrupted. Detection counts existence only, not validity. Invalid files detected during context validation gate.

2. **Missing Individual Context File:** Project has 5/6 context files. Detection returns greenfield mode; user may need to regenerate missing file via /create-context.

3. **Extra Context Files:** Project has 7+ files in context directory. Detection treats >=6 as brownfield to accommodate future additions.

4. **Symlinked or Nested Paths:** Glob pattern only matches standard location. Users must ensure files in correct path.

5. **Concurrent Execution:** No race conditions (read-only operation). Each invocation gets independent detection.

6. **Git Ignored Context Files:** Glob finds files regardless of git status (filesystem-based, not repo-aware).

## UI Specification

**Not applicable** - This story involves command logic with no visual UI components.

## Definition of Done

### Implementation Checklist
- [ ] Glob check added to ideate.md Phase 1
- [ ] Context file counting logic implemented
- [ ] Mode determination (6 = brownfield, <6 = greenfield)
- [ ] Context marker passed to skill
- [ ] Error handling for glob failures

### Testing Checklist
- [ ] Test: 6 context files detected as brownfield
- [ ] Test: 0-5 context files detected as greenfield
- [ ] Test: Mode marker received by skill
- [ ] Test: Detection completes in <50ms
- [ ] Test: Glob failure produces user-friendly error

### Documentation Checklist
- [ ] EPIC-028 updated with story reference
- [ ] No additional documentation required

### Quality Checklist
- [ ] Glob uses native tool (not Bash)
- [ ] No regressions in /ideate functionality
- [ ] Story marked as "Dev Complete" upon implementation

## AC Verification Checklist

### AC#1: Brownfield Detection
- [ ] 6 context files present
- [ ] Mode = brownfield
- [ ] Next action = /orchestrate suggested

### AC#2: Greenfield Detection
- [ ] <6 context files present
- [ ] Mode = greenfield
- [ ] Next action = /create-context suggested

### AC#3: Context Passing
- [ ] Mode marker in skill context
- [ ] Skill reads mode correctly
- [ ] Phase 6.6 uses mode for recommendation

### AC#4: Performance
- [ ] Detection <50ms
- [ ] Consistent across invocations
- [ ] No caching side effects
