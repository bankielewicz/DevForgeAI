# AI Constraints and Guardrails for Controlled Development

## Document Status

- **Type**: Research & Practical Guide
- **Evidence Level**: High - Based on Anthropic official documentation and proven practices
- **Last Updated**: 2025-10-09
- **Sources**: Anthropic Claude Code documentation, official best practices

## Overview

This document provides evidence-based techniques for constraining AI behavior during software development to prevent "going off the rails" or "bull in china shop" scenarios.

**Goal**: Enable AI to be productive while maintaining strict control over scope, quality, and changes.

## The Problem: Unconstrained AI Behavior

### Real-World Scenarios

**Scenario 1**: Over-Implementation
```
Human: "Add a login button"

Unconstrained AI might:
- Add login button ✓
- Redesign entire navigation bar
- Implement OAuth2, 2FA, password reset
- Add admin dashboard
- Refactor authentication system
- Install 10 new dependencies
- Change database schema
```

**Scenario 2**: Unintended Refactoring
```
Human: "Fix the typo in user-service.ts"

Unconstrained AI might:
- Fix typo ✓
- "Improve" variable names throughout file
- Refactor functions to "better" patterns
- Add error handling everywhere
- Split file into multiple modules
- Update all imports across project
```

**Scenario 3**: Architectural Drift
```
Human: "Add caching to the API"

Unconstrained AI might:
- Add Redis caching layer
- Change from REST to GraphQL
- Implement pub/sub messaging
- Add microservices
- Dockerize everything
- Set up Kubernetes
```

## Constraint Mechanisms (Evidence-Based)

### Mechanism 1: Permission Controls

**Evidence**: Documented in Claude Code official settings documentation

**File**: `.claude/settings.json`

```json
{
  "permissions": {
    "allow": [
      "Read(*)",
      "Write(src/features/current-feature/*)",
      "Edit(tests/current-feature/*)",
      "Bash(npm test*)",
      "Bash(git diff*)"
    ],
    "ask": [
      "Edit(package.json)",
      "Edit(tsconfig.json)",
      "Bash(git push*)"
    ],
    "deny": [
      "Edit(src/core/**/*)",
      "Edit(src/database/**/*)",
      "Write(.env*)",
      "Bash(rm -rf *)",
      "Bash(git reset*)"
    ],
    "additionalDirectories": [],
    "defaultMode": "acceptEdits"
  }
}
```

**Granularity Levels**:

**File-Level**:
```json
{
  "allow": ["Edit(src/auth/login.ts)"],  // Only this file
  "deny": ["Edit(src/auth/*.ts)"]         // Block all other auth files
}
```

**Directory-Level**:
```json
{
  "allow": ["Write(src/features/search/**/*)", "Edit(tests/search/**/*)"  ],
  "deny": ["Edit(src/features/checkout/**/*)"  ]
}
```

**Tool-Level**:
```json
{
  "allow": ["Read(*)", "Grep(*)", "Glob(*)"],  // Read-only mode
  "deny": ["Write(*)", "Edit(*)", "Bash(*)"]
}
```

**Command-Level**:
```json
{
  "allow": [
    "Bash(npm test*)",
    "Bash(npm run lint*)",
    "Bash(git status)",
    "Bash(git diff*)"
  ],
  "deny": [
    "Bash(npm install*)",     // Prevent dependency changes
    "Bash(git push*)",        // Prevent pushing
    "Bash(docker*)"           // Prevent Docker operations
  ]
}
```

### Mechanism 2: CLAUDE.md Project Guidelines

**Evidence**: Recommended in Anthropic official best practices

**Purpose**: Auto-loaded project constitution that constrains ALL AI behavior

**Location**: `CLAUDE.md` (project root) or `.claude/CLAUDE.md`

**Complete Example** (framework-agnostic):

