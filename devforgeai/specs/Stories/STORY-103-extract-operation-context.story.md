---
id: STORY-103
title: Implement extractOperationContext() Function
epic: EPIC-006
feature: "6.3"
status: Backlog
priority: Medium
points: 13
sprint: Backlog
created: 2025-12-18
created-by: /create-missing-stories
---

# STORY-103: Implement extractOperationContext() Function

## User Story

**As a** framework maintainer,
**I want** a function that extracts operation context from TodoWrite (todos, errors, timing),
**So that** feedback conversations can be pre-populated with rich, specific context instead of generic questions.

## Background

STORY-019 (Operation Lifecycle Integration) has complete specification but incomplete implementation. This story implements the core `extractOperationContext()` function that captures operation state for feedback conversations.

## Acceptance Criteria

### AC1: Context Extraction Function
- [ ] `extractOperationContext()` function implemented in `.claude/skills/devforgeai-feedback/context_extraction.py`
- [ ] Extracts todos (content, status, execution time)
- [ ] Extracts overall operation status (success/failure/partial)
- [ ] Extracts execution timing (start, end, duration)
- [ ] Extracts error context when present (message, failed todo)

### AC2: Context Sanitization
- [ ] `sanitize_context()` function removes secrets from context
- [ ] Removes environment variables containing KEY, SECRET, TOKEN, PASSWORD
- [ ] Removes file paths containing credentials
- [ ] Removes PII patterns (email, phone, SSN)
- [ ] Logs sanitization actions for debugging

### AC3: Performance Requirements
- [ ] Context extraction completes in <200ms
- [ ] Context size capped at 50KB maximum
- [ ] Summarizes if >100 todos (include first 50 + last 10 + summary)
- [ ] Truncates stack traces if >5KB

### AC4: Graceful Degradation
- [ ] Returns partial context if some data unavailable
- [ ] Logs warning (not error) for missing TodoWrite data
- [ ] Never throws exceptions to caller
- [ ] Returns empty context dict if extraction completely fails

### AC5: Data Model
- [ ] `OperationContext` dataclass implemented with fields:
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

### Implementation Location
- File: `.claude/skills/devforgeai-feedback/context_extraction.py`
- Functions: `extract_operation_context()`, `sanitize_context()`, `summarize_todos()`

### Integration Point
- Called by `devforgeai invoke-hooks` before feedback conversation starts
- Returns `OperationContext` instance or empty dict on failure

### Dependencies
- TodoWrite tool state (internal API)
- datetime for timing calculations
- re for sanitization patterns

## Definition of Done

- [ ] All acceptance criteria verified
- [ ] Unit tests with >95% coverage
- [ ] Integration test with mock TodoWrite data
- [ ] Performance benchmark: extraction <200ms
- [ ] Code review approved
- [ ] No secrets in test fixtures

## Test Cases

1. **Happy Path**: Extract context from completed /dev operation with 5 todos
2. **Error Context**: Extract context from failed /qa operation with error details
3. **Large Operation**: Extract context from operation with 150 todos (verify summarization)
4. **Sanitization**: Verify secrets removed from context (API_KEY, passwords)
5. **Performance**: Verify extraction completes in <200ms with 100 todos
6. **Graceful Degradation**: Verify partial context returned when TodoWrite unavailable

## Notes

- This story completes the implementation portion of STORY-019 specification
- Context extraction is critical for Feature 6.3's value proposition
- Must be non-blocking (failures don't prevent feedback)
