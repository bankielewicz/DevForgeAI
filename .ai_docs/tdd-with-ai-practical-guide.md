# Test-Driven Development (TDD) with AI - Practical Guide

## Document Status

- **Type**: Research & Practical Guide
- **Evidence Level**: High - Based on academic research and Anthropic official recommendations
- **Last Updated**: 2025-10-09
- **Sources**: Anthropic Engineering, arXiv research papers, industry analysis

## Why TDD Works Exceptionally Well with AI

### Research-Backed Benefits

**Finding** (from academic research on MBPP, HumanEval, CodeChef datasets):
> "Including tests solves more programming problems than not including them. TDD is a better development model than just using a problem statement when using GPT4 for code generation tasks."

**Finding** (from industry analysis):
> "AI thrives on clear, measurable goals, and a binary test is one of the clearest goals you can give it."

**Finding** (Anthropic official):
> "Test-Driven Development: This is an Anthropic-favorite workflow for changes that are easily verifiable with unit, integration, or end-to-end tests."

### Why Tests Are Perfect AI Constraints

1. **Binary Success Criteria**
   - Test passes = Success
   - Test fails = Not done yet
   - No ambiguity, no judgment needed

2. **Iteration Capability**
   - AI can iterate until tests pass
   - Self-correcting based on test failures
   - Measurable progress

3. **Scope Definition**
   - Tests define exact behavior needed
   - No more, no less
   - Prevents feature creep

4. **Regression Prevention**
   - Existing tests must keep passing
   - Changes that break tests are immediately caught
   - Safe refactoring

5. **Human Labor Reduction**
   - AI excels at boilerplate test generation
   - Edge cases generated quickly
   - Humans focus on design, not typing

## The TDD Red-Green-Refactor Cycle with AI

### Traditional TDD (Human-Driven)

```
┌────────────────────────────────────────┐
│ RED: Write failing test (slow for humans) │
├────────────────────────────────────────┤
│ GREEN: Make test pass (slow for humans)   │
├────────────────────────────────────────┤
│ REFACTOR: Improve code (slow for humans)  │
└────────────────────────────────────────┘
```

**Problem**: Humans find writing tests tedious and time-consuming.

### TDD with AI (Human-Guided, AI-Executed)

```
┌────────────────────────────────────────┐
│ SPEC: Human defines behavior (fast)   │
├────────────────────────────────────────┤
│ RED: AI writes failing tests (fast)   │
├────────────────────────────────────────┤
│ GREEN: AI makes tests pass (fast)     │
├────────────────────────────────────────┤
│ REFACTOR: AI improves code (fast)     │
├────────────────────────────────────────┤
│ REVIEW: Human validates (critical)    │
└────────────────────────────────────────┘
```

**Advantage**: AI handles boilerplate, human provides judgment and domain knowledge.

## Complete TDD Workflow with AI

### Workflow 1: Human Writes Acceptance Criteria, AI Writes Tests

**Best for**: Features with clear requirements

**Step 1**: Human defines behavior (framework-agnostic)

```markdown
Feature: User Registration

Acceptance Criteria:

AC-1: WHEN user submits valid registration data (email, password, name)
      THEN account is created
      AND confirmation email is sent
      AND user receives success message

AC-2: WHEN user submits duplicate email
      THEN registration fails
      AND error message indicates email already exists
      AND no account is created

AC-3: WHEN user submits invalid email format
      THEN registration fails with validation error

AC-4: WHEN user submits password shorter than 8 characters
      THEN registration fails with validation error

AC-5: WHEN user submits password without uppercase, lowercase, and number
      THEN registration fails with validation error
```

**Step 2**: AI generates tests from acceptance criteria

**Prompt**:
```
"Read the acceptance criteria above.

Generate comprehensive tests for user registration.

Requirements:
1. Use [your test framework - e.g., Jest/pytest/xUnit]
2. Follow the existing test pattern in tests/auth/login.test.ts
3. One test per acceptance criterion minimum
4. Include edge cases
5. Use descriptive test names

File to create: tests/auth/register.test.ts

STOP after writing tests. Do NOT implement the registration logic yet."
```

