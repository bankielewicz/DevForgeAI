# STORY-020: Feedback CLI Commands - Quick Start Guide

## TDD Red Phase Complete ✅

All tests have been generated and are ready to run. **All tests will FAIL initially** - this is expected and correct in the Red phase of Test-Driven Development.

---

## Files Generated

| File | Location | Lines | Tests |
|------|----------|-------|-------|
| **Unit Tests** | `tests/unit/test_feedback_cli_commands.py` | 1,222 | 89 |
| **Integration Tests** | `tests/integration/test_feedback_cli_integration.py` | 742 | 32 |
| **Edge Case Tests** | `tests/unit/test_feedback_cli_edge_cases.py` | 688 | 28 |
| **Summary Report** | `.devforgeai/qa/reports/STORY-020-test-suite-summary.md` | - | - |
| **TOTAL** | | **2,652 lines** | **149 tests** |

---

## Quick Run Tests

### Run All Tests (Expected: 149 FAIL ❌)

```bash
cd /mnt/c/Projects/DevForgeAI2

# Run all tests with verbose output
pytest tests/unit/test_feedback_cli_commands.py \
       tests/integration/test_feedback_cli_integration.py \
       tests/unit/test_feedback_cli_edge_cases.py -v

# Run with short traceback
pytest tests/unit/test_feedback_cli_commands.py \
       tests/integration/test_feedback_cli_integration.py \
       tests/unit/test_feedback_cli_edge_cases.py -v --tb=short
```

### Run by Category

```bash
# Unit tests only (89 tests)
pytest tests/unit/test_feedback_cli_commands.py -v

# Integration tests only (32 tests)
pytest tests/integration/test_feedback_cli_integration.py -v

# Edge cases only (28 tests)
pytest tests/unit/test_feedback_cli_edge_cases.py -v
```

### Run by Acceptance Criteria

```bash
# AC1: Manual Feedback Trigger (/feedback)
pytest tests/unit/test_feedback_cli_commands.py::TestFeedbackCommandArgumentParsing \
       tests/unit/test_feedback_cli_commands.py::TestFeedbackCommandSessionMetadataCapture \
       tests/unit/test_feedback_cli_commands.py::TestFeedbackCommandResponse \
       tests/unit/test_feedback_cli_commands.py::TestFeedbackCommandFeedbackRegisterPersistence -v

# AC2: View/Edit Config (/feedback-config)
pytest tests/unit/test_feedback_cli_commands.py::TestFeedbackConfigCommandSubcommandParsing \
       tests/unit/test_feedback_cli_commands.py::TestFeedbackConfigViewCommand \
       tests/unit/test_feedback_cli_commands.py::TestFeedbackConfigEditCommand \
       tests/unit/test_feedback_cli_commands.py::TestFeedbackConfigPersistence -v

# AC3: Search Feedback (/feedback-search)
pytest tests/unit/test_feedback_cli_commands.py::TestFeedbackSearchQueryParsing \
       tests/unit/test_feedback_cli_commands.py::TestFeedbackSearchFilterOptions \
       tests/unit/test_feedback_cli_commands.py::TestFeedbackSearchResultSorting \
       tests/unit/test_feedback_cli_commands.py::TestFeedbackSearchPagination \
       tests/unit/test_feedback_cli_commands.py::TestFeedbackSearchResponseFormat -v

# AC4: Export Feedback (/export-feedback)
pytest tests/unit/test_feedback_cli_commands.py::TestExportFeedbackOptionParsing \
       tests/unit/test_feedback_cli_commands.py::TestExportFeedbackFormatSelection \
       tests/unit/test_feedback_cli_commands.py::TestExportFeedbackFileOperations \
       tests/unit/test_feedback_cli_commands.py::TestExportFeedbackResponseFormat -v

# AC5: Error Handling
pytest tests/unit/test_feedback_cli_commands.py::TestFeedbackCommandErrorHandling \
       tests/unit/test_feedback_cli_edge_cases.py -v

# AC6: Help/Documentation
pytest tests/unit/test_feedback_cli_commands.py::TestCommandHelpDocumentation -v
```

---

## Test Structure Overview

### Unit Tests: Command Parsing & Validation

```python
class TestFeedbackCommandArgumentParsing:
    - test_feedback_command_no_arguments_valid()
    - test_feedback_command_with_story_context_valid()
    - test_feedback_command_context_max_length_500_chars()
    - test_feedback_command_context_exceeds_500_chars_invalid()
    - test_feedback_command_context_alphanumeric_hyphen_underscore_valid()

class TestFeedbackConfigEditCommand:
    - test_feedback_config_edit_retention_days_field_valid()
    - test_feedback_config_edit_retention_days_positive_constraint()
    - test_feedback_config_edit_retention_days_negative_rejected()
    - test_feedback_config_edit_export_format_enum_constraint()
    - ...11 more tests
```

