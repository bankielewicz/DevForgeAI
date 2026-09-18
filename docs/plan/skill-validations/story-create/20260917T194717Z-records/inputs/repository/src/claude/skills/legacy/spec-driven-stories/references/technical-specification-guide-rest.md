# Technical Specification Guide — REST / HTTP API

Sub-reference for stories with REST/HTTP endpoints. Loaded by Phase 03 Step 3.2.5 when `detect-indicators` identifies REST API needs.

---

## API Contract Templates

### REST API Specification (OpenAPI 3.0 Style)

#### HTTP Methods & Use Cases

**GET** - Retrieve data (safe, idempotent)
- List resources: `GET /api/users`
- Get single resource: `GET /api/users/{id}`
- Search/filter: `GET /api/users?role=admin&status=active`

**POST** - Create new resource (not idempotent)
- Create: `POST /api/users`
- Custom actions: `POST /api/users/{id}/verify-email`

**PUT** - Replace entire resource (idempotent)
- Full update: `PUT /api/users/{id}`
- Requires all fields in request body

**PATCH** - Partial update (idempotent)
- Update specific fields: `PATCH /api/users/{id}`
- Only modified fields in request body

**DELETE** - Remove resource (idempotent)
- Delete: `DELETE /api/users/{id}`
- Soft delete: `DELETE /api/users/{id}?soft=true`

#### Complete Endpoint Documentation Template

```markdown
#### Endpoint: {METHOD} /api/{resource}/{id}

**Description:** {What this endpoint does}

**Authentication:** {Required|Optional|None}
- Method: {Bearer Token|API Key|OAuth2|None}
- Required scopes: {scope1, scope2}

**Request Headers:**
```http
Content-Type: application/json
Authorization: Bearer {token}
X-API-Key: {api_key}
```

**Path Parameters:**
- `id` (UUID, required): {Resource identifier}

**Query Parameters:**
- `param1` (string, optional): {Description, default value}
- `param2` (integer, optional): {Description, range: 1-100}

**Request Body:**
```json
{
  "field1": "string (required, max 100 chars, email format)",
  "field2": 42,
  "field3": true,
  "nested": {
    "subfield": "value"
  }
}
```

**Validation Rules:**
- field1: Required, email format, unique in database
- field2: Optional, integer, range 1-100
- field3: Required, boolean

**Success Response (200 OK):**
```json
{
  "id": "uuid-v4",
  "field1": "string",
  "field2": 42,
  "field3": true,
  "created_at": "2025-11-05T14:30:00Z",
  "updated_at": "2025-11-05T14:30:00Z"
}
```

**Error Responses:**

**400 Bad Request (Validation Error):**
```json
{
  "error": "Validation failed",
  "details": [
    {
      "field": "field1",
      "message": "Email format is invalid"
    }
  ]
}
```

**401 Unauthorized (Authentication Failed):**
```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired token"
}
```

**403 Forbidden (Authorization Failed):**
```json
{
  "error": "Forbidden",
  "message": "Insufficient permissions. Required scope: admin:write"
}
```

**404 Not Found (Resource Not Found):**
```json
{
  "error": "Not found",
  "message": "{Resource} with id {id} not found"
}
```

**422 Unprocessable Entity (Business Rule Violation):**
```json
{
  "error": "Business rule violation",
  "message": "Cannot delete user with active orders",
  "details": {
    "active_orders": 3
  }
}
```

**500 Internal Server Error:**
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred. Request ID: {request_id}",
  "request_id": "uuid-v4"
}
```

**Rate Limiting (429 Too Many Requests):**
```json
{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Try again in 60 seconds.",
  "retry_after": 60
}
```
```

---

## REST API Examples by Operation

### Create Resource (POST)

```markdown
#### Endpoint: POST /api/users

**Description:** Create new user account

**Authentication:** Required (admin:write scope)

**Request Body:**
```json
{
  "email": "john.doe@example.com",
  "password": "SecurePass123!",
  "name": "John Doe",
  "role": "customer"
}
```

**Validation Rules:**
- email: Required, email format, unique, max 255 chars
- password: Required, min 8 chars, must include uppercase, lowercase, number, special char
- name: Required, 2-100 chars
- role: Required, one of: customer, admin, moderator

**Success Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "john.doe@example.com",
  "name": "John Doe",
  "role": "customer",
  "created_at": "2025-11-05T14:30:00Z"
}
```

**Response Headers:**
```http
Location: /api/users/550e8400-e29b-41d4-a716-446655440000
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Validation failed",
  "details": [
    {
      "field": "email",
      "message": "Email already exists"
    },
    {
      "field": "password",
      "message": "Password must include at least one uppercase letter"
    }
  ]
}
```
```

### List Resources (GET)

