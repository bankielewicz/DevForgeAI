---
id: STORY-104
title: Implement Adaptive Questioning Based on Context
epic: EPIC-006
feature: "6.3"
status: QA Approved ✅
priority: Medium
points: 8
sprint: Backlog
created: 2025-12-18
created-by: /create-missing-stories
depends_on:
  - STORY-103
format_version: "2.2"
---

# STORY-104: Implement Adaptive Questioning Based on Context

## User Story

**As a** user who just completed a DevForgeAI operation,
**I want** feedback questions that reference my specific todos and errors,
**So that** my retrospective feedback is contextual and actionable rather than generic.

## Background

With STORY-103 providing operation context extraction patterns, this story implements the adaptive questioning patterns that tailor feedback questions based on the extracted context.

## Acceptance Criteria

### AC1: Context-Aware Question Templates Documentation

- [x] `references/adaptive-questioning.md` created in `.claude/skills/devforgeai-feedback/`
- [x] Documents question templates that adapt based on operation type (dev, qa, release)
- [x] Documents templates that reference specific todos that took longest
- [x] Documents templates that ask about specific errors when operation failed
- [x] Documents templates that reference phase durations for multi-phase operations

### AC2: Template Pre-Population Pattern

- [x] Documents how feedback template metadata includes operation context
- [x] Documents operation type, duration, status, todo count pre-fill pattern
- [x] Documents error message inclusion when present
- [x] Documents longest-running phase identification and referencing

### AC3: Adaptive Question Selection Pattern

- [x] Documents success operations question selection (process improvements)
- [x] Documents failed operations question selection (specific failure focus)
- [x] Documents partial operations question selection (what succeeded/blocked)
- [x] Documents long operations (>10 min) question selection (time expectations)

### AC4: Context Variables in Prompts

- [x] Documents how AskUserQuestion prompts can reference context variables
- [x] Documents context passing to devforgeai-feedback skill
- [x] Documents variables: `{operation_type}`, `{duration}`, `{error_message}`, `{todo_count}`

### AC5: Graceful Fallback Pattern

- [x] Documents generic questions used when context unavailable
- [x] Documents no errors when context is partial
- [x] Documents logging which context fields were available

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "Adaptive Questioning Pattern Documentation"
      file_path: ".claude/skills/devforgeai-feedback/references/adaptive-questioning.md"
      purpose: "Documents patterns for selecting and formatting context-aware questions"
      required_sections:
        - section: "Question Selection Pattern"
          description: "How to select questions based on operation outcome"
          test_requirement: "Test: Correct questions selected for each outcome type"
        - section: "Template Variable Substitution"
          description: "How to substitute context variables in question templates"
          test_requirement: "Test: Variables correctly replaced in questions"
        - section: "Success Questions"
          description: "Question templates for successful operations"
          test_requirement: "Test: Success questions focus on improvements"
        - section: "Failure Questions"
          description: "Question templates for failed operations"
          test_requirement: "Test: Failure questions reference error details"
        - section: "Long Operation Questions"
          description: "Question templates for operations >10 minutes"
          test_requirement: "Test: Long operation questions ask about timing"
        - section: "Graceful Fallback"
          description: "How to handle missing or partial context"
          test_requirement: "Test: Generic questions used when context unavailable"

    - type: "Configuration"
      name: "Question Templates"
      file_path: ".claude/skills/devforgeai-feedback/references/question-templates.md"
      purpose: "Contains the actual question template strings"
      required_sections:
        - section: "Success Templates"
          description: "Templates for successful operation feedback"
          test_requirement: "Test: All success templates have valid variables"
        - section: "Failure Templates"
          description: "Templates for failed operation feedback"
          test_requirement: "Test: All failure templates include error variable"
        - section: "Partial Templates"
          description: "Templates for partially completed operations"
          test_requirement: "Test: Partial templates reference both success and failure"
        - section: "Long Running Templates"
          description: "Templates for operations exceeding time threshold"
          test_requirement: "Test: Long running templates reference duration"
        - section: "Generic Templates"
          description: "Fallback templates when context unavailable"
          test_requirement: "Test: Generic templates work without variables"

  business_rules:
    - id: "BR-001"
      rule: "Questions must reference specific context when available"
      trigger: "Question formatting"
      validation: "Context variables substituted in templates"
      error_handling: "Fall back to generic if variable missing"
      test_requirement: "Test: Questions include context details"
      priority: "High"
    - id: "BR-002"
      rule: "Question count limited to 5-7 per session"
      trigger: "Question selection"
      validation: "Count questions before presenting"
      error_handling: "Prioritize most relevant questions"
      test_requirement: "Test: No more than 7 questions per session"
      priority: "Medium"
    - id: "BR-003"
      rule: "Failure questions must include error context"
      trigger: "Operation status = failure"
      validation: "Error message or failed todo referenced"
      error_handling: "Generic failure question if no error details"
      test_requirement: "Test: Failure questions reference error"
      priority: "High"
    - id: "BR-004"
      rule: "Questions should feel natural, not templated"
      trigger: "Template design"
      validation: "Review for natural language flow"
      error_handling: "Revise awkward templates"
      test_requirement: "Test: Questions read naturally"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Usability"
      requirement: "Questions feel contextual and relevant"
      metric: "User satisfaction with question relevance"
      test_requirement: "Test: Questions reference specific operation details"
      priority: "High"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Question selection completes in <100ms"
      metric: "< 100ms selection time"
      test_requirement: "Test: Benchmark question selection"
      priority: "Medium"
    - id: "NFR-003"
      category: "Reliability"
      requirement: "Graceful fallback when context unavailable"
      metric: "0% failures due to missing context"
      test_requirement: "Test: Generic questions used when context missing"
      priority: "High"
