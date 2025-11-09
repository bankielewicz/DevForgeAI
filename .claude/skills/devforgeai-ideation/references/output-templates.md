# Ideation Output Templates

This reference provides standardized templates for presenting ideation results to users. Load this file when preparing completion summaries in Phase 6 of the ideation workflow.

---

## Completion Summary Template

Use this template when reporting ideation completion to users:

```markdown
## ✅ Ideation Complete

### Generated Artifacts

**Epic Documents:**
- EPIC-001: {Epic Title} ({Feature Count} features, {Story Points} points)
- EPIC-002: {Epic Title} ({Feature Count} features, {Story Points} points)
[... list all epics ...]
- Location: `.ai_docs/Epics/`

**Requirements Specification:**
- Location: `.devforgeai/specs/requirements/{project-name}-requirements.md`
- Functional Requirements: {count}
- Non-Functional Requirements: {count}
- Data Models: {count} entities
- Integration Points: {count} external systems

### Complexity Assessment

**Total Score:** {score}/60
**Architecture Tier:** {Simple|Standard|Advanced|Enterprise}

**Score Breakdown:**
- Functional Complexity: {score}/20
- Technical Complexity: {score}/20
- Team/Organizational Complexity: {score}/10
- Non-Functional Complexity: {score}/10

### Recommended Technology Stack

Based on {tier} architecture tier:

**Backend:** {recommendations}
**Frontend:** {recommendations}
**Database:** {recommendations}
**Infrastructure:** {recommendations}

### Next Steps

1. **Review** generated epics and requirements specification
2. **Validate** complexity assessment and architecture tier
3. **Proceed** to architecture phase (`/create-context`) to define:
   - Technology stack decisions (tech-stack.md)
   - Project structure (source-tree.md)
   - Approved dependencies (dependencies.md)
   - Coding standards (coding-standards.md)
   - Architecture constraints (architecture-constraints.md)
   - Anti-patterns to avoid (anti-patterns.md)
```

---

## Technology Recommendations by Tier

Use these recommendations when presenting technology stack guidance based on complexity tier.

### Tier 1: Simple Application (0-15 points)

**Characteristics:**
- Single developer or small team
- Straightforward requirements
- Limited integrations
- Low to moderate traffic
- Minimal compliance requirements

**Backend Recommendations:**

**Node.js Stack:**
- Framework: Express.js (lightweight, unopinionated)
- ORM: Prisma (type-safe, modern)
- Validation: Zod (TypeScript-first)
- API Style: RESTful

**Python Stack:**
- Framework: FastAPI (high performance, automatic docs)
- ORM: SQLAlchemy (mature, flexible)
- Validation: Pydantic (data validation)
- API Style: RESTful

**.NET Stack:**
- Framework: ASP.NET Core Minimal APIs
- ORM: Entity Framework Core
- Validation: FluentValidation
- API Style: RESTful

**Frontend Recommendations:**

**React Ecosystem:**
- Framework: React 18+ with Vite
- Routing: React Router
- State: React Context or Zustand (lightweight)
- Styling: Tailwind CSS
- Build: Vite (fast, modern)

**Vue Ecosystem:**
- Framework: Vue 3 with Composition API
- Routing: Vue Router
- State: Pinia (official state management)
- Styling: Tailwind CSS
- Build: Vite

**Other Options:**
- Next.js (React with SSR)
- Plain HTML/CSS/JavaScript (for simple UIs)
- Svelte (lightweight, compiled framework)

**Database Recommendations:**

**Relational:**
- SQLite (file-based, zero-config, perfect for small apps)
- PostgreSQL (single instance, robust features)
- MySQL (mature, widely supported)

**NoSQL:**
- MongoDB (single node, document-based)

**Infrastructure Recommendations:**

**Serverless:**
- Vercel (frontend + serverless functions)
- Netlify (frontend + edge functions)
- AWS Lambda (backend APIs)

**Traditional Hosting:**
- Single VPS (DigitalOcean, Linode, Hetzner)
- Heroku (platform-as-a-service)
- Fly.io (modern PaaS)

**Containerization:**
- Docker Compose (local development)
- Single Docker container (production)

---

### Tier 2: Standard Application (16-30 points)

**Characteristics:**
- Small to medium team (2-5 developers)
- Moderate complexity requirements
- Multiple integrations
- Moderate to high traffic
- Standard compliance (GDPR, basic security)

**Backend Recommendations:**

**Node.js Stack:**
- Framework: Express.js or NestJS (enterprise patterns)
- ORM: Prisma or TypeORM
- Validation: Zod or class-validator
- Authentication: Passport.js or Auth0
- API Style: RESTful with OpenAPI/Swagger
- Testing: Jest, Supertest

