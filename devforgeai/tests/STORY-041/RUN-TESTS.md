# STORY-041 Test Execution Guide

Quick reference for running the test suite for STORY-041.

---

## Quick Start

### Run All Tests (Sequential)
```bash
cd /mnt/c/Projects/DevForgeAI2

# Run all tests in order
for test in devforgeai/tests/STORY-041/test-ac*.sh; do
    bash "$test" || true
done
```

### Run Individual Tests

**AC#1: Directory Structure**
```bash
bash devforgeai/tests/STORY-041/test-ac1-directory-structure.sh
```

**AC#2: .gitignore Rules**
```bash
bash devforgeai/tests/STORY-041/test-ac2-gitignore-rules.sh
```

**AC#3: version.json Schema**
```bash
bash devforgeai/tests/STORY-041/test-ac3-version-json.sh
```

**AC#4: Current Operations**
```bash
bash devforgeai/tests/STORY-041/test-ac4-current-operations.sh
```

**AC#5: Git Tracking**
```bash
bash devforgeai/tests/STORY-041/test-ac5-git-tracking.sh
```

**AC#6: Specification Match**
```bash
bash devforgeai/tests/STORY-041/test-ac6-specification-match.sh
```

**AC#7: Component Counts**
```bash
bash devforgeai/tests/STORY-041/test-ac7-component-counts.sh
```

---

## Test Status

### Current Status: RED Phase (All Failing)

```
AC#1 Directory Structure      ✗ FAIL  (src/ doesn't exist)
AC#2 .gitignore Rules         ✗ FAIL  (.gitignore not updated)
AC#3 version.json Schema      ✗ FAIL  (version.json missing)
AC#4 Current Operations       ✓ PASS  (operational code intact)
AC#5 Git Tracking             ✗ FAIL  (src/ not committed)
AC#6 Specification Match      ✗ FAIL  (structure missing)
AC#7 Component Counts         ✗ FAIL  (version.json missing)
```

---

## Test Execution Details

### Each test produces:
1. **Test Groups** - Organized by theme
2. **Individual Assertions** - Pass/Fail per test
3. **Colored Output**
   - 🟢 PASS (green) - Test passed
   - 🔴 FAIL (red) - Test failed
   - 🟡 SKIP (yellow) - Test skipped (deferred)

4. **Summary Section**
   ```
   ═══════════════════════════════════════════
   TEST SUMMARY: AC#[N]
   ═══════════════════════════════════════════
   Tests Run:    XX
   Tests Passed: YY
   Tests Failed: ZZ

   STATUS: FAILING/PASSING
   ```

---

## Interpreting Results

### When test_ac1_directory_structure.sh runs:

```
✓ PASS: src/claude/ directory exists
✓ PASS: src/claude/skills/ directory exists
✓ PASS: src/claude/agents/ directory exists
✓ PASS: src/claude/commands/ directory exists
✓ PASS: src/claude/memory/ directory exists
✓ PASS: src/claude/ contains exactly 4 subdirectories

✗ FAIL: src/claude/skills/devforgeai-ideation exists
  Expected directory: src/claude/skills/devforgeai-ideation

...

STATUS: FAILING (Red Phase) ✗
Expected: All tests should be FAILING initially (TDD Red phase)
Reason:   src/ directory structure does not yet exist
```

---

## Test Assertions Explained

### AC#1: Directory Assertions
```bash
assert_directory_exists "src/claude" "src/claude/ directory exists"
# Checks: [ -d "src/claude" ]
```

### AC#2: .gitignore Pattern Assertions
```bash
assert_pattern_in_gitignore "src/devforgeai/qa/coverage/*" "Exclusion pattern"
# Checks: grep -F "pattern" .gitignore
```

### AC#3: JSON Validation
```bash
assert_valid_json "version.json" "Valid JSON format"
# Checks: python -m json.tool version.json > /dev/null
```

### AC#4: Grep Assertions
```bash
assert_grep_no_matches "src/claude" ".claude/commands/" "No references to src/"
# Checks: grep -r "pattern" path | wc -l == 0
```

### AC#5: Git Assertions
```bash
assert_git_check_ignore "src/devforgeai/qa/reports/test.md" 0 "File is ignored"
# Checks: git check-ignore path; echo $?
```

### AC#6: Count Assertions
```bash
assert_subdirectory_count "src/claude" 4 "Contains 4 subdirs"
# Checks: find dir -maxdepth 1 -type d | wc -l == 4
```

### AC#7: Component Count Assertions
```bash
assert_component_count_matches "Skills" 10 5 "Skills count accurate"
# Compares: json_count == actual_count
```

---

## Running Tests with Output Capture

### Save results to file:
```bash
bash devforgeai/tests/STORY-041/test-ac1-directory-structure.sh | tee test-ac1-results.txt
```