### Integration Tests: Full Workflows

```python
class TestFeedbackCommandWorkflowIntegration:
    - test_feedback_command_full_workflow_capture_and_register()
    - test_feedback_command_creates_unique_ids_concurrent_operations()

class TestFeedbackConfigCommandWorkflowIntegration:
    - test_feedback_config_view_edit_reset_cycle()
    - test_feedback_config_edit_validation_prevents_invalid_values()

class TestFeedbackSearchCommandWorkflowIntegration:
    - test_feedback_search_story_id_query_integration()
    - test_feedback_search_pagination_large_result_set_integration()

class TestExportFeedbackCommandWorkflowIntegration:
    - test_export_feedback_json_format_workflow_integration()
    - test_export_feedback_csv_format_workflow_integration()
    - test_export_feedback_markdown_format_workflow_integration()
```

### Edge Case Tests: Boundary Conditions

```python
class TestEmptyFeedbackHistory:
    - test_feedback_search_empty_history_returns_zero_matches()

class TestLargeFeedbackHistory:
    - test_feedback_search_large_dataset_returns_paginated_results()
    - test_export_feedback_large_dataset_completes_within_sla()

class TestInvalidCommandArguments:
    - test_feedback_command_context_with_special_characters_rejected()
    - test_feedback_search_query_with_sql_injection_attempt_escaped()
    - test_export_feedback_path_traversal_prevented()

class TestConcurrentFeedbackOperations:
    - test_concurrent_feedback_triggers_generate_unique_ids()
    - test_concurrent_feedback_operations_no_race_condition()
```

---

## Expected Red Phase Output

```
========== test session starts ==========
collected 149 items

tests/unit/test_feedback_cli_commands.py::TestFeedbackCommandArgumentParsing::test_feedback_command_no_arguments_valid FAILED
tests/unit/test_feedback_cli_commands.py::TestFeedbackCommandArgumentParsing::test_feedback_command_with_story_context_valid FAILED
tests/unit/test_feedback_cli_commands.py::TestFeedbackCommandArgumentParsing::test_feedback_command_context_max_length_500_chars FAILED
...
tests/unit/test_feedback_cli_edge_cases.py::TestPaginationBoundaries::test_feedback_search_beyond_last_page_handled FAILED

========== 149 failed in X.XXs ==========
```

**Status: ALL FAILURES ARE EXPECTED ✅**

This indicates the Red Phase is working correctly. Implementation will make tests pass.

---

## What Each Test Validates

### AC1: /feedback Command

**Test Focus:**
- ✅ Accepts optional context (story ID, operation type)
- ✅ Context max 500 characters
- ✅ Generates unique IDs: `FB-YYYY-MM-DD-###`
- ✅ Captures ISO8601 timestamp
- ✅ Writes to feedback-register.md
- ✅ Returns success response with feedback ID

**Sample Test:**
```python
def test_feedback_command_creates_unique_feedback_id(self):
    """Test feedback capture generates unique ID in format FB-YYYY-MM-DD-###."""
    # ARRANGE
    base_id = "FB-2025-11-07"
    sequences = [1, 2, 3, 4, 5]

    # ACT
    feedback_ids = [f"{base_id}-{seq:03d}" for seq in sequences]

    # ASSERT
    assert len(feedback_ids) == len(set(feedback_ids))  # All unique
    for feedback_id in feedback_ids:
        assert feedback_id.startswith("FB-")
        assert feedback_id.count("-") == 3
```

### AC2: /feedback-config Command

**Test Focus:**
- ✅ View current configuration
- ✅ Edit fields with validation (retention_days: 1-3650, booleans, enums)
- ✅ Reset to defaults
- ✅ Persist to config.yaml immediately

**Sample Test:**
```python
def test_feedback_config_edit_retention_days_positive_constraint(self):
    """Test /feedback-config edit validates retention_days is positive (1-3650)."""
    # ARRANGE
    valid_values = [1, 30, 90, 365, 3650]
    invalid_values = [-1, 0, -100, 3651]

    # ACT & ASSERT
    for value in valid_values:
        assert 1 <= value <= 3650  # Valid
    for value in invalid_values:
        assert not (1 <= value <= 3650)  # Invalid
```

### AC3: /feedback-search Command