**Python Stack:**
- Framework: Django (batteries-included) or FastAPI
- ORM: Django ORM or SQLAlchemy
- Validation: Pydantic or Django Rest Framework serializers
- Authentication: Django Auth or JWT
- API Style: RESTful or GraphQL
- Testing: pytest

**.NET Stack:**
- Framework: ASP.NET Core Web API
- ORM: Entity Framework Core
- Validation: FluentValidation
- Authentication: ASP.NET Core Identity or IdentityServer
- API Style: RESTful with Swagger
- Testing: xUnit, NUnit

**Frontend Recommendations:**

**React Ecosystem:**
- Framework: React with TypeScript
- Routing: React Router
- State: Redux Toolkit or Zustand
- Data Fetching: React Query or SWR
- Forms: React Hook Form
- Styling: Tailwind CSS or Material-UI
- Build: Vite or Webpack
- Testing: Vitest, React Testing Library

**Vue Ecosystem:**
- Framework: Vue 3 with TypeScript
- Routing: Vue Router
- State: Pinia
- Data Fetching: VueQuery
- Forms: VeeValidate
- Styling: Tailwind CSS or Vuetify
- Build: Vite
- Testing: Vitest, Vue Testing Library

**Angular Ecosystem:**
- Framework: Angular 16+ with TypeScript
- Routing: Angular Router
- State: NgRx (Redux pattern)
- Forms: Reactive Forms
- Styling: Angular Material or Tailwind CSS
- Build: Angular CLI
- Testing: Jasmine, Karma

**Database Recommendations:**

**Relational:**
- PostgreSQL (primary + read replicas)
- MySQL/MariaDB (primary + read replicas)
- Azure SQL Database (managed)
- AWS RDS (managed PostgreSQL/MySQL)

**NoSQL:**
- MongoDB (replica set for high availability)
- Redis (caching and session storage)

**Infrastructure Recommendations:**

**Cloud Platforms:**
- AWS (EC2, ECS, or Elastic Beanstalk)
- Azure (App Service, Container Instances)
- Google Cloud Platform (Cloud Run, App Engine)

**Containerization:**
- Docker containers
- Docker Compose (multi-container orchestration)
- Kubernetes (single cluster) - optional for this tier

**CI/CD:**
- GitHub Actions
- GitLab CI/CD
- Azure DevOps
- CircleCI

**Monitoring:**
- Application Insights (Azure)
- CloudWatch (AWS)
- Datadog
- New Relic

---

### Tier 3: Advanced Platform (31-45 points)

**Characteristics:**
- Medium to large team (5-15 developers)
- Complex business logic
- Extensive integrations
- High traffic and scalability needs
- Advanced compliance (HIPAA, SOC2, PCI-DSS)

**Backend Recommendations:**

**Microservices Architecture:**

**Node.js Stack:**
- Framework: NestJS (microservices support)
- API Gateway: Kong or AWS API Gateway
- Service Communication: gRPC or message queues
- Event Bus: RabbitMQ or Apache Kafka
- ORM: Prisma or TypeORM
- Authentication: OAuth2 or JWT with refresh tokens
- API Style: RESTful + GraphQL federation
- Testing: Jest, Integration tests, Contract testing

**Python Stack:**
- Framework: FastAPI (async support) or Django
- API Gateway: Kong or Traefik
- Service Communication: gRPC or Celery
- Event Bus: RabbitMQ or Apache Kafka
- ORM: SQLAlchemy or Django ORM
- Authentication: OAuth2
- API Style: RESTful + GraphQL
- Testing: pytest, Integration tests

**.NET Stack:**
- Framework: ASP.NET Core (microservices templates)
- API Gateway: Ocelot or YARP
- Service Communication: gRPC
- Event Bus: MassTransit with RabbitMQ
- ORM: Entity Framework Core
- Authentication: IdentityServer4 or Duende IdentityServer
- API Style: RESTful + GraphQL
- Testing: xUnit, Integration tests

**Go Stack (High Performance Services):**
- Framework: Gin or Echo
- Service Communication: gRPC
- Event Bus: NATS or Kafka
- ORM: GORM or sqlx
- Authentication: JWT
- Testing: Go testing package

**Frontend Recommendations:**

**Micro-Frontends:**
- Framework: React or Vue with Module Federation
- Routing: Framework Router + Shell Router
- State: Framework state + shared state bus
- Component Library: Custom design system
- Build: Webpack 5 Module Federation or Vite
- Testing: Component tests, Integration tests

