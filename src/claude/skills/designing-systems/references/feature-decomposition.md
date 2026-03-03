<!-- MERGED: epic-decomposition-workflow.md + feature-decomposition-patterns.md (STORY-434) -->

# Feature Decomposition

Break down epics into independently valuable features and work units. This unified reference combines the decomposition process (workflow) and domain patterns (templates) into a single authoritative guide.

---

## Table of Contents

1. [Process](#process)
2. [Domain Patterns](#domain-patterns)
3. [Sizing Guidelines](#sizing-guidelines)
4. [Framework Integration](#framework-integration)

---

## Process

### Overview

Feature decomposition is the critical bridge between high-level epics (business initiatives spanning 2-6 sprints) and detailed user stories (work units implementable in 1-3 days).

**Duration:** 10-20 minutes
**Output:** 3-8 features per epic, high-level story outlines, dependencies

### Step 1: Epic Identification

An **epic** is:
- High-level business capability or initiative
- Spans multiple sprints (4-8 weeks typical)
- Delivers measurable business value independently
- Can be prioritized relative to other epics
- Contains 3-8 features

### Step 2: Extract Capabilities from Epic Goal

```
Epic Goal: "Improve checkout experience to increase conversion rate"

Capabilities:
- Allow guests to check out without account
- Let users save payment methods
- Display progress through checkout steps
- Support multiple currencies
- Recover from checkout errors gracefully
```

### Step 3: Feature Grouping — Group Related Capabilities into Features

```
Feature 1: Guest Checkout
├─ Guest checkout form (minimal data)
├─ Guest account creation option
└─ Email confirmation of order

Feature 2: Payment Method Management
├─ Save payment methods to account
├─ Select from saved methods
├─ Update/delete payment methods
└─ Add new payment method during checkout
```

### Step 4: Validate Independence

Check dependency matrix:
```
                 F1   F2   F3   F4
Feature 1 (Guest) -   Hard Soft  Soft
Feature 2 (Payment) Soft  -   Soft  Hard

Key: Hard = blocks other feature, Soft = nice-to-have ordering
```

**If many Hard dependencies:** Reconsider grouping

### Step 5: Right-Size Each Feature

Estimate story count per feature:
```
Feature 1 (Guest): 4 stories, 10 points, 1 sprint
Feature 2 (Payment): 5 stories, 13 points, 1-2 sprints
```

**If feature is 20+ points → split further**

### Step 6: Define Feature Acceptance Criteria

```
Feature 1: Guest Checkout
[ ] Guest checkout form displays without login
[ ] Email validation works (confirmation email sent)
[ ] Order confirmation page shows for guests
[ ] Guest can track order without account
```

### Step 7: Story Decomposition (High-Level)

A **story** is:
- Smallest deliverable increment
- Completed within single sprint (1-5 days)
- Has testable acceptance criteria (Given/When/Then)
- Delivers user value (no technical-only stories)

**Example - Feature: "User Registration"**

**Story 1:** Registration form with validation
- As a new user, I want to register with email/password, so I can create an account

**Story 2:** Email verification workflow
- As a new user, I want to verify my email, so I can activate my account

### Epic Prioritization

**Prioritization criteria:**
- Business value (user-facing features first)
- Dependencies (must-have-first features)
- Risk (de-risk technical unknowns early)
- MVP definition (core user flow complete)

---

## Domain Patterns

### 1. CRUD Application Pattern

**Use for:** Entity management covering Create, Read, Update, Delete, List, Search

**Example Epic:** User Management System

**Decomposition:**
```
Feature 1: User Creation & Registration
├─ User registration form with validation
├─ Email verification workflow
├─ Initial profile setup
└─ Account activation

Feature 2: User Profile Management
├─ View user profile information
├─ Edit personal information
├─ Change password
└─ Update profile picture

Feature 3: User Search & Directory
├─ Search users by name/email
├─ Filter by department/role
├─ Browse user directory
└─ View user details

Feature 4: User Deactivation & Cleanup
├─ Deactivate user account
├─ Archive user data
├─ Reassign user responsibilities
└─ Account recovery option
```

**Duration:** 3-4 sprints

---

### 2. Authentication/Authorization Pattern

**Use for:** Identity features covering registration, authentication, session management, permission models

**Example Epic:** Enterprise User Authentication

**Decomposition:**
```
Feature 1: Basic Email/Password Authentication
├─ User registration with email
├─ Login with credentials
├─ Password reset via email
└─ Session management

Feature 2: Multi-Factor Authentication
├─ TOTP (authenticator app) setup
├─ Backup codes generation
├─ MFA enforcement policies
└─ Device trust management

Feature 3: Single Sign-On (SSO) Integration
├─ OAuth 2.0 provider integration (Google, Microsoft)
├─ SAML 2.0 support for enterprises
├─ Automatic account linking
└─ SSO session management

Feature 4: Role-Based Access Control (RBAC)
├─ Define system roles
├─ Assign roles to users
├─ Permission inheritance hierarchy
└─ Role-based view filtering
```

**Duration:** 4-5 sprints (security-critical)

**Framework Integration:**
- MUST check anti-patterns.md for forbidden patterns
- MUST check tech-stack.md for approved authentication libraries
- security-auditor subagent required for validation

---

### 3. API Development Pattern

**Use for:** REST/GraphQL endpoint features covering resources, operations, versioning

**Example Epic:** REST API v2 Development

**Decomposition:**
```
Feature 1: Core Resource Endpoints
├─ GET /users (list users with pagination)
├─ POST /users (create new user)
├─ PUT /users/{id} (update user)
├─ DELETE /users/{id} (delete user)
└─ Error handling and validation

Feature 2: Advanced Querying
├─ Filter by field values
├─ Sort by multiple fields
├─ Cursor-based pagination
└─ Partial responses (field selection)

Feature 3: API Documentation & Discovery
├─ OpenAPI/Swagger specification
├─ API documentation portal
└─ Interactive API explorer

Feature 4: API Security & Rate Limiting
├─ API key authentication
├─ OAuth 2.0 token validation
├─ Rate limiting per client
└─ DDoS protection headers
```

**Duration:** 3-4 sprints

---

### 4. Workflow/Process Pattern

**Use for:** Stage features covering initiation, processing, approval, completion

**Example Epic:** Approval Workflow System

**Decomposition:**
```
Feature 1: Request Creation & Submission
├─ Request form with validation
├─ Attachment support
├─ Request draft saving
└─ Notification to approvers

Feature 2: Approval Process Management
├─ View pending approvals
├─ Approve/reject with comments
├─ Multi-level approval routing
└─ Approval history tracking

Feature 3: Escalation & Delegation
├─ Escalation to manager
├─ Delegation to colleague
├─ Escalation timeout rules
└─ Audit trail of delegations

Feature 4: Completion & Documentation
├─ Auto-execution after approval
├─ Completion notification
├─ Delivery/implementation tracking
└─ Archive approved requests
```

**Duration:** 3-4 sprints

**Dependencies:** Feature 1 → Feature 2 → Features 3-4

---

### 5. E-Commerce Pattern

**Use for:** Transaction features covering catalog, cart, checkout, payment, fulfillment

**Example Epic:** E-Commerce Platform

**Decomposition:**
```
Feature 1: Product Catalog Management
├─ Add/edit/delete products
├─ Product categorization
├─ Inventory management
└─ Product variants (size, color)

Feature 2: Shopping Cart & Wishlist
├─ Add/remove items from cart
├─ Update quantities
├─ Wishlist functionality
└─ Cart persistence across sessions

Feature 3: Checkout Flow
├─ Shipping address entry
├─ Shipping method selection
├─ Order review page
└─ Order confirmation

Feature 4: Payment Processing
├─ Credit/debit card payments
├─ PayPal integration
├─ PCI compliance
└─ Payment error handling

Feature 5: Order Management & Fulfillment
├─ Order status tracking
├─ Shipment notifications
├─ Return request processing
└─ Return shipping labels
```

**Duration:** 4-5 sprints

**Dependencies:** Feature 1 → Features 2-3 → Feature 4 → Feature 5

---

### 6. SaaS Platform Pattern

**Use for:** Multi-tenant platforms with subscription, billing, admin

**Decomposition:**
```
Feature 1: Tenant Onboarding
├─ Organization registration
├─ Initial admin setup
├─ Workspace configuration
└─ User invitation flow

Feature 2: Core Application Features
├─ [Domain-specific CRUD]
├─ Collaboration features
├─ Export/import data
└─ Activity audit log

Feature 3: Subscription & Billing
├─ Pricing tier selection
├─ Payment method management
├─ Invoice generation
└─ Usage tracking

Feature 4: Admin Dashboard
├─ Tenant management
├─ User administration
├─ System configuration
└─ Analytics/reporting
```

**Duration:** 5-6 sprints

---

## Sizing Guidelines

### Feature Size Reference

| Size | Sprints | Points | Characteristics |
|------|---------|--------|-----------------|
| **Small** | 1 | 8-13 | Single entity, minimal integrations |
| **Medium** | 1-2 | 13-21 | 2-3 entities, one integration |
| **Large** | 2-3 | 21-30 | 4+ entities, multiple integrations |
| **Very Large** | >3 | >30 | **SHOULD SPLIT** |

### What Makes a Good Feature

| Characteristic | Good | Poor |
|---|---|---|
| **Scope** | 1-2 sprints | <5 pts or >25 pts |
| **Value** | User-facing benefit | Technical-only work |
| **Independence** | Can be developed separately | Tightly coupled |
| **Testing** | Clear acceptance criteria | Vague success conditions |
| **Demonstration** | Shippable demo possible | Requires other features |

---

## Framework Integration

### Before Finalizing Feature List

**Technology Alignment:**
- [ ] Proposed technologies appear in tech-stack.md
- [ ] External integrations in dependencies.md
- [ ] No unapproved library substitutions

**Architecture Compliance:**
- [ ] Features respect architecture-constraints.md layer boundaries
- [ ] No cross-layer violations
- [ ] Integration points clearly defined

**Anti-Pattern Prevention:**
- [ ] No God Object features (500+ line classes)
- [ ] No direct instantiation (DI required)
- [ ] No hardcoded secrets or SQL concatenation

**Security Considerations:**
- [ ] Features handling sensitive data flagged for security-auditor
- [ ] Authentication/authorization requirements documented
- [ ] Compliance requirements noted (PCI/GDPR)

**Dependency Mapping:**
- [ ] Feature dependencies form valid DAG (no cycles)
- [ ] Critical path clearly identified
- [ ] Parallel-able features isolated

---

## Common Issues and Recovery

### Too Many Epics (>5)

**Recovery:**
1. Group related epics under parent epic
2. Merge epics with <3 features
3. Defer low-priority epics to future releases

### Epic Too Small (<3 features)

**Recovery:**
1. Consider if this is really a feature, not an epic
2. Expand feature list (are there related capabilities?)
3. Merge with another related epic

### Circular Dependencies

**Recovery:**
1. Identify shared capability
2. Extract as separate epic that both depend on
3. Or merge both epics if tightly coupled

### Feature Too Large (>8 stories)

**Recovery:**
1. Split feature into 2 features
2. Identify natural breakpoint
3. Re-estimate each feature

---

## Output Template

```markdown
## Feature: {Name} (Epic: EPIC-001)

**Description:** {What and why}
**Acceptance:** {Completion criteria}
**Estimated Effort:** {Small/Medium/Large} ({story points})
**Dependencies:** {Other features required first}

**Stories (high-level):**
1. {Story 1 outline}
2. {Story 2 outline}
3. {Story 3 outline}
```

---

**Use this guide in Phase 4 (Epic & Feature Decomposition) to systematically break down epics into implementable features.**