### View only failures:
```bash
bash devforgeai/tests/STORY-041/test-ac1-directory-structure.sh 2>&1 | grep "FAIL"
```

### Count test results:
```bash
bash devforgeai/tests/STORY-041/test-ac1-directory-structure.sh 2>&1 | grep -c "PASS"
bash devforgeai/tests/STORY-041/test-ac1-directory-structure.sh 2>&1 | grep -c "FAIL"
```

---

## Batch Test Execution

### Run all tests and collect summary:
```bash
#!/bin/bash
cd /mnt/c/Projects/DevForgeAI2

echo "STORY-041 Test Execution Summary"
echo "================================="
echo ""

TOTAL_PASSED=0
TOTAL_FAILED=0

for test in devforgeai/tests/STORY-041/test-ac*.sh; do
    NAME=$(basename "$test" .sh)
    AC=$(echo "$NAME" | grep -o "ac[0-9]")

    echo -n "Running AC#${AC#ac}... "

    if bash "$test" > /tmp/test-output.txt 2>&1; then
        echo "PASS ✓"
        ((TOTAL_PASSED++))
    else
        echo "FAIL ✗"
        ((TOTAL_FAILED++))
        # Show last 5 lines of output
        tail -5 /tmp/test-output.txt | sed 's/^/  /'
    fi
done

echo ""
echo "================================="
echo "Total: $TOTAL_PASSED PASS, $TOTAL_FAILED FAIL"
```

Save as `run-all-tests.sh` and execute:
```bash
chmod +x run-all-tests.sh
./run-all-tests.sh
```

---

## After Implementation

Once implementation is complete, all tests should PASS:

```bash
#!/bin/bash
cd /mnt/c/Projects/DevForgeAI2

echo "Validating STORY-041 Implementation..."
echo ""

ALL_PASS=true
for test in devforgeai/tests/STORY-041/test-ac*.sh; do
    AC=$(basename "$test" | grep -o "ac[0-9]")

    if bash "$test" > /dev/null 2>&1; then
        echo "✓ AC#${AC#ac} PASS"
    else
        echo "✗ AC#${AC#ac} FAIL"
        ALL_PASS=false
    fi
done

echo ""
if [ "$ALL_PASS" = true ]; then
    echo "✓ All acceptance criteria validated!"
    exit 0
else
    echo "✗ Some tests failed. Review output above."
    exit 1
fi
```

---

## Test Dependencies

Each test requires:
- **Bash 4.0+** (for array support)
- **Python 3** (for JSON validation in AC#3, AC#7)
- **Git** (for AC#2, AC#4, AC#5)
- **Standard Unix tools** (grep, find, wc, stat, ls)

Check availability:
```bash
bash --version       # Should be 4.0+
python3 --version   # Should be 3.6+
git --version       # Any recent version
```

---

## Troubleshooting

### "bash: No such file or directory"
Make sure you're in the project root:
```bash
cd /mnt/c/Projects/DevForgeAI2
pwd  # Should show /mnt/c/Projects/DevForgeAI2
```

### "Permission denied"
Make test files executable:
```bash
chmod +x devforgeai/tests/STORY-041/*.sh
```

### "python3: command not found"
For AC#3 and AC#7 only. Install Python or use:
```bash
# Skip JSON validation (will run other tests)
# Only impacts AC#3, AC#7 tests
```

### "test-ac4 fails unexpectedly"
AC#4 validates current operational code. If it fails:
- Check that .claude/ and devforgeai/ folders exist
- Verify operational code hasn't been modified
- This test should always PASS (validates baseline)

---

## Test Output Examples

### Passing Test
```
✓ PASS: Directory structure is created
  Path: src/claude/
✓ PASS: src/claude/skills/ contains 10 skill subdirectories
  Count: 10 (expected: 10)

...

Tests Run:    35
Tests Passed: 35
Tests Failed: 0

STATUS: PASSING ✓
```

### Failing Test
```
✗ FAIL: src/claude/ directory exists
  Expected directory: src/claude/
✗ FAIL: src/claude/skills/ subdirectory exists
  Expected: src/claude/skills/

...

Tests Run:    35
Tests Passed: 0
Tests Failed: 35

STATUS: FAILING (Red Phase) ✗
```

---

## Documentation

For detailed test documentation, see:
- **TEST-STATUS-REPORT.md** - Comprehensive analysis
- **STORY-041.story.md** - Acceptance criteria and specifications

---

## Quick Exit Codes

```
0 = All tests passed
1 = One or more tests failed
```

Use in scripts:
```bash
bash test-ac1-directory-structure.sh
if [ $? -eq 0 ]; then
    echo "AC#1 passed!"
else
    echo "AC#1 failed!"
fi
```

---

**Last Updated:** 2025-11-18
**Test Suite Version:** 1.0
**Framework Phase:** TDD Red Phase