**Server-Side Rendering:**
- Next.js (React) - Enterprise patterns
- Nuxt.js (Vue) - Universal apps
- SvelteKit (Svelte) - Modern SSR

**Progressive Web Apps:**
- Service Workers (offline support)
- Web Push Notifications
- IndexedDB (client-side storage)
- App Shell pattern

**Database Recommendations:**

**Polyglot Persistence:**

**Relational:**
- PostgreSQL (multi-instance with read replicas)
- CockroachDB (distributed SQL)
- Azure SQL Database (geo-replication)

**NoSQL:**
- MongoDB (sharded clusters)
- Cassandra (distributed wide-column store)
- DynamoDB (AWS managed NoSQL)

**Caching:**
- Redis Cluster (distributed caching)
- Memcached (simple caching)

**Search:**
- Elasticsearch (full-text search)
- OpenSearch (AWS managed Elasticsearch)

**Time-Series:**
- InfluxDB (metrics and monitoring)
- TimescaleDB (PostgreSQL extension for time-series)

**Event Sourcing:**
- EventStore (purpose-built for event sourcing)
- Kafka (event log)

**Infrastructure Recommendations:**

**Container Orchestration:**
- Kubernetes (multi-cluster setup)
- AWS EKS, Azure AKS, or Google GKE
- Helm (package management)
- Kustomize (configuration management)

**Service Mesh:**
- Istio (traffic management, security)
- Linkerd (lightweight service mesh)
- Consul Connect (HashiCorp)

**API Gateway:**
- Kong (API management)
- AWS API Gateway
- Azure API Management
- Traefik (cloud-native proxy)

**Event Streaming:**
- Apache Kafka (distributed event streaming)
- AWS Kinesis
- Azure Event Hubs
- Google Pub/Sub

**Observability:**
- Prometheus (metrics collection)
- Grafana (dashboards)
- Jaeger or Zipkin (distributed tracing)
- ELK Stack (logging: Elasticsearch, Logstash, Kibana)
- Datadog or New Relic (APM)

**CI/CD:**
- GitLab CI/CD or GitHub Actions (pipelines)
- ArgoCD or Flux (GitOps deployment)
- Spinnaker (multi-cloud deployment)

---

### Tier 4: Enterprise Platform (46-60 points)

**Characteristics:**
- Large team (15+ developers, multiple teams)
- Highly complex business logic
- Extensive integration ecosystem
- Massive scale (millions of users)
- Strict compliance (multi-region, audit trails)
- High availability requirements (99.99%+)

**Backend Recommendations:**

**Distributed Microservices with Event-Driven Architecture:**

**Multi-Language Stack:**
- Core Services: .NET or Java (enterprise-grade)
- High-Performance Services: Go or Rust
- Data Processing: Python or Scala
- Scripting/Automation: Node.js

**Architecture Patterns:**
- CQRS (Command Query Responsibility Segregation)
- Event Sourcing (full audit trail)
- Saga Pattern (distributed transactions)
- Domain-Driven Design (DDD)

**Service Communication:**
- gRPC (internal service-to-service)
- REST (external APIs)
- GraphQL Federation (unified API layer)
- WebSockets (real-time communication)

**API Gateway:**
- Kong Enterprise (API management)
- Apigee (Google)
- AWS API Gateway + AppSync
- Azure API Management

**Event Bus:**
- Apache Kafka (distributed event streaming)
- AWS Kinesis + EventBridge
- Azure Event Hubs + Event Grid
- NATS (high-performance messaging)

**Authentication/Authorization:**
- OAuth2 + OpenID Connect
- IdentityServer or Auth0 (enterprise)
- Azure AD or AWS Cognito
- Multi-factor authentication (MFA)
- Single Sign-On (SSO)

**Frontend Recommendations:**

**Enterprise Micro-Frontends:**
- Shell Application: Module Federation
- Framework: React, Vue, or Angular
- Design System: Custom component library
- State Management: Distributed state
- Deployment: Independent deployments per team

**Real-Time Collaboration:**
- WebSockets (Socket.io, SignalR)
- WebRTC (peer-to-peer video/audio)
- Operational Transform or CRDT (conflict-free data structures)

**Edge Computing:**
- Cloudflare Workers (edge functions)
- AWS Lambda@Edge
- Azure Front Door

**Database Recommendations:**

**Polyglot Persistence (Strategic):**

**Relational (Primary Data):**
- Google Cloud Spanner (globally distributed SQL)
- CockroachDB (multi-region consistency)
- Azure Cosmos DB (SQL API)
- Aurora Global Database (AWS)

