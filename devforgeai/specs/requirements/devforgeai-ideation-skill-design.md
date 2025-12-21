# DevForgeAI Ideation Skill - Design Specification

**Date Created:** 2025-10-30
**Status:** Design Phase
**Purpose:** Define the ideation/brainstorming skill that initiates the DevForgeAI spec-driven development workflow

---

## Executive Summary

The **devforgeai-ideation** skill is the **entry point** for the entire DevForgeAI framework. It transforms raw business ideas, problems, or opportunities into structured requirements that feed into the Epic → Sprint → Story → Architecture → Development → QA → Release workflow.

**Key Capabilities:**
1. **Discovery & Exploration** - Understand problem space through structured questioning
2. **Requirements Elicitation** - Extract functional and non-functional requirements
3. **Epic/Feature Decomposition** - Break large ideas into manageable work units
4. **Feasibility Analysis** - Assess technical, business, and resource constraints
5. **Greenfield/Brownfield Support** - Handle both new projects and existing codebases
6. **Multi-tier Architecture Planning** - Support simple apps through complex platforms

**Integration Point:** Outputs structured requirements that feed directly into:
- `devforgeai-orchestration` (create epics/sprints/stories)
- `devforgeai-architecture` (define technical constraints)

---

## 1. Skill Metadata (SKILL.md Frontmatter)

```yaml
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
---
```

---

## 2. Skill Purpose & Philosophy

### Purpose Statement

This skill guides the **ideation and requirements discovery** phase of spec-driven development. It ensures that:

1. **Business problems are clearly understood** before solution design
2. **Requirements are complete, testable, and unambiguous**
3. **Stakeholder needs are captured systematically**
4. **Technical feasibility is assessed early**
5. **Work is decomposed appropriately** (Epic → Features → Stories)
6. **Context is established** for downstream skills

### Philosophy

**"Start with Why, Then What, Then How"**

- **Why:** Business value, user needs, success metrics
- **What:** Functional/non-functional requirements, constraints
- **How:** Technical approach (delegated to architecture skill)

**"Ask, Don't Assume"**

- Use AskUserQuestion for ALL ambiguities
- Never infer requirements from incomplete information
- Validate assumptions explicitly

**"Right-size the Solution"**

- Progressive complexity assessment (simple → moderate → complex)
- Don't over-engineer simple problems
- Don't under-architect complex platforms

---

## 3. When to Use This Skill

**Trigger Scenarios:**

✅ **Greenfield Projects:**
- "I want to build a new application for [purpose]"
- "We need a system that handles [business function]"
- "Can you help me design a platform for [use case]"

✅ **Brownfield Feature Additions:**
- "Add multi-factor authentication to our existing system"
- "We need to integrate payment processing"
- "Expand our platform to support [new capability]"

✅ **Problem Exploration:**
- "Our current system has [problem], how can we fix it?"
- "Users are complaining about [issue], what are our options?"
- "We need to improve [metric] by [target]"

✅ **Strategic Planning:**
- "We want to migrate from [old tech] to [new tech]"
- "Plan our roadmap for the next 6 months"
- "Evaluate feasibility of [ambitious idea]"

❌ **When NOT to Use:**
- Implementation of well-defined stories (use devforgeai-development)
- Architecture decisions with clear requirements (use devforgeai-architecture)
- Code quality validation (use devforgeai-qa)

---

## 4. Ideation Workflow (6 Phases)

### Phase 1: Discovery & Problem Understanding

**Objective:** Understand the business context, problem space, and desired outcomes

#### 1.1 Project Context Discovery

**Use AskUserQuestion to establish foundation:**

```
Question: "What type of project is this?"
Header: "Project type"
Description: "This determines the discovery approach"
Options:
  - "Greenfield - New project/product from scratch"
  - "Brownfield - Adding features to existing system"
  - "Modernization - Replacing/upgrading legacy system"
  - "Problem-solving - Fixing issues in current system"
multiSelect: false
```

