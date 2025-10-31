# Git Workflow Conventions Reference

Complete guide for version control operations during Phase 6 (Git Workflow) of the TDD development process.

## Overview

This reference provides conventions for:
- Branch naming strategies
- Commit message formatting (Conventional Commits)
- Commit timing in TDD workflow
- Staging strategies
- Push timing and best practices
- Git hooks integration

---

## Branch Naming Conventions

### Feature Branches

**Pattern:** `feature/[STORY-ID]-[brief-description]`

**Examples:**
```bash
feature/STORY-001-user-authentication
feature/STORY-042-checkout-optimization
feature/EPIC-003-payment-integration
```

**Rules:**
- Always include story/epic ID
- Use lowercase with hyphens
- Keep description brief (2-4 words)
- Branch from main/master or development branch

### Bugfix Branches

**Pattern:** `bugfix/[STORY-ID]-[brief-description]`

**Examples:**
```bash
bugfix/STORY-015-login-redirect-issue
bugfix/BUG-028-cart-calculation-error
bugfix/critical-security-patch
```

**Rules:**
- Include bug/story ID when available
- "critical" prefix for urgent production fixes
- Branch from main/master or release branch

### Hotfix Branches

**Pattern:** `hotfix/[description]` or `hotfix/[HOTFIX-ID]-[description]`

**Examples:**
```bash
hotfix/production-crash-fix
hotfix/HOTFIX-001-payment-gateway-failure
hotfix/security-vulnerability-CVE-2024-XXXX
```

**Rules:**
- For critical production issues only
- Branch from production/main
- Merge to both production and development branches
- Deploy immediately after testing

### Release Branches

**Pattern:** `release/v[MAJOR].[MINOR].[PATCH]` or `release/[SPRINT-ID]`

**Examples:**
```bash
release/v1.2.0
release/v2.0.0-beta
release/SPRINT-003
```

**Rules:**
- Created when features complete for release
- No new features (bug fixes only)
- Merge to main and development when ready

---

## Conventional Commit Format