**NoSQL (Specialized Workloads):**
- Cassandra (massive write throughput)
- DynamoDB Global Tables (AWS)
- Azure Cosmos DB (multi-model)

**Caching (Multi-Tier):**
- Redis Enterprise (distributed caching)
- Memcached (session caching)
- CDN edge caching (Cloudflare, Fastly)

**Search & Analytics:**
- Elasticsearch (full-text search at scale)
- OpenSearch (AWS)
- Azure Cognitive Search

**Time-Series & Metrics:**
- InfluxDB Enterprise (high cardinality)
- TimescaleDB (PostgreSQL-based)
- Prometheus (metrics)

**Graph Database:**
- Neo4j (relationship-heavy data)
- Amazon Neptune (AWS managed)

**Data Warehouse:**
- Snowflake (cloud data warehouse)
- Google BigQuery
- Azure Synapse Analytics
- Amazon Redshift

**Infrastructure Recommendations:**

**Multi-Region Kubernetes:**
- AWS EKS (multi-region)
- Azure AKS (geo-distributed)
- Google GKE (global clusters)
- Rancher or OpenShift (enterprise Kubernetes)

**Service Mesh:**
- Istio (advanced traffic management)
- Consul + Envoy (HashiCorp stack)

**Auto-Scaling:**
- Horizontal Pod Autoscaler (HPA)
- Vertical Pod Autoscaler (VPA)
- Cluster Autoscaler
- KEDA (event-driven autoscaling)

**Global Load Balancing:**
- AWS Global Accelerator
- Azure Front Door
- Google Cloud Load Balancing
- Cloudflare Load Balancing

**CDN & Edge:**
- Cloudflare (global CDN)
- Fastly (real-time CDN)
- AWS CloudFront
- Azure CDN

**Disaster Recovery:**
- Multi-region active-active
- Cross-region replication
- Automated failover
- RTO < 1 hour, RPO < 5 minutes

**Observability (Enterprise-Grade):**
- Prometheus + Thanos (long-term metrics)
- Grafana (dashboards)
- Jaeger or Datadog APM (distributed tracing)
- ELK or Splunk (logging at scale)
- PagerDuty or Opsgenie (incident management)

**Security:**
- Zero Trust Architecture
- Secrets Management (HashiCorp Vault, AWS Secrets Manager)
- Network Policies (Kubernetes)
- WAF (Web Application Firewall)
- DDoS Protection (Cloudflare, AWS Shield)
- SIEM (Security Information and Event Management)

**CI/CD (Enterprise):**
- GitLab Ultimate or GitHub Enterprise
- ArgoCD or Flux (GitOps)
- Spinnaker (multi-cloud deployment)
- Jenkins X (cloud-native CI/CD)

**Cost Optimization:**
- Spot Instances / Reserved Instances
- Auto-scaling policies
- Resource quotas
- Cost monitoring (Kubecost, CloudHealth)

---

## Next Steps Template

Use this template when transitioning users to the architecture phase:

```markdown
## 🎯 Ready for Architecture Phase

Ideation is complete with structured requirements and complexity assessment. The next step is defining architectural constraints.

### What /create-context Does

The architecture skill will generate **6 context files** that serve as immutable constraints for all development:

1. **tech-stack.md** - Locked technology choices (prevents library substitution)
2. **source-tree.md** - Project structure rules (prevents chaos)
3. **dependencies.md** - Approved packages (prevents bloat)
4. **coding-standards.md** - Code patterns (enforces consistency)
5. **architecture-constraints.md** - Layer boundaries (prevents violations)
6. **anti-patterns.md** - Forbidden patterns (prevents technical debt)

### Input from Ideation

The architecture skill will reference:
- ✅ Requirements specification (functional/non-functional requirements)
- ✅ Complexity assessment (architecture tier: {tier})
- ✅ Technology recommendations (based on {score}/60 complexity)
- ✅ Epic documents (feature scope and priorities)

### Expected Interaction

The architecture skill will:
1. **Validate** requirements and complexity tier
2. **Ask** technology preference questions (via AskUserQuestion)
3. **Recommend** technologies based on complexity tier
4. **Resolve** any conflicts between user preferences and requirements
5. **Generate** all 6 context files
6. **Create** initial ADR (Architecture Decision Record)

### Command to Run

```bash
/create-context {project-name}
```

Example:
```bash
/create-context task-management-saas
```

This will create context files in `.devforgeai/context/` and transition you to orchestration phase (sprint planning).
```

---

## Brownfield Project Template

Use this template when dealing with existing codebases:

