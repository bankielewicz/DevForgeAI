#!/bin/bash
# Test: AC#2 - ADR Documents New Directory Structure
# Story: STORY-339
# Purpose: Verify ADR documents sessions/ and learning/ subdirectories with rationale
#
# TDD Red Phase: This test should FAIL until ADR content is complete.

set -e

ADR_FILE="devforgeai/specs/adrs/ADR-014-memory-directory-structure.md"
TEST_NAME="AC#2: ADR Documents New Directory Structure"

echo "=========================================="
echo "Test: ${TEST_NAME}"
echo "File: ${ADR_FILE}"
echo "=========================================="

# Check if ADR file exists first
if [ ! -f "${ADR_FILE}" ]; then
    echo "FAIL: ADR file not found - cannot verify content"
    exit 1
fi

# Track failures
FAILURES=0

echo ""
echo "Test 2.1: ADR documents sessions/ directory"
echo "--------------------------------------------"
if grep -qi 'sessions/' "${ADR_FILE}"; then
    echo "PASS: ADR mentions sessions/ directory"
else
    echo "FAIL: ADR does not document sessions/ directory"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 2.2: ADR documents learning/ directory"
echo "--------------------------------------------"
if grep -qi 'learning/' "${ADR_FILE}"; then
    echo "PASS: ADR mentions learning/ directory"
else
    echo "FAIL: ADR does not document learning/ directory"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 2.3: ADR has Context section"
echo "----------------------------------"
if grep -qE '^## Context' "${ADR_FILE}"; then
    echo "PASS: ADR has Context section"
else
    echo "FAIL: ADR missing Context section"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 2.4: ADR has Decision section"
echo "-----------------------------------"
if grep -qE '^## Decision' "${ADR_FILE}"; then
    echo "PASS: ADR has Decision section"
else
    echo "FAIL: ADR missing Decision section"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 2.5: ADR has Consequences section"
echo "---------------------------------------"
if grep -qE '^## Consequences' "${ADR_FILE}"; then
    echo "PASS: ADR has Consequences section"
else
    echo "FAIL: ADR missing Consequences section"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 2.6: ADR references EPIC-052"
echo "----------------------------------"
if grep -qi 'EPIC-052' "${ADR_FILE}"; then
    echo "PASS: ADR references EPIC-052"
else
    echo "FAIL: ADR does not reference EPIC-052 as driver for change"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 2.7: ADR has rationale/rationale section or content"
echo "---------------------------------------------------------"
# Check for either a Rationale section header OR the word rationale in content
if grep -qiE '(^## Rationale|rationale)' "${ADR_FILE}"; then
    echo "PASS: ADR contains rationale content"
else
    echo "FAIL: ADR missing rationale for multi-layer memory architecture"
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
