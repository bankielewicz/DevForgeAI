# Complete devforgeai-architecture References - Missing Files

## Context

The devforgeai-architecture skill has broken reference links that need to be fixed.

**Current Issues**:
1. ❌ **Missing**: `references/system-design-patterns.md` (referenced in SKILL.md line 893)
2. ❌ **Broken links**: Template filenames mismatch (lines 891-892)
3. ⚠️ **Empty**: `assets/adr-examples/` directory (no example ADRs)

**Priority**: Fix issues 1 and 2 (CRITICAL), issue 3 is optional

---

## Objective

Fix all broken reference links in devforgeai-architecture skill:
1. Create `system-design-patterns.md` reference file
2. Fix template filename references in SKILL.md
3. (Optional) Populate ADR examples directory

**Estimated Time**: 2.5-3 hours for critical fixes, +1-2 hours for optional ADR examples

---

## Required Actions

### Action 1: Create system-design-patterns.md (CRITICAL)

**File**: `.claude/skills/devforgeai-architecture/references/system-design-patterns.md`

**Content**: Comprehensive guide to common architecture patterns used in software development

**Structure** (800-1,000 lines):

```markdown
# System Design Patterns Reference

Common architecture patterns for DevForgeAI projects. Use this guide when making architectural decisions during context file creation.

---

## Layered Architecture Patterns

### Clean Architecture (Onion Architecture)

**Description:**
A layered architecture pattern that enforces dependency rules: outer layers can depend on inner layers, but never the reverse.

**Layers (inside-out):**
1. **Domain** (Core) - Business entities, value objects, domain services
2. **Application** - Use cases, application services, interfaces
3. **Infrastructure** - Data access, external services, frameworks
4. **Presentation** (API/UI) - Controllers, views, DTOs

**Dependency Rules:**
- Domain depends on: Nothing (pure business logic)
- Application depends on: Domain only
- Infrastructure depends on: Domain, Application (implements interfaces)
- Presentation depends on: Application only (never Domain or Infrastructure directly)

**When to Use:**
- Medium to complex applications
- Long-term maintainability important
- Testability is priority
- Team experienced with layered architecture

**When NOT to Use:**
- Simple CRUD applications (over-engineering)
- Rapid prototyping (too much ceremony)
- Team unfamiliar with pattern (learning curve)

**Example Project Structure:**
```
src/
├── Domain/
│   ├── Entities/
│   ├── ValueObjects/
│   ├── Interfaces/
│   └── Services/
├── Application/
│   ├── UseCases/
│   ├── Services/
│   └── DTOs/
├── Infrastructure/
│   ├── Persistence/
│   ├── Repositories/
│   └── Services/
└── API/
    ├── Controllers/
    └── Middleware/
```

**Context File Impact:**
- tech-stack.md: Should specify "Clean Architecture"
- source-tree.md: Should enforce layer directory structure
- architecture-constraints.md: Should define dependency rules
- anti-patterns.md: Should forbid layer violations (Domain → Infrastructure)

---

### N-Tier Architecture (3-Tier)

**Description:**
Traditional layered architecture with presentation, business logic, and data access tiers.

**Tiers:**
1. **Presentation Tier** - UI, API controllers
2. **Business Logic Tier** - Services, business rules
3. **Data Access Tier** - Repositories, database operations

**When to Use:**
- Standard enterprise applications
- Team familiar with traditional layering
- Clear separation of concerns needed
- Moderate complexity

**Example Project Structure:**
```
src/
├── Presentation/
│   ├── Web/
│   ├── API/
│   └── Controllers/
├── Business/
│   ├── Services/
│   └── Models/
└── DataAccess/
    ├── Repositories/
    └── Context/
