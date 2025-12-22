---
id: STORY-139
title: Skill Loading Failure Recovery
epic: EPIC-029
sprint: Backlog
status: Backlog
points: 4
depends_on: []
priority: Medium
assigned_to: Unassigned
created: 2025-12-22
format_version: "2.3"
---

# Story: Skill Loading Failure Recovery

## Description

**As a** framework user,
**I want** clear error messages and repair instructions when the ideation skill fails to load,
**so that** I can self-recover from skill corruption without requiring support intervention.

## Acceptance Criteria

### AC#1: Skill Load Error Detection

**Given** the /ideate command invokes the devforgeai-ideation skill
**When** the skill fails to load (SKILL.md missing, corrupted, or invalid)
**Then** the error is detected and captured:
- Skill tool returns error indicator
- Error type identified (missing file, YAML parse error, invalid structure)
- Error context preserved for user display

**Test Requirements:**
- Delete SKILL.md, verify error detected
- Corrupt YAML frontmatter, verify parse error detected
- Remove required sections, verify structure error detected

---

### AC#2: HALT with Repair Instructions Display

**Given** a skill loading failure is detected
**When** the error handler executes
**Then** the user sees a clear error message:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ❌ Skill Loading Failure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The devforgeai-ideation skill failed to load.

Error Type: {YAML_PARSE_ERROR | FILE_MISSING | INVALID_STRUCTURE}
Details: {specific error message}

Possible causes:
- SKILL.md has invalid YAML frontmatter
- SKILL.md file is missing or corrupted
- Reference files in references/ are missing

Recovery steps:
1. Check: .claude/skills/devforgeai-ideation/SKILL.md exists
2. Validate YAML frontmatter (lines 1-10)
3. Compare with GitHub version: https://github.com/anthropics/claude-code
4. Run: git checkout .claude/skills/devforgeai-ideation/

If issue persists, report at: https://github.com/anthropics/claude-code/issues
```

**Test Requirements:**
- Verify error message format matches template
- Verify error type displayed correctly
- Verify recovery steps included
- Verify links are valid

---

### AC#3: No Session Crash on Skill Load Failure

**Given** the ideation skill fails to load
**When** the error is displayed to the user
**Then** the session remains active:
- Claude conversation continues (no terminal crash)
- User can run other commands
- User can attempt /ideate again after repair
- No orphaned processes or corrupted state

**Test Requirements:**
- Trigger skill load failure
- Verify subsequent commands work
- Verify /ideate retry works after repair

---

### AC#4: Specific Error Messages by Failure Type

**Given** different types of skill loading failures
**When** each error type occurs
**Then** specific, actionable error messages are displayed:

| Error Type | Message | Recovery Action |
|------------|---------|-----------------|
| FILE_MISSING | "SKILL.md not found at expected location" | "Run: git checkout .claude/skills/devforgeai-ideation/" |
| YAML_PARSE_ERROR | "Invalid YAML in frontmatter at line {N}" | "Check frontmatter syntax (lines 1-10)" |
| INVALID_STRUCTURE | "Missing required section: {section_name}" | "Compare with template at {url}" |
| PERMISSION_DENIED | "Cannot read SKILL.md - permission denied" | "Check file permissions: chmod 644" |

**Test Requirements:**
- Trigger each error type
- Verify correct message displayed
- Verify recovery action is actionable

---

## Technical Specification

```yaml
technical_specification:
  version: "2.0"

  reference_files:
    command_to_modify: ".claude/commands/ideate.md"
    skill_definition: ".claude/skills/devforgeai-ideation/SKILL.md"
    existing_error_handling: ".claude/skills/devforgeai-ideation/references/error-handling.md"

  github_repository_url: "https://github.com/anthropics/claude-code"
  github_issues_url: "https://github.com/anthropics/claude-code/issues"

  components:
    - name: SkillLoadErrorHandler
      type: Service
      description: "Handles skill loading failures with user-friendly error messages"
      location: ".claude/commands/ideate.md"
      dependencies:
        - "Skill tool error handling"
      test_requirement: "Unit tests for each error type"

    - name: ErrorMessageTemplates
      type: Configuration
      description: "Template strings for error messages by type"
      location: ".claude/commands/ideate.md"
      test_requirement: "Template formatting tests"

  business_rules:
    - id: BR-001
      description: "Skill load failures MUST display actionable recovery steps"
      test_requirement: "Verify recovery steps in all error messages"

    - id: BR-002
      description: "Session MUST remain active after skill load failure"
      test_requirement: "Post-failure command execution test"

    - id: BR-003
      description: "Error messages MUST include GitHub issue link for unresolvable errors"
      test_requirement: "Verify link presence in all templates"

  non_functional_requirements:
    - id: NFR-001
      category: User Experience
      description: "Error messages understandable by non-technical users"
      metric: "Readability score"
      target: "Grade 8 reading level"
      test_requirement: "Readability analysis of error messages"

    - id: NFR-002
      category: Reliability
      description: "Error handler itself does not crash"
      metric: "Handler stability"
      target: "100% stable"
      test_requirement: "Fuzzing test with malformed error data"
```

---

## Technical Limitations

```yaml
technical_limitations: []
# None identified at Architecture phase
```

---

## Edge Cases

| # | Scenario | Expected Behavior | Test Approach |
|---|----------|-------------------|---------------|
| 1 | Multiple errors (missing file + corrupt reference) | Show primary error, mention additional issues | Create multi-error scenario |
| 2 | Git not available for recovery | Suggest manual download instead | Mock git unavailable |
| 3 | User on read-only filesystem | Detect and explain limitation | Mock read-only FS |
| 4 | Network unavailable for GitHub link | Link still displayed (user retries later) | Mock network failure |

---

## UI Specification

**Not applicable** - Error message display in terminal.

---

## Definition of Done

### Implementation
- [ ] Skill load error detection implemented
- [ ] Error handler with HALT pattern implemented
- [ ] Error message templates implemented for all types
- [ ] Recovery steps included in all messages
- [ ] GitHub issue link included

### Quality
- [ ] All acceptance criteria verified with tests
- [ ] Code follows coding-standards.md patterns
- [ ] No CRITICAL or HIGH anti-pattern violations

### Testing
- [ ] Unit tests for SkillLoadErrorHandler
- [ ] Integration tests for each error type
- [ ] Session continuity test after failure
- [ ] Edge case tests
- [ ] Coverage meets thresholds (95%/85%/80%)

### Documentation
- [ ] Error recovery documented in troubleshooting guide
- [ ] Common failure scenarios documented

---

## Workflow Status

- [ ] Story created
- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

---

**Created:** 2025-12-22
**Source:** /create-missing-stories EPIC-029 (batch mode)
**Epic Reference:** EPIC-029 Feature 4: Skill Loading Failure Recovery
