# Remediation Mode (QA-Dev Integration)

Reference documentation for test-automator subagent. Contains workflow for MODE:REMEDIATION test generation from gaps.json.

---

## Purpose

Generate targeted tests when invoked with coverage gaps from gaps.json after QA failure.

**When active:** `/dev` runs after QA failure and gaps.json exists.

---

## Detecting Remediation Mode

When invoked, check if prompt contains `MODE: REMEDIATION`:

```python
IF prompt contains "MODE: REMEDIATION":
    # Remediation mode - targeted test generation
    $REMEDIATION_MODE = true

    # Parse coverage_gaps from prompt JSON
    coverage_gaps = parse_json(prompt.coverage_gaps)

    # Focus ONLY on files in coverage_gaps array
    target_files = [gap.file for gap in coverage_gaps]
    suggested_tests = [gap.suggested_tests for gap in coverage_gaps]

ELSE:
    # Normal mode - full test generation from AC
    $REMEDIATION_MODE = false
```

---

## Remediation Mode Workflow

### 1. Parse Coverage Gaps

```python
FOR EACH gap in coverage_gaps:
    file_path = gap.file
    current_coverage = gap.current_coverage
    target_coverage = gap.target_coverage
    gap_percentage = gap.gap_percentage
    uncovered_lines = gap.uncovered_line_count
    suggestions = gap.suggested_tests
```

### 2. Convert Suggestions to Test Cases

The `suggested_tests` array contains natural language descriptions:

```python
["Test rollback on corrupted backup file",
 "Test rollback when target directory is read-only",
 "Test partial rollback recovery after interruption"]
```

Convert each to test function:

```python
def test_rollback_corrupted_backup():
    """
    Scenario: Rollback handles corrupted backup gracefully
    Given: A backup file that is corrupted (invalid format/truncated)
    When: rollback() is called
    Then: Should raise BackupCorruptedError with clear message
    """
    # Arrange
    corrupted_backup = create_corrupted_backup()

    # Act & Assert
    with pytest.raises(BackupCorruptedError):
        rollback(corrupted_backup)
```

### 3. Read Target Files

```python
FOR EACH file in target_files:
    Read(file_path=file)

    # Analyze code structure
    - Functions/methods
    - Error handling paths
    - Edge cases
    - Conditional branches
```

### 4. Generate Targeted Tests

```python
FOR EACH suggestion in suggestions:
    # Parse the scenario from suggestion text
    scenario = extract_scenario(suggestion)

    # Generate test following AAA pattern
    test_code = generate_test(
        scenario=scenario,
        file=file_path,
        test_framework=$TEST_FRAMEWORK
    )

    # Write test to appropriate test file
    Write(file_path=test_file_path, content=test_code)
```

### 5. Report Coverage Improvement

```json
{
  "remediation_mode": true,
  "gaps_addressed": 3,
  "tests_generated": 12,
  "files_created": ["tests/test_rollback_edge_cases.py"],
  "suggestions_converted": [
    {
      "suggestion": "Test rollback on corrupted backup file",
      "test_function": "test_rollback_corrupted_backup",
      "file": "tests/test_rollback_edge_cases.py"
    }
  ],
  "expected_coverage_improvement": {
    "installer/rollback.py": "+25%",
    "installer/migration_discovery.py": "+2%"
  }
}
```

---

## Key Differences from Normal Mode

| Aspect | Normal Mode | Remediation Mode |
|--------|-------------|------------------|
| Scope | Full story AC + Tech Spec | Coverage gaps only |
| Source | Story file | gaps.json |
| Tests | All AC-derived tests | Suggested tests from QA |
| Target | All story files | Only gap.file entries |
| Output | Full test suite | Targeted test additions |

---

## Example Remediation Prompt

```
Generate tests to close coverage gaps for STORY-078.

MODE: REMEDIATION (targeted, not full coverage)

COVERAGE GAPS TO ADDRESS:
[
  {
    "file": "installer/rollback.py",
    "layer": "business_logic",
    "current_coverage": 63.6,
    "target_coverage": 95.0,
    "gap_percentage": 31.4,
    "uncovered_line_count": 56,
    "suggested_tests": [
      "Test rollback on corrupted backup file",
      "Test rollback when target directory is read-only",
      "Test partial rollback recovery after interruption",
      "Test rollback error handling for missing backup"
    ]
  }
]

INSTRUCTIONS:
1. For EACH file in coverage_gaps:
   - Analyze the suggested_tests descriptions
   - Generate specific test cases for each suggestion
   - Target the uncovered scenarios
2. Test naming: test_{scenario_from_suggestion}
3. Focus on error handling paths and edge cases
4. Do NOT generate tests for files not in coverage_gaps
```

---

## Gap File Schema (gaps.json)

```json
{
  "story_id": "STORY-078",
  "timestamp": "2026-01-15T10:30:00Z",
  "coverage_gaps": [
    {
      "file": "string - path to source file",
      "layer": "business_logic | application | infrastructure",
      "current_coverage": "number - percentage",
      "target_coverage": "number - threshold for layer",
      "gap_percentage": "number - difference",
      "uncovered_line_count": "number - lines not covered",
      "suggested_tests": ["array of natural language test descriptions"]
    }
  ]
}
```

---

## Validation

After generating remediation tests:

1. **Verify tests target correct files** - All tests should be for files in coverage_gaps
2. **Verify suggestions converted** - Each suggested_test has a corresponding test function
3. **Run tests** - Confirm tests execute (may fail initially - TDD Red phase)
4. **Report coverage delta** - Estimate improvement from new tests