```markdown
# Project Guidelines for Claude

## Project Context

This is a [monolithic/microservices/etc] application built with [your stack].

Current phase: [Feature development / Maintenance / Refactoring]

## Code Style

### Language: [JavaScript/Python/C#/Go/etc]

- Follow [ESLint/Pylint/StyleCop/golint] rules
- Use [Prettier/Black/dotnet-format/gofmt] for formatting
- [Language-specific conventions]

### File Organization

- Follow existing directory structure
- New features go in: src/features/[feature-name]/
- Tests mirror src/ structure in tests/
- Do NOT create new top-level directories without approval

## Testing Requirements

- **Minimum Coverage**: 80% (statements, branches, functions)
- **Test Framework**: [Jest/pytest/xUnit/JUnit/testing]
- **TDD Required**: Write tests BEFORE implementation
- **Test Location**: tests/ directory (mirrors src/ structure)
- **Naming Convention**: [describe your pattern]

### Test Quality Standards

- One assertion per test (focused tests)
- Descriptive test names
- No skipped tests in commits
- Edge cases required
- Integration tests for API endpoints

## Git Workflow

- Create feature branches: feature/STORY-XXX-description
- Commit message format: type(scope): description
- Do NOT push without running tests
- Squash commits before merge

## Implementation Constraints

### What TO Do

- Follow existing architectural patterns
- Reuse existing services and utilities
- Use existing error handling approach
- Match existing API response formats
- Follow existing authentication/authorization

### What NOT To Do

DO NOT:
- Refactor existing working code unless explicitly requested
- Add features beyond current story/requirement
- Change database schema without approval
- Modify API contracts without approval
- Install new dependencies without asking
- Change configuration files (package.json, tsconfig.json, etc.)
- Implement multiple stories simultaneously
- Skip writing tests
- Use deprecated patterns or libraries
- Modify files outside current feature scope

## Architecture Patterns

### Current Architecture

- Pattern: [MVC/Clean Architecture/Layered/etc]
- Database: [PostgreSQL/MySQL/MongoDB/etc]
- API Style: [REST/GraphQL/gRPC/etc]
- Authentication: [JWT/Session/OAuth/etc]

### Patterns to Follow

- Controllers: Thin, delegate to services
- Services: Business logic, no framework dependencies
- Repositories: Data access only
- Models: Pure data structures

### Anti-Patterns to Avoid

- No God objects
- No circular dependencies
- No business logic in controllers
- No database queries in controllers

## Security Constraints

- Always hash passwords (use existing auth service)
- Validate all user input
- Parameterized queries only (no SQL injection)
- Escape output (no XSS)
- Use HTTPS only
- No secrets in code (use environment variables)

## Performance Requirements

- API endpoints: p95 < 500ms
- Database queries: < 100ms
- No N+1 query problems
- Use pagination for large datasets
- Cache expensive operations

## Dependencies

- Check existing package.json/requirements.txt/etc BEFORE adding dependencies
- Prefer built-in solutions over new libraries
- If new dependency needed:
  1. STOP and explain why it's needed
  2. Propose specific package
  3. Wait for approval

## Error Handling

- Use existing error classes in src/errors/
- Follow existing error response format
- Log all errors to existing logger
- Never swallow exceptions silently

## Documentation

- Update API documentation (OpenAPI spec) for API changes
- Add JSDoc/docstrings for public functions
- Update README if adding new feature
- Do NOT generate separate documentation files unless asked

## Questions to Ask Before Proceeding

If you encounter ANY of these, STOP and ask:

- Should I change the database schema?
- Should I add a new dependency?
- Should I refactor this existing code?
- Should I change the API contract?
- Should I modify this configuration file?
- Should I implement this related feature?
- Should I change this architectural pattern?

## Validation Before Completion

Before marking work complete, verify:

- [ ] All tests pass (including existing tests)
- [ ] Coverage meets minimum (80%)
- [ ] Linter passes with zero errors
- [ ] No TODO/FIXME/HACK comments
- [ ] No console.log/print debugging statements
- [ ] No commented-out code
- [ ] Git diff shows ONLY relevant changes
- [ ] Definition of Done satisfied

## Emergency Stops

IMMEDIATELY STOP and ask human if:

- A test starts failing that was passing
- You need to modify core/shared code
- You need to change database migrations
- You need to update production configuration
- You're about to delete code
- You're about to make a breaking change
- You're uncertain about requirements
```

**Why This Works**:
- Auto-loaded every session
- Provides consistent constraints
- Team-wide standards
- Version controlled
- Easy to update

### Mechanism 3: Sub-Agent Scope Limitation

**Evidence**: Documented in Claude Code sub-agents documentation

**Pattern**: Create agents with narrow, specific scope

**Example**: Feature Implementation Agent