### Standard Structure

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Components:**
- **type**: Required - Commit category
- **scope**: Optional - Area of change (component, module, feature)
- **subject**: Required - Brief description (imperative mood, no period)
- **body**: Optional - Detailed explanation
- **footer**: Optional - References (closes #123, breaking changes)

### Commit Types

| Type | Usage | Example |
|------|-------|---------|
| **feat** | New feature or functionality | `feat: Add user authentication` |
| **fix** | Bug fix | `fix: Correct cart calculation error` |
| **refactor** | Code refactoring (no behavior change) | `refactor: Extract discount calculation method` |
| **test** | Adding or updating tests | `test: Add edge cases for order validation` |
| **docs** | Documentation changes | `docs: Update API endpoint documentation` |
| **style** | Code formatting (no logic change) | `style: Format code with Prettier` |
| **chore** | Build, dependencies, tooling | `chore: Update Dapper to 2.1.28` |
| **perf** | Performance improvements | `perf: Optimize database query for orders` |
| **ci** | CI/CD changes | `ci: Add code coverage to pipeline` |
| **build** | Build system changes | `build: Configure webpack for production` |
| **revert** | Revert previous commit | `revert: Revert "feat: Add feature X"` |

### Commit Message Examples

#### Feature Commit

```
feat(auth): Implement JWT authentication

- Added login/logout endpoints in AuthController
- Implemented token validation middleware
- Created user session management service
- Tests: 12 unit tests, 3 integration tests (95% coverage)
- Compliance: tech-stack.md (JWT), coding-standards.md (async/await)

Closes #STORY-001
```

#### Bug Fix Commit

```
fix(cart): Prevent duplicate items in shopping cart

- Added duplicate check before adding item to cart
- Updated CartService.AddItem method
- Added regression test for duplicate prevention
- Coverage: 98% for CartService

Fixes #BUG-045
```

#### Refactor Commit

```
refactor(order-service): Extract validation logic to separate class

- Created OrderValidator class
- Moved validation from OrderService to OrderValidator
- No behavior changes (all tests still passing)
- Tests: 100% pass rate maintained
- Improved testability and separation of concerns

Part of #STORY-003 refactoring phase
```

#### Test Commit

```
test(order-service): Add edge case tests for discount calculation

- Added tests for zero total
- Added tests for null coupon
- Added tests for expired coupon
- Added tests for negative discount
- Coverage increased from 87% to 95%

Part of #STORY-001 TDD cycle
```

#### Documentation Commit

```
docs(api): Update order endpoints documentation

- Added request/response examples for POST /api/orders
- Documented error codes and responses
- Updated authentication requirements
- Added rate limiting information

Related to #STORY-001
```

#### Breaking Change Commit

```
feat(api): Change order creation endpoint contract

BREAKING CHANGE: Order creation now requires customerId in request body

- Updated POST /api/orders to require customerId
- Removed customerEmail as alternative identifier
- Updated validation rules
- Migration guide added to docs/migration/v2.0.md

Closes #STORY-050
```

---

## Commit Timing in TDD Workflow

### Option 1: Single Commit Per Story (Recommended)

**When:** After Phase 5 (Integration) completes successfully

**Benefits:**
- Clean git history (one commit = one story)
- Easy to revert entire feature
- Simple workflow
- Matches story lifecycle

**Pattern:**
```bash
# After Phase 5: Integration complete
# All tests passing, QA approved, ready to commit

git add src/ tests/
git commit -m "$(cat <<'EOF'
feat: Implement order discount calculation

- Implemented CalculateDiscount method following TDD
- Tests: 15 unit tests, 3 integration tests
- Edge cases: null inputs, expired coupons, invalid codes
- Compliance: tech-stack.md (Dapper), coding-standards.md (Result Pattern)
- Coverage: 95% for OrderService
- QA: Light validation passed

Closes #STORY-001
EOF
)"

git push origin feature/STORY-001-order-discounts
```

**Git History:**
```
feat: Implement order discount calculation (STORY-001)
feat: Add user profile page (STORY-002)
fix: Correct cart total bug (BUG-012)
```

### Option 2: Multiple Commits Per TDD Phase

**When:** For complex stories or learning/demonstration purposes

**Benefits:**
- Visible TDD progression in history
- Can revert to specific phase
- Educational (shows RED→GREEN→REFACTOR)

**Pattern:**
```bash
# After Phase 2: Tests written (RED)
git add tests/
git commit -m "test: Add failing tests for order discount calculation

- Added 15 test cases for discount scenarios
- Tests currently failing (RED phase)
- Will implement in next commit

Part of #STORY-001"

# After Phase 3: Implementation (GREEN)
git add src/
git commit -m "feat: Implement order discount calculation (Green phase)

- Implemented CalculateDiscount method
- All tests now passing
- Minimal implementation (will refactor next)

Part of #STORY-001"

# After Phase 4: Refactoring
git add src/
git commit -m "refactor: Improve discount calculation code quality

- Extracted validation logic to separate method
- Removed magic numbers
- Improved variable names
- All tests still passing

Part of #STORY-001"

# After Phase 5: Integration
git commit -m "feat: Complete order discount feature

- Integration tests passing
- QA validation passed
- Coverage: 95%
- Ready for code review

Closes #STORY-001"
```

**Git History:**
```
test: Add failing tests for order discount calculation
feat: Implement order discount calculation (Green phase)
refactor: Improve discount calculation code quality
feat: Complete order discount feature (STORY-001)
```

### Option 3: Hybrid Approach

**When:** Balance between clean history and meaningful checkpoints

**Pattern:**
```bash
# Commit after each significant milestone
# Squash before merging to main

# Checkpoint 1: Core implementation
git commit -m "feat: Implement core discount calculation logic"

# Checkpoint 2: Edge cases
git commit -m "feat: Add edge case handling for discounts"

# Checkpoint 3: Refactoring
git commit -m "refactor: Improve discount code quality"

# Before merge: Squash into single commit
git rebase -i HEAD~3
# Squash commits into one
```

### Recommended Strategy

**For most development:**
✅ **Use Option 1: Single Commit Per Story**

**Reasoning:**
- Simpler workflow
- Cleaner git history
- Easier code reviews
- Matches DevForgeAI story-driven development
- One story = one merge = one commit to main

---

## Staging Strategy

### What to Stage

**Always include:**
```bash
# Source code changes
git add src/Application/Services/AuthService.cs
git add src/Domain/Entities/User.cs

# Test files
git add tests/Application.Tests/Services/AuthServiceTests.cs
git add tests/Integration/AuthIntegrationTests.cs

# Updated documentation
git add docs/api/auth-endpoints.md

# Configuration changes (if needed for feature)
git add appsettings.json
```

**Always exclude:**
```bash
# Temporary files
git reset HEAD temp.txt
git reset HEAD *.tmp

# IDE configuration (should be in .gitignore)
.vscode/
.idea/
.vs/

# Build artifacts (should be in .gitignore)
bin/
obj/
dist/
node_modules/

# Secrets or credentials
git reset HEAD .env
git reset HEAD secrets.json
git reset HEAD credentials.config
```

### Git Add Commands

**Stage specific files:**
```bash
git add src/Services/OrderService.cs
git add tests/Services/OrderServiceTests.cs
```

**Stage by pattern:**
```bash
# All C# files in src/
git add src/**/*.cs

# All test files
git add tests/**/*Tests.cs

# All markdown files
git add docs/**/*.md
```

**Stage all changes (use carefully):**
```bash
# Stage everything (review first with git status!)
git add .
```

**Interactive staging (selective hunks):**
```bash
# Choose which changes to stage interactively
git add -p

# y = stage this hunk
# n = don't stage this hunk
# s = split into smaller hunks
# q = quit
```

### Reviewing Staged Changes

```bash
# See what's staged
git diff --staged

# See what's not staged
git diff

# See both staged and unstaged
git status
```

---

## Commit Message Template

### Bash Command Format

**Using heredoc for multi-line messages:**

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

- <change 1>
- <change 2>
- <change 3>
- Tests: <test description>
- Compliance: <context file references>
- Coverage: <percentage>

Closes #<story-id>
EOF
)"
```

**Important:** Use `<<'EOF'` (with quotes) to prevent bash variable expansion

### Template by Commit Type

#### feat (Feature)

```bash
git commit -m "$(cat <<'EOF'
feat(module): Brief description of feature

