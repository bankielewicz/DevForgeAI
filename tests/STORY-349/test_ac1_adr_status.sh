#!/bin/bash
# Test: AC#1 - ADR Status Updated to APPROVED
# Story: STORY-349
# Purpose: Verify ADR-013 status is changed from PROPOSED to APPROVED
#
# TDD Red Phase: These tests should FAIL until implementation is complete.
# Expected state: ADR-013 currently has status: "PROPOSED"

set -e

ADR_FILE="devforgeai/specs/adrs/ADR-013-treelint-integration.md"
TEST_NAME="AC#1: ADR Status Updated to APPROVED"

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

echo ""
echo "Test 1.1: YAML frontmatter status field equals 'APPROVED'"
echo "---------------------------------------------------------"
# The status field in YAML frontmatter should be "APPROVED"
# Pattern: status: "APPROVED" (with quotes) or status: APPROVED (without quotes)
if grep -qE '^status:\s*"?APPROVED"?\s*$' "${ADR_FILE}"; then
    echo "PASS: YAML status field is 'APPROVED'"
else
    echo "FAIL: YAML status field is NOT 'APPROVED'"
    echo "  Expected: status: \"APPROVED\" or status: APPROVED"
    echo "  Current value:"
    grep -E '^status:' "${ADR_FILE}" || echo "  (status field not found)"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 1.2: Status section header shows '**APPROVED** - [date]'"
echo "--------------------------------------------------------------"
# The Status section should have a line like: **APPROVED** - 2026-01-31
# Pattern: **APPROVED** followed by " - " and a date (YYYY-MM-DD format)
if grep -qE '\*\*APPROVED\*\*\s*-\s*[0-9]{4}-[0-9]{2}-[0-9]{2}' "${ADR_FILE}"; then
    echo "PASS: Status section header shows APPROVED with date"
else
    echo "FAIL: Status section header does NOT show APPROVED with date"
    echo "  Expected: **APPROVED** - YYYY-MM-DD"
    echo "  Current Status section content:"
    # Show Status section content (lines after ## Status until next ##)
    sed -n '/^## Status/,/^##/p' "${ADR_FILE}" | head -5 || echo "  (Status section not found)"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 1.3: Status is NOT 'PROPOSED' anymore"
echo "-------------------------------------------"
# Ensure the old PROPOSED status is no longer present in the Status section
if grep -qE '\*\*PROPOSED\*\*' "${ADR_FILE}"; then
    echo "FAIL: Status section still contains **PROPOSED**"
    echo "  The old PROPOSED status should be replaced with APPROVED"
    FAILURES=$((FAILURES + 1))
else
    echo "PASS: No **PROPOSED** marker found in Status section"
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
