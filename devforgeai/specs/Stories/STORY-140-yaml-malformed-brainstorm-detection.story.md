---
id: STORY-140
title: YAML-Malformed Brainstorm Detection
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

# Story: YAML-Malformed Brainstorm Detection

## Description

**As a** framework user with a corrupted brainstorm file,
**I want** the ideation skill to detect malformed YAML and offer graceful fallback,
**so that** I can continue with fresh ideation instead of experiencing a crash.

## Acceptance Criteria

### AC#1: YAML Validation on Brainstorm Load

**Given** the user selects a brainstorm file to continue from (via /ideate command Phase 0 brainstorm selection or direct file reference)
**When** the skill loads the brainstorm file in Phase 1 Step 0 (brainstorm handoff detection)
**Then** YAML validation occurs:
- Parse YAML frontmatter (lines between `---` markers)
- Validate required fields present (id, title, status, created)
- Validate field types match schema
- Validation completes before any user prompts

**Test Requirements:**
- Valid brainstorm loads successfully
- Invalid YAML detected before processing
- Validation time < 100ms

---

### AC#2: Clear Error Message on Parse Failure

**Given** a brainstorm file has malformed YAML
**When** the YAML parser encounters an error
**Then** user sees informative error:

```
⚠️ Brainstorm file has invalid YAML

File: devforgeai/specs/brainstorms/BRAINSTORM-001.brainstorm.md
Error: {YAML parser error message}
Line: {line number if available}

The file cannot be loaded in its current state.
```

**Test Requirements:**
- Verify error message format
- Verify file path displayed
- Verify line number shown when available

---

### AC#3: Graceful Fallback to Fresh Ideation

**Given** a brainstorm file fails YAML validation
**When** the error is displayed to the user
**Then** the skill offers to continue:
- AskUserQuestion: "Proceed with fresh ideation (skip brainstorm)?"
- Option 1: "Yes, start fresh" → Continue without brainstorm context
- Option 2: "No, I'll fix the file first" → HALT session

**Test Requirements:**
- Verify AskUserQuestion presented after error
- Test "Yes" path (session continues)
- Test "No" path (session halts cleanly)

---

### AC#4: Validation for Common YAML Errors

**Given** various YAML syntax errors in brainstorm files
**When** each error type is encountered
**Then** specific, helpful error messages are displayed:

| Error Type | Example | Message |
|------------|---------|---------|
| Missing closing delimiter | `---\nid: BRAINSTORM-001\ntitle:` | "Unclosed YAML frontmatter - missing closing ---" |
| Invalid indentation | Tabs mixed with spaces | "Invalid indentation at line {N} - use spaces only" |
| Duplicate keys | Two `id:` fields | "Duplicate key 'id' at line {N}" |
| Invalid value type | `created: not-a-date` | "Invalid date format for 'created' field" |
| Missing required field | No `id:` field | "Missing required field: id" |

**Test Requirements:**
- Create fixture for each error type
- Verify correct message for each
- Verify line numbers accurate

---

### AC#5: Brainstorm Schema Validation

**Given** a brainstorm file has valid YAML syntax but missing/invalid fields
**When** schema validation executes
**Then** specific field errors are reported:
- Required fields: id, title, status, created
- Optional fields validated if present: problem_statement, key_challenges, personas
- Validation stops at first error (fail-fast) with clear message

**Test Requirements:**
- Test each required field missing
- Test invalid field types
- Verify fail-fast behavior

---

## Technical Specification

```yaml
technical_specification:
  version: "2.0"

  reference_files:
    skill_to_modify: ".claude/skills/devforgeai-ideation/SKILL.md"
    brainstorm_handoff: ".claude/skills/devforgeai-ideation/references/brainstorm-handoff-workflow.md"
    error_handling: ".claude/skills/devforgeai-ideation/references/error-handling.md"
    brainstorm_template: ".claude/skills/devforgeai-brainstorming/assets/templates/brainstorm-template.md"

  components:
    - name: BrainstormValidator
      type: Service
      description: "Validates brainstorm YAML syntax and schema"
      location: ".claude/skills/devforgeai-ideation/references/brainstorm-handoff-workflow.md"
      dependencies:
        - "Read tool"
        - "YAML parser (implicit in Read)"
      test_requirement: "Unit tests for all validation scenarios"

    - name: YAMLErrorMapper
      type: Service
      description: "Maps YAML parser errors to user-friendly messages"
      location: ".claude/skills/devforgeai-ideation/references/error-handling.md"
      test_requirement: "Error mapping tests for each error type"

    - name: BrainstormSchema
      type: DataModel
      description: "Schema definition for brainstorm file validation"
      location: ".claude/skills/devforgeai-brainstorming/assets/templates/brainstorm-template.md"
      fields:
        - name: id
          type: string
          pattern: "BRAINSTORM-NNN"
          required: true
        - name: title
          type: string
          required: true
        - name: status
          type: enum
          values: ["Active", "Complete", "Abandoned"]
          required: true
        - name: created
          type: date
          format: "YYYY-MM-DD"
          required: true
      test_requirement: "Schema validation tests"

  business_rules:
    - id: BR-001
      description: "YAML validation MUST occur before any user interaction"
      test_requirement: "Verify validation timing in skill flow"

    - id: BR-002
      description: "Validation failures MUST offer fallback, not crash"
      test_requirement: "Graceful degradation test"

    - id: BR-003
      description: "Error messages MUST be actionable (what to fix)"
      test_requirement: "Error message content validation"

  non_functional_requirements:
    - id: NFR-001
      category: Performance
      description: "Validation completes < 100ms"
      metric: "Validation duration"
      target: "< 100ms"
      test_requirement: "Performance benchmark"

    - id: NFR-002
      category: Reliability
      description: "Validator handles all YAML edge cases without crash"
      metric: "Crash count"
      target: "0 crashes"
      test_requirement: "Fuzzing with malformed YAML"
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
| 1 | Empty file | Detect as invalid, offer fresh start | Create empty file |
| 2 | Binary file | Detect as non-text, clear error | Use binary fixture |
| 3 | Very large file (>1MB) | Timeout with warning | Create oversized file |
| 4 | Valid YAML but wrong file type (story file) | Detect type mismatch | Use story file as input |
| 5 | Encoding issues (non-UTF8) | Detect encoding error | Create Latin-1 encoded file |

---

## UI Specification

**Not applicable** - Error handling in terminal with AskUserQuestion for fallback.

---

## Definition of Done

### Implementation
- [ ] YAML validation logic implemented
- [ ] Error message templates for all error types
- [ ] Graceful fallback flow implemented
- [ ] Schema validation implemented
- [ ] Error mapping from parser to user messages

### Quality
- [ ] All acceptance criteria verified with tests
- [ ] Code follows coding-standards.md patterns
- [ ] No CRITICAL or HIGH anti-pattern violations

### Testing
- [ ] Unit tests for BrainstormValidator
- [ ] Unit tests for YAMLErrorMapper
- [ ] Unit tests for each error type
- [ ] Integration test for fallback flow
- [ ] Edge case tests
- [ ] Coverage meets thresholds (95%/85%/80%)

### Documentation
- [ ] Validation errors documented
- [ ] Recovery steps documented

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
**Epic Reference:** EPIC-029 Feature 5: YAML-Malformed Brainstorm Detection
