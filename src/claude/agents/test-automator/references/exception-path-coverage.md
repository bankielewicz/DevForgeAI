# Exception Path Coverage (STORY-264)

Reference documentation for test-automator subagent. Contains the 4-category exception path coverage framework.

---

## Purpose

Generate comprehensive test coverage for exception handling paths, targeting the 4 categories of code paths most commonly missed during test generation.

---

## 4-Category Coverage Framework

Every method/function should have test coverage in these 4 categories:

| Category | Description | Test Pattern |
|----------|-------------|--------------|
| **HAPPY_PATH** | Normal execution flow, expected inputs | `test_*_success_*`, `test_*_valid_*` |
| **ERROR_PATHS** | Error return conditions (False/None/errors) | `test_*_error_*`, `test_*_invalid_*` |
| **EXCEPTION_HANDLERS** | Try/except/catch blocks | `test_*_exception_*`, `test_*_raises_*` |
| **BOUNDARY_CONDITIONS** | Edge cases, min/max, empty collections | `test_*_boundary_*`, `test_*_edge_*` |

---

## Coverage Checklist Template

When analyzing a method/function, generate this checklist:

```
Coverage Checklist for {method_name}:
- [ ] Happy path (normal execution flow)
- [ ] Error return paths (error conditions)
- [ ] Exception handlers (except/catch blocks)
- [ ] Boundary conditions (edge cases)
```

**Checklist Generation:**
1. Parse the method for all code paths
2. Identify which categories have existing test coverage
3. Generate checklist showing covered/uncovered categories
4. Report: "Coverage: 3/4 categories - missing: Boundaries"

---

## Identify Missing Exception Tests

### Workflow for analyzing existing test suite against checklist:

```python
def analyze_test_coverage_against_checklist(method, existing_tests):
    """
    Analyze existing test suite to identify which 4 categories lack coverage.

    Returns: List of missing categories (e.g., ["EXCEPTION_HANDLERS", "BOUNDARY_CONDITIONS"])
    """
    coverage_map = {
        "HAPPY_PATH": False,
        "ERROR_PATHS": False,
        "EXCEPTION_HANDLERS": False,
        "BOUNDARY_CONDITIONS": False
    }

    # Scan existing tests for patterns
    for test in existing_tests:
        if matches_happy_path_pattern(test):
            coverage_map["HAPPY_PATH"] = True
        if matches_error_path_pattern(test):
            coverage_map["ERROR_PATHS"] = True
        if matches_exception_pattern(test):
            coverage_map["EXCEPTION_HANDLERS"] = True
        if matches_boundary_pattern(test):
            coverage_map["BOUNDARY_CONDITIONS"] = True

    # Identify gaps - compare tests against checklist to match each category
    missing = [cat for cat, covered in coverage_map.items() if not covered]
    return missing
```

### Compare Tests Against Checklist Workflow:

1. Load existing test files for method
2. Match test names against category patterns (happy, error, exception, boundary)
3. Compare each test against the 4-category checklist
4. Mark categories as covered when matching tests found
5. Report remaining gaps

### Output Format:

```
Analysis Result:
  Method: process_user_input()
  Existing tests: 5
  Coverage: 2/4 categories
  Covered: Happy | Errors
  missing: Exceptions | Boundaries
```

---

## Generate Tests for Missing Categories

### Purpose

Generate targeted tests specifically for each category that lacks coverage.

### Category-specific test generation guidance:

- This guidance helps generate tests targeting each category that lacks coverage
- Each category has distinct patterns and triggering strategies
- Test names should indicate category being tested (see table below)

### FOR EACH missing category, generate targeted tests:

```python
def generate_tests_for_missing_categories(method, missing_categories):
    """
    Generate tests specifically targeting each missing category.
    Uses descriptive test names that indicate the category being tested.
    """
    generated_tests = []

    for category in missing_categories:
        if category == "HAPPY_PATH":
            tests = generate_happy_path_tests(method)
            # Names: test_{method}_success_*, test_{method}_valid_*

        elif category == "ERROR_PATHS":
            tests = generate_error_path_tests(method)
            # Names: test_{method}_error_*, test_{method}_returns_false_*

        elif category == "EXCEPTION_HANDLERS":
            tests = generate_exception_tests(method)
            # Names: test_{method}_exception_*, test_{method}_raises_*

        elif category == "BOUNDARY_CONDITIONS":
            tests = generate_boundary_tests(method)
            # Names: test_{method}_boundary_*, test_{method}_edge_*

        generated_tests.extend(tests)

    return generated_tests
```