**Step 3**: Human reviews tests

```bash
# Review test file
cat tests/auth/register.test.ts

# Verify completeness
# - All AC covered? ✓
# - Edge cases included? ✓
# - Test names descriptive? ✓
```

**Step 4**: Verify tests fail

```bash
npm test tests/auth/register.test.ts
# Should fail (not implemented yet)
```

**Step 5**: AI implements to make tests pass

**Prompt**:
```
"Implement the user registration logic to make all tests in tests/auth/register.test.ts pass.

Requirements:
1. Read the tests to understand what needs to be implemented
2. Follow the existing auth pattern in src/auth/login.ts
3. Use the existing email service in src/services/email.ts
4. Store users in the database using existing User model

Constraints:
- Do NOT modify the User model
- Do NOT change existing auth code
- Do NOT add new dependencies
- Implement ONLY what's needed to pass the tests

Verification:
After implementation, run: npm test tests/auth/register.test.ts
All tests must pass."
```

**Step 6**: Human verifies

```bash
# Run tests
npm test tests/auth/register.test.ts
# Should all pass

# Run full suite
npm test
# Should all pass (no regressions)

# Check coverage
npm run coverage
# Should meet minimum threshold

# Review code changes
git diff
```

### Workflow 2: AI Writes Tests and Implementation Together

**Best for**: Well-understood features with clear patterns

**Step 1**: Human provides specification

```markdown
Feature: Shopping Cart - Add Item

Requirements:
- User can add product to cart
- Quantity must be positive integer
- Product must exist in catalog
- Cart persists across sessions

Constraints:
- Use existing Cart model
- Follow existing product service pattern
- Do NOT modify checkout flow
```

**Step 2**: AI writes tests and implementation

**Prompt**:
```
"Implement 'Add Item to Cart' feature using strict TDD.

Process:
1. Read existing code: src/models/Cart.ts, src/services/ProductService.ts
2. Write failing tests first (Red phase)
3. Run tests to confirm they fail
4. Implement minimal code to pass tests (Green phase)
5. Run tests to confirm they pass
6. Refactor for quality (Refactor phase)
7. Run tests again to ensure still passing

After EACH phase, report status before proceeding.

Use Jest for tests.
Create tests/cart/addItem.test.ts
Modify src/services/CartService.ts

DO NOT:
- Modify Cart model
- Change ProductService
- Implement remove/update cart features
- Add any features beyond 'add item'"
```

**Step 3**: AI reports progress at checkpoints

```
AI: "Phase 1 (RED) complete. Created 8 tests in tests/cart/addItem.test.ts:
- test_add_valid_product_succeeds
- test_add_invalid_quantity_fails
- test_add_nonexistent_product_fails
- test_add_increases_cart_total
- test_add_same_product_increments_quantity
- test_add_to_empty_cart
- test_add_persists_to_database
- test_add_emits_cart_updated_event

Running tests... ❌ All tests fail (expected)

Proceed to Green phase?"
```

**Step 4**: Human approves or requests changes

```
Human: "Tests look good. The test for 'emits event' is not in requirements.
Remove that test. Then proceed to Green phase."
```

**Step 5**: AI implements

```
AI: "Removed event emission test.

Phase 2 (GREEN) complete. Implemented addItem() in CartService.

Running tests... ✅ All 7 tests pass

Proceed to Refactor phase?"
```

**Step 6**: Human reviews and approves

### Workflow 3: AI Generates Test Cases from Examples

**Best for**: Complex business logic

**Step 1**: Human provides example scenarios

```markdown
Feature: Shipping Cost Calculation

Example Scenarios:

Scenario 1:
- Order total: $50
- Shipping to: United States
- Expected shipping: $5 (flat rate)

Scenario 2:
- Order total: $100
- Shipping to: United States
- Expected shipping: $0 (free over $75)

Scenario 3:
- Order total: $60
- Shipping to: Canada
- Expected shipping: $15 (international)

Scenario 4:
- Order total: $200
- Shipping to: Canada
- Expected shipping: $15 (international, no free shipping)

Scenario 5:
- Order total: $50
- Items include: hazardous materials
- Expected shipping: $25 (hazmat surcharge)
```

