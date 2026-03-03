# OpenAPI 3.0 Specification Reference

**Purpose:** Complete OpenAPI 3.0 specification template with CRUD endpoint examples.

---

## Complete Example

```yaml
openapi: 3.0.0
info:
  title: User Management API
  description: API for managing user accounts and authentication
  version: 1.0.0
  contact:
    name: API Support
    email: api@example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server

paths:
  /users:
    get:
      summary: List users
      description: Retrieve a paginated list of users
      operationId: listUsers
      tags:
        - Users
      parameters:
        - name: page
          in: query
          description: Page number
          schema:
            type: integer
            minimum: 1
            default: 1
        - name: limit
          in: query
          description: Items per page
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: sort
          in: query
          description: Sort order (field:asc or field:desc)
          schema:
            type: string
            example: created_at:desc
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
        '401':
          $ref: '#/components/responses/Unauthorized'
      security:
        - bearerAuth: []

    post:
      summary: Create user
      description: Create a new user account
      operationId: createUser
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreate'
            examples:
              example1:
                summary: Standard user
                value:
                  email: user@example.com
                  password: SecurePass123!
                  name: John Doe
                  role: user
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          description: User already exists
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
      security:
        - bearerAuth: []

  /users/{userId}:
    get:
      summary: Get user
      description: Retrieve a specific user by ID
      operationId: getUser
      tags:
        - Users
      parameters:
        - name: userId
          in: path
          required: true
          description: User ID (UUID)
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'
      security:
        - bearerAuth: []

    patch:
      summary: Update user
      description: Update specific fields of a user
      operationId: updateUser
      tags:
        - Users
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserUpdate'
      responses:
        '200':
          description: User updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '404':
          $ref: '#/components/responses/NotFound'
      security:
        - bearerAuth: []

    delete:
      summary: Delete user
      description: Delete a user account
      operationId: deleteUser
      tags:
        - Users
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '204':
          description: User deleted successfully
        '404':
          $ref: '#/components/responses/NotFound'
      security:
        - bearerAuth: []

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
          example: "123e4567-e89b-12d3-a456-426614174000"
        email:
          type: string
          format: email
          example: "user@example.com"
        name:
          type: string
          minLength: 2
          maxLength: 100
          example: "John Doe"
        role:
          type: string
          enum: [user, admin]
          example: "user"
        created_at:
          type: string
          format: date-time
          example: "2025-01-15T10:30:00Z"
        updated_at:
          type: string
          format: date-time
          example: "2025-01-15T10:30:00Z"
      required:
        - id
        - email
        - name
        - role
        - created_at
        - updated_at

    UserCreate:
      type: object
      properties:
        email:
          type: string
          format: email
        password:
          type: string
          format: password
          minLength: 12
        name:
          type: string
          minLength: 2
          maxLength: 100
        role:
          type: string
          enum: [user, admin]
          default: user
      required:
        - email
        - password
        - name

    UserUpdate:
      type: object
      properties:
        name:
          type: string
          minLength: 2
          maxLength: 100
        role:
          type: string
          enum: [user, admin]

    Error:
      type: object
      properties:
        error:
          type: string
          description: Error message
        details:
          oneOf:
            - type: string
            - type: array
              items:
                type: object
                properties:
                  field:
                    type: string
                  message:
                    type: string
      required:
        - error

    Pagination:
      type: object
      properties:
        page:
          type: integer
          minimum: 1
        limit:
          type: integer
          minimum: 1
        total_pages:
          type: integer
          minimum: 0
        total_items:
          type: integer
          minimum: 0
        has_next:
          type: boolean
        has_previous:
          type: boolean

  responses:
    BadRequest:
      description: Invalid input
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    Unauthorized:
      description: Not authenticated
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT token obtained from /auth/login endpoint

security:
  - bearerAuth: []
```