#### 1.2 Existing System Analysis (Brownfield/Modernization Only)

**For existing systems, analyze current state:**

```
# Discover codebase
Glob(pattern="**/*.sln")         # .NET solutions
Glob(pattern="**/package.json")  # Node.js projects
Glob(pattern="**/pom.xml")       # Java projects
Glob(pattern="**/requirements.txt") # Python projects

# Check for existing DevForgeAI context
Read(file_path="devforgeai/context/tech-stack.md")
Read(file_path="devforgeai/specs/Epics/")
Read(file_path="README.md")

# Analyze current architecture
Grep(pattern="class.*Controller", type="cs")  # Find controllers
Grep(pattern="interface I.*Repository", type="cs")  # Find repositories
Grep(pattern="CREATE TABLE", glob="**/*.sql")  # Find database schema
```

**Document findings:**
- Current technology stack
- Architecture patterns in use
- Database schema
- API structure
- Deployment model
- Known pain points

#### 1.3 Problem Space Exploration

**Use AskUserQuestion for open-ended discovery:**

```
Question: "What business problem are you trying to solve?"
Header: "Problem statement"
Description: "Describe the core problem or opportunity in 1-3 sentences"
Options:
  - "Other (please specify)" [user provides custom text input]
multiSelect: false
```

**Follow-up probing questions:**
```
Question: "Who are the primary users or beneficiaries?"
Header: "Users"
Options:
  - "End customers/consumers"
  - "Internal employees"
  - "Business partners/vendors"
  - "Administrators/operators"
  - "Other (specify)"
multiSelect: true
```

```
Question: "What is the primary goal or success metric?"
Header: "Success criteria"
Options:
  - "Increase revenue/conversions"
  - "Reduce costs/inefficiency"
  - "Improve user experience"
  - "Enable new capabilities"
  - "Compliance/regulatory requirement"
  - "Other (specify)"
multiSelect: true
```

#### 1.4 Scope Boundary Definition

**Establish what's IN and OUT of scope:**

```
Question: "What is the initial scope for the MVP or first release?"
Header: "MVP scope"
Description: "Focus on minimum viable functionality"
Options:
  - "Core feature only (single user flow)"
  - "Core + 2-3 secondary features"
  - "Full feature set (comprehensive solution)"
  - "Not sure - need help defining MVP"
multiSelect: false
```

**Document scope boundaries:**
- **In Scope:** Features/capabilities included
- **Out of Scope:** Explicitly excluded items
- **Future Scope:** Deferred to later phases

---

### Phase 2: Requirements Elicitation

**Objective:** Extract functional and non-functional requirements systematically

#### 2.1 Functional Requirements Discovery

**Use structured questioning to uncover features:**

**User Stories Format:**
```
For each major feature area:

Question: "For [feature area], what should users be able to do?"
Header: "[Feature] capabilities"
Description: "Select all capabilities needed"
Options:
  - "[Capability 1 - e.g., Create new records]"
  - "[Capability 2 - e.g., View/search existing records]"
  - "[Capability 3 - e.g., Edit/update records]"
  - "[Capability 4 - e.g., Delete records]"
  - "Other (specify)"
multiSelect: true
```

**Example - E-commerce Platform:**
```
Question: "What shopping capabilities should the platform support?"
Header: "Shopping features"
Options:
  - "Browse products by category"
  - "Search products by keyword/filters"
  - "View product details and images"
  - "Add products to cart"
  - "Checkout and payment processing"
  - "Order tracking and history"
  - "Reviews and ratings"
  - "Wishlist/favorites"
multiSelect: true
```

**Capture as user stories:**
```markdown
As a [user type],
I want to [action/capability],
So that [business value/benefit].
```

#### 2.2 Data Requirements Discovery

**Identify core entities and relationships:**

```
Question: "What are the main data entities (objects) this system will manage?"
Header: "Data entities"
Description: "Select or specify the primary data objects"
Options:
  - "Users/Accounts"
  - "Products/Inventory"
  - "Orders/Transactions"
  - "Content/Documents"
  - "Events/Activities"
  - "Other (specify)"
multiSelect: true
```

