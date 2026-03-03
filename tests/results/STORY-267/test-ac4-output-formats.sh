#!/bin/bash
# STORY-267 AC#4: Success and Failure Output Formats Documented
# Test: Success, failure, timeout, skip output formats with JSON example
#
# Expected: FAIL (documentation not yet expanded with all output format examples)

# Note: No 'set -e' - we need to track failures, not exit on first grep failure

TARGET_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-qa/references/deep-validation-workflow.md"
STORY_ID="STORY-267"
AC_NUM="AC#4"

echo "================================================================"
echo "  ${STORY_ID} - ${AC_NUM}: Success and Failure Output Formats Documented"
echo "================================================================"
echo ""
echo "Target: ${TARGET_FILE}"
echo ""

# Track test results
TESTS_PASSED=0
TESTS_FAILED=0

# Check file exists
if [[ ! -f "${TARGET_FILE}" ]]; then
    echo "FAIL: Target file does not exist"
    exit 1
fi

# Extract the Runtime Smoke Test section
SECTION_CONTENT=""
if grep -q "^### 1\.4 Runtime Smoke Test" "${TARGET_FILE}"; then
    SECTION_CONTENT=$(sed -n '/^### 1\.4 Runtime Smoke Test/,/^##[#]* [0-9]/p' "${TARGET_FILE}")
elif grep -q "^### 1\.3 Runtime Smoke Test" "${TARGET_FILE}"; then
    echo "Note: Section 1.4 not found, checking section 1.3 (current state)"
    SECTION_CONTENT=$(sed -n '/^### 1\.3 Runtime Smoke Test/,/^##[#]* [0-9]/p' "${TARGET_FILE}")
fi

# Test 4.1: Success output format documented
echo "Test 4.1: Success output format documented"
# Per AC#4: "Runtime smoke test PASSED: {language} CLI is executable"
if echo "${SECTION_CONTENT}" | grep -qiE "PASS(ED)?.*smoke.*test|smoke.*test.*PASS|success.*output|output.*success|Runtime.*smoke.*test.*PASS"; then
    echo "  PASS: Success output format documented"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Success output format not documented"
    echo "        Expected: 'Runtime smoke test PASSED: {language} CLI is executable'"
    ((TESTS_FAILED++))
fi

# Test 4.2: Failure output format documented
echo ""
echo "Test 4.2: Failure output format documented"
if echo "${SECTION_CONTENT}" | grep -qiE "FAIL(ED)?.*smoke.*test|smoke.*test.*FAIL|failure.*output|output.*failure|CRITICAL.*violation"; then
    echo "  PASS: Failure output format documented"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Failure output format not documented"
    ((TESTS_FAILED++))
fi

# Test 4.3: Timeout output format documented
echo ""
echo "Test 4.3: Timeout output format documented"
if echo "${SECTION_CONTENT}" | grep -qiE "timeout.*(10s|output|format)|>.*10.*second|exceed.*timeout"; then
    echo "  PASS: Timeout output format documented"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Timeout output format not documented"
    echo "        Expected: Documentation of >10s timeout behavior"
    ((TESTS_FAILED++))
fi

# Test 4.4: Skip output format documented
echo ""
echo "Test 4.4: Skip output format documented"
if echo "${SECTION_CONTENT}" | grep -qiE "SKIP(PED)?.*output|skip.*(format|library|unsupported)|output.*skip"; then
    echo "  PASS: Skip output format documented"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Skip output format not documented"
    echo "        Expected: Documentation for library/unsupported language skip behavior"
    ((TESTS_FAILED++))
fi

# Test 4.5: JSON violation example exists (for gaps.json integration)
echo ""
echo "Test 4.5: JSON violation example exists"
# Look for JSON code block with violation structure
JSON_BLOCK=$(echo "${SECTION_CONTENT}" | sed -n '/```json/,/```/p')

if [[ -n "${JSON_BLOCK}" ]]; then
    # Check if JSON contains violation-related fields
    if echo "${JSON_BLOCK}" | grep -qiE '"(type|severity|violation|RUNTIME_EXECUTION_FAILURE)"'; then
        echo "  PASS: JSON violation example found with violation fields"
        ((TESTS_PASSED++))
    else
        echo "  FAIL: JSON block found but missing violation structure"
        echo "        Expected: JSON with 'type', 'severity', or 'RUNTIME_EXECUTION_FAILURE'"
        ((TESTS_FAILED++))
    fi
else
    echo "  FAIL: No JSON code block found"
    echo "        Expected: JSON example showing violation format for gaps.json"
    ((TESTS_FAILED++))
fi

# Test 4.6: CRITICAL violation type mentioned
echo ""
echo "Test 4.6: CRITICAL violation type for runtime failures"
if echo "${SECTION_CONTENT}" | grep -qiE "CRITICAL.*(violation|severity)|severity.*CRITICAL|RUNTIME_EXECUTION_FAILURE"; then
    echo "  PASS: CRITICAL violation type documented"
    ((TESTS_PASSED++))
else
    echo "  FAIL: CRITICAL violation type not documented"
    echo "        Expected: RUNTIME_EXECUTION_FAILURE as CRITICAL severity"
    ((TESTS_FAILED++))
fi

# Test 4.7: gaps.json integration mentioned
echo ""
echo "Test 4.7: gaps.json integration documented"
if echo "${SECTION_CONTENT}" | grep -qiE "gaps\.json|gaps.*json"; then
    echo "  PASS: gaps.json integration documented"
    ((TESTS_PASSED++))
else
    echo "  FAIL: gaps.json integration not documented"
    ((TESTS_FAILED++))
fi

# Summary
echo ""
echo "================================================================"
echo "  SUMMARY: ${AC_NUM}"
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
