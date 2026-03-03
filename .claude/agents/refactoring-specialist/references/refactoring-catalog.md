# Refactoring Catalog

**Source:** Martin Fowler's Refactoring, 2nd Edition
**Purpose:** Complete refactoring pattern library with before/after examples

---

## Refactoring Patterns

| Pattern | When to Use | Key Steps |
|---------|-------------|-----------|
| Extract Method | Method too long, duplicate code | Identify fragment, create method, replace with call, run tests |
| Extract Class | Class too large, multiple responsibilities | Identify cohesive group, create class, move members, run tests |
| Rename | Name doesn't reveal intent | Choose better name, find all references, update, run tests |
| Introduce Parameter Object | Long parameter lists | Create class for params, replace parameters, run tests |
| Replace Conditional with Polymorphism | Complex type-based conditionals | Create subclass per branch, move logic, run tests |
| Replace Magic Number with Constant | Unexplained numbers | Declare constant, replace number, run tests |
| Simplify Conditional Expression | Complex boolean logic | Extract to method, use early returns, run tests |

---

## Refactoring Process

### Step 1: Ensure Tests Exist
```bash
# Run tests before refactoring
npm test  # OR pytest OR dotnet test

# Verify 100% pass rate
# If tests don't exist, write them first
```

### Step 2: Apply Small Refactoring
```
# ONE refactoring pattern at a time
# Example: Extract Method
```

### Step 3: Run Tests
```bash
# After EACH refactoring step
npm test

# If tests fail:
#   - Revert changes
#   - Try smaller refactoring
# If tests pass:
#   - Commit changes
#   - Continue to next refactoring
```

### Step 4: Measure Improvement
```
# Check complexity
# Check duplication percentage
# Verify readability improved
```

---

## Common Code Smells

| Smell | Threshold | Detection | Refactoring |
|-------|-----------|-----------|-------------|
| Long Method | > 50 lines | Treelint function search + line range | Extract Method |
| God Object | > 500 lines | Treelint class search + line range | Extract Class |
| Duplicate Code | > 5% duplication | Grep pattern analysis | Extract Method, Pull Up Method |
| Long Parameter List | > 4 parameters | Treelint signature field | Introduce Parameter Object |
| Complex Conditional | Cyclomatic > 10 | Manual analysis | Decompose Conditional, Replace with Polymorphism |

---

## Complexity Reduction

**Cyclomatic Complexity Calculation:**
```
Complexity = 1 (base)
  + 1 for each if, elif, else
  + 1 for each case in switch
  + 1 for each loop (for, while)
  + 1 for each boolean operator (&&, ||)
  + 1 for each catch block

Target: < 10 per method
```

**Refactoring Strategy:**
- Extract complex conditionals to methods
- Replace nested loops with methods
- Simplify boolean logic
- Use early returns

---

## Error Handling

**When tests don't exist:**
- Report: "No tests found for [code]. Cannot safely refactor."
- Action: Suggest writing tests first
- Halt: Don't refactor without tests

**When tests fail after refactoring:**
- Report: "Tests failed after refactoring"
- Action: Revert changes immediately
- Try: Smaller refactoring step or different approach

**When complexity doesn't reduce:**
- Report: "Refactoring didn't reduce complexity"
- Action: Try different refactoring pattern
- Consider: Code may need redesign, not just refactoring

---

## References

- Refactoring by Martin Fowler
- Clean Code by Robert C. Martin
- Working Effectively with Legacy Code by Michael Feathers