**For each entity, probe for attributes:**
```
Question: "For [Entity], what information needs to be stored?"
Header: "[Entity] attributes"
Description: "Consider required vs optional fields"
Options: [Dynamic based on entity type]
multiSelect: true
```

**Relationship mapping:**
- One-to-many (User → Orders)
- Many-to-many (Products ↔ Categories)
- One-to-one (User → Profile)

#### 2.3 Integration Requirements

**External systems and APIs:**

```
Question: "Does this system need to integrate with external services?"
Header: "Integrations"
Options:
  - "Payment gateway (Stripe, PayPal, etc.)"
  - "Email service (SendGrid, AWS SES, etc.)"
  - "Authentication provider (Auth0, OAuth, etc.)"
  - "Cloud storage (S3, Azure Blob, etc.)"
  - "Analytics (Google Analytics, Mixpanel, etc.)"
  - "CRM/ERP systems"
  - "Third-party APIs"
  - "No external integrations"
multiSelect: true
```

#### 2.4 Non-Functional Requirements (NFRs)

**Performance:**
```
Question: "What are the performance requirements?"
Header: "Performance"
Options:
  - "High performance (<100ms response time, >10k concurrent users)"
  - "Standard performance (<500ms response time, 1k-10k users)"
  - "Moderate performance (<2s response time, <1k users)"
  - "Performance not critical (internal tool, low usage)"
multiSelect: false
```

**Security:**
```
Question: "What security requirements apply?"
Header: "Security"
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
Header: "Scalability"
Options:
  - "Small scale (100s of users, single server)"
  - "Medium scale (1000s of users, horizontal scaling)"
  - "Large scale (10k+ concurrent users, multi-region)"
  - "Massive scale (millions of users, global CDN)"
multiSelect: false
```

**Availability:**
```
Question: "What availability is required?"
Header: "Availability"
Options:
  - "High availability (99.9% uptime, 24/7 monitoring)"
  - "Business hours only (99% uptime during work hours)"
  - "Best effort (no SLA)"
multiSelect: false
```

---

### Phase 3: Complexity Assessment & Architecture Planning

**Objective:** Assess solution complexity and determine appropriate architecture tier

#### 3.1 Complexity Scoring

**Evaluate across dimensions:**

**Functional Complexity:**
- Number of user roles: 1-2 (Low), 3-5 (Medium), 6+ (High)
- Number of core entities: 1-3 (Low), 4-10 (Medium), 11+ (High)
- Number of integrations: 0-1 (Low), 2-4 (Medium), 5+ (High)
- Workflow complexity: Linear (Low), Branching (Medium), State machines (High)

**Technical Complexity:**
- Data volume: <10k records (Low), 10k-1M (Medium), >1M (High)
- Concurrency: <100 (Low), 100-10k (Medium), >10k (High)
- Real-time requirements: None (Low), Polling (Medium), WebSockets/Events (High)

**Team/Organizational Complexity:**
- Team size: 1-3 (Low), 4-10 (Medium), 11+ (High)
- Team distribution: Co-located (Low), Remote (Medium), Multi-timezone (High)

**Complexity Score:** Sum scores across dimensions
- **0-15 points:** Simple Application
- **16-30 points:** Moderate Application
- **31-45 points:** Complex Platform
- **46+ points:** Enterprise Platform

#### 3.2 Architecture Tier Recommendation

**Based on complexity score, recommend tier:**

**Tier 1: Simple Application (0-15 points)**
- Architecture: Monolithic (single codebase)
- Layers: 2-3 (API, Business Logic, Data)
- Database: Single database
- Deployment: Single server or serverless
- Example: Todo app, blog, portfolio site

**Tier 2: Moderate Application (16-30 points)**
- Architecture: Modular Monolith or simple microservices
- Layers: 3-4 (API, Application, Domain, Infrastructure)
- Database: Primary + optional read replicas
- Deployment: Load-balanced multi-instance
- Example: E-commerce site, SaaS tool, internal dashboard

