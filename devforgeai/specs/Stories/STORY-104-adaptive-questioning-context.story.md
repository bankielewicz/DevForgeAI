---
id: STORY-104
title: Implement Adaptive Questioning Based on Context
epic: EPIC-006
feature: "6.3"
status: Backlog
priority: Medium
points: 8
sprint: Backlog
created: 2025-12-18
created-by: /create-missing-stories
depends-on: STORY-103
---

# STORY-104: Implement Adaptive Questioning Based on Context

## User Story

**As a** user who just completed a DevForgeAI operation,
**I want** feedback questions that reference my specific todos and errors,
**So that** my retrospective feedback is contextual and actionable rather than generic.

## Background

With STORY-103 providing operation context extraction, this story implements the adaptive questioning logic that tailors feedback questions based on the extracted context.

## Acceptance Criteria

### AC1: Context-Aware Question Templates
- [ ] Questions adapt based on operation type (dev, qa, release)
- [ ] Questions reference specific todos that took longest
- [ ] Questions ask about specific errors when operation failed
- [ ] Questions reference phase durations for multi-phase operations

### AC2: Template Pre-Population
- [ ] Feedback template metadata includes operation context
- [ ] Operation type, duration, status, todo count pre-filled
- [ ] Error message included when present
- [ ] Longest-running phase identified and referenced

### AC3: Adaptive Question Selection
- [ ] Success operations: Ask about process improvements
- [ ] Failed operations: Ask about the specific failure
- [ ] Partial operations: Ask about what succeeded and what blocked
- [ ] Long operations (>10 min): Ask about time expectations

### AC4: Context Availability in Prompts
- [ ] AskUserQuestion prompts can reference context variables
- [ ] Context passed to devforgeai-feedback skill
- [ ] Variables: `{operation_type}`, `{duration}`, `{error_message}`, `{todo_count}`

### AC5: Graceful Fallback
- [ ] Generic questions used when context unavailable
- [ ] No errors when context is partial
- [ ] Logs which context fields were available

## Technical Specification

### Implementation Location
- File: `.claude/skills/devforgeai-feedback/adaptive_questions.py`
- Functions: `select_questions()`, `populate_template()`, `format_question()`

### Question Templates by Scenario
```python
QUESTIONS = {
    "success": [
        "The {operation_type} operation completed successfully in {duration}. What went well?",
        "You completed {todo_count} tasks. Any process improvements for next time?"
    ],
    "failure": [
        "The operation failed with: {error_message}. What caused this?",
        "What would have prevented this failure?"
    ],
    "long_running": [
        "This {operation_type} took {duration} - was this expected?",
        "Which phase took longer than expected?"
    ]
}
```

### Integration
- Receives `OperationContext` from STORY-103
- Returns list of formatted question strings
- Called by devforgeai-feedback skill before conversation

## Definition of Done

- [ ] All acceptance criteria verified
- [ ] Unit tests for each question scenario
- [ ] Integration test with real context data
- [ ] Template variable substitution tested
- [ ] Fallback to generic questions verified
- [ ] Code review approved

## Test Cases

1. **Success Context**: Verify success-specific questions selected
2. **Failure Context**: Verify error message appears in questions
3. **Long Running**: Verify duration-based questions for >10 min operations
4. **No Context**: Verify graceful fallback to generic questions
5. **Partial Context**: Verify questions adapt to available fields

## Notes

- Depends on STORY-103 for context extraction
- Questions should feel natural, not templated
- Keep question count manageable (5-7 per session)
