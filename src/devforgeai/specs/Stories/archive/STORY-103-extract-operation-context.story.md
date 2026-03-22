---
id: STORY-103
title: Implement extractOperationContext() Pattern
epic: EPIC-006
feature: "6.3"
status: QA Approved ✅
priority: Medium
points: 13
sprint: Backlog
created: 2025-12-18
created-by: /create-missing-stories
format_version: "2.2"
---

# STORY-103: Implement extractOperationContext() Pattern

## User Story

**As a** framework maintainer,
**I want** a documented pattern for extracting operation context from TodoWrite (todos, errors, timing),
**So that** feedback conversations can be pre-populated with rich, specific context instead of generic questions.

## Background

STORY-019 (Operation Lifecycle Integration) has complete specification but incomplete implementation. This story implements the core `extractOperationContext()` pattern as documentation that Claude follows during feedback skill execution.

## Acceptance Criteria

### AC1: Context Extraction Pattern Documentation

- [x] `references/context-extraction.md` created in `.claude/skills/devforgeai-feedback/`
- [x] Documents pattern for extracting todos (content, status, execution time)
- [x] Documents pattern for extracting overall operation status (success/failure/partial)
- [x] Documents pattern for extracting execution timing (start, end, duration)
- [x] Documents pattern for extracting error context when present (message, failed todo)

### AC2: Context Sanitization Pattern

- [x] `references/context-sanitization.md` documents sanitization approach
- [x] Documents removal of environment variables containing KEY, SECRET, TOKEN, PASSWORD
- [x] Documents removal of file paths containing credentials
- [x] Documents removal of PII patterns (email, phone, SSN)
- [x] Documents logging of sanitization actions for debugging

### AC3: Performance Requirements Documentation

- [x] Context extraction pattern targets <200ms completion
- [x] Context size cap documented (50KB maximum)
- [x] Summarization pattern for >100 todos documented (first 50 + last 10 + summary)
- [x] Stack trace truncation pattern for >5KB documented

### AC4: Graceful Degradation Pattern

- [x] Documents returning partial context if some data unavailable
- [x] Documents warning (not error) logging for missing TodoWrite data
- [x] Documents never throwing exceptions to caller
- [x] Documents returning empty context dict if extraction completely fails

### AC5: Data Model Documentation

- [x] `OperationContext` data model documented with fields:
  - `operation_id: str`
  - `operation_type: str` (dev, qa, release, etc.)
  - `story_id: Optional[str]`
  - `start_time: datetime`
  - `end_time: datetime`
  - `duration_seconds: float`
  - `status: str` (success, failure, partial)
  - `todos: List[TodoContext]`
  - `error: Optional[ErrorContext]`
  - `phases: List[str]`

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "Context Extraction Pattern Documentation"
      file_path: ".claude/skills/devforgeai-feedback/references/context-extraction.md"
      purpose: "Documents pattern for extracting operation context during feedback"
      required_sections:
        - section: "Context Extraction Pattern"
          description: "Step-by-step pattern for extracting TodoWrite state"
          test_requirement: "Test: Pattern produces valid context structure"
        - section: "TodoContext Extraction"
          description: "How to extract todo content, status, timing"
          test_requirement: "Test: Pattern extracts all todo fields"
        - section: "ErrorContext Extraction"
          description: "How to extract error details when operation failed"
          test_requirement: "Test: Pattern extracts error message and failed todo"
        - section: "Timing Calculation"
          description: "How to calculate start, end, duration"
          test_requirement: "Test: Pattern produces accurate timing"

    - type: "Configuration"
      name: "Context Sanitization Pattern Documentation"
      file_path: ".claude/skills/devforgeai-feedback/references/context-sanitization.md"
      purpose: "Documents pattern for removing secrets from context"
      required_sections:
        - section: "Sanitization Patterns"
          description: "Regex patterns for identifying secrets"
          test_requirement: "Test: Patterns match common secret formats"
        - section: "PII Removal"
          description: "Patterns for removing email, phone, SSN"
          test_requirement: "Test: Patterns identify PII correctly"
        - section: "Logging Sanitization"
          description: "How to log sanitization for debugging"
          test_requirement: "Test: Sanitization logged without exposing secrets"

    - type: "DataModel"
      name: "OperationContext"
      table: "N/A (documented pattern, in-memory during execution)"
      purpose: "Represents extracted operation context for feedback"
      fields:
        - name: "operation_id"
          type: "String"
          constraints: "Required, UUID format"
          description: "Unique identifier for this operation"
          test_requirement: "Test: operation_id is valid UUID"
        - name: "operation_type"
          type: "String"
          constraints: "Required, Enum(dev, qa, release, orchestrate)"
          description: "Type of DevForgeAI operation"
          test_requirement: "Test: operation_type matches valid enum"
        - name: "story_id"
          type: "String"
          constraints: "Optional, STORY-NNN format"
          description: "Associated story if applicable"
          test_requirement: "Test: story_id matches expected format"
        - name: "start_time"
          type: "DateTime"
          constraints: "Required, ISO 8601"
          description: "When operation started"
          test_requirement: "Test: start_time is valid datetime"
        - name: "end_time"
          type: "DateTime"
          constraints: "Required, ISO 8601"
          description: "When operation ended"
          test_requirement: "Test: end_time >= start_time"
        - name: "duration_seconds"
          type: "Float"
          constraints: "Required, >= 0"
          description: "Total operation duration"
          test_requirement: "Test: duration_seconds = end_time - start_time"
        - name: "status"
          type: "String"
          constraints: "Required, Enum(success, failure, partial)"
          description: "Operation outcome"
          test_requirement: "Test: status matches valid enum"
        - name: "todos"
          type: "List[TodoContext]"
          constraints: "Required, may be empty"
          description: "Extracted todo items"
          test_requirement: "Test: todos list populated from TodoWrite"
        - name: "error"
          type: "ErrorContext"
          constraints: "Optional, present when status=failure"
          description: "Error details if operation failed"
          test_requirement: "Test: error present only when status=failure"
        - name: "phases"
          type: "List[String]"
          constraints: "Required, may be empty"
          description: "List of completed phases"
          test_requirement: "Test: phases list populated"

  business_rules:
    - id: "BR-001"
      rule: "Context extraction must complete within 200ms"
      trigger: "Before feedback conversation starts"
      validation: "Time extraction, log if exceeds target"
      error_handling: "Return partial context if timeout"
      test_requirement: "Test: Extraction completes in <200ms"
      priority: "High"
    - id: "BR-002"
      rule: "Context size must not exceed 50KB"
      trigger: "After extraction, before return"
      validation: "Measure serialized size"
      error_handling: "Truncate and summarize if over limit"
      test_requirement: "Test: Context <= 50KB"
      priority: "High"
    - id: "BR-003"
      rule: "Secrets must never appear in context"
      trigger: "Before returning context"
      validation: "Run sanitization patterns"
      error_handling: "Redact matching content"
      test_requirement: "Test: No secrets in output"
      priority: "Critical"
    - id: "BR-004"
      rule: "Extraction failures must not break feedback"
      trigger: "Any extraction error"
      validation: "Catch all exceptions"
      error_handling: "Return empty context, log warning"
      test_requirement: "Test: Failure returns empty dict"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Context extraction completes in <200ms"
      metric: "< 200ms extraction time"
      test_requirement: "Test: Benchmark extraction time"
      priority: "High"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Never blocks feedback conversation"
      metric: "0% blocking failures"
      test_requirement: "Test: Failure returns gracefully"
      priority: "Critical"
    - id: "NFR-003"
      category: "Security"
      requirement: "Zero secrets in extracted context"
      metric: "0 secret patterns in output"
      test_requirement: "Test: Sanitization removes all secrets"
      priority: "Critical"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Context extraction: < 200ms