**Tier 3: Complex Platform (31-45 points)**
- Architecture: Microservices or Clean Architecture
- Layers: 4-5 (API, Application, Domain, Infrastructure, Cross-cutting)
- Database: Multiple databases (polyglot persistence)
- Deployment: Kubernetes, service mesh
- Example: Multi-tenant SaaS, marketplace platform

**Tier 4: Enterprise Platform (46+ points)**
- Architecture: Distributed microservices with event-driven patterns
- Layers: 5+ with domain-driven design
- Database: Polyglot + event sourcing + CQRS
- Deployment: Multi-region, auto-scaling, chaos engineering
- Example: Global fintech platform, streaming service, IoT platform

**Use AskUserQuestion to validate:**
```
Question: "Based on your requirements, this appears to be a [Tier] [Name]. Does this match your expectations?"
Header: "Complexity validation"
Description: "[Brief justification of recommendation]"
Options:
  - "Yes, that's correct"
  - "No, it should be simpler (explain why)"
  - "No, it should be more complex (explain why)"
multiSelect: false
```

---

### Phase 4: Epic & Feature Decomposition

**Objective:** Break down the solution into manageable work units

#### 4.1 Epic Identification

**Group features into business-value themes:**

**Epic Definition:**
- High-level business capability or initiative
- Spans multiple sprints (4-8 weeks typical)
- Delivers measurable business value
- Can be prioritized independently

**Use AskUserQuestion for prioritization:**
```
Question: "Which epics should be prioritized for initial implementation?"
Header: "Epic priority"
Description: "Select 1-3 epics for MVP/Phase 1"
Options:
  - "Epic 1: [Name - e.g., User Management] (Est: [X] story points)"
  - "Epic 2: [Name - e.g., Product Catalog] (Est: [X] story points)"
  - "Epic 3: [Name - e.g., Order Processing] (Est: [X] story points)"
  - "Epic 4: [Name - e.g., Admin Dashboard] (Est: [X] story points)"
multiSelect: true
```

#### 4.2 Feature Breakdown

**For each epic, identify features:**

**Feature = User-facing capability that delivers value**

Example - Epic: "User Management"
- Feature 1: User Registration
- Feature 2: User Login/Authentication
- Feature 3: Profile Management
- Feature 4: Password Reset
- Feature 5: Multi-Factor Authentication

#### 4.3 Story Decomposition (High-Level)

**For priority features, outline stories:**

**Story = Atomic unit of work (1-3 days)**

Example - Feature: "User Registration"
- Story 1: Registration form with email/password
- Story 2: Email verification workflow
- Story 3: Registration validation rules
- Story 4: Registration error handling

**Note:** Detailed story creation happens in devforgeai-orchestration skill

---

### Phase 5: Feasibility & Constraints Analysis

**Objective:** Identify technical, business, and resource constraints

#### 5.1 Technical Feasibility

**Assess technical risks:**

```
Question: "Are there any technical constraints or concerns?"
Header: "Technical constraints"
Options:
  - "Must integrate with legacy systems"
  - "Must support offline functionality"
  - "Must work on low-bandwidth networks"
  - "Requires real-time data synchronization"
  - "Requires complex algorithms/ML"
  - "Requires specialized hardware"
  - "No major technical constraints"
multiSelect: true
```

**For each constraint, document:**
- Nature of constraint
- Impact on architecture/design
- Mitigation approach
- Risk level (Low/Medium/High)

#### 5.2 Business Constraints

**Budget & Resources:**
```
Question: "What are the budget and resource constraints?"
Header: "Resources"
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
Header: "Timeline"
Options:
  - "Urgent - MVP in 4-6 weeks"
  - "Standard - MVP in 2-3 months"
  - "Flexible - 4-6 months or longer"
multiSelect: false
```

#### 5.3 Risk Assessment

**Identify top risks:**