```

---

### Vertical Slice Architecture

**Description:**
Organize code by feature/use case rather than technical layers. Each feature is a vertical slice through all layers.

**Structure:**
```
src/Features/
├── Users/
│   ├── Register/
│   │   ├── RegisterCommand.cs
│   │   ├── RegisterHandler.cs
│   │   ├── RegisterValidator.cs
│   │   └── RegisterEndpoint.cs
│   └── Login/
│       ├── LoginCommand.cs
│       ├── LoginHandler.cs
│       └── LoginEndpoint.cs
└── Products/
    ├── Create/
    ├── Update/
    └── Delete/
```

**When to Use:**
- Feature-focused development
- Frequent feature additions
- Small to medium applications
- Rapid iteration

---

## Microservices Patterns

### Service Decomposition Strategies

**By Business Capability:**
- User Service (authentication, profiles)
- Order Service (order management, fulfillment)
- Payment Service (transactions, billing)
- Notification Service (emails, SMS, push)

**By Subdomain (DDD):**
- Bounded contexts define service boundaries
- Each service owns its data
- Services communicate via events or APIs

**Decomposition Criteria:**
- Single Responsibility Principle
- Independent deployability
- Team autonomy
- Data ownership

---

### API Gateway Pattern

**Purpose:** Single entry point for clients, routes to appropriate services

**Responsibilities:**
- Request routing
- Authentication/authorization
- Rate limiting
- Request aggregation
- Protocol translation

**Technologies:** Kong, Nginx, Ocelot, AWS API Gateway, Azure API Management

---

### Event-Driven Architecture

**Pattern:** Services communicate via events (asynchronous)

**Components:**
- Event Producers (publish events)
- Event Bus/Broker (RabbitMQ, Kafka, Azure Service Bus)
- Event Consumers (subscribe to events)

**When to Use:**
- Loose coupling required
- Asynchronous processing acceptable
- High scalability needed
- Complex workflows across services

---

## Data Access Patterns

### Repository Pattern

**Purpose:** Abstraction layer between domain and data access

**Structure:**
```csharp
public interface IUserRepository
{
    User GetById(int id);
    void Add(User user);
    void Update(User user);
    void Delete(int id);
}

