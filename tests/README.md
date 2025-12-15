# STORY-015 Comprehensive Test Suite

**Story:** STORY-015 - Comprehensive Testing for STORY-014 DoD Template
**Status:** Implementation Complete
**Test Coverage Target:** ≥95% for template/story edit operations
**Total Tests:** 18 (3 unit + 9 unit + 3 unit + 3 unit + 3 integration + 1 E2E)

---

## Test Suite Overview

This test suite validates the Definition of Done (DoD) template modifications from STORY-014. The suite is organized into three tiers following the test pyramid pattern:

### Test Tier Distribution

- **Unit Tests (14 tests, 78%)** - Validate individual operations
  - 3 tests: Template DoD insertion
  - 9 tests: Story DoD insertion (3 per story: STORY-027, 028, 029)
  - 3 tests: YAML frontmatter validation
  - 3 tests: Section ordering validation

- **Integration Tests (3 tests, 17%)** - Validate combined workflows
  - 1 test: Full update workflow (template + 3 stories + validation)
  - 1 test: Template structure matching (vs STORY-007 reference)
  - 1 test: Story consistency (all 3 stories DoD identical)

- **E2E Tests (1 test, 5%)** - Validate real-world usage
  - 1 test: Future story creation with auto-populated DoD

---

## Test Files and Locations

### Unit Tests

#### `tests/unit/test_template_dod_insertion.py` (5 tests)

**Purpose:** Validate template DoD section is correctly inserted

**Tests:**
1. `test_dod_section_placement` - DoD after Edge Cases, before Notes
2. `test_dod_subsections_present` - All 4 subsections present in correct order
3. `test_template_variables_preserved` - Template variables intact (no corruption)
4. `test_dod_section_has_checklist_items` - Checkboxes in correct format
5. `test_dod_section_not_empty` - DoD section has meaningful content

**Acceptance Criteria Covered:** AC1

---

#### `tests/unit/test_story_dod_insertion.py` (9 tests)

**Purpose:** Validate DoD insertion in STORY-027, 028, 029

**Tests:**
1. `test_story_027_dod_section_placement` - Placement validation
2. `test_story_028_dod_section_placement` - Placement validation
3. `test_story_029_dod_section_placement` - Placement validation
4. `test_story_027_dod_subsections_present` - Subsection validation
5. `test_story_028_dod_subsections_present` - Subsection validation
6. `test_story_029_dod_subsections_present` - Subsection validation
7. `test_story_027_yaml_frontmatter_unchanged` - YAML integrity
8. `test_story_028_yaml_frontmatter_unchanged` - YAML integrity
9. `test_story_029_yaml_frontmatter_unchanged` - YAML integrity

**Acceptance Criteria Covered:** AC2

---

#### `tests/unit/test_yaml_frontmatter_validation.py` (3 tests)

**Purpose:** Validate YAML frontmatter syntax and required fields

**Tests:**
1. `test_story_027_yaml_valid_syntax` - YAML parses without errors
2. `test_story_028_yaml_valid_syntax` - YAML parses without errors
3. `test_story_029_yaml_valid_syntax` - YAML parses without errors
4. `test_story_027_required_fields` - All required fields present and non-null
5. `test_story_028_required_fields` - All required fields present and non-null
6. `test_story_029_required_fields` - All required fields present and non-null

**Acceptance Criteria Covered:** AC3

---

#### `tests/unit/test_section_ordering_validation.py` (3 tests)

**Purpose:** Validate section ordering in template and stories

**Tests:**
1. `test_template_section_ordering` - Template sections in canonical order
2. `test_story_027_section_ordering` - STORY-027 sections in canonical order
3. `test_story_028_section_ordering` - STORY-028 sections in canonical order
4. `test_story_029_section_ordering` - STORY-029 sections in canonical order
5. `test_dod_section_has_correct_header_format` - Exact header format validation

**Acceptance Criteria Covered:** AC3

---

### Integration Tests

#### `tests/integration/test_full_update_workflow.py` (2 tests)

**Purpose:** Validate complete workflow (template + 3 stories + validation)

**Tests:**
1. `test_full_update_workflow` - All files exist, have DoD, formatted correctly, <30s
2. `test_workflow_consistency_across_stories` - Identical subsection structure

**Acceptance Criteria Covered:** AC4 (first part)

**Performance Requirements:**
- Full workflow executes in <30 seconds
- Individual file reads/writes <1 second

---

#### `tests/integration/test_template_structure_match.py` (2 tests)

**Purpose:** Validate template structure matches STORY-007 reference

**Tests:**
1. `test_template_contains_all_canonical_sections` - All 7 canonical sections present
2. `test_template_sections_in_canonical_order` - Sections in correct order
3. `test_template_dod_subsections_correct` - All 4 DoD subsections present
4. `test_template_dod_subsections_in_canonical_order` - DoD subsections in order
5. `test_reference_story_matches_template_structure` - STORY-007 validates template