**Technical Risks:**
- Integration complexity with [external system]
- Performance at scale (untested)
- Security vulnerabilities

**Business Risks:**
- Market competition/timing
- User adoption uncertainty
- Scope creep potential

**Team Risks:**
- Knowledge gaps in [technology]
- Key person dependencies
- Distributed team communication

**For each risk:**
- Probability (Low/Medium/High)
- Impact (Low/Medium/High)
- Mitigation strategy

---

### Phase 6: Requirements Documentation & Handoff

**Objective:** Generate structured requirements documents for downstream skills

#### 6.1 Generate Epic Document(s)

**Use devforgeai-orchestration epic template:**

```
Write(file_path="devforgeai/specs/Epics/EPIC-001-[name].epic.md", content="""
---
id: EPIC-001
title: [Epic Title]
status: Planning
start_date: [Date]
target_date: [Date]
total_points: [Estimated]
created: [Date]
---

# Epic: [Title]

## Business Goal
[Clear statement of business value]

## Success Metrics
- [Metric 1: Quantifiable measure]
- [Metric 2: Quantifiable measure]

## Scope
[High-level features included]

### Features
1. [Feature 1]
2. [Feature 2]
3. [Feature 3]

## Target Sprints
[Sprint breakdown]

## Dependencies
[External dependencies]

## Stakeholders
- Product Owner: [Name]
- Tech Lead: [Name]

## Requirements

### Functional Requirements
[User stories and capabilities]

### Non-Functional Requirements
- Performance: [Targets]
- Security: [Requirements]
- Scalability: [Requirements]
- Availability: [Requirements]

### Data Requirements
[Entities, relationships, attributes]

### Integration Requirements
[External systems/APIs]

## Architecture Considerations
- Complexity Tier: [Tier N: Name]
- Recommended Architecture: [Pattern]
- Technology Constraints: [List]

## Risks & Constraints
[Top risks and mitigation strategies]

## Next Steps
1. Invoke devforgeai-architecture to create context files
2. Plan Sprint 1 with devforgeai-orchestration
3. Create detailed stories for priority features
""")
```

#### 6.2 Generate Requirements Specification

**Comprehensive technical requirements doc:**

```
Write(file_path="devforgeai/specs/requirements/[project-name]-requirements.md", content="""
# [Project Name] - Requirements Specification

## Project Context
- Type: [Greenfield/Brownfield/Modernization]
- Complexity: [Tier N]
- Target Date: [Date]

## Problem Statement
[Clear description of problem being solved]

## Solution Overview
[High-level solution approach]

## User Roles & Personas
[Detailed user types and needs]

## Functional Requirements
[Comprehensive feature list with acceptance criteria]

## Non-Functional Requirements
[Detailed NFRs: performance, security, scalability, availability]

## Data Model
[Entity definitions, relationships, constraints]

## Integration Points
[External systems, APIs, protocols]

## Architecture Recommendations
- Tier: [X]
- Pattern: [Y]
- Rationale: [Z]

## Technology Constraints
[Known technology requirements or restrictions]

## Risks & Assumptions
[Documented risks and underlying assumptions]

## Success Criteria
[Measurable outcomes for project success]
""")
```

#### 6.3 Transition to Architecture Skill

**Check if architecture context exists:**

```
# Check for existing context files
context_files_exist = all([
    file_exists("devforgeai/context/tech-stack.md"),
    file_exists("devforgeai/context/source-tree.md"),
    file_exists("devforgeai/context/dependencies.md"),
    file_exists("devforgeai/context/coding-standards.md"),
    file_exists("devforgeai/context/architecture-constraints.md"),
    file_exists("devforgeai/context/anti-patterns.md")
])

IF NOT context_files_exist:
    # Invoke architecture skill to create context
    Skill(command="devforgeai-architecture")

    Report: """
    ✅ Requirements documentation complete

    Next Steps:
    1. Architecture skill invoked to create context files
    2. After context creation, use devforgeai-orchestration to:
       - Create Sprint 1 plan
       - Generate detailed stories
    3. Begin development with devforgeai-development
    """
ELSE:
    Report: """
    ✅ Requirements documentation complete

    Context files already exist. Ready to proceed with:
    1. devforgeai-orchestration (create sprints/stories)
    2. devforgeai-development (implement features)
    """
```