public class UserRepository : IUserRepository
{
    // Implementation using Dapper, EF, etc.
}
```

**Benefits:**
- Testability (mock repositories in tests)
- Abstraction from data access technology
- Centralized data access logic

**When to Use:**
- Domain-Driven Design
- Multiple data sources
- Complex queries need abstraction

---

### Unit of Work Pattern

**Purpose:** Coordinate multiple repository operations in single transaction

**Pattern:**
```csharp
using (var unitOfWork = new UnitOfWork())
{
    unitOfWork.UserRepository.Add(user);
    unitOfWork.OrderRepository.Add(order);
    unitOfWork.Commit(); // Single transaction
}
```

**When to Use:**
- Multiple entities changed in one operation
- Transaction coordination needed
- Working with Entity Framework or NHibernate

---

### Active Record vs Data Mapper

**Active Record:**
- Domain objects have data access methods
- User.Save(), User.Delete()
- Simpler, less abstraction
- Used by: Ruby on Rails, Laravel

**Data Mapper:**
- Separate domain objects from data access
- Repository handles persistence
- More testable, cleaner domain
- Used by: Clean Architecture, DDD

---

## API Design Patterns

### RESTful API Design

**Principles:**
- Resources as nouns (not verbs)
- HTTP methods: GET, POST, PUT, DELETE, PATCH
- Status codes: 200, 201, 204, 400, 401, 403, 404, 500
- Stateless communication

**Example:**
```
GET    /api/users          - List users
GET    /api/users/{id}     - Get user
POST   /api/users          - Create user
PUT    /api/users/{id}     - Update user
DELETE /api/users/{id}     - Delete user
```

---

### CQRS (Command Query Responsibility Segregation)

**Pattern:** Separate read and write operations

**Structure:**
- **Commands:** Modify state (CreateUser, UpdateOrder)
- **Queries:** Read state (GetUser, ListOrders)

**Benefits:**
- Optimized read models (different from write models)
- Scalability (scale reads and writes independently)
- Complex domain logic separation

**When to Use:**
- Different read and write requirements
- High read/write ratio imbalance
- Complex business logic on writes

---

## Caching Strategies

### Cache-Aside (Lazy Loading)

1. Check cache
2. If miss: Load from database, populate cache
3. If hit: Return cached value

**When to Use:** Read-heavy workloads

---

### Write-Through

1. Write to cache AND database simultaneously
2. Cache always in sync with database

**When to Use:** Consistency critical

---

### Write-Behind (Write-Back)

1. Write to cache immediately
2. Asynchronously write to database later

**When to Use:** Write performance critical

---

## Authentication Patterns

### JWT (JSON Web Tokens)

**Pattern:** Stateless authentication with signed tokens

**Flow:**
1. User logs in with credentials
2. Server validates, issues JWT
3. Client includes JWT in subsequent requests
4. Server validates JWT signature

**When to Use:**
- Stateless API (no server sessions)
- Microservices (token valid across services)
- Mobile/SPA clients

---

### Session-Based Authentication

**Pattern:** Server maintains session state

**Flow:**
1. User logs in
2. Server creates session, stores session ID in cookie
3. Client sends session cookie with requests
4. Server validates session

**When to Use:**
- Traditional web applications
- Server-side rendering
- Simple authentication needs

---

### OAuth 2.0 / OpenID Connect

**Pattern:** Delegated authentication (third-party)

**When to Use:**
- "Login with Google/Facebook/GitHub"
- API authorization scopes
- Enterprise SSO (Single Sign-On)

---

## Database Patterns

### Database per Service (Microservices)

**Pattern:** Each microservice has its own database

**Benefits:**
- Service independence
- Technology flexibility (polyglot persistence)
- Isolated failures

**Challenges:**
- Distributed transactions
- Data consistency
- Joins across services

---

### Shared Database (Monolith/N-Tier)

**Pattern:** All services/modules share single database

**Benefits:**
- ACID transactions
- Simple joins
- Easier consistency

**Challenges:**
- Coupling between services
- Schema changes affect all services
- Scalability bottleneck

---

## Integration Patterns

### Synchronous (HTTP/REST)

**Pattern:** Request-response, client waits

**When to Use:**
- Immediate response needed
- Simple request-response workflows
- Low latency requirements

---

### Asynchronous (Message Queue)

**Pattern:** Fire-and-forget, eventual consistency

**Technologies:** RabbitMQ, Kafka, Azure Service Bus, AWS SQS

**When to Use:**
- Long-running operations
- Decoupled services
- High throughput needed

---

## Scalability Patterns

### Horizontal Scaling (Scale Out)

**Pattern:** Add more instances/servers

**When to Use:**
- Stateless applications
- Cloud-native applications
- Load distribution needed

---

### Vertical Scaling (Scale Up)

**Pattern:** Increase resources of existing server

**When to Use:**
- Database servers
- Legacy applications
- Short-term capacity increase

---

### Load Balancing

**Strategies:**
- Round Robin
- Least Connections
- IP Hash
- Weighted Round Robin

**Technologies:** Nginx, HAProxy, AWS ALB, Azure Load Balancer

---

## Reference Materials for Pattern Selection

**When making architecture decisions:**

1. **Read existing context if brownfield:**
   ```
   Read(file_path=".devforgeai/context/architecture-constraints.md")
   ```

2. **Use AskUserQuestion for pattern selection:**
   ```
   Question: "Which architecture pattern should be used?"
   Options:
     - "Clean Architecture (Domain-centric, testable)"
     - "N-Tier (Traditional, simple)"
     - "Vertical Slice (Feature-focused)"
     - "Microservices (Distributed, scalable)"
   ```

3. **Document decision in ADR:**
   - Use ADR template from references/adr-template.md
   - Document pattern choice, rationale, trade-offs

4. **Update context files:**
   - architecture-constraints.md: Define layer rules for chosen pattern
   - source-tree.md: Define directory structure for pattern

---

**This reference should be consulted during Phase 2 (Create Immutable Context Files) when defining architecture-constraints.md for projects.**
```

