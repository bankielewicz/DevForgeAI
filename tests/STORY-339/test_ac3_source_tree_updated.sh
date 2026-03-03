#!/bin/bash
# Test: AC#3 - Source Tree Updated After ADR Approval
# Story: STORY-339
# Purpose: Verify source-tree.md contains .claude/memory/sessions/ and .claude/memory/learning/
#
# TDD Red Phase: This test should FAIL until source-tree.md is updated.

set -e

SOURCE_TREE_FILE="devforgeai/specs/context/source-tree.md"
TEST_NAME="AC#3: Source Tree Updated After ADR Approval"

echo "=========================================="
echo "Test: ${TEST_NAME}"
echo "File: ${SOURCE_TREE_FILE}"
echo "=========================================="

# Check if source-tree.md exists
if [ ! -f "${SOURCE_TREE_FILE}" ]; then
    echo "FAIL: Source tree file not found: ${SOURCE_TREE_FILE}"
    exit 1
fi

# Track failures
FAILURES=0

echo ""
echo "Test 3.1: source-tree.md contains sessions/ entry under memory/"
echo "----------------------------------------------------------------"
# Tree notation uses pipes and dashes, check for sessions/ under memory directory
if grep -qE 'sessions/' "${SOURCE_TREE_FILE}"; then
    echo "PASS: source-tree.md contains sessions/ entry"
else
    echo "FAIL: source-tree.md missing sessions/ entry"
    echo "  Expected: Directory entry for sessions/ under memory/"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 3.2: source-tree.md contains learning/ entry under memory/"
echo "----------------------------------------------------------------"
if grep -qE 'learning/' "${SOURCE_TREE_FILE}"; then
    echo "PASS: source-tree.md contains learning/ entry"
else
    echo "FAIL: source-tree.md missing learning/ entry"
    echo "  Expected: Directory entry for learning/ under memory/"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 3.3: sessions/ directory has description"
echo "----------------------------------------------"
# Check that sessions/ entry has accompanying description with comment
if grep 'sessions/' "${SOURCE_TREE_FILE}" | grep -qiE '(session|state|memory|workflow|artifact)'; then
    echo "PASS: sessions/ entry has descriptive context"
else
    echo "FAIL: sessions/ entry lacks description"
    echo "  Expected: Description explaining purpose of sessions/ directory"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 3.4: learning/ directory has description"
echo "----------------------------------------------"
# Check that learning/ entry has accompanying description
if grep 'learning/' "${SOURCE_TREE_FILE}" | grep -qiE '(learn|pattern|knowledge|improvement|framework)'; then
    echo "PASS: learning/ entry has descriptive context"
else
    echo "FAIL: learning/ entry lacks description"
    echo "  Expected: Description explaining purpose of learning/ directory"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "Test 3.5: Version number updated (indicates change)"
echo "----------------------------------------------------"
# Check version is higher than 3.4 (current version before this change)
# Note: source-tree.md uses **Version**: format (markdown bold)
CURRENT_VERSION=$(grep -oE '\*\*Version\*\*:\s*[0-9]+\.[0-9]+' "${SOURCE_TREE_FILE}" | grep -oE '[0-9]+\.[0-9]+' | head -1)
if [ -n "${CURRENT_VERSION}" ]; then
    # Compare versions: must be > 3.4
    MAJOR=$(echo "${CURRENT_VERSION}" | cut -d. -f1)
    MINOR=$(echo "${CURRENT_VERSION}" | cut -d. -f2)
    if [ "${MAJOR}" -gt 3 ] || ([ "${MAJOR}" -eq 3 ] && [ "${MINOR}" -gt 4 ]); then
        echo "PASS: Version updated to ${CURRENT_VERSION} (> 3.4)"
    else
        echo "FAIL: Version not updated (current: ${CURRENT_VERSION}, expected: > 3.4)"
        FAILURES=$((FAILURES + 1))
    fi
else
    echo "FAIL: Could not determine version from source-tree.md"
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
