# DevForgeAI Subagents Reference

Detailed guidance for working with the 14 specialized subagents.

---

## Overview

Subagents are specialized AI workers with domain expertise that operate in isolated contexts. They are automatically invoked by DevForgeAI skills or can be explicitly called for specific tasks. **14 subagents** are available in `.claude/agents/`.

---

## Subagent Invocation Methods

### 1. Automatic Invocation (Proactive)

Subagents are automatically invoked by DevForgeAI skills at appropriate workflow phases:

**During devforgeai-development:**
- **Phase 1 (Red)**: test-automator generates failing tests from acceptance criteria
- **Phase 2 (Green)**: backend-architect or frontend-developer implements code to pass tests
- **Phase 2 (Validation)**: context-validator checks constraint compliance
- **Phase 3 (Refactor)**: refactoring-specialist improves code quality, code-reviewer provides feedback
- **Phase 4 (Integration)**: integration-tester creates cross-component tests

**During devforgeai-qa:**
- **Light Validation**: context-validator checks constraints
- **Deep Validation**: security-auditor scans for vulnerabilities, test-automator fills coverage gaps

**During devforgeai-architecture:**
- architect-reviewer validates architecture decisions
- api-designer defines API contract standards

**During devforgeai-release:**
- deployment-engineer handles infrastructure and deployment
- security-auditor performs pre-release security scan

### 2. Explicit Invocation

Invoke subagents directly using the Task tool with `subagent_type` parameter:

```
Task(
  subagent_type="test-automator",
  description="Generate tests for calculator",
  prompt="Generate comprehensive unit tests for a calculator class with add, subtract, multiply, and divide methods. Follow TDD principles and AAA pattern."
)
```

**Examples:**

```
# Code review
Task(
  subagent_type="code-reviewer",
  description="Review authentication code",
  prompt="Review the authentication implementation in src/auth/ for security issues, code quality, and adherence to coding standards."
)

# Frontend implementation
Task(
  subagent_type="frontend-developer",
  description="Implement login component",
  prompt="Implement a login form component in React following the design system in context files. Include email/password fields, validation, and API integration."
)

# Security audit
Task(
  subagent_type="security-auditor",
  description="Audit payment processing",
  prompt="Perform comprehensive security audit of payment processing code in src/payments/ focusing on PCI compliance and OWASP Top 10."
)

# Context validation
Task(
  subagent_type="context-validator",
  description="Validate constraints",
  prompt="Check all code changes for violations of the 6 context files (tech-stack, source-tree, dependencies, coding-standards, architecture-constraints, anti-patterns)."
)
```

### 3. Parallel Execution

Multiple subagents can run simultaneously for different tasks:

```
# Send single message with multiple Task tool calls
Task(subagent_type="test-automator", description="Generate tests", prompt="...")
Task(subagent_type="documentation-writer", description="Write API docs", prompt="...")

# Both execute in parallel, return results independently
```

---

## Available Subagents

| Subagent | Purpose | Model | Token Target | When to Use |
|----------|---------|-------|--------------|-------------|
| **test-automator** | TDD test generation (unit, integration, E2E) | sonnet | <50K | Implementing features, filling coverage gaps |
| **backend-architect** | Backend implementation (clean architecture, DDD) | sonnet | <50K | Implementing backend features, APIs, services |
| **frontend-developer** | Frontend implementation (React, Vue, Angular) | sonnet | <50K | Implementing UI components, state management |
| **context-validator** | Fast constraint enforcement (6 context files) | haiku | <5K | Before commits, after implementation |
| **code-reviewer** | Code quality and security review | inherit | <30K | After implementation, during refactoring |
| **security-auditor** | OWASP Top 10, auth/authz, vulnerability scanning | sonnet | <40K | After auth code, handling sensitive data |
| **deployment-engineer** | Infrastructure, IaC, CI/CD pipelines | sonnet | <40K | Release phase, deployment configuration |
| **requirements-analyst** | User story creation, acceptance criteria | sonnet | <30K | Epic decomposition, story planning |
| **documentation-writer** | Technical docs, API specs, user guides | sonnet | <30K | After API implementation, when coverage <80% |
| **architect-reviewer** | Architecture validation, design patterns | sonnet | <40K | After ADRs, major architectural changes |
| **refactoring-specialist** | Safe refactoring, code smell removal | inherit | <40K | When complexity >10, code duplication >5% |
| **integration-tester** | Cross-component testing, API contracts | sonnet | <40K | After unit tests pass, API endpoints ready |
| **api-designer** | REST/GraphQL/gRPC contract design | sonnet | <30K | Creating new APIs, ensuring consistency |
| **agent-generator** | Generate new specialized subagents | haiku | N/A | Creating custom subagents for framework |

---

## Subagent Integration with Skills

**devforgeai-development** uses:
- test-automator → backend-architect/frontend-developer → context-validator → refactoring-specialist + code-reviewer → integration-tester

**devforgeai-qa** uses:
- context-validator → security-auditor → test-automator (coverage gaps)

**devforgeai-architecture** uses:
- architect-reviewer → api-designer

**devforgeai-release** uses:
- security-auditor → deployment-engineer

**devforgeai-orchestration** uses:
- requirements-analyst (story creation)

---

## Autonomous Subagent Usage

**When to autonomously invoke subagents:**

1. **Context Validation**: Always use `context-validator` before git commits or after implementation
2. **Test Generation**: Use `test-automator` when implementing features (TDD Red phase)
3. **Code Review**: Use `code-reviewer` after implementation or refactoring
4. **Security Audits**: Use `security-auditor` after auth/security code or handling sensitive data
5. **Documentation**: Use `documentation-writer` after API implementation or when coverage <80%
6. **Architecture Review**: Use `architect-reviewer` after creating ADRs or major design changes

---

## Subagent Context Isolation

- Each subagent operates in a separate context window
- Main conversation context is preserved (token efficiency)
- Subagents return results that integrate into main workflow
- No context leakage between parallel subagents

---

## Token Efficiency with Subagents

- Subagent work happens in isolated contexts
- Main conversation only pays invocation cost (~5-10K) + summary
- Total workflow can exceed 200K tokens across subagents without affecting main context
- **Example:** Full dev cycle (test-automator 50K + backend-architect 50K + code-reviewer 30K + integration-tester 40K = 170K) appears as ~15K in main conversation

---

## Subagent Best Practices

1. **Use specific, detailed prompts**: Subagents work best with clear instructions
2. **Reference context files**: Subagents respect tech-stack, source-tree, dependencies, etc.
3. **Specify success criteria**: Define what "done" looks like in the prompt
4. **Leverage parallelism**: Run independent subagents simultaneously for speed
5. **Check validation results**: context-validator blocks on violations, fix before proceeding
6. **Trust specialized expertise**: Subagents are domain experts (security, testing, architecture)

---

## Subagent File Locations

All subagents are defined in `.claude/agents/`:
- `test-automator.md` (546 lines)
- `backend-architect.md` (728 lines)
- `frontend-developer.md` (629 lines)
- `integration-tester.md` (502 lines)
- `context-validator.md` (356 lines)
- `code-reviewer.md` (457 lines)
- `security-auditor.md` (550 lines)
- `refactoring-specialist.md` (471 lines)
- `requirements-analyst.md` (473 lines)
- `architect-reviewer.md` (528 lines)
- `api-designer.md` (754 lines)
- `deployment-engineer.md` (820 lines)
- `documentation-writer.md` (519 lines)
- `agent-generator.md` (855 lines)

Each file contains complete system prompts with tool access, model selection, and execution patterns.
