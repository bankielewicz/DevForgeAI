## Output Format

**Primary Output:**
```markdown
## User Story

**As a** [specific persona],
**I want** [clear action],
**so that** [business benefit].

## Acceptance Criteria

### AC1: [Title]
**Given** [initial state]
**When** [trigger action]
**Then** [expected outcome]

### AC2: [Title]
**Given** [initial state]
**When** [trigger action]
**Then** [expected outcome]

### AC3: [Title]
**Given** [initial state]
**When** [trigger action]
**Then** [expected outcome]

## Edge Cases

1. **[Scenario title]:** [Description of edge case and handling]
2. **[Scenario title]:** [Description of edge case and handling]

## Non-Functional Requirements

### Performance
- [Measurable metric, e.g., "< 100ms per call (p95)"]
- [Measurable metric, e.g., "< 5 seconds for batch of 100"]

### Security
- [Specific mechanism, e.g., "QUOTENAME() + parameterized queries"]
- [Specific permission, e.g., "VIEW DEFINITION required"]

### Reliability
- [Specific error handling, e.g., "Return NULL on errors"]
- [Specific retry policy, e.g., "No retry (idempotent, read-only)"]

### Scalability
- [Specific concurrency limit, e.g., "Support 10,000 concurrent users"]
- [Specific data volume, e.g., "Tested with 50,000 indexes"]
```

**Optional Sections:**
- `## Data Validation Rules` - Input parameter constraints, validation logic
- `## Component Information` - For v2.0 YAML: Service/Worker/API/Repository/DataModel specifications

**Delivery Method:** Return as single markdown string to parent skill (not multiple files)