```markdown
## 🏗️ Brownfield Project Detected

Existing codebase found. Ideation complete with requirements for new features/modernization.

### Existing Context Files

**Status:** Context files found in `.devforgeai/context/`

**Files:**
- ✅ tech-stack.md (existing technology choices)
- ✅ source-tree.md (current project structure)
- ✅ dependencies.md (approved packages)
- ✅ coding-standards.md (existing standards)
- ✅ architecture-constraints.md (current constraints)
- ✅ anti-patterns.md (known anti-patterns)

### Requirements Validation

The ideation skill has validated new requirements against existing constraints:

**Conflicts Detected:** {count}
- {List any technology conflicts}
- {List any architecture constraint violations}
- {List any anti-pattern concerns}

**Resolution Required:**
- Use AskUserQuestion to resolve each conflict
- Update context files if strategic change needed
- Create ADR documenting any context file changes

### Next Steps

**Option 1: Proceed with Orchestration**
If no conflicts or all resolved:
```bash
/create-sprint {sprint-number}
```

**Option 2: Update Context Files**
If strategic technology changes needed:
```bash
/create-context {project-name}
```
Note: This will update existing context files and create ADRs for changes.

**Option 3: Manual Review**
Review requirements and context files manually:
- Requirements: `.devforgeai/specs/requirements/`
- Context: `.devforgeai/context/`
- Epics: `.ai_docs/Epics/`
```

---

## Epic Summary Template

Use this template when summarizing individual epics:

```markdown
### Epic: {EPIC-ID} - {Epic Title}

**Business Value:** {1-sentence value proposition}

**Features:** {count} features
- {Feature 1 name} (Priority: {High|Medium|Low})
- {Feature 2 name} (Priority: {High|Medium|Low})
[... list all features ...]

**Estimated Complexity:** {story points} points

**Success Metrics:**
- {Metric 1}: {Target}
- {Metric 2}: {Target}
[... list all metrics ...]

**Dependencies:**
- {Dependency 1}
- {Dependency 2}

**Risks:**
- {Risk 1} (Likelihood: {Low|Medium|High}, Impact: {Low|Medium|High})
- {Risk 2} (Likelihood: {Low|Medium|High}, Impact: {Low|Medium|High})

**Timeline:** {estimated weeks}
```

---

## Complexity Assessment Explanation Template

Use this template when explaining complexity scores to users:

```markdown
### Understanding Your Complexity Score

**Total Score:** {score}/60
**Tier:** {Simple|Standard|Advanced|Enterprise}

#### Score Breakdown

**Functional Complexity: {score}/20**
- User Roles: {count} roles ({Low|Medium|High} = {points} points)
- Core Entities: {count} entities ({Low|Medium|High} = {points} points)
- Integrations: {count} integrations ({Low|Medium|High} = {points} points)
- Workflow Complexity: {Linear|Branching|State Machines} = {points} points

**Technical Complexity: {score}/20**
- Data Volume: {volume} ({Low|Medium|High} = {points} points)
- Concurrency: {users} concurrent users ({Low|Medium|High} = {points} points)
- Real-time Requirements: {None|Polling|WebSockets} = {points} points

**Team/Organizational Complexity: {score}/10**
- Team Size: {count} developers ({Low|Medium|High} = {points} points)
- Team Distribution: {Co-located|Remote|Multi-timezone} = {points} points

**Non-Functional Complexity: {score}/10**
- Performance Requirements: {Moderate|Standard|High} = {points} points
- Compliance Requirements: {None|Standard|Strict} = {points} points

#### What This Means

**{Tier} Architecture** is recommended for complexity level {score}/60.

**Typical characteristics of {tier} applications:**
{Insert tier-specific characteristics from tier definitions above}

**Technology recommendations:**
{Insert tier-specific tech stack recommendations}

**Development timeline estimate:**
MVP: {weeks} weeks
Full feature set: {weeks} weeks

**Team size recommendation:**
{count} developers for optimal velocity
```

---

## Reference Usage Instructions

**When to Load This File:**
- Phase 6: Requirements Documentation & Handoff
- Specifically Phase 6.3: Transition to Architecture Skill
- When preparing completion summary for user

**How to Use Templates:**
1. Load this reference file: `Read(file_path=".claude/skills/devforgeai-ideation/references/output-templates.md")`
2. Select appropriate template based on context (greenfield vs brownfield, tier, etc.)
3. Fill in placeholders with actual values from ideation process
4. Present formatted output to user

**Progressive Disclosure:**
- Load only when needed (Phase 6)
- Templates provide structure without consuming tokens during Phases 1-5
- Reference file can be updated without changing skill logic
