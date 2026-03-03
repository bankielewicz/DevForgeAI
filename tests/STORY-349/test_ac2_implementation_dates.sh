#!/bin/bash
# Test: AC#2 - Implementation Plan Section Has Concrete Dates
# Story: STORY-349
# Purpose: Verify each phase in Implementation Plan has concrete date ranges
#
# TDD Red Phase: These tests should FAIL until implementation is complete.
# Expected state: ADR-013 currently has generic "Week X-Y" without specific dates

set -e

ADR_FILE="devforgeai/specs/adrs/ADR-013-treelint-integration.md"
TEST_NAME="AC#2: Implementation Plan Has Concrete Dates"

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

# Extract Implementation Plan section
IMPL_SECTION=$(sed -n '/^## Implementation Plan/,/^## /p' "${ADR_FILE}" | head -n -1)

if [ -z "${IMPL_SECTION}" ]; then
    echo "FAIL: Implementation Plan section not found"
    exit 1
fi

echo ""
echo "Test 2.1: Phase 1 has concrete date range (e.g., 'Feb 3-7')"
echo "------------------------------------------------------------"
# Pattern: Phase 1: ... followed by date like "Feb X-Y" or "February X-Y"
# Example: "### Phase 1: Foundation (Week 1-2: Feb 3-7)"
if echo "${IMPL_SECTION}" | grep -qiE 'Phase 1.*\((Week [0-9]+-?[0-9]*:?\s*)?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+[0-9]+-[0-9]+'; then
    echo "PASS: Phase 1 has concrete date range"
else
    echo "FAIL: Phase 1 does NOT have concrete date range"
    echo "  Expected pattern: Phase 1: ... (Week X-Y: Month DD-DD) or (Month DD-DD)"
    echo "  Current Phase 1 line:"
    echo "${IMPL_SECTION}" | grep -i "Phase 1" | head -1 || echo "  (Phase 1 not found)"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 2.2: Phase 2 has concrete date range"
echo "------------------------------------------"
if echo "${IMPL_SECTION}" | grep -qiE 'Phase 2.*\((Week [0-9]+-?[0-9]*:?\s*)?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+[0-9]+-[0-9]+'; then
    echo "PASS: Phase 2 has concrete date range"
else
    echo "FAIL: Phase 2 does NOT have concrete date range"
    echo "  Expected pattern: Phase 2: ... (Week X-Y: Month DD-DD)"
    echo "  Current Phase 2 line:"
    echo "${IMPL_SECTION}" | grep -i "Phase 2" | head -1 || echo "  (Phase 2 not found)"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 2.3: Phase 3 has concrete date range"
echo "------------------------------------------"
if echo "${IMPL_SECTION}" | grep -qiE 'Phase 3.*\((Week [0-9]+-?[0-9]*:?\s*)?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+[0-9]+-[0-9]+'; then
    echo "PASS: Phase 3 has concrete date range"
else
    echo "FAIL: Phase 3 does NOT have concrete date range"
    echo "  Expected pattern: Phase 3: ... (Week X-Y: Month DD-DD)"
    echo "  Current Phase 3 line:"
    echo "${IMPL_SECTION}" | grep -i "Phase 3" | head -1 || echo "  (Phase 3 not found)"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 2.4: Phase 4 has concrete date range"
echo "------------------------------------------"
if echo "${IMPL_SECTION}" | grep -qiE 'Phase 4.*\((Week [0-9]+-?[0-9]*:?\s*)?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+[0-9]+-[0-9]+'; then
    echo "PASS: Phase 4 has concrete date range"
else
    echo "FAIL: Phase 4 does NOT have concrete date range"
    echo "  Expected pattern: Phase 4: ... (Week X-Y: Month DD-DD)"
    echo "  Current Phase 4 line:"
    echo "${IMPL_SECTION}" | grep -i "Phase 4" | head -1 || echo "  (Phase 4 not found)"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 2.5: No generic 'Week X' without dates remains"
echo "----------------------------------------------------"
# Check for generic "Week X-Y)" patterns without month/date (indicates incomplete)
# This catches patterns like "(Week 1-2)" without a following date
if echo "${IMPL_SECTION}" | grep -qE '\(Week [0-9]+-[0-9]+\)\s*$'; then
    echo "FAIL: Found generic Week pattern without concrete dates"
    echo "  Lines with generic Week patterns:"
    echo "${IMPL_SECTION}" | grep -E '\(Week [0-9]+-[0-9]+\)\s*$' || true
    FAILURES=$((FAILURES + 1))
else
    echo "PASS: No generic Week patterns without dates found"
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
