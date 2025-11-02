---
name: devforgeai-ideation
description: Transform business ideas and problems into structured requirements through guided discovery, requirements elicitation, and feasibility analysis. Use when starting new projects (greenfield), planning features for existing systems (brownfield), or exploring solution spaces before architecture and development. Supports simple apps through multi-tier platforms via progressive complexity assessment.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - WebFetch
  - Bash(git:*)
  - Skill
  - TodoWrite
---

# DevForgeAI Ideation Skill

Transform raw business ideas, problems, and opportunities into structured, actionable requirements that drive spec-driven development with zero technical debt.

## Purpose

This skill serves as the **entry point** for the entire DevForgeAI framework. Transform business ideas into structured requirements through systematic discovery, requirements elicitation, complexity assessment, and feasibility analysis.

**Core Capabilities:**
1. **Discovery & Exploration** - Understand problem space through structured questioning
2. **Requirements Elicitation** - Extract functional and non-functional requirements
3. **Complexity Assessment** - Determine appropriate architecture tier (Simple → Enterprise)
4. **Epic/Feature Decomposition** - Break large ideas into manageable work units
5. **Feasibility Analysis** - Assess technical, business, and resource constraints
6. **Greenfield/Brownfield Support** - Handle both new projects and existing codebases

## Core Philosophy

**"Start with Why, Then What, Then How"**
- **Why:** Business value, user needs, success metrics
- **What:** Functional/non-functional requirements, constraints
- **How:** Technical approach (delegated to architecture skill)

**"Ask, Don't Assume"**
- Use AskUserQuestion for ALL ambiguities
- Never infer requirements from incomplete information
- Validate assumptions explicitly

**"Right-size the Solution"**
- Progressive complexity assessment (simple → moderate → complex → enterprise)
- Don't over-engineer simple problems
- Don't under-architect complex platforms

## When to Use This Skill

### ✅ Trigger Scenarios

- "I want to build a new application for [purpose]" (Greenfield)
- "Add multi-factor authentication to our existing system" (Brownfield)
- "Our current system has [problem], how can we fix it?" (Problem-solving)
- "We want to migrate from [old tech] to [new tech]" (Strategic planning)

### ❌ When NOT to Use

- Implementation of well-defined stories (use devforgeai-development)
- Architecture decisions with clear requirements (use devforgeai-architecture)
- Code quality validation (use devforgeai-qa)
- Deployment and release (use devforgeai-release)

---

## Ideation Workflow (6 Phases)

### Phase 1: Discovery & Problem Understanding

**Objective:** Understand the business context, problem space, and desired outcomes

#### 1.1 Project Context Discovery

Use AskUserQuestion to establish foundation:

```
Question: "What type of project is this?"
Header: "Project type"
Options:
  - "Greenfield - New project/product from scratch"
  - "Brownfield - Adding features to existing system"
  - "Modernization - Replacing/upgrading legacy system"
  - "Problem-solving - Fixing issues in current system"
```

#### 1.2 Existing System Analysis (Brownfield/Modernization Only)

**Discover codebase structure:**
```
Glob(pattern="**/*.sln")          # .NET solutions
Glob(pattern="**/package.json")   # Node.js projects
Glob(pattern="**/requirements.txt") # Python projects
```

**Check for existing DevForgeAI context:**
```
Read(file_path=".devforgeai/context/tech-stack.md")
Read(file_path=".devforgeai/context/source-tree.md")
```

**Analyze current architecture:**
```
Grep(pattern="class.*Controller", type="cs")
Grep(pattern="interface I.*Repository", type="cs")
```

Document: technology stack, architecture patterns, database schema, pain points

#### 1.3 Problem Space Exploration

Use AskUserQuestion for open-ended discovery:

```
Question: "What business problem are you trying to solve?"
Question: "Who are the primary users or beneficiaries?"
Options:
  - "End customers/consumers"
  - "Internal employees"
  - "Business partners/vendors"
  - "Administrators/operators"
multiSelect: true

Question: "What is the primary goal or success metric?"
Options:
  - "Increase revenue/conversions"
  - "Reduce costs/inefficiency"
  - "Improve user experience"
  - "Enable new capabilities"
  - "Compliance/regulatory requirement"
multiSelect: true
```