---

## 5. Bundled Resources

### 5.1 Reference Files (`references/`)

**requirements-elicitation-guide.md**
- Comprehensive list of probing questions by domain
- User story templates for common features
- NFR checklists by industry (healthcare, fintech, e-commerce)

**complexity-assessment-matrix.md**
- Detailed scoring rubric for complexity dimensions
- Architecture tier definitions with examples
- Technology recommendations by tier

**domain-specific-patterns.md**
- Common patterns by domain (e-commerce, SaaS, fintech, healthcare)
- Standard features and user flows
- Regulatory considerations (GDPR, HIPAA, PCI-DSS)

**feasibility-analysis-framework.md**
- Technical risk assessment checklist
- Business viability criteria
- MVP scoping techniques (MoSCoW, Kano model)

### 5.2 Asset Templates (`assets/templates/`)

**epic-template.md**
- Pre-structured epic document (same as orchestration)

**requirements-spec-template.md**
- Comprehensive requirements specification format

**user-persona-template.md**
- Structured persona documentation

**feature-prioritization-matrix.xlsx**
- Effort vs. Value grid for feature prioritization

### 5.3 Scripts (`scripts/`)

**complexity_scorer.py**
- Automated complexity calculation from answered questions
- Architecture tier recommendation engine

**requirements_validator.py**
- Validates requirements documents for completeness
- Checks for ambiguous language ("fast", "scalable" without metrics)
- Ensures acceptance criteria are testable

---

## 6. AskUserQuestion Patterns

### Pattern 1: Ambiguous Business Goal

```
CONTEXT:
- User says "make the system faster" without metrics
- Need specific, measurable targets

AskUserQuestion:
Question: "What does 'faster' mean for this project?"
Header: "Performance target"
Description: "Specific metrics help define success and guide architecture"
Options:
  - "Page load <1 second (high performance)"
  - "API response <500ms (standard performance)"
  - "Batch processing time reduced by 50%"
  - "User-perceived speed (no specific metric)"
multiSelect: false
```

### Pattern 2: MVP Scope Negotiation

```
CONTEXT:
- User wants "everything" in MVP
- Estimated timeline is 6+ months
- Need to narrow scope

AskUserQuestion:
Question: "The full feature set would take ~6 months. What's the minimum for an initial release?"
Header: "MVP definition"
Description: "Focus on core value, iterate based on feedback"
Options:
  - "Core workflow only (2-3 months)"
  - "Core + 2 secondary features (3-4 months)"
  - "Full feature set is required (6+ months)"
  - "Help me prioritize (not sure what's core)"
multiSelect: false
```

### Pattern 3: Technology Preference Discovery

```
CONTEXT:
- Requirements suggest multiple valid tech stacks
- Team experience matters

AskUserQuestion:
Question: "Does your team have experience with any of these technologies?"
Header: "Team expertise"
Description: "Team familiarity can influence architecture decisions"
Options:
  - ".NET/C#"
  - "Node.js/TypeScript"
  - "Python"
  - "Java/Spring"
  - "No preference - choose best fit"
multiSelect: true
```

### Pattern 4: Compliance Uncertainty

```
CONTEXT:
- Application handles sensitive data
- Compliance requirements unclear

AskUserQuestion:
Question: "What type of data will this system handle?"
Header: "Data sensitivity"
Description: "Determines security and compliance requirements"
Options:
  - "Health information (HIPAA compliance required)"
  - "Payment data (PCI-DSS compliance required)"
  - "Personal data - EU users (GDPR compliance required)"
  - "Sensitive business data (standard security)"
  - "Public/non-sensitive data"
multiSelect: true
```

---

## 7. Integration with Other Skills