**Acceptance Criteria Covered:** AC4 (second part)

---

#### `tests/integration/test_story_consistency.py` (4 tests)

**Purpose:** Validate all 3 stories have identical DoD structure

**Tests:**
1. `test_all_stories_have_dod_sections` - All 3 stories have DoD
2. `test_all_stories_have_canonical_subsections` - All have 4 subsections
3. `test_all_stories_have_consistent_checkbox_format` - Format consistency
4. `test_all_stories_have_minimum_checkboxes` - Minimum 1 per subsection
5. `test_all_stories_have_similar_checkbox_counts` - Counts within 2 of each other
6. `test_subsection_order_identical_across_stories` - Identical ordering

**Acceptance Criteria Covered:** AC4 (third part)

---

### E2E Tests

#### `tests/e2e/test_future_story_creation.py` (1 test with 7 assertions)

**Purpose:** Validate future stories auto-populate DoD from template

**Tests:**
1. `test_new_story_includes_dod_section` - DoD section present
2. `test_dod_section_positioning` - DoD positioned correctly
3. `test_dod_subsections_present` - All 4 subsections with checkboxes
4. `test_template_variables_replaced` - No unreplaced variables
5. `test_story_has_valid_yaml_frontmatter` - YAML valid
6. `test_story_completeness` - All sections present with content
7. `test_cleanup_successful` - Cleanup successful

**Acceptance Criteria Covered:** AC5

**Test Approach:**
- Uses temporary directory for test story
- Instantiates template with test values
- Validates all assertions
- Cleanup automatic via pytest fixture

---

## Running the Tests

### Run All Tests

```bash
# Run full test suite with coverage
pytest tests/ -v

# Run with coverage report (HTML + terminal)
pytest tests/ --cov=.claude/skills/devforgeai-story-creation --cov-report=html

# Run with timing information
pytest tests/ --durations=0
```

### Run by Category

```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# E2E tests only
pytest tests/e2e/ -v -m e2e
```

### Run Specific Test

```bash
# Run specific test file
pytest tests/unit/test_template_dod_insertion.py -v

# Run specific test function
pytest tests/unit/test_template_dod_insertion.py::TestTemplateDoD_Insertion::test_dod_section_placement -v
```

### Run with Markers

```bash
# Run only unit tests (not integration/e2e)
pytest tests/unit/ -m unit -v

# Run deterministic tests (no flaky tests)
pytest -m deterministic -v

# Skip slow tests
pytest -m "not slow" -v
```

### Performance Testing

```bash
# Check test execution time
pytest tests/ --durations=0

# Expect: Full suite <120 seconds, individual tests <2 seconds
```

---

## Test Configuration

### pytest.ini

**Location:** `tests/pytest.ini`

**Key Settings:**
- `testpaths = tests` - Test discovery path
- `python_files = test_*.py` - Test file pattern
- `addopts = --cov --cov-report=html --cov-report=term-missing` - Coverage settings
- `fail_under = 95` - Minimum coverage threshold (95%)

**Coverage Report Output:**
- Terminal: `--cov-report=term-missing` (shows uncovered lines)
- HTML: `.devforgeai/qa/coverage/STORY-015-coverage-report/` (detailed report)
- JSON: `.devforgeai/qa/coverage/STORY-015-coverage.json` (machine-readable)

---

## Acceptance Criteria Traceability

| AC # | Title | Test File | Test Count | Pass Criteria |
|------|-------|-----------|------------|---------------|
| AC1 | Template DoD Section Insertion | test_template_dod_insertion.py | 5 | 5/5 PASS |
| AC2 | Story DoD Section Insertion | test_story_dod_insertion.py | 9 | 9/9 PASS |
| AC3 | YAML & Section Ordering | test_yaml_*.py, test_section_*.py | 6 | 6/6 PASS |
| AC4 | Integration Tests | test_full_update_*.py, test_*_consistency.py | 3 | 3/3 PASS |
| AC5 | E2E Test | test_future_story_creation.py | 1 | 1/1 PASS |
| AC6 | Documentation | (manual verification) | 4 items | (see below) |
| AC7 | Coverage & Performance | (pytest-cov) | 1 | ≥95% coverage, <2min |

---

## Coverage Analysis

### Target Coverage: ≥95% for Template/Story Edit Operations

**Key Modules Covered:**
- `.claude/skills/devforgeai-story-creation/` - Story creation logic
- Template file operations - Read, instantiate, validate
- Story file validation - YAML, structure, DoD sections

**Coverage Report:**
```
pytest tests/ --cov=.claude/skills/devforgeai-story-creation --cov-report=term

Expected output:
- TOTAL: 95-98% (achieves ≥95% threshold)
- Module-level breakdown showing coverage per file
- Uncovered lines identified for review
```