#### 1.4 Scope Boundary Definition

```
Question: "What is the initial scope for the MVP or first release?"
Options:
  - "Core feature only (single user flow)"
  - "Core + 2-3 secondary features"
  - "Full feature set (comprehensive solution)"
  - "Not sure - need help defining MVP"
```

Document: In Scope (included), Out of Scope (excluded), Future Scope (deferred)

---

### Phase 2: Requirements Elicitation

**Objective:** Extract functional and non-functional requirements systematically

#### 2.1 Functional Requirements Discovery

Use structured questioning to uncover features. Capture requirements as user stories:

```markdown
As a [user type],
I want to [action/capability],
So that [business value/benefit].
```

**Load domain-specific elicitation patterns:**
```
Read(file_path=".claude/skills/devforgeai-ideation/references/requirements-elicitation-guide.md")
```

This reference provides comprehensive probing questions for:
- E-commerce platforms
- SaaS applications
- Fintech systems
- Healthcare platforms
- Content management
- Workflow/automation tools

**Example questioning approach:**
```
Question: "What [domain-specific] capabilities should the platform support?"
Options: [Domain-specific feature list]
multiSelect: true
```

#### 2.2 Data Requirements Discovery

Identify core entities and relationships:

```
Question: "What are the main data entities this system will manage?"
Options:
  - "Users/Accounts"
  - "Products/Inventory"
  - "Orders/Transactions"
  - "Content/Documents"
  - "Events/Activities"
multiSelect: true
```

Probe for attributes and document relationships (one-to-many, many-to-many, one-to-one)

#### 2.3 Integration Requirements

```
Question: "Does this system need to integrate with external services?"
Options:
  - "Payment gateway (Stripe, PayPal, etc.)"
  - "Email service (SendGrid, AWS SES, etc.)"
  - "Authentication provider (Auth0, OAuth, etc.)"
  - "Cloud storage (S3, Azure Blob, etc.)"
  - "Analytics (Google Analytics, Mixpanel, etc.)"
  - "No external integrations"
multiSelect: true
```

#### 2.4 Non-Functional Requirements (NFRs)

**Performance:**
```
Question: "What are the performance requirements?"
Options:
  - "High performance (<100ms response time, >10k concurrent users)"
  - "Standard performance (<500ms response time, 1k-10k users)"
  - "Moderate performance (<2s response time, <1k users)"
  - "Performance not critical (internal tool, low usage)"
```

**Security:**
```
Question: "What security requirements apply?"
Options:
  - "Authentication required (user login)"
  - "Authorization/role-based access control"
  - "Data encryption (at rest and in transit)"
  - "Compliance (GDPR, HIPAA, SOC2, PCI-DSS)"
  - "Audit logging"
  - "Standard security practices"
multiSelect: true
```

**Scalability:**
```
Question: "What scalability is needed?"
Options:
  - "Small scale (100s of users, single server)"
  - "Medium scale (1000s of users, horizontal scaling)"
  - "Large scale (10k+ concurrent users, multi-region)"
  - "Massive scale (millions of users, global CDN)"
```

**Availability:**
```
Question: "What availability is required?"
Options:
  - "High availability (99.9% uptime, 24/7 monitoring)"
  - "Business hours only (99% uptime during work hours)"
  - "Best effort (no SLA)"
```

---

### Phase 3: Complexity Assessment & Architecture Planning

**Objective:** Assess solution complexity and determine appropriate architecture tier

#### 3.1 Complexity Scoring

Load comprehensive assessment matrix:
```
Read(file_path=".claude/skills/devforgeai-ideation/references/complexity-assessment-matrix.md")
```

**Score across 4 dimensions (0-60 total):**

**Functional Complexity (0-20 points):**
- User roles: 1-2 (Low=5), 3-5 (Medium=10), 6+ (High=15)
- Core entities: 1-3 (Low=5), 4-10 (Medium=10), 11+ (High=15)
- Integrations: 0-1 (Low=3), 2-4 (Medium=7), 5+ (High=10)
- Workflow complexity: Linear (Low=3), Branching (Medium=7), State machines (High=10)

