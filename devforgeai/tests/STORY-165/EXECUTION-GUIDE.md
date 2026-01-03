# STORY-165 Test Execution Guide

## Quick Start

Run all tests with:

```bash
bash devforgeai/tests/STORY-165/run-all-tests.sh
```

## Test Files Overview

| File | Purpose | AC Coverage |
|------|---------|------------|
| `test-ac1-template-format.sh` | Verify template uses `### AC#N: Title` format | AC#1 |
| `test-ac2-new-stories-format.sh` | Verify new stories follow updated format | AC#2 |
| `test-ac3-no-breaking-changes.sh` | Verify old stories not auto-migrated | AC#3 |
| `test-ac4-numbering-reference.sh` | Verify AC#N numbering is referenceable | AC#4 |
| `run-all-tests.sh` | Test suite orchestrator | All ACs |

## Running Tests

### Method 1: Run All Tests at Once (Recommended)

```bash
bash devforgeai/tests/STORY-165/run-all-tests.sh
```

**Output:**
- Summary of all test results (PASS/FAIL)
- Error messages for failed tests
- Remediation steps if tests fail

---

### Method 2: Run Individual Tests

#### AC#1: Template Format Verification
```bash
bash devforgeai/tests/STORY-165/test-ac1-template-format.sh
```

**What it tests:**
- Template file exists at correct location
- Acceptance Criteria section is present
- AC headers use format: `### AC#1: {Title}`
- No old checkbox syntax (`### 1. [ ]`) exists

**Expected output (if PASS):**
```
✓ Template file found: .claude/skills/devforgeai-story-creation/assets/templates/story-template.md
✓ Acceptance Criteria section found

Example AC headers from template:
### AC#1: [Criterion 1 Title]
### AC#2: [Criterion 2 Title]
### AC#3: [Criterion 3 Title]
### AC#4: [Criterion 4 Title]

PASS: Template AC headers use correct format (### AC#N: {Title})
PASS: No old checkbox syntax found (### N. [ ] {Title})
```

---

#### AC#2: New Stories Format Verification
```bash
bash devforgeai/tests/STORY-165/test-ac2-new-stories-format.sh
```

**What it tests:**
- Story template is properly formatted
- New stories will inherit correct AC format
- No checkbox syntax in template examples

**Expected output (if PASS):**
```
✓ Story template found
✓ Extracted AC section from template
✓ Found 4 AC headers in correct format

Example AC headers from template:
### AC#1: [Criterion 1 Title]
### AC#2: [Criterion 2 Title]

PASS: New stories will use correct AC header format
PASS: Template generates stories without checkbox syntax
```

---

#### AC#3: Backward Compatibility Verification
```bash
bash devforgeai/tests/STORY-165/test-ac3-no-breaking-changes.sh
```

**What it tests:**
- Existing stories are not automatically migrated
- Old-format stories remain unchanged
- No mixed-format stories (both old and new in same story)

**Expected output (if PASS):**
```
✓ Stories directory found: devforgeai/specs/Stories

Scanning for stories with AC headers...
  ✓ STORY-007-*.story.md: Has old format (not migrated)
  ✓ STORY-008-*.story.md: Has old format (not migrated)
  ... (many stories listed)

Story Format Summary:
  Stories with old format: 40
  Stories with new format: 133
  Stories with mixed format: 0

PASS: Found 40 stories with old format (not automatically migrated)
PASS: No automatic migration occurred (old stories unchanged)
PASS: No mixed-format stories detected
```

**Note:** Some scenarios may show mixed-format stories, indicating partial migrations. See TEST-RESULTS-SUMMARY.md for analysis.

---

#### AC#4: Numbering Reference Verification
```bash
bash devforgeai/tests/STORY-165/test-ac4-numbering-reference.sh
```

**What it tests:**
- AC numbering is sequential and unambiguous
- References like "See AC#3" work correctly
- Numbering supports cross-referencing

**Expected output (if PASS):**
```
✓ Template file found
✓ AC section extracted
✓ Found 4 AC headers in template

AC Headers found in template:
  AC#1: [Criterion 1 Title]
  AC#2: [Criterion 2 Title]
  AC#3: [Criterion 3 Title]
  AC#4: [Criterion 4 Title]

✓ Found 4 AC headers in template
✓ All AC numbers are valid numeric format

Testing reference format validity...
  ✓ Reference format valid: 'AC#1'
  ✓ Reference format valid: 'AC#2'
  ✓ Reference format valid: 'See AC#1'

PASS: AC numbering is sequential and unambiguous
PASS: AC#N format enables clear cross-references
PASS: References like 'See AC#3' work logically
```

---

## Interpreting Test Results

