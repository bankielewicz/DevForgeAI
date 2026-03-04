---
id: STORY-556
title: "/ops-plan Command & Skill Assembly"
type: feature
epic: EPIC-078
sprint: Sprint-28
status: Ready for Dev
points: 2
depends_on: ["STORY-554", "STORY-555"]
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-03-03
format_version: "2.9"
---

# Story: /ops-plan Command & Skill Assembly

## Description

**As a** DevForgeAI user who has completed business planning,
**I want** a single `/ops-plan` command that assembles and invokes the full operating-business skill,
**so that** I can transition from business planning to operational execution with one command that works both as a standalone tool and integrated within an active DevForgeAI project.

## Provenance

```xml
<provenance>
  <origin document="devforgeai/specs/Epics/EPIC-078-operations-launch.epic.md" section="feature-3">
    <quote>"Create /ops-plan command invoking operating-business skill"</quote>
    <line_reference>lines 57-61</line_reference>
    <quantified_impact>Single entry point for all operations guidance with project integration</quantified_impact>
  </origin>
</provenance>
```

## Acceptance Criteria

### AC#1: Command Invocation

```xml
<acceptance_criteria id="AC1" implements="OPS-001">
  <given>a user runs /ops-plan from any directory</given>
  <when>the command is invoked</when>
  <then>it invokes the operating-business skill, passes through user-provided context, and begins the workflow with a welcome message identifying which mode is active (standalone or project-anchored)</then>
  <verification>
    <source_files>
      <file hint="command invocation pattern">src/claude/commands/ops-plan.md</file>
      <file hint="skill entry point">src/claude/skills/operating-business/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-556/test-ac1-command-invocation.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Project Detection and /release Integration

```xml
<acceptance_criteria id="AC2" implements="OPS-002">
  <given>a user runs /ops-plan inside a directory containing a DevForgeAI project</given>
  <when>the command initializes</when>
  <then>it detects the active project automatically, offers /release integration, and if accepted, links generated outputs to devforgeai/specs/business/operations/ within the detected project</then>
  <verification>
    <source_files>
      <file hint="project detection logic">src/claude/commands/ops-plan.md</file>
    </source_files>
    <test_file>tests/STORY-556/test-ac2-project-detection.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Progressive Disclosure Menu

```xml
<acceptance_criteria id="AC3" implements="OPS-003">
  <given>the operating-business skill is assembled</given>
  <when>a user navigates the skill</when>
  <then>the skill presents sub-skills as a numbered menu with one-line descriptions, allowing individual or sequential invocation with progressive disclosure</then>
  <verification>
    <source_files>
      <file hint="skill menu structure">src/claude/skills/operating-business/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-556/test-ac3-progressive-disclosure-menu.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Size Constraints

```xml
<acceptance_criteria id="AC4" implements="OPS-004">
  <given>the command and skill files are created</given>
  <when>inspected for size compliance</when>
  <then>ops-plan.md is < 500 lines and SKILL.md is < 1,000 lines, with detail delegated to references/</then>
  <verification>
    <source_files>
      <file hint="command file">src/claude/commands/ops-plan.md</file>
      <file hint="skill file">src/claude/skills/operating-business/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-556/test-ac4-size-constraints.md</test_file>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "ops-plan.md"
      file_path: "src/claude/commands/ops-plan.md"
      required_keys:
        - key: "command_name"
          type: "string"
          example: "ops-plan"
          required: true
          validation: "Matches /ops-plan pattern"
          test_requirement: "Test: Command file contains ops-plan command definition"
        - key: "skill_invocation"
          type: "string"
          example: "Skill(command='operating-business')"
          required: true
          validation: "Delegates to operating-business skill"
          test_requirement: "Test: Command invokes operating-business skill"

    - type: "Configuration"
      name: "SKILL.md"
      file_path: "src/claude/skills/operating-business/SKILL.md"
      required_keys:
        - key: "sub_skills_menu"
          type: "array"
          example: "[launch-checklist, tool-selection, process-design, scaling-assessment]"
          required: true
          validation: "All 4 sub-skills listed"
          test_requirement: "Test: Skill menu contains all 4 sub-skill entries"
        - key: "references_directory"
          type: "string"
          example: "src/claude/skills/operating-business/references/"
          required: true
          validation: "Progressive disclosure references exist"
          test_requirement: "Test: References directory exists with expected files"

  business_rules:
    - id: "BR-001"
      rule: "Command is a thin invoker delegating to skill"
      trigger: "When /ops-plan is invoked"
      validation: "Command < 500 lines, no business logic in command"
      error_handling: "Display error if SKILL.md missing"
      test_requirement: "Test: Command file < 500 lines and contains Skill() invocation"
      priority: "Critical"
    - id: "BR-002"
      rule: "Project detection via devforgeai/ directory presence"
      trigger: "At command initialization"
      validation: "File system check only, no git or network calls"
      error_handling: "Default to standalone mode if detection fails"
      test_requirement: "Test: Project detected when devforgeai/ exists, standalone when absent"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Fast command initialization"
      metric: "< 3 seconds from invocation to first output"
      test_requirement: "Test: Measure command startup time"
      priority: "Medium"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Standalone mode fully functional"
      metric: "Zero dependencies on project structure"
      test_requirement: "Test: Full workflow completes without devforgeai/ directory"
      priority: "Critical"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Performance
