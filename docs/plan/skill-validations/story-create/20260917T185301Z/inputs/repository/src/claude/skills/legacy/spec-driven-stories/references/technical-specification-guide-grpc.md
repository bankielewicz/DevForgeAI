# Technical Specification Guide — gRPC API

Sub-reference for stories with gRPC services. Loaded by Phase 03 Step 3.2.5 when `detect-indicators` identifies gRPC needs.

---

## gRPC API Patterns

### Service Definition

```markdown
#### gRPC Service: UserService

**Description:** User management operations

**Protocol Buffers Definition:**
```protobuf
syntax = "proto3";

package user.v1;

service UserService {
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
  rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
  rpc UpdateUser(UpdateUserRequest) returns (UpdateUserResponse);
  rpc DeleteUser(DeleteUserRequest) returns (DeleteUserResponse);
}

message CreateUserRequest {
  string email = 1;
  string password = 2;
  string name = 3;
  Role role = 4;
}

message CreateUserResponse {
  User user = 1;
  repeated Error errors = 2;
}

message User {
  string id = 1;
  string email = 2;
  string name = 3;
  Role role = 4;
  google.protobuf.Timestamp created_at = 5;
}

enum Role {
  ROLE_UNSPECIFIED = 0;
  ROLE_CUSTOMER = 1;
  ROLE_ADMIN = 2;
  ROLE_MODERATOR = 3;
}

message Error {
  string field = 1;
  string message = 2;
}
```

**Example Request/Response:**
```
Request:
CreateUserRequest {
  email: "user@example.com"
  password: "SecurePass123!"
  name: "John Doe"
  role: ROLE_CUSTOMER
}

Success Response:
CreateUserResponse {
  user: {
    id: "uuid"
    email: "user@example.com"
    name: "John Doe"
    role: ROLE_CUSTOMER
    created_at: {timestamp}
  }
  errors: []
}

Error Response:
CreateUserResponse {
  user: null
  errors: [
    {field: "email", message: "Email already exists"}
  ]
}
```
```

---

**Use these templates to create complete, unambiguous gRPC specifications that enable implementation without back-and-forth clarification.**