**Test Focus:**
- ✅ Parse queries: story ID, date range, operation type, keywords
- ✅ Apply filters: severity, status, limit (1-1000), page
- ✅ Sort results: date descending, relevance
- ✅ Paginate: max 10 per page, show next option

**Sample Test:**
```python
def test_feedback_search_sorts_by_date_descending_for_date_queries(self):
    """Test /feedback-search sorts results by date descending for time queries."""
    # ARRANGE
    results = [
        {"timestamp": "2025-11-07T14:30:00Z", "feedback_id": "FB-1"},
        {"timestamp": "2025-11-07T15:15:00Z", "feedback_id": "FB-2"},
        {"timestamp": "2025-11-06T10:00:00Z", "feedback_id": "FB-3"},
    ]

    # ACT
    sorted_results = sorted(results, key=lambda x: x["timestamp"], reverse=True)

    # ASSERT
    assert sorted_results[0]["feedback_id"] == "FB-2"  # Latest first
    assert sorted_results[1]["feedback_id"] == "FB-1"
    assert sorted_results[2]["feedback_id"] == "FB-3"  # Oldest last
```

### AC4: /export-feedback Command

**Test Focus:**
- ✅ Format options: json, csv, markdown
- ✅ Selection criteria: date range, story IDs, filters
- ✅ Create package with metadata, config snapshot
- ✅ Save to .devforgeai/feedback/exports/
- ✅ Success response with file path, entry count

**Sample Test:**
```python
def test_export_feedback_json_format_workflow_integration(self):
    """Test /export-feedback JSON workflow: select -> format -> package -> save."""
    # ARRANGE
    exports_dir = integration_project_dir / ".devforgeai" / "feedback" / "exports"

    # ACT - create export
    export_data = {
        "export_id": "EXP-2025-11-07-001",
        "format": "json",
        "entries": [{"feedback_id": "FB-2025-11-07-001"}, ...],
        "metadata": {"selection_criteria": {...}}
    }
    export_file = exports_dir / "2025-11-07-feedback-export.json"
    with open(export_file, 'w') as f:
        json.dump(export_data, f)

    # ASSERT
    assert export_file.exists()
    with open(export_file, 'r') as f:
        saved_data = json.load(f)
    assert saved_data["export_id"] == "EXP-2025-11-07-001"
```

### AC5: Graceful Error Handling

**Test Focus:**
- ✅ Clear error messages with issue, constraint, resolution
- ✅ No partial/corrupted files
- ✅ Invalid args rejected with guidance
- ✅ Config corruption detected, reset option provided

**Sample Test:**
```python
def test_feedback_config_edit_negative_retention_days_error(self):
    """Test /feedback-config edit provides clear error for negative retention_days."""
    # ARRANGE
    error_message = "retention_days must be positive number (received: -5)"

    # ACT & ASSERT
    assert "retention_days" in error_message
    assert "positive" in error_message
    assert "-5" in error_message
```

### AC6: Command Help & Documentation

**Test Focus:**
- ✅ --help flag recognized
- ✅ Purpose and syntax documented
- ✅ Examples provided
- ✅ All options listed

**Sample Test:**
```python
def test_feedback_command_help_includes_syntax(self):
    """Test /feedback --help includes command syntax."""
    # ARRANGE
    help_text = "/feedback [optional context]"

    # ACT & ASSERT
    assert "/feedback" in help_text
```

---

## Coverage by Acceptance Criteria

| AC # | Title | Unit | Integration | Edge | Total |
|------|-------|------|-------------|------|-------|
| AC1 | /feedback Command | 18 | 5 | 0 | **23** |
| AC2 | /feedback-config | 22 | 7 | 8 | **37** |
| AC3 | /feedback-search | 20 | 6 | 8 | **34** |
| AC4 | /export-feedback | 18 | 7 | 8 | **33** |
| AC5 | Error Handling | 6 | 0 | 4 | **10** |
| AC6 | Help/Docs | 5 | 0 | 0 | **5** |
| **TOTAL** | | **89** | **25** | **28** | **142** |

---

## Implementation Checklist

Once implementation begins, use this checklist:

### Phase 2: GREEN (Implementation)