**Step 2**: AI converts to tests

**Prompt**:
```
"Generate parameterized tests from the shipping cost scenarios above.

Use [your test framework]'s data-driven testing approach.
Create tests/shipping/calculateShipping.test.ts

Then implement the calculation logic to make tests pass.

Follow TDD strictly:
1. Write all test cases first
2. Verify they fail
3. Implement logic
4. Verify they pass"
```

**Result**: AI creates data-driven tests, all scenarios become test cases.

## Framework-Specific TDD Examples

### Example 1: JavaScript/TypeScript + Jest

**Acceptance Criteria**:
```markdown
AC-1: WHEN user validates email format
      THEN valid emails pass, invalid emails fail
```

**Test (AI-generated)**:
```typescript
// tests/validators/email.test.ts
import { validateEmail } from '@/validators/email';

describe('validateEmail', () => {
  describe('valid emails', () => {
    test.each([
      'user@example.com',
      'user.name@example.com',
      'user+tag@example.co.uk',
      'user_name@example.io'
    ])('should accept: %s', (email) => {
      expect(validateEmail(email)).toBe(true);
    });
  });

  describe('invalid emails', () => {
    test.each([
      'invalid',
      '@example.com',
      'user@',
      'user @example.com',
      'user@example',
    ])('should reject: %s', (email) => {
      expect(validateEmail(email)).toBe(false);
    });
  });
});
```

**Implementation (AI-generated)**:
```typescript
// src/validators/email.ts
export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}
```

### Example 2: Python + pytest

**Acceptance Criteria**:
```markdown
AC-1: WHEN calculating discount for order
      THEN 10% discount for orders >$100
      AND 20% discount for orders >$500
```

**Test (AI-generated)**:
```python
# tests/test_discount.py
import pytest
from services.discount import calculate_discount

@pytest.mark.parametrize("order_total,expected_discount", [
    (50.00, 0.00),      # Below threshold
    (100.00, 0.00),     # At threshold (not over)
    (100.01, 10.00),    # Just over first threshold
    (150.00, 15.00),    # 10% of 150
    (500.00, 50.00),    # At second threshold
    (500.01, 100.00),   # Just over second threshold (20%)
    (1000.00, 200.00),  # 20% of 1000
])
def test_calculate_discount(order_total, expected_discount):
    result = calculate_discount(order_total)
    assert result == expected_discount
```

**Implementation (AI-generated)**:
```python
# src/services/discount.py
def calculate_discount(order_total: float) -> float:
    """Calculate discount based on order total."""
    if order_total > 500:
        return order_total * 0.20
    elif order_total > 100:
        return order_total * 0.10
    return 0.0
```

### Example 3: C# + xUnit

**Acceptance Criteria**:
```markdown
AC-1: WHEN validating password strength
      THEN password must be at least 8 characters
      AND contain uppercase, lowercase, and number
```

**Test (AI-generated)**:
```csharp
// Tests/Validators/PasswordValidatorTests.cs
using Xunit;
using FluentAssertions;
using MyApp.Validators;

public class PasswordValidatorTests
{
    [Theory]
    [InlineData("Valid123", true)]
    [InlineData("AnotherValid1", true)]
    [InlineData("short1A", false)]           // Too short
    [InlineData("nouppercase1", false)]      // No uppercase
    [InlineData("NOLOWERCASE1", false)]      // No lowercase
    [InlineData("NoNumbers", false)]         // No numbers
    [InlineData("Valid1234567890", true)]    // Long valid
    public void ValidatePassword_ShouldReturnExpectedResult(string password, bool expected)
    {
        // Arrange
        var validator = new PasswordValidator();

        // Act
        var result = validator.Validate(password);

        // Assert
        result.Should().Be(expected);
    }
}
```