`.claude/agents/feature-implementer.md`:
```markdown
---
name: feature-implementer
description: Implement single feature following TDD
tools: [Read, Write, Edit, Bash, Grep]
model: sonnet
---

You are a focused feature implementation specialist.

Constraints:
1. Implement ONLY the current feature/story
2. Work ONLY in the specified files
3. Follow TDD: tests first, implementation second
4. Do NOT refactor existing code
5. Do NOT add related features
6. Do NOT modify files outside feature scope

When invoked:
1. Read the story/requirement
2. Identify files to modify
3. Ask human to confirm file scope
4. Write failing tests
5. Implement to pass tests
6. Verify no regressions
7. Report completion

If you need to:
- Change files outside scope → STOP and ask
- Add dependencies → STOP and ask
- Modify schema → STOP and ask
- Refactor existing code → STOP and ask

Always stay within the explicit boundaries provided.
```

**Why It Works**: Agent is self-aware of limitations and will halt when reaching boundaries.

### Mechanism 4: Explicit Scope Documents

**Pattern**: Write explicit scope definition

**Example**: Story Scope Document

```markdown
# STORY-123: Add Product Search

## In Scope

Implementation:
- ✅ Search endpoint: GET /api/products/search
- ✅ Query parameter: ?q=searchTerm
- ✅ Search by: product name, description, SKU
- ✅ Case-insensitive search
- ✅ Pagination (20 results per page)
- ✅ Response: JSON with products array

Files to Modify:
- ✅ src/api/product-routes.ts (add new route)
- ✅ src/services/ProductService.ts (add search method)
- ✅ tests/api/product-search.test.ts (new file)

## Out of Scope

DO NOT Implement:
- ❌ Full-text search engine (Elasticsearch)
- ❌ Search history tracking
- ❌ Search suggestions/autocomplete
- ❌ Filters (price, category, brand)
- ❌ Sorting options
- ❌ Search analytics
- ❌ Related products
- ❌ Search result highlighting

Files to NOT Modify:
- ❌ src/models/Product.ts
- ❌ src/database/schema.ts
- ❌ src/api/routes.ts (except adding import)
- ❌ Any checkout-related files
- ❌ Any cart-related files
- ❌ package.json

## Questions Before Starting

- Q: Can we use database LIKE queries?
- A: Yes, PostgreSQL ILIKE is sufficient

- Q: Should we index search fields?
- A: No, out of scope for MVP

- Q: What if user searches empty string?
- A: Return empty results array (not error)
```

**Prompt with Scope**:
```
"Read STORY-123-scope.md

Implement the product search feature.

You must:
- Stay within the 'In Scope' section ONLY
- Do NOT implement anything in 'Out of Scope'
- Work only in the specified files
- If you need to modify unlisted files, STOP and ask

Follow TDD:
1. Write tests first
2. Implement to pass tests
3. Do NOT add extra features"
```

### Mechanism 5: Incremental Prompts with Checkpoints

**Evidence**: Anthropic recommends incremental approach with human oversight

**Pattern**: Break work into small, verifiable chunks

**Example**: Multi-Step Feature

```
Prompt 1:
"Step 1: Write tests for the search endpoint.

Create tests/api/product-search.test.ts
Include tests for:
- Valid search returns results
- Empty query returns empty array
- Pagination works correctly
- Case-insensitive matching

STOP after writing tests. Do NOT implement yet."

[AI writes tests, human reviews]

Prompt 2:
"Step 2: Implement the search method in ProductService.

Requirements:
- Make the tests pass
- Use database ILIKE query
- Do NOT modify Product model
- Follow existing service pattern

STOP after implementation."

[AI implements, human reviews]

Prompt 3:
"Step 3: Add the route in product-routes.ts

Requirements:
- Add GET /api/products/search route
- Call ProductService.search()
- Follow existing route pattern
- Do NOT modify other routes

STOP after adding route."

[AI adds route, human reviews]

Prompt 4:
"Step 4: Run full test suite and verify.

Run:
1. npm test tests/api/product-search.test.ts
2. npm test (full suite)
3. npm run coverage

Report results."

[AI runs tests, reports, human validates]
```

**Why This Works**:
- Human reviews after each step
- Small changes easier to verify
- Errors caught immediately
- Can course-correct quickly

### Mechanism 6: Definition of Done (DoD) Checklist

**Pattern**: Explicit completion criteria

**Example**: Story Definition of Done