- Command invocation to first output: < 3 seconds
- Project detection: < 500 milliseconds

### Security
- No context files read without user navigation
- No credentials requested

### Scalability
- New sub-skills added via SKILL.md menu section
- Future --mode flag support stubbed

### Reliability
- Graceful failure if SKILL.md missing
- Standalone mode fully functional without project

### Observability
- Log mode detection (standalone vs project-anchored)

---

## Dependencies

### Prerequisite Stories
- [ ] **STORY-554:** MVP Launch Checklist (reference file needed for menu)
- [ ] **STORY-555:** Tool Selection Guide (reference file needed for menu)

### External Dependencies
- None

### Technology Dependencies
- No new packages required

---

## Test Strategy

### Unit Tests
**Coverage Target:** 95%+
1. **Happy Path:** Command invokes skill, mode detected correctly
2. **Edge Cases:** No project, mid-workflow skill switch, /release integration declined then requested
3. **Error Cases:** Missing SKILL.md, missing references

### Integration Tests
**Coverage Target:** 85%+
1. Full command-to-skill invocation chain
2. Project detection and integration linking

---

## Acceptance Criteria Verification Checklist

### AC#1: Command Invocation
- [ ] Command invokes operating-business skill - **Phase:** 2
- [ ] Mode message displayed (standalone/project) - **Phase:** 2

### AC#2: Project Detection
- [ ] DevForgeAI project auto-detected - **Phase:** 2
- [ ] /release integration offered - **Phase:** 2

### AC#3: Progressive Disclosure Menu
- [ ] Numbered menu with 4 sub-skills - **Phase:** 2
- [ ] Individual and sequential invocation supported - **Phase:** 2

### AC#4: Size Constraints
- [ ] ops-plan.md < 500 lines - **Phase:** 2
- [ ] SKILL.md < 1,000 lines - **Phase:** 2

---

**Checklist Progress:** 0/8 items complete (0%)

---

## Implementation Notes

*To be filled during /dev workflow*

## Definition of Done

### Implementation
- [ ] Command file ops-plan.md created in src/claude/commands/
- [ ] Skill file SKILL.md created in src/claude/skills/operating-business/
- [ ] Project detection with /release integration offer
- [ ] Progressive disclosure menu with 4 sub-skills

### Quality
- [ ] All 4 acceptance criteria have passing tests
- [ ] Command < 500 lines, skill < 1,000 lines
- [ ] No anti-patterns

### Testing
- [ ] Unit tests for command invocation
- [ ] Unit tests for project detection
- [ ] Unit tests for size constraints
- [ ] Integration tests for command-skill chain

### Documentation
- [ ] Command usage documented in ops-plan.md
- [ ] Skill menu descriptions in SKILL.md

---

### TDD Workflow Summary
| Phase | Status | Details |
|-------|--------|---------|

### Files Created/Modified
| File | Action | Lines |
|------|--------|-------|

---

## Change Log

**Current Status:** Ready for Dev

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-03-03 | .claude/story-requirements-analyst | Created | Story created from EPIC-078 Feature 3 | STORY-556.story.md |

## Notes

**Edge Cases:**
1. Standalone mode without business plan → brief context gathering
2. Missing operations directory → auto-create
3. Mid-workflow skill conflict → detect and prompt
4. /release integration declined then requested → re-offer capability

---

Story Template Version: 2.9
Last Updated: 2026-03-03