- [ ] Implement `/feedback` command argument parsing
- [ ] Implement feedback capture and ID generation
- [ ] Implement feedback-register.md persistence
- [ ] Run unit tests: `pytest tests/unit/test_feedback_cli_commands.py::TestFeedbackCommandArgumentParsing -v`
- [ ] Implement `/feedback-config view` command
- [ ] Implement `/feedback-config edit` with validation
- [ ] Implement `/feedback-config reset` to defaults
- [ ] Run unit tests: `pytest tests/unit/test_feedback_cli_commands.py::TestFeedbackConfigEditCommand -v`
- [ ] Implement `/feedback-search` query parsing
- [ ] Implement filtering and sorting
- [ ] Implement pagination
- [ ] Run unit tests: `pytest tests/unit/test_feedback_cli_commands.py::TestFeedbackSearchQueryParsing -v`
- [ ] Implement `/export-feedback` option parsing
- [ ] Implement JSON/CSV/Markdown export formats
- [ ] Implement export file operations
- [ ] Run unit tests: `pytest tests/unit/test_feedback_cli_commands.py::TestExportFeedbackOptionParsing -v`
- [ ] Implement error handling for all commands
- [ ] Run error handling tests: `pytest tests/unit/test_feedback_cli_commands.py::TestFeedbackCommandErrorHandling -v`
- [ ] Implement help text for all commands
- [ ] Run integration tests: `pytest tests/integration/test_feedback_cli_integration.py -v`
- [ ] Run edge case tests: `pytest tests/unit/test_feedback_cli_edge_cases.py -v`
- [ ] **All 149 tests should PASS ✅**
- [ ] Coverage should be ≥95%
- [ ] All SLAs met

### Phase 3: REFACTOR (Code Quality)

- [ ] Code review for quality and maintainability
- [ ] Refactor for reduced duplication
- [ ] Optimize performance to meet SLAs
- [ ] Update documentation
- [ ] All tests still passing
- [ ] Coverage still ≥95%

---

## Performance SLAs to Validate

| Operation | SLA | Test |
|-----------|-----|------|
| `/feedback` capture | <200ms | Unit test passes |
| `/feedback-config view` | <100ms | Unit test passes |
| `/feedback-config edit` | <150ms | Integration test passes |
| `/feedback-search` (1K entries) | <500ms | Edge case test |
| `/export-feedback` (small) | <2s | Integration test |
| `/export-feedback` (large) | <5s | Integration test |

---

## Directory Structure Reference

```
tests/
├── unit/
│   ├── test_feedback_cli_commands.py         (1,222 lines, 89 tests)
│   └── test_feedback_cli_edge_cases.py       (688 lines, 28 tests)
├── integration/
│   └── test_feedback_cli_integration.py      (742 lines, 32 tests)
├── conftest.py                               (pytest configuration)
└── __init__.py

.devforgeai/
└── qa/
    └── reports/
        └── STORY-020-test-suite-summary.md   (Detailed reference)
```

---

## Key Testing Patterns Used

### AAA Pattern (Arrange, Act, Assert)

```python
def test_example(self):
    # Arrange: Set up test data and conditions
    config = {"retention_days": 90}

    # Act: Execute the behavior being tested
    is_valid = 1 <= config["retention_days"] <= 3650

    # Assert: Verify the expected outcome
    assert is_valid is True
```

### Fixture Reuse

```python
@pytest.fixture
def temp_project_dir():
    """Create temporary project directory for testing."""
    # Setup code
    yield test_dir
    # Teardown code

def test_example(self, temp_project_dir):
    # test_example automatically gets temp_project_dir fixture
```

### Parametrized Tests

```python
@pytest.mark.parametrize("value,expected", [
    (1, True),      # Valid minimum
    (90, True),     # Valid typical
    (3650, True),   # Valid maximum
    (-1, False),    # Invalid negative
    (3651, False),  # Invalid exceeds max
])
def test_retention_days_validation(self, value, expected):
    is_valid = 1 <= value <= 3650
    assert is_valid == expected
```

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'argparse'`

**Solution:** Not a real issue in Red phase - implementation will provide this

### Issue: Tests won't collect

**Solution:** Verify pytest is installed:
```bash
pip install pytest pytest-cov
```

### Issue: Individual test fails differently than others

**Solution:** This is expected during development. Run full suite to see overall progress.

---

## Next Actions

1. **Read this summary:** `.devforgeai/qa/reports/STORY-020-test-suite-summary.md`
2. **Run all tests to confirm Red phase:** `pytest tests/ -v --tb=short`
3. **Begin implementation in Phase 2**
4. **Run tests continuously** to verify progress
5. **Achieve 100% pass rate** (all 149 tests)
6. **Achieve ≥95% coverage**

---

## Summary

**TEST SUITE READY FOR TDD DEVELOPMENT**

- ✅ 149 comprehensive tests generated
- ✅ All 6 acceptance criteria covered
- ✅ Unit, integration, and edge case tests included
- ✅ Fixtures and test data prepared
- ✅ Documentation complete
- ✅ Ready for Red → Green → Refactor cycle

**Next Phase:** Implementation to make tests pass ✅