**Technical Complexity (0-20 points):**
- Data volume: <10k (Low=5), 10k-1M (Medium=10), >1M (High=15)
- Concurrency: <100 (Low=5), 100-10k (Medium=10), >10k (High=15)
- Real-time requirements: None (Low=3), Polling (Medium=7), WebSockets/Events (High=10)

**Team/Organizational Complexity (0-10 points):**
- Team size: 1-3 (Low=3), 4-10 (Medium=6), 11+ (High=10)
- Team distribution: Co-located (Low=2), Remote (Medium=5), Multi-timezone (High=8)

**Non-Functional Complexity (0-10 points):**
- Performance: Moderate (Low=3), Standard (Medium=6), High (High=10)
- Compliance: None (Low=0), Standard (Medium=5), Strict (High=10)

#### 3.2 Architecture Tier Recommendation

**Tier 1: Simple Application (0-15 points)**
- Architecture: Monolithic
- Layers: 2-3 (API, Business Logic, Data)
- Database: Single database
- Deployment: Single server or serverless
- Example: Todo app, blog, portfolio site

**Tier 2: Moderate Application (16-30 points)**
- Architecture: Modular Monolith
- Layers: 3-4 (API, Application, Domain, Infrastructure)
- Database: Primary + read replicas
- Deployment: Load-balanced multi-instance
- Example: E-commerce site, SaaS tool

**Tier 3: Complex Platform (31-45 points)**
- Architecture: Microservices or Clean Architecture
- Layers: 4-5 with domain separation
- Database: Polyglot persistence
- Deployment: Kubernetes, service mesh
- Example: Multi-tenant SaaS, marketplace

**Tier 4: Enterprise Platform (46-60 points)**
- Architecture: Distributed microservices with event-driven patterns
- Layers: 5+ with DDD
- Database: Polyglot + event sourcing + CQRS
- Deployment: Multi-region, auto-scaling
- Example: Global fintech, streaming service

**Validate recommendation:**
```
Question: "Based on requirements, this appears to be [Tier] with complexity score [X]. Does this match expectations?"
Options:
  - "Yes, that's correct"
  - "No, it should be simpler (explain why)"
  - "No, it should be more complex (explain why)"
```

---

### Phase 4: Epic & Feature Decomposition

**Objective:** Break down solution into manageable work units

#### 4.1 Epic Identification

Group features into business-value themes.

**Epic Definition:**
- High-level business capability
- Spans multiple sprints (4-8 weeks)
- Delivers measurable business value
- Prioritized independently

**Load domain patterns for decomposition guidance:**
```
Read(file_path=".claude/skills/devforgeai-ideation/references/domain-specific-patterns.md")
```

**Example decomposition (E-commerce):**
- Epic 1: User Management
- Epic 2: Product Catalog
- Epic 3: Shopping & Checkout
- Epic 4: Order Management
- Epic 5: Admin Dashboard

**Prioritize epics:**
```
Question: "Which epics should be prioritized for initial implementation?"
Options:
  - "Epic 1: [Name] (Est: [X] story points)"
  - "Epic 2: [Name] (Est: [X] story points)"
  - "Epic 3: [Name] (Est: [X] story points)"
multiSelect: true
```

#### 4.2 Feature Breakdown

For each epic, identify features (user-facing capabilities).

Example - Epic: "User Management"
- Feature 1: User Registration
- Feature 2: User Login/Authentication
- Feature 3: Profile Management
- Feature 4: Password Reset

#### 4.3 Story Decomposition (High-Level)

For priority features, outline stories (atomic units of work, 1-3 days each).

Example - Feature: "User Registration"
- Story 1: Registration form with email/password
- Story 2: Email verification workflow
- Story 3: Registration validation rules

**Note:** Detailed story creation happens in devforgeai-orchestration skill

---

### Phase 5: Feasibility & Constraints Analysis

**Objective:** Identify technical, business, and resource constraints

#### 5.1 Technical Feasibility

