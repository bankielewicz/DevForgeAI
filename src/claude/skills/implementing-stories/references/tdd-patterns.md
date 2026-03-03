# Test-Driven Development Patterns

## TDD Cycle: Red -> Green -> Refactor

### Red Phase: Write Failing Test

1. Identify ONE specific behavior to test
2. Write test that exercises that behavior
3. Run test -> MUST fail (if passes, test is wrong)
4. Verify failure is for the RIGHT reason (not syntax error)

### Green Phase: Make Test Pass

1. Write MINIMAL code to pass the test
2. Implement simplest solution that passes
3. Run test -> MUST pass
4. Do not add features not covered by tests

### Refactor Phase: Improve Code

1. Improve code quality WITHOUT changing behavior
2. Extract magic numbers, helper methods, rename for clarity
3. Remove duplication
4. Run tests after EVERY change -> MUST stay green

---

## Test Naming Convention

**Pattern:** `MethodName_Scenario_ExpectedBehavior`

**Examples:**
- `CalculateDiscount_ValidCoupon_ReturnsDiscountedPrice`
- `CalculateDiscount_ExpiredCoupon_ReturnsOriginalPrice`
- `CalculateDiscount_NullCoupon_ThrowsArgumentNullException`

Use AAA (Arrange-Act-Assert) or Given-When-Then structure consistently within a project.

---

## Coverage Thresholds (ADR-010)

**Coverage gaps are CRITICAL blockers, NOT warnings.**

| Layer | Minimum Coverage | Enforcement |
|-------|------------------|-------------|
| Business Logic | 95% | CRITICAL - blocks QA |
| Application | 85% | CRITICAL - blocks QA |
| Infrastructure | 80% | CRITICAL - blocks QA |

If coverage is below threshold, QA result MUST be "FAILED", not "PASS WITH WARNINGS". Coverage gaps cannot be deferred.

**Coverage priority:**
- **High:** Business logic, validation rules, state transitions, error handling, edge cases
- **Lower:** Property getters/setters (unless logic), simple constructors, mapping code, auto-generated code

### Generating Coverage Reports

```bash
# .NET
dotnet test --collect:"XPlat Code Coverage"

# Python
pytest --cov=src --cov-report=html --cov-report=term

# JavaScript
npm test -- --coverage
```

---

## Test Error Handling (Result Pattern)

**When coding-standards.md specifies Result Pattern, test both paths:**

```csharp
// Failure path
[Fact]
public void ValidateOrder_InvalidOrder_ReturnsFailureResult()
{
    var service = new OrderService();
    var result = service.ValidateOrder(new Order { Total = -10m });

    Assert.False(result.IsSuccess);
    Assert.Equal("Order total cannot be negative", result.Error);
}

// Success path
[Fact]
public void ValidateOrder_ValidOrder_ReturnsSuccessResult()
{
    var service = new OrderService();
    var result = service.ValidateOrder(new Order { Total = 100m, CustomerId = 1 });

    Assert.True(result.IsSuccess);
    Assert.Null(result.Error);
}
```

---

## Test Independence Rules

Each test MUST:
- Set up its own data (no shared mutable state)
- Not depend on other tests' execution order
- Clean up after itself
- Be runnable in isolation

```csharp
// FORBIDDEN: Tests depend on execution order
private static Order _sharedOrder;

[Fact]
public void Test1_CreateOrder() { _sharedOrder = new Order { Id = 1 }; }

[Fact]
public void Test2_UpdateOrder() { _sharedOrder.Status = OrderStatus.Completed; } // Fails if Test1 didn't run
```

```csharp
// CORRECT: Each test creates its own data
[Fact]
public void UpdateOrder_PendingOrder_UpdatesStatus()
{
    var order = new Order { Id = 1, Status = OrderStatus.Pending };
    var service = new OrderService();

    service.UpdateOrderStatus(order, OrderStatus.Completed);

    Assert.Equal(OrderStatus.Completed, order.Status);
}
```

---

## TDD Anti-Patterns

| Anti-Pattern | Description | Fix |
|--------------|-------------|-----|
| The Liar | Test passes but doesn't verify meaningful behavior (e.g., `Assert.NotNull`) | Assert specific expected values |
| The Slow Poke | Unnecessary delays (`Task.Delay`, `Thread.Sleep`) | Use async properly, mock time |
| The Giant | Single test verifying multiple scenarios | Split into focused single-behavior tests |
| The Mockery | Over-mocking simple value objects/POCOs | Only mock external dependencies |
| The Inspector | Testing private implementation via reflection | Test public behavior only |

---

## TDD Workflow Checklist

- [ ] **Red:** Write failing test for ONE behavior
- [ ] **Verify:** Test fails for RIGHT reason
- [ ] **Green:** Write MINIMAL code to pass
- [ ] **Verify:** Test passes
- [ ] **Refactor:** Improve code quality
- [ ] **Verify:** Tests still pass
- [ ] **Repeat:** Next behavior

## Test Quality Checklist

- [ ] Clear test names (`MethodName_Scenario_ExpectedBehavior`)
- [ ] AAA or Given-When-Then structure
- [ ] Each test is independent
- [ ] Tests run fast (<100ms for unit tests)
- [ ] No logic in tests (no if/loops)
- [ ] Edge cases covered (null, empty, boundary values)
- [ ] Error paths tested
- [ ] Mocks used only for external dependencies
