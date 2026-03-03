---
id: STORY-427
title: "Move Error Handling from Command to Skill Reference"
type: refactor
epic: EPIC-067
sprint: Sprint-2
status: Deferred
points: 3
depends_on: ["STORY-425", "STORY-426"]
priority: High
assigned_to: DevForgeAI AI Agent
created: 2026-02-17
format_version: "2.9"
---

# Story: Move Error Handling from Command to Skill Reference

## Description

**As a** DevForgeAI framework maintainer,
**I want** to move the error handling business logic from the ideate command to a skill reference file and simplify the brainstorm parsing in the command,
**so that** the command follows the lean orchestration principle ("commands orchestrate, skills implement") and reduces from 567 to ~460 lines.

**Context:** This story addresses conformance analysis findings 9.1 (High) and 9.2 (Medium) from Category 9: Command-Skill Separation. The command contains ~114 lines of error handling logic (lines 365-479) that should be in the skill, and ~96 lines of brainstorm parsing implementation (lines 18-113) that crosses into implementation territory.

**Analysis Source:** `devforgeai/specs/analysis/ideation-anthropic-conformance-analysis.md`, Category 9, Findings 9.1-9.2

## Acceptance Criteria

### AC#1: Error Handling Extracted to Reference File

```xml
<acceptance_criteria id="AC1" implements="FINDING-9.1">
  <given>ideate.md contains error handling logic at lines 365-479 (~114 lines)</given>
  <when>Error handling is extracted to a skill reference file</when>
  <then>A new file references/command-error-handling.md exists containing the error categorization, pattern matching, and recovery logic; ideate.md contains only a 5-line reference pointer</then>
  <verification>
    <source_files>
      <file hint="New error handling reference">.claude/skills/devforgeai-ideation/references/command-error-handling.md</file>
      <file hint="Command file">.claude/commands/ideate.md</file>
    </source_files>
    <test_file>tests/STORY-427/test_ac1_error_extraction.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Command Error Section Simplified

```xml
<acceptance_criteria id="AC2">
  <given>Error handling has been extracted (AC1)</given>
  <when>The command's error handling section is reviewed</when>
  <then>Command contains ≤10 lines for error handling: detection of error, reference loading instruction, and display delegation</then>
  <verification>
    <source_files>
      <file hint="Command file">.claude/commands/ideate.md</file>
    </source_files>
    <test_file>tests/STORY-427/test_ac2_error_section_size.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Brainstorm Parsing Simplified

```xml
<acceptance_criteria id="AC3" implements="FINDING-9.2">
  <given>Command Phase 0 contains YAML parsing logic for brainstorm frontmatter</given>
  <when>The parsing is simplified</when>
  <then>Command passes only the brainstorm file path to the skill; skill's brainstorm-handoff-workflow.md handles all YAML parsing and field extraction</then>
  <verification>
    <source_files>
      <file hint="Command file">.claude/commands/ideate.md</file>
      <file hint="Brainstorm handoff workflow">.claude/skills/devforgeai-ideation/references/brainstorm-handoff-workflow.md</file>
    </source_files>
    <test_file>tests/STORY-427/test_ac3_brainstorm_parsing.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Command Size Reduced

```xml
<acceptance_criteria id="AC4">
  <given>ideate.md is currently 567 lines</given>
  <when>Error handling and brainstorm parsing are extracted/simplified</when>
  <then>ideate.md is reduced to ≤480 lines (at least 15% reduction)</then>
  <verification>
    <source_files>
      <file hint="Command file">.claude/commands/ideate.md</file>
    </source_files>
    <test_file>tests/STORY-427/test_ac4_command_size.sh</test_file>
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
      name: "command-error-handling.md"
      file_path: ".claude/skills/devforgeai-ideation/references/command-error-handling.md"
      required_keys:
        - key: "error_categories"
          type: "array"
          example: "['FILE_MISSING', 'YAML_PARSE_ERROR', 'INVALID_STRUCTURE', 'PERMISSION_DENIED', 'UNKNOWN']"
          required: true
          test_requirement: "Test: File contains all 5 error categories"
        - key: "recovery_actions"
          type: "object"
          required: true
          test_requirement: "Test: Each error category has recovery action table row"

  business_rules:
    - id: "BR-001"
      rule: "Command may only contain error detection and reference pointer"
      trigger: "When validating command structure"
      validation: "Error handling section ≤10 lines"
      error_handling: "Fail if error handling exceeds 10 lines"
      test_requirement: "Test: Count lines in Error Handling section ≤ 10"
      priority: "High"

    - id: "BR-002"
      rule: "Command delegates YAML parsing to skill"
      trigger: "When processing brainstorm input"
      validation: "Command contains no parse_yaml_frontmatter() calls"
      error_handling: "Fail if command contains YAML parsing logic"
      test_requirement: "Test: Grep for parse_yaml_frontmatter returns empty"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Command size reduction of at least 15%"
      metric: "Line count ≤ 480 (from 567)"
      test_requirement: "Test: wc -l ideate.md ≤ 480"
      priority: "Medium"
```

---

## Dependencies

### Prerequisite Stories
- [ ] **STORY-425:** Role Prompting (Sprint 1 must complete)
- [ ] **STORY-426:** YAML Frontmatter (Sprint 1 must complete)

---

## Definition of Done

### Implementation
- [ ] references/command-error-handling.md created with full error handling logic
- [ ] Error categorization (5 types) preserved in reference file
- [ ] Recovery action table preserved in reference file
- [ ] ideate.md error section reduced to reference pointer only
- [ ] Brainstorm parsing simplified to file path passing
- [ ] brainstorm-handoff-workflow.md handles YAML parsing

### Quality
- [ ] All 4 acceptance criteria have passing tests
- [ ] No regression in error reporting functionality
- [ ] No regression in brainstorm context passing

### Testing
- [ ] Test: command-error-handling.md exists with required content
- [ ] Test: ideate.md error section ≤10 lines
- [ ] Test: No YAML parsing in command
- [ ] Test: Command line count ≤480

---

## Change Log

**Current Status:** Deferred — Blocked by EPIC-068

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-17 15:30 | devforgeai-story-creation | Created | Story created from EPIC-067 Feature 3 | STORY-427.story.md |
| 2026-02-17 | DevForgeAI AI Agent | Deferred | Blocked by EPIC-068 (Skill Responsibility Restructure). Command-skill separation partially resolved by EPIC-068 F8 (command re-routing). Re-evaluate after EPIC-068 Sprint 3 — may be fully resolved. | STORY-427.story.md |

## Notes

**Architecture Principle:** "Commands orchestrate, skills implement" — error handling is implementation, not orchestration.

**Risk Mitigation:** Create reference file first, then update command to reference it. Both changes in single commit to prevent broken state.

---

Story Template Version: 2.9
Last Updated: 2026-02-17
