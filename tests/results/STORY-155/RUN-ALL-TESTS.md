# STORY-155 Test Execution Guide

**Story**: STORY-155 - RCA Document Parsing
**Test Suite**: 75 Failing Tests (TDD Red Phase)
**Framework**: Bash
**Location**: `/mnt/c/Projects/DevForgeAI2/tests/results/STORY-155/`

---

## Quick Start

### Run All Tests
```bash
cd /mnt/c/Projects/DevForgeAI2/tests/results/STORY-155/

# Execute all test files in sequence
bash test-rca-parser-ac1-frontmatter.sh
bash test-rca-parser-ac2-recommendations.sh
bash test-rca-parser-ac3-effort.sh
bash test-rca-parser-ac4-success-criteria.sh
bash test-rca-parser-ac5-filtering.sh
bash test-rca-parser-integration.sh
```

### Run Tests by Acceptance Criteria

**AC#1 - Frontmatter Parsing (15 tests)**
```bash
bash test-rca-parser-ac1-frontmatter.sh
```

**AC#2 - Recommendations (15 tests)**
```bash
bash test-rca-parser-ac2-recommendations.sh
```

**AC#3 - Effort Estimates (15 tests)**
```bash
bash test-rca-parser-ac3-effort.sh
```

**AC#4 - Success Criteria (15 tests)**
```bash
bash test-rca-parser-ac4-success-criteria.sh
```

**AC#5 - Filtering & Sorting (15 tests)**
```bash
bash test-rca-parser-ac5-filtering.sh
```

**Integration Tests (15 tests)**
```bash
bash test-rca-parser-integration.sh
```

---

## Expected Test Output

### For Each Test File
```
==========================================
STORY-155 AC#N: [Test Category Name]
==========================================

TEST: test_<scenario_1>
  Scenario: ...
  Expected: ...
  Implementation needed: ...

TEST: test_<scenario_2>
  ...

==========================================
All AC#N tests generated (FAILING)
Implementation required for all tests
==========================================
```

### Example Output
```
==========================================
STORY-155 AC#1: Parse RCA Frontmatter
==========================================

TEST: test_parse_frontmatter_extracts_id
  Scenario: Parse RCA with valid frontmatter
  Expected: id field = 'RCA-022'
  Implementation needed: grep '^id:' and extract value

TEST: test_parse_frontmatter_extracts_title
  Scenario: Parse RCA with valid frontmatter
  Expected: title = 'Database Connection Pool Exhaustion'
  Implementation needed: grep '^title:' and extract value

... (13 more tests)

==========================================
All AC#1 tests generated (FAILING)
Implementation required for all tests
==========================================
```

---

## Test Files Overview

| File | Tests | Focus |
|------|-------|-------|
| `test-rca-parser-ac1-frontmatter.sh` | 15 | YAML frontmatter parsing & metadata extraction |
| `test-rca-parser-ac2-recommendations.sh` | 15 | Recommendation extraction & ordering |
| `test-rca-parser-ac3-effort.sh` | 15 | Effort estimation & story point conversion |
| `test-rca-parser-ac4-success-criteria.sh` | 15 | Success criteria extraction & association |
| `test-rca-parser-ac5-filtering.sh` | 15 | Filtering by threshold & priority sorting |
| `test-rca-parser-integration.sh` | 15 | End-to-end workflows & integration |

---

## Test Scenarios by Category

### AC#1: Frontmatter Parsing
- Extract id, title, date, severity, status, reporter fields
- Validate YAML frontmatter between --- markers
- Handle missing/malformed frontmatter
- Validate enum values (severity, status)
- Validate date format (YYYY-MM-DD)
- Validate id format (RCA-NNN)

### AC#2: Recommendation Extraction
- Extract recommendations from `### REC-N: PRIORITY - Title` format
- Parse id, priority, title, description
- Maintain document order
- Handle multiple recommendations
- Detect malformed headers
- Handle duplicate IDs

### AC#3: Effort Estimation
- Extract hours: `**Effort Estimate:** 8 hours`
- Extract story points: `**Effort Estimate:** 5 story points`
- Convert points to hours (1 point = 4 hours)
- Handle mixed units
- Validate positive integer values
- Handle missing estimates

### AC#4: Success Criteria
- Extract checklist: `**Success Criteria:**` section
- Parse checkbox items: `- [ ] Checklist item`
- Associate with parent recommendation
- Handle multiple criteria per recommendation
- Strip checkbox markers from text

### AC#5: Filtering & Sorting
- Filter by effort_hours >= threshold
- Sort by priority: CRITICAL > HIGH > MEDIUM > LOW
- Apply story point conversion before threshold
- Maintain document order within priority groups
- Handle edge cases (threshold=0, all filtered out)