**Viewing Coverage Report:**
```bash
# Generate HTML report
pytest tests/ --cov=.claude/skills/devforgeai-story-creation --cov-report=html

# Open in browser
open .devforgeai/qa/coverage/STORY-015-coverage-report/index.html
```

---

## Test Data and Fixtures

### Story Files Used as Fixtures

The tests use actual story files as fixtures (not mocks):

- `devforgeai/specs/Stories/STORY-027-wire-hooks-into-create-story-command.story.md`
- `devforgeai/specs/Stories/STORY-028-wire-hooks-into-create-epic-command.story.md`
- `devforgeai/specs/Stories/STORY-029-wire-hooks-into-create-sprint-command.story.md`

**Rationale:** Integration testing requires real files to validate actual file operations

### Template File Used as Fixture

- `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`

**Rationale:** Validates template changes made in STORY-014

### Temporary Test Data (E2E Tests)

- E2E tests create temporary test stories in `/tmp/` (via pytest tempfile fixture)
- Automatic cleanup on test completion
- No permanent test data left behind

---

## Test Execution Notes

### Prerequisites

1. **Environment Setup:**
   ```bash
   pip install pytest pytest-cov PyYAML
   ```

2. **File Structure:**
   - All story files must exist in `devforgeai/specs/Stories/`
   - Template must exist at `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`
   - Coverage report directory: `.devforgeai/qa/coverage/` (created by pytest-cov)

3. **File Permissions:**
   - All story files must be readable
   - Template must be readable
   - Coverage report directory must be writable

### Troubleshooting

**Test: FileNotFoundError for story files**
```
Solution: Verify story files exist:
ls -la devforgeai/specs/Stories/STORY-027* STORY-028* STORY-029*
```

**Test: yaml.YAMLError during YAML validation**
```
Solution: Check YAML syntax in story frontmatter:
head -15 devforgeai/specs/Stories/STORY-027-*.story.md
Look for: --- at line 1, --- at ~line 11 (closing delimiter)
```

**Coverage: Reports not generated**
```
Solution: Verify coverage command:
pytest tests/ --cov=.claude/skills/devforgeai-story-creation
Check: .devforgeai/qa/coverage/ directory for reports
```

---

## Non-Functional Requirements

### Performance

**Requirements:**
- Full test suite execution: <120 seconds
- Individual test execution: <2 seconds (p95)

**Verification:**
```bash
pytest tests/ --durations=0
# Review output for any test >2000ms
```

### Reliability

**Requirements:**
- 100% pass rate (all 18 tests PASS)
- Deterministic tests (no flaky failures)
- No test ordering dependencies

**Verification:**
```bash
# Run tests 10 times (check for consistency)
for i in {1..10}; do pytest tests/ -q; done
# All 10 runs should show 18 passed
```

### Security

**Requirements:**
- No sensitive data in logs
- Test output sanitized (no absolute paths)
- No secrets in test fixtures

**Verification:** Manual review of pytest output for sensitive data

---

## Maintenance

### Adding New Tests

When modifying STORY-014 or template structure:

1. **Identify affected component** (template/story/both)
2. **Find appropriate test file** (test_*.py in unit/integration/e2e)
3. **Add test following AAA pattern** (Arrange, Act, Assert)
4. **Verify coverage** (pytest --cov)
5. **Update this README** (add test to table)

### Updating Test Data

If story files are updated (legitimate changes):

1. **Verify changes don't break tests**
   ```bash
   pytest tests/ -v
   ```

2. **If tests fail, update test assertions** to match new structure
3. **Re-run coverage** to verify ≥95% still achieved
4. **Document changes** in test file comments

### Refactoring Tests

Keep tests maintainable:

- **Extract common logic** to helper methods
- **Use pytest fixtures** for setup/teardown
- **Keep test names descriptive** (test_should_[behavior]_when_[condition])
- **Comment complex assertions** for clarity

---

## Related Documentation

- **STORY-015:** Comprehensive Testing for STORY-014 DoD Template
- **STORY-014:** Add Definition of Done Section to Story Template
- **STORY-007:** Post-Operation Retrospective Conversation (reference story)
- **ADR-002:** Defer STORY-014 Testing to Dedicated Story

---

## Contact

For questions about the test suite:

1. **Test implementation:** See test file docstrings
2. **Coverage gaps:** Run `pytest --cov` and check coverage report
3. **Flaky tests:** Review test file for dependencies on execution order
4. **Performance:** Run `pytest --durations=0` and investigate slow tests

---

**Test Suite Version:** 1.0
**Last Updated:** 2025-11-13
**Framework:** pytest + pytest-cov
**Coverage Target:** ≥95% for template/story edit operations