**Size Limits:**
- Maximum context size: 50KB
- Summarization threshold: > 100 todos

---

### Security

**Data Protection:**
- Remove environment variables containing KEY, SECRET, TOKEN, PASSWORD
- Remove file paths containing credentials
- Remove PII patterns (email, phone, SSN)
- Log sanitization actions (without exposing secrets)

---

### Reliability

**Error Handling:**
- Return partial context if some data unavailable
- Log warning (not error) for missing data
- Never throw exceptions to caller
- Return empty context dict if completely fails

---

## Dependencies

### Prerequisite Stories

None - this is a foundation story for EPIC-006 Feature 6.3.

### Technology Dependencies

- [ ] **TodoWrite tool** (Claude Code built-in)
  - **Purpose:** Source of operation state
  - **Approved:** Yes (built-in)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for documented patterns

**Test Scenarios:**
1. **Happy Path**: Extract context from completed /dev operation with 5 todos
2. **Error Context**: Extract context from failed /qa operation with error details
3. **Large Operation**: Extract context from operation with 150 todos (verify summarization)
4. **Sanitization**: Verify secrets removed from context (API_KEY, passwords)
5. **Performance**: Verify extraction completes in <200ms with 100 todos
6. **Graceful Degradation**: Verify partial context returned when TodoWrite unavailable

---

## Acceptance Criteria Verification Checklist

### AC1: Context Extraction Pattern Documentation

- [x] references/context-extraction.md created - **Phase:** GREEN - **Evidence:** File exists at .claude/skills/devforgeai-feedback/references/context-extraction.md (357 lines)
- [x] Todo extraction pattern documented - **Phase:** GREEN - **Evidence:** Step 2: Extract Todo Items section
- [x] Status extraction pattern documented - **Phase:** GREEN - **Evidence:** Step 3: Determine Operation Status section
- [x] Timing extraction pattern documented - **Phase:** GREEN - **Evidence:** Step 4: Calculate Timing section
- [x] Error extraction pattern documented - **Phase:** GREEN - **Evidence:** Step 5: Extract Error Context section

### AC2: Context Sanitization Pattern