```markdown
#### Endpoint: GET /api/users

**Description:** List all users with pagination and filtering

**Authentication:** Required (admin:read scope)

**Query Parameters:**
- `page` (integer, optional, default: 1): Page number
- `limit` (integer, optional, default: 20, max: 100): Items per page
- `role` (string, optional): Filter by role (customer, admin, moderator)
- `status` (string, optional): Filter by status (active, inactive, suspended)
- `search` (string, optional): Search in name or email
- `sort` (string, optional, default: created_at): Sort field
- `order` (string, optional, default: desc): Sort order (asc, desc)

**Success Response (200 OK):**
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total_items": 150,
    "total_pages": 8
  },
  "links": {
    "self": "/api/users?page=1&limit=20",
    "next": "/api/users?page=2&limit=20",
    "prev": null,
    "first": "/api/users?page=1&limit=20",
    "last": "/api/users?page=8&limit=20"
  }
}
```
```

### Get Single Resource (GET)

```markdown
#### Endpoint: GET /api/users/{id}

**Description:** Retrieve single user by ID

**Authentication:** Required (read:users scope)

**Path Parameters:**
- `id` (UUID, required): User identifier

**Success Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "john.doe@example.com",
  "name": "John Doe",
  "role": "customer",
  "status": "active",
  "created_at": "2025-11-05T14:30:00Z",
  "updated_at": "2025-11-05T14:30:00Z"
}
```
```

### Update Resource (PUT/PATCH)

```markdown
#### Endpoint: PATCH /api/users/{id}

**Description:** Update user fields (partial update)

**Authentication:** Required (write:users scope or self)

**Request Body (Partial - only include fields to update):**
```json
{
  "name": "John Smith",
  "role": "moderator"
}
```

**Success Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Smith",
  "role": "moderator",
  "updated_at": "2025-11-05T18:45:00Z"
}
```
```

### Delete Resource (DELETE)

```markdown
#### Endpoint: DELETE /api/users/{id}

**Description:** Soft delete user (mark as deleted, preserve data)

**Authentication:** Required (admin:write scope)

**Success Response (204 No Content):** Empty body

**Error Response (422 — Dependencies Exist):**
```json
{
  "error": "Cannot delete user",
  "message": "User has 5 active orders. Cancel orders before deleting user."
}
```
```

---

## Data Model Documentation

### Entity Documentation Template

```markdown
#### Entity: {EntityName}

**Purpose:** {1-2 sentence description of what this entity represents}

**Attributes:**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Required, PK, Auto-generated | Unique identifier |
| {field} | {Type} | {Constraints} | {Description} |

**Relationships:**
- {Relationship type}: {Related entity} ({cardinality})

**Indexes:**
- {field} ({unique|non-unique}): {Purpose}

**Constraints:**
- Unique: {fields that must be unique together}
- Check: {custom constraints}

**Lifecycle:**
- Created when: {Trigger}
- Updated when: {Triggers}
- Deleted when: {Soft delete or hard delete strategy}

**Example Record:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "field1": "value",
  "created_at": "2025-11-05T14:30:00Z"
}
```
```

### Data Type Reference

| Type | Description | Examples | Validation |
|------|-------------|----------|------------|
| **UUID** | Universally unique identifier | `550e8400-e29b-41d4-a716-446655440000` | UUID v4 format |
| **String** | Text data | `"John Doe"`, `"test@example.com"` | Max length, pattern |
| **Integer** | Whole numbers | `42`, `-10`, `0` | Min/max range |
| **Float/Decimal** | Decimal numbers | `99.99`, `3.14159` | Precision, range |
| **Boolean** | True/false | `true`, `false` | N/A |
| **DateTime** | Timestamp | `"2025-11-05T14:30:00Z"` | ISO 8601 format |
| **Enum** | Fixed set of values | `"active"`, `"inactive"` | One of allowed values |
| **JSON** | Structured data | `{"key": "value"}` | Valid JSON |
| **Array** | List of items | `[1, 2, 3]` | Item type, length |

---

## Business Rules Documentation

### Business Rule Template

```markdown
### Business Rule: {Rule Name}

**Description:** {What this rule enforces}

**Trigger:** {When this rule is evaluated}

**Logic:**
{Step-by-step rule logic}

**Validation:**
{How to validate compliance}

**Error Handling:**
{What happens if rule is violated}

**Example:**
{Concrete example showing rule in action}
```

---

## Dependency Documentation

### Dependency Template

```markdown
### Dependency: {Service/Library Name}

**Type:** {External Service | Third-Party API | Database | Infrastructure | Library}

**Purpose:** {Why this dependency is needed}

**Integration Method:**
- {REST API | SDK | Library | Database connection | Message queue}
- Authentication: {API Key | OAuth2 | None}
- Endpoint/Connection: {URL or connection string}

**SLA Requirements:**
- Availability: {99.9% uptime}
- Response Time: {<500ms}
- Rate Limits: {100 requests/second}

**Fallback Behavior:**
{What happens if dependency is unavailable}

**Error Handling:**
{How errors from this dependency are handled}
```

---

**Use these templates to create complete, unambiguous technical specifications that enable implementation without back-and-forth clarification.**
