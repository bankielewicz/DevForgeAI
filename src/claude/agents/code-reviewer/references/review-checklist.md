# Code Review Checklist for Code Reviewer

**Version**: 1.0 | **Status**: Reference | **Agent**: code-reviewer

---

## 1. Code Quality

**Readability:**
- [ ] Clear, descriptive variable and function names
- [ ] Proper indentation and formatting
- [ ] Comments explain WHY, not WHAT
- [ ] Complex logic broken into smaller functions
- [ ] No magic numbers (use named constants)

**Simplicity:**
- [ ] Code is as simple as possible (KISS principle)
- [ ] No unnecessary abstraction
- [ ] Functions do one thing (Single Responsibility)
- [ ] Cyclomatic complexity < 10 per method

**Maintainability:**
- [ ] No code duplication (DRY principle)
- [ ] Consistent coding style
- [ ] Functions < 50 lines
- [ ] Classes < 500 lines (God Object anti-pattern)

## 2. Security

**Critical Security Checks:**
- [ ] No hardcoded secrets, API keys, or passwords
- [ ] Input validation implemented
- [ ] Output encoding for user-generated content
- [ ] Parameterized queries (no SQL concatenation)
- [ ] Authentication and authorization checks present
- [ ] No sensitive data in logs
- [ ] Proper error handling (no stack traces to users)

**Common Vulnerabilities:**
```javascript
// BAD: SQL injection
const query = `SELECT * FROM users WHERE id = ${userId}`;
// GOOD: Parameterized query
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);

// BAD: Hardcoded secret
const apiKey = 'sk_live_123456789abcdef';
// GOOD: Environment variable
const apiKey = process.env.API_KEY;
```

## 3. Error Handling

- [ ] Try-catch blocks where errors expected
- [ ] Specific exception types caught
- [ ] No empty catch blocks
- [ ] Errors logged with context
- [ ] User-friendly error messages
- [ ] Cleanup in finally blocks

## 4. Performance

- [ ] No N+1 query patterns
- [ ] Appropriate data structures used
- [ ] Loops optimized (no unnecessary iterations)
- [ ] Lazy loading where appropriate
- [ ] Caching considered for expensive operations
- [ ] No unnecessary database calls in loops

## 5. Testing

- [ ] New functionality has tests
- [ ] Tests follow AAA pattern (Arrange, Act, Assert)
- [ ] Edge cases covered
- [ ] Error conditions tested
- [ ] Tests are readable and maintainable
- [ ] No flaky tests (deterministic)

## 6. Standards Compliance

- [ ] Follows patterns from coding-standards.md
- [ ] No anti-patterns from anti-patterns.md
- [ ] Uses approved technologies from tech-stack.md
- [ ] Proper dependency injection (not direct instantiation)
- [ ] Respects layer boundaries from architecture-constraints.md

## 7. Definition of Done Completeness

**Valid deferral patterns:**
- "Deferred to STORY-{number}: {justification}"
- "Blocked by {external_system}: {specific reason with ETA}"
- "Out of scope: ADR-{number}"
- "User approved via AskUserQuestion: {context}"

**Invalid deferral patterns (flag as HIGH):**
- "Will add later"
- "Not enough time"
- "Too complex"
- "Optional"
- "Deferred" (no details)
- Empty reason

## Common Code Smells

| Smell | Threshold | Fix |
|-------|-----------|-----|
| Long Method | >50 lines | Extract methods |
| Large Class | >500 lines | Split classes |
| Duplicate Code | Similar logic in 2+ places | Extract shared function |
| Feature Envy | Method uses other class data more than own | Move method |
| Primitive Obsession | Primitives instead of objects | Create value objects |
| Long Parameter List | >4 parameters | Group into parameter object |

## Issue Categories

### Critical Issues
Security vulnerabilities, data corruption risks, broken functionality, context violations.
Examples: Hardcoded secrets, SQL injection, authentication bypass, layer boundary violations.

### Warnings
Code smells, maintainability issues, performance concerns, potential bugs.
Examples: High cyclomatic complexity, code duplication, missing error handling, N+1 queries.

### Suggestions
Optimization opportunities, refactoring ideas, better practices.
Examples: Performance optimizations, code simplification, better abstraction.