**Implementation (AI-generated)**:
```csharp
// Validators/PasswordValidator.cs
namespace MyApp.Validators
{
    public class PasswordValidator
    {
        public bool Validate(string password)
        {
            if (password.Length < 8) return false;
            if (!password.Any(char.IsUpper)) return false;
            if (!password.Any(char.IsLower)) return false;
            if (!password.Any(char.IsDigit)) return false;
            return true;
        }
    }
}
```

### Example 4: Go + testing

**Acceptance Criteria**:
```markdown
AC-1: WHEN parsing user input
      THEN valid integers are accepted
      AND invalid input returns error
```

**Test (AI-generated)**:
```go
// validators/parse_int_test.go
package validators

import "testing"

func TestParseUserInt(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    int
        wantErr bool
    }{
        {"valid positive", "42", 42, false},
        {"valid negative", "-10", -10, false},
        {"valid zero", "0", 0, false},
        {"invalid letters", "abc", 0, true},
        {"invalid mixed", "12abc", 0, true},
        {"invalid empty", "", 0, true},
        {"invalid spaces", "  42  ", 0, true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := ParseUserInt(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("ParseUserInt() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if got != tt.want {
                t.Errorf("ParseUserInt() = %v, want %v", got, tt.want)
            }
        })
    }
}
```

**Implementation (AI-generated)**:
```go
// validators/parse_int.go
package validators

import (
    "errors"
    "strconv"
    "strings"
)

func ParseUserInt(input string) (int, error) {
    trimmed := strings.TrimSpace(input)
    if trimmed != input {
        return 0, errors.New("input contains whitespace")
    }
    return strconv.Atoi(trimmed)
}
```

## Complete TDD Workflow Examples

### Example 1: Add New API Endpoint

**Language**: Any (examples show JavaScript, but process is identical for all)

**Phase 1: Human Defines Specification**

```markdown
# Specification: GET /api/users/:id

## Behavior
Retrieve user by ID

## Request
- Method: GET
- Path: /api/users/:id
- Parameters: userId (UUID format)

## Responses

200 OK:
{
  "id": "uuid",
  "email": "string",
  "name": "string",
  "createdAt": "ISO8601"
}

404 Not Found:
{
  "error": "User not found"
}

400 Bad Request:
{
  "error": "Invalid user ID format"
}

## Constraints
- Do NOT return password field
- Do NOT modify existing /api/users POST endpoint
- Use existing User model
- Follow existing error handling pattern
```

**Phase 2: Prompt AI to Write Tests**

```
"Read the specification above.

Write comprehensive tests for GET /api/users/:id endpoint.

Requirements:
1. Use existing test setup from tests/api/auth.test.ts
2. Test all response codes (200, 404, 400)
3. Test validation (invalid UUID format)
4. Test that password is NOT returned
5. Use descriptive test names

Create: tests/api/users.test.ts

STOP after writing tests."
```

**Phase 3: AI Generates Tests**

```typescript
// tests/api/users.test.ts
import request from 'supertest';
import { app } from '@/app';
import { createTestUser, cleanupTestDb } from './helpers';

describe('GET /api/users/:id', () => {
  beforeEach(async () => {
    await cleanupTestDb();
  });

  describe('200 OK responses', () => {
    it('should return user when valid ID provided', async () => {
      const testUser = await createTestUser({
        email: 'test@example.com',
        name: 'Test User'
      });

      const res = await request(app)
        .get(`/api/users/${testUser.id}`)
        .expect(200);

      expect(res.body).toHaveProperty('id', testUser.id);
      expect(res.body).toHaveProperty('email', 'test@example.com');
      expect(res.body).toHaveProperty('name', 'Test User');
      expect(res.body).toHaveProperty('createdAt');
    });

    it('should NOT return password field', async () => {
      const testUser = await createTestUser({
        email: 'test@example.com',
        password: 'secret123'
      });

      const res = await request(app)
        .get(`/api/users/${testUser.id}`)
        .expect(200);

      expect(res.body).not.toHaveProperty('password');
      expect(res.body).not.toHaveProperty('passwordHash');
    });
  });

  describe('404 Not Found responses', () => {
    it('should return 404 when user does not exist', async () => {
      const nonExistentId = '550e8400-e29b-41d4-a716-446655440000';

      const res = await request(app)
        .get(`/api/users/${nonExistentId}`)
        .expect(404);

      expect(res.body).toHaveProperty('error', 'User not found');
    });
  });

  describe('400 Bad Request responses', () => {
    it('should return 400 when ID is not valid UUID', async () => {
      const res = await request(app)
        .get('/api/users/invalid-id')
        .expect(400);

      expect(res.body).toHaveProperty('error', 'Invalid user ID format');
    });

    it('should return 400 when ID is empty', async () => {
      const res = await request(app)
        .get('/api/users/')
        .expect(400);
    });
  });
});
```