- Implemented <functionality>
- Added <components>
- Tests: <count> unit tests, <count> integration tests
- Compliance: tech-stack.md, coding-standards.md
- Coverage: <percentage>%

Closes #STORY-XXX
EOF
)"
```

#### fix (Bug Fix)

```bash
git commit -m "$(cat <<'EOF'
fix(module): Brief description of bug

- Fixed <issue>
- Root cause: <explanation>
- Added regression test
- Coverage: <percentage>%

Fixes #BUG-XXX
EOF
)"
```

#### refactor (Refactoring)

```bash
git commit -m "$(cat <<'EOF'
refactor(module): Brief description of refactoring

- Extracted <method/class>
- Removed duplication
- Improved <aspect>
- No behavior changes
- All tests still passing (100%)

Part of #STORY-XXX refactoring phase
EOF
)"
```

#### test (Tests Only)

```bash
git commit -m "$(cat <<'EOF'
test(module): Brief description of tests

- Added tests for <scenarios>
- Edge cases: <list>
- Coverage increased from X% to Y%

Part of #STORY-XXX TDD cycle
EOF
)"
```

---

## Push Timing and Best Practices

### When to Push

✅ **CORRECT timing:**
```bash
# After Phase 5: Integration complete
# All tests passing
# QA validation passed
# Ready for code review

git push origin feature/STORY-001-user-auth
```

✅ **CORRECT for checkpointing:**
```bash
# After significant milestone
# Tests passing
# Want to backup work

git push origin feature/STORY-001-user-auth
```

❌ **FORBIDDEN timing:**
```bash
# Don't push when tests are failing
# Don't push with commented-out code
# Don't push with secrets/credentials
# Don't push incomplete implementation (unless draft PR)
```

### Push Commands

**Standard push:**
```bash
# Push current branch to remote
git push origin feature/STORY-001-user-auth
```

**First push (set upstream):**
```bash
# Push and set upstream tracking
git push -u origin feature/STORY-001-user-auth

# Now can use simple 'git push'
git push
```

**Force push (use with caution):**
```bash
# ONLY use on personal feature branches
# NEVER use on shared branches (main, development)

git push --force-with-lease origin feature/STORY-001-user-auth
```

### Pre-Push Checklist

- [ ] All tests passing (`dotnet test` / `pytest` / `npm test`)
- [ ] Build succeeds (`dotnet build` / `npm run build`)
- [ ] No debug code or console.log statements
- [ ] No commented-out code
- [ ] No secrets or credentials in code
- [ ] Commit message follows conventions
- [ ] Changes reviewed with `git diff`

---

## Git Hooks Integration

### Pre-Commit Hook

**Purpose:** Validate changes before commit

**Checks:**
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run linter
npm run lint || exit 1

# Check for secrets
if git diff --cached | grep -i "password\|secret\|api_key"; then
    echo "❌ Secrets detected in commit"
    exit 1
fi

# Run quick tests
npm run test:quick || exit 1

echo "✅ Pre-commit checks passed"
exit 0
```

### Commit-Msg Hook

**Purpose:** Validate commit message format

**Checks:**
```bash
#!/bin/bash
# .git/hooks/commit-msg

commit_msg=$(cat "$1")

# Check conventional commit format
if ! echo "$commit_msg" | grep -E "^(feat|fix|refactor|test|docs|style|chore|perf|ci|build|revert)(\(.+\))?: .+"; then
    echo "❌ Commit message must follow conventional format"
    echo "Example: feat(auth): Add login endpoint"
    exit 1
fi

# Check message length
subject=$(echo "$commit_msg" | head -n1)
if [ ${#subject} -gt 100 ]; then
    echo "❌ Subject line must be ≤ 100 characters"
    exit 1
fi

echo "✅ Commit message validated"
exit 0
```

### Pre-Push Hook

**Purpose:** Run full validation before pushing

