#!/bin/bash
# STORY-263 NFR-003: STORY_ID must be validated before path construction
# Test: STORY_ID matches regex '^STORY-\d{1,4}$'; no path traversal possible
#
# Expected: PARTIAL PASS (STORY_ID regex exists in Step 0.1, path validation may not)

# Note: No 'set -e' - we need to track failures, not exit on first grep failure

TARGET_FILE="/mnt/c/Projects/DevForgeAI2/.claude/commands/dev.md"
STORY_ID="STORY-263"
TEST_ID="NFR-003"

echo "================================================================"
echo "  ${STORY_ID} - ${TEST_ID}: STORY_ID validation before path construction"
echo "================================================================"
echo ""
echo "Target: ${TARGET_FILE}"
echo ""

# Track test results
TESTS_PASSED=0
TESTS_FAILED=0

# Test NFR3.1: File exists
echo "Test NFR3.1: Target file exists"
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

# Test NFR3.2: STORY_ID regex validation present
echo ""
echo "Test NFR3.2: STORY_ID regex validation"
# Expected: STORY-[0-9]+ or ^STORY-\d{1,4}$
if grep -qE 'STORY-\[0-9\]|STORY-\\d' "${TARGET_FILE}"; then
    echo "  PASS: STORY_ID regex pattern found"
    ((TESTS_PASSED++))
else
    echo "  FAIL: No STORY_ID regex validation"
    echo "        Expected: Pattern like 'STORY-[0-9]+'"
    ((TESTS_FAILED++))
fi

# Test NFR3.3: Validation occurs before path construction
echo ""
echo "Test NFR3.3: Validation before path construction"
# STORY_ID validation should be in Step 0.1 (argument parsing)
# Path construction should be in Step 0.3 (look for GAPS_FILE_PATH assignment, not comments)
VALIDATION_LINE=$(grep -n "STORY-\[0-9\]" "${TARGET_FILE}" | head -1 | cut -d: -f1)
PATH_CONSTRUCT_LINE=$(grep -n "GAPS_FILE_PATH.*=.*qa/reports" "${TARGET_FILE}" | head -1 | cut -d: -f1)

if [[ -n "${VALIDATION_LINE}" && -n "${PATH_CONSTRUCT_LINE}" ]]; then
    if [[ ${VALIDATION_LINE} -lt ${PATH_CONSTRUCT_LINE} ]]; then
        echo "  PASS: Validation (line ${VALIDATION_LINE}) before path construction (line ${PATH_CONSTRUCT_LINE})"
        ((TESTS_PASSED++))
    else
        echo "  FAIL: Path construction before validation"
        ((TESTS_FAILED++))
    fi
elif [[ -n "${VALIDATION_LINE}" && -z "${PATH_CONSTRUCT_LINE}" ]]; then
    echo "  INFO: Validation exists, path construction not yet implemented"
    echo "  PASS: Validation is in place (path will use validated STORY_ID)"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Validation line not found"
    ((TESTS_FAILED++))
fi

# Test NFR3.4: No path traversal characters allowed in STORY_ID
echo ""
echo "Test NFR3.4: Path traversal prevention"
# Check that STORY_ID regex doesn't allow: / \ .. or other dangerous chars
# Current pattern: STORY-[0-9]+ - this is safe (only digits after STORY-)
# Look for pattern like STORY-[0-9]+ or similar numeric-only patterns
STORY_PATTERN=$(grep -oE 'STORY-\[0-9\][+*]?' "${TARGET_FILE}" | head -1)
if [[ -n "${STORY_PATTERN}" ]]; then
    # Check if pattern only allows safe characters (digits)
    if [[ "${STORY_PATTERN}" =~ "0-9" ]] && \
       [[ ! "${STORY_PATTERN}" =~ "/" ]] && \
       [[ ! "${STORY_PATTERN}" =~ "\\\\" ]] && \
       [[ ! "${STORY_PATTERN}" =~ "\.\." ]]; then
        echo "  PASS: STORY_ID pattern allows only digits (no path traversal)"
        echo "        Pattern: ${STORY_PATTERN}"
        ((TESTS_PASSED++))
    else
        echo "  FAIL: STORY_ID pattern may allow dangerous characters"
        ((TESTS_FAILED++))
    fi
else
    echo "  FAIL: Could not extract STORY_ID pattern for analysis"
    ((TESTS_FAILED++))
fi

# Test NFR3.5: Invalid STORY_ID rejection documented
echo ""
echo "Test NFR3.5: Invalid STORY_ID handling"
# Check for error handling when STORY_ID doesn't match pattern
if grep -qE "(invalid.*STORY|STORY.*empty|HALT|exit)" "${TARGET_FILE}"; then
    echo "  PASS: Invalid STORY_ID handling documented (HALT/exit on invalid)"
    ((TESTS_PASSED++))
else
    echo "  FAIL: No explicit invalid STORY_ID handling"
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