**Estimated Size**: ~900 lines

**Should cover**:
- 10-15 major architecture patterns
- Each pattern: Description, benefits, when to use, example structure, context file impact
- Clear guidance for architecture decision-making

---

### Action 2: Fix Template Filename References (CRITICAL)

**File**: `.claude/skills/devforgeai-architecture/SKILL.md`

**Lines to Fix**:

**Line 891-892 (Current - INCORRECT)**:
```markdown
- [Tech Stack Template](./assets/context-templates/tech-stack-template.md) - Technology documentation
- [Source Tree Template](./assets/context-templates/source-tree-template.md) - Structure documentation
```

**Should Be (CORRECT)**:
```markdown
- [Tech Stack Template](./assets/context-templates/tech-stack.md) - Technology documentation
- [Source Tree Template](./assets/context-templates/source-tree.md) - Structure documentation
```

**Action**: Use Edit tool to fix the two filenames

```
Edit(file_path=".claude/skills/devforgeai-architecture/SKILL.md",
     old_string="- [Tech Stack Template](./assets/context-templates/tech-stack-template.md)",
     new_string="- [Tech Stack Template](./assets/context-templates/tech-stack.md)")

Edit(file_path=".claude/skills/devforgeai-architecture/SKILL.md",
     old_string="- [Source Tree Template](./assets/context-templates/source-tree-template.md)",
     new_string="- [Source Tree Template](./assets/context-templates/source-tree.md)")
```

**Estimated Time**: 2 minutes

---

### Action 3: Populate ADR Examples (OPTIONAL)

**Directory**: `.claude/skills/devforgeai-architecture/assets/adr-examples/`

**Create 5 Example ADRs** showing different decision scenarios:

#### 1. ADR-EXAMPLE-001-database-selection.md (200-250 lines)