**Checks:**
```bash
#!/bin/bash
# .git/hooks/pre-push

# Run full test suite
echo "Running full test suite..."
npm test || exit 1

# Run code coverage
echo "Checking code coverage..."
npm run test:coverage || exit 1

# Check coverage threshold (example: 80%)
coverage=$(npm run test:coverage | grep "All files" | awk '{print $10}')
threshold=80

if [ "${coverage%.*}" -lt "$threshold" ]; then
    echo "❌ Coverage ${coverage}% below threshold ${threshold}%"
    exit 1
fi

echo "✅ Pre-push checks passed"
exit 0
```

---

## Branch Management

### Merging Strategies

#### Squash and Merge (Recommended)

**Use case:** Feature branches to main
**Benefits:** Clean history (one commit per feature)

```bash
# On GitHub/GitLab: Use "Squash and merge" button
# Combines all commits into one

# Manual squash:
git checkout main
git merge --squash feature/STORY-001-user-auth
git commit -m "feat: Implement user authentication (STORY-001)"
```

#### Merge Commit

**Use case:** Long-running branches (development → main)
**Benefits:** Preserves branch history

```bash
git checkout main
git merge feature/STORY-001-user-auth --no-ff
```

#### Rebase and Merge

**Use case:** Clean linear history
**Benefits:** No merge commits

```bash
git checkout feature/STORY-001-user-auth
git rebase main
git checkout main
git merge feature/STORY-001-user-auth --ff-only
```

### Branch Cleanup

**After merge:**
```bash
# Delete local branch
git branch -d feature/STORY-001-user-auth

# Delete remote branch
git push origin --delete feature/STORY-001-user-auth
```

---

## Multi-File Commit Organization

### Single Cohesive Commit (Recommended)

**When:** All changes are part of same story

```bash
# Stage all related files together
git add src/Services/OrderService.cs
git add src/Models/Order.cs
git add tests/Services/OrderServiceTests.cs
git add docs/api/orders.md

# Single commit for entire story
git commit -m "$(cat <<'EOF'
feat: Implement order management

- Created OrderService with CRUD operations
- Added Order model with validation
- Tests: 20 unit tests, 5 integration tests
- Documentation: Updated API docs
- Coverage: 95%

Closes #STORY-001
EOF
)"
```

### Multiple Logical Commits

**When:** Story has distinct logical phases

```bash
# Commit 1: Data model
git add src/Models/Order.cs
git commit -m "feat: Add Order data model"

# Commit 2: Service implementation
git add src/Services/OrderService.cs
git add tests/Services/OrderServiceTests.cs
git commit -m "feat: Implement OrderService with tests"

# Commit 3: API endpoints
git add src/Controllers/OrdersController.cs
git add docs/api/orders.md
git commit -m "feat: Add order API endpoints"

# Before merge: Squash into single commit
git rebase -i HEAD~3
```

---

## Git Workflow Checklist

### Pre-Commit Checklist

- [ ] Review changes: `git status`, `git diff`
- [ ] All tests passing
- [ ] Build succeeds
- [ ] No debug code
- [ ] No secrets in code
- [ ] Commit message follows format
- [ ] Only relevant files staged

### Pre-Push Checklist

- [ ] All commits follow conventions
- [ ] Full test suite passing
- [ ] Code coverage meets requirements
- [ ] No force push to shared branches
- [ ] Branch up to date with main

### Pre-Merge Checklist

- [ ] All CI checks passing
- [ ] Code review approved
- [ ] No merge conflicts
- [ ] Documentation updated
- [ ] Ready to deploy

---

## Quick Reference

### Git Commands Summary

```bash
# Status and review
git status                          # Show working tree status
git diff                            # Show unstaged changes
git diff --staged                   # Show staged changes
git log --oneline                   # Show commit history

# Staging
git add <file>                      # Stage specific file
git add .                           # Stage all changes
git add -p                          # Interactive staging

# Committing
git commit -m "message"             # Commit with inline message
git commit -m "$(cat <<'EOF'...)"   # Commit with heredoc

# Pushing
git push origin <branch>            # Push to remote
git push -u origin <branch>         # Push and set upstream
git push --force-with-lease         # Force push safely

# Branching
git checkout -b <branch>            # Create and switch to branch
git branch -d <branch>              # Delete local branch
git push origin --delete <branch>   # Delete remote branch
```

### Conventional Commit Types

| Type | Purpose |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code refactoring |
| `test` | Tests only |
| `docs` | Documentation |
| `chore` | Dependencies, build |
| `perf` | Performance |
| `style` | Formatting |

### Branch Name Patterns

```
feature/STORY-XXX-description
bugfix/BUG-XXX-description
hotfix/description
release/vX.Y.Z
```

---

This reference should be used during Phase 6 (Git Workflow) to maintain clean, traceable version control history that aligns with the TDD development process and DevForgeAI story-driven workflow.