### Test Naming Conventions (Descriptive Names):

Each generated test covers its assigned category explicitly via naming convention:

| Category | Naming Pattern | Example |
|----------|---------------|---------|
| Exception handlers | `test_*_exception_*`, `test_*_raises_*` | `test_process_input_exception_invalid_format` |
| Error paths | `test_*_error_*`, `test_*_returns_none` | `test_validate_user_error_missing_email` |
| Boundary conditions | `test_*_boundary_*`, `test_*_edge_*` | `test_paginate_boundary_zero_items` |

**Test-to-Category Mapping:** The naming convention maps each test to its category for traceability.

---

## Exception Block Detection

### Purpose

Identify all try/except (Python) or try/catch (JS/TS) blocks in source code and generate tests that trigger each exception handler.

### Python Exception Detection (try/except)

**COMP-001:** Parse try/except blocks and analyze exception handlers to identify all exception paths.

```python
# COMP-001: Parse method/function for try/except blocks
def detect_exception_blocks_python(source_code):
    """
    Identify all try/except blocks and their exception types.

    Returns list of:
    - Exception type (ValueError, TypeError, KeyError, etc.)
    - Line numbers
    - Handler code
    """
    import ast

    tree = ast.parse(source_code)
    exception_blocks = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Try):
            for handler in node.handlers:
                exception_type = handler.type.id if handler.type else "Exception"
                exception_blocks.append({
                    "type": exception_type,
                    "lineno": handler.lineno,
                    "handler": ast.unparse(handler)
                })

    return exception_blocks
```

### JavaScript/TypeScript Exception Detection (try/catch)

```javascript
// Detect try/catch blocks in JS/TS code
function detectExceptionBlocksJS(sourceCode) {
    // Pattern: try { ... } catch (error) { ... }
    const tryCatchPattern = /try\s*\{[\s\S]*?\}\s*catch\s*\((\w+)\)\s*\{[\s\S]*?\}/g;
    const matches = [...sourceCode.matchAll(tryCatchPattern)];

    return matches.map(match => ({
        type: "Error",  // JS uses generic Error
        errorVar: match[1],
        block: match[0]
    }));
}
```

### COMP-002: Exception Type to Test Mapping

Map each identified exception type to test generation targets:

```python
EXCEPTION_TEST_MAP = {
    "ValueError": {
        "trigger": "invalid argument value",
        "test_name": "test_{method}_raises_value_error",
        "inputs": ["negative values", "out of range", "wrong type coerced"]
    },
    "TypeError": {
        "trigger": "wrong argument type",
        "test_name": "test_{method}_raises_type_error",
        "inputs": ["None where int expected", "string where list expected"]
    },
    "KeyError": {
        "trigger": "missing dictionary key",
        "test_name": "test_{method}_raises_key_error",
        "inputs": ["missing required key", "typo in key name"]
    },
    "FileNotFoundError": {
        "trigger": "file does not exist",
        "test_name": "test_{method}_raises_file_not_found",
        "inputs": ["non-existent path", "deleted file"]
    }
}
```

### COMP-004: Generate Exception Trigger Tests

```python
def generate_exception_trigger_tests(method, exception_blocks):
    """
    Generate tests that call method with arguments to trigger each identified exception.

    Example: If method has `except ValueError`, generate test that passes
    invalid value to trigger that handler.
    """
    tests = []

    for block in exception_blocks:
        exception_type = block["type"]
        mapping = EXCEPTION_TEST_MAP.get(exception_type, {})

        test = f'''
def test_{method.name}_raises_{exception_type.lower()}():
    """
    Test: {method.name} handles {exception_type} correctly.
    Trigger: {mapping.get("trigger", "exception condition")}
    """
    # Arrange
    invalid_input = {mapping.get("inputs", ["invalid"])[0]!r}

    # Act & Assert
    with pytest.raises({exception_type}):
        {method.name}(invalid_input)
'''
        tests.append(test)

    return tests
```

