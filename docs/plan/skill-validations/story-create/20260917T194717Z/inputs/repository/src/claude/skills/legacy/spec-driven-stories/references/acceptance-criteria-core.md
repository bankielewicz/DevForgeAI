# Acceptance Criteria — Core Principles & Universal Patterns

Core principles, Given/When/Then syntax, and universal patterns that apply to ALL story types. Always loaded in Phase 02.

**See also:**
- `acceptance-criteria-domains.md` — Domain-specific patterns (CRUD, Auth, Workflow, etc.)
- `acceptance-criteria-refactor.md` — Refactor-only patterns (conditionally loaded)

---

## Purpose

This guide provides proven principles for writing testable, unambiguous acceptance criteria. The universal content here applies to every story type. Domain-specific pattern libraries are in `acceptance-criteria-domains.md`.

---

## Core Principles

### Testability

**Every acceptance criterion must be verifiable through automated testing.**

✅ **Testable:**
```
Given user is logged in
When user clicks "Logout" button
Then user session is terminated and redirected to login page
```
**Why:** Can write test that verifies session termination and redirect

❌ **Not Testable:**
```
User should have a good experience when logging out
```
**Why:** "good experience" is subjective, cannot automate

### Completeness

**Acceptance criteria must cover:**
- Happy path (successful completion)
- Error scenarios (validation failures, system errors)
- Edge cases (boundary conditions, concurrent access)
- Security scenarios (unauthorized access, injection attempts)

### Unambiguity

**Avoid vague language:**
- ❌ "should", "might", "could", "probably"
- ❌ "fast", "slow", "easy", "intuitive"
- ❌ "user-friendly", "responsive", "efficient"

**Use specific, measurable terms:**
- ✅ "within 500ms", "less than 2 seconds"
- ✅ "displays error message 'Invalid email format'"
- ✅ "supports 1,000 concurrent users"

---

## Given/When/Then Format

### Structure

**Given** - Context/Precondition
- System state before action
- User authentication/authorization state
- Data that already exists
- External system state

**When** - Action/Trigger
- User action (click, type, submit, navigate)
- System event (timer, webhook, message)
- External trigger (API call, scheduled job)

**Then** - Expected Outcome
- System response
- Data changes
- UI updates
- Side effects (emails sent, logs created)

### Examples by Complexity

**Simple (Single action, single outcome):**
```
Given user is on homepage
When user clicks "Sign Up" button
Then registration form displays
```

**Moderate (Multiple conditions):**
```
Given user is logged in as admin
And there are 10 users in the database
When user navigates to "/admin/users" page
Then all 10 users are displayed in a table with columns: Name, Email, Role, Status
```

**Complex (Multiple steps and validations):**
```
Given user has items in shopping cart totaling $150
And user has selected express shipping ($25)
And user has applied coupon "SAVE10" (10% off)
When user proceeds to checkout
Then order total displays as $160.50 ($150 - $15 discount + $25 shipping)
And payment page loads within 2 seconds
And order summary shows itemized breakdown
```

---

## Error Handling Patterns (Universal)

### Network Errors

```
### AC1: API request fails (network error)
Given user submits form
When network request fails (no connection)
Then error message displays "Connection error. Please check your internet and try again."
And form data is preserved (not lost)
And "Retry" button is displayed
And user can retry without re-entering data
```

### Server Errors (5XX)

```
### AC2: Server error (500)
Given user submits request
When server returns 500 Internal Server Error
Then error message displays "Something went wrong. Our team has been notified. Please try again later."
And error is logged with request ID for debugging
And user can retry or contact support
And request ID is shown to user (for support reference)
```

### Validation Errors (400)

```
### AC3: Multiple validation errors
Given user submits form with 3 invalid fields
When server returns 400 with validation errors
Then all 3 errors are displayed near their respective fields
And first invalid field receives focus
And error summary displays at top: "Please correct 3 errors below"
And screen reader announces "Form has errors"
```

### Timeout Errors

```
### AC4: Request timeout
Given user submits request
When request takes longer than 30 seconds
Then timeout error displays "Request taking longer than expected"
And options displayed: "Keep waiting" or "Cancel"
And if user keeps waiting, timeout extends by 30 seconds
And if user cancels, request is aborted (if possible)
```

---

## Edge Case Patterns (Universal)

### Boundary Conditions

```
### ACX: Empty input handling
Given user submits form with all fields empty
Then validation errors display for all required fields
And form is not submitted
And focus moves to first invalid field

Given user submits form with whitespace-only values ("   ")
Then validation treats as empty
And error displays "{Field} cannot be blank"
```

