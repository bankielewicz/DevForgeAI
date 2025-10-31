---
id: STORY-XXX
title: [Story Title - What is being built]
epic: EPIC-XXX
sprint: SPRINT-XXX
status: Backlog
points: [Story points: 1, 2, 3, 5, 8, 13]
priority: [High / Medium / Low]
assigned_to: [Developer Name]
created: YYYY-MM-DD
---

# Story: [Title]

## Description

**As a** [user role/persona],
**I want** [capability/feature],
**so that** [business value/benefit].

**Example:**
As a returning customer, I want to use my saved payment method during checkout, so that I can complete purchases faster without re-entering card details.

## Acceptance Criteria

Define testable, specific conditions that must be met for story completion. Use Given/When/Then format for clarity.

### 1. [ ] [Criterion 1 Title]

**Given** [initial context/state],
**When** [action/event occurs],
**Then** [expected outcome].

**Example:**
- **Given** a returning user with saved payment method
- **When** the user reaches payment step in checkout
- **Then** saved payment method is displayed and selectable

---

### 2. [ ] [Criterion 2 Title]

**Given** [initial context/state],
**When** [action/event occurs],
**Then** [expected outcome].

---

### 3. [ ] [Criterion 3 Title]

**Given** [initial context/state],
**When** [action/event occurs],
**Then** [expected outcome].

---

### 4. [ ] [Criterion 4 Title]

**Given** [initial context/state],
**When** [action/event occurs],
**Then** [expected outcome].

---

*Add more criteria as needed (typically 3-7 per story)*

## Technical Specification

### API Endpoints

Define all API endpoints created or modified by this story.

#### Endpoint 1: [Method] [Path]

**POST** `/api/[resource]/[action]`

**Description:** [What this endpoint does]

**Authentication:** [Required / Optional / None]

**Request:**
```json
{
  "field1": "type (string)",
  "field2": "type (number)",
  "field3": {
    "nestedField": "type"
  }
}
```

**Request Validation:**
- `field1`: Required, max length 100, valid email format
- `field2`: Required, min 0, max 999999
- `field3.nestedField`: Optional, enum [value1, value2, value3]

**Response (200 OK):**
```json
{
  "id": "uuid",
  "field1": "string",
  "field2": "number",
  "createdAt": "ISO8601 timestamp"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "ValidationError",
  "message": "Validation failed",
  "details": {
    "field1": "Invalid email format",
    "field2": "Value must be between 0 and 999999"
  }
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Unauthorized",
  "message": "Authentication required"
}
```

**Response (500 Internal Server Error):**
```json
{
  "error": "InternalServerError",
  "message": "An unexpected error occurred",
  "requestId": "uuid"
}
```

---

#### Endpoint 2: [Method] [Path]

**GET** `/api/[resource]/{id}`

**Description:** [What this endpoint does]

**Path Parameters:**
- `id`: [Type, description]

**Query Parameters:**
- `param1`: [Optional/Required, type, description]
- `param2`: [Optional/Required, type, description]

**Response (200 OK):**
```json
{
  "id": "uuid",
  "data": { }
}
```

**Response (404 Not Found):**
```json
{
  "error": "NotFound",
  "message": "Resource not found"
}
```

---

### Data Models

Define all data models (database entities, DTOs, domain objects).

#### Model 1: [EntityName]

**Type:** [Entity / DTO / Domain Object / Value Object]

**Purpose:** [What this model represents]

**C# Example:**
```csharp
public class EntityName
{
    public Guid Id { get; set; }
    public string Field1 { get; set; }  // Required, max 100 chars
    public int Field2 { get; set; }     // Required, min 0
    public DateTime CreatedAt { get; set; }  // Auto-generated
    public DateTime? UpdatedAt { get; set; }  // Nullable, auto-updated

    // Navigation properties
    public List<RelatedEntity> RelatedItems { get; set; }
}
```

**Database Table:** `[TableName]`

**Indexes:**
- Primary Key: `Id` (clustered)
- Unique Index: `Field1` (non-clustered)
- Index: `CreatedAt` (non-clustered)

**Relationships:**
- One-to-Many: `EntityName` → `RelatedEntity` (via foreign key `EntityNameId`)

---

#### Model 2: [RequestDTO]

**Type:** DTO (Request)

**Purpose:** [What this DTO represents]