### Multiple Exception Handlers

When a method has multiple except blocks (e.g., 3 different exception types), generate a test for EACH:

```python
# Method with 3 except blocks:
# except ValueError: ...
# except TypeError: ...
# except KeyError: ...

# Generated tests:
def test_process_data_raises_value_error(): ...
def test_process_data_raises_type_error(): ...
def test_process_data_raises_key_error(): ...
```

### Finally Block Testing

Also detect `finally` blocks and verify cleanup code executes:

```python
def test_method_finally_cleanup_executes():
    """Verify finally block executes even on exception."""
    cleanup_called = False

    def track_cleanup():
        nonlocal cleanup_called
        cleanup_called = True

    # Inject cleanup tracker
    with pytest.raises(SomeException):
        method_with_finally(callback=track_cleanup)

    assert cleanup_called, "Finally block cleanup should always execute"
```

---

## Boundary Condition Identification

### Purpose

Identify boundary conditions in code with numeric parameters, loop conditions, or collection operations, and generate tests for edge cases.

### COMP-003: Numeric Boundary Identification

```python
def identify_boundary_conditions(method):
    """
    Identify boundary conditions for numeric code.

    For function with range(10):
    - Identifies 0 (min), 9 (max valid), 10 (first invalid) as boundary tests

    For function with if x > 0:
    - Identifies -1, 0, 1 as boundary tests
    """
    boundaries = []

    # Detect range() calls
    for range_call in find_range_calls(method):
        start, stop = parse_range_args(range_call)
        boundaries.extend([
            {"type": "min", "value": start, "description": "minimum valid index"},
            {"type": "max_valid", "value": stop - 1, "description": "maximum valid index"},
            {"type": "first_invalid", "value": stop, "description": "first out-of-range value"}
        ])

    # Detect comparison operators
    for comparison in find_comparisons(method):
        operator, threshold = parse_comparison(comparison)
        if operator == ">":
            boundaries.extend([
                {"type": "below", "value": threshold - 1},
                {"type": "at", "value": threshold},
                {"type": "above", "value": threshold + 1}
            ])

    return boundaries
```

### Collection Boundary Conditions (BR-003)

**BR-003 specifies collection boundaries: empty, single element, and max size testing.**

For functions iterating over collections, identify these boundary tests:

```python
# BR-003: Boundary conditions for collections include:
# - empty: []
# - single element: [1]
# - at max size: [1, 2, ..., N]

COLLECTION_BOUNDARIES = [
    {"type": "empty", "value": [], "description": "empty collection"},
    {"type": "single", "value": [1], "description": "single element"},
    {"type": "max_size", "value": "list of N elements", "description": "at maximum size"}
]
```

### Loop Boundary Identification

**Range boundary analysis:** For loops with `range(N)`, identify loop boundary values for testing.

For loops with `range(N)`, identify these test values:

| Loop | Test Values | Description |
|------|-------------|-------------|
| `range(10)` | 0, 9, 10 | min, max valid, first invalid |
| `range(1, 100)` | 1, 99, 0, 100 | min, max, below min, above max |
| `while i < limit` | limit-1, limit, limit+1 | approaching, at, past boundary |

### Parameterized Boundary Tests

Generate parameterized tests for comprehensive boundary coverage:

```python
@pytest.mark.parametrize("index,should_succeed", [
    (0, True),    # min valid (boundary)
    (9, True),    # max valid (boundary)
    (10, False),  # first invalid (off-by-one)
    (-1, False),  # below min (edge case)
])
def test_access_item_boundary_conditions(index, should_succeed):
    """Boundary test: array access with range(10)."""
    items = list(range(10))

    if should_succeed:
        result = access_item(items, index)
        assert result == items[index]
    else:
        with pytest.raises(IndexError):
            access_item(items, index)
```
