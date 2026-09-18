# REST API Design Patterns

**Purpose:** Complete REST API design reference including URL patterns, HTTP methods, status codes, request/response examples, versioning, and error handling.

---

## Resource-Oriented URLs

```
# GOOD: Resource-oriented
GET    /api/users           # List users
POST   /api/users           # Create user
GET    /api/users/:id       # Get user
PUT    /api/users/:id       # Update user
DELETE /api/users/:id       # Delete user

GET    /api/users/:id/orders    # User's orders (sub-resource)
POST   /api/users/:id/orders    # Create order for user

# BAD: Action-oriented
GET    /api/getUsers
POST   /api/createUser
GET    /api/getUserById
```

---

## HTTP Method Semantics

| Method | Purpose | Idempotent | Safe | Response |
|--------|---------|------------|------|----------|
| GET | Retrieve resource(s) | Yes | Yes | 200, 404 |
| POST | Create resource | No | No | 201, 400, 409 |
| PUT | Replace resource | Yes | No | 200, 404 |
| PATCH | Update resource partially | No | No | 200, 404 |
| DELETE | Delete resource | Yes | No | 204, 404 |

---

## HTTP Status Codes

**Success (2xx):**
- 200 OK: Request succeeded (GET, PUT, PATCH)
- 201 Created: Resource created (POST)
- 204 No Content: Success with no body (DELETE)

**Client Errors (4xx):**
- 400 Bad Request: Invalid input
- 401 Unauthorized: Not authenticated
- 403 Forbidden: Not authorized
- 404 Not Found: Resource doesn't exist
- 409 Conflict: Resource already exists or conflict

**Server Errors (5xx):**
- 500 Internal Server Error: Unexpected error
- 503 Service Unavailable: Temporary unavailability

---

## Request/Response Examples

**Create User (POST):**
```yaml
POST /api/users
Content-Type: application/json

Request:
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe",
  "role": "user"
}

Response (201 Created):
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}

Response (400 Bad Request):
{
  "error": "Validation failed",
  "details": [
    { "field": "email", "message": "Email format is invalid" },
    { "field": "password", "message": "Password must be at least 12 characters" }
  ]
}

Response (409 Conflict):
{
  "error": "User already exists",
  "details": "A user with this email address already exists"
}
```

**Get User (GET):**
```yaml
GET /api/users/123e4567-e89b-12d3-a456-426614174000
Authorization: Bearer <token>

Response (200 OK):
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}

Response (404 Not Found):
{
  "error": "User not found",
  "details": "No user exists with ID 123e4567-e89b-12d3-a456-426614174000"
}
```

**Update User (PATCH):**
```yaml
PATCH /api/users/123e4567-e89b-12d3-a456-426614174000
Authorization: Bearer <token>
Content-Type: application/json

Request:
{
  "name": "Jane Doe"
}

Response (200 OK):
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "name": "Jane Doe",
  "role": "user",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T11:45:00Z"
}
```

**List Users (GET with pagination):**
```yaml
GET /api/users?page=1&limit=20&sort=created_at:desc
Authorization: Bearer <token>

Response (200 OK):
{
  "data": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "email": "user1@example.com",
      "name": "User 1",
      "created_at": "2025-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total_pages": 5,
    "total_items": 93,
    "has_next": true,
    "has_previous": false
  }
}
```

---

## API Versioning Strategies

### 1. URL Path Versioning (Recommended)
```
https://api.example.com/v1/users
https://api.example.com/v2/users
```

### 2. Header Versioning
```
GET /api/users
Accept: application/vnd.example.v1+json
```

### 3. Query Parameter Versioning
```
https://api.example.com/users?version=1
```

**Recommendation**: URL path versioning (most explicit and discoverable)

---

## Error Handling Standards

**Standard Error Format:**
```json
{
  "error": "Brief error message",
  "details": "More detailed explanation",
  "code": "ERROR_CODE",
  "request_id": "uuid",
  "timestamp": "ISO8601"
}
```

**Example Errors:**
```json
// Validation Error
{
  "error": "Validation failed",
  "details": [
    { "field": "email", "message": "Email format is invalid", "value": "invalid-email" }
  ],
  "code": "VALIDATION_ERROR"
}

// Authorization Error
{
  "error": "Forbidden",
  "details": "You do not have permission to access this resource",
  "code": "INSUFFICIENT_PERMISSIONS"
}

// Rate Limit Error
{
  "error": "Rate limit exceeded",
  "details": "Maximum 100 requests per minute allowed",
  "code": "RATE_LIMIT_EXCEEDED",
  "retry_after": 45
}
```

---

## API Consistency Checklist

**Naming Conventions:**
- [ ] Resources use plural nouns (`/users`, not `/user`)
- [ ] Snake_case for JSON keys (or camelCase, but consistent)
- [ ] Boolean fields prefixed with `is_` or `has_`
- [ ] Timestamp fields suffixed with `_at`

**Response Format:**
- [ ] Consistent structure across endpoints
- [ ] Timestamps in ISO8601 format
- [ ] Pagination format consistent
- [ ] Error format standardized

**HTTP Methods:**
- [ ] GET for retrieval (no side effects)
- [ ] POST for creation
- [ ] PUT for full replacement
- [ ] PATCH for partial updates
- [ ] DELETE for removal

**Authentication:**
- [ ] Consistent auth mechanism (Bearer token)
- [ ] 401 for unauthenticated
- [ ] 403 for unauthorized
- [ ] Token expiration handled
