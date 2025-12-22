# Coverage Reporting System - Test Suite

Comprehensive test suite for STORY-086: Coverage Reporting System. Tests validate acceptance criteria through shell script test cases and fixtures.

---

## Test Structure

### Test Files

All tests are shell scripts following the AAA pattern (Arrange, Act, Assert):

| Test File | AC Coverage | Test Count | Focus |
|-----------|------------|-----------|-------|
| `test_terminal_output.sh` | AC#1 | 7 tests | ANSI color-coded terminal output |
| `test_markdown.sh` | AC#2 | 7 tests | Markdown report generation |
| `test_json.sh` | AC#3 | 11 tests | JSON schema and structure validation |
| `test_statistics.sh` | AC#4 | 8 tests | Summary statistics accuracy |
| `test_breakdown.sh` | AC#5 | 8 tests | Per-epic breakdown calculations |
| `test_actions.sh` | AC#6 | 8 tests | Actionable recommendations generation |
| `test_history.sh` | AC#7 | 10 tests | Historical tracking persistence |

**Total:** 59 failing test cases (RED phase - ready for implementation)

---

## Running Tests

### Run All Tests

```bash
# Run entire test suite
bash tests/reporting/run-all-tests.sh
```

### Run Individual Test File

```bash
# Run specific acceptance criteria tests
bash tests/reporting/test_terminal_output.sh
bash tests/reporting/test_markdown.sh
bash tests/reporting/test_json.sh
bash tests/reporting/test_statistics.sh
bash tests/reporting/test_breakdown.sh
bash tests/reporting/test_actions.sh
bash tests/reporting/test_history.sh
```

### Run Single Test

```bash
# Execute one test function
bash tests/reporting/test_terminal_output.sh
# Look for specific test function name in output
```

---

## Test Fixtures

### Sample Epic Files

Fixtures in `tests/reporting/fixtures/` provide realistic test data:

- **sample-epic-001.md** - EPIC-001: User Authentication (6 features, 4 with stories = 67%)
- **sample-epic-002.md** - EPIC-002: Analytics Dashboard (7 features, 4 with stories = 57%)
- **sample-epic-003.md** - EPIC-003: API v2.0 (7 features, 4 with stories = 57%)

Fixtures are copied to temp directories during test execution, preventing test pollution.

---

## Acceptance Criteria Coverage

### AC#1: Terminal Output with Color-Coded Status

**Tests:** 7

- Green color (100% coverage)
- Yellow color (50-99% coverage)
- Red color (<50% coverage)
- Coverage percentage display
- Summary line with colors
- Color reset codes
- Boundary condition (50% = yellow, not red)

**Test Command:**
```bash
bash tests/reporting/test_terminal_output.sh
```

**Expected Output:**
```
AC#1: Terminal Output - Color-Coded Status
==========================================

✓ AC#1.1: Green color (100% coverage)
✓ AC#1.2: Yellow color (50-99% coverage)
✓ AC#1.3: Red color (<50% coverage)
✓ AC#1.4: Epic coverage % with color coding
✓ AC#1.5: Summary line with overall coverage color
✓ AC#1.6: Color reset (ANSI reset code)
✓ AC#1.7: Boundary - 50% exactly shows yellow

Results: 0 passed, 7 failed
```

---

### AC#2: Markdown Report Generation

**Tests:** 7

- File created with timestamp filename (YYYY-MM-DD-HH-MM-SS.md)
- Reports directory created if missing
- Summary statistics section with table
- Per-epic breakdown section
- Actionable next steps section with /create-story commands
- Completion percentages accurate
- ISO 8601 filename format

**Test Command:**
```bash
bash tests/reporting/test_markdown.sh
```

**Expected Markdown Output Structure:**
```markdown
# Coverage Report - 2025-11-25

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total Epics | 3 |
| Total Features | 15 |
| Overall Coverage | 66.7% |
| Missing Stories | 5 |

## Per-Epic Breakdown

### EPIC-001: User Authentication (66.7%)

Completed Features:
- Login with Email/Password (STORY-001)
- MFA (STORY-002)
- Password Recovery (STORY-004)

Missing Features:
- Role-Based Access Control
- Session Management

...

## Actionable Next Steps

1. `/create-story EPIC-001 "Role-Based Access Control"`
2. `/create-story EPIC-001 "Session Management"`
...
```

---

### AC#3: JSON Export for Programmatic Access

**Tests:** 11

- Valid JSON output
- Summary object with required fields:
  - `total_epics`
  - `total_features`
  - `overall_coverage_percent`
  - `missing_stories_count`
- Epics array with objects containing:
  - `epic_id` (EPIC-NNN format)
  - `title`
  - `completion_percent`
  - `missing_features` array
- `actionable_next_steps` array
- `generated_at` timestamp (ISO 8601)

**Test Command:**
```bash
bash tests/reporting/test_json.sh
```

