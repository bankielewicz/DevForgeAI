#!/bin/bash
# STORY-267 AC#1: Documentation Section Added to Reference File
# Test: Section "1.4 Runtime Smoke Test" exists after section "1.3"
#
# Expected: FAIL (documentation not yet expanded - current section is 1.3 not 1.4)

# Note: No 'set -e' - we need to track failures, not exit on first grep failure

TARGET_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-qa/references/deep-validation-workflow.md"
STORY_ID="STORY-267"
AC_NUM="AC#1"

echo "================================================================"
echo "  ${STORY_ID} - ${AC_NUM}: Section 1.4 Runtime Smoke Test Exists"
echo "================================================================"
echo ""
echo "Target: ${TARGET_FILE}"
echo ""

# Track test results
TESTS_PASSED=0
TESTS_FAILED=0

# Test 1.1: File exists
echo "Test 1.1: Target file exists"
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

# Test 1.2: Section header "### 1.4 Runtime Smoke Test" exists
# Note: Current state has "### 1.3 Runtime Smoke Test" - needs renumbering
echo ""
echo "Test 1.2: Section '### 1.4 Runtime Smoke Test' exists"
if grep -qE "^### 1\.4 Runtime Smoke Test" "${TARGET_FILE}"; then
    echo "  PASS: Section 1.4 Runtime Smoke Test found"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Section 1.4 Runtime Smoke Test NOT found"
    echo "        (Current state likely has 1.3 - needs renumbering)"
    ((TESTS_FAILED++))
fi

# Test 1.3: Section appears AFTER section 1.3 (Documentation Accuracy Validation should be renumbered to 1.5)
echo ""
echo "Test 1.3: Section 1.4 appears after section 1.3"
SECTION_13_LINE=$(grep -n "^### 1\.3" "${TARGET_FILE}" | head -1 | cut -d: -f1)
SECTION_14_LINE=$(grep -n "^### 1\.4 Runtime Smoke Test" "${TARGET_FILE}" | head -1 | cut -d: -f1)

if [[ -n "${SECTION_13_LINE}" && -n "${SECTION_14_LINE}" ]]; then
    if [[ ${SECTION_14_LINE} -gt ${SECTION_13_LINE} ]]; then
        echo "  PASS: Section 1.4 (line ${SECTION_14_LINE}) appears after 1.3 (line ${SECTION_13_LINE})"
        ((TESTS_PASSED++))
    else
        echo "  FAIL: Section ordering incorrect"
        ((TESTS_FAILED++))
    fi
else
    echo "  FAIL: Could not find both sections 1.3 and 1.4"
    echo "        Section 1.3 line: ${SECTION_13_LINE:-NOT FOUND}"
    echo "        Section 1.4 line: ${SECTION_14_LINE:-NOT FOUND}"
    ((TESTS_FAILED++))
fi

# Test 1.4: Section follows established documentation format (has Purpose, Steps, Code blocks)
echo ""
echo "Test 1.4: Section follows documentation format (Purpose, Steps, Code blocks)"
# Extract section content between "### 1.4" and next "### " or "## "
SECTION_CONTENT=$(sed -n '/^### 1\.4 Runtime Smoke Test/,/^##[#]* [0-9]/p' "${TARGET_FILE}" | head -100)

FORMAT_CHECKS=0

# Check for Purpose statement
if echo "${SECTION_CONTENT}" | grep -qiE "(Purpose|purpose)"; then
    echo "  - Purpose statement: FOUND"
    ((FORMAT_CHECKS++))
else
    echo "  - Purpose statement: NOT FOUND"
fi

# Check for Step references
if echo "${SECTION_CONTENT}" | grep -qE "Step [0-9]"; then
    echo "  - Step references: FOUND"
    ((FORMAT_CHECKS++))
else
    echo "  - Step references: NOT FOUND"
fi

# Check for code blocks
if echo "${SECTION_CONTENT}" | grep -qE '```'; then
    echo "  - Code blocks: FOUND"
    ((FORMAT_CHECKS++))
else
    echo "  - Code blocks: NOT FOUND"
fi

if [[ ${FORMAT_CHECKS} -ge 2 ]]; then
    echo "  PASS: Section follows documentation format (${FORMAT_CHECKS}/3 elements found)"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Section missing required format elements (${FORMAT_CHECKS}/3 found)"
    ((TESTS_FAILED++))
fi

# Test 1.5: Section is comprehensive (>50 lines, not just 6-step summary)
echo ""
echo "Test 1.5: Section is comprehensive (>50 lines)"
if [[ -n "${SECTION_CONTENT}" ]]; then
    LINE_COUNT=$(echo "${SECTION_CONTENT}" | wc -l)
    if [[ ${LINE_COUNT} -gt 50 ]]; then
        echo "  PASS: Section has ${LINE_COUNT} lines (comprehensive)"
        ((TESTS_PASSED++))
    else
        echo "  FAIL: Section has only ${LINE_COUNT} lines (expected >50 for comprehensive docs)"
        ((TESTS_FAILED++))
    fi
else
    echo "  FAIL: Could not extract section content"
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
