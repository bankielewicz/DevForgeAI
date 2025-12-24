# STORY-133 Integration Test Execution Guide

## Overview

This document provides a reference for executing the integration test suite for STORY-133 (Create ideation-result-interpreter Subagent).

**Test Suite Location:** `/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-133/`

**Test Count:** 6 integration tests
**Execution Time:** ~2-3 seconds total
**Language:** Bash shell scripts

---

## Test Files

| File | Test | Category | Purpose |
|------|------|----------|---------|
| test-ac1-subagent-structure.sh | AC#1 | Structure | Validate YAML frontmatter and required sections |
| test-ac2-output-parsing.sh | AC#2 | Output Parsing | Verify ideation-specific metric parsing |
| test-ac3-success-templates.sh | AC#3 | Success Templates | Validate success case display templates |
| test-ac4-warning-templates.sh | AC#4 | Warning Templates | Validate warning case display templates |
| test-ac5-tool-restrictions.sh | AC#5 | Tool Restrictions | Verify read-only tool usage only |
| test-nfr-file-size.sh | NFR#1 | File Size | Validate file size constraints (≤200 lines) |

---

## Running Tests

### Individual Test Execution

Run a single test:

```bash
cd /mnt/c/Projects/DevForgeAI2
bash devforgeai/tests/STORY-133/test-ac1-subagent-structure.sh
```

### Run All Tests (Sequential)

Execute all tests in sequence:

```bash
cd /mnt/c/Projects/DevForgeAI2

for test in devforgeai/tests/STORY-133/test-*.sh; do
    bash "$test"
    if [ $? -ne 0 ]; then
        echo "FAILED: $test"
        exit 1
    fi
done

echo "All tests passed!"
```

### Run All Tests with Summary (Parallel)

Execute tests in parallel and collect results:

```bash
cd /mnt/c/Projects/DevForgeAI2

bash devforgeai/tests/STORY-133/test-ac1-subagent-structure.sh &
bash devforgeai/tests/STORY-133/test-ac2-output-parsing.sh &
bash devforgeai/tests/STORY-133/test-ac3-success-templates.sh &
bash devforgeai/tests/STORY-133/test-ac4-warning-templates.sh &
bash devforgeai/tests/STORY-133/test-ac5-tool-restrictions.sh &
bash devforgeai/tests/STORY-133/test-nfr-file-size.sh

wait
```

---

## Test Output Examples

### Test AC#1 Output (Success)

```
════════════════════════════════════════════════════════════════
Test AC#1: Subagent Structure and Initialization
Story: STORY-133
Testing: .claude/agents/ideation-result-interpreter.md
════════════════════════════════════════════════════════════════

TEST 1: File exists at .claude/agents/ideation-result-interpreter.md
  ✓ PASS: File found at .claude/agents/ideation-result-interpreter.md
...
TEST 13: Contains '# Related Subagents' section
  ✓ PASS: Related Subagents section found

════════════════════════════════════════════════════════════════
✓ AC#1 Test Suite: ALL TESTS PASSED
════════════════════════════════════════════════════════════════
```

### Test Failure Example

When a test fails, output shows:

```
TEST N: [Description]
  ✗ FAIL: [Reason]
         Expected: [Expected value]
         Found: [Actual value]
```

Exit code will be non-zero (1 or higher).

---

## Test Specifics

### AC#1: Subagent Structure

**Checks:**
1. File exists
2. YAML frontmatter starts with `---`
3. Has `name:` field
4. Has `description:` field
5. Has `tools:` field
6. Has `model:` field
7. Frontmatter closes with `---`
8. Contains `# Purpose` section
9. Contains `# When Invoked` section
10. Contains `# Workflow` section
11. Contains `# Templates` section
12. Contains `# Error Handling` section
13. Contains `# Related Subagents` section

**Expected Result:** All 13 checks pass

---

### AC#2: Ideation-Specific Output Parsing

**Checks:**
1. File exists (prerequisite)
2. Workflow includes epic count extraction
3. Workflow includes complexity score (0-60)
4. Workflow includes architecture tier (1-4)
5. Workflow includes requirements summary
6. Workflow includes functional requirements
7. Workflow includes non-functional requirements
8. Workflow includes integration points
9. Workflow includes next-action guidance
10. Workflow includes greenfield guidance
11. Workflow includes brownfield guidance

**Expected Result:** All 11 checks pass

---

### AC#3: Display Template Generation (Success)

**Checks:**
1. File exists (prerequisite)
2. Templates section exists
3. Success template mentioned
4. Header with epic count
5. Header with complexity score
6. Architecture tier classification
7. Requirements breakdown
8. Key design decisions
9. Recommended next command
10. Functional requirements breakdown
11. Non-functional requirements breakdown
12. Integration points breakdown

**Expected Result:** All 12 checks pass

---

### AC#4: Display Template Generation (Warning)

**Checks:**
1. File exists (prerequisite)
2. Templates section exists
3. Warning template mentioned
4. Completion status display
5. Quality warnings with severity
6. Incomplete sections highlighted
7. Resolution path
8. Recommendations
9. Resume ideation option
10. Proceed despite gaps option
11. Impact assessment
12. Missing information guidance

**Expected Result:** All 12 checks pass

---

### AC#5: Framework Integration and Tool Restrictions

**Checks:**
1. File exists (prerequisite)
2. Has `tools:` field
3. Contains `Read` tool
4. Contains `Glob` tool
5. Contains `Grep` tool
6. Does NOT contain `Write` tool
7. Does NOT contain `Edit` tool
8. Does NOT contain `Bash` tool
9. No `Write(` references in workflow
10. No `Edit(` references in workflow
11. No `Bash(` references in workflow
12. No shell file operation commands
13. Tools list contains only Read, Glob, Grep

