#!/bin/bash
# Test: AC#4 - Decision Record Table Updated
# Story: STORY-349
# Purpose: Verify Decision Record table has new approval row
#
# TDD Red Phase: These tests should FAIL until implementation is complete.
# Expected state: ADR-013 Decision Record currently has "TBD" entries

set -e

ADR_FILE="devforgeai/specs/adrs/ADR-013-treelint-integration.md"
TEST_NAME="AC#4: Decision Record Table Updated"

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

# Extract Decision Record section
RECORD_SECTION=$(sed -n '/^## Decision Record/,/^## /p' "${ADR_FILE}")

if [ -z "${RECORD_SECTION}" ]; then
    # Try alternate location - may be at end of file
    RECORD_SECTION=$(sed -n '/^## Decision Record/,$p' "${ADR_FILE}")
fi

if [ -z "${RECORD_SECTION}" ]; then
    echo "FAIL: Decision Record section not found"
    exit 1
fi

echo ""
echo "Test 4.1: Decision Record has row with 'ADR approved' action"
echo "-------------------------------------------------------------"
# Look for a table row with "ADR approved" (case insensitive)
if echo "${RECORD_SECTION}" | grep -qiE '\|.*ADR\s*approved.*\|'; then
    echo "PASS: Found 'ADR approved' action in Decision Record"
else
    echo "FAIL: No 'ADR approved' action found in Decision Record"
    echo "  Expected: A table row with action 'ADR approved'"
    echo "  Current Decision Record table:"
    echo "${RECORD_SECTION}" | grep -E '^\|' | head -10 || echo "  (table not found)"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 4.2: Approval row has 'Framework Architect' as approver"
echo "-------------------------------------------------------------"
# Look for a table row with "Framework Architect" in the approver/By column
if echo "${RECORD_SECTION}" | grep -qiE '\|.*Framework\s*Architect.*\|'; then
    echo "PASS: Found 'Framework Architect' as approver"
else
    echo "FAIL: No 'Framework Architect' approver found"
    echo "  Expected: A table row with 'Framework Architect' in the By column"
    echo "  Current Decision Record rows:"
    echo "${RECORD_SECTION}" | grep -E '^\|' | head -10 || echo "  (table not found)"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 4.3: Approval row has a valid date (not TBD)"
echo "--------------------------------------------------"
# Check for approval row with actual date, not "TBD"
# Pattern: | YYYY-MM-DD | ... ADR approved ... | or | Month DD, YYYY | ...
if echo "${RECORD_SECTION}" | grep -iE 'ADR\s*approved' | grep -qE '\|\s*[0-9]{4}-[0-9]{2}-[0-9]{2}\s*\|'; then
    echo "PASS: Approval row has valid date format (YYYY-MM-DD)"
else
    echo "FAIL: Approval row does not have valid date"
    echo "  Expected: Date in YYYY-MM-DD format on ADR approved row"
    echo "  Current approval-related rows:"
    echo "${RECORD_SECTION}" | grep -iE '(approved|TBD)' | head -5 || echo "  (not found)"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 4.4: No remaining 'TBD' entries for approval"
echo "--------------------------------------------------"
# The TBD entries for approval should be replaced with actual dates
# Check if there's still a TBD associated with approval actions
if echo "${RECORD_SECTION}" | grep -iE '\|\s*TBD\s*\|.*approved'; then
    echo "FAIL: Still found TBD entries for approval actions"
    echo "  TBD entries found:"
    echo "${RECORD_SECTION}" | grep -iE 'TBD' | head -5
    FAILURES=$((FAILURES + 1))
else
    echo "PASS: No TBD entries remaining for approval"
fi

echo ""
echo "Test 4.5: Table structure is valid (3 columns: Date, Action, By)"
echo "-----------------------------------------------------------------"
# Verify table has proper structure with header row
if echo "${RECORD_SECTION}" | grep -qE '^\|\s*Date\s*\|\s*Action\s*\|\s*By\s*\|'; then
    echo "PASS: Decision Record table has valid header structure"
else
    echo "FAIL: Decision Record table header structure invalid"
    echo "  Expected: | Date | Action | By |"
    echo "  Current header row:"
    echo "${RECORD_SECTION}" | grep -E '^\|' | head -2 || echo "  (not found)"
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