**Phase 4: Human Reviews Tests**

```bash
# Review
cat tests/api/users.test.ts

# Verify coverage
# - All response codes? ✓
# - Password exclusion? ✓
# - Edge cases? ✓
```

**Phase 5: Run Tests (Should Fail)**

```bash
npm test tests/api/users.test.ts

# Expected output:
# ✗ should return user when valid ID provided
# ✗ should NOT return password field
# ✗ should return 404 when user does not exist
# ✗ should return 400 when ID is not valid UUID
# ✗ should return 400 when ID is empty
#
# 0 passing, 5 failing
```

**Phase 6: Prompt AI to Implement**

```
"The tests are written and failing as expected.

Now implement the GET /api/users/:id endpoint to make all tests pass.

Requirements:
1. Read tests/api/users.test.ts to see what needs to pass
2. Add route in src/api/routes.ts (follow existing pattern)
3. Create controller in src/controllers/UserController.ts
4. Use existing User model and database service

Constraints:
- Implement ONLY what's needed to pass the tests
- Do NOT add extra features (update user, delete user, etc.)
- Do NOT modify existing endpoints
- Follow the error handling pattern in other controllers

After implementation:
1. Run: npm test tests/api/users.test.ts
2. Report: How many tests pass/fail
3. If any fail, fix and re-run"
```

**Phase 7: AI Implements and Reports**

```
AI: "Implementation complete.

Created:
- src/controllers/UserController.ts (getById method)
- Added route in src/api/routes.ts

Running tests...
✅ should return user when valid ID provided
✅ should NOT return password field
✅ should return 404 when user does not exist
✅ should return 400 when ID is not valid UUID
✅ should return 400 when ID is empty

5 passing, 0 failing

All tests pass!"
```

**Phase 8: Human Validates**

```bash
# Run full test suite
npm test
# All tests should pass (including existing ones)

# Check for regressions
git diff src/api/routes.ts
# Should see only one new route added

# Check controller
cat src/controllers/UserController.ts
# Should see clean, focused implementation

# Verify no unrelated changes
git status
# Should only show:
# - tests/api/users.test.ts
# - src/controllers/UserController.ts
# - src/api/routes.ts
```

## Advanced TDD Patterns with AI

### Pattern 1: Outside-In TDD

**Start from user interface, work inward**

```
┌────────────────────────────────┐
│ 1. Integration Test (API)     │ ← Human defines
├────────────────────────────────┤
│ 2. Service Test               │ ← AI generates
├────────────────────────────────┤
│ 3. Repository Test            │ ← AI generates
├────────────────────────────────┤
│ 4. Implement (inside-out)     │ ← AI implements
└────────────────────────────────┘
```

**Example Prompt**:
```
"Implement user search using outside-in TDD.

Step 1: Write integration test for GET /api/users/search?q=john
Step 2: Write service test for UserService.search()
Step 3: Write repository test for UserRepository.findByQuery()
Step 4: Implement each layer to make tests pass

Report after EACH step before proceeding."
```

### Pattern 2: Test-First Bug Fixes

**Write reproduction test before fixing**

**Step 1**: Human reports bug

```markdown
Bug: User can login with incorrect password

Steps to Reproduce:
1. User enters correct email
2. User enters WRONG password
3. System allows login (should reject)

Expected: Login fails with 401
Actual: Login succeeds with 200
```

