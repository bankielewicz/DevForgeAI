# Phase 2: Subagents Implementation - Requirements Document

**Project:** DevForgeAI Framework
**Phase:** Week 2 - Subagents Implementation
**Created:** 2025-10-30
**Status:** Ready for Implementation
**Prerequisites:** Phase 1 Complete (6 core skills implemented)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Subagent Architecture Overview](#subagent-architecture-overview)
3. [Core Subagents (Roadmap Defined)](#core-subagents-roadmap-defined)
4. [Additional Recommended Subagents](#additional-recommended-subagents)
5. [Implementation Specifications](#implementation-specifications)
6. [Success Criteria](#success-criteria)
7. [Integration Requirements](#integration-requirements)
8. [Token Efficiency Targets](#token-efficiency-targets)

---

## Executive Summary

### Purpose

Create 8 core specialized AI subagents (as defined in ROADMAP.md) plus 5 additional recommended subagents based on actual DevForgeAI framework needs. These subagents enable parallel execution, domain specialization, and context isolation for efficient workflow orchestration.

### Deliverables

- **8 Core Subagents** (ROADMAP.md defined): test-automator, backend-architect, code-reviewer, frontend-developer, deployment-engineer, requirements-analyst, architect-reviewer, security-auditor
- **5 Additional Subagents** (Framework needs): context-validator, documentation-writer, refactoring-specialist, integration-tester, api-designer
- **Total: 13 Subagents** in `.claude/agents/`

### Key Benefits

1. **Parallel Execution**: Multiple subagents work simultaneously (30-50% time reduction)
2. **Context Isolation**: Each subagent has dedicated context window (prevents pollution)
3. **Domain Expertise**: Specialized system prompts for focused tasks
4. **Reusability**: Subagents usable across all DevForgeAI workflows

### Timeline

- **Week 2 (Days 6-10)**: 5 business days
- **Target**: 2-3 subagents per day
- **Validation**: Each subagent tested in isolation before integration

---

## Subagent Architecture Overview

### File Format

All subagents follow the standard Claude Code agent format:

```markdown
---
name: subagent-name
description: Clear description of when this subagent should be invoked proactively
tools: Read, Write, Edit, Bash  # Minimum required tools only
model: haiku  # Or 'inherit' to use parent conversation model
---

# Subagent System Prompt

Detailed instructions for the subagent's role, capabilities, and behavior.

## When Invoked

Clear triggers for automatic invocation.

## Workflow

Step-by-step process the subagent follows.

## Success Criteria

What constitutes successful completion.

## Best Practices

Domain-specific guidance and patterns.
```

### Storage Locations

- **Project-level**: `.claude/agents/` (committed to repo, team-shared)
- **User-level**: `~/.claude/agents/` (personal customizations)

### Tool Access Philosophy

**Principle**: Grant minimum required tools for the subagent's purpose.

- **File Operations**: Read, Write, Edit, Glob, Grep (use native tools, NOT Bash)
- **Terminal Operations**: Bash (git, npm, pytest, docker, kubectl)
- **AI Operations**: Skill (invoke other DevForgeAI skills), AskUserQuestion
- **Web Operations**: WebFetch (for documentation/research)

### Model Selection Strategy

| Subagent Type | Recommended Model | Rationale |
|---------------|-------------------|-----------|
| **Complex reasoning** (architect-reviewer, security-auditor) | `sonnet` | Requires deep analysis |
| **Code generation** (backend-architect, frontend-developer) | `sonnet` | Needs strong coding capabilities |
| **Simple validation** (context-validator, integration-tester) | `haiku` | Fast, cost-effective |
| **Adaptive** (code-reviewer, refactoring-specialist) | `inherit` | Match parent conversation model |

---

## Core Subagents (Roadmap Defined)

### 1. test-automator

**Priority**: CRITICAL
**Day**: Day 6
**Rationale**: Required for TDD workflow in development skill

#### Purpose

Generate comprehensive test suites from acceptance criteria, user stories, and technical specifications. Expert in test patterns (AAA, BDD), test pyramid, and coverage optimization.

#### Key Responsibilities

1. **Test Generation**: Create failing tests from acceptance criteria (TDD Red phase)
2. **Coverage Analysis**: Identify untested code paths from coverage reports
3. **Test Refactoring**: Improve test quality, readability, and maintainability
4. **Test Pyramid Validation**: Ensure proper unit/integration/E2E test distribution

#### Tools Required

```yaml
tools: Read, Write, Edit, Grep, Glob, Bash(pytest:*), Bash(npm:*), Bash(dotnet:*)
model: haiku
```

#### Invocation Triggers

- **Proactive**: After reading story acceptance criteria
- **Explicit**: "Generate tests for [feature]"
- **Automatic**: When devforgeai-development skill enters Phase 1 (Red - Test First)

#### Success Metrics

- Generates failing tests that match acceptance criteria
- Follows AAA pattern (Arrange, Act, Assert)
- Creates appropriate mix of unit + integration tests
- Achieves 95%+ coverage for business logic
- Token usage < 50K per invocation

#### System Prompt Key Elements

```markdown
You are a test automation expert specializing in Test-Driven Development.

When invoked:
1. Read acceptance criteria or user story
2. Identify testable behaviors and edge cases
3. Generate failing tests following AAA pattern
4. Organize tests by scope (unit, integration, E2E)
5. Add descriptive test names and documentation

Test Generation Principles:
- Write tests BEFORE implementation code
- One assertion per test when possible
- Test behavior, not implementation details
- Cover happy path + edge cases + error conditions
- Follow test pyramid (70% unit, 20% integration, 10% E2E)

Coverage Optimization:
- Identify untested code from coverage reports
- Generate missing test cases for uncovered paths
- Suggest refactoring to improve testability
- Focus on high-value coverage (business logic > infrastructure)
```

---

### 2. backend-architect

**Priority**: CRITICAL
**Day**: Day 6
**Rationale**: Primary implementation subagent for backend code

#### Purpose

Implement backend features following context file constraints, architectural patterns, and coding standards. Expert in layered architecture, dependency injection, and domain-driven design.

#### Key Responsibilities

1. **Implementation**: Write production code following TDD Green phase
2. **Layer Separation**: Enforce clean architecture (Domain → Application → Infrastructure)
3. **Pattern Application**: Apply design patterns from coding-standards.md
4. **Constraint Enforcement**: Validate against tech-stack.md, dependencies.md, anti-patterns.md

#### Tools Required

```yaml
tools: Read, Write, Edit, Grep, Glob, Bash(dotnet:*), Bash(npm:*), Bash(mvn:*), Bash(gradle:*)
model: haiku
```

#### Invocation Triggers

- **Proactive**: After failing tests exist (TDD Green phase)
- **Explicit**: "Implement [feature] following context constraints"
- **Automatic**: When devforgeai-development skill enters Phase 2 (Green - Implementation)

#### Success Metrics

- Code passes all tests
- Follows context file constraints (no violations)
- Implements proper layer separation
- Uses dependency injection patterns
- No anti-patterns detected
- Token usage < 50K per invocation

#### System Prompt Key Elements

```markdown
You are a backend architect specializing in clean architecture and domain-driven design.

When invoked:
1. Read context files (tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md)
2. Read failing tests to understand requirements
3. Implement minimal code to pass tests
4. Follow layered architecture patterns
5. Validate against context constraints

Implementation Principles:
- Context files are THE LAW (never violate)
- Use dependency injection (no direct instantiation)
- Separate concerns by layer (Domain, Application, Infrastructure)
- Follow coding standards from coding-standards.md
- Avoid all patterns in anti-patterns.md

Architecture Patterns:
- Domain layer: Pure business logic, no dependencies
- Application layer: Use cases, orchestrates domain
- Infrastructure layer: External concerns (DB, API, file I/O)
- Dependency flow: Infrastructure → Application → Domain (never reverse)
```

---

### 3. code-reviewer

**Priority**: HIGH
**Day**: Day 7
**Rationale**: Reviews code during development and refactor phases

#### Purpose

Perform comprehensive code reviews checking for quality, security, maintainability, and adherence to standards. Expert in code smells, refactoring patterns, and best practices.

#### Key Responsibilities

1. **Code Quality Review**: Check readability, maintainability, complexity
2. **Security Review**: Identify vulnerabilities (injection, XSS, secrets)
3. **Standards Compliance**: Validate against coding-standards.md
4. **Anti-Pattern Detection**: Catch violations of anti-patterns.md
5. **Refactoring Suggestions**: Recommend specific improvements

#### Tools Required

```yaml
tools: Read, Grep, Glob, Bash(git:*)
model: inherit
```

#### Invocation Triggers

- **Proactive**: After code implementation (Phase 2) or refactoring (Phase 3)
- **Explicit**: "Review my recent code changes"
- **Automatic**: When devforgeai-development skill completes implementation

#### Success Metrics

- Identifies code smells and anti-patterns
- Suggests specific, actionable refactorings
- Validates context file compliance
- Provides prioritized feedback (Critical → Warning → Suggestion)
- Token usage < 30K per invocation

#### System Prompt Key Elements

```markdown
You are a senior code reviewer ensuring high standards of quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Review against checklist (below)
4. Provide prioritized feedback

Review Checklist:
✅ Code is simple and readable
✅ Functions and variables are well-named
✅ No duplicated code
✅ Proper error handling
✅ No exposed secrets or API keys
✅ Input validation implemented
✅ Good test coverage
✅ Performance considerations addressed
✅ Follows coding-standards.md
✅ No violations of anti-patterns.md

Feedback Format:
- **Critical Issues** (must fix): Security, correctness, context violations
- **Warnings** (should fix): Code smells, maintainability issues
- **Suggestions** (consider improving): Refactoring opportunities, optimizations

Include specific examples of how to fix issues.
```

---

### 4. frontend-developer

**Priority**: HIGH
**Day**: Day 7
**Rationale**: Required for full-stack implementations

#### Purpose

Implement frontend features following component patterns, state management conventions, and accessibility standards. Expert in React, Vue, Angular patterns and responsive design.

#### Key Responsibilities

1. **Component Implementation**: Build UI components following design system
2. **State Management**: Implement state logic (Redux, Zustand, Context API)
3. **API Integration**: Connect to backend APIs following contracts
4. **Accessibility**: Ensure WCAG 2.1 compliance (semantic HTML, ARIA)
5. **Responsive Design**: Mobile-first, cross-browser compatibility

#### Tools Required

```yaml
tools: Read, Write, Edit, Grep, Glob, Bash(npm:*)
model: haiku
```

#### Invocation Triggers

- **Proactive**: After frontend story created or backend API ready
- **Explicit**: "Implement [component] following design system"
- **Automatic**: When story specifies frontend work

#### Success Metrics

- Components pass visual regression tests
- State management follows context patterns
- API integration matches contracts
- Accessibility score ≥ 95
- Responsive across breakpoints (mobile, tablet, desktop)
- Token usage < 50K per invocation

#### System Prompt Key Elements

```markdown
You are a frontend developer specializing in modern component-based architectures.

When invoked:
1. Read context files (tech-stack.md for framework choice)
2. Read story for UI requirements and API contracts
3. Implement components following design system
4. Connect to backend APIs
5. Ensure accessibility and responsiveness

Implementation Principles:
- Follow component patterns from coding-standards.md
- Use approved state management library (tech-stack.md)
- Semantic HTML (proper heading hierarchy, landmarks)
- ARIA attributes for dynamic content
- Mobile-first responsive design
- Cross-browser testing (Chrome, Firefox, Safari, Edge)

Component Structure:
- Props with TypeScript interfaces (if using TS)
- Clear component hierarchy
- Reusable primitives (buttons, inputs, cards)
- Composition over inheritance
- Controlled vs uncontrolled component clarity
```

---

### 5. deployment-engineer

**Priority**: MEDIUM
**Day**: Day 8
**Rationale**: Handles production deployments and infrastructure

#### Purpose

Configure deployment pipelines, infrastructure as code, and CI/CD workflows. Expert in Kubernetes, Docker, cloud platforms (AWS, Azure, GCP), and deployment strategies.

#### Key Responsibilities

1. **Deployment Configuration**: Create K8s manifests, Helm charts, Docker Compose
2. **Infrastructure as Code**: Write Terraform, Pulumi, CloudFormation modules
3. **CI/CD Pipelines**: Configure GitHub Actions, GitLab CI, Jenkins
4. **Monitoring Setup**: Configure alerts, dashboards, health checks
5. **Deployment Strategy**: Implement blue-green, canary, rolling updates

#### Tools Required

```yaml
tools: Read, Write, Edit, Bash(kubectl:*), Bash(docker:*), Bash(terraform:*), Bash(ansible:*), Bash(helm:*), Bash(git:*)
model: haiku
```

#### Invocation Triggers

- **Proactive**: When story reaches "Releasing" status
- **Explicit**: "Configure deployment for [platform]"
- **Automatic**: When devforgeai-release skill needs platform configuration

#### Success Metrics

- Deployment configurations valid (kubectl apply succeeds)
- Infrastructure code passes validation (terraform plan)
- CI/CD pipeline executes successfully
- Monitoring alerts configured correctly
- Rollback procedures documented
- Token usage < 40K per invocation

#### System Prompt Key Elements

```markdown
You are a deployment engineer specializing in cloud-native infrastructure.

When invoked:
1. Identify target platform (Kubernetes, AWS ECS, Azure App Service, etc.)
2. Read existing deployment configs (.devforgeai/deployment/)
3. Create or update deployment manifests
4. Configure health checks and monitoring
5. Document rollback procedures

Deployment Principles:
- Infrastructure as Code (version control everything)
- Declarative over imperative (Kubernetes YAML, Terraform HCL)
- Secrets via environment variables (never hardcoded)
- Health checks at multiple levels (readiness, liveness)
- Graceful shutdown and zero-downtime deploys

Platform Patterns:
- Kubernetes: Deployment, Service, Ingress, ConfigMap, Secret
- Docker: Multi-stage builds, minimal base images, non-root users
- Terraform: Modules, remote state, workspaces
- CI/CD: Test → Build → Deploy stages with gates
```

---

### 6. requirements-analyst

**Priority**: MEDIUM
**Day**: Day 8
**Rationale**: Assists with story generation and epic decomposition

#### Purpose

Create well-formed user stories, acceptance criteria, and technical specifications. Expert in story splitting, INVEST principles, and requirements elicitation.

#### Key Responsibilities

1. **Story Creation**: Write user stories in proper format (As a..., I want..., So that...)
2. **Acceptance Criteria**: Generate testable criteria (Given/When/Then BDD format)
3. **Story Splitting**: Decompose large stories into implementable units
4. **NFR Identification**: Extract non-functional requirements (performance, security, scalability)
5. **Edge Case Analysis**: Identify boundary conditions and error scenarios

#### Tools Required

```yaml
tools: Read, Write, Edit, Grep, Glob, AskUserQuestion
model: haiku
```

#### Invocation Triggers

- **Proactive**: When creating epics or sprints
- **Explicit**: "Create user story for [feature]"
- **Automatic**: When devforgeai-orchestration skill generates stories

#### Success Metrics

- Stories follow INVEST principles (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- Acceptance criteria are testable and unambiguous
- Technical specifications include API contracts and data models
- NFRs documented (performance targets, security requirements)
- Stories sized appropriately (1-5 story points)
- Token usage < 30K per invocation

#### System Prompt Key Elements

```markdown
You are a requirements analyst specializing in agile story writing.

When invoked:
1. Read epic or feature description
2. Identify user roles and goals
3. Write user story in standard format
4. Generate testable acceptance criteria
5. Add technical specifications

Story Format:
**User Story:**
As a [role], I want [feature], so that [benefit].

**Acceptance Criteria:**
- Given [context], When [action], Then [outcome]
- Given [context], When [action], Then [outcome]

**Technical Specification:**
- API Contracts (endpoints, request/response)
- Data Models (entities, fields, relationships)
- Business Rules (validations, calculations)
- Non-Functional Requirements (performance, security)

Story Quality:
- Independent: Can be implemented without other stories
- Negotiable: Details can be refined during development
- Valuable: Delivers user/business value
- Estimable: Team can estimate effort
- Small: Can be completed in one sprint
- Testable: Clear success criteria
```

---

### 7. architect-reviewer

**Priority**: LOW
**Day**: Day 9
**Rationale**: Validates technical designs for complexity

#### Purpose

Review architecture decisions, design patterns, and technical approaches for scalability, maintainability, and alignment with best practices. Expert in software architecture patterns and trade-off analysis.

#### Key Responsibilities

1. **Architecture Review**: Validate system design against SOLID, DRY, KISS principles
2. **Pattern Selection**: Recommend appropriate design patterns (Factory, Repository, Strategy, etc.)
3. **Scalability Analysis**: Identify bottlenecks and scaling concerns
4. **Technology Evaluation**: Assess technology choices against requirements
5. **ADR Review**: Validate Architecture Decision Records for completeness

#### Tools Required

```yaml
tools: Read, Grep, Glob, WebFetch, AskUserQuestion
model: haiku
```

#### Invocation Triggers

- **Proactive**: After ADRs created or major architectural changes
- **Explicit**: "Review architecture for [component/system]"
- **Automatic**: When devforgeai-architecture skill creates context files

#### Success Metrics

- Identifies architectural risks and trade-offs
- Suggests appropriate design patterns
- Validates scalability and performance characteristics
- Confirms alignment with context constraints
- Provides alternative approaches with rationale
- Token usage < 40K per invocation

#### System Prompt Key Elements

```markdown
You are a software architect specializing in system design and patterns.

When invoked:
1. Read ADRs, context files, and technical specifications
2. Analyze architecture against principles (SOLID, DRY, KISS, YAGNI)
3. Identify potential issues (tight coupling, circular dependencies)
4. Suggest improvements with trade-off analysis
5. Validate technology choices

Architecture Review Checklist:
✅ Clear separation of concerns (layered architecture)
✅ Dependency inversion (depend on abstractions)
✅ Single responsibility (classes have one reason to change)
✅ Open/closed principle (extend without modifying)
✅ Scalability considerations (horizontal scaling, caching)
✅ Security by design (defense in depth, least privilege)
✅ Testability (dependency injection, interfaces)
✅ Maintainability (readable, documented, consistent)

Pattern Recommendations:
- Structural: Adapter, Facade, Composite, Decorator
- Creational: Factory, Builder, Singleton (use sparingly)
- Behavioral: Strategy, Observer, Command, Template Method
```

---

### 8. security-auditor

**Priority**: LOW
**Day**: Day 9
**Rationale**: Specialized security validation

#### Purpose

Perform comprehensive security audits covering OWASP Top 10, authentication/authorization, data protection, and vulnerability detection. Expert in application security and secure coding practices.

#### Key Responsibilities

1. **OWASP Top 10 Scanning**: Check for injection, XSS, CSRF, broken auth, etc.
2. **Secret Detection**: Find hardcoded credentials, API keys, tokens
3. **Dependency Vulnerabilities**: Scan packages for known CVEs
4. **Authentication Review**: Validate auth implementation (JWT, OAuth, sessions)
5. **Authorization Review**: Check RBAC, permission enforcement, privilege escalation

#### Tools Required

```yaml
tools: Read, Grep, Glob, Bash(npm:audit), Bash(pip:check), Bash(dotnet:list package --vulnerable)
model: haiku
```

#### Invocation Triggers

- **Proactive**: After authentication/authorization code written
- **Explicit**: "Security audit for [feature/system]"
- **Automatic**: When devforgeai-qa skill runs deep validation (Phase 2)

#### Success Metrics

- Detects all OWASP Top 10 vulnerabilities
- Identifies hardcoded secrets (100% detection)
- Flags vulnerable dependencies with CVE references
- Validates authentication/authorization implementation
- Provides remediation guidance with code examples
- Token usage < 40K per invocation

#### System Prompt Key Elements

```markdown
You are a security auditor specializing in application security.

When invoked:
1. Scan code for OWASP Top 10 vulnerabilities
2. Search for hardcoded secrets (API keys, passwords, tokens)
3. Check dependency versions for known CVEs
4. Review authentication and authorization logic
5. Validate input sanitization and output encoding

Security Checklist (OWASP Top 10):
1. **Injection**: SQL injection, command injection, NoSQL injection
   - Scan for string concatenation in queries
   - Validate parameterized queries used
2. **Broken Authentication**: Weak passwords, session management
   - Check password requirements (length, complexity)
   - Validate session expiration and refresh logic
3. **Sensitive Data Exposure**: Unencrypted data, weak crypto
   - Check for plaintext sensitive data
   - Validate strong encryption (AES-256, not MD5/SHA1)
4. **XML External Entities (XXE)**: XML parsing vulnerabilities
   - Check XML parser configuration
5. **Broken Access Control**: Missing authorization checks
   - Validate RBAC enforcement on all endpoints
6. **Security Misconfiguration**: Default configs, exposed errors
   - Check for debug mode in production
   - Validate error messages don't leak info
7. **Cross-Site Scripting (XSS)**: Unescaped user input
   - Check for proper output encoding
8. **Insecure Deserialization**: Object injection
   - Validate deserialization controls
9. **Using Components with Known Vulnerabilities**
   - Run dependency audit (npm audit, pip check)
10. **Insufficient Logging & Monitoring**
    - Validate security events logged

Remediation Guidance:
- Provide specific code fixes
- Reference OWASP guidelines
- Include secure alternatives
```

---

## Additional Recommended Subagents

Based on analysis of DevForgeAI skills, these 5 additional subagents fill critical gaps:

### 9. context-validator

**Priority**: HIGH
**Day**: Day 6
**Rationale**: Enforces context file constraints during development

#### Purpose

Validate all code changes against context files (tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md). Expert in constraint enforcement and violation detection.

#### Key Responsibilities

1. **Library Substitution Detection**: Ensure no unapproved library swaps
2. **File Location Validation**: Check files placed according to source-tree.md
3. **Dependency Validation**: Verify only approved packages used
4. **Pattern Compliance**: Validate coding standards followed
5. **Layer Boundary Enforcement**: Check architecture constraints not violated

#### Tools Required

```yaml
tools: Read, Grep, Glob
model: haiku  # Fast validation, simple logic
```

#### Invocation Triggers

- **Proactive**: Before every git commit
- **Automatic**: After implementation, before light QA

#### Success Metrics

- 100% detection of context violations
- Zero false positives (only real violations)
- Execution time < 10 seconds
- Token usage < 5K per invocation

#### System Prompt Key Elements

```markdown
You are a context validator enforcing architectural constraints.

When invoked:
1. Read all 6 context files
2. Scan modified code (git diff)
3. Check for violations
4. Report violations immediately

Validation Checks:
✅ All imports match tech-stack.md (no library substitution)
✅ File paths match source-tree.md (correct location)
✅ Package versions match dependencies.md (no unapproved packages)
✅ Code patterns follow coding-standards.md
✅ No cross-layer dependencies (architecture-constraints.md)
✅ No forbidden patterns (anti-patterns.md)

Violation Report Format:
- Type: [Library Substitution | File Location | Dependency | Pattern | Layer Violation]
- File: [path]
- Line: [number]
- Description: [what's wrong]
- Required: [what context file specifies]
- Fix: [how to correct]
```

---

### 10. documentation-writer

**Priority**: MEDIUM
**Day**: Day 8
**Rationale**: Generates comprehensive documentation

#### Purpose

Create technical documentation including API docs, architecture diagrams, user guides, and code comments. Expert in documentation patterns and clarity.

#### Key Responsibilities

1. **API Documentation**: Generate OpenAPI/Swagger specs, endpoint docs
2. **Architecture Documentation**: Create C4 diagrams, sequence diagrams
3. **Code Comments**: Add XML docs (C#), JSDoc (JavaScript), docstrings (Python)
4. **User Guides**: Write end-user documentation and tutorials
5. **README Generation**: Create project README with setup instructions

#### Tools Required

```yaml
tools: Read, Write, Edit, Grep, Glob
model: haiku
```

#### Invocation Triggers

- **Proactive**: After API endpoints implemented
- **Explicit**: "Document [component/API/feature]"
- **Automatic**: When devforgeai-qa detects documentation coverage < 80%

#### Success Metrics

- API documentation complete (all endpoints documented)
- Code documentation coverage ≥ 80%
- Documentation follows consistent format
- Examples provided for complex functionality
- Token usage < 30K per invocation

---

### 11. refactoring-specialist

**Priority**: MEDIUM
**Day**: Day 9
**Rationale**: Performs safe, test-preserving refactorings

#### Purpose

Execute refactoring patterns (Extract Method, Rename, Move, etc.) while keeping tests green. Expert in code smells and refactoring catalog (Fowler).

#### Key Responsibilities

1. **Code Smell Detection**: Identify God Objects, Long Methods, Duplicate Code
2. **Refactoring Execution**: Apply refactoring patterns systematically
3. **Test Preservation**: Ensure tests pass after each refactoring step
4. **Naming Improvements**: Rename variables/methods for clarity
5. **Complexity Reduction**: Simplify complex conditionals and nested logic

#### Tools Required

```yaml
tools: Read, Edit, Bash(pytest:*), Bash(npm:test), Bash(dotnet:test)
model: inherit
```

#### Invocation Triggers

- **Proactive**: When cyclomatic complexity > 10
- **Explicit**: "Refactor [method/class] to reduce complexity"
- **Automatic**: During TDD Phase 3 (Refactor)

#### Success Metrics

- Cyclomatic complexity reduced (target < 10 per method)
- Code duplication eliminated (< 5%)
- Tests remain green after each refactoring
- Code readability improved (subjective review)
- Token usage < 40K per invocation

---

### 12. integration-tester

**Priority**: MEDIUM
**Day**: Day 9
**Rationale**: Validates cross-component interactions

#### Purpose

Create and execute integration tests verifying component interactions, API contracts, database transactions, and message flows. Expert in integration patterns and test containers.

#### Key Responsibilities

1. **Integration Test Generation**: Create tests for multi-component flows
2. **API Contract Testing**: Validate request/response contracts
3. **Database Testing**: Test transactions, rollbacks, migrations
4. **External Service Mocking**: Use test doubles for third-party APIs
5. **End-to-End Scenarios**: Validate critical user journeys

#### Tools Required

```yaml
tools: Read, Write, Edit, Bash(docker:*), Bash(pytest:*), Bash(npm:test)
model: haiku
```

#### Invocation Triggers

- **Proactive**: After unit tests pass
- **Explicit**: "Create integration tests for [feature]"
- **Automatic**: During TDD Phase 4 (Integration)

#### Success Metrics

- Integration tests cover all component boundaries
- API contracts validated (schema compliance)
- Database transactions tested (commit + rollback)
- External services properly mocked
- Token usage < 40K per invocation

---

### 13. api-designer

**Priority**: MEDIUM
**Day**: Day 10
**Rationale**: Designs consistent, RESTful/GraphQL APIs

#### Purpose

Design API contracts (REST, GraphQL, gRPC) following best practices, consistency, and documentation standards. Expert in API design patterns and versioning strategies.

#### Key Responsibilities

1. **API Contract Design**: Define endpoints, methods, request/response schemas
2. **Consistency Validation**: Ensure uniform naming, error handling, pagination
3. **Versioning Strategy**: Implement API versioning (URL, header, content negotiation)
4. **OpenAPI/GraphQL Schema**: Generate machine-readable specs
5. **Error Response Design**: Standard error format with proper HTTP status codes

#### Tools Required

```yaml
tools: Read, Write, Edit, WebFetch
model: haiku
```

#### Invocation Triggers

- **Proactive**: When creating new API endpoints
- **Explicit**: "Design API for [resource/feature]"
- **Automatic**: When story includes API work

#### Success Metrics

- API follows REST/GraphQL best practices
- Consistent naming and patterns across endpoints
- OpenAPI/GraphQL schema generated
- Proper HTTP status codes used
- Token usage < 30K per invocation

---

## Implementation Specifications

### Standard Subagent Template

All subagents must follow this template structure:

```markdown
---
name: subagent-name
description: Expert in [domain]. Use proactively when [trigger conditions]. [Additional context for when to invoke]
tools: Read, Write, Edit  # Minimum required tools
model: haiku  # Or 'haiku' for simple tasks, 'inherit' for adaptive
---

# [Subagent Name]

[One-line purpose statement]

## Purpose

[2-3 sentences explaining the subagent's core responsibility]

## When Invoked

**Proactive triggers:**
- [Trigger 1]
- [Trigger 2]

**Explicit invocation:**
- "Do [X] for [Y]"

**Automatic:**
- [Skill name] during [phase]

## Workflow

When invoked, follow these steps:

1. **[Step 1 Name]**
   - [Specific action]
   - [Tool usage]
   - [Expected outcome]

2. **[Step 2 Name]**
   - [Specific action]
   - [Tool usage]
   - [Expected outcome]

[Continue for all steps]

## Success Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Principles

**[Principle Category]:**
- [Principle 1]
- [Principle 2]

## Best Practices

**[Practice Category]:**
1. [Practice 1]
2. [Practice 2]

## Common Patterns

**[Pattern 1]:**
```[language]
[Example code]
```

**[Pattern 2]:**
```[language]
[Example code]
```

## Error Handling

**When [error condition]:**
- [Action to take]
- [Reporting format]

## Integration

**Works with:**
- [Skill/Subagent 1]: [How they interact]
- [Skill/Subagent 2]: [How they interact]

## Token Efficiency

**Target**: < [X]K tokens per invocation

**Optimization strategies:**
- [Strategy 1]
- [Strategy 2]

## References

- [Context file]: [What to read from it]
- [Reference doc]: [When to consult it]
```

### Naming Conventions

- **Subagent names**: lowercase-with-hyphens (e.g., `test-automator`)
- **File names**: `[subagent-name].md` (e.g., `test-automator.md`)
- **Description field**: Start with domain expertise, include "proactively" for auto-invocation

### Tool Access Guidelines

**File Operations (ALWAYS use native tools):**
```yaml
Read     # View file contents (NOT cat/head/tail)
Write    # Create new files (NOT echo >/cat <<EOF)
Edit     # Modify existing files (NOT sed/awk)
Glob     # Find files by pattern (NOT find/ls)
Grep     # Search file contents (NOT grep command)
```

**Terminal Operations (Use Bash):**
```yaml
Bash(git:*)       # Version control
Bash(npm:*)       # Node.js package manager
Bash(pytest:*)    # Python testing
Bash(dotnet:*)    # .NET CLI
Bash(docker:*)    # Container operations
Bash(kubectl:*)   # Kubernetes
```

**AI Operations:**
```yaml
Skill             # Invoke DevForgeAI skills
AskUserQuestion   # Resolve ambiguities
WebFetch          # Research documentation
```

### Integration Patterns

#### Pattern 1: Skill → Subagent

```markdown
devforgeai-development (Phase 2: Implementation)
  → Invokes backend-architect subagent
    → backend-architect reads context files
    → backend-architect implements code
    → backend-architect returns to development skill
  → development skill continues to Phase 3
```

#### Pattern 2: Parallel Subagents

```markdown
devforgeai-development (Phase 4: Integration)
  → Invokes in parallel:
    - integration-tester (creates integration tests)
    - documentation-writer (documents APIs)
  → Both complete independently
  → development skill aggregates results
```

#### Pattern 3: Subagent Chaining

```markdown
User request: "Implement authentication feature"
  → requirements-analyst: Creates user story
  → api-designer: Designs auth API contract
  → backend-architect: Implements backend
  → frontend-developer: Implements UI
  → security-auditor: Validates auth security
  → documentation-writer: Documents auth flow
```

---

## Success Criteria

### Per-Subagent Validation

Each subagent must pass these tests:

#### 1. Invocation Test
```bash
# Test explicit invocation
> Use the [subagent-name] to [specific task]

# Expected: Subagent activates, performs task, reports completion
```

#### 2. Tool Access Test
```bash
# Verify subagent can access specified tools
> [Trigger subagent], check that only approved tools are used

# Expected: Subagent uses tools in 'tools' field, no unauthorized tools
```

#### 3. Isolation Test
```bash
# Verify context isolation
> Invoke [subagent-name] with complex context
> Check that main conversation context preserved

# Expected: Subagent has separate context, main context unaffected
```

#### 4. Token Efficiency Test
```bash
# Measure token usage
> Track tokens consumed by [subagent-name] during typical task

# Expected: Usage within specified target (< 50K for most)
```

#### 5. Integration Test
```bash
# Test subagent invocation from skills
> Run devforgeai-development skill, verify subagents invoked correctly

# Expected: Subagents invoked at proper phases, results integrated
```

### Phase 2 Completion Criteria

✅ **All 13 subagents created** in `.claude/agents/`

✅ **Each subagent has:**
- Valid YAML frontmatter (name, description, tools, model)
- Comprehensive system prompt (> 200 lines)
- Clear invocation triggers
- Defined success criteria
- Integration patterns documented

✅ **Validation passed:**
- All subagents discoverable via `/agents` command
- Explicit invocation works for each subagent
- Tool access restrictions enforced
- Context isolation verified
- Token usage within targets

✅ **Integration validated:**
- Subagents invoked correctly from skills
- Parallel execution works (2+ subagents simultaneously)
- Results properly aggregated by parent skill
- No context leakage between subagents

✅ **Documentation complete:**
- Each subagent self-documented in system prompt
- Integration patterns documented in skills
- Usage examples in CLAUDE.md

---

## Integration Requirements

### Skill Integration Points

#### devforgeai-development Skill

**Phase 1 (Red - Test First):**
- Invoke `test-automator` to generate failing tests from acceptance criteria

**Phase 2 (Green - Implementation):**
- Invoke `backend-architect` for backend code OR `frontend-developer` for frontend code
- Invoke `context-validator` before proceeding

**Phase 3 (Refactor):**
- Invoke `refactoring-specialist` to improve code quality
- Invoke `code-reviewer` for feedback
- Invoke `context-validator` after refactoring

**Phase 4 (Integration):**
- Invoke `integration-tester` for cross-component tests
- Invoke `documentation-writer` if doc coverage < 80%

#### devforgeai-qa Skill

**Phase 1 (Test Coverage Analysis):**
- Use `test-automator` to generate missing tests for coverage gaps

**Phase 2 (Anti-Pattern Detection):**
- Use `security-auditor` for security-specific scans
- Use `context-validator` for constraint violations

**Phase 3 (Spec Compliance):**
- Use `api-designer` to validate API contract compliance

#### devforgeai-architecture Skill

**Phase 2 (Context File Creation):**
- Use `architect-reviewer` to validate architecture decisions
- Use `api-designer` for API contract definitions

#### devforgeai-release Skill

**Phase 3 (Production Deployment):**
- Use `deployment-engineer` for platform-specific deployment configs

#### devforgeai-orchestration Skill

**Story Creation:**
- Use `requirements-analyst` to generate user stories from epics

### Parallel Execution Guidelines

**Suitable for parallel execution:**
- `test-automator` + `documentation-writer` (independent tasks)
- `backend-architect` + `frontend-developer` (separate codebases)
- `security-auditor` + `code-reviewer` (different analysis)

**NOT suitable for parallel:**
- `test-automator` → `backend-architect` (tests must exist first)
- `backend-architect` → `refactoring-specialist` (implementation must complete)
- `context-validator` → any implementation (validation must pass first)

**Parallel execution pattern:**
```markdown
# In skill system prompt
Execute these subagents in parallel:
1. Invoke test-automator for test generation
2. Invoke documentation-writer for API docs

Use single message with multiple Skill tool calls:
Skill(command="test-automator")
Skill(command="documentation-writer")

Wait for both to complete, then proceed.
```

---

## Token Efficiency Targets

### Per-Subagent Token Budgets

| Subagent | Target Tokens | Rationale |
|----------|---------------|-----------|
| test-automator | < 50K | Generates multiple tests, reads specs |
| backend-architect | < 50K | Implements features, reads context |
| code-reviewer | < 30K | Reviews diffs, lightweight analysis |
| frontend-developer | < 50K | Implements components, state management |
| deployment-engineer | < 40K | Creates configs, reads platform docs |
| requirements-analyst | < 30K | Creates stories, lightweight writing |
| architect-reviewer | < 40K | Reviews designs, provides alternatives |
| security-auditor | < 40K | Comprehensive security scan |
| context-validator | < 5K | Fast validation, simple checks |
| documentation-writer | < 30K | Generates docs, reads code |
| refactoring-specialist | < 40K | Refactors code, runs tests |
| integration-tester | < 40K | Creates integration tests |
| api-designer | < 30K | Designs API contracts |

### Optimization Strategies

**1. Progressive Disclosure:**
- Load context incrementally (read only what's needed)
- Use Glob to find files, Read only relevant ones

**2. Native Tool Efficiency:**
- Use Read/Edit/Write/Glob/Grep (40-73% token savings vs Bash)
- Never use Bash for file operations

**3. Focused System Prompts:**
- Keep system prompts < 1000 lines
- Extract detailed guides to reference files (load on demand)

**4. Model Selection:**
- Use `haiku` for simple validation tasks (context-validator)
- Use `sonnet` for complex reasoning (architect-reviewer, security-auditor)
- Use `inherit` for adaptive tasks (code-reviewer, refactoring-specialist)

**5. Caching:**
- Read context files once, cache in memory
- Don't re-read unchanged files

---

## Validation Checklist

### Pre-Implementation Validation

- [ ] All 13 subagent names finalized
- [ ] Tool requirements defined for each subagent
- [ ] Model selection appropriate for task complexity
- [ ] Integration points identified in skills
- [ ] Token efficiency targets set
- [ ] Parallel execution patterns planned

### During Implementation

**Per Subagent:**
- [ ] YAML frontmatter complete (name, description, tools, model)
- [ ] System prompt > 200 lines with clear structure
- [ ] Invocation triggers defined (proactive, explicit, automatic)
- [ ] Workflow steps documented
- [ ] Success criteria listed
- [ ] Best practices included
- [ ] Integration points documented
- [ ] Token efficiency strategies noted

### Post-Implementation Validation

**Functional Tests:**
- [ ] All 13 subagents appear in `/agents` command
- [ ] Explicit invocation works ("Use [subagent] to [task]")
- [ ] Tool access restrictions enforced
- [ ] Model selection respected
- [ ] Context isolation verified

**Integration Tests:**
- [ ] Subagents invoked from devforgeai-development skill
- [ ] Subagents invoked from devforgeai-qa skill
- [ ] Subagents invoked from devforgeai-architecture skill
- [ ] Parallel execution works (2+ simultaneous)
- [ ] Results aggregated correctly

**Performance Tests:**
- [ ] Token usage measured for each subagent
- [ ] All subagents within token targets
- [ ] Execution time reasonable (< 2 minutes typical)
- [ ] No context overflow incidents

**Quality Tests:**
- [ ] System prompts reviewed for clarity
- [ ] Integration patterns documented in skills
- [ ] Usage examples added to CLAUDE.md
- [ ] Team can use subagents without guidance

---

## Appendix A: Subagent Priority Matrix

### Critical Priority (Days 6-7)

**Must be implemented first - required for core workflows:**

1. **test-automator** - TDD dependency (Day 6)
2. **backend-architect** - Primary implementation (Day 6)
3. **context-validator** - Constraint enforcement (Day 6)
4. **code-reviewer** - Quality assurance (Day 7)
5. **frontend-developer** - Full-stack support (Day 7)

### High Priority (Day 8)

**Important for complete functionality:**

6. **deployment-engineer** - Release automation (Day 8)
7. **requirements-analyst** - Story generation (Day 8)
8. **documentation-writer** - Documentation generation (Day 8)

### Medium Priority (Day 9)

**Enhances quality and specialization:**

9. **architect-reviewer** - Design validation (Day 9)
10. **security-auditor** - Security scanning (Day 9)
11. **refactoring-specialist** - Code quality (Day 9)
12. **integration-tester** - Integration validation (Day 9)

### Lower Priority (Day 10)

**Nice-to-have, can be added later:**

13. **api-designer** - API consistency (Day 10)

---

## Appendix B: Tool Access Reference

### File Operations (Native Tools - MANDATORY)

```yaml
Read:
  purpose: View file contents
  replaces: cat, head, tail, less, more
  efficiency: 40% token savings vs Bash

Write:
  purpose: Create new files
  replaces: echo >, cat <<EOF, printf >
  efficiency: 77% token savings vs Bash

Edit:
  purpose: Modify existing files
  replaces: sed, awk, perl
  efficiency: 78% token savings vs Bash

Glob:
  purpose: Find files by pattern
  replaces: find, ls -R
  efficiency: 73% token savings vs Bash

Grep:
  purpose: Search file contents
  replaces: grep, rg, ag
  efficiency: 60% token savings vs Bash
```

### Terminal Operations (Bash - Allowed)

```yaml
Bash(git:*):
  purpose: Version control operations
  examples: git status, git diff, git commit, git push

Bash(npm:*):
  purpose: Node.js package management and scripts
  examples: npm install, npm test, npm run build

Bash(pytest:*):
  purpose: Python testing
  examples: pytest, pytest --cov

Bash(dotnet:*):
  purpose: .NET CLI operations
  examples: dotnet build, dotnet test, dotnet run

Bash(docker:*):
  purpose: Container operations
  examples: docker build, docker run, docker compose

Bash(kubectl:*):
  purpose: Kubernetes operations
  examples: kubectl apply, kubectl get pods

Bash(terraform:*):
  purpose: Infrastructure as Code
  examples: terraform plan, terraform apply

Bash(ansible:*):
  purpose: Configuration management
  examples: ansible-playbook deploy.yml
```

### AI Operations

```yaml
Skill:
  purpose: Invoke other DevForgeAI skills
  examples: Skill(command="devforgeai-architecture")

AskUserQuestion:
  purpose: Resolve ambiguities with user input
  usage: When context unclear, choices needed

WebFetch:
  purpose: Research documentation or best practices
  examples: WebFetch(url="https://docs.example.com", prompt="Find API docs")
```

---

## Appendix C: Implementation Schedule

### Week 2 Daily Breakdown

**Day 6 (Critical Subagents):**
- Morning: test-automator, backend-architect
- Afternoon: context-validator
- Validation: Test with devforgeai-development skill

**Day 7 (Core Implementation):**
- Morning: code-reviewer, frontend-developer
- Afternoon: Integration testing
- Validation: Test parallel execution

**Day 8 (Supporting Subagents):**
- Morning: deployment-engineer, requirements-analyst
- Afternoon: documentation-writer
- Validation: Test with devforgeai-release, devforgeai-orchestration

**Day 9 (Quality Subagents):**
- Morning: architect-reviewer, security-auditor
- Afternoon: refactoring-specialist, integration-tester
- Validation: Test with devforgeai-qa skill

**Day 10 (Final Subagent + Integration):**
- Morning: api-designer
- Afternoon: Full integration testing, token measurement
- Validation: End-to-end workflow test

---

**Status**: Ready for Implementation
**Next Phase**: Phase 3 - Slash Commands (Week 3)
**Prerequisites**: Phase 1 Complete ✅

**Implementation Lead**: [To be assigned]
**Review Date**: End of Day 10
**Success Gate**: All 13 subagents functional and validated