```markdown
# ADR-EXAMPLE-001: PostgreSQL for E-Commerce Platform

**Date**: 2025-10-15
**Status**: Accepted
**Deciders**: Technical Architect, Lead Developer
**Project**: E-Commerce Platform

## Context

We need to select a database for a new e-commerce platform that will handle:
- Product catalog (50,000+ products)
- User accounts (100,000+ users)
- Order history (transactional data)
- Shopping cart (session data)
- Search functionality (full-text search)

**Requirements:**
- ACID compliance for transactions
- JSON support for flexible product attributes
- Full-text search capabilities
- Proven at scale (millions of records)
- Strong community and tooling support
- Cost-effective for startup budget

## Decision

We will use **PostgreSQL 15.x** as our primary database.

## Rationale

### Technical Capabilities
- **ACID Compliance**: Full transaction support for order processing
- **JSON/JSONB Support**: Flexible product attributes without schema changes
- **Full-Text Search**: Built-in tsvector for product search (avoid separate search engine)
- **Performance**: Proven at scale (Instagram, Twitch use PostgreSQL)
- **Extensions**: PostGIS for location features, pg_trgm for fuzzy search

### Operational Considerations
- **Mature Ecosystem**: 25+ years of development, stable releases
- **Tooling**: pgAdmin, DBeaver, strong ORM support (Dapper, EF Core, Hibernate)
- **Managed Services**: AWS RDS, Azure Database, Google Cloud SQL
- **Cost**: Open-source, no licensing fees

### Team Skills
- 3 of 5 developers have PostgreSQL experience
- Similar to MySQL (minimal learning curve for others)
- Good documentation and community resources

### Future-Proofing
- Horizontal scaling via Citus extension
- Read replicas for scaling reads
- Partitioning for large tables
- Logical replication for multi-region

## Consequences

### Positive
- No licensing costs (open-source)
- Flexible schema with JSON support
- Built-in full-text search (avoid ElasticSearch initially)
- Excellent performance for transactional workloads
- Strong ACID guarantees for financial transactions
- Rich extension ecosystem
- Managed services available (reduced ops burden)

### Negative
- Steeper learning curve than MySQL for some developers
- Write performance can be lower than MySQL in some scenarios
- Vertical scaling limits (eventual need for sharding or Citus)
- More resource-intensive than MySQL

### Risks and Mitigations
- **Risk**: Team unfamiliar with advanced features
  - **Mitigation**: Training session, documentation, pair programming
- **Risk**: Scaling beyond single instance
  - **Mitigation**: Plan for read replicas, partitioning, Citus extension
- **Risk**: Managed service costs at scale
  - **Mitigation**: Start with AWS RDS, evaluate cost vs self-hosted later

## Alternatives Considered

### Alternative 1: MySQL 8.0
**Pros:**
- Simpler for basic operations
- Slightly better write performance
- More developers have experience

**Cons:**
- Weaker JSON support (no JSONB equivalent)
- Limited full-text search compared to PostgreSQL
- Fewer advanced features

**Why Rejected:** JSON support and full-text search are critical requirements

### Alternative 2: MongoDB
**Pros:**
- Native JSON documents (no schema)
- Horizontal scaling built-in
- Flexible schema changes

**Cons:**
- No ACID transactions across documents (historically)
- Weaker querying for relational data
- Different paradigm (learning curve for SQL team)
- Eventual consistency challenges for transactions

**Why Rejected:** ACID compliance critical for e-commerce transactions, team expertise in SQL

### Alternative 3: Microsoft SQL Server
**Pros:**
- Excellent tooling (SSMS, Visual Studio integration)
- Strong ACID compliance
- Mature and proven

**Cons:**
- Licensing costs (significant for startup)
- Primarily Windows-focused (Linux support improving)
- Vendor lock-in

**Why Rejected:** Cost prohibitive for startup budget, prefer open-source

## Implementation

### Immediate Actions
1. ✅ Add to tech-stack.md: "Database: PostgreSQL 15.x (LOCKED)"
2. ✅ Add to dependencies.md: "Npgsql 7.x (for .NET) or pg 8.x (for Node.js)"
3. ✅ Add to architecture-constraints.md: "All data access through repositories"
4. ✅ Document this decision: Create ADR-001 in docs/architecture/decisions/

### Database Setup
- Provision AWS RDS PostgreSQL 15.x instance
- Configure connection pooling (pgBouncer)
- Set up automated backups (daily)
- Configure read replica for reporting queries

### Development Standards
- Use parameterized queries (prevent SQL injection)
- Use Dapper for queries, EF Core for migrations (per tech-stack.md)
- Implement repository pattern (abstraction from database)

## Monitoring

- Track query performance (pg_stat_statements)
- Monitor connection pool usage
- Set up alerts for slow queries (>1 second)
- Review query plans quarterly

## Review Schedule

- 3 months: Assess performance and scaling needs
- 6 months: Evaluate read replica requirements
- 12 months: Consider partitioning strategy for orders table

---

**Status**: Accepted and implemented
**Last Updated**: 2025-10-15
**Related ADRs**: None
**Supersedes**: None
```

#### 2. ADR-EXAMPLE-002-orm-selection.md (200 lines)

[Similar structure for Dapper vs Entity Framework choice]

#### 3. ADR-EXAMPLE-003-state-management.md (200 lines)

[Similar structure for Zustand vs Redux choice]

#### 4. ADR-EXAMPLE-004-clean-architecture.md (250 lines)

[Similar structure for Clean Architecture pattern choice]

#### 5. ADR-EXAMPLE-005-deployment-strategy.md (200 lines)

[Similar structure for Kubernetes vs Azure App Service]

**Total ADR Examples**: ~1,050 lines across 5 files

---

