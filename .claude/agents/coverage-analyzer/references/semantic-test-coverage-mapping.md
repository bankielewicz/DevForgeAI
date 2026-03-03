# Semantic Test Coverage Mapping Reference

**Purpose:** Complete algorithms and edge case documentation for semantic test-to-source function correlation.

**Version:** 1.0 (STORY-372)

---

## Algorithm Overview

Semantic test coverage mapping correlates test functions with source functions using:
1. Treelint AST-aware function discovery
2. Naming convention pattern matching
3. Multi-file aggregation

---

## Source Function Discovery Algorithm

### Treelint Command

```bash
treelint search --type function --file ${source_file} --format json
```

### JSON Output Schema

```json
{
  "functions": [
    {
      "name": "process_order",
      "start_line": 10,
      "end_line": 25,
      "enclosing_class": "OrderService",
      "signature": "def process_order(self, order_id: int) -> Order"
    }
  ],
  "count": 5,
  "file": "src/orders/service.py"
}
```

### Zero Omission Guarantee

Every function defined in the source file MUST be enumerated. Treelint's AST parsing ensures:
- No functions omitted due to complex syntax
- Nested functions included with parent context
- Static methods, class methods, and instance methods all captured

---

## Test Function Discovery Algorithm

### Name Pattern Extraction Pipeline

Apply transformations in sequence until source function name extracted:

**Stage 1: Remove test_ prefix**
```
test_processOrder → processOrder
test_validate_input → validate_input
```

**Stage 2: Remove bracket suffixes (parameterized tests)**
```
test_validate[valid] → test_validate → validate
test_calculate[1,2,3] → test_calculate → calculate
```

**Stage 3: Strip Test class prefix**
```
TestUserService.test_create → UserService.create
TestOrderProcessor.test_validate → OrderProcessor.validate
```

**Stage 4: Normalize case**
```
ProcessOrder → processorder (for case-insensitive matching)
```

### Extraction Examples

| Test Function | Extracted Source | Matched Source |
|---------------|------------------|----------------|
| `test_processOrder` | `processOrder` | `processOrder` |
| `test_validate_input` | `validate_input` | `validate_input` |
| `TestUserService.test_create` | `UserService.create` | `UserService.create` |
| `test_handle_payment[visa]` | `handle_payment` | `handle_payment` |
| `test_edge_case_regression_789` | `edge_case_regression_789` | (unmapped) |

---

## Semantic Correlation Algorithm

### Matching Rules (Priority Order)

1. **Exact match:** Extracted name equals source function name
2. **Class-qualified match:** Extracted `Class.method` matches `Class.method`
3. **Case-insensitive fallback:** `processorder` matches `processOrder`
4. **Unmapped:** No match found, add to `unmapped_tests` array

### Classification Logic

```python
def classify_function(source_func, test_functions):
    matched = []
    for test in test_functions:
        extracted = extract_source_name(test.name)
        if matches(extracted, source_func.name):
            matched.append(test)

    return {
        "source_function": source_func.name,
        "matched_tests": matched,
        "status": "covered" if matched else "uncovered"
    }
```

### Output Structure

```json
{
  "correlations": [
    {
      "source_function": "processOrder",
      "matched_tests": ["test_processOrder"],
      "status": "covered"
    },
    {
      "source_function": "calculate_tax",
      "matched_tests": [],
      "status": "uncovered"
    }
  ],
  "unmapped_tests": ["test_regression_fix_789", "test_edge_case_abc"]
}
```

---

## Gap Report Generation

### Function-Level Gaps Schema

```json
{
  "function_level_gaps": [
    {
      "file": "src/orders/service.py",
      "function_name": "calculate_tax",
      "start_line": 45,
      "end_line": 67,
      "enclosing_class": "OrderService",
      "suggested_test": "test_calculate_tax",
      "priority": "high"
    }
  ]
}
```

### Suggested Test Generation

Based on function name and signature:
- `calculate_*` → `test_calculate_*`
- `validate_*` → `test_validate_*`
- `handle_*` → `test_handle_*`
- Private functions (`_helper`) → excluded by default

---

## Report Integration

### Function Coverage Metrics

```json
{
  "function_coverage": {
    "total_functions": 25,
    "covered_functions": 20,
    "uncovered_functions": 5,
    "coverage_percentage": 80.0,
    "uncovered_list": [
      {"name": "calculate_tax", "file": "service.py", "lines": [45, 67]},
      {"name": "validate_address", "file": "service.py", "lines": [70, 85]}
    ]
  }
}
```

### Recommendations Integration

Function gaps are referenced in the recommendations array:
- "Add test for uncovered function {name} in {file}"
- "Function-level coverage: {%} ({covered}/{total} functions covered)"

---

## Multi-File Aggregation

### When Multiple Test Files Exist

1. **Discovery:** Glob for test files matching source:
   - `tests/unit/test_{source_name}.py`
   - `tests/integration/test_{source_name}.py`
   - `tests/{source_name}_test.py`

2. **Aggregation:** Collect all test functions before correlation

3. **Coverage Rule:** Source function is covered if ANY test file contains matching test

### matched_tests with Originating File

```json
{
  "source_function": "validate_order",
  "matched_tests": [
    {"test": "test_validate_order", "file": "tests/unit/test_orders.py"},
    {"test": "test_validate_order_full", "file": "tests/integration/test_orders.py"}
  ],
  "status": "covered"
}
```

---

## Edge Cases

### Private Functions

Functions prefixed with `_` are:
- Excluded from uncovered report by default
- Included in covered list if explicitly tested (`test__validate_item`)

### Disambiguation

When multiple source files define same function name:
- Use test file naming: `test_order_service.py` → `order_service.py`
- Use class context: `TestOrderService` → `OrderService`
- If ambiguous: mark as `ambiguous_mapping`

### Nested Functions

Inner functions are tracked but:
- Attribution to parent function for coverage calculation
- Separate entries in gap report if uncovered

---

## Performance Considerations

- Single file mapping: < 1 second (excluding Treelint)
- Batch correlation (50 files): < 30 seconds
- Accuracy target: > 90% correct correlations

---

## References

- STORY-372: Implement Semantic Test Coverage Mapping via Treelint
- ADR-013: Treelint Integration for AST-Aware Code Search
- `.claude/agents/coverage-analyzer.md`: Parent subagent