### Flow to devforgeai-architecture

**Handoff Data:**
- Requirements specification document
- Complexity tier recommendation
- Known technology constraints
- Compliance requirements

**Architecture skill will:**
- Create 6 context files (tech-stack, source-tree, dependencies, etc.)
- Make technology decisions (with AskUserQuestion)
- Create ADRs for major decisions

### Flow to devforgeai-orchestration

**Handoff Data:**
- Epic documents with features
- Requirements specification
- Success metrics

**Orchestration skill will:**
- Create Sprint 1 plan
- Generate detailed stories from features
- Manage story workflow (Architecture → Dev → QA → Release)

---

## 8. Success Criteria

**Ideation skill succeeds when:**

- [ ] Business problem clearly articulated (measurable)
- [ ] Requirements complete and unambiguous
- [ ] All NFRs documented with specific targets
- [ ] Complexity tier determined
- [ ] Epics created with features
- [ ] Risks and constraints identified
- [ ] Requirements documents generated
- [ ] No ambiguities remain (all resolved via AskUserQuestion)
- [ ] Ready for architecture skill (clear handoff)

**Output Artifacts:**
- 1+ Epic documents (`devforgeai/specs/Epics/`)
- Requirements specification (`devforgeai/specs/requirements/`)
- Complexity assessment report

**Transition Point:**
- Architecture context files created (or exist)
- Orchestration can begin sprint planning
- Development can start on first stories

---

## 9. Example Walkthrough

### Scenario: "Build me an e-commerce platform"

**Phase 1: Discovery**
- Project type: Greenfield
- Problem: Need online storefront to sell products
- Users: Customers (buyers), Admins (manage products/orders)
- Success: $10k revenue in first 3 months

**Phase 2: Requirements**
- Functional: Product catalog, shopping cart, checkout, order management
- Data: Products, Orders, Users, Categories
- Integrations: Stripe (payment), SendGrid (email)
- NFRs: Standard performance (<500ms), 99% availability, GDPR compliance

**Phase 3: Complexity**
- Score: 22 points (Moderate Application - Tier 2)
- Architecture: Modular Monolith with Clean Architecture
- Database: PostgreSQL (primary) + Redis (cache)

**Phase 4: Decomposition**
- Epic 1: Product Catalog (5 stories)
- Epic 2: Shopping & Checkout (8 stories)
- Epic 3: Order Management (5 stories)
- Epic 4: Admin Dashboard (6 stories)
- MVP: Epic 1 + Epic 2 (13 stories, ~4 weeks)

**Phase 5: Feasibility**
- Technical: Stripe integration complexity (Medium risk)
- Business: Timeline aggressive but achievable
- Team: Need 2-3 developers + designer

**Phase 6: Documentation**
- Generated 4 epic documents
- Generated requirements spec
- Invoked devforgeai-architecture

**Result:** Ready for architecture skill to create context files, then orchestration to create Sprint 1.

---

## 10. Notes & Best Practices

**Progressive Disclosure:**
- Start broad (problem space)
- Narrow to specifics (features, NFRs)
- Don't overwhelm with 20 questions upfront

**Validation at Each Phase:**
- Summarize understanding after each phase
- Ask "Is this correct?" before proceeding
- Allow course correction

**Avoid Over-Engineering:**
- If complexity score suggests Tier 1, don't default to microservices
- Match architecture to actual requirements

**Document Assumptions:**
- When making educated guesses (with user validation), document as assumptions
- Flag for validation during architecture phase

**Brownfield Respect:**
- Don't propose wholesale rewrites lightly
- Understand existing patterns before suggesting changes
- Propose incremental improvements where possible

---

## 11. Future Enhancements

**Potential Additions:**
- Market research integration (WebFetch for competitor analysis)
- Cost estimation (cloud infrastructure, licensing)
- AI-powered requirements extraction from existing docs
- Visual diagramming output (architecture diagrams)
- Automated persona generation from analytics data

---

**End of Design Specification**
