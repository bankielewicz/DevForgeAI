---
id: STORY-098
title: Headless Mode Answer Configuration
epic: EPIC-010
sprint: Sprint-6
status: Backlog
points: 5
priority: Medium
assigned_to: TBD
created: 2025-11-25
format_version: "2.1"
depends_on: ["STORY-097"]
deferred_to_phase: 2
---

# Story: Headless Mode Answer Configuration

## Description

**As a** DevForgeAI framework user running CI/CD pipelines,
**I want** a configuration system for providing pre-defined answers to AskUserQuestion prompts,
**so that** /dev and /qa can run unattended in headless mode without interactive input.

**Context:** This is Feature 8 of EPIC-010 (Parallel Story Development). **DEFERRED TO PHASE 2** - Required for GitHub Actions integration (STORY-097).

## Acceptance Criteria

### AC#1: CI Answers Configuration File

**Given** `.devforgeai/config/ci-answers.yaml` exists
**When** Claude Code runs in headless mode (`-p` flag)
**Then** reads pre-defined answers from configuration
**And** uses them to respond to AskUserQuestion prompts automatically

---

### AC#2: Answer Matching Logic

**Given** AskUserQuestion prompt with specific text pattern
**When** matching answer exists in ci-answers.yaml
**Then** automatically selects the matching answer
**And** logs: "CI Mode: Selected '{answer}' for prompt '{pattern}'"

---

### AC#3: Fail-on-Unanswered Mode

**Given** headless mode is active
**And** AskUserQuestion has no matching pre-defined answer
**When** fail_on_unanswered: true in configuration
**Then** execution fails immediately
**And** displays: "Headless mode: No answer configured for prompt '{text}'"
**And** includes prompt text for debugging

---

### AC#4: Default Answer Fallback

**Given** headless mode is active
**And** AskUserQuestion has no specific match
**When** default_answer is configured for that question type
**Then** uses default answer
**And** logs warning: "Using default answer for unmatched prompt"

---

### AC#5: Answer Validation on Load

**Given** ci-answers.yaml is loaded
**When** configuration is parsed
**Then** validates all answer values are valid options
**And** warns about potentially outdated answers
**And** fails if answer references non-existent option

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "ci-answers.yaml"
      file_path: "src/devforgeai/config/ci-answers.yaml.example"
      purpose: "Pre-defined answers for headless mode"
      required_keys:
        - key: "headless_mode.enabled"
          type: "boolean"
          default: "true"
        - key: "headless_mode.fail_on_unanswered"
          type: "boolean"
          default: "true"
        - key: "answers"
          type: "object"
          description: "Map of prompt patterns to answer values"

    - type: "Service"
      name: "HeadlessAnswerResolver"
      file_path: "src/claude/skills/devforgeai-development/references/headless-answer-resolver.md"
      requirements:
        - id: "SVC-001"
          description: "Load and parse ci-answers.yaml"
          testable: true
          test_requirement: "Test: Valid YAML loads without error"
          priority: "Critical"
        - id: "SVC-002"
          description: "Match AskUserQuestion prompt to configured answer"
          testable: true
          test_requirement: "Test: Pattern 'priority' matches priority_default"
          priority: "Critical"
        - id: "SVC-003"
          description: "Handle unmatched prompts per fail_on_unanswered setting"
          testable: true
          test_requirement: "Test: Unmatched prompt with fail=true throws error"
          priority: "Critical"

  business_rules:
    - id: "BR-001"
      rule: "Headless mode answers must be pre-validated"
      trigger: "Configuration load"
      validation: "All answers must be valid option labels"
      test_requirement: "Test: Invalid answer value rejected"
      priority: "Critical"
    - id: "BR-002"
      rule: "Interactive mode ignores ci-answers.yaml"
      trigger: "Normal /dev execution"
      validation: "Check for -p flag before using headless answers"
      test_requirement: "Test: Interactive mode still shows prompts"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Answer resolution time"
      metric: "< 10ms per prompt lookup"
      test_requirement: "Test: Time prompt matching"
      priority: "Medium"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Configuration validation"
      metric: "All invalid configs detected before execution starts"
      test_requirement: "Test: Malformed YAML fails at load time"
      priority: "High"
```

---

## Configuration File Format

```yaml
# .devforgeai/config/ci-answers.yaml
headless_mode:
  enabled: true
  fail_on_unanswered: true

answers:
  # Story creation prompts
  epic_association:
    pattern: "Which epic does this story belong to"
    answer: "None - standalone story"

  sprint_assignment:
    pattern: "Which sprint should this story be assigned to"
    answer: "Backlog"

  priority:
    pattern: "What is the story priority"
    answer: "High"

  story_points:
    pattern: "Estimate story complexity"
    answer: "5"

  # Development prompts
  test_failure_action:
    pattern: "Tests failed. How should we proceed"
    answer: "Fix implementation"

  deferral_approval:
    pattern: "Do you approve this deferral"
    answer: "No - implement now"

  # QA prompts
  qa_mode:
    pattern: "Which QA mode"
    answer: "deep"

  # Overlap prompts
  overlap_proceed:
    pattern: "Proceed with parallel development"
    answer: "Yes"

defaults:
  unknown_prompt: "fail"  # fail | first_option | ask_user
```

---

## Non-Functional Requirements

### Performance
- Config load: < 100ms
- Prompt matching: < 10ms
- No impact on interactive mode

### Reliability
- Fail-fast on invalid configuration
- Clear error messages for debugging
- Backward compatible (config optional)

### Security
- Config file permissions: 600
- No sensitive data in answers

---

## Edge Cases

1. **ci-answers.yaml missing:** Fall back to interactive mode
2. **Malformed YAML:** Fail at load with line number
3. **Pattern matches multiple prompts:** First match wins
4. **Answer is multiSelect:** Support array of answers

---

## Dependencies

### Prerequisite Stories
- [ ] **STORY-097:** GitHub Actions Workflow Templates

---

## Definition of Done

### Implementation
- [ ] ci-answers.yaml.example template created
- [ ] HeadlessAnswerResolver service implemented
- [ ] Pattern matching logic
- [ ] Fail-on-unanswered mode
- [ ] Default answer fallback
- [ ] Validation on load

### Quality
- [ ] All 5 acceptance criteria pass
- [ ] Edge cases handled
- [ ] No impact on interactive mode

### Testing
- [ ] Unit tests for pattern matching
- [ ] Unit tests for validation
- [ ] Integration tests with headless mode

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

---

## Notes

**Deferral Justification:** Per EPIC-010 discovery, "defer headless to Phase 2." Local parallel doesn't require this complexity. This story is only needed for GitHub Actions CI/CD integration.

---

**Story Template Version:** 2.1
**Created:** 2025-11-25

## Implementation Notes

No implementation yet - story in planning/backlog phase.
