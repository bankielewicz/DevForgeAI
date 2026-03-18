# Multishot Examples for Discovering Requirements

This reference provides concrete input/output examples for each phase of the discovering-requirements skill. Load this file to calibrate output quality and format expectations.

---

## Table of Contents

- [Phase 1: Discovery & Problem Understanding](#phase-1-discovery-problem-understanding)
  - [Problem Statement](#problem-statement)
  - [User Personas](#user-personas)
  - [Scope Boundaries](#scope-boundaries)
- [Phase 2: Epic Decomposition](#phase-2-epic-decomposition)
  - [Decomposed Epics](#decomposed-epics)
  - [Summary](#summary)
  - [Recommended MVP Scope (12-week target)](#recommended-mvp-scope-12-week-target)
- [Phase 3: Complexity Scoring](#phase-3-complexity-scoring)
  - [Complexity Assessment](#complexity-assessment)

---

## Phase 1: Discovery & Problem Understanding

<example name="discovery-session-saas">
<input>
User says: "I want to build a task management SaaS. Something like Asana but simpler, focused on small dev teams. I don't have any specs yet, just the idea."
</input>
<output>

### Problem Statement

Small software development teams (3-15 members) lack a lightweight, developer-centric task management tool. Existing solutions (Asana, Monday, Jira) are either too complex with enterprise features that create overhead, or too simple (Trello) without adequate workflow automation. Teams waste 20-30 minutes per day navigating bloated interfaces and configuring irrelevant features.

**Target Outcome:** A streamlined task management platform that reduces daily project management overhead by 50% for small dev teams through opinionated workflows and minimal configuration.

### User Personas

**Persona 1: Team Lead (Primary)**
- **Role:** Engineering manager or tech lead for a 3-15 person dev team
- **Goals:** Track sprint progress, assign tasks, identify blockers quickly
- **Pain Points:** Jira is too heavy; spreadsheets lack automation; needs board + list views
- **Usage Frequency:** Daily, 30-60 minutes active use
- **Decision Authority:** Selects tools for the team, approves budget

**Persona 2: Developer (Primary)**
- **Role:** Individual contributor (frontend, backend, or fullstack)
- **Goals:** See assigned tasks, update status, log time, link commits
- **Pain Points:** Context switching between IDE and project tool; manual status updates
- **Usage Frequency:** Multiple times daily, 5-10 minute sessions
- **Decision Authority:** Influences tool selection through adoption/rejection

**Persona 3: Stakeholder (Secondary)**
- **Role:** Product owner, CTO, or client representative
- **Goals:** View progress dashboards, review milestones, export reports
- **Pain Points:** Needs visibility without learning a complex tool
- **Usage Frequency:** Weekly, 15-minute sessions
- **Decision Authority:** Approves project scope and timelines

### Scope Boundaries

**In Scope:**
- Task CRUD with assignees, priorities, due dates, and labels
- Kanban board and list views with drag-and-drop
- Sprint planning with backlog grooming
- Team workspaces with role-based access (Admin, Member, Viewer)
- Basic reporting (velocity, burndown, task completion rates)
- Notification system (in-app + email)
- REST API for integrations

**Out of Scope (Phase 1):**
- Native mobile applications (web-responsive only)
- Portfolio/program management (multi-project hierarchy)
- Built-in time tracking (defer to integrations)
- Custom workflow engines (opinionated statuses: To Do, In Progress, Review, Done)
- AI-powered features (auto-assignment, prediction)
- On-premise deployment (cloud-only SaaS)

**Open Questions for Phase 2:**
1. What pricing model? (freemium, per-seat, flat-rate)
2. Which Git provider integrations are highest priority? (GitHub, GitLab, Bitbucket)
3. Does the team need SSO/SAML for authentication?
4. What is the target launch timeline (MVP)?

</output>
</example>

---

## Phase 2: Epic Decomposition

<example name="epic-decomposition-saas">
<input>
Requirements gathered from Phase 1 discovery for the task management SaaS:
- Multi-tenant workspaces with role-based access
- Task management with boards, lists, sprints
- Team collaboration (comments, mentions, notifications)
- Reporting and analytics dashboards
- REST API and third-party integrations (GitHub, Slack)
- Authentication with email/password and Google OAuth
- Subscription billing (free tier + paid plans)

Target users: Small dev teams (3-15 members). MVP timeline: 12 weeks.
</input>
<output>

### Decomposed Epics

**EPIC-001: User Management & Authentication**
Priority: P0 (Must Have) | Estimated Points: 34

Features:
1. Email/password registration with verification (5 pts) - Priority: High
2. Google OAuth integration (3 pts) - Priority: High
3. User profile management (3 pts) - Priority: Medium
4. Password reset flow (3 pts) - Priority: High
5. Role-based access control (Admin, Member, Viewer) (8 pts) - Priority: High
6. Team invitation system with email invites (5 pts) - Priority: High
7. Session management and token refresh (3 pts) - Priority: High
8. Account deactivation and data export (4 pts) - Priority: Low

Dependencies: None (foundational epic)
Risks: OAuth provider API changes; email deliverability for verification

---

**EPIC-002: Task & Project Management**
Priority: P0 (Must Have) | Estimated Points: 55

Features:
1. Workspace creation and configuration (5 pts) - Priority: High
2. Project CRUD within workspaces (5 pts) - Priority: High
3. Task CRUD with rich fields (assignee, priority, due date, labels) (8 pts) - Priority: High
4. Kanban board view with drag-and-drop (8 pts) - Priority: High
5. List/table view with sorting and filtering (5 pts) - Priority: High
6. Sprint planning (create sprint, assign tasks, set dates) (8 pts) - Priority: High
7. Backlog management with priority ordering (5 pts) - Priority: Medium
8. Task dependencies and blocking relationships (5 pts) - Priority: Medium
9. Bulk task operations (move, assign, label) (3 pts) - Priority: Medium
10. Task templates for recurring work (3 pts) - Priority: Low
11. Subtasks and checklists (5 pts) - Priority: Medium
12. Custom labels and color coding (3 pts) - Priority: Low

Dependencies: EPIC-001 (requires authentication and RBAC)
Risks: Drag-and-drop performance with large boards; real-time sync conflicts

---

**EPIC-003: Collaboration & Notifications**
Priority: P1 (Should Have) | Estimated Points: 29

Features:
1. Task comments with @mentions (5 pts) - Priority: High
2. Activity feed per task and project (5 pts) - Priority: Medium
3. In-app notification center (5 pts) - Priority: High
4. Email notification preferences (3 pts) - Priority: Medium
5. Real-time updates via WebSocket (8 pts) - Priority: High
6. File attachments on tasks (3 pts) - Priority: Medium

Dependencies: EPIC-001, EPIC-002
Risks: WebSocket scaling; notification volume management

---

**EPIC-004: Reporting & Analytics**
Priority: P1 (Should Have) | Estimated Points: 26

Features:
1. Sprint velocity chart (5 pts) - Priority: High
2. Burndown chart (5 pts) - Priority: High
3. Task completion rate dashboard (3 pts) - Priority: Medium
4. Team workload distribution view (5 pts) - Priority: Medium
5. Export reports to CSV/PDF (5 pts) - Priority: Low
6. Custom date range filtering (3 pts) - Priority: Medium

Dependencies: EPIC-002 (requires task data)
Risks: Charting library performance with large datasets

---

**EPIC-005: Integrations & API**
Priority: P2 (Nice to Have for MVP) | Estimated Points: 31

Features:
1. Public REST API with API key auth (8 pts) - Priority: High
2. GitHub integration (link commits/PRs to tasks) (8 pts) - Priority: High
3. Slack integration (notifications, task creation) (5 pts) - Priority: Medium
4. Webhook system for custom integrations (5 pts) - Priority: Medium
5. API documentation with OpenAPI/Swagger (5 pts) - Priority: Medium

Dependencies: EPIC-001, EPIC-002
Risks: Third-party API rate limits; webhook delivery reliability

---

**EPIC-006: Subscription & Billing**
Priority: P1 (Should Have) | Estimated Points: 23

Features:
1. Free tier with workspace limits (3 workspaces, 10 members) (3 pts) - Priority: High
2. Stripe integration for payment processing (8 pts) - Priority: High
3. Plan management UI (upgrade, downgrade, cancel) (5 pts) - Priority: High
4. Usage metering and limit enforcement (5 pts) - Priority: High
5. Invoice history and receipts (2 pts) - Priority: Medium

Dependencies: EPIC-001
Risks: Stripe API versioning; proration calculations; PCI compliance

---

### Summary

| Epic | Priority | Points | Features | Dependencies |
|------|----------|--------|----------|-------------|
| EPIC-001: User Management | P0 | 34 | 8 | None |
| EPIC-002: Task & Project Mgmt | P0 | 55 | 12 | EPIC-001 |
| EPIC-003: Collaboration | P1 | 29 | 6 | EPIC-001, EPIC-002 |
| EPIC-004: Reporting | P1 | 26 | 6 | EPIC-002 |
| EPIC-005: Integrations & API | P2 | 31 | 5 | EPIC-001, EPIC-002 |
| EPIC-006: Billing | P1 | 23 | 5 | EPIC-001 |
| **Total** | | **198** | **42** | |

### Recommended MVP Scope (12-week target)

**Sprint 1-3:** EPIC-001 (Authentication) + EPIC-002 partial (Task CRUD, Board view)
**Sprint 4-6:** EPIC-002 completion (Sprints, Backlog) + EPIC-006 (Billing)
**Sprint 7-9:** EPIC-003 (Collaboration) + EPIC-004 (Reporting)
**Sprint 10-12:** EPIC-005 (Integrations) + Polish, QA, Launch prep

</output>
</example>

---

## Phase 3: Complexity Scoring

<example name="complexity-scoring-saas">
<input>
Requirements document for the task management SaaS with the following characteristics:
- 3 user roles (Admin, Member, Viewer) + external stakeholder view
- 8 core entities (User, Workspace, Project, Task, Sprint, Comment, Notification, Subscription)
- 3 external integrations (GitHub, Slack, Stripe)
- Multi-tenant architecture with workspace isolation
- Real-time updates via WebSocket for board changes
- Expected 500 concurrent users at launch, scaling to 5,000 within 12 months
- GDPR compliance required (EU customers)
- 99.9% uptime SLA target
</input>
<output>

### Complexity Assessment

**Total Score: 38/60**
**Architecture Tier: Advanced (Tier 3: 31-45)**

---

#### Score Breakdown

**Functional Complexity: 14/20**

| Factor | Assessment | Score |
|--------|-----------|-------|
| User Roles | 3 roles + external view = Medium-High | 4/5 |
| Core Entities | 8 entities with relationships = Medium | 3/5 |
| External Integrations | 3 integrations (GitHub, Slack, Stripe) = Medium | 3/5 |
| Workflow Complexity | Sprint workflows + task state machines = High | 4/5 |

Rationale: The combination of RBAC with workspace-scoped permissions, sprint state management (Planning -> Active -> Completed), and task lifecycle (To Do -> In Progress -> Review -> Done with blocked states) drives functional complexity above average. Three external integrations each with distinct protocols (REST for GitHub, WebSocket for Slack, webhook-driven for Stripe) add integration surface area.

**Technical Complexity: 13/20**

| Factor | Assessment | Score |
|--------|-----------|-------|
| Data Volume | Multi-tenant with workspace isolation = Medium | 3/5 |
| Concurrency | 500-5,000 concurrent users = Medium-High | 4/5 |
| Real-time Requirements | WebSocket for board updates = High | 4/5 |
| Architecture Pattern | Multi-tenant SaaS with tenant isolation = Medium | 2/5 |

Rationale: WebSocket connections for real-time board updates are the primary technical complexity driver. Each workspace needs its own update channel, and drag-and-drop operations require optimistic UI with conflict resolution. Scaling from 500 to 5,000 concurrent users within 12 months demands connection pooling and horizontal scaling strategy from day one.

**Team/Organizational Complexity: 5/10**

| Factor | Assessment | Score |
|--------|-----------|-------|
| Team Size | 3-5 developers (estimated) = Medium | 3/5 |
| Team Distribution | Assumed co-located or single timezone = Low | 2/5 |

Rationale: A small team building a full-featured SaaS means each developer covers multiple domains (auth + tasks + billing). This increases coordination overhead despite the small team size. The breadth of the feature set relative to team size is the primary complexity factor.

**Non-Functional Complexity: 6/10**

| Factor | Assessment | Score |
|--------|-----------|-------|
| Performance | 99.9% uptime SLA = High | 3/5 |
| Compliance | GDPR (EU data residency, right to deletion) = Medium-High | 3/5 |

Rationale: GDPR compliance requires data residency controls, right-to-erasure implementation across all 8 entities, consent management, and audit logging. Combined with 99.9% uptime (8.7 hours downtime/year maximum), this demands proper monitoring, alerting, and zero-downtime deployment strategies.

---

#### Architecture Tier Implications

**Advanced (Tier 3) recommends:**

- **Backend:** NestJS or FastAPI with structured module architecture
- **Frontend:** React or Next.js with state management (Zustand or Redux Toolkit)
- **Database:** PostgreSQL with row-level security for tenant isolation
- **Cache:** Redis for session management and real-time pub/sub
- **Search:** PostgreSQL full-text search (upgrade to Elasticsearch if needed later)
- **Infrastructure:** Docker containers on AWS ECS or GCP Cloud Run, with auto-scaling
- **CI/CD:** GitHub Actions with staging environment and automated testing
- **Monitoring:** Structured logging + APM (Datadog or self-hosted Grafana stack)

**Key architectural decisions to resolve:**
1. Tenant isolation strategy: Schema-per-tenant vs. row-level security vs. database-per-tenant
2. WebSocket scaling: Native WebSocket server vs. managed service (Pusher, Ably)
3. Background job processing: Bull/BullMQ (Node.js) or Celery (Python)

</output>
</example>
