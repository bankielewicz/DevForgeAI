---
id: STORY-564
title: /build-team Command and Skill Assembly
type: feature
epic: EPIC-079
sprint: Sprint-29
status: Ready for Dev
points: 1
depends_on: ["STORY-562", "STORY-563"]
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-03-03
format_version: "2.9"
---

# Story: /build-team Command and Skill Assembly

## Description

**As a** solo founder or early-stage entrepreneur using DevForgeAI,
**I want** a `/build-team` command that invokes a `building-team` skill with progressive disclosure and adaptive pacing,
**so that** I receive structured, context-aware guidance on team-building decisions without needing to navigate multiple disconnected resources.

## Acceptance Criteria

> **IMPORTANT:** XML acceptance criteria format is REQUIRED for automated verification.

### XML Acceptance Criteria Format

### AC#1: Command File Delegates to Skill

```xml
<acceptance_criteria id="AC1" implements="CMD-001">
  <given>The file src/claude/commands/build-team.md exists</given>
  <when>The command is invoked via /build-team</when>
  <then>It delegates execution to src/claude/skills/building-team/SKILL.md without containing business logic itself, and the command file is fewer than 500 lines</then>
  <verification>
    <source_files>
      <file hint="Command file">src/claude/commands/build-team.md</file>
    </source_files>
    <test_file>tests/STORY-564/test_ac1_command_delegation.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Skill File Uses Progressive Disclosure References

```xml
<acceptance_criteria id="AC2" implements="SVC-001">
  <given>The file src/claude/skills/building-team/SKILL.md exists</given>
  <when>The skill is loaded</when>
  <then>It references external files in a references/ subdirectory for detailed content rather than inlining all content, and the SKILL.md file is fewer than 1,000 lines</then>
  <verification>
    <source_files>
      <file hint="Skill file">src/claude/skills/building-team/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-564/test_ac2_progressive_disclosure.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Standalone Mode Operates Without Project Context

```xml
<acceptance_criteria id="AC3" implements="SVC-002">
  <given>A user invokes /build-team without an active project or epic context</given>
  <when>The skill executes</when>
  <then>It provides general team-building guidance workflows without errors or references to missing project files</then>
  <verification>
    <source_files>
      <file hint="Skill file">src/claude/skills/building-team/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-564/test_ac3_standalone_mode.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Project-Anchored Mode Integrates Project Context

```xml
<acceptance_criteria id="AC4" implements="SVC-003">
  <given>A user invokes /build-team while working within a project with business context</given>
  <when>The skill detects available project context</when>
  <then>It adapts guidance to the project's specific situation</then>
  <verification>
    <source_files>
      <file hint="Skill file">src/claude/skills/building-team/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-564/test_ac4_project_mode.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Adaptive Pacing Integrates with User Profile