**Step 2**: AI writes failing test

```
"Write a test that reproduces the bug described above.

Test should:
1. Create a user with known password
2. Attempt login with WRONG password
3. Assert that login is rejected (401)

This test will currently PASS (proving the bug exists).
After we fix the bug, the test should FAIL.

Create: tests/bugs/auth-bug-001.test.ts"
```

**Step 3**: Verify test proves bug

```bash
npm test tests/bugs/auth-bug-001.test.ts
# Test passes = Bug confirmed
```

**Step 4**: AI fixes bug

```
"Fix the bug so that tests/bugs/auth-bug-001.test.ts fails.

Requirements:
- Find where password validation happens
- Fix the logic
- Do NOT change the test
- All other tests must still pass"
```

**Step 5**: Verify fix

```bash
npm test tests/bugs/auth-bug-001.test.ts
# Test should now fail (bug fixed)

npm test
# All other tests should still pass
```

### Pattern 3: Property-Based Testing

**For complex logic with many input combinations**

**Example** (framework-agnostic concept):

```
Property: "Sorting function should return sorted array"

Test cases (generated):
- Empty array → []
- Single element → [1]
- Already sorted → [1,2,3]
- Reverse sorted → [3,2,1]
- Random order → [2,1,3]
- Duplicates → [1,1,2]
- All same → [1,1,1]
- Negative numbers → [-3,-1,-2]
```

**Prompt to AI**:
```
"Write property-based tests for the sorting function.

Use [fast-check for JS / Hypothesis for Python / FsCheck for C#]

Properties to test:
1. Output length equals input length
2. All elements from input appear in output
3. Output is in ascending order
4. Sorting is stable (equal elements maintain order)

Generate at least 100 random test cases per property."
```

## Integration with DevForgeAI Framework

### How DevForgeAI Enables TDD

**DevForgeAI provides the SDLC structure**:

```
Analyst Persona
    ↓ Requirements with acceptance criteria
[VALIDATION GATE]
    ↓
Architect Persona
    ↓ Design with technical approach
[VALIDATION GATE]
    ↓
Product Owner Persona
    ↓ Stories with EARS-format AC
[VALIDATION GATE]
    ↓
Developer Persona (TDD)
    ↓ Tests from AC → Implementation
[VALIDATION GATE]
    ↓
QA Persona
    ↓ Validation against requirements
```

### DevForgeAI + TDD Workflow

**Story Input** (from PO persona):
```markdown
Story: DEVFORGE-STORY-123

As a developer
I want to validate story acceptance criteria
So that I know the story is ready for implementation

Acceptance Criteria:
AC-1: WHEN story has EARS-format acceptance criteria
      THEN validation passes

AC-2: WHEN story missing acceptance criteria
      THEN validation HALTS with error

AC-3: WHEN story has ambiguous criteria (score >7)
      THEN validation FAILS with ambiguity report
```

**Developer Persona Process**:

```bash
# Step 1: Read story
/dev:implement-story DEVFORGE-STORY-123.md

# Step 2: AI generates tests from AC
# Creates: tests/validation/story-validator.test.ts

# Step 3: AI runs tests (should fail)
# Reports: 3 tests failing (expected)

# Step 4: AI implements validation logic
# Creates: src/validation/story-validator.ts

# Step 5: AI runs tests
# Reports: 3 tests passing

# Step 6: AI validates Definition of Done
# Checks:
# - All AC have tests? ✓
# - All tests pass? ✓
# - Coverage ≥80%? ✓
# - Linter passes? ✓
# - No TODOs? ✓

# Step 7: Human reviews
git diff

# Step 8: Commit
git commit -m "feat: implement story validation"
```

## Best Practices (Evidence-Based)

### 1. Always Write Tests First

**Why** (from research):
- Measurably better success rate
- Prevents scope creep
- Provides clear goal for AI

**How**:
```
❌ "Implement user registration"

✅ "Write tests for user registration first.
   Then implement to make tests pass."
```