**Expected Result:** All 13 checks pass (warnings are informational only)

---

### NFR#1: File Size Constraint

**Checks:**
1. File exists (prerequisite)
2. File has content (not empty)
3. Count total lines
4. File size ≤ 200 lines
5. Check for complete content
6. Verify valid UTF-8 encoding
7. Code/content density analysis
8. Verify key sections present
9. File has sufficient content (≥30 lines)

**Expected Result:** All 9 checks pass

**Metrics:**
- Target: ≤ 200 lines
- Actual: 144 lines
- Usage: 72% of limit

---

## Interpreting Results

### Exit Code 0 (Success)

All tests in the suite passed. The test output will end with:

```
✓ [Test Name] Test Suite: ALL TESTS PASSED
```

### Exit Code 1 (Failure)

At least one test in the suite failed. Output will show:

```
✗ [Test Name] Test Suite: SOME TESTS FAILED
```

Review the failed test output to identify which specific check failed and why.

---

## Debugging Failed Tests

### Common Issues

**Issue: File not found**
```
✗ FAIL: File not found at .claude/agents/ideation-result-interpreter.md
```
**Solution:** Verify the file exists at the correct location and project root is correct.

**Issue: Missing section**
```
✗ FAIL: '# Purpose' section not found
```
**Solution:** Add the missing section to the subagent file.

**Issue: Tool restriction violated**
```
✗ FAIL: 'Write' tool found in tools list (should not be present)
```
**Solution:** Remove Write tool from the tools list in YAML frontmatter.

**Issue: File too large**
```
✗ FAIL: File size exceeds limit
    Lines: 244 / 200 (+44 lines, +22%)
```
**Solution:** Reduce file size by consolidating content or removing non-essential sections.

### Manual Verification

If tests fail, manually verify:

```bash
# Check file exists
ls -la .claude/agents/ideation-result-interpreter.md

# Check YAML frontmatter
head -10 .claude/agents/ideation-result-interpreter.md

# Count lines
wc -l .claude/agents/ideation-result-interpreter.md

# Check for specific keywords
grep "epic count" .claude/agents/ideation-result-interpreter.md
grep "tools:" .claude/agents/ideation-result-interpreter.md
```

---

## Test Results Archive

After execution, test results are captured in:

- **Summary:** `STORY-133-INTEGRATION-TEST-RESULTS.md`
- **Summary (Text):** `STORY-133-INTEGRATION-SUMMARY.txt`
- **Execution Log:** `STORY-133-TEST-EXECUTION-GUIDE.md` (this file)

---

## Integration with CI/CD

To integrate these tests into CI/CD pipelines:

### GitHub Actions Example

```yaml
name: STORY-133 Integration Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Run STORY-133 Integration Tests
        run: |
          for test in devforgeai/tests/STORY-133/test-*.sh; do
            bash "$test"
            if [ $? -ne 0 ]; then
              echo "Test failed: $test"
              exit 1
            fi
          done
```

### Pre-commit Hook Example

```bash
#!/bin/bash
# .git/hooks/pre-commit

if git diff --cached --name-only | grep -q ".claude/agents/ideation-result-interpreter.md"; then
    echo "Running STORY-133 integration tests..."
    bash devforgeai/tests/STORY-133/test-ac1-subagent-structure.sh || exit 1
    bash devforgeai/tests/STORY-133/test-ac5-tool-restrictions.sh || exit 1
fi
```

---

## Performance Metrics

**Test Execution Time:**
- Single test: ~300-400ms
- Full suite (sequential): ~2-3 seconds
- Full suite (parallel): ~400-500ms

**Token Usage:**
- Integration test execution: 0 tokens (tests are pure bash)
- Test result documentation: ~8K tokens (this document)

---

## Troubleshooting

### Tests Pass Locally But Fail in CI

**Cause:** Different shell environment or working directory
**Solution:** Ensure working directory is project root and use absolute paths in test commands

### "Cannot cd to project root" Error

**Cause:** Project root check failed
**Solution:** Verify CLAUDE.md exists and contains "DevForgeAI" text

### "File not found" on File That Exists

**Cause:** Working directory is not project root
**Solution:** Run tests from project root:
```bash
cd /mnt/c/Projects/DevForgeAI2
bash devforgeai/tests/STORY-133/test-ac1-subagent-structure.sh
```

### Warnings Not Affecting Pass/Fail

Some tests display warnings (marked with ⚠️) that do not cause test failure:
- These are informational only
- Review but do not block deployment
- Examples: parser limitations, encoding detection failures

---

## Test Maintenance

### Adding New Checks

Edit individual test files and add new TEST blocks:

```bash
# Test N: New check description
echo "TEST N: New check description"
if [ condition ]; then
    echo "  ✓ PASS: Description"
else
    echo "  ✗ FAIL: Description"
    TEST_RESULTS=1
fi
echo ""
```

### Updating Test Files

When the subagent is updated, verify tests still pass. No changes needed unless:
- New required sections added
- Tool list changes
- File size approaches 200 lines

---

## Related Documentation

- **Story File:** `devforgeai/specs/Stories/STORY-133-create-ideation-result-interpreter-subagent.story.md`
- **Subagent File:** `.claude/agents/ideation-result-interpreter.md`
- **Test Results:** `STORY-133-INTEGRATION-TEST-RESULTS.md`
- **Test Summary:** `STORY-133-INTEGRATION-SUMMARY.txt`

---

## Contact & Support

For issues with test execution or results, refer to:
1. This guide's Troubleshooting section
2. Test output error messages (contain specific guidance)
3. Story technical specification for detailed requirements
4. CLAUDE.md for framework integration details

---

**Last Updated:** 2025-12-24
**Test Suite Version:** 1.0
**Framework:** DevForgeAI
**Status:** Production Ready