```xml
<acceptance_criteria id="AC5" implements="SVC-004">
  <given>A user profile exists with experience-level indicators</given>
  <when>The skill renders guidance</when>
  <then>It adjusts detail depth: more explanation for novice users, concise summaries for experienced users</then>
  <verification>
    <source_files>
      <file hint="Skill file">src/claude/skills/building-team/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-564/test_ac5_adaptive_pacing.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### Source Files Guidance

Command file and skill file are separate Markdown files following DevForgeAI patterns.

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "build-team command"
      file_path: "src/claude/commands/build-team.md"
      required_keys:
        - key: "skill_invocation"
          type: "string"
          example: "Skill(command='building-team')"
          required: true
          validation: "Must reference building-team skill"
          test_requirement: "Test: Command contains skill invocation directive"
      requirements:
        - id: "CMD-001"
          description: "Thin invoker < 500 lines that delegates to building-team skill"
          testable: true
          test_requirement: "Test: Command file < 500 lines and contains no business logic"
          priority: "Critical"

    - type: "Service"
      name: "building-team skill"
      file_path: "src/claude/skills/building-team/SKILL.md"
      interface: "Markdown skill"
      lifecycle: "Static"
      dependencies:
        - "references/ subdirectory files"
        - "User profile (optional)"
        - "Project context (optional)"
      requirements:
        - id: "SVC-001"
          description: "Progressive disclosure via external reference files; SKILL.md < 1,000 lines"
          testable: true
          test_requirement: "Test: SKILL.md references at least 1 file in references/; file < 1,000 lines"
          priority: "Critical"
        - id: "SVC-002"
          description: "Standalone mode operates without project context (no errors on missing files)"
          testable: true
          test_requirement: "Test: Skill executes without error when no project context exists"
          priority: "High"
        - id: "SVC-003"
          description: "Project-anchored mode adapts output when project context is present"
          testable: true
          test_requirement: "Test: Output differs when project context file exists vs absent"
          priority: "High"
        - id: "SVC-004"
          description: "Adaptive pacing adjusts verbosity based on user profile experience level"
          testable: true
          test_requirement: "Test: Output verbosity changes between novice and experienced profile"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Command file must contain zero business logic — only delegation"
      trigger: "Command file review"
      validation: "No decision trees, guidance content, or workflow steps in command"
      error_handling: "Move logic to skill file"
      test_requirement: "Test: Command contains no workflow steps, decision trees, or guidance content"
      priority: "Critical"
    - id: "BR-002"
      rule: "Missing skill directory produces clear error, not silent failure"
      trigger: "Skill file not found at delegation path"
      validation: "Error message identifies missing skill path"
      error_handling: "Display specific error with skill path"
      test_requirement: "Test: Missing SKILL.md produces error message with path"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Command load time < 2 seconds from invocation to first output"
      metric: "< 2 seconds"
      test_requirement: "Test: Command responds within 2 seconds"
      priority: "Medium"
    - id: "NFR-002"
      category: "Scalability"
      requirement: "Total skill directory < 50 KB"
      metric: "< 50 KB (SKILL.md + all references)"
      test_requirement: "Test: du -sk returns < 50"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "User Profile Integration"
    limitation: "EPIC-072 (Assessment & Coaching Core) is in Planning status — user profile may not exist"
    decision: "workaround:default to mid-level detail depth when profile absent"
    discovered_phase: "Architecture"
    impact: "Adaptive pacing uses defaults instead of personalized settings"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Command load: < 2 seconds to first output
- Context detection: < 1 second

---

### Security

**Data Protection:**
- No secrets or credentials in command or skill files
- User profile read-only during skill execution

---

### Scalability

**Extensibility:**
- New team-building topics added by adding files to references/ without modifying SKILL.md
- Total directory < 50 KB

---

### Reliability

**Error Handling:**
- Graceful degradation: standalone mode if any project context file missing
- Missing references produce named warning, not silent skip

---

### Observability

**Logging:**
- Mode detected (standalone vs project-anchored) logged
- Profile adaptation level logged

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-562:** First Hire Decision Framework
  - **Why:** Reference file needed for first-hire guidance workflow
  - **Status:** Backlog
- [ ] **STORY-563:** Co-Founder Compatibility Assessment
  - **Why:** Reference file needed for co-founder assessment workflow
  - **Status:** Backlog

### External Dependencies

- None

### Technology Dependencies

- None (Markdown files only)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Command invokes skill, skill loads references, guidance displayed
2. **Edge Cases:**
   - No user profile → mid-level defaults
   - Partial project context → available data used
   - Missing skill directory → clear error
3. **Error Cases:**
   - SKILL.md missing → error with path

---

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **Command-to-Skill delegation:** Verify command invokes skill correctly
2. **Mode detection:** Test standalone vs project-anchored

---

## Acceptance Criteria Verification Checklist

### AC#1: Command Delegation

- [ ] Command file exists at correct path - **Phase:** 2 - **Evidence:** src/claude/commands/build-team.md
- [ ] Command < 500 lines - **Phase:** 2 - **Evidence:** wc -l
- [ ] No business logic in command - **Phase:** 2 - **Evidence:** grep for workflow patterns

### AC#2: Progressive Disclosure

- [ ] SKILL.md exists - **Phase:** 2 - **Evidence:** src/claude/skills/building-team/SKILL.md
- [ ] SKILL.md < 1,000 lines - **Phase:** 2 - **Evidence:** wc -l
- [ ] References directory with files - **Phase:** 2 - **Evidence:** ls references/

### AC#3: Standalone Mode

- [ ] No errors without project context - **Phase:** 4 - **Evidence:** integration test

### AC#4: Project-Anchored Mode

- [ ] Adapted output with project context - **Phase:** 4 - **Evidence:** integration test

### AC#5: Adaptive Pacing

- [ ] Verbosity changes per profile - **Phase:** 4 - **Evidence:** integration test

---

**Checklist Progress:** 0/10 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT -->

## Implementation Notes

*To be filled during /dev workflow*

## Definition of Done

### Implementation
- [ ] Command file created at src/claude/commands/build-team.md (< 500 lines)
- [ ] SKILL.md created at src/claude/skills/building-team/SKILL.md (< 1,000 lines)
- [ ] references/ directory with team-building reference files
- [ ] Standalone mode works without project context
- [ ] Project-anchored mode adapts with context
- [ ] Adaptive pacing based on user profile

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] Edge cases covered (no profile, partial context, missing skill)
- [ ] NFRs met (command < 500 lines, skill < 1,000 lines, dir < 50 KB)

### Testing
- [ ] Unit tests for command structure
- [ ] Unit tests for skill structure
- [ ] Integration tests for mode detection

### Documentation
- [ ] Command and skill are self-documenting
- [ ] Integration notes for EPIC-072 profile

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-03-03 | .claude/story-requirements-analyst | Created | Story created from EPIC-079 Feature 3 | STORY-564.story.md |

## Notes

**Design Decisions:**
- Command follows thin-invoker pattern per DevForgeAI conventions
- Skill uses progressive disclosure to stay under 1,000 lines
- Dual-mode (standalone + project-anchored) for flexibility
- Depends on STORY-562 and STORY-563 for reference content

**Related ADRs:**
- ADR-017: Skill naming convention (gerund-object: building-team)

---

Story Template Version: 2.9
Last Updated: 2026-03-03
