#!/bin/bash
# Test: AC#3 - Validation Criteria References Epic Stories
# Story: STORY-349
# Purpose: Verify Validation Criteria section references specific EPIC or STORY IDs
#
# TDD Red Phase: These tests should FAIL until implementation is complete.
# Expected state: ADR-013 Validation Criteria currently has no story references

set -e

ADR_FILE="devforgeai/specs/adrs/ADR-013-treelint-integration.md"
TEST_NAME="AC#3: Validation Criteria References Epic Stories"

echo "=========================================="
echo "Test: ${TEST_NAME}"
echo "File: ${ADR_FILE}"
echo "=========================================="

# Check if ADR file exists
if [ ! -f "${ADR_FILE}" ]; then
    echo "FAIL: ADR file not found: ${ADR_FILE}"
    exit 1
fi

# Track failures
FAILURES=0

# Extract Validation Criteria section
VAL_SECTION=$(sed -n '/^## Validation Criteria/,/^## /p' "${ADR_FILE}" | head -n -1)

if [ -z "${VAL_SECTION}" ]; then
    echo "FAIL: Validation Criteria section not found"
    exit 1
fi

echo ""
echo "Test 3.1: Validation Criteria references EPIC-055 or STORY-XXX"
echo "---------------------------------------------------------------"
# Check for any EPIC-XXX or STORY-XXX reference pattern
if echo "${VAL_SECTION}" | grep -qE '(EPIC-[0-9]+|STORY-[0-9]+)'; then
    echo "PASS: Found epic/story references in Validation Criteria"
    echo "  References found:"
    echo "${VAL_SECTION}" | grep -oE '(EPIC-[0-9]+|STORY-[0-9]+)' | sort -u | head -10
else
    echo "FAIL: No EPIC-XXX or STORY-XXX references found in Validation Criteria"
    echo "  Expected: References to EPIC-055 or specific story IDs"
    echo "  Current Validation Criteria section:"
    echo "${VAL_SECTION}" | head -15
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 3.2: Token reduction metric references validation story"
echo "-------------------------------------------------------------"
# The token reduction metric should reference how it will be validated
# Look for "Token reduction" or "40-80%" with a story/epic reference on same line or nearby
if echo "${VAL_SECTION}" | grep -iE 'token.*reduction|40-80%' | grep -qE '(EPIC-[0-9]+|STORY-[0-9]+|validated|verify|measured)'; then
    echo "PASS: Token reduction metric has validation reference"
else
    echo "FAIL: Token reduction metric lacks validation story reference"
    echo "  Expected: Token reduction row to reference a validation story"
    echo "  Current token reduction line(s):"
    echo "${VAL_SECTION}" | grep -iE 'token|40-80%' | head -3 || echo "  (not found)"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 3.3: Subagent adoption metric references validation mechanism"
echo "-------------------------------------------------------------------"
# The subagent adoption metric should reference how it will be validated
if echo "${VAL_SECTION}" | grep -iE 'subagent.*adoption|100%.*agent' | grep -qE '(EPIC-[0-9]+|STORY-[0-9]+|audit|validated|verify)'; then
    echo "PASS: Subagent adoption metric has validation reference"
else
    echo "FAIL: Subagent adoption metric lacks validation story reference"
    echo "  Expected: Subagent adoption row to reference validation epic (EPIC-057) or story"
    echo "  Current subagent adoption line(s):"
    echo "${VAL_SECTION}" | grep -iE 'subagent|adoption|agent' | head -3 || echo "  (not found)"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 3.4: Validation table includes validation story column or reference"
echo "-------------------------------------------------------------------------"
# Check if the table has been extended to include validation references
# Either a new column or inline references in the Measurement column
if echo "${VAL_SECTION}" | grep -qE '\|.*(EPIC-|STORY-|Validation Story|Validated by)'; then
    echo "PASS: Validation table includes story/epic references"
else
    echo "FAIL: Validation table does not include story/epic references"
    echo "  Expected: Either a 'Validation Story' column or inline references"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "=========================================="
echo "Test Summary: ${TEST_NAME}"
echo "=========================================="
if [ ${FAILURES} -eq 0 ]; then
    echo "RESULT: ALL TESTS PASSED"
    exit 0
else
    echo "RESULT: ${FAILURES} TEST(S) FAILED"
    exit 1
fi
