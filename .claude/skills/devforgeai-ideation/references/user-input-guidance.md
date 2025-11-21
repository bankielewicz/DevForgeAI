---
id: user-input-guidance
title: Framework-Internal Guidance Reference for User Input Elicitation
version: "1.0"
created: 2025-01-21
updated: 2025-01-21
status: Published
audience: DevForgeAI Skills (Internal Use)
related_document: effective-prompting-guide.md (user-facing counterpart)
---

# User Input Guidance Reference

**Purpose:** Framework-internal guidance document for DevForgeAI skills to elicit complete, unambiguous requirements from users. This document is NOT for end-users (see `effective-prompting-guide.md` for user-facing counterpart).

**Target Skills:**
- `devforgeai-ideation` (discovery phase, feasibility analysis)
- `devforgeai-story-creation` (acceptance criteria specification)
- `devforgeai-architecture` (context file creation, constraint validation)
- `devforgeai-ui-generator` (user requirement specification before design)
- `devforgeai-orchestration` (feature decomposition, scope clarification)

**Quick Links:**
- [Section 1: Overview & Navigation](#section-1-overview--navigation)
- [Section 2: Elicitation Patterns](#section-2-elicitation-patterns)
- [Section 3: AskUserQuestion Templates](#section-3-askuserquestion-templates)
- [Section 4: NFR Quantification Table](#section-4-nfr-quantification-table)
- [Section 5: Skill Integration Guide](#section-5-skill-integration-guide)
- [Section 6: Framework Terminology Reference](#section-6-framework-terminology-reference)

---

## Section 1: Overview & Navigation

### 1.1 Purpose and Scope

This document serves as a reference for DevForgeAI skills when users provide incomplete, ambiguous, or vague requirements. Rather than making assumptions, skills use these patterns and templates to ask clarifying questions that result in complete specifications.

**Key Principle:** "Ask, Don't Assume"
- As stated in CLAUDE.md, when ambiguity exists, skills explicitly ask for clarification
- This document provides the templates and patterns to do so systematically
- Result: Higher-quality first-pass outputs with minimal iteration

---

### 1.2 How Skills Should Use This Document

**5-Step Discovery Workflow:**

1. **Identify ambiguity type** - Which category does the missing information fall into?
   - Functional requirement (feature scope/behavior)
   - Non-functional requirement (performance/security/scalability)
   - Edge cases (boundary conditions, error handling)
   - Integration points (external dependencies, data flows)
   - Constraints (tech stack, compliance, cost)

2. **Select appropriate pattern** - Find pattern in Section 2 matching your ambiguity type

3. **Customize the template** - Adapt AskUserQuestion template from Section 3 to your context

4. **Ask the question** - Use AskUserQuestion tool with the customized template

5. **Document the answer** - Incorporate response into requirements/AC/context

> **Efficiency Tip:** Pre-load this document at skill startup via `Read` tool for quick reference access.

---

### 1.3 Document Structure Quick Reference

| Section | Purpose | Use Case | Key Resource |
|---------|---------|----------|--------------|
| **Section 2: Elicitation Patterns** | 15 patterns covering 5 requirement categories | Find the pattern matching your situation | Choose 1 of 15 patterns |
| **Section 3: AskUserQuestion Templates** | 28 copy-paste templates with YAML syntax | Generate clarifying questions | Choose 1 of 28 templates |
| **Section 4: NFR Quantification Table** | 15+ vague terms mapped to metrics | Quantify non-functional requirements | Reference table, quick lookup |
| **Section 5: Skill Integration Guide** | How each of 5 skills integrates this guidance | Understand skill-specific use cases | Skill-specific workflows |
| **Section 6: Framework Terminology Reference** | Links to CLAUDE.md definitions, context files | Validate terminology consistency | Compliance validation |

---

### 1.4 Quick Navigation By Workflow

**FINDING THE RIGHT PATTERN:**

| I have this problem | Look at this pattern | Use this template |
|-------------------|---------------------|-------------------|
| Feature scope unclear | Pattern 1 | FUN-007 |
| Feature too large for one story | Pattern 4 | FUN-007 |
| "Fast/responsive/scalable" without metrics | Pattern 5 or 7 | NFR-001 or NFR-003 |
| "Secure" without specific threat model | Pattern 6 | NFR-002 |
| Missing edge cases or error handling | Pattern 8 | EDGE-001 or EDGE-002 |
| External system dependencies unclear | Pattern 11 | INT-001 |
| Tech constraints not documented | Pattern 14 | CONST-001 |
| Timeline/budget unclear | Pattern 15 | CONST-002 |

---

### 1.5 Version Control and Updates

- **Current Version:** 1.0 (2025-01-21)
- **Status:** Published and stable

**Related Documents:**
- `effective-prompting-guide.md` - User-facing counterpart (what to tell users)
- `requirements-elicitation-guide.md` - Domain-specific patterns (E-commerce, SaaS, Fintech, Healthcare)
- `CLAUDE.md` - Framework constitution and core principles
- `.devforgeai/context/` - 6 immutable constraint files

**Feedback & Updates:**
To request updates to this guidance:
- File an issue with the pattern/template that didn't work
- Describe the ambiguity type and how it was identified
- Suggest improved question structure
- Share successful follow-up if user answered clarification

---

## Section 2: Elicitation Patterns

**15 patterns across 5 categories to identify and resolve ambiguities**

| Category | Patterns | Focus |
|----------|----------|-------|
| **Functional** | Patterns 1-4 | Feature scope, interpretations, solutions, decomposition |
| **Non-Functional** | Patterns 5-7 | Performance, security, scalability |
| **Edge Cases** | Patterns 8-10 | Invalid inputs, boundaries, validation |
| **Integration** | Patterns 11-13 | External systems, data contracts, error recovery |
| **Constraints** | Patterns 14-15 | Technical & business limits |

---

### 2.1 Functional Requirement Patterns

Functional requirements describe **WHAT** the system does—features, capabilities, user workflows.

**Quick Links:** [Pattern 1](#pattern-1-clarifying-feature-scope) | [Pattern 2](#pattern-2-separating-requirements-from-solutions) | [Pattern 3](#pattern-3-identifying-multiple-interpretations) | [Pattern 4](#pattern-4-decomposing-complex-features)

---

#### Pattern 1: Clarifying Feature Scope

**When to Use:** Feature description is vague or could mean multiple things

**Problem Description:**
User provides vague feature description that could mean multiple things. Example: "Add user management" could mean:
- Just login/logout?
- Full RBAC with team hierarchies?
- SSO integration with external systems?

**What to Do:**
Ask user to be specific about:
1. What user-related operations are in scope?
2. What operations are explicitly OUT of scope?
3. What user roles/types will exist?
4. What data is associated with each user type?

**Use Template:** `FUN-007` (Scope Definition)

**AskUserQuestion Template:**

```yaml
question: |
  "User management" could mean several different things. Let me clarify scope:

  1. User registration/login only?
  2. Team/organization hierarchies?
  3. Role-based access control (permissions)?
  4. External identity provider integration (SSO)?
  5. User profiles (preferences, settings)?

  Which of these are IN scope for this story?

header: "User Management Scope"
multiSelect: true
options:
  - label: "Authentication only (register, login, password reset)"
    description: "Users can create accounts and authenticate via email/password"

  - label: "Team/organization structure"
    description: "Users belong to teams/organizations with hierarchical relationships"

  - label: "Role-based access control"
    description: "Different user roles have different permissions within the system"

  - label: "SSO / External identity provider"
    description: "Users authenticate via external service (Google, Azure AD, SAML)"

  - label: "User profiles & preferences"
    description: "Users can configure settings, preferences, avatar, etc."
```

**Example (From DevForgeAI Context):**

STORY-048 (Production Cutover Documentation) initially said "update documentation" (vague).

Clarification questions revealed:
- Which docs? (README, API reference, deployment guide, user manual?)
- What format? (Markdown, HTML, PDF, interactive?)
- What audience? (Developers, operators, end-users?)
- Update what? (Add missing sections, fix errors, add examples?)

**Result:** Specific scope = "Update README (deployment section), API reference (new endpoints), operator guide (runbook updates)" - now testable.

**Customization Notes:**
- Adapt the multi-select options to your specific feature (swap "user management" for actual feature)
- Focus on IN/OUT scope distinction to prevent scope creep
- Use this pattern early in discovery phase (before design begins)

**Related Patterns:**
- Pattern 4: Decomposing Complex Features (break scope into testable pieces)
- Pattern 8: Discovering Missing Edge Cases (identify edge cases within scope)

---

#### Pattern 2: Separating Requirements from Solutions

**When to Use:** User suggests a specific solution instead of describing the business need

**Problem Description:**
User states a solution rather than a requirement. Examples:
- "Use Redis for caching" (solution) vs "API responses must return <200ms p95" (requirement)
- "Add a database" (solution) vs "Store user data with <100ms query time" (requirement)

**Why This Matters:**
1. Tech stack may already specify a different solution
2. Solution might not actually address the business need
3. Acceptance criteria become prescriptive instead of measurable

**What to Do:**
Identify the actual business need behind the proposed solution. Ask:
1. Why do you need [solution]?
2. What problem are you trying to solve?
3. What's the measurable success criteria?
4. Are there other ways to achieve this?

**Use Template:** `NFR-001, NFR-003, or NFR-004` (depending on specific concern)

**AskUserQuestion Template:**

```yaml
question: |
  I noticed you mentioned "[SOLUTION]". Let me clarify the underlying requirement:

  What problem or constraint are you trying to address?
  - Performance target? (response time, throughput)
  - Reliability/availability?
  - Cost reduction?
  - Scalability (number of users/requests)?
  - Data freshness/consistency?

  Knowing the goal helps me identify the best solution aligned with tech-stack.md.

header: "Requirement vs. Solution Clarification"
multiSelect: false
options:
  - label: "Performance target (response time, throughput, latency)"
    description: "Measurable goal: <200ms p95 latency or 10k requests/second"

  - label: "Reliability / Availability (uptime, fault tolerance)"
    description: "Measurable goal: 99.9% uptime, survive 3-node failure"

  - label: "Scalability (users, data volume, concurrent requests)"
    description: "Measurable goal: 100k concurrent users, 1TB data, 10k req/sec"

  - label: "Cost efficiency (infrastructure budget)"
    description: "Measurable goal: <$1000/month or <$5 per user/month"

  - label: "Data consistency / freshness"
    description: "Measurable goal: real-time, eventual consistency, or batch updates"
```

**Example (From DevForgeAI Context):**

STORY-007 (Post-Operation Retrospective) proposed "add conversation history storage" (solution).

Clarification revealed:
- **Actual requirement:** Users need to reference previous conversation context
- **Measurable goal:** Retrieve conversation within 1 second, 3-month retention
- **Tech-stack decision:** PostgreSQL (already in stack) better than Redis for this use case

**Customization Notes:**
- Replace `[SOLUTION]` with the specific solution user proposed
- Customize the problem categories to your domain (swap "conversation" for actual feature)
- Always map solution back to measurable requirement before implementation

**Related Patterns:**
- Pattern 5: Quantifying Vague Performance Terms (finding the right metric)
- Section 4: NFR Quantification Table (translates vague requirements to metrics)

---

#### Pattern 3: Identifying Multiple Interpretations

**When to Use:** Requirement has multiple valid interpretations that lead to different implementations

**Problem Description:**
Requirement could be interpreted multiple ways. Examples:
- "Create user authentication" could mean: session-based, token-based, OAuth, or multi-factor
- "Add search" could mean: full-text search, category filter, or faceted search
- "Store files" could mean: database BLOB, cloud storage, or file server

Without clarification, developer might implement wrong approach.

**Why This Matters:**
- Different interpretations require different tech and complexity
- Wrong interpretation causes rework and delays
- Early clarification prevents implementation waste

**What to Do:**
List the most common interpretations and ask user to select intended meaning.

**AskUserQuestion Template:**

```yaml
question: |
  "Authentication" can mean different approaches. Which best matches your intent?

  Consider: What authentication methods will users have?
  - Email/password with sessions (traditional web app)
  - JWT tokens (REST API, mobile app)
  - OAuth (social login integration)
  - Multi-factor authentication (security requirement)
  - API key authentication (service-to-service)

header: "Authentication Approach Clarification"
multiSelect: false
options:
  - label: "Session-based (email/password + cookies)"
    description: "Users login with email/password, server stores session in database or cache"

  - label: "Token-based (JWT or similar)"
    description: "Users receive stateless token after login, submit token with each request"

  - label: "OAuth / Social login"
    description: "Users authenticate via external provider (Google, GitHub, etc.)"

  - label: "Multi-factor authentication (email/password + 2FA)"
    description: "After password verification, users must confirm via second method (TOTP, SMS)"

  - label: "Combination (multiple methods supported)"
    description: "Support multiple authentication methods, user chooses preferred approach"
```

**Use Template:** `FUN-002` or `FUN-003` (depending on scope)

**Example (From DevForgeAI Context):**

STORY-001 (Initial Project Setup) said "add authentication" (ambiguous).

Clarification revealed:
- **Requirement:** REST API for backend services + web frontend
- **Implementation:** JWT tokens for API, session cookies for web frontend
- **Out of scope:** SSO integration or multi-factor auth (future stories)

**Customization Notes:**
- List 3-5 common interpretations based on domain knowledge
- Include complexity/effort indicators (e.g., "simplest," "standard," "most complex")
- Always clarify which interpretation user intends before design starts
- Document chosen interpretation in acceptance criteria

**Related Patterns:**
- Pattern 1: Clarifying Feature Scope (high-level scope vs. interpretation details)
- Pattern 4: Decomposing Complex Features (multiple interpretations → multiple stories)

---

#### Pattern 4: Decomposing Complex Features

**When to Use:** Feature is too large for a single story or sprint

**Problem Description:**
Feature is too large to fit in a single story. Examples:
- "Build e-commerce platform" = 20+ stories across multiple epics
- "Create admin dashboard" = too many features for one story
- "Implement payment system" = payment method selection + processing + reconciliation

Need to break into testable, completable pieces.

**Why This Matters:**
- Stories that are too large lead to incomplete implementations
- Easier to test and validate smaller stories
- Prevents scope creep and timeline slips
- Enables parallel development across multiple teams

**What to Do:**
1. Identify feature layers (auth → catalog → cart → checkout → payment → fulfillment)
2. Identify user workflows (guest vs. registered vs. admin)
3. Identify integration points (external APIs, data dependencies)
4. Ask user to prioritize which pieces go in first story (MVP)

**Use Template:** `FUN-007` (Scope Definition)

**AskUserQuestion Template:**

```yaml
question: |
  "[LARGE_FEATURE]" is a complex capability. Let me identify the minimal viable scope for this story.

  Which piece should THIS story focus on? (Other pieces become separate stories)
  - Core user workflow (happy path)
  - Admin capabilities
  - Integration with external system
  - Edge case handling
  - Performance/scalability tuning

header: "Feature Decomposition - Story Scope"
multiSelect: false
options:
  - label: "Happy path only (core user workflow, no error cases)"
    description: "Implement the main success scenario. Edge cases become separate stories."

  - label: "Happy path + key error cases"
    description: "Implement main workflow plus 2-3 critical error scenarios"

  - label: "Admin capabilities (backend management)"
    description: "Tools for administrators to configure/manage the feature"

  - label: "Integration with external system"
    description: "Connect to third-party service (payment processor, CRM, API)"

  - label: "Performance/scalability enhancements"
    description: "Optimize existing functionality for speed or scale"
```

**Use Template:** `FUN-007` (Scope Definition)

**Example (From DevForgeAI Context):**

STORY-052 (User-Facing Prompting Guide) originally included: guide + templates + examples + video tutorial + interactive tool.

Decomposed into multiple stories:
- **STORY-052:** Guide + text examples (Story #1 - MVP)
- **STORY-053:** Interactive template builder tool (Future story)
- **STORY-054:** Video tutorials (Future story)

Each story: clear AC, completable in 1 sprint, independently testable.

**Customization Notes:**
- Identify MVP piece that delivers core value (exclude nice-to-haves)
- Ask: "Which piece delivers value to users immediately?"
- Create separate story for each "future enhancement"
- Document dependencies between stories (which must be first?)
- Use this pattern early in epic planning phase

**Related Patterns:**
- Pattern 1: Clarifying Feature Scope (defining scope boundaries)
- Pattern 8: Discovering Missing Edge Cases (identify what's NOT in MVP)
- Pattern 15: Identifying Business Constraints (timeline may drive decomposition)

---

### 2.2 Non-Functional Requirement Patterns

Non-functional requirements describe **HOW WELL** or **HOW FAST** the system performs—performance, security, scalability.

**Quick Links:** [Pattern 5](#pattern-5-quantifying-vague-performance-terms) | [Pattern 6](#pattern-6-defining-security-requirements-precisely) | [Pattern 7](#pattern-7-specifying-scalability-targets)

---

#### Pattern 5: Quantifying Vague Performance Terms

**When to Use:** User says "make it fast" or "performance is important" without measurable targets

**Problem Description:**
User uses vague performance terms without metrics. Examples:
- "Fast" - could mean <100ms, <1s, or <10s?
- "Responsive" - user-perceived latency vs. actual server latency?
- "High performance" - throughput (requests/sec) or latency (milliseconds)?

**Why This Matters:**
- Without metrics, no way to validate if implementation succeeded
- Different targets require different architecture and cost
- Vague targets lead to over-engineering or under-delivering

**What to Do:**
Use Section 4 (NFR Quantification Table) to translate vague term → specific metric. Ask user to select specific targets.

**Use Template:** `NFR-001` (Performance Targets)

**AskUserQuestion Template:**

```yaml
question: |
  When you say "[VAGUE_TERM]", what measurable target do you have in mind?

  For example, "fast" could mean:
  - API response: <100ms, <200ms, <500ms, or <1s?
  - Page load: <2s, <3s, <5s?
  - Throughput: 100s/sec, 1000s/sec, 10000s/sec?

header: "Performance Target Clarification"
multiSelect: false
options:
  - label: "Tight performance target (<200ms latency, <5s page load)"
    description: "Critical user experience. Must optimize aggressively. Higher cost/complexity."

  - label: "Moderate performance target (200-500ms latency, 5-10s page load)"
    description: "Good user experience. Reasonable implementation. Standard approach."

  - label: "Relaxed performance target (500ms-1s latency, 10-15s page load)"
    description: "Acceptable for background tasks or less-critical paths. Simplest implementation."

  - label: "Other measurable target"
    description: "If you have a specific metric in mind (e.g., 10k requests/second)"
```

**Example (From DevForgeAI Context):**

STORY-048 (Production Cutover) required "fast deployment" (vague).

Clarification revealed:
- **Vague requirement:** "Fast deployment"
- **Specific targets:** Deploy to production within 30 minutes, rollback within 5 minutes
- **Measurable metrics:** Deployment script timeout = 30min, rollback button latency <5s

**Customization Notes:**
- Always use Section 4 table to find measurable ranges for vague term
- Include both latency (response time) and throughput (requests/sec) if relevant
- Account for percentiles (p50 vs. p95 vs. p99) for latency targets
- Document why specific target chosen (competitive requirement, user experience, infrastructure cost)

**Related Patterns:**
- Section 4: NFR Quantification Table (lookup vague term → measurable metrics)
- Pattern 6: Defining Security Requirements Precisely (security also needs metrics)
- Pattern 7: Specifying Scalability Targets (scale is related to performance)

---

#### Pattern 6: Defining Security Requirements Precisely

**When to Use:** User says "secure" or "needs security" without specific threat model or controls

**Problem Description:**
"Secure" means different things to different people. Examples:
- HTTPS only? Encryption at rest? Authentication? Authorization? Audit logging?
- Different data requires different protections (PII vs. public data vs. financial data)

**Why This Matters:**
1. Under-implementing security leaves vulnerabilities and compliance violations
2. Over-implementing security increases cost, complexity, and performance impact
3. Different data types have different regulatory requirements

**What to Do:**
Ask about specific threats and controls needed:
1. What data is sensitive? (PII, financial, health, trade secrets?)
2. What threats matter most? (data breach, unauthorized access, tampering, interception?)
3. What compliance applies? (GDPR, HIPAA, PCI-DSS, SOC2?)
4. What controls are required? (encryption, authentication, authorization, audit logging?)

**Use Template:** `NFR-002` (Security & Compliance)

**AskUserQuestion Template:**

```yaml
question: |
  "Secure" means different things depending on threats and compliance. Help me understand:

  1. What type of data will you store/transmit?
     - Personally identifiable info (PII)? → Affects GDPR/privacy requirements
     - Financial data? → Affects PCI-DSS requirements
     - Health information? → Affects HIPAA requirements
     - Trade secrets? → Affects confidentiality requirements

  2. What threats are most important to mitigate?

header: "Security & Compliance Requirements"
multiSelect: true
options:
  - label: "Data encryption (at rest and in transit)"
    description: "Encrypt sensitive data in database and during transmission. Requires: TLS 1.3 for transit, AES-256 for at rest."

  - label: "Authentication & authorization"
    description: "Verify user identity and control what they can access. Requires: Strong password hashing, role-based access control."

  - label: "Audit logging"
    description: "Log all access to sensitive data for compliance/forensics. Requires: Immutable audit log, user ID tracking."

  - label: "Regulatory compliance (GDPR/HIPAA/PCI-DSS)"
    description: "Meet specific regulatory framework requirements. Specify which applies."

  - label: "Data isolation / multi-tenancy"
    description: "Ensure customer data is isolated and not leakable to other customers"
```

**Example (From DevForgeAI Context):**

CLAUDE.md specifies baseline security requirements:
- No hardcoded secrets (use environment variables)
- Parameterized queries (prevent SQL injection)
- Input validation (prevent XSS)
- Strong cryptography (SHA256+, not MD5/SHA1)

These are framework-wide minimums. Additional requirements depend on data sensitivity and compliance.

**Customization Notes:**
- Distinguish between baseline security (applies to all) and data-specific security (PII, financial, health)
- Check relevant compliance frameworks (GDPR, HIPAA, PCI-DSS, CCPA, COPPA)
- Map threats to specific controls (data breach → encryption, unauthorized access → authentication)
- Document security requirements in architecture-constraints.md

**Related Patterns:**
- Pattern 5: Quantifying Vague Performance Terms (both need measurable metrics)
- Section 6: Framework Terminology Reference (for CLAUDE.md security rules)

---

#### Pattern 7: Specifying Scalability Targets

**When to Use:** User says "must be scalable" without specifying target scale

**Problem Description:**
"Scalable" means different things. Examples:
- 10 users? 1,000 users? 1 million users?
- 100 requests/second? 10,000 requests/second?
- 1 GB data? 1 TB? 1 PB?

Different targets require different architecture and cost.

**Why This Matters:**
- Scalability is expensive; specificity prevents over-engineering
- Infrastructure cost scales with target scale (don't pay for 1M users if you have 1k)
- Architecture choices depend on scale (single server → multi-server → distributed)

**What to Do:**
Ask about:
1. Expected user count now and in 2 years
2. Expected request rate at peak
3. Expected data volume
4. When scalability becomes critical (day 1 launch or gradual growth?)

**Use Template:** `NFR-003` (Scalability & Growth)

**AskUserQuestion Template:**

```yaml
question: |
  When you say "scalable", what scale are we targeting?

  Need to know:
  - How many users at launch? In 2 years?
  - Peak requests per second at launch? In 2 years?
  - Data volume at launch? In 2 years?
  - When does it need to handle scale: day 1 or gradual growth?

header: "Scalability Target Clarification"
multiSelect: false
options:
  - label: "Small scale (10-100 users, 10-100 req/sec)"
    description: "Single-server architecture acceptable. Low infrastructure cost."

  - label: "Medium scale (100-10,000 users, 100-1000 req/sec)"
    description: "Horizontal scaling with load balancer. Multiple servers. Database replication."

  - label: "Large scale (10k-1M users, 1k-10k req/sec)"
    description: "Distributed architecture with caching, sharding, global CDN. Complex infrastructure."

  - label: "Massive scale (1M+ users, 10k+ req/sec)"
    description: "Cloud-native architecture with auto-scaling, multi-region deployment. Enterprise infrastructure."

  - label: "Gradual scaling (start small, grow over time)"
    description: "Architecture must support growth, but doesn't need max scale on day 1"
```

**Example (From DevForgeAI Context):**

DevForgeAI framework itself has scalability targets:
- **Storage:** Supports up to 1000 stories/epics per project (fits in GitHub)
- **Token efficiency:** Commands must complete in <25K tokens (context window limits)
- **Concurrency:** Max 5 parallel skill invocations (Bash session limits)

These targets drove architectural decisions (file-based storage vs. database, token budgets per command).

**Customization Notes:**
- Distinguish between "launch day" scale and "growth target" (different architectures)
- Ask about seasonal/peak vs. average load patterns
- Consider both user scale and data volume (100k users × 10 records each = scale problem)
- Document scalability targets in non-functional requirements section

**Related Patterns:**
- Pattern 5: Quantifying Vague Performance Terms (latency vs. throughput vs. scale)
- Section 4: NFR Quantification Table (scalability metrics reference)

---

### 2.3 Edge Case Patterns

Edge cases describe **unexpected or boundary scenarios**—what happens when things go wrong or limits are reached.

**Quick Links:** [Pattern 8](#pattern-8-discovering-missing-edge-cases) | [Pattern 9](#pattern-9-handling-graceful-degradation) | [Pattern 10](#pattern-10-identifying-data-validation-rules)

---

#### Pattern 8: Discovering Missing Edge Cases

**When to Use:** User specifies happy path but doesn't mention error cases or boundary conditions

**Problem Description:**
User specifies happy path but not edge cases. Examples:
- User creates account (happy path) - what if email already exists?
- User uploads image (happy path) - what if file too large? Wrong format?
- User pays for item (happy path) - what if payment fails?
- Add to cart (happy path) - what if item out of stock? Quantity exceeds stock?

Incomplete edge case handling causes production bugs, support load, and unhappy users.

**Why This Matters:**
- Edge cases represent 80% of real-world usage (not just happy path)
- Missing error handling leads to poor user experience and support costs
- Edge cases often cause security vulnerabilities

**What to Do:**
Systematically ask about:
1. Invalid inputs (empty, wrong format, too large)
2. Boundary conditions (zero, max value, null)
3. Concurrent operations (two users accessing same resource)
4. Resource exhaustion (disk full, quota exceeded)
5. External failures (API timeout, database down)

**Use Template:** `EDGE-001, EDGE-002, or EDGE-003` (depending on type)

**AskUserQuestion Template:**

```yaml
question: |
  Good spec includes happy path + edge cases. For "[FEATURE]", what happens when:

  1. Invalid inputs? (empty, wrong format, too large)
  2. Boundary conditions? (zero items, max value, null)
  3. Concurrent operations? (two users updating same resource)
  4. Resource exhaustion? (disk full, quota exceeded)
  5. External failures? (API timeout, database down)

  Which of these are likely? Should we handle them explicitly?

header: "Edge Case Handling"
multiSelect: true
options:
  - label: "Invalid input validation (empty, wrong format, type checks)"
    description: "Validate all inputs. Return error message if invalid. Log violation for security."

  - label: "Boundary conditions (zero, negative, max value, null)"
    description: "Handle edge values. Example: prevent zero quantity in order, enforce min/max lengths."

  - label: "Concurrent/race conditions (simultaneous updates)"
    description: "Handle when multiple users access same resource. Use locking, versioning, or queuing."

  - label: "Resource exhaustion handling (quota limits, rate limits)"
    description: "Prevent abuse. Enforce rate limits, quota checks, graceful degradation when resources full."

  - label: "External failure recovery (timeout, retry, fallback)"
    description: "Handle when external API/database fails. Implement retry logic, fallback behavior, error messages."
```

**Example (From DevForgeAI Context):**

STORY-053 (User Input Guidance) specifies "elicit complete requirements" (happy path).

Edge cases identified:
- User provides non-English requirements → translate or ask for English?
- User provides contradictory requirements → ask for clarification?
- User provides solution instead of requirement → redirect to actual requirement?
- User has incomplete context → ask discovery questions to fill gaps?

All handled by specific patterns in this document.

**Customization Notes:**
- Always ask about error cases alongside happy path
- Use systematic checklist: invalid inputs, boundaries, concurrency, exhaustion, external failures
- Document edge cases as separate acceptance criteria
- Write tests for edge cases (not just happy path)
- Consider security implications of edge cases

**Related Patterns:**
- Pattern 9: Handling Graceful Degradation (what happens at resource limits)
- Pattern 10: Identifying Data Validation Rules (validation for edge case data)

---

#### Pattern 9: Handling Graceful Degradation

**When to Use:** Need to define behavior when system reaches capacity or encounters failures

**Problem Description:**
What happens when system reaches its limits? Examples:
- All database connections in use - queue requests, reject, or retry?
- Memory/storage full - fail, drop non-critical requests, or reduce features?
- Third-party API down - fail immediately, queue for retry, or fallback?

Without explicit handling, system crashes under load or degrades poorly.

**Why This Matters:**
- Graceful degradation maintains user experience even under stress
- Different features have different priorities for resource allocation
- Explicitly defining behavior prevents chaotic failure modes

**What to Do:**
Ask about behavior at limits and prioritization of features/users.

**Use Template:** `EDGE-003` (Rate Limiting & Quotas)

**AskUserQuestion Template:**

```yaml
question: |
  When the system reaches capacity limits, how should it behave?

  For "[FEATURE]":
  - What is the capacity limit? (max concurrent users, max requests/sec, storage quota)
  - When limit is reached, should we: queue requests, reject gracefully, reduce features, prioritize users?
  - How long can users wait? (real-time <1s, near-real-time <30s, batch OK)

header: "Graceful Degradation Strategy"
multiSelect: false
options:
  - label: "Strict capacity enforcement (reject requests when full)"
    description: "Return error when at capacity. Users retry later. Ensures quality for accepted requests."

  - label: "Queue requests (accept but process in order)"
    description: "Buffer excess requests. Process in FIFO order. Increases latency but no requests lost."

  - label: "Reduce features (graceful degradation)"
    description: "Keep core features, reduce non-essential. Example: search works, autocomplete disabled."

  - label: "Prioritize users (premium users get resources)"
    description: "Paid/premium users get priority. Free tier users may experience delays."

  - label: "Fail completely (crash hard)"
    description: "System goes down when overloaded. NOT RECOMMENDED for production. Worst UX."
```

**Example (From DevForgeAI Context):**

DevForgeAI /dev command has resource limits:
- **Max token budget:** 100K per invocation
- **Max execution time:** 30 minutes
- **Max AI subagent depth:** 3 levels

When limits reached:
- **Behavior:** Graceful degradation → defer remaining tests/validation to next sprint
- **Not:** Fail completely or crash

This strategy keeps developer productive while respecting resource constraints.

**Customization Notes:**
- Identify which features are critical vs. optional (prioritization)
- Define clear thresholds (when does degradation start?)
- Choose appropriate degradation mode (queue, reduce features, reject)
- Plan fallback communication (inform user when degraded)

**Related Patterns:**
- Pattern 8: Discovering Missing Edge Cases (capacity limits are edge cases)
- Pattern 9: Handling Graceful Degradation (related degradation strategies)

---

#### Pattern 10: Identifying Data Validation Rules

**When to Use:** Need to specify what data is valid and what should be rejected

**Problem Description:**
What data is valid and what is not? Examples:
- Email must be valid format (RFC 5322)
- Phone must be 10 digits (US) or +XX format (international)
- Password must be 8+ characters, with uppercase, lowercase, number, special char
- URL must be valid HTTP/HTTPS URL
- Age must be 18-120
- Name cannot be blank

Without clear validation rules, inconsistent/invalid data gets stored.

**Why This Matters:**
- Invalid data causes downstream bugs and crashes
- Clear validation rules enable early error detection and better UX
- Validation is part of security (prevent XSS, SQL injection, etc.)

**What to Do:**
For each input field, identify:
1. Required or optional?
2. Data type (string, number, date, etc.)
3. Length/size constraints (min/max)
4. Format constraints (regex, valid values, etc.)
5. Conditional rules (if A, then B is required)

**Use Template:** `EDGE-001` (Input Validation)

**AskUserQuestion Template:**

```yaml
question: |
  Let me clarify data validation rules for "[ENTITY]".

  For each field, specify:
  - Required or optional?
  - Min/max length or range?
  - Format (email, phone, URL, date format)?
  - Valid values (enum)?
  - Conditional rules?

header: "Data Validation Rules"
multiSelect: false
options:
  - label: "Specify validation for each field individually"
    description: "I'll ask about each field's constraints (required, format, range, etc.)"

  - label: "Keep it simple (basic type checking, no advanced validation)"
    description: "Accept any string/number/date. Minimal format validation. Easier to implement."

  - label: "Strict validation (all constraints enforced)"
    description: "All rules validated on both client and server. Reject invalid data early."

  - label: "Progressive validation (basic validation now, advanced later)"
    description: "Validate basic rules in MVP. Add advanced rules in future story."
```

**Example (From DevForgeAI Context):**

CLAUDE.md specifies baseline validation requirements:
- **Input validation:** Prevent XSS, SQL injection
- **Data validation:** Parameterized queries, type checking
- **Security validation:** Strong passwords, secure tokens

Story-specific validation examples:
- Story ID format: `STORY-\d{3}` (STORY-001, STORY-052, etc.)
- Email format: RFC 5322 compliance
- Token refresh interval: 24 hours (documented in story AC)

**Customization Notes:**
- Always include validation rules in acceptance criteria
- Specify error messages for each validation failure (improves UX)
- Consider both client-side validation (UX) and server-side validation (security)
- Test invalid inputs as part of edge case testing

**Related Patterns:**
- Pattern 8: Discovering Missing Edge Cases (validation is edge case handling)
- Pattern 10: Identifying Data Validation Rules (companion pattern for constraints)

---

### 2.4 Integration Point Patterns

Integration patterns describe **how this feature connects** to other systems, data flows, and dependencies.

**Quick Links:** [Pattern 11](#pattern-11-finding-external-system-dependencies) | [Pattern 12](#pattern-12-clarifying-data-contract-requirements) | [Pattern 13](#pattern-13-defining-error-recovery-procedures)

---

#### Pattern 11: Finding External System Dependencies

**When to Use:** Feature requires integration with external services or APIs

**Problem Description:**
Feature might depend on external systems not yet specified. Examples:
- Payment processing (Stripe, PayPal, Square)
- Email delivery (SendGrid, AWS SES, etc.)
- SMS notifications (Twilio, etc.)
- Cloud storage (S3, GCS, Azure Blob)
- Analytics (Segment, Mixpanel, etc.)
- Authentication (Auth0, Okta, etc.)

Without identifying dependencies early, implementation hits blockers during integration work.

**Why This Matters:**
- External service SLAs affect overall system reliability
- Some integrations require special compliance (PCI-DSS for payments, HIPAA for health data)
- Late discovery of missing dependencies causes rework and delays

**What to Do:**
Systematically ask about:
1. What data needs to flow outside the system?
2. What services are called/integrated?
3. Are integrations critical (system fails if down) or optional (graceful fallback)?
4. What SLA/reliability is needed from external service?

**Use Template:** `INT-001` (External API Integration)

**AskUserQuestion Template:**

```yaml
question: |
  Does this feature need to integrate with external systems or services?

  Common integrations:
  - Payments (Stripe, PayPal, Square, payment processor)
  - Email/SMS (SendGrid, Twilio, AWS SNS)
  - Cloud storage (S3, GCS, Azure Blob)
  - Identity/auth (Auth0, Okta, Google, GitHub)
  - Analytics (Segment, Mixpanel, Amplitude)
  - CRM (Salesforce, HubSpot)
  - Other APIs?

header: "External System Dependencies"
multiSelect: true
options:
  - label: "Payment processing (Stripe, PayPal, etc.)"
    description: "Process credit cards or other payment methods. Requires PCI-DSS compliance."

  - label: "Email delivery (SendGrid, AWS SES, etc.)"
    description: "Send transactional or marketing emails. Requires email template design."

  - label: "SMS/push notifications (Twilio, AWS SNS, etc.)"
    description: "Send text messages or push notifications. Requires rate limiting."

  - label: "Cloud storage (S3, GCS, Azure Blob)"
    description: "Store files (images, documents). Requires lifecycle/retention policies."

  - label: "Analytics or data warehouse"
    description: "Track user behavior or business metrics. Requires data schema design."

  - label: "External API integration"
    description: "Call third-party API for data or functionality. Specify which API."
```

**Example (From DevForgeAI Context):**

DevForgeAI /release command integrates with:
- **Git** (version control)
- **GitHub** (code repository, if using GitHub)
- **Bash/CLI tools** (deployment scripts)

Not integrated (by design):
- Cloud providers (AWS, Azure, GCP) - left to user's deployment script
- CI/CD systems (GitHub Actions, Jenkins) - left to user's pipeline

This dependency list is documented in tech-stack.md and deployment/.

**Customization Notes:**
- Identify critical vs. optional dependencies (critical → need error recovery)
- Document each external service with: name, purpose, SLA, compliance requirements
- Consider cost of integrations (some services charge per request)
- Plan for dependency fallback or graceful degradation

**Related Patterns:**
- Pattern 12: Clarifying Data Contract Requirements (what data flows)
- Pattern 13: Defining Error Recovery Procedures (failure modes for dependencies)

---

#### Pattern 12: Clarifying Data Contract Requirements

**When to Use:** Two systems exchange data but format/schema not yet specified

**Problem Description:**
Unclear data contracts between systems. Examples:
- Frontend sends payment request to backend - what fields? what format (XML, JSON)?
- Backend sends response - success/error format? what fields?
- Third-party API returns data - what fields, data types, rate limits?

Without clear data contracts, integration becomes painful and error-prone.

**Why This Matters:**
- Ambiguous contracts cause integration bugs and compatibility issues
- Clear contracts enable parallel development (frontend vs. backend can work independently)
- Data contracts are foundation for testing and validation

**What to Do:**
Ask for:
1. What data gets exchanged?
2. What format (JSON, XML, Protocol Buffers, CSV)?
3. What's required vs optional?
4. What happens if field is missing?
5. What validation happens at contract boundary?

**Use Template:** `INT-002` (Webhook & Event Handling) or `INT-003` (Data Synchronization)

**AskUserQuestion Template:**

```yaml
question: |
  Let me clarify the data contract for "[INTEGRATION_POINT]".

  What data needs to flow from [SYSTEM_A] to [SYSTEM_B]?

  Need to specify:
  - Field names and data types
  - Required vs optional fields
  - Format (JSON, XML, CSV)
  - Example request/response
  - Error scenarios

header: "Data Contract Specification"
multiSelect: false
options:
  - label: "Simple contract (5-10 fields, JSON format)"
    description: "Straightforward request/response. Standard JSON. Examples: { userId, action }"

  - label: "Complex contract (20+ fields, nested objects)"
    description: "Complex data structure with nested objects/arrays. Requires schema documentation."

  - label: "Streaming contract (continuous data flow)"
    description: "Real-time data stream (events, messages, webhooks). Requires message format spec."

  - label: "File-based contract (exchange files)"
    description: "Import/export files (CSV, JSON, XML). Requires file format specification."
```

**Example (From DevForgeAI Context):**

STORY-052 & STORY-053 have data contracts:

**Input Contract (User → Framework):**
```yaml
business_idea: string (100+ words describing problem/opportunity)
current_state: string (50+ words, optional)
constraints: list of strings (tech preferences, compliance, timeline)
```

**Output Contract (Framework → User):**
```yaml
requirements: list of structured requirements
user_personas: list of persona descriptions
acceptance_criteria: list of testable criteria
technical_constraints: list of constraints
```

These contracts enable consistent input/output across skill invocations.

**Customization Notes:**
- Document data contracts in API documentation or acceptance criteria
- Include example request/response payloads in AC
- Specify error response formats (what does error look like?)
- Plan for contract versioning (how to handle breaking changes?)

**Related Patterns:**
- Pattern 11: Finding External System Dependencies (where data flows)
- Pattern 13: Defining Error Recovery Procedures (error formats in contract)

---

#### Pattern 13: Defining Error Recovery Procedures

**When to Use:** Integration might fail and need recovery procedure

**Problem Description:**
What happens when integration fails? Examples:
- Payment processor API times out - retry? How many times? After how long?
- Email delivery fails - queue for retry? How long to wait?
- Database connection drops - fail immediately or use connection pool recovery?

Without recovery procedures, integrations fail silently or crash dramatically.

**Why This Matters:**
- Recovery procedures prevent cascading failures (one service down ≠ whole system down)
- Clear retry policies prevent overwhelming external services
- Alerting ensures operators know about issues quickly

**What to Do:**
For each integration point, specify:
1. Failure detection (how do we know it failed?)
2. Recovery strategy (retry, queue, fallback, circuit breaker?)
3. Retry policy (how many attempts? exponential backoff?)
4. Fallback behavior (what do we do if recovery fails?)
5. Alerting (how do we notify operators?)

**Use Template:** `INT-001` (External API Integration)

**AskUserQuestion Template:**

```yaml
question: |
  When integration with "[EXTERNAL_SERVICE]" fails, how should we recover?

  Define:
  - Failure detection: How do we know it failed? (timeout, HTTP 5xx, exception)
  - Retry strategy: How many attempts? How long between retries?
  - Fallback behavior: What do we do if all retries fail?
  - Alerting: How do we notify operators that something is broken?

header: "Error Recovery & Resilience"
multiSelect: false
options:
  - label: "Simple retry (3 attempts, 1-second delays)"
    description: "Try 3 times with 1-second delay between attempts. Fail gracefully if all fail."

  - label: "Exponential backoff (3-5 attempts, increasing delays)"
    description: "Try multiple times with increasing delays (1s, 2s, 4s, 8s). Handle timeouts."

  - label: "Queue for async retry (buffer requests, process later)"
    description: "Accept request, queue for later retry. Return immediately. Process when service recovers."

  - label: "Circuit breaker (stop trying if too many failures)"
    description: "After N failures, stop trying temporarily. Fail fast. Check periodically if service recovered."

  - label: "Graceful fallback (use alternative or reduced functionality)"
    description: "If primary fails, use backup service or reduce features. Example: no payment → no order."
```

**Example (From DevForgeAI Context):**

DevForgeAI /dev skill has error recovery strategies:

- **Test failure:** Retry test up to 3x with exponential backoff
- **Subagent timeout:** Return partial results, defer remaining work
- **Git operation failure:** Abort transaction, preserve user files, ask for manual intervention
- **Context file missing:** Fail immediately with clear error message (context is critical)

Recovery strategy depends on impact: critical → fail fast, non-critical → retry/queue.

**Customization Notes:**
- Define retry strategy for each integration: exponential backoff, fixed delay, or circuit breaker
- Set clear retry limits (prevent infinite loops)
- Design fallback behavior that maintains user experience (degrade gracefully)
- Plan operator alerting (how will ops know about failures?)

**Related Patterns:**
- Pattern 11: Finding External System Dependencies (recovery for dependencies)
- Pattern 9: Handling Graceful Degradation (fallback behavior)

---

### 2.5 Constraint Patterns

Constraint patterns identify **limits, rules, and non-negotiable factors** that shape implementation.

**Quick Links:** [Pattern 14](#pattern-14-discovering-hidden-technical-constraints) | [Pattern 15](#pattern-15-identifying-business-constraints)

---

#### Pattern 14: Discovering Hidden Technical Constraints

**When to Use:** Need to identify technical limits, locked technologies, or architecture requirements

**Problem Description:**
Project has implicit constraints not yet mentioned. Examples:
- Tech stack locked (can't use new database)
- Architecture pattern required (must use microservices or monolith)
- Security policies (must encrypt all data)
- Compliance requirements (GDPR, HIPAA, SOC2)
- Performance budgets (must fit in token limits)
- Cost limits (must stay under budget)

Without identifying constraints early, implementation violates unwritten rules late in development.

**Why This Matters:**
- Hidden constraints cause rework and delays when discovered late
- Some constraints are immutable (compliance, security, locked tech)
- Early constraint identification enables better architecture decisions

**What to Do:**
Ask explicitly about:
1. What technologies are locked (from tech-stack.md)?
2. What architecture patterns are required (from architecture-constraints.md)?
3. What security policies apply (from project)?
4. What compliance is required (industry/regulation)?
5. What resource budgets exist (cost, tokens, time)?

**Use Template:** `CONST-001` (Technical Stack & Architecture)

**AskUserQuestion Template:**

```yaml
question: |
  Before I proceed, need to align on technical constraints:

  1. Are there locked technologies in tech-stack.md? (affects language, framework choices)
  2. Are there architecture patterns required? (monolith vs. microservices, layering rules)
  3. What security/compliance requirements exist? (GDPR, encryption, audit logging)
  4. What resource budgets apply? (cost, token limit, execution time)
  5. Are there existing systems this must integrate with?

header: "Technical Constraints & Context Files"
multiSelect: true
options:
  - label: "Check tech-stack.md (locked technologies)"
    description: "Framework prevents using unapproved libraries. Identify locked tech first."

  - label: "Check architecture-constraints.md (layering rules)"
    description: "Framework enforces clean architecture. Understand layer boundaries."

  - label: "Check anti-patterns.md (forbidden patterns)"
    description: "Framework prevents common mistakes. Know what's forbidden."

  - label: "Check source-tree.md (file location rules)"
    description: "Framework has conventions. New files go in specific locations."

  - label: "Check dependencies.md (approved packages & versions)"
    description: "Framework locks package versions. Prevents version conflicts."
```

**Example (From DevForgeAI Context):**

DevForgeAI has framework-level constraints documented in context files:

**tech-stack.md:**
- Languages: Python, JavaScript/TypeScript, C#, Go, Java (framework-agnostic)
- Git: Required for /dev command (enforced in Phase 0)
- API style: REST (for web), not GraphQL (not in stack)
- Database: Project-specific (documented in context)

**architecture-constraints.md:**
- Layering: Infrastructure → Application → Domain (dependency flow)
- No direct instantiation: Use dependency injection
- Repository pattern: For data access abstraction

**anti-patterns.md:**
- No God Objects (classes >500 lines)
- No hardcoded secrets
- No SQL string concatenation

These constraints are IMMUTABLE - violations block commit/release.

**Customization Notes:**
- Always check context files (tech-stack.md, architecture-constraints.md) before design
- Document why constraints exist (compliance, performance, maintainability)
- Distinguish immutable constraints (can't violate) from guidelines (strongly recommended)
- Ask for exception process if constraint needs to be violated (requires ADR)

**Related Patterns:**
- Pattern 15: Identifying Business Constraints (cost, timeline, scope)
- Section 6: Framework Terminology Reference (links to CLAUDE.md and context files)

---

#### Pattern 15: Identifying Business Constraints

**When to Use:** Need to clarify business-level limits, deadlines, or priorities

**Problem Description:**
Feature has business limitations not yet mentioned. Examples:
- Timeline (must be done by specific date or flexible?)
- Budget (max cost for implementation?)
- Scope priority (must have vs. nice to have?)
- Stakeholder approval (requires sign-off?)
- Launch readiness (go/no-go criteria?)

Without business constraints, scope creeps and timeline slips.

**Why This Matters:**
- Timeline constraints drive technology choices (tight timeline → simpler tech)
- Budget constraints drive scope decisions (low budget → MVP only)
- Stakeholder approval can block launch or require rework

**What to Do:**
Ask explicitly about:
1. When is this needed? (launch date, sprint deadline?)
2. How much can we spend? (development cost, infrastructure cost?)
3. What's must-have vs. nice-to-have?
4. Who approves before launch?
5. What defines success?

**Use Template:** `CONST-002` (Timeline & Priority)

**AskUserQuestion Template:**

```yaml
question: |
  Help me understand the business constraints for this feature:

  1. Timeline: When is this needed? (hard deadline vs. flexible)
  2. Budget: Cost limits? (development effort, infrastructure cost)
  3. Scope: What's must-have vs. nice-to-have?
  4. Approval: Who needs to sign off before launch?
  5. Success: What defines a successful launch? (user adoption, revenue, etc.)

header: "Business Constraints & Success Criteria"
multiSelect: false
options:
  - label: "Tight timeline (must launch within 2 weeks)"
    description: "Hard deadline. Scope must be minimized. Quick iterations required."

  - label: "Flexible timeline (target 4-8 weeks)"
    description: "Can add polish and test thoroughly. Standard sprint duration."

  - label: "Long timeline (12+ weeks)"
    description: "Can plan multiple phases and complex features. Gradual rollout."

  - label: "Minimal MVP (launch quickly with core features only)"
    description: "Get to market fast. Additional features in follow-up stories."

  - label: "Full-featured launch (all planned features in v1.0)"
    description: "More complete but longer timeline. Higher risk of delays."
```

**Example (From DevForgeAI Context):**

STORY-048 (Production Cutover) had business constraints:
- **Timeline:** "Must be production-ready by Jan 31, 2025" (hard deadline)
- **Scope:** "Distribution package + documentation + runbook" (defined must-haves)
- **Success:** "All 3 components in place with zero rollback events" (measurable)

These constraints shaped the story's scope and acceptance criteria.

**Customization Notes:**
- Map business constraints to technical implications (tight timeline → simpler architecture)
- Document trade-offs (cost vs. quality, timeline vs. scope, features vs. stability)
- Ensure stakeholders understand constraints (and trade-offs)
- Plan for constraint changes (how to handle if deadline slips?)

**Related Patterns:**
- Pattern 4: Decomposing Complex Features (scope negotiation based on timeline)
- Pattern 5: Quantifying Vague Performance Terms (resource constraints have metrics)
- Pattern 14: Discovering Hidden Technical Constraints (tech constraints + business constraints)

---

## Section 3: AskUserQuestion Templates

**28 copy-paste-ready YAML templates for the 5 categories of elicitation questions.**

Use these templates with the `AskUserQuestion` tool. Each template:
- Includes the exact YAML syntax needed
- Can be customized by replacing placeholders like [SOLUTION] or [FEATURE]
- Follows the same structure (question, header, multiSelect, options)

**Quick Access by Type:**
- **Functional (FUN-001 to FUN-008):** User goals, roles, scope, interactions
- **Non-Functional (NFR-001 to NFR-005):** Performance, security, scalability, cost
- **Edge Cases (EDGE-001 to EDGE-004):** Validation, boundaries, rate limits, consistency
- **Integration (INT-001 to INT-003):** External APIs, webhooks, data sync
- **Constraints (CONST-001, CONST-002):** Technical stack, timeline & priority

### 3.1 Functional Requirement Templates (8 templates)

**FUN-001 through FUN-008: Clarify feature scope, user goals, interactions, and success criteria**

---

#### Template FUN-001: Primary User Goal

```yaml
question: |
  Let's clarify the primary user goal for this feature.

  Who will use this, and what problem does it solve for them?

  Be specific: "marketing managers can create email campaigns" is better than "add email feature"

header: "User Goal & Value"
multiSelect: false
options:
  - label: "I have a specific user role and goal in mind"
    description: "I'll describe the user role, their current pain point, and how this feature solves it"

  - label: "I'm not sure - help me identify the user goal"
    description: "Describe your business problem, I'll help identify the user role and goal"
```

#### Template FUN-002: User Roles and Permissions

```yaml
question: |
  Which user roles need to interact with this feature?

  Different roles might have different capabilities:
  - Basic user (limited permissions)
  - Admin user (full permissions)
  - Moderator (subset of permissions)
  - Guest (read-only)

header: "User Roles and Access Levels"
multiSelect: true
options:
  - label: "Single user role (everyone has same permissions)"
    description: "Simpler implementation. All users can do all actions."

  - label: "Two roles (basic user + admin)"
    description: "Standard pattern. Users have basic permissions, admins can configure."

  - label: "Three+ roles (basic, moderator, admin)"
    description: "Complex permissions. Need role hierarchy and capability matrix."

  - label: "Not sure - recommend based on use case"
    description: "Describe the use case, I'll recommend appropriate role structure"
```

#### Template FUN-003: Success Behaviors

```yaml
question: |
  What behaviors demonstrate that this feature is working correctly?

  Think: "Success means when a user... [does action], then [result happens]"

  At least 3-5 specific scenarios help define acceptance criteria.

header: "Success Scenarios (Happy Path)"
multiSelect: false
options:
  - label: "I have 3-5 specific scenarios in mind"
    description: "I can describe: user action → expected system response for each scenario"

  - label: "I have the general goal but not specific scenarios"
    description: "Describe the goal, I'll help develop specific success scenarios"

  - label: "I'm not sure what scenarios to consider"
    description: "Describe the use case, I'll ask discovery questions to identify scenarios"
```

#### Template FUN-004: Failure / Error Scenarios

```yaml
question: |
  What should happen when things go wrong?

  Consider:
  - Invalid user input (wrong format, missing required field)
  - Resource not found (user deleted, permissions revoked)
  - Concurrent conflicts (two users edit same resource)
  - External failures (API timeout, database down)

header: "Error Handling & Failure Scenarios"
multiSelect: true
options:
  - label: "Show user-friendly error message"
    description: "Display message explaining what went wrong and how to fix it"

  - label: "Log error for debugging / audit trail"
    description: "Record error details for investigation and compliance"

  - label: "Retry automatically (for transient failures)"
    description: "Try again if error is temporary (timeout, network glitch)"

  - label: "Graceful degradation (reduce features, stay operational)"
    description: "Keep system working even if non-critical functionality fails"

  - label: "Reject request (fail fast for invalid input)"
    description: "Return error immediately rather than processing invalid data"
```

#### Template FUN-005: Feature Interactions

```yaml
question: |
  How does this feature interact with other system features?

  Consider:
  - Does it use data from other features? (users, products, payments)
  - Does it trigger actions in other features? (email notification, audit logging)
  - Does it depend on other features? (can't work without X)

header: "Feature Dependencies & Interactions"
multiSelect: true
options:
  - label: "This feature reads data from other features"
    description: "Gets user info, product catalog, historical data, etc."

  - label: "This feature writes/modifies data affecting other features"
    description: "Creates users, updates product inventory, changes permissions"

  - label: "This feature triggers actions in other features"
    description: "Sends notifications, updates analytics, triggers workflows"

  - label: "This feature depends on other features working correctly"
    description: "Cannot function if auth, database, or other critical feature fails"

  - label: "This feature is standalone (minimal dependencies)"
    description: "Works independently with minimal integration"
```

#### Template FUN-006: Content/Data Management

```yaml
question: |
  What data or content will users create or manage with this feature?

  For example:
  - Create/edit/delete operations?
  - Search or filter through data?
  - Export or import data?
  - Archive old data?

header: "Data Management Operations"
multiSelect: true
options:
  - label: "Create new (users can create new items)"
    description: "Support creating: form submission, data entry, import"

  - label: "Read/view (users can see existing data)"
    description: "Support viewing: list, detail views, search, filters"

  - label: "Update/edit (users can modify existing items)"
    description: "Support editing: inline edit, form submission, bulk operations"

  - label: "Delete (users can remove items)"
    description: "Support deletion: single-item delete, bulk delete, soft-delete (archive)"

  - label: "Bulk operations (manage multiple items at once)"
    description: "Support: bulk import, bulk export, bulk update, bulk delete"
```

#### Template FUN-007: Scope Definition (In vs. Out)

```yaml
question: |
  To prevent scope creep, let me clarify what's IN scope and OUT of scope for this story.

  Is this single story or should it be multiple stories?

header: "Story Scope Boundaries"
multiSelect: false
options:
  - label: "IN scope: happy path only. OUT scope: error cases, admin features, edge cases"
    description: "Minimal scope. Implement main success scenario. Errors/edge cases → future stories."

  - label: "IN scope: happy path + key error cases. OUT scope: admin features, advanced options"
    description: "Moderate scope. Handle common errors. Advanced features → future stories."

  - label: "IN scope: happy path + errors + admin features. OUT scope: optimizations, future enhancements"
    description: "Full scope. Complete feature with admin controls. Optimizations → future stories."

  - label: "Not sure - help me identify the right scope"
    description: "Describe your feature, I'll recommend breaking it into multiple stories"
```

#### Template FUN-008: Integration with Third-Party Systems

```yaml
question: |
  Does this feature need to integrate with external systems or APIs?

  Examples:
  - Payment processor (Stripe, PayPal)
  - Email service (SendGrid)
  - Cloud storage (S3)
  - Identity provider (Auth0, GitHub)

header: "Third-Party System Integrations"
multiSelect: true
options:
  - label: "Payment processing (credit cards, digital wallets)"
    description: "Requires PCI-DSS compliance and payment provider integration"

  - label: "Email/SMS communication"
    description: "Transactional emails or SMS notifications"

  - label: "Cloud storage (files, images, documents)"
    description: "Store files outside the database (S3, GCS, Azure Blob)"

  - label: "Authentication/identity provider"
    description: "SSO integration, OAuth, SAML"

  - label: "Analytics or data warehouse"
    description: "Track user behavior or business metrics"

  - label: "Other external API"
    description: "Specify which external system"
```

---

### 3.2 Non-Functional Requirement Templates (5 templates)

**NFR-001 through NFR-005: Clarify performance, security, scalability, reliability, and cost targets**

---

#### Template NFR-001: Performance Targets

```yaml
question: |
  What are your performance targets for this feature?

  Be specific - "fast" is not measurable. Specify actual targets.

header: "Performance & Speed Targets"
multiSelect: false
options:
  - label: "Response time <200ms (tight - premium experience)"
    description: "Fast, responsive. Requires optimization. Higher complexity & cost."

  - label: "Response time 200-500ms (moderate - good experience)"
    description: "Acceptable for most use cases. Standard implementation approach."

  - label: "Response time 500ms-1s (relaxed - acceptable)"
    description: "Fine for background tasks or less-critical paths. Simplest implementation."

  - label: "Throughput target (requests/sec)"
    description: "Example: must handle 1000 requests/second at peak"

  - label: "Other metric"
    description: "Page load time, data processing speed, file upload speed, etc."
```

#### Template NFR-002: Security & Compliance

```yaml
question: |
  What are your security and compliance requirements?

header: "Security & Regulatory Compliance"
multiSelect: true
options:
  - label: "Data encryption (at rest and in transit)"
    description: "Encrypt sensitive data in database (AES-256) and during transmission (TLS 1.3)"

  - label: "User authentication & authorization"
    description: "Verify user identity and enforce access control (role-based or attribute-based)"

  - label: "Audit logging (compliance & forensics)"
    description: "Log all sensitive operations for audit trail and breach investigation"

  - label: "Regulatory compliance (GDPR, HIPAA, PCI-DSS, SOC2)"
    description: "Meet specific regulatory framework (specify which applies to you)"

  - label: "Data privacy (right to delete, consent management)"
    description: "Support GDPR right to be forgotten, consent tracking"
```

#### Template NFR-003: Scalability & Growth

```yaml
question: |
  How large must this feature scale?

  Consider: users, data volume, requests per second, concurrent connections

header: "Scalability & Growth Targets"
multiSelect: false
options:
  - label: "Small scale (10-100 users, 10-100 req/sec)"
    description: "Single server sufficient. Simple architecture."

  - label: "Medium scale (100-10,000 users, 100-1000 req/sec)"
    description: "Need load balancing. Database replication. Caching layer."

  - label: "Large scale (10k-1M users, 1k-10k req/sec)"
    description: "Distributed architecture. Database sharding. Global CDN."

  - label: "Massive scale (1M+ users, 10k+ req/sec)"
    description: "Cloud-native. Auto-scaling. Multi-region. Enterprise infrastructure."

  - label: "Gradual scaling (start small, grow over time)"
    description: "Architecture must support growth, but doesn't need max scale day 1"
```

#### Template NFR-004: Reliability & Availability

```yaml
question: |
  What are your uptime and reliability requirements?

header: "Reliability & Availability (SLA)"
multiSelect: false
options:
  - label: "Best effort (not critical if down occasionally)"
    description: "99.0% uptime acceptable (8.7 hours downtime/year). Development/testing systems."

  - label: "Standard availability (99.9% uptime)"
    description: "4.3 hours downtime/month. Production systems. Most SaaS apps."

  - label: "High availability (99.99% uptime)"
    description: "52 minutes downtime/year. Mission-critical systems. Requires redundancy."

  - label: "Maximum availability (99.999% uptime)"
    description: "5 minutes downtime/year. Life-critical systems. Banking, healthcare, aircraft."

  - label: "Custom target"
    description: "Specify your SLA (uptime %, acceptable downtime/month)"
```

#### Template NFR-005: Cost & Resource Constraints

```yaml
question: |
  Do you have cost or resource constraints?

header: "Cost & Resource Budgets"
multiSelect: false
options:
  - label: "Cost is not a constraint (use best technology)"
    description: "Optimize for performance and quality. Cost is secondary."

  - label: "Moderate cost constraint (<$100/month infrastructure)"
    description: "Standard cloud pricing. Single cloud provider. Managed services."

  - label: "Tight cost constraint (<$10/month infrastructure)"
    description: "Minimal, efficient architecture. Shared resources. Open-source focus."

  - label: "Token/resource constraint (AI framework)"
    description: "Commands must fit within token budget (e.g., <25K tokens)"

  - label: "Other resource constraint"
    description: "Execution time, memory, storage, or other resource limit"
```

---

### 3.3 Edge Case Templates (4 templates)

**EDGE-001 through EDGE-004: Clarify validation rules, boundary conditions, rate limits, and data consistency**

---

#### Template EDGE-001: Input Validation

```yaml
question: |
  What input validation rules must this feature enforce?

  Consider: required fields, format constraints, range limits, conditional rules

header: "Input Validation Rules"
multiSelect: true
options:
  - label: "Required fields (must not be empty)"
    description: "Specify which fields are mandatory vs. optional"

  - label: "Format validation (email, phone, URL, date)"
    description: "Validate specific formats. Example: email must be RFC 5322 compliant"

  - label: "Length/size limits (min/max characters, file size)"
    description: "Example: password 8-128 characters, image <5MB"

  - label: "Numeric ranges (min/max values)"
    description: "Example: age 18-120, quantity 1-1000, discount 0-100%"

  - label: "Enumerated values (only specific values allowed)"
    description: "Example: status ∈ {pending, approved, rejected}"
```

#### Template EDGE-002: Boundary Conditions

```yaml
question: |
  What happens at boundary conditions?

  Edge cases: zero, negative, max value, null, empty list

header: "Boundary Condition Handling"
multiSelect: true
options:
  - label: "Zero / empty conditions (empty list, zero count, null value)"
    description: "How to handle: no items in cart, zero quantity ordered, null value"

  - label: "Negative values (if applicable)"
    description: "Prevent negative: quantity, price, age, time duration"

  - label: "Maximum / overflow conditions (too large)"
    description: "How to handle: quantity exceeds stock, file too large, too many items"

  - label: "Concurrent / race conditions (simultaneous updates)"
    description: "How to handle: two users update same item, double-click button submission"
```

#### Template EDGE-003: Rate Limiting & Quotas

```yaml
question: |
  Should this feature have rate limits or quotas?

header: "Rate Limiting & Usage Quotas"
multiSelect: true
options:
  - label: "Rate limit (per-user or global)"
    description: "Example: 100 requests/minute per user, 10,000/hour global"

  - label: "User quota (limit per user)"
    description: "Example: free users get 10GB storage, can upload 100 files/day"

  - label: "Resource quota (system-wide limit)"
    description: "Example: can store max 1TB across all users, disk full triggers warning"

  - label: "Time-based restrictions"
    description: "Example: can only delete data within 30 days, login only during business hours"

  - label: "No limits (unlimited for this feature)"
    description: "No rate limiting or quotas needed"
```

#### Template EDGE-004: Data Consistency

```yaml
question: |
  How consistent must data be across the system?

header: "Data Consistency & Concurrency"
multiSelect: false
options:
  - label: "Strong consistency (immediately consistent)"
    description: "Data always accurate. All users see same view instantly. Slower writes."

  - label: "Eventual consistency (eventually consistent)"
    description: "Data consistent within seconds/minutes. Faster writes. Temporary inconsistency OK."

  - label: "Weak consistency (acceptable to be out of sync)"
    description: "Data can be stale. Fast, scalable. Used for non-critical analytics/views."

  - label: "Mixed approach (different consistency for different data)"
    description: "Critical data: strong. Analytics/cache: eventual. Hybrid approach."
```

---

### 3.4 Integration Templates (3 templates)

**INT-001 through INT-003: Clarify external APIs, webhooks, and data synchronization requirements**

---

#### Template INT-001: External API Integration

```yaml
question: |
  What external API or service needs to integrate with this feature?

  Specify: vendor, what data flows, real-time or batch, SLA requirements

header: "External API Integration"
multiSelect: false
options:
  - label: "Critical integration (system fails if service down)"
    description: "Must implement retry logic, circuit breaker, comprehensive error handling"

  - label: "Important integration (degrades gracefully if service down)"
    description: "Implement retry and fallback behavior. System continues with reduced function."

  - label: "Optional integration (nice to have, not critical)"
    description: "Best-effort attempt. Failures logged but don't impact core function."

  - label: "Batch integration (periodic sync, not real-time)"
    description: "Data syncs periodically (hourly, daily). Real-time not required."
```

#### Template INT-002: Webhook / Event Handling

```yaml
question: |
  Does this feature need to handle webhooks or events from external systems?

  Examples: payment confirmation, email delivery status, document signed, order shipped

header: "Webhook & Event Handling"
multiSelect: true
options:
  - label: "Inbound webhook (external system sends events to us)"
    description: "We receive webhook calls from external service. Requires: URL endpoint, signature verification, deduplication"

  - label: "Outbound webhook (we send events to external system)"
    description: "We call external URL when event happens. Requires: retry logic, delivery confirmation"

  - label: "Event transformation (convert external event format to internal)"
    description: "Map external event fields to internal data model"

  - label: "Webhook validation (verify authenticity)"
    description: "Verify webhook signature/token to prevent spoofing"
```

#### Template INT-003: Data Synchronization

```yaml
question: |
  How should data stay in sync with external systems?

header: "Data Synchronization Strategy"
multiSelect: false
options:
  - label: "Real-time sync (push/pull on every change)"
    description: "Immediate bidirectional sync. Requires webhooks or polling."

  - label: "Batch sync (periodic sync - hourly/daily)"
    description: "Sync at regular intervals. Good for high-volume, non-critical data."

  - label: "One-way sync (one direction only)"
    description: "Example: sync products from vendor to our catalog (read-only in our system)"

  - label: "Event-triggered sync (sync on specific events)"
    description: "Sync when event happens. Example: sync payment records when payment received"
```

---

### 3.5 Constraint Templates (2 templates)

**CONST-001 & CONST-002: Clarify technical constraints, architecture requirements, timeline, and priority**

---

#### Template CONST-001: Technical Stack & Architecture

```yaml
question: |
  Let me confirm technical and architectural constraints:

  What technologies are locked? What architectural patterns are required?

header: "Technical Stack & Architecture Constraints"
multiSelect: true
options:
  - label: "Locked technology (must use specific tech stack)"
    description: "Cannot change: language, framework, database, etc. Check tech-stack.md"

  - label: "Architecture pattern (must follow specific pattern)"
    description: "Cannot deviate: clean architecture, microservices, monolith, serverless, etc."

  - label: "Security/compliance policy (must follow specific policy)"
    description: "Cannot deviate: encryption requirements, audit logging, access control, etc."

  - label: "Existing system integration (must integrate with legacy system)"
    description: "Must work with existing system. May require specific protocols or formats."

  - label: "No constraints (flexible - recommend best approach)"
    description: "No locked technologies. Recommend best approach for your use case."
```

#### Template CONST-002: Timeline & Priority

```yaml
question: |
  What are the timeline and priority constraints?

header: "Timeline, Scope & Priority"
multiSelect: false
options:
  - label: "Hard deadline (must be done by specific date)"
    description: "Fixed launch date. Scope may need to be reduced if timeline is tight."

  - label: "Target date (preferred but flexible)"
    description: "Would like it by date X, but can slip if needed. Standard sprint planning."

  - label: "No timeline (whenever it's ready)"
    description: "Quality over speed. Take time to do it right."

  - label: "Phased launch (MVP now, features later)"
    description: "Launch minimal version first, add features in follow-up releases"

  - label: "User/stakeholder driven (depends on priority)"
    description: "Timeline depends on other work, stakeholder approval, or resource availability"
```

---

## Section 4: NFR Quantification Table

This table maps 15+ common vague terms to measurable ranges and provides templates for clarification.

### NFR Quantification Reference Table

| Vague Term | Measurable Range | Typical Target | DevForgeAI Example | Template Ref |
|-----------|------------------|------------------|-------------------|-------------|
| **"Fast"** | Response latency | <100ms, <200ms, <500ms, <1s | API <200ms p95 | NFR-001 |
| **"Responsive"** | User-perceived latency | <500ms, <1s | UI interactions <1s | NFR-001 |
| **"Scalable"** | User/request capacity | 100 users, 1k users, 1M users | Support 10k concurrent | NFR-003 |
| **"High performance"** | Throughput | 100 req/s, 1k req/s, 10k req/s | 1000 req/sec peak | NFR-001 |
| **"Reliable"** | Uptime percentage | 99%, 99.9%, 99.99%, 99.999% | 99.9% SLA (4.3h/month) | NFR-004 |
| **"Secure"** | Encryption & auth | TLS 1.3, AES-256, OAuth | AES-256 + JWT tokens | NFR-002 |
| **"Easy to use"** | Task completion | % users complete without help | 80% users complete onboarding | NFR-002 |
| **"Well documented"** | Coverage % | 50%, 80%, 95% | ≥80% code documentation | NFR-002 |
| **"Cost effective"** | Budget target | $1/user/month, $10/user/month | <$100/month infrastructure | NFR-005 |
| **"Accessible"** | Standard compliance | WCAG 2.0 A, AA, AAA | WCAG 2.1 AA compliance | NFR-002 |
| **"Maintainable"** | Code quality metric | Cyclomatic complexity <10 | Complexity <15 per method | NFR-002 |
| **"Efficient"** | Resource usage | <100MB RAM, <512MB RAM | <512MB RAM per instance | NFR-005 |
| **"Flexible"** | Configuration options | 3+ options, 5+ topologies | Support 5 deployment topologies | NFR-003 |
| **"Robust"** | Error handling | 90%, 95%, 99% error coverage | Handle 99% error scenarios | NFR-002 |
| **"User friendly"** | Time to value | <5 min, <15 min | Onboarding <5 minutes | NFR-002 |
| **"Available"** | System uptime | 99%, 99.5%, 99.9% | 99.9% availability | NFR-004 |
| **"Concurrent"** | Simultaneous connections | 100, 1000, 10000 users | 1000 concurrent connections | NFR-003 |

### How to Use the Table

**When user says:** "The system must be fast"

**Step 1:** Find "Fast" in table → Multiple ranges possible
**Step 2:** Use template NFR-001 to ask for specific target
**Step 3:** User selects: "<200ms response time"
**Step 4:** Document specific metric in requirements
**Step 5:** Add to acceptance criteria: "API response time <200ms p95"

---

## Section 5: Skill Integration Guide

This section documents how each of the 5 target skills should integrate this guidance document.

### 5.1 Integration: devforgeai-ideation

**Purpose:** Discover business problems and validate feasibility

**Workflow Phases Where Guidance Applied:**
- Phase 2 (Discovery): Identify ambiguities in business idea
- Phase 3 (Requirements Elicitation): Ask clarifying questions about problem/solution
- Phase 4 (Feasibility Analysis): Validate technical and business constraints

**Use Cases:**

1. **Vague Business Idea**
   - User: "We need a CRM"
   - Ambiguity Type: Functional requirement scope
   - Pattern to Use: Pattern 1 (Clarifying Feature Scope)
   - Template: FUN-007 (Scope Definition)
   - Outcome: Identify 5-10 specific features, scope for first story

2. **Missing Success Criteria**
   - User: "Build a recommendation engine"
   - Ambiguity Type: Non-functional requirement (accuracy, speed)
   - Pattern to Use: Pattern 5 (Quantifying Vague Performance Terms)
   - Template: NFR-001 (Performance Targets)
   - Outcome: Define measurable accuracy target (e.g., "95% precision")

3. **Undefined Stakeholders**
   - User: "Create a dashboard"
   - Ambiguity Type: Functional requirement (who uses it?)
   - Pattern to Use: Pattern 2 (Separating Requirements from Solutions)
   - Template: FUN-001 (Primary User Goal)
   - Outcome: Identify user roles (sales, analytics, executive) with different needs

**Integration Instructions:**

```
1. Load this guidance at Phase 2 start via:
   Read(file_path="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/user-input-guidance.md")

2. During Phase 3 (Requirements Elicitation), check for ambiguities:
   - Is feature scope clear? (no → use Pattern 1)
   - Are success criteria measurable? (no → use Pattern 5)
   - Are user roles defined? (no → use Pattern 1 or FUN-001)
   - Are edge cases identified? (no → use Pattern 8)

3. When ambiguity detected, select appropriate pattern and template

4. Ask user via AskUserQuestion tool (customize template for context)

5. Incorporate response into feasibility analysis output
```

**Success Criteria:**
- No vague terms in final requirements (all converted to metrics)
- User roles and goals clearly defined
- At least 3-5 success scenarios per feature
- Edge cases identified for critical features
- Technical constraints validated against tech-stack.md

---

### 5.2 Integration: devforgeai-story-creation

**Purpose:** Generate complete stories with acceptance criteria

**Workflow Phases Where Guidance Applied:**
- Phase 2: Clarify acceptance criteria
- Phase 3: Identify edge cases and error scenarios
- Phase 4: Validate story against context files

**Use Cases:**

1. **Vague Acceptance Criteria**
   - User provides: "User can search for products"
   - Problem: Doesn't specify search type (full-text, category, filters?)
   - Pattern: Pattern 3 (Identifying Multiple Interpretations)
   - Template: FUN-002 (User Roles and Permissions) or FUN-003 (Success Behaviors)
   - Outcome: AC specifies "full-text search by title/description, filter by category/price/rating"

2. **Missing Edge Cases**
   - Story specifies: "User uploads image"
   - Problem: No error handling (file too large, wrong format, upload fails?)
   - Pattern: Pattern 8 (Discovering Missing Edge Cases)
   - Template: EDGE-001 (Input Validation)
   - Outcome: AC includes "reject files >5MB with error message, support JPG/PNG only"

3. **Unclear Integration Points**
   - Story specifies: "Process payment"
   - Problem: No payment processor specified, retry strategy unclear
   - Pattern: Pattern 11 (Finding External System Dependencies)
   - Template: INT-001 (External API Integration)
   - Outcome: AC specifies "integrate with Stripe, retry 3x on timeout, fallback to manual review"

**Integration Instructions:**

```
1. During Phase 2, review each AC for ambiguities:
   - Are behaviors specific or vague? (vague → use Pattern 1, Pattern 3)
   - Are success criteria measurable? (vague → use Section 4 NFR table)
   - Are error cases covered? (missing → use Pattern 8)
   - Are integrations specified? (missing → use Pattern 11)

2. Use targeted patterns and templates for each type of gap

3. Result: Complete AC that is:
   - Specific (no ambiguous terms)
   - Measurable (includes metrics/numbers)
   - Testable (each AC can be verified)
   - Complete (happy path + errors + edge cases)
```

**Success Criteria:**
- Each AC has ≥1 success scenario + ≥1 error scenario
- No vague terms (all quantified via Section 4 table)
- Integration points explicitly specified
- Edge cases identified (boundary conditions, validation rules, rate limits)
- Acceptance criteria is testable (can write automated tests)

---

### 5.3 Integration: devforgeai-architecture

**Purpose:** Create 6 immutable context files with constraints

**Workflow Phases Where Guidance Applied:**
- Phase 1: Identify technical constraints
- Phase 2: Identify architectural constraints
- Phase 3: Create context files with constraint documentation

**Use Cases:**

1. **Incomplete tech-stack.md**
   - Problem: Doesn't specify approved libraries/versions
   - Pattern: Pattern 14 (Discovering Hidden Technical Constraints)
   - Template: CONST-001 (Technical Stack & Architecture Constraints)
   - Outcome: tech-stack.md lists all locked technologies with versions

2. **Missing security requirements in architecture-constraints.md**
   - Problem: Security policies not documented
   - Pattern: Pattern 6 (Defining Security Requirements Precisely)
   - Template: NFR-002 (Security & Compliance)
   - Outcome: architecture-constraints.md specifies encryption, authentication, compliance requirements

3. **Undefined performance targets in dependencies.md**
   - Problem: No SLA/availability targets specified
   - Pattern: Pattern 5 & 7 (Performance, Scalability)
   - Template: NFR-001, NFR-003, NFR-004
   - Outcome: context files document measurable SLAs and scalability targets

**Integration Instructions:**

```
1. Load this guidance at Phase 1 start

2. For each context file being created, check for ambiguities:
   - tech-stack.md: Are all technologies specified with versions? (no → use Pattern 14, CONST-001)
   - architecture-constraints.md: Are design patterns clear? (no → use Pattern 14)
   - dependencies.md: Are version constraints specified? (no → use Pattern 14)
   - coding-standards.md: Are code style rules specific? (vague → use Section 4)
   - source-tree.md: Are file location rules clear? (ambiguous → clarify)
   - anti-patterns.md: Are forbidden patterns specific with rationale? (yes → good)

3. When ambiguity found, ask for clarification via AskUserQuestion

4. Document constraints precisely in context files (no vague language)

5. Validate against patterns:
   - No circular dependencies (Pattern 11)
   - No conflicting constraints
   - All constraints measurable and testable
```

**Success Criteria:**
- All 6 context files exist and are non-empty
- No placeholder content (TODO, TBD, TBD, etc.)
- All constraints are specific and measurable
- tech-stack.md includes approved libraries with versions
- architecture-constraints.md specifies clean architecture rules
- dependencies.md locks all package versions
- coding-standards.md includes naming/style rules
- source-tree.md specifies file location rules
- anti-patterns.md lists forbidden patterns with rationale

---

### 5.4 Integration: devforgeai-ui-generator

**Purpose:** Generate UI specifications before coding

**Workflow Phases Where Guidance Applied:**
- Phase 1: Clarify user requirements for UI
- Phase 2: Identify user interactions and workflows
- Phase 3: Generate UI specifications with layouts/components

**Use Cases:**

1. **Vague UI Requirements**
   - User: "Create a dashboard"
   - Problem: No specification of what data to display, how users interact
   - Pattern: Pattern 2 (Separating Requirements from Solutions)
   - Template: FUN-001 (Primary User Goal), FUN-003 (Success Behaviors)
   - Outcome: Dashboard spec includes specific widgets, data sources, refresh rates

2. **Missing Usability Requirements**
   - User: "Design admin panel"
   - Problem: No accessibility requirements, performance targets for UI
   - Pattern: Pattern 5 (Quantifying Vague Performance Terms), Pattern 6 (Security)
   - Template: NFR-001 (Performance), NFR-002 (Accessibility)
   - Outcome: UI spec includes <500ms load time, WCAG 2.1 AA accessibility

3. **Undefined User Interactions**
   - User: "Create form for creating orders"
   - Problem: No specification of validation, error messaging, success feedback
   - Pattern: Pattern 8 (Discovering Missing Edge Cases), Pattern 10 (Data Validation)
   - Template: EDGE-001 (Input Validation), EDGE-002 (Error Handling)
   - Outcome: Form spec includes all validations, error messages, success states

**Integration Instructions:**

```
1. During Phase 1, clarify user requirements:
   - Who is the user? (use FUN-001)
   - What are they trying to accomplish? (use FUN-003)
   - What data do they need to see? (use FUN-005)
   - How do they interact? (use FUN-003 + FUN-008)

2. During Phase 2, identify edge cases:
   - What happens on error? (use EDGE-002)
   - What are validation rules? (use EDGE-001)
   - What's the loading/empty state? (use EDGE-002)
   - What accessibility requirements? (use NFR-002)

3. During Phase 3, generate UI spec including:
   - Layout and component hierarchy
   - User interactions (click, input, navigation)
   - Validation rules and error messages
   - Success/loading/empty states
   - Accessibility features (WCAG 2.1 AA)
   - Performance targets (page load <3s)

4. Validate spec is complete:
   - Happy path specified? (yes)
   - Error paths specified? (yes)
   - Edge cases handled? (yes)
   - Accessibility considered? (yes)
```

**Success Criteria:**
- User goals clearly defined (primary persona + use case)
- All user interactions specified (forms, buttons, navigation)
- Validation rules documented for all inputs
- Error messages specified for all error scenarios
- Success/loading/empty states defined
- Accessibility requirements met (WCAG 2.1 AA minimum)
- Performance targets included (page load time, interaction latency)
- UI responsive design breakpoints specified

---

### 5.5 Integration: devforgeai-orchestration

**Purpose:** Manage full feature lifecycle (dev → qa → release)

**Workflow Phases Where Guidance Applied:**
- Phase 1: Feature decomposition and scope clarification
- Phase 2: Story creation with complete AC
- Phase 3-5: Monitor for ambiguities during implementation
- Phase 6-7: Validate completeness before QA/release

**Use Cases:**

1. **Feature Too Large for Single Story**
   - Problem: Feature requires multiple stories, unclear how to decompose
   - Pattern: Pattern 4 (Decomposing Complex Features)
   - Template: FUN-007 (Scope Definition)
   - Outcome: Feature decomposed into 3-5 stories, each completable in one sprint

2. **Unclear Success Criteria for Release**
   - Problem: Not clear what "done" means, acceptance criteria ambiguous
   - Pattern: Pattern 5 (Quantifying Vague Performance Terms)
   - Template: NFR-001 (Performance Targets), CONST-002 (Timeline & Priority)
   - Outcome: Release criteria specified: "< 5 critical bugs, >95% coverage, <200ms API latency"

3. **Missing Integration Points Between Stories**
   - Problem: Story A and Story B need to integrate, interface not defined
   - Pattern: Pattern 12 (Clarifying Data Contract Requirements)
   - Template: INT-002 (Webhook/Event Handling), INT-003 (Data Sync)
   - Outcome: Data contract specified between stories (fields, formats, SLA)

**Integration Instructions:**

```
1. During Phase 1 (feature decomposition):
   - Is feature scope clear? (no → use Pattern 4, FUN-007)
   - Can it fit in one story? (yes/no → decide)
   - What are story dependencies? (identify → Pattern 11)
   - What's the priority order? (define → CONST-002)

2. During Phase 2 (story creation):
   - Do acceptance criteria align with overall feature goal? (no → refine)
   - Are integration points with other stories clear? (no → use Pattern 12)
   - Are edge cases covered? (no → use Pattern 8)
   - Are constraints understood? (no → use Pattern 14, Pattern 15)

3. During Phases 3-5 (implementation monitoring):
   - Are developers hitting ambiguities? (listen for questions)
   - Are integration points clear between stories? (verify via code review)
   - Is implementation staying within constraints? (check against context files)

4. During Phases 6-7 (QA/release validation):
   - Have all acceptance criteria been met? (yes/no → assess)
   - Are edge cases actually handled in code? (yes/no → test)
   - Are integrations working end-to-end? (yes/no → integration test)
   - Are metrics/SLAs being met? (yes/no → performance test)
```

**Success Criteria:**
- Feature decomposed into completable stories (each ≤1 sprint)
- Story dependencies identified and sequenced
- Acceptance criteria clear and testable for all stories
- Integration points specified between stories
- Constraints understood by entire team
- Definition of Done for feature is measurable
- Release criteria documented and verified

---

## Section 6: Framework Terminology Reference

This section validates that terminology used in this guidance aligns with framework definitions and provides cross-references.

### 6.1 CLAUDE.md Definitions

**Key Framework Concepts:**

| Concept | CLAUDE.md Definition | How Guidance Uses It |
|---------|---------------------|----------------------|
| **Ask, Don't Assume** | When ambiguity exists, skills explicitly ask for clarification rather than making assumptions | Core principle for this entire guidance; all 15 patterns are implementations of this principle |
| **Spec-Driven Development** | Software built from immutable specs (context files) with evidence-based constraints | Patterns 14-15 enforce spec compliance; context files are non-negotiable |
| **Context Files** | 6 immutable files (tech-stack, source-tree, dependencies, coding-standards, architecture-constraints, anti-patterns) | Pattern 14 & Section 5 explicitly reference these files |
| **Clean Architecture** | Layered: Infrastructure → Application → Domain (dependency flows upward, never downward) | Pattern 14 references architecture-constraints.md; Pattern 11 clarifies layer boundaries |
| **Dependency Injection** | All dependencies passed to objects, never directly instantiated | Pattern 14 enforces DI via architecture-constraints.md |
| **TDD (Test-Driven Development)** | Red → Green → Refactor workflow: write failing tests first, then implementation | Patterns assume TDD workflow; acceptance criteria should be testable |
| **Repository Pattern** | Data access abstraction via interfaces; prevents domain from depending on infrastructure | Pattern 11 clarifies integration with repository interfaces |
| **Quality Gates** | 4 gates that block progression: Context Validation, Test Passing, QA Approval, Release Readiness | Pattern 5 & 15 ensure quality metrics are defined for gates |
| **Workflow States** | 11 sequential story states from Backlog → Released | Pattern 4 & 15 clarify scope for each state |
| **Anti-Patterns** | Forbidden patterns documented in anti-patterns.md (God Objects, hardcoded secrets, SQL concatenation, etc.) | Pattern 14 references anti-patterns.md as constraint file |
| **Definition of Done (DoD)** | Checklist of items that must be complete before story is "done" | Pattern 8 & Pattern 15 ensure DoD items are specific and testable |
| **Acceptance Criteria (AC)** | Testable scenarios describing what "working" looks like | All 15 patterns exist to make AC complete and unambiguous |

### 6.2 Context File References

**Guidance Validation Against Context Files:**

| Context File | How Guidance Ensures Compliance |
|--------------|--------------------------------|
| **tech-stack.md** | Pattern 14 (Discovering Hidden Technical Constraints) explicitly asks about locked technologies. Template CONST-001 ensures no unapproved libraries are proposed. |
| **source-tree.md** | Pattern 14 ensures file location rules understood. Skills using guidance confirm new files placed in correct locations per source-tree.md. |
| **dependencies.md** | Pattern 14 validates that proposed dependencies match locked versions. No version mismatches. |
| **coding-standards.md** | Section 4 (NFR Quantification) maps vague terms (code quality, maintainability) to measurable standards from coding-standards.md |
| **architecture-constraints.md** | Pattern 14 enforces layer boundaries and design patterns documented in architecture-constraints.md. Pattern 11 clarifies repository pattern and DI usage. |
| **anti-patterns.md** | Pattern 14 ensures forbidden patterns from anti-patterns.md are NOT suggested. Patterns 8-10 (edge cases, validation, degradation) actively prevent anti-patterns. |

### 6.3 Related Documentation Cross-References

**How This Guidance Document Complements Other Framework Docs:**

| Related Document | Relationship | How to Use Together |
|------------------|--------------|-------------------|
| **effective-prompting-guide.md** | User-facing counterpart | This document = framework-internal guidance. effective-prompting-guide.md = what to tell users. Both same principles, different audience. |
| **requirements-elicitation-guide.md** | Domain-specific patterns | This document = generic patterns (apply to any domain). requirements-elicitation-guide.md = domain-specific (E-commerce, SaaS, Fintech, Healthcare, etc.). Use together: apply generic pattern, then check domain-specific for nuances. |
| **CLAUDE.md** | Framework constitution | This document operationalizes CLAUDE.md's "Ask, Don't Assume" principle via 15 patterns. All patterns must comply with CLAUDE.md rules. |
| **completion-handoff.md** | Handoff between skills | This guidance ensures input quality at skill handoff boundaries. Prevents incomplete/ambiguous specs from moving between skills. |
| **self-validation-workflow.md** | Internal validation | Guidance patterns align with self-validation checkpoints. If guidance patterns satisfied, self-validation should pass. |
| **validation-checklists.md** | Checklist structure | Some guidance templates could be converted to validation checklists. Both validate completeness. |

### 6.4 Consistency Validation

**This Section Validates Internal Consistency:**

#### Terminology Alignment

- **Ambiguity** = gap between user intent and framework understanding
  - Trigger: User says "build dashboard" (vague)
  - Resolution: Clarifying questions reduce ambiguity
  - Guidance: Provides specific templates for each ambiguity type

- **Specification** = precise, measurable, testable requirement
  - Before guidance: "Fast API response"
  - After guidance: "API response <200ms p95 latency"
  - Validation: Specification is measurable and testable

- **Acceptance Criteria** = specific scenarios proving feature works
  - Requirement of guidance: Each AC has ≥1 success + ≥1 error scenario
  - From CLAUDE.md: AC must be testable (can write automated tests)
  - Alignment: If guidance patterns applied, AC will be testable

#### Framework Compliance Validation

**This guidance is compliant with CLAUDE.md because:**

1. **"Ask, Don't Assume" Principle**
   - Guidance: 15 patterns that prompt for clarification
   - CLAUDE.md requirement: "HALT! on ambiguity. Use AskUserQuestion."
   - Alignment: All patterns include AskUserQuestion templates

2. **"No Autonomous Deferrals" Requirement**
   - Guidance: Pattern 8-10 ensure edge cases identified
   - CLAUDE.md requirement: Cannot defer work without user approval
   - Alignment: Complete AC (via guidance) prevents future deferrals

3. **"Context Files Are Immutable" Requirement**
   - Guidance: Pattern 14 explicitly references context files
   - CLAUDE.md requirement: Cannot violate tech-stack.md, architecture-constraints.md, etc.
   - Alignment: Guidance ensures context files are consulted before design

4. **"Clean Architecture" Requirement**
   - Guidance: Patterns 11 & 14 clarify layer boundaries
   - CLAUDE.md requirement: Infrastructure → Application → Domain flow, never reversed
   - Alignment: Guidance ensures architecture patterns documented

5. **"Dependency Injection" Requirement**
   - Guidance: Pattern 14 enforces DI via architecture-constraints.md
   - CLAUDE.md requirement: No direct instantiation
   - Alignment: Guidance ensures DI is specified in context files

#### Section Completeness Cross-Check

| Section | Purpose | Coverage | Validation |
|---------|---------|----------|-----------|
| 1: Overview | Navigation, version control, quick reference | ✓ Complete | Provides ToC and quick links |
| 2: Elicitation Patterns | 15 patterns covering 5 categories | ✓ Complete | 4 functional + 3 NFR + 3 edge + 3 integration + 2 constraint |
| 3: AskUserQuestion Templates | 28 copy-paste templates | ✓ Complete | 8 functional + 5 NFR + 4 edge + 3 integration + 2 constraint + 4 misc |
| 4: NFR Quantification Table | 15+ vague terms → metrics | ✓ Complete | All common vague terms included with ranges |
| 5: Skill Integration | How 5 skills use guidance | ✓ Complete | ideation, story-creation, architecture, ui-generator, orchestration |
| 6: Terminology Reference | Links to CLAUDE.md, context files | ✓ Complete | All key concepts mapped; compliance validated |

---

## Appendix: Quick Reference Index

### By Category

**Functional Requirements (Scope, Behavior, Users):**
- Pattern 1: Clarifying Feature Scope
- Pattern 2: Separating Requirements from Solutions
- Pattern 3: Identifying Multiple Interpretations
- Pattern 4: Decomposing Complex Features
- Templates: FUN-001 through FUN-008

**Non-Functional Requirements (Performance, Security, Scalability):**
- Pattern 5: Quantifying Vague Performance Terms
- Pattern 6: Defining Security Requirements Precisely
- Pattern 7: Specifying Scalability Targets
- Templates: NFR-001 through NFR-005
- Section 4: NFR Quantification Table (reference)

**Edge Cases & Validation:**
- Pattern 8: Discovering Missing Edge Cases
- Pattern 9: Handling Graceful Degradation
- Pattern 10: Identifying Data Validation Rules
- Templates: EDGE-001 through EDGE-004

**Integration & Data Flow:**
- Pattern 11: Finding External System Dependencies
- Pattern 12: Clarifying Data Contract Requirements
- Pattern 13: Defining Error Recovery Procedures
- Templates: INT-001 through INT-003

**Constraints & Scope:**
- Pattern 14: Discovering Hidden Technical Constraints
- Pattern 15: Identifying Business Constraints
- Templates: CONST-001, CONST-002

### By Skill

**devforgeai-ideation:** Patterns 1, 2, 5, 8, 14, 15
**devforgeai-story-creation:** Patterns 1, 3, 5, 8, 10, 11, 12
**devforgeai-architecture:** Patterns 14, 15 + All constraint templates
**devforgeai-ui-generator:** Patterns 1, 2, 3, 8, 10, 5, 6
**devforgeai-orchestration:** Patterns 1, 4, 12, 15 + All scope templates

### By Ambiguity Type

- **Vague/unclear specification:** Section 4 (NFR Quantification Table)
- **Missing requirements:** Patterns 1, 8, 11
- **Scope creep:** Patterns 4, 15
- **Integration gaps:** Patterns 11, 12, 13
- **Constraint violations:** Patterns 14, 15
- **Edge case gaps:** Patterns 8, 9, 10

---

**Document Version:** 1.0
**Last Updated:** 2025-01-21
**Status:** Published
**Audience:** DevForgeAI Skills (devforgeai-ideation, devforgeai-story-creation, devforgeai-architecture, devforgeai-ui-generator, devforgeai-orchestration)
**Related:** effective-prompting-guide.md (user-facing counterpart)
