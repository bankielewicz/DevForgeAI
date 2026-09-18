## Examples

### Example 1: Database Function Story

**Input:**
```
Feature: Capture SQL Server index characteristics for preservation during maintenance operations
Story ID: STORY-245
Priority: High
Points: 8
```

**Sample Output (abbreviated):**
```markdown
## User Story

**As a** database administrator,
**I want** to capture all index characteristics before rebuild operations,
**so that** performance tuning settings are preserved and data loss prevented.

## Acceptance Criteria

### AC1: Capture standard index properties
**Given** a clustered or non-clustered index exists in the database
**When** fn_GetIndexDefinition() is called with database, schema, table, and index names
**Then** the function returns JSON containing IndexType, FillFactor, IsPadded, IgnoreDupKey, AllowRowLocks, AllowPageLocks, DataCompression, KeyColumns, and IncludedColumns

### AC2: Preserve filtered index predicates
**Given** a filtered index with WHERE clause exists
**When** fn_GetIndexDefinition() is called
**Then** the JSON includes FilterDefinition field with complete WHERE clause

### AC3: Performance requirement
**Given** a database with 1000+ indexes
**When** fn_GetIndexDefinition() is called for any single index
**Then** the function completes in less than 100 milliseconds

## Edge Cases

1. **Columnstore indexes:** No key columns (return NULL for KeyColumns/IncludedColumns)
2. **Partitioned indexes (Enterprise Edition only):** Capture partition scheme details

## Non-Functional Requirements

### Performance
- Response time: < 100ms per call (p95 and p99)
- Batch performance: < 5 seconds for 100 indexes

### Security
- Authentication: Inherits caller's SQL authentication
- Authorization: Requires VIEW DEFINITION permission

### Reliability
- Error handling: Return NULL on errors (no exceptions)

### Scalability
- Stateless function (no session state)
- Scales with sys.indexes row count (tested 10,000+ indexes)
```

### Example 2: API Endpoint Story

**Input:**
```
Feature: Build RESTful API endpoint for user authentication with JWT token support and rate limiting
Story ID: STORY-346
Priority: Critical
Points: 13
```

**Invocation Pattern:**
```python
Task(
    subagent_type="story-requirements-analyst",
    description="Generate requirements content for authentication API endpoint",
    prompt="""
    Generate user story, acceptance criteria, edge cases, and non-functional requirements.

    Feature: Build RESTful API endpoint for user authentication with JWT token support and rate limiting
    Story ID: STORY-346
    Priority: Critical
    Points: 13

    Requirements:
    - POST /api/auth/login endpoint accepting email/password
    - Return JWT token valid for 24 hours
    - Implement rate limiting (5 attempts per 15 minutes)
    - Hash passwords with bcrypt (salt rounds >= 10)
    - Log failed attempts (no passwords in logs)

    Return ONLY markdown content (no file creation).
    """
)
```
