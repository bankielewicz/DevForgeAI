#!/bin/bash
# STORY-263 COMP-002: Construct canonical gaps.json path from STORY_ID
# Test: Path constructed as 'devforgeai/qa/reports/STORY-XXX-gaps.json'
#
# Expected: FAIL (path construction not yet implemented in Step 0.3)

# Note: No 'set -e' - we need to track failures, not exit on first grep failure

TARGET_FILE="/mnt/c/Projects/DevForgeAI2/.claude/commands/dev.md"
STORY_ID="STORY-263"
TEST_ID="COMP-002"

echo "================================================================"
echo "  ${STORY_ID} - ${TEST_ID}: Canonical gaps.json path construction"
echo "================================================================"
echo ""
echo "Target: ${TARGET_FILE}"
echo ""

# Track test results
TESTS_PASSED=0
TESTS_FAILED=0

# Test C2.1: File exists
echo "Test C2.1: Target file exists"
if [[ -f "${TARGET_FILE}" ]]; then
    echo "  PASS: File exists"
    ((TESTS_PASSED++))
else
    echo "  FAIL: File does not exist"
    ((TESTS_FAILED++))
    echo ""
    echo "RESULT: FAILED (file not found)"
    exit 1
fi

# Test C2.2: Canonical path pattern documented
echo ""
echo "Test C2.2: Canonical path pattern documented"
# Expected: devforgeai/qa/reports/STORY-XXX-gaps.json
if grep -qE "devforgeai/qa/reports/.*gaps\.json" "${TARGET_FILE}"; then
    echo "  PASS: Canonical path pattern found"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Canonical path pattern NOT found"
    echo "        Expected: devforgeai/qa/reports/STORY-XXX-gaps.json"
    ((TESTS_FAILED++))
fi

# Test C2.3: Path uses STORY_ID variable (not hardcoded)
echo ""
echo "Test C2.3: Path uses STORY_ID variable"
# Look for variable interpolation pattern
if grep -qE 'devforgeai/qa/reports/\$\{?STORY_ID\}?.*gaps\.json|STORY_ID.*gaps\.json' "${TARGET_FILE}"; then
    echo "  PASS: Path uses STORY_ID variable"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Path does not use STORY_ID variable"
    echo "        Expected: devforgeai/qa/reports/\${STORY_ID}-gaps.json"
    ((TESTS_FAILED++))
fi

# Test C2.4: Path construction in Step 0.3 context
echo ""
echo "Test C2.4: Path construction in Step 0.3"
STEP_03_CONTENT=$(sed -n '/Step 0\.3/,/Step 0\.4\|Phase 1/p' "${TARGET_FILE}" 2>/dev/null)
if [[ -n "${STEP_03_CONTENT}" ]]; then
    if echo "${STEP_03_CONTENT}" | grep -qE "gaps\.json|qa/reports"; then
        echo "  PASS: Path construction in Step 0.3 context"
        ((TESTS_PASSED++))
    else
        echo "  FAIL: No path construction in Step 0.3"
        ((TESTS_FAILED++))
    fi
else
    echo "  FAIL: Step 0.3 section not found"
    ((TESTS_FAILED++))
fi

# Test C2.5: Path format matches exactly (no variations)
echo ""
echo "Test C2.5: Exact path format (canonical only)"
# Should NOT match versioned files like STORY-086-gaps-v2.json (BR-004)
WRONG_PATTERN=$(grep -oE "gaps-v[0-9]+\.json|gaps_backup\.json" "${TARGET_FILE}" 2>/dev/null)
if [[ -z "${WRONG_PATTERN}" ]]; then
    echo "  PASS: No versioned/backup gap file patterns"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Non-canonical patterns found: ${WRONG_PATTERN}"
    ((TESTS_FAILED++))
fi

# Summary
echo ""
echo "================================================================"
echo "  SUMMARY: ${TEST_ID}"
echo "================================================================"
echo "  Tests Passed: ${TESTS_PASSED}"
echo "  Tests Failed: ${TESTS_FAILED}"
echo ""

if [[ ${TESTS_FAILED} -eq 0 ]]; then
    echo "RESULT: PASSED"
    exit 0
else
    echo "RESULT: FAILED"
    exit 1
fi