## Commands to Execute

### Critical Fixes (Required)

```bash
# 1. Read current architecture SKILL.md
Read(file_path=".claude/skills/devforgeai-architecture/SKILL.md")

# 2. Create system-design-patterns.md
Write(file_path=".claude/skills/devforgeai-architecture/references/system-design-patterns.md", content="[900 lines of architecture patterns]")

# 3. Fix template filename references
Edit(file_path=".claude/skills/devforgeai-architecture/SKILL.md",
     old_string="tech-stack-template.md",
     new_string="tech-stack.md")

Edit(file_path=".claude/skills/devforgeai-architecture/SKILL.md",
     old_string="source-tree-template.md",
     new_string="source-tree.md")

# 4. Validate fixes
Bash(command="ls -la .claude/skills/devforgeai-architecture/references/")
Bash(command="grep -o 'references/[^)]*\\.md' .claude/skills/devforgeai-architecture/SKILL.md | sort -u")
```

### Optional ADR Examples

```bash
# 5. Create ADR examples (optional)
Write(file_path=".claude/skills/devforgeai-architecture/assets/adr-examples/ADR-EXAMPLE-001-database-selection.md", content="...")
Write(file_path=".claude/skills/devforgeai-architecture/assets/adr-examples/ADR-EXAMPLE-002-orm-selection.md", content="...")
Write(file_path=".claude/skills/devforgeai-architecture/assets/adr-examples/ADR-EXAMPLE-003-state-management.md", content="...")
Write(file_path=".claude/skills/devforgeai-architecture/assets/adr-examples/ADR-EXAMPLE-004-clean-architecture.md", content="...")
Write(file_path=".claude/skills/devforgeai-architecture/assets/adr-examples/ADR-EXAMPLE-005-deployment-strategy.md", content="...")
```

---

## Validation

After completing fixes:

```bash
# Check system-design-patterns.md created
ls -lh .claude/skills/devforgeai-architecture/references/system-design-patterns.md
# Expected: Exists, 800-1,000 lines

# Verify all 3 reference files exist
ls -la .claude/skills/devforgeai-architecture/references/
# Expected: 3 files (adr-template, ambiguity-detection, system-design-patterns)

# Check template references fixed
grep "context-templates" .claude/skills/devforgeai-architecture/SKILL.md | grep -E "(tech-stack|source-tree)"
# Expected: No "-template" suffix in filenames

# Optional: Check ADR examples created
ls -la .claude/skills/devforgeai-architecture/assets/adr-examples/
# Expected: 5 example ADR files (if Option B chosen)
```

---

## Success Criteria

### Critical Fixes (Minimum)
- [ ] system-design-patterns.md created (800-1,000 lines)
- [ ] Template filename references fixed in SKILL.md
- [ ] All 3 reference links working
- [ ] No broken links in architecture skill

### Complete Package (Full)
- [ ] system-design-patterns.md created
- [ ] Template filenames fixed
- [ ] 5 ADR examples created
- [ ] All reference links working
- [ ] All example links working

---

## Post-Completion Review Prompt

```
I've completed the architecture skill missing files. Please review:

1. Does system-design-patterns.md exist with 800-1,000 lines?
2. Are template filename references fixed (tech-stack.md not tech-stack-template.md)?
3. Do all reference links work?
4. (Optional) Are ADR examples created in assets/adr-examples/?

Run validation:
- ls -la .claude/skills/devforgeai-architecture/references/
- ls -la .claude/skills/devforgeai-architecture/assets/adr-examples/
- grep "references/" .claude/skills/devforgeai-architecture/SKILL.md
- grep "context-templates" .claude/skills/devforgeai-architecture/SKILL.md
```

---

**Priority**: CRITICAL (broken reference links)
**Estimated Time**: 2.5-3 hours (critical) or 3.5-5 hours (with ADR examples)
**Recommended**: Fix critical issues first, defer ADR examples to future iteration