```markdown
# Definition of Done: STORY-123

Implementation cannot be marked complete until ALL items checked:

## Code Quality
- [ ] All acceptance criteria implemented
- [ ] Linter passes with zero errors
- [ ] No TODO/FIXME/HACK comments in committed code
- [ ] No commented-out code
- [ ] No console.log/print debugging statements

## Testing
- [ ] All acceptance criteria have passing tests
- [ ] Unit tests for business logic
- [ ] Integration tests for API endpoints
- [ ] Edge cases covered
- [ ] Test coverage ≥80%
- [ ] All tests passing (including existing tests)
- [ ] No skipped tests

## Documentation
- [ ] API documentation updated (if API changed)
- [ ] README updated (if user-facing change)
- [ ] Code comments for complex logic
- [ ] JSDoc/docstrings for public functions

## Security
- [ ] Input validation implemented
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Authentication/authorization enforced
- [ ] No secrets in code

## Performance
- [ ] Performance benchmarks met (if specified)
- [ ] No N+1 query problems
- [ ] Pagination implemented (if needed)

## Integration
- [ ] No breaking changes to existing APIs
- [ ] Backward compatibility maintained
- [ ] Database migrations tested (if schema changed)
- [ ] No regressions (all existing tests pass)

## Git
- [ ] Changes limited to relevant files only
- [ ] Commit message follows convention
- [ ] No unrelated changes in diff
```

**Usage with AI**:
```
"Before marking this story complete, verify the Definition of Done.

Read STORY-123-dod.md and check each item.

Report:
- Items satisfied: [list]
- Items NOT satisfied: [list with reasons]
- Files changed: [list]

If ANY items are not satisfied, STOP and explain what's needed."
```

### Mechanism 7: Validation Scripts

**Pattern**: Automated guardrails

**Example**: Pre-Implementation Validation

```bash
#!/bin/bash
# scripts/validate-before-implement.sh

STORY_FILE=$1

# HALT checks
echo "Running HALT checks..."

# Check 1: Story has acceptance criteria
if ! grep -q "Acceptance Criteria" "$STORY_FILE"; then
  echo "❌ HALT: No acceptance criteria found"
  exit 1
fi

# Check 2: Tests exist
STORY_ID=$(grep "Story:" "$STORY_FILE" | awk '{print $2}')
if [ ! -f "tests/$STORY_ID.test.ts" ]; then
  echo "❌ HALT: No tests found. Write tests first."
  exit 1
fi

# Check 3: Tests are failing
if npm test "tests/$STORY_ID.test.ts" >/dev/null 2>&1; then
  echo "❌ HALT: Tests are passing. Implementation may already exist."
  exit 1
fi

echo "✅ All HALT checks passed. Safe to implement."
exit 0
```

**Usage**:
```
"Before implementing, run: ./scripts/validate-before-implement.sh STORY-123.md

If validation passes, proceed with implementation.
If validation fails, STOP and report the error."
```

### Mechanism 8: Read-First Mandate

**Evidence**: Anthropic best practice - "Explore, Plan, Code, Commit"

**Pattern**: Force AI to read existing code before changing

**Example Prompt Structure**:
```
"PHASE 1: Exploration (Read-Only)

Read these files to understand existing patterns:
- src/auth/login.ts
- src/middleware/auth-middleware.ts
- src/services/UserService.ts
- tests/auth/login.test.ts

After reading, create a summary of:
1. Current authentication pattern used
2. Error handling approach
3. Test structure and style
4. Database interaction pattern

STOP after summary. Do NOT implement yet."

[AI reads and summarizes, human verifies understanding]

"PHASE 2: Planning

Based on your exploration, create a plan to add password reset.

Plan must:
- Follow existing authentication pattern
- Use existing error handling
- Match existing test structure
- Reuse existing UserService methods

STOP after creating plan."

[AI creates plan, human approves]

"PHASE 3: Implementation

Implement the plan using TDD:
1. Write tests following existing test pattern
2. Implement to make tests pass
3. Do NOT deviate from the approved plan"
```

**Why This Works**: AI understands context and follows established patterns instead of inventing new ones.

## Multi-Layer Guardrail Strategy

### Layer 1: Permission Layer (Technical Enforcement)

```json
{
  "permissions": {
    "allow": ["Read(*)", "Edit(src/feature-x/**)", "Write(tests/feature-x/**)"],
    "deny": ["Edit(src/core/**)", "Edit(*.config.js)"]
  }
}
```

**Prevents**: Accidental modification of protected files

### Layer 2: CLAUDE.md (Project-Wide Rules)

```markdown
## Constraints

DO NOT:
- Refactor without explicit request
- Add features beyond requirement
- Change architecture patterns
```

**Prevents**: Intentional but unwanted actions based on AI judgment

