# Story Format Template

**Version**: 1.0
**Parent Agent**: requirements-analyst

This reference contains the complete story format template used by the requirements-analyst subagent when generating user stories.

---

## Complete Story Template

```markdown
# STORY-XXX: [Story Title]

**Status**: Backlog
**Priority**: [High/Medium/Low]
**Story Points**: [1-5]
**Epic**: [EPIC-XXX]
**Sprint**: [SPRINT-XX] (optional)

## User Story

As a [specific user role],
I want [specific feature or capability],
So that [specific business value or benefit].

## Acceptance Criteria

### Scenario 1: [Happy Path Description]
- Given [initial context or precondition]
- When [specific action or event]
- Then [expected outcome or result]

### Scenario 2: [Edge Case Description]
- Given [initial context]
- When [action]
- Then [outcome]

### Scenario 3: [Error Handling Description]
- Given [initial context]
- When [invalid action or error condition]
- Then [error handling outcome]

## Technical Specification

### API Contract

**Endpoint**: `POST /api/resource`

**Request**:
```json
{
  "field1": "string",
  "field2": 123
}
```

**Response (Success - 200)**:
```json
{
  "id": "uuid",
  "field1": "string",
  "created_at": "ISO8601"
}
```

**Response (Error - 400)**:
```json
{
  "error": "Validation failed",
  "details": ["field1 is required"]
}
```

### Data Model

**Entity**: ResourceEntity

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| id | UUID | Yes | Auto-generated |
| field1 | String | Yes | 1-100 chars |
| field2 | Integer | Yes | > 0 |
| created_at | DateTime | Yes | Auto-generated |

### Business Rules

1. Field1 must be unique per user
2. Field2 must be greater than zero
3. Resource creation triggers notification
4. Maximum 100 resources per user

### Non-Functional Requirements

**Performance**:
- API response time < 200ms (95th percentile)
- Supports 1000 concurrent requests

**Security**:
- Requires authentication (JWT token)
- Input validation on all fields
- SQL injection prevention (parameterized queries)

**Scalability**:
- Horizontal scaling supported
- Database connection pooling
- Cache frequently accessed resources

## Dependencies

- STORY-XXX must be completed first (hard dependency)
- STORY-YYY should be completed (soft dependency)

## Definition of Done

- [ ] Code implemented and passes all tests
- [ ] All acceptance criteria validated
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] QA validation passed

## Implementation Notes

<!-- This section will be filled in by implementing-stories skill during implementation -->
<!-- Developer will document: DoD status, implementation decisions, files created, test results, AC verification -->

*To be completed during development*
```