### 2. Keep Tests Simple and Focused

**Why**: AI can understand and satisfy simple tests better

**Example**:
```javascript
// ✅ Good: Single assertion
test('should return user by ID', async () => {
  const user = await getUserById('123');
  expect(user.id).toBe('123');
});

// ❌ Too complex: Multiple concerns
test('should handle complete user workflow', async () => {
  const user = await createUser({...});
  await loginUser(user);
  await updateUser(user.id, {...});
  const updated = await getUserById(user.id);
  expect(updated).toMatchObject({...});
  await deleteUser(user.id);
});
```

### 3. Use Descriptive Test Names

**Why**: AI uses test names to understand intent

**Pattern**: `should_[expected behavior]_when_[condition]`

```python
# ✅ Good: Clear intent
def test_should_return_401_when_password_invalid():
    pass

def test_should_create_user_when_data_valid():
    pass

# ❌ Unclear
def test_user():
    pass

def test_case_1():
    pass
```

### 4. Run Tests Frequently

**From Anthropic best practices**: Human should run tests, not AI

**Why**: Human can judge failures and provide direction

**Workflow**:
```bash
# After AI writes tests
npm test

# After AI implements
npm test

# After AI refactors
npm test

# Human interprets results and guides AI
```

### 5. Use Test Coverage as Quality Gate

**Enforce minimum coverage**:

```bash
# In your test command
npm test -- --coverage --coverageThreshold='{"global":{"statements":80,"branches":80,"functions":80,"lines":80}}'
```

**In CLAUDE.md**:
```markdown
## Testing Requirements

- Minimum 80% code coverage
- All public functions must have tests
- All edge cases must be tested
- Integration tests for API endpoints
- No implementation without tests
```

### 6. Leverage Parameterized Tests

**Why**: Tests many cases with little code

**JavaScript (Jest)**:
```javascript
test.each([
  [100, 10],    // 10% discount
  [500, 100],   // 20% discount
  [50, 0],      // No discount
])('should calculate discount: $%i → $%i', (amount, expectedDiscount) => {
  expect(calculateDiscount(amount)).toBe(expectedDiscount);
});
```

**Python (pytest)**:
```python
@pytest.mark.parametrize("amount,expected", [
    (100, 10),   # 10% discount
    (500, 100),  # 20% discount
    (50, 0),     # No discount
])
def test_calculate_discount(amount, expected):
    assert calculate_discount(amount) == expected
```

**C# (xUnit)**:
```csharp
[Theory]
[InlineData(100, 10)]   // 10% discount
[InlineData(500, 100)]  // 20% discount
[InlineData(50, 0)]     // No discount
public void ShouldCalculateDiscount(decimal amount, decimal expected)
{
    Assert.Equal(expected, CalculateDiscount(amount));
}
```

## Common Pitfalls and Solutions

### Pitfall 1: AI Implements Before Tests

**Problem**: AI starts coding immediately

**Solution**: Explicit instructions

```
❌ "Implement user search"

✅ "STOP. Do NOT implement yet.

   First: Write tests for user search
   Then: Wait for my approval
   Finally: Implement to make tests pass"
```

### Pitfall 2: AI Modifies Tests to Make Them Pass

**Problem**: AI changes tests instead of implementation

**Solution**: Mark tests as immutable

```
"Implement code to make tests pass.

CONSTRAINT: Do NOT modify the tests.
If a test seems wrong, STOP and ask me.
Only change implementation code."
```

### Pitfall 3: AI Adds "Helpful" Features

**Problem**: AI implements beyond test scope

**Solution**: Explicit scope boundaries

```
"Implement ONLY the login feature to pass these tests.

Do NOT add:
- Password reset
- Registration
- OAuth
- Email verification
- Profile management

If you think any of these are needed, STOP and ask."
```

### Pitfall 4: AI Skips Edge Cases

**Problem**: AI writes only happy-path tests

**Solution**: Require edge case coverage