### Integration Tests
- Complete parse → extract → filter → sort workflow
- Data model relationships
- Error handling
- Performance validation (<500ms for 100 recommendations)
- Real-world scenarios
- Multiple RCA sequential parsing

---

## Implementation Checklist

When implementing the parser, ensure all tests pass:

### Phase 03 (Green) Implementation
- [ ] Create RCAParser service in `.claude/commands/create-stories-from-rca.md`
- [ ] Implement RCADocument data model
- [ ] Implement Recommendation data model
- [ ] Implement frontmatter parsing (AC#1) - 15 tests should pass
- [ ] Implement recommendation extraction (AC#2) - 15 tests should pass
- [ ] Implement effort extraction (AC#3) - 15 tests should pass
- [ ] Implement success criteria extraction (AC#4) - 15 tests should pass
- [ ] Implement filtering & sorting (AC#5) - 15 tests should pass
- [ ] Verify integration tests pass (15 tests)

### Acceptance Criteria Verification
```
AC#1: Parse RCA Frontmatter ✓ (15/15 tests passing)
AC#2: Extract Recommendations ✓ (15/15 tests passing)
AC#3: Extract Effort Estimates ✓ (15/15 tests passing)
AC#4: Extract Success Criteria ✓ (15/15 tests passing)
AC#5: Filter by Threshold ✓ (15/15 tests passing)
Integration Tests ✓ (15/15 tests passing)

TOTAL: 75/75 tests passing ✓
```

---

## Test Infrastructure

### Test Utilities Available
Each test file includes these utility functions:
```bash
assert_equals() {
    local expected="$1"
    local actual="$2"
    local test_name="$3"
    # Compares and reports results
}

assert_array_length() {
    local expected_count="$1"
    local actual_count="$2"
    local test_name="$3"
    # Validates array/list sizes
}

assert_not_empty() {
    local value="$1"
    local test_name="$2"
    # Validates value is not empty
}
```

### Test Setup Functions
Each file provides setup functions for different RCA scenarios:
```bash
setup_valid_rca_file()              # Valid RCA with all fields
setup_rca_with_multiple_recommendations()  # 4 recommendations
setup_rca_with_success_criteria()   # With checklist items
setup_rca_no_effort()              # Missing effort estimates
setup_rca_malformed_frontmatter()  # Invalid YAML
# ... and many more
```

---

## Debugging Failed Tests

### When Tests Fail (Expected During Implementation)

1. **Read the test output** - Each test includes:
   - Test name
   - Scenario description
   - Expected outcome
   - Implementation hints

2. **Review the test file** - Look at setup functions to understand:
   - What test data is created
   - What format is expected
   - What validation rules apply

3. **Check implementation** - Verify parser:
   - Reads file correctly
   - Extracts data in expected format
   - Validates constraints (enums, formats)
   - Handles edge cases gracefully

### Example Debugging Session
```bash
# Run AC#1 tests
bash test-rca-parser-ac1-frontmatter.sh

# Output shows which tests fail:
TEST: test_parse_frontmatter_extracts_id
  Scenario: Parse RCA with valid frontmatter
  Expected: id field = 'RCA-022'
  Implementation needed: grep '^id:' and extract value

# Check what test data looks like:
head /tmp/test-rca-valid.md

# Verify your parser handles this correctly:
# 1. Check that ID is extracted from YAML
# 2. Validate format matches RCA-NNN
# 3. Return in structured object
```

---

## Test Data Files

Tests create temporary test files in `/tmp/`:

| File | Used By | Content |
|------|---------|---------|
| `/tmp/test-rca-valid.md` | AC#1 | Valid RCA with all fields |
| `/tmp/test-rca-minimal.md` | AC#1 | Minimal required fields only |
| `/tmp/test-rca-no-frontmatter.md` | AC#1 | RCA without YAML frontmatter |
| `/tmp/test-rca-recommendations.md` | AC#2 | 4 recommendations with varied priorities |
| `/tmp/test-rca-effort-hours.md` | AC#3 | Effort specified in hours |
| `/tmp/test-rca-story-points.md` | AC#3 | Effort specified in story points |
| `/tmp/test-rca-success-criteria.md` | AC#4 | Recommendations with success criteria |
| `/tmp/test-rca-filter.md` | AC#5 | Comprehensive RCA for filtering tests |
| `/tmp/test-rca-integration.md` | Integration | Full RCA with all components |

---

## Performance Requirements

### NFR: Parse Time < 500ms
The integration test includes performance validation:
```bash
test_performance_large_rca()
  # Creates RCA with 100 recommendations
  # Expects parsing to complete in <500ms
```

When this test passes, parser meets performance requirements.

---

## Business Rules Implementation

### BR-001: Effort Threshold Filter
```
RULE: Only recommendations with effort_hours >= threshold are returned
TEST: test_filter_recommendations_threshold_2
EXPECTED: Items with effort < threshold excluded from results
```

### BR-002: Priority Sorting
```
RULE: Results sorted by priority (CRITICAL > HIGH > MEDIUM > LOW)
TEST: test_sort_critical_first, test_sort_high_second, etc.
EXPECTED: Recommendations ordered by priority level
```

### BR-003: Story Point Conversion
```
RULE: Convert story points to hours using 1 point = 4 hours
TEST: test_convert_story_points_to_hours
EXPECTED: 5 points = 20 hours, 3 points = 12 hours, etc.
```

---

## Continuous Testing During Development

### After Each Implementation Stage
```bash
# After AC#1 implementation
bash test-rca-parser-ac1-frontmatter.sh
# Expect: 15/15 passing

# After AC#2 implementation
bash test-rca-parser-ac2-recommendations.sh
# Expect: 15/15 passing

# ... repeat for AC#3, AC#4, AC#5

# After complete implementation
bash test-rca-parser-integration.sh
# Expect: 15/15 passing
```

### Running All Tests Together
```bash
# Run all test files and collect results
for test_file in test-rca-parser-*.sh; do
    echo "Running $test_file..."
    bash "$test_file"
done
```

---

## Test Maintenance

### Adding New Tests
If additional scenarios need testing:
1. Add new test function to appropriate file
2. Follow naming convention: `test_<scenario>_<expected>`
3. Include Arrange, Act, Assert comments
4. Update TEST-GENERATION-SUMMARY.md with new count

### Modifying Test Data
Test setup functions can be modified to test new scenarios:
```bash
setup_rca_custom_scenario() {
    cat > /tmp/test-rca-custom.md <<'EOF'
---
# Custom RCA definition
---
Content
EOF
}
```

### Updating Expected Outcomes
As requirements evolve, update test expectations:
```bash
test_example() {
    # OLD: Expected: X
    # NEW: Expected: Y (with reason for change)
    echo "TEST: test_example"
    echo "  Expected: Y (updated requirement)"
}
```

---

## Troubleshooting

### Tests Not Running
```bash
# Check file permissions
ls -l test-rca-parser-*.sh
# Should show -rwxrwxrwx

# Make executable if needed
chmod +x test-rca-parser-*.sh
```

### Tests Not Finding Test Data
```bash
# Ensure /tmp is writable
touch /tmp/test-file
rm /tmp/test-file

# Tests create files in /tmp during execution
# If /tmp is full or read-only, tests will fail
```

### Bash Syntax Errors
```bash
# Check for shell syntax errors
bash -n test-rca-parser-ac1-frontmatter.sh
# Should output nothing if valid

# Run with debug output
bash -x test-rca-parser-ac1-frontmatter.sh 2>&1 | head -20
```

---

## Integration with CI/CD

### GitHub Actions (Example)
```yaml
- name: Run STORY-155 Tests
  run: |
    cd tests/results/STORY-155/
    bash test-rca-parser-ac1-frontmatter.sh
    bash test-rca-parser-ac2-recommendations.sh
    # ... run all test files
    # Exit code 0 = all pass, exit code 1 = any fail
```

### Local Pre-commit Hook
```bash
#!/bin/bash
# Run tests before commit
cd tests/results/STORY-155/
bash test-rca-parser-*.sh || exit 1
```

---

## Coverage Summary

| Category | Tests | Status |
|----------|-------|--------|
| AC#1 Frontmatter | 15 | All FAILING (ready to implement) |
| AC#2 Recommendations | 15 | All FAILING (ready to implement) |
| AC#3 Effort | 15 | All FAILING (ready to implement) |
| AC#4 Success Criteria | 15 | All FAILING (ready to implement) |
| AC#5 Filtering | 15 | All FAILING (ready to implement) |
| Integration | 15 | All FAILING (ready to implement) |
| **TOTAL** | **75** | **All FAILING** |

**TDD Phase**: Red (Tests written, implementation needed)

---

## References

- **Story**: `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-155-rca-document-parsing.story.md`
- **Tech Stack**: `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/tech-stack.md`
- **Source Tree**: `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/source-tree.md`
- **Test Summary**: `/mnt/c/Projects/DevForgeAI2/tests/results/STORY-155/TEST-GENERATION-SUMMARY.md`

---

**Last Updated**: 2025-12-30
**Test Suite Version**: 1.0
**Status**: Ready for Phase 03 (Green - Implementation)