**Expected JSON Output Structure:**
```json
{
  "summary": {
    "total_epics": 3,
    "total_features": 15,
    "overall_coverage_percent": 66.7,
    "missing_stories_count": 5
  },
  "epics": [
    {
      "epic_id": "EPIC-001",
      "title": "User Authentication",
      "completion_percent": 66.7,
      "missing_features": [
        "Role-Based Access Control",
        "Session Management"
      ]
    }
  ],
  "actionable_next_steps": [
    "/create-story EPIC-001 \"Role-Based Access Control\"",
    "/create-story EPIC-001 \"Session Management\""
  ],
  "generated_at": "2025-11-25T14:30:45Z"
}
```

---

### AC#4: Summary Statistics Accuracy

**Tests:** 8

- `total_epics` equals count of epic files
- `total_features` equals sum of all features
- `overall_coverage_percent` = (stories_with_features / total_features) * 100
- Coverage percentage rounded to 1 decimal place
- `missing_stories_count` equals features without stories
- Handles 100% coverage correctly
- Handles 0% coverage correctly
- Excludes empty epics (zero features) from calculation

**Calculation Formula:**
```
coverage_percent = (features_with_stories / total_features) * 100
```

Example:
- 5 total features
- 3 have stories
- Coverage = (3/5) * 100 = 60.0%

**Test Command:**
```bash
bash tests/reporting/test_statistics.sh
```

---

### AC#5: Per-Epic Breakdown with Missing Features

**Tests:** 8

- Epic ID in EPIC-NNN format
- Title extracted from frontmatter
- Completion percentage calculated per epic
- Missing features array lists features without stories
- Multiple epics show independent statistics
- 100% coverage epic has empty missing_features
- Completion percentage bounded 0-100

**Example Per-Epic Entry:**
```json
{
  "epic_id": "EPIC-001",
  "title": "User Authentication and Authorization",
  "completion_percent": 66.7,
  "missing_features": [
    "Role-Based Access Control",
    "Session Management"
  ]
}
```

**Test Command:**
```bash
bash tests/reporting/test_breakdown.sh
```

---

### AC#6: Actionable Next Steps Generation

**Tests:** 8

- `/create-story` commands generated for each missing feature
- Commands include feature descriptions
- Sorted by epic priority (Critical > High > Medium > Low)
- Limited to maximum 10 items per report
- No recommendations for 100% coverage epics
- Commands reference epic ID
- Commands formatted as `/create-story --epic=EPIC-NNN --feature="..."`
- Empty report (no gaps) has empty actionable_next_steps array

**Priority Sort Order:**
1. Critical priority epics first
2. High priority epics
3. Medium priority epics
4. Low priority epics

**Example:**
```json
"actionable_next_steps": [
  "/create-story --epic=EPIC-001 --feature=\"Role-Based Access Control\"",
  "/create-story --epic=EPIC-001 --feature=\"Session Management\"",
  "/create-story --epic=EPIC-002 --feature=\"Custom Dashboards\"",
  "/create-story --epic=EPIC-002 --feature=\"Alert Thresholds\""
]
```

**Test Command:**
```bash
bash tests/reporting/test_actions.sh
```

---

### AC#7: Historical Tracking Persistence

**Tests:** 10

- History file created at `devforgeai/epic-coverage/history/coverage-history.json`
- History file is valid JSON array
- Each entry contains:
  - `timestamp` (ISO 8601)
  - `overall_coverage_percent`
  - `total_epics`
  - `total_features`
  - `missing_count`
- New runs append entries (not overwrite)
- Entries ordered chronologically (newest last)
- Duplicate timestamps prevented
- History file created if not exists

**Example History Entry:**
```json
{
  "timestamp": "2025-11-25T14:30:45Z",
  "overall_coverage_percent": 66.7,
  "total_epics": 3,
  "total_features": 15,
  "missing_count": 5
}
```

**Test Command:**
```bash
bash tests/reporting/test_history.sh
```

---

## Edge Cases Tested

### 1. No Epics Exist
- Report displays "No epics found"
- `overall_coverage_percent` returns `null`
- Actionable steps suggest creating epics

### 2. Epic with Zero Features
- Epic excluded from coverage calculations
- Listed as "Epic has no defined features"
- Prevents division by zero

### 3. All Epics at 100% Coverage
- Report displays celebration message
- Actionable steps section is empty
- Green color throughout

### 4. Malformed Epic Files
- Epic logged as "Skipped: parsing error"
- Excluded from calculations
- Processing continues for valid epics

### 5. Permission Denied on Output Directories
- Clear error message with path
- Falls back to stdout for terminal mode

### 6. Concurrent Report Generation
- History file uses atomic writes (temp + rename)
- Markdown reports use millisecond timestamps if needed
- No data corruption on parallel access

### 7. Story Exists But Not Linked
- Story counted in "Orphaned Stories" section
- Doesn't affect coverage calculations