```
"Write tests including these edge cases:

Happy path:
- Valid input succeeds

Edge cases:
- Empty input
- Null input
- Extremely large values
- Negative values
- Special characters
- Boundary values (0, max int, etc.)
- Concurrent access

Generate tests for ALL of these."
```

### Pitfall 5: Tests Pass But Requirements Not Met

**Problem**: Tests don't fully capture requirements

**Solution**: Human writes or reviews test spec

```
Human writes test specification:
"Tests must verify:
1. Valid login works ✓
2. Invalid password fails ✓
3. Rate limiting works ✓
4. Passwords are hashed (NOT plaintext) ← Often forgotten
5. Failed attempts are logged ← Often forgotten
6. Timing attacks prevented ← Often forgotten"

Then AI generates tests for all 6 requirements.
```

## Measuring TDD Effectiveness

### Metrics to Track

**Before Merging**:
- [ ] Test coverage ≥ target (e.g., 80%)
- [ ] All tests passing
- [ ] No skipped tests
- [ ] No test warnings

**After Deployment**:
- [ ] No bugs related to tested functionality
- [ ] No regressions in tested areas
- [ ] Refactoring safe (tests catch issues)

### Example Coverage Report

```bash
# JavaScript (Jest)
npm run test:coverage

# Python (pytest)
pytest --cov=src --cov-report=term-missing

# C# (.NET)
dotnet test /p:CollectCoverage=true /p:CoverageReportsDirectory=./coverage

# Go
go test -cover ./...
```

**Require minimum coverage**:
```
Statements: 85%
Branches: 80%
Functions: 90%
Lines: 85%
```

## Framework-Agnostic TDD Checklist

Use this checklist regardless of language/framework:

### Pre-Implementation

- [ ] Requirements clearly defined
- [ ] Acceptance criteria written
- [ ] Edge cases identified
- [ ] Test framework selected
- [ ] Test structure planned

### During Development (Red Phase)

- [ ] Tests written for all acceptance criteria
- [ ] Tests written for edge cases
- [ ] Tests use descriptive names
- [ ] Tests are isolated (no dependencies on execution order)
- [ ] Tests run successfully (even though failing)
- [ ] All tests fail for right reason (not implemented)

### During Development (Green Phase)

- [ ] Implementation makes tests pass
- [ ] Only minimal code added (no gold-plating)
- [ ] No features beyond test scope
- [ ] All new tests passing
- [ ] All existing tests still passing

### During Development (Refactor Phase)

- [ ] Code follows style guide
- [ ] No duplication
- [ ] Clear variable/function names
- [ ] Appropriate abstractions
- [ ] Tests still passing after refactor

### Post-Implementation

- [ ] Full test suite passes
- [ ] Coverage meets minimum threshold
- [ ] No skipped tests
- [ ] No TODO comments
- [ ] Linter passes
- [ ] Performance benchmarks met
- [ ] Definition of Done satisfied

## References

### Academic Research

- **"Test-Driven Development for Code Generation"** (arXiv:2402.13521v1)
  - Datasets: MBPP, HumanEval, CodeChef
  - Finding: TDD improves AI code generation success rate

### Official Documentation

- **Anthropic Engineering**: "Claude Code Best Practices"
  - TDD recommended as "Anthropic-favorite workflow"
  - URL: https://www.anthropic.com/engineering/claude-code-best-practices

### Industry Articles

- **The New Stack**: "Claude Code and the Art of Test-Driven Development"
- **Builder.io**: "Test-Driven Development with AI"
- **DAGWorks Blog**: "Test Driven Development (TDD) of LLM / Agent Applications"
- **Medium (Multiple Authors)**: TDD with LLMs guides

### Industry Standards

- **Contract-First API Development** (Moesif, InfoQ, Microsoft)
- **OpenAPI Specification** (API contracts)
- **Design-First Approach** (Stoplight, Swagger, Postman)

---

**Document Version**: 1.0
**Evidence Level**: High - All practices sourced from research or official documentation
**Aspirational Content**: None
**Framework Dependency**: None - Patterns apply universally
**Applicability**: Small to large projects, any language/framework