```csharp
public class RequestDTO
{
    [Required]
    [MaxLength(100)]
    [EmailAddress]
    public string Email { get; set; }

    [Required]
    [Range(0, 999999)]
    public int Amount { get; set; }
}
```

---

### Business Rules

Define domain logic and business constraints.

#### Rule 1: [Rule Name]

**Description:** [What the rule enforces]

**Logic:**
- IF [condition]
- THEN [action]
- ELSE [alternative action]

**Example:**
- IF user has saved payment method AND it's not expired
- THEN allow selection of saved payment method
- ELSE prompt for new payment method

---

#### Rule 2: [Rule Name]

**Description:** [What the rule enforces]

**Validation:**
- [Constraint 1]
- [Constraint 2]

**Error Handling:**
- IF rule violated: Return [error type] with message "[error message]"

---

### Database Changes

#### Migrations

**Migration 1: Add[TableName]Table**

**SQL (up migration):**
```sql
CREATE TABLE [dbo].[TableName]
(
    [Id] UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    [Field1] NVARCHAR(100) NOT NULL,
    [Field2] INT NOT NULL,
    [CreatedAt] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    [UpdatedAt] DATETIME2 NULL
);

CREATE UNIQUE INDEX IX_TableName_Field1 ON [TableName]([Field1]);
CREATE INDEX IX_TableName_CreatedAt ON [TableName]([CreatedAt]);
```

**SQL (down migration):**
```sql
DROP INDEX IX_TableName_CreatedAt ON [TableName];
DROP INDEX IX_TableName_Field1 ON [TableName];
DROP TABLE [dbo].[TableName];
```

---

**Migration 2: AlterExistingTable**

**SQL (up migration):**
```sql
ALTER TABLE [dbo].[ExistingTable]
ADD [NewColumn] NVARCHAR(50) NULL;
```

**SQL (down migration):**
```sql
ALTER TABLE [dbo].[ExistingTable]
DROP COLUMN [NewColumn];
```

---

### Architecture

#### Layer Assignment

Based on source-tree.md:

- **Domain Layer:** `src/Domain/Entities/[EntityName].cs`
- **Application Layer:** `src/Application/Services/[ServiceName].cs`
- **Infrastructure Layer:** `src/Infrastructure/Repositories/[RepositoryName].cs`
- **API Layer:** `src/API/Controllers/[ControllerName].cs`

#### Components Created/Modified

**New Components:**
- `[ComponentName]` - [Purpose]

**Modified Components:**
- `[ComponentName]` - [What changes]

#### Design Patterns

- **Pattern 1:** [Pattern name] - [Where used and why]
- **Pattern 2:** [Pattern name] - [Where used and why]

**Example:**
- **Repository Pattern:** Used for data access abstraction in `[RepositoryName]`
- **Result Pattern:** Used for error handling in business logic (per coding-standards.md)

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- **API Endpoint 1:** < [X]ms (p95), < [X]ms (p99)
- **API Endpoint 2:** < [X]ms (p95), < [X]ms (p99)

**Throughput:**
- Support [X] requests per second
- Support [X] concurrent users

**Performance Test:**
- Load test with [X] concurrent users
- Verify response time under load
- Verify no memory leaks over [X] hour run

---

### Security

**Authentication:**
- [Required / Optional / None]
- [Auth method: OAuth 2.0, JWT, API Key, etc.]

**Authorization:**
- [Role-based / Permission-based / None]
- Required roles: [Roles that can access this feature]

**Data Protection:**
- Sensitive fields: [List fields requiring encryption/masking]
- Encryption: [At rest / In transit / Both]
- PII handling: [GDPR/CCPA compliance requirements]

**Security Testing:**
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] No hardcoded secrets
- [ ] Proper input validation
- [ ] Proper output encoding
- [ ] Authentication enforced
- [ ] Authorization enforced

**Rate Limiting:**
- [X] requests per [time period] per [IP / user / API key]

---

### Scalability

**Horizontal Scaling:**
- Stateless design: [Yes / No]
- Load balancing: [Required / Not Required]

**Database:**
- Expected data volume: [X] records per [time period]
- Growth rate: [X]% per [time period]
- Indexing strategy: [Described above in Data Models]

**Caching:**
- Cache strategy: [None / Redis / In-Memory]
- Cache TTL: [X] seconds/minutes
- Cache invalidation: [Strategy]

---

### Reliability

**Error Handling:**
- Follow Result Pattern (per coding-standards.md)
- Log all errors with context
- Return user-friendly error messages (no stack traces)