### All Tests Pass ✅

```
═════════════════════════════════════════════════
  Total Tests:  4
  Passed:      4
  Failed:      0

✓ All tests passed!
═════════════════════════════════════════════════
```

**Status:** STORY-165 implementation is complete. All acceptance criteria are satisfied.

**Next Steps:**
- Mark story as "Dev Complete"
- Proceed to Phase 03: QA validation
- Update Definition of Done

---

### Some Tests Fail ❌

```
═════════════════════════════════════════════════
  Total Tests:  4
  Passed:      3
  Failed:      1

✗ 1 test(s) failed
═════════════════════════════════════════════════

Next steps:
  1. Review failing test output above
  2. Implement AC#1: Update template...
  3. ...
```

**Status:** Implementation incomplete. Review failing tests.

**Troubleshooting:**
1. Read error output carefully
2. Identify which AC failed
3. Check implementation requirements
4. Fix and re-run test

---

## Test Output Explanation

### PASS Indicator
```
[0;32mPASS[0m
```
Green text = Test passed = Assertion satisfied

### FAIL Indicator
```
[0;31mFAIL[0;00m
```
Red text = Test failed = Implementation needed

### Test Pattern

Each test follows this structure:

```bash
echo "================================"
echo "AC#N: [Acceptance Criterion Title]"
echo "================================"

# Step 1: Verify preconditions
if [ ! -f "$FILE" ]; then
    echo "FAIL: File not found"
    exit 1
fi

# Step 2: Extract relevant data
DATA=$(extract from file)

# Step 3: Verify expectations
if [ condition ]; then
    echo "PASS: Assertion successful"
    exit 0
else
    echo "FAIL: Assertion failed"
    exit 1
fi
```

---

## Common Issues & Solutions

### Issue: "Template file not found"

**Cause:** Test is running from wrong directory or file path is incorrect

**Solution:**
```bash
# Run test from project root:
cd /mnt/c/Projects/DevForgeAI2
bash devforgeai/tests/STORY-165/run-all-tests.sh
```

---

### Issue: "No AC headers found"

**Cause:** Template has been moved or renamed

**Solution:**
```bash
# Find the template:
find . -name "story-template.md" -type f

# Update test file path if needed:
# In test scripts, change:
# TEMPLATE_FILE=".claude/skills/devforgeai-story-creation/assets/templates/story-template.md"
# To the correct path
```

---

### Issue: Tests hang or don't complete

**Cause:** Grep pattern is matching too much or too little

**Solution:**
```bash
# Run test with debugging:
bash -x devforgeai/tests/STORY-165/test-ac1-template-format.sh 2>&1 | head -50

# Review the output to see where it's hanging
```

---

### Issue: "Mixed format detected"

**Cause:** Some stories have both old and new AC header formats

**Solution:**
See TEST-RESULTS-SUMMARY.md for analysis and remediation options.

---

## Performance Notes

- **Test Suite Runtime:** ~2-5 seconds (all 4 tests)
- **Individual Test Runtime:** 0.5-1 second each
- **No external dependencies required**
- **No network calls made**
- **All tests use local files only**

---

## Integrating with CI/CD

### GitHub Actions Example

```yaml
name: STORY-165 Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run STORY-165 Tests
        run: bash devforgeai/tests/STORY-165/run-all-tests.sh
```

### GitLab CI Example

```yaml
story-165-tests:
  script:
    - bash devforgeai/tests/STORY-165/run-all-tests.sh
```

---

## Test Maintenance

### Adding New Tests

To add a new test for a new AC:

1. Create `test-ac5-new-feature.sh`
2. Follow template structure
3. Update `run-all-tests.sh` (automatically picks up `test-*.sh` files)
4. Update README.md with new test documentation

### Updating Existing Tests

If template format changes:

1. Update the relevant test pattern
2. Test manually first: `bash test-ac1-template-format.sh`
3. Verify all tests still pass: `bash run-all-tests.sh`
4. Document change in test file comments

---

## Reference Documentation

- **Story Requirements:** `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`
- **Test Strategy:** `devforgeai/tests/STORY-165/README.md`
- **Results Analysis:** `devforgeai/tests/STORY-165/TEST-RESULTS-SUMMARY.md`
- **Template Changelog:** Template file lines 80-95 (RCA-012 v2.1)

---

## Questions?

For test-related questions, refer to:
1. `README.md` - Overview and AC details
2. `TEST-RESULTS-SUMMARY.md` - Test results and remediation
3. Test script comments - Implementation details
4. Template file - Source of truth for format

---

**Last Updated:** 2026-01-03
**Test Framework:** Bash with grep pattern matching
**Maintained by:** test-automator subagent
