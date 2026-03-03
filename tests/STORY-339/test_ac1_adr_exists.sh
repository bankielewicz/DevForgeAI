#!/bin/bash
# Test: AC#1 - ADR Document Created
# Story: STORY-339
# Purpose: Verify ADR-014-memory-directory-structure.md exists in devforgeai/specs/adrs/
#
# TDD Red Phase: This test should FAIL until ADR document is created.
# Expected state: ADR file does not exist yet.

set -e

ADR_FILE="devforgeai/specs/adrs/ADR-014-memory-directory-structure.md"
TEST_NAME="AC#1: ADR Document Created"

echo "=========================================="
echo "Test: ${TEST_NAME}"
echo "File: ${ADR_FILE}"
echo "=========================================="

# Track failures
FAILURES=0

echo ""
echo "Test 1.1: ADR file exists at correct path"
echo "------------------------------------------"
if [ -f "${ADR_FILE}" ]; then
    echo "PASS: ADR file exists"
else
    echo "FAIL: ADR file not found: ${ADR_FILE}"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 1.2: ADR has valid YAML frontmatter"
echo "-----------------------------------------"
if [ -f "${ADR_FILE}" ]; then
    # Check for YAML frontmatter (starts with --- and ends with ---)
    if head -1 "${ADR_FILE}" | grep -q '^---$'; then
        echo "PASS: ADR has YAML frontmatter start marker"
    else
        echo "FAIL: ADR missing YAML frontmatter start marker (---)"
        FAILURES=$((FAILURES + 1))
    fi
else
    echo "SKIP: Cannot check frontmatter - file does not exist"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 1.3: ADR has required 'id' field in frontmatter"
echo "-----------------------------------------------------"
if [ -f "${ADR_FILE}" ]; then
    if grep -qE '^id:\s*ADR-014' "${ADR_FILE}"; then
        echo "PASS: ADR has id field with ADR-014"
    else
        echo "FAIL: ADR missing or incorrect 'id' field"
        echo "  Expected: id: ADR-014"
        FAILURES=$((FAILURES + 1))
    fi
else
    echo "SKIP: Cannot check id field - file does not exist"
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