**Retry Logic:**
- Retry transient failures: [Yes / No]
- Max retries: [X]
- Backoff strategy: [Exponential / Linear / Fixed]

**Monitoring:**
- Metrics to track: [List key metrics]
- Alerts: [When to alert, who receives alerts]

---

### Observability

**Logging:**
- Log level: [INFO / DEBUG / WARN / ERROR]
- Log structured data (JSON format)
- Include correlation ID for request tracing
- Do NOT log sensitive data (passwords, tokens, PII)

**Metrics:**
- Request count
- Response time (p50, p95, p99)
- Error rate
- [Custom metric 1]
- [Custom metric 2]

**Tracing:**
- Distributed tracing: [Yes / No]
- Trace all external calls

---

## Dependencies

### Prerequisite Stories

Stories that must complete BEFORE this story can start:

- [ ] **STORY-XXX:** [Story title]
  - **Why:** [Explanation of dependency]
  - **Status:** [Not Started / In Progress / Complete]

- [ ] **STORY-YYY:** [Story title]
  - **Why:** [Explanation of dependency]
  - **Status:** [Not Started / In Progress / Complete]

### External Dependencies

Dependencies outside the team's control:

- [ ] **External Dependency 1:** [Description]
  - **Owner:** [Team/Vendor]
  - **ETA:** [Date]
  - **Status:** [On Track / At Risk / Blocked]
  - **Impact if delayed:** [Description]

- [ ] **External Dependency 2:** [Description]
  - **Owner:** [Team/Vendor]
  - **ETA:** [Date]
  - **Status:** [On Track / At Risk / Blocked]

### Technology Dependencies

New packages or versions required:

- [ ] **Package 1:** [Name] v[Version]
  - **Purpose:** [Why needed]
  - **Approved:** [Yes / Pending]
  - **Added to dependencies.md:** [Yes / No]

- [ ] **Package 2:** [Name] v[Version]
  - **Purpose:** [Why needed]
  - **Approved:** [Yes / Pending]

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:** [Description of normal flow]
2. **Edge Cases:**
   - [Edge case 1]
   - [Edge case 2]
   - [Edge case 3]
3. **Error Cases:**
   - [Error case 1: null input]
   - [Error case 2: invalid input]
   - [Error case 3: business rule violation]

**Example Test Structure:**
```csharp
public class ServiceNameTests
{
    [Fact]
    public void MethodName_ValidInput_ReturnsExpectedResult()
    {
        // Arrange
        var sut = new ServiceName();
        var input = CreateValidInput();

        // Act
        var result = sut.MethodName(input);

        // Assert
        Assert.True(result.IsSuccess);
        Assert.Equal(expectedValue, result.Value);
    }

    [Fact]
    public void MethodName_NullInput_ReturnsError()
    {
        // Arrange
        var sut = new ServiceName();

        // Act
        var result = sut.MethodName(null);

        // Assert
        Assert.False(result.IsSuccess);
        Assert.Equal("Input cannot be null", result.Error);
    }
}
```

---

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**
1. **End-to-End API Flow:** [Description]
2. **Database Integration:** [Description]
3. **External Service Integration:** [Description]

**Example Test:**
```csharp
[Fact]
public async Task PostEndpoint_ValidRequest_CreatesResource()
{
    // Arrange
    var client = _factory.CreateClient();
    var request = new RequestDTO { /* ... */ };

    // Act
    var response = await client.PostAsJsonAsync("/api/endpoint", request);

    // Assert
    response.EnsureSuccessStatusCode();
    var result = await response.Content.ReadFromJsonAsync<ResponseDTO>();
    Assert.NotNull(result.Id);
}
```

---

### E2E Tests (If Applicable)

**Coverage Target:** 10% of total tests (critical paths only)

**Test Scenarios:**
1. **Critical User Journey:** [Description]

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

[Additional context, design decisions, clarifications, or open questions]

**Design Decisions:**
- [Decision 1 and rationale]
- [Decision 2 and rationale]

**Open Questions:**
- [ ] [Question 1] - **Owner:** [Name] - **Due:** [Date]
- [ ] [Question 2] - **Owner:** [Name] - **Due:** [Date]

**Related ADRs:**
- [ADR-XXX: [Title]](../ADRs/ADR-XXX.md)

**References:**
- [External documentation link]
- [Design mockup link]
- [Related ticket/issue]

---

**Story Template Version:** 1.0
**Last Updated:** 2025-10-30