Load feasibility framework:
```
Read(file_path=".claude/skills/devforgeai-ideation/references/feasibility-analysis-framework.md")
```

**Assess technical risks:**
```
Question: "Are there any technical constraints or concerns?"
Options:
  - "Must integrate with legacy systems"
  - "Must support offline functionality"
  - "Must work on low-bandwidth networks"
  - "Requires real-time data synchronization"
  - "Requires complex algorithms/ML"
  - "No major technical constraints"
multiSelect: true
```

Document each: nature, impact on architecture, mitigation, risk level

#### 5.2 Business Constraints

**Budget & Resources:**
```
Question: "What are the budget and resource constraints?"
Options:
  - "Limited budget - minimize cloud/licensing costs"
  - "Limited team - simple, maintainable architecture"
  - "Time-constrained - MVP in [X weeks/months]"
  - "No major resource constraints"
multiSelect: true
```

**Timeline:**
```
Question: "What is the target timeline?"
Options:
  - "Urgent - MVP in 4-6 weeks"
  - "Standard - MVP in 2-3 months"
  - "Flexible - 4-6 months or longer"
```

#### 5.3 Risk Assessment

Identify risks (technical, business, team). For each: Probability, Impact, Mitigation

---

### Phase 6: Requirements Documentation & Handoff

**Objective:** Generate structured requirements documents for downstream skills

#### 6.1 Generate Epic Document(s)

**Track epic creation with TodoWrite:**
```
At start of epic generation, create todos for each epic:
TodoWrite([
  "Create EPIC-001: [name]",
  "Create EPIC-002: [name]",
  ...
  "Create EPIC-N: [name]",
])

Mark each epic as completed after creating the file.
```

Create epic documents in `.ai_docs/Epics/EPIC-NNN-[name].epic.md` with:
- YAML frontmatter (id, title, status, dates, points)
- Business goal and success metrics
- Features breakdown
- Requirements (functional, NFRs, data, integrations)
- Architecture considerations (tier, pattern, constraints)
- Risks and next steps

**CRITICAL: Verify all planned epics are created**

Before proceeding to Phase 6.2:
```
# Count planned epics (from decomposition phase)
planned_epics = [count from Phase 4 decomposition]

# Count created epic files
created_epic_files = Glob(pattern=".ai_docs/Epics/EPIC-*.epic.md")
created_count = len(created_epic_files)

# Verification gate
if created_count < planned_epics:
    # HALT - Incomplete work detected
    missing_count = planned_epics - created_count

    ERROR: Only {created_count}/{planned_epics} epics created

    Missing epics: Review Phase 4 decomposition and create remaining epic documents

    DO NOT PROCEED to Phase 6.2 until all epics are created and verified.

else:
    # All epics created, safe to proceed
    ✓ All {planned_epics} epics created and verified
    → Proceed to Phase 6.2
```

#### 6.2 Generate Requirements Specification

Create requirements spec in `.devforgeai/specs/requirements/[project]-requirements.md` with:
- Project context (type, complexity, timeline)
- Problem statement and solution overview
- User roles and personas
- Complete requirements (functional, NFRs, data model, integrations)
- Architecture recommendations
- Risks, assumptions, success criteria

#### 6.3 Transition to Architecture Skill

**Check if architecture context exists:**
```
Glob(pattern=".devforgeai/context/*.md")
```

**If context files don't exist:**
```
Report: """
✅ Requirements documentation complete

Generated Documents:
- [N] Epic documents in .ai_docs/Epics/
- Requirements specification in .devforgeai/specs/requirements/

Next Steps:
1. Invoking devforgeai-architecture skill to create context files
2. After context creation, use devforgeai-orchestration to create Sprint 1
"""

Skill(command="devforgeai-architecture")
```

**If context files exist (brownfield):**
```
Read(file_path=".devforgeai/context/tech-stack.md")
Read(file_path=".devforgeai/context/source-tree.md")

# Validate requirements against existing constraints
# Use AskUserQuestion to resolve any conflicts

Report: """
✅ Requirements documentation complete

Context files exist. Requirements validated against constraints.

Ready to proceed with:
1. devforgeai-orchestration (create sprints/stories)
2. devforgeai-development (implement features)
"""
```