```

---

## Non-Functional Requirements (NFRs)

### Usability

**Question Relevance:**
- Questions feel contextual, not generic
- Questions reference specific operation details
- Questions should feel natural, not templated

### Performance

**Response Time:**
- Question selection: < 100ms

### Reliability

**Fallback:**
- Graceful fallback to generic questions when context unavailable
- No errors when context is partial

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-103:** Implement extractOperationContext() Pattern
  - **Why:** Provides the context data for adaptive questions
  - **Status:** QA Approved

### Technology Dependencies

- [x] **AskUserQuestion tool** (Claude Code built-in)
  - **Purpose:** Present questions to user
  - **Approved:** Yes (built-in)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for documented patterns

**Test Scenarios:**
1. **Success Context**: Verify success-specific questions selected
2. **Failure Context**: Verify error message appears in questions
3. **Long Running**: Verify duration-based questions for >10 min operations
4. **No Context**: Verify graceful fallback to generic questions
5. **Partial Context**: Verify questions adapt to available fields

---

## Acceptance Criteria Verification Checklist

### AC1: Context-Aware Question Templates Documentation

- [x] references/adaptive-questioning.md created - **Phase:** Green - **Evidence:** File exists at `.claude/skills/devforgeai-feedback/references/adaptive-questioning.md` (484 lines)
- [x] Operation type templates documented - **Phase:** Green - **Evidence:** Decision Matrix table with dev/qa/release; Success/Failure Question Templates sections
- [x] Todo-referencing templates documented - **Phase:** Green - **Evidence:** Variables `{todo_count}`, `{completed_count}` in Available Variables table
- [x] Error-referencing templates documented - **Phase:** Green - **Evidence:** Variables `{error_message}`, `{failed_todo}` in Failure Question Templates section
- [x] Phase duration templates documented - **Phase:** Green - **Evidence:** `{longest_phase}` variable and Long-Running Success section

### AC2: Template Pre-Population Pattern

- [x] Context metadata inclusion documented - **Phase:** Green - **Evidence:** "Context Metadata Pre-Population" section with YAML schema
- [x] Pre-fill patterns documented - **Phase:** Green - **Evidence:** "Pre-Fill Pattern" 5-step process documented
- [x] Error message inclusion documented - **Phase:** Green - **Evidence:** ErrorContext fields in metadata; failure templates reference `{error_message}`
- [x] Phase identification documented - **Phase:** Green - **Evidence:** "Longest-Running Phase Identification" section with algorithm

### AC3: Adaptive Question Selection Pattern

- [x] Success question selection documented - **Phase:** Green - **Evidence:** "Success Question Templates" with Standard and Long-Running subcategories
- [x] Failure question selection documented - **Phase:** Green - **Evidence:** "Failure Question Templates" section with 6 question templates
- [x] Partial question selection documented - **Phase:** Green - **Evidence:** "Partial Completion Templates" section with 4 templates
- [x] Long operation question selection documented - **Phase:** Green - **Evidence:** Decision Matrix (>= 600s = success_long_running); Long-Running section

### AC4: Context Variables in Prompts

- [x] AskUserQuestion variable usage documented - **Phase:** Green - **Evidence:** "AskUserQuestion Integration" section with YAML example
- [x] Context passing pattern documented - **Phase:** Green - **Evidence:** "Context Passing to devforgeai-feedback Skill" 5-step pattern
- [x] Variable list documented - **Phase:** Green - **Evidence:** "Available Variables" table with 8 variables

### AC5: Graceful Fallback Pattern

- [x] Generic fallback documented - **Phase:** Green - **Evidence:** "Generic Fallback Templates" section with 4 context-free questions
- [x] Partial context handling documented - **Phase:** Green - **Evidence:** "Graceful Fallback Pattern" section; "No-Error Guarantee" subsection
- [x] Context field logging documented - **Phase:** Green - **Evidence:** "Logging Pattern" subsection with format and example output

---

**Checklist Progress:** 19/19 items complete (100%)

---

## Definition of Done

### Implementation
- [x] `references/adaptive-questioning.md` created
- [x] `references/feedback-question-templates.md` extended with context variable support (deviation: extended existing file per user decision)
- [x] Question selection patterns documented
- [x] Variable substitution patterns documented
- [x] Fallback patterns documented

### Quality
- [x] All 5 acceptance criteria documented
- [x] Questions feel natural, not templated (verified: BR-004 Natural Language Guidelines section)
- [x] Test scenarios defined for each pattern
- [x] No Python code in framework (documentation only)

### Testing
- [x] Test scenarios for question selection (23 tests in test-adaptive-questioning-patterns.sh)
- [x] Test scenarios for variable substitution
- [x] Test scenarios for graceful fallback
- [x] Test scenarios for each operation outcome

### Documentation
- [x] Adaptive questioning patterns fully documented (484 lines)
- [x] Question templates fully documented (context variable section added)
- [x] Integration with context extraction documented

---

## QA Validation History

**Deep Mode Validation (2025-12-19):**
- **Phase 0.9:** AC-DoD Traceability Validation → PASS (100% traceability, all DoD items complete)
- **Phase 1:** Test Coverage Analysis → PASS (23/23 tests passing, 100% functional coverage)
- **Phase 2:** Anti-Pattern Detection → PASS (0 CRITICAL, 0 HIGH, 3 MEDIUM non-blocking)
- **Phase 3:** Spec Compliance → PASS (5/5 ACs verified, no deferrals, 100% traceability)
- **Phase 4:** Code Quality → PASS (documentation-only, no code violations)
- **Phase 5:** QA Report Generated → `devforgeai/qa/reports/STORY-104-qa-report.md`

**Overall Result:** ✅ **QA APPROVED**
- Coverage: 100% (23/23 tests passing)
- Violations: 0 CRITICAL, 0 HIGH
- Traceability: 100% (5/5 ACs → 12/12 DoD items → 23/23 tests)
- Status Change: Dev Complete → QA Approved

---

## Workflow Status

- [x] Architecture phase complete
- [x] Development phase complete
- [x] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- **Framework-compliant:** Documentation patterns in references/, no Python code
- Questions should feel natural, not templated
- Keep question count manageable (5-7 per session)
- Per anti-patterns.md: "Framework must be language-agnostic"

**Question Template Examples:**

```markdown
## Success Templates

- "The {operation_type} operation completed successfully in {duration}. What went well?"
- "You completed {todo_count} tasks. Any process improvements for next time?"
- "All tests passed. Was there anything that surprised you during implementation?"

## Failure Templates

- "The operation failed with: {error_message}. What caused this?"
- "The {failed_todo} task couldn't be completed. What would have prevented this?"
- "What additional information would have helped avoid this failure?"

## Long Running Templates

- "This {operation_type} took {duration} - was this expected?"
- "Which phase took longer than expected?"
- "Would you like to set a time expectation for future {operation_type} operations?"

## Generic Templates (Fallback)

- "How did this operation go?"
- "Any challenges or blockers worth noting?"
- "What would you do differently next time?"
```

**References:**
- EPIC-006: Feedback Hook System
- STORY-103: Context Extraction Pattern (provides context data)

---

**Story Template Version:** 2.2
**Last Updated:** 2025-12-19
**Context Compliance:** Verified against tech-stack.md, anti-patterns.md (no Python code)
**Dev Completed:** 2025-12-19
**Test Results:** 23/23 tests passing (devforgeai/tests/STORY-104/test-adaptive-questioning-patterns.sh)
