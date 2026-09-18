# Technical Specification Guide — GraphQL API

Sub-reference for stories with GraphQL API. Loaded by Phase 03 Step 3.2.5 when `detect-indicators` identifies GraphQL needs.

---

## GraphQL API Patterns

### Query

```markdown
#### GraphQL Query: user

**Description:** Fetch user by ID with related data

**Arguments:**
- `id` (ID!, required): User identifier

**Returns:** User object with fields

**Schema:**
```graphql
type Query {
  user(id: ID!): User
}

type User {
  id: ID!
  email: String!
  name: String!
  role: Role!
  orders(first: Int, after: String): OrderConnection!
  createdAt: DateTime!
}

type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type OrderEdge {
  node: Order!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

**Example Query:**
```graphql
query GetUser {
  user(id: "550e8400-e29b-41d4-a716-446655440000") {
    id
    email
    name
    role
    orders(first: 10) {
      edges {
        node {
          orderNumber
          total
          status
        }
      }
      totalCount
    }
  }
}
```

**Example Response:**
```json
{
  "data": {
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "john@example.com",
      "name": "John Doe",
      "role": "CUSTOMER",
      "orders": {
        "edges": [
          {
            "node": {
              "orderNumber": "ORD-2025-00042",
              "total": 187.50,
              "status": "DELIVERED"
            }
          }
        ],
        "totalCount": 15
      }
    }
  }
}
```
```

### Mutation

```markdown
#### GraphQL Mutation: createUser

**Description:** Create new user account

**Arguments:**
- `input` (CreateUserInput!, required): User creation data

**Returns:** CreateUserPayload with created user or errors

**Schema:**
```graphql
type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}

input CreateUserInput {
  email: String!
  password: String!
  name: String!
  role: Role = CUSTOMER
}

type CreateUserPayload {
  user: User
  errors: [UserError!]
}

type UserError {
  field: String!
  message: String!
}
```

**Example Mutation:**
```graphql
mutation CreateUser {
  createUser(input: {
    email: "new@example.com"
    password: "SecurePass123!"
    name: "New User"
    role: CUSTOMER
  }) {
    user {
      id
      email
      name
    }
    errors {
      field
      message
    }
  }
}
```

**Success Response:**
```json
{
  "data": {
    "createUser": {
      "user": {
        "id": "new-uuid",
        "email": "new@example.com",
        "name": "New User"
      },
      "errors": []
    }
  }
}
```

**Error Response (Validation):**
```json
{
  "data": {
    "createUser": {
      "user": null,
      "errors": [
        {
          "field": "email",
          "message": "Email already exists"
        }
      ]
    }
  }
}
```
```

---

**Use these templates to create complete, unambiguous GraphQL specifications that enable implementation without back-and-forth clarification.**