```
### ACX: Maximum length handling
Given field has max_length = 100 characters
When user types 100 characters
Then input is accepted
And character counter shows "100/100"

When user tries to type 101st character
Then input is rejected (character not entered)
And counter shows "100/100" in warning color
```

```
### ACX: Minimum value handling
Given quantity field has minimum = 1
When user enters 0 or negative number
Then validation error displays "Quantity must be at least 1"
And submit is disabled

When user enters 1
Then validation passes
```

### Concurrent Access

```
### ACX: Two users edit same record
Given User A loads {entity} at time T1
And User B loads same {entity} at time T2
And User B saves changes at time T3
When User A tries to save changes at time T4
Then conflict detection triggers
And message displays "This {entity} was modified by {User B} at {T3}. Please refresh and retry."
And User A's changes are preserved (shown in comparison view)
And User A can choose: Overwrite, Merge, or Cancel
```

### Race Conditions

```
### ACX: Prevent duplicate submission
Given user clicks "Submit" button on payment form
When network is slow (2 second delay)
And user clicks "Submit" button again (double-click)
Then only ONE payment request is sent
And button is disabled after first click
And loading spinner displays
And duplicate click is ignored (no second request)
```

### Session Expiration

```
### ACX: Session expires during form fill
Given user session expires after 30 minutes of inactivity
And user has been filling form for 35 minutes
When user submits form
Then 401 Unauthorized response
And modal displays "Your session has expired. Please log in again to continue."
And form data is preserved in session storage
And after login, user is returned to form with data intact
```

### Data Loss Prevention

```
### ACX: Browser refresh with unsaved changes
Given user has modified form fields
And changes are not saved
When user attempts to refresh page or navigate away
Then browser confirmation displays "You have unsaved changes. Are you sure you want to leave?"
And if user confirms: Changes are lost
And if user cancels: User remains on page with changes intact
```

---

## Testing Guidance

### How to Write Tests from Acceptance Criteria

**Each Given/When/Then maps to test structure:**

**Acceptance Criterion:**
```
Given user is logged in
When user clicks "Profile" link
Then profile page displays user's name and email
```

**Corresponding Test (AAA Pattern):**
```javascript
test('displays user profile when logged in', async () => {
  // ARRANGE (Given)
  const user = await createTestUser({ name: 'John Doe', email: 'john@example.com' });
  await loginAs(user);

  // ACT (When)
  await click('Profile');

  // ASSERT (Then)
  expect(screen.getByText('John Doe')).toBeInTheDocument();
  expect(screen.getByText('john@example.com')).toBeInTheDocument();
});
```

### Test Coverage Requirements

**From acceptance criteria:**
- Each AC becomes at least 1 automated test
- Happy path scenarios → positive tests
- Error scenarios → negative tests
- Edge cases → boundary tests

**Example:**
```
Story has 5 acceptance criteria:
- AC1 (happy path) → 1 test
- AC2 (validation error) → 1 test
- AC3 (edge case: empty data) → 1 test
- AC4 (edge case: max data) → 1 test
- AC5 (concurrent access) → 1 test

Minimum: 5 tests from acceptance criteria
Additional: Integration tests, E2E tests
```

---

## Integration with Technical Specification (v2.0)

**For stories using v2.0 structured YAML format:**

**Acceptance criteria drive tech spec components:**

**Example mapping:**

**AC:** "Given user submits registration form, When validation passes, Then account created"

**Generates components:**
```yaml
components:
  - type: "API"
    name: "UserRegistration"
    endpoint: "/api/users/register"
    method: "POST"
    requirements:
      - id: "API-001"
        description: "Must validate email format before account creation"
        test_requirement: "Test: POST with invalid email returns 400 Bad Request"
        priority: "Critical"

  - type: "Service"
    name: "UserRegistrationService"
    file_path: "src/Application/Services/UserRegistrationService.cs"
    requirements:
      - id: "SVC-001"
        description: "Must create user account when validation passes"
        test_requirement: "Test: Valid request creates user in database"
        priority: "Critical"
```

**Each Given/When/Then should map to:**
- Component requirement (what must be built)
- Test requirement (how to verify it)

**See:** `technical-specification-creation.md` for complete v2.0 generation guide

---

**Use these principles to write complete, testable, unambiguous acceptance criteria that enable TDD implementation and automated validation. For domain-specific patterns (CRUD, Auth, Workflow, etc.), see `acceptance-criteria-domains.md`.**