- [x] references/context-sanitization.md created - **Phase:** GREEN - **Evidence:** File exists at .claude/skills/devforgeai-feedback/references/context-sanitization.md (342 lines)
- [x] Secret removal patterns documented - **Phase:** GREEN - **Evidence:** Secret Removal Patterns section with regex
- [x] PII removal patterns documented - **Phase:** GREEN - **Evidence:** PII Removal Patterns section (email, phone, SSN)
- [x] Sanitization logging documented - **Phase:** GREEN - **Evidence:** Logging Sanitization section

### AC3: Performance Requirements Documentation

- [x] 200ms target documented - **Phase:** GREEN - **Evidence:** Performance Requirements > Timing Target section
- [x] 50KB limit documented - **Phase:** GREEN - **Evidence:** Performance Requirements > Size Limit section
- [x] Summarization pattern documented - **Phase:** GREEN - **Evidence:** Performance Requirements > Summarization for Large Operations
- [x] Stack trace truncation documented - **Phase:** GREEN - **Evidence:** Performance Requirements > Stack Trace Truncation

### AC4: Graceful Degradation Pattern

- [x] Partial context return documented - **Phase:** GREEN - **Evidence:** Graceful Degradation > Return Partial Context section
- [x] Warning logging documented - **Phase:** GREEN - **Evidence:** Graceful Degradation > Warning Logging section
- [x] No-exception guarantee documented - **Phase:** GREEN - **Evidence:** Graceful Degradation > No-Exception Guarantee section
- [x] Empty fallback documented - **Phase:** GREEN - **Evidence:** Graceful Degradation > Empty Context Fallback section

### AC5: Data Model Documentation

- [x] OperationContext fields documented - **Phase:** GREEN - **Evidence:** Data Models > OperationContext table (10 fields)
- [x] TodoContext model documented - **Phase:** GREEN - **Evidence:** Data Models > TodoContext table
- [x] ErrorContext model documented - **Phase:** GREEN - **Evidence:** Data Models > ErrorContext table

---

**Checklist Progress:** 20/20 items complete (100%)

---

## Definition of Done

### Implementation
- [x] `references/context-extraction.md` created with extraction patterns
- [x] `references/context-sanitization.md` created with sanitization patterns
- [x] OperationContext data model documented
- [x] Performance requirements documented
- [x] Graceful degradation patterns documented

### Quality
- [x] All 5 acceptance criteria documented
- [x] Test scenarios defined for each pattern
- [x] NFRs met (200ms, 50KB, zero secrets)
- [x] No Python code in framework (documentation only)

### Testing
- [x] Test scenarios for context extraction
- [x] Test scenarios for sanitization
- [x] Test scenarios for performance
- [x] Test scenarios for graceful degradation

### Documentation
- [x] Context extraction pattern fully documented
- [x] Sanitization patterns fully documented
- [x] Data models fully documented

---

## Workflow Status

- [x] Architecture phase complete
- [x] Development phase complete
- [x] QA phase complete
- [ ] Released

## QA Validation History

### Validation: 2025-12-19 (Deep Mode)

**Result:** ✅ **PASSED**

**Coverage Analysis:**
- Acceptance Criteria Traceability: 100% (20/20 requirements)
- Test Coverage: 100% (25/25 tests passing)
- Anti-Pattern Violations: 0 (CRITICAL: 0, HIGH: 0)
- Definition of Done: 100% complete (no deferrals)

**Validation Phases:**
- ✅ Phase 0.9: AC-DoD Traceability (Score 100%)
- ✅ Phase 1: Test Coverage (25/25 tests)
- ✅ Phase 2: Anti-Pattern Detection (0 violations)
- ✅ Phase 3: Spec Compliance (5/5 ACs verified)
- ✅ Phase 4: Code Quality (0 issues)
- ✅ Phase 5: QA Report (Report generated)

**Report:** `devforgeai/qa/reports/STORY-103-qa-report.md`

**Recommendation:** APPROVED FOR RELEASE

---

## Notes

**Design Decisions:**
- **Framework-compliant:** Documentation patterns in references/, no Python code
- Context extraction is critical for Feature 6.3's value proposition
- Must be non-blocking (failures don't prevent feedback)
- Per anti-patterns.md: "Framework must be language-agnostic"

**Pattern Example (Context Extraction):**
```markdown
## Context Extraction Pattern

When extracting operation context for feedback:

1. **Read TodoWrite State**
   - Access internal TodoWrite state
   - Extract all todo items with content, status, timing

2. **Determine Operation Status**
   - Check if all todos completed successfully
   - Status = "success" if all completed
   - Status = "failure" if any failed
   - Status = "partial" if mixed

3. **Calculate Timing**
   - start_time = first todo start
   - end_time = last todo end
   - duration_seconds = end_time - start_time

4. **Extract Error Context (if failure)**
   - Capture error message
   - Identify failed todo
   - Include stack trace (truncated to 5KB)

5. **Sanitize Before Return**
   - Run sanitization patterns
   - Remove secrets, PII
   - Log sanitization actions
```

**References:**
- EPIC-006: Feedback Hook System
- STORY-019: Operation Lifecycle Integration (specification)

---

**Story Template Version:** 2.2
**Last Updated:** 2025-12-18
**Context Compliance:** Verified against tech-stack.md, anti-patterns.md (no Python code)