---

## AskUserQuestion Best Practices

This skill relies heavily on AskUserQuestion to prevent ambiguity.

### Key Patterns

**Ambiguous Business Goal:**
```
Question: "What does 'faster' mean for this project?"
Header: "Performance target"
Options:
  - "Page load <1 second (high performance)"
  - "API response <500ms (standard performance)"
  - "User-perceived speed (no specific metric)"
```

**MVP Scope Negotiation:**
```
Question: "Full feature set would take ~6 months. What's minimum for initial release?"
Header: "MVP definition"
Options:
  - "Core workflow only (2-3 months)"
  - "Core + 2 secondary features (3-4 months)"
  - "Full feature set required (6+ months)"
  - "Help me prioritize"
```

**Technology Preference:**
```
Question: "Does your team have experience with any of these technologies?"
Header: "Team expertise"
Options: [Technology options based on requirements]
multiSelect: true
```

**Compliance Uncertainty:**
```
Question: "What type of data will this system handle?"
Header: "Data sensitivity"
Options:
  - "Health information (HIPAA required)"
  - "Payment data (PCI-DSS required)"
  - "Personal data - EU users (GDPR required)"
  - "Public/non-sensitive data"
multiSelect: true
```

**For complete elicitation patterns, load:**
```
Read(file_path=".claude/skills/devforgeai-ideation/references/requirements-elicitation-guide.md")
```

---

## Integration with Other Skills

### Flow to devforgeai-architecture

Handoff: requirements spec, complexity tier, technology constraints, compliance
Architecture skill creates 6 context files, makes technology decisions, documents ADRs

### Flow to devforgeai-orchestration

Handoff: epic documents, requirements spec, success metrics
Orchestration skill creates Sprint 1, generates stories, manages workflow

---

## Success Criteria

This skill succeeds when:

- [ ] Business problem clearly articulated (measurable)
- [ ] Requirements complete and unambiguous
- [ ] All NFRs documented with specific targets
- [ ] Complexity tier determined with rationale
- [ ] Epics created with features breakdown
- [ ] Risks and constraints identified
- [ ] Requirements documents generated
- [ ] No ambiguities remain (resolved via AskUserQuestion)
- [ ] Ready for architecture skill (clear handoff)

**Output Artifacts:**
- 1+ Epic documents (`.ai_docs/Epics/`)
- Requirements specification (`.devforgeai/specs/requirements/`)
- Complexity assessment report

**Transition Point:**
- Architecture context files created (or exist)
- Orchestration can begin sprint planning
- Development can start on first stories

---

## Reference Files

Load these as needed during ideation:

- **[Requirements Elicitation Guide](./references/requirements-elicitation-guide.md)** - Comprehensive probing questions by domain (e-commerce, SaaS, fintech, healthcare), user story templates, NFR checklists, interview techniques (723 lines)

- **[Complexity Assessment Matrix](./references/complexity-assessment-matrix.md)** - Detailed 0-60 scoring rubric across 4 dimensions with examples, architecture tier definitions, technology recommendations (700 lines)

- **[Domain-Specific Patterns](./references/domain-specific-patterns.md)** - Common features, user flows, data models, and regulatory considerations for major domains (e-commerce, SaaS, fintech, healthcare, CMS, marketplaces, workflow tools) (975 lines)

- **[Feasibility Analysis Framework](./references/feasibility-analysis-framework.md)** - Technical/business/resource feasibility checklists, risk assessment templates, MVP scoping techniques, decision frameworks (649 lines)

---

## Best Practices

- **Progressive Disclosure:** Start broad, narrow to specifics, ask 2-3 questions per interaction
- **Validation:** Summarize after each phase, confirm correctness, allow correction
- **Avoid Over-Engineering:** Match architecture to requirements, simpler is better
- **Document Assumptions:** Flag guesses for validation during architecture phase
- **Brownfield Respect:** Understand patterns before changes, propose incremental improvements

---

**The goal:** Transform business ideas into structured, actionable requirements with zero ambiguity, enabling downstream skills to implement with zero technical debt.