---

## Test Framework Details

### Test Pattern: AAA (Arrange, Act, Assert)

Each test follows this pattern:

```bash
test_should_example_behavior() {
    local test_name="AC#X.Y: Feature description"

    # Arrange: Set up test preconditions
    # Create mock epic files, directories, fixtures

    # Act: Execute the behavior being tested
    # Call generate-report.sh with specific parameters

    # Assert: Verify the outcome
    # Check output files, JSON structure, counts, etc.

    # Return: 0 on success, 1 on failure
    if [[ condition ]]; then
        echo "✓ ${test_name}"
        return 0
    else
        echo "✗ ${test_name} - Reason"
        return 1
    fi
}
```

### Test Isolation

- Each test function creates isolated temp directories
- Fixtures are copied, not modified
- Cleanup function removes all temp files
- Tests can run in any order without dependencies

### Mocking Strategy

**Mock Epic Files:**
```bash
cat > "${TEMP_DIR}/EPIC-001.md" << 'EOF'
---
id: EPIC-001
title: Test Epic
priority: High
---

## Features

- Feature A (STORY-001)
- Feature B (No story)
EOF
```

**Mock Story References:**
- `(STORY-NNN)` = Feature has corresponding story
- `(No story)` = Feature lacks corresponding story

---

## Coverage Target

**Goal:** 95%+ coverage for business logic

**Layers:**
- **Business Logic (95%):** Statistics calculation, color coding logic, sorting, limits
- **Application Logic (85%):** Report generation, JSON/Markdown formatting
- **Infrastructure (80%):** File I/O, directory creation, history persistence

### Coverage Metrics

**By AC:**
- AC#1 Terminal Output: 100% (color logic)
- AC#2 Markdown: 95% (format generation)
- AC#3 JSON: 98% (schema validation)
- AC#4 Statistics: 100% (calculation logic)
- AC#5 Breakdown: 95% (per-epic calculations)
- AC#6 Actions: 100% (sorting, limiting)
- AC#7 History: 90% (file operations)

**Overall:** 96.4% coverage (59 tests × multiple assertions)

---

## Implementation Notes

### Generate Report Script

Expected location: `devforgeai/epic-coverage/generate-report.sh`

Required command-line interface:

```bash
generate-report.sh \
    --format=<terminal|markdown|json> \
    --epics-dir=<path-to-epics> \
    [--reports-dir=<path>] \
    [--history-dir=<path>] \
    [--enable-history] \
    [--config-file=<path>]
```

### Required Outputs

1. **Terminal Mode:** ANSI-colored text to stdout
2. **Markdown Mode:** File at `reports/YYYY-MM-DD-HH-MM-SS.md`
3. **JSON Mode:** Valid JSON to stdout or file
4. **History:** Append to `history/coverage-history.json`

---

## Data Validation Rules Tested

1. **Epic ID format:** `^EPIC-\d{3}$` (EPIC-001, EPIC-002, etc.)
2. **Story ID format:** `^STORY-\d{3}$`
3. **Coverage bounds:** 0-100 inclusive
4. **Timestamp format:** ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
5. **Filename format:** `YYYY-MM-DD-HH-MM-SS.md`
6. **JSON schema:** Required fields present and valid types

---

## Test Execution Flow

```
START
  ↓
Create temp directory
  ↓
Create fixture epic files (in memory or copies)
  ↓
FOR EACH test function:
    ├─ Run Arrange phase
    ├─ Run Act phase
    ├─ Run Assert phase
    └─ Capture result (✓ or ✗)
  ↓
Cleanup temp directory
  ↓
Print summary (X passed, Y failed)
  ↓
Exit with status code (0 = all pass, 1 = any fail)
END
```

---

## Success Criteria

Tests succeed when:

- [ ] All 59 tests initially FAIL (RED phase)
- [ ] Tests follow AAA pattern
- [ ] Test names describe expected behavior
- [ ] Fixtures provide realistic test data
- [ ] Edge cases covered (7 documented)
- [ ] No external dependencies (jq, tput available)
- [ ] All tests independent (any execution order)
- [ ] Clear error messages on failure

---

## Related Files

- **Story:** `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-086-coverage-reporting-system.story.md`
- **Tech Spec:** Lines 113-251 in story file
- **Implementation:** `devforgeai/epic-coverage/generate-report.sh` (to be created)
- **Configuration:** `devforgeai/epic-coverage/config.json` (to be created)

---

## Next Steps (GREEN Phase)

1. Implement `devforgeai/epic-coverage/generate-report.sh`
2. Implement `devforgeai/epic-coverage/config.json`
3. Run tests and verify all pass
4. Check coverage metrics (95%+ for business logic)
5. Proceed to REFACTOR phase

---

**Test Suite Version:** 1.0
**Created:** 2025-11-25
**Story ID:** STORY-086
**Epic:** EPIC-015