### Layer 3: Prompt-Level Instructions (Task-Specific)

```
"Implement login endpoint.

Constraints for this task:
- Modify ONLY src/auth/login.ts
- Do NOT change User model
- Do NOT add registration/password reset"
```

**Prevents**: Scope creep within allowed files

### Layer 4: Test Specifications (Behavior Boundary)

```javascript
// Only these behaviors will be implemented
test('should login with valid credentials')
test('should reject invalid password')
test('should rate-limit after 5 failures')
```

**Prevents**: Implementation beyond specified behavior

### Layer 5: Definition of Done (Quality Gate)

```markdown
- [ ] All AC have tests
- [ ] Coverage ≥80%
- [ ] No regressions
```

**Prevents**: Premature completion

### Layer 6: Human Review (Final Validation)

```bash
git diff
npm test
npm run lint
```

**Prevents**: Any issues that slipped through automated checks

**Layered Defense**: Multiple independent constraints. If one fails, others catch issues.

## Practical Constraint Examples

### Constraint Type 1: File Scope

**Scenario**: Implementing search feature

**Constraint**:
```
"Files you may modify:
- src/services/SearchService.ts (create new)
- src/api/search-routes.ts (create new)
- src/api/routes.ts (add import only)
- tests/search/ (create new directory)

Files you may NOT modify:
- src/models/ (any model)
- src/database/ (any database code)
- src/services/ (except SearchService)
- package.json

If you need to modify any unlisted file, STOP and ask."
```

### Constraint Type 2: Behavioral Scope

**Scenario**: Adding validation

**Constraint**:
```
"Implement email validation ONLY.

Implement:
- ✅ Email format validation
- ✅ Return true/false

Do NOT implement:
- ❌ Email uniqueness check (out of scope)
- ❌ DNS verification (out of scope)
- ❌ Disposable email detection (out of scope)
- ❌ Email sending (different feature)

The ONLY behavior: Format validation (regex-based)"
```

### Constraint Type 3: Technology Scope

**Scenario**: Adding caching

**Constraint**:
```
"Add in-memory caching to the product service.

Technology constraints:
- ✅ Use native Map/Dictionary (no new dependencies)
- ✅ LRU eviction (implement simple version)
- ❌ Do NOT install Redis
- ❌ Do NOT add cache library
- ❌ Do NOT implement distributed caching
- ❌ Do NOT add cache warming/preloading

This is a simple, MVP, in-process cache only."
```

### Constraint Type 4: Temporal Scope

**Scenario**: Multi-phase project

**Constraint**:
```
"This is Phase 1 of a 3-phase project.

Phase 1 (THIS PHASE):
- Implement basic search (keyword only)

Phase 2 (NOT NOW):
- Add filters
- Add sorting

Phase 3 (NOT NOW):
- Add full-text search
- Add search analytics

ONLY implement Phase 1. Do NOT implement Phase 2 or 3 features."
```

### Constraint Type 5: Dependency Scope

**Scenario**: Adding functionality

**Constraint**:
```
"Implement JSON parsing.

Dependency constraints:
- ✅ Use built-in JSON.parse() [JavaScript]
- ✅ Use built-in json module [Python]
- ✅ Use built-in System.Text.Json [C#]
- ❌ Do NOT install external parsing library
- ❌ Do NOT add Newtonsoft.Json [C#]
- ❌ Do NOT add third-party validators

Current dependency count: 15
After implementation dependency count must be: 15 (no new dependencies)"
```

## Checkpoint vs Autonomous Mode

### Checkpoint Mode (Safe, Recommended)

**Evidence**: Mentioned in Anthropic best practices and Claude Code documentation

**Characteristics**:
- AI pauses at decision points
- Human reviews intermediate results
- Proceeds only after approval
- 3-4 message boundaries for decisions

**Use When**:
- Critical features
- Complex refactoring
- Database changes
- API modifications
- Learning new codebase
- High-risk operations

**Example Checkpoint Workflow**:
```
Prompt: "Add user search feature. Use checkpoint mode."

AI: "I'll implement this in 4 checkpoints:
     Checkpoint 1: Write tests
     Checkpoint 2: Implement search logic
     Checkpoint 3: Add API endpoint
     Checkpoint 4: Validate and finalize

     Starting Checkpoint 1: Writing tests...
     [writes tests]

     Checkpoint 1 complete. Tests written.
     Review tests before I proceed to Checkpoint 2?